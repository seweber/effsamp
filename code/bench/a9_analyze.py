"""A9: cuStateVec Ex (delayed lower-bound sampling, one trajectory per shot) against noisecirc and A6's simulators.

Reads the A9 runs (a9_custatevec.py, default fusion) and the A6 table (a6_analyze.py output, 24
qubits, damping, 1000 shots), and prints per circuit and load: the times for 1000 shots, noisecirc's
speedups, and passes per shot: cuStateVec Ex's effective passes (its time per shot over t_bw),
noisecirc's passes per shot without sharing (variant pershot) and with it (default). Writes
OUT_PREFIX.svg/.png.

Usage: a9_analyze.py OUT_PREFIX A6_TABLE.jsonl A9_DIR...
"""

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

T_BW_24 = 0.155e-3
COLORS = {"noisecirc": "#4C72B0", "custatevec_ex": "#55A868", "aer_branch": "#DD8452", "cudaq": "#8172B3"}
LABELS = {"noisecirc": "noisecirc", "custatevec_ex": "cuStateVec Ex (lower bounds, per shot)",
          "aer_branch": "Aer, shot branching", "cudaq": "CUDA-Q"}


def main():
    prefix, table_path, dirs = sys.argv[1], sys.argv[2], sys.argv[3:]
    table = {(r["circuit"], round(r["p"], 9)): r for r in map(json.loads, Path(table_path).read_text().splitlines())}
    cusv = {}
    for d in dirs:
        for line in (Path(d) / "stdout.txt").read_text().splitlines():
            if line.startswith("{"):
                r = json.loads(line)
                if r.get("kind") == "run" and r.get("dense_fusion") is None and r["n"] == 24:
                    cusv[(r["circuit"], round(r["p"], 9))] = r["time"] * 1000 / r["shots"]
    rows = []
    for key, t in sorted(cusv.items()):
        a6 = table.get(key)
        if a6 is None:
            continue
        row = {"circuit": key[0], "p": key[1], "M": a6["M"], "T_custatevec_ex": t, "T_noisecirc": a6["T_noisecirc"],
               "T_aer_branch": a6.get("T_aer_branch"), "T_cudaq": a6.get("T_cudaq"),
               "cusv_passes_per_shot": t / 1000 / T_BW_24,
               "nc_pershot_passes_per_shot": a6["P_nc_pershot"] / 1000, "nc_passes_per_shot": a6["P_noisecirc"] / 1000,
               "gates": a6.get("gates")}
        row["speedup"] = t / a6["T_noisecirc"]
        rows.append(row)
        print(json.dumps(row))
    names = [c for c in ("ghz", "brickwork", "qft", "qaoa") if any(r["circuit"] == c for r in rows)]
    fig, axes = plt.subplots(1, len(names), figsize=(2.7 * len(names) + 2.4, 3.0), sharey=True, squeeze=False)
    for ax, c, label in zip(axes[0], names, "abcd"):
        rs = sorted((r for r in rows if r["circuit"] == c), key=lambda r: r["M"])
        for sim, color in COLORS.items():
            pts = [(r["M"], r[f"T_{sim}"]) for r in rs if r.get(f"T_{sim}")]
            if pts:
                ax.plot(*zip(*pts), "o-", ms=3.5, color=color, label=LABELS[sim])
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_title(c, fontsize=9)
        ax.set_xlabel("$M$" if label != "b" else "$M$ (expected damping events per shot)")
        ax.text(-0.02, 1.02, f"({label})", transform=ax.transAxes, fontsize=9, ha="right", va="bottom")
    axes[0, 0].set_ylabel("time for 1000 shots (s)")
    axes[0, -1].legend(fontsize=7, frameon=False, loc="upper left", bbox_to_anchor=(1.03, 1.0))
    fig.tight_layout()
    fig.savefig(prefix + ".svg")
    fig.savefig(prefix + ".png", dpi=110)


if __name__ == "__main__":
    main()
