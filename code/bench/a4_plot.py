"""A4: figures of the dry-run predictions.

Usage:
  python a4_plot.py noise OUT.svg PRED_DIR...     passes per block and shot against M, a panel per noise type
  python a4_plot.py fusion OUT.svg FUSION_DIR     passes against max_fused_qudits at M = 0, 0.1, 1
"""
import json
import math
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

COLORS = {"ghz": "#4C72B0", "brickwork": "#DD8452", "qft": "#55A868", "random": "#C44E52", "grid": "#8172B3",
          "qaoa": "#937860", "scramble": "#DA8BC3"}
NOISES = ["damping", "thermal", "gad", "dephasing", "depolarizing"]
TITLES = {"damping": "amplitude damping", "thermal": "thermal relaxation", "gad": "generalized damping",
          "dephasing": "dephasing (mixed-unitary)", "depolarizing": "depolarizing (mixed-unitary)"}


def rows(dirs):
    return [json.loads(x) for d in dirs for x in (Path(d) / "stdout.txt").read_text().splitlines() if x.startswith("{")]


def label(ax, text):
    ax.text(-0.02, 1.02, f"({text})", transform=ax.transAxes, fontsize=9, ha="right", va="bottom")


def noise_panels(data):
    fig, axes = plt.subplots(1, 5, figsize=(12.0, 2.9), sharey=True)
    ms = np.logspace(-2.3, 1.3, 100)
    for ax, kind, text in zip(axes, NOISES, "abcde"):
        for c, color in COLORS.items():
            r = sorted((x["load"], x["block_passes"] / (x["blocks"] * x["shots"])) for x in data
                       if x["noise"] == kind and x["circuit"] == c and x["shots"] == 1000)
            if r:
                ax.plot(*zip(*r), "o-", ms=3, lw=0.8, color=color, label=c)
        f = np.array([1 - (1 - math.exp(-m)) / m for m in ms])
        ax.plot(ms, 1e-3 + f, "k:", lw=0.9, label="$1/N + f(M)$")
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_title(TITLES[kind], fontsize=8.5)
        ax.set_xlabel("$M$" if text != "c" else "expected accepted errors per shot $M$")
        label(ax, text)
    axes[0].set_ylabel("passes / (blocks × shots)")
    axes[0].legend(fontsize=6, frameon=False, loc="upper left")
    fig.tight_layout()
    return fig


def fusion_panels(data):
    fig, axes = plt.subplots(1, 3, figsize=(8.4, 2.9), sharey=True)
    for ax, load, text in zip(axes, (0.0, 0.1, 1.0), "abc"):
        for c, color in COLORS.items():
            r = sorted((x["max_fused_qudits"], x["block_passes"]) for x in data if x["circuit"] == c and x["load"] == load)
            if r:
                base = dict(r)[9]
                ax.plot([k for k, _ in r], [v / base for _, v in r], "o-", ms=3, color=color, label=c)
        ax.set_yscale("log")
        ax.set_yticks([1, 2, 3, 4, 6, 8], ["1", "2", "3", "4", "6", "8"])
        ax.minorticks_off()
        ax.set_xticks([3, 5, 7, 9])
        ax.set_title(f"M = {load:g}" + (" (ideal)" if load == 0 else ""), fontsize=9)
        ax.set_xlabel("max_fused_qudits")
        label(ax, text)
    axes[0].set_ylabel("block passes / passes at width 9")
    axes[2].legend(fontsize=6.5, frameon=False, loc="upper right")
    fig.tight_layout()
    return fig


if __name__ == "__main__":
    kind, out, dirs = sys.argv[1], sys.argv[2], sys.argv[3:]
    fig = {"noise": noise_panels, "fusion": fusion_panels}[kind](rows(dirs))
    fig.savefig(out)
    fig.savefig(out.rsplit(".", 1)[0] + ".png", dpi=110)
