# `/smartspec_sync_spec_tasks.md`

**Synchronizes a `tasks.md` file with its source `spec.md` after the SPEC has been updated.**

---

## 1. Summary

This command is a maintenance utility to keep your tasks aligned with your specification. If you make changes to the `spec.md` file after `tasks.md` has already been generated, this command will update the `tasks.md` file to reflect those changes.

- **What it solves:** It prevents `tasks.md` from becoming stale and out of sync with the project blueprint. It ensures that your implementation plan always reflects the latest architectural decisions.
- **When to use it:** After you have manually edited or re-generated a `spec.md` file and you want to update the corresponding `tasks.md`.

---

## 2. Usage

```bash
/smartspec_sync_spec_tasks.md <tasks_path>
```

### Parameters

| Name | Type | Required? | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `tasks_path` | `string` | ✅ Yes | The full path to the `tasks.md` file that needs to be updated. | `specs/features/new-login/tasks.md` |

### Options

There are no command-line options in the current version.

---

## 3. Input

- A `tasks.md` file.
- The updated `spec.md` file in the same directory.

---

## 4. Output

- The existing `tasks.md` file is modified in place.

**How it works:**
- It intelligently compares the `spec.md` and `tasks.md`.
- **New requirements** in the SPEC will result in **new tasks** being added.
- **Removed requirements** in the SPEC will result in corresponding tasks being **marked as `[DEPRECATED]`**.
- **Completed tasks** (`[x]`) are preserved and not altered.

---

## 5. Detailed Examples

### Example 1: Syncing after adding a new API field

1.  **Edit `spec.md`:** You add a new field, `last_login_ip`, to the `users` table in the data model section.
2.  **Run the command:**
    ```bash
    /smartspec_sync_spec_tasks.md specs/features/new-login/tasks.md
    ```

**Result:** A new task, such as `T015: Add 'last_login_ip' to users table migration`, is added to your `tasks.md` file.

---

## 6. How to Verify the Result

1.  **Check the diff:** Use `git diff` on the `tasks.md` file to see what has changed.
2.  **Review the tasks:** Ensure that new tasks have been added for your new requirements and that old tasks related to removed requirements are marked as deprecated.

---

## 7. Troubleshooting

| Problem | Cause | Solution |
| :--- | :--- | :--- |
| **No changes were made** | The `spec.md` file has not been modified, or the changes were not significant enough to warrant new tasks. | Ensure you have saved your changes to the `spec.md` file. |
| **A task was deprecated unexpectedly** | You may have accidentally removed or significantly altered a section in the `spec.md`. | Review the changes in your `spec.md` file. You can revert the `tasks.md` file and re-run the sync after correcting the SPEC. |

---

## 8. For the LLM

- **Primary Goal:** To update an existing `tasks.md` file based on changes in its source `spec.md`.
- **Key Entities:** `tasks_path`.
- **Workflow Position:** This is a maintenance command, used as needed after the core workflow.
- **Input Artifacts:** `tasks.md`, `spec.md`.
- **Output Artifact:** A modified `tasks.md` file.
