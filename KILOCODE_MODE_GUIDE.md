# Kilo Code Sub-Task Mode Guide

## Overview

The `--kilocode` parameter enables **Kilo Code's automatic sub-task breakdown** when implementing SmartSpec tasks. This helps avoid Kilo Code's `line_count` limitation and error loops by delegating complex tasks to Kilo Code's built-in sub-task system.

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

When you use the `--kilocode` flag, SmartSpec changes how it sends tasks to Kilo Code:

**Without `--kilocode` (Direct Implementation):**
```
T033 Goal: Implement credit transaction service
```
→ Kilo tries to implement entire task in one go  
→ May hit `line_count` error if >25 lines

**With `--kilocode` (Sub-Task Mode):**
```
Create a new sub-task in code mode:
T033 Goal: Implement credit transaction service with createTransaction() and getTransactionHistory() methods
```
→ **Kilo Code automatically detects complexity**  
→ **Kilo Code breaks down into smaller sub-tasks**  
→ Each sub-task <50 lines → No `line_count` errors!

---

## Key Concept

**You DON'T manually specify sub-tasks.**

SmartSpec simply:
1. Analyzes if task is COMPLEX (>50 lines OR >2 methods OR multiple files)
2. If COMPLEX: Prefixes task with `Create a new sub-task in code mode:`
3. **Kilo Code does the rest automatically**

**Kilo Code's AI will:**
- Detect task complexity
- Break down into logical sub-tasks
- Execute sub-tasks sequentially
- Each sub-task <50 lines

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

### Scenario

**Task:** T033 - Implement credit transaction service  
**Requirements:**
- Create `transaction.service.ts`
- Implement `createTransaction()` method
- Implement `getTransactionHistory()` method
- Add error handling
- Add logging

**Estimated:** 120 lines, 5 methods

---

### Without `--kilocode` (May Fail)

```bash
/smartspec_implement_tasks tasks.md --tasks T033
```

**What SmartSpec sends to Kilo:**
```
T033 Goal: Implement credit transaction service
```

**What happens:**
- Kilo tries to create entire `transaction.service.ts` (120 lines)
- Hits `line_count` limitation
- Error: "required parameter 'line_count' was missing..."
- Retry loop
- Manual intervention needed ❌

---

### With `--kilocode` (Success!)

```bash
/smartspec_implement_tasks tasks.md --tasks T033 --kilocode
```

**What SmartSpec does:**

1. **Analyzes T033:**
   - Estimated: 120 lines
   - Methods: 5 methods
   - Complexity: **COMPLEX**

2. **Sends to Kilo Code:**
   ```
   Create a new sub-task in code mode:
   T033 Goal: Implement credit transaction service with createTransaction() and getTransactionHistory() methods
   ```

3. **Kilo Code automatically breaks down:**
   - Sub-task 1: Create skeleton (imports, class, constructor) - 20 lines
   - Sub-task 2: Implement createTransaction() - 30 lines
   - Sub-task 3: Implement getTransactionHistory() - 30 lines
   - Sub-task 4: Add error handling - 20 lines
   - Sub-task 5: Add logging - 20 lines

4. **Kilo executes sub-tasks sequentially:**
   - Sub-task 1: ✅ Complete
   - Sub-task 2: ✅ Complete
   - Sub-task 3: ✅ Complete
   - Sub-task 4: ✅ Complete
   - Sub-task 5: ✅ Complete

5. **Result:**
   - Total: 120 lines implemented
   - No `line_count` errors!
   - Task T033 completed ✅

---

## Complexity Detection

SmartSpec classifies tasks as **SIMPLE** or **COMPLEX**:

### SIMPLE Tasks (Direct Implementation)

**Criteria:**
- ≤50 lines of code
- ≤2 methods
- Single file modification

**Action:**
- Implement directly (no sub-task mode)

**Example:**
```
T001 Goal: Add user ID field to User model
```
→ Simple addition, ~10 lines → Direct implementation

---

### COMPLEX Tasks (Sub-Task Mode)

**Criteria:**
- >50 lines of code, OR
- >2 methods, OR
- Multiple file modifications

**Action:**
- Use Kilo Code sub-task mode
- Prefix with `Create a new sub-task in code mode:`

**Example:**
```
Create a new sub-task in code mode:
T033 Goal: Implement credit transaction service with createTransaction() and getTransactionHistory() methods
```
→ Complex service, 120 lines, 5 methods → Sub-task mode

---

## When to Use `--kilocode`

### ✅ Use `--kilocode` when:

1. **Implementing large services/controllers:**
   - Expected >50 lines
   - Multiple methods
   - Complex logic

2. **Experiencing Kilo Code errors:**
   - `line_count` errors
   - Retry loops
   - Truncation issues

3. **Complex tasks:**
   - Multiple logical components
   - Need staged implementation
   - Multiple file modifications

4. **Want automatic breakdown:**
   - Don't want to manually split tasks
   - Trust Kilo Code's AI to break down optimally

---

### ❌ Don't use `--kilocode` when:

1. **Tasks are already small:**
   - <50 lines
   - 1-2 methods only
   - Single simple modification

2. **Using different AI agent:**
   - Claude (no `line_count` limitation)
   - Cursor (IDE integration)
   - Roo Cline (VSCode extension)

3. **Tasks are simple:**
   - Configuration files
   - Small utilities
   - Type definitions
   - Documentation updates

---

## How Kilo Code Breaks Down Tasks

**Kilo Code's AI analyzes:**
- Task description
- File size requirements
- Number of methods/functions
- Logical components
- Dependencies

**Kilo Code creates sub-tasks based on:**
- **Skeleton first:** Imports, class definition, constructor
- **One method per sub-task:** Each method in separate sub-task
- **Cross-cutting concerns:** Error handling, logging, validation
- **Size limit:** Each sub-task <50 lines

**Example breakdown patterns:**

### Service Implementation
```
Sub-task 1: Create skeleton (imports, class, constructor)
Sub-task 2: Implement method 1
Sub-task 3: Implement method 2
Sub-task 4: Add error handling
Sub-task 5: Add logging
```

### Controller Implementation
```
Sub-task 1: Create skeleton (imports, class, dependencies)
Sub-task 2: Implement GET endpoint
Sub-task 3: Implement POST endpoint
Sub-task 4: Add validation middleware
Sub-task 5: Add error handling
```

### Model Implementation
```
Sub-task 1: Create schema definition
Sub-task 2: Add validation rules
Sub-task 3: Add instance methods
Sub-task 4: Add static methods
```

---

## Comparison

| Feature | Without `--kilocode` | With `--kilocode` |
|---------|---------------------|-------------------|
| **Task execution** | Direct implementation | Kilo Code sub-task mode |
| **Task size** | Any size | Auto-split if complex |
| **Error rate** | High (for large tasks) | Low |
| **Sub-tasks** | None | Automatic (by Kilo) |
| **Kilo limitations** | Hit often | Avoided |
| **Speed** | Fast (if no errors) | Slightly slower |
| **Success rate** | 60-70% | 90-95% |
| **Manual work** | High (fix errors) | Low (automatic) |

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

### 4. ✅ Monitor sub-task execution in Kilo UI

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

### Issue 1: Still Getting `line_count` Errors

**Possible causes:**
- Sub-task still too large (Kilo's breakdown not optimal)
- Kilo Code API issues
- Network problems

**Solutions:**
1. Check sub-task size in Kilo UI
2. Manually create smaller sub-task
3. Report to Kilo Code team
4. Use different AI agent temporarily

---

### Issue 2: Too Many Sub-Tasks Created

**Possible causes:**
- Task complexity overestimated by Kilo
- Kilo being overly cautious

**Solutions:**
1. This is actually OK! Better safe than error
2. Sub-tasks execute quickly
3. Total time may be similar

---

### Issue 3: Sub-Tasks Not Created

**Possible causes:**
- Task is SIMPLE (≤50 lines, ≤2 methods)
- `--kilocode` flag not recognized
- Workflow not updated

**Solutions:**
1. Check task size estimate (may actually be simple)
2. Verify flag syntax: `--kilocode` (not `--kilo-code`)
3. Update SmartSpec: Run installation script again

---

### Issue 4: Kilo Code Doesn't Recognize Sub-Task Command

**Possible causes:**
- Kilo Code version outdated
- Command syntax changed

**Solutions:**
1. Update Kilo Code to latest version
2. Check Kilo Code documentation
3. Try alternative: Manually split task in tasks.md

---

## Technical Details

### What SmartSpec Does

**Phase 1: Task Analysis**
```
FOR each task in selected tasks:
  1. Read task description
  2. Estimate lines of code
  3. Count methods/functions
  4. Count files to modify
  
  5. IF (lines > 50 OR methods > 2 OR files > 1):
       complexity = COMPLEX
     ELSE:
       complexity = SIMPLE
```

**Phase 2: Task Execution**
```
IF complexity == COMPLEX AND --kilocode flag present:
  Send to Kilo Code:
    "Create a new sub-task in code mode:
     {task_id} Goal: {task_description}"
  
  Kilo Code handles breakdown automatically

ELSE:
  Send to Kilo Code:
    "{task_id} Goal: {task_description}"
  
  Direct implementation
```

---

### What Kilo Code Does

When Kilo Code receives:
```
Create a new sub-task in code mode:
T033 Goal: Implement credit transaction service
```

**Kilo Code's AI:**
1. Analyzes task requirements
2. Estimates total complexity
3. Identifies logical components
4. Creates sub-tasks automatically
5. Executes sub-tasks sequentially
6. Each sub-task <50 lines (avoids `line_count` error)

**You don't control the breakdown** - Kilo Code's AI decides the optimal split.

---

## Summary

### Key Benefits

1. ✅ **Avoid Kilo Code limitations**
   - No `line_count` errors
   - No retry loops
   - No truncation issues

2. ✅ **Automatic breakdown by Kilo Code**
   - No manual task splitting
   - Kilo's AI optimizes breakdown
   - You just add `--kilocode` flag

3. ✅ **Higher success rate**
   - 90-95% vs 60-70%
   - Fewer manual interventions
   - Faster overall completion

4. ✅ **Better error handling**
   - Isolated failures (one sub-task, not entire task)
   - Easier debugging
   - Clear error messages

---

### How It Works (Simple Explanation)

**Without `--kilocode`:**
```
SmartSpec → Kilo Code: "Do T033"
Kilo Code: *tries to do everything* → ERROR (too large)
```

**With `--kilocode`:**
```
SmartSpec → Kilo Code: "Create sub-task: Do T033"
Kilo Code: *analyzes* → "OK, I'll break this into 5 sub-tasks"
Kilo Code: *executes sub-task 1* → ✅
Kilo Code: *executes sub-task 2* → ✅
Kilo Code: *executes sub-task 3* → ✅
Kilo Code: *executes sub-task 4* → ✅
Kilo Code: *executes sub-task 5* → ✅
```

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

**Use `--kilocode` to let Kilo Code automatically break down complex tasks and avoid `line_count` errors!** 🚀
