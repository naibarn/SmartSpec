# smartspec_execute_prompts_batch

**Version:** 1.0.0  
**Category:** Implementation  
**Status:** Production Ready  
**Autopilot:** Recommended

---

## Overview

Execute all generated prompts in a single batch run with automatic priority ordering, progress tracking, and error handling.

---

## Purpose

After generating implementation prompts with `smartspec_report_implement_prompter`, this workflow executes all prompts in the correct order, implementing fixes for all verification issues in one go.

---

## When to Use

- After generating prompts from verify report
- When you have multiple prompt files to execute
- When you want automated batch implementation
- When you need progress tracking across multiple tasks

---

## Prerequisites

- Generated prompts directory (from `smartspec_report_implement_prompter`)
- tasks.md file
- Repository with write access

---

## Parameters

### Required

- `--prompts-dir` - Directory containing generated prompts (e.g., `.spec/prompts/20251226_083000/`)
- `--tasks` - Path to tasks.md file

### Optional

- `--checkpoint` - Enable checkpointing (resume on failure)
- `--dry-run` - Preview execution plan without making changes
- `--skip-category` - Skip specific categories (comma-separated)
- `--only-category` - Execute only specific categories (comma-separated)
- `--max-failures` - Maximum failures before stopping (default: 3)
- `--verify-after-each` - Verify after each category (default: false)
- `--verify-at-end` - Verify at the end (default: true)

---

## Usage

### Basic Usage

```bash
/smartspec_execute_prompts_batch \
  --prompts-dir .spec/prompts/20251226_083000/ \
  --tasks tasks.md
```

### With Checkpointing

```bash
/smartspec_execute_prompts_batch \
  --prompts-dir .spec/prompts/latest/ \
  --tasks tasks.md \
  --checkpoint
```

### Dry Run (Preview Only)

```bash
/smartspec_execute_prompts_batch \
  --prompts-dir .spec/prompts/latest/ \
  --tasks tasks.md \
  --dry-run
```

### Skip Specific Categories

```bash
/smartspec_execute_prompts_batch \
  --prompts-dir .spec/prompts/latest/ \
  --tasks tasks.md \
  --skip-category naming_issue,content_issue
```

### Execute Only High Priority

```bash
/smartspec_execute_prompts_batch \
  --prompts-dir .spec/prompts/latest/ \
  --tasks tasks.md \
  --only-category not_implemented,missing_tests
```

---

## Execution Order

The workflow executes prompts in this priority order:

1. **Priority 1** - Critical issues (marked [x] but failed)
2. **Priority 2** - Missing features
   - not_implemented
   - missing_tests
   - missing_code
3. **Priority 3** - Symbol/content issues
   - symbol_issue
   - content_issue
4. **Priority 4** - Naming issues
   - naming_issue

---

## Implementation Steps

### Step 1: Read Prompts Directory

```
Read prompts directory structure:
.spec/prompts/20251226_083000/
├── README.md
├── not_implemented.md
├── missing_tests.md
├── missing_code.md
├── naming_issues.md
├── symbol_issues.md
├── content_issues.md
└── meta/
    └── summary.json
```

Parse:
- README.md for overview
- summary.json for metadata
- Each category file for tasks

---

### Step 2: Create Execution Plan

```
Execution Plan:
1. not_implemented (Priority 2, 5 tasks)
2. missing_tests (Priority 2, 2 tasks)
3. symbol_issues (Priority 3, 1 task)
4. naming_issues (Priority 4, 1 task)

Total: 9 tasks across 4 categories
Estimated time: 15-20 minutes
```

If `--dry-run`, show plan and exit.

---

### Step 3: Execute Each Category

For each category file:

#### 3.1. Parse Category File

Extract:
- Task ID
- Task title
- Files to create/modify
- Implementation code
- Test code
- Evidence hooks

#### 3.2. Execute Tasks in Category

For each task in category:

1. **Create/modify files**
   ```python
   # Create code file
   Path(code_path).parent.mkdir(parents=True, exist_ok=True)
   Path(code_path).write_text(code_content)
   
   # Create test file
   Path(test_path).parent.mkdir(parents=True, exist_ok=True)
   Path(test_path).write_text(test_content)
   ```

2. **Add evidence hooks**
   ```python
   # Ensure evidence hooks are present
   if "EVIDENCE_HOOK" not in code_content:
       add_evidence_hook(code_path, task_id)
   ```

3. **Track progress**
   ```
   ✅ [1/9] TASK-001: Add user authentication
   ✅ [2/9] TASK-002: Add payment processing
   ⏳ [3/9] TASK-003: Add email service
   ```

4. **Handle errors**
   ```python
   try:
       execute_task(task)
   except Exception as e:
       log_error(task_id, str(e))
       failures += 1
       if failures >= max_failures:
           save_checkpoint()
           raise
   ```

#### 3.3. Verify After Category (Optional)

If `--verify-after-each`:
```bash
python3 .smartspec/scripts/verify_evidence_enhanced.py tasks.md
```

#### 3.4. Save Checkpoint

If `--checkpoint`:
```json
{
  "timestamp": "2025-12-26 08:30:00",
  "prompts_dir": ".spec/prompts/20251226_083000/",
  "completed_categories": ["not_implemented", "missing_tests"],
  "current_category": "symbol_issues",
  "current_task": 3,
  "total_tasks": 9,
  "failures": 0
}
```

---

### Step 4: Final Verification

If `--verify-at-end` (default):

```bash
python3 .smartspec/scripts/verify_evidence_enhanced.py \
  tasks.md \
  --repo-root . \
  --json \
  --out .spec/reports/
```

---

### Step 5: Generate Summary Report

```markdown
# Batch Execution Summary

**Started:** 2025-12-26 08:30:00
**Completed:** 2025-12-26 08:45:00
**Duration:** 15 minutes

## Results

**Total Tasks:** 9
**Successful:** 8 (89%)
**Failed:** 1 (11%)

## By Category

### not_implemented (5 tasks)
- ✅ TASK-001: Add user authentication
- ✅ TASK-002: Add payment processing
- ✅ TASK-003: Add email service
- ✅ TASK-004: Add logging
- ✅ TASK-005: Add caching

### missing_tests (2 tasks)
- ✅ TASK-006: Add auth tests
- ✅ TASK-007: Add payment tests

### symbol_issues (1 task)
- ❌ TASK-008: Add CacheManager class
  Error: Syntax error in generated code

### naming_issues (1 task)
- ✅ TASK-009: Rename logger.py

## Verification

**Before:**
- Total: 10 tasks
- Verified: 1 (10%)
- Not Verified: 9 (90%)

**After:**
- Total: 10 tasks
- Verified: 9 (90%)
- Not Verified: 1 (10%)

## Failed Tasks

### TASK-008: Add CacheManager class
**Error:** Syntax error in generated code
**File:** src/cache/manager.py
**Line:** 42
**Fix:** Manual intervention required

## Next Steps

1. Fix failed task: TASK-008
2. Run verification again
3. Commit changes

---

**Report saved to:** .spec/reports/batch_execution_20251226_084500.md
```

---

## Output Structure

```
.spec/
├── prompts/
│   └── 20251226_083000/          # Input prompts
│       ├── README.md
│       ├── not_implemented.md
│       └── ...
├── reports/
│   ├── batch_execution_20251226_084500.md    # Summary report
│   └── batch_execution_20251226_084500.json  # JSON metadata
└── checkpoints/
    └── batch_execution_20251226_083000.json  # Checkpoint (if enabled)
```

---

## Error Handling

### Recoverable Errors

- File already exists → Skip or overwrite (based on flag)
- Directory creation fails → Retry with sudo (if allowed)
- Syntax error in generated code → Log and continue

### Non-Recoverable Errors

- Prompts directory not found → Exit
- tasks.md not found → Exit
- Max failures reached → Save checkpoint and exit
- Permission denied → Exit

### Resume After Failure

If execution fails with checkpoint enabled:

```bash
# Resume from checkpoint
/smartspec_execute_prompts_batch \
  --prompts-dir .spec/prompts/20251226_083000/ \
  --tasks tasks.md \
  --checkpoint \
  --resume
```

---

## Best Practices

### 1. Always Use Dry Run First

```bash
# Preview execution plan
/smartspec_execute_prompts_batch \
  --prompts-dir .spec/prompts/latest/ \
  --tasks tasks.md \
  --dry-run
```

### 2. Enable Checkpointing for Large Batches

```bash
# For 10+ tasks
/smartspec_execute_prompts_batch \
  --prompts-dir .spec/prompts/latest/ \
  --tasks tasks.md \
  --checkpoint
```

### 3. Verify After Each Category for Critical Changes

```bash
# Verify incrementally
/smartspec_execute_prompts_batch \
  --prompts-dir .spec/prompts/latest/ \
  --tasks tasks.md \
  --verify-after-each
```

### 4. Skip Low Priority for Quick Wins

```bash
# Focus on high priority
/smartspec_execute_prompts_batch \
  --prompts-dir .spec/prompts/latest/ \
  --tasks tasks.md \
  --skip-category naming_issue
```

### 5. Commit After Successful Execution

```bash
# After successful batch
git add -A
git commit -m "feat: Implement tasks from batch execution"
```

---

## Integration with Other Workflows

### Complete Workflow

```bash
# 1. Verify
/smartspec_verify_tasks_progress_strict tasks.md

# 2. Generate prompts
/smartspec_report_implement_prompter \
  --verify-report .spec/reports/latest/summary.json \
  --tasks tasks.md

# 3. Execute batch (NEW!)
/smartspec_execute_prompts_batch \
  --prompts-dir .spec/prompts/latest/ \
  --tasks tasks.md \
  --checkpoint

# 4. Verify again
/smartspec_verify_tasks_progress_strict tasks.md
```

---

## Troubleshooting

### Issue: Prompts directory not found

**Solution:**
```bash
# Check latest symlink
ls -la .spec/prompts/latest

# Or use specific directory
/smartspec_execute_prompts_batch \
  --prompts-dir .spec/prompts/20251226_083000/ \
  --tasks tasks.md
```

### Issue: Too many failures

**Solution:**
```bash
# Increase max failures
/smartspec_execute_prompts_batch \
  --prompts-dir .spec/prompts/latest/ \
  --tasks tasks.md \
  --max-failures 10
```

### Issue: Want to skip problematic category

**Solution:**
```bash
# Skip category
/smartspec_execute_prompts_batch \
  --prompts-dir .spec/prompts/latest/ \
  --tasks tasks.md \
  --skip-category symbol_issues
```

---

## Safety Features

### 1. Dry Run Mode
Preview all changes before execution

### 2. Checkpointing
Resume from failure point

### 3. Max Failures Limit
Stop before causing too much damage

### 4. Verification
Confirm implementation correctness

### 5. Detailed Logging
Track all operations for debugging

---

## Performance

### Typical Execution Times

- **Small batch** (1-5 tasks): 2-5 minutes
- **Medium batch** (6-15 tasks): 5-15 minutes
- **Large batch** (16-30 tasks): 15-30 minutes
- **Very large batch** (30+ tasks): 30+ minutes

### Optimization Tips

1. Use `--skip-category` for low priority
2. Disable `--verify-after-each` for speed
3. Use `--only-category` for focused execution
4. Run in parallel (advanced, not recommended)

---

## Examples

### Example 1: Quick Fix

```bash
# Execute only critical issues
/smartspec_execute_prompts_batch \
  --prompts-dir .spec/prompts/latest/ \
  --tasks tasks.md \
  --only-category not_implemented
```

### Example 2: Safe Execution

```bash
# Dry run first
/smartspec_execute_prompts_batch \
  --prompts-dir .spec/prompts/latest/ \
  --tasks tasks.md \
  --dry-run

# Then execute with checkpoint
/smartspec_execute_prompts_batch \
  --prompts-dir .spec/prompts/latest/ \
  --tasks tasks.md \
  --checkpoint \
  --verify-after-each
```

### Example 3: Resume After Failure

```bash
# First run (failed)
/smartspec_execute_prompts_batch \
  --prompts-dir .spec/prompts/latest/ \
  --tasks tasks.md \
  --checkpoint

# Fix the issue manually

# Resume
/smartspec_execute_prompts_batch \
  --prompts-dir .spec/prompts/latest/ \
  --tasks tasks.md \
  --checkpoint \
  --resume
```

---

## Related Workflows

- `smartspec_verify_tasks_progress_strict` - Verify tasks
- `smartspec_report_implement_prompter` - Generate prompts
- `smartspec_implement_tasks` - Implement single task

---

## Version History

- **1.0.0** (2025-12-26) - Initial release

---

## Metadata

```yaml
workflow_id: smartspec_execute_prompts_batch
version: 1.0.0
category: implementation
status: production_ready
autopilot: recommended
inputs:
  - prompts_dir: .spec/prompts/<timestamp>/
  - tasks: tasks.md
outputs:
  - report: .spec/reports/batch_execution_<timestamp>.md
  - checkpoint: .spec/checkpoints/batch_execution_<timestamp>.json
safety_level: medium
requires_approval: false
supports_checkpoint: true
supports_parallel: false
estimated_duration: 5-30 minutes
```
