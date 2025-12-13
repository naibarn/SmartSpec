name: /smartspec_generate_plan
version: 5.7.0
role: plan-generation/orchestration
write_guard: ALLOW-WRITE
purpose: Generate a high-level, dependency-aware implementation plan
         for one or more SmartSpec specifications with v5.6
         centralization, UI mode alignment, multi-repo/multi-registry
         safety, KiloCode-compatible orchestration, and
         web/AI-aware security, dependency, and data-sensitivity
         guardrails (including React/Next.js/RSC/Node/npm and AI/LLM
         features).
---

## 1) Summary

`/smartspec_generate_plan` creates or updates **plan documents** (for example
`plan.md`) for one or more specs, driven by the SmartSpec index,
registries, and multi-repo context.

This is the planning layer in the v5.6 chain:

1. `/smartspec_validate_index`
2. `/smartspec_generate_spec`
3. `/smartspec_generate_plan`
4. `/smartspec_generate_tasks`
5. `/smartspec_sync_spec_tasks`

Core goals:

- produce plans that are **task-ready** and safe inputs to
  `/smartspec_generate_tasks`
- prevent cross-SPEC and cross-repo drift for shared names and entities
- respect **UI mode** (JSON-first vs inline) so UI sequencing matches
  both SPEC and TASKS rules
- remain conservative when index/registry context is incomplete
- keep plan content **aligned with `spec.md`** (no hidden requirements)

> **Execution but governance-aware**
>
> - This workflow **may write** plan files and reports in the current
>   repo (subject to `--dry-run` and safety-mode).
> - It **does not** modify specs, tasks, tests, code, or registries in
>   non-additive ways.
> - It **does not** run test suites or external systems.
> - It focuses on structure and sequencing, not low-level commands.

**v5.6.2 note (retained):**

- v5.6.2 adds `--run-label`, `--plan-layout`, explicit safety status
  markers, and stronger guidance for AI UI JSON and Kilo multi-spec
  scopes. No prior flags or behaviors are removed.

**v5.6.3 note (additive hardening, retained):**

- When target specs use **React/Next.js/RSC/Node/npm**, plans must:
  - read `tool-version-registry.json` when available;
  - schedule upgrade/patch tasks that comply with registry policy
    (no downgrades below `min_patch`, safe ranges only);
  - include tasks to review RSC and `react-server-dom-*` surfaces and
    SSR/Edge runtimes as high-risk integration points.
- For specs describing **AI/LLM features**, plans must:
  - schedule work for prompt & context hygiene, prompt injection
    defenses, logging policies, and red-team-style testing.
- For specs involving **sensitive data**, plans must:
  - consider data classification, anonymization/masking, and ensure
    SmartSpec artifacts (plans/reports/ui.json) do not persist
    sensitive data.
- For **design-system-driven UIs** (MUI/React etc.), plans must:
  - align work with design tokens and App-level component registries,
    and avoid ad-hoc visual/structural decisions.
- Plan reports must carry **audit metadata** (workflow version,
  KB version/hash when available, key flags such as `--safety-mode`,
  `--kilocode`, index/registry paths, timestamp, run-label).

**v5.6.4 note (patch-level tightening):**

- Removed non-SmartSpec citation/markup artifacts from the specification
  to keep it clean and deterministic for LLMs and tooling.
- Clarified that when registries (especially `tool-version-registry.json`)
  are missing but clearly needed, the plan must schedule Phase 0
  tasks to create/populate them.
- Added explicit expectations to:
  - avoid propagating secrets/PII from specs into plans/reports;
  - mark any detected secret/PII patterns for redaction/cleanup;
  - make `DEV-ONLY` plans unsuitable for production/release gating
    without human review and (ideally) strict-mode regeneration.

Use this workflow to obtain a **structured, dependency-ordered plan**
across one or more specs, ready for task breakdown and execution.

---

## 2) When to Use

Use `/smartspec_generate_plan` when:

- starting a new feature or program and multiple specs are involved
- onboarding a new team to an existing spec portfolio
- preparing to run `/smartspec_generate_tasks` on a set of specs
- re-planning after major refactors, reindexing, or ownership changes
- coordinating work across **two or more repos** that share registries
  or ownership
- planning work for stacks that include **React/Next.js/RSC/Node/npm**
  or **AI/LLM features**, where security, dependency, and
  data-sensitivity guardrails must be explicit.

Do **not** use this workflow when:

- you only want to generate tasks for a fully-scoped single spec →
  consider `/smartspec_generate_tasks` directly
- you want to mass-edit specs or tasks → use appropriate generation or
  editing workflows instead
- the project explicitly forbids auto-generated plans (for example,
  manual-only planning required for audit reasons)

---

## 3) Inputs / Outputs

### 3.1 Inputs (artifacts, read-only)

- **SPEC_INDEX** (index, if present)
  - `.spec/SPEC_INDEX.json` (canonical)
  - `SPEC_INDEX.json` at repo root (legacy mirror)
  - `.smartspec/SPEC_INDEX.json` (deprecated)
  - `specs/SPEC_INDEX.json` (older layout)

- **Registries** (read-only for this workflow)
  - primary: `.spec/registry/` by default
  - supplemental: directories from `--registry-roots`
  - including, when present:
    - `tool-version-registry.json` for tool/framework version policy;
    - design-system registries such as
      `design-tokens-registry.json`,
      `ui-component-registry.json`,
      `app-component-registry.json`,
      `patterns-registry.json`.

- **Target spec files**
  - `specs/<category>/<spec-id>/spec.md` (recommended)
  - optionally with existing `plan.md` next to `spec.md`
  - optionally with `tasks.md` for context
  - optionally with `ui.json` for UI specs

- **Multi-repo context** (optional)
  - `--workspace-roots` and/or `--repos-config` to locate dependent
    specs in other repos (read-only)

- **Optional UI governance context** (read-only)
  - UI governance metadata may be embedded in specs, registries, or
    separate reports (for example from `/smartspec_ui_validation` or
    `/smartspec_ui_consistency_audit`). When present, the plan should
    schedule review/remediation phases for high-risk UI units.

- **Optional AI/data-sensitivity context** (read-only)
  - Indicators in specs/registries/reports that:
    - features are AI/LLM-based;
    - data flows include sensitive classes (PII, financial, health,
      trade secrets, regulated data).

### 3.2 Inputs (flags)

All flags are described in **Section 5)**.

### 3.3 Outputs

- **Plan document**
  - default path: `plan.md` next to the primary target `spec.md`
  - for multi-spec scopes, the layout is governed by `--plan-layout`
    and `--output` (see 6.3).
  - each plan MUST include a small header block (YAML or table) that
    captures at least:
    - spec IDs in scope
    - SPEC_INDEX path (and version/hash if known)
    - planning run label (if `--run-label` used)
    - planning timestamp
    - `safety_status = SAFE | UNSAFE | DEV-ONLY`
    - note of whether:
      - web stack guardrails (e.g., React/Next.js/Node) were applied;
      - AI/LLM safety planning was in scope;
      - data-sensitivity considerations were in scope.

- **Plan report**
  - default directory: `.spec/reports/generate-plan/`
  - contents (human-readable and/or JSON):
    - index path used
    - registry directory used
    - registry roots used
    - workspace roots / repos-config used
    - safety mode
    - UI mode
    - planning run label
    - planning scope (spec paths / spec IDs)
    - dependency graph summary
    - multi-repo reuse vs implement notes
    - registry alignment notes
    - cross-SPEC naming drift warnings
    - safety status and reasons
    - web/React/Next.js/Node/npm stack detection (if any)
    - `tool-version-registry.json` presence and usage (if any)
    - AI/LLM feature detection and planned guardrails (if any)
    - data-sensitivity classification and related plan items (if any)
    - recommended follow-up workflows
    - audit metadata:
      - workflow name & version
      - SmartSpec KB version/hash (if available)
      - key flags (`--safety-mode`, `--kilocode`, `--index`,
        `--registry-dir`, presence of tool-version-registry)
      - timestamp and run-label

When `--dry-run` is enabled, no files are written; the plan is printed
or simulated via stdout and/or report content.

---

## 4) Modes

### 4.1 Role & write guard

- Role: **plan-generation/orchestration (execution)**
- Write guard: **ALLOW-WRITE**, with constraints:
  - Writes are limited to:
    - `plan.md` next to target `spec.md`
    - the consolidated plan at `--output` (if provided)
    - `.spec/reports/generate-plan/` (or `--report-dir`)
  - specs, tasks, registries, and other docs remain read-only.
  - sibling repos discovered via `--workspace-roots` or
    `--repos-config` are always treated as **read-only**.
  - `--dry-run` forces full read-only behavior.

### 4.2 Safety mode (strict vs dev)

Controlled by `--safety-mode` and legacy alias `--strict`.

- `strict` (default)
  - If ambiguity would cause cross-repo duplication or conflicting
    ownership in the plan, generation must:
    - either stop, or
    - clearly flag the plan as **unsafe to use as-is**, via
      `safety_status=UNSAFE` in both plan and report.
  - requires explicit reuse vs implement decisions for shared entities.
  - blocks when shared names conflict across registries or when
    critical dependencies are unresolved.
  - for web stacks, blocks plans that recommend versions below
    registry `min_patch` or incompatible series.

- `dev`
  - allows plan generation even when index/registries are incomplete or
    ambiguous.
  - the plan must contain prominent warnings and TODOs, and
    `safety_status` must be set to `DEV-ONLY`.
  - intended for exploration and early-stage planning; should not be
    treated as a final, release-governed plan without review.
  - plans marked `DEV-ONLY` **must not** be used as-is for
    production/release gating without human review and, ideally,
    regeneration under `strict` mode.

### 4.3 UI mode (JSON-first vs inline)

Controlled by `--ui-mode=<auto|json|inline>`:

- `auto` (default): infer from context, consistent with
  `/smartspec_generate_spec` and UI workflows.
- `json`: plan assumes JSON-first UI (`ui.json` as primary UI spec) and
  schedules UI JSON work explicitly.
- `inline`: plan assumes UI specification is embedded in `spec.md`, and
  does not require or depend on `ui.json`.

The resolved UI mode influences which UI planning steps appear (for
example, `ui.json` production, component mapping, AI review steps).

### 4.4 Platform semantics & KiloCode mode

The workflow is platform-agnostic, but when running under Kilo with
`--kilocode`:

- effective role: **Ask/Architect**, with write operations executed
  under the same constraints as above.
- must follow the **Kilo Orchestrator-per-task rule**:
  - before each top-level planning scope (each spec or spec group),
    switch to Orchestrator and decompose subtasks, unless
    `--nosubtasks` is set.
- default under Kilo: **subtasks ON**.

For multi-spec scopes, Orchestrator SHOULD:

- group spec-level subtasks in **dependency order** based on
  SPEC_INDEX;
- for specs at the same level, sort deterministically (for example,
  by category then spec-id) to keep plans stable across runs.

If `--kilocode` is present but Kilo is not detected, treat it as a
meta-flag (no-op) and run as normal.

If Orchestrator is unavailable or misconfigured:

- in `strict` safety mode:
  - treat as an **infra failure**; prefer to stop with a clear error
    and report entry rather than silently degrading behavior.
- in `dev` safety mode:
  - may degrade to a single-flow behavior while:
    - marking the degradation clearly in the report; and
    - recommending follow-up remediation.

---

## 5) Flags

> **Non-removal guarantee:** All flags and semantics from the prior
> version are preserved; new behavior is additive only.

### 5.1 Index / Registry

- `--index=<path>`
  - Path to SPEC_INDEX.
  - Default: auto-detect in canonical order.

- `--specindex=<path>`
  - Alias for `--index` (kept for cross-workflow consistency).

- `--registry-dir=<path>`
  - Primary registry directory.
  - Default: `.spec/registry`.

- `--registry-roots="<dir1>,<dir2>,..."`
  - Comma-separated list of supplemental registry directories.
  - Loaded read-only as additional validation sources.
  - Precedence:
    - primary registry (`--registry-dir`) is authoritative.
    - supplemental registries (`--registry-roots`) must never be
      overwritten; conflicts are reported in the plan, not silently
      resolved.

### 5.2 Multi-repo resolution

- `--workspace-roots="<root1>,<root2>,..."`
  - Additional repo roots to search for dependency specs.

- `--repos-config=<path>`
  - JSON map of repo IDs to filesystem roots.
  - Preferred over `--workspace-roots` when present.
  - Recommended path: `.spec/smartspec.repos.json`.

### 5.3 Scope & identity

- `--spec=<path>`
  - Explicit spec path.
  - Example: `specs/core/spec-core-004-rate-limiting/spec.md`.

- `--spec-ids=<id1,id2,...>`
  - Comma-separated list of spec IDs to plan for.
  - Requires SPEC_INDEX to resolve IDs.

- `--run-label=<string>`
  - Optional human/CI-friendly label for this planning run.
  - Included in plan header and plan report.
  - Can be used to correlate with CI jobs, branches, or releases.

If neither `--spec` nor `--spec-ids` is provided, the workflow may
require an explicit spec path based on project conventions.

### 5.4 Output & layout

- `--output=<path>`
  - Optional output plan path. When omitted, defaults to `plan.md` next
    to the primary target `spec.md` for single-spec scopes.

- `--plan-layout=<per-spec|consolidated>`
  - Controls how plans are written when multiple specs are in scope.
  - `per-spec` (default):
    - one `plan.md` per spec (next to each `spec.md`).
  - `consolidated`:
    - a single consolidated plan at `--output`.
    - if `--output` is not provided, behavior must be clearly
      documented in the report (for example, defaulting to
      `plan.md` next to the primary spec).

- `--report-dir=<path>`
  - Override default `.spec/reports/generate-plan/`.

- `--stdout-summary`
  - Print a short summary of the planning run to stdout (scope, index
    path, safety mode, safety status, key warnings).

### 5.5 Safety

- `--safety-mode=<strict|dev>`
  - Default: `strict`.

- `--strict`
  - Alias for `--safety-mode=strict`.

- `--dry-run`
  - Generate and print the plan and report content **without writing**
    any files.

### 5.6 UI mode alignment

- `--ui-mode=<auto|json|inline>`
  - Default: `auto`.
  - Planning behavior and UI phases align with the resolved UI mode.

### 5.7 Kilo / subtasks

- `--kilocode`
  - Enable KiloCode semantics and Orchestrator-per-task behavior when
    running under Kilo.

- `--nosubtasks`
  - Disable Orchestrator automatic subtasks, for small scopes or
    debugging.

---

## 6) Canonical Folders & File Placement

### 6.1 SPEC_INDEX detection order

Detection order (single source of truth):

1. `.spec/SPEC_INDEX.json` (canonical)
2. `SPEC_INDEX.json` at repo root (legacy mirror)
3. `.smartspec/SPEC_INDEX.json` (deprecated)
4. `specs/SPEC_INDEX.json` (older layout)

If no index is found:

- planning proceeds in **local-spec-only** mode.
- the plan must include a **Phase 0** recommendation to initialize and
  validate the index (for example, via `/smartspec_reindex_specs` and
  `/smartspec_validate_index`).

### 6.2 Registries

- primary registry directory: `.spec/registry/` (configurable via
  `--registry-dir`).
- supplemental registries: directories from `--registry-roots` (read-
  only).

If a shared name is defined in any loaded registry:

- the plan must treat it as **reused**, not as a new shared entity to
  create.

When `tool-version-registry.json` exists in the primary registry:

- treat it as the authoritative description of allowed and minimum
  patched tool/framework versions (including React/Next.js/Node).
- plans must:
  - avoid recommending versions below configured `min_patch` for any
    chosen major/minor;
  - avoid downgrades across series except as explicit emergency
    rollbacks with clear justification;
  - surface incompatible combinations (e.g., microfrontends sharing
    runtimes but using divergent, disallowed versions) as plan items
    for consolidation.

When a registry that is clearly relevant (for example,
`tool-version-registry.json` in a React/Next.js/Node stack) is missing
or obviously stale:

- the plan MUST include Phase 0 tasks to create or refresh that
  registry under the appropriate owner (platform/security) rather than
  silently assuming defaults.

### 6.3 Plan files

- default plan location for single-spec runs:
  - `specs/<category>/<spec-id>/plan.md`.
- for multi-spec scopes:
  - if `--plan-layout=per-spec` (default):
    - write `plan.md` next to each `spec.md` in scope.
  - if `--plan-layout=consolidated`:
    - if `--output` is provided, write a single consolidated plan to
      that path.
    - if `--output` is not provided, the workflow MUST document the
      chosen default path (for example, primary spec's `plan.md`) in
      the report and stdout summary.

Every generated or updated plan MUST include:

- a header block with spec IDs, index path, run-label (if any),
  timestamp, and `safety_status`.

### 6.4 Reports

- default directory: `.spec/reports/generate-plan/`.
- file naming pattern (recommended):
  - `<timestamp>_<primary-spec-id>_generate-plan.{md|json}`.

The workflow must **not** create new top-level directories outside
`.spec/` or `specs/` by default.

---

## 7) Weakness & Risk Check (Quality Gate)

Before treating this workflow specification as complete, verify:

1. **Write safety**
   - `--dry-run` truly prevents all writes.
   - writes are scoped to plan files and plan reports in the current
     repo only.

2. **Index & registry correctness**
   - SPEC_INDEX detection order is followed.
   - primary vs supplemental registries are respected.
   - shared entities found in registries are treated as reused in the
     plan.

3. **Multi-repo safety**
   - sibling repos are read-only.
   - cross-repo dependencies are modeled as external and planned via
     reuse, not duplication.

4. **UI mode governance**
   - UI mode (`auto|json|inline`) is resolved consistently with other
     workflows.
   - JSON-first UI planning steps are included when appropriate.
   - no planning step encourages embedding business logic in `ui.json`.
   - when AI-generated UI JSON or UI governance signals are available,
     high-risk UI units are surfaced as explicit plan items.

5. **Safety-mode behavior**
   - `strict` mode blocks or hard-frames plans when ambiguity would
     cause duplicate or conflicting shared entities or unsafe
     web-stack versioning.
   - `dev` mode allows generation but always calls out risks clearly
     and sets `safety_status=DEV-ONLY`.

6. **Spec/plan/tasks alignment**
   - plans remain aligned with `spec.md` as the source-of-truth.
   - missing or ambiguous requirements are turned into explicit plan
     items (for example, "clarify X in spec"), not silently invented.

7. **Legacy compatibility**
   - all original flags remain supported.
   - no existing behavior is weakened or removed.

8. **KiloCode support**
   - `--kilocode` and `--nosubtasks` behave as documented.
   - Orchestrator-per-task is followed under Kilo.
   - Orchestrator failure modes respect `strict` vs `dev` semantics.

9. **Safety status markers**
   - both plan and report clearly carry a `safety_status` field.
   - downstream automation can reliably treat non-`SAFE` plans as a
     gate failure or review-required.

10. **Framework & dependency guardrails (React/Next.js/RSC/Node/npm)**
    - for specs using these stacks, plans:
      - read and respect `tool-version-registry.json` policy;
      - avoid planning downgrades below `min_patch` or disallowed
        combinations;
      - schedule upgrades/patches and convergence when multiple series
        must coexist;
      - schedule reviews around RSC, SSR/Edge, and
        `react-server-dom-*` boundaries as high-risk surfaces.

11. **Design-system & component-registry alignment**
    - when design tokens and UI/App component registries exist, plans:
      - schedule work to use App-level components rather than raw
        library components for new UI;
      - encourage consolidating hard-coded styles into design tokens;
      - incorporate remediation tasks for pages/components that diverge
        from patterns without rationale.

12. **AI & prompt safety planning**
    - when specs include AI/LLM features, plans:
      - include tasks for prompt/context hygiene;
      - consider prompt-injection defense and instruction hierarchy;
      - consider logging and output-handling policies;
      - include red-team style testing tasks for worst-case prompts.

13. **Data sensitivity & SmartSpec artifacts**
    - when specs touch sensitive data, plans:
      - include tasks for data classification and anonymization/masking
        where appropriate;
      - avoid planning to store sensitive data inside logs, plans,
        reports, `ui.json`, design tokens, or long-lived prompts;
      - surface gaps in data-protection baselines as explicit plan
        items.

14. **Registry conflict surfacing**
    - when multiple registries define conflicting versions or UI
      components, plans:
      - treat conflicts as explicit items to resolve;
      - prefer platform/global registries as starting points;
      - avoid silently merging conflicting entries.

15. **Secret/PII propagation**
    - planning runs must:
      - avoid copying or persisting secrets, access tokens, passwords,
        or PII from specs or other artifacts into plans or reports;
      - treat any detected secret/PII-like patterns as issues to be
        redacted or cleaned up by humans, with follow-up tasks and
        ownership noted in the report;
      - rely on dedicated secret/data scanners in CI as a complement,
        not a replacement for these guardrails.

---

## 8) Legacy Flags Inventory

- **Kept as-is (legacy behavior):**
  - `--index`
  - `--specindex` (alias)
  - `--registry-dir`
  - `--registry-roots`
  - `--workspace-roots`
  - `--repos-config`
  - `--spec`
  - `--spec-ids`
  - `--output`
  - `--safety-mode`
  - `--strict`
  - `--dry-run`
  - `--ui-mode`

- **New additive flags (v5.6.x family):**
  - `--report-dir`
  - `--stdout-summary`
  - `--kilocode`
  - `--nosubtasks`
  - `--run-label`
  - `--plan-layout`

No legacy flag or behavior is removed.

---

## 9) KiloCode Support (Meta-Flag)

As a planning workflow, `/smartspec_generate_plan` must support
KiloCode semantics without depending on them.

- Accepts `--kilocode` as a meta-flag.
- Under Kilo:
  - Orchestrator coordinates per-spec planning tasks.
  - Code/tool mode reads specs, indexes, registries, and formats plans.
  - write guard and safety-mode rules apply as in non-Kilo mode.
- Under non-Kilo:
  - `--kilocode` is treated as no-op.

### 9.1 Orchestrator loop (Kilo + subtasks)

For each spec or spec group in scope (following dependency order):

1. Resolve index/registry context.
2. Resolve multi-repo dependencies.
3. Read spec(s) and optional existing plan(s).
4. Detect web stacks (React/Next.js/Node/etc), AI/LLM features,
   and data-sensitivity markers.
5. Build dependency graph for that scope.
6. Generate phase-structured plan, including:
   - web-stack security/dependency guardrails;
   - AI/LLM safety and data-sensitivity tasks;
   - UI/design-system alignment.
7. Attach cross-repo and registry alignment notes.
8. Set an appropriate `safety_status` for that scope and propagate it
   to the consolidated view (for example, any UNSAFE scope makes the
   overall run UNSAFE).

Subtasks are ON by default; `--nosubtasks` can disable them.

---

## 10) Inline Detection Rules

The workflow must not call other SmartSpec workflows programmatically.
Instead, it:

- detects environment markers for Kilo/ClaudeCode/Antigravity from
  system context.
- checks for `--kilocode` in arguments.
- detects web stack usage by:
  - inspecting specs and optional dependency files (when available)
    for references to React, Next.js, Node, RSC/server actions,
    `react-server-dom-*`, SSR/Edge runtimes;
  - considering hints in SPEC_INDEX or registries.
- detects AI/LLM features by:
  - scanning specs for AI/LLM feature descriptions (chat, copilots,
    agents, prompt-based flows, etc.);
  - reviewing any AI-usage markers from other workflows (if present).
- detects data sensitivity by:
  - scanning specs for references to PII, financial/health data,
    trade secrets, or regulated zones.
- only **recommends** follow-up workflows (for example,
  `/smartspec_generate_tasks`, `/smartspec_release_readiness`,
  `/smartspec_ui_validation`,
  `/smartspec_ui_consistency_audit`) inside the human-readable plan or
  report.

---

## 11) Multi-repo / Multi-registry Rules

1. Use `--repos-config` when available to map logical repo IDs to
   physical roots.
2. Use `--workspace-roots` as a simpler fall-back list of sibling
   repositories.
3. When resolving dependencies from SPEC_INDEX:
   - search current repo first.
   - then repos from `--repos-config`.
   - then `--workspace-roots`.
4. When a dependency spec is resolved outside the current repo:
   - mark it as an **external dependency** in the plan.
   - include a **reuse-not-rebuild** note describing what to reuse.
5. For entities already present in registries (APIs, models, terms,
   components):
   - the plan must not schedule creation of a conflicting shared entity.
   - instead, the plan must schedule:
     - integration, client, adapter, or migration steps.
6. Conflicts between primary and supplemental registries must be
   surfaced as explicit plan items for reconciliation, preferring the
   platform/global registry as the starting point for resolution.

---

## 12) UI Addendum (v5.6, JSON-first & Inline UI)

Apply this addendum when any of the following are true:

- a target spec is categorized as `ui` in SPEC_INDEX.
- the target spec folder contains `ui.json` (or similar UI JSON files).
- the spec explicitly mentions a design/`ui.json` workflow.

### 12.1 UI planning phases

When UI is in scope, the plan SHOULD include:

1. **Design source alignment**
   - confirm whether UI is JSON-first or inline (`UI_MODE`).
   - if JSON-first, ensure a step exists to create/update `ui.json` as a
     design source-of-truth.

2. **Component mapping gate**
   - plan a step to map UI JSON nodes or design frames to components.
   - if `ui-component-registry.json` exists, align names and variants.

3. **Logic separation**
   - ensure business logic is modeled in spec and code layers, **not**
     in `ui.json`.
   - plan separation between UI layout/state and domain rules.

4. **Consistency & modern UX expectations**
   - recommend using workflows like `/smartspec_ui_consistency_audit`
     and `/smartspec_ui_validation` (by name only) to govern design
     system adherence and validation coverage.

### 12.2 JSON-first UI vs inline UI

- When `UI_MODE=json`:
  - `ui.json` is treated as the primary UI spec artifact.
  - plans must schedule:
    - UI JSON authoring or regeneration (possibly AI-assisted).
    - review/approval steps for AI-generated UI JSON.
    - alignment with design system registries and global style presets.

- When `UI_MODE=inline`:
  - keep UI/UX requirements and flows inside `spec.md`.
  - plans focus on implementation and validation of documented UX,
    without assuming `ui.json` exists.

### 12.3 AI-generated UI JSON and UI workflow signals

If AI is used to generate `ui.json`, and/or if UI governance reports are
available from other workflows, the plan SHOULD:

- treat signals such as (where present):
  - `ui_spec_origin = AI | HUMAN | MIXED | UNKNOWN`
  - `ui_spec_review_status = UNREVIEWED | DESIGNER_APPROVED | OVERRIDDEN | UNKNOWN`
  - `ui_json_quality_status = STRONG | OK | WEAK | BROKEN | UNKNOWN`
- schedule:
  - designer/UX review for UI units where origin is AI and review status
    is UNREVIEWED, especially for CRITICAL/HIGH flows.
  - remediation steps where `ui_json_quality_status` is WEAK or BROKEN.
  - follow-up consistency and validation checks using the UI workflows
    (by name only).

The plan must never assume AI-generated UI JSON is production-ready
without explicit review or governance steps.

### 12.4 Web Stack Security & Dependency Planning (React/Next.js/RSC/Node/npm)

When target specs involve React, Next.js, or related Node-based web
stacks (including SSR/Edge, RSC/server actions, or
`react-server-dom-*` packages), plans MUST:

1. **Use tool-version-registry policy when available**
   - read `.spec/registry/tool-version-registry.json` (or from
     supplemental registries) for React/ReactDOM/Next/Node baseline
     policy;
   - ensure planning items:
     - respect `min_patch` and allowed series;
     - avoid recommending downgrades below these baselines;
     - describe any necessary series-consolidation work.

2. **Treat RSC and `react-server-dom-*` as high-risk**
   - schedule reviews of:
     - data crossing RSC boundaries;
     - streaming responses and serialization;
     - server actions and access control.

3. **Include CI/release guardrail tasks**
   - lockfile maintenance (e.g., `package-lock.json`, `yarn.lock`,
     `pnpm-lock.yaml`);
   - regular dependency scans via `npm audit` and/or SCA tools;
   - configuration of dependency bots (Dependabot/Renovate/etc.);
   - integration with CI/release/security workflows that compare actual
     tool versions against registry policy.

4. **Surface incompatible fragmentation**
   - if multiple services in scope rely on incompatible or disallowed
     combinations of tool versions, the plan should:
     - call this out explicitly;
     - schedule upgrade paths that converge on allowed, compatible
       ranges.

### 12.5 Design-System & Component-Registry Planning

When a design system is present (with design tokens and/or UI/App
component registries):

- plans SHOULD:
  - reference `design-tokens-registry.json` for spacing, colors,
    typography, radius, shadows, and motion instead of ad-hoc values;
  - reference `ui-component-registry.json` and/or
    `app-component-registry.json` to define which components are used
    for each view (preferring App-level wrappers such as `AppButton`,
    `AppCard`, etc.);
  - pull layout patterns from `patterns-registry.json` and schedule
    remediation when existing UIs diverge without good reason;
  - ensure loading/empty/error states use standard components like
    `AppSkeleton`, `AppEmptyState`, `AppErrorState`.

- the plan MAY add tasks to:
  - document or update App-level components in Storybook (or similar);
  - validate design tokens and patterns across all affected UIs.

### 12.6 AI & Prompt/Data-Sensitivity Planning for UI

When UI surfaces expose AI/LLM features or sensitive data:

- plans SHOULD:
  - include tasks to define safe prompt & context-construction rules
    (what data can appear, how to redact, how to scope per-user/tenant);
  - include tasks to review UI for unsafe logging or display of
    sensitive data (e.g., PII) in prompts, results, or previews;
  - ensure specifications for error/logging components align with
    data-protection baselines (no secrets in logs, limited retention).

---

## 13) Best Practices

- Always run with `--safety-mode=strict` for production-bound programs,
  unless explicitly experimenting.
- Use `--dry-run` the first time in a repo to validate index/registry
  resolution.
- Keep `.spec/SPEC_INDEX.json` and `.spec/registry/` up to date; plan
  work to fix them if they lag behind reality.
- For multi-repo setups, maintain `--repos-config` under `.spec/` to
  avoid brittle path-based discovery.
- Decide on UI mode per spec (JSON-first vs inline) and keep it
  consistent across the project.
- Treat each plan as a **governance artifact**:
  - include `safety_status` and run-label.
  - version it and review it.
  - tie it into release and roadmap discussions.
- When plans and specs diverge, fix the spec first, then regenerate or
  update the plan.
- For React/Next.js/Node/npm stacks:
  - always align planned upgrades with registry-encoded baselines;
  - ensure plans include explicit RSC/SSR/Edge guardrail tasks.
- For AI/LLM features:
  - treat the model as untrusted; plan clear guardrails and
    red-team-style testing.
  - avoid including sensitive data in long-lived prompts, logs, or
    examples; prefer redaction and sampling.
- For sensitive or regulated data:
  - assume additional external data-protection and compliance tooling
    (e.g., DLP, secret scanners, SCA) will complement this workflow;
  - use `safety_status` and plan phases to make these dependencies
    explicit.

---

## 14) For the LLM / Step-by-step Flow & Stop Conditions

### 14.1 Step-by-step flow

1. **Resolve flags & environment**
   - parse `--index`/`--specindex`, `--registry-dir`,
     `--registry-roots`, `--workspace-roots`, `--repos-config`,
     `--spec`, `--spec-ids`, `--run-label`, `--output`,
     `--plan-layout`, `--safety-mode`, `--strict`, `--dry-run`,
     `--ui-mode`, `--kilocode`, `--nosubtasks`, `--report-dir`,
     `--stdout-summary`.

2. **Resolve SPEC_INDEX**
   - detect index path using canonical order.
   - if none found, set local-spec-only mode and record warnings.

3. **Resolve registry directories**
   - locate primary registry dir (`--registry-dir` or default).
   - record supplemental registry roots (`--registry-roots`).
   - detect presence of `tool-version-registry.json` and
     design-system registries (design tokens, UI/App components,
     patterns).

4. **Resolve multi-repo roots**
   - build a search set from current repo, `--repos-config`, and
     `--workspace-roots`.

5. **Identify planning scope**
   - use `--spec` if provided.
   - otherwise use `--spec-ids` via SPEC_INDEX.
   - if neither is available, follow project conventions or request a
     spec path (where allowed).

6. **Read spec(s) (read-only)**
   - load `spec.md` for each target.
   - collect:
     - scope and objectives
     - functional and non-functional requirements
     - dependencies and integrations
     - API/model/term hints
     - UI markers (`ui` category, `ui.json` presence, etc.)
     - any explicit description of web stack, AI features, or
       sensitive data.

7. **Detect web stacks, AI features, and data sensitivity**
   - infer whether target specs:
     - use React/Next.js/RSC/Node or other notable frameworks;
     - specify AI/LLM features;
     - deal with sensitive data (PII, financial/health, trade
       secrets, regulated zones).

8. **Build a dependency graph**
   - if index exists, use its dependency graph as primary.
   - validate spec-local dependencies against the index.
   - if no index, infer minimal ordering from spec text and structure.

9. **Centralization consistency gate**
   - check registries for shared names referenced by target specs.
   - label entities as reused vs new.
   - detect naming drift across registries and specs.
   - in strict mode, treat unresolved conflicts as blocking (set
     `safety_status=UNSAFE` and avoid presenting the plan as
     ready-to-execute).

10. **Resolve UI mode**
    - compute `UI_MODE` based on `--ui-mode` and contextual signals.
    - determine whether UI addendum applies.

11. **Incorporate UI governance signals (if available)**
    - if specs, registries, or provided reports contain AI UI JSON
      signals or design-system hints, integrate them into planning
      (review/remediation steps).

12. **Integrate web-stack security & dependency planning**
    - if React/Next.js/RSC/Node are in scope:
      - consult `tool-version-registry.json` (if present) for policy;
      - identify any version misalignments or fragmentation;
      - add plan items for upgrades, patching, and convergence;
      - add plan items for RSC/SSR/Edge and
        `react-server-dom-*` boundary reviews.

13. **Integrate AI & data-sensitivity planning**
    - if AI/LLM features are in scope:
      - add plan items for prompt/context hygiene, injection defense,
        logging, and red-team testing.
    - if sensitive data is in scope:
      - add plan items for data classification and
        anonymization/masking where appropriate;
      - add plan items ensuring specs/plans/logs/ui.json avoid storing
        sensitive data inappropriately.

14. **Generate phase-structured plan**
    - use phases such as:
      - Phase 0: Foundations (index/registry/multi-repo readiness).
      - Phase 1: Shared Contracts & Patterns.
      - Phase 2: Core Domain & Data.
      - Phase 3: Service/Use Case Layer.
      - Phase 4: API & Integration.
      - Phase 5: Observability & Security (including web-stack, AI,
        and data-sensitivity guardrails).
      - Phase 6: UI (when applicable).
    - attach testing strategy expectations to each phase.
    - ensure plan items do not contradict spec; missing clarity becomes
      plan items to refine the spec.

15. **Attach multi-repo and registry notes**
    - mark external specs, reuse-not-rebuild notes, and registry
      alignment items.

16. **Determine safety_status**
    - set `safety_status=SAFE` only if no blocking ambiguity or
      critical drift is detected (including version policy).
    - set `UNSAFE` when strict mode finds unresolved conflicts.
    - set `DEV-ONLY` for dev mode runs or exploratory plans.

17. **Secret/PII sanity check (best-effort)**
    - before finalizing content for write (or simulated write):
      - scan plan text for obvious secret/PII patterns or raw logs;
      - avoid adding such content when possible; otherwise, mark it
        clearly for redaction/cleanup in the report with an owner.
    - note in the report that external secret/data scanners are still
      required for full coverage.

18. **Write outputs**
    - if not `--dry-run`:
      - write plan files according to `--plan-layout` and `--output`.
      - embed header with spec IDs, index path, run-label (if any),
        timestamp, and `safety_status`.
      - write a plan report into `--report-dir`, including audit
        metadata.
    - if `--dry-run`:
      - simulate plan and indicate intended file paths and safety
        status.

19. **Stdout summary**
    - if `--stdout-summary`:
      - print scope, index path, safety mode, `safety_status`, and count
        of key warnings (including web-stack, AI, data-sensitivity,
        registry conflicts).

### 14.2 Stop conditions

The workflow must stop after:

- completing write/simulated-write operations in the current repo, and
- emitting the plan report and optional stdout summary.

It must **not**:

- modify `spec.md`, `tasks.md`, or registry definitions.
- write into sibling repos.
- invoke other SmartSpec workflows programmatically.

