---
name: /smartspec_release_readiness
version: 5.6.2
role: verification/governance
write_guard: NO-WRITE
purpose: Generate a spec-driven release checklist and readiness assessment
         aligned with SPEC_INDEX, registries, NFRs, tasks completion, and
         cross-repo/compatibility rules.
---

## 1) Summary

This workflow analyzes a *candidate release scope* (one or more specs) and
produces a **release readiness report** that is:

- bound to the canonical SPEC_INDEX and registries
- aligned with each spec’s NFRs and tasks
- explicit about environment/config assumptions
- explicit about backward compatibility and cross-repo impact
- explicit about UI governance readiness (JSON-first vs inline)

It is **strictly NO-WRITE**:

- no code changes
- no spec/tasks edits
- no registry edits
- only reports and summaries are produced.

Use it as the **final gate before deployment** or promotion to staging/production
in a SmartSpec-governed program.

---

## 2) When to Use

Use `/smartspec_release_readiness` when:

- you are preparing a **release or deployment** from a SmartSpec-governed repo
- you want a **checklist** tied directly to:
  - SPEC_INDEX entries
  - registries (API, data model, critical sections, UI components, ownership, etc.)
  - tasks completion status
  - declared NFRs and their evidence
- you need a **project-owned report file** under `.spec/reports/` for:
  - CI/CD gates
  - release manager reviews
  - audit/compliance evidence

Typical timing in the chain:

`generate_spec → generate_plan → generate_tasks → sync_spec_tasks → implement_tasks → generate_tests → verify_tasks_progress → /smartspec_release_readiness`

Do **not** use this workflow to:

- design or execute data migrations (that belongs to `/smartspec_data_migration_governance`)
- create or modify specs/tasks (use authoring workflows instead)
- generate CI matrices (use `/smartspec_ci_quality_gate`)

It can, however, *reference* their existence as part of the readiness decision.

---

## 3) Inputs / Outputs

### 3.1 Inputs (artifacts)

The workflow expects (read-only):

- **Index**
  - `.spec/SPEC_INDEX.json` (canonical, if present)
  - `SPEC_INDEX.json` at repo root (legacy mirror)
  - `.smartspec/SPEC_INDEX.json` (deprecated)
  - `specs/SPEC_INDEX.json` (older layout)

- **Specs for each targeted spec-id**
  - `specs/<category>/<spec-id>/spec.md`
  - `specs/<category>/<spec-id>/tasks.md`
  - `specs/<category>/<spec-id>/ui.json` (if JSON-first UI is used)

- **Registries (if present)**
  - `.spec/registry/api-registry.json`
  - `.spec/registry/data-model-registry.json`
  - `.spec/registry/glossary.json`
  - `.spec/registry/critical-sections-registry.json`
  - `.spec/registry/ui-component-registry.json`
  - `.spec/registry/file-ownership-registry.json`

- **Optional environment/config files** (for `--target-env`)
  - any paths passed via `--env-config-paths` (e.g. `config/*.yaml`, `infra/*.tf`)

- **Optional CI/quality metadata**
  - test reports / coverage reports (if available in predictable locations)
  - performance test results (if present)

All of these are treated as **read-only evidence**.

### 3.2 Inputs (flags)

See section **5) Flags**.

### 3.3 Outputs

- **Primary report file** (human-readable + machine-parseable structure)
  - Default location:
    - `.spec/reports/smartspec_release_readiness/<timestamp>_<release-label>.md`
  - If `--report-format=json` is used:
    - `.spec/reports/smartspec_release_readiness/<timestamp>_<release-label>.json`

Report content (per spec-id):

- scope & metadata
- NFR coverage summary (no invented NFRs)
- tasks completion evidence
- tests & evidence summary (unit/integration/contract/perf if available)
- environment/config assumptions and gaps
- backward compatibility analysis (APIs, data contracts, data migrations)
- cross-repo/registry reuse vs duplication notes
- UI governance checklist (JSON-first vs inline and consistency with project policy)
- result status per spec:
  - `READY`
  - `READY_WITH_RISKS`
  - `BLOCKED`

Release-level summary:

- aggregate status (e.g., `READY_WITH_RISKS`)
- top blocking items
- top risks grouped by category (NFR, security, data, ops, UI, duplication)
- recommended follow-up workflows (generate_tests, nfr_perf_verifier, data_migration_governance, etc.)
  - *Recommendation only, no cross-workflow calls.*

Optional **stdout summary** if `--stdout-summary` is enabled.

---

## 4) Modes

### 4.1 Role & write guard

- Role: **Verification / Governance**
- Default write guard: **NO-WRITE**

MUST NOT:

- modify any code
- modify `spec.md`, `tasks.md`, or registry files
- toggle task checkboxes

MAY:

- read all allowed artifacts
- generate report files under `.spec/reports/`
- print summaries to stdout

### 4.2 Platform semantics

- Tool-agnostic by default.
- Under Kilo (when `--kilocode` is active and environment looks like Kilo):
  - Effective mode: **Ask / Architect** (never Code for write operations)
  - Enforce **Orchestrator-per-check** for internal reasoning only:
    - For each top-level check (NFR, tasks, env/config, compat, UI, duplication):
      1) Switch to Orchestrator.
      2) Decompose into sub-checks as needed.
      3) Analyze artifacts in Code-mode read-only.
      4) Return a summarized result to Orchestrator.
  - Write guard stays **NO-WRITE** at all times.

If `--kilocode` is passed but the platform **does not** look like Kilo:

- Treat `--kilocode` as a **safe no-op meta-flag**.
- Continue in a generic LLM mode.
- Emit a warning in the report summary header.

---

## 5) Flags

> หมายเหตุ: ไม่มีการลบหรือเปลี่ยนความหมาย flag เก่า เพราะ workflow นี้เป็นของใหม่ทั้งหมด

### 5.1 Scope selection

- `--spec-ids=<id1,id2,...>`
  - Comma-separated list of spec IDs to include.
  - **MUST** map to entries found in SPEC_INDEX.
  - If any ID is not found in SPEC_INDEX:
    - mark it as an error in the report header
    - do not silently invent or remap.

- `--include-dependencies`
  - When set, expand scope using registries + SPEC_INDEX:
    - include dependent specs (e.g. upstream APIs, shared models, shared UI components).
  - All resolved spec-ids must also exist in SPEC_INDEX.

- `--release-label=<string>`
  - Optional human-readable name for the release
    - e.g. `2025.12.08-prod`, `v1.3.0-rc1`.
  - Used in report filenames and headings.

### 5.2 Environment / configuration

- `--target-env=<env>`
  - e.g. `dev`, `staging`, `prod`.
  - Used to contextualize config checks and NFR expectations.

- `--env-config-paths="<glob1>;<glob2>;..."`
  - Optional semicolon-separated glob patterns for configuration files
    - e.g. `"config/*.yaml;infra/*.tf"`.

### 5.3 Multi-repo / registry / index

- `--workspace-roots="<path1>;<path2>;..."`
  - Roots where repos may live.

- `--repos-config=<path>`
  - Takes precedence over `--workspace-roots` when both provided.
  - Describes multi-repo layout and relationships.

- `--registry-dir=<path>`
  - Primary registry root.
  - Defaults to `.spec/registry/`.

- `--registry-roots="<path1>;<path2>;..."`
  - Supplemental registries (read-only) used for validation only.

- `--index=<path>` / `--specindex=<path>`
  - Optional overrides if SPEC_INDEX is not at canonical locations.

- `--safety-mode=<level>`
  - Values:
    - `normal` (default)
    - `strict`
  - `--strict` acts as a legacy alias for `--safety-mode=strict`.

  **Behavior:**

  - `normal`:
    - `READY_WITH_RISKS` allowed where risks are documented.
  - `strict` / `--strict`:
    - If any *critical* risk remains (e.g. missing critical NFR evidence,
      unresolved backward incompatibility, missing required migration):
      - the spec-level status MUST NOT be `READY`.
      - release-level status MUST reflect at least `READY_WITH_RISKS` or `BLOCKED`.

### 5.4 Kilo / subtasks

- `--kilocode`
  - Enables Kilo-aware behavior (Ask/Architect mode, Orchestrator-per-check) when
    environment indicates Kilo is available.
  - No change in write guard (still NO-WRITE).

- `--nosubtasks`
  - Opt-out from Orchestrator subtask decomposition:
    - still perform checks, but without auto splitting into sub-checks.

### 5.5 Output control

- `--report-format=<md|json>`
  - Default: `md`.

- `--report-dir=<path>`
  - Default: `.spec/reports/smartspec_release_readiness/`.
  - Must be under project-owned `.spec/` when possible.

- `--stdout-summary`
  - When set, print a concise summary to stdout (in addition to file report).

---

## 6) Canonical Folders & File Placement

This workflow MUST follow canonical SmartSpec folder rules:

1. **Index detection order** (read-only):
   1) `.spec/SPEC_INDEX.json` (canonical)
   2) `SPEC_INDEX.json` at repo root (legacy mirror)
   3) `.smartspec/SPEC_INDEX.json` (deprecated)
   4) `specs/SPEC_INDEX.json` (older layout)

2. **Registries**:
   - Primary: `.spec/registry/`
   - Supplemental: any paths from `--registry-roots` (read-only)

3. **Spec locations**:
   - `specs/<category>/<spec-id>/spec.md`
   - Companion files:
     - `tasks.md`
     - `ui.json` (for UI JSON-first projects)

4. **Reports**:
   - Default:
     - `.spec/reports/smartspec_release_readiness/<timestamp>_<release-label>.{md|json}`
   - MUST avoid defaulting to `.smartspec/` for new reports.

---

## 7) Weakness & Risk Check (Quality Gate for This Workflow)

Before treating this workflow as “done”, the LLM / implementer should verify:

1. **Flags and legacy aliases**
   - `--kilocode` is present and documented.
   - `--strict` is preserved as a legacy alias for `--safety-mode=strict`.
   - No existing cross-chain flags (index/registry/multi-repo) are repurposed.

2. **Mode instructions**
   - Role is clearly verification/governance.
   - Write guard is NO-WRITE, explicitly defined.
   - Kilo behavior does not switch into Code mode for writes.

3. **AI implementation drift**
   - Instructions emphasize:
     - reuse of registry-owned assets
     - no new APIs/models/policies for already-registered entities
     - no invention of new NFRs or removal of existing ones.

4. **Cross-repo duplication risks**
   - Release report includes a section:
     - “Shared assets reused vs duplicated” per spec-id.
   - Cross-repo duplication check is implemented (see section 11).

5. **Folder/file placement**
   - SPEC_INDEX, registries, specs, and reports follow canonical locations.

6. **UI governance clarity**
   - Report explicitly states:
     - whether each spec is JSON-first or inline UI
     - what is missing, if anything, for UI readiness
     - whether a project-level UI JSON opt-out is detected and respected.

7. **Data migration scope boundaries**
   - Readiness report only **checks for the presence and linkage** of migration
     requirements/tasks/artifacts.
   - It does not attempt to **design or execute** migrations (that is the job of
     `/smartspec_data_migration_governance`).

---

## 8) Legacy Flags Inventory

Since `/smartspec_release_readiness` is a new workflow, the inventory is:

- **Kept as-is**:
  - (none – new workflow)

- **Kept as legacy alias**:
  - `--strict` → alias for `--safety-mode=strict`.

- **New additive flags**:
  - `--spec-ids`
  - `--include-dependencies`
  - `--release-label`
  - `--target-env`
  - `--env-config-paths`
  - `--registry-dir`
  - `--registry-roots`
  - `--index`
  - `--specindex`
  - `--safety-mode`
  - `--report-format`
  - `--report-dir`
  - `--stdout-summary`
  - `--workspace-roots`
  - `--repos-config`
  - `--kilocode`
  - `--nosubtasks`

---

## 9) KiloCode Support (Meta-Flag)

### 9.1 Role-based semantics

As a verification/governance workflow:

- Accepts `--kilocode`.
- MUST NOT change its role (still verification).
- Effective mode: **Ask / Architect** under Kilo.
- Write guard: **NO-WRITE** (even under Kilo).

### 9.2 Orchestrator-per-check loop

When `--kilocode` is active **and** Kilo is available:

For each top-level check (per spec-id and at release level):

1. Switch to Orchestrator.
2. Request a sub-check breakdown:
   - e.g. `NFR` → `latency`, `throughput`, `error rate`, `availability`.
   - `compatibility` → `API`, `data model`, `migration presence`.
3. In Code mode (read-only), analyze artifacts for each sub-check.
4. Return to Orchestrator to aggregate a summary per category.
5. Combine all categories into a final status decision.

Subtasks are ON by default; `--nosubtasks` disables step 2.

### 9.3 Non-Kilo environments

If `--kilocode` is present but platform doesn’t look like Kilo:

- Treat `--kilocode` as a **no-op meta-flag**.
- Proceed in a generic LLM mode.
- Add a warning line in the report header, e.g.:
  - "Kilo not detected; `--kilocode` treated as no-op."

---

## 10) Inline Detection Rules

The workflow must *not* call any other workflow for detection. Instead:

1. **Environment hints**:
   - Look for platform/model names in system prompt or environment tags
     - e.g., mentions of "Kilo Code", "Claude Code", "Antigravity".

2. **Flag scanning**:
   - Inspect the current command line / prompt for:
     - `--kilocode`
     - other tool-specific flags if present.

3. **Safe behavior**:
   - If Kilo is likely:
     - enable Orchestrator-per-check loop (still NO-WRITE).
   - If unsure:
     - stay tool-agnostic.
     - mark uncertainty in the report header.

---

## 11) Multi-repo / Multi-registry Rules

1. **Index / discovery**:
   - Use `--repos-config` when provided as the primary description of
     multi-repo layout.
   - Fall back to `--workspace-roots` if `--repos-config` is absent.

2. **Registry precedence**:
   - Primary registry: `--registry-dir` (default `.spec/registry/`).
   - Supplemental registries: `--registry-roots` (read-only).

3. **Cross-repo anti-duplication**:
   - For each shared asset name/entity encountered in scope
     (API, data model, policy, UI component, critical section):
     - check all loaded registries.
     - if the release introduces a new implementation for a name that already
       exists in any registry:
       - mark this as a potential duplication risk in the report.
       - recommend reuse/refactor into the existing shared asset.

4. **Impact on status**:
   - Under `--safety-mode=normal`:
     - duplication risk may still result in `READY_WITH_RISKS`.
   - Under `--safety-mode=strict` / `--strict`:
     - severe duplication (e.g. duplicate core shared model or API) should
       push status to at least `READY_WITH_RISKS`, and may justify `BLOCKED`
       depending on severity and project policy.

5. **Report representation**:
   - For each spec-id:
     - list owning repo.
     - list cross-repo dependencies (from registries).
     - flag any suspected duplication.

---

## 12) UI Addendum (JSON-first vs Inline)

Even though this workflow does **not** generate or modify UI artifacts, it must
assess UI readiness in a way that is consistent with project-wide UI
governance.

### 12.1 Detecting UI mode per spec

For each spec-id in scope, the workflow MUST:

1. Determine UI mode:
   - **JSON-first UI** when:
     - a `ui.json` file exists alongside `spec.md` for that spec, or
     - SPEC_INDEX / project config explicitly marks the spec as JSON-first.
   - **Inline UI** when:
     - no `ui.json` is present and
     - the UI is only described in `spec.md`.

2. Respect project-level **UI JSON opt-out** if present:
   - If SPEC_INDEX or project config declares that the project (or a spec
     family) has opted out of JSON-first UI separation, the workflow MUST:
     - treat that as the source of truth.
     - NOT mark the absence of `ui.json` as a defect by itself.
   - If no explicit opt-out is found:
     - apply the default SmartSpec guidance (JSON-first for UI-heavy specs),
       but only as a **governance recommendation**, not as a hard failure.

### 12.2 Readiness checks for JSON-first specs

For specs classified as JSON-first UI, the report should check (read-only):

- that `ui.json` exists and is parseable.
- that tasks include (and ideally mark complete):
  - creation or update of `ui.json` for this release scope.
  - mapping between `ui.json` components and any
    `ui-component-registry.json` entries (if present).
  - clear separation of concerns:
    - no business logic embedded in `ui.json`.
- any mismatches between `ui.json` and `spec.md` UI description.

Missing or outdated `ui.json` should usually be treated as at least a
`READY_WITH_RISKS` indicator for UI, and under `--safety-mode=strict` may
contribute to `BLOCKED` depending on project policy.

### 12.3 Readiness checks for inline UI specs

For specs classified as inline UI:

- confirm that `spec.md` describes:
  - main flows and states.
  - key components and interactions.
  - relevant accessibility or UX constraints (if any).
- confirm that tasks include reasonable UI implementation and validation
  steps (even if not JSON-first).

If inline UI is used despite a project-level JSON-first expectation, the
workflow should:

- mark this as a governance risk;
- recommend alignment (migrating to `ui.json`) in the **recommendations**
  section, without blocking the release *unless* project policy or
`safety-mode=strict` demands it.

### 12.4 Reporting format

For each spec-id, the UI section of the report should include:

- UI mode: `json-first` | `inline` | `unknown`.
- Project UI opt-out: `true` | `false` | `not-detected`.
- Key UI risks (if any) and their linkage to tasks.
- A clear statement whether UI issues contribute to:
  - `READY_WITH_RISKS` or
  - `BLOCKED` (under strict mode or per project rules).

---

## 13) Best Practices

- **Always run task verification first**
  - Run `smartspec_verify_tasks_progress` or equivalent before this workflow,
    so tasks completion evidence is up to date.

- **Anchor everything to SPEC_INDEX and registries**
  - Never guess spec-ids from file paths alone.
  - Never introduce new shared assets (APIs/models/policies/UI components) in
    this workflow; only reference those defined in registries.

- **Use `--release-label` consistently**
  - Align `--release-label` across code tags, deployment pipelines, and this
    report to make traceability and incident analysis easier.

- **Prefer `--repos-config` in multi-repo programs**
  - Use `--repos-config` to describe multi-repo layout and ownership rather
    than relying solely on `--workspace-roots`.

- **Treat `--safety-mode=strict` as a real gate**
  - In strict mode, avoid downgrading serious issues to minor risks.
  - Be explicit when strict mode is causing a `READY` → `READY_WITH_RISKS`
    or `BLOCKED` transition.

- **Separate proposals from readiness facts**
  - Any proposals (e.g., new NFRs or future enhancements) must be clearly
    labeled as such and must not be mixed with the readiness verdict.

- **Store reports as artifacts**
  - Commit reports or attach them to CI/CD artifacts to keep an audit trail
    for releases and production incidents.

---

## 14) For the LLM / Step-by-Step Flow & Stop Conditions

This section describes how an LLM-backed implementation should execute the
workflow while honoring SmartSpec governance constraints.

### 14.1 Step-by-step flow

1. **Resolve scope**
   - Read flags (`--spec-ids`, `--include-dependencies`, `--release-label`).
   - Load SPEC_INDEX using canonical detection order.
   - Validate that every `--spec-ids` entry is present in SPEC_INDEX.
   - If `--include-dependencies` is set, expand spec-ids using registries and
     SPEC_INDEX.
   - If scope **cannot** be resolved without guessing (e.g., no spec-ids,
     no clear mapping from branch/changes):
     - do **not** invent spec-ids.
     - in Ask/Architect mode, request clarification from the caller.

2. **Gather artifacts**
   - For each spec-id in scope:
     - load `spec.md`, `tasks.md`, optional `ui.json`.
     - load relevant registry entries:
       - APIs, data models, critical sections, UI components, ownership.
   - Load any environment/config files from `--env-config-paths`.

3. **Evaluate readiness dimensions per spec-id**

   For each spec-id, evaluate the following categories **without inventing
   new requirements**:

   a. **NFRs vs evidence**
   - Extract NFRs from `spec.md` and/or SPEC_INDEX.
   - Do not invent new NFRs or change thresholds; only summarize.
   - Check for evidence of tests or measurements (unit/integration/perf).
   - Classify NFR-related risks as:
     - none / low / medium / critical.

   b. **Tasks completion**
   - Summarize from `tasks.md` which tasks are complete vs pending.
   - Pay special attention to tasks related to:
     - tests
     - documentation
     - security
     - data migration
     - ops/observability
     - UI.

   c. **Environment/configuration**
   - Using `--target-env` and any loaded configs, identify:
     - missing configs
     - conflicting values
     - environment-specific assumptions.

   d. **Backward compatibility & migrations**
   - Use registries to check for:
     - breaking API or data model changes.
   - Determine whether migration requirements/tasks exist where they should.
   - Only **check** for the existence and linkage of migration artifacts;
     do not attempt to design or execute migrations.

   e. **Cross-repo duplication**
   - Check for duplicate implementations of shared assets using registries
     (see section 11).

   f. **UI governance**
   - Apply section 12 to determine UI mode, opt-out status, and UI risks.

4. **Assign status per spec-id**

   For each spec-id, assign one of:

   - `READY`
   - `READY_WITH_RISKS`
   - `BLOCKED`

   using the following minimal rules:

   - A spec **MUST NOT** be `READY` if any of the following holds:
     - a critical NFR has no evidence at all.
     - there is a known breaking API/data contract change **without** a
       documented migration/compat plan and tasks.
     - required environment/config for `--target-env` is missing.
   - Under `--safety-mode=strict` / `--strict`:
     - any critical risk (NFR, compat, migration, security, or severe
       duplication) forces the status to at least `READY_WITH_RISKS` or
       `BLOCKED`.

5. **Aggregate release-level summary**

   - Roll up all spec-level statuses into a release-level status.
   - List:
     - blocking items
     - critical and high risks by category.
   - Note explicitly if strict mode influenced the decision.

6. **Write report**

   - Serialize the full findings into `.md` or `.json` under
     `.spec/reports/smartspec_release_readiness/` (or `--report-dir`).
   - Include a human-readable summary and a structured section per spec-id.

7. **Optional stdout summary**

   - If `--stdout-summary` is set, print a short release summary:
     - overall status
     - count of specs by status
     - count of critical risks
     - pointer to the report file.

### 14.2 Stop conditions

The workflow MUST stop after:

- the report file is written (or would be written, in dry-run simulation), and
- any optional stdout summary is emitted.

It MUST NOT:

- modify any code or specs or tasks
- toggle task checkboxes
- create or modify registry entries
- call other workflows (it may only **recommend** them in its output).

