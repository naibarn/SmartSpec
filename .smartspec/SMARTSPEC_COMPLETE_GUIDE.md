# SmartSpec Complete Guide

**Version:** 2.0.0  
**Date:** 2025-12-26  
**Purpose:** Complete guide from verification to implementation

---

## 📖 Table of Contents

1. [Introduction](#introduction)
2. [Quick Start](#quick-start)
3. [Verification Workflow](#verification-workflow)
4. [Understanding Verification Reports](#understanding-verification-reports)
5. [Prompt Generation](#prompt-generation)
6. [After Prompt Generation](#after-prompt-generation)
7. [Batch Execution](#batch-execution)
8. [Complete Examples](#complete-examples)
9. [Best Practices](#best-practices)
10. [FAQ](#faq)
11. [Troubleshooting](#troubleshooting)

---

## Introduction

SmartSpec provides an automated workflow for verifying task completion, generating implementation prompts, and executing fixes. This guide covers the complete workflow from start to finish.

### What You'll Learn

- How to verify tasks and understand reports
- How to generate prompts for fixing issues
- When to use batch vs manual execution
- Best practices for efficient workflows
- Troubleshooting common problems

### Prerequisites

- SmartSpec installed
- Python 3 available
- tasks.md file with evidence markers

---

## Quick Start

### The Complete Workflow

```
1. Verify → 2. Generate Prompts → 3. Execute → 4. Verify Again
```

### 30-Second Example

```bash
# 1. Verify
/smartspec_verify_tasks_progress_strict tasks.md --json

# 2. Generate prompts
/smartspec_report_implement_prompter \
  --verify-report .spec/reports/latest/summary.json \
  --tasks tasks.md

# 3. Execute (if 5+ tasks)
/smartspec_execute_prompts_batch \
  --prompts-dir .spec/prompts/latest/ \
  --tasks tasks.md

# 4. Verify again
/smartspec_verify_tasks_progress_strict tasks.md
```

---

## Verification Workflow

### Step 1: Run Verification

**Basic Usage:**
```bash
/smartspec_verify_tasks_progress_strict tasks.md
```

**With JSON Output:**
```bash
/smartspec_verify_tasks_progress_strict tasks.md \
  --out .spec/reports/verify-tasks-progress/latest \
  --json
```

**With Platform (Kilo):**
```bash
/smartspec_verify_tasks_progress_strict tasks.md \
  --out .spec/reports/verify-tasks-progress/latest \
  --json \
  --platform kilo
```

### What Verification Does

1. ✅ Reads tasks.md
2. ✅ Checks evidence for each task
3. ✅ Categorizes issues
4. ✅ Generates detailed report
5. ✅ Provides recommendations

### Output Files

- `report.md` - Human-readable report
- `summary.json` - Machine-readable data
- `README.md` - Quick summary

---

## Understanding Verification Reports

### Report Structure

```markdown
# Executive Summary
- Total tasks: 152
- Verified: 59 (38%)
- Not Verified: 93 (61%)

# Problem Categories
1. Naming Issues (79 tasks)
2. Missing Tests (11 tasks)
3. Missing Code (2 tasks)
4. Symbol Issues (1 task)
```

### Problem Categories

#### 1. Naming Issues
**Problem:** Files exist but names don't match evidence

**Example:**
```
Expected: jwt.util.test.ts
Found: jwt.util.edge-cases.test.ts
```

**Solution:** Update evidence or rename file

---

#### 2. Missing Tests
**Problem:** Implementation exists but no test file

**Example:**
```
✅ Code: src/auth.service.ts
❌ Test: tests/auth.service.test.ts (not found)
```

**Solution:** Create test file

---

#### 3. Missing Code
**Problem:** Evidence file doesn't exist

**Example:**
```
❌ Code: src/phone.routes.ts (not found)
```

**Solution:** Implement the code

---

#### 4. Symbol Issues
**Problem:** File exists but symbol not found

**Example:**
```
✅ File: src/auth.ts
❌ Symbol: validateToken (not found)
```

**Solution:** Add missing symbol

---

## Prompt Generation

### When to Generate Prompts

After verification, if you have issues to fix:

```bash
# Check report
cat .spec/reports/latest/summary.json

# If not_verified > 0, generate prompts
/smartspec_report_implement_prompter \
  --verify-report .spec/reports/latest/summary.json \
  --tasks tasks.md
```

### Basic Usage

```bash
/smartspec_report_implement_prompter \
  --verify-report .spec/reports/verify-tasks-progress/latest/summary.json \
  --tasks tasks.md \
  --out .spec/prompts/latest
```

### Filter by Category

```bash
# Only missing tests
/smartspec_report_implement_prompter \
  --verify-report .spec/reports/latest/summary.json \
  --tasks tasks.md \
  --category missing_tests

# Only naming issues
/smartspec_report_implement_prompter \
  --verify-report .spec/reports/latest/summary.json \
  --tasks tasks.md \
  --category naming_issues
```

### Filter by Priority

```bash
# Only Priority 1 (critical)
/smartspec_report_implement_prompter \
  --verify-report .spec/reports/latest/summary.json \
  --tasks tasks.md \
  --priority 1

# Priority 1 and 2
/smartspec_report_implement_prompter \
  --verify-report .spec/reports/latest/summary.json \
  --tasks tasks.md \
  --priority 1,2
```

### Output Structure

```
.spec/prompts/latest/
├── README.md                  # Summary
├── not_implemented.md         # Implementation prompts
├── missing_tests.md           # Test creation prompts
├── naming_issues.md           # Naming fix prompts
└── symbol_issues.md           # Symbol fix prompts
```

---

## After Prompt Generation

### Decision Tree

```
How many prompt files generated?
├─ 1-4 tasks → Manual Execution
│  └─ Read prompts one by one
│     └─ Implement manually
│        └─ Verify after each
└─ 5+ tasks → Batch Execution (Recommended)
   └─ Use execute_prompts_batch.py
      └─ Automatic execution
         └─ Verify at end
```

### Check Generated Prompts

```bash
# Read summary
cat .spec/prompts/latest/README.md

# Output example:
# Generated 8 prompts:
# - not_implemented.md (3 tasks)
# - missing_tests.md (5 tasks)
#
# Recommendation: Use batch execution
```

### Manual Execution (1-4 tasks)

```bash
# 1. Read each prompt
cat .spec/prompts/latest/not_implemented.md

# 2. Follow instructions
# (Implement code as described)

# 3. Verify
/smartspec_verify_tasks_progress_strict tasks.md

# 4. Next prompt
cat .spec/prompts/latest/missing_tests.md

# 5. Repeat
```

### Batch Execution (5+ tasks)

```bash
# Execute all prompts at once
/smartspec_execute_prompts_batch \
  --prompts-dir .spec/prompts/latest/ \
  --tasks tasks.md \
  --checkpoint
```

**See [Batch Execution](#batch-execution) section for details**

---

## Batch Execution

### When to Use

- ✅ 5+ tasks to implement
- ✅ Similar task types
- ✅ Want to save time
- ✅ Want consistency

### Basic Usage

```bash
/smartspec_execute_prompts_batch \
  --prompts-dir .spec/prompts/latest/ \
  --tasks tasks.md
```

### With Checkpoint (Recommended)

```bash
/smartspec_execute_prompts_batch \
  --prompts-dir .spec/prompts/latest/ \
  --tasks tasks.md \
  --checkpoint
```

**Benefits:**
- Resume if interrupted
- Skip completed tasks
- Save progress

### Dry Run (Test First)

```bash
/smartspec_execute_prompts_batch \
  --prompts-dir .spec/prompts/latest/ \
  --tasks tasks.md \
  --dry-run
```

**Output:**
```
Would execute 8 tasks:
1. TSK-001: Create auth service
2. TSK-002: Add tests
...
8. TSK-008: Fix naming
```

### Priority Ordering

```bash
/smartspec_execute_prompts_batch \
  --prompts-dir .spec/prompts/latest/ \
  --tasks tasks.md \
  --priority-order
```

**Execution Order:**
1. Priority 1 tasks first
2. Then Priority 2
3. Then Priority 3

### Category Filtering

```bash
# Only execute missing_tests
/smartspec_execute_prompts_batch \
  --prompts-dir .spec/prompts/latest/ \
  --tasks tasks.md \
  --category missing_tests
```

### Progress Tracking

```
🚀 Executing 8 tasks...

[1/8] TSK-001: Create auth service
✅ Success (2.3s)

[2/8] TSK-002: Add tests
✅ Success (1.8s)

...

[8/8] TSK-008: Fix naming
✅ Success (0.5s)

📊 Results:
✅ Success: 8/8 (100%)
❌ Failed: 0/8 (0%)
⏱️  Total time: 15.2s
```

### Resume After Failure

```bash
# If execution stopped
/smartspec_execute_prompts_batch \
  --prompts-dir .spec/prompts/latest/ \
  --tasks tasks.md \
  --checkpoint \
  --resume
```

### Benefits

| Aspect | Manual | Batch | Improvement |
|:---|:---:|:---:|:---:|
| **Time (8 tasks)** | 40 min | 10 min | -75% |
| **Errors** | 2-3 | 0-1 | -80% |
| **Consistency** | Variable | High | +90% |
| **Tracking** | Manual | Automatic | +100% |

---

## Complete Examples

### Example 1: First-Time Verification

```bash
# 1. Verify
/smartspec_verify_tasks_progress_strict tasks.md \
  --out .spec/reports/verify-tasks-progress/spec-001 \
  --json

# Output:
# Verified: 10/50 (20%)
# Not Verified: 40/50 (80%)

# 2. Check report
cat .spec/reports/verify-tasks-progress/spec-001/report.md

# 3. Generate prompts
/smartspec_report_implement_prompter \
  --verify-report .spec/reports/verify-tasks-progress/spec-001/summary.json \
  --tasks tasks.md \
  --out .spec/prompts/spec-001

# Output:
# Generated 4 prompt files
# Total tasks: 40

# 4. Check count
cat .spec/prompts/spec-001/README.md

# Output:
# 40 tasks → Recommended: Batch execution

# 5. Execute batch
/smartspec_execute_prompts_batch \
  --prompts-dir .spec/prompts/spec-001/ \
  --tasks tasks.md \
  --checkpoint

# Output:
# ✅ 38/40 success (95%)
# ❌ 2/40 failed (5%)

# 6. Verify again
/smartspec_verify_tasks_progress_strict tasks.md

# Output:
# Verified: 48/50 (96%)
# Not Verified: 2/50 (4%)

# 7. Fix remaining 2 manually
cat .spec/prompts/spec-001/failed_tasks.md

# 8. Final verify
/smartspec_verify_tasks_progress_strict tasks.md

# Output:
# ✅ All tasks verified! (100%)
```

---

### Example 2: Incremental Implementation

```bash
# 1. Verify
/smartspec_verify_tasks_progress_strict tasks.md --json

# 2. Generate Priority 1 only
/smartspec_report_implement_prompter \
  --verify-report .spec/reports/latest/summary.json \
  --tasks tasks.md \
  --priority 1 \
  --out .spec/prompts/p1

# 3. Execute P1
/smartspec_execute_prompts_batch \
  --prompts-dir .spec/prompts/p1/ \
  --tasks tasks.md

# 4. Verify
/smartspec_verify_tasks_progress_strict tasks.md --json

# 5. Generate Priority 2
/smartspec_report_implement_prompter \
  --verify-report .spec/reports/latest/summary.json \
  --tasks tasks.md \
  --priority 2 \
  --out .spec/prompts/p2

# 6. Execute P2
/smartspec_execute_prompts_batch \
  --prompts-dir .spec/prompts/p2/ \
  --tasks tasks.md

# 7. Final verify
/smartspec_verify_tasks_progress_strict tasks.md
```

---

### Example 3: Category-Focused

```bash
# 1. Verify
/smartspec_verify_tasks_progress_strict tasks.md --json

# 2. Fix naming issues first
/smartspec_report_implement_prompter \
  --verify-report .spec/reports/latest/summary.json \
  --tasks tasks.md \
  --category naming_issues

# 3. Execute (manual - usually quick)
cat .spec/prompts/latest/naming_issues.md
# (Update evidence in tasks.md)

# 4. Verify again
/smartspec_verify_tasks_progress_strict tasks.md --json

# 5. Add missing tests
/smartspec_report_implement_prompter \
  --verify-report .spec/reports/latest/summary.json \
  --tasks tasks.md \
  --category missing_tests

# 6. Execute batch
/smartspec_execute_prompts_batch \
  --prompts-dir .spec/prompts/latest/ \
  --tasks tasks.md

# 7. Final verify
/smartspec_verify_tasks_progress_strict tasks.md
```

---

## Best Practices

### 1. Always Use JSON Output

```bash
# ✅ Good
/smartspec_verify_tasks_progress_strict tasks.md --json

# ❌ Bad
/smartspec_verify_tasks_progress_strict tasks.md
```

**Why:** JSON output enables prompt generation

---

### 2. Use Checkpoint for Batch

```bash
# ✅ Good
/smartspec_execute_prompts_batch \
  --checkpoint

# ❌ Bad
/smartspec_execute_prompts_batch
```

**Why:** Can resume if interrupted

---

### 3. Dry Run First

```bash
# ✅ Good
/smartspec_execute_prompts_batch \
  --dry-run

# Then execute
/smartspec_execute_prompts_batch
```

**Why:** Preview what will happen

---

### 4. Fix by Priority

```bash
# ✅ Good
--priority 1  # Critical first
--priority 2  # Then important
--priority 3  # Then nice-to-have

# ❌ Bad
# Fix everything at once
```

**Why:** Focus on critical issues first

---

### 5. Verify After Each Major Change

```bash
# ✅ Good
implement → verify → implement → verify

# ❌ Bad
implement → implement → implement → verify
```

**Why:** Catch issues early

---

### 6. Use Descriptive Output Paths

```bash
# ✅ Good
--out .spec/reports/verify-tasks-progress/spec-core-001-auth

# ❌ Bad
--out .spec/reports/latest
```

**Why:** Easy to track and reference

---

### 7. Keep Prompts Organized

```bash
# ✅ Good structure
.spec/prompts/
├── spec-core-001-auth/
│   ├── 2025-12-26-initial/
│   └── 2025-12-26-p1-only/
└── spec-core-002-api/
    └── 2025-12-26-initial/

# ❌ Bad structure
.spec/prompts/
├── prompts1/
├── prompts2/
└── latest/
```

**Why:** Easy to find and reference

---

## FAQ

### Q1: How do I know if I should use batch or manual?

**A:** Check the README.md in prompts directory:
- 1-4 tasks → Manual
- 5+ tasks → Batch

---

### Q2: Can I resume batch execution if it fails?

**A:** Yes, if you used `--checkpoint`:

```bash
/smartspec_execute_prompts_batch \
  --checkpoint \
  --resume
```

---

### Q3: What if verification still fails after batch execution?

**A:**
1. Check execution report
2. Review failed tasks
3. Fix manually
4. Verify again

---

### Q4: Can I filter prompts by multiple categories?

**A:** Yes:

```bash
--category missing_tests,missing_code
```

---

### Q5: How do I see what batch execution will do?

**A:** Use dry run:

```bash
--dry-run
```

---

### Q6: Can I execute only specific tasks?

**A:** Yes:

```bash
--tasks TSK-001,TSK-002,TSK-003
```

---

### Q7: What if I want to skip some tasks?

**A:** Use exclude:

```bash
--exclude TSK-010,TSK-020
```

---

### Q8: How do I track progress?

**A:** Batch execution shows real-time progress:

```
[3/10] TSK-003: Add tests
✅ Success (1.2s)
```

---

### Q9: Can I run verification on specific tasks only?

**A:** Not directly, but you can filter in tasks.md:

```markdown
# Only verify these
- [ ] TSK-001
- [ ] TSK-002
```

---

### Q10: What's the fastest workflow?

**A:**

```bash
# 1. Verify with JSON
/smartspec_verify_tasks_progress_strict tasks.md --json

# 2. Generate all prompts
/smartspec_report_implement_prompter \
  --verify-report .spec/reports/latest/summary.json \
  --tasks tasks.md

# 3. Batch execute
/smartspec_execute_prompts_batch \
  --prompts-dir .spec/prompts/latest/ \
  --tasks tasks.md \
  --checkpoint

# 4. Verify again
/smartspec_verify_tasks_progress_strict tasks.md
```

**Time:** ~10-15 minutes for 50 tasks

---

## Troubleshooting

### Issue 1: Verification Fails

**Symptoms:**
```
Error: tasks.md not found
```

**Solutions:**
1. Check file path
2. Run from project root
3. Verify file exists

---

### Issue 2: No Prompts Generated

**Symptoms:**
```
No prompts generated
```

**Solutions:**
1. Check if verification found issues
2. Verify JSON output exists
3. Check category/priority filters

---

### Issue 3: Batch Execution Fails

**Symptoms:**
```
Error: prompts directory not found
```

**Solutions:**
1. Check prompts-dir path
2. Verify prompts were generated
3. Check directory structure

---

### Issue 4: Tasks Still Not Verified

**Symptoms:**
```
Verified: 45/50 (90%)
```

**Solutions:**
1. Check report for remaining issues
2. Generate prompts for remaining
3. Fix manually if < 5 tasks
4. Run batch if >= 5 tasks

---

### Issue 5: Checkpoint Not Working

**Symptoms:**
```
Warning: checkpoint file not found
```

**Solutions:**
1. Use `--checkpoint` flag
2. Check write permissions
3. Verify .spec directory exists

---

### Issue 6: Slow Execution

**Symptoms:**
```
[1/50] Taking too long...
```

**Solutions:**
1. Use `--parallel` flag (if available)
2. Filter by priority
3. Execute in batches

---

### Issue 7: Wrong Evidence Path

**Symptoms:**
```
Evidence not found: wrong/path.ts
```

**Solutions:**
1. Check naming issues in report
2. Update evidence in tasks.md
3. Or rename file to match

---

### Issue 8: Symbol Not Found

**Symptoms:**
```
Symbol 'validateToken' not found
```

**Solutions:**
1. Check if symbol exists
2. Check symbol name spelling
3. Check export statement
4. Update evidence if needed

---

## Summary

### Complete Workflow

```
1. Verify
   ↓
2. Check Report
   ↓
3. Generate Prompts
   ↓
4. Check Count
   ↓
5. Execute (Batch or Manual)
   ↓
6. Verify Again
   ↓
7. Repeat if Needed
   ↓
8. Done! ✅
```

### Key Commands

```bash
# Verify
/smartspec_verify_tasks_progress_strict tasks.md --json

# Generate
/smartspec_report_implement_prompter \
  --verify-report .spec/reports/latest/summary.json \
  --tasks tasks.md

# Execute
/smartspec_execute_prompts_batch \
  --prompts-dir .spec/prompts/latest/ \
  --tasks tasks.md \
  --checkpoint
```

### Time Savings

- **Manual:** 40 minutes for 8 tasks
- **Batch:** 10 minutes for 8 tasks
- **Savings:** 75% faster

---

## Additional Resources

- 📖 **WORKFLOW_REFERENCE.md** - Quick reference
- 📖 **SMARTSPEC_HANDBOOK.md** - Installation & setup
- 📖 **AUTOPILOT_GUIDE.md** - Autopilot features

---

**Version:** 2.0.0  
**Last Updated:** 2025-12-26  
**Consolidated From:**
- VERIFICATION_WORKFLOWS_GUIDE.md
- AFTER_PROMPT_GENERATION_GUIDE.md
- BATCH_EXECUTION_GUIDE.md
- PROMPTER_USAGE_GUIDE.md
- VERIFY_REPORT_ACTION_GUIDE.md
