"""A13: analyse the precision x block-size sweep of block pass times (a13_blocks.py runs).

For each run directory data/*-a13-block-times-<dtype>-max-fused-qudits-<q>-max-operations-<g>, and
each circuit: the blocks B, the time of one trajectory through the circuit with dominant kernels
(sum of the blocks' pass times), its ratio to B passes at the bandwidth of the stored type, and the
mean static work. Writes data/a13-analysis/a13.jsonl and a figure a13.svg.
"""

import glob
import json
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "a13-analysis"
OUT.mkdir(parents=True, exist_ok=True)

rows = []
for run in sorted(glob.glob(str(ROOT / "data" / "*-a13-block-times-*"))):
    m = re.search(r"a13-block-times-(complex\d+)-max-fused-qudits-(\d+)-max-operations-(\d+)$", run)
    if not m:
        continue
    dtype, q, g = m.group(1), int(m.group(2)), int(m.group(3))
    for line in open(Path(run) / "stdout.txt"):
        rec = json.loads(line)
        per = rec["per_block"]
        t_traj = sum(b["t_dom"] for b in per)
        rows.append({
            "dtype": dtype, "max_fused_qudits": q, "max_operations": g, "circuit": rec["circuit"],
            "blocks": rec["blocks"], "t_bw": rec["t_bw"], "t_traj": t_traj,
            "t_traj_mask": sum(b["t_mask"] for b in per),
            "ratio": t_traj / (rec["blocks"] * rec["t_bw"]),
            "fp_ops": float(np.mean([b["fp_ops"] for b in per])),
            "shared": float(np.mean([b["shared"] for b in per])),
            "gates_per_block": float(np.mean([b["gates"] for b in per])),
            "t_compile": rec["t_compile"], "run": Path(run).name,
        })
with open(OUT / "a13.jsonl", "w") as f:
    for r in rows:
        f.write(json.dumps(r) + "\n")

circuits = ["ghz", "brickwork", "qft", "qaoa", "grid"]
colors = {9: "#1f77b4", 10: "#ff7f0e", 11: "#2ca02c"}
fig, axes = plt.subplots(2, len(circuits), figsize=(15, 6), sharex=True)
for j, c in enumerate(circuits):
    ref = next(r for r in rows if r["circuit"] == c and r["dtype"] == "complex64"
               and r["max_fused_qudits"] == 9 and r["max_operations"] == 128)
    for q in (9, 10, 11):
        for dtype, style in (("complex64", "-o"), ("complex32", "--s")):
            sel = sorted((r for r in rows if r["circuit"] == c and r["dtype"] == dtype and r["max_fused_qudits"] == q),
                         key=lambda r: r["max_operations"])
            if not sel:
                continue
            x = [r["max_operations"] for r in sel]
            axes[0, j].plot(x, [r["t_traj"] / ref["t_traj"] for r in sel], style, color=colors[q], ms=4,
                            label=f"{dtype}, width {q}")
            axes[1, j].plot(x, [r["ratio"] for r in sel], style, color=colors[q], ms=4)
    axes[0, j].set_title(c)
    axes[1, j].set_xscale("log", base=2)
    axes[1, j].set_xlabel("max_operations (gates per block)")
    axes[0, j].axhline(1, color="gray", lw=0.5)
    axes[1, j].axhline(1, color="gray", lw=0.5)
axes[0, 0].set_ylabel("trajectory time / default\n(complex64, width 9, 128 gates)")
axes[1, 0].set_ylabel("time / (blocks × t_bw of stored type)")
axes[0, 0].legend(fontsize=7)
for ax, label in zip(axes[:, 0], "ab"):
    ax.text(-0.35, 1.02, f"({label})", transform=ax.transAxes, fontsize=11)
fig.tight_layout()
fig.savefig(OUT / "a13.svg")
print(f"{'circuit':10s} {'dtype':9s} q   g    B   t_traj/ms  ratio  ops  shared")
for r in sorted(rows, key=lambda r: (r["circuit"], r["dtype"], r["max_fused_qudits"], r["max_operations"])):
    print(f"{r['circuit']:10s} {r['dtype']:9s} {r['max_fused_qudits']:2d} {r['max_operations']:4d} {r['blocks']:4d} "
          f"{1e3 * r['t_traj']:8.2f} {r['ratio']:6.2f} {r['fp_ops']:5.0f} {r['shared']:5.1f}")
