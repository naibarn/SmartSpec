# Workflow: /smartspec_generate_component_registry

**Scans the component library and automatically generates the component registry file for a JSON-driven UI renderer.**

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

## 4. Example Usage

### Generate the Initial Registry

**Command:**
```bash
/smartspec_generate_component_registry \
  --scan-dir "src/components/business/" \
  --output-file "src/config/component-registry.ts" \
  --base-registry "src/config/base-components.json"
```

**Result:**
- The script scans all `.tsx` files in `src/components/business/`, finds all named exports, and generates a `component-registry.ts` file. This file will contain import statements for all discovered components and a `ComponentMapper` object that maps their string names to the component implementations. It will also include the components defined in `base-components.json`.

---

### Run in a CI/CD Pipeline

**Command:**
```bash
# This command can be added to a pre-commit hook or a CI job
/smartspec_generate_component_registry \
  --scan-dir "src/components/" \
  --output-file "src/config/component-registry.ts"
```

**Result:**
- Ensures that the component registry is always kept in sync with the component library, preventing runtime errors from unregistered components.

## 5. Notes

- This workflow is designed to be run frequently, especially in a CI/CD environment.
- The script uses regular expressions to parse exports and may not cover every possible edge case in TypeScript syntax. It is optimized for common patterns like `export const MyComponent = ...` and `export { MyComponent }`.
- Default exports are currently ignored. It is recommended to use named exports for all components in your library for consistency.
