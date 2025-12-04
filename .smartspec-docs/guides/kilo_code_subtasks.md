# Guide: Kilo Code Sub-Tasks

This guide provides a comprehensive overview of how to use Kilo Code's powerful **Sub-Task** feature, especially within a SmartSpec workflow.

---

## 1. What Are Sub-Tasks?

In Kilo Code, a **Sub-Task** is a child task that is automatically decomposed from a larger parent task. This allows Kilo Code to:

-   **Solve Complex Problems:** Break down a large goal into smaller, manageable steps.
-   **Optimize Mode Selection:** Use the best mode (Architect, Code, Debug, Ask) for each specific step.
-   **Drive a Workflow:** Think → Plan → Execute → Summarize → Return to Parent.

This is all managed by the **Orchestrator Mode**, which acts as a project manager for your AI.

---

## 2. How Sub-Tasks Are Created

Sub-tasks are created **automatically** by the Orchestrator Mode. You do not need to create them manually.

**The Workflow:**

1.  **You provide a large task:** For example, "Implement the entire authentication system."
2.  **Orchestrator Mode Activates:** Kilo Code detects the task is large and complex.
3.  **Planning Phase:** The Orchestrator analyzes the goal and creates a step-by-step plan.
4.  **Sub-Task Creation:** The plan is converted into a series of sub-tasks (e.g., T001.1, T001.2).
5.  **Execution:** Each sub-task is executed in the most appropriate mode.

---

## 3. Using Sub-Tasks with SmartSpec

The `generate_implement_prompt` workflow is designed to leverage this feature automatically when using the `--kilocode` flag.

### Default Behavior (Sub-Tasks Enabled)

When you run the command with `--kilocode`, the generated prompt will instruct Kilo Code to use its Orchestrator Mode to break down tasks.

```bash
/smartspec_generate_implement_prompt.md specs/your-feature/tasks.md --kilocode
```

**Resulting Prompt Instructions:**
```markdown
## Platform Instructions (Kilo Code)

- **Mode:** Use `Orchestrator Mode` to manage the workflow.
- **Sub-Tasks:** **Enable automatic sub-task decomposition.** Break down each task into smaller, verifiable steps.
- **Validation:** Run `npm test` after each top-level task is complete.
```

### Disabling Sub-Tasks (`--nosubtasks`)

If you have a series of simple, independent tasks, you might want to disable sub-task decomposition for speed.

```bash
/smartspec_generate_implement_prompt.md specs/your-feature/tasks.md --kilocode --nosubtasks
```

**Resulting Prompt Instructions:**
```markdown
## Platform Instructions (Kilo Code)

- **Mode:** Use `Code Generation` mode.
- **Sub-Tasks:** **Disable automatic sub-task decomposition.** Execute tasks sequentially as listed.
- **Validation:** Run `npm test` after each task.
```

---

## 4. Best Practices

-   **Let the Orchestrator Do the Work:** For complex features, trust the Orchestrator to create a plan. Don't try to break down the tasks yourself in the `tasks.md` file.
-   **Use `--nosubtasks` for Simple Chores:** If you're just fixing a series of small bugs or adding simple fields, disabling sub-tasks can be faster.
-   **Review the Plan:** Kilo Code will typically present its sub-task plan for your approval before execution. Review it to ensure it aligns with your expectations.

---

## 5. Sub-Tasks vs. Sub-Agents: A Quick Comparison

It's crucial to understand the difference between Kilo Code's Sub-Tasks and Claude Code's Sub-Agents.

| Feature | Kilo Code (Sub-Tasks) | Claude Code (Sub-Agents) |
| :--- | :--- | :--- |
| **Creation** | **Automatic** (by Orchestrator) | **Manual** (pre-defined in `.claude/agents/`) |
| **Concept** | A **process** (a step in a plan) | An **expert** (a role with a specialty) |
| **Control** | Managed by the AI | Selected by the user (or a planner agent) |
| **When to Use** | For breaking down a single, large task. | For coordinating work across multiple domains. |
