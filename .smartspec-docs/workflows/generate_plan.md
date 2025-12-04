# `/smartspec_generate_plan.md`

**Generates a high-level, phased project plan from a SPEC document.**

---

## 1. Summary

This command takes a completed `spec.md` and creates a strategic, high-level implementation plan (`plan.md`). It breaks the project down into logical phases, estimates timelines, and identifies major milestones.

- **What it solves:** It provides a strategic overview of the project, helping teams understand the development sequence and manage expectations.
- **When to use it:** After the `spec.md` is finalized and you need a strategic roadmap before diving into detailed tasks.

---

## 2. Usage

```bash
/smartspec_generate_plan.md <spec_path>
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

A new file named `plan.md` is created in the same directory as the source `spec.md`.

**Example `plan.md` Structure:**
```markdown
# Implementation Plan: Credit Purchase System

## Phase 1: Core Infrastructure & Backend (Weeks 1-2)
- **Goal:** Establish the database schema and core API endpoints.
- **Milestones:**
  - [ ] Database schema finalized and migrated.
  - [ ] `POST /api/credit/purchase` endpoint functional.

## Phase 2: Frontend Integration (Weeks 3-4)
- **Goal:** Build the user interface for purchasing credits.
- **Milestones:**
  - [ ] Purchase form created.
  - [ ] API connected to the frontend.

## Phase 3: Testing & Deployment (Week 5)
- **Goal:** Ensure quality and release to production.
- **Milestones:**
  - [ ] End-to-end tests passing.
  - [ ] Deployed to production environment.
```

---

## 5. Detailed Examples

### Example 1: Creating a plan for a new backend service

1.  **Prerequisite:** You have a file at `specs/services/user-profile/spec.md`.
2.  **Run the command:**
    ```bash
    /smartspec_generate_plan.md specs/services/user-profile/spec.md
    ```

**Result:** A new file is created at `specs/services/user-profile/plan.md` outlining the phases for building the service.

---

## 6. How to Verify the Result

1.  **Check the file:** Ensure the `plan.md` file has been created in the same directory as the `spec.md`.
2.  **Review the content:** Read the plan to ensure it logically breaks down the project into reasonable phases based on the `spec.md`.

---

## 7. Troubleshooting

| Problem | Cause | Solution |
| :--- | :--- | :--- |
| **File not created** | The source `spec.md` path is incorrect or the file doesn't exist. | Verify the path to the `spec.md` file is correct. |
| **Plan seems illogical** | The source `spec.md` may be incomplete or poorly structured. | Improve the quality and detail of the `spec.md` file and re-run the command. |

---

## 8. For the LLM

- **Primary Goal:** To convert a detailed `spec.md` into a high-level, phased `plan.md`.
- **Key Entities:** `spec_path`.
- **Workflow Position:** This is the **second step** in the SmartSpec workflow, after `generate_spec`.
- **Input Artifact:** `spec.md`.
- **Output Artifact:** `plan.md`.
