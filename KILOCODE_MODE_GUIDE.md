# Kilo Code Sub-Task Mode Guide

## Overview

The `--kilocode` parameter enables automatic sub-task breakdown when using Kilo Code to implement SmartSpec tasks. This helps avoid Kilo Code's `line_count` limitation and error loops.

---

## Problem

**Kilo Code has a limitation:**
- `write_to_file` requires `line_count` parameter
- Files >25 lines often cause errors
- Error: "required parameter 'line_count' was missing or truncated"

**Result:**
- Implementation fails
- Retry loops
- Manual intervention required

---

## Solution: `--kilocode` Flag

### How It Works

When you use `--kilocode` flag:

1. **SmartSpec analyzes each task:**
   - Estimates lines of code needed
   - Counts methods/functions
   - Identifies logical components

2. **If task is COMPLEX (>50 lines OR >2 methods):**
   - Automatically creates Kilo Code sub-tasks
   - Each sub-task targets <50 lines
   - Sub-tasks execute sequentially

3. **If task is SIMPLE (≤50 lines AND ≤2 methods):**
   - Implements directly
   - No sub-task overhead

---

## Usage

### Basic Usage

```bash
/smartspec_implement_tasks specs/feature/spec-004/tasks.md --tasks T033 --kilocode
```

### With Other Flags

```bash
# Implement phase 4 with kilocode mode
/smartspec_implement_tasks specs/feature/spec-004/tasks.md --phase 4 --kilocode

# Skip completed tasks and use kilocode mode
/smartspec_implement_tasks specs/feature/spec-004/tasks.md --skip-completed --kilocode

# Implement specific task range with kilocode mode
/smartspec_implement_tasks specs/feature/spec-004/tasks.md --tasks T033-T040 --kilocode
```

---

## Example: T033 Credit Transaction Service

### Without `--kilocode` (May Fail)

```bash
/smartspec_implement_tasks tasks.md --tasks T033
```

**What happens:**
- Kilo tries to create `transaction.service.ts` (100+ lines)
- Hits `line_count` limitation
- Error: "required parameter 'line_count' was missing..."
- Retry loop

---

### With `--kilocode` (Success!)

```bash
/smartspec_implement_tasks tasks.md --tasks T033 --kilocode
```

**What happens:**

1. **SmartSpec analyzes T033:**
   - Estimated: 120 lines
   - Methods: 5 methods
   - Complexity: COMPLEX

2. **SmartSpec creates sub-tasks:**
   ```
   Create a new sub-task in code mode:
   Goal: Create transaction.service.ts skeleton with imports, class definition, and constructor
   
   Create a new sub-task in code mode:
   Goal: Implement createTransaction() method with validation and database insert
   
   Create a new sub-task in code mode:
   Goal: Implement getTransactionHistory() method with query building and execution
   
   Create a new sub-task in code mode:
   Goal: Add error handling with try-catch blocks and error logging to all methods
   ```

3. **Kilo executes sub-tasks:**
   - Sub-task 1: Creates skeleton (20 lines) ✅
   - Sub-task 2: Adds createTransaction() (30 lines) ✅
   - Sub-task 3: Adds getTransactionHistory() (30 lines) ✅
   - Sub-task 4: Adds error handling (20 lines) ✅

4. **Result:**
   - Total: 100 lines implemented
   - No errors!
   - Task T033 completed ✅

---

## Sub-Task Breakdown Strategy

### Complexity Threshold

| Metric | SIMPLE | COMPLEX |
|--------|--------|---------|
| **Lines of code** | ≤50 | >50 |
| **Methods** | ≤2 | >2 |
| **Action** | Direct implementation | Create sub-tasks |

### Sub-Task Size Guidelines

Each sub-task should:
- Target <50 lines of code
- Implement 1-2 methods max
- Be sequential (not parallel)
- Have clear, focused goal

### Example Breakdown Patterns

#### Pattern 1: Service Implementation
```
Sub-task 1: Create skeleton (imports, class, constructor)
Sub-task 2: Implement method 1
Sub-task 3: Implement method 2
Sub-task 4: Add error handling
Sub-task 5: Add logging
```

#### Pattern 2: Controller Implementation
```
Sub-task 1: Create skeleton (imports, class, dependencies)
Sub-task 2: Implement GET endpoint
Sub-task 3: Implement POST endpoint
Sub-task 4: Add validation middleware
Sub-task 5: Add error handling
```

#### Pattern 3: Model Implementation
```
Sub-task 1: Create schema definition
Sub-task 2: Add validation rules
Sub-task 3: Add instance methods
Sub-task 4: Add static methods
```

---

## When to Use `--kilocode`

### ✅ Use `--kilocode` when:

1. **Implementing large services/controllers:**
   - Expected >50 lines
   - Multiple methods

2. **Experiencing Kilo Code errors:**
   - `line_count` errors
   - Retry loops
   - Truncation issues

3. **Complex tasks:**
   - Multiple logical components
   - Need staged implementation

4. **Want automatic breakdown:**
   - Don't want to manually split tasks
   - Trust SmartSpec's analysis

---

### ❌ Don't use `--kilocode` when:

1. **Tasks are already small:**
   - <50 lines
   - 1-2 methods only

2. **Using different AI agent:**
   - Claude (no line_count limitation)
   - Cursor (IDE integration)
   - Roo Cline (VSCode extension)

3. **Tasks are simple:**
   - Configuration files
   - Small utilities
   - Type definitions

---

## Comparison

| Feature | Without `--kilocode` | With `--kilocode` |
|---------|---------------------|-------------------|
| **Task size** | Any size | Auto-split if >50 lines |
| **Error rate** | High (for large tasks) | Low |
| **Sub-tasks** | Manual | Automatic |
| **Kilo limitations** | Hit often | Avoided |
| **Speed** | Fast (if no errors) | Slightly slower |
| **Success rate** | 60-70% | 90-95% |

---

## Best Practices

### 1. ✅ Use with `--skip-completed`

```bash
/smartspec_implement_tasks tasks.md --skip-completed --kilocode
```

**Why:**
- Skip already completed tasks
- Only process pending tasks
- Avoid re-implementation

---

### 2. ✅ Use for specific phases

```bash
/smartspec_implement_tasks tasks.md --phase 4 --kilocode
```

**Why:**
- Focus on complex phases
- Phase 4-6 usually have large services
- Better control

---

### 3. ✅ Combine with task range

```bash
/smartspec_implement_tasks tasks.md --tasks T033-T040 --kilocode
```

**Why:**
- Target specific complex tasks
- Leave simple tasks for direct implementation

---

### 4. ✅ Monitor sub-task execution

**Watch for:**
- Sub-task creation messages
- Sub-task completion status
- Any sub-task failures

**If sub-task fails:**
- Kilo will retry
- Or break down further
- Or report error

---

## Troubleshooting

### Issue 1: Still Getting Errors

**Possible causes:**
- Sub-task still too large
- Kilo Code API issues
- Network problems

**Solutions:**
1. Check sub-task size in Kilo UI
2. Manually break down further
3. Use different AI agent

---

### Issue 2: Too Many Sub-Tasks

**Possible causes:**
- Task complexity overestimated
- Sub-tasks too granular

**Solutions:**
1. Review task description
2. Simplify task if possible
3. Adjust complexity threshold (manual)

---

### Issue 3: Sub-Tasks Not Created

**Possible causes:**
- Task is SIMPLE (≤50 lines)
- `--kilocode` flag not parsed
- Workflow not updated

**Solutions:**
1. Check task size estimate
2. Verify flag syntax
3. Update SmartSpec repository

---

## Summary

### Key Benefits

1. ✅ **Avoid Kilo Code limitations**
   - No `line_count` errors
   - No retry loops

2. ✅ **Automatic breakdown**
   - No manual task splitting
   - Smart complexity analysis

3. ✅ **Higher success rate**
   - 90-95% vs 60-70%
   - Fewer manual interventions

4. ✅ **Better error handling**
   - Isolated failures
   - Easier debugging

---

### Quick Reference

```bash
# Basic usage
/smartspec_implement_tasks tasks.md --tasks T033 --kilocode

# With skip-completed
/smartspec_implement_tasks tasks.md --skip-completed --kilocode

# For specific phase
/smartspec_implement_tasks tasks.md --phase 4 --kilocode

# For task range
/smartspec_implement_tasks tasks.md --tasks T033-T040 --kilocode
```

---

**Use `--kilocode` to avoid Kilo Code limitations and increase implementation success rate!** 🚀
