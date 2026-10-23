# Lab Book

Terse ledger of the project's history: one entry per experiment, simulation,
or investigation, newest first, failures included. Each entry states the
outcome and points to the evidence (`data/`, `code/`) and to the detail
(`memory/`, `wiki/`); it does not repeat them.

Approved tasks live in `PLAN.md`; name the task ID in each entry. Working
detail and know-how go in `memory/`, findings in `wiki/`, conceptual traps in
`PROBLEMS.md`, task proposals in `TASKS.md`.

---

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
