# /smartspec_security_audit_reporter Manual (v6.0, English)

## Overview

The `/smartspec_security_audit_reporter` workflow is designed to generate a comprehensive security audit report. Its primary function is to correlate identified threats (from `threats.md`) with mitigation tasks (from `tasks.md`), and critically, validate the effectiveness of these mitigations using **strict verification evidence** provided by reports from the `/smartspec_verify_tasks_progress_strict` workflow.

This is a **reports-only** workflow (Version 6.1.1, Category: quality). It is safe to run locally or in Continuous Integration (CI) environments as it does not modify any governed artifacts.

**Dependencies:**
This workflow requires successful execution of:
1. `/smartspec_security_threat_modeler` (generates `threats.md`)
2. `/smartspec_generate_tasks` (generates `tasks.md`)
3. `/smartspec_verify_tasks_progress_strict` (generates verification evidence, typically `summary.json`)

## Usage

### CLI Usage

The workflow is invoked via the command line, requiring the path to the specification file (`spec.md`) as the primary input.

```bash
/smartspec_security_audit_reporter \
  <path/to/spec.md> \
  [--report-format <summary|detailed>] \
  [--verify-summary <path/to/verify-tasks-progress-strict/summary.json>] \
  [--out <output-root>] \
  [--json]
```

### Kilo Code Usage

When integrating into a Kilo Code environment (e.g., within a larger SmartSpec pipeline), the invocation remains similar, typically referencing paths relative to the project root.

```bash
/smartspec_security_audit_reporter.md \
  specs/<category>/<spec-id>/spec.md \
  [--report-format detailed] \
  [--verify-summary .spec/reports/verify-tasks-progress-strict/<run-id>/summary.json] \
  [--out <output-root>] \
  [--json]
```

## Use Cases

### Use Case 1: Standard Audit with Auto-Selected Evidence

**Scenario:** A developer needs a detailed security audit report for a new feature specification (`specs/feature/api/spec.md`). The threat model and verification steps have already been run, and the latest verification report should be used automatically.

**CLI Command:**

```bash
/smartspec_security_audit_reporter specs/feature/api/spec.md --report-format detailed
```

**Workflow Logic:**
1. **Input:** Reads `specs/feature/api/spec.md`.
2. **Implicit Inputs:** Looks for `threats.md` and `tasks.md` in `specs/feature/api/`.
3. **Evidence Selection:** Searches `.spec/reports/verify-tasks-progress-strict/**/summary.json` and selects the latest trusted summary based on the ISO-like run ID pattern.
4. **Processing:** Correlates threats, tasks, and verification evidence. If a threat (e.g., T-001) is linked to a task (TSK-123) and TSK-123 is marked as `verified` with `confidence: high` in the selected summary, T-001 is marked **Mitigated**.
5. **Output:** Generates `report.md` and `summary.json` in a new run folder under `.spec/reports/security-audit/`.

**Expected Result:** A detailed report showing the status of all threats. If all threats are mitigated, the exit code is `0`. If any are unmitigated, the exit code is `1`.

### Use Case 2: Rerunning Audit with Specific Verification Evidence

**Scenario:** The security team needs to generate an audit report using a specific, archived verification run (`20240515-103000Z`) to compare findings against a previous codebase state.

**CLI Command:**

```bash
/smartspec_security_audit_reporter specs/feature/api/spec.md \
  --verify-summary .spec/reports/verify-tasks-progress-strict/20240515-103000Z/summary.json \
  --out .spec/reports/archived_audits
```

**Workflow Logic:**
1. **Evidence Selection:** Uses the path provided by `--verify-summary`. This file must pass the Evidence validation checks (e.g., must contain `workflow: smartspec_verify_tasks_progress_strict`).
2. **Output Root:** Writes the report under the requested output root, provided it passes the Output root safety validation checks.
3. **Processing:** Generates the report based solely on the historical verification data.

**Expected Result:** A report generated in `.spec/reports/archived_audits/<run-id>/` referencing the specific verification run.

### Use Case 3: Failure due to Missing Required Inputs

**Scenario:** The workflow is run on a specification file that exists, but the required companion files (`threats.md` or `tasks.md`) are missing from the same directory.

**CLI Command:**

```bash
/smartspec_security_audit_reporter specs/incomplete/feature/spec.md
```

**Workflow Logic:**
1. **Input Validation:** Checks for the existence of `threats.md` and `tasks.md` next to `spec.md`.
2. **Failure:** If either is missing, the workflow triggers the Input validation failure rule.

**Expected Result:** The workflow hard-fails immediately with exit code `2` (Usage/config error) and outputs a message instructing the user to ensure all required input files are present.

## Parameters

| Parameter/Flag | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `<path/to/spec.md>` | Positional | Yes | N/A | Path to the `spec.md` file. Companion `threats.md` and `tasks.md` must be in the same directory. |
| `--report-format` | String | No | `detailed` | Controls the level of detail in `report.md`. Options: `summary` or `detailed`. |
| `--threats` | Path | No | Auto-select | Optional explicit path to a threat model `threats.md`. If provided, it overrides auto-selection. |
| `--verify-summary` | Path | No | Auto-select | Optional explicit path to a `smartspec_verify_tasks_progress_strict` `summary.json`. If provided, it overrides auto-selection. |
| `--out` | Path | No | `.spec/reports/security-audit/` | Requested base output root. Must pass Output root safety validation. |
| `--json` | Flag | No | False | Outputs the final report structure in JSON format to stdout (in addition to writing `summary.json`). |
| `--config` | Path | No | N/A | Path to the configuration file. |
| `--lang` | String | No | N/A | Language setting for output (`th` or `en`). |
| `--platform` | String | No | N/A | Execution platform context (`cli`, `kilo`, `ci`, `other`). |
| `--apply` | Flag | No | False | Accepted for compatibility but **ignored** (workflow is reports-only). |
| `--quiet` | Flag | No | False | Suppresses non-critical output. |

## Output

The workflow generates output artifacts within a unique run folder to prevent collision, typically located under `.spec/reports/security-audit/<run-id>/`.

**Default Output Root:** `.spec/reports/security-audit/<run-id>/`

| Artifact | Format | Description |
| :--- | :--- | :--- |
| `report.md` | Markdown | The human-readable security audit report, including executive summary, threat status table, and detailed findings for unmitigated threats. |
| `summary.json` | JSON | A machine-readable summary of the audit results, including threat status, counts, scope details, and any generated warnings (`SAR-xxx`). |

### Exit Codes

| Code | Status | Description |
| :--- | :--- | :--- |
| `0` | Success | Audit complete; all threats are determined to be **Mitigated**. |
| `1` | Warning | Audit complete; one or more threats are **Not Mitigated** or **Partially Mitigated**. |
| `2` | Error | Usage or configuration error (e.g., missing inputs, unsafe paths, no trusted evidence found, invalid flag usage). |

## Notes & Related Workflows

### Mitigation Linking Contract
The workflow strictly enforces the mitigation linking contract. Mitigation is only recognized if the task contains a structured field referencing the threat ID:

```markdown
Mitigates: T-001, T-002
```
Threat IDs must match the pattern `T-\d{3}`. References outside this structured field are treated as weak links (`SAR-203`) and do not contribute to the mitigation status.

### Trust Rules
The workflow implements strict trust rules