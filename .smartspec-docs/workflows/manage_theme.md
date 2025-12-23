_**Note:** This is the user manual for the `smartspec_manage_theme` workflow. For the technical workflow definition, please see [`.smartspec/workflows/smartspec_manage_theme.md`](../../.smartspec/workflows/smartspec_manage_theme.md)._

# Workflow: smartspec_manage_theme

## 1. Overview

The `smartspec_manage_theme` workflow is a powerful tool for managing the design system theme of your A2UI applications. It provides a structured and centralized way to define, update, and validate your project's visual identity, ensuring consistency across all generated UI components. This workflow is essential for maintaining a cohesive user experience and streamlining the design-to-development handoff.

At its core, the workflow operates on a `theme.json` file, which serves as the single source of truth for all styling information. By centralizing design tokens (like colors and fonts) and pre-defined component styles (variants), you can manage your design system with confidence and scale.

## 2. Key Concepts

To effectively use this workflow, it is important to understand a few key concepts.

### Design Tokens

Design tokens are the atomic, named entities that store your visual design attributes. Instead of hardcoding values like a specific hex code for a color (e.g., `#0ea5e9`), you use a token reference (e.g., `{colors.primary.500}`). This abstraction is the foundation of a scalable design system.

**Advantages of using design tokens:**
- **Consistency:** Ensures that the same values are used across the entire application, eliminating visual inconsistencies.
- **Maintainability:** Updating a token's value in one place automatically propagates the change to all components that reference it, making rebranding or style updates trivial.
- **Scalability:** Simplifies the management of complex design systems and makes it easy to introduce new themes (e.g., dark mode).

### `theme.json`

The `theme.json` file is the heart of the theming system. It is a structured JSON file that contains three main sections:

1.  **`tokens`**: A hierarchical collection of your design tokens. This includes colors, typography scales, spacing units, border radii, and shadows.
2.  **`components`**: A library of pre-styled component variants. For example, you can define what a `primary` button or an `elevated` card looks like.
3.  **`metadata`**: Information about the theme, such as its version, author, and source, which is useful for tracking and maintenance.

### Component Variants

Component variants are pre-defined styles for a specific component. For instance, a `button` component might have `primary`, `secondary`, and `danger` variants, each with a distinct appearance defined in `theme.json`. These variants reference the design tokens for their styling.

When generating UI specifications, you can simply specify the desired variant (e.g., `variant: "primary"`) instead of manually defining all the styles. This not only saves time but also enforces design consistency.

## 3. Parameters

The `smartspec_manage_theme` workflow is controlled by a set of parameters that allow you to perform various actions on the theme.

### Required Parameters

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `--action` | string | The specific action to perform on the theme. This is the primary parameter that determines the workflow's behavior. |

### Actions

The `--action` parameter accepts the following values:

| Action | Description |
| :--- | :--- |
| `init` | Creates a new `theme.json` file with a default set of tokens and variants. |
| `update-token` | Updates the value of a specific design token. |
| `add-variant` | Adds a new variant to a component's style definition. |
| `remove-variant` | Removes an existing component variant. |
| `validate` | Validates the `theme.json` schema and all token references. |
| `export-css` | Exports the theme's design tokens as CSS custom properties. |
| `export-scss` | Exports the theme's design tokens as SCSS variables. |

### Optional Parameters

The availability of optional parameters depends on the selected action.

| Parameter | Type | Description | Required For |
| :--- | :--- | :--- | :--- |
| `--token-path` | string | The JSON path to the token (e.g., `colors.primary.500`). | `update-token` |
| `--token-value` | string | The new value for the token. | `update-token` |
| `--component` | string | The name of the component (e.g., `button`). | `add-variant`, `remove-variant` |
| `--variant-name` | string | The name of the variant (e.g., `outline`). | `add-variant`, `remove-variant` |
| `--variant-spec` | JSON string | The JSON specification of the variant's styles. | `add-variant` |
| `--output-file` | string | The output file path for the exported theme. | `export-css`, `export-scss` |
| `--theme-file` | string | The path to the `theme.json` file. Defaults to `.spec/theme.json`. | All actions |

## 4. Example Usage

Here are some practical examples of how to use the `smartspec_manage_theme` workflow.

### Use Case 1: Initializing a New Theme

When starting a new project, you can create a default theme to get started quickly.

**Command:**
```bash
/smartspec_manage_theme --action init
```

**Result:** A `theme.json` file is created at `.spec/theme.json` with a standard set of design tokens and component variants, providing a solid foundation for your design system.

### Use Case 2: Updating a Brand Color

Imagine your brand's primary color changes. With the theming system, this is a simple, one-line change.

**Command:**
```bash
/smartspec_manage_theme \
  --action update-token \
  --token-path colors.primary.500 \
  --token-value "#a855f7" # New purple color
```

**Result:** The value of the `colors.primary.500` token is updated. All components that reference this token will automatically adopt the new color, ensuring a consistent update across your entire application.

### Use Case 3: Adding a Custom Button Variant

Suppose you need a new "outline" style for buttons that is not in the default theme.

**Command:**
```bash
/smartspec_manage_theme \
  --action add-variant \
  --component button \
  --variant-name outline \
  --variant-spec '{"backgroundColor": "transparent", "color": "{colors.primary.500}", "borderColor": "{colors.primary.500}"}'
```

**Result:** A new `outline` variant is added to the `button` component in `theme.json`. You can now use `variant: "outline"` in your UI specifications to create buttons with this style.

### Use Case 4: Validating the Theme

To ensure your theme is well-formed and all token references are correct, you can run the validation action.

**Command:**
```bash
/smartspec_manage_theme --action validate
```

**Result:** The workflow checks the `theme.json` file for schema compliance and verifies that all token references (e.g., `{colors.primary.500}`) point to valid tokens. It will report any errors or warnings it finds.

### Use Case 5: Exporting for Web Development

To use your design tokens in a traditional web project, you can export them as CSS variables.

**Command:**
```bash
/smartspec_manage_theme \
  --action export-css \
  --output-file public/theme.css
```

**Result:** A `theme.css` file is created with all your design tokens converted to CSS custom properties, which can be directly used in your web application's stylesheets.

## 5. Related Workflows

- **`smartspec_import_penpot_tokens`**: Imports design tokens directly from a Penpot design file, bridging the gap between design and code.
- **`smartspec_generate_ui_spec`**: Generates A2UI specifications that can reference the variants and tokens defined in your theme.
- **`smartspec_validate_golden_tests`**: Uses the theme file to validate that A2UI JSON output correctly references theme tokens.
