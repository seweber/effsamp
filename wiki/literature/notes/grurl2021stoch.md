---
type: paper
citekey: grurl2021stoch
doi: 10.23919/DATE51398.2021.9474135
summary: Stochastic noisy circuit simulation with decision diagrams.
updated: 2026-10-23
---
# Stochastic Quantum Circuit Simulation Using Decision Diagrams

[PDF](../pdf/grurl2021stoch.pdf) · [BibTeX](../bib/grurl2021stoch.bib) · <https://doi.org/10.23919/DATE51398.2021.9474135>

## Summary

The paper simulates noisy circuits by independent stochastic runs on decision diagrams, choosing Kraus operators per gate from the state-dependent probabilities, e.g. both branch norms for amplitude damping, and runs many trajectories concurrently on CPUs.

## Relevance

An example of the standard per-gate state-dependent sampling noisecirc avoids; outside the GPU state-vector scope. See [Prior art](../../studies/prior-art.md).
