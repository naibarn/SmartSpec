# Implementation Prompt: Missing Code (TDD Mode)

**Category:** Missing Code  
**Priority:** {{priority}}  
**Generated:** {{timestamp}}  
**Report:** {{report_path}}

---

## Overview

The following tasks have test files but no implementation. This is Test-Driven Development (TDD) mode - implement code to make existing tests pass.

**Tasks in this category:** {{task_count}}

---

{{#each tasks}}
## Task {{task_number}}: {{task_id}} - {{title}}

### Problem
Test file exists but no implementation file found.

### Existing Test
**File:** `{{test_path}}`  
**Status:** ✅ Test file exists  
{{#if test_symbol}}
**Test Function:** `{{test_symbol}}` ✅ (found)
{{/if}}

### Implementation File to Create
**Path:** `{{code_path}}`

{{#if code_symbol}}
**Required Symbol:** `{{code_symbol}}`
{{/if}}

{{#if code_contains}}
**Required Content:** `{{code_contains}}`
{{/if}}

### TDD Approach

**Step 1: Review Existing Tests**

Read the test file to understand requirements:
```bash
cat {{test_path}}
```

**Step 2: Identify Test Expectations**

From the tests, determine:
- What classes/functions are needed
- What methods/parameters are expected
- What behavior is tested
- What return values are expected

**Step 3: Create Minimal Implementation**

Start with minimal code to make tests pass:

```python
{{#if code_symbol}}
class {{code_symbol}}:
    """{{title}}
    
    Implementation based on test requirements in {{test_path}}
    """
    
    def __init__(self):
        """Initialize {{code_symbol}}"""
        # TODO: Add initialization based on test setup
        pass
    
    # TODO: Add methods based on test expectations
{{else}}
# TODO: Implement based on test requirements
{{/if}}
```

**Step 4: Run Tests (Red Phase)**

```bash
pytest {{test_path}} -v
```

Expected: Tests fail (no implementation yet)

**Step 5: Implement (Green Phase)**

Add implementation to make tests pass:
1. Implement required methods
2. Return expected values
3. Handle test cases

**Step 6: Run Tests Again**

```bash
pytest {{test_path}} -v
```

Expected: Tests pass ✅

**Step 7: Refactor (Refactor Phase)**

Improve code quality:
- Add error handling
- Optimize performance
- Add documentation
- Follow best practices

### Implementation Template

Based on common test patterns:

```python
"""{{title}}

Implementation module for {{code_symbol}}.
Tests are defined in {{test_path}}.
"""

{{#if code_symbol}}
class {{code_symbol}}:
    """{{title}}"""
    
    def __init__(self, *args, **kwargs):
        """Initialize {{code_symbol}}
        
        Args:
            *args: Positional arguments
            **kwargs: Keyword arguments
        """
        # TODO: Initialize based on test setup
        pass
    
    def __str__(self):
        """String representation"""
        return f"{{code_symbol}}()"
    
    def __repr__(self):
        """Developer representation"""
        return self.__str__()
    
    # TODO: Add methods based on test calls
{{else}}
def main():
    """Main function for {{title}}"""
    # TODO: Implement based on tests
    pass
{{/if}}
```

### Implementation Steps

1. **Create implementation file:**
   ```bash
   touch {{code_path}}
   ```

2. **Review tests thoroughly:**
   ```bash
   cat {{test_path}}
   # Note: Classes, methods, parameters, return values
   ```

3. **Add minimal implementation:**
   - Define required classes/functions
   - Add method signatures
   - Return dummy values

4. **Run tests (should fail):**
   ```bash
   pytest {{test_path}} -v
   ```

5. **Implement functionality:**
   - Make tests pass one by one
   - Follow test expectations exactly

6. **Run tests (should pass):**
   ```bash
   pytest {{test_path}} -v
   ```

7. **Refactor and improve:**
   - Add docstrings
   - Add error handling
   - Optimize code

8. **Final test run:**
   ```bash
   pytest {{test_path}} -v --cov={{code_module}}
   ```

### Suggestions from Report

{{#each suggestions}}
- {{this}}
{{/each}}

### Verification

After implementation, verify with:
```bash
# Run tests
pytest {{test_path}} -v

# Verify task
/smartspec_verify_tasks_progress_strict {{tasks_path}} --json
```

**Expected result:** `{{task_id}}` verified ✅

---

{{/each}}

## Summary

**Total tasks:** {{task_count}}  
**Priority:** {{priority}}  
**Category:** Missing Code (TDD Mode)

### TDD Workflow

```
1. Read Tests → Understand requirements
2. Create File → Minimal structure
3. Run Tests → See failures (Red)
4. Implement → Make tests pass (Green)
5. Refactor → Improve code quality
6. Verify → Confirm all pass
```

### Implementation Checklist

- [ ] Review all test files
- [ ] Understand test expectations
- [ ] Create implementation files
- [ ] Add minimal code (Red phase)
- [ ] Implement functionality (Green phase)
- [ ] Refactor and improve
- [ ] Verify all tests pass

### Verification Command

```bash
# Run all tests
pytest {{test_dir}} -v

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
**Template:** missing_code_template.md  
**Date:** {{timestamp}}
