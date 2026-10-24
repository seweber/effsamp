"""A12: E and mu of noisecirc's Kraus sets (canonical, optimize_kraus of bench/fixes) against the optimum and its lower bound.

For single-qubit channels and their two-qubit tensor squares (the noise after a two-qubit gate), at
strength p: the canonical set, noisecirc's `optimize_kraus` (branch bench/fixes, which keeps the
dominant operator first), and a12_kraus.optimize at weight w (E + w mu), with lower_bound. Prints JSON.
Usage: a12_compare.py [p]
"""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from a12_kraus import canonical, channel, lower_bound, metrics, optimize, tensor  # noqa: E402

from noisecirc.twirling.kraus_optimization import optimize_kraus  # noqa: E402

p = float(sys.argv[1]) if len(sys.argv) > 1 else 1e-2
kinds = sys.argv[2].split(",") if len(sys.argv) > 2 else ["damping", "dephasing", "depolarizing", "gad", "thermal", "damp_depol", "damp_overrot"]
for kind in kinds:
    single = channel(kind, p)
    for width, kraus in ((1, single), (2, tensor(single, single))):
        can = canonical(kraus)
        nc = np.asarray(optimize_kraus(list(can)))
        w = 5.0
        opt, _ = optimize(kraus, w, starts=3 if width == 2 else 6)
        lb = lower_bound(kraus, w, starts=3 if width == 2 else 6)
        row = {"kind": kind, "p": p, "width": width}
        for label, ops in (("canonical", can), ("optimize_kraus", nc), ("optimum", opt)):
            m = metrics(ops)
            row[label] = {"E_over_p": m["E"] / p, "mu_over_p": m["mu"] / p, "Z_minus_1_over_p": (m["Z"] - 1) / p, "n": m["n"]}
        row["bound"] = {"J_over_p": lb["J"] / p, "E_over_p": lb["E_bound"] / p, "mu_over_p": lb["mu"] / p, "w": w}
        print(json.dumps(row), flush=True)
