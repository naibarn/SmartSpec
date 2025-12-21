# `/smartspec_ui_test_generator` - Generate UI Tests

| Metadata | Value |
|----------|-------|
| **Workflow ID** | `smartspec_ui_test_generator` |
| **Category** | UI / A2UI / Testing |
| **Version** | 6.0.0+ |
| **Requires `--apply`** | Yes |
| **Platform Support** | CLI, Kilo Code |

---

## Overview

Generate automated UI tests from UI specifications. This workflow creates comprehensive test suites including unit tests, integration tests, and end-to-end tests based on your A2UI specification. Tests cover component rendering, user interactions, accessibility, and data flow.

The generated tests follow best practices for your target platform and testing framework.

---

## Usage

### CLI

```bash
/smartspec_ui_test_generator \
  --spec specs/feature/spec-001-booking/ui-spec.json \
  --output tests/ui/booking \
  --test-type all
```

### Kilo Code

```bash
/smartspec_ui_test_generator.md \
  --spec specs/feature/spec-001-booking/ui-spec.json \
  --output tests/ui/booking \
  --test-type all \
  --platform kilo
```

---

## Use Cases

### 1. Generate Complete Test Suite

**Scenario:** Create unit, integration, and E2E tests for a booking form.

**Command:**
```bash
/smartspec_ui_test_generator \
  --spec specs/feature/spec-001-booking/ui-spec.json \
  --output tests/ui/booking \
  --test-type all \
  --framework jest \
  --include-accessibility
```

**Expected Result:** Complete test suite with unit tests, integration tests, E2E tests, and accessibility tests.

### 2. Generate Unit Tests Only

**Scenario:** Create unit tests for individual components.

**Command:**
```bash
/smartspec_ui_test_generator \
  --spec specs/feature/spec-002-dashboard/ui-spec.json \
  --output tests/unit/dashboard \
  --test-type unit \
  --coverage-target 80
```

**Expected Result:** Unit tests for each component with 80% coverage target.

### 3. Generate E2E Tests with Visual Regression

**Scenario:** Create end-to-end tests with screenshot comparison.

**Command:**
```bash
/smartspec_ui_test_generator \
  --spec specs/feature/spec-003-profile/ui-spec.json \
  --output tests/e2e/profile \
  --test-type e2e \
  --framework playwright \
  --visual-regression
```

**Expected Result:** E2E tests with visual regression testing using Playwright.

---

## Parameters

### Required Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `--spec` | path | Path to UI specification JSON file |
| `--output` | path | Output directory for test files |

### Universal Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--apply` | boolean | false | Apply changes (without this flag, runs in preview mode) |
| `--platform` | string | cli | Platform: cli, kilo |
| `--verbose` | boolean | false | Enable verbose output |
| `--dry-run` | boolean | false | Simulate without making changes |
| `--report-dir` | path | auto | Custom report directory |
| `--force` | boolean | false | Force overwrite existing files |

### Workflow-Specific Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--test-type` | string | all | Test type: unit, integration, e2e, all |
| `--framework` | string | auto | Testing framework: jest, vitest, playwright, cypress, flutter_test |
| `--target-platform` | string | auto | Target platform: web, flutter, mobile |
| `--include-accessibility` | boolean | true | Include accessibility tests |
| `--include-visual` | boolean | false | Include visual regression tests |
| `--coverage-target` | number | 80 | Code coverage target percentage |
| `--mock-api` | boolean | true | Generate API mocks for tests |
| `--test-data` | path | - | Path to test data file |
| `--parallel` | boolean | true | Enable parallel test execution |

---

## Output

### Report Location
```
.spec/reports/ui-test-generator/<run-id>/
├── report.md              # Human-readable summary
├── report.json            # Machine-readable data
└── preview/
    ├── test-plan.md       # Test plan overview
    ├── coverage-map.json  # Coverage mapping
    └── tests/             # Preview of test files
```

### Generated Files (with `--apply`)

**For Web/React with Jest:**
```
<output-dir>/
├── unit/
│   ├── BookingForm.test.tsx
│   ├── DatePicker.test.tsx
│   └── __mocks__/
├── integration/
│   └── BookingFlow.test.tsx
├── e2e/
│   └── booking.spec.ts
├── accessibility/
│   └── booking-a11y.test.tsx
└── setup/
    ├── test-utils.ts
    └── mocks.ts
```

**For Flutter:**
```
<output-dir>/
├── widget_test/
│   ├── booking_form_test.dart
│   └── date_picker_test.dart
├── integration_test/
│   └── booking_flow_test.dart
└── test_utils/
    └── test_helpers.dart
```

---

## Test Coverage

### Unit Tests
- ✅ Component rendering
- ✅ Props validation
- ✅ State management
- ✅ Event handlers
- ✅ Edge cases

### Integration Tests
- ✅ Component interaction
- ✅ Data flow
- ✅ Form submission
- ✅ API integration
- ✅ Error handling

### E2E Tests
- ✅ User workflows
- ✅ Navigation
- ✅ Multi-step processes
- ✅ Cross-browser testing
- ✅ Performance metrics

### Accessibility Tests
- ✅ WCAG compliance
- ✅ Keyboard navigation
- ✅ Screen reader support
- ✅ Color contrast
- ✅ Focus management

---

## Prerequisites

**Required:**
- Valid UI specification file
- Testing framework installed
- Test runner configured

**Optional:**
- Test data files
- Mock API definitions
- Visual regression baseline images

---

## Notes

1. **Preview First:** Always run without `--apply` to review test plan
2. **Framework Detection:** Testing framework is auto-detected from project config
3. **Coverage:** Generated tests aim for specified coverage target
4. **Mocking:** API calls are automatically mocked unless disabled
5. **Accessibility:** WCAG tests are included by default
6. **Visual Regression:** Requires baseline images for comparison
7. **Parallel Execution:** Tests are configured for parallel execution by default
8. **Maintenance:** Update tests when UI spec changes

---

## Related Workflows

- [`/smartspec_generate_ui_spec`](./generate_ui_spec.md) - Generate UI specification
- [`/smartspec_generate_ui_implementation`](./generate_ui_implementation.md) - Generate UI code
- [`/smartspec_ui_accessibility_audit`](./ui_accessibility_audit.md) - Audit accessibility
- [`/smartspec_test_suite_runner`](./test_suite_runner.md) - Run test suite

---

**For more information, see the [A2UI Documentation](../../README-A2UI.md).**
