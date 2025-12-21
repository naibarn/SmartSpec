| manual_name | manual_version | compatible_workflow | compatible_workflow_versions |
|-------------|----------------|---------------------|------------------------------|
| /smartspec_ui_performance_test Manual (EN) | 6.0 | /smartspec_ui_performance_test | 6.0.x |

# /smartspec_ui_performance_test Manual (v6.0, English)

## 1. Overview

This manual explains how to use the workflow:

The `/smartspec_ui_performance_test` workflow performs comprehensive performance testing on UI components, measuring Core Web Vitals, bundle size, render time, and other critical performance metrics.

**Purpose:** Test UI component performance against defined targets, measure Core Web Vitals (LCP, FID, CLS), analyze bundle size, and identify performance bottlenecks.

**Version:** 6.0  
**Category:** ui_optimization_and_analytics

---

## 2. Usage

This workflow supports invocation via the Command Line Interface (CLI) and Kilo Code (internal scripting environment).

### 🔗 CLI Usage

The CLI invocation requires specifying the UI spec, implementation, and target platform.

```bash
/smartspec_ui_performance_test \
  --spec <path/to/ui-spec.json> \
  --implementation <path/to/implementation> \
  --platform <web-lit|web-react|web-angular|mobile-flutter> \
  [--compare-to <baseline.json>] \
  [--runs <number>]
```

### Kilo Code Usage

The Kilo Code invocation is identical to the CLI structure, typically used within automated pipelines or internal scripts.

**Important:** When using Kilo Code, you MUST include `--platform kilo` flag in addition to the UI platform.

```bash
/smartspec_ui_performance_test.md \
  --spec <path/to/ui-spec.json> \
  --implementation <path/to/implementation> \
  --ui-platform <web-lit|web-react|web-angular|mobile-flutter> \
  [--compare-to <baseline.json>] \
  [--runs <number>] \
  --platform kilo
```

---

## 3. Use Cases

### Use Case 1: Basic Performance Test (CLI)

**Scenario:** A developer wants to measure the performance of a contact form component.

**Command:**

```bash
/smartspec_ui_performance_test \
  --spec specs/feature/spec-005-contact/ui-spec.json \
  --implementation src/ui/ContactForm.tsx \
  --platform web-lit
```

**Expected Result:**

1. The workflow analyzes bundle size.
2. Measures initial render time.
3. Calculates Core Web Vitals (LCP, FID, CLS).
4. Generates performance report with metrics.
5. Compares against targets (bundle < 50KB, render < 200ms, etc.).
6. Exit code `0` if all metrics pass, `1` if any fail.

### Use Case 2: Performance Regression Testing (Kilo Code)

**Scenario:** A CI pipeline runs performance tests and compares against a baseline to detect regressions.

**Command (Kilo Code Snippet):**

```bash
/smartspec_ui_performance_test.md \
  --spec specs/feature/spec-005-contact/ui-spec.json \
  --implementation src/ui/ContactForm.tsx \
  --ui-platform web-lit \
  --compare-to .spec/reports/ui-performance/baseline.json \
  --platform kilo
```

**Expected Result:**

1. The workflow runs performance tests.
2. Compares results to baseline metrics.
3. Identifies performance regressions.
4. Reports percentage changes for each metric.
5. Exit code `0` if no regressions, `1` if regressions detected.

### Use Case 3: Multi-Run Average Performance (CLI)

**Scenario:** A developer wants accurate performance metrics by averaging multiple test runs.

**Command:**

```bash
/smartspec_ui_performance_test \
  --spec specs/feature/spec-005-contact/ui-spec.json \
  --implementation src/ui/ContactForm.tsx \
  --platform web-react \
  --runs 5 \
  --json
```

**Expected Result:**

1. The workflow runs performance tests 5 times.
2. Calculates average metrics across runs.
3. Reports standard deviation for variability.
4. Output includes `performance-report.json` with averaged results.
5. Exit code `0` (Success).

---

## 4. Parameters

The following parameters and flags control the execution and behavior of the `/smartspec_ui_performance_test` workflow.

### Required Parameters

| Parameter | Type | Description | Validation |
| :--- | :--- | :--- | :--- |
| `--spec` | `<string>` | Path to UI specification JSON file. | Must exist and be valid JSON. |
| `--implementation` | `<string>` | Path to implementation file or directory. | Must exist and be accessible. |
| `--platform` (or `--ui-platform` for Kilo) | `<string>` | UI platform: `web-lit`, `web-react`, `web-angular`, or `mobile-flutter`. | Must be one of the allowed values. |

### Universal Flags

| Flag | Description | Default | Platform Support |
| :--- | :--- | :--- | :--- |
| `--config` | Path to the SmartSpec configuration file. | `.spec/smartspec.config.yaml` | `cli` \| `kilo` \| `ci` \| `other` |
| `--lang` | Language for report generation (e.g., `th`, `en`). | (System default) | `cli` \| `kilo` \| `ci` \| `other` |
| `--platform` | Execution platform context. **Required for Kilo Code.** | (Inferred) | `cli` \| `kilo` \| `ci` \| `other` |
| `--out` | Base path for safe outputs. | `.spec/reports/ui-performance/` | `cli` \| `kilo` \| `ci` \| `other` |
| `--json` | Output in JSON format. | `false` | `cli` \| `kilo` \| `ci` \| `other` |
| `--quiet` | Suppress standard output logs. | `false` | `cli` \| `kilo` \| `ci` \| `other` |

### Workflow-Specific Flags

| Flag | Description | Platform Support |
| :--- | :--- | :--- |
| `--compare-to` | Path to baseline performance JSON for regression testing. | `cli` \| `kilo` \| `ci` \| `other` |
| `--runs` | Number of test runs to average (default: 1). | `cli` \| `kilo` \| `ci` \| `other` |
| `--all-platforms` | Test on all supported platforms. | `cli` \| `kilo` \| `ci` \| `other` |

---

## 5. Output

The workflow generates output artifacts according to its configuration.

### Output Files

| File Path | Description |
| :--- | :--- |
| `.spec/reports/ui-performance/<run-id>/performance-report.md` | Detailed performance test report. |
| `.spec/reports/ui-performance/<run-id>/summary.json` | JSON summary of performance metrics. |
| `.spec/reports/ui-performance/<run-id>/metrics.csv` | CSV export of metrics for analysis. |

### Report Structure

The performance report includes:
- **Summary:** Overall pass/fail status
- **Bundle Size Analysis:** Total size, JavaScript, CSS, assets
- **Render Performance:** Initial render, re-render, mount time
- **Core Web Vitals:** LCP, FID, CLS with targets
- **Memory Usage:** Heap size, allocations
- **Network Performance:** Load time, requests
- **Recommendations:** Performance optimization suggestions

---

## 6. Performance Metrics

### Performance Targets

| Metric | Target | Description |
| :--- | :--- | :--- |
| **Bundle Size** | < 50 KB | Total component bundle size |
| **Initial Render** | < 200ms | Time to first render |
| **LCP** | < 2.5s | Largest Contentful Paint |
| **FID** | < 100ms | First Input Delay |
| **CLS** | < 0.1 | Cumulative Layout Shift |

### Core Web Vitals

#### LCP (Largest Contentful Paint)
- **Good:** < 2.5s
- **Needs Improvement:** 2.5s - 4.0s
- **Poor:** > 4.0s

#### FID (First Input Delay)
- **Good:** < 100ms
- **Needs Improvement:** 100ms - 300ms
- **Poor:** > 300ms

#### CLS (Cumulative Layout Shift)
- **Good:** < 0.1
- **Needs Improvement:** 0.1 - 0.25
- **Poor:** > 0.25

---

## 7. Pass/Fail Criteria

### Pass Conditions

All metrics must meet targets:
- Bundle size < 50 KB
- Initial render < 200ms
- LCP < 2.5s
- FID < 100ms
- CLS < 0.1

### Status Levels

- ✅ **PASS:** All metrics within targets
- ⚠️ **WARNING:** 1-2 metrics slightly over targets
- ❌ **FAIL:** 3+ metrics over or critical metric significantly over

---

## 8. Notes

- **Platform Flag:** When using Kilo Code, use `--ui-platform` for UI framework and `--platform kilo` for execution context.
- **Baseline Comparison:** Create baseline with first run, then use `--compare-to` for regression testing.
- **Multiple Runs:** Use `--runs 5` or more for accurate averages, as performance can vary.
- **Real Devices:** Test on real devices when possible, not just emulators.
- **Network Conditions:** Consider testing under different network conditions (3G, 4G, WiFi).
- **CI Integration:** Run performance tests in CI to catch regressions early.
- **Configuration:** The workflow respects settings in `.spec/smartspec.config.yaml`.

---

**End of Manual**
