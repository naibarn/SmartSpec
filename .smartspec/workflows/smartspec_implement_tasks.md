name: /smartspec_implement_tasks
version: 5.8.0
role: implementation/execution
write_guard: ALLOW-WRITE
purpose: Implement code changes from `tasks.md` (and `spec.md`/`plan.md` when present)
         with SmartSpec v5.6+ centralization, multi-repo and multi-registry
         alignment, KiloCode Orchestrator support, web-stack
         (React/Next.js/RSC/Node/npm) guardrails, AI/data-sensitivity safety,
         and strict, non-removable governance for tasks, Kilo sub-tasks,
         and Orchestrator recovery.

---

## 0) Non-Removable Invariants (DO NOT DELETE OR WEAKEN)

> These invariants encode legacy SmartSpec + Kilo behaviour. They MUST NOT
> be removed, renamed, or weakened without an explicit governance KB change
> and a major version bump for this workflow.

### 0.1 Tasks-First Invariant

1. Implementation MUST ALWAYS be driven by `tasks.md`.
   - No code change may be performed that is not traceable to an explicit
     task entry in `tasks.md`.
   - This applies across all environments (CLI, Kilo Code, Claude Code,
     Google Antigravity).
2. This workflow MUST NOT run if:
   - `tasks.md` is missing;
   - `tasks.md` cannot be parsed; or
   - task selection flags resolve to an empty set.
   It MUST instead fail fast with a clear governance error.
3. `tasks.md` is the canonical mechanism for scoping work. This workflow
   MUST NOT:
   - infer new tasks implicitly from diffs or code structure;
   - silently expand scope beyond the selected tasks;
   - modify task numbering or structure (only checkboxes/notes are allowed).

### 0.2 Kilo Orchestrator Sub-Task Invariant (Legacy Rule — DO NOT REMOVE)

When running under Kilo with `--kilocode`:

1. Kilo MUST NOT execute this workflow as a single root job over many tasks
   without sub-task decomposition.
2. Before any implementation begins, Kilo MUST:
   - enable Orchestrator Mode; and
   - create an appropriate set of Kilo sub-tasks that map to the selected
     SmartSpec tasks (typically one sub-task per top-level task, or per
     small batch).
3. This workflow MUST assume that it is running inside a Kilo sub-task
   whenever `--kilocode` is set and Orchestrator is active.
4. If this workflow detects that it is running with `--kilocode` but not
   inside a sub-task context (for example, required Kilo sub-task metadata
   is missing), it MUST:
   - in `strict` safety mode: fail fast with a governance error and
     instruct the user/Orchestrator to enable sub-task decomposition;
   - in `dev` safety mode: it MAY either fail fast or run in degraded
     non-Orchestrator mode, but MUST emit a prominent warning and label the
     run as non-compliant with Kilo sub-task governance.
5. Orchestrator must treat sub-task creation as mandatory for complex
   implementations. The legacy rule is explicitly preserved:

   > When switching to Orchestrator Mode under Kilo, you MUST `new subtasks`
   > before implementing tasks.

### 0.3 Non-Stop Workflow Invariant

To prevent premature stops and half-finished work:

1. Completion of a single task or edit attempt MUST NOT be treated as a
   reason to end the entire workflow if there are remaining selected tasks.
2. When running under `--kilocode`, any single Kilo edit failure (for
   example "Edit Unsuccessful" or similar) MUST be treated as a recoverable
   event:
   - narrow scope (fewer tasks, smaller file ranges);
   - retry where appropriate; and
   - surface clear next-step options.
3. The workflow MAY stop early only when:
   - a hard governance violation occurs (for example missing SPEC_INDEX,
     registry corruption, forbidden write target);
   - Orchestrator requirement is not satisfied while `--require-orchestrator`
     is present; or
   - the user/Orchestrator explicitly cancels.
4. Under Kilo, finishing a sub-task MUST:
   - return a clear per-task report;
   - hand control back to Orchestrator so it can decide the next sub-task;
   - not terminate the entire project run unless Orchestrator decides so.

### 0.4 Orchestrator Recovery Invariant (Legacy Rule — DO NOT REMOVE)

This invariant encodes the legacy rule that implementation runs must not
"die quietly" under Kilo Orchestrator:

1. When running with `--kilocode` and Orchestrator is active, if an
   implementation attempt:
   - stalls or makes no forward progress;
   - fails repeatedly with non-fatal edit errors; or
   - encounters partial completion where some, but not all, selected
     tasks are done;
   then this workflow MUST hand control back to Orchestrator Mode to
   re-plan and continue, rather than terminating silently.
2. The correct behaviour is:
   - detect the stalled/partial state;
   - summarise what has been completed and what remains;
   - explicitly request Orchestrator to re-enter planning for the
     remaining work (narrowing scope if needed);
   - return a structured report so Orchestrator can:
     - update its task/sub-task view; and
     - decide whether to retry, split tasks further, or escalate.
3. This workflow MUST NOT treat a non-fatal implementation issue as a
   terminal success state. If progress cannot be made within the current
   sub-task, it MUST:
   - surface a clear governance/completion status back to Orchestrator; and
   - allow Orchestrator to resume control and plan the next steps.
4. Under Kilo, a valid stop condition is either:
   - Orchestrator explicitly decides the project is complete or cancelled; or
   - a hard governance violation (see 0.3) that prevents any safe
     continuation.

The historical rule can be restated as:

> If an implementation run cannot continue under Kilo, you MUST switch back
> into Orchestrator Mode, re-plan, and then continue — you must not simply
> stop and leave tasks half-finished.

These invariants are part of the SmartSpec core governance for this
workflow. Teams may extend them but MUST NOT delete or contradict them.

---

## 1) Summary

`/smartspec_implement_tasks` drives real code and test changes based on
reviewed `tasks.md`, while enforcing:

- SPEC_INDEX and registry centralization rules;
- multi-repo ownership boundaries;
- reuse-over-duplicate for shared APIs/models/terms/UI components;
- UI JSON governance where applicable;
- KiloCode Orchestrator-per-task execution when enabled;
- strict tasks-first execution and Kilo sub-task governance (Section 0);
- stricter Kilo behaviour for teams that require Orchestrator Mode via
  `--require-orchestrator`.

It follows after:

1. `/smartspec_generate_spec`
2. `/smartspec_generate_plan`
3. `/smartspec_generate_tasks`
4. `/smartspec_implement_tasks`
5. `/smartspec_sync_spec_tasks` (for alignment)

v5.6 baseline (retained):

- KiloCode support via `--kilocode` and per-task Orchestrator loop.
- SPEC_INDEX + registry resolution and precedence.
- multi-repo search via `--workspace-roots` / `--repos-config`.
- UI JSON addendum for Penpot/`ui.json` flows.
- safety gating via `--safety-mode` and `--strict`.
- task-range selection flags and checkbox update rules.

v5.6.4 (additive hardening):

- Introduces:
  - explicit sections for Modes, Canonical Folders & File Placement,
    Multi-repo & Multi-registry rules, KiloCode Support (Meta-Flag),
    Inline Detection Rules, Best Practices, and Weakness & Risk Check.
  - web-stack guardrails:
    - integration with `tool-version-registry.json` for React/Next.js/
      RSC/Node/npm;
    - tasks to avoid unsafe downgrades and version drift;
    - focused checks for RSC, SSR/Edge, and `react-server-dom-*`.
  - AI/LLM and data-sensitivity guardrails:
    - no secrets/PII in code, tests, or logs;
    - prompt/logging safety when AI features exist.
  - design-system-aware UI implementation:
    - App-level components, design tokens, and patterns registries.
  - optional implementation reports under
    `.spec/reports/implement-tasks/` with audit metadata.
  - a best-effort secret/PII sanity check before run completion.

v5.7.2 (additive, Kilo-only stricter option):

- Adds `--require-orchestrator` flag:
  - lets teams treat `--kilocode` as explicit consent to run under
    Kilo Orchestrator Mode and fail fast when Orchestrator is not active
    or not available;
  - behaviour is strictly additive; invocations that do not use
    `--require-orchestrator` retain legacy semantics.

v5.8.0 (additive, tasks + Kilo governance hardening):

- Adds Section 0 invariants:
  - tasks-first execution;
  - mandatory Kilo sub-tasks under Orchestrator;
  - non-stop workflow behaviour for recoverable failures;
  - Orchestrator recovery and re-planning.
- Ties Kilo sections (4.5, 5.7, 18, 21) back to invariants.
- No previous flags or sections are removed.

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

Do not use this workflow to:

- generate or edit `tasks.md` itself (use `/smartspec_generate_tasks`);
- author or change registries directly;
- reindex specs or validate the index (use index/registry workflows).

---

## 3) Inputs / Outputs

### 3.1 Inputs (artifacts, read-only)

- Target tasks path (recommended), e.g.
  - `specs/core/spec-core-004-rate-limiting/tasks.md`.

- Adjacent spec artifacts:
  - `spec.md` (required);
  - `plan.md` (optional but recommended);
  - `ui.json` (for UI specs when present).

- Governance context:
  - `.spec/SPEC_INDEX.json` (canonical);
  - `SPEC_INDEX.json` at repo root (legacy mirror);
  - `.smartspec/SPEC_INDEX.json` (deprecated);
  - `specs/SPEC_INDEX.json` (older layout);
  - primary registry: `.spec/registry/` (or `--registry-dir`);
  - supplemental registries: from `--registry-roots` (read-only);
  - `tool-version-registry.json` (when present) for tools/frameworks.

- Multi-repo context (read-only):
  - `--workspace-roots` and/or `--repos-config`.

### 3.2 Inputs (flags)

- See Section 5 (Flags).

### 3.3 Outputs

- Code changes in the current repository only:
  - implementation code;
  - tests (unit/integration/contract/performance) where applicable;
  - non-destructive config changes (e.g. CI, dependency files) aligned
    with registries and safety rules.

- Updated `tasks.md`:
  - checkboxes and implementation notes updated according to rules.

- Optional implementation report:
  - default path under `.spec/reports/implement-tasks/`;
  - includes audit metadata, scope, and summarized risks.

No registries are modified directly; registry changes, if needed, must be
expressed as separate governance tasks or recommendations.

---

## 4) Modes

### 4.1 Role & write guard

- Role: implementation/execution.
- Write guard: ALLOW-WRITE, constrained to:
  - code, tests, and configuration files inside the current repo;
  - `tasks.md` in spec folders (checkboxes / notes only);
  - `.spec/reports/implement-tasks/` (or `--report-dir`).
- Must never:
  - write into sibling repos discovered via `--workspace-roots` or
    `--repos-config`;
  - write into `.spec/registry/` (only read for validation);
  - modify SPEC_INDEX.

### 4.2 Safety mode

Supported flags:

- `--safety-mode=<strict|dev>` (preferred);
- `--strict` (alias for `--safety-mode=strict`).

Semantics:

- `strict` (default):
  - for production or shared branches;
  - stop or downgrade changes when:
    - new shared names would conflict with registries;
    - SPEC_INDEX or key registries are missing or clearly stale;
    - required web-stack baselines are violated;
  - may require `--validate-only` first to assess readiness.

- `dev`:
  - for local or early work;
  - allows implementation with warnings and TODOs when governance
    artifacts are incomplete;
  - must clearly report gaps and recommend follow-up governance work.

### 4.3 Preview & validation modes

- `--validate-only`:
  - perform all checks and planning but do not write code or update
    `tasks.md` (read-only dry run).

- `--dry-run`:
  - alias for `--validate-only`.

### 4.4 Architect / planning mode

- This workflow is primarily implementation-focused but must:
  - respect planning decisions already encoded in `plan.md` and `tasks.md`;
  - avoid rewriting high-level plans; instead, surface gaps as tasks.

### 4.5 KiloCode mode (updated)

When `--kilocode` is present and Kilo is detected:

- Role: Ask/Architect + Code implementation.
- Orchestrator-per-task rule:
  - for each top-level task in `tasks.md`:
    1. Orchestrator selects the task (and any subtasks);
    2. Orchestrator confirms index/registry/ownership boundaries;
    3. Code mode implements the required changes and tests;
    4. Orchestrator validates completion and moves to the next task.
- Sub-task requirement (legacy invariant, Section 0.2):
  - when Orchestrator Mode is active, this workflow MUST assume it is
    running inside a Kilo sub-task;
  - running as a single root job over many tasks without sub-task
    decomposition is considered non-compliant in `strict` mode;
  - if `--kilocode` is set but sub-task context is clearly missing, the
    workflow MUST:
    - in `strict` mode: fail fast with a governance error and instruct
      Kilo to new subtasks before rerun;
    - in `dev` mode: MAY continue in degraded linear mode but MUST emit a
      prominent warning.
- If `--kilocode` is passed without a Kilo environment:
  - treat as a no-op meta-flag, logging a note in the report.

---

## 5) Flags

### 5.1 Spec & tasks selection

- `--spec-path=<path>`
- `--tasks-path=<path>`
- `--spec-id=<id>`

(Use existing semantics from v5.7.2: resolve SPEC, plan, tasks from
canonical locations and SPEC_INDEX.)

### 5.2 Task selection

- `--task=<n>`
  - implement a single task by index.

- `--tasks=<csv>`
  - implement multiple tasks by index.

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
  - bias implementation toward a particular concern while still respecting
    dependencies.

### 5.6 Safety / preview

- `--safety-mode=<strict|dev>`
- `--strict`
- `--validate-only`
- `--dry-run` (alias for `--validate-only`).

### 5.7 Kilo / Orchestrator

- `--kilocode`:
  - enable KiloCode semantics where running under Kilo;
  - MUST obey Section 0.2 Kilo Orchestrator Sub-Task Invariant.

- `--require-orchestrator` (additive):
  - only meaningful when `--kilocode` is present;
  - treats `--kilocode` as explicit consent to run under Kilo Orchestrator
    Mode;
  - when running inside Kilo, the workflow MUST verify that Orchestrator
    Mode is active before starting implementation;
  - if the environment does not explicitly report that Orchestrator Mode
    is active, the workflow MUST treat Orchestrator as not active and
    apply Section 18 rules for `--require-orchestrator`;
  - if Orchestrator Mode is not active or cannot be enabled by the IDE,
    the workflow MUST:
    - in `strict` safety mode: fail fast with a clear error message;
    - in `dev` safety mode: MAY either fail fast or continue with
      degraded non-Orchestrator behaviour, but MUST emit a prominent
      warning.

### 5.8 Reporting & summary (additive)

- `--report-dir=<path>`
  - override default `.spec/reports/implement-tasks/`.

- `--stdout-summary`
  - print concise per-run summary to stdout (in addition to any report
    file).

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

## 10) Implementation Governance (summary)

(Aligned with core KB; unchanged semantics other than references to
Section 0 invariants.)

---

## 11) Failure Handling Principles

- Do not stop instantly on a single Kilo edit failure;
- Narrow scope;
- Retry with smaller ranges;
- Provide explicit next-step options.

These are strengthened by Section 0.3 and 0.4.

---

## 12) Cross-Workflow Behaviour

- Workflows may reference each other but must not call each other.
- Must guide users to use the correct workflow path.
- Must respect `--validate-only` always.

---

## 13) Best Practices (Selected)

- For implement phase under Kilo, prefer:

  ```
  --kilocode --require-orchestrator --safety-mode=strict
  ```

- Use `--validate-only` before running on a large repo.
- Keep SPEC_INDEX and registry updated.
- Keep tasks small and precise.

---

## 16) Weakness & Risk Check (Quality Gate)

(Based on existing v5.7.2 content; unchanged in spirit.)

1. Write safety
   - `--validate-only` / `--dry-run` prevent all writes.
   - no writes to sibling repos or registries.
2. Index & registry correctness
   - SPEC_INDEX detection order is followed.
   - primary vs supplemental registries are respected.
   - shared entities are reused, not duplicated.

---

## 18) KiloCode Support (Meta-Flag)

Retains existing v5.7.2 semantics and extends them:

- `--kilocode` is a meta-flag signalling Kilo integration.
- `--require-orchestrator` allows teams to treat Orchestrator as required.
- Orchestrator-per-task loop is recommended for multiple tasks.
- Prefer Orchestrator-per-task over giant edits:
  - when multiple tasks are in scope, keep the Orchestrator loop per
    top-level task rather than attempting a single monolithic edit across
    many files;
  - allow the Orchestrator to re-plan smaller edits after failures, while
    preserving ownership and registry rules.
- Only treat repeated failures on a narrow, well-specified scope as a
  hard stop condition, and report these clearly (including which task and
  file/line range failed).
- When Kilo is not detected, `--kilocode` is a no-op meta-flag.

### 18.1 Orchestrator requirement

- When `--require-orchestrator` is set under Kilo:
  - in `strict` mode, the run must stop early when Orchestrator is treated
    as not active;
  - in `dev` mode, the workflow may continue with warnings.

### 18.2 Orchestrator recovery (ties to Section 0.4)

- When running under Kilo with `--kilocode`, single edit/tool failures
  MUST be treated as recoverable where possible:
  - narrow scope, retry, and surface remaining tasks to Orchestrator;
  - do not treat partial completion as a final success state when selected
    tasks remain.
- If progress cannot be made within the current sub-task:
  - summarise what was done and what remains; and
  - hand control back to Orchestrator so it can re-plan the remaining
    work.
- Stopping with tasks half-finished is only valid when:
  - Orchestrator explicitly cancels or marks the project complete; or
  - a hard governance violation prevents safe continuation.

---

## 19) Inline Detection Rules

- This workflow must not call other SmartSpec workflows programmatically.
- It may detect:
  - Kilo/ClaudeCode/Antigravity environments from context;
  - flags such as `--kilocode` and `--require-orchestrator`;
  - web-stack usage by scanning:
    - specs, plans, tasks, and key files for React/Next/Node/RSC,
      `react-server-dom-*`, SSR/Edge hints;
  - AI/LLM features and data-sensitivity from spec/plan/tasks.
- It may recommend follow-up workflows by name in summaries or reports
  but must not invoke them itself.

---

## 20) Best Practices

- For CI/prod-bound implementation, use `--safety-mode=strict` and prefer
  `--validate-only` on the first run in a repo.
- Keep `.spec/SPEC_INDEX.json` and `.spec/registry/` up to date; if they
  lag reality, add tasks to repair them before large-scale changes.
- In multi-repo setups, maintain a single `--repos-config` under `.spec/`
  and avoid redefining shared entities across repos.
- Decide early per spec how UI is governed (JSON-first vs inline) and
  align implementation with that choice.
- Treat `tasks.md` as an execution contract but remember that `spec.md`
  remains the source of truth for requirements.
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
    - verify that Kilo Orchestrator Mode is active before proceeding;
    - check the environment for an explicit signal that Orchestrator is
      active (for example `env.orchestrator_active = true` or an
      equivalent integration flag);
    - if such a signal is missing, false, or unknown, the workflow must
      treat Orchestrator as not active and apply the failure/warning rules
      from Section 18;
    - in `strict` mode, the run must stop early when Orchestrator is
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
9. Under KiloCode, follow the Orchestrator-per-task loop; otherwise, run
   in a linear task order respecting dependencies.
10. For each task/subtask in scope:
    - apply ownership and registry rules;
    - implement or adjust code and tests in the current repo only;
    - obey UI JSON/design-system rules when relevant;
    - obey web-stack and AI/data-sensitivity guardrails.
11. Update `tasks.md` checkboxes and notes according to checkbox rules.
12. Perform a best-effort scan to avoid writing secrets/PII/raw logs into
    code, tests, or `tasks.md`.
13. Generate a final summary and, if configured, write a report under
    `.spec/reports/implement-tasks/`.
14. If `--stdout-summary` is set, print a concise summary including
    safety-mode and key warnings.
15. Under KiloCode (when `--kilocode` is present):
    - if a tool/edit attempt fails mid-run (for example Kilo reports
      "Edit Unsuccessful" or similar), do not end the workflow
      immediately;
    - instead, follow the failure-handling and recovery rules in
      Sections 0.3, 0.4, and 18.2:
      - narrow the scope (fewer tasks, smaller file ranges);
      - surface a short explanation of the failure;
      - propose concrete next steps or task splits for the user or
        Orchestrator;
      - hand control back to Orchestrator as needed to re-plan.

### 21.2 Stop conditions

The workflow must stop after:

- applying code and test changes in the current repo only (or none in
  `--validate-only` / `--dry-run`);
- updating `tasks.md` and reports (if applicable);
- emitting final summary/summary+report.

It must never:

- write into sibling repos;
- update SPEC_INDEX or registries directly;
- invoke other SmartSpec workflows programmatically.

---

## 22) Governance Notes (Non-Removable)

1. This workflow spec is aligned with core governance KBs and Kilo
   sub-task guidance.
2. Section 0 (Non-Removable Invariants) encodes legacy SmartSpec +
   KiloCode behaviour and MUST NOT be deleted or weakened without updating
   the governance KBs and bumping this workflow's major version.
3. Teams may extend this workflow but must not remove or contradict
   Section 0.

---

# END v5.8.0 (additive, strict tasks + Kilo sub-task + Orchestrator recovery governance)

