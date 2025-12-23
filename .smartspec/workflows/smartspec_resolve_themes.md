---
title: 'SmartSpec Resolve Themes'
workflow_id: 'smartspec_resolve_themes'
version: '1.0.0'
author: 'Manus AI'
description: 'Merges multiple theme files into a single, resolved theme based on a specified hierarchy, enabling multi-level theming.'
---

## 1. Overview

This workflow implements a multi-level, hierarchical theme system, a core concept from `SPEC-UI-001`. It takes a base theme and a series of override themes, then performs a deep merge to produce a single, resolved `theme.json` file. This is essential for enabling white-labeling, company-specific branding, and user personalization.

## 2. Category

`ui_theming_and_design`

## 3. Parameters

### Required Parameters

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `--base-theme` | string | Path to the base or system-level theme file (lowest precedence). |
| `--override-themes` | list | A JSON string representing an ordered list of paths to theme files that will override the base. The last theme in the list has the highest precedence. |
| `--output-file` | string | Path to save the final, merged theme file. |

## 4. Execution Logic

1.  **Load Base Theme:** The workflow first loads the JSON content from the `--base-theme` file.
2.  **Iterate and Merge:** It then iterates through the list of `--override-themes` in the order they are provided.
3.  **Deep Merge:** For each override theme, it performs a deep (recursive) merge on top of the result from the previous step. If a key exists in both themes, the value from the override theme is used.
4.  **Write Output:** The final, fully resolved JSON object is written to the `--output-file`.

## 5. Example Usage

### CLI

```bash
# Resolve themes for a specific user in a specific company
/smartspec_resolve_themes \
  --base-theme "src/config/themes/system.theme.json" \
  --override-themes '[\
    "src/config/themes/company-acme.theme.json", \
    "src/config/themes/user-123.theme.json" \
  ]' \
  --output-file ".spec/resolved-theme.json"
```

### Kilo Code

```kilo
// Resolve themes for a public-facing, white-labeled site
smartspec_resolve_themes(
  base_theme: "src/config/themes/system.theme.json",
  override_themes: [
    "src/config/themes/public-customer-xyz.theme.json"
  ],
  output_file: "public/theme.json"
)
```

## 6. Use Cases

-   **White-Labeling:** Create a unique brand experience for different customers by providing a company-specific theme file.
-   **User Personalization:** Allow users to have their own theme preferences (e.g., dark mode, high contrast, custom colors) by applying a user-specific theme on top.
-   **Feature-Specific Themes:** Apply special themes for certain sections of an application.

## 7. Related Workflows

-   `smartspec_manage_theme`: For creating and managing the individual theme files that are used as input for this workflow.
-   `smartspec_generate_ui_spec`: Generates UI that will be styled by the resolved theme.

## 8. Implementation

Implemented in: `.smartspec/scripts/resolve_themes.py`

## 9. Notes

-   The `--override-themes` parameter must be a valid JSON array of strings.
-   The merge logic is deep, meaning nested objects are merged recursively.
-   This workflow is critical for implementing the `Enhanced Theme System` described in `SPEC-UI-001`.
