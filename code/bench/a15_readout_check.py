"""A15: exactness check of the readout map (a15_readout.py) on small registers, by density matrices.

For each circuit: the exact measurement distribution with damping after every gate, against the
distribution of the circuit whose tail channels are removed, followed by the classical map of the
removed channels (each removed channel on qubit q flips a sampled 1 to 0 with probability gamma; on
the tail, the order of these maps does not matter, they act on q's bit only). Prints the total
variation distance, which must be at rounding level; and, as a control, the distance when the naive
criterion (later gates on q diagonal, partners ignored) is used.
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import circuits  # noqa: E402
import noise  # noqa: E402
from a15_firstjump_ref import exact  # noqa: E402
from a15_readout import DIAGONAL, masked_maps, readout_circuit  # noqa: E402
from dryrun import compile_like_simulator  # noqa: E402

from noisecirc import Simulator  # noqa: E402


def naive_circuit(qc):
    from qiskit import QuantumCircuit
    from qiskit.circuit import Gate

    ops = [(ci.operation, [qc.find_bit(q).index for q in ci.qubits]) for ci in qc.data]
    tail = [True] * qc.num_qubits
    masks = []
    for op, qs in reversed(ops):
        masks.append(sum(1 << j for j, q in enumerate(qs) if not tail[q]))
        if op.name not in DIAGONAL:
            for q in qs:
                tail[q] = False
    masks.reverse()
    out = QuantumCircuit(qc.num_qubits)
    removed = 0
    for (op, qs), mask in zip(ops, masks):
        removed += len(qs) - bin(mask).count("1")
        out.append(Gate(f"{op.name}_m{mask}", len(qs), list(op.params)), qs)
    return out, removed, 0


def removed_per_qubit(qc, modified, n):
    counts = np.zeros(n, dtype=int)
    for a, b in zip(qc.data, modified.data):
        qs = [qc.find_bit(q).index for q in a.qubits]
        mask = int(b.operation.name.rsplit("_m", 1)[1])
        for j, q in enumerate(qs):
            if not mask >> j & 1:
                counts[q] += 1
    return counts


def classical(dist, counts, gamma, n):
    for q in range(n):
        keep = (1 - gamma) ** counts[q]
        new = dist.copy()
        for x in range(2**n):
            if x >> q & 1:
                new[x] -= (1 - keep) * dist[x]
                new[x ^ (1 << q)] += (1 - keep) * dist[x]
        dist = new
    return dist


n, p = 6, 0.15
for name in ("ghz", "qft", "brickwork", "qaoa"):
    qc = circuits.make(name, n)
    maps = masked_maps(p)
    blocks = lambda c: compile_like_simulator(c, Simulator(maps=maps, max_fused_qudits=2))[0].blocks  # noqa: E731
    ref = exact(blocks(qc), n)
    for label, make in (("tail", readout_circuit), ("naive", naive_circuit)):
        modified, removed, _ = make(qc)
        dist = classical(exact(blocks(modified), n), removed_per_qubit(qc, modified, n), p, n)
        print(f"{name:10s} {label:5s} removed {removed:3d} tvd {0.5 * np.abs(dist - ref).sum():.2e}", flush=True)
