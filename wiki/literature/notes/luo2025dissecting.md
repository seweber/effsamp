---
type: paper
citekey: luo2025dissecting
doi: 10.48550/arXiv.2501.12084
summary: "Microbenchmarks of the Hopper GPU (H800 PCIe): the warp-level tensor-core instruction mma reaches on average 62.9% of the peak, the warpgroup instruction wgmma over 95%; also memory, DPX, distributed shared memory and TMA."
updated: 2026-10-26
---
# Dissecting the NVIDIA Hopper Architecture through Microbenchmarking and Multiple Level Analysis

[PDF](../pdf/luo2025dissecting.pdf) · [BibTeX](../bib/luo2025dissecting.bib) · <https://doi.org/10.48550/arXiv.2501.12084>

## Summary

The authors measure latency and throughput of the memory hierarchy, the tensor-core instructions, the DPX instructions, distributed shared memory and the Tensor Memory Accelerator on an H800 PCIe (Hopper), compared with an A100 and an RTX 4090. For the tensor cores, the warp-level `mma.sync` instructions, which Hopper keeps for compatibility, reach on average only 62.9% of Hopper's theoretical peak, while the asynchronous warpgroup instructions `wgmma` reach over 95% with zero-initialized matrices and less with random ones, as the card then runs into its 350 W power limit. Sparse `mma` instructions gain only 1.42 times over dense ones on Hopper instead of 2. The paper extends the IPDPS 2024 paper "Benchmarking and Dissecting the Nvidia Hopper GPU Architecture" (arXiv 2402.13499).

## Relevance

It calibrates the tensor-core measurements of this project: `mma.sync` with FP16 inputs reached 483 TFLOP/s on GPU 0 (H100 PCIe), about 64% of its peak of 756 TFLOP/s, which matches the 62.9% measured here; `wgmma` would raise the ceiling by about 1.5 times. See [Tensor cores for block passes](../../studies/tensor-cores.md) and [Chained tensor-core stages and complex32](../../studies/chained-tensor-cores.md). The brainstorm of PLAN.md task A18 cites this study for the same figures.
