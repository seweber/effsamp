"""A10: how many error proposals tighter, checkpoint-dependent proposal bounds could avoid (estimate).

noisecirc proposes a damping jump on qubit q with the state-independent bound gamma (the operator norm
of the jump operator), and the jump is accepted with the excited population n_q of the state it acts
on. A bound may depend on the checkpoint state psi the segment starts from (and on the choices proposed
earlier in the block) as long as it bounds n_q for every state the jump can act on. Two valid rules:

- D (diagonal prefix): if every operation on q in the block up to and including the gate the channel
  follows is diagonal, n_q equals n_q(psi), up to the renormalization by no-jump operators on other
  qubits, a factor of at most 1/(1-gamma) each; bound gamma n_q(psi) / prod(1 - gamma).
- S (single-qubit prefix): if every operation on q in the block up to the channel acts on q alone,
  n_q <= lambda_max(rho_q(psi)) / prod(1 - gamma).
Otherwise the bound stays gamma. A jump proposed earlier in the block voids D and S for later
channels (conditioning can raise n_q to 1); that case has probability O(gamma) and is ignored here.

States at the checkpoints are the dry run's surrogate: each qubit's pure state followed from |0> until
an operation entangles it, maximally mixed (n = lambda_max = 1/2) after. ``free`` restricts D to the
qubits whose populations the checkpoint's last pass already provides in its chunk sums (all but the
8 lowest qubits of that block's tile order); ``all`` allows every qubit, and ``all+S`` adds rule S
(which needs the qubit's coherence, an extra reduction).

For every block the error-proposal mass sum_j sum_t gamma_t is compared with the tightened mass, and
the dry run's general-kernel passes of the block are scaled by that ratio. Prints JSON lines.
The oracle row assumes bounds equal to the populations themselves, the limit of any valid bound.
Usage: a10_estimate.py [circuits] (local, CPU; damping at M = 0.1 and 1, n = 28, 1000 shots)
"""

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import circuits  # noqa: E402
import dryrun  # noqa: E402
import noise  # noqa: E402
from noisecirc import Simulator  # noqa: E402


def is_diagonal(m: np.ndarray) -> bool:
    return bool(np.all(np.abs(m - np.diag(np.diag(m))) < 1e-12))


def checkpoint_states(compiled):
    """Per block: the surrogate's per-qubit (n, lambda_max) at the block's start."""
    pure = {q: np.array([1.0, 0.0], dtype=complex) for q in range(compiled.n)}
    out = []
    for block in compiled.blocks:
        out.append({q: ((abs(s[1]) ** 2, 1.0) if s is not None else (0.5, 0.5)) for q, s in pure.items()})
        for placed in block.operations:
            op, targets = placed.operation, placed.targets
            states = [pure[q] for q in targets]
            if any(s is None for s in states):
                for q in targets:
                    pure[q] = None
                continue
            psi = np.array([1.0 + 0j])
            for s in states:
                psi = np.kron(s, psi)
            out_state = op.stack[op.choice_of_code[op.dominant_code]] @ psi
            out_state /= np.linalg.norm(out_state)
            w = len(targets)
            tensor = out_state.reshape([2] * w)
            for j, q in enumerate(targets):
                moved = np.moveaxis(tensor, w - 1 - j, 0).reshape(2, -1)
                vals, vecs = np.linalg.eigh(moved @ moved.conj().T)
                pure[q] = vecs[:, -1] if vals[-1] > 1 - 1e-9 else None
    return out


def low_tile_qubits(block, pinned: int) -> set:
    """The 8 lowest qubits of a block's tile order (pinned qubits first, then its targets ascending)."""
    tile = sorted({q for placed in block.operations for q in placed.targets} | set(range(pinned)))
    return set(tile[:8])


def mass_ratios(compiled, gamma: float, mode: str) -> list[float]:
    states = checkpoint_states(compiled)
    pinned = compiled.config.pinned_qubits
    ratios = []
    previous_low = set()
    for b, block in enumerate(compiled.blocks):
        old = new = 0.0
        prefix = {}  # qubit -> (all diagonal so far, all single-qubit so far)
        channels_before = 0
        for placed in block.operations:
            op, targets = placed.operation, placed.targets
            diag = is_diagonal(op.stack[op.choice_of_code[op.dominant_code]])
            for q in targets:
                d, s = prefix.get(q, (True, True))
                prefix[q] = (d and diag, s and len(targets) == 1)
            factor = 1.0 / (1.0 - gamma) ** channels_before
            for q in targets:
                n_q, lam = states[b][q]
                d, s = prefix[q]
                bound = 1.0
                if d and (mode != "free" or q not in previous_low):
                    bound = min(bound, n_q * factor)
                if s and mode == "all+S":
                    bound = min(bound, lam * factor)
                old += gamma
                new += gamma * bound
            channels_before += len(targets)
        ratios.append(new / old if old else 1.0)
        previous_low = low_tile_qubits(block, pinned)
    return ratios


def main():
    names = sys.argv[1].split(",") if len(sys.argv) > 1 else ["ghz", "brickwork", "qft", "qaoa", "grid", "scramble"]
    for name in names:
        qc = circuits.make(name, 28)
        c = circuits.channels(qc)
        for load in (0.1, 1.0):
            p = 2 * load / c
            maps = noise.maps("damping", p)
            compiled, _, _ = dryrun.compile_like_simulator(qc, Simulator(maps=maps))
            runs = [dryrun.predict(qc, maps, 1000, seed=s, compiled=compiled) for s in (1, 2, 3)]
            dom = np.mean([r["dom_per_block"] for r in runs], axis=0)
            gen = np.mean([r["gen_per_block"] for r in runs], axis=0)
            row = {"circuit": name, "load": load, "p": p, "blocks": len(compiled.blocks),
                   "passes": float(dom.sum() + gen.sum()), "general": float(gen.sum())}
            # Oracle: bounds equal to the populations the jumps act on (the surrogate's acceptance of
            # each error choice), the most any valid bound could save: per block, the bound-weighted
            # mean acceptance of the error proposals.
            dryrun.prepare(compiled)
            oracle = []
            for block in compiled.blocks:
                table = dryrun._FACTORS[id(block)]
                mass = accepted = 0.0
                for i, placed in enumerate(block.operations):
                    op = placed.operation
                    bounds = op.upper_probability_bounds[0]
                    for k in range(bounds.size):
                        if k != op.dominant_code and bounds[k] > 0:
                            mass += bounds[k]
                            accepted += bounds[k] * table[i, k]
                oracle.append(accepted / mass if mass else 1.0)
            row["general_oracle"] = float((gen * np.array(oracle)).sum())
            row["passes_oracle"] = float(dom.sum() + (gen * np.array(oracle)).sum())
            for mode in ("free", "all", "all+S"):
                ratios = np.array(mass_ratios(compiled, p, mode))
                row[f"general_{mode}"] = float((gen * ratios).sum())
                row[f"passes_{mode}"] = float(dom.sum() + (gen * ratios).sum())
            print(json.dumps(row), flush=True)


if __name__ == "__main__":
    main()
