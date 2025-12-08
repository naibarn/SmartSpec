---
description: SmartSpec Global Registry Audit Guide (v5.6)
version: 5.6
last_updated: 2025-12-08
---

# SmartSpec Global Registry Audit Guide

This guide explains how to use `/smartspec_global_registry_audit` in SmartSpec v5.6.

Global Registry Audit is a governance workflow that scans your SmartSpec ecosystem to detect and reduce cross-SPEC naming and definition drift. It focuses on shared registries such as glossary, data models, API contracts, critical sections, and optional patterns/UI component registries.

Rather than silently rewriting your system, it produces **audit reports and alignment recommendations** for human review.

This v5.6 guide preserves the original structure and intent of the v5.2 manual while adding:

- **Multi-registry support** with explicit precedence
- **Multi-repo alignment** consistent with the v5.6 chain
- **Safety-mode** semantics separated from `--mode=portfolio|runtime`
- **Chain readiness notes** for generate_spec and generate_tasks

---

## Key Concepts

### SmartSpec Centralization (v5.6)

SmartSpec v5.6 continues the separation of **tooling** from **project-owned truth**.

- **Project-owned canonical space:** `.spec/`
- **Canonical index:** `.spec/SPEC_INDEX.json`
- **Shared registries (primary):** `.spec/registry/`
- **Legacy root mirror:** `SPEC_INDEX.json`
- **Deprecated tooling index:** `.smartspec/SPEC_INDEX.json`

The audit reads from the canonical layer when present and remains compatible with the existing `SPEC_INDEX.json` schema already used in production.

### Status-Aware Governance

Large systems often keep roadmap specs in the index before all files exist.

To avoid forcing low-quality placeholder specs, audit severities should be interpreted consistently with other governance flows:

- `--mode=portfolio` (default)
  - Optimized for roadmap-level normalization.
  - Planned/backlog specs may be incomplete.

- `--mode=runtime`
  - Optimized for delivery readiness.
  - Drift affecting active/core/stable specs is treated with higher urgency.

### Safety Mode (NEW in v5.6)

v5.6 introduces `--safety-mode` to standardize strictness across the chain without changing the meaning of `--mode`.

- `--safety-mode=strict` (default)
  - Escalates cross-registry collisions and ownership ambiguity.

- `--safety-mode=dev`
  - Continues with high-visibility warnings.

`--strict` remains supported as a legacy alias.

### Multi-Registry Precedence (NEW in v5.6)

Multi-repo programs may maintain more than one registry set.

- **Primary registry:** `--registry-dir` (default `.spec/registry`)
- **Supplemental registries:** `--registry-roots` (read-only)

Precedence rules:

1) The primary registry is authoritative.
2) Supplemental registries are validation sources used to prevent cross-repo duplication.
3) Names found only in supplemental registries should be treated as likely cross-repo owners until clarified.

### UI Design Addendum

When your portfolio includes UI specs:

- **UI design source of truth** is `ui.json` inside the UI spec folder (Penpot-aligned) when the project uses JSON-first UI.
- `spec.md` documents constraints, mapping, and logic boundaries.
- UI JSON should not contain business logic.

Projects that do not use UI JSON are not affected.

---

## What the Audit Checks

If present, the workflow audits these registries:

1) `api-registry.json`
2) `data-model-registry.json`
3) `glossary.json`
4) `critical-sections-registry.json`
5) `patterns-registry.json` (optional)
6) `ui-component-registry.json` (optional)
7) `file-ownership-registry.json` (optional)

It also evaluates cross-SPEC usage signals from:

- the canonical SPEC_INDEX
- `spec.md` metadata
- `tasks.md` signals (when adjacent)
- `ui.json` references (when present)

### Examples of Drift Signals

- Near-duplicate domain terms across multiple specs
- Shared model names with conflicting field semantics
- APIs that appear semantically identical but differ in naming or versioning
- Critical cross-cutting requirements that vary between core specs
- UI component names used in multiple UI specs but not registered

---

## When to Use

### Use it when you:

- Have many SPECS maintained by multiple teams
- See repeated concepts with different names
- Are about to standardize APIs/domain models
- Suspect drift between public/private repos
- Want to improve long-term maintainability

### Skip it when you:

- Only need to validate index structure or path health
  - use `/smartspec_validate_index`

---

## Inputs & Resolution Rules

### SPEC_INDEX auto-detection order

If you do not pass `--index`, SmartSpec resolves the index in this order:

1) `.spec/SPEC_INDEX.json` (canonical)
2) `SPEC_INDEX.json` (legacy root mirror)
3) `.smartspec/SPEC_INDEX.json` (deprecated)
4) `specs/SPEC_INDEX.json` (older layout)

### Default directories

- `SPEC_HUB_DIR = ".spec"`
- `REGISTRY_DIR = ".spec/registry"`
- `REPORT_DIR = ".spec/reports/global-registry-audit"`

> Note: Reports remain project-owned and should not default to `.smartspec/`.

---

## Multi-Repo Support (v5.6)

Many large projects distribute specs across sibling repositories (e.g., public + private). The audit can search for spec artifacts across these repos.

You can configure multi-repo resolution in two ways:

### Option A) Simple workspace roots

```bash
/smartspec_global_registry_audit \
  --workspace-roots="../Repo-A,../Repo-B"
```

### Option B) Structured config

Create:

`.spec/smartspec.repos.json`

Example:

```json
{
  "version": "1.0",
  "repos": [
    { "id": "public",  "root": "../Repo-A" },
    { "id": "private", "root": "../Repo-B" }
  ]
}
```

Then run:

```bash
/smartspec_global_registry_audit --repos-config=.spec/smartspec.repos.json
```

### Default behavior

If neither `--workspace-roots` nor `--repos-config` is provided, the audit checks **only the current repo**.

---

## Multi-Registry Support (v5.6)

In multi-repo programs, shared names may exist in more than one registry set.

### Primary registry

```bash
--registry-dir=.spec/registry
```

### Supplemental registries (read-only)

```bash
--registry-roots="../Repo-A/.spec/registry,../Repo-B/.spec/registry"
```

The audit uses supplemental registries to:

- detect cross-repo collisions early
- identify likely owner registries
- reduce accidental duplication during spec/tasks generation

---

## Command Usage

### Basic audit

```bash
/smartspec_global_registry_audit
```

### Detailed report

```bash
/smartspec_global_registry_audit --report=detailed
```

### Portfolio interpretation (recommended for early roadmaps)

```bash
/smartspec_global_registry_audit --mode=portfolio
```

### Runtime interpretation (recommended before releases)

```bash
/smartspec_global_registry_audit --mode=runtime --safety-mode=strict
```

### Multi-repo + multi-registry audit

```bash
/smartspec_global_registry_audit \
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

### Interpretation

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
  - Print findings without writing files.

---

## Outputs

Reports are written to:

```text
.spec/reports/global-registry-audit/
```

Typical files:

- `global-registry-audit-summary-<timestamp>.md`
- `global-registry-audit-detailed-<timestamp>.md`

This workflow is **analysis-first**. It should not mutate registries unless your team explicitly adds a future append-only mode.

---

## How to Interpret Findings

### Glossary drift

- Near-duplicate terms often mean you need a canonical naming decision.
- Prefer registering a canonical term and listing aliases in the glossary.

### Data model drift

- Watch for collisions caused by parallel feature teams naming the same business concept differently.
- Use the audit output to drive a model ownership and evolution policy.

### API drift

- Similar endpoints with inconsistent naming often require a shared API namespace rule.
- Confirm consistency across core cross-cutting specs.

### Critical sections drift

- Variations across auth/authz/audit/rate-limiting specs are high-risk.
- Treat runtime-mode warnings in this area as release blockers.

### Cross-registry collisions (v5.6)

- If the same name exists in primary and supplemental registries with conflicting meaning:
  - treat the primary as authoritative
  - add a remediation plan to reconcile or formally declare the boundary

### UI component drift (optional)

- If `ui-component-registry.json` exists, align UI component names to it.
- If UI specs are active but `ui.json` is missing, prioritize creating `ui.json` before large-scale implementation.

---

## Best Practices

- Run after:
  - major spec additions
  - schema or API refactors
  - merging long-lived branches
- Combine with:
  - `/smartspec_portfolio_planner`
  - `/smartspec_validate_index`
  - `/smartspec_spec_lifecycle_manager`
- For multi-repo platforms:
  - run with `--registry-roots` to prevent cross-repo duplicate naming

---

## Troubleshooting

### “UI checks are noisy”

If your project has not adopted Penpot JSON-first UI yet:

- keep UI checks as warnings in portfolio mode
- ensure UI specs are not incorrectly categorized as `ui`
- migrate gradually

### “Audit misses specs in the private repo”

Provide multi-repo configuration:

```bash
/smartspec_global_registry_audit \
  --workspace-roots="../Repo-A,../Repo-B"
```

### “Audit reports shared-name conflicts across registries”

- Confirm primary vs supplemental registry roles.
- Decide the canonical owner.
- Update specs/tasks to reuse the declared owner.

---

## Summary

Global Registry Audit is SmartSpec’s long-term consistency guard. In v5.6, it remains aligned with the centralization model, supports optional UI JSON governance, and adds multi-registry safety so multi-repo ecosystems can keep shared names and cross-cutting constraints consistent without risky automatic rewrites.

