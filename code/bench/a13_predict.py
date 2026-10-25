"""A13 follow-up: predicted dominant-pass times of kernel designs, from SASS counts and the refitted model.

For the five A13 workloads at n = 26 and a base configuration (default: A14 kernels, 4-qubit stages,
complex32), counts each block's SASS instructions per amplitude (a13_sass.py) for the generated kernel
with and without `additive_addresses`, and estimates a kernel whose diagonal operations need no
register qubits: the stages of a13_stage_estimate.py (free diagonals), with 2 shared accesses and the
per-stage integer instructions (fitted over the blocks: integer = a + b * stages) removed for every
stage saved, the floating-point instructions unchanged. The time of each is predicted with the
model "fp+shared+integer" of data/a13-analysis/refit.json and summed over the blocks (one trajectory),
relative to the base kernel.

Usage: a13_predict.py [--set key=value ...] (local, CPU; needs $NVDISASM)
"""

import argparse
import dataclasses
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import circuits  # noqa: E402
import configpatch  # noqa: E402
import noise  # noqa: E402
from a13_sass import cubin, opcodes, per_amplitude, sass  # noqa: E402
from a13_stage_estimate import WORKLOADS, stages  # noqa: E402
from dryrun import compile_like_simulator  # noqa: E402

from noisecirc import Simulator  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
FP_RATE = 23.0e12
T_BW = {"complex64": 0.599e-3, "complex32": 0.347e-3}  # measured at n = 26 (A13 sweeps)


def predict(c: dict, slots: float, model: dict) -> float:
    k = model["coefficients"]
    return max(model["floor"], (k["F"] * c["F"] + k["L"] * c["L"] + k["I"] * c["I"]) / slots)


def features(s: dict) -> dict:
    return {"F": s["fp32"] + s["fp64"], "L": s["shared"], "I": s["integer"] + s["move"] + s.get("local", 0.0)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--set", action="append", default=["stage_fusion=1", "rotation_form=1", "stage_qubits=4", "dtype=complex32"])
    args = parser.parse_args()
    options, config = configpatch.parse(args.set)
    configpatch.apply(config)
    model = json.loads((ROOT / "data" / "a13-analysis" / "refit.json").read_text())["fp+shared+integer"]
    for name, p in WORKLOADS:
        qc = circuits.make(name, 26)
        compiled, _, _ = compile_like_simulator(qc, Simulator(maps=noise.maps("damping", p), **options))
        cfg = dataclasses.replace(compiled.config, threads=1024)
        slots = T_BW[cfg.dtype] / 2**26 * FP_RATE
        rows = []
        for block in compiled.blocks:
            dom = block.dominant_block
            k = len(dom.tile(cfg))
            base = features(per_amplitude(opcodes(sass(cubin(dom, cfg))), cfg, k))
            add_cfg = dataclasses.replace(cfg, additive_addresses=True)
            additive = features(per_amplitude(opcodes(sass(cubin(dom, add_cfg))), add_cfg, k))
            ops = []
            for op in dom.operations:
                m = np.asarray(op.kraus[0])
                ops.append((tuple(int(q) for q in op.targets), bool(np.abs(m - np.diag(np.diag(m))).max() < 1e-12)))
            rows.append({"base": base, "additive": additive, "stages": dom.n_stages,
                         "free_stages": stages(ops, cfg.stage_qubits, True)})
        # Per-stage integer instructions per amplitude, fitted over this circuit's blocks (additive kernels).
        st = np.array([r["stages"] for r in rows], dtype=float)
        ii = np.array([r["additive"]["I"] for r in rows])
        slope = float(np.polyfit(st, ii, 1)[0]) if len(set(st)) > 1 else 20.0 / (1 << cfg.stage_qubits)
        totals = {"base": 0.0, "additive": 0.0, "free_diagonals": 0.0}
        for r in rows:
            saved = r["stages"] - r["free_stages"]
            free = dict(r["additive"])
            free["L"] = max(2.0, free["L"] - 2 * saved)
            free["I"] = max(0.0, free["I"] - slope * saved)
            totals["base"] += predict(r["base"], slots, model)
            totals["additive"] += predict(r["additive"], slots, model)
            totals["free_diagonals"] += predict(free, slots, model)
        print(json.dumps({"circuit": name, "dtype": cfg.dtype, "stage_qubits": cfg.stage_qubits,
                          "blocks": len(rows), "per_stage_integer": slope,
                          "t_over_t_bw_base": totals["base"] / len(rows),
                          "additive_vs_base": totals["additive"] / totals["base"],
                          "free_diagonals_vs_base": totals["free_diagonals"] / totals["base"],
                          "mean_stages": float(st.mean()), "mean_free_stages": float(np.mean([r["free_stages"] for r in rows]))}),
              flush=True)


if __name__ == "__main__":
    main()
