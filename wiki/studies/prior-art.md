---
title: Prior art of noisecirc's algorithm
summary: "Systematic literature check: which of noisecirc's sampling and fusion ideas are anticipated"
type: study
tasks: [A1]
status: partially verified
updated: 2026-10-23
---
# Prior art of noisecirc's algorithm

## Question

Which of noisecirc's ideas are anticipated in the literature (PLAN.md task A1)? The ideas checked are the three groups described in [NoiseCirc's sampling algorithm](../concepts/noisecirc-algorithm.md):

1. proposing Kraus operators from state-independent operator-norm bounds and accepting them by the propagated norm, with all shots proposed up front and grouped into distinct trajectories;
2. segmented sampling: depth-first traversal of the trajectory tree with checkpoints, rejection at segment ends, and refills from the checkpoint;
3. fusion of many gates into wide shared-memory blocks, with a no-error (dominant) kernel and a fusion limit set by the oversampling ceiling.

## Approach

A literature search (2026-10-23) covered GPU trajectory simulators (Qiskit Aer, qsim/Cirq, CUDA-Q, cuStateVec), tree-based reuse of trajectories, unravelings with state-independent probabilities, and GPU gate fusion. Every paper below was checked against its source, its DOI resolved, and its PDF stored; its note in `wiki/literature/notes/` summarizes it. Library documentation was read for Aer, CUDA-Q and cuStateVec, and Aer's source for how it applies a Kraus channel to a branch (`apply_kraus` in `src/simulators/statevector/statevector_executor.hpp`).

## Runs

No runs: a literature and source check.

## Results

### Idea 1: state-independent proposals accepted by the norm (partially verified as new)

The general principle is old, but its use for exact batched sampling of non-unitary channels was not found:

- Choosing a measurement outcome with a state-independent "ostensible" probability, applying the scaled operator and carrying the squared norm as a weight is a standard unraveling ([Wiseman 1996](../literature/notes/wiseman1996.md)). Granet et al. normalise Kraus operators by their operator norm in the same way, but use the norms as importance weights ([granet2025analog](../literature/notes/granet2025analog.md)).
- qsim's delayed inner-product algorithm is the closest sampling prior art ([isakov2021qsim](../literature/notes/isakov2021qsim.md)), also used by cuStateVec Ex: it chooses a Kraus operator without the state with the probability of state-independent **lower** bounds, and computes exact norms for the remainder. For amplitude damping of strength γ, the exact fallback still happens with probability about γ per channel; noisecirc uses **upper** bounds and rejection instead, and never computes a probability pass.
- Pre-sampling the noise of all shots before simulation, deduplicating the trajectories and simulating each distinct one once is prior art for mixed-unitary noise: PTSBE in CUDA-Q ([patti2025ptsbe](../literature/notes/patti2025ptsbe.md)), TUSQ ([dangwal2026tusq](../literature/notes/dangwal2026tusq.md)), SANQ ([li2019sanq](../literature/notes/li2019sanq.md)).
- Qiskit Aer, CUDA-Q and cuStateVec Ex all compute state-dependent probabilities for general channels ([doi2023shots](../literature/notes/doi2023shots.md), library documentation).

No source was found that chooses the proposal probabilities proportional to the operator norms so that every weight is at most one and becomes an acceptance probability, and thereby makes pre-sampled, grouped trajectories exact for non-mixed-unitary channels. The same holds for the multinomial splitting of shot counts with the classical thinning by $Z(\text{path})/Z^\ast$.

### Idea 2: depth-first trajectory tree with checkpoints (base idea anticipated, verified; extensions partially verified as new)

The base idea is published:

- SANQ (also DAC 2020) generates Pauli error traces up front, orders them by their first error and executes them recursively, storing as many states as the recursion is deep ([li2019sanq](../literature/notes/li2019sanq.md)).
- TUSQ traverses the tree of pre-sampled error realizations depth-first on GPUs, backtracking by uncomputation, with a checkpoint cache for non-invertible steps ([dangwal2026tusq](../literature/notes/dangwal2026tusq.md)).

Related but different:

- TQSim reuses random, not identical, prefixes and is approximate ([wang2025tqsim](../literature/notes/wang2025tqsim.md)).
- Trajectree caches branch probabilities and states on CPUs with matrix-product states ([singal2026trajectree](../literature/notes/singal2026trajectree.md)).
- Aer's shot branching shares prefixes breadth-first, keeps all branches in memory, and restarts waiting shots from the beginning when memory runs out; its authors state that they do not record states for a recursive execution ([doi2023shots](../literature/notes/doi2023shots.md)).

Not found in any of them, and specific to noisecirc: rejection of proposals at segment ends, refilling rejected shots from the same checkpoint in exact mode, a bound of one batch of states per segment, and exactness for non-unitary Kraus channels. A publication should therefore not claim depth-first, memory-bounded prefix reuse as new, but it can claim its combination with rejection sampling.

### Idea 3: wide fused shared-memory blocks (partially verified as new)

The kernel structure has prior art:

- HyQuas applies gate groups of 10 qubits in shared memory, with up to 600 gates per group (from its source code; the paper itself was not accessible).
- Atlas uses shared-memory kernels that always include the three lowest qubits ([xu2024atlas](../literature/notes/xu2024atlas.md)), as noisecirc pins three qubits.
- Dense fusion stays at 4 to 5 qubits in qsim, Aer and cuStateVec, because a dense matrix beyond about 5 qubits is no longer memory-bound on the H100 ([bayraktar2023cuquantum](../literature/notes/bayraktar2023cuquantum.md)).

Not found: kernels specialised for the no-error path of noisy blocks, and a fusion limit set by the oversampling ceiling. One lead remains open: CUDA-Q tracks up to 16 "branches" of trajectories in its gate fusion (`CUDAQ_BATCHED_SIM_MAX_BRANCHES`), which should be checked when CUDA-Q is benchmarked (task A6).

### Further related work

Three more papers were read and found not to bear on the three ideas:

- stochastic simulation with decision diagrams, which samples every Kraus operator from the state ([grurl2021stoch](../literature/notes/grurl2021stoch.md));
- variance-reduced unravelings on GPUs, which report that Qiskit Aer rewrites Kraus channels before applying them ([you2026varred](../literature/notes/you2026varred.md));
- the subspace twirling of leakage that noisecirc implements for qutrits, outside this project's qubit scope ([marshall2025leakage](../literature/notes/marshall2025leakage.md)).

## Caveats

- A literature search can show prior art but cannot prove its absence: "not found" means not in the sources searched (arXiv, publisher pages, library documentation, Aer's source) on 2026-10-23.
- Not accessible: the HyQuas paper (ICS'21, paywalled; its code was read), the DAC 2020 version of SANQ (its arXiv version was read), Q-GPU (HPCA 2022) and SV-Sim (SC21), of which only the metadata was seen.

## Verdict

The algorithmic core of noisecirc, exact rejection sampling of non-mixed-unitary Kraus channels with state-independent operator-norm proposals that permits pre-sampling and grouping of shots, appears new (partially verified). The depth-first, memory-bounded reuse of trajectory prefixes is not new by itself (SANQ, TUSQ for Pauli noise), but its combination with rejection and refills is. The wide shared-memory kernels have close prior art (HyQuas, Atlas); their noise-aware parts appear new.
