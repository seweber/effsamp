"""A18: several dense 3-qubit gates per HBM pass, chained in registers on the tensor cores, complex32 storage.

The brainstorm of PLAN_ADDITIONAL_NOTES_1.md proposes to apply several 3-qubit unitaries per read and
write of a complex32 (FP16 pair) state, keeping the amplitudes on chip between `mma.sync` products.
This benchmark measures that design in isolation, outside noisecirc.

Tensor-core kernel (`tc`). A warp holds tiles of 128 amplitudes (the 7 low qubits) as the A operand
of `mma.sync.m16n8k16` (FP16 inputs, FP32 accumulation): row index = qubits 3..6 (16 rows), column
index = qubits 0..2, real parts in columns 0..7 and imaginary parts in 8..15. A gate U on the column
qubits is the right product with the real form [[Re U^T, Im U^T], [-Im U^T, Re U^T]], two products
(real and imaginary output columns) per tile (split 1); four with the matrix split into an FP16
leading part and an FP16 rest (split 2, `f16x2`); six with the amplitudes split as well (split 3,
`f16x3`: lead x rest, rest x lead, lead x lead, Ootomo and Yokota), which keeps single precision
between gates. The accumulators of one product are, after conversion to FP16, exactly the A
fragments of the next (no shuffles). Between gates on different triples (`switch` 1) `movmatrix.trans`
swaps qubits 0..2 with 3..5 in registers, or (`switch` 2) the warp stores its tiles to shared memory
and loads them transposed, as at a stage boundary of a shared-memory tile. `tiles` independent tiles
per warp are interleaved to hide latency.

CUDA-core kernel (`cuda`). A thread holds 8 amplitudes (one triple group of qubits 0..2) in FP32 and
applies each gate as a dense complex 8x8 product (32 FMA per amplitude); between gates on different
triples, the warp's 256 amplitudes are transposed through shared memory.

Structured CUDA-core kernel (`cudas`). Like `cuda`, but each stage applies `rot` real two-term
rotations (noisecirc's rotation form) instead of a dense product: 2 * rot floating-point
instructions per amplitude and stage, the range of noisecirc's contracted 3-qubit stages (3 to 18).

All alternate gates between qubits 0..2 and 3..5 (`switch` 1, 2) or apply all to 0..2 (`switch` 0).
Prints, per kernel, mode, tiles and gate count, the pass time over the copy-kernel time t_bw at
n qubits, and the tensor-core TFLOP/s of the products. `--check` compares with NumPy at 12 qubits.

Usage: a18_chain.py [--qubits 28] [--check]
"""

import argparse
import json

import cupy as cp
import numpy as np

SOURCE = r"""
#include <cuda_fp16.h>
typedef unsigned int u32;

__device__ __forceinline__ void mma(float (&d)[4], const u32 (&a)[4], u32 b0, u32 b1) {
    asm("mma.sync.aligned.m16n8k16.row.col.f32.f16.f16.f32 {%0,%1,%2,%3}, {%4,%5,%6,%7}, {%8,%9}, {%0,%1,%2,%3};"
        : "+f"(d[0]), "+f"(d[1]), "+f"(d[2]), "+f"(d[3]) : "r"(a[0]), "r"(a[1]), "r"(a[2]), "r"(a[3]), "r"(b0), "r"(b1));
}
__device__ __forceinline__ u32 pack(float lo, float hi) {
    u32 r;
    asm("cvt.rn.f16x2.f32 %0, %1, %2;" : "=r"(r) : "f"(hi), "f"(lo));
    return r;
}
__device__ __forceinline__ u32 trans(u32 a) {
    u32 r;
    asm("movmatrix.sync.aligned.m8n8.trans.b16 %0, %1;" : "=r"(r) : "r"(a));
    return r;
}


// The FP16 pair of the rest of (x, y) after its leading FP16 pair `lead`.
__device__ __forceinline__ u32 rest(float x, float y, u32 lead) {
    __half2 h = *reinterpret_cast<__half2*>(&lead);
    float2 f = __half22float2(h);
    return pack(x - f.x, y - f.y);
}

// Swizzled word position of amplitude i of a warp's tile: conflict-free stores and transposed loads.
__device__ __forceinline__ int sw(int i) { return i ^ (((i >> 5) & 1) << 3); }

// Swap qubits 0..2 with 3..5 through shared memory, as a stage boundary of a shared-memory tile does.
template <int TILES, int SPLIT>
__device__ __forceinline__ void relayout(u32 (&a)[TILES][4], u32 (&lo)[TILES][4], u32* buffer) {
    const int lane = threadIdx.x & 31, g = lane >> 2, c = lane & 3;
#pragma unroll
    for (int part = 0; part < (SPLIT == 3 ? 2 : 1); ++part) {
        u32 (&x)[TILES][4] = part ? lo : a;
        __syncwarp();
#pragma unroll
        for (int t = 0; t < TILES; ++t)
#pragma unroll
            for (int h = 0; h < 2; ++h) {
                int i = 64 * h + 8 * g + 2 * c;
                *reinterpret_cast<uint2*>(buffer + t * 128 + sw(i)) =
                    make_uint2(__byte_perm(x[t][h], x[t][h + 2], 0x5410), __byte_perm(x[t][h], x[t][h + 2], 0x7632));
            }
        __syncwarp();
#pragma unroll
        for (int t = 0; t < TILES; ++t)
#pragma unroll
            for (int h = 0; h < 2; ++h) {
                // row' = g (old column), columns' 2c, 2c + 1 (old rows)
                u32 w0 = buffer[t * 128 + sw(64 * h + 16 * c + g)], w1 = buffer[t * 128 + sw(64 * h + 16 * c + 8 + g)];
                x[t][h] = __byte_perm(w0, w1, 0x5410);
                x[t][h + 2] = __byte_perm(w0, w1, 0x7632);
            }
    }
}

// table: per gate, per lane, SPLIT uint4 (re b0, re b1, im b0, im b1), leading part first.
template <int TILES, int GATES, int SPLIT, int SWITCH>
__device__ void chain(u32* __restrict__ state, const uint4* __restrict__ table, long long n_tiles) {
    const int lane = threadIdx.x & 31, g = lane >> 2, c = lane & 3;
    const long long warp = (blockIdx.x * (long long)blockDim.x + threadIdx.x) >> 5;
    const long long warps = (gridDim.x * (long long)blockDim.x) >> 5;
    __shared__ u32 shared[8][TILES * 128];
    u32* buffer = shared[threadIdx.x >> 5];
    for (long long first = warp * TILES; first < n_tiles; first += warps * TILES) {
        u32 a[TILES][4], lo[TILES][4];
#pragma unroll
        for (int t = 0; t < TILES; ++t) {
#pragma unroll
            for (int j = 0; j < 4; ++j) lo[t][j] = 0u;
            const u32* tile = state + (first + t) * 128;
            uint2 lo = *reinterpret_cast<const uint2*>(tile + 8 * g + 2 * c);
            uint2 hi = *reinterpret_cast<const uint2*>(tile + 8 * (g + 8) + 2 * c);
            a[t][0] = __byte_perm(lo.x, lo.y, 0x5410);
            a[t][2] = __byte_perm(lo.x, lo.y, 0x7632);
            a[t][1] = __byte_perm(hi.x, hi.y, 0x5410);
            a[t][3] = __byte_perm(hi.x, hi.y, 0x7632);
        }
#pragma unroll
        for (int k = 0; k < GATES; ++k) {
            if (SWITCH == 1 && k > 0) {
#pragma unroll
                for (int t = 0; t < TILES; ++t)
#pragma unroll
                    for (int j = 0; j < 4; ++j) {
                        a[t][j] = trans(a[t][j]);
                        if (SPLIT == 3) lo[t][j] = trans(lo[t][j]);
                    }
            }
            if (SWITCH == 2 && k > 0) relayout<TILES, SPLIT>(a, lo, buffer);
            constexpr int PARTS = SPLIT == 3 ? 2 : SPLIT;  // matrix parts in the table
            uint4 m[PARTS];
#pragma unroll
            for (int s = 0; s < PARTS; ++s) m[s] = __ldg(table + ((k * 32 + lane) * PARTS + s));
#pragma unroll
            for (int t = 0; t < TILES; ++t) {
                float re[4] = {0.f, 0.f, 0.f, 0.f}, im[4] = {0.f, 0.f, 0.f, 0.f};
                if (SPLIT == 3) {
                    // Ootomo and Yokota: lead x rest and rest x lead, then lead x lead.
                    mma(re, lo[t], m[0].x, m[0].y);
                    mma(im, lo[t], m[0].z, m[0].w);
                    mma(re, a[t], m[1].x, m[1].y);
                    mma(im, a[t], m[1].z, m[1].w);
                    mma(re, a[t], m[0].x, m[0].y);
                    mma(im, a[t], m[0].z, m[0].w);
                } else {
#pragma unroll
                    for (int s = PARTS - 1; s >= 0; --s) {
                        mma(re, a[t], m[s].x, m[s].y);
                        mma(im, a[t], m[s].z, m[s].w);
                    }
                }
                a[t][0] = pack(re[0], re[1]);
                a[t][1] = pack(re[2], re[3]);
                a[t][2] = pack(im[0], im[1]);
                a[t][3] = pack(im[2], im[3]);
                if (SPLIT == 3) {
                    lo[t][0] = rest(re[0], re[1], a[t][0]);
                    lo[t][1] = rest(re[2], re[3], a[t][1]);
                    lo[t][2] = rest(im[0], im[1], a[t][2]);
                    lo[t][3] = rest(im[2], im[3], a[t][3]);
                }
            }
        }
        if (SWITCH == 1 && (GATES - 1) % 2) {
#pragma unroll
            for (int t = 0; t < TILES; ++t)
#pragma unroll
                for (int j = 0; j < 4; ++j) a[t][j] = trans(a[t][j]);
        }
        if (SWITCH == 2 && (GATES - 1) % 2) relayout<TILES, 1>(a, lo, buffer);
#pragma unroll
        for (int t = 0; t < TILES; ++t) {
            u32* tile = state + (first + t) * 128;
            *reinterpret_cast<uint2*>(tile + 8 * g + 2 * c) =
                make_uint2(__byte_perm(a[t][0], a[t][2], 0x5410), __byte_perm(a[t][0], a[t][2], 0x7632));
            *reinterpret_cast<uint2*>(tile + 8 * (g + 8) + 2 * c) =
                make_uint2(__byte_perm(a[t][1], a[t][3], 0x5410), __byte_perm(a[t][1], a[t][3], 0x7632));
        }
    }
}

__constant__ float2 gate_c[64][64];  // per gate, U[row][col] row-major, complex

// CUDA cores: a thread holds the 8 amplitudes of one group of qubits 0..2; a warp 256 amplitudes.
template <int GATES, int SWITCH>
__device__ void chain_cuda(u32* __restrict__ state, long long n_tiles) {
    __shared__ float2 buffer[8][256 + 32];
    const int lane = threadIdx.x & 31, w = threadIdx.x >> 5;
    const long long warp = (blockIdx.x * (long long)blockDim.x + threadIdx.x) >> 5;
    const long long warps = (gridDim.x * (long long)blockDim.x) >> 5;
    for (long long tile = warp; tile < n_tiles; tile += warps) {
        u32* base = state + tile * 256 + 8 * lane;
        float2 x[8];
        uint4 p = *reinterpret_cast<const uint4*>(base), q = *reinterpret_cast<const uint4*>(base + 4);
        u32 words[8] = {p.x, p.y, p.z, p.w, q.x, q.y, q.z, q.w};
#pragma unroll
        for (int j = 0; j < 8; ++j) x[j] = __half22float2(*reinterpret_cast<__half2*>(&words[j]));
        bool transposed = false;
#pragma unroll
        for (int k = 0; k < GATES; ++k) {
            if (SWITCH && k > 0) {
                // Swap the register index (qubits 0..2 or 3..5) with lane bits 0..2.
                __syncwarp();
#pragma unroll
                for (int j = 0; j < 8; ++j) {
                    int i = transposed ? ((lane >> 3) * 64 + 8 * j + (lane & 7)) : (8 * lane + j);
                    buffer[w][i + (i >> 3)] = x[j];
                }
                __syncwarp();
#pragma unroll
                for (int j = 0; j < 8; ++j) {
                    int i = transposed ? (8 * lane + j) : ((lane >> 3) * 64 + 8 * j + (lane & 7));
                    x[j] = buffer[w][i + (i >> 3)];
                }
                transposed = !transposed;
            }
            float2 y[8];
#pragma unroll
            for (int r = 0; r < 8; ++r) {
                float re = 0.f, im = 0.f;
#pragma unroll
                for (int s = 0; s < 8; ++s) {
                    const float2 u = gate_c[k][8 * r + s];
                    re = fmaf(u.x, x[s].x, fmaf(-u.y, x[s].y, re));
                    im = fmaf(u.x, x[s].y, fmaf(u.y, x[s].x, im));
                }
                y[r] = make_float2(re, im);
            }
#pragma unroll
            for (int r = 0; r < 8; ++r) x[r] = y[r];
        }
        if (transposed) {
            __syncwarp();
#pragma unroll
            for (int j = 0; j < 8; ++j) {
                int i = (lane >> 3) * 64 + 8 * j + (lane & 7);
                buffer[w][i + (i >> 3)] = x[j];
            }
            __syncwarp();
#pragma unroll
            for (int j = 0; j < 8; ++j) {
                int i = 8 * lane + j;
                x[j] = buffer[w][i + (i >> 3)];
            }
        }
#pragma unroll
        for (int j = 0; j < 8; ++j) {
            __half2 h = __float22half2_rn(x[j]);
            words[j] = *reinterpret_cast<u32*>(&h);
        }
        *reinterpret_cast<uint4*>(base) = make_uint4(words[0], words[1], words[2], words[3]);
        *reinterpret_cast<uint4*>(base + 4) = make_uint4(words[4], words[5], words[6], words[7]);
    }
}

// CUDA cores, structured stages: like chain_cuda, but each stage applies ROT real two-term
// rotations (noisecirc's rotation form, 2 FMA per amplitude each) on the register qubits in turn,
// 2 * ROT floating-point instructions per amplitude, as noisecirc's contracted stages cost 3 to 25.
template <int ROT, int GATES, int SWITCH>
__device__ void chain_structured(u32* __restrict__ state, long long n_tiles) {
    __shared__ float2 buffer[8][256 + 32];
    const int lane = threadIdx.x & 31, w = threadIdx.x >> 5;
    const long long warp = (blockIdx.x * (long long)blockDim.x + threadIdx.x) >> 5;
    const long long warps = (gridDim.x * (long long)blockDim.x) >> 5;
    for (long long tile = warp; tile < n_tiles; tile += warps) {
        u32* base = state + tile * 256 + 8 * lane;
        float2 x[8];
        uint4 p = *reinterpret_cast<const uint4*>(base), q = *reinterpret_cast<const uint4*>(base + 4);
        u32 words[8] = {p.x, p.y, p.z, p.w, q.x, q.y, q.z, q.w};
#pragma unroll
        for (int j = 0; j < 8; ++j) x[j] = __half22float2(*reinterpret_cast<__half2*>(&words[j]));
        bool transposed = false;
#pragma unroll
        for (int k = 0; k < GATES; ++k) {
            if (SWITCH && k > 0) {
                __syncwarp();
#pragma unroll
                for (int j = 0; j < 8; ++j) {
                    int i = transposed ? ((lane >> 3) * 64 + 8 * j + (lane & 7)) : (8 * lane + j);
                    buffer[w][i + (i >> 3)] = x[j];
                }
                __syncwarp();
#pragma unroll
                for (int j = 0; j < 8; ++j) {
                    int i = transposed ? (8 * lane + j) : ((lane >> 3) * 64 + 8 * j + (lane & 7));
                    x[j] = buffer[w][i + (i >> 3)];
                }
                transposed = !transposed;
            }
#pragma unroll
            for (int g = 0; g < ROT; ++g) {
                const int bit = 1 << (g % 3);
                const float t = gate_c[k][g].x;
#pragma unroll
                for (int c0 = 0; c0 < 8; ++c0) {
                    if (c0 & bit) continue;
                    const float2 v0 = x[c0], v1 = x[c0 | bit];
                    x[c0] = make_float2(fmaf(-t, v1.x, v0.x), fmaf(-t, v1.y, v0.y));
                    x[c0 | bit] = make_float2(fmaf(t, v0.x, v1.x), fmaf(t, v0.y, v1.y));
                }
            }
        }
        if (transposed) {
            __syncwarp();
#pragma unroll
            for (int j = 0; j < 8; ++j) {
                int i = (lane >> 3) * 64 + 8 * j + (lane & 7);
                buffer[w][i + (i >> 3)] = x[j];
            }
            __syncwarp();
#pragma unroll
            for (int j = 0; j < 8; ++j) {
                int i = 8 * lane + j;
                x[j] = buffer[w][i + (i >> 3)];
            }
        }
#pragma unroll
        for (int j = 0; j < 8; ++j) {
            __half2 h = __float22half2_rn(x[j]);
            words[j] = *reinterpret_cast<u32*>(&h);
        }
        *reinterpret_cast<uint4*>(base) = make_uint4(words[0], words[1], words[2], words[3]);
        *reinterpret_cast<uint4*>(base + 4) = make_uint4(words[4], words[5], words[6], words[7]);
    }
}

extern "C" __global__ void copy(const uint4* __restrict__ src, uint4* __restrict__ dst, long long n) {
    for (long long i = blockIdx.x * (long long)blockDim.x + threadIdx.x; i < n; i += gridDim.x * (long long)blockDim.x)
        dst[i] = src[i];
}
"""

TC_GATES = (1, 4, 8, 16, 32)
CUDA_GATES = (1, 4, 8)
STRUCTURED_ROTATIONS = (2, 4, 8)


def kernel_names() -> list[str]:
    names = []
    for split in (1, 2, 3):
        for tiles in (2, 4):
            for gates in TC_GATES:
                for switch in (0, 1, 2):
                    names.append(f"tc_{tiles}_{gates}_{split}_{switch}")
    for gates in CUDA_GATES:
        for switch in (0, 1):
            names.append(f"cuda_{gates}_{switch}")
    for rot in STRUCTURED_ROTATIONS:
        for gates in TC_GATES:
            for switch in (0, 1):
                names.append(f"cudas_{rot}_{gates}_{switch}")
    return names


def instantiations() -> str:
    lines = []
    for name in kernel_names():
        parts = name.split("_")
        if parts[0] == "tc":
            tiles, gates, split, switch = parts[1:]
            lines.append(f'extern "C" __global__ void __launch_bounds__(256) {name}(u32* s, const uint4* t, long long n) '
                         f'{{ chain<{tiles}, {gates}, {split}, {switch}>(s, t, n); }}')
        elif parts[0] == "cuda":
            gates, switch = parts[1:]
            lines.append(f'extern "C" __global__ void __launch_bounds__(256) {name}(u32* s, const uint4* t, long long n) '
                         f'{{ chain_cuda<{gates}, {switch}>(s, n); }}')
        else:
            rot, gates, switch = parts[1:]
            lines.append(f'extern "C" __global__ void __launch_bounds__(256) {name}(u32* s, const uint4* t, long long n) '
                         f'{{ chain_structured<{rot}, {gates}, {switch}>(s, n); }}')
    return "\n".join(lines)


def random_unitary(rng: np.random.Generator, d: int) -> np.ndarray:
    z = (rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))) / np.sqrt(2)
    q, r = np.linalg.qr(z)
    return q * (np.diag(r) / np.abs(np.diag(r)))


def table(gates: list[np.ndarray], split: int) -> np.ndarray:
    """Per gate, lane and split part: the B fragments (as uint32 pairs of FP16) of the real and imaginary output columns."""
    out = np.zeros((len(gates), 32, split, 4), dtype=np.uint32)
    for k, u in enumerate(gates):
        a, b = u.real.T, u.imag.T  # right product with U^T
        m_re = np.vstack([a, -b])  # K = 16 (Re x, Im x) x N = 8 (Re y)
        m_im = np.vstack([b, a])
        parts = []
        rest_re, rest_im = m_re, m_im
        for _ in range(split):
            lead_re, lead_im = rest_re.astype(np.float16), rest_im.astype(np.float16)
            parts.append((lead_re, lead_im))
            rest_re, rest_im = rest_re - lead_re.astype(np.float64), rest_im - lead_im.astype(np.float64)
        for lane in range(32):
            g, c = lane >> 2, lane & 3
            for s, (pr, pi) in enumerate(parts):
                words = []
                for m in (pr, pi):
                    for k0 in (2 * c, 2 * c + 8):
                        pair = np.array([m[k0, g], m[k0 + 1, g]], dtype=np.float16)
                        words.append(int(pair.view(np.uint32)[0]))
                out[k, lane, s] = words
    return out


def reference(state: np.ndarray, gates: list[np.ndarray], switch: int) -> np.ndarray:
    psi = state.astype(np.complex128).reshape(-1, 2, 2, 2, 2, 2, 2, 2)  # axes: rest, q6..q0
    for k, u in enumerate(gates):
        q = 0 if not switch or k % 2 == 0 else 3
        axes = [7 - q - 2, 7 - q - 1, 7 - q]  # q+2, q+1, q (most significant first)
        moved = np.moveaxis(psi, axes, [-3, -2, -1])
        shape = moved.shape
        moved = (moved.reshape(-1, 8) @ u.T).reshape(shape)
        psi = np.moveaxis(moved, [-3, -2, -1], axes)
    return psi.reshape(-1)


def to_c32(state: np.ndarray) -> cp.ndarray:
    pairs = np.stack([state.real, state.imag], -1).astype(np.float16)
    return cp.asarray(pairs.view(np.uint32).reshape(-1))


def from_c32(words: cp.ndarray) -> np.ndarray:
    pairs = cp.asnumpy(words).view(np.float16).reshape(-1, 2).astype(np.float64)
    return pairs[:, 0] + 1j * pairs[:, 1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--qubits", type=int, default=28)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    module = cp.RawModule(code=SOURCE + instantiations(), options=("-std=c++17", "-arch=sm_90"))
    rng = np.random.default_rng(5)
    gates = [random_unitary(rng, 8) for _ in range(64)]
    # cudas reads its rotations' tangents from the real parts of gate_c[k][0..7]; its amplitudes may
    # overflow over many stages, which does not change the time of FP32 arithmetic.
    gate_c = module.get_global("gate_c")
    flat = np.zeros((64, 64, 2), dtype=np.float32)
    for k, u in enumerate(gates):
        flat[k, :, 0], flat[k, :, 1] = u.real.reshape(-1), u.imag.reshape(-1)
    cp.cuda.runtime.memcpy(gate_c.ptr, flat.ctypes.data, flat.nbytes, cp.cuda.runtime.memcpyHostToDevice)
    tables = {split: cp.asarray(table(gates, min(split, 2)).reshape(-1)) for split in (1, 2, 3)}
    sms = cp.cuda.runtime.getDeviceProperties(0)["multiProcessorCount"]

    def launch(name: str, state: cp.ndarray, n: int) -> None:
        kind = name.split("_")[0]
        split = int(name.split("_")[3]) if kind == "tc" else 1
        per_warp = 128 * int(name.split("_")[1]) if kind == "tc" else 256
        n_tiles = (1 << n) // (128 if kind == "tc" else 256)
        # One iteration per warp: every warp of the grid handles its tiles once.
        blocks = max(1, (1 << n) // per_warp // 8)
        module.get_function(name)((blocks,), (256,), (state, tables[split], cp.int64(n_tiles)))

    if args.check:
        n = 12
        psi = rng.normal(size=1 << n) + 1j * rng.normal(size=1 << n)
        psi /= np.linalg.norm(psi)
        psi *= np.sqrt(1 << n)  # amplitudes near 1, as svpass's complex32 storage scale
        for name in kernel_names():
            parts = name.split("_")
            if parts[0] == "cudas":
                continue  # random rotations, no reference
            count, switch = (int(parts[2]), int(parts[4])) if parts[0] == "tc" else (int(parts[1]), int(parts[2]))
            state = to_c32(psi)
            launch(name, state, n)
            out = from_c32(state)
            ref = reference(from_c32(to_c32(psi)), gates[:count], switch)
            err = np.linalg.norm(out - ref) / np.linalg.norm(ref)
            print(json.dumps({"kind": "check", "kernel": name, "rel_err": float(err)}), flush=True)
        return

    n = args.qubits
    words = cp.zeros(1 << n, dtype=cp.uint32)
    words[:] = to_c32(np.ones(1, dtype=complex))[0]
    other = cp.empty_like(words)
    copy = module.get_function("copy")
    start, stop = cp.cuda.Event(), cp.cuda.Event()

    def timed(fn, reps: int = 5) -> float:
        fn()
        times = []
        for _ in range(reps):
            start.record()
            fn()
            stop.record()
            stop.synchronize()
            times.append(cp.cuda.get_elapsed_time(start, stop) / 1e3)
        return float(np.median(times))

    n_vec = (1 << n) // 4
    t_bw = timed(lambda: copy((sms * 8,), (256,), (words, other, cp.int64(n_vec))))
    print(json.dumps({"kind": "copy", "n": n, "t_bw": t_bw, "GB_per_s": 2 * 4 * (1 << n) / t_bw / 1e9}), flush=True)
    for name in kernel_names():
        # Re-normalise between kernels: products of random unitaries keep the norm, rounding drifts it.
        words[:] = to_c32(np.ones(1, dtype=complex))[0]
        t = timed(lambda name=name: launch(name, words, n))
        parts = name.split("_")
        if parts[0] == "tc":
            tiles, count, split, switch = map(int, parts[1:])
            flops = 2 * split * 2 * 16 * 8 * 16 * count * ((1 << n) // 128)  # products issued
            row = {"kernel": "tc", "tiles": tiles, "gates": count, "split": split, "switch": switch,
                   "tensor_tflops": flops / t / 1e12}
        elif parts[0] == "cuda":
            count, switch = map(int, parts[1:])
            row = {"kernel": "cuda", "gates": count, "switch": switch,
                   "fma_tflops": 2 * 32 * count * (1 << n) / t / 1e12}
        else:
            rot, count, switch = map(int, parts[1:])
            row = {"kernel": "cuda_structured", "fp_per_amp": 2 * rot, "gates": count, "switch": switch}
        print(json.dumps({"kind": "run", "n": n, "time": t, "t_over_tbw": t / t_bw, **row}), flush=True)


if __name__ == "__main__":
    main()
