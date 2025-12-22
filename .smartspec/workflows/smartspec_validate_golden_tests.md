# smartspec_validate_golden_tests

## Overview
Validates A2UI JSON output against golden test cases to ensure quality and compliance.

## Version
1.0.0

## Category
testing_and_validation

## Description
This workflow runs **golden test cases** to validate that A2UI JSON output meets quality standards, accessibility requirements, and A2UI v0.8 specification compliance. Golden tests are reference implementations that define the expected structure and behavior of A2UI components.

The workflow:
- **Loads golden test cases** from `.spec/golden_tests/`
- **Validates A2UI JSON** against expected output
- **Checks validation rules** (accessibility, theming, structure)
- **Generates test reports** with pass/fail status
- **Identifies regressions** when output doesn't match expectations

## Parameters

### Optional Parameters

#### `--test-id`
- **Type:** string
- **Required:** No
- **Description:** Run a specific test by ID (if not provided, runs all tests)
- **Example:** `01_basic_button`

#### `--category`
- **Type:** string
- **Required:** No
- **Description:** Run tests in a specific category
- **Allowed Values:**
  - `basic_components`: Simple component tests
  - `forms`: Form and validation tests
  - `theming`: Theme token tests
  - `complex_layouts`: Multi-component layout tests
  - `error_scenarios`: Tests that should fail
  - `interactions`: Interactive component tests
  - `data_binding`: Data-driven component tests
- **Example:** `basic_components`

#### `--input-file`
- **Type:** string
- **Required:** No
- **Description:** Validate a specific A2UI JSON file against golden tests
- **Example:** `.spec/output/ui_spec.json`

#### `--theme-file`
- **Type:** string
- **Required:** No
- **Default:** `.spec/theme.json`
- **Description:** Theme file to use for theme token validation

#### `--verbose`
- **Type:** boolean
- **Required:** No
- **Default:** `false`
- **Description:** Show detailed validation output

#### `--output-format`
- **Type:** string
- **Required:** No
- **Default:** `markdown`
- **Description:** Output format for test report
- **Allowed Values:**
  - `markdown`: Markdown report
  - `json`: JSON report
  - `junit`: JUnit XML (for CI/CD)

#### `--output-file`
- **Type:** string
- **Required:** No
- **Default:** `.spec/test_results.md`
- **Description:** Output file path for test report

#### `--fail-fast`
- **Type:** boolean
- **Required:** No
- **Default:** `false`
- **Description:** Stop on first test failure

## Behavior

### Test Execution Process
1. **Load Golden Tests:** Reads all test cases from `.spec/golden_tests/`
2. **Filter Tests:** Applies filters (test-id, category) if specified
3. **Run Tests:** For each test:
   - Validates required fields (version, type, component)
   - Checks accessibility compliance
   - Validates theme token references
   - Verifies component structure
   - Compares with expected output
4. **Generate Report:** Creates test report with results
5. **Exit Status:** Returns 0 if all tests pass, 1 if any fail

### Validation Checks

Each test performs multiple validation checks:

| Check | Description | Failure Impact |
|-------|-------------|----------------|
| Schema Validation | A2UI JSON structure is valid | Critical |
| Accessibility | Component has accessibility object | Critical |
| Theme Tokens | Theme references are valid | Error |
| Component Structure | Component has required fields | Critical |
| Expected Output | Output matches expected | Warning |
| Validation Rules | Custom rules pass | Varies |

### Test Result Status

- ✅ **PASS**: Test passed all validation checks
- ❌ **FAIL**: Test failed one or more critical checks
- ⚠️ **WARN**: Test passed but has warnings
- ⏭️ **SKIP**: Test was skipped (not in filter)

## Output
- **Test Report:** Markdown, JSON, or JUnit XML report
- **Summary Statistics:** Total, passed, failed, skipped
- **Failure Details:** Specific validation errors for failed tests

## Example Usage

### CLI

```bash
# Run all golden tests
/smartspec_validate_golden_tests

# Run a specific test
/smartspec_validate_golden_tests --test-id 01_basic_button

# Run tests in a category
/smartspec_validate_golden_tests --category basic_components

# Validate a specific file
/smartspec_validate_golden_tests \
  --input-file .spec/output/ui_spec.json

# Run with verbose output
/smartspec_validate_golden_tests \
  --verbose true \
  --output-format markdown

# Generate JUnit report for CI/CD
/smartspec_validate_golden_tests \
  --output-format junit \
  --output-file test-results.xml

# Fail fast on first error
/smartspec_validate_golden_tests \
  --fail-fast true
```

### Kilo Code

```kilo
# Run all tests
smartspec_validate_golden_tests()

# Run specific category
smartspec_validate_golden_tests(
  category="forms"
)

# Validate specific file
smartspec_validate_golden_tests(
  input_file=".spec/output/ui_spec.json",
  verbose=true
)

# Generate JSON report
smartspec_validate_golden_tests(
  output_format="json",
  output_file=".spec/test_results.json"
)
```

## Use Cases

### Use Case 1: Pre-Commit Validation
**Scenario:** Validate A2UI output before committing changes.

**Command:**
```bash
/smartspec_validate_golden_tests --fail-fast true
```

**Result:** All tests must pass before commit is allowed.

---

### Use Case 2: CI/CD Integration
**Scenario:** Run golden tests in CI/CD pipeline.

**Command:**
```bash
/smartspec_validate_golden_tests \
  --output-format junit \
  --output-file test-results.xml
```

**Result:** JUnit XML report for CI/CD integration (GitHub Actions, Jenkins, etc.).

---

### Use Case 3: Regression Testing
**Scenario:** Ensure new changes don't break existing functionality.

**Command:**
```bash
/smartspec_validate_golden_tests --verbose true
```

**Result:** Detailed report showing any regressions.

---

### Use Case 4: Category-Specific Testing
**Scenario:** Test only accessibility-related features.

**Command:**
```bash
/smartspec_validate_golden_tests \
  --category error_scenarios \
  --verbose true
```

**Result:** Focused testing on specific feature area.

## Test Report Example

```markdown
# Golden Test Results

**Date:** 2025-12-22 10:30:00
**Total Tests:** 8
**Passed:** 7
**Failed:** 1
**Skipped:** 0

## Summary by Category

| Category | Total | Passed | Failed |
|----------|-------|--------|--------|
| basic_components | 1 | 1 | 0 |
| forms | 1 | 1 | 0 |
| theming | 1 | 0 | 1 |
| complex_layouts | 1 | 1 | 0 |
| error_scenarios | 2 | 2 | 0 |
| interactions | 1 | 1 | 0 |
| data_binding | 1 | 1 | 0 |

## Failed Tests

### ❌ 03_themed_card
**Category:** theming
**Error:** Invalid theme token reference: {colors.nonexistent.500}
**Expected:** Theme token should exist in theme.json
**Actual:** Token not found

## Passed Tests

✅ 01_basic_button
✅ 02_form_with_validation
✅ 04_complex_layout
✅ 05_error_missing_accessibility
✅ 06_error_invalid_theme_token
✅ 07_interactive_modal
✅ 08_data_driven_list
```

## Related Workflows
- `smartspec_generate_ui_spec`: Generate UI specs to validate
- `smartspec_manage_theme`: Manage theme for theme token validation
- `smartspec_ui_validation`: Validate individual UI specs

## Implementation
Implemented in: `.smartspec/scripts/validate_golden_tests.py`

## Notes
- Golden tests are located in `.spec/golden_tests/`
- Tests with `expected_valid: false` should fail validation
- Theme token validation requires a valid `theme.json`
- JUnit XML output is compatible with most CI/CD systems
- Verbose mode shows detailed validation output for debugging
- Failed tests indicate potential regressions or specification violations
