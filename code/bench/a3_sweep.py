"""A3: how NoiseCirc's parameters set the number of blocks and of block passes (dry run, no GPU).

Sweeps, each changing one parameter from NoiseCirc's defaults (n = 24, damping, 1000 shots,
seed 0, the H100's memory for the batch sizes):

- fusion: blocks of each circuit against max_fused_qudits and max_operations (ideal and p = 1e-3);
- noise: block passes against the damping strength p, for shots 100, 1000, 10000;
- segment: block passes against blocks_per_segment (1, 2, 4, 8, inf) at three strengths;
- oversampling: block passes against max_oversampling (1.1 .. inf) at three strengths.

Each point is averaged over 3 seeds. Prints JSON lines.
Usage: python a3_sweep.py SWEEP [circuits]
"""

import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import circuits  # noqa: E402
import dryrun  # noqa: E402
import noise  # noqa: E402
from noisecirc import Simulator  # noqa: E402

CIRCUITS = ["ghz", "brickwork", "qft", "random", "grid", "qaoa"]
KEYS = ("block_passes", "proposals", "unique_simulations", "batches", "blocks", "expected_oversampling",
        "checkpoints", "cache_hits")


def mean_predict(qc, maps, shots, seeds=3, **options):
    runs = [dryrun.predict(qc, maps, shots, seed=s, **options) for s in range(seeds)]
    return {k: float(np.mean([r[k] for r in runs])) for k in KEYS} | {
        "block_passes_std": float(np.std([r["block_passes"] for r in runs]))}


def emit(**row):
    print(json.dumps(row), flush=True)


def main():
    sweep = sys.argv[1]
    names = sys.argv[2].split(",") if len(sys.argv) > 2 else CIRCUITS
    n = 24
    for name in names:
        qc = circuits.make(name, n)
        meta = {"circuit": name, "n": n, "gates": len(qc.data), "channels": circuits.channels(qc)}
        if sweep == "fusion":
            for p in (0.0, 1e-3):
                maps = noise.maps("damping" if p else None, p)
                for k in range(0, 10):
                    c, _, _ = dryrun.compile_like_simulator(qc, Simulator(maps=maps, max_fused_qudits=k))
                    emit(sweep=sweep, **meta, p=p, max_fused_qudits=k, max_operations=128, blocks=len(c.blocks))
                for m in (8, 16, 24, 32, 48, 64, 96, 128, 256):
                    c, _, _ = dryrun.compile_like_simulator(qc, Simulator(maps=maps, max_operations=m))
                    emit(sweep=sweep, **meta, p=p, max_fused_qudits=9, max_operations=m, blocks=len(c.blocks))
        elif sweep == "noise":
            for p in (1e-5, 3e-5, 1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2):
                for shots in (100, 1000, 10000):
                    emit(sweep=sweep, **meta, p=p, shots=shots, **mean_predict(qc, noise.maps("damping", p), shots))
        elif sweep == "segment":
            for p in (1e-4, 1e-3, 1e-2):
                for bps in (1, 2, 4, 8, math.inf):
                    sim = Simulator(maps=noise.maps("damping", p), blocks_per_segment=bps)
                    c, b, _ = dryrun.compile_like_simulator(qc, sim)
                    logs = [blk.log_oversampling_ceiling for blk in c.blocks]
                    worst = max(sum(logs[i : i + b]) for i in range(0, len(logs), b))
                    if worst > 6.0:  # more than e^6 = 400 proposals per shot: hopeless, and memory-bound here
                        emit(sweep=sweep, **meta, p=p, shots=1000, blocks_per_segment=str(bps), skipped=True,
                             max_segment_log_ceiling=worst)
                        continue
                    d = mean_predict(qc, noise.maps("damping", p), 1000, blocks_per_segment=bps)
                    emit(sweep=sweep, **meta, p=p, shots=1000, blocks_per_segment=str(bps), **d)
        elif sweep == "oversampling":
            for p in (1e-4, 1e-3, 1e-2):
                for mo in (1.1, 1.5, 2.0, math.e, 5.0, 10.0, math.inf):
                    d = mean_predict(qc, noise.maps("damping", p), 1000, max_oversampling=mo)
                    emit(sweep=sweep, **meta, p=p, shots=1000, max_oversampling=str(mo), **d)
        else:
            raise ValueError(sweep)


if __name__ == "__main__":
    main()
