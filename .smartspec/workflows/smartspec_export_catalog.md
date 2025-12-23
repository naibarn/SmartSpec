# smartspec_export_catalog

## Overview
Export SmartSpec UI catalog to standard A2UI v0.8 format for interoperability with external A2UI renderers.

## Version
1.0.0

## Category
A2UI

## Description
This workflow converts a SmartSpec-managed UI catalog (`.spec/ui-catalog.json`) into a standard A2UI v0.8 Catalog Definition Document. This enables UI components governed by SmartSpec to be used by any A2UI-compliant renderer, bridging the gap between SmartSpec's server-side governance model and A2UI's client-side catalog model.

## Use Cases
1. **Interoperability**: Export SmartSpec components for use in standard A2UI web or mobile renderers
2. **Multi-Platform Deployment**: Generate platform-specific A2UI catalogs from a single governed source
3. **Migration Path**: Transition from SmartSpec governance to standard A2UI ecosystem while preserving component definitions

## Parameters

### Required Parameters
- `output_file` (string): Path where the exported A2UI catalog will be written (e.g., `public/web-catalog.json`)
- `catalog_id` (string): Unique identifier for the exported catalog, typically a URL (e.g., `https://my-app.com/web-catalog-v1`)
- `output_format` (string): Target format, currently only `a2ui-v0.8` is supported

### Optional Parameters
- `input_catalog` (string): Path to the SmartSpec catalog file (default: `.spec/ui-catalog.json`)
- `platform` (string): Platform filter for multi-platform catalogs (e.g., `web`, `flutter`, `mobile`)
- `include_metadata` (boolean): Include SmartSpec metadata as comments in the output (default: `false`)

## Behavior
1. Reads the SmartSpec catalog from `input_catalog`
2. Validates the catalog structure
3. Transforms each component to A2UI v0.8 format:
   - Maps SmartSpec component types to A2UI component types
   - Converts SmartSpec properties to A2UI property definitions
   - Filters out governance-only metadata (complexity, tags, validation rules)
4. Generates a valid A2UI Catalog Definition Document with the specified `catalog_id`
5. Writes the result to `output_file`
6. Reports transformation statistics

## Output
- A valid A2UI v0.8 Catalog Definition Document (JSON file)
- Transformation report showing:
  - Number of components exported
  - Number of properties mapped
  - Any warnings or skipped fields

## Example Usage

### CLI
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

## Flags
- `--input-catalog`: Source SmartSpec catalog path
- `--output-file`: Destination A2UI catalog path
- `--catalog-id`: Unique catalog identifier (URL)
- `--output-format`: Target format (a2ui-v0.8)
- `--platform`: Platform filter (optional)
- `--include-metadata`: Include SmartSpec metadata (optional)

## Related Workflows
- `smartspec_manage_ui_catalog`: Manage the source SmartSpec catalog
- `smartspec_generate_ui_spec`: Generate UI specs using the SmartSpec catalog
- `smartspec_ui_component_audit`: Audit components before export

## Notes
- The exported catalog is a **derived artifact**; the SmartSpec catalog remains the source of truth
- Governance metadata (validation rules, complexity, tags) is not included in the A2UI export
- For multi-platform support, export separate catalogs for each platform
- The `catalog_id` should be versioned (e.g., append `-v1`, `-v2`) when making breaking changes

## Implementation
Implemented in: `.smartspec/scripts/export_catalog.py`
