# Lab Book

Terse ledger of the project's history: one entry per experiment, simulation,
or investigation, newest first, failures included. Each entry states the
outcome and points to the evidence (`data/`, `code/`) and to the detail
(`memory/`, `wiki/`); it does not repeat them.

Approved tasks live in `PLAN.md`; name the task ID in each entry. Working
detail and know-how go in `memory/`, findings in `wiki/`, conceptual traps in
`PROBLEMS.md`, task proposals in `TASKS.md`.

---

## 2026-10-23 21:43 UTC  A3 dry-run sampler
- **Goal:** Predict block passes without GPU
- **Task:** A3
- **Method:** code/bench/dryrun.py runs noisecirc's sample() with surrogate states: norm factor per gate = tr(M^dag M)/2^w (maximally mixed targets)
- **Outcome:** Works, ~0.01-1 s per point at n=24; to be validated against GPU diagnostics
- **Next:** Validate against A2 run diagnostics
- **Refs:** code/bench/dryrun.py

## 2026-10-23 21:43 UTC  A1 algorithm reading and prior-art check
- **Goal:** Understand noisecirc's algorithm and check its ideas against the literature
- **Task:** A1
- **Method:** Read src/ and svpass; literature search by subagent (18 papers, 14 recorded via research-lit); key claims spot-checked in the PDFs' text
- **Outcome:** Operator-norm proposals with rejection for non-mixed-unitary channels not found in literature; depth-first prefix reuse anticipated (SANQ, TUSQ, Pauli noise only); wide shared-memory kernels anticipated (HyQuas, Atlas); wrong DOI in noisecirc docs fixed on fix/elsman-doi
- **Next:** Check CUDA-Q's batched-branch fusion when benchmarking CUDA-Q (A6)
- **Refs:** wiki/concepts/noisecirc-algorithm.md, wiki/studies/prior-art.md, wiki/studies/noisecirc-issues.md, memory/tasks/A1.md

## 2026-10-23 21:40 UTC  A2 end-to-end runs n=24
- **Goal:** Wall time and block passes of NoiseCirc runs (defaults, damping, 1000 shots) at n=24 to test T = passes x t_bw
- **Task:** A2
- **Method:** code/bench/gpurun a2_runs.py --circuits ghz,brickwork,qft,random,grid,qaoa --qubits 24 --ps 0,0.0001,0.001,0.01 --shots 1000 --budget 480
- **Outcome:** exit 124; outputs in data/20261023-213022-a2-end-to-end-runs-n-24
- **Next:** none
- **Refs:** data/20261023-213022-a2-end-to-end-runs-n-24, code/bench/a2_runs.py

## 2026-10-23 21:31 UTC  A3 dry-run sweep fusion
- **Goal:** Block and block-pass counts of six circuits at n=24 against one NoiseCirc parameter (fusion), by dry run
- **Task:** A3
- **Method:** code/noisecirc/.venv/bin/python code/bench/a3_sweep.py fusion
- **Outcome:** exit 0; outputs in data/20261023-213106-a3-dry-run-sweep-fusion
- **Next:** none
- **Refs:** data/20261023-213106-a3-dry-run-sweep-fusion, code/bench/a3_sweep.py, code/bench/dryrun.py

## 2026-10-23 21:31 UTC  A3 dry-run sweep noise
- **Goal:** Block and block-pass counts of six circuits at n=24 against one NoiseCirc parameter (noise), by dry run
- **Task:** A3
- **Method:** code/noisecirc/.venv/bin/python code/bench/a3_sweep.py noise
- **Outcome:** exit 1; outputs in data/20261023-213106-a3-dry-run-sweep-noise
- **Next:** none
- **Refs:** data/20261023-213106-a3-dry-run-sweep-noise, code/bench/a3_sweep.py, code/bench/dryrun.py

## 2026-10-23 21:31 UTC  A3 dry-run sweep segment
- **Goal:** Block and block-pass counts of six circuits at n=24 against one NoiseCirc parameter (segment), by dry run
- **Task:** A3
- **Method:** code/noisecirc/.venv/bin/python code/bench/a3_sweep.py segment
- **Outcome:** exit 1; outputs in data/20261023-213106-a3-dry-run-sweep-segment
- **Next:** none
- **Refs:** data/20261023-213106-a3-dry-run-sweep-segment, code/bench/a3_sweep.py, code/bench/dryrun.py

## 2026-10-23 21:31 UTC  A3 dry-run sweep oversampling
- **Goal:** Block and block-pass counts of six circuits at n=24 against one NoiseCirc parameter (oversampling), by dry run
- **Task:** A3
- **Method:** code/noisecirc/.venv/bin/python code/bench/a3_sweep.py oversampling
- **Outcome:** exit 1; outputs in data/20261023-213106-a3-dry-run-sweep-oversampling
- **Next:** none
- **Refs:** data/20261023-213106-a3-dry-run-sweep-oversampling, code/bench/a3_sweep.py, code/bench/dryrun.py

## 2026-10-23 21:29 UTC  A2 block pass times n=28
- **Goal:** Time each block of six circuits (damping 1e-3, defaults) against the bandwidth floor at n=28
- **Task:** A2
- **Method:** code/bench/gpurun a2_blocks.py --qubits 28
- **Outcome:** exit 0; outputs in data/20261023-212736-a2-block-pass-times-n-28
- **Next:** none
- **Refs:** data/20261023-212736-a2-block-pass-times-n-28, code/bench/a2_blocks.py

## 2026-10-23 21:27 UTC  A2 block pass times n=26
- **Goal:** Time each block of six circuits (damping 1e-3, defaults) against the bandwidth floor at n=26
- **Task:** A2
- **Method:** code/bench/gpurun a2_blocks.py --qubits 26
- **Outcome:** exit 0; outputs in data/20261023-212635-a2-block-pass-times-n-26
- **Next:** none
- **Refs:** data/20261023-212635-a2-block-pass-times-n-26, code/bench/a2_blocks.py

## 2026-10-23 21:26 UTC  A2 block pass times n=24
- **Goal:** Time each block of six circuits (damping 1e-3, defaults) against the bandwidth floor at n=24
- **Task:** A2
- **Method:** code/bench/gpurun a2_blocks.py --qubits 24
- **Outcome:** exit 0; outputs in data/20261023-212608-a2-block-pass-times-n-24
- **Next:** none
- **Refs:** data/20261023-212608-a2-block-pass-times-n-24, code/bench/a2_blocks.py

<!-- New entries go above this line, newest first. Template:

## YYYY-MM-DD HH:MM UTC  Short title
- **Goal:** what question this entry tries to answer
- **Task:** PLAN.md task ID, or "none"
- **Method:** one line: command, model, or parameters
- **Outcome:** result, or "blocked: …"
- **Next:** the immediate follow-up (or "none")
- **Refs:** data/<run>, code/<subdir>, memory/tasks/<ID>.md, wiki/studies/<page>.md

-->
