---
title: Optimal Kraus representations for noisecirc
summary: Which Kraus set of a noise channel costs noisecirc the fewest passes, a lower bound, and the set that attains it (A12)
type: study
tasks: [A12]
status: verified
updated: 2026-10-25
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
- Shot merging: per-gate costs `data/20261025-0851*-a12-collision-aware-kraus-sets-*` (`code/bench/a12_collisions.py`); dry runs with the sequential sets `data/20261025-*-a12-dry-run-sequential-kraus-sets-*` (1000 and 10 000 shots).
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

In the cost $E + w\mu$, which counts every proposal and every accepted error as one pass, only the dominant operator's choice matters; the remaining operators enter only through their total oversampling $E$. That cost ignores that noisecirc merges shots which propose the same error, where the shape of the remaining operators matters as well; the section *Shots that propose the same error share one pass* below treats this, and shows that the greedy rule is then optimal for the remaining operators too. What the greedy rule does not settle is $E$: the remaining canonical operators can carry far more oversampling than necessary.

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

### Shots that propose the same error share one pass: the sequential rule for the remaining operators (proved and verified)

The cost $E + w\mu$ above counts every error proposal and every accepted error as a pass of its own. noisecirc merges shots, though: all shots of a checkpoint that propose the same operator at the same gate form one trajectory and one pass (`propose_unique_trajectories`). When $n$ shots cross a gate and operator $L_j$ is proposed with probability $b_j = \lVert L_j\rVert^2$ and accepted with probability $a_j = \mathrm{tr}(\rho L_j^\dagger L_j)$, the expected passes are therefore

$$P_n = \sum_{j \ge 1} \bigl(1 - e^{-n b_j}\bigr), \qquad A_n = \sum_{j \ge 1} \bigl(1 - e^{-n a_j}\bigr), \tag{3}$$

distinct error proposals and distinct accepted errors. For $n b_j \ll 1$ they are $nE$ and $n\mu$, the cost used so far. For $n b_j \gtrsim 1$ they saturate: a second shot proposing the same operator costs nothing. Then it pays to concentrate the error probability on few operators, and the shape of the remaining operators matters, not only their sum. At the root checkpoint of the dry runs, $n p$ is between about 0.1 ($M = 0.1$, 1000 shots) and 20 ($M = 1$, 10 000 shots), so this regime is the relevant one.

**The sequential rule minimises the distinct accepted errors (proved).** The vector $(a_j)$ of any Kraus set is the diagonal of the Gram matrix $G$ of the section on the greedy rule, written in a rotated basis and padded with zeros. By the Schur–Horn theorem, the eigenvalues $\lambda$ of $G$ majorise it. The cost $\sum_{j \ne \text{dom}} \phi(a_j)$ of Eq. (3), with $\phi(a) = 1 - e^{-na}$ concave and increasing, is Schur-concave: moving probability from a smaller to a larger operator, or onto the dominant one, never increases it. Hence for every $n$ (and every concave $\phi$) the minimum of $A_n$ is attained by the eigenvectors of $G$: the most dominant operator first, then the most dominant of the rest, and so on. For a maximally mixed input that is the canonical set. So the intuition of PLAN.md task A12 holds for all operators, not only the first, once shot merging is counted.

**A lower bound for the proposals (proved).** Each operator is proposed at least as often as it is accepted ($b_j \ge a_j$), so $P_n \ge A_n \ge A_n^{\text{canonical}}$. Hence

$$P_n + w A_n \ge (1 + w)\, A_n^{\text{canonical}} \tag{4}$$

for every set. A set attains it if its operators are the canonical ones up to a unitary mixing that keeps $a_j$ and has $b_j = a_j$, which holds when every remaining operator is proportional to a unitary. For depolarizing noise the Pauli set does this, so it is optimal at every $n$.

**The best set at intermediate $n$ (verified numerically).** Minimising $P_n + wA_n$ over all sets with the canonical dominant operator (`code/bench/a12_collisions.py`, $p = 10^{-2}$, $x = np$ from 0.1 to 30, $w = 0, 1, 5$) separates the channels into two groups. For depolarizing, dephasing and thermal relaxation, the optimum is the same at every $n$: the Pauli set or the canonical set. For generalized amplitude damping and damping plus depolarizing, the sets that minimise the oversampling $E$ are not unique. Among them, the one that concentrates the bounds on the first remaining operators is best; it is called the *sequential* set here. The table gives the per-gate costs for one qubit, in units of $p$ for $E$ and as counts for $P$ and $A$:

| channel | set | bounds $b_j/p$ | $E$ | $P_n$ at $np = 0.1$ / 1 / 10 | $A_n$ at $np = 1$ / 10 |
| --- | --- | --- | --- | --- | --- |
| generalized damping | canonical | 0.80, 0.20 | 1.00 | 0.097 / 0.73 / 1.87 | 0.43 / 1.62 |
| | minimal $E$ (previous optimum) | 0.45, 0.35 | 0.80 | 0.078 / 0.66 / 1.96 | 0.44 / 1.84 |
| | sequential | 0.64, 0.16 | 0.80 | 0.078 / 0.62 / 1.80 | 0.44 / 1.77 |
| damping + depolarizing | canonical | 1.65, 0.67, 0.34 | 2.66 | 0.250 / 1.58 / 2.96 | 1.13 / 2.93 |
| | minimal $E$ (previous optimum) | 0.93, 0.72, 0.34 | 1.99 | 0.192 / 1.40 / 2.96 | 1.16 / 2.96 |
| | sequential | 1.18, 0.48, 0.34 | 1.99 | 0.190 / 1.36 / 2.96 | 1.16 / 2.95 |

Three observations follow from the table and the optimisation:

- **The sequential set keeps the minimal oversampling and concentrates it.** Its bounds have the shape of the canonical ones (for generalized damping exactly: 0.64 : 0.16 = 0.80 : 0.20) scaled down to the minimal $E$. It makes fewer distinct proposals than the previous optimum at every $n$, by 6 to 8% at $np = 1$ to 10.
- **At large $n$ and $w \ge 1$, the canonical set wins again.** The optimisation at $np = 10$ with $w = 1$ or 5 returns the canonical set, because its accepted errors are the most concentrated (Schur–Horn), while every set's proposals are nearly saturated.
- **Applying the rule to the bounds instead of the acceptances does not help.** Choosing the operator with the largest bound $\lVert L\rVert^2$ first, then the largest among the rest (`greedy` in the script), was never better than the canonical set and up to 3% worse.

In the dry runs of the five circuits at 28 qubits, these per-gate differences hardly show. With 1000 shots, the sequential sets need the same passes as the previous optimum within the dry run's scatter (ratios 0.97 to 1.04 for damping plus depolarizing; 0.85 to 1.08 for generalized damping, mostly within 4%). With 10 000 shots of generalized damping, GHZ needs 3 to 4% fewer passes with the sequential set and the QFT the same. Both remain 1.1 to 1.7 times fewer than with the canonical sets. Error proposals are only part of a run's passes, and the sets differ only in how the proposals are spread.

## Caveats

- The optimality is per gate and for a maximally mixed input. A qubit waiting in a basis state could use a set adapted to that state (lower $\mu$), but such state-dependent unravellings gained nothing in the A10 study ([Checkpoint-dependent proposal bounds](tighter-bounds.md)).
- Optimality is certified numerically for the fourteen cases listed, not proved for every channel; the lower bound is found by a non-convex minimisation over the dominant operator, so it is exact up to the search.
- The weight $w$ was treated as a free parameter; that the optimum does not depend on it is an observation for these channels, and holds only while shots rarely propose the same error ($np \ll 1$).
- The cost with shot merging, Eq. (3), treats each gate on its own with a fixed number of shots; in a run, $n$ changes from gate to gate and checkpoint to checkpoint, so one set per channel cannot be optimal everywhere.
- Pass counts are dry runs (surrogate states); for channels other than damping, the surrogate's acceptance is the maximally mixed one.

## Verdict

The intuition of PLAN.md task A12 holds and can be made precise. Dominance is the weight $\mathrm{tr}(\rho L_0^\dagger L_0)$ of the operator that all no-error shots share, and choosing the most dominant operator first, then the next, gives exactly the canonical Kraus set, noisecirc's default. What the greedy rule leaves open is the oversampling of the other operators, and there the canonical set can be far from optimal. The optimal set for noisecirc keeps the canonical dominant operator and mixes the others down to the lower bound of Eq. (1); it is optimal for every weighting of error proposals against accepted errors, so there is no trade-off, and for a two-qubit gate the tensor square of the one-qubit optimum is within 0.6% of optimal. Optimality is certified numerically by the lower bound for seven channels (within 0.5%), not proved in general.

Once noisecirc's merging of shots that propose the same error is counted, the shape of the remaining operators matters as well, and the sequential rule ("most dominant first, then the most dominant of the rest") is provably optimal for the distinct accepted errors at every shot count. Among the sets with minimal oversampling, the most concentrated one (the sequential set) makes the fewest distinct proposals, and at many shots per gate the canonical set itself becomes best. In the dry runs these refinements change the passes by at most a few percent; the large gain remains that of minimising the oversampling.

For amplitude damping and its coherent variants the canonical set is already optimal, provably. For channels with a mixed-unitary or degenerate part the optimal set needs 1.1 to 2.4 times fewer passes and makes runs 1.1 to 1.4 times faster. noisecirc's `optimize_kraus` reaches nearly the same sets once the residual target is fixed (branch `fix/optimize-kraus-residual-target`). Because $E$ and $\mu$ do not change when an operator is multiplied by a unitary, the optimisation needs to run once per noise channel rather than once per gate, which would remove most of its compile time.
