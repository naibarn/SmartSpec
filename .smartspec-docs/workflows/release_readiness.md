---
manual_name: /smartspec_release_readiness Manual (EN)
manual_version: 5.6
compatible_workflow: /smartspec_release_readiness
compatible_workflow_versions: 5.6.2 – 5.6.x
role: user/operator manual (release managers, tech leads, senior ICs)
---

# /smartspec_release_readiness Manual (v5.6, English)

## 1. Overview

This manual explains **how to use** the workflow:

> `/smartspec_release_readiness v5.6.2`

The workflow answers the question:

> “Is this release scope **actually ready** (from the perspective of specs,
> tasks, NFRs, compatibility, multi-repo, and UI), or are there still
> gaps and risks?”

This is a **verification / governance** workflow and is **100% NO-WRITE**:

- it does *not* modify code
- it does *not* edit specs or tasks
- it does *not* modify registries
- it **only** reads artifacts and produces a **release readiness report** under
  `.spec/reports/...`

Use it as the **final gate before deployment** or promotion to staging/
production in a SmartSpec-governed program.

---

## 2. What’s New in v5.6

This manual covers workflow version **v5.6.2**, which refines and clarifies the
original ideas from the coverage summary.

### 2.1 Clear criteria for READY / READY_WITH_RISKS / BLOCKED

The workflow now has explicit guidance for when a spec **must not** be marked
`READY`, for example:

- there is a breaking API/data contract change with **no** migration/compat
  plan and tasks
- a critical NFR (e.g., latency, availability, data loss) has **no evidence**
  at all
- critical configuration for `--target-env` is missing or undefined

Under `--safety-mode=strict`, these issues must at least result in
`READY_WITH_RISKS` or even `BLOCKED` for the affected spec and release.

### 2.2 Separation from Data Migration Governance

- `/smartspec_release_readiness`:
  - **checks** whether migration requirements, tasks, and artifacts exist and
    are linked to specs where they should be
  - counts missing migrations as a **risk or blocking condition**

- `/smartspec_data_migration_governance` (separate workflow):
  - is responsible for **designing and governing** how migrations are planned
    and executed

This workflow does **not** design or run data migrations.

### 2.3 `--safety-mode` / `--strict` has real behavioral impact

- `--safety-mode=normal` (default)
  - `READY_WITH_RISKS` is allowed; the team decides how to interpret it.

- `--safety-mode=strict` (or `--strict`)
  - if there is any **critical** risk (NFR, compat, migration, security,
    severe duplication), the spec **must not** be marked `READY`
  - the release-level status should reflect at least `READY_WITH_RISKS` or
    `BLOCKED`.

### 2.4 No guessing spec-ids outside SPEC_INDEX

If `--spec-ids` are not provided and there is no clear mapping in
SPEC_INDEX/project config between changes and spec-ids, the workflow must:

- **not guess** spec-ids from file paths or repo structure
- instead, ask for clarification (Ask/Architect mode) or stop with an
  appropriate message

### 2.5 Cross-repo duplication check is first-class

The workflow introduces a dedicated step for **cross-repo duplication**:

- identifies potential duplicates of shared assets such as:
  - shared APIs
  - shared data models
  - shared policies
  - shared UI components
- uses primary and supplemental registries to detect these cases and reflect
  them in the readiness report

### 2.6 Clear UI governance + UI JSON opt-out

- differentiates between **JSON-first UI** and **inline UI** per spec
- if the project has an explicit **opt-out** from JSON-first UI (e.g., noted
  in SPEC_INDEX or a project config):
  - the workflow **must respect** that decision
  - the absence of `ui.json` is not treated as a defect by itself

### 2.7 Guardrails against inventing or deleting NFRs

The workflow explicitly instructs that it must:

- **not** invent new NFRs
- **not** change NFR SLA values from what’s written in specs
- **not** delete existing NFRs from consideration

Any proposals for new NFRs or improvements must be clearly labeled as
**proposals**, separate from the core readiness verdict.

---

## 3. Backward Compatibility Notes

- This manual v5.6 applies to workflow `/smartspec_release_readiness` starting
  from version **5.6.2**.
- The workflow is **new** in the SmartSpec family; there is no older
  release-readiness manual to migrate from.

Inherited system-wide rules include:

- do **not** modify specs, tasks, or code (NO-WRITE)
- use index/registry + multi-repo flags in a consistent way with other
  workflows
- support `--kilocode` with Ask/Architect + Orchestrator-per-check semantics

If the workflow is updated with patch versions (e.g., 5.6.2 → 5.6.3) and the
core flags/modes do not change, this manual remains valid.

---

## 4. Core Concepts

### 4.1 Release scope = a set of spec-ids

Each run of the workflow works over a **set of spec-ids** representing the
release scope.

Scope is determined by:

- `--spec-ids=<id1,id2,...>`
- and optionally expanded via `--include-dependencies` using SPEC_INDEX and
  registries

### 4.2 Evidence = what the workflow can read

The workflow only uses **existing artifacts** as evidence, including:

- specs (`spec.md`) and tasks (`tasks.md`)
- registries (API, data-model, UI-component, critical-sections, ownership,
  glossary, etc.)
- test/coverage reports (where your project provides them)
- env/config files provided via `--env-config-paths`

### 4.3 Readiness dimensions

For each spec-id, the workflow evaluates readiness along several dimensions:

1. NFRs & SLAs vs actual evidence
2. Task completion (especially testing, security, migrations, ops, UI)
3. Environment & configuration for the declared `--target-env`
4. Backward compatibility (APIs, data models, migrations)
5. Cross-repo duplication (using registries)
6. UI governance (JSON-first vs inline, opt-out or not)

### 4.4 Three-level status

Both at spec-level and release-level, the workflow uses three statuses:

- `READY`
- `READY_WITH_RISKS`
- `BLOCKED`

Later sections describe the rules for deciding between these.

---

## 5. Quick Start

### 5.1 Single-repo, simple case

For a single repo with canonical index and no special multi-repo setup:

```bash
smartspec_release_readiness \
  --spec-ids=checkout_api,order_core \
  --release-label=2025.12.09-prod \
  --target-env=prod \
  --env-config-paths="config/*.yaml" \
  --report-format=md \
  --stdout-summary
```

You will get:

- a report file, e.g.:
  - `.spec/reports/smartspec_release_readiness/2025-12-09T13-05_checkout_api+order_core.md`
- a short stdout summary such as:
  - overall status = `READY_WITH_RISKS`
  - 2 specs: 1 READY, 1 READY_WITH_RISKS, 0 BLOCKED

### 5.2 Single-repo with strict mode

```bash
smartspec_release_readiness \
  --spec-ids=checkout_api \
  --release-label=v1.4.0-rc1 \
  --target-env=staging \
  --safety-mode=strict \
  --stdout-summary
```

In this case:

- if `checkout_api` still has a critical NFR with no evidence, it **cannot** be
  marked `READY`
- the workflow will return `READY_WITH_RISKS` or `BLOCKED` instead

### 5.3 Multi-repo, multi-registry, dependencies included

```bash
smartspec_release_readiness \
  --spec-ids=payments_gateway \
  --include-dependencies \
  --release-label=pay-2025.12.15 \
  --target-env=prod \
  --repos-config=.spec/repos_config.yaml \
  --registry-dir=.spec/registry \
  --registry-roots="../shared/.spec/registry;../legacy/.spec/registry" \
  --env-config-paths="config/*.yaml;infra/*.tf" \
  --report-format=json
```

Here the report will:

- expand scope to include specs that `payments_gateway` depends on (e.g.,
  `core_billing`, `user_profile`) via SPEC_INDEX and registries
- show cross-repo impact: which shared assets are reused vs potentially
  duplicated
- store the report as JSON for CI/CD or dashboards to consume

---

## 6. CLI / Flags Cheat Sheet

> Full semantics live in the workflow spec; this section focuses on
> day-to-day usage.

### 6.1 Scope & release metadata

- `--spec-ids=<id1,id2,...>`
  - required to define the release scope in most setups
  - each id **must** be present in SPEC_INDEX

- `--include-dependencies`
  - expand scope using SPEC_INDEX + registries

- `--release-label=<string>`
  - human-readable label used in the report filename and inside the report

### 6.2 Environment & configuration

- `--target-env=<env>`
  - e.g., `dev`, `staging`, `prod`

- `--env-config-paths="<glob1>;<glob2>"`
  - configuration and infrastructure files to inspect
  - e.g., `"config/*.yaml;infra/*.tf"`

### 6.3 Index / registry / multi-repo

- `--workspace-roots`
  - coarse hint for where repos live

- `--repos-config`
  - more precise description of multi-repo layout and relationships
  - recommended for serious multi-repo setups

- `--registry-dir`
  - primary registry root (usually `.spec/registry`)

- `--registry-roots`
  - additional registries treated as read-only

- `--index`, `--specindex`
  - override SPEC_INDEX path if not at a canonical location

### 6.4 Safety / kilocode / output

- `--safety-mode=normal|strict` (or `--strict`)
  - `normal`: allows `READY_WITH_RISKS`
  - `strict`: treats critical risks as hard gates

- `--kilocode`
  - enables Kilo-aware behavior (Ask/Architect + Orchestrator-per-check),
    still NO-WRITE

- `--nosubtasks`
  - disables automatic subtask decomposition under Kilo

- `--report-format=md|json`
- `--report-dir=<path>`
- `--stdout-summary`

---

## 7. How Readiness Is Decided

### 7.1 Per spec-id

Each spec will get one of:

- `READY`
- `READY_WITH_RISKS`
- `BLOCKED`

Minimum rules:

1. A spec **must not** be `READY` if:
   - a critical NFR has no evidence at all
   - there is a known breaking API/data contract change **without** a
     migration/compat plan and tasks
   - required environment/config for `--target-env` is missing

2. Under `--safety-mode=strict` / `--strict`:
   - any **critical** risk in the categories below must prevent `READY`:
     - NFRs
     - compatibility/migrations
     - security
     - severe cross-repo duplication
     - major ops/observability gaps for production

3. If there are no critical risks and remaining risks are minor → `READY`
   is acceptable.

### 7.2 Release-level

The workflow aggregates spec-level results into a release-level status.

- If **any** spec is `BLOCKED`, the overall release should be considered
  `BLOCKED`.
- If several specs are `READY_WITH_RISKS`, the release can still be
  `READY_WITH_RISKS`, but the report will highlight those risks so that
  release managers can make an informed decision.

---

## 8. KiloCode Usage Examples

### 8.1 Governance-only, Ask/Architect mode

```bash
smartspec_release_readiness \
  --spec-ids=billing_core \
  --release-label=billing-1.2.0 \
  --target-env=prod \
  --kilocode \
  --safety-mode=strict \
  --stdout-summary
```

Under Kilo, the workflow will:

- use Orchestrator to break down checks by NFR, compat, UI, etc.
- analyze artifacts in Code mode (read-only)
- never perform writes, even in Code mode

### 8.2 Turning off subtasks (small releases)

```bash
smartspec_release_readiness \
  --spec-ids=small_feature \
  --target-env=staging \
  --kilocode \
  --nosubtasks
```

This keeps Kilo-aware behavior but disables automatic subtask decomposition,
which can be useful for tiny releases.

---

## 9. Multi-repo / Multi-registry Usage Examples

### 9.1 Monorepo + shared registry

```bash
smartspec_release_readiness \
  --spec-ids=search_api \
  --include-dependencies \
  --repos-config=.spec/repos.yaml \
  --registry-dir=.spec/registry \
  --registry-roots="../platform/.spec/registry" \
  --target-env=prod
```

- `repos-config` describes which repo owns `search_api` and what it depends on
- the primary and shared registries help detect duplicate usage of shared
  models or APIs

### 9.2 Multiple teams, multiple repos

```bash
smartspec_release_readiness \
  --spec-ids=teamA_payments,teamB_notifications \
  --workspace-roots="../teamA;../teamB" \
  --registry-dir=../platform/.spec/registry \
  --target-env=prod \
  --safety-mode=strict
```

Here the interesting part is cross-repo duplication, for example:

- both Team A and Team B introduce their own Notification model while a
  shared Notification model already exists in the platform registry

The report will flag this as a duplication risk.

---

## 10. UI JSON vs Inline UI Examples

### 10.1 JSON-first UI project

Assume SPEC_INDEX or project config indicates the project uses JSON-first UI:

```bash
smartspec_release_readiness \
  --spec-ids=web_checkout \
  --target-env=prod \
  --env-config-paths="config/*.yaml" \
  --stdout-summary
```

In the report for `web_checkout`, you will see:

- UI mode: `json-first`
- checks that `ui.json` exists and is consistent with `spec.md`
- if `ui.json` is missing despite the JSON-first policy, this is at least a
  `READY_WITH_RISKS` issue (or `BLOCKED` under strict/project policy).

### 10.2 Project opted out of UI JSON separation

If the project has explicitly opted out of JSON-first UI (e.g. via SPEC_INDEX
or config):

```bash
smartspec_release_readiness \
  --spec-ids=admin_portal \
  --target-env=staging
```

The workflow will:

- respect this opt-out decision
- not treat the absence of `ui.json` as a defect by itself
- instead, check whether `spec.md` describes:
  - main flows, components, interactions
  - relevant UX/accessibility requirements
  - and whether tasks cover essential UI work

---

## 11. Best Practices & Anti-patterns

### 11.1 Best Practices

- Always provide `--spec-ids` explicitly where possible.
- Use `--release-label` consistently across code, CI, and reports.
- Run `verify_tasks_progress` before release readiness so task status is
  up to date.
- In multi-repo programs, prefer `--repos-config` over relying only on
  `--workspace-roots`.
- Turn on `--safety-mode=strict` in production-grade pipelines.

### 11.2 Anti-patterns

- Letting the workflow guess scope from files without SPEC_INDEX mapping.
- Treating `READY_WITH_RISKS` as equivalent to `READY` without reading
  the risk sections.
- Expecting this workflow to design or run data migrations.
- Ignoring registries and re-creating shared models in multiple repos.

---

## 12. FAQ / Troubleshooting

### Q1: Why is a spec marked `BLOCKED` even though devs say “it’s ready”?

Check:

- is there a critical NFR with no evidence?
- is there a breaking API/data model change with no migration/compat plan
  and tasks?
- are required configs for `--target-env` missing?
- is `--safety-mode=strict` enabled (which tightens rules)?

### Q2: We want to ship despite minor risks. What should we do?

- Use `--safety-mode=normal`.
- Accept `READY_WITH_RISKS` as the status.
- Have a release manager or tech lead review the risk sections in the report
  and decide whether to proceed.

### Q3: Why does the report say “scope unclear / please specify spec-ids”?

- Because the workflow is **not allowed to guess** spec-ids outside
  SPEC_INDEX.
- Provide `--spec-ids` explicitly, or define a mapping from branch/changes
  to spec-ids in your SPEC_INDEX or project config.

### Q4: Why is UI marked as a risk even though we don’t use JSON-first yet?

- Make sure there is a project-level opt-out of JSON-first UI recorded in
  SPEC_INDEX or a config the workflow can read.
- If the decision is only verbal, the workflow will default to general
  SmartSpec guidance and may treat missing `ui.json` as a governance risk.

### Q5: Should we commit the report to git?

- It is recommended to either commit the report or store it as a CI artifact
  for important releases.
- This makes it easier to reason about past decisions during incident
  analysis.

---

End of `/smartspec_release_readiness` Manual v5.6 (English).

If new features are added to the workflow (e.g. new artifact types or
significant changes to strict-mode criteria), a new manual version (e.g. 5.7)
should be issued while keeping patch-level compatibility clear.

