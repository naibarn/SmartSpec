# `/smartspec_generate_implement_prompt.md`

**Generates a context-rich prompt for a specific task, ready for use in an AI coding assistant.**

---

## 1. Summary

This is the core command for the "Vibe Coding" workflow. It takes a specific task from `tasks.md` and gathers all relevant context from the `spec.md` to create a high-quality, detailed prompt. This prompt can then be pasted into an AI coding tool like Cursor, VSCode+Claude, or ChatGPT.

- **What it solves:** It eliminates the need to manually copy-paste context. It provides the AI with everything it needs to know (data models, API specs, business rules) to complete the task correctly the first time.
- **When to use it:** This is your main, day-to-day command during development when you are manually implementing tasks with an AI assistant.

---

## 2. Usage

```bash
/smartspec_generate_implement_prompt.md <tasks_path> [--task <task_id>]
```

### Parameters

| Name | Type | Required? | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `tasks_path` | `string` | ✅ Yes | The full path to the source `tasks.md` file. | `specs/features/new-login/tasks.md` |

### Options

| Name | Type | Required? | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `--task <task_id>` | `string` | ✅ Yes | The ID of the task you want to generate a prompt for. | `--task T004` |

---

## 3. Input

- A `tasks.md` file.
- The associated `spec.md` file (must be in the same directory).
- The ID of the task to be implemented.

---

## 4. Output

A context-rich prompt is generated and displayed in the chat. This prompt is designed to be copied and pasted directly into your AI coding tool.

**Example Prompt Output:**

> **Context:**
> 
> You are building a credit purchase system. Here is the relevant context from the `spec.md`:
> 
> **Data Model:**
> - `credits` (id, user_id, amount)
> - `users` (id, name, email)
> 
> **API Specification:**
> - `POST /api/credit/purchase`
>   - Body: `{ userId: string, amount: number }`
> 
> **Business Rules:**
> - Users cannot purchase more than 1,000 credits at a time.
> - A record must be created in the `credit_transactions` table.
> 
> ---
> 
> **Task:**
> 
> Implement the business logic for the `POST /api/credit/purchase` endpoint. This includes:
> 1.  Validating the request body.
> 2.  Checking the business rules (max purchase amount).
> 3.  Updating the user's credit balance.
> 4.  Creating a transaction record.
> 5.  Returning a success response.

---

## 5. Detailed Examples

### Example 1: Generating a prompt for an API endpoint task

1.  **Prerequisite:** You have `tasks.md` with a task `T005: Implement business logic...`.
2.  **Run the command:**
    ```bash
    /smartspec_generate_implement_prompt.md specs/services/user-profile/tasks.md --task T005
    ```

**Result:** A detailed prompt appears in the chat, ready for you to copy into Cursor or your preferred tool.

---

## 6. How to Verify the Result

1.  **Read the prompt:** Ensure the generated prompt contains the correct task and all relevant context from the `spec.md`.
2.  **Use the prompt:** The ultimate test is to use the prompt with your AI assistant. A good prompt should result in high-quality, correct code with minimal need for re-prompting.

---

## 7. Troubleshooting

| Problem | Cause | Solution |
| :--- | :--- | :--- |
| **"Task ID not found"** | The task ID you provided does not exist in the `tasks.md` file. | Check the `tasks.md` file for the correct task ID. |
| **Prompt is missing context** | The `spec.md` file is missing or in a different directory. | Ensure the `spec.md` file is in the same directory as the `tasks.md` file. |
| **AI generates incorrect code** | The context in the `spec.md` may be incorrect or insufficient. | Improve the detail in the `spec.md` and re-generate the prompt. |

---

## 8. For the LLM

- **Primary Goal:** To assemble a detailed, context-rich prompt for a specific task ID.
- **Key Entities:** `tasks_path`, `task_id`.
- **Workflow Position:** This is the **fourth step** (manual path) in the core workflow.
- **Input Artifacts:** `tasks.md`, `spec.md`.
- **Output Artifact:** A natural language text prompt displayed to the user.
