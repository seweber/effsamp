"""A6: time competing GPU state-vector simulators on the noisy benchmark circuits.

Simulators (single precision, GPU 0):

- ``aer_branch``: Qiskit Aer, state vector on the GPU, shot branching (and branching sampling).
- ``aer_batched``: Qiskit Aer, batched shots on the GPU (``batched_shots_gpu``), no branching.
- ``aer_plain``: Qiskit Aer, one trajectory per shot, one after another.
- ``cudaq``: CUDA-Q, target ``nvidia`` (cuStateVec), ``fp32``, its trajectory simulation.

The noise is the same as NoiseCirc's maps of `noise.py`: after every gate a single-qubit channel
on each of its targets (a k-qubit gate gets the k-fold tensor product). A first run is untimed
(compilation, allocation); ``--reps`` runs are then timed. Prints one JSON line per timed run,
or a ``failed`` line with the error.
"""

import argparse
import json
import sys
import time
import traceback

import numpy as np
from qiskit import QuantumCircuit, transpile

sys.path.insert(0, "/work/bench")
import circuits  # noqa: E402
import noise  # noqa: E402


class Aer:
    def __init__(self, qc: QuantumCircuit, kind: str | None, p: float, mode: str, extra: dict | None = None) -> None:
        from qiskit_aer import AerSimulator
        from qiskit_aer.noise import NoiseModel, kraus_error

        model = None
        if kind is not None and p > 0:
            model = NoiseModel(basis_gates=["r", "rz", "cp"])
            error = kraus_error([np.asarray(k, dtype=complex) for k in noise.kraus(kind, p)])
            model.add_all_qubit_quantum_error(error, ["r", "rz"])
            model.add_all_qubit_quantum_error(error.tensor(error), ["cp"])
        self.sim = AerSimulator(
            method="statevector", device="GPU", precision="single", noise_model=model,
            shot_branching_enable=mode == "branch", shot_branching_sampling_enable=mode == "branch",
            batched_shots_gpu=mode == "batched",
        )
        measured = qc.copy()
        measured.measure_all()
        self.circuit = transpile(measured, self.sim, optimization_level=0)
        self.metadata = {}
        # Aer's fusion of Kraus operators fails on some noisy circuits in an eigendecomposition
        # ("heevx", a known Aer bug, see noisecirc's benchmarks/_aer_worker.py); those run without it.
        from qiskit_aer.backends import aer_compiler

        aer_compiler.BACKEND_RUN_ARG_TYPES.setdefault("fusion_allow_kraus", (bool, np.bool_))
        # A11: further Aer options go in as run options (not all are constructor options, e.g. the
        # fusion cost factor); they are registered with Aer's run-argument types like the one above.
        for key, value in (extra or {}).items():
            aer_compiler.BACKEND_RUN_ARG_TYPES.setdefault(key, (type(value),))
        self.extra = dict(extra or {})
        self.options = {}
        trial = self.sim.run(self.circuit, shots=1, seed_simulator=0, fusion_verbose=True, **self.extra).result()
        if not trial.success and "heevx" in str(trial.status):
            self.options = {"fusion_allow_kraus": False}
            trial = self.sim.run(self.circuit, shots=1, seed_simulator=0, fusion_verbose=True, **self.extra,
                                 **self.options).result()
        fusion = trial.results[0].metadata.get("fusion", {})
        ops = [o for o in fusion.get("output_ops", []) if o.get("name") != "measure"]
        self.fused = {"method": fusion.get("method"), "max_fused_qubits": fusion.get("max_fused_qubits"),
                      "cost_factor": fusion.get("cost_factor"), "ops": len(ops), "kraus_ops": sum(o.get("name") == "kraus" for o in ops),
                      "kraus_matrices": sum(len(o.get("mats", [])) for o in ops if o.get("name") == "kraus"),
                      "max_qubits": max((len(o.get("qubits", [])) for o in ops), default=0)}

    def run(self, shots: int, seed: int) -> None:
        result = self.sim.run(self.circuit, shots=shots, seed_simulator=seed, **self.extra, **self.options).result()
        if not result.success and "heevx" in str(result.status) and not self.options:
            self.options = {"fusion_allow_kraus": False}
            result = self.sim.run(self.circuit, shots=shots, seed_simulator=seed, **self.extra, **self.options).result()
        if not result.success:
            raise RuntimeError(str(result.status))
        meta = result.results[0].metadata
        self.metadata = {k: meta.get(k) for k in ("batched_shots_optimization", "shot_branching_enabled",
                                                   "cuStateVec_enable", "max_memory_mb", "gpu_parallel_shots_")}
        self.metadata["fused"] = self.fused
        self.metadata["fusion_allow_kraus"] = not self.options
        result.get_counts()


class Cudaq:
    def __init__(self, qc: QuantumCircuit, kind: str | None, p: float) -> None:
        import cudaq

        self.cudaq = cudaq
        cudaq.set_target("nvidia", option="fp32")
        self.kernel = cudaq.make_kernel()
        q = self.kernel.qalloc(qc.num_qubits)
        for instruction in qc.data:
            t = [qc.find_bit(x).index for x in instruction.qubits]
            params = [float(v) for v in instruction.operation.params]
            name = instruction.operation.name
            if name == "r":
                self.kernel.u3(params[0], params[1] - np.pi / 2, np.pi / 2 - params[1], q[t[0]])
            elif name == "rz":
                self.kernel.rz(params[0], q[t[0]])
            elif name == "cp":
                self.kernel.cr1(params[0], q[t[0]], q[t[1]])
            else:
                raise ValueError(name)
        self.model = None
        if kind is not None and p > 0:
            ops = [np.asarray(k, dtype=np.complex128) for k in noise.kraus(kind, p)]
            two = [np.kron(a, b) for a in ops for b in ops]
            self.model = cudaq.NoiseModel()
            self.model.add_all_qubit_channel("u3", cudaq.KrausChannel(ops))
            self.model.add_all_qubit_channel("rz", cudaq.KrausChannel(ops))
            self.model.add_all_qubit_channel("r1", cudaq.KrausChannel(two), num_controls=1)
        self.metadata = {}

    def run(self, shots: int, seed: int) -> None:
        self.cudaq.set_random_seed(seed)
        if self.model is None:
            self.cudaq.sample(self.kernel, shots_count=shots)
        else:
            self.cudaq.sample(self.kernel, shots_count=shots, noise_model=self.model)


def make(sim: str, qc, kind, p, extra=None):
    if sim.startswith("aer_"):
        return Aer(qc, kind, p, sim.removeprefix("aer_"), extra)
    if sim == "cudaq":
        return Cudaq(qc, kind, p)
    raise ValueError(sim)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sim", required=True)
    parser.add_argument("--circuit", default="brickwork")
    parser.add_argument("--qubits", type=int, default=24)
    parser.add_argument("--noise", default="damping")
    parser.add_argument("--ps", default="0.001")
    parser.add_argument("--shots", type=int, default=1000)
    parser.add_argument("--reps", type=int, default=2)
    parser.add_argument("--aer-option", action="append", default=[],
                        help="key=value passed to AerSimulator (A11), e.g. fusion_max_qubit=3; repeatable")
    parser.add_argument("--budget", type=float, default=450.0, help="seconds after which no new point starts")
    args = parser.parse_args()
    kind = None if args.noise == "none" else args.noise
    qc = circuits.make(args.circuit, args.qubits)
    begin = time.perf_counter()
    for p in [float(x) for x in args.ps.split(",")]:
        if time.perf_counter() - begin > args.budget:
            print(json.dumps({"kind": "skipped", "sim": args.sim, "circuit": args.circuit, "n": args.qubits, "p": p}))
            continue
        run_point(args, qc, kind, p)


def _value(text: str):
    """An option value from the command line: bool, int, float or string."""
    if text in ("True", "False"):
        return text == "True"
    for cast in (int, float):
        try:
            return cast(text)
        except ValueError:
            pass
    return text


def run_point(args, qc, kind, p) -> None:
    meta = {"sim": args.sim, "circuit": args.circuit, "n": args.qubits, "noise": args.noise, "p": p,
            "shots": args.shots, "gates": len(qc.data), "channels": circuits.channels(qc)}
    extra = {k: _value(v) for k, v in (o.split("=", 1) for o in args.aer_option)}
    if extra:
        meta["aer_options"] = extra
    try:
        sim = make(args.sim, qc, kind, p, extra)
        start = time.perf_counter()
        sim.run(args.shots, 0)
        t_first = time.perf_counter() - start
        reps = args.reps if t_first < 60 else 0
        if reps == 0:
            print(json.dumps({"kind": "run", **meta, "seed": 0, "time": t_first, "t_first": t_first,
                              "first_only": True, "metadata": sim.metadata}, default=str), flush=True)
        for seed in range(1, reps + 1):
            start = time.perf_counter()
            sim.run(args.shots, seed * args.shots)
            elapsed = time.perf_counter() - start
            print(json.dumps({"kind": "run", **meta, "seed": seed, "time": elapsed, "t_first": t_first,
                              "metadata": sim.metadata}, default=str), flush=True)
    except Exception as error:  # noqa: BLE001
        print(json.dumps({"kind": "failed", **meta, "error": repr(error)[:500],
                          "trace": traceback.format_exc()[-1500:]}), flush=True)


if __name__ == "__main__":
    main()
