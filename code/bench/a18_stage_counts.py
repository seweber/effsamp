"""A18: stages per block pass of the A13 workloads (CPU), for estimating register-chained tensor-core passes.

For each workload at n qubits and each stage width R, compiles the circuit as noisecirc does
(`dryrun.compile_like_simulator`, stage contraction and additive addresses on) and prints, over the
dominant kernels of the blocks (each block once, as in a16_time.py's trajectory weighting), the mean
number of stages per pass, the CUDA-core floating-point instructions per amplitude of a pass and of
a stage (the `codegen._contraction` costs of the stages), and the tile qubits.

Usage: a18_stage_counts.py [--qubits 26] [--dtype complex32] [--workloads circuit:p,...] [--set key=value ...]
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import circuits  # noqa: E402
import configpatch  # noqa: E402
import noise  # noqa: E402
from dryrun import compile_like_simulator  # noqa: E402

from noisecirc import Simulator  # noqa: E402
from svpass.cuda import codegen  # noqa: E402

WORKLOADS = [("ghz", 0.0019802), ("brickwork", 0.000280112), ("qft", 0.0002849), ("qaoa", 0.000512821), ("grid", 0.00017094)]


recorded: list[float] = []
_contraction = codegen._contraction


def _recording(items, r, eps, *rest):
    found = _contraction(items, r, eps, *rest)
    if found is not None:
        recorded.append(found[1])
    return found


codegen._contraction = _recording


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--qubits", type=int, default=26)
    parser.add_argument("--dtype", default="complex32")
    parser.add_argument("--workloads", default=",".join(f"{name}:{p}" for name, p in WORKLOADS))
    parser.add_argument("--set", action="append", default=[])
    args = parser.parse_args()
    _, config = configpatch.parse(args.set)
    configpatch.apply({"stage_contraction": 1, "additive_addresses": 1, **config})
    for workload in args.workloads.split(","):
        name, p = workload.split(":")
        p = float(p)
        for r in (3, 4):
            sim = Simulator(maps=noise.maps("damping", p), dtype=args.dtype, stage_qubits=r)
            compiled, _, _ = compile_like_simulator(circuits.make(name, args.qubits), sim)
            stages, costs, tiles = [], [], []
            for block in compiled.blocks:
                dominant = block.dominant_block
                recorded.clear()
                found = codegen._stages(dominant, compiled.config)
                stages.append(len(found))
                costs.append(sum(recorded))
                tiles.append(len(dominant.tile(compiled.config)))
            print(json.dumps({"circuit": name, "R": r, "config": config, "blocks": len(stages), "mean_stages": float(np.mean(stages)),
                              "max_stages": int(np.max(stages)), "mean_fp_per_amp": float(np.mean(costs)),
                              "fp_per_amp_per_stage": float(np.sum(costs) / np.sum(stages)),
                              "mean_tile_qubits": float(np.mean(tiles)), "max_tile_qubits": int(np.max(tiles))}), flush=True)


if __name__ == "__main__":
    main()
