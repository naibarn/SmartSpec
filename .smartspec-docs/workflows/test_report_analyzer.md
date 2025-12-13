# /smartspec_test_report_analyzer Manual (v6.0, English)

## Overview

The `/smartspec_test_report_analyzer` workflow (Version: 6.1.1, Category: quality) is designed to analyze raw test results produced by the `smartspec_test_suite_runner` workflow and generate a high-level diagnostic report.

**Purpose:**

The primary goal is to transform low-level test execution data (logs, JUnit XML) into actionable insights, including:

1.  Classifying failure patterns (e.g., flaky, deterministic assertion failure, infrastructure issue).
2.  Summarizing the top failing test suites and individual test cases.
3.  Extracting actionable follow-ups and suggested next steps (without modifying governed code).
4.  Computing trend-like signals from structured evidence (best-effort).

This workflow is **reports-only** and writes analysis artifacts exclusively under `.spec/reports/test-report-analyzer/**`. It ignores the universal `--apply` flag.

---

## Usage

### CLI Usage

The workflow is invoked via the SmartSpec command-line interface, requiring the path to a single, previously executed `smartspec_test_suite_runner` run folder.

```bash
/smartspec_test_report_analyzer \
  --test-report .spec/reports/test-suite-runner/<run-id> \
  [--mode <normal|strict>] \
  [--max-log-bytes <int>] \
  [--max-junit-bytes <int>] \
  [--max-test-cases <int>] \
  [--out <output-root>] \
  [--json]
```

### Kilo Code Usage

For integration within SmartSpec Kilo Code files, the invocation uses the `.md` extension syntax.

```bash
/smartspec_test_report_analyzer.md \
  --test-report .spec/reports/test-suite-runner/<run-id> \
  --mode normal \
  --out .spec/reports/test-report-analyzer \
  --json \
  --kilocode
```

---

## Use Cases

### Use Case 1: Standard Diagnostic Analysis (CLI)

**Scenario:** A recent CI run failed, and the user wants a quick, high-level diagnosis of the failure root causes without manually sifting through large log files. The runner output is located at `.spec/reports/test-suite-runner/run_20240515_A1B2C3`.

**Command:**

```bash
/smartspec_test_report_analyzer \
  --test-report .spec/reports/test-suite-runner/run_20240515_A1B2C3 \
  --mode normal
```

**Expected Result:**

1.  The workflow validates the input path and the runner's `summary.json` (TRA-000, TRA-001).
2.  It generates a new folder, e.g., `.spec/reports/test-report-analyzer/run_20240515_A1B2C3/`.
3.  The output folder contains `report.md` detailing:
    *   The top 3 failing tests.
    *   A classification that 60% of failures were "flaky hints" due to specific log patterns.
    *   Suggested next steps, such as running `/smartspec_test_flakiness_triage`.
4.  Exit code `0`.

### Use Case 2: Strict Analysis with Bounded Evidence (CLI)

**Scenario:** The test report is extremely large (gigabytes of logs), and the user needs to ensure the analysis is performed quickly and securely, capping the amount of data processed to prevent CI cost spikes. The analysis must fail if evidence is insufficient (`strict` mode).

**Command:**

```bash
/smartspec_test_report_analyzer \
  --test-report .spec/reports/test-suite-runner/large_run_X9Y8Z7 \
  --mode strict \
  --max-log-bytes 1048576 \
  --max-junit-bytes 524288 \
  --max-test-cases 500
```

**Expected Result (Case A: Sufficient Evidence):**

1.  The workflow processes the report, truncating logs and JUnit XML as required (TRA-101, TRA-102).
2.  If the core failure pattern can be identified within the bounds, `report.md` is generated with a warning about reduced confidence (TRA-103).
3.  Exit code `0`.

**Expected Result (Case B: Insufficient Evidence in Strict Mode):**

1.  The workflow processes the report but determines that the truncation (due to `--max-log-bytes`) resulted in the loss of critical stack traces needed for classification.
2.  Since `--mode strict` was used, the workflow fails, indicating insufficient evidence.
3.  Exit code `1`.

### Use Case 3: Kilo Code Integration for Automated Reporting

**Scenario:** An automated Kilo Code pipeline needs to process the latest test run report (`$LAST_RUN_ID`) and output the structured results to a specific, validated location (`$REPORT_OUTPUT`).

**Kilo Code Snippet:**

```markdown
# Process the latest test run
/smartspec_test_report_analyzer.md \
  --test-report .spec/reports/test-suite-runner/$LAST_RUN_ID \
  --mode normal \
  --out $REPORT_OUTPUT \
  --json \
  --kilocode
```

**Expected Result:**

1.  The workflow executes, respecting the configured output root safety checks.
2.  The diagnostic report is written to `$REPORT_OUTPUT/$LAST_RUN_ID/report.md` and the structured summary to `$REPORT_OUTPUT/$LAST_RUN_ID/summary.json`.
3.  The console output includes the full structured JSON summary due to the `--json` flag.
4.  Exit code `0`.

---

## Parameters

The following parameters (flags) are supported by the `/smartspec_test_report_analyzer` workflow.

### Required Workflow-Specific Parameters

| Parameter | Description | Constraints & Validation |
| :--- | :--- | :--- |
| `--test-report <path>` | Path to a **single** `smartspec_test_suite_runner` run folder. | **MANDATORY:** Must resolve under `.spec/reports/test-suite-runner/`. Must pass path/symlink safety and contain required run folder shape (`summary.json`, `report.md`, logs). |

### Optional Workflow-Specific Parameters

| Parameter | Description | Default |
| :--- | :--- | :--- |
| `--mode <normal|strict>` | Defines failure tolerance. `strict` mode can fail (`exit 1`) if evidence is insufficient or untrusted. | `normal` |
| `--max-log-bytes <int>` | Cap bytes read from each of `stdout.txt` and `stderr.txt`. | Config-defined |
| `--max-junit-bytes <int>` | Cap bytes read from `junit.xml`. | Config-defined |
| `--max-test-cases <int>` | Cap total test cases parsed from JUnit to limit memory usage. | Config-defined |

### Universal Flags (Supported)

| Flag | Description | Notes |
| :--- | :--- | :--- |
| `--config <path>` | Path to the configuration file. | Standard SmartSpec configuration. |
| `--lang <th|en>` | Output language preference. | |
| `--platform <cli|kilo|ci|other>` | Execution context platform. | |
| `--out <path>` | Requested base output root for artifacts. | Must pass output root safety checks (TRA-000). |
| `--json` | Output structured results to stdout in JSON format. | |
| `--quiet` | Suppress non-essential output. | |
| `--kilocode` | (Kilo Code only) Indicates execution within a Kilo Code context. | |

### Universal Flags (Ignored)

| Flag | Description | Notes |
| :--- | :--- | :--- |
| `--apply` | Accepted for compatibility but **ignored**. | This workflow is reports-only and never modifies governed artifacts. |

---

## Output

The workflow produces diagnostic artifacts in a dedicated run folder, typically located under `.spec/reports/test-report-analyzer/<run-id>/`. If `--out` is specified, the output root is adjusted accordingly, provided it passes safety checks.

### Output Artifacts

1.  **`report.md`**: The human-readable diagnostic report. It includes the analysis header, trust status, failure classification, top failures, and suggested next steps (registry-backed commands).
2.  **`summary.json`**: A structured, machine-readable summary of the analysis, including scope, limits, input trust details, and detailed failure classification (see schema in workflow file).

### Exit Codes

| Code | Description |
| :--- | :--- |
| `0` | Analysis completed successfully. |
| `1` | Strict-mode