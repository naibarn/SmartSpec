# /smartspec_spec_lifecycle_manager.md

## Overview

**Spec Lifecycle Manager** governs the **life stages** of SPECS across a large system.
It addresses a common large-project failure mode:
SPECS remain effectively “active forever,” while deprecated content still influences new work.

This workflow enables:

- Clear lifecycle states (recommended: `draft`, `active`, `deprecated`, `archived`)
- Impact analysis for dependent SPECS
- Safer transitions in multi-repo projects
- Cleaner task generation rules

By default, it updates **only the canonical** index:

- `.spec/SPEC_INDEX.json`

---

## When to Use

### ✅ Use it when you:

- Want to deprecate or archive a spec safely
- Need to understand the impact of removing a contract
- Are preparing for a large refactor or platform migration
- Maintain both public and private repos

### ❌ Skip it when you:

- Only need to check index integrity (use `/smartspec_validate_index.md`)

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

### Deprecate a specific spec

```bash
/smartspec_spec_lifecycle_manager --spec-id=spec-120 --set-status=deprecated
```

### Archive a specific spec

```bash
/smartspec_spec_lifecycle_manager --spec-id=spec-045 --set-status=archived
```

### Report-only mode

```bash
/smartspec_spec_lifecycle_manager --category=deprecated --report-only
```

### Auto-propagation analysis

```bash
/smartspec_spec_lifecycle_manager --spec-id=spec-120 --set-status=deprecated --auto-propagate
```

---

## What It Updates (Schema-Preserving)

To remain compatible with existing workflows:

- If `status` exists in the index, this workflow updates it.
- If `status` does not exist, the workflow can:
  - update `category` in an additive, standardized way,
  - and recommend adding `status` in future revisions.

It should not rewrite unrelated fields.

---

## Impact Analysis Rules

When setting a spec to `deprecated`:

- List all **active dependents**
- Mark them as:
  - **at-risk** (report annotation)
  - not auto-changed unless a policy explicitly allows it

When setting a spec to `archived`:

- Raise a stronger warning if any dependents remain active.

---

## Public ↔ Private Policy

Recommended enforcement:

- Public specs that depend on private/core:
  - should treat private specs as **external contracts**
  - should not generate tasks that directly modify private code/specs
- If a public spec requires a private contract change:
  - create/update the private spec first

Lifecycle Manager should highlight violations in its report.

---

## UI-Specific Rules

If a spec is `category=ui`:

- Ensure a Penpot-editable design artifact is present:
  - `ui.json` (or configured filename)
- If missing:
  - report as **warning** (legacy UI mode)
  - recommend migration tasks

When deprecating a UI spec:

- Recommend archiving:
  - the design artifact
  - component bindings
  - and related tasks

---

## Outputs

Reports are written to:

```
.smartspec/reports/lifecycle/
```

Typical files:

- `lifecycle-summary-<timestamp>.md`
- `lifecycle-impact-<timestamp>.md`

---

## Best Practices

- Run in `--report-only` mode first when making large changes
- Deprecate before archive
- Use this workflow together with:
  - `/smartspec_portfolio_planner.md`
  - `/smartspec_global_registry_audit.md`
  - `/smartspec_validate_index.md`

---

## Summary

Spec Lifecycle Manager provides a safe, centralized way to evolve a large SmartSpec system.
It reduces hidden dependencies, prevents “zombie specs,”
and supports clean long-term platform maintenance.
