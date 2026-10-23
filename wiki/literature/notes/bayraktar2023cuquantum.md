---
type: paper
citekey: bayraktar2023cuquantum
doi: 10.1109/QCE57702.2023.00119
summary: "cuQuantum SDK: cuStateVec and cuTensorNet libraries and their performance."
updated: 2026-10-23
---
# cuQuantum SDK: A High-Performance Library for Accelerating Quantum Science

[PDF](../pdf/bayraktar2023cuquantum.pdf) · [BibTeX](../bib/bayraktar2023cuquantum.bib) · <https://doi.org/10.1109/QCE57702.2023.00119>

## Summary

The paper describes NVIDIA's cuQuantum SDK. For cuStateVec it shows that applying a dense gate matrix is memory-bound up to about 5 qubits in complex64 on the H100 and 4 on the A100, which sets the recommended gate-fusion size. The paper has no trajectory API.

## Relevance

Background for the bandwidth argument of the [Block-pass cost model](../../concepts/block-pass-cost-model.md): a dense fused gate stops being memory-bound beyond about 5 qubits on the H100, whereas noisecirc's blocks of up to 9 + 3 qubits hold many sparse gates. See [Prior art](../../studies/prior-art.md).
