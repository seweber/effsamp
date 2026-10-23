"""A2: time one pass of each of a circuit's blocks against the time of moving the state vector.

For every circuit and register size, the circuit is compiled as `noisecirc.Simulator` compiles it
(its defaults, the given noise), and every distinct block's kernels are timed on one state of ``n``
qubits: the dominant kernel (no error in the block) and, for blocks with choices, the general kernel
(all operations on their dominant choice, so that the work is the same but the code switches).
The floor is a pass of a block holding a single ``rz`` on qubit 0, NoiseCirc's cheapest pass, and
a CuPy in-place scaling of the same bytes, the raw bandwidth.

Prints one JSON line per block, then one summary line per circuit.
"""

import argparse
import json
import sys
import time

import cupy as cp
import numpy as np
from qiskit import QuantumCircuit

sys.path.insert(0, "/work/bench")
import circuits  # noqa: E402
import noise  # noqa: E402

from noisecirc import Simulator, release_device_memory  # noqa: E402


def timed(apply, reps: int, sync) -> float:
    """Median of ``reps`` timings of ``apply`` launched 5 times back to back (seconds per launch)."""
    apply()
    sync()
    times = []
    for _ in range(reps):
        start = time.perf_counter()
        for _ in range(5):
            apply()
        sync()
        times.append((time.perf_counter() - start) / 5)
    return float(np.median(times))


def bandwidth_time(n: int, itemsize: int = 8, reps: int = 7) -> float:
    """Seconds of an in-place scaling of a 2**n complex64 vector with CuPy: one read and one write."""
    a = cp.ones(2**n, dtype=cp.complex64)
    s = cp.float32(1.0)

    def apply():
        cp.multiply(a, s, out=a)

    t = timed(apply, reps, cp.cuda.runtime.deviceSynchronize)
    del a
    cp.get_default_memory_pool().free_all_blocks()
    return t


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--circuits", default="ghz,brickwork,qft,random,grid,qaoa")
    parser.add_argument("--qubits", default="24")
    parser.add_argument("--noise", default="damping")
    parser.add_argument("--p", type=float, default=1e-3)
    parser.add_argument("--reps", type=int, default=5)
    parser.add_argument("--max-operations", type=int, default=None)
    parser.add_argument("--max-fused", type=int, default=None)
    args = parser.parse_args()

    maps = noise.maps(None if args.noise == "none" else args.noise, args.p)
    options = {}
    if args.max_operations is not None:
        options["max_operations"] = args.max_operations
    if args.max_fused is not None:
        options["max_fused_qudits"] = args.max_fused
    sim = Simulator(maps=maps, **options)
    for n in [int(q) for q in args.qubits.split(",")]:
        t_cupy = bandwidth_time(n)
        floor_circuit = QuantumCircuit(n)
        floor_circuit.rz(0.1, 0)
        floor, _, _ = Simulator(maps=noise.maps(None))._compiled(floor_circuit)
        engine = sim._engine(floor.config)
        state = engine.canonical_state(n, np.zeros(1, dtype=np.int64))
        floor_kernel = engine.compile(floor.blocks[0].engine_block).result()
        floor_kernel.apply(state)  # generates |0...0> into a row of its own
        t_floor = timed(lambda: floor_kernel.apply(state), args.reps, engine.synchronize)
        for name in args.circuits.split(","):
            qc = circuits.make(name, n)
            start = time.perf_counter()
            compiled, _, _ = sim._compiled(qc)
            futures = [f for block in compiled.blocks for f in block.kernels(engine)]
            for f in futures:
                f.result()
            t_compile = time.perf_counter() - start
            seen = {}
            total_dom = 0.0
            total_gen = 0.0
            for index, block in enumerate(compiled.blocks):
                if block not in seen:
                    dom = engine.compile(block.dominant_block).result()
                    t_dom = timed(lambda: dom.apply(state), args.reps, engine.synchronize)
                    t_gen = None
                    if block.has_choices:
                        gen = engine.compile(block.engine_block).result()
                        codes = block.dominant_codes[:, None]
                        choices = engine.upload(block.choices(codes))
                        t_gen = timed(lambda: gen.apply(state, choices), args.reps, engine.synchronize)
                    seen[block] = (t_dom, t_gen)
                    stages = len(block.stage_offsets) - 1
                    tile = len({q for op in block.operations for q in op.targets} | set(range(compiled.config.pinned_qubits)))
                    print(json.dumps({
                        "kind": "block", "circuit": name, "n": n, "noise": args.noise, "p": args.p,
                        "block": index, "ops": len(block.operations),
                        "two_qubit": sum(len(op.targets) == 2 for op in block.operations),
                        "stages": stages, "tile": tile, "t_dom": t_dom, "t_gen": t_gen,
                        "log_ceiling": block.log_oversampling_ceiling,
                    }), flush=True)
                t_dom, t_gen = seen[block]
                total_dom += t_dom
                total_gen += t_gen if t_gen is not None else t_dom
            print(json.dumps({
                "kind": "circuit", "circuit": name, "n": n, "noise": args.noise, "p": args.p,
                "gates": len(qc.data), "channels": circuits.channels(qc), "blocks": len(compiled.blocks),
                "distinct_blocks": len(seen), "t_floor": t_floor, "t_cupy": t_cupy,
                "sum_dom": total_dom, "sum_gen": total_gen, "t_compile": t_compile, "options": options,
            }), flush=True)
        del state, floor_kernel
        sim._engines.clear()
        release_device_memory()


if __name__ == "__main__":
    main()
