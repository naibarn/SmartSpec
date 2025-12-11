name: /smartspec_implement_tasks
version: 5.7.2
role: implementation/execution
write_guard: ALLOW-WRITE
purpose: Implement code changes from `tasks.md` (and `spec.md`/`plan.md` when present)
         with SmartSpec v5.6+ centralization, multi-repo and multi-registry
         alignment, KiloCode Orchestrator support, web-stack
         (React/Next.js/RSC/Node/npm) guardrails, and AI/data-sensitivity safety.

---

## 1) Summary

`/smartspec_implement_tasks` drives real code and test changes based on
reviewed `tasks.md`, while enforcing:

- SPEC_INDEX and registry centralization rules;
- multi-repo ownership boundaries;
- reuse-over-duplicate for shared APIs/models/terms/UI components;
- UI JSON governance where applicable;
- KiloCode Orchestrator-per-task execution when enabled;
- **(new, additive)** stricter Kilo behaviour for teams that require
  Orchestrator Mode via `--require-orchestrator`.

It follows after:

1. `/smartspec_generate_spec`
2. `/smartspec_generate_plan`
3. `/smartspec_generate_tasks`
4. `/smartspec_implement_tasks`
5. `/smartspec_sync_spec_tasks` (for alignment)

**v5.6 baseline (retained)**

- KiloCode support via `--kilocode` and per-task Orchestrator loop.
- SPEC_INDEX + registry resolution and precedence.
- multi-repo search via `--workspace-roots` / `--repos-config`.
- UI JSON addendum for Penpot/`ui.json` flows.
- safety gating via `--safety-mode` and `--strict`.
- task-range selection flags and checkbox update rules.

**v5.6.4 (additive hardening)**

- Introduces:
  - explicit sections for Modes, Canonical Folders & File Placement,
    Multi-repo & Multi-registry rules, KiloCode Support (Meta-Flag),
    Inline Detection Rules, Best Practices, and Weakness & Risk Check.
  - web-stack guardrails:
    - integration with `tool-version-registry.json` for
      React/Next.js/RSC/Node/npm;
    - tasks to avoid unsafe downgrades and version drift;
    - focused checks for RSC, SSR/Edge, and `react-server-dom-*`.
  - AI/LLM and data-sensitivity guardrails:
    - no secrets/PII in code, tests, or logs;
    - prompt/logging safety when AI features exist.
  - design-system-aware UI implementation:
    - App-level components, design tokens, and patterns registries.
  - optional implementation reports under `.spec/reports/implement-tasks/`
    with audit metadata.
  - a best-effort secret/PII sanity check before run completion.

**v5.7.2 (additive, Kilo-only stricter option)**

- Adds `--require-orchestrator` flag:
  - lets teams treat `--kilocode` as explicit consent to run under
    Kilo Orchestrator Mode **and** fail fast when Orchestrator is not
    active or not available;
  - behaviour is strictly additive; invocations that do not use
    `--require-orchestrator` retain legacy semantics.

All existing flags and behaviours are preserved; new behaviour is additive.

---

## 2) When to Use

Use `/smartspec_implement_tasks` when:

- `tasks.md` has been generated (and ideally reviewed);
- you are actively implementing or updating a SPEC in this repo;
- you must respect cross-SPEC and cross-repo ownership and registries;
- you need Orchestrator-driven per-task execution under KiloCode;
- you are implementing:
  - React/Next.js/Node/RSC-based services;
  - AI/LLM-driven features;
  - flows touching sensitive or regulated data.

Do **not** use this workflow to:

- generate or edit `tasks.md` itself (use `/smartspec_generate_tasks`);
- author or change registries directly;
- reindex specs or validate the index (use index/registry workflows).

---

## 3) Inputs / Outputs

### 3.1 Inputs (artifacts, read-only)

- Target tasks path (recommended)
  - e.g. `specs/core/spec-core-004-rate-limiting/tasks.md`.

- Adjacent spec artifacts:
  - `spec.md` (required).
  - `plan.md` (optional but recommended).
  - `ui.json` (for UI specs when present).

- Governance context:
  - `.spec/SPEC_INDEX.json` (canonical).
  - `SPEC_INDEX.json` at repo root (legacy mirror).
  - `.smartspec/SPEC_INDEX.json` (deprecated).
  - `specs/SPEC_INDEX.json` (older layout).
  - primary registry: `.spec/registry/` (or `--registry-dir`).
  - supplemental registries: from `--registry-roots` (read-only).
  - `tool-version-registry.json` (when present) for tools/frameworks.

- Multi-repo context (read-only):
  - `--workspace-roots` and/or `--repos-config`.

### 3.2 Inputs (flags)

- See **Section 5 (Flags)**.

### 3.3 Outputs

- Code changes in the current repository:
  - implementation code;
  - tests (unit/integration/contract/performance) where applicable;
  - non-destructive config changes (e.g. CI, dependency files) aligned
    with registries and safety rules.

- Updated `tasks.md`:
  - checkboxes and implementation notes updated according to rules.

- Optional implementation report:
  - default path under `.spec/reports/implement-tasks/`;
  - includes audit metadata, scope, and summarized risks.

No registries are modified directly; registry changes, if needed,
must be expressed as separate governance tasks or recommendations.

---

## 4) Modes

### 4.1 Role & write guard

- Role: **implementation/execution**.
- Write guard: **ALLOW-WRITE**, constrained to:
  - code, tests, and configuration files inside the **current repo**;
  - `tasks.md` in spec folders (checkboxes / notes only);
  - `.spec/reports/implement-tasks/` (or `--report-dir`).
- Must **never**:
  - write into sibling repos discovered via `--workspace-roots` or
    `--repos-config`;
  - write into `.spec/registry/` (only read for validation);
  - modify SPEC_INDEX.

### 4.2 Safety mode

Supported flags:

- `--safety-mode=<strict|dev>`
  - preferred in v5.6 chain.
- `--strict`
  - alias for `--safety-mode=strict`.

Semantics:

- `strict` (default)
  - for production or shared branches;
  - stop or downgrade changes when:
    - new shared names would conflict with registries;
    - SPEC_INDEX or key registries are missing or clearly stale;
    - required web-stack baselines are violated.
  - may require `--validate-only` mode first to assess readiness.

- `dev`
  - for local or early work;
  - allows implementation with warnings and TODOs when governance
    artifacts are incomplete;
  - must clearly report gaps and recommend follow-up governance work.

### 4.3 Preview & validation modes

- `--validate-only`
  - perform all checks and planning but do **not** write code or update
    `tasks.md` (read-only dry run).

- `--dry-run` (new, additive)
  - alias of `--validate-only` for consistency with other workflows.

### 4.4 Architect mode

- `--architect`
  - emphasize system/architectural reasoning before code changes;
  - under KiloCode, Orchestrator may still chain Architect → Code.

### 4.5 KiloCode mode

- `--kilocode`
  - when running under Kilo:
    - Orchestrator coordinates per-task execution when Orchestrator
      Mode is active;
    - subtasks and checkpoints are handled per top-level task;
    - this workflow acts as the implementation engine inside that loop.
  - when Orchestrator Mode is not active, behaviour depends on
    `--require-orchestrator` and `--safety-mode`:
    - without `--require-orchestrator`, the workflow MAY degrade to a
      linear flow, logging a clear note that Orchestrator is not active;
    - with `--require-orchestrator`, see Section 18 (KiloCode Support).

- `--require-orchestrator` (**new, additive, Kilo-only**)
  - only meaningful when `--kilocode` is present.
  - treats `--kilocode` as **explicit consent** to run under Kilo
    Orchestrator Mode and to fail fast when Orchestrator is not
    available.
  - when running inside Kilo, the workflow MUST verify that
    Orchestrator Mode is active **before** starting implementation
    when this flag is set.
  - if the environment does **not explicitly report** that Orchestrator
    Mode is active (for example, no `env.orchestrator_active = true`
    or equivalent signal is present), this workflow MUST treat
    Orchestrator as **not active** and apply the rules below.
  - if Orchestrator Mode is not active or cannot be enabled by the IDE:
    - in `strict` safety mode: the workflow MUST stop early with a
      clear error message explaining that Orchestrator is required but
      not available;
    - in `dev` safety mode: the workflow MAY either fail fast with the
      same error or continue with degraded non-Orchestrator behaviour,
      but MUST emit a prominent warning.

- If `--kilocode` is passed without a Kilo environment:
  - treat as a no-op meta-flag, logging a note in the report.

---

## 5) Flags

> **Non-removal guarantee:** All legacy flags from v5.2/v5.6 remain and
> keep their meanings; new flags are additive only.

### 5.1 Index / Registry

- `--index=<path>`
  - explicit SPEC_INDEX path override.

- `--specindex=<path>`
  - legacy alias for `--index`.

- `--registry-dir=<path>`
  - primary registry directory (default `.spec/registry`).

- `--registry-roots=<dir1,dir2,...>`
  - supplemental registry directories (read-only validation sources).

### 5.2 Multi-Repo

- `--workspace-roots=<root1,root2,...>`
  - additional repo roots for cross-repo spec discovery.

- `--repos-config=<path>`
  - JSON mapping of repo IDs to file-system roots.
  - preferred over `--workspace-roots`, typical path:
    `.spec/smartspec.repos.json`.

### 5.3 Target selection & scope

- `--spec=<path>`
  - explicit spec path.

- `--tasks=<path>`
  - explicit tasks path.

#### 5.3.1 Task subset selection (backward compatible)

- `--task=<n>`
  - implement a single task by index.

- `--tasks=<csv>`
  - implement multiple tasks (by index).

- `--range=<a-b>`
  - implement a contiguous task range.

- `--from=<n>`
  - implement starting at the given index to the end.

- `--start-from=<Tnnn>`
  - legacy task-ID alias for `--from`.

#### 5.3.2 Completion mode

- `--skip-completed`
  - skip checked tasks (default).

- `--force-all`
  - ignore checkboxes and re-implement all tasks in scope.

#### 5.3.3 Resume

- `--resume`
  - resume from the last safe checkpoint (if supported by integrations).

### 5.4 Phase filtering

If `tasks.md` is phase-tagged:

- `--phase=<n>`
- `--phases=<csv>`
- `--phase-range=<a-b>`

These limit the implementation scope to specific phases.

### 5.5 Focus

- `--focus=<api|model|ui|tests|migration|observability|security>`
  - bias implementation toward a particular concern while still
    respecting dependencies.

### 5.6 Safety / preview

- `--safety-mode=<strict|dev>`
- `--strict`
- `--validate-only`
- `--dry-run` (alias for `--validate-only`)

### 5.7 Kilo / Orchestrator

- `--kilocode`
  - enable KiloCode semantics where running under Kilo.

- `--require-orchestrator` (new, additive)
  - only meaningful when `--kilocode` is present.
  - treats `--kilocode` as **explicit consent** to run under
    Kilo Orchestrator Mode.
  - when running inside Kilo, the workflow MUST verify that
    Orchestrator Mode is active **before** starting implementation.
  - if the environment does **not explicitly report** that Orchestrator
    Mode is active, the workflow MUST treat Orchestrator as **not
    active** and apply the Section 18 rules for `--require-orchestrator`.
  - if Orchestrator Mode is not active or cannot be enabled by the IDE,
    the workflow MUST:
    - in `strict` safety mode: fail fast with a clear error message
      explaining that Orchestrator is required but not available;
    - in `dev` safety mode: it MAY either fail fast or continue with
      degraded non-Orchestrator behaviour, but MUST emit a prominent
      warning.

### 5.8 Reporting & summary (additive)

- `--report-dir=<path>`
  - override default `.spec/reports/implement-tasks/`.

- `--stdout-summary`
  - print concise per-run summary to stdout (in addition to any
    report file).

---

## 6) Canonical Folders & File Placement

- Workflow file: `.smartspec/workflows/smartspec_implement_tasks.md`.
- Manuals: `.smartspec-docs/workflows/smartspec_implement_tasks/`.
- Reports: `.spec/reports/implement-tasks/` (default, or `--report-dir`).
- Per-spec artifacts: `specs/<category>/<spec-id>/spec.md|plan.md|tasks.md`.

This workflow must never attempt to write into `.smartspec/` or
`.smartspec-docs/`.

---

## 7) Multi-repo & Multi-registry Rules

- Use `--workspace-roots` / `--repos-config` to locate related repos.
- Treat `.spec/registry/` (or `--registry-dir`) as canonical registry.
- Supplemental registries from `--registry-roots` are read-only.
- Never write into sibling repos; only scan them for context.
- Prefer reuse of registry entries over new, duplicate definitions.

---

## 8) UI Governance Addendum

- Respect design-system registries (design tokens, UI components,
  patterns) when present.
- Prefer App-level components over raw UI library components for
  critical flows.
- `ui.json` may be present for JSON-first flows; business logic must
  not live in `ui.json`.

---

## 9) Web-stack & AI/Data Guardrails

- For React/Next/RSC/Node/npm:
  - align changes with `tool-version-registry.json`;
  - avoid unsafe version downgrades or fragmentation;
  - be careful with RSC/SSR/Edge boundaries and `react-server-dom-*`.

- For AI/LLM features:
  - treat models as untrusted; defend against prompt-injection;
  - avoid secrets/PII in prompts, logs, and tests.

- For sensitive/regulated data:
  - assume external tools (DLP, secret scanners, SCA) complement this
    workflow; make these dependencies explicit where relevant.

---

## 16) Weakness & Risk Check (Quality Gate)

Before treating this spec as stable, verify:

1. **Write safety**
   - `--validate-only` / `--dry-run` prevent all writes.
   - no writes to sibling repos or registries.

2. **Index & registry correctness**
   - SPEC_INDEX detection order is followed.
   - primary vs supplemental registries are respected.
   - shared entities are reused, not duplicated.

3. **Multi-repo safety**
   - sibling repos are read-only.
   - external owners are modeled as reuse, not duplicate implementations.

4. **UI governance**
   - business logic is not pushed into `ui.json`.
   - design-system and App-level component rules are followed.

5. **Safety-mode behaviour**
   - strict/dev behaviour matches expectations.
   - conflicts and missing context are surfaced as warnings or blocks.

6. **Web-stack guardrails**
   - React/Next/RSC/Node/npm changes respect baselines.
   - no unsafe downgrades or version fragmentation are introduced.

7. **AI & data-sensitivity**
   - prompts/logs/tests do not carry secrets/PII.
   - data classification/masking tasks are present where needed.

8. **KiloCode support**
   - `--kilocode` behaviour and Orchestrator-per-task loop are honoured.
   - where `--require-orchestrator` is used, failure conditions are
     clearly reported and non-Orchestrator runs are not silently
     allowed in strict mode.

9. **Secret/PII propagation**
   - best-effort checks are in place.
   - expectation of external scanning in CI is documented.

---

## 17) Legacy Flags Inventory

- **Kept (legacy):**
  - `--index`
  - `--specindex`
  - `--registry-dir`
  - `--registry-roots`
  - `--workspace-roots`
  - `--repos-config`
  - `--spec`
  - `--tasks`
  - `--task`
  - `--tasks=<csv>`
  - `--range`
  - `--from`
  - `--start-from`
  - `--skip-completed`
  - `--force-all`
  - `--resume`
  - `--phase`
  - `--phases`
  - `--phase-range`
  - `--focus`
  - `--safety-mode`
  - `--strict`
  - `--validate-only`
  - `--architect`
  - `--kilocode`

- **New additive (v5.6.4+ and later):**
  - `--dry-run` (alias for `--validate-only`)
  - `--report-dir`
  - `--stdout-summary`
  - `--require-orchestrator` (Kilo-only stricter behaviour)

No legacy flag is removed or weakened.

---

## 18) KiloCode Support (Meta-Flag)

When `--kilocode` is present and Kilo is detected:

- role: Ask/Architect + Code implementation.
- Orchestrator-per-task rule:
  - for each top-level task in `tasks.md`:
    1. Orchestrator selects the task (and any subtasks).
    2. Orchestrator confirms index/registry/ownership boundaries.
    3. Code mode implements the required changes and tests.
    4. Orchestrator validates completion and moves to the next task.
- subtasks are expected to be ON where task numbering supports it.
- `--kilocode` is treated as **explicit consent** for the IDE to
  enable Orchestrator Mode if it chooses to do so.

When both `--kilocode` and `--require-orchestrator` are present and
Kilo Orchestrator Mode is **not explicitly reported as active by the
environment**:

- the workflow MUST assume Orchestrator is **not active** (missing,
  false, or unknown signals are treated as "not active").
- in `strict` safety mode, this workflow MUST stop early with a
  configuration error such as:

  > "Kilo Orchestrator Mode is required (`--require-orchestrator`) but
  > is not active. Please enable Orchestrator Mode in Kilo UI and rerun
  > this workflow."

- in `dev` safety mode, the workflow MAY either stop with the same
  error or continue in degraded, non-Orchestrator mode, but MUST emit
  a prominent warning and clearly label the run as non-Orchestrator.

When Orchestrator is unavailable and `--require-orchestrator` is **not**
set:

- in `strict` safety mode, this workflow SHOULD prefer
  `--validate-only` and emit a clear infra/config error;
- in `dev` safety mode, it may degrade to a linear flow with a warning
  in the report/summary explaining that Orchestrator was not active.

### 18.1 Failure handling under KiloCode

When running under Kilo with `--kilocode`, this workflow must treat
single tool/edit failures (for example Kilo messages such as
"Edit Unsuccessful" / "Kilo Code is having trouble…") as
**recoverable** events, not automatic hard stops.

If an edit attempt fails while `--kilocode` is active:

1. **Narrow the scope instead of stopping**
   - prefer retrying with:
     - fewer tasks in scope (e.g. a smaller `--tasks` range or a single
       `Txxx`), and/or
     - a smaller file/line range for the same task.
   - surface a short note in the per-run summary/report explaining why
     the larger edit failed (too large, ambiguous, conflicting context).

2. **Ask for user/Orchestrator guidance**
   - explicitly suggest 1–3 next-step options, such as:
     - "split this route into two tasks (read vs write)",
     - "run again with `--tasks=T003` only",
     - "run once with `--validate-only` to review the planned changes
        before editing".

3. **Prefer Orchestrator-per-task over giant edits**
   - when multiple tasks are in scope, keep the Orchestrator loop
     per top-level task rather than attempting a single monolithic edit
     across many files.
   - allow the Orchestrator to re-plan smaller edits after failures,
     while preserving ownership and registry rules.

Only treat repeated failures on a **narrow, well-specified scope** as a
hard stop condition, and report these clearly (including which task and
file/line range failed).

When Kilo is not detected, `--kilocode` is a no-op meta-flag.

---

## 19) Inline Detection Rules

This workflow must **not** call other SmartSpec workflows
programmatically. It may:

- detect Kilo/ClaudeCode/Antigravity environments from context;
- inspect flags such as `--kilocode` and `--require-orchestrator`;
- detect web-stack usage by scanning:
  - specs, plans, tasks, and key files for React/Next/Node/RSC,
    `react-server-dom-*`, SSR/Edge hints;
- detect AI/LLM features and data-sensitivity from spec/plan/tasks.

It may **recommend** follow-up workflows (by name) in summaries or
reports (e.g. `/smartspec_sync_spec_tasks`, `/smartspec_release_readiness`,
`/smartspec_ui_validation`, `/smartspec_ui_consistency_audit`)
but must not invoke them itself.

---

## 20) Best Practices

- For CI/prod-bound implementation, use `--safety-mode=strict` and
  prefer `--validate-only` on the first run in a repo.
- Keep `.spec/SPEC_INDEX.json` and `.spec/registry/` up to date; if they
  lag reality, add tasks to repair them before large-scale changes.
- In multi-repo setups, maintain a single `--repos-config` under `.spec/`
  and avoid redefining shared entities across repos.
- Decide early per spec how UI is governed (JSON-first vs inline) and
  align implementation with that choice.
- Treat `tasks.md` as an execution contract but remember that `spec.md`
  remains the source-of-truth for requirements.
- For web stacks (React/Next.js/RSC/Node/npm):
  - always align dependency changes with `tool-version-registry.json`;
  - ensure RSC/SSR/Edge guardrail tasks are present and implemented.
- For AI/LLM features:
  - treat the model as untrusted; design for prompt-injection resistance;
  - avoid including real user data, secrets, or PII in code examples,
    prompts, or tests.
- For sensitive/regulated data:
  - assume external tools (DLP, secret scanners, SCA) complement this
    workflow; make these dependencies explicit in tasks and CI.

---

## 21) For the LLM / Step-by-step Flow & Stop Conditions

### 21.1 Step-by-step flow

1. Parse all flags and environment, resolving safety-mode, target
   spec/tasks, index, registries, and multi-repo roots.

1.a Under Kilo with `--kilocode` and `--require-orchestrator`:
    - verify that Kilo Orchestrator Mode is active **before**
      proceeding;
    - check the environment for an explicit signal that Orchestrator
      is active (for example `env.orchestrator_active = true` or an
      equivalent integration flag);
    - if such a signal is **missing, false, or unknown**, the workflow
      MUST treat Orchestrator as **not active** and apply the
      failure/warning rules from Section 18 (KiloCode Support);
    - in `strict` mode, the run MUST stop early when Orchestrator is
      treated as not active.

2. Resolve SPEC_INDEX and registry directories using canonical order.
3. Detect presence/absence of `tool-version-registry.json` and
   design-system registries.
4. Locate `spec.md`, `tasks.md`, `plan.md` (optional), and `ui.json`
   (if any) for the target spec.
5. Read spec/tasks/plan and classify dependencies and shared entities
   using registries and SPEC_INDEX.
6. Detect web-stack, AI/LLM features, and data-sensitivity markers.
7. Run the pre-implementation consistency gate; in `strict`, either
   continue safely, downgrade to `--validate-only`, or block.
8. Determine execution scope based on task selection flags, phases, and
   focus.
9. Under KiloCode, follow the Orchestrator-per-task loop; otherwise,
   run in a linear task order respecting dependencies.
10. For each task/subtask in scope:
    - apply ownership and registry rules;
    - implement or adjust code and tests in the current repo only;
    - obey UI JSON/design-system rules when relevant;
    - obey web-stack and AI/data-sensitivity guardrails.
11. Update `tasks.md` checkboxes and notes according to checkbox rules.
12. Perform a best-effort scan to avoid writing secrets/PII/raw logs
    into code, tests, or `tasks.md`.
13. Generate a final summary and, if configured, write a report under
    `.spec/reports/implement-tasks/`.
14. If `--stdout-summary` is set, print a concise summary including
    safety-mode and key warnings.
15. Under KiloCode (when `--kilocode` is present):
    - if a tool/edit attempt fails mid-run (for example Kilo reports
      "Edit Unsuccessful" or similar), do **not** end the workflow
      immediately;
    - instead, follow the failure-handling rules in Section 18.1:
      - narrow the scope (fewer tasks, smaller file ranges),
      - surface a short explanation of the failure,
      - and propose concrete next steps or task splits for the user or
        Orchestrator.

### 21.2 Stop conditions

The workflow must stop after:

- applying code and test changes in the **current repo only** (or none
  in `--validate-only`/`--dry-run`);
- updating `tasks.md` and reports (if applicable);
- emitting final summary/summary+report.

It must **never**:

- write into sibling repos;
- update SPEC_INDEX or registries directly;
- invoke other SmartSpec workflows programmatically.

