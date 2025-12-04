# Workflow: /smartspec_generate_implement_prompt.md

This workflow generates a comprehensive, context-rich implementation prompt file from a `tasks.md` file. It is designed to be used with automated AI platforms like Kilo Code, Claude Code, and Roo Code.

---

## 1. Core Functionality

-   **Input:** A `tasks.md` file containing a list of implementation tasks.
-   **Output:** A single Markdown file (`implement-prompt-*.md`) containing all the necessary context for an AI to start working.
-   **Platforms:** Supports Kilo Code, Claude Code, and Roo Code with platform-specific instructions.

---

## 2. How to Use

### Command Structure

```bash
/smartspec_generate_implement_prompt.md <path_to_tasks.md> [options]
```

### Options

| Flag | Description | Default |
| :--- | :--- | :--- |
| `--kilocode` | Generate prompt with Kilo Code specific instructions. | | 
| `--nosubtasks` | **(Kilo Only)** Disable automatic sub-task decomposition. | Enabled |
| `--claude` | Generate prompt with Claude Code specific instructions. | **claude** |
| `--with-subagents` | **(Claude Only)** Enable Sub-Agent workflow. Requires `.claude/agents/` folder. | Disabled |
| `--roocode` | Generate prompt with Roo Code specific instructions. | |
| `--tasks <range>` | Specify a range of tasks to include (e.g., `T001-T010`). | All tasks |
| `--phase <range>` | Specify a range of phases to include (e.g., `1-3`). | All phases |

---

## 3. Platform-Specific Examples

### Example 1: Kilo Code with Sub-Tasks (Default)

Generates a prompt that leverages Kilo Code's Orchestrator Mode to automatically break down complex tasks.

```bash
/smartspec_generate_implement_prompt.md specs/feature/tasks.md --kilocode
```

**Resulting Prompt Includes:**
-   **Platform Instructions (Kilo Code):**
    -   `Sub-Task Mode: Enabled (Default)`
    -   Instructions to use `Orchestrator Mode` for automatic decomposition.
    -   **[Read the Full Guide on Kilo Code Sub-Tasks](../guides/kilo_code_subtasks.md)**

### Example 2: Kilo Code without Sub-Tasks

For simpler tasks, you can disable sub-task decomposition.

```bash
/smartspec_generate_implement_prompt.md specs/feature/tasks.md --kilocode --nosubtasks
```

**Resulting Prompt Includes:**
-   **Platform Instructions (Kilo Code):**
    -   `Sub-Task Mode: Disabled`
    -   Instructions to use `Code Generation` mode and execute tasks sequentially.

### Example 3: Claude Code with Sub-Agents

Generates a prompt for Claude Code's multi-agent workflow, referencing pre-defined agents.

```bash
/smartspec_generate_implement_prompt.md specs/feature/tasks.md --claude --with-subagents
```

**Resulting Prompt Includes:**
-   **Platform Instructions (Claude Code):**
    -   A step-by-step guide for using the `planner`, `db`, `backend`, `api`, `tester`, and `security` agents.
    -   **[Read the Full Guide on Claude Sub-Agents](../guides/claude_sub_agents.md)**

### Example 4: Standard Claude Code

Generates a standard prompt for a single, interactive Claude Code session.

```bash
/smartspec_generate_implement_prompt.md specs/feature/tasks.md --claude
```

---

## 4. The Deep-Context Assembly Process

This workflow gathers information from multiple sources to create a rich and detailed prompt. This process ensures the AI has all the necessary context to generate high-quality, accurate code from the first attempt.

### The 5 Layers of Context

1.  **Project & Task Context (The "Why"):** High-level overview of the project and the specific task's goal.
2.  **File & Code Context (The "Where"):** Relevant existing code snippets and file structures.
3.  **Dependency Context (The "How"):** Information about related tasks, libraries, and APIs.
4.  **Platform-Specific Instructions (The "Rules"):** Tailored instructions for the target AI platform (Kilo, Claude, or Roo).
5.  **Output & Validation Context (The "What"):** Clear definition of the expected output and the commands to validate it.

This deep context is what enables the AI to perform complex tasks correctly and efficiently.
