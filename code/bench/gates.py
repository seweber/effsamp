"""Two-qubit gates beyond noisecirc's default set {r, rz, cp, mcphase}, as qubit maps (tasks A18, A19).

Each entry of `EXTRA_MAPS` is a `noisecirc.maps.QuantumMap` on plain qubits
(`noisecirc.twirling.QUBIT_BRANCHES`) of a Qiskit instruction name; `noise.maps` adds them to the
default gates, so circuits may use them with any noise model. Matrices are given in the basis
|q1 q0>, the first target the least-significant bit, as noisecirc's operations order their targets.

- ``su4`` (15 parameters): ``exp(-i sum_k c_k P_k)`` over the 15 two-qubit Paulis other than the
  identity, a generic dense two-qubit unitary for random coefficients.
- ``fsim`` (theta, phi): Google's fSim, an XX+YY rotation by ``theta`` on |01>, |10> and the phase
  ``e^{-i phi}`` on |11>.
- ``rxx``, ``ryy``, ``rzz`` (theta): Qiskit's ``exp(-i theta/2 P P)``.
- ``cry`` (theta): Qiskit's controlled RY, control the first target.
"""

from functools import cache
from itertools import product

import numpy as np
from scipy.linalg import expm

PAULIS = [np.eye(2), np.array([[0, 1], [1, 0]]), np.array([[0, -1j], [1j, 0]]), np.diag([1.0, -1.0])]
# Two-qubit Paulis P_a (x) P_b on |q1 q0>: b acts on q0 (the first target).
TWO_QUBIT_PAULIS = [np.kron(PAULIS[a], PAULIS[b]) for a, b in product(range(4), repeat=2)][1:]


def su4(*coefficients: float) -> np.ndarray:
    return expm(-1j * sum(c * p for c, p in zip(coefficients, TWO_QUBIT_PAULIS, strict=True)))


def fsim(theta: float, phi: float) -> np.ndarray:
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[1, 0, 0, 0], [0, c, -1j * s, 0], [0, -1j * s, c, 0], [0, 0, 0, np.exp(-1j * phi)]])


def pauli_rotation(axis: int):
    pp = np.kron(PAULIS[axis], PAULIS[axis])

    def rotation(theta: float) -> np.ndarray:
        return np.cos(theta / 2) * np.eye(4) - 1j * np.sin(theta / 2) * pp

    return rotation


def cry(theta: float) -> np.ndarray:
    # Control q0 (first target, low bit), target q1.
    c, s = np.cos(theta / 2), np.sin(theta / 2)
    out = np.eye(4, dtype=complex)
    out[np.ix_([1, 3], [1, 3])] = [[c, -s], [s, c]]
    return out


MATRICES = {"su4": su4, "fsim": fsim, "rxx": pauli_rotation(1), "ryy": pauli_rotation(2), "rzz": pauli_rotation(3),
            "cry": cry}


@cache
def extra_maps() -> dict:
    """Return the qubit maps of the gates above, by Qiskit instruction name."""
    import qutip as qt

    from noisecirc.maps import QuantumMap
    from noisecirc.twirling import QUBIT_BRANCHES

    def channel(function):
        return lambda *params: qt.Qobj(function(*params), dims=[[2, 2], [2, 2]])

    return {name: QuantumMap(2, channel(function), branches=QUBIT_BRANCHES) for name, function in MATRICES.items()}
