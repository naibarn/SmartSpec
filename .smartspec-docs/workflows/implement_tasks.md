# `/smartspec_implement_tasks.md`

**Autonomously implements a set of tasks using an AI agent like Kilo Code.**

---

## 1. Summary

This command is for automated, hands-off implementation. It reads tasks from a `tasks.md` file and executes them using a powerful AI agent. It's best suited for well-defined, boilerplate tasks.

- **What it solves:** It automates the tedious, repetitive parts of coding, freeing up developers to focus on more complex, creative problems.
- **When to use it:** When you have a set of clear, well-defined tasks and want to automate their implementation.

---

## 2. Usage

```bash
/smartspec_implement_tasks.md <tasks_path> [--tasks <task_range>]
```

### Parameters

| Name | Type | Required? | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `tasks_path` | `string` | ✅ Yes | The full path to the source `tasks.md` file. | `specs/features/new-login/tasks.md` |

### Options

| Name | Type | Required? | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `--tasks <task_range>` | `string` | ❌ No | A specific task or range of tasks to implement. If omitted, all tasks will be implemented. | `--tasks T001-T005` or `--tasks T007` |

---

## 3. Input

- A `tasks.md` file.
- The associated `spec.md` file (must be in the same directory).

---

## 4. Output

- **Modified source code:** The agent will directly modify the files in your project to implement the tasks.
- **Updated `tasks.md`:** The checkboxes for completed tasks will be marked as done (`[x]`).
- **Log output:** A real-time log of the agent's progress will be displayed.

---

## 5. Detailed Examples

### Example 1: Implementing all tasks in a file

1.  **Prerequisite:** You have a `tasks.md` file with several unchecked tasks.
2.  **Run the command:**
    ```bash
    /smartspec_implement_tasks.md specs/services/user-profile/tasks.md
    ```

**Result:** The AI agent will start implementing all tasks in the file sequentially.

### Example 2: Implementing a specific range of tasks

1.  **Run the command:**
    ```bash
    /smartspec_implement_tasks.md specs/services/user-profile/tasks.md --tasks T001-T003
    ```

**Result:** The agent will implement only tasks T001, T002, and T003.

---

## 6. How to Verify the Result

1.  **Check the code:** Review the code that the agent has written. Use `git diff` to see the changes.
2.  **Run tests:** Run your project's unit and integration tests to ensure the new code works correctly and hasn't introduced regressions.
3.  **Check `tasks.md`:** Verify that the checkboxes for the implemented tasks have been updated.

---

## 7. Troubleshooting

| Problem | Cause | Solution |
| :--- | :--- | :--- |
| **Agent gets stuck or produces errors** | The task may be too complex, ambiguous, or lack sufficient context in the `spec.md`. | 1. Stop the agent. 2. Improve the detail in the `spec.md` for the problematic task. 3. Re-generate the tasks. 4. Try implementing the task manually using `/smartspec_generate_implement_prompt.md`. |
| **Agent modifies the wrong files** | The project structure might be unconventional or not clearly defined in the `spec.md`. | Add a section to your `spec.md` that describes the project's directory structure. |

---

## 8. For the LLM

- **Primary Goal:** To autonomously execute a list of tasks from a `tasks.md` file.
- **Key Entities:** `tasks_path`, `task_range`.
- **Workflow Position:** This is the **fourth step** (automated path) in the core workflow.
- **Input Artifacts:** `tasks.md`, `spec.md`.
- **Output Artifacts:** Modified source code files and an updated `tasks.md`.
