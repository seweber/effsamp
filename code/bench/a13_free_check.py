"""A13: check free diagonals (svpass Config.free_diagonals) on whole circuits against an independent reference.

For each workload, compiles the circuit with and without `free_diagonals` (the flag changes noisecirc's
stage partition); runs the no-error trajectory (dominant kernels) of the flagged compilation in
complex64 and of the plain one in complex128, and prints the total variation distance, the relative
error of the squared norm and the infidelity, with the mean stages per block of both.

Usage: a13_free_check.py --workloads circuit:noise:p,... --qubits n [--set key=value ...]
"""

import argparse
import dataclasses
import json
import sys

import numpy as np

sys.path.insert(0, "/work/bench")
import circuits  # noqa: E402
import configpatch  # noqa: E402
import noise  # noqa: E402
from a16_accuracy import final_state  # noqa: E402

from noisecirc import Simulator  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workloads", required=True)
    parser.add_argument("--qubits", type=int, default=24)
    parser.add_argument("--set", action="append", default=[])
    args = parser.parse_args()
    options, config = configpatch.parse(args.set)
    n = args.qubits
    for workload in args.workloads.split(","):
        name, kind, p = workload.split(":")
        qc = circuits.make(name, n)
        compiled = {}
        for free in (False, True):
            configpatch.apply({**config, "free_diagonals": free})
            sim = Simulator(maps=noise.maps(None if kind == "none" else kind, float(p)), **options)
            compiled[free] = sim._compiled(qc)[0]
        plain, flagged = compiled[False], compiled[True]
        ref = final_state(plain, dataclasses.replace(plain.config, dtype="complex128"), n)
        psi = final_state(flagged, flagged.config, n)
        pref, prob = np.abs(ref) ** 2, np.abs(psi) ** 2
        print(json.dumps({
            "circuit": name, "noise": kind, "p": float(p), "n": n, "options": options, "config": config,
            "stages_plain": float(np.mean([b.dominant_block.n_stages for b in plain.blocks])),
            "stages_free": float(np.mean([b.dominant_block.n_stages for b in flagged.blocks])),
            "norm_rel_err": float(prob.sum() / pref.sum() - 1),
            "tvd": float(0.5 * np.abs(prob / prob.sum() - pref / pref.sum()).sum()),
            "infidelity": float(1 - abs(np.vdot(ref, psi)) ** 2 / (pref.sum() * prob.sum())),
        }), flush=True)


if __name__ == "__main__":
    main()
