"""A19: floating-point cost of a dense two-qubit gate applied directly or split by the KAK decomposition (CPU).

The canonical (KAK) decomposition writes a two-qubit unitary as local gates, a two-level rotation
``N`` of the pairs |00>, |11> and |01>, |10>, and local gates. With svpass's two-level rotation form
(noisecirc branch feature/two-level-rotations, `Config.two_level_rotations`) each piece could be
applied as a real rotation between deferred diagonals. This script compares, for random two-qubit
unitaries followed by no-error damping on both qubits, svpass's cost model (`codegen._matrix_cost`,
`codegen._rotation_cost`, instructions per amplitude): the dense matrix; the five KAK pieces in
rotation form; the canonical rotation with only one local gate per qubit (as if the other local
gates merged with neighbouring gates); and the cheapest contraction of stages of 1 to 4 such gates
on 3 qubits with and without the split. A first version of `_kak_split` lived in svpass's code
generator; since it never lowered a stage's cost, it was moved here.

Usage: a19_kak_cost.py (local, CPU; noisecirc branch feature/two-level-rotations)
"""

import json

import numpy as np
from svpass.cuda import codegen
from svpass.cuda.codegen import _diagonal, _two_level_factors

# The magic basis, in which local two-qubit gates (A (x) B, both in SU(2)) are real orthogonal.
_MAGIC = np.array([[1, 1j, 0, 0], [0, 0, 1j, 1], [0, 0, 1j, -1], [1, -1j, 0, 0]]) / np.sqrt(2)


def _kron_factors(matrix: np.ndarray, eps: float) -> tuple[np.ndarray, np.ndarray] | None:
    """Return ``A``, ``B`` with ``matrix = kron(A, B)``, or None if it has no such form."""
    rearranged = matrix.reshape(2, 2, 2, 2).transpose(0, 2, 1, 3).reshape(4, 4)
    u, s, vh = np.linalg.svd(rearranged)
    high, low = np.sqrt(s[0]) * u[:, 0].reshape(2, 2), np.sqrt(s[0]) * vh[0].reshape(2, 2)
    return (high, low) if np.abs(np.kron(high, low) - matrix).max() <= 1e3 * eps + 1e-9 else None


def _kak(matrix: np.ndarray, eps: float) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray] | None:
    """Return a two-qubit unitary as ``kron(A1, B1) N kron(A2, B2)`` with two-level ``N``, or None.

    The canonical (KAK) decomposition: in the magic basis the unitary, scaled to determinant 1, is
    ``O1 L O2`` with real orthogonal ``O1``, ``O2`` and diagonal ``L``; ``O2`` diagonalizes the
    symmetric unitary ``U^T U``, whose real and imaginary parts commute. In the computational
    basis ``L`` is ``N``, which rotates the pairs |00>, |11> and |01>, |10>, and the ``O`` are
    local gates; the determinant's root goes into ``N``. Returns None for degenerate cases this
    simple diagonalization does not resolve, and for matrices that are not unitary.

    Returns:
        ``A1``, ``B1``, ``N``, ``A2``, ``B2``; ``A`` acts on the high index bit, ``B`` on the low one.
    """
    if np.abs(matrix.conj().T @ matrix - np.eye(4)).max() > 1e-9:
        return None
    root = np.linalg.det(matrix) ** 0.25
    magic = _MAGIC.conj().T @ (matrix / root) @ _MAGIC
    symmetric = magic.T @ magic
    _, orthogonal = np.linalg.eigh(symmetric.real + 0.6180339887 * symmetric.imag)
    if np.linalg.det(orthogonal) < 0:
        orthogonal[:, 0] *= -1
    diagonal = orthogonal.T @ symmetric @ orthogonal
    if np.abs(diagonal - np.diag(np.diag(diagonal))).max() > 1e-9:
        return None
    phases = np.sqrt(np.diag(diagonal))
    left = magic @ orthogonal / phases
    if np.abs(left.imag).max() > 1e-9:
        return None
    left = left.real
    if np.linalg.det(left) < 0:
        left[:, 0] *= -1
        phases[0] *= -1
    first = _kron_factors(_MAGIC @ orthogonal.T @ _MAGIC.conj().T, eps)
    last = _kron_factors(_MAGIC @ left @ _MAGIC.conj().T, eps)
    if first is None or last is None:
        return None
    canonical = root * (_MAGIC @ np.diag(phases) @ _MAGIC.conj().T)
    return last[0], last[1], canonical, first[0], first[1]


def _kak_split(items: list, eps: float) -> list:
    """Return the items with each dense two-qubit operation, a unitary up to a diagonal, split by `_kak`.

    An operation ``D U`` with diagonal ``D`` and two-qubit unitary ``U`` that is neither diagonal
    nor two-level becomes the one-qubit operations of ``U``'s second local factor, its two-level
    ``N``, and the one-qubit operations of ``D`` times its first local factor, so that the rotation
    form can take them; the contraction search still finds their product where that costs less.
    """
    out = []
    for item in items:
        index, local, matrices = item
        matrix = np.asarray(matrices[0][1], dtype=complex)
        if len(local) != 2 or len(matrices) != 1 or _two_level_factors(matrix, eps) is not None or _diagonal(matrix, eps):
            out.append(item)
            continue
        # D U with D the row norms: the rows of a unitary times a diagonal are orthogonal.
        norms = np.linalg.norm(matrix, axis=1)
        if np.any(norms < eps):
            out.append(item)
            continue
        found = _kak(matrix / norms[:, None], eps)
        if found is None:
            out.append(item)
            continue
        a1, b1, canonical, a2, b2 = found
        low, high = local
        scale = np.diag(norms)
        last = scale @ np.kron(a1, b1)
        factors = _kron_factors(last, eps)
        if factors is None:
            out.append(item)
            continue
        choice = matrices[0][0]
        out += [(index, (low,), [(choice, b2)]), (index, (high,), [(choice, a2)]), (index, local, [(choice, canonical)]),
                (index, (low,), [(choice, factors[1])]), (index, (high,), [(choice, factors[0])])]
    return out


def unitary(rng: np.random.Generator, d: int) -> np.ndarray:
    z = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
    q, r = np.linalg.qr(z)
    return q * (np.diag(r) / np.abs(np.diag(r)))


def main() -> None:
    rng = np.random.default_rng(0)
    eps = 1e-12
    damping = np.kron(np.diag([1, np.sqrt(0.999)]), np.diag([1, np.sqrt(0.999)]))
    dense, split, merged = [], [], []
    for _ in range(100):
        gate = damping @ unitary(rng, 4)
        pieces = _kak_split([(0, (0, 1), [(0, gate)])], eps)
        gates = [(local, matrices[0][1]) for _, local, matrices in pieces]
        dense.append(codegen._matrix_cost(gate, eps))
        split.append(codegen._rotation_cost(gates, 2, eps, True))
        merged.append(codegen._rotation_cost(gates[2:], 2, eps, True))
    print(json.dumps({"kind": "gate", "dense": float(np.mean(dense)), "kak_rotation_form": float(np.mean(split)),
                      "canonical_and_one_local_per_qubit": float(np.mean(merged))}))
    for count in range(1, 5):
        pairs = [(0, 1), (1, 2)] * 2
        plain, kak = [], []
        for _ in range(20):
            items = [(i, pairs[i], [(0, damping @ unitary(rng, 4))]) for i in range(count)]
            plain.append(codegen._contraction(items, 3, eps)[1])
            kak.append(codegen._contraction(_kak_split(items, eps), 3, eps, True)[1])
        print(json.dumps({"kind": "stage", "gates": count, "contraction": float(np.mean(plain)),
                          "contraction_with_kak": float(np.mean(kak))}))


if __name__ == "__main__":
    main()
