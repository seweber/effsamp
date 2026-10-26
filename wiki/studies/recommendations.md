---
title: Recommendations for noisecirc
summary: What to merge, what to make default, what to build next and what not to pursue in noisecirc, from the findings of tasks A1 to A16 (A17)
type: study
tasks: [A17]
status: verified
updated: 2026-10-26
---
# Recommendations for noisecirc

## Question

PLAN.md task A17 asks for recommendations for improving noisecirc, drawn from the findings of tasks A1 to A16. This page ranks them by how firmly they are established and by what they gain. It adds no new measurements; every recommendation links the study that supports it.

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

All branches named below are local branches of the noisecirc repository in `code/noisecirc` (not pushed). They build on each other: `bench/fixes` is `main` with the fixes and the first two improvements merged, `feature/stage-fusion` builds on `bench/fixes`, `feature/stage-contraction` on `feature/stage-fusion`, and `feature/tensor-cores` on `feature/stage-contraction`.

## Runs

No runs of its own. The evidence is in the runs of the linked studies; the measurements made for this write-up are those of the A13 follow-up and of A16 (LOG.md, 2026-10-26).

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

### 3. Decide: a complex32 mode for 1.5 to 1.9 times faster runs (verified, with an accuracy caveat)

Storing amplitudes as pairs of 16-bit floats, while computing in single precision, halves the bytes per pass. Once the kernels issue few instructions (recommendation 2), this pays: whole runs are 1.5 to 1.9 times faster than today's defaults (geometric mean 0.585; QFT 0.52, brickwork 0.57) ([Precision, block size and the instruction-bound pass](kernel-regime.md)).

The price is accuracy. `complex32` is accurate to about $10^{-3}$ instead of $10^{-6}$: total variation distances of 1.5 to $8.6 \times 10^{-4}$ and squared-norm errors up to $4.7 \times 10^{-4}$ for the no-error trajectory. Because noisecirc accepts proposals by squared norms, sampling is then exact only up to about $10^{-3}$, a bias rather than noise. This is far below the statistical error of thousands of shots, but it is a different promise from "exact sampling". Whether to offer it, as an opt-in mode with the accuracy stated, is a decision for noisecirc's author (it also touches PLAN.md's restriction to `complex64` for this project).

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

### 5. Do not pursue (verified or estimated)

| idea | why not | evidence |
| --- | --- | --- |
| Tensor cores | Single-precision modes are 15% to 2.6 times slower; FP16 products gain 4 to 8% on brickwork only, at an accuracy worse than `complex32` | [Tensor cores for block passes](tensor-cores.md) |
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

None of these changes how noisecirc compares with other simulators in kind: its lead of 6 to 52 times over Aer's shot branching is algorithmic, from wide fusion of noisy gates, shared trajectories and the absence of norm passes ([noisecirc against Qiskit Aer and CUDA-Q](competitors.md)).

### Further suggestions

- **Expose the cost model.** noisecirc's sampler, run on surrogate states without a GPU, predicts the block passes within 14%; with measured kernel ratios the run time within 33% ([Validation of the predicted work](validation.md)). A "dry run" entry point would let users plan runs and could replace the timing-based autotuning.
- **Sampling's prefix sum.** Drawing measurement outcomes computes a prefix sum with one thread block per row, about 2.6 ms per call at 28 qubits (5% of a 20 s run). It is not changed yet ([Issues](noisecirc-issues.md), issue 2).

## Caveats

- One GPU (H100 PCIe), amplitude damping for most kernel measurements, five benchmark circuits at 24 to 28 qubits; other devices may favour other settings (proposal T004 was declined).
- Gains of different recommendations were measured on different baselines and do not multiply exactly. The kernel options and autotuning, in particular, were not measured together.
- First-jump sampling and peeling the last block are estimates (small registers, dry runs, kernel prototype), not implementations in noisecirc.
- `complex32`'s effect on sampling was checked for the no-error trajectory, not for whole sampled distributions.

## Verdict

noisecirc's algorithm is sound and its main lead over other simulators is algorithmic; the improvements found are of two kinds:

- **Ready now:** four verified fixes and improvements to merge, and three kernel options to make default, about 11% faster at unchanged accuracy.
- **Two larger steps:**
  - a `complex32` mode, 1.5 to 1.9 times faster at an accuracy of about $10^{-3}$, for noisecirc's author to decide;
  - first-jump sampling, which removes the rejected proposals and is estimated at 1.1 to 2.5 times at one error per shot and more at strong noise.

Tensor cores, stages that ignore diagonal gates, half-precision arithmetic, larger tiles and tighter proposal bounds were tested and should not be pursued.
