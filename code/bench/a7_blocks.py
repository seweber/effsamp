"""A7/A8: time every block of a workload's compiled circuit, for one setting of noisecirc's parameters.

A workload is a circuit, a noise channel and a strength; the setting is a set of Simulator options
(max_fused_qudits, max_operations, pinned_bytes, max_oversampling) and svpass Config overrides
(stage_qubits, group_amplitudes, threads, min_registers; see configpatch.py). Every distinct block
is timed on one state of n qubits with its dominant kernel and, if it has choices, its general kernel
(all operations on their dominant choice, the same work through the switching code). Prints one JSON
line per workload with the times per block index, the compile time, and the bandwidth time t_bw.

Usage: a7_blocks.py --workloads circuit:noise:p,... --qubits n [--set key=value ...]
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

from noisecirc import Simulator, release_device_memory  # noqa: E402


def timed(apply, sync, reps: int = 3, inner: int = 5) -> float:
    apply()
    sync()
    times = []
    for _ in range(reps):
        start = time.perf_counter()
        for _ in range(inner):
            apply()
        sync()
        times.append((time.perf_counter() - start) / inner)
    return float(np.median(times))


def bandwidth_time(n: int) -> float:
    a = cp.ones(2**n, dtype=cp.complex64)
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
    args = parser.parse_args()
    options, config = configpatch.parse(args.set)
    configpatch.apply(config)
    n = args.qubits
    t_bw = bandwidth_time(n)
    for workload in args.workloads.split(","):
        name, kind, p = workload.split(":")
        p = float(p)
        qc = circuits.make(name, n)
        sim = Simulator(maps=noise.maps(None if kind == "none" else kind, p), **options)
        start = time.perf_counter()
        compiled, bps, batch = sim._compiled(qc)
        engine = sim._engine(compiled.config)
        futures = [f for block in compiled.blocks for f in block.kernels(engine)]
        for f in futures:
            f.result()
        t_compile = time.perf_counter() - start
        state = engine.canonical_state(n, np.zeros(1, dtype=np.int64))
        first = engine.compile(compiled.blocks[0].dominant_block).result()
        first.apply(state)  # a row of its own
        seen = {}
        t_dom, t_gen, gates = [], [], []
        for block in compiled.blocks:
            if block not in seen:
                dom = engine.compile(block.dominant_block).result()
                td = timed(lambda: dom.apply(state), engine.synchronize)
                tg = td
                if block.has_choices:
                    gen = engine.compile(block.engine_block).result()
                    choices = engine.upload(block.choices(block.dominant_codes[:, None]))
                    tg = timed(lambda: gen.apply(state, choices), engine.synchronize)
                seen[block] = (td, tg)
            td, tg = seen[block]
            t_dom.append(td)
            t_gen.append(tg)
            gates.append(len(block.operations))
        print(json.dumps({
            "label": args.label, "circuit": name, "noise": kind, "p": p, "n": n, "options": options,
            "config": config, "blocks": len(compiled.blocks), "blocks_per_segment": bps, "max_batch": batch,
            "t_bw": t_bw, "t_compile": t_compile, "t_dom": t_dom, "t_gen": t_gen, "gates": gates,
            "distinct": len(seen),
        }), flush=True)
        del state, first
        sim._engines.clear()
        release_device_memory()


if __name__ == "__main__":
    main()
