# `/smartspec_implement_tasks.md`

**Autonomously implements a set of tasks using an AI agent, with robust checkpointing, validation, and selective execution.**

---

## 1. Summary

This is the automated workhorse of the SmartSpec framework. It reads a `tasks.md` file and executes the tasks sequentially using a powerful AI agent (like Kilo Code). It's designed for hands-off, autonomous implementation, featuring robust error handling, checkpoint/resume functionality, and post-implementation validation.

- **What it solves:** It automates the tedious, repetitive parts of coding, allowing developers to focus on complex problems. It ensures consistency and quality by running validation (compiling, testing, linting) after each task.
- **When to use it:** When you have a clear, well-defined `tasks.md` and want to automate the implementation, especially for boilerplate code, new endpoints, or data models.

---

## 2. Usage

```bash
/smartspec_implement_tasks.md <tasks_path> [options...]
```

---

## 3. Parameters & Options

### **Primary Argument**

| Name | Type | Required? | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `tasks_path` | `string` | ✅ Yes | The full path to the source `tasks.md` file or the directory containing it. | `specs/features/new-login/tasks.md` |

### **Execution Control Options**

These options allow you to precisely control which tasks are executed.

| Option | Value | Default | Description |
| :--- | :--- | :--- | :--- |
| `--phase` | `1`, `1-3`, `1,3` | (all) | Specifies which phase(s) to implement. | `--phase 2` |
| `--tasks` | `T001`, `T001-T005` | (all) | Specifies a single task or a range of tasks to implement. | `--tasks T001-T005` |
| `--resume` | (flag) | (unset) | Resumes implementation from the last saved checkpoint. | `--resume` |
| `--skip-completed` | (flag) | **set** | Skips any tasks that are already marked as complete (`[x]`). This is the default behavior. |
| `--force-all` | (flag) | (unset) | Ignores all checkboxes and re-implements every task in the selected scope. | `--force-all` |
| `--validate-only` | (flag) | (unset) | Runs the validation steps for each task without implementing any code. Useful for checking the current state of the project. | `--validate-only` |

---

## 4. The Implementation Lifecycle

When you run this command, the AI agent performs a rigorous, multi-step process for each task:

1.  **Scope Filtering:** It first determines the exact list of tasks to run based on your `--phase`, `--tasks`, and mode flags (`--skip-completed`, `--force-all`).
2.  **Pre-flight Validation:** Before starting, it runs all validation commands (compile, test, lint) to ensure the project is in a healthy state.
3.  **Dependency Check:** For each task, it checks if its dependencies (other tasks or SPECs) are complete. If not, the task is skipped.
4.  **Implementation:** It reads the task description and supporting files, then writes the code, following strict file-size-aware strategies to avoid errors.
5.  **Post-task Validation:** After implementing the code, it immediately runs the validation commands again.
6.  **Auto-Fix & Retry:** If validation fails, it attempts to analyze the error and fix the code. It will retry up to two times before marking the task as failed.
7.  **Progress Update:** It updates the checkbox in `tasks.md` (`[ ]` -> `[x]`) for successful tasks.
8.  **Checkpointing:** After each task, it saves a checkpoint (`.smartspec-checkpoint.json`) so you can safely stop and resume later.

---

## 5. Detailed Examples

### **Example 1: Implementing an Entire Phase**

**Goal:** Autonomously implement all pending tasks in Phase 2.

```bash
/smartspec_implement_tasks.md specs/services/user-profile/tasks.md --phase 2
```

**Result:** The agent will execute all tasks under "Phase 2" that are not already marked with `[x]`, validating after each one.

### **Example 2: Resuming a Failed Implementation**

**Goal:** You ran the implementation yesterday, but it failed on task `T015`. You have since fixed the issue and want to continue.

```bash
/smartspec_implement_tasks.md specs/services/user-profile/tasks.md --resume
```

**Result:** The agent reads the `.smartspec-checkpoint.json` file, skips all tasks before `T015`, and resumes the implementation starting from `T015`.

### **Example 3: Re-implementing a Specific Feature**

**Goal:** You are not happy with the implementation of tasks `T010` to `T012`. You want the AI to re-do them from scratch.

```bash
/smartspec_implement_tasks.md specs/services/user-profile/tasks.md --tasks T010-T012 --force-all
```

**Result:** The `--force-all` flag tells the agent to ignore the `[x]` checkboxes for tasks `T010`, `T011`, and `T012` and implement them again.

---

## 6. Using with Cursor / Google Antigravity (Manual Implementation)

While `/implement_tasks` is for full automation, you often need to implement tasks manually with AI assistance. SmartSpec is designed to integrate seamlessly with tools like **Cursor** and **Google Antigravity**.

The key is the `/smartspec_generate_implement_prompt.md` command (or its alias `/kilo`).

### **Workflow:**

1.  **Generate the Prompt:** First, generate a dedicated, context-rich prompt for the task you want to work on.

    ```bash
    /smartspec_generate_implement_prompt.md specs/services/user-profile/tasks.md --tasks T015
    ```

2.  **Copy the Prompt:** This creates a new file like `implement-prompt-T015.md`. Open this file. It contains everything the AI needs to know:
    - The full task description.
    - The relevant sections from `spec.md`.
    - The content of related files (`openapi.yaml`, existing source code).
    - A clear instruction of what to do.

3.  **Paste into Cursor/Antigravity:**
    - In Cursor, open a new chat (`Cmd+K`) or use the inline editor.
    - In Google Antigravity, open the chat panel.
    - **Paste the entire content** of the `implement-prompt-T015.md` file into the chat.

4.  **Let the AI Work:** The AI now has all the necessary context to write the code correctly, referencing the files and requirements you provided. It will suggest code changes directly in your editor.

**Why this is powerful:** You are no longer manually copying and pasting snippets of code and descriptions. You are giving the AI a **complete, self-contained context package**, which dramatically improves the accuracy and quality of its suggestions.

---

## 7. Troubleshooting

| Problem | Cause | Solution |
| :--- | :--- | :--- |
| **Agent gets stuck or produces errors** | The task is too complex, ambiguous, or the `spec.md` lacks context. | Stop the agent. Use the **Cursor/Antigravity workflow** described above to tackle the task manually. This gives you more control. Once done, manually check the task in `tasks.md` and `--resume` the automation. |
| **Agent stops due to validation errors** | The code it wrote has a bug. | The agent will try to self-correct. If it fails after 3 attempts, the process stops. You must manually fix the error (compile error, failing test) and then run the command again with `--resume`. |
| **`--resume` doesn't work** | The `.smartspec-checkpoint.json` file may be deleted or corrupted. | If the checkpoint is gone, you cannot resume. The agent will start from the beginning (but will still skip completed tasks by default). |

---

## 8. For the LLM

- **Primary Goal:** To autonomously execute a list of tasks from a `tasks.md` file, including validation and checkpointing.
- **Key Entities:** `tasks_path`, `--phase`, `--tasks`, `--resume`, `--skip-completed`, `--force-all`, `--validate-only`.
- **Workflow Position:** This is the **fourth step** (automated path) in the core workflow.
- **Input Artifacts:** `tasks.md`, `spec.md`, and any supporting files.
- **Output Artifacts:** Modified source code files and an updated `tasks.md` with completed tasks marked `[x]`.
