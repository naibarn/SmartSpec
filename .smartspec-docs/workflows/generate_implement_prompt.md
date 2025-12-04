_# `/smartspec_generate_implement_prompt.md`

**Generates a single, comprehensive prompt file for automated execution by platforms like Kilo Code, Roo Code, and Claude Code.**

---

## 1. Summary

This command is the bridge between your `tasks.md` and powerful, agent-based coding platforms. It creates a single, deep-context prompt file that contains all the information an AI agent needs to perform a series of tasks autonomously.

- **What it solves:** It packages your requirements into a format that automated platforms can execute directly, eliminating the need for manual copy-pasting for these specific tools.
- **When to use it:** Use this command when your target platform is **Kilo Code, Roo Code, or Claude Code**—platforms that can read a prompt file and execute it.

---

## 2. Target Platforms & Execution Model

This command is **specifically designed for platforms that support file-based execution**. It is **NOT** for manual copy-paste workflows like those used with Cursor or Antigravity.

| Platform | How to Execute the Generated Prompt | Workflow |
| :--- | :--- | :--- |
| **Kilo Code** | `kilocode execute "<prompt_file>"` | Fully Automated |
| **Roo Code** | `roo run "<prompt_file>"` | Fully Automated |
| **Claude Code** | Upload the file and instruct Claude to execute it. | Semi-Automated |

---

## 3. Usage

```bash
/smartspec_generate_implement_prompt.md <tasks_path> --tasks <task_id_or_range> --<platform>
```

---

## 4. Parameters & Options

| Option | Value | Default | Description |
| :--- | :--- | :--- | :--- |
| `--tasks` | `<task_id_or_range>` | (all) | The ID of the task(s) to include. Supports single tasks (`T001`), ranges (`T001-T005`), or comma-separated lists (`T001,T003`). |
| `--kilocode` | (flag) | (unset) | Generates a prompt with instructions specifically for the Kilo Code platform. |
| `--roocode` | (flag) | (unset) | Generates a prompt with instructions specifically for the Roo Code platform. |
| `--claude` | (flag) | ✅ **Yes** | Generates a prompt with instructions specifically for the Claude Code platform. This is the default if no platform is specified. |

---

## 5. Platform-Specific Examples

This section provides clear examples of the prompt output for each supported platform, highlighting the differences in their instructions.

### **Example 1: Kilo Code (`--kilocode`)**

Kilo Code excels at **automatic sub-task decomposition**. The prompt instructs it to use this capability.

**Command:**
```bash
/smartspec_generate_implement_prompt.md ... --tasks T001-T002 --kilocode
```

**Resulting Prompt (Key Section):**
```markdown
## Platform Instructions (Kilo Code)

- **Mode:** Use `Code Generation` mode.
- **Sub-Tasks:** **Enable automatic sub-task decomposition.** Break down each task into smaller, verifiable steps before implementation.
- **Validation:** Run `npm test` and `npm run lint` after each top-level task is complete.
```

### **Example 2: Claude Code (`--claude`)**

Claude Code uses a **sub-agent architecture**. The prompt instructs it to activate the relevant agents.

**Command:**
```bash
/smartspec_generate_implement_prompt.md ... --tasks T001-T002 --claude
```

**Resulting Prompt (Key Section):**
```markdown
## Platform Instructions (Claude Code)

- **Mode:** Use `Multi-Agent` mode.
- **Sub-Agents:** **Activate `DatabaseAgent` for schema tasks and `APIAgent` for route creation.**
- **Validation:** The `ReviewerAgent` will run validation checks after each agent completes its work.
```

### **Example 3: Roo Code (`--roocode`)**

Roo Code is focused on a **safety-first, sequential workflow**. The prompt emphasizes validation and previews.

**Command:**
```bash
/smartspec_generate_implement_prompt.md ... --tasks T001-T002 --roocode
```

**Resulting Prompt (Key Section):**
```markdown
## Platform Instructions (Roo Code)

- **Mode:** Use `Safe Execution` mode.
- **Workflow:** Execute tasks strictly in the order they appear. Do not proceed to the next task if the current one fails validation.
- **Preview:** Show a diff preview of all file changes before applying them.
- **Validation:** Run `npm test` and confirm success before committing changes.
```

---

## 6. Troubleshooting

| Problem | Cause | Solution |
| :--- | :--- | :--- |
| **"Platform not supported"** | You are trying to use this for Cursor/Antigravity. | Use `/smartspec_generate_cursor_prompt.md` instead. |
| **Kilo/Roo command fails** | The generated prompt may have issues. | Check the prompt file for obvious errors. Ensure the platform flag (`--kilocode`, etc.) was used correctly. |
| **Claude doesn't understand** | The instruction to Claude was not clear. | Be explicit. Say: "Read the uploaded file and execute the implementation tasks described inside, following the platform instructions provided." |
