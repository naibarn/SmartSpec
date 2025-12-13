| manual_name | manual_version | compatible_workflow | compatible_workflow_versions |
|-------------|----------------|---------------------|------------------------------|
| /smartspec_test_suite_runner Manual (EN) | 6.0 | /smartspec_test_suite_runner | 6.0.x |

# /smartspec_test_suite_runner Manual (v6.0, English)

## 1. Overview

The `/smartspec_test_suite_runner` workflow executes test suites based on test plans and specifications.

**Purpose:** Execute test suites based on test plans, running tests and collecting results.

**Version:** 6.0  
**Category:** quality-testing

---

## 2. Usage

### 🔗 CLI Usage

```bash
/smartspec_test_suite_runner \
  <test_plan> \
  [--suite <name>] \
  [--parallel]
```

### Kilo Code Usage

**Important:** When using Kilo Code, you MUST include `--platform kilo` flag.

```bash
/smartspec_test_suite_runner.md \
  <test_plan> \
  [--suite <name>] \
  [--parallel] \
  --platform kilo
```

---

## 3. Use Cases

### Use Case 1: Running Full Test Suite (CLI)

**Scenario:** Execute all tests in test plan.

**Command:**

```bash
/smartspec_test_suite_runner specs/auth/testplan/tests.md
```

**Expected Result:**

1. All tests executed.
2. Results collected.
3. Exit code `0` (Success).

### Use Case 2: Parallel Execution (Kilo Code)

**Scenario:** CI pipeline runs tests in parallel.

**Command (Kilo Code Snippet):**

```bash
/smartspec_test_suite_runner.md \
  specs/api/testplan/tests.md \
  --parallel \
  --platform kilo
```

**Expected Result:**

1. Tests run in parallel.
2. Exit code `0` (Success).

### Use Case 3: Specific Suite (CLI)

**Scenario:** Run specific test suite.

**Command:**

```bash
/smartspec_test_suite_runner specs/payments/testplan/tests.md \
  --suite integration
```

**Expected Result:**

1. Integration suite executed.
2. Exit code `0` (Success).

---

## 4. Parameters

### Required Parameters

| Parameter | Type | Description | Validation |
| :--- | :--- | :--- | :--- |
| `<test_plan>` | `<path>` | Path to test plan file. | Must exist. |

### Universal Flags

| Flag | Description | Default | Platform Support |
| :--- | :--- | :--- | :--- |
| `--platform` | Execution platform. **Required for Kilo Code.** | (Inferred) | `cli` \| `kilo` \| `ci` \| `other` |

### Workflow-Specific Flags

| Flag | Description | Default | Platform Support |
| :--- | :--- | :--- | :--- |
| `--suite` | Specific test suite to run. | (All suites) | `cli` \| `kilo` \| `ci` \| `other` |
| `--parallel` | Enable parallel test execution. | `false` | `cli` \| `kilo` \| `ci` \| `other` |

---

## 5. Output

### Output Files

| File Path | Description |
| :--- | :--- |
| `.spec/reports/test-suite-runner/<run-id>/results.json` | Test execution results. |

---

## 6. Notes

- **Platform Flag:** When using Kilo Code, always include `--platform kilo`.

---

**End of Manual**
