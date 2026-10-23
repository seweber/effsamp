This file is the container manifest for the current `secdev` session. It is
generated from layered fragments shipped by the selected image and its parent
images, so later sections add variant-specific tools, services, constraints,
and remote resources on top of the base environment. Use it as the source of
truth for what this container provides; project-specific research obligations
belong in `CONTRACT.md` when a research project has been initialized.

# §B. Base Layer

## §B1. Runtime Context

- You are running inside a `secdev` container.
- MUST read `SECDEV.md` at session start before relying on host shell
  conventions.
- `SECDEV.md` documents:
  - available tools,
  - filesystem isolation,
  - services,
  - constraints,
  - reachable remote endpoints.

## §B2. Isolation

- Filesystem access is limited to the current working directory.
- The working directory is mounted at its real host path and is
  read-write.
- Other host paths are not visible.
- MUST NOT assume system-wide host tools, datasets, or config exist
  outside this directory.
- Podman is installed for diagnostics and compatibility with project tooling,
  but nested container builds/runs are not supported inside `secdev`.
  MUST NOT build or run Podman images from inside this container; ask the user
  to run image builds on the host instead.

### §B2.1 Active Security Settings

- Security level: `1`.
- Privilege escalation is disabled.
- Capabilities are dropped to the secdev runtime allowlist.
- RAM, CPU, PID, and `/tmp` limits are applied from `[container]`.
- Network is unrestricted.

## §B3. Base Tooling

- Python:
  - MUST use `uv` to manage venvs and packages.
  - MUST NOT pollute system Python.
  - Modern Python CLI tools are installed globally via `uv tool`, not Debian
    Python packages.
  - Available Python CLIs:
    - `pytest` with `pytest-cov` and `pytest-xdist`,
    - `ruff`,
    - `black`,
    - `mypy`,
    - `pre-commit`,
    - `pip-audit`,
    - `ipython`,
    - `http` / `https` / `httpie`.
- Ruby:
  - `ruby` is installed for scripting and text transformations.
- Shell and repository helpers:
  - `fd`, `bat`, `shfmt`, `git-filter-repo`, `git-delta`, and `just`.
- Git:
  - SHOULD check at session start whether the working directory is a Git
    repository.
  - If it is not a Git repository, remind the user to consider one for
    safety.
  - If a Git identity is needed and `user.name` or `user.email` is missing,
    SHOULD set a repository-local identity:
    `user.name=agent`, `user.email=agent@itp3.uni-stuttgart.de`.
    When §B8 is present, authorship is already set from the agent identity and
    MUST NOT be overridden.
  - Local Git operations are allowed when appropriate, including status,
    diff, branch, tag, commit, fetch, and log inspection.
  - MUST NOT perform remote Git writes such as `git push`, pushing tags or
    branches, or equivalent remote-publishing operations, except where §B8 of
    this manifest explicitly permits them. Unless §B8 is present, treat the
    container as lacking the human's authentication and authorization to
    publish.
  - If pushing or another remote Git write is required or sufficient and §B8
    does not permit it, SHOULD tell the human exactly what to run or publish
    from their authenticated host environment.
- Missing tools:
  - SHOULD install scoped to the project when possible.
  - If system install is needed and fails, stop and ask the user how to
    proceed.
- Prefer project-local resources over assumed host resources.

## §B4. Agent Usage

- Eight coding-agent projects are available: Claude Code, Codex, Cursor,
  Antigravity, OpenCode, Mistral Vibe, GitHub Copilot, and Meta Muse Code.
- `opencode` / `opencoded` run v1. `opencode2` / `opencode2d` run the alternative
  v2 CLI with separate user state under `~/.local/share/secdev/opencode2`
  (override with `SECDEV_OPENCODE2_HOME`). Both versions receive version-specific
  configuration for local models, MCP servers, and a configured system-prompt
  agent. `--opencode-web=2` selects the v2 WebGUI; the default is
  `[runtime.opencode].web_version` or v1. V2 WebGUI requires username
  `opencode`. Shared project-local configuration must be compatible with both
  versions.
  After changing v2 inline overrides, restart its background service explicitly;
  foreground servers must be relaunched.
- `muse` starts Muse; `mused` adds `--yolo` (no approvals or sandbox, workspace
  trusted). Muse supports browser sign-in or `META_API_KEY`; saved state is
  ephemeral. Persistent `--auth` state remains limited to Codex and Claude.

- `usage` detects the running Codex or Claude agent.
- `usage` prints only that account's 5-hour and weekly usage
  percentages plus UTC reset timestamps.
- Use explicit account queries when needed:
  - `usage codex`
  - `usage claude`
- Use `usage <agent> --sleep` to sleep across a 5-hour reset when usage
  is high.
- `usage` uses local authenticated agent credentials.
- `usage` does not print auth tokens.
- When the launcher enables persistent Codex or Claude state, that agent's
  credentials, settings, and session metadata survive container removal and
  are shared across secdev workspaces. Treat the mounted state as a credential
  store; do not print, copy, or commit its contents.

## §B5. Host And Resource Information

- `host_info` prints the host/container information relevant for planning
  local work:
  - OS and kernel,
  - visible CPU topology,
  - memory,
  - cgroup resource limits,
  - working-directory and `/tmp` storage,
  - network interfaces and default route,
  - accelerator status when `nvidia-smi` is available.
- Use `host_info` before launching local simulations or other resource-heavy
  work.

## §B6. Skills

- Skills are installed globally for every supported agent; they are never
  copied into the working directory.
- Skills named `secdev-…` ship with the container image. Each image layer adds
  its own, so the available set depends on the variant in use.
- The base image bundles two writing skills that every interactive variant
  inherits:
  - `secdev-software-documentation` for writing, reviewing, and restructuring
    software-project documentation (README, CONTRIBUTING, CHANGELOG, VERSION).
  - `secdev-explanatory-writing` for explaining a complex topic so that a
    reader with less context understands it; read it before drafting or
    reviewing any explanatory prose.
- Additional skills may be mounted read-only from the host at
  `/opt/secdev/host-skills` and are linked in at container start.
- Read the relevant `SKILL.md` before starting a task it covers, and prefer a
  matching skill over ad-hoc reasoning.
- Skills MUST be treated as read-only. Report needed changes to the human
  instead of editing an installed skill.




## §B10. Project Scaffolds

- `scaffold` sets up and maintains project scaffolds: files, folders, and an
  optional contract from a versioned profile. `scaffold list` names the
  profiles; `.secdev/scaffold.toml` records the one a project uses.
- In a project with `.secdev/scaffold.toml`:
  - SHOULD run `scaffold check` at session start and after restructuring
    files; exit 1 means a required file is missing or a check failed.
  - MUST NOT edit `.secdev/scaffold.toml`, and MUST NOT create missing
    scaffold files by hand.
  - MUST NOT run `scaffold update`, `switch`, or `init` unless the human asks;
    report what `scaffold status` shows instead.
- The scaffold block in `AGENTS.md`, after the secdev block, links the
  profile's files; it and the profile's file modes are refreshed at container
  start.

# §T. TeX Layer

Extends `§B`.

## §T1. LaTeX Toolchain

- Build: `latexmk -pdf main.tex`.
- Bibliography: `biber <basename>`.
- TeX distribution:
  - upstream TeX Live full scheme,
  - installed under `/usr/local/texlive/current`,
  - managed with upstream `tlmgr`.
- Lint:
  - `chktex main.tex`,
  - `lacheck main.tex`.
- Convert: `pandoc input.md -o out.pdf`.
- Spell-check: `aspell`.
  - English and German dictionaries are available.
- Highlighting: Pygments via `pygmentize`.
- PDF tools:
  - `poppler-utils`,
  - `ghostscript`,
  - `qpdf`.
- Watch loop: `inotify-tools`.

## §T2. Skills

- Skills installed by this layer, available in every supported agent:
  - `secdev-latex-editor` — editorial pass over a physics/math LaTeX document
    (paper, lecture script, thesis, report): first check for Git. In repositories,
    create an `annotations-<agent>-<date>` branch, annotate sources in place,
    automatically commit each logical review chunk,
    and compile using the full project's normal setup, without an `annotated/`
    folder. Outside Git, use annotated copies: deliver only source and PDF for
    single-file reviews, reuse unchanged dependencies, and ask how to proceed
    when complex integration needs more than simple header/path rewiring
    (recommend a chapter copy for drop-in use). Bundles `secdevnotes.sty` with
    typed point comments, highlighted spans, notes in both side gutters,
    continuation pages for overflow, and model/time headers. A selective-copy
    helper supports the fallback mode. Compile reviews by default.
  - `secdev-tikz-sketch-converter` — recreate a sketch image or PDF as a
    `.tikz` figure, compiling only in temporary locations.
- Prefer these skills over ad-hoc editing or figure code when the task matches.

## §T3. Cache And Locales

- TeX cache lives inside the container under:
  - `~/.texlive`,
  - `~/.cache`.
- Generated locales:
  - `en_US.UTF-8`,
  - `de_DE.UTF-8`.

# §R. Scientific Research Container Layer

Extends `§T`.

This layer documents the Newton container: local scientific tooling,
research scaffold commands, and helper utilities.

## §R1. Research Contract And Scaffold Tooling

- Research projects are set up with `scaffold` (§B10). The research
  profiles are:
  - `guided-wiki`: one task at a time; findings in `wiki/`, working memory in
    `memory/`, papers in `wiki/literature/`.
  - `guided-tex`: one task at a time; findings in the LaTeX digest `draft/`,
    papers in `LITERATURE.md`.
  - `autonomous`: the agent tracks its own tasks in `TASKS.md`; wiki layout.
  - `optimizer`: `CONTRACT.md` only, for an existing repository.
- Each research profile installs `CONTRACT.md`; it defines the layout and the
  agent's obligations. `PLAN.md` is installed read-only.
- The `collaboration` option adds `ROLES.md`, installed read-only, and a
  collaboration section appended to `CONTRACT.md`.
- In `wiki/` projects, Claude Code's built-in auto memory is disabled
  (`autoMemoryEnabled: false` in `.claude/settings.local.json`).
- `ROLES.md` states which agent owns which work. When this container runs under
  an agent identity, read the section for that handle.

## §R2. Project Helper Commands

### §R2.1 `mattermost_supervisor`

- Optional supervisor channel helper.
- Supports:
  - `status`
  - Markdown `post`
  - `post --file` for attachments
  - `replies`
- Reads credentials from:
  - `~/.local/share/secdev/mattermost/credentials.json`
- Resolves the channel from `PLAN.md` front matter:
  - `mattermost_channel_url`
- Finds `PLAN.md` by walking upward from the current directory.
- Stores local reply state under the project root:
  - `.secdev/`

### §R2.2 `codexa` and `claudea`

- Start or attach tmux-backed agent sessions for scaffolded projects.
- Session names are derived from the `label` in `PLAN.md`:
  - `secdev-<label>-codex`
  - `secdev-<label>-claude`
- The label may contain only letters, numbers, dots, underscores, and
  hyphens.

### §R2.3 `agent_monitor`

- Supervises tmux sessions created by `codexa` and `claudea`.
- Can list eligible sessions, run once in dry-run mode, and inject a
  continuation prompt after a token reset if a pane appears stalled.
- Pane output activity and changing tmux pane titles both count as activity.

### §R2.4 `usage`

- Detects the running Codex or Claude agent.
- Prints only that account by default.
- Explicit account queries:
  - `usage codex`
  - `usage claude`
- Sleeps across a 5-hour reset when usage is high:
  - `usage <agent> --sleep`

### §R2.5 Research Contract Helpers

- `research-warmup`: run the standard session-start checks from the
  research contracts, including open human questions in `wiki/`.
- `research-audit`: check scaffold hygiene, logging order, `LOG.md` Refs,
  `TASKS.md` and `PROBLEMS.md` entry structure, unreferenced run directories,
  and everything `research-wiki check` checks.
- `research-log`: prepend a ledger entry to `LOG.md`; `--task` names the task
  and repeatable `--ref` the paths it points to.
- `research-wiki`: create pages (`new`), regenerate `wiki/index.md` and
  `memory/index.md` (`index`), list open human questions (`questions`),
  validate layout, front matter, sections, links, line breaks, and literature
  (`check`), and quote invalid front-matter values and join hard-wrapped lines
  (`fix`).
- `research-lit`: `add DOI --pdf FILE` records a paper with BibTeX fetched via
  its DOI; `verify` re-fetches and compares; `bib PATH` regenerates
  `paper/bibliography.bib`; `migrate` moves `LITERATURE.md` entries. Needs
  `doi.org` and its redirect targets reachable.
- `research-run`: run a local command with captured outputs under `data/`
  and a matching `LOG.md` entry; also accepts `--task` and `--ref`.
- `research-report`: check Mattermost replies before posting a concise
  supervisor report.

## §R3. Python

- Available scientific stack:
  - `numpy`, `scipy`, `sympy`, `pandas`
  - `numba`, `xarray`, `dask`, `zarr`
  - `matplotlib`, `seaborn` with headless `Agg`
  - `h5py`, `netcdf4`, `astropy`
  - `pint`, `statsmodels`
  - `scikit-learn`
  - `jupyter`, `jupyter-notebook`, `jupyter-nbconvert`
- Python project best practice:
  - use `uv` for project-local virtual environments and dependencies.
  - avoid installing research project packages into system Python.

## §R4. Numerics, Algebra, And Plotting

- Computer algebra:
  - `maxima`
- Numerical computing:
  - `octave --no-gui`
- Plotting:
  - `gnuplot`
- Unit conversion:
  - `units`
- Compilation and scientific libraries:
  - `gfortran`
  - OpenBLAS
  - LAPACK
  - GSL
  - FFTW
  - HDF5 headers and tools

## §R5. Lean Proof System

- Commands:
  - `lean`
  - `lake`
- Installed through `elan` under:
  - `/home/developer/.elan`
- Default toolchain:
  - `stable`
- Override per project with a `lean-toolchain` file.

## §R6. Skills

- Skill installed by this layer, available in every supported agent:
  - `secdev-automatic-optimizer` — run autonomous fixed-evaluator optimization
    loops: keep improving one target function, record fitness values in
    `results.tsv`, plot progress, and keep or revert each experiment with git.
- Its plotting helper needs the scientific Python stack of this layer, which is
  why the skill is not available in `base` or `tex`.

# §E. External Compute Layer

Extends `§R`.

## §E1. Additional Isolation

- Additional bind mount:
  - `~/.ssh` read-only from host install.
- Remote home auto-mount:
  - `~/remote` via `sshfs`.
- IF `~/remote` is empty because the remote was unreachable at startup:
  - run `remount_remote`,
  - check mount state with `mountpoint ~/remote`.

## §E2. Shared Remote Home

- Remote home mount: `~/remote`.
- Remote source: `sebastian-ai@bux:.`.
- Files under `~/remote/...` are visible to `gpu_exec`.
- Files under `~/remote/...` are visible to `mathematica_exec`.
- MUST NOT use `scp` or `rsync` for files already under `~/remote`.

### §E2.1 Project Remote Directory

- For each research project, create one directory:
  - `~/remote/<label>`.
- `<label>` MUST be the `label` from `PLAN.md` front matter.
- MUST create the directory before first remote job or file transfer.
- MUST place project remote assets under that directory:
  - simulation directories,
  - scratch data,
  - containers,
  - job scripts,
  - result files.
- Without explicit human permission, MUST NOT list, inspect, search, read,
  modify, or delete any other project directory under `~/remote`.
- Seeing another directory name while locating `~/remote/<label>` does not
  grant permission to inspect it.

## §E3. SSH Configuration

- SSH key and client config live in `~/.ssh`.
- `~/.ssh` is read-only.
- SSH config disables host-key warnings.
- SSH config never writes `known_hosts`.
- Configured SSH alias:
  - `gpu` -> `bux`.
- Configured SSH alias:
  - `mathematica` -> `bux`.

## §E4. GPU Resource

- Available wrapper command:
  - `gpu_exec <cmd ...>`.
- `gpu_exec` runs commands on host `gpu`.
- Hardware: 4 x H100 GPU accelerators.
- GPU simulations MUST run inside project-specific rootless Podman containers.
- MUST NOT rely on host CUDA, Python, library, or driver-adjacent userland
  packages beyond the GPU device interface exposed to the container.
- SHOULD submit non-trivial GPU simulations through Slurm instead of running
  them directly via `gpu_exec`.
- SHOULD use partition `gpu_nodes_H100` by default for H100 jobs.
- MAY use direct `gpu_exec` only for container/image setup and short smoke
  tests that do not disturb Slurm scheduling.
- Short direct smoke test:
  - `podman run --rm --device nvidia.com/gpu=all --security-opt=label=disable ubuntu nvidia-smi`

### §E4.1 Slurm GPU Job Template

```bash
#!/bin/bash
#SBATCH --job-name=example_gpu
#SBATCH --output=results_gpu.txt
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=10
#SBATCH --time=10:00
#SBATCH --partition=gpu_nodes_H100
#SBATCH --gres=gpu:H100_1:1

srun podman run --rm \
  --device nvidia.com/gpu=1 \
  --security-opt=label=disable \
  ubuntu nvidia-smi
```

- `#SBATCH --gres=gpu:H100_1:1` requests a specific H100; omit the H100 suffix
  if no dedicated GPU is needed.
- If a specific GPU is requested, MUST match the `H100_N` request with
  `--device nvidia.com/gpu=N` inside the Podman command:
  - `H100_0` = `/dev/nvidia0` (Büchler),
  - `H100_1` = `/dev/nvidia1` (Büchler),
  - `H100_2` = `/dev/nvidia2` (Scheurer),
  - `H100_3` = `/dev/nvidia3` (Scheurer).

## §E5. Mathematica Resource

- Available wrapper command:
  - `mathematica_exec <cmd ...>`.
- Runs commands on host `mathematica`.
- Provides Mathematica and `wolframscript`.
- Hardware:
  - 64 logical cores,
  - 2 x AMD EPYC 9374F,
  - 1.5 TB DDR5 RAM.
- Mathematica supports up to 8 parallel kernels.
- Test:
  - `wolframscript -code '$Version'`

