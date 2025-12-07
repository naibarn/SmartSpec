---
description: SmartSpec Global Registry Audit Guide (v5.2)
version: 5.2
last_updated: 2025-12-07
---

# SmartSpec Global Registry Audit Guide

This guide explains how to use `/smartspec_global_registry_audit` in SmartSpec v5.2.

Global Registry Audit is a governance workflow that scans your SmartSpec ecosystem to detect and reduce cross-SPEC naming and definition drift. It focuses on shared registries such as glossary, data models, API contracts, critical sections, and optional patterns/UI component registries.

Rather than silently rewriting your system, it produces **audit reports and alignment recommendations** for human review.

---

## Key Concepts

### SmartSpec Centralization (v5.2)

SmartSpec v5.2 separates **tooling** from **project-owned truth**.

- **Project-owned canonical space:** `.spec/`
- **Canonical index:** `.spec/SPEC_INDEX.json`
- **Shared registries (optional):** `.spec/registry/`
- **Legacy root mirror:** `SPEC_INDEX.json`
- **Deprecated tooling index:** `.smartspec/SPEC_INDEX.json`

The audit reads from the canonical layer when present and remains compatible with the existing `SPEC_INDEX.json` schema already used in production.

### Status-Aware Governance

Large systems often keep roadmap specs in the index before all files exist.

To avoid forcing low-quality placeholder specs, audit severities should be interpreted consistently with other v5.2 governance flows:

- `--mode=portfolio` (default)
  - Optimized for roadmap-level normalization.
  - Planned/backlog specs may be incomplete.

- `--mode=runtime`
  - Optimized for delivery readiness.
  - Drift that affects active/core/stable specs is treated with higher urgency.

### UI Design Addendum

When your portfolio includes UI specs:

- **UI design source of truth** is `ui.json` inside the UI spec folder (Penpot-aligned).
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
- **`REPORT_DIR = ".spec/reports/registry-audit"`**

> Note: In v5.2, reports are project-owned and should not default to `.smartspec/`.

---

## Multi-Repo Support (v5.2)

Many large projects distribute specs across sibling repositories (e.g., public + private). The audit can search for spec artifacts across these repos.

You can configure multi-repo resolution in two ways:

### Option A) Simple workspace roots

```bash
/smartspec_global_registry_audit \
  --workspace-roots="../Smart-AI-Hub,../smart-ai-hub-enterprise-security"
```

### Option B) Structured config

Create:

`.spec/smartspec.repos.json`

Example:

```json
{
  "version": "1.0",
  "repos": [
    { "id": "public", "root": "../Smart-AI-Hub" },
    { "id": "private", "root": "../smart-ai-hub-enterprise-security" }
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

## Command Usage

### Basic audit

```bash
/smartspec_global_registry_audit
```

### Detailed report

```bash
/smartspec_global_registry_audit --report-dir=.spec/reports/registry-audit
```

### Portfolio interpretation (recommended for early roadmaps)

```bash
/smartspec_global_registry_audit --mode=portfolio
```

### Runtime interpretation (recommended before releases)

```bash
/smartspec_global_registry_audit --mode=runtime --strict
```

### Multi-repo audit

```bash
/smartspec_global_registry_audit \
  --workspace-roots="../Smart-AI-Hub,../smart-ai-hub-enterprise-security" \
  --mode=portfolio
```

---

## Flags

### Index / Registry

- `--index`
  - Override SPEC_INDEX path.

- `--registry-dir`
  - Default: `.spec/registry`

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

- `--report-dir`
  - Default: `.spec/reports/registry-audit/`

- `--strict`
  - Fail on high-risk drift patterns that could break shared contracts.

- `--dry-run`
  - Print findings without writing files.

---

## Outputs

Reports are written to:

```text
.spec/reports/registry-audit/
```

Typical files:

- `registry-audit-summary-<timestamp>.md`
- `registry-audit-detailed-<timestamp>.md`

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
  --workspace-roots="../Smart-AI-Hub,../smart-ai-hub-enterprise-security"
```

---

## Summary

Global Registry Audit is SmartSpec’s long-term consistency guard. In v5.2, it aligns with the new centralization model, supports optional UI JSON governance, and can operate across multi-repo ecosystems to keep shared names and cross-cutting constraints consistent without risky automatic rewrites.

