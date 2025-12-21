---
name: /smartspec_ui_accessibility_audit
version: 1.0.0
role: verification
description: Automated accessibility audit for A2UI implementations against WCAG 2.1 AA standards
workflow: /smartspec_ui_accessibility_audit
---

# smartspec_ui_accessibility_audit

> **Canonical path:** `.smartspec/workflows/smartspec_ui_accessibility_audit.md`  
> **Version:** 1.0.0  
> **Status:** Production Ready  
> **Category:** verification

## Purpose

Perform automated accessibility audits on UI implementations:

- WCAG 2.1 Level AA compliance checking
- Semantic HTML validation
- ARIA attributes verification
- Keyboard navigation testing
- Color contrast analysis
- Screen reader compatibility

This workflow ensures UI implementations meet accessibility standards.

---

## Governance contract

This workflow MUST follow:

- `knowledge_base_smartspec_handbook.md` (v6)
- `.spec/smartspec.config.yaml`

### Write scopes (enforced)

Allowed writes:

- Report outputs: `.spec/reports/ui-accessibility-audit/**` (no `--apply` required)

Forbidden writes (must hard-fail):

- Any path outside config `safety.allow_writes_only_under`
- Any source code modifications
- Any governed artifacts

### `--apply` behavior

This workflow is **report-only** and does not require `--apply`.

---

## Invocation

### CLI

```bash
/smartspec_ui_accessibility_audit \
  --spec specs/feature/spec-003-profile/ui-spec.json \
  --implementation src/ui/profile/ \
  [--json]
```

### Kilo Code

```bash
/smartspec_ui_accessibility_audit.md \
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
| `--level` | No | WCAG level (`A`, `AA`, `AAA`; default: `AA`) |
| `--ignore-warnings` | No | Only report errors, skip warnings |
| `--auto-fix` | No | Generate auto-fix suggestions |

### Flag usage notes

- `--spec` must point to valid A2UI specification
- `--implementation` must contain UI implementation files
- `--level AA` is recommended (default)
- `--auto-fix` provides actionable fix suggestions

---

## Behavior

### 1) Load UI spec and implementation

- Read A2UI specification
- Scan implementation directory
- Identify all UI components

### 2) Semantic HTML validation

Check for:

- Proper HTML5 semantic elements
- Heading hierarchy (h1-h6)
- Landmark regions (header, nav, main, footer)
- List structures (ul, ol, dl)
- Form labels and fieldsets

### 3) ARIA attributes verification

Verify:

- ARIA roles correctness
- ARIA properties completeness
- ARIA states validity
- ARIA relationships (aria-labelledby, aria-describedby)
- No redundant ARIA (when semantic HTML sufficient)

### 4) Keyboard navigation testing

Test:

- Tab order logical
- Focus indicators visible
- Keyboard shortcuts functional
- Skip links present
- Focus trap prevention

### 5) Color contrast analysis

Check:

- Text contrast ratio (4.5:1 for normal text, 3:1 for large text)
- Interactive element contrast
- Focus indicator contrast
- Disabled state contrast

### 6) Screen reader compatibility

Verify:

- Alt text for images
- Form labels associated
- Button text descriptive
- Link text meaningful
- Hidden content properly marked

### 7) Additional checks

- Form validation accessible
- Error messages clear
- Loading states announced
- Dynamic content updates announced
- Modal dialogs accessible

### 8) Generate report

Write comprehensive accessibility report.

---

## Output

### Report structure

**report.md:**

```markdown
# UI Accessibility Audit Report

## Summary
- **Overall Score:** 85/100 (Good)
- **WCAG Level:** AA
- **Errors:** 2
- **Warnings:** 5
- **Passed:** 23

## Critical Issues (Errors)

### 1. Missing alt text on image
- **Component:** ProfileAvatar
- **File:** src/ui/profile/ProfileAvatar.ts:45
- **Issue:** `<img>` element missing `alt` attribute
- **WCAG:** 1.1.1 Non-text Content (Level A)
- **Impact:** Screen readers cannot describe image
- **Fix:** Add `alt="User profile avatar"` to image element

### 2. Insufficient color contrast
- **Component:** SubmitButton
- **File:** src/ui/profile/SubmitButton.ts:22
- **Issue:** Text contrast ratio 3.2:1 (requires 4.5:1)
- **WCAG:** 1.4.3 Contrast (Minimum) (Level AA)
- **Impact:** Low vision users may not read text
- **Fix:** Darken text color to #1a1a1a or lighten background

## Warnings

### 1. Heading hierarchy skip
- **Component:** ProfileForm
- **File:** src/ui/profile/ProfileForm.ts:12
- **Issue:** Jumps from h2 to h4 (skips h3)
- **WCAG:** 1.3.1 Info and Relationships (Level A)
- **Impact:** Screen reader navigation confusing
- **Fix:** Change h4 to h3

## Passed Checks (23)

✅ Semantic HTML structure  
✅ ARIA roles correct  
✅ Keyboard navigation functional  
✅ Focus indicators visible  
✅ Form labels associated  
✅ Button text descriptive  
... (17 more)

## Recommendations

1. **High Priority:** Fix missing alt text (blocks Level A)
2. **High Priority:** Fix color contrast (blocks Level AA)
3. **Medium Priority:** Fix heading hierarchy
4. **Low Priority:** Add skip links for keyboard users
5. **Low Priority:** Enhance error message clarity

## Compliance Status

- **WCAG 2.1 Level A:** ❌ FAILED (1 error)
- **WCAG 2.1 Level AA:** ❌ FAILED (2 errors)
- **WCAG 2.1 Level AAA:** ❌ FAILED (2 errors + 5 warnings)

**Action Required:** Fix 2 errors to achieve Level AA compliance
```

**summary.json:**

```json
{
  "status": "failed",
  "score": 85,
  "level": "AA",
  "errors": 2,
  "warnings": 5,
  "passed": 23,
  "compliance": {
    "level_a": false,
    "level_aa": false,
    "level_aaa": false
  },
  "issues": [
    {
      "severity": "error",
      "component": "ProfileAvatar",
      "file": "src/ui/profile/ProfileAvatar.ts",
      "line": 45,
      "rule": "1.1.1",
      "description": "Missing alt text on image",
      "fix": "Add alt attribute to img element"
    }
  ],
  "timestamp": "2025-12-22T00:00:00Z"
}
```

---

## Compliance levels

### WCAG 2.1 Level A (Minimum)

Essential accessibility features:

- Text alternatives for non-text content
- Captions for audio/video
- Adaptable content structure
- Distinguishable content
- Keyboard accessible
- Enough time to read/use
- No seizure-inducing content
- Navigable
- Readable
- Predictable
- Input assistance

### WCAG 2.1 Level AA (Recommended)

Enhanced accessibility:

- Captions for live audio
- Audio descriptions for video
- Contrast ratio 4.5:1
- Text resize up to 200%
- Images of text avoided
- Multiple ways to find pages
- Headings and labels descriptive
- Focus visible
- Language of page identified
- Consistent navigation
- Error identification
- Labels or instructions provided

### WCAG 2.1 Level AAA (Optimal)

Highest level of accessibility:

- Sign language interpretation
- Extended audio descriptions
- Contrast ratio 7:1
- No images of text
- Context-sensitive help
- Error prevention

---

## Auto-fix suggestions

When `--auto-fix` is used, provides actionable fixes:

```markdown
## Auto-Fix Suggestions

### Fix 1: Add alt text to ProfileAvatar

**File:** src/ui/profile/ProfileAvatar.ts:45

**Current:**
```typescript
<img src={avatarUrl} class="avatar" />
```

**Suggested:**
```typescript
<img src={avatarUrl} alt="User profile avatar" class="avatar" />
```

### Fix 2: Improve color contrast for SubmitButton

**File:** src/ui/profile/SubmitButton.ts:22

**Current:**
```css
color: #666666;
background: #ffffff;
```

**Suggested:**
```css
color: #1a1a1a; /* Contrast ratio: 16.1:1 */
background: #ffffff;
```
```

---

## Error handling

### Invalid spec

If UI spec is invalid:

- Report spec validation errors
- Cannot proceed with audit
- Exit with code 1

### Implementation not found

If implementation directory doesn't exist:

- Report missing implementation
- Cannot proceed with audit
- Exit with code 1

### Partial implementation

If some components not implemented:

- Audit implemented components only
- Report missing components
- Continue with available components

---

## Usage examples

### Example 1: Basic audit

```bash
/smartspec_ui_accessibility_audit \
  --spec specs/feature/spec-003-profile/ui-spec.json \
  --implementation src/ui/profile/
```

### Example 2: Strict Level AAA audit

```bash
/smartspec_ui_accessibility_audit \
  --spec specs/feature/spec-003-profile/ui-spec.json \
  --implementation src/ui/profile/ \
  --level AAA
```

### Example 3: With auto-fix suggestions

```bash
/smartspec_ui_accessibility_audit \
  --spec specs/feature/spec-003-profile/ui-spec.json \
  --implementation src/ui/profile/ \
  --auto-fix
```

### Example 4: Kilo Code

```bash
/smartspec_ui_accessibility_audit.md \
  --spec specs/feature/spec-003-profile/ui-spec.json \
  --implementation src/ui/profile/ \
  --platform kilo \
  --json
```

---

## Integration

This workflow integrates with:

- `smartspec_verify_ui_implementation` - Accessibility as part of verification
- `smartspec_verify_tasks_progress_strict` - Include accessibility in task verification
- `smartspec_quality_gate` - Accessibility as quality gate criterion
- CI/CD pipelines - Automated accessibility testing

---

## Best practices

1. **Run early and often** - Catch accessibility issues early
2. **Aim for Level AA** - Industry standard for accessibility
3. **Use auto-fix** - Get actionable suggestions
4. **Integrate with CI** - Block merges on accessibility failures
5. **Manual testing** - Automated tools catch ~30-50% of issues
6. **User testing** - Test with real assistive technology users

---

## Limitations

Automated accessibility testing has limitations:

- **Cannot test:** Meaningful alt text quality, logical reading order, user experience
- **Can test:** Technical compliance, ARIA correctness, contrast ratios
- **Recommendation:** Combine automated testing with manual testing and user feedback

---

## Security considerations

- Audit does not modify source code
- Reports may contain sensitive information (file paths, code snippets)
- Store reports securely
- Review reports before sharing externally

---

# End of workflow doc
