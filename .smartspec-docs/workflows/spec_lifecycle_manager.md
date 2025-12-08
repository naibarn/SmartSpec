---
description: SmartSpec Spec Lifecycle Manager Guide (v5.6)
version: 5.6
last_updated: 2025-12-08
---

# SmartSpec Spec Lifecycle Manager Guide

This guide explains how to use `/smartspec_spec_lifecycle_manager` in SmartSpec v5.6.

The lifecycle manager helps teams govern how specs move from idea → planned → active → stable → deprecated → archived, while preventing large-scale dependency breakage in multi-team environments.

This v5.6 guide preserves the structure and intent of the v5.2 manual while adding:

- Multi-registry awareness with explicit precedence
- `--specindex` alias consistency
- `--safety-mode` semantics separated from `--mode=portfolio|runtime`
- Optional UI-mode-aware lifecycle checks
- Chain readiness notes for generate_spec/tasks

---

## Key Concepts

### SmartSpec Centralization (v5.6)

SmartSpec v5.6 separates **tooling files** from **project-owned truth**.

- **Project-owned canonical space:** `.spec/`
- **Canonical index:** `.spec/SPEC_INDEX.json`
- **Shared registries (optional but recommended):** `.spec/registry/`
- **Legacy root mirror:** `SPEC_INDEX.json`
- **Deprecated tooling index:** `.smartspec/SPEC_INDEX.json`

The lifecycle manager updates lifecycle-related metadata in the **canonical index** while preserving the existing `SPEC_INDEX.json` schema already used in production.

### Status Buckets

For compatibility and readability, lifecycle status values are interpreted in three buckets:

- **Planned:** `planned`, `backlog`, `idea`, `draft`
- **Active:** `active`, `in-progress`, `stable`, `core`
- **End-of-life:** `deprecated`, `archived`

If a spec has no explicit status, SmartSpec assumes `active`.

### Portfolio vs Runtime Interpretation

The lifecycle manager uses the same interpretation model as validation and planning workflows:

- `--mode=portfolio` (default)
  - Optimized for roadmap governance.
  - Allows planned/backlog specs to be incomplete without treating them as hard blockers.

- `--mode=runtime`
  - Optimized for delivery readiness.
  - Applies stricter checks when changing the status of active/core/stable specs.

### Safety Mode (NEW in v5.6)

v5.6 introduces `--safety-mode` to standardize strictness across the chain without changing the meaning of `--mode`.

- `--safety-mode=strict` (default)
  - Blocks unsafe transitions when ambiguity could create cross-repo duplication or break shared contracts.

- `--safety-mode=dev`
  - Continues with warnings and requires explicit remediation notes.

`--strict` remains supported as a legacy alias.

### Multi-Registry Precedence (NEW in v5.6)

- **Primary registry:** `--registry-dir` (default `.spec/registry`)
- **Supplemental registries:** `--registry-roots` (read-only)

Precedence rules:

1) The primary registry is authoritative.
2) Supplemental registries are validation sources used to prevent cross-repo duplication.
3) Names found only in supplemental registries should be treated as likely cross-repo owners until clarified.

### UI Design Addendum

When UI specs exist:

- **UI design source of truth** is `ui.json` inside the UI spec folder.
- `spec.md` documents constraints, mapping, and logic boundaries.
- UI JSON must not contain business logic.

Lifecycle changes must not force UI design artifacts into `.smartspec/`.

Projects that do not use UI JSON are not affected.

---

## What the Lifecycle Manager Produces

The workflow may output:

- **Updated canonical index:** `.spec/SPEC_INDEX.json`
- **Optional legacy mirror:** `SPEC_INDEX.json` (root)
- **Lifecycle report:** `.spec/reports/spec-lifecycle/`

The report is project-owned and can be version-controlled.

---

## When to Use

- During roadmap grooming
- When promoting a spec from planned to active
- When stabilizing a core contract
- Before deprecating shared APIs or models
- Before release gates (use runtime mode)
- When ownership boundaries span public/private repos

---

## Inputs

The lifecycle manager relies on:

- `.spec/SPEC_INDEX.json` (preferred)
- `SPEC_INDEX.json` at repo root (legacy mirror)
- `.spec/registry/*` (optional for impact analysis)
- Optional supplemental registries for cross-repo validation
- `specs/**/spec.md` (read-only)
- `ui.json` for UI specs (read-only, conditional)

---

## Command Reference

### Audit-Only (No Changes)

If you do not specify an operation flag, the workflow generates an analysis report only.

```bash
/smartspec_spec_lifecycle_manager
```

### Set Status for a Single Spec

```bash
/smartspec_spec_lifecycle_manager --spec-id=spec-core-004-rate-limiting --set-status=stable
```

### Promote / Demote Maturity

```bash
/smartspec_spec_lifecycle_manager --spec-id=spec-core-003-audit-logging --promote
/smartspec_spec_lifecycle_manager --spec-id=spec-core-003-audit-logging --demote
```

### Deprecate or Archive

```bash
/smartspec_spec_lifecycle_manager --spec-id=spec-some-feature --deprecate
/smartspec_spec_lifecycle_manager --spec-id=spec-some-feature --archive
```

### Batch Operations by Category

```bash
/smartspec_spec_lifecycle_manager --category=ui --set-status=planned
```

### Runtime Gate Lens

```bash
/smartspec_spec_lifecycle_manager --mode=runtime --safety-mode=strict
```

### Control Root Mirror

```bash
/smartspec_spec_lifecycle_manager --mirror-root=true
/smartspec_spec_lifecycle_manager --mirror-root=false
```

### Dry Run

```bash
/smartspec_spec_lifecycle_manager --spec-id=spec-123 --set-status=deprecated --dry-run
```

### Multi-repo + multi-registry lifecycle review

```bash
/smartspec_spec_lifecycle_manager \
  --repos-config=.spec/smartspec.repos.json \
  --registry-dir=.spec/registry \
  --registry-roots="../Repo-A/.spec/registry,../Repo-B/.spec/registry" \
  --mode=portfolio \
  --report=detailed
```

---

## Flags

### Index / Registry

- `--index`
  - Override SPEC_INDEX path.
  - If omitted, auto-detect order:
    1) `.spec/SPEC_INDEX.json`
    2) `SPEC_INDEX.json`
    3) `.smartspec/SPEC_INDEX.json` (deprecated)
    4) `specs/SPEC_INDEX.json`

- `--specindex`
  - Legacy alias for `--index`.

- `--registry-dir`
  - Default: `.spec/registry`

- `--registry-roots`
  - Supplemental registries (read-only validation).

### Multi-Repo

- `--workspace-roots`
  - Comma-separated list of additional repo roots to search for specs.

- `--repos-config`
  - JSON config describing known repos and aliases.
  - Recommended: `.spec/smartspec.repos.json`

### Target Selection

- `--spec-id`
- `--spec-ids`
- `--category`
- `--status`

If no target is provided, the workflow defaults to analysis-only.

### Lifecycle Operations

- `--set-status`
  - Common values: `planned`, `backlog`, `draft`, `active`, `in-progress`, `stable`, `deprecated`, `archived`

- `--promote`
- `--demote`
- `--deprecate`
- `--archive`

### Interpretation

- `--mode`
  - Values: `portfolio`, `runtime`
  - Default: `portfolio`

### Mirroring / Safety

- `--mirror-root`
  - Default behavior:
    - `true` if `SPEC_INDEX.json` already exists at root
    - otherwise `false`

- `--safety-mode`
  - Values: `strict`, `dev`
  - Default: `strict`

- `--strict`
  - Legacy alias for strict gating.

- `--dry-run`
  - Show planned changes without writing files.

- `--report`
  - Values: `summary`, `detailed`

---

## How to Interpret Common Findings

### Deprecating a Spec With Active Dependents

This is the highest-risk transition in large systems.

Expected lifecycle report guidance:

- list dependents
- recommend a replacement or migration wave
- identify registry items impacted

In `--mode=runtime --safety-mode=strict`, this transition should be blocked.

### Planned Spec Required by Active Specs

This usually indicates either:

- a missing foundational spec, or
- an incorrectly assigned status on the dependency.

Use:

- `/smartspec_validate_index --mode=portfolio`
- `/smartspec_portfolio_planner --view=dependency`

### Cross-Registry Ownership Ambiguity (v5.6)

If a shared name appears only in supplemental registries:

- treat it as likely owned elsewhere
- avoid promoting new local specs that would introduce a competing definition
- add an explicit ownership clarification step in the roadmap

---

## UI-Specific Lifecycle Guidance

The lifecycle workflow will:

- warn when an active UI spec lacks `ui.json`
- highlight potential UI component registry impacts when deprecating UI specs

It does not modify UI files.

---

## Recommended Follow-Up Workflows

- `/smartspec_validate_index`
- `/smartspec_portfolio_planner`
- `/smartspec_global_registry_audit`
- `/smartspec_reindex_specs`
- `/smartspec_generate_plan`
- `/smartspec_generate_tasks`

---

## Best Practices

- Treat `.spec/SPEC_INDEX.json` as canonical.
- Keep root `SPEC_INDEX.json` only as a legacy mirror.
- Use `portfolio` mode for governance and roadmap transitions.
- Use `runtime` mode before releases or when deprecating shared contracts.
- For multi-repo portfolios, include `--registry-roots` to tighten cross-repo safety.
- Add explicit status values to planned specs to reduce false alarms in strict validation.

---

## Troubleshooting

### The lifecycle tool changed the root index unexpectedly

Explicitly set:

```bash
/smartspec_spec_lifecycle_manager --mirror-root=false
```

### The tool seems too strict for early roadmap work

Use:

```bash
/smartspec_spec_lifecycle_manager --mode=portfolio --safety-mode=dev
```

---

## Summary

`/smartspec_spec_lifecycle_manager` in SmartSpec v5.6 provides a safe, schema-compatible approach to lifecycle governance. It keeps large portfolios coherent by enforcing dependency-aware transitions, aligning with canonical centralization rules, and adds multi-registry safety so cross-repo shared contracts can evolve without accidental duplication.

