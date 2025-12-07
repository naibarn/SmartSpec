# /smartspec_global_registry_audit.md

## Overview

**Global Registry Audit** is a governance workflow that scans your **entire SmartSpec system**
to detect and reduce cross-SPEC naming and definition drift.

It focuses on shared registries such as:

- Glossary
- Data models
- API contracts
- Critical sections
- Optional UI component registry

Instead of silently rewriting your system,
it produces **reports and alignment task proposals** for human review.

---

## When to Use

### ✅ Use it when you:

- Have many SPECS maintained by multiple teams
- See repeated concepts with different names
- Are about to standardize APIs or domain models
- Want to improve long-term maintainability

### ❌ Skip it when you:

- Only need to validate index structure (use `/smartspec_validate_index.md`)
- Are working on a tiny feature with no shared domain impact

---

## Inputs & Resolution Rules

### SPEC_INDEX resolution order

1. `--specindex="<path>"`
2. `.spec/SPEC_INDEX.json`
3. `SPEC_INDEX.json` (legacy)
4. `.smartspec/SPEC_INDEX.json` (legacy)
5. `specs/SPEC_INDEX.json` (legacy)

### Default directories

- `SPEC_HUB_DIR = ".spec"`
- `REGISTRY_DIR = ".spec/registry"`
- `OUTPUT_DIR = ".smartspec"`

---

## Command Usage

### Basic audit

```bash
/smartspec_global_registry_audit
```

### Narrow scope by tag or domain

```bash
/smartspec_global_registry_audit --scope=security
```

### Detailed report

```bash
/smartspec_global_registry_audit --report=detailed
```

### Emit alignment task proposals

```bash
/smartspec_global_registry_audit --emit-alignment-tasks
```

---

## What It Checks

### 1) Glossary drift

- Near-duplicate terms
- Missing canonical terms used across specs
- Candidate aliases

### 2) Data model drift

- Entity names with overlapping meaning
- Field-name collisions
- Registry-vs-spec mismatch

### 3) API drift

- Similar endpoints with inconsistent naming
- Resource naming divergence

### 4) Critical-sections coverage

- Whether high-risk domains are documented consistently

### 5) UI component drift (optional)

If your project uses UI centralization:

- Verify that UI specs reference canonical component names
- Check:
  - `.spec/registry/ui-component-registry.json`
  - and `ui.json` artifacts
- Flag missing or inconsistent bindings

---

## Outputs

Reports are written to:

```
.smartspec/reports/registry-audit/
```

Typical files:

- `registry-audit-summary-<timestamp>.md`
- `registry-audit-detailed-<timestamp>.md`

When `--emit-alignment-tasks` is used:

- Per-spec proposal files may be generated, e.g.:

```
.smartspec/reports/registry-audit/alignment-tasks.spec-123.md
```

These files should not overwrite your existing `tasks.md` automatically.

---

## Best Practices

- Run after:
  - major spec additions
  - schema or API refactors
  - merging long-lived branches
- Combine with:
  - `/smartspec_portfolio_planner.md`
  - `/smartspec_generate_tasks.md`
  - `/smartspec_sync_spec_tasks.md`

---

## Troubleshooting

### “UI checks are noisy”

If your project has not adopted Penpot JSON-first UI yet:

- Keep UI checks as warnings,
- Use legacy UI mode,
- Migrate gradually.

---

## Summary

Global Registry Audit is your long-term consistency guard.
It helps keep a multi-team, multi-spec system aligned
without forcing risky automatic rewrites.
