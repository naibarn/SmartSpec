# Knowledge Base: Theming System Concepts

## 1. Introduction to Theming in SmartSpec

The SmartSpec theming system is a comprehensive solution for managing the visual identity of your A2UI applications. It is built on the principle of a **single source of truth**, ensuring that your design language is applied consistently and can be maintained with ease. By abstracting styling decisions into a centralized `theme.json` file, the system decouples design from implementation, allowing for greater flexibility and scalability.

This document provides a deep dive into the core concepts, benefits, and best practices of using the SmartSpec theming system.

## 2. The Philosophy: Design Tokens

The foundation of the theming system is **design tokens**. These are the atomic, named variables that store your visual design attributes. Instead of hardcoding a hex value like `#1d4ed8` for a button's background, you use a semantic token reference like `{colors.primary.600}`.

### Why Use Design Tokens?

- **Consistency and Cohesion:** Tokens enforce the use of a pre-defined palette of colors, fonts, and spacing, ensuring a cohesive visual experience across the entire application.
- **Effortless Maintenance:** When a brand color needs to be updated, you only need to change the value of a single token. The change will automatically propagate to every component that references it, saving countless hours of manual work.
- **Scalability and Theming:** Tokens are essential for building scalable design systems. They make it trivial to implement new themes, such as a **dark mode**. A dark mode theme can be created by simply providing a new set of token values for the same token names.
- **Clear Communication:** Tokens create a shared language between designers and developers. A developer can implement a `primary` button without needing to know the exact hex code, as it is already defined in the theme.

### Structure of Tokens

In `theme.json`, tokens are organized hierarchically for clarity and ease of use:

```json
{
  "tokens": {
    "colors": {
      "primary": {
        "50": "#eff6ff",
        "100": "#dbeafe",
        // ...
        "900": "#1e3a8a"
      }
    },
    "typography": {
      "fontFamily": {
        "sans": "Inter, sans-serif"
      },
      "fontSize": {
        "sm": "0.875rem"
      }
    },
    "spacing": {
      "4": "1rem"
    }
  }
}
```

## 3. The `theme.json` File: The Single Source of Truth

The `theme.json` file is the heart of the system. It is a structured JSON file that centralizes all aspects of your design system.

### Key Sections

1.  **`tokens`**: This section contains all the atomic design tokens, as described above. It is the foundational layer of the theme.
2.  **`components`**: This section defines pre-styled **variants** for your UI components. It maps semantic variant names (e.g., `primary`, `outline`) to a set of styles that reference the design tokens.
3.  **`metadata`**: This section stores important information about the theme, such as its version, author, and a description. This is useful for tracking changes and managing multiple themes.

### Component Variants

Component variants are a powerful feature that allows you to define reusable styles for your components. Instead of manually styling each button, you can define variants like `primary`, `secondary`, and `danger` once in your theme.

**Example of a Button Variant:**

```json
{
  "components": {
    "button": {
      "variants": {
        "primary": {
          "backgroundColor": "{colors.primary.600}",
          "color": "{colors.white}",
          "hover": {
            "backgroundColor": "{colors.primary.700}"
          }
        },
        "outline": {
          "backgroundColor": "transparent",
          "color": "{colors.primary.600}",
          "borderColor": "{colors.primary.600}"
        }
      }
    }
  }
}
```

When generating a UI specification, you can simply use `variant: "primary"` to apply this style, ensuring consistency and reducing redundancy.

## 4. Multi-Level Theming with `/smartspec_resolve_themes`

While a single `theme.json` is powerful, real-world applications often require multiple layers of theming to support white-labeling, company-specific branding, and user personalization. The `/smartspec_resolve_themes` workflow is designed for this exact purpose.

### The Hierarchy

The workflow operates on a clear hierarchy, where themes are merged in a specific order, with later themes overriding earlier ones:

**System Theme (Base) < Company Theme < User Theme (Highest Precedence)**

This allows you to:
1.  **Define a robust base theme** with system-wide defaults.
2.  **Apply company-specific branding** (e.g., Acme Corp's primary color is red) that overrides the base.
3.  **Allow user personalization** (e.g., User 123 prefers dark mode) that overrides both the company and system themes.

### How It Works

The `/smartspec_resolve_themes` workflow performs a **deep merge** on the theme files. This means it recursively merges nested objects, allowing for fine-grained overrides. For example, a user theme can change just the `colors.primary.500` token without needing to redefine the entire `colors` object.

```bash
# Example of resolving a theme for a specific user
/smartspec_resolve_themes \
  --base-theme "src/config/themes/system.theme.json" \
  --override-themes '["src/config/themes/company-acme.theme.json", "src/config/themes/user-123.theme.json"]' \
  --output-file ".spec/resolved-theme.json"
```

This resolved theme then becomes the single source of truth for the UI renderer for that specific user session.

## 5. Core Theming Workflows

SmartSpec provides two key workflows for managing your theme:

### `smartspec_manage_theme`

This is your primary tool for interacting with the `theme.json` file. It allows you to:
- **Initialize** a new theme with a default structure.
- **Update** the value of any design token.
- **Add or remove** component variants.
- **Validate** the theme for schema compliance and broken token references.
- **Export** your tokens to CSS or SCSS for use in traditional web projects.

### `smartspec_import_penpot_tokens`

This workflow automates the process of synchronizing your design system from **Penpot**. It can import tokens directly from a Penpot file or via its API, mapping Penpot's color libraries and text styles to the `theme.json` structure. This creates a seamless bridge between your design tool and your development environment.

## 6. Best Practices

- **Start with a Strong Foundation:** Use the `init` action to create a well-structured default theme. It is easier to customize an existing structure than to build one from scratch.
- **Embrace Semantic Naming:** Use meaningful names for your tokens (e.g., `colors.action.primary` instead of `colors.blue.500`). This makes the system more intuitive and resilient to changes.
- **Keep It DRY (Don't Repeat Yourself):** Leverage token references within other tokens or in component variants. For example, a `hover` color can be a slightly darker shade of the base color token.
- **Validate Regularly:** Run the `validate` action frequently, especially in a CI/CD pipeline, to catch errors early.
- **Integrate with Your Design Process:** Use the `smartspec_import_penpot_tokens` workflow to ensure that your theme always reflects the latest design decisions.

By adopting the SmartSpec theming system, you are investing in a more scalable, maintainable, and consistent approach to UI development. It empowers your team to build beautiful, cohesive applications faster than ever before.
