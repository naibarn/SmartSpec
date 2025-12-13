| manual_name | manual_version | compatible_workflow | compatible_workflow_versions |
|-------------|----------------|---------------------|------------------------------|
| /smartspec_test_report_analyzer Manual (EN) | 6.0 | /smartspec_test_report_analyzer | 6.0.x |

# /smartspec_test_report_analyzer Manual (v6.0, English)

## 1. Overview

The `/smartspec_test_report_analyzer` workflow analyzes test execution reports and provides insights on test coverage and quality.

**Purpose:** Analyze test execution reports, providing insights on coverage, failures, and quality metrics.

**Version:** 6.0  
**Category:** quality-testing

---

## 2. Usage

### 🔗 CLI Usage

```bash
/smartspec_test_report_analyzer \
  <test_report> \
  [--format <junit|tap|json>]
```

### Kilo Code Usage

**Important:** When using Kilo Code, you MUST include `--platform kilo` flag.

```bash
/smartspec_test_report_analyzer.md \
  <test_report> \
  [--format <junit|tap|json>] \
  --platform kilo
```

---

## 3. Use Cases

### Use Case 1: Analyzing JUnit Report (CLI)

**Scenario:** Analyze test results from JUnit report.

**Command:**

```bash
/smartspec_test_report_analyzer test-results/junit.xml \
  --format junit
```

**Expected Result:**

1. Report is analyzed.
2. Insights are generated.
3. Exit code `0` (Success).

### Use Case 2: CI Pipeline Analysis (Kilo Code)

**Scenario:** CI pipeline analyzes test results.

**Command (Kilo Code Snippet):**

```bash
/smartspec_test_report_analyzer.md \
  test-results/report.json \
  --format json \
  --platform kilo
```

**Expected Result:**

1. Analysis performed.
2. Exit code `0` (Success).

### Use Case 3: JSON Output (CLI)

**Scenario:** Structured output for dashboards.

**Command:**

```bash
/smartspec_test_report_analyzer test-results/tap.txt \
  --format tap \
  --json
```

**Expected Result:**

1. Analysis with JSON output.
2. Exit code `0` (Success).

---

## 4. Parameters

### Required Parameters

| Parameter | Type | Description | Validation |
| :--- | :--- | :--- | :--- |
| `<test_report>` | `<path>` | Path to test report file. | Must exist. |

### Universal Flags

| Flag | Description | Default | Platform Support |
| :--- | :--- | :--- | :--- |
| `--platform` | Execution platform. **Required for Kilo Code.** | (Inferred) | `cli` \| `kilo` \| `ci` \| `other` |
| `--json` | Output in JSON format. | `false` | `cli` \| `kilo` \| `ci` \| `other` |

### Workflow-Specific Flags

| Flag | Description | Default | Platform Support |
| :--- | :--- | :--- | :--- |
| `--format` | Report format: `junit`, `tap`, or `json`. | (Auto-detect) | `cli` \| `kilo` \| `ci` \| `other` |

---

## 5. Output

### Output Files

| File Path | Description |
| :--- | :--- |
| `.spec/reports/test-report-analyzer/<run-id>/analysis.md` | Analysis report. |

---

## 6. Notes

- **Platform Flag:** When using Kilo Code, always include `--platform kilo`.

---

**End of Manual**
