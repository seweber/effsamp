# Lab Book

Terse ledger of the project's history: one entry per experiment, simulation,
or investigation, newest first, failures included. Each entry states the
outcome and points to the evidence (`data/`, `code/`) and to the detail
(`memory/`, `wiki/`); it does not repeat them.

Approved tasks live in `PLAN.md`; name the task ID in each entry. Working
detail and know-how go in `memory/`, findings in `wiki/`, conceptual traps in
`PROBLEMS.md`, task proposals in `TASKS.md`.

---

## 2026-10-24 15:40 UTC  A11 Aer tuning: analysis and conclusion
- **Goal:** Tune Qiskit Aer's shot branching options and compare tuned Aer with tuned noisecirc
- **Task:** A11
- **Method:** Aer 0.17.2 source read for options; code/bench/a6_runs.py --aer-option (10 settings x 4 circuits, n=24, A6 points); noisecirc bench/fixes dd4b8c8 default and autotune (5 reps, medians); 5 points at n=28; code/bench/a11_analyze.py
- **Outcome:** Only fusion width helps Aer: width 3 (default 2 with noise) saves 8% geomean, 0-28% per point; cost factor neutral, no fusion 1.8x and no branching sampling 6.2x slower. noisecirc autotune 4%. Speedup defaults 6.2-61x, tuned 6.3-67x (6.3-48 without brickwork M=0.1, where Aer's heevx bug disables its fusion); n=28 tuned 10-30x. 2-rep noisecirc runs had outliers, superseded by 5-rep runs
- **Next:** none
- **Refs:** wiki/studies/aer-tuning.md, data/a11-analysis, code/bench/a11_analyze.py

## 2026-10-24 15:37 UTC  A11 noisecirc autotune qaoa n=24 5 reps
- **Goal:** noisecirc bench/fixes dd4b8c8 (autotune) at the A6 points: qaoa, damping M=0.01/0.1/1, 1000 shots, 5 timed reps (the 2-rep runs had outliers at 10-30 ms)
- **Task:** A11
- **Method:** code/bench/gpurun a2_runs.py --circuits qaoa --qubits 24 --noise damping --ps 5.55556e-05,0.000555556,0.00555556 --shots 1000 --reps 5 --option autotune=1
- **Outcome:** exit 0; outputs in data/20261024-153652-a11-noisecirc-autotune-qaoa-n-24-5-reps
- **Next:** none
- **Refs:** data/20261024-153652-a11-noisecirc-autotune-qaoa-n-24-5-reps, code/bench/a2_runs.py

## 2026-10-24 15:36 UTC  A11 noisecirc autotune qft n=24 5 reps
- **Goal:** noisecirc bench/fixes dd4b8c8 (autotune) at the A6 points: qft, damping M=0.01/0.1/1, 1000 shots, 5 timed reps (the 2-rep runs had outliers at 10-30 ms)
- **Task:** A11
- **Method:** code/bench/gpurun a2_runs.py --circuits qft --qubits 24 --noise damping --ps 3.33333e-05,0.000333333,0.00333333 --shots 1000 --reps 5 --option autotune=1
- **Outcome:** exit 0; outputs in data/20261024-153640-a11-noisecirc-autotune-qft-n-24-5-reps
- **Next:** none
- **Refs:** data/20261024-153640-a11-noisecirc-autotune-qft-n-24-5-reps, code/bench/a2_runs.py

## 2026-10-24 15:36 UTC  A11 noisecirc autotune brickwork n=24 5 reps
- **Goal:** noisecirc bench/fixes dd4b8c8 (autotune) at the A6 points: brickwork, damping M=0.01/0.1/1, 1000 shots, 5 timed reps (the 2-rep runs had outliers at 10-30 ms)
- **Task:** A11
- **Method:** code/bench/gpurun a2_runs.py --circuits brickwork --qubits 24 --noise damping --ps 3.26797e-05,0.000326797,0.00326797 --shots 1000 --reps 5 --option autotune=1
- **Outcome:** exit 0; outputs in data/20261024-153622-a11-noisecirc-autotune-brickwork-n-24-5-reps
- **Next:** none
- **Refs:** data/20261024-153622-a11-noisecirc-autotune-brickwork-n-24-5-reps, code/bench/a2_runs.py

## 2026-10-24 15:36 UTC  A11 noisecirc autotune ghz n=24 5 reps
- **Goal:** noisecirc bench/fixes dd4b8c8 (autotune) at the A6 points: ghz, damping M=0.01/0.1/1, 1000 shots, 5 timed reps (the 2-rep runs had outliers at 10-30 ms)
- **Task:** A11
- **Method:** code/bench/gpurun a2_runs.py --circuits ghz --qubits 24 --noise damping --ps 0.000215054,0.00215054,0.0215054 --shots 1000 --reps 5 --option autotune=1
- **Outcome:** exit 0; outputs in data/20261024-153615-a11-noisecirc-autotune-ghz-n-24-5-reps
- **Next:** none
- **Refs:** data/20261024-153615-a11-noisecirc-autotune-ghz-n-24-5-reps, code/bench/a2_runs.py

## 2026-10-24 15:36 UTC  A11 noisecirc default qaoa n=24 5 reps
- **Goal:** noisecirc bench/fixes dd4b8c8 (default) at the A6 points: qaoa, damping M=0.01/0.1/1, 1000 shots, 5 timed reps (the 2-rep runs had outliers at 10-30 ms)
- **Task:** A11
- **Method:** code/bench/gpurun a2_runs.py --circuits qaoa --qubits 24 --noise damping --ps 5.55556e-05,0.000555556,0.00555556 --shots 1000 --reps 5
- **Outcome:** exit 0; outputs in data/20261024-153603-a11-noisecirc-default-qaoa-n-24-5-reps
- **Next:** none
- **Refs:** data/20261024-153603-a11-noisecirc-default-qaoa-n-24-5-reps, code/bench/a2_runs.py

## 2026-10-24 15:36 UTC  A11 noisecirc default qft n=24 5 reps
- **Goal:** noisecirc bench/fixes dd4b8c8 (default) at the A6 points: qft, damping M=0.01/0.1/1, 1000 shots, 5 timed reps (the 2-rep runs had outliers at 10-30 ms)
- **Task:** A11
- **Method:** code/bench/gpurun a2_runs.py --circuits qft --qubits 24 --noise damping --ps 3.33333e-05,0.000333333,0.00333333 --shots 1000 --reps 5
- **Outcome:** exit 0; outputs in data/20261024-153551-a11-noisecirc-default-qft-n-24-5-reps
- **Next:** none
- **Refs:** data/20261024-153551-a11-noisecirc-default-qft-n-24-5-reps, code/bench/a2_runs.py

## 2026-10-24 15:35 UTC  A11 noisecirc default brickwork n=24 5 reps
- **Goal:** noisecirc bench/fixes dd4b8c8 (default) at the A6 points: brickwork, damping M=0.01/0.1/1, 1000 shots, 5 timed reps (the 2-rep runs had outliers at 10-30 ms)
- **Task:** A11
- **Method:** code/bench/gpurun a2_runs.py --circuits brickwork --qubits 24 --noise damping --ps 3.26797e-05,0.000326797,0.00326797 --shots 1000 --reps 5
- **Outcome:** exit 0; outputs in data/20261024-153535-a11-noisecirc-default-brickwork-n-24-5-reps
- **Next:** none
- **Refs:** data/20261024-153535-a11-noisecirc-default-brickwork-n-24-5-reps, code/bench/a2_runs.py

## 2026-10-24 15:35 UTC  A11 noisecirc default ghz n=24 5 reps
- **Goal:** noisecirc bench/fixes dd4b8c8 (default) at the A6 points: ghz, damping M=0.01/0.1/1, 1000 shots, 5 timed reps (the 2-rep runs had outliers at 10-30 ms)
- **Task:** A11
- **Method:** code/bench/gpurun a2_runs.py --circuits ghz --qubits 24 --noise damping --ps 0.000215054,0.00215054,0.0215054 --shots 1000 --reps 5
- **Outcome:** exit 0; outputs in data/20261024-153527-a11-noisecirc-default-ghz-n-24-5-reps
- **Next:** none
- **Refs:** data/20261024-153527-a11-noisecirc-default-ghz-n-24-5-reps, code/bench/a2_runs.py

## 2026-10-24 15:34 UTC  A11 noisecirc autotune brickwork n=28
- **Goal:** noisecirc bench/fixes dd4b8c8 (autotune) at the A6 28-qubit points: brickwork, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a2_runs.py --circuits brickwork --qubits 28 --noise damping --ps 2.42131e-05 --shots 1000 --reps 2 --option autotune=1
- **Outcome:** exit 0; outputs in data/20261024-153426-a11-noisecirc-autotune-brickwork-n-28
- **Next:** none
- **Refs:** data/20261024-153426-a11-noisecirc-autotune-brickwork-n-28, code/bench/a2_runs.py

## 2026-10-24 15:34 UTC  A11 noisecirc autotune qft n=28
- **Goal:** noisecirc bench/fixes dd4b8c8 (autotune) at the A6 28-qubit points: qft, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a2_runs.py --circuits qft --qubits 28 --noise damping --ps 2.46305e-05,0.000246305 --shots 1000 --reps 2 --option autotune=1
- **Outcome:** exit 0; outputs in data/20261024-153404-a11-noisecirc-autotune-qft-n-28
- **Next:** none
- **Refs:** data/20261024-153404-a11-noisecirc-autotune-qft-n-28, code/bench/a2_runs.py

## 2026-10-24 15:34 UTC  A11 noisecirc autotune qaoa n=28
- **Goal:** noisecirc bench/fixes dd4b8c8 (autotune) at the A6 28-qubit points: qaoa, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a2_runs.py --circuits qaoa --qubits 28 --noise damping --ps 4.7619e-05 --shots 1000 --reps 2 --option autotune=1
- **Outcome:** exit 0; outputs in data/20261024-153355-a11-noisecirc-autotune-qaoa-n-28
- **Next:** none
- **Refs:** data/20261024-153355-a11-noisecirc-autotune-qaoa-n-28, code/bench/a2_runs.py

## 2026-10-24 15:33 UTC  A11 noisecirc autotune ghz n=28
- **Goal:** noisecirc bench/fixes dd4b8c8 (autotune) at the A6 28-qubit points: ghz, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a2_runs.py --circuits ghz --qubits 28 --noise damping --ps 0.000183486 --shots 1000 --reps 2 --option autotune=1
- **Outcome:** exit 0; outputs in data/20261024-153350-a11-noisecirc-autotune-ghz-n-28
- **Next:** none
- **Refs:** data/20261024-153350-a11-noisecirc-autotune-ghz-n-28, code/bench/a2_runs.py

## 2026-10-24 15:33 UTC  A11 noisecirc default brickwork n=28
- **Goal:** noisecirc bench/fixes dd4b8c8 (default) at the A6 28-qubit points: brickwork, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a2_runs.py --circuits brickwork --qubits 28 --noise damping --ps 2.42131e-05 --shots 1000 --reps 2
- **Outcome:** exit 0; outputs in data/20261024-153342-a11-noisecirc-default-brickwork-n-28
- **Next:** none
- **Refs:** data/20261024-153342-a11-noisecirc-default-brickwork-n-28, code/bench/a2_runs.py

## 2026-10-24 15:33 UTC  A11 noisecirc default qft n=28
- **Goal:** noisecirc bench/fixes dd4b8c8 (default) at the A6 28-qubit points: qft, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a2_runs.py --circuits qft --qubits 28 --noise damping --ps 2.46305e-05,0.000246305 --shots 1000 --reps 2
- **Outcome:** exit 0; outputs in data/20261024-153324-a11-noisecirc-default-qft-n-28
- **Next:** none
- **Refs:** data/20261024-153324-a11-noisecirc-default-qft-n-28, code/bench/a2_runs.py

## 2026-10-24 15:33 UTC  A11 noisecirc default qaoa n=28
- **Goal:** noisecirc bench/fixes dd4b8c8 (default) at the A6 28-qubit points: qaoa, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a2_runs.py --circuits qaoa --qubits 28 --noise damping --ps 4.7619e-05 --shots 1000 --reps 2
- **Outcome:** exit 0; outputs in data/20261024-153318-a11-noisecirc-default-qaoa-n-28
- **Next:** none
- **Refs:** data/20261024-153318-a11-noisecirc-default-qaoa-n-28, code/bench/a2_runs.py

## 2026-10-24 15:33 UTC  A11 noisecirc default ghz n=28
- **Goal:** noisecirc bench/fixes dd4b8c8 (default) at the A6 28-qubit points: ghz, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a2_runs.py --circuits ghz --qubits 28 --noise damping --ps 0.000183486 --shots 1000 --reps 2
- **Outcome:** exit 0; outputs in data/20261024-153313-a11-noisecirc-default-ghz-n-28
- **Next:** none
- **Refs:** data/20261024-153313-a11-noisecirc-default-ghz-n-28, code/bench/a2_runs.py

## 2026-10-24 15:33 UTC  A11 aer_branch mq3 brickwork n=28
- **Goal:** Aer shot branching (mq3) at the A6 28-qubit points that ran: brickwork, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit brickwork --qubits 28 --noise damping --ps 2.42131e-05 --shots 1000 --reps 1 --budget 400 --aer-option fusion_max_qubit=3
- **Outcome:** exit 0; outputs in data/20261024-153248-a11-aer-branch-mq3-brickwork-n-28
- **Next:** none
- **Refs:** data/20261024-153248-a11-aer-branch-mq3-brickwork-n-28, code/bench/a6_runs.py

## 2026-10-24 15:32 UTC  A11 aer_branch mq3 qft n=28
- **Goal:** Aer shot branching (mq3) at the A6 28-qubit points that ran: qft, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit qft --qubits 28 --noise damping --ps 2.46305e-05,0.000246305 --shots 1000 --reps 1 --budget 400 --aer-option fusion_max_qubit=3
- **Outcome:** exit 0; outputs in data/20261024-153050-a11-aer-branch-mq3-qft-n-28
- **Next:** none
- **Refs:** data/20261024-153050-a11-aer-branch-mq3-qft-n-28, code/bench/a6_runs.py

## 2026-10-24 15:30 UTC  A11 aer_branch mq3 qaoa n=28
- **Goal:** Aer shot branching (mq3) at the A6 28-qubit points that ran: qaoa, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit qaoa --qubits 28 --noise damping --ps 4.7619e-05 --shots 1000 --reps 1 --budget 400 --aer-option fusion_max_qubit=3
- **Outcome:** exit 0; outputs in data/20261024-153035-a11-aer-branch-mq3-qaoa-n-28
- **Next:** none
- **Refs:** data/20261024-153035-a11-aer-branch-mq3-qaoa-n-28, code/bench/a6_runs.py

## 2026-10-24 15:30 UTC  A11 aer_branch mq3 ghz n=28
- **Goal:** Aer shot branching (mq3) at the A6 28-qubit points that ran: ghz, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit ghz --qubits 28 --noise damping --ps 0.000183486 --shots 1000 --reps 1 --budget 400 --aer-option fusion_max_qubit=3
- **Outcome:** exit 0; outputs in data/20261024-153026-a11-aer-branch-mq3-ghz-n-28
- **Next:** none
- **Refs:** data/20261024-153026-a11-aer-branch-mq3-ghz-n-28, code/bench/a6_runs.py

## 2026-10-24 15:30 UTC  A11 aer_branch default brickwork n=28
- **Goal:** Aer shot branching (default) at the A6 28-qubit points that ran: brickwork, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit brickwork --qubits 28 --noise damping --ps 2.42131e-05 --shots 1000 --reps 1 --budget 400
- **Outcome:** exit 0; outputs in data/20261024-153001-a11-aer-branch-default-brickwork-n-28
- **Next:** none
- **Refs:** data/20261024-153001-a11-aer-branch-default-brickwork-n-28, code/bench/a6_runs.py

## 2026-10-24 15:30 UTC  A11 aer_branch default qft n=28
- **Goal:** Aer shot branching (default) at the A6 28-qubit points that ran: qft, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit qft --qubits 28 --noise damping --ps 2.46305e-05 --shots 1000 --reps 1 --budget 400
- **Outcome:** exit 0; outputs in data/20261024-152936-a11-aer-branch-default-qft-n-28
- **Next:** none
- **Refs:** data/20261024-152936-a11-aer-branch-default-qft-n-28, code/bench/a6_runs.py

## 2026-10-24 15:29 UTC  A11 aer_branch default qaoa n=28
- **Goal:** Aer shot branching (default) at the A6 28-qubit points that ran: qaoa, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit qaoa --qubits 28 --noise damping --ps 4.7619e-05 --shots 1000 --reps 1 --budget 400
- **Outcome:** exit 0; outputs in data/20261024-152922-a11-aer-branch-default-qaoa-n-28
- **Next:** none
- **Refs:** data/20261024-152922-a11-aer-branch-default-qaoa-n-28, code/bench/a6_runs.py

## 2026-10-24 15:29 UTC  A11 aer_branch default ghz n=28
- **Goal:** Aer shot branching (default) at the A6 28-qubit points that ran: ghz, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit ghz --qubits 28 --noise damping --ps 0.000183486 --shots 1000 --reps 1 --budget 400
- **Outcome:** exit 0; outputs in data/20261024-152912-a11-aer-branch-default-ghz-n-28
- **Next:** none
- **Refs:** data/20261024-152912-a11-aer-branch-default-ghz-n-28, code/bench/a6_runs.py

## 2026-10-24 15:29 UTC  A11 noisecirc autotune qaoa n=24
- **Goal:** noisecirc bench/fixes dd4b8c8 (autotune) at the A6 points: qaoa, damping M=0.01/0.1/1, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a2_runs.py --circuits qaoa --qubits 24 --noise damping --ps 5.55556e-05,0.000555556,0.00555556 --shots 1000 --reps 2 --option autotune=1
- **Outcome:** exit 0; outputs in data/20261024-152857-a11-noisecirc-autotune-qaoa-n-24
- **Next:** none
- **Refs:** data/20261024-152857-a11-noisecirc-autotune-qaoa-n-24, code/bench/a2_runs.py

## 2026-10-24 15:28 UTC  A11 noisecirc autotune qft n=24
- **Goal:** noisecirc bench/fixes dd4b8c8 (autotune) at the A6 points: qft, damping M=0.01/0.1/1, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a2_runs.py --circuits qft --qubits 24 --noise damping --ps 3.33333e-05,0.000333333,0.00333333 --shots 1000 --reps 2 --option autotune=1
- **Outcome:** exit 0; outputs in data/20261024-152838-a11-noisecirc-autotune-qft-n-24
- **Next:** none
- **Refs:** data/20261024-152838-a11-noisecirc-autotune-qft-n-24, code/bench/a2_runs.py

## 2026-10-24 15:28 UTC  A11 noisecirc autotune brickwork n=24
- **Goal:** noisecirc bench/fixes dd4b8c8 (autotune) at the A6 points: brickwork, damping M=0.01/0.1/1, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a2_runs.py --circuits brickwork --qubits 24 --noise damping --ps 3.26797e-05,0.000326797,0.00326797 --shots 1000 --reps 2 --option autotune=1
- **Outcome:** exit 0; outputs in data/20261024-152805-a11-noisecirc-autotune-brickwork-n-24
- **Next:** none
- **Refs:** data/20261024-152805-a11-noisecirc-autotune-brickwork-n-24, code/bench/a2_runs.py

## 2026-10-24 15:28 UTC  A11 noisecirc autotune ghz n=24
- **Goal:** noisecirc bench/fixes dd4b8c8 (autotune) at the A6 points: ghz, damping M=0.01/0.1/1, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a2_runs.py --circuits ghz --qubits 24 --noise damping --ps 0.000215054,0.00215054,0.0215054 --shots 1000 --reps 2 --option autotune=1
- **Outcome:** exit 0; outputs in data/20261024-152758-a11-noisecirc-autotune-ghz-n-24
- **Next:** none
- **Refs:** data/20261024-152758-a11-noisecirc-autotune-ghz-n-24, code/bench/a2_runs.py

## 2026-10-24 15:27 UTC  A11 noisecirc default qaoa n=24
- **Goal:** noisecirc bench/fixes dd4b8c8 (default) at the A6 points: qaoa, damping M=0.01/0.1/1, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a2_runs.py --circuits qaoa --qubits 24 --noise damping --ps 5.55556e-05,0.000555556,0.00555556 --shots 1000 --reps 2
- **Outcome:** exit 0; outputs in data/20261024-152747-a11-noisecirc-default-qaoa-n-24
- **Next:** none
- **Refs:** data/20261024-152747-a11-noisecirc-default-qaoa-n-24, code/bench/a2_runs.py

## 2026-10-24 15:27 UTC  A11 noisecirc default qft n=24
- **Goal:** noisecirc bench/fixes dd4b8c8 (default) at the A6 points: qft, damping M=0.01/0.1/1, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a2_runs.py --circuits qft --qubits 24 --noise damping --ps 3.33333e-05,0.000333333,0.00333333 --shots 1000 --reps 2
- **Outcome:** exit 0; outputs in data/20261024-152733-a11-noisecirc-default-qft-n-24
- **Next:** none
- **Refs:** data/20261024-152733-a11-noisecirc-default-qft-n-24, code/bench/a2_runs.py

## 2026-10-24 15:27 UTC  A11 noisecirc default brickwork n=24
- **Goal:** noisecirc bench/fixes dd4b8c8 (default) at the A6 points: brickwork, damping M=0.01/0.1/1, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a2_runs.py --circuits brickwork --qubits 24 --noise damping --ps 3.26797e-05,0.000326797,0.00326797 --shots 1000 --reps 2
- **Outcome:** exit 0; outputs in data/20261024-152715-a11-noisecirc-default-brickwork-n-24
- **Next:** none
- **Refs:** data/20261024-152715-a11-noisecirc-default-brickwork-n-24, code/bench/a2_runs.py

## 2026-10-24 15:27 UTC  A11 noisecirc default ghz n=24
- **Goal:** noisecirc bench/fixes dd4b8c8 (default) at the A6 points: ghz, damping M=0.01/0.1/1, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a2_runs.py --circuits ghz --qubits 24 --noise damping --ps 0.000215054,0.00215054,0.0215054 --shots 1000 --reps 2
- **Outcome:** exit 0; outputs in data/20261024-152708-a11-noisecirc-default-ghz-n-24
- **Next:** none
- **Refs:** data/20261024-152708-a11-noisecirc-default-ghz-n-24, code/bench/a2_runs.py

## 2026-10-24 15:27 UTC  A11 aer_branch mq4-cf3 qaoa n=24
- **Goal:** Aer shot branching with fusion_max_qubit=4 fusion_cost_factor=3.0 on qaoa, damping M=0.01/0.1/1, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit qaoa --qubits 24 --noise damping --ps 5.55556e-05,0.000555556,0.00555556 --shots 1000 --reps 2 --aer-option fusion_max_qubit=4 --aer-option fusion_cost_factor=3.0
- **Outcome:** exit 0; outputs in data/20261024-152624-a11-aer-branch-mq4-cf3-qaoa-n-24
- **Next:** none
- **Refs:** data/20261024-152624-a11-aer-branch-mq4-cf3-qaoa-n-24, code/bench/a6_runs.py

## 2026-10-24 15:26 UTC  A11 aer_branch mq4-cf3 qft n=24
- **Goal:** Aer shot branching with fusion_max_qubit=4 fusion_cost_factor=3.0 on qft, damping M=0.01/0.1/1, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit qft --qubits 24 --noise damping --ps 3.33333e-05,0.000333333,0.00333333 --shots 1000 --reps 2 --aer-option fusion_max_qubit=4 --aer-option fusion_cost_factor=3.0
- **Outcome:** exit 0; outputs in data/20261024-152458-a11-aer-branch-mq4-cf3-qft-n-24
- **Next:** none
- **Refs:** data/20261024-152458-a11-aer-branch-mq4-cf3-qft-n-24, code/bench/a6_runs.py

## 2026-10-24 15:24 UTC  A11 aer_branch mq4-cf3 brickwork n=24
- **Goal:** Aer shot branching with fusion_max_qubit=4 fusion_cost_factor=3.0 on brickwork, damping M=0.01/0.1/1, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit brickwork --qubits 24 --noise damping --ps 3.26797e-05,0.000326797,0.00326797 --shots 1000 --reps 2 --aer-option fusion_max_qubit=4 --aer-option fusion_cost_factor=3.0
- **Outcome:** exit 0; outputs in data/20261024-152302-a11-aer-branch-mq4-cf3-brickwork-n-24
- **Next:** none
- **Refs:** data/20261024-152302-a11-aer-branch-mq4-cf3-brickwork-n-24, code/bench/a6_runs.py

## 2026-10-24 15:23 UTC  A11 aer_branch mq4-cf3 ghz n=24
- **Goal:** Aer shot branching with fusion_max_qubit=4 fusion_cost_factor=3.0 on ghz, damping M=0.01/0.1/1, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit ghz --qubits 24 --noise damping --ps 0.000215054,0.00215054,0.0215054 --shots 1000 --reps 2 --aer-option fusion_max_qubit=4 --aer-option fusion_cost_factor=3.0
- **Outcome:** exit 0; outputs in data/20261024-152244-a11-aer-branch-mq4-cf3-ghz-n-24
- **Next:** none
- **Refs:** data/20261024-152244-a11-aer-branch-mq4-cf3-ghz-n-24, code/bench/a6_runs.py

## 2026-10-24 15:22 UTC  A11 aer_branch mq3-cf3 qaoa n=24
- **Goal:** Aer shot branching with fusion_max_qubit=3 fusion_cost_factor=3.0 on qaoa, damping M=0.01/0.1/1, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit qaoa --qubits 24 --noise damping --ps 5.55556e-05,0.000555556,0.00555556 --shots 1000 --reps 2 --aer-option fusion_max_qubit=3 --aer-option fusion_cost_factor=3.0
- **Outcome:** exit 0; outputs in data/20261024-152200-a11-aer-branch-mq3-cf3-qaoa-n-24
- **Next:** none
- **Refs:** data/20261024-152200-a11-aer-branch-mq3-cf3-qaoa-n-24, code/bench/a6_runs.py

## 2026-10-24 15:22 UTC  A11 aer_branch mq3-cf3 qft n=24
- **Goal:** Aer shot branching with fusion_max_qubit=3 fusion_cost_factor=3.0 on qft, damping M=0.01/0.1/1, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit qft --qubits 24 --noise damping --ps 3.33333e-05,0.000333333,0.00333333 --shots 1000 --reps 2 --aer-option fusion_max_qubit=3 --aer-option fusion_cost_factor=3.0
- **Outcome:** exit 0; outputs in data/20261024-152034-a11-aer-branch-mq3-cf3-qft-n-24
- **Next:** none
- **Refs:** data/20261024-152034-a11-aer-branch-mq3-cf3-qft-n-24, code/bench/a6_runs.py

## 2026-10-24 15:20 UTC  A11 aer_branch mq3-cf3 brickwork n=24
- **Goal:** Aer shot branching with fusion_max_qubit=3 fusion_cost_factor=3.0 on brickwork, damping M=0.01/0.1/1, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit brickwork --qubits 24 --noise damping --ps 3.26797e-05,0.000326797,0.00326797 --shots 1000 --reps 2 --aer-option fusion_max_qubit=3 --aer-option fusion_cost_factor=3.0
- **Outcome:** exit 0; outputs in data/20261024-151839-a11-aer-branch-mq3-cf3-brickwork-n-24
- **Next:** none
- **Refs:** data/20261024-151839-a11-aer-branch-mq3-cf3-brickwork-n-24, code/bench/a6_runs.py

## 2026-10-24 15:18 UTC  A11 aer_branch mq3-cf3 ghz n=24
- **Goal:** Aer shot branching with fusion_max_qubit=3 fusion_cost_factor=3.0 on ghz, damping M=0.01/0.1/1, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit ghz --qubits 24 --noise damping --ps 0.000215054,0.00215054,0.0215054 --shots 1000 --reps 2 --aer-option fusion_max_qubit=3 --aer-option fusion_cost_factor=3.0
- **Outcome:** exit 0; outputs in data/20261024-151821-a11-aer-branch-mq3-cf3-ghz-n-24
- **Next:** none
- **Refs:** data/20261024-151821-a11-aer-branch-mq3-cf3-ghz-n-24, code/bench/a6_runs.py

## 2026-10-24 15:17 UTC  A11 aer_branch cf3 qaoa n=24
- **Goal:** Aer shot branching with fusion_cost_factor=3.0 on qaoa, damping M=0.01/0.1/1, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit qaoa --qubits 24 --noise damping --ps 5.55556e-05,0.000555556,0.00555556 --shots 1000 --reps 2 --aer-option fusion_cost_factor=3.0
- **Outcome:** exit 0; outputs in data/20261024-151639-a11-aer-branch-cf3-qaoa-n-24
- **Next:** none
- **Refs:** data/20261024-151639-a11-aer-branch-cf3-qaoa-n-24, code/bench/a6_runs.py

## 2026-10-24 15:16 UTC  A11 aer_branch cf3 qft n=24
- **Goal:** Aer shot branching with fusion_cost_factor=3.0 on qft, damping M=0.01/0.1/1, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit qft --qubits 24 --noise damping --ps 3.33333e-05,0.000333333,0.00333333 --shots 1000 --reps 2 --aer-option fusion_cost_factor=3.0
- **Outcome:** exit 0; outputs in data/20261024-151512-a11-aer-branch-cf3-qft-n-24
- **Next:** none
- **Refs:** data/20261024-151512-a11-aer-branch-cf3-qft-n-24, code/bench/a6_runs.py

## 2026-10-24 15:15 UTC  A11 aer_branch cf3 brickwork n=24
- **Goal:** Aer shot branching with fusion_cost_factor=3.0 on brickwork, damping M=0.01/0.1/1, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit brickwork --qubits 24 --noise damping --ps 3.26797e-05,0.000326797,0.00326797 --shots 1000 --reps 2 --aer-option fusion_cost_factor=3.0
- **Outcome:** exit 0; outputs in data/20261024-151316-a11-aer-branch-cf3-brickwork-n-24
- **Next:** none
- **Refs:** data/20261024-151316-a11-aer-branch-cf3-brickwork-n-24, code/bench/a6_runs.py

## 2026-10-24 15:13 UTC  A11 aer_branch cf3 ghz n=24
- **Goal:** Aer shot branching with fusion_cost_factor=3.0 on ghz, damping M=0.01/0.1/1, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit ghz --qubits 24 --noise damping --ps 0.000215054,0.00215054,0.0215054 --shots 1000 --reps 2 --aer-option fusion_cost_factor=3.0
- **Outcome:** exit 0; outputs in data/20261024-151259-a11-aer-branch-cf3-ghz-n-24
- **Next:** none
- **Refs:** data/20261024-151259-a11-aer-branch-cf3-ghz-n-24, code/bench/a6_runs.py

## 2026-10-24 15:12 UTC  A11 aer_branch cf1.2 qaoa n=24
- **Goal:** Aer shot branching with fusion_cost_factor=1.2 on qaoa, damping M=0.01/0.1/1, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit qaoa --qubits 24 --noise damping --ps 5.55556e-05,0.000555556,0.00555556 --shots 1000 --reps 2 --aer-option fusion_cost_factor=1.2
- **Outcome:** exit 0; outputs in data/20261024-151215-a11-aer-branch-cf1-2-qaoa-n-24
- **Next:** none
- **Refs:** data/20261024-151215-a11-aer-branch-cf1-2-qaoa-n-24, code/bench/a6_runs.py

## 2026-10-24 15:12 UTC  A11 aer_branch cf1.2 qft n=24
- **Goal:** Aer shot branching with fusion_cost_factor=1.2 on qft, damping M=0.01/0.1/1, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit qft --qubits 24 --noise damping --ps 3.33333e-05,0.000333333,0.00333333 --shots 1000 --reps 2 --aer-option fusion_cost_factor=1.2
- **Outcome:** exit 0; outputs in data/20261024-151049-a11-aer-branch-cf1-2-qft-n-24
- **Next:** none
- **Refs:** data/20261024-151049-a11-aer-branch-cf1-2-qft-n-24, code/bench/a6_runs.py

## 2026-10-24 15:10 UTC  A11 aer_branch cf1.2 brickwork n=24
- **Goal:** Aer shot branching with fusion_cost_factor=1.2 on brickwork, damping M=0.01/0.1/1, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit brickwork --qubits 24 --noise damping --ps 3.26797e-05,0.000326797,0.00326797 --shots 1000 --reps 2 --aer-option fusion_cost_factor=1.2
- **Outcome:** exit 0; outputs in data/20261024-150856-a11-aer-branch-cf1-2-brickwork-n-24
- **Next:** none
- **Refs:** data/20261024-150856-a11-aer-branch-cf1-2-brickwork-n-24, code/bench/a6_runs.py

## 2026-10-24 15:08 UTC  A11 aer_branch cf1.2 ghz n=24
- **Goal:** Aer shot branching with fusion_cost_factor=1.2 on ghz, damping M=0.01/0.1/1, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit ghz --qubits 24 --noise damping --ps 0.000215054,0.00215054,0.0215054 --shots 1000 --reps 2 --aer-option fusion_cost_factor=1.2
- **Outcome:** exit 0; outputs in data/20261024-150838-a11-aer-branch-cf1-2-ghz-n-24
- **Next:** none
- **Refs:** data/20261024-150838-a11-aer-branch-cf1-2-ghz-n-24, code/bench/a6_runs.py

## 2026-10-24 15:08 UTC  A11 aer_branch nosampling qaoa n=24
- **Goal:** Aer shot branching with shot_branching_sampling_enable=False on qaoa, damping M=0.01/0.1/1, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit qaoa --qubits 24 --noise damping --ps 5.55556e-05,0.000555556,0.00555556 --shots 1000 --reps 2 --aer-option shot_branching_sampling_enable=False
- **Outcome:** exit 0; outputs in data/20261024-150544-a11-aer-branch-nosampling-qaoa-n-24
- **Next:** none
- **Refs:** data/20261024-150544-a11-aer-branch-nosampling-qaoa-n-24, code/bench/a6_runs.py

## 2026-10-24 15:05 UTC  A11 aer_branch nosampling qft n=24
- **Goal:** Aer shot branching with shot_branching_sampling_enable=False on qft, damping M=0.01/0.1/1, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit qft --qubits 24 --noise damping --ps 3.33333e-05,0.000333333,0.00333333 --shots 1000 --reps 2 --aer-option shot_branching_sampling_enable=False
- **Outcome:** exit 0; outputs in data/20261024-150215-a11-aer-branch-nosampling-qft-n-24
- **Next:** none
- **Refs:** data/20261024-150215-a11-aer-branch-nosampling-qft-n-24, code/bench/a6_runs.py

## 2026-10-24 15:02 UTC  A11 aer_branch nosampling brickwork n=24
- **Goal:** Aer shot branching with shot_branching_sampling_enable=False on brickwork, damping M=0.01/0.1/1, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit brickwork --qubits 24 --noise damping --ps 3.26797e-05,0.000326797,0.00326797 --shots 1000 --reps 2 --aer-option shot_branching_sampling_enable=False
- **Outcome:** exit 0; outputs in data/20261024-145723-a11-aer-branch-nosampling-brickwork-n-24
- **Next:** none
- **Refs:** data/20261024-145723-a11-aer-branch-nosampling-brickwork-n-24, code/bench/a6_runs.py

## 2026-10-24 14:57 UTC  A11 aer_branch nosampling ghz n=24
- **Goal:** Aer shot branching with shot_branching_sampling_enable=False on ghz, damping M=0.01/0.1/1, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit ghz --qubits 24 --noise damping --ps 0.000215054,0.00215054,0.0215054 --shots 1000 --reps 2 --aer-option shot_branching_sampling_enable=False
- **Outcome:** exit 0; outputs in data/20261024-145657-a11-aer-branch-nosampling-ghz-n-24
- **Next:** none
- **Refs:** data/20261024-145657-a11-aer-branch-nosampling-ghz-n-24, code/bench/a6_runs.py

## 2026-10-24 14:56 UTC  A11 aer_branch nofusion qaoa n=24
- **Goal:** Aer shot branching with fusion_enable=False on qaoa, damping M=0.01/0.1/1, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit qaoa --qubits 24 --noise damping --ps 5.55556e-05,0.000555556,0.00555556 --shots 1000 --reps 2 --aer-option fusion_enable=False
- **Outcome:** exit 0; outputs in data/20261024-145445-a11-aer-branch-nofusion-qaoa-n-24
- **Next:** none
- **Refs:** data/20261024-145445-a11-aer-branch-nofusion-qaoa-n-24, code/bench/a6_runs.py

## 2026-10-24 14:54 UTC  A11 aer_branch nofusion qft n=24
- **Goal:** Aer shot branching with fusion_enable=False on qft, damping M=0.01/0.1/1, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit qft --qubits 24 --noise damping --ps 3.33333e-05,0.000333333,0.00333333 --shots 1000 --reps 2 --aer-option fusion_enable=False
- **Outcome:** exit 0; outputs in data/20261024-145256-a11-aer-branch-nofusion-qft-n-24
- **Next:** none
- **Refs:** data/20261024-145256-a11-aer-branch-nofusion-qft-n-24, code/bench/a6_runs.py

## 2026-10-24 14:52 UTC  A11 aer_branch nofusion brickwork n=24
- **Goal:** Aer shot branching with fusion_enable=False on brickwork, damping M=0.01/0.1/1, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit brickwork --qubits 24 --noise damping --ps 3.26797e-05,0.000326797,0.00326797 --shots 1000 --reps 2 --aer-option fusion_enable=False
- **Outcome:** exit 0; outputs in data/20261024-145101-a11-aer-branch-nofusion-brickwork-n-24
- **Next:** none
- **Refs:** data/20261024-145101-a11-aer-branch-nofusion-brickwork-n-24, code/bench/a6_runs.py

## 2026-10-24 14:51 UTC  A11 aer_branch nofusion ghz n=24
- **Goal:** Aer shot branching with fusion_enable=False on ghz, damping M=0.01/0.1/1, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit ghz --qubits 24 --noise damping --ps 0.000215054,0.00215054,0.0215054 --shots 1000 --reps 2 --aer-option fusion_enable=False
- **Outcome:** exit 0; outputs in data/20261024-145031-a11-aer-branch-nofusion-ghz-n-24
- **Next:** none
- **Refs:** data/20261024-145031-a11-aer-branch-nofusion-ghz-n-24, code/bench/a6_runs.py

## 2026-10-24 14:50 UTC  A11 aer_branch mq5 qaoa n=24
- **Goal:** Aer shot branching with fusion_max_qubit=5 on qaoa, damping M=0.01/0.1/1, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit qaoa --qubits 24 --noise damping --ps 5.55556e-05,0.000555556,0.00555556 --shots 1000 --reps 2 --aer-option fusion_max_qubit=5
- **Outcome:** exit 0; outputs in data/20261024-144951-a11-aer-branch-mq5-qaoa-n-24
- **Next:** none
- **Refs:** data/20261024-144951-a11-aer-branch-mq5-qaoa-n-24, code/bench/a6_runs.py

## 2026-10-24 14:49 UTC  A11 aer_branch mq5 qft n=24
- **Goal:** Aer shot branching with fusion_max_qubit=5 on qft, damping M=0.01/0.1/1, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit qft --qubits 24 --noise damping --ps 3.33333e-05,0.000333333,0.00333333 --shots 1000 --reps 2 --aer-option fusion_max_qubit=5
- **Outcome:** exit 0; outputs in data/20261024-144807-a11-aer-branch-mq5-qft-n-24
- **Next:** none
- **Refs:** data/20261024-144807-a11-aer-branch-mq5-qft-n-24, code/bench/a6_runs.py

## 2026-10-24 14:48 UTC  A11 aer_branch mq5 brickwork n=24
- **Goal:** Aer shot branching with fusion_max_qubit=5 on brickwork, damping M=0.01/0.1/1, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit brickwork --qubits 24 --noise damping --ps 3.26797e-05,0.000326797,0.00326797 --shots 1000 --reps 2 --aer-option fusion_max_qubit=5
- **Outcome:** exit 0; outputs in data/20261024-144621-a11-aer-branch-mq5-brickwork-n-24
- **Next:** none
- **Refs:** data/20261024-144621-a11-aer-branch-mq5-brickwork-n-24, code/bench/a6_runs.py

## 2026-10-24 14:46 UTC  A11 aer_branch mq5 ghz n=24
- **Goal:** Aer shot branching with fusion_max_qubit=5 on ghz, damping M=0.01/0.1/1, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit ghz --qubits 24 --noise damping --ps 0.000215054,0.00215054,0.0215054 --shots 1000 --reps 2 --aer-option fusion_max_qubit=5
- **Outcome:** exit 0; outputs in data/20261024-144604-a11-aer-branch-mq5-ghz-n-24
- **Next:** none
- **Refs:** data/20261024-144604-a11-aer-branch-mq5-ghz-n-24, code/bench/a6_runs.py

## 2026-10-24 14:46 UTC  A11 aer_branch mq4 qaoa n=24
- **Goal:** Aer shot branching with fusion_max_qubit=4 on qaoa, damping M=0.01/0.1/1, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit qaoa --qubits 24 --noise damping --ps 5.55556e-05,0.000555556,0.00555556 --shots 1000 --reps 2 --aer-option fusion_max_qubit=4
- **Outcome:** exit 0; outputs in data/20261024-144524-a11-aer-branch-mq4-qaoa-n-24
- **Next:** none
- **Refs:** data/20261024-144524-a11-aer-branch-mq4-qaoa-n-24, code/bench/a6_runs.py

## 2026-10-24 14:45 UTC  A11 aer_branch mq4 qft n=24
- **Goal:** Aer shot branching with fusion_max_qubit=4 on qft, damping M=0.01/0.1/1, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit qft --qubits 24 --noise damping --ps 3.33333e-05,0.000333333,0.00333333 --shots 1000 --reps 2 --aer-option fusion_max_qubit=4
- **Outcome:** exit 0; outputs in data/20261024-144414-a11-aer-branch-mq4-qft-n-24
- **Next:** none
- **Refs:** data/20261024-144414-a11-aer-branch-mq4-qft-n-24, code/bench/a6_runs.py

## 2026-10-24 14:44 UTC  A11 aer_branch mq4 brickwork n=24
- **Goal:** Aer shot branching with fusion_max_qubit=4 on brickwork, damping M=0.01/0.1/1, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit brickwork --qubits 24 --noise damping --ps 3.26797e-05,0.000326797,0.00326797 --shots 1000 --reps 2 --aer-option fusion_max_qubit=4
- **Outcome:** exit 0; outputs in data/20261024-144228-a11-aer-branch-mq4-brickwork-n-24
- **Next:** none
- **Refs:** data/20261024-144228-a11-aer-branch-mq4-brickwork-n-24, code/bench/a6_runs.py

## 2026-10-24 14:42 UTC  A11 aer_branch mq4 ghz n=24
- **Goal:** Aer shot branching with fusion_max_qubit=4 on ghz, damping M=0.01/0.1/1, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit ghz --qubits 24 --noise damping --ps 0.000215054,0.00215054,0.0215054 --shots 1000 --reps 2 --aer-option fusion_max_qubit=4
- **Outcome:** exit 0; outputs in data/20261024-144211-a11-aer-branch-mq4-ghz-n-24
- **Next:** none
- **Refs:** data/20261024-144211-a11-aer-branch-mq4-ghz-n-24, code/bench/a6_runs.py

## 2026-10-24 14:42 UTC  A11 aer_branch mq3 qaoa n=24
- **Goal:** Aer shot branching with fusion_max_qubit=3 on qaoa, damping M=0.01/0.1/1, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit qaoa --qubits 24 --noise damping --ps 5.55556e-05,0.000555556,0.00555556 --shots 1000 --reps 2 --aer-option fusion_max_qubit=3
- **Outcome:** exit 0; outputs in data/20261024-144131-a11-aer-branch-mq3-qaoa-n-24
- **Next:** none
- **Refs:** data/20261024-144131-a11-aer-branch-mq3-qaoa-n-24, code/bench/a6_runs.py

## 2026-10-24 14:41 UTC  A11 aer_branch mq3 qft n=24
- **Goal:** Aer shot branching with fusion_max_qubit=3 on qft, damping M=0.01/0.1/1, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit qft --qubits 24 --noise damping --ps 3.33333e-05,0.000333333,0.00333333 --shots 1000 --reps 2 --aer-option fusion_max_qubit=3
- **Outcome:** exit 0; outputs in data/20261024-144022-a11-aer-branch-mq3-qft-n-24
- **Next:** none
- **Refs:** data/20261024-144022-a11-aer-branch-mq3-qft-n-24, code/bench/a6_runs.py

## 2026-10-24 14:40 UTC  A11 aer_branch mq3 brickwork n=24
- **Goal:** Aer shot branching with fusion_max_qubit=3 on brickwork, damping M=0.01/0.1/1, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit brickwork --qubits 24 --noise damping --ps 3.26797e-05,0.000326797,0.00326797 --shots 1000 --reps 2 --aer-option fusion_max_qubit=3
- **Outcome:** exit 0; outputs in data/20261024-143838-a11-aer-branch-mq3-brickwork-n-24
- **Next:** none
- **Refs:** data/20261024-143838-a11-aer-branch-mq3-brickwork-n-24, code/bench/a6_runs.py

## 2026-10-24 14:38 UTC  A11 aer_branch mq3 ghz n=24
- **Goal:** Aer shot branching with fusion_max_qubit=3 on ghz, damping M=0.01/0.1/1, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit ghz --qubits 24 --noise damping --ps 0.000215054,0.00215054,0.0215054 --shots 1000 --reps 2 --aer-option fusion_max_qubit=3
- **Outcome:** exit 0; outputs in data/20261024-143820-a11-aer-branch-mq3-ghz-n-24
- **Next:** none
- **Refs:** data/20261024-143820-a11-aer-branch-mq3-ghz-n-24, code/bench/a6_runs.py

## 2026-10-24 14:38 UTC  A11 aer_branch mq1 qaoa n=24
- **Goal:** Aer shot branching with fusion_max_qubit=1 on qaoa, damping M=0.01/0.1/1, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit qaoa --qubits 24 --noise damping --ps 5.55556e-05,0.000555556,0.00555556 --shots 1000 --reps 2 --aer-option fusion_max_qubit=1
- **Outcome:** exit 0; outputs in data/20261024-143651-a11-aer-branch-mq1-qaoa-n-24
- **Next:** none
- **Refs:** data/20261024-143651-a11-aer-branch-mq1-qaoa-n-24, code/bench/a6_runs.py

## 2026-10-24 14:36 UTC  A11 aer_branch mq1 qft n=24
- **Goal:** Aer shot branching with fusion_max_qubit=1 on qft, damping M=0.01/0.1/1, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit qft --qubits 24 --noise damping --ps 3.33333e-05,0.000333333,0.00333333 --shots 1000 --reps 2 --aer-option fusion_max_qubit=1
- **Outcome:** exit 0; outputs in data/20261024-143511-a11-aer-branch-mq1-qft-n-24
- **Next:** none
- **Refs:** data/20261024-143511-a11-aer-branch-mq1-qft-n-24, code/bench/a6_runs.py

## 2026-10-24 14:35 UTC  A11 aer_branch mq1 brickwork n=24
- **Goal:** Aer shot branching with fusion_max_qubit=1 on brickwork, damping M=0.01/0.1/1, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit brickwork --qubits 24 --noise damping --ps 3.26797e-05,0.000326797,0.00326797 --shots 1000 --reps 2 --aer-option fusion_max_qubit=1
- **Outcome:** exit 0; outputs in data/20261024-143149-a11-aer-branch-mq1-brickwork-n-24
- **Next:** none
- **Refs:** data/20261024-143149-a11-aer-branch-mq1-brickwork-n-24, code/bench/a6_runs.py

## 2026-10-24 14:31 UTC  A11 aer_branch mq1 ghz n=24
- **Goal:** Aer shot branching with fusion_max_qubit=1 on ghz, damping M=0.01/0.1/1, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit ghz --qubits 24 --noise damping --ps 0.000215054,0.00215054,0.0215054 --shots 1000 --reps 2 --aer-option fusion_max_qubit=1
- **Outcome:** exit 0; outputs in data/20261024-143122-a11-aer-branch-mq1-ghz-n-24
- **Next:** none
- **Refs:** data/20261024-143122-a11-aer-branch-mq1-ghz-n-24, code/bench/a6_runs.py

## 2026-10-24 14:31 UTC  A11 aer_branch default qaoa n=24
- **Goal:** Aer shot branching with defaults on qaoa, damping M=0.01/0.1/1, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit qaoa --qubits 24 --noise damping --ps 5.55556e-05,0.000555556,0.00555556 --shots 1000 --reps 2
- **Outcome:** exit 0; outputs in data/20261024-143040-a11-aer-branch-default-qaoa-n-24
- **Next:** none
- **Refs:** data/20261024-143040-a11-aer-branch-default-qaoa-n-24, code/bench/a6_runs.py

## 2026-10-24 14:30 UTC  A11 aer_branch default qft n=24
- **Goal:** Aer shot branching with defaults on qft, damping M=0.01/0.1/1, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit qft --qubits 24 --noise damping --ps 3.33333e-05,0.000333333,0.00333333 --shots 1000 --reps 2
- **Outcome:** exit 0; outputs in data/20261024-142913-a11-aer-branch-default-qft-n-24
- **Next:** none
- **Refs:** data/20261024-142913-a11-aer-branch-default-qft-n-24, code/bench/a6_runs.py

## 2026-10-24 14:29 UTC  A11 aer_branch default brickwork n=24
- **Goal:** Aer shot branching with defaults on brickwork, damping M=0.01/0.1/1, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit brickwork --qubits 24 --noise damping --ps 3.26797e-05,0.000326797,0.00326797 --shots 1000 --reps 2
- **Outcome:** exit 0; outputs in data/20261024-142716-a11-aer-branch-default-brickwork-n-24
- **Next:** none
- **Refs:** data/20261024-142716-a11-aer-branch-default-brickwork-n-24, code/bench/a6_runs.py

## 2026-10-24 14:27 UTC  A11 aer_branch default ghz n=24
- **Goal:** Aer shot branching with defaults on ghz, damping M=0.01/0.1/1, 1000 shots
- **Task:** A11
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit ghz --qubits 24 --noise damping --ps 0.000215054,0.00215054,0.0215054 --shots 1000 --reps 2
- **Outcome:** exit 0; outputs in data/20261024-142659-a11-aer-branch-default-ghz-n-24
- **Next:** none
- **Refs:** data/20261024-142659-a11-aer-branch-default-ghz-n-24, code/bench/a6_runs.py

## 2026-10-24 10:41 UTC  A8 figure
- **Goal:** Record the A8 analysis figure
- **Task:** A8
- **Method:** code/bench/a8_plot.py: per-block kernel ratios (dominant, general, masked) and masked/general run-time ratios
- **Outcome:** data/a8-analysis/masked.svg, used by wiki/studies/error-kernels.md
- **Next:** none
- **Refs:** data/a8-analysis

## 2026-10-24 10:40 UTC  A8 autotuning: implementation and runs
- **Goal:** Choose block size and stage width per circuit now that error passes cost about a dominant pass
- **Task:** A8
- **Method:** noisecirc feature/autotune 60913e8 (Simulator(stage_qubits), Simulator(autotune) over max_operations 64/96/128 x stage_qubits 3/4, one timed trajectory each), merged bench/fixes dd4b8c8; GPU tests 326+182; a2_runs --option autotune=1 n=28, 5 circuits x M=0.1/1
- **Outcome:** Chose 64/3 (brickwork), 64/4 (grid, qaoa), 64-96/4 (qft); vs masked default: brickwork -14%, grid -13/-2%, qft -3/-7%, qaoa -2%, ghz 0; geomean -6% (uniform best -4%); tuning cost 3-7 s per circuit. Masked kernels + autotune: 6-25% faster than defaults
- **Next:** Overview, glossary, final audit
- **Refs:** wiki/studies/error-kernels.md

## 2026-10-24 10:39 UTC  A8 autotune grid n=28
- **Goal:** End-to-end time with Simulator(autotune=True) (bench/fixes dd4b8c8), grid, damping M=0.1/1, 1000 shots, against the masked default
- **Task:** A8
- **Method:** code/bench/gpurun a2_runs.py --circuits grid --qubits 28 --noise damping --ps 0.000141443,0.00141443 --shots 1000 --reps 2 --budget 430 --option autotune=1
- **Outcome:** exit 0; outputs in data/20261024-103624-a8-autotune-grid-n-28
- **Next:** none
- **Refs:** data/20261024-103624-a8-autotune-grid-n-28, code/bench/a2_runs.py

## 2026-10-24 10:36 UTC  A8 autotune qaoa n=28
- **Goal:** End-to-end time with Simulator(autotune=True) (bench/fixes dd4b8c8), qaoa, damping M=0.1/1, 1000 shots, against the masked default
- **Task:** A8
- **Method:** code/bench/gpurun a2_runs.py --circuits qaoa --qubits 28 --noise damping --ps 0.00047619,0.0047619 --shots 1000 --reps 2 --budget 430 --option autotune=1
- **Outcome:** exit 0; outputs in data/20261024-103508-a8-autotune-qaoa-n-28
- **Next:** none
- **Refs:** data/20261024-103508-a8-autotune-qaoa-n-28, code/bench/a2_runs.py

## 2026-10-24 10:35 UTC  A8 autotune qft n=28
- **Goal:** End-to-end time with Simulator(autotune=True) (bench/fixes dd4b8c8), qft, damping M=0.1/1, 1000 shots, against the masked default
- **Task:** A8
- **Method:** code/bench/gpurun a2_runs.py --circuits qft --qubits 28 --noise damping --ps 0.000246305,0.00246305 --shots 1000 --reps 2 --budget 430 --option autotune=1
- **Outcome:** exit 0; outputs in data/20261024-103334-a8-autotune-qft-n-28
- **Next:** none
- **Refs:** data/20261024-103334-a8-autotune-qft-n-28, code/bench/a2_runs.py

## 2026-10-24 10:33 UTC  A8 autotune brickwork n=28
- **Goal:** End-to-end time with Simulator(autotune=True) (bench/fixes dd4b8c8), brickwork, damping M=0.1/1, 1000 shots, against the masked default
- **Task:** A8
- **Method:** code/bench/gpurun a2_runs.py --circuits brickwork --qubits 28 --noise damping --ps 0.000242131,0.00242131 --shots 1000 --reps 2 --budget 430 --option autotune=1
- **Outcome:** exit 0; outputs in data/20261024-103113-a8-autotune-brickwork-n-28
- **Next:** none
- **Refs:** data/20261024-103113-a8-autotune-brickwork-n-28, code/bench/a2_runs.py

## 2026-10-24 10:31 UTC  A7 parameter tuning: predictions and validation
- **Goal:** Find the best settings of noisecirc's fusion and kernel parameters on the H100 and the achievable gain
- **Task:** A7
- **Method:** 31 one-parameter settings (general kernels) and 13 settings/combinations (masked kernels) predicted from per-block times x dry-run per-block passes (n=26); best run end to end at n=28 (a2_runs with --option/--config)
- **Outcome:** Defaults near-optimal (best single change -2.5% on average); max_operations=64 + group_amplitudes=4096 never slower, -4% geomean, brickwork -13/-14%; brickwork max_operations=64 -15/-16%; QFT stage_qubits=4 -3/-7%; predictions off by up to 15%
- **Next:** A8 autotune runs
- **Refs:** wiki/studies/parameter-tuning.md, data/a7-analysis

## 2026-10-24 10:31 UTC  A8 autotune ghz n=28
- **Goal:** End-to-end time with Simulator(autotune=True) (bench/fixes dd4b8c8), ghz, damping M=0.1/1, 1000 shots, against the masked default
- **Task:** A8
- **Method:** code/bench/gpurun a2_runs.py --circuits ghz --qubits 28 --noise damping --ps 0.00183486,0.0183486 --shots 1000 --reps 2 --budget 430 --option autotune=1
- **Outcome:** exit 0; outputs in data/20261024-103044-a8-autotune-ghz-n-28
- **Next:** none
- **Refs:** data/20261024-103044-a8-autotune-ghz-n-28, code/bench/a2_runs.py

## 2026-10-24 10:28 UTC  A7 validation grid n=28 max_operations=64 group_amplitudes=4096
- **Goal:** End-to-end time with max_operations=64 group_amplitudes=4096 (bench/fixes, masked kernels), grid, damping M=0.1/1, 1000 shots, against the default runs of A8
- **Task:** A7
- **Method:** code/bench/gpurun a2_runs.py --circuits grid --qubits 28 --noise damping --ps 0.000141443,0.00141443 --shots 1000 --reps 2 --budget 430 --option max_operations=64 --config group_amplitudes=4096
- **Outcome:** exit 0; outputs in data/20261024-102605-a7-validation-grid-n-28-max-operations-64-group-amplitudes-4096
- **Next:** none
- **Refs:** data/20261024-102605-a7-validation-grid-n-28-max-operations-64-group-amplitudes-4096, code/bench/a2_runs.py

## 2026-10-24 10:26 UTC  A7 validation qaoa n=28 max_operations=64 group_amplitudes=4096
- **Goal:** End-to-end time with max_operations=64 group_amplitudes=4096 (bench/fixes, masked kernels), qaoa, damping M=0.1/1, 1000 shots, against the default runs of A8
- **Task:** A7
- **Method:** code/bench/gpurun a2_runs.py --circuits qaoa --qubits 28 --noise damping --ps 0.00047619,0.0047619 --shots 1000 --reps 2 --budget 430 --option max_operations=64 --config group_amplitudes=4096
- **Outcome:** exit 0; outputs in data/20261024-102457-a7-validation-qaoa-n-28-max-operations-64-group-amplitudes-4096
- **Next:** none
- **Refs:** data/20261024-102457-a7-validation-qaoa-n-28-max-operations-64-group-amplitudes-4096, code/bench/a2_runs.py

## 2026-10-24 10:24 UTC  A7 validation qft n=28 max_operations=64 group_amplitudes=4096
- **Goal:** End-to-end time with max_operations=64 group_amplitudes=4096 (bench/fixes, masked kernels), qft, damping M=0.1/1, 1000 shots, against the default runs of A8
- **Task:** A7
- **Method:** code/bench/gpurun a2_runs.py --circuits qft --qubits 28 --noise damping --ps 0.000246305,0.00246305 --shots 1000 --reps 2 --budget 430 --option max_operations=64 --config group_amplitudes=4096
- **Outcome:** exit 0; outputs in data/20261024-102318-a7-validation-qft-n-28-max-operations-64-group-amplitudes-4096
- **Next:** none
- **Refs:** data/20261024-102318-a7-validation-qft-n-28-max-operations-64-group-amplitudes-4096, code/bench/a2_runs.py

## 2026-10-24 10:23 UTC  A7 validation brickwork n=28 max_operations=64 group_amplitudes=4096
- **Goal:** End-to-end time with max_operations=64 group_amplitudes=4096 (bench/fixes, masked kernels), brickwork, damping M=0.1/1, 1000 shots, against the default runs of A8
- **Task:** A7
- **Method:** code/bench/gpurun a2_runs.py --circuits brickwork --qubits 28 --noise damping --ps 0.000242131,0.00242131 --shots 1000 --reps 2 --budget 430 --option max_operations=64 --config group_amplitudes=4096
- **Outcome:** exit 0; outputs in data/20261024-102108-a7-validation-brickwork-n-28-max-operations-64-group-amplitudes-4096
- **Next:** none
- **Refs:** data/20261024-102108-a7-validation-brickwork-n-28-max-operations-64-group-amplitudes-4096, code/bench/a2_runs.py

## 2026-10-24 10:21 UTC  A7 validation ghz n=28 max_operations=64 group_amplitudes=4096
- **Goal:** End-to-end time with max_operations=64 group_amplitudes=4096 (bench/fixes, masked kernels), ghz, damping M=0.1/1, 1000 shots, against the default runs of A8
- **Task:** A7
- **Method:** code/bench/gpurun a2_runs.py --circuits ghz --qubits 28 --noise damping --ps 0.00183486,0.0183486 --shots 1000 --reps 2 --budget 430 --option max_operations=64 --config group_amplitudes=4096
- **Outcome:** exit 0; outputs in data/20261024-102038-a7-validation-ghz-n-28-max-operations-64-group-amplitudes-4096
- **Next:** none
- **Refs:** data/20261024-102038-a7-validation-ghz-n-28-max-operations-64-group-amplitudes-4096, code/bench/a2_runs.py

## 2026-10-24 10:20 UTC  A7 validation qft n=28 stage_qubits=4
- **Goal:** End-to-end time with stage_qubits=4 (bench/fixes, masked kernels), qft, damping M=0.1/1, 1000 shots, against the default runs of A8
- **Task:** A7
- **Method:** code/bench/gpurun a2_runs.py --circuits qft --qubits 28 --noise damping --ps 0.000246305,0.00246305 --shots 1000 --reps 2 --budget 430 --config stage_qubits=4
- **Outcome:** exit 0; outputs in data/20261024-101902-a7-validation-qft-n-28-stage-qubits-4
- **Next:** none
- **Refs:** data/20261024-101902-a7-validation-qft-n-28-stage-qubits-4, code/bench/a2_runs.py

## 2026-10-24 10:19 UTC  A7 validation grid n=28 max_operations=96
- **Goal:** End-to-end time with max_operations=96 (bench/fixes, masked kernels), grid, damping M=0.1/1, 1000 shots, against the default runs of A8
- **Task:** A7
- **Method:** code/bench/gpurun a2_runs.py --circuits grid --qubits 28 --noise damping --ps 0.000141443,0.00141443 --shots 1000 --reps 2 --budget 430 --option max_operations=96
- **Outcome:** exit 0; outputs in data/20261024-101622-a7-validation-grid-n-28-max-operations-96
- **Next:** none
- **Refs:** data/20261024-101622-a7-validation-grid-n-28-max-operations-96, code/bench/a2_runs.py

## 2026-10-24 10:16 UTC  A7 validation brickwork n=28 max_operations=64
- **Goal:** End-to-end time with max_operations=64 (bench/fixes, masked kernels), brickwork, damping M=0.1/1, 1000 shots, against the default runs of A8
- **Task:** A7
- **Method:** code/bench/gpurun a2_runs.py --circuits brickwork --qubits 28 --noise damping --ps 0.000242131,0.00242131 --shots 1000 --reps 2 --budget 430 --option max_operations=64
- **Outcome:** exit 0; outputs in data/20261024-101411-a7-validation-brickwork-n-28-max-operations-64
- **Next:** none
- **Refs:** data/20261024-101411-a7-validation-brickwork-n-28-max-operations-64, code/bench/a2_runs.py

## 2026-10-24 10:15 UTC  A9 cuStateVec Ex comparison
- **Goal:** Compare noisecirc with delayed lower-bound per-shot sampling and split the gain
- **Task:** A9
- **Method:** a9_custatevec.py (SVUpdater, default fusion = best of 3-6) at A6's points (n=24, damping M=0.01/0.1/1, 100 shots); a9_analyze.py with the A6 table
- **Outcome:** cuStateVec Ex 12-69 passes/shot, 7-15x faster than CUDA-Q/Aer per shot; noisecirc 190-520x (M=0.01), 29-76x (0.1), 4-10x (1) faster; factors: sharing 15-270x (2.3-3.7 at M=1), per trajectory 1.6-3.2x
- **Next:** A9 done
- **Refs:** wiki/studies/lower-bound-sampling.md, data/a9-analysis

## 2026-10-24 10:12 UTC  A8 predicted times with masked kernels
- **Goal:** Predicted GPU times of the masked-kernel settings (error passes at t_mask), n=26, 5 circuits x 2 loads
- **Task:** A8
- **Method:** code/noisecirc/.venv/bin/python code/bench/a7_predict.py --error-kernel masked data/20261024-100152-a7-a8-block-times-with-masked-kernels-default data/20261024-100223-a7-a8-block-times-with-masked-kernels-max-operations-32 data/20261024-100253-a7-a8-block-times-with-masked-kernels-max-operations-48 data/20261024-100320-a7-a8-block-times-with-masked-kernels-max-operations-64 data/20261024-100345-a7-a8-block-times-with-masked-kernels-max-operations-96 data/20261024-100407-a7-a8-block-times-with-masked-kernels-max-operations-192 data/20261024-100424-a7-a8-block-times-with-masked-kernels-max-operations-256 data/20261024-100440-a7-a8-block-times-with-masked-kernels-stage-qubits-4 data/20261024-100525-a7-a8-block-times-with-masked-kernels-group-amplitudes-4096 data/20261024-100547-a7-a8-block-times-with-masked-kernels-max-operations-64-group-amplitudes-4096 data/20261024-100623-a7-a8-block-times-with-masked-kernels-stage-qubits-4-group-amplitudes-4096 data/20261024-100657-a7-a8-block-times-with-masked-kernels-stage-qubits-4-max-operations-64-group-amplitudes-4096 data/20261024-100835-a7-a8-block-times-with-masked-kernels-max-operations-64-pinned-bytes-128
- **Outcome:** exit 0; outputs in data/20261024-101021-a8-predicted-times-with-masked-kernels
- **Next:** none
- **Refs:** data/20261024-101021-a8-predicted-times-with-masked-kernels, code/bench/a7_predict.py

## 2026-10-24 10:12 UTC  A9 cuStateVec Ex qaoa n=24 dense fusion 6
- **Goal:** cuStateVec Ex with DENSE_FUSION_SIZE=6, qaoa, damping M=0.1, 100 shots
- **Task:** A9
- **Method:** code/bench/gpurun -p /local/venv-cuq/bin/python a9_custatevec.py --circuit qaoa --qubits 24 --ps 0.000555556 --shots 100 --dense-fusion 6
- **Outcome:** exit 0; outputs in data/20261024-101214-a9-custatevec-ex-qaoa-n-24-dense-fusion-6
- **Next:** none
- **Refs:** data/20261024-101214-a9-custatevec-ex-qaoa-n-24-dense-fusion-6, code/bench/a9_custatevec.py

## 2026-10-24 10:12 UTC  A9 cuStateVec Ex qaoa n=24 dense fusion 5
- **Goal:** cuStateVec Ex with DENSE_FUSION_SIZE=5, qaoa, damping M=0.1, 100 shots
- **Task:** A9
- **Method:** code/bench/gpurun -p /local/venv-cuq/bin/python a9_custatevec.py --circuit qaoa --qubits 24 --ps 0.000555556 --shots 100 --dense-fusion 5
- **Outcome:** exit 0; outputs in data/20261024-101211-a9-custatevec-ex-qaoa-n-24-dense-fusion-5
- **Next:** none
- **Refs:** data/20261024-101211-a9-custatevec-ex-qaoa-n-24-dense-fusion-5, code/bench/a9_custatevec.py

## 2026-10-24 10:12 UTC  A9 cuStateVec Ex qaoa n=24 dense fusion 4
- **Goal:** cuStateVec Ex with DENSE_FUSION_SIZE=4, qaoa, damping M=0.1, 100 shots
- **Task:** A9
- **Method:** code/bench/gpurun -p /local/venv-cuq/bin/python a9_custatevec.py --circuit qaoa --qubits 24 --ps 0.000555556 --shots 100 --dense-fusion 4
- **Outcome:** exit 0; outputs in data/20261024-101208-a9-custatevec-ex-qaoa-n-24-dense-fusion-4
- **Next:** none
- **Refs:** data/20261024-101208-a9-custatevec-ex-qaoa-n-24-dense-fusion-4, code/bench/a9_custatevec.py

## 2026-10-24 10:12 UTC  A9 cuStateVec Ex qaoa n=24 dense fusion 3
- **Goal:** cuStateVec Ex with DENSE_FUSION_SIZE=3, qaoa, damping M=0.1, 100 shots
- **Task:** A9
- **Method:** code/bench/gpurun -p /local/venv-cuq/bin/python a9_custatevec.py --circuit qaoa --qubits 24 --ps 0.000555556 --shots 100 --dense-fusion 3
- **Outcome:** exit 0; outputs in data/20261024-101205-a9-custatevec-ex-qaoa-n-24-dense-fusion-3
- **Next:** none
- **Refs:** data/20261024-101205-a9-custatevec-ex-qaoa-n-24-dense-fusion-3, code/bench/a9_custatevec.py

## 2026-10-24 10:12 UTC  A9 cuStateVec Ex qaoa n=24
- **Goal:** cuStateVec Ex SVUpdater per-shot trajectories, qaoa, damping M=0.01/0.1/1, 100 shots, default fusion
- **Task:** A9
- **Method:** code/bench/gpurun -p /local/venv-cuq/bin/python a9_custatevec.py --circuit qaoa --qubits 24 --ps 5.55556e-05,0.000555556,0.00555556 --shots 100
- **Outcome:** exit 0; outputs in data/20261024-101201-a9-custatevec-ex-qaoa-n-24
- **Next:** none
- **Refs:** data/20261024-101201-a9-custatevec-ex-qaoa-n-24, code/bench/a9_custatevec.py

## 2026-10-24 10:12 UTC  A9 cuStateVec Ex qft n=24 dense fusion 6
- **Goal:** cuStateVec Ex with DENSE_FUSION_SIZE=6, qft, damping M=0.1, 100 shots
- **Task:** A9
- **Method:** code/bench/gpurun -p /local/venv-cuq/bin/python a9_custatevec.py --circuit qft --qubits 24 --ps 0.000333333 --shots 100 --dense-fusion 6
- **Outcome:** exit 0; outputs in data/20261024-101156-a9-custatevec-ex-qft-n-24-dense-fusion-6
- **Next:** none
- **Refs:** data/20261024-101156-a9-custatevec-ex-qft-n-24-dense-fusion-6, code/bench/a9_custatevec.py

## 2026-10-24 10:11 UTC  A9 cuStateVec Ex qft n=24 dense fusion 5
- **Goal:** cuStateVec Ex with DENSE_FUSION_SIZE=5, qft, damping M=0.1, 100 shots
- **Task:** A9
- **Method:** code/bench/gpurun -p /local/venv-cuq/bin/python a9_custatevec.py --circuit qft --qubits 24 --ps 0.000333333 --shots 100 --dense-fusion 5
- **Outcome:** exit 0; outputs in data/20261024-101153-a9-custatevec-ex-qft-n-24-dense-fusion-5
- **Next:** none
- **Refs:** data/20261024-101153-a9-custatevec-ex-qft-n-24-dense-fusion-5, code/bench/a9_custatevec.py

## 2026-10-24 10:11 UTC  A9 cuStateVec Ex qft n=24 dense fusion 4
- **Goal:** cuStateVec Ex with DENSE_FUSION_SIZE=4, qft, damping M=0.1, 100 shots
- **Task:** A9
- **Method:** code/bench/gpurun -p /local/venv-cuq/bin/python a9_custatevec.py --circuit qft --qubits 24 --ps 0.000333333 --shots 100 --dense-fusion 4
- **Outcome:** exit 0; outputs in data/20261024-101149-a9-custatevec-ex-qft-n-24-dense-fusion-4
- **Next:** none
- **Refs:** data/20261024-101149-a9-custatevec-ex-qft-n-24-dense-fusion-4, code/bench/a9_custatevec.py

## 2026-10-24 10:11 UTC  A9 cuStateVec Ex qft n=24 dense fusion 3
- **Goal:** cuStateVec Ex with DENSE_FUSION_SIZE=3, qft, damping M=0.1, 100 shots
- **Task:** A9
- **Method:** code/bench/gpurun -p /local/venv-cuq/bin/python a9_custatevec.py --circuit qft --qubits 24 --ps 0.000333333 --shots 100 --dense-fusion 3
- **Outcome:** exit 0; outputs in data/20261024-101145-a9-custatevec-ex-qft-n-24-dense-fusion-3
- **Next:** none
- **Refs:** data/20261024-101145-a9-custatevec-ex-qft-n-24-dense-fusion-3, code/bench/a9_custatevec.py

## 2026-10-24 10:11 UTC  A9 cuStateVec Ex qft n=24
- **Goal:** cuStateVec Ex SVUpdater per-shot trajectories, qft, damping M=0.01/0.1/1, 100 shots, default fusion
- **Task:** A9
- **Method:** code/bench/gpurun -p /local/venv-cuq/bin/python a9_custatevec.py --circuit qft --qubits 24 --ps 3.33333e-05,0.000333333,0.00333333 --shots 100
- **Outcome:** exit 0; outputs in data/20261024-101140-a9-custatevec-ex-qft-n-24
- **Next:** none
- **Refs:** data/20261024-101140-a9-custatevec-ex-qft-n-24, code/bench/a9_custatevec.py

## 2026-10-24 10:11 UTC  A9 cuStateVec Ex brickwork n=24 dense fusion 6
- **Goal:** cuStateVec Ex with DENSE_FUSION_SIZE=6, brickwork, damping M=0.1, 100 shots
- **Task:** A9
- **Method:** code/bench/gpurun -p /local/venv-cuq/bin/python a9_custatevec.py --circuit brickwork --qubits 24 --ps 0.000326797 --shots 100 --dense-fusion 6
- **Outcome:** exit 0; outputs in data/20261024-101136-a9-custatevec-ex-brickwork-n-24-dense-fusion-6
- **Next:** none
- **Refs:** data/20261024-101136-a9-custatevec-ex-brickwork-n-24-dense-fusion-6, code/bench/a9_custatevec.py

## 2026-10-24 10:11 UTC  A9 cuStateVec Ex brickwork n=24 dense fusion 5
- **Goal:** cuStateVec Ex with DENSE_FUSION_SIZE=5, brickwork, damping M=0.1, 100 shots
- **Task:** A9
- **Method:** code/bench/gpurun -p /local/venv-cuq/bin/python a9_custatevec.py --circuit brickwork --qubits 24 --ps 0.000326797 --shots 100 --dense-fusion 5
- **Outcome:** exit 0; outputs in data/20261024-101133-a9-custatevec-ex-brickwork-n-24-dense-fusion-5
- **Next:** none
- **Refs:** data/20261024-101133-a9-custatevec-ex-brickwork-n-24-dense-fusion-5, code/bench/a9_custatevec.py

## 2026-10-24 10:11 UTC  A9 cuStateVec Ex brickwork n=24 dense fusion 4
- **Goal:** cuStateVec Ex with DENSE_FUSION_SIZE=4, brickwork, damping M=0.1, 100 shots
- **Task:** A9
- **Method:** code/bench/gpurun -p /local/venv-cuq/bin/python a9_custatevec.py --circuit brickwork --qubits 24 --ps 0.000326797 --shots 100 --dense-fusion 4
- **Outcome:** exit 0; outputs in data/20261024-101130-a9-custatevec-ex-brickwork-n-24-dense-fusion-4
- **Next:** none
- **Refs:** data/20261024-101130-a9-custatevec-ex-brickwork-n-24-dense-fusion-4, code/bench/a9_custatevec.py

## 2026-10-24 10:11 UTC  A9 cuStateVec Ex brickwork n=24 dense fusion 3
- **Goal:** cuStateVec Ex with DENSE_FUSION_SIZE=3, brickwork, damping M=0.1, 100 shots
- **Task:** A9
- **Method:** code/bench/gpurun -p /local/venv-cuq/bin/python a9_custatevec.py --circuit brickwork --qubits 24 --ps 0.000326797 --shots 100 --dense-fusion 3
- **Outcome:** exit 0; outputs in data/20261024-101127-a9-custatevec-ex-brickwork-n-24-dense-fusion-3
- **Next:** none
- **Refs:** data/20261024-101127-a9-custatevec-ex-brickwork-n-24-dense-fusion-3, code/bench/a9_custatevec.py

## 2026-10-24 10:11 UTC  A9 cuStateVec Ex brickwork n=24
- **Goal:** cuStateVec Ex SVUpdater per-shot trajectories, brickwork, damping M=0.01/0.1/1, 100 shots, default fusion
- **Task:** A9
- **Method:** code/bench/gpurun -p /local/venv-cuq/bin/python a9_custatevec.py --circuit brickwork --qubits 24 --ps 3.26797e-05,0.000326797,0.00326797 --shots 100
- **Outcome:** exit 0; outputs in data/20261024-101122-a9-custatevec-ex-brickwork-n-24
- **Next:** none
- **Refs:** data/20261024-101122-a9-custatevec-ex-brickwork-n-24, code/bench/a9_custatevec.py

## 2026-10-24 10:11 UTC  A9 cuStateVec Ex ghz n=24 dense fusion 6
- **Goal:** cuStateVec Ex with DENSE_FUSION_SIZE=6, ghz, damping M=0.1, 100 shots
- **Task:** A9
- **Method:** code/bench/gpurun -p /local/venv-cuq/bin/python a9_custatevec.py --circuit ghz --qubits 24 --ps 0.00215054 --shots 100 --dense-fusion 6
- **Outcome:** exit 0; outputs in data/20261024-101119-a9-custatevec-ex-ghz-n-24-dense-fusion-6
- **Next:** none
- **Refs:** data/20261024-101119-a9-custatevec-ex-ghz-n-24-dense-fusion-6, code/bench/a9_custatevec.py

## 2026-10-24 10:11 UTC  A9 cuStateVec Ex ghz n=24 dense fusion 5
- **Goal:** cuStateVec Ex with DENSE_FUSION_SIZE=5, ghz, damping M=0.1, 100 shots
- **Task:** A9
- **Method:** code/bench/gpurun -p /local/venv-cuq/bin/python a9_custatevec.py --circuit ghz --qubits 24 --ps 0.00215054 --shots 100 --dense-fusion 5
- **Outcome:** exit 0; outputs in data/20261024-101117-a9-custatevec-ex-ghz-n-24-dense-fusion-5
- **Next:** none
- **Refs:** data/20261024-101117-a9-custatevec-ex-ghz-n-24-dense-fusion-5, code/bench/a9_custatevec.py

## 2026-10-24 10:11 UTC  A9 cuStateVec Ex ghz n=24 dense fusion 4
- **Goal:** cuStateVec Ex with DENSE_FUSION_SIZE=4, ghz, damping M=0.1, 100 shots
- **Task:** A9
- **Method:** code/bench/gpurun -p /local/venv-cuq/bin/python a9_custatevec.py --circuit ghz --qubits 24 --ps 0.00215054 --shots 100 --dense-fusion 4
- **Outcome:** exit 0; outputs in data/20261024-101115-a9-custatevec-ex-ghz-n-24-dense-fusion-4
- **Next:** none
- **Refs:** data/20261024-101115-a9-custatevec-ex-ghz-n-24-dense-fusion-4, code/bench/a9_custatevec.py

## 2026-10-24 10:11 UTC  A9 cuStateVec Ex ghz n=24 dense fusion 3
- **Goal:** cuStateVec Ex with DENSE_FUSION_SIZE=3, ghz, damping M=0.1, 100 shots
- **Task:** A9
- **Method:** code/bench/gpurun -p /local/venv-cuq/bin/python a9_custatevec.py --circuit ghz --qubits 24 --ps 0.00215054 --shots 100 --dense-fusion 3
- **Outcome:** exit 0; outputs in data/20261024-101111-a9-custatevec-ex-ghz-n-24-dense-fusion-3
- **Next:** none
- **Refs:** data/20261024-101111-a9-custatevec-ex-ghz-n-24-dense-fusion-3, code/bench/a9_custatevec.py

## 2026-10-24 10:11 UTC  A9 cuStateVec Ex ghz n=24
- **Goal:** cuStateVec Ex SVUpdater per-shot trajectories, ghz, damping M=0.01/0.1/1, 100 shots, default fusion
- **Task:** A9
- **Method:** code/bench/gpurun -p /local/venv-cuq/bin/python a9_custatevec.py --circuit ghz --qubits 24 --ps 0.000215054,0.00215054,0.0215054 --shots 100
- **Outcome:** exit 0; outputs in data/20261024-101109-a9-custatevec-ex-ghz-n-24
- **Next:** none
- **Refs:** data/20261024-101109-a9-custatevec-ex-ghz-n-24, code/bench/a9_custatevec.py

## 2026-10-24 10:11 UTC  A9 cuStateVec Ex runner: correctness check
- **Goal:** Check that the SVUpdater trajectory runner samples the noisy distribution
- **Task:** A9
- **Method:** a9_custatevec.py --check: 20000 shots of ghz (p=0.2) and brickwork (p=0.1) at n=4 against exact density matrix
- **Outcome:** TVD 0.008/0.007, max |z| 1.9/1.6: consistent with sampling noise
- **Next:** A9 timing batch
- **Refs:** code/bench/a9_custatevec.py

## 2026-10-24 10:10 UTC  A9 cuStateVec Ex tier 1
- **Goal:** Check the SVUpdater trajectory runner on brickwork n=20
- **Task:** A9
- **Method:** code/bench/gpurun -p /local/venv-cuq/bin/python a9_custatevec.py --circuit brickwork --qubits 20 --ps 0.001 --shots 20
- **Outcome:** exit 0; outputs in data/20261024-101021-a9-custatevec-ex-tier-1
- **Next:** none
- **Refs:** data/20261024-101021-a9-custatevec-ex-tier-1, code/bench/a9_custatevec.py

## 2026-10-24 10:09 UTC  A7/A8 block times with masked kernels max_operations=64,pinned_bytes=128
- **Goal:** Per-block dominant, general and masked kernel times on bench/fixes 807fe90 (masked error kernels), 5 circuits x 2 loads, n=26
- **Task:** A8
- **Method:** code/bench/gpurun a7_blocks.py --workloads ghz:damping:0.0019802,ghz:damping:0.019802,brickwork:damping:0.000280112,brickwork:damping:0.00280112,qft:damping:0.0002849,qft:damping:0.002849,qaoa:damping:0.000512821,qaoa:damping:0.00512821,grid:damping:0.00017094,grid:damping:0.0017094 --qubits 26 --label masked:max_operations=64,pinned_bytes=128 --set max_operations=64 --set pinned_bytes=128
- **Outcome:** exit 0; outputs in data/20261024-100835-a7-a8-block-times-with-masked-kernels-max-operations-64-pinned-bytes-128
- **Next:** none
- **Refs:** data/20261024-100835-a7-a8-block-times-with-masked-kernels-max-operations-64-pinned-bytes-128, code/bench/a7_blocks.py

## 2026-10-24 10:08 UTC  A7/A8 block times with masked kernels stage_qubits=4,max_operations=64,group_amplitudes=4096
- **Goal:** Per-block dominant, general and masked kernel times on bench/fixes 807fe90 (masked error kernels), 5 circuits x 2 loads, n=26
- **Task:** A8
- **Method:** code/bench/gpurun a7_blocks.py --workloads ghz:damping:0.0019802,ghz:damping:0.019802,brickwork:damping:0.000280112,brickwork:damping:0.00280112,qft:damping:0.0002849,qft:damping:0.002849,qaoa:damping:0.000512821,qaoa:damping:0.00512821,grid:damping:0.00017094,grid:damping:0.0017094 --qubits 26 --label masked:stage_qubits=4,max_operations=64,group_amplitudes=4096 --set stage_qubits=4 --set max_operations=64 --set group_amplitudes=4096
- **Outcome:** exit 0; outputs in data/20261024-100657-a7-a8-block-times-with-masked-kernels-stage-qubits-4-max-operations-64-group-amplitudes-4096
- **Next:** none
- **Refs:** data/20261024-100657-a7-a8-block-times-with-masked-kernels-stage-qubits-4-max-operations-64-group-amplitudes-4096, code/bench/a7_blocks.py

## 2026-10-24 10:06 UTC  A7/A8 block times with masked kernels stage_qubits=4,group_amplitudes=4096
- **Goal:** Per-block dominant, general and masked kernel times on bench/fixes 807fe90 (masked error kernels), 5 circuits x 2 loads, n=26
- **Task:** A8
- **Method:** code/bench/gpurun a7_blocks.py --workloads ghz:damping:0.0019802,ghz:damping:0.019802,brickwork:damping:0.000280112,brickwork:damping:0.00280112,qft:damping:0.0002849,qft:damping:0.002849,qaoa:damping:0.000512821,qaoa:damping:0.00512821,grid:damping:0.00017094,grid:damping:0.0017094 --qubits 26 --label masked:stage_qubits=4,group_amplitudes=4096 --set stage_qubits=4 --set group_amplitudes=4096
- **Outcome:** exit 0; outputs in data/20261024-100623-a7-a8-block-times-with-masked-kernels-stage-qubits-4-group-amplitudes-4096
- **Next:** none
- **Refs:** data/20261024-100623-a7-a8-block-times-with-masked-kernels-stage-qubits-4-group-amplitudes-4096, code/bench/a7_blocks.py

## 2026-10-24 10:06 UTC  A7/A8 block times with masked kernels max_operations=64,group_amplitudes=4096
- **Goal:** Per-block dominant, general and masked kernel times on bench/fixes 807fe90 (masked error kernels), 5 circuits x 2 loads, n=26
- **Task:** A8
- **Method:** code/bench/gpurun a7_blocks.py --workloads ghz:damping:0.0019802,ghz:damping:0.019802,brickwork:damping:0.000280112,brickwork:damping:0.00280112,qft:damping:0.0002849,qft:damping:0.002849,qaoa:damping:0.000512821,qaoa:damping:0.00512821,grid:damping:0.00017094,grid:damping:0.0017094 --qubits 26 --label masked:max_operations=64,group_amplitudes=4096 --set max_operations=64 --set group_amplitudes=4096
- **Outcome:** exit 0; outputs in data/20261024-100547-a7-a8-block-times-with-masked-kernels-max-operations-64-group-amplitudes-4096
- **Next:** none
- **Refs:** data/20261024-100547-a7-a8-block-times-with-masked-kernels-max-operations-64-group-amplitudes-4096, code/bench/a7_blocks.py

## 2026-10-24 10:05 UTC  A7/A8 block times with masked kernels group_amplitudes=4096
- **Goal:** Per-block dominant, general and masked kernel times on bench/fixes 807fe90 (masked error kernels), 5 circuits x 2 loads, n=26
- **Task:** A8
- **Method:** code/bench/gpurun a7_blocks.py --workloads ghz:damping:0.0019802,ghz:damping:0.019802,brickwork:damping:0.000280112,brickwork:damping:0.00280112,qft:damping:0.0002849,qft:damping:0.002849,qaoa:damping:0.000512821,qaoa:damping:0.00512821,grid:damping:0.00017094,grid:damping:0.0017094 --qubits 26 --label masked:group_amplitudes=4096 --set group_amplitudes=4096
- **Outcome:** exit 0; outputs in data/20261024-100525-a7-a8-block-times-with-masked-kernels-group-amplitudes-4096
- **Next:** none
- **Refs:** data/20261024-100525-a7-a8-block-times-with-masked-kernels-group-amplitudes-4096, code/bench/a7_blocks.py

## 2026-10-24 10:05 UTC  A7/A8 block times with masked kernels stage_qubits=4
- **Goal:** Per-block dominant, general and masked kernel times on bench/fixes 807fe90 (masked error kernels), 5 circuits x 2 loads, n=26
- **Task:** A8
- **Method:** code/bench/gpurun a7_blocks.py --workloads ghz:damping:0.0019802,ghz:damping:0.019802,brickwork:damping:0.000280112,brickwork:damping:0.00280112,qft:damping:0.0002849,qft:damping:0.002849,qaoa:damping:0.000512821,qaoa:damping:0.00512821,grid:damping:0.00017094,grid:damping:0.0017094 --qubits 26 --label masked:stage_qubits=4 --set stage_qubits=4
- **Outcome:** exit 0; outputs in data/20261024-100440-a7-a8-block-times-with-masked-kernels-stage-qubits-4
- **Next:** none
- **Refs:** data/20261024-100440-a7-a8-block-times-with-masked-kernels-stage-qubits-4, code/bench/a7_blocks.py

## 2026-10-24 10:04 UTC  A7/A8 block times with masked kernels max_operations=256
- **Goal:** Per-block dominant, general and masked kernel times on bench/fixes 807fe90 (masked error kernels), 5 circuits x 2 loads, n=26
- **Task:** A8
- **Method:** code/bench/gpurun a7_blocks.py --workloads ghz:damping:0.0019802,ghz:damping:0.019802,brickwork:damping:0.000280112,brickwork:damping:0.00280112,qft:damping:0.0002849,qft:damping:0.002849,qaoa:damping:0.000512821,qaoa:damping:0.00512821,grid:damping:0.00017094,grid:damping:0.0017094 --qubits 26 --label masked:max_operations=256 --set max_operations=256
- **Outcome:** exit 0; outputs in data/20261024-100424-a7-a8-block-times-with-masked-kernels-max-operations-256
- **Next:** none
- **Refs:** data/20261024-100424-a7-a8-block-times-with-masked-kernels-max-operations-256, code/bench/a7_blocks.py

## 2026-10-24 10:04 UTC  A7/A8 block times with masked kernels max_operations=192
- **Goal:** Per-block dominant, general and masked kernel times on bench/fixes 807fe90 (masked error kernels), 5 circuits x 2 loads, n=26
- **Task:** A8
- **Method:** code/bench/gpurun a7_blocks.py --workloads ghz:damping:0.0019802,ghz:damping:0.019802,brickwork:damping:0.000280112,brickwork:damping:0.00280112,qft:damping:0.0002849,qft:damping:0.002849,qaoa:damping:0.000512821,qaoa:damping:0.00512821,grid:damping:0.00017094,grid:damping:0.0017094 --qubits 26 --label masked:max_operations=192 --set max_operations=192
- **Outcome:** exit 0; outputs in data/20261024-100407-a7-a8-block-times-with-masked-kernels-max-operations-192
- **Next:** none
- **Refs:** data/20261024-100407-a7-a8-block-times-with-masked-kernels-max-operations-192, code/bench/a7_blocks.py

## 2026-10-24 10:04 UTC  A7/A8 block times with masked kernels max_operations=96
- **Goal:** Per-block dominant, general and masked kernel times on bench/fixes 807fe90 (masked error kernels), 5 circuits x 2 loads, n=26
- **Task:** A8
- **Method:** code/bench/gpurun a7_blocks.py --workloads ghz:damping:0.0019802,ghz:damping:0.019802,brickwork:damping:0.000280112,brickwork:damping:0.00280112,qft:damping:0.0002849,qft:damping:0.002849,qaoa:damping:0.000512821,qaoa:damping:0.00512821,grid:damping:0.00017094,grid:damping:0.0017094 --qubits 26 --label masked:max_operations=96 --set max_operations=96
- **Outcome:** exit 0; outputs in data/20261024-100345-a7-a8-block-times-with-masked-kernels-max-operations-96
- **Next:** none
- **Refs:** data/20261024-100345-a7-a8-block-times-with-masked-kernels-max-operations-96, code/bench/a7_blocks.py

## 2026-10-24 10:03 UTC  A7/A8 block times with masked kernels max_operations=64
- **Goal:** Per-block dominant, general and masked kernel times on bench/fixes 807fe90 (masked error kernels), 5 circuits x 2 loads, n=26
- **Task:** A8
- **Method:** code/bench/gpurun a7_blocks.py --workloads ghz:damping:0.0019802,ghz:damping:0.019802,brickwork:damping:0.000280112,brickwork:damping:0.00280112,qft:damping:0.0002849,qft:damping:0.002849,qaoa:damping:0.000512821,qaoa:damping:0.00512821,grid:damping:0.00017094,grid:damping:0.0017094 --qubits 26 --label masked:max_operations=64 --set max_operations=64
- **Outcome:** exit 0; outputs in data/20261024-100320-a7-a8-block-times-with-masked-kernels-max-operations-64
- **Next:** none
- **Refs:** data/20261024-100320-a7-a8-block-times-with-masked-kernels-max-operations-64, code/bench/a7_blocks.py

## 2026-10-24 10:03 UTC  A7/A8 block times with masked kernels max_operations=48
- **Goal:** Per-block dominant, general and masked kernel times on bench/fixes 807fe90 (masked error kernels), 5 circuits x 2 loads, n=26
- **Task:** A8
- **Method:** code/bench/gpurun a7_blocks.py --workloads ghz:damping:0.0019802,ghz:damping:0.019802,brickwork:damping:0.000280112,brickwork:damping:0.00280112,qft:damping:0.0002849,qft:damping:0.002849,qaoa:damping:0.000512821,qaoa:damping:0.00512821,grid:damping:0.00017094,grid:damping:0.0017094 --qubits 26 --label masked:max_operations=48 --set max_operations=48
- **Outcome:** exit 0; outputs in data/20261024-100253-a7-a8-block-times-with-masked-kernels-max-operations-48
- **Next:** none
- **Refs:** data/20261024-100253-a7-a8-block-times-with-masked-kernels-max-operations-48, code/bench/a7_blocks.py

## 2026-10-24 10:02 UTC  A7/A8 block times with masked kernels max_operations=32
- **Goal:** Per-block dominant, general and masked kernel times on bench/fixes 807fe90 (masked error kernels), 5 circuits x 2 loads, n=26
- **Task:** A8
- **Method:** code/bench/gpurun a7_blocks.py --workloads ghz:damping:0.0019802,ghz:damping:0.019802,brickwork:damping:0.000280112,brickwork:damping:0.00280112,qft:damping:0.0002849,qft:damping:0.002849,qaoa:damping:0.000512821,qaoa:damping:0.00512821,grid:damping:0.00017094,grid:damping:0.0017094 --qubits 26 --label masked:max_operations=32 --set max_operations=32
- **Outcome:** exit 0; outputs in data/20261024-100223-a7-a8-block-times-with-masked-kernels-max-operations-32
- **Next:** none
- **Refs:** data/20261024-100223-a7-a8-block-times-with-masked-kernels-max-operations-32, code/bench/a7_blocks.py

## 2026-10-24 10:02 UTC  A7/A8 block times with masked kernels default
- **Goal:** Per-block dominant, general and masked kernel times on bench/fixes 807fe90 (masked error kernels), 5 circuits x 2 loads, n=26
- **Task:** A8
- **Method:** code/bench/gpurun a7_blocks.py --workloads ghz:damping:0.0019802,ghz:damping:0.019802,brickwork:damping:0.000280112,brickwork:damping:0.00280112,qft:damping:0.0002849,qft:damping:0.002849,qaoa:damping:0.000512821,qaoa:damping:0.00512821,grid:damping:0.00017094,grid:damping:0.0017094 --qubits 26 --label masked:default
- **Outcome:** exit 0; outputs in data/20261024-100152-a7-a8-block-times-with-masked-kernels-default
- **Next:** none
- **Refs:** data/20261024-100152-a7-a8-block-times-with-masked-kernels-default, code/bench/a7_blocks.py

## 2026-10-24 10:01 UTC  A8 masked error kernels: implementation and A/B
- **Goal:** Make passes of trajectories with errors as cheap as dominant passes
- **Task:** A8
- **Method:** svpass Block.with_defaults + stage mask rows, two bodies per stage (feature/masked-error-kernels d6f43d1, docs 2nd commit; merged into bench/fixes 807fe90/7578381); tests 326+179 GPU, statistical 2; a7_blocks masked timing; a2_runs n=28 5 circuits x M=0.1/1 MASKED_ERROR_KERNELS True vs False
- **Outcome:** Masked kernel per pass 1.1-1.7 t_bw vs general 1.3-2.5 (dominant 1.1-1.6); end-to-end 4-13% faster (brickwork 12-13%, qaoa 8-10%, ghz 8-9%, qft 5%, grid 4%), identical passes
- **Next:** Block-size sweep with masked kernels (a7batch2)
- **Refs:** data/a7-analysis, code/noisecirc

## 2026-10-24 10:01 UTC  A8 masked kernels False grid n=28
- **Goal:** End-to-end time with MASKED_ERROR_KERNELS=False (bench/fixes 807fe90), grid, damping M=0.1/1, 1000 shots
- **Task:** A8
- **Method:** code/bench/gpurun a2_runs.py --circuits grid --qubits 28 --noise damping --ps 0.000141443,0.00141443 --shots 1000 --reps 2 --budget 430 --tunable MASKED_ERROR_KERNELS=False
- **Outcome:** exit 0; outputs in data/20261024-095850-a8-masked-kernels-false-grid-n-28
- **Next:** none
- **Refs:** data/20261024-095850-a8-masked-kernels-false-grid-n-28, code/bench/a2_runs.py

## 2026-10-24 09:58 UTC  A8 masked kernels True grid n=28
- **Goal:** End-to-end time with MASKED_ERROR_KERNELS=True (bench/fixes 807fe90), grid, damping M=0.1/1, 1000 shots
- **Task:** A8
- **Method:** code/bench/gpurun a2_runs.py --circuits grid --qubits 28 --noise damping --ps 0.000141443,0.00141443 --shots 1000 --reps 2 --budget 430 --tunable MASKED_ERROR_KERNELS=True
- **Outcome:** exit 0; outputs in data/20261024-095606-a8-masked-kernels-true-grid-n-28
- **Next:** none
- **Refs:** data/20261024-095606-a8-masked-kernels-true-grid-n-28, code/bench/a2_runs.py

## 2026-10-24 09:56 UTC  A8 masked kernels False qaoa n=28
- **Goal:** End-to-end time with MASKED_ERROR_KERNELS=False (bench/fixes 807fe90), qaoa, damping M=0.1/1, 1000 shots
- **Task:** A8
- **Method:** code/bench/gpurun a2_runs.py --circuits qaoa --qubits 28 --noise damping --ps 0.00047619,0.0047619 --shots 1000 --reps 2 --budget 430 --tunable MASKED_ERROR_KERNELS=False
- **Outcome:** exit 0; outputs in data/20261024-095448-a8-masked-kernels-false-qaoa-n-28
- **Next:** none
- **Refs:** data/20261024-095448-a8-masked-kernels-false-qaoa-n-28, code/bench/a2_runs.py

## 2026-10-24 09:54 UTC  A8 masked kernels True qaoa n=28
- **Goal:** End-to-end time with MASKED_ERROR_KERNELS=True (bench/fixes 807fe90), qaoa, damping M=0.1/1, 1000 shots
- **Task:** A8
- **Method:** code/bench/gpurun a2_runs.py --circuits qaoa --qubits 28 --noise damping --ps 0.00047619,0.0047619 --shots 1000 --reps 2 --budget 430 --tunable MASKED_ERROR_KERNELS=True
- **Outcome:** exit 0; outputs in data/20261024-095337-a8-masked-kernels-true-qaoa-n-28
- **Next:** none
- **Refs:** data/20261024-095337-a8-masked-kernels-true-qaoa-n-28, code/bench/a2_runs.py

## 2026-10-24 09:53 UTC  A8 masked kernels False qft n=28
- **Goal:** End-to-end time with MASKED_ERROR_KERNELS=False (bench/fixes 807fe90), qft, damping M=0.1/1, 1000 shots
- **Task:** A8
- **Method:** code/bench/gpurun a2_runs.py --circuits qft --qubits 28 --noise damping --ps 0.000246305,0.00246305 --shots 1000 --reps 2 --budget 430 --tunable MASKED_ERROR_KERNELS=False
- **Outcome:** exit 0; outputs in data/20261024-095154-a8-masked-kernels-false-qft-n-28
- **Next:** none
- **Refs:** data/20261024-095154-a8-masked-kernels-false-qft-n-28, code/bench/a2_runs.py

## 2026-10-24 09:51 UTC  A8 masked kernels True qft n=28
- **Goal:** End-to-end time with MASKED_ERROR_KERNELS=True (bench/fixes 807fe90), qft, damping M=0.1/1, 1000 shots
- **Task:** A8
- **Method:** code/bench/gpurun a2_runs.py --circuits qft --qubits 28 --noise damping --ps 0.000246305,0.00246305 --shots 1000 --reps 2 --budget 430 --tunable MASKED_ERROR_KERNELS=True
- **Outcome:** exit 0; outputs in data/20261024-095013-a8-masked-kernels-true-qft-n-28
- **Next:** none
- **Refs:** data/20261024-095013-a8-masked-kernels-true-qft-n-28, code/bench/a2_runs.py

## 2026-10-24 09:50 UTC  A8 masked kernels False brickwork n=28
- **Goal:** End-to-end time with MASKED_ERROR_KERNELS=False (bench/fixes 807fe90), brickwork, damping M=0.1/1, 1000 shots
- **Task:** A8
- **Method:** code/bench/gpurun a2_runs.py --circuits brickwork --qubits 28 --noise damping --ps 0.000242131,0.00242131 --shots 1000 --reps 2 --budget 430 --tunable MASKED_ERROR_KERNELS=False
- **Outcome:** exit 0; outputs in data/20261024-094724-a8-masked-kernels-false-brickwork-n-28
- **Next:** none
- **Refs:** data/20261024-094724-a8-masked-kernels-false-brickwork-n-28, code/bench/a2_runs.py

## 2026-10-24 09:48 UTC  A7 predicted times of all settings
- **Goal:** Combine per-block kernel times of 31 settings with dry-run per-block passes into predicted GPU times (n=26, 5 circuits x 2 loads, 1000 shots)
- **Task:** A7
- **Method:** code/noisecirc/.venv/bin/python code/bench/a7_predict.py data/20261024-091611-a7-block-times-default data/20261024-091638-a7-block-times-max-operations-16 data/20261024-091708-a7-block-times-max-operations-24 data/20261024-091735-a7-block-times-max-operations-32 data/20261024-091801-a7-block-times-max-operations-48 data/20261024-091825-a7-block-times-max-operations-64 data/20261024-091846-a7-block-times-max-operations-96 data/20261024-091904-a7-block-times-max-operations-192 data/20261024-091917-a7-block-times-max-operations-256 data/20261024-091930-a7-block-times-max-fused-qudits-5 data/20261024-092000-a7-block-times-max-fused-qudits-6 data/20261024-092028-a7-block-times-max-fused-qudits-7 data/20261024-092055-a7-block-times-max-fused-qudits-8 data/20261024-092121-a7-block-times-max-fused-qudits-10 data/20261024-092149-a7-block-times-pinned-bytes-16 data/20261024-092217-a7-block-times-pinned-bytes-32 data/20261024-092244-a7-block-times-pinned-bytes-128 data/20261024-092310-a7-block-times-stage-qubits-2 data/20261024-092333-a7-block-times-stage-qubits-4 data/20261024-092412-a7-block-times-group-amplitudes-512 data/20261024-092428-a7-block-times-group-amplitudes-1024 data/20261024-092441-a7-block-times-group-amplitudes-4096 data/20261024-092457-a7-block-times-group-amplitudes-8192 data/20261024-092523-a7-block-times-threads-64 data/20261024-092552-a7-block-times-threads-128 data/20261024-092619-a7-block-times-threads-512 data/20261024-092645-a7-block-times-min-registers-32 data/20261024-092713-a7-block-times-min-registers-48 data/20261024-092741-a7-block-times-min-registers-96 data/20261024-092807-a7-block-times-min-registers-128
- **Outcome:** exit 0; outputs in data/20261024-094143-a7-predicted-times-of-all-settings
- **Next:** none
- **Refs:** data/20261024-094143-a7-predicted-times-of-all-settings, code/bench/a7_predict.py

## 2026-10-24 09:47 UTC  A8 masked kernels True brickwork n=28
- **Goal:** End-to-end time with MASKED_ERROR_KERNELS=True (bench/fixes 807fe90), brickwork, damping M=0.1/1, 1000 shots
- **Task:** A8
- **Method:** code/bench/gpurun a2_runs.py --circuits brickwork --qubits 28 --noise damping --ps 0.000242131,0.00242131 --shots 1000 --reps 2 --budget 430 --tunable MASKED_ERROR_KERNELS=True
- **Outcome:** exit 0; outputs in data/20261024-094452-a8-masked-kernels-true-brickwork-n-28
- **Next:** none
- **Refs:** data/20261024-094452-a8-masked-kernels-true-brickwork-n-28, code/bench/a2_runs.py

## 2026-10-24 09:44 UTC  A8 masked kernels False ghz n=28
- **Goal:** End-to-end time with MASKED_ERROR_KERNELS=False (bench/fixes 807fe90), ghz, damping M=0.1/1, 1000 shots
- **Task:** A8
- **Method:** code/bench/gpurun a2_runs.py --circuits ghz --qubits 28 --noise damping --ps 0.00183486,0.0183486 --shots 1000 --reps 2 --budget 430 --tunable MASKED_ERROR_KERNELS=False
- **Outcome:** exit 0; outputs in data/20261024-094421-a8-masked-kernels-false-ghz-n-28
- **Next:** none
- **Refs:** data/20261024-094421-a8-masked-kernels-false-ghz-n-28, code/bench/a2_runs.py

## 2026-10-24 09:44 UTC  A8 masked kernels True ghz n=28
- **Goal:** End-to-end time with MASKED_ERROR_KERNELS=True (bench/fixes 807fe90), ghz, damping M=0.1/1, 1000 shots
- **Task:** A8
- **Method:** code/bench/gpurun a2_runs.py --circuits ghz --qubits 28 --noise damping --ps 0.00183486,0.0183486 --shots 1000 --reps 2 --budget 430 --tunable MASKED_ERROR_KERNELS=True
- **Outcome:** exit 0; outputs in data/20261024-094352-a8-masked-kernels-true-ghz-n-28
- **Next:** none
- **Refs:** data/20261024-094352-a8-masked-kernels-true-ghz-n-28, code/bench/a2_runs.py

## 2026-10-24 09:28 UTC  A7 block times min_registers=128
- **Goal:** Per-block kernel times of 5 circuits x 2 loads at n=26 with min_registers=128
- **Task:** A7
- **Method:** code/bench/gpurun a7_blocks.py --workloads ghz:damping:0.0019802,ghz:damping:0.019802,brickwork:damping:0.000280112,brickwork:damping:0.00280112,qft:damping:0.0002849,qft:damping:0.002849,qaoa:damping:0.000512821,qaoa:damping:0.00512821,grid:damping:0.00017094,grid:damping:0.0017094 --qubits 26 --label min_registers=128 --set min_registers=128
- **Outcome:** exit 0; outputs in data/20261024-092807-a7-block-times-min-registers-128
- **Next:** none
- **Refs:** data/20261024-092807-a7-block-times-min-registers-128, code/bench/a7_blocks.py

## 2026-10-24 09:28 UTC  A7 block times min_registers=96
- **Goal:** Per-block kernel times of 5 circuits x 2 loads at n=26 with min_registers=96
- **Task:** A7
- **Method:** code/bench/gpurun a7_blocks.py --workloads ghz:damping:0.0019802,ghz:damping:0.019802,brickwork:damping:0.000280112,brickwork:damping:0.00280112,qft:damping:0.0002849,qft:damping:0.002849,qaoa:damping:0.000512821,qaoa:damping:0.00512821,grid:damping:0.00017094,grid:damping:0.0017094 --qubits 26 --label min_registers=96 --set min_registers=96
- **Outcome:** exit 0; outputs in data/20261024-092741-a7-block-times-min-registers-96
- **Next:** none
- **Refs:** data/20261024-092741-a7-block-times-min-registers-96, code/bench/a7_blocks.py

## 2026-10-24 09:27 UTC  A7 block times min_registers=48
- **Goal:** Per-block kernel times of 5 circuits x 2 loads at n=26 with min_registers=48
- **Task:** A7
- **Method:** code/bench/gpurun a7_blocks.py --workloads ghz:damping:0.0019802,ghz:damping:0.019802,brickwork:damping:0.000280112,brickwork:damping:0.00280112,qft:damping:0.0002849,qft:damping:0.002849,qaoa:damping:0.000512821,qaoa:damping:0.00512821,grid:damping:0.00017094,grid:damping:0.0017094 --qubits 26 --label min_registers=48 --set min_registers=48
- **Outcome:** exit 0; outputs in data/20261024-092713-a7-block-times-min-registers-48
- **Next:** none
- **Refs:** data/20261024-092713-a7-block-times-min-registers-48, code/bench/a7_blocks.py

## 2026-10-24 09:27 UTC  A7 block times min_registers=32
- **Goal:** Per-block kernel times of 5 circuits x 2 loads at n=26 with min_registers=32
- **Task:** A7
- **Method:** code/bench/gpurun a7_blocks.py --workloads ghz:damping:0.0019802,ghz:damping:0.019802,brickwork:damping:0.000280112,brickwork:damping:0.00280112,qft:damping:0.0002849,qft:damping:0.002849,qaoa:damping:0.000512821,qaoa:damping:0.00512821,grid:damping:0.00017094,grid:damping:0.0017094 --qubits 26 --label min_registers=32 --set min_registers=32
- **Outcome:** exit 0; outputs in data/20261024-092645-a7-block-times-min-registers-32
- **Next:** none
- **Refs:** data/20261024-092645-a7-block-times-min-registers-32, code/bench/a7_blocks.py

## 2026-10-24 09:26 UTC  A7 block times threads=512
- **Goal:** Per-block kernel times of 5 circuits x 2 loads at n=26 with threads=512
- **Task:** A7
- **Method:** code/bench/gpurun a7_blocks.py --workloads ghz:damping:0.0019802,ghz:damping:0.019802,brickwork:damping:0.000280112,brickwork:damping:0.00280112,qft:damping:0.0002849,qft:damping:0.002849,qaoa:damping:0.000512821,qaoa:damping:0.00512821,grid:damping:0.00017094,grid:damping:0.0017094 --qubits 26 --label threads=512 --set threads=512
- **Outcome:** exit 0; outputs in data/20261024-092619-a7-block-times-threads-512
- **Next:** none
- **Refs:** data/20261024-092619-a7-block-times-threads-512, code/bench/a7_blocks.py

## 2026-10-24 09:26 UTC  A7 block times threads=128
- **Goal:** Per-block kernel times of 5 circuits x 2 loads at n=26 with threads=128
- **Task:** A7
- **Method:** code/bench/gpurun a7_blocks.py --workloads ghz:damping:0.0019802,ghz:damping:0.019802,brickwork:damping:0.000280112,brickwork:damping:0.00280112,qft:damping:0.0002849,qft:damping:0.002849,qaoa:damping:0.000512821,qaoa:damping:0.00512821,grid:damping:0.00017094,grid:damping:0.0017094 --qubits 26 --label threads=128 --set threads=128
- **Outcome:** exit 0; outputs in data/20261024-092552-a7-block-times-threads-128
- **Next:** none
- **Refs:** data/20261024-092552-a7-block-times-threads-128, code/bench/a7_blocks.py

## 2026-10-24 09:25 UTC  A7 block times threads=64
- **Goal:** Per-block kernel times of 5 circuits x 2 loads at n=26 with threads=64
- **Task:** A7
- **Method:** code/bench/gpurun a7_blocks.py --workloads ghz:damping:0.0019802,ghz:damping:0.019802,brickwork:damping:0.000280112,brickwork:damping:0.00280112,qft:damping:0.0002849,qft:damping:0.002849,qaoa:damping:0.000512821,qaoa:damping:0.00512821,grid:damping:0.00017094,grid:damping:0.0017094 --qubits 26 --label threads=64 --set threads=64
- **Outcome:** exit 0; outputs in data/20261024-092523-a7-block-times-threads-64
- **Next:** none
- **Refs:** data/20261024-092523-a7-block-times-threads-64, code/bench/a7_blocks.py

## 2026-10-24 09:25 UTC  A7 block times group_amplitudes=8192
- **Goal:** Per-block kernel times of 5 circuits x 2 loads at n=26 with group_amplitudes=8192
- **Task:** A7
- **Method:** code/bench/gpurun a7_blocks.py --workloads ghz:damping:0.0019802,ghz:damping:0.019802,brickwork:damping:0.000280112,brickwork:damping:0.00280112,qft:damping:0.0002849,qft:damping:0.002849,qaoa:damping:0.000512821,qaoa:damping:0.00512821,grid:damping:0.00017094,grid:damping:0.0017094 --qubits 26 --label group_amplitudes=8192 --set group_amplitudes=8192
- **Outcome:** exit 2; outputs in data/20261024-092457-a7-block-times-group-amplitudes-8192
- **Next:** none
- **Refs:** data/20261024-092457-a7-block-times-group-amplitudes-8192, code/bench/a7_blocks.py

## 2026-10-24 09:24 UTC  A7 block times group_amplitudes=4096
- **Goal:** Per-block kernel times of 5 circuits x 2 loads at n=26 with group_amplitudes=4096
- **Task:** A7
- **Method:** code/bench/gpurun a7_blocks.py --workloads ghz:damping:0.0019802,ghz:damping:0.019802,brickwork:damping:0.000280112,brickwork:damping:0.00280112,qft:damping:0.0002849,qft:damping:0.002849,qaoa:damping:0.000512821,qaoa:damping:0.00512821,grid:damping:0.00017094,grid:damping:0.0017094 --qubits 26 --label group_amplitudes=4096 --set group_amplitudes=4096
- **Outcome:** exit 0; outputs in data/20261024-092441-a7-block-times-group-amplitudes-4096
- **Next:** none
- **Refs:** data/20261024-092441-a7-block-times-group-amplitudes-4096, code/bench/a7_blocks.py

## 2026-10-24 09:24 UTC  A7 block times group_amplitudes=1024
- **Goal:** Per-block kernel times of 5 circuits x 2 loads at n=26 with group_amplitudes=1024
- **Task:** A7
- **Method:** code/bench/gpurun a7_blocks.py --workloads ghz:damping:0.0019802,ghz:damping:0.019802,brickwork:damping:0.000280112,brickwork:damping:0.00280112,qft:damping:0.0002849,qft:damping:0.002849,qaoa:damping:0.000512821,qaoa:damping:0.00512821,grid:damping:0.00017094,grid:damping:0.0017094 --qubits 26 --label group_amplitudes=1024 --set group_amplitudes=1024
- **Outcome:** exit 0; outputs in data/20261024-092428-a7-block-times-group-amplitudes-1024
- **Next:** none
- **Refs:** data/20261024-092428-a7-block-times-group-amplitudes-1024, code/bench/a7_blocks.py

## 2026-10-24 09:24 UTC  A7 block times group_amplitudes=512
- **Goal:** Per-block kernel times of 5 circuits x 2 loads at n=26 with group_amplitudes=512
- **Task:** A7
- **Method:** code/bench/gpurun a7_blocks.py --workloads ghz:damping:0.0019802,ghz:damping:0.019802,brickwork:damping:0.000280112,brickwork:damping:0.00280112,qft:damping:0.0002849,qft:damping:0.002849,qaoa:damping:0.000512821,qaoa:damping:0.00512821,grid:damping:0.00017094,grid:damping:0.0017094 --qubits 26 --label group_amplitudes=512 --set group_amplitudes=512
- **Outcome:** exit 0; outputs in data/20261024-092412-a7-block-times-group-amplitudes-512
- **Next:** none
- **Refs:** data/20261024-092412-a7-block-times-group-amplitudes-512, code/bench/a7_blocks.py

## 2026-10-24 09:24 UTC  A10 tighter proposal bounds: theory and estimate
- **Goal:** Determine how much of the 2MN error-proposal term valid checkpoint-dependent bounds can avoid
- **Task:** A10
- **Method:** Validity proof (per-operation acceptance factors <= 1; rules D diagonal prefix and S single-qubit prefix); a10_estimate.py dry-run scaling of error passes per block, n=28 damping M=0.1/1, variants free/all/all+S/oracle
- **Outcome:** Free information: <=6% of passes (QFT), <=4% others; all populations: QFT 13-15%; rule S adds nothing (light-cone blocks); oracle limit 4-36% (GHZ most). Not worth implementing except for diagonal-heavy circuits
- **Next:** none (A10 done unless the human wants an implementation for QFT-like circuits)
- **Refs:** wiki/studies/tighter-bounds.md, code/bench/a10_estimate.py

## 2026-10-24 09:24 UTC  A7 block times stage_qubits=4
- **Goal:** Per-block kernel times of 5 circuits x 2 loads at n=26 with stage_qubits=4
- **Task:** A7
- **Method:** code/bench/gpurun a7_blocks.py --workloads ghz:damping:0.0019802,ghz:damping:0.019802,brickwork:damping:0.000280112,brickwork:damping:0.00280112,qft:damping:0.0002849,qft:damping:0.002849,qaoa:damping:0.000512821,qaoa:damping:0.00512821,grid:damping:0.00017094,grid:damping:0.0017094 --qubits 26 --label stage_qubits=4 --set stage_qubits=4
- **Outcome:** exit 0; outputs in data/20261024-092333-a7-block-times-stage-qubits-4
- **Next:** none
- **Refs:** data/20261024-092333-a7-block-times-stage-qubits-4, code/bench/a7_blocks.py

## 2026-10-24 09:23 UTC  A7 block times stage_qubits=2
- **Goal:** Per-block kernel times of 5 circuits x 2 loads at n=26 with stage_qubits=2
- **Task:** A7
- **Method:** code/bench/gpurun a7_blocks.py --workloads ghz:damping:0.0019802,ghz:damping:0.019802,brickwork:damping:0.000280112,brickwork:damping:0.00280112,qft:damping:0.0002849,qft:damping:0.002849,qaoa:damping:0.000512821,qaoa:damping:0.00512821,grid:damping:0.00017094,grid:damping:0.0017094 --qubits 26 --label stage_qubits=2 --set stage_qubits=2
- **Outcome:** exit 0; outputs in data/20261024-092310-a7-block-times-stage-qubits-2
- **Next:** none
- **Refs:** data/20261024-092310-a7-block-times-stage-qubits-2, code/bench/a7_blocks.py

## 2026-10-24 09:23 UTC  A10 dry-run estimate with oracle bound
- **Goal:** Same as the A10 estimate, plus the oracle limit (bounds = actual populations)
- **Task:** A10
- **Method:** code/noisecirc/.venv/bin/python code/bench/a10_estimate.py
- **Outcome:** exit 0; outputs in data/20261024-092215-a10-dry-run-estimate-with-oracle-bound
- **Next:** none
- **Refs:** data/20261024-092215-a10-dry-run-estimate-with-oracle-bound, code/bench/a10_estimate.py

## 2026-10-24 09:23 UTC  A7 block times pinned_bytes=128
- **Goal:** Per-block kernel times of 5 circuits x 2 loads at n=26 with pinned_bytes=128
- **Task:** A7
- **Method:** code/bench/gpurun a7_blocks.py --workloads ghz:damping:0.0019802,ghz:damping:0.019802,brickwork:damping:0.000280112,brickwork:damping:0.00280112,qft:damping:0.0002849,qft:damping:0.002849,qaoa:damping:0.000512821,qaoa:damping:0.00512821,grid:damping:0.00017094,grid:damping:0.0017094 --qubits 26 --label pinned_bytes=128 --set pinned_bytes=128
- **Outcome:** exit 0; outputs in data/20261024-092244-a7-block-times-pinned-bytes-128
- **Next:** none
- **Refs:** data/20261024-092244-a7-block-times-pinned-bytes-128, code/bench/a7_blocks.py

## 2026-10-24 09:22 UTC  A7 block times pinned_bytes=32
- **Goal:** Per-block kernel times of 5 circuits x 2 loads at n=26 with pinned_bytes=32
- **Task:** A7
- **Method:** code/bench/gpurun a7_blocks.py --workloads ghz:damping:0.0019802,ghz:damping:0.019802,brickwork:damping:0.000280112,brickwork:damping:0.00280112,qft:damping:0.0002849,qft:damping:0.002849,qaoa:damping:0.000512821,qaoa:damping:0.00512821,grid:damping:0.00017094,grid:damping:0.0017094 --qubits 26 --label pinned_bytes=32 --set pinned_bytes=32
- **Outcome:** exit 0; outputs in data/20261024-092217-a7-block-times-pinned-bytes-32
- **Next:** none
- **Refs:** data/20261024-092217-a7-block-times-pinned-bytes-32, code/bench/a7_blocks.py

## 2026-10-24 09:22 UTC  A7 block times pinned_bytes=16
- **Goal:** Per-block kernel times of 5 circuits x 2 loads at n=26 with pinned_bytes=16
- **Task:** A7
- **Method:** code/bench/gpurun a7_blocks.py --workloads ghz:damping:0.0019802,ghz:damping:0.019802,brickwork:damping:0.000280112,brickwork:damping:0.00280112,qft:damping:0.0002849,qft:damping:0.002849,qaoa:damping:0.000512821,qaoa:damping:0.00512821,grid:damping:0.00017094,grid:damping:0.0017094 --qubits 26 --label pinned_bytes=16 --set pinned_bytes=16
- **Outcome:** exit 0; outputs in data/20261024-092149-a7-block-times-pinned-bytes-16
- **Next:** none
- **Refs:** data/20261024-092149-a7-block-times-pinned-bytes-16, code/bench/a7_blocks.py

## 2026-10-24 09:21 UTC  A7 block times max_fused_qudits=10
- **Goal:** Per-block kernel times of 5 circuits x 2 loads at n=26 with max_fused_qudits=10
- **Task:** A7
- **Method:** code/bench/gpurun a7_blocks.py --workloads ghz:damping:0.0019802,ghz:damping:0.019802,brickwork:damping:0.000280112,brickwork:damping:0.00280112,qft:damping:0.0002849,qft:damping:0.002849,qaoa:damping:0.000512821,qaoa:damping:0.00512821,grid:damping:0.00017094,grid:damping:0.0017094 --qubits 26 --label max_fused_qudits=10 --set max_fused_qudits=10
- **Outcome:** exit 0; outputs in data/20261024-092121-a7-block-times-max-fused-qudits-10
- **Next:** none
- **Refs:** data/20261024-092121-a7-block-times-max-fused-qudits-10, code/bench/a7_blocks.py

## 2026-10-24 09:21 UTC  A10 dry-run estimate of tighter proposal bounds
- **Goal:** Estimate how many error proposals checkpoint-dependent bounds (rules D, S) avoid, n=28, damping M=0.1/1
- **Task:** A10
- **Method:** code/noisecirc/.venv/bin/python code/bench/a10_estimate.py
- **Outcome:** exit 0; outputs in data/20261024-092028-a10-dry-run-estimate-of-tighter-proposal-bounds
- **Next:** none
- **Refs:** data/20261024-092028-a10-dry-run-estimate-of-tighter-proposal-bounds, code/bench/a10_estimate.py

## 2026-10-24 09:21 UTC  A7 block times max_fused_qudits=8
- **Goal:** Per-block kernel times of 5 circuits x 2 loads at n=26 with max_fused_qudits=8
- **Task:** A7
- **Method:** code/bench/gpurun a7_blocks.py --workloads ghz:damping:0.0019802,ghz:damping:0.019802,brickwork:damping:0.000280112,brickwork:damping:0.00280112,qft:damping:0.0002849,qft:damping:0.002849,qaoa:damping:0.000512821,qaoa:damping:0.00512821,grid:damping:0.00017094,grid:damping:0.0017094 --qubits 26 --label max_fused_qudits=8 --set max_fused_qudits=8
- **Outcome:** exit 0; outputs in data/20261024-092055-a7-block-times-max-fused-qudits-8
- **Next:** none
- **Refs:** data/20261024-092055-a7-block-times-max-fused-qudits-8, code/bench/a7_blocks.py

## 2026-10-24 09:20 UTC  A7 block times max_fused_qudits=7
- **Goal:** Per-block kernel times of 5 circuits x 2 loads at n=26 with max_fused_qudits=7
- **Task:** A7
- **Method:** code/bench/gpurun a7_blocks.py --workloads ghz:damping:0.0019802,ghz:damping:0.019802,brickwork:damping:0.000280112,brickwork:damping:0.00280112,qft:damping:0.0002849,qft:damping:0.002849,qaoa:damping:0.000512821,qaoa:damping:0.00512821,grid:damping:0.00017094,grid:damping:0.0017094 --qubits 26 --label max_fused_qudits=7 --set max_fused_qudits=7
- **Outcome:** exit 0; outputs in data/20261024-092028-a7-block-times-max-fused-qudits-7
- **Next:** none
- **Refs:** data/20261024-092028-a7-block-times-max-fused-qudits-7, code/bench/a7_blocks.py

## 2026-10-24 09:20 UTC  A7 block times max_fused_qudits=6
- **Goal:** Per-block kernel times of 5 circuits x 2 loads at n=26 with max_fused_qudits=6
- **Task:** A7
- **Method:** code/bench/gpurun a7_blocks.py --workloads ghz:damping:0.0019802,ghz:damping:0.019802,brickwork:damping:0.000280112,brickwork:damping:0.00280112,qft:damping:0.0002849,qft:damping:0.002849,qaoa:damping:0.000512821,qaoa:damping:0.00512821,grid:damping:0.00017094,grid:damping:0.0017094 --qubits 26 --label max_fused_qudits=6 --set max_fused_qudits=6
- **Outcome:** exit 0; outputs in data/20261024-092000-a7-block-times-max-fused-qudits-6
- **Next:** none
- **Refs:** data/20261024-092000-a7-block-times-max-fused-qudits-6, code/bench/a7_blocks.py

## 2026-10-24 09:20 UTC  A7 block times max_fused_qudits=5
- **Goal:** Per-block kernel times of 5 circuits x 2 loads at n=26 with max_fused_qudits=5
- **Task:** A7
- **Method:** code/bench/gpurun a7_blocks.py --workloads ghz:damping:0.0019802,ghz:damping:0.019802,brickwork:damping:0.000280112,brickwork:damping:0.00280112,qft:damping:0.0002849,qft:damping:0.002849,qaoa:damping:0.000512821,qaoa:damping:0.00512821,grid:damping:0.00017094,grid:damping:0.0017094 --qubits 26 --label max_fused_qudits=5 --set max_fused_qudits=5
- **Outcome:** exit 0; outputs in data/20261024-091930-a7-block-times-max-fused-qudits-5
- **Next:** none
- **Refs:** data/20261024-091930-a7-block-times-max-fused-qudits-5, code/bench/a7_blocks.py

## 2026-10-24 09:19 UTC  A7 block times max_operations=256
- **Goal:** Per-block kernel times of 5 circuits x 2 loads at n=26 with max_operations=256
- **Task:** A7
- **Method:** code/bench/gpurun a7_blocks.py --workloads ghz:damping:0.0019802,ghz:damping:0.019802,brickwork:damping:0.000280112,brickwork:damping:0.00280112,qft:damping:0.0002849,qft:damping:0.002849,qaoa:damping:0.000512821,qaoa:damping:0.00512821,grid:damping:0.00017094,grid:damping:0.0017094 --qubits 26 --label max_operations=256 --set max_operations=256
- **Outcome:** exit 0; outputs in data/20261024-091917-a7-block-times-max-operations-256
- **Next:** none
- **Refs:** data/20261024-091917-a7-block-times-max-operations-256, code/bench/a7_blocks.py

## 2026-10-24 09:19 UTC  A7 block times max_operations=192
- **Goal:** Per-block kernel times of 5 circuits x 2 loads at n=26 with max_operations=192
- **Task:** A7
- **Method:** code/bench/gpurun a7_blocks.py --workloads ghz:damping:0.0019802,ghz:damping:0.019802,brickwork:damping:0.000280112,brickwork:damping:0.00280112,qft:damping:0.0002849,qft:damping:0.002849,qaoa:damping:0.000512821,qaoa:damping:0.00512821,grid:damping:0.00017094,grid:damping:0.0017094 --qubits 26 --label max_operations=192 --set max_operations=192
- **Outcome:** exit 0; outputs in data/20261024-091904-a7-block-times-max-operations-192
- **Next:** none
- **Refs:** data/20261024-091904-a7-block-times-max-operations-192, code/bench/a7_blocks.py

## 2026-10-24 09:19 UTC  A7 block times max_operations=96
- **Goal:** Per-block kernel times of 5 circuits x 2 loads at n=26 with max_operations=96
- **Task:** A7
- **Method:** code/bench/gpurun a7_blocks.py --workloads ghz:damping:0.0019802,ghz:damping:0.019802,brickwork:damping:0.000280112,brickwork:damping:0.00280112,qft:damping:0.0002849,qft:damping:0.002849,qaoa:damping:0.000512821,qaoa:damping:0.00512821,grid:damping:0.00017094,grid:damping:0.0017094 --qubits 26 --label max_operations=96 --set max_operations=96
- **Outcome:** exit 0; outputs in data/20261024-091846-a7-block-times-max-operations-96
- **Next:** none
- **Refs:** data/20261024-091846-a7-block-times-max-operations-96, code/bench/a7_blocks.py

## 2026-10-24 09:18 UTC  A7 block times max_operations=64
- **Goal:** Per-block kernel times of 5 circuits x 2 loads at n=26 with max_operations=64
- **Task:** A7
- **Method:** code/bench/gpurun a7_blocks.py --workloads ghz:damping:0.0019802,ghz:damping:0.019802,brickwork:damping:0.000280112,brickwork:damping:0.00280112,qft:damping:0.0002849,qft:damping:0.002849,qaoa:damping:0.000512821,qaoa:damping:0.00512821,grid:damping:0.00017094,grid:damping:0.0017094 --qubits 26 --label max_operations=64 --set max_operations=64
- **Outcome:** exit 0; outputs in data/20261024-091825-a7-block-times-max-operations-64
- **Next:** none
- **Refs:** data/20261024-091825-a7-block-times-max-operations-64, code/bench/a7_blocks.py

## 2026-10-24 09:18 UTC  A7 block times max_operations=48
- **Goal:** Per-block kernel times of 5 circuits x 2 loads at n=26 with max_operations=48
- **Task:** A7
- **Method:** code/bench/gpurun a7_blocks.py --workloads ghz:damping:0.0019802,ghz:damping:0.019802,brickwork:damping:0.000280112,brickwork:damping:0.00280112,qft:damping:0.0002849,qft:damping:0.002849,qaoa:damping:0.000512821,qaoa:damping:0.00512821,grid:damping:0.00017094,grid:damping:0.0017094 --qubits 26 --label max_operations=48 --set max_operations=48
- **Outcome:** exit 0; outputs in data/20261024-091801-a7-block-times-max-operations-48
- **Next:** none
- **Refs:** data/20261024-091801-a7-block-times-max-operations-48, code/bench/a7_blocks.py

## 2026-10-24 09:18 UTC  A7 block times max_operations=32
- **Goal:** Per-block kernel times of 5 circuits x 2 loads at n=26 with max_operations=32
- **Task:** A7
- **Method:** code/bench/gpurun a7_blocks.py --workloads ghz:damping:0.0019802,ghz:damping:0.019802,brickwork:damping:0.000280112,brickwork:damping:0.00280112,qft:damping:0.0002849,qft:damping:0.002849,qaoa:damping:0.000512821,qaoa:damping:0.00512821,grid:damping:0.00017094,grid:damping:0.0017094 --qubits 26 --label max_operations=32 --set max_operations=32
- **Outcome:** exit 0; outputs in data/20261024-091735-a7-block-times-max-operations-32
- **Next:** none
- **Refs:** data/20261024-091735-a7-block-times-max-operations-32, code/bench/a7_blocks.py

## 2026-10-24 09:17 UTC  A7 block times max_operations=24
- **Goal:** Per-block kernel times of 5 circuits x 2 loads at n=26 with max_operations=24
- **Task:** A7
- **Method:** code/bench/gpurun a7_blocks.py --workloads ghz:damping:0.0019802,ghz:damping:0.019802,brickwork:damping:0.000280112,brickwork:damping:0.00280112,qft:damping:0.0002849,qft:damping:0.002849,qaoa:damping:0.000512821,qaoa:damping:0.00512821,grid:damping:0.00017094,grid:damping:0.0017094 --qubits 26 --label max_operations=24 --set max_operations=24
- **Outcome:** exit 0; outputs in data/20261024-091708-a7-block-times-max-operations-24
- **Next:** none
- **Refs:** data/20261024-091708-a7-block-times-max-operations-24, code/bench/a7_blocks.py

## 2026-10-24 09:17 UTC  A7 block times max_operations=16
- **Goal:** Per-block kernel times of 5 circuits x 2 loads at n=26 with max_operations=16
- **Task:** A7
- **Method:** code/bench/gpurun a7_blocks.py --workloads ghz:damping:0.0019802,ghz:damping:0.019802,brickwork:damping:0.000280112,brickwork:damping:0.00280112,qft:damping:0.0002849,qft:damping:0.002849,qaoa:damping:0.000512821,qaoa:damping:0.00512821,grid:damping:0.00017094,grid:damping:0.0017094 --qubits 26 --label max_operations=16 --set max_operations=16
- **Outcome:** exit 0; outputs in data/20261024-091638-a7-block-times-max-operations-16
- **Next:** none
- **Refs:** data/20261024-091638-a7-block-times-max-operations-16, code/bench/a7_blocks.py

## 2026-10-24 09:16 UTC  A7 block times default
- **Goal:** Per-block kernel times of 5 circuits x 2 loads at n=26 with default
- **Task:** A7
- **Method:** code/bench/gpurun a7_blocks.py --workloads ghz:damping:0.0019802,ghz:damping:0.019802,brickwork:damping:0.000280112,brickwork:damping:0.00280112,qft:damping:0.0002849,qft:damping:0.002849,qaoa:damping:0.000512821,qaoa:damping:0.00512821,grid:damping:0.00017094,grid:damping:0.0017094 --qubits 26 --label default
- **Outcome:** exit 0; outputs in data/20261024-091611-a7-block-times-default
- **Next:** none
- **Refs:** data/20261024-091611-a7-block-times-default, code/bench/a7_blocks.py

## 2026-10-24 03:13 UTC  A6 robustness: shots and thermal relaxation
- **Goal:** Check the A6 comparison at 100/10000 shots and with thermal noise
- **Task:** A6
- **Method:** a2_runs.py and a6_runs.py at n=24: qft/qaoa damping M=0.01/0.1 with 100 and 10000 shots (noisecirc, aer_branch); qft/brickwork thermal M=0.1 (all simulators)
- **Outcome:** Aer branching / noisecirc: 10-30x (100 shots), 11-55x (10000 shots); thermal: 19-36x over Aer branching, 330-1000x over Aer per shot, 240-570x over CUDA-Q
- **Next:** none
- **Refs:** wiki/studies/competitors.md

## 2026-10-24 03:12 UTC  A6 thermal cudaq brickwork n=24
- **Goal:** cudaq with thermal relaxation at M=0.1, 100 shots
- **Task:** A6
- **Method:** code/bench/gpurun a6_runs.py --sim cudaq --circuit brickwork --qubits 24 --noise thermal --ps 0.000217865 --shots 100 --reps 1 --budget 400
- **Outcome:** exit 0; outputs in data/20261024-031241-a6-thermal-cudaq-brickwork-n-24
- **Next:** none
- **Refs:** data/20261024-031241-a6-thermal-cudaq-brickwork-n-24, code/bench/a6_runs.py

## 2026-10-24 03:12 UTC  A6 thermal aer_plain brickwork n=24
- **Goal:** aer_plain with thermal relaxation at M=0.1, 100 shots
- **Task:** A6
- **Method:** code/bench/gpurun a6_runs.py --sim aer_plain --circuit brickwork --qubits 24 --noise thermal --ps 0.000217865 --shots 100 --reps 1 --budget 400
- **Outcome:** exit 0; outputs in data/20261024-031218-a6-thermal-aer-plain-brickwork-n-24
- **Next:** none
- **Refs:** data/20261024-031218-a6-thermal-aer-plain-brickwork-n-24, code/bench/a6_runs.py

## 2026-10-24 03:12 UTC  A6 thermal aer_branch brickwork n=24
- **Goal:** aer_branch with thermal relaxation at M=0.1, 1000 shots
- **Task:** A6
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit brickwork --qubits 24 --noise thermal --ps 0.000217865 --shots 1000 --reps 1 --budget 400
- **Outcome:** exit 0; outputs in data/20261024-031202-a6-thermal-aer-branch-brickwork-n-24
- **Next:** none
- **Refs:** data/20261024-031202-a6-thermal-aer-branch-brickwork-n-24, code/bench/a6_runs.py

## 2026-10-24 03:12 UTC  A6 thermal noisecirc brickwork n=24
- **Goal:** noisecirc with thermal relaxation at M=0.1, 1000 shots
- **Task:** A6
- **Method:** code/bench/gpurun a2_runs.py --circuits brickwork --qubits 24 --noise thermal --ps 0.000217865 --shots 1000 --reps 2
- **Outcome:** exit 0; outputs in data/20261024-031153-a6-thermal-noisecirc-brickwork-n-24
- **Next:** none
- **Refs:** data/20261024-031153-a6-thermal-noisecirc-brickwork-n-24, code/bench/a2_runs.py

## 2026-10-24 03:11 UTC  A6 thermal cudaq qft n=24
- **Goal:** cudaq with thermal relaxation at M=0.1, 100 shots
- **Task:** A6
- **Method:** code/bench/gpurun a6_runs.py --sim cudaq --circuit qft --qubits 24 --noise thermal --ps 0.000222222 --shots 100 --reps 1 --budget 400
- **Outcome:** exit 0; outputs in data/20261024-031133-a6-thermal-cudaq-qft-n-24
- **Next:** none
- **Refs:** data/20261024-031133-a6-thermal-cudaq-qft-n-24, code/bench/a6_runs.py

## 2026-10-24 03:11 UTC  A6 thermal aer_plain qft n=24
- **Goal:** aer_plain with thermal relaxation at M=0.1, 100 shots
- **Task:** A6
- **Method:** code/bench/gpurun a6_runs.py --sim aer_plain --circuit qft --qubits 24 --noise thermal --ps 0.000222222 --shots 100 --reps 1 --budget 400
- **Outcome:** exit 0; outputs in data/20261024-031056-a6-thermal-aer-plain-qft-n-24
- **Next:** none
- **Refs:** data/20261024-031056-a6-thermal-aer-plain-qft-n-24, code/bench/a6_runs.py

## 2026-10-24 03:10 UTC  A6 thermal aer_branch qft n=24
- **Goal:** aer_branch with thermal relaxation at M=0.1, 1000 shots
- **Task:** A6
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit qft --qubits 24 --noise thermal --ps 0.000222222 --shots 1000 --reps 1 --budget 400
- **Outcome:** exit 0; outputs in data/20261024-031039-a6-thermal-aer-branch-qft-n-24
- **Next:** none
- **Refs:** data/20261024-031039-a6-thermal-aer-branch-qft-n-24, code/bench/a6_runs.py

## 2026-10-24 03:10 UTC  A6 thermal noisecirc qft n=24
- **Goal:** noisecirc with thermal relaxation at M=0.1, 1000 shots
- **Task:** A6
- **Method:** code/bench/gpurun a2_runs.py --circuits qft --qubits 24 --noise thermal --ps 0.000222222 --shots 1000 --reps 2
- **Outcome:** exit 0; outputs in data/20261024-031032-a6-thermal-noisecirc-qft-n-24
- **Next:** none
- **Refs:** data/20261024-031032-a6-thermal-noisecirc-qft-n-24, code/bench/a2_runs.py

## 2026-10-24 03:10 UTC  A6 shots aer_branch qaoa n=24 N=10000
- **Goal:** Aer shot branching with 10000 shots, damping M=0.01/0.1
- **Task:** A6
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit qaoa --qubits 24 --noise damping --ps 5.55556e-05,0.000555556 --shots 10000 --reps 1 --budget 400
- **Outcome:** exit 0; outputs in data/20261024-031008-a6-shots-aer-branch-qaoa-n-24-n-10000
- **Next:** none
- **Refs:** data/20261024-031008-a6-shots-aer-branch-qaoa-n-24-n-10000, code/bench/a6_runs.py

## 2026-10-24 03:10 UTC  A6 shots noisecirc qaoa n=24 N=10000
- **Goal:** noisecirc with 10000 shots, damping M=0.01/0.1
- **Task:** A6
- **Method:** code/bench/gpurun a2_runs.py --circuits qaoa --qubits 24 --noise damping --ps 5.55556e-05,0.000555556 --shots 10000 --reps 2
- **Outcome:** exit 0; outputs in data/20261024-031001-a6-shots-noisecirc-qaoa-n-24-n-10000
- **Next:** none
- **Refs:** data/20261024-031001-a6-shots-noisecirc-qaoa-n-24-n-10000, code/bench/a2_runs.py

## 2026-10-24 03:10 UTC  A6 shots aer_branch qaoa n=24 N=100
- **Goal:** Aer shot branching with 100 shots, damping M=0.01/0.1
- **Task:** A6
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit qaoa --qubits 24 --noise damping --ps 5.55556e-05,0.000555556 --shots 100 --reps 1 --budget 400
- **Outcome:** exit 0; outputs in data/20261024-030953-a6-shots-aer-branch-qaoa-n-24-n-100
- **Next:** none
- **Refs:** data/20261024-030953-a6-shots-aer-branch-qaoa-n-24-n-100, code/bench/a6_runs.py

## 2026-10-24 03:09 UTC  A6 shots noisecirc qaoa n=24 N=100
- **Goal:** noisecirc with 100 shots, damping M=0.01/0.1
- **Task:** A6
- **Method:** code/bench/gpurun a2_runs.py --circuits qaoa --qubits 24 --noise damping --ps 5.55556e-05,0.000555556 --shots 100 --reps 2
- **Outcome:** exit 0; outputs in data/20261024-030948-a6-shots-noisecirc-qaoa-n-24-n-100
- **Next:** none
- **Refs:** data/20261024-030948-a6-shots-noisecirc-qaoa-n-24-n-100, code/bench/a2_runs.py

## 2026-10-24 03:09 UTC  A6 shots aer_branch qft n=24 N=10000
- **Goal:** Aer shot branching with 10000 shots, damping M=0.01/0.1
- **Task:** A6
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit qft --qubits 24 --noise damping --ps 3.33333e-05,0.000333333 --shots 10000 --reps 1 --budget 400
- **Outcome:** exit 0; outputs in data/20261024-030848-a6-shots-aer-branch-qft-n-24-n-10000
- **Next:** none
- **Refs:** data/20261024-030848-a6-shots-aer-branch-qft-n-24-n-10000, code/bench/a6_runs.py

## 2026-10-24 03:09 UTC  Records: A3 figures, bench worktree, PROBLEMS and TASKS
- **Goal:** Reference remaining artefacts and record conceptual problems and proposals
- **Task:** A3
- **Method:** data/a3-figures (segments, collapse figures of A3); code/noisecirc-bench = git worktree of noisecirc branch bench/fixes that gpurun syncs (.gitignore entry added); PROBLEMS.md P001/P002 (closed); TASKS.md T001-T003 (open)
- **Outcome:** Recorded
- **Next:** Batch 5 (shots, thermal) for A6 robustness
- **Refs:** data/a3-figures, code/noisecirc-bench, memory/topics/gpu-environment.md

## 2026-10-24 03:08 UTC  A6 shots noisecirc qft n=24 N=10000
- **Goal:** noisecirc with 10000 shots, damping M=0.01/0.1
- **Task:** A6
- **Method:** code/bench/gpurun a2_runs.py --circuits qft --qubits 24 --noise damping --ps 3.33333e-05,0.000333333 --shots 10000 --reps 2
- **Outcome:** exit 0; outputs in data/20261024-030840-a6-shots-noisecirc-qft-n-24-n-10000
- **Next:** none
- **Refs:** data/20261024-030840-a6-shots-noisecirc-qft-n-24-n-10000, code/bench/a2_runs.py

## 2026-10-24 03:08 UTC  A6 shots aer_branch qft n=24 N=100
- **Goal:** Aer shot branching with 100 shots, damping M=0.01/0.1
- **Task:** A6
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit qft --qubits 24 --noise damping --ps 3.33333e-05,0.000333333 --shots 100 --reps 1 --budget 400
- **Outcome:** exit 0; outputs in data/20261024-030832-a6-shots-aer-branch-qft-n-24-n-100
- **Next:** none
- **Refs:** data/20261024-030832-a6-shots-aer-branch-qft-n-24-n-100, code/bench/a6_runs.py

## 2026-10-24 03:08 UTC  A6 shots noisecirc qft n=24 N=100
- **Goal:** noisecirc with 100 shots, damping M=0.01/0.1
- **Task:** A6
- **Method:** code/bench/gpurun a2_runs.py --circuits qft --qubits 24 --noise damping --ps 3.33333e-05,0.000333333 --shots 100 --reps 2
- **Outcome:** exit 0; outputs in data/20261024-030825-a6-shots-noisecirc-qft-n-24-n-100
- **Next:** none
- **Refs:** data/20261024-030825-a6-shots-noisecirc-qft-n-24-n-100, code/bench/a2_runs.py

## 2026-10-24 03:07 UTC  A6 analysis and competitors page
- **Goal:** Quantify noisecirc's speedup over Aer and CUDA-Q and split it into algorithm and implementation
- **Task:** A6
- **Method:** a6_analyze.py over data/*a6-* (n=24) incl. noisecirc variants; aer_dryrun pass counts; n=28 Aer branching / per-shot (20 shots) and noisecirc M=0.01 runs
- **Outcome:** Over Aer shot branching 6-52x (passes 2.7-30x where Aer fuses; time per pass 1.0-2.1x at M=1); over Aer per-shot/batched and CUDA-Q 27-7700x; at equal algorithm (noisecirc pershot_k2) 0.70-1.74x of the per-shot competitors (correcting the 0.7-1.4 of the earlier entry); gains: fusion 4-25x, sharing 2-270x, no norm passes 1.5x. n=28: Aer branching segfaults from M=0.1 (branches exceed GPU memory); where it ran noisecirc 8-41x faster
- **Next:** Final overview check; optional extra studies
- **Refs:** wiki/studies/competitors.md, data/a6-analysis, memory/tasks/A6.md

## 2026-10-24 03:05 UTC  A6 noisecirc brickwork n=28 M=0.01
- **Goal:** noisecirc at the A6 n=28 point M=0.01 (damping), 1000 shots
- **Task:** A6
- **Method:** code/bench/gpurun a2_runs.py --circuits brickwork --qubits 28 --noise damping --ps 2.42131e-05 --shots 1000 --reps 2
- **Outcome:** exit 0; outputs in data/20261024-030543-a6-noisecirc-brickwork-n-28-m-0-01
- **Next:** none
- **Refs:** data/20261024-030543-a6-noisecirc-brickwork-n-28-m-0-01, code/bench/a2_runs.py

## 2026-10-24 03:05 UTC  A6 noisecirc qft n=28 M=0.01
- **Goal:** noisecirc at the A6 n=28 point M=0.01 (damping), 1000 shots
- **Task:** A6
- **Method:** code/bench/gpurun a2_runs.py --circuits qft --qubits 28 --noise damping --ps 2.46305e-05 --shots 1000 --reps 2
- **Outcome:** exit 0; outputs in data/20261024-030536-a6-noisecirc-qft-n-28-m-0-01
- **Next:** none
- **Refs:** data/20261024-030536-a6-noisecirc-qft-n-28-m-0-01, code/bench/a2_runs.py

## 2026-10-24 03:05 UTC  A6 noisecirc qaoa n=28 M=0.01
- **Goal:** noisecirc at the A6 n=28 point M=0.01 (damping), 1000 shots
- **Task:** A6
- **Method:** code/bench/gpurun a2_runs.py --circuits qaoa --qubits 28 --noise damping --ps 4.7619e-05 --shots 1000 --reps 2
- **Outcome:** exit 0; outputs in data/20261024-030530-a6-noisecirc-qaoa-n-28-m-0-01
- **Next:** none
- **Refs:** data/20261024-030530-a6-noisecirc-qaoa-n-28-m-0-01, code/bench/a2_runs.py

## 2026-10-24 03:05 UTC  A6 noisecirc ghz n=28 M=0.01
- **Goal:** noisecirc at the A6 n=28 point M=0.01 (damping), 1000 shots
- **Task:** A6
- **Method:** code/bench/gpurun a2_runs.py --circuits ghz --qubits 28 --noise damping --ps 0.000183486 --shots 1000 --reps 2
- **Outcome:** exit 0; outputs in data/20261024-030525-a6-noisecirc-ghz-n-28-m-0-01
- **Next:** none
- **Refs:** data/20261024-030525-a6-noisecirc-ghz-n-28-m-0-01, code/bench/a2_runs.py

## 2026-10-24 03:05 UTC  A6 cudaq brickwork n=28
- **Goal:** cudaq on brickwork at n=28, damping M=0.1, 20 shots (per-shot time)
- **Task:** A6
- **Method:** code/bench/gpurun a6_runs.py --sim cudaq --circuit brickwork --qubits 28 --noise damping --ps 0.000242131 --shots 20 --reps 1 --budget 400
- **Outcome:** exit 0; outputs in data/20261024-030436-a6-cudaq-brickwork-n-28
- **Next:** none
- **Refs:** data/20261024-030436-a6-cudaq-brickwork-n-28, code/bench/a6_runs.py

## 2026-10-24 03:04 UTC  A6 aer_plain brickwork n=28
- **Goal:** aer_plain on brickwork at n=28, damping M=0.1, 20 shots (per-shot time)
- **Task:** A6
- **Method:** code/bench/gpurun a6_runs.py --sim aer_plain --circuit brickwork --qubits 28 --noise damping --ps 0.000242131 --shots 20 --reps 1 --budget 400
- **Outcome:** exit 0; outputs in data/20261024-030314-a6-aer-plain-brickwork-n-28
- **Next:** none
- **Refs:** data/20261024-030314-a6-aer-plain-brickwork-n-28, code/bench/a6_runs.py

## 2026-10-24 03:03 UTC  A6 aer_branch brickwork n=28
- **Goal:** Aer shot branching on brickwork at n=28 (GPU memory holds ~35 states), damping M=0.01/0.1/1, 1000 shots
- **Task:** A6
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit brickwork --qubits 28 --noise damping --ps 2.42131e-05,0.000242131,0.00242131 --shots 1000 --reps 1 --budget 400
- **Outcome:** exit 139; outputs in data/20261024-030204-a6-aer-branch-brickwork-n-28
- **Next:** none
- **Refs:** data/20261024-030204-a6-aer-branch-brickwork-n-28, code/bench/a6_runs.py

## 2026-10-24 03:02 UTC  A6 cudaq qft n=28
- **Goal:** cudaq on qft at n=28, damping M=0.1, 20 shots (per-shot time)
- **Task:** A6
- **Method:** code/bench/gpurun a6_runs.py --sim cudaq --circuit qft --qubits 28 --noise damping --ps 0.000246305 --shots 20 --reps 1 --budget 400
- **Outcome:** exit 0; outputs in data/20261024-030103-a6-cudaq-qft-n-28
- **Next:** none
- **Refs:** data/20261024-030103-a6-cudaq-qft-n-28, code/bench/a6_runs.py

## 2026-10-24 03:01 UTC  A6 aer_plain qft n=28
- **Goal:** aer_plain on qft at n=28, damping M=0.1, 20 shots (per-shot time)
- **Task:** A6
- **Method:** code/bench/gpurun a6_runs.py --sim aer_plain --circuit qft --qubits 28 --noise damping --ps 0.000246305 --shots 20 --reps 1 --budget 400
- **Outcome:** exit 0; outputs in data/20261024-025855-a6-aer-plain-qft-n-28
- **Next:** none
- **Refs:** data/20261024-025855-a6-aer-plain-qft-n-28, code/bench/a6_runs.py

## 2026-10-24 02:58 UTC  A6 aer_branch qft n=28
- **Goal:** Aer shot branching on qft at n=28 (GPU memory holds ~35 states), damping M=0.01/0.1/1, 1000 shots
- **Task:** A6
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit qft --qubits 28 --noise damping --ps 2.46305e-05,0.000246305,0.00246305 --shots 1000 --reps 1 --budget 400
- **Outcome:** exit 139; outputs in data/20261024-025454-a6-aer-branch-qft-n-28
- **Next:** none
- **Refs:** data/20261024-025454-a6-aer-branch-qft-n-28, code/bench/a6_runs.py

## 2026-10-24 02:54 UTC  A6 cudaq qaoa n=28
- **Goal:** cudaq on qaoa at n=28, damping M=0.1, 20 shots (per-shot time)
- **Task:** A6
- **Method:** code/bench/gpurun a6_runs.py --sim cudaq --circuit qaoa --qubits 28 --noise damping --ps 0.00047619 --shots 20 --reps 1 --budget 400
- **Outcome:** exit 0; outputs in data/20261024-025423-a6-cudaq-qaoa-n-28
- **Next:** none
- **Refs:** data/20261024-025423-a6-cudaq-qaoa-n-28, code/bench/a6_runs.py

## 2026-10-24 02:54 UTC  A6 aer_plain qaoa n=28
- **Goal:** aer_plain on qaoa at n=28, damping M=0.1, 20 shots (per-shot time)
- **Task:** A6
- **Method:** code/bench/gpurun a6_runs.py --sim aer_plain --circuit qaoa --qubits 28 --noise damping --ps 0.00047619 --shots 20 --reps 1 --budget 400
- **Outcome:** exit 0; outputs in data/20261024-025346-a6-aer-plain-qaoa-n-28
- **Next:** none
- **Refs:** data/20261024-025346-a6-aer-plain-qaoa-n-28, code/bench/a6_runs.py

## 2026-10-24 02:53 UTC  A6 aer_branch qaoa n=28
- **Goal:** Aer shot branching on qaoa at n=28 (GPU memory holds ~35 states), damping M=0.01/0.1/1, 1000 shots
- **Task:** A6
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit qaoa --qubits 28 --noise damping --ps 4.7619e-05,0.00047619,0.0047619 --shots 1000 --reps 1 --budget 400
- **Outcome:** exit 139; outputs in data/20261024-025312-a6-aer-branch-qaoa-n-28
- **Next:** none
- **Refs:** data/20261024-025312-a6-aer-branch-qaoa-n-28, code/bench/a6_runs.py

## 2026-10-24 02:53 UTC  A6 cudaq ghz n=28
- **Goal:** cudaq on ghz at n=28, damping M=0.1, 20 shots (per-shot time)
- **Task:** A6
- **Method:** code/bench/gpurun a6_runs.py --sim cudaq --circuit ghz --qubits 28 --noise damping --ps 0.00183486 --shots 20 --reps 1 --budget 400
- **Outcome:** exit 0; outputs in data/20261024-025300-a6-cudaq-ghz-n-28
- **Next:** none
- **Refs:** data/20261024-025300-a6-cudaq-ghz-n-28, code/bench/a6_runs.py

## 2026-10-24 02:53 UTC  A6 aer_plain ghz n=28
- **Goal:** aer_plain on ghz at n=28, damping M=0.1, 20 shots (per-shot time)
- **Task:** A6
- **Method:** code/bench/gpurun a6_runs.py --sim aer_plain --circuit ghz --qubits 28 --noise damping --ps 0.00183486 --shots 20 --reps 1 --budget 400
- **Outcome:** exit 0; outputs in data/20261024-025240-a6-aer-plain-ghz-n-28
- **Next:** none
- **Refs:** data/20261024-025240-a6-aer-plain-ghz-n-28, code/bench/a6_runs.py

## 2026-10-24 02:52 UTC  A6 aer_branch ghz n=28
- **Goal:** Aer shot branching on ghz at n=28 (GPU memory holds ~35 states), damping M=0.01/0.1/1, 1000 shots
- **Task:** A6
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit ghz --qubits 28 --noise damping --ps 0.000183486,0.00183486,0.0183486 --shots 1000 --reps 1 --budget 400
- **Outcome:** exit 139; outputs in data/20261024-025208-a6-aer-branch-ghz-n-28
- **Next:** none
- **Refs:** data/20261024-025208-a6-aer-branch-ghz-n-28, code/bench/a6_runs.py

## 2026-10-24 02:41 UTC  optimize_kraus fix v4 verified on GPU
- **Goal:** Check that keeping the dominant Kraus operator restores sparse kernels
- **Task:** A5
- **Method:** bench/fixes db41e9b: GPU tests; a2_blocks qft depolarizing --optimize-kraus; a2_runs brickwork/qft depolarizing optimize_kraus M=0.1/1 at n=28
- **Outcome:** 317+179 tests pass; QFT kernels 1.14/1.79 x t_bw (as default); optimize_kraus now 20-30% faster than default at M=1 (QFT 25-26 vs 32.6 s; brickwork 32.8 vs 47.0 s), equal at M=0.1; compile 22-67 s vs main 72-144 s
- **Next:** A6 page
- **Refs:** wiki/studies/noisecirc-issues.md

## 2026-10-24 02:35 UTC  A5 validation qft depolarizing optimized M=1 (fix v4)
- **Goal:** Depolarizing with optimize_kraus on qft, n=28, M=1, bench/fixes db41e9b
- **Task:** A5
- **Method:** code/bench/gpurun a2_runs.py --circuits qft --qubits 28 --noise depolarizing --ps 0.00123153 --shots 1000 --reps 2 --budget 430 --option optimize_kraus=1
- **Outcome:** exit 0; outputs in data/20261024-023351-a5-validation-qft-depolarizing-optimized-m-1-fix-v4
- **Next:** none
- **Refs:** data/20261024-023351-a5-validation-qft-depolarizing-optimized-m-1-fix-v4, code/bench/a2_runs.py

## 2026-10-24 02:33 UTC  A5 validation qft depolarizing optimized M=0.1 (fix v4)
- **Goal:** Depolarizing with optimize_kraus on qft, n=28, M=0.1, bench/fixes db41e9b
- **Task:** A5
- **Method:** code/bench/gpurun a2_runs.py --circuits qft --qubits 28 --noise depolarizing --ps 0.000123153 --shots 1000 --reps 2 --budget 430 --option optimize_kraus=1
- **Outcome:** exit 0; outputs in data/20261024-023316-a5-validation-qft-depolarizing-optimized-m-0-1-fix-v4
- **Next:** none
- **Refs:** data/20261024-023316-a5-validation-qft-depolarizing-optimized-m-0-1-fix-v4, code/bench/a2_runs.py

## 2026-10-24 02:33 UTC  A5 validation brickwork depolarizing optimized M=1 (fix v4)
- **Goal:** Depolarizing with optimize_kraus on brickwork, n=28, M=1, bench/fixes db41e9b
- **Task:** A5
- **Method:** code/bench/gpurun a2_runs.py --circuits brickwork --qubits 28 --noise depolarizing --ps 0.00121065 --shots 1000 --reps 2 --budget 430 --option optimize_kraus=1
- **Outcome:** exit 0; outputs in data/20261024-023133-a5-validation-brickwork-depolarizing-optimized-m-1-fix-v4
- **Next:** none
- **Refs:** data/20261024-023133-a5-validation-brickwork-depolarizing-optimized-m-1-fix-v4, code/bench/a2_runs.py

## 2026-10-24 02:31 UTC  A5 validation brickwork depolarizing optimized M=0.1 (fix v4)
- **Goal:** Depolarizing with optimize_kraus on brickwork, n=28, M=0.1, bench/fixes db41e9b
- **Task:** A5
- **Method:** code/bench/gpurun a2_runs.py --circuits brickwork --qubits 28 --noise depolarizing --ps 0.000121065 --shots 1000 --reps 2 --budget 430 --option optimize_kraus=1
- **Outcome:** exit 0; outputs in data/20261024-023045-a5-validation-brickwork-depolarizing-optimized-m-0-1-fix-v4
- **Next:** none
- **Refs:** data/20261024-023045-a5-validation-brickwork-depolarizing-optimized-m-0-1-fix-v4, code/bench/a2_runs.py

## 2026-10-24 02:30 UTC  A5 block pass times qft depolarizing n=28 optimize-kraus v4
- **Goal:** Kernel times of QFT blocks with optimize_kraus after keeping the dominant operator
- **Task:** A5
- **Method:** code/bench/gpurun a2_blocks.py --circuits qft --qubits 28 --noise depolarizing --p 0.000123 --optimize-kraus
- **Outcome:** exit 0; outputs in data/20261024-023021-a5-block-pass-times-qft-depolarizing-n-28-optimize-kraus-v4
- **Next:** none
- **Refs:** data/20261024-023021-a5-block-pass-times-qft-depolarizing-n-28-optimize-kraus-v4, code/bench/a2_blocks.py

## 2026-10-24 02:30 UTC  GPU tests of bench/fixes db41e9b
- **Goal:** Tests on the H100 after keeping the dominant Kraus operator
- **Task:** A5
- **Method:** code/bench/gpurun run_tests.py
- **Outcome:** exit 0; outputs in data/20261024-022958-gpu-tests-of-bench-fixes-db41e9b
- **Next:** none
- **Refs:** data/20261024-022958-gpu-tests-of-bench-fixes-db41e9b, code/bench/run_tests.py

## 2026-10-24 02:30 UTC  A6 competitor runs and noisecirc variants
- **Goal:** Time Aer (branching, batched, plain), CUDA-Q and noisecirc variants on ghz/brickwork/qft/qaoa at n=24, damping M=0.01/0.1/1, 1000 shots
- **Task:** A6
- **Method:** a6_runs.py, a2_runs.py, a6_variants.py (k2, pershot, pershot_k2); aer_dryrun.py counts Aer's passes from its own fused ops; heevx failures retried without Kraus fusion
- **Outcome:** noisecirc 5-45x faster than Aer shot branching, 40-7000x than Aer plain/batched and CUDA-Q; Aer branching needs 3-54x more passes; noisecirc pershot_k2 (Aer-like algorithm) matches the per-shot competitors' times within 0.7-1.4x
- **Next:** Final A6 analysis and wiki page
- **Refs:** data/a6-analysis, code/bench/aer_dryrun.py, code/bench/a6_variants.py

## 2026-10-24 02:30 UTC  A5 validation complete; optimize_kraus fix iterations
- **Goal:** Validate A4 predictions on GPU; resolve the optimize_kraus anomaly
- **Task:** A5
- **Method:** 27 a5-validation runs (n=28, 1000 shots) vs committed predictions (a5_compare.py); optimize_kraus fix v1 (second stage) -> v2 (oversampling limit, GPU test failure 1.76e-4 > tol) -> v3 (guard + 150 iterations, compile cost) -> v4 (first keep the dominant operator fixed: sparse kernels); block times qft depolarizing default vs optimize
- **Outcome:** Passes 0.86-1.13x, kernel-ratio times 1.00-1.33x, bandwidth model 1.28-2.42x (47/39 points). optimize_kraus v3: passes <= default but kernels 1.9x (dom) / 1.7x (gen) slower from lost sparsity (verified by block timing); v4 keeps the dominant operator diagonal and compiles 30x faster; GPU check running
- **Next:** Evaluate v4 on GPU; update issues/validation pages
- **Refs:** data/a5-comparison, wiki/studies/validation.md, wiki/studies/noisecirc-issues.md

## 2026-10-24 02:28 UTC  A5 block pass times qft depolarizing n=28 --optimize-kraus
- **Goal:** Kernel times of QFT blocks with depolarizing p=1.23e-4, with and without optimize_kraus (sparsity hypothesis)
- **Task:** A5
- **Method:** code/bench/gpurun a2_blocks.py --circuits qft --qubits 28 --noise depolarizing --p 0.000123 --optimize-kraus
- **Outcome:** exit 0; outputs in data/20261024-022752-a5-block-pass-times-qft-depolarizing-n-28-optimize-kraus
- **Next:** none
- **Refs:** data/20261024-022752-a5-block-pass-times-qft-depolarizing-n-28-optimize-kraus, code/bench/a2_blocks.py

## 2026-10-24 02:27 UTC  A5 block pass times qft depolarizing n=28 default
- **Goal:** Kernel times of QFT blocks with depolarizing p=1.23e-4, with and without optimize_kraus (sparsity hypothesis)
- **Task:** A5
- **Method:** code/bench/gpurun a2_blocks.py --circuits qft --qubits 28 --noise depolarizing --p 0.000123
- **Outcome:** exit 0; outputs in data/20261024-022734-a5-block-pass-times-qft-depolarizing-n-28-default
- **Next:** none
- **Refs:** data/20261024-022734-a5-block-pass-times-qft-depolarizing-n-28-default, code/bench/a2_blocks.py

## 2026-10-24 02:22 UTC  A5 validation qft depolarizing optimized M=1 (fix v3)
- **Goal:** Depolarizing with optimize_kraus on qft, n=28, M=1, bench/fixes 594dcd7
- **Task:** A5
- **Method:** code/bench/gpurun a2_runs.py --circuits qft --qubits 28 --noise depolarizing --ps 0.00123153 --shots 1000 --reps 2 --budget 430 --option optimize_kraus=1
- **Outcome:** exit 0; outputs in data/20261024-021947-a5-validation-qft-depolarizing-optimized-m-1-fix-v3
- **Next:** none
- **Refs:** data/20261024-021947-a5-validation-qft-depolarizing-optimized-m-1-fix-v3, code/bench/a2_runs.py

## 2026-10-24 02:19 UTC  A5 validation qft depolarizing optimized M=0.1 (fix v3)
- **Goal:** Depolarizing with optimize_kraus on qft, n=28, M=0.1, bench/fixes 594dcd7
- **Task:** A5
- **Method:** code/bench/gpurun a2_runs.py --circuits qft --qubits 28 --noise depolarizing --ps 0.000123153 --shots 1000 --reps 2 --budget 430 --option optimize_kraus=1
- **Outcome:** exit 0; outputs in data/20261024-021848-a5-validation-qft-depolarizing-optimized-m-0-1-fix-v3
- **Next:** none
- **Refs:** data/20261024-021848-a5-validation-qft-depolarizing-optimized-m-0-1-fix-v3, code/bench/a2_runs.py

## 2026-10-24 02:18 UTC  A5 validation brickwork depolarizing optimized M=1 (fix v3)
- **Goal:** Depolarizing with optimize_kraus on brickwork, n=28, M=1, bench/fixes 594dcd7
- **Task:** A5
- **Method:** code/bench/gpurun a2_runs.py --circuits brickwork --qubits 28 --noise depolarizing --ps 0.00121065 --shots 1000 --reps 2 --budget 430 --option optimize_kraus=1
- **Outcome:** exit 0; outputs in data/20261024-021532-a5-validation-brickwork-depolarizing-optimized-m-1-fix-v3
- **Next:** none
- **Refs:** data/20261024-021532-a5-validation-brickwork-depolarizing-optimized-m-1-fix-v3, code/bench/a2_runs.py

## 2026-10-24 02:15 UTC  A5 validation brickwork depolarizing optimized M=0.1 (fix v3)
- **Goal:** Depolarizing with optimize_kraus on brickwork, n=28, M=0.1, bench/fixes 594dcd7
- **Task:** A5
- **Method:** code/bench/gpurun a2_runs.py --circuits brickwork --qubits 28 --noise depolarizing --ps 0.000121065 --shots 1000 --reps 2 --budget 430 --option optimize_kraus=1
- **Outcome:** exit 0; outputs in data/20261024-021306-a5-validation-brickwork-depolarizing-optimized-m-0-1-fix-v3
- **Next:** none
- **Refs:** data/20261024-021306-a5-validation-brickwork-depolarizing-optimized-m-0-1-fix-v3, code/bench/a2_runs.py

## 2026-10-24 02:13 UTC  GPU tests of bench/fixes 594dcd7
- **Goal:** svpass and noisecirc tests on the H100 after the guarded second stage
- **Task:** A5
- **Method:** code/bench/gpurun run_tests.py
- **Outcome:** exit 0; outputs in data/20261024-021243-gpu-tests-of-bench-fixes-594dcd7
- **Next:** none
- **Refs:** data/20261024-021243-gpu-tests-of-bench-fixes-594dcd7, code/bench/run_tests.py

## 2026-10-24 02:11 UTC  A5 validation qft depolarizing optimized M=1 (fix v2)
- **Goal:** Depolarizing with optimize_kraus on qft, n=28, M=1, bench/fixes da5420c
- **Task:** A5
- **Method:** code/bench/gpurun a2_runs.py --circuits qft --qubits 28 --noise depolarizing --ps 0.00123153 --shots 1000 --reps 2 --budget 430 --option optimize_kraus=1
- **Outcome:** exit 0; outputs in data/20261024-020652-a5-validation-qft-depolarizing-optimized-m-1-fix-v2
- **Next:** none
- **Refs:** data/20261024-020652-a5-validation-qft-depolarizing-optimized-m-1-fix-v2, code/bench/a2_runs.py

## 2026-10-24 02:06 UTC  A5 validation qft depolarizing optimized M=0.1 (fix v2)
- **Goal:** Depolarizing with optimize_kraus on qft, n=28, M=0.1, bench/fixes da5420c
- **Task:** A5
- **Method:** code/bench/gpurun a2_runs.py --circuits qft --qubits 28 --noise depolarizing --ps 0.000123153 --shots 1000 --reps 2 --budget 430 --option optimize_kraus=1
- **Outcome:** exit 0; outputs in data/20261024-020335-a5-validation-qft-depolarizing-optimized-m-0-1-fix-v2
- **Next:** none
- **Refs:** data/20261024-020335-a5-validation-qft-depolarizing-optimized-m-0-1-fix-v2, code/bench/a2_runs.py

## 2026-10-24 02:03 UTC  A5 validation brickwork depolarizing optimized M=1 (fix v2)
- **Goal:** Depolarizing with optimize_kraus on brickwork, n=28, M=1, bench/fixes da5420c
- **Task:** A5
- **Method:** code/bench/gpurun a2_runs.py --circuits brickwork --qubits 28 --noise depolarizing --ps 0.00121065 --shots 1000 --reps 2 --budget 430 --option optimize_kraus=1
- **Outcome:** exit 124; outputs in data/20261024-015344-a5-validation-brickwork-depolarizing-optimized-m-1-fix-v2
- **Next:** none
- **Refs:** data/20261024-015344-a5-validation-brickwork-depolarizing-optimized-m-1-fix-v2, code/bench/a2_runs.py

## 2026-10-24 01:53 UTC  A5 validation brickwork depolarizing optimized M=0.1 (fix v2)
- **Goal:** Depolarizing with optimize_kraus on brickwork, n=28, M=0.1, bench/fixes da5420c
- **Task:** A5
- **Method:** code/bench/gpurun a2_runs.py --circuits brickwork --qubits 28 --noise depolarizing --ps 0.000121065 --shots 1000 --reps 2 --budget 430 --option optimize_kraus=1
- **Outcome:** exit 124; outputs in data/20261024-014353-a5-validation-brickwork-depolarizing-optimized-m-0-1-fix-v2
- **Next:** none
- **Refs:** data/20261024-014353-a5-validation-brickwork-depolarizing-optimized-m-0-1-fix-v2, code/bench/a2_runs.py

## 2026-10-24 01:43 UTC  GPU tests of bench/fixes (optimize_kraus fix, second commit)
- **Goal:** svpass and noisecirc test suites on the H100 after tightening the second stage
- **Task:** A5
- **Method:** code/bench/gpurun run_tests.py
- **Outcome:** exit 0; outputs in data/20261024-014259-gpu-tests-of-bench-fixes-optimize-kraus-fix-second-commit
- **Next:** none
- **Refs:** data/20261024-014259-gpu-tests-of-bench-fixes-optimize-kraus-fix-second-commit, code/bench/run_tests.py

## 2026-10-24 01:40 UTC  A6 aer_batched brickwork n=24 M=0.1 (rerun with heevx fallback)
- **Goal:** Rerun of the point that failed with heevx in Aer Kraus fusion
- **Task:** A6
- **Method:** code/bench/gpurun a6_runs.py --sim aer_batched --circuit brickwork --qubits 24 --noise damping --ps 0.000326797 --shots 1000 --reps 2
- **Outcome:** exit 0; outputs in data/20261024-013714-a6-aer-batched-brickwork-n-24-m-0-1-rerun-with-heevx-fallback
- **Next:** none
- **Refs:** data/20261024-013714-a6-aer-batched-brickwork-n-24-m-0-1-rerun-with-heevx-fallback, code/bench/a6_runs.py

## 2026-10-24 01:37 UTC  A6 aer_branch brickwork n=24 M=0.1 (rerun with heevx fallback)
- **Goal:** Rerun of the point that failed with heevx in Aer Kraus fusion
- **Task:** A6
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit brickwork --qubits 24 --noise damping --ps 0.000326797 --shots 1000 --reps 2
- **Outcome:** exit 0; outputs in data/20261024-013632-a6-aer-branch-brickwork-n-24-m-0-1-rerun-with-heevx-fallback
- **Next:** none
- **Refs:** data/20261024-013632-a6-aer-branch-brickwork-n-24-m-0-1-rerun-with-heevx-fallback, code/bench/a6_runs.py

## 2026-10-24 01:36 UTC  A5 validation qft depolarizing optimized (with fix)
- **Goal:** Depolarizing with optimize_kraus on qft, n=28, M=0.1,1, after fix/optimize-kraus-dominant
- **Task:** A5
- **Method:** code/bench/gpurun a2_runs.py --circuits qft --qubits 28 --noise depolarizing --ps 0.000123153,0.00123153 --shots 1000 --reps 2 --budget 430 --option optimize_kraus=1
- **Outcome:** exit 0; outputs in data/20261024-012859-a5-validation-qft-depolarizing-optimized-with-fix
- **Next:** none
- **Refs:** data/20261024-012859-a5-validation-qft-depolarizing-optimized-with-fix, code/bench/a2_runs.py

## 2026-10-24 01:28 UTC  A5 validation brickwork depolarizing optimized (with fix)
- **Goal:** Depolarizing with optimize_kraus on brickwork, n=28, M=0.1,1, after fix/optimize-kraus-dominant
- **Task:** A5
- **Method:** code/bench/gpurun a2_runs.py --circuits brickwork --qubits 28 --noise depolarizing --ps 0.000121065,0.00121065 --shots 1000 --reps 2 --budget 430 --option optimize_kraus=1
- **Outcome:** exit 124; outputs in data/20261024-011908-a5-validation-brickwork-depolarizing-optimized-with-fix
- **Next:** none
- **Refs:** data/20261024-011908-a5-validation-brickwork-depolarizing-optimized-with-fix, code/bench/a2_runs.py

## 2026-10-24 01:19 UTC  A6 noisecirc variant pershot_k2 qaoa n=24
- **Goal:** noisecirc with part of its algorithm off (pershot_k2) on qaoa, damping M=0.01/0.1/1, 1000 shots (per-shot variants: 100 single-shot runs scaled)
- **Task:** A6
- **Method:** code/bench/gpurun a6_variants.py --variant pershot_k2 --circuit qaoa --qubits 24 --noise damping --ps 5.55556e-05,0.000555556,0.00555556 --shots 1000
- **Outcome:** exit 0; outputs in data/20261024-011850-a6-noisecirc-variant-pershot-k2-qaoa-n-24
- **Next:** none
- **Refs:** data/20261024-011850-a6-noisecirc-variant-pershot-k2-qaoa-n-24, code/bench/a6_variants.py

## 2026-10-24 01:18 UTC  A6 noisecirc variant pershot qaoa n=24
- **Goal:** noisecirc with part of its algorithm off (pershot) on qaoa, damping M=0.01/0.1/1, 1000 shots (per-shot variants: 100 single-shot runs scaled)
- **Task:** A6
- **Method:** code/bench/gpurun a6_variants.py --variant pershot --circuit qaoa --qubits 24 --noise damping --ps 5.55556e-05,0.000555556,0.00555556 --shots 1000
- **Outcome:** exit 0; outputs in data/20261024-011842-a6-noisecirc-variant-pershot-qaoa-n-24
- **Next:** none
- **Refs:** data/20261024-011842-a6-noisecirc-variant-pershot-qaoa-n-24, code/bench/a6_variants.py

## 2026-10-24 01:18 UTC  A6 noisecirc variant k2 qaoa n=24
- **Goal:** noisecirc with part of its algorithm off (k2) on qaoa, damping M=0.01/0.1/1, 1000 shots (per-shot variants: 100 single-shot runs scaled)
- **Task:** A6
- **Method:** code/bench/gpurun a6_variants.py --variant k2 --circuit qaoa --qubits 24 --noise damping --ps 5.55556e-05,0.000555556,0.00555556 --shots 1000
- **Outcome:** exit 0; outputs in data/20261024-011807-a6-noisecirc-variant-k2-qaoa-n-24
- **Next:** none
- **Refs:** data/20261024-011807-a6-noisecirc-variant-k2-qaoa-n-24, code/bench/a6_variants.py

## 2026-10-24 01:18 UTC  A6 noisecirc variant pershot_k2 qft n=24
- **Goal:** noisecirc with part of its algorithm off (pershot_k2) on qft, damping M=0.01/0.1/1, 1000 shots (per-shot variants: 100 single-shot runs scaled)
- **Task:** A6
- **Method:** code/bench/gpurun a6_variants.py --variant pershot_k2 --circuit qft --qubits 24 --noise damping --ps 3.33333e-05,0.000333333,0.00333333 --shots 1000
- **Outcome:** exit 0; outputs in data/20261024-011718-a6-noisecirc-variant-pershot-k2-qft-n-24
- **Next:** none
- **Refs:** data/20261024-011718-a6-noisecirc-variant-pershot-k2-qft-n-24, code/bench/a6_variants.py

## 2026-10-24 01:17 UTC  A6 noisecirc variant pershot qft n=24
- **Goal:** noisecirc with part of its algorithm off (pershot) on qft, damping M=0.01/0.1/1, 1000 shots (per-shot variants: 100 single-shot runs scaled)
- **Task:** A6
- **Method:** code/bench/gpurun a6_variants.py --variant pershot --circuit qft --qubits 24 --noise damping --ps 3.33333e-05,0.000333333,0.00333333 --shots 1000
- **Outcome:** exit 0; outputs in data/20261024-011709-a6-noisecirc-variant-pershot-qft-n-24
- **Next:** none
- **Refs:** data/20261024-011709-a6-noisecirc-variant-pershot-qft-n-24, code/bench/a6_variants.py

## 2026-10-24 01:17 UTC  A6 noisecirc variant k2 qft n=24
- **Goal:** noisecirc with part of its algorithm off (k2) on qft, damping M=0.01/0.1/1, 1000 shots (per-shot variants: 100 single-shot runs scaled)
- **Task:** A6
- **Method:** code/bench/gpurun a6_variants.py --variant k2 --circuit qft --qubits 24 --noise damping --ps 3.33333e-05,0.000333333,0.00333333 --shots 1000
- **Outcome:** exit 0; outputs in data/20261024-011441-a6-noisecirc-variant-k2-qft-n-24
- **Next:** none
- **Refs:** data/20261024-011441-a6-noisecirc-variant-k2-qft-n-24, code/bench/a6_variants.py

## 2026-10-24 01:14 UTC  A6 noisecirc variant pershot_k2 brickwork n=24
- **Goal:** noisecirc with part of its algorithm off (pershot_k2) on brickwork, damping M=0.01/0.1/1, 1000 shots (per-shot variants: 100 single-shot runs scaled)
- **Task:** A6
- **Method:** code/bench/gpurun a6_variants.py --variant pershot_k2 --circuit brickwork --qubits 24 --noise damping --ps 3.26797e-05,0.000326797,0.00326797 --shots 1000
- **Outcome:** exit 0; outputs in data/20261024-011412-a6-noisecirc-variant-pershot-k2-brickwork-n-24
- **Next:** none
- **Refs:** data/20261024-011412-a6-noisecirc-variant-pershot-k2-brickwork-n-24, code/bench/a6_variants.py

## 2026-10-24 01:14 UTC  A6 noisecirc variant pershot brickwork n=24
- **Goal:** noisecirc with part of its algorithm off (pershot) on brickwork, damping M=0.01/0.1/1, 1000 shots (per-shot variants: 100 single-shot runs scaled)
- **Task:** A6
- **Method:** code/bench/gpurun a6_variants.py --variant pershot --circuit brickwork --qubits 24 --noise damping --ps 3.26797e-05,0.000326797,0.00326797 --shots 1000
- **Outcome:** exit 0; outputs in data/20261024-011402-a6-noisecirc-variant-pershot-brickwork-n-24
- **Next:** none
- **Refs:** data/20261024-011402-a6-noisecirc-variant-pershot-brickwork-n-24, code/bench/a6_variants.py

## 2026-10-24 01:14 UTC  A6 noisecirc variant k2 brickwork n=24
- **Goal:** noisecirc with part of its algorithm off (k2) on brickwork, damping M=0.01/0.1/1, 1000 shots (per-shot variants: 100 single-shot runs scaled)
- **Task:** A6
- **Method:** code/bench/gpurun a6_variants.py --variant k2 --circuit brickwork --qubits 24 --noise damping --ps 3.26797e-05,0.000326797,0.00326797 --shots 1000
- **Outcome:** exit 0; outputs in data/20261024-011239-a6-noisecirc-variant-k2-brickwork-n-24
- **Next:** none
- **Refs:** data/20261024-011239-a6-noisecirc-variant-k2-brickwork-n-24, code/bench/a6_variants.py

## 2026-10-24 01:12 UTC  A6 noisecirc variant pershot_k2 ghz n=24
- **Goal:** noisecirc with part of its algorithm off (pershot_k2) on ghz, damping M=0.01/0.1/1, 1000 shots (per-shot variants: 100 single-shot runs scaled)
- **Task:** A6
- **Method:** code/bench/gpurun a6_variants.py --variant pershot_k2 --circuit ghz --qubits 24 --noise damping --ps 0.000215054,0.00215054,0.0215054 --shots 1000
- **Outcome:** exit 0; outputs in data/20261024-011230-a6-noisecirc-variant-pershot-k2-ghz-n-24
- **Next:** none
- **Refs:** data/20261024-011230-a6-noisecirc-variant-pershot-k2-ghz-n-24, code/bench/a6_variants.py

## 2026-10-24 01:12 UTC  A6 noisecirc variant pershot ghz n=24
- **Goal:** noisecirc with part of its algorithm off (pershot) on ghz, damping M=0.01/0.1/1, 1000 shots (per-shot variants: 100 single-shot runs scaled)
- **Task:** A6
- **Method:** code/bench/gpurun a6_variants.py --variant pershot --circuit ghz --qubits 24 --noise damping --ps 0.000215054,0.00215054,0.0215054 --shots 1000
- **Outcome:** exit 0; outputs in data/20261024-011224-a6-noisecirc-variant-pershot-ghz-n-24
- **Next:** none
- **Refs:** data/20261024-011224-a6-noisecirc-variant-pershot-ghz-n-24, code/bench/a6_variants.py

## 2026-10-24 01:12 UTC  A6 noisecirc variant k2 ghz n=24
- **Goal:** noisecirc with part of its algorithm off (k2) on ghz, damping M=0.01/0.1/1, 1000 shots (per-shot variants: 100 single-shot runs scaled)
- **Task:** A6
- **Method:** code/bench/gpurun a6_variants.py --variant k2 --circuit ghz --qubits 24 --noise damping --ps 0.000215054,0.00215054,0.0215054 --shots 1000
- **Outcome:** exit 0; outputs in data/20261024-011214-a6-noisecirc-variant-k2-ghz-n-24
- **Next:** none
- **Refs:** data/20261024-011214-a6-noisecirc-variant-k2-ghz-n-24, code/bench/a6_variants.py

## 2026-10-24 01:12 UTC  A6 noisecirc brickwork n=24 (rerun)
- **Goal:** Rerun of the invalid run 00:43 (wrong branch)
- **Task:** A6
- **Method:** code/bench/gpurun a2_runs.py --circuits brickwork --qubits 24 --noise damping --ps 3.26797e-05,0.000326797,0.00326797 --shots 1000 --reps 2
- **Outcome:** exit 0; outputs in data/20261024-011201-a6-noisecirc-brickwork-n-24-rerun
- **Next:** none
- **Refs:** data/20261024-011201-a6-noisecirc-brickwork-n-24-rerun, code/bench/a2_runs.py

## 2026-10-24 01:12 UTC  GPU tests of bench/fixes (optimize_kraus fix)
- **Goal:** svpass and noisecirc test suites on the H100 for bench/fixes e00cabd
- **Task:** A5
- **Method:** code/bench/gpurun run_tests.py
- **Outcome:** exit 0; outputs in data/20261024-011123-gpu-tests-of-bench-fixes-optimize-kraus-fix
- **Next:** none
- **Refs:** data/20261024-011123-gpu-tests-of-bench-fixes-optimize-kraus-fix, code/bench/run_tests.py

## 2026-10-24 01:10 UTC  A6 cudaq qaoa n=24
- **Goal:** cudaq on qaoa, damping M=0.01/0.1/1, 100 shots, n=24
- **Task:** A6
- **Method:** code/bench/gpurun a6_runs.py --sim cudaq --circuit qaoa --qubits 24 --noise damping --ps 5.55556e-05,0.000555556,0.00555556 --shots 100 --reps 2
- **Outcome:** exit 0; outputs in data/20261024-011006-a6-cudaq-qaoa-n-24
- **Next:** none
- **Refs:** data/20261024-011006-a6-cudaq-qaoa-n-24, code/bench/a6_runs.py

## 2026-10-24 01:10 UTC  A6 aer_plain qaoa n=24
- **Goal:** aer_plain on qaoa, damping M=0.01/0.1/1, 100 shots, n=24
- **Task:** A6
- **Method:** code/bench/gpurun a6_runs.py --sim aer_plain --circuit qaoa --qubits 24 --noise damping --ps 5.55556e-05,0.000555556,0.00555556 --shots 100 --reps 2
- **Outcome:** exit 0; outputs in data/20261024-010922-a6-aer-plain-qaoa-n-24
- **Next:** none
- **Refs:** data/20261024-010922-a6-aer-plain-qaoa-n-24, code/bench/a6_runs.py

## 2026-10-24 01:09 UTC  A6 aer_batched qaoa n=24
- **Goal:** aer_batched on qaoa, damping M=0.01/0.1/1, 1000 shots, n=24
- **Task:** A6
- **Method:** code/bench/gpurun a6_runs.py --sim aer_batched --circuit qaoa --qubits 24 --noise damping --ps 5.55556e-05,0.000555556,0.00555556 --shots 1000 --reps 2
- **Outcome:** exit 0; outputs in data/20261024-010319-a6-aer-batched-qaoa-n-24
- **Next:** none
- **Refs:** data/20261024-010319-a6-aer-batched-qaoa-n-24, code/bench/a6_runs.py

## 2026-10-24 01:03 UTC  A6 aer_branch qaoa n=24
- **Goal:** aer_branch on qaoa, damping M=0.01/0.1/1, 1000 shots, n=24
- **Task:** A6
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit qaoa --qubits 24 --noise damping --ps 5.55556e-05,0.000555556,0.00555556 --shots 1000 --reps 2
- **Outcome:** exit 0; outputs in data/20261024-010235-a6-aer-branch-qaoa-n-24
- **Next:** none
- **Refs:** data/20261024-010235-a6-aer-branch-qaoa-n-24, code/bench/a6_runs.py

## 2026-10-24 01:02 UTC  A6 noisecirc qaoa n=24
- **Goal:** noisecirc reference at the A6 points: qaoa, damping M=0.01/0.1/1, 1000 shots
- **Task:** A6
- **Method:** code/bench/gpurun a2_runs.py --circuits qaoa --qubits 24 --noise damping --ps 5.55556e-05,0.000555556,0.00555556 --shots 1000 --reps 2
- **Outcome:** exit 0; outputs in data/20261024-010224-a6-noisecirc-qaoa-n-24
- **Next:** none
- **Refs:** data/20261024-010224-a6-noisecirc-qaoa-n-24, code/bench/a2_runs.py

## 2026-10-24 01:02 UTC  A6 cudaq qft n=24
- **Goal:** cudaq on qft, damping M=0.01/0.1/1, 100 shots, n=24
- **Task:** A6
- **Method:** code/bench/gpurun a6_runs.py --sim cudaq --circuit qft --qubits 24 --noise damping --ps 3.33333e-05,0.000333333,0.00333333 --shots 100 --reps 2
- **Outcome:** exit 0; outputs in data/20261024-010108-a6-cudaq-qft-n-24
- **Next:** none
- **Refs:** data/20261024-010108-a6-cudaq-qft-n-24, code/bench/a6_runs.py

## 2026-10-24 01:01 UTC  A6 aer_plain qft n=24
- **Goal:** aer_plain on qft, damping M=0.01/0.1/1, 100 shots, n=24
- **Task:** A6
- **Method:** code/bench/gpurun a6_runs.py --sim aer_plain --circuit qft --qubits 24 --noise damping --ps 3.33333e-05,0.000333333,0.00333333 --shots 100 --reps 2
- **Outcome:** exit 0; outputs in data/20261024-005858-a6-aer-plain-qft-n-24
- **Next:** none
- **Refs:** data/20261024-005858-a6-aer-plain-qft-n-24, code/bench/a6_runs.py

## 2026-10-24 00:58 UTC  A6 aer_batched qft n=24
- **Goal:** aer_batched on qft, damping M=0.01/0.1/1, 1000 shots, n=24
- **Task:** A6
- **Method:** code/bench/gpurun a6_runs.py --sim aer_batched --circuit qft --qubits 24 --noise damping --ps 3.33333e-05,0.000333333,0.00333333 --shots 1000 --reps 2
- **Outcome:** exit 0; outputs in data/20261024-005205-a6-aer-batched-qft-n-24
- **Next:** none
- **Refs:** data/20261024-005205-a6-aer-batched-qft-n-24, code/bench/a6_runs.py

## 2026-10-24 00:52 UTC  A6 aer_branch qft n=24
- **Goal:** aer_branch on qft, damping M=0.01/0.1/1, 1000 shots, n=24
- **Task:** A6
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit qft --qubits 24 --noise damping --ps 3.33333e-05,0.000333333,0.00333333 --shots 1000 --reps 2
- **Outcome:** exit 0; outputs in data/20261024-005038-a6-aer-branch-qft-n-24
- **Next:** none
- **Refs:** data/20261024-005038-a6-aer-branch-qft-n-24, code/bench/a6_runs.py

## 2026-10-24 00:50 UTC  A6 noisecirc qft n=24
- **Goal:** noisecirc reference at the A6 points: qft, damping M=0.01/0.1/1, 1000 shots
- **Task:** A6
- **Method:** code/bench/gpurun a2_runs.py --circuits qft --qubits 24 --noise damping --ps 3.33333e-05,0.000333333,0.00333333 --shots 1000 --reps 2
- **Outcome:** exit 0; outputs in data/20261024-005025-a6-noisecirc-qft-n-24
- **Next:** none
- **Refs:** data/20261024-005025-a6-noisecirc-qft-n-24, code/bench/a2_runs.py

## 2026-10-24 00:50 UTC  A6 cudaq brickwork n=24
- **Goal:** cudaq on brickwork, damping M=0.01/0.1/1, 100 shots, n=24
- **Task:** A6
- **Method:** code/bench/gpurun a6_runs.py --sim cudaq --circuit brickwork --qubits 24 --noise damping --ps 3.26797e-05,0.000326797,0.00326797 --shots 100 --reps 2
- **Outcome:** exit 0; outputs in data/20261024-004930-a6-cudaq-brickwork-n-24
- **Next:** none
- **Refs:** data/20261024-004930-a6-cudaq-brickwork-n-24, code/bench/a6_runs.py

## 2026-10-24 00:49 UTC  A6 aer_plain brickwork n=24
- **Goal:** aer_plain on brickwork, damping M=0.01/0.1/1, 100 shots, n=24
- **Task:** A6
- **Method:** code/bench/gpurun a6_runs.py --sim aer_plain --circuit brickwork --qubits 24 --noise damping --ps 3.26797e-05,0.000326797,0.00326797 --shots 100 --reps 2
- **Outcome:** exit 0; outputs in data/20261024-004733-a6-aer-plain-brickwork-n-24
- **Next:** none
- **Refs:** data/20261024-004733-a6-aer-plain-brickwork-n-24, code/bench/a6_runs.py

## 2026-10-24 00:47 UTC  A6 aer_batched brickwork n=24
- **Goal:** aer_batched on brickwork, damping M=0.01/0.1/1, 1000 shots, n=24
- **Task:** A6
- **Method:** code/bench/gpurun a6_runs.py --sim aer_batched --circuit brickwork --qubits 24 --noise damping --ps 3.26797e-05,0.000326797,0.00326797 --shots 1000 --reps 2
- **Outcome:** exit 0; outputs in data/20261024-004452-a6-aer-batched-brickwork-n-24
- **Next:** none
- **Refs:** data/20261024-004452-a6-aer-batched-brickwork-n-24, code/bench/a6_runs.py

## 2026-10-24 00:45 UTC  Fix: optimize_kraus spreads the no-error operator
- **Goal:** Explain why optimize_kraus made QFT/brickwork depolarizing runs slower (A5)
- **Task:** A5
- **Method:** Per-gate non-dominant proposal probability: cp(0.012) optimized set 0.022 vs minimal 5e-4 (degenerate optimal family of mixed-unitary sets); fix: second stage lowering the non-dominant bounds under an oversampling penalty; branch fix/optimize-kraus-dominant 4dca134 (+ regression test failing on main), merged into bench/fixes e00cabd
- **Outcome:** Optimized sets now have lower Z and fewer non-dominant proposals than minimal sets for depolarizing, GAD, thermal; damping unchanged; 163 CPU tests + 27 STA tests pass; GPU tests and rerun of the A5 optimize points pending
- **Next:** GPU tests and A5 reruns after the A6 batch
- **Refs:** wiki/studies/noisecirc-issues.md, code/noisecirc

## 2026-10-24 00:45 UTC  Invalid run: A6 noisecirc brickwork n=24 on wrong branch
- **Goal:** Record a run made with the wrong noisecirc code
- **Task:** A6
- **Method:** gpurun syncs code/noisecirc's working tree; it was switched to fix/optimize-kraus-dominant (main-based, without the squared-norms fix) 00:42-00:45 UTC while the A6 batch ran
- **Outcome:** data/20261024-004312-a6-noisecirc-brickwork-n-24 ran without fix/squared-norms-parallel; excluded, to be rerun. Aer/CUDA-Q runs unaffected
- **Next:** Rerun after the batch; make gpurun sync a dedicated worktree
- **Refs:** data/20261024-004312-a6-noisecirc-brickwork-n-24

## 2026-10-24 00:44 UTC  A6 aer_branch brickwork n=24
- **Goal:** aer_branch on brickwork, damping M=0.01/0.1/1, 1000 shots, n=24
- **Task:** A6
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit brickwork --qubits 24 --noise damping --ps 3.26797e-05,0.000326797,0.00326797 --shots 1000 --reps 2
- **Outcome:** exit 0; outputs in data/20261024-004330-a6-aer-branch-brickwork-n-24
- **Next:** none
- **Refs:** data/20261024-004330-a6-aer-branch-brickwork-n-24, code/bench/a6_runs.py

## 2026-10-24 00:43 UTC  A6 noisecirc brickwork n=24
- **Goal:** noisecirc reference at the A6 points: brickwork, damping M=0.01/0.1/1, 1000 shots
- **Task:** A6
- **Method:** code/bench/gpurun a2_runs.py --circuits brickwork --qubits 24 --noise damping --ps 3.26797e-05,0.000326797,0.00326797 --shots 1000 --reps 2
- **Outcome:** exit 0; outputs in data/20261024-004312-a6-noisecirc-brickwork-n-24
- **Next:** none
- **Refs:** data/20261024-004312-a6-noisecirc-brickwork-n-24, code/bench/a2_runs.py

## 2026-10-24 00:43 UTC  A6 cudaq ghz n=24
- **Goal:** cudaq on ghz, damping M=0.01/0.1/1, 100 shots, n=24
- **Task:** A6
- **Method:** code/bench/gpurun a6_runs.py --sim cudaq --circuit ghz --qubits 24 --noise damping --ps 0.000215054,0.00215054,0.0215054 --shots 100 --reps 2
- **Outcome:** exit 0; outputs in data/20261024-004257-a6-cudaq-ghz-n-24
- **Next:** none
- **Refs:** data/20261024-004257-a6-cudaq-ghz-n-24, code/bench/a6_runs.py

## 2026-10-24 00:42 UTC  A6 aer_plain ghz n=24
- **Goal:** aer_plain on ghz, damping M=0.01/0.1/1, 100 shots, n=24
- **Task:** A6
- **Method:** code/bench/gpurun a6_runs.py --sim aer_plain --circuit ghz --qubits 24 --noise damping --ps 0.000215054,0.00215054,0.0215054 --shots 100 --reps 2
- **Outcome:** exit 0; outputs in data/20261024-004234-a6-aer-plain-ghz-n-24
- **Next:** none
- **Refs:** data/20261024-004234-a6-aer-plain-ghz-n-24, code/bench/a6_runs.py

## 2026-10-24 00:42 UTC  A6 aer_batched ghz n=24
- **Goal:** aer_batched on ghz, damping M=0.01/0.1/1, 1000 shots, n=24
- **Task:** A6
- **Method:** code/bench/gpurun a6_runs.py --sim aer_batched --circuit ghz --qubits 24 --noise damping --ps 0.000215054,0.00215054,0.0215054 --shots 1000 --reps 2
- **Outcome:** exit 0; outputs in data/20261024-003956-a6-aer-batched-ghz-n-24
- **Next:** none
- **Refs:** data/20261024-003956-a6-aer-batched-ghz-n-24, code/bench/a6_runs.py

## 2026-10-24 00:39 UTC  A6 aer_branch ghz n=24
- **Goal:** aer_branch on ghz, damping M=0.01/0.1/1, 1000 shots, n=24
- **Task:** A6
- **Method:** code/bench/gpurun a6_runs.py --sim aer_branch --circuit ghz --qubits 24 --noise damping --ps 0.000215054,0.00215054,0.0215054 --shots 1000 --reps 2
- **Outcome:** exit 0; outputs in data/20261024-003938-a6-aer-branch-ghz-n-24
- **Next:** none
- **Refs:** data/20261024-003938-a6-aer-branch-ghz-n-24, code/bench/a6_runs.py

## 2026-10-24 00:39 UTC  A6 noisecirc ghz n=24
- **Goal:** noisecirc reference at the A6 points: ghz, damping M=0.01/0.1/1, 1000 shots
- **Task:** A6
- **Method:** code/bench/gpurun a2_runs.py --circuits ghz --qubits 24 --noise damping --ps 0.000215054,0.00215054,0.0215054 --shots 1000 --reps 2
- **Outcome:** exit 0; outputs in data/20261024-003929-a6-noisecirc-ghz-n-24
- **Next:** none
- **Refs:** data/20261024-003929-a6-noisecirc-ghz-n-24, code/bench/a2_runs.py

## 2026-10-24 00:39 UTC  A5 validation qft depolarizing optimized
- **Goal:** Mixed-unitary depolarizing at M=0.1,1 on qft, n=28 --option optimize_kraus=1
- **Task:** A5
- **Method:** code/bench/gpurun a2_runs.py --circuits qft --qubits 28 --noise depolarizing --ps 0.000123153,0.00123153 --shots 1000 --reps 2 --budget 430 --option optimize_kraus=1
- **Outcome:** exit 0; outputs in data/20261024-003516-a5-validation-qft-depolarizing-optimized
- **Next:** none
- **Refs:** data/20261024-003516-a5-validation-qft-depolarizing-optimized, code/bench/a2_runs.py

## 2026-10-24 00:35 UTC  A5 validation qft depolarizing
- **Goal:** Mixed-unitary depolarizing at M=0.1,1 on qft, n=28
- **Task:** A5
- **Method:** code/bench/gpurun a2_runs.py --circuits qft --qubits 28 --noise depolarizing --ps 0.000123153,0.00123153 --shots 1000 --reps 2 --budget 430
- **Outcome:** exit 0; outputs in data/20261024-003303-a5-validation-qft-depolarizing
- **Next:** none
- **Refs:** data/20261024-003303-a5-validation-qft-depolarizing, code/bench/a2_runs.py

## 2026-10-24 00:33 UTC  A5 validation qft dephasing
- **Goal:** Mixed-unitary dephasing at M=0.1,1 on qft, n=28
- **Task:** A5
- **Method:** code/bench/gpurun a2_runs.py --circuits qft --qubits 28 --noise dephasing --ps 0.000492611,0.00492611 --shots 1000 --reps 2 --budget 430
- **Outcome:** exit 0; outputs in data/20261024-003116-a5-validation-qft-dephasing
- **Next:** none
- **Refs:** data/20261024-003116-a5-validation-qft-dephasing, code/bench/a2_runs.py

## 2026-10-24 00:31 UTC  A5 validation brickwork depolarizing optimized
- **Goal:** Mixed-unitary depolarizing at M=0.1,1 on brickwork, n=28 --option optimize_kraus=1
- **Task:** A5
- **Method:** code/bench/gpurun a2_runs.py --circuits brickwork --qubits 28 --noise depolarizing --ps 0.000121065,0.00121065 --shots 1000 --reps 2 --budget 430 --option optimize_kraus=1
- **Outcome:** exit 0; outputs in data/20261024-002544-a5-validation-brickwork-depolarizing-optimized
- **Next:** none
- **Refs:** data/20261024-002544-a5-validation-brickwork-depolarizing-optimized, code/bench/a2_runs.py

## 2026-10-24 00:25 UTC  A5 validation brickwork depolarizing
- **Goal:** Mixed-unitary depolarizing at M=0.1,1 on brickwork, n=28
- **Task:** A5
- **Method:** code/bench/gpurun a2_runs.py --circuits brickwork --qubits 28 --noise depolarizing --ps 0.000121065,0.00121065 --shots 1000 --reps 2 --budget 430
- **Outcome:** exit 0; outputs in data/20261024-002237-a5-validation-brickwork-depolarizing
- **Next:** none
- **Refs:** data/20261024-002237-a5-validation-brickwork-depolarizing, code/bench/a2_runs.py

## 2026-10-24 00:22 UTC  A5 validation brickwork dephasing
- **Goal:** Mixed-unitary dephasing at M=0.1,1 on brickwork, n=28
- **Task:** A5
- **Method:** code/bench/gpurun a2_runs.py --circuits brickwork --qubits 28 --noise dephasing --ps 0.000484262,0.00484262 --shots 1000 --reps 2 --budget 430
- **Outcome:** exit 0; outputs in data/20261024-002032-a5-validation-brickwork-dephasing
- **Next:** none
- **Refs:** data/20261024-002032-a5-validation-brickwork-dephasing, code/bench/a2_runs.py

## 2026-10-24 00:20 UTC  A5 validation random gad
- **Goal:** Measured time and passes of random at n=28, gad at loads M=[0.1], 1000 shots, against A4 predictions
- **Task:** A5
- **Method:** code/bench/gpurun a2_runs.py --circuits random --qubits 28 --noise gad --ps 1.22865e-05 --shots 1000 --reps 2 --budget 430
- **Outcome:** exit 0; outputs in data/20261024-001831-a5-validation-random-gad
- **Next:** none
- **Refs:** data/20261024-001831-a5-validation-random-gad, code/bench/a2_runs.py

## 2026-10-24 00:18 UTC  A5 validation scramble gad
- **Goal:** Measured time and passes of scramble at n=28, gad at loads M=[0.1, 1.0], 1000 shots, against A4 predictions
- **Task:** A5
- **Method:** code/bench/gpurun a2_runs.py --circuits scramble --qubits 28 --noise gad --ps 0.000238095,0.00238095 --shots 1000 --reps 2 --budget 430
- **Outcome:** exit 0; outputs in data/20261024-001543-a5-validation-scramble-gad
- **Next:** none
- **Refs:** data/20261024-001543-a5-validation-scramble-gad, code/bench/a2_runs.py

## 2026-10-24 00:15 UTC  A5 validation qaoa gad
- **Goal:** Measured time and passes of qaoa at n=28, gad at loads M=[0.1, 1.0], 1000 shots, against A4 predictions
- **Task:** A5
- **Method:** code/bench/gpurun a2_runs.py --circuits qaoa --qubits 28 --noise gad --ps 0.00047619,0.0047619 --shots 1000 --reps 2 --budget 430
- **Outcome:** exit 0; outputs in data/20261024-001418-a5-validation-qaoa-gad
- **Next:** none
- **Refs:** data/20261024-001418-a5-validation-qaoa-gad, code/bench/a2_runs.py

## 2026-10-24 00:14 UTC  A5 validation qft gad
- **Goal:** Measured time and passes of qft at n=28, gad at loads M=[0.1, 1.0], 1000 shots, against A4 predictions
- **Task:** A5
- **Method:** code/bench/gpurun a2_runs.py --circuits qft --qubits 28 --noise gad --ps 0.000246305,0.00246305 --shots 1000 --reps 2 --budget 430
- **Outcome:** exit 0; outputs in data/20261024-001214-a5-validation-qft-gad
- **Next:** none
- **Refs:** data/20261024-001214-a5-validation-qft-gad, code/bench/a2_runs.py

## 2026-10-24 00:12 UTC  A5 validation grid gad
- **Goal:** Measured time and passes of grid at n=28, gad at loads M=[0.1, 1.0], 1000 shots, against A4 predictions
- **Task:** A5
- **Method:** code/bench/gpurun a2_runs.py --circuits grid --qubits 28 --noise gad --ps 0.000141443,0.00141443 --shots 1000 --reps 2 --budget 430
- **Outcome:** exit 0; outputs in data/20261024-000923-a5-validation-grid-gad
- **Next:** none
- **Refs:** data/20261024-000923-a5-validation-grid-gad, code/bench/a2_runs.py

## 2026-10-24 00:09 UTC  A5 validation brickwork gad
- **Goal:** Measured time and passes of brickwork at n=28, gad at loads M=[0.1, 1.0], 1000 shots, against A4 predictions
- **Task:** A5
- **Method:** code/bench/gpurun a2_runs.py --circuits brickwork --qubits 28 --noise gad --ps 0.000242131,0.00242131 --shots 1000 --reps 2 --budget 430
- **Outcome:** exit 0; outputs in data/20261024-000616-a5-validation-brickwork-gad
- **Next:** none
- **Refs:** data/20261024-000616-a5-validation-brickwork-gad, code/bench/a2_runs.py

## 2026-10-24 00:06 UTC  A5 validation ghz gad
- **Goal:** Measured time and passes of ghz at n=28, gad at loads M=[0.1, 1.0], 1000 shots, against A4 predictions
- **Task:** A5
- **Method:** code/bench/gpurun a2_runs.py --circuits ghz --qubits 28 --noise gad --ps 0.00183486,0.0183486 --shots 1000 --reps 2 --budget 430
- **Outcome:** exit 0; outputs in data/20261024-000541-a5-validation-ghz-gad
- **Next:** none
- **Refs:** data/20261024-000541-a5-validation-ghz-gad, code/bench/a2_runs.py

## 2026-10-24 00:05 UTC  A5 validation random thermal
- **Goal:** Measured time and passes of random at n=28, thermal at loads M=[0.1], 1000 shots, against A4 predictions
- **Task:** A5
- **Method:** code/bench/gpurun a2_runs.py --circuits random --qubits 28 --noise thermal --ps 8.19101e-06 --shots 1000 --reps 2 --budget 430
- **Outcome:** exit 0; outputs in data/20261024-000349-a5-validation-random-thermal
- **Next:** none
- **Refs:** data/20261024-000349-a5-validation-random-thermal, code/bench/a2_runs.py

## 2026-10-24 00:03 UTC  A5 validation scramble thermal
- **Goal:** Measured time and passes of scramble at n=28, thermal at loads M=[0.1, 1.0], 1000 shots, against A4 predictions
- **Task:** A5
- **Method:** code/bench/gpurun a2_runs.py --circuits scramble --qubits 28 --noise thermal --ps 0.00015873,0.0015873 --shots 1000 --reps 2 --budget 430
- **Outcome:** exit 0; outputs in data/20261024-000109-a5-validation-scramble-thermal
- **Next:** none
- **Refs:** data/20261024-000109-a5-validation-scramble-thermal, code/bench/a2_runs.py

## 2026-10-24 00:01 UTC  A5 validation qaoa thermal
- **Goal:** Measured time and passes of qaoa at n=28, thermal at loads M=[0.1, 1.0], 1000 shots, against A4 predictions
- **Task:** A5
- **Method:** code/bench/gpurun a2_runs.py --circuits qaoa --qubits 28 --noise thermal --ps 0.00031746,0.0031746 --shots 1000 --reps 2 --budget 430
- **Outcome:** exit 0; outputs in data/20261023-235952-a5-validation-qaoa-thermal
- **Next:** none
- **Refs:** data/20261023-235952-a5-validation-qaoa-thermal, code/bench/a2_runs.py

## 2026-10-23 23:59 UTC  A5 validation qft thermal
- **Goal:** Measured time and passes of qft at n=28, thermal at loads M=[0.1, 1.0], 1000 shots, against A4 predictions
- **Task:** A5
- **Method:** code/bench/gpurun a2_runs.py --circuits qft --qubits 28 --noise thermal --ps 0.000164204,0.00164204 --shots 1000 --reps 2 --budget 430
- **Outcome:** exit 0; outputs in data/20261023-235754-a5-validation-qft-thermal
- **Next:** none
- **Refs:** data/20261023-235754-a5-validation-qft-thermal, code/bench/a2_runs.py

## 2026-10-23 23:57 UTC  A5 validation grid thermal
- **Goal:** Measured time and passes of grid at n=28, thermal at loads M=[0.1, 1.0], 1000 shots, against A4 predictions
- **Task:** A5
- **Method:** code/bench/gpurun a2_runs.py --circuits grid --qubits 28 --noise thermal --ps 9.42951e-05,0.000942951 --shots 1000 --reps 2 --budget 430
- **Outcome:** exit 0; outputs in data/20261023-235506-a5-validation-grid-thermal
- **Next:** none
- **Refs:** data/20261023-235506-a5-validation-grid-thermal, code/bench/a2_runs.py

## 2026-10-23 23:55 UTC  A5 validation brickwork thermal
- **Goal:** Measured time and passes of brickwork at n=28, thermal at loads M=[0.1, 1.0], 1000 shots, against A4 predictions
- **Task:** A5
- **Method:** code/bench/gpurun a2_runs.py --circuits brickwork --qubits 28 --noise thermal --ps 0.000161421,0.00161421 --shots 1000 --reps 2 --budget 430
- **Outcome:** exit 0; outputs in data/20261023-235219-a5-validation-brickwork-thermal
- **Next:** none
- **Refs:** data/20261023-235219-a5-validation-brickwork-thermal, code/bench/a2_runs.py

## 2026-10-23 23:52 UTC  A5 validation ghz thermal
- **Goal:** Measured time and passes of ghz at n=28, thermal at loads M=[0.1, 1.0], 1000 shots, against A4 predictions
- **Task:** A5
- **Method:** code/bench/gpurun a2_runs.py --circuits ghz --qubits 28 --noise thermal --ps 0.00122324,0.0122324 --shots 1000 --reps 2 --budget 430
- **Outcome:** exit 0; outputs in data/20261023-235148-a5-validation-ghz-thermal
- **Next:** none
- **Refs:** data/20261023-235148-a5-validation-ghz-thermal, code/bench/a2_runs.py

## 2026-10-23 23:51 UTC  A5 validation random damping
- **Goal:** Measured time and passes of random at n=28, damping at loads M=[0.1], 1000 shots, against A4 predictions
- **Task:** A5
- **Method:** code/bench/gpurun a2_runs.py --circuits random --qubits 28 --noise damping --ps 1.22865e-05 --shots 1000 --reps 2 --budget 430
- **Outcome:** exit 0; outputs in data/20261023-234924-a5-validation-random-damping
- **Next:** none
- **Refs:** data/20261023-234924-a5-validation-random-damping, code/bench/a2_runs.py

## 2026-10-23 23:49 UTC  A5 validation scramble damping
- **Goal:** Measured time and passes of scramble at n=28, damping at loads M=[0.1, 1.0], 1000 shots, against A4 predictions
- **Task:** A5
- **Method:** code/bench/gpurun a2_runs.py --circuits scramble --qubits 28 --noise damping --ps 0.000238095,0.00238095 --shots 1000 --reps 2 --budget 430
- **Outcome:** exit 0; outputs in data/20261023-234638-a5-validation-scramble-damping
- **Next:** none
- **Refs:** data/20261023-234638-a5-validation-scramble-damping, code/bench/a2_runs.py

## 2026-10-23 23:46 UTC  A5 validation qaoa damping
- **Goal:** Measured time and passes of qaoa at n=28, damping at loads M=[0.1, 1.0], 1000 shots, against A4 predictions
- **Task:** A5
- **Method:** code/bench/gpurun a2_runs.py --circuits qaoa --qubits 28 --noise damping --ps 0.00047619,0.0047619 --shots 1000 --reps 2 --budget 430
- **Outcome:** exit 0; outputs in data/20261023-234519-a5-validation-qaoa-damping
- **Next:** none
- **Refs:** data/20261023-234519-a5-validation-qaoa-damping, code/bench/a2_runs.py

## 2026-10-23 23:45 UTC  A5 validation qft damping
- **Goal:** Measured time and passes of qft at n=28, damping at loads M=[0.1, 1.0], 1000 shots, against A4 predictions
- **Task:** A5
- **Method:** code/bench/gpurun a2_runs.py --circuits qft --qubits 28 --noise damping --ps 0.000246305,0.00246305 --shots 1000 --reps 2 --budget 430
- **Outcome:** exit 0; outputs in data/20261023-234333-a5-validation-qft-damping
- **Next:** none
- **Refs:** data/20261023-234333-a5-validation-qft-damping, code/bench/a2_runs.py

## 2026-10-23 23:44 UTC  A4 dry-run predictions depolarizing optimize_kraus
- **Goal:** Predicted passes for depolarizing with optimize_kraus (brickwork, qft; M=0.1, 1), before the A5 runs of these points
- **Task:** A4
- **Method:** code/noisecirc/.venv/bin/python code/bench/a4_predict.py depolarizing --optimize-kraus --circuits brickwork,qft --loads 0.1,1
- **Outcome:** exit 0; outputs in data/20261023-234140-a4-dry-run-predictions-depolarizing-optimize-kraus
- **Next:** none
- **Refs:** data/20261023-234140-a4-dry-run-predictions-depolarizing-optimize-kraus, code/bench/a4_predict.py

## 2026-10-23 23:43 UTC  A5 validation grid damping
- **Goal:** Measured time and passes of grid at n=28, damping at loads M=[0.1, 1.0], 1000 shots, against A4 predictions
- **Task:** A5
- **Method:** code/bench/gpurun a2_runs.py --circuits grid --qubits 28 --noise damping --ps 0.000141443,0.00141443 --shots 1000 --reps 2 --budget 430
- **Outcome:** exit 0; outputs in data/20261023-234042-a5-validation-grid-damping
- **Next:** none
- **Refs:** data/20261023-234042-a5-validation-grid-damping, code/bench/a2_runs.py

## 2026-10-23 23:40 UTC  A5 validation brickwork damping
- **Goal:** Measured time and passes of brickwork at n=28, damping at loads M=[0.1, 1.0], 1000 shots, against A4 predictions
- **Task:** A5
- **Method:** code/bench/gpurun a2_runs.py --circuits brickwork --qubits 28 --noise damping --ps 0.000242131,0.00242131 --shots 1000 --reps 2 --budget 430
- **Outcome:** exit 0; outputs in data/20261023-233749-a5-validation-brickwork-damping
- **Next:** none
- **Refs:** data/20261023-233749-a5-validation-brickwork-damping, code/bench/a2_runs.py

## 2026-10-23 23:39 UTC  A4 benchmark categories and predictions
- **Goal:** Choose benchmark circuits/categories and predict noisecirc's work without running them
- **Task:** A4
- **Method:** Dry-run predictions (a4_predict.py) for 7 circuits x 5 noise types x M=0.01..10 at n=28, 1000 shots; fusion width 3..9 at M=0/0.1/1 (a4_fusion.py); times via kernel ratios (a4_times.py)
- **Outcome:** Three fusion categories (chain, width-limited, gate-count-limited); at equal M passes per block and shot nearly universal across circuits and non-mixed-unitary noise types; fusion gain shrinks with M for few-block circuits; predicted times committed before A5
- **Next:** A5 validation runs (running)
- **Refs:** wiki/studies/benchmark-suite.md, data/a4-figures

## 2026-10-23 23:37 UTC  A5 validation ghz damping
- **Goal:** Measured time and passes of ghz at n=28, damping at loads M=[0.1, 1.0], 1000 shots, against A4 predictions
- **Task:** A5
- **Method:** code/bench/gpurun a2_runs.py --circuits ghz --qubits 28 --noise damping --ps 0.00183486,0.0183486 --shots 1000 --reps 2 --budget 430
- **Outcome:** exit 0; outputs in data/20261023-233718-a5-validation-ghz-damping
- **Next:** none
- **Refs:** data/20261023-233718-a5-validation-ghz-damping, code/bench/a2_runs.py

## 2026-10-23 23:36 UTC  A5 block pass times n=28 damping scramble
- **Goal:** Kernel ratios of the scramble circuit with damping at n=28
- **Task:** A5
- **Method:** code/bench/gpurun a2_blocks.py --circuits scramble --qubits 28 --noise damping --p 0.001
- **Outcome:** exit 0; outputs in data/20261023-233639-a5-block-pass-times-n-28-damping-scramble
- **Next:** none
- **Refs:** data/20261023-233639-a5-block-pass-times-n-28-damping-scramble, code/bench/a2_blocks.py

## 2026-10-23 23:36 UTC  A5 block pass times n=28 gad
- **Goal:** Kernel ratios with generalized damping (p=1e-3) at n=28
- **Task:** A5
- **Method:** code/bench/gpurun a2_blocks.py --circuits ghz,brickwork,qft,grid,qaoa,scramble,random --qubits 28 --noise gad --p 0.001
- **Outcome:** exit 0; outputs in data/20261023-233416-a5-block-pass-times-n-28-gad
- **Next:** none
- **Refs:** data/20261023-233416-a5-block-pass-times-n-28-gad, code/bench/a2_blocks.py

## 2026-10-23 23:35 UTC  A4 dry-run fusion width at fixed noise load
- **Goal:** Predicted passes against max_fused_qudits 3..9 at M=0, 0.1, 1 (n=28, damping, 1000 shots)
- **Task:** A4
- **Method:** code/noisecirc/.venv/bin/python code/bench/a4_fusion.py
- **Outcome:** exit 0; outputs in data/20261023-233200-a4-dry-run-fusion-width-at-fixed-noise-load
- **Next:** none
- **Refs:** data/20261023-233200-a4-dry-run-fusion-width-at-fixed-noise-load, code/bench/a4_fusion.py

## 2026-10-23 23:34 UTC  A5 block pass times n=28 thermal
- **Goal:** Kernel ratios of the seven circuits with thermal noise (p=1e-3) at n=28, for A5 time predictions
- **Task:** A5
- **Method:** code/bench/gpurun a2_blocks.py --circuits ghz,brickwork,qft,grid,qaoa,scramble,random --qubits 28 --noise thermal --p 0.001
- **Outcome:** exit 0; outputs in data/20261023-233216-a5-block-pass-times-n-28-thermal
- **Next:** none
- **Refs:** data/20261023-233216-a5-block-pass-times-n-28-thermal, code/bench/a2_blocks.py

## 2026-10-23 23:31 UTC  A2 max_operations at n=26 and A2 conclusion
- **Goal:** Find a regime where T ~ passes x t_bw within ~1.5
- **Task:** A2
- **Method:** a2_runs.py --option max_operations=32/48/64/128, five circuits, damping 1e-3/1e-2, n=26, bench/fixes; a2_timemodel.py over all bench/fixes runs
- **Outcome:** Defaults: T/(P t_bw) 1.24-2.58 (geomean 1.81); kernel-ratio model 0.95-1.37. max_operations=32: 1.29-1.84, wall time -6..-17% at p=1e-2, up to +25% at 1e-3
- **Next:** A4 study page from dry-run predictions; A5 validation runs
- **Refs:** wiki/studies/block-pass-time.md, data/a2-figures, data/a2-timemodel

## 2026-10-23 23:29 UTC  A2 max_operations=128 n=26 (bench/fixes)
- **Goal:** Effect of max_operations=128 on wall time, block passes and T/(P t_bw) at n=26 (one variable vs default 128)
- **Task:** A2
- **Method:** code/bench/gpurun a2_runs.py --circuits ghz,qft,qaoa,brickwork,grid --qubits 26 --ps 0.001,0.01 --shots 1000 --reps 2 --budget 500 --option max_operations=128
- **Outcome:** exit 0; outputs in data/20261023-232306-a2-max-operations-128-n-26-bench-fixes
- **Next:** none
- **Refs:** data/20261023-232306-a2-max-operations-128-n-26-bench-fixes, code/bench/a2_runs.py

## 2026-10-23 23:23 UTC  A2 max_operations=64 n=26 (bench/fixes)
- **Goal:** Effect of max_operations=64 on wall time, block passes and T/(P t_bw) at n=26 (one variable vs default 128)
- **Task:** A2
- **Method:** code/bench/gpurun a2_runs.py --circuits ghz,qft,qaoa,brickwork,grid --qubits 26 --ps 0.001,0.01 --shots 1000 --reps 2 --budget 500 --option max_operations=64
- **Outcome:** exit 0; outputs in data/20261023-231659-a2-max-operations-64-n-26-bench-fixes
- **Next:** none
- **Refs:** data/20261023-231659-a2-max-operations-64-n-26-bench-fixes, code/bench/a2_runs.py

## 2026-10-23 23:22 UTC  A4 dry-run predictions damping
- **Goal:** Predicted block passes of 7 circuit categories at n=28, noise damping at loads M=0.01..10, 1000 shots
- **Task:** A4
- **Method:** code/noisecirc/.venv/bin/python code/bench/a4_predict.py damping
- **Outcome:** exit 0; outputs in data/20261023-231143-a4-dry-run-predictions-damping
- **Next:** none
- **Refs:** data/20261023-231143-a4-dry-run-predictions-damping, code/bench/a4_predict.py

## 2026-10-23 23:20 UTC  A4 dry-run predictions thermal
- **Goal:** Predicted block passes of 7 circuit categories at n=28, noise thermal at loads M=0.01..10, 1000 shots
- **Task:** A4
- **Method:** code/noisecirc/.venv/bin/python code/bench/a4_predict.py thermal
- **Outcome:** exit 0; outputs in data/20261023-231143-a4-dry-run-predictions-thermal
- **Next:** none
- **Refs:** data/20261023-231143-a4-dry-run-predictions-thermal, code/bench/a4_predict.py

## 2026-10-23 23:20 UTC  A4 dry-run predictions gad
- **Goal:** Predicted block passes of 7 circuit categories at n=28, noise gad at loads M=0.01..10, 1000 shots
- **Task:** A4
- **Method:** code/noisecirc/.venv/bin/python code/bench/a4_predict.py gad
- **Outcome:** exit 0; outputs in data/20261023-231143-a4-dry-run-predictions-gad
- **Next:** none
- **Refs:** data/20261023-231143-a4-dry-run-predictions-gad, code/bench/a4_predict.py

## 2026-10-23 23:18 UTC  A4 dry-run predictions depolarizing
- **Goal:** Predicted block passes of 7 circuit categories at n=28, noise depolarizing at loads M=0.01..10, 1000 shots
- **Task:** A4
- **Method:** code/noisecirc/.venv/bin/python code/bench/a4_predict.py depolarizing
- **Outcome:** exit 0; outputs in data/20261023-231143-a4-dry-run-predictions-depolarizing
- **Next:** none
- **Refs:** data/20261023-231143-a4-dry-run-predictions-depolarizing, code/bench/a4_predict.py

## 2026-10-23 23:17 UTC  A4 dry-run predictions dephasing
- **Goal:** Predicted block passes of 7 circuit categories at n=28, noise dephasing at loads M=0.01..10, 1000 shots
- **Task:** A4
- **Method:** code/noisecirc/.venv/bin/python code/bench/a4_predict.py dephasing
- **Outcome:** exit 0; outputs in data/20261023-231143-a4-dry-run-predictions-dephasing
- **Next:** none
- **Refs:** data/20261023-231143-a4-dry-run-predictions-dephasing, code/bench/a4_predict.py

## 2026-10-23 23:16 UTC  A2 max_operations=48 n=26 (bench/fixes)
- **Goal:** Effect of max_operations=48 on wall time, block passes and T/(P t_bw) at n=26 (one variable vs default 128)
- **Task:** A2
- **Method:** code/bench/gpurun a2_runs.py --circuits ghz,qft,qaoa,brickwork,grid --qubits 26 --ps 0.001,0.01 --shots 1000 --reps 2 --budget 500 --option max_operations=48
- **Outcome:** exit 0; outputs in data/20261023-231110-a2-max-operations-48-n-26-bench-fixes
- **Next:** none
- **Refs:** data/20261023-231110-a2-max-operations-48-n-26-bench-fixes, code/bench/a2_runs.py

## 2026-10-23 23:11 UTC  A2 max_operations=32 n=26 (bench/fixes)
- **Goal:** Effect of max_operations=32 on wall time, block passes and T/(P t_bw) at n=26 (one variable vs default 128)
- **Task:** A2
- **Method:** code/bench/gpurun a2_runs.py --circuits ghz,qft,qaoa,brickwork,grid --qubits 26 --ps 0.001,0.01 --shots 1000 --reps 2 --budget 500 --option max_operations=32
- **Outcome:** exit 0; outputs in data/20261023-230530-a2-max-operations-32-n-26-bench-fixes
- **Next:** none
- **Refs:** data/20261023-230530-a2-max-operations-32-n-26-bench-fixes, code/bench/a2_runs.py

## 2026-10-23 23:05 UTC  A2 end-to-end runs n=28 grid (bench/fixes)
- **Goal:** Wall time and block passes of NoiseCirc runs (defaults, damping, 1000 shots) at n=28 on bench/fixes
- **Task:** A2
- **Method:** code/bench/gpurun a2_runs.py --circuits grid --qubits 28 --ps 0,0.0001,0.001,0.01 --shots 1000 --budget 420
- **Outcome:** exit 124; outputs in data/20261023-225513-a2-end-to-end-runs-n-28-grid-bench-fixes
- **Next:** none
- **Refs:** data/20261023-225513-a2-end-to-end-runs-n-28-grid-bench-fixes, code/bench/a2_runs.py

## 2026-10-23 22:55 UTC  A2 end-to-end runs n=28 brickwork (bench/fixes)
- **Goal:** Wall time and block passes of NoiseCirc runs (defaults, damping, 1000 shots) at n=28 on bench/fixes
- **Task:** A2
- **Method:** code/bench/gpurun a2_runs.py --circuits brickwork --qubits 28 --ps 0,0.0001,0.001,0.01 --shots 1000 --budget 420
- **Outcome:** exit 0; outputs in data/20261023-224903-a2-end-to-end-runs-n-28-brickwork-bench-fixes
- **Next:** none
- **Refs:** data/20261023-224903-a2-end-to-end-runs-n-28-brickwork-bench-fixes, code/bench/a2_runs.py

## 2026-10-23 22:49 UTC  A2 end-to-end runs n=28 ghz,qft,qaoa (bench/fixes)
- **Goal:** Wall time and block passes of NoiseCirc runs (defaults, damping, 1000 shots) at n=28 on bench/fixes
- **Task:** A2
- **Method:** code/bench/gpurun a2_runs.py --circuits ghz,qft,qaoa --qubits 28 --ps 0,0.0001,0.001,0.01 --shots 1000 --budget 420
- **Outcome:** exit 0; outputs in data/20261023-224113-a2-end-to-end-runs-n-28-ghz-qft-qaoa-bench-fixes
- **Next:** none
- **Refs:** data/20261023-224113-a2-end-to-end-runs-n-28-ghz-qft-qaoa-bench-fixes, code/bench/a2_runs.py

## 2026-10-23 22:42 UTC  A3 dry-run sweep noise grid,qaoa
- **Goal:** Complete the noise sweep (the full run timed out after ghz, brickwork, qft and most of random)
- **Task:** A3
- **Method:** code/noisecirc/.venv/bin/python code/bench/a3_sweep.py noise grid,qaoa
- **Outcome:** exit 0; outputs in data/20261023-223621-a3-dry-run-sweep-noise-grid-qaoa
- **Next:** none
- **Refs:** data/20261023-223621-a3-dry-run-sweep-noise-grid-qaoa, code/bench/a3_sweep.py

## 2026-10-23 22:41 UTC  A2 end-to-end runs n=26 (bench/fixes)
- **Goal:** Wall time and block passes of NoiseCirc runs (defaults, damping, 1000 shots) at n=26 on bench/fixes (main + parallel squared norms)
- **Task:** A2
- **Method:** code/bench/gpurun a2_runs.py --circuits ghz,qft,qaoa,brickwork,grid --qubits 26 --ps 0,0.0001,0.001,0.01 --shots 1000 --budget 480
- **Outcome:** exit 0; outputs in data/20261023-223250-a2-end-to-end-runs-n-26-bench-fixes
- **Next:** none
- **Refs:** data/20261023-223250-a2-end-to-end-runs-n-26-bench-fixes, code/bench/a2_runs.py

## 2026-10-23 22:36 UTC  A3 pass-count model validated against GPU runs
- **Goal:** Test the closed-form pass estimate and the dry run against measured block passes
- **Task:** A3
- **Method:** code/bench/a3_validate.py on 30 noisy points of the A2 main-branch runs (n=24-28, damping 1e-4..1e-2, 1000 shots)
- **Outcome:** Dry run within 0.89-1.12x of measured passes (rms 1.05x); closed form (with balls-into-bins dedup of error proposals) within 0.70-1.93x (rms 1.3x), worst GHZ p=1e-2 and QFT (qubits idle in |0>)
- **Next:** Write A3 study page; noise sweep plot
- **Refs:** data/a3-validation, code/bench/a3_model.py, code/bench/dryrun.py

## 2026-10-23 22:35 UTC  A3 dry-run sweep noise (tracking surrogate)
- **Goal:** Block and block-pass counts of six circuits at n=24 against one NoiseCirc parameter (noise), by dry run with the tracking surrogate (supersedes the killed mixed-surrogate sweeps of 21:31)
- **Task:** A3
- **Method:** code/noisecirc/.venv/bin/python code/bench/a3_sweep.py noise
- **Outcome:** blocked: timeout after 3000s; outputs in data/20261023-214521-a3-dry-run-sweep-noise-tracking-surrogate
- **Next:** none
- **Refs:** data/20261023-214521-a3-dry-run-sweep-noise-tracking-surrogate, code/bench/a3_sweep.py, code/bench/dryrun.py

## 2026-10-23 22:33 UTC  A3 dry-run sweep oversampling (tracking surrogate)
- **Goal:** Block and block-pass counts of six circuits at n=24 against one NoiseCirc parameter (oversampling), by dry run with the tracking surrogate (supersedes the killed mixed-surrogate sweeps of 21:31)
- **Task:** A3
- **Method:** code/noisecirc/.venv/bin/python code/bench/a3_sweep.py oversampling
- **Outcome:** exit 0; outputs in data/20261023-214521-a3-dry-run-sweep-oversampling-tracking-surrogate
- **Next:** none
- **Refs:** data/20261023-214521-a3-dry-run-sweep-oversampling-tracking-surrogate, code/bench/a3_sweep.py, code/bench/dryrun.py

## 2026-10-23 22:32 UTC  A2 end-to-end runs n=24 (bench/fixes)
- **Goal:** Wall time and block passes of NoiseCirc runs (defaults, damping, 1000 shots) at n=24 on bench/fixes (main + parallel squared norms)
- **Task:** A2
- **Method:** code/bench/gpurun a2_runs.py --circuits ghz,qft,qaoa,brickwork,grid --qubits 24 --ps 0,0.0001,0.001,0.01 --shots 1000 --budget 480
- **Outcome:** exit 0; outputs in data/20261023-223052-a2-end-to-end-runs-n-24-bench-fixes
- **Next:** none
- **Refs:** data/20261023-223052-a2-end-to-end-runs-n-24-bench-fixes, code/bench/a2_runs.py

## 2026-10-23 22:31 UTC  A6 runner tier-1 test
- **Goal:** Check a6_runs.py runs all four competitor configurations
- **Task:** A6
- **Method:** gpurun a6_runs.py brickwork n=20 p=1e-3 100 shots, sims aer_branch/aer_batched/aer_plain/cudaq
- **Outcome:** All run; Aer reports fusion method 'kraus' with max_fused_qubits 2 under noise; times 0.23/0.49/0.47/1.31 s (tier 1, not conclusions)
- **Next:** Full A6 runs after A2/A5
- **Refs:** code/bench/a6_runs.py

## 2026-10-23 22:31 UTC  Fix: parallel squared norms (svpass)
- **Goal:** Remove the per-call latency of svpass's squared_norms on long rows
- **Task:** A2
- **Method:** Two-stage fixed-order reduction (thread block per part of >=4096 chunk sums, warp per row over parts); branch fix/squared-norms-parallel a2d9fdd; merged with fix/elsman-doi into bench/fixes 619e018
- **Outcome:** svpass 317 + noisecirc 178 tests pass on H100; brickwork n=28 p=1e-3 1000 shots 35.1 s -> 20.9 s (GPU passes 17.7 s)
- **Next:** Use bench/fixes for all further runs; rerun A2 end-to-end
- **Refs:** wiki/studies/noisecirc-issues.md, code/noisecirc

## 2026-10-23 22:29 UTC  A2 profile n=28 with fix/squared-norms-parallel
- **Goal:** Check that the two-stage squared-norm reduction removes the ~4 ms per call overhead at n=28
- **Task:** A2
- **Method:** code/bench/gpurun a2_profile.py --circuits brickwork --qubits 28 --ps 0.000001,0.0001,0.001
- **Outcome:** exit 0; outputs in data/20261023-222839-a2-profile-n-28-with-fix-squared-norms-parallel
- **Next:** none
- **Refs:** data/20261023-222839-a2-profile-n-28-with-fix-squared-norms-parallel, code/bench/a2_profile.py

## 2026-10-23 22:26 UTC  A2 profile n=28
- **Goal:** Split NoiseCirc run time into GPU passes and host work (brickwork, damping 0/1e-4/1e-3, 1000 shots, n=28)
- **Task:** A2
- **Method:** code/bench/gpurun a2_profile.py --circuits brickwork --qubits 28 --ps 0.000001,0.0001,0.001
- **Outcome:** exit 0; outputs in data/20261023-222447-a2-profile-n-28
- **Next:** none
- **Refs:** data/20261023-222447-a2-profile-n-28, code/bench/a2_profile.py

## 2026-10-23 22:24 UTC  A2 profile n=24
- **Goal:** Split NoiseCirc run time into GPU passes and host work (brickwork, damping 0/1e-4/1e-3, 1000 shots, n=24)
- **Task:** A2
- **Method:** code/bench/gpurun a2_profile.py --circuits brickwork --qubits 24 --ps 0.000001,0.0001,0.001
- **Outcome:** exit 0; outputs in data/20261023-222439-a2-profile-n-24
- **Next:** none
- **Refs:** data/20261023-222439-a2-profile-n-24, code/bench/a2_profile.py

## 2026-10-23 22:24 UTC  A2 end-to-end runs n=28 random
- **Goal:** Wall time and block passes of NoiseCirc runs (defaults, damping, 1000 shots) at n=28
- **Task:** A2
- **Method:** code/bench/gpurun a2_runs.py --circuits random --qubits 28 --ps 0,0.0001,0.001,0.01 --shots 1000 --budget 450
- **Outcome:** exit 124; outputs in data/20261023-221419-a2-end-to-end-runs-n-28-random
- **Next:** none
- **Refs:** data/20261023-221419-a2-end-to-end-runs-n-28-random, code/bench/a2_runs.py

## 2026-10-23 22:22 UTC  A3 dry-run sweep segment (tracking, guarded)
- **Goal:** Block passes against blocks_per_segment by dry run; points with a segment ceiling above e^6 skipped (the unguarded run 21:45 was OOM-killed at random/p=1e-3/inf)
- **Task:** A3
- **Method:** code/noisecirc/.venv/bin/python code/bench/a3_sweep.py segment
- **Outcome:** exit 0; outputs in data/20261023-220449-a3-dry-run-sweep-segment-tracking-guarded
- **Next:** none
- **Refs:** data/20261023-220449-a3-dry-run-sweep-segment-tracking-guarded, code/bench/a3_sweep.py

## 2026-10-23 22:14 UTC  A2 end-to-end runs n=28 qaoa,grid
- **Goal:** Wall time and block passes of NoiseCirc runs (defaults, damping, 1000 shots) at n=28
- **Task:** A2
- **Method:** code/bench/gpurun a2_runs.py --circuits qaoa,grid --qubits 28 --ps 0,0.0001,0.001,0.01 --shots 1000 --budget 450
- **Outcome:** exit 124; outputs in data/20261023-220426-a2-end-to-end-runs-n-28-qaoa-grid
- **Next:** none
- **Refs:** data/20261023-220426-a2-end-to-end-runs-n-28-qaoa-grid, code/bench/a2_runs.py

## 2026-10-23 22:04 UTC  A3 dry-run sweep segment (tracking surrogate)
- **Goal:** Block and block-pass counts of six circuits at n=24 against one NoiseCirc parameter (segment), by dry run with the tracking surrogate (supersedes the killed mixed-surrogate sweeps of 21:31)
- **Task:** A3
- **Method:** code/noisecirc/.venv/bin/python code/bench/a3_sweep.py segment
- **Outcome:** exit -9; outputs in data/20261023-214521-a3-dry-run-sweep-segment-tracking-surrogate
- **Next:** none
- **Refs:** data/20261023-214521-a3-dry-run-sweep-segment-tracking-surrogate, code/bench/a3_sweep.py, code/bench/dryrun.py

## 2026-10-23 22:04 UTC  A2 end-to-end runs n=28 ghz,brickwork,qft
- **Goal:** Wall time and block passes of NoiseCirc runs (defaults, damping, 1000 shots) at n=28
- **Task:** A2
- **Method:** code/bench/gpurun a2_runs.py --circuits ghz,brickwork,qft --qubits 28 --ps 0,0.0001,0.001,0.01 --shots 1000 --budget 450
- **Outcome:** blocked: timeout after 600s; outputs in data/20261023-215006-a2-end-to-end-runs-n-28-ghz-brickwork-qft
- **Next:** none
- **Refs:** data/20261023-215006-a2-end-to-end-runs-n-28-ghz-brickwork-qft, code/bench/a2_runs.py

## 2026-10-23 21:50 UTC  A2 end-to-end runs n=26
- **Goal:** Wall time and block passes of NoiseCirc runs (defaults, damping, 1000 shots) at n=26 to test T = passes x t_bw
- **Task:** A2
- **Method:** code/bench/gpurun a2_runs.py --circuits ghz,brickwork,qft,random,grid,qaoa --qubits 26 --ps 0,0.0001,0.001,0.01 --shots 1000 --budget 480
- **Outcome:** exit 124; outputs in data/20261023-214014-a2-end-to-end-runs-n-26
- **Next:** none
- **Refs:** data/20261023-214014-a2-end-to-end-runs-n-26, code/bench/a2_runs.py

## 2026-10-23 21:45 UTC  A3 dry-run sweep fusion (tracking surrogate)
- **Goal:** Block and block-pass counts of six circuits at n=24 against one NoiseCirc parameter (fusion), by dry run with the tracking surrogate (supersedes the killed mixed-surrogate sweeps of 21:31)
- **Task:** A3
- **Method:** code/noisecirc/.venv/bin/python code/bench/a3_sweep.py fusion
- **Outcome:** exit 0; outputs in data/20261023-214521-a3-dry-run-sweep-fusion-tracking-surrogate
- **Next:** none
- **Refs:** data/20261023-214521-a3-dry-run-sweep-fusion-tracking-surrogate, code/bench/a3_sweep.py, code/bench/dryrun.py

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
