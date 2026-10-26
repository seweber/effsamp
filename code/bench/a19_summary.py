"""A19: figure of the single-qubit gate forms (a19_gate_forms.py) and of two-level rotations (a16_time.py).

Writes data/a19-analysis/gate-forms.svg: (a) pass time over the copy time against gates per pass
applied in registers, per form, complex64, 28 qubits; (b) mean pass time of the dominant kernels of
three circuits of two-qubit rotations with and without svpass's two_level_rotations, 4-qubit stages.

Usage: a19_summary.py [png]   (local, from the project root)
"""

import glob
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

OUT = Path("data/a19-analysis")
COLORS = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]
LABELS = {"direct": "direct complex 2x2 (16 FMA/pair)", "shear": "three shears (12 FMA/pair)",
          "ratio": "rotation form with phase ratio (8 FMA/pair)", "rotation": "rotation form (4 FMA/pair)"}


def newest(pattern: str) -> str:
    return sorted(glob.glob(f"data/*{pattern}"))[-1]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    run = newest("a19-single-qubit-gate-forms-unrolled-n-28")
    rows = [json.loads(line) for line in open(f"{run}/stdout.txt") if line.startswith("{")]
    summary = {"forms_run": run, "forms": {}, "two_level": {}}
    plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False})
    fig, (left, right) = plt.subplots(1, 2, figsize=(10.0, 3.6), gridspec_kw={"width_ratios": [1.3, 1]})
    for color, (form, label) in zip(COLORS, LABELS.items(), strict=True):
        points = sorted((r["gates"], r["t_over_tbw"]) for r in rows if r["kind"] == "chain" and r["form"] == form)
        summary["forms"][form] = {"chain": points, "one_gate_per_pass": next(r["t_over_tbw"] for r in rows
                                                                             if r["kind"] == "hbm" and r["form"] == form)}
        left.plot(*zip(*points), color=color, linewidth=2, marker="o", markersize=4, label=label)
    left.set_xscale("log", base=2)
    left.set_xticks([3, 6, 12, 24, 48], ["3", "6", "12", "24", "48"])
    left.set_xlabel("single-qubit gates per pass, in registers")
    left.set_ylabel("pass time / copy time")
    left.set_ylim(0, 2.6)
    left.set_title("(a) gate forms, complex64, 28 qubits", loc="left", fontsize=9)
    left.grid(color="#e4e3dd", linewidth=0.6)
    left.set_axisbelow(True)
    left.legend(frameon=False, fontsize=7.5, loc="upper left")

    circuits = ["heisenberg", "fsim", "cry"]
    for k, dtype in enumerate(["complex64", "complex32"]):
        data = {}
        for line in open(f"{newest(f'a19-two-level-rotations-{dtype}-sq4-n-26')}/stdout.txt"):
            if line.startswith("{"):
                r = json.loads(line)
                data[r["circuit"]] = r["t_over_tbw"]
        summary["two_level"][dtype] = data
        for i, (variant, label) in enumerate([("base", "one-qubit rotation form"),
                                              ("two_level_rotations=1", "two-level rotations")]):
            x = [j + 4 * k + (i - 0.5) * 0.38 for j in range(len(circuits))]
            right.bar(x, [data[c][variant] for c in circuits], 0.34, color=["#52514e", COLORS[0]][i],
                      label=label if k == 0 else None)
    right.set_xticks([j + 4 * k for k in range(2) for j in range(3)], circuits * 2, fontsize=8)
    right.text(1, -0.15, "complex64", ha="center", transform=right.get_xaxis_transform())
    right.text(5, -0.15, "complex32", ha="center", transform=right.get_xaxis_transform())
    right.set_ylabel("mean pass time / $t_{bw}$")
    right.set_title("(b) two-level rotations, 4-qubit stages, 26 qubits", loc="left", fontsize=9)
    right.grid(axis="y", color="#e4e3dd", linewidth=0.6)
    right.set_axisbelow(True)
    right.legend(frameon=False, fontsize=7.5, loc="upper left")
    right.set_ylim(0, 2.7)
    fig.tight_layout()
    fig.savefig(OUT / "gate-forms.svg")
    if len(sys.argv) > 1:
        fig.savefig(sys.argv[1], dpi=150)
    (OUT / "summary.json").write_text(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
