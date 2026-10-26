"""A16: accuracy of tensor-core kernel variants over a whole circuit, against complex128.

Like a13_accuracy.py: applies every block of a workload's compiled circuit (dominant kernels: the
no-error trajectory) to |0>, once per --variant (comma-separated Config overrides, dtype included,
e.g. "dtype=complex32,tensor_cores=f16,min_registers=96"; "base" for the compiled Config), and
compares the final probabilities with complex128 kernels of the same blocks: total variation
distance, relative error of the squared norm (what noisecirc's acceptance uses) and infidelity.

Usage: a16_accuracy.py --workloads circuit:noise:p,... --qubits n [--set key=value ...] --variant SPEC [...]
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
from a16_time import parse_variant  # noqa: E402

from noisecirc import Simulator, release_device_memory  # noqa: E402
from svpass import Engine  # noqa: E402
from svpass import engine as svpass_engine  # noqa: E402


def final_state(compiled, config, n: int) -> np.ndarray:
    """The no-error trajectory's final amplitudes with kernels of ``config``."""
    svpass_engine._compiled.clear()
    engine = Engine(config)
    state = engine.canonical_state(n, np.zeros(1, dtype=np.int64))
    for block in compiled.blocks:
        engine.compile(block.dominant_block).result().apply(state)
    out = state.amplitudes[0].astype(np.complex128)
    del state, engine
    release_device_memory()
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workloads", required=True)
    parser.add_argument("--qubits", type=int, default=24)
    parser.add_argument("--set", action="append", default=[])
    parser.add_argument("--variant", action="append", default=[])
    args = parser.parse_args()
    options, config = configpatch.parse(args.set)
    configpatch.apply(config)
    n = args.qubits
    for workload in args.workloads.split(","):
        name, kind, p = workload.split(":")
        qc = circuits.make(name, n)
        sim = Simulator(maps=noise.maps(None if kind == "none" else kind, float(p)), **options)
        compiled, _, _ = sim._compiled(qc)
        ref = final_state(compiled, dataclasses.replace(compiled.config, dtype="complex128", tensor_cores=""), n)
        pref = np.abs(ref) ** 2
        for spec in args.variant:
            psi = final_state(compiled, dataclasses.replace(compiled.config, **parse_variant(spec)), n)
            prob = np.abs(psi) ** 2
            print(json.dumps({
                "circuit": name, "noise": kind, "p": float(p), "n": n, "variant": spec, "options": options,
                "config": config, "blocks": len(compiled.blocks),
                "norm_rel_err": float(prob.sum() / pref.sum() - 1),
                "tvd": float(0.5 * np.abs(prob / prob.sum() - pref / pref.sum()).sum()),
                "infidelity": float(1 - abs(np.vdot(ref, psi)) ** 2 / (pref.sum() * prob.sum())),
            }), flush=True)
        sim._engines.clear()


if __name__ == "__main__":
    main()
