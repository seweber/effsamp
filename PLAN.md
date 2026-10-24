---
# Human-owned, read-only project plan. Agents must read but never edit it.
# To edit as the human researcher: chmod +w PLAN.md; restore mode 0444 after.
# title: full title used in the wiki, reports, and human-facing summaries.
# label: ASCII project slug for sessions and remote storage; only letters,
# numbers, dots, underscores, and hyphens.
# mattermost_channel_url: optional supervisor channel used by configured tools.
title: "Benchmarking noisecirc"
label: "bench"
mattermost_channel_url: ""
---

# Research Plan

## Overview

<!-- Scientific context, scope, constraints, and concrete success criteria. -->

I have written the library noisecirc for simulating noisy quantum circuits, see code/noisecirc. It is based on a new idea of using rejection sampling. Also the depth first memory optimal reuse of trajectory prefixes is maybe new in this form, but there I am not sure. Also the code for applying blocks of gates might to state vectors might contain something that is new, but there I am not sure, too.

I want to make a publication that focuses on the algorithmic improvement of sampling for gates represented as non-mixed unitary Kraus channels. To my knowledge the closest competitor is here the state branching sampling of Qiskit Aer, but maybe I am overlooking other libraries.

**Important:**
* If something blocks you, leave a note in the wiki and continue with other tasks.
* I am not interested in the "average" sampling mode of noisecirc, but only the "exact" one.
* I am not interested in qutrits and subspace twirling, use qubits only.
* I am not interested in any other data types than complex64 (single precision).
* I am not interested in any CPU-based circuit simulation or tensor network methods, but only in GPU-based state vector simulators.
* Ignore noisecirc's AGENTS.md as it is out of date.
* Do not implement competing algorithms in noisecirc, but investigate and maybe annotate other libraries if you are interested in the algorithms they use. However, you are allowed to use noisecirc with different parameters to isolate effects. And you are encouraged to improve upon noisecirc itself, and also improve its algorithm - however, the core idea of noisecirc should remain intact.
* You are allowed to make your own branches of the noisecirc code. Do not commit directly to the main branch. Note that you cannot push but must keep the branches locally.
* If you find any bugs or issues in noisecirc, report them immediately in the wiki and fix them. Provide also a dedicated branch (starting with fix/) that only contains the bug fix so that I can easily review it. Note that any problems with noisecirc must not stop you, but after you fixed them, you must continue.
* You are only allowed to use the gpu 0 on the host bux - it is forbidden to use any other GPU. I, my user name is "sebastian", have blocked gpu 0 for you, using a slurm process that is attached to it infinitely and prevents any other slurm jobs from accessing it. You must use the gpu 0 directly, without going through slurm.
* It is crucial that you run any code with a timeout of at most 10 minutes to avoid getting stuck; for image builds etc. you can use a longer timeout if necessary. If you have longer-running experiments, you must break them down into smaller parts that each complete within the timeout. But avoid excessive numerical work wherever possible.
* You have a lot of time to work on the tasks, so focus on careful analysis and understanding rather than rushing through experiments. Continuously update the wiki. 

**Where this plan conflicts with CONTRACT.md or SECDEV.md, this plan takes precedence. For example:** 
* Do not return to me after every step but do them all before finishing.
* Follow strictly my instructions on the GPU usage, do not use slurm or any other GPU!
* Use a GPU-enabled podman image on bux so that you can install things freely.
* If you cannot access a publication from a site, try to get it from a different source. If it is not working out, do not use the publication and leave me a note in the wiki. But do not stop your work because of it, but continue without that publication.
* You are also allowed to cite papers that are arXiv preprints and do not have a doi of a journal.

## Goal

<!-- The central scientific question this project answers. One paragraph. -->

I want to understand exactly how large performance improvements of noisecirc are against state of the art, and where the performance improvements come from. In particular, I want to separate performance gains due to the new algorithmic ideas from those due to implementation.

## Tasks

<!-- Human-approved research tasks: initial directions plus proposals
     accepted from TASKS.md. Give each a human-assigned ID distinct from
     proposal IDs (e.g. A1, A2, ...). Progress, outcomes, and technical
     micro-steps belong in LOG.md. -->

### A1

Understand how the algorithm implemented in noisecirc is working. Perform a systematic prior art check.

### A2

For larger workloads, the duration of a simulation with noisecirc can be understood by the number of `blocks`: If the blocksize is reasonable and the number of operations in it as well, the application of a block is bandwidth bound and the duration is in good approximation the time it takes to read and write a state vector. For sufficiently large workloads, this time dominates the overall simulation time that can then be approximated by the number of blocks multiplied by the time per block.

Figure out how good this approximation is. I want to operate in a regime where this connection is reasonable because then you can reason about the performance of noisecirc analytically. Note that it is fine with me, if it is a rough approximation. But it should be not off by more than a factor of 1.5, I guess. If this is not reasonable because it would require simulations that take very long, you can also relax this requirement and work with a coarser approximation.

### A3

Figure out how the parameters of noisecirc affect the number of blocks. Note that you must not choose parameters where the assumption that the application time of a block is given by the bandwith is completely off. But stretching this approximation a bit is fine. I want to be able to understand and predict the dominating behavior.

### A4

Using this findings, we now want to benchmark noisecirc by looking at estimated numbers of blocks that must be applied; circuits must not yet be run.

Figure out what good quantum circuits are for benchmarking. I expect that the circuits should in particular behave differently under gate fusion and also have different types of non-mixed unitary noise and the strength of this noise (for completeness you can also consider an ideal circuit and mixed-unitary noise, but there should not be the focus on). Think about how to partition the circuits into different categories. Establish representative circuits. Figure out how changes between these categories affect the performance of noisecirc, for example strength of the noise or the degree of gate fusion possible.

### A5

After the analysis of the estimated number of blocks, run now the most interesting circuits to validate the predictions. From the runs, you get the actual runtimes and also the exact number of blocks applied.

### A6

Find other libraries to benchmark against noisecirc. If possible, translate the work of the libraries also in applicaton of blocks so that we can get an analytic understanding of the algorithmic performance of the libraries independent on the implementation (for example, for the branching simulator of qiskit Aer, I expect that much more blocks must be applied because in there implementation gate fusion is only helpful up to about k=2 and they also have Kraus operators to apply to get the norm, just to figure out that the result is discarded).

### A7

Tune parameters of noisecirc, for example i) the number of fused gates per block, ii) the number of fused blocks per stage, iii) the pinned qubits per block, iv) values in tunables.py. Figure out which improvements can be achieved by optimizing these parameters.

### A8 — Noise-aware block sizes and cheaper error kernels in noisecirc

- **Proposed:** 2026-10-24 by Claude
- **Purpose:** On the H100, the passes of trajectories with an error in a block use the general kernel, which costs 1.3 to 4.5 times the bandwidth time (growing with the gates per block and the Kraus operators per gate), and these passes are 20 to 60% of all passes at one expected error per shot. Blocks of at most 32 instead of 128 gates were 6 to 17% faster at damping $10^{-2}$ but up to 25% slower at $10^{-3}$ (LOG.md "A2 max_operations at n=26 and A2 conclusion"; wiki/studies/block-pass-time.md). The best block size thus depends on the noise, which noisecirc's fixed defaults ignore.
- **Proposal:** Model the run time as dominant plus general passes times their kernel costs (both predictable, wiki/studies/validation.md), choose the block size per circuit from it, and test whether a kernel specialized to trajectories with a single error in a block (the common case at low noise) closes the gap between general and dominant kernels. Expected gain 10 to 30% at loads near one error per shot; cost a few days; risk: compile time of more kernel variants.
- **Discussion:**
  - 2026-10-24 AI: Proposed from the A2 and A5 results; it improves the implementation and the fusion policy, not the core algorithm.

### A9 — Comparison with delayed lower-bound sampling (cuStateVec Ex)

- **Proposed:** 2026-10-24 by Claude
- **Purpose:** The closest prior art to noisecirc's state-independent proposals is qsim's delayed inner-product algorithm, which cuStateVec Ex's state-vector updater implements on GPUs (wiki/studies/prior-art.md). It skips the norm passes for the no-error operator of amplitude damping with probability $1 - \gamma$ but simulates one trajectory per shot. CUDA-Q, measured in A6, may or may not use it; its time was independent of the noise strength (wiki/studies/competitors.md). A direct comparison would isolate the value of noisecirc's upper-bound proposals with rejection, which allow sharing trajectories, against lower-bound proposals, which do not.
- **Proposal:** Run cuStateVec Ex's updater (through CuPy or its Python bindings) on the A6 circuits, count its passes, and compare with noisecirc's per-shot variant and default. Expected outcome: the per-shot ceiling of lower-bound sampling, and how much of noisecirc's gain is the sharing that only upper bounds permit. Cost: one to two days; risk: API availability in the installed cuQuantum version.
- **Discussion:**
  - 2026-10-24 AI: Proposed from the literature check (A1) and the A6 caveat that CUDA-Q's algorithm was not modelled.

### A10 — Fewer rejected proposals at strong noise

- **Proposed:** 2026-10-24 by Claude
- **Purpose:** At strong noise, noisecirc's work is dominated by error proposals: about $2MN$ passes for amplitude damping, of which half are rejected, which no fusion reduces (wiki/studies/pass-count.md, wiki/studies/benchmark-suite.md); against Aer's shot branching the speedup falls from about 30 times at $M = 0.1$ to 6 to 20 times at $M = 1$ (wiki/studies/competitors.md). The proposal bounds are state-independent operator norms; tighter bounds that are still valid for all states of a checkpoint's subtree would cut the rejections.
- **Proposal:** Study proposal bounds that use information available at a checkpoint without extra passes (e.g. the chunk sums of the last pass, which bound the populations of the pinned qubits), prove their validity for exact sampling, and measure the reduction of passes at $M \ge 1$ with the dry run before any GPU implementation. Expected outcome: a bound on how much of the $2MN$ term is avoidable; risk: tighter bounds may need state information whose cost exceeds the saving.
- **Discussion:**
  - 2026-10-24 AI: Proposed from the A3 and A6 results; it concerns noisecirc's core algorithm and needs the human's view on whether it is in scope.

### A11

Also optimize parameters of the shot branching simulator of Qiskit Aer, for example the number of fused gates. I think this is necessary to make the comparison fair, if we optimize the parameters of noisecirc.

### A12

I wonder how to optimize the Kraus representation for noisecirc. Probably, it benefits if one uses the freedom that one has to make the first operator the most "dominant" one (I am not sure how to quantify this dominance yet), than from the remaining operators the second operator the most dominant one, etc. On the other hand, also oversampling should be kept small. Think about it. Play around with different ideas. My feeling is that one can find a way to opimize the Kraus operators that is provably close to optimal or even perfectly optimal for noisecirc's efficiency.

### A13

I wonder how gate fusion and the application of the block could be optimized further. I am not interested in getting tiny improvements, but I am thinking about changes that could make noisecirc substantially more efficient. One direction that I have in mind is to look at the complex32 data type and increase the size of the block as large as possible. I think in this scenario one easily runs into situations where the applictaion of the block is compute bound. I wonder how the optimal kernel should be designed in this regime. In particular i wonder whether there are changes that do not make the kernel more complicated but still improve the efficiency clearly. Maybe there are also better strategies than implemented currently in the kernel.

### A14

Building upon A14, I want to investigate the compute efficiency of the kernels fundamentally. I think there should be optimal ways to apply one block with as few flops as possible. For this, you probably must make perfect use of the sparse structure / diagonality / controlled qubits / etc. of the block. An additional direction to think about is to optimize the contraction order within a block instead of sequentially applying the gates to the state vector.

### A15

I wonder whether there is something that we were overlooking up to now and that would fundamentally improve noisecirc's efficiency. Note that I want to stay in the statevector world, so tensor network approaches, Clifford approaches, etc. are out of scope. To get ideas, brainstorm with subagents. Try out the most promising suggestions.

### References

<!-- Pointers to seed literature, prior internal work, related codebases.
     Papers and their notes live in wiki/literature/. -->