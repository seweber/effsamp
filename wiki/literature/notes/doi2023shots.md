---
type: paper
citekey: doi2023shots
doi: 10.48550/arXiv.2308.03399
summary: "Qiskit Aer's GPU multi-shot techniques: batched shots and shot branching."
updated: 2026-10-23
---
# Efficient techniques to GPU Accelerations of Multi-Shot Quantum Computing Simulations

[PDF](../pdf/doi2023shots.pdf) · [BibTeX](../bib/doi2023shots.bib) · <https://doi.org/10.48550/arXiv.2308.03399>

## Summary

The paper describes how Qiskit Aer accelerates many-shot noisy simulation on GPUs. Batched execution runs many independent shots in one kernel; for a general Kraus channel every shot computes the expectation values of the Kraus operators on its own state and compares them with its random number. Shot branching keeps one state for all shots and splits it into several states whenever the shots draw different outcomes of a noise channel or measurement, which shares the common prefix of the trajectories. Branching is breadth-first: all branches live at once, and the authors state that they do not record states for a recursive execution; when memory runs out, waiting shots restart from the beginning. Gate fusion is Aer's usual fusion of up to about 5 qubits.

## Relevance

Aer with shot branching is the closest competitor named in PLAN.md (task A6). It shares trajectory prefixes like noisecirc's segmented sampling, but needs state-dependent probability passes at every non-unitary channel and keeps all branches in memory instead of traversing depth-first. See [NoiseCirc's sampling algorithm](../../concepts/noisecirc-algorithm.md) and [Prior art](../../studies/prior-art.md).
