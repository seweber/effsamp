---
type: paper
citekey: li2019sanq
doi: 10.48550/arXiv.1904.11590
summary: "SANQ: noisy simulation that pre-generates Pauli error traces and executes them recursively, storing states only along the recursion."
updated: 2026-10-23
---
# SANQ: A Simulation Framework for Architecting Noisy Intermediate-Scale Quantum Computing System

[PDF](../pdf/li2019sanq.pdf) · [BibTeX](../bib/li2019sanq.bib) · <https://doi.org/10.48550/arXiv.1904.11590>

## Summary

The paper introduces a simulation framework for noisy circuits. Its execution reordering generates the Pauli error traces of all shots before simulation, orders them by the location of their first error, and processes traces with a common prefix recursively from the stored state at the branching point. The number of stored state vectors is the recursion depth, which stays small because errors are rare. The same technique was published at DAC 2020 (Li, Ding, Xie, 10.1109/DAC18072.2020.9218666). It is CPU-only and limited to Pauli noise.

## Relevance

The earliest found instance of depth-first, memory-bounded prefix reuse of pre-sampled noisy trajectories; noisecirc's segmented sampling extends it to non-unitary channels by rejection. The paper should not claim depth-first prefix reuse as new. See [NoiseCirc's sampling algorithm](../../concepts/noisecirc-algorithm.md) and [Prior art](../../studies/prior-art.md).
