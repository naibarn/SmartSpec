# SmartSpec Manual: /smartspec_verify_tasks_progress

This guide explains how to verify implementation progress against `tasks.md` without modifying code.

---

## What this command does

`/smartspec_verify_tasks_progress` provides a read-only assessment of implementation status by comparing:

- Expected tasks in `tasks.md`
- Actual files in the codebase
- Validation results
- Acceptance criteria

It is designed to answer:

- What is truly complete?
- What is partially implemented?
- What is missing?
- Which tasks are marked complete but fail verification?

---

## Strict boundaries (updated)

This workflow is **verification-only**.

It must not:

- Implement missing code
- Fix compilation/test errors
- Invoke Orchestrator Mode
- Read unrelated Kilo prompt templates

If `--kilocode` is present:

- It should be ignored or produce a warning.

---

## Required input

Provide a path to `tasks.md`:

```bash
/smartspec_verify_tasks_progress specs/feature/spec-005-promo-system/tasks.md
```

---

## Task scope selection

### 1) Single task

```bash
/smartspec_verify_tasks_progress specs/feature/spec-005-promo-system/tasks.md --tasks T021
```

### 2) Multiple tasks

```bash
/smartspec_verify_tasks_progress specs/feature/spec-005-promo-system/tasks.md --tasks T021,T022,T023
```

### 3) Task ranges

```bash
/smartspec_verify_tasks_progress specs/feature/spec-005-promo-system/tasks.md --tasks T001-T020
```

### 4) Start from a task

```bash
/smartspec_verify_tasks_progress specs/feature/spec-005-promo-system/tasks.md --start-from T031
```

---

## SPEC_INDEX.json resolution (updated)

When verifying cross-spec dependencies:

1. Prefer `SPEC_INDEX.json` at repository root.
2. Fall back to `.smartspec/SPEC_INDEX.json`.

If neither exists:

- Log a warning.
- Continue verification with best effort.

---

## How completion should be determined

A task should be considered complete only when the workflow can verify:

- Expected files exist
- For EDIT tasks, changes appear relevant to this SPEC (where such detection is supported)
- Acceptance criteria are satisfied
- In strict mode (if supported), validation commands pass

---

## Checkbox update behavior

Your implementation may support one of these patterns:

### Pattern A: explicit update flag

```bash
/smartspec_verify_tasks_progress specs/feature/spec-005-promo-system/tasks.md --update
```

### Pattern B: explicit no-update flag

```bash
/smartspec_verify_tasks_progress specs/feature/spec-005-promo-system/tasks.md --no-update
```

Expected safety rules:

- Verify may update `[ ] → [x]` only for fully verified tasks.
- Verify must **never** automatically uncheck tasks.
- If a task is marked `[x]` but fails verification, the report must warn clearly.

---

## Report expectations (updated)

The progress report should include:

- Overall completion estimate
- Phase-by-phase breakdown
- Task-by-task status with reasons
- A dedicated section for:

  **“Incomplete or Error Tasks (Verification Only)”**

This section is the authoritative list for what still requires work.

---

## Example: Verification loop

```bash
# Verify current state
/smartspec_verify_tasks_progress specs/feature/spec-005-promo-system/tasks.md

# Implement a targeted chunk
/smartspec_implement_tasks specs/feature/spec-005-promo-system/tasks.md --tasks T021-T030 --skip-completed

# Verify again
/smartspec_verify_tasks_progress specs/feature/spec-005-promo-system/tasks.md
```

---

## Troubleshooting

### Verification says tasks are incomplete but implement already ran

This usually means:

- Tasks were not fully validated
- Checkboxes were not updated (or were intentionally skipped)
- The implement run stopped early

Recommended action:

- Check the implement per-run summary.
- Re-run implement for specific tasks:

  ```bash
  /smartspec_implement_tasks specs/feature/spec-005-promo-system/tasks.md --tasks T0XX --skip-completed
  ```

### “SPEC_INDEX.json not found”

This should not block verification.

---

## Summary

Use `/smartspec_verify_tasks_progress` to get a truthful, read-only view of progress.  
It complements `/smartspec_implement_tasks`, which is responsible for actual fixes and code changes.
