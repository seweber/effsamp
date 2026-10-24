"""A12: end-to-end times and passes with canonical and optimal Kraus sets (data/*-a12-end-to-end-*), medians over seeds."""
import glob, json, re
from collections import defaultdict
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[2]
t, P = defaultdict(list), {}
for run in glob.glob(str(ROOT / "data" / "*-a12-end-to-end-*")):
    for line in open(Path(run) / "stdout.txt"):
        r = json.loads(line)
        if r.get("kind") == "run":
            key = (r["noise"], r["circuit"], r["p"], r["kraus_set"])
            t[key].append(r["time"]); P[key] = r["block_passes"]
for key in sorted({k[:3] for k in t}):
    a, b = np.median(t[(*key, "canonical")]), np.median(t[(*key, "optimum")])
    print(f"{key[0]:13s} {key[1]:10s} p={key[2]:.3g}: time {a:6.2f} -> {b:6.2f} s ({a/b:.2f}x)  passes {P[(*key,'canonical')]:.0f} -> {P[(*key,'optimum')]:.0f} ({P[(*key,'canonical')]/P[(*key,'optimum')]:.2f}x)")
