# SmartSpec Manual: /smartspec_implement_tasks

This guide explains how to implement tasks from `tasks.md` safely and predictably, aligned with the latest SmartSpec implementation workflow rules.

---

## What this command does

`/smartspec_implement_tasks` reads a `tasks.md` and performs implementation for a selected scope of tasks.

It may:

- Create or edit files listed in tasks
- Run validation commands
- Use Debug Mode when compile/tests fail
- Attempt Orchestrator Mode when `--kilocode` is provided
- Update task checkboxes to reflect **successfully completed tasks in this run**
- Produce a detailed **per-run final summary**

This command is the **implementation/fix** counterpart to `/smartspec_verify_tasks_progress`.

---

## Allowed file changes

This workflow is allowed to:

- Create/edit source files
- Add or update configuration files when required by tasks
- Update `tasks.md` checkboxes **only** for tasks completed in the current run

---

## Required input

Provide a path to `tasks.md`:

```bash
/smartspec_implement_tasks specs/feature/spec-005-promo-system/tasks.md
```

### Tasks file can be inside a folder

You can reference a nested tasks file path directly:

```bash
/smartspec_implement_tasks specs/feature/spec-004-financial-system/tasks.md
```

---

## Task scope selection (updated)

You can limit the run to a subset of tasks using any combination of the filters below.

### 1) Single task

```bash
/smartspec_implement_tasks specs/feature/spec-005-promo-system/tasks.md --tasks T021
```

### 2) Multiple tasks

```bash
/smartspec_implement_tasks specs/feature/spec-005-promo-system/tasks.md --tasks T021,T022,T023
```

### 3) Task ranges

```bash
/smartspec_implement_tasks specs/feature/spec-005-promo-system/tasks.md --tasks T001-T010
```

> `--task` is accepted as an alias for `--tasks` if supported by your runtime.

### 4) Start from a task

```bash
/smartspec_implement_tasks specs/feature/spec-005-promo-system/tasks.md --start-from T031
```

### 5) Skip completed tasks (recommended)

```bash
/smartspec_implement_tasks specs/feature/spec-005-promo-system/tasks.md --skip-completed
```

Expected behavior:

- Tasks already marked `[x]` should be skipped in this run.
- This reduces duplicate or overlapping implementations.

### 6) Resume

```bash
/smartspec_implement_tasks specs/feature/spec-005-promo-system/tasks.md --resume
```

Expected behavior:

- Continue from the last known checkpoint if your implementation supports checkpoints.

---

## Phase filtering (added)

If your `tasks.md` is structured by phases, you can implement tasks by phase.

### 1) A single phase

```bash
/smartspec_implement_tasks <tasks.md> --phase 1
```

### 2) Multiple phases

```bash
/smartspec_implement_tasks <tasks.md> --phase 1,2,3
```

### 3) A phase range

```bash
/smartspec_implement_tasks <tasks.md> --phase 1-3
```

Recommended pairing:

```bash
/smartspec_implement_tasks <tasks.md> --phase 2 --skip-completed
```

---

## Architect Mode

Use Architect Mode to force an implementation plan before coding.

```bash
/smartspec_implement_tasks specs/feature/spec-005-promo-system/tasks.md --tasks T021 --architect
```

Expected behavior:

- Produce an architecture/implementation plan for the task.
- Then proceed to code changes.

---

## KiloCode / Orchestrator Mode (updated)

### Key rule

**Orchestrator Mode is allowed only when `--kilocode` is explicitly set.**

```bash
/smartspec_implement_tasks specs/feature/spec-005-promo-system/tasks.md --tasks T001-T010 --kilocode
```

### What `--kilocode` now means

With the updated workflow rules:

- The system MUST **attempt** to activate Orchestrator Mode for tasks in scope.
- Actual activation may be blocked by platform/tool limits.

### Mandatory fallback behavior (Policy A)

If Orchestrator cannot be activated:

- The workflow must log a clear warning.
- The workflow must fall back to **Standard Implementation Mode** for that task.
- The run must continue.

This prevents a stalled run while keeping behavior transparent.

---

## Evidence-first integration rule (Auth/JWT/OAuth/OIDC)

For tasks that involve external integration assumptions — especially authentication/authorization tasks — the implement workflow must:

1. Read any explicitly referenced supporting specs.
2. Resolve spec IDs using:
   - `SPEC_INDEX.json` at repository root (preferred)
   - `.smartspec/SPEC_INDEX.json` (fallback)
3. Search the codebase for real evidence:
   - middleware/guards
   - API clients/gateway config
   - environment variables (`AUTH_*`, `JWT_*`, `OIDC_*`)
   - OpenAPI references

Only if no reliable evidence is found may it ask the user.

**The workflow must not auto-select a default assumption.**

---

## SPEC_INDEX.json resolution (updated)

When the workflow needs to map cross-spec dependencies:

1. Prefer `SPEC_INDEX.json` at repository root.
2. Fall back to `.smartspec/SPEC_INDEX.json`.

If neither exists:

- Log a warning.
- Continue with best-effort dependency handling.

---

## Validation options

### Validate-only

```bash
/smartspec_implement_tasks specs/feature/spec-005-promo-system/tasks.md --tasks T011-T020 --validate-only
```

Expected behavior:

- Do not modify code.
- Run relevant validations.
- Report pass/fail for the selected tasks.

---

## Checkbox update rules

A task should be marked `[x] only when:

- Implementation is complete for that task.
- The task-level validations/acceptance criteria pass per workflow rules.
- Success occurred **in this run**.

Tasks that fail must remain `[ ]`.

---

## Required final summary (per run)

At the end of an implement run, you should see a summary that is as informative as verification output but scoped to tasks in this run.

It should include:

- Tasks file path
- Filters used (`--tasks`, `--phase`, `--start-from`, etc.)
- Counts:
  - Completed
  - Failed
  - Skipped (dependencies/filters)
  - Not attempted (if the run stops early)
- Clear reasons for failures and skipped tasks
- Suggested next commands

This eliminates ambiguity about why later phases were not implemented.

---

## Examples

### Example 1: Phase-based implementation

```bash
# Implement Phase 1 only
/smartspec_implement_tasks specs/feature/spec-005-promo-system/tasks.md --phase 1 --skip-completed

# Continue to Phase 2 only
/smartspec_implement_tasks specs/feature/spec-005-promo-system/tasks.md --phase 2 --skip-completed
```

### Example 2: Safe iterative loop

```bash
# 1) Implement a chunk (prefer Orchestrator if available)
/smartspec_implement_tasks specs/feature/spec-005-promo-system/tasks.md --tasks T021-T030 --kilocode --skip-completed

# 2) Verify current status (read-only)
/smartspec_verify_tasks_progress specs/feature/spec-005-promo-system/tasks.md

# 3) Fix specific errors (if needed)
/smartspec_fix_errors specs/feature/spec-005-promo-system

# 4) Continue implementation
/smartspec_implement_tasks specs/feature/spec-005-promo-system/tasks.md --start-from T031 --skip-completed
```

### Example 3: Validate only for a phase

```bash
/smartspec_implement_tasks specs/feature/spec-005-promo-system/tasks.md --phase 3 --validate-only
```

---

## Troubleshooting

### Orchestrator does not appear even with `--kilocode`

Possible cause:

- Platform/tool limits.

Expected behavior after the update:

- You should see a warning indicating Orchestrator could not be activated.
- The workflow should fall back to Standard Mode and continue.

### “SPEC_INDEX.json not found”

Expected behavior:

- Prefer root `SPEC_INDEX.json`.
- Fall back to `.smartspec/SPEC_INDEX.json`.
- Continue with a warning if both are missing.

---

## Summary

Use `/smartspec_implement_tasks` to implement a well-defined subset of tasks with safe re-runs, evidence-driven integration decisions, and a detailed per-run final summary.

`--kilocode` enables Orchestrator attempts, and the system must gracefully fall back when Orchestrator is unavailable.
