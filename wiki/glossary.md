# Glossary

## Abbreviations

- **ARRAY** — ACM SIGPLAN workshop on libraries, languages and compilers for array programming
- **CPU** — central processing unit
- **CUDA** — NVIDIA's GPU programming platform
- **CUDA-Q** — NVIDIA's quantum programming platform, with GPU state-vector simulators
- **cuStateVec Ex** — the extended API of NVIDIA's cuStateVec library, whose state-vector updater (SVUpdater) applies queued gates and noise channels with qsim's delayed lower-bound sampling
- **DAC** — Design Automation Conference
- **GB**, **MB**, **TB** — gigabyte, megabyte, terabyte (10^9, 10^6, 10^12 bytes)
- **GHZ** — Greenberger–Horne–Zeilinger state; here the circuit preparing it as a chain of controlled phases
- **GPU** — graphics processing unit
- **H100** — NVIDIA H100 PCIe, the GPU used here (GPU 0 of bux)
- **KB** — kilobyte, 1024 bytes
- **TF32** — NVIDIA's tensor-core format with an 8-bit exponent and a 10-bit significand
- **TFLOP** — $10^{12}$ floating-point operations
- **HPCA** — International Symposium on High-Performance Computer Architecture
- **ICS** — International Conference on Supercomputing
- **PTSBE** — pre-trajectory sampling with batched execution, CUDA-Q's method of pre-sampled noisy trajectories
- **QAOA** — quantum approximate optimization algorithm; here MaxCut on a random 3-regular graph
- **QFT** — quantum Fourier transform
- **RTX** — prefix of NVIDIA's consumer GPUs; the RTX 4060 Ti is the GPU noisecirc was tuned on
- **SANQ** — simulation framework for noisy intermediate-scale quantum computers (Li, Ding, Xie)
- **SC21** — Supercomputing conference 2021
- **SV-Sim** — a GPU state-vector simulator (SC21)
- **TUSQ** — tracking, uncomputation and sampling for noisy quantum simulation (ISCA 2026)

## Notation

- $n$ — number of qubits of the register
- $N$ — number of shots
- $B$ — number of fused blocks of a compiled circuit
- $C$ — number of noise channels: gate-qubit pairs, as every gate is followed by noise on each of its targets
- $p$ — noise strength of a channel (for amplitude damping: the jump probability $|1\rangle \to |0\rangle$)
- $b_i$ — upper bound of Kraus operator $i$'s probability, the largest eigenvalue of $K_i^\dagger K_i$
- $Z$ — oversampling factor of a gate, $\sum_i b_i$; $Z_b$ of block $b$, the product over its gates
- $M$ — expected number of accepted errors per shot; for damping $M \approx pC/2$
- $\mu$ — expected accepted errors per shot of one channel
- $P$ — block passes: launches of a block's kernel times the trajectories they propagate (noisecirc's `block_passes`); $P_{\text{dom}}$ and $P_{\text{gen}}$ its passes with the dominant and the general kernel
- $t_{bw}(n)$ — time to read and write one `complex64` state of $n$ qubits at the measured bandwidth
- $r_{\text{dom}}$, $r_{\text{gen}}$ — pass time of the dominant and the general kernel over $t_{bw}$
- $f(M)$ — $1 - (1 - e^{-M})/M$, the mean fraction of shots carrying a distinct prefix
- **stage** — a run of a block's operations on at most `stage_qubits` qubits that a kernel applies together from registers
- **dominant / general / masked kernel** — a block's kernel for trajectories without error (each gate's most likely Kraus choice), for any choices (switching on each gate's choice in every stage), and for trajectories with errors that runs the dominant code in every stage but those its stage mask flags
- **autotuning** — noisecirc's choice of `max_operations` and `stage_qubits` per circuit by timing one trajectory under each candidate (branch `feature/autotune`)
- **fusion width** — the most qubits of one fused operation: Aer's `fusion_max_qubit` (2 by default for circuits with Kraus noise), noisecirc's `max_fused_qudits` plus its pinned qubits
- $E$ — error proposals of a Kraus set per gate and shot, $Z - \lVert L_0\rVert^2$: proposals of non-dominant operators until acceptance, each a pass of an error kernel
- $\mu(\rho)$ — accepted errors of a Kraus set per gate for input $\rho$, $1 - \mathrm{tr}(\rho L_0^\dagger L_0)$, with $L_0$ the dominant operator
- **canonical Kraus set** — the Kraus operators from the eigenvectors of the channel's Choi matrix, largest first; noisecirc's default
- $F$, $S$ — floating-point instructions and shared-memory accesses per amplitude of a pass; $F_{bw} \approx 206$, $S_{bw} \approx 29$ the numbers the H100 issues in $t_{bw}$ per amplitude
- **instruction-bound pass** — a pass whose time is set by the instructions it issues (arithmetic plus shared accesses), not by moving the state
- **complex32** — noisecirc's/svpass's precision that stores each amplitude as two 16-bit floats and computes in single precision
- **stage fusion** — multiplying a run of a stage's operations into one matrix where that needs fewer instructions (svpass `Config.stage_fusion`, branch `feature/stage-fusion`)
- **rotation form** — applying a one-qubit gate as $D_L T D_R$ with a real two-term rotation $T$ and diagonals deferred at generation time (svpass `Config.rotation_form`)
- **first-jump sampling** — splitting a checkpoint's shots exactly over the first error in a block, with probabilities reduced during the dominant pass, instead of proposing errors from bounds (A15 idea, reference implementation only)
- **readout map** — moving noise channels in a circuit's diagonal tail out of the simulation into a classical map on the sampled bits
- **SASS** — the GPU's native instruction set, the code the CUDA compiler actually emits; disassembled with `nvdisasm` to count the instructions a kernel executes
- **HFMA2** — a GPU instruction that performs two half-precision fused multiply-adds at once
- **sequential Kraus set** — among the Kraus sets with minimal oversampling, the one whose bounds are concentrated on the first remaining operators (A12 follow-up)
- **additive addresses** — shared-memory addresses of a stage split into a part of the thread and an immediate offset (svpass `Config.additive_addresses`)
- **contraction order** — which of a stage's gates are multiplied into one matrix before being applied to the registers, and in which sequence (svpass `Config.stage_contraction` applies the cheapest)
- **down-set** — a set of a stage's gates that contains, with every gate, all earlier gates it depends on (those sharing a qubit with it); the gates applied before any point of a contraction order
- **NVRTC** — NVIDIA's runtime compiler for CUDA source, which svpass uses to compile kernels; it compiles for a given architecture without a GPU
- **FMA** — fused multiply-add, $a \cdot b + c$ in one instruction with one rounding; FFMA, FMUL and FADD are the GPU's single-precision fused multiply-add, multiply and add instructions
- **FMUL** — see FMA
- **FP32** — single-precision (32-bit) floating point
