"""A13 follow-up: refit the pass-time model of the A13 sweeps with the SASS instruction counts.

Reads the per-block rows of a13_sass_blocks.py (data/*-a13-sass-counts-of-timed-blocks-*/stdout.txt):
measured dominant pass time, t_bw of the stored type, and the instructions per amplitude by class.
Fits, by least squares on log(predicted / measured), models of the form

    t / t_bw = max(c0, sum_k a_k X_k / t_amp)  or  max(c0, issue, shared),

with t_amp = t_bw / 2**26 the bandwidth time of one amplitude, and reports the rms log error and
the fitted time per instruction in units of one FP32 instruction issued at the H100's FMA peak.
Writes data/a13-analysis/refit.json.

Usage: a13_refit.py (local)
"""

import glob
import json
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

ROOT = Path(__file__).resolve().parents[2]
N = 26
# FP32 instructions per second per amplitude-lane at the measured FMA peak (46 TFLOP/s, A13).
FP_RATE = 23.0e12


def load() -> list[dict]:
    rows, seen = [], set()
    for path in sorted(glob.glob(str(ROOT / "data" / "*-a13-sass-counts-of-timed-blocks-*" / "stdout.txt"))):
        for line in open(path):
            r = json.loads(line)
            key = (r["run"], r["circuit"], r["t_dom"])
            if key in seen or not r.get("exact", True):
                continue
            seen.add(key)
            s = r["sass"]
            r["F"] = s["fp32"] + s["fp64"]
            r["L"] = s["shared"]
            # Rows of part 1 predate the "local" class: spills counted as integer there.
            r["I"] = s["integer"] + s["move"] + s.get("local", 0.0)
            r["C"] = s["control"]
            r["V"] = s["convert"] + s["global"]
            # Time of one amplitude at the bandwidth of the stored type, in FP32-instruction slots.
            r["slots"] = r["t_bw"] / 2**N * FP_RATE
            r["y"] = r["t_dom"] / r["t_bw"]
            rows.append(r)
    return rows


MODELS = {
    "fp+shared (A13 Eq. 1)": (["F", "L"], "sum"),
    "fp+shared+integer": (["F", "L", "I"], "sum"),
    "fp+shared+integer+control": (["F", "L", "I", "C"], "sum"),
    "all issued, one price": (["F+L+I+C+V"], "sum"),
    "issue | shared bandwidth": (["F+I+C+V", "L"], "max"),
    "issue + shared bandwidth": (["F+I+C+V", "L"], "sum"),
}


def feature(r: dict, name: str) -> float:
    return sum(r[k] for k in name.split("+"))


def fit(rows: list[dict], names: list[str], combine: str) -> dict:
    x = np.array([[feature(r, n) / r["slots"] for n in names] for r in rows])
    y = np.array([r["y"] for r in rows])

    def pred(p):
        floor, coef = np.exp(p[0]), np.exp(p[1:])
        terms = x * coef
        body = terms.sum(axis=1) if combine == "sum" else terms.max(axis=1)
        return np.maximum(floor, body)

    def loss(p):
        return np.mean(np.log(pred(p) / y) ** 2)

    best = None
    for start in ([0.1] + [0.0] * len(names), [0.2] + [-0.5] * len(names), [0.0] + [0.5] * len(names)):
        res = minimize(loss, np.array(start), method="Nelder-Mead", options={"maxiter": 20000, "xatol": 1e-8, "fatol": 1e-12})
        if best is None or res.fun < best.fun:
            best = res
    p = best.x
    return {"rms_log": float(np.sqrt(best.fun)), "floor": float(np.exp(p[0])),
            "coefficients": dict(zip(names, np.exp(p[1:]).round(4).tolist())), "blocks": len(rows)}


def main() -> None:
    rows = load()
    out = {}
    for label, (names, combine) in MODELS.items():
        out[label] = fit(rows, names, combine)
        print(f"{label:32s} {json.dumps(out[label])}")
    means = {c: {k: float(np.mean([r[k] for r in rows if c in r["run"]])) for k in ("F", "L", "I", "C", "V")}
             for c in ("complex64", "complex32", "fused-kernels")}
    out["mean_counts"] = means
    print(json.dumps(means))
    dest = ROOT / "data" / "a13-analysis" / "refit.json"
    dest.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
