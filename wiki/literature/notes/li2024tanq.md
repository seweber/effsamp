---
type: paper
citekey: li2024tanq
doi: 10.48550/arXiv.2404.13184
summary: "TANQ-Sim: GPU density-matrix simulation of noisy circuits whose two-qubit superoperators run on the FP64 tensor cores of A100 and H100 GPUs."
updated: 2026-10-25
---
# TANQ-Sim: Tensorcore Accelerated Noisy Quantum System Simulation via QIR on Perlmutter HPC

[PDF](../pdf/li2024tanq.pdf) · [BibTeX](../bib/li2024tanq.bib) · <https://doi.org/10.48550/arXiv.2404.13184>

## Summary

TANQ-Sim simulates noisy circuits with full density matrices on multi-GPU systems (Perlmutter, NVSHMEM). Applying a two-qubit gate's 16 x 16 superoperator to the vectorized density matrix is a matrix product of shape 16 x 16 times 16 x 4^(n-2), which it maps onto the double-precision tensor cores with mma instructions; one-qubit gates stay on the CUDA cores. It also fuses gates for density matrices. The authors call it the first use of FP64 tensor cores outside machine learning.

## Relevance

Prior art for tensor cores in noisy-circuit simulation, in double precision and for density matrices, where products of superoperators are dense; noisecirc samples state vectors in single precision, see [Tensor cores for block passes](../../studies/tensor-cores.md) and [Prior art](../../studies/prior-art.md).
