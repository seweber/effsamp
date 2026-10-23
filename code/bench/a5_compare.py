"""A5: measured runs against the A4 predictions (committed before the runs).

Matches every measured point (a2_runs.py output of the A5 validation runs) with the A4 prediction of
the same circuit, noise and strength, and compares passes (dry run) and times (bandwidth model and
kernel-ratio model). Prints JSON lines and writes OUT_PREFIX.svg/.png.

Usage: python a5_compare.py OUT_PREFIX --pred PREDICTED_TIMES.jsonl A4_PRED_DIRS... --runs A5_DIRS...
"""
import argparse
import json
import math
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).parent))
import summarize_runs  # noqa: E402

COLORS = {"ghz": "#4C72B0", "brickwork": "#DD8452", "qft": "#55A868", "random": "#C44E52", "grid": "#8172B3",
          "qaoa": "#937860", "scramble": "#DA8BC3"}
MARKERS = {"damping": "o", "thermal": "s", "gad": "^", "dephasing": "v", "depolarizing": "D"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("prefix")
    parser.add_argument("--pred", nargs="+", required=True)
    parser.add_argument("--runs", nargs="+", required=True)
    args = parser.parse_args()
    predictions = []
    for path in args.pred:
        path = Path(path)
        lines = path.read_text().splitlines() if path.is_file() else (path / "stdout.txt").read_text().splitlines()
        predictions += [json.loads(x) for x in lines if x.startswith("{")]
    rows = []
    for pt in summarize_runs.points(summarize_runs.load(args.runs)):
        optimized = bool(pt["options"].get("optimize_kraus"))
        match = [q for q in predictions if q["circuit"] == pt["circuit"] and q["noise"] == pt["noise"]
                 and abs(q["p"] / pt["p"] - 1) < 1e-3 and q["shots"] == pt["shots"]
                 and bool(q.get("optimize_kraus")) == optimized]
        if not match:
            continue
        # Prefer a prediction with times (a4_times output) over a bare dry run.
        q = max(match, key=lambda x: "T_kern" in x)
        row = {**{k: pt[k] for k in ("circuit", "n", "noise", "p", "shots", "time", "block_passes", "t_bw")},
               "optimize_kraus": optimized, "load": q["load"], "pred_passes": q["block_passes"],
               "pred_T_bw": q["block_passes"] * pt["t_bw"], "pred_T_kern": q.get("T_kern")}
        rows.append(row)
        print(json.dumps(row), flush=True)

    fig, axes = plt.subplots(1, 3, figsize=(10.5, 3.3))
    panels = (("pred_passes", "block_passes", "block passes"), ("pred_T_bw", "time", "time: passes × $t_{bw}$ (s)"),
              ("pred_T_kern", "time", "time: kernel-ratio model (s)"))
    for ax, (pk, mk, title), text in zip(axes, panels, "abc"):
        pairs = [(r[pk], r[mk], r) for r in rows if r[pk]]
        for x, y, r in pairs:
            ax.scatter(x, y / x, color=COLORS[r["circuit"]], marker=MARKERS[r["noise"]], s=20, linewidths=0)
        ax.axhline(1, color="k", lw=0.8)
        for f in (1.5, 1 / 1.5):
            ax.axhline(f, color="k", lw=0.6, ls="--")
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_ylim(0.4, 3)
        ax.set_yticks([0.5, 0.67, 1, 1.5, 2, 3], ["0.5", "0.67", "1", "1.5", "2", "3"])
        ax.minorticks_off()
        ax.set_xlabel(f"predicted {title}")
        ax.text(-0.02, 1.02, f"({text})", transform=ax.transAxes, fontsize=9, ha="right", va="bottom")
        if pairs:
            logs = [math.log(y / x) for x, y, _ in pairs]
            gm = math.exp(sum(logs) / len(logs))
            ax.set_title(f"measured/predicted: {min(y / x for x, y, _ in pairs):.2f} to "
                         f"{max(y / x for x, y, _ in pairs):.2f}, geo. mean {gm:.2f}", fontsize=8)
    axes[0].set_ylabel("measured / predicted")
    handles = [plt.Line2D([], [], color=c, marker="o", ls="", ms=4, label=k) for k, c in COLORS.items()
               if any(r["circuit"] == k for r in rows)]
    handles += [plt.Line2D([], [], color="gray", marker=m, ls="", ms=4, label=k) for k, m in MARKERS.items()
                if any(r["noise"] == k for r in rows)]
    axes[2].legend(handles=handles, fontsize=6, frameon=False, ncol=2, loc="lower right")
    fig.tight_layout()
    fig.savefig(args.prefix + ".svg")
    fig.savefig(args.prefix + ".png", dpi=110)


if __name__ == "__main__":
    main()
