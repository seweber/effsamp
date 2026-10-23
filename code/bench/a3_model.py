"""A3: closed-form estimate of NoiseCirc's block passes (exact mode, one block per segment).

For a circuit compiled into blocks ``b = 1..B`` with oversampling ceilings ``Z_b`` (product of the
blocks' gates' factors), ``N`` shots and an expected number ``mu_b`` of accepted errors per shot in
block ``b``:

- every shot proposes, on average over its refills, one no-error path and ``Z_b - 1`` paths with an
  error per block (the no-error path of a trace-preserving channel has bound one, so it is proposed
  with probability ``1 / Z_b`` per attempt, and a shot makes ``Z_b`` attempts on average);
- the no-error paths of all shots at one checkpoint coincide and are propagated once per checkpoint;
  the error paths are distinct;
- the checkpoints entering block ``b`` are the distinct accepted prefixes, ``1 + N (1 - exp(-M))``
  with ``M = sum of mu`` over the earlier blocks (a shot carries a distinct prefix once it has had an error).

So the dominant-kernel passes are ``P_dom = sum_b [1 + N (1 - exp(-M_{b-1}))]`` and the
general-kernel passes ``P_gen = N sum_b (Z_b - 1)``. For damping ``mu`` per channel is ``p <n1>``,
here with ``<n1> = 1/2`` (maximally mixed), so ``mu_b = (Z_b - 1)/2`` for small ``p``.
"""

import math

import numpy as np


def estimate(log_ceilings, shots: int, accepted_fraction: float = 0.5, error_codes=None) -> dict[str, float]:
    """Return the estimated dominant and general block passes from the blocks' log ceilings.

    With ``error_codes`` (per block, the number of distinct single-error paths: the error choices
    summed over its gates), the error proposals of block ``b`` are deduplicated as balls into bins:
    ``N (Z_b - 1)`` proposals spread over ``D_b K_b`` distinct paths from the ``D_b`` checkpoints.
    """
    z = np.exp(np.asarray(log_ceilings, dtype=float))
    errors = (z - 1) * accepted_fraction  # expected accepted errors per shot per block
    before = np.concatenate([[0.0], np.cumsum(errors)[:-1]])
    checkpoints = 1 + shots * (1 - np.exp(-before))
    p_dom = float(np.sum(checkpoints))
    proposals = shots * (z - 1)
    if error_codes is None:
        p_gen = float(np.sum(proposals))
    else:
        bins = checkpoints * np.asarray(error_codes, dtype=float)
        p_gen = float(np.sum(bins * -np.expm1(-proposals / np.maximum(bins, 1e-300))))
    return {"p_dom": p_dom, "p_gen": p_gen, "passes": p_dom + p_gen, "M": float(errors.sum()),
            "L": float(np.sum(np.log(z)))}


def error_codes(block) -> int:
    """The distinct single-error paths of a block: each gate's declared choices besides its dominant one."""
    return sum(int(np.count_nonzero(placed.operation.output_sectors[0] >= 0)) - 1 for placed in block.operations)


def uniform(blocks: int, total_errors: float, total_log_ceiling: float, shots: int) -> float:
    """The same for B equal blocks: B (1 + N f(M)) + N (Z - 1) B, f(M) = 1 - (1 - e^-M)/M."""
    m = total_errors
    f = 1 - (1 - math.exp(-m)) / m if m > 0 else 0.0
    z_minus_1 = math.exp(total_log_ceiling / blocks) - 1
    return blocks * (1 + shots * f) + shots * blocks * z_minus_1
