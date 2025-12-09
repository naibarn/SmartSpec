name: /smartspec_implement_tasks
version: 5.6.4
role: implementation/execution
write_guard: ALLOW-WRITE
purpose: Implement code changes from `tasks.md` (and `spec.md`/`plan.md`
         when present) with SmartSpec v5.6 centralization, multi-repo
         and multi-registry alignment, KiloCode Orchestrator support,
         web-stack (React/Next.js/RSC/Node/npm) guardrails, and
         AI/data-sensitivity safety.

---

## 1) Summary

`/smartspec_implement_tasks` drives real code and test changes based on
reviewed `tasks.md`, while enforcing:

- SPEC_INDEX and registry centralization rules;
- multi-repo ownership boundaries;
- reuse-over-duplicate for shared APIs/models/terms/UI components;
- UI JSON governance where applicable;
- KiloCode Orchestrator-per-task execution when enabled.

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

All existing flags and behaviors are preserved; new behavior is additive.

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
    - Orchestrator coordinates per-task execution;
    - subtasks and checkpoints are handled per top-level task;
    - this workflow acts as the implementation engine inside that loop.

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

### 5.8 Reporting & summary (additive)

- `--report-dir=<path>`
  - override default `.spec/reports/implement-tasks/`.

- `--stdout-summary`
  - emit a short summary at the end (scope, safety mode, key warnings)
    to stdout.

---

## 6) Canonical Folders & File Placement

### 6.1 SPEC_INDEX detection

Detection order:

1. `.spec/SPEC_INDEX.json` (canonical).
2. `SPEC_INDEX.json` at repo root (legacy mirror).
3. `.smartspec/SPEC_INDEX.json` (deprecated).
4. `specs/SPEC_INDEX.json` (older layout).

If `--index`/`--specindex` is provided, it overrides detection.

If no index is found:

- `strict`:
  - treat as a major gap; prefer `--validate-only` and add governance
    recommendations rather than unbounded implementation.
- `dev`:
  - may continue with local-only assumptions but must emit explicit
    TODOs to create/validate SPEC_INDEX.

### 6.2 Registries

- primary: `.spec/registry/` or `--registry-dir`.
- supplemental: `--registry-roots` (read-only).

When `tool-version-registry.json` exists:

- treat as authoritative tool/framework baseline for React/Next/Node;
- do not downgrade below `min_patch` or outside allowed series;
- implementation must converge toward allowed baselines where feasible.

If a web stack is detected but `tool-version-registry.json` is missing
or clearly outdated:

- `strict`:
  - prefer to block high-risk dependency changes, adding governance
    recommendations instead of guessing.
- `dev`:
  - may implement local changes but must add TODOs to create/refresh
    the registry under platform/security ownership.

### 6.3 Spec & tasks files

- Spec: `specs/<category>/<spec-id>/spec.md`.
- Tasks: `specs/<category>/<spec-id>/tasks.md`.
- Optional plan: `specs/<category>/<spec-id>/plan.md`.
- Optional `ui.json` for UI specs.

### 6.4 Reports

- default directory: `.spec/reports/implement-tasks/`.
- suggested file naming:
  - `<timestamp>_<spec-id>_implement-tasks.{md|json}`.

Reports must include audit metadata:

- workflow name & version;
- SmartSpec KB version/hash (if available);
- effective safety-mode;
- key paths (index, registry-dir, repos-config);
- detection of web-stack/AI/data-sensitivity;
- summary of scope and key warnings/blockers.

The workflow must **not** create new top-level directories outside
`.spec/` or `specs/` by default.

---

## 7) Multi-Repo & Multi-Registry Rules

1. Resolve repos from `--repos-config` first, then `--workspace-roots`.
2. Treat other repos as **read-only** and **ownership sources**.
3. When a dependency is owned by another repo:
   - implement integration/adapter/consumer code only in the current
     repo;
   - do not create parallel owners for the same shared concept.
4. Where registries disagree, treat conflicts as governance issues and
   avoid creating new shared entities until resolved.
5. All cross-repo work should be captured as recommendations or tasks,
   not direct code changes in sibling repos.

---

## 8) Pre-Implementation Consistency Gate

Before any code changes:

1. Validate that `spec.md`, `tasks.md` (and `plan.md` if present) refer
   to the same spec ID and scope.
2. Check SPEC_INDEX and registries for:
   - name collisions;
   - mismatched owners;
   - missing canonical entries for referenced shared entities.
3. For UI specs, ensure:
   - `ui.json` (when present) is consistent with spec and tasks;
   - no instruction implies pushing business logic into `ui.json`.

Under `strict` safety-mode:

- block or fall back to `--validate-only` when:
  - new shared-name creation is implied without registry confirmation;
  - registry conflicts or missing baselines would make code unsafe.

---

## 9) Implementation Strategy & Phasing

Implement tasks in a dependency-safe order, typically:

1. Shared contracts/interfaces (only when explicitly required and
   registry-aligned).
2. Domain models and core business logic.
3. Service/use case layer.
4. API/controllers and integration boundaries.
5. Persistence/data access.
6. Observability (logging/metrics/tracing).
7. Security and access control.
8. UI components and interactions.
9. AI/LLM layer glue (if applicable).

When `--focus` is set, adjust emphasis but keep dependencies intact.

---

## 10) UI JSON & Design-System Addendum

Apply when any of:

- spec category is `ui` in SPEC_INDEX;
- `ui.json` exists beside `spec.md`;
- spec references Penpot/UI JSON flows.

Rules:

- `ui.json` is design-owned source; treat as read-only unless tasks
  explicitly require engineering changes.
- never embed business logic or permission rules in `ui.json`.
- align components with:
  - `ui-component-registry.json`;
  - `app-component-registry.json` (prefer App-level wrappers);
  - `design-tokens-registry.json` (colors/spacing/typography/etc.);
  - `patterns-registry.json` (layout flows).

Implementation expectations:

- use App-level components like `AppButton`, `AppCard`, etc., instead
  of raw library components where defined.
- use standard loading/empty/error components.
- keep data fetching and domain logic in code, not in UI JSON.

---

## 11) Web Stack Guardrails (React/Next.js/RSC/Node/npm)

When implementing for React/Next.js/Node/RSC stacks:

1. Respect `tool-version-registry.json`:
   - do not downgrade React/Next/Node below `min_patch`;
   - prefer converging to a single allowed series per runtime boundary;
   - avoid mixing incompatible versions across microfrontends that
     share a runtime.

2. Treat RSC/server actions/`react-server-dom-*` as high-risk:
   - ensure data crossing server/client boundaries is validated and
     sanitized;
   - check that secrets and sensitive data never appear in serialized
     payloads or client bundles;
   - verify access control around server actions.

3. SSR/Edge:
   - verify environment variables are not rendered accidentally;
   - ensure cache headers and revalidation policies do not leak
     sensitive data;
   - confirm logging does not dump raw HTTP bodies or secrets.

4. Dependency & CI hygiene:
   - keep lockfiles present and consistent;
   - wire up dependency scans (`npm audit`/SCA tools);
   - ensure CI checks actual runtime tool versions vs registry baselines.

---

## 12) AI & Data-Sensitivity Guardrails

When the feature involves AI/LLM:

- implement prompt/context construction following tasks.md guidance;
- ensure instruction hierarchy and system prompts are centralized,
  not scattered in code;
- never embed secrets/PII in prompts or prompt templates;
- add logging for AI interactions that:
  - avoids raw user data where possible;
  - redacts sensitive fields;
  - is governed by retention policy.

When the feature touches sensitive data (PII/financial/health/trade
secrets/regulated):

- apply data classification and masking where appropriate;
- avoid copying production logs or data into code, tests, or examples;
- integrate with external DLP/secret-scanning tooling as required.

---

## 13) Testing Expectations

Implement or update tests aligned with:

- domain and service logic;
- contracts for shared APIs;
- integration flows across services;
- performance/SLA when defined.

Testing must:

- respect ownership (no re-creating cross-repo owners just to make
  tests pass);
- avoid using real production data or secrets in fixtures or snapshots.

---

## 14) Checkbox Update Rules (`tasks.md`)

A task can be marked as completed only when:

- required code changes are implemented;
- acceptance criteria in `tasks.md` are met;
- required tests listed for that task are green.

Partial completion:

- add notes under the task;
- do **not** check the box.

`--skip-completed` (default) skips already checked tasks.
`--force-all` can re-run implementation regardless of checkbox state.

---

## 15) Required Final Summary & Report

Each run must produce:

- human-readable summary:
  - tasks attempted/completed;
  - key files changed or created;
  - registry alignment and conflicts;
  - UI JSON/design-system notes (if applicable);
  - web-stack and AI/data-sensitivity guardrails applied;
  - open risks/blockers;
  - suggested follow-up commands or workflows.

- when `--report-dir` is set or defaulting to
  `.spec/reports/implement-tasks/`:
  - write an implementation report with the above content plus
    audit metadata.

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

5. **Safety-mode behavior**
   - strict/dev behavior matches expectations.
   - conflicts and missing context are surfaced as warnings or blocks.

6. **Web-stack guardrails**
   - React/Next/RSC/Node/npm changes respect baselines.
   - no unsafe downgrades or version fragmentation are introduced.

7. **AI & data-sensitivity**
   - prompts/logs/tests do not carry secrets/PII.
   - data classification/masking tasks are present where needed.

8. **KiloCode support**
   - `--kilocode` behavior and Orchestrator-per-task loop are honored.

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

- **New additive (v5.6.4):**
  - `--dry-run` (alias for `--validate-only`)
  - `--report-dir`
  - `--stdout-summary`

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

When Orchestrator is unavailable:

- in `strict`:
  - prefer `--validate-only` with a clear infra error.

- in `dev`:
  - may degrade to a linear flow with a warning in the report.

When Kilo is not detected, `--kilocode` is a no-op meta-flag.

---

## 19) Inline Detection Rules

This workflow must **not** call other SmartSpec workflows
programmatically. It may:

- detect Kilo/ClaudeCode/Antigravity environments from context;
- inspect flags such as `--kilocode`;
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

