# /smartspec_generate_tasks Manual (v6.0, English)

## Overview

The `/smartspec_generate_tasks` workflow is the canonical tool for generating or refining a `tasks.md` file from a source specification (`spec.md`) or plan (`plan.md`).

The primary purpose is to create tasks in a **verification-ready** format, ensuring they include stable IDs, acceptance criteria, and specific evidence hooks. This strict format guarantees compatibility with downstream SmartSpec verification and reporting workflows.

This workflow is **safe-by-default** and requires the `--apply` flag to write changes to the source tree.

* **Workflow Version:** 6.0.2
* **Category:** core
* **Status:** Production Ready

---

## Usage

### CLI

The Command Line Interface (CLI) invocation requires the path to the source specification or plan file.

```bash
/smartspec_generate_tasks <spec_or_plan_md> [--json] [--apply] [universal flags...]
```

**Example (Preview):**
```bash
/smartspec_generate_tasks specs/feature/user-auth/spec.md
```

**Example (Apply changes):**
```bash
/smartspec_generate_tasks specs/feature/user-auth/spec.md --apply
```

### Kilo Code

The Kilo Code invocation is identical to the CLI, often used within CI/CD pipelines or automated SmartSpec environments.

```kilo
/smartspec_generate_tasks.md <spec_or_plan_md> [--json] [--apply] [universal flags...]
```

**Example:**
```kilo
# Generate tasks for a newly approved specification
run /smartspec_generate_tasks.md specs/api/v2/new-endpoint/spec.md --apply
```

---

## Use Cases

### Use Case 1: Initial Task Generation (Preview Mode)

**Scenario:** A new specification, `specs/core/db-migration/spec.md`, has been drafted. The user wants to see the proposed tasks and evidence hooks before committing them.

**Command (CLI):**

```bash
/smartspec_generate_tasks specs/core/db-migration/spec.md
```

**Expected Result:**

1.  The workflow runs and analyzes the specification.
2.  No files under `specs/` are modified (due to the absence of `--apply`).
3.  A detailed report and preview of the generated `tasks.md` are written to the reports directory, e.g., `.spec/reports/generate-tasks/<run-id>/preview/db-migration/tasks.md`.
4.  A summary is printed to the console, including the task counts and a note that the changes were not applied.

### Use Case 2: Refining Existing Tasks (Applying Changes)

**Scenario:** The existing `tasks.md` for `specs/ui/homepage/` needs updating after the `spec.md` was modified (e.g., a new requirement for accessibility was added). The user wants to merge the new tasks non-destructively.

**Command (Kilo Code):**

```kilo
run /smartspec_generate_tasks.md specs/ui/homepage/spec.md --apply
```

**Expected Result:**

1.  The workflow reads the existing `specs/ui/homepage/tasks.md`.
2.  It compares the existing tasks with the newly generated set.
3.  Existing task IDs and completion statuses (`[x]`) are preserved where the task meaning hasn't changed.
4.  New tasks derived from the updated spec are inserted.
5.  The `specs/ui/homepage/tasks.md` file is atomically updated.
6.  The report includes a summary of preserved, updated, and newly added tasks.

### Use Case 3: Secret Detection and Refusal

**Scenario:** A developer accidentally included a placeholder secret (`"API_KEY=sk_test_12345"`) in the `plan.md`. The workflow is configured with a redaction pattern matching `sk_test_`.

**Command (CLI):**

```bash
/smartspec_generate_tasks specs/security/audit/plan.md --apply
```

**Expected Result:**

1.  The workflow detects the pattern match while processing the plan content.
2.  The workflow **refuses** to apply the changes (Exit code `1`).
3.  The report (`report.md`) logs a security warning stating that a potential secret was detected, and the apply operation was blocked as per the hardening requirements.
4.  The preview output redacts the detected secret.

---

## Parameters

### Positional Arguments (Inputs)

| Argument | Required | Description | Validation |
| :--- | :--- | :--- | :--- |
| `<spec_or_plan_md>` | Yes | Path to the source specification (`spec.md`) or plan (`plan.md`). | Must exist, must resolve under `specs/**`, must not escape via symlink. |

### Flags

| Flag | Category | Description | Default |
| :--- | :--- | :--- | :--- |
| `--apply` | Workflow-specific | Enables write operations to the source tree (`specs/**/tasks.md`). **Required for persistent changes.** | Absent |
| `--config <path>` | Universal | Path to the SmartSpec configuration file. | `.spec/smartspec.config.yaml` |
| `--lang <th|en>` | Universal | Specifies the language for generated content/reports. | (Config dependent) |
| `--platform <cli|kilo|ci|other>` | Universal | Contextual platform flag. | (Inferred) |
| `--out <path>` | Universal | Specifies a custom output path for reports/previews. Must be under an allowed path. | `.spec/reports/generate-tasks/<run-id>/` |
| `--json` | Universal | Outputs the final summary in JSON format (`summary.json`). | Absent |
| `--quiet` | Universal | Suppresses non-error console output. | Absent |

---

## Output

The workflow generates several output artifacts, primarily located under the reports directory, and optionally updates the target `tasks.md` file if `--apply` is used.

### Report Artifacts (Always Generated)

All reports are written under: `.spec/reports/generate-tasks/<run-id>/` (or `<out>/<run-id>/`).

| Artifact | Description | Purpose |
| :--- | :--- | :--- |
| `preview/<spec-id>/tasks.md` | The full proposed `tasks.md` file. | Allows review before applying. |
| `diff/<spec-id>.patch` | A best-effort patch file showing changes to the existing `tasks.md`. | Facilitates quick review of modifications. |
| `report.md` | A human-readable summary of the run, including task counts, evidence coverage, and security notes. | Primary audit trail. |
| `summary.json` | A machine-readable summary of the run (if `--json` is used). | Used for CI/CD integration and tracking. |

### Applied Artifacts (Only with `--apply`)

| Artifact | Description | Location |
| :--- | :--- | :--- |
| `tasks.md` | The final, merged, and updated tasks file. | Sibling to the source spec: `specs/<category>/<spec-id>/tasks.md` |

---

## Notes & Related Workflows

### Task Format Contract

The generated `tasks.md` strictly adheres to a machine-verifiable contract, ensuring:
*   **Deterministic Task IDs:** Stable IDs (e.g., `TSK-SPECID-001`) are used for tracking.
*   **Non-destructive Merging:** Existing completed tasks and user notes are preserved during updates.
*   **Evidence Hooks:** Every task must include specific, actionable evidence hooks (Code, Test, UI, Docs) to prove completion.

### Minimum Coverage Policy

The workflow enforces a minimum coverage policy, ensuring that tasks are generated for:
*   Happy path and edge cases.
*   Critical UI states (loading, empty, error, success).
*   Accessibility and at least one test task for critical flows.

### Related Workflows

*   **`/smartspec_verify_tasks_progress_strict`**: Uses the evidence hooks generated here to automatically check implementation progress against the codebase.
*   **`/smartspec_report_implement_prompter`**: Uses the tasks and spec content to generate targeted prompts for implementation assistance.
*   **`/smartspec_quality_gate`**: Relies on the verified status of these tasks to determine if a specification or feature is ready for deployment.

---
*Last updated: SmartSpec v6.0*