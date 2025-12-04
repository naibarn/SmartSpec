# `/smartspec_generate_spec.md`

**Generates a new, comprehensive SPEC document from a high-level idea.**

---

## 1. Summary

This is the starting point for any new project or feature in SmartSpec. It transforms a vague, high-level idea into a structured, detailed, and machine-readable blueprint (`spec.md`). This document becomes the single source of truth for the entire development lifecycle.

- **What it solves:** It prevents ambiguity, ensures all critical aspects (security, performance, data models) are considered upfront, and provides the necessary context for AI agents.
- **When to use it:** At the very beginning of a new project, or when starting a significant new feature.

---

## 2. Usage

```bash
/smartspec_generate_spec.md <spec_path>
```

### Parameters

| Name | Type | Required? | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `spec_path` | `string` | ✅ Yes | The full path where the new `spec.md` file will be created. | `specs/features/new-login/spec.md` |

### Options

This command is interactive and will prompt the user for selections. There are no command-line options in the current version.

---

## 3. Input

This command takes its primary input from the user through a series of interactive prompts in the chat interface.

**The user will be asked for:**
1.  **High-Level Feature Description:** A few sentences describing the feature (e.g., "Build a credit purchase system for a fintech app").
2.  **Profile Selection:** The user will choose a project profile.
3.  **Domain Selection:** The user will choose one or more relevant domains.

---

## 4. Output

The command generates a single, comprehensive Markdown file: `spec.md`.

**Example `spec.md` Structure (using `financial` profile):**
```markdown
# SPEC: Credit Purchase System

## 1. System Overview
...

## 2. Architecture Summary
...

## 3. Data Model
...

## 4. API Specification
...

## 5. Feature Definitions & Use Cases
...

## 6. Business Rules
...

## 7. Security Requirements (STRIDE Analysis)
...

## 8. Performance Requirements
...

## 9. Audit & Logging Requirements
...
```

---

## 5. Detailed Examples

### Example 1: Creating a SPEC for a new backend service

1.  **Run the command:**
    ```bash
    /smartspec_generate_spec.md specs/services/user-profile/spec.md
    ```
2.  **Provide a description:**
    > "Create a backend service to manage user profiles, including creating, reading, updating, and deleting user data. It should also handle profile picture uploads."
3.  **Select a profile:**
    > `backend-service`
4.  **Select a domain:**
    > `internal`

**Result:** A new file is created at `specs/services/user-profile/spec.md` with all the necessary sections for a standard backend service.

---

## 6. How to Verify the Result

1.  **Check the file:** Ensure the `spec.md` file has been created at the specified path.
2.  **Review the content:** Open the file and check that the sections match the profile you selected.
3.  **Check for completeness:** Read through the generated content. While much of it will be boilerplate, ensure it has correctly incorporated your high-level description.

---

## 7. Troubleshooting

| Problem | Cause | Solution |
| :--- | :--- | :--- |
| **File not created** | Incorrect path or permissions issue. | Verify the path is correct and that you have write permissions in the target directory. |
| **SPEC is missing sections** | You may have chosen a profile that is too basic (e.g., `basic`). | Re-run the command and choose a more comprehensive profile like `backend-service` or `full`. |
| **Content is irrelevant** | The initial description was too vague. | Re-run the command with a more detailed and specific feature description. |

---

## 8. For the LLM

- **Primary Goal:** To convert a user's natural language description into a structured `spec.md` file.
- **Key Entities:** `spec_path`, `Profile`, `Domain`.
- **Workflow Position:** This is always the **first step** in the SmartSpec workflow.
- **Output Artifact:** A single Markdown file (`spec.md`) which serves as the input for `/smartspec_generate_plan.md` and `/smartspec_generate_tasks.md`.
