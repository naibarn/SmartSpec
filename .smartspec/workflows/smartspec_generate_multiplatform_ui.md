---
workflow_id: smartspec_generate_multiplatform_ui
version: "6.0.0"
status: active
category: ui
platform_support:
  - cli
  - kilo
requires_apply: true
---

# smartspec_generate_multiplatform_ui

**Generate UI implementation for multiple platforms simultaneously from a single A2UI specification.**

## Purpose

This workflow generates platform-specific UI implementation code for multiple target platforms (Web, Flutter, etc.) from a single A2UI specification. It ensures consistent behavior across platforms while respecting platform-specific conventions and best practices.

## Governance contract

This workflow MUST follow:
- `knowledge_base_smartspec_handbook.md` (v6)
- A2UI Specification v0.8
- `.spec/smartspec.config.yaml`
- `.spec/ui-catalog.json`
- Platform-specific style guides

## Prerequisites

**Required:**
- A2UI must be enabled in `.spec/smartspec.config.yaml`
- Valid UI specification file
- UI component catalog

**Optional:**
- Platform-specific configuration files
- Custom component templates
- Design system tokens

## Invocation

### CLI

```bash
/smartspec_generate_multiplatform_ui \
  --spec specs/feature/spec-002-contact/ui-spec.json \
  --platforms web,flutter \
  --web-renderer lit \
  --output-dir src/ui/contact \
  --apply
```

### Kilo Code

```bash
/smartspec_generate_multiplatform_ui.md \
  --spec specs/feature/spec-002-contact/ui-spec.json \
  --platforms web,flutter \
  --web-renderer lit \
  --output-dir src/ui/contact \
  --platform kilo \
  --apply
```

## Flags

### Universal Flags

| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--apply` | boolean | No | Apply changes (default: preview mode) |
| `--platform` | string | No | Platform: cli, kilo (default: cli) |
| `--verbose` | boolean | No | Verbose output |
| `--report-dir` | path | No | Custom report directory |

### Workflow-Specific Flags

| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--spec` | path | Yes | Path to UI specification JSON file |
| `--platforms` | string | Yes | Comma-separated list: web, flutter, mobile |
| `--output-dir` | path | Yes | Base output directory for all platforms |
| `--web-renderer` | string | Conditional | Web renderer: lit, react, angular (required if web in platforms) |
| `--typescript` | boolean | No | Generate TypeScript (default: true for web) |
| `--tests` | boolean | No | Generate unit tests (default: true) |
| `--storybook` | boolean | No | Generate Storybook stories (web only, default: false) |
| `--shared-types` | boolean | No | Generate shared type definitions (default: true) |
| `--shared-components` | path | No | Path to shared component library |
| `--consistency-check` | boolean | No | Verify consistency across platforms (default: true) |

### Flag Usage Notes

**Platforms:**
- `web`: Web platforms (Lit, React, Angular)
- `flutter`: Flutter (iOS + Android)
- `mobile`: Native mobile (future support)

**Output Structure:**
```
<output-dir>/
├── web/           # Web implementation
├── flutter/       # Flutter implementation
├── shared/        # Shared types and utilities
└── docs/          # Cross-platform documentation
```

**Shared Types:**
- Generated once in `shared/` directory
- Imported by all platforms
- Ensures type consistency

**Consistency Check:**
- Verifies component parity across platforms
- Checks data model consistency
- Validates action compatibility

## Behavior

### Preview Mode (default)

1. **Validate Prerequisites**
   - Check A2UI is enabled
   - Verify UI spec exists and is valid
   - Check catalog exists
   - Validate platform selections

2. **Parse UI Specification**
   - Load and validate UI spec JSON
   - Extract components
   - Extract data model
   - Extract actions and bindings

3. **Plan Multi-Platform Generation**
   - Determine platform-specific requirements
   - Identify shared components
   - Plan directory structure
   - Calculate file count

4. **Generate Shared Types**
   - Create TypeScript/Dart type definitions
   - Generate data model interfaces
   - Create action type definitions
   - Generate utility types

5. **Generate Platform-Specific Code**
   - For each platform:
     - Generate component files
     - Generate platform-specific types
     - Generate tests
     - Generate documentation

6. **Perform Consistency Check**
   - Verify component parity
   - Check data model consistency
   - Validate action compatibility
   - Report discrepancies

7. **Generate Cross-Platform Documentation**
   - Create platform comparison table
   - Document platform-specific differences
   - Provide usage examples for each platform

8. **Generate Preview Report**
   - List all files to be generated
   - Show directory structure
   - Display consistency check results
   - Provide apply command

9. **Prompt for Apply**
   - Instruct user to review preview
   - Provide command with `--apply`

### Apply Mode (`--apply`)

1. **Perform all preview mode steps**

2. **Create Directory Structure**
   - Create platform directories
   - Create shared directory
   - Create docs directory

3. **Write Shared Types**
   - Write type definition files
   - Write utility files
   - Write shared constants

4. **Write Platform-Specific Code**
   - For each platform:
     - Write component files
     - Write test files
     - Write configuration files
     - Write platform documentation

5. **Write Cross-Platform Documentation**
   - Write README.md
   - Write platform comparison
   - Write migration guide
   - Write troubleshooting guide

6. **Generate Summary Report**
   - List generated files
   - Show statistics per platform
   - Display next steps

7. **Suggest Verification**
   - Provide verification commands for each platform

## Output

### Preview Mode

```
.spec/reports/generate-multiplatform-ui/<run-id>/
├── report.md                      # Full generation report
├── file-list.txt                  # List of files to be generated
├── directory-structure.txt        # Directory structure preview
├── consistency-report.md          # Consistency check results
└── platform-comparison.md         # Platform comparison table
```

### Apply Mode (additional)

```
<output-dir>/
├── web/
│   ├── components/
│   │   ├── ContactForm.ts
│   │   ├── NameField.ts
│   │   ├── EmailField.ts
│   │   └── ...
│   ├── tests/
│   │   └── *.test.ts
│   ├── types/
│   │   └── ContactFormTypes.ts
│   └── README.md
├── flutter/
│   ├── lib/
│   │   ├── widgets/
│   │   │   ├── contact_form.dart
│   │   │   ├── name_field.dart
│   │   │   ├── email_field.dart
│   │   │   └── ...
│   │   ├── models/
│   │   │   └── contact_form_model.dart
│   │   └── main.dart
│   ├── test/
│   │   └── *_test.dart
│   └── README.md
├── shared/
│   ├── types/
│   │   ├── ContactFormTypes.ts
│   │   └── CommonTypes.ts
│   ├── constants/
│   │   └── ValidationRules.ts
│   └── README.md
└── docs/
    ├── README.md
    ├── platform-comparison.md
    ├── migration-guide.md
    └── troubleshooting.md
```

### Generation Report

```markdown
# Multi-Platform UI Generation Report

**Specification:** specs/feature/spec-002-contact/ui-spec.json
**Platforms:** web (Lit), flutter
**Output Directory:** src/ui/contact
**Date:** 2025-12-22

## Summary

- ✅ **Platforms:** 2
- ✅ **Components:** 5
- ✅ **Shared Types:** 3
- ✅ **Total Files:** 28
- ✅ **Consistency:** 100%

---

## Platform Breakdown

### Web (Lit)

**Files Generated:**
- Components: 5 files
- Tests: 5 files
- Types: 2 files
- Total: 12 files

**Technology:**
- Renderer: Lit (Web Components)
- Language: TypeScript
- Testing: Vitest
- Styling: Material Design

### Flutter

**Files Generated:**
- Widgets: 5 files
- Tests: 5 files
- Models: 2 files
- Total: 12 files

**Technology:**
- Framework: Flutter
- Language: Dart
- Testing: Flutter Test
- Styling: Material Design

### Shared

**Files Generated:**
- Types: 3 files
- Constants: 1 file
- Total: 4 files

---

## Consistency Check: ✅ PASS

### Component Parity: 100%

All components present in both platforms:
- ✅ ContactForm
- ✅ NameField
- ✅ EmailField
- ✅ MessageField
- ✅ SubmitButton

### Data Model: 100%

Data model consistent across platforms:
- ✅ Same properties
- ✅ Same types
- ✅ Same validation rules

### Actions: 100%

Actions consistent across platforms:
- ✅ submit
- ✅ validate
- ✅ reset

---

## Platform Comparison

| Feature | Web (Lit) | Flutter |
|---------|-----------|---------|
| **Language** | TypeScript | Dart |
| **Component Count** | 5 | 5 |
| **Test Coverage** | 100% | 100% |
| **Accessibility** | WCAG-AA | Material Semantics |
| **Styling** | CSS + Material | Material Theme |
| **State Management** | Lit Reactive | setState |

---

## Next Steps

### 1. Verify Web Implementation

```bash
/smartspec_verify_ui_implementation \
  --spec specs/feature/spec-002-contact/ui-spec.json \
  --implementation src/ui/contact/web \
  --target-platform web
```

### 2. Verify Flutter Implementation

```bash
/smartspec_verify_ui_implementation \
  --spec specs/feature/spec-002-contact/ui-spec.json \
  --implementation src/ui/contact/flutter/lib \
  --target-platform flutter
```

### 3. Run Tests

**Web:**
```bash
cd src/ui/contact/web
npm test
```

**Flutter:**
```bash
cd src/ui/contact/flutter
flutter test
```

### 4. Start Development Servers

**Web:**
```bash
cd src/ui/contact/web
npm run dev
```

**Flutter:**
```bash
cd src/ui/contact/flutter
flutter run
```

---

## Files Generated

**Total:** 28 files

**By Platform:**
- Web: 12 files
- Flutter: 12 files
- Shared: 4 files

**By Type:**
- Components/Widgets: 10 files
- Tests: 10 files
- Types/Models: 5 files
- Documentation: 3 files
```

## Example Usage

### Example 1: Web + Flutter

**Generate for Web and Flutter:**

```bash
/smartspec_generate_multiplatform_ui \
  --spec specs/feature/spec-002-contact/ui-spec.json \
  --platforms web,flutter \
  --web-renderer lit \
  --output-dir src/ui/contact \
  --typescript \
  --tests \
  --apply
```

**Output:**
```
✅ Generated 28 files across 2 platforms
✅ Consistency check: PASS

Platforms:
- Web (Lit): 12 files
- Flutter: 12 files
- Shared: 4 files

Next: Verify implementations
```

### Example 2: Multiple Web Renderers

**Generate for Lit and React:**

```bash
# Generate Lit version
/smartspec_generate_multiplatform_ui \
  --spec specs/feature/spec-003-dashboard/ui-spec.json \
  --platforms web \
  --web-renderer lit \
  --output-dir src/ui/dashboard/lit \
  --apply

# Generate React version
/smartspec_generate_multiplatform_ui \
  --spec specs/feature/spec-003-dashboard/ui-spec.json \
  --platforms web \
  --web-renderer react \
  --output-dir src/ui/dashboard/react \
  --apply
```

### Example 3: With Shared Component Library

**Use shared components:**

```bash
/smartspec_generate_multiplatform_ui \
  --spec specs/feature/spec-004-booking/ui-spec.json \
  --platforms web,flutter \
  --web-renderer lit \
  --output-dir src/ui/booking \
  --shared-components src/ui/shared \
  --apply
```

**Result:**
- Imports shared components instead of regenerating
- Reduces code duplication
- Maintains consistency

### Example 4: With Storybook

**Generate with Storybook stories:**

```bash
/smartspec_generate_multiplatform_ui \
  --spec specs/feature/spec-002-contact/ui-spec.json \
  --platforms web \
  --web-renderer lit \
  --output-dir src/ui/contact \
  --storybook \
  --apply
```

**Additional output:**
```
src/ui/contact/web/
├── components/
│   └── *.ts
├── stories/
│   └── *.stories.ts
└── .storybook/
    └── main.js
```

### Example 5: Skip Consistency Check

**Fast generation without consistency check:**

```bash
/smartspec_generate_multiplatform_ui \
  --spec specs/feature/spec-005-settings/ui-spec.json \
  --platforms web,flutter \
  --web-renderer react \
  --output-dir src/ui/settings \
  --consistency-check false \
  --apply
```

**Use when:**
- Platforms intentionally differ
- Speed is critical
- Manual verification preferred

## Consistency Checks

### 1. Component Parity

**Verifies:**
- All components exist in all platforms
- Component hierarchy matches
- Component names consistent

**Example:**
```
✅ ContactForm: present in web, flutter
✅ NameField: present in web, flutter
✅ EmailField: present in web, flutter
```

### 2. Data Model Consistency

**Verifies:**
- Same properties across platforms
- Compatible types
- Same validation rules
- Same default values

**Example:**
```
✅ ContactForm.name: string (web), String (flutter)
✅ ContactForm.email: string (web), String (flutter)
✅ ContactForm.message: string (web), String (flutter)
```

### 3. Action Compatibility

**Verifies:**
- Same actions in all platforms
- Compatible action parameters
- Same event payloads

**Example:**
```
✅ submit: compatible across platforms
✅ validate: compatible across platforms
✅ reset: compatible across platforms
```

### 4. Accessibility Parity

**Verifies:**
- ARIA labels present (web)
- Semantics widgets present (flutter)
- Keyboard navigation (both)

**Example:**
```
✅ Web: ARIA labels on all inputs
✅ Flutter: Semantics on all widgets
✅ Both: Tab navigation support
```

## Shared Types

### Type Generation

**Shared types are generated once:**

```typescript
// shared/types/ContactFormTypes.ts
export interface ContactFormData {
  name: string;
  email: string;
  message: string;
}

export interface ContactFormActions {
  submit: (data: ContactFormData) => Promise<void>;
  validate: (field: keyof ContactFormData) => boolean;
  reset: () => void;
}

export interface ContactFormState {
  data: ContactFormData;
  errors: Partial<Record<keyof ContactFormData, string>>;
  isSubmitting: boolean;
}
```

### Platform Usage

**Web (TypeScript):**
```typescript
import { ContactFormData, ContactFormActions } from '../../../shared/types/ContactFormTypes';
```

**Flutter (Dart):**
```dart
// Generated Dart equivalent in flutter/lib/models/
class ContactFormData {
  String name;
  String email;
  String message;
}
```

## Platform-Specific Conventions

### Web (Lit)

**Conventions:**
- camelCase for properties
- kebab-case for custom elements
- TypeScript types
- CSS modules for styling

**Example:**
```typescript
@customElement('contact-form')
export class ContactForm extends LitElement {
  @property() formData: ContactFormData;
}
```

### Flutter

**Conventions:**
- snake_case for files
- PascalCase for classes
- Dart types
- Material Theme for styling

**Example:**
```dart
class ContactForm extends StatefulWidget {
  final ContactFormData formData;
}
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

5) **Related Workflows**
   - `smartspec_implement_ui_from_spec.md`
   - `smartspec_verify_ui_implementation.md`

## Best Practices

### When to Use Multi-Platform Generation

**Use when:**
- Building for multiple platforms
- Need consistent behavior across platforms
- Want to reduce development time
- Need to maintain parity

**Don't use when:**
- Platforms have significantly different UX
- Platform-specific features required
- Custom optimization needed per platform

### Directory Organization

**Recommended structure:**
```
src/ui/<feature>/
├── web/           # Web-specific code
├── flutter/       # Flutter-specific code
├── shared/        # Shared types and utilities
└── docs/          # Cross-platform documentation
```

### Testing Strategy

**Test each platform independently:**
```bash
# Web
cd src/ui/contact/web && npm test

# Flutter
cd src/ui/contact/flutter && flutter test
```

**Test consistency:**
```bash
/smartspec_verify_ui_implementation \
  --spec ... \
  --implementation src/ui/contact/web \
  --target-platform web

/smartspec_verify_ui_implementation \
  --spec ... \
  --implementation src/ui/contact/flutter/lib \
  --target-platform flutter
```

### Version Control

**Commit structure:**
```
src/ui/contact/
├── web/           # Commit separately
├── flutter/       # Commit separately
├── shared/        # Commit first (dependency)
└── docs/          # Commit with shared
```

## Troubleshooting

### Error: "Platform not supported"

**Solution:** Check platform name:
```bash
# Correct
--platforms web,flutter

# Incorrect
--platforms ios,android  # Use "flutter" instead
```

### Error: "Web renderer required"

**Solution:** Specify renderer when using web:
```bash
/smartspec_generate_multiplatform_ui \
  --platforms web \
  --web-renderer lit \
  ...
```

### Warning: "Consistency check failed"

**Solution:** Review consistency report:
```
.spec/reports/generate-multiplatform-ui/.../consistency-report.md
```

Fix issues or skip check:
```bash
--consistency-check false
```

### Error: "Shared types conflict"

**Solution:** Clear shared directory:
```bash
rm -rf src/ui/contact/shared
```

Then regenerate:
```bash
/smartspec_generate_multiplatform_ui ... --apply
```

## Related Workflows

**Before multi-platform generation:**

1. **Generate UI spec:**
   ```bash
   /smartspec_generate_ui_spec \
     --requirements "..." \
     --spec specs/feature/spec-002-contact/ui-spec.json \
     --apply
   ```

**After multi-platform generation:**

2. **Verify each platform:**
   ```bash
   /smartspec_verify_ui_implementation \
     --spec specs/feature/spec-002-contact/ui-spec.json \
     --implementation src/ui/contact/web \
     --target-platform web

   /smartspec_verify_ui_implementation \
     --spec specs/feature/spec-002-contact/ui-spec.json \
     --implementation src/ui/contact/flutter/lib \
     --target-platform flutter
   ```

**Alternative (single platform):**

3. **Use smartspec_implement_ui_from_spec:**
   ```bash
   /smartspec_implement_ui_from_spec \
     --spec specs/feature/spec-002-contact/ui-spec.json \
     --target-platform web \
     --renderer lit \
     --output-dir src/ui/contact/web \
     --apply
   ```

## Security Considerations

- **Shared types** - Validated against catalog
- **Platform isolation** - No cross-platform code execution
- **Catalog validation** - All components approved
- **Type safety** - Enforced in both TypeScript and Dart

## Version History

- **6.0.0** (2025-12-22): Initial release with A2UI v0.8 support

---

**Status:** Active  
**Requires Apply:** Yes (generates code files)  
**Platform Support:** CLI, Kilo  
**Category:** UI Generation (Multi-Platform)
