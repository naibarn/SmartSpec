# SmartSpec Golden Test Cases

This directory contains **golden test cases** for validating A2UI v0.8 JSON output. These tests ensure that SmartSpec workflows generate valid, accessible, and well-structured A2UI specifications.

## Purpose

Golden test cases serve as:
- **Reference implementations** for A2UI v0.8 components
- **Validation benchmarks** for automated testing
- **Documentation** of expected A2UI structure
- **Quality assurance** for SmartSpec output

## Test Categories

### 1. Basic Components (`01_*.json`)
Simple, single-component tests covering fundamental UI elements:
- Buttons
- Inputs
- Text
- Images

### 2. Forms (`02_*.json`)
Form-related tests with validation and accessibility:
- Input validation
- Required fields
- Error messages
- Form submission

### 3. Theming (`03_*.json`)
Tests for theme token usage and design system integration:
- Theme token references
- Component variants
- Style consistency

### 4. Complex Layouts (`04_*.json`)
Multi-component layouts with nesting:
- Dashboards
- Grids
- Nested components
- Section layouts

### 5. Error Scenarios (`05_*.json`, `06_*.json`)
Tests that should **fail validation**:
- Missing accessibility
- Invalid theme tokens
- Malformed structure

### 6. Interactions (`07_*.json`)
Interactive components with state and events:
- Modals
- Dropdowns
- State management
- Event handlers

### 7. Data Binding (`08_*.json`)
Dynamic components with data sources:
- Lists
- Tables
- Pagination
- Data binding syntax

## Test Structure

Each golden test case is a JSON file with the following structure:

```json
{
  "test_id": "unique_test_identifier",
  "name": "Human-readable test name",
  "description": "Detailed description of what this test validates",
  "category": "test_category",
  "a2ui_version": "0.8",
  "expected_valid": true,
  "input": {
    // Input specification
  },
  "expected_output": {
    // Expected A2UI JSON output
  },
  "expected_errors": [
    // Expected validation errors (for invalid tests)
  ],
  "validation_rules": [
    {
      "rule": "rule_name",
      "description": "What this rule validates",
      "should_fail": false
    }
  ],
  "metadata": {
    "created_at": "2025-12-22",
    "author": "SmartSpec Team",
    "tags": ["tag1", "tag2"]
  }
}
```

## Validation Rules

Common validation rules used across test cases:

| Rule | Description | Applies To |
|------|-------------|------------|
| `has_version` | Must have version field | All |
| `has_type` | Must have type field | All |
| `has_component` | Must have component object | Components |
| `has_accessibility` | Must have accessibility object | All components |
| `has_theme_references` | Must use theme tokens | Themed components |
| `valid_theme_tokens` | Theme tokens must exist | Themed components |
| `has_validation` | Form fields must have validation | Forms |
| `has_event_handlers` | Interactive elements must have events | Interactive |
| `has_data_source` | Lists must have data source | Data-driven |

## Running Tests

Use the `smartspec_validate_golden_tests` workflow to run all golden tests:

```bash
# Run all tests
/smartspec_validate_golden_tests

# Run specific category
/smartspec_validate_golden_tests --category basic_components

# Run with detailed output
/smartspec_validate_golden_tests --verbose true
```

## Adding New Tests

To add a new golden test case:

1. **Create a new JSON file** in this directory
2. **Follow the naming convention**: `##_descriptive_name.json`
3. **Include all required fields** (test_id, name, description, etc.)
4. **Define validation rules** that apply to this test
5. **Add metadata** with tags for categorization
6. **Test your test** using the validation workflow

## Test Coverage

Current test coverage:

| Category | Test Count | Coverage |
|----------|------------|----------|
| Basic Components | 1 | ✅ Button |
| Forms | 1 | ✅ Validation |
| Theming | 1 | ✅ Theme tokens |
| Complex Layouts | 1 | ✅ Dashboard |
| Error Scenarios | 2 | ✅ Accessibility, Theme |
| Interactions | 1 | ✅ Modal |
| Data Binding | 1 | ✅ List |
| **Total** | **8** | **Comprehensive** |

## A2UI v0.8 Compliance

All golden tests are designed to comply with **A2UI v0.8 specification**:

- ✅ Version field required
- ✅ Type field required (component, layout, etc.)
- ✅ Accessibility object required for all components
- ✅ Theme token references supported
- ✅ Event handlers for interactive elements
- ✅ Data binding syntax for dynamic content
- ✅ State management for stateful components

## References

- [A2UI v0.8 Specification](https://a2ui.dev/spec/v0.8)
- [SmartSpec Documentation](../../README.md)
- [Validation Workflow](../../.smartspec/workflows/smartspec_validate_golden_tests.md)

## Maintenance

Golden tests should be updated when:
- A2UI specification changes
- New component types are added
- Validation rules are updated
- Issues are discovered in existing tests

Last updated: 2025-12-22
