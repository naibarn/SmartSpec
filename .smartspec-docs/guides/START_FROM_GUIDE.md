# `--start-from` Parameter Guide

## Overview

The `--start-from` parameter allows you to **start implementation from a specific task and continue to the end** of the tasks file. This is useful when you want to resume work from a particular point without manually specifying the end task.

---

## Problem

**Before `--start-from`:**

If you wanted to implement from T033 to the end, you had to:
1. Count total tasks in file (e.g., T050)
2. Use `--tasks T033-T050`
3. Update range if tasks are added

**With `--start-from`:**
- Just specify: `--start-from T033`
- Automatically includes all tasks from T033 to end
- No need to know the last task ID

---

## Usage

### Basic Usage

```bash
/smartspec_implement_tasks tasks.md --start-from T033
```

**What happens:**
- Starts from T033
- Continues through T034, T035, T036, ...
- Stops at the last task in file

---

### With `--kilocode` Flag

```bash
/smartspec_implement_tasks tasks.md --start-from T033 --kilocode
```

**What happens:**
- Starts from T033
- Continues to end
- Uses Kilo Code sub-task mode for complex tasks (≥2h)

---

### With `--phase` Filter

```bash
/smartspec_implement_tasks tasks.md --start-from T033 --phase 4
```

**What happens:**
- Starts from T033 **within Phase 4**
- Continues to end of Phase 4
- Skips tasks in other phases

---

### With `--skip-completed` (Default)

```bash
/smartspec_implement_tasks tasks.md --start-from T033 --skip-completed
```

**What happens:**
- Starts from T033
- Skips tasks with `[x]` checkbox
- Implements only pending tasks `[ ]`
- Continues to end

---

## Comparison

### `--tasks` vs `--start-from`

| Feature | `--tasks T033-T050` | `--start-from T033` |
|---------|---------------------|---------------------|
| **End task** | Must specify (T050) | Automatic (end of file) |
| **If tasks added** | Must update range | No update needed |
| **Use case** | Specific range | From point to end |
| **Flexibility** | Fixed range | Dynamic range |

---

## Examples

### Example 1: Resume from Middle

**Scenario:** You completed T001-T032, want to continue from T033

```bash
/smartspec_implement_tasks tasks.md --start-from T033
```

**Result:**
- Implements T033, T034, T035, ..., T050 (end)
- Total: 18 tasks

---

### Example 2: Start from Phase 4

**Scenario:** You want to implement all Phase 4 tasks starting from T033

```bash
/smartspec_implement_tasks tasks.md --start-from T033 --phase 4
```

**Result:**
- Implements T033-T040 (Phase 4 tasks only)
- Skips Phase 5+ tasks

---

### Example 3: With Kilo Code Sub-Task Mode

**Scenario:** Resume from T033 with automatic sub-task breakdown

```bash
/smartspec_implement_tasks tasks.md --start-from T033 --kilocode
```

**Result:**
- T033 (2h) → COMPLEX → Sub-task mode
- T034 (0.5h) → SIMPLE → Direct implementation
- T035 (4h) → COMPLEX → Sub-task mode
- Continues to end

---

### Example 4: Force Re-implement from T033

**Scenario:** Re-implement all tasks from T033 (ignore checkboxes)

```bash
/smartspec_implement_tasks tasks.md --start-from T033 --force-all
```

**Result:**
- Implements T033-T050 (all tasks)
- Ignores `[x]` checkboxes
- Re-implements completed tasks

---

## Behavior Details

### Filtering Logic

```
1. Parse all tasks from tasks.md
2. Find task with ID matching --start-from
3. Include that task and all subsequent tasks
4. Apply other filters (phase, skip-completed, etc.)
```

### Example with 50 Tasks

**Tasks file:** T001-T050

**Command:** `--start-from T033`

**Result:**
```
Included: T033, T034, T035, ..., T050
Excluded: T001-T032
Total: 18 tasks
```

---

### Combining with Other Filters

**Command:** `--start-from T033 --phase 4 --skip-completed`

**Logic:**
1. Start from T033
2. Include tasks to end
3. Filter by Phase 4
4. Skip completed tasks

**Result:**
```
Phase 4 tasks: T033-T040
Start from: T033
Completed: T035 [x], T037 [x]
Final: T033, T034, T036, T038, T039, T040
```

---

## When to Use

### ✅ Use `--start-from` when:

1. **Resuming work from a specific point**
   - Completed T001-T032
   - Want to continue from T033

2. **Don't know the last task ID**
   - Tasks file may change
   - Don't want to count tasks

3. **Working on later phases**
   - Start from first task of Phase 4
   - Continue to end

4. **Iterative implementation**
   - Implement in chunks
   - Resume from last completed

---

### ❌ Don't use `--start-from` when:

1. **Need specific task range**
   - Want T033-T040 only (not to end)
   - Use `--tasks T033-T040` instead

2. **Implementing single task**
   - Want T033 only
   - Use `--tasks T033` instead

3. **Starting from beginning**
   - No need for `--start-from`
   - Just run without parameters

---

## Parameter Precedence

When multiple parameters are used:

```
--start-from > --tasks > --phase > --skip-completed
```

**Example:**
```bash
--start-from T033 --tasks T001-T010
```

**Result:** `--start-from` takes precedence
- Implements T033 to end
- Ignores `--tasks T001-T010`

---

## Common Use Cases

### Use Case 1: Daily Work Sessions

**Day 1:**
```bash
/smartspec_implement_tasks tasks.md --tasks T001-T020
```

**Day 2:**
```bash
/smartspec_implement_tasks tasks.md --start-from T021
```

**Day 3:**
```bash
/smartspec_implement_tasks tasks.md --start-from T035
```

---

### Use Case 2: Phase-by-Phase Implementation

**Phase 1-3:** (Completed)

**Phase 4 onwards:**
```bash
/smartspec_implement_tasks tasks.md --start-from T033 --phase 4
```

**Phase 5 onwards:**
```bash
/smartspec_implement_tasks tasks.md --start-from T041 --phase 5
```

---

### Use Case 3: After Adding New Tasks

**Original tasks:** T001-T040

**After adding tasks:** T001-T050 (added T041-T050)

**Command:**
```bash
/smartspec_implement_tasks tasks.md --start-from T041
```

**Result:** Implements new tasks T041-T050

---

## Troubleshooting

### Issue 1: Task ID Not Found

**Error:** "Task T033 not found in tasks file"

**Solutions:**
1. Check task ID exists in tasks.md
2. Verify correct format: `T033` (not `t033` or `Task033`)
3. Check task is not in different file

---

### Issue 2: No Tasks Implemented

**Scenario:** All tasks after T033 are completed `[x]`

**Command:** `--start-from T033 --skip-completed`

**Result:** No tasks to implement (all skipped)

**Solution:** Use `--force-all` to re-implement

---

### Issue 3: Wrong Tasks Implemented

**Scenario:** Expected T033-T050, but only T033-T040 implemented

**Possible cause:** Combined with `--phase` filter

**Check:** Are T041-T050 in different phase?

---

## Summary

### Key Benefits

1. ✅ **No need to specify end task**
   - Automatically goes to end of file
   - Dynamic range

2. ✅ **Easy to resume work**
   - Just specify starting point
   - Continue from where you left off

3. ✅ **Flexible with file changes**
   - Tasks added to end? No problem
   - Range adjusts automatically

4. ✅ **Combines with other filters**
   - Works with `--phase`
   - Works with `--skip-completed`
   - Works with `--kilocode`

---

### Quick Reference

```bash
# Start from T033 to end
/smartspec_implement_tasks tasks.md --start-from T033

# Start from T033 to end (with kilocode)
/smartspec_implement_tasks tasks.md --start-from T033 --kilocode

# Start from T033 within Phase 4
/smartspec_implement_tasks tasks.md --start-from T033 --phase 4

# Start from T033, skip completed
/smartspec_implement_tasks tasks.md --start-from T033 --skip-completed

# Start from T033, force all
/smartspec_implement_tasks tasks.md --start-from T033 --force-all
```

---

## Related Guides

- **[Kilo Code Complete Guide](KILO_CODE_COMPLETE_GUIDE.md)** - Complete guide for all Kilo Code modes
- **[Kilo Code Sub-Task Mode Guide](KILOCODE_MODE_GUIDE.md)** - How to use Orchestrator Mode for sub-tasks
- **[Architect Mode Guide](ARCHITECT_MODE_GUIDE.md)** - How to use Architect Mode for system design
- **[Debug Mode Guide](DEBUG_MODE_GUIDE.md)** - How to use Debug Mode for problem-solving
- **[Implement Tasks Guide](IMPLEMENT_TASKS_DETAILED_GUIDE.md)** - Full workflow documentation

---

**Use `--start-from` to easily resume implementation from any point and continue to the end!** 🚀
