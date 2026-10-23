---
type: paper
citekey: xu2024atlas
doi: 10.1109/SC41406.2024.00087
summary: "Atlas: hierarchical circuit partitioning for multi-GPU state-vector simulation with shared-memory kernels."
updated: 2026-10-23
---
# Atlas: Hierarchical Partitioning for Quantum Circuit Simulation on GPUs

[PDF](../pdf/xu2024atlas.pdf) · [BibTeX](../bib/xu2024atlas.bib) · <https://doi.org/10.1109/SC41406.2024.00087>

## Summary

Atlas partitions circuits hierarchically for multi-GPU state-vector simulation. Within a GPU, it uses two kernel types: dense fused kernels through cuStateVec, up to about 5 qubits, and shared-memory kernels that load a subset of the state into shared memory and apply many gates one by one. Its shared-memory kernels always include the three least significant qubits for contiguous memory access. It does not treat noise.

## Relevance

Prior art for the kernel structure of noisecirc's fused blocks (wide tiles in shared memory, pinned low qubits), see [NoiseCirc's sampling algorithm](../../concepts/noisecirc-algorithm.md) and [Prior art](../../studies/prior-art.md).
