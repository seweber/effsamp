"""A13/A14: end-to-end times of the kernel variants (data/*-a13-a14-end-to-end-<setting>-<circuit>-n-28), median over seeds."""
import glob
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
times = defaultdict(list)
passes = {}
for run in sorted(glob.glob(str(ROOT / "data" / "*-a13-a14-end-to-end-*-n-28"))):
    setting = re.search(r"end-to-end-(.+)-(ghz|brickwork|qft|qaoa|grid)-n-28$", run).group(1)
    for line in open(Path(run) / "stdout.txt"):
        r = json.loads(line)
        if r.get("kind") != "run":
            continue
        times[(setting, r["circuit"], r["p"])].append(r["time"])
        passes[(setting, r["circuit"], r["p"])] = r["block_passes"]
settings = ["default", "c32", "fused", "fused-sq4", "fused-sq4-c32", "contract-add-sq4", "contract-add-sq4-c32"]
rows = []
print(f"{'circuit':10s} {'p':>10s} " + " ".join(f"{s:>16s}" for s in settings))
for key in sorted({(c, p) for (_, c, p) in times}):
    base = np.median(times[("default", *key)])
    cells = []
    for s in settings:
        t = np.median(times[(s, *key)]) if times.get((s, *key)) else np.nan
        cells.append(f"{t:7.2f}s ({t / base:4.2f})")
        rows.append({"circuit": key[0], "p": key[1], "setting": s, "time": float(t), "ratio": float(t / base),
                     "passes": passes.get((s, *key))})
    print(f"{key[0]:10s} {key[1]:10.3g} " + " ".join(cells))
out = ROOT / "data" / "a13-analysis" / "e2e.jsonl"
with open(out, "w") as f:
    for r in rows:
        f.write(json.dumps(r) + "\n")
ratios = {s: [r["ratio"] for r in rows if r["setting"] == s] for s in settings}
print("geomean ratio:", {s: round(float(np.exp(np.mean(np.log(v)))), 3) for s, v in ratios.items()})

# Figure: time relative to the default kernels in complex64, per circuit and load.
import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

labels = {"c32": "complex32, default kernels", "fused": "A14 kernels",
          "fused-sq4": "A14 kernels, 4-qubit stages", "fused-sq4-c32": "A14 kernels, 4-qubit stages, complex32",
          "contract-add-sq4": "+ contraction order, additive addresses",
          "contract-add-sq4-c32": "+ contraction order, additive addresses, complex32"}
colors = {"c32": "#9467bd", "fused": "#1f77b4", "fused-sq4": "#ff7f0e", "fused-sq4-c32": "#2ca02c",
          "contract-add-sq4": "#d62728", "contract-add-sq4-c32": "#8c564b"}
keys = sorted({(r["circuit"], r["p"]) for r in rows}, key=lambda k: (["ghz", "brickwork", "qft", "qaoa", "grid"].index(k[0]), k[1]))
fig, ax = plt.subplots(figsize=(10, 3.6))
width = 0.14
for i, s in enumerate(labels):
    vals = [next(r["ratio"] for r in rows if (r["circuit"], r["p"]) == k and r["setting"] == s) for k in keys]
    ax.bar(np.arange(len(keys)) + (i - (len(labels) - 1) / 2) * width, vals, width * 0.9, color=colors[s], label=labels[s])
ax.axhline(1, color="gray", lw=0.8)
ax.set_xticks(np.arange(len(keys)))
ax.set_xticklabels([f"{c}\nM = {'0.1' if j % 2 == 0 else '1'}" for j, (c, _) in enumerate(keys)], fontsize=9)
ax.set_ylabel("run time / default kernels\n(complex64)")
ax.set_ylim(0, 1.15)
ax.legend(fontsize=8, ncol=3, loc="upper center", bbox_to_anchor=(0.5, 1.25), frameon=False)
fig.tight_layout()
fig.savefig(ROOT / "data" / "a13-analysis" / "e2e.svg")
if len(sys.argv) > 1:  # a raster copy to inspect
    fig.savefig(sys.argv[1], dpi=130)
