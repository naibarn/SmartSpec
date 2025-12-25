---
name: /smartspec_ui_analytics_reporter
version: 1.0.0
role: monitoring
description: Track UI component usage, adoption metrics, and quality indicators across the project
workflow: /smartspec_ui_analytics_reporter
---

# smartspec_ui_analytics_reporter

> **Canonical path:** `.smartspec/workflows/smartspec_ui_analytics_reporter.md`  
> **Version:** 1.0.0  
> **Status:** Production Ready  
> **Category:** monitoring

## Purpose

Generate analytics reports for UI components:

- Component usage statistics
- Adoption metrics
- Quality indicators
- Accessibility compliance rates
- Performance metrics trends
- Component catalog health

This workflow provides insights into UI development patterns and quality.

---

## Governance contract

This workflow MUST follow:

- `knowledge_base_smartspec_handbook.md` (v6)
- `.spec/smartspec.config.yaml`

### Write scopes (enforced)

Allowed writes:

- Report outputs: `.spec/reports/ui-analytics/**` (no `--apply` required)

Forbidden writes (must hard-fail):

- Any path outside config `safety.allow_writes_only_under`
- Any source code modifications

### `--apply` behavior

This workflow is **report-only** and does not require `--apply`.

---

## Invocation

### CLI

```bash
/smartspec_ui_analytics_reporter \
  --catalog .spec/ui-catalog.json \
  --implementation src/ui/ \
  [--json]
```

### Kilo Code

```bash
/smartspec_ui_analytics_reporter.md \
  --catalog .spec/ui-catalog.json \
  --implementation src/ui/ \
  --platform kilo \
  [--json]
```

---

## Flags

### Universal flags (must support)

| Flag | Required | Description |
|---|---|---|
| `--config` | No | Path to custom config file (default: `.spec/smartspec.config.yaml`) |
| `--lang` | No | Output language (`th` for Thai, `en` for English) |
| `--platform` | No | Platform mode (`cli`, `kilo`, `ci`, `other`) |
| `--out` | No | Base output directory for reports |
| `--json` | No | Output results in JSON format |
| `--quiet` | No | Suppress non-essential output |

### Workflow-specific flags

| Flag | Required | Description |
|---|---|---|
| `--catalog` | Yes | Path to UI catalog file |
| `--implementation` | Yes | Path to implementation directory |
| `--time-range` | No | Time range for metrics (`7d`, `30d`, `90d`, `all`; default: `30d`) |
| `--compare-to` | No | Compare to previous report |

### Flag usage notes

- `--catalog` must point to valid UI catalog
- `--implementation` must contain UI implementation files
- `--time-range` affects metrics calculation
- `--compare-to` enables trend analysis

---

## Behavior

### 1) Load catalog and implementation

- Read UI catalog
- Scan implementation directory
- Identify all UI components

### 2) Component usage analysis

Track:

- Component usage frequency
- Most/least used components
- Unused components
- Component dependencies

### 3) Adoption metrics

Measure:

- Catalog coverage (% of catalog components used)
- Implementation completeness
- New components added
- Deprecated components

### 4) Quality indicators

Analyze:

- Accessibility compliance rate
- Performance metrics (average)
- Code quality scores
- Test coverage

### 5) Trends analysis

Track over time:

- Usage trends
- Quality trends
- Performance trends
- Adoption rate

### 6) Component health

Assess:

- Well-maintained components
- Components needing attention
- Outdated components
- Security issues

### 7) Generate report

Write comprehensive analytics report with visualizations.

---

## Output

### Report structure

**report.md:**

```markdown
# UI Analytics Report

**Period:** Last 30 days  
**Generated:** 2025-12-22

## Executive Summary

- **Total Components:** 17 (catalog) / 14 (implemented)
- **Catalog Coverage:** 82%
- **Avg Accessibility Score:** 92/100
- **Avg Performance Score:** 85/100
- **Unused Components:** 3

## Component Usage

### Top 10 Most Used Components

| Component | Usage Count | % of Total |
|---|---|---|
| button-primary | 45 | 18% |
| input-text | 38 | 15% |
| card | 32 | 13% |
| modal | 28 | 11% |
| input-email | 24 | 10% |
| ... | ... | ... |

### Unused Components (3)

- `chart-pie` - Never used
- `input-date-range` - Never used
- `badge-notification` - Never used

**Recommendation:** Consider removing or promoting these components

## Adoption Metrics

### Catalog Coverage

- **Implemented:** 14/17 (82%)
- **Not Implemented:** 3/17 (18%)

**Trend:** +2 components this period

### Component Categories

| Category | Components | Usage |
|---|---|---|
| Buttons | 3 | 25% |
| Inputs | 5 | 30% |
| Cards | 2 | 15% |
| Modals | 2 | 10% |
| Charts | 3 | 5% |
| Other | 2 | 15% |

## Quality Indicators

### Accessibility Compliance

- **WCAG AA Compliant:** 13/14 (93%)
- **Needs Improvement:** 1/14 (7%)

**Issues:**
- `ProfileForm`: CLS exceeds target

### Performance Metrics

| Metric | Average | Target | Status |
|---|---|---|---|
| Bundle Size | 45 KB | < 50 KB | ✅ GOOD |
| Render Time | 120ms | < 200ms | ✅ GOOD |
| LCP | 2.2s | < 2.5s | ✅ GOOD |
| CLS | 0.08 | < 0.1 | ✅ GOOD |

### Test Coverage

- **Unit Tests:** 85%
- **Integration Tests:** 70%
- **E2E Tests:** 45%

**Recommendation:** Increase E2E test coverage

## Trends (vs Previous Period)

### Usage Trends

- **Total Usage:** +15% (215 → 247)
- **New Components:** +2
- **Deprecated:** 0

### Quality Trends

- **Accessibility:** +5% (87 → 92)
- **Performance:** -3% (88 → 85)
- **Test Coverage:** +8% (77 → 85)

⚠️ **Alert:** Performance score decreased

## Component Health

### Healthy Components (11)

Components with good metrics across all dimensions:

- button-primary
- input-text
- card
- modal
- ...

### Components Needing Attention (3)

| Component | Issues | Priority |
|---|---|---|
| ProfileForm | High CLS, large bundle | High |
| chart-line | Low test coverage | Medium |
| input-date | Accessibility issues | High |

## Recommendations

### High Priority

1. **Fix ProfileForm CLS issue** - Affects user experience
2. **Improve input-date accessibility** - Blocks WCAG AA compliance
3. **Investigate performance regression** - Overall score decreased

### Medium Priority

1. **Increase E2E test coverage** - Currently only 45%
2. **Promote or remove unused components** - 3 components never used
3. **Add tests for chart-line** - Low coverage

### Low Priority

1. **Document component best practices** - Improve adoption
2. **Create component usage examples** - Help developers
3. **Monitor bundle size trends** - Prevent bloat

## Detailed Metrics

### Component-Level Metrics

| Component | Usage | Accessibility | Performance | Tests | Health |
|---|---|---|---|---|---|
| button-primary | 45 | 95/100 | 90/100 | 90% | ✅ Healthy |
| input-text | 38 | 92/100 | 88/100 | 85% | ✅ Healthy |
| ProfileForm | 12 | 85/100 | 72/100 | 80% | ⚠️ Needs Attention |
| ... | ... | ... | ... | ... | ... |

## Conclusion

Overall UI development health is **GOOD** with some areas needing attention:

✅ **Strengths:**
- High catalog coverage (82%)
- Good accessibility compliance (93%)
- Strong test coverage (85%)

⚠️ **Areas for Improvement:**
- Performance regression (-3%)
- 3 components need attention
- E2E test coverage low (45%)

**Next Steps:** Address high-priority recommendations
```

**summary.json:**

```json
{
  "period": "30d",
  "generated_at": "2025-12-22T00:00:00Z",
  "summary": {
    "total_components_catalog": 17,
    "total_components_implemented": 14,
    "catalog_coverage": 0.82,
    "avg_accessibility_score": 92,
    "avg_performance_score": 85,
    "unused_components": 3
  },
  "usage": {
    "total_usage": 247,
    "top_components": [
      { "id": "button-primary", "count": 45, "percentage": 0.18 }
    ],
    "unused": ["chart-pie", "input-date-range", "badge-notification"]
  },
  "quality": {
    "accessibility_compliant": 13,
    "accessibility_total": 14,
    "test_coverage": {
      "unit": 0.85,
      "integration": 0.70,
      "e2e": 0.45
    }
  },
  "trends": {
    "usage_change": 0.15,
    "accessibility_change": 0.05,
    "performance_change": -0.03
  },
  "health": {
    "healthy": 11,
    "needs_attention": 3,
    "critical": 0
  }
}
```

---

## Metrics definitions

### Component usage

- **Usage count:** Number of times component is used in implementation
- **Usage percentage:** Percentage of total component usage

### Catalog coverage

- **Coverage:** Percentage of catalog components that are implemented
- **Implemented:** Number of catalog components used in implementation
- **Not implemented:** Number of catalog components not used

### Quality indicators

- **Accessibility score:** Average WCAG compliance score (0-100)
- **Performance score:** Average performance metrics score (0-100)
- **Test coverage:** Percentage of code covered by tests

### Component health

- **Healthy:** All metrics above targets
- **Needs attention:** Some metrics below targets
- **Critical:** Multiple metrics significantly below targets

---

## Trend analysis

When `--compare-to` is provided:

- Compare current metrics to previous report
- Calculate percentage changes
- Identify regressions and improvements
- Generate trend visualizations

---

## Error handling

### Invalid catalog

If catalog is invalid:

- Report validation errors
- Cannot proceed with analytics
- Exit with code 1

### Implementation not found

If implementation directory doesn't exist:

- Report missing implementation
- Cannot proceed with analytics
- Exit with code 1

---

## Usage examples

### Example 1: Basic analytics report

```bash
/smartspec_ui_analytics_reporter \
  --catalog .spec/ui-catalog.json \
  --implementation src/ui/
```

### Example 2: 90-day report with comparison

```bash
/smartspec_ui_analytics_reporter \
  --catalog .spec/ui-catalog.json \
  --implementation src/ui/ \
  --time-range 90d \
  --compare-to .spec/reports/ui-analytics/2025-11-22/summary.json
```

### Example 3: Kilo Code

```bash
/smartspec_ui_analytics_reporter.md \
  --catalog .spec/ui-catalog.json \
  --implementation src/ui/ \
  --platform kilo \
  --json
```

---

## Integration

This workflow integrates with:

- `smartspec_ui_accessibility_audit` - Accessibility metrics
- `smartspec_ui_performance_test` - Performance metrics
- `smartspec_verify_ui_implementation` - Quality metrics
- CI/CD pipelines - Automated reporting
- Dashboards - Metrics visualization

---

## Best practices

1. **Run regularly** - Weekly or monthly reports
2. **Track trends** - Compare to previous reports
3. **Act on insights** - Address recommendations
4. **Share with team** - Improve awareness
5. **Monitor health** - Catch issues early
6. **Celebrate wins** - Recognize improvements

---

## Security considerations

- Reports may contain sensitive information
- Store reports securely
- Review reports before sharing externally
- Anonymize data if needed

---

# End of workflow doc
