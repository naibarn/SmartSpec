---
description: Auto-implement tasks from tasks.md or implement-prompt.md with safety constraints, progress tracking, checkpoint/resume functionality, and validation.
---

## User Input
```text
$ARGUMENTS
```

**Patterns:**
- `specs/feature/spec-004/tasks.md`
- `specs/feature/spec-004/implement-prompt-spec-004.md`
- `specs/feature/spec-004`
- `specs/feature/spec-004/tasks.md --phase 1`
- `specs/feature/spec-004/tasks.md --phase 1-3`
- `specs/feature/spec-004/tasks.md --tasks T001-T010`
- `specs/feature/spec-004/tasks.md --start-from T033`
- `specs/feature/spec-004/tasks.md --resume`
- `specs/feature/spec-004/tasks.md --skip-completed`
- `specs/feature/spec-004/tasks.md --force-all`
- `specs/feature/spec-004/tasks.md --validate-only`
- `specs/feature/spec-004/tasks.md --phase 1-2 --skip-completed`
- `specs/feature/spec-004/tasks.md --start-from T033 --kilocode`
- `specs/feature/spec-004/tasks.md --tasks T033 --kilocode`

**Default Behavior:**
- Mode: `--skip-completed` (skip checked tasks)
- Phase: all phases (if not specified)
- Tasks: all tasks (if not specified)
- Resume: false (start from beginning)
- Validate-only: false (implement + validate)
- Kilocode: false (direct implementation)

## 0. Parse Arguments & Detect Input

**Parse arguments:**
- Extract path from first argument
- Parse `--phase` parameter (single, comma-separated, or range)
- Parse `--tasks` parameter (single, comma-separated, or range)
- Parse `--start-from` parameter (start from specified task to end)
- Parse `--resume` flag (continue from last checkpoint)
- Parse `--skip-completed` flag (default, skip checked tasks)
- Parse `--force-all` flag (ignore checkboxes, re-implement all)
- Parse `--validate-only` flag (validate only, no implementation)
- Parse `--kilocode` flag (use Kilo Code sub-task mode)

**Detect input type:**
- If path is directory: Look for `tasks.md` in directory
- If path ends with `tasks.md`: Use as tasks file
- If path ends with `implement-prompt-*.md`: Use as implement prompt
- If not found: Error and stop

**Set working directory:**
- WORK_DIR = directory containing the input file
- TASKS_FILE = path to tasks.md
- PROMPT_FILE = path to implement-prompt.md (if exists)

## 1. Load Context

**Read `.smartspec/` files:**
- Auto-detect `.smartspec/SPEC_INDEX.json` in project root
- If found: Parse and load into SPEC_REGISTRY
- If not found: Continue without dependency resolution

**Determine source:**
- If implement-prompt.md provided: Use as primary source
- Else: Use tasks.md as source

**Parse YAML frontmatter from tasks.md:**
```yaml
---
spec_id: spec-004-financial-system
version: 1.0.0
technology_stack: TypeScript, Node.js, PostgreSQL
validation_commands:
  compile: "tsc --noEmit"
  test: "npm test -- {test_file}"
  lint: "npm run lint"
  integration: "npm run test:integration"
---
```

**If frontmatter missing:**
- Use default TypeScript validation commands
- Log warning: "No validation_commands in frontmatter, using TypeScript defaults"

**Extract validation commands:**
- COMPILE_CMD = validation_commands.compile
- TEST_CMD = validation_commands.test
- LINT_CMD = validation_commands.lint
- INTEGRATION_CMD = validation_commands.integration (optional)

## 2. Parse Tasks & Status

**Parse tasks.md structure:**
- Project metadata
- Phase overview table
- All phases with tasks
- Checkpoints
- Supporting files references

**Extract task list:**
- For each task: Extract ID, title, hours, checkbox status, description, files, dependencies

**Task structure:**
```typescript
interface Task {
  id: string;              // "T001"
  title: string;           // "Setup project structure"
  hours: number;           // 4
  completed: boolean;      // true if checkbox is [x], false if [ ]
  phase: number;           // 1
  description: string;     // Full task description
  files: File[];           // List of files to create/edit
  dependencies: string[];  // ["T000", "spec-003"]
  supporting_files: string[]; // ["openapi.yaml", "data-model.md"]
}
```

**Parse checkbox status:**
- `- [x]` or `- [X]` → completed = true
- `- [ ]` → completed = false

**Build task registry:**
- TASKS = array of all tasks
- COMPLETED_TASKS = array of completed task IDs
- PENDING_TASKS = array of pending task IDs

## 3. Load Checkpoint (If Resume)

**If `--resume` flag:**
- Look for checkpoint file: `WORK_DIR/.smartspec-checkpoint.json`
- If found: Load checkpoint data
- Extract: last_completed_task, failed_tasks, skipped_tasks, timestamp

**Checkpoint structure:**
```json
{
  "timestamp": "2025-01-04T14:30:22Z",
  "spec_id": "spec-004-financial-system",
  "last_completed_task": "T015",
  "completed_tasks": ["T001", "T002", ..., "T015"],
  "failed_tasks": ["T010"],
  "skipped_tasks": ["T008"],
  "validation_status": {
    "compile": "PASS",
    "test": "PASS",
    "lint": "PASS"
  },
  "files_modified": ["src/index.ts", "src/models/User.ts"],
  "next_task": "T016"
}
```

**If checkpoint found:**
- Resume from next_task
- Skip all tasks before next_task
- Log: "Resuming from checkpoint: T016"

**If checkpoint not found:**
- Start from beginning
- Log: "No checkpoint found, starting from T001"

## 4. Filter Scope

**Apply mode filter:**
- If `--skip-completed`: Filter out tasks where completed = true
- If `--force-all`: Include all tasks regardless of checkbox status
- Default: `--skip-completed`

**Apply phase filter:**
- If `--phase 1`: Include only Phase 1 tasks
- If `--phase 1,2,3`: Include Phases 1, 2, 3 tasks
- If `--phase 1-3`: Include Phases 1 through 3 tasks
- If no `--phase`: Include all phases

**Apply task filter:**
- If `--tasks T001`: Include only T001
- If `--tasks T001,T002,T003`: Include T001, T002, T003
- If `--tasks T001-T010`: Include T001 through T010
- If no `--tasks`: Include all tasks (within selected phases)

**Apply start-from filter:**
- If `--start-from T033`: Include T033 and all tasks after T033 until end of file
- Example: `--start-from T033` with tasks T001-T050 → Include T033-T050
- Can combine with `--phase`: `--start-from T033 --phase 4` → Start from T033 within Phase 4 only
- **Note:** `--start-from` takes precedence over `--tasks` parameter

**Apply resume filter:**
- If `--resume` and checkpoint exists: Start from checkpoint.next_task

**Validate ranges:**
- Check phase numbers exist
- Check task IDs exist
- If invalid: Stop and report error

**Result:**
- FILTERED_TASKS = array of tasks to implement
- TOTAL_HOURS = sum of hours for filtered tasks

**Report scope:**
```
📊 Implementation Scope:
- Total tasks in file: 45
- Completed tasks: 15
- Pending tasks: 30
- Filtered tasks: 18 (T033-T050)
- Estimated effort: 72 hours
- Mode: Skip completed
- Start from: T033 (continue to end)
```

## 5. Validate Environment

**Check project setup:**
- Verify WORK_DIR exists
- Verify package.json exists (for Node.js projects)
- Verify required dependencies installed

**Check validation commands:**
- Test if COMPILE_CMD is available
- Test if TEST_CMD is available
- Test if LINT_CMD is available

**If validation commands fail:**
- Log warning: "Validation command not available: {command}"
- Continue with available commands only

**Check supporting files:**
- Verify referenced supporting files exist
- Log warnings for missing files

**Pre-flight validation:**
```bash
# Run initial validation to ensure project is in good state
{COMPILE_CMD}
{TEST_CMD}
{LINT_CMD}
```

**If pre-flight fails:**
- Stop and report errors
- Request user to fix before continuing
- Do NOT proceed with implementation

## 6. Execute Tasks (Main Loop)

**For each task in FILTERED_TASKS:**

### 6.1 Check Dependencies

**For each dependency:**
- If dependency is task ID: Check if completed
- If dependency is spec ID: Check if spec exists/implemented
- If dependency not satisfied: **SKIP task**
  - Log: "Skipped {task_id}: depends on incomplete {dependency}"
  - Add to skipped_tasks list
  - Continue to next task

### 6.2 Read Task Details

**Load full task information:**
- Description
- Files to create/edit
- File size categories (SMALL/MEDIUM/LARGE)
- Supporting files references
- Expected outcome

**Read supporting files:**
- If task references openapi.yaml: Read relevant sections
- If task references data-model.md: Read relevant sections
- If task references other files: Read as needed

### 6.3 Implement Task (If Not Validate-Only)

**If `--validate-only` flag: SKIP implementation, go to validation**

**If `--kilocode` flag: Use Kilo Code Sub-Task Mode**

**Kilo Code Sub-Task Mode (when `--kilocode` flag is set):**

1. **Check task estimated hours:**
   - Read estimated hours from task definition
   - Example: `T005: Set Up BullMQ 5.x (2h)` → hours = 2

2. **If task is COMPLEX (estimated hours >= 2):**
   - **Delegate to Kilo Code's automatic sub-task breakdown:**
     ```
     Create a new sub-task in code mode:
     T005 Goal: Set Up BullMQ 5.x for Background Job Processing
     ```
   
   - **How it works:**
     - Kilo Code will automatically detect task complexity
     - Kilo Code will break down the task into smaller sub-tasks
     - Each sub-task will be <50 lines to avoid `line_count` errors
     - Sub-tasks execute sequentially
   
   - **Example for T005 (Set Up BullMQ - 2h):**
     ```
     Task definition:
     - [ ] T005: Set Up BullMQ 5.x for Background Job Processing (2h)
     
     SmartSpec detects: 2h >= 2 → COMPLEX
     
     SmartSpec sends to Kilo Code:
     Create a new sub-task in code mode:
     T005 Goal: Set Up BullMQ 5.x for Background Job Processing
     
     Kilo Code will automatically break this into:
     - Sub-task 1: Install BullMQ dependencies
     - Sub-task 2: Create queue configuration
     - Sub-task 3: Implement job processor
     - Sub-task 4: Add error handling and logging
     ```
   
   - **Important:**
     - DO NOT manually specify sub-tasks
     - Let Kilo Code detect and break down automatically
     - Just prefix with "Create a new sub-task in code mode:"

3. **If task is SIMPLE (estimated hours < 2):**
   - Implement directly without sub-task mode
   - Use standard file size strategy (below)
   
   - **Example for T001 (Add field - 0.5h):**
     ```
     Task definition:
     - [ ] T001: Add user ID field to User model (0.5h)
     
     SmartSpec detects: 0.5h < 2 → SIMPLE
     
     SmartSpec sends to Kilo Code:
     T001 Goal: Add user ID field to User model
     
     Direct implementation (no sub-task mode)
     ```

**Standard Implementation Mode (when `--kilocode` flag is NOT set):**

**Apply file size strategy:**

**For SMALL files (<200 lines):**
- CREATE: Generate full file content
- EDIT: Can use full rewrite or str_replace

**For MEDIUM files (200-500 lines):**
- CREATE: Staged creation (outline first, then fill)
- EDIT: **str_replace ONLY**, max 50 lines per operation

**For LARGE files (>500 lines):**
- CREATE: Incremental build (section by section)
- EDIT: **Surgical str_replace ONLY**, max 50 lines per operation

**Implementation process:**
1. Read task description carefully
2. Review supporting files
3. For each file in task:
   - If CREATE: Generate file with appropriate strategy
   - If EDIT: Apply changes with appropriate strategy
4. Verify changes applied correctly

**Error handling during implementation:**
- If str_replace fails: Retry with expanded context (max 2 attempts)
- If still fails: STOP and report error
- Do NOT continue to next task

### 6.4 Validate Task

**Run validation commands:**
```bash
# Compilation check
{COMPILE_CMD}

# Run relevant tests
{TEST_CMD}

# Linting
{LINT_CMD}
```

**Check validation results:**
- If ALL pass: Task successful
- If ANY fail: Task failed

**If validation fails:**

**Attempt 1: Analyze and fix**
1. Read error messages
2. Identify root cause
3. Apply fix
4. Re-validate

**Attempt 2: Different approach**
1. Try alternative fix
2. Re-validate

**Attempt 3: STOP**
- Do NOT continue
- Report error details
- Add to failed_tasks list
- Request manual guidance

**If 3 consecutive tasks fail:**
- STOP execution immediately
- Create checkpoint
- Report: "Stopped due to 3 consecutive failures"
- Request manual review

### 6.5 Update Progress

**If task successful:**
- Update checkbox in tasks.md: `- [ ]` → `- [x]`
- Add to completed_tasks list
- Log: "✅ Completed {task_id}: {title}"

**If task failed:**
- Keep checkbox unchecked
- Add to failed_tasks list
- Log: "❌ Failed {task_id}: {title} - {error}"

**If task skipped:**
- Keep checkbox unchecked
- Add to skipped_tasks list
- Log: "⏭️ Skipped {task_id}: {title} - {reason}"

### 6.6 Create Mini-Checkpoint

**Every 5 tasks:**
- Create checkpoint file
- Save progress
- Run comprehensive validation
- Report progress

**Checkpoint creation:**
```json
{
  "timestamp": "2025-01-04T15:45:30Z",
  "spec_id": "spec-004-financial-system",
  "last_completed_task": "T020",
  "completed_tasks": ["T016", "T017", "T018", "T019", "T020"],
  "failed_tasks": [],
  "skipped_tasks": ["T018"],
  "validation_status": {
    "compile": "PASS",
    "test": "PASS",
    "lint": "PASS"
  },
  "files_modified": ["src/api/balance.ts", "src/models/Transaction.ts"],
  "next_task": "T021"
}
```

### 6.7 Monitor Context

**Check token usage:**
- If approaching 80%: Create checkpoint and pause
- Report: "Context limit approaching, checkpoint created"
- Instructions: "Resume with --resume flag"

**On context overflow:**
- Immediate checkpoint
- Save state
- Report current position

### 6.8 Safety Constraints

**Enforce hard limits:**
- ❌ Maximum 10 tasks per execution cycle
- ❌ Maximum 5 file edits per task
- ❌ Maximum 50 lines per str_replace
- ❌ Maximum 2 retry attempts per operation
- ❌ STOP at 3 consecutive errors

**If limit reached:**
- Create checkpoint
- Report progress
- Pause execution

## 7. Phase Checkpoint

**At end of each phase:**

**Run comprehensive validation:**
```bash
# Full compilation
{COMPILE_CMD}

# All tests
{TEST_CMD}

# Linting
{LINT_CMD}

# Integration tests (if defined)
{INTEGRATION_CMD}
```

**Validation checklist:**
- [ ] Compilation passes
- [ ] All tests passing
- [ ] No critical lint errors
- [ ] Integration verified

**If ALL pass:**
- Create phase checkpoint
- Report: "✅ Phase {X} complete"
- Continue to next phase

**If ANY fail:**
- STOP execution
- Report failures
- Request manual fix
- Do NOT continue to next phase

## 8. Final Report

**Generate comprehensive report:**

```markdown
# Implementation Report: {spec_id}

**Generated:** {timestamp}
**Duration:** {duration}
**Status:** {COMPLETE / PARTIAL / FAILED}

---

## Summary

**Total Tasks:** {total}
**Completed:** {completed} ✅
**Failed:** {failed} ❌
**Skipped:** {skipped} ⏭️
**Success Rate:** {completed/total * 100}%

**Estimated Effort:** {total_hours}h
**Actual Duration:** {actual_duration}

---

## Completed Tasks

{For each completed task:}
- ✅ **{task_id}**: {title} ({hours}h)

---

## Failed Tasks

{For each failed task:}
- ❌ **{task_id}**: {title} ({hours}h)
  - **Error:** {error_message}
  - **Attempts:** {attempts}
  - **Action Required:** {action}

---

## Skipped Tasks

{For each skipped task:}
- ⏭️ **{task_id}**: {title} ({hours}h)
  - **Reason:** {reason}
  - **Dependency:** {dependency}
  - **Action Required:** Complete {dependency} first

---

## Validation Status

**Final Validation:**
- Compilation: {PASS/FAIL}
- Tests: {PASS/FAIL} ({coverage}% coverage)
- Linting: {PASS/FAIL}
- Integration: {PASS/FAIL}

**Issues Found:** {count}
{List of issues if any}

---

## Files Modified

**Total Files:** {count}

{For each file:}
- `{file_path}` ({lines_added}+ / {lines_removed}-)

---

## Checkpoints Created

**Total Checkpoints:** {count}

{For each checkpoint:}
- **{timestamp}**: After {task_id} ({completed_count} tasks completed)

---

## Next Steps

{If status == COMPLETE:}
✅ **All tasks completed successfully!**

Next actions:
1. Review implementation
2. Run final integration tests
3. Update documentation
4. Prepare for deployment

{If status == PARTIAL:}
⚠️ **Partial completion**

Next actions:
1. Review failed tasks: {failed_task_ids}
2. Fix issues manually
3. Resume with: `/smartspec_implement_tasks.md {path} --resume`

{If status == FAILED:}
❌ **Implementation failed**

Next actions:
1. Review error logs
2. Fix critical issues
3. Restart with: `/smartspec_implement_tasks.md {path}`

---

## Resume Command

{If incomplete:}
```bash
/smartspec_implement_tasks.md {path} --resume
```

{If need to re-implement specific tasks:}
```bash
/smartspec_implement_tasks.md {path} --tasks {failed_task_ids} --force-all
```

---

**Report saved to:** {WORK_DIR}/implementation-report-{timestamp}.md
**Checkpoint saved to:** {WORK_DIR}/.smartspec-checkpoint.json
**Updated tasks file:** {TASKS_FILE}
```

## 9. Save Artifacts

**Save implementation report:**
- Path: `{WORK_DIR}/implementation-report-{timestamp}.md`
- Content: Full report as above

**Save final checkpoint:**
- Path: `{WORK_DIR}/.smartspec-checkpoint.json`
- Content: Final checkpoint data

**Update tasks.md:**
- Update all checkboxes for completed tasks
- Preserve all other content

**Commit changes (optional):**
```bash
git add .
git commit -m "Implement tasks {task_range}: {summary}"
```

## 10. Report to User (Thai)

```
✅ การ Implement Tasks เสร็จสิ้น

📊 สรุปผลการทำงาน:
- Tasks ทั้งหมด: {total}
- สำเร็จ: {completed} ✅
- ล้มเหลว: {failed} ❌
- ข้าม: {skipped} ⏭️
- อัตราความสำเร็จ: {success_rate}%

⏱️ เวลาที่ใช้: {duration}
📁 ไฟล์ที่แก้ไข: {files_count} files

✅ Validation Status:
- Compilation: {compile_status}
- Tests: {test_status}
- Linting: {lint_status}

📄 รายงานฉบับเต็ม: {report_path}
💾 Checkpoint: {checkpoint_path}
📋 Tasks อัปเดต: {tasks_path}

{If incomplete:}
🔄 ต่อไป:
1. ตรวจสอบ tasks ที่ล้มเหลว: {failed_tasks}
2. แก้ไขปัญหาด้วยตนเอง
3. Resume ด้วย: `/smartspec_implement_tasks.md {path} --resume`

{If complete:}
🎉 ทุก tasks เสร็จสมบูรณ์!

ขั้นตอนต่อไป:
1. Review implementation
2. Run integration tests
3. Update documentation
4. Deploy

---

💡 Tips:
- ใช้ `--validate-only` เพื่อตรวจสอบโดยไม่ implement
- ใช้ `--phase X` เพื่อ implement เฉพาะ phase
- ใช้ `--tasks T001-T010` เพื่อ implement เฉพาะ tasks
- ใช้ `--resume` เพื่อ continue จาก checkpoint
```

---

Context: $ARGUMENTS
