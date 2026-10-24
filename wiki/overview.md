# Overview

<!-- Agent-maintained entry point for the human. Keep it current whenever the picture changes; link every study that is not superseded. -->

## Question

How much faster is noisecirc than state-of-the-art GPU state-vector simulators of noisy circuits, and which part of the gain comes from its algorithm and which from its implementation? The focus is on gates whose noise is a non-mixed-unitary Kraus channel (such as amplitude damping), on qubits, `complex64`, noisecirc's exact sampling mode, and GPU state-vector simulators (PLAN.md).

## Current picture

noisecirc samples quantum trajectories by rejection: it proposes Kraus operators from state-independent upper bounds and accepts them by the norm of the propagated state, which lets it propose all shots before simulating, propagate each distinct trajectory once, and share trajectory prefixes through checkpoints, segment by segment and depth-first ([NoiseCirc's sampling algorithm](concepts/noisecirc-algorithm.md)). The literature check found the rejection-based exact sampling of non-mixed-unitary channels new; depth-first prefix reuse exists for Pauli noise, and wide shared-memory kernels exist without noise ([Prior art of noisecirc's algorithm](studies/prior-art.md)).

Its work is counted in block passes: launches of a fused block's kernel on one state vector. The passes follow a universal law in the expected errors per shot $M$, $P \approx BN[1/N + f(M)] + 2MN$ for amplitude damping, and noisecirc's own sampler, run on surrogate states without a GPU, predicts them to about 10% ([Block passes against noisecirc's parameters](studies/pass-count.md), [Block-pass cost model](concepts/block-pass-cost-model.md)).

On the H100, a run takes the passes times the bandwidth time of one state times 1.2 to 2.6 at noisecirc's defaults, and 1.3 to 1.8 with blocks of at most 32 gates; large blocks and the general (error) kernels are slower than the bandwidth on this GPU ([Block-pass time on the H100](studies/block-pass-time.md)). Against Qiskit Aer and CUDA-Q, noisecirc is 6 to 7700 times faster on amplitude damping, and the gain is algorithmic: wide fusion of noisy gates, sharing of trajectories and no norm passes, all enabled by proposing Kraus operators without the state; at equal algorithm the implementations are within a factor of 2 ([noisecirc against Qiskit Aer and CUDA-Q](studies/competitors.md)). Without running a circuit, its passes are predicted within 14% and its time within 33% (kernel-ratio model), as GPU runs of seven circuits and five channels confirm ([Benchmark circuits and predicted work](studies/benchmark-suite.md), [Validation of the predicted work](studies/validation.md)). Two performance issues of noisecirc were found and fixed on branches ([Issues found in noisecirc](studies/noisecirc-issues.md)).

## Key results

- noisecirc's exact rejection sampling of non-mixed-unitary channels with state-independent operator-norm proposals was not found in the literature; depth-first prefix reuse was (SANQ, TUSQ, Pauli noise only). Partially verified. [Prior art](studies/prior-art.md)
- Block passes are predicted by a dry run of noisecirc's sampler within 0.89 to 1.12 times (30 GPU runs), by a closed form within 0.70 to 1.93 times. Verified. [Block passes](studies/pass-count.md)
- At equal expected errors per shot, the passes per block and shot are the same function for all six circuits and, within about ±40%, for five noise types. Verified on dry runs. [Block passes](studies/pass-count.md)
- Time over passes times $t_{bw}$: 1.24 to 2.58 (geometric mean 1.81) at defaults, 1.29 to 1.84 with `max_operations` = 32, which costs no time overall. Verified, H100, damping, 24 to 28 qubits. [Block-pass time](studies/block-pass-time.md)
- Benchmark circuits fall into three fusion categories (chain, width-limited, gate-count-limited); at equal error load the passes hardly depend on the circuit or the non-mixed-unitary channel. Verified on dry runs and GPU runs. [Benchmark circuits](studies/benchmark-suite.md)
- GPU runs of 7 circuits × 5 channels at 28 qubits confirm the predictions: passes within 0.86 to 1.13 times, times within 1.00 to 1.33 times (kernel-ratio model). Verified. [Validation](studies/validation.md)
- noisecirc is 6 to 52 times faster than Aer's shot branching and 27 to 7700 times faster than per-shot trajectories (Aer, CUDA-Q) at 24 qubits; almost all of it is algorithmic: wide fusion of noisy gates (4 to 25 times), sharing of trajectories (2 to 270 times) and no norm passes (1.5 times), while the implementations are within a factor of 2 at equal algorithm. At 28 qubits Aer's shot branching runs out of device memory from 0.1 expected errors per shot. Verified, amplitude damping. [Competitors](studies/competitors.md)
- svpass's single-warp norm reduction made 28-qubit runs up to 1.7 times slower; fixed on `fix/squared-norms-parallel`. Verified. [Issues](studies/noisecirc-issues.md)
- `optimize_kraus` spread the no-error Kraus operator and filled the kernels' zero entries, making depolarizing runs up to 10 times slower; fixed on `fix/optimize-kraus-dominant`, after which it saves 20 to 30% at $M = 1$. Verified. [Issues](studies/noisecirc-issues.md)

## Open threads

- More register sizes, shot counts and noise types for the comparison with Aer and CUDA-Q (only amplitude damping at 24 and 28 qubits and 1000 shots so far).
- Task A5: validation runs of the most interesting circuits.
- Improvement opportunities for noisecirc: a block size chosen by the noise strength; a cheaper general kernel; the cumulative sums of the measurement at large registers.
