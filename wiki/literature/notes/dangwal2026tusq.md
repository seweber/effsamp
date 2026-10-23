---
type: paper
citekey: dangwal2026tusq
doi: 10.1109/ISCA66397.2026.00163
summary: "TUSQ: pre-sampled Pauli error realizations traversed depth-first on GPU with uncomputation and a checkpoint cache."
updated: 2026-10-23
---
# TUSQ: Tracking, Uncomputation, and Sampling for Noisy Quantum Simulation

[PDF](../pdf/dangwal2026tusq.pdf) · [BibTeX](../bib/dangwal2026tusq.bib) · <https://doi.org/10.1109/ISCA66397.2026.00163>

## Summary

TUSQ pre-samples error realizations for Pauli or Pauli-twirled noise, commutes and tallies them with their counts, and prunes improbable ones, which makes it approximate. It then traverses the tree of error realizations depth-first: after simulating one branch it uncomputes back to the branching point instead of storing the state, and keeps a last-in-first-out checkpoint cache for operations that cannot be inverted, such as mid-circuit measurements. It runs on GPU state-vector and tensor-network backends and reports about 13 times speedup over CUDA-Q.

## Relevance

Anticipates depth-first traversal with checkpoints of noisecirc's segmented sampling, but only for invertible (mixed-unitary) noise, without rejection or refills. See [NoiseCirc's sampling algorithm](../../concepts/noisecirc-algorithm.md) and [Prior art](../../studies/prior-art.md).
