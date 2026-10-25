"""A12 follow-up: Kraus sets when shots that propose the same error share one trajectory.

noisecirc groups shots (`propose_unique_trajectories`): all shots of a checkpoint that propose the
same operator at the same gate form one trajectory, one pass. For n shots crossing a gate, the
expected distinct error proposals and accepted errors are

    P_n = sum_{j>=1} (1 - exp(-n b_j)),   A_n = sum_{j>=1} (1 - exp(-n a_j)),

with b_j = ||L_j||^2 (operator norm) and a_j = tr(rho L_j^dag L_j). For n b_j << 1 they are n E and
n mu of a12_kraus; for n b_j >> 1 they count the operators. This script compares four sets with the
canonical dominant operator kept:

- canonical: Choi eigenvectors (sequential PCA: most dominant first, then the most dominant of the rest);
- greedy: the PLAN.md rule applied to the bounds: operator 1 maximizes ||L||^2 among the residual
  span, operator 2 among the orthogonal rest, and so on;
- E-optimum: residual mixed to minimize sum b_j (a12_kraus.optimize_residual), the small-n optimum;
- n-optimum: residual mixed to minimize P_n + w A_n for given x = n p and weight w (an accepted
  distinct error costs w proposal passes: the passes of the rest of the circuit).

Usage: a12_collisions.py [kinds] (local, CPU) -> JSON lines; two-qubit rows are tensor squares of the one-qubit sets
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

sys.path.insert(0, str(Path(__file__).parent))
from a12_kraus import _skew, _skew_gradient, bounds, canonical, channel, optimize_residual, tensor  # noqa: E402


def mix_residual(ops: np.ndarray, phi, dphi, starts: int = 24, seed: int = 0, x0s=(), w: float = 0.0) -> np.ndarray:
    """Keep ops[0] and mix the rest by a unitary to minimize sum_j phi(b_j) + w phi(a_j) (phi concave, increasing).

    a_j = tr(L_j^dag L_j) / d, the acceptance of L_j for a maximally mixed input.
    """
    rest = ops[1:]
    m = len(rest)
    eye = np.eye(m)
    rng = np.random.default_rng(seed)

    def cost_grad(x):
        a = _skew(x, m)
        inv = np.linalg.inv(eye + a)
        v = (eye - a) @ inv
        mixed = np.einsum("ji,iab->jab", v, rest)
        vals, vecs = np.linalg.eigh(np.einsum("jab,jac->jbc", mixed.conj(), mixed))
        b = vals[:, -1]
        top = vecs[:, :, -1]
        d = mixed.shape[-1]
        acc = np.einsum("jab,jab->j", mixed.conj(), mixed).real / d
        h = np.einsum("jab,jb,jc->jac", mixed, top, top.conj()) * dphi(b)[:, None, None]
        h = h + w * mixed * (dphi(acc) / d)[:, None, None]
        g = np.einsum("jac,iac->ji", h, rest.conj())
        g = -2 * (eye + v).conj().T @ g @ inv.conj().T
        return float(phi(b).sum() + w * phi(acc).sum()), _skew_gradient(g)

    best_x, best = np.zeros(m * m), cost_grad(np.zeros(m * m))[0]
    starts_list = [np.zeros(m * m), *x0s] + [rng.normal(scale=[0.3, 1.0, 3.0][s % 3], size=m * m) for s in range(starts)]
    for x0 in starts_list:
        res = minimize(cost_grad, x0, jac=True, method="BFGS", options={"maxiter": 2000, "gtol": 1e-12})
        if res.fun < best - 1e-15:
            best, best_x = float(res.fun), res.x
    a = _skew(best_x, m)
    return np.concatenate([ops[:1], np.einsum("ji,iab->jab", (eye - a) @ np.linalg.inv(eye + a), rest)])


def greedy(ops: np.ndarray, starts: int = 16, seed: int = 0) -> np.ndarray:
    """Sequentially pick, in the orthogonal complement of the previous picks, the unit mixture of the residual with the largest ||L||^2."""
    rest = ops[1:]
    m = len(rest)
    rng = np.random.default_rng(seed)
    basis = np.eye(m, dtype=complex)  # orthonormal basis of the remaining coefficient space (rows)
    out = [ops[0]]
    while len(basis):
        k = len(basis)
        if k == 1:
            out.append(np.einsum("i,iab->ab", basis[0], rest))
            break

        def cost(x):
            c = x[:k] + 1j * x[k:]
            c = c / np.linalg.norm(c)
            op = np.einsum("i,iab->ab", c @ basis, rest)
            return -np.linalg.norm(op, 2) ** 2

        best = None
        for s in range(starts):
            res = minimize(cost, rng.normal(size=2 * k), method="BFGS")
            if best is None or res.fun < best.fun:
                best = res
        c = best.x[:k] + 1j * best.x[k:]
        c = c / np.linalg.norm(c)
        v = c @ basis
        out.append(np.einsum("i,iab->ab", v, rest))
        # Remove v from the basis: orthonormal complement of v within span(basis).
        proj = basis - np.outer(basis @ v.conj(), v)
        q, r = np.linalg.qr(proj.T)
        keep = np.abs(np.diag(r)) > 1e-9
        basis = q[:, keep].T[: k - 1]
    return np.asarray(out)


def costs(ops: np.ndarray, p: float, xs) -> dict:
    d = ops.shape[-1]
    b = bounds(ops)[1:]
    a = np.einsum("jab,jab->j", ops.conj(), ops).real[1:] / d
    return {
        "b_over_p": sorted((b / p).round(4).tolist(), reverse=True),
        "E": float(b.sum() / p),
        "mu": float(a.sum() / p),
        **{f"P@{x:g}": float(np.sum(1 - np.exp(-x / p * b))) for x in xs},
        **{f"A@{x:g}": float(np.sum(1 - np.exp(-x / p * a))) for x in xs},
    }


def main() -> None:
    p = 1e-2
    xs = (0.1, 1.0, 3.0, 10.0, 30.0)
    kinds = sys.argv[1].split(",") if len(sys.argv) > 1 else ["depolarizing", "dephasing", "damp_depol", "gad", "thermal"]
    for kind in kinds:
        k1 = channel(kind, p)
        ops = canonical(k1)
        sets = {"canonical": ops, "greedy": greedy(ops)}
        eopt = optimize_residual(k1, starts=24)[0]
        sets["E-optimum"] = eopt
        for x in (1.0, 10.0):
            for w in (0.0, 1.0, 5.0):
                n = x / p
                phi = lambda b, n=n: 1 - np.exp(-n * b)  # noqa: E731
                dphi = lambda b, n=n: n * np.exp(-n * b)  # noqa: E731
                sets[f"optimum@x={x:g},w={w:g}"] = mix_residual(ops, phi, dphi, starts=24, x0s=(params_of(ops, eopt),), w=w)
        for label, s1 in sets.items():
            print(json.dumps({"channel": kind, "qubits": 1, "set": label, **costs(s1, p, xs)}), flush=True)
            # The noise after a two-qubit gate: the tensor square, as the dry runs use it.
            s2 = canonical_first(np.asarray([np.kron(a, b) for a in s1 for b in s1]))
            print(json.dumps({"channel": kind, "qubits": 2, "set": label, **costs(s2, p, xs)}), flush=True)


def params_of(ops: np.ndarray, target: np.ndarray) -> np.ndarray:
    """Return `_skew` parameters x whose Cayley unitary maps ops[1:] to target[1:] (same dominant)."""
    rest, goal = ops[1:].reshape(len(ops) - 1, -1), target[1:].reshape(len(target) - 1, -1)
    w = goal @ np.linalg.pinv(rest)
    u, _, vh = np.linalg.svd(w)
    w = u @ vh  # nearest unitary
    m = len(w)
    a = (np.eye(m) - w) @ np.linalg.inv(np.eye(m) + w)
    iu = np.triu_indices(m, 1)
    return np.concatenate([a[iu].real, a[iu].imag, np.diag(a).imag])


def canonical_first(ops: np.ndarray) -> np.ndarray:
    """Order a set so that its largest-bound operator comes first."""
    order = np.argsort(-bounds(ops), kind="stable")
    return ops[order]


if __name__ == "__main__":
    main()
