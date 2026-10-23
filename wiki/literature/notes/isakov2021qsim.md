---
type: paper
citekey: isakov2021qsim
doi: 10.48550/arXiv.2111.02396
summary: qsim/Cirq noisy trajectories with the delayed inner-product algorithm based on state-independent lower bounds.
updated: 2026-10-23
---
# Simulations of Quantum Circuits with Approximate Noise using qsim and Cirq

[PDF](../pdf/isakov2021qsim.pdf) · [BibTeX](../bib/isakov2021qsim.bib) · <https://doi.org/10.48550/arXiv.2111.02396>

## Summary

The paper presents noisy trajectory simulation in qsim and Cirq. Its delayed inner-product algorithm gives each Kraus operator a state-independent lower bound on its probability, the squared smallest singular value. If a uniform random number falls below the sum of the lower bounds, the Kraus operator is chosen without computing any inner product, and its application can be fused with later gates. Otherwise the deferred operators are applied and the remaining probability is sampled exactly from the state's norms. For mixed-unitary channels the lower bounds sum to one, so no norm is ever computed; for amplitude damping of strength gamma, the fallback still happens with probability about gamma per channel. Trajectories are independent, and GPU fusion is about 4 qubits.

## Relevance

Closest prior art to noisecirc's state-independent proposals ([NoiseCirc's sampling algorithm](../../concepts/noisecirc-algorithm.md)). It uses lower bounds and an exact fallback, where noisecirc uses upper bounds and rejection; it neither pre-samples nor groups shots. cuStateVec Ex uses the same algorithm. See [Prior art](../../studies/prior-art.md).
