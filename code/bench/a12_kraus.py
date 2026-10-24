"""A12: what a Kraus set costs noisecirc, and the sets of a channel that cost the least.

noisecirc proposes each gate's Kraus operator L_j with probability ||L_j||^2 / Z (operator norm,
Z = sum_j ||L_j||^2) and accepts it with ||L_j psi||^2 / ||L_j||^2. The operator of the largest
bound is the dominant one (no error, dominant kernel, shared by all shots of a checkpoint). Per gate
and shot, two numbers of a set cost passes:

- E = Z - ||L_dom||^2, the expected proposals of non-dominant operators until acceptance; each is a
  pass of an error kernel, accepted or not;
- mu(rho) = 1 - tr(rho L_dom^dagger L_dom), the expected accepted non-dominant operators; each
  starts a distinct trajectory that is propagated through the rest of the circuit.

Bounds: E >= mu(rho) for every rho (an accepted proposal was proposed), so E >= 1 - sigma_min(L_dom)^2;
and tr(rho L^dagger L) over L = sum_i v_i K_i, |v| <= 1, is at most the largest eigenvalue of the
Gram matrix G_ik = tr(rho K_i^dagger K_k), which the canonical (Choi) set attains for rho = I/d.

Every Kraus set of the channel is L = V K with an isometry V (m x r, m >= r) and K the canonical set
of rank r. The functions below compute the metrics, the canonical set, and minimize E + w * mu(rho)
over V for a weight w, which traces the trade-off between error proposals and distinct
trajectories.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import minimize


def canonical(kraus: list[np.ndarray] | np.ndarray, tol: float = 1e-14) -> np.ndarray:
    """Return the canonical Kraus set: the Choi eigenvectors scaled, largest Frobenius norm first."""
    ops = np.asarray(kraus, dtype=complex)
    _, s, vh = np.linalg.svd(ops.reshape(len(ops), -1), full_matrices=False)
    keep = s**2 > tol
    return (s[keep, None] * vh[keep]).reshape(-1, *ops.shape[1:])


def bounds(ops: np.ndarray) -> np.ndarray:
    """Return the upper probability bounds ||L_j||^2 (largest eigenvalue of L_j^dagger L_j)."""
    return np.linalg.eigvalsh(np.einsum("jab,jac->jbc", ops.conj(), ops))[:, -1]


def metrics(ops: np.ndarray, rho: np.ndarray | None = None) -> dict:
    """Return Z, E, mu(rho) (maximally mixed by default), mu_max and the dominant index of a set."""
    ops = np.asarray(ops, dtype=complex)
    d = ops.shape[-1]
    rho = np.eye(d) / d if rho is None else rho
    b = bounds(ops)
    dom = int(np.argmax(b))
    gram = ops[dom].conj().T @ ops[dom]
    z = float(b.sum())
    return {
        "Z": z,
        "E": z - float(b[dom]),
        "mu": 1.0 - float(np.trace(rho @ gram).real),
        "mu_max": 1.0 - float(np.linalg.eigvalsh(gram)[0]),
        "dom": dom,
        "n": int(np.count_nonzero(b > 1e-15)),
    }


def mixed(ops: np.ndarray, x: np.ndarray, m: int) -> np.ndarray:
    """Return V K for the isometry V = first r columns of exp(A), A skew-Hermitian from ``x`` (m x m)."""
    r = len(ops)
    a = np.zeros((m, m), dtype=complex)
    iu = np.triu_indices(m, 1)
    c = len(iu[0])
    a[iu] = x[:c] + 1j * x[c : 2 * c]
    a = a - a.conj().T
    a[np.diag_indices(m)] = 1j * x[2 * c :]
    eye = np.eye(m)
    v = np.linalg.solve((eye + a).T, (eye - a).T).T[:, :r]  # Cayley transform (1 - A)(1 + A)^-1
    return np.einsum("ji,iab->jab", v, ops)


def _skew(x: np.ndarray, m: int) -> np.ndarray:
    """Skew-Hermitian m x m matrix from m*m reals (upper real, upper imaginary, imaginary diagonal)."""
    iu = np.triu_indices(m, 1)
    c = len(iu[0])
    a = np.zeros((m, m), dtype=complex)
    a[iu] = x[:c] + 1j * x[c : 2 * c]
    a = a - a.conj().T
    a[np.diag_indices(m)] = 1j * x[2 * c :]
    return a


def _skew_gradient(g: np.ndarray) -> np.ndarray:
    """Gradient in `_skew`'s parameters of Re tr(G^dagger dA)."""
    m = len(g)
    iu = np.triu_indices(m, 1)
    paired = g - g.conj().T
    return np.concatenate([paired[iu].real, paired[iu].imag, np.diag(g).imag])


def optimize(
    kraus: list[np.ndarray] | np.ndarray,
    w: float,
    extra: int = 0,
    rho: np.ndarray | None = None,
    starts: int = 8,
    seed: int = 0,
) -> tuple[np.ndarray, dict]:
    """Minimize E + w * mu(rho) over Kraus sets of rank + ``extra`` operators, operator 0 the dominant one.

    L = V K with K the canonical set padded by ``extra`` zero operators and V = (1 - A)(1 + A)^-1
    unitary (Cayley), by BFGS with the analytic gradient (d lambda_max(L^dagger L) = 2 Re v^dagger
    L^dagger dL v), from the identity and random starts. The cost treats operator 0 as the dominant
    one; the returned metrics use the true dominant (largest bound).

    Returns:
        The best set and its metrics.
    """
    cost_grad, padded, rho = _objective(kraus, w, extra, rho)
    m = len(padded)
    eye = np.eye(m)
    rng = np.random.default_rng(seed)
    best_x, best = np.zeros(m * m), cost_grad(np.zeros(m * m))[0]
    for s in range(starts):
        x0 = np.zeros(m * m) if s == 0 else rng.normal(scale=[0.1, 0.5, 1.5][s % 3], size=m * m)
        res = minimize(cost_grad, x0, jac=True, method="BFGS", options={"maxiter": 3000, "gtol": 1e-11})
        if res.fun < best - 1e-15:
            best, best_x = float(res.fun), res.x
    a = _skew(best_x, m)
    out = np.einsum("ji,iab->jab", (eye - a) @ np.linalg.inv(eye + a), padded)
    return out, metrics(out, rho)


def _objective(kraus, w: float, extra: int, rho):
    """Return the cost E + w * mu (operator 0 dominant) with its gradient in `_skew`'s parameters, the padded set and rho."""
    ops = canonical(kraus)
    d = ops.shape[-1]
    rho = np.eye(d) / d if rho is None else rho
    m = len(ops) + extra
    padded = np.concatenate([ops, np.zeros((extra, d, d), dtype=complex)])
    eye = np.eye(m)

    def cost_grad(x: np.ndarray) -> tuple[float, np.ndarray]:
        a = _skew(x, m)
        inv = np.linalg.inv(eye + a)
        v = (eye - a) @ inv
        mixed = np.einsum("ji,iab->jab", v, padded)
        vals, vecs = np.linalg.eigh(np.einsum("jab,jac->jbc", mixed.conj(), mixed))
        top = vecs[:, :, -1]
        h = np.einsum("jab,jb,jc->jac", mixed, top, top.conj())
        h[0] = -w * mixed[0] @ rho
        cost = float(vals[1:, -1].sum()) + w * (1 - float(np.trace(rho @ mixed[0].conj().T @ mixed[0]).real))
        g = np.einsum("jac,iac->ji", h, padded.conj())
        g = -2 * (eye + v).conj().T @ g @ inv.conj().T
        return cost, _skew_gradient(g)

    return cost_grad, padded, rho


# --- Channels ------------------------------------------------------------------------------------

X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]])
Zp = np.diag([1.0 + 0j, -1.0])
I2 = np.eye(2, dtype=complex)


def channel(kind: str, p: float, **kw: float) -> list[np.ndarray]:
    """Return Kraus operators of a single-qubit channel (any set; the canonical one is derived)."""
    if kind == "damping":
        return [np.diag([1, np.sqrt(1 - p)]).astype(complex), np.sqrt(p) * np.array([[0, 1], [0, 0]], dtype=complex)]
    if kind == "dephasing":  # phase damping, as code/bench/noise.py
        return [np.diag([1, np.sqrt(1 - p)]).astype(complex), np.diag([0, np.sqrt(p)]).astype(complex)]
    if kind == "depolarizing":
        return [np.sqrt(1 - p) * I2, *(np.sqrt(p / 3) * m for m in (X, Y, Zp))]
    if kind == "gad":
        n = kw.get("n", 0.2)
        a, b = np.sqrt(1 - n), np.sqrt(n)
        return [
            a * np.diag([1, np.sqrt(1 - p)]),
            a * np.sqrt(p) * np.array([[0, 1], [0, 0]]),
            b * np.diag([np.sqrt(1 - p), 1]),
            b * np.sqrt(p) * np.array([[0, 0], [1, 0]]),
        ]
    if kind == "thermal":  # damping p then phase damping p, as code/bench/noise.py
        return [d @ a for d in channel("dephasing", p) for a in channel("damping", p)]
    if kind == "damp_depol":  # damping p then depolarizing q
        q = kw.get("q", p)
        return [d @ a for d in channel("depolarizing", q) for a in channel("damping", p)]
    if kind == "damp_overrot":  # damping p after a coherent over-rotation exp(-i eps X / 2), eps = sqrt(p)
        eps = kw.get("eps", np.sqrt(p))
        u = np.cos(eps / 2) * I2 - 1j * np.sin(eps / 2) * X
        return [a @ u for a in channel("damping", p)]
    raise ValueError(kind)


def tensor(*sets: list[np.ndarray]) -> list[np.ndarray]:
    """Return the Kraus operators of the tensor product of channels, the first the most significant."""
    out = [np.eye(1, dtype=complex)]
    for s in sets:
        out = [np.kron(a, b) for a in out for b in s]
    return out


def lower_bound(kraus: list[np.ndarray] | np.ndarray, w: float, rho: np.ndarray | None = None, starts: int = 20, seed: int = 0) -> dict:
    """Return a lower bound on min E + w * mu(rho) over all Kraus sets, and the dominant operator attaining it.

    For a dominant L0 = sum_i v_i K_i (|v| <= 1), every set has E >= 1 - sigma_min(L0)^2 (E >= mu(rho')
    for every state rho') and E >= ||E(I) - L0 L0^dagger|| (the remaining operators' sum of L L^dagger),
    so min over L0 of max(both) + w * mu(rho) bounds every set. The minimization over v is
    non-convex; the best of several starts is returned, so the bound is the found minimum (exact up to
    the search).
    """
    ops = canonical(kraus)
    r, d = len(ops), ops.shape[-1]
    rho = np.eye(d) / d if rho is None else rho
    out_identity = np.einsum("jab,jcb->ac", ops, ops.conj())
    rng = np.random.default_rng(seed)

    def parts(x):
        v = x[:r] + 1j * x[r:]
        v = v / max(1.0, np.linalg.norm(v))
        l0 = np.einsum("i,iab->ab", v, ops)
        s_min = np.linalg.svd(l0, compute_uv=False)[-1]
        e_in = 1 - s_min**2
        e_out = np.linalg.eigvalsh(out_identity - l0 @ l0.conj().T)[-1]
        mu = 1 - np.trace(rho @ l0.conj().T @ l0).real
        return e_in, e_out, mu

    def cost(x):
        e_in, e_out, mu = parts(x)
        return max(e_in, e_out) + w * mu

    best = None
    for s in range(starts):
        x0 = np.zeros(2 * r)
        x0[0] = 1.0
        if s:
            x0 = rng.normal(size=2 * r)
        res = minimize(cost, x0, method="Nelder-Mead", options={"maxiter": 20000, "xatol": 1e-13, "fatol": 1e-16})
        if best is None or res.fun < best.fun:
            best = res
    e_in, e_out, mu = parts(best.x)
    return {"J": float(best.fun), "E_bound": max(e_in, e_out), "mu": mu, "e_in": e_in, "e_out": e_out}


def optimize_residual(kraus, extra: int = 0, starts: int = 24, seed: int = 0) -> tuple[np.ndarray, dict]:
    """Keep the canonical dominant operator and minimize the remaining operators' oversampling E.

    The canonical first operator maximizes tr(L0^dagger L0), i.e. minimizes mu for a maximally mixed
    input; the remaining canonical operators (padded by ``extra`` zeros) are mixed by a unitary W to
    minimize sum_j ||L_j||^2 (BFGS with analytic gradient, Cayley parametrization, many random starts
    since the canonical set is often a degenerate stationary point).

    Returns:
        The set (dominant first) and its metrics.
    """
    ops = canonical(kraus)
    d = ops.shape[-1]
    rest = np.concatenate([ops[1:], np.zeros((extra, d, d), dtype=complex)])
    m = len(rest)
    if m == 0:
        return ops, metrics(ops)
    eye = np.eye(m)
    rng = np.random.default_rng(seed)

    def cost_grad(x):
        a = _skew(x, m)
        inv = np.linalg.inv(eye + a)
        v = (eye - a) @ inv
        mixed = np.einsum("ji,iab->jab", v, rest)
        vals, vecs = np.linalg.eigh(np.einsum("jab,jac->jbc", mixed.conj(), mixed))
        top = vecs[:, :, -1]
        h = np.einsum("jab,jb,jc->jac", mixed, top, top.conj())
        g = np.einsum("jac,iac->ji", h, rest.conj())
        g = -2 * (eye + v).conj().T @ g @ inv.conj().T
        return float(vals[:, -1].sum()), _skew_gradient(g)

    best_x, best = np.zeros(m * m), cost_grad(np.zeros(m * m))[0]
    for s in range(starts):
        x0 = rng.normal(scale=[0.3, 1.0, 3.0][s % 3], size=m * m)
        res = minimize(cost_grad, x0, jac=True, method="BFGS", options={"maxiter": 2000, "gtol": 1e-12})
        if res.fun < best - 1e-15:
            best, best_x = float(res.fun), res.x
    a = _skew(best_x, m)
    out = np.concatenate([ops[:1], np.einsum("ji,iab->jab", (eye - a) @ np.linalg.inv(eye + a), rest)])
    return out, metrics(out)
