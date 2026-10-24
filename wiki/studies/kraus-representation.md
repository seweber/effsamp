---
title: Optimal Kraus representations for noisecirc
summary: Which Kraus set of a noise channel costs noisecirc the fewest passes, a lower bound, and the set that attains it (A12)
type: study
tasks: [A12]
status: verified
updated: 2026-10-24
---
# Optimal Kraus representations for noisecirc

## Question

A noise channel has many Kraus representations: any set $L_j = \sum_i V_{ji} K_i$ with an isometry $V$ describes the same channel. noisecirc's work depends on which set it samples, so PLAN.md task A12 asks how to choose the set, whether the intuition "make the first operator as dominant as possible, then the second, and so on, while keeping the oversampling small" is right, and whether a provably optimal choice exists.

## Approach

The study has three parts:

1. **Cost of a Kraus set.** Derive from the [Block-pass cost model](../concepts/block-pass-cost-model.md) the two numbers of a set that cost passes, and lower bounds on both.
2. **Optimal sets.** Minimise a weighted sum of the two numbers over all Kraus sets of seven channels, on one qubit and on two qubits (the noise after a two-qubit gate), and compare with the lower bound (`code/bench/a12_kraus.py`, `code/bench/a12_compare.py`).
3. **Passes.** Run the dry run of [Block passes against noisecirc's parameters](pass-count.md) with noisecirc's canonical set, its option `optimize_kraus`, and the optimal set, on five circuits (`code/bench/a12_dryrun.py`).

The channels are those of `code/bench/noise.py` plus two mixtures, all at strength $p = 10^{-2}$:

- amplitude damping, phase damping (dephasing), depolarizing;
- generalized amplitude damping (excited bath population 0.2);
- thermal relaxation (damping $p$, then dephasing $p$);
- damping followed by depolarizing (`damp_depol`);
- damping after a coherent over-rotation $e^{-i\sqrt{p}X/2}$ (`damp_overrot`).

## Runs

- End to end on the GPU: `data/20261024-21*-a12-end-to-end-*-n-28/`, summary `data/a12-kraus/e2e.txt` (`code/bench/a12_e2e.py`).
- Optimisation over all sets for four weights, one qubit: `data/a12-kraus/weights-p0.01-1q.txt` (`code/bench/a12_weights.py`).
- Optimisation against the bound, one and two qubits: `data/a12-kraus/compare-p0.01-a.jsonl`, `data/a12-kraus/compare-p0.01-b.jsonl` (two-qubit optimum of `a12_compare.py` superseded by `optimize_residual`, see Results).
- Dry runs: `data/20261024-*-a12-dry-run-canonical-vs-optimal-kraus-sets-*-tensor-optimum/` (LOG.md "A12 dry run canonical vs optimal Kraus sets … (tensor optimum)"); earlier attempts that timed out are logged in LOG.md.

## Results

### What a Kraus set costs noisecirc (derivation)

noisecirc proposes operator $L_j$ with probability $\lVert L_j\rVert^2/Z$, where $\lVert\cdot\rVert$ is the operator norm and $Z = \sum_j \lVert L_j\rVert^2$ the oversampling factor, and accepts it with $\lVert L_j\psi\rVert^2/\lVert L_j\rVert^2$ ([NoiseCirc's sampling algorithm](../concepts/noisecirc-algorithm.md)). The operator with the largest bound, $L_0$, is the dominant one: its proposals from one checkpoint share one trajectory and use the cheap dominant kernel. Every other proposal is a trajectory of its own. Per gate and shot, two numbers of the set therefore cost passes:

- the **error proposals** $E = Z - \lVert L_0\rVert^2$, the expected proposals of non-dominant operators until a shot is accepted; each costs one pass of an error kernel, whether accepted or rejected;
- the **accepted errors** $\mu(\rho) = 1 - \mathrm{tr}(\rho L_0^\dagger L_0)$, for a gate input $\rho$; each accepted error starts a distinct trajectory that is propagated through all remaining blocks.

In the pass model, an accepted error at intermediate noise costs about $B f'(M)$ passes (half the blocks at weak noise, none at strong noise, when every shot is already distinct), while an error proposal costs one. A set is thus judged by $E + w\,\mu$ with a weight $w$ between 0 and about $B/2$.

### The greedy "most dominant first" rule is the canonical set (proved)

How dominant an operator is depends on the state it acts on: its acceptance is $\mathrm{tr}(\rho L_0^\dagger L_0)$. Writing $L_0 = \sum_i v_i K_i$ with $\lvert v\rvert \le 1$, this acceptance is $v^\dagger G v$ with the Gram matrix $G_{ik} = \mathrm{tr}(\rho K_i^\dagger K_k)$. For the maximally mixed input $\rho = I/d$, which is what an entangled qubit looks like locally, $G$ is diagonal in the canonical set (the eigenvectors of the Choi matrix), with entries $\lVert K_i\rVert_F^2/d$ in decreasing order. Hence:

- the most dominant single operator is the first canonical operator, and choosing the most dominant operator among the remaining ones, step by step, reproduces the canonical set (this is principal component analysis of the Choi matrix);
- the canonical set, noisecirc's default, therefore already minimises $\mu$ for a maximally mixed input.

The order of the non-dominant operators does not matter to noisecirc's pass count, so the greedy rule settles only the dominant operator. What it does not settle is $E$: the remaining canonical operators can carry far more oversampling than necessary.

### Lower bounds on the error proposals (proved)

Two inequalities bound $E$ for any set with dominant operator $L_0$:

$$E \ge 1 - \sigma_{\min}(L_0)^2, \qquad E \ge \bigl\lVert \mathcal{E}(I) - L_0 L_0^\dagger \bigr\rVert. \tag{1}$$

The first holds because a proposal must be made for every accepted error, so $E \ge \mu(\rho)$ for every state, and the worst state gives $1-\sigma_{\min}^2$. The second holds because $\lVert L\rVert^2 \ge \langle\phi|LL^\dagger|\phi\rangle$ for one $\phi$ shared by all non-dominant operators, whose $\sum_j L_jL_j^\dagger$ is $\mathcal{E}(I) - L_0L_0^\dagger$. Since $\lVert L_0\rVert \le 1$, the second gives a bound that holds for every set:

$$E \ge \lVert\mathcal{E}(I)\rVert - 1, \tag{2}$$

the non-unitality of the channel. For amplitude damping, $\mathcal{E}(I) = \mathrm{diag}(1+\gamma, 1-\gamma)$, so $E \ge \gamma$, which the canonical set attains.

The lower bound on $E + w\mu$ is the minimum of the larger bound in Eq. (1) plus $w\mu$, over all dominant operators $L_0$ in the span of the canonical set (`a12_kraus.lower_bound`). It is a certificate: a set reaching it is optimal.

### One set is optimal for every weight: canonical dominant, optimised rest (verified numerically)

For all seven channels on one qubit, minimising $E + w\mu$ over all Kraus sets (with up to two extra operators) for $w = 0, 1, 5, 50$ gave the same set for every weight, and it reached the lower bound. There is no trade-off between error proposals and accepted errors. The optimal set keeps the canonical dominant operator, which minimises $\mu$, and mixes the remaining operators to minimise their oversampling down to the bound of Eq. (1).

For two qubits, minimising over all sets stalled at the canonical set, a degenerate stationary point. Keeping the canonical dominant operator and minimising only the rest from many random starts (`a12_kraus.optimize_residual`) reached the lower bound within 0.5% in all fourteen cases. The table gives the error proposals and accepted errors per gate in units of $p$:

| channel | qubits | canonical $E$ | `optimize_kraus` $E$ ($\mu$) | optimal $E$ | bound $E$ | $\mu$ (canonical = optimal) |
| --- | --- | --- | --- | --- | --- | --- |
| amplitude damping | 1 / 2 | 1.00 / 2.01 | 1.00 / 2.01 | 1.00 / 2.01 | 1.00 / 2.01 | 0.50 / 1.00 |
| dephasing | 1 / 2 | 0.25 / 1.00 | 0.25 / 0.89 (0.88) | 0.25 / 0.50 | 0.25 / 0.50 | 0.25 / 0.50 |
| depolarizing | 1 / 2 | 1.67 / 3.82 | 1.01 / 2.00 | 1.00 / 1.99 | 1.00 / 1.99 | 1.00 / 1.99 |
| generalized damping | 1 / 2 | 1.00 / 2.01 | 0.81 / 1.61 | 0.80 / 1.60 | 0.80 / 1.60 | 0.50 / 1.00 |
| thermal relaxation | 1 / 2 | 1.25 / 3.00 | 1.25 / 2.52 | 1.25 / 2.51 | 1.25 / 2.50 | 0.75 / 1.49 |
| damping + depolarizing | 1 / 2 | 2.66 / 5.98 | 1.99 / 3.98 | 1.99 / 3.97 | 1.99 / 3.95 | 1.49 / 2.96 |
| damping + over-rotation | 1 / 2 | 1.00 / 2.01 | 1.00 / 2.01 | 1.00 / 2.01 | 1.00 / 2.01 | 0.50 / 1.00 |

For the noise after a two-qubit gate, the tensor square of the optimal one-qubit set is within 0.6% of the two-qubit bound for all seven channels (`a12_kraus.optimize_residual` and the bounds above): optimising each qubit's channel separately is enough.

Three conclusions follow:

- **Amplitude damping and its coherent variants:** the canonical set is optimal, provably by Eq. (2) and the maximal dominance.
- **Channels with a mixed-unitary or degenerate part** (depolarizing, dephasing on two qubits, damping plus depolarizing, generalized damping, thermal relaxation on two qubits): the canonical set makes 1.2 to 2 times more error proposals than necessary, at the same accepted errors.
- **noisecirc's `optimize_kraus`** (branch `fix/optimize-kraus-dominant`) is within 1% of the optimum in all cases but one: dephasing after a two-qubit gate, where it leaves the canonical dominant operator and makes 1.76 times more accepted errors (0.88 instead of 0.50). The cause is its target: it aims at the bound $\max(1, \lVert\mathcal{E}(I)\rVert)$ on the whole oversampling, which its first stage (dominant kept) fails to reach from its start, so it falls back to rotating all operators. Aiming at the bound of Eq. (1) with the dominant operator fixed, and starting from several random points, would make it optimal; see [Issues found in noisecirc](noisecirc-issues.md), item 4.

### Effect on the passes (dry run)

The dry run counts the block passes of the five benchmark circuits at 28 qubits with 1000 shots, at the strengths that give amplitude damping $M = 0.1$ and 1 expected errors per shot, once with noisecirc's canonical sets and once with the optimal ones (for two-qubit gates the tensor square of the optimal one-qubit set). The table gives canonical over optimal passes at $M = 0.1$ / $M = 1$, means of three seeds:

| noise | GHZ | brickwork | QFT | QAOA | grid |
| --- | --- | --- | --- | --- | --- |
| depolarizing | 1.27 / 2.37 | 1.31 / 1.27 | 1.30 / 1.31 | 1.22 / 1.36 | 1.23 / 1.26 |
| damping + depolarizing | 1.14 / 1.74 | 1.08 / 1.19 | 1.17 / 1.23 | 1.16 / 1.25 | 1.15 / 1.12 |
| dephasing | 1.42 / 1.61 | 1.17 / 1.12 | 1.67 / 1.34 | 1.32 / 1.18 | 1.51 / 1.11 |
| generalized damping | 1.10 / 1.25 | 1.08 / 1.11 | 0.93 / 1.11 | 1.11 / 1.10 | 1.12 / 1.14 |
| thermal relaxation | 1.12 / 1.11 | 1.09 / 1.03 | 1.11 / 1.12 | 0.96 / 1.05 | 0.96 / 1.04 |

With the optimal sets, noisecirc needs 1.2 to 1.4 times fewer passes for depolarizing noise (GHZ at $M = 1$: 2.4 times), 1.1 to 1.7 times fewer for dephasing and for damping plus depolarizing, and about 1.1 times fewer for generalized damping and thermal relaxation, where the dry run's scatter (single entries of 0.93 to 0.96) is of the same order. For amplitude damping the sets are identical.

### Effect on the run time (verified on the GPU)

Whole runs at 28 qubits on the H100 (`bench/fixes`, 1000 shots, medians of three seeds) confirm the dry run: with the optimal sets, brickwork and QFT run 1.33 to 1.40 times faster with depolarizing noise and 1.12 to 1.23 times faster with damping plus depolarizing, with 1.0 to 1.5 times fewer passes (`data/a12-kraus/e2e.txt`, LOG.md "A12 end-to-end …").

## Caveats

- The optimality is per gate and for a maximally mixed input. A qubit waiting in a basis state could use a set adapted to that state (lower $\mu$), but such state-dependent unravellings gained nothing in the A10 study ([Checkpoint-dependent proposal bounds](tighter-bounds.md)).
- Optimality is certified numerically for the fourteen cases listed, not proved for every channel; the lower bound is found by a non-convex minimisation over the dominant operator, so it is exact up to the search.
- The weight $w$ was treated as a free parameter; that the optimum does not depend on it is an observation for these channels.
- Pass counts are dry runs (surrogate states); for channels other than damping, the surrogate's acceptance is the maximally mixed one.

## Verdict

The intuition of PLAN.md task A12 holds and can be made precise. Dominance is the weight $\mathrm{tr}(\rho L_0^\dagger L_0)$ of the operator that all no-error shots share, and choosing the most dominant operator first, then the next, gives exactly the canonical Kraus set, noisecirc's default. What the greedy rule leaves open is the oversampling of the other operators, and there the canonical set can be far from optimal. The optimal set for noisecirc keeps the canonical dominant operator and mixes the others down to the lower bound of Eq. (1); it is optimal for every weighting of error proposals against accepted errors, so there is no trade-off, and for a two-qubit gate the tensor square of the one-qubit optimum is within 0.6% of optimal. Optimality is certified numerically by the lower bound for seven channels (within 0.5%), not proved in general.

For amplitude damping and its coherent variants the canonical set is already optimal, provably. For channels with a mixed-unitary or degenerate part the optimal set needs 1.1 to 2.4 times fewer passes and makes runs 1.1 to 1.4 times faster. noisecirc's `optimize_kraus` reaches nearly the same sets once the residual target is fixed (branch `fix/optimize-kraus-residual-target`). Because $E$ and $\mu$ do not change when an operator is multiplied by a unitary, the optimisation needs to run once per noise channel rather than once per gate, which would remove most of its compile time.
