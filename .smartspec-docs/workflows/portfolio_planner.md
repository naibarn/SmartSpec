---
description: SmartSpec Portfolio Planner Guide (v5.6)
version: 5.6
last_updated: 2025-12-08
---

# SmartSpec Portfolio Planner Guide

This guide explains how to use `/smartspec_portfolio_planner` in SmartSpec v5.6.

The portfolio planner provides a strategic, multi-SPEC view for large projects. It is designed to help teams prioritize work, detect dependency risks, and coordinate large-scale delivery across capability areas such as security, observability, platform, integration, and UI.

This v5.6 guide preserves the original v5.2 structure and readability while adding:

- **Multi-registry** awareness with explicit precedence
- `--specindex` alias consistency
- `--safety-mode` semantics separated from `--mode=portfolio|runtime`
- Chain readiness hints for generate_spec and generate_tasks

---

## Key Concepts

### SmartSpec Centralization (v5.6)

SmartSpec v5.6 separates **tooling** from **project-owned truth**.

- **Project-owned canonical space:** `.spec/`
- **Canonical index:** `.spec/SPEC_INDEX.json`
- **Shared registries (if present):** `.spec/registry/`
- **Legacy mirror:** `SPEC_INDEX.json` at repository root
- **Deprecated tooling index:** `.smartspec/SPEC_INDEX.json`

The portfolio planner **reads** from the canonical layer to generate planning reports.

### Portfolio vs Runtime Interpretation

The planner uses the same interpretation model as validation and lifecycle workflows:

- `--mode=portfolio` (default)
  - Designed for roadmap-level planning.
  - Planned/backlog/idea/draft specs may be incomplete without being treated as readiness blockers.

- `--mode=runtime`
  - Designed for delivery readiness.
  - Emphasizes that active/core/stable specs should have resolvable artifacts and valid dependency chains.

### Safety Mode (NEW in v5.6)

v5.6 introduces `--safety-mode` to standardize strictness across the chain.

- `strict` (default)
  - Blocks recommendations that would cause cross-repo duplication risk.

- `dev`
  - Continues with high-visibility warnings.

`--strict` remains a legacy alias for strict gating.

### Multi-Registry Precedence (NEW in v5.6)

- **Primary registry:** `--registry-dir` (default `.spec/registry`)
- **Supplemental registries:** `--registry-roots` (read-only)

Precedence rules:

1) The primary registry is authoritative.
2) Supplemental registries are validation sources used to prevent cross-repo duplication.

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
- cross-repo reuse risk notes (v5.6)

---

## When to Use

- Quarterly/half-year planning
- Portfolio grooming for large systems
- Before onboarding multiple teams
- After major index reindexing
- After lifecycle transitions for large sets of specs
- When public/private repos share domain ownership

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
/smartspec_portfolio_planner --report=detailed --view=full
```

### View-Specific Planning

```bash
/smartspec_portfolio_planner --view=dependency
/smartspec_portfolio_planner --view=category
/smartspec_portfolio_planner --view=capability
/smartspec_portfolio_planner --view=public-private
/smartspec_portfolio_planner --view=ui
```

### Runtime Gate Lens

```bash
/smartspec_portfolio_planner --mode=runtime --safety-mode=strict
```

### Multi-repo + multi-registry planning

```bash
/smartspec_portfolio_planner \
  --repos-config=.spec/smartspec.repos.json \
  --registry-dir=.spec/registry \
  --registry-roots="../Repo-A/.spec/registry,../Repo-B/.spec/registry" \
  --view=full \
  --mode=portfolio \
  --report=detailed
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

### Planning View

- `--view`
  - Values: `full`, `dependency`, `category`, `capability`, `public-private`, `ui`
  - Default: `full`

### Interpretation Mode

- `--mode`
  - Values: `portfolio`, `runtime`
  - Default: `portfolio`

### Reporting / Safety

- `--report`
  - Values: `summary`, `detailed`
  - Default: `summary`

- `--safety-mode`
  - Values: `strict`, `dev`
  - Default: `strict`

- `--strict`
  - Legacy alias for strict gating.

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

### Registry Gap Lens (v5.6)

In multi-repo platforms:

- Names present only in supplemental registries are likely owned elsewhere.
- The planner should treat them as **reuse** candidates until governance clarifies ownership.

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
- For multi-repo portfolios, run with `--registry-roots` to reduce duplicate-shared-name risk.
- For UI-heavy programs, maintain `ui.json` early to reduce rework during implementation.

---

## Troubleshooting

### The report looks too strict for early-stage roadmaps

Use:

```bash
/smartspec_portfolio_planner --mode=portfolio --safety-mode=dev
```

### UI warnings appear in a non-UI project

Confirm that no spec is incorrectly categorized as `ui` in the index.

---

## Summary

The SmartSpec Portfolio Planner is an executive-level lens that complements strict validation. In v5.6, it remains aligned to the centralization model while adding multi-registry awareness and chain-consistent safety semantics so multi-repo programs can plan accurately without encouraging accidental duplication.

