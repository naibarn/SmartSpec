---
name: /smartspec_ui_performance_test
version: 1.0.0
role: verification
description: Performance testing for UI implementations with metrics and benchmarks
workflow: /smartspec_ui_performance_test
---

# smartspec_ui_performance_test

> **Canonical path:** `.smartspec/workflows/smartspec_ui_performance_test.md`  
> **Version:** 1.0.0  
> **Status:** Production Ready  
> **Category:** verification

## Purpose

Measure and verify UI performance metrics:

- Component render time
- Bundle size analysis
- Memory usage
- Network requests
- Core Web Vitals (LCP, FID, CLS)
- Time to Interactive (TTI)

This workflow ensures UI implementations meet performance standards.

---

## Governance contract

This workflow MUST follow:

- `knowledge_base_smartspec_handbook.md` (v6)
- `.spec/smartspec.config.yaml`

### Write scopes (enforced)

Allowed writes:

- Report outputs: `.spec/reports/ui-performance-test/**` (no `--apply` required)

Forbidden writes (must hard-fail):

- Any path outside config `safety.allow_writes_only_under`
- Any source code modifications

### `--apply` behavior

This workflow is **report-only** and does not require `--apply`.

---

## Invocation

### CLI

```bash
/smartspec_ui_performance_test \
  --spec specs/feature/spec-003-profile/ui-spec.json \
  --implementation src/ui/profile/ \
  [--json]
```

### Kilo Code

```bash
/smartspec_ui_performance_test.md \
  --spec specs/feature/spec-003-profile/ui-spec.json \
  --implementation src/ui/profile/ \
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
| `--spec` | Yes | Path to UI spec file (A2UI format) |
| `--implementation` | Yes | Path to implementation directory |
| `--benchmark` | No | Compare against benchmark file |
| `--iterations` | No | Number of test iterations (default: 10) |
| `--device` | No | Device profile (`mobile`, `desktop`, `tablet`; default: `desktop`) |

### Flag usage notes

- `--spec` must point to valid A2UI specification
- `--implementation` must contain UI implementation files
- `--benchmark` enables regression testing
- `--iterations` affects test accuracy (more = more accurate)

---

## Behavior

### 1) Load UI spec and implementation

- Read A2UI specification
- Scan implementation directory
- Identify all UI components

### 2) Bundle size analysis

Measure:

- Total bundle size
- Component-level bundle size
- Dependency sizes
- Tree-shaking effectiveness

### 3) Render performance

Test:

- Initial render time
- Re-render time
- Component mount time
- Component update time
- Component unmount time

### 4) Memory usage

Monitor:

- Heap size
- Memory leaks
- Component memory footprint
- Cleanup effectiveness

### 5) Network performance

Analyze:

- Number of requests
- Total transfer size
- Request timing
- Caching effectiveness

### 6) Core Web Vitals

Measure:

- **LCP (Largest Contentful Paint):** < 2.5s (good)
- **FID (First Input Delay):** < 100ms (good)
- **CLS (Cumulative Layout Shift):** < 0.1 (good)

### 7) Additional metrics

- Time to Interactive (TTI)
- First Contentful Paint (FCP)
- Speed Index
- Total Blocking Time (TBT)

### 8) Generate report

Write comprehensive performance report with recommendations.

---

## Output

### Report structure

**report.md:**

```markdown
# UI Performance Test Report

## Summary
- **Overall Score:** 78/100 (Good)
- **Device:** Desktop
- **Iterations:** 10
- **Status:** ⚠️ WARNINGS

## Core Web Vitals

| Metric | Value | Target | Status |
|---|---|---|---|
| LCP | 2.1s | < 2.5s | ✅ GOOD |
| FID | 45ms | < 100ms | ✅ GOOD |
| CLS | 0.15 | < 0.1 | ⚠️ NEEDS IMPROVEMENT |

## Bundle Size

- **Total:** 245 KB (gzipped: 78 KB)
- **JavaScript:** 180 KB
- **CSS:** 45 KB
- **Assets:** 20 KB

**Breakdown by component:**

| Component | Size | % of Total |
|---|---|---|
| ProfileForm | 85 KB | 35% |
| ProfileAvatar | 45 KB | 18% |
| SubmitButton | 30 KB | 12% |
| Other | 85 KB | 35% |

**Warning:** ProfileForm is large (85 KB). Consider code splitting.

## Render Performance

| Metric | Value | Target | Status |
|---|---|---|---|
| Initial Render | 145ms | < 200ms | ✅ GOOD |
| Re-render | 25ms | < 50ms | ✅ GOOD |
| TTI | 1.8s | < 3.5s | ✅ GOOD |

## Memory Usage

- **Initial:** 12 MB
- **Peak:** 18 MB
- **After GC:** 13 MB
- **Leak detected:** No

## Network Performance

- **Requests:** 8
- **Total size:** 312 KB
- **Cached:** 45%
- **Load time:** 1.2s

## Issues & Recommendations

### ⚠️ Warning: High CLS (0.15)

**Issue:** Layout shifts detected during page load

**Impact:** Poor user experience, content jumping

**Recommendations:**
1. Add explicit width/height to images
2. Reserve space for dynamic content
3. Avoid inserting content above existing content
4. Use CSS aspect-ratio for responsive images

### ⚠️ Warning: Large bundle (245 KB)

**Issue:** Bundle size exceeds recommended 200 KB

**Impact:** Slower load times on slow networks

**Recommendations:**
1. Code split ProfileForm component
2. Lazy load non-critical components
3. Remove unused dependencies
4. Optimize images

## Benchmark Comparison

Compared to previous run (2025-12-21):

| Metric | Previous | Current | Change |
|---|---|---|---|
| LCP | 2.3s | 2.1s | ✅ -8.7% |
| Bundle Size | 260 KB | 245 KB | ✅ -5.8% |
| CLS | 0.08 | 0.15 | ❌ +87.5% |

**Regression detected:** CLS increased significantly

## Performance Score Breakdown

- Bundle Size: 85/100
- Render Performance: 90/100
- Memory Usage: 95/100
- Network Performance: 88/100
- Core Web Vitals: 72/100

**Overall:** 78/100 (Good)
```

**summary.json:**

```json
{
  "status": "warning",
  "score": 78,
  "device": "desktop",
  "iterations": 10,
  "core_web_vitals": {
    "lcp": { "value": 2.1, "target": 2.5, "status": "good" },
    "fid": { "value": 45, "target": 100, "status": "good" },
    "cls": { "value": 0.15, "target": 0.1, "status": "needs_improvement" }
  },
  "bundle_size": {
    "total_bytes": 250880,
    "gzipped_bytes": 79872,
    "components": [
      { "name": "ProfileForm", "bytes": 87040 }
    ]
  },
  "render_performance": {
    "initial_render_ms": 145,
    "re_render_ms": 25,
    "tti_ms": 1800
  },
  "memory": {
    "initial_mb": 12,
    "peak_mb": 18,
    "after_gc_mb": 13,
    "leak_detected": false
  },
  "issues": [
    {
      "severity": "warning",
      "metric": "cls",
      "message": "CLS exceeds target (0.15 > 0.1)"
    }
  ],
  "timestamp": "2025-12-22T00:00:00Z"
}
```

---

## Performance targets

### Bundle size

- **Good:** < 200 KB total
- **Acceptable:** 200-300 KB
- **Poor:** > 300 KB

### Render performance

- **Initial render:** < 200ms (good), < 500ms (acceptable)
- **Re-render:** < 50ms (good), < 100ms (acceptable)
- **TTI:** < 3.5s (good), < 5s (acceptable)

### Core Web Vitals

- **LCP:** < 2.5s (good), 2.5-4s (needs improvement), > 4s (poor)
- **FID:** < 100ms (good), 100-300ms (needs improvement), > 300ms (poor)
- **CLS:** < 0.1 (good), 0.1-0.25 (needs improvement), > 0.25 (poor)

---

## Benchmark comparison

When `--benchmark` is provided:

- Compare current metrics against benchmark
- Detect regressions
- Report performance changes
- Fail if critical regressions detected

**Benchmark file format:**

```json
{
  "date": "2025-12-21",
  "metrics": {
    "lcp": 2.3,
    "fid": 50,
    "cls": 0.08,
    "bundle_size": 260000
  }
}
```

---

## Error handling

### Invalid spec

If UI spec is invalid:

- Report spec validation errors
- Cannot proceed with test
- Exit with code 1

### Implementation not found

If implementation directory doesn't exist:

- Report missing implementation
- Cannot proceed with test
- Exit with code 1

### Critical regression

If critical performance regression detected:

- Report regression details
- Exit with code 1 (fail build)

---

## Usage examples

### Example 1: Basic performance test

```bash
/smartspec_ui_performance_test \
  --spec specs/feature/spec-003-profile/ui-spec.json \
  --implementation src/ui/profile/
```

### Example 2: Mobile device profile

```bash
/smartspec_ui_performance_test \
  --spec specs/feature/spec-003-profile/ui-spec.json \
  --implementation src/ui/profile/ \
  --device mobile
```

### Example 3: With benchmark comparison

```bash
/smartspec_ui_performance_test \
  --spec specs/feature/spec-003-profile/ui-spec.json \
  --implementation src/ui/profile/ \
  --benchmark .spec/benchmarks/profile-ui-benchmark.json
```

### Example 4: Kilo Code

```bash
/smartspec_ui_performance_test.md \
  --spec specs/feature/spec-003-profile/ui-spec.json \
  --implementation src/ui/profile/ \
  --platform kilo \
  --json
```

---

## Integration

This workflow integrates with:

- `smartspec_verify_ui_implementation` - Performance as part of verification
- `smartspec_quality_gate` - Performance as quality gate criterion
- CI/CD pipelines - Automated performance testing
- `smartspec_production_monitor` - Compare with production metrics

---

## Best practices

1. **Run regularly** - Catch performance regressions early
2. **Use benchmarks** - Track performance over time
3. **Test on mobile** - Mobile performance is critical
4. **Integrate with CI** - Block merges on performance regressions
5. **Monitor production** - Compare test results with real-world data
6. **Optimize iteratively** - Focus on biggest performance wins first

---

## Performance optimization tips

### Bundle size

- Code splitting
- Tree shaking
- Lazy loading
- Remove unused dependencies
- Optimize images

### Render performance

- Memoization
- Virtual scrolling
- Debouncing/throttling
- Avoid unnecessary re-renders
- Use production builds

### Core Web Vitals

- **LCP:** Optimize images, lazy load, use CDN
- **FID:** Minimize JavaScript, code splitting, web workers
- **CLS:** Reserve space, avoid layout shifts, use aspect-ratio

---

## Security considerations

- Performance tests do not modify source code
- Reports may contain sensitive information
- Store reports securely
- Review reports before sharing externally

---

# End of workflow doc
