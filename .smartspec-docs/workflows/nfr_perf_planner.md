| manual_name | manual_version | compatible_workflow | compatible_workflow_versions |
|-------------|----------------|---------------------|------------------------------|
| /smartspec_nfr_perf_planner Manual (EN) | 6.0 | /smartspec_nfr_perf_planner | 6.0.x |

# /smartspec_nfr_perf_planner Manual (v6.0, English)

## 1. Overview

The `/smartspec_nfr_perf_planner` workflow generates non-functional requirements (NFR) and performance plans from specifications.

**Purpose:** Generate non-functional requirements (NFR) and performance plans, defining performance targets and testing strategies.

**Version:** 6.0  
**Category:** nfr-performance

---

## 2. Usage

### 🔗 CLI Usage

```bash
/smartspec_nfr_perf_planner \
  <spec_md> \
  [--nfr-type <performance|scalability|reliability>] \
  [--apply]
```

### Kilo Code Usage

**Important:** When using Kilo Code, you MUST include `--platform kilo` flag.

```bash
/smartspec_nfr_perf_planner.md \
  <spec_md> \
  [--nfr-type <performance|scalability|reliability>] \
  [--apply] \
  --platform kilo
```

---

## 3. Use Cases

### Use Case 1: Generating Performance Plan (CLI)

**Scenario:** Generate performance requirements for API.

**Command:**

```bash
/smartspec_nfr_perf_planner specs/api/search_engine/spec.md \
  --nfr-type performance
```

**Expected Result:**

1. Performance NFRs generated.
2. Exit code `0` (Success).

### Use Case 2: Scalability Planning (Kilo Code)

**Scenario:** Plan scalability requirements.

**Command (Kilo Code Snippet):**

```bash
/smartspec_nfr_perf_planner.md \
  specs/system/load_balancer/spec.md \
  --nfr-type scalability \
  --apply \
  --platform kilo
```

**Expected Result:**

1. Scalability plan generated and saved.
2. Exit code `0` (Success).

### Use Case 3: Reliability Requirements (CLI)

**Scenario:** Define reliability NFRs.

**Command:**

```bash
/smartspec_nfr_perf_planner specs/services/payment/spec.md \
  --nfr-type reliability \
  --json
```

**Expected Result:**

1. Reliability NFRs with JSON output.
2. Exit code `0` (Success).

---

## 4. Parameters

### Required Parameters

| Parameter | Type | Description | Validation |
| :--- | :--- | :--- | :--- |
| `<spec_md>` | `<path>` | Path to spec.md file. | Must resolve under `specs/**`. |

### Universal Flags

| Flag | Description | Default | Platform Support |
| :--- | :--- | :--- | :--- |
| `--platform` | Execution platform. **Required for Kilo Code.** | (Inferred) | `cli` \| `kilo` \| `ci` \| `other` |
| `--apply` | Save NFR plan to spec folder. | `false` | `cli` \| `kilo` \| `ci` \| `other` |
| `--json` | Output in JSON format. | `false` | `cli` \| `kilo` \| `ci` \| `other` |

### Workflow-Specific Flags

| Flag | Description | Default | Platform Support |
| :--- | :--- | :--- | :--- |
| `--nfr-type` | NFR type: `performance`, `scalability`, `reliability`. | `performance` | `cli` \| `kilo` \| `ci` \| `other` |

---

## 5. Output

### Output Files

| File Path | Description |
| :--- | :--- |
| `.spec/reports/nfr-perf-planner/<run-id>/nfr_plan.md` | NFR plan. |
| `specs/**/nfr/performance.md` | Saved NFR plan (with `--apply`). |

---

## 6. Notes

- **Platform Flag:** When using Kilo Code, always include `--platform kilo`.

---

**End of Manual**
