# `/smartspec_generate_cursor_prompt.md`

**Generates a list of user-friendly prompts for manual, step-by-step execution in platforms like Cursor and Google Antigravity.**

---

## 1. Summary

This command is the heart of the manual "vibe coding" workflow. It takes technical tasks from your `tasks.md` file and converts them into a series of simple, human-readable prompts. It's designed for a developer who wants to work interactively with an AI assistant, one task at a time.

- **What it solves:** It saves you from having to manually formulate a good prompt for every single task. It provides just enough context for the AI to be helpful without overwhelming it.
- **When to use it:** Use this command when your target platform is **Cursor or Google Antigravity**, or any other platform that relies on a **manual copy-paste workflow**.

---

## 2. Target Platforms & Execution Model

This command is **specifically designed for interactive, manual workflows**.

| Platform | How to Execute the Generated Prompts | Workflow |
| :--- | :--- | :--- |
| **Cursor** | Copy and paste each prompt section, one by one. | Manual, Interactive |
| **Antigravity** | Copy and paste each prompt section, one by one. | Manual, Interactive |

---

## 3. Usage

```bash
/smartspec_generate_cursor_prompt.md <tasks_path> --tasks <task_id_or_range> [options...]
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
| `--tasks` | `<task_id_or_range>` | (none) | ✅ **Required.** The ID of the task(s) you want to generate prompts for. Supports single tasks (`T001`), ranges (`T001-T005`), or comma-separated lists (`T001,T003`). |
| `--cursor` | (flag) | ✅ **Yes** | Optimizes the prompt language and structure for Cursor. This is the default. |
| `--antigravity` | (flag) | (unset) | Optimizes the prompt language and structure for Google Antigravity. |
| `--breakdown` | (flag) | (unset) | Automatically breaks down large tasks (>8 hours) into smaller, more manageable sub-task prompts. |

---

## 5. How Multiple Tasks are Handled

This command bundles all specified tasks into **one single file**, but structures it as a **list of distinct prompts**.

**Example Command:**
```bash
/smartspec_generate_cursor_prompt.md specs/services/user-profile/tasks.md --tasks T001-T003
```

**Resulting Prompt File (`cursor-prompt-T001-T003.md`):**

This single file will contain a list of prompts, clearly separated for easy copying.

```markdown
--- PROMPT FOR TASK T001 ---

# Task T001: Create User Model

**Goal:** Create the Prisma model for the `User`.

**Files to create:**
- `prisma/schema.prisma`

**Instructions:**
1. Add a `User` model to the `schema.prisma` file.
2. Include fields: `id`, `email`, `password`.

---

--- PROMPT FOR TASK T002 ---

# Task T002: Create Database Migration

**Goal:** Generate a new database migration based on the updated schema.

**Instructions:**
1. Run the command `npx prisma migrate dev --name init-user`.

---

--- PROMPT FOR TASK T003 ---

# Task T003: Implement User Service

**Goal:** Create the basic `UserService`.

**Files to create:**
- `src/services/user.service.ts`

**Instructions:**
1. Create a `UserService` class.
2. Add a `createUser` method that takes an email and password.

---
```

**Your Workflow:**
1. Open the generated file.
2. Copy the first prompt (for T001).
3. Paste into Cursor and let it run.
4. Copy the second prompt (for T002).
5. Paste into Cursor and let it run.
6. Continue for all tasks.

---

## 6. Detailed Examples

### **Example 1: Generating Prompts for a Feature**

**Goal:** Get a list of prompts to implement a new feature with Cursor.

```bash
/smartspec_generate_cursor_prompt.md specs/features/new-feature/tasks.md --tasks T021-T025
```

**Result:** A single file `cursor-prompt-T021-T025.md` is created, containing five separate, easy-to-copy prompts.

### **Example 2: Generating Prompts for Antigravity**

**Goal:** Get prompts optimized for Google Antigravity.

```bash
/smartspec_generate_cursor_prompt.md specs/services/auth/tasks.md --tasks T010,T012 --antigravity
```

**Result:** A file `cursor-prompt-T010,T012.md` is created with prompts tailored for Antigravity's style.

---

## 7. Troubleshooting

| Problem | Cause | Solution |
| :--- | :--- | :--- |
| **"Task ID not found"** | The task ID is incorrect. | Check the `tasks.md` file for the correct task ID. |
| **Prompts are too simple** | The task descriptions in `tasks.md` are not detailed enough. | Add more detail to the task descriptions in `tasks.md` to get richer prompts. |
| **AI is confused** | You may have pasted multiple prompts at once. | Ensure you are only copying and pasting one prompt section at a time. |
