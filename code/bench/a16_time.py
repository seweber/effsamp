"""A16: trajectory time of a workload's dominant kernels for several kernel-generation variants.

For each workload and each --variant (comma-separated key=value Config overrides on top of --set,
e.g. "tensor_cores=f16,tensor_unroll=4,min_registers=96"; "base" for none), compiles the dominant
kernel of every block and times one pass of each on a basis state; prints the mean pass time over
the bandwidth time of the stored type, weighted by how often each block occurs (one trajectory).
svpass's in-memory kernel cache is cleared per variant.

Usage: a16_time.py --workloads circuit:noise:p,... --qubits n [--set key=value ...] --variant SPEC [--variant ...]
"""

import argparse
import dataclasses
import json
import sys
import time

import numpy as np

sys.path.insert(0, "/work/bench")
import circuits  # noqa: E402
import configpatch  # noqa: E402
import noise  # noqa: E402
from a7_blocks import timed  # noqa: E402
from a13_blocks import bandwidth_time  # noqa: E402

from noisecirc import Simulator, release_device_memory  # noqa: E402
from svpass import Engine  # noqa: E402
from svpass import engine as svpass_engine  # noqa: E402


def parse_variant(spec: str) -> dict:
    """Return the Config overrides of a variant spec."""
    if spec == "base":
        return {}
    overrides = {}
    for item in spec.split(","):
        key, value = item.split("=")
        overrides[key] = value if key in ("tensor_cores", "dtype") else float(value) if key == "tensor_threshold" else (
            bool(int(value)) if key in ("stage_fusion", "rotation_form", "additive_addresses", "stage_contraction") else int(value))
    return overrides


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workloads", required=True)
    parser.add_argument("--qubits", type=int, default=26)
    parser.add_argument("--set", action="append", default=[])
    parser.add_argument("--variant", action="append", default=[])
    parser.add_argument("--label", default="")
    args = parser.parse_args()
    options, config = configpatch.parse(args.set)
    configpatch.apply(config)
    n = args.qubits
    itemsize = 4 if options.get("dtype") == "complex32" else 8
    t_bw = bandwidth_time(n, itemsize)
    for workload in args.workloads.split(","):
        name, kind, p = workload.split(":")
        qc = circuits.make(name, n)
        sim = Simulator(maps=noise.maps(None if kind == "none" else kind, float(p)), **options)
        compiled, _, _ = sim._compiled(qc)
        distinct = list(dict.fromkeys(compiled.blocks))
        counts = [compiled.blocks.count(block) for block in distinct]
        result, compile_times = {}, {}
        for spec in args.variant:
            svpass_engine._compiled.clear()
            engine = Engine(dataclasses.replace(compiled.config, **parse_variant(spec)))
            start = time.perf_counter()
            kernels = [f.result() for f in [engine.compile(b.dominant_block) for b in distinct]]
            compile_times[spec] = time.perf_counter() - start
            state = engine.canonical_state(n, np.zeros(1, dtype=np.int64))
            kernels[0].apply(state)  # a row of its own
            times = [timed(lambda: k.apply(state), engine.synchronize) for k in kernels]
            result[spec] = sum(c * t for c, t in zip(counts, times)) / (sum(counts) * t_bw)
            del state, kernels, engine
            release_device_memory()
        print(json.dumps({"label": args.label, "circuit": name, "noise": kind, "p": float(p), "n": n,
                          "options": options, "config": config, "blocks": len(compiled.blocks), "t_bw": t_bw,
                          "t_over_tbw": result, "t_compile": compile_times}), flush=True)


if __name__ == "__main__":
    main()
