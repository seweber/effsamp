"""A13: pass times of every block of a workload's circuit, by precision and block size, with each block's static work.

Like a7_blocks.py, but for the precision study: the bandwidth time is that of the stored type
(complex64: 8 bytes, complex32: 4 bytes per amplitude), only the dominant kernel and the masked
kernel of a single deviation are timed, and every block carries its static work (kernel_ops.py):
FP instructions and shared-memory accesses per amplitude. One JSON line per workload and setting.

Usage: a13_blocks.py --workloads circuit:noise:p,... --qubits n [--set key=value ...]
"""

import argparse
import json
import sys
import time

import cupy as cp
import numpy as np

sys.path.insert(0, "/work/bench")
import circuits  # noqa: E402
import configpatch  # noqa: E402
import noise  # noqa: E402
from a7_blocks import timed  # noqa: E402
from kernel_ops import block_work  # noqa: E402

from noisecirc import Simulator, release_device_memory  # noqa: E402


def bandwidth_time(n: int, itemsize: int) -> float:
    """Time to read and write 2**n amplitudes of ``itemsize`` bytes in place (CuPy scaling)."""
    dtype = cp.complex64 if itemsize == 8 else cp.float32
    a = cp.ones(2**n, dtype=dtype)
    s = cp.float32(1.0)
    t = timed(lambda: cp.multiply(a, s, out=a), cp.cuda.runtime.deviceSynchronize, reps=7)
    del a
    cp.get_default_memory_pool().free_all_blocks()
    return t


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workloads", required=True)
    parser.add_argument("--qubits", type=int, default=26)
    parser.add_argument("--set", action="append", default=[])
    parser.add_argument("--label", default="")
    parser.add_argument("--no-masked", action="store_true")
    args = parser.parse_args()
    options, config = configpatch.parse(args.set)
    configpatch.apply(config)
    n = args.qubits
    itemsize = 4 if options.get("dtype") == "complex32" else 8
    t_bw = bandwidth_time(n, itemsize)
    for workload in args.workloads.split(","):
        name, kind, p = workload.split(":")
        p = float(p)
        qc = circuits.make(name, n)
        sim = Simulator(maps=noise.maps(None if kind == "none" else kind, p), **options)
        start = time.perf_counter()
        compiled, bps, batch = sim._compiled(qc)
        engine = sim._engine(compiled.config)
        futures = [engine.compile(block.dominant_block) for block in compiled.blocks]
        if not args.no_masked:
            futures += [engine.compile(block.masked_block) for block in compiled.blocks if block.has_choices]
        for f in futures:
            f.result()
        t_compile = time.perf_counter() - start
        state = engine.canonical_state(n, np.zeros(1, dtype=np.int64))
        first = engine.compile(compiled.blocks[0].dominant_block).result()
        first.apply(state)  # a row of its own
        seen = {}
        rows = []
        for block in compiled.blocks:
            if block not in seen:
                dom = engine.compile(block.dominant_block).result()
                td = timed(lambda: dom.apply(state), engine.synchronize)
                tm = td
                if block.has_choices and not args.no_masked:
                    masked_block = block.masked_block
                    masked = engine.compile(masked_block).result()
                    host = block.choices(block.dominant_codes[:, None])
                    multi = [i for i, placed in enumerate(block.operations) if placed.operation.stack.shape[0] > 1]
                    i = multi[len(multi) // 2]
                    host[i, 0] = (host[i, 0] + 1) % block.operations[i].operation.stack.shape[0]
                    choice_rows = engine.upload(np.concatenate([host, masked_block.stage_mask(host)]))
                    tm = timed(lambda: masked.apply(state, choice_rows), engine.synchronize)
                seen[block] = {"t_dom": td, "t_mask": tm, "gates": len(block.operations),
                               **block_work(block.dominant_block, compiled.config)}
            rows.append(seen[block])
        print(json.dumps({
            "label": args.label, "circuit": name, "noise": kind, "p": p, "n": n, "options": options,
            "config": config, "blocks": len(compiled.blocks), "t_bw": t_bw, "t_compile": t_compile,
            "per_block": rows,
        }), flush=True)
        del state, first
        sim._engines.clear()
        release_device_memory()


if __name__ == "__main__":
    main()
