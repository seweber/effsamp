# Task Proposals

Proposal board for new high-level scientific tasks. The agent proposes; the
human and the agent discuss in the entry's `Discussion` list. Accepted
proposals are copied into `PLAN.md` by the human under a new task ID and then
closed here with a pointer to that task.

Only `PLAN.md` defines the tasks that are worked on. Progress and outcomes of
approved tasks belong in `LOG.md` and `wiki/`, never here. Proposals are never
deleted; IDs (T001, T002, ...) are stable, never reused, and independent of
`PLAN.md` task IDs.

---

## T001 — Noise-aware block sizes and cheaper error kernels in noisecirc
- **State:** CLOSED
- **Proposed:** 2026-10-24 by Claude
- **Purpose:** On the H100, the passes of trajectories with an error in a block use the general kernel, which costs 1.3 to 4.5 times the bandwidth time (growing with the gates per block and the Kraus operators per gate), and these passes are 20 to 60% of all passes at one expected error per shot. Blocks of at most 32 instead of 128 gates were 6 to 17% faster at damping $10^{-2}$ but up to 25% slower at $10^{-3}$ (LOG.md "A2 max_operations at n=26 and A2 conclusion"; wiki/studies/block-pass-time.md). The best block size thus depends on the noise, which noisecirc's fixed defaults ignore.
- **Proposal:** Model the run time as dominant plus general passes times their kernel costs (both predictable, wiki/studies/validation.md), choose the block size per circuit from it, and test whether a kernel specialized to trajectories with a single error in a block (the common case at low noise) closes the gap between general and dominant kernels. Expected gain 10 to 30% at loads near one error per shot; cost a few days; risk: compile time of more kernel variants.
- **Discussion:**
  - 2026-10-24 AI: Proposed from the A2 and A5 results; it improves the implementation and the fusion policy, not the core algorithm.
- **Outcome:** accepted into PLAN.md as A8 (2026-10-24)

## T002 — Comparison with delayed lower-bound sampling (cuStateVec Ex)
- **State:** CLOSED
- **Proposed:** 2026-10-24 by Claude
- **Purpose:** The closest prior art to noisecirc's state-independent proposals is qsim's delayed inner-product algorithm, which cuStateVec Ex's state-vector updater implements on GPUs (wiki/studies/prior-art.md). It skips the norm passes for the no-error operator of amplitude damping with probability $1 - \gamma$ but simulates one trajectory per shot. CUDA-Q, measured in A6, may or may not use it; its time was independent of the noise strength (wiki/studies/competitors.md). A direct comparison would isolate the value of noisecirc's upper-bound proposals with rejection, which allow sharing trajectories, against lower-bound proposals, which do not.
- **Proposal:** Run cuStateVec Ex's updater (through CuPy or its Python bindings) on the A6 circuits, count its passes, and compare with noisecirc's per-shot variant and default. Expected outcome: the per-shot ceiling of lower-bound sampling, and how much of noisecirc's gain is the sharing that only upper bounds permit. Cost: one to two days; risk: API availability in the installed cuQuantum version.
- **Discussion:**
  - 2026-10-24 AI: Proposed from the literature check (A1) and the A6 caveat that CUDA-Q's algorithm was not modelled.
- **Outcome:** accepted into PLAN.md as A9 (2026-10-24)

## T003 — Fewer rejected proposals at strong noise
- **State:** CLOSED
- **Proposed:** 2026-10-24 by Claude
- **Purpose:** At strong noise, noisecirc's work is dominated by error proposals: about $2MN$ passes for amplitude damping, of which half are rejected, which no fusion reduces (wiki/studies/pass-count.md, wiki/studies/benchmark-suite.md); against Aer's shot branching the speedup falls from about 30 times at $M = 0.1$ to 6 to 20 times at $M = 1$ (wiki/studies/competitors.md). The proposal bounds are state-independent operator norms; tighter bounds that are still valid for all states of a checkpoint's subtree would cut the rejections.
- **Proposal:** Study proposal bounds that use information available at a checkpoint without extra passes (e.g. the chunk sums of the last pass, which bound the populations of the pinned qubits), prove their validity for exact sampling, and measure the reduction of passes at $M \ge 1$ with the dry run before any GPU implementation. Expected outcome: a bound on how much of the $2MN$ term is avoidable; risk: tighter bounds may need state information whose cost exceeds the saving.
- **Discussion:**
  - 2026-10-24 AI: Proposed from the A3 and A6 results; it concerns noisecirc's core algorithm and needs the human's view on whether it is in scope.
- **Outcome:** accepted into PLAN.md as A10 (2026-10-24)

## T004 — Device dependence of noisecirc's cost model and settings
- **State:** OPEN
- **Proposed:** 2026-10-24 by Claude
- **Purpose:** Every conclusion about pass times and best settings so far rests on one GPU, the H100, which has 2.9 times fewer floating-point operations per byte of bandwidth than the RTX 4060 Ti noisecirc was tuned on (PROBLEMS.md P001). On the H100, large blocks and error kernels are not bound by the bandwidth (wiki/studies/block-pass-time.md), masked kernels gained 4 to 13% and autotuning 0 to 14% (wiki/studies/error-kernels.md). The pass counts are device-independent (wiki/studies/pass-count.md), but how passes translate into time, and so which settings and improvements pay, may not be.
- **Proposal:** Repeat the kernel-ratio measurements and the end-to-end comparison of masked kernels and autotuning on a second GPU with a different arithmetic-to-bandwidth ratio (e.g. the RTX 4060 Ti or an A100), with the existing tools (code/bench/a7_blocks.py, a2_runs.py). Expected outcome: whether the cost model needs device-specific kernel ratios only, or different defaults per device. Cost: about a day of GPU time; risk: access to a second GPU with the same software stack.
- **Discussion:**
  - 2026-10-24 AI: Proposed from A2, A7 and A8; it needs hardware outside GPU 0 of bux, so the human decides.
- **Outcome:** pending

<!-- Add proposals above this line, oldest first. Template:

## T00X — Short scientific task title
- **State:** OPEN | CLOSED
- **Proposed:** YYYY-MM-DD by <agent>
- **Purpose:** the scientific question, why it matters for the PLAN.md goal,
  and the evidence (LOG.md entries, data, literature) that prompted it
- **Proposal:** rough approach, expected outcome, acceptance criteria, cost
  and risk
- **Discussion:**
  - YYYY-MM-DD AI: ...
  - YYYY-MM-DD Human: ...
- **Outcome:** pending while OPEN; on closure one of
  - accepted into PLAN.md as <PLAN.md task ID> (YYYY-MM-DD)
  - rejected: <reason>
  - withdrawn: <reason>
  - superseded by T00Y

-->
