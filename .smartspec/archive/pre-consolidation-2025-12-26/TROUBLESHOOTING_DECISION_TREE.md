# Troubleshooting Decision Tree

**Version:** 1.0.0  
**Date:** 2025-12-26  
**Purpose:** Interactive guide to find the right workflow for your problem

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
