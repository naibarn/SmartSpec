# Enhancement Prompt: Content Issues

**Category:** Content Issues  
**Priority:** {{priority}}  
**Generated:** {{timestamp}}  
**Report:** {{report_path}}

---

## Overview

The following tasks have files and symbols but are missing required content (strings, patterns, specific code). This prompt provides instructions for adding missing content.

**Tasks in this category:** {{task_count}}

---

{{#each tasks}}
## Task {{task_number}}: {{task_id}} - {{title}}

### Problem
File and symbol exist but required content is missing.

### File Information
**Path:** `{{file_path}}`  
**Status:** ✅ File exists  
{{#if symbol}}
**Symbol:** `{{symbol}}` ✅ (found)  
{{/if}}
**Missing Content:** `{{missing_content}}`

### Current State
The file `{{file_path}}` exists{{#if symbol}} and contains symbol `{{symbol}}`{{/if}}, but does not contain the required content: `{{missing_content}}`

### Content to Add

{{#if is_string_literal}}
**Type:** String Literal

**Location:** Add to appropriate location in {{#if symbol}}`{{symbol}}`{{else}}file{{/if}}

**Content:**
```python
"{{missing_content}}"
```

**Example Usage:**
```python
{{#if symbol}}
class {{symbol}}:
    # Add as class attribute
    CONTENT = "{{missing_content}}"
    
    # Or in method
    def method(self):
        value = "{{missing_content}}"
{{else}}
# Add at module level
CONTENT = "{{missing_content}}"
{{/if}}
```
{{else if is_regex_pattern}}
**Type:** Regex Pattern

**Pattern to match:** `{{missing_content}}`

**Location:** Add code that matches this pattern

**Example:**
```python
{{#if symbol}}
class {{symbol}}:
    def method(self):
        # Add code that contains the pattern
        {{missing_content}}
{{else}}
# Add code that contains the pattern
{{missing_content}}
{{/if}}
```
{{else}}
**Type:** Code Pattern

**Pattern:** `{{missing_content}}`

**Location:** Add to {{#if symbol}}`{{symbol}}`{{else}}file{{/if}}

**Implementation:**
```python
{{missing_content}}
```
{{/if}}

### Implementation Steps

1. **Open file:**
   ```bash
   vim {{file_path}}
   ```

2. **Locate insertion point:**
   {{#if symbol}}
   - Find `{{symbol}}` definition
   - Determine appropriate location for content
   {{else}}
   - Determine appropriate location in file
   {{/if}}

3. **Add content:**
   - Insert content from template above
   - Ensure proper indentation
   - Follow project conventions

4. **Verify syntax:**
   ```bash
   python3 -m py_compile {{file_path}}
   ```

5. **Test changes:**
   ```bash
   {{#if test_path}}
   pytest {{test_path}} -v
   {{else}}
   # Run relevant tests
   pytest tests/ -k {{task_id_lower}} -v
   {{/if}}
   ```

### Context and Purpose

{{#if content_context}}
**Why this content is needed:**
{{content_context}}
{{else}}
This content is required by the evidence specification in tasks.md. Review the task description for context on why this specific content is needed.
{{/if}}

### Suggestions from Report

{{#each suggestions}}
- {{this}}
{{/each}}

### Alternative: Update Evidence

If similar content exists with different wording:

**Action:** Update evidence in `{{tasks_path}}`

```markdown
# Before
- evidence: code path="{{file_path}}" contains="{{missing_content}}"

# After (if different content exists)
- evidence: code path="{{file_path}}" contains="ActualContentHere"
```

Or use regex for flexible matching:
```markdown
- evidence: code path="{{file_path}}" regex="pattern.*here"
```

### Verification

After adding content, verify with:
```bash
# Check content exists
grep -n "{{missing_content}}" {{file_path}}

# Verify task
/smartspec_verify_tasks_progress_strict {{tasks_path}} --json
```

**Expected result:** `{{task_id}}` verified ✅

---

{{/each}}

## Summary

**Total tasks:** {{task_count}}  
**Priority:** {{priority}}  
**Category:** Content Issues

### Implementation Checklist

- [ ] Review each missing content
- [ ] Understand content purpose
- [ ] Add content to appropriate location
- [ ] Verify syntax
- [ ] Test implementation
- [ ] Verify all tasks

### Verification Command

```bash
# Verify all tasks
/smartspec_verify_tasks_progress_strict {{tasks_path}} --json

# Expected: {{task_count}} tasks verified
```



### What's Next?

After fixing these issues:

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




### What's Next?

After fixing these issues:

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
**Template:** content_issues_template.md  
**Date:** {{timestamp}}
