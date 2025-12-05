# Kilo Code Architect Mode Guide

## Overview

**Architect Mode** is a built-in mode in Kilo Code designed for **system design, architecture planning, and technical specification**. It's used when you need to "design", "structure", "think at system-level", or "define specs" before starting to write code.

Architect Mode doesn't focus on editing code file-by-file like Code Mode, and doesn't analyze errors like Debug Mode. Instead, it focuses on **high-level / system-level** work.

---

## When to Use Architect Mode

### ✅ Use Architect Mode when:

| Situation | Why Architect Mode? |
|-----------|---------------------|
| **System Design** | Need to design overall architecture before coding |
| **New Feature** | Don't know how to break down the work yet |
| **Technical Planning** | Need to create implementation plan before execution |
| **Spec Writing** | Need to convert vague requirements into clear technical specs |
| **Large-Scale Refactor** | Need to plan refactoring strategy before making changes |
| **Module Structure** | Need to decide how to organize files, modules, and responsibilities |

---

## When to Switch to Architect Mode

### Use Architect Mode BEFORE:

1. **Starting a new feature** → Design first, code later
2. **Complex implementation** → Plan structure before execution
3. **System integration** → Design how components interact
4. **Large refactoring** → Plan changes before making them

### Typical Workflow:

```
Architect Mode → Code Mode → Debug Mode → Test Mode
```

**Architect Mode = Think before do**  
**Code/Debug Mode = Actually do it**

---

## Architect Mode Use Cases

### ✅ 1) System Design

**Scenario:**
- Need to design Login/Register system
- Need to design Payment system
- Need to design architecture for Next.js, Nest.js, Express

**Example Prompt:**
```
Use Architect Mode to design the system architecture and create implementation plan.
Design the overall architecture for the new authentication system.
Break it into modules, files, responsibilities, and data flow.
```

---

### ✅ 2) Starting New Feature (Don't Know How to Break Down)

**Scenario:**
- Every time you think: "Before coding, let me summarize what needs to be done"
- Need to break requirements into tasks/subtasks
- Need to define data flow
- Need to define naming and file structure

**Example Prompt:**
```
Use Architect Mode to design the system architecture and create implementation plan.
Create a detailed implementation plan for adding a shopping cart feature.
Include file names, function responsibilities, and API endpoints.
```

---

### ✅ 3) Planning Ahead Before Code Mode

**Best workflow:**
```
Architect Mode → Code Mode → Debug Mode
```

Use Architect Mode to:
- Create technical plan
- Setup architecture layout
- Specify files/folders to be created
- Design logic flow
- Decide which libraries to use

---

### ✅ 4) Writing SPEC or Clear Requirements

**Scenario:**
- Requirements are messy, vague, or unclear
- Architect Mode helps:
  - Make requirements unambiguous
  - Convert general descriptions → actionable specs
  - Define constraints
  - Identify edge cases

**Example Prompt:**
```
Use Architect Mode to design the system architecture and create implementation plan.
Convert this raw idea into a clean, complete technical specification.
```

---

### ✅ 5) Large-Scale Refactor

**Scenario:**
- Need to move business logic out of controllers
- Need to separate monolithic → modular
- Need to reorganize file structure

**Architect Mode helps plan before refactoring**

**Example Prompt:**
```
Use Architect Mode to design the system architecture and create implementation plan.
Create a refactor plan to separate business logic from routes in this project.
```

---

### ✅ 6) Working with Orchestrator Mode

**Orchestrator often creates sub-tasks in this order:**
```
1. Architect Mode - Design architecture
2. Code Mode - Implement code
3. Debug Mode - Fix bugs
4. Test Mode - Run tests
```

**Architect Mode is the first sub-task** in complex work  
Used to "set direction" before switching to actual coding

---

## Architect Mode vs Other Modes

| Mode | Purpose | When to Use |
|------|---------|-------------|
| **Architect Mode** | Design system, create plan | Before coding, for complex features |
| **Code Mode** | Write actual code | Implementing features, generating code |
| **Orchestrator Mode** | Break into sub-tasks, manage workflow | Complex tasks, automatic sub-task creation |
| **Debug Mode** | Diagnose and fix problems | Bugs, errors, validation failures |

---

## 🛑 Architect Mode is NOT for...

| Not Suitable | Why | Use Instead |
|--------------|-----|-------------|
| Fixing bugs / errors | → Use **Debug Mode** | Debug Mode |
| Writing actual code | → Use **Code Mode** | Code Mode |
| Running tests, build, commands | → Use **Code / Debug Mode** | Code/Debug Mode |
| Detailed file editing | → Use **Code Mode** | Code Mode |

**Architect Mode = Think before do**  
**Code/Debug Mode = Actually do**

---

## How SmartSpec Uses Architect Mode

### 1. With `--architect` Flag

**Command:**
```bash
/smartspec_implement_tasks tasks.md --architect
```

**What happens:**
- For EVERY task, Architect Mode runs first
- Architect Mode designs system architecture and creates implementation plan
- Then Code Mode implements based on the architecture

**Workflow:**
```
Task → Architect Mode (design) → Code Mode (implement) → Validate
```

---

### 2. With `--kilocode` Flag (Orchestrator decides)

**Command:**
```bash
/smartspec_implement_tasks tasks.md --kilocode
```

**What happens:**
- Orchestrator Mode analyzes task complexity
- If complex: Orchestrator may use Architect Mode first
- Then breaks into sub-tasks: Architect → Code → Debug → Test

**Example:**
```
Task: T005: Set Up BullMQ 5.x for Background Job Processing (2h)

Orchestrator decides:
- This is complex → Use Architect Mode first

Sub-tasks created:
1. Architect Mode: Design BullMQ architecture and integration plan
2. Code Mode: Install BullMQ dependencies
3. Code Mode: Create queue configuration based on architecture
4. Code Mode: Implement job processor
5. Code Mode: Add error handling and logging
6. Debug Mode: Fix any issues
7. Test Mode: Validate BullMQ integration
```

---

## Example Workflow

### Scenario: New Shopping Cart Feature

```markdown
**Task:** T010: Implement Shopping Cart Feature (4h)

**Step 1: Architect Mode (Design)**
→ Command: "Use Architect Mode to design the system architecture and create implementation plan. T010: Implement Shopping Cart Feature"

→ Architect Mode output:
  - System Architecture:
    - Cart Service (business logic)
    - Cart Controller (API endpoints)
    - Cart Model (data structure)
    - Cart Repository (database operations)
  
  - File Structure:
    - src/services/cart.service.ts
    - src/controllers/cart.controller.ts
    - src/models/cart.model.ts
    - src/repositories/cart.repository.ts
    - src/routes/cart.routes.ts
  
  - API Endpoints:
    - POST /api/cart/add
    - GET /api/cart
    - DELETE /api/cart/item/:id
    - PUT /api/cart/item/:id
  
  - Data Flow:
    Controller → Service → Repository → Database
  
  - Dependencies:
    - Express.js for routing
    - TypeORM for database
    - class-validator for validation

**Step 2: Code Mode (Implementation)**
→ Implement based on architecture
→ Create files according to structure
→ Follow data flow design
→ Use specified dependencies

**Step 3: Debug Mode (Fix Issues)**
→ Fix any bugs or errors
→ Ensure code works as designed

**Step 4: Test Mode (Validation)**
→ Run tests
→ Validate functionality
→ Ensure all endpoints work

**Result:** ✅ Shopping cart feature implemented with proper architecture
```

---

## Best Practices

### ✅ Do:

- Use Architect Mode for **new features** and **complex tasks**
- Let Architect Mode **define structure** before coding
- **Follow the architecture** created by Architect Mode
- Use Architect Mode to **clarify vague requirements**
- Use Architect Mode for **large-scale refactoring plans**

### ❌ Don't:

- Use Architect Mode for **simple tasks** (overkill)
- Skip Architect Mode for **complex system design** (will cause problems later)
- Ignore the **architecture plan** when implementing
- Use Architect Mode to **write actual code** (use Code Mode instead)
- Use Architect Mode to **fix bugs** (use Debug Mode instead)

---

## Common Scenarios

### 1. New Authentication System

```
Use Architect Mode to design the system architecture and create implementation plan.
Design authentication system with JWT, refresh tokens, and role-based access control.
```

**Architect Mode will:**
- Design auth flow
- Define middleware structure
- Specify token handling
- Define user roles and permissions
- Create file structure

---

### 2. API Integration

```
Use Architect Mode to design the system architecture and create implementation plan.
Design integration with external payment API (Stripe).
```

**Architect Mode will:**
- Design API client structure
- Define error handling strategy
- Specify webhook handling
- Define data transformation
- Create service layer

---

### 3. Database Schema Design

```
Use Architect Mode to design the system architecture and create implementation plan.
Design database schema for e-commerce platform.
```

**Architect Mode will:**
- Design entity relationships
- Define tables and columns
- Specify indexes and constraints
- Design migration strategy
- Define repository pattern

---

### 4. Microservices Architecture

```
Use Architect Mode to design the system architecture and create implementation plan.
Design microservices architecture for order processing system.
```

**Architect Mode will:**
- Design service boundaries
- Define inter-service communication
- Specify data consistency strategy
- Design API gateway
- Define deployment architecture

---

## Combining Flags

### `--architect` + `--kilocode`

```bash
/smartspec_implement_tasks tasks.md --architect --kilocode
```

**What happens:**
1. **Architect Mode** designs system architecture for each task
2. **Orchestrator Mode** breaks implementation into sub-tasks
3. **Code Mode** implements based on architecture
4. **Debug Mode** fixes issues
5. **Test Mode** validates

**Best for:**
- Complex features requiring both design and sub-task breakdown
- New systems with multiple components
- Large-scale implementations

---

## Troubleshooting

### Architect Mode creates too much overhead

**Solution:**
- Don't use `--architect` for simple tasks
- Use `--architect` only for complex features
- Let Orchestrator decide (use `--kilocode` only)

### Architecture doesn't match requirements

**Solution:**
- Provide more detailed requirements in task description
- Review architecture output before implementation
- Adjust architecture as needed

### Implementation doesn't follow architecture

**Solution:**
- Explicitly reference architecture in implementation
- Use architecture output as specification
- Validate against architecture during code review

---

## Summary

**Architect Mode is your system designer:**

- ✅ Use for system design, architecture planning, technical specs
- ✅ Use BEFORE coding complex features
- ✅ Part of Architect → Code → Debug → Test workflow
- ✅ Focuses on high-level structure, not implementation details
- ✅ Creates clear plans for Code Mode to follow

**Remember:** Architect Mode designs, Code Mode implements, Debug Mode fixes!

---

## Related Guides

- **[Kilo Code Sub-Task Mode Guide](KILOCODE_MODE_GUIDE.md)** - How to use Orchestrator Mode for sub-tasks
- **[Debug Mode Guide](DEBUG_MODE_GUIDE.md)** - How to use Debug Mode for problem-solving
- **[Implement Tasks Guide](IMPLEMENT_TASKS_DETAILED_GUIDE.md)** - Full workflow documentation
