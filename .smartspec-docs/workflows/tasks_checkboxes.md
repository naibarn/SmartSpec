| manual_name | manual_version | compatible_workflow | compatible_workflow_versions |
|-------------|----------------|---------------------|------------------------------|
| /smartspec_tasks_checkboxes Manual (EN) | 6.0 | /smartspec_tasks_checkboxes | 6.0.x |

# /smartspec_tasks_checkboxes Manual (v6.0, English)

## 1. Overview

This manual explains how to use the workflow:

The `/smartspec_tasks_checkboxes` workflow synchronizes task checkboxes between tasks.md files and implementation evidence, ensuring accurate task completion tracking.

**Purpose:** Sync task checkboxes in tasks.md based on verified implementation evidence, maintaining accurate task completion status across the project.

**Version:** 6.0  
**Category:** verify

---

## 2. Usage

This workflow supports invocation via the Command Line Interface (CLI) and Kilo Code (internal scripting environment).

### 🔗 CLI Usage

The CLI invocation requires specifying the target tasks.md file.

```bash
/smartspec_tasks_checkboxes \
  <tasks_md> \
  [--apply] \
  [--strict]
```

### Kilo Code Usage

The Kilo Code invocation is identical to the CLI structure, typically used within automated pipelines or internal scripts.

**Important:** When using Kilo Code, you MUST include `--platform kilo` flag.

```bash
/smartspec_tasks_checkboxes.md \
  <tasks_md> \
  [--apply] \
  [--strict] \
  --platform kilo
```

---

## 3. Use Cases

### Use Case 1: Syncing Checkboxes Based on Evidence (CLI)

**Scenario:** A developer has completed several tasks and wants to update the checkboxes based on verified evidence.

**Command:**

```bash
/smartspec_tasks_checkboxes specs/auth/login_service/tasks.md \
  --apply
```

**Expected Result:**

1. The workflow loads `specs/auth/login_service/tasks.md`.
2. It scans for implementation evidence for each task.
3. Checkboxes are updated based on verified evidence.
4. With `--apply`, the updated tasks.md is written.
5. Exit code `0` (Success).

### Use Case 2: Strict Verification Mode (Kilo Code)

**Scenario:** A CI pipeline needs to ensure all checkboxes are backed by parseable evidence hooks.

**Command (Kilo Code Snippet):**

```bash
/smartspec_tasks_checkboxes.md \
  specs/payments/checkout/tasks.md \
  --strict \
  --platform kilo
```

**Expected Result:**

1. The workflow loads the tasks file.
2. It verifies evidence for all checked tasks in strict mode.
3. Any checked task without valid evidence is flagged.
4. A report is generated with verification results.
5. Exit code `0` if all checks pass, `1` if violations found.

### Use Case 3: Preview Mode Without Applying Changes (CLI)

**Scenario:** A team lead wants to see what checkbox changes would be made before applying them.

**Command:**

```bash
/smartspec_tasks_checkboxes specs/dashboard/analytics/tasks.md
```

**Expected Result:**

1. The workflow loads the tasks file.
2. It analyzes evidence and determines checkbox updates.
3. A preview report is generated showing proposed changes.
4. No changes are applied (no `--apply` flag).
5. Exit code `0` (Success).

---

## 4. Parameters

The following parameters and flags control the execution and behavior of the `/smartspec_tasks_checkboxes` workflow.

### Required Parameters

| Parameter | Type | Description | Validation |
| :--- | :--- | :--- | :--- |
| `<tasks_md>` | `<path>` | Path to the tasks.md file. | Must resolve under `specs/**`. |

### Universal Flags

| Flag | Description | Default | Platform Support |
| :--- | :--- | :--- | :--- |
| `--config` | Path to the SmartSpec configuration file. | `.spec/smartspec.config.yaml` | `cli` \| `kilo` \| `ci` \| `other` |
| `--lang` | Language for report generation (e.g., `th`, `en`). | (System default) | `cli` \| `kilo` \| `ci` \| `other` |
| `--platform` | Execution platform context. **Required for Kilo Code.** | (Inferred) | `cli` \| `kilo` \| `ci` \| `other` |
| `--apply` | Enables governed writes (updating tasks.md checkboxes). | `false` | `cli` \| `kilo` \| `ci` \| `other` |
| `--out` | Base path for safe outputs. | `.spec/reports/tasks-checkboxes/` | `cli` \| `kilo` \| `ci` \| `other` |
| `--json` | Output in JSON format. | `false` | `cli` \| `kilo` \| `ci` \| `other` |
| `--quiet` | Suppress standard output logs. | `false` | `cli` \| `kilo` \| `ci` \| `other` |

### Workflow-Specific Flags

| Flag | Description | Default | Platform Support |
| :--- | :--- | :--- | :--- |
| `--strict` | Enable strict evidence verification mode. | `false` | `cli` \| `kilo` \| `ci` \| `other` |

---

## 5. Output

The workflow generates output artifacts according to its configuration.

### Output Files

| File Path | Description |
| :--- | :--- |
| `.spec/reports/tasks-checkboxes/<run-id>/sync_report.md` | Checkbox synchronization report. |
| `specs/**/tasks.md` | Updated tasks file with synchronized checkboxes (only with `--apply`). |

---

## 6. Notes

- **Platform Flag:** When using Kilo Code, always include `--platform kilo` to ensure proper context and logging.
- **Preview Mode:** Without `--apply`, the workflow generates safe previews without modifying tasks.md.
- **Governed Writes:** Use `--apply` flag to enable checkbox updates.
- **Strict Mode:** Use `--strict` to enforce evidence requirements for all checked tasks.
- **Configuration:** The workflow respects settings in `.spec/smartspec.config.yaml`.

---

**End of Manual**
