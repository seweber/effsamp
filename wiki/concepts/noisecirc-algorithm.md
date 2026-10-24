---
title: NoiseCirc's sampling algorithm
summary: How noisecirc samples trajectories of non-mixed-unitary Kraus channels, and what its work is counted in
type: concept
tasks: [A1]
updated: 2026-10-23
---
# NoiseCirc's sampling algorithm

## Description

NoiseCirc samples measurement outcomes of a noisy circuit by quantum trajectories: each shot follows one state vector, and every noisy gate applies one of its Kraus operators, chosen at random. This page describes how NoiseCirc chooses the Kraus operators without looking at the state, why the result is still exact, and how the work it does can be counted in passes over the state vector. It reflects the code of `code/noisecirc` at commit `1808d30` (main), restricted to what PLAN.md asks for: qubits, `complex64`, and the `"exact"` sampling mode.

The page builds up in four steps:

1. how one gate's Kraus operator is chosen (rejection sampling),
2. how many shots are sampled together (distinct trajectories),
3. how the circuit is cut into segments with checkpoints (segmented sampling),
4. how gates are fused into blocks, the unit of work on the GPU.

The [Block-pass cost model](block-pass-cost-model.md) then turns the number of block passes into a runtime.

### Choosing a Kraus operator by rejection

A noisy gate is a channel with Kraus operators $K_1, \dots, K_r$, so that a trajectory in state $|\psi\rangle$ takes operator $i$ with probability $p_i = \lVert K_i \psi \rVert^2$. The standard trajectory method computes these probabilities, which costs a pass over the state vector for each operator, before it applies the chosen one.

NoiseCirc instead draws the operator from a distribution that does not depend on the state. Each operator gets a state-independent upper bound $b_i$, the largest eigenvalue of $K_i^\dagger K_i$, so that $p_i \le b_i$ for every state. The bounds sum to the oversampling factor of the gate:

$$Z = \sum_i b_i \ge 1. \tag{1}$$

The proposal picks operator $i$ with probability $b_i / Z$ and applies the rescaled operator $K_i / \sqrt{b_i}$. The squared norm of the result, $p_i / b_i \le 1$, is the probability of accepting the proposal. A proposal is therefore accepted with overall probability $\sum_i (b_i/Z)(p_i/b_i) = 1/Z$ for a trace-preserving channel, whatever the state, and an accepted operator is distributed exactly as $p_i$.

Two cases matter for this project:

- For a **mixed-unitary channel** (each $K_i$ proportional to a unitary, e.g. depolarizing noise), $b_i = p_i$, so $Z = 1$ and no proposal is ever rejected. Noise then only selects which unitary to apply.
- For a **non-mixed-unitary channel** such as amplitude damping with strength $\gamma$, $K_0 = \mathrm{diag}(1, \sqrt{1-\gamma})$ and $K_1 = \sqrt{\gamma}\,|0\rangle\langle 1|$ have bounds $1$ and $\gamma$, so $Z = 1 + \gamma$. Proposals are rejected, at a rate set by $\gamma$, and this is the regime the publication focuses on.

Along a trajectory, the factors multiply: a whole trajectory through the circuit is accepted with probability $1/Z^\ast$ on average, where $Z^\ast$ is the product of all gates' factors. In NoiseCirc the factor of a gate may depend on the input sector (only relevant for leakage; with qubits there is a single sector), so $Z^\ast$ is the product of each gate's largest factor, and a path with a smaller product is first thinned classically by $Z(\text{path})/Z^\ast$ before its state is propagated (`sampling/sample.py`).

### Sampling distinct trajectories instead of shots

Because proposals do not depend on the state, all shots can be proposed before any state is computed. NoiseCirc proposes them in groups (`sampling/propose_unique_trajectories.py`): at every gate, the shots of a group are split over the Kraus operators by a multinomial draw, and every operator that receives shots starts a new group. The result is one entry per distinct trajectory with the number of shots that proposed it.

Each distinct trajectory is propagated once, and its shots are then accepted together by one binomial draw with its squared norm. At weak noise almost all shots propose the noise-free trajectory, which is then simulated once for all of them.

### Segmented sampling with checkpoints

Proposing whole trajectories wastes work: a proposal rejected at the end of the circuit was propagated through all of it, and trajectories that share their first gates propagate that prefix separately. NoiseCirc therefore cuts the circuit into segments, fixed before anything is drawn (`blocks_per_segment`, by default one fused block per segment).

The sampler expands the tree of trajectories one segment at a time (`sampling/sample.py`):

1. From each accepted prefix, a *checkpoint* holding the state at the segment boundary, it proposes paths through the next segment for the shots the checkpoint carries.
2. It propagates every distinct (checkpoint, path) pair once, starting from the checkpoint's state.
3. It accepts each pair by the squared norm over the segment, so that a rejected proposal costs only one segment.
4. In exact mode, it re-proposes the rejected shots from the same checkpoint until all shots of the checkpoint are accepted.

The result is exact for any fixed segmentation, because the acceptance probabilities of the segments multiply to that of the whole trajectory. The tree is traversed depth-first: at most one batch of states per segment is held along the current path, so memory grows with the depth of the circuit, not with the number of shots. In exact mode, the squared norms of trajectories propagated in earlier refill rounds are cached, so that a recurring proposal is not propagated again unless it is accepted and its earlier copy is no longer held.

### Gate fusion into blocks

All propagation happens in blocks: groups of consecutive gates on at most `max_fused_qudits = 9` qubits, besides 3 pinned lowest qubits, and at most `max_operations = 128` gates (`block/fusion.py`). A generated CUDA kernel applies a whole block in one pass over the state vector: it loads a tile of amplitudes into shared memory, applies the gates stage by stage from registers, and writes the tile back (`packages/svpass`).

Fusion interacts with the sampling in two ways:

- **A block is the smallest segment.** A proposal rejected in a block wastes the whole block's pass, so fusion stops adding noisy gates once a block's oversampling factor would exceed `max_oversampling = e`. If every proposal is distinct, cutting a circuit of total log factor $L$ into blocks of factor $c$ costs about $(L / \ln c)\, c$ passes per shot, which is smallest at $c = e$ (`docs/design.md`).
- **Each block has two kernels.** The dominant kernel applies every gate's most likely Kraus operator (no error) and reads no choices; the general kernel switches on each gate's choice. Trajectories without an error in the block take the cheaper dominant kernel.

### The unit of work: block passes

Every kernel launch reads and writes each of its state vectors once, and NoiseCirc counts these as `block_passes` in its diagnostics: the number of rows (trajectories) times the blocks they were propagated through. Checkpoints, normalizations, norms and the probabilities for measurement are computed during these passes and cost no pass of their own. If a pass costs the time to read and write one state vector, the runtime is approximately the block passes times that time; how well this holds is the subject of task A2, see [Block-pass cost model](block-pass-cost-model.md).

### Where the gains over standard trajectory sampling come from

To separate algorithmic from implementation gains (PLAN.md goal), NoiseCirc's ingredients split into two groups. The first group changes how many passes a simulation needs:

- proposing without the state (no passes to compute Kraus probabilities),
- propagating each distinct trajectory once (no repeated work for shots that agree),
- sharing prefixes through checkpoints (no repeated work for shots that agree up to a point, and rejection after one segment instead of the whole circuit),
- fusing up to 9 + 3 qubits and 128 gates per block, including noisy gates (fewer passes per trajectory).

The second group changes how long a pass takes:

- generated kernels specialised on the numerical matrix entries,
- the dominant kernel that skips the choice logic,
- batching many trajectories into one launch, which shares the host's work.

How much each ingredient gains against Qiskit Aer and CUDA-Q is measured in [noisecirc against Qiskit Aer and CUDA-Q](../studies/competitors.md): the first group accounts for nearly all of noisecirc's advantage, while at equal algorithm the implementations are within a factor of 2.

## Prior art

The literature check is in [Prior art of noisecirc's algorithm](../studies/prior-art.md). In short:

- The state-independent operator-norm proposals with acceptance by the norm, which make pre-sampled and grouped trajectories exact for non-mixed-unitary channels, were not found in the literature; the closest is qsim's delayed algorithm with lower bounds ([isakov2021qsim](../literature/notes/isakov2021qsim.md)).
- Pre-sampling and deduplicating trajectories exists for mixed-unitary noise ([patti2025ptsbe](../literature/notes/patti2025ptsbe.md)).
- Depth-first, memory-bounded reuse of trajectory prefixes exists for Pauli noise ([li2019sanq](../literature/notes/li2019sanq.md), [dangwal2026tusq](../literature/notes/dangwal2026tusq.md)); its combination with rejection and refills was not found.
- Wide shared-memory fusion kernels exist without noise ([xu2024atlas](../literature/notes/xu2024atlas.md), HyQuas); the no-error kernel and the ceiling-limited fusion were not found.
