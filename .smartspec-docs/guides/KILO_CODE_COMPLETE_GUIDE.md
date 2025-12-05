# Kilo Code Complete Guide

## Overview

This is the **complete guide** for using Kilo Code with SmartSpec workflows. It covers all 5 Kilo Code modes and how to use them effectively with the `--kilocode` flag.

**Kilo Code** is an AI-powered coding assistant with multiple specialized modes for different tasks. When you use the `--kilocode` flag in SmartSpec workflows, you enable intelligent task management with automatic mode switching.

---

## Table of Contents

1. [Kilo Code Modes Overview](#kilo-code-modes-overview)
2. [When to Use Each Mode](#when-to-use-each-mode)
3. [The `--kilocode` Flag](#the---kilocode-flag)
4. [Typical Workflows](#typical-workflows)
5. [Mode Switching](#mode-switching)
6. [Best Practices](#best-practices)
7. [Troubleshooting](#troubleshooting)
8. [Examples](#examples)

---

## Kilo Code Modes Overview

Kilo Code has **5 specialized modes**, each designed for specific tasks:

| Mode | Purpose | When to Use | Output |
|------|---------|-------------|--------|
| **Ask Mode** | Analyze and understand | Before making decisions | Insights, options, recommendations |
| **Architect Mode** | Design and plan | Before implementing complex features | Architecture, technical specs, plans |
| **Code Mode** | Implement | Writing actual code | Code files |
| **Debug Mode** | Fix problems | When bugs or errors occur | Bug fixes, error resolution |
| **Orchestrator Mode** | Manage workflow | Complex tasks needing sub-tasks | Sub-tasks, task breakdown |

---

### 1. Ask Mode

**Purpose:** Analyze, understand, and explore before making decisions.

**Use when:**
- Need to understand existing code
- Exploring implementation options
- Analyzing impact of changes
- Clarifying vague requirements
- Need recommendations or best practices

**Command:**
```
Ask Mode.
Based on the current project structure, what approaches can we use to add role-based authentication?
```

**Output:**
- Analysis of current code
- List of available options
- Pros and cons of each approach
- Recommendations
- Impact analysis

**Learn more:** [Ask Mode Guide](ASK_MODE_GUIDE.md)

---

### 2. Architect Mode

**Purpose:** Design system architecture and create implementation plans.

**Use when:**
- Starting complex new features
- Need to design system structure
- Creating technical specifications
- Planning large refactors
- Defining API contracts and data models

**Command:**
```
Use Architect Mode to design the system architecture and create implementation plan.
```

**Output:**
- System architecture design
- Technical specifications
- File structure and modules
- Data flow diagrams
- Implementation plan

**Learn more:** [Architect Mode Guide](ARCHITECT_MODE_GUIDE.md)

---

### 3. Code Mode

**Purpose:** Write and implement actual code.

**Use when:**
- Implementing features
- Writing new code
- Adding functionality
- Creating files and modules
- Following an existing plan

**Command:**
```
Implement the feature according to the architecture.
```

**Output:**
- Code files
- Implementation
- Functions and classes
- Tests (if requested)

**Note:** Code Mode is the default mode. You don't need to explicitly switch to it unless coming from another mode.

---

### 4. Debug Mode

**Purpose:** Systematically diagnose and fix bugs, errors, and issues.

**Use when:**
- Bugs or errors occur
- Tests are failing
- Compilation errors
- Runtime errors
- Code behaves unexpectedly

**Command:**
```
Use Debug Mode to analyze and fix the issue.
```

**Output:**
- Root cause analysis
- Bug fixes
- Error resolution
- Verification that issue is resolved

**Learn more:** [Debug Mode Guide](DEBUG_MODE_GUIDE.md)

---

### 5. Orchestrator Mode

**Purpose:** Break complex tasks into manageable sub-tasks and coordinate execution.

**Use when:**
- Task is complex (estimated 2+ hours)
- Task needs to be broken down
- Multiple steps required
- Using `--kilocode` flag in SmartSpec workflows

**Command:**
```
Use Orchestrator Mode to break this task into subtasks. T005: Set Up BullMQ 5.x for Background Job Processing
```

**Output:**
- Sub-tasks breakdown
- Workflow coordination
- May use other modes (Ask, Architect, Code, Debug, Test)
- Progress tracking

**Learn more:** [Kilo Code Sub-Task Mode Guide](KILOCODE_MODE_GUIDE.md)

---

## When to Use Each Mode

### Decision Tree

```
Start
  │
  ├─ Need to understand/analyze? → Ask Mode
  │
  ├─ Need to design architecture? → Architect Mode
  │
  ├─ Need to write code? → Code Mode
  │
  ├─ Need to fix bugs/errors? → Debug Mode
  │
  └─ Task is complex/needs breakdown? → Orchestrator Mode
```

---

### Mode Combinations

Modes are often used together in sequences:

#### Simple Task
```
Code → Test
```

#### Medium Task
```
Architect → Code → Debug → Test
```

#### Complex Task
```
Ask → Architect → Code → Debug → Test
```

#### Unclear Task
```
Ask → Architect → Code → Debug → Test
```

#### Bug Fixing
```
Ask (analyze) → Debug (fix)
```

#### Large Refactor
```
Ask (impact analysis) → Architect (design) → Code (refactor) → Debug (fix) → Test
```

---

## The `--kilocode` Flag

### What is `--kilocode`?

The `--kilocode` flag enables **Orchestrator Mode** in SmartSpec workflows. When you use this flag:

1. Tasks are sent to **Orchestrator Mode**
2. Orchestrator **analyzes task complexity**
3. Orchestrator **decides which modes to use**
4. Orchestrator **breaks into sub-tasks if needed**
5. Orchestrator **coordinates execution**

### Supported Workflows

The `--kilocode` flag is supported in these SmartSpec workflows:

| Workflow | Purpose | Typical Mode Sequence |
|----------|---------|----------------------|
| `smartspec_implement_tasks` | Implement features | Ask → Architect → Code → Debug → Test |
| `smartspec_fix_errors` | Fix errors | Debug |
| `smartspec_refactor_code` | Refactor code | Ask → Architect → Code → Debug → Test |
| `smartspec_generate_tests` | Generate tests | Ask → Architect → Code → Test |

### Usage Examples

#### Implement Tasks
```bash
/smartspec_implement_tasks tasks.md --kilocode
/smartspec_implement_tasks tasks.md --start-from T033 --kilocode
/smartspec_implement_tasks tasks.md --phase 4 --kilocode
```

#### Fix Errors
```bash
/smartspec_fix_errors specs/feature/spec-004 --kilocode
/smartspec_fix_errors specs/feature/spec-004 --file src/services/credit.service.ts --kilocode
```

#### Refactor Code
```bash
/smartspec_refactor_code specs/feature/spec-004 --kilocode
/smartspec_refactor_code specs/feature/spec-004 --focus complexity --kilocode
```

#### Generate Tests
```bash
/smartspec_generate_tests specs/feature/spec-004 --kilocode
/smartspec_generate_tests specs/feature/spec-004 --target-coverage 90 --kilocode
```

---

## Typical Workflows

### Workflow 1: Implement New Feature (Simple)

**Task:** Add validation to user registration (1h)

```
1. Code Mode: Implement validation
2. Test: Verify validation works
```

**Command:**
```bash
/smartspec_implement_tasks tasks.md --tasks T001
```

**No need for `--kilocode`** - simple task, direct implementation.

---

### Workflow 2: Implement New Feature (Complex)

**Task:** Set up BullMQ for background job processing (2h)

```
1. Ask Mode: Analyze current job processing and BullMQ options
2. Architect Mode: Design BullMQ architecture
3. Code Mode: Install dependencies
4. Code Mode: Create queue configuration
5. Code Mode: Implement job processor
6. Code Mode: Add error handling
7. Debug Mode: Fix any issues
8. Test Mode: Validate integration
```

**Command:**
```bash
/smartspec_implement_tasks tasks.md --tasks T005 --kilocode
```

**Use `--kilocode`** - complex task, needs breakdown and planning.

---

### Workflow 3: Fix Errors

**Scenario:** Multiple TypeScript errors after refactoring

```
1. Debug Mode: Analyze all errors
2. Debug Mode: Fix errors one by one
3. Debug Mode: Verify fixes
4. Test: Run tests
```

**Command:**
```bash
/smartspec_fix_errors specs/feature/spec-004 --kilocode
```

**Use `--kilocode`** - systematic error fixing with Debug Mode.

---

### Workflow 4: Refactor Code

**Scenario:** Reduce complexity in payment service

```
1. Ask Mode: Analyze current code structure and complexity
2. Architect Mode: Design refactored architecture
3. Code Mode: Extract methods
4. Code Mode: Simplify logic
5. Code Mode: Update tests
6. Debug Mode: Fix any issues
7. Test: Verify all tests pass
```

**Command:**
```bash
/smartspec_refactor_code specs/feature/spec-004 --focus complexity --kilocode
```

**Use `--kilocode`** - complex refactoring needs planning.

---

### Workflow 5: Generate Tests

**Scenario:** Increase coverage from 45% to 80%

```
1. Ask Mode: Analyze current test structure and patterns
2. Architect Mode: Design test architecture and test cases
3. Code Mode: Generate unit tests
4. Code Mode: Generate integration tests
5. Code Mode: Generate e2e tests
6. Test Mode: Run all tests and verify coverage
```

**Command:**
```bash
/smartspec_generate_tests specs/feature/spec-004 --target-coverage 80 --kilocode
```

**Use `--kilocode`** - comprehensive test generation needs planning.

---

## Mode Switching

### Automatic Mode Switching

When using `--kilocode`, Orchestrator Mode **automatically switches modes** based on needs:

```
Orchestrator analyzes task
  │
  ├─ Complex/unclear? → Ask Mode (analyze)
  │                      ↓
  ├─ Needs design? → Architect Mode (design)
  │                   ↓
  ├─ Ready to code? → Code Mode (implement)
  │                    ↓
  ├─ Errors occur? → Debug Mode (fix)
  │                   ↓
  └─ Need to verify? → Test Mode (validate)
```

### Manual Mode Switching

You can also manually switch modes in SmartSpec workflows:

#### Switch to Debug Mode
```
Use Debug Mode to analyze and fix the issue.
```

#### Switch to Orchestrator Mode
```
Use Orchestrator Mode to resolve the issue.
```

#### Switch to Architect Mode
```
Use Architect Mode to design the system architecture and create implementation plan.
```

#### Switch to Ask Mode
```
Ask Mode.
Based on the current project structure, what approaches can we use?
```

---

## Best Practices

### ✅ Do:

1. **Use `--kilocode` for complex tasks (2+ hours)**
   - Orchestrator will break down and manage
   - Automatic mode switching
   - Better planning and execution

2. **Let Orchestrator decide mode sequence**
   - Orchestrator is smart
   - Knows when to use Ask, Architect, Code, Debug
   - Don't micromanage

3. **Use Ask Mode before complex decisions**
   - Analyze before deciding
   - Explore options
   - Understand impact

4. **Use Architect Mode for complex features**
   - Design before coding
   - Clear architecture
   - Better code quality

5. **Use Debug Mode for systematic problem-solving**
   - Root cause analysis
   - Systematic fixes
   - Verification

### ❌ Don't:

1. **Don't use `--kilocode` for simple tasks**
   - Overkill for simple tasks
   - Direct implementation is faster
   - Use only for complex tasks (2+ hours)

2. **Don't skip Ask Mode for unclear tasks**
   - Will cause problems later
   - Need to understand first
   - Analyze before deciding

3. **Don't skip Architect Mode for complex features**
   - Will result in messy code
   - Need clear design
   - Plan before coding

4. **Don't manually switch modes unnecessarily**
   - Let Orchestrator decide
   - Trust the workflow
   - Only switch when stuck

5. **Don't expect Code Mode to design**
   - Code Mode implements
   - Use Architect Mode for design
   - Use Ask Mode for analysis

---

## Troubleshooting

### Problem: Kilo Code stuck in loop

**Symptoms:**
- Same action repeated
- No progress
- "Model stuck in loop" error

**Solution:**
- SmartSpec automatically switches to Orchestrator Mode
- Orchestrator will try different approach
- If still stuck, switch to Debug Mode manually

**Prevention:**
- Use `--kilocode` for complex tasks
- Let Orchestrator manage workflow

---

### Problem: Task not broken into sub-tasks

**Symptoms:**
- Using `--kilocode` but task not broken down
- Direct implementation instead of sub-tasks

**Cause:**
- Task is simple (< 2 hours)
- Orchestrator decided sub-tasks not needed

**Solution:**
- This is normal behavior
- Orchestrator is smart enough to decide
- Simple tasks don't need sub-tasks

---

### Problem: Wrong mode used

**Symptoms:**
- Code Mode trying to design
- Debug Mode trying to implement
- Wrong output

**Cause:**
- Manual mode switching error
- Unclear instructions

**Solution:**
- Use `--kilocode` flag
- Let Orchestrator decide modes
- Follow recommended workflows

---

### Problem: No architecture design

**Symptoms:**
- Code written without design
- Messy structure
- Hard to maintain

**Cause:**
- Skipped Architect Mode
- Direct to Code Mode

**Solution:**
- Use `--kilocode` flag
- Orchestrator will use Architect Mode for complex tasks
- Or manually use `--architect` flag

---

## Examples

### Example 1: Implement Credit System (Complex)

**Task:**
```markdown
- [ ] T033: Implement Credit Transaction Service (4h)
```

**Command:**
```bash
/smartspec_implement_tasks tasks.md --tasks T033 --kilocode
```

**What happens:**

1. **Orchestrator analyzes:** 4h = complex task

2. **Sub-tasks created:**
   - **Ask Mode:** Analyze current payment/credit system structure
   - **Architect Mode:** Design credit transaction service architecture
   - **Code Mode:** Create credit transaction model
   - **Code Mode:** Implement transaction creation
   - **Code Mode:** Implement transaction history
   - **Code Mode:** Add balance validation
   - **Code Mode:** Add error handling
   - **Debug Mode:** Fix any issues
   - **Test Mode:** Validate all functionality

3. **Execution:** Each sub-task executed in order

4. **Result:** ✅ Credit transaction service implemented with clear architecture

---

### Example 2: Fix TypeScript Errors

**Scenario:** 15 TypeScript errors after refactoring

**Command:**
```bash
/smartspec_fix_errors specs/feature/spec-004 --kilocode
```

**What happens:**

1. **Orchestrator analyzes:** Multiple errors, use Debug Mode

2. **Debug Mode workflow:**
   - Analyze all 15 errors
   - Identify root causes
   - Group related errors
   - Fix errors systematically
   - Verify each fix
   - Run tests

3. **Result:** ✅ All errors fixed, tests passing

---

### Example 3: Refactor Complex Service

**Scenario:** Payment service has complexity score of 25 (should be < 10)

**Command:**
```bash
/smartspec_refactor_code specs/feature/spec-004 --focus complexity --kilocode
```

**What happens:**

1. **Orchestrator analyzes:** Complex refactoring needed

2. **Sub-tasks created:**
   - **Ask Mode:** Analyze current code structure and complexity sources
   - **Architect Mode:** Design refactored architecture with lower complexity
   - **Code Mode:** Extract helper methods
   - **Code Mode:** Simplify conditional logic
   - **Code Mode:** Split large functions
   - **Code Mode:** Update tests
   - **Debug Mode:** Fix any issues
   - **Test Mode:** Verify all tests pass

3. **Result:** ✅ Complexity reduced from 25 to 8, all tests passing

---

### Example 4: Generate Comprehensive Tests

**Scenario:** Coverage is 45%, target is 80%

**Command:**
```bash
/smartspec_generate_tests specs/feature/spec-004 --target-coverage 80 --kilocode
```

**What happens:**

1. **Orchestrator analyzes:** Need to generate many tests

2. **Sub-tasks created:**
   - **Ask Mode:** Analyze current test structure and patterns
   - **Architect Mode:** Design test architecture and test cases
   - **Code Mode:** Generate unit tests for service layer
   - **Code Mode:** Generate unit tests for controller layer
   - **Code Mode:** Generate integration tests
   - **Code Mode:** Generate e2e tests
   - **Test Mode:** Run all tests and verify coverage

3. **Result:** ✅ Coverage increased from 45% to 82%

---

## Summary

### Kilo Code Modes

| Mode | Purpose | Use Case |
|------|---------|----------|
| **Ask** | Analyze | Understanding, exploring options |
| **Architect** | Design | System architecture, planning |
| **Code** | Implement | Writing code |
| **Debug** | Fix | Bugs, errors, issues |
| **Orchestrator** | Manage | Complex tasks, workflow coordination |

### When to Use `--kilocode`

✅ **Use for:**
- Complex tasks (2+ hours)
- Tasks needing breakdown
- Systematic error fixing
- Large refactorings
- Comprehensive test generation

❌ **Don't use for:**
- Simple tasks (< 1 hour)
- Clear, straightforward implementation
- Quick fixes
- Single file changes

### Typical Workflows

```
Simple:   Code → Test
Medium:   Architect → Code → Debug → Test
Complex:  Ask → Architect → Code → Debug → Test
Unclear:  Ask → Architect → Code → Debug → Test
Bug Fix:  Ask → Debug
Refactor: Ask → Architect → Code → Debug → Test
```

### Best Practices

1. Use `--kilocode` for complex tasks
2. Let Orchestrator decide mode sequence
3. Use Ask Mode before complex decisions
4. Use Architect Mode for complex features
5. Use Debug Mode for systematic problem-solving
6. Trust the workflow
7. Don't micromanage mode switching

---

## Related Guides

- **[Ask Mode Guide](ASK_MODE_GUIDE.md)** - Detailed guide for Ask Mode
- **[Architect Mode Guide](ARCHITECT_MODE_GUIDE.md)** - Detailed guide for Architect Mode
- **[Debug Mode Guide](DEBUG_MODE_GUIDE.md)** - Detailed guide for Debug Mode
- **[Kilo Code Sub-Task Mode Guide](KILOCODE_MODE_GUIDE.md)** - Detailed guide for Orchestrator Mode
- **[Implement Tasks Workflow](../.smartspec/workflows/smartspec_implement_tasks.md)** - Main implementation workflow
- **[Troubleshooting Guide](troubleshooting.md)** - Common issues and solutions

---

## Quick Reference

### Commands

```bash
# Implement with Kilo Code
/smartspec_implement_tasks tasks.md --kilocode

# Fix errors with Kilo Code
/smartspec_fix_errors specs/feature/spec-004 --kilocode

# Refactor with Kilo Code
/smartspec_refactor_code specs/feature/spec-004 --kilocode

# Generate tests with Kilo Code
/smartspec_generate_tests specs/feature/spec-004 --kilocode
```

### Mode Switching

```
# Ask Mode
Ask Mode.
[Your question]

# Architect Mode
Use Architect Mode to design the system architecture and create implementation plan.

# Debug Mode
Use Debug Mode to analyze and fix the issue.

# Orchestrator Mode
Use Orchestrator Mode to break this task into subtasks. [Task description]
```

---

**Remember:** Kilo Code is your intelligent assistant. Use `--kilocode` for complex tasks and let Orchestrator manage the workflow. Trust the process! 🚀
