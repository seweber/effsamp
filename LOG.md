# Lab Book

Terse ledger of the project's history: one entry per experiment, simulation,
or investigation, newest first, failures included. Each entry states the
outcome and points to the evidence (`data/`, `code/`) and to the detail
(`memory/`, `wiki/`); it does not repeat them.

Approved tasks live in `PLAN.md`; name the task ID in each entry. Working
detail and know-how go in `memory/`, findings in `wiki/`, conceptual traps in
`PROBLEMS.md`, task proposals in `TASKS.md`.

---

## 2026-10-26 01:15 UTC  A13 pending GPU work: additive addresses, contraction order, free diagonals timed
- **Goal:** Time the A13 designs that were only predicted while GPU 0 was down; implement and time stages that ignore diagonal gates
- **Task:** A13
- **Method:** a16_time.py (n=26, sq3/sq4, c32/c64), a2_runs.py end to end (n=28, 3 seeds), free_diagonals in noisecirc feature/tensor-cores (fusion partition + codegen outside factors + sub-stages), checks a13_free_check.py, a13_free_errors_check.py, noisecirc GPU and statistical tests
- **Outcome:** additive+contraction: passes -6..-15% c32, -4..-9% c64; runs gm 0.585 (c32) / 0.891 (c64) vs defaults. free_diagonals correct but slower at sq4 (+3..+24%), faster only QFT sq3. Predictions: too low for additive/contraction, wrong sign for free diagonals
- **Next:** A17
- **Refs:** wiki/studies/kernel-regime.md, data/a13-analysis/e2e.svg, memory/tasks/A13.md, code/bench/a13_free_check.py, code/bench/a13_free_errors_check.py

## 2026-10-26 01:13 UTC  A13 free diagonals timing complex64 sq4 free 1 n=26
- **Goal:** Mean dominant pass time over t_bw with stage_contraction and additive_addresses, free_diagonals=1, complex64, 4-qubit stages
- **Task:** A13
- **Method:** code/bench/gpurun -s noisecirc a16_time.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --set dtype=complex64 --set stage_qubits=4 --set stage_contraction=1 --set additive_addresses=1 --set free_diagonals=1 --variant base
- **Outcome:** exit 0; outputs in data/20261026-011240-a13-free-diagonals-timing-complex64-sq4-free-1-n-26
- **Next:** none
- **Refs:** data/20261026-011240-a13-free-diagonals-timing-complex64-sq4-free-1-n-26

## 2026-10-26 01:12 UTC  A13 free diagonals timing complex64 sq4 free 0 n=26
- **Goal:** Mean dominant pass time over t_bw with stage_contraction and additive_addresses, free_diagonals=0, complex64, 4-qubit stages
- **Task:** A13
- **Method:** code/bench/gpurun -s noisecirc a16_time.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --set dtype=complex64 --set stage_qubits=4 --set stage_contraction=1 --set additive_addresses=1 --set free_diagonals=0 --variant base
- **Outcome:** exit 0; outputs in data/20261026-011148-a13-free-diagonals-timing-complex64-sq4-free-0-n-26
- **Next:** none
- **Refs:** data/20261026-011148-a13-free-diagonals-timing-complex64-sq4-free-0-n-26

## 2026-10-26 01:11 UTC  A13 free diagonals timing complex64 sq3 free 1 n=26
- **Goal:** Mean dominant pass time over t_bw with stage_contraction and additive_addresses, free_diagonals=1, complex64, 3-qubit stages
- **Task:** A13
- **Method:** code/bench/gpurun -s noisecirc a16_time.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --set dtype=complex64 --set stage_qubits=3 --set stage_contraction=1 --set additive_addresses=1 --set free_diagonals=1 --variant base
- **Outcome:** exit 0; outputs in data/20261026-011137-a13-free-diagonals-timing-complex64-sq3-free-1-n-26
- **Next:** none
- **Refs:** data/20261026-011137-a13-free-diagonals-timing-complex64-sq3-free-1-n-26

## 2026-10-26 01:11 UTC  A13 free diagonals timing complex64 sq3 free 0 n=26
- **Goal:** Mean dominant pass time over t_bw with stage_contraction and additive_addresses, free_diagonals=0, complex64, 3-qubit stages
- **Task:** A13
- **Method:** code/bench/gpurun -s noisecirc a16_time.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --set dtype=complex64 --set stage_qubits=3 --set stage_contraction=1 --set additive_addresses=1 --set free_diagonals=0 --variant base
- **Outcome:** exit 0; outputs in data/20261026-011123-a13-free-diagonals-timing-complex64-sq3-free-0-n-26
- **Next:** none
- **Refs:** data/20261026-011123-a13-free-diagonals-timing-complex64-sq3-free-0-n-26

## 2026-10-26 01:11 UTC  A13 free diagonals timing complex32 sq4 free 1 n=26
- **Goal:** Mean dominant pass time over t_bw with stage_contraction and additive_addresses, free_diagonals=1, complex32, 4-qubit stages
- **Task:** A13
- **Method:** code/bench/gpurun -s noisecirc a16_time.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --set dtype=complex32 --set stage_qubits=4 --set stage_contraction=1 --set additive_addresses=1 --set free_diagonals=1 --variant base
- **Outcome:** exit 0; outputs in data/20261026-011055-a13-free-diagonals-timing-complex32-sq4-free-1-n-26
- **Next:** none
- **Refs:** data/20261026-011055-a13-free-diagonals-timing-complex32-sq4-free-1-n-26

## 2026-10-26 01:10 UTC  A13 free diagonals timing complex32 sq4 free 0 n=26
- **Goal:** Mean dominant pass time over t_bw with stage_contraction and additive_addresses, free_diagonals=0, complex32, 4-qubit stages
- **Task:** A13
- **Method:** code/bench/gpurun -s noisecirc a16_time.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --set dtype=complex32 --set stage_qubits=4 --set stage_contraction=1 --set additive_addresses=1 --set free_diagonals=0 --variant base
- **Outcome:** exit 0; outputs in data/20261026-011004-a13-free-diagonals-timing-complex32-sq4-free-0-n-26
- **Next:** none
- **Refs:** data/20261026-011004-a13-free-diagonals-timing-complex32-sq4-free-0-n-26

## 2026-10-26 01:10 UTC  A13 free diagonals timing complex32 sq3 free 1 n=26
- **Goal:** Mean dominant pass time over t_bw with stage_contraction and additive_addresses, free_diagonals=1, complex32, 3-qubit stages
- **Task:** A13
- **Method:** code/bench/gpurun -s noisecirc a16_time.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --set dtype=complex32 --set stage_qubits=3 --set stage_contraction=1 --set additive_addresses=1 --set free_diagonals=1 --variant base
- **Outcome:** exit 0; outputs in data/20261026-010954-a13-free-diagonals-timing-complex32-sq3-free-1-n-26
- **Next:** none
- **Refs:** data/20261026-010954-a13-free-diagonals-timing-complex32-sq3-free-1-n-26

## 2026-10-26 01:09 UTC  A13 free diagonals timing complex32 sq3 free 0 n=26
- **Goal:** Mean dominant pass time over t_bw with stage_contraction and additive_addresses, free_diagonals=0, complex32, 3-qubit stages
- **Task:** A13
- **Method:** code/bench/gpurun -s noisecirc a16_time.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --set dtype=complex32 --set stage_qubits=3 --set stage_contraction=1 --set additive_addresses=1 --set free_diagonals=0 --variant base
- **Outcome:** exit 0; outputs in data/20261026-010941-a13-free-diagonals-timing-complex32-sq3-free-0-n-26
- **Next:** none
- **Refs:** data/20261026-010941-a13-free-diagonals-timing-complex32-sq3-free-0-n-26

## 2026-10-26 01:09 UTC  A13 error kernels input-relative free diagonals 1 sq4 n=10
- **Goal:** Masked and general kernels with 1-3 errors per block against svpass's NumPy device, deviation relative to the input norm, free_diagonals=1, 4-qubit stages
- **Task:** A13
- **Method:** code/bench/gpurun -s noisecirc a13_free_errors_check.py --workloads ghz:damping:0.05,brickwork:damping:0.05,qft:damping:0.05,qaoa:damping:0.05,grid:damping:0.05 --qubits 10 --draws 8 --set stage_contraction=1 --set additive_addresses=1 --set free_diagonals=1 --set stage_qubits=4
- **Outcome:** exit 0; outputs in data/20261026-010920-a13-error-kernels-input-relative-free-diagonals-1-sq4-n-10
- **Next:** none
- **Refs:** data/20261026-010920-a13-error-kernels-input-relative-free-diagonals-1-sq4-n-10

## 2026-10-26 01:09 UTC  A13 error kernels input-relative free diagonals 1 sq3 n=10
- **Goal:** Masked and general kernels with 1-3 errors per block against svpass's NumPy device, deviation relative to the input norm, free_diagonals=1, 3-qubit stages
- **Task:** A13
- **Method:** code/bench/gpurun -s noisecirc a13_free_errors_check.py --workloads ghz:damping:0.05,brickwork:damping:0.05,qft:damping:0.05,qaoa:damping:0.05,grid:damping:0.05 --qubits 10 --draws 8 --set stage_contraction=1 --set additive_addresses=1 --set free_diagonals=1 --set stage_qubits=3
- **Outcome:** exit 0; outputs in data/20261026-010915-a13-error-kernels-input-relative-free-diagonals-1-sq3-n-10
- **Next:** none
- **Refs:** data/20261026-010915-a13-error-kernels-input-relative-free-diagonals-1-sq3-n-10

## 2026-10-26 01:09 UTC  A13 error kernels input-relative free diagonals 0 sq4 n=10
- **Goal:** Masked and general kernels with 1-3 errors per block against svpass's NumPy device, deviation relative to the input norm, free_diagonals=0, 4-qubit stages
- **Task:** A13
- **Method:** code/bench/gpurun -s noisecirc a13_free_errors_check.py --workloads ghz:damping:0.05,brickwork:damping:0.05,qft:damping:0.05,qaoa:damping:0.05,grid:damping:0.05 --qubits 10 --draws 8 --set stage_contraction=1 --set additive_addresses=1 --set free_diagonals=0 --set stage_qubits=4
- **Outcome:** exit 0; outputs in data/20261026-010906-a13-error-kernels-input-relative-free-diagonals-0-sq4-n-10
- **Next:** none
- **Refs:** data/20261026-010906-a13-error-kernels-input-relative-free-diagonals-0-sq4-n-10

## 2026-10-26 01:09 UTC  A13 error kernels input-relative free diagonals 0 sq3 n=10
- **Goal:** Masked and general kernels with 1-3 errors per block against svpass's NumPy device, deviation relative to the input norm, free_diagonals=0, 3-qubit stages
- **Task:** A13
- **Method:** code/bench/gpurun -s noisecirc a13_free_errors_check.py --workloads ghz:damping:0.05,brickwork:damping:0.05,qft:damping:0.05,qaoa:damping:0.05,grid:damping:0.05 --qubits 10 --draws 8 --set stage_contraction=1 --set additive_addresses=1 --set free_diagonals=0 --set stage_qubits=3
- **Outcome:** exit 0; outputs in data/20261026-010900-a13-error-kernels-input-relative-free-diagonals-0-sq3-n-10
- **Next:** none
- **Refs:** data/20261026-010900-a13-error-kernels-input-relative-free-diagonals-0-sq3-n-10

## 2026-10-26 01:08 UTC  A13 error kernels few errors free diagonals 1 sq4 n=10
- **Goal:** Masked and general kernels with 1-3 errors per block against svpass's NumPy device, free_diagonals=1, 4-qubit stages
- **Task:** A13
- **Method:** code/bench/gpurun -s noisecirc a13_free_errors_check.py --workloads ghz:damping:0.05,brickwork:damping:0.05,qft:damping:0.05,qaoa:damping:0.05,grid:damping:0.05 --qubits 10 --draws 8 --set stage_contraction=1 --set additive_addresses=1 --set free_diagonals=1 --set stage_qubits=4
- **Outcome:** exit 0; outputs in data/20261026-010834-a13-error-kernels-few-errors-free-diagonals-1-sq4-n-10
- **Next:** none
- **Refs:** data/20261026-010834-a13-error-kernels-few-errors-free-diagonals-1-sq4-n-10

## 2026-10-26 01:08 UTC  A13 error kernels few errors free diagonals 1 sq3 n=10
- **Goal:** Masked and general kernels with 1-3 errors per block against svpass's NumPy device, free_diagonals=1, 3-qubit stages
- **Task:** A13
- **Method:** code/bench/gpurun -s noisecirc a13_free_errors_check.py --workloads ghz:damping:0.05,brickwork:damping:0.05,qft:damping:0.05,qaoa:damping:0.05,grid:damping:0.05 --qubits 10 --draws 8 --set stage_contraction=1 --set additive_addresses=1 --set free_diagonals=1 --set stage_qubits=3
- **Outcome:** exit 0; outputs in data/20261026-010829-a13-error-kernels-few-errors-free-diagonals-1-sq3-n-10
- **Next:** none
- **Refs:** data/20261026-010829-a13-error-kernels-few-errors-free-diagonals-1-sq3-n-10

## 2026-10-26 01:08 UTC  A13 error kernels few errors free diagonals 0 sq4 n=10
- **Goal:** Masked and general kernels with 1-3 errors per block against svpass's NumPy device, free_diagonals=0, 4-qubit stages
- **Task:** A13
- **Method:** code/bench/gpurun -s noisecirc a13_free_errors_check.py --workloads ghz:damping:0.05,brickwork:damping:0.05,qft:damping:0.05,qaoa:damping:0.05,grid:damping:0.05 --qubits 10 --draws 8 --set stage_contraction=1 --set additive_addresses=1 --set free_diagonals=0 --set stage_qubits=4
- **Outcome:** exit 0; outputs in data/20261026-010821-a13-error-kernels-few-errors-free-diagonals-0-sq4-n-10
- **Next:** none
- **Refs:** data/20261026-010821-a13-error-kernels-few-errors-free-diagonals-0-sq4-n-10

## 2026-10-26 01:08 UTC  A13 error kernels few errors free diagonals 0 sq3 n=10
- **Goal:** Masked and general kernels with 1-3 errors per block against svpass's NumPy device, free_diagonals=0, 3-qubit stages
- **Task:** A13
- **Method:** code/bench/gpurun -s noisecirc a13_free_errors_check.py --workloads ghz:damping:0.05,brickwork:damping:0.05,qft:damping:0.05,qaoa:damping:0.05,grid:damping:0.05 --qubits 10 --draws 8 --set stage_contraction=1 --set additive_addresses=1 --set free_diagonals=0 --set stage_qubits=3
- **Outcome:** exit 0; outputs in data/20261026-010815-a13-error-kernels-few-errors-free-diagonals-0-sq3-n-10
- **Next:** none
- **Refs:** data/20261026-010815-a13-error-kernels-few-errors-free-diagonals-0-sq3-n-10

## 2026-10-26 01:08 UTC  A13 error-kernel checks with uniform random choices invalid
- **Goal:** Check masked/general kernels against NumPy
- **Task:** A13
- **Method:** a13_free_errors_check.py with uniformly random choices per operation
- **Outcome:** Relative errors 1.0 also without free diagonals (control): chained damping jumps drive the expected state to (nearly) zero, so complex64 relative errors are meaningless; single-error debug (code/bench/a13_free_debug.py) matches to 2e-7. Runs 'A13 error kernels vs numpy ...' and '... vs svpass numpy device ...' invalid as tests
- **Next:** Rerun with dominant choices plus 1-3 errors
- **Refs:** code/bench/a13_free_errors_check.py

## 2026-10-26 01:07 UTC  A13 error kernels vs svpass numpy device free diagonals 1 sq4 n=10
- **Goal:** Masked and general kernels with random choices against svpass's NumPy device (complex128), free_diagonals=1, 4-qubit stages
- **Task:** A13
- **Method:** code/bench/gpurun -s noisecirc a13_free_errors_check.py --workloads ghz:damping:0.05,brickwork:damping:0.05,qft:damping:0.05,qaoa:damping:0.05,grid:damping:0.05 --qubits 10 --set stage_contraction=1 --set additive_addresses=1 --set free_diagonals=1 --set stage_qubits=4
- **Outcome:** exit 0; outputs in data/20261026-010709-a13-error-kernels-vs-svpass-numpy-device-free-diagonals-1-sq4-n-10
- **Next:** none
- **Refs:** data/20261026-010709-a13-error-kernels-vs-svpass-numpy-device-free-diagonals-1-sq4-n-10

## 2026-10-26 01:07 UTC  A13 error kernels vs svpass numpy device free diagonals 1 sq3 n=10
- **Goal:** Masked and general kernels with random choices against svpass's NumPy device (complex128), free_diagonals=1, 3-qubit stages
- **Task:** A13
- **Method:** code/bench/gpurun -s noisecirc a13_free_errors_check.py --workloads ghz:damping:0.05,brickwork:damping:0.05,qft:damping:0.05,qaoa:damping:0.05,grid:damping:0.05 --qubits 10 --set stage_contraction=1 --set additive_addresses=1 --set free_diagonals=1 --set stage_qubits=3
- **Outcome:** exit 0; outputs in data/20261026-010703-a13-error-kernels-vs-svpass-numpy-device-free-diagonals-1-sq3-n-10
- **Next:** none
- **Refs:** data/20261026-010703-a13-error-kernels-vs-svpass-numpy-device-free-diagonals-1-sq3-n-10

## 2026-10-26 01:07 UTC  A13 error kernels vs svpass numpy device free diagonals 0 sq4 n=10
- **Goal:** Masked and general kernels with random choices against svpass's NumPy device (complex128), free_diagonals=0, 4-qubit stages
- **Task:** A13
- **Method:** code/bench/gpurun -s noisecirc a13_free_errors_check.py --workloads ghz:damping:0.05,brickwork:damping:0.05,qft:damping:0.05,qaoa:damping:0.05,grid:damping:0.05 --qubits 10 --set stage_contraction=1 --set additive_addresses=1 --set free_diagonals=0 --set stage_qubits=4
- **Outcome:** exit 0; outputs in data/20261026-010655-a13-error-kernels-vs-svpass-numpy-device-free-diagonals-0-sq4-n-10
- **Next:** none
- **Refs:** data/20261026-010655-a13-error-kernels-vs-svpass-numpy-device-free-diagonals-0-sq4-n-10

## 2026-10-26 01:06 UTC  A13 error kernels vs svpass numpy device free diagonals 0 sq3 n=10
- **Goal:** Masked and general kernels with random choices against svpass's NumPy device (complex128), free_diagonals=0, 3-qubit stages
- **Task:** A13
- **Method:** code/bench/gpurun -s noisecirc a13_free_errors_check.py --workloads ghz:damping:0.05,brickwork:damping:0.05,qft:damping:0.05,qaoa:damping:0.05,grid:damping:0.05 --qubits 10 --set stage_contraction=1 --set additive_addresses=1 --set free_diagonals=0 --set stage_qubits=3
- **Outcome:** exit 0; outputs in data/20261026-010649-a13-error-kernels-vs-svpass-numpy-device-free-diagonals-0-sq3-n-10
- **Next:** none
- **Refs:** data/20261026-010649-a13-error-kernels-vs-svpass-numpy-device-free-diagonals-0-sq3-n-10

## 2026-10-26 01:06 UTC  A13 error kernels vs numpy free diagonals 1 sq4 n=10 rerun
- **Goal:** Masked and general kernels with random non-dominant choices against NumPy, free_diagonals=1, 4-qubit stages
- **Task:** A13
- **Method:** code/bench/gpurun -s noisecirc a13_free_errors_check.py --workloads ghz:damping:0.05,brickwork:damping:0.05,qft:damping:0.05,qaoa:damping:0.05,grid:damping:0.05 --qubits 10 --set stage_contraction=1 --set additive_addresses=1 --set free_diagonals=1 --set stage_qubits=4
- **Outcome:** exit 0; outputs in data/20261026-010542-a13-error-kernels-vs-numpy-free-diagonals-1-sq4-n-10-rerun
- **Next:** none
- **Refs:** data/20261026-010542-a13-error-kernels-vs-numpy-free-diagonals-1-sq4-n-10-rerun

## 2026-10-26 01:05 UTC  A13 error kernels vs numpy free diagonals 1 sq3 n=10 rerun
- **Goal:** Masked and general kernels with random non-dominant choices against NumPy, free_diagonals=1, 3-qubit stages
- **Task:** A13
- **Method:** code/bench/gpurun -s noisecirc a13_free_errors_check.py --workloads ghz:damping:0.05,brickwork:damping:0.05,qft:damping:0.05,qaoa:damping:0.05,grid:damping:0.05 --qubits 10 --set stage_contraction=1 --set additive_addresses=1 --set free_diagonals=1 --set stage_qubits=3
- **Outcome:** exit 0; outputs in data/20261026-010525-a13-error-kernels-vs-numpy-free-diagonals-1-sq3-n-10-rerun
- **Next:** none
- **Refs:** data/20261026-010525-a13-error-kernels-vs-numpy-free-diagonals-1-sq3-n-10-rerun

## 2026-10-26 01:05 UTC  A13 error kernels vs numpy free diagonals 0 sq4 n=10 rerun
- **Goal:** Masked and general kernels with random non-dominant choices against NumPy, free_diagonals=0, 4-qubit stages
- **Task:** A13
- **Method:** code/bench/gpurun -s noisecirc a13_free_errors_check.py --workloads ghz:damping:0.05,brickwork:damping:0.05,qft:damping:0.05,qaoa:damping:0.05,grid:damping:0.05 --qubits 10 --set stage_contraction=1 --set additive_addresses=1 --set free_diagonals=0 --set stage_qubits=4
- **Outcome:** exit 0; outputs in data/20261026-010456-a13-error-kernels-vs-numpy-free-diagonals-0-sq4-n-10-rerun
- **Next:** none
- **Refs:** data/20261026-010456-a13-error-kernels-vs-numpy-free-diagonals-0-sq4-n-10-rerun

## 2026-10-26 01:04 UTC  A13 error kernels vs numpy free diagonals 0 sq3 n=10 rerun
- **Goal:** Masked and general kernels with random non-dominant choices against NumPy, free_diagonals=0, 3-qubit stages
- **Task:** A13
- **Method:** code/bench/gpurun -s noisecirc a13_free_errors_check.py --workloads ghz:damping:0.05,brickwork:damping:0.05,qft:damping:0.05,qaoa:damping:0.05,grid:damping:0.05 --qubits 10 --set stage_contraction=1 --set additive_addresses=1 --set free_diagonals=0 --set stage_qubits=3
- **Outcome:** exit 0; outputs in data/20261026-010438-a13-error-kernels-vs-numpy-free-diagonals-0-sq3-n-10-rerun
- **Next:** none
- **Refs:** data/20261026-010438-a13-error-kernels-vs-numpy-free-diagonals-0-sq3-n-10-rerun

## 2026-10-26 01:04 UTC  A13 error-kernel check runs failed (configpatch)
- **Goal:** Check masked/general kernels with free diagonals against NumPy
- **Task:** A13
- **Method:** a13_free_errors_check.py, four runs
- **Outcome:** All four runs failed at start: free_diagonals not in configpatch's Config fields (TypeError in Simulator); fixed
- **Next:** Rerun
- **Refs:** code/bench/configpatch.py

## 2026-10-26 01:04 UTC  A13 error kernels vs numpy free diagonals 1 sq4 n=10
- **Goal:** Masked and general kernels with random non-dominant choices against NumPy, free_diagonals=1, 4-qubit stages
- **Task:** A13
- **Method:** code/bench/gpurun -s noisecirc a13_free_errors_check.py --workloads ghz:damping:0.05,brickwork:damping:0.05,qft:damping:0.05,qaoa:damping:0.05,grid:damping:0.05 --qubits 10 --set stage_contraction=1 --set additive_addresses=1 --set free_diagonals=1 --set stage_qubits=4
- **Outcome:** exit 1; outputs in data/20261026-010418-a13-error-kernels-vs-numpy-free-diagonals-1-sq4-n-10
- **Next:** none
- **Refs:** data/20261026-010418-a13-error-kernels-vs-numpy-free-diagonals-1-sq4-n-10

## 2026-10-26 01:04 UTC  A13 error kernels vs numpy free diagonals 1 sq3 n=10
- **Goal:** Masked and general kernels with random non-dominant choices against NumPy, free_diagonals=1, 3-qubit stages
- **Task:** A13
- **Method:** code/bench/gpurun -s noisecirc a13_free_errors_check.py --workloads ghz:damping:0.05,brickwork:damping:0.05,qft:damping:0.05,qaoa:damping:0.05,grid:damping:0.05 --qubits 10 --set stage_contraction=1 --set additive_addresses=1 --set free_diagonals=1 --set stage_qubits=3
- **Outcome:** exit 1; outputs in data/20261026-010416-a13-error-kernels-vs-numpy-free-diagonals-1-sq3-n-10
- **Next:** none
- **Refs:** data/20261026-010416-a13-error-kernels-vs-numpy-free-diagonals-1-sq3-n-10

## 2026-10-26 01:04 UTC  A13 error kernels vs numpy free diagonals 0 sq4 n=10
- **Goal:** Masked and general kernels with random non-dominant choices against NumPy, free_diagonals=0, 4-qubit stages
- **Task:** A13
- **Method:** code/bench/gpurun -s noisecirc a13_free_errors_check.py --workloads ghz:damping:0.05,brickwork:damping:0.05,qft:damping:0.05,qaoa:damping:0.05,grid:damping:0.05 --qubits 10 --set stage_contraction=1 --set additive_addresses=1 --set free_diagonals=0 --set stage_qubits=4
- **Outcome:** exit 1; outputs in data/20261026-010414-a13-error-kernels-vs-numpy-free-diagonals-0-sq4-n-10
- **Next:** none
- **Refs:** data/20261026-010414-a13-error-kernels-vs-numpy-free-diagonals-0-sq4-n-10

## 2026-10-26 01:04 UTC  A13 error kernels vs numpy free diagonals 0 sq3 n=10
- **Goal:** Masked and general kernels with random non-dominant choices against NumPy, free_diagonals=0, 3-qubit stages
- **Task:** A13
- **Method:** code/bench/gpurun -s noisecirc a13_free_errors_check.py --workloads ghz:damping:0.05,brickwork:damping:0.05,qft:damping:0.05,qaoa:damping:0.05,grid:damping:0.05 --qubits 10 --set stage_contraction=1 --set additive_addresses=1 --set free_diagonals=0 --set stage_qubits=3
- **Outcome:** exit 1; outputs in data/20261026-010412-a13-error-kernels-vs-numpy-free-diagonals-0-sq3-n-10
- **Next:** none
- **Refs:** data/20261026-010412-a13-error-kernels-vs-numpy-free-diagonals-0-sq3-n-10

## 2026-10-26 01:03 UTC  A13 noisecirc statistical tests with free diagonals on
- **Goal:** noisecirc statistical tests (sampling vs ground truth) on GPU 0 with free_diagonals defaulted on (temporary)
- **Task:** A13
- **Method:** code/bench/gpurun -s noisecirc run_stat_tests.py
- **Outcome:** exit 0; outputs in data/20261026-010247-a13-noisecirc-statistical-tests-with-free-diagonals-on
- **Next:** none
- **Refs:** data/20261026-010247-a13-noisecirc-statistical-tests-with-free-diagonals-on

## 2026-10-26 01:02 UTC  A13 noisecirc GPU tests with free diagonals on full after order fix
- **Goal:** All svpass and noisecirc tests on GPU 0 with free_diagonals defaulted on (temporary), after keeping the order of free operations
- **Task:** A13
- **Method:** code/bench/gpurun -s noisecirc run_tests_full.py
- **Outcome:** exit 0; outputs in data/20261026-010218-a13-noisecirc-gpu-tests-with-free-diagonals-on-full-after-order-fix
- **Next:** none
- **Refs:** data/20261026-010218-a13-noisecirc-gpu-tests-with-free-diagonals-on-full-after-order-fix

## 2026-10-26 00:56 UTC  A13 noisecirc GPU tests with free diagonals on full
- **Goal:** All svpass and noisecirc tests on GPU 0 with free_diagonals defaulted on (temporary), listing failures
- **Task:** A13
- **Method:** code/bench/gpurun -s noisecirc run_tests_full.py
- **Outcome:** exit 0; outputs in data/20261026-005530-a13-noisecirc-gpu-tests-with-free-diagonals-on-full
- **Next:** none
- **Refs:** data/20261026-005530-a13-noisecirc-gpu-tests-with-free-diagonals-on-full

## 2026-10-26 00:55 UTC  A13 noisecirc GPU tests with free diagonals on
- **Goal:** svpass and noisecirc test suites on GPU 0 with free_diagonals defaulted on (temporary, uncommitted), to check masked and general kernels with sub-stages
- **Task:** A13
- **Method:** code/bench/gpurun -s noisecirc run_tests.py
- **Outcome:** exit 0; outputs in data/20261026-005517-a13-noisecirc-gpu-tests-with-free-diagonals-on
- **Next:** none
- **Refs:** data/20261026-005517-a13-noisecirc-gpu-tests-with-free-diagonals-on

## 2026-10-26 00:55 UTC  A13 free diagonals whole-circuit check sq4 n=24
- **Goal:** No-error trajectory with free_diagonals (complex64) against an independent complex128 compilation without it; stages per block
- **Task:** A13
- **Method:** code/bench/gpurun -s noisecirc a13_free_check.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 24 --set stage_contraction=1 --set additive_addresses=1 --set stage_qubits=4
- **Outcome:** exit 0; outputs in data/20261026-005402-a13-free-diagonals-whole-circuit-check-sq4-n-24
- **Next:** none
- **Refs:** data/20261026-005402-a13-free-diagonals-whole-circuit-check-sq4-n-24

## 2026-10-26 00:54 UTC  A13 free diagonals whole-circuit check sq3 n=24
- **Goal:** No-error trajectory with free_diagonals (complex64) against an independent complex128 compilation without it; stages per block
- **Task:** A13
- **Method:** code/bench/gpurun -s noisecirc a13_free_check.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 24 --set stage_contraction=1 --set additive_addresses=1 --set stage_qubits=3
- **Outcome:** exit 0; outputs in data/20261026-005332-a13-free-diagonals-whole-circuit-check-sq3-n-24
- **Next:** none
- **Refs:** data/20261026-005332-a13-free-diagonals-whole-circuit-check-sq3-n-24

## 2026-10-26 00:53 UTC  A13 A14 end-to-end contract-add-sq4 grid n=28
- **Goal:** End-to-end time of stage_contraction + additive_addresses with 4-qubit stages (contract-add-sq4), damping M=0.1 and 1, 1000 shots, 3 seeds
- **Task:** A13
- **Method:** code/bench/gpurun -t 590 -s noisecirc a2_runs.py --circuits grid --qubits 28 --noise damping --ps 0.000141443,0.00141443 --shots 1000 --reps 3 --budget 450 --config stage_contraction=1 --config additive_addresses=1 --config stage_qubits=4
- **Outcome:** exit 0; outputs in data/20261026-004914-a13-a14-end-to-end-contract-add-sq4-grid-n-28
- **Next:** none
- **Refs:** data/20261026-004914-a13-a14-end-to-end-contract-add-sq4-grid-n-28

## 2026-10-26 00:49 UTC  A13 A14 end-to-end contract-add-sq4 qaoa n=28
- **Goal:** End-to-end time of stage_contraction + additive_addresses with 4-qubit stages (contract-add-sq4), damping M=0.1 and 1, 1000 shots, 3 seeds
- **Task:** A13
- **Method:** code/bench/gpurun -t 590 -s noisecirc a2_runs.py --circuits qaoa --qubits 28 --noise damping --ps 0.00047619,0.0047619 --shots 1000 --reps 3 --budget 450 --config stage_contraction=1 --config additive_addresses=1 --config stage_qubits=4
- **Outcome:** exit 0; outputs in data/20261026-004721-a13-a14-end-to-end-contract-add-sq4-qaoa-n-28
- **Next:** none
- **Refs:** data/20261026-004721-a13-a14-end-to-end-contract-add-sq4-qaoa-n-28

## 2026-10-26 00:47 UTC  A13 A14 end-to-end contract-add-sq4 qft n=28
- **Goal:** End-to-end time of stage_contraction + additive_addresses with 4-qubit stages (contract-add-sq4), damping M=0.1 and 1, 1000 shots, 3 seeds
- **Task:** A13
- **Method:** code/bench/gpurun -t 590 -s noisecirc a2_runs.py --circuits qft --qubits 28 --noise damping --ps 0.000246305,0.00246305 --shots 1000 --reps 3 --budget 450 --config stage_contraction=1 --config additive_addresses=1 --config stage_qubits=4
- **Outcome:** exit 0; outputs in data/20261026-004513-a13-a14-end-to-end-contract-add-sq4-qft-n-28
- **Next:** none
- **Refs:** data/20261026-004513-a13-a14-end-to-end-contract-add-sq4-qft-n-28

## 2026-10-26 00:45 UTC  A13 A14 end-to-end contract-add-sq4 brickwork n=28
- **Goal:** End-to-end time of stage_contraction + additive_addresses with 4-qubit stages (contract-add-sq4), damping M=0.1 and 1, 1000 shots, 3 seeds
- **Task:** A13
- **Method:** code/bench/gpurun -t 590 -s noisecirc a2_runs.py --circuits brickwork --qubits 28 --noise damping --ps 0.000242131,0.00242131 --shots 1000 --reps 3 --budget 450 --config stage_contraction=1 --config additive_addresses=1 --config stage_qubits=4
- **Outcome:** exit 0; outputs in data/20261026-004148-a13-a14-end-to-end-contract-add-sq4-brickwork-n-28
- **Next:** none
- **Refs:** data/20261026-004148-a13-a14-end-to-end-contract-add-sq4-brickwork-n-28

## 2026-10-26 00:41 UTC  A13 A14 end-to-end contract-add-sq4 ghz n=28
- **Goal:** End-to-end time of stage_contraction + additive_addresses with 4-qubit stages (contract-add-sq4), damping M=0.1 and 1, 1000 shots, 3 seeds
- **Task:** A13
- **Method:** code/bench/gpurun -t 590 -s noisecirc a2_runs.py --circuits ghz --qubits 28 --noise damping --ps 0.00183486,0.0183486 --shots 1000 --reps 3 --budget 450 --config stage_contraction=1 --config additive_addresses=1 --config stage_qubits=4
- **Outcome:** exit 0; outputs in data/20261026-004108-a13-a14-end-to-end-contract-add-sq4-ghz-n-28
- **Next:** none
- **Refs:** data/20261026-004108-a13-a14-end-to-end-contract-add-sq4-ghz-n-28

## 2026-10-26 00:41 UTC  A13 A14 end-to-end contract-add-sq4-c32 grid n=28
- **Goal:** End-to-end time of stage_contraction + additive_addresses with 4-qubit stages (contract-add-sq4-c32), damping M=0.1 and 1, 1000 shots, 3 seeds
- **Task:** A13
- **Method:** code/bench/gpurun -t 590 -s noisecirc a2_runs.py --circuits grid --qubits 28 --noise damping --ps 0.000141443,0.00141443 --shots 1000 --reps 3 --budget 450 --config stage_contraction=1 --config additive_addresses=1 --config stage_qubits=4 --config dtype=complex32
- **Outcome:** exit 0; outputs in data/20261026-003749-a13-a14-end-to-end-contract-add-sq4-c32-grid-n-28
- **Next:** none
- **Refs:** data/20261026-003749-a13-a14-end-to-end-contract-add-sq4-c32-grid-n-28

## 2026-10-26 00:37 UTC  A13 A14 end-to-end contract-add-sq4-c32 qaoa n=28
- **Goal:** End-to-end time of stage_contraction + additive_addresses with 4-qubit stages (contract-add-sq4-c32), damping M=0.1 and 1, 1000 shots, 3 seeds
- **Task:** A13
- **Method:** code/bench/gpurun -t 590 -s noisecirc a2_runs.py --circuits qaoa --qubits 28 --noise damping --ps 0.00047619,0.0047619 --shots 1000 --reps 3 --budget 450 --config stage_contraction=1 --config additive_addresses=1 --config stage_qubits=4 --config dtype=complex32
- **Outcome:** exit 0; outputs in data/20261026-003618-a13-a14-end-to-end-contract-add-sq4-c32-qaoa-n-28
- **Next:** none
- **Refs:** data/20261026-003618-a13-a14-end-to-end-contract-add-sq4-c32-qaoa-n-28

## 2026-10-26 00:36 UTC  A13 A14 end-to-end contract-add-sq4-c32 qft n=28
- **Goal:** End-to-end time of stage_contraction + additive_addresses with 4-qubit stages (contract-add-sq4-c32), damping M=0.1 and 1, 1000 shots, 3 seeds
- **Task:** A13
- **Method:** code/bench/gpurun -t 590 -s noisecirc a2_runs.py --circuits qft --qubits 28 --noise damping --ps 0.000246305,0.00246305 --shots 1000 --reps 3 --budget 450 --config stage_contraction=1 --config additive_addresses=1 --config stage_qubits=4 --config dtype=complex32
- **Outcome:** exit 0; outputs in data/20261026-003501-a13-a14-end-to-end-contract-add-sq4-c32-qft-n-28
- **Next:** none
- **Refs:** data/20261026-003501-a13-a14-end-to-end-contract-add-sq4-c32-qft-n-28

## 2026-10-26 00:35 UTC  A13 A14 end-to-end contract-add-sq4-c32 brickwork n=28
- **Goal:** End-to-end time of stage_contraction + additive_addresses with 4-qubit stages (contract-add-sq4-c32), damping M=0.1 and 1, 1000 shots, 3 seeds
- **Task:** A13
- **Method:** code/bench/gpurun -t 590 -s noisecirc a2_runs.py --circuits brickwork --qubits 28 --noise damping --ps 0.000242131,0.00242131 --shots 1000 --reps 3 --budget 450 --config stage_contraction=1 --config additive_addresses=1 --config stage_qubits=4 --config dtype=complex32
- **Outcome:** exit 0; outputs in data/20261026-003222-a13-a14-end-to-end-contract-add-sq4-c32-brickwork-n-28
- **Next:** none
- **Refs:** data/20261026-003222-a13-a14-end-to-end-contract-add-sq4-c32-brickwork-n-28

## 2026-10-26 00:32 UTC  A13 A14 end-to-end contract-add-sq4-c32 ghz n=28
- **Goal:** End-to-end time of stage_contraction + additive_addresses with 4-qubit stages (contract-add-sq4-c32), damping M=0.1 and 1, 1000 shots, 3 seeds
- **Task:** A13
- **Method:** code/bench/gpurun -t 590 -s noisecirc a2_runs.py --circuits ghz --qubits 28 --noise damping --ps 0.00183486,0.0183486 --shots 1000 --reps 3 --budget 450 --config stage_contraction=1 --config additive_addresses=1 --config stage_qubits=4 --config dtype=complex32
- **Outcome:** exit 0; outputs in data/20261026-003149-a13-a14-end-to-end-contract-add-sq4-c32-ghz-n-28
- **Next:** none
- **Refs:** data/20261026-003149-a13-a14-end-to-end-contract-add-sq4-c32-ghz-n-28

## 2026-10-26 00:31 UTC  A13 timing additive addresses and stage contraction complex64 sq4 n=26
- **Goal:** Measure predicted gains (GPU 0 was down): A14 kernels vs +additive_addresses, stage_contraction, both, and with 96 registers; complex64, 4-qubit stages, five workloads
- **Task:** A13
- **Method:** code/bench/gpurun -s noisecirc a16_time.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --set dtype=complex64 --set stage_qubits=4 --set stage_fusion=1 --set rotation_form=1 --variant base --variant additive_addresses=1 --variant stage_contraction=1 --variant stage_contraction=1,additive_addresses=1 --variant stage_contraction=1,additive_addresses=1,min_registers=96 --variant min_registers=96
- **Outcome:** exit 0; outputs in data/20261026-002817-a13-timing-additive-addresses-and-stage-contraction-complex64-sq4-n-26
- **Next:** none
- **Refs:** data/20261026-002817-a13-timing-additive-addresses-and-stage-contraction-complex64-sq4-n-26

## 2026-10-26 00:28 UTC  A13 timing additive addresses and stage contraction complex32 sq4 n=26
- **Goal:** Measure predicted gains (GPU 0 was down): A14 kernels vs +additive_addresses, stage_contraction, both, and with 96 registers; complex32, 4-qubit stages, five workloads
- **Task:** A13
- **Method:** code/bench/gpurun -s noisecirc a16_time.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --set dtype=complex32 --set stage_qubits=4 --set stage_fusion=1 --set rotation_form=1 --variant base --variant additive_addresses=1 --variant stage_contraction=1 --variant stage_contraction=1,additive_addresses=1 --variant stage_contraction=1,additive_addresses=1,min_registers=96 --variant min_registers=96
- **Outcome:** exit 0; outputs in data/20261026-002525-a13-timing-additive-addresses-and-stage-contraction-complex32-sq4-n-26
- **Next:** none
- **Refs:** data/20261026-002525-a13-timing-additive-addresses-and-stage-contraction-complex32-sq4-n-26

## 2026-10-26 00:24 UTC  A16 tensor cores for block passes: implementation, timing, verdict
- **Goal:** Answer whether tensor cores speed up noisecirc's block passes
- **Task:** A16
- **Method:** svpass Config.tensor_cores (noisecirc feature/tensor-cores: mma.sync m16n8k8 TF32 / m16n8k16 FP16 on the real form of each stage's product; modes tf32x3/x2/x1, f16x3/x2/x1; tensor_unroll, tensor_threshold); a16_check/time/ablate/accuracy/mma_rate.py; four implementation rounds (latency, fallback i-cache, address tables, stage-ahead table loads)
- **Outcome:** Split modes as accurate as complex64 (whole-circuit TVD <=5.6e-7) but 15% to 2.6x slower than contraction CUDA-core kernels; f16 single product brickwork -8% (c64 sq4) / -4% (c32 sq4), others equal or slower, accuracy ~1e-3 (QFT norm 1.5e-2 with all stages). mma.sync peaks f16 483, tf32 242, FFMA 41.7 TFLOP/s. Side: CUDA sq4 kernels 2-6% faster with min_registers 96. Verdict: no at single precision
- **Next:** Pending A13 GPU timings, then A17
- **Refs:** wiki/studies/tensor-cores.md, data/a16-analysis, code/bench/a16_time.py, memory/tasks/A16.md

## 2026-10-26 00:21 UTC  A16 whole-circuit accuracy of tensor-core variants n=24
- **Goal:** TVD, squared-norm error and infidelity of the no-error trajectory for tensor-core variants vs complex128, against complex64 and complex32 CUDA-core kernels
- **Task:** A16
- **Method:** code/bench/gpurun -s noisecirc a16_accuracy.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 24 --set stage_contraction=1 --set stage_qubits=4 --variant base --variant dtype=complex32 --variant tensor_cores=tf32x3,tensor_unroll=1,min_registers=96 --variant tensor_cores=f16x3,tensor_unroll=1,min_registers=96 --variant tensor_cores=f16,tensor_unroll=2,min_registers=96,tensor_threshold=12 --variant tensor_cores=f16,tensor_unroll=2,min_registers=96
- **Outcome:** exit 0; outputs in data/20261026-001744-a16-whole-circuit-accuracy-of-tensor-core-variants-n-24
- **Next:** none
- **Refs:** data/20261026-001744-a16-whole-circuit-accuracy-of-tensor-core-variants-n-24

## 2026-10-26 00:17 UTC  A16 hybrid tensor-core threshold complex32 sq4 f16
- **Goal:** Trajectory time of stages on tensor cores only above a CUDA-core cost threshold (0, 12, 18, 24 FP/amp), complex32, 4-qubit stages, f16
- **Task:** A16
- **Method:** code/bench/gpurun -s noisecirc a16_time.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --set stage_contraction=1 --set dtype=complex32 --set stage_qubits=4 --variant base --variant min_registers=96 --variant tensor_cores=f16,tensor_unroll=2,min_registers=96,tensor_threshold=0 --variant tensor_cores=f16,tensor_unroll=2,min_registers=96,tensor_threshold=12 --variant tensor_cores=f16,tensor_unroll=2,min_registers=96,tensor_threshold=18 --variant tensor_cores=f16,tensor_unroll=2,min_registers=96,tensor_threshold=24
- **Outcome:** exit 0; outputs in data/20261026-001316-a16-hybrid-tensor-core-threshold-complex32-sq4-f16
- **Next:** none
- **Refs:** data/20261026-001316-a16-hybrid-tensor-core-threshold-complex32-sq4-f16

## 2026-10-26 00:13 UTC  A16 invalid ablations (kernel cache)
- **Goal:** Record that the first ablation runs measured unablated kernels
- **Task:** A16
- **Method:** a16_ablate.py monkeypatched codegen.kernel_source, but svpass.engine._compiled caches kernels by block and Config
- **Outcome:** Runs 'A16 ablation of tensor-core passes f16/tf32x3 n=26', '... with no-fallback f16', '... unroll 4 f16', 'A16 ablation swizzle ...' and the first 'fixed cache' run (regex assertion) are invalid; valid from 'A16 ablation of tensor-core passes fixed cache f16 unroll 4 n=26 rerun' on
- **Next:** none
- **Refs:** code/bench/a16_ablate.py, memory/tasks/A16.md

## 2026-10-26 00:13 UTC  A16 literature on tensor cores for state vectors
- **Goal:** Prior art for applying gates with tensor cores and recovering single precision
- **Task:** A16
- **Method:** Web search; research-lit add of four arXiv/journal papers
- **Outcome:** Added ootomo2022recovering (3-term TF32/FP16 split, RZ accumulation fix), ootomo2023quantum (TC SGEMM emulation for TN contraction), li2024tanq (FP64 TC density matrices), zhang2025can (TC bound 1.33x for memory-bound FP64 kernels). HyQuas (TransMM, ICS'21, DOI 10.1145/3447818.3460357): PDF blocked by ACM, not added or cited
- **Next:** Notes after the study page exists
- **Refs:** wiki/literature/notes

## 2026-10-26 00:13 UTC  GPU 0 back after bux reboot; container without stale CDI
- **Goal:** Restore GPU 0 runs after the 2026-10-25 outage
- **Task:** A16
- **Method:** Rebuilt bench image (local podman store wiped by reboot); ~/remote/bench/run now passes /dev/nvidia0 and the CUDA driver libraries explicitly because /etc/cdi/nvidia.yaml is stale after the driver update and podman 4.6 ignores cdi_spec_dirs; code/bench/gpucheck.py
- **Outcome:** cuInit 0 on GPU 0 (H100 PCIe), only GPU 0 visible in the container; venv re-synced
- **Next:** A16 measurements; then the pending A13 timings
- **Refs:** memory/topics/gpu-environment.md, code/bench/gpucheck.py

## 2026-10-26 00:13 UTC  A16 hybrid tensor-core threshold complex32 sq3 f16
- **Goal:** Trajectory time of stages on tensor cores only above a CUDA-core cost threshold (0, 12, 18, 24 FP/amp), complex32, 3-qubit stages, f16
- **Task:** A16
- **Method:** code/bench/gpurun -s noisecirc a16_time.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --set stage_contraction=1 --set dtype=complex32 --set stage_qubits=3 --variant base --variant min_registers=96 --variant tensor_cores=f16,tensor_unroll=2,min_registers=96,tensor_threshold=0 --variant tensor_cores=f16,tensor_unroll=2,min_registers=96,tensor_threshold=12 --variant tensor_cores=f16,tensor_unroll=2,min_registers=96,tensor_threshold=18 --variant tensor_cores=f16,tensor_unroll=2,min_registers=96,tensor_threshold=24
- **Outcome:** exit 0; outputs in data/20261026-001207-a16-hybrid-tensor-core-threshold-complex32-sq3-f16
- **Next:** none
- **Refs:** data/20261026-001207-a16-hybrid-tensor-core-threshold-complex32-sq3-f16

## 2026-10-26 00:12 UTC  A16 hybrid tensor-core threshold complex64 sq4 f16
- **Goal:** Trajectory time of stages on tensor cores only above a CUDA-core cost threshold (0, 12, 18, 24 FP/amp), complex64, 4-qubit stages, f16
- **Task:** A16
- **Method:** code/bench/gpurun -s noisecirc a16_time.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --set stage_contraction=1 --set dtype=complex64 --set stage_qubits=4 --variant base --variant min_registers=96 --variant tensor_cores=f16,tensor_unroll=2,min_registers=96,tensor_threshold=0 --variant tensor_cores=f16,tensor_unroll=2,min_registers=96,tensor_threshold=12 --variant tensor_cores=f16,tensor_unroll=2,min_registers=96,tensor_threshold=18 --variant tensor_cores=f16,tensor_unroll=2,min_registers=96,tensor_threshold=24
- **Outcome:** exit 0; outputs in data/20261026-000753-a16-hybrid-tensor-core-threshold-complex64-sq4-f16
- **Next:** none
- **Refs:** data/20261026-000753-a16-hybrid-tensor-core-threshold-complex64-sq4-f16

## 2026-10-26 00:07 UTC  A16 hybrid tensor-core threshold complex64 sq4 f16x3
- **Goal:** Trajectory time of stages on tensor cores only above a CUDA-core cost threshold (0, 12, 18, 24 FP/amp), complex64, 4-qubit stages, f16x3
- **Task:** A16
- **Method:** code/bench/gpurun -s noisecirc a16_time.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --set stage_contraction=1 --set dtype=complex64 --set stage_qubits=4 --variant base --variant min_registers=96 --variant tensor_cores=f16x3,tensor_unroll=1,min_registers=96,tensor_threshold=0 --variant tensor_cores=f16x3,tensor_unroll=1,min_registers=96,tensor_threshold=12 --variant tensor_cores=f16x3,tensor_unroll=1,min_registers=96,tensor_threshold=18 --variant tensor_cores=f16x3,tensor_unroll=1,min_registers=96,tensor_threshold=24
- **Outcome:** exit 0; outputs in data/20261026-000316-a16-hybrid-tensor-core-threshold-complex64-sq4-f16x3
- **Next:** none
- **Refs:** data/20261026-000316-a16-hybrid-tensor-core-threshold-complex64-sq4-f16x3

## 2026-10-26 00:01 UTC  A16 tensor-core stages complex32 sq4 n=26
- **Goal:** Trajectory time of tensor-core stages (f16, f16x2, f16x3) against contraction CUDA-core kernels, complex32, 4-qubit stages, five workloads
- **Task:** A16
- **Method:** code/bench/gpurun -s noisecirc a16_time.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --set stage_contraction=1 --set dtype=complex32 --set stage_qubits=4 --variant base --variant tensor_cores=f16,tensor_unroll=2 --variant tensor_cores=f16,tensor_unroll=2,min_registers=96 --variant tensor_cores=f16x2,tensor_unroll=2 --variant tensor_cores=f16x3,tensor_unroll=1 --variant tensor_cores=f16x3,tensor_unroll=1,min_registers=96
- **Outcome:** exit 0; outputs in data/20261025-235943-a16-tensor-core-stages-complex32-sq4-n-26
- **Next:** none
- **Refs:** data/20261025-235943-a16-tensor-core-stages-complex32-sq4-n-26

## 2026-10-25 23:59 UTC  A16 tensor-core stages complex32 sq3 n=26
- **Goal:** Trajectory time of tensor-core stages (f16, f16x2, f16x3) against contraction CUDA-core kernels, complex32, 3-qubit stages, five workloads
- **Task:** A16
- **Method:** code/bench/gpurun -s noisecirc a16_time.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --set stage_contraction=1 --set dtype=complex32 --set stage_qubits=3 --variant base --variant tensor_cores=f16,tensor_unroll=2 --variant tensor_cores=f16,tensor_unroll=2,min_registers=96 --variant tensor_cores=f16x2,tensor_unroll=2 --variant tensor_cores=f16x3,tensor_unroll=1 --variant tensor_cores=f16x3,tensor_unroll=1,min_registers=96
- **Outcome:** exit 0; outputs in data/20261025-235820-a16-tensor-core-stages-complex32-sq3-n-26
- **Next:** none
- **Refs:** data/20261025-235820-a16-tensor-core-stages-complex32-sq3-n-26

## 2026-10-25 23:58 UTC  A16 tensor-core stages complex64 sq4 n=26
- **Goal:** Trajectory time of tensor-core stages (f16, f16x2, f16x3) against contraction CUDA-core kernels, complex64, 4-qubit stages, five workloads
- **Task:** A16
- **Method:** code/bench/gpurun -s noisecirc a16_time.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --set stage_contraction=1 --set dtype=complex64 --set stage_qubits=4 --variant base --variant tensor_cores=f16,tensor_unroll=2 --variant tensor_cores=f16,tensor_unroll=2,min_registers=96 --variant tensor_cores=f16x2,tensor_unroll=2 --variant tensor_cores=f16x3,tensor_unroll=1 --variant tensor_cores=f16x3,tensor_unroll=1,min_registers=96
- **Outcome:** exit 0; outputs in data/20261025-235633-a16-tensor-core-stages-complex64-sq4-n-26
- **Next:** none
- **Refs:** data/20261025-235633-a16-tensor-core-stages-complex64-sq4-n-26

## 2026-10-25 23:56 UTC  A16 tensor-core stages with preloaded tables sq3 n=26
- **Goal:** Trajectory time of tensor-core stages with tables loaded a stage ahead (f16, f16x3, tf32x3) against contraction CUDA-core kernels, five workloads, 3-qubit stages
- **Task:** A16
- **Method:** code/bench/gpurun -s noisecirc a16_time.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --set stage_contraction=1 --variant base --variant tensor_cores=f16,tensor_unroll=2 --variant tensor_cores=f16,tensor_unroll=8 --variant tensor_cores=f16x3,tensor_unroll=1 --variant tensor_cores=f16x3,tensor_unroll=2 --variant tensor_cores=tf32x3,tensor_unroll=1 --variant tensor_cores=tf32x3,tensor_unroll=2
- **Outcome:** exit 0; outputs in data/20261025-235415-a16-tensor-core-stages-with-preloaded-tables-sq3-n-26
- **Next:** none
- **Refs:** data/20261025-235415-a16-tensor-core-stages-with-preloaded-tables-sq3-n-26

## 2026-10-25 23:51 UTC  A16 mma.sync throughput on H100 GPU 0
- **Goal:** Achieved TFLOP/s of mma.sync m16n8k16 f16 and m16n8k8 tf32 (f32 accumulate) against independent chains per warp, and FP32 FMA rate
- **Task:** A16
- **Method:** code/bench/gpurun -s noisecirc a16_mma_rate.py
- **Outcome:** exit 0; outputs in data/20261025-235145-a16-mma-sync-throughput-on-h100-gpu-0
- **Next:** none
- **Refs:** data/20261025-235145-a16-mma-sync-throughput-on-h100-gpu-0

## 2026-10-25 23:51 UTC  A16 ablation of table-addressed tensor-core passes tf32x3 unroll 1 n=26
- **Goal:** Decompose the pass time of table-addressed tensor-core stages: fragment and address-table loads, mma, shared accesses, conversions
- **Task:** A16
- **Method:** code/bench/gpurun -s noisecirc a16_ablate.py --workloads brickwork:damping:0.000280112,qaoa:damping:0.000512821 --qubits 26 --set stage_contraction=1 --set tensor_unroll=1 --mode tf32x3
- **Outcome:** exit 0; outputs in data/20261025-234940-a16-ablation-of-table-addressed-tensor-core-passes-tf32x3-unroll-1-n-26
- **Next:** none
- **Refs:** data/20261025-234940-a16-ablation-of-table-addressed-tensor-core-passes-tf32x3-unroll-1-n-26

## 2026-10-25 23:49 UTC  A16 ablation of table-addressed tensor-core passes f16 unroll 2 n=26
- **Goal:** Decompose the pass time of table-addressed tensor-core stages: fragment and address-table loads, mma, shared accesses, conversions
- **Task:** A16
- **Method:** code/bench/gpurun -s noisecirc a16_ablate.py --workloads brickwork:damping:0.000280112,qaoa:damping:0.000512821 --qubits 26 --set stage_contraction=1 --set tensor_unroll=2 --mode f16
- **Outcome:** exit 0; outputs in data/20261025-234844-a16-ablation-of-table-addressed-tensor-core-passes-f16-unroll-2-n-26
- **Next:** none
- **Refs:** data/20261025-234844-a16-ablation-of-table-addressed-tensor-core-passes-f16-unroll-2-n-26

## 2026-10-25 23:47 UTC  A16 table-addressed tensor-core stages sweep n=26
- **Goal:** Trajectory time of tensor-core stages with per-thread address tables and unrolled tiles, over unroll, registers and mode, against contraction CUDA-core kernels
- **Task:** A16
- **Method:** code/bench/gpurun -s noisecirc a16_time.py --workloads brickwork:damping:0.000280112,qaoa:damping:0.000512821 --qubits 26 --set stage_contraction=1 --variant base --variant tensor_cores=f16,tensor_unroll=1 --variant tensor_cores=f16,tensor_unroll=2 --variant tensor_cores=f16,tensor_unroll=4 --variant tensor_cores=f16,tensor_unroll=8 --variant tensor_cores=f16,tensor_unroll=4,min_registers=96 --variant tensor_cores=f16x2,tensor_unroll=4 --variant tensor_cores=tf32,tensor_unroll=4 --variant tensor_cores=tf32x3,tensor_unroll=1 --variant tensor_cores=tf32x3,tensor_unroll=2 --variant tensor_cores=tf32x3,tensor_unroll=2,min_registers=96
- **Outcome:** exit 0; outputs in data/20261025-234700-a16-table-addressed-tensor-core-stages-sweep-n-26
- **Next:** none
- **Refs:** data/20261025-234700-a16-table-addressed-tensor-core-stages-sweep-n-26

## 2026-10-25 23:43 UTC  A16 pipelined tensor-core stages unroll and registers sweep n=26
- **Goal:** Trajectory time of pipelined tensor-core stages (no fallback) over unroll and register budget, f16/f16x2/tf32x3, against contraction CUDA-core kernels
- **Task:** A16
- **Method:** code/bench/gpurun -s noisecirc a16_time.py --workloads brickwork:damping:0.000280112,qaoa:damping:0.000512821 --qubits 26 --set stage_contraction=1 --variant base --variant tensor_cores=f16,tensor_unroll=2 --variant tensor_cores=f16,tensor_unroll=4 --variant tensor_cores=f16,tensor_unroll=2,min_registers=96 --variant tensor_cores=f16,tensor_unroll=4,min_registers=96 --variant tensor_cores=f16,tensor_unroll=4,min_registers=128 --variant tensor_cores=f16x2,tensor_unroll=2,min_registers=96 --variant tensor_cores=tf32x3,tensor_unroll=1 --variant tensor_cores=tf32x3,tensor_unroll=1,min_registers=96 --variant tensor_cores=tf32x3,tensor_unroll=2,min_registers=128
- **Outcome:** exit 0; outputs in data/20261025-234235-a16-pipelined-tensor-core-stages-unroll-and-registers-sweep-n-26
- **Next:** none
- **Refs:** data/20261025-234235-a16-pipelined-tensor-core-stages-unroll-and-registers-sweep-n-26

## 2026-10-25 23:40 UTC  A16 ablation of tensor-core passes fixed cache f16 unroll 4 n=26 rerun
- **Goal:** Decompose tensor-core pass time with the kernel cache cleared per variant and regexes for unrolled names
- **Task:** A16
- **Method:** code/bench/gpurun -s noisecirc a16_ablate.py --workloads brickwork:damping:0.000280112,qaoa:damping:0.000512821 --qubits 26 --set stage_contraction=1 --set tensor_unroll=4 --mode f16
- **Outcome:** exit 0; outputs in data/20261025-233910-a16-ablation-of-tensor-core-passes-fixed-cache-f16-unroll-4-n-26-rerun
- **Next:** none
- **Refs:** data/20261025-233910-a16-ablation-of-tensor-core-passes-fixed-cache-f16-unroll-4-n-26-rerun

## 2026-10-25 23:38 UTC  A16 ablation of tensor-core passes fixed cache f16 unroll 4 n=26
- **Goal:** Decompose tensor-core pass time (kernel cache cleared per variant; earlier ablations reused the unablated kernel and are invalid)
- **Task:** A16
- **Method:** code/bench/gpurun -s noisecirc a16_ablate.py --workloads brickwork:damping:0.000280112,qaoa:damping:0.000512821 --qubits 26 --set stage_contraction=1 --set tensor_unroll=4 --mode f16
- **Outcome:** exit 1; outputs in data/20261025-233833-a16-ablation-of-tensor-core-passes-fixed-cache-f16-unroll-4-n-26
- **Next:** none
- **Refs:** data/20261025-233833-a16-ablation-of-tensor-core-passes-fixed-cache-f16-unroll-4-n-26

## 2026-10-25 23:37 UTC  A16 ablation swizzle of tensor-core kernels f16 n=26
- **Goal:** Test whether the swizzle chosen for tensor-core accesses slows the kernel skeleton (no stages) and the CUDA-core kernel
- **Task:** A16
- **Method:** code/bench/gpurun -s noisecirc a16_ablate.py --workloads brickwork:damping:0.000280112,qaoa:damping:0.000512821 --qubits 26 --set stage_contraction=1 --set tensor_unroll=4 --mode f16
- **Outcome:** exit 0; outputs in data/20261025-233719-a16-ablation-swizzle-of-tensor-core-kernels-f16-n-26
- **Next:** none
- **Refs:** data/20261025-233719-a16-ablation-swizzle-of-tensor-core-kernels-f16-n-26

## 2026-10-25 23:36 UTC  A16 ablation of tensor-core passes unroll 4 f16 n=26
- **Goal:** Decompose tensor-core pass time with 4 tiles per warp iteration: skeleton without stages, empty stages, single ablations
- **Task:** A16
- **Method:** code/bench/gpurun -s noisecirc a16_ablate.py --workloads brickwork:damping:0.000280112,qaoa:damping:0.000512821 --qubits 26 --set stage_contraction=1 --set tensor_unroll=4 --mode f16
- **Outcome:** exit 0; outputs in data/20261025-233628-a16-ablation-of-tensor-core-passes-unroll-4-f16-n-26
- **Next:** none
- **Refs:** data/20261025-233628-a16-ablation-of-tensor-core-passes-unroll-4-f16-n-26

## 2026-10-25 23:35 UTC  A16 tensor-core stages unroll 8 brickwork qaoa n=26
- **Goal:** Error and pass time of tensor-core stages with 8 tiles per warp iteration (latency overlap), against contraction CUDA-core kernels
- **Task:** A16
- **Method:** code/bench/gpurun -s noisecirc a16_check.py --workloads brickwork:damping:0.000280112,qaoa:damping:0.000512821 --qubits 26 --set stage_contraction=1 --set tensor_unroll=8 --mode tf32x3 --mode f16x2 --mode f16
- **Outcome:** exit 0; outputs in data/20261025-233406-a16-tensor-core-stages-unroll-8-brickwork-qaoa-n-26
- **Next:** none
- **Refs:** data/20261025-233406-a16-tensor-core-stages-unroll-8-brickwork-qaoa-n-26

## 2026-10-25 23:34 UTC  A16 tensor-core stages unroll 4 brickwork qaoa n=26
- **Goal:** Error and pass time of tensor-core stages with 4 tiles per warp iteration (latency overlap), against contraction CUDA-core kernels
- **Task:** A16
- **Method:** code/bench/gpurun -s noisecirc a16_check.py --workloads brickwork:damping:0.000280112,qaoa:damping:0.000512821 --qubits 26 --set stage_contraction=1 --set tensor_unroll=4 --mode tf32x3 --mode f16x2 --mode f16
- **Outcome:** exit 0; outputs in data/20261025-233222-a16-tensor-core-stages-unroll-4-brickwork-qaoa-n-26
- **Next:** none
- **Refs:** data/20261025-233222-a16-tensor-core-stages-unroll-4-brickwork-qaoa-n-26

## 2026-10-25 23:32 UTC  A16 tensor-core stages unroll 2 brickwork qaoa n=26
- **Goal:** Error and pass time of tensor-core stages with 2 tiles per warp iteration (latency overlap), against contraction CUDA-core kernels
- **Task:** A16
- **Method:** code/bench/gpurun -s noisecirc a16_check.py --workloads brickwork:damping:0.000280112,qaoa:damping:0.000512821 --qubits 26 --set stage_contraction=1 --set tensor_unroll=2 --mode tf32x3 --mode f16x2 --mode f16
- **Outcome:** exit 0; outputs in data/20261025-233038-a16-tensor-core-stages-unroll-2-brickwork-qaoa-n-26
- **Next:** none
- **Refs:** data/20261025-233038-a16-tensor-core-stages-unroll-2-brickwork-qaoa-n-26

## 2026-10-25 23:29 UTC  A16 ablation of tensor-core passes with no-fallback f16 n=26
- **Goal:** Test whether the unexecuted CUDA-core fallback code of tensor-core stages (instruction cache) explains their slow passes
- **Task:** A16
- **Method:** code/bench/gpurun -s noisecirc a16_ablate.py --workloads brickwork:damping:0.000280112,qaoa:damping:0.000512821 --qubits 26 --set stage_contraction=1 --mode f16
- **Outcome:** exit 0; outputs in data/20261025-232854-a16-ablation-of-tensor-core-passes-with-no-fallback-f16-n-26
- **Next:** none
- **Refs:** data/20261025-232854-a16-ablation-of-tensor-core-passes-with-no-fallback-f16-n-26

## 2026-10-25 23:28 UTC  A16 ablation of tensor-core passes tf32x3 n=26
- **Goal:** Locate the time of tensor-core stage passes: without fragment loads, without mma, without shared accesses, against CUDA-core contraction kernels
- **Task:** A16
- **Method:** code/bench/gpurun -s noisecirc a16_ablate.py --workloads brickwork:damping:0.000280112,qaoa:damping:0.000512821 --qubits 26 --set stage_contraction=1 --mode tf32x3
- **Outcome:** exit 0; outputs in data/20261025-232753-a16-ablation-of-tensor-core-passes-tf32x3-n-26
- **Next:** none
- **Refs:** data/20261025-232753-a16-ablation-of-tensor-core-passes-tf32x3-n-26

## 2026-10-25 23:27 UTC  A16 ablation of tensor-core passes f16 n=26
- **Goal:** Locate the time of tensor-core stage passes: without fragment loads, without mma, without shared accesses, against CUDA-core contraction kernels
- **Task:** A16
- **Method:** code/bench/gpurun -s noisecirc a16_ablate.py --workloads brickwork:damping:0.000280112,qaoa:damping:0.000512821 --qubits 26 --set stage_contraction=1 --mode f16
- **Outcome:** exit 0; outputs in data/20261025-232744-a16-ablation-of-tensor-core-passes-f16-n-26
- **Next:** none
- **Refs:** data/20261025-232744-a16-ablation-of-tensor-core-passes-f16-n-26

## 2026-10-25 23:25 UTC  A16 tensor-core stages vs contraction kernels c64 sq3 n=26 qaoa
- **Goal:** Error vs complex128 and pass time of tf32x3/tf32x2/f16x2/tf32/f16 tensor-core stages against stage_contraction CUDA-core kernels, every block, 3-qubit stages
- **Task:** A16
- **Method:** code/bench/gpurun -s noisecirc a16_check.py --workloads qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --set stage_contraction=1 --mode tf32x3 --mode tf32x2 --mode f16x2 --mode tf32 --mode f16
- **Outcome:** exit 0; outputs in data/20261025-232157-a16-tensor-core-stages-vs-contraction-kernels-c64-sq3-n-26-qaoa
- **Next:** none
- **Refs:** data/20261025-232157-a16-tensor-core-stages-vs-contraction-kernels-c64-sq3-n-26-qaoa

## 2026-10-25 23:21 UTC  A16 tensor-core stages vs contraction kernels c64 sq3 n=26 ghz
- **Goal:** Error vs complex128 and pass time of tf32x3/tf32x2/f16x2/tf32/f16 tensor-core stages against stage_contraction CUDA-core kernels, every block, 3-qubit stages
- **Task:** A16
- **Method:** code/bench/gpurun -s noisecirc a16_check.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849 --qubits 26 --set stage_contraction=1 --mode tf32x3 --mode tf32x2 --mode f16x2 --mode tf32 --mode f16
- **Outcome:** exit 0; outputs in data/20261025-231826-a16-tensor-core-stages-vs-contraction-kernels-c64-sq3-n-26-ghz
- **Next:** none
- **Refs:** data/20261025-231826-a16-tensor-core-stages-vs-contraction-kernels-c64-sq3-n-26-ghz

## 2026-10-25 19:52 UTC  A13 stage contraction: results, implementation, GPU 0 check
- **Goal:** Answer whether a stage's contraction order can lower arithmetic, and whether the optimum is provable and easy
- **Task:** A13
- **Method:** Exact shortest path over down-sets (code/bench/a13_contraction.py); svpass Config.stage_contraction on noisecirc branch feature/stage-contraction 1556408; CPU tests + all 772 workload stages executed in Python; SASS + refit prediction (a13_contraction_predict.py)
- **Outcome:** R=4 FP/amp vs A14: brickwork -11%, grid -18%, QAOA -8%, GHZ/QFT 0; heuristics reach only part; lower bound 3-12x below; SASS FP -10/-11%, predicted passes -4% brickwork/grid. GPU 0 still fails cuInit (3) at 20:27 CET; not timed. Wiki kernel-regime corrected (min 4 per rotation only one at a time; dense 4*2^k).
- **Next:** Time stage_contraction and additive_addresses when GPU 0 works
- **Refs:** wiki/studies/kernel-regime.md, memory/tasks/A13.md, data/20261025-194446-contraction-order-of-stages-r4

## 2026-10-25 19:48 UTC  SASS and predicted passes with stage contraction c32 sq4
- **Goal:** Compile A14 kernels with and without stage_contraction (branch feature/stage-contraction) for sm_90, count SASS, predict pass time with refit
- **Task:** A13
- **Method:** code/noisecirc/.venv/bin/python code/bench/a13_contraction_predict.py
- **Outcome:** exit 0; outputs in data/20261025-194446-sass-and-predicted-passes-with-stage-contraction-c32-sq4
- **Next:** none
- **Refs:** data/20261025-194446-sass-and-predicted-passes-with-stage-contraction-c32-sq4

## 2026-10-25 19:47 UTC  Contraction order of stages R4
- **Goal:** Exact cheapest contraction order of each stage vs gate-by-gate, A14 runs/rotation form, heuristics and bounds (FP per amplitude, CPU)
- **Task:** A13
- **Method:** code/noisecirc/.venv/bin/python code/bench/a13_contraction.py 4
- **Outcome:** exit 0; outputs in data/20261025-194446-contraction-order-of-stages-r4
- **Next:** none
- **Refs:** data/20261025-194446-contraction-order-of-stages-r4

## 2026-10-25 19:45 UTC  Contraction order of stages R3
- **Goal:** Exact cheapest contraction order of each stage vs gate-by-gate, A14 runs/rotation form, heuristics and bounds (FP per amplitude, CPU)
- **Task:** A13
- **Method:** code/noisecirc/.venv/bin/python code/bench/a13_contraction.py 3
- **Outcome:** exit 0; outputs in data/20261025-194446-contraction-order-of-stages-r3
- **Next:** none
- **Refs:** data/20261025-194446-contraction-order-of-stages-r3

## 2026-10-25 09:24 UTC  A13 stage estimate free diagonals
- **Goal:** Mean stages per block with and without diagonal gates counting towards a stage's register qubits, R=3 and 4, five workloads n=26
- **Task:** A13
- **Method:** env PYTHONPATH=/itp3/home/sebastian/effsamp/code/noisecirc-bench/src:/itp3/home/sebastian/effsamp/code/noisecirc-bench/packages/svpass/src code/noisecirc/.venv/bin/python code/bench/a13_stage_estimate.py 3 4
- **Outcome:** exit 0; outputs in data/20261025-092423-a13-stage-estimate-free-diagonals
- **Next:** none
- **Refs:** data/20261025-092423-a13-stage-estimate-free-diagonals, code/bench/a13_stage_estimate.py

## 2026-10-25 09:24 UTC  A13 refit of pass-time model with SASS counts
- **Goal:** Fit models of pass time over t_bw with disassembled FP, shared, integer and control instructions on 1247 timed A13 kernels
- **Task:** A13
- **Method:** code/noisecirc/.venv/bin/python code/bench/a13_refit.py
- **Outcome:** exit 0; outputs in data/20261025-092422-a13-refit-of-pass-time-model-with-sass-counts
- **Next:** none
- **Refs:** data/20261025-092422-a13-refit-of-pass-time-model-with-sass-counts, code/bench/a13_refit.py, data/a13-analysis/refit.json

## 2026-10-25 09:22 UTC  A13 half-precision arithmetic and tile accuracy n=16 (fixed)
- **Goal:** TVD and norm error of complex64, complex32 storage (rounding per block and per stage) and half-precision arithmetic against complex128, unitary circuits, CPU emulation; rerun after a KeyError
- **Task:** A13
- **Method:** code/noisecirc/.venv/bin/python code/bench/a13_half_arith.py 16
- **Outcome:** exit 0; outputs in data/20261025-092209-a13-half-precision-arithmetic-and-tile-accuracy-n-16-fixed
- **Next:** none
- **Refs:** data/20261025-092209-a13-half-precision-arithmetic-and-tile-accuracy-n-16-fixed, code/bench/a13_half_arith.py

## 2026-10-25 09:21 UTC  A13 half-precision arithmetic and tile accuracy n=16
- **Goal:** TVD and norm error of complex64, complex32 storage (rounding per block and per stage) and half-precision arithmetic against complex128, unitary circuits, CPU emulation
- **Task:** A13
- **Method:** code/noisecirc/.venv/bin/python code/bench/a13_half_arith.py 16
- **Outcome:** exit 1; outputs in data/20261025-092155-a13-half-precision-arithmetic-and-tile-accuracy-n-16
- **Next:** none
- **Refs:** data/20261025-092155-a13-half-precision-arithmetic-and-tile-accuracy-n-16, code/bench/a13_half_arith.py

## 2026-10-25 09:21 UTC  A13 half-precision arithmetic accuracy n=16
- **Goal:** TVD and norm error of complex64, complex32 storage and half-precision arithmetic against complex128, unitary circuits, CPU emulation
- **Task:** A13
- **Method:** code/noisecirc/.venv/bin/python code/bench/a13_half_arith.py 16
- **Outcome:** exit 0; outputs in data/20261025-092129-a13-half-precision-arithmetic-accuracy-n-16
- **Next:** none
- **Refs:** data/20261025-092129-a13-half-precision-arithmetic-accuracy-n-16, code/bench/a13_half_arith.py

## 2026-10-25 09:20 UTC  A13 predicted kernel designs c32 sq4
- **Goal:** Predicted trajectory time of additive addresses and diagonal-free stages relative to A14 kernels with 4-qubit stages in complex32 (SASS counts + refitted model)
- **Task:** A13
- **Method:** code/noisecirc/.venv/bin/python code/bench/a13_predict.py
- **Outcome:** exit 0; outputs in data/20261025-091811-a13-predicted-kernel-designs-c32-sq4
- **Next:** none
- **Refs:** data/20261025-091811-a13-predicted-kernel-designs-c32-sq4, code/bench/a13_predict.py, data/a13-analysis/refit.json

## 2026-10-25 09:17 UTC  A13 SASS counts of timed blocks part 4 of 4
- **Goal:** SASS instruction classes per amplitude of every block timed in the A13 sweeps (local NVRTC sm_90 + nvdisasm), for a refit of the pass-time model
- **Task:** A13
- **Method:** code/noisecirc/.venv/bin/python code/bench/a13_sass_blocks.py data/20261024-190010-a13-block-times-complex32-max-fused-qudits-11-max-operations-256 data/20261024-190024-a13-block-times-complex32-max-fused-qudits-11-max-operations-1024 data/20261024-191352-a13-block-times-fused-kernels-base data/20261024-191404-a13-block-times-fused-kernels-sq4 data/20261024-191438-a13-block-times-fused-kernels-sq4-reg96 data/20261024-191510-a13-block-times-fused-kernels-c32 data/20261024-191530-a13-block-times-fused-kernels-w10 data/20261024-191550-a13-block-times-fused-kernels-c32-sq4 data/20261024-191623-a13-block-times-fused-kernels-c32-w10
- **Outcome:** exit 0; outputs in data/20261025-090848-a13-sass-counts-of-timed-blocks-part-4-of-4
- **Next:** none
- **Refs:** data/20261025-090848-a13-sass-counts-of-timed-blocks-part-4-of-4, code/bench/a13_sass_blocks.py, code/bench/a13_sass.py

## 2026-10-25 09:13 UTC  A12 dry run sequential Kraus sets gad qft 10000 shots
- **Goal:** Block passes with canonical, E-optimal and sequential Kraus sets, generalized amplitude damping, n=28, M=0.1 and 1, 10000 shots (more collisions)
- **Task:** A12
- **Method:** code/noisecirc/.venv/bin/python code/bench/a12_dryrun.py gad qft canonical,optimum,sequential 10000
- **Outcome:** exit 0; outputs in data/20261025-090910-a12-dry-run-sequential-kraus-sets-gad-qft-10000-shots
- **Next:** none
- **Refs:** data/20261025-090910-a12-dry-run-sequential-kraus-sets-gad-qft-10000-shots, code/bench/a12_dryrun.py

## 2026-10-25 09:10 UTC  A12 dry run sequential Kraus sets gad ghz 10000 shots
- **Goal:** Block passes with canonical, E-optimal and sequential Kraus sets, generalized amplitude damping, n=28, M=0.1 and 1, 10000 shots (more collisions)
- **Task:** A12
- **Method:** code/noisecirc/.venv/bin/python code/bench/a12_dryrun.py gad ghz canonical,optimum,sequential 10000
- **Outcome:** exit 0; outputs in data/20261025-090908-a12-dry-run-sequential-kraus-sets-gad-ghz-10000-shots
- **Next:** none
- **Refs:** data/20261025-090908-a12-dry-run-sequential-kraus-sets-gad-ghz-10000-shots, code/bench/a12_dryrun.py

## 2026-10-25 09:09 UTC  A13 SASS counts of timed blocks part 2 of 4 (rerun)
- **Goal:** SASS instruction classes per amplitude of every block timed in the A13 sweeps (local NVRTC sm_90 + nvdisasm), for a refit of the pass-time model; part 2 rerun after an assertion on 2**14-amplitude tiles
- **Task:** A13
- **Method:** code/noisecirc/.venv/bin/python code/bench/a13_sass_blocks.py data/20261024-185652-a13-block-times-complex64-max-fused-qudits-11-max-operations-64 data/20261024-185709-a13-block-times-complex64-max-fused-qudits-11-max-operations-128 data/20261024-185728-a13-block-times-complex64-max-fused-qudits-11-max-operations-256 data/20261024-185743-a13-block-times-complex64-max-fused-qudits-11-max-operations-1024 data/20261024-185751-a13-block-times-complex32-max-fused-qudits-9-max-operations-64 data/20261024-185808-a13-block-times-complex32-max-fused-qudits-9-max-operations-128 data/20261024-185823-a13-block-times-complex32-max-fused-qudits-9-max-operations-256
- **Outcome:** exit 0; outputs in data/20261025-090259-a13-sass-counts-of-timed-blocks-part-2-of-4-rerun
- **Next:** none
- **Refs:** data/20261025-090259-a13-sass-counts-of-timed-blocks-part-2-of-4-rerun, code/bench/a13_sass_blocks.py, code/bench/a13_sass.py

## 2026-10-25 09:09 UTC  A13 SASS counts of timed blocks part 3 of 4 (rerun)
- **Goal:** SASS instruction classes per amplitude of every block timed in the A13 sweeps (local NVRTC sm_90 + nvdisasm), for a refit of the pass-time model; part 2 rerun after an assertion on 2**14-amplitude tiles
- **Task:** A13
- **Method:** code/noisecirc/.venv/bin/python code/bench/a13_sass_blocks.py data/20261024-185832-a13-block-times-complex32-max-fused-qudits-9-max-operations-1024 data/20261024-185841-a13-block-times-complex32-max-fused-qudits-10-max-operations-64 data/20261024-185857-a13-block-times-complex32-max-fused-qudits-10-max-operations-128 data/20261024-185916-a13-block-times-complex32-max-fused-qudits-10-max-operations-256 data/20261024-185927-a13-block-times-complex32-max-fused-qudits-10-max-operations-1024 data/20261024-185935-a13-block-times-complex32-max-fused-qudits-11-max-operations-64 data/20261024-185952-a13-block-times-complex32-max-fused-qudits-11-max-operations-128
- **Outcome:** exit 0; outputs in data/20261025-090301-a13-sass-counts-of-timed-blocks-part-3-of-4-rerun
- **Next:** none
- **Refs:** data/20261025-090301-a13-sass-counts-of-timed-blocks-part-3-of-4-rerun, code/bench/a13_sass_blocks.py, code/bench/a13_sass.py

## 2026-10-25 09:07 UTC  A12 dry run sequential Kraus sets gad ghz,brickwork,qft
- **Goal:** Block passes with canonical, E-optimal and sequential (collision-optimal) Kraus sets, generalized amplitude damping, n=28, M=0.1 and 1, 1000 shots
- **Task:** A12
- **Method:** code/noisecirc/.venv/bin/python code/bench/a12_dryrun.py gad ghz,brickwork,qft canonical,optimum,sequential 1000
- **Outcome:** exit 0; outputs in data/20261025-090333-a12-dry-run-sequential-kraus-sets-gad-ghz-brickwork-qft
- **Next:** none
- **Refs:** data/20261025-090333-a12-dry-run-sequential-kraus-sets-gad-ghz-brickwork-qft, code/bench/a12_dryrun.py, code/bench/a12_collisions.py

## 2026-10-25 09:07 UTC  A12 dry run sequential Kraus sets gad qaoa,grid
- **Goal:** Block passes with canonical, E-optimal and sequential (collision-optimal) Kraus sets, generalized amplitude damping, n=28, M=0.1 and 1, 1000 shots
- **Task:** A12
- **Method:** code/noisecirc/.venv/bin/python code/bench/a12_dryrun.py gad qaoa,grid canonical,optimum,sequential 1000
- **Outcome:** exit 0; outputs in data/20261025-090335-a12-dry-run-sequential-kraus-sets-gad-qaoa-grid
- **Next:** none
- **Refs:** data/20261025-090335-a12-dry-run-sequential-kraus-sets-gad-qaoa-grid, code/bench/a12_dryrun.py, code/bench/a12_collisions.py

## 2026-10-25 09:04 UTC  A13 SASS counts of timed blocks part 1 of 4
- **Goal:** SASS instruction classes per amplitude of every block timed in the A13 sweeps (local NVRTC sm_90 + nvdisasm), for a refit of the pass-time model
- **Task:** A13
- **Method:** code/noisecirc/.venv/bin/python code/bench/a13_sass_blocks.py data/20261024-185525-a13-block-times-complex64-max-fused-qudits-9-max-operations-64 data/20261024-185533-a13-block-times-complex64-max-fused-qudits-9-max-operations-128 data/20261024-185541-a13-block-times-complex64-max-fused-qudits-9-max-operations-256 data/20261024-185550-a13-block-times-complex64-max-fused-qudits-9-max-operations-1024 data/20261024-185558-a13-block-times-complex64-max-fused-qudits-10-max-operations-64 data/20261024-185614-a13-block-times-complex64-max-fused-qudits-10-max-operations-128 data/20261024-185633-a13-block-times-complex64-max-fused-qudits-10-max-operations-256 data/20261024-185644-a13-block-times-complex64-max-fused-qudits-10-max-operations-1024
- **Outcome:** exit 0; outputs in data/20261025-085723-a13-sass-counts-of-timed-blocks-part-1-of-4
- **Next:** none
- **Refs:** data/20261025-085723-a13-sass-counts-of-timed-blocks-part-1-of-4, code/bench/a13_sass_blocks.py, code/bench/a13_sass.py

## 2026-10-25 09:01 UTC  A12 dry run sequential Kraus sets damp_depol ghz,brickwork,qft
- **Goal:** Block passes with canonical, E-optimal and sequential (collision-optimal) Kraus sets, damp_depol, n=28, M=0.1 and 1, 1000 shots
- **Task:** A12
- **Method:** code/noisecirc/.venv/bin/python code/bench/a12_dryrun.py damp_depol ghz,brickwork,qft canonical,optimum,sequential 1000
- **Outcome:** exit 0; outputs in data/20261025-085809-a12-dry-run-sequential-kraus-sets-damp-depol-ghz-brickwork-qft
- **Next:** none
- **Refs:** data/20261025-085809-a12-dry-run-sequential-kraus-sets-damp-depol-ghz-brickwork-qft, code/bench/a12_dryrun.py, code/bench/a12_collisions.py

## 2026-10-25 09:01 UTC  A12 dry run sequential Kraus sets damp_depol qaoa,grid
- **Goal:** Block passes with canonical, E-optimal and sequential (collision-optimal) Kraus sets, damp_depol, n=28, M=0.1 and 1, 1000 shots
- **Task:** A12
- **Method:** code/noisecirc/.venv/bin/python code/bench/a12_dryrun.py damp_depol qaoa,grid canonical,optimum,sequential 1000
- **Outcome:** exit 0; outputs in data/20261025-085811-a12-dry-run-sequential-kraus-sets-damp-depol-qaoa-grid
- **Next:** none
- **Refs:** data/20261025-085811-a12-dry-run-sequential-kraus-sets-damp-depol-qaoa-grid, code/bench/a12_dryrun.py, code/bench/a12_collisions.py

## 2026-10-25 08:57 UTC  A13 SASS counts of timed blocks part 2 of 4
- **Goal:** SASS instruction classes per amplitude of every block timed in the A13 sweeps (local NVRTC sm_90 + nvdisasm), for a refit of the pass-time model
- **Task:** A13
- **Method:** code/noisecirc/.venv/bin/python code/bench/a13_sass_blocks.py data/20261024-185652-a13-block-times-complex64-max-fused-qudits-11-max-operations-64 data/20261024-185709-a13-block-times-complex64-max-fused-qudits-11-max-operations-128 data/20261024-185728-a13-block-times-complex64-max-fused-qudits-11-max-operations-256 data/20261024-185743-a13-block-times-complex64-max-fused-qudits-11-max-operations-1024 data/20261024-185751-a13-block-times-complex32-max-fused-qudits-9-max-operations-64 data/20261024-185808-a13-block-times-complex32-max-fused-qudits-9-max-operations-128 data/20261024-185823-a13-block-times-complex32-max-fused-qudits-9-max-operations-256
- **Outcome:** exit 1; outputs in data/20261025-085725-a13-sass-counts-of-timed-blocks-part-2-of-4
- **Next:** none
- **Refs:** data/20261025-085725-a13-sass-counts-of-timed-blocks-part-2-of-4, code/bench/a13_sass_blocks.py, code/bench/a13_sass.py

## 2026-10-25 08:52 UTC  A12 collision-aware Kraus sets damp_depol,gad
- **Goal:** Distinct proposals and accepted errors per gate (P_n, A_n) of canonical, greedy, E-optimal and collision-optimal Kraus sets, p=0.01, one qubit and tensor square
- **Task:** A12
- **Method:** code/noisecirc/.venv/bin/python code/bench/a12_collisions.py damp_depol,gad
- **Outcome:** exit 0; outputs in data/20261025-085157-a12-collision-aware-kraus-sets-damp-depol-gad
- **Next:** none
- **Refs:** data/20261025-085157-a12-collision-aware-kraus-sets-damp-depol-gad, code/bench/a12_collisions.py

## 2026-10-25 08:52 UTC  A12 collision-aware Kraus sets depolarizing,dephasing,thermal
- **Goal:** Distinct proposals and accepted errors per gate (P_n, A_n) of canonical, greedy, E-optimal and collision-optimal Kraus sets, p=0.01, one qubit and tensor square
- **Task:** A12
- **Method:** code/noisecirc/.venv/bin/python code/bench/a12_collisions.py depolarizing,dephasing,thermal
- **Outcome:** exit 0; outputs in data/20261025-085155-a12-collision-aware-kraus-sets-depolarizing-dephasing-thermal
- **Next:** none
- **Refs:** data/20261025-085155-a12-collision-aware-kraus-sets-depolarizing-dephasing-thermal, code/bench/a12_collisions.py

## 2026-10-24 21:49 UTC  A12 weighted optimization over all Kraus sets (one qubit)
- **Goal:** Is there a trade-off between error proposals E and accepted errors mu?
- **Task:** A12
- **Method:** code/bench/a12_weights.py: minimize E + w mu, w=0,1,5,50, over sets of rank and rank+2 operators (BFGS, analytic gradient) and the lower bound; 7 channels, p=0.01
- **Outcome:** Same optimum for every w, at the lower bound, keeping the canonical mu: no trade-off
- **Next:** two-qubit check
- **Refs:** data/a12-kraus/weights-p0.01-1q.txt, code/bench/a12_weights.py

## 2026-10-24 21:48 UTC  A12 end-to-end summary canonical vs optimal Kraus sets
- **Goal:** GPU confirmation of the dry-run pass savings
- **Task:** A12
- **Method:** code/bench/a2_runs.py --kraus-set optimum (patched sta_sectors, a12_dryrun.optimal_maps), bench/fixes, n=28, brickwork and QFT, depolarizing and damp_depol at p for damping M=0.1/1, 3 seeds; code/bench/a12_e2e.py
- **Outcome:** depolarizing 1.33-1.40x faster (passes 1.29-1.49x fewer), damp_depol 1.12-1.23x faster (passes 1.01-1.23x)
- **Next:** wiki verdict
- **Refs:** data/a12-kraus/e2e.txt, code/bench/a12_e2e.py

## 2026-10-24 21:47 UTC  A12 end-to-end optimum Kraus sets damp_depol qft n=28
- **Goal:** End-to-end run of qft at n=28 with damp_depol noise (p as for damping M=0.1 and 1), 1000 shots, optimum Kraus sets, bench/fixes
- **Task:** A12
- **Method:** code/bench/gpurun -t 590 a2_runs.py --circuits qft --qubits 28 --noise damp_depol --ps 0.000246305,0.00246305 --shots 1000 --reps 3 --budget 450 --kraus-set optimum
- **Outcome:** exit 0; outputs in data/20261024-214502-a12-end-to-end-optimum-kraus-sets-damp-depol-qft-n-28
- **Next:** none
- **Refs:** data/20261024-214502-a12-end-to-end-optimum-kraus-sets-damp-depol-qft-n-28, code/bench/a2_runs.py, code/bench/a12_dryrun.py

## 2026-10-24 21:45 UTC  A12 end-to-end canonical Kraus sets damp_depol qft n=28
- **Goal:** End-to-end run of qft at n=28 with damp_depol noise (p as for damping M=0.1 and 1), 1000 shots, canonical Kraus sets, bench/fixes
- **Task:** A12
- **Method:** code/bench/gpurun -t 590 a2_runs.py --circuits qft --qubits 28 --noise damp_depol --ps 0.000246305,0.00246305 --shots 1000 --reps 3 --budget 450 --kraus-set canonical
- **Outcome:** exit 0; outputs in data/20261024-214151-a12-end-to-end-canonical-kraus-sets-damp-depol-qft-n-28
- **Next:** none
- **Refs:** data/20261024-214151-a12-end-to-end-canonical-kraus-sets-damp-depol-qft-n-28, code/bench/a2_runs.py, code/bench/a12_dryrun.py

## 2026-10-24 21:41 UTC  A12 end-to-end optimum Kraus sets damp_depol brickwork n=28
- **Goal:** End-to-end run of brickwork at n=28 with damp_depol noise (p as for damping M=0.1 and 1), 1000 shots, optimum Kraus sets, bench/fixes
- **Task:** A12
- **Method:** code/bench/gpurun -t 590 a2_runs.py --circuits brickwork --qubits 28 --noise damp_depol --ps 0.000242131,0.00242131 --shots 1000 --reps 3 --budget 450 --kraus-set optimum
- **Outcome:** exit 0; outputs in data/20261024-213803-a12-end-to-end-optimum-kraus-sets-damp-depol-brickwork-n-28
- **Next:** none
- **Refs:** data/20261024-213803-a12-end-to-end-optimum-kraus-sets-damp-depol-brickwork-n-28, code/bench/a2_runs.py, code/bench/a12_dryrun.py

## 2026-10-24 21:38 UTC  A12 end-to-end canonical Kraus sets damp_depol brickwork n=28
- **Goal:** End-to-end run of brickwork at n=28 with damp_depol noise (p as for damping M=0.1 and 1), 1000 shots, canonical Kraus sets, bench/fixes
- **Task:** A12
- **Method:** code/bench/gpurun -t 590 a2_runs.py --circuits brickwork --qubits 28 --noise damp_depol --ps 0.000242131,0.00242131 --shots 1000 --reps 3 --budget 450 --kraus-set canonical
- **Outcome:** exit 0; outputs in data/20261024-213356-a12-end-to-end-canonical-kraus-sets-damp-depol-brickwork-n-28
- **Next:** none
- **Refs:** data/20261024-213356-a12-end-to-end-canonical-kraus-sets-damp-depol-brickwork-n-28, code/bench/a2_runs.py, code/bench/a12_dryrun.py

## 2026-10-24 21:35 UTC  A15 peeling the last block estimate
- **Goal:** Saving of sampling outside the last block's tile from the marginal
- **Task:** A15
- **Method:** code/bench/a15_peel.py: dry-run passes per block, saving = last block passes - 0.5 x entering checkpoints; n=28, M=0.1/1
- **Outcome:** GHZ 1.49-1.57x, others 1.03-1.08x
- **Next:** none
- **Refs:** data/a15-peel, code/bench/a15_peel.py

## 2026-10-24 21:35 UTC  A15 first-jump exactness check and pass model
- **Goal:** Verify first-jump sampling is exact; estimate passes at n=28
- **Task:** A15
- **Method:** code/bench/a15_firstjump_ref.py --check (n=6, 200000 shots, chi2 vs density matrix, both samplers); code/bench/a15_firstjump.py (pass model with noisecirc block counts, n=28)
- **Outcome:** chi2 57-70 for 63 dof for both samplers (exact); model: 1.07-2x fewer passes at M<=1, 1.6-4x at M=10 without ceiling
- **Next:** kernel cost prototype
- **Refs:** data/a15-firstjump, code/bench/a15_firstjump.py

## 2026-10-24 21:35 UTC  A12 optimal Kraus sets against lower bound
- **Goal:** Optimal Kraus sets for noisecirc and certificates
- **Task:** A12
- **Method:** code/bench/a12_kraus.py (optimize over all sets, optimize_residual with canonical dominant kept, lower_bound), code/bench/a12_compare.py; 7 channels x 1 and 2 qubits, p=1e-2
- **Outcome:** Optimum = canonical dominant + rest minimized, within 0.5% of the bound for all 14 cases and all weights (no trade-off); tensor square of 1q optimum within 0.6% of 2q bound; optimize_kraus within 1% except dephasing 2q (mu 1.76x) -> fix branch fix/optimize-kraus-residual-target (9236680, worktree code/noisecirc-fix)
- **Next:** dry runs, GPU confirmation
- **Refs:** data/a12-kraus, code/bench/a12_kraus.py, code/noisecirc-fix, wiki/studies/kraus-representation.md

## 2026-10-24 21:35 UTC  A14 instruction lower bound per block
- **Goal:** Lower bound on FP instructions per amplitude, against achieved counts
- **Task:** A14
- **Method:** code/bench/a14_bound.py: 2 per non-diagonal 1q gate after merging same-qubit runs (not across multi-qubit diagonals), diagonals free, +4; CPU, n=26
- **Outcome:** GHZ at bound (38); brickwork/grid/QAOA 2.3-2.6x above; QFT 5x (diagonal phases); random circuit excluded (multi-qubit non-diagonal gates). First version wrongly merged 1q gates across cp: fixed
- **Next:** none
- **Refs:** data/a13-static/a14-bound.txt, code/bench/a14_bound.py

## 2026-10-24 21:35 UTC  A13 analysis of block-time sweeps and end-to-end runs
- **Goal:** Trajectory times per setting and end-to-end ratios
- **Task:** A13
- **Method:** code/bench/a13_analyze.py (sweep -> a13.jsonl, a13.svg), code/bench/a14_e2e.py (n=28 runs -> e2e.jsonl, e2e.svg)
- **Outcome:** complex32 alone: trajectories -4..-15% (GHZ -26%), runs 0.71-0.85; A14 kernels+sq4+complex32: runs 0.53-0.69 (gm 0.63)
- **Next:** wiki
- **Refs:** data/a13-analysis, wiki/studies/kernel-regime.md

## 2026-10-24 21:35 UTC  A13 static work model fitted to A7/A8 block times
- **Goal:** Explain pass times by static work per amplitude
- **Task:** A13
- **Method:** code/bench/kernel_ops.py counts FP instructions of generated stages and shared accesses; code/bench/a13_static.py recompiles the A7/A8 runs' circuits (CPU) and pairs counts with measured t_dom (106 blocks)
- **Outcome:** t_pass/t_bw = max(1.17, 0.90 F/206 + 0.81 S/29) fits within 12% rms (max of terms: 24%): passes are instruction-issue bound
- **Next:** precision x block-size sweep
- **Refs:** data/a13-static, code/bench/kernel_ops.py, code/bench/a13_static.py

## 2026-10-24 21:33 UTC  A12 end-to-end optimum Kraus sets depolarizing qft n=28
- **Goal:** End-to-end run of qft at n=28 with depolarizing noise (p as for damping M=0.1 and 1), 1000 shots, optimum Kraus sets, bench/fixes
- **Task:** A12
- **Method:** code/bench/gpurun -t 590 a2_runs.py --circuits qft --qubits 28 --noise depolarizing --ps 0.000246305,0.00246305 --shots 1000 --reps 3 --budget 450 --kraus-set optimum
- **Outcome:** exit 0; outputs in data/20261024-213047-a12-end-to-end-optimum-kraus-sets-depolarizing-qft-n-28
- **Next:** none
- **Refs:** data/20261024-213047-a12-end-to-end-optimum-kraus-sets-depolarizing-qft-n-28, code/bench/a2_runs.py, code/bench/a12_dryrun.py

## 2026-10-24 21:30 UTC  A12 end-to-end canonical Kraus sets depolarizing qft n=28
- **Goal:** End-to-end run of qft at n=28 with depolarizing noise (p as for damping M=0.1 and 1), 1000 shots, canonical Kraus sets, bench/fixes
- **Task:** A12
- **Method:** code/bench/gpurun -t 590 a2_runs.py --circuits qft --qubits 28 --noise depolarizing --ps 0.000246305,0.00246305 --shots 1000 --reps 3 --budget 450 --kraus-set canonical
- **Outcome:** exit 0; outputs in data/20261024-212650-a12-end-to-end-canonical-kraus-sets-depolarizing-qft-n-28
- **Next:** none
- **Refs:** data/20261024-212650-a12-end-to-end-canonical-kraus-sets-depolarizing-qft-n-28, code/bench/a2_runs.py, code/bench/a12_dryrun.py

## 2026-10-24 21:26 UTC  A12 end-to-end optimum Kraus sets depolarizing brickwork n=28
- **Goal:** End-to-end run of brickwork at n=28 with depolarizing noise (p as for damping M=0.1 and 1), 1000 shots, optimum Kraus sets, bench/fixes
- **Task:** A12
- **Method:** code/bench/gpurun -t 590 a2_runs.py --circuits brickwork --qubits 28 --noise depolarizing --ps 0.000242131,0.00242131 --shots 1000 --reps 3 --budget 450 --kraus-set optimum
- **Outcome:** exit 0; outputs in data/20261024-212254-a12-end-to-end-optimum-kraus-sets-depolarizing-brickwork-n-28
- **Next:** none
- **Refs:** data/20261024-212254-a12-end-to-end-optimum-kraus-sets-depolarizing-brickwork-n-28, code/bench/a2_runs.py, code/bench/a12_dryrun.py

## 2026-10-24 21:24 UTC  A12 dry run canonical vs optimal Kraus sets damp_depol-thermal (tensor optimum)
- **Goal:** Block passes with canonical and optimal Kraus sets (two-qubit: tensor square of the one-qubit optimum) for noise damp_depol,thermal on five circuits, n=28, M=0.1 and 1
- **Task:** A12
- **Method:** env PYTHONPATH=/itp3/home/sebastian/effsamp/code/noisecirc-bench/src:/itp3/home/sebastian/effsamp/code/noisecirc-bench/packages/svpass/src code/noisecirc/.venv/bin/python code/bench/a12_dryrun.py damp_depol,thermal ghz,brickwork,qft,qaoa,grid
- **Outcome:** exit 0; outputs in data/20261024-211910-a12-dry-run-canonical-vs-optimal-kraus-sets-damp-depol-thermal-tensor-optimum
- **Next:** none
- **Refs:** data/20261024-211910-a12-dry-run-canonical-vs-optimal-kraus-sets-damp-depol-thermal-tensor-optimum, code/bench/a12_dryrun.py, code/bench/a12_kraus.py

## 2026-10-24 21:22 UTC  A12 end-to-end canonical Kraus sets depolarizing brickwork n=28
- **Goal:** End-to-end run of brickwork at n=28 with depolarizing noise (p as for damping M=0.1 and 1), 1000 shots, canonical Kraus sets, bench/fixes
- **Task:** A12
- **Method:** code/bench/gpurun -t 590 a2_runs.py --circuits brickwork --qubits 28 --noise depolarizing --ps 0.000242131,0.00242131 --shots 1000 --reps 3 --budget 450 --kraus-set canonical
- **Outcome:** exit 0; outputs in data/20261024-211950-a12-end-to-end-canonical-kraus-sets-depolarizing-brickwork-n-28
- **Next:** none
- **Refs:** data/20261024-211950-a12-end-to-end-canonical-kraus-sets-depolarizing-brickwork-n-28, code/bench/a2_runs.py, code/bench/a12_dryrun.py

## 2026-10-24 21:22 UTC  A12 dry run canonical vs optimal Kraus sets depolarizing-dephasing (tensor optimum)
- **Goal:** Block passes with canonical and optimal Kraus sets (two-qubit: tensor square of the one-qubit optimum) for noise depolarizing,dephasing on five circuits, n=28, M=0.1 and 1
- **Task:** A12
- **Method:** env PYTHONPATH=/itp3/home/sebastian/effsamp/code/noisecirc-bench/src:/itp3/home/sebastian/effsamp/code/noisecirc-bench/packages/svpass/src code/noisecirc/.venv/bin/python code/bench/a12_dryrun.py depolarizing,dephasing ghz,brickwork,qft,qaoa,grid
- **Outcome:** exit 0; outputs in data/20261024-211908-a12-dry-run-canonical-vs-optimal-kraus-sets-depolarizing-dephasing-tensor-optimum
- **Next:** none
- **Refs:** data/20261024-211908-a12-dry-run-canonical-vs-optimal-kraus-sets-depolarizing-dephasing-tensor-optimum, code/bench/a12_dryrun.py, code/bench/a12_kraus.py

## 2026-10-24 21:22 UTC  A12 dry run canonical vs optimal Kraus sets gad (tensor optimum)
- **Goal:** Block passes with canonical and optimal Kraus sets (two-qubit: tensor square of the one-qubit optimum) for noise gad on five circuits, n=28, M=0.1 and 1
- **Task:** A12
- **Method:** env PYTHONPATH=/itp3/home/sebastian/effsamp/code/noisecirc-bench/src:/itp3/home/sebastian/effsamp/code/noisecirc-bench/packages/svpass/src code/noisecirc/.venv/bin/python code/bench/a12_dryrun.py gad ghz,brickwork,qft,qaoa,grid
- **Outcome:** exit 0; outputs in data/20261024-211912-a12-dry-run-canonical-vs-optimal-kraus-sets-gad-tensor-optimum
- **Next:** none
- **Refs:** data/20261024-211912-a12-dry-run-canonical-vs-optimal-kraus-sets-gad-tensor-optimum, code/bench/a12_dryrun.py, code/bench/a12_kraus.py

## 2026-10-24 21:18 UTC  A12 dry run canonical vs optimal Kraus sets damp_depol-thermal-gad
- **Goal:** Block passes with canonical and optimal Kraus sets for noise damp_depol,thermal,gad on five circuits, n=28, M=0.1 and 1
- **Task:** A12
- **Method:** env PYTHONPATH=/itp3/home/sebastian/effsamp/code/noisecirc-bench/src:/itp3/home/sebastian/effsamp/code/noisecirc-bench/packages/svpass/src code/noisecirc/.venv/bin/python code/bench/a12_dryrun.py damp_depol,thermal,gad ghz,brickwork,qft,qaoa,grid
- **Outcome:** blocked: timeout after 3500s; outputs in data/20261024-202014-a12-dry-run-canonical-vs-optimal-kraus-sets-damp-depol-thermal-gad
- **Next:** none
- **Refs:** data/20261024-202014-a12-dry-run-canonical-vs-optimal-kraus-sets-damp-depol-thermal-gad, code/bench/a12_dryrun.py, code/bench/a12_kraus.py

## 2026-10-24 21:18 UTC  A12 dry run canonical vs optimal Kraus sets depolarizing-dephasing
- **Goal:** Block passes with canonical and optimal Kraus sets for noise depolarizing,dephasing on five circuits, n=28, M=0.1 and 1
- **Task:** A12
- **Method:** env PYTHONPATH=/itp3/home/sebastian/effsamp/code/noisecirc-bench/src:/itp3/home/sebastian/effsamp/code/noisecirc-bench/packages/svpass/src code/noisecirc/.venv/bin/python code/bench/a12_dryrun.py depolarizing,dephasing ghz,brickwork,qft,qaoa,grid
- **Outcome:** blocked: timeout after 3500s; outputs in data/20261024-202012-a12-dry-run-canonical-vs-optimal-kraus-sets-depolarizing-dephasing
- **Next:** none
- **Refs:** data/20261024-202012-a12-dry-run-canonical-vs-optimal-kraus-sets-depolarizing-dephasing, code/bench/a12_dryrun.py, code/bench/a12_kraus.py

## 2026-10-24 21:07 UTC  A12 tests of bench/fixes with fix/optimize-kraus-residual-target
- **Goal:** svpass and noisecirc test suites on the H100 after merging the residual-target fix into bench/fixes (5c8fc57)
- **Task:** A12
- **Method:** code/bench/gpurun -t 590 run_tests.py
- **Outcome:** exit 0; outputs in data/20261024-210719-a12-tests-of-bench-fixes-with-fix-optimize-kraus-residual-target
- **Next:** none
- **Refs:** data/20261024-210719-a12-tests-of-bench-fixes-with-fix-optimize-kraus-residual-target, code/bench/run_tests.py, code/noisecirc-bench

## 2026-10-24 20:33 UTC  A15 population reductions v2 fused-sq4-c32-on
- **Goal:** Pass times at n=26 with and without per-stage population reductions (first-jump kernel cost prototype v2, partials to distinct addresses, svpass stage_populations), setting fused-sq4-c32-on
- **Task:** A15
- **Method:** code/bench/gpurun -t 590 -s noisecirc a13_blocks.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --no-masked --set stage_fusion=1 --set rotation_form=1 --set stage_qubits=4 --set dtype=complex32 --set stage_populations=1 --label pop:fused-sq4-c32-on
- **Outcome:** exit 0; outputs in data/20261024-203320-a15-population-reductions-v2-fused-sq4-c32-on
- **Next:** none
- **Refs:** data/20261024-203320-a15-population-reductions-v2-fused-sq4-c32-on, code/bench/a13_blocks.py, code/noisecirc

## 2026-10-24 20:33 UTC  A15 population reductions v2 fused-sq4-c32-off
- **Goal:** Pass times at n=26 with and without per-stage population reductions (first-jump kernel cost prototype v2, partials to distinct addresses, svpass stage_populations), setting fused-sq4-c32-off
- **Task:** A15
- **Method:** code/bench/gpurun -t 590 -s noisecirc a13_blocks.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --no-masked --set stage_fusion=1 --set rotation_form=1 --set stage_qubits=4 --set dtype=complex32 --label pop:fused-sq4-c32-off
- **Outcome:** exit 0; outputs in data/20261024-203306-a15-population-reductions-v2-fused-sq4-c32-off
- **Next:** none
- **Refs:** data/20261024-203306-a15-population-reductions-v2-fused-sq4-c32-off, code/bench/a13_blocks.py, code/noisecirc

## 2026-10-24 20:33 UTC  A15 population reductions v2 fused-on
- **Goal:** Pass times at n=26 with and without per-stage population reductions (first-jump kernel cost prototype v2, partials to distinct addresses, svpass stage_populations), setting fused-on
- **Task:** A15
- **Method:** code/bench/gpurun -t 590 -s noisecirc a13_blocks.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --no-masked --set stage_fusion=1 --set rotation_form=1 --set stage_populations=1 --label pop:fused-on
- **Outcome:** exit 0; outputs in data/20261024-203255-a15-population-reductions-v2-fused-on
- **Next:** none
- **Refs:** data/20261024-203255-a15-population-reductions-v2-fused-on, code/bench/a13_blocks.py, code/noisecirc

## 2026-10-24 20:32 UTC  A15 population reductions v2 fused-off
- **Goal:** Pass times at n=26 with and without per-stage population reductions (first-jump kernel cost prototype v2, partials to distinct addresses, svpass stage_populations), setting fused-off
- **Task:** A15
- **Method:** code/bench/gpurun -t 590 -s noisecirc a13_blocks.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --no-masked --set stage_fusion=1 --set rotation_form=1 --label pop:fused-off
- **Outcome:** exit 0; outputs in data/20261024-203246-a15-population-reductions-v2-fused-off
- **Next:** none
- **Refs:** data/20261024-203246-a15-population-reductions-v2-fused-off, code/bench/a13_blocks.py, code/noisecirc

## 2026-10-24 20:32 UTC  A15 population reductions v2 default-on
- **Goal:** Pass times at n=26 with and without per-stage population reductions (first-jump kernel cost prototype v2, partials to distinct addresses, svpass stage_populations), setting default-on
- **Task:** A15
- **Method:** code/bench/gpurun -t 590 -s noisecirc a13_blocks.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --no-masked --set stage_populations=1 --label pop:default-on
- **Outcome:** exit 0; outputs in data/20261024-203235-a15-population-reductions-v2-default-on
- **Next:** none
- **Refs:** data/20261024-203235-a15-population-reductions-v2-default-on, code/bench/a13_blocks.py, code/noisecirc

## 2026-10-24 20:32 UTC  A15 population reductions v2 default-off
- **Goal:** Pass times at n=26 with and without per-stage population reductions (first-jump kernel cost prototype v2, partials to distinct addresses, svpass stage_populations), setting default-off
- **Task:** A15
- **Method:** code/bench/gpurun -t 590 -s noisecirc a13_blocks.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --no-masked --label pop:default-off
- **Outcome:** exit 0; outputs in data/20261024-203228-a15-population-reductions-v2-default-off
- **Next:** none
- **Refs:** data/20261024-203228-a15-population-reductions-v2-default-off, code/bench/a13_blocks.py, code/noisecirc

## 2026-10-24 20:32 UTC  A15 population reductions v1 summary
- **Goal:** Kernel cost of per-stage population reductions (first-jump sampling) with the v1 prototype
- **Task:** A15
- **Method:** svpass stage_populations v1: per stage, per register qubit, warp shuffle reduction then a double atomicAdd by lane 0 to one of 256 shared global addresses; a13_blocks.py n=26, dominant kernels
- **Outcome:** Trajectory time 2.3-3.6x (default kernels), 2.2-3.6x (A14 kernels), 3.0-4.1x (A14, 4-qubit stages, complex32) of the same kernels without reductions, e.g. QFT 10.0 -> 36.4 ms. Dominated by contention of all warps on the same 256 atomic addresses, an artifact: v2 writes partials to distinct addresses
- **Next:** time v2
- **Refs:** code/noisecirc, code/bench/a13_blocks.py

## 2026-10-24 20:31 UTC  A15 population reductions fused-sq4-c32-on
- **Goal:** Pass times at n=26 with and without per-stage population reductions (first-jump kernel cost prototype, svpass stage_populations), setting fused-sq4-c32-on
- **Task:** A15
- **Method:** code/bench/gpurun -t 590 -s noisecirc a13_blocks.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --no-masked --set stage_fusion=1 --set rotation_form=1 --set stage_qubits=4 --set dtype=complex32 --set stage_populations=1 --label pop:fused-sq4-c32-on
- **Outcome:** exit 0; prototype v1 (contended global atomics); outputs deleted by mistake, times kept in the entry "A15 population reductions v1 summary"
- **Next:** none
- **Refs:** code/bench/a13_blocks.py, code/noisecirc

## 2026-10-24 20:31 UTC  A15 population reductions fused-sq4-c32-off
- **Goal:** Pass times at n=26 with and without per-stage population reductions (first-jump kernel cost prototype, svpass stage_populations), setting fused-sq4-c32-off
- **Task:** A15
- **Method:** code/bench/gpurun -t 590 -s noisecirc a13_blocks.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --no-masked --set stage_fusion=1 --set rotation_form=1 --set stage_qubits=4 --set dtype=complex32 --label pop:fused-sq4-c32-off
- **Outcome:** exit 0; prototype v1 (contended global atomics); outputs deleted by mistake, times kept in the entry "A15 population reductions v1 summary"
- **Next:** none
- **Refs:** code/bench/a13_blocks.py, code/noisecirc

## 2026-10-24 20:31 UTC  A15 population reductions fused-on
- **Goal:** Pass times at n=26 with and without per-stage population reductions (first-jump kernel cost prototype, svpass stage_populations), setting fused-on
- **Task:** A15
- **Method:** code/bench/gpurun -t 590 -s noisecirc a13_blocks.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --no-masked --set stage_fusion=1 --set rotation_form=1 --set stage_populations=1 --label pop:fused-on
- **Outcome:** exit 0; prototype v1 (contended global atomics); outputs deleted by mistake, times kept in the entry "A15 population reductions v1 summary"
- **Next:** none
- **Refs:** code/bench/a13_blocks.py, code/noisecirc

## 2026-10-24 20:30 UTC  A15 population reductions fused-off
- **Goal:** Pass times at n=26 with and without per-stage population reductions (first-jump kernel cost prototype, svpass stage_populations), setting fused-off
- **Task:** A15
- **Method:** code/bench/gpurun -t 590 -s noisecirc a13_blocks.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --no-masked --set stage_fusion=1 --set rotation_form=1 --label pop:fused-off
- **Outcome:** exit 0; prototype v1 (contended global atomics); outputs deleted by mistake, times kept in the entry "A15 population reductions v1 summary"
- **Next:** none
- **Refs:** code/bench/a13_blocks.py, code/noisecirc

## 2026-10-24 20:30 UTC  A15 population reductions default-on
- **Goal:** Pass times at n=26 with and without per-stage population reductions (first-jump kernel cost prototype, svpass stage_populations), setting default-on
- **Task:** A15
- **Method:** code/bench/gpurun -t 590 -s noisecirc a13_blocks.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --no-masked --set stage_populations=1 --label pop:default-on
- **Outcome:** exit 0; prototype v1 (contended global atomics); outputs deleted by mistake, times kept in the entry "A15 population reductions v1 summary"
- **Next:** none
- **Refs:** code/bench/a13_blocks.py, code/noisecirc

## 2026-10-24 20:30 UTC  A15 population reductions default-off
- **Goal:** Pass times at n=26 with and without per-stage population reductions (first-jump kernel cost prototype, svpass stage_populations), setting default-off
- **Task:** A15
- **Method:** code/bench/gpurun -t 590 -s noisecirc a13_blocks.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --no-masked --label pop:default-off
- **Outcome:** exit 0; prototype v1 (contended global atomics); outputs deleted by mistake, times kept in the entry "A15 population reductions v1 summary"
- **Next:** none
- **Refs:** code/bench/a13_blocks.py, code/noisecirc

## 2026-10-24 20:29 UTC  A13 A14 end-to-end c32 grid n=28
- **Goal:** End-to-end noisy run of grid at n=28, damping M=0.1 and 1, 1000 shots, complex32 with the default kernels (noisecirc feature/stage-fusion, flags off)
- **Task:** A13
- **Method:** code/bench/gpurun -t 590 -s noisecirc a2_runs.py --circuits grid --qubits 28 --noise damping --ps 0.000141443,0.00141443 --shots 1000 --reps 3 --budget 450 --config dtype=complex32
- **Outcome:** exit 0; outputs in data/20261024-202449-a13-a14-end-to-end-c32-grid-n-28
- **Next:** none
- **Refs:** data/20261024-202449-a13-a14-end-to-end-c32-grid-n-28, code/bench/a2_runs.py, code/noisecirc

## 2026-10-24 20:24 UTC  A13 A14 end-to-end c32 qaoa n=28
- **Goal:** End-to-end noisy run of qaoa at n=28, damping M=0.1 and 1, 1000 shots, complex32 with the default kernels (noisecirc feature/stage-fusion, flags off)
- **Task:** A13
- **Method:** code/bench/gpurun -t 590 -s noisecirc a2_runs.py --circuits qaoa --qubits 28 --noise damping --ps 0.00047619,0.0047619 --shots 1000 --reps 3 --budget 450 --config dtype=complex32
- **Outcome:** exit 0; outputs in data/20261024-202330-a13-a14-end-to-end-c32-qaoa-n-28
- **Next:** none
- **Refs:** data/20261024-202330-a13-a14-end-to-end-c32-qaoa-n-28, code/bench/a2_runs.py, code/noisecirc

## 2026-10-24 20:23 UTC  A13 A14 end-to-end c32 qft n=28
- **Goal:** End-to-end noisy run of qft at n=28, damping M=0.1 and 1, 1000 shots, complex32 with the default kernels (noisecirc feature/stage-fusion, flags off)
- **Task:** A13
- **Method:** code/bench/gpurun -t 590 -s noisecirc a2_runs.py --circuits qft --qubits 28 --noise damping --ps 0.000246305,0.00246305 --shots 1000 --reps 3 --budget 450 --config dtype=complex32
- **Outcome:** exit 0; outputs in data/20261024-202155-a13-a14-end-to-end-c32-qft-n-28
- **Next:** none
- **Refs:** data/20261024-202155-a13-a14-end-to-end-c32-qft-n-28, code/bench/a2_runs.py, code/noisecirc

## 2026-10-24 20:21 UTC  A13 A14 end-to-end c32 brickwork n=28
- **Goal:** End-to-end noisy run of brickwork at n=28, damping M=0.1 and 1, 1000 shots, complex32 with the default kernels (noisecirc feature/stage-fusion, flags off)
- **Task:** A13
- **Method:** code/bench/gpurun -t 590 -s noisecirc a2_runs.py --circuits brickwork --qubits 28 --noise damping --ps 0.000242131,0.00242131 --shots 1000 --reps 3 --budget 450 --config dtype=complex32
- **Outcome:** exit 0; outputs in data/20261024-201909-a13-a14-end-to-end-c32-brickwork-n-28
- **Next:** none
- **Refs:** data/20261024-201909-a13-a14-end-to-end-c32-brickwork-n-28, code/bench/a2_runs.py, code/noisecirc

## 2026-10-24 20:20 UTC  A12 dry runs with optimize_kraus aborted
- **Goal:** Dry-run block passes for canonical, optimize_kraus and optimal Kraus sets, five circuits, five noise kinds
- **Task:** A12
- **Method:** code/bench/a12_dryrun.py with all three sets, two parallel CPU processes
- **Outcome:** Killed after about 50 min: optimize_kraus re-optimizes every distinct gate (hundreds of random angles in brickwork/QFT, up to 20 s per two-qubit set), so the runs would exceed their timeouts; outputs incomplete and deleted. optimize_kraus is within 1% of the optimum per gate (data/a12-kraus), so the dry run now compares canonical and optimum only
- **Next:** rerun a12_dryrun.py with two sets
- **Refs:** code/bench/a12_dryrun.py, data/a12-kraus

## 2026-10-24 20:19 UTC  A13 A14 end-to-end c32 ghz n=28
- **Goal:** End-to-end noisy run of ghz at n=28, damping M=0.1 and 1, 1000 shots, complex32 with the default kernels (noisecirc feature/stage-fusion, flags off)
- **Task:** A13
- **Method:** code/bench/gpurun -t 590 -s noisecirc a2_runs.py --circuits ghz --qubits 28 --noise damping --ps 0.00183486,0.0183486 --shots 1000 --reps 3 --budget 450 --config dtype=complex32
- **Outcome:** exit 0; outputs in data/20261024-201839-a13-a14-end-to-end-c32-ghz-n-28
- **Next:** none
- **Refs:** data/20261024-201839-a13-a14-end-to-end-c32-ghz-n-28, code/bench/a2_runs.py, code/noisecirc

## 2026-10-24 20:18 UTC  A15 readout map dry run
- **Goal:** Block passes when channels followed only by tail (diagonal, measurement-final) gates are applied as classical readout noise, five circuits, n=28, damping M=0.1/1, 1000 shots
- **Task:** A15
- **Method:** env PYTHONPATH=/itp3/home/sebastian/effsamp/code/noisecirc-bench/src:/itp3/home/sebastian/effsamp/code/noisecirc-bench/packages/svpass/src code/noisecirc/.venv/bin/python code/bench/a15_readout.py
- **Outcome:** exit 0; outputs in data/20261024-201403-a15-readout-map-dry-run
- **Next:** none
- **Refs:** data/20261024-201403-a15-readout-map-dry-run, code/bench/a15_readout.py, code/bench/a15_readout_check.py, data/a15-readout

## 2026-10-24 20:11 UTC  A13 A14 end-to-end fused-sq4-c32 grid n=28
- **Goal:** End-to-end noisy run of grid at n=28, damping M=0.1 and 1, 1000 shots, kernels fused-sq4-c32 (noisecirc feature/stage-fusion)
- **Task:** A14
- **Method:** code/bench/gpurun -t 590 -s noisecirc a2_runs.py --circuits grid --qubits 28 --noise damping --ps 0.000141443,0.00141443 --shots 1000 --reps 3 --budget 450 --config stage_fusion=1 --config rotation_form=1 --config stage_qubits=4 --config dtype=complex32
- **Outcome:** exit 0; outputs in data/20261024-200741-a13-a14-end-to-end-fused-sq4-c32-grid-n-28
- **Next:** none
- **Refs:** data/20261024-200741-a13-a14-end-to-end-fused-sq4-c32-grid-n-28, code/bench/a2_runs.py, code/noisecirc

## 2026-10-24 20:07 UTC  A13 A14 end-to-end fused-sq4-c32 qaoa n=28
- **Goal:** End-to-end noisy run of qaoa at n=28, damping M=0.1 and 1, 1000 shots, kernels fused-sq4-c32 (noisecirc feature/stage-fusion)
- **Task:** A14
- **Method:** code/bench/gpurun -t 590 -s noisecirc a2_runs.py --circuits qaoa --qubits 28 --noise damping --ps 0.00047619,0.0047619 --shots 1000 --reps 3 --budget 450 --config stage_fusion=1 --config rotation_form=1 --config stage_qubits=4 --config dtype=complex32
- **Outcome:** exit 0; outputs in data/20261024-200638-a13-a14-end-to-end-fused-sq4-c32-qaoa-n-28
- **Next:** none
- **Refs:** data/20261024-200638-a13-a14-end-to-end-fused-sq4-c32-qaoa-n-28, code/bench/a2_runs.py, code/noisecirc

## 2026-10-24 20:06 UTC  A13 A14 end-to-end fused-sq4-c32 qft n=28
- **Goal:** End-to-end noisy run of qft at n=28, damping M=0.1 and 1, 1000 shots, kernels fused-sq4-c32 (noisecirc feature/stage-fusion)
- **Task:** A14
- **Method:** code/bench/gpurun -t 590 -s noisecirc a2_runs.py --circuits qft --qubits 28 --noise damping --ps 0.000246305,0.00246305 --shots 1000 --reps 3 --budget 450 --config stage_fusion=1 --config rotation_form=1 --config stage_qubits=4 --config dtype=complex32
- **Outcome:** exit 0; outputs in data/20261024-200522-a13-a14-end-to-end-fused-sq4-c32-qft-n-28
- **Next:** none
- **Refs:** data/20261024-200522-a13-a14-end-to-end-fused-sq4-c32-qft-n-28, code/bench/a2_runs.py, code/noisecirc

## 2026-10-24 20:05 UTC  A13 A14 end-to-end fused-sq4-c32 brickwork n=28
- **Goal:** End-to-end noisy run of brickwork at n=28, damping M=0.1 and 1, 1000 shots, kernels fused-sq4-c32 (noisecirc feature/stage-fusion)
- **Task:** A14
- **Method:** code/bench/gpurun -t 590 -s noisecirc a2_runs.py --circuits brickwork --qubits 28 --noise damping --ps 0.000242131,0.00242131 --shots 1000 --reps 3 --budget 450 --config stage_fusion=1 --config rotation_form=1 --config stage_qubits=4 --config dtype=complex32
- **Outcome:** exit 0; outputs in data/20261024-200257-a13-a14-end-to-end-fused-sq4-c32-brickwork-n-28
- **Next:** none
- **Refs:** data/20261024-200257-a13-a14-end-to-end-fused-sq4-c32-brickwork-n-28, code/bench/a2_runs.py, code/noisecirc

## 2026-10-24 20:02 UTC  A13 A14 end-to-end fused-sq4-c32 ghz n=28
- **Goal:** End-to-end noisy run of ghz at n=28, damping M=0.1 and 1, 1000 shots, kernels fused-sq4-c32 (noisecirc feature/stage-fusion)
- **Task:** A14
- **Method:** code/bench/gpurun -t 590 -s noisecirc a2_runs.py --circuits ghz --qubits 28 --noise damping --ps 0.00183486,0.0183486 --shots 1000 --reps 3 --budget 450 --config stage_fusion=1 --config rotation_form=1 --config stage_qubits=4 --config dtype=complex32
- **Outcome:** exit 0; outputs in data/20261024-200228-a13-a14-end-to-end-fused-sq4-c32-ghz-n-28
- **Next:** none
- **Refs:** data/20261024-200228-a13-a14-end-to-end-fused-sq4-c32-ghz-n-28, code/bench/a2_runs.py, code/noisecirc

## 2026-10-24 20:02 UTC  A13 A14 end-to-end fused-sq4 grid n=28
- **Goal:** End-to-end noisy run of grid at n=28, damping M=0.1 and 1, 1000 shots, kernels fused-sq4 (noisecirc feature/stage-fusion)
- **Task:** A14
- **Method:** code/bench/gpurun -t 590 -s noisecirc a2_runs.py --circuits grid --qubits 28 --noise damping --ps 0.000141443,0.00141443 --shots 1000 --reps 3 --budget 450 --config stage_fusion=1 --config rotation_form=1 --config stage_qubits=4
- **Outcome:** exit 0; outputs in data/20261024-195942-a13-a14-end-to-end-fused-sq4-grid-n-28
- **Next:** none
- **Refs:** data/20261024-195942-a13-a14-end-to-end-fused-sq4-grid-n-28, code/bench/a2_runs.py, code/noisecirc

## 2026-10-24 20:00 UTC  A15 first-jump reference pass counts n=10
- **Goal:** Block passes of noisecirc's proposals vs first-jump sampling (with and without oversampling ceiling) with real states, NumPy reference on noisecirc's compiled blocks, n=10, 1000 shots, damping M=0.1/1/3
- **Task:** A15
- **Method:** env PYTHONPATH=/itp3/home/sebastian/effsamp/code/noisecirc-bench/src:/itp3/home/sebastian/effsamp/code/noisecirc-bench/packages/svpass/src code/noisecirc/.venv/bin/python code/bench/a15_firstjump_ref.py
- **Outcome:** exit 0; outputs in data/20261024-195809-a15-first-jump-reference-pass-counts-n-10
- **Next:** none
- **Refs:** data/20261024-195809-a15-first-jump-reference-pass-counts-n-10, code/bench/a15_firstjump_ref.py

## 2026-10-24 19:59 UTC  A13 A14 end-to-end fused-sq4 qaoa n=28
- **Goal:** End-to-end noisy run of qaoa at n=28, damping M=0.1 and 1, 1000 shots, kernels fused-sq4 (noisecirc feature/stage-fusion)
- **Task:** A14
- **Method:** code/bench/gpurun -t 590 -s noisecirc a2_runs.py --circuits qaoa --qubits 28 --noise damping --ps 0.00047619,0.0047619 --shots 1000 --reps 3 --budget 450 --config stage_fusion=1 --config rotation_form=1 --config stage_qubits=4
- **Outcome:** exit 0; outputs in data/20261024-195816-a13-a14-end-to-end-fused-sq4-qaoa-n-28
- **Next:** none
- **Refs:** data/20261024-195816-a13-a14-end-to-end-fused-sq4-qaoa-n-28, code/bench/a2_runs.py, code/noisecirc

## 2026-10-24 19:58 UTC  A13 A14 end-to-end fused-sq4 qft n=28
- **Goal:** End-to-end noisy run of qft at n=28, damping M=0.1 and 1, 1000 shots, kernels fused-sq4 (noisecirc feature/stage-fusion)
- **Task:** A14
- **Method:** code/bench/gpurun -t 590 -s noisecirc a2_runs.py --circuits qft --qubits 28 --noise damping --ps 0.000246305,0.00246305 --shots 1000 --reps 3 --budget 450 --config stage_fusion=1 --config rotation_form=1 --config stage_qubits=4
- **Outcome:** exit 0; outputs in data/20261024-195610-a13-a14-end-to-end-fused-sq4-qft-n-28
- **Next:** none
- **Refs:** data/20261024-195610-a13-a14-end-to-end-fused-sq4-qft-n-28, code/bench/a2_runs.py, code/noisecirc

## 2026-10-24 19:56 UTC  A13 A14 end-to-end fused-sq4 brickwork n=28
- **Goal:** End-to-end noisy run of brickwork at n=28, damping M=0.1 and 1, 1000 shots, kernels fused-sq4 (noisecirc feature/stage-fusion)
- **Task:** A14
- **Method:** code/bench/gpurun -t 590 -s noisecirc a2_runs.py --circuits brickwork --qubits 28 --noise damping --ps 0.000242131,0.00242131 --shots 1000 --reps 3 --budget 450 --config stage_fusion=1 --config rotation_form=1 --config stage_qubits=4
- **Outcome:** exit 0; outputs in data/20261024-195302-a13-a14-end-to-end-fused-sq4-brickwork-n-28
- **Next:** none
- **Refs:** data/20261024-195302-a13-a14-end-to-end-fused-sq4-brickwork-n-28, code/bench/a2_runs.py, code/noisecirc

## 2026-10-24 19:53 UTC  A13 A14 end-to-end fused-sq4 ghz n=28
- **Goal:** End-to-end noisy run of ghz at n=28, damping M=0.1 and 1, 1000 shots, kernels fused-sq4 (noisecirc feature/stage-fusion)
- **Task:** A14
- **Method:** code/bench/gpurun -t 590 -s noisecirc a2_runs.py --circuits ghz --qubits 28 --noise damping --ps 0.00183486,0.0183486 --shots 1000 --reps 3 --budget 450 --config stage_fusion=1 --config rotation_form=1 --config stage_qubits=4
- **Outcome:** exit 0; outputs in data/20261024-195221-a13-a14-end-to-end-fused-sq4-ghz-n-28
- **Next:** none
- **Refs:** data/20261024-195221-a13-a14-end-to-end-fused-sq4-ghz-n-28, code/bench/a2_runs.py, code/noisecirc

## 2026-10-24 19:52 UTC  A13 A14 end-to-end fused grid n=28
- **Goal:** End-to-end noisy run of grid at n=28, damping M=0.1 and 1, 1000 shots, kernels fused (noisecirc feature/stage-fusion)
- **Task:** A14
- **Method:** code/bench/gpurun -t 590 -s noisecirc a2_runs.py --circuits grid --qubits 28 --noise damping --ps 0.000141443,0.00141443 --shots 1000 --reps 3 --budget 450 --config stage_fusion=1 --config rotation_form=1
- **Outcome:** exit 0; outputs in data/20261024-194939-a13-a14-end-to-end-fused-grid-n-28
- **Next:** none
- **Refs:** data/20261024-194939-a13-a14-end-to-end-fused-grid-n-28, code/bench/a2_runs.py, code/noisecirc

## 2026-10-24 19:49 UTC  A13 A14 end-to-end fused qaoa n=28
- **Goal:** End-to-end noisy run of qaoa at n=28, damping M=0.1 and 1, 1000 shots, kernels fused (noisecirc feature/stage-fusion)
- **Task:** A14
- **Method:** code/bench/gpurun -t 590 -s noisecirc a2_runs.py --circuits qaoa --qubits 28 --noise damping --ps 0.00047619,0.0047619 --shots 1000 --reps 3 --budget 450 --config stage_fusion=1 --config rotation_form=1
- **Outcome:** exit 0; outputs in data/20261024-194814-a13-a14-end-to-end-fused-qaoa-n-28
- **Next:** none
- **Refs:** data/20261024-194814-a13-a14-end-to-end-fused-qaoa-n-28, code/bench/a2_runs.py, code/noisecirc

## 2026-10-24 19:48 UTC  A13 A14 end-to-end fused qft n=28
- **Goal:** End-to-end noisy run of qft at n=28, damping M=0.1 and 1, 1000 shots, kernels fused (noisecirc feature/stage-fusion)
- **Task:** A14
- **Method:** code/bench/gpurun -t 590 -s noisecirc a2_runs.py --circuits qft --qubits 28 --noise damping --ps 0.000246305,0.00246305 --shots 1000 --reps 3 --budget 450 --config stage_fusion=1 --config rotation_form=1
- **Outcome:** exit 0; outputs in data/20261024-194600-a13-a14-end-to-end-fused-qft-n-28
- **Next:** none
- **Refs:** data/20261024-194600-a13-a14-end-to-end-fused-qft-n-28, code/bench/a2_runs.py, code/noisecirc

## 2026-10-24 19:46 UTC  A13 A14 end-to-end fused brickwork n=28
- **Goal:** End-to-end noisy run of brickwork at n=28, damping M=0.1 and 1, 1000 shots, kernels fused (noisecirc feature/stage-fusion)
- **Task:** A14
- **Method:** code/bench/gpurun -t 590 -s noisecirc a2_runs.py --circuits brickwork --qubits 28 --noise damping --ps 0.000242131,0.00242131 --shots 1000 --reps 3 --budget 450 --config stage_fusion=1 --config rotation_form=1
- **Outcome:** exit 0; outputs in data/20261024-194258-a13-a14-end-to-end-fused-brickwork-n-28
- **Next:** none
- **Refs:** data/20261024-194258-a13-a14-end-to-end-fused-brickwork-n-28, code/bench/a2_runs.py, code/noisecirc

## 2026-10-24 19:42 UTC  A13 A14 end-to-end fused ghz n=28
- **Goal:** End-to-end noisy run of ghz at n=28, damping M=0.1 and 1, 1000 shots, kernels fused (noisecirc feature/stage-fusion)
- **Task:** A14
- **Method:** code/bench/gpurun -t 590 -s noisecirc a2_runs.py --circuits ghz --qubits 28 --noise damping --ps 0.00183486,0.0183486 --shots 1000 --reps 3 --budget 450 --config stage_fusion=1 --config rotation_form=1
- **Outcome:** exit 0; outputs in data/20261024-194220-a13-a14-end-to-end-fused-ghz-n-28
- **Next:** none
- **Refs:** data/20261024-194220-a13-a14-end-to-end-fused-ghz-n-28, code/bench/a2_runs.py, code/noisecirc

## 2026-10-24 19:42 UTC  A13 A14 end-to-end default grid n=28
- **Goal:** End-to-end noisy run of grid at n=28, damping M=0.1 and 1, 1000 shots, kernels default (noisecirc feature/stage-fusion)
- **Task:** A14
- **Method:** code/bench/gpurun -t 590 -s noisecirc a2_runs.py --circuits grid --qubits 28 --noise damping --ps 0.000141443,0.00141443 --shots 1000 --reps 3 --budget 450
- **Outcome:** exit 0; outputs in data/20261024-193930-a13-a14-end-to-end-default-grid-n-28
- **Next:** none
- **Refs:** data/20261024-193930-a13-a14-end-to-end-default-grid-n-28, code/bench/a2_runs.py, code/noisecirc

## 2026-10-24 19:39 UTC  A13 A14 end-to-end default qaoa n=28
- **Goal:** End-to-end noisy run of qaoa at n=28, damping M=0.1 and 1, 1000 shots, kernels default (noisecirc feature/stage-fusion)
- **Task:** A14
- **Method:** code/bench/gpurun -t 590 -s noisecirc a2_runs.py --circuits qaoa --qubits 28 --noise damping --ps 0.00047619,0.0047619 --shots 1000 --reps 3 --budget 450
- **Outcome:** exit 0; outputs in data/20261024-193758-a13-a14-end-to-end-default-qaoa-n-28
- **Next:** none
- **Refs:** data/20261024-193758-a13-a14-end-to-end-default-qaoa-n-28, code/bench/a2_runs.py, code/noisecirc

## 2026-10-24 19:37 UTC  A13 A14 end-to-end default qft n=28
- **Goal:** End-to-end noisy run of qft at n=28, damping M=0.1 and 1, 1000 shots, kernels default (noisecirc feature/stage-fusion)
- **Task:** A14
- **Method:** code/bench/gpurun -t 590 -s noisecirc a2_runs.py --circuits qft --qubits 28 --noise damping --ps 0.000246305,0.00246305 --shots 1000 --reps 3 --budget 450
- **Outcome:** exit 0; outputs in data/20261024-193547-a13-a14-end-to-end-default-qft-n-28
- **Next:** none
- **Refs:** data/20261024-193547-a13-a14-end-to-end-default-qft-n-28, code/bench/a2_runs.py, code/noisecirc

## 2026-10-24 19:37 UTC  A12 dry run Kraus sets damp_depol-thermal-gad
- **Goal:** Block passes with canonical, optimize_kraus and optimal Kraus sets for noise damp_depol,thermal,gad on five circuits, n=28, M=0.1 and 1
- **Task:** A12
- **Method:** env PYTHONPATH=/itp3/home/sebastian/effsamp/code/noisecirc-bench/src:/itp3/home/sebastian/effsamp/code/noisecirc-bench/packages/svpass/src code/noisecirc/.venv/bin/python code/bench/a12_dryrun.py damp_depol,thermal,gad ghz,brickwork,qft,qaoa,grid
- **Outcome:** exit 1 at once: code/bench/noise.py had no channel damp_depol (added); failed output deleted, rerun in the entry above
- **Next:** none
- **Refs:** code/bench/noise.py, code/bench/a12_dryrun.py, code/bench/a12_kraus.py

## 2026-10-24 19:35 UTC  A13 A14 end-to-end default brickwork n=28
- **Goal:** End-to-end noisy run of brickwork at n=28, damping M=0.1 and 1, 1000 shots, kernels default (noisecirc feature/stage-fusion)
- **Task:** A14
- **Method:** code/bench/gpurun -t 590 -s noisecirc a2_runs.py --circuits brickwork --qubits 28 --noise damping --ps 0.000242131,0.00242131 --shots 1000 --reps 3 --budget 450
- **Outcome:** exit 0; outputs in data/20261024-193231-a13-a14-end-to-end-default-brickwork-n-28
- **Next:** none
- **Refs:** data/20261024-193231-a13-a14-end-to-end-default-brickwork-n-28, code/bench/a2_runs.py, code/noisecirc

## 2026-10-24 19:32 UTC  A13 A14 end-to-end default ghz n=28
- **Goal:** End-to-end noisy run of ghz at n=28, damping M=0.1 and 1, 1000 shots, kernels default (noisecirc feature/stage-fusion)
- **Task:** A14
- **Method:** code/bench/gpurun -t 590 -s noisecirc a2_runs.py --circuits ghz --qubits 28 --noise damping --ps 0.00183486,0.0183486 --shots 1000 --reps 3 --budget 450
- **Outcome:** exit 0; outputs in data/20261024-193150-a13-a14-end-to-end-default-ghz-n-28
- **Next:** none
- **Refs:** data/20261024-193150-a13-a14-end-to-end-default-ghz-n-28, code/bench/a2_runs.py, code/noisecirc

## 2026-10-24 19:31 UTC  A13 complex32 accuracy n=24
- **Goal:** Accuracy of complex32 and complex64 against complex128 for the no-error trajectory through each circuit, fused kernels with 4-qubit stages
- **Task:** A13
- **Method:** code/bench/gpurun -t 590 -s noisecirc a13_accuracy.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094,random:damping:0.0001 --qubits 24 --set stage_fusion=1 --set rotation_form=1 --set stage_qubits=4
- **Outcome:** exit 0; outputs in data/20261024-192627-a13-complex32-accuracy-n-24
- **Next:** none
- **Refs:** data/20261024-192627-a13-complex32-accuracy-n-24, code/bench/a13_accuracy.py

## 2026-10-24 19:16 UTC  A13 block times fused kernels c32-w10
- **Goal:** Pass times at n=26 with stage fusion and rotation form (noisecirc feature/stage-fusion), setting c32-w10
- **Task:** A13
- **Method:** code/bench/gpurun -t 590 -s noisecirc a13_blocks.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --set stage_fusion=1 --set rotation_form=1 --set dtype=complex32 --set max_fused_qudits=10 --label fr:c32-w10
- **Outcome:** exit 0; outputs in data/20261024-191623-a13-block-times-fused-kernels-c32-w10
- **Next:** none
- **Refs:** data/20261024-191623-a13-block-times-fused-kernels-c32-w10, code/bench/a13_blocks.py, code/noisecirc

## 2026-10-24 19:16 UTC  A13 block times fused kernels c32-sq4
- **Goal:** Pass times at n=26 with stage fusion and rotation form (noisecirc feature/stage-fusion), setting c32-sq4
- **Task:** A13
- **Method:** code/bench/gpurun -t 590 -s noisecirc a13_blocks.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --set stage_fusion=1 --set rotation_form=1 --set dtype=complex32 --set stage_qubits=4 --label fr:c32-sq4
- **Outcome:** exit 0; outputs in data/20261024-191550-a13-block-times-fused-kernels-c32-sq4
- **Next:** none
- **Refs:** data/20261024-191550-a13-block-times-fused-kernels-c32-sq4, code/bench/a13_blocks.py, code/noisecirc

## 2026-10-24 19:15 UTC  A13 block times fused kernels w10
- **Goal:** Pass times at n=26 with stage fusion and rotation form (noisecirc feature/stage-fusion), setting w10
- **Task:** A13
- **Method:** code/bench/gpurun -t 590 -s noisecirc a13_blocks.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --set stage_fusion=1 --set rotation_form=1 --set max_fused_qudits=10 --label fr:w10
- **Outcome:** exit 0; outputs in data/20261024-191530-a13-block-times-fused-kernels-w10
- **Next:** none
- **Refs:** data/20261024-191530-a13-block-times-fused-kernels-w10, code/bench/a13_blocks.py, code/noisecirc

## 2026-10-24 19:15 UTC  A13 block times fused kernels c32
- **Goal:** Pass times at n=26 with stage fusion and rotation form (noisecirc feature/stage-fusion), setting c32
- **Task:** A13
- **Method:** code/bench/gpurun -t 590 -s noisecirc a13_blocks.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --set stage_fusion=1 --set rotation_form=1 --set dtype=complex32 --label fr:c32
- **Outcome:** exit 0; outputs in data/20261024-191510-a13-block-times-fused-kernels-c32
- **Next:** none
- **Refs:** data/20261024-191510-a13-block-times-fused-kernels-c32, code/bench/a13_blocks.py, code/noisecirc

## 2026-10-24 19:15 UTC  A13 block times fused kernels sq4-reg96
- **Goal:** Pass times at n=26 with stage fusion and rotation form (noisecirc feature/stage-fusion), setting sq4-reg96
- **Task:** A13
- **Method:** code/bench/gpurun -t 590 -s noisecirc a13_blocks.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --set stage_fusion=1 --set rotation_form=1 --set stage_qubits=4 --set min_registers=96 --label fr:sq4-reg96
- **Outcome:** exit 0; outputs in data/20261024-191438-a13-block-times-fused-kernels-sq4-reg96
- **Next:** none
- **Refs:** data/20261024-191438-a13-block-times-fused-kernels-sq4-reg96, code/bench/a13_blocks.py, code/noisecirc

## 2026-10-24 19:14 UTC  A13 block times fused kernels sq4
- **Goal:** Pass times at n=26 with stage fusion and rotation form (noisecirc feature/stage-fusion), setting sq4
- **Task:** A13
- **Method:** code/bench/gpurun -t 590 -s noisecirc a13_blocks.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --set stage_fusion=1 --set rotation_form=1 --set stage_qubits=4 --label fr:sq4
- **Outcome:** exit 0; outputs in data/20261024-191404-a13-block-times-fused-kernels-sq4
- **Next:** none
- **Refs:** data/20261024-191404-a13-block-times-fused-kernels-sq4, code/bench/a13_blocks.py, code/noisecirc

## 2026-10-24 19:14 UTC  A13 block times fused kernels base
- **Goal:** Pass times at n=26 with stage fusion and rotation form (noisecirc feature/stage-fusion), setting base
- **Task:** A13
- **Method:** code/bench/gpurun -t 590 -s noisecirc a13_blocks.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --set stage_fusion=1 --set rotation_form=1 --label fr:base
- **Outcome:** exit 0; outputs in data/20261024-191352-a13-block-times-fused-kernels-base
- **Next:** none
- **Refs:** data/20261024-191352-a13-block-times-fused-kernels-base, code/bench/a13_blocks.py, code/noisecirc

## 2026-10-24 19:13 UTC  A14 stage fusion and rotation form check n=26
- **Goal:** Correctness and pass times of in-stage fusion plus rotation form (svpass stage_fusion, rotation_form; noisecirc feature/stage-fusion) against the default kernels, A7 workloads at M=0.1
- **Task:** A14
- **Method:** code/bench/gpurun -t 590 -s noisecirc a14_check.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --variant stage_fusion=1 --variant rotation_form=1 --label fusion+rotation
- **Outcome:** exit 0; outputs in data/20261024-190951-a14-stage-fusion-and-rotation-form-check-n-26
- **Next:** none
- **Refs:** data/20261024-190951-a14-stage-fusion-and-rotation-form-check-n-26, code/bench/a14_check.py, code/noisecirc

## 2026-10-24 19:05 UTC  A14 stage fusion check n=26
- **Goal:** Correctness and pass times of in-stage fusion (svpass stage_fusion, noisecirc feature/stage-fusion) against the default kernels on every block of the A7 workloads at M=0.1
- **Task:** A14
- **Method:** code/bench/gpurun -t 590 -s noisecirc a14_check.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --variant stage_fusion=1 --label fusion
- **Outcome:** exit 0; outputs in data/20261024-190130-a14-stage-fusion-check-n-26
- **Next:** none
- **Refs:** data/20261024-190130-a14-stage-fusion-check-n-26, code/bench/a14_check.py, code/noisecirc

## 2026-10-24 19:00 UTC  A13 block times complex32 max-fused-qudits 11 max-operations 1024
- **Goal:** Pass times and static work of every block at n=26 for precision complex32, max_fused_qudits=11, max_operations=1024 (A7 workloads, damping M=0.1)
- **Task:** A13
- **Method:** code/bench/gpurun a13_blocks.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --set dtype=complex32 --set max_fused_qudits=11 --set max_operations=1024 --label complex32:11:1024
- **Outcome:** exit 0; outputs in data/20261024-190024-a13-block-times-complex32-max-fused-qudits-11-max-operations-1024
- **Next:** none
- **Refs:** data/20261024-190024-a13-block-times-complex32-max-fused-qudits-11-max-operations-1024, code/bench/a13_blocks.py

## 2026-10-24 19:00 UTC  A13 block times complex32 max-fused-qudits 11 max-operations 256
- **Goal:** Pass times and static work of every block at n=26 for precision complex32, max_fused_qudits=11, max_operations=256 (A7 workloads, damping M=0.1)
- **Task:** A13
- **Method:** code/bench/gpurun a13_blocks.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --set dtype=complex32 --set max_fused_qudits=11 --set max_operations=256 --label complex32:11:256
- **Outcome:** exit 0; outputs in data/20261024-190010-a13-block-times-complex32-max-fused-qudits-11-max-operations-256
- **Next:** none
- **Refs:** data/20261024-190010-a13-block-times-complex32-max-fused-qudits-11-max-operations-256, code/bench/a13_blocks.py

## 2026-10-24 19:00 UTC  A13 block times complex32 max-fused-qudits 11 max-operations 128
- **Goal:** Pass times and static work of every block at n=26 for precision complex32, max_fused_qudits=11, max_operations=128 (A7 workloads, damping M=0.1)
- **Task:** A13
- **Method:** code/bench/gpurun a13_blocks.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --set dtype=complex32 --set max_fused_qudits=11 --set max_operations=128 --label complex32:11:128
- **Outcome:** exit 0; outputs in data/20261024-185952-a13-block-times-complex32-max-fused-qudits-11-max-operations-128
- **Next:** none
- **Refs:** data/20261024-185952-a13-block-times-complex32-max-fused-qudits-11-max-operations-128, code/bench/a13_blocks.py

## 2026-10-24 18:59 UTC  A13 block times complex32 max-fused-qudits 11 max-operations 64
- **Goal:** Pass times and static work of every block at n=26 for precision complex32, max_fused_qudits=11, max_operations=64 (A7 workloads, damping M=0.1)
- **Task:** A13
- **Method:** code/bench/gpurun a13_blocks.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --set dtype=complex32 --set max_fused_qudits=11 --set max_operations=64 --label complex32:11:64
- **Outcome:** exit 0; outputs in data/20261024-185935-a13-block-times-complex32-max-fused-qudits-11-max-operations-64
- **Next:** none
- **Refs:** data/20261024-185935-a13-block-times-complex32-max-fused-qudits-11-max-operations-64, code/bench/a13_blocks.py

## 2026-10-24 18:59 UTC  A13 block times complex32 max-fused-qudits 10 max-operations 1024
- **Goal:** Pass times and static work of every block at n=26 for precision complex32, max_fused_qudits=10, max_operations=1024 (A7 workloads, damping M=0.1)
- **Task:** A13
- **Method:** code/bench/gpurun a13_blocks.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --set dtype=complex32 --set max_fused_qudits=10 --set max_operations=1024 --label complex32:10:1024
- **Outcome:** exit 0; outputs in data/20261024-185927-a13-block-times-complex32-max-fused-qudits-10-max-operations-1024
- **Next:** none
- **Refs:** data/20261024-185927-a13-block-times-complex32-max-fused-qudits-10-max-operations-1024, code/bench/a13_blocks.py

## 2026-10-24 18:59 UTC  A13 block times complex32 max-fused-qudits 10 max-operations 256
- **Goal:** Pass times and static work of every block at n=26 for precision complex32, max_fused_qudits=10, max_operations=256 (A7 workloads, damping M=0.1)
- **Task:** A13
- **Method:** code/bench/gpurun a13_blocks.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --set dtype=complex32 --set max_fused_qudits=10 --set max_operations=256 --label complex32:10:256
- **Outcome:** exit 0; outputs in data/20261024-185916-a13-block-times-complex32-max-fused-qudits-10-max-operations-256
- **Next:** none
- **Refs:** data/20261024-185916-a13-block-times-complex32-max-fused-qudits-10-max-operations-256, code/bench/a13_blocks.py

## 2026-10-24 18:59 UTC  A13 block times complex32 max-fused-qudits 10 max-operations 128
- **Goal:** Pass times and static work of every block at n=26 for precision complex32, max_fused_qudits=10, max_operations=128 (A7 workloads, damping M=0.1)
- **Task:** A13
- **Method:** code/bench/gpurun a13_blocks.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --set dtype=complex32 --set max_fused_qudits=10 --set max_operations=128 --label complex32:10:128
- **Outcome:** exit 0; outputs in data/20261024-185857-a13-block-times-complex32-max-fused-qudits-10-max-operations-128
- **Next:** none
- **Refs:** data/20261024-185857-a13-block-times-complex32-max-fused-qudits-10-max-operations-128, code/bench/a13_blocks.py

## 2026-10-24 18:58 UTC  A13 block times complex32 max-fused-qudits 10 max-operations 64
- **Goal:** Pass times and static work of every block at n=26 for precision complex32, max_fused_qudits=10, max_operations=64 (A7 workloads, damping M=0.1)
- **Task:** A13
- **Method:** code/bench/gpurun a13_blocks.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --set dtype=complex32 --set max_fused_qudits=10 --set max_operations=64 --label complex32:10:64
- **Outcome:** exit 0; outputs in data/20261024-185841-a13-block-times-complex32-max-fused-qudits-10-max-operations-64
- **Next:** none
- **Refs:** data/20261024-185841-a13-block-times-complex32-max-fused-qudits-10-max-operations-64, code/bench/a13_blocks.py

## 2026-10-24 18:58 UTC  A13 block times complex32 max-fused-qudits 9 max-operations 1024
- **Goal:** Pass times and static work of every block at n=26 for precision complex32, max_fused_qudits=9, max_operations=1024 (A7 workloads, damping M=0.1)
- **Task:** A13
- **Method:** code/bench/gpurun a13_blocks.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --set dtype=complex32 --set max_fused_qudits=9 --set max_operations=1024 --label complex32:9:1024
- **Outcome:** exit 0; outputs in data/20261024-185832-a13-block-times-complex32-max-fused-qudits-9-max-operations-1024
- **Next:** none
- **Refs:** data/20261024-185832-a13-block-times-complex32-max-fused-qudits-9-max-operations-1024, code/bench/a13_blocks.py

## 2026-10-24 18:58 UTC  A13 block times complex32 max-fused-qudits 9 max-operations 256
- **Goal:** Pass times and static work of every block at n=26 for precision complex32, max_fused_qudits=9, max_operations=256 (A7 workloads, damping M=0.1)
- **Task:** A13
- **Method:** code/bench/gpurun a13_blocks.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --set dtype=complex32 --set max_fused_qudits=9 --set max_operations=256 --label complex32:9:256
- **Outcome:** exit 0; outputs in data/20261024-185823-a13-block-times-complex32-max-fused-qudits-9-max-operations-256
- **Next:** none
- **Refs:** data/20261024-185823-a13-block-times-complex32-max-fused-qudits-9-max-operations-256, code/bench/a13_blocks.py

## 2026-10-24 18:58 UTC  A13 block times complex32 max-fused-qudits 9 max-operations 128
- **Goal:** Pass times and static work of every block at n=26 for precision complex32, max_fused_qudits=9, max_operations=128 (A7 workloads, damping M=0.1)
- **Task:** A13
- **Method:** code/bench/gpurun a13_blocks.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --set dtype=complex32 --set max_fused_qudits=9 --set max_operations=128 --label complex32:9:128
- **Outcome:** exit 0; outputs in data/20261024-185808-a13-block-times-complex32-max-fused-qudits-9-max-operations-128
- **Next:** none
- **Refs:** data/20261024-185808-a13-block-times-complex32-max-fused-qudits-9-max-operations-128, code/bench/a13_blocks.py

## 2026-10-24 18:58 UTC  A13 block times complex32 max-fused-qudits 9 max-operations 64
- **Goal:** Pass times and static work of every block at n=26 for precision complex32, max_fused_qudits=9, max_operations=64 (A7 workloads, damping M=0.1)
- **Task:** A13
- **Method:** code/bench/gpurun a13_blocks.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --set dtype=complex32 --set max_fused_qudits=9 --set max_operations=64 --label complex32:9:64
- **Outcome:** exit 0; outputs in data/20261024-185751-a13-block-times-complex32-max-fused-qudits-9-max-operations-64
- **Next:** none
- **Refs:** data/20261024-185751-a13-block-times-complex32-max-fused-qudits-9-max-operations-64, code/bench/a13_blocks.py

## 2026-10-24 18:57 UTC  A13 block times complex64 max-fused-qudits 11 max-operations 1024
- **Goal:** Pass times and static work of every block at n=26 for precision complex64, max_fused_qudits=11, max_operations=1024 (A7 workloads, damping M=0.1)
- **Task:** A13
- **Method:** code/bench/gpurun a13_blocks.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --set dtype=complex64 --set max_fused_qudits=11 --set max_operations=1024 --label complex64:11:1024
- **Outcome:** exit 0; outputs in data/20261024-185743-a13-block-times-complex64-max-fused-qudits-11-max-operations-1024
- **Next:** none
- **Refs:** data/20261024-185743-a13-block-times-complex64-max-fused-qudits-11-max-operations-1024, code/bench/a13_blocks.py

## 2026-10-24 18:57 UTC  A13 block times complex64 max-fused-qudits 11 max-operations 256
- **Goal:** Pass times and static work of every block at n=26 for precision complex64, max_fused_qudits=11, max_operations=256 (A7 workloads, damping M=0.1)
- **Task:** A13
- **Method:** code/bench/gpurun a13_blocks.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --set dtype=complex64 --set max_fused_qudits=11 --set max_operations=256 --label complex64:11:256
- **Outcome:** exit 0; outputs in data/20261024-185728-a13-block-times-complex64-max-fused-qudits-11-max-operations-256
- **Next:** none
- **Refs:** data/20261024-185728-a13-block-times-complex64-max-fused-qudits-11-max-operations-256, code/bench/a13_blocks.py

## 2026-10-24 18:57 UTC  A13 block times complex64 max-fused-qudits 11 max-operations 128
- **Goal:** Pass times and static work of every block at n=26 for precision complex64, max_fused_qudits=11, max_operations=128 (A7 workloads, damping M=0.1)
- **Task:** A13
- **Method:** code/bench/gpurun a13_blocks.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --set dtype=complex64 --set max_fused_qudits=11 --set max_operations=128 --label complex64:11:128
- **Outcome:** exit 0; outputs in data/20261024-185709-a13-block-times-complex64-max-fused-qudits-11-max-operations-128
- **Next:** none
- **Refs:** data/20261024-185709-a13-block-times-complex64-max-fused-qudits-11-max-operations-128, code/bench/a13_blocks.py

## 2026-10-24 18:57 UTC  A13 block times complex64 max-fused-qudits 11 max-operations 64
- **Goal:** Pass times and static work of every block at n=26 for precision complex64, max_fused_qudits=11, max_operations=64 (A7 workloads, damping M=0.1)
- **Task:** A13
- **Method:** code/bench/gpurun a13_blocks.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --set dtype=complex64 --set max_fused_qudits=11 --set max_operations=64 --label complex64:11:64
- **Outcome:** exit 0; outputs in data/20261024-185652-a13-block-times-complex64-max-fused-qudits-11-max-operations-64
- **Next:** none
- **Refs:** data/20261024-185652-a13-block-times-complex64-max-fused-qudits-11-max-operations-64, code/bench/a13_blocks.py

## 2026-10-24 18:56 UTC  A13 block times complex64 max-fused-qudits 10 max-operations 1024
- **Goal:** Pass times and static work of every block at n=26 for precision complex64, max_fused_qudits=10, max_operations=1024 (A7 workloads, damping M=0.1)
- **Task:** A13
- **Method:** code/bench/gpurun a13_blocks.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --set dtype=complex64 --set max_fused_qudits=10 --set max_operations=1024 --label complex64:10:1024
- **Outcome:** exit 0; outputs in data/20261024-185644-a13-block-times-complex64-max-fused-qudits-10-max-operations-1024
- **Next:** none
- **Refs:** data/20261024-185644-a13-block-times-complex64-max-fused-qudits-10-max-operations-1024, code/bench/a13_blocks.py

## 2026-10-24 18:56 UTC  A13 block times complex64 max-fused-qudits 10 max-operations 256
- **Goal:** Pass times and static work of every block at n=26 for precision complex64, max_fused_qudits=10, max_operations=256 (A7 workloads, damping M=0.1)
- **Task:** A13
- **Method:** code/bench/gpurun a13_blocks.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --set dtype=complex64 --set max_fused_qudits=10 --set max_operations=256 --label complex64:10:256
- **Outcome:** exit 0; outputs in data/20261024-185633-a13-block-times-complex64-max-fused-qudits-10-max-operations-256
- **Next:** none
- **Refs:** data/20261024-185633-a13-block-times-complex64-max-fused-qudits-10-max-operations-256, code/bench/a13_blocks.py

## 2026-10-24 18:56 UTC  A13 block times complex64 max-fused-qudits 10 max-operations 128
- **Goal:** Pass times and static work of every block at n=26 for precision complex64, max_fused_qudits=10, max_operations=128 (A7 workloads, damping M=0.1)
- **Task:** A13
- **Method:** code/bench/gpurun a13_blocks.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --set dtype=complex64 --set max_fused_qudits=10 --set max_operations=128 --label complex64:10:128
- **Outcome:** exit 0; outputs in data/20261024-185614-a13-block-times-complex64-max-fused-qudits-10-max-operations-128
- **Next:** none
- **Refs:** data/20261024-185614-a13-block-times-complex64-max-fused-qudits-10-max-operations-128, code/bench/a13_blocks.py

## 2026-10-24 18:56 UTC  A13 block times complex64 max-fused-qudits 10 max-operations 64
- **Goal:** Pass times and static work of every block at n=26 for precision complex64, max_fused_qudits=10, max_operations=64 (A7 workloads, damping M=0.1)
- **Task:** A13
- **Method:** code/bench/gpurun a13_blocks.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --set dtype=complex64 --set max_fused_qudits=10 --set max_operations=64 --label complex64:10:64
- **Outcome:** exit 0; outputs in data/20261024-185558-a13-block-times-complex64-max-fused-qudits-10-max-operations-64
- **Next:** none
- **Refs:** data/20261024-185558-a13-block-times-complex64-max-fused-qudits-10-max-operations-64, code/bench/a13_blocks.py

## 2026-10-24 18:55 UTC  A13 block times complex64 max-fused-qudits 9 max-operations 1024
- **Goal:** Pass times and static work of every block at n=26 for precision complex64, max_fused_qudits=9, max_operations=1024 (A7 workloads, damping M=0.1)
- **Task:** A13
- **Method:** code/bench/gpurun a13_blocks.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --set dtype=complex64 --set max_fused_qudits=9 --set max_operations=1024 --label complex64:9:1024
- **Outcome:** exit 0; outputs in data/20261024-185550-a13-block-times-complex64-max-fused-qudits-9-max-operations-1024
- **Next:** none
- **Refs:** data/20261024-185550-a13-block-times-complex64-max-fused-qudits-9-max-operations-1024, code/bench/a13_blocks.py

## 2026-10-24 18:55 UTC  A13 block times complex64 max-fused-qudits 9 max-operations 256
- **Goal:** Pass times and static work of every block at n=26 for precision complex64, max_fused_qudits=9, max_operations=256 (A7 workloads, damping M=0.1)
- **Task:** A13
- **Method:** code/bench/gpurun a13_blocks.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --set dtype=complex64 --set max_fused_qudits=9 --set max_operations=256 --label complex64:9:256
- **Outcome:** exit 0; outputs in data/20261024-185541-a13-block-times-complex64-max-fused-qudits-9-max-operations-256
- **Next:** none
- **Refs:** data/20261024-185541-a13-block-times-complex64-max-fused-qudits-9-max-operations-256, code/bench/a13_blocks.py

## 2026-10-24 18:55 UTC  A13 block times complex64 max-fused-qudits 9 max-operations 128
- **Goal:** Pass times and static work of every block at n=26 for precision complex64, max_fused_qudits=9, max_operations=128 (A7 workloads, damping M=0.1)
- **Task:** A13
- **Method:** code/bench/gpurun a13_blocks.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --set dtype=complex64 --set max_fused_qudits=9 --set max_operations=128 --label complex64:9:128
- **Outcome:** exit 0; outputs in data/20261024-185533-a13-block-times-complex64-max-fused-qudits-9-max-operations-128
- **Next:** none
- **Refs:** data/20261024-185533-a13-block-times-complex64-max-fused-qudits-9-max-operations-128, code/bench/a13_blocks.py

## 2026-10-24 18:55 UTC  A13 block times complex64 max-fused-qudits 9 max-operations 64
- **Goal:** Pass times and static work of every block at n=26 for precision complex64, max_fused_qudits=9, max_operations=64 (A7 workloads, damping M=0.1)
- **Task:** A13
- **Method:** code/bench/gpurun a13_blocks.py --workloads ghz:damping:0.0019802,brickwork:damping:0.000280112,qft:damping:0.0002849,qaoa:damping:0.000512821,grid:damping:0.00017094 --qubits 26 --set dtype=complex64 --set max_fused_qudits=9 --set max_operations=64 --label complex64:9:64
- **Outcome:** exit 0; outputs in data/20261024-185525-a13-block-times-complex64-max-fused-qudits-9-max-operations-64
- **Next:** none
- **Refs:** data/20261024-185525-a13-block-times-complex64-max-fused-qudits-9-max-operations-64, code/bench/a13_blocks.py

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
