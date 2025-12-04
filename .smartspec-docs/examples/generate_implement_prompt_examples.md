# Real-World Examples: `/smartspec_generate_implement_prompt.md`

This document provides four concrete, real-world examples of how to use the `/smartspec_generate_implement_prompt.md` command for different platforms and workflows. 

**Scenario:** All examples are based on the same goal: **Implementing a User Profile API** as defined in `specs/user-profile/tasks.md`.

---

## Example 1: Kilo Code with Sub-Tasks (Default)

**Goal:** Implement the entire User Profile API, letting Kilo Code manage the complexity by breaking down large tasks automatically.

**Use Case:** Ideal for large, complex features where you trust the AI to create an optimal execution plan.

### Command

```bash
/smartspec_generate_implement_prompt.md specs/user-profile/tasks.md --kilocode
```

### Resulting Prompt (`implement-prompt-user-profile.md`)

```markdown
# Implementation Prompt: User Profile API

## Project Context
**SPEC:** user-profile-spec v1.2
**Tech Stack:** TypeScript, Fastify, Prisma, PostgreSQL
...

## Platform Instructions (Kilo Code)

- **Sub-Task Mode:** Enabled (Default)
- **Mode:** Use `Orchestrator Mode` to manage the workflow.
- **Strategy:** For any task over 8 hours, automatically decompose it into smaller sub-tasks (1.5-5h each) and assign the optimal mode (Architect, Code, Debug) to each.
- **Validation:** Run `npm test` and `npm run lint` after each top-level task is complete.

## Tasks to Implement

### Phase 1: Database & Core Logic (14h)

- [ ] **T001: Implement User Profile Prisma Schema (12h)**
  - Description: Create the Prisma schema for the user profile, including personal details, settings, and relations.
  - *Note: This task is >8h and will be automatically decomposed by the Orchestrator.*

- [ ] **T002: Add Database Indexes (2h)**
  - Description: Add indexes to `email` and `username` for performance.

...
```

### Expected Kilo Code Behavior

1.  Kilo Code reads the entire prompt.
2.  It enters **Orchestrator Mode**.
3.  For task **T001 (12h)**, it creates a sub-task plan, for example:
    -   `T001.1: Design schema for personal details (2h)` -> Architect Mode
    -   `T001.2: Implement Prisma models (4h)` -> Code Mode
    -   `T001.3: Define relations and constraints (3h)` -> Code Mode
    -   `T001.4: Generate initial migration (1h)` -> Code Mode
    -   `T001.5: Write model validation tests (2h)` -> Code Mode
4.  It executes these sub-tasks sequentially.
5.  For task **T002 (2h)**, it executes it directly in **Code Mode** without decomposition.

---

## Example 2: Kilo Code without Sub-Tasks

**Goal:** Implement a series of small, independent tasks quickly without the overhead of planning.

**Use Case:** Perfect for a batch of bug fixes or simple, sequential updates where planning is unnecessary.

### Command

```bash
/smartspec_generate_implement_prompt.md specs/user-profile/tasks.md --kilocode --nosubtasks
```

### Resulting Prompt (`implement-prompt-user-profile.md`)

```markdown
# Implementation Prompt: User Profile API

## Project Context
...

## Platform Instructions (Kilo Code)

- **Sub-Task Mode:** Disabled
- **Mode:** Use `Code Generation` mode.
- **Strategy:** Execute tasks sequentially as they are listed. Do not decompose tasks.
- **Validation:** Run `npm test` after each task.

## Tasks to Implement

### Phase 1: Bug Fixes (4h)

- [ ] **T003: Fix email validation regex (1h)**
- [ ] **T004: Add missing error handling for not-found user (1h)**
- [ ] **T005: Correct the data type for `lastLogin` (2h)**

...
```

### Expected Kilo Code Behavior

1.  Kilo Code reads the prompt.
2.  It enters **Code Generation Mode**.
3.  It executes T003, T004, and T005 strictly in order, without creating any sub-tasks.

---

## Example 3: Claude Code with Sub-Agents

**Goal:** Implement the User Profile API by delegating work to a team of specialized AI agents.

**Use Case:** Best for large, multi-domain projects (e.g., FinTech, Healthcare) where specialized knowledge in DB, Backend, Security, etc., is critical.

### Command

```bash
/smartspec_generate_implement_prompt.md specs/user-profile/tasks.md --claude --with-subagents
```

### Resulting Prompt (`implement-prompt-user-profile.md`)

```markdown
# Implementation Prompt: User Profile API

## Project Context
...

## Platform Instructions (Claude Code)

This project will be implemented using a multi-agent workflow. Use the pre-defined agents in the `.claude/agents/` directory.

**Recommended Workflow:**

1.  **Use the `planner-smart` agent** to review the tasks and create a detailed execution plan.
2.  **Use the `db-agent-smart` agent** to handle all database schema and migration tasks (T001, T002).
3.  **Use the `backend-smart` agent** to implement the core business logic and services.
4.  **Use the `api-agent-smart` agent** to create the Fastify routes and controllers.
5.  **Use the `tester-smart` agent** to write unit and integration tests.

**[Full Guide on Claude Sub-Agents](../guides/claude_sub_agents.md)**

## Tasks to Implement
...
```

### Expected Claude Code Behavior

1.  The user uploads the prompt file to Claude Code.
2.  The user first instructs Claude: `"Using the planner-smart agent, create a step-by-step plan for this project."`
3.  Claude (as the planner) outputs a plan.
4.  The user then instructs Claude for the next step: `"Excellent. Now, using the db-agent-smart agent, implement the database tasks T001 and T002."`
5.  This process continues, with the user delegating work to the appropriate specialized agent for each phase.

---

## Example 4: Claude Code without Sub-Agents (Default)

**Goal:** Work interactively with a single, general-purpose AI assistant to implement the User Profile API.

**Use Case:** A standard, flexible workflow for developers who prefer a conversational, co-pilot style of development.

### Command

```bash
/smartspec_generate_implement_prompt.md specs/user-profile/tasks.md --claude
```

### Resulting Prompt (`implement-prompt-user-profile.md`)

```markdown
# Implementation Prompt: User Profile API

## Project Context
...

## Platform Instructions (Claude Code)

- **Mode:** Interactive Session
- **Strategy:** We will work through the tasks together, one by one. I will provide the task, and you will generate the code. Please ask for clarification if anything is unclear.

## Tasks to Implement

### Phase 1: Database

- [ ] **T001: Implement User Profile Prisma Schema**
  - Description: Create the Prisma schema for the user profile...

...
```

### Expected Claude Code Behavior

1.  The user uploads the prompt file.
2.  The user instructs Claude: `"Let's start with task T001. Please generate the Prisma schema as described."`
3.  Claude generates the code for T001.
4.  The user reviews the code, provides feedback, and then says, `"Great, let's move on to T002."`
5.  The development proceeds as a back-and-forth conversation.
