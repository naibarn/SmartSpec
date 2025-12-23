# smartspec_export_catalog

## Overview
**Version:** 1.0.0  
**Category:** A2UI

Export SmartSpec UI catalog to standard A2UI v0.8 format, enabling interoperability with external A2UI renderers while preserving SmartSpec's governance model as the source of truth.

## Purpose
This workflow bridges the gap between SmartSpec's server-side, governed component catalog and A2UI's client-side catalog model. It allows components managed within SmartSpec to be used by any A2UI-compliant renderer, providing a clear path from SmartSpec governance to A2UI ecosystem interoperability.

## Usage

### Command Line Interface
```bash
/smartspec_export_catalog \
  --output-file public/web-catalog.json \
  --catalog-id "https://my-app.com/web-catalog-v1" \
  --output-format a2ui-v0.8
```

### Kilo Code
```
export catalog to A2UI format for web platform
```

## Use Cases

### 1. Web Application Deployment
**Scenario:** You've built a component library using SmartSpec governance and now want to deploy it as a web application using a standard A2UI renderer.

**Command:**
```bash
/smartspec_export_catalog \
  --input-catalog .spec/ui-catalog.json \
  --output-file public/web-catalog.json \
  --catalog-id "https://myapp.com/catalogs/web-v1" \
  --output-format a2ui-v0.8 \
  --platform web
```

**Result:** A standard A2UI catalog file that can be compiled into your React, Vue, or vanilla JavaScript web renderer.

---

### 2. Multi-Platform Deployment
**Scenario:** You need to deploy the same component library to both web and Flutter platforms.

**Commands:**
```bash
# Export for web
/smartspec_export_catalog \
  --output-file dist/web-catalog.json \
  --catalog-id "https://myapp.com/catalogs/web-v1" \
  --platform web

# Export for Flutter
/smartspec_export_catalog \
  --output-file dist/flutter-catalog.json \
  --catalog-id "https://myapp.com/catalogs/flutter-v1" \
  --platform flutter
```

**Result:** Two platform-specific A2UI catalogs, each optimized for its target renderer.

---

### 3. Gradual Migration
**Scenario:** You're migrating from a custom UI system to A2UI and want to test compatibility before fully committing.

**Command:**
```bash
/smartspec_export_catalog \
  --output-file test/a2ui-catalog.json \
  --catalog-id "https://myapp.com/catalogs/test-v1" \
  --include-metadata
```

**Result:** An A2UI catalog with SmartSpec metadata included as comments, allowing you to verify the transformation and debug any issues.

## Parameters

### Required Parameters

| Parameter | Type | Description |
|:----------|:-----|:------------|
| `--output-file` | string | Path where the exported A2UI catalog will be written (e.g., `public/web-catalog.json`) |
| `--catalog-id` | string | Unique identifier for the exported catalog, typically a URL (e.g., `https://my-app.com/web-catalog-v1`) |
| `--output-format` | string | Target format, currently only `a2ui-v0.8` is supported |

### Optional Parameters

| Parameter | Type | Default | Description |
|:----------|:-----|:--------|:------------|
| `--input-catalog` | string | `.spec/ui-catalog.json` | Path to the SmartSpec catalog file |
| `--platform` | string | (none) | Platform filter for multi-platform catalogs (e.g., `web`, `flutter`, `mobile`) |
| `--include-metadata` | boolean | `false` | Include SmartSpec metadata as comments in the output |

## Output

The workflow produces:

1. **A2UI v0.8 Catalog Definition Document** (JSON file)
   - Valid A2UI catalog with `catalogId` and `components` array
   - Each component has an `id`, `type`, and `properties` object
   - Properties include `type`, `description`, and `default` values

2. **Transformation Report** (console output)
   - Number of components exported
   - Number of properties mapped
   - Any warnings or skipped fields

### Example Output File
```json
{
  "catalogId": "https://my-app.com/web-catalog-v1",
  "version": "0.8",
  "components": [
    {
      "id": "input-name",
      "type": "TextInput",
      "properties": {
        "label": {
          "type": "string",
          "description": "The text label for the component.",
          "default": "Name"
        },
        "required": {
          "type": "boolean",
          "description": "Whether the input is required.",
          "default": true
        },
        "placeholder": {
          "type": "string",
          "description": "Placeholder text for the input.",
          "default": "Enter your name"
        }
      }
    }
  ]
}
```

## Transformation Logic

### Component Type Mapping

| SmartSpec Type | A2UI Type |
|:---------------|:----------|
| `input-text` | `TextInput` |
| `input-email` | `EmailInput` |
| `button-primary` | `Button` |
| `data-table` | `Table` |
| `card` | `Card` |
| `modal` | `Modal` |

### Property Mapping

| SmartSpec Property | A2UI Property | Notes |
|:-------------------|:--------------|:------|
| `label` | `properties.label.default` | Mapped as default value |
| `required` | `properties.required.default` | Mapped as default value |
| `placeholder` | `properties.placeholder.default` | Mapped as default value |
| `validation` | (not exported) | Governance-only metadata |
| `complexity` | (not exported) | Governance-only metadata |
| `tags` | (not exported) | Governance-only metadata |

## Related Workflows

- **smartspec_manage_ui_catalog**: Manage the source SmartSpec catalog before export
- **smartspec_generate_ui_spec**: Generate UI specs using the SmartSpec catalog
- **smartspec_ui_component_audit**: Audit components before export to ensure quality

## Best Practices

1. **Version Your Catalog ID**: Use versioned URLs (e.g., `-v1`, `-v2`) in your `catalog-id` to track breaking changes
2. **Export During Build**: Integrate the export step into your CI/CD pipeline
3. **Keep SmartSpec as Source of Truth**: Always edit the SmartSpec catalog, then re-export
4. **Test After Export**: Validate the exported catalog with your target renderer before deployment
5. **Document Platform Differences**: If using multi-platform, document platform-specific properties

## Notes

- The exported catalog is a **derived artifact**; the SmartSpec catalog remains the source of truth
- Governance metadata (validation rules, complexity, tags) is intentionally excluded from the A2UI export
- For multi-platform support, export separate catalogs for each platform
- The `catalog-id` should follow URI conventions and be versioned for breaking changes

## See Also

- [A2UI Export Utility Design](../../docs/guides/A2UI_EXPORT_UTILITY_DESIGN.md)
- [SmartSpec-Flavored A2UI](../../docs/guides/A2UI_SMARTSPEC_FLAVOR.md)
- [A2UI v0.8 Specification](https://a2ui.org/specification/v0.8-a2ui/)
