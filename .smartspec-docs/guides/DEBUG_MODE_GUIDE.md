# Kilo Code Debug Mode Guide

## Overview

**Debug Mode** is a built-in mode in Kilo Code designed for **systematic problem diagnosis and troubleshooting**. It's used when you encounter bugs, errors, or unexpected behavior in your code that needs to be analyzed and fixed.

In Debug Mode, the AI has access to all tools (read, edit, command, mcp, browser) to read files, make edits, run commands, and debug code comprehensively.

---

## When to Use Debug Mode

### ✅ Use Debug Mode when:

| Situation | Why Debug Mode? |
|-----------|-----------------|
| **Bug / Error / Crash / Unexpected Behavior** | AI can read code, analyze error/stack trace, and fix systematically |
| **Complex code with multiple related parts** | Debug Mode has full access to edit multiple files, run commands, check dependencies |
| **Code doesn't work after generate/refactor/merge** | Let AI inspect and fix, reducing human error |
| **Build / Runtime / Environment issues** | AI can run commands, run tests, fix config, check logs |
| **Need root cause analysis + fix plan** | Debug Mode is designed for "diagnosis + fix", not just code generation |

---

## When to Switch to Debug Mode

### From Other Modes:

1. **After Code Mode** → Code generated but has bugs/errors
2. **After generate/auto-refactor/merge** → Results don't match expectations
3. **Before commit** → Run Debug Mode to test and check for issues
4. **When other modes can't fix** → Switch to Debug for focused problem-solving

---

## How SmartSpec Uses Debug Mode

### In `smartspec_implement_tasks` workflow:

SmartSpec automatically switches to Debug Mode in these scenarios:

#### 1. **Validation Failures**

```
Task implementation complete
→ Run validation (compile, test, lint)
→ Validation fails
→ Attempt 1: Quick fix
→ Still fails
→ Switch to Debug Mode
```

**Command:**
```
Use Debug Mode to analyze and fix the issue.
```

**Debug Mode will:**
- Systematically diagnose the problem
- Read error/stack trace
- Check related files and dependencies
- Apply targeted fix
- Run validation again

---

#### 2. **Error Handling**

**File edit/str_replace limit:**
```
Edits keep failing
→ Switch to Debug Mode
→ Debug checks why edits are failing
→ Applies fix
```

**Retry limit (2 attempts):**
```
Same approach fails twice
→ Switch to Debug Mode
→ Debug diagnoses why previous attempts failed
→ Tries different approach
```

**Consecutive errors (3 tasks):**
```
3 tasks fail in a row
→ Switch to Debug Mode
→ Debug looks for common patterns across failures
→ Fixes systemic issues
```

**Infinite loop detection:**
```
Same command executed 3+ times with same result
→ Switch to Debug Mode
→ Debug diagnoses why command keeps failing
→ Breaks the loop
```

---

#### 3. **Phase Checkpoint Validation**

```
End of phase
→ Run phase validation
→ Validation fails
→ Switch to Debug Mode
→ Debug analyzes and fixes
→ Re-run validation
```

---

## Debug Mode vs Other Modes

| Mode | Purpose | When to Use |
|------|---------|-------------|
| **Code Mode** | Generate new code | Creating features, implementing tasks |
| **Orchestrator Mode** | Break into sub-tasks, manage workflow | Complex tasks, stuck in loop |
| **Debug Mode** | Diagnose and fix problems | Bugs, errors, validation failures |

---

## Escalation Chain

SmartSpec uses a **3-level escalation** for problem-solving:

```
Level 1: Quick Fix (Attempt 1)
  ↓ (if fails)
Level 2: Debug Mode
  ↓ (if fails)
Level 3: Orchestrator Mode
  ↓ (if fails)
STOP: Request manual review
```

**Why this order?**

1. **Quick fix** - Fast, for simple issues
2. **Debug Mode** - Systematic diagnosis for bugs/errors
3. **Orchestrator Mode** - Different strategy, broader view
4. **Manual review** - Human intervention needed

---

## Example Workflow

### Scenario: Validation Failure

```markdown
**Task:** T033: Implement Credit Deduction APIs (2h)

**Step 1: Implementation**
→ Code generated successfully

**Step 2: Validation**
→ Run: npm test -- credit/deduct.routes.test.ts
→ Result: ❌ 2 tests failed

**Step 3: Quick Fix (Attempt 1)**
→ Read error messages
→ Fix: Update validation logic
→ Re-run tests
→ Result: ❌ Still 1 test failing

**Step 4: Switch to Debug Mode**
→ Command: "Use Debug Mode to analyze and fix the issue."
→ Debug Mode actions:
  - Read full stack trace
  - Check test file: credit/deduct.routes.test.ts
  - Check implementation: routes/credit/deduct.routes.ts
  - Identify root cause: Missing error handling for negative amounts
  - Apply fix: Add validation for amount > 0
  - Re-run tests
→ Result: ✅ All tests pass

**Step 5: Continue**
→ Task marked as completed
→ Move to next task
```

---

## Best Practices

### ✅ Do:

- Use Debug Mode when you have **concrete errors** to fix
- Let Debug Mode **read error messages and stack traces**
- Give Debug Mode **context** about what was expected vs actual behavior
- **Verify fixes** after Debug Mode completes

### ❌ Don't:

- Use Debug Mode for **generating new features** (use Code Mode)
- Give Debug Mode **too broad scope** (break into sub-tasks with Orchestrator first)
- Skip **manual review** after Debug Mode fixes complex issues
- Ignore **underlying architecture issues** that Debug Mode reveals

---

## Common Scenarios

### 1. Compilation Errors

```
Error: Module not found
→ Debug Mode: Check imports, dependencies, file paths
→ Fix: Update import paths, install missing packages
```

### 2. Test Failures

```
Error: Expected 200, got 400
→ Debug Mode: Check test expectations, API implementation
→ Fix: Update validation logic, fix response format
```

### 3. Runtime Errors

```
Error: Cannot read property 'id' of undefined
→ Debug Mode: Check data flow, null checks
→ Fix: Add null checks, update data handling
```

### 4. Configuration Issues

```
Error: Environment variable not found
→ Debug Mode: Check .env, config files
→ Fix: Add missing env vars, update config
```

---

## Troubleshooting

### Debug Mode doesn't fix the issue

**Try:**
1. Check if Debug Mode identified the root cause correctly
2. Provide more context or error details
3. Switch to Orchestrator Mode for different strategy
4. Request manual review if issue is too complex

### Debug Mode takes too long

**Try:**
1. Break down into smaller sub-tasks first (use Orchestrator)
2. Provide specific scope (which files/functions to check)
3. Skip to manual review for very complex issues

### Debug Mode fixes one issue but creates another

**Try:**
1. Run full validation suite after Debug Mode
2. Use Orchestrator Mode to review overall architecture
3. Manual code review to check for side effects

---

## Summary

**Debug Mode is your systematic problem-solver:**

- ✅ Use for bugs, errors, validation failures
- ✅ Automatically triggered by SmartSpec workflow
- ✅ Part of 3-level escalation (Quick Fix → Debug → Orchestrator)
- ✅ Has full access to diagnose and fix
- ✅ Focused on "diagnosis + fix", not generation

**Remember:** Debug Mode is smart, but always verify fixes and run full validation after debugging!

---

## Related Guides

- **[Kilo Code Sub-Task Mode Guide](KILOCODE_MODE_GUIDE.md)** - How to use Orchestrator Mode for sub-tasks
- **[Troubleshooting Guide](troubleshooting.md)** - Common issues and solutions
- **[Implement Tasks Guide](IMPLEMENT_TASKS_DETAILED_GUIDE.md)** - Full workflow documentation
