# SmartSpec Command Manuals (Updated)

This document updates the user-facing manuals for the three core SmartSpec commands so they match the latest workflow logic we refined together:

1. `/smartspec_generate_tasks`
2. `/smartspec_implement_tasks`
3. `/smartspec_verify_tasks_progress`

It consolidates the most important behaviors, flags, and safety rules into one place.

---

## 1) /smartspec_generate_tasks

### Purpose
Generate a developer-ready `tasks.md` from a `spec.md`, while auto-detecting and (when appropriate) auto-generating supporting documents such as OpenAPI and data model references.

### Usage
```bash
/smartspec_generate_tasks <spec_path> [options]
```

### Primary Argument
- `spec_path` (required)
  - Path to the source `spec.md`.

### Options
- `--specindex <path>`
  - Use a custom SPEC index location.
- `--nogenerate`
  - Dry-run mode. Analyze and show what would be created without writing files.

### Updated SPEC_INDEX Resolution Rules
If `--specindex` is **not** provided, the workflow should auto-detect `SPEC_INDEX.json` with **project root as highest priority**.

Recommended search order:
1. `SPEC_INDEX.json` (project root)
2. `.smartspec/SPEC_INDEX.json`
3. `specs/SPEC_INDEX.json`
4. `.smartspec/spec-index.json`
5. `spec-index.json` (root)

If no SPEC index is found, the workflow should:
- Warn clearly.
- Offer a user choice for where to create it (root recommended).
- Allow continuing without index when the user explicitly chooses to skip.

### Supporting File Priority (Key Principle)
When building tasks, the generator should prioritize **actual source-of-truth artifacts** over descriptive text whenever they exist.

Suggested priority:
1. **Prisma schema** (if present) for canonical field names and models.
2. Existing OpenAPI specs.
3. Existing data model docs.
4. The SPEC text itself.

### Output
- `tasks.md` in the same folder as the SPEC.
- Optional auto-generated supporting files when triggered by SPEC content.

---

## 2) /smartspec_implement_tasks

### Purpose
Implement tasks from `tasks.md` safely and incrementally, with accurate progress tracking and per-run reporting.

### Usage
```bash
/smartspec_implement_tasks <tasks_path | spec_folder | implement-prompt.md> [options]
```

### Path Formats
```bash
# Direct tasks file
/smartspec_implement_tasks specs/feature/spec-005-promo-system/tasks.md

# Directory (auto-resolve tasks.md inside)
/smartspec_implement_tasks specs/feature/spec-005-promo-system

# Implement prompt file
/smartspec_implement_tasks specs/feature/spec-005-promo-system/implement-prompt-spec-005.md
```

### Mode & Safety Options
- `--skip-completed` (default)
  - Skip tasks already marked `[x]` in `tasks.md`.
- `--force-all`
  - Re-implement all tasks regardless of checkbox status.
- `--validate-only`
  - Run validation and status checks without implementing.

### Scope Options
- `--phase <n | n,m | n-m>`
- `--tasks <T001 | T001,T002 | T001-T010>`
- `--start-from <Txxx>`
  - Start at the given task and continue to the end of scope.
- `--resume`
  - Resume from the last checkpoint file.

### Execution Options
- `--architect`
  - Force an architecture plan before implementation.
- `--kilocode`
  - **The only flag that may enable Orchestrator Mode.**

### Updated Orchestrator Safety Rule
To avoid accidental mode switching:
- **Orchestrator Mode is allowed ONLY when `--kilocode` is set.**
- Without `--kilocode`, the workflow must not mention or attempt an Orchestrator switch as a hidden fallback.

### Updated SPEC Resolution Before Assumptions
For integration-sensitive tasks (especially auth-related):
1. Read any explicitly referenced supporting spec files.
2. Resolve spec IDs using:
   - `SPEC_INDEX.json` at root (preferred)
   - `.smartspec/SPEC_INDEX.json` (fallback)
3. Search the existing codebase for real evidence.

If evidence is missing:
- The workflow may ask the user.
- The workflow must not auto-select a default assumption.

### Validation & Error Handling
After each task in scope:
- Run validation commands defined in `tasks.md` frontmatter if available.
- Otherwise use reasonable defaults for the stack.

If validation fails:
- Attempt a targeted fix.
- Use Debug Mode if needed.
- Use Orchestrator fallback **only** when `--kilocode` is true.

### Checkbox Updates
A task should be marked `[x]` only when:
- The implementation is complete for that task.
- The task’s required validations/acceptance criteria pass per workflow rules.

### Required Final Summary (Per Run)
At the end of a run, the workflow should output a summary that is as informative as the verification report but scoped only to tasks processed in this run:
- Tasks in scope
- Completed / failed / skipped
- List of files created/edited
- Validation outcomes
- Clear next-step command suggestions

---

## 3) /smartspec_verify_tasks_progress

### Purpose
Read-only verification of implementation progress by comparing `tasks.md` against the codebase and validations.

This workflow should **report** and optionally **update checkboxes**, but **never fix code**.

### Usage
```bash
/smartspec_verify_tasks_progress <tasks_path> [options]
```

### Scope Options
- `--tasks <range>` or `--task <range>` (alias)
- `--start-from <Txxx>`
- `--phase <name_or_id>`

### Update Behavior
- Default: verification-only (no code changes).
- Checkbox update behavior should depend on the workflow’s supported flag.
  - If your implementation supports `--update`, use it to mark verified-complete tasks.
  - If your implementation supports `--no-update`, treat it as an explicit guardrail.

### Updated Safety Rules
- **This workflow must NOT invoke Orchestrator Mode.**
- If `--kilocode` is present, it should be ignored or trigger a warning.
- The workflow must not read unrelated Kilo prompt templates that are not required for verification.

### Completion Criteria Expectations
A task should be considered complete only when the workflow can verify:
- All expected files exist (and where relevant, are actually modified for this SPEC).
- Acceptance criteria are satisfied.
- In strict mode (if enabled), all relevant validation commands pass.

### Output
- A progress report file in the same folder as `tasks.md` by default.
- A backup of `tasks.md` before any checkbox updates (if updates are enabled).

---

## Recommended End-to-End Flow

```bash
# 1) Generate tasks from spec
/smartspec_generate_tasks specs/feature/spec-005-promo-system/spec.md

# 2) Implement incrementally
/smartspec_implement_tasks specs/feature/spec-005-promo-system/tasks.md --phase 1

# 3) Verify progress (read-only)
/smartspec_verify_tasks_progress specs/feature/spec-005-promo-system/tasks.md

# 4) Update checkboxes when you want the file to reflect reality
/smartspec_verify_tasks_progress specs/feature/spec-005-promo-system/tasks.md --update

# 5) Continue implementation safely
/smartspec_implement_tasks specs/feature/spec-005-promo-system/tasks.md --start-from T031
```

---

## Notes on UI Confirmation Prompts

Some Kilo UI checkpoints may still present choice buttons (e.g., architecture approval). Even if they appear, the workflow-backed behavior should be:
- Use specs and code evidence first.
- Avoid auto-assumptions for external integration details.
- Treat architecture confirmation as a plan-approval gate, not an assumption roulette.

---

## Change Log (Manual-Level)

- Updated `/smartspec_generate_tasks` documentation to reflect root-first SPEC_INDEX detection, multi-path fallback, and safer missing-index handling.
- Updated `/smartspec_implement_tasks` documentation to affirm:
  - Orchestrator Mode is **only** allowed with `--kilocode`.
  - Integration assumptions must be evidence-driven (spec → code) before asking the user.
  - Final per-run summary is required.
- Updated `/smartspec_verify_tasks_progress` documentation to emphasize verification-only behavior and no Orchestrator usage.

---

## What You Can Replace in Your Repo

You can use this document to update the three standalone manuals:
- `generate_tasks.md`
- `implement_tasks.md`
- `verify_tasks_progress.md`

If you prefer, I can split this into three separate updated files in the same style as your existing docs.

