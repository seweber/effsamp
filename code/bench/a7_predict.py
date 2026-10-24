"""A7/A8: predicted run times for each setting of noisecirc's parameters, from block times and dry runs.

For every record of a7_blocks.py (a setting and a workload, with the time of each block's dominant and
general kernel), the dry run of the same setting counts the passes of each block with each kernel
(mean of 3 seeds, ``--shots`` shots), and the predicted GPU time is

    T_gpu = sum_b (P_dom,b t_dom,b + P_gen,b t_gen,b).

Prints one JSON line per record. Usage: a7_predict.py [--shots N] DIR...  (run locally, CPU)
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import circuits  # noqa: E402
import configpatch  # noqa: E402
import dryrun  # noqa: E402
import noise  # noqa: E402


def records(dirs):
    for d in dirs:
        path = Path(d) / "stdout.txt"
        if path.exists():
            for line in path.read_text().splitlines():
                if line.startswith("{") and '"t_dom"' in line:
                    yield json.loads(line)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--shots", type=int, default=1000)
    parser.add_argument("--seeds", type=int, default=3)
    parser.add_argument("dirs", nargs="+")
    args = parser.parse_args()
    for r in records(args.dirs):
        configpatch.apply(r["config"])
        qc = circuits.make(r["circuit"], r["n"])
        maps = noise.maps(None if r["noise"] == "none" else r["noise"], r["p"])
        runs = [dryrun.predict(qc, maps, args.shots, seed=s, **r["options"]) for s in range(1, args.seeds + 1)]
        if runs[0]["blocks"] != len(r["t_dom"]):
            print(json.dumps({"label": r["label"], "circuit": r["circuit"], "p": r["p"], "error": "block mismatch",
                              "dry_blocks": runs[0]["blocks"], "gpu_blocks": len(r["t_dom"])}), flush=True)
            continue
        t_dom, t_gen = np.array(r["t_dom"]), np.array(r["t_gen"])
        t_gpu = [float(np.dot(d["dom_per_block"], t_dom) + np.dot(d["gen_per_block"], t_gen)) for d in runs]
        print(json.dumps({
            "label": r["label"], "options": r["options"], "config": r["config"], "circuit": r["circuit"],
            "p": r["p"], "n": r["n"], "shots": args.shots, "blocks": r["blocks"], "t_bw": r["t_bw"],
            "t_compile": r["t_compile"], "T_gpu": float(np.mean(t_gpu)),
            "passes": float(np.mean([d["block_passes"] for d in runs])),
            "general": float(np.mean([d["general_passes"] for d in runs])),
            "batches": float(np.mean([d["batches"] for d in runs])),
            "single_trajectory": float(t_dom.sum()),
        }), flush=True)
    configpatch.apply({})


if __name__ == "__main__":
    main()
