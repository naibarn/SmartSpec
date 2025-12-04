# `/smartspec_generate_implement_prompt.md`

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

### **Primary Argument**

| Name | Type | Required? | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `tasks_path` | `string` | ✅ Yes | The full path to the source `tasks.md` file. | `specs/features/new-login/tasks.md` |

### **Options**

| Option | Value | Default | Description |
| :--- | :--- | :--- | :--- |
| `--tasks` | `<task_id_or_range>` | (all) | The ID of the task(s) to include. Supports single tasks (`T001`), ranges (`T001-T005`), or comma-separated lists (`T001,T003`). |
| `--kilocode` | (flag) | (unset) | Generates a prompt with instructions specifically for the Kilo Code platform. |
| `--roocode` | (flag) | (unset) | Generates a prompt with instructions specifically for the Roo Code platform. |
| `--claude` | (flag) | ✅ **Yes** | Generates a prompt with instructions specifically for the Claude Code platform. This is the default if no platform is specified. |

---

## 5. Output Format: A Continuous Document

Unlike `generate_cursor_prompt`, this command does **not** create a list of separate prompts. Instead, it generates **one continuous document** that the target platform reads and processes in its entirety.

**Example Command:**
```bash
/smartspec_generate_implement_prompt.md specs/services/user-profile/tasks.md --tasks T001-T002 --kilocode
```

**Resulting Prompt File (`implement-prompt-T001-T002.md`):**

```markdown
# Implementation Prompt: User Profile Service

## Project Context

**SPEC:** user-profile-spec v1.2
**Tech Stack:** TypeScript, Fastify, Prisma, PostgreSQL
**OpenAPI Spec:**
(content of openapi.yaml...)

## Platform Instructions (Kilo Code)

- **Mode:** Use `Code Generation` mode.
- **Sub-Agents:** Activate `DatabaseAgent` and `APIAgent`.
- **Validation:** Run `npm test` and `npm run lint` after each phase.

---

## Tasks to Implement

### Phase 1: Database Layer

#### Task T001: Create User Model

**Description:** Create the Prisma model for the `User`.
**Files to create:** `prisma/schema.prisma`
**Context:** This is the foundational model for the entire service.

#### Task T002: Create Database Migration

**Description:** Generate a new database migration based on the updated schema.
**Depends on:** T001
**Context:** This task will use the `User` model created in T001.
```

**Key Takeaway:** The platform (e.g., Kilo Code) is expected to read this entire file, understand the full context, and execute the tasks sequentially based on the provided information.

---

## 6. Detailed Examples

### **Example 1: Generating a Prompt for Kilo Code**

**Goal:** Create a prompt file to implement the first phase of a feature, to be executed by Kilo Code.

```bash
# 1. Generate the prompt file
/smartspec_generate_implement_prompt.md specs/features/new-feature/tasks.md --phase 1 --kilocode

# 2. Execute in Kilo Code
kilocode execute "specs/features/new-feature/implement-prompt-new-feature.md"
```

### **Example 2: Generating a Prompt for Claude Code**

**Goal:** Create a prompt file for a few specific tasks, to be executed by Claude Code.

```bash
# 1. Generate the prompt file (defaults to --claude)
/smartspec_generate_implement_prompt.md specs/services/auth/tasks.md --tasks T010,T012

# 2. Use with Claude Code
# - Upload the generated 'implement-prompt-auth.md' file.
# - Instruct Claude: "Please execute the tasks in this prompt file."
```

---

## 7. Troubleshooting

| Problem | Cause | Solution |
| :--- | :--- | :--- |
| **"Platform not supported"** | You are trying to use this for Cursor/Antigravity. | Use `/smartspec_generate_cursor_prompt.md` instead. |
| **Kilo/Roo command fails** | The generated prompt may have issues. | Check the prompt file for obvious errors. Ensure the platform flag (`--kilocode`, etc.) was used correctly. |
| **Claude doesn't understand** | The instruction to Claude was not clear. | Be explicit. Say: "Read the uploaded file and execute the implementation tasks described inside, following the platform instructions provided instructions." |
