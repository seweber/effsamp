"""A15: estimated saving of peeling the last block (dry run).

Peeling samples the qubits outside the last block's tile from the marginal of each checkpoint that
enters the last block, then simulates the last block on the 2^|tile| slice of each sampled outcome
(cheap, ~1e-4 of a pass at 28 qubits) with exact jump probabilities. It removes the last block's
passes (dominant and error) and costs one read of each entering checkpoint (half a pass) for the
marginal. Saving = last-block passes - 0.5 * entering checkpoints, from the dry run's per-block counts.
Usage: a15_peel.py (local, CPU; damping, n = 28, 1000 shots, M = 0.1 and 1)
"""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import circuits  # noqa: E402
import dryrun  # noqa: E402
import noise  # noqa: E402

for name in ["ghz", "brickwork", "qft", "qaoa", "grid"]:
    qc = circuits.make(name, 28)
    c = circuits.channels(qc)
    for load in (0.1, 1.0):
        maps = noise.maps("damping", 2 * load / c)
        runs = [dryrun.predict(qc, maps, 1000, seed=s) for s in (1, 2, 3)]
        dom = np.mean([r["dom_per_block"] for r in runs], axis=0)
        gen = np.mean([r["gen_per_block"] for r in runs], axis=0)
        total = float(dom.sum() + gen.sum())
        last = float(dom[-1] + gen[-1])
        # Checkpoints entering the last block: its distinct dominant continuations.
        entering = float(dom[-1])
        saving = last - 0.5 * entering
        print(json.dumps({"circuit": name, "load": load, "blocks": len(dom), "passes": total, "last_block": last,
                          "entering": entering, "gain": total / (total - saving)}), flush=True)
