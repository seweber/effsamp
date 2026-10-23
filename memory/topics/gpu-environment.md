---
title: GPU environment on bux
summary: How to run code on bux GPU 0 in the bench podman image
type: topic
status: active
updated: 2026-10-23
---
# GPU environment on bux

## Know-how

- PLAN.md: GPU 0 of bux only, directly (no Slurm); every run ≤ 10 min (gpurun uses `timeout 590`).
- Podman's default store is on NFS (`/itp3/home/sebastian-ai/.local/share/containers`) and fails with `lsetxattr ... operation not supported`. `~/remote/bench/pm` wraps podman with `--root /tmp/sebastian-ai-bench/storage --runroot /tmp/sebastian-ai-bench/run` (bux local disk). A `storage.conf` via `CONTAINERS_STORAGE_CONF` was read but its graphroot ignored (podman DB remembers the old root) — use the flags.
- Image `localhost/bench:latest` from `~/remote/bench/image/Containerfile` (python:3.13-bookworm + uv 0.9.5 + build tools). Build: `gpu_exec bash -lc 'cd ~/bench/image && ~/bench/pm build -t bench:latest .'`.
- `~/remote/bench/run CMD` runs CMD in the image with `--device nvidia.com/gpu=0`, `~/bench` at `/work`, and `/tmp/sebastian-ai-bench/local` at `/local` holding the venv (`UV_PROJECT_ENVIRONMENT=/local/venv`), uv cache, svpass kernel cache and numba cache (local disk, fast; lost on bux reboot → rerun `uv sync --group research`).
- `code/bench/gpurun [-t S] script.py args` rsyncs `code/noisecirc` → `~/remote/bench/noisecirc` and `code/bench` → `~/remote/bench/bench`, then runs `uv run --frozen --group research python /work/bench/script.py` in the image. To run a noisecirc branch, check it out in `code/noisecirc` first (the working tree is synced).
- Local rsync to the sshfs mount: use `-rlt` (`-a` fails on chgrp).
- Env verified 2026-10-23: 178 noisecirc tests pass on the H100; qiskit-aer-gpu-cu11 0.17.2 sees GPU; cudaq 0.15.1 imports.
