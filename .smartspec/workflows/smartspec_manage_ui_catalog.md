---
workflow_id: smartspec_manage_ui_catalog
version: "6.0.0"
status: active
category: ui
platform_support:
  - cli
  - kilo
requires_apply: true
---

# smartspec_manage_ui_catalog

**Manage the UI component catalog for A2UI workflows.**

## Purpose

This workflow manages the UI component catalog (`.spec/ui-catalog.json`) which defines approved components that can be used in UI specifications. It supports adding, removing, updating components, validating catalog integrity, and importing/exporting catalogs.

## Governance contract

This workflow MUST follow:
- `knowledge_base_smartspec_handbook.md` (v6)
- A2UI Specification v0.8
- `.spec/smartspec.config.yaml`
- Component security policies

## Prerequisites

**Required:**
- A2UI must be enabled in `.spec/smartspec.config.yaml`
- UI component catalog exists (`.spec/ui-catalog.json`)

**Optional:**
- Custom component definitions
- External catalog files for import

## Invocation

### CLI

```bash
/smartspec_manage_ui_catalog \
  --action add \
  --component-type slider \
  --component-def slider-component.json \
  --apply
```

### Kilo Code

```bash
/smartspec_manage_ui_catalog.md \
  --action add \
  --component-type slider \
  --component-def slider-component.json \
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
| `--action` | string | Yes | Action: add, remove, update, validate, export, import, list |
| `--component-type` | string | Conditional | Component type (required for add/remove/update) |
| `--component-def` | path | Conditional | Component definition file (required for add/update) |
| `--security-level` | string | No | Security level: safe, trusted, review-required (default: review-required) |
| `--category` | string | No | Component category: input, layout, data, feedback, overlay, basic |
| `--export-file` | path | Conditional | Export destination (required for export) |
| `--import-file` | path | Conditional | Import source (required for import) |
| `--merge` | boolean | No | Merge on import instead of replace (default: false) |
| `--force` | boolean | No | Force operation without confirmation |

### Flag Usage Notes

**Actions:**
- `add`: Add new component to catalog
- `remove`: Remove component from catalog
- `update`: Update existing component definition
- `validate`: Validate catalog integrity
- `export`: Export catalog to file
- `import`: Import catalog from file
- `list`: List all components in catalog

**Security Levels:**
- `safe`: Pre-approved, no review needed
- `trusted`: Approved after review
- `review-required`: Needs review before use (default)

**Component Definition File:**
- JSON file with component schema
- Includes properties, events, slots
- Defines validation rules

## Behavior

### Preview Mode (default)

1. **Validate Prerequisites**
   - Check A2UI is enabled
   - Verify catalog exists
   - Validate action parameters

2. **Perform Action (in memory)**
   - Execute requested action
   - Validate changes
   - Check for conflicts

3. **Show Preview**
   - Display catalog changes
   - Show affected components
   - Calculate impact

4. **Generate Report**
   - List changes
   - Show warnings
   - Provide apply command

5. **Prompt for Apply**
   - Instruct user to review changes
   - Provide command with `--apply`

### Apply Mode (`--apply`)

1. **Perform all preview mode steps**

2. **Apply Changes**
   - Backup current catalog
   - Write changes to catalog
   - Validate new catalog

3. **Update Dependencies**
   - Check affected UI specs
   - List specs using changed components
   - Suggest re-generation if needed

4. **Report Success**
   - Display catalog statistics
   - Show next steps

## Actions

### Add Component

**Add new component to catalog:**

```bash
/smartspec_manage_ui_catalog \
  --action add \
  --component-type slider \
  --component-def slider-component.json \
  --security-level trusted \
  --category input \
  --apply
```

**Component definition file (slider-component.json):**
```json
{
  "type": "slider",
  "label": "Slider",
  "description": "Range slider for numeric input",
  "category": "input",
  "securityLevel": "trusted",
  "properties": {
    "min": {
      "type": "number",
      "description": "Minimum value",
      "default": 0
    },
    "max": {
      "type": "number",
      "description": "Maximum value",
      "default": 100
    },
    "value": {
      "type": "number",
      "description": "Current value",
      "default": 50
    },
    "step": {
      "type": "number",
      "description": "Step increment",
      "default": 1
    },
    "label": {
      "type": "string",
      "description": "Slider label"
    },
    "disabled": {
      "type": "boolean",
      "description": "Disabled state",
      "default": false
    }
  },
  "events": {
    "change": {
      "description": "Fired when value changes",
      "payload": {
        "value": "number"
      }
    }
  },
  "accessibility": {
    "role": "slider",
    "ariaLabel": "required",
    "ariaValueMin": "auto",
    "ariaValueMax": "auto",
    "ariaValueNow": "auto"
  }
}
```

**Output:**
```
✅ Component 'slider' added to catalog
✅ Category: input
✅ Security level: trusted
✅ Properties: 6
✅ Events: 1

Catalog updated: .spec/ui-catalog.json
```

### Remove Component

**Remove component from catalog:**

```bash
/smartspec_manage_ui_catalog \
  --action remove \
  --component-type slider \
  --apply
```

**Output:**
```
⚠️ Warning: 3 UI specs use 'slider' component:
  - specs/feature/spec-005-settings/ui-spec.json
  - specs/feature/spec-007-preferences/ui-spec.json
  - specs/feature/spec-012-volume/ui-spec.json

❌ Component 'slider' removed from catalog

Next steps:
1. Update affected UI specs
2. Regenerate implementations
```

### Update Component

**Update component definition:**

```bash
/smartspec_manage_ui_catalog \
  --action update \
  --component-type slider \
  --component-def slider-component-v2.json \
  --apply
```

**Output:**
```
✅ Component 'slider' updated
✅ Added property: 'showTicks'
✅ Updated property: 'step' (now optional)

⚠️ Breaking changes detected:
  - Property 'label' is now required

Affected UI specs: 3
Recommend regenerating implementations.
```

### Validate Catalog

**Validate catalog integrity:**

```bash
/smartspec_manage_ui_catalog \
  --action validate
```

**Output:**
```
✅ Catalog validation: PASS

Statistics:
- Total components: 18
- Categories: 6
- Security levels:
  - safe: 12
  - trusted: 5
  - review-required: 1

Issues: None

Catalog is valid and ready to use.
```

### Export Catalog

**Export catalog to file:**

```bash
/smartspec_manage_ui_catalog \
  --action export \
  --export-file catalogs/my-catalog-v1.json \
  --apply
```

**Output:**
```
✅ Catalog exported to: catalogs/my-catalog-v1.json

Contents:
- 18 components
- 6 categories
- A2UI v0.8 format

You can share this file or use it in other projects.
```

### Import Catalog

**Import catalog from file:**

```bash
/smartspec_manage_ui_catalog \
  --action import \
  --import-file catalogs/material-design-catalog.json \
  --merge \
  --apply
```

**Output:**
```
✅ Catalog imported from: catalogs/material-design-catalog.json

Changes:
- Added: 8 new components
- Updated: 3 existing components
- Skipped: 7 duplicates

Total components: 26

Catalog updated: .spec/ui-catalog.json
```

### List Components

**List all components:**

```bash
/smartspec_manage_ui_catalog \
  --action list
```

**Output:**
```
UI Component Catalog

Category: Input (7 components)
  - text-field (safe)
  - text-area (safe)
  - select (safe)
  - checkbox (safe)
  - radio-group (safe)
  - date-picker (trusted)
  - number-input (safe)

Category: Layout (3 components)
  - card (safe)
  - container (safe)
  - divider (safe)

Category: Data (2 components)
  - list (trusted)
  - table (trusted)

Category: Feedback (2 components)
  - progress-bar (safe)
  - alert (safe)

Category: Overlay (1 component)
  - dialog (trusted)

Category: Basic (2 components)
  - text (safe)
  - button (safe)

Total: 17 components
```

## Output

### Preview Mode

```
.spec/reports/manage-ui-catalog/<run-id>/
├── report.md                      # Full report
├── catalog-preview.json           # Preview of changes
├── diff.txt                       # Diff of changes
├── affected-specs.txt             # List of affected UI specs
└── impact-analysis.md             # Impact analysis
```

### Apply Mode (additional)

```
.spec/
├── ui-catalog.json                # Updated catalog
└── ui-catalog.backup.json         # Backup of previous version
```

## Example Usage

### Example 1: Add Custom Component

**Create component definition:**

```json
// tooltip-component.json
{
  "type": "tooltip",
  "label": "Tooltip",
  "description": "Contextual tooltip for help text",
  "category": "overlay",
  "securityLevel": "safe",
  "properties": {
    "text": {
      "type": "string",
      "description": "Tooltip text",
      "required": true
    },
    "position": {
      "type": "string",
      "description": "Tooltip position",
      "enum": ["top", "bottom", "left", "right"],
      "default": "top"
    },
    "trigger": {
      "type": "string",
      "description": "Trigger event",
      "enum": ["hover", "click", "focus"],
      "default": "hover"
    }
  },
  "slots": {
    "default": {
      "description": "Element to attach tooltip to"
    }
  },
  "accessibility": {
    "role": "tooltip",
    "ariaLabel": "auto"
  }
}
```

**Add to catalog:**

```bash
/smartspec_manage_ui_catalog \
  --action add \
  --component-type tooltip \
  --component-def tooltip-component.json \
  --security-level safe \
  --category overlay \
  --apply
```

### Example 2: Update Component for New Feature

**Update button component to support loading state:**

```json
// button-component-v2.json
{
  "type": "button",
  "label": "Button",
  "description": "Interactive button component",
  "category": "basic",
  "securityLevel": "safe",
  "properties": {
    "label": {
      "type": "string",
      "description": "Button label",
      "required": true
    },
    "disabled": {
      "type": "boolean",
      "description": "Disabled state",
      "default": false
    },
    "loading": {
      "type": "boolean",
      "description": "Loading state (NEW)",
      "default": false
    },
    "loadingText": {
      "type": "string",
      "description": "Text to show when loading (NEW)",
      "default": "Loading..."
    }
  },
  "events": {
    "click": {
      "description": "Fired when button clicked"
    }
  }
}
```

**Update catalog:**

```bash
/smartspec_manage_ui_catalog \
  --action update \
  --component-type button \
  --component-def button-component-v2.json \
  --apply
```

### Example 3: Import Third-Party Catalog

**Import Fluent UI catalog:**

```bash
/smartspec_manage_ui_catalog \
  --action import \
  --import-file catalogs/fluent-ui-catalog.json \
  --merge \
  --apply
```

**Result:**
- Existing components preserved
- New Fluent UI components added
- Conflicts resolved (keeps existing)

### Example 4: Validate Before Deployment

**Validate catalog in CI/CD:**

```bash
/smartspec_manage_ui_catalog \
  --action validate
```

**Exit codes:**
- `0`: Validation passed
- `1`: Validation failed

## Component Definition Schema

### Required Fields

```json
{
  "type": "component-name",
  "label": "Human-readable name",
  "description": "Component description",
  "category": "input|layout|data|feedback|overlay|basic",
  "securityLevel": "safe|trusted|review-required",
  "properties": { ... },
  "events": { ... },
  "accessibility": { ... }
}
```

### Property Definition

```json
{
  "propertyName": {
    "type": "string|number|boolean|object|array",
    "description": "Property description",
    "required": true|false,
    "default": "default value",
    "enum": ["option1", "option2"],
    "validation": {
      "min": 0,
      "max": 100,
      "pattern": "regex"
    }
  }
}
```

### Event Definition

```json
{
  "eventName": {
    "description": "Event description",
    "payload": {
      "field1": "type",
      "field2": "type"
    }
  }
}
```

### Accessibility Definition

```json
{
  "role": "ARIA role",
  "ariaLabel": "required|optional|auto",
  "ariaDescribedBy": "optional",
  "keyboardShortcuts": ["Enter", "Space"]
}
```

## Security Levels

### Safe

**Characteristics:**
- Pre-approved by security team
- No known vulnerabilities
- Standard HTML/Material Design components
- Can be used without review

**Examples:** text-field, button, card

### Trusted

**Characteristics:**
- Approved after security review
- Custom components
- Third-party components (vetted)
- Can be used in production

**Examples:** date-picker, table, dialog

### Review-Required

**Characteristics:**
- Not yet reviewed
- New custom components
- Experimental components
- Requires approval before use

**Examples:** Newly added custom components

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

## Best Practices

### Component Naming

- **Use kebab-case** for component types
- **Be descriptive** but concise
- **Avoid abbreviations** unless standard
- **Use consistent naming** across catalog

### Security

- **Start with review-required** for new components
- **Review thoroughly** before promoting to trusted
- **Document security considerations** in description
- **Validate all properties** with strict schemas

### Versioning

- **Export catalog** before major changes
- **Keep backups** of previous versions
- **Document breaking changes** in commit messages
- **Communicate changes** to team

### Organization

- **Group by category** for easy discovery
- **Use consistent property names** across components
- **Document all properties** thoroughly
- **Include examples** in descriptions

## Troubleshooting

### Error: "Component already exists"

**Solution:** Use `update` action instead:
```bash
/smartspec_manage_ui_catalog \
  --action update \
  --component-type slider \
  --component-def slider-component-v2.json \
  --apply
```

### Error: "Invalid component definition"

**Solution:** Validate JSON schema:
```bash
# Check JSON syntax
cat slider-component.json | jq .

# Ensure all required fields present
```

### Warning: "Component used in X specs"

**Solution:** Update affected specs:
```bash
# List affected specs
/smartspec_manage_ui_catalog \
  --action remove \
  --component-type slider

# Update each spec
/smartspec_generate_ui_spec \
  --spec specs/feature/spec-005-settings/spec.md \
  --output specs/feature/spec-005-settings/ui-spec.json \
  --apply
```

## Related Workflows

**After adding components:**

1. **Use in UI spec:**
   ```bash
   /smartspec_generate_ui_spec \
     --requirements "Use new slider component" \
     --spec specs/feature/spec-005-settings/ui-spec.json \
     --apply
   ```

2. **Implement UI:**
   ```bash
   /smartspec_implement_ui_from_spec \
     --spec specs/feature/spec-005-settings/ui-spec.json \
     --target-platform web \
     --output-dir src/ui/settings \
     --apply
   ```

## Security Considerations

- **Validate all inputs** - Prevent malicious component definitions
- **Backup before changes** - Enable rollback
- **Review custom components** - Security team approval
- **Audit catalog changes** - Track who changed what

## Version History

- **6.0.0** (2025-12-22): Initial release with A2UI v0.8 support

---

**Status:** Active  
**Requires Apply:** Yes (for catalog modifications)  
**Platform Support:** CLI, Kilo  
**Category:** UI Catalog Management
