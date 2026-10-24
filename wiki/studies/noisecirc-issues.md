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

3. **`optimize_kraus=True` can multiply the distinct trajectories** (performance, verified). For a mixed-unitary channel the Kraus sets that reach the oversampling's lower bound are not unique: rotating the no-error operator $U$ into a Pauli error $P U$ that commutes with it, $\cos a\, U + i \sin a\, P U$, keeps every operator a scaled unitary. The optimizer (`twirling/kraus_optimization.py`) stops anywhere on this family, and so can spread the no-error weight over several operators. Every proposal of a non-dominant operator is propagated by the general kernel and starts a trajectory of its own. With depolarizing noise after the QFT's controlled phase of angle 0.012, the optimized set proposed a non-dominant operator with probability 0.022 per gate, 44 times as often as the minimal set; on a 28-qubit QFT at 0.1 expected errors per shot, `optimize_kraus=True` made 6478 block passes instead of 980 to 1286, and the run took 40 s instead of 4 s (A5 runs, LOG.md "A5 validation qft depolarizing optimized"). Generalized amplitude damping showed the same effect in the operation tables (2.4 times more accepted errors). Fix: branch `fix/optimize-kraus-dominant`, commit `4dca134`: a second stage lowers the bounds of all operators but the largest, with a penalty that keeps the oversampling within the tolerance of the first stage's result. Optimized sets then have a lower oversampling and fewer non-dominant proposals than the minimal sets for depolarizing, generalized damping and thermal noise (at the angle above: 2.5e-4 against 4.8e-4 for the minimal set), and amplitude damping is unchanged. A new test fails on `main` and passes with the fix; noisecirc's tests pass on the NumPy backend (the GPU run of the tests and of the affected A5 points follows).

All later measurements of this project use the branch `bench/fixes`, which is `main` with the fixes merged.

## Caveats

The list covers what the benchmarking touched: the exact sampling mode, qubits, `complex64`, and GPU 0 of bux (an H100 PCIe). The average mode, qutrits and subspace twirling were not examined (PLAN.md).

## Verdict

No issue so far affects simulation results. Issue 2 affects performance at large registers (from about 26 qubits, where batches are small) and inflated every 28-qubit timing taken on `main` by up to 1.7 times. Issue 3 makes the opt-in `optimize_kraus` counterproductive for mixed-unitary noise on near-identity gates.
