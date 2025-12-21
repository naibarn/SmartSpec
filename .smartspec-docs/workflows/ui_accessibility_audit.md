| manual_name | manual_version | compatible_workflow | compatible_workflow_versions |
|-------------|----------------|---------------------|------------------------------|
| /smartspec_ui_accessibility_audit Manual (EN) | 6.0 | /smartspec_ui_accessibility_audit | 6.0.x |

# /smartspec_ui_accessibility_audit Manual (v6.0, English)

## 1. Overview

This manual explains how to use the workflow:

The `/smartspec_ui_accessibility_audit` workflow performs comprehensive WCAG 2.1 accessibility compliance audits on UI components, ensuring inclusive design and legal compliance with accessibility standards.

**Purpose:** Audit UI components for WCAG 2.1 Level A/AA/AAA compliance, identify accessibility issues, and provide actionable recommendations for remediation.

**Version:** 6.0  
**Category:** ui_optimization_and_analytics

---

## 2. Usage

This workflow supports invocation via the Command Line Interface (CLI) and Kilo Code (internal scripting environment).

### 🔗 CLI Usage

The CLI invocation requires specifying the UI spec, implementation, and compliance level.

```bash
/smartspec_ui_accessibility_audit \
  --spec <path/to/ui-spec.json> \
  --implementation <path/to/implementation> \
  --level <A|AA|AAA> \
  [--auto-fix] \
  [--ignore-minor]
```

### Kilo Code Usage

The Kilo Code invocation is identical to the CLI structure, typically used within automated pipelines or internal scripts.

**Important:** When using Kilo Code, you MUST include `--platform kilo` flag.

```bash
/smartspec_ui_accessibility_audit.md \
  --spec <path/to/ui-spec.json> \
  --implementation <path/to/implementation> \
  --level <A|AA|AAA> \
  [--auto-fix] \
  [--ignore-minor] \
  --platform kilo
```

---

## 3. Use Cases

### Use Case 1: WCAG AA Compliance Audit (CLI)

**Scenario:** A developer needs to verify that a contact form meets WCAG AA accessibility standards before deployment.

**Command:**

```bash
/smartspec_ui_accessibility_audit \
  --spec specs/feature/spec-005-contact/ui-spec.json \
  --implementation src/ui/ContactForm.tsx \
  --level AA
```

**Expected Result:**

1. The workflow analyzes the UI implementation.
2. Checks semantic HTML, ARIA attributes, keyboard navigation.
3. Validates color contrast, focus management, form labels.
4. Generates detailed accessibility report with issues.
5. Reports pass rate (≥80% required for pass).
6. Exit code `0` if pass (≥80%), `1` if fail (<80%).

### Use Case 2: Automated Audit with Auto-Fix (Kilo Code)

**Scenario:** A CI pipeline runs accessibility audits and automatically fixes simple issues.

**Command (Kilo Code Snippet):**

```bash
/smartspec_ui_accessibility_audit.md \
  --spec specs/feature/spec-005-contact/ui-spec.json \
  --implementation src/ui/ContactForm.tsx \
  --level AA \
  --auto-fix \
  --platform kilo
```

**Expected Result:**

1. The workflow audits accessibility compliance.
2. Identifies fixable issues (missing alt text, ARIA labels).
3. With `--auto-fix`, applies automatic fixes to code.
4. Generates report with fixed and remaining issues.
5. Exit code `0` (Success).

### Use Case 3: Comprehensive AAA Audit (CLI)

**Scenario:** A government project requires maximum WCAG AAA accessibility compliance.

**Command:**

```bash
/smartspec_ui_accessibility_audit \
  --spec specs/feature/spec-005-contact/ui-spec.json \
  --implementation src/ui/ContactForm.tsx \
  --level AAA \
  --json
```

**Expected Result:**

1. The workflow performs comprehensive AAA audit.
2. Checks all WCAG AAA success criteria.
3. Reports critical, serious, moderate, and minor issues.
4. Output includes `audit-report.json` with detailed results.
5. Exit code `0` if pass, `1` if fail.

---

## 4. Parameters

The following parameters and flags control the execution and behavior of the `/smartspec_ui_accessibility_audit` workflow.

### Required Parameters

| Parameter | Type | Description | Validation |
| :--- | :--- | :--- | :--- |
| `--spec` | `<string>` | Path to UI specification JSON file. | Must exist and be valid JSON. |
| `--implementation` | `<string>` | Path to implementation file or directory. | Must exist and be accessible. |
| `--level` | `<string>` | WCAG compliance level: `A`, `AA`, or `AAA`. | Must be one of the allowed values. |

### Universal Flags

| Flag | Description | Default | Platform Support |
| :--- | :--- | :--- | :--- |
| `--config` | Path to the SmartSpec configuration file. | `.spec/smartspec.config.yaml` | `cli` \| `kilo` \| `ci` \| `other` |
| `--lang` | Language for report generation (e.g., `th`, `en`). | (System default) | `cli` \| `kilo` \| `ci` \| `other` |
| `--platform` | Execution platform context. **Required for Kilo Code.** | (Inferred) | `cli` \| `kilo` \| `ci` \| `other` |
| `--out` | Base path for safe outputs. | `.spec/reports/ui-accessibility/` | `cli` \| `kilo` \| `ci` \| `other` |
| `--json` | Output in JSON format. | `false` | `cli` \| `kilo` \| `ci` \| `other` |
| `--quiet` | Suppress standard output logs. | `false` | `cli` \| `kilo` \| `ci` \| `other` |

### Workflow-Specific Flags

| Flag | Description | Platform Support |
| :--- | :--- | :--- |
| `--auto-fix` | Automatically fix simple accessibility issues. | `cli` \| `kilo` \| `ci` \| `other` |
| `--ignore-minor` | Ignore minor severity issues in pass/fail calculation. | `cli` \| `kilo` \| `ci` \| `other` |

---

## 5. Output

The workflow generates output artifacts according to its configuration.

### Output Files

| File Path | Description |
| :--- | :--- |
| `.spec/reports/ui-accessibility/<run-id>/audit-report.md` | Detailed accessibility audit report. |
| `.spec/reports/ui-accessibility/<run-id>/summary.json` | JSON summary of audit results. |
| `.spec/reports/ui-accessibility/<run-id>/issues.csv` | CSV export of all issues for tracking. |

### Report Structure

The audit report includes:
- **Summary:** Total issues, pass rate, status
- **Critical Issues:** Blockers for accessibility
- **Serious Issues:** Major accessibility problems
- **Moderate Issues:** Important improvements needed
- **Minor Issues:** Nice-to-have enhancements
- **Recommendations:** Prioritized action items
- **WCAG Mapping:** Issues mapped to WCAG criteria

---

## 6. Accessibility Checks

### WCAG 2.1 Compliance Areas

The workflow audits the following areas:

#### Perceivable
- **Text Alternatives:** Alt text for images
- **Time-based Media:** Captions and transcripts
- **Adaptable:** Semantic HTML structure
- **Distinguishable:** Color contrast, text sizing

#### Operable
- **Keyboard Accessible:** Full keyboard navigation
- **Enough Time:** No time limits or adjustable
- **Seizures:** No flashing content
- **Navigable:** Skip links, focus indicators

#### Understandable
- **Readable:** Clear language, readable text
- **Predictable:** Consistent navigation
- **Input Assistance:** Form labels, error messages

#### Robust
- **Compatible:** Valid HTML, ARIA usage
- **Parsing:** No markup errors
- **Name, Role, Value:** Proper ARIA implementation

---

## 7. Pass/Fail Criteria

### Pass Threshold

- **Pass:** ≥ 80% compliance
- **Fail:** < 80% compliance

### Issue Severity Weighting

| Severity | Weight | Impact on Score |
| :--- | :--- | :--- |
| Critical | 10 | Major deduction |
| Serious | 5 | Significant deduction |
| Moderate | 2 | Moderate deduction |
| Minor | 1 | Small deduction |

---

## 8. Notes

- **Platform Flag:** When using Kilo Code, always include `--platform kilo` to ensure proper context and logging.
- **Auto-Fix Safety:** Auto-fix only applies to simple, safe fixes (alt text, ARIA labels). Complex issues require manual review.
- **Level Selection:** Use AA for most projects (recommended), AAA for government/healthcare.
- **CI Integration:** Run audits in CI pipeline to catch accessibility issues early.
- **Screen Reader Testing:** Automated audits complement but don't replace manual screen reader testing.
- **Configuration:** The workflow respects settings in `.spec/smartspec.config.yaml`.

---

**End of Manual**
