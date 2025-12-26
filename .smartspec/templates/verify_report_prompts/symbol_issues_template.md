# Enhancement Prompt: Symbol Issues

**Category:** Symbol Issues  
**Priority:** {{priority}}  
**Generated:** {{timestamp}}  
**Report:** {{report_path}}

---

## Overview

The following tasks have files that exist but are missing required symbols (classes, functions, constants). This prompt provides instructions for adding missing symbols.

**Tasks in this category:** {{task_count}}

---

{{#each tasks}}
## Task {{task_number}}: {{task_id}} - {{title}}

### Problem
File exists but required symbol is missing.

### File Information
**Path:** `{{file_path}}`  
**Status:** ✅ File exists  
**Missing Symbol:** `{{missing_symbol}}`

### Current State
The file `{{file_path}}` exists but does not contain the required symbol `{{missing_symbol}}`.

### Symbol to Add

{{#if is_class}}
**Type:** Class

**Template:**
```python
class {{missing_symbol}}:
    """{{title}}
    
    TODO: Add class description
    """
    
    def __init__(self):
        """Initialize {{missing_symbol}}"""
        # TODO: Add initialization
        pass
    
    # TODO: Add methods
```
{{else if is_function}}
**Type:** Function

**Template:**
```python
def {{missing_symbol}}():
    """{{title}}
    
    TODO: Add function description
    
    Returns:
        TODO: Add return type and description
    """
    # TODO: Add implementation
    pass
```
{{else}}
**Type:** Constant/Variable

**Template:**
```python
{{missing_symbol}} = None  # TODO: Set appropriate value
```
{{/if}}

### Implementation Steps

1. **Open file:**
   ```bash
   vim {{file_path}}
   ```

2. **Find appropriate location:**
   - For classes: After imports, before other classes
   - For functions: After imports and classes
   - For constants: At module level, after imports

3. **Add symbol:**
   - Copy template above
   - Replace TODOs with actual implementation
   - Add docstrings
   - Follow project conventions

4. **Add imports (if needed):**
   ```python
   # Add any required imports
   ```

5. **Test changes:**
   ```bash
   # If test file exists
   pytest {{test_path}} -v
   ```

### Suggestions from Report

{{#each suggestions}}
- {{this}}
{{/each}}

### Alternative: Update Evidence

If the symbol exists with a different name:

**Action:** Update evidence in `{{tasks_path}}`

```markdown
# Before
- evidence: code path="{{file_path}}" symbol="{{missing_symbol}}"

# After (if symbol is actually named differently)
- evidence: code path="{{file_path}}" symbol="ActualSymbolName"
```

### Verification

After adding symbol, verify with:
```bash
# Check symbol exists
python3 -c "from {{module_path}} import {{missing_symbol}}; print('✅ Symbol found')"

# Verify task
/smartspec_verify_tasks_progress_strict {{tasks_path}} --json
```

**Expected result:** `{{task_id}}` verified ✅

---

{{/each}}

## Summary

**Total tasks:** {{task_count}}  
**Priority:** {{priority}}  
**Category:** Symbol Issues

### Implementation Checklist

- [ ] Review each missing symbol
- [ ] Determine symbol type (class/function/constant)
- [ ] Add symbol to file
- [ ] Add docstrings
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
**Template:** symbol_issues_template.md  
**Date:** {{timestamp}}
