"""Summarize a2_runs.py output: per point, median time, mean work, and the time over block passes x t_bw.

Usage: python summarize_runs.py DATA_DIR...
"""

import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np


def load(dirs):
    rows = []
    for d in dirs:
        path = Path(d) / "stdout.txt"
        if path.exists():
            rows += [json.loads(line) for line in path.read_text().splitlines()
                     if line.startswith("{") and '"kind": "run"' in line]
    return rows


def points(rows):
    groups = defaultdict(list)
    for r in rows:
        groups[(r["circuit"], r["n"], r.get("noise"), r["p"], r["shots"], json.dumps(r.get("options", {})),
                json.dumps(r.get("tunables", [])))].append(r)
    out = []
    for key, rs in groups.items():
        first = rs[0]
        out.append({
            **{k: first[k] for k in ("circuit", "n", "noise", "p", "shots", "blocks", "t_bw", "gates", "channels")},
            "options": first.get("options", {}),
            "tunables": first.get("tunables", []),
            "time": float(np.median([r["time"] for r in rs])),
            "t_first": first["t_first"],
            **{k: float(np.mean([r[k] for r in rs])) for k in (
                "block_passes", "batches", "proposals", "unique_simulations", "expected_oversampling", "checkpoints")},
        })
    return out


if __name__ == "__main__":
    for p in sorted(points(load(sys.argv[1:])), key=lambda x: (x["n"], x["circuit"], x["p"])):
        ratio = p["time"] / (p["block_passes"] * p["t_bw"])
        print(f"{p['circuit']:10s} n={p['n']} p={p['p']:<7g} B={p['blocks']:4d} passes={p['block_passes']:9.0f} "
              f"batches={p['batches']:7.0f} T={p['time']:8.3f}s ratio={ratio:5.2f} first={p['t_first']:6.1f}s")
