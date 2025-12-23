# smartspec_manage_theme

## Overview
Manages the design system theme (colors, typography, spacing, component variants) for A2UI applications.

## Version
1.0.0

## Category
ui_theming_and_design

## Description
This workflow allows you to create, update, and validate the `theme.json` file, which serves as the **source of truth for styling** in SmartSpec A2UI applications. The theme defines design tokens (colors, typography, spacing, shadows) and component variants (button styles, input states, etc.) that ensure UI consistency across all generated components.

## Parameters

### Required Parameters

#### `--action`
- **Type:** string
- **Required:** Yes
- **Description:** The action to perform on the theme
- **Allowed Values:**
  - `init`: Create a new theme.json with default values
  - `update-token`: Update a specific design token
  - `add-variant`: Add a new component variant
  - `remove-variant`: Remove a component variant
  - `validate`: Validate the theme.json schema
  - `export-css`: Export theme as CSS variables
  - `export-scss`: Export theme as SCSS variables

### Optional Parameters (depends on action)

#### `--token-path`
- **Type:** string
- **Required:** For `update-token` action
- **Description:** JSON path to the token (e.g., `colors.primary.500`, `typography.fontSize.lg`)
- **Example:** `colors.primary.500`

#### `--token-value`
- **Type:** string
- **Required:** For `update-token` action
- **Description:** New value for the token
- **Example:** `#0ea5e9`

#### `--component`
- **Type:** string
- **Required:** For `add-variant` and `remove-variant` actions
- **Description:** Component name (e.g., `button`, `input`, `card`)
- **Example:** `button`

#### `--variant-name`
- **Type:** string
- **Required:** For `add-variant` and `remove-variant` actions
- **Description:** Variant name (e.g., `primary`, `secondary`, `danger`)
- **Example:** `outline`

#### `--variant-spec`
- **Type:** JSON string
- **Required:** For `add-variant` action
- **Description:** JSON specification of the variant styles
- **Example:** `{"backgroundColor": "transparent", "borderColor": "{colors.primary.500}"}`

#### `--output-file`
- **Type:** string
- **Required:** For `export-css` and `export-scss` actions
- **Description:** Output file path for exported theme
- **Example:** `public/theme.css`

#### `--theme-file`
- **Type:** string
- **Required:** No
- **Default:** `.spec/theme.json`
- **Description:** Path to the theme.json file

## Behavior

### Action: `init`
1. Creates a new `theme.json` file with default design tokens
2. Includes standard color palette, typography scale, spacing, and shadows
3. Defines default variants for common components (button, input, card, text)
4. Validates the generated theme

### Action: `update-token`
1. Reads the existing `theme.json`
2. Updates the specified token at the given path
3. Validates the updated theme
4. Saves the changes

### Action: `add-variant`
1. Reads the existing `theme.json`
2. Adds the new variant to the specified component
3. Validates that the variant spec uses valid token references
4. Saves the changes

### Action: `remove-variant`
1. Reads the existing `theme.json`
2. Removes the specified variant from the component
3. Saves the changes

### Action: `validate`
1. Reads the `theme.json`
2. Validates the JSON schema
3. Checks that all token references (e.g., `{colors.primary.500}`) are valid
4. Reports any errors or warnings

### Action: `export-css`
1. Reads the `theme.json`
2. Converts design tokens to CSS custom properties (variables)
3. Writes the output to the specified file

### Action: `export-scss`
1. Reads the `theme.json`
2. Converts design tokens to SCSS variables
3. Writes the output to the specified file

## Output
- **Success:** Updated `theme.json` file or exported theme file
- **Validation Report:** If action is `validate`, returns a report of errors/warnings
- **Statistics:** Number of tokens, components, and variants in the theme

## Example Usage

### CLI

```bash
# Initialize a new theme
/smartspec_manage_theme --action init

# Update a color token
/smartspec_manage_theme \
  --action update-token \
  --token-path colors.primary.500 \
  --token-value "#0ea5e9"

# Add a new button variant
/smartspec_manage_theme \
  --action add-variant \
  --component button \
  --variant-name outline \
  --variant-spec '{"backgroundColor": "transparent", "color": "{colors.primary.500}", "borderColor": "{colors.primary.500}"}'

# Validate the theme
/smartspec_manage_theme --action validate

# Export theme as CSS
/smartspec_manage_theme \
  --action export-css \
  --output-file public/theme.css
```

### Kilo Code

```kilo
# Initialize theme
smartspec_manage_theme(action="init")

# Update primary color
smartspec_manage_theme(
  action="update-token",
  token_path="colors.primary.500",
  token_value="#0ea5e9"
)

# Add outline button variant
smartspec_manage_theme(
  action="add-variant",
  component="button",
  variant_name="outline",
  variant_spec={
    "backgroundColor": "transparent",
    "color": "{colors.primary.500}",
    "borderColor": "{colors.primary.500}"
  }
)
```

## Use Cases

### Use Case 1: Initialize Theme for New Project
**Scenario:** Starting a new A2UI project and need a design system theme.

**Command:**
```bash
/smartspec_manage_theme --action init
```

**Result:** A complete `theme.json` with default tokens and component variants.

---

### Use Case 2: Update Brand Colors
**Scenario:** The brand primary color has changed from blue to purple.

**Command:**
```bash
/smartspec_manage_theme \
  --action update-token \
  --token-path colors.primary.500 \
  --token-value "#a855f7"
```

**Result:** All components using `{colors.primary.500}` will now use the new purple color.

---

### Use Case 3: Add Custom Button Variant
**Scenario:** Need a new "outline" button style for secondary actions.

**Command:**
```bash
/smartspec_manage_theme \
  --action add-variant \
  --component button \
  --variant-name outline \
  --variant-spec '{"backgroundColor": "transparent", "color": "{colors.primary.500}", "borderColor": "{colors.primary.500}", "states": {"hover": {"backgroundColor": "{colors.primary.50}"}}}'
```

**Result:** New `outline` variant is available for use in UI specs.

## Related Workflows
- `smartspec_import_penpot_tokens`: Import design tokens from Penpot
- `smartspec_generate_ui_spec`: Generate UI specs that use theme variants
- `smartspec_ui_validation`: Validate that UI specs use valid theme variants

## Implementation
Implemented in: `.smartspec/scripts/manage_theme.py`

## Notes
- Theme tokens use a reference syntax: `{path.to.token}` (e.g., `{colors.primary.500}`)
- Component variants should reference tokens, not hardcode values, for consistency
- Exported CSS/SCSS files can be used in web projects for consistent styling
- The theme is a design-time artifact; it does not appear in the A2UI JSON payload
