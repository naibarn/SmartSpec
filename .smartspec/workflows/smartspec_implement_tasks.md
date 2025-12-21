---
description: Implement code changes strictly from tasks.md with 100% duplication prevention.
version: 7.0.0
workflow: /smartspec_implement_tasks
---

# smartspec_implement_tasks

> **Canonical path:** `.smartspec/workflows/smartspec_implement_tasks.md`  
> **Version:** 7.0.0  
> **Status:** Production Ready  
> **Category:** core

## Purpose

Implement code changes strictly from `tasks.md` with **100% duplication prevention** and **reuse-first** governance.

This workflow is the canonical entry point for:

- **preventing duplicate implementations** before they are created
- enforcing tasks-first execution
- enforcing reuse-first behavior (avoid duplicates)
- producing an auditable preview + diff before any governed writes

It is **safe-by-default** and writes governed artifacts only when explicitly applied.

---

## File Locations (Important for AI Agents)

**All SmartSpec configuration and registry files are located in the `.spec/` folder:**

- **Config:** `.spec/smartspec.config.yaml`
- **Spec Index:** `.spec/SPEC_INDEX.json`
- **Registry:** `.spec/registry/` (component registry, reuse index)
- **Reports:** `.spec/reports/` (workflow outputs, previews, diffs)
- **Scripts:** `.spec/scripts/` (automation scripts)

**When searching for these files, ALWAYS use the `.spec/` prefix from project root.**

---

## Governance contract

This workflow MUST follow:

- `knowledge_base_smartspec_handbook.md` (v6)
- `.spec/smartspec.config.yaml`

### Write scopes (enforced)

Allowed writes:

- Governed specs: `specs/**` (**requires** `--apply`)
- Safe outputs (previews/reports): `.spec/reports/implement-tasks/**` (no `--apply` required)

Forbidden writes (must hard-fail):

- Any path outside config `safety.allow_writes_only_under`
- Any path under config `safety.deny_writes_under` (e.g., `.spec/registry/**`, `.spec/cache/**`)
- Any runtime source tree modifications

### `--apply` behavior

- Without `--apply`:
  - MUST NOT modify `specs/**/tasks.md`.
  - MUST write a deterministic preview bundle to `.spec/reports/`.
- With `--apply`:
  - MAY update or create `specs/**/tasks.md`.
  - MUST NOT modify any other files.

---

## Behavior

### 1) Pre-Implementation Validation (MANDATORY)

Before implementing any task, the AI agent **MUST** check for existing similar components.

**Validation Command:**
```bash
python3 .spec/scripts/detect_duplicates.py \
  --registry-dir .spec/registry/ \
  --threshold 0.8
```

**Validation Rules:**
- **Exit Code `0` (Success):** No duplicates found. The agent may proceed.
- **Exit Code `1` (Failure):** Potential duplicates found. The agent **MUST**:
  - Present the duplicates to the user.
  - Ask the user to:
    a) Reuse existing components
    b) Justify creating new components
    c) Cancel and review existing specs
  - **MUST NOT** proceed until the user confirms.

### 2) Implement tasks

- Implement code changes strictly from `tasks.md`.
- Ensure every task has verifiable outputs (evidence hooks).

### 3) Preview & report (always)

Write:

- `.spec/reports/implement-tasks/<run-id>/report.md`
- `.spec/reports/implement-tasks/<run-id>/summary.json`
- `.spec/reports/implement-tasks/<run-id>/change_plan.md` (always generated when `--apply` is present; generated before any write)

### 4) Post-Implementation Validation (MANDATORY)

After implementing tasks and before applying changes, the AI agent **MUST** validate the changes.

**Validation Command:**
```bash
python3 .spec/scripts/validate_implementation.py \
  --tasks specs/<category>/<spec-id>/tasks.md \
  --spec specs/<category>/<spec-id>/spec.md \
  --registry .spec/registry/ \
  --check-duplicates --threshold 0.8
```

**Validation Rules:**
- **Exit Code `0` (Success):** The implementation is valid. The agent may proceed with `--apply`.
- **Exit Code `1` (Failure):** The implementation is invalid. The agent **MUST NOT** use `--apply`.
- The full output from the validation script **MUST** be included in `report.md`.

### 5) Apply (only with `--apply` and if validation passes)

- Update `specs/<category>/<spec-id>/tasks.md`.
- Apply code changes.

---

# End of workflow doc
