# `/smartspec_ui_catalog_generator` - Generate UI Component Catalog

| Metadata | Value |
|----------|-------|
| **Workflow ID** | `smartspec_ui_catalog_generator` |
| **Category** | UI / A2UI |
| **Version** | 6.0.0+ |
| **Requires `--apply`** | Yes |
| **Platform Support** | CLI, Kilo Code |

---

## Overview

Generate a comprehensive UI component catalog from existing UI specifications and implementations. This workflow scans your project for UI components, analyzes their structure and usage, and creates or updates the `.spec/ui-catalog.json` file that serves as the component library for A2UI workflows.

The generated catalog includes component definitions, variants, properties, accessibility features, and usage examples.

---

## Usage

### CLI

```bash
/smartspec_ui_catalog_generator \
  --scan-dir src/ui \
  --output .spec/ui-catalog.json
```

### Kilo Code

```bash
/smartspec_ui_catalog_generator.md \
  --scan-dir src/ui \
  --output .spec/ui-catalog.json \
  --platform kilo
```

---

## Use Cases

### 1. Generate Catalog from Existing Components

**Scenario:** Create a catalog from your existing React components.

**Command:**
```bash
/smartspec_ui_catalog_generator \
  --scan-dir src/components \
  --target-platform web \
  --framework react \
  --output .spec/ui-catalog.json
```

**Expected Result:** Complete catalog with all discovered components, props, and usage patterns.

### 2. Update Catalog with New Components

**Scenario:** Add newly created components to existing catalog.

**Command:**
```bash
/smartspec_ui_catalog_generator \
  --scan-dir src/components/new \
  --merge \
  --output .spec/ui-catalog.json
```

**Expected Result:** Existing catalog updated with new components while preserving existing entries.

### 3. Generate Catalog from UI Specs

**Scenario:** Create catalog from UI specification files.

**Command:**
```bash
/smartspec_ui_catalog_generator \
  --scan-specs specs/feature/*/ui-spec.json \
  --include-variants \
  --output .spec/ui-catalog.json
```

**Expected Result:** Catalog generated from spec definitions including all component variants.

---

## Parameters

### Required Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `--scan-dir` or `--scan-specs` | path | Directory to scan for components or specs pattern |
| `--output` | path | Output path for catalog file |

### Universal Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--apply` | boolean | false | Apply changes (without this flag, runs in preview mode) |
| `--platform` | string | cli | Platform: cli, kilo |
| `--verbose` | boolean | false | Enable verbose output |
| `--dry-run` | boolean | false | Simulate without making changes |
| `--report-dir` | path | auto | Custom report directory |
| `--force` | boolean | false | Force overwrite existing catalog |

### Workflow-Specific Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--target-platform` | string | auto | Target platform: web, flutter, mobile |
| `--framework` | string | auto | Framework: react, vue, angular, flutter |
| `--merge` | boolean | false | Merge with existing catalog instead of replacing |
| `--include-variants` | boolean | true | Include component variants in catalog |
| `--include-examples` | boolean | true | Include usage examples |
| `--include-accessibility` | boolean | true | Include accessibility metadata |
| `--exclude-pattern` | string | - | Glob pattern for files to exclude |
| `--category-mapping` | path | - | Custom category mapping file |
| `--security-level` | string | review-required | Default security level: safe, trusted, review-required |

---

## Output

### Report Location
```
.spec/reports/ui-catalog-generator/<run-id>/
├── report.md              # Human-readable summary
├── report.json            # Machine-readable data
└── preview/
    ├── catalog.json       # Preview of generated catalog
    ├── components.md      # Component list
    └── statistics.json    # Catalog statistics
```

### Generated Files (with `--apply`)
- `.spec/ui-catalog.json` - Complete UI component catalog

### Catalog Structure
```json
{
  "version": "0.8",
  "metadata": {
    "generated": "2025-12-22T...",
    "component_count": 42,
    "platform": "web"
  },
  "categories": {
    "input": [...],
    "layout": [...],
    "data": [...],
    "feedback": [...],
    "overlay": [...],
    "basic": [...]
  },
  "components": [
    {
      "id": "button",
      "name": "Button",
      "category": "basic",
      "variants": [...],
      "properties": [...],
      "accessibility": {...},
      "examples": [...]
    }
  ]
}
```

---

## Catalog Features

### Component Discovery
- ✅ Automatic component detection
- ✅ Props/properties extraction
- ✅ Variant identification
- ✅ Dependency analysis

### Metadata Extraction
- ✅ Component documentation
- ✅ Usage examples
- ✅ Accessibility features
- ✅ Platform compatibility

### Categorization
- ✅ Automatic category assignment
- ✅ Custom category mapping
- ✅ Component relationships
- ✅ Security classification

### Validation
- ✅ Schema validation
- ✅ Duplicate detection
- ✅ Naming consistency
- ✅ Accessibility compliance

---

## Prerequisites

**Required:**
- A2UI enabled in config
- Source code or UI specs to scan
- Write access to `.spec/` directory

**Optional:**
- Existing catalog for merging
- Custom category mapping
- Component documentation

---

## Notes

1. **Preview First:** Always run without `--apply` to review discovered components
2. **Merge Mode:** Use `--merge` to add to existing catalog without losing entries
3. **Exclusions:** Use `--exclude-pattern` to skip test files, stories, etc.
4. **Security:** Components default to `review-required` security level
5. **Platform Detection:** Framework and platform are auto-detected when possible
6. **Variants:** Component variants are automatically identified and cataloged
7. **Accessibility:** WCAG compliance features are extracted when available
8. **Updates:** Re-run to update catalog when components change

---

## Related Workflows

- [`/smartspec_generate_ui_spec`](./generate_ui_spec.md) - Generate UI specification
- [`/smartspec_optimize_ui_catalog`](./optimize_ui_catalog.md) - Optimize catalog performance
- [`/smartspec_ui_component_audit`](./ui_component_audit.md) - Audit components
- [`/smartspec_manage_ui_catalog`](./ui_catalog_generator.md) - Manage catalog manually

---

**For more information, see the [A2UI Documentation](../../README-A2UI.md).**
