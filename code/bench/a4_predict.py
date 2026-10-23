"""A4: predicted work of the benchmark candidates, by dry run, without running them.

Per circuit category, noise type and target noise load M (expected accepted errors per shot), the
strength p is chosen as p = M / ((mu/p) C), with mu/p of the noise type (a4_noise_table.py, at
maximally mixed input) and C the circuit's gate-qubit channels. Prints JSON lines with the dry run's
diagnostics (mean of 3 seeds).

Usage: python a4_predict.py NOISE [--qubits 28] [--shots 1000] [--circuits ...]
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import circuits  # noqa: E402
import dryrun  # noqa: E402
import noise  # noqa: E402

MU_PER_P = {"damping": 0.5, "thermal": 0.75, "gad": 0.5, "dephasing": 0.25, "depolarizing": 1.0}
KEYS = ("block_passes", "dominant_passes", "general_passes", "proposals", "unique_simulations", "batches",
        "blocks", "expected_oversampling")

parser = argparse.ArgumentParser()
parser.add_argument("noise")
parser.add_argument("--qubits", type=int, default=28)
parser.add_argument("--shots", default="1000")
parser.add_argument("--circuits", default="ghz,brickwork,grid,qft,qaoa,scramble,random")
parser.add_argument("--loads", default="0.01,0.1,1,10")
parser.add_argument("--optimize-kraus", action="store_true")
args = parser.parse_args()
for name in args.circuits.split(","):
    qc = circuits.make(name, args.qubits)
    c = circuits.channels(qc)
    for load in [float(x) for x in args.loads.split(",")]:
        p = load / (MU_PER_P[args.noise] * c)
        if p >= 0.2:
            continue
        maps = noise.maps(args.noise, p)
        for shots in [int(s) for s in args.shots.split(",")]:
            options = {"optimize_kraus": True} if args.optimize_kraus else {}
            runs = [dryrun.predict(qc, maps, shots, seed=s, **options) for s in range(3)]
            print(json.dumps({"circuit": name, "n": args.qubits, "gates": len(qc.data), "channels": c,
                              "noise": args.noise, "optimize_kraus": args.optimize_kraus, "load": load, "p": p,
                              "shots": shots, **{k: float(np.mean([r[k] for r in runs])) for k in KEYS}}),
                  flush=True)
