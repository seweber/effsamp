"""A2/A5: time whole NoiseCirc runs and record the work they did (block passes and other diagnostics).

For each point, a first run compiles the kernels (its time is reported as ``t_first``) and gives the
diagnostics; then ``--reps`` runs with seeds 1, 2, ... are timed and their diagnostics kept, as
the work varies with the seed. The bandwidth floor ``t_bw`` (a CuPy in-place scaling of one
complex64 state of n qubits: one read and one write) is measured once per register size.

Prints one JSON line per timed run.
"""

import argparse
import json
import sys
import time

import cupy as cp
import numpy as np

sys.path.insert(0, "/work/bench")
import circuits  # noqa: E402
import noise  # noqa: E402

from noisecirc import Simulator, release_device_memory  # noqa: E402


def bandwidth_time(n: int, reps: int = 7) -> float:
    """Seconds of an in-place scaling of a 2**n complex64 vector: one read and one write of the state."""
    a = cp.ones(2**n, dtype=cp.complex64)
    s = cp.float32(1.0)
    cp.multiply(a, s, out=a)
    cp.cuda.runtime.deviceSynchronize()
    times = []
    for _ in range(reps):
        start = time.perf_counter()
        for _ in range(5):
            cp.multiply(a, s, out=a)
        cp.cuda.runtime.deviceSynchronize()
        times.append((time.perf_counter() - start) / 5)
    del a
    cp.get_default_memory_pool().free_all_blocks()
    return float(np.median(times))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--circuits", default="brickwork")
    parser.add_argument("--qubits", default="24")
    parser.add_argument("--noise", default="damping")
    parser.add_argument("--ps", default="0.001")
    parser.add_argument("--shots", default="1000")
    parser.add_argument("--reps", type=int, default=3)
    parser.add_argument("--budget", type=float, default=500.0, help="seconds after which no new point starts")
    parser.add_argument("--option", action="append", default=[], help="Simulator option key=value")
    parser.add_argument("--tunable", action="append", default=[], help="noisecirc.tunables NAME=VALUE (int, float, True/False)")
    parser.add_argument("--config", action="append", default=[], help="svpass Config field=value, see configpatch.py")
    parser.add_argument("--kraus-set", default="canonical", choices=["canonical", "optimum"],
                        help="optimum: the optimal Kraus sets of task A12 (a12_dryrun.optimal_maps)")
    args = parser.parse_args()

    options = {}
    for item in args.option:
        key, value = item.split("=")
        options[key] = float(value) if "." in value or value in ("inf",) else int(value)
    from noisecirc import tunables

    import configpatch

    extra_options, config = configpatch.parse(args.config)
    options.update(extra_options)  # stage_qubits is a Simulator option, see configpatch.parse
    configpatch.apply(config)

    for item in args.tunable:
        name, value = item.split("=")
        setattr(tunables, name, {"True": True, "False": False}.get(value, value if not value[0].isdigit() else float(value) if "." in value else int(value)))
    begin = time.perf_counter()
    for n in [int(q) for q in args.qubits.split(",")]:
        t_bw = bandwidth_time(n)
        for name in args.circuits.split(","):
            qc = circuits.make(name, n)
            for p in [float(x) for x in args.ps.split(",")]:
                maps = noise.maps(None if args.noise == "none" or p == 0 else args.noise, p)
                if args.kraus_set == "optimum":
                    import a12_dryrun
                    import noisecirc.block.operation as operation_module

                    operation_module.sta_sectors = a12_dryrun.sta_as_given
                    maps = a12_dryrun.optimal_maps(args.noise, p)
                    options["optimize_kraus"] = True
                for shots in [int(s) for s in args.shots.split(",")]:
                    if time.perf_counter() - begin > args.budget:
                        print(json.dumps({"kind": "skipped", "circuit": name, "n": n, "p": p, "shots": shots}))
                        continue
                    sim = Simulator(maps=maps, **options)
                    start = time.perf_counter()
                    first = sim.run(qc, shots=shots, seed=0)
                    t_first = time.perf_counter() - start
                    compiled, bps, batch = sim._compiled(qc)
                    reps = args.reps if t_first < 60 else 1
                    for seed in range(1, reps + 1):
                        start = time.perf_counter()
                        result = sim.run(qc, shots=shots, seed=seed)
                        elapsed = time.perf_counter() - start
                        d = result.diagnostics
                        print(json.dumps({
                            "kind": "run", "circuit": name, "n": n, "noise": args.noise, "p": p, "shots": shots,
                            "seed": seed, "time": elapsed, "t_first": t_first, "t_bw": t_bw,
                            "gates": len(qc.data), "channels": circuits.channels(qc),
                            "blocks": len(compiled.blocks), "blocks_per_segment": bps, "max_batch": batch,
                            "options": {**options, **config}, "tunables": args.tunable, "kraus_set": args.kraus_set,
                            "tuned": [list(v) for v in getattr(sim, "_tuned", {}).values()], **{k: float(v) for k, v in d.items()},
                        }), flush=True)
                    del sim
                    release_device_memory()


if __name__ == "__main__":
    main()
