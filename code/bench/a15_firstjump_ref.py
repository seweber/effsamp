"""A15: reference implementation (NumPy, small registers) of first-jump sampling against noisecirc's proposals.

Both samplers run on noisecirc's own compiled blocks (operations, Kraus stacks, bounds, dominant
choices) with one block per segment, exact mode, and count block passes the way noisecirc does: one
pass per distinct trajectory propagated through a block from a checkpoint.

- ``proposals`` (noisecirc's scheme, simplified): for the shots of a checkpoint, draw each gate's
  choice from its bounds, propagate every distinct path once (norms cached across refill rounds),
  accept by the squared norm of the proposal-normalized product, re-propose the rejected shots.
- ``first_jump``: the pass of the checkpoint's dominant path yields, at each gate, the probability
  that the trajectory leaves the dominant choice there for the first time, ||K_{g,i} D_{<g} psi||^2;
  the shots are split exactly over {no deviation, first deviation at (g, i)} by one multinomial; every
  group that deviated costs one pass, which continues from (g, i) and yields the probabilities of the
  next deviation, and so on. No proposal is rejected. Because every probability is computed and not
  bounded, the block may hold any number of noisy gates (no oversampling ceiling).

At the end each leaf state is measured. ``exact`` gives the measurement distribution of the noisy
circuit from its density matrix, to check both samplers. Prints JSON lines.

Usage: a15_firstjump_ref.py [--check] (local, CPU)
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from collections import Counter
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import circuits  # noqa: E402
import noise  # noqa: E402
from dryrun import compile_like_simulator  # noqa: E402

from noisecirc import Simulator  # noqa: E402


def apply(psi: np.ndarray, matrix: np.ndarray, targets: tuple[int, ...], n: int) -> np.ndarray:
    """Apply ``matrix`` (bit j of its index = qubit targets[j]) to the state ``psi`` of n qubits (qubit q = bit q)."""
    k = len(targets)
    t = psi.reshape([2] * n)  # axis a is qubit n-1-a
    axes = [n - 1 - q for q in reversed(targets)]  # matrix index bits, most significant first
    m = matrix.reshape([2] * (2 * k))
    out = np.tensordot(m, t, axes=(list(range(k, 2 * k)), axes))
    return np.moveaxis(out, list(range(k)), axes).reshape(-1)


def gate_table(block) -> list[dict]:
    """Per operation of a block: targets, unnormalized Kraus operators, bounds, dominant index."""
    table = []
    for placed in block.operations:
        op = placed.operation
        n_choices = op.stack.shape[0]
        bounds = op.upper_probability_bounds[0][:n_choices]
        kraus = [op.stack[i] * math.sqrt(bounds[i]) for i in range(n_choices)]
        table.append({"targets": tuple(int(q) for q in placed.targets), "kraus": kraus, "bounds": bounds,
                      "dom": int(op.choice_of_code[op.dominant_code])})
    return table


def proposals(blocks, psi0, shots, n, rng):
    """noisecirc's scheme; returns leaves [(state, shots)] and the passes."""
    passes = 0
    checkpoints = [(psi0, shots)]
    for block in blocks:
        table = gate_table(block)
        new = Counter()
        states = {}
        for ci, (psi, count) in enumerate(checkpoints):
            cache = {}
            remaining = count
            while remaining:
                draws = np.stack([rng.choice(len(g["bounds"]), size=remaining, p=g["bounds"] / g["bounds"].sum())
                                  for g in table])
                rows, counts = np.unique(draws, axis=1, return_counts=True)
                paths = {tuple(int(x) for x in rows[:, j]): int(counts[j]) for j in range(rows.shape[1])}
                remaining = 0
                for path, k in paths.items():
                    if path not in cache:
                        phi = psi
                        for g, i in zip(table, path):
                            phi = apply(phi, g["kraus"][i] / math.sqrt(g["bounds"][i]), g["targets"], n)
                        cache[path] = phi
                        passes += 1
                    phi = cache[path]
                    accepted = rng.binomial(k, min(1.0, float(np.vdot(phi, phi).real)))
                    if accepted:
                        new[(ci, path)] += accepted
                        states[(ci, path)] = phi / np.linalg.norm(phi)
                    remaining += k - accepted
        checkpoints = [(states[key], k) for key, k in new.items()]
    return checkpoints, passes


def first_jump(blocks, psi0, shots, n, rng):
    """First-jump sampling; returns leaves [(state, shots)] and the passes."""
    passes = 0
    checkpoints = [(psi0, shots)]
    for block in blocks:
        table = gate_table(block)
        leaves = []
        for psi, count in checkpoints:
            # Work items: (state before gate `start`, unnormalized; first gate to continue from; shots).
            stack = [(psi, 0, count)]
            while stack:
                phi, start, k = stack.pop()
                passes += 1  # one pass of this trajectory through the block
                # Along the dominant continuation from `start`, collect the probabilities of the first deviation.
                outcomes, probs = [], []
                for gi in range(start, len(table)):
                    g = table[gi]
                    for i, kraus in enumerate(g["kraus"]):
                        if i != g["dom"]:
                            dev = apply(phi, kraus, g["targets"], n)
                            w = float(np.vdot(dev, dev).real)
                            if w > 0:
                                outcomes.append((gi, dev))
                                probs.append(w)
                    phi = apply(phi, g["kraus"][g["dom"]], g["targets"], n)
                norm0 = float(np.vdot(phi, phi).real)
                total = norm0 + sum(probs)
                p = np.array([norm0, *probs]) / total
                draws = rng.multinomial(k, p)
                if draws[0]:
                    leaves.append((phi / math.sqrt(norm0), int(draws[0])))
                for (gi, dev), d in zip(outcomes, draws[1:]):
                    if d:
                        stack.append((dev / np.linalg.norm(dev), gi + 1, int(d)))
        # Leaves with equal states (same path) are already merged per draw; distinct paths stay apart.
        checkpoints = leaves
    return checkpoints, passes


def measure(leaves, rng, n) -> Counter:
    out = Counter()
    for psi, k in leaves:
        p = np.abs(psi) ** 2
        for x, c in enumerate(rng.multinomial(k, p / p.sum())):
            if c:
                out[x] += int(c)
    return out


def exact(blocks, n) -> np.ndarray:
    """Measurement distribution of the noisy circuit (density matrix)."""
    rho = np.zeros((2**n, 2**n), dtype=complex)
    rho[0, 0] = 1
    for block in blocks:
        for g in gate_table(block):
            new = np.zeros_like(rho)
            for kraus in g["kraus"]:
                left = np.stack([apply(col, kraus, g["targets"], n) for col in rho.T], axis=1)
                new += np.stack([apply(row.conj(), kraus, g["targets"], n) for row in left], axis=0).conj()
            rho = new
    return np.real(np.diag(rho))


def compiled_blocks(name: str, n: int, load: float, ceiling: bool, width: int):
    qc = circuits.make(name, n)
    c = circuits.channels(qc)
    p = 2 * load / c
    options = {"max_fused_qudits": width} if ceiling else {"max_fused_qudits": width, "max_oversampling": math.inf}
    compiled, _, _ = compile_like_simulator(qc, Simulator(maps=noise.maps("damping", p), **options))
    return compiled.blocks, p


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="exactness check on 6 qubits")
    args = parser.parse_args()
    rng = np.random.default_rng(7)
    if args.check:
        n, shots = 6, 200000
        for name in ("brickwork", "ghz"):
            for load in (0.3, 2.0):
                blocks, p = compiled_blocks(name, n, load, True, 2)
                ref = exact(blocks, n)
                psi0 = np.zeros(2**n, dtype=complex)
                psi0[0] = 1
                for label, fn in (("proposals", proposals), ("first_jump", first_jump)):
                    leaves, passes = fn(blocks, psi0, shots, n, rng)
                    counts = measure(leaves, rng, n)
                    freq = np.array([counts.get(x, 0) for x in range(2**n)]) / shots
                    tvd = 0.5 * np.abs(freq - ref).sum()
                    # Expected TVD of an exact sampler at this many shots, by simulation from ref.
                    sim = rng.multinomial(shots, ref, size=20) / shots
                    expected = float(np.mean(0.5 * np.abs(sim - ref).sum(axis=1)))
                    chi2 = float(((freq - ref) ** 2 * shots / np.maximum(ref, 1e-12))[ref > 1e-9].sum())
                    print(json.dumps({"check": True, "circuit": name, "n": n, "load": load, "p": p, "sampler": label,
                                      "blocks": len(blocks), "tvd": tvd, "tvd_expected": expected, "chi2": chi2,
                                      "dof": int((ref > 1e-9).sum() - 1), "passes": passes}), flush=True)
        return
    n, shots = 10, 1000
    for name in ("ghz", "brickwork", "qft", "qaoa"):
        for load in (0.1, 1.0, 3.0):
            psi0 = np.zeros(2**n, dtype=complex)
            psi0[0] = 1
            row = {"circuit": name, "n": n, "shots": shots, "load": load}
            for label, fn, ceiling in (("proposals", proposals, True), ("first_jump", first_jump, True),
                                       ("first_jump_no_ceiling", first_jump, False)):
                blocks, p = compiled_blocks(name, n, load, ceiling, 4)
                _, passes = fn(blocks, psi0, shots, n, rng)
                row[label] = {"passes": passes, "blocks": len(blocks)}
            row["p"] = p
            print(json.dumps(row), flush=True)


if __name__ == "__main__":
    main()
