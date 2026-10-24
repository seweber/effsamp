"""A14: lower bound on FP instructions per amplitude of each block's dominant kernel, against the counts achieved.

Bound: a non-diagonal one-qubit operation mixes two amplitudes; each output component needs at least
one FMA, so at least 2 instructions per amplitude, unless it is a permutation up to signs (0). Runs of
consecutive one-qubit operations on the same qubit with at most one-qubit diagonals in between multiply
into one, and diagonal operations can in principle be deferred into the phases of later operations (0); multi-qubit
non-diagonal operations count 2 per amplitude as well (a loose bound). Plus 4 for the scaling at load
and the norm at store. Prints per circuit the mean bound and the mean counts of the default kernel, of
stage fusion, and of fusion plus rotation form (stage_qubits 3 and 4).
Usage: a14_bound.py (local, CPU; n = 26, damping M = 0.1)
"""
import dataclasses
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import circuits  # noqa: E402
import noise  # noqa: E402
from dryrun import compile_like_simulator  # noqa: E402
from kernel_ops import block_work  # noqa: E402

from noisecirc import Simulator  # noqa: E402


def bound(block) -> float:
    ops = block.dominant_block.operations
    last = {}  # qubit -> index in `kept` of the last non-diagonal op touching only it, if nothing else since
    count = 0
    for op in ops:
        m = np.asarray(op.kraus[0])
        offdiag = np.abs(m - np.diag(np.diag(m))).max() > 1e-12
        targets = tuple(int(q) for q in op.targets)
        if not offdiag:
            if len(targets) > 1:
                for q in targets:
                    last[q] = False  # a one-qubit gate cannot merge across a multi-qubit diagonal
            continue  # diagonal: deferrable
        if len(targets) == 1 and last.get(targets[0]):
            continue  # merges into the previous one-qubit op on this qubit
        perm = np.all(np.isclose(np.abs(m[np.abs(m) > 1e-12]), 1)) and np.all((np.abs(m) > 1e-12).sum(axis=1) == 1)
        count += 0 if perm else 1
        for q in targets:
            last[q] = len(targets) == 1
    return 2.0 * count + 4


for name, p in [("ghz", 0.0019802), ("brickwork", 0.000280112), ("qft", 0.0002849), ("qaoa", 0.000512821), ("grid", 0.00017094), ("random", 1e-4)]:
    qc = circuits.make(name, 26)
    row = [name]
    for sq in (3,):
        compiled, _, _ = compile_like_simulator(qc, Simulator(maps=noise.maps("damping", p), stage_qubits=sq))
        cfg = compiled.config
        b = np.mean([bound(blk) for blk in compiled.blocks])
        counts = [np.mean([block_work(blk.dominant_block, dataclasses.replace(cfg, **kw))["fp_ops"] for blk in compiled.blocks])
                  for kw in ({}, {"stage_fusion": True}, {"stage_fusion": True, "rotation_form": True})]
        row.append(f"sq{sq}: bound {b:5.1f} default {counts[0]:5.1f} fused {counts[1]:5.1f} rot {counts[2]:5.1f}")
    print(" | ".join(row), flush=True)
