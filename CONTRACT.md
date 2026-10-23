# §C. Guided Research Contract

This contract applies to a project set up with the `guided-wiki` scaffold
profile. It defines project-specific research behavior.
Container capabilities, installed tools, security constraints, and optional
remote resources are documented separately in [`SECDEV.md`](SECDEV.md).

## §C1. Project Scaffold

- MUST read [`SECDEV.md`](SECDEV.md), `CONTRACT.md`, [`PLAN.md`](PLAN.md),
  [`TASKS.md`](TASKS.md), [`PROBLEMS.md`](PROBLEMS.md), [`LOG.md`](LOG.md),
  [`wiki/index.md`](wiki/index.md), [`wiki/overview.md`](wiki/overview.md), and
  [`memory/index.md`](memory/index.md) at session start.
- MUST NOT create the research layout manually if required scaffold files are
  missing; run `scaffold check` and ask before running `scaffold update`.
- `scaffold` is opt-in and refuses to overwrite existing files.

### §C1.1 [`PLAN.md`](PLAN.md)

- Human-owned project contract.
- MUST read at session start.
- MUST NOT modify.
- If edits are requested, tell the human to run `chmod +w PLAN.md`.
- Front matter:
  - `title`: title for the wiki, reports, and summaries.
  - `label`: ASCII slug; use only letters, numbers, dots, underscores,
    hyphens.
  - `mattermost_channel_url`: optional metadata; this guided contract does
    not use Mattermost for reporting.
- The `Tasks` section lists the human-approved research tasks: initial
  directions plus accepted [`TASKS.md`](TASKS.md) proposals, under
  human-assigned IDs.

### §C1.2 [`TASKS.md`](TASKS.md)

- Shared proposal board for new high-level scientific tasks; not a work list.
- MAY propose a task when evidence, literature, or results suggest a direction
  not covered by [`PLAN.md`](PLAN.md). Proposals MUST cite that evidence and
  MUST contain only high-level scientific objectives, not technical
  micro-steps.
- Proposals use stable IDs `T001`, `T002`, ..., never reused and independent of
  [`PLAN.md`](PLAN.md) task IDs, with `State` (`OPEN` or `CLOSED`), `Purpose`,
  and `Outcome` (`pending` while open).
- MUST reply to human comments in the proposal's `Discussion` list, with dated
  entries signed `AI:` or `Human:`.
- MUST NOT work on a proposal, beyond small checks that inform the
  discussion, until the human has copied it into [`PLAN.md`](PLAN.md).
- At session start, MUST close each open proposal the human has copied into
  [`PLAN.md`](PLAN.md): set `State` to `CLOSED` and `Outcome` to
  `accepted into PLAN.md as <PLAN.md task ID>`. If the correspondence is
  unclear, ask in the `Discussion` list instead.
- Rejected, withdrawn, or superseded proposals are closed with the reason.
- MUST NOT delete proposals; closed proposals keep their full text and
  discussion.

### §C1.3 [`PROBLEMS.md`](PROBLEMS.md)

- Shared, human- and agent-readable record of conceptual or structural
  research problems.
- MUST keep unresolved problems under `OPEN` and resolved problems under
  `CLOSED`, with stable IDs and a resolution or closure reason.
- MUST NOT delete closed problems.
- Technical failures, package limitations, and implementation details belong
  in [`LOG.md`](LOG.md), not [`PROBLEMS.md`](PROBLEMS.md).

### §C1.4 [`LOG.md`](LOG.md)

- Terse ledger of the project's history.
- MUST read at session start.
- MUST record every experiment, simulation, investigation, failure, and
  dead end, newest first.
- Each entry gives goal, one-line method, outcome, and next step, names the
  [`PLAN.md`](PLAN.md) task ID of work on an approved task (`--task`), and
  points to `data/`, `code/`, [`memory/`](memory/index.md), and
  [`wiki/`](wiki/index.md) paths (`--ref`).
- Detail belongs in [`memory/`](memory/index.md) and findings in
  [`wiki/`](wiki/index.md); MUST NOT repeat them here.
- SHOULD use `research-log` or `research-run` instead of hand-formatting
  entries.

### §C1.5 Literature

- Papers live in `wiki/literature/`, one file per paper in each subfolder:
  `notes/<citekey>.md`, `pdf/<citekey>.pdf`, and `bib/<citekey>.bib`.
- A paper exists for the project only once `research-lit add DOI --pdf FILE`
  has stored its downloaded PDF and its BibTeX fetched via the DOI. Until then
  MUST NOT cite, link, or rely on it.
- MUST NOT write or edit `.bib` files by hand; regenerate
  `paper/bibliography.bib` with `research-lit bib`.
- A paper counts as read only once its note has a Summary and Relevance in
  the agent's own words; Relevance MUST link the concept and study pages the
  paper informs.
- MUST locate the original source; MUST NOT cite from memory or guess a DOI.
- A paper without DOI needs explicit human approval, recorded in its note as
  `no_doi: approved by human YYYY-MM-DD`.

### §C1.6 [`wiki/`](wiki/index.md)

- Research wiki and the agent-human interface. The agent maintains it; the
  human reads it in Obsidian and MAY edit any page. MUST NOT revert human
  edits.
- Layout: [`overview.md`](wiki/overview.md) (current picture, the human's entry
  point), [`glossary.md`](wiki/glossary.md) (abbreviations and notation),
  `concepts/` (concepts, models, variants, methods), `studies/` (one page per
  line of investigation), `literature/`, and `assets/` (hand-made images only).
- MUST create pages with `research-wiki new` and regenerate
  [`index.md`](wiki/index.md) with `research-wiki index`; MUST NOT edit
  [`index.md`](wiki/index.md) by hand.
- MUST use relative Markdown links and embed figures from `data/<run>/` in
  place instead of copying them.
- MUST write each paragraph, list item, and callout line of a wiki page on
  one line, never hard-wrapped, because Obsidian shows every line break; and
  MUST double-quote front-matter values that contain `: ` or start with a
  YAML indicator such as `#` or `[`. `research-wiki fix` repairs both.
- Every claim MUST link its evidence and carry its status; only tested results
  are presented as results. No raw dumps, code listings, or chatter.
- MUST keep [`overview.md`](wiki/overview.md) current and link every study that
  is not superseded.
- MUST answer each human `> [!question]` callout below it and change it to
  `> [!answer]`.
- MUST keep pages well structured: sections and subsections by topic, short
  paragraphs, lists for enumerations instead of chained sentences, and no
  walls of text dense with inline maths.
- MUST set any equation longer than a short symbol or relation as a display
  equation (`$$…$$`), and number or name it when the text refers to it.
- SHOULD follow the `secdev-explanatory-writing` skill for wiki prose.
- `research-wiki check` MUST pass before returning to the human.

### §C1.7 [`memory/`](memory/index.md)

- The agent's only persistent memory, shared by every agent on the project.
  MUST NOT use built-in agent memory features.
- Written for agents, not humans: working state, labelled hunches, detailed
  failure reasons, and know-how.
- `tasks/<ID>.md` holds the working state of one approved task,
  `topics/<slug>.md` cross-cutting know-how, `archive/` condensed files of
  closed tasks. Create files with `research-wiki new task|topic`.
- MUST read [`memory/index.md`](memory/index.md) and the current task file at
  session start; read topics only as the job needs them.
- MUST update the task file before ending a session or switching tasks.
- When a task closes, MUST condense its file: lasting know-how to `topics/`,
  verified insights to [`wiki/`](wiki/index.md) (linked, not copied), the rest
  to `archive/`.
- MUST NOT hold findings ([`wiki/`](wiki/index.md)) or chronology
  ([`LOG.md`](LOG.md)).

### §C1.8 Folders

- `data/`: store simulation or experimental output; use `research-run` for
  local command runs when practical so outputs and [`LOG.md`](LOG.md) stay
  linked.
- `code/`: store independent codebases or `uv` projects; prefer one
  subfolder per experiment and reference it from [`LOG.md`](LOG.md).
- `paper/`: final-paper workspace; edit only on explicit human request.
  Prose in final papers MUST be human-written, so agents MUST NOT write
  fully formulated paper paragraphs.

## §C2. Session Warmup

- At session start, MUST run `research-warmup`.
- MUST read the files listed in §C1; the helper checks presence, lists open
  human questions in [`wiki/`](wiki/index.md), and summarizes
  `research-wiki check`, but does not replace reading them.
- SHOULD run `research-audit` when starting substantial work or before
  returning final results.

## §C3. Guided Work Loop

For the user-requested job:

1. Read current project state, approved tasks in [`PLAN.md`](PLAN.md), open
   proposals in [`TASKS.md`](TASKS.md), and known problems.
2. Plan the next concrete step.
3. Execute.
4. Evaluate evidence.
5. Record the step in [`LOG.md`](LOG.md), update the task file in
   [`memory/`](memory/index.md), maintain [`PROBLEMS.md`](PROBLEMS.md), propose
   new high-level tasks in [`TASKS.md`](TASKS.md) when the evidence suggests
   them, and, when noteworthy, update [`wiki/`](wiki/index.md).
6. Continue until the requested job is fully achieved or genuinely blocked.
7. Return to the user with the outcome, evidence, and remaining risks.

Loop rules:

- MUST continue after intermediate steps when useful work remains within the
  requested job.
- MUST return to the user after the requested job is complete.
- MUST return to the user when progress requires a decision that cannot be
  derived from [`PLAN.md`](PLAN.md), [`TASKS.md`](TASKS.md),
  [`PROBLEMS.md`](PROBLEMS.md), evidence, or a safe default.
- MUST NOT use Mattermost for progress reporting under this contract.

## §C4. Planning Before Execution

- For any non-trivial task:
  - MUST plan before editing, running simulations, or modifying the wiki.
  - MUST base plan on the approved tasks in [`PLAN.md`](PLAN.md), plus
    [`PROBLEMS.md`](PROBLEMS.md) and [`LOG.md`](LOG.md). Open proposals in
    [`TASKS.md`](TASKS.md) are not work orders.
- Trivial tasks are limited to mechanical inspection or status checks that do
  not change project state.

### §C4.1 Git Discipline

- Unless the user explicitly requests another workflow, SHOULD develop on the
  repository's default branch, normally `master` or `main`, and SHOULD NOT
  create additional branches.
- SHOULD commit autonomously at reasonable, coherent checkpoints with
  explanatory commit messages.
- If undoing committed changes is necessary, SHOULD use `git revert` rather
  than rewriting history.

## §C5. Token Budget

- MUST use `research-warmup` during warmup.
- SHOULD check `usage` before token-heavy steps, after experiments finish,
  and when nearing limits.
- If token budget prevents safe completion, record the state in the
  [`memory/`](memory/index.md) task file and in [`LOG.md`](LOG.md)
  with `research-log` and return to the user with the next concrete action.

## §C6. Completion And Blocking

- A job is complete only when the requested deliverable is produced, checked,
  and documented.
- If blocked, MUST document:
  - what was attempted,
  - the evidence for the block,
  - the smallest user decision or external change needed to continue.
- SHOULD use `research-log --blocked` for blocked work. A blocked approved task
  is recorded in [`LOG.md`](LOG.md) with its task ID; it has no state in
  [`TASKS.md`](TASKS.md).
- MUST NOT treat a failed experiment as a scientific conclusion until the
  implementation has been checked.

## §C7. Integrity

### §C7.1 Never break a promise.

- If you say "I will do X", do it.
- Under-promise and over-deliver.
- If work is deferred, MUST record reason in [`LOG.md`](LOG.md), preferably
  with `research-log`.

### §C7.2 Never manipulate evaluation.

- MUST NOT change metrics, test sets, problem definitions, or fixed
  hyperparameters to make results look better.
- MUST NOT hard-code results.
- MUST NOT cherry-pick seeds.

### §C7.3 Never fabricate citations.

- MUST verify every bibliography entry against the actual source; papers enter
  only through `research-lit add` (§C1.5).
- MUST confirm exact title, full author list, year, venue, and DOI/arXiv or
  other identifier.
- If the paper cannot be found, do not guess.

## §C8. Efficiency

### §C8.1 Make it work before moving on.

- Treat experiment crashes as bugs, not as evidence against the method.
- MUST NOT discard methods because of implementation failures.
- If an experiment crashes, investigate, fix, and rerun when still relevant
  to the requested job.

### §C8.2 Use compute intelligently.

- At session start, SHOULD check local CPU/memory capability.
- IF [`SECDEV.md`](SECDEV.md) documents specialized compute or remote resources
  suitable for the task, SHOULD use them according to that documentation.
- IF starting a local simulation:
  - MUST estimate expected runtime before launch.
  - SHOULD use `research-run` to capture outputs, timeout metadata, and the
    matching [`LOG.md`](LOG.md) entry.
  - MUST use a reasonable timeout when the runtime has not been tested
    before.
  - MUST run without a timeout only after prior tests give a good runtime
    estimate.
  - MUST schedule and perform a status check at that expected runtime.
  - MUST investigate simulations that run much longer than expected.
- Remote jobs that can be actively monitored, such as Slurm jobs, are exempt
  from the local timeout requirement.
- For embarrassingly parallel work, SHOULD use multiple worker processes when
  it materially reduces wall time and MUST leave CPU headroom.

## §C9. Scientific Rigor

### §C9.1 One variable per experiment.

- Change exactly one thing per experiment.
- If two things change and the metric improves, you cannot know which helped.

### §C9.2 Evaluate in tiers.

- Tier 1: seconds, does it run?
- Tier 2: minutes, signal on small subset?
- Tier 3: full evaluation for reportable claims.
- MUST NOT draw conclusions from small-scale bug-catching runs.

### §C9.3 Bound your expectations.

- Before implementing a heuristic, identify theoretical best case and
  estimate maximum possible improvement or correction.

### §C9.4 Never overstate simplified results.

- MUST state caveats for toy models, approximations, restricted parameter
  regimes, finite-size systems, relaxed assumptions, and surrogate metrics.
- Restricted contradiction is evidence, not full disproof.
- Keep caveats visible in [`LOG.md`](LOG.md), plots, user reports, and
  [`wiki/`](wiki/index.md). If the caveat affects a human-selected paper
  result, include it in `paper/` as a terse note or figure/caption constraint.

## §C10. Documentation And Reproducibility

### §C10.1 Record everything.

- MUST log every experiment with goal, method, outcome, and next step,
  preferably with `research-log` or `research-run`.
- MUST include failures.
- MUST document tested, noteworthy results in [`wiki/`](wiki/index.md).
- SHOULD use plots when available.
- MUST use tables only when clearly better than plots for the message.
- MUST keep [`wiki/glossary.md`](wiki/glossary.md) current.
- Dead ends and later-invalidated results are logged in [`LOG.md`](LOG.md),
  with their detail in [`memory/`](memory/index.md).
- If it is not in [`LOG.md`](LOG.md), it did not happen.

### §C10.2 Verify before claiming.

- Assume you are wrong until verified.
- MUST write verification scripts, not just explanations.
- MUST actively try to falsify claims.
- MUST grade claims as verified, partially verified, or unverified.

### §C10.3 Wiki And Paper Roles.

- [`wiki/`](wiki/index.md) is the agent-human interface. Agents MAY write clear
  prose, explanations, caveats, plots, and result summaries there.
- `paper/` is the final-paper workspace. Agents MUST edit it only when the
  human explicitly asks.
- Agents MUST NOT convert [`wiki/`](wiki/index.md) wholesale into `paper/`.
- Normal flow is [`LOG.md`](LOG.md), `data/`, and `code/` to
  [`wiki/`](wiki/index.md), then human-selected content to `paper/`.
- In `paper/`, agents MAY add paper-grade figures, equations, labels,
  bibliography wiring, provenance notes, and keyword-style placeholders.
- In `paper/`, agents MUST NOT write fully formulated prose paragraphs; prose
  may only be inserted when supplied by the human.

### §C10.4 Plot And Figure Quality.

- Figure rules apply to both [`wiki/`](wiki/index.md) and `paper/`. Wiki
  figures are SVG; the paper uses PDF exports of the selected figures.
- Every figure MUST support one clear claim and be referenced from nearby text
  or notes.
- Multi-panel labels such as `(a)`, `(b)`, `(c)` MUST use the same font, size,
  style, and relative position; corresponding labels SHOULD align across
  panels.
- Text inside figures MUST be legible at final rendered size, with consistent
  font sizes for labels, ticks, legends, annotations, and panel labels.
- Labels, legends, annotations, arrows, and panel marks MUST NOT overlap data,
  axes, colorbars, or other informative content.
- Axes and colorbars MUST name quantities and units where applicable.
- Related figures MUST use consistent variable names, colors, markers, line
  styles, limits, and normalization when comparing the same quantities.
- Prefer vector formats for plots when practical; avoid decorative styling.
- Before marking a figure ready, compile or render it and inspect final-size
  output for alignment, readability, overlap, missing labels, and consistency
  with captions or notes.
