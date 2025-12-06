---
description: Verify implementation progress by checking tasks.md against actual files, running validation, and reporting incomplete/error tasks without modifying code. Optionally update checkboxes for tasks that are fully verified as complete.
---

## User Input

```text
$ARGUMENTS
```

Typical usage:

```bash
/smartspec_verify_tasks_progress specs/feature/spec-004-financial-system/tasks.md
/smartspec_verify_tasks_progress specs/feature/spec-004-financial-system/tasks.md --tasks T001-T020
```

> This workflow is **verification-only**. It must **never attempt to fix code** or auto-implement missing work. There are separate workflows (e.g. `/smartspec_implement_tasks`, `/smartspec_fix_errors`) responsible for making code changes.

---

## 0. Load Context

Load only the SmartSpec context required to verify implementation progress for a single SPEC.

1. From project root:
   - `SPEC_INDEX.json` (preferred, if present at the repository root)
   - If not found, optionally try `.smartspec/SPEC_INDEX.json`
     - If the fallback file is also missing, log a warning but **do not fail** the workflow. Continue without SPEC index data.

2. From the target SPEC:
   - The `tasks.md` file from `$ARGUMENTS`
   - Any spec metadata files referenced by `tasks.md` (e.g. `spec.md`, `architecture.md`, `openapi.yaml`, `data-model.md`)

3. Explicitly **do NOT** load or call any KiloCode/Orchestrator prompt templates:
   - Do not read `.smartspec/KILO-PROMPT*`
   - Do not read `.smartspec/KILO-ASK*`
   - Do not read `.smartspec/KILO-ARCHITECT*`
   - Do not read `.smartspec/KILO-CODE*`
   - Do not read `.smartspec/KILO-DEBUG*`
   - Do not read `.smartspec/KILO-TEST*`

> This workflow is verification-only. It must not invoke Orchestrator Mode or use any `--kilocode`-only tools.  
> It **reads** the current implementation state and **reports** it. It does not generate code or fix errors.

---

## 1. Resolve Path and Parse Arguments

### 1.1 Resolve TASKS_PATH

1. If `$ARGUMENTS` contains a path ending with `tasks.md`, use it as `TASKS_PATH`.
2. Otherwise, if the currently active file is a `tasks.md`, use that.
3. Normalize to a project-relative path, for example:

```text
specs/feature/spec-004-financial-system/tasks.md
```

If `TASKS_PATH` cannot be resolved → stop with a clear error:

```text
❌ Could not resolve tasks.md path from arguments. Expected: specs/.../tasks.md
```

### 1.2 Supported CLI Flags

Parse the following flags:

- `--tasks <RANGE>` (optional)
  - Limit verification to a subset of tasks.
  - Supports:
    - Single ID: `T005`
    - Comma-separated list: `T001,T003,T010`
    - Ranges: `T001-T010`
    - Mixed: `T001-T005,T010,T020-T022`

- `--task <RANGE>` (alias for `--tasks`)

- `--start-from <TASK_ID>` (optional)
  - Verify tasks starting from this ID (inclusive), based on order in `tasks.md`.

- `--phase <PHASE_NAME_OR_ID>` (optional)
  - Only verify tasks in the specified phase (if phases are defined in `tasks.md`).

- `--output <PATH>` (optional)
  - Custom output path for the progress report.
  - Default: same directory as `tasks.md` with name `progress-report-YYYYMMDD.md`.

- `--no-update` (optional)
  - Do not modify `tasks.md` at all. Only generate the report.

- `--strict` (optional)
  - Use stricter rules to determine completion (e.g., require all validation commands and all acceptance criteria to pass).

> This workflow does **not** support `--kilocode`. If such a flag is present, it must be ignored or produce a clear warning.

Store parsed options:

```python
options = {
  "task_selector_raw": "...",   # from --tasks/--task
  "start_from": "T010" or None,
  "phase": "Phase 2" or None,
  "output": "custom-path.md" or None,
  "no_update": bool,
  "strict": bool,
}
```

### 1.3 Parse Task Selector

If `task_selector_raw` is provided:

1. Split by comma.
2. For each token:
   - If it matches `T\d+` → single task ID.
   - If it matches `T\d+-T\d+` → expand numeric range (e.g. `T001-T003` → `T001,T002,T003`).
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
- `dependencies` (task IDs or spec IDs)
- `files` (list of file operations)
  - `operation`: `CREATE` | `EDIT`
  - `path`: file path (e.g. `src/services/promo-code.service.ts`)
- `acceptance_criteria` (list of textual criteria)
- `validation_commands` (e.g. `npm test`, `npm run lint`, `npm run test promo`)
- `checkbox_state`:
  - `"checked"`   if the task line starts with `- [x] T001:`
  - `"unchecked"` if the task line starts with `- [ ] T001:`

Example task header pattern:

```text
- [ ] T001: Initialize Promo System
- [x] T002: Setup Promo Database
```

Regex (conceptual):

```text
^- \[( |x)\] (T[0-9]{3}): (.*)$
```

Return structure:

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
    "checkbox_state": "unchecked",  # or "checked"
  },
  ...
]
```

---

## 3. Filter Scope

Determine which tasks to verify in this run.

### 3.1 Apply Task Selector

If `selected_task_ids` is not empty:

- Keep only tasks where `task.id` is in `selected_task_ids`.
- Preserve original order from `tasks.md`.

### 3.2 Apply `--start-from`

If `options["start_from"]` is set:

- Find the first index `i` where `tasks[i].id == start_from`.
- Keep tasks from `i` onward.

### 3.3 Apply `--phase`

If `options["phase"]` is set:

- Keep only tasks whose `phase` matches the given phase name or ID (case-insensitive comparison or pattern matching).

The final ordered list is `FILTERED_TASKS`.

If `FILTERED_TASKS` is empty → report and stop:

```text
No tasks to verify for the given filters.
```

---

## 4. Verify Each Task (Read-Only for Code)

For each task in `FILTERED_TASKS`, verify its completion based on:

- File existence and modification state
- Validation command results
- Acceptance criteria

Create per-task fields:

```python
task.file_status = {}          # path -> {expected, exists, modified}
task.validation_results = {}   # command -> {exit_code, stdout, stderr}
task.criteria_flags = []       # list of booleans
task.completion_percentage = 0
task.is_complete = False
task.status = "⬜ NOT STARTED"
task.error_summary = None      # short text summarizing why it is not complete (if applicable)
```

> **Important:** This workflow must not modify any source files. It only reads them and runs validation commands.

### 4.1 Check Files Existence and Modification

For each file in `task.files`:

```python
for f in task.files:
    exists = check_file_exists(f.path)

    if f.operation == "CREATE":
        task.file_status[f.path] = {
            "expected": "created",
            "exists": exists,
        }

    elif f.operation == "EDIT":
        modified = check_file_modified_since(f.path, task_created_date)
        task.file_status[f.path] = {
            "expected": "edited",
            "exists": exists,
            "modified": modified,
        }
```

Rules:

- For `CREATE`: file must exist to count as satisfied.
- For `EDIT`: file must exist **and** have been modified since the task was created (to avoid counting pre-existing files from other specs).

### 4.2 Run Validation Commands

For each `command` in `task.validation_commands`:

```python
for command in task.validation_commands:
    result = run_command(command)  # returns {exit_code, stdout, stderr}
    task.validation_results[command] = result
```

- Commands are run in the project root (or appropriate working directory).
- **No attempt is made to fix any errors**. Failures are recorded and reported.

### 4.3 Evaluate Acceptance Criteria

Each acceptance criterion is evaluated using:

- `task.file_status`
- `task.validation_results`

Conceptual:

```python
criteria_flags = []

for criterion in task.acceptance_criteria:
    met = check_criterion(
        criterion,
        file_status=task.file_status,
        validation_results=task.validation_results,
    )
    criteria_flags.append(met)

task.criteria_flags = criteria_flags
```

Compute completion percentage:

```python
if criteria_flags:
    task.completion_percentage = (
        sum(1 for x in criteria_flags if x) / len(criteria_flags) * 100
    )
else:
    # If there are no explicit criteria, infer completion from files + validation
    task.completion_percentage = infer_completion_from_files_and_validation(task)
```

### 4.4 Determine Task Status and Error Summary

Derive high-level status:

```python
any_files_exist = any(
    status.get("exists") for status in task.file_status.values()
)

all_files_ok = all(
    status.get("exists") and (status.get("modified", True))
    for status in task.file_status.values()
)

all_validation_passed = all(
    r["exit_code"] == 0 for r in task.validation_results.values()
)

all_criteria_met = (task.completion_percentage == 100)
```

Completion rules:

- In **strict mode** (`options["strict"] == True`):
  - `is_complete = all_files_ok and all_validation_passed and all_criteria_met`
- In default mode:
  - `is_complete = all_files_ok and all_criteria_met`
  - Validation failures may mark the task as incomplete (recommended).

Set status:

```python
if task.is_complete:
    task.status = "✅ COMPLETE"
    task.error_summary = None
elif any_files_exist or task.validation_results:
    task.status = f"🟦 IN PROGRESS ({task.completion_percentage}%)"
    task.error_summary = build_error_summary(task)
else:
    task.status = "⬜ NOT STARTED"
    task.error_summary = "No related files or validation activity detected."
```

`build_error_summary(task)` should produce a short one-line explanation, for example:

- `"Missing file: src/services/promo-code.service.ts"`
- `"TypeScript compile error: 3 errors in src/middleware/auth.ts"`
- `"Tests failing: 2 Jest test suites red"`

> These error summaries will be shown clearly in the final report.  
> **The verify workflow never tries to fix them.** It only describes what is wrong.

---

## 5. Generate Progress Report (Read-Only Summary)

Generate a Markdown progress report summarizing:

- Overall status
- Phase-by-phase status
- Per-task details
- Blockers and recommendations
- Explicit list of tasks that are incomplete or have errors

### 5.1 Determine Output Path

If `options["output"]` is set:

- Use that path.

Otherwise:

- Use the same directory as `tasks.md`:
  - `progress-report-YYYYMMDD.md`

### 5.2 Overall Summary Section

```markdown
# Implementation Progress Report

**Generated:** YYYY-MM-DD HH:mm  
**Source:** [tasks.md path]

---

## Executive Summary

**Overall Progress:** {completed_tasks}/{total_tasks} tasks complete ({overall_percentage}%)

**Status Breakdown:**
- ✅ Complete: {complete_count} tasks ({complete_pct}%)
- 🟦 In Progress: {in_progress_count} tasks ({in_progress_pct}%)
- ⬜ Not Started: {not_started_count} tasks ({not_started_pct}%)

> This report is verification-only. No code was modified during this process.
```

### 5.3 Detailed Task Status Section

```markdown
## Detailed Status

### Phase 1: [Name]

#### {task.status} {task.id}: {task.title}

**Completion:** {task.completion_percentage}%  

**Files:**
- ✅ `path/file1.ts` - Created
- ✅ `path/file2.ts` - Edited (modified)
- ❌ `path/file3.ts` - Missing

**Validation:**
- ✅ `npm run build` - PASS
- ⚠️ `npm test` - FAIL (3 failing tests)
- ✅ `npm run lint` - PASS

**Acceptance:**
- ✅ Criterion 1
- ✅ Criterion 2
- ❌ Criterion 3 (missing negative test cases)

**Summary:**  
- If `task.is_complete`: `Task is fully implemented and passes all checks under current rules.`  
- If not: include `task.error_summary`, e.g.  
  `Task is incomplete: TypeScript compile errors remain in src/middleware/auth.ts and tests are failing.`
```

### 5.4 Explicit Incomplete/Error Tasks Section

This section is critical for your request: it clearly lists tasks that are **not complete or have errors**, without attempting to fix anything.

```markdown
## 🚧 Incomplete or Error Tasks (Verification Only)

The following tasks are **not** fully complete or have validation errors.  
No code has been changed; this section is for visibility and planning.

### In Progress / Incomplete
- {task.id}: {task.title} – {task.completion_percentage}%  
  - Reason: {task.error_summary}

### Not Started
- {task.id}: {task.title}  
  - Reason: No implementation detected for this task.

### Marked Complete but Failed Verification
- {task.id}: {task.title}  
  - tasks.md: `[x]` (marked complete)  
  - Verification result: **FAILED**  
  - Reason: {task.error_summary}
```

> This section is **pure reporting**. It does not change any files.  
> To actually fix these tasks, the user should run the appropriate implementation/fix workflows.

### 5.5 Blockers & Recommendations Section

```markdown
## ⚠️ Blockers & Recommendations

### Critical Blockers (Must be addressed before further implementation)
1. T0XX: Missing file `src/.../file.ts`
   - Impact: Blocks dependent tasks (T0YY, T0ZZ)
   - Suggested workflow: `/smartspec_implement_tasks ... --tasks T0XX`

2. T0AA: TypeScript compile errors in `src/...`
   - Impact: Prevents successful build and testing
   - Suggested workflow: `/smartspec_fix_errors specs/...`

### Suggested Next Steps

- To implement missing features:
  - `/smartspec_implement_tasks specs/.../tasks.md --tasks T0NN-T0MM`
- To fix compilation/test errors:
  - `/smartspec_fix_errors specs/...`
- To generate missing tests:
  - `/smartspec_generate_tests specs/... --target-coverage 80`

> Again, **this verify workflow does not perform these fixes**.  
> It only points out what needs attention and suggests which workflows to use.
```

---

## 6. Optional: Auto-Update tasks.md (Checkboxes Only)

> This is the only part of the workflow that writes to a file, and it **only** touches `tasks.md` checkboxes.  
> No source code or config files are modified by this workflow.

### 6.1 Rules

If `options["no_update"]` is **true**:

- Skip this section entirely (do not modify `tasks.md`).

Otherwise:

For each verified task `task`:

- If `task.is_complete == True` **and** `task.checkbox_state == "unchecked"`:
  - Update the corresponding task header line in `tasks.md`:
    - From:
      ```text
      - [ ] T001:
      ```
    - To:
      ```text
      - [x] T001:
      ```

- If `task.is_complete == False` **and** `task.checkbox_state == "checked"`:
  - **Do not automatically uncheck.**
  - Record a warning in the report:

    ```markdown
    ⚠️ T001 is marked complete in tasks.md but verification failed. Please review manually.
    ```

Implementation sketch:

```python
if not options["no_update"]:
    with open(TASKS_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    for task in tasks:
        if task.is_complete and task.checkbox_state == "unchecked":
            pattern = f"- [ ] {task.id}:"
            replacement = f"- [x] {task.id}:"
            content = content.replace(pattern, replacement)

    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        f.write(content)
```

---

## 7. Final Output

### 7.1 Console Summary

At the end of the workflow, print a concise summary, for example:

```text
📊 Verification completed (no code changes were made).

📁 Progress Report: specs/feature/spec-005-promo-system/progress-report-20251206.md
📄 Tasks File:       specs/feature/spec-005-promo-system/tasks.md
   (checkboxes updated only for tasks fully verified as complete)

Summary:
- ✅ Complete:      12/30 tasks (40%)
- 🟦 In Progress:   8 tasks
- ⬜ Not Started:   10 tasks

Incomplete/Error Tasks:
- 5 tasks are incomplete or have validation errors.
  See the "Incomplete or Error Tasks" section in the report for details.

To fix issues and continue implementation, use:
- /smartspec_implement_tasks ...
- /smartspec_fix_errors ...
- /smartspec_generate_tests ...
```

### 7.2 No Orchestrator / KiloCode Behavior

This workflow must **never**:

- Switch into Orchestrator Mode.
- Call any KiloCode-specific tools or prompts.
- Use any `--kilocode`-specific behavior.
- Attempt to fix or generate code.

If there is a need to **fix** or **implement** missing work:

- The report should suggest running `/smartspec_implement_tasks`, `/smartspec_fix_errors`, or `/smartspec_generate_tests` as separate steps.
- This verification workflow remains read-only for all code and config files, and only writes:
  - The progress report.
  - Optionally, checkbox updates in `tasks.md` for tasks that have been fully verified as complete.

---

By following this workflow, `smartspec_verify_tasks_progress`:

- Gives a **clear, explicit summary** of all incomplete/error tasks.
- **Does not attempt to fix** those tasks—only reports them.
- Keeps `tasks.md` in sync (when allowed) by marking only truly complete tasks as `[x]`.
- Leaves actual fixing to other dedicated workflows (implement, fix_errors, generate_tests, etc.).
