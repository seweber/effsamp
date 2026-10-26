---
type: paper
citekey: ootomo2023quantum
doi: 10.48550/arXiv.2303.08989
summary: "Tensor-network quantum-circuit simulation with single-precision GEMMs emulated on tensor cores (TF32 or FP16 with error correction) and automatic precision selection."
updated: 2026-10-25
---
# Quantum Circuit Simulation by SGEMM Emulation on Tensor Cores and Automatic Precision Selection

[PDF](../pdf/ootomo2023quantum.pdf) · [BibTeX](../bib/ootomo2023quantum.bib) · <https://doi.org/10.48550/arXiv.2303.08989>

## Summary

The paper contracts quantum circuits as tensor networks, whose contractions reduce to matrix products, and runs these products on tensor cores with the error-corrected emulation of single precision (three products of split operands). FP16 is faster but its exponent range is too narrow for the small amplitudes of many qubits, so the authors select per contraction between FP16 with scaling and TF32 from exponent statistics of the inputs. On an A100 this is up to 1.86 times faster than cuBLAS's complex single-precision GEMM for random circuits and 1.45 times for the Sycamore circuit. Gate applications with small matrices are bandwidth bound and use a custom CUDA-core kernel instead.

## Relevance

Closest prior art for using tensor cores in quantum-circuit simulation at single-precision accuracy; it gains only for large matrix products, while noisecirc's stages are products of 8 x 8 to 16 x 16 complex matrices with long state vectors, see [Tensor cores for block passes](../../studies/tensor-cores.md). Tensor networks are out of scope for this project (PLAN.md); the paper is cited for the precision technique only.
