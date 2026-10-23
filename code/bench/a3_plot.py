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


def segments(data, out):
    """Block passes against blocks_per_segment and against max_oversampling, relative to noisecirc's defaults."""
    seg = [x for x in data if x.get("sweep") == "segment" and not x.get("skipped")]
    ovs = [x for x in data if x.get("sweep") == "oversampling"]
    fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.0), sharey=True)
    ticks = ["1", "2", "4", "8", "inf"]
    for c, color in COLORS.items():
        for p, ls in ((1e-4, ":"), (1e-3, "-"), (1e-2, "--")):
            base = [x for x in seg if x["circuit"] == c and x["p"] == p and x["blocks_per_segment"] == "1"]
            if not base:
                continue
            r = [(ticks.index(x["blocks_per_segment"]), x["block_passes"] / base[0]["block_passes"]) for x in seg
                 if x["circuit"] == c and x["p"] == p]
            axes[0].plot(*zip(*sorted(r)), ls, marker="o", ms=3, color=color)
            base = [x for x in ovs if x["circuit"] == c and x["p"] == p and x["max_oversampling"].startswith("2.71")]
            r = sorted((float(x["max_oversampling"]) if x["max_oversampling"] != "inf" else 30.0,
                        x["block_passes"] / base[0]["block_passes"]) for x in ovs if x["circuit"] == c and x["p"] == p)
            axes[1].plot(*zip(*r), ls, marker="o", ms=3, color=color)
    axes[0].set_xticks(range(5), ticks)
    axes[0].set_xlabel("blocks_per_segment")
    axes[0].set_ylabel("block passes / passes at default")
    axes[1].set_xscale("log")
    axes[1].set_xticks([1.1, 1.5, 2, np.e, 5, 10, 30], ["1.1", "1.5", "2", "e", "5", "10", "inf"])
    axes[1].minorticks_off()
    axes[1].set_xlabel("max_oversampling")
    axes[0].set_yscale("log")
    handles = [plt.Line2D([], [], color=c, marker="o", ls="", ms=4, label=k) for k, c in COLORS.items()]
    handles += [plt.Line2D([], [], color="gray", ls=ls, label=f"p = {p:g}") for p, ls in
                ((1e-4, ":"), (1e-3, "-"), (1e-2, "--"))]
    axes[1].legend(handles=handles, fontsize=6.5, frameon=False, ncol=2, loc="upper right")
    for ax, label in zip(axes, "ab"):
        panel_label(ax, label)
    fig.tight_layout()
    return fig


def collapse(data, out):
    """Block passes per block and shot against M = p C / 2, the expected accepted damping events per shot."""
    import math
    fig, axes = plt.subplots(1, 3, figsize=(8.4, 2.9), sharey=True)
    ms = np.logspace(-3.5, 1.5, 200)
    for ax, shots, label in zip(axes, (100, 1000, 10000), "abc"):
        for c, color in COLORS.items():
            r = sorted((x["p"] * x["channels"] / 2, x["block_passes"] / (x["blocks"] * shots)) for x in data
                       if x["circuit"] == c and x["shots"] == shots)
            if r:
                ax.plot([a for a, _ in r], [b for _, b in r], "o", ms=3.5, color=color, label=c)
        f = np.array([1 - (1 - math.exp(-m)) / m for m in ms])
        ax.plot(ms, 1 / shots + f, "k-", lw=0.9, label="$1/N + f(M)$")
        ax.plot(ms, 1 / shots + f + 2 * ms / 10, "k--", lw=0.9, label="$+\\,2M/B$, $B=10$")
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_title(f"N = {shots} shots", fontsize=9)
        ax.set_xlabel("$M = pC/2$" if label != "b" else "expected damping events per shot $M = pC/2$")
        ax.set_xlim(3e-4, 30)
        ax.set_ylim(5e-5, 5)
        panel_label(ax, label)
    axes[0].set_ylabel("block passes / (blocks $B$ × shots $N$)")
    axes[2].legend(fontsize=6.5, frameon=False, loc="lower right", ncol=2)
    fig.tight_layout()
    return fig


if __name__ == "__main__":
    sweep, out, d = sys.argv[1:4]
    data = [r for dd in sys.argv[3:] for r in rows(dd)]
    fig = {"fusion": fusion, "noise": noise_sweep, "collapse": collapse, "segments": segments}[sweep](data, out)
    fig.savefig(out)
    fig.savefig(out.rsplit(".", 1)[0] + ".png", dpi=110)
