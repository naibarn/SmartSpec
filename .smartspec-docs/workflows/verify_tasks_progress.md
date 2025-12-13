| manual_name | manual_version | compatible_workflow | compatible_workflow_versions |
|-------------|----------------|---------------------|------------------------------|
| /smartspec_verify_tasks_progress Manual (EN) | 6.0 | /smartspec_verify_tasks_progress | 6.0.x |

# /smartspec_verify_tasks_progress Manual (v6.0, English)

## 1. Overview

This manual explains how to use the workflow:

The `/smartspec_verify_tasks_progress` workflow performs strict evidence-only verification using parseable evidence hooks to validate task completion.

**Purpose:** Strict evidence-only verification using parseable evidence hooks (evidence: type key=value...). Ensures all task completions are backed by verifiable evidence in the codebase.

**Version:** 6.0  
**Category:** verify

---

## 2. Usage

This workflow supports invocation via the Command Line Interface (CLI) and Kilo Code (internal scripting environment).

### 🔗 CLI Usage

The CLI invocation requires specifying the target tasks.md file.

```bash
/smartspec_verify_tasks_progress \
  <tasks_md> \
  [--report-format <markdown|json>] \
  [--strict]
```

### Kilo Code Usage

The Kilo Code invocation is identical to the CLI structure, typically used within automated pipelines or internal scripts.

**Important:** When using Kilo Code, you MUST include `--platform kilo` flag.

```bash
/smartspec_verify_tasks_progress.md \
  <tasks_md> \
  [--report-format <markdown|json>] \
  [--strict] \
  --platform kilo
```

---

## 3. Use Cases

### Use Case 1: Verifying Task Progress with Evidence (CLI)

**Scenario:** A developer wants to verify that all checked tasks have valid evidence in the codebase.

**Command:**

```bash
/smartspec_verify_tasks_progress specs/auth/login_service/tasks.md
```

**Expected Result:**

1. The workflow loads `specs/auth/login_service/tasks.md`.
2. It scans for evidence hooks in the codebase for each checked task.
3. A verification report is generated showing evidence status.
4. Exit code `0` if all verified, `1` if violations found.

### Use Case 2: Strict Verification for CI Pipeline (Kilo Code)

**Scenario:** A CI pipeline requires strict verification where all checked tasks must have parseable evidence.

**Command (Kilo Code Snippet):**

```bash
/smartspec_verify_tasks_progress.md \
  specs/payments/checkout/tasks.md \
  --strict \
  --report-format json \
  --platform kilo
```

**Expected Result:**

1. The workflow loads the tasks file in strict mode.
2. It verifies evidence for all checked tasks.
3. Any checked task without valid evidence causes failure.
4. Output includes `verification.json` with detailed results.
5. Exit code `0` if all pass, `1` if any violations.

### Use Case 3: Markdown Report for Team Review (CLI)

**Scenario:** A team lead wants a human-readable report of task verification for team review.

**Command:**

```bash
/smartspec_verify_tasks_progress specs/dashboard/analytics/tasks.md \
  --report-format markdown
```

**Expected Result:**

1. The workflow loads the tasks file.
2. It verifies evidence for all checked tasks.
3. A markdown report is generated with detailed findings.
4. Exit code `0` (Success).

---

## 4. Parameters

The following parameters and flags control the execution and behavior of the `/smartspec_verify_tasks_progress` workflow.

### Required Parameters

| Parameter | Type | Description | Validation |
| :--- | :--- | :--- | :--- |
| `<tasks_md>` | `<path>` | Path to the tasks.md file to verify. | Must resolve under `specs/**`. |

### Universal Flags

| Flag | Description | Default | Platform Support |
| :--- | :--- | :--- | :--- |
| `--config` | Path to the SmartSpec configuration file. | `.spec/smartspec.config.yaml` | `cli` \| `kilo` \| `ci` \| `other` |
| `--lang` | Language for report generation (e.g., `th`, `en`). | (System default) | `cli` \| `kilo` \| `ci` \| `other` |
| `--platform` | Execution platform context. **Required for Kilo Code.** | (Inferred) | `cli` \| `kilo` \| `ci` \| `other` |
| `--out` | Base path for safe outputs. | `.spec/reports/verify-tasks-progress/` | `cli` \| `kilo` \| `ci` \| `other` |
| `--json` | Output in JSON format. | `false` | `cli` \| `kilo` \| `ci` \| `other` |
| `--quiet` | Suppress standard output logs. | `false` | `cli` \| `kilo` \| `ci` \| `other` |

### Workflow-Specific Flags

| Flag | Description | Default | Platform Support |
| :--- | :--- | :--- | :--- |
| `--report-format` | Report format: `markdown` or `json`. | `markdown` | `cli` \| `kilo` \| `ci` \| `other` |
| `--strict` | Enable strict verification mode (fail on missing evidence). | `false` | `cli` \| `kilo` \| `ci` \| `other` |

---

## 5. Output

The workflow generates output artifacts according to its configuration.

### Output Files

| File Path | Description |
| :--- | :--- |
| `.spec/reports/verify-tasks-progress/<run-id>/verification.md` | Verification report in markdown format. |
| `.spec/reports/verify-tasks-progress/<run-id>/verification.json` | Verification report in JSON format (if `--report-format json`). |

---

## 6. Notes

- **Platform Flag:** When using Kilo Code, always include `--platform kilo` to ensure proper context and logging.
- **Evidence Hooks:** Tasks must include parseable evidence hooks (e.g., `evidence: file path=src/auth.ts`) for verification.
- **Strict Mode:** Use `--strict` to fail the workflow if any checked task lacks valid evidence.
- **Report Formats:** Choose between markdown for human reading or JSON for programmatic processing.
- **Configuration:** The workflow respects settings in `.spec/smartspec.config.yaml`.

---

**End of Manual**
