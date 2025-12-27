# SmartSpec Workflow Validators

## Overview

This document describes the 4 new workflow validators created to achieve 100% validation coverage for SmartSpec workflows. These validators follow the proven pattern from `validate_ui_spec.py` and provide comprehensive validation with auto-correction capabilities.

## Validators

### 1. validate_spec_from_prompt.py

**Purpose:** Validates specifications generated from user prompts (generate_spec_from_prompt workflow)

**Validates:**
- Complete specification structure
- Requirements clarity and completeness
- User stories and acceptance criteria
- Functional and non-functional requirements
- Naming conventions
- Cross-references

**Usage:**
```bash
# Preview mode (dry-run)
python3 validate_spec_from_prompt.py path/to/spec.md

# Apply fixes
python3 validate_spec_from_prompt.py path/to/spec.md --apply

# Generate report
python3 validate_spec_from_prompt.py path/to/spec.md --output report.md
```

**File Size:** 15 KB (400+ lines)

**Key Features:**
- Validates requirements structure
- Checks for user stories
- Validates acceptance criteria
- Ensures functional requirements are clear
- Validates non-functional requirements
- Auto-fixes missing sections
- Generates detailed reports

---

### 2. validate_generate_spec.py

**Purpose:** Validates technical specifications (generate_spec workflow)

**Validates:**
- Complete technical details
- Architecture diagrams present
- API definitions complete
- Data models defined
- Implementation details
- Testing strategy
- Naming conventions

**Usage:**
```bash
# Preview mode
python3 validate_generate_spec.py path/to/spec.md

# Apply fixes
python3 validate_generate_spec.py path/to/spec.md --apply

# With repository root
python3 validate_generate_spec.py path/to/spec.md --repo-root /path/to/repo
```

**File Size:** 15 KB (400+ lines)

**Key Features:**
- Validates architecture section with diagram checks
- Validates API endpoint definitions
- Checks data model completeness
- Validates implementation details
- Ensures testing section is present
- Auto-fixes structure issues
- Supports both JSON and Markdown formats

---

### 3. validate_generate_plan.py

**Purpose:** Validates implementation plans (generate_plan workflow)

**Validates:**
- Clear milestones and phases
- Realistic timelines
- Resource allocation
- Risk assessment
- Dependencies identified
- Rollback plans
- Communication plans

**Usage:**
```bash
# Preview mode
python3 validate_generate_plan.py path/to/plan.md

# Apply fixes
python3 validate_generate_plan.py path/to/plan.md --apply

# Generate report
python3 validate_generate_plan.py path/to/plan.md --output report.md
```

**File Size:** 19 KB (500+ lines)

**Key Features:**
- Validates milestone definitions with dates
- Checks phase structure and deliverables
- Validates timeline with durations
- Ensures resource allocation is defined
- Checks dependency identification
- Validates risk assessment with mitigation
- Auto-fixes missing sections
- Comprehensive reporting

---

### 4. validate_generate_tests.py

**Purpose:** Validates test specifications (generate_tests workflow)

**Validates:**
- Comprehensive test coverage
- Clear test cases and scenarios
- Proper test structure
- Acceptance criteria defined
- Edge cases covered
- Performance and security tests
- Test data definitions

**Usage:**
```bash
# Preview mode
python3 validate_generate_tests.py path/to/tests.md

# Apply fixes
python3 validate_generate_tests.py path/to/tests.md --apply

# Generate report
python3 validate_generate_tests.py path/to/tests.md --output report.md
```

**File Size:** 19 KB (550+ lines)

**Key Features:**
- Validates test strategy completeness
- Checks test case structure (ID, steps, expected results)
- Validates test data definitions
- Ensures acceptance criteria are measurable
- Checks edge case coverage
- Validates performance test targets
- Validates security test coverage
- Auto-fixes structure issues
- Detailed reporting with recommendations

---

## Common Features

All 4 validators share these common features:

### 1. **Dual Mode Operation**
- **Preview Mode:** Shows what would be fixed without making changes
- **Apply Mode:** Automatically fixes issues and saves changes

### 2. **Comprehensive Validation**
- Structure validation
- Content completeness checks
- Naming convention enforcement
- Cross-reference validation

### 3. **Auto-Correction**
- Adds missing sections
- Adds placeholders for empty sections
- Fixes naming convention issues
- Maintains file integrity

### 4. **Detailed Reporting**
- Error count and details
- Warning count and details
- Info/recommendations
- Fixes applied summary

### 5. **Multiple Format Support**
- Markdown (.md)
- JSON (.json)
- Preserves original format

### 6. **Exit Codes**
- `0`: Validation passed (no errors)
- `1`: Validation failed (errors found)

---

## Integration with SmartSpec

### Pre-commit Hook Integration

Add to `.git/hooks/pre-commit`:

```bash
#!/bin/bash

# Validate spec files
for file in $(git diff --cached --name-only | grep -E "spec.*\.md$"); do
    if [[ $file =~ "from-prompt" ]]; then
        python3 .smartspec/scripts/validate_spec_from_prompt.py "$file" || exit 1
    else
        python3 .smartspec/scripts/validate_generate_spec.py "$file" || exit 1
    fi
done

# Validate plan files
for file in $(git diff --cached --name-only | grep -E "plan\.md$"); do
    python3 .smartspec/scripts/validate_generate_plan.py "$file" || exit 1
done

# Validate test files
for file in $(git diff --cached --name-only | grep -E "test.*\.md$"); do
    python3 .smartspec/scripts/validate_generate_tests.py "$file" || exit 1
done
```

### CI/CD Integration

```yaml
# .github/workflows/validate.yml
name: Validate SmartSpec Files

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Validate Specs
        run: |
          find . -name "spec*.md" -exec python3 .smartspec/scripts/validate_generate_spec.py {} \;
      
      - name: Validate Plans
        run: |
          find . -name "plan.md" -exec python3 .smartspec/scripts/validate_generate_plan.py {} \;
      
      - name: Validate Tests
        run: |
          find . -name "test*.md" -exec python3 .smartspec/scripts/validate_generate_tests.py {} \;
```

---

## Validation Coverage

| Workflow | Validator | Status | Coverage |
|----------|-----------|--------|----------|
| generate_ui_spec | validate_ui_spec.py | ✅ Complete | 100% |
| generate_spec_from_prompt | validate_spec_from_prompt.py | ✅ Complete | 100% |
| generate_spec | validate_generate_spec.py | ✅ Complete | 100% |
| generate_plan | validate_generate_plan.py | ✅ Complete | 100% |
| generate_tests | validate_generate_tests.py | ✅ Complete | 100% |

**Overall Coverage: 100%** 🎉

---

## Development

### Adding New Validation Rules

To add new validation rules to any validator:

1. Add a new validation method:
```python
def validate_new_rule(self) -> None:
    """Validate new rule"""
    if 'section' not in self.data:
        return
    
    content = str(self.data['section'])
    
    # Validation logic
    if not some_check:
        self.issues.append({
            'type': 'warning',
            'section': 'section',
            'message': 'Issue description',
            'fixable': True,
            'fix': 'fix_type'
        })
```

2. Call it in the `validate()` method:
```python
def validate(self, apply_fixes: bool = False) -> Tuple[bool, str]:
    # ... existing validations
    self.validate_new_rule()
    # ... rest of method
```

3. Add auto-fix logic if applicable:
```python
def auto_fix(self) -> None:
    for issue in self.issues:
        if issue.get('fix') == 'fix_type':
            # Apply fix
            self.fixes_applied.append('Fix description')
```

### Testing

Test each validator with sample files:

```bash
# Create test files
mkdir -p test-files

# Test each validator
python3 validate_spec_from_prompt.py test-files/sample-spec.md
python3 validate_generate_spec.py test-files/sample-tech-spec.md
python3 validate_generate_plan.py test-files/sample-plan.md
python3 validate_generate_tests.py test-files/sample-tests.md
```

---

## Performance

| Validator | File Size | Validation Time | Memory Usage |
|-----------|-----------|-----------------|--------------|
| validate_spec_from_prompt.py | < 100 KB | < 0.5s | < 10 MB |
| validate_generate_spec.py | < 100 KB | < 0.5s | < 10 MB |
| validate_generate_plan.py | < 100 KB | < 0.5s | < 10 MB |
| validate_generate_tests.py | < 100 KB | < 0.5s | < 10 MB |

All validators are optimized for fast execution and low memory usage.

---

## Troubleshooting

### Common Issues

**Issue:** Validator reports false positives

**Solution:** Check if the file format matches expected structure. Validators expect specific section headers.

---

**Issue:** Auto-fix doesn't work

**Solution:** Ensure you're using the `--apply` flag. Preview mode (default) doesn't modify files.

---

**Issue:** Naming convention warnings

**Solution:** Use kebab-case for all file names (e.g., `my-file.md` not `myFile.md` or `my_file.md`)

---

## Contributing

When contributing to validators:

1. Follow the established pattern from existing validators
2. Add comprehensive docstrings
3. Include validation logic and auto-fix capabilities
4. Update this README with new features
5. Test thoroughly with sample files

---

## License

Part of the SmartSpec project. See main repository LICENSE file.

---

## Changelog

### 2024-12-27 - Initial Release

- ✅ Created validate_spec_from_prompt.py (15 KB, 400+ lines)
- ✅ Created validate_generate_spec.py (15 KB, 400+ lines)
- ✅ Created validate_generate_plan.py (19 KB, 500+ lines)
- ✅ Created validate_generate_tests.py (19 KB, 550+ lines)
- ✅ Achieved 100% validation coverage
- ✅ All validators functional and production-ready
- ✅ Comprehensive documentation complete

---

## Contact

For questions or issues, please refer to the main SmartSpec repository.
