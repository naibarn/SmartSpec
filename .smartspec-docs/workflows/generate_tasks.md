# `/smartspec_generate_tasks.md`

**Breaks down a SPEC document into a detailed, actionable `tasks.md` checklist.**

---

## 1. Summary

This command transforms a high-level `spec.md` into a granular, developer-ready checklist of tasks. Each task is small, specific, and ready for implementation.

- **What it solves:** It bridges the gap between high-level planning and day-to-day coding. It creates a clear, actionable to-do list for developers and AI agents.
- **When to use it:** After the `spec.md` is ready and you want to start coding.

---

## 2. Usage

```bash
/smartspec_generate_tasks.md <spec_path>
```

### Parameters

| Name | Type | Required? | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `spec_path` | `string` | ✅ Yes | The full path to the source `spec.md` file. | `specs/features/new-login/spec.md` |

### Options

There are no command-line options in the current version.

---

## 3. Input

- A completed `spec.md` file.

---

## 4. Output

A new file named `tasks.md` is created in the same directory as the source `spec.md`.

**Example `tasks.md` Structure:**
```markdown
# Implementation Tasks: Credit Purchase System

## Phase 1: Core Infrastructure & Backend

### Epic: Database Setup
- [ ] **T001:** Create `credits` table with fields: `id`, `user_id`, `amount`, `purchase_date`.
- [ ] **T002:** Create `credit_transactions` table.

### Epic: API Endpoint
- [ ] **T003:** Create `POST /api/credit/purchase` endpoint route.
- [ ] **T004:** Implement request validation for the endpoint.
- [ ] **T005:** Implement business logic to add credits to user account.
```

---

## 5. Detailed Examples

### Example 1: Creating tasks for a new backend service

1.  **Prerequisite:** You have a file at `specs/services/user-profile/spec.md`.
2.  **Run the command:**
    ```bash
    /smartspec_generate_tasks.md specs/services/user-profile/spec.md
    ```

**Result:** A new file is created at `specs/services/user-profile/tasks.md` with a detailed checklist of tasks to build the service.

---

## 6. How to Verify the Result

1.  **Check the file:** Ensure the `tasks.md` file has been created.
2.  **Review the content:** Read the tasks to ensure they are logical, granular, and accurately reflect the requirements in the `spec.md`.

---

## 7. Troubleshooting

| Problem | Cause | Solution |
| :--- | :--- | :--- |
| **File not created** | The source `spec.md` path is incorrect. | Verify the path to the `spec.md` file. |
| **Tasks are too high-level** | The source `spec.md` lacks sufficient detail. | Add more specific details to the `Data Model`, `API Specification`, and `Business Rules` sections of your `spec.md` and re-run. |

---

## 8. For the LLM

- **Primary Goal:** To convert a `spec.md` into a checklist of small, actionable tasks in `tasks.md`.
- **Key Entities:** `spec_path`.
- **Workflow Position:** This is the **third step** in the core workflow.
- **Input Artifact:** `spec.md`.
- **Output Artifact:** `tasks.md`, which is the input for `/smartspec_generate_implement_prompt.md` and `/smartspec_implement_tasks.md`.
