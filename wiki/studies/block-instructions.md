---
title: Fewer instructions per block pass
summary: "Applying a block with fewer floating-point instructions: fusing runs within stages and real rotations between deferred diagonals (A14)"
type: study
tasks: [A14]
status: verified
updated: 2026-10-24
---
# Fewer instructions per block pass

## Question

PLAN.md task A14 asks how to apply one block with as few floating-point operations as possible, using the structure of its gates (diagonal, controlled, sparse) and possibly a better contraction order than applying the gates one after another. On the H100 this matters because a pass is bound by the instructions it issues, arithmetic and shared-memory accesses together, Eq. (1) of [Precision, block size and the instruction-bound pass](kernel-regime.md).

## Approach

svpass generates one kernel per block. The kernel loads a tile of amplitudes into shared memory and applies the block in stages: a stage loads $2^R$ amplitudes per thread into registers ($R = 3$ by default), applies its gates one after another, unrolled and with zero entries pruned, and stores them back ([NoiseCirc's sampling algorithm](../concepts/noisecirc-algorithm.md)). In the benchmark circuits every gate is `r` (a dense one-qubit rotation), `rz` or `cp` (diagonal), each followed by amplitude damping, whose no-error operator $\mathrm{diag}(1, \sqrt{1-\gamma})$ is part of the gate's matrix. Within a stage, there are two ways to issue fewer instructions:

1. **Contraction order within a stage (stage fusion).** A run of consecutive gates can be multiplied into one matrix on the union of their qubits before the kernel is generated. A product on $k$ qubits costs up to $8 \cdot 2^k$ instructions per amplitude, its factors the sum of theirs, so fusing pays only for some runs: chains of diagonal gates, consecutive gates on the same qubit, gates whose product is sparse. A dynamic program over the stage's gates, in order, chooses the partition into runs with the fewest instructions, counted from the matrices exactly as the generator lowers them (`_matrix_cost`).
2. **Structure of one-qubit gates (rotation form).** Every one-qubit gate of the circuits, unitary or times a damping diagonal, factors as $M = D_L\,T\,D_R$ with diagonal $D_L, D_R$ and a real two-term matrix $T = \begin{pmatrix}1 & -t\\ t & 1\end{pmatrix}$ (or its cotangent form when $\lvert t\rvert > 1$). Applying $T$ costs one fused multiply-add per real component, 4 instructions per amplitude pair, against 6 to 8 for the dense complex $M$. The diagonals are multiplied into a pending diagonal at generation time, together with the stage's diagonal gates; before each $T$ on qubit $q$ only the part of the pending diagonal that depends on $q$ is applied, and the rest at the end of the stage.

The generator chooses, per stage, the cheaper of the two by its own count. Both are opt-in flags of svpass's `Config` (`stage_fusion`, `rotation_form`) on the noisecirc branch `feature/stage-fusion` (commit `7347915`); the defaults are unchanged.

The variants were checked and timed block by block against the default kernels on the same random state (`code/bench/a14_check.py`, 26 qubits, the A7 workloads at $M = 0.1$), and end to end at 28 qubits (`code/bench/a2_runs.py`). A lower bound on the instructions (`code/bench/a14_bound.py`) counts 2 per amplitude for every non-diagonal one-qubit gate after merging consecutive ones on the same qubit (each output component needs at least one fused multiply-add), nothing for diagonal gates, and 4 for the kernel's scaling and norm.

## Runs

- Stage fusion: `data/20261024-190130-a14-stage-fusion-check-n-26/` (LOG.md "A14 stage fusion check n=26").
- Stage fusion with rotation form: `data/20261024-*-a14-stage-fusion-and-rotation-form-check-n-26/` (LOG.md "A14 stage fusion and rotation form check n=26").
- Static counts and bound: `data/a13-static/a14-bound.txt`.
- End to end: `data/20261024-*-a13-a14-end-to-end-*-n-28/`, summary `data/a13-analysis/e2e.jsonl`.

## Results

### Both transformations are exact to single precision (verified)

On every block of the five circuits, dominant and masked kernels, the amplitudes after one pass differ from the default kernel's by at most $1.3\times10^{-6}$ of the largest amplitude, the rounding of `complex64`.

### Fewer instructions, and 11 to 15% faster passes where arithmetic binds (verified)

The table gives the mean floating-point instructions per amplitude of the circuits' dominant kernels, and the time of one trajectory (the sum of the dominant passes) relative to the default kernels:

| circuit | default | stage fusion | + rotation form | lower bound | time, fusion | time, + rotation |
| --- | --- | --- | --- | --- | --- | --- |
| GHZ | 84 | 39 | 39 | 38 | 1.00 | 1.00 |
| brickwork | 215 | 176 | 152 | 63 | 0.93 | 0.89 |
| QFT | 63 | 42 | 42 | 8 | 1.00 | 1.00 |
| QAOA | 160 | 77 | 62 | 26 | 0.86 | 0.85 |
| grid | 207 | 160 | 150 | 59 | 0.92 | 0.87 |
| random (static only) | 297 | 74 | 74 | — | | |

Three observations:

- **Diagonal chains are the largest saving.** QAOA's cost layers of `rz` and `cp` and the damping diagonals fuse into one diagonal per stage: 160 to 62 instructions. In the deep random circuit, consecutive one-qubit gates on the same qubit fuse into one: 297 to 74.
- **The time follows only where arithmetic binds.** GHZ is at the memory floor and the QFT is bound by shared accesses (Eq. (1) of the precision study), so fewer instructions do not shorten their passes. They do shorten them once the stages are wider and the state smaller: with 4-qubit stages and `complex32`, the QFT's trajectory takes 0.60 of the default time, see [Precision, block size and the instruction-bound pass](kernel-regime.md).
- **The masked kernels of trajectories with an error gain as much** (0.82 to 0.99 of their default time), because their non-deviating stages use the same generated code.

### The remaining gap to the bound is the diagonals' phases (verified, static)

Brickwork, grid and QAOA still issue 2.3 to 2.6 times the lower bound, and the QFT 5 times. The bound counts diagonal gates as free, while a controlled phase between two rotations on the same qubits must be applied in between: in the rotation form each rotation pays 2 instructions per amplitude for the part of the pending diagonal on its qubit, and each stage up to 4 for the rest. GHZ, without such interleaving, reaches the bound. Closing the gap would need diagonals that are applied outside the stages that hold their qubits, from the bits of the amplitude index, which also removes stages; the brainstorm of task A15 estimated that this saves a third to a half of the shared accesses ([Directions beyond the current algorithm](new-directions.md)).

### End to end (verified)

On whole noisy runs at 28 qubits, the A14 kernels make noisecirc 0 to 11% faster in `complex64` (geometric mean 6%) and, with 4-qubit stages and `complex32`, 1.45 to 1.9 times faster, against 1.18 to 1.41 times for `complex32` with the default kernels; the table is in [Precision, block size and the instruction-bound pass](kernel-regime.md).

## Caveats

- The instruction counts are a static model of the generated statements; the compiler may emit a few more or fewer. The times are measured.
- The rotation form needs every non-diagonal operation of a stage to be a one-qubit matrix of the form $D_L T D_R$, which holds for unitaries and unitaries times diagonals; other stages (two-qubit dense gates, general non-unitary Kraus operators) keep the fused or sequential code.
- Contraction order was optimised within stages and in gate order; reordering commuting gates and choosing the stages themselves by cost (rather than by width, as noisecirc's fusion does) were not tried.
- One device, five circuits, amplitude damping.

## Verdict

Using the gates' structure lowers the floating-point instructions of noisecirc's kernels by 18 to 75% at unchanged accuracy, with code-generation changes only and no change to the kernel itself. Where a pass is bound by arithmetic, it becomes 11 to 15% faster; elsewhere the saving appears only together with wider stages and `complex32`. A contraction into dense matrices pays only for diagonal chains and runs on the same qubits; the remaining factor of about 2.5 to the instruction bound lies in the controlled phases between rotations, which would need diagonals applied outside the stage structure.
