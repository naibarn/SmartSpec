# `/smartspec_generate_ui_spec` - Generate UI Specification

| Metadata | Value |
|----------|-------|
| **Workflow ID** | `smartspec_generate_ui_spec` |
| **Category** | UI / A2UI |
| **Version** | 6.0.0+ |
| **Requires `--apply`** | Yes |
| **Platform Support** | CLI, Kilo Code |

---

## Overview

Generate A2UI-compliant UI specification from natural language requirements. This workflow creates a governed, platform-agnostic UI specification in A2UI format that serves as the single source of truth for implementing UIs across multiple platforms (Web, Flutter, React, etc.).

The generated `ui-spec.json` follows the A2UI v0.8 specification and includes component structure, layout, styling, interactions, and accessibility requirements.

---

## Usage

### CLI

```bash
/smartspec_generate_ui_spec \
  --requirements "Create restaurant booking form with date picker, time selector, guest count, and special requests" \
  --spec specs/feature/spec-001-booking/ui-spec.json
```

### Kilo Code

```bash
/smartspec_generate_ui_spec.md \
  --requirements "Create restaurant booking form with date picker, time selector, guest count, and special requests" \
  --spec specs/feature/spec-001-booking/ui-spec.json \
  --platform kilo
```

---

## Use Cases

### 1. Generate UI Spec from Requirements

**Scenario:** Create a UI specification for a new booking form feature.

**Command:**
```bash
/smartspec_generate_ui_spec \
  --requirements "Create restaurant booking form with date picker, time selector, guest count, and special requests" \
  --spec specs/feature/spec-001-booking/ui-spec.json \
  --target-platform web \
  --accessibility wcag-aa
```

**Expected Result:** A complete `ui-spec.json` file with form components, validation rules, and accessibility attributes.

### 2. Generate UI Spec with Design Reference

**Scenario:** Create UI specification based on a design mockup.

**Command:**
```bash
/smartspec_generate_ui_spec \
  --requirements "Implement the dashboard layout from the mockup" \
  --spec specs/feature/spec-002-dashboard/ui-spec.json \
  --mockup designs/dashboard-mockup.png \
  --style material
```

**Expected Result:** UI specification matching the design mockup with Material Design components.

### 3. Interactive UI Spec Generation

**Scenario:** Generate UI spec with iterative refinement.

**Command:**
```bash
/smartspec_generate_ui_spec \
  --requirements "Create user profile edit page" \
  --spec specs/feature/spec-003-profile/ui-spec.json \
  --interactive \
  --context-spec specs/feature/spec-003-profile/spec.md
```

**Expected Result:** Interactive session where you can refine the UI spec based on preview and feedback.

---

## Parameters

### Required Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `--requirements` | string | Natural language UI requirements (inline or file path) |
| `--spec` | path | Path to save the generated ui-spec.json file |

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
| `--target-platform` | string | web | Target platform: web, flutter, mobile, all |
| `--catalog` | path | .spec/ui-catalog.json | Path to component catalog |
| `--style` | string | from config | Style preset: material, fluent, custom |
| `--accessibility` | string | from config | Accessibility level: basic, wcag-aa, wcag-aaa |
| `--interactive` | boolean | false | Enable interactive mode with refinement |
| `--context-spec` | path | - | Path to functional spec for context |
| `--mockup` | path | - | Path to design mockup/reference image |

---

## Output

### Report Location
```
.spec/reports/generate-ui-spec/<run-id>/
├── report.md              # Human-readable summary
├── report.json            # Machine-readable data
└── preview/
    ├── ui-spec.json       # Preview of generated spec
    └── mockup.png         # Visual preview (if applicable)
```

### Generated Files (with `--apply`)
- `<spec-path>` - A2UI-compliant UI specification JSON file

### UI Spec Structure
```json
{
  "version": "0.8",
  "metadata": { ... },
  "components": [ ... ],
  "layout": { ... },
  "styling": { ... },
  "interactions": [ ... ],
  "accessibility": { ... },
  "validation": { ... }
}
```

---

## Prerequisites

**Required:**
- A2UI must be enabled in `.spec/smartspec.config.yaml` (`a2ui.enabled: true`)
- UI component catalog must exist (`.spec/ui-catalog.json`) or preset must be configured

**Optional:**
- Existing functional specification for context
- Design references or mockups
- Accessibility requirements

---

## Notes

1. **Preview First:** Always run without `--apply` first to review the generated UI spec
2. **Requirements Format:** Can be inline string or path to requirements file
3. **Platform Agnostic:** Generated spec works across web, mobile, and desktop platforms
4. **Catalog Reuse:** Automatically reuses components from existing catalog
5. **Accessibility:** Follows WCAG guidelines when `--accessibility` is specified
6. **Interactive Mode:** Use `--interactive` for iterative refinement with visual feedback
7. **Design Integration:** Use `--mockup` to generate spec from design files

---

## Related Workflows

- [`/smartspec_generate_ui_implementation`](./generate_ui_implementation.md) - Generate UI code from spec
- [`/smartspec_ui_catalog_generator`](./ui_catalog_generator.md) - Generate component catalog
- [`/smartspec_ui_validation`](./ui_validation_manual.md) - Validate UI implementation
- [`/smartspec_ui_component_audit`](./ui_component_audit.md) - Audit UI components

---

**For more information, see the [A2UI Documentation](../../README-A2UI.md).**
