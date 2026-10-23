"""A4: predicted block passes against the fusion width, at fixed noise loads (dry run, n=28, damping).

Usage: python a4_fusion.py [circuits]
"""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import circuits  # noqa: E402
import dryrun  # noqa: E402
import noise  # noqa: E402

names = sys.argv[1].split(",") if len(sys.argv) > 1 else ["ghz", "brickwork", "grid", "qft", "qaoa", "scramble"]
for name in names:
    qc = circuits.make(name, 28)
    c = circuits.channels(qc)
    for load in (0.0, 0.1, 1.0):
        p = load / (0.5 * c)
        maps = noise.maps("damping" if p else None, p)
        for k in (3, 5, 7, 9):
            runs = [dryrun.predict(qc, maps, 1000, seed=s, max_fused_qudits=k) for s in range(2 if p else 1)]
            print(json.dumps({"circuit": name, "load": load, "p": p, "max_fused_qudits": k, "gates": len(qc.data),
                              **{key: float(np.mean([r[key] for r in runs])) for key in
                                 ("blocks", "block_passes", "general_passes", "blocks_per_segment")}}), flush=True)
