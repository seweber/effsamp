"""A16: throughput of the warp-level tensor-core instructions noisecirc's tensor-core stages use, on GPU 0.

Each warp of a grid filling the GPU issues `mma.sync` m16n8k16 (f16 inputs) or m16n8k8 (tf32 inputs)
with f32 accumulation in a loop, on `chains` independent accumulators so that several are in flight;
prints the achieved dense TFLOP/s (2 * M * N * K per instruction) per chain count, and the FP32 FMA
rate of the CUDA cores measured the same way for comparison. The inputs are constants; only the
issue rate and latency of the instructions count.

Usage: a16_mma_rate.py
"""

import json

import cupy as cp

SOURCE = r"""
template <int CHAINS>
__device__ void body_f16(float* out, int iters) {
    float d[CHAINS][4] = {};
    unsigned int a0 = threadIdx.x, a1 = a0 * 3u, a2 = a0 * 5u, a3 = a0 * 7u, b0 = a0 * 11u, b1 = a0 * 13u;
    for (int i = 0; i < iters; ++i) {
#pragma unroll
        for (int c = 0; c < CHAINS; ++c)
            asm volatile("mma.sync.aligned.m16n8k16.row.col.f32.f16.f16.f32 {%0,%1,%2,%3}, {%4,%5,%6,%7}, {%8,%9}, {%0,%1,%2,%3};"
                : "+f"(d[c][0]), "+f"(d[c][1]), "+f"(d[c][2]), "+f"(d[c][3]) : "r"(a0), "r"(a1), "r"(a2), "r"(a3), "r"(b0), "r"(b1));
    }
    float s = 0.0f;
    for (int c = 0; c < CHAINS; ++c) s += d[c][0] + d[c][1] + d[c][2] + d[c][3];
    out[blockIdx.x * blockDim.x + threadIdx.x] = s;
}
template <int CHAINS>
__device__ void body_tf32(float* out, int iters) {
    float d[CHAINS][4] = {};
    unsigned int a0 = threadIdx.x, a1 = a0 * 3u, a2 = a0 * 5u, a3 = a0 * 7u, b0 = a0 * 11u, b1 = a0 * 13u;
    for (int i = 0; i < iters; ++i) {
#pragma unroll
        for (int c = 0; c < CHAINS; ++c)
            asm volatile("mma.sync.aligned.m16n8k8.row.col.f32.tf32.tf32.f32 {%0,%1,%2,%3}, {%4,%5,%6,%7}, {%8,%9}, {%0,%1,%2,%3};"
                : "+f"(d[c][0]), "+f"(d[c][1]), "+f"(d[c][2]), "+f"(d[c][3]) : "r"(a0), "r"(a1), "r"(a2), "r"(a3), "r"(b0), "r"(b1));
    }
    float s = 0.0f;
    for (int c = 0; c < CHAINS; ++c) s += d[c][0] + d[c][1] + d[c][2] + d[c][3];
    out[blockIdx.x * blockDim.x + threadIdx.x] = s;
}
template <int CHAINS>
__device__ void body_ffma(float* out, int iters) {
    float d[CHAINS];
    for (int c = 0; c < CHAINS; ++c) d[c] = threadIdx.x * 1e-3f + c;
    const float a = 0.999f, b = 1e-4f;
    for (int i = 0; i < iters; ++i) {
#pragma unroll
        for (int c = 0; c < CHAINS; ++c) d[c] = fmaf(d[c], a, b);
    }
    float s = 0.0f;
    for (int c = 0; c < CHAINS; ++c) s += d[c];
    out[blockIdx.x * blockDim.x + threadIdx.x] = s;
}
#define K(name, kind, c) extern "C" __global__ void name(float* out, int iters) { body_##kind<c>(out, iters); }
K(f16_1, f16, 1) K(f16_2, f16, 2) K(f16_4, f16, 4) K(f16_8, f16, 8)
K(tf32_1, tf32, 1) K(tf32_2, tf32, 2) K(tf32_4, tf32, 4) K(tf32_8, tf32, 8)
K(ffma_8, ffma, 8)
"""


def main() -> None:
    module = cp.RawModule(code=SOURCE, options=("-std=c++17",))
    sms = cp.cuda.runtime.getDeviceProperties(0)["multiProcessorCount"]
    out = cp.zeros(sms * 8 * 256, dtype=cp.float32)
    flops_per = {"f16": 2 * 16 * 8 * 16, "tf32": 2 * 16 * 8 * 8}
    results = {}
    for name in ["f16_1", "f16_2", "f16_4", "f16_8", "tf32_1", "tf32_2", "tf32_4", "tf32_8", "ffma_8"]:
        kernel = module.get_function(name)
        kind, chains = name.split("_")
        chains = int(chains)
        for threads in (128, 256):
            blocks = sms * 2048 // threads
            iters = 2000
            kernel((blocks,), (threads,), (out, cp.int32(iters)))
            cp.cuda.runtime.deviceSynchronize()
            start, stop = cp.cuda.Event(), cp.cuda.Event()
            start.record()
            kernel((blocks,), (threads,), (out, cp.int32(iters)))
            stop.record()
            stop.synchronize()
            seconds = cp.cuda.get_elapsed_time(start, stop) / 1e3
            if kind == "ffma":
                flops = blocks * threads * iters * chains * 2
            else:
                flops = blocks * threads // 32 * iters * chains * flops_per[kind]
            results[f"{name}_t{threads}"] = flops / seconds / 1e12
    print(json.dumps({"sms": sms, "tflops": results}), flush=True)


if __name__ == "__main__":
    main()
