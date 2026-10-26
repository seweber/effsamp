---
title: Recommendations for noisecirc
summary: What to merge, what to make default, what to build next and what not to pursue in noisecirc, from the findings of tasks A1 to A16 (A17), updated with A18 and A19
type: study
tasks: [A17, A18, A19]
status: verified
updated: 2026-10-26
---
# Recommendations for noisecirc

## Question

PLAN.md task A17 asks for recommendations for improving noisecirc, drawn from the findings of tasks A1 to A16; tasks A18 (tensor cores for `complex32`, after a brainstorm) and A19 (fewer instructions per gate, after a brainstorm) ask to update them. This page ranks them by how firmly they are established and by what they gain. It adds no new measurements; every recommendation links the study that supports it.

## Approach

### What the recommendations rest on

noisecirc's run time on large registers is the number of block passes times the time per pass ([Block-pass cost model](../concepts/block-pass-cost-model.md)). The improvements found act on one of the two factors:

- **Fewer passes**, an algorithmic gain. The passes follow $P \approx BN[1/N + f(M)] + 2MN$ for amplitude damping, with $B$ blocks, $N$ shots and $M$ expected errors per shot ([Block passes against noisecirc's parameters](pass-count.md)). The first term, every distinct trajectory propagated through the rest of the circuit, is a floor for any exact state-vector sampler that materialises trajectories. The second, the error proposals, half of which are rejected, is not ([Directions beyond the current algorithm](new-directions.md)).
- **Shorter passes**, an implementation gain. On the H100 a pass is bound by the instructions it issues, arithmetic, integer and shared-memory accesses together, and takes 1.1 to 2.6 times the time of reading and writing the state ([Precision, block size and the instruction-bound pass](kernel-regime.md)).

### How the recommendations are ranked

1. **Merge:** fixes and improvements that are verified on the GPU, change no result and need no decision.
2. **Make default:** kernel options that are verified and faster, after review.
3. **Decide:** an option that trades accuracy for speed (`complex32`).
4. **Build next:** algorithmic changes whose gain is estimated, not yet implemented in noisecirc.
5. **Do not pursue:** ideas that were measured or estimated not to pay.

All branches named below are local branches of the noisecirc repository in `code/noisecirc` (not pushed). They build on each other: `bench/fixes` is `main` with the fixes and the first two improvements merged, `feature/stage-fusion` builds on `bench/fixes`, `feature/stage-contraction` on `feature/stage-fusion`, `feature/tensor-cores` on `feature/stage-contraction`, and `feature/two-level-rotations` on `feature/tensor-cores`.

## Runs

No runs of its own. The evidence is in the runs of the linked studies; the measurements made for this write-up are those of the A13 follow-up, of A16, and for the update those of A18 and A19 (LOG.md, 2026-10-26).

## Results

### 1. Merge: fixes and verified improvements (verified)

| change | branch | effect | evidence |
| --- | --- | --- | --- |
| Sum the squared norms of long rows with many thread blocks instead of one warp | `fix/squared-norms-parallel` | 28-qubit runs up to 1.7 times faster | [Issues](noisecirc-issues.md), issue 2 |
| Keep the dominant Kraus operator when `optimize_kraus` rotates the others, and aim at the residual bound | `fix/optimize-kraus-dominant`, then `fix/optimize-kraus-residual-target` | `optimize_kraus` saves 20 to 30% at one error per shot instead of making depolarizing runs up to 10 times slower | [Issues](noisecirc-issues.md), issues 3 and 4 |
| Masked kernels for trajectories with errors: the dominant code in every stage but those the trajectory deviates in | `feature/masked-error-kernels` | runs 4 to 13% faster; the best block size no longer depends on the noise | [Error kernels and block sizes](error-kernels.md) |
| Correct DOI of a reference | `fix/elsman-doi` | documentation | [Issues](noisecirc-issues.md), issue 1 |

None of these changes a sampled distribution; all were measured in whole runs.

### 2. Make default: faster kernels at unchanged accuracy (verified)

The code generator can apply a block's gates with far fewer instructions. Three options of svpass, all on `feature/stage-contraction` and off by default, together with 4-qubit stages:

- **Cheapest contraction order of each stage** (`stage_contraction`): which gates of a stage to multiply into one matrix, found exactly as a shortest path over the stage's dependency graph. It contains the A14 options `stage_fusion` and `rotation_form` (real rotations between deferred diagonals) as special cases.
- **Immediate shared-memory addresses** (`additive_addresses`): most loads and stores take their address as a constant offset instead of computing it.
- **4-qubit stages** (`stage_qubits = 4`): fewer stages, each costing 2 shared accesses per amplitude and a fixed setup.

Measured on whole runs at 28 qubits (amplitude damping, $M$ = 0.1 and 1, five circuits), relative to the current defaults: geometric mean 0.89, from 0.80 (brickwork) to 1.01 (GHZ, unchanged), at the same accuracy as today's kernels ([Precision, block size and the instruction-bound pass](kernel-regime.md)).

Two further improvements combine with these:

- **Autotuning** of block size and stage width per circuit (`feature/autotune`, off by default): 0 to 14% (6% on average) at a one-time cost of seconds ([Error kernels and block sizes](error-kernels.md)). It was measured with the older kernels, so its gain on top of 4-qubit stages may be smaller.
- **H100-specific settings** (`max_operations` = 64, `group_amplitudes` = 4096): 4% on average with the older kernels ([Tuning noisecirc's parameters on the H100](parameter-tuning.md)). Autotuning would subsume this.

The recommendation is to make `stage_contraction`, `additive_addresses` and 4-qubit stages the defaults, after a review of the generated code, and to remove the A14 options that `stage_contraction` contains. The contraction search costs 0.04 to 1.25 s per block in Python; kernels are cached on disk, so this is paid once per block.

A small addition from A19: **two-level rotations** (`two_level_rotations`, commit `d07b8c5` on `feature/two-level-rotations`) extend the rotation form from one-qubit gates to multi-qubit gates that rotate pairs of basis states: controlled rotations, fSim and XX+YY gates, $\exp(-i\theta P\otimes P)$. It is verified (unchanged accuracy, error kernels within $2 \times 10^{-7}$) and makes circuits of such gates 0 to 8% faster with 4-qubit stages (CRY brickwork 7.9% in `complex32`, fSim grid 5.5%, Heisenberg chain unchanged); it changes nothing for the benchmark circuits, whose two-qubit gates are diagonal ([Fewer instructions per gate](gate-arithmetic.md)). Its commit touches only the rotation form and can be moved onto `feature/stage-contraction` without the tensor-core prototype.

### 3. Decide: a complex32 mode for 1.5 to 1.9 times faster runs (verified, with an accuracy caveat)

Storing amplitudes as pairs of 16-bit floats, while computing in single precision, halves the bytes per pass. Once the kernels issue few instructions (recommendation 2), this pays: whole runs are 1.5 to 1.9 times faster than today's defaults (geometric mean 0.585; QFT 0.52, brickwork 0.57) ([Precision, block size and the instruction-bound pass](kernel-regime.md)).

The price is accuracy. `complex32` is accurate to about $10^{-3}$ instead of $10^{-6}$: total variation distances of 1.5 to $8.6 \times 10^{-4}$ and squared-norm errors up to $4.7 \times 10^{-4}$ for the no-error trajectory. Because noisecirc accepts proposals by squared norms, sampling is then exact only up to about $10^{-3}$, a bias rather than noise. This is far below the statistical error of thousands of shots, but it is a different promise from "exact sampling". Whether to offer it, as an opt-in mode with the accuracy stated, is a decision for noisecirc's author (it also touches PLAN.md's restriction to `complex64` for this project).

If the mode is offered, A18 adds a cheap option to it: **tensor-core stages in `f16x2` for dense stages only** (`tensor_cores = "f16x2"`, `tensor_threshold = 24`, already on `feature/tensor-cores`). For circuits of dense two-qubit gates (su4 brickwork, 3-qubit stages) passes get 16% shorter; the benchmark circuits are unchanged (0.98 to 1.00), as none of their stages reaches the threshold. Its accuracy is that of `complex32` within a factor of 1.2 to 3 in total variation distance (su4: $9.5 \times 10^{-4}$ against $3.4 \times 10^{-4}$), so it belongs to the `complex32` mode, not to the default ([Chained tensor-core stages and complex32](chained-tensor-cores.md)).

### 4. Build next: fewer passes by sampling first errors exactly (partially verified)

The largest remaining gain is algorithmic. **First-jump sampling** (proposal T005) removes the rejected error proposals. During the pass that a checkpoint's no-error path makes anyway, the kernel sums the exact probabilities of every possible first error in the block; one multinomial draw then splits all shots of the checkpoint over "no error" and "first error at gate $g$ with operator $i$". Nothing is rejected, and the oversampling ceiling that splits blocks at strong noise is no longer needed ([Directions beyond the current algorithm](new-directions.md)).

- **Exactness:** verified with a NumPy reference on noisecirc's compiled blocks against density matrices (6 qubits).
- **Passes:** 1.04 to 3.3 times fewer at up to one expected error per shot, 1.7 to 4.7 times at three (10 qubits, real states).
- **Kernel cost:** the reductions add about a fifth to a pass (prototype, 26 qubits).
- **Net:** no gain at $M = 0.1$, 1.1 to 2.5 times at $M = 1$, 1.5 to 3.9 times at $M = 3$. That is where noisecirc's lead over Qiskit Aer is smallest ([noisecirc against Qiskit Aer and CUDA-Q](competitors.md)). Skipping the reductions where no shot can err would remove the loss at weak noise.

It changes noisecirc's core loop (a dominant pass before the error passes of each segment) but keeps its core idea: shared trajectories and state-independent proposals for everything else. Estimated cost: about a week.

Three smaller algorithmic changes are exact and cheap but pay only for some circuits:

| change | gain | evidence |
| --- | --- | --- |
| Optimal Kraus sets for channels with a mixed-unitary part (via the fixed `optimize_kraus`), computed once per channel instead of once per gate | runs 1.1 to 1.4 times faster for such channels; less compile time | [Optimal Kraus representations](kraus-representation.md) |
| Readout map: damping in a circuit's diagonal tail applied to the sampled bits instead of simulated | 1.5 to 1.6 times fewer passes for GHZ, a few percent otherwise | [Directions beyond the current algorithm](new-directions.md) |
| Peeling the last block: sample the qubits outside its tile from the entering checkpoint | 1.5 times for GHZ (3 blocks), 1.03 to 1.08 for circuits of 9 to 30 blocks | [Directions beyond the current algorithm](new-directions.md) (estimate) |

The default Kraus set needs no change for amplitude damping: noisecirc's canonical set is already provably optimal there ([Optimal Kraus representations](kraus-representation.md)).

A larger kernel project, ranked below first-jump sampling, follows from A18: **a `complex32` pass built around tensor-core stages chained in registers.** A microbenchmark shows that the tensor cores keep 8 to 16 dense 3-qubit gates per pass at memory speed when several tiles per warp are in flight, and that in such a kernel `f16x2` stages are a quarter to a third cheaper than brickwork-like stages on the CUDA cores. noisecirc's current tensor-core stages, which pass every stage through shared memory in single precision, do not reach this. Realizing it needs FP16 tiles in shared memory, stages chained in registers where their qubits allow, and several tiles per warp; the gain would apply to arithmetic-heavy circuits (brickwork, grid) and not to GHZ, QFT or QAOA, and it is an estimate ([Chained tensor-core stages and complex32](chained-tensor-cores.md)).

### 5. Do not pursue (verified or estimated)

| idea | why not | evidence |
| --- | --- | --- |
| Tensor cores in `complex64` | Single-precision modes are 15% to 2.6 times slower on the benchmark circuits; FP16 products gain 4 to 8% on brickwork only, at an accuracy worse than `complex32`. In `complex32` see recommendations 3 and 4 | [Tensor cores for block passes](tensor-cores.md), [Chained tensor-core stages and complex32](chained-tensor-cores.md) |
| Three complex shears per one-qubit gate (A19 brainstorm) | 12 FMA per amplitude pair, against 4 to 8 for the rotation form noisecirc already uses; measured slower per gate | [Fewer instructions per gate](gate-arithmetic.md) |
| KAK decomposition of dense two-qubit gates | Its five pieces cost 24 instructions per amplitude in rotation form, the dense matrix 16 | [Fewer instructions per gate](gate-arithmetic.md) |
| Gauss's three-product form for dense products | 3 to 7% for chains of dense 3-qubit gates, nothing for the benchmark circuits | [Fewer instructions per gate](gate-arithmetic.md) |
| Stages that ignore diagonal gates | Fewer stages, but run-time factors and lost contraction make 4-qubit-stage passes 3 to 24% slower | [Precision, block size and the instruction-bound pass](kernel-regime.md) |
| Half-precision arithmetic | Biases squared norms by up to 4% | [Precision, block size and the instruction-bound pass](kernel-regime.md) |
| Wider tiles (11 qubits) or blocks beyond 128 gates | Occupancy drops; the blocks of the benchmark circuits are limited by width, not gate count | [Precision, block size and the instruction-bound pass](kernel-regime.md) |
| Checkpoint-dependent proposal bounds | At most 6% fewer passes (QFT), even perfect bounds 4 to 36% | [Checkpoint-dependent proposal bounds](tighter-bounds.md) |
| Lower-bound (per-shot) sampling as in qsim | Gives up the sharing of trajectories, which is most of noisecirc's gain | [noisecirc against delayed lower-bound sampling](lower-bound-sampling.md) |

The prototype code of the first two rows (`tensor_cores`, `tensor_unroll`, `tensor_threshold`, `free_diagonals`, only on `feature/tensor-cores`) should not be merged: it adds code without gain. Merging `feature/stage-contraction` leaves it out, but brings the A15 timing prototype `stage_populations` (commit `0aba53f` in its history), which should be reverted to keep noisecirc's code minimal.

### What the recommendations add up to

Relative to today's `bench/fixes` defaults in `complex64`, on the benchmark circuits at 28 qubits:

- **Recommendations 1 and 2:** about 11% faster on average, up to 20% for brickwork. The fixes of recommendation 1 are already in the baseline; against `main`, the squared-norm fix alone is worth up to 1.7 times at 28 qubits.
- **With `complex32` (3):** 1.5 to 1.9 times faster.
- **With first-jump sampling (4):** a further 1.1 to 2.5 times at one expected error per shot, more at strong noise (estimate).
- **For circuits of dense or rotating two-qubit gates:** two-level rotations 0 to 8%, and in `complex32` tensor-core stages for dense stages 16% (A18, A19).

None of these changes how noisecirc compares with other simulators in kind: its lead of 6 to 52 times over Aer's shot branching is algorithmic, from wide fusion of noisy gates, shared trajectories and the absence of norm passes ([noisecirc against Qiskit Aer and CUDA-Q](competitors.md)).

### Further suggestions

- **Expose the cost model.** noisecirc's sampler, run on surrogate states without a GPU, predicts the block passes within 14%; with measured kernel ratios the run time within 33% ([Validation of the predicted work](validation.md)). A "dry run" entry point would let users plan runs and could replace the timing-based autotuning.
- **Sampling's prefix sum.** Drawing measurement outcomes computes a prefix sum with one thread block per row, about 2.6 ms per call at 28 qubits (5% of a 20 s run). It is not changed yet ([Issues](noisecirc-issues.md), issue 2).

## Caveats

- One GPU (H100 PCIe), amplitude damping for most kernel measurements, five benchmark circuits at 24 to 28 qubits; other devices may favour other settings (proposal T004 was declined).
- Gains of different recommendations were measured on different baselines and do not multiply exactly. The kernel options and autotuning, in particular, were not measured together.
- First-jump sampling and peeling the last block are estimates (small registers, dry runs, kernel prototype), not implementations in noisecirc. So is the gain of a pass built around chained tensor-core stages (a microbenchmark outside noisecirc).
- The circuits of A18 and A19 with dense or rotating two-qubit gates (su4, fSim, CRY, Heisenberg) are synthetic workloads added for these tasks; their gains were measured per pass, not in whole runs.
- `complex32`'s effect on sampling was checked for the no-error trajectory, not for whole sampled distributions.

## Verdict

noisecirc's algorithm is sound and its main lead over other simulators is algorithmic; the improvements found are of two kinds:

- **Ready now:** four verified fixes and improvements to merge, and three kernel options to make default, about 11% faster at unchanged accuracy; two-level rotations add 0 to 8% for circuits of controlled rotations and fSim gates.
- **Two larger steps:**
  - a `complex32` mode, 1.5 to 1.9 times faster at an accuracy of about $10^{-3}$, for noisecirc's author to decide; with it, tensor-core stages for dense stages make circuits of dense two-qubit gates 16% faster;
  - first-jump sampling, which removes the rejected proposals and is estimated at 1.1 to 2.5 times at one error per shot and more at strong noise.

Tensor cores in `complex64`, stages that ignore diagonal gates, half-precision arithmetic, larger tiles, tighter proposal bounds, shear and KAK forms of gates were tested and should not be pursued. The brainstorms of A18 and A19 were right that fusing many gates per pass matters more than the form of one gate; noisecirc's blocks already do this, and its rotation form is at the instruction bound of a gate that mixes two amplitudes.
