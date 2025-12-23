# Knowledge Base: Multi-Level Theming Architecture

## 1. The Need for Advanced Theming

While a single, global theme is sufficient for many applications, enterprise-grade software and SaaS platforms require a more sophisticated approach. The ability to customize the user interface for different customers (white-labeling) or allow end-users to personalize their experience is a critical feature. This requires a theming system that can handle multiple layers of styles in a predictable and hierarchical manner.

This is the problem that the `/smartspec_resolve_themes` workflow is designed to solve.

## 2. The Hierarchical Theming Model

SmartSpec implements a hierarchical theming model that allows for multiple theme files to be merged into a single, resolved theme. The hierarchy is based on precedence, where themes applied later in the sequence override the values from earlier themes.

**System Theme (Base) < Company Theme < User Theme (Highest Precedence)**

This layered approach provides a powerful and flexible system for managing UI styles:

-   **System Theme:** This is the foundational, out-of-the-box theme for the application. It defines the core design language and acts as a fallback for all other layers.
-   **Company Theme:** This layer is used for white-labeling. A company (or tenant in a multi-tenant application) can provide a theme file that overrides the system theme with their own branding, such as custom logos, primary colors, and fonts.
-   **User Theme:** This is the highest-precedence layer, allowing individual users to personalize their experience. A common use case is selecting a "dark mode" or "high contrast" theme.

## 3. The `/smartspec_resolve_themes` Workflow

This workflow is the engine that powers the hierarchical theming model. It takes a base theme and a list of override themes and intelligently merges them to produce a final, resolved theme file.

### The Deep Merge Algorithm

The workflow uses a **deep merge** (or recursive merge) algorithm. This is a critical detail that makes the system both powerful and efficient. Instead of replacing entire objects, it merges them property by property.

Consider a `system.theme.json`:
```json
{
  "tokens": {
    "colors": {
      "primary": "#007bff",
      "background": "#ffffff"
    }
  }
}
```

And a `dark-mode.theme.json`:
```json
{
  "tokens": {
    "colors": {
      "background": "#121212"
    }
  }
}
```

When merged, the `resolve_themes` workflow will produce:
```json
{
  "tokens": {
    "colors": {
      "primary": "#007bff", // Retained from base
      "background": "#121212"  // Overridden by dark mode
    }
  }
}
```

This deep merge capability means that override themes only need to specify the values they want to change, making them small, manageable, and easy to maintain.

### Workflow Execution

Executing the workflow is straightforward:

```bash
/smartspec_resolve_themes \
  --base-theme "src/config/themes/system.theme.json" \
  --override-themes '["src/config/themes/company-acme.theme.json", "src/config/themes/user-123-dark.theme.json"]' \
  --output-file ".spec/resolved-theme.json"
```

This command tells SmartSpec to:
1.  Start with `system.theme.json`.
2.  Merge `company-acme.theme.json` on top of it.
3.  Finally, merge `user-123-dark.theme.json` on top of the result.
4.  Save the final, fully resolved theme to `.spec/resolved-theme.json`.

This output file is then used by the A2UI renderer to style the interface for that specific user session.

## 4. Practical Applications and Best Practices

### White-Labeling a SaaS Product

For a multi-tenant SaaS application, you can store a theme file for each customer (e.g., `acme.json`, `globex.json`). When a user from Acme Corp logs in, the application server invokes the `resolve_themes` workflow with the system theme and `acme.json` to generate a branded UI.

### User Personalization

Allow users to choose their preferred theme (e.g., Light, Dark, High Contrast) from a settings panel. When the user makes a selection, the application can call the workflow to merge their chosen theme on top of the system and company themes.

### Best Practices

-   **Keep Override Themes Lean:** Override themes should only contain the specific tokens they need to change. Avoid duplicating values that are already present in the base theme.
-   **Optional Overrides:** The workflow is designed to handle missing override files gracefully. This allows you to have optional themes (e.g., a user theme that may not exist for everyone) without causing errors.
-   **Clear Naming Convention:** Use a clear and consistent naming convention for your theme files (e.g., `system.json`, `company-acme.json`, `user-dark.json`) to make the hierarchy easy to understand.
-   **Dynamic Resolution:** In a live application, the `resolve_themes` workflow should be called dynamically at the start of a user session to ensure the correct theme is always applied.
