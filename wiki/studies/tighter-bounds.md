---
title: Checkpoint-dependent proposal bounds
summary: Valid tighter proposal bounds from the checkpoint state, and how many rejected proposals they can avoid (A10)
type: study
tasks: [A10]
status: partially verified
updated: 2026-10-24
---
# Checkpoint-dependent proposal bounds

## Question

At strong noise, noisecirc's work is dominated by proposals with an error, about $2MN$ passes for amplitude damping, of which about half are rejected (see [Block passes against noisecirc's parameters](pass-count.md)). The proposal bounds are the operator norms of the Kraus operators, which hold for every state. How many of the rejected proposals could bounds that use the state at a checkpoint avoid, without breaking the exactness of the sampling (PLAN.md task A10)?

## Approach

The approach has three steps: derive which state-dependent bounds are valid, find which of them the GPU passes already provide, and estimate their effect with the dry run of [Block passes against noisecirc's parameters](pass-count.md) before any implementation.

### Which bounds keep the sampling exact

The proposals of a segment are drawn after its checkpoint, an accepted state $\psi$, has been computed. A bound may therefore depend on $\psi$, and on the choices the same proposal made at earlier operations of the segment, since a proposal draws its choices one after another. Rejection sampling stays exact as long as every acceptance factor is at most one: for an operation with Kraus operator $K$ proposed with bound $b$, the factor is $\lVert K \varphi \rVert^2 / (b \lVert \varphi \rVert^2)$, where $\varphi$ is the state the operator acts on. A valid bound must therefore be at least this probability for every $\varphi$ that can occur at that operation, given $\psi$ and the earlier choices of the proposal. The product of the factors is then the probability of the path divided by its proposal weight, as in noisecirc's current scheme, and each accepted path carries the probability it has under the circuit.

For amplitude damping of strength $\gamma$ on qubit $q$, the jump has probability $\gamma\, n_q(\varphi)$, where $n_q$ is the excited population; noisecirc's bound is $\gamma$, i.e. $n_q \le 1$. The state $\varphi$ follows from $\psi$ by the operations of the segment before the channel, including the gate the channel follows. Two cases give a smaller valid bound:

- **Rule D, diagonal prefix.** If every operation on $q$ since the start of the segment is diagonal in the computational basis (controlled phases, $z$ rotations, no-jump damping), and no jump on another qubit was proposed earlier in the segment, then $n_q(\varphi) \le n_q(\psi) / \prod (1-\gamma_c)$. Diagonal unitaries commute with the projector on $|1\rangle_q$ and leave $n_q$ unchanged; a no-jump operator $K_0$ on a qubit $c$ renormalizes the state by $\langle K_0^\dagger K_0 \rangle \ge 1 - \gamma_c$ while $K_0^\dagger K_0 \le 1$, which raises $n_q$ by at most the factor $1/(1-\gamma_c)$. A jump on another qubit can raise $n_q$ to one (it conditions on that qubit having been excited), so after one the rule falls back to $\gamma$.
- **Rule S, single-qubit prefix.** If every operation on $q$ since the start of the segment acts on $q$ alone, $n_q(\varphi) \le \lambda_{\max}(\rho_q(\psi)) / \prod(1-\gamma_c)$, with $\rho_q$ the reduced density matrix of $q$: unitaries on $q$ keep its spectrum, and operations elsewhere only renormalize as above.

Mixing both kinds of operations voids both rules: after a controlled-Z, which can disentangle $q$ from a partner, a rotation can reach $n_q = 1$ even if $n_q(\psi) = \lambda_{\max} = 1/2$ (for example $(|0\rangle|+\rangle + |1\rangle|-\rangle)/\sqrt 2$ becomes $|+\rangle|+\rangle$).

### Which information is free

Every pass writes the probabilities of chunks of 256 consecutive amplitudes in its block's tile order, so the populations of all qubits except the 8 lowest of that order follow from the chunk sums of the checkpoint's last pass, at the cost of a small reduction over the chunk sums. The populations of the 8 lowest qubits need a reduction during the pass, and rule S needs the coherences of the reduced density matrices, which a single pass provides only for qubits within its tile.

### Estimate

`code/bench/a10_estimate.py` takes the dry run's passes of every block (28 qubits, damping at $M$ = 0.1 and 1, 1000 shots, noisecirc's defaults) and scales its error passes by the ratio of tightened to current error-proposal weight of the block, $\sum \gamma\, \hat n_q$ against $\sum \gamma$. The checkpoint populations come from the dry run's surrogate (each qubit pure from $|0\rangle$ until an operation entangles it, maximally mixed after). Four variants:

- *free*: rule D with the populations the chunk sums provide;
- *all*: rule D with every population;
- *all+S*: rules D and S;
- *oracle*: bounds equal to the population the jump acts on, the limit of any valid bound.

## Runs

LOG.md entries "A10 dry-run estimate of tighter proposal bounds" and "A10 dry-run estimate with oracle bound" (2026-10-24): `data/20261024-092215-a10-dry-run-estimate-with-oracle-bound/`.

## Results

### Most rejected proposals cannot be avoided with checkpoint information (dry-run estimate)

The table gives the block passes relative to noisecirc's current scheme (1.00 = no saving):

| circuit | share of error passes | free | all | all+S | oracle |
| --- | --- | --- | --- | --- | --- |
| GHZ | 59 to 72% | 0.99 | 0.99 | 0.99 | 0.64 to 0.71 |
| brickwork | 16 to 21% | 0.99 | 0.99 | 0.99 | 0.90 to 0.92 |
| QFT | 20 to 22% | 0.94 | 0.85 to 0.87 | 0.85 to 0.87 | 0.84 to 0.85 |
| QAOA | 25 to 31% | 0.96 to 0.97 | 0.96 to 0.97 | 0.96 to 0.97 | 0.85 to 0.88 |
| grid | 8 to 12% | 0.99 | 0.99 | 0.99 | 0.94 to 0.96 |
| scramble | 12 to 16% | 0.99 | 0.98 to 0.99 | 0.98 to 0.99 | 0.92 to 0.94 |

Three findings:

- **The avoidable part is small even in the limit.** Perfect bounds (oracle) would save 4 to 36% of the passes: the rejected proposals are about half of the error passes, and the error passes are 8 to 72% of all passes. The most is possible for GHZ, whose few blocks make error proposals the majority of its work.
- **Valid bounds capture the limit only for diagonal-heavy circuits.** For the QFT, whose controlled phases follow each other on the same qubits, rule D with all populations reaches nearly the oracle (13 to 15% of the passes), and 6% with the free populations alone. For the other circuits, the channels mostly follow a rotation that comes after an entangling gate in the same block, where neither rule holds; they save at most 4% (QAOA).
- **Rule S adds nothing.** Because noisecirc's blocks follow light cones, a qubit's first operation in a block is rarely a single-qubit gate that is not preceded by an entangling one in the same block: on brickwork, 28 of 826 channels qualify, all on qubits still in their initial state, where $\lambda_{\max} = 1$.

In time, the saving is somewhat larger than in passes, as error passes use the slower general kernel: for the QFT at $M = 1$, whose error passes take about 27% of its time, about 8% with the free populations and 17% with all of them (kernel ratios of the QFT at 28 qubits from [Block-pass time on the H100](block-pass-time.md)).

## Caveats

- The estimate scales the dry run's error passes by the change of the bound weight; it does not run a sampler with state-dependent proposals, whose refill rounds and deduplication would change the counts somewhat.
- The checkpoint populations are the surrogate's: maximally mixed for every entangled qubit. In real circuits, populations may be farther from 1/2 (e.g. after amplitude damping has relaxed a qubit), which makes rule D more effective; the oracle column has the same limitation.
- Only amplitude damping; for channels whose error operators are not projective in the computational basis (e.g. depolarizing), the rules need other state information.

## Verdict

Checkpoint-dependent bounds are valid under the two rules above, and the proof needs nothing beyond the per-operation acceptance factors. Their benefit is small: with the information the GPU passes already provide, they save at most 6% of the passes (QFT) and up to 4% elsewhere; even perfect bounds would save 4 to 36%. The $2MN$ term is therefore mostly inherent to proposing without the state; implementing state-dependent proposal tables in noisecirc's proposer pays only for circuits rich in diagonal gates, such as the QFT. Not implemented.
