"""Predict NoiseCirc's work (block passes, proposals, distinct trajectories) without a GPU.

The dry run executes NoiseCirc's own sampler, `noisecirc.sampling.sample`, unchanged, on the
circuit's real blocks, segments and batch sizes, but with a surrogate for the trajectory states: a
state is replaced by its squared norm, and propagating it through a segment multiplies the norm by a
factor per gate. The factor of a gate's proposal-normalized Kraus operator ``M`` (``K / sqrt(b)``)
is its average over random states, ``tr(M^dagger M) / 2**w``: the surrogate assumes each gate's
targets look maximally mixed. It keeps the exact property of the real sampler that a proposal is
accepted with probability ``1 / Z`` on average for every trace-preserving channel, so the number of
proposals and rejections is exact on average; what it approximates is which paths are accepted, and
hence how many distinct trajectories survive (e.g. a damping jump is accepted with probability 1/2
instead of the actual excited population of its qubit).

Usage as a library: ``predict(circuit, maps, shots, seed=0, **simulator_options)``.
"""

from __future__ import annotations

import math
from collections import Counter
from dataclasses import dataclass, field

import numpy as np

import sys as _sys

import noisecirc.sampling.sample  # noqa: F401
from noisecirc import Simulator
from noisecirc.circuit import CompiledCircuit

sample_module = _sys.modules["noisecirc.sampling.sample"]

# H100 PCIe: 80 GB, of which NoiseCirc reserves 90% of the free memory for rows.
DEVICE_BYTES = 0.9 * 79.0e9


@dataclass
class _Counters:
    reads: int = 0
    writes: int = 0


@dataclass
class FakeEngine:
    """What `sample` reads of an engine: its counters."""

    counters: _Counters = field(default_factory=_Counters)


_FACTORS: dict[int, np.ndarray] = {}


def _factors(block) -> np.ndarray:
    """(n_operations, max_codes) surrogate acceptance factor of each operation's codes; nan for padding."""
    key = id(block)
    table = _FACTORS.get(key)
    if table is None:
        ops = [placed.operation for placed in block.operations]
        width = max(op.choice_of_code.size for op in ops)
        table = np.full((len(ops), width), np.nan)
        for i, op in enumerate(ops):
            dim = op.stack.shape[-1]
            per_choice = np.einsum("kij,kij->k", op.stack.conj(), op.stack).real / dim
            valid = op.choice_of_code >= 0
            table[i, : op.choice_of_code.size][valid] = per_choice[op.choice_of_code[valid]]
        _FACTORS[key] = table
    return table


class SurrogateStates:
    """Stands in for `noisecirc.states.TrajectoryStates`: a row is its squared norm and its branches."""

    engine: FakeEngine | None = None

    def __init__(self, norms: np.ndarray, branches: np.ndarray) -> None:
        self.norms = norms
        self.branches = branches

    @classmethod
    def root(cls, engine, n: int) -> SurrogateStates:
        return cls(np.ones(1), np.zeros((1, n), dtype=np.int64))

    @property
    def rows(self) -> int:
        return self.norms.size

    def select(self, indices) -> SurrogateStates:
        return SurrogateStates(self.norms[indices], self.branches[indices])

    @staticmethod
    def concatenate(parts) -> SurrogateStates:
        return SurrogateStates(np.concatenate([p.norms for p in parts]), np.concatenate([p.branches for p in parts]))

    @staticmethod
    def compile(engine, blocks):
        return []

    def propagate(self, blocks, codes, end_branches, scales=None) -> None:
        start_norms = self.norms * (scales**2 if scales is not None else 1.0)
        log = np.zeros(self.rows)
        row = 0
        for block in blocks:
            table = _factors(block)
            k = len(block.operations)
            block_codes = codes[row : row + k]
            log += np.log(table[np.arange(k)[:, None], block_codes]).sum(axis=0)
            row += k
        self.norms = start_norms * np.exp(log)
        self.branches = np.array(end_branches, dtype=np.int64)
        engine = SurrogateStates.engine
        engine.counters.writes += self.rows * len(blocks)
        engine.counters.reads += self.rows * len(blocks)

    def squared_norms(self) -> np.ndarray:
        return self.norms.copy()

    def measure(self, shots, rng):
        shots = np.asarray(shots)
        n = self.branches.shape[1]
        total = int(shots.sum())
        return np.zeros((1 if total else 0, n), dtype=np.int64), np.array([total] if total else [], dtype=np.int64)


def segmentation(compiled: CompiledCircuit, simulator: Simulator) -> tuple[int, int]:
    """`Simulator._segmentation` with the H100's free rows instead of a device query."""
    n_blocks = len(compiled.blocks)
    free_rows = int(DEVICE_BYTES // (2**compiled.n * 8 + 2**compiled.n // 64 * 8))
    blocks_per_segment = simulator.blocks_per_segment
    if blocks_per_segment is not None:
        blocks_per_segment = max(1, int(min(blocks_per_segment, n_blocks)))
    n_segments = -(-n_blocks // (blocks_per_segment or 1))
    max_batch_size = max(1, free_rows // (n_segments + 2))
    if simulator.max_batch_size is not None:
        max_batch_size = min(simulator.max_batch_size, max_batch_size)
    if blocks_per_segment is None:
        max_segments = free_rows // max_batch_size - 2
        blocks_per_segment = n_blocks if max_segments < 1 else max(1, -(-n_blocks // max_segments))
    return blocks_per_segment, max_batch_size


def compile_like_simulator(circuit, simulator: Simulator) -> tuple[CompiledCircuit, int, int]:
    """`Simulator._compiled` without a GPU."""
    from functools import partial

    compile_with = partial(
        CompiledCircuit,
        circuit,
        maps=simulator.maps,
        max_fused_qudits=simulator.max_fused_qudits,
        dtype=simulator.dtype,
        optimize_kraus=simulator.optimize_kraus,
        max_operations=simulator.max_operations,
        pinned_bytes=simulator.pinned_bytes,
    )
    max_oversampling = simulator.max_oversampling if (simulator.blocks_per_segment or 1) < 2 else math.inf
    compiled = compile_with(max_oversampling=max_oversampling)
    bps, batch = segmentation(compiled, simulator)
    if bps > 1 and math.isfinite(max_oversampling):
        compiled = compile_with(max_oversampling=math.inf)
        bps, batch = segmentation(compiled, simulator)
    return compiled, bps, batch


def predict(circuit, maps, shots: int, seed: int = 0, compiled=None, **options) -> dict[str, float]:
    """Run NoiseCirc's sampler with surrogate states; return its diagnostics plus the block count."""
    simulator = Simulator(maps=maps, **options)
    if compiled is None:
        compiled, bps, batch = compile_like_simulator(circuit, simulator)
    else:
        bps, batch = segmentation(compiled, simulator)
    original = sample_module.TrajectoryStates
    sample_module.TrajectoryStates = SurrogateStates
    SurrogateStates.engine = FakeEngine()
    try:
        _, diagnostics = sample_module.sample(
            compiled, shots, simulator.sampling_mode, batch, bps, seed, SurrogateStates.engine
        )
    finally:
        sample_module.TrajectoryStates = original
    return {**diagnostics, "blocks": len(compiled.blocks)}


if __name__ == "__main__":
    import sys
    import time

    sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
    import circuits
    import noise

    for name in ("ghz", "brickwork", "qft"):
        for p in (1e-4, 1e-3, 1e-2):
            qc = circuits.make(name, 24)
            start = time.perf_counter()
            d = predict(qc, noise.maps("damping", p), 1000)
            print(name, p, {k: d[k] for k in ("blocks", "block_passes", "proposals", "unique_simulations", "batches")},
                  f"{time.perf_counter() - start:.2f}s")
    _ = Counter
