"""A4: per-channel oversampling and error rates of each noise type, from noisecirc's operation tables.

For an ``r`` gate followed by the channel, at strength p: Z - 1 (error proposals per shot and
channel in exact mode), mu (accepted errors per shot and channel, maximally mixed input), the
number of Kraus operators noisecirc keeps (choices), and both with ``optimize_kraus``.
"""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import noise  # noqa: E402
from noisecirc.block.operation import Operation  # noqa: E402

for kind in ("damping", "gad", "thermal", "dephasing", "depolarizing"):
    for p in (1e-4, 1e-3, 1e-2):
        for optimize in (False, True):
            op = Operation.from_map(noise.maps(kind, p)["r"], (0.7, 0.3), optimize)
            z = float(np.exp(op.log_oversampling[0]))
            m = op.stack
            dom = op.choice_of_code[op.dominant_code]
            acc = np.einsum("kij,kij->k", m.conj(), m).real / 2  # surrogate acceptance per choice
            bounds = op.upper_probability_bounds[0]
            probs = bounds[bounds > 0] / bounds.sum()
            mu = float(sum(probs[k] * acc[k] for k in range(len(probs)) if k != dom) * z)
            print(json.dumps({"noise": kind, "p": p, "optimize_kraus": optimize, "choices": int(len(probs)),
                              "Z_minus_1": z - 1, "mu": mu, "accepted_fraction": mu / (z - 1) if z > 1 else None}))
