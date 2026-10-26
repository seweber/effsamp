"""A16: check and time tensor-core kernels (svpass Config.tensor_cores) against the CUDA-core kernels, block by block.

Compiles each workload's circuit once; for every distinct block, applies the dominant kernel of the
base Config (CUDA cores, complex64 or the --set dtype), of each --mode of `tensor_cores`, and of a
complex128 reference to the same random normalized state, and prints per workload and block the
relative L2 error of each against the reference and the pass times over the bandwidth time of the
stored type. The base Config's flags (e.g. stage_contraction) apply to the CUDA-core kernel only
where tensor cores take no stage.

Usage: a16_check.py --workloads circuit:noise:p,... --qubits n --mode tf32x3 [--mode ...] [--set key=value ...]
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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workloads", required=True)
    parser.add_argument("--qubits", type=int, default=26)
    parser.add_argument("--set", action="append", default=[])
    parser.add_argument("--mode", action="append", default=[])
    parser.add_argument("--label", default="")
    parser.add_argument("--no-time", action="store_true")
    args = parser.parse_args()
    options, config = configpatch.parse(args.set)
    configpatch.apply(config)
    n = args.qubits
    rng = np.random.default_rng(1)
    itemsize = 4 if options.get("dtype") == "complex32" else 8
    t_bw = bandwidth_time(n, itemsize)
    for workload in args.workloads.split(","):
        name, kind, p = workload.split(":")
        qc = circuits.make(name, n)
        sim = Simulator(maps=noise.maps(None if kind == "none" else kind, float(p)), **options)
        compiled, _, _ = sim._compiled(qc)
        base = compiled.config
        configs = {"cuda": base, **{m: dataclasses.replace(base, tensor_cores=m) for m in args.mode}}
        engines = {label: sim._engine(base) if label == "cuda" else Engine(c) for label, c in configs.items()}
        reference = Engine(dataclasses.replace(base, dtype="complex128", tensor_cores=""))
        amplitudes = rng.normal(size=2**n) + 1j * rng.normal(size=2**n)
        amplitudes /= np.linalg.norm(amplitudes)
        blocks = list(dict.fromkeys(compiled.blocks))
        start = time.perf_counter()
        futures = {(label, b): engines[label].compile(block.dominant_block) for label in engines for b, block in enumerate(blocks)}
        ref_futures = [reference.compile(block.dominant_block) for block in blocks]
        for f in [*futures.values(), *ref_futures]:
            f.result()
        t_compile = time.perf_counter() - start
        rows = []
        for b, block in enumerate(blocks):
            state = reference.states(amplitudes[None, :])
            ref_futures[b].result().apply(state)
            ref = state.amplitudes[0]
            del state
            row = {"gates": len(block.operations), "count": compiled.blocks.count(block)}
            for label, eng in engines.items():
                kernel = futures[(label, b)].result()
                state = eng.states(amplitudes.astype(np.complex64)[None, :])
                kernel.apply(state)
                out = state.amplitudes[0].astype(np.complex128)
                row[f"err_{label}"] = float(np.linalg.norm(out - ref) / np.linalg.norm(ref))
                row[f"norm_{label}"] = float(np.vdot(out, out).real - np.vdot(ref, ref).real)
                if not args.no_time:
                    row[f"t_{label}"] = timed(lambda: kernel.apply(state), eng.synchronize) / t_bw
                del state
            rows.append(row)
        print(json.dumps({"label": args.label, "circuit": name, "noise": kind, "p": float(p), "n": n,
                          "options": options, "config": config, "modes": args.mode, "t_bw": t_bw,
                          "t_compile": t_compile, "blocks": rows}), flush=True)
        sim._engines.clear()
        release_device_memory()


if __name__ == "__main__":
    main()
