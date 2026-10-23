---
type: paper
citekey: singal2026trajectree
doi: 10.48550/arXiv.2610.24160
summary: "Trajectree: CPU/MPS trajectory simulator caching branch probabilities and states in a tree."
updated: 2026-10-23
---
# Trajectree - A quantum trajectory-based quantum circuit simulator

[PDF](../pdf/singal2026trajectree.pdf) · [BibTeX](../bib/singal2026trajectree.bib) · <https://doi.org/10.48550/arXiv.2610.24160>

## Summary

Trajectree organizes trajectories as a tree over the Kraus branches of each channel. On the first visit of a node it computes all branch probabilities exactly from the state, then caches these probabilities and the most frequently used branch states under a memory cap. It runs on CPUs with matrix-product states and reports about 5 times speedup over qsim at 0.1% amplitude damping.

## Relevance

Prefix reuse with exact state-dependent probabilities on CPU tensor networks, outside this project's GPU state-vector scope, but related to noisecirc's segmented sampling. See [Prior art](../../studies/prior-art.md).
