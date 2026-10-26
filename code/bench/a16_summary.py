"""A16: figure and table of tensor-core against CUDA-core block passes, from the a16_time.py runs.

Reads the hybrid-threshold runs (complex64 and complex32, 4-qubit stages) and writes
data/a16-analysis/tensor-cores.svg (two panels: mean dominant pass time over the bandwidth time,
per workload) and data/a16-analysis/summary.json.

Usage: a16_summary.py   (local, from the project root)
"""

import glob
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

OUT = Path("data/a16-analysis")
CIRCUITS = ["ghz", "brickwork", "qft", "qaoa", "grid"]
COLORS = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]


def rows(pattern: str) -> dict:
    """The t_over_tbw of every workload of the newest run matching ``pattern``."""
    run = sorted(glob.glob(f"data/*{pattern}"))[-1]
    out = {}
    for line in open(f"{run}/stdout.txt"):
        if line.startswith("{"):
            r = json.loads(line)
            out[r["circuit"]] = r["t_over_tbw"]
    return {"run": run, "rows": out}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    panels = [
        ("(a) complex64, 4-qubit stages", [
            ("CUDA cores", "f16x3,tensor_unroll=1", "min_registers=96"),
            ("tensor cores f16x3 (single-precision accurate)", "f16x3,tensor_unroll=1",
             "tensor_cores=f16x3,tensor_unroll=1,min_registers=96,tensor_threshold=24"),
            ("tensor cores f16, stages > 12 FP/amp (~1e-3)", "f16,tensor_unroll=2",
             "tensor_cores=f16,tensor_unroll=2,min_registers=96,tensor_threshold=12"),
        ]),
        ("(b) complex32, 4-qubit stages", [
            ("CUDA cores", "f16,tensor_unroll=2", "base"),
            ("tensor cores f16, stages > 18 FP/amp (~1e-3)", "f16,tensor_unroll=2",
             "tensor_cores=f16,tensor_unroll=2,min_registers=96,tensor_threshold=18"),
        ]),
    ]
    dtypes = {"(a)": "complex64", "(b)": "complex32"}
    summary = {}
    plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False})
    fig, axes = plt.subplots(1, 2, figsize=(9.0, 3.4), sharey=True)
    for ax, (title, series) in zip(axes, panels, strict=True):
        dtype = dtypes[title[:3]]
        width = 0.8 / len(series)
        summary[title] = {}
        for i, (label, suffix, variant) in enumerate(series):
            data = rows(f"a16-hybrid-tensor-core-threshold-{dtype}-sq4-{suffix.split(',')[0]}")
            values = [data["rows"][c][variant] for c in CIRCUITS]
            summary[title][label] = {"run": data["run"], "variant": variant, **dict(zip(CIRCUITS, values, strict=True))}
            x = [j + (i - (len(series) - 1) / 2) * width for j in range(len(CIRCUITS))]
            ax.bar(x, values, width * 0.9, color=COLORS[i], label=label)
        ax.set_xticks(range(len(CIRCUITS)), CIRCUITS)
        ax.set_title(title, loc="left", fontsize=9)
        ax.set_ylim(0, 2.3)
        ax.grid(axis="y", color="#e4e3dd", linewidth=0.6)
        ax.set_axisbelow(True)
        ax.legend(frameon=False, fontsize=7.5, loc="upper left")
    axes[0].set_ylabel("mean pass time / bandwidth time $t_{bw}$")
    fig.tight_layout()
    fig.savefig(OUT / "tensor-cores.svg")
    if len(sys.argv) > 1:  # a raster copy to inspect
        fig.savefig(sys.argv[1], dpi=150)
    (OUT / "summary.json").write_text(json.dumps(summary, indent=1))
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
