---
type: paper
citekey: patti2025ptsbe
doi: 10.1145/3712285.3759871
summary: "CUDA-Q pre-trajectory sampling with batched execution (PTSBE): Kraus selections drawn before simulation, deduplicated, each simulated once."
updated: 2026-10-23
---
# Augmenting Simulated Noisy Quantum Data Collection by Orders of Magnitude Using Pre-Trajectory Sampling with Batched Execution

[PDF](../pdf/patti2025ptsbe.pdf) · [BibTeX](../bib/patti2025ptsbe.bib) · <https://doi.org/10.1145/3712285.3759871>

## Summary

The paper augments noisy data generation in CUDA-Q. Its baseline simulates independent trajectories, sampling unitary mixtures without the state but computing state-dependent probabilities for general channels. PTSBE instead draws the Kraus selections of many trajectories from fixed probabilities before any state is propagated, deduplicates them, assigns shots to each distinct selection, prepares each distinct trajectory once and samples its shots in bulk. All examples use depolarizing noise, and the paper gives no rule that keeps the method exact for non-unitary Kraus channels. Distinct trajectories share no prefix work.

## Relevance

Anticipates the pre-sample-and-deduplicate part of noisecirc's grouped proposals, but only for mixed-unitary noise. noisecirc's operator-norm proposals with rejection extend this exactly to general Kraus channels. See [NoiseCirc's sampling algorithm](../../concepts/noisecirc-algorithm.md) and [Prior art](../../studies/prior-art.md).
