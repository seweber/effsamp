"""A18: figure of register-chained tensor-core stages against CUDA-core stages, and of the dense su4 workload.

Reads the newest a18_chain.py run with structured CUDA-core stages and the four su4 timing runs
(a16_time.py), and writes data/a18-analysis/chained-tensor-cores.svg: (a) pass time over the copy
time against stages per pass in the microbenchmark (4 tiles per warp, stages relaid out through
shared memory, complex32 storage, 28 qubits); (b) mean pass time of the su4 brickwork's dominant
kernels with 3-qubit stages, CUDA cores against noisecirc's tensor-core stages (A16 implementation).

Usage: a18_summary.py [png]   (local, from the project root)
"""

import glob
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

OUT = Path("data/a18-analysis")
COLORS = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#6250d6"]


def newest(pattern: str) -> str:
    return sorted(glob.glob(f"data/*{pattern}"))[-1]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    chain = newest("a18-register-chained-tensor-core-vs-structured-cuda-core-stages-complex32-n-28")
    runs = [json.loads(line) for line in open(f"{chain}/stdout.txt") if line.startswith("{")]
    series = [
        ("tensor cores f16 (~1e-3, gate rounding)", lambda r: r["kernel"] == "tc" and r["split"] == 1),
        ("tensor cores f16x2 (TVD ~2x complex32)", lambda r: r["kernel"] == "tc" and r["split"] == 2),
        ("tensor cores f16x3 (= complex32)", lambda r: r["kernel"] == "tc" and r["split"] == 3),
        ("CUDA cores, 16 FP/amp per stage (brickwork-like)",
         lambda r: r["kernel"] == "cuda_structured" and r["fp_per_amp"] == 16 and r["gates"] <= 16),
        ("CUDA cores, 8 FP/amp per stage (GHZ/QAOA-like)",
         lambda r: r["kernel"] == "cuda_structured" and r["fp_per_amp"] == 8 and r["gates"] <= 16),
        ("CUDA cores, dense 3-qubit (64 FP/amp)", lambda r: r["kernel"] == "cuda"),
    ]
    summary = {"chain_run": chain, "series": {}}
    plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False})
    fig, (left, right) = plt.subplots(1, 2, figsize=(10.0, 3.8), gridspec_kw={"width_ratios": [1.5, 1]})
    for color, (label, keep) in zip(COLORS, series, strict=True):
        points = sorted((r["gates"], r["t_over_tbw"]) for r in runs if r.get("kind") == "run" and keep(r)
                        and r["switch"] == (1 if r["kernel"] == "cuda" else 2 if r["kernel"] == "tc" else 1)
                        and r.get("tiles", 4) == 4)
        summary["series"][label] = points
        left.plot(*zip(*points), color=color, linewidth=2, marker="o", markersize=4, label=label)
    left.set_xscale("log", base=2)
    left.set_yscale("log", base=2)
    left.set_xticks([1, 4, 8, 16, 32], ["1", "4", "8", "16", "32"])
    left.set_yticks([1, 2, 4, 8], ["1", "2", "4", "8"])
    left.set_xlabel("stages (3-qubit gates) per pass")
    left.set_ylabel("pass time / copy time")
    left.set_title("(a) microbenchmark, complex32, 28 qubits", loc="left", fontsize=9)
    left.grid(color="#e4e3dd", linewidth=0.6)
    left.set_axisbelow(True)
    left.legend(frameon=False, fontsize=7, loc="upper left")

    variants = [("CUDA cores", "min_registers=96"), ("f16x3", "tensor_cores=f16x3,tensor_unroll=2,min_registers=96"),
                ("f16x2", "tensor_cores=f16x2,tensor_unroll=2,min_registers=96"),
                ("f16", "tensor_cores=f16,tensor_unroll=2,min_registers=96")]
    for k, dtype in enumerate(["complex32", "complex64"]):
        run = newest(f"a18-dense-su4-brickwork-tensor-core-stages-{dtype}-sq3-n-26")
        row = json.loads(open(f"{run}/stdout.txt").readline())["t_over_tbw"]
        summary[dtype] = {"run": run, **{label: row[v] for label, v in variants}}
        for i, (label, variant) in enumerate(variants):
            right.bar(k + (i - 1.5) * 0.2, row[variant], 0.18, color=COLORS[[0, 2, 1, 0][i]] if i else "#52514e",
                      label=label if k == 0 else None)
    right.set_xticks([0, 1], ["complex32", "complex64"])
    right.set_ylabel("mean pass time / $t_{bw}$")
    right.set_title("(b) noisecirc, su4 brickwork, 26 qubits", loc="left", fontsize=9)
    right.grid(axis="y", color="#e4e3dd", linewidth=0.6)
    right.set_axisbelow(True)
    right.legend(frameon=False, fontsize=7.5, loc="upper right")
    fig.tight_layout()
    fig.savefig(OUT / "chained-tensor-cores.svg")
    if len(sys.argv) > 1:
        fig.savefig(sys.argv[1], dpi=150)
    (OUT / "summary.json").write_text(json.dumps(summary, indent=1))
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
