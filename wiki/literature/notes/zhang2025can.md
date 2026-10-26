---
type: paper
citekey: zhang2025can
doi: 10.48550/arXiv.2502.16851
summary: "A roofline argument and measurements that tensor cores speed up memory-bound kernels by at most 1.33 times in double precision (2 times in the limit), and in practice not at all."
updated: 2026-10-25
---
# Can Tensor Cores Benefit Memory-Bound Kernels? (No!)

[PDF](../pdf/zhang2025can.pdf) · [BibTeX](../bib/zhang2025can.bib) · <https://doi.org/10.48550/arXiv.2502.16851>

## Summary

The authors bound the speedup of a kernel whose time is the sum or the maximum of memory and computation when its computation moves from CUDA cores to tensor cores with alpha times their throughput: for memory-bound kernels the speedup stays below 1 + (alpha - 1)/(alpha + 1) times a term below one, which is 1.33 for FP64 tensor cores on V100, A100 and H100 and 2 for infinitely fast ones. Measurements of STREAM scale, SpMV and a stencil with tensor-core implementations confirm no sound gains over CUDA cores.

## Relevance

The same logic bounds noisecirc's tensor-core stages: its passes are within 1.1 to 1.4 times of the memory floor in complex64, so even free arithmetic gains little, see [Tensor cores for block passes](../../studies/tensor-cores.md).
