"""A2: where the time of a NoiseCirc run goes: GPU passes against host work.

The run is repeated with svpass's ``Kernel.apply`` (launches: host cost, rows, kernel),
``States.squared_norms`` (where the host waits for the GPU), the sampler's proposals and its
classical thinning wrapped by timers. Afterwards every kernel the run launched is timed alone, per
row, on one state, so that the run's GPU time is estimated as the sum over launches of rows x time
per row. Prints one JSON line per point.
"""

import argparse
import json
import sys
import time
from collections import defaultdict

import numpy as np

sys.path.insert(0, "/work/bench")
import circuits  # noqa: E402
import noise  # noqa: E402

import svpass.engine  # noqa: E402
import svpass.states  # noqa: E402
from noisecirc import Simulator, release_device_memory  # noqa: E402

sample_module = sys.modules["noisecirc.sampling.sample"]
TIMERS = defaultdict(float)
COUNTS = defaultdict(int)
LAUNCHES = defaultdict(int)  # (kernel id) -> rows
KERNELS = {}


def wrap(owner, name, label):
    original = getattr(owner, name)

    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return original(*args, **kwargs)
        finally:
            TIMERS[label] += time.perf_counter() - start
            COUNTS[label] += 1

    setattr(owner, name, wrapper)
    return original


original_apply = svpass.engine.Kernel.apply


def apply(self, states, choices=None, *, scales=None, where=None):
    rows = len(states) if where is None else int(np.count_nonzero(where))
    LAUNCHES[id(self)] += rows
    KERNELS[id(self)] = self
    start = time.perf_counter()
    try:
        return original_apply(self, states, choices, scales=scales, where=where)
    finally:
        TIMERS["apply_host"] += time.perf_counter() - start
        COUNTS["apply_host"] += 1


def time_per_row(kernel, engine, n, reps=5):
    state = engine.canonical_state(n, np.zeros(1, dtype=np.int64))
    kernel_choices = None
    if not kernel.fixed:
        kernel_choices = engine.upload(np.zeros((kernel.n_operations, 1), dtype=np.int32))
    original_apply(kernel, state, kernel_choices)
    engine.synchronize()
    times = []
    for _ in range(reps):
        start = time.perf_counter()
        for _ in range(5):
            original_apply(kernel, state, kernel_choices)
        engine.synchronize()
        times.append((time.perf_counter() - start) / 5)
    return float(np.median(times))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--circuits", default="brickwork")
    parser.add_argument("--qubits", type=int, default=26)
    parser.add_argument("--noise", default="damping")
    parser.add_argument("--ps", default="0.001")
    parser.add_argument("--shots", type=int, default=1000)
    parser.add_argument("--option", action="append", default=[])
    args = parser.parse_args()
    options = {}
    for item in args.option:
        key, value = item.split("=")
        options[key] = float(value) if "." in value or value == "inf" else int(value)

    svpass.engine.Kernel.apply = apply
    wrap(svpass.states.States, "squared_norms", "squared_norms")
    wrap(svpass.states.States, "sample", "measure")
    wrap(sample_module._Context, "propose", "propose")
    wrap(sample_module, "log_oversampling", "thinning")
    n = args.qubits
    for name in args.circuits.split(","):
        qc = circuits.make(name, n)
        for p in [float(x) for x in args.ps.split(",")]:
            sim = Simulator(maps=noise.maps(args.noise, p), **options)
            sim.run(qc, shots=args.shots, seed=0)  # compiles
            TIMERS.clear()
            COUNTS.clear()
            LAUNCHES.clear()
            start = time.perf_counter()
            result = sim.run(qc, shots=args.shots, seed=1)
            total = time.perf_counter() - start
            timers, counts, launches = dict(TIMERS), dict(COUNTS), dict(LAUNCHES)
            compiled, _, _ = sim._compiled(qc)
            engine = sim._engine(compiled.config)
            gpu = 0.0
            per_kernel = []
            for key, rows in launches.items():
                kernel = KERNELS[key]
                t = time_per_row(kernel, engine, n)
                gpu += rows * t
                per_kernel.append((rows, t, kernel.fixed, kernel.n_operations))
            d = result.diagnostics
            print(json.dumps({
                "circuit": name, "n": n, "p": p, "shots": args.shots, "options": options, "time": total,
                "gpu_estimate": gpu, "timers": timers, "counts": counts,
                "rows_fixed": sum(r for r, _, f, _ in per_kernel if f),
                "rows_general": sum(r for r, _, f, _ in per_kernel if not f),
                "gpu_fixed": sum(r * t for r, t, f, _ in per_kernel if f),
                "gpu_general": sum(r * t for r, t, f, _ in per_kernel if not f),
                **{k: float(v) for k, v in d.items()},
            }), flush=True)
            del sim
            release_device_memory()


if __name__ == "__main__":
    main()
