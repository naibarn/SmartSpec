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
| `--claude` | Generate prompt with Claude Code specific instructions. | **claude** |
| `--roocode` | Generate prompt with Roo Code specific instructions. | |
| `--with-subagents` | **(Claude Only)** Enable Sub-Agent workflow. Requires `.claude/agents/` folder. | Disabled |
| `--tasks <range>` | Specify a range of tasks to include (e.g., `T001-T010`). | All tasks |
| `--phase <range>` | Specify a range of phases to include (e.g., `1-3`). | All phases |

---

## 3. Platform-Specific Examples

### Example 1: Kilo Code (`--kilocode`)

Generates a prompt that leverages Kilo Code's multi-mode architecture and automatic sub-task decomposition.

```bash
/smartspec_generate_implement_prompt.md specs/feature/tasks.md --kilocode
```

**Resulting Prompt Includes:**
-   **Platform Instructions (Kilo Code):**
    -   `Mode:` Use `Code Generation` mode.
    -   `Sub-Tasks:` Enable automatic sub-task decomposition.
    -   `Validation:` Run `npm test` and `npm run lint` after each phase.

### Example 2: Claude Code with Sub-Agents (`--claude --with-subagents`)

Generates a prompt designed for Claude Code's multi-agent workflow. It references the pre-defined agents in the `.claude/agents/` directory.

```bash
/smartspec_generate_implement_prompt.md specs/feature/tasks.md --claude --with-subagents
```

**Resulting Prompt Includes:**
-   **Platform Instructions (Claude Code):**
    -   Instructions to use the `planner-smart.md` agent to create a plan.
    -   A step-by-step guide for using the `db-agent-smart`, `backend-smart`, `api-agent-smart`, `tester-smart`, and `security-finance` agents.
    -   **[Read the Full Guide on Claude Sub-Agents](../guides/claude_sub_agents.md)**

### Example 3: Standard Claude Code (`--claude`)

If `--with-subagents` is not used, it generates a standard prompt for a single, interactive Claude Code session.

```bash
/smartspec_generate_implement_prompt.md specs/feature/tasks.md --claude
```

**Resulting Prompt Includes:**
-   General instructions for an interactive coding session.
-   No references to sub-agents.

### Example 4: Roo Code (`--roocode`)

Generates a prompt for Roo Code's safety-first, sequential workflow.

```bash
/smartspec_generate_implement_prompt.md specs/feature/tasks.md --roocode
```

**Resulting Prompt Includes:**
-   **Platform Instructions (Roo Code):**
    -   `Mode:` Use `Safe Execution` mode.
    -   `Workflow:` Execute tasks strictly in order.
    -   `Preview:` Show a diff preview before applying changes.

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
