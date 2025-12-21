# A2UI Phase 2: Core Workflows - Quick Start

**Phase 2 Status:** ✅ Complete  
**SmartSpec Version:** v6.3.4  
**A2UI Version:** v0.8  
**Date:** December 22, 2025

---

## What's New in Phase 2?

Phase 2 adds **3 core workflows** that complete the A2UI development lifecycle:

1. **`smartspec_implement_ui_from_spec`** - Generate platform code
2. **`smartspec_verify_ui_implementation`** - Verify implementation
3. **`smartspec_manage_ui_catalog`** - Manage component catalog

Together with Phase 1's `smartspec_generate_ui_spec`, you now have a **complete UI development workflow** from requirements to verified implementation.

---

## Complete A2UI Workflow

### End-to-End Example

**Scenario:** Build a contact form UI

#### Step 1: Generate UI Specification

```bash
/smartspec_generate_ui_spec \
  --requirements "Create contact form with name, email, message fields and submit button" \
  --spec specs/feature/spec-002-contact/ui-spec.json \
  --apply
```

**Output:** `specs/feature/spec-002-contact/ui-spec.json`

---

#### Step 2: Implement UI Code

```bash
/smartspec_implement_ui_from_spec \
  --spec specs/feature/spec-002-contact/ui-spec.json \
  --target-platform web \
  --renderer lit \
  --output-dir src/ui/contact \
  --typescript \
  --tests \
  --apply
```

**Output:** 
```
src/ui/contact/
├── components/
│   ├── ContactForm.ts
│   ├── NameField.ts
│   ├── EmailField.ts
│   ├── MessageField.ts
│   └── SubmitButton.ts
├── types/
│   └── ContactFormTypes.ts
├── tests/
│   └── *.test.ts
└── index.ts
```

---

#### Step 3: Verify Implementation

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
```

---

#### Step 4: Fix Issues (if any)

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
✅ Compliance Score: 100%
```

---

## Workflow Details

### 1. smartspec_implement_ui_from_spec

**Generate platform-specific code from UI spec.**

**Supported Platforms:**
- **Web:** Lit, React, Angular
- **Mobile:** Flutter

**Features:**
- ✅ Generate component files
- ✅ Generate TypeScript types
- ✅ Generate unit tests
- ✅ Generate Storybook stories
- ✅ Material Design styling
- ✅ Accessibility compliance

**Example (Web/Lit):**
```bash
/smartspec_implement_ui_from_spec \
  --spec specs/feature/spec-002-contact/ui-spec.json \
  --target-platform web \
  --renderer lit \
  --output-dir src/ui/contact \
  --typescript \
  --tests \
  --storybook \
  --apply
```

**Example (Flutter):**
```bash
/smartspec_implement_ui_from_spec \
  --spec specs/feature/spec-003-dashboard/ui-spec.json \
  --target-platform flutter \
  --output-dir lib/ui/dashboard \
  --tests \
  --apply
```

**Example (React):**
```bash
/smartspec_implement_ui_from_spec \
  --spec specs/feature/spec-004-booking/ui-spec.json \
  --target-platform web \
  --renderer react \
  --output-dir src/components/booking \
  --typescript \
  --tests \
  --storybook \
  --apply
```

---

### 2. smartspec_verify_ui_implementation

**Verify implementation matches specification.**

**Checks:**
- ✅ Component structure (25%)
- ✅ Data bindings (25%)
- ✅ Actions/events (20%)
- ✅ Catalog adherence (15%)
- ✅ Accessibility (15%)

**Pass Threshold:** 80%

**Example (Basic):**
```bash
/smartspec_verify_ui_implementation \
  --spec specs/feature/spec-002-contact/ui-spec.json \
  --implementation src/ui/contact \
  --target-platform web
```

**Example (Strict Mode for CI/CD):**
```bash
/smartspec_verify_ui_implementation \
  --spec specs/feature/spec-002-contact/ui-spec.json \
  --implementation src/ui/contact \
  --target-platform web \
  --strict
```

**Example (Runtime Verification):**
```bash
# Start dev server first
npm run dev

# Run verification with runtime checks
/smartspec_verify_ui_implementation \
  --spec specs/feature/spec-002-contact/ui-spec.json \
  --implementation src/ui/contact \
  --target-platform web \
  --runtime-check
```

**Example (Auto-Fix):**
```bash
/smartspec_verify_ui_implementation \
  --spec specs/feature/spec-002-contact/ui-spec.json \
  --implementation src/ui/contact \
  --target-platform web \
  --fix
```

---

### 3. smartspec_manage_ui_catalog

**Manage component catalog.**

**Actions:**
- `add` - Add new component
- `remove` - Remove component
- `update` - Update component definition
- `validate` - Validate catalog integrity
- `export` - Export catalog to file
- `import` - Import catalog from file
- `list` - List all components

**Example (Add Component):**
```bash
/smartspec_manage_ui_catalog \
  --action add \
  --component-type slider \
  --component-def slider-component.json \
  --security-level trusted \
  --category input \
  --apply
```

**Example (Remove Component):**
```bash
/smartspec_manage_ui_catalog \
  --action remove \
  --component-type slider \
  --apply
```

**Example (Update Component):**
```bash
/smartspec_manage_ui_catalog \
  --action update \
  --component-type button \
  --component-def button-component-v2.json \
  --apply
```

**Example (Validate Catalog):**
```bash
/smartspec_manage_ui_catalog \
  --action validate
```

**Example (Export Catalog):**
```bash
/smartspec_manage_ui_catalog \
  --action export \
  --export-file catalogs/my-catalog-v1.json \
  --apply
```

**Example (Import Catalog):**
```bash
/smartspec_manage_ui_catalog \
  --action import \
  --import-file catalogs/material-design-catalog.json \
  --merge \
  --apply
```

**Example (List Components):**
```bash
/smartspec_manage_ui_catalog \
  --action list
```

---

## Common Scenarios

### Scenario 1: New Feature with UI

**Goal:** Build a new feature with UI from scratch

```bash
# 1. Generate UI spec
/smartspec_generate_ui_spec \
  --requirements "User profile page with avatar, name, email, bio" \
  --spec specs/feature/spec-010-profile/ui-spec.json \
  --apply

# 2. Implement UI
/smartspec_implement_ui_from_spec \
  --spec specs/feature/spec-010-profile/ui-spec.json \
  --target-platform web \
  --renderer lit \
  --output-dir src/ui/profile \
  --typescript \
  --tests \
  --apply

# 3. Verify implementation
/smartspec_verify_ui_implementation \
  --spec specs/feature/spec-010-profile/ui-spec.json \
  --implementation src/ui/profile \
  --target-platform web

# 4. Fix issues (if any)
/smartspec_verify_ui_implementation \
  --spec specs/feature/spec-010-profile/ui-spec.json \
  --implementation src/ui/profile \
  --target-platform web \
  --fix
```

---

### Scenario 2: Add Custom Component

**Goal:** Add a custom component to the catalog and use it

```bash
# 1. Create component definition
cat > tooltip-component.json << 'EOF'
{
  "type": "tooltip",
  "label": "Tooltip",
  "description": "Contextual tooltip",
  "category": "overlay",
  "securityLevel": "safe",
  "properties": {
    "text": { "type": "string", "required": true },
    "position": { "type": "string", "enum": ["top", "bottom"], "default": "top" }
  }
}
EOF

# 2. Add to catalog
/smartspec_manage_ui_catalog \
  --action add \
  --component-type tooltip \
  --component-def tooltip-component.json \
  --apply

# 3. Use in UI spec
/smartspec_generate_ui_spec \
  --requirements "Add tooltips to form fields" \
  --spec specs/feature/spec-002-contact/ui-spec.json \
  --apply

# 4. Regenerate implementation
/smartspec_implement_ui_from_spec \
  --spec specs/feature/spec-002-contact/ui-spec.json \
  --target-platform web \
  --renderer lit \
  --output-dir src/ui/contact \
  --apply
```

---

### Scenario 3: Multi-Platform UI

**Goal:** Generate UI for both Web and Mobile

```bash
# 1. Generate UI spec (platform-agnostic)
/smartspec_generate_ui_spec \
  --requirements "Dashboard with metrics and charts" \
  --spec specs/feature/spec-003-dashboard/ui-spec.json \
  --apply

# 2. Implement for Web
/smartspec_implement_ui_from_spec \
  --spec specs/feature/spec-003-dashboard/ui-spec.json \
  --target-platform web \
  --renderer lit \
  --output-dir src/ui/dashboard \
  --typescript \
  --apply

# 3. Implement for Flutter
/smartspec_implement_ui_from_spec \
  --spec specs/feature/spec-003-dashboard/ui-spec.json \
  --target-platform flutter \
  --output-dir lib/ui/dashboard \
  --apply

# 4. Verify both implementations
/smartspec_verify_ui_implementation \
  --spec specs/feature/spec-003-dashboard/ui-spec.json \
  --implementation src/ui/dashboard \
  --target-platform web

/smartspec_verify_ui_implementation \
  --spec specs/feature/spec-003-dashboard/ui-spec.json \
  --implementation lib/ui/dashboard \
  --target-platform flutter
```

---

### Scenario 4: CI/CD Integration

**Goal:** Verify UI implementation in CI/CD pipeline

```yaml
# .github/workflows/verify-ui.yml
name: Verify UI Implementation

on: [push, pull_request]

jobs:
  verify-ui:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Install dependencies
        run: npm install
      
      - name: Verify Contact Form UI
        run: |
          /smartspec_verify_ui_implementation \
            --spec specs/feature/spec-002-contact/ui-spec.json \
            --implementation src/ui/contact \
            --target-platform web \
            --strict
      
      - name: Verify Dashboard UI
        run: |
          /smartspec_verify_ui_implementation \
            --spec specs/feature/spec-003-dashboard/ui-spec.json \
            --implementation src/ui/dashboard \
            --target-platform web \
            --strict
```

---

## Best Practices

### 1. Preview-First Workflow

**Always preview before applying:**

```bash
# Preview first (no --apply)
/smartspec_implement_ui_from_spec \
  --spec specs/feature/spec-002-contact/ui-spec.json \
  --target-platform web \
  --output-dir src/ui/contact

# Review generated code in report directory
# Then apply
/smartspec_implement_ui_from_spec \
  --spec specs/feature/spec-002-contact/ui-spec.json \
  --target-platform web \
  --output-dir src/ui/contact \
  --apply
```

### 2. Verify After Implementation

**Always verify after implementing:**

```bash
# Implement
/smartspec_implement_ui_from_spec ... --apply

# Verify immediately
/smartspec_verify_ui_implementation ...
```

### 3. Use Strict Mode in CI/CD

**Fail builds on warnings:**

```bash
/smartspec_verify_ui_implementation \
  --spec ... \
  --implementation ... \
  --target-platform web \
  --strict
```

### 4. Validate Catalog Regularly

**Validate catalog before deployment:**

```bash
/smartspec_manage_ui_catalog --action validate
```

### 5. Version Control Catalog

**Export catalog before major changes:**

```bash
/smartspec_manage_ui_catalog \
  --action export \
  --export-file catalogs/backup-$(date +%Y%m%d).json \
  --apply
```

---

## Troubleshooting

### Issue: "Component not in catalog"

**Solution:** Add component to catalog first:
```bash
/smartspec_manage_ui_catalog \
  --action add \
  --component-type <component-type> \
  --component-def <definition-file> \
  --apply
```

### Issue: "Verification failed"

**Solution:** Use auto-fix:
```bash
/smartspec_verify_ui_implementation \
  --spec ... \
  --implementation ... \
  --target-platform web \
  --fix
```

### Issue: "Renderer dependencies not installed"

**Solution:** Install dependencies:
```bash
# Lit
npm install lit

# React
npm install react react-dom

# Flutter
flutter pub add flutter
```

---

## What's Next?

### Phase 3: Advanced Features (Coming Soon)

- `smartspec_generate_multiplatform_ui` - Generate for multiple platforms simultaneously
- `smartspec_ui_agent` - Interactive UI design agent
- Advanced component templates
- Design system integration

### Phase 4: Integration (Coming Soon)

- Integration with existing SmartSpec workflows
- UI specs in SPEC_INDEX
- UI tasks in tasks.md
- UI verification in verify_tasks_progress_strict

---

## Resources

- **Full Documentation:** `README-A2UI.md`
- **Phase 1 Quick Start:** `README-A2UI-QUICKSTART.md`
- **Integration Report:** `A2UI_SmartSpec_Integration_Report.md`
- **Workflow Specs:** `a2ui_workflow_specifications.md`
- **A2UI Official Docs:** https://a2ui.org
- **A2UI GitHub:** https://github.com/google/A2UI

---

**SmartSpec Version:** v6.3.4  
**A2UI Version:** v0.8  
**Phase 2 Status:** ✅ Complete  
**Last Updated:** December 22, 2025
