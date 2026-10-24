"""A11: Aer's shot branching with tuned options against noisecirc with tuned options.

Reads the A11 runs: Aer (a6_runs.py --sim aer_branch, with or without --aer-option) and noisecirc
(a2_runs.py, its defaults or --option autotune=1), all at the A6 points (24 qubits, damping, M = 0.01,
0.1 and 1, 1000 shots). A setting is named by its options ("default" without). Times are
the median of the timed repetitions, or the single first run where that took over a minute (a6_runs.py's
``first_only``).

Prints JSON lines: one per (circuit, load) with every setting's time; one per Aer setting with its
time over the default, as a geometric mean over all points and its range; and one per point with
noisecirc's speedup, defaults against defaults and tuned against tuned. Tuned Aer is the setting with
the smallest geometric-mean time over the circuit's three loads, chosen afterwards on the measured
data, i.e. an oracle choice in Aer's favour; tuned noisecirc is its own autotuning, which chooses
before the run. Writes OUT_PREFIX.svg/.png.

Runs at 28 qubits (selected points, where Aer's shot branching fits into device memory) are printed
as ``n28`` lines, their load from the expected damping events per shot, p C / 2.

Usage: a11_analyze.py OUT_PREFIX RUN_DIR...
"""

import json
import sys
from collections import defaultdict
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

LOADS = (0.01, 0.1, 1.0)
CIRCUITS = ("ghz", "brickwork", "qft", "qaoa")


def setting(r) -> tuple[str, str]:
    """(simulator, setting name) of a run record."""
    if r.get("sim") == "aer_branch":
        opts = r.get("aer_options") or {}
        return "aer", ",".join(f"{k}={v}" for k, v in sorted(opts.items())) or "default"
    if "block_passes" in r:
        opts = r.get("options") or {}
        return "nc", "autotune" if opts.get("autotune") else ("default" if not opts else json.dumps(opts))
    return "", ""


def records(dirs):
    for d in dirs:
        path = Path(d) / "stdout.txt"
        for line in path.read_text().splitlines() if path.exists() else []:
            if line.startswith("{"):
                r = json.loads(line)
                if r.get("kind", "run") == "run":
                    yield r


def load28(dirs):
    times = defaultdict(list)
    for r in records(dirs):
        sim, name = setting(r)
        if sim and r.get("n") == 28:
            times[(sim, name, r["circuit"], float(f"{r['p'] * r['channels'] / 2:.1g}"))].append(r["time"])
    return {k: float(np.median(v)) for k, v in times.items()}


def load(dirs):
    times = defaultdict(list)
    for d in dirs:
        path = Path(d) / "stdout.txt"
        for line in path.read_text().splitlines() if path.exists() else []:
            if not line.startswith("{"):
                continue
            r = json.loads(line)
            if r.get("kind", "run") != "run" or r.get("n") != 24:
                continue
            sim, name = setting(r)
            if sim:
                times[(sim, name, r["circuit"], r["p"])].append(r["time"])
    # The loads of a circuit, in increasing p, are M = 0.01, 0.1, 1.
    ps = defaultdict(set)
    for _, _, c, p in times:
        ps[c].add(p)
    load_of = {(c, p): LOADS[i] for c in ps for i, p in enumerate(sorted(ps[c]))}
    return {(sim, name, c, load_of[(c, p)]): float(np.median(t)) for (sim, name, c, p), t in times.items()}


def geomean(xs):
    return float(np.exp(np.mean(np.log(xs))))


def main():
    prefix, dirs = sys.argv[1], sys.argv[2:]
    t = load(dirs)
    points = sorted({(c, m) for (_, _, c, m) in t}, key=lambda x: (CIRCUITS.index(x[0]), x[1]))
    aer_settings = sorted({name for (sim, name, _, _) in t if sim == "aer"})
    for c, m in points:
        print(json.dumps({"kind": "point", "circuit": c, "M": m,
                          **{f"{sim}:{name}": round(v, 4) for (sim, name, cc, mm), v in t.items() if (cc, mm) == (c, m)}}))
    # Every Aer setting against Aer's default, over the points where both ran.
    summary = {}
    for name in aer_settings:
        ratios = {(c, m): t[("aer", name, c, m)] / t[("aer", "default", c, m)] for c, m in points
                  if ("aer", name, c, m) in t and ("aer", "default", c, m) in t}
        if ratios:
            summary[name] = ratios
            print(json.dumps({"kind": "setting", "setting": name, "points": len(ratios),
                              "geomean": round(geomean(list(ratios.values())), 4),
                              "min": round(min(ratios.values()), 4), "max": round(max(ratios.values()), 4),
                              "per_circuit": {c: round(geomean([v for (cc, _), v in ratios.items() if cc == c]), 4)
                                              for c in CIRCUITS if any(cc == c for cc, _ in ratios)}}))
    # Tuned Aer: per circuit the setting with the smallest geometric mean time over the three loads.
    best = {}
    for c in CIRCUITS:
        cands = [name for name in aer_settings if all(("aer", name, c, m) in t for m in LOADS)]
        if cands:
            best[c] = min(cands, key=lambda name: geomean([t[("aer", name, c, m)] for m in LOADS]))
    rows = []
    for c, m in points:
        row = {"kind": "speedup", "circuit": c, "M": m, "aer_tuned_setting": best.get(c)}
        if ("aer", "default", c, m) in t and ("nc", "default", c, m) in t:
            row["default_vs_default"] = t[("aer", "default", c, m)] / t[("nc", "default", c, m)]
        if c in best and ("nc", "autotune", c, m) in t:
            row["tuned_vs_tuned"] = t[("aer", best[c], c, m)] / t[("nc", "autotune", c, m)]
            row["aer_gain"] = t[("aer", "default", c, m)] / t[("aer", best[c], c, m)]
            if ("nc", "default", c, m) in t:
                row["nc_gain"] = t[("nc", "default", c, m)] / t[("nc", "autotune", c, m)]
        rows.append(row)
        print(json.dumps({k: (round(v, 3) if isinstance(v, float) else v) for k, v in row.items()}))
    t28 = load28(dirs)
    for c, m in sorted({(c, m) for (_, _, c, m) in t28}):
        row = {"kind": "n28", "circuit": c, "M": m,
               **{f"{sim}:{name}": round(v, 3) for (sim, name, cc, mm), v in t28.items() if (cc, mm) == (c, m)}}
        print(json.dumps(row))
    plot(prefix, summary, rows)


def plot(prefix, summary, rows):
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.6), gridspec_kw={"width_ratios": [1.6, 1]})
    ax = axes[0]
    short = {"fusion_max_qubit=1": "width 1", "fusion_max_qubit=3": "width 3", "fusion_max_qubit=4": "width 4",
             "fusion_max_qubit=5": "width 5", "fusion_enable=False": "no fusion", "fusion_cost_factor=1.2": "cost 1.2",
             "fusion_cost_factor=3.0": "cost 3", "fusion_cost_factor=3.0,fusion_max_qubit=3": "width 3\ncost 3",
             "fusion_cost_factor=3.0,fusion_max_qubit=4": "width 4\ncost 3",
             "shot_branching_sampling_enable=False": "no branch\nsampling"}
    names = [n for n in short if n in summary] + [n for n in summary if n not in short and n != "default"]
    colors = {"ghz": "#4C72B0", "brickwork": "#DD8452", "qft": "#55A868", "qaoa": "#937860"}
    markers = {0.01: "o", 0.1: "s", 1.0: "^"}
    for i, name in enumerate(names):
        for j, c in enumerate(CIRCUITS):
            for m, marker in markers.items():
                if (c, m) in summary[name]:
                    ax.scatter(i + (j - 1.5) * 0.17, summary[name][(c, m)], marker=marker, s=16,
                               color=colors[c], linewidths=0, label=f"{c}" if (i, m) == (0, 0.01) else None)
    for m, marker in markers.items():
        ax.scatter([], [], marker=marker, color="0.5", s=16, label=f"$M = {m:g}$")
    ax.axhline(1, color="k", lw=0.6)
    ax.set_yscale("log")
    ax.set_xticks(range(len(names)), [short.get(n, n) for n in names], fontsize=7)
    ax.set_ylabel("Aer time / Aer default time")
    ax.set_yticks([0.7, 1, 2, 5, 10, 50], ["0.7", "1", "2", "5", "10", "50"])
    ax.minorticks_off()
    ax.legend(fontsize=6.5, frameon=False, ncol=2)
    ax.text(-0.02, 1.02, "(a)", transform=ax.transAxes, fontsize=9, ha="right", va="bottom")
    ax = axes[1]
    for k, (key, label, color) in enumerate((("default_vs_default", "defaults", "#A6C8E0"),
                                             ("tuned_vs_tuned", "both tuned", "#4C72B0"))):
        xs, ys = [], []
        for i, r in enumerate(rows):
            if key in r:
                xs.append(i + (k - 0.5) * 0.38)
                ys.append(r[key])
        ax.bar(xs, ys, 0.38, color=color, label=label)
    # Aer's Kraus fusion fails there (heevx) in every setting, so Aer runs unfused.
    for i, r in enumerate(rows):
        if (r["circuit"], r["M"]) == ("brickwork", 0.1):
            ax.text(i, max(r.get("default_vs_default", 1), r.get("tuned_vs_tuned", 1)) * 1.05, "*", ha="center", fontsize=9)
    ax.set_yscale("log")
    ax.set_yticks([5, 10, 20, 50], ["5", "10", "20", "50"])
    ax.minorticks_off()
    ax.set_xticks(range(len(rows)), [f"{r['circuit'].replace('brickwork', 'brick')}\n{r['M']:g}" for r in rows], fontsize=6)
    ax.set_ylabel("Aer branching time / noisecirc time")
    ax.set_xlabel("circuit and $M$ (* Aer without Kraus fusion, its heevx bug)", fontsize=7)
    ax.legend(fontsize=7, frameon=False)
    ax.text(-0.02, 1.02, "(b)", transform=ax.transAxes, fontsize=9, ha="right", va="bottom")
    fig.tight_layout()
    fig.savefig(prefix + ".svg")
    fig.savefig(prefix + ".png", dpi=110)


if __name__ == "__main__":
    main()
