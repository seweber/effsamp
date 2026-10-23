"""A4: predicted run times at n=28 from the dry-run predictions and measured kernel ratios.

T_bw = P t_bw (the bandwidth model) and T_kern = t_bw (r_dom P_dom + r_gen P_gen) (the kernel-ratio
model), with r from a2_blocks.py runs at n=28 for the same noise type.
Usage: python a4_times.py --pred DIR... --blocks DIR...   (prints JSON lines)
"""
import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("--pred", nargs="+")
parser.add_argument("--blocks", nargs="+")
args = parser.parse_args()
ratio, t_bw = {}, {}
blocks = defaultdict(list)
for d in args.blocks:
    for line in (Path(d) / "stdout.txt").read_text().splitlines():
        if not line.startswith("{"):
            continue
        r = json.loads(line)
        if r["kind"] == "block":
            blocks[(r["circuit"], r["noise"], r["n"])].append(r)
        else:
            t_bw[r["n"]] = r["t_cupy"]
for (c, k, n), rs in blocks.items():
    ratio[(c, k, n)] = (np.mean([b["t_dom"] for b in rs]) / t_bw[n],
                        np.mean([b["t_gen"] or b["t_dom"] for b in rs]) / t_bw[n])
for d in args.pred:
    for line in (Path(d) / "stdout.txt").read_text().splitlines():
        if not line.startswith("{"):
            continue
        r = json.loads(line)
        key = (r["circuit"], r["noise"], r["n"])
        if key not in ratio:
            continue
        r_dom, r_gen = ratio[key]
        tb = t_bw[r["n"]]
        print(json.dumps({**r, "t_bw": tb, "r_dom": r_dom, "r_gen": r_gen, "T_bw": r["block_passes"] * tb,
                          "T_kern": tb * (r_dom * r["dominant_passes"] + r_gen * r["general_passes"])}))
