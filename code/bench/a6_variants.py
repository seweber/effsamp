"""A6: noisecirc with parts of its algorithm switched off, to separate algorithmic from implementation gains.

Variants (one noisecirc implementation throughout):

- ``default``: noisecirc's defaults.
- ``k2``: fusion limited to blocks of 2 qubits with no pinned qubits (``max_fused_qudits=2``,
  ``pinned_bytes=0``), the width Aer fuses noisy gates to; trajectories still shared.
- ``pershot``: every shot its own run of one shot, so that no trajectory or prefix is shared between
  shots (rejection sampling per shot, with checkpoints only within the shot's own refills).
- ``pershot_k2``: both, the closest noisecirc gets to per-shot trajectory simulation at Aer's fusion.

Per-shot variants run ``--pershot-shots`` single-shot runs (seeds 1, 2, ...) and report their total,
scaled to the requested shots. Prints JSON lines with time and summed block passes.
"""

import argparse
import json
import sys
import time

sys.path.insert(0, "/work/bench")
import circuits  # noqa: E402
import noise  # noqa: E402

from noisecirc import Simulator, release_device_memory  # noqa: E402

OPTIONS = {"default": {}, "k2": {"max_fused_qudits": 2, "pinned_bytes": 0},
           "pershot": {}, "pershot_k2": {"max_fused_qudits": 2, "pinned_bytes": 0}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--variant", required=True)
    parser.add_argument("--circuit", default="brickwork")
    parser.add_argument("--qubits", type=int, default=24)
    parser.add_argument("--noise", default="damping")
    parser.add_argument("--ps", default="0.001")
    parser.add_argument("--shots", type=int, default=1000)
    parser.add_argument("--pershot-shots", type=int, default=100)
    parser.add_argument("--budget", type=float, default=450.0)
    args = parser.parse_args()
    qc = circuits.make(args.circuit, args.qubits)
    begin = time.perf_counter()
    for p in [float(x) for x in args.ps.split(",")]:
        if time.perf_counter() - begin > args.budget:
            print(json.dumps({"kind": "skipped", "variant": args.variant, "circuit": args.circuit, "p": p}))
            continue
        sim = Simulator(maps=noise.maps(args.noise, p), **OPTIONS[args.variant])
        sim.run(qc, shots=1 if args.variant.startswith("pershot") else args.shots, seed=0)  # compiles
        compiled, _, _ = sim._compiled(qc)
        start = time.perf_counter()
        passes = 0.0
        if args.variant.startswith("pershot"):
            for seed in range(1, args.pershot_shots + 1):
                passes += sim.run(qc, shots=1, seed=seed).diagnostics["block_passes"]
            scale = args.shots / args.pershot_shots
        else:
            passes = sim.run(qc, shots=args.shots, seed=1).diagnostics["block_passes"]
            scale = 1.0
        elapsed = (time.perf_counter() - start) * scale
        print(json.dumps({"kind": "variant", "variant": args.variant, "circuit": args.circuit, "n": args.qubits,
                          "noise": args.noise, "p": p, "shots": args.shots, "time": elapsed,
                          "block_passes": passes * scale, "blocks": len(compiled.blocks),
                          "gates": len(qc.data), "channels": circuits.channels(qc)}), flush=True)
        del sim
        release_device_memory()


if __name__ == "__main__":
    main()
