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
- Parse `--architect` flag (use Architect Mode for system design before implementation)

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

**IMPORTANT: This is a LOOP - You MUST iterate through ALL tasks in FILTERED_TASKS**

**Loop structure:**
```
FOR each task in FILTERED_TASKS:
  1. Check dependencies
  2. Read task details
  3. Implement task
  4. Validate task
  5. Update progress
  6. Report completion
  7. Continue to NEXT task
  
DO NOT STOP until ALL tasks are completed or error occurs
```

**Progress tracking:**
- Track: current_task_index, total_tasks, completed_count, failed_count
- Report after each task: "Completed {current}/{total} tasks"
- At end: "All {total} tasks completed" or "Stopped at {current}/{total}"

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

**Referenced SPEC resolution (mandatory before asking assumptions):**
- If the task includes **supporting spec references** (by path or spec ID), the agent MUST open and read them before making any integration assumptions.
- Resolve spec references in this priority order:
  1. Explicit file paths listed in the task (e.g., `spec.md`, `architecture.md`, `openapi.yaml`).
  2. Spec IDs or names referenced by the task, resolved via:
     - `SPEC_INDEX.json` at repository root (preferred)
     - `.smartspec/SPEC_INDEX.json` (fallback)
- If a referenced spec cannot be resolved, log a warning and continue with best-effort verification from codebase.

**Anti-auto-guess rule for external integrations (e.g., Auth/JWT/OAuth/OIDC/MFA):**
- For tasks that mention any of: `auth`, `jwt`, `oauth`, `oidc`, `session`, `mfa`, `identity`, the agent MUST:
  1. Read the referenced auth-related spec(s) first.
  2. Search the existing codebase for evidence:
     - auth middleware/guards
     - API clients/gateway config
     - environment variables (`AUTH_*`, `JWT_*`, `OIDC_*`)
     - OpenAPI references for the auth service
  3. Use evidence found in specs/code to decide endpoints, token format/algorithm, and patterns.

- If **no reliable evidence** is found after steps (1)-(2):
  - The agent MAY ask the user to choose an assumption.
  - The agent MUST NOT auto-select a default option.
  - If a choice is unavoidable without evidence, prefer the safe choice:
    **"Let me examine the existing codebase to understand the current authentication patterns."**


### 6.3 Implement Task (If Not Validate-Only)

**If `--validate-only` flag: SKIP implementation, go to validation**

**If `--architect` flag: Use Architect Mode first**

**Architect Mode (when `--architect` flag is set):**

**For EVERY task, use Architect Mode first:**
```
Use Architect Mode to design the system architecture and create implementation plan. {task_id}: {task_title}
```

**Architect Mode will:**
- Design system architecture and structure
- Create technical specification
- Define file structure, modules, and responsibilities
- Define data flow and API endpoints
- Identify libraries and dependencies needed
- Create detailed implementation plan

**After Architect Mode completes:**
- Use the architecture and plan to implement the code
- Follow the structure defined by Architect Mode
- Reference the technical specification

**If `--kilocode` flag: Use Orchestrator Mode**

**Orchestrator Mode (when `--kilocode` flag is set):**

**For EVERY task, send to Orchestrator Mode:**
```
Use Orchestrator Mode to break this task into subtasks. {task_id}: {task_title}
```

**How it works:**
- Orchestrator Mode will analyze task complexity automatically
- If task is complex: Orchestrator may use **Architect Mode first** to design system architecture
- Then breaks into smaller sub-tasks (Architect → Code → Debug → Test)
- If task is simple: Orchestrator implements directly
- **You don't need to check estimated hours or complexity**
- Orchestrator is smart enough to decide

**Orchestrator may create sub-tasks like:**
1. **Ask Mode** - Analyze existing code and explore implementation options
2. **Architect Mode** - Design system architecture and create implementation plan
3. **Code Mode** - Implement the code based on architecture
4. **Debug Mode** - Fix any bugs or errors
5. **Test Mode** - Run tests and validate

**Typical workflows:**
- **Simple task:** Code → Test
- **Medium task:** Architect → Code → Debug → Test
- **Complex task:** Ask → Architect → Code → Debug → Test
- **Unclear task:** Ask → Architect → Code → Debug → Test

**Example 1: Complex Task with Analysis and Architecture Design**
```
Task definition:
- [ ] T005: Set Up BullMQ 5.x for Background Job Processing (2h)

SmartSpec sends to Kilo Code:
Use Orchestrator Mode to break this task into subtasks. T005: Set Up BullMQ 5.x for Background Job Processing

Orchestrator decides:
- This is complex and needs analysis → Use Ask Mode first, then Architect Mode:
  - Sub-task 1 (Ask Mode): Analyze current job processing approach and BullMQ integration options
  - Sub-task 2 (Architect Mode): Design BullMQ architecture and integration plan based on analysis
  - Sub-task 3 (Code Mode): Install BullMQ dependencies
  - Sub-task 4 (Code Mode): Create queue configuration based on architecture
  - Sub-task 5 (Code Mode): Implement job processor
  - Sub-task 6 (Code Mode): Add error handling and logging
  - Sub-task 7 (Debug Mode): Fix any issues
  - Sub-task 8 (Test Mode): Validate BullMQ integration
```

**Example 2: Simple Task**
```
Task definition:
- [ ] T001: Add user ID field to User model (0.5h)

SmartSpec sends to Kilo Code:
Use Orchestrator Mode to break this task into subtasks. T001: Add user ID field to User model

Orchestrator decides:
- This is simple → Implement directly (no sub-tasks needed)
```

**Important:**
- DO NOT check estimated hours yourself
- DO NOT decide complexity yourself
- Just send ALL tasks to Orchestrator Mode with the same command
- Let Orchestrator decide whether to break down or not

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

**Attempt 2: Switch to Debug Mode**
- Do NOT retry with same approach
- Switch mode: "Use Debug Mode to analyze and fix the issue."
- Debug Mode will:
  - Systematically diagnose the problem
  - Read error/stack trace
  - Check related files and dependencies
  - Apply targeted fix
  - Run validation again

**Attempt 3: Switch to Orchestrator Mode (if Debug fails)**
- If Debug Mode cannot fix the issue
- Switch mode: "Use Orchestrator Mode to resolve the issue."
- Orchestrator will try different strategy
- If Orchestrator also fails, then STOP:
  - Report error details
  - Add to failed_tasks list
  - Request manual guidance

**If same error repeats 2+ times:**
- Switch mode: "Use Orchestrator Mode to resolve the issue."
- Orchestrator can break the loop with different strategy

**If 3 consecutive tasks fail:**
- STOP execution immediately
- Create checkpoint
- Report: "Stopped due to 3 consecutive failures"
- Switch mode: "Use Orchestrator Mode to review and fix issues."
- Request manual review if Orchestrator cannot resolve

### 6.5 Update Progress

**If task successful:**

**STEP 1: Update checkbox in tasks.md (MANDATORY)**

**Action:** Use file editing tool to update the checkbox
```
Find in {TASKS_FILE}:
  - [ ] {task_id}: {task_title}

Replace with:
  - [x] {task_id}: {task_title}
```

**Example:**
```
Find:    - [ ] T037: Implement Credit Deduction APIs (2h)
Replace: - [x] T037: Implement Credit Deduction APIs (2h)
```

**IMPORTANT:** 
- You MUST update the checkbox in the actual tasks.md file
- Use str_replace or edit_file tool
- Do NOT skip this step
- Do NOT just log completion without updating file

**STEP 2: Update tracking variables**
- Add to completed_tasks list
- Increment completed_count
- Log: "✅ Completed {task_id}: {title}"

**STEP 3: Verify update**
- Read the line from tasks.md to confirm it shows `[x]`
- If still shows `[ ]`, retry update
- If retry fails, log warning but continue

**If task failed:**

**STEP 1: Keep checkbox unchecked (DO NOT update)**
- The checkbox should remain as `- [ ]` in tasks.md
- Do NOT change it to `[x]`

**STEP 2: Update tracking variables**
- Add to failed_tasks list
- Increment failed_count
- Log: "❌ Failed {task_id}: {title} - {error}"

**If task skipped:**

**STEP 1: Keep checkbox unchecked (DO NOT update)**
- The checkbox should remain as `- [ ]` in tasks.md
- Do NOT change it to `[x]`

**STEP 2: Update tracking variables**
- Add to skipped_tasks list
- Increment skipped_count
- Log: "⏭️ Skipped {task_id}: {title} - {reason}"

**Report progress after EACH task:**
```
📊 Progress: {current_task_index}/{total_tasks} tasks processed
   ✅ Completed: {completed_count}
   ❌ Failed: {failed_count}
   ⏭️ Skipped: {skipped_count}
   ⏳ Remaining: {total_tasks - current_task_index}
```

**IMPORTANT: After reporting progress, CONTINUE to next task in loop**
**DO NOT STOP until all tasks are processed**

### 6.6 Create Mini-Checkpoint

**Every 5 tasks:**

**STEP 1: Verify checkboxes were updated**
- Read tasks.md
- Count `[x]` checkboxes for completed tasks
- If count doesn't match completed_count:
  - Log warning: "Checkbox mismatch detected"
  - List tasks that should be checked but aren't
  - Attempt to fix by updating missing checkboxes

**STEP 2: Create checkpoint file**
- Save progress to .smartspec-checkpoint.json
- Include completed_tasks list
- Include failed_tasks list
- Include skipped_tasks list

**STEP 3: Run comprehensive validation**
- Compile check
- Test check
- Lint check

**STEP 4: Report progress**
- Show checkpoint summary
- Show validation results

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
- ❌ Maximum 5 file edits per task
- ❌ Maximum 50 lines per str_replace
- ❌ Maximum 2 retry attempts per operation
- ❌ STOP at 3 consecutive errors

**Note:** There is NO limit on number of tasks per execution
**The loop MUST continue until ALL tasks in FILTERED_TASKS are processed**

**If limit reached:**

**For file edits/str_replace limit:**
- Report error
- Switch mode: "Use Debug Mode to analyze and fix the issue."
- Debug Mode will check why edits are failing
- If Debug cannot resolve, switch to Orchestrator Mode
- If Orchestrator cannot resolve, skip task

**For retry limit (2 attempts):**
- Do NOT retry 3rd time with same approach
- Switch mode: "Use Debug Mode to analyze and fix the issue."
- Debug Mode will diagnose why previous attempts failed
- If Debug cannot resolve, switch to Orchestrator Mode

**For consecutive errors (3 tasks):**
- Create checkpoint
- Switch mode: "Use Debug Mode to analyze and fix issues."
- Debug Mode will look for common patterns across failures
- If Debug cannot resolve, switch to Orchestrator Mode
- Report progress before stopping
- If Orchestrator cannot resolve, request manual review

**For infinite loop detection:**
- If same command executed 3+ times with same result
- Switch mode: "Use Debug Mode to analyze and fix the issue."
- Debug Mode will diagnose why command keeps failing
- If Debug cannot break loop, switch to Orchestrator Mode

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

**First failure:**
- Report failures with details
- Switch mode: "Use Debug Mode to analyze and fix the issue."
- Debug Mode will:
  - Analyze error messages and stack traces
  - Check related files and dependencies
  - Identify root cause
  - Apply targeted fixes
  - Re-run validation

**If validation fails again after Debug Mode:**
- Switch mode: "Use Orchestrator Mode to resolve the issue."
- Let Orchestrator try different strategy
- Re-run validation after Orchestrator fixes

**If validation fails again after Orchestrator:**
- STOP execution
- Create checkpoint
- Report failures
- Request manual fix
- Do NOT continue to next phase

**If validation command itself fails (not test failures):**
- Switch mode: "Use Debug Mode to analyze and fix the issue."
- Debug Mode will check environment, dependencies, configuration
- If Debug cannot fix, switch to Orchestrator Mode

## 8. Final Report

**COMPLETION CHECK:**
```
IF current_task_index == total_tasks:
  status = "COMPLETE - All tasks processed"
ELSE IF failed_count >= 3:
  status = "STOPPED - Too many failures"
ELSE:
  status = "PARTIAL - Stopped at task {current_task_index}/{total_tasks}"
```

**IMPORTANT: Only reach this section after processing ALL tasks in FILTERED_TASKS**
**If you reach here early, you have NOT completed the loop correctly**

**STEP 1: Generate comprehensive report and save to file**

**Action:** Write full report to file `{WORK_DIR}/implementation-report-{timestamp}.md`

**Full report template:**

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

**STEP 2: Return compact summary (NOT full report)**

**IMPORTANT: Do NOT return the full report above**
**Only return this compact summary to save context:**

```markdown
# ✅ Implementation {status}

## 📊 Summary

**Total tasks:** {total_tasks}
**Completed:** {completed_count} ✅
**Failed:** {failed_count} ❌
**Skipped:** {skipped_count} ⏭️
**Success rate:** {success_rate}%

**Duration:** {duration}
**Estimated effort:** {total_hours}h

---

## 📄 Reports

**Full report:** `{WORK_DIR}/implementation-report-{timestamp}.md`
**Checkpoint:** `{WORK_DIR}/.smartspec-checkpoint.json`
**Tasks file:** `{TASKS_FILE}`

---

## 🔍 Status Details

{If completed_count > 0:}
✅ **Completed:** {completed_task_ids}

{If failed_count > 0:}
❌ **Failed:** {failed_task_ids}

{If skipped_count > 0:}
⏭️ **Skipped:** {skipped_task_ids}

---

## ⏭️ Next Steps

{If status == COMPLETE:}
1. Review full report: `{report_file}`
2. Run final validation
3. Commit changes

{If status == PARTIAL:}
1. Review failed tasks in report
2. Fix issues manually
3. Resume: `/smartspec_implement_tasks {path} --resume`

{If status == FAILED:}
1. Check error details in report
2. Fix critical issues
3. Restart: `/smartspec_implement_tasks {path}`
```

**FINAL VERIFICATION:**
```
Processed tasks: {current_task_index}/{total_tasks}

IF current_task_index == total_tasks:
  ✅ SUCCESS - All tasks in FILTERED_TASKS were processed
ELSE:
  ❌ ERROR - Loop terminated early, not all tasks processed
  ⚠️ This indicates a workflow execution error
```

## 9. Save Artifacts

**STEP 1: Save implementation report to file (MANDATORY)**

**Action:** Write the FULL report from section 8 to file
- Path: `{WORK_DIR}/implementation-report-{timestamp}.md`
- Content: Complete markdown report with all sections:
  - Summary
  - Completed Tasks (full list)
  - Failed Tasks (full list with errors)
  - Skipped Tasks (full list with reasons)
  - Validation Status
  - Files Modified
  - Checkpoints Created
  - Next Steps
  - Resume Command

**IMPORTANT:** This file contains the FULL detailed report

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

## 10. Report to User

**IMPORTANT: Return ONLY the compact summary from section 8 STEP 2**
**DO NOT return the full report - it's already saved to file**

**What to return:**
- Use the compact summary template from section 8 STEP 2
- Include: status, statistics, file paths, next steps
- Keep it under 50 lines total

**What NOT to return:**
- Full list of completed tasks
- Full list of failed tasks with error details
- Full list of skipped tasks
- Full validation details
- Full file modification list

**Reason:** Save context space and prevent context overflow

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

---

# UI Centralization Addendum (Penpot-first)

เอกสารนี้เป็นส่วนเสริมของ **SmartSpec Centralization Contract**  
เพื่อรองรับ **SPEC ประเภท UI** ที่มีข้อกำหนดพิเศษ:

- **UI design source of truth เป็น JSON** (เพื่อใช้กับ Penpot)
- ทีม UI ต้องสามารถแก้ UI ได้ตรงจากไฟล์นี้
- งานของทีม dev ต้องผูกกับ component/logic โดยไม่ทำให้ไฟล์ UI JSON ปน logic

ใช้ addendum นี้วางต่อท้าย contract ในทุก workflow ที่แตะ UI:
- generate-spec
- generate-plan
- generate-tasks
- implement-tasks
- verify-tasks-progress
- generate-tests
- refactor-code
- reverse-to-spec
- reindex-specs
- validate-index
- sync-spec-tasks
- fix-errors
- generate-implement-prompt / generate-cursor-prompt (ในส่วน canonical constraints)

---

## 1) UI File Model

สำหรับ UI spec ให้ถือว่าในโฟลเดอร์ spec มีไฟล์หลัก 2 ชั้น:

1) `spec.md`  
   - narrative, scope, non-goals, UX rules, accessibility, performance targets  
   - อ้างอิงไฟล์ UI JSON เป็น design artifact

2) `ui.json` (หรือชื่อที่ทีมกำหนดใน config)  
   - **Penpot-editable**  
   - เก็บ layout, components mapping, design tokens references  
   - **ห้าม** ใส่ business logic หรือ API behaviour ในไฟล์นี้

> ถ้าทีมต้องการชื่อไฟล์เฉพาะ ให้กำหนดใน config:
```json
{
  "ui_spec": {
    "ui_json_name": "ui.json",
    "component_registry": "ui-component-registry.json"
  }
}
```

---

## 2) Registry เพิ่มเติมสำหรับ UI (แนะนำ)

เพิ่มไฟล์ registry ใหม่แบบ optional:

- `.spec/registry/ui-component-registry.json`

โครงสร้างขั้นต่ำแนะนำ:
```json
{
  "version": "1.0.0",
  "last_updated": "ISO-8601",
  "components": [
    {
      "canonical_name": "UserAvatar",
      "penpot_component_id": "penpot:component:xxx",
      "code_component_path": "src/components/user/UserAvatar.tsx",
      "owned_by_spec": "spec-XXX",
      "aliases": []
    }
  ]
}
```

**กติกา:**
- ชื่อ component ใน tasks/implementation ต้องอ้าง `canonical_name` เป็นค่า default
- ถ้าพบชื่อใหม่:
  - generate-spec / generate-tasks สามารถเพิ่ม entry ใหม่ได้
  - implement / verify ต้องอ่านอย่างเดียว

---

## 3) UI Naming & Separation Rules (MUST)

### 3.1 Separation of Concerns

- `ui.json` = design + structure + bindings
- business logic / data fetching / permissions  
  ต้องอยู่ใน:
  - code components
  - service layer
  - hooks/store
  - หรือ spec.md ในส่วน logic description

### 3.2 Canonical-first

เมื่อ workflow ต้องเสนอชื่อ component:
1) เช็ค `ui-component-registry.json` (ถ้ามี)
2) เช็ค glossary (คำเรียกหน้าจอ/ฟีเจอร์)
3) ถ้ายังไม่มี:
   - เสนอชื่อใหม่แบบ `Proposed`
   - สร้าง task ให้ลงทะเบียน

---

## 4) Workflow-specific Enforcement

### 4.1 generate-spec (UI category)

ต้อง:
- ตรวจ/สร้าง `ui.json` template ขั้นต่ำ (ถ้ายังไม่มี)
- เพิ่ม `ui.json` ลงใน SPEC_INDEX `files` (ถ้าสคีมารองรับ)
- ระบุใน spec.md ว่า:
  - design source-of-truth = ui.json
  - logic อยู่ที่ code layer

### 4.2 generate-tasks

สำหรับ UI spec:
- สร้าง 3 กลุ่มงานแยกกันชัดเจน:

1) **Design tasks (UI team)**
   - ปรับ layout/flow ใน `ui.json` ผ่าน Penpot

2) **Component binding tasks**
   - map Penpot component → code component
   - อัปเดต `ui-component-registry.json` (ถ้าจำเป็น)

3) **Logic tasks (Dev team)**
   - สร้าง/แก้ hooks/services/state
   - ห้ามใส่ logic ใหม่ใน `ui.json`

### 4.3 implement-tasks / refactor-code

- Treat `ui.json` เป็น **design-owned**
- แก้ไขได้เฉพาะเมื่อ tasks ระบุชัดเจน
- ถ้าพบว่า logic ถูกฝังใน ui.json:
  - สร้าง refactor task เพื่อย้าย logic ออก

### 4.4 generate-tests

- อ้าง component canonical names
- สนับสนุนแนวทาง:
  - component tests
  - accessibility checks
  - visual regression (ถ้าทีมใช้)

---

## 5) Index & Validation Rules

### 5.1 SPEC_INDEX

สำหรับ UI spec:
- แนะนำให้มี field เสริมใน entry (ถ้าทีมอนุญาตแบบ additive):
```json
{
  "ui_artifacts": {
    "ui_json_path": "specs/ui/spec-123/ui.json",
    "penpot_project": "optional-string"
  }
}
```

ถ้าไม่เพิ่ม schema:
- ให้ใช้ `files` list แทน

### 5.2 validate-index / global-registry-audit

ต้องตรวจอย่างน้อย:
- UI spec ที่ category=ui ต้องมี `ui.json`
- ชื่อ component ที่ spec/tasks อ้าง ต้องสอดคล้องกับ registry

---

## 6) ผลลัพธ์ที่ต้องการ

- ทีม UI แก้ UI ได้โดยไม่ชนกับ dev logic
- ลดการแตกชื่อ component ซ้ำซ้อน
- UI specs กลายเป็นส่วนหนึ่งของ centralization ไม่ใช่โลกคู่ขนาน
