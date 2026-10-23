---
type: paper
citekey: wang2025tqsim
doi: 10.1145/3695053.3730992
summary: "TQSim: noisy simulation that reuses intermediate states of a trajectory tree, approximately."
updated: 2026-10-23
---
# Accelerating Simulation of Quantum Circuits under Noise via Computational Reuse

[PDF](../pdf/wang2025tqsim.pdf) · [BibTeX](../bib/wang2025tqsim.bib) · <https://doi.org/10.1145/3695053.3730992>

## Summary

The paper accelerates noisy simulation by computational reuse. The circuit is partitioned into subcircuits, and each noisy intermediate state is reused as the parent of a fixed number of child trajectories, forming a tree whose arity is chosen by a dynamic partition rule. Because children reuse a random rather than an identical prefix, the result is approximate; the authors report fidelity deviations up to about 0.016. States are cached in otherwise unused memory, on a CPU (Qulacs) backend.

## Relevance

Related to the prefix sharing of noisecirc's segmented sampling, but approximate and without a memory bound or rejection. See [NoiseCirc's sampling algorithm](../../concepts/noisecirc-algorithm.md) and [Prior art](../../studies/prior-art.md).
