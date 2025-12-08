---
name: /smartspec_ci_quality_gate
version: 5.6.2
role: quality/governance
write_guard: NO-WRITE
purpose: Derive a CI matrix and unified quality gates from SmartSpec specs,
         tasks, and registries, and output a CI plan + suggested checks
         without modifying pipelines directly.
---

## 1) Summary

`/smartspec_ci_quality_gate` reads SmartSpec artifacts (SPEC_INDEX, specs,
 tasks, registries) and generates a **CI plan + quality gate definition**.

It focuses on:

- deriving a **CI matrix** from specs/tasks (per spec, per service, per repo)
- enforcing unified quality gates across teams for:
  - lint/static analysis
  - unit/integration/contract tests
  - coverage thresholds
  - optional performance / security / UI checks
- ensuring **contract tests and shared registries are respected** so CI does
  not allow regressions that break shared APIs/models/policies.

The workflow is:

- **read-only** (NO-WRITE): it does *not* edit CI YAML or code
- responsible for producing **plans and configuration suggestions**, not for
  applying them

Use it as the **bridge between SmartSpec-world and CI/CD systems**, so that
quality checks in pipelines stay aligned with what the specs/tasks expect.

---

## 2) When to Use

Use `/smartspec_ci_quality_gate` when:

- you want to standardize CI quality gates across repos/teams based on
  SmartSpec specs and tasks
- you have tests being generated (`smartspec_generate_tests`) and run in CI,
  but want a **single source of truth** for which checks must pass
- you are introducing new services/specs and want to bootstrap CI configuration
  from day one

Typical position in the chain (execution-first stability path):

`generate_spec → generate_plan → generate_tasks → sync_spec_tasks → implement_tasks → generate_tests → verify_tasks_progress → /smartspec_ci_quality_gate`

Do **not** use this workflow to:

- directly write or modify CI files (GitHub Actions, GitLab CI, etc.)
- substitute test generation (`smartspec_generate_tests`)
- replace release-level decisions (use `/smartspec_release_readiness` for
  pre-deploy gates)

Instead, treat the outputs as **inputs to your CI system** that humans or
separate tooling can apply.

---

## 3) Inputs / Outputs

### 3.1 Inputs (artifacts)

Read-only artifacts:

- **Index**
  - `.spec/SPEC_INDEX.json` (canonical)
  - `SPEC_INDEX.json` at repo root (legacy mirror)
  - `.smartspec/SPEC_INDEX.json` (deprecated)
  - `specs/SPEC_INDEX.json` (older layout)

- **Specs & tasks for each spec-id in scope**
  - `specs/<category>/<spec-id>/spec.md`
  - `specs/<category>/<spec-id>/tasks.md`

- **Registries (if present)**
  - `.spec/registry/api-registry.json`
  - `.spec/registry/data-model-registry.json`
  - `.spec/registry/glossary.json`
  - `.spec/registry/critical-sections-registry.json`
  - `.spec/registry/ui-component-registry.json`
  - `.spec/registry/file-ownership-registry.json`

- **Existing CI configs (read-only, optional)**
  - whatever matches `--ci-config-paths` (e.g. `.github/workflows/*.yml`,
    `.gitlab-ci.yml`, `.azure-pipelines/*.yml`)

- **Test result paths (optional)**
  - any reports referenced via `--test-report-paths` to detect existing
    test categories & coverage

### 3.2 Inputs (flags)

See section **5) Flags**.

### 3.3 Outputs

- **Primary CI plan file** (human-readable + structured)
  - Default location:
    - `.spec/ci/ci_quality_gate_<ci-label>.md`
  - If `--ci-output-format=json|yaml` is used, additional machine-friendly
    output:
    - `.spec/ci/ci_quality_gate_<ci-label>.{json|yaml}`

Contents:

- CI matrix structure, e.g.:
  - per spec-id
  - per service/repo
  - per environment (`dev`, `staging`, `prod`)
- Required check types per dimension:
  - lint/static analysis
  - unit tests
  - integration/contract tests
  - coverage thresholds
  - optional perf/security/UI checks
- Mapping from SmartSpec tasks to CI jobs/stages
- Recommended failure criteria per job and per pipeline
- **Separation of sections**:
  - `Required checks` – derived from specs/tasks/registries/baseline policy
  - `Proposed checks` – suggestions and improvements only
- Optional **CI-system-specific suggestions**, e.g. job names/stages for
  GitHub Actions, GitLab CI, Azure Pipelines, etc.

Optional **stdout summary** if `--stdout-summary` is set.

---

## 4) Modes

### 4.1 Role & write guard

- Role: **Quality / Governance**
- Default write guard: **NO-WRITE**

MUST NOT:

- modify CI YAML or pipeline configs directly
- modify code, specs, tasks, or registries

MAY:

- read CI configs to understand current coverage
- generate CI plan files under `.spec/ci/`
- print suggestions and summaries

### 4.2 Platform semantics

- Tool-agnostic by default.
- Under Kilo (when `--kilocode` is active and environment looks like Kilo):
  - Effective mode: **Ask / Architect**
  - Enforce **Orchestrator-per-dimension** for reasoning only:
    - For each CI dimension (lint, unit, integration, contract, coverage,
      perf, security, UI):
      1) Switch to Orchestrator.
      2) Decompose checks into sub-tasks.
      3) Analyze artifacts in Code mode (read-only).
      4) Return summarized CI requirements per dimension.
  - Write guard stays **NO-WRITE**.

If `--kilocode` is passed but the platform does not look like Kilo:

- Treat `--kilocode` as a **no-op meta-flag**.
- Continue in a generic LLM mode.
- Emit a warning in the CI plan header.

---

## 5) Flags

> No existing flags are removed or repurposed. All additions are additive.

### 5.1 Scope & label

- `--spec-ids=<id1,id2,...>`
  - Comma-separated spec IDs.
  - All IDs **must** exist in SPEC_INDEX.

- `--include-dependencies`
  - Expand scope via registries + SPEC_INDEX to include dependent specs
    (upstream APIs, shared models, shared UI components, etc.).

- `--ci-label=<string>`
  - Human-readable label used in output filenames and headings.
  - e.g., `monorepo-main`, `payments-pipeline`, `2025.12.09-ci`.

### 5.2 CI environment & system

- `--target-envs="<env1>,<env2>,..."`
  - e.g., `dev,staging,prod`.
  - Controls which environments are represented in the CI matrix.

- `--ci-system=<github_actions|gitlab_ci|azure_pipelines|circleci|generic>`
  - Defines which CI system to tailor suggestions for.
  - `generic` = system-agnostic description.

- `--ci-config-paths="<glob1>;<glob2>;..."`
  - Optional locations of existing CI configuration files.
  - Used only for **reading** current CI setup and mapping.

- `--test-report-paths="<glob1>;<glob2>;..."`
  - Optional locations of existing test reports/coverage reports.
  - Used to understand current coverage and adjust recommendations.

### 5.3 Multi-repo / registry / index

- `--workspace-roots="<path1>;<path2>;..."`
- `--repos-config=<path>`
- `--registry-dir=<path>`
- `--registry-roots="<path1>;<path2>;..."`
- `--index=<path>` / `--specindex=<path>`
- `--safety-mode=<normal|strict>`
  - `--strict` as legacy alias for `--safety-mode=strict`.

Semantics:

- `--repos-config` preferred for precise multi-repo topology.
- `--workspace-roots` used as fallback when `--repos-config` is absent.
- `--registry-dir` is the primary registry root (default `.spec/registry`).
- `--registry-roots` are read-only supplemental registries.

**Safety mode behavior:**

- `normal` (default):
  - Missing or weak CI checks are recorded as **recommendations** or
    non-blocking gaps in the plan.

- `strict` / `--strict`:
  - Any **critical** CI gap must be promoted to a required gate in the plan,
    for example:
    - a test type (unit/integration/contract/security/perf) mentioned in
      specs/tasks that has no CI job at all.
    - coverage thresholds defined in specs/org policy that are lower in
      current CI configs.
    - changes to shared APIs/models without a contract test requirement.
  - The plan must clearly mark these as **must-add or must-fix** checks,
    not just optional suggestions.

### 5.4 Kilo / subtasks

- `--kilocode`
  - Enables Kilo-aware behavior (Ask/Architect + Orchestrator-per-dimension).

- `--nosubtasks`
  - Disables automatic subtask decomposition under Orchestrator.

### 5.5 Output control

- `--ci-output-format=<md|json|yaml>`
  - Default: `md`.

- `--ci-output-dir=<path>`
  - Default: `.spec/ci/`.

- `--stdout-summary`
  - Prints a brief CI matrix summary to stdout.

---

## 6) Canonical Folders & File Placement

The workflow MUST obey SmartSpec canonical folder rules:

1. **Index detection order**:
   1) `.spec/SPEC_INDEX.json` (canonical)
   2) `SPEC_INDEX.json` at repo root (legacy mirror)
   3) `.smartspec/SPEC_INDEX.json` (deprecated)
   4) `specs/SPEC_INDEX.json` (older layout)

2. **Registries**:
   - Primary: `.spec/registry/`
   - Supplemental: from `--registry-roots` (read-only)

3. **Specs**:
   - `specs/<category>/<spec-id>/spec.md`
   - `specs/<category>/<spec-id>/tasks.md`

4. **CI plan outputs**:
   - Default:
     - `.spec/ci/ci_quality_gate_<ci-label>.{md|json|yaml}`
   - Must **not** create new top-level folders outside `.spec/` for CI plans
     by default.

---

## 7) Weakness & Risk Check (Quality Gate for This Workflow)

Before treating this workflow spec as complete, verify:

1. **Write guard**
   - It is clearly NO-WRITE.
   - It prohibits direct modification of CI configs, specs, tasks, and
     registries.

2. **Flag safety**
   - `--kilocode` is supported.
   - Multi-repo flags are consistent with other workflows.
   - `--strict` is an alias for `--safety-mode=strict` only.

3. **AI drift prevention**
   - CI requirements must be derived from:
     - specs, tasks, registries, baseline CI policy, and (optionally)
       existing CI/test artifacts.
   - The workflow must **not** invent entirely new quality policies that are
     inconsistent with spec/registry ownership.
   - Any new recommendations must appear in the `Proposed checks` section
     and be clearly labeled as proposals.

4. **Cross-repo alignment**
   - Shared assets (APIs, models, policies, UI components) are validated
     against registries when defining contract test requirements.
   - Where ownership is defined (e.g., via `file-ownership-registry`), the
     CI plan identifies which repo/pipeline is the **primary CI owner** for
     each shared asset, and which pipelines only need lighter checks.

5. **Scope clarity**
   - The workflow does not guess spec-ids outside SPEC_INDEX.
   - When mapping CI jobs to specs, it uses explicit mappings (from
     SPEC_INDEX, repos-config, naming conventions documented by the team)
     rather than pure string similarity. Unmapped jobs are listed as
     `unmapped_ci_jobs` instead of being forced into the matrix.

6. **UI governance awareness**
   - When UI tests are part of the CI matrix, they reflect the current UI
     governance mode (JSON-first vs inline, with UI JSON opt-out respected)
     instead of enforcing one pattern unconditionally.

7. **Alignment with release readiness**
   - CI gates defined here produce the kinds of evidence that
     `/smartspec_release_readiness` expects (e.g., NFR/perf tests,
     contract tests, coverage reports).
   - Critical gaps in CI must correspond to potential critical risks at
     release readiness time.

---

## 8) Legacy Flags Inventory

New workflow; legacy inventory is:

- **Kept as-is**:
  - (none)

- **Kept as legacy alias**:
  - `--strict` → alias for `--safety-mode=strict`.

- **New additive flags**:
  - `--spec-ids`
  - `--include-dependencies`
  - `--ci-label`
  - `--target-envs`
  - `--ci-system`
  - `--ci-config-paths`
  - `--test-report-paths`
  - `--workspace-roots`
  - `--repos-config`
  - `--registry-dir`
  - `--registry-roots`
  - `--index`
  - `--specindex`
  - `--safety-mode`
  - `--ci-output-format`
  - `--ci-output-dir`
  - `--stdout-summary`
  - `--kilocode`
  - `--nosubtasks`

---

## 9) KiloCode Support (Meta-Flag)

### 9.1 Role-based semantics

As a quality/governance workflow:

- Accepts `--kilocode`.
- Must stay in **Ask / Architect** mode, not Code-for-write.
- Write guard stays NO-WRITE.

### 9.2 Orchestrator-per-dimension loop

With `--kilocode` active and Kilo detected:

For each CI dimension (e.g. lint, unit, integration, contract, coverage,
perf, security, UI):

1. Orchestrator plans sub-checks for that dimension.
2. Code mode (read-only) inspects specs, tasks, registries, and existing
   CI/test artifacts for that dimension.
3. Orchestrator aggregates findings into normalized CI requirements.
4. Tag each requirement as `Required` or `Proposed`.
5. Repeat for the next dimension.

`--nosubtasks` disables step 1 while still allowing the rest of the logic.

### 9.3 Non-Kilo environments

If Kilo is not detected:

- Treat `--kilocode` as a no-op.
- Continue with a single-step reasoning flow.

---

## 10) Inline Detection Rules

This workflow must not call other workflows for detection. It should:

1. Inspect system prompt / environment metadata for platform hints, including
   references to Kilo/Claude Code/Antigravity.

2. Inspect command line / invocation text for `--kilocode` or other
   environment-specific flags.

3. When signals are ambiguous, prefer **safe, tool-agnostic behavior** and
   document uncertainty in the CI plan header.

---

## 11) Multi-repo / Multi-registry Rules

1. Use `--repos-config` when available to map spec-ids to repos and services.

2. Use `--workspace-roots` when `--repos-config` is absent to discover repos,
   but do not guess spec-ids outside SPEC_INDEX.

3. Treat `--registry-dir` as the primary registry root; treat
   `--registry-roots` as read-only supplements.

4. When defining **contract tests** in the CI matrix:
   - Use API/data-model registries to:
     - identify shared interfaces
     - ensure there is at least one CI job requiring their contract tests.
   - Use file-ownership or explicit ownership metadata (when available) to
     identify which repo/pipeline is the **primary CI gate** for each shared
     asset. Other pipelines may only need smoke or minimal checks.

5. If a spec introduces changes to a shared asset without a corresponding
   contract test requirement:
   - Mark this as a CI gating risk.
   - Under `--safety-mode=strict`, require adding such tests before CI passes
     the gate for that spec.

6. When the CI matrix implies duplicated heavy checks (e.g., full contract
   suites) across many repos, prefer centralizing them under the owner
   pipeline and using lighter verification elsewhere.

---

## 12) UI Addendum (CI-level UI Checks)

When UI is part of the system, CI quality gates may include UI-specific
checks. This workflow should:

1. Determine UI mode per spec (JSON-first vs inline) using:
   - presence of `ui.json` next to `spec.md`, and/or
   - fields in SPEC_INDEX or project config declaring UI mode.

2. Respect project-level **UI JSON opt-out**:
   - If SPEC_INDEX or project config declares that the project or spec family
     has opted out of JSON-first UI separation, the plan must:
     - not require `ui.json`-specific validation jobs as hard gates.
     - still recommend UI tests appropriate to inline UI.

3. For JSON-first UI specs:
   - Suggest CI jobs for:
     - validating `ui.json` structure and schema.
     - running UI snapshot/visual regression tests where applicable.
     - ensuring UI component usage stays aligned with `ui-component-registry`
       (if present).

4. For inline UI specs:
   - Suggest UI tests appropriate to that style (e.g., end-to-end flows using
     documented screens/components) without forcing JSON-first adoption.

5. In strict mode and under explicit JSON-first policy:
   - Missing `ui.json` validation in CI should be treated as a required
     addition to the CI plan.

---

## 13) Baseline CI Dimensions by Spec Type

To avoid under-specifying CI requirements when specs/tasks are weak, the
workflow defines minimal CI dimensions per spec type. Spec type may be
inferred from SPEC_INDEX, spec category, or project config.

Examples (non-exhaustive, to be refined per program):

- **API/service specs** (e.g., category `api/` or `service/`):
  - Required dimensions:
    - lint/static analysis
    - unit tests
    - integration tests (service-level)
    - contract tests for exposed APIs
    - coverage threshold (per project policy)

- **Library/shared model specs** (e.g., `lib/`, `shared/`):
  - Required dimensions:
    - lint/static analysis
    - unit tests
    - contract tests where libraries define shared schemas or behaviors

- **Infra/config specs** (e.g., `infra/`, `ops/`):
  - Required dimensions:
    - config/infra linting
    - basic integration validation (e.g., terraform plan validation, schema
      checks)

Under `--safety-mode=normal`:

- Missing baseline dimensions should be flagged as recommendations.

Under `--safety-mode=strict`:

- Missing baseline dimensions must be raised as required CI gates for the
  affected specs.

---

## 14) Best Practices (for Users)

- Always run this workflow **after** tests are generated and tasks are in a
  reasonably up-to-date state.

- Provide `--spec-ids` explicitly rather than relying on heuristics.

- Use `--ci-system` to get suggestions tailored to your CI provider.

- Treat `--safety-mode=strict` as the default in production CI pipelines.

- Version control the generated CI plan files or store them as CI artifacts
  for traceability.

- Align the CI plan’s job names and stages with your existing pipelines to
  minimize confusion.

- Make sure CI plans and release readiness reports are reviewed together,
  so that CI evidence matches release gating expectations.

---

## 15) For the LLM / Step-by-Step Flow & Stop Conditions

### 15.1 Step-by-step flow

1. **Resolve scope**
   - Parse `--spec-ids`, `--include-dependencies`, `--ci-label`, and
     `--target-envs`.
   - Load SPEC_INDEX via canonical order.
   - Validate that all `--spec-ids` exist in SPEC_INDEX.
   - Expand to include dependencies if requested.
   - If scope cannot be resolved without guessing, do not invent spec-ids;
     ask for clarification instead (Ask mode) or stop with a clear message.

2. **Gather artifacts**
   - Load specs and tasks for all spec-ids in scope.
   - Load registries from `--registry-dir` and `--registry-roots`.
   - Optionally read CI configs and test reports from configured paths.

3. **Determine spec types and baseline CI dimensions**
   - Infer spec types (API, service, library, infra, etc.) from SPEC_INDEX,
     categories, or project config.
   - Attach baseline CI dimensions per spec type (see section 13).

4. **Derive CI requirements per spec-id**
   For each spec-id, map to:
   - required test types based on:
     - tasks (e.g., explicit unit/integration/contract test tasks)
     - registries (e.g., shared APIs/models requiring contract tests)
     - baseline CI dimensions for its spec type.
   - required static analysis/linting steps.
   - minimum coverage expectations (from specs/org policy, where available).
   - environment-specific gates for `--target-envs`.

5. **Map against existing CI configs (if any)**
   - Use explicit mappings from SPEC_INDEX/repos-config to relate specs to
     CI jobs.
   - Do not guess spec-job mappings purely via fuzzy string matching.
   - List any CI jobs that cannot be mapped as `unmapped_ci_jobs`.

6. **Apply safety mode**
   - Under `normal`, mark missing checks as recommendations.
   - Under `strict`, mark missing critical/baseline checks as required gates.

7. **Construct CI matrix**
   - Group spec-level requirements into:
     - per-repo / per-service views
     - per-environment views
   - If `--ci-system` is set, express them in that system’s mental model
     (jobs/stages/workflows).
   - Separate output sections into `Required checks` and `Proposed checks`.

8. **Generate plan files**
   - Write the CI plan to
     `.spec/ci/ci_quality_gate_<ci-label>.{md|json|yaml}` according to
     output flags.
   - Plan should contain both human narrative and structured sections.

9. **Optional stdout summary**
   - If `--stdout-summary` is set, print:
     - number of specs in scope
     - CI systems targeted
     - key required check types
     - pointer to the plan file.

### 15.2 Stop conditions

The workflow MUST stop after:

- CI plan file(s) are written (or would be written in dry-run) and
- optional stdout summary is emitted.

It MUST NOT:

- modify CI configuration files
- modify code, specs, tasks, or registries
- invoke other workflows directly (only recommend them in narrative text).

