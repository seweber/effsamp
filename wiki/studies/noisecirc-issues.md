---
title: Issues found in noisecirc
summary: Bugs and issues found in noisecirc during benchmarking, with their fix branches
type: study
tasks: [A1]
status: verified
updated: 2026-10-23
---
# Issues found in noisecirc

## Question

Which bugs and issues in `code/noisecirc` turned up while benchmarking it (PLAN.md asks to report each one here and fix it on a dedicated `fix/` branch)? Each issue lists its evidence, its fix branch in the local noisecirc repository (branches cannot be pushed from this container), and its status.

## Approach

Issues are recorded as they are found, during reading the code (task A1) and running it (tasks A2 to A6). A fix branch starts from noisecirc's `main` and holds only that fix, so that it can be reviewed alone.

## Runs

- Profile of brickwork runs at 24 and 28 qubits on `main`, LOG.md entries "A2 profile n=24" and "A2 profile n=28" of 2026-10-23: `data/20261023-*-a2-profile-n-24`, `data/20261023-*-a2-profile-n-28`.
- The same at 28 qubits with the fix, LOG.md entry "A2 profile n=28 with fix/squared-norms-parallel".

## Results

The issues found so far:

1. **Wrong DOI in a reference** (documentation only, verified). `docs/snippets/kronfree.py` cites Elsman and Henriksen, "Gate Fusion Is Map Fusion" (ARRAY '25), with DOI `10.1145/3736112.3736142`. Crossref lists that DOI for Berthelot, Ioualalen and Martel's "Accelerating the Static Analysis of Neural Networks by Batch Representation of Abstract Values" from the same proceedings; the cited paper is `10.1145/3736112.3736143`. Fix: branch `fix/elsman-doi`, commit `59a79fe`. Found by the literature check of [Prior art](prior-art.md).

2. **Squared norms of long rows take longer than the pass that wrote them** (performance, verified). svpass reduces each row's chunk sums with a single warp (`squared_norms.cu`). A row of $2^n$ amplitudes has $2^{n-8}$ chunk sums, so at 28 qubits one warp adds $2^{20}$ values one after another, about 4 ms on the H100, while the pass over the row takes 2.4 to 4 ms. At 28 qubits the device memory holds only about 33 rows, so batches hold one or two rows and every segment waits for this reduction. On a 28-qubit brickwork with damping $p = 10^{-3}$ and 1000 shots, the run took 35.1 s, of which the passes were 17.7 s. Fix: branch `fix/squared-norms-parallel`, commit `a2d9fdd`: rows of more than 4096 chunk sums are summed in parts by one thread block each and the parts by one warp per row, both in a fixed order, so the sums stay reproducible. The same run then takes 20.9 s (1.7 times faster), and an ideal run 0.073 s instead of 0.145 s. svpass's 317 tests (one new, on 22-qubit rows) and noisecirc's 178 tests pass on the H100.

A related, smaller cost remains: measuring draws from a cumulative sum of the chunk sums that one thread block per row computes, about 2.6 ms per call at 28 qubits. It runs once per leaf pool, not per segment, and cost 1.0 s of the 20.9 s run above; it was not changed.

3. **`optimize_kraus=True` made depolarizing runs slower instead of faster** (performance, verified). The option rotates each gate's Kraus operators to lower the oversampling $Z$ (`twirling/kraus_optimization.py`). For a mixed-unitary channel the sets that reach the lower bound are not unique: rotating the no-error operator $U$ into a Pauli error $P U$ that commutes with it, $\cos a\, U + i \sin a\, P U$, keeps every operator a scaled unitary. The optimizer stopped anywhere on this family, which had two costs:
   - It could spread the no-error weight over several operators. Every proposal of a non-dominant operator is propagated by the general kernel and starts a trajectory of its own: with depolarizing noise after the QFT's controlled phase of angle 0.012, the optimized set proposed a non-dominant operator with probability 0.022 per gate, 44 times as often as the minimal set, and a 28-qubit QFT at 0.1 expected errors per shot made 6478 block passes instead of 980 to 1286 and took 40 s instead of 4 s (LOG.md "A5 validation qft depolarizing optimized").
   - Any rotation into the no-error operator fills the zero entries that the generated kernels skip: the QFT's no-error kernels took 2.16 instead of 1.14 times $t_{bw}$ and its general kernels 3.01 instead of 1.78 (LOG.md "A5 block pass times qft depolarizing n=28 …").

   Fix: branch `fix/optimize-kraus-dominant`, four commits (`4dca134`, `a5a045e`, `815d6a9`, `f76a052`). The optimization first rotates only the non-dominant operators and keeps the dominant one as it is, which for a mixed-unitary block is already the scaled gate; only where that misses the target does it rotate all operators, followed by a second stage that lowers the weight of the non-dominant operators (where the first stage raised it above the minimal set's, for at most 150 iterations) while the oversampling stays within the first stage's. A new test fails on `main` and passes with the fix; svpass's 317 and noisecirc's 179 tests pass on the H100. With the fix, on 28 qubits, 1000 shots (LOG.md "A5 validation … depolarizing optimized … (fix v4)"):

   | run | without `optimize_kraus` | `optimize_kraus`, `main` | `optimize_kraus`, fixed |
   | --- | --- | --- | --- |
   | QFT, $M = 0.1$ | 3.5 to 4.5 s | 40 s | 3.7 to 4.7 s |
   | QFT, $M = 1$ | 32.6 s | — | 25.0 to 26.0 s |
   | brickwork, $M = 0.1$ | 6.4 s | 11.1 s | 5.3 to 6.2 s |
   | brickwork, $M = 1$ | 47.0 s | — | 32.8 s |

   The kernels are as fast as without the option (QFT: 1.14 and 1.79 times $t_{bw}$), and the optimization itself takes less compile time than on `main` (first runs of 22 to 67 s against 72 to 144 s).

4. **`optimize_kraus` can still move the dominant operator, e.g. for dephasing after a two-qubit gate** (performance, verified on the Kraus sets). The first stage of the fixed optimization (issue 3) keeps the dominant operator but aims the other operators at the bound of the whole set minus the dominant bound, which they may not reach; it then falls back to rotating all operators. For phase damping after a two-qubit gate, the result makes 1.76 times more accepted errors per gate than the canonical set (0.88 instead of 0.50 in units of $p$), each of which starts a trajectory of its own ([Optimal Kraus representations for noisecirc](kraus-representation.md)). The right target is the other operators' own lower bound, $\max(\lVert\sum_j L_j^\dagger L_j\rVert, \lVert\sum_j L_jL_j^\dagger\rVert)$ over them, and since the canonical set is often a degenerate stationary point, the minimisation needs random starts. Fix: branch `fix/optimize-kraus-residual-target` (on top of `fix/optimize-kraus-dominant`), commit `9236680`, with a new tunable `KRAUS_RESIDUAL_STARTS` = 12. With it, all fourteen one- and two-qubit channels of the A12 study come within 1% of the certified optimum and keep the canonical dominant operator; noisecirc's 36 tests of `test_sta.py` and `test_maps.py` pass (CPU); merged into `bench/fixes` (`5c8fc57`), where svpass's 326 and noisecirc's 182 tests pass on the H100 (LOG.md "A12 tests of bench/fixes with fix/optimize-kraus-residual-target"). Not measured end to end.

All later measurements of this project use the branch `bench/fixes`, which is `main` with the fixes merged; from 2026-10-24 09:30 UTC on (tasks A7 to A9), it also contains the improvements of [Error kernels and block sizes](error-kernels.md) (masked error kernels, on by default, and autotuning, off by default).

## Caveats

The list covers what the benchmarking touched: the exact sampling mode, qubits, `complex64`, and GPU 0 of bux (an H100 PCIe). The average mode, qutrits and subspace twirling were not examined (PLAN.md).

## Verdict

No issue so far affects simulation results. Issue 2 affects performance at large registers (from about 26 qubits, where batches are small) and inflated every 28-qubit timing taken on `main` by up to 1.7 times. Issue 3 made the opt-in `optimize_kraus` counterproductive for mixed-unitary noise; with the fix it saves 20 to 30% of the run time at one expected error per shot. Issue 4 is a remaining suboptimality of the same option for channels with a degenerate mixed-unitary part.
