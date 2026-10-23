---
title: Block-pass cost model
summary: Runtime of a simulation as block passes times the time to read and write a state vector
type: concept
tasks: [A2, A3]
updated: 2026-10-23
---
# Block-pass cost model

## Description

The block-pass cost model predicts the runtime of a noisecirc simulation from two numbers: how many block passes the simulation makes, and how long one pass takes. A *block pass* is one launch of a fused block's kernel on one state vector, which reads and writes every amplitude once ([NoiseCirc's sampling algorithm](../concepts/noisecirc-algorithm.md)). The model in PLAN.md (task A2) assumes that a pass takes the time $t_{bw}(n)$ to read and write one state vector of $n$ qubits at the device's memory bandwidth, so that

$$T \approx P \, t_{bw}(n), \qquad t_{bw}(n) = \frac{2 \cdot 2^n \cdot 8\ \text{bytes}}{\text{bandwidth}}, \tag{1}$$

with $P$ the number of block passes (noisecirc's diagnostic `block_passes`). On the H100 PCIe, $t_{bw}$ is 0.155 ms at 24 qubits, 0.60 ms at 26 and 2.37 ms at 28 (a CuPy in-place scaling of one `complex64` state, 1.7 TB/s).

The model has two factors, which are studied separately:

- **The pass count $P$** depends on the circuit, the noise, the shots and noisecirc's parameters, not on the hardware. Task A3 predicts it, see [Pass-count model](#pass-count-model) below and the study [Block passes against noisecirc's parameters](../studies/pass-count.md).
- **The time per pass** depends on the block's content and on the hardware. Task A2 measures it, see [Block-pass time on the H100](../studies/block-pass-time.md).

### Pass-count model

For noisecirc's default of one block per segment in exact mode, the passes split into two kinds:

- **Continuations without error.** Every distinct accepted prefix (checkpoint) propagates its no-error path through the next block once, with the block's cheaper dominant kernel. Before block $b$ there are $1 + N(1 - e^{-M_{b-1}})$ distinct prefixes, where $N$ is the number of shots and $M_{b-1}$ the expected number of accepted errors per shot in the blocks before $b$.
- **Proposals with an error.** In exact mode a shot proposes on average one no-error path and $Z_b - 1$ paths with an error per block, where $Z_b$ is the block's oversampling factor (the product of its noisy gates' factors, Eq. (1) of [NoiseCirc's sampling algorithm](noisecirc-algorithm.md)). The error paths are mostly distinct, and each costs a pass of the general kernel, whether it is then accepted or rejected.

Together,

$$P \approx \underbrace{\sum_{b=1}^{B} \left[1 + N\left(1 - e^{-M_{b-1}}\right)\right]}_{P_{\text{dom}}} + \underbrace{N \sum_{b=1}^{B} \left(Z_b - 1\right)}_{P_{\text{gen}}}. \tag{2}$$

For $B$ blocks of equal noise and a total of $M$ accepted errors per shot, the first sum becomes $B\,[1 + N f(M)]$ with $f(M) = 1 - (1 - e^{-M})/M$, which grows as $M/2$ for small $M$ and tends to one for large $M$. For amplitude damping of strength $p$ on $C$ gate-qubit channels, $\sum_b (Z_b - 1) \approx pC$ and $M \approx pC/2$, because a proposed jump is accepted with the excited-state population, about one half. Normalised by the work of simulating every shot separately, $BN$ passes, this gives

$$\frac{P}{BN} \approx \frac{1}{N} + f(M) + \frac{2M}{B}. \tag{3}$$

Equation (3) contains the three regimes of noisecirc's sampling:

1. At weak noise ($NM \ll 1$), one trajectory serves all shots, and $P \approx B$.
2. At intermediate noise, the work grows linearly with $M$: $P/(BN) \approx M/2 + 2M/B$.
3. At strong noise ($M \gg 1$), every shot is its own trajectory, and $P \approx BN + 2MN$; the rejected proposals add $2M$ passes per shot.

The circuit enters only through $B$ (fusion) and $C$ (noise channels). The refinements used for the predictions in [Block passes against noisecirc's parameters](../studies/pass-count.md) are the actual block ceilings $Z_b$ instead of equal blocks, and the deduplication of error proposals that start from the same checkpoint and hit the same gate (few blocks and many shots).

### Time per pass

A pass takes longer than $t_{bw}$ when the block's arithmetic and shared-memory traffic exceed the time of moving the state, and the host adds work per batch of trajectories. The measured time is therefore written as

$$T \approx t_{bw}(n)\left(r_{\text{dom}} P_{\text{dom}} + r_{\text{gen}} P_{\text{gen}}\right) + T_{\text{host}}, \tag{4}$$

with kernel ratios $r_{\text{dom}}, r_{\text{gen}} \ge 1$ for the dominant and the general kernel. How large the ratios and the host term are on the H100, and in which regime Eq. (1) holds within a factor of 1.5, is the subject of [Block-pass time on the H100](../studies/block-pass-time.md).
