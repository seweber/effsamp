Applying multiple gates at once makes Tensor Cores considerably more attractive on an H100, especially with your precision format: complex32 = two FP16 values (4 bytes per complex amplitude).

However, it depends on what you mean by multiple gates:
- Several gates fused across different qubits: This can make Tensor Cores worthwhile by creating a larger matrix operation.
- Many independent single-qubit gates evaluated in parallel: Batching improves utilization, but a direct CUDA kernel may still be faster.
- Several consecutive gates on the same qubit: Multiply their \(2\times2\) matrices first, then apply the result once. This is generally better than using Tensor Cores for each gate.
My suggested starting point is to benchmark fused unitaries of 8×8, 16×16, and 32×32 complex FP16, corresponding to 3, 4, and 5 qubits. These are candidates, not experimentally established crossover sizes.
1. Minimum useful Tensor Core dimensions
On H100, a particularly useful warp-level FP16 Tensor Core instruction is:
mma.sync.aligned.m16n8k16.row.col.f32.f16.f16.f32


It performs:
\[
D_{16\times8}
=
A_{16\times16}B_{16\times8}+C_{16\times8}
\]

with FP16 operands and FP32 accumulation. 

Apache TVM
+1




A complex matrix multiplication can be implemented using a real-valued representation:
\[
U=U_r+iU_i
\]

\[
\underbrace{
\begin{pmatrix}
U_r&-U_i\\
U_i&U_r
\end{pmatrix}
}_{2d\times2d}
\underbrace{
\begin{pmatrix}
\Psi_r\\
\Psi_i
\end{pmatrix}
}_{2d\times N}
=
\begin{pmatrix}
\Psi'_r\\
\Psi'_i
\end{pmatrix}.
\]

This is an ordinary real matrix multiplication, and it fits Tensor Cores.

The crucial consequence is that a complex \(d\times d\) gate becomes a real \(2d\times2d\) operator.
Fused qubits	Complex gate	Real representation	Fit into FP16 MMA
1	2×2	4×4	Poor
2	4×4	8×8	Poor
3	8×8	16×16	Full M/K tile
4	16×16	32×32	Four M/K tiles
5	32×32	64×64	Sixteen M/K tiles
6	64×64	128×128	Sixty-four M/K tiles

The counts in the last three rows refer to covering the real operator's M and K dimensions with \(16\times16\) tiles, not the total number of MMA instructions.

Three fused qubits are enough to fill the M and K dimensions of the FP16 warp-level MMA. You also need at least 8 independent state-vector columns to fill N, which is normally easy for a large state vector.

That is a hardware-utilization threshold, not a guarantee of speedup.
2. Why multiple gates change the performance calculation
For an H100 SXM, the relevant theoretical hardware figures are approximately:
- Dense FP16 Tensor Core throughput: 989 TFLOP/s
- HBM bandwidth: 3.35 TB/s
- L2 cache: 50 MB


ML Cloud User Guide
+1


A complex32 amplitude occupies 4 bytes. Reading and rewriting every amplitude requires at least 8 bytes per amplitude per pass.

For a dense fused \(d\times d\) complex unitary, the arithmetic intensity, assuming the gate matrix is reused and no intermediate state is materialized, is approximately
\[
I(d)=\frac{8d\text{ FLOPs/amplitude}}{8\text{ bytes/amplitude}}
=\boxed{d\text{ FLOPs/byte}}.
\]

Arithmetic intensity as fused gate size increases

01503004506001 qubit2 qubits3 qubits4 qubits5 qubits6 qubits7 qubits8 qubits9 qubits









The H100 ridge point uses ideal dense FP16 Tensor Core throughput divided by HBM bandwidth. It is not an empirical gate-performance threshold.





The ideal H100 FP16 Tensor Core compute/bandwidth balance is around 295 FLOPs/byte. Dense gates below that are theoretically HBM-bandwidth-bound with perfect Tensor Core utilization.
This tells us something important: Even a 5-qubit fused gate is not inherently compute-intensive enough to saturate the H100 Tensor Cores when streaming a large state vector from HBM.

Tensor Cores become useful because they make the additional arithmetic from gate fusion relatively inexpensive, allowing several gate applications to share one state-vector read/write pass.
3. Example: four single-qubit gates on four distinct qubits
Suppose you apply four gates, each operating on a different qubit.

Without fusion, you execute four state-vector passes:
\[
\psi^{(4)}=U_4 U_3 U_2 U_1\psi.
\]

With fusion, the combined operator is
\[
U_{\mathrm{fused}}=U_4\otimes U_3\otimes U_2\otimes U_1
\]

with dimension \(16\times16\).

You then execute one larger gate:
\[
\psi'=U_{\mathrm{fused}}\psi.
\]

For a 30-qubit state stored in complex32:
Quantity	Four separate gates	One fused gate
Full-state read/write passes	4	1
Minimum HBM traffic	34.4 GB	8.6 GB
Ideal HBM time	10.3 ms	2.56 ms
Complex products per output amplitude	8	16

The times assume full 3.35 TB/s HBM bandwidth and exclude overhead, so they are theoretical lower bounds, not measured runtimes.

The fused operator performs twice as much arithmetic as four separate single-qubit applications, but needs only one-quarter of the state-vector HBM traffic.

This is precisely the scenario where Tensor Cores become attractive.

There is another alternative, though: load 16 amplitudes into registers or shared memory, apply the four small gates there, and write the result once. That also saves HBM passes without forming a dense \(16\times16\) matrix. It is an important competing implementation.
4. What if you batch independent single-qubit gates instead?
This is different from fusion.

Suppose you have hundreds of independent \(2\times2\) complex gates, operating on separate state vectors or independent amplitude groups.

You could pack four realified \(4\times4\) gates into one \(16\times16\) block-diagonal matrix:
\[
A=
\begin{pmatrix}
R(U_0)&0&0&0\\
0&R(U_1)&0&0\\
0&0&R(U_2)&0\\
0&0&0&R(U_3)
\end{pmatrix}
\]

where \(R(U)\) is the real representation of a complex gate.

That fills the Tensor Core instruction dimensions, but 75% of the matrix entries are zero. A dense Tensor Core MMA still performs arithmetic for those zeros.

This can be useful for large batches of small independent vectors if packing is cheap and data is already organized appropriately. It is usually not the best approach for conventional state-vector simulation, where a direct CUDA gate kernel is already highly parallel.
5. What I would benchmark
For complex32 on H100, I would compare these three implementations:
Implementation	1-qubit	3-qubit	4–5-qubit
Direct CUDA gate kernel	Best starting point	Competitive	Baseline
Multiple small gates fused in registers/shared memory	Useful	Very promising	Very promising
FP16 Tensor Core dense gate multiplication	Usually unattractive	Plausible	Strong candidate

For the Tensor Core implementation, I would start with mma.sync and FP32 accumulation, not WGMMA. The smaller tile dimensions are easier to exploit for these relatively small fused matrices.

For a practical baseline, NVIDIA's cuStateVec gate-fusion documentation is useful. NVIDIA's CUDA-Q simulator also uses gate fusion, with a documented default fusion size of 5 qubits on H100 for FP32, although that does not establish a Tensor Core or complex32 optimum. 

NVIDIA cuQuantum
+1




One important benchmarking detail: try a large state vector that exceeds L2 cache capacity, as well as smaller states that fit in cache. The optimal strategy may change substantially.

Bottom line: If you're applying a single \(2\times2\) complex32 gate, I would not expect a Tensor Core implementation to win. If you're applying three or more gates together on distinct qubits, the answer changes: a 3-qubit fused unitary is the first size that naturally fills a realified FP16 MMA tile, and 4–5-qubit fusion is where I'd concentrate optimization effort.

The most informative comparison is not just Tensor Cores versus separate gates, but Tensor Core dense fusion versus register/shared-memory fusion. Both can avoid repeated state-vector memory passes, and the latter avoids the exponential arithmetic overhead of forming a dense fused unitary.
















With three qubits, is one having already max thoughput or is one latency bound?












2m 44s nachgedacht







With 3 fused qubits, you can fill a warp-level FP16 Tensor Core MMA tile, but you are not yet achieving maximum Tensor Core throughput on the H100.

There are three distinct issues: instruction utilization, instruction latency, and memory bandwidth.
1. Three qubits fill one MMA tile
For a fused 3-qubit gate, your complex32 matrix has dimension \(8\times8\). Using the real-valued representation:
\[
U_{\mathrm{real}}\in\mathbb R^{16\times16}
\]

On the H100, you can use:
mma.sync.aligned.m16n8k16.row.col.f32.f16.f16.f32


This performs:
\[
C_{16\times8}=A_{16\times16}B_{16\times8}
\]

One instruction can therefore apply the same three-qubit unitary to 8 independent groups of 8 complex amplitudes, assuming appropriate operand layouts.

That is excellent instruction-level tile utilization:
- \(M=16\): completely utilized.
- \(K=16\): completely utilized.
- \(N=8\): completely utilized if you have eight independent amplitude groups.
But fully utilizing a single instruction is not the same as saturating the Tensor Core pipeline. 

Apache TVM
+1



2. Are you latency-bound?
That depends primarily on how much independent work you launch.
Workload	Likely limitation
One 3-qubit state	Too little parallelism; latency/launch overhead
A few hundred independent 8-amplitude groups	Insufficient GPU occupancy
Thousands of independent groups	Enough potential parallelism to hide MMA latency
Large state vector streamed from HBM	Primarily memory bandwidth

With only one warp executing one MMA, most of the H100 is idle. The instruction's latency dominates its useful work.

With thousands of independent warps, the GPU can overlap instruction execution and hide much of that latency.

However, even this does not imply maximum Tensor Core throughput.
3. There is a second limitation specific to Hopper
The H100 has two important Tensor Core instruction families:
	mma.sync	wgmma.mma_async
Threads	32 (one warp)	128 (four warps)
FP16 tile M	16	64
FP16 tile K	16	16
FP16 tile N	8	8–256
Maximum Hopper Tensor Core throughput	Cannot reach full peak	Can approach peak

A Hopper microbenchmark study measured approximately 63% of peak FP16 throughput using mma.sync, compared with over 95% using appropriately sized WGMMA instructions under favorable conditions. These measurements were on an H800, not an H100, but illustrate an important Hopper architectural limitation. 

arXiv
+1




For your realified complex matrix, the natural minimum sizes are therefore:
Fused qubits	Real matrix	Instruction family
3	16×16	Efficient tile fit for mma.sync
4	32×32	Multiple mma.sync tiles
5	64×64	First size that fills WGMMA's M dimension

Five qubits are thus a better match to Hopper's fastest instruction family. But that does not mean five-qubit fusion is faster overall.
4. A large 3-qubit simulation will probably be memory-bound
For a complex32 state vector, each amplitude occupies 4 bytes.

A dense 3-qubit gate performs approximately 64 real FLOPs per output amplitude, requiring at least 4 bytes read and 4 bytes written.

Its arithmetic intensity is therefore:
\[
I=\frac{64}{8}=\boxed{8\ \text{FLOPs/byte}}
\]

For H100 SXM:
\[
\frac{989\ \text{TFLOP/s}}{3.35\ \text{TB/s}}
\approx295\ \text{FLOPs/byte}
\]

Hence, an ideal three-qubit gate kernel processing a large state directly from HBM needs only:
\[
\frac{8}{295}\approx\boxed{2.7\%}
\]

of the theoretical FP16 Tensor Core peak throughput to saturate HBM bandwidth. 

ML Cloud User Guide
+1




This is an ideal roofline estimate, assuming each amplitude is read and written once, the matrix is reused, and the memory accesses are efficient.

Consequently, increasing the gate dimension to obtain more Tensor Core throughput is not necessarily beneficial.
5. What I would optimize
For your complex32 state-vector simulator:
1. At 3 qubits: Use warp-level MMA, with FP32 accumulation, and distribute many independent amplitude groups across warps.
2. Avoid explicit global-memory reshaping: The cost of rearranging amplitudes may exceed the actual matrix multiplication cost.
3. Compare against register-based fusion: An ordinary CUDA kernel that processes the same eight amplitudes entirely in registers can be highly competitive.
4. At 5 qubits: Benchmark WGMMA, preferably with an N tile of at least 64 columns, while accounting for extra shared-memory preparation and synchronization.
To determine the actual bottleneck, use Nsight Compute and inspect achieved DRAM bandwidth, Tensor Core utilization, active warps, and warp stall reasons. 

NsightCompute
+1




The key distinction: Three qubits can fully utilize the arithmetic within one MMA instruction, but not necessarily the Tensor Core pipeline. For a small state you can indeed be latency- or occupancy-bound; for a sufficiently large state, you are much more likely to be memory-bandwidth-bound.

In fact, for a large complex32 state vector, I would not assume that any dense three-qubit Tensor Core kernel can outperform a carefully optimized, register-fused CUDA kernel. That is the comparison worth measuring first.
















Can I circumvent the memory bound by applying multiple three qubit unitaries within one kernel?












2m 48s nachgedacht







Yes. This is probably the most promising way to make three-qubit Tensor Core operations useful on an H100. You can substantially reduce HBM traffic by applying several \(8\times8\) complex32 unitaries while keeping the relevant state-vector amplitudes in registers or shared memory.

The important requirement is that the intermediate state vectors must remain on-chip. Merely executing several gates in one CUDA kernel does not eliminate memory traffic if each gate still reads and writes global memory.
1. How the arithmetic intensity changes
For a dense three-qubit complex unitary, each output amplitude requires approximately 64 real FLOPs.

With complex32 storage (FP16 real + FP16 imaginary), one read and one write require 8 bytes per amplitude.

A single gate therefore has arithmetic intensity
\[
I_1=\frac{64}{8}=8\text{ FLOPs/byte}.
\]

If you apply \(g\) three-qubit unitaries to amplitudes retained on-chip, the intensity becomes
\[
\boxed{I_g\approx8g\text{ FLOPs/byte}}
\]

provided the intermediate results never reach HBM.
Arithmetic intensity from temporal gate fusion

0 FLOPs/byte90 FLOPs/byte180 FLOPs/byte270 FLOPs/byte360 FLOPs/byte12481624323740









Ideal roofline model; assumes perfect reuse of state amplitudes and negligible intermediate rearrangement costs.





The theoretical H100 SXM FP16 Tensor Core compute/HBM balance is approximately 295 FLOPs/byte, reached at around 37 dense three-qubit gates in this ideal model.
This does not mean you need 37 gates to benefit. Even fusing four or eight applications can significantly improve performance because the same state-vector data is transferred only once.
2. A concrete example: two gates on six qubits
Consider two three-qubit unitaries:
\[
U_A\text{ acts on qubits }0,1,2
\]

\[
U_B\text{ acts on qubits }3,4,5.
\]

For six qubits, the local state comprises 64 complex amplitudes.
Two three-qubit gates, one HBM round trip
HBM

Load 64 complex32 amplitudes · 256 bytes

Registers / shared memory
Tensor Core MMA: \(U_A\)

Rearrange on-chip fragments
Tensor Core MMA: \(U_B\)


HBM

Store 64 complex32 amplitudes · 256 bytes


Conceptual flow. The intermediate result stays on-chip instead of being written back to HBM.
Interestingly, the two gates can be interpreted as left and right multiplications on an \(8\times8\) complex matrix:
\[
\boxed{\Psi'=U_A\Psi U_B^T}
\]

(up to your qubit-index convention).

This is an especially convenient case for Tensor Cores: both operations are small matrix multiplications, and all 64 complex amplitudes can be kept on-chip.

You avoid the cost of forming a dense \(64\times64\) six-qubit unitary.
3. The main constraint: how many distinct qubits are involved?
Suppose you fuse gates that collectively act on \(q\) distinct qubits.

To execute all of them without global-memory intermediates, a straightforward implementation keeps groups of \(2^q\) amplitudes on-chip.
Distinct qubits	Amplitudes per group	Complex32 storage
6	64	256 B
8	256	1 KiB
10	1,024	4 KiB
12	4,096	16 KiB
14	16,384	64 KiB
16	65,536	256 KiB

H100 has up to 228 KiB of shared memory per SM, with up to 227 KiB addressable by one thread block. 

Hopper Tuning Guide 13.4 documentation
+1




As the distinct-qubit count increases, shared-memory usage, occupancy, and data rearrangement become increasingly problematic.

A practical strategy is therefore to partition the circuit into gate groups whose union of target and control qubits remains small, while respecting gate dependencies.

This is similar to the shared-memory gate-grouping approach discussed in the quantum-circuit simulation literature. 

cds.cern.ch



4. What could prevent the expected speedup?
There are three particularly relevant issues for your design.

Tensor Core accumulator layout. The mma.sync instruction outputs FP32 accumulators in a warp-distributed register layout. The next MMA expects FP16 input fragments in a different layout. You need a conversion and potentially warp shuffles or shared-memory rearrangement between applications. That can become a significant bottleneck.

Cross-qubit permutations. When successive gates target different triples, the logical state matrix must be reindexed. For example, switching from qubits (0,1,2) to (3,4,5) effectively transposes the local \(8\times8\) amplitude arrangement. Keeping those permutations on-chip is essential.

Sequential dependencies. The next unitary cannot consume its input until the previous MMA result is available. With many gates, you may become limited by dependent MMA latency, conversion instructions, or shared-memory bandwidth rather than HBM. Multiple independent tiles in flight help hide that latency.

One special case is worth excluding from this approach: if several consecutive gates operate on exactly the same three qubits, precompute
\[
U_{\mathrm{combined}}=U_g\cdots U_2U_1
\]

and apply the combined \(8\times8\) gate once. This is usually cheaper than executing all the MMAs on-chip.
5. What I would implement on H100
I would prototype a warp-level kernel using mma.sync.m16n8k16.f32.f16.f16.f32, with the following structure:
// Conceptual pseudocode for a tiled state-vector kernel

// Load a locally closed set of amplitudes
Tile state = load_from_global(...);

// Apply several 3-qubit unitaries
for (int g = 0; g < num_gates; ++g) {

    // Reindex within registers/shared memory
    state = arrange_for_gate(state, gate[g].targets);

    // Complex FP16 Tensor Core MMA, FP32 accumulation
    Accumulator result = tensor_core_apply(
        gate[g].matrix, state
    );

    // Convert to FP16 for the next Tensor Core input
    state = convert_and_relayout(result);
}

// Single write-back
store_to_global(state);


For benchmarking, I would test 2, 4, 8, and 16 sequential three-qubit gates, comparing a single on-chip fused kernel against separate Tensor Core kernels and a register-based non-Tensor-Core implementation.

NVIDIA's cuStateVec algorithms documentation also describes pipelined gate application with gate fusion, although that does not establish the performance of your proposed FP16 Tensor Core implementation. 

NVIDIA cuQuantum




My conclusion: With complex32, executing several three-qubit unitaries over a limited set of qubits while keeping the amplitudes on-chip is a much more promising optimization than increasing the dimension of one dense fused matrix merely to improve Tensor Core utilization.

The most important performance parameter is likely to be the number of gates you can execute per HBM read/write pass without expensive on-chip permutations, rather than the number of qubits in any individual gate.
















Is the tensor core pipeline filled in such an implementation












2m 34s nachgedacht







Not automatically. In your proposed H100 implementation, the Tensor Core pipeline would likely be underutilized unless you execute enough independent state-vector tiles concurrently.

Applying many three-qubit gates in one kernel solves one problem—repeated HBM accesses—but introduces another: dependencies between consecutive Tensor Core operations.
1. Why a single chain of gates does not fill the pipeline
For complex32 (FP16 real and imaginary), a three-qubit gate is an \(8\times8\) complex matrix. Using realification, it fits the H100's warp-level FP16 MMA:
mma.sync.aligned.m16n8k16.row.col.f32.f16.f16.f32


A sequence of three-qubit gates looks like this:
One warp, dependent gate applications
MMA: Gate 1

Wait for result

Convert FP32 → FP16, rearrange fragments

MMA: Gate 2

Wait, convert, rearrange

MMA: Gate 3



The next MMA consumes the previous result, so it cannot execute independently.

For each gate, the warp performs one MMA, followed by FP32-to-FP16 conversion and possibly register shuffles or shared-memory operations.

Therefore, adding more sequential gates increases arithmetic intensity but not instruction-level parallelism within that chain.

Other independent warps can, however, execute their MMAs during these dependency stalls.
2. How much MMA latency is there?
A Hopper microbenchmark study by Luo et al. measured the following for the FP16 instruction you would use:
Measurement	Result on H800 (Hopper)
MMA shape	16×8×16
Inputs	FP16
Accumulator	FP32
Completion latency	24.1 clock cycles
Throughput	490.7 TFLOP/s
Fraction of FP16 peak	~65%



arXiv


These are H800 measurements of the MMA instruction itself, not measurements of an H100 quantum simulation kernel.

The study found that warp-level MMA instructions achieved approximately 62.9% of theoretical peak on average, whereas larger Hopper WGMMA instructions could exceed 95% under favorable microbenchmark conditions.

Consequently, even perfect scheduling of mma.sync is not necessarily enough to reach H100's full advertised FP16 throughput.
3. How to keep the Tensor Cores busy
The solution is to execute multiple independent chains of gates concurrently.

For example, instead of assigning only one state-vector tile to each warp, you could interleave two independent tiles:
// Conceptual instruction schedule

A = mma(U1, A);
B = mma(U1, B);  // Independent of A

A = mma(U2, A);
B = mma(U2, B);

A = mma(U3, A);
B = mma(U3, B);


The real implementation must perform the required FP32-to-FP16 conversions and fragment rearrangements between dependent operations.

Two mechanisms can hide the dependencies:
1. Warp-level parallelism: Different resident warps process independent state-vector tiles. When one warp waits for its MMA result, another warp can issue MMA instructions.
2. Instruction-level parallelism: Each warp handles two or more independent tiles and interleaves their operations.
The second approach can reduce dependency stalls, but requires more registers and may reduce occupancy. Increasing parallelism indefinitely is therefore not beneficial.

For a large state vector, there are usually enough independent amplitude groups to provide substantial warp-level parallelism.
4. What is likely to limit your implementation?
After retaining intermediate states on-chip, I would expect three possible bottlenecks:
Bottleneck	When it occurs
Dependent MMA latency	Too few independent warps or tiles
Register/shared-memory rearrangement	Consecutive gates act on different qubit triples
Instruction throughput	Conversion, permutation, and loading instructions consume many issue slots between MMAs

A particularly important point is that adding more sequential gates does not increase the ratio of MMA instructions to rearrangement instructions if every gate needs essentially the same amount of preparation.

So even with excellent occupancy, Tensor Core utilization may remain limited by the cost of preparing operands.
5. How I would measure it
Use Nsight Compute to inspect these metrics:
ncu --metrics \
sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_elapsed,\
smsp__warps_eligible.avg.per_cycle_active,\
dram__throughput.avg.pct_of_peak_sustained_elapsed \
./your_simulator


The first metric measures Tensor pipeline activity; the second helps identify whether schedulers have independent warps ready; the third measures HBM traffic utilization. Actual achieved FLOP/s must be evaluated separately.

I would benchmark three variants:
- One state-vector tile per warp, with sequential three-qubit MMAs.
- Two or four independent tiles per warp, with interleaved MMAs.
- Several warps sharing a larger on-chip state tile, with shared-memory rearrangement between gates.
My expectation: With one MMA per gate and a permutation/conversion step between gates, your initial implementation will probably not saturate the H100 Tensor Cores. Multiple resident warps should hide much of the MMA latency, but operand preparation may remain the main limitation.

The interesting optimization is therefore not simply fusing more gates, but arranging the state-vector tiles so that several independent Tensor Core MMAs can be issued while other gate results are being converted and permuted.

That is where I would focus the kernel design.