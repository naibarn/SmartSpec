# /smartspec_test_suite_runner Manual (v6.0, English)

## Overview

The `/smartspec_test_suite_runner` workflow (Version 6.1.1) is designed to execute a project's existing test suite (e.g., Jest, Vitest, Cypress) defined in `package.json` scripts and generate standardized SmartSpec report artifacts.

**Purpose:** To provide a safe, hardened, and standardized mechanism for running project tests within the SmartSpec governance framework, ensuring results are captured, redacted, and validated against safety constraints.

**Key Characteristics:**
*   **Reports-Only:** The primary output is structured reports (`.md`, `.json`, `.xml`).
*   **Privileged Operation:** Executes external, project-defined scripts.
*   **Safety Focused:** Enforces strict path validation, process isolation, and mandatory timeouts to mitigate risks like arbitrary code execution and workspace pollution.

## Usage

### CLI Usage

The workflow is invoked from the command line, requiring the name of the script defined in your project's `package.json`.

```bash
/smartspec_test_suite_runner \
  --test-script <npm-script-name> \
  [--junit-report-path <relative/path/to/junit.xml>] \
  [--timeout 600] \
  [--allow-network] \
  [--out <output-root>] \
  [--json]
```

### Kilo Code Usage

When integrating into a larger SmartSpec pipeline or using the Kilo interface, the workflow is called as follows:

```bash
/smartspec_test_suite_runner.md \
  --test-script test:unit \
  --junit-report-path .spec/reports/test-suite-runner/_tmp/junit.xml \
  --timeout 600 \
  --out .spec/reports/test-suite-runner \
  --json \
  --kilocode
```

## Use Cases

### Use Case 1: Running Unit Tests with Timeout and Safe Output

**Scenario:** A developer needs to run the project's standard unit test suite (`test:unit`) and ensure the run fails if it takes longer than 5 minutes (300 seconds). The results must be stored in a specific, safe output directory for CI consumption.

| Parameter | Value | Description |
| :--- | :--- | :--- |
| `--test-script` | `test:unit` | Assumes `package.json` contains `"test:unit": "jest --config jest.unit.js"`. |
| `--timeout` | `300` | Sets the wall-clock timeout to 5 minutes. |
| `--out` | `.spec/ci_reports/unit_tests` | Requested base output root (must pass safety checks). |

**CLI Command:**

```bash
/smartspec_test_suite_runner \
  --test-script test:unit \
  --timeout 300 \
  --out .spec/ci_reports/unit_tests
```

**Expected Result:**
1.  **Preflight:** Workflow validates that `test:unit` exists and `.spec/ci_reports/unit_tests` is a safe output path.
2.  **Execution:** The `test:unit` script runs with process isolation and a 300-second timer.
3.  **Artifacts:** Reports (`report.md`, `summary.json`, `stdout.txt`) are generated under a unique run ID within `.spec/ci_reports/unit_tests/`.
4.  **Exit Code:** `0` if all tests pass within the timeout, `1` if tests fail, or `2` if the timeout is reached.

### Use Case 2: Running E2E Tests Requiring Network Access

**Scenario:** The project includes End-to-End (E2E) tests (`test:e2e`) that require outbound network calls (e.g., connecting to a staging API). The default security policy denies network access, so it must be explicitly allowed. A JUnit XML report must be generated for external CI tools.

| Parameter | Value | Description |
| :--- | :--- | :--- |
| `--test-script` | `test:e2e` | Executes the E2E script. |
| `--allow-network` | (Flag) | Explicitly permits outbound network connections. |
| `--junit-report-path` | `e2e_results/junit.xml` | Specifies where the test runner should write the JUnit report. |

**Kilo Code Invocation:**

```bash
/smartspec_test_suite_runner.md \
  --test-script test:e2e \
  --allow-network \
  --junit-report-path e2e_results/junit.xml \
  --kilocode
```

**Expected Result:**
1.  **Safety Check:** TSR-103 notes that network access is explicitly allowed.
2.  **Execution:** The test runner is configured (if possible) to output JUnit XML to the specified path, relative to the run folder.
3.  **Artifacts:** The final report includes the parsed results from `e2e_results/junit.xml`. The `summary.json` explicitly logs `allow_network: true`.

## Parameters

The following parameters and flags are supported by `/smartspec_test_suite_runner`:

### Required Inputs

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `--test-script <name>` | String | **MANDATORY.** The name of the script in `package.json` to execute (e.g., `test`, `test:unit`). Must exist in `package.json`. |

### Workflow-Specific Optional Inputs

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `--junit-report-path <path>` | Path | None | Path where the test runner will write a JUnit XML report. Path must be relative and safe. |
| `--timeout <seconds>` | Integer | 300 | Wall-clock timeout in seconds for the entire test run. |
| `--allow-network` | Flag | False | Explicitly permits outbound network calls from the test process. |

### Universal Flags (Supported)

| Flag | Description | Notes |
| :--- | :--- | :--- |
| `--out <path>` | Requested base output root. Must pass safety validation. | If not provided, defaults to `.spec/reports/test-suite-runner/<run-id>`. |
| `--json` | Output the final report summary in JSON format to stdout. | |
| `--apply` | Accepted for compatibility but **ignored**. | The report header will note that this flag was ignored. |
| `--config <path>` | Path to the SmartSpec configuration file. | |
| `--lang <th|en>` | Language for output messages. | |
| `--platform <cli|kilo|ci|other>` | Execution context platform. | |
| `--quiet` | Suppress non-critical output. | |

## Output

All outputs are written under a unique run folder, typically located at `.spec/reports/test-suite-runner/<run-id>/` unless `--out` is specified and validated.

### Output Artifacts

| Artifact | Format | Description |
| :--- | :--- | :--- |
| `report.md` | Markdown | Human-readable summary including status, failures, slowest tests, and safety checks. |
| `summary.json` | JSON | Structured, machine-readable results conforming to the defined schema. |
| `stdout.txt` | Text | Redacted standard output captured from the test process. |
| `stderr.txt` | Text | Redacted standard error captured from the test process. |
| `junit.xml` | XML | The JUnit report produced by the test runner (if configured and successful). Redactions are applied to sensitive content. |

### Exit Codes

| Code | Meaning | Description |
| :--- | :--- | :--- |
| `0` | Success | All tests passed. |
| `1` | Failure | One or more tests failed, or a strict safety check reported a critical risk (e.g., shell injection attempt). |
| `2` | Usage/Config Error | Invalid input (e.g., `--test-script` missing), configuration error, or the test run timed out (TSR-101). |

## Notes & Related Workflows

### Hardening and Isolation

This workflow enforces significant hardening measures:
1.  **No Arbitrary Commands:** Only scripts defined in `package.json` can be executed.
2.  **No Shell:** Processes are spawned directly without invoking a shell (`sh -c`) to prevent shell injection.
3.  **Isolation:** Environment variables like `CI=1`, `TMPDIR`, and `HOME` are set to temporary locations within the run folder to minimize workspace pollution.

### Network Policy

By default, the test process is denied network access. If your tests require external connectivity, you **must** explicitly use the `--allow-network` flag. If the environment cannot enforce network denial, a warning (`TSR-206`) will be logged.

### Related Workflows

*   