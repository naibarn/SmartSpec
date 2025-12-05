# Kilo Code Sub-Task Mode Guide

## Overview

The `--kilocode` parameter enables **Kilo Code's automatic sub-task breakdown** for complex tasks. SmartSpec determines complexity based on **estimated hours** in your tasks.md file, and delegates large tasks (≥2 hours) to Kilo Code's built-in sub-task system.

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

SmartSpec uses **estimated hours** from your tasks.md to determine complexity:

**Task Definition Example:**
```markdown
- [ ] T005: Set Up BullMQ 5.x for Background Job Processing (2h)
- [ ] T001: Add user ID field to User model (0.5h)
```

**Without `--kilocode`:**
```
Both tasks implemented directly (may fail for large tasks)
```

**With `--kilocode`:**
```
T005 (2h >= 2) → COMPLEX → Sub-task mode
T001 (0.5h < 2) → SIMPLE → Direct implementation
```

---

## Key Concept

**Complexity is based on estimated hours, not lines of code.**

### SIMPLE Tasks (< 2 hours)
- Implemented directly
- No sub-task overhead
- Fast execution

**Example:**
```markdown
- [ ] T001: Add user ID field to User model (0.5h)
```
→ Direct implementation

### COMPLEX Tasks (≥ 2 hours)
- Delegated to Kilo Code sub-task mode
- Automatic breakdown
- Avoids `line_count` errors

**Example:**
```markdown
- [ ] T005: Set Up BullMQ 5.x for Background Job Processing (2h)
```
→ Sub-task mode

---

## Usage

### Basic Usage

```bash
/smartspec_implement_tasks specs/feature/spec-004/tasks.md --tasks T005 --kilocode
```

### With Other Flags

```bash
# Implement phase 4 with kilocode mode
/smartspec_implement_tasks specs/feature/spec-004/tasks.md --phase 4 --kilocode

# Skip completed tasks and use kilocode mode
/smartspec_implement_tasks specs/feature/spec-004/tasks.md --skip-completed --kilocode

# Implement specific task range with kilocode mode
/smartspec_implement_tasks specs/feature/spec-004/tasks.md --tasks T005-T010 --kilocode
```

---

## Example: T005 Set Up BullMQ (2h)

### Scenario

**Task Definition:**
```markdown
- [ ] T005: Set Up BullMQ 5.x for Background Job Processing (2h)
```

**Requirements:**
- Install BullMQ dependencies
- Create queue configuration
- Implement job processor
- Add error handling
- Add logging

**Estimated:** 2 hours

---

### Without `--kilocode` (May Fail)

```bash
/smartspec_implement_tasks tasks.md --tasks T005
```

**What SmartSpec sends to Kilo:**
```
T005 Goal: Set Up BullMQ 5.x for Background Job Processing
```

**What happens:**
- Kilo tries to implement entire task in one go
- Creates multiple files, 100+ lines total
- Hits `line_count` limitation
- Error: "required parameter 'line_count' was missing..."
- Retry loop
- Manual intervention needed ❌

---

### With `--kilocode` (Success!)

```bash
/smartspec_implement_tasks tasks.md --tasks T005 --kilocode
```

**What SmartSpec does:**

1. **Reads task hours:**
   ```
   T005: Set Up BullMQ 5.x for Background Job Processing (2h)
   ```
   → Estimated hours: **2h**

2. **Checks complexity:**
   ```
   2h >= 2 → COMPLEX
   ```

3. **Sends to Kilo Code:**
   ```
   Create a new sub-task in code mode:
   T005 Goal: Set Up BullMQ 5.x for Background Job Processing
   ```

4. **Kilo Code automatically breaks down:**
   - Sub-task 1: Install BullMQ dependencies (package.json) - 15 lines
   - Sub-task 2: Create queue configuration (queue.config.ts) - 30 lines
   - Sub-task 3: Implement job processor (job.processor.ts) - 40 lines
   - Sub-task 4: Add error handling - 20 lines
   - Sub-task 5: Add logging - 15 lines

5. **Kilo executes sub-tasks sequentially:**
   - Sub-task 1: ✅ Complete
   - Sub-task 2: ✅ Complete
   - Sub-task 3: ✅ Complete
   - Sub-task 4: ✅ Complete
   - Sub-task 5: ✅ Complete

6. **Result:**
   - Total: 120 lines implemented
   - No `line_count` errors!
   - Task T005 completed ✅

---

## Complexity Detection

### SIMPLE Tasks (< 2 hours)

**Criteria:**
- Estimated hours < 2

**Action:**
- Implement directly (no sub-task mode)

**Examples:**
```markdown
- [ ] T001: Add user ID field to User model (0.5h)
- [ ] T002: Update validation rules (1h)
- [ ] T003: Fix typo in error message (0.25h)
```

**What SmartSpec sends:**
```
T001 Goal: Add user ID field to User model
```
→ Direct implementation

---

### COMPLEX Tasks (≥ 2 hours)

**Criteria:**
- Estimated hours >= 2

**Action:**
- Use Kilo Code sub-task mode
- Prefix with `Create a new sub-task in code mode:`

**Examples:**
```markdown
- [ ] T005: Set Up BullMQ 5.x for Background Job Processing (2h)
- [ ] T010: Implement credit transaction service (4h)
- [ ] T015: Create user authentication system (6h)
```

**What SmartSpec sends:**
```
Create a new sub-task in code mode:
T005 Goal: Set Up BullMQ 5.x for Background Job Processing
```
→ Kilo Code handles breakdown automatically

---

## When to Use `--kilocode`

### ✅ Use `--kilocode` when:

1. **Your tasks have varying complexity:**
   - Some tasks are 0.5h (simple)
   - Some tasks are 4h+ (complex)
   - Want automatic handling

2. **Experiencing Kilo Code errors:**
   - `line_count` errors
   - Retry loops
   - Truncation issues

3. **Working with large features:**
   - Multi-file implementations
   - Complex integrations
   - System setup tasks

4. **Want automatic optimization:**
   - Don't want to manually split tasks
   - Trust Kilo Code's AI to break down optimally
   - Focus on planning, not execution details

---

### ❌ Don't use `--kilocode` when:

1. **All tasks are small:**
   - All tasks < 2 hours
   - No benefit from sub-task mode

2. **Using different AI agent:**
   - Claude (no `line_count` limitation)
   - Cursor (IDE integration)
   - Roo Cline (VSCode extension)

3. **Tasks are already broken down:**
   - Each task is already granular
   - No need for further breakdown

---

## How Kilo Code Breaks Down Tasks

**When Kilo Code receives:**
```
Create a new sub-task in code mode:
T005 Goal: Set Up BullMQ 5.x for Background Job Processing
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

## Comparison

| Feature | Without `--kilocode` | With `--kilocode` |
|---------|---------------------|-------------------|
| **Complexity detection** | None | Hours-based |
| **Task execution** | Direct | Sub-task mode (if ≥2h) |
| **Error rate** | High (for large tasks) | Low |
| **Sub-tasks** | None | Automatic (by Kilo) |
| **Kilo limitations** | Hit often | Avoided |
| **Success rate** | 60-70% | 90-95% |
| **Manual work** | High (fix errors) | Low (automatic) |

---

## Best Practices

### 1. ✅ Estimate hours accurately in tasks.md

```markdown
- [ ] T001: Add field (0.5h)          ← SIMPLE
- [ ] T005: Set up BullMQ (2h)        ← COMPLEX
- [ ] T010: Build auth system (6h)    ← COMPLEX
```

**Why:**
- Accurate hours → Correct complexity detection
- Better sub-task breakdown
- More predictable results

---

### 2. ✅ Use with `--skip-completed`

```bash
/smartspec_implement_tasks tasks.md --skip-completed --kilocode
```

**Why:**
- Skip already completed tasks
- Only process pending tasks
- Avoid re-implementation

---

### 3. ✅ Use for specific phases

```bash
/smartspec_implement_tasks tasks.md --phase 4 --kilocode
```

**Why:**
- Focus on complex phases
- Phase 4-6 usually have large tasks (2h+)
- Better control

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

### Issue 1: Task should be COMPLEX but treated as SIMPLE

**Possible causes:**
- Hours not specified in tasks.md
- Hours < 2 but task is actually complex

**Solutions:**
1. Update estimated hours in tasks.md:
   ```markdown
   - [ ] T005: Set Up BullMQ (2h)  ← Add hours
   ```
2. Or manually split task into smaller tasks

---

### Issue 2: Still Getting `line_count` Errors

**Possible causes:**
- Sub-task still too large (Kilo's breakdown not optimal)
- Kilo Code API issues
- Network problems

**Solutions:**
1. Check sub-task size in Kilo UI
2. Increase estimated hours (forces sub-task mode)
3. Manually create smaller sub-task
4. Use different AI agent temporarily

---

### Issue 3: Too Many Sub-Tasks Created

**Possible causes:**
- Task complexity overestimated by Kilo
- Kilo being overly cautious

**Solutions:**
1. This is actually OK! Better safe than error
2. Sub-tasks execute quickly
3. Total time may be similar

---

### Issue 4: Hours not parsed correctly

**Possible causes:**
- Hours format incorrect
- Missing parentheses

**Solutions:**
1. Use correct format: `(2h)` or `(0.5h)`
2. Examples:
   ```markdown
   ✅ - [ ] T005: Set Up BullMQ (2h)
   ✅ - [ ] T001: Add field (0.5h)
   ❌ - [ ] T005: Set Up BullMQ 2h
   ❌ - [ ] T005: Set Up BullMQ (2 hours)
   ```

---

## Technical Details

### What SmartSpec Does

**Phase 1: Parse Task Hours**
```
FOR each task in selected tasks:
  1. Read task definition
  2. Extract hours from pattern: (Xh)
  3. Parse hours as number
  
  Example:
    "T005: Set Up BullMQ (2h)" → hours = 2
    "T001: Add field (0.5h)" → hours = 0.5
```

**Phase 2: Determine Complexity**
```
IF hours >= 2:
  complexity = COMPLEX
ELSE:
  complexity = SIMPLE
```

**Phase 3: Execute Task**
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

### Hours Parsing Examples

| Task Definition | Parsed Hours | Complexity |
|----------------|--------------|------------|
| `T001: Add field (0.5h)` | 0.5 | SIMPLE |
| `T002: Update validation (1h)` | 1 | SIMPLE |
| `T003: Fix bug (1.5h)` | 1.5 | SIMPLE |
| `T005: Set up BullMQ (2h)` | 2 | COMPLEX |
| `T010: Build service (4h)` | 4 | COMPLEX |
| `T015: Create auth (6h)` | 6 | COMPLEX |

**Threshold:** 2 hours

---

## Summary

### Key Benefits

1. ✅ **Hours-based complexity detection**
   - Uses your existing task estimates
   - No manual analysis needed
   - Accurate and predictable

2. ✅ **Automatic breakdown by Kilo Code**
   - No manual task splitting
   - Kilo's AI optimizes breakdown
   - You just add `--kilocode` flag

3. ✅ **Higher success rate**
   - 90-95% vs 60-70%
   - Fewer manual interventions
   - Faster overall completion

4. ✅ **Avoids Kilo Code limitations**
   - No `line_count` errors
   - No retry loops
   - No truncation issues

---

### How It Works (Simple Explanation)

**Without `--kilocode`:**
```
T005 (2h) → Kilo Code: "Do T005"
Kilo Code: *tries to do everything* → ERROR (too large)
```

**With `--kilocode`:**
```
T005 (2h >= 2) → COMPLEX

SmartSpec → Kilo Code: "Create sub-task: Do T005"
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
/smartspec_implement_tasks tasks.md --tasks T005 --kilocode

# With skip-completed
/smartspec_implement_tasks tasks.md --skip-completed --kilocode

# For specific phase
/smartspec_implement_tasks tasks.md --phase 4 --kilocode

# For task range
/smartspec_implement_tasks tasks.md --tasks T005-T010 --kilocode
```

**Remember:** Complexity is based on **estimated hours** (≥2h = COMPLEX), not lines of code!

---

**Use `--kilocode` to let Kilo Code automatically break down complex tasks (≥2h) and avoid `line_count` errors!** 🚀
