| manual_name | manual_version | compatible_workflow | compatible_workflow_versions |
|-------------|----------------|---------------------|------------------------------|
| /smartspec_report_implement_prompter Manual (EN) | 6.0 | /smartspec_report_implement_prompter | 6.0.x |

# /smartspec_report_implement_prompter Manual (v6.0, English)

## 1. Overview

This manual explains how to use the workflow:

The `/smartspec_report_implement_prompter` workflow generates implementation prompts and reports based on verified tasks, helping developers understand what needs to be implemented next.

**Purpose:** Generate implementation prompts and reports from verified tasks to guide developers through the implementation process with clear, actionable instructions.

**Version:** 6.0  
**Category:** implementation

---

## 2. Usage

This workflow supports invocation via the Command Line Interface (CLI) and Kilo Code (internal scripting environment).

### 🔗 CLI Usage

The CLI invocation requires specifying the target tasks.md file.

```bash
/smartspec_report_implement_prompter \
  <tasks_md> \
  [--format <markdown|json>] \
  [--filter <pending|all>]
```

### Kilo Code Usage

The Kilo Code invocation is identical to the CLI structure, typically used within automated pipelines or internal scripts.

**Important:** When using Kilo Code, you MUST include `--platform kilo` flag.

```bash
/smartspec_report_implement_prompter.md \
  <tasks_md> \
  [--format <markdown|json>] \
  [--filter <pending|all>] \
  --platform kilo
```

---

## 3. Use Cases

### Use Case 1: Generating Implementation Prompts for Pending Tasks (CLI)

**Scenario:** A developer wants to see what tasks need to be implemented next with detailed prompts.

**Command:**

```bash
/smartspec_report_implement_prompter specs/auth/login_service/tasks.md \
  --filter pending
```

**Expected Result:**

1. The workflow loads `specs/auth/login_service/tasks.md`.
2. It filters for pending (unchecked) tasks.
3. Implementation prompts are generated for each pending task.
4. A report is written to `.spec/reports/implement-prompter/<run-id>/`.
5. Exit code `0` (Success).

### Use Case 2: Generating JSON Report for CI Pipeline (Kilo Code)

**Scenario:** A CI pipeline needs structured implementation data for dashboard display.

**Command (Kilo Code Snippet):**

```bash
/smartspec_report_implement_prompter.md \
  specs/payments/checkout/tasks.md \
  --format json \
  --platform kilo
```

**Expected Result:**

1. The workflow loads the tasks file.
2. Implementation prompts are generated in JSON format.
3. Output includes `prompts.json` with structured data.
4. Exit code `0` (Success).

### Use Case 3: Comprehensive Report for All Tasks (CLI)

**Scenario:** A project manager wants a complete report of all tasks (pending and completed) with implementation details.

**Command:**

```bash
/smartspec_report_implement_prompter specs/dashboard/analytics/tasks.md \
  --filter all \
  --format markdown
```

**Expected Result:**

1. The workflow loads all tasks from the file.
2. Implementation prompts are generated for all tasks.
3. A comprehensive markdown report is created.
4. Exit code `0` (Success).

---

## 4. Parameters

The following parameters and flags control the execution and behavior of the `/smartspec_report_implement_prompter` workflow.

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
| `--out` | Base path for safe outputs. | `.spec/reports/implement-prompter/` | `cli` \| `kilo` \| `ci` \| `other` |
| `--json` | Output in JSON format. | `false` | `cli` \| `kilo` \| `ci` \| `other` |
| `--quiet` | Suppress standard output logs. | `false` | `cli` \| `kilo` \| `ci` \| `other` |

### Workflow-Specific Flags

| Flag | Description | Default | Platform Support |
| :--- | :--- | :--- | :--- |
| `--format` | Output format: `markdown` or `json`. | `markdown` | `cli` \| `kilo` \| `ci` \| `other` |
| `--filter` | Task filter: `pending` or `all`. | `pending` | `cli` \| `kilo` \| `ci` \| `other` |

---

## 5. Output

The workflow generates output artifacts according to its configuration.

### Output Files

| File Path | Description |
| :--- | :--- |
| `.spec/reports/implement-prompter/<run-id>/prompts.md` | Implementation prompts in markdown format. |
| `.spec/reports/implement-prompter/<run-id>/prompts.json` | Implementation prompts in JSON format (if `--format json`). |

---

## 6. Notes

- **Platform Flag:** When using Kilo Code, always include `--platform kilo` to ensure proper context and logging.
- **Task Filtering:** Use `--filter pending` to focus on uncompleted tasks only.
- **Format Options:** Choose between markdown for human reading or JSON for programmatic processing.
- **Configuration:** The workflow respects settings in `.spec/smartspec.config.yaml`.

---

**End of Manual**
