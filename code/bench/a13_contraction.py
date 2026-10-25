"""A13 follow-up: the contraction order of a stage's operations, and the floating-point work it needs.

A stage applies its operations to the 2**R amplitudes a thread holds in registers. Since the
operations' matrices are constants of the generated kernel, multiplying some of them into one matrix
costs nothing at run time; only applying the products to the registers costs instructions. Every
contraction order of the stage (a contraction tree of the state with the operations) therefore
amounts to a sequence of clusters of operations, each applied as its product: the operations already
applied before a cluster form a down-set of the stage's dependency graph, and a cluster is the
difference of two nested down-sets. The cheapest order is thus a shortest path through the down-sets,
which this script finds exactly (`optimal`), for two dependency graphs: operations depend on earlier
ones sharing a qubit ("strict"), or not if both are diagonal ("diagonals commute").

The cost of a cluster is svpass's own model of its lowering (`codegen._matrix_cost`, vectorized here
as `costs`): floating-point instructions per amplitude, FMAs counted once, entries 0, +-1, +-i free.
It is compared with
  gate      every operation applied by itself (svpass's default),
  runs      the dynamic program over runs of consecutive operations (`stage_fusion`, task A14),
  rotation  real rotations between deferred diagonals (`rotation_form`, task A14),
  a14       what the A14 kernels choose: min(rotation, runs),
  dense     the stage's product as one matrix,
  bound     a lower bound for any straight-line program of FMAs: one instruction per real output
            component that is not plus or minus one real input (`bound`).

Usage: a13_contraction.py [R ...]  (local, CPU; noisecirc branch feature/stage-fusion; the A13
workloads at n = 26 with damping noise; writes one JSON line per circuit and R)
"""

import itertools
import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import circuits  # noqa: E402
import noise  # noqa: E402
from a13_stage_estimate import WORKLOADS  # noqa: E402
from dryrun import compile_like_simulator  # noqa: E402

from noisecirc import Simulator  # noqa: E402
from svpass.cuda import codegen  # noqa: E402

EPS = 1e-12
# Down-sets per stage at most for the exact search; larger stages use the strict graph, else are skipped.
MAX_DOWNSETS = 3000
# Down-sets per stage at most for the search that also lowers clusters in rotation form (slower).
MAX_COMBINED = 1500


def costs(m: np.ndarray, eps: float = EPS) -> np.ndarray:
    """Return `codegen._matrix_cost` of each matrix of the stack ``m`` (B, n, n), vectorized."""
    a = np.abs(m)
    nz = a > eps
    t0 = nz.sum(-1)
    n = m.shape[-1]
    diag = np.eye(n, dtype=bool)
    # Rows that are a copy of one amplitude (identity rows included) cost nothing.
    single_one = (t0 == 1) & (np.abs(np.where(nz, m, 0).sum(-1) - 1.0) < eps)
    amax = np.where(nz, a, -np.inf).max(-1)
    amin = np.where(nz, a, np.inf).min(-1)
    shared = (t0 > 1) & (amax - amin <= eps)
    common = np.where(shared, amax, 1.0)
    v = m / common[..., None]
    realish = np.abs(v.imag) < eps
    imagish = np.abs(v.real) < eps
    one_part = realish | imagish
    part = np.where(realish, v.real, v.imag)
    unit = np.abs(np.abs(part) - 1.0) < eps
    terms = np.where(nz, np.where(one_part, 1, 2), 0).sum(-1)
    products = np.where(nz, np.where(one_part, ~unit, 2), 0).sum(-1)
    row = terms - 1 + products - np.minimum(products, terms - 1) + (np.abs(common - 1.0) > eps)
    row = np.where((t0 == 0) | single_one, 0, row)
    del diag
    return 2 * row.sum(-1) / n


def bound(u: np.ndarray, eps: float = 1e-9) -> float:
    """Return a lower bound on the instructions per amplitude of applying ``u`` by any FMA program.

    Each instruction yields one real value, and a real output component that is neither 0 nor plus
    or minus one real input component must be such a value; distinct outputs need distinct values.
    """
    n = len(u)
    real = np.block([[u.real, -u.imag], [u.imag, u.real]])
    forms = set()
    for rowv in real:
        nzc = np.flatnonzero(np.abs(rowv) > eps)
        if len(nzc) == 0 or (len(nzc) == 1 and abs(abs(rowv[nzc[0]]) - 1.0) < eps):
            continue
        forms.add(tuple(np.round(rowv / rowv[nzc[0]] * np.sign(rowv[nzc[0]]), 9)) + (round(abs(rowv[nzc[0]]), 9),))
    return len(forms) / n


def full(matrix: np.ndarray, local: tuple[int, ...], r: int) -> np.ndarray:
    """Return ``matrix`` on the register bits ``local`` as a matrix on all ``r`` bits."""
    return codegen._embed(np.asarray(matrix, dtype=complex), tuple(local), tuple(range(r)))


def downsets(preds: list[int], m: int, limit: int) -> list[int] | None:
    """Return the down-sets (bit masks) of the graph with predecessor masks ``preds``, or None above ``limit``."""
    out = [0]
    for i in range(m):
        # Down-sets of operations 0..i: those of 0..i-1, and those plus i where its predecessors are in.
        out += [d | 1 << i for d in out if d & preds[i] == preds[i]]
        if len(out) > limit:
            return None
    return out


def _scale_costs(z: np.ndarray, eps: float = EPS) -> np.ndarray:
    """Return the instructions of multiplying a register by each ``z`` (`_rotation_form`'s ``scale``)."""
    realish = np.abs(z.imag) < eps
    imagish = np.abs(z.real) < eps
    part = np.where(realish, z.real, z.imag)
    c = np.where(realish | imagish, np.where(np.abs(np.abs(part) - 1.0) < eps, 0, 2), 4)
    return np.where(np.abs(z - 1.0) < eps, 0, c)


def rotation_cost(gates: list[tuple[tuple[int, ...], np.ndarray]], r: int, eps: float = EPS) -> float:
    """Return `codegen._rotation_form`'s instructions per amplitude for ``gates`` (local bits, matrix), inf if inapplicable."""
    size = 1 << r
    c = np.arange(size)
    pending = np.ones(size, dtype=complex)
    cost = 0.0
    for local, matrix in gates:
        if np.all(np.abs(matrix - np.diag(np.diag(matrix))) < eps):
            sub = sum(((c >> bit) & 1) << j for j, bit in enumerate(local))
            pending = pending * np.diag(matrix)[sub]
            continue
        if len(local) != 1:
            return np.inf
        factors = codegen._rotation_factors(matrix, eps)
        if factors is None:
            return np.inf
        form, value, left, right = factors
        q = local[0]
        bitv = (c >> q) & 1
        pending = pending * right[bitv]
        high = c[bitv == 1]
        low = pending[high ^ (1 << q)]
        if np.any(np.abs(low) < eps):
            return np.inf
        cost += _scale_costs(pending[high] / low).sum()
        pending[high] = low
        if not (form == "cot" and value == 0.0):
            cost += 2 * size
        pending = pending * left[bitv]
    cost += _scale_costs(pending).sum()
    return cost / size


def optimal(mats: list[np.ndarray], preds: list[int], limit: int, gates=None) -> tuple[float, list[int]] | None:
    """Return the least total cost over contraction orders and the cluster masks of one, or None if too many down-sets.

    With ``gates`` (each operation's local bits and matrix), a cluster may also be applied in rotation
    form (`rotation_cost`), whichever is cheaper.
    """
    m = len(mats)
    ds = downsets(preds, m, limit)
    if ds is None:
        return None
    ds.sort(key=lambda d: bin(d).count("1"))
    n = len(mats[0])
    r = n.bit_length() - 1
    rot_cache: dict[int, float] = {}

    def rot(mask: int) -> float:
        if mask not in rot_cache:
            rot_cache[mask] = rotation_cost([gates[i] for i in range(m) if mask >> i & 1], r)
        return rot_cache[mask]
    # Product of each down-set, in index order (a linear extension of the graph).
    prod = {}
    for d in ds:
        u = np.eye(n, dtype=complex)
        for i in range(m):
            if d >> i & 1:
                u = mats[i] @ u
        prod[d] = u
    inv = {d: np.linalg.inv(prod[d]) for d in ds}
    best = {0: (0.0, None)}
    for d in ds[1:]:
        subs = [e for e in ds if e & d == e and e != d and e in best]
        clusters = np.stack([prod[d] @ inv[e] for e in subs])
        c = costs(clusters, 1e-9)
        if gates is not None:
            c = np.minimum(c, [rot(d & ~e) for e in subs])
        c = c + np.array([best[e][0] for e in subs])
        j = int(np.argmin(c))
        best[d] = (float(c[j]), subs[j])
    path, d = [], ds[-1]
    while d:
        e = best[d][1]
        path.append(d & ~e)
        d = e
    return best[ds[-1]][0], path[::-1]


def greedy(mats: list[np.ndarray], preds: list[int], gates) -> tuple[float, list[int]]:
    """Return the cost and clusters of greedy merging: start from single operations, merge the pair that saves most.

    A cluster is applied as its product or in rotation form, whichever is cheaper; two clusters may
    merge if the clusters still form an acyclic graph (then they can be applied in some order).
    """
    m = len(mats)
    r = len(mats[0]).bit_length() - 1
    cache: dict[int, float] = {}

    def cost(mask: int) -> float:
        if mask not in cache:
            u = np.eye(1 << r, dtype=complex)
            for i in range(m):
                if mask >> i & 1:
                    u = mats[i] @ u
            cache[mask] = min(float(costs(u[None], 1e-9)[0]), rotation_cost([gates[i] for i in range(m) if mask >> i & 1], r))
        return cache[mask]

    def acyclic(clusters: list[int]) -> bool:
        # Cluster a precedes b if an operation of b has a predecessor in a.
        left, done = list(clusters), 0
        while left:
            ready = [c for c in left if all((preds[i] & ~c) & ~done == 0 for i in range(m) if c >> i & 1)]
            if not ready:
                return False
            for c in ready:
                left.remove(c)
                done |= c
        return True

    clusters = [1 << i for i in range(m)]
    while True:
        best = None
        for a, b in itertools.combinations(range(len(clusters)), 2):
            saving = cost(clusters[a]) + cost(clusters[b]) - cost(clusters[a] | clusters[b])
            if saving > 1e-9 and (best is None or saving > best[0]):
                trial = [c for k, c in enumerate(clusters) if k not in (a, b)] + [clusters[a] | clusters[b]]
                if acyclic(trial):
                    best = (saving, trial)
        if best is None:
            break
        clusters = best[1]
    return sum(cost(c) for c in clusters), clusters


def runs_both(mats: list[np.ndarray], gates, order: list[int]) -> float:
    """Return the least cost of applying runs of consecutive operations of ``order``, each as its product or in rotation form."""
    m = len(order)
    r = len(mats[0]).bit_length() - 1
    best = [0.0] + [np.inf] * m
    for stop in range(1, m + 1):
        u = np.eye(1 << r, dtype=complex)
        for begin in range(stop - 1, -1, -1):
            u = u @ mats[order[begin]]
            c = min(float(costs(u[None], 1e-9)[0]), rotation_cost([gates[i] for i in order[begin:stop]], r))
            best[stop] = min(best[stop], best[begin] + c)
    return best[m]


def stage_items(block, config):
    """Yield each stage's register width and items ``(index, local bits, [(choice, matrix)])`` of the dominant kernel."""
    tile = block.tile(config)
    k = len(tile)
    r = codegen.stage_width(config, k)
    tile_bit = {qubit: bit for bit, qubit in enumerate(tile)}
    for start, stop in block.stage_ranges():
        used = {tile_bit[int(q)] for op in block.operations[start:stop] for q in op.targets}
        fill = [bit for bit in range(k - 1, -1, -1) if bit not in used][: r - len(used)]
        bits = tuple(sorted(used | set(fill)))
        items = []
        for i in range(start, stop):
            op = block.operations[i]
            local = tuple(bits.index(tile_bit[int(q)]) for q in op.targets)
            choice = 0 if block.defaults is None else int(block.defaults[i])
            items.append((i, local, [(choice, np.asarray(op.kraus[choice], dtype=complex))]))
        yield r, items


def analyse_stage(r: int, items, precision) -> dict:
    mats = [full(m[0][1], local, r) for _, local, m in items]
    diagonal = [bool(np.abs(u - np.diag(np.diag(u))).max() < EPS) for u in mats]
    m = len(items)
    out = {"ops": m}
    out["gate"] = float(sum(codegen._matrix_cost(mm[0][1], EPS) for _, _, mm in items))
    out["runs"] = float(sum(codegen._matrix_cost(mm[0][1], EPS) for _, _, mm in codegen._fuse_runs(items, EPS)))
    rot = codegen._rotation_form(precision, items, r, EPS)
    out["rotation"] = float(rot[3]) if rot is not None else None
    out["a14"] = min(out["runs"], out["rotation"]) if rot is not None and out["rotation"] <= out["runs"] else out["runs"]
    total = np.eye(1 << r, dtype=complex)
    for u in mats:
        total = u @ total
    out["dense"] = float(costs(total[None], 1e-9)[0])
    out["bound"] = bound(total)
    gates = [(local, mm[0][1]) for _, local, mm in items]
    for name, relax in (("strict", False), ("commute", True)):
        preds = [0] * m
        for i, j in itertools.combinations(range(m), 2):
            if set(items[i][1]) & set(items[j][1]) and not (relax and diagonal[i] and diagonal[j]):
                preds[j] |= 1 << i
        res = optimal(mats, preds, MAX_DOWNSETS)
        out[name] = None if res is None else res[0]
        if res is not None:
            # Check: the clusters' products, applied in order, give the stage's product.
            u = np.eye(1 << r, dtype=complex)
            for mask in res[1]:
                c = np.eye(1 << r, dtype=complex)
                for i in range(m):
                    if mask >> i & 1:
                        c = mats[i] @ c
                u = c @ u
            assert np.allclose(u, total, atol=1e-9), "clusters do not reproduce the stage"
            out[name + "_clusters"] = len(res[1])
        if relax:
            res = optimal(mats, preds, MAX_COMBINED, gates) or optimal(mats, strict_preds, MAX_COMBINED, gates)
            out["combined"] = None if res is None else res[0]
            # A cheap order: a linear extension that follows the last operation's qubits, fused by runs.
            order, done, last = [], 0, set()
            while len(order) < m:
                ready = [i for i in range(m) if not done >> i & 1 and preds[i] & done == preds[i]]
                i = max(ready, key=lambda i: (len(set(items[i][1]) & last), -i))
                order.append(i)
                done |= 1 << i
                last = set(items[i][1])
            out["greedy"] = greedy(mats, preds, gates)[0]
            out["runs_both"] = min(runs_both(mats, gates, list(range(m))), runs_both(mats, gates, order))
            t = time.time()
            res = optimal(mats, strict_preds, MAX_COMBINED, gates)
            out["combined_strict"] = out["combined"] if res is None else res[0]
            out["seconds_strict"] = time.time() - t
            fused = codegen._fuse_runs([items[i] for i in order], EPS)
            out["local_runs"] = float(sum(codegen._matrix_cost(mm[0][1], EPS) for _, _, mm in fused))
        else:
            strict_preds = preds
    out["rotations"] = sum(not d for d in diagonal)
    if rot is not None:
        assert abs(rotation_cost(gates, r) - out["rotation"]) < 1e-9, "rotation_cost disagrees with codegen"
    return out


def main() -> None:
    widths = [int(a) for a in sys.argv[1:]] or [3, 4]
    for name, p in WORKLOADS:
        qc = circuits.make(name, 26)
        for r in widths:
            t0 = time.time()
            compiled, _, _ = compile_like_simulator(qc, Simulator(maps=noise.maps("damping", p), stage_qubits=r))
            config = compiled.config
            precision = codegen.Precision.of(config.dtype)
            sums: dict[str, float] = {}
            skipped = commute_missing = combined_missing = n_stages = 0
            for block in compiled.blocks:
                dom = block.dominant_block
                for rr, items in stage_items(dom, config):
                    s = analyse_stage(rr, items, precision)
                    n_stages += 1
                    if s["strict"] is None:
                        skipped += 1
                        continue
                    if s["commute"] is None:
                        commute_missing += 1
                        s["commute"] = s["strict"]
                    s["best"] = min(s["commute"], s["rotation"] if s["rotation"] is not None else np.inf)
                    s["local_a14"] = min(s["local_runs"], s["rotation"] if s["rotation"] is not None else np.inf)
                    if s["combined"] is None:
                        combined_missing += 1
                        s["combined"] = s["best"]
                    for key in ("gate", "runs", "a14", "dense", "bound", "strict", "commute", "best",
                                "local_runs", "local_a14", "combined", "greedy", "runs_both", "combined_strict", "seconds_strict", "rotations"):
                        sums[key] = sums.get(key, 0.0) + s[key]
            nb = len(compiled.blocks)
            print(json.dumps({"circuit": name, "R": r, "blocks": nb, "stages": n_stages, "skipped": skipped,
                              "commute_capped": commute_missing, "combined_capped": combined_missing,
                              "fp_per_amplitude_per_block": {k: v / nb for k, v in sums.items()},
                              "seconds": round(time.time() - t0, 1)}), flush=True)


if __name__ == "__main__":
    main()
