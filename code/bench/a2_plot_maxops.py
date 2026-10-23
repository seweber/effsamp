"""A2: wall time and T/(P t_bw) against max_operations at n=26 (a2_runs.py with --option max_operations=m).

Usage: python a2_plot_maxops.py OUT.svg DIR...
"""
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).parent))
import summarize_runs  # noqa: E402

COLORS = {"ghz": "#4C72B0", "brickwork": "#DD8452", "qft": "#55A868", "grid": "#8172B3", "qaoa": "#937860"}
out, dirs = sys.argv[1], sys.argv[2:]
pts = summarize_runs.points(summarize_runs.load(dirs))
fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.0))
for c, color in COLORS.items():
    for p, ls in ((1e-3, "-"), (1e-2, "--")):
        r = sorted((x["options"]["max_operations"], x) for x in pts if x["circuit"] == c and x["p"] == p)
        if not r:
            continue
        base = dict(r)[128]["time"]
        axes[0].plot([m for m, _ in r], [x["time"] / base for _, x in r], ls, marker="o", ms=3, color=color)
        axes[1].plot([m for m, _ in r], [x["time"] / (x["block_passes"] * x["t_bw"]) for _, x in r], ls, marker="o",
                     ms=3, color=color)
for ax in axes:
    ax.set_xscale("log", base=2)
    ax.set_xticks([32, 48, 64, 128], ["32", "48", "64", "128"])
    ax.minorticks_off()
    ax.set_xlabel("max_operations")
axes[0].set_ylabel("wall time / wall time at 128")
axes[1].set_ylabel("measured time / (passes × $t_{bw}$)")
axes[1].axhline(1.5, color="k", lw=0.6, ls=":")
handles = [plt.Line2D([], [], color=c, marker="o", ls="", ms=4, label=k) for k, c in COLORS.items()]
handles += [plt.Line2D([], [], color="gray", ls=ls, label=f"p = {p:g}") for p, ls in ((1e-3, "-"), (1e-2, "--"))]
axes[0].legend(handles=handles, fontsize=6.5, frameon=False, ncol=2, loc="upper right")
for ax, label in zip(axes, "ab"):
    ax.text(-0.02, 1.02, f"({label})", transform=ax.transAxes, fontsize=9, ha="right", va="bottom")
fig.tight_layout()
fig.savefig(out)
fig.savefig(out.rsplit(".", 1)[0] + ".png", dpi=110)
