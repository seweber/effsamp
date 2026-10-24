"""A15: estimated block passes of first-jump sampling against noisecirc's proposals, by noise load.

First-jump sampling (A15 brainstorm): the dominant pass of a checkpoint also reduces, per noisy
channel of the block, the probability of a first jump there, so the shots of the checkpoint are split
exactly over {no jump, first jump at (channel, operator)}; only accepted jumps are propagated, and the
block ceiling max_oversampling is no longer needed. Model (Eq. (2) of the block-pass cost model with
equal blocks, amplitude damping, M = pC/2 accepted jumps per shot):

- noisecirc: P = sum_b [1 + N(1 - exp(-M b/B))] + N sum_b (Z_b - 1), B from compiling with the ceiling e;
- first jump: P = sum_b [1 + N(1 - exp(-M b/B'))] + N M, B' from compiling without the ceiling.

Block counts come from noisecirc's own fusion at each strength (no GPU). Prints JSON lines.
Usage: a15_firstjump.py (local, CPU; n = 28, 1000 shots)
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

N = 1000


def dominant(blocks: int, load: float) -> float:
    b = np.arange(blocks)
    return float(np.sum(1 + N * (1 - np.exp(-load * b / blocks))))


for name in ["ghz", "brickwork", "qft", "qaoa", "grid"]:
    qc = circuits.make(name, 28)
    c = circuits.channels(qc)
    for load in (0.1, 1.0, 3.0, 10.0):
        p = 2 * load / c
        maps = noise.maps("damping", p)
        with_ceiling, _, _ = dryrun.compile_like_simulator(qc, Simulator(maps=maps))
        without, _, _ = dryrun.compile_like_simulator(qc, Simulator(maps=maps, max_oversampling=math.inf))
        z = [math.exp(sum(op.operation.log_oversampling_ceiling for op in blk.operations)) for blk in with_ceiling.blocks]
        b1, b2 = len(with_ceiling.blocks), len(without.blocks)
        p_now = dominant(b1, load) + N * sum(zb - 1 for zb in z)
        p_fj_same = dominant(b1, load) + N * load
        p_fj = dominant(b2, load) + N * load
        print(json.dumps({"circuit": name, "load": load, "p": p, "blocks_ceiling": b1, "blocks_free": b2,
                          "passes_now": p_now, "passes_firstjump_same_blocks": p_fj_same, "passes_firstjump": p_fj,
                          "gain_same_blocks": p_now / p_fj_same, "gain": p_now / p_fj}), flush=True)
