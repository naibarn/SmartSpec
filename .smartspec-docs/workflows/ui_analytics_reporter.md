| manual_name | manual_version | compatible_workflow | compatible_workflow_versions |
|-------------|----------------|---------------------|------------------------------|
| /smartspec_ui_analytics_reporter Manual (EN) | 6.0 | /smartspec_ui_analytics_reporter | 6.0.x |

# /smartspec_ui_analytics_reporter Manual (v6.0, English)

## 1. Overview

This manual explains how to use the workflow:

The `/smartspec_ui_analytics_reporter` workflow tracks UI component usage, adoption metrics, and quality indicators across the project, providing data-driven insights for UI development strategy.

**Purpose:** Generate comprehensive analytics reports on UI component usage, catalog adoption, quality metrics, and trends to guide UI development decisions and improvements.

**Version:** 6.0  
**Category:** ui_optimization_and_analytics

---

## 2. Usage

This workflow supports invocation via the Command Line Interface (CLI) and Kilo Code (internal scripting environment).

### 🔗 CLI Usage

The CLI invocation requires specifying the catalog and implementation directory.

```bash
/smartspec_ui_analytics_reporter \
  --catalog <path/to/ui-catalog.json> \
  --implementation <path/to/implementation-dir> \
  [--time-range <7d|30d|90d|all>] \
  [--compare-to <previous-report.json>]
```

### Kilo Code Usage

The Kilo Code invocation is identical to the CLI structure, typically used within automated pipelines or internal scripts.

**Important:** When using Kilo Code, you MUST include `--platform kilo` flag.

```bash
/smartspec_ui_analytics_reporter.md \
  --catalog <path/to/ui-catalog.json> \
  --implementation <path/to/implementation-dir> \
  [--time-range <7d|30d|90d|all>] \
  [--compare-to <previous-report.json>] \
  --platform kilo
```

---

## 3. Use Cases

### Use Case 1: Monthly Analytics Report (CLI)

**Scenario:** A team lead wants to review UI component usage and quality metrics for the past month.

**Command:**

```bash
/smartspec_ui_analytics_reporter \
  --catalog .spec/ui-catalog.json \
  --implementation src/ui/ \
  --time-range 30d
```

**Expected Result:**

1. The workflow analyzes component usage over 30 days.
2. Calculates adoption metrics (catalog coverage).
3. Aggregates quality indicators (accessibility, performance, tests).
4. Identifies top/unused components.
5. Generates comprehensive analytics report.
6. Exit code `0` (Success).

### Use Case 2: Trend Analysis with Comparison (Kilo Code)

**Scenario:** A CI pipeline generates weekly analytics reports and compares to the previous week to track trends.

**Command (Kilo Code Snippet):**

```bash
/smartspec_ui_analytics_reporter.md \
  --catalog .spec/ui-catalog.json \
  --implementation src/ui/ \
  --time-range 7d \
  --compare-to .spec/reports/ui-analytics/2025-12-15/summary.json \
  --platform kilo
```

**Expected Result:**

1. The workflow generates analytics for the past 7 days.
2. Compares metrics to the previous week's report.
3. Calculates percentage changes for all metrics.
4. Identifies trends (improving, declining, stable).
5. Generates trend analysis report.
6. Exit code `0` (Success).

### Use Case 3: Comprehensive Project Analytics (CLI)

**Scenario:** A project manager needs a complete overview of all UI components since project start.

**Command:**

```bash
/smartspec_ui_analytics_reporter \
  --catalog .spec/ui-catalog.json \
  --implementation src/ui/ \
  --time-range all \
  --json
```

**Expected Result:**

1. The workflow analyzes all historical data.
2. Generates complete usage statistics.
3. Reports lifetime quality metrics.
4. Identifies component health across the project.
5. Output includes `analytics-report.json` with full data.
6. Exit code `0` (Success).

---

## 4. Parameters

The following parameters and flags control the execution and behavior of the `/smartspec_ui_analytics_reporter` workflow.

### Required Parameters

| Parameter | Type | Description | Validation |
| :--- | :--- | :--- | :--- |
| `--catalog` | `<string>` | Path to UI catalog JSON file. | Must exist and be valid JSON. |
| `--implementation` | `<string>` | Path to implementation directory. | Must exist and be accessible. |

### Universal Flags

| Flag | Description | Default | Platform Support |
| :--- | :--- | :--- | :--- |
| `--config` | Path to the SmartSpec configuration file. | `.spec/smartspec.config.yaml` | `cli` \| `kilo` \| `ci` \| `other` |
| `--lang` | Language for report generation (e.g., `th`, `en`). | (System default) | `cli` \| `kilo` \| `ci` \| `other` |
| `--platform` | Execution platform context. **Required for Kilo Code.** | (Inferred) | `cli` \| `kilo` \| `ci` \| `other` |
| `--out` | Base path for safe outputs. | `.spec/reports/ui-analytics/` | `cli` \| `kilo` \| `ci` \| `other` |
| `--json` | Output in JSON format. | `false` | `cli` \| `kilo` \| `ci` \| `other` |
| `--quiet` | Suppress standard output logs. | `false` | `cli` \| `kilo` \| `ci` \| `other` |

### Workflow-Specific Flags

| Flag | Description | Platform Support |
| :--- | :--- | :--- |
| `--time-range` | Time range for metrics: `7d`, `30d`, `90d`, or `all` (default: `30d`). | `cli` \| `kilo` \| `ci` \| `other` |
| `--compare-to` | Path to previous report JSON for trend analysis. | `cli` \| `kilo` \| `ci` \| `other` |

---

## 5. Output

The workflow generates output artifacts according to its configuration.

### Output Files

| File Path | Description |
| :--- | :--- |
| `.spec/reports/ui-analytics/<run-id>/report.md` | Comprehensive analytics report. |
| `.spec/reports/ui-analytics/<run-id>/summary.json` | JSON summary of analytics data. |
| `.spec/reports/ui-analytics/<run-id>/components.csv` | CSV export of component-level metrics. |

### Report Structure

The analytics report includes:
- **Executive Summary:** Key metrics overview
- **Component Usage:** Top/unused components, usage frequency
- **Adoption Metrics:** Catalog coverage, new/deprecated components
- **Quality Indicators:** Accessibility, performance, test coverage
- **Trends Analysis:** Changes over time (if comparison provided)
- **Component Health:** Healthy/needs attention/critical status
- **Recommendations:** Prioritized action items

---

## 6. Analytics Metrics

### Component Usage

- **Usage Count:** Number of times component is used
- **Usage Percentage:** Percentage of total component usage
- **Top Components:** Most frequently used components
- **Unused Components:** Components in catalog but not used

### Adoption Metrics

- **Catalog Coverage:** Percentage of catalog components implemented
- **Implementation Rate:** Components implemented vs. total catalog
- **New Components:** Components added in time period
- **Deprecated Components:** Components marked for removal

### Quality Indicators

- **Accessibility Score:** Average WCAG compliance score (0-100)
- **Performance Score:** Average performance metrics score (0-100)
- **Test Coverage:** Percentage of code covered by tests
  - Unit test coverage
  - Integration test coverage
  - E2E test coverage

### Component Health

- **Healthy:** All metrics above targets
- **Needs Attention:** Some metrics below targets
- **Critical:** Multiple metrics significantly below targets

---

## 7. Trend Analysis

When `--compare-to` is provided, the report includes:

### Trend Metrics

- **Usage Trends:** Component usage changes over time
- **Quality Trends:** Accessibility and performance score changes
- **Adoption Trends:** Catalog coverage changes
- **Health Trends:** Component health status changes

### Trend Indicators

- 📈 **Improving:** Metrics increasing positively
- 📉 **Declining:** Metrics decreasing negatively
- ➡️ **Stable:** Metrics unchanged or minor fluctuation

---

## 8. Notes

- **Platform Flag:** When using Kilo Code, always include `--platform kilo` to ensure proper context and logging.
- **Time Range:** Use `30d` for monthly reviews, `7d` for weekly tracking, `all` for comprehensive analysis.
- **Comparison Reports:** Save summary.json from each run to enable trend analysis in future runs.
- **Regular Reporting:** Run analytics weekly or monthly to track progress and identify issues early.
- **Team Sharing:** Share reports with the team to improve awareness and drive improvements.
- **Action Items:** Focus on high-priority recommendations from the report.
- **Configuration:** The workflow respects settings in `.spec/smartspec.config.yaml`.

---

**End of Manual**
