# Overview

<!-- Agent-maintained entry point for the human. Keep it current whenever the picture changes; link every study that is not superseded. -->

## Question

How much faster is noisecirc than state-of-the-art GPU state-vector simulators of noisy circuits, and which part of the gain comes from its algorithm and which from its implementation? The focus is on gates whose noise is a non-mixed-unitary Kraus channel (such as amplitude damping), on qubits, `complex64`, noisecirc's exact sampling mode, and GPU state-vector simulators (PLAN.md).

## Current picture

noisecirc samples quantum trajectories by rejection: it proposes Kraus operators from state-independent upper bounds and accepts them by the norm of the propagated state, which lets it propose all shots before simulating, propagate each distinct trajectory once, and share trajectory prefixes through checkpoints, segment by segment and depth-first ([NoiseCirc's sampling algorithm](concepts/noisecirc-algorithm.md)). The literature check found the rejection-based exact sampling of non-mixed-unitary channels new; depth-first prefix reuse exists for Pauli noise, and wide shared-memory kernels exist without noise ([Prior art of noisecirc's algorithm](studies/prior-art.md)).

Its work is counted in block passes: launches of a fused block's kernel on one state vector. The passes follow a universal law in the expected errors per shot $M$, $P \approx BN[1/N + f(M)] + 2MN$ for amplitude damping, and noisecirc's own sampler, run on surrogate states without a GPU, predicts them to about 10% ([Block passes against noisecirc's parameters](studies/pass-count.md), [Block-pass cost model](concepts/block-pass-cost-model.md)).

On the H100, a run takes the passes times the bandwidth time of one state times 1.2 to 2.6 at noisecirc's defaults, and 1.3 to 1.8 with blocks of at most 32 gates; large blocks and the general (error) kernels are slower than the bandwidth on this GPU ([Block-pass time on the H100](studies/block-pass-time.md)). A bug in noisecirc's norm reduction slowed 28-qubit runs by up to 1.7 times and is fixed on a branch ([Issues found in noisecirc](studies/noisecirc-issues.md)).

## Key results

- noisecirc's exact rejection sampling of non-mixed-unitary channels with state-independent operator-norm proposals was not found in the literature; depth-first prefix reuse was (SANQ, TUSQ, Pauli noise only). Partially verified. [Prior art](studies/prior-art.md)
- Block passes are predicted by a dry run of noisecirc's sampler within 0.89 to 1.12 times (30 GPU runs), by a closed form within 0.70 to 1.93 times. Verified. [Block passes](studies/pass-count.md)
- At equal expected errors per shot, the passes per block and shot are the same function for all six circuits and, within about ±40%, for five noise types. Verified on dry runs. [Block passes](studies/pass-count.md)
- Time over passes times $t_{bw}$: 1.24 to 2.58 (geometric mean 1.81) at defaults, 1.29 to 1.84 with `max_operations` = 32, which costs no time overall. Verified, H100, damping, 24 to 28 qubits. [Block-pass time](studies/block-pass-time.md)
- svpass's single-warp norm reduction made 28-qubit runs up to 1.7 times slower; fixed on `fix/squared-norms-parallel`. Verified. [Issues](studies/noisecirc-issues.md)

## Open threads

- Task A4: choice of benchmark circuits and predictions of their work (dry-run predictions for 7 circuit categories and 5 noise types computed).
- Task A5: validation runs of the most interesting circuits.
- Task A6: Qiskit Aer (shot branching, batched, plain) and CUDA-Q on the same circuits, translated into passes.
- Improvement opportunities for noisecirc: a block size chosen by the noise strength; a cheaper general kernel; the cumulative sums of the measurement at large registers.
