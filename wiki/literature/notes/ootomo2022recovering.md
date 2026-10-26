---
type: paper
citekey: ootomo2022recovering
doi: 10.1177/10943420221090256
summary: "Single-precision matrix products on tensor cores by splitting each FP32 operand into a TF32 or FP16 leading term and a rounded residual, with the leading product accumulated outside the tensor cores to avoid their round-toward-zero."
updated: 2026-10-25
---
# Recovering single precision accuracy from Tensor Cores while surpassing the FP32 theoretical peak performance

[PDF](../pdf/ootomo2022recovering.pdf) · [BibTeX](../bib/ootomo2022recovering.bib) · <https://doi.org/10.1177/10943420221090256>

## Summary

The authors split each single-precision matrix into a half-precision (or TF32) leading part and a scaled residual, and compute the product from three tensor-core products, dropping the product of the two residuals as negligible. They show that the remaining accuracy loss of earlier schemes comes from the tensor cores rounding their accumulation toward zero, and avoid it by adding the products to the accumulator on the CUDA cores, which round to nearest. They also choose the residual's scaling so that it rarely underflows. On an A100, their CUTLASS implementation matches FP32 accuracy at 51 TFLOP/s with FP16 (limited exponent range) and 33 TFLOP/s with TF32, above the 19.5 TFLOP/s FP32 peak.

## Relevance

Its splitting and its fix for the tensor cores' truncation are the basis of the `tf32x3` and `f16x3` modes of noisecirc's tensor-core stages, see [Tensor cores for block passes](../../studies/tensor-cores.md). The three-fold cost of the split is what makes single-precision tensor-core stages slower than noisecirc's structured CUDA-core kernels on the H100.
