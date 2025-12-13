| manual_name | manual_version | compatible_workflow | compatible_workflow_versions |
|-------------|----------------|---------------------|------------------------------|
| /smartspec_nfr_perf_verifier Manual (EN) | 6.0 | /smartspec_nfr_perf_verifier | 6.0.x |

# /smartspec_nfr_perf_verifier Manual (v6.0, English)

## 1. Overview

The `/smartspec_nfr_perf_verifier` workflow verifies that implementations meet defined non-functional requirements and performance targets.

**Purpose:** Verify that implementations meet defined NFRs and performance targets through testing and measurement.

**Version:** 6.0  
**Category:** nfr-performance

---

## 2. Usage

### 🔗 CLI Usage

```bash
/smartspec_nfr_perf_verifier \
  <nfr_plan> \
  [--test-results <path>] \
  [--strict]
```

### Kilo Code Usage

**Important:** When using Kilo Code, you MUST include `--platform kilo` flag.

```bash
/smartspec_nfr_perf_verifier.md \
  <nfr_plan> \
  [--test-results <path>] \
  [--strict] \
  --platform kilo
```

---

## 3. Use Cases

### Use Case 1: Verifying Performance NFRs (CLI)

**Scenario:** Verify performance against NFR targets.

**Command:**

```bash
/smartspec_nfr_perf_verifier specs/api/search_engine/nfr/performance.md \
  --test-results perf-results/load-test.json
```

**Expected Result:**

1. NFRs verified against test results.
2. Verification report generated.
3. Exit code `0` if met, `1` if failed.

### Use Case 2: Strict Verification (Kilo Code)

**Scenario:** CI pipeline strict NFR verification.

**Command (Kilo Code Snippet):**

```bash
/smartspec_nfr_perf_verifier.md \
  specs/system/load_balancer/nfr/scalability.md \
  --strict \
  --platform kilo
```

**Expected Result:**

1. Strict verification performed.
2. Exit code `0` if all pass, `1` if any fail.

### Use Case 3: JSON Output (CLI)

**Scenario:** Structured verification results.

**Command:**

```bash
/smartspec_nfr_perf_verifier specs/services/payment/nfr/reliability.md \
  --json
```

**Expected Result:**

1. Verification with JSON output.
2. Exit code `0` (Success).

---

## 4. Parameters

### Required Parameters

| Parameter | Type | Description | Validation |
| :--- | :--- | :--- | :--- |
| `<nfr_plan>` | `<path>` | Path to NFR plan file. | Must exist. |

### Universal Flags

| Flag | Description | Default | Platform Support |
| :--- | :--- | :--- | :--- |
| `--platform` | Execution platform. **Required for Kilo Code.** | (Inferred) | `cli` \| `kilo` \| `ci` \| `other` |
| `--json` | Output in JSON format. | `false` | `cli` \| `kilo` \| `ci` \| `other` |

### Workflow-Specific Flags

| Flag | Description | Default | Platform Support |
| :--- | :--- | :--- | :--- |
| `--test-results` | Path to performance test results file. | (Auto-detect) | `cli` \| `kilo` \| `ci` \| `other` |
| `--strict` | Enable strict verification mode. | `false` | `cli` \| `kilo` \| `ci` \| `other` |

---

## 5. Output

### Output Files

| File Path | Description |
| :--- | :--- |
| `.spec/reports/nfr-perf-verifier/<run-id>/verification.md` | Verification report. |

---

## 6. Notes

- **Platform Flag:** When using Kilo Code, always include `--platform kilo`.

---

**End of Manual**
