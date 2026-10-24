"""A15: block passes when noise channels followed only by diagonal gates become classical readout noise (dry run).

The tail of a circuit is the set of diagonal gates all of whose qubits see only tail gates afterwards
(found backwards). On the tail, the Z-basis populations evolve classically: diagonal gates leave them
unchanged and their phases cannot reach a later non-diagonal gate, and amplitude damping maps them by
the stochastic matrix 1 -> 0 with probability gamma whatever the coherences (phase covariance). A
channel on qubit q all of whose later operations on q are tail gates or channels can therefore be
removed from the simulation and applied to the sampled bits instead, exactly. A channel followed by a
diagonal gate whose partner later meets a non-diagonal gate cannot: the controlled phase then depends
on whether q decayed. This script makes those gate instances carry no noise on the affected targets (gate maps
with noise on a subset of targets) and compares the dry-run passes with the unchanged circuit.

Usage: a15_readout.py (local, CPU; damping, n = 28, 1000 shots, M = 0.1 and 1 of the full circuit)
"""
import json
import sys
from itertools import product
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import circuits  # noqa: E402
import dryrun  # noqa: E402
import noise  # noqa: E402
from qiskit import QuantumCircuit  # noqa: E402
from qiskit.circuit import Gate  # noqa: E402

DIAGONAL = {"rz", "cp", "p", "cz", "mcphase"}


def masked_maps(p: float) -> dict:
    """noise.maps("damping", p) plus maps '<gate>_m<mask>' with noise only on the targets in ``mask``."""
    import qutip as qt

    from noisecirc.maps import DEFAULT_MAPS, QuantumMap, qubit_restricted_maps

    maps = dict(noise.maps("damping", p))
    ideal = qubit_restricted_maps(DEFAULT_MAPS)
    damp = [qt.Qobj(np.asarray(k, dtype=complex)) for k in noise.kraus("damping", p)]
    eye = [qt.qeye(2)]
    for name, ideal_map in ideal.items():
        width = ideal_map.num_qudits
        if width > 2:
            continue
        for mask in range(1 << width):
            # Qubit j of the gate is target j, which is the j-th factor of the tensor product (checked).
            per_target = [damp if mask >> j & 1 else eye for j in range(width)]
            ops = [qt.tensor(list(c)) if width > 1 else c[0] for c in product(*per_target)]

            def channel(*params, ideal_map=ideal_map, ops=ops):
                unitary = ideal_map.channel(params)
                return [op @ unitary for op in ops]

            maps[f"{name}_m{mask}"] = QuantumMap(width, channel, branches=ideal_map.branches, tol=ideal_map.tol)
    return maps


def readout_circuit(qc: QuantumCircuit) -> tuple[QuantumCircuit, int, int]:
    """Return the circuit with tail channels removed (renamed gates) and the numbers of channels removed and kept."""
    ops = [(ci.operation, [qc.find_bit(q).index for q in ci.qubits]) for ci in qc.data]
    tail = [True] * qc.num_qubits  # every later operation on the qubit is a tail gate or a channel
    masks = []
    for op, qs in reversed(ops):
        # The channels after this gate: removable on the qubits whose later operations are all tail.
        masks.append(sum(1 << j for j, q in enumerate(qs) if not tail[q]))
        in_tail = op.name in DIAGONAL and all(tail[q] for q in qs)
        if not in_tail:
            for q in qs:
                tail[q] = False
    masks.reverse()
    out = QuantumCircuit(qc.num_qubits)
    removed = kept = 0
    for (op, qs), mask in zip(ops, masks):
        width = len(qs)
        removed += width - bin(mask).count("1")
        kept += bin(mask).count("1")
        out.append(Gate(f"{op.name}_m{mask}", width, list(op.params)), qs)
    return out, removed, kept


def main() -> None:
    for name in ["ghz", "brickwork", "qft", "qaoa", "grid"]:
        qc = circuits.make(name, 28)
        c = circuits.channels(qc)
        modified, removed, kept = readout_circuit(qc)
        for load in (0.1, 1.0):
            p = 2 * load / c
            maps = masked_maps(p)
            runs_a = [dryrun.predict(qc, maps, 1000, seed=s) for s in (1, 2, 3)]
            runs_b = [dryrun.predict(modified, maps, 1000, seed=s) for s in (1, 2, 3)]
            a = float(np.mean([r["block_passes"] for r in runs_a]))
            b = float(np.mean([r["block_passes"] for r in runs_b]))
            print(json.dumps({"circuit": name, "load": load, "p": p, "channels_removed": removed, "channels_kept": kept,
                              "passes": a, "passes_readout": b, "gain": a / b,
                              "blocks": runs_a[0]["blocks"], "blocks_readout": runs_b[0]["blocks"]}), flush=True)


if __name__ == "__main__":
    main()
