# `/smartspec_generate_ui_implementation` - Generate UI Implementation

| Metadata | Value |
|----------|-------|
| **Workflow ID** | `smartspec_generate_ui_implementation` |
| **Category** | UI / A2UI |
| **Version** | 6.0.0+ |
| **Requires `--apply`** | Yes |
| **Platform Support** | CLI, Kilo Code |

---

## Overview

Generate platform-specific UI implementation code from an A2UI specification. This workflow transforms a platform-agnostic `ui-spec.json` file into production-ready UI code for your target platform (Web/React, Flutter, React Native, etc.).

The generated code includes component structure, styling, data bindings, event handlers, and accessibility attributes, all following best practices for the target platform.

---

## Usage

### CLI

```bash
/smartspec_generate_ui_implementation \
  --spec specs/feature/spec-001-booking/ui-spec.json \
  --output src/ui/booking \
  --target-platform web
```

### Kilo Code

```bash
/smartspec_generate_ui_implementation.md \
  --spec specs/feature/spec-001-booking/ui-spec.json \
  --output src/ui/booking \
  --target-platform web \
  --platform kilo
```

---

## Use Cases

### 1. Generate React Web Implementation

**Scenario:** Generate React components from UI specification.

**Command:**
```bash
/smartspec_generate_ui_implementation \
  --spec specs/feature/spec-001-booking/ui-spec.json \
  --output src/ui/booking \
  --target-platform web \
  --framework react \
  --typescript
```

**Expected Result:** React components with TypeScript, hooks, and styled-components.

### 2. Generate Flutter Mobile Implementation

**Scenario:** Generate Flutter widgets for mobile app.

**Command:**
```bash
/smartspec_generate_ui_implementation \
  --spec specs/feature/spec-002-dashboard/ui-spec.json \
  --output lib/ui/dashboard \
  --target-platform flutter \
  --state-management bloc
```

**Expected Result:** Flutter widgets with BLoC pattern and Material Design.

### 3. Generate with Custom Styling

**Scenario:** Generate UI with custom design system.

**Command:**
```bash
/smartspec_generate_ui_implementation \
  --spec specs/feature/spec-003-profile/ui-spec.json \
  --output src/ui/profile \
  --target-platform web \
  --style-system custom \
  --theme-file src/theme/custom-theme.ts
```

**Expected Result:** Components using custom design tokens and theme.

---

## Parameters

### Required Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `--spec` | path | Path to UI specification JSON file |
| `--output` | path | Output directory for generated code |
| `--target-platform` | string | Target platform: web, flutter, mobile |

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
| `--framework` | string | auto | Framework: react, vue, angular, flutter, react-native |
| `--typescript` | boolean | false | Generate TypeScript code (for web platforms) |
| `--style-system` | string | from config | Styling approach: css-modules, styled-components, tailwind, material |
| `--state-management` | string | auto | State management: hooks, redux, bloc, provider |
| `--theme-file` | path | - | Path to custom theme/design tokens file |
| `--catalog` | path | .spec/ui-catalog.json | Path to component catalog |
| `--include-tests` | boolean | false | Generate unit tests for components |
| `--include-stories` | boolean | false | Generate Storybook stories (web only) |

---

## Output

### Report Location
```
.spec/reports/generate-ui-implementation/<run-id>/
├── report.md              # Human-readable summary
├── report.json            # Machine-readable data
└── preview/
    ├── components/        # Preview of generated components
    └── structure.md       # File structure overview
```

### Generated Files (with `--apply`)

**For Web/React:**
```
<output-dir>/
├── components/
│   ├── BookingForm.tsx
│   ├── BookingForm.module.css
│   └── index.ts
├── hooks/
│   └── useBookingForm.ts
└── types/
    └── booking.types.ts
```

**For Flutter:**
```
<output-dir>/
├── widgets/
│   ├── booking_form.dart
│   └── booking_form_state.dart
├── models/
│   └── booking_model.dart
└── bloc/
    ├── booking_bloc.dart
    └── booking_event.dart
```

---

## Code Generation Features

### Component Structure
- ✅ Component hierarchy from spec
- ✅ Props/parameters with types
- ✅ State management setup
- ✅ Event handlers and callbacks

### Styling
- ✅ Platform-specific styling
- ✅ Responsive design
- ✅ Theme integration
- ✅ Design tokens usage

### Accessibility
- ✅ ARIA attributes (web)
- ✅ Semantic markup
- ✅ Keyboard navigation
- ✅ Screen reader support

### Data Binding
- ✅ Form validation
- ✅ Data flow setup
- ✅ API integration hooks
- ✅ Error handling

---

## Prerequisites

**Required:**
- Valid UI specification file (`ui-spec.json`)
- A2UI enabled in config
- Target platform development environment set up

**Optional:**
- Component catalog for reuse
- Custom theme/design system
- Testing framework for test generation

---

## Notes

1. **Preview First:** Always run without `--apply` to review generated code structure
2. **Platform Best Practices:** Generated code follows platform-specific conventions
3. **Catalog Integration:** Reuses existing components from catalog when possible
4. **Customization:** Use `--theme-file` to integrate with existing design system
5. **Testing:** Use `--include-tests` to generate unit tests alongside components
6. **Storybook:** Use `--include-stories` for component documentation (web only)
7. **Type Safety:** Use `--typescript` for type-safe React components

---

## Related Workflows

- [`/smartspec_generate_ui_spec`](./generate_ui_spec.md) - Generate UI specification
- [`/smartspec_verify_ui_implementation`](./ui_validation_manual.md) - Verify implementation
- [`/smartspec_ui_test_generator`](./ui_test_generator.md) - Generate UI tests
- [`/smartspec_ui_catalog_generator`](./ui_catalog_generator.md) - Generate component catalog

---

**For more information, see the [A2UI Documentation](../../README-A2UI.md).**
