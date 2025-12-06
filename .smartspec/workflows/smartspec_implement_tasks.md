---
description: Implement tasks from tasks.md using SmartSpec, with optional Architect Mode and KiloCode Orchestrator Mode, update tasks.md checkboxes, and produce a detailed per-run summary. This workflow is the implementation/fix counterpart to smartspec_verify_tasks_progress (which is verification-only).
---

## User Input

```text
$ARGUMENTS
```

Expected example:

```bash
/smartspec_implement_tasks specs/feature/spec-004-financial-system/tasks.md --tasks T001-T090 --kilocode --skip-completed
```

This workflow describes how `/smartspec_implement_tasks` should behave.

- **This workflow is allowed to change code** (implement/fix tasks).
- It operates only on the tasks in the current run (scope).
- It **does not** attempt to verify the entire SPEC; that is the job of `/smartspec_verify_tasks_progress`.

---

## 0. Load Context

Load only the context required to implement tasks for a single SPEC:

1. From project root:
   - `SPEC_INDEX.json` (preferred, if present at the repository root)
   - If not found, optionally try `.smartspec/SPEC_INDEX.json`.
     - If the fallback file is also missing, log a warning but **do not fail** the workflow. Continue without SPEC index data.

2. From the target SPEC:
   - The `tasks.md` file from `$ARGUMENTS`
   - Any referenced spec files (e.g., `spec.md`, `architecture.md`, `openapi.yaml`, `data-model.md`)

3. Do **NOT** load KILO prompt templates as plain text (they are invoked via tools, not read as content):
   - Skip `.smartspec/KILO-PROMPT*`
   - Skip `.smartspec/KILO-ASK*`
   - Skip `.smartspec/KILO-ARCHITECT*`
   - Skip `.smartspec/KILO-CODE*`
   - Skip `.smartspec/KILO-DEBUG*`
   - Skip `.smartspec/KILO-TEST*`

Goal: keep context focused on the SPEC and its tasks, not on implementation prompt templates.

---

## 1. Resolve Path and Parse Arguments

### 1.1 Resolve TASKS_PATH

1. If `$ARGUMENTS` contains an explicit path ending with `tasks.md`, use it as `TASKS_PATH`.
2. Otherwise, if the currently active file is a `tasks.md`, use that.
3. Normalize to a project-relative path, e.g.:

```text
specs/feature/spec-004-financial-system/tasks.md
```

If `TASKS_PATH` cannot be resolved → stop with a clear error.

### 1.2 Supported CLI Flags

Parse the following flags:

- `--tasks <RANGE>` (optional)
  - Filter which tasks to run.
  - Supports:
    - Single ID: `T005`
    - Comma-separated list: `T001,T003,T010`
    - Ranges: `T001-T010`
    - Mixed: `T001-T005,T010,T020-T022`

- `--task <RANGE>` (alias for `--tasks`)

- `--start-from <TASK_ID>` (optional)
  - Start processing from this task ID (inclusive), based on order in `tasks.md`.

- `--resume` (optional)
  - Continue from a previous checkpoint, if available.

- `--skip-completed` (optional)
  - Skip tasks whose checkbox is already `[x]` in `tasks.md`.
  - This is recommended when running again after earlier passes or after verification.

- `--validate-only` (optional)
  - Do not change code; only run validation commands per task.
  - Useful to quickly check the impact of code that was already written.

- `--architect` (optional)
  - For each task, run Architect Mode first to design an implementation plan before coding.

- `--kilocode` (optional, **KiloCode-only feature**)
  - Enable Orchestrator Mode for implementation and error-handling.
  - **Important:** The workflow must **attempt** to use Orchestrator Mode when this flag is set, but actual activation depends on system/tool limits.

Store parsed options into a configuration object:

```python
options = {
  "task_selector_raw": "...",       # from --tasks/--task
  "start_from": "T010" or None,
  "resume": bool,
  "skip_completed": bool,
  "validate_only": bool,
  "architect": bool,
  "kilocode": bool,
}
```

### 1.3 Parse Task Selector

If `task_selector_raw` is provided:

1. Split by comma.
2. For each token:
   - If it matches `T\d+` → single task ID.
   - If it matches `T\d+-T\d+` → expand numeric range (e.g., `T001-T003` → `T001,T002,T003`).
3. Collect unique task IDs in order.

Result:

```python
selected_task_ids = ["T001", "T002", "T003", ...]
```

---

## 2. Parse tasks.md

Parse `tasks.md` into a structured list of phases and tasks.

For each task `T00X`, extract:

- `phase` (e.g., `"Phase 1: Foundation"`)
- `id` (e.g., `"T001"`)
- `title`
- `description` (optional)
- `estimate` (optional, e.g., `"2h"`)
- `dependencies` (task IDs or spec IDs)
- `files` (list of file operations)
  - `operation`: `CREATE` | `EDIT`
  - `path`: file path (e.g., `src/services/promo-code.service.ts`)
  - `size_category`: `SMALL` / `MEDIUM` / `LARGE` (if specified or inferred)
- `acceptance_criteria` (list of textual criteria)
- `validation_commands` (e.g. `npm test`, `npm run lint`, `npm run test promo`)
- `checkbox_state`:
  - `"checked"`   if line starts with `- [x] T001:`
  - `"unchecked"` if line starts with `- [ ] T001:`

Example task header pattern:

```text
- [ ] T001: Initialize Promo System (2h)
- [x] T002: Setup Promo Database (1h)
```

Regex (conceptual):

```text
^- \[( |x)\] (T[0-9]{3}): (.*)$
```

Return:

```python
tasks = [
  {
    "phase": "Phase 1: Foundation",
    "id": "T001",
    "title": "Initialize Promo System",
    "description": "...",
    "dependencies": [],
    "files": [...],
    "acceptance_criteria": [...],
    "validation_commands": [...],
    "checkbox_state": "unchecked",
  },
  ...
]
```

---

## 3. Filter Scope

Determine which tasks to process in this run.

### 3.1 Apply Task Selector

If `selected_task_ids` is not empty:

- Keep only tasks where `task.id` is in `selected_task_ids`.
- Preserve original order from `tasks.md`.

### 3.2 Apply `--start-from`

If `options["start_from"]` is set:

- Find the first index `i` where `tasks[i].id == start_from`.
- Keep tasks from `i` onward.

### 3.3 Apply `--skip-completed`

If `options["skip_completed"]` is true:

- Remove tasks where `task.checkbox_state == "checked"`.

### 3.4 Apply Resume Logic

If `options["resume"]` is true and a checkpoint exists:

- Load checkpoint data.
- Skip tasks already recorded as completed in checkpoint.
- Optionally resume from last processed index.

The final ordered list is `FILTERED_TASKS`.

If `FILTERED_TASKS` is empty → report and stop.

---

## 4. Initialize Tracking (Per-Run Status)

Create tracking structures for **this run only**:

```python
current_task_index = 0
total_tasks = len(FILTERED_TASKS)

completed_tasks = []      # tasks successfully implemented + validated in THIS run
failed_tasks = []         # tasks attempted but failed
skipped_tasks = []        # tasks skipped due to dependency / filter / explicit logic
not_attempted_tasks = []  # tasks in FILTERED_TASKS that were never reached because the run stopped early

completed_count = 0
failed_count = 0
skipped_count = 0
not_attempted_count = 0
```

Also initialize:

```python
failed_in_a_row = 0
max_consecutive_failures = 3   # safety limit to stop the run early
run_stopped_early = False
stop_reason = None  # e.g. "3 consecutive failures", "manual abort"
```

> `not_attempted_tasks` is crucial to explain why a later phase may not have been implemented even if the user specified a full range like `T001-T090`. Any task in `FILTERED_TASKS` that is never processed because the loop terminated early must be recorded here.

---

## 5. Main Loop

Iterate over each task in `FILTERED_TASKS` **until**:

- All tasks processed, or
- Global stop condition is triggered (e.g., too many consecutive failures).

```python
for task in FILTERED_TASKS:
    if run_stopped_early:
        # This and all subsequent tasks in FILTERED_TASKS were not attempted
        not_attempted_tasks.append({
            "task": task,
            "reason": stop_reason or "Run stopped early before this task was reached."
        })
        not_attempted_count += 1
        continue

    current_task_index += 1
    implement_single_task(task, options, tracking_state)
```

`tracking_state` includes references to:

- `completed_tasks`, `failed_tasks`, `skipped_tasks`, `not_attempted_tasks`
- counts
- `failed_in_a_row`, `run_stopped_early`, `stop_reason`

---

## 6. Per-Task Workflow

### 6.1 Check Dependencies

For each dependency in `task.dependencies`:

- If dependency is a task ID:
  - Check if that task is in `completed_tasks` or already `[x]` in `tasks.md`.
- If dependency is a spec ID:
  - If SPEC index data was loaded:
    - Check `SPEC_INDEX.json` (root) or `.smartspec/SPEC_INDEX.json` (fallback) for that spec and its "implemented" status.
  - If SPEC index is unavailable:
    - Treat dependencies conservatively or log a warning.

If any dependency is not satisfied:

- Mark task as **skipped** for this run:
  - Checkbox remains unchanged.
  - Add to `skipped_tasks` with a reason, e.g. `"Depends on incomplete T00X"`.
  - Increment `skipped_count`.
  - Log:

    ```text
    ⏭️ Skipped {task.id}: depends on incomplete {dependency_id}
    ```

- Continue to next task.

### 6.2 Read Task Details

For each task, confirm:

- Files to create/edit.
- File size categories (SMALL / MEDIUM / LARGE).
- Supporting references (OpenAPI, data model, other docs) as needed.

### 6.3 Implement Task (If Not Validate-Only)

If `options["validate_only"]` is true:

- **Skip code changes**, jump to validation (6.4).
- This run will only report whether the existing implementation passes validation.

Otherwise, choose the implementation mode:

#### 6.3.1 Architect Mode (optional)

If `options["architect"]` is true:

- Invoke Architect Mode for this task:

  ```text
  Use Architect Mode to design the system architecture and create implementation plan.
  {task_id}: {task_title}
  ```

- Architect Mode should:
  - Design structure.
  - Define modules/files/responsibilities.
  - Define data flows/interfaces.
  - Produce a concrete plan for coding.

#### 6.3.2 Orchestrator Mode (KiloCode-only, with fallback)

If `options["kilocode"]` is **true**:

- The workflow MUST **attempt** to enable Orchestrator Mode for this task:

  ```text
  Attempt to use Orchestrator Mode to break this task into subtasks. {task_id}: {task_title}.
  ```

- If Orchestrator Mode is successfully activated:
  - Use it to:
    - Analyze task complexity.
    - Optionally use Architect Mode.
    - Break into Ask → Architect → Code → Debug → Test.
    - Coordinate all sub-steps until the task is ready for validation.

- If Orchestrator activation **fails** (e.g. due to tool limit, system restriction, or other non-task error):

  1. Log a clear warning, for example:

     ```text
     ⚠️ Orchestrator Mode could not be activated for {task.id} (system/tool limit). Falling back to Standard Implementation Mode for this task.
     ```

  2. Continue implementing this task using **Standard Implementation Mode** (Section 6.3.3) instead of Orchestrator.

- The workflow must **never silently pretend** that Orchestrator Mode is active when it is not. Any fallback must be explicitly logged.

> Note: `--kilocode` means “prefer Orchestrator when available”. It does **not** guarantee Orchestrator will be active if the underlying platform blocks it. In those cases, this workflow will continue in Standard Mode to avoid wasting the run.

#### 6.3.3 Standard Implementation Mode (no Orchestrator)

Standard Implementation Mode is used when:

- `options["kilocode"]` is **false**, or
- Orchestrator activation failed and the workflow fell back as described above.

Use a standard implementation strategy based on file size:

- **SMALL files (< 200 lines):**
  - CREATE: generate full file content in one pass.
  - EDIT: full rewrite or small targeted `str_replace`.

- **MEDIUM files (200–500 lines):**
  - CREATE: staged creation (outline → fill).
  - EDIT: `str_replace` with strict line limits.

- **LARGE files (> 500 lines):**
  - CREATE: incremental build in sections.
  - EDIT: surgical `str_replace` only.

Implementation attempts should always aim to:

- Satisfy acceptance criteria.
- Keep code consistent with existing architecture.
- Avoid duplicating logic when re-run; prefer idempotent patterns (e.g. replace blocks instead of continually appending).

### 6.3.4 Implementation Error Handling

If implementation fails for a particular operation (e.g., unable to locate snippet for `str_replace`):

1. Attempt a small number of retries with slightly extended context.
2. If still failing:
   - Mark this operation as failed for this task.
   - Do **not** attempt any hidden Orchestrator switch unless `options["kilocode"]` is true **and** Orchestrator is actually available.
   - Continue with remaining operations if appropriate, or mark the task as a hard failure.

If a task ends in a hard failure (before or after validation):

- Add it to `failed_tasks` with an error summary.
- Increment `failed_count` and `failed_in_a_row`.
- If `failed_in_a_row >= max_consecutive_failures`:
  - Set:

    ```python
    run_stopped_early = True
    stop_reason = "Reached max_consecutive_failures limit"
    ```

  - Do **not** process further tasks in this run (they will be recorded as `not_attempted_tasks`).

### 6.4 Validate Task

After implementation (or in `--validate-only` mode), run validation:

- Use `task.validation_commands` if present, otherwise fall back to project-level defaults (e.g. compile/test/lint).

Evaluate success:

- If all relevant validations pass:
  - Consider validation successful.
- If any validation fails:
  - Optionally attempt Debug Mode.

#### 6.4.1 Debug Mode

If validation fails:

- Use Debug Mode:

  ```text
  Use Debug Mode to analyze and fix the issue for {task_id}: {task_title}.
  ```

- Debug Mode may:
  - Read error messages, stack traces, logs.
  - Inspect relevant source files.
  - Apply focused fixes.
  - Re-run only affected validations.

If Debug Mode fixes the issue → treat as success.

If Debug Mode still fails:

- If `options["kilocode"]` is **true** and Orchestrator is available:
  - Orchestrator fallback is allowed for this task:

    ```text
    Use Orchestrator Mode to resolve the issue for {task_id}: {task_title}.
    ```

- If Orchestrator is not available or `options["kilocode"]` is **false**:
  - Do **not** attempt Orchestrator.
  - Mark the task as failed; keep checkbox as `[ ]`.
  - Update tracking (failed_tasks, failed_count, failed_in_a_row).
  - Possibly trigger global stop if `failed_in_a_row` hits the configured limit.

### 6.5 Mark Task as Successful

If implementation + validation complete successfully:

- Add `task.id` (and other metadata) to `completed_tasks`.
- Increase `completed_count`.
- Reset `failed_in_a_row = 0`.
- Prepare to update checkbox in `tasks.md` (see Section 7).

---

## 7. Update tasks.md Checkboxes

For tasks that were **successfully completed in this run**:

- If their current `checkbox_state == "unchecked"`:
  - Update the line in `tasks.md`:

    ```text
    - [ ] T001: Title
    ```

    to:

    ```text
    - [x] T001: Title
    ```

Implementation sketch:

```python
with open(TASKS_FILE, "r", encoding="utf-8") as f:
    content = f.read()

for t in completed_tasks:
    task_id = t["id"]
    pattern = f"- [ ] {task_id}:"
    replacement = f"- [x] {task_id}:"
    content = content.replace(pattern, replacement)

with open(TASKS_FILE, "w", encoding="utf-8") as f:
    f.write(content)
```

> This only changes checkboxes for tasks that are **actually completed in this run** (implementation + validation).  
> Tasks that fail remain `[ ]`. Tasks already `[x]` stay `[x]`.

You may optionally re-read `tasks.md` and verify that checkbox updates were applied as expected.

---

## 8. Final Per-Run Summary (Detailed, Task-Focused)

To avoid situations where the user finishes `/smartspec_implement_tasks` but does not know which tasks are incomplete, the workflow MUST produce a **clear, detailed summary** for this run only.

This summary should answer:

- Which tasks were **completed** in this run?
- Which tasks **failed**, and why?
- Which tasks were **skipped** due to dependencies or filters?
- Which tasks in the requested range were **not even attempted** because the run stopped early?

### 8.1 Build Per-Task Status Table

For each task in `FILTERED_TASKS`, assign one of:

- `COMPLETED`
- `FAILED`
- `SKIPPED`
- `NOT_ATTEMPTED`

With a short reason.

Pseudo:

```python
per_task_status = []

for task in FILTERED_TASKS:
    record = {
        "id": task.id,
        "title": task.title,
        "phase": task.phase,
        "status": None,
        "reason": None,
    }

    if any(t["id"] == task.id for t in completed_tasks):
        record["status"] = "COMPLETED"
        record["reason"] = "Implemented and validated in this run."
    elif any(t["id"] == task.id for t in failed_tasks):
        record["status"] = "FAILED"
        record["reason"] = get_fail_reason_for(task.id)
    elif any(t["task"].id == task.id for t in skipped_tasks):
        record["status"] = "SKIPPED"
        record["reason"] = get_skip_reason_for(task.id)
    elif any(t["task"].id == task.id for t in not_attempted_tasks):
        record["status"] = "NOT_ATTEMPTED"
        record["reason"] = get_not_attempted_reason_for(task.id)  # e.g. global stop
    else:
        record["status"] = "UNKNOWN"
        record["reason"] = "No record for this task in this run."

    per_task_status.append(record)
```

### 8.2 Console Summary (Human-Friendly)

Print a compact but clear summary:

```text
📊 Implementation run finished.

Scope in this run:
- Tasks file: specs/feature/spec-005-promo-system/tasks.md
- Tasks in scope: T001-T090 (based on filters)

In this run:
- ✅ Completed:   {completed_count} tasks
- ❌ Failed:      {failed_count} tasks
- ⏭️ Skipped:     {skipped_count} tasks (dependencies / filters)
- 🚫 Not run:     {not_attempted_count} tasks (not attempted because the run stopped early)

Run stop reason: {stop_reason or "None (all tasks processed)"}
```

Then show grouped lists, for example:

```text
✅ Completed in this run:
- T011: Setup promo schema (Phase 2)
- T012: Add Campaign model (Phase 2)
...

❌ Failed in this run:
- T021: Implement promo auth middleware (Phase 3) – TypeScript errors remain after Debug Mode
- T022: Add promo tests (Phase 3) – Jest tests still failing (3 tests red)

⏭️ Skipped in this run:
- T015: Generate API docs (Phase 1) – depends on incomplete T010

🚫 Not attempted in this run:
- T081-T090: Phase 9 tasks – Run stopped early before these were reached
```

This makes it immediately clear why a later phase may not have been implemented even if the user specified a wide range like `--tasks T001-T090`.

### 8.3 Optional: Per-Phase Summary (This Run Only)

You may also build a per-phase summary **restricted to this run**:

```markdown
## Per-Phase Summary (This Run Only)

- Phase 1: 3 completed, 2 failed, 1 skipped, 0 not attempted
- Phase 2: 8 completed, 0 failed, 0 skipped, 0 not attempted
- Phase 3: 1 completed, 3 failed, 0 skipped, 6 not attempted
- Phase 4: 0 completed, 0 failed, 0 skipped, 10 not attempted
```

### 8.4 Implementation Report (Optional File)

Optionally, write a markdown report for this run:

- `implementation-report-YYYYMMDD-HHmm.md` in the same directory as `tasks.md`.
- Contents:
  - Scope (tasks file, filters).
  - Per-run statistics (counts).
  - Detailed per-task table (status + reason).
  - Error summaries for failed tasks.
  - List of not-attempted tasks with explanation.
  - Suggested next commands, e.g.:

    ```bash
    # To continue from first failed or not-attempted task:
    /smartspec_implement_tasks specs/feature/spec-005-promo-system/tasks.md --start-from T031 --skip-completed
    ```

---

## 9. Relationship with smartspec_verify_tasks_progress

To keep behavior consistent and predictable:

- `/smartspec_implement_tasks`:
  - **Can change code** (implement/fix tasks).
  - Works on a selected subset of tasks in a given run.
  - Updates checkboxes for tasks completed in that run.
  - Produces a **per-run summary** of which tasks were completed/failed/skipped/not-attempted.

- `/smartspec_verify_tasks_progress`:
  - Is **verification-only** (no code changes).
  - Reads the **current state** of the entire SPEC (or filtered set of tasks).
  - Runs validation, checks acceptance criteria, and reports incomplete/error tasks.
  - Optionally updates checkboxes only for tasks that pass full verification.

Recommended usage pattern:

1. Use `/smartspec_implement_tasks` to implement or fix a group of tasks (e.g. a phase or range).
2. Then use `/smartspec_verify_tasks_progress` to verify the broader state of the SPEC.
3. Based on the verify report:
   - Re-run `/smartspec_implement_tasks` for specific tasks or ranges.
   - Or use `/smartspec_fix_errors` / `/smartspec_generate_tests` as suggested.

---

## 10. Rules About Orchestrator Mode (KiloCode)

To avoid accidental or misleading mode switching:

1. `--kilocode` means: **“attempt to use Orchestrator Mode when available”**, not “guarantee Orchestrator Mode”.

2. Orchestrator Mode is **only allowed** when the `--kilocode` flag is set.  
   - If `--kilocode` is not set:
     - The workflow may use **Standard Implementation Mode**, **Architect Mode**, and **Debug Mode** only.
     - It must **not** route to Orchestrator as a hidden fallback.

3. When `--kilocode` **is** set:
   - The workflow MUST attempt to activate Orchestrator Mode for each task.
   - If the underlying platform/tool **allows** Orchestrator:
     - Use Orchestrator for task implementation and complex error-handling.
   - If the platform/tool **blocks** Orchestrator (tool limit, quota, or similar):
     - Log a clear warning for the user.
     - Fall back to Standard Implementation Mode for that task (and continue the run).
     - Do **not** silently claim Orchestrator is active when it is not.

4. In irrecoverable failure cases (e.g., many consecutive task failures, but not platform/tool limits):
   - The workflow should:
     - Mark the relevant tasks as failed.
     - Optionally stop the run after too many consecutive failures.
     - Clearly report which tasks were not attempted and why in the final summary.

This guarantees that:

- Only KiloCode-aware usage (`--kilocode`) can trigger Orchestrator behavior.
- The user is never misled about whether Orchestrator is actually in use.
- If Orchestrator cannot be activated due to external limits, the run can still make progress via Standard Mode, and the fallback is clearly reported to the user.
---
