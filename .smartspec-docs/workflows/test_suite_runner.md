_# SmartSpec Workflow: Test Suite Runner

**Workflow:** `/smartspec_test_suite_runner`  
**Version:** 6.1.1

## 1. Overview

The Test Suite Runner executes a project's test suite (e.g., Jest, Vitest, Cypress) and generates a standardized SmartSpec report. It acts as a wrapper around your existing test commands, providing a consistent interface for running tests and capturing results within the SmartSpec ecosystem.

This is a **reports-only** workflow, but it involves a **privileged operation** (running external code). It is designed to be safe, with strict hardening requirements.

## 2. Key Features

- **Standardized Execution:** Provides a single, consistent command to run any test suite.
- **Report Generation:** Produces a standard report, including `summary.json`, `report.md`, `stdout.txt`, `stderr.txt`, and optionally `junit.xml`.
- **Safety First:** Implements robust security hardening, including timeouts, network policies, and workspace isolation.
- **CI/CD Integration:** Ideal for use in CI/CD pipelines to run tests and feed results to other workflows like the `/smartspec_test_report_analyzer`.

## 3. How It Works

1.  **Validates Input:** Checks that the specified `--test-script` exists in `package.json`.
2.  **Spawns Test Process:** Executes the test script using the configured package manager (e.g., `npm run test:unit`) in a sandboxed environment.
3.  **Captures Output:** Streams `stdout` and `stderr` to files.
4.  **Collects Artifacts:** Gathers the JUnit XML report if generated.
5.  **Generates Report:** Creates the final SmartSpec report in the specified output directory.

## 4. Usage

### Command Line

```bash
/smartspec_test_suite_runner \
  --test-script test:e2e \
  --timeout 600 \
  --junit-report-path ./reports/junit.xml
```

### Kilo Code

```bash
/smartspec_test_suite_runner.md \
  --test-script test \
  --out .spec/reports/test-suite-runner/run-abc
```

## 5. Input and Flags

- **`--test-script <name>` (Required):** The name of the script in `package.json` to run.
- **`--timeout <seconds>` (Optional):** Timeout for the test run. Defaults to 300.
- **`--junit-report-path <path>` (Optional):** Path where the test runner should output a JUnit XML report.
- **`--allow-network` (Optional):** Explicitly allows the test suite to make outbound network calls.

## 6. Output: Test Run Report

The workflow generates a run folder in `.spec/reports/test-suite-runner/` containing:

-   `summary.json`: High-level summary of the run (pass/fail, duration, etc.).
-   `report.md`: Human-readable summary.
-   `stdout.txt`: Raw standard output from the test process.
-   `stderr.txt`: Raw standard error output.
-   `junit.xml` (Optional): Standardized test results.

This output is the direct input for the `/smartspec_test_report_analyzer`.

## 7. Use Cases

- **Standardize Test Execution:** Run different types of tests (unit, integration, E2E) with a single, unified workflow.
- **Automate Test Analysis:** Use this workflow as the first step in a chain, followed by the Test Report Analyzer to automatically classify failures.
- **Enforce Quality Gates:** Integrate into your CI pipeline to ensure tests pass before merging or deploying code.
_
