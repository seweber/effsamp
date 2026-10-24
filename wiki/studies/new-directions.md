---
title: Directions beyond the current algorithm
summary: Brainstormed ideas for fundamentally faster noisecirc and the estimates or tests of the most promising (A15)
type: study
tasks: [A15]
status: partially verified
updated: 2026-10-24
---
# Directions beyond the current algorithm

## Question

PLAN.md task A15 asks whether something overlooked so far could fundamentally improve noisecirc's efficiency, staying with state vectors (no tensor networks, no Clifford methods). The ideas were gathered by brainstorming with three subagents, and the most promising were tried.

## Approach

Three subagents, each given the wiki's algorithm, cost model and results and a different angle, proposed and ranked ideas (2026-10-24, reports summarised in `memory/tasks/A15.md`):

- the sampling algorithm and the structure of the trajectory tree;
- the mathematics of trajectories (linearity, unravellings, exactness);
- the GPU execution of a pass.

Their ideas were then tested in proportion to their promise:

1. by a reference implementation with real states on small registers, which checks exactness against density matrices and counts passes exactly (`code/bench/a15_firstjump_ref.py`, `code/bench/a15_readout_check.py`);
2. by dry runs of noisecirc's own sampler at 28 qubits (`code/bench/a15_readout.py`, `code/bench/a15_peel.py`) or the pass model of the [Block-pass cost model](../concepts/block-pass-cost-model.md) (`code/bench/a15_firstjump.py`);
3. for kernel ideas, by implementing them in svpass's code generator and timing them on the H100 (tasks A13 and A14).

## Runs

- First-jump sampling, exactness on 6 qubits: `data/a15-firstjump/check-n6.jsonl`; passes on 10 qubits: `data/20261024-195809-a15-first-jump-reference-pass-counts-n-10/` (LOG.md "A15 first-jump reference pass counts n=10"); kernel cost: `data/20261024-2032*-a15-population-reductions-v2-*` (LOG.md "A15 population reductions v2 …"; the contended v1 prototype in LOG.md "A15 population reductions v1 summary").
- Readout map: `data/a15-readout/check-n6.txt`, `data/*-a15-readout-map-dry-run/` (LOG.md "A15 readout map dry run").
- Peeling the last block: `data/a15-peel/peel.jsonl`.
- Kernel ideas: the runs of [Precision, block size and the instruction-bound pass](kernel-regime.md) and [Fewer instructions per block pass](block-instructions.md).

## Results

### The ideas and how they were judged

The subagents on sampling and on mathematics agreed on one point: the term $BN f(M)$ of the pass model, the propagation of every distinct trajectory through the rest of the circuit, is a floor for any exact state-vector sampler that materialises distinct trajectories. What can still be gained lies in the rejected proposals ($2MN$ in total, of which half are rejected), in the blocks at the circuit's end, and in the time per pass. The ideas, ranked by their estimated gain:

| idea | where it saves | status |
| --- | --- | --- |
| First-jump sampling (below) | rejected proposals; the oversampling ceiling at strong noise | exactness verified, passes measured with real states, kernel cost measured |
| Fewer instructions per pass: structure, wider stages, then `complex32` | time per pass | implemented and measured (A13, A14): 1.45 to 1.9 times end to end |
| Readout map for noise in the circuit's diagonal tail | channels at the end | exactness verified, dry run |
| Peeling the last block | passes of the last block | dry-run estimate |
| Diagonals outside the stage structure; asynchronous tile loads; first and last stage straight from global memory | time per pass | estimated only (5 to 30%) |
| Scheduling channels as late as possible; fork kernel for a checkpoint's error children; canonical jump positions | a few percent | not pursued |
| Random-phase superpositions of trajectories; delta states; tensor cores; thread-block clusters; warp shuffles | — | judged not to pay or not exact |

### First-jump sampling: exact, and 1.04 to 4.7 times fewer passes (verified on small registers)

noisecirc proposes errors from state-independent bounds and pays a pass for every proposal, also for the half that is rejected. First-jump sampling instead computes the exact probability of every possible first error in a block during the pass that the checkpoint's no-error path makes anyway. Within a block, the kernel does not normalise, so the probability that a trajectory leaves the dominant choice for the first time at gate $g$ with operator $K_i$ is

$$P(g, i) = \bigl\lVert K_i\, D_{<g}\, \psi \bigr\rVert^2, \tag{1}$$

with $D_{<g}$ the product of the dominant operators before $g$. For amplitude damping, $P(g, 1) = \gamma\, n_q$ with $n_q$ the population of the gate's qubit at that point, a sum the kernel can accumulate. These probabilities and that of no error, $\lVert D\psi\rVert^2$, sum to one, so one multinomial draw splits all shots of the checkpoint exactly over {no error, first error at $(g, i)$}. Each group that erred costs one pass, which continues from $(g, i)$ and yields the probabilities of its next error in the block in the same way. Nothing is ever rejected, and every probability is computed rather than bounded.

Two gains follow:

1. **No rejected proposals.** The error passes fall from about $2MN$ to $MN$.
2. **No oversampling ceiling.** noisecirc splits a block once its proposals' oversampling exceeds $e$, so that rejections stay cheap; at strong noise that makes blocks small and many. Without rejections, blocks can be as large as the fusion allows.

A NumPy reference of both samplers on noisecirc's own compiled blocks shows that first-jump sampling is exact: on 6 qubits, 200 000 shots of brickwork and GHZ at 0.3 and 2 expected errors per shot have $\chi^2$ of 57 to 70 for 63 degrees of freedom against the density matrix, like noisecirc's own sampler. On 10 qubits, with real states and 1000 shots, its passes relative to noisecirc's scheme:

| circuit | $M = 0.1$ | $M = 1$ | $M = 3$ | $M = 3$, no ceiling |
| --- | --- | --- | --- | --- |
| GHZ | 1.09 | 2.21 | 1.71 | 3.50 |
| brickwork | 1.22 | 1.51 | 1.68 | 1.97 |
| QFT | 1.33 | 3.06 | 2.35 | 4.73 |
| QAOA | 1.04 | 1.32 | 1.73 | 1.78 |

(Factor of fewer passes, single seed.) The QFT gains most because its qubits wait in $|0\rangle$, where a damping jump has probability zero and noisecirc's proposals are all rejected. For 28 qubits, the pass model with noisecirc's own block counts gives 1.07 to 2 times at $M \le 1$ and 1.6 to 4 times at $M = 10$ (`code/bench/a15_firstjump.py`).

### What first-jump sampling costs in the kernel (verified, prototype)

The probabilities of Eq. (1) must be summed during the pass. A timing prototype (svpass `Config.stage_populations`, branch `feature/stage-fusion`) makes every stage of a kernel sum the populations of its register qubits per thread, reduce them over the warp by shuffles, and write one partial sum per warp to its own address, as a real implementation would next to the chunk sums. On the circuits' dominant passes at 26 qubits it costs:

| kernels | GHZ | brickwork | QFT | QAOA | grid |
| --- | --- | --- | --- | --- | --- |
| default | +6% | +15% | +24% | +15% | +20% |
| A14 kernels | +3% | +13% | +24% | +6% | +21% |
| A14, 4-qubit stages, `complex32` | +15% | +23% | +32% | +30% | +27% |

A first prototype that added every warp's sum atomically to one of 256 shared addresses was 2.2 to 4.1 times slower; the contention, not the arithmetic, dominated it. With the realistic version, about a fifth more time per pass, the net speedup of first-jump sampling is about the pass ratio of the table above divided by 1.2: no gain at $M = 0.1$ (0.9 to 1.1), 1.1 to 2.5 times at $M = 1$, and 1.5 to 3.9 times at $M = 3$ without the ceiling. The reductions can be skipped for checkpoints whose shots cannot err in the block (a pass with no noisy gate, or a proposal with no error under noisecirc's current scheme), which would remove the loss at weak noise.

### Readout map: exact, 1.5 times for GHZ, a few percent otherwise (verified, dry run)

At the end of a circuit, after the last non-diagonal gate on a group of qubits, only diagonal gates follow, whose phases can no longer reach a measurement. On this tail the Z-basis populations evolve classically, and amplitude damping acts on them as the map "1 becomes 0 with probability $\gamma$" whatever the coherences. A channel whose later operations on its qubit all lie in the tail can therefore be removed from the simulation and applied to the sampled bits. The condition is transitive: a channel followed by a controlled phase whose partner later meets a rotation cannot be removed, because the phase then depends on whether the qubit decayed. On 6 qubits the transformed simulation reproduces the density-matrix distribution to $10^{-15}$, while the naive condition (only later gates on the qubit itself diagonal) is off by 0.19 for GHZ.

In the dry run at 28 qubits, the readout map removes 28 of GHZ's 109 channels and makes 1.46 to 1.61 times fewer passes; for brickwork, QFT, QAOA and the grid it removes 3 to 7% of the channels and changes the passes by −3 to +8%, within the dry run's scatter. It costs nothing at run time and is simple to implement (compile-time pass plus a classical map on the samples), but it pays only for circuits that end in long diagonal stretches.

### Peeling the last block: about 1/B (dry-run estimate)

The qubits outside the last block's tile cannot be changed by it, so their outcome can be sampled from the marginal of the checkpoint that enters the last block, and the last block simulated only on the $2^{12}$ amplitudes consistent with that outcome. This removes the last block's passes at the price of one read of each entering state. From the dry run's passes per block, the saving is 1.49 to 1.57 times for GHZ (3 blocks) and 1.03 to 1.08 times for the other circuits (9 to 30 blocks). Not implemented.

### Kernel ideas

The brainstorm on the execution of a pass confirmed the instruction-bound picture of task A13 and proposed real rotations with deferred diagonals (implemented in A14), wider stages once the arithmetic is cheap (measured in A13), and `complex32` only after both (measured in A13: 1.45 to 1.9 times end to end). Not tried: applying diagonal gates outside the stages that hold their qubits, from the bits of the amplitude index (estimated to cut a third to a half of the shared accesses), asynchronous double-buffered tile loads to lower the memory floor of Eq. (1) of the precision study (estimated 8 to 13%), and loading the first stage's registers straight from global memory (about 5%).

## Caveats

- The first-jump and readout passes come from a reference implementation on 6 to 10 qubits (real states) and from dry runs at 28 qubits (surrogate states); first-jump sampling is not implemented in noisecirc.
- The kernel cost of first-jump sampling was measured with a timing prototype that reduces the populations of every stage's register qubits, a proxy for the per-channel sums; the second pass of each segment (the error groups after the dominant pass) adds a synchronisation that the prototype does not include.
- The brainstorm's estimates of untested ideas are estimates, not measurements.

## Verdict

Nothing found removes the floor of the pass model, the propagation of every distinct trajectory through the rest of the circuit; what can be gained lies around it. The most promising idea is first-jump sampling: it is exact (verified on small registers), it removes all rejected proposals and the oversampling ceiling, and it makes 1.04 to 3.3 times fewer passes at up to one expected error per shot and 1.7 to 4.7 times fewer at three; its reductions cost about a fifth of a pass, so it pays from about one error per shot and most at strong noise, which is where noisecirc's advantage over Qiskit Aer was smallest ([noisecirc against Qiskit Aer and CUDA-Q](competitors.md)). It changes noisecirc's core loop (a dominant pass before the error passes of each segment) and its kernels; its implementation is the natural next task. The second largest gain, 1.45 to 1.9 times on the whole run, comes from issuing fewer instructions per pass and then storing `complex32` ([Precision, block size and the instruction-bound pass](kernel-regime.md)). The readout map and peeling the last block are exact and cheap but pay only for circuits with few blocks or long diagonal tails, such as GHZ (about 1.5 times each).
