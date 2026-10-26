For an NVIDIA H100, my recommendation is to use a fused, register-only three-shear kernel if minimizing FLOPs is your primary objective, but benchmark it against a direct \(SU(2)\) kernel for actual speed.

The reason is that the H100 is extremely fast at floating-point arithmetic, and a single-qubit gate on a large state vector is usually limited by memory bandwidth rather than FLOPs.
1. H100 arithmetic and memory limits
For an H100 SXM, NVIDIA specifies approximately 67 TFLOP/s FP32 throughput and 3.35 TB/s memory bandwidth. 

NVIDIA




For a complex64 state vector, each amplitude pair requires 32 bytes of memory traffic: 16 bytes read and 16 bytes written.
Algorithm	FLOPs/pair	FP32 arithmetic instructions using FMA	Arithmetic intensity
Direct complex \(2\times2\)	28	16	0.875 FLOP/byte
Three complex shears	24	12	0.750 FLOP/byte
Eight-multiplication quaternion algorithm	27–28	Depends on implementation	~0.84–0.88 FLOP/byte

Here, an FMA counts as two FLOPs but executes as one arithmetic instruction. These are arithmetic counts, excluding coefficient setup, addressing, and memory operations.
H100 SXM FP32 roofline comparison

061218243 shearsDirectH100 compute/bandwidth crossover














Using peak FP32 throughput divided by peak HBM bandwidth, the H100's compute/bandwidth crossover is approximately 20 FLOPs/byte. Both gate kernels are far below it.
Consequently, when the state vector resides in HBM and is large enough to saturate memory bandwidth, removing four FLOPs per amplitude pair may barely change runtime. Both algorithms must transfer essentially the same number of bytes.

What would change performance most is eliminating a complete memory pass, not reducing arithmetic from 28 to 24 FLOPs.
2. A three-shear CUDA kernel optimized for FP32 FMA
For \(U\in SU(2)\), using the factorization from our previous discussion, you can apply each gate with only 12 FP32 FMA instructions per amplitude pair.

This implementation uses one CUDA thread per pair, keeps both amplitudes in registers, and performs one read and one write per amplitude.

#include <cuda_runtime.h>
#include <stdint.h>

// dst += c * src
// Four FP32 FMAs, or eight FLOPs.
__device__ __forceinline__
void complex_axpy(float2& dst, float2 src, float2 c)
{
    float re = fmaf(-c.y, src.y,
               fmaf( c.x, src.x, dst.x));

    float im = fmaf( c.y, src.x,
               fmaf( c.x, src.y, dst.y));

    dst.x = re;
    dst.y = im;
}

__global__
void apply_su2_shears(
    float2* __restrict__ psi,
    uint64_t num_pairs,
    int target,
    float2 p, float2 q, float2 r)
{
    uint64_t k =
        uint64_t(blockIdx.x) * blockDim.x
        + threadIdx.x;

    if (k >= num_pairs) return;

    // Insert a zero bit at the target position.
    uint64_t mask = (1ULL << target) - 1;
    uint64_t i0 = ((k & ~mask) << 1)
                | (k & mask);
    uint64_t i1 = i0 | (1ULL << target);

    float2 x0 = psi[i0];
    float2 x1 = psi[i1];

    // Apply U = Upper(p) Lower(q) Upper(r).
    complex_axpy(x0, x1, r);
    complex_axpy(x1, x0, q);
    complex_axpy(x0, x1, p);

    psi[i0] = x0;
    psi[i1] = x1;
}



Precompute on the CPU or once per gate:
\[
p=\frac{a-1}{c},\quad q=c,\quad r=\frac{d-1}{c}.
\]

The kernel assumes \(\det U=1\) and \(c\neq0\). Use a different path when the coefficients are poorly conditioned.

This implementation has several useful H100 properties:
- 12 FP32 FMAs per amplitude pair, subject to compiler code generation.
- No shared memory, atomics, or inter-thread synchronization.
- No temporary state-vector allocation.
- Each amplitude loaded and stored once.
- Coalesced access is achievable for both low- and high-index qubits, with a specially vectorized path worth considering for target qubit zero.
The main disadvantage is the serial dependence between the three shears. A direct matrix multiplication has more independent arithmetic, which can help GPU scheduling.
3. Why I would not use a diagonal/Hadamard decomposition
The eight-real-multiplication quaternion approach is mathematically attractive, but on an H100 it trades multiplications for additions.

An H100 can execute an FP32 FMA as one arithmetic instruction, performing both a multiplication and an addition. Therefore, the shear kernel's 12 FMAs can be more efficient than a decomposition with eight multiplies and approximately nineteen additions.

Moreover, the Hadamard-like stages introduce intermediate sums and additional data dependencies.

For an individual state-vector gate, I would expect a straightforward FMA-based shear implementation to be a stronger candidate than a fast quaternion multiplication circuit. This is an architectural prediction, not a measured performance result.

Similarly, H100 Tensor Cores are designed for larger matrix-multiply-accumulate tiles. Applying independent \(2\times2\) gates does not naturally exploit their throughput, and converting the work into tensor-core tiles typically creates more overhead than it saves.
4. The biggest optimization: fuse gates
If you are applying a sequence of single-qubit gates, reducing global-memory traffic will have a much larger impact than optimizing individual matrix multiplications.

For example, suppose you apply five gates consecutively to the same qubit:
\[
U_{\mathrm{total}}=U_5U_4U_3U_2U_1.
\]

You can multiply the five \(2\times2\) matrices first and apply the result once.

For a complex64 state vector containing \(2^{30}\) amplitudes:
Theoretical H100 SXM memory-traffic comparison
Five separate gate passes
85.9 GB

One fused gate pass
17.2 GB



Ideal bandwidth-only lower bounds at 3.35 TB/s
Five passes
25.6 ms



One fused pass
5.1 ms



Illustrative bandwidth lower bounds, not measured kernel runtimes. Assumes all accesses reach HBM and ignores launch overhead.
For gates on different qubits, tile several amplitudes into registers or shared memory and apply multiple gates before writing them back. NVIDIA's cuStateVec also supports gate fusion specifically to reduce memory traffic. 

NVIDIA cuQuantum



5. What I would actually benchmark
Situation	First algorithm to try
Large vector, generic \(SU(2)\)	Direct FMA kernel vs. three shears
Small or cache-resident vector	Three shears, checking instruction dependencies
Diagonal or permutation gates	Dedicated specialized kernel
Numerically problematic shear coefficients	Direct matrix multiplication
Many consecutive gates	Gate fusion
Arbitrary \(U(2)\), exact global phase required	Direct kernel, or track the global phase separately
Many small state vectors	Batched application

For large vectors, use Nsight Compute to determine whether the bottleneck is HBM bandwidth, instruction throughput, or latency. For short-running kernels, compare CUDA Graph replay timings to avoid confusing launch overhead with kernel execution time.
Final recommendation
For the H100, the three-shear algorithm is a good choice for minimizing scalar arithmetic: 12 FP32 FMAs rather than 16 arithmetic instructions for a conventional direct multiply.

But for minimizing execution time, I would prioritize coalesced memory access, register-resident amplitude pairs, and fusion of consecutive gates. A well-optimized direct kernel may match or outperform the shear kernel despite performing more FLOPs.

One detail would materially change the recommendation: are you applying a single arbitrary unitary once to a large state vector, or are you building a simulator that applies thousands of successive gates? In the latter case, the best optimization strategy is quite different.