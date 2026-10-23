"""A3: compare the closed-form pass estimate (a3_model) and the dry run with the passes GPU runs did.

Usage: python a3_validate.py OUT_PREFIX GPU_RUN_DIRS...   (a2_runs.py output; noisecirc defaults)
Prints one JSON line per point and writes OUT_PREFIX.svg/.png: predicted against measured passes.
"""

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import a3_model  # noqa: E402
import circuits  # noqa: E402
import dryrun  # noqa: E402
import noise  # noqa: E402
import summarize_runs  # noqa: E402
from noisecirc import Simulator  # noqa: E402

COLORS = {"ghz": "#4C72B0", "brickwork": "#DD8452", "qft": "#55A868", "random": "#C44E52", "grid": "#8172B3",
          "qaoa": "#937860"}


def main():
    prefix, dirs = sys.argv[1], sys.argv[2:]
    points = [p for p in summarize_runs.points(summarize_runs.load(dirs)) if p["p"] > 0 and not p["options"]]
    out = []
    for pt in points:
        qc = circuits.make(pt["circuit"], pt["n"])
        maps = noise.maps(pt["noise"], pt["p"])
        compiled, _, _ = dryrun.compile_like_simulator(qc, Simulator(maps=maps))
        model = a3_model.estimate([b.log_oversampling_ceiling for b in compiled.blocks], pt["shots"],
                                  error_codes=[a3_model.error_codes(b) for b in compiled.blocks])
        dry = np.mean([dryrun.predict(qc, maps, pt["shots"], seed=s, compiled=compiled)["block_passes"]
                       for s in range(3)])
        row = {**{k: pt[k] for k in ("circuit", "n", "p", "shots", "blocks")}, "measured": pt["block_passes"],
               "dryrun": float(dry), "model": model["passes"], "model_dom": model["p_dom"],
               "model_gen": model["p_gen"], "M": model["M"], "L": model["L"]}
        out.append(row)
        print(json.dumps(row), flush=True)
    fig, ax = plt.subplots(figsize=(4.4, 3.8))
    for row in out:
        c = COLORS[row["circuit"]]
        ax.scatter(row["measured"], row["dryrun"], marker="o", s=16, color=c, linewidths=0)
        ax.scatter(row["measured"], row["model"], marker="x", s=16, color=c)
    lo = min(r["measured"] for r in out) / 1.5
    hi = max(r["measured"] for r in out) * 1.5
    ax.plot([lo, hi], [lo, hi], "k-", lw=0.8)
    for f in (1.5, 1 / 1.5):
        ax.plot([lo, hi], [lo * f, hi * f], "k--", lw=0.6)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("block passes, measured on the GPU")
    ax.set_ylabel("block passes, predicted")
    handles = [plt.Line2D([], [], color=c, marker="o", ls="", ms=4, label=k) for k, c in COLORS.items()
               if any(r["circuit"] == k for r in out)]
    handles += [plt.Line2D([], [], color="gray", marker="o", ls="", ms=4, label="dry run"),
                plt.Line2D([], [], color="gray", marker="x", ls="", ms=4, label="closed form")]
    ax.legend(handles=handles, fontsize=7, frameon=False, loc="upper left")
    fig.tight_layout()
    fig.savefig(prefix + ".svg")
    fig.savefig(prefix + ".png", dpi=110)


if __name__ == "__main__":
    main()
