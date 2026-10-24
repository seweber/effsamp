"""Qubit noise models as NoiseCirc maps: every gate followed by a single-qubit channel on each target.

All maps act on plain qubits (`noisecirc.twirling.QUBIT_BRANCHES`, PLAN.md: qubits only), built from
`noisecirc.maps.qubit_restricted_maps`. A channel is given by its single-qubit Kraus operators; a
k-qubit gate gets their k-fold tensor products after its unitary.

Channels (``p`` is the strength):

- ``damping``: amplitude damping |1> -> |0> (T1), not mixed-unitary.
- ``gad``: generalized amplitude damping at excited-state population 0.2 (finite temperature), not
  mixed-unitary.
- ``thermal``: amplitude damping ``p`` followed by pure dephasing ``p`` (a T1/T2 pair), not mixed-unitary.
- ``dephasing``: phase damping, mixed-unitary (equals a random Z), included for completeness.
- ``depolarizing``: random X, Y, Z of total probability ``p``, mixed-unitary.
- ``damp_depol``: amplitude damping ``p`` followed by depolarizing ``p``, not mixed-unitary (A12).
"""

from functools import cache
from itertools import product

import numpy as np


def kraus(kind: str, p: float) -> list[np.ndarray]:
    """Return the single-qubit Kraus operators of channel ``kind`` at strength ``p``."""
    if kind == "damping":
        return [np.array([[1, 0], [0, np.sqrt(1 - p)]]), np.array([[0, np.sqrt(p)], [0, 0]])]
    if kind == "gad":
        n = 0.2  # excited-state population of the bath
        a = np.sqrt(1 - n)
        b = np.sqrt(n)
        return [
            a * np.array([[1, 0], [0, np.sqrt(1 - p)]]),
            a * np.array([[0, np.sqrt(p)], [0, 0]]),
            b * np.array([[np.sqrt(1 - p), 0], [0, 1]]),
            b * np.array([[0, 0], [np.sqrt(p), 0]]),
        ]
    if kind == "thermal":
        damp = kraus("damping", p)
        deph = kraus("dephasing", p)
        return [d @ a for d, a in product(deph, damp)]
    if kind == "dephasing":
        return [np.array([[1, 0], [0, np.sqrt(1 - p)]]), np.array([[0, 0], [0, np.sqrt(p)]])]
    if kind == "depolarizing":
        x = np.array([[0, 1], [1, 0]])
        y = np.array([[0, -1j], [1j, 0]])
        z = np.diag([1, -1])
        return [np.sqrt(1 - p) * np.eye(2), *(np.sqrt(p / 3) * m for m in (x, y, z))]
    if kind == "damp_depol":
        return [d @ a for d, a in product(kraus("depolarizing", p), kraus("damping", p))]
    raise ValueError(f"unknown noise {kind!r}")


@cache
def maps(kind: str | None, p: float = 0.0) -> dict:
    """Return qubit maps of the default gates, each followed by noise ``kind`` on every target; ideal for None."""
    # Imported here, so that `kraus` works without noisecirc (e.g. in the cuStateVec environment of A9).
    import qutip as qt

    from noisecirc.maps import DEFAULT_MAPS, QuantumMap, qubit_restricted_maps

    ideal = qubit_restricted_maps(DEFAULT_MAPS)
    if kind is None or p == 0.0:
        return ideal
    local = [qt.Qobj(np.asarray(k, dtype=complex)) for k in kraus(kind, p)]
    noisy = {}
    for name, ideal_map in ideal.items():
        width = ideal_map.num_qudits
        noise = [qt.tensor(list(ops)) if width > 1 else ops[0] for ops in product(local, repeat=width)]

        def channel(*params: float, ideal_map=ideal_map, noise: list = noise) -> list:
            unitary = ideal_map.channel(params)
            return [op @ unitary for op in noise]

        noisy[name] = QuantumMap(width, channel, branches=ideal_map.branches, tol=ideal_map.tol)
    return noisy
