# Workflow Reference Guide

**Version:** 2.0.0  
**Date:** 2025-12-26  
**Purpose:** Quick reference for workflows, parameters, and troubleshooting

---

## 📖 Table of Contents

1. [Quick Reference](#quick-reference)
2. [Problem-Solution Matrix](#problem-solution-matrix)
3. [Troubleshooting Decision Tree](#troubleshooting-decision-tree)
4. [Workflow Parameters](#workflow-parameters)
5. [Common Scenarios](#common-scenarios)

---

## Quick Reference

### Problem → Solution Mapping

| Problem | Category | Workflow | Priority |
|:---|:---|:---|:---:|
| Tasks not verified | Verification | verify → generate → execute | High |
| Missing tests | Missing Tests | Generate prompts → Add tests | High |
| Missing code | Missing Code | Generate prompts → Implement | High |
| Naming mismatch | Naming Issues | Update evidence or rename | Medium |
| Symbol not found | Symbol Issues | Add symbol to code | Medium |


---

## Problem Solution Matrix

---

## How to Use This Matrix

1. **Find your problem** in the table below
2. **Check the category** and priority
3. **Run the recommended command**
4. **Follow the next steps**

---

## Quick Reference Table

| Problem | Category | Priority | Workflow | Command | Next Steps |
|:---|:---|:---:|:---|:---|:---|
| **Verification failed** | All | 1 | Verify → Prompter | `verify_evidence_enhanced.py tasks.md --json` | Review report, generate prompts |
| **Tasks not implemented** | Not Implemented | 2 | Prompter → Implement | `generate_prompts_from_verify_report.py --category not_implemented` | Follow prompts, implement files |
| **Tests missing** | Missing Tests | 2 | Prompter → Test | `generate_prompts_from_verify_report.py --category missing_tests` | Create test files |
| **Code missing (TDD)** | Missing Code | 2 | Prompter → Code | `generate_prompts_from_verify_report.py --category missing_code` | Implement code for existing tests |
| **File names wrong** | Naming Issue | 4 | Manual Fix | Check report `similar_files` | Rename files or update evidence |
| **Symbols missing** | Symbol Issue | 3 | Prompter → Add | `generate_prompts_from_verify_report.py --category symbol_issue` | Add missing symbols |
| **Content missing** | Content Issue | 3 | Prompter → Add | `generate_prompts_from_verify_report.py --category content_issue` | Add missing content |
| **Critical issues** | Any | 1 | Prompter Priority | `generate_prompts_from_verify_report.py --priority 1` | Fix marked [x] but failed tasks |
| **Multiple categories** | Mixed | 2 | Prompter All | `generate_prompts_from_verify_report.py --verify-report report.json` | Fix by priority order |
| **Multiple prompts** | Batch | 2 | Batch Execute | `execute_prompts_batch.py --prompts-dir .spec/prompts/latest/` | Execute all at once |

---

## Detailed Problem-Solution Mapping

### 1. Verification Failed

**Symptoms:**
- `verify_evidence_enhanced.py` shows failures
- Tasks marked [x] but not verified
- Evidence not found

**Diagnosis:**
```bash
python3 .smartspec/scripts/verify_evidence_enhanced.py \
  tasks.md \
  --repo-root . \
  --json \
  --out reports/
```

**Solution Path:**
```
1. Review report: cat reports/latest/report.md
2. Check category: Look at "by_category" section
3. Generate prompts: See command below
4. Implement fixes: Follow generated prompts
5. Verify again: Run verify script
```

**Commands:**
```bash
# Step 1: Verify
python3 .smartspec/scripts/verify_evidence_enhanced.py \
  tasks.md --repo-root . --json --out reports/

# Step 2: Generate prompts
python3 .smartspec/scripts/generate_prompts_from_verify_report.py \
  --verify-report reports/latest/summary.json \
  --tasks tasks.md

# Step 3: Review
cat .spec/prompts/latest/README.md

# Step 4: Implement (follow prompts in category files)

# Step 5: Verify again
python3 .smartspec/scripts/verify_evidence_enhanced.py \
  tasks.md --repo-root .
```

---

### 2. Tasks Not Implemented

**Symptoms:**
- No implementation files
- No test files
- Category: "not_implemented"

**Diagnosis:**
Check verify report for "not_implemented" category

**Solution Path:**
```
1. Generate implementation prompts
2. Create implementation files
3. Create test files
4. Add evidence hooks
5. Verify
```

**Commands:**
```bash
# Generate prompts for not implemented tasks
python3 .smartspec/scripts/generate_prompts_from_verify_report.py \
  --verify-report reports/latest/summary.json \
  --tasks tasks.md \
  --category not_implemented

# Review prompts
cat .spec/prompts/latest/not_implemented.md

# Implement following the prompts
# (Create files, add code, add tests)

# Verify
python3 .smartspec/scripts/verify_evidence_enhanced.py \
  tasks.md --repo-root .
```

---

### 3. Tests Missing

**Symptoms:**
- Implementation files exist
- Test files missing
- Category: "missing_tests"

**Diagnosis:**
Check verify report for "missing_tests" category

**Solution Path:**
```
1. Generate test prompts
2. Create test files
3. Write unit tests
4. Run tests
5. Verify
```

**Commands:**
```bash
# Generate prompts for missing tests
python3 .smartspec/scripts/generate_prompts_from_verify_report.py \
  --verify-report reports/latest/summary.json \
  --tasks tasks.md \
  --category missing_tests

# Review prompts
cat .spec/prompts/latest/missing_tests.md

# Create test files following prompts

# Run tests
pytest tests/ -v

# Verify
python3 .smartspec/scripts/verify_evidence_enhanced.py \
  tasks.md --repo-root .
```

---

### 4. Code Missing (TDD Scenario)

**Symptoms:**
- Test files exist
- Implementation files missing
- Category: "missing_code"

**Diagnosis:**
Check verify report for "missing_code" category

**Solution Path:**
```
1. Generate code prompts
2. Create implementation files
3. Implement to pass tests
4. Run tests
5. Verify
```

**Commands:**
```bash
# Generate prompts for missing code
python3 .smartspec/scripts/generate_prompts_from_verify_report.py \
  --verify-report reports/latest/summary.json \
  --tasks tasks.md \
  --category missing_code

# Review prompts
cat .spec/prompts/latest/missing_code.md

# Implement code following prompts

# Run tests
pytest tests/ -v

# Verify
python3 .smartspec/scripts/verify_evidence_enhanced.py \
  tasks.md --repo-root .
```

---

### 5. File Names Wrong

**Symptoms:**
- Files exist but names don't match evidence
- Report shows "similar_files" with high similarity
- Category: "naming_issue"

**Diagnosis:**
Check verify report for "similar_files" suggestions

**Solution Path:**
```
Option A: Rename files to match evidence
Option B: Update evidence to match files
```

**Commands:**
```bash
# Option A: Rename files
mv old_name.py new_name.py

# Option B: Update evidence in tasks.md
vim tasks.md  # Update evidence path

# Verify
python3 .smartspec/scripts/verify_evidence_enhanced.py \
  tasks.md --repo-root .
```

**Example:**
```
Report says:
  Expected: tests/ss_autopilot/test_checkpoint_manager.py
  Found similar: tests/ss_autopilot/test_agent_wrapper.py (65% match)

Solution:
  Either rename test_agent_wrapper.py to test_checkpoint_manager.py
  OR update evidence in tasks.md to point to test_agent_wrapper.py
```

---

### 6. Symbols Missing

**Symptoms:**
- Files exist
- Required symbols (classes/functions) not found
- Category: "symbol_issue"

**Diagnosis:**
Check verify report for missing symbols

**Solution Path:**
```
1. Generate symbol prompts
2. Add missing symbols
3. Verify
```

**Commands:**
```bash
# Generate prompts for symbol issues
python3 .smartspec/scripts/generate_prompts_from_verify_report.py \
  --verify-report reports/latest/summary.json \
  --tasks tasks.md \
  --category symbol_issue

# Review prompts
cat .spec/prompts/latest/symbol_issues.md

# Add missing symbols to files

# Verify
python3 .smartspec/scripts/verify_evidence_enhanced.py \
  tasks.md --repo-root .
```

---

### 7. Content Missing

**Symptoms:**
- Files exist
- Required content/regex not found
- Category: "content_issue"

**Diagnosis:**
Check verify report for missing content

**Solution Path:**
```
1. Generate content prompts
2. Add missing content
3. Verify
```

**Commands:**
```bash
# Generate prompts for content issues
python3 .smartspec/scripts/generate_prompts_from_verify_report.py \
  --verify-report reports/latest/summary.json \
  --tasks tasks.md \
  --category content_issue

# Review prompts
cat .spec/prompts/latest/content_issues.md

# Add missing content to files

# Verify
python3 .smartspec/scripts/verify_evidence_enhanced.py \
  tasks.md --repo-root .
```

---

### 8. Critical Issues (Priority 1)

**Symptoms:**
- Tasks marked [x] but verification failed
- High priority issues
- Priority: 1

**Diagnosis:**
Check verify report for Priority 1 tasks

**Solution Path:**
```
1. Generate critical issue prompts
2. Fix immediately
3. Verify
```

**Commands:**
```bash
# Generate prompts for critical issues only
python3 .smartspec/scripts/generate_prompts_from_verify_report.py \
  --verify-report reports/latest/summary.json \
  --tasks tasks.md \
  --priority 1

# Review prompts
cat .spec/prompts/latest/README.md

# Fix critical issues first

# Verify
python3 .smartspec/scripts/verify_evidence_enhanced.py \
  tasks.md --repo-root .
```

---

### 9. Multiple Categories

**Symptoms:**
- Multiple types of issues
- Mixed categories
- Need systematic approach

**Diagnosis:**
Check verify report for all categories

**Solution Path:**
```
1. Generate all prompts
2. Review README for priority order
3. Fix by priority
4. Verify after each category
```

**Commands:**
```bash
# Generate prompts for all issues
python3 .smartspec/scripts/generate_prompts_from_verify_report.py \
  --verify-report reports/latest/summary.json \
  --tasks tasks.md

# Review priority order
cat .spec/prompts/latest/README.md

# Fix in order:
# 1. Priority 1 (critical)
# 2. Priority 2 (missing features)
# 3. Priority 3 (symbols/content)
# 4. Priority 4 (naming)

# Verify after each category
python3 .smartspec/scripts/verify_evidence_enhanced.py \
  tasks.md --repo-root .
```

---

## Workflow Selection Decision Tree

```
Start: Have a problem
  ↓
Q: Have you run verification?
  NO → Run verify_evidence_enhanced.py
  YES → Continue
  ↓
Q: What does the report show?
  ├→ Not Implemented → Use prompter --category not_implemented
  ├→ Missing Tests → Use prompter --category missing_tests
  ├→ Missing Code → Use prompter --category missing_code
  ├→ Naming Issues → Manual rename or update evidence
  ├→ Symbol Issues → Use prompter --category symbol_issue
  ├→ Content Issues → Use prompter --category content_issue
  ├→ Multiple → Use prompter (all categories)
  └→ Critical (Priority 1) → Use prompter --priority 1
  ↓
Implement fixes following generated prompts
  ↓
Verify again
  ↓
Q: All verified?
  YES → Done!
  NO → Repeat from verification
```

---

## Common Scenarios

### Scenario 1: Starting Fresh
**Situation:** New tasks.md, nothing implemented

**Steps:**
```bash
# 1. Verify to see what's missing
python3 .smartspec/scripts/verify_evidence_enhanced.py \
  tasks.md --repo-root . --json --out reports/

# 2. Generate all prompts
python3 .smartspec/scripts/generate_prompts_from_verify_report.py \
  --verify-report reports/latest/summary.json \
  --tasks tasks.md

# 3. Implement in priority order
cat .spec/prompts/latest/README.md

# 4. Verify progress
python3 .smartspec/scripts/verify_evidence_enhanced.py \
  tasks.md --repo-root .
```

---

### Scenario 2: Partial Implementation
**Situation:** Some tasks done, some missing

**Steps:**
```bash
# 1. Verify current state
python3 .smartspec/scripts/verify_evidence_enhanced.py \
  tasks.md --repo-root . --json --out reports/

# 2. Generate prompts for remaining issues
python3 .smartspec/scripts/generate_prompts_from_verify_report.py \
  --verify-report reports/latest/summary.json \
  --tasks tasks.md

# 3. Focus on not_implemented first
cat .spec/prompts/latest/not_implemented.md

# 4. Then missing_tests
cat .spec/prompts/latest/missing_tests.md

# 5. Verify
python3 .smartspec/scripts/verify_evidence_enhanced.py \
  tasks.md --repo-root .
```

---

### Scenario 3: Debugging Failures
**Situation:** Tasks marked [x] but failing verification

**Steps:**
```bash
# 1. Verify with JSON output
python3 .smartspec/scripts/verify_evidence_enhanced.py \
  tasks.md --repo-root . --json --out reports/

# 2. Generate prompts for Priority 1 only
python3 .smartspec/scripts/generate_prompts_from_verify_report.py \
  --verify-report reports/latest/summary.json \
  --tasks tasks.md \
  --priority 1

# 3. Fix critical issues
cat .spec/prompts/latest/README.md

# 4. Verify
python3 .smartspec/scripts/verify_evidence_enhanced.py \
  tasks.md --repo-root .
```

---

## Tips & Best Practices

### 1. Always Verify First
Before generating prompts, run verification to get current state

### 2. Use JSON Output
`--json` flag creates machine-readable reports for prompter

### 3. Filter When Needed
Use `--category` or `--priority` to focus on specific issues

### 4. Follow Priority Order
Fix Priority 1 (critical) before Priority 4 (naming)

### 5. Verify After Each Fix
Run verification after implementing each category

### 6. Check Similar Files
Report shows similar files - use them to identify naming issues

### 7. Read Suggestions
Report provides actionable suggestions for each task

### 8. Use Templates
Generated prompts include code templates - use them!

---

## Related Documentation

- `VERIFY_REPORT_ACTION_GUIDE.md` - Detailed action guide
- `PROMPTER_USAGE_GUIDE.md` - Complete prompter usage
- `TROUBLESHOOTING_DECISION_TREE.md` - Interactive troubleshooting

---

**Version:** 1.0.0  
**Date:** 2025-12-26  
**Status:** ✅ Production Ready



---

## Troubleshooting Decision Tree

---

## 🎯 How to Use This Guide

1. Start at the beginning
2. Answer each question
3. Follow the path
4. Get your solution!

---

## 🚀 Start Here

### Question 1: What do you want to do?

**A.** I want to verify my tasks → [Go to Verification](#verification)  
**B.** I have a verification report with issues → [Go to Fix Issues](#fix-issues)  
**C.** I want to implement new features → [Go to Implementation](#implementation)  
**D.** I have test failures → [Go to Test Failures](#test-failures)  
**E.** Something else → [Go to Other](#other)

---

## 🔍 Verification

### You want to verify your tasks

**Question:** Have you created `tasks.md`?

**YES** → Run verification:
```bash
python3 .smartspec/scripts/verify_evidence_enhanced.py \
  tasks.md \
  --repo-root . \
  --json \
  --out reports/
```

**NO** → Create `tasks.md` first, then run verification

---

### After Running Verification

**Question:** What does the report show?

**A.** All tasks verified ✅ → **Done!** You're good to go!

**B.** Some tasks not verified ❌ → [Go to Fix Issues](#fix-issues)

**C.** Error running script → [Go to Troubleshoot Verification](#troubleshoot-verification)

---

## 🛠️ Fix Issues

### You have a verification report with issues

**Question:** What type of issues do you have?

Check your report:
```bash
cat reports/latest/report.md
```

Look at the "Issues by Category" section.

---

### Issue Type Selection

**A.** Not Implemented (no files) → [Go to Not Implemented](#not-implemented)

**B.** Missing Tests (code exists, no tests) → [Go to Missing Tests](#missing-tests)

**C.** Missing Code (tests exist, no code) → [Go to Missing Code](#missing-code)

**D.** Naming Issues (wrong file names) → [Go to Naming Issues](#naming-issues)

**E.** Symbol Issues (missing symbols) → [Go to Symbol Issues](#symbol-issues)

**F.** Content Issues (missing content) → [Go to Content Issues](#content-issues)

**G.** Multiple types → [Go to Multiple Issues](#multiple-issues)

**H.** Critical (marked [x] but failed) → [Go to Critical Issues](#critical-issues)

---

## 📝 Not Implemented

### Problem: No implementation or test files exist

**Solution:** Generate implementation prompts

```bash
# Generate prompts
python3 .smartspec/scripts/generate_prompts_from_verify_report.py \
  --verify-report reports/latest/summary.json \
  --tasks tasks.md \
  --category not_implemented

# Review prompts
cat .spec/prompts/latest/not_implemented.md
```

**Next Steps:**
1. Read the generated prompts
2. Create implementation files
3. Create test files
4. Add evidence hooks
5. Run tests: `pytest tests/ -v`
6. Verify: `python3 .smartspec/scripts/verify_evidence_enhanced.py tasks.md`

**Expected Result:** Tasks verified ✅

---

## 🧪 Missing Tests

### Problem: Implementation files exist but test files are missing

**Solution:** Generate test prompts

```bash
# Generate prompts
python3 .smartspec/scripts/generate_prompts_from_verify_report.py \
  --verify-report reports/latest/summary.json \
  --tasks tasks.md \
  --category missing_tests

# Review prompts
cat .spec/prompts/latest/missing_tests.md
```

**Next Steps:**
1. Read the generated prompts
2. Create test files
3. Write unit tests
4. Run tests: `pytest tests/ -v`
5. Verify: `python3 .smartspec/scripts/verify_evidence_enhanced.py tasks.md`

**Expected Result:** Tests created and tasks verified ✅

---

## 💻 Missing Code

### Problem: Test files exist but implementation files are missing (TDD)

**Solution:** Generate code prompts

```bash
# Generate prompts
python3 .smartspec/scripts/generate_prompts_from_verify_report.py \
  --verify-report reports/latest/summary.json \
  --tasks tasks.md \
  --category missing_code

# Review prompts
cat .spec/prompts/latest/missing_code.md
```

**Next Steps:**
1. Read the generated prompts
2. Create implementation files
3. Implement code to pass tests
4. Run tests: `pytest tests/ -v`
5. Verify: `python3 .smartspec/scripts/verify_evidence_enhanced.py tasks.md`

**Expected Result:** Code implemented and tests pass ✅

---

## 📛 Naming Issues

### Problem: Files exist but names don't match evidence

**Check Report:** Look for "similar_files" suggestions

**Solution A: Rename Files**
```bash
# Rename file to match evidence
mv old_name.py new_name.py

# Verify
python3 .smartspec/scripts/verify_evidence_enhanced.py tasks.md
```

**Solution B: Update Evidence**
```bash
# Edit tasks.md to match actual file names
vim tasks.md

# Verify
python3 .smartspec/scripts/verify_evidence_enhanced.py tasks.md
```

**Question:** Which solution to use?

- **Rename files** if evidence path is correct
- **Update evidence** if file names are correct

**Expected Result:** Names match and tasks verified ✅

---

## 🔤 Symbol Issues

### Problem: Files exist but required symbols (classes/functions) not found

**Solution:** Generate symbol prompts

```bash
# Generate prompts
python3 .smartspec/scripts/generate_prompts_from_verify_report.py \
  --verify-report reports/latest/summary.json \
  --tasks tasks.md \
  --category symbol_issue

# Review prompts
cat .spec/prompts/latest/symbol_issues.md
```

**Next Steps:**
1. Read the generated prompts
2. Add missing symbols to files
3. Verify: `python3 .smartspec/scripts/verify_evidence_enhanced.py tasks.md`

**Expected Result:** Symbols added and tasks verified ✅

---

## 📄 Content Issues

### Problem: Files exist but required content/regex not found

**Solution:** Generate content prompts

```bash
# Generate prompts
python3 .smartspec/scripts/generate_prompts_from_verify_report.py \
  --verify-report reports/latest/summary.json \
  --tasks tasks.md \
  --category content_issue

# Review prompts
cat .spec/prompts/latest/content_issues.md
```

**Next Steps:**
1. Read the generated prompts
2. Add missing content to files
3. Verify: `python3 .smartspec/scripts/verify_evidence_enhanced.py tasks.md`

**Expected Result:** Content added and tasks verified ✅

---

## 🔥 Critical Issues

### Problem: Tasks marked [x] but verification failed (Priority 1)

**Solution:** Generate critical issue prompts

```bash
# Generate prompts for Priority 1 only
python3 .smartspec/scripts/generate_prompts_from_verify_report.py \
  --verify-report reports/latest/summary.json \
  --tasks tasks.md \
  --priority 1

# Review prompts
cat .spec/prompts/latest/README.md
```

**Next Steps:**
1. Read the generated prompts
2. Fix critical issues immediately
3. Verify: `python3 .smartspec/scripts/verify_evidence_enhanced.py tasks.md`

**Expected Result:** Critical issues fixed ✅

---

## 🎭 Multiple Issues

### Problem: Multiple types of issues across different categories

**Solution:** Generate all prompts and fix by priority

```bash
# Generate prompts for all issues
python3 .smartspec/scripts/generate_prompts_from_verify_report.py \
  --verify-report reports/latest/summary.json \
  --tasks tasks.md

# Review priority order
cat .spec/prompts/latest/README.md
```

**Priority Order:**
1. **Priority 1** - Critical (marked [x] but failed)
2. **Priority 2** - Missing features (not_implemented, missing_tests, missing_code)
3. **Priority 3** - Symbol/content issues
4. **Priority 4** - Naming issues

**Next Steps:**
1. Fix Priority 1 first
2. Then Priority 2
3. Then Priority 3
4. Finally Priority 4
5. Verify after each priority level

**Expected Result:** All issues fixed ✅

---

## 🔧 Implementation

### You want to implement new features

**Question:** Do you have `tasks.md` with evidence?

**YES** → Run verification first:
```bash
python3 .smartspec/scripts/verify_evidence_enhanced.py \
  tasks.md --repo-root . --json --out reports/
```

Then [Go to Fix Issues](#fix-issues)

**NO** → Create `tasks.md` first with evidence, then verify

---

## ❌ Test Failures

### You have test failures

**Question:** What type of test failure?

**A.** Tests not found → [Go to Missing Tests](#missing-tests)

**B.** Tests fail (assertion errors) → Fix implementation:
```bash
# Run tests to see failures
pytest tests/ -v

# Fix implementation
# (Edit code to pass tests)

# Run tests again
pytest tests/ -v

# Verify
python3 .smartspec/scripts/verify_evidence_enhanced.py tasks.md
```

**C.** Import errors → Check dependencies:
```bash
# Install dependencies
pip3 install -r requirements.txt

# Run tests
pytest tests/ -v
```

---

## 🤔 Other

### Something else not covered above

**Common Issues:**

#### Issue: Script not found
```bash
# Check if script exists
ls -la .smartspec/scripts/verify_evidence_enhanced.py

# If not found, check git status
git status

# Pull latest changes
git pull origin main
```

#### Issue: Permission denied
```bash
# Make script executable
chmod +x .smartspec/scripts/verify_evidence_enhanced.py
chmod +x .smartspec/scripts/generate_prompts_from_verify_report.py
```

#### Issue: Python version
```bash
# Check Python version (need 3.11+)
python3 --version

# If not installed, install Python 3.11
```

#### Issue: Module not found
```bash
# Install dependencies
pip3 install -r requirements.txt
```

---

## 🐛 Troubleshoot Verification

### Error running verification script

**Error 1: Script not found**
```bash
# Check path
ls -la .smartspec/scripts/verify_evidence_enhanced.py

# If not found, pull latest
git pull origin main
```

**Error 2: Permission denied**
```bash
# Make executable
chmod +x .smartspec/scripts/verify_evidence_enhanced.py
```

**Error 3: Python not found**
```bash
# Check Python
python3 --version

# Use python3 if python3 not available
python3 .smartspec/scripts/verify_evidence_enhanced.py tasks.md
```

**Error 4: tasks.md not found**
```bash
# Check if tasks.md exists
ls -la tasks.md

# Create if not exists
touch tasks.md
```

**Error 5: Invalid JSON**
```bash
# Run without --json first
python3 .smartspec/scripts/verify_evidence_enhanced.py \
  tasks.md --repo-root .

# Check output for errors
```

---

## 📊 Visual Decision Tree

```
START
  ↓
[What do you want to do?]
  ├→ Verify tasks
  │   ↓
  │  [Run verification]
  │   ↓
  │  [Check report]
  │   ├→ All verified ✅ → DONE
  │   └→ Issues found ❌ → [Go to Fix Issues]
  │
  ├→ Fix issues
  │   ↓
  │  [What type?]
  │   ├→ Not Implemented → [Generate prompts] → [Implement] → [Verify]
  │   ├→ Missing Tests → [Generate prompts] → [Add tests] → [Verify]
  │   ├→ Missing Code → [Generate prompts] → [Add code] → [Verify]
  │   ├→ Naming Issues → [Rename or update] → [Verify]
  │   ├→ Symbol Issues → [Generate prompts] → [Add symbols] → [Verify]
  │   ├→ Content Issues → [Generate prompts] → [Add content] → [Verify]
  │   ├→ Multiple → [Generate all] → [Fix by priority] → [Verify]
  │   └→ Critical → [Generate P1] → [Fix immediately] → [Verify]
  │
  ├→ Implement features
  │   ↓
  │  [Have tasks.md?]
  │   ├→ YES → [Verify] → [Go to Fix Issues]
  │   └→ NO → [Create tasks.md] → [Verify] → [Go to Fix Issues]
  │
  ├→ Test failures
  │   ↓
  │  [What type?]
  │   ├→ Tests not found → [Go to Missing Tests]
  │   ├→ Assertion errors → [Fix code] → [Run tests] → [Verify]
  │   └→ Import errors → [Install deps] → [Run tests]
  │
  └→ Other
      ↓
     [Check common issues]
      ├→ Script not found → [Pull latest]
      ├→ Permission denied → [chmod +x]
      ├→ Python version → [Install 3.11+]
      └→ Module not found → [pip install]
```

---

## 🎓 Examples

### Example 1: Fresh Start

**Situation:** New project, tasks.md created, nothing implemented

**Steps:**
```bash
# 1. Verify
python3 .smartspec/scripts/verify_evidence_enhanced.py \
  tasks.md --repo-root . --json --out reports/

# 2. Generate all prompts
python3 .smartspec/scripts/generate_prompts_from_verify_report.py \
  --verify-report reports/latest/summary.json \
  --tasks tasks.md

# 3. Review README
cat .spec/prompts/latest/README.md

# 4. Implement by priority
cat .spec/prompts/latest/not_implemented.md

# 5. Verify progress
python3 .smartspec/scripts/verify_evidence_enhanced.py tasks.md
```

---

### Example 2: Partial Progress

**Situation:** Some tasks done, some missing tests

**Steps:**
```bash
# 1. Verify current state
python3 .smartspec/scripts/verify_evidence_enhanced.py \
  tasks.md --repo-root . --json --out reports/

# 2. Generate prompts for missing tests
python3 .smartspec/scripts/generate_prompts_from_verify_report.py \
  --verify-report reports/latest/summary.json \
  --tasks tasks.md \
  --category missing_tests

# 3. Add tests
cat .spec/prompts/latest/missing_tests.md

# 4. Verify
python3 .smartspec/scripts/verify_evidence_enhanced.py tasks.md
```

---

### Example 3: Critical Issues

**Situation:** Tasks marked [x] but failing

**Steps:**
```bash
# 1. Verify
python3 .smartspec/scripts/verify_evidence_enhanced.py \
  tasks.md --repo-root . --json --out reports/

# 2. Generate Priority 1 prompts
python3 .smartspec/scripts/generate_prompts_from_verify_report.py \
  --verify-report reports/latest/summary.json \
  --tasks tasks.md \
  --priority 1

# 3. Fix critical issues
cat .spec/prompts/latest/README.md

# 4. Verify
python3 .smartspec/scripts/verify_evidence_enhanced.py tasks.md
```

---

## 🔗 Related Documentation

- `PROBLEM_SOLUTION_MATRIX.md` - Quick reference table
- `VERIFY_REPORT_ACTION_GUIDE.md` - Detailed action guide
- `PROMPTER_USAGE_GUIDE.md` - Complete prompter usage

---

## 💡 Tips

1. **Always verify first** - Know your current state
2. **Use JSON output** - Required for prompter
3. **Filter when needed** - Use `--category` or `--priority`
4. **Follow priority order** - Fix critical first
5. **Verify after each fix** - Track progress
6. **Read suggestions** - Report provides hints
7. **Use templates** - Generated prompts include code

---

**Version:** 1.0.0  
**Date:** 2025-12-26  
**Status:** ✅ Production Ready



---

## Workflow Parameters Reference

---

## smartspec_api_contract_validator

**Description:** Validate API contracts and OpenAPI specifications.

**Version:** 6.0.0

### Universal Flags (Supported)

These flags are supported by this workflow:
`--apply`, `--json`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_api_contract_validator \
  --contract <path/to/openapi.yaml> \
  --implementation-root <path/to/src> \
  [--spec <path/to/spec.md>] \
  [--spec-id <id>] \
  [--out <output-root>] \
  [--json] \
  [--strict]
```

**Kilo Code:**
```bash
/smartspec_api_contract_validator.md \
  --contract <path/to/openapi.yaml> \
  --implementation-root <path/to/src> \
  [--spec <path/to/spec.md>] \
  [--spec-id <id>] \
  [--out <output-root>] \
  [--json] \
  [--strict] \
  --platform kilo
```

---

## smartspec_code_assistant

**Description:** Consolidated implementation helper (implement/fix/refactor) producing

**Version:** 6.0.0

### Universal Flags (Supported)

These flags are supported by this workflow:
`--apply`, `--json`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_code_assistant \
  --mode <implement|fix|refactor> \
  [--spec <path/to/spec.md>] \
  [--tasks <path/to/tasks.md>] \
  [--context <path/to/log-or-error.txt>] \
  [--out <output-root>] \
  [--json]
```

**Kilo Code:**
```bash
/smartspec_code_assistant.md \
  --mode <implement|fix|refactor> \
  [--spec <path/to/spec.md>] \
  [--tasks <path/to/tasks.md>] \
  [--context <path/to/log-or-error.txt>] \
  [--out <output-root>] \
  [--json] \
  --platform kilo
```

---

## smartspec_data_migration_generator

**Description:** Generate data migration scripts and documentation.

**Version:** 6.0.0

### Universal Flags (Supported)

These flags are supported by this workflow:
`--apply`, `--json`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_data_migration_generator \
  --report <path/to/validation-report.json> \
  --migration-tool <flyway|liquibase|raw-sql> \
  --output-dir <path/to/migrations> \
  [--allow-destructive] \
  [--apply]
```

**Kilo Code:**
```bash
/smartspec_data_migration_generator.md \
  --report .spec/reports/data-model-validation/<run-id>/summary.json \
  --migration-tool flyway \
  --output-dir db/migrations \
  --platform kilo
```

---

## smartspec_data_model_validator

**Description:** Validate data models and database schemas.

**Version:** 6.0.0

### Universal Flags (Supported)

These flags are supported by this workflow:
`--apply`, `--json`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_data_model_validator \
  specs/<category>/<spec-id>/spec.md \
  [--schema-files <glob[,glob...]>] \
  [--model-files <glob[,glob...]>] \
  [--migration-files <glob[,glob...]>] \
  [--dialect <postgres|mysql|sqlite|mssql|other>] \
  [--orm <prisma|typeorm|sequelize|django|rails|sqlalchemy|other>] \
  [--strict] \
  [--out <output-root>] \
  [--json]
```

**Kilo Code:**
```bash
/smartspec_data_model_validator.md \
  specs/<category>/<spec-id>/spec.md \
  [--schema-files <glob[,glob...]>] \
  [--model-files <glob[,glob...]>] \
  [--migration-files <glob[,glob...]>] \
  [--dialect <postgres|mysql|sqlite|mssql|other>] \
  [--orm <prisma|typeorm|sequelize|django|rails|sqlalchemy|other>] \
  [--strict] \
  [--out <output-root>] \
  [--json] \
  --platform kilo
```

---

## smartspec_dependency_updater

**Version:** 1.0.0

### Universal Flags (Supported)

These flags are supported by this workflow:
`--config`, `--json`, `--lang`, `--out`, `--platform`, `--quiet`

---

## smartspec_deployment_planner

**Description:** Generate deployment plans and checklists.

**Version:** 6.1.1

### Universal Flags (Supported)

These flags are supported by this workflow:
`--config`, `--json`, `--lang`, `--out`, `--platform`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_deployment_planner \
  specs/<category>/<spec-id>/spec.md \
  --verify-summary .spec/reports/verify-tasks-progress/<run-id>/summary.json \
  --target-env prod \
  --out .spec/reports/deployment-planner \
  --json
```

**CLI:**
```bash
/smartspec_deployment_planner \
  specs/<category>/<spec-id>/spec.md \
  --verify-summary .spec/reports/verify-tasks-progress/<run-id>/summary.json \
  --apply \
  --out .spec/reports/deployment-planner \
  --json
```

---

## smartspec_design_system_migration_assistant

**Description:** Assist in migrating between design systems (e.g., MUI to Ant Design).

**Version:** 6.0.0

### Usage Examples

**CLI:**
```bash
/smartspec_design_system_migration_assistant \
  --source-root <path/to/ui> \
  --from mui \
  --to custom \
  [--audit-summary .spec/reports/ui-component-audit/<run-id>/summary.json] \
  [--token-map .smartspec/mappings/design-tokens.json] \
  [--framework auto] \
  [--style-system auto] \
  [--confidence-threshold high] \
  [--apply-scope high_only] \
  [--out <output-root>] \
  [--json]
```

**Kilo Code:**
```bash
/smartspec_design_system_migration_assistant.md \
  --source-root <path/to/ui> \
  --from mui \
  --to custom \
  [--audit-summary .spec/reports/ui-component-audit/<run-id>/summary.json] \
  [--token-map .smartspec/mappings/design-tokens.json] \
  [--framework auto] \
  [--style-system auto] \
  [--confidence-threshold high] \
  [--apply-scope high_only] \
  [--out <output-root>] \
  [--json] \
  --platform kilo
```

---

## smartspec_docs_generator

**Description:** Generate technical documentation from specs and code.

**Version:** 6.1.1

### Universal Flags (Supported)

These flags are supported by this workflow:
`--config`, `--json`, `--lang`, `--out`, `--platform`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_docs_generator \
  --mode api-docs \
  --spec specs/<category>/<spec-id>/spec.md \
  --out .spec/reports/docs-generator \
  --json
```

**CLI:**
```bash
/smartspec_docs_generator \
  --mode user-guide \
  --spec specs/<category>/<spec-id>/spec.md \
  --target-dir docs \
  --write-docs \
  --apply \
  --out .spec/reports/docs-generator \
  --json
```

---

## smartspec_docs_publisher

**Description:** Publish documentation to various platforms.

**Version:** 6.1.1

### Universal Flags (Supported)

These flags are supported by this workflow:
`--config`, `--json`, `--lang`, `--out`, `--platform`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_docs_publisher \
  --docs-dir .spec/reports/docs-generator/<run-id>/bundle.preview \
  --publish-platform github-pages \
  --version v1.2.3 \
  --remote origin \
  --github-branch gh-pages \
  --out .spec/reports/docs-publisher \
  --json
```

**CLI:**
```bash
/smartspec_docs_publisher \
  --docs-dir .spec/reports/docs-generator/<run-id>/bundle.preview \
  --publish-platform github-pages \
  --version v1.2.3 \
  --remote origin \
  --github-branch gh-pages \
  --allow-network \
  --apply \
  --out .spec/reports/docs-publisher \
  --json
```

---

## smartspec_export_catalog

### Parameters

| Parameter | Status | Description |
|---|---|---|
| `--catalog-id` | Optional | Unique catalog identifier (URL) |
| `--include-metadata` | Optional | Include SmartSpec metadata (optional) |
| `--input-catalog` | Optional | Source SmartSpec catalog path |
| `--output-file` | Optional | Destination A2UI catalog path |
| `--output-format` | Optional | Target format (a2ui-v0.8) |
| `--platform` | Optional | Platform filter (optional) |

### Usage Examples

**CLI:**
```bash
/smartspec_export_catalog \
  --output-file public/web-catalog.json \
  --catalog-id "https://my-app.com/web-catalog-v1" \
  --output-format a2ui-v0.8
```

---

## smartspec_feedback_aggregator

**Description:** Aggregate feedback from multiple sources to drive continuous improvement.

**Version:** 1.0.0

### Parameters

| Parameter | Status | Description |
|---|---|---|
| `--help` | Optional | Show help message. |
| `--quiet` | Optional | Suppress all output except errors. |
| `--run-once` | Optional | Run the aggregation process once and exit. |
| `--verbose` | Optional | Enable verbose logging. |
| `--version` | Optional | Show version. |

### Usage Examples

**CLI:**
```bash
/smartspec_feedback_aggregator \
  --run-once
```

---

## smartspec_generate_multiplatform_ui

### Usage Examples

**CLI:**
```bash
/smartspec_generate_multiplatform_ui \
  --spec specs/feature/spec-002-contact/ui-spec.json \
  --platforms web,flutter \
  --web-renderer lit \
  --output-dir src/ui/contact \
  --apply
```

**Kilo Code:**
```bash
/smartspec_generate_multiplatform_ui.md \
  --spec specs/feature/spec-002-contact/ui-spec.json \
  --platforms web,flutter \
  --web-renderer lit \
  --output-dir src/ui/contact \
  --platform kilo \
  --apply
```

---

## smartspec_generate_plan

**Description:** Convert spec.md → plan.md (preview-first; dependency-aware; reuse-first;

**Version:** 6.0.6

### Universal Flags (Supported)

These flags are supported by this workflow:
`--apply`, `--json`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_generate_plan <spec_md> [--apply] [--ui-mode auto|json|inline] [--safety-mode strict|dev] [--plan-layout per-spec|consolidated] [--run-label "..."] [--json]
```

**Kilo Code:**
```bash
/smartspec_generate_plan.md \
  specs/<category>/<spec-id>/spec.md \
  --platform kilo \
  [--apply] [--ui-mode auto|json|inline] [--safety-mode strict|dev] [--plan-layout per-spec|consolidated] [--run-label "..."] [--json]
```

---

## smartspec_generate_spec

**Description:** Refine spec.md (SPEC-first) with 100% duplication prevention and reuse-first

**Version:** 7.0.0

### Universal Flags (Supported)

These flags are supported by this workflow:
`--config`, `--json`, `--lang`, `--out`, `--platform`, `--quiet`

---

## smartspec_generate_spec_from_prompt

**Description:** Bootstrap starter specs from a natural-language prompt (ideation-first;

**Version:** 7.0.0

### Parameters

| Parameter | Status | Description |
|---|---|---|
| `--interactive` | Optional | Force interactive mode for clarifying questions, even in non-interactive environments. |
| `--skip-ideation` | Optional | Skip the ideation phase if the user is confident the prompt is clear. |

---

## smartspec_generate_tasks

**Description:** Convert spec.md (or plan.md) → tasks.md with 100% duplication prevention.

**Version:** 7.0.0

### Universal Flags (Supported)

These flags are supported by this workflow:
`--config`, `--json`, `--lang`, `--out`, `--platform`, `--quiet`

---

## smartspec_generate_tests

**Description:** Generate test artifacts/suggestions (prompts/scripts/reports).

**Version:** 6.1.1

### Universal Flags (Supported)

These flags are supported by this workflow:
`--config`, `--json`, `--lang`, `--out`, `--platform`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_generate_tests \
  specs/<category>/<spec-id>/spec.md \
  [--mode strict] \
  [--plan-format both] \
  [--include-dependencies] \
  [--out .spec/reports/generate-tests/<label>] \
  [--json]
```

**CLI:**
```bash
/smartspec_generate_tests \
  specs/<category>/<spec-id>/spec.md \
  --apply \
  [--target-path specs/<category>/<spec-id>/testplan/tests.md] \
  [--out .spec/reports/generate-tests/<label>] \
  [--json]
```

---

## smartspec_generate_ui_spec

### Usage Examples

**CLI:**
```bash
/smartspec_generate_ui_spec \
  --requirements "Create restaurant booking form with date picker, time selector, guest count, and special requests" \
  --spec specs/feature/spec-001-booking/ui-spec.json
```

**Kilo Code:**
```bash
/smartspec_generate_ui_spec.md \
  --requirements "Create restaurant booking form with date picker, time selector, guest count, and special requests" \
  --spec specs/feature/spec-001-booking/ui-spec.json \
  --platform kilo
```

---

## smartspec_hotfix_assistant

**Description:** Assist in creating and managing hotfixes.

**Version:** 6.1.1

### Universal Flags (Supported)

These flags are supported by this workflow:
`--config`, `--json`, `--lang`, `--out`, `--platform`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_hotfix_assistant \
  --base-tag v1.2.3 \
  --hotfix-version v1.2.4 \
  --commit-sha <sha> \
  --remote origin \
  --main-branch main \
  --verify-summary .spec/reports/verify-tasks-progress/<run-id>/summary.json \
  --deployment-summary .spec/reports/deployment-planner/<run-id>/summary.json \
  --release-notes specs/<category>/<spec-id>/deployment/release_notes.md \
  --test-script test \
  --out .spec/reports/hotfix-assistant \
  --json
```

**CLI:**
```bash
/smartspec_hotfix_assistant \
  --base-tag v1.2.3 \
  --hotfix-version v1.2.4 \
  --commit-sha <sha> \
  --remote origin \
  --main-branch main \
  --allow-network \
  --require-tests-pass \
  --verify-summary .spec/reports/verify-tasks-progress/<run-id>/summary.json \
  --deployment-summary .spec/reports/deployment-planner/<run-id>/summary.json \
  --release-notes specs/<category>/<spec-id>/deployment/release_notes.md \
  --test-script test \
  --apply \
  --out .spec/reports/hotfix-assistant \
  --json
```

---

## smartspec_implement_tasks

**Description:** Implement code changes strictly from tasks.md with 100% duplication prevention and SmartSpec v7 governance.

**Version:** 7.0.0

### Universal Flags (Supported)

These flags are supported by this workflow:
`--config`, `--json`, `--lang`, `--out`, `--platform`, `--quiet`

---

## smartspec_implement_ui_from_spec

### Usage Examples

**CLI:**
```bash
/smartspec_implement_ui_from_spec \
  --spec specs/feature/spec-002-contact/ui-spec.json \
  --target-platform web \
  --renderer lit \
  --output-dir src/ui/contact \
  --apply
```

**Kilo Code:**
```bash
/smartspec_implement_ui_from_spec.md \
  --spec specs/feature/spec-002-contact/ui-spec.json \
  --target-platform web \
  --renderer lit \
  --output-dir src/ui/contact \
  --platform kilo \
  --apply
```

---

## smartspec_incident_response

**Description:** Manage production incidents from triage to resolution and post-mortem.

**Version:** 1.0.0

### Parameters

| Parameter | Status | Description |
|---|---|---|
| `--alert-payload` | Optional | The JSON payload of the alert that triggered the incident. |
| `--help` | Optional | Show help message. |
| `--quiet` | Optional | Suppress all output except errors. |
| `--verbose` | Optional | Enable verbose logging. |
| `--version` | Optional | Show version. |

### Usage Examples

**CLI:**
```bash
/smartspec_incident_response \
  --alert-payload <json-payload>
```

---

## smartspec_manage_ui_catalog

### Usage Examples

**CLI:**
```bash
/smartspec_manage_ui_catalog \
  --action add \
  --component-type slider \
  --component-def slider-component.json \
  --apply
```

**Kilo Code:**
```bash
/smartspec_manage_ui_catalog.md \
  --action add \
  --component-type slider \
  --component-def slider-component.json \
  --platform kilo \
  --apply
```

---

## smartspec_nfr_perf_planner

**Description:** Produce NFR/performance plan from spec (reports).

**Version:** 6.1.1

### Universal Flags (Supported)

These flags are supported by this workflow:
`--config`, `--json`, `--lang`, `--out`, `--platform`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_nfr_perf_planner \
  [--spec-ids <csv>] \
  [--include-dependencies] \
  [--nfr-policy-paths <glob[,glob...]>] \
  [--target-envs <csv>] \
  [--preferred-tools <csv>] \
  [--intensity-level <light|normal|heavy>] \
  [--max-tasks-per-nfr <int>] \
  [--plan-label <string>] \
  [--plan-format <md|json>] \
  [--safety-mode <normal|strict>] \
  [--stdout-summary] \
  [--nosubtasks] \
  [--out <output-root>] \
  [--json]
```

**Kilo Code:**
```bash
/smartspec_nfr_perf_planner.md \
  [--spec-ids <csv>] \
  [--include-dependencies] \
  [--nfr-policy-paths <glob[,glob...]>] \
  [--target-envs <csv>] \
  [--preferred-tools <csv>] \
  [--intensity-level <light|normal|heavy>] \
  [--max-tasks-per-nfr <int>] \
  [--plan-label <string>] \
  [--plan-format <md|json>] \
  [--safety-mode <normal|strict>] \
  [--stdout-summary] \
  [--nosubtasks] \
  [--out <output-root>] \
  [--json] \
  --platform kilo
```

---

## smartspec_nfr_perf_verifier

**Description:** Verify NFR/performance evidence (reports).

**Version:** 6.1.1

### Universal Flags (Supported)

These flags are supported by this workflow:
`--config`, `--json`, `--lang`, `--out`, `--platform`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_nfr_perf_verifier \
  specs/<category>/<spec-id>/spec.md \
  [--evidence-manifest .spec/reports/nfr-evidence/<run-id>/evidence.json] \
  [--target-env prod] \
  [--time-window 30d] \
  [--mode strict] \
  [--report-format both] \
  [--stdout-summary] \
  [--out <output-root>] \
  [--json]
```

**Kilo Code:**
```bash
/smartspec_nfr_perf_verifier.md \
  specs/<category>/<spec-id>/spec.md \
  [--evidence-manifest .spec/reports/nfr-evidence/<run-id>/evidence.json] \
  [--target-env prod] \
  [--time-window 30d] \
  [--mode strict] \
  [--report-format both] \
  [--stdout-summary] \
  [--out <output-root>] \
  [--json] \
  --platform kilo
```

---

## smartspec_observability_configurator

**Description:** Configure observability tools (logging, metrics, tracing).

**Version:** 6.1.1

### Universal Flags (Supported)

These flags are supported by this workflow:
`--config`, `--json`, `--lang`, `--out`, `--platform`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_observability_configurator \
  --spec specs/<category>/<spec-id>/spec.md \
  --obs-platform opentelemetry \
  --out .spec/reports/observability-configurator \
  --json
```

**CLI:**
```bash
/smartspec_observability_configurator \
  --spec specs/<category>/<spec-id>/spec.md \
  --obs-platform opentelemetry \
  --target-dir <path/approved/by/config> \
  --write-runtime-config \
  --apply \
  --out .spec/reports/observability-configurator \
  --json
```

---

## smartspec_optimize_ui_catalog

**Description:** Optimize and cache UI component catalog for faster lookup and improved performance

**Version:** 1.0.0

### Universal Flags (Supported)

These flags are supported by this workflow:
`--apply`, `--config`, `--json`, `--lang`, `--out`, `--platform`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_optimize_ui_catalog \
  --catalog .spec/ui-catalog.json \
  [--apply] \
  [--json]
```

**Kilo Code:**
```bash
/smartspec_optimize_ui_catalog.md \
  --catalog .spec/ui-catalog.json \
  --platform kilo \
  [--apply] \
  [--json]
```

---

## smartspec_performance_profiler

**Version:** 1.0.0

### Universal Flags (Supported)

These flags are supported by this workflow:
`--config`, `--json`, `--lang`, `--out`, `--platform`, `--quiet`

---

## smartspec_production_monitor

**Description:** Monitor production health, generate alerts, and feed metrics back into the SmartSpec ecosystem.

**Version:** 1.0.0

### Parameters

| Parameter | Status | Description |
|---|---|---|
| `--daemon` | Optional | Run continuously as a background process. |
| `--help` | Optional | Show help message. |
| `--quiet` | Optional | Suppress all output except errors. |
| `--run-once` | Optional | Run the monitoring check once and exit. |
| `--spec-id` | Optional | The ID of the spec to monitor. |
| `--verbose` | Optional | Enable verbose logging. |
| `--version` | Optional | Show version. |

### Usage Examples

**CLI:**
```bash
/smartspec_production_monitor \
  --spec-id <spec-id> \
  [--run-once] \
  [--daemon]
```

---

## smartspec_project_copilot

**Description:** Read-only project copilot that summarizes status and routes users to

**Version:** 6.0.7

### Universal Flags (Supported)

These flags are supported by this workflow:
`--json`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_project_copilot "<question>" \
  [--domain <name>] \
  [--spec-id <id>] \
  [--spec-path <path>] \
  [--aspect status|roadmap|security|ci|ui|perf|all] \
  [--report <path>] \
  [--format markdown|plain|json] \
  [--short] \
  [--repos-config <path>] \
  [--workspace-roots <root1,root2,...>] \
  [--registry-roots <dir1,dir2,...>] \
  [--out <safe_reports_root>] \
  [--json]
```

**Kilo Code:**
```bash
/smartspec_project_copilot.md "<question>" --platform kilo \
  [--domain <name>] [--spec-id <id>] [--spec-path <path>] [--aspect ...] \
  [--report <path>] [--format ...] [--short] \
  [--repos-config <path>] [--workspace-roots ...] [--registry-roots ...] \
  [--out <safe_reports_root>] \
  [--json]
```

---

## smartspec_quality_gate

**Description:** Consolidated quality gate (replaces ci_quality_gate + release_readiness).

**Version:** 6.0.0

### Universal Flags (Supported)

These flags are supported by this workflow:
`--apply`, `--json`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_quality_gate \
  --profile <ci|release> \
  [--spec <path/to/spec.md>|--spec-id <id>] \
  [--out <output-root>] \
  [--json] \
  [--strict]
```

**Kilo Code:**
```bash
/smartspec_quality_gate.md \
  --profile <ci|release> \
  [--spec <path/to/spec.md>|--spec-id <id>] \
  [--out <output-root>] \
  [--json] \
  [--strict] \
  --platform kilo
```

---

## smartspec_refactor_planner

**Version:** 1.0.0

### Universal Flags (Supported)

These flags are supported by this workflow:
`--config`, `--json`, `--lang`, `--out`, `--platform`, `--quiet`

---

## smartspec_reindex_specs

**Description:** Rebuild/refresh SPEC_INDEX.json from specs/** (non-destructive; reports

**Version:** 6.0.0

### Universal Flags (Supported)

These flags are supported by this workflow:
`--apply`, `--json`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_reindex_specs [--apply] [--json]
```

**Kilo Code:**
```bash
/smartspec_reindex_specs.md [--apply] [--json] \
  --platform kilo
```

---

## smartspec_reindex_workflows

**Description:** Rebuild/refresh WORKFLOWS_INDEX.yaml from .smartspec/workflows/** (non-destructive;

**Version:** 6.0.0

### Universal Flags (Supported)

These flags are supported by this workflow:
`--apply`, `--json`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_reindex_workflows [--apply] [--json]
```

**Kilo Code:**
```bash
/smartspec_reindex_workflows.md [--apply] [--json] \
  --platform kilo
```

---

## smartspec_release_tagger

**Description:** Manage release tags and versioning.

**Version:** 6.1.1

### Universal Flags (Supported)

These flags are supported by this workflow:
`--config`, `--json`, `--lang`, `--out`, `--platform`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_release_tagger \
  --version v1.2.3 \
  --commit-sha <sha> \
  --spec-id <spec-id> \
  --release-notes specs/<category>/<spec-id>/deployment/release_notes.md \
  --verify-summary .spec/reports/verify-tasks-progress/<run-id>/summary.json \
  --deployment-summary .spec/reports/deployment-planner/<run-id>/summary.json \
  --out .spec/reports/release-tagger \
  --json
```

**CLI:**
```bash
/smartspec_release_tagger \
  --version v1.2.3 \
  --commit-sha <sha> \
  --spec-id <spec-id> \
  --release-notes specs/<category>/<spec-id>/deployment/release_notes.md \
  --verify-summary .spec/reports/verify-tasks-progress/<run-id>/summary.json \
  --deployment-summary .spec/reports/deployment-planner/<run-id>/summary.json \
  --remote origin \
  --provider github \
  --allow-network \
  --apply \
  --out .spec/reports/release-tagger \
  --json
```

---

## smartspec_report_implement_prompter

**Description:** Generate implementation prompt packs with 100% duplication prevention.

**Version:** 7.0.0

### Universal Flags (Supported)

These flags are supported by this workflow:
`--config`, `--json`, `--lang`, `--out`, `--platform`, `--quiet`

### Usage Examples

**CLI:**
```bash
python3 .spec/scripts/validate_prompts.py \
  --prompts .spec/prompts/<spec-id>/<target>/<run-id>/ \
  --registry .spec/registry/ \
  --check-duplicates --threshold 0.8
```

---

## smartspec_rollback

**Description:** Safely roll back a failed deployment to a previous stable version.

**Version:** 1.0.0

### Parameters

| Parameter | Status | Description |
|---|---|---|
| `--auto-approve` | Optional | (Optional) Skip manual approval for high-risk rollbacks. Use with caution. |
| `--failed-deployment-id` | Optional | The ID of the deployment that failed. |
| `--help` | Optional | Show help message. |
| `--quiet` | Optional | Suppress all output except errors. |
| `--target-version` | Optional | (Optional) The specific version to roll back to. Defaults to the last known good version. |
| `--verbose` | Optional | Enable verbose logging. |
| `--version` | Optional | Show version. |

### Usage Examples

**CLI:**
```bash
/smartspec_rollback \
  --failed-deployment-id <id> \
  [--target-version <version>] \
  [--auto-approve]
```

---

## smartspec_security_audit_reporter

**Description:** Generate security audit reports.

**Version:** 6.0.0

### Universal Flags (Supported)

These flags are supported by this workflow:
`--apply`, `--json`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_security_audit_reporter \
  <path/to/spec.md> \
  [--report-format <summary|detailed>] \
  [--verify-summary <path/to/verify-tasks-progress-strict/summary.json>] \
  [--out <output-root>] \
  [--json]
```

**Kilo Code:**
```bash
/smartspec_security_audit_reporter.md \
  specs/<category>/<spec-id>/spec.md \
  [--report-format detailed] \
  [--verify-summary .spec/reports/verify-tasks-progress-strict/<run-id>/summary.json] \
  [--out <output-root>] \
  [--json] \
  --platform kilo
```

---

## smartspec_security_threat_modeler

**Description:** Model security threats and generate mitigation strategies.

**Version:** 6.0.0

### Universal Flags (Supported)

These flags are supported by this workflow:
`--apply`, `--json`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_security_threat_modeler \
  <path/to/spec.md> \
  [--framework <STRIDE|DREAD>] \
  [--apply] \
  [--json]
```

**Kilo Code:**
```bash
/smartspec_security_threat_modeler.md \
  specs/<category>/<spec-id>/spec.md \
  [--framework <STRIDE>] \
  [--apply] \
  [--json] \
  --platform kilo
```

---

## smartspec_sync_tasks_checkboxes

**Description:** Sync checkbox states in tasks.md using a strict verifier summary.json

**Version:** 6.0.0

### Parameters

| Parameter | Status | Description |
|---|---|---|
| `--apply` | Optional | - `--out <path>` (reports root; safe outputs only) |
| `--config` | Optional | (default `.spec/smartspec.config.yaml`) |
| `--json` | Optional | - `--quiet` |
| `--lang` | Optional | - `--platform <cli|kilo|ci|other>` |
| `--manual-policy` | Optional | (default `uncheck`) |
| `--recompute-parents` | Optional | (default `true`) |
| `--report-format` | Optional | (default `both`) |
| `--verify-report` | Required | strict verifier `summary.json` |

### Usage Examples

**CLI:**
```bash
/smartspec_sync_tasks_checkboxes <path/to/tasks.md> \
  --verify-report <path/to/summary.json> \
  [--manual-policy leave|uncheck] \
  [--recompute-parents true|false] \
  [--report-format md|json|both] \
  [--apply] [--json]
```

**Kilo Code:**
```bash
/smartspec_sync_tasks_checkboxes.md <path/to/tasks.md> \
  --platform kilo \
  --verify-report <path/to/summary.json> \
  [--manual-policy leave|uncheck] \
  [--recompute-parents true|false] \
  [--report-format md|json|both] \
  [--apply] [--json]
```

---

## smartspec_test_report_analyzer

**Description:** Analyze test reports and generate insights.

**Version:** 6.0.0

### Universal Flags (Supported)

These flags are supported by this workflow:
`--apply`, `--json`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_test_report_analyzer \
  --test-report .spec/reports/test-suite-runner/<run-id> \
  [--mode <normal|strict>] \
  [--max-log-bytes <int>] \
  [--max-junit-bytes <int>] \
  [--max-test-cases <int>] \
  [--out <output-root>] \
  [--json]
```

**Kilo Code:**
```bash
/smartspec_test_report_analyzer.md \
  --test-report .spec/reports/test-suite-runner/<run-id> \
  --mode normal \
  --out .spec/reports/test-report-analyzer \
  --json \
  --platform kilo
```

---

## smartspec_test_suite_runner

**Description:** Run test suites and generate reports.

**Version:** 6.0.0

### Universal Flags (Supported)

These flags are supported by this workflow:
`--apply`, `--json`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_test_suite_runner \
  --test-script <npm-script-name> \
  [--junit-report-path <relative/path/to/junit.xml>] \
  [--timeout 600] \
  [--allow-network] \
  [--out <output-root>] \
  [--json]
```

**Kilo Code:**
```bash
/smartspec_test_suite_runner.md \
  --test-script test:unit \
  --junit-report-path .spec/reports/test-suite-runner/_tmp/junit.xml \
  --timeout 600 \
  --out .spec/reports/test-suite-runner \
  --json \
  --platform kilo
```

---

## smartspec_ui_accessibility_audit

**Description:** Automated accessibility audit for A2UI implementations against WCAG 2.1 AA standards

**Version:** 1.0.0

### Universal Flags (Supported)

These flags are supported by this workflow:
`--config`, `--json`, `--lang`, `--out`, `--platform`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_ui_accessibility_audit \
  --spec specs/feature/spec-003-profile/ui-spec.json \
  --implementation src/ui/profile/ \
  [--json]
```

**Kilo Code:**
```bash
/smartspec_ui_accessibility_audit.md \
  --spec specs/feature/spec-003-profile/ui-spec.json \
  --implementation src/ui/profile/ \
  --platform kilo \
  [--json]
```

---

## smartspec_ui_agent

### Usage Examples

**CLI:**
```bash
/smartspec_ui_agent \
  --mode interactive \
  --context specs/feature/spec-002-contact
```

**Kilo Code:**
```bash
/smartspec_ui_agent.md \
  --mode interactive \
  --context specs/feature/spec-002-contact \
  --platform kilo
```

---

## smartspec_ui_analytics_reporter

**Description:** Track UI component usage, adoption metrics, and quality indicators across the project

**Version:** 1.0.0

### Universal Flags (Supported)

These flags are supported by this workflow:
`--config`, `--json`, `--lang`, `--out`, `--platform`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_ui_analytics_reporter \
  --catalog .spec/ui-catalog.json \
  --implementation src/ui/ \
  [--json]
```

**Kilo Code:**
```bash
/smartspec_ui_analytics_reporter.md \
  --catalog .spec/ui-catalog.json \
  --implementation src/ui/ \
  --platform kilo \
  [--json]
```

---

## smartspec_ui_component_audit

**Description:** Audit UI components for consistency and best practices.

**Version:** 6.0.0

### Universal Flags (Supported)

These flags are supported by this workflow:
`--apply`, `--json`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_ui_component_audit \
  --source-root <path/to/src> \
  --component-library <mui|antd|chakra|other> \
  --design-tokens <path/to/tokens.json> \
  [--wcag-level <AA|AAA>] \
  [--strict] \
  [--out <output-root>] \
  [--json]
```

**Kilo Code:**
```bash
/smartspec_ui_component_audit.md \
  --source-root <path/to/src> \
  --component-library <mui|antd|chakra|other> \
  --design-tokens <path/to/tokens.json> \
  [--wcag-level <AA|AAA>] \
  [--strict] \
  [--out <output-root>] \
  [--json] \
  --platform kilo
```

---

## smartspec_ui_performance_test

**Description:** Performance testing for UI implementations with metrics and benchmarks

**Version:** 1.0.0

### Universal Flags (Supported)

These flags are supported by this workflow:
`--config`, `--json`, `--lang`, `--out`, `--platform`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_ui_performance_test \
  --spec specs/feature/spec-003-profile/ui-spec.json \
  --implementation src/ui/profile/ \
  [--json]
```

**Kilo Code:**
```bash
/smartspec_ui_performance_test.md \
  --spec specs/feature/spec-003-profile/ui-spec.json \
  --implementation src/ui/profile/ \
  --platform kilo \
  [--json]
```

---

## smartspec_ui_validation

**Description:** UI audit/validation (includes consistency mode).

**Version:** 6.0.0

### Universal Flags (Supported)

These flags are supported by this workflow:
`--apply`, `--json`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_ui_validation \
  --mode <validation|consistency> \
  [--spec <path/to/spec.md>|--spec-id <id>] \
  [--scope <global|spec|ui-registry>] \
  [--out <output-root>] \
  [--json] \
  [--strict]
```

**Kilo Code:**
```bash
/smartspec_ui_validation.md \
  --mode <validation|consistency> \
  [--spec <path/to/spec.md>|--spec-id <id>] \
  [--scope <global|spec|ui-registry>] \
  [--out <output-root>] \
  [--json] \
  [--strict] \
  --platform kilo
```

---

## smartspec_validate_index

**Description:** Validate SPEC_INDEX and WORKFLOWS_INDEX integrity.

**Version:** 6.0.0

### Universal Flags (Supported)

These flags are supported by this workflow:
`--apply`, `--json`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_validate_index \
  [--out <output-root>] \
  [--json] \
  [--strict]
```

**Kilo Code:**
```bash
/smartspec_validate_index.md \
  [--out <output-root>] \
  [--json] \
  [--strict] \
  --platform kilo
```

---

## smartspec_verify_tasks_progress_strict

**Description:** 'Strict evidence-only verification using parseable evidence hooks (evidence:

**Version:** 6.0.0

### Universal Flags (Supported)

These flags are supported by this workflow:
`--json`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_verify_tasks_progress_strict <path/to/tasks.md> [--report-format <md|json|both>] [--json]
```

**Kilo Code:**
```bash
/smartspec_verify_tasks_progress_strict.md <path/to/tasks.md> [--report-format <md|json|both>] [--json] \
  --platform kilo
```

---

## smartspec_verify_ui_implementation

### Usage Examples

**CLI:**
```bash
/smartspec_verify_ui_implementation \
  --spec specs/feature/spec-002-contact/ui-spec.json \
  --implementation src/ui/contact \
  --target-platform web
```

**Kilo Code:**
```bash
/smartspec_verify_ui_implementation.md \
  --spec specs/feature/spec-002-contact/ui-spec.json \
  --implementation src/ui/contact \
  --target-platform web \
  --platform kilo
```

---




---

## Workflow Scenarios Guide

---

## How to Use This Guide

This guide provides **scenario-based recommendations** for using SmartSpec workflows effectively. Each scenario includes:

- **Context:** When to use this approach
- **Recommended workflow(s):** Which workflows to use
- **Parameter combinations:** Specific flags and their purposes
- **Command examples:** Both CLI and Kilo Code
- **Best practices:** Tips for optimal results
- **Common pitfalls:** What to avoid

### Important: Dual-Syntax Requirement

**When answering user questions about workflow usage, ALWAYS provide BOTH syntaxes:**

1. **CLI syntax:** `/workflow_name <args> --flags`
2. **Kilo Code syntax:** `/workflow_name.md <args> --flags --platform kilo`

**Example:**

**CLI:**
```bash
/smartspec_generate_spec --spec specs/feature/spec-001/spec.md --apply
```

**Kilo Code:**
```bash
/smartspec_generate_spec.md --spec specs/feature/spec-001/spec.md --apply --platform kilo
```

**Rules:**
- MUST show both syntaxes for every workflow command recommendation
- Kilo Code MUST include `--platform kilo` flag
- Use code blocks for clarity
- If a scenario below shows only one syntax, generate the other syntax following this pattern

### Important: Directory Structure and Design Principle

**CRITICAL:** SmartSpec follows a strict separation between read-only and read-write directories:

- **`.smartspec/`** = Read-Only (workflows, scripts, knowledge) - ❌ NEVER write here
- **`.spec/`** = Read-Write (reports, specs, registry) - ✅ ALWAYS write reports here

**All workflow outputs MUST go to `.spec/reports/`**, NOT `.smartspec/reports/`.

**Correct:**
```bash
--out .spec/reports/implement-tasks/spec-core-001-auth
```

**Incorrect:**
```bash
--out .smartspec/reports/...  ❌ (violates read-only principle)
```

For detailed explanation, see Section 0.5 in `knowledge_base_smartspec_handbook.md`.

---

## Table of Contents

1. [Starting a New Feature](#1-starting-a-new-feature)
2. [Implementing from Specifications](#2-implementing-from-specifications)
3. [Validating Implementation Progress](#3-validating-implementation-progress)
4. [API Contract Validation](#4-api-contract-validation)
5. [Production Deployment](#5-production-deployment)
6. [Security Auditing](#6-security-auditing)
7. [Performance Optimization](#7-performance-optimization)
8. [Emergency Hotfix](#8-emergency-hotfix)
9. [Documentation Generation](#9-documentation-generation)
10. [CI/CD Integration](#10-cicd-integration)

---

## 1. Starting a New Feature

### Context
You have a feature idea but no formal specification yet.

### Recommended Workflow
`smartspec_generate_spec_from_prompt` → `smartspec_generate_spec`

### Step 1: Generate Draft Spec

**CLI:**
```bash
/smartspec_generate_spec_from_prompt \
  "User authentication system with OAuth2, JWT tokens, and role-based access control" \
  --out .spec/reports/generate-spec-from-prompt \
  --json
```

**Kilo Code:**
```bash
/smartspec_generate_spec_from_prompt.md \
  "User authentication system with OAuth2, JWT tokens, and role-based access control" \
  --out .spec/reports/generate-spec-from-prompt \
  --json \
  --platform kilo
```

**Parameter Explanation:**
- `--out`: Where to save the draft spec (safe output, no `--apply` needed)
- `--json`: Machine-readable output for automation

### Step 2: Human Review and Edit
Manually review and refine the generated draft at:
`.spec/reports/generate-spec-from-prompt/<run-id>/draft_spec.md`

### Step 3: Finalize Spec

**CLI:**
```bash
/smartspec_generate_spec \
  --spec specs/feature/spec-003-auth-system/spec.md \
  --apply
```

**Kilo Code:**
```bash
/smartspec_generate_spec.md \
  --spec specs/feature/spec-003-auth-system/spec.md \
  --apply \
  --platform kilo
```

**Parameter Explanation:**
- `--apply`: Required because spec.md is a governed artifact
- `--spec`: Path to the spec file to refine

### Best Practices
✅ Keep prompts focused and specific  
✅ Include NFRs (performance, security, scalability) in prompt  
✅ Always human-review before finalizing  
✅ Use `--apply` only after review  

### Common Pitfalls
❌ Skipping human review  
❌ Vague prompts leading to unclear specs  
❌ Forgetting to specify NFRs  

---

## 2. Implementing from Specifications

### Context
You have a finalized spec and want to implement it.

### Recommended Workflow
`smartspec_generate_plan` → `smartspec_generate_tasks` → `smartspec_implement_tasks`

### Step 1: Generate Plan

**CLI:**
```bash
/smartspec_generate_plan \
  specs/feature/spec-003-auth-system/spec.md \
  --apply
```

**Parameter Explanation:**
- Positional argument: spec.md path
- `--apply`: Required (plan.md is governed)

### Step 2: Generate Tasks

**CLI:**
```bash
/smartspec_generate_tasks \
  specs/feature/spec-003-auth-system/spec.md \
  --apply
```

**Parameter Explanation:**
- Positional argument: spec.md path
- `--apply`: Required (tasks.md is governed)

### Step 3: Implement (Validation Only First)

**CLI:**
```bash
/smartspec_implement_tasks \
  specs/feature/spec-003-auth-system/tasks.md \
  --validate-only \
  --out .spec/reports/implement-tasks/spec-003 \
  --json
```

**Parameter Explanation:**
- `--validate-only`: Preview changes without writing
- `--out`: Where to save validation report
- `--json`: Structured output

### Step 4: Implement (Actual Changes)

**CLI:**
```bash
/smartspec_implement_tasks \
  specs/feature/spec-003-auth-system/tasks.md \
  --apply \
  --out .spec/reports/implement-tasks/spec-003 \
  --json
```

**Parameter Explanation:**
- `--apply`: Required for actual code changes (governed artifacts)

### Best Practices
✅ Always run `--validate-only` first  
✅ Review change_plan.md before applying  
✅ Use `--allow-network` only when needed (dependency installation)  
✅ Commit after each successful implementation  

### Common Pitfalls
❌ Skipping validation step  
❌ Not reviewing change plan  
❌ Not using `--apply` for actual changes  

---

## 3. Validating Implementation Progress

### Context
You want to check which tasks are actually complete (not just checked off).

### Recommended Workflow
`smartspec_verify_tasks_progress_strict` → `smartspec_sync_tasks_checkboxes`

### Step 1: Strict Verification

**CLI:**
```bash
/smartspec_verify_tasks_progress_strict \
  specs/feature/spec-003-auth-system/tasks.md \
  --out .spec/reports/verify-tasks-progress/spec-003 \
  --json
```

**Kilo Code:**
```bash
/smartspec_verify_tasks_progress_strict.md \
  specs/feature/spec-003-auth-system/tasks.md \
  --out .spec/reports/verify-tasks-progress/spec-003 \
  --json \
  --platform kilo
```

**Parameter Explanation:**
- Positional argument: tasks.md path
- `--out`: Where to save verification report (safe output)
- `--json`: Machine-readable results

### Step 2: Sync Checkboxes

**CLI:**
```bash
/smartspec_sync_tasks_checkboxes \
  specs/feature/spec-003-auth-system/tasks.md \
  --apply
```

**Parameter Explanation:**
- `--apply`: Required (tasks.md is governed)

### Best Practices
✅ Never trust checkboxes alone  
✅ Run strict verification before claiming completion  
✅ Sync checkboxes to reflect actual progress  
✅ Include verification in CI pipeline  

### Common Pitfalls
❌ Manually checking boxes without evidence  
❌ Assuming [x] means done  
❌ Skipping verification before deployment  

---

## 4. API Contract Validation

### Context
You have an OpenAPI spec and want to validate implementation against it.

### Recommended Workflow
`smartspec_api_contract_validator`

### For Development (Warnings OK)

**CLI:**
```bash
/smartspec_api_contract_validator \
  --contract openapi.yaml \
  --implementation-root src/api \
  --spec specs/feature/spec-003-auth-system/spec.md \
  --out .spec/reports/api-contract-validation \
  --json
```

**Parameter Explanation:**
- `--contract`: Path to OpenAPI/GraphQL schema
- `--implementation-root`: Where your API code lives
- `--spec`: Optional, for context
- No `--strict`: Warnings won't fail the check

### For CI/CD (Strict Mode)

**CLI:**
```bash
/smartspec_api_contract_validator \
  --contract openapi.yaml \
  --implementation-root src/api \
  --strict \
  --json
```

**Parameter Explanation:**
- `--strict`: Fail on any MUST requirement violation
- `--json`: Machine-readable for CI parsing

### Best Practices
✅ Use `--strict` in CI/CD  
✅ Use non-strict in development  
✅ Keep contract and spec in sync  
✅ Run validation before merging  

### Common Pitfalls
❌ Using `--strict` too early (blocks development)  
❌ Not running validation in CI  
❌ Contract and implementation drift  

---

## 5. Production Deployment

### Context
You want to plan and execute a production deployment.

### Recommended Workflow
`smartspec_deployment_planner` → `smartspec_release_tagger`

### Step 1: Plan Deployment

**CLI:**
```bash
/smartspec_deployment_planner \
  --environment prod \
  --spec specs/feature/spec-003-auth-system/spec.md \
  --out .spec/reports/deployment-planner \
  --json
```

**Parameter Explanation:**
- `--environment`: Target environment (dev|staging|prod)
- `--spec`: Optional, for context
- `--out`: Where to save deployment plan

### Step 2: Create Release Tag

**CLI:**
```bash
/smartspec_release_tagger \
  --version v1.2.0 \
  --json
```

**Parameter Explanation:**
- `--version`: Semantic version tag (e.g., v1.2.0)
- `--json`: Structured output

### Best Practices
✅ Always plan before deploying  
✅ Use semantic versioning  
✅ Tag releases consistently  
✅ Review deployment plan with team  

### Common Pitfalls
❌ Deploying without a plan  
❌ Inconsistent version numbering  
❌ Skipping staging environment  

---

## 6. Security Auditing

### Context
You want to scan for vulnerabilities and model threats.

### Recommended Workflow
`smartspec_security_audit_reporter` → `smartspec_security_threat_modeler`

### Step 1: Security Audit

**CLI:**
```bash
/smartspec_security_audit_reporter \
  --scope all \
  --out .spec/reports/security-audit \
  --json
```

**Parameter Explanation:**
- `--scope`: What to audit (all|dependencies|code|config)
- `--out`: Where to save audit report

### Step 2: Threat Modeling

**CLI:**
```bash
/smartspec_security_threat_modeler \
  --spec specs/feature/spec-003-auth-system/spec.md \
  --out .spec/reports/security-threat-model \
  --json
```

**Parameter Explanation:**
- `--spec`: Spec to analyze for threats
- `--out`: Where to save threat model

### Best Practices
✅ Run security audit regularly (weekly/monthly)  
✅ Threat model before implementation  
✅ Address high-severity issues immediately  
✅ Include security checks in CI  

### Common Pitfalls
❌ Running security audit only once  
❌ Ignoring dependency vulnerabilities  
❌ Not threat modeling sensitive features  

---

## 7. Performance Optimization

### Context
You want to profile code and plan performance improvements.

### Recommended Workflow
`smartspec_performance_profiler` → `smartspec_refactor_planner`

### Step 1: Profile Performance

**CLI:**
```bash
/smartspec_performance_profiler \
  --target src/api/auth \
  --out .spec/reports/performance-profiler \
  --json
```

**Parameter Explanation:**
- `--target`: Path to code/module to profile
- `--out`: Where to save profiling report

### Step 2: Plan Refactoring

**CLI:**
```bash
/smartspec_refactor_planner \
  --target src/api/auth \
  --out .spec/reports/refactor-planner \
  --json
```

**Parameter Explanation:**
- `--target`: Path to code to analyze
- `--out`: Where to save refactoring plan

### Best Practices
✅ Profile before optimizing  
✅ Focus on bottlenecks identified by profiler  
✅ Plan refactoring before making changes  
✅ Measure performance after changes  

### Common Pitfalls
❌ Premature optimization  
❌ Optimizing without profiling data  
❌ Refactoring without a plan  

---

## 8. Emergency Hotfix

### Context
Production issue requires immediate fix.

### Recommended Workflow
`smartspec_incident_response` → `smartspec_hotfix_assistant` → `smartspec_rollback` (if needed)

### Step 1: Incident Triage

**CLI:**
```bash
/smartspec_incident_response \
  --incident-id INC-2025-001 \
  --mode triage \
  --out .spec/reports/incident-response \
  --json
```

**Parameter Explanation:**
- `--incident-id`: Unique incident identifier
- `--mode`: Operation mode (triage|investigate|postmortem)
- `--out`: Where to save incident report

### Step 2: Hotfix Planning

**CLI:**
```bash
/smartspec_hotfix_assistant \
  --incident-id INC-2025-001 \
  --out .spec/reports/hotfix-assistant \
  --json
```

**Parameter Explanation:**
- `--incident-id`: Link to incident
- `--out`: Where to save hotfix plan

### Step 3: Rollback (If Needed)

**CLI:**
```bash
/smartspec_rollback \
  --environment prod \
  --version v1.1.9 \
  --out .spec/reports/rollback \
  --json
```

**Parameter Explanation:**
- `--environment`: Target environment
- `--version`: Version to roll back to
- `--out`: Where to save rollback plan

### Best Practices
✅ Document incident immediately  
✅ Follow hotfix process  
✅ Test hotfix in staging first (if possible)  
✅ Write post-mortem after resolution  

### Common Pitfalls
❌ Rushing without a plan  
❌ Not documenting the incident  
❌ Skipping post-mortem  

---

## 9. Documentation Generation

### Context
You want to generate and publish technical documentation.

### Recommended Workflow
`smartspec_docs_generator` → `smartspec_docs_publisher`

### Step 1: Generate Documentation

**CLI:**
```bash
/smartspec_docs_generator \
  --mode api-docs \
  --spec specs/feature/spec-003-auth-system/spec.md \
  --out .spec/reports/docs-generator \
  --json
```

**Parameter Explanation:**
- `--mode`: Type of docs (api-docs|user-guide|dev-guide)
- `--spec`: Spec to generate docs from
- `--out`: Where to save generated docs

### Step 2: Publish Documentation

**CLI:**
```bash
/smartspec_docs_publisher \
  --docs-dir .spec/reports/docs-generator/<run-id>/bundle.preview \
  --publish-platform github-pages \
  --version v1.2.0 \
  --allow-network \
  --apply \
  --json
```

**Parameter Explanation:**
- `--docs-dir`: Path to generated documentation
- `--publish-platform`: Where to publish (github-pages|wiki|s3)
- `--version`: Version tag for docs
- `--allow-network`: Required for publishing
- `--apply`: Required for write operations

### Best Practices
✅ Generate docs from specs (single source of truth)  
✅ Version documentation with releases  
✅ Publish to accessible platform  
✅ Keep docs in sync with code  

### Common Pitfalls
❌ Manual documentation (gets outdated)  
❌ Not versioning docs  
❌ Publishing without review  

---

## 10. CI/CD Integration

### Context
You want to integrate SmartSpec workflows into CI/CD pipeline.

### Recommended Workflows
Multiple workflows with `--json` and `--strict` flags

### Quality Gate (CI)

**CLI:**
```bash
/smartspec_quality_gate \
  --strict \
  --out .spec/reports/quality-gate \
  --json
```

**Parameter Explanation:**
- `--strict`: Fail CI on any quality warning
- `--json`: Machine-readable for CI parsing

### Test Suite Runner (CI)

**CLI:**
```bash
/smartspec_test_suite_runner \
  --suite all \
  --out .spec/reports/test-suite-runner \
  --json
```

**Parameter Explanation:**
- `--suite`: Which tests to run (unit|integration|e2e|all)
- `--json`: Structured output for CI

### API Contract Validation (CI)

**CLI:**
```bash
/smartspec_api_contract_validator \
  --contract openapi.yaml \
  --implementation-root src/api \
  --strict \
  --json
```

**Parameter Explanation:**
- `--strict`: Fail CI on contract violations
- `--json`: Machine-readable output

### Best Practices
✅ Use `--json` for all CI workflows  
✅ Use `--strict` for quality gates  
✅ Fail fast on critical issues  
✅ Generate reports for every run  

### Common Pitfalls
❌ Not using `--json` (hard to parse)  
❌ Too lenient quality gates  
❌ Not failing CI on violations  

---

## Universal Flags Reference

These flags are supported by all workflows:

| Flag | Purpose | When to Use |
|---|---|---|
| `--config <path>` | Custom config file | Non-standard project structure |
| `--lang <th\|en>` | Output language | Thai or English output |
| `--platform <cli\|kilo\|ci\|other>` | Platform mode | Kilo Code: use `--platform kilo` |
| `--apply` | Enable writes to governed artifacts | Modifying specs/plans/tasks/indexes |
| `--out <path>` | Output directory | Custom report location |
| `--json` | JSON output | CI/CD, automation, parsing |
| `--quiet` | Suppress non-essential output | CI/CD, scripts |

---

## Parameter Combination Patterns

### Read-Only Workflows (Reports/Analysis)
```bash
workflow_name \
  [inputs] \
  --out <path> \
  --json
```
- No `--apply` needed
- Safe to run anytime

### Governed Artifact Writers (Specs/Plans/Tasks)
```bash
workflow_name \
  [inputs] \
  --apply
```
- `--apply` required
- Preview before applying

##### Runtime Tree Writes (Code/Config)
```bash
workflow_name \
  [inputs] \
  --apply
```
- `--apply` required for governed artifacts
- Some workflows may require additional flags (check workflow docs)
- Always validate firstirst

### Network Operations (Fetch/Push/Publish)
```bash
workflow_name \
  [inputs] \
  --allow-network \
  --apply
```
- `--allow-network` required
- Use only when necessary

### CI/CD Integration
```bash
workflow_name \
  [inputs] \
  --strict \
  --json
```
- `--strict`: Fail on warnings
- `--json`: Machine-readable

---

## Troubleshooting Common Issues

### Issue: "Missing required flag --apply"
**Cause:** Trying to modify governed artifacts without `--apply`  
**Solution:** Add `--apply` flag

### Issue: "Permission denied writing to runtime tree"
**Cause:** Missing required flag or permission  
**Solution:** Check workflow documentation for required flags

### Issue: "Network access denied"
**Cause:** Workflow needs network but `--allow-network` not provided  
**Solution:** Add `--allow-network` flag

### Issue: "Workflow not found"
**Cause:** Using `.md` extension without `--platform kilo`  
**Solution:** Add `--platform kilo` for Kilo Code

### Issue: "Invalid output path"
**Cause:** Output path outside allowed write scopes  
**Solution:** Use path under `.spec/reports/` or `.spec/prompts/`

---

## Best Practices Summary

### General Principles
1. **Evidence-first:** Never claim progress without verification
2. **Preview-first:** Always validate before applying
3. **Config-first:** Use config defaults, minimize flags
4. **Secure-by-default:** No secrets in CLI, use env vars

### Workflow Execution
1. **Read-only first:** Run analysis/validation workflows first
2. **Two-gate writes:** Use `--apply` + specific write flags
3. **Network minimal:** Use `--allow-network` only when needed
4. **Strict in CI:** Use `--strict` for quality gates

### Documentation
1. **Single source:** Generate docs from specs
2. **Version everything:** Tag releases and docs
3. **Keep in sync:** Update docs with code changes

### Security
1. **Audit regularly:** Run security workflows weekly/monthly
2. **Threat model early:** Before implementing sensitive features
3. **Fix high-severity:** Address critical issues immediately

---

**Guide Version:** 6.2.0  
**Last Updated:** December 21, 2025  
**Maintained by:** SmartSpec Team


---

**Version:** 2.0.0  
**Last Updated:** 2025-12-26  
**Consolidated From:**
- PROBLEM_SOLUTION_MATRIX.md
- TROUBLESHOOTING_DECISION_TREE.md
- WORKFLOW_PARAMETERS_REFERENCE.md
- WORKFLOW_SCENARIOS_GUIDE.md
