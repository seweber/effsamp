"""A2: predict run times from block passes, against the measured times.

Three predictions per point:

- ``bw``: the PLAN.md model, block passes x t_bw (Eq. (1) of the cost-model page);
- ``kernels``: t_bw (r_dom P_dom + r_gen P_gen), with the dry run's split of the passes into
  dominant- and general-kernel passes and each circuit's mean kernel ratios r = t_pass / t_bw over
  its blocks, measured alone (a2_blocks.py at the same n);
- the measured time.

Usage: python a2_timemodel.py OUT_PREFIX --blocks DIR... --runs DIR...
"""

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import circuits  # noqa: E402
import dryrun  # noqa: E402
import noise  # noqa: E402
import summarize_runs  # noqa: E402

COLORS = {"ghz": "#4C72B0", "brickwork": "#DD8452", "qft": "#55A868", "random": "#C44E52", "grid": "#8172B3",
          "qaoa": "#937860"}


def kernel_ratios(dirs):
    """(circuit, n) -> (mean t_dom / t_bw, mean t_gen / t_bw) over the circuit's blocks."""
    blocks, t_bw = defaultdict(list), {}
    for d in dirs:
        for line in (Path(d) / "stdout.txt").read_text().splitlines():
            if not line.startswith("{"):
                continue
            r = json.loads(line)
            if r["kind"] == "block":
                blocks[(r["circuit"], r["n"])].append(r)
            else:
                t_bw[r["n"]] = r["t_cupy"]
    out = {}
    for (c, n), rs in blocks.items():
        dom = np.mean([b["t_dom"] for b in rs]) / t_bw[n]
        gen = np.mean([b["t_gen"] if b["t_gen"] is not None else b["t_dom"] for b in rs]) / t_bw[n]
        out[(c, n)] = (float(dom), float(gen))
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("prefix")
    parser.add_argument("--blocks", nargs="+", required=True)
    parser.add_argument("--runs", nargs="+", required=True)
    args = parser.parse_args()
    ratios = kernel_ratios(args.blocks)
    rows = []
    for pt in summarize_runs.points(summarize_runs.load(args.runs)):
        if pt["p"] == 0 or pt["options"] or (pt["circuit"], pt["n"]) not in ratios:
            continue
        qc = circuits.make(pt["circuit"], pt["n"])
        maps = noise.maps(pt["noise"], pt["p"])
        runs = [dryrun.predict(qc, maps, pt["shots"], seed=s) for s in range(3)]
        p_dom = np.mean([r["dominant_passes"] for r in runs])
        p_gen = np.mean([r["general_passes"] for r in runs])
        r_dom, r_gen = ratios[(pt["circuit"], pt["n"])]
        row = {**{k: pt[k] for k in ("circuit", "n", "p", "shots", "blocks", "time", "t_bw", "block_passes")},
               "p_dom": float(p_dom), "p_gen": float(p_gen), "r_dom": r_dom, "r_gen": r_gen,
               "bw": pt["block_passes"] * pt["t_bw"],
               "kernels": pt["t_bw"] * (r_dom * p_dom + r_gen * p_gen)}
        rows.append(row)
        print(json.dumps(row), flush=True)

    fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.3), sharey=True)
    markers = {24: "o", 26: "s", 28: "^"}
    for ax, key, title, label in zip(axes, ("bw", "kernels"), ("passes × $t_{bw}$", "kernel-ratio model, Eq. (4)"),
                                     "ab"):
        for r in rows:
            ax.scatter(r[key], r["time"] / r[key], color=COLORS[r["circuit"]], marker=markers.get(r["n"], "o"),
                       s=18, linewidths=0)
        ax.axhline(1, color="k", lw=0.8)
        for f in (1.5, 1 / 1.5):
            ax.axhline(f, color="k", lw=0.6, ls="--")
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_ylim(0.5, 5)
        ax.set_yticks([0.5, 0.67, 1, 1.5, 2, 3, 4], ["0.5", "0.67", "1", "1.5", "2", "3", "4"])
        ax.minorticks_off()
        ax.set_xlabel(f"predicted time (s): {title}")
        ax.text(-0.02, 1.02, f"({label})", transform=ax.transAxes, fontsize=9, ha="right", va="bottom")
    axes[0].set_ylabel("measured / predicted time")
    handles = [plt.Line2D([], [], color=c, marker="o", ls="", ms=4, label=k) for k, c in COLORS.items()
               if any(r["circuit"] == k for r in rows)]
    handles += [plt.Line2D([], [], color="gray", marker=m, ls="", ms=4, label=f"n = {n}") for n, m in markers.items()]
    axes[1].legend(handles=handles, fontsize=7, frameon=False, ncol=2, loc="upper right")
    fig.tight_layout()
    fig.savefig(args.prefix + ".svg")
    fig.savefig(args.prefix + ".png", dpi=110)


if __name__ == "__main__":
    main()
