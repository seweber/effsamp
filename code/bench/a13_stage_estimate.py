"""A13 follow-up: stages per block if diagonal operations needed no register qubits (estimate).

A stage holds the amplitudes of R register qubits per thread; today every operation of a stage acts
on register qubits only, so diagonal gates (rz, cp, damping's no-error operator) count towards the
stage's width like dense ones. A diagonal operation can instead be applied in any stage, its factor
read from the bits of the amplitude index (the thread knows them), so only non-diagonal operations
would need register qubits. This script partitions each block's operations greedily into stages
both ways, respecting the order of operations on each qubit (diagonal operations commute with each
other), and prints the mean stages and the shared accesses 2 + 2 * stages per amplitude.

Usage: a13_stage_estimate.py [R ...] (local, CPU; the A13 workloads at n = 26)
"""

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import circuits  # noqa: E402
import noise  # noqa: E402
from dryrun import compile_like_simulator  # noqa: E402

from noisecirc import Simulator  # noqa: E402

WORKLOADS = [("ghz", 0.0019802), ("brickwork", 0.000280112), ("qft", 0.0002849), ("qaoa", 0.000512821), ("grid", 0.00017094)]


def stages(ops: list[tuple[tuple[int, ...], bool]], r: int, free_diagonals: bool) -> int:
    """Greedy stages: take ready operations that fit (diagonals free if ``free_diagonals``), fewest added qubits first."""
    n = len(ops)
    # Predecessors: the previous operation on a shared qubit, unless both are diagonal.
    preds = [set() for _ in range(n)]
    for i, (qi, di) in enumerate(ops):
        for j in range(i):
            qj, dj = ops[j]
            if set(qi) & set(qj) and not (di and dj):
                preds[i].add(j)
    done = set()
    count = 0
    while len(done) < n:
        count += 1
        reg: set[int] = set()
        progress = True
        while progress:
            progress = False
            ready = [i for i in range(n) if i not in done and preds[i] <= done]
            best = None
            for i in ready:
                q, d = ops[i]
                need = set() if (d and free_diagonals) else set(q) - reg
                if len(reg | need) > r:
                    continue
                if best is None or len(need) < best[0]:
                    best = (len(need), i, need)
            if best is not None:
                reg |= best[2]
                done.add(best[1])
                progress = True
    return count


def main() -> None:
    widths = [int(a) for a in sys.argv[1:]] or [3, 4]
    for name, p in WORKLOADS:
        qc = circuits.make(name, 26)
        for r in widths:
            compiled, _, _ = compile_like_simulator(qc, Simulator(maps=noise.maps("damping", p), stage_qubits=r))
            now, greedy, free = [], [], []
            for block in compiled.blocks:
                ops = []
                for op in block.dominant_block.operations:
                    m = np.asarray(op.kraus[0])
                    ops.append((tuple(int(q) for q in op.targets), bool(np.abs(m - np.diag(np.diag(m))).max() < 1e-12)))
                now.append(block.dominant_block.n_stages)
                greedy.append(stages(ops, r, False))
                free.append(stages(ops, r, True))
            print(json.dumps({"circuit": name, "R": r, "stages_noisecirc": float(np.mean(now)),
                              "stages_greedy": float(np.mean(greedy)), "stages_free_diagonals": float(np.mean(free)),
                              "shared_noisecirc": 2 + 2 * float(np.mean(now)), "shared_free": 2 + 2 * float(np.mean(free))}), flush=True)


if __name__ == "__main__":
    main()
