"""A3: plots of the dry-run sweeps.

Usage: python a3_plot.py SWEEP OUT.svg DATA_DIR
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
LABEL = dict(fontsize=9, ha="right", va="bottom")


def rows(d):
    return [json.loads(x) for x in (Path(d) / "stdout.txt").read_text().splitlines() if x.startswith("{")]


def panel_label(ax, label):
    ax.text(-0.02, 1.02, f"({label})", transform=ax.transAxes, **LABEL)


def fusion(data, out):
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.0), sharey=True)
    for c, color in COLORS.items():
        r = [x for x in data if x["circuit"] == c and x["p"] == 0.0]
        k = sorted((x["max_fused_qudits"], x["blocks"]) for x in r if x["max_operations"] == 128)
        m = sorted((x["max_operations"], x["blocks"]) for x in r if x["max_fused_qudits"] == 9)
        gates = r[0]["gates"]
        axes[0].plot([a for a, _ in k], [b / gates for _, b in k], "o-", ms=3, color=color, label=c)
        axes[1].plot([a for a, _ in m], [b / gates for _, b in m], "o-", ms=3, color=color, label=c)
    axes[0].set_xlabel("max_fused_qudits $k$ (besides 3 pinned)")
    axes[1].set_xlabel("max_operations")
    axes[1].set_xscale("log", base=2)
    axes[0].set_ylabel("blocks per gate")
    axes[0].set_yscale("log")
    axes[0].legend(fontsize=7, frameon=False)
    for ax, label in zip(axes, "ab"):
        panel_label(ax, label)
    fig.tight_layout()
    return fig


def noise_sweep(data, out):
    names = [c for c in COLORS if any(x["circuit"] == c for x in data)]
    fig, axes = plt.subplots(1, len(names), figsize=(2.4 * len(names), 2.9), sharey=True, squeeze=False)
    for ax, c, label in zip(axes[0], names, "abcdef"):
        for shots, ls in ((100, ":"), (1000, "-"), (10000, "--")):
            r = sorted((x["p"], x["block_passes"] / (x["blocks"] * shots), x) for x in data
                       if x["circuit"] == c and x["shots"] == shots)
            ax.plot([p for p, _, _ in r], [v for _, v, _ in r], ls, marker="o", ms=3, color=COLORS[c],
                    label=f"{shots} shots")
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_title(c, fontsize=9)
        ax.set_xlabel("damping $p$")
        panel_label(ax, label)
    axes[0, 0].set_ylabel("block passes / (blocks × shots)")
    axes[0, 0].legend(fontsize=7, frameon=False)
    fig.tight_layout()
    return fig


if __name__ == "__main__":
    sweep, out, d = sys.argv[1:4]
    data = rows(d)
    fig = {"fusion": fusion, "noise": noise_sweep}[sweep](data, out)
    fig.savefig(out)
    fig.savefig(out.rsplit(".", 1)[0] + ".png", dpi=110)
