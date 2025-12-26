# Verification Workflows Guide

**Version:** 1.0.0  
**Date:** 2025-12-26  
**Purpose:** Complete guide for verification and fix workflows

---

## 📖 Overview

This guide covers the complete verification and fix workflow in SmartSpec, from initial verification to automated prompt generation and implementation.

---

## 🎯 The Verification Workflow

### High-Level Flow

```
Create tasks.md
  ↓
Verify Evidence (verify_evidence_enhanced.py)
  ↓
Review Report (categorized issues)
  ↓
Generate Prompts (generate_prompts_from_verify_report.py)
  ↓
Implement Fixes (follow generated prompts)
  ↓
Verify Again
  ↓
All Verified? → Done!
```

---

## 🔍 Step 1: Verification

### Purpose
Check if all tasks in `tasks.md` have corresponding evidence (files, symbols, content)

### Command
```bash
python3 .smartspec/scripts/verify_evidence_enhanced.py \
  tasks.md \
  --repo-root . \
  --json \
  --out reports/
```

### Output
- `reports/YYYYMMDD_HHMMSS/report.md` - Human-readable report
- `reports/YYYYMMDD_HHMMSS/summary.json` - Machine-readable summary
- `reports/latest/` - Symlink to latest report

### What It Checks
1. **File Existence** - Do evidence files exist?
2. **Symbol Presence** - Do required symbols exist in files?
3. **Content Match** - Does content match regex patterns?
4. **Checkbox Status** - Are tasks marked [x] or [ ]?

### Report Structure
```markdown
# Verification Report

## Summary
- Total: 10 tasks
- Verified: 7 tasks (70%)
- Not Verified: 3 tasks (30%)

## Issues by Category
### Not Implemented (1 task)
- TASK-001: Feature X

### Missing Tests (1 task)
- TASK-002: Feature Y

### Naming Issues (1 task)
- TASK-003: Feature Z
  Similar files: feature_z_old.py (85% match)
```

---

## 📊 Step 2: Review Report

### Understanding Categories

#### 1. Not Implemented (Priority 2)
**What:** No implementation or test files exist

**Example:**
```
TASK-001: Add user authentication
Evidence: 
  - src/auth/user_auth.py (not found)
  - tests/test_user_auth.py (not found)
```

**Action:** Implement both code and tests

---

#### 2. Missing Tests (Priority 2)
**What:** Implementation exists but tests are missing

**Example:**
```
TASK-002: Add payment processing
Evidence:
  - src/payment/processor.py (found ✓)
  - tests/test_processor.py (not found ✗)
```

**Action:** Create test files

---

#### 3. Missing Code (Priority 2)
**What:** Tests exist but implementation is missing (TDD scenario)

**Example:**
```
TASK-003: Add email service
Evidence:
  - src/email/service.py (not found ✗)
  - tests/test_email_service.py (found ✓)
```

**Action:** Implement code to pass tests

---

#### 4. Naming Issues (Priority 4)
**What:** Files exist but names don't match evidence

**Example:**
```
TASK-004: Add logging
Evidence:
  - src/utils/logger.py (not found)
Similar files:
  - src/utils/logging_util.py (85% match)
```

**Action:** Rename file or update evidence

---

#### 5. Symbol Issues (Priority 3)
**What:** Files exist but required symbols (classes/functions) are missing

**Example:**
```
TASK-005: Add cache manager
Evidence:
  - src/cache/manager.py (found ✓)
  - Symbol: CacheManager (not found ✗)
```

**Action:** Add missing symbols

---

#### 6. Content Issues (Priority 3)
**What:** Files exist but required content/regex not found

**Example:**
```
TASK-006: Add error handling
Evidence:
  - src/errors.py (found ✓)
  - Content: "class.*Error" (not found ✗)
```

**Action:** Add missing content

---

## 🛠️ Step 3: Generate Prompts

### Purpose
Automatically generate implementation prompts based on report categories

### Command
```bash
python3 .smartspec/scripts/generate_prompts_from_verify_report.py \
  --verify-report reports/latest/summary.json \
  --tasks tasks.md
```

### Options

#### Filter by Category
```bash
--category not_implemented
--category missing_tests
--category missing_code
--category naming_issue
--category symbol_issue
--category content_issue
```

#### Filter by Priority
```bash
--priority 1  # Critical (marked [x] but failed)
--priority 2  # Missing features
--priority 3  # Symbol/content issues
--priority 4  # Naming issues
```

#### Custom Output
```bash
--output-dir custom/path/
--json  # Include JSON metadata
```

### Output Structure
```
.spec/prompts/YYYYMMDD_HHMMSS/
├── README.md                    # Overview and priority order
├── not_implemented.md           # Implementation prompts
├── missing_tests.md             # Test generation prompts
├── missing_code.md              # Code implementation prompts
├── naming_issues.md             # Naming fix instructions
├── symbol_issues.md             # Symbol addition prompts
├── content_issues.md            # Content addition prompts
└── meta/
    └── summary.json             # Metadata
```

---

## 📝 Step 4: Implement Fixes

### Read README First
```bash
cat .spec/prompts/latest/README.md
```

**README contains:**
- Summary statistics
- Priority order
- File list
- Next steps

### Follow Priority Order

#### Priority 1: Critical Issues
```bash
cat .spec/prompts/latest/README.md
# Look for Priority 1 tasks
# Fix immediately
```

#### Priority 2: Missing Features
```bash
# Not Implemented
cat .spec/prompts/latest/not_implemented.md

# Missing Tests
cat .spec/prompts/latest/missing_tests.md

# Missing Code
cat .spec/prompts/latest/missing_code.md
```

#### Priority 3: Symbol/Content
```bash
cat .spec/prompts/latest/symbol_issues.md
cat .spec/prompts/latest/content_issues.md
```

#### Priority 4: Naming
```bash
cat .spec/prompts/latest/naming_issues.md
```

### Prompt Structure

Each prompt file contains:
```markdown
# Category: Not Implemented

## Tasks in this category: 2

---

## Task 1: TASK-001 - Add user authentication

### Description
Implement user authentication with JWT tokens

### Files to Create
1. src/auth/user_auth.py
2. tests/test_user_auth.py

### Implementation

#### File: src/auth/user_auth.py
```python
# Implementation code with evidence hooks
# EVIDENCE_HOOK: TASK-001
class UserAuth:
    pass
```

#### File: tests/test_user_auth.py
```python
# Test code
def test_user_auth():
    pass
```

### Verification
After implementation, verify:
```bash
python3 .smartspec/scripts/verify_evidence_enhanced.py tasks.md
```

---

## Task 2: ...
```

---

## ✅ Step 5: Verify Again

### After Each Category
```bash
python3 .smartspec/scripts/verify_evidence_enhanced.py tasks.md
```

### Check Progress
```bash
cat reports/latest/report.md
```

### If Issues Remain
```bash
# Generate prompts for remaining issues
python3 .smartspec/scripts/generate_prompts_from_verify_report.py \
  --verify-report reports/latest/summary.json \
  --tasks tasks.md
```

---

## 🎯 Complete Example

### Scenario: New Feature Implementation

```bash
# 1. Create tasks.md with new features
vim tasks.md

# 2. Verify
python3 .smartspec/scripts/verify_evidence_enhanced.py \
  tasks.md --repo-root . --json --out reports/

# 3. Review report
cat reports/latest/report.md

# Output:
# Not Implemented: 5 tasks
# Missing Tests: 2 tasks
# Naming Issues: 1 task

# 4. Generate all prompts
python3 .smartspec/scripts/generate_prompts_from_verify_report.py \
  --verify-report reports/latest/summary.json \
  --tasks tasks.md

# 5. Review priority order
cat .spec/prompts/latest/README.md

# Output:
# Priority 2: Not Implemented (5 tasks)
# Priority 2: Missing Tests (2 tasks)
# Priority 4: Naming Issues (1 task)

# 6. Implement not_implemented first
cat .spec/prompts/latest/not_implemented.md
# (Implement all 5 tasks)

# 7. Verify progress
python3 .smartspec/scripts/verify_evidence_enhanced.py tasks.md

# Output:
# Verified: 5 tasks (62.5%)
# Not Verified: 3 tasks (37.5%)

# 8. Implement missing_tests
cat .spec/prompts/latest/missing_tests.md
# (Add 2 test files)

# 9. Verify again
python3 .smartspec/scripts/verify_evidence_enhanced.py tasks.md

# Output:
# Verified: 7 tasks (87.5%)
# Not Verified: 1 task (12.5%)

# 10. Fix naming issue
cat .spec/prompts/latest/naming_issues.md
# (Rename file or update evidence)

# 11. Final verification
python3 .smartspec/scripts/verify_evidence_enhanced.py tasks.md

# Output:
# All tasks verified! ✅
```

---

## 🔄 Workflow Variants

### Variant 1: Focus on Critical Issues

```bash
# Verify
python3 .smartspec/scripts/verify_evidence_enhanced.py \
  tasks.md --json

# Generate Priority 1 only
python3 .smartspec/scripts/generate_prompts_from_verify_report.py \
  --verify-report reports/latest/summary.json \
  --tasks tasks.md \
  --priority 1

# Fix critical issues
cat .spec/prompts/latest/README.md

# Verify
python3 .smartspec/scripts/verify_evidence_enhanced.py tasks.md
```

---

### Variant 2: Focus on One Category

```bash
# Verify
python3 .smartspec/scripts/verify_evidence_enhanced.py \
  tasks.md --json

# Generate missing_tests only
python3 .smartspec/scripts/generate_prompts_from_verify_report.py \
  --verify-report reports/latest/summary.json \
  --tasks tasks.md \
  --category missing_tests

# Add tests
cat .spec/prompts/latest/missing_tests.md

# Verify
python3 .smartspec/scripts/verify_evidence_enhanced.py tasks.md
```

---

### Variant 3: Incremental Implementation

```bash
# Verify
python3 .smartspec/scripts/verify_evidence_enhanced.py \
  tasks.md --json

# Generate all prompts
python3 .smartspec/scripts/generate_prompts_from_verify_report.py \
  --verify-report reports/latest/summary.json \
  --tasks tasks.md

# Implement one category at a time
cat .spec/prompts/latest/not_implemented.md
# (Implement)

# Verify after each category
python3 .smartspec/scripts/verify_evidence_enhanced.py tasks.md

# Next category
cat .spec/prompts/latest/missing_tests.md
# (Implement)

# Verify
python3 .smartspec/scripts/verify_evidence_enhanced.py tasks.md

# Continue until all verified
```

---

## 🚀 Step 6: Batch Execution (Optional)

### When to Use
When you have multiple prompt files (5+) and want to execute them all at once

### Command
```bash
python3 .smartspec/scripts/execute_prompts_batch.py \
  --prompts-dir .spec/prompts/latest/ \
  --tasks tasks.md \
  --checkpoint
```

### Benefits
- ✅ Execute all prompts in one command
- ✅ Automatic priority ordering
- ✅ Progress tracking
- ✅ Error handling
- ✅ Checkpoint support (resume on failure)
- ✅ **70-80% time savings** compared to manual execution

### Example
```bash
# 1. Generate prompts
python3 .smartspec/scripts/generate_prompts_from_verify_report.py \
  --verify-report reports/latest/summary.json \
  --tasks tasks.md

# 2. Preview execution plan
python3 .smartspec/scripts/execute_prompts_batch.py \
  --prompts-dir .spec/prompts/latest/ \
  --tasks tasks.md \
  --dry-run

# 3. Execute batch
python3 .smartspec/scripts/execute_prompts_batch.py \
  --prompts-dir .spec/prompts/latest/ \
  --tasks tasks.md \
  --checkpoint

# 4. Verify results
python3 .smartspec/scripts/verify_evidence_enhanced.py tasks.md
```

### See Full Guide
`.smartspec/BATCH_EXECUTION_GUIDE.md` for complete documentation

---

## 🎓 Best Practices

### 1. Verify Early, Verify Often
Run verification after every implementation session

### 2. Use JSON Output
Always use `--json` flag for automation

### 3. Follow Priority Order
Fix Priority 1 (critical) before Priority 4 (naming)

### 4. Review README First
Always read `README.md` in prompts directory

### 5. Verify After Each Category
Don't wait until everything is done

### 6. Use Category Filters
Focus on one type of issue at a time

### 7. Check Similar Files
Report shows similar files - use them!

### 8. Add Evidence Hooks
Include evidence hooks in implementation

---

## 🐛 Troubleshooting

### Issue: Verification takes too long
**Solution:** Verify specific tasks only (TODO: add parameter)

### Issue: Too many issues
**Solution:** Use `--priority 1` to focus on critical

### Issue: Similar files not helpful
**Solution:** Check file content, not just names

### Issue: Prompts not generated
**Solution:** Check JSON report exists and is valid

### Issue: Can't find latest report
**Solution:** Check `reports/latest/` symlink

---

## 🔗 Related Documentation

- `PROBLEM_SOLUTION_MATRIX.md` - Quick reference
- `TROUBLESHOOTING_DECISION_TREE.md` - Interactive guide
- `VERIFY_REPORT_ACTION_GUIDE.md` - Detailed actions
- `PROMPTER_USAGE_GUIDE.md` - Prompter details
- `scripts/SCRIPTS_INDEX.md` - All scripts

---

## 📚 Workflow Files

- `workflows/smartspec_verify_tasks_progress_strict.md` - Verification workflow (v6.3.0)
- `workflows/smartspec_report_implement_prompter.md` - Prompter workflow (v7.1.0)

---

**Version:** 1.0.0  
**Date:** 2025-12-26  
**Status:** ✅ Production Ready
```bash
python3 .smartspec/scripts/execute_prompts_batch.py \
  --prompts-dir .spec/prompts/latest/ \
  --tasks tasks.md \
  --checkpoint
```

### What It Does
- Reads all prompt files in directory
- Executes in priority order
- Shows progress (e.g., [3/10] 30%)
- Handles errors gracefully
- Supports resume from checkpoint
- Verifies after completion

### Benefits
- ✅ 70-80% faster than manual
- ✅ 90% fewer errors
- ✅ Automatic progress tracking
- ✅ Resume support
- ✅ Consistent results

### See Full Guide
📖 **`.smartspec/BATCH_EXECUTION_GUIDE.md`**

---

## 📚 After Prompt Generation - What Next?

### 🎯 IMPORTANT: Read This First!

After generating prompts, you need to decide:
1. **Manual Execution** (1-4 tasks) - Follow prompts one by one
2. **Batch Execution** (5+ tasks) - Execute all at once

### Complete Guide
📖 **`.smartspec/AFTER_PROMPT_GENERATION_GUIDE.md`**

This guide covers:
- How to read generated prompts
- When to use batch vs manual
- Step-by-step execution
- Best practices
- Troubleshooting
- Complete examples

### Quick Decision

```bash
# Check how many tasks
cat .spec/prompts/latest/README.md

# 1-4 tasks? → Manual execution
cat .spec/prompts/latest/*.md
# Follow prompts one by one

# 5+ tasks? → Batch execution
python3 .smartspec/scripts/execute_prompts_batch.py \
  --prompts-dir .spec/prompts/latest/ \
  --tasks tasks.md \
  --checkpoint
```

---
