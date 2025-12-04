# Guide: Using Claude Code Sub-Agents with SmartSpec

This guide explains what Sub-Agents are in Claude Code, how to create them, and how to use them effectively within a SmartSpec project.

---

## 1. What Are Sub-Agents in Claude Code?

Think of Sub-Agents as a team of specialized AIs within your project. Instead of one generalist AI handling everything (planning, backend, frontend, testing, security), you delegate tasks to specialists.

**Example Team:**
-   `planner`: Reads the SmartSpec files and creates a high-level plan.
-   `backend`: Writes the service, API, and database logic.
-   `tester`: Writes and runs tests for the code.
-   `security`: Audits the code for security vulnerabilities.

**Key Advantages:**
-   **Focused Context:** Each Sub-Agent has a narrow, deep context, leading to more accurate and relevant code generation.
-   **Improved Quality:** Specialists are better at their specific tasks than generalists.
-   **Parallel Work:** You can instruct Claude to use multiple Sub-Agents to work on different parts of the project concurrently.

---

## 2. The Standard Sub-Agent Pack

SmartSpec now includes a standard set of Sub-Agent definitions, the **SmartSpec Sub-Agent Pack (Set A)**. These files are located in the `.claude/agents/` directory of your project and provide a production-grade starting point.

### Folder Structure

```text
.your-project-root/
└─ .claude/
   └─ agents/
      ├─ planner/
      │  └─ planner-smart.md
      ├─ backend/
      │  └─ backend-smart.md
      ├─ db/
      │  └─ db-agent-smart.md
      ├─ api/
      │  └─ api-agent-smart.md
      ├─ tester/
      │  └─ tester-smart.md
      └─ security/
         └─ security-finance.md
```

### The Agents

| Agent File | Role |
| :--- | :--- |
| `planner-smart.md` | A System Architect that reads SmartSpec files and creates a detailed execution plan. |
| `backend-smart.md` | A Senior Backend Engineer that implements business logic and services. |
| `db-agent-smart.md` | A Database Engineer that handles Prisma schema, migrations, and performance. |
| `api-agent-smart.md` | An API Engineer that builds the REST/API layer, including routes and validation. |
| `tester-smart.md` | A QA Automation Engineer that writes unit, integration, and e2e tests. |
| `security-finance.md` | A Security & Compliance Engineer focused on FinTech-grade security. |

> You can customize these `.md` files to match your project's specific tech stack, coding standards, and requirements.

---

## 3. How to Use Sub-Agents with SmartSpec

The workflow combines the power of SmartSpec's structured planning with Claude's multi-agent execution capabilities.

### Step 1: Generate the Implementation Prompt

First, use the `generate_implement_prompt` command with the `--claude` and `--with-subagents` flags. This tells SmartSpec to create a prompt that is aware of the Sub-Agent structure.

```bash
/smartspec_generate_implement_prompt.md specs/your-feature/tasks.md --claude --with-subagents
```

### Step 2: Instruct the Planner Agent

In the main Claude Code chat, start by instructing the `planner` agent to create a plan.

```text
Use the "planner" agent to analyze the attached prompt file.

Your tasks:
1. Summarize the project scope.
2. Create a phase-by-phase execution plan.
3. For each phase, map the required tasks to the appropriate agents (e.g., db, backend, api, tester, security).
4. Return the plan as a checklist.
```

### Step 3: Execute the Plan with Specialized Agents

Once the planner returns a structured plan, you can delegate the work to the specialized agents.

**Example: Executing Phase 1 (Database and Backend)**

```text
Great, let's start Phase 1.

1.  **DB Agent:** Use the `db-agent-smart` to implement the database schema and migrations for tasks T001-T005.
2.  **Backend Agent:** Once the DB schema is ready, use the `backend-smart` agent to implement the initial service logic for tasks T006-T010.

Execute these steps sequentially and report back on completion.
```

### Step 4: Iterate Through Testing and Security Review

After the core logic is implemented, bring in the `tester` and `security` agents.

```text
Phase 1 implementation is complete. Now:

1.  **Tester Agent:** Use the `tester-smart` agent to write and run unit and integration tests for the new services.
2.  **Security Agent:** Use the `security-finance` agent to audit the new code for compliance and security best practices.

Report any findings or required fixes.
```

---

## 4. Best Practices

-   **Start with the Planner:** Always use the `planner-smart` agent first to ensure the execution plan aligns with the SmartSpec structure.
-   **Customize Agents:** Modify the `.md` files in `.claude/agents/` to fit your project's unique needs.
-   **Version Control:** Keep the `.claude` directory in your Git repository so the entire team shares the same agent definitions.
-   **Be Explicit:** When instructing agents, be clear about which agent should perform which tasks.
