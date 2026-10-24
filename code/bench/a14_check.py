"""A14: check and time a kernel-generation variant against the default on every block of a workload.

Compiles each workload's circuit twice, with svpass's default Config and with the overrides given by
--variant (e.g. stage_fusion=1), and for every distinct block applies both dominant kernels (and
the masked kernels of one deviation) to the same random state. Prints per workload the largest
relative deviation of the amplitudes and the pass times of both, with the static work of both.

Usage: a14_check.py --workloads circuit:noise:p,... --qubits n --variant key=value [--variant ...] [--set ...]
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
from kernel_ops import block_work  # noqa: E402

from noisecirc import Simulator, release_device_memory  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workloads", required=True)
    parser.add_argument("--qubits", type=int, default=26)
    parser.add_argument("--set", action="append", default=[])
    parser.add_argument("--variant", action="append", default=[])
    parser.add_argument("--label", default="")
    parser.add_argument("--no-masked", action="store_true")
    args = parser.parse_args()
    options, config = configpatch.parse(args.set)
    variant = {}
    for item in args.variant:
        key, value = item.split("=")
        variant[key] = bool(int(value)) if key in ("stage_fusion", "rotation_form") else int(value)
    configpatch.apply(config)
    n = args.qubits
    rng = np.random.default_rng(1)
    for workload in args.workloads.split(","):
        name, kind, p = workload.split(":")
        qc = circuits.make(name, n)
        sim = Simulator(maps=noise.maps(None if kind == "none" else kind, float(p)), **options)
        compiled, _, _ = sim._compiled(qc)
        base_config = compiled.config
        var_config = dataclasses.replace(base_config, **variant)
        engine = sim._engine(base_config)
        from svpass import Engine

        var_engine = Engine(var_config)
        amplitudes = (rng.normal(size=2**n) + 1j * rng.normal(size=2**n)).astype(np.complex64)
        amplitudes /= np.linalg.norm(amplitudes)
        start = time.perf_counter()
        pairs = []
        seen = set()
        for block in compiled.blocks:
            if block in seen:
                continue
            seen.add(block)
            kinds = [("dom", block.dominant_block, None)]
            if block.has_choices and not args.no_masked:
                host = block.choices(block.dominant_codes[:, None])
                multi = [i for i, placed in enumerate(block.operations) if placed.operation.stack.shape[0] > 1]
                i = multi[len(multi) // 2]
                host[i, 0] = (host[i, 0] + 1) % block.operations[i].operation.stack.shape[0]
                kinds.append(("mask", block.masked_block, np.concatenate([host, block.masked_block.stage_mask(host)])))
            for label, engine_block, choices in kinds:
                pairs.append((block, label, engine_block, choices,
                              engine.compile(engine_block), var_engine.compile(engine_block)))
        for pair in pairs:
            pair[4].result(), pair[5].result()
        t_compile = time.perf_counter() - start
        rows = []
        for block, label, engine_block, choices, fa, fb in pairs:
            outs, times = [], []
            for eng, fut in ((engine, fa), (var_engine, fb)):
                kernel = fut.result()
                state = eng.states(amplitudes[None, :])
                dev_choices = None if choices is None else eng.upload(choices)
                kernel.apply(state, dev_choices) if dev_choices is not None else kernel.apply(state)
                outs.append(state.amplitudes[0])
                del state
                state = eng.states(amplitudes[None, :])
                apply = (lambda: kernel.apply(state, dev_choices)) if dev_choices is not None else (lambda: kernel.apply(state))
                times.append(timed(apply, eng.synchronize))
                del state
            deviation = float(np.abs(outs[0] - outs[1]).max() / np.abs(outs[0]).max())
            rows.append({"kind": label, "gates": len(block.operations), "deviation": deviation,
                         "t_base": times[0], "t_variant": times[1],
                         "work_base": block_work(engine_block, base_config),
                         "work_variant": block_work(engine_block, var_config)})
        print(json.dumps({"label": args.label, "circuit": name, "noise": kind, "p": float(p), "n": n,
                          "options": options, "config": config, "variant": variant,
                          "t_compile": t_compile, "blocks": rows}), flush=True)
        sim._engines.clear()
        release_device_memory()


if __name__ == "__main__":
    main()
