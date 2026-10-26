---
title: GPU environment on bux
summary: How to run code on bux GPU 0 in the bench podman image
type: topic
status: active
updated: 2026-10-26
---
# GPU environment on bux

## Know-how

- PLAN.md: GPU 0 of bux only, directly (no Slurm); every run ≤ 10 min (gpurun uses `timeout 590`).
- Podman's default store is on NFS (`/itp3/home/sebastian-ai/.local/share/containers`) and fails with `lsetxattr ... operation not supported`. `~/remote/bench/pm` wraps podman with `--root /tmp/sebastian-ai-bench/storage --runroot /tmp/sebastian-ai-bench/run` (bux local disk). A `storage.conf` via `CONTAINERS_STORAGE_CONF` was read but its graphroot ignored (podman DB remembers the old root) — use the flags.
- Image `localhost/bench:latest` from `~/remote/bench/image/Containerfile` (python:3.13-bookworm + uv 0.9.5 + build tools). Build: `gpu_exec bash -lc 'cd ~/bench/image && ~/bench/pm build -t bench:latest .'`.
- `~/remote/bench/run CMD` runs CMD in the image with `--device nvidia.com/gpu=0`, `~/bench` at `/work`, and `/tmp/sebastian-ai-bench/local` at `/local` holding the venv (`UV_PROJECT_ENVIRONMENT=/local/venv`), uv cache, svpass kernel cache and numba cache (local disk, fast; lost on bux reboot → rerun `uv sync --group research`).
- `code/bench/gpurun [-t S] script.py args` rsyncs `code/noisecirc-bench` (a git worktree of noisecirc branch `bench/fixes`, ignored by the outer repo) → `~/remote/bench/noisecirc` and `code/bench` → `~/remote/bench/bench`, then runs `uv run --frozen --group research python /work/bench/script.py` in the image. Develop in `code/noisecirc` (any branch except bench/fixes); merge fixes into bench/fixes inside `code/noisecirc-bench`. Before 2026-10-24 00:50 UTC gpurun synced `code/noisecirc`'s working tree, and a branch switch during a batch corrupted one run (LOG.md "Invalid run ...").
- Local rsync to the sshfs mount: use `-rlt` (`-a` fails on chgrp).
- Env verified 2026-10-23: 178 noisecirc tests pass on the H100; qiskit-aer-gpu-cu11 0.17.2 sees GPU; cudaq 0.15.1 imports.
- Local CPU dry runs: the venv `code/noisecirc/.venv` imports noisecirc from `code/noisecirc` (checked out at `main`). To dry-run `bench/fixes`, prepend `PYTHONPATH=$PWD/code/noisecirc-bench/src:$PWD/code/noisecirc-bench/packages/svpass/src` (from the project root). Do not pgrep -f for a script name inside a wait loop whose own command line contains that name (it matches itself).
- Never edit code/bench/gpurun while a batch runs: bash reads scripts lazily (a7 group_amplitudes=8192 run ended with a syntax error after its output was complete).
- Branch feature/stage-contraction (from feature/stage-fusion; adds stage_contraction) and feature/stage-fusion (A14 flags stage_fusion, rotation_form; A15 prototype stage_populations) is run with `gpurun -s noisecirc` after `git -C code/noisecirc checkout feature/stage-fusion`; code/noisecirc is left on main. Worktree code/noisecirc-fix holds fix/optimize-kraus-residual-target (ignored by the outer repo).
- Never `pkill -f PATTERN` or `ps | grep PATTERN | kill` from a shell whose own command line contains PATTERN (also inside heredocs): it kills the calling shell (exit 144; happened 3 times on 2026-10-24). Kill by PID found in a separate command, or wait on status files.
- `research-run` writes stdout.txt progressively but status.txt only at the end; two research-runs started in the same second get distinct dirs only if titles differ.
- 2026-10-25 from ~09:45 CET (still at 20:27 CET): GPU 0 of bux fails CUDA init (`cuInit` returns 3, CUDA_ERROR_NOT_INITIALIZED) on the host and in the container; nvidia-smi shows it idle and error-free, device nodes open, GPU 1 initializes fine. Not fixable without admin; PLAN.md forbids other GPUs -> GPU work blocked, retried periodically. SASS analysis works without GPU: NVRTC (local venv) for sm_90 + nvdisasm from pip `nvidia-cuda-nvdisasm` (scratch venv; on bux /local/venv-sass), see code/bench/a13_sass.py.
- 2026-10-25 ~23:00 CET: bux rebooted (driver 595.71 -> 595.99); GPU 0 initializes again (cuInit 0). The reboot wiped /tmp/sebastian-ai-bench (image, /local venv): rebuilt image (`gpu_exec bash -lc 'cd ~/bench/image && ~/bench/pm build -t bench:latest .'`, ~1 min), venv re-synced by the first gpurun. /etc/cdi/nvidia.yaml is stale (595.71) and podman 4.6 reads it (`--device nvidia.com/gpu=0` fails: cannot stat libEGL_nvidia.so.595.71.05); `cdi_spec_dirs` via CONTAINERS_CONF(_OVERRIDE) was ignored. Fix: ~/remote/bench/run passes only /dev/nvidia0 + nvidiactl/uvm/uvm-tools and binds libcuda/ptxjit/nvvm/nvml (version from /sys/module/nvidia/version) and nvidia-smi; old script ~/remote/bench/run.cdi-backup. After the next reboot: check `~/bench/pm images` and rebuild if empty.
- svpass caches compiled kernels in memory (`svpass.engine._compiled`) by block digest and Config, not by source: a script that monkeypatches `codegen.kernel_source` must clear it per variant (A16 ablations were invalid until it did).
- `mma.sync` peaks on GPU 0 (code/bench/a16_mma_rate.py): f16 m16n8k16 483 TFLOP/s, tf32 m16n8k8 242, FP32 FFMA 41.7 (4+ independent chains per warp needed).
- Branch feature/tensor-cores (from feature/stage-contraction) holds every kernel flag so far: stage_fusion, rotation_form, stage_populations, additive_addresses, stage_contraction, tensor_cores/tensor_unroll/tensor_threshold, free_diagonals (all off by default); check it out in code/noisecirc and run `gpurun -s noisecirc`; code/noisecirc is left on main.
