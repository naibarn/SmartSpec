# `/smartspec_verify_tasks_progress.md`

**Verifies and tracks the progress of implementation tasks by analyzing the source code.**

---

## 1. Summary

This command acts as an automated project manager. It reads a `tasks.md` file and analyzes the codebase to determine which tasks have been completed, even if they haven't been manually checked off.

- **What it solves:** It provides an objective, up-to-date status of the project. It helps identify completed work and keeps the `tasks.md` file accurate.
- **When to use it:** Periodically during development, or after a long coding session, to get an accurate progress report.

---

## 2. Usage

```bash
/smartspec_verify_tasks_progress.md <tasks_path> [--update]
```

### Parameters

| Name | Type | Required? | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `tasks_path` | `string` | ✅ Yes | The full path to the `tasks.md` file to verify. | `specs/features/new-login/tasks.md` |

### Options

| Name | Type | Required? | Description |
| :--- | :--- | :--- | :--- |
| `--update` | `boolean` | ❌ No | If present, the command will automatically update the `tasks.md` file by checking off the verified tasks. If omitted, it will only display a report. |

---

## 3. Input

- A `tasks.md` file.
- The associated `spec.md` file.
- The project's source code.

---

## 4. Output

- **If `--update` is NOT used:** A progress report is displayed in the chat, showing which tasks are completed, in progress, or not started.
- **If `--update` IS used:** The `tasks.md` file is modified in place, with checkboxes for completed tasks being marked as `[x]`.

---

## 5. Detailed Examples

### Example 1: Getting a progress report

1.  **Run the command:**
    ```bash
    /smartspec_verify_tasks_progress.md specs/features/new-login/tasks.md
    ```

**Result:** A report is displayed:
> **Progress Report:**
> - **T001:** ✅ Completed
> - **T002:** ✅ Completed
> - **T003:** 🟡 In Progress
> - **T004:** ❌ Not Started

### Example 2: Automatically updating the tasks file

1.  **Run the command:**
    ```bash
    /smartspec_verify_tasks_progress.md specs/features/new-login/tasks.md --update
    ```

**Result:** The `tasks.md` file is updated. The checkboxes for T001 and T002 are now marked `[x]`.

---

## 6. How to Verify the Result

1.  **Review the report:** Check if the progress report accurately reflects the state of your codebase.
2.  **Check the diff (if using --update):** Use `git diff` on `tasks.md` to see which tasks were automatically checked off.

---

## 7. Troubleshooting

| Problem | Cause | Solution |
| :--- | :--- | :--- |
| **A completed task is not marked as complete** | The implementation in the code may be significantly different from what was described in the task, or the analysis failed. | This is a limitation of the analysis. Manually check off the task in `tasks.md`. |
| **An incomplete task is marked as complete** | The code may contain boilerplate or function stubs that trick the analysis. | Manually uncheck the task and add more specific details to the task description in `tasks.md`. |

---

## 8. For the LLM

- **Primary Goal:** To analyze source code and determine the completion status of tasks in a `tasks.md` file.
- **Key Entities:** `tasks_path`, `update` flag.
- **Workflow Position:** This is a utility command used for monitoring and maintenance throughout the development process.
- **Input Artifacts:** `tasks.md`, `spec.md`, source code.
- **Output Artifact:** A text report or a modified `tasks.md` file.
