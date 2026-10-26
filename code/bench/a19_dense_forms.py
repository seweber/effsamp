"""A19: a dense 3-qubit gate with four real products per complex entry (direct) or three (Gauss's trick), on GPU 0.

For a dense complex d x d matrix U = A + iB applied to x + iy, the direct form computes every output's
real part as sum(A x - B y) and its imaginary part as sum(A y + B x): 4d FMAs per amplitude. Gauss's
trick computes T1 = A x, T2 = B y and T3 = (A + B)(x + y), with A + B a constant of the kernel, and
re = T1 - T2, im = T3 - T1 - T2: 3d FMAs, the d sums x + y shared by all rows (one per amplitude), and 3
subtractions per amplitude, 3d + 4 instructions; for d = 8, 28 instead of 32.

Each thread loads 8 consecutive complex64 amplitudes (qubits 0..2) of a state of n qubits, applies
`gates` dense 8x8 gates to them in registers (unrolled, the matrices kernel constants), and stores
them. Prints the pass time over the copy-kernel time and the FP32 instruction rate; `--check`
compares both forms with NumPy.

Usage: a19_dense_forms.py [--qubits 28] [--check]
"""

import argparse
import json

import cupy as cp
import numpy as np

SOURCE = r"""
__constant__ float2 gate_c[16][64];   // U[row][col] per gate
__constant__ float gate_sum[16][64];  // Re U + Im U

template <int THREE, int GATES>
__device__ void chain(float2* __restrict__ psi, long long groups) {
    for (long long k = blockIdx.x * (long long)blockDim.x + threadIdx.x; k < groups; k += gridDim.x * (long long)blockDim.x) {
        float4* base = reinterpret_cast<float4*>(psi + 8 * k);
        float2 x[8];
#pragma unroll
        for (int j = 0; j < 4; ++j) {
            const float4 v = base[j];
            x[2 * j] = make_float2(v.x, v.y);
            x[2 * j + 1] = make_float2(v.z, v.w);
        }
#pragma unroll
        for (int g = 0; g < GATES; ++g) {
            float2 y[8];
            if (THREE) {
                float s[8];
#pragma unroll
                for (int c = 0; c < 8; ++c) s[c] = x[c].x + x[c].y;
#pragma unroll
                for (int r = 0; r < 8; ++r) {
                    float t1 = 0.f, t2 = 0.f, t3 = 0.f;
#pragma unroll
                    for (int c = 0; c < 8; ++c) {
                        t1 = fmaf(gate_c[g][8 * r + c].x, x[c].x, t1);
                        t2 = fmaf(gate_c[g][8 * r + c].y, x[c].y, t2);
                        t3 = fmaf(gate_sum[g][8 * r + c], s[c], t3);
                    }
                    y[r] = make_float2(t1 - t2, t3 - t1 - t2);
                }
            } else {
#pragma unroll
                for (int r = 0; r < 8; ++r) {
                    float re = 0.f, im = 0.f;
#pragma unroll
                    for (int c = 0; c < 8; ++c) {
                        const float2 u = gate_c[g][8 * r + c];
                        re = fmaf(u.x, x[c].x, fmaf(-u.y, x[c].y, re));
                        im = fmaf(u.x, x[c].y, fmaf(u.y, x[c].x, im));
                    }
                    y[r] = make_float2(re, im);
                }
            }
#pragma unroll
            for (int r = 0; r < 8; ++r) x[r] = y[r];
        }
#pragma unroll
        for (int j = 0; j < 4; ++j) base[j] = make_float4(x[2 * j].x, x[2 * j].y, x[2 * j + 1].x, x[2 * j + 1].y);
    }
}

#define K(g) \
    extern "C" __global__ void direct_##g(float2* psi, long long groups) { chain<0, g>(psi, groups); } \
    extern "C" __global__ void gauss_##g(float2* psi, long long groups) { chain<1, g>(psi, groups); }
K(1) K(2) K(4) K(8) K(16)

extern "C" __global__ void copy(const float4* __restrict__ src, float4* __restrict__ dst, long long n) {
    for (long long i = blockIdx.x * (long long)blockDim.x + threadIdx.x; i < n; i += gridDim.x * (long long)blockDim.x)
        dst[i] = src[i];
}
"""

GATES = (1, 2, 4, 8, 16)
INSTRUCTIONS = {"direct": 32, "gauss": 28}  # FP32 instructions per amplitude and gate


def random_unitary(rng: np.random.Generator, d: int) -> np.ndarray:
    z = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
    q, r = np.linalg.qr(z)
    return q * (np.diag(r) / np.abs(np.diag(r)))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--qubits", type=int, default=28)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    module = cp.RawModule(code=SOURCE, options=("-std=c++17", "-arch=sm_90"))
    rng = np.random.default_rng(13)
    gates = [random_unitary(rng, 8) for _ in range(16)]
    matrices = np.stack(gates).astype(np.complex64)
    sums = (matrices.real + matrices.imag).astype(np.float32)
    for name, array in (("gate_c", matrices), ("gate_sum", sums)):
        symbol = module.get_global(name)
        cp.cuda.runtime.memcpy(symbol.ptr, array.ctypes.data, array.nbytes, cp.cuda.runtime.memcpyHostToDevice)
    sms = cp.cuda.runtime.getDeviceProperties(0)["multiProcessorCount"]
    grid = sms * 8

    if args.check:
        n = 12
        psi = (rng.normal(size=1 << n) + 1j * rng.normal(size=1 << n)).astype(np.complex64)
        for form in INSTRUCTIONS:
            for count in (1, 4):
                state = cp.asarray(psi)
                module.get_function(f"{form}_{count}")((grid,), (256,), (state, cp.int64(1 << (n - 3))))
                ref = psi.astype(np.complex128).reshape(-1, 8)
                for u in gates[:count]:
                    ref = ref @ u.T
                err = np.linalg.norm(cp.asnumpy(state) - ref.reshape(-1)) / np.linalg.norm(ref)
                print(json.dumps({"kind": "check", "form": form, "gates": count, "rel_err": float(err)}))
        return

    n = args.qubits
    psi = cp.full(1 << n, 1 / np.sqrt(1 << n), dtype=cp.complex64)
    other = cp.empty_like(psi)
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

    copy = module.get_function("copy")
    t_bw = timed(lambda: copy((grid,), (256,), (psi, other, cp.int64((1 << n) // 2))))
    print(json.dumps({"kind": "copy", "n": n, "t_bw": t_bw}), flush=True)
    for form, instructions in INSTRUCTIONS.items():
        for count in GATES:
            kernel = module.get_function(f"{form}_{count}")
            t = timed(lambda kernel=kernel: kernel((grid,), (256,), (psi, cp.int64(1 << (n - 3)))))
            print(json.dumps({"kind": "chain", "form": form, "gates": count, "t_over_tbw": t / t_bw,
                              "fp32_tinstr_per_s": instructions * count * (1 << n) / t / 1e12}), flush=True)


if __name__ == "__main__":
    main()
