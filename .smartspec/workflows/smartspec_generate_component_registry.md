---
title: 'SmartSpec Generate Component Registry'
workflow_id: 'smartspec_generate_component_registry'
version: '1.0.0'
author: 'Manus AI'
description: 'Scans the component library and automatically generates the component registry file for a JSON-driven UI renderer.'
---

## 1. Overview

This workflow automates the creation and maintenance of the `component-registry.ts` file. This file is critical for a JSON-driven UI system, as it maps component keys (e.g., `"type": "card"`) in an A2UI JSON to their actual React component implementations. By automating this process, it eliminates a common source of human error where developers forget to register new components, leading to runtime failures.

## 2. Category

`project_management_and_support`

## 3. Parameters

### Required Parameters

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `--scan-dir` | string | The directory containing the React components to be registered (e.g., `src/components/custom/`). |
| `--output-file` | string | The path to the output `component-registry.ts` file. |

### Optional Parameters

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `--base-registry` | string | `null` | Optional path to a JSON file defining a base set of components to include (e.g., from a library like MUI). The keys are component names and values are import sources. |
| `--wildcard-export-files` | list | `["index.ts", "index.tsx"]` | A JSON array of filenames that are assumed to use wildcard exports (`export * from './component'`). The script will look inside the referenced files. |

## 4. Execution Logic

1.  **Initialize Registry:** The script starts with an empty registry or loads the one from `--base-registry` if provided.
2.  **Scan Directory:** It recursively scans the `--scan-dir` for component files (`.ts`, `.tsx`).
3.  **Parse Exports:** For each file, it uses regular expressions to identify named exports (e.g., `export const MyComponent = ...` or `export { MyComponent }`).
4.  **Handle Wildcards:** If it encounters a file listed in `--wildcard-export-files`, it reads the file to find the source of the wildcard exports and analyzes those files instead.
5.  **Generate Registry:** It constructs a TypeScript file that:
    *   Imports all discovered components.
    *   Creates a `ComponentMapper` object that maps the component's name (string) to its imported class/function.
6.  **Write Output:** The generated content is written to the `--output-file`.

## 5. Example Usage

### CLI

```bash
# Generate the component registry for a project
/smartspec_generate_component_registry \
  --scan-dir "src/components/business/" \
  --output-file "src/config/component-registry.ts" \
  --base-registry "src/config/base-components.json"
```

### Kilo Code

```kilo
// Update the component registry after adding new components
smartspec_generate_component_registry(
  scan_dir: "src/components/business/",
  output_file: "src/config/component-registry.ts"
)
```

## 6. Use Cases

-   **CI/CD Integration:** Run this workflow in a pre-commit hook or CI pipeline to ensure the registry is always up-to-date.
-   **Developer Productivity:** Frees developers from the manual, repetitive task of registering components.
-   **Project Scaffolding:** Use it once during project setup to generate the initial registry.

## 7. Related Workflows

-   `smartspec_generate_ui_spec`: Generates A2UI JSON that consumes the component registry.

## 8. Implementation

Implemented in: `.smartspec/scripts/generate_component_registry.py`

## 9. Notes

-   The script relies on regex and may not cover all possible TypeScript export syntaxes. It is designed to cover the most common patterns.
-   Default exports are currently ignored, as named exports are a more explicit and maintainable pattern for a component library.
