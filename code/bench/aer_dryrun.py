"""A6: Qiskit Aer's work on a noisy circuit, counted in passes over the state vector, without a GPU.

Aer (0.17/0.18, state vector) fuses a noisy circuit's gates and channels into Kraus operations of at
most 2 qubits (`fusion_verbose` lists them; the local CPU build fuses like the GPU build). It then
applies a Kraus operation K_0..K_{m-1} as `apply_kraus` in its source does
(`statevector_executor.hpp`, `statevector_state.hpp`):

- **plain** (one trajectory per shot): for j = 0, 1, ..., it computes ||K_j psi||^2, a reduction over
  the state vector (a read: half a pass), until the cumulative probability exceeds the shot's random
  number, then applies the chosen K_j / sqrt(p_j) (a read and a write: one pass);
- **shot branching**: for each branch, it computes the norms until the cumulative probability exceeds
  the largest random number of the branch's shots (at most m - 1 of them), splits the branch into one
  branch per operator that received shots (a new branch is a copy of the state: one pass), and
  applies each branch's operator (one pass).

The probabilities come from the same surrogate as `dryrun.py`: each qubit's state is followed as a
pure single-qubit state from |0> under the dominant operator until an operation entangles it, and is
maximally mixed after. The branches' shot counts are drawn multinomially, the largest random number of
s shots from Beta(s, 1). Counted here: norm reads, applies and copies; not counted: the initial state
and the final measurement (one pass per trajectory or branch each).

Usage as a library: ``count(circuit, kind, p, shots, mode)``.
"""

from __future__ import annotations

import numpy as np
from qiskit import QuantumCircuit, transpile

import noise


def fused_operations(circuit: QuantumCircuit, kind: str, p: float) -> list[tuple[list[int], list[np.ndarray]]]:
    """Aer's fused operations of ``circuit`` with noise ``kind`` after every gate: (qubits, Kraus matrices)."""
    from qiskit_aer import AerSimulator
    from qiskit_aer.noise import NoiseModel, kraus_error

    model = NoiseModel(basis_gates=["r", "rz", "cp"])
    error = kraus_error([np.asarray(k, dtype=complex) for k in noise.kraus(kind, p)])
    model.add_all_qubit_quantum_error(error, ["r", "rz"])
    model.add_all_qubit_quantum_error(error.tensor(error), ["cp"])
    sim = AerSimulator(method="statevector", precision="single", noise_model=model, fusion_verbose=True)
    measured = circuit.copy()
    measured.measure_all()
    compiled = transpile(measured, sim, optimization_level=0)
    ops = sim.run(compiled, shots=1, seed_simulator=0).result().results[0].metadata["fusion"]["output_ops"]
    out = []
    for op in ops:
        if op["name"] == "measure":
            continue
        mats = [np.array(m) for m in op.get("mats", [])]
        mats = [m[..., 0] + 1j * m[..., 1] if m.ndim == 3 else m for m in mats]
        out.append((list(op["qubits"]), mats))
    return out


def _probabilities(ops, n: int) -> list[np.ndarray]:
    """Each operation's Kraus probabilities under the tracking surrogate, in Aer's order."""
    pure: dict[int, np.ndarray | None] = {q: np.array([1.0, 0.0], dtype=complex) for q in range(n)}
    probs = []
    for qubits, mats in ops:
        states = [pure[q] for q in qubits]
        # Aer's matrices index qubit qubits[0] as the least significant bit.
        rho = np.array([[1.0 + 0j]])
        for s in states:
            local = np.eye(2) / 2 if s is None else np.outer(s, s.conj())
            rho = np.kron(local, rho)
        pk = np.array([np.trace(m.conj().T @ m @ rho).real for m in mats])
        pk = np.clip(pk, 0, None)
        pk = pk / pk.sum()
        probs.append(pk)
        if any(s is None for s in states):
            for q in qubits:
                pure[q] = None
            continue
        psi = np.array([1.0 + 0j])
        for s in states:
            psi = np.kron(s, psi)
        out = mats[int(np.argmax(pk))] @ psi
        out /= np.linalg.norm(out)
        w = len(qubits)
        tensor = out.reshape([2] * w)
        for j, q in enumerate(qubits):
            moved = np.moveaxis(tensor, w - 1 - j, 0).reshape(2, -1)
            vals, vecs = np.linalg.eigh(moved @ moved.conj().T)
            pure[q] = vecs[:, -1] if vals[-1] > 1 - 1e-9 else None
    return probs


def count(circuit: QuantumCircuit, kind: str, p: float, shots: int, mode: str, seed: int = 0) -> dict[str, float]:
    """Aer's norm reads, applies and copies for ``shots`` shots in ``mode`` ("plain" or "branch")."""
    rng = np.random.default_rng(seed)
    ops = fused_operations(circuit, kind, p)
    probs = _probabilities(ops, circuit.num_qubits)
    reads = applies = copies = 0.0
    peak = 1
    if mode == "plain":
        for pk in probs:
            cum = np.cumsum(pk)[:-1]
            r = rng.random(shots)
            # norms computed: until the cumulative probability exceeds r, at most m - 1
            k = np.minimum(np.searchsorted(cum, r, side="right") + 1, len(pk) - 1) if len(pk) > 1 else np.zeros(shots)
            reads += float(np.sum(k))
            applies += shots
    else:
        branches = np.array([shots])
        for pk in probs:
            cum = np.cumsum(pk)[:-1]
            new = []
            for s in branches.tolist():
                if len(pk) > 1:
                    u = rng.random() ** (1.0 / s)  # the largest of s uniforms
                    reads += min(int(np.searchsorted(cum, u, side="right")) + 1, len(pk) - 1)
                children = rng.multinomial(s, pk)
                children = children[children > 0]
                applies += children.size
                copies += children.size - 1
                new.extend(children.tolist())
            branches = np.array(new)
            peak = max(peak, branches.size)
    return {"ops": len(ops), "kraus_matrices": sum(len(m) for _, m in ops), "reads": reads, "applies": applies,
            "copies": copies, "passes": 0.5 * reads + applies + copies, "peak_branches": peak}
