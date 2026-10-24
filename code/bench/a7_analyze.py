"""A7: predicted run time of every parameter setting relative to noisecirc's defaults.

Reads a7_predict.py's output, and for each swept parameter plots the predicted GPU time of each
workload relative to the default setting against the parameter's value (panel per parameter), plus
the geometric mean; prints a table of the geometric means, also for a single trajectory (the ideal
circuit's time, the sum of the dominant kernels) and the compile time.

Usage: a7_analyze.py OUT_PREFIX PREDICT_DIR
"""

import json
import math
import sys
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

COLORS = {"ghz": "#4C72B0", "brickwork": "#DD8452", "qft": "#55A868", "grid": "#8172B3", "qaoa": "#937860"}
DEFAULTS = {"max_operations": 128, "max_fused_qudits": 9, "pinned_bytes": 64, "stage_qubits": 3,
            "group_amplitudes": 2048, "threads": 256, "min_registers": 64}
TITLES = {"max_operations": "gates per block (max_operations)", "max_fused_qudits": "block qubits (max_fused_qudits)",
          "pinned_bytes": "pinned bytes (pinned qubits)", "stage_qubits": "stage qubits",
          "group_amplitudes": "amplitudes per thread block", "threads": "threads per thread block",
          "min_registers": "min. registers per thread"}


def main():
    prefix, d = sys.argv[1], sys.argv[2]
    rows = [json.loads(x) for x in (Path(d) / "stdout.txt").read_text().splitlines()
            if x.startswith("{") and "T_gpu" in x]
    base = {(r["circuit"], r["p"]): r for r in rows if r["label"] == "default"}
    by_param = defaultdict(lambda: defaultdict(list))  # param -> value -> [(workload, ratio, single, compile)]
    for r in rows:
        settings = {**r["options"], **r["config"]}
        if not settings:
            settings = {}
        key = (r["circuit"], r["p"])
        if key not in base:
            continue
        b = base[key]
        entry = (key, r["T_gpu"] / b["T_gpu"], r["single_trajectory"] / b["single_trajectory"],
                 r["t_compile"] / b["t_compile"])
        if not settings:
            for param, value in DEFAULTS.items():
                by_param[param][value].append(entry)
        for param, value in settings.items():
            by_param[param][value].append(entry)
    table = []
    params = [p for p in DEFAULTS if p in by_param]
    fig, axes = plt.subplots(2, 4, figsize=(12.5, 5.6), sharey=True)
    for ax, param, label in zip(axes.flat, params, "abcdefg"):
        values = sorted(by_param[param])
        for circuit, color in COLORS.items():
            for p_index, ls in ((0, ":"), (1, "-")):
                pts = []
                for v in values:
                    ws = sorted({e[0][1] for e in by_param[param][v] if e[0][0] == circuit})
                    for e in by_param[param][v]:
                        if e[0][0] == circuit and len(ws) > p_index and e[0][1] == ws[p_index]:
                            pts.append((v, e[1]))
                if pts:
                    ax.plot(*zip(*pts), ls, marker="o", ms=2.5, lw=0.9, color=color)
        gm = [(v, math.exp(sum(math.log(e[1]) for e in by_param[param][v]) / len(by_param[param][v])))
              for v in values]
        ax.plot(*zip(*gm), "k-", lw=1.8, label="geometric mean")
        ax.axhline(1, color="k", lw=0.6, ls="--")
        ax.set_xscale("log", base=2)
        ax.set_xticks(values, [str(v) for v in values], fontsize=7)
        ax.minorticks_off()
        ax.set_title(TITLES[param], fontsize=8.5)
        ax.text(-0.02, 1.02, f"({label})", transform=ax.transAxes, fontsize=9, ha="right", va="bottom")
        for v in values:
            es = by_param[param][v]
            g = lambda i: math.exp(sum(math.log(e[i]) for e in es) / len(es))  # noqa: E731
            table.append({"param": param, "value": v, "time": g(1), "time_min": min(e[1] for e in es),
                          "time_max": max(e[1] for e in es), "single": g(2), "compile": g(3), "n": len(es)})
    for ax in axes[:, 0]:
        ax.set_ylabel("predicted time / default")
    axes.flat[-1].axis("off")
    handles = [plt.Line2D([], [], color=c, label=k) for k, c in COLORS.items()]
    handles += [plt.Line2D([], [], color="gray", ls=":", label="M = 0.1"), plt.Line2D([], [], color="gray", ls="-", label="M = 1"),
                plt.Line2D([], [], color="k", lw=1.8, label="geometric mean")]
    axes.flat[-1].legend(handles=handles, fontsize=8, frameon=False, loc="center")
    axes.flat[0].set_ylim(0.6, 3.3)
    fig.tight_layout()
    fig.savefig(prefix + ".svg")
    fig.savefig(prefix + ".png", dpi=110)
    for t in table:
        print(json.dumps(t))


if __name__ == "__main__":
    main()
