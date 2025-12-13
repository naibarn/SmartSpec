# /smartspec_verify_tasks_progress_strict Manual (v6.0, English)

## Overview

The `/smartspec_verify_tasks_progress_strict` workflow is a critical tool for ensuring that tasks defined in a `tasks.md` file are genuinely complete based on verifiable evidence within the codebase, rather than relying solely on manually checked checkboxes.

**Purpose:** Verify progress for a given `tasks.md` using **strict, evidence-only checks**.

**Key Features:**
*   Treats checkboxes as **non-authoritative**.
*   Verifies tasks via explicit evidence hooks (code, test, ui, docs).
*   Produces auditable reports under `.spec/reports/verify-tasks-progress/`.
*   Operates in a **safe-by-default** mode, performing reports-only writes.

**Version:** 6.0.3

## Usage

This workflow is designed to be invoked via the command line (CLI) or through Kilo Code environments.

### CLI Usage

The primary input is the path to the `tasks.md` file you wish to verify.

```bash
/smartspec_verify_tasks_progress_strict <path/to/tasks.md> [--report-format <md|json|both>] [--json]
```

**Example:**

```bash
# Verify the tasks for the 'feature-orders' specification
/smartspec_verify_tasks_progress_strict specs/feature-orders/tasks.md --report-format both
```

### Kilo Code Usage

In environments supporting Kilo Code execution, the invocation is similar, using the `.md` extension for the workflow file.

```bash
/smartspec_verify_tasks_progress_strict.md <path/to/tasks.md> [--report-format <md|json|both>] [--json]
```

**Example:**

```bash
# Verify tasks and output the report exclusively in JSON format
/smartspec_verify_tasks_progress_strict.md specs/v6/tasks.md --report-format json
```

## Use Cases

### Use Case 1: Standard Verification and Report Generation

**Scenario:** A developer needs to verify the completion status of tasks for a new API feature (`api-v2.md`) and generate both a human-readable markdown report and a machine-readable JSON summary.

| Detail | Value |
| :--- | :--- |
| **Tasks File** | `specs/api-v2/tasks.md` |
| **Goal** | Generate full verification report. |

**Command (CLI):**

```bash
/smartspec_verify_tasks_progress_strict specs/api-v2/tasks.md --report-format both
```

**Expected Result:**

1.  Exit code `0`.
2.  A new run folder is created, e.g., `.spec/reports/verify-tasks-progress/20240101-123456/`.
3.  The following files are generated:
    *   `report.md`: Detailed markdown report showing per-task status, confidence, and remediation suggestions.
    *   `summary.json`: JSON file containing structured data on totals and results.
4.  The report highlights tasks lacking evidence hooks or those with evidence pointing to non-existent files.

### Use Case 2: Verification of Specific Documentation Tasks

**Scenario:** A technical writer wants to ensure all documentation tasks in their specification are complete, specifically checking for the existence of files and headings defined in the `docs` evidence hooks. They only need the JSON output for integration with a CI pipeline.

| Detail | Value |
| :--- | :--- |
| **Tasks File** | `specs/docs-migration/tasks.md` |
| **Goal** | Verify documentation progress, output JSON only. |

**Command (Kilo Code):**

```bash
/smartspec_verify_tasks_progress_strict.md specs/docs-migration/tasks.md --report-format json --quiet
```

**Expected Result:**

1.  Exit code `0`.
2.  A run folder is created containing only `summary.json`.
3.  The `summary.json` includes entries where `type: docs` evidence hooks were checked against the file system. Tasks where the specified `path` and `heading` were found are marked `verified: true` with `confidence: high`.
4.  The console output is minimal due to the `--quiet` flag.

### Use Case 3: Handling Invalid Scope and Redaction

**Scenario:** A developer attempts to verify a `tasks.md` file that contains an evidence hook pointing to a file outside the allowed workspace root (e.g., using an absolute path or path traversal `../..`). The system must enforce safety policies.

| Detail | Value |
| :--- | :--- |
| **Tasks File** | `specs/security-audit/tasks.md` |
| **Evidence Hook** | `evidence: code path=../../secrets/config.yaml` |
| **Goal** | Verify safety and report invalid scope. |

**Command (CLI):**

```bash
/smartspec_verify_tasks_progress_strict specs/security-audit/tasks.md
```

**Expected Result:**

1.  Exit code `0` (if other tasks are valid, otherwise `1` if validation fails early).
2.  The report is generated.
3.  The task containing the malicious hook is marked with `status: invalid_scope`.
4.  The report explicitly states that the evidence read was blocked due to path traversal/scope violation, ensuring the workflow adheres to the **Governance contract** and **Evidence read scope** rules.

## Parameters

The workflow accepts the following positional argument and flags:

### Positional Input

| Parameter | Required | Description | Validation |
| :--- | :--- | :--- | :--- |
| `tasks_md` | Yes | Path to the `tasks.md` file to be verified. | Must exist, resolve under `specs/**`, and not escape via symlink. |

### Universal Flags (Standard SmartSpec Flags)

| Flag | Default | Description |
| :--- | :--- | :--- |
| `--config <path>` | `.spec/smartspec.config.yaml` | Path to the SmartSpec configuration file. |
| `--lang <th|en>` | (System default) | Specifies the language for output messages. |
| `--platform <cli|kilo|ci|other>` | (Inferred) | Specifies the execution platform. |
| `--out <path>` | (Internal report path) | Specifies an alternative output directory for reports. Must be within the allowed write scope. |
| `--json` | (None) | Alias for `--report-format json`. Enables JSON output for summary data. |
| `--quiet` | (None) | Suppresses non-essential output to the console. |

### Workflow-Specific Flags

| Flag | Default | Description |
| :--- | :--- | :--- |
| `--report-format <md|json|both>` | `both` | Specifies the format(s) for the generated report files. |

## Output

The workflow is designed to produce auditable reports detailing the verification process and results.

### Output Artifacts

All reports are written under a unique run folder, typically located at:
`.spec/reports/verify-tasks-progress/<run-id>/`

If the `--out <path>` flag is used, reports are written under:
`<out>/<run-id>/`

| File Name | Format | Condition | Description |
| :--- | :--- | :--- | :--- |
| `report.md` | Markdown | When `--report-format` includes `md` or `both`. | A detailed, human-readable report including per-task status, confidence levels, and remediation suggestions. |
| `summary.json` | JSON | When `--report-format` includes `json` or `both`, or when `--json` is used. | A structured, machine-readable summary of the verification results, following the defined schema. |

### Required Content in `report.md`

The markdown report must include:

1.  Target file path and resolved specification ID (`spec-id`).
2.  Summary totals (Verified Done, Not Verified, Missing Hooks, etc.).
3.  Per-task results (ID, title, status, confidence, evidence pointers).
4.  Evidence gaps list with concrete **remediation suggestions** (templates for missing hooks).
5.  Redaction note (if applicable, based on configuration).
6.  Output inventory (list of generated files).
7.  Recommended next steps (e.g., how to sync checkboxes).

## Notes & Related Workflows

### Non-Destructive Operation

This workflow is strictly non-destructive. It **MUST NOT** modify the `tasks.md` file or any source code. It only generates reports.

### Checkbox Synchronization

This workflow verifies *progress* based on evidence. It does not update the checkboxes in `tasks.md`.

To update the checkboxes based on the verification results, use the related workflow:

*   **`/smartspec_sync_tasks_checkboxes`**: Used to safely update the checkbox states in `tasks.md` based on the latest verification status.

**Recommended Next Step:**

If the verification report shows tasks are