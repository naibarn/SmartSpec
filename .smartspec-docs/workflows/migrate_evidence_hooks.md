# Manual: /smartspec_migrate_evidence_hooks

## 1. Overview

**`/smartspec_migrate_evidence_hooks`** is an AI-powered workflow designed to automate the conversion of descriptive, natural-language evidence in `tasks.md` files into standardized, machine-readable evidence hooks.

This is a critical tool for modernizing legacy SmartSpec projects and enabling automated verification workflows like `/smartspec_verify_tasks_progress_strict`.

## 2. The Problem It Solves

In older `tasks.md` files, the "Evidence" section was often a free-form text field:

```markdown
| **Evidence:** The user model should have a `last_login` field. |
```

This is easy for humans to read but impossible for machines to verify automatically. To solve this, SmartSpec introduced standardized **evidence hooks**:

```markdown
| **Evidence:** evidence: db_schema table=users column=last_login |
```

Manually converting hundreds of these descriptions is tedious and error-prone. This workflow automates that process.

## 3. How It Works

The workflow uses an AI model to intelligently parse the task and its descriptive evidence, then generates a precise evidence hook.

1.  **Parse `tasks.md`:** It reads the specified file and identifies all tasks with descriptive evidence.
2.  **AI Conversion:** For each identified task, it sends the task description and the evidence text to an AI model.
3.  **Generate Hook:** The AI is prompted to choose the best hook format (e.g., `file_exists`, `file_contains`, `api_route`) and generate the corresponding hook.
4.  **Preview or Apply:**
    -   **Preview Mode (Default):** It displays a `diff` of the proposed changes without modifying the file, allowing for a safe review.
    -   **Apply Mode (`--apply`):** It modifies the `tasks.md` file directly, replacing the old descriptions with the new hooks.

## 4. Parameters

| Parameter | Type | Description | Required |
| :--- | :--- | :--- | :--- |
| `--tasks-file` | `string` | The path to the `tasks.md` file to be migrated. | Yes |
| `--apply` | `boolean` | If `true`, applies the changes directly to the file. Defaults to `false` (preview mode). | No |
| `--model` | `string` | The AI model to use for conversion (e.g., `gpt-4.1-mini`). Defaults to `gpt-4.1-mini`. | No |

## 5. Step-by-Step Guide

### Step 1: Run in Preview Mode (Recommended)

Always start with a preview to ensure the AI is generating the correct hooks. This is a safe, read-only operation.

```bash
/smartspec_migrate_evidence_hooks \
  --tasks-file "specs/core/spec-core-001-authentication/tasks.md"
```

Review the output carefully. The `diff` will clearly show the old evidence (`-`) and the proposed new hook (`+`).

```diff
--- a/specs/core/spec-core-001-authentication/tasks.md
+++ b/specs/core/spec-core-001-authentication/tasks.md
@@ -150,7 +150,7 @@
 | TSK-AUTH-020 | Create OpenAPI Specification | The full OpenAPI 3.0 specification for all authentication endpoints. |
-| **Evidence:** The openapi.yaml file should be present in the /docs directory. |
+| **Evidence:** evidence: file_exists path=docs/openapi.yaml |
 --------------------------------------------------------------------------------
```

### Step 2: Review the Suggestions

-   **Are the hooks correct?** Does `file_exists` make sense? Is the path correct?
-   **Is the AI confident?** If the AI is unsure, it may generate a hook like `evidence: file_exists path=MANUAL_REVIEW_REQUIRED`. You will need to fix these manually.
-   **Are there any mistakes?** The AI is powerful but not perfect. Double-check file paths and identifiers.

### Step 3: Apply the Changes

Once you are satisfied with the preview, run the command again with the `--apply` flag. The workflow will wait for 5 seconds, giving you a final chance to cancel (with `Ctrl+C`).

```bash
/smartspec_migrate_evidence_hooks \
  --tasks-file "specs/core/spec-core-001-authentication/tasks.md" \
  --apply
```

After execution, the `tasks.md` file will be updated.

## 6. Supported Evidence Types

The AI is trained to generate the following common hook types:

-   `evidence: file_exists path=<path>`
-   `evidence: file_contains path=<path> content=<text>`
-   `evidence: api_route method=<GET|POST|PUT|DELETE> path=<route>`
-   `evidence: db_schema table=<table_name> [column=<column_name>]`
-   `evidence: gh_commit repo=<repo> sha=<commit_sha>`
-   `evidence: test_exists path=<test_file> name=<test_name>`
-   `evidence: config_key file=<config_file> key=<key_name>`

## 7. Best Practices

-   **Version Control:** Always run this workflow on a clean Git branch, so you can easily review and revert changes.
-   **Run Preview First:** Never run with `--apply` on the first go. The preview is your safety net.
-   **Iterate:** For large files, you can run the migration, manually fix any issues, and then commit the changes.
-   **Combine with Verification:** After migrating, run `/smartspec_verify_tasks_progress_strict` to immediately see the benefits of automated verification.

By using `/smartspec_migrate_evidence_hooks`, you can significantly accelerate the modernization of your projects and unlock the full power of the SmartSpec automated governance ecosystem.
