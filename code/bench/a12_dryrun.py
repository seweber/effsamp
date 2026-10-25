"""A12: block passes of the benchmark circuits with canonical, noisecirc-optimized and optimal Kraus sets (dry run).

Two Kraus sets per noisy gate, for each noise kind:
- canonical: noisecirc's default (Choi eigenvectors);
- optimum: the canonical dominant operator and the remaining operators mixed to minimize their
  oversampling (a12_kraus.optimize_residual), computed once per noise kind and strength (two-qubit
  gates: its tensor square) and multiplied by each gate's unitary (E and mu do not change under
  L -> L U). It reaches the lower bound of a12_kraus.lower_bound within 0.6% for all channels tested.
- sequential: the remaining operators mixed to minimize the distinct proposals and accepted errors
  of n shots, P_n + A_n at n p = 1 (a12_collisions.mix_residual, started from the optimum); this
  keeps the minimal oversampling and concentrates it on the first remaining operators.
For the optimum, noisecirc's decomposition is bypassed: with optimize_kraus=True, `sta_sectors` is
replaced (qubits only, one sector) by one returning the given operators, so that the map's own
Kraus operators are used as they are. Prints one JSON line per circuit, noise, load and set.

Usage: a12_dryrun.py kinds circuits [sets] [shots] (local, CPU; n = 28, M = 0.1 and 1; default sets
canonical,optimum and 1000 shots)
"""
import json
import sys
from functools import cache
from itertools import product
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import circuits  # noqa: E402
import dryrun  # noqa: E402
import noise  # noqa: E402
from a12_kraus import canonical, channel, metrics, optimize_residual, tensor  # noqa: E402

import noisecirc.block.operation as operation_module  # noqa: E402
from noisecirc import Simulator  # noqa: E402

_original = operation_module.sta_sectors


def sta_as_given(channel_ops, branches, tol=1e-12, optimize=False):
    """`sta_sectors` that returns the map's operators unchanged (qubit maps, one sector) when optimizing."""
    if not optimize:
        return _original(channel_ops, branches=branches, tol=tol, optimize=False)
    ops = [np.asarray(op.full() if hasattr(op, "full") else op) for op in channel_ops]
    width = int(round(np.log2(ops[0].shape[0])))
    zero = (0,) * width
    return {(zero, zero): [op for op in ops if np.linalg.norm(op) > tol]}


@cache
def optimal_noise(kind: str, p: float, width: int, label: str = "optimum") -> tuple[np.ndarray, ...]:
    """The optimal one-qubit set; for two qubits its tensor square, which is within 0.6% of the
    two-qubit lower bound for all channels of a12_compare (a direct two-qubit optimization takes
    about 40 s per strength). With label "sequential", the set of a12_collisions at n p = 1, w = 1."""
    ops, _ = optimize_residual(channel(kind, p), starts=24)
    if label == "sequential":
        from a12_collisions import mix_residual, params_of

        n = 1.0 / p
        start = params_of(canonical(channel(kind, p)), ops)
        ops = mix_residual(canonical(channel(kind, p)), lambda b: 1 - np.exp(-n * b), lambda b: n * np.exp(-n * b),
                           starts=24, x0s=(start,), w=1.0)
    return tuple(ops) if width == 1 else tuple(np.kron(a, b) for a in ops for b in ops)


def optimal_maps(kind: str, p: float, label: str = "optimum") -> dict:
    import qutip as qt

    from noisecirc.maps import DEFAULT_MAPS, QuantumMap, qubit_restricted_maps

    ideal = qubit_restricted_maps(DEFAULT_MAPS)
    out = {}
    for name, ideal_map in ideal.items():
        width = ideal_map.num_qudits

        def chan(*params, ideal_map=ideal_map, width=width):
            if width > 2:
                raise ValueError("only one- and two-qubit gates")
            ops = optimal_noise(kind, p, width, label)
            unitary = ideal_map.channel(params)
            return [qt.Qobj(op, dims=unitary.dims) @ unitary for op in ops]

        out[name] = QuantumMap(width, chan, branches=ideal_map.branches, tol=ideal_map.tol)
    return out


def main():
    kinds = sys.argv[1].split(",")
    names = sys.argv[2].split(",")
    labels = sys.argv[3].split(",") if len(sys.argv) > 3 else ["canonical", "optimum"]
    shots = int(sys.argv[4]) if len(sys.argv) > 4 else 1000
    for name, kind in product(names, kinds):
        qc = circuits.make(name, 28)
        c = circuits.channels(qc)
        for load in (0.1, 1.0):
            # Strength such that a damping-like channel gives `load` accepted errors per shot; for every
            # kind the same p, the loads then differ by the kinds' mu/p (reported).
            p = 2 * load / c
            # optimize_kraus is left out: it re-optimizes every distinct gate (hundreds of random angles,
            # up to 20 s each for two-qubit sets) and is within 1% of the optimum per gate (a12_compare).
            for label in labels:
                operation_module.sta_sectors = sta_as_given if label != "canonical" else _original
                maps = optimal_maps(kind, p, label) if label != "canonical" else noise.maps(kind, p)
                opt = label != "canonical"
                runs = [dryrun.predict(qc, maps, shots, seed=s, optimize_kraus=opt) for s in (1, 2, 3)]
                row = {"circuit": name, "noise": kind, "load": load, "p": p, "set": label, "shots": shots,
                       "passes": float(np.mean([r["block_passes"] for r in runs])),
                       "general": float(np.mean([r.get("general_passes", np.nan) for r in runs])),
                       "blocks": runs[0].get("blocks")}
                print(json.dumps(row), flush=True)
    operation_module.sta_sectors = _original


if __name__ == "__main__":
    main()
