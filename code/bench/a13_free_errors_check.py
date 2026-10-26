"""A13: check the error kernels (masked and general) of blocks partitioned with free diagonals, against NumPy.

With svpass Config.free_diagonals, noisecirc partitions stages so that operations whose dominant choice
is diagonal take no width; kernels that apply other choices split such stages into sub-stages. For
each workload (at a small register), every distinct block with choices, and several random choice
vectors (the dominant choices with 1 to 3 operations leaving them),
applies the masked and the general kernel to a random state on the GPU and the same operations one by
one in NumPy (complex128), and prints the largest L2 deviation relative to the input's norm.

Usage: a13_free_errors_check.py --workloads circuit:noise:p,... --qubits n [--set key=value ...] [--draws k]
"""

import argparse
import json
import sys

import dataclasses

import numpy as np

sys.path.insert(0, "/work/bench")
import circuits  # noqa: E402
import configpatch  # noqa: E402
import noise  # noqa: E402

from noisecirc import Simulator, release_device_memory  # noqa: E402
from svpass import testing  # noqa: E402
from svpass.cuda import codegen  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workloads", required=True)
    parser.add_argument("--qubits", type=int, default=10)
    parser.add_argument("--set", action="append", default=[])
    parser.add_argument("--draws", type=int, default=4)
    args = parser.parse_args()
    options, config = configpatch.parse(args.set)
    configpatch.apply(config)
    n = args.qubits
    rng = np.random.default_rng(7)
    for workload in args.workloads.split(","):
        name, kind, p = workload.split(":")
        sim = Simulator(maps=noise.maps(kind, float(p)), **options)
        compiled = sim._compiled(circuits.make(name, n))[0]
        engine = sim._engine(compiled.config)
        numpy_engine = testing.engine(dataclasses.replace(compiled.config, dtype="complex128"))
        worst = {"masked": 0.0, "general": 0.0}
        substaged = 0
        checked = 0
        for block in dict.fromkeys(compiled.blocks):
            if not block.has_choices:
                continue
            general = block.engine_block
            n_choices = general.n_choices
            for _ in range(args.draws):
                # The dominant choices with 1 to 3 random operations leaving them, as trajectories do;
                # uniformly random choices chain jumps that annihilate the state.
                choices = block.choices(block.dominant_codes[:, None])[:, 0].astype(np.int64)
                multi = np.flatnonzero(n_choices > 1)
                for i in rng.choice(multi, size=min(len(multi), int(rng.integers(1, 4))), replace=False):
                    choices[i] = (choices[i] + 1 + rng.integers(n_choices[i] - 1)) % n_choices[i]
                amplitudes = rng.normal(size=2**n) + 1j * rng.normal(size=2**n)
                host = choices[:, None].astype(np.int32)
                reference = numpy_engine.states(amplitudes[None, :])
                numpy_engine.compile(general).result().apply(reference, numpy_engine.upload(host))
                expected = reference.amplitudes[0]
                for label, engine_block in (("masked", block.masked_block), ("general", general)):
                    rows = np.concatenate([host, engine_block.stage_mask(host)]) if label == "masked" else host
                    kernel = engine.compile(engine_block).result()
                    state = engine.states(amplitudes.astype(np.complex64)[None, :])
                    kernel.apply(state, engine.upload(rows))
                    out = state.amplitudes[0].astype(np.complex128)
                    # Relative to the input, which single-precision rounding scales with: two jumps on
                    # one qubit annihilate the output, so relative to the output is meaningless.
                    worst[label] = max(worst[label], float(np.linalg.norm(out - expected) / np.linalg.norm(amplitudes)))
                    del state
                checked += 1
            substaged += sum(stage.parts is not None for stage in codegen._stages(general, compiled.config))
        print(json.dumps({"circuit": name, "noise": kind, "p": float(p), "n": n, "options": options, "config": config,
                          "checked": checked, "substaged_stages": substaged, "max_rel_err": worst}), flush=True)
        sim._engines.clear()
        release_device_memory()


if __name__ == "__main__":
    main()
