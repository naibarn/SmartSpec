># `/smartspec_generate_implement_prompt.md`

**(Alias: `/kilo`)**

**Generates a comprehensive, context-rich prompt for a specific task, ready for use in AI coding assistants like Cursor or Google Antigravity.**

---

## 1. Summary

This is the central command for the manual, AI-assisted "Vibe Coding" workflow. It acts as a powerful context assembler. You point it to a task, and it intelligently gathers all relevant information—from the `spec.md`, `openapi.yaml`, data models, and even existing source code—to create a perfect, self-contained prompt.

- **What it solves:** It eliminates the tedious and error-prone process of manually copy-pasting context for an AI. It provides the AI with a "complete world view" for the task, dramatically improving the accuracy and quality of the generated code.
- **When to use it:** This is your primary, day-to-day command during development when you are implementing tasks with an AI assistant.

---

## 2. Usage

```bash
/smartspec_generate_implement_prompt.md <tasks_path> --tasks <task_id> [options...]
# Alias
/kilo <tasks_path> --tasks <task_id> [options...]
```

---

## 3. Parameters & Options

### **Primary Argument**

| Name | Type | Required? | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `tasks_path` | `string` | ✅ Yes | The full path to the source `tasks.md` file. | `specs/features/new-login/tasks.md` |

### **Options**

| Option | Value | Default | Description |
| :--- | :--- | :--- | :--- |
| `--tasks` | `<task_id>` | (none) | ✅ **Required.** The ID of the single task you want to generate a prompt for. | `--tasks T004` |
| `--include-files` | `<glob_pattern>` | (auto) | Includes the content of specified files in the context. Supports glob patterns. | `--include-files "src/utils/*.ts"` |
| `--no-related-code` | (flag) | (unset) | Prevents the AI from automatically searching for and including related code snippets from the existing codebase. |

---

## 4. The Prompt Generation Process

When you run this command, the AI performs a deep-context assembly:

1.  **Task Extraction:** It reads the specified task (`--tasks <task_id>`) from `tasks.md`.
2.  **SPEC Context:** It finds the associated `spec.md` and extracts the sections most relevant to the task (e.g., Data Models, API Specification, Business Rules).
3.  **Supporting Document Context:** It automatically finds and includes relevant parts of supporting documents like `openapi.yaml` or `data-model.md`.
4.  **Code Context (Auto):** It searches the codebase for existing files or code snippets that are relevant to the task (e.g., related utility functions, type definitions) and includes them. This can be disabled with `--no-related-code`.
5.  **Explicit File Context:** It includes the full content of any files you specify with `--include-files`.
6.  **Prompt Assembly:** It combines all this context into a single, perfectly formatted Markdown prompt, ready for you to copy.

---

## 5. Detailed Examples

### **Example 1: Generating a Basic Prompt for an API Task**

**Goal:** Generate a prompt to implement the business logic for an API endpoint.

```bash
/kilo specs/services/user-profile/tasks.md --tasks T005
```

**Result:** A detailed prompt is generated in the chat. It will automatically include:
- The description of task `T005`.
- The `API Specification` and `Data Models` sections from `user-profile/spec.md`.
- The contents of `user-profile/openapi.yaml` if it exists.
- Any existing type definitions from `src/types/user.ts` if found.

### **Example 2: Generating a Prompt and Explicitly Including a Utility File**

**Goal:** Generate a prompt for a task that relies on a specific utility function, and you want to make sure the AI sees it.

```bash
/kilo specs/features/new-feature/tasks.md --tasks T021 --include-files "src/utils/string-helpers.ts"
```

**Result:** The generated prompt will be identical to the basic one, but will now also contain the full source code of the `src/utils/string-helpers.ts` file inside a `<file>` block, ensuring the AI knows exactly how to use it.

### **Example 3: Generating a Prompt for a Frontend Component**

**Goal:** Generate a prompt to create a new React component, but prevent the AI from pulling in backend code.

```bash
/kilo specs/frontend/tasks.md --tasks T045 --no-related-code --include-files "src/components/ui/Button.tsx"
```

**Result:** The AI generates a prompt for task `T045`. The `--no-related-code` flag stops it from automatically searching for backend files. Instead, you explicitly provide the `Button.tsx` component as the primary context, guiding the AI to build the new component in a similar style.

---

## 6. How to Use with Cursor / Google Antigravity

This workflow is the same as described in the `/implement_tasks` documentation:

1.  **Generate the Prompt:** Run `/kilo` with the desired task ID.
2.  **Copy the Entire Prompt:** A new file (`implement-prompt-Txxx.md`) is created and its content is displayed. Copy the entire text.
3.  **Paste into your AI Assistant:** Paste the complete prompt into the chat panel of Cursor or Google Antigravity.
4.  **Review and Apply:** The AI will now generate the code with full context. Review its suggestions and apply them.

---

## 7. Troubleshooting

| Problem | Cause | Solution |
| :--- | :--- | :--- |
| **"Task ID not found"** | The task ID is incorrect or doesn't exist in the file. | Check the `tasks.md` file for the correct task ID. Remember, you can only specify one task ID. |
| **Prompt is missing context** | The `spec.md` or other supporting files are missing or in a different directory. | Ensure all related SmartSpec files (`spec.md`, `openapi.yaml`, etc.) are co-located in the same directory as `tasks.md`. |
| **AI generates incorrect code** | The context in the `spec.md` is insufficient, or the auto-included code is misleading. | 1. Improve the detail in the `spec.md`. 2. Use `--no-related-code` to prevent the AI from finding irrelevant code. 3. Use `--include-files` to force the inclusion of the exact files you want the AI to see. |

---

## 8. For the LLM

- **Primary Goal:** To assemble a detailed, context-rich prompt for a single, specific task ID.
- **Key Entities:** `tasks_path`, `--tasks` (required, single ID), `--include-files`, `--no-related-code`.
- **Workflow Position:** This is the **fourth step** (manual path) in the core workflow, used for iterative, human-in-the-loop development.
- **Input Artifacts:** `tasks.md`, `spec.md`, and any other supporting or source code files it can find.
- **Output Artifact:** A natural language text prompt written to a file (`implement-prompt-Txxx.md`) and displayed to the user.


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
