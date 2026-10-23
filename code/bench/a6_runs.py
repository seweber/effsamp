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
    def __init__(self, qc: QuantumCircuit, kind: str | None, p: float, mode: str) -> None:
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

    def run(self, shots: int, seed: int) -> None:
        result = self.sim.run(self.circuit, shots=shots, seed_simulator=seed).result()
        if not result.success:
            raise RuntimeError(str(result.status))
        meta = result.results[0].metadata
        self.metadata = {k: meta.get(k) for k in ("fusion", "batched_shots_optimization", "shot_branching_enabled",
                                                   "runtime_parameter_bind", "num_bind_params", "cuStateVec_enable")}
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


def make(sim: str, qc, kind, p):
    if sim.startswith("aer_"):
        return Aer(qc, kind, p, sim.removeprefix("aer_"))
    if sim == "cudaq":
        return Cudaq(qc, kind, p)
    raise ValueError(sim)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sim", required=True)
    parser.add_argument("--circuit", default="brickwork")
    parser.add_argument("--qubits", type=int, default=24)
    parser.add_argument("--noise", default="damping")
    parser.add_argument("--p", type=float, default=1e-3)
    parser.add_argument("--shots", type=int, default=1000)
    parser.add_argument("--reps", type=int, default=2)
    args = parser.parse_args()
    kind = None if args.noise == "none" else args.noise
    qc = circuits.make(args.circuit, args.qubits)
    meta = {"sim": args.sim, "circuit": args.circuit, "n": args.qubits, "noise": args.noise, "p": args.p,
            "shots": args.shots, "gates": len(qc.data), "channels": circuits.channels(qc)}
    try:
        sim = make(args.sim, qc, kind, args.p)
        start = time.perf_counter()
        sim.run(args.shots, 0)
        t_first = time.perf_counter() - start
        reps = args.reps if t_first < 100 else 0
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
