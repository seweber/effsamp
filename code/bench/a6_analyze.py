"""A6: noisecirc against Aer and CUDA-Q, in time and in passes over the state vector.

Reads the A6 runs (a6_runs.py, a2_runs.py for noisecirc, a6_variants.py), scales every time to 1000
shots (per-shot simulators ran 100 shots; their time is linear in the shots), counts Aer's passes
with aer_dryrun.py, and prints one JSON line per (circuit, load) with every simulator's time, passes
and efficiency T / (P t_bw). Writes OUT_PREFIX-speedup.svg and OUT_PREFIX-passes.svg.

Usage: python a6_analyze.py OUT_PREFIX DATA_DIR...
"""
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import aer_dryrun  # noqa: E402
import circuits  # noqa: E402

T_BW_24 = 0.155e-3  # s, one complex64 state of 24 qubits read and written (A2)
SHOTS = 1000


def load(dirs):
    runs = defaultdict(list)  # (sim, circuit, p) -> rows
    for d in dirs:
        path = Path(d) / "stdout.txt"
        if not path.exists():
            continue
        for line in path.read_text().splitlines():
            if not line.startswith("{"):
                continue
            r = json.loads(line)
            if r.get("kind") == "run" and "sim" in r:
                sim = r["sim"]
            elif r.get("kind") == "run":
                sim = "noisecirc"
            elif r.get("kind") == "variant":
                sim = "nc_" + r["variant"]
            else:
                continue
            if r.get("n", 24) != 24:
                continue
            runs[(sim, r["circuit"], round(r["p"], 9))].append(r)
    return runs


def main():
    prefix, dirs = sys.argv[1], sys.argv[2:]
    runs = load(dirs)
    points = sorted({(c, p) for (_, c, p) in runs})
    table = []
    for c, p in points:
        qc = circuits.make(c, 24)
        load_m = p * circuits.channels(qc) / 2
        row = {"circuit": c, "p": p, "M": round(load_m, 4)}
        for (sim, cc, pp), rs in runs.items():
            if cc != c or pp != p:
                continue
            times = [r["time"] * SHOTS / r["shots"] for r in rs]
            row[f"T_{sim}"] = float(np.median(times))
            if "block_passes" in rs[0]:
                row[f"P_{sim}"] = float(np.mean([r["block_passes"] * SHOTS / r["shots"] for r in rs]))
            meta = rs[0].get("metadata") or {}
            if "fusion_allow_kraus" in meta:
                row[f"kraus_fusion_{sim}"] = meta["fusion_allow_kraus"]
        if not any(k.startswith("T_aer") for k in row):
            continue
        for mode in ("plain", "branch"):
            # Count with the fusion the GPU run used; Aer falls back to no Kraus fusion after heevx.
            allow = row.get(f"kraus_fusion_aer_{mode}", True) is not False
            try:
                counted = aer_dryrun.count(qc, "damping", p, SHOTS, mode, allow_kraus=allow)
            except RuntimeError:
                # The local Aer cannot fuse this point; counted unfused, and the row says so.
                print(f"local Kraus fusion failed: {c} p={p} {mode}", file=sys.stderr)
                allow = False
                counted = aer_dryrun.count(qc, "damping", p, SHOTS, mode, allow_kraus=False)
            row[f"aer_kraus_fusion_{mode}"] = allow
            row[f"P_aer_{mode}"] = counted["passes"]
            row[f"aer_ops_{mode}"] = counted["ops"]
        for sim in ("noisecirc", "aer_plain", "aer_branch", "nc_k2", "nc_pershot", "nc_pershot_k2"):
            if f"T_{sim}" in row and f"P_{sim}" in row:
                row[f"eff_{sim}"] = row[f"T_{sim}"] / (row[f"P_{sim}"] * T_BW_24)
        table.append(row)
        print(json.dumps(row), flush=True)

    sims = [("aer_branch", "Aer, shot branching", "#DD8452"), ("aer_batched", "Aer, batched shots", "#C44E52"),
            ("aer_plain", "Aer, per shot", "#8172B3"), ("cudaq", "CUDA-Q", "#55A868")]
    names = [c for c in ("ghz", "brickwork", "qft", "qaoa") if any(r["circuit"] == c for r in table)]
    fig, axes = plt.subplots(1, len(names), figsize=(2.6 * len(names) + 0.6, 3.0), sharey=True, squeeze=False)
    for ax, c, label in zip(axes[0], names, "abcd"):
        rows = sorted((r for r in table if r["circuit"] == c), key=lambda r: r["M"])
        for sim, title, color in sims:
            pts = [(r["M"], r[f"T_{sim}"] / r["T_noisecirc"]) for r in rows if f"T_{sim}" in r and "T_noisecirc" in r]
            if pts:
                ax.plot(*zip(*pts), "o-", ms=3.5, color=color, label=title)
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_title(c, fontsize=9)
        ax.set_xlabel("$M$ (expected damping events per shot)" if label == "b" else "$M$")
        ax.axhline(1, color="k", lw=0.6)
        ax.text(-0.02, 1.02, f"({label})", transform=ax.transAxes, fontsize=9, ha="right", va="bottom")
    axes[0, 0].set_ylabel("time / noisecirc's time")
    axes[0, -1].legend(fontsize=6.5, frameon=False, loc="lower left")
    fig.tight_layout()
    fig.savefig(prefix + "-speedup.svg")
    fig.savefig(prefix + "-speedup.png", dpi=110)


if __name__ == "__main__":
    main()
