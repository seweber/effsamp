---
type: paper
citekey: you2026varred
doi: 10.48550/arXiv.2607.17678
summary: Variance-reduced trajectory unravelings for GPU noisy simulation, characterized against Qiskit Aer.
updated: 2026-10-23
---
# Variance-Reduced Trajectory Unravelings for GPU Noisy Quantum-Circuit Simulation: Characterization and a Qiskit-Aer Integration Gap

[PDF](../pdf/you2026varred.pdf) · [BibTeX](../bib/you2026varred.bib) · <https://doi.org/10.48550/arXiv.2607.17678>

## Summary

The paper characterizes projector and analog unravelings of noise channels on a GPU state vector and reports about 21 times fewer trajectories than Aer's batched shots for the same statistical error. It also notes that Aer canonicalises Kraus channels at apply time, which affects which unraveling Aer actually samples.

## Relevance

Orthogonal to noisecirc's ideas (it reduces variance rather than work per trajectory), but relevant for how Aer applies Kraus channels in task A6. See [Prior art](../../studies/prior-art.md).
