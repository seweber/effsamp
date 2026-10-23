"""A2: plot block pass times over the bandwidth time, against the gates per block.

Usage: python a2_plot_blocks.py OUT.svg DATA_DIR...  (stdout.txt of a2_blocks.py runs)
"""

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

COLORS = {"ghz": "#4C72B0", "brickwork": "#DD8452", "qft": "#55A868", "random": "#C44E52", "grid": "#8172B3",
          "qaoa": "#937860"}


def load(dirs):
    blocks, summaries = [], []
    for d in dirs:
        for line in (Path(d) / "stdout.txt").read_text().splitlines():
            if not line.startswith("{"):
                continue
            row = json.loads(line)
            (blocks if row["kind"] == "block" else summaries).append(row)
    return blocks, summaries


def main():
    out, dirs = sys.argv[1], sys.argv[2:]
    blocks, summaries = load(dirs)
    t_bw = {(s["n"]): s["t_cupy"] for s in summaries}
    ns = sorted(t_bw)
    fig, axes = plt.subplots(2, len(ns), figsize=(3.2 * len(ns), 5.6), sharex=True, sharey="row", squeeze=False)
    for j, n in enumerate(ns):
        for i, key in enumerate(("t_dom", "t_gen")):
            ax = axes[i, j]
            for circuit, color in COLORS.items():
                rows = [b for b in blocks if b["n"] == n and b["circuit"] == circuit and b[key] is not None]
                if rows:
                    ax.scatter([b["ops"] for b in rows], [b[key] / t_bw[n] for b in rows], s=9, color=color,
                               label=circuit, alpha=0.75, linewidths=0)
            ax.axhline(1.0, color="k", lw=0.8)
            ax.axhline(1.5, color="k", lw=0.8, ls="--")
            ax.set_yscale("log")
            ax.set_ylim(0.7, 12)
            if i == 0:
                ax.set_title(f"n = {n}  ($t_{{bw}}$ = {t_bw[n] * 1e3:.2f} ms)", fontsize=9)
            if i == 1:
                ax.set_xlabel("gates per block")
            if j == 0:
                ax.set_ylabel(("no-error kernel" if key == "t_dom" else "general kernel") + "\npass time / $t_{bw}$")
    axes[0, 0].legend(fontsize=7, loc="upper left", ncol=2, frameon=False)
    for ax, label in zip(axes.flat, "abcdef"):
        ax.text(-0.02, 1.02, f"({label})", transform=ax.transAxes, fontsize=9, ha="right", va="bottom")
    fig.tight_layout()
    fig.savefig(out)
    fig.savefig(str(out).rsplit(".", 1)[0] + ".png", dpi=110)
    # summary table to stdout
    for s in summaries:
        print(f"{s['circuit']:10s} n={s['n']} blocks={s['blocks']:4d} mean_dom/bw={s['sum_dom'] / s['blocks'] / s['t_cupy']:.2f}"
              f" mean_gen/bw={s['sum_gen'] / s['blocks'] / s['t_cupy']:.2f} floor/bw={s['t_floor'] / s['t_cupy']:.2f}")


if __name__ == "__main__":
    main()
