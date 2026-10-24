"""A13: accuracy of complex32 against complex64 (and complex128 as reference) for a trajectory through a circuit.

Applies every block of the circuit's compiled noise-free... (damped, dominant kernels: the no-error
trajectory) to |0>, in each precision with the same kernel options, and compares the final
probabilities: total variation distance to complex128, the squared norm (the acceptance a sampler
would use) relative to complex128's, and the fidelity. One JSON line per circuit and precision.

Usage: a13_accuracy.py --workloads circuit:noise:p,... --qubits n [--set key=value ...]
"""
import argparse
import json
import sys

import numpy as np

sys.path.insert(0, "/work/bench")
import circuits  # noqa: E402
import configpatch  # noqa: E402
import noise  # noqa: E402

from noisecirc import Simulator, release_device_memory  # noqa: E402

parser = argparse.ArgumentParser()
parser.add_argument("--workloads", required=True)
parser.add_argument("--qubits", type=int, default=24)
parser.add_argument("--set", action="append", default=[])
args = parser.parse_args()
options, config = configpatch.parse(args.set)
configpatch.apply(config)
n = args.qubits
for workload in args.workloads.split(","):
    name, kind, p = workload.split(":")
    qc = circuits.make(name, n)
    finals = {}
    for dtype in ("complex128", "complex64", "complex32"):
        sim = Simulator(maps=noise.maps(None if kind == "none" else kind, float(p)), dtype=dtype, **options)
        compiled, _, _ = sim._compiled(qc)
        engine = sim._engine(compiled.config)
        state = engine.canonical_state(n, np.zeros(1, dtype=np.int64))
        for block in compiled.blocks:
            engine.compile(block.dominant_block).result().apply(state)
        finals[dtype] = state.amplitudes[0].astype(np.complex128)
        del state
        sim._engines.clear()
        release_device_memory()
    ref = finals["complex128"]
    pref = np.abs(ref) ** 2
    for dtype in ("complex64", "complex32"):
        psi = finals[dtype]
        prob = np.abs(psi) ** 2
        print(json.dumps({
            "circuit": name, "noise": kind, "p": float(p), "n": n, "dtype": dtype, "options": options, "config": config,
            "norm_rel_err": float(prob.sum() / pref.sum() - 1),
            "tvd": float(0.5 * np.abs(prob / prob.sum() - pref / pref.sum()).sum()),
            "infidelity": float(1 - abs(np.vdot(ref, psi)) ** 2 / (pref.sum() * prob.sum())),
        }), flush=True)
