# Problem-Solution Matrix

**Version:** 1.0.0  
**Date:** 2025-12-26  
**Purpose:** Quick reference for problem → workflow → command mapping

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
