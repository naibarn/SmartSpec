# A2UI Integration Quick Start

## What is A2UI?

**A2UI (Agent-to-User Interface)** is an open-source protocol from Google that enables AI agents to generate rich, interactive user interfaces using declarative JSON specifications instead of code.

**Key Benefits:**
- ✅ **Safe:** Declarative data format, no code execution
- ✅ **Cross-platform:** Generate once, render on Web, Flutter, React, etc.
- ✅ **Governed:** Component catalog ensures security and consistency
- ✅ **LLM-friendly:** AI agents can easily generate valid UI specs

## Installation (Optional)

A2UI features are **completely optional** and disabled by default. Install only if you need UI generation workflows.

### Step 1: Install Dependencies

```bash
# From SmartSpec root directory
npm install @a2ui/core@^0.8.0 lit@^3.0.0

# Optional renderers
npm install --save-dev @a2ui/lit-renderer@^0.8.0
npm install --save-dev @a2ui/flutter-renderer@^0.8.0
```

### Step 2: Enable A2UI

Edit `.spec/smartspec.config.yaml`:

```yaml
a2ui:
  enabled: true  # Change from false to true
```

### Step 3: Initialize Catalog

```bash
cp .spec/ui-catalog.template.json .spec/ui-catalog.json
```

## Basic Usage

### Generate UI Specification

**Preview Mode (default):**
```bash
/smartspec_generate_ui_spec \
  --requirements "Create contact form with name, email, message fields" \
  --spec specs/feature/spec-002-contact/ui-spec.json
```

**Apply Mode (save to final location):**
```bash
/smartspec_generate_ui_spec \
  --requirements "Create contact form with name, email, message fields" \
  --spec specs/feature/spec-002-contact/ui-spec.json \
  --apply
```

**Kilo Code:**
```bash
/smartspec_generate_ui_spec.md \
  --requirements "Create contact form with name, email, message fields" \
  --spec specs/feature/spec-002-contact/ui-spec.json \
  --platform kilo \
  --apply
```

### Interactive Mode

```bash
/smartspec_generate_ui_spec \
  --requirements "Create dashboard with metrics and charts" \
  --spec specs/feature/spec-003-dashboard/ui-spec.json \
  --interactive \
  --apply
```

The agent will:
1. Generate initial UI spec
2. Show preview mockup
3. Ask for feedback
4. Refine iteratively
5. Save when you approve

## Example Output

**Generated UI Spec (simplified):**
```json
{
  "version": "0.8",
  "surfaces": [
    {
      "id": "contact-form",
      "components": [
        {
          "id": "name-field",
          "type": "text-field",
          "label": "Name",
          "valuePath": "/contact/name",
          "required": true
        },
        {
          "id": "email-field",
          "type": "text-field",
          "label": "Email",
          "type": "email",
          "valuePath": "/contact/email",
          "required": true
        },
        {
          "id": "submit-button",
          "type": "button",
          "label": "Send Message",
          "action": "submit-contact"
        }
      ]
    }
  ],
  "dataModel": {
    "contact": {
      "name": "",
      "email": "",
      "message": ""
    }
  }
}
```

## Available Workflows (Phase 1)

| Workflow | Purpose | Status |
|----------|---------|--------|
| `smartspec_generate_ui_spec` | Generate UI specification from requirements | ✅ Active |

**Coming in Phase 2-4:**
- `smartspec_implement_ui_from_spec` - Generate platform-specific code
- `smartspec_verify_ui_implementation` - Verify implementation compliance
- `smartspec_manage_ui_catalog` - Manage component catalog
- `smartspec_generate_multiplatform_ui` - Cross-platform generation
- `smartspec_ui_agent` - Interactive UI design agent

## Component Catalog

The catalog (`.spec/ui-catalog.json`) defines approved components:

**Available Components (Material Design preset):**
- **Input:** text-field, text-area, select, checkbox, radio-group, date-picker, number-input
- **Layout:** card, container, divider
- **Data:** list, table
- **Feedback:** progress-bar, alert, dialog
- **Basic:** text, button

## Troubleshooting

**Error: "A2UI not enabled"**
```yaml
# Enable in .spec/smartspec.config.yaml
a2ui:
  enabled: true
```

**Error: "Catalog not found"**
```bash
cp .spec/ui-catalog.template.json .spec/ui-catalog.json
```

**Error: "Dependencies not installed"**
```bash
npm install @a2ui/core lit
```

## Uninstallation

If you decide not to use A2UI:

```bash
# Remove dependencies
npm uninstall @a2ui/core lit @a2ui/lit-renderer

# Disable in config
# Edit .spec/smartspec.config.yaml:
# a2ui:
#   enabled: false

# Delete files (optional)
rm -f a2ui-package.json README-A2UI.md
rm -f .spec/ui-catalog.json
```

## Resources

- **A2UI Official Docs:** https://a2ui.org
- **A2UI GitHub:** https://github.com/google/A2UI
- **Full Documentation:** `README-A2UI.md`
- **Integration Report:** `A2UI_SmartSpec_Integration_Report.md`
- **Workflow Specs:** `a2ui_workflow_specifications.md`

## Zero-Impact Guarantee

✅ **Opt-in only** - Disabled by default  
✅ **No breaking changes** - All existing workflows unchanged  
✅ **Graceful degradation** - Clear error messages if dependencies missing  
✅ **Independent** - A2UI workflows don't interfere with others  

---

**SmartSpec Version:** v6.3.3  
**A2UI Version:** v0.8  
**Last Updated:** December 22, 2025
