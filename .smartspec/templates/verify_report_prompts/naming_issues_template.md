# Refactoring Prompt: Naming Issues

**Category:** Naming Issues  
**Priority:** {{priority}}  
**Generated:** {{timestamp}}  
**Report:** {{report_path}}

---

## Overview

The following tasks have files that exist but names don't match evidence. This prompt provides options for resolving naming mismatches.

**Tasks in this category:** {{task_count}}

---

{{#each tasks}}
## Task {{task_number}}: {{task_id}} - {{title}}

### Problem
Files exist but names don't match evidence paths.

### Evidence Expectations

{{#if code_path}}
**Code Evidence:**
- Expected path: `{{code_path}}`
- Status: ❌ Not found at expected path
{{/if}}

{{#if test_path}}
**Test Evidence:**
- Expected path: `{{test_path}}`
- Status: ❌ Not found at expected path
{{/if}}

### Similar Files Found

{{#if similar_files}}
{{#each similar_files}}
- `{{file}}` ({{similarity}}% similar)
{{/each}}
{{else}}
No similar files found by fuzzy matching.
{{/if}}

### Resolution Options

#### Option A: Update Evidence (Recommended)

If the similar file is the correct implementation:

**Action:** Update evidence in `{{tasks_path}}`

{{#if code_path}}
**Code Evidence Change:**
```markdown
# Before
- evidence: code path="{{code_path}}" {{#if code_symbol}}symbol="{{code_symbol}}"{{/if}}

# After (if using {{similar_files.0.file}})
- evidence: code path="{{similar_files.0.file}}" {{#if code_symbol}}symbol="{{code_symbol}}"{{/if}}
```
{{/if}}

{{#if test_path}}
**Test Evidence Change:**
```markdown
# Before
- evidence: test path="{{test_path}}" {{#if test_symbol}}contains="{{test_symbol}}"{{/if}}

# After (if using {{similar_files.0.file}})
- evidence: test path="{{similar_files.0.file}}" {{#if test_symbol}}contains="{{test_symbol}}"{{/if}}
```
{{/if}}

**Steps:**
1. Open `{{tasks_path}}`
2. Find task `{{task_id}}`
3. Update evidence paths
4. Save file
5. Verify again

---

#### Option B: Rename File

If evidence is correct and file name is wrong:

**Action:** Rename file to match evidence

{{#if code_path}}
**Code File Rename:**
```bash
# If similar file is the correct one
mv {{similar_files.0.file}} {{code_path}}
```
{{/if}}

{{#if test_path}}
**Test File Rename:**
```bash
# If similar file is the correct one
mv {{similar_files.0.file}} {{test_path}}
```
{{/if}}

**⚠️ Warning:** Before renaming:
1. Check for imports/references
2. Update import statements
3. Run tests to verify
4. Check for breaking changes

**Steps:**
1. Search for imports: `grep -r "{{similar_files.0.file_name}}" .`
2. Update all import statements
3. Rename file
4. Run tests: `pytest tests/ -v`
5. Verify: `/smartspec_verify_tasks_progress_strict {{tasks_path}}`

---

#### Option C: Create New File

If neither similar file is correct:

**Action:** Create new file at expected path

{{#if code_path}}
**Create Code File:**
```bash
touch {{code_path}}
# Then implement according to task requirements
```
{{/if}}

{{#if test_path}}
**Create Test File:**
```bash
touch {{test_path}}
# Then add tests according to task requirements
```
{{/if}}

### Suggestions from Report

{{#each suggestions}}
- {{this}}
{{/each}}

### Recommended Approach

{{#if similar_files}}
**Recommendation:** Option A (Update Evidence)

Reason: Similar file found with {{similar_files.0.similarity}}% match. Likely the correct implementation with wrong evidence path.
{{else}}
**Recommendation:** Option C (Create New File)

Reason: No similar files found. Likely not implemented yet.
{{/if}}

### Verification

After changes, verify with:
```bash
/smartspec_verify_tasks_progress_strict {{tasks_path}}
```

**Expected result:** `{{task_id}}` verified ✅

---

{{/each}}

## Summary

**Total tasks:** {{task_count}}  
**Priority:** {{priority}}  
**Category:** Naming Issues

### Resolution Strategy

1. **Review similar files** - Check if they're the correct implementation
2. **Choose option** - Update evidence (A), rename file (B), or create new (C)
3. **Apply changes** - Make the chosen changes
4. **Verify** - Run verification to confirm

### Quick Commands

```bash
# Option A: Update evidence
vim {{tasks_path}}

# Option B: Rename file (example)
# mv old_path new_path

# Option C: Create new file (example)
# touch new_path

# Verify all tasks
/smartspec_verify_tasks_progress_strict {{tasks_path}} --json

# Expected: {{task_count}} tasks verified
```

### What's Next?

After fixing naming issues:

1. **Re-run verification** to check if there are other issues
2. **Generate new prompts** for remaining issues
3. **Execute prompts** (batch or manual)

```bash
# Step 1: Verify again
/smartspec_verify_tasks_progress_strict {{tasks_path}} \
  --out .spec/reports/verify-tasks-progress/latest \
  --json

# Step 2: Generate prompts for remaining issues
/smartspec_report_implement_prompter \
  --verify-report .spec/reports/verify-tasks-progress/latest/summary.json \
  --tasks {{tasks_path}} \
  --out .spec/prompts/latest

# Step 3: Check how many prompts generated
cat .spec/prompts/latest/README.md

# Step 4: Execute (choose based on count)
# - If 1-4 tasks: Manual execution (read prompts one by one)
# - If 5+ tasks: Batch execution (recommended)

python3 .smartspec/scripts/execute_prompts_batch.py \
  --prompts-dir .spec/prompts/latest/ \
  --tasks {{tasks_path}} \
  --checkpoint
```

📖 **See:** `.smartspec/AFTER_PROMPT_GENERATION_GUIDE.md` for complete workflow

---

**Generated by:** smartspec_report_implement_prompter v7.1.0  
**Template:** naming_issues_template.md  
**Date:** {{timestamp}}
