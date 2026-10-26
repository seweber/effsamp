"""A19: time of a single-qubit gate in the forms of PLAN_ADDITIONAL_NOTES_2.md and noisecirc's rotation form, on GPU 0.

Four forms of applying a 2x2 gate to a pair of complex64 amplitudes:

- ``direct``: the complex matrix, 16 FP32 instructions (FMA) per pair;
- ``shear``: three complex shears ``Upper(p) Lower(q) Upper(r)`` of the gate scaled to determinant 1
  (the notes' kernel), 12 per pair;
- ``rotation``: noisecirc's rotation form, a real two-term rotation ``[[1, -t], [t, 1]]`` with the
  gate's diagonal factors deferred, 4 per pair;
- ``ratio``: the rotation form where the pending diagonal is not symmetric on the pair, so that a
  complex ratio multiplies one amplitude first, 8 per pair.

Two settings: ``hbm`` applies one gate per pass over a state of n qubits (target qubit 12), so that
the pass is bound by memory bandwidth; ``chain`` lets each thread load 8 amplitudes (3 qubits) once
and apply 3 to 48 gates to them in registers, cycling over the 3 qubits (unrolled, the gates'
constants operands of the instructions), so that it is bound by instruction issue. Prints the time over the copy-kernel time t_bw and, for ``chain``, the time per
gate and amplitude and the FP32 instruction rate. `--check` compares every form with NumPy.

Usage: a19_gate_forms.py [--qubits 28] [--check]
"""

import argparse
import json

import cupy as cp
import numpy as np

SOURCE = r"""
// Per gate: direct (a, b, c, d), shear (p, q, r), rotation t, ratio z; complex values as float2.
struct Gate { float2 a, b, c, d, p, q, r, z; float t; float pad[3]; };
__constant__ Gate gates[64];

__device__ __forceinline__ float2 cmul_add(float2 acc, float2 u, float2 v) {  // acc + u v
    return make_float2(fmaf(u.x, v.x, fmaf(-u.y, v.y, acc.x)), fmaf(u.x, v.y, fmaf(u.y, v.x, acc.y)));
}
__device__ __forceinline__ float2 cmul(float2 u, float2 v) {
    return make_float2(fmaf(u.x, v.x, -u.y * v.y), fmaf(u.x, v.y, u.y * v.x));
}

template <int FORM>
__device__ __forceinline__ void apply(float2& x0, float2& x1, const Gate& g) {
    if (FORM == 0) {  // direct
        const float2 y0 = cmul_add(cmul(g.a, x0), g.b, x1);
        const float2 y1 = cmul_add(cmul(g.c, x0), g.d, x1);
        x0 = y0; x1 = y1;
    } else if (FORM == 1) {  // shears
        x0 = cmul_add(x0, g.r, x1);
        x1 = cmul_add(x1, g.q, x0);
        x0 = cmul_add(x0, g.p, x1);
    } else if (FORM == 2) {  // real rotation
        const float2 v0 = x0, v1 = x1;
        x0 = make_float2(fmaf(-g.t, v1.x, v0.x), fmaf(-g.t, v1.y, v0.y));
        x1 = make_float2(fmaf(g.t, v0.x, v1.x), fmaf(g.t, v0.y, v1.y));
    } else {  // ratio, then real rotation
        x1 = cmul(g.z, x1);
        const float2 v0 = x0, v1 = x1;
        x0 = make_float2(fmaf(-g.t, v1.x, v0.x), fmaf(-g.t, v1.y, v0.y));
        x1 = make_float2(fmaf(g.t, v0.x, v1.x), fmaf(g.t, v0.y, v1.y));
    }
}

// One gate on qubit TARGET per pass.
template <int FORM>
__device__ void hbm(float2* __restrict__ psi, long long pairs, int target) {
    const Gate g = gates[0];
    for (long long k = blockIdx.x * (long long)blockDim.x + threadIdx.x; k < pairs; k += gridDim.x * (long long)blockDim.x) {
        const long long mask = (1ll << target) - 1;
        const long long i0 = ((k & ~mask) << 1) | (k & mask), i1 = i0 | (1ll << target);
        float2 x0 = psi[i0], x1 = psi[i1];
        apply<FORM>(x0, x1, g);
        psi[i0] = x0; psi[i1] = x1;
    }
}

// Each thread: 8 consecutive amplitudes (qubits 0..2), 3 * ROUNDS gates cycling over the 3 qubits.
// The loops are unrolled, so that the gates' constants are operands of the FMAs.
template <int FORM, int ROUNDS>
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
        for (int round = 0; round < ROUNDS; ++round) {
#pragma unroll
            for (int bit = 0; bit < 3; ++bit) {
                const Gate g = gates[(3 * round + bit) & 63];
#pragma unroll
                for (int c0 = 0; c0 < 8; ++c0)
                    if (!(c0 & (1 << bit))) apply<FORM>(x[c0], x[c0 | (1 << bit)], g);
            }
        }
#pragma unroll
        for (int j = 0; j < 4; ++j) base[j] = make_float4(x[2 * j].x, x[2 * j].y, x[2 * j + 1].x, x[2 * j + 1].y);
    }
}

#define K(form, id) \
    extern "C" __global__ void hbm_##form(float2* psi, long long pairs, int target) { hbm<id>(psi, pairs, target); } \
    extern "C" __global__ void chain_##form##_1(float2* psi, long long groups) { chain<id, 1>(psi, groups); } \
    extern "C" __global__ void chain_##form##_2(float2* psi, long long groups) { chain<id, 2>(psi, groups); } \
    extern "C" __global__ void chain_##form##_4(float2* psi, long long groups) { chain<id, 4>(psi, groups); } \
    extern "C" __global__ void chain_##form##_8(float2* psi, long long groups) { chain<id, 8>(psi, groups); } \
    extern "C" __global__ void chain_##form##_16(float2* psi, long long groups) { chain<id, 16>(psi, groups); }
K(direct, 0) K(shear, 1) K(rotation, 2) K(ratio, 3)

extern "C" __global__ void copy(const float4* __restrict__ src, float4* __restrict__ dst, long long n) {
    for (long long i = blockIdx.x * (long long)blockDim.x + threadIdx.x; i < n; i += gridDim.x * (long long)blockDim.x)
        dst[i] = src[i];
}
"""

FORMS = {"direct": 16, "shear": 12, "rotation": 4, "ratio": 8}  # FP32 instructions per pair


def gate_table(rng: np.random.Generator) -> tuple[np.ndarray, list[dict]]:
    """Random gates in every form; returns the packed constant table and, per gate, the matrices each form applies."""
    dtype = np.dtype([("a", "<c8"), ("b", "<c8"), ("c", "<c8"), ("d", "<c8"), ("p", "<c8"), ("q", "<c8"),
                      ("r", "<c8"), ("z", "<c8"), ("t", "<f4"), ("pad", "<f4", 3)])
    table = np.zeros(64, dtype=dtype)
    matrices = []
    for k in range(64):
        z = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
        q, r = np.linalg.qr(z)
        u = q / np.sqrt(np.linalg.det(q))  # SU(2)
        (a, b), (c, d) = u
        t = float(rng.uniform(-1, 1))
        ratio = np.exp(1j * rng.uniform(0, 2 * np.pi))
        table[k] = (a, b, c, d, (a - 1) / c, c, (d - 1) / c, ratio, t, (0, 0, 0))
        rotation = np.array([[1, -t], [t, 1]])
        matrices.append({"direct": u, "shear": u, "rotation": rotation, "ratio": rotation @ np.diag([1, ratio])})
    return table, matrices


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--qubits", type=int, default=28)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    module = cp.RawModule(code=SOURCE, options=("-std=c++17", "-arch=sm_90"))
    rng = np.random.default_rng(11)
    table, matrices = gate_table(rng)
    symbol = module.get_global("gates")
    cp.cuda.runtime.memcpy(symbol.ptr, table.ctypes.data, table.nbytes, cp.cuda.runtime.memcpyHostToDevice)
    sms = cp.cuda.runtime.getDeviceProperties(0)["multiProcessorCount"]
    grid = sms * 8

    if args.check:
        n = 14
        psi = (rng.normal(size=1 << n) + 1j * rng.normal(size=1 << n)).astype(np.complex64)
        for form in FORMS:
            state = cp.asarray(psi)
            module.get_function(f"hbm_{form}")((grid,), (256,), (state, cp.int64(1 << (n - 1)), cp.int32(12)))
            ref = psi.astype(np.complex128).reshape(-1, 2, 1 << 12)
            ref = np.einsum("ij,ajb->aib", matrices[0][form], ref).reshape(-1)
            err = np.linalg.norm(cp.asnumpy(state) - ref) / np.linalg.norm(ref)
            state = cp.asarray(psi)
            rounds = 2
            module.get_function(f"chain_{form}_{rounds}")((grid,), (256,), (state, cp.int64(1 << (n - 3))))
            chained = psi.astype(np.complex128).reshape(-1, 2, 2, 2)  # axes: rest, q2, q1, q0
            for g in range(3 * rounds):
                axis = 3 - g % 3
                chained = np.moveaxis(np.tensordot(matrices[g][form], chained, axes=([1], [axis])), 0, axis)
            err_chain = np.linalg.norm(cp.asnumpy(state) - chained.reshape(-1)) / np.linalg.norm(chained)
            print(json.dumps({"kind": "check", "form": form, "hbm_rel_err": float(err), "chain_rel_err": float(err_chain)}))
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
    print(json.dumps({"kind": "copy", "n": n, "t_bw": t_bw, "GB_per_s": 2 * 8 * (1 << n) / t_bw / 1e9}), flush=True)
    for form, instructions in FORMS.items():
        kernel = module.get_function(f"hbm_{form}")
        t = timed(lambda kernel=kernel: kernel((grid,), (256,), (psi, cp.int64(1 << (n - 1)), cp.int32(12))))
        print(json.dumps({"kind": "hbm", "form": form, "t_over_tbw": t / t_bw}), flush=True)
        for rounds in (1, 2, 4, 8, 16):
            kernel = module.get_function(f"chain_{form}_{rounds}")
            psi.fill(1 / np.sqrt(1 << n))
            t = timed(lambda kernel=kernel: kernel((grid,), (256,), (psi, cp.int64(1 << (n - 3)))))
            gates = 3 * rounds
            print(json.dumps({"kind": "chain", "form": form, "gates": gates, "t_over_tbw": t / t_bw,
                              "ps_per_gate_amp": t / gates / (1 << n) * 1e12,
                              "fp32_tinstr_per_s": instructions / 2 * gates * (1 << n) / t / 1e12}), flush=True)


if __name__ == "__main__":
    main()
