---
workflow_id: smartspec_verify_ui_implementation
version: "6.0.0"
status: active
category: ui
platform_support:
  - cli
  - kilo
requires_apply: false
---

# smartspec_verify_ui_implementation

**Verify that UI implementation matches the A2UI specification.**

## Purpose

This workflow verifies that platform-specific UI implementation code correctly implements the A2UI specification. It checks component structure, data bindings, actions, accessibility compliance, and catalog adherence.

## Governance contract

This workflow MUST follow:
- `knowledge_base_smartspec_handbook.md` (v6)
- A2UI Specification v0.8
- `.spec/smartspec.config.yaml`
- `.spec/ui-catalog.json`
- WCAG-AA accessibility standards

## Prerequisites

**Required:**
- A2UI must be enabled in `.spec/smartspec.config.yaml`
- Valid UI specification file
- Implemented UI code (generated or manual)
- UI component catalog

**Optional:**
- Running application for runtime verification
- Test coverage reports
- Accessibility testing tools

## Invocation

### CLI

```bash
/smartspec_verify_ui_implementation \
  --spec specs/feature/spec-002-contact/ui-spec.json \
  --implementation src/ui/contact \
  --target-platform web
```

### Kilo Code

```bash
/smartspec_verify_ui_implementation.md \
  --spec specs/feature/spec-002-contact/ui-spec.json \
  --implementation src/ui/contact \
  --target-platform web \
  --platform kilo
```

## Flags

### Universal Flags

| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--platform` | string | No | Platform: cli, kilo (default: cli) |
| `--verbose` | boolean | No | Verbose output |
| `--report-dir` | path | No | Custom report directory |

### Workflow-Specific Flags

| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--spec` | path | Yes | Path to UI specification JSON file |
| `--implementation` | path | Yes | Path to implementation directory |
| `--target-platform` | string | Yes | Target platform: web, flutter, mobile |
| `--runtime-check` | boolean | No | Perform runtime verification (requires running app) |
| `--accessibility-check` | boolean | No | Run accessibility tests (default: true) |
| `--strict` | boolean | No | Strict mode - fail on warnings |
| `--fix` | boolean | No | Auto-fix issues where possible |

### Flag Usage Notes

**Runtime Check:**
- Requires application to be running
- Tests actual component behavior
- Validates data bindings at runtime
- Checks event handling

**Accessibility Check:**
- Runs automated accessibility tests
- Checks WCAG-AA compliance
- Validates ARIA labels
- Tests keyboard navigation

**Strict Mode:**
- Treats warnings as errors
- Fails verification if any issues found
- Recommended for CI/CD pipelines

**Fix Mode:**
- Attempts to auto-fix common issues
- Updates code where safe
- Generates fix suggestions for manual issues

## Behavior

### Standard Mode

1. **Validate Prerequisites**
   - Check A2UI is enabled
   - Verify UI spec exists and is valid
   - Check implementation directory exists
   - Validate catalog exists

2. **Parse UI Specification**
   - Load and validate UI spec JSON
   - Extract expected components
   - Extract data model
   - Extract actions and bindings

3. **Analyze Implementation**
   - Scan implementation directory
   - Parse component files
   - Extract component structure
   - Identify data bindings
   - Find event handlers

4. **Verify Component Structure**
   - Check all spec components exist
   - Verify component properties
   - Validate component hierarchy
   - Check component names

5. **Verify Data Bindings**
   - Check data model implementation
   - Verify two-way bindings
   - Validate data paths
   - Check default values

6. **Verify Actions**
   - Check action handlers exist
   - Verify action parameters
   - Validate event dispatching
   - Check action names

7. **Verify Catalog Adherence**
   - Check components match catalog
   - Verify security levels
   - Validate component properties
   - Check for unauthorized components

8. **Accessibility Verification**
   - Check ARIA labels
   - Verify keyboard navigation
   - Validate focus management
   - Check color contrast
   - Test screen reader support

9. **Generate Verification Report**
   - List all checks performed
   - Report passed/failed checks
   - Provide fix suggestions
   - Calculate compliance score

10. **Display Results**
    - Show summary statistics
    - List critical issues
    - Show warnings
    - Provide next steps

### Runtime Check Mode (`--runtime-check`)

**Additional steps:**

11. **Connect to Running Application**
    - Detect running dev server
    - Connect to application
    - Load test page

12. **Test Component Rendering**
    - Verify components render correctly
    - Check component visibility
    - Validate layout

13. **Test Data Bindings**
    - Set data values
    - Verify UI updates
    - Test two-way binding
    - Validate data synchronization

14. **Test Actions**
    - Trigger actions
    - Verify event dispatching
    - Check action handlers
    - Validate action results

15. **Test Interactions**
    - Simulate user input
    - Test form submission
    - Validate error handling
    - Check loading states

### Fix Mode (`--fix`)

**Additional steps:**

16. **Identify Fixable Issues**
    - Categorize issues by fixability
    - Prioritize critical issues

17. **Apply Automatic Fixes**
    - Fix missing ARIA labels
    - Add keyboard handlers
    - Fix data binding syntax
    - Update component names

18. **Generate Fix Suggestions**
    - Create code snippets for manual fixes
    - Provide step-by-step instructions
    - Link to documentation

19. **Re-verify After Fixes**
    - Run verification again
    - Report remaining issues

## Output

### Verification Report

```
.spec/reports/verify-ui-implementation/<run-id>/
├── report.md                      # Full verification report
├── summary.json                   # Machine-readable summary
├── issues.json                    # Detailed issues list
├── accessibility-report.html      # Accessibility test results
├── coverage.json                  # Verification coverage
└── fixes/                         # Auto-fix suggestions
    ├── ContactForm.ts.patch
    └── README.md
```

### Report Contents

**Summary:**
```markdown
# UI Implementation Verification Report

**Specification:** specs/feature/spec-002-contact/ui-spec.json
**Implementation:** src/ui/contact
**Platform:** web
**Date:** 2025-12-22

## Summary

- ✅ **Compliance Score:** 95%
- ✅ **Components:** 5/5 implemented
- ✅ **Data Bindings:** 8/8 correct
- ✅ **Actions:** 3/3 implemented
- ⚠️ **Accessibility:** 4/5 checks passed
- ✅ **Catalog Adherence:** 100%

## Status: PASS (with warnings)

---

## Component Verification

### ✅ ContactForm
- Structure: ✅ Correct
- Properties: ✅ All present
- Data bindings: ✅ Correct
- Actions: ✅ Implemented
- Accessibility: ⚠️ Missing ARIA label on submit button

### ✅ NameField
- Structure: ✅ Correct
- Properties: ✅ All present
- Data bindings: ✅ Correct
- Accessibility: ✅ WCAG-AA compliant

... (more components)

---

## Issues Found

### ⚠️ Warnings (1)

1. **Missing ARIA Label**
   - **Component:** SubmitButton
   - **Issue:** Button missing `aria-label` attribute
   - **Fix:** Add `aria-label="Send contact form"`
   - **File:** src/ui/contact/components/SubmitButton.ts:15

### ℹ️ Suggestions (2)

1. **Improve Keyboard Navigation**
   - **Component:** ContactForm
   - **Suggestion:** Add `Tab` key handler for better navigation
   - **File:** src/ui/contact/components/ContactForm.ts

2. **Add Loading State**
   - **Component:** SubmitButton
   - **Suggestion:** Add loading state during form submission
   - **File:** src/ui/contact/components/SubmitButton.ts

---

## Accessibility Report

### WCAG-AA Compliance: 80%

✅ **Passed (4/5):**
- Keyboard navigation
- Focus management
- Color contrast
- Semantic HTML

⚠️ **Failed (1/5):**
- ARIA labels (1 missing)

**Recommendations:**
- Add `aria-label` to SubmitButton
- Consider adding `aria-describedby` for error messages

---

## Next Steps

1. **Fix Critical Issues:** None found ✅
2. **Address Warnings:** Fix missing ARIA label
3. **Consider Suggestions:** Improve keyboard navigation
4. **Re-verify:** Run verification again after fixes

**Command to re-verify:**
```bash
/smartspec_verify_ui_implementation \
  --spec specs/feature/spec-002-contact/ui-spec.json \
  --implementation src/ui/contact \
  --target-platform web
```
```

## Example Usage

### Example 1: Basic Verification

**Verify implementation:**
```bash
/smartspec_verify_ui_implementation \
  --spec specs/feature/spec-002-contact/ui-spec.json \
  --implementation src/ui/contact \
  --target-platform web
```

**Output:**
```
✅ Compliance Score: 95%
✅ Components: 5/5 implemented
⚠️ Accessibility: 4/5 checks passed

Status: PASS (with warnings)

Report: .spec/reports/verify-ui-implementation/20251222-143022/report.md
```

### Example 2: Strict Mode (CI/CD)

**Verify with strict mode:**
```bash
/smartspec_verify_ui_implementation \
  --spec specs/feature/spec-003-dashboard/ui-spec.json \
  --implementation src/ui/dashboard \
  --target-platform web \
  --strict
```

**Output:**
```
❌ Compliance Score: 95%
❌ Status: FAIL (strict mode)

Issues:
- ⚠️ Missing ARIA label on submit button

Fix issues and re-run verification.
```

### Example 3: Runtime Verification

**Verify with runtime checks:**
```bash
# Start dev server first
npm run dev

# Run verification
/smartspec_verify_ui_implementation \
  --spec specs/feature/spec-002-contact/ui-spec.json \
  --implementation src/ui/contact \
  --target-platform web \
  --runtime-check
```

**Output:**
```
✅ Static Analysis: PASS
✅ Runtime Checks: PASS
  ✅ Components render correctly
  ✅ Data bindings work
  ✅ Actions dispatch events
  ✅ Form submission works

Status: PASS
```

### Example 4: Auto-Fix Issues

**Verify and fix:**
```bash
/smartspec_verify_ui_implementation \
  --spec specs/feature/spec-002-contact/ui-spec.json \
  --implementation src/ui/contact \
  --target-platform web \
  --fix
```

**Output:**
```
🔧 Auto-fixing issues...

✅ Fixed: Added ARIA label to SubmitButton
✅ Fixed: Added keyboard handler to ContactForm

⚠️ Manual fix required: Add loading state to SubmitButton
   See: .spec/reports/verify-ui-implementation/.../fixes/README.md

Re-running verification...

✅ Compliance Score: 100%
✅ Status: PASS
```

### Example 5: Flutter Verification

**Verify Flutter implementation:**
```bash
/smartspec_verify_ui_implementation \
  --spec specs/feature/spec-003-dashboard/ui-spec.json \
  --implementation lib/ui/dashboard \
  --target-platform flutter
```

**Checks:**
- Widget structure
- State management
- Data bindings (setState, Provider, etc.)
- Navigation
- Accessibility (Semantics widgets)

## Verification Checks

### Component Structure (Weight: 25%)

- ✅ All spec components exist
- ✅ Component hierarchy matches spec
- ✅ Component names correct
- ✅ Component properties present

### Data Bindings (Weight: 25%)

- ✅ Data model implemented
- ✅ Two-way bindings work
- ✅ Data paths correct
- ✅ Default values set

### Actions (Weight: 20%)

- ✅ Action handlers exist
- ✅ Event dispatching correct
- ✅ Action parameters match
- ✅ Error handling present

### Catalog Adherence (Weight: 15%)

- ✅ Components in catalog
- ✅ Security levels respected
- ✅ No unauthorized components
- ✅ Component properties match catalog

### Accessibility (Weight: 15%)

- ✅ ARIA labels present
- ✅ Keyboard navigation works
- ✅ Focus management correct
- ✅ Color contrast WCAG-AA
- ✅ Screen reader support

## Compliance Score Calculation

```
Score = (
  Component Structure * 0.25 +
  Data Bindings * 0.25 +
  Actions * 0.20 +
  Catalog Adherence * 0.15 +
  Accessibility * 0.15
) * 100

Pass: Score >= 80%
Fail: Score < 80%
```

## Evidence sources

When answering questions, the agent MUST read:

1) **Knowledge base**
   - `knowledge_base_smartspec_handbook.md`
   - `knowledge_base_smartspec_install_and_usage.md`
   - `.smartspec/WORKFLOW_PARAMETERS_REFERENCE.md`

2) **A2UI Resources**
   - A2UI Specification v0.8
   - `.spec/ui-catalog.json`
   - `docs/a2ui/A2UI_SmartSpec_Integration_Report.md`

3) **Configuration**
   - `.spec/smartspec.config.yaml` (a2ui section)

4) **UI Specification**
   - The UI spec file specified in `--spec`

5) **Implementation Code**
   - Files in `--implementation` directory

## Best Practices

### When to Verify

**Always verify:**
- After generating implementation
- Before committing code
- In CI/CD pipeline
- After manual changes

**Use strict mode:**
- In CI/CD pipelines
- Before production deployment
- For critical features

### Fixing Issues

**Priority order:**
1. Critical issues (blocking)
2. Accessibility issues
3. Data binding issues
4. Suggestions

**Auto-fix when:**
- Issue is simple and safe
- Fix doesn't change logic
- Fix is well-defined

**Manual fix when:**
- Issue requires design decision
- Fix affects business logic
- Multiple solutions possible

## Troubleshooting

### Error: "Implementation directory not found"

**Solution:** Check path:
```bash
ls -la src/ui/contact
```

### Error: "Cannot parse component files"

**Solution:** Ensure files are valid TypeScript/Dart:
```bash
# TypeScript
npx tsc --noEmit

# Dart
flutter analyze
```

### Error: "Runtime check failed - app not running"

**Solution:** Start dev server:
```bash
npm run dev
# or
flutter run
```

### Warning: "Component not in catalog"

**Solution:** Either:
1. Add component to catalog
2. Remove component from implementation
3. Update spec to use approved components

## Related Workflows

**Before verifying:**

1. **Implement UI:**
   ```bash
   /smartspec_implement_ui_from_spec \
     --spec specs/feature/spec-002-contact/ui-spec.json \
     --target-platform web \
     --output-dir src/ui/contact \
     --apply
   ```

**After verifying:**

2. **Fix issues and re-verify:**
   ```bash
   # Fix issues manually or with --fix
   /smartspec_verify_ui_implementation \
     --spec specs/feature/spec-002-contact/ui-spec.json \
     --implementation src/ui/contact \
     --target-platform web \
     --fix
   ```

3. **Update tasks:**
   ```bash
   /smartspec_verify_tasks_progress_strict \
     specs/feature/spec-002-contact/spec.md
   ```

## Security Considerations

- **Catalog validation** - Ensures only approved components used
- **Code injection check** - Validates no malicious code
- **Data validation** - Checks data bindings are safe
- **XSS prevention** - Validates proper escaping

## Version History

- **6.0.0** (2025-12-22): Initial release with A2UI v0.8 support

---

**Status:** Active  
**Requires Apply:** No (read-only verification)  
**Platform Support:** CLI, Kilo  
**Category:** UI Verification
