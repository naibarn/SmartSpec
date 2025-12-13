# /smartspec_ci_quality_gate Manual (v6.0, English)

## Overview

The `/smartspec_quality_gate` workflow (Version 6.0.0) is a consolidated, production-ready quality gate designed to replace the legacy workflows: `smartspec_ci_quality_gate` and `smartspec_release_readiness`.

**Purpose:** To perform comprehensive quality checks against SmartSpec governance contracts, configuration, and artifacts. It is a read-only workflow that produces **reports only**, making it safe to run in Continuous Integration (CI) environments or locally.

**Key Features:**

*   **Profiles:** Supports two primary modes: `ci` (fast, early-stage checks) and `release` (deep, readiness-focused checks).
*   **Safety:** Enforces strict write scopes, network denial, and secret redaction to adhere to the SmartSpec threat model.
*   **Scoping:** Can run globally (repo-wide) or be scoped to a single specification (`--spec` or `--spec-id`).

## Usage

### CLI Usage

The workflow is invoked directly using the command line interface.

```bash
/smartspec_quality_gate \
  --profile <ci|release> \
  [--spec <path/to/spec.md>|--spec-id <id>] \
  [--out <output-root>] \
  [--json] \
  [--strict]
```

### Kilo Code Usage

When integrating this workflow into other SmartSpec workflows or Kilo Code pipelines, use the `.md` extension for invocation:

```bash
/smartspec_quality_gate.md \
  --profile <ci|release> \
  [--spec <path/to/spec.md>|--spec-id <id>] \
  [--out <output-root>] \
  [--json] \
  [--strict]
```

## Use Cases

### Use Case 1: Fast CI Quality Check (CLI)

**Scenario:** A developer wants to run a quick quality check on a newly created specification (`specs/feature/new_api.md`) before merging the branch. The check should prioritize speed and configuration sanity.

**Command:**

```bash
/smartspec_quality_gate \
  --profile ci \
  --spec specs/feature/new_api.md \
  --strict \
  --json
```

**Expected Result:**

1.  A report is generated under `.spec/reports/quality-gate/ci/<run-id>/` (e.g., `report.md`).
2.  A machine-readable summary is created at `summary.json` in the run directory.
3.  The workflow checks for configuration sanity (e.g., `network_policy.default=deny`).
4.  If any MUST requirement fails (e.g., missing evidence discipline check), the exit code is `1` (fail) due to the `--strict` flag.

### Use Case 2: Release Readiness Audit (Kilo Code)

**Scenario:** A release pipeline needs to ensure all governance and security requirements are met for the entire repository before deployment.

**Kilo Code Snippet:**

```kilo
# Run the release profile globally
run: /smartspec_quality_gate.md
  --profile release
  --out ./release_audit_results
  --strict
```

**Expected Result:**

1.  The workflow runs globally, checking all specs and governance artifacts.
2.  Output reports are written to `./release_audit_results/release/<run-id>/...`.
3.  The workflow performs deep checks, including verifying the existence of Security Evidence Audit reports and NFR/Perf plans for relevant features.
4.  If the check fails, the `report.md` will contain recommended next steps, such as running `/smartspec_security_evidence_audit`.

### Use Case 3: Global Non-Strict Check with Custom Output (CLI)

**Scenario:** A user wants to perform a general health check on the repository, allowing warnings but capturing the output in a specific temporary directory.

**Command:**

```bash
/smartspec_quality_gate \
  --profile ci \
  --out /tmp/qg_scan_results
```

**Expected Result:**

1.  The workflow runs globally (no `--spec` or `--spec-id`).
2.  Output reports are written to `/tmp/qg_scan_results/ci/<run-id>/...`.
3.  The workflow will exit with code `0` (pass) even if SHOULD checks fail, as long as no MUST checks fail, because `--strict` was not provided.

## Parameters

The `/smartspec_quality_gate` workflow supports universal flags and workflow-specific flags.

| Flag | Category | Required | Description |
| :--- | :--- | :--- | :--- |
| `--profile <ci|release>` | Workflow-Specific | Yes | Defines the set of checks to run. `ci` is fast, `release` is comprehensive. |
| `--spec <path>` | Workflow-Specific | No | Scopes the quality check to a single specification file path (e.g., `specs/feature/api.md`). |
| `--spec-id <id>` | Workflow-Specific | No | Scopes the quality check using a specification ID (resolved via `.spec/SPEC_INDEX.json`). |
| `--strict` | Workflow-Specific | No | If present, the workflow fails the gate on any unmet MUST requirement (exit code 1). |
| `--config <path>` | Universal | No | Path to the SmartSpec configuration file (Default: `.spec/smartspec.config.yaml`). |
| `--lang <th|en>` | Universal | No | Language for report generation. |
| `--platform <cli|kilo|ci|other>` | Universal | No | Contextual platform identifier. |
| `--apply` | Universal | No | Accepted for contract compatibility, but **ignored** (no effect on write scopes). |
| `--out <path>` | Universal | No | Base directory for output reports. |
| `--json` | Universal | No | Generates a machine-readable `summary.json` file. |
| `--quiet` | Universal | No | Suppresses non-critical console output. |

**Input Validation Notes:**

*   Providing both `--spec` and `--spec-id` results in a hard failure (exit code 2).
*   The `--out` path must be a directory, resolve under the config allowlist, and not escape via symlink or resolve under any denylist path.

## Output

The workflow produces reports only, written under a unique run folder (`<run-id>`) within the chosen output root.

### Output Root Selection

| Condition | Output Path Structure |
| :--- | :--- |
| `--out` provided | `<out>/<profile>/<run-id>/` |
| `--out` not provided | `.spec/reports/quality-gate/<profile>/<run-id>/` |

### Artifacts

| Artifact | Description | Condition |
| :--- | :--- | :--- |
| `report.md` | The human-readable quality gate report, including rationale, status, and recommended next steps. | Always generated (unless write safety blocks it). |
| `summary.json` | The machine-readable summary of the run, adhering to the defined schema. | Generated if `--json` is specified. |
| `artifacts/*` | Optional supporting files (e.g., redacted configuration excerpts). | Dependent on specific checks. |

### Exit Codes

| Code | Status | Description |
| :--- | :--- | :--- |
| `0` | Pass | All checks passed, or only warnings were raised (when not in `--strict` mode). |
| `1` | Fail | A MUST requirement failed, or the gate failed due to `--strict` mode. |
| `2` | Usage Error | Invalid flags, invalid paths, or configuration errors (e.g., missing registry files). |

## Notes & Related Workflows

### Universal Flag Behavior

The universal flag `--apply` is accepted for contract compliance but has **no effect** on this workflow, as it is strictly read-only and governed by hard write scope restrictions. The report will note that `--apply` was ignored.

### Deprecation Mapping

This workflow is the consolidated replacement for v5 workflows:

*   `smartspec_ci_quality_gate` is replaced by `/smartspec_quality_gate --profile=ci`.
*   `smartspec_release_readiness` is replaced by `/smartspec_quality_gate --profile=release`.

### Recommended Next Steps

The `report.md` and `summary.json` will often suggest running other SmartSpec workflows to address identified gaps, such as:

*   `/smartspec_verify_tasks_progress_strict` (when scoped and tasks exist)
*   `/smartspec_security_evidence_audit` (for release profile gaps)
*   `/smartspec_nfr_perf_planner` (when performance evidence is missing)

---
*Last updated: SmartSpec v6.0*