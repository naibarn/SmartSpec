---
workflow_id: smartspec_migrate_evidence_hooks
version: "6.3.0"
status: active
category: a2ui
platform_support:
  - cli
  - kilo
requires_apply: true
---

# /smartspec_migrate_evidence_hooks

## 1. Description

**Migrates descriptive evidence in a `tasks.md` file to standardized evidence hooks.**

This workflow addresses a critical gap in legacy `tasks.md` files where the "Evidence" section contains natural language descriptions instead of the standardized `evidence: type key=value` format. It uses AI to parse the descriptive text and the task description, then intelligently converts it into a structured evidence hook.

This is a crucial step for enabling automated verification with workflows like `/smartspec_verify_tasks_progress_strict`.

## 2. Why It's Important

-   **Enables Automation:** Standardized hooks are machine-readable, allowing for automated verification of task completion.
-   **Improves Accuracy:** Eliminates the ambiguity of natural language, leading to more reliable progress tracking.
-   **Reduces Manual Effort:** Automates the tedious process of manually converting hundreds of evidence descriptions.
-   **Maintains Consistency:** Enforces a single, consistent format for evidence across all `tasks.md` files.

## 3. How It Works

The workflow operates in two modes: **preview** and **apply**.

1.  **Parsing:** It reads the target `tasks.md` file and identifies all tasks.
2.  **Identification:** For each task, it checks if the "Evidence" section contains free-form text instead of a standardized hook.
3.  **AI-Powered Conversion:** If descriptive evidence is found, it sends the following to an AI model:
    -   The task description
    -   The descriptive evidence text
    -   A prompt asking it to generate the most appropriate `evidence:` hook.
4.  **Suggestion Generation:** The AI returns a suggested evidence hook. The workflow supports common types like `file_exists`, `file_contains`, `api_route`, `db_schema`, `gh_commit`, etc.
5.  **Preview Mode (Default):**
    -   It generates a diff-like output showing the proposed changes for each task.
    -   It does **not** modify the original file.
    -   This allows the user to review the changes before applying them.
6.  **Apply Mode (`--apply`):**
    -   It directly modifies the `tasks.md` file, replacing the descriptive text with the generated evidence hooks.
    -   It is highly recommended to run in preview mode first.

## 4. Parameters

| Parameter | Type | Description | Required |
| :--- | :--- | :--- | :--- |
| `--tasks-file` | `string` | The path to the `tasks.md` file to be migrated. | Yes |
| `--apply` | `boolean` | If `true`, applies the changes directly to the file. Defaults to `false` (preview mode). | No |
| `--model` | `string` | The AI model to use for conversion (e.g., `gpt-4.1-mini`). Defaults to `gpt-4.1-mini`. | No |

## 5. Example Usage

### Preview Changes

This command will analyze the file and show what changes it *would* make without modifying the file.

```bash
/smartspec_migrate_evidence_hooks \
  --tasks-file "specs/core/spec-core-001-authentication/tasks.md"
```

**Example Output (Preview):**

```diff
--- a/specs/core/spec-core-001-authentication/tasks.md
+++ b/specs/core/spec-core-001-authentication/tasks.md
@@ -150,7 +150,7 @@
 | TSK-AUTH-020 | Create OpenAPI Specification | The full OpenAPI 3.0 specification for all authentication endpoints. |
-| **Evidence:** The openapi.yaml file should be present in the /docs directory. |
+| **Evidence:** evidence: file_exists path=docs/openapi.yaml |
 --------------------------------------------------------------------------------
 | TSK-AUTH-021 | Implement User Registration Endpoint | The main /auth/register endpoint should be implemented. |
-| **Evidence:** Check the main router file for the /auth/register route definition. |
+| **Evidence:** evidence: file_contains path=src/routes/auth.ts content=/auth/register |
 --------------------------------------------------------------------------------

```

### Apply Changes

This command will directly modify the `tasks.md` file after a 5-second countdown.

```bash
/smartspec_migrate_evidence_hooks \
  --tasks-file "specs/core/spec-core-001-authentication/tasks.md" \
  --apply
```

## 6. Manual

For more detailed information, please refer to the full manual:
- [English Manual](/.smartspec-docs/workflows/migrate_evidence_hooks.md)
- [Thai Manual](/.smartspec-docs/workflows/migrate_evidence_hooks_th.md)

## 7. Implementation

Implemented in: `.smartspec/scripts/migrate_evidence_hooks.py`
