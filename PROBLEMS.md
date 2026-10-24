# Conceptual And Structural Problems

Shared concise record of conceptual or structural problems discovered during
the research. Its purpose is to keep humans and new agents from repeating
known traps. Technical problems such as package limitations, command failures,
or implementation details belong in `LOG.md`.

Keep entries under `OPEN` until resolved. Move resolved entries to `CLOSED`;
never delete them.

## OPEN

<!-- Add open entries above this line. Use stable, unique IDs. Template:

### P001 — Short problem title
- **Problem:** concise description of the conceptual or structural issue
- **Impact:** how it can invalidate, misdirect, or limit the research
- **Resolution:** open; the promising resolution direction, if known

-->

## CLOSED

### P001 — The bandwidth model of a block pass depends on the device
- **Problem:** PLAN.md task A2 assumes that a block pass costs the time to read and write one state vector. noisecirc's block size (up to 128 gates) was tuned on an RTX 4060 Ti; on the H100, with 2.9 times fewer floating-point operations per byte of bandwidth, large blocks and the general (error) kernels are bound by arithmetic and shared memory, not bandwidth (1.5 to 4.5 times $t_{bw}$).
- **Impact:** Pass counts times $t_{bw}$ underestimate run times by 1.2 to 2.6 times on the H100; conclusions drawn in pass units hold, but converting passes to time needs a device-specific factor.
- **Resolution:** Times are predicted from passes with measured kernel ratios (kernel-ratio model, within 1.0 to 1.4 times; wiki/studies/block-pass-time.md, wiki/studies/validation.md), and the bandwidth model holds within about 1.8 times with `max_operations` = 32. Comparisons between simulators are made in passes and in time per pass separately (wiki/studies/competitors.md).

### P002 — Minimizing the oversampling is not minimizing noisecirc's work
- **Problem:** `optimize_kraus` minimizes the oversampling $Z$ of each gate's Kraus set. noisecirc's work also depends on how often non-dominant operators are proposed (each starts a trajectory of its own) and on the sparsity of the dominant operator (the kernels skip zero entries); for mixed-unitary noise the optimal sets are degenerate, and an arbitrary one can be much worse on both.
- **Impact:** With `optimize_kraus`, depolarizing runs were up to 10 times slower (A5).
- **Resolution:** Fixed on noisecirc branch `fix/optimize-kraus-dominant`: keep the dominant operator where possible and lower the non-dominant weight; the option now saves 20 to 30% (wiki/studies/noisecirc-issues.md, item 3).

<!-- Add closed entries above this line. Template:

### P001 — Short problem title
- **Problem:** concise description of the original issue
- **Impact:** how it affected the research
- **Resolution:** verified resolution or reason for closure

-->
