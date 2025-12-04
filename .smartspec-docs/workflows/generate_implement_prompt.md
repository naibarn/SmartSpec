# `/smartspec_generate_implement_prompt.md`

**(Alias: `/kilo`)**

**Generates a comprehensive, context-rich prompt for a specific task, ready for use in AI coding assistants like Cursor or Google Antigravity.**

---

## 1. Summary

This is the central command for the manual, AI-assisted "Vibe Coding" workflow. It acts as a powerful context assembler. You point it to a task, and it intelligently gathers all relevant information—from the `spec.md`, `openapi.yaml`, data models, and even existing source code—to create a perfect, self-contained prompt.

- **What it solves:** It eliminates the tedious and error-prone process of manually copy-pasting context for an AI. It provides the AI with a "complete world view" for the task, dramatically improving the accuracy and quality of the generated code.
- **When to use it:** This is your primary, day-to-day command during development when you are implementing tasks with an AI assistant.

---

## 2. Clarification: `generate_implement_prompt` vs. `implement_tasks`

There is a critical distinction between these two commands:

- **`/smartspec_implement_tasks.md`**: This is for **full automation**. The AI agent takes the `tasks.md` and runs the implementation autonomously, writing code directly to your files.
- **`/smartspec_generate_implement_prompt.md`**: This is for **manual, AI-assisted coding**. Its only job is to **GENERATE A PROMPT**. It does **NOT** write any code. You take the generated prompt and use it in a separate tool like Cursor.

**Key takeaway:** This command is a **prompt generator**, not a code implementer.

---

## 3. Usage

```bash
/smartspec_generate_implement_prompt.md <tasks_path> --tasks <task_id_or_range> [options...]
# Alias
/kilo <tasks_path> --tasks <task_id_or_range> [options...]
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
| `--tasks` | `<task_id_or_range>` | (none) | ✅ **Required.** The ID of the task(s) you want to generate a prompt for. Supports single tasks (`T001`), ranges (`T001-T005`), or comma-separated lists (`T001,T003`). |
| `--include-files` | `<glob_pattern>` | (auto) | Includes the content of specified files in the context. Supports glob patterns. | `--include-files "src/utils/*.ts"` |
| `--no-related-code` | (flag) | (unset) | Prevents the AI from automatically searching for and including related code snippets from the existing codebase. |

---

## 5. How Multiple Tasks are Handled

This is a key point of clarification:

- **One Prompt File:** Even if you specify multiple tasks (e.g., `--tasks T001-T005`), the command generates **ONE single prompt file** (e.g., `implement-prompt-T001-T005.md`).
- **Sequential Tasks in One Prompt:** Inside that single file, the tasks are presented sequentially. The prompt will guide the AI to implement them in the correct order, one after the other.

**Example Command:**
```bash
/kilo specs/services/user-profile/tasks.md --tasks T001-T003
```

**Resulting Prompt Structure (in `implement-prompt-T001-T003.md`):**

> ### Task 1 of 3: T001 - Create User Model
> (Context and instructions for T001)
>
> ---
>
> ### Task 2 of 3: T002 - Create Database Migration
> (Context and instructions for T002, noting that it depends on T001)
>
> ---
>
> ### Task 3 of 3: T003 - Implement User Service
> (Context and instructions for T003, noting it uses the model from T001)

This structure allows you to paste one large prompt into Cursor and have it work through a series of related tasks in a single session.

---

## 6. The Deep-Context Assembly Process

When you run this command, the AI performs a deep-context assembly:

1.  **Task Extraction:** It reads the specified task(s) from `tasks.md`.
2.  **SPEC Context:** It finds the associated `spec.md` and extracts the sections most relevant to the task(s).
3.  **Supporting Document Context:** It automatically finds and includes relevant parts of supporting documents like `openapi.yaml`.
4.  **Code Context (Auto):** It searches the codebase for existing files or code snippets that are relevant.
5.  **Explicit File Context:** It includes the full content of any files you specify with `--include-files`.
6.  **Prompt Assembly:** It combines all this context into a single, perfectly formatted Markdown prompt, ready for you to copy.

---

## 7. Detailed Examples

### **Example 1: Generating a Prompt for a Single API Task**

**Goal:** Generate a prompt to implement the business logic for one API endpoint.

```bash
/kilo specs/services/user-profile/tasks.md --tasks T005
```

**Result:** A file `implement-prompt-T005.md` is created containing a detailed prompt for only task `T005`.

### **Example 2: Generating a Prompt for a Sequence of Tasks**

**Goal:** Generate a single prompt to create a model, a service, and a controller.

```bash
/kilo specs/features/new-feature/tasks.md --tasks T021-T023
```

**Result:** A single file `implement-prompt-T021-T023.md` is created. Inside, it will have three sections, one for each task, ordered sequentially.

---

## 8. How to Use with Cursor / Google Antigravity

1.  **Generate the Prompt:** Run `/kilo` with the desired task ID(s).
2.  **Copy the Entire Prompt:** A new file (`implement-prompt-Txxx.md`) is created and its content is displayed. Copy the entire text.
3.  **Paste into your AI Assistant:** Paste the complete prompt into the chat panel of Cursor or Google Antigravity.
4.  **Review and Apply:** The AI will now generate the code for all the tasks in the prompt, one by one.

---

## 9. Troubleshooting

| Problem | Cause | Solution |
| :--- | :--- | :--- |
| **"Task ID not found"** | The task ID is incorrect. | Check the `tasks.md` file for the correct task ID. |
| **Prompt is missing context** | The `spec.md` or other supporting files are missing. | Ensure all related SmartSpec files are in the same directory as `tasks.md`. |
| **AI generates incorrect code** | The context in the `spec.md` may be insufficient. | Improve the detail in the `spec.md` and re-generate the prompt. Use `--include-files` to force-feed specific context to the AI. |

---

## Appendix: The Deep-Context Assembly Process

This section provides a detailed look into the **Deep-Context Assembly** process, which is the secret behind the high-accuracy prompts generated by this command.

### What is Deep-Context Assembly?

It's an intelligent mechanism that gathers and organizes all relevant information about a specific coding task into a single, comprehensive prompt. Instead of just giving the AI a one-line instruction, it builds a **"complete world view"** for that task, dramatically reducing ambiguity.

### The 5 Layers of Context

The process assembles information from five distinct layers:

| Layer | Context Type | Information Assembled | Source(s) |
| :--- | :--- | :--- | :--- |
| **1** | **Project & Task (The "Why")** | - Project Overview & Tech Stack<br>- Specific Task Definition & Goal | `tasks.md` | 
| **2** | **Specification (The "What")** | - Relevant `spec.md` sections:<br>  - Data Models<br>  - API Specification<br>  - Business Rules | `spec.md` | 
| **3** | **Supporting Docs (The "How")** | - API Contracts<br>- Detailed Schemas<br>- Architecture Diagrams | `openapi.yaml`, `data-model.md` | 
| **4** | **Codebase (The "Where")** | - Related Type Definitions<br>- Existing Utility Functions<br>- Similar Components (for style) | `*.ts`, `*.js` (auto-detected) | 
| **5** | **Platform (The "Execution")** | - Instructions for Kilo, Claude, or Roo Code<br>- Mode selection logic | Workflow Definition | 

### Example: Assembling a Prompt for an API Task

For a task like **"Implement `POST /api/credit/purchase` endpoint,"** the process gathers:

1.  **From `tasks.md`**: The task description.
2.  **From `spec.md`**: The `credits` data model and the "max 1,000 credits" business rule.
3.  **From `openapi.yaml`**: The exact request/response schema for the endpoint.
4.  **From the codebase**: The existing `User` type from `src/types/user.ts` and the `handleApiError` function from `src/utils/error-handler.ts`.
5.  **From the workflow**: Instructions for the target AI platform (e.g., "Use the API Agent for this task").

### Why This Leads to First-Time Accuracy

- **Reduces Ambiguity:** The AI doesn't have to guess the data model or business rules.
- **Ensures Consistency:** By seeing existing code, the AI writes new code that matches the project's style.
- **Prevents Hallucinations:** The AI is constrained to the project's reality, preventing it from inventing incorrect structures.
- **Improves Efficiency:** Developers waste less time correcting the AI, as the first output is significantly more accurate.
