---
name: /smartspec_sync_tasks_checkboxes
version: 1.0.0
role: maintenance/governance
write_guard: TASKS-ONLY
purpose: Synchronize `tasks.md` checkbox status with evidence from `/smartspec_verify_tasks_progress`.
version_notes:
  - v1.0.0: initial workflow, designed to pair with /smartspec_verify_tasks_progress v5.8 evidence-first model.
---

# /smartspec_sync_tasks_checkboxes (v1.0.0)

This workflow updates `tasks.md` so that **checkboxes always match real evidence** gathered by
`/smartspec_verify_tasks_progress`.

- Tasks are marked complete (`[x]`) **only** when evidence says they are complete.
- Tasks are unmarked (`[ ]`) when evidence is missing or partial — even if they were manually checked.
- This guarantees that `tasks.md` is a trustworthy reflection of implementation reality.

The workflow **only edits `tasks.md`** and never touches:
- `spec.md`
- code files
- registry files
- UI JSON

---
## 1. Relationship with `/smartspec_verify_tasks_progress`

This workflow assumes that you already ran:

```bash
/smartspec_verify_tasks_progress \
  --spec <spec-path> \
  --report-format=json \
  --report=summary --dry-run \
  > .spec/reports/verify-tasks-progress/<spec-id>.json
```

The JSON report must contain per-task verdicts in the v5.8 evidence-first model:

- `verdict` ∈ {`complete`, `unsynced_complete`, `false_positive`, `partial`, `incomplete`}
- `id` corresponds to task IDs in `tasks.md` (e.g., `T001`, `T064`, etc.)

`/smartspec_sync_tasks_checkboxes` then:

- Reads the JSON report
- Parses `tasks.md`
- Updates checkboxes based on verdicts

---
## 2. Inputs & Flags

### 2.1 Core Inputs

```bash
--tasks=<path>       # required: path to tasks.md
--report=<path>      # optional: JSON report from verify-tasks
```

- If `--report` is omitted, an implementation **may** invoke
  `/smartspec_verify_tasks_progress --report-format=json --dry-run` internally and
  use its JSON output.

### 2.2 Mode & Safety

```bash
--mode=<safe|auto>   # default: safe
--dry-run            # compute changes but do not write
--safety-mode=<strict|dev>  # default: strict (aligns with other workflows)
--strict                    # alias for --safety-mode=strict
```

- `safe` mode:
  - generate a diff / summary of checkbox changes
  - require user confirmation (implementation-dependent) before applying
- `auto` mode:
  - apply changes directly (for CI / scripted use)
- `--dry-run`:
  - show what would change but leave `tasks.md` untouched

### 2.3 Optional Spec Hint

```bash
--spec=<path>        # optional, used only for context/logging
```

The `--spec` path may be used to:
- verify that `tasks.md` belongs to the same spec folder
- include spec metadata in logs or reports

---
## 3. Behavior

1. **Load JSON report**
   - Validate JSON structure and presence of `tasks[]` with `id` and `verdict`.

2. **Parse `tasks.md`**
   - Build a structured representation of tasks/subtasks.
   - Identify lines that correspond to task IDs (e.g., `T001`, `T064`, etc.).

3. **Apply verdict rules** for each task ID found in the JSON report:

   ```text
   verdict ∈ {complete, unsynced_complete}     → checkbox MUST be [x]
   verdict ∈ {false_positive, partial, incomplete} → checkbox MUST be [ ]
   ```

   - If a matching task line does not currently start with `[x]` or `[ ]`,
     the workflow **MAY** normalize it by prepending the correct marker.

4. **Parent task handling (optional)**
   - If an implementation supports an extra internal flag (e.g. `--recompute-parents`):
     - A parent task is marked `[x]` only when **all** of its subtasks have
       verdict ∈ {`complete`, `unsynced_complete`}.
     - Otherwise, the parent is set to `[ ]`.

5. **Write changes**
   - In `--dry-run` mode → only print the diff / summary.
   - In `--mode=safe` → prompt/confirm before writing.
   - In `--mode=auto` → write changes directly.

---
## 4. Output & Logging

The workflow should provide a clear summary, for example:

```text
/smartspec_sync_tasks_checkboxes --tasks specs/feature/spec-002-user-management/tasks.md \
  --report .spec/reports/verify-tasks-progress/spec-002-user-management.json \
  --mode=safe

Summary:
  23 tasks set to [x] (complete/unsynced_complete)
  11 tasks set to [ ] (false_positive/partial/incomplete)
  44 tasks unchanged

Diff:
  - [ ] T047: Implement phone verification add endpoint
  + [x] T047: Implement phone verification add endpoint
  - [x] T072: Performance tests for permission caching
  + [ ] T072: Performance tests for permission caching
```

This summary/diff may be printed to stdout or written to an optional log file.

---
## 5. Governance & Safety

- **Write scope**:
  - Only `tasks.md` is modified.
  - No other files (spec, code, registries, UI JSON) may be changed.

- **Change scope**:
  - Only the checkbox markers `[x]` and `[ ]` at the **start of task/subtask lines** may be edited.
  - Task titles, descriptions, estimates, and metadata must remain untouched.

- **Error handling** (especially in `strict` mode):
  - Missing or malformed JSON report → fail with a clear error message.
  - Unknown task IDs in the report → log and ignore; do not create new tasks.
  - If parsing `tasks.md` fails, no writes are performed.

---
## 6. Example End-to-End Flow

```bash
# 1) Generate evidence-first report
/smartspec_verify_tasks_progress \
  --spec specs/feature/spec-002-user-management/spec.md \
  --report-format=json --report=summary --dry-run \
  > .spec/reports/verify-tasks-progress/spec-002-user-management.json

# 2) Sync tasks.md checkboxes with verified evidence
/smartspec_sync_tasks_checkboxes \
  --tasks specs/feature/spec-002-user-management/tasks.md \
  --report .spec/reports/verify-tasks-progress/spec-002-user-management.json \
  --mode=safe
```

After this flow, `tasks.md` will:
- mark only evidence-backed tasks as complete
- unmark tasks whose completion cannot be proven by real code/tests
- provide a reliable base for future planning and implementation workflows.

