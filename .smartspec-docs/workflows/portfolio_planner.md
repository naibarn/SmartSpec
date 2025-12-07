---
description: SmartSpec Portfolio Planner Guide (v5.2)
version: 5.2
last_updated: 2025-12-07
---

# SmartSpec Portfolio Planner Guide

This guide explains how to use `/smartspec_portfolio_planner` in SmartSpec v5.2.

The portfolio planner provides a strategic, multi-SPEC view for large projects. It is designed to help teams prioritize work, detect dependency risks, and coordinate large-scale delivery across capability areas such as security, observability, platform, integration, and UI.

---

## Key Concepts

### SmartSpec Centralization (v5.2)

SmartSpec v5.2 separates **tooling** from **project-owned truth**.

- **Project-owned canonical space:** `.spec/`
- **Canonical index:** `.spec/SPEC_INDEX.json`
- **Shared registries (if present):** `.spec/registry/`
- **Legacy mirror:** `SPEC_INDEX.json` at repository root
- **Deprecated tooling index:** `.smartspec/SPEC_INDEX.json`

The portfolio planner **reads** from the canonical layer to generate planning reports.

### UI Design Addendum

When the portfolio contains UI specs:

- **UI design source of truth** is `ui.json` inside the UI spec folder.
- `spec.md` documents constraints, mapping, and logic boundaries.
- Business logic must remain outside UI JSON.

Projects that do not use UI JSON are not affected.

---

## What the Planner Produces

The planner generates a report under:

- **Default:** `.spec/reports/portfolio-planner/`

The report may include:

- dependency-first roadmap view
- category streams
- capability map (security/observability/data/infra/integration/ui)
- public/private split insights (heuristic)
- UI readiness and component alignment checks (conditional)
- registry gap observations (read-only)

---

## When to Use

- Quarterly/half-year planning
- Portfolio grooming for large systems
- Before onboarding multiple teams
- After major index reindexing
- After lifecycle transitions for large sets of specs

---

## Inputs

The planner relies on:

- `.spec/SPEC_INDEX.json` (preferred)
- `SPEC_INDEX.json` (legacy mirror)
- `.spec/registry/*` (optional)
- `specs/**/spec.md`
- `ui.json` for UI specs (optional but recommended when UI specs are active)

---

## Command Reference

### Basic Usage

```bash
/smartspec_portfolio_planner
```

### Detailed Report

```bash
/smartspec_portfolio_planner --report-dir=.spec/reports/portfolio-planner --view=full
```

### View-Specific Planning

```bash
/smartspec_portfolio_planner --view=dependency
/smartspec_portfolio_planner --view=category
/smartspec_portfolio_planner --view=capability
/smartspec_portfolio_planner --view=public-private
/smartspec_portfolio_planner --view=ui
```

---

## Flags

### Index / Registry

- `--index`
  - Override SPEC_INDEX path.
  - If omitted, the planner auto-detects in this order:
    1) `.spec/SPEC_INDEX.json`
    2) `SPEC_INDEX.json`
    3) `.smartspec/SPEC_INDEX.json` (deprecated)
    4) `specs/SPEC_INDEX.json` (older layout)

- `--registry-dir`
  - Default: `.spec/registry`

### Planning View

- `--view`
  - Values: `full`, `dependency`, `category`, `capability`, `public-private`, `ui`
  - Default: `full`

### Interpretation Mode

- `--mode`
  - Values: `portfolio`, `runtime`
  - Default: `portfolio`

**Meaning:**

- `portfolio`
  - Designed for roadmap-level planning.
  - Planned/backlog/idea/draft specs may be incomplete without being treated as readiness blockers.

- `runtime`
  - Designed for delivery readiness.
  - Emphasizes that active/core/stable specs should have resolvable artifacts and valid dependency chains.

### Reporting / Safety

- `--report-dir`
  - Default: `.spec/reports/portfolio-planner/`

- `--strict`
  - Rarely needed for planning.
  - Use only when you want to treat structural inconsistencies as hard failures.

- `--dry-run`
  - Print findings without writing report files.

---

## How to Interpret Common Findings

### High Orphan Count

A large number of orphaned specs is common in roadmap-centric indexes.

- In `portfolio` mode this is typically advisory.
- In `runtime` mode it becomes a delivery risk primarily for **active/core** specs.

### Similar Titles

Similar titles often indicate overlapping scope or a missing domain naming standard.

Use follow-up workflows:

- `/smartspec_global_registry_audit`
- `/smartspec_validate_index --mode=portfolio`

### Foundational Gaps

If core capabilities (auth, authorization, audit, rate limiting, observability) are missing or weakly defined, the planner will highlight this as a scaling risk.

---

## UI-Specific Guidance

The planner’s UI view becomes relevant when:

- a spec category is `ui`, or
- a UI spec folder contains `ui.json`.

The planner will warn when:

- `ui.json` is missing for an active UI spec.
- UI component naming appears inconsistent with `ui-component-registry.json` (if present).

The planner does not modify UI files.

---

## Recommended Follow-Up Workflows

- `/smartspec_validate_index --mode=portfolio`
- `/smartspec_spec_lifecycle_manager`
- `/smartspec_reindex_specs`
- `/smartspec_generate_plan`
- `/smartspec_generate_tasks`
- `/smartspec_global_registry_audit`

---

## Best Practices

- Keep `.spec/SPEC_INDEX.json` as your canonical index.
- Treat root `SPEC_INDEX.json` as a legacy mirror for backward compatibility.
- Use `portfolio` mode for strategy and roadmap.
- Use `runtime` mode before release gates.
- For UI-heavy programs, maintain `ui.json` early to reduce rework during implementation.

---

## Troubleshooting

### The report looks too strict for early-stage roadmaps

Use:

```bash
/smartspec_portfolio_planner --mode=portfolio
```

### UI warnings appear in a non-UI project

Confirm that no spec is incorrectly categorized as `ui` in the index.

---

## Summary

The SmartSpec Portfolio Planner is an executive-level lens that complements strict validation. It helps teams prioritize the right specs in the right order, while remaining aligned to the v5.2 centralization model and the optional UI JSON design workflow.

