"""A8: pass time of each block's dominant, general and masked kernel against its gates (a7_blocks.py output).

Usage: a8_plot.py OUT.svg BLOCK_TIMES_DIR [AB_DIRS...]
With A/B run directories (a2_runs.py with --tunable MASKED_ERROR_KERNELS=True/False), a second panel
shows the end-to-end time with masked kernels over the time with general kernels.
"""

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).parent))
import summarize_runs  # noqa: E402

KERNELS = (("t_dom", "dominant (no error)", "#4C72B0"), ("t_gen", "general (switches everywhere)", "#C44E52"),
           ("t_mask", "masked (error in one stage)", "#55A868"))
COLORS = {"ghz": "#4C72B0", "brickwork": "#DD8452", "qft": "#55A868", "grid": "#8172B3", "qaoa": "#937860"}


def main():
    out, d, ab = sys.argv[1], sys.argv[2], sys.argv[3:]
    records = [json.loads(x) for x in (Path(d) / "stdout.txt").read_text().splitlines() if x.startswith("{")]
    # The stronger noise of each circuit, whose blocks have the most error passes.
    strongest = {}
    for r in records:
        if r["circuit"] not in strongest or r["p"] > strongest[r["circuit"]]["p"]:
            strongest[r["circuit"]] = r
    fig, axes = plt.subplots(1, 2 if ab else 1, figsize=(9.6 if ab else 5.0, 3.4), squeeze=False)
    ax = axes[0, 0]
    for key, label, color in KERNELS:
        xs, ys = [], []
        for r in strongest.values():
            xs += r["gates"]
            ys += [t / r["t_bw"] for t in r[key]]
        ax.scatter(xs, ys, s=10, color=color, alpha=0.7, linewidths=0, label=label)
    ax.axhline(1, color="k", lw=0.6)
    ax.set_yscale("log")
    ax.set_yticks([1, 1.5, 2, 3, 4, 6], ["1", "1.5", "2", "3", "4", "6"])
    ax.minorticks_off()
    ax.set_xlabel("gates per block")
    ax.set_ylabel("pass time / $t_{bw}$")
    ax.legend(fontsize=7, frameon=False, loc="upper left")
    ax.text(-0.02, 1.02, "(a)", transform=ax.transAxes, fontsize=9, ha="right", va="bottom")
    if ab:
        pts = summarize_runs.points(summarize_runs.load(ab))
        by = {(p["circuit"], p["p"], p["tunables"][0].split("=")[1]): p for p in pts}
        ax = axes[0, 1]
        names = list(COLORS)
        for j, load_index in enumerate((0, 1)):
            xs, ys = [], []
            for i, c in enumerate(names):
                ps = sorted({k[1] for k in by if k[0] == c})
                if len(ps) <= load_index:
                    continue
                p = ps[load_index]
                xs.append(i + (j - 0.5) * 0.35)
                ys.append(by[(c, p, "True")]["time"] / by[(c, p, "False")]["time"])
            ax.bar(xs, ys, 0.35, color=("#A6C8E0", "#4C72B0")[j], label=("$M = 0.1$", "$M = 1$")[j])
        ax.axhline(1, color="k", lw=0.6)
        ax.set_ylim(0.8, 1.06)
        ax.set_xticks(range(len(names)), names)
        ax.set_ylabel("time with masked / general kernels")
        ax.legend(fontsize=7, frameon=False, loc="upper left", ncol=2)
        ax.text(-0.02, 1.02, "(b)", transform=ax.transAxes, fontsize=9, ha="right", va="bottom")
    fig.tight_layout()
    fig.savefig(out)
    fig.savefig(out.rsplit(".", 1)[0] + ".png", dpi=110)


if __name__ == "__main__":
    main()
