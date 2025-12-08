---
manual_name: /smartspec_ci_quality_gate Manual (EN)
manual_version: 5.6
compatible_workflow: /smartspec_ci_quality_gate
compatible_workflow_versions: 5.6.2 – 5.6.x
role: user/operator manual (release managers, tech leads, senior ICs)
---

# /smartspec_ci_quality_gate Manual (v5.6, English)

## 1. Overview

This manual explains **how to use** the workflow:

> `/smartspec_ci_quality_gate v5.6.2`

The workflow answers questions like:

> “Given our SmartSpec specs/tasks/registries, does our **CI pipeline** have
> the right checks and gates? What’s missing? What should the CI matrix
> look like?”

Key characteristics:

- **quality / governance** workflow (not an executor)
- `write_guard: NO-WRITE`:
  - does **not** modify CI YAML, code, specs, or tasks
  - only **reads** artifacts and produces a **CI plan + quality gate
    definition**
  - writes plan files under `.spec/ci/`

Primary goal:

- build a **CI matrix** aligned with SmartSpec
- define **minimum quality gates** per spec type
- ensure CI evidence lines up with what `/smartspec_release_readiness`
  expects at pre-release time

---

## 2. What’s New in v5.6

Workflow version **5.6.2** introduces the following refinements:

### 2.1 Strict mode with real behavioral impact

- `--safety-mode=strict` (or `--strict`) now means:
  - any test type (unit/integration/contract/security/perf) mentioned in
    specs/tasks that has **no CI job at all** must be a **required gate**
  - coverage thresholds defined in specs/org policy must not be reduced in
    the CI plan
  - changes to shared APIs/models without contract tests are treated as CI
    gating risks in the `Required checks` section, not merely suggestions

### 2.2 Clear split between Required and Proposed checks

The CI plan output is explicitly split into:

- `Required checks` – derived from:
  - specs
  - tasks
  - registries
  - baseline CI policy per spec type
- `Proposed checks` – optional improvements, hardening, or future ideas

This prevents proposals from being misinterpreted as hard requirements.

### 2.3 Cross-repo & shared assets with CI owner

- Uses registries (including `file-ownership-registry` when available) to
  identify **CI owners** for shared assets (shared APIs/models/policies).
- Other pipelines that **use** those shared assets are recommended to run
  lighter checks (e.g., smoke), avoiding duplicated heavy contract suites
  everywhere.

### 2.4 UI governance + UI JSON opt-out

- Differentiates JSON-first UI vs inline UI using:
  - presence of `ui.json` next to `spec.md`
  - SPEC_INDEX or project config fields
- When there is a **UI JSON opt-out** for a project or spec family:
  - CI plans do **not** require `ui.json`-specific validation as a hard gate
  - they still recommend appropriate UI tests for inline UI

### 2.5 Baseline CI dimensions per spec type

To avoid under-specified CI matrices when specs/tasks are weak, the workflow
adds **baseline dimensions** per inferred spec type, e.g.:

- API/service → lint + unit + integration + contract + coverage
- library/shared model → lint + unit + contract
- infra/config → infra lint + validation

- `normal` mode: missing baseline → recommendations
- `strict` mode: missing baseline → required gates

### 2.6 Alignment with `/smartspec_release_readiness`

- CI plans from this workflow are designed to be the **primary evidence
  source** for `/smartspec_release_readiness`.
- Critical CI gaps correspond to potential critical risks during
  release readiness assessment.

---

## 3. Backward Compatibility Notes

- This manual v5.6 applies to `/smartspec_ci_quality_gate` starting from
  **5.6.2**.
- The workflow is new as a CI quality gate; there is no older CI-gate manual
  to migrate from.

Inherited core rules:

- never modify code, specs, tasks, registries, or CI configs (NO-WRITE)
- use multi-repo flags (`--workspace-roots`, `--repos-config`,
  `--registry-dir`, `--registry-roots`, `--index`, `--specindex`) consistent
  with other workflows
- support `--kilocode` with Ask/Architect + Orchestrator-per-dimension

Patch-level updates (5.6.3, 5.6.4, …) that do not alter flag/mode semantics
remain compatible with this manual.

---

## 4. Core Concepts

### 4.1 CI matrix from a SmartSpec perspective

Each spec-id has its own quality requirements:

- which types of tests are expected (unit/integration/contract/etc.)
- what coverage levels are needed
- whether security/perf/UI checks are relevant

The workflow reads from:

- `spec.md`
- `tasks.md`
- registries
- baseline policy per spec type

and summarizes them into a **CI matrix** mapping:

- specs → jobs
- jobs → stages
- stages → gates across `dev` / `staging` / `prod` (or custom envs)

### 4.2 Evidence the workflow uses

- SPEC_INDEX (canonical `.spec/SPEC_INDEX.json`)
- specs and tasks for all spec-ids in scope
- registries (API/data-model/UI/etc.)
- existing CI configs (if `--ci-config-paths` is provided)
- test/coverage reports (if `--test-report-paths` is provided)

### 4.3 Scope = set of spec-ids

- Use `--spec-ids=<id1,id2,...>` to define scope
- Optionally expand via `--include-dependencies` using SPEC_INDEX + registries
- The workflow must **not guess spec-ids** outside SPEC_INDEX

### 4.4 Spec type & baseline dimensions

The workflow infers `spec type` (API/service, library/shared, infra/config,
…) from SPEC_INDEX/category/project config and uses baselines so matrices
are not “too thin” when specs/tasks are under-specified.

---

## 5. Quick Start

### 5.1 Single repo, basic CI plan

```bash
smartspec_ci_quality_gate \
  --spec-ids=checkout_api,order_core \
  --ci-label=monorepo-main \
  --target-envs=dev,staging,prod \
  --ci-system=github_actions \
  --ci-output-format=md \
  --stdout-summary
```

Result:

- `.spec/ci/ci_quality_gate_monorepo-main.md`
- a matrix for each environment with jobs for lint/unit/integration/contract
  and coverage gates as required.

### 5.2 Strict mode for production pipeline

```bash
smartspec_ci_quality_gate \
  --spec-ids=payments_gateway \
  --ci-label=payments-prod-ci \
  --target-envs=prod \
  --ci-system=gitlab_ci \
  --safety-mode=strict \
  --stdout-summary
```

With `strict`:

- any requested contract tests missing from CI → required gate in the plan
- coverage below policy → required improvement

### 5.3 Multi-repo with shared registry

```bash
smartspec_ci_quality_gate \
  --spec-ids=teamA_payments,teamB_notifications \
  --ci-label=multi-team-ci \
  --target-envs=staging,prod \
  --repos-config=.spec/repos.yaml \
  --registry-dir=.spec/registry \
  --registry-roots="../platform/.spec/registry" \
  --ci-system=generic \
  --ci-output-format=yaml
```

Here the plan will:

- map each spec to its owning repo/service
- use platform registries to identify shared APIs/models
- highlight which pipeline is the CI owner for each shared asset

---

## 6. CLI / Flags Cheat Sheet

> For day-to-day usage; see workflow spec for deeper semantics.

### 6.1 Scope & label

- `--spec-ids=<id1,id2,...>`
- `--include-dependencies`
- `--ci-label=<string>`

### 6.2 CI environment & system

- `--target-envs="dev,staging,prod"`
- `--ci-system=github_actions|gitlab_ci|azure_pipelines|circleci|generic`
- `--ci-config-paths=".github/workflows/*.yml;ci/*.yaml"`
- `--test-report-paths="reports/tests/*.xml;coverage/*.json"`

### 6.3 Multi-repo & registry

- `--workspace-roots`
- `--repos-config`
- `--registry-dir`
- `--registry-roots`
- `--index`, `--specindex`

### 6.4 Safety / kilocode / output

- `--safety-mode=normal|strict` (or `--strict`)
- `--kilocode`, `--nosubtasks`
- `--ci-output-format=md|json|yaml`
- `--ci-output-dir=.spec/ci`
- `--stdout-summary`

---

## 7. How Required vs Proposed Checks Are Decided

### 7.1 Sources of Required checks

A CI requirement is considered **Required** if it is derived from:

- `spec.md` or `tasks.md` (explicitly)
- registries (e.g., contract tests for shared API X)
- baseline CI dimensions for the spec type
- clearly defined org-level policy encoded in SPEC_INDEX/config

### 7.2 Normal vs Strict mode

- `normal`:
  - missing test types or baselines → recorded as recommendations under
    `Proposed checks`.

- `strict`:
  - missing test types that are requested by specs/registries/baselines →
    must be marked as **required gates**.
  - coverage below policy → required improvement.
  - missing contract tests for changed shared assets → CI gating risk in
    `Required checks`.

---

## 8. KiloCode Usage Examples

### 8.1 Governance mode on Kilo

```bash
smartspec_ci_quality_gate \
  --spec-ids=billing_core \
  --ci-label=billing-ci \
  --target-envs=dev,prod \
  --kilocode \
  --safety-mode=strict \
  --stdout-summary
```

With Kilo:

- Orchestrator breaks down CI dimensions (lint/unit/integration/contract,...)
- Code mode inspects artifacts read-only per dimension
- Orchestrator recombines them into a CI plan
- No writes are performed anywhere

### 8.2 Disabling subtasks

```bash
smartspec_ci_quality_gate \
  --spec-ids=small_feature \
  --ci-label=small-ci \
  --target-envs=staging \
  --kilocode \
  --nosubtasks
```

- Still Kilo-aware, but skips auto subtask decomposition, useful for small
  scopes.

---

## 9. Multi-repo / Multi-registry Usage Examples

### 9.1 Monorepo + platform registry

```bash
smartspec_ci_quality_gate \
  --spec-ids=search_api \
  --ci-label=search-ci \
  --target-envs=dev,prod \
  --repos-config=.spec/repos.yaml \
  --registry-dir=.spec/registry \
  --registry-roots="../platform/.spec/registry" \
  --ci-system=github_actions
```

- `repos-config` maps specs to services/jobs
- platform registry identifies shared APIs/models that require contract tests

### 9.2 Multiple teams & repos

```bash
smartspec_ci_quality_gate \
  --spec-ids=teamA_payments,teamB_notifications \
  --ci-label=multi-team-ci \
  --target-envs=prod \
  --workspace-roots="../teamA;../teamB" \
  --registry-dir=../platform/.spec/registry \
  --safety-mode=strict
```

- The CI plan identifies CI owners for shared assets
- Other pipelines are recommended to run only minimal/smoke checks where
  appropriate

---

## 10. UI JSON vs Inline UI (from CI’s perspective)

### 10.1 JSON-first UI project

```bash
smartspec_ci_quality_gate \
  --spec-ids=web_checkout \
  --ci-label=web-checkout-ci \
  --target-envs=staging,prod \
  --ci-system=github_actions
```

If SPEC_INDEX/config signals JSON-first UI:

- the plan suggests jobs for:
  - `ui.json` validation (schema/structure)
  - visual regression/snapshot tests
  - alignment with `ui-component-registry`

In strict mode, missing these becomes a required gate.

### 10.2 Project opted out of JSON-first UI

```bash
smartspec_ci_quality_gate \
  --spec-ids=admin_portal \
  --ci-label=admin-ci \
  --target-envs=staging \
  --ci-system=generic
```

If SPEC_INDEX/config declares an opt-out:

- the plan does not treat the absence of `ui.json` jobs as failure
- it still suggests E2E/UI tests based on the flows/screens described in
  `spec.md`.

---

## 11. Best Practices & Anti-patterns

### 11.1 Best Practices

- Always specify `--spec-ids` explicitly.
- Align `--ci-label` with your real CI pipeline name.
- In multi-repo setups, prefer `--repos-config` over raw `--workspace-roots`.
- Use `--safety-mode=strict` for production pipelines.
- Version control CI plan files or store them as CI artifacts.
- Review CI plans alongside `/smartspec_release_readiness` reports.

### 11.2 Anti-patterns

- Letting the workflow guess scope or job↔spec mappings from names alone.
- Treating `READY_WITH_RISKS` or a matrix with obvious gaps as “good enough”
  without reading the details.
- Expecting the workflow to edit CI YAML for you.
- Duplicating heavy contract suites across many repos without a clear CI
  owner.

---

## 12. FAQ / Troubleshooting

### Q1: Why does the plan say we’re missing contract tests when we already have integration tests?

Because:

- integration tests validate end-to-end behavior of the system.
- contract tests focus on a specific interface/contract between producer and
  consumers (services or clients).

If a registry indicates that an API/model is a shared asset, the workflow
expects explicit contract tests for that asset.

### Q2: What if we don’t want strict gating yet?

- Use `--safety-mode=normal`.
- Many gaps will appear under `Proposed checks` rather than as required gates.
- Teams can then prioritize and phase in those proposals.

### Q3: Why do I see `unmapped_ci_jobs` in the plan?

Because:

- the workflow could not map those jobs to any spec-id using explicit
  mappings.
- You may:
  - add mapping info to SPEC_INDEX / repos-config.
  - or accept that these are legacy/utility jobs outside SmartSpec’s scope.

### Q4: Do we have to update CI YAML to match the plan exactly?

Not necessarily:

- `Required checks` are the parts you should align with specs/policy.
- `Proposed checks` can be treated as tech debt / future improvements.

### Q5: How often should we run `/smartspec_ci_quality_gate`?

Recommended:

- whenever new specs/services are added
- whenever org-level quality policy changes
- periodically (e.g., each quarter) to ensure CI stays aligned with specs.

---

End of `/smartspec_ci_quality_gate` Manual v5.6 (English).

If new features are added to the workflow (e.g. support for new artifact
types or significant changes to baseline/strict rules), issue a new manual
version (e.g. 5.7) with clear notes on compatible workflow versions.

