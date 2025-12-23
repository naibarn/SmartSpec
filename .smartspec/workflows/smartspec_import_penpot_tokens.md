# smartspec_import_penpot_tokens

## Overview
Imports design tokens from Penpot design files into the SmartSpec theme system.

## Version
1.0.0

## Category
ui_theming_and_design

## Description
This workflow allows you to **import design tokens** (colors, typography, spacing) from **Penpot** design files into your SmartSpec `theme.json`. Penpot is an open-source design and prototyping platform, and this workflow bridges the gap between design and development by automatically extracting design tokens from Penpot exports.

The workflow supports:
- **Color tokens** from Penpot color libraries
- **Typography tokens** from text styles
- **Component variants** from Penpot components
- **Automatic mapping** to SmartSpec theme structure

## Parameters

### Required Parameters

#### `--source`
- **Type:** string
- **Required:** Yes
- **Description:** Source of Penpot tokens
- **Allowed Values:**
  - `file`: Import from exported Penpot JSON file
  - `api`: Import directly from Penpot API (requires authentication)

#### `--input-file`
- **Type:** string
- **Required:** For `file` source
- **Description:** Path to the exported Penpot JSON file
- **Example:** `design/penpot-export.json`

### Optional Parameters

#### `--penpot-url`
- **Type:** string
- **Required:** For `api` source
- **Description:** Penpot instance URL
- **Default:** `https://design.penpot.app`
- **Example:** `https://design.penpot.app`

#### `--project-id`
- **Type:** string
- **Required:** For `api` source
- **Description:** Penpot project ID
- **Example:** `a1b2c3d4-e5f6-7890-abcd-ef1234567890`

#### `--file-id`
- **Type:** string
- **Required:** For `api` source
- **Description:** Penpot file ID
- **Example:** `f1e2d3c4-b5a6-9870-fedc-ba0987654321`

#### `--access-token`
- **Type:** string
- **Required:** For `api` source
- **Description:** Penpot API access token
- **Example:** `penpot_token_abc123...`

#### `--merge-strategy`
- **Type:** string
- **Required:** No
- **Default:** `merge`
- **Description:** How to handle conflicts with existing theme
- **Allowed Values:**
  - `merge`: Merge with existing theme (keep existing values on conflict)
  - `overwrite`: Overwrite existing theme completely
  - `append`: Only add new tokens, skip existing ones

#### `--theme-file`
- **Type:** string
- **Required:** No
- **Default:** `.spec/theme.json`
- **Description:** Path to the theme.json file

#### `--mapping-file`
- **Type:** string
- **Required:** No
- **Description:** Custom mapping file for Penpot → SmartSpec token conversion
- **Example:** `config/penpot-mapping.json`

## Behavior

### Source: `file`
1. Reads the Penpot export JSON file
2. Extracts color libraries, text styles, and components
3. Maps Penpot tokens to SmartSpec theme structure
4. Merges with existing theme based on merge strategy
5. Validates the updated theme
6. Saves changes to `theme.json`

### Source: `api`
1. Authenticates with Penpot API using access token
2. Fetches project and file data
3. Extracts design tokens from the file
4. Maps tokens to SmartSpec theme structure
5. Merges with existing theme
6. Validates and saves

### Token Mapping
The workflow automatically maps Penpot tokens to SmartSpec structure:

| Penpot Element | SmartSpec Path | Notes |
|----------------|----------------|-------|
| Color Library → Primary | `tokens.colors.primary.*` | Maps color shades |
| Color Library → Secondary | `tokens.colors.secondary.*` | Maps color shades |
| Text Style → Heading 1 | `tokens.typography.fontSize.4xl` | Maps font size |
| Text Style → Body | `tokens.typography.fontSize.base` | Maps font size |
| Component → Button/Primary | `components.button.variants.primary` | Maps component styles |

## Output
- **Updated theme.json:** Theme file with imported Penpot tokens
- **Import Report:** Summary of imported tokens (colors, typography, components)
- **Validation Report:** Any errors or warnings from theme validation

## Example Usage

### CLI

```bash
# Import from Penpot export file
/smartspec_import_penpot_tokens \
  --source file \
  --input-file design/penpot-tokens.json

# Import from Penpot API
/smartspec_import_penpot_tokens \
  --source api \
  --penpot-url https://design.penpot.app \
  --project-id a1b2c3d4-e5f6-7890-abcd-ef1234567890 \
  --file-id f1e2d3c4-b5a6-9870-fedc-ba0987654321 \
  --access-token $PENPOT_TOKEN

# Import with overwrite strategy
/smartspec_import_penpot_tokens \
  --source file \
  --input-file design/penpot-tokens.json \
  --merge-strategy overwrite
```

### Kilo Code

```kilo
# Import from file
smartspec_import_penpot_tokens(
  source="file",
  input_file="design/penpot-tokens.json"
)

# Import from API
smartspec_import_penpot_tokens(
  source="api",
  penpot_url="https://design.penpot.app",
  project_id="a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  file_id="f1e2d3c4-b5a6-9870-fedc-ba0987654321",
  access_token=env.PENPOT_TOKEN
)
```

## Use Cases

### Use Case 1: Import Design System from Penpot
**Scenario:** Design team has created a complete design system in Penpot with colors, typography, and components.

**Steps:**
1. Export the Penpot file as JSON
2. Run the import workflow
3. Validate the imported theme

**Command:**
```bash
/smartspec_import_penpot_tokens \
  --source file \
  --input-file design/design-system.json
```

**Result:** Complete theme.json with all design tokens from Penpot.

---

### Use Case 2: Sync Design Changes from Penpot
**Scenario:** Design team has updated brand colors in Penpot, need to sync to development.

**Command:**
```bash
/smartspec_import_penpot_tokens \
  --source api \
  --project-id abc123 \
  --file-id def456 \
  --access-token $PENPOT_TOKEN \
  --merge-strategy merge
```

**Result:** Updated colors in theme.json while preserving custom tokens.

---

### Use Case 3: Bootstrap New Project from Penpot
**Scenario:** Starting a new project with an existing Penpot design file.

**Command:**
```bash
/smartspec_import_penpot_tokens \
  --source file \
  --input-file design/new-project.json \
  --merge-strategy overwrite
```

**Result:** Fresh theme.json based entirely on Penpot design.

## Penpot Export Instructions

To export design tokens from Penpot:

1. Open your Penpot file
2. Go to **Main Menu** → **Export**
3. Select **Export as JSON**
4. Save the file (e.g., `penpot-export.json`)
5. Use this file with the workflow

For API access:
1. Go to **Penpot Settings** → **Access Tokens**
2. Create a new access token
3. Copy the token and use it with `--access-token`

## Related Workflows
- `smartspec_manage_theme`: Manage theme after import
- `smartspec_generate_ui_spec`: Use imported theme in UI specs
- `smartspec_export_catalog`: Export theme with catalog

## Implementation
Implemented in: `.smartspec/scripts/import_penpot_tokens.py`

## Notes
- Penpot color names are automatically mapped to SmartSpec color scales (50-900)
- Custom mapping files allow you to control how Penpot tokens map to SmartSpec
- The workflow preserves Penpot component structure when possible
- API import requires network access to Penpot instance
- Imported themes are automatically validated before saving
