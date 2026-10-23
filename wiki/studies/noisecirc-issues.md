---
title: Issues found in noisecirc
summary: Bugs and issues found in noisecirc during benchmarking, with their fix branches
type: study
tasks: [A1]
status: unverified
updated: 2026-10-23
---
# Issues found in noisecirc

## Question

Which bugs and issues in `code/noisecirc` turned up while benchmarking it (PLAN.md asks to report each one here and fix it on a dedicated `fix/` branch)? Each issue lists its evidence, its fix branch in the local noisecirc repository (branches cannot be pushed from this container), and its status.

## Approach

Issues are recorded as they are found, during reading the code (task A1) and running it (tasks A2 to A6). A fix branch starts from noisecirc's `main` and holds only that fix, so that it can be reviewed alone.

## Runs

No runs: the issues so far were found by reading.

## Results

The issues found so far:

1. **Wrong DOI in a reference** (documentation only, verified). `docs/snippets/kronfree.py` cites Elsman and Henriksen, "Gate Fusion Is Map Fusion" (ARRAY '25), with DOI `10.1145/3736112.3736142`. Crossref lists that DOI for Berthelot, Ioualalen and Martel's "Accelerating the Static Analysis of Neural Networks by Batch Representation of Abstract Values" from the same proceedings; the cited paper is `10.1145/3736112.3736143`. Fix: branch `fix/elsman-doi`, commit `59a79fe`. Found by the literature check of [Prior art](prior-art.md).

## Caveats

The list covers what the benchmarking touched: the exact sampling mode, qubits, `complex64`, and GPU 0 of bux (an H100 PCIe). The average mode, qutrits and subspace twirling were not examined (PLAN.md).

## Verdict

No issue so far affects simulation results.
