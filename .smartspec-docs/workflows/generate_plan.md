---
manual_name: /smartspec_generate_plan Manual (EN)
manual_version: 5.6
compatible_workflow: /smartspec_generate_plan
compatible_workflow_versions: 5.6.2 – 5.6.x
role: user/operator manual (architect, tech lead, PM, platform, spec owner)
---

# /smartspec_generate_plan Manual (v5.6, English)

## 1. Overview

This manual explains how to use the workflow:

> `/smartspec_generate_plan v5.6.x` (e.g., v5.6.2)

This workflow is the **planning layer** in the SmartSpec chain. It
creates/updates high-level implementation plans (`plan.md`) that are
ordered by dependencies and ready to be used by task-generation
workflows.

The typical v5.6 chain:

1. `/smartspec_validate_index`
2. `/smartspec_generate_spec`
3. `/smartspec_generate_plan`
4. `/smartspec_generate_tasks`
5. `/smartspec_sync_spec_tasks`

The goals of `/smartspec_generate_plan` are to:

- produce plans that are **task-ready** and safe inputs to
  `/smartspec_generate_tasks`
- avoid cross-SPEC and cross-repo drift for shared entities
- respect **UI mode** (JSON-first vs inline) so UI work aligns with
  specs and UI workflows
- behave in a **governance-aware** way: do not silently invent new
  requirements
- handle multi-repo / multi-registry safely
- support KiloCode (`--kilocode`) and the Orchestrator-per-task rule

> **v5.6.2 note**
> - Introduces `safety_status = SAFE | UNSAFE | DEV-ONLY` in both plans
>   and reports.
> - Adds `--run-label` and `--plan-layout` for better traceability and
>   deterministic output.
> - Strengthens guidance for AI UI JSON signals and multi-spec Kilo
>   orchestration.
> - No existing flags or behaviors are removed; all changes are
>   additive.

---

## 2. When to Use

Use `/smartspec_generate_plan` when you:

- start a new feature/program involving multiple specs
- want a clear phase-structured plan before breaking work into tasks
- prepare to run `/smartspec_generate_tasks` on several specs
- need to re-plan after significant refactors, reindexing, or ownership
  changes
- coordinate work across **multiple repos** that share registries or
  contracts

Do **not** use this workflow when:

- you only need tasks for a single, well-scoped spec →
  `/smartspec_generate_tasks` alone may be enough
- you want to mass-edit `spec.md` or `tasks.md` → use the appropriate
  spec/task workflows instead
- your process requires fully manual planning for audit reasons

---

## 3. Core Concepts

### 3.1 SPEC_INDEX and registries

- `SPEC_INDEX` is the central map of all specs in the system.
- `registries` are catalogs of shared entities that must be reused, not
  redefined, such as:
  - API registry
  - data model registry
  - glossary
  - critical sections
  - UI component registry

`/smartspec_generate_plan` uses the index and registries to:

- understand dependency structure between specs
- identify which entities must be treated as shared contracts rather
  than re-created

### 3.2 Safety mode and safety_status

- `--safety-mode=strict` (default)
  - strict about ownership and duplication
  - if ambiguity or conflicts could lead to duplicated or conflicting
    shared entities, the plan must be marked as
    `safety_status=UNSAFE` (or the run must fail)
- `--safety-mode=dev`
  - relaxed mode for sandbox/PoC/exploratory planning
  - allows incomplete index/registries, but the plan is marked as
    `safety_status=DEV-ONLY`

Every generated plan must include a header with at least:

- spec IDs in scope
- SPEC_INDEX path used
- run-label (if any)
- timestamp
- `safety_status = SAFE | UNSAFE | DEV-ONLY`

### 3.3 Alignment between spec ↔ plan ↔ tasks

- `spec.md` is the source-of-truth for requirements.
- Plans **must not silently introduce new requirements**.
- If specs are unclear or conflicting, the plan should:
  - add explicit items like “clarify requirement X in spec”, rather than
    guessing the requirement.
- `/smartspec_generate_tasks` is expected to use both spec and plan;
  the two must remain aligned.

### 3.4 UI mode and AI UI JSON

- UI mode is controlled by `--ui-mode=auto|json|inline`.
- `json` → JSON-first UI: `ui.json` is a primary design artifact.
- `inline` → UI is specified inside `spec.md`; no `ui.json` is required.

When UI is in scope, the plan should:

- schedule steps for authoring/reviewing `ui.json` when JSON-first
- use signals from UI-related workflows when available, such as:
  - `ui_spec_origin`, `ui_spec_review_status`,
    `ui_json_quality_status`
- treat AI-generated UI JSON as **draft** until reviewed and aligned
  with the design system

---

## 4. Inputs / Outputs

### 4.1 Inputs (artifacts)

- SPEC_INDEX (if present)
- registries (primary + supplemental)
- target specs: `specs/<category>/<spec-id>/spec.md`
- existing `plan.md` (if any)
- existing `tasks.md` or other reports (read-only context)
- optional UI governance reports from UI workflows

### 4.2 Inputs (key flags)

- Scope
  - `--spec=<path>`
  - `--spec-ids=<id1,id2,...>`
- Index & registries
  - `--index`, `--specindex`
  - `--registry-dir`, `--registry-roots`
- Multi-repo
  - `--workspace-roots`
  - `--repos-config`
- Identity & layout
  - `--run-label=<id>`
  - `--plan-layout=per-spec|consolidated`
  - `--output=<path>`
- Safety & UI
  - `--safety-mode=strict|dev`, `--strict`, `--dry-run`
  - `--ui-mode=auto|json|inline`
- Reporting & Kilo
  - `--report-dir`, `--stdout-summary`
  - `--kilocode`, `--nosubtasks`

### 4.3 Outputs

- `plan.md` (or the path specified by `--output`) with a header
  containing `safety_status` and run metadata
- a planning report under `.spec/reports/generate-plan/` (or
  `--report-dir`), including:
  - index/registry context
  - scope, safety mode, safety_status
  - dependency graph summary
  - multi-repo, reuse-not-rebuild, and drift notes

---

## 5. Quick Start Examples

### 5.1 Single spec, strict mode

```bash
smartspec_generate_plan \
  --spec=specs/payments/spec-pay-001-checkout/spec.md \
  --index=.spec/SPEC_INDEX.json \
  --registry-dir=.spec/registry \
  --safety-mode=strict \
  --run-label=checkout-v2-planning \
  --stdout-summary
```

Result:

- `plan.md` next to `spec.md` with header and `safety_status`.
- planning report in `.spec/reports/generate-plan/`.

### 5.2 Multiple specs, per-spec plans

```bash
smartspec_generate_plan \
  --spec-ids=payments.checkout,identity.login \
  --index=.spec/SPEC_INDEX.json \
  --registry-dir=.spec/registry \
  --plan-layout=per-spec \
  --safety-mode=strict \
  --run-label=release-2024Q4 \
  --stdout-summary
```

Each spec gets its own `plan.md`, ordered according to the dependency
graph from the index.

### 5.3 Consolidated plan for multiple specs

```bash
smartspec_generate_plan \
  --spec-ids=payments.checkout,identity.login \
  --index=.spec/SPEC_INDEX.json \
  --registry-dir=.spec/registry \
  --plan-layout=consolidated \
  --output=plans/release-2024Q4-plan.md \
  --run-label=release-2024Q4 \
  --safety-mode=strict \
  --stdout-summary
```

---

## 6. Multi-repo / Multi-registry Examples

### 6.1 Monorepo with multiple services

```bash
smartspec_generate_plan \
  --spec-ids=billing.invoice,notifications.email \
  --index=.spec/SPEC_INDEX.json \
  --registry-dir=.spec/registry \
  --workspace-roots="." \
  --plan-layout=per-spec \
  --safety-mode=strict \
  --stdout-summary
```

### 6.2 Multi-repo, shared platform registry

```bash
smartspec_generate_plan \
  --spec-ids=teamA.web_portal,teamB.mobile_app \
  --specindex=../platform/.spec/SPEC_INDEX.json \
  --registry-dir=.spec/registry \
  --registry-roots="../platform/.spec/registry" \
  --workspace-roots="../platform,../teamA,../teamB" \
  --repos-config=.spec/smartspec.repos.json \
  --plan-layout=consolidated \
  --output=.spec/plans/cross-team-2024Q4.md \
  --safety-mode=strict \
  --stdout-summary
```

External specs and shared entities are treated as **external
dependencies** with explicit reuse-not-rebuild notes.

---

## 7. UI JSON vs Inline UI Examples

### 7.1 JSON-first UI with AI-generated UI JSON

```bash
smartspec_generate_plan \
  --spec=specs/web/spec-web-001-dashboard/spec.md \
  --index=.spec/SPEC_INDEX.json \
  --registry-dir=.spec/registry \
  --ui-mode=json \
  --run-label=dashboard-ui-v3 \
  --safety-mode=strict \
  --stdout-summary
```

The resulting plan should include phases for:

- authoring/updating `ui.json` aligned with the design system and UI
  registries
- reviewing AI-generated UI JSON when `meta.source=ai` and
  `meta.review_status=unreviewed`
- separating layout from business logic

### 7.2 Legacy UI (inline only)

```bash
smartspec_generate_plan \
  --spec=specs/legacy/spec-legacy-ui-001/spec.md \
  --index=.spec/SPEC_INDEX.json \
  --registry-dir=.spec/registry \
  --ui-mode=inline \
  --safety-mode=dev \
  --run-label=legacy-ui-cleanup \
  --stdout-summary
```

Here the plan focuses on refactoring UI according to inline spec
requirements, without requiring `ui.json`, while optionally suggesting a
future move to JSON-first.

---

## 8. KiloCode Usage Examples

### 8.1 Kilo, multiple specs, per-spec plans

```bash
smartspec_generate_plan \
  --spec-ids=payments.checkout,identity.login \
  --index=.spec/SPEC_INDEX.json \
  --registry-dir=.spec/registry \
  --kilocode \
  --plan-layout=per-spec \
  --run-label=release-2024Q4 \
  --safety-mode=strict \
  --stdout-summary
```

On Kilo:

- Orchestrator breaks work into subtasks per spec, ordered by
  dependencies from SPEC_INDEX.
- Code mode reads specs/index/registries and generates plans.
- If any scope is `UNSAFE`, the overall run is considered `UNSAFE`.

### 8.2 Disable subtasks for a small scope

```bash
smartspec_generate_plan \
  --spec=specs/tools/spec-tools-001-linter/spec.md \
  --index=.spec/SPEC_INDEX.json \
  --registry-dir=.spec/registry \
  --kilocode \
  --nosubtasks \
  --run-label=tools-linter-plan \
  --stdout-summary
```

---

## 9. Best Practices

- Use `--safety-mode=strict` by default for production-bound work.
- Run with `--dry-run` the first time in a new repo or configuration.
- Keep `.spec/SPEC_INDEX.json` and `.spec/registry/` up to date and
  plan remediation work when they fall behind reality.
- Socialize the meaning of `safety_status`:
  - SAFE → may be used for downstream automation after appropriate
    review.
  - UNSAFE → requires resolution of conflicts/ambiguities first.
  - DEV-ONLY → for sandbox/PoC; not a release plan.
- Maintain spec ↔ plan alignment; if they drift, fix the spec first and
  regenerate the plan.

---

## 10. Risks if you don’t use (or misuse) this workflow

- The spec → plan → tasks chain becomes inconsistent, causing teams to
  implement different interpretations of the same feature.
- Shared entities (APIs/models/terms) are duplicated across repos
  without a clear view of drift.
- AI-generated UI JSON reaches production with no explicit review
  phases.
- Multi-repo programs evolve with reimplementation instead of reuse,
  leading to long-term maintenance issues.

---

## 11. FAQ / Troubleshooting

**Q1: Can I use this without SPEC_INDEX?**  
Yes. The workflow operates in local-spec-only mode and the plan should
include a Phase 0 recommending index/registry initialization before
production use.

**Q2: What if we don’t want UI JSON / AI UI yet?**  
Use `--ui-mode=inline` and keep UI requirements in `spec.md`. The plan
can still suggest a future migration path to JSON-first.

**Q3: How much should we trust `safety_status`?**  
Treat `safety_status` as a strong signal for CI and release boards,
especially SAFE vs UNSAFE in strict mode. Human review is still
recommended for major initiatives.

**Q4: Does this workflow modify specs or tasks?**  
No. It only creates/updates plans and planning reports. Specs and tasks
are managed by other workflows in the SmartSpec chain.

---

End of `/smartspec_generate_plan v5.6.2 – 5.6.x` manual (English).
If future versions significantly change safety-mode, plan-layout, UI
mode, or multi-repo behavior, create a new manual (e.g., v5.7) and
clearly state the compatible workflow versions.

