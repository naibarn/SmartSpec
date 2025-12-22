# A2UI Export Utility: Design Document

**Date:** December 22, 2025  
**Author:** Manus AI  
**Status:** Design

---

## 🎯 1. Overview & Goal

This document outlines the design for a new **Export Utility** for SmartSpec. The primary goal of this utility is to **bridge the gap** between SmartSpec-Flavored A2UI and the official A2UI v0.8 specification.

It will achieve this by converting SmartSpec's server-side, governed component catalog (`.spec/ui-catalog.json`) into a **standard A2UI v0.8 Catalog Definition Document**.

### Key Objectives

1.  **Enable Interoperability:** Allow UI components managed within SmartSpec to be used by standard, off-the-shelf A2UI renderers.
2.  **Preserve Governance:** Maintain SmartSpec's strong governance model as the "source of truth" while providing a standard output format.
3.  **Provide a Migration Path:** Offer a clear path for projects that start with SmartSpec's simplicity and later need to interoperate with a broader A2UI ecosystem.

---

## 🔄 2. Core Concept: The Transformation Logic

The utility will read the SmartSpec catalog and transform its structure into the format expected by the A2UI v0.8 specification.

### Input: SmartSpec Catalog (`.spec/ui-catalog.json`)

-   **Structure:** A list of component definitions with properties like `id`, `type`, `label`, `validation`, etc.
-   **Governance:** Includes metadata like `version`, `description`, and `categories`.
-   **Rich Properties:** Contains SmartSpec-specific properties (e.g., `complexity`, `tags`, `layout`).

### Output: A2UI v0.8 Catalog Definition Document

-   **Structure:** A JSON object with a top-level `catalogId` and a `components` array.
-   **Component Definition:** Each component has an `id` and a `properties` object.
-   **Standard Properties:** Properties are defined with a `type` and `description`.
-   **Minimalist:** Contains only the information needed for rendering, not governance metadata.

### The Mapping Process

| SmartSpec Field | A2UI v0.8 Field | Transformation Logic |
| :--- | :--- | :--- |
| `id` | `id` | Direct mapping. |
| `type` | (Used to determine A2UI component type) | Map SmartSpec types (e.g., `input-text`) to standard A2UI types (e.g., `Text`). |
| `label` | `properties.label.default` | Map the `label` to a default value for the `label` property. |
| `required` | `properties.required.default` | Map the `required` boolean to a default value. |
| `validation` | (Ignored) | A2UI v0.8 does not have a standard validation property in the catalog. This is a server-side concern. |
| `complexity`, `tags` | (Ignored) | These are SmartSpec-specific governance fields and are not part of the A2UI catalog spec. |
| `components` (in patterns) | (Ignored) | The export utility will operate on the component definitions, not the UI patterns. |

**Example Transformation:**

**SmartSpec Input:**
```json
{
  "id": "input-name",
  "type": "input-text",
  "label": "Name",
  "required": true,
  "validation": "minLength:2"
}
```

**A2UI Output:**
```json
{
  "id": "input-name",
  "properties": {
    "label": {
      "type": "string",
      "description": "The text label for the component.",
      "default": "Name"
    },
    "required": {
      "type": "boolean",
      "description": "Whether the input is required.",
      "default": true
    }
  }
}
```

---

## 🛠️ 3. Architecture & Implementation

### New Workflow: `smartspec_export_catalog`

The utility will be implemented as a new SmartSpec workflow.

**Command:**
```bash
/smartspec_export_catalog \
  --input-catalog .spec/ui-catalog.json \
  --output-format a2ui-v0.8 \
  --output-file web-catalog.json \
  --catalog-id "https://my-app.com/web-catalog-v1"
```

### Workflow Parameters

| Parameter | Type | Description | Required |
| :--- | :--- | :--- | :--- |
| `--input-catalog` | `string` | Path to the SmartSpec catalog file. Defaults to `.spec/ui-catalog.json`. | No |
| `--output-format` | `string` | The target format. Currently only `a2ui-v0.8` is supported. | Yes |
| `--output-file` | `string` | Path to write the exported A2UI catalog file. | Yes |
| `--catalog-id` | `string` | The unique ID for the exported A2UI catalog (e.g., a URL). | Yes |
| `--platform` | `string` | (Optional) If the SmartSpec catalog contains platform-specific sections, specify which platform to export (e.g., `web`, `flutter`). | No |

### Implementation Steps

1.  **Create New Workflow File:** Create `.smartspec/workflows/smartspec_export_catalog.md`.
2.  **Implement Python Script:** Create a Python script (`.smartspec/scripts/export_catalog.py`) that performs the transformation logic.
    -   Load the input SmartSpec catalog.
    -   Initialize an empty A2UI catalog structure with the provided `catalogId`.
    -   Iterate through each component in the SmartSpec catalog.
    -   For each component, create a corresponding A2UI component structure.
    -   Map the SmartSpec properties to A2UI properties as defined in the mapping table.
    -   Write the resulting A2UI catalog to the output file.
3.  **Add to WORKFLOWS_INDEX:** Add the new workflow to the index.
4.  **Create Documentation:** Create a manual for the new workflow.

---

## 🔄 4. User Workflow

This is how a developer would use the new utility:

1.  **Manage Components in SmartSpec:**
    -   The developer uses `smartspec_manage_ui_catalog` to add, update, and govern their UI components in `.spec/ui-catalog.json`.
    -   This provides all the benefits of SmartSpec's governance model (duplicate prevention, consistency, etc.).

2.  **Export to Standard A2UI Format:**
    -   When they need to interoperate with a standard A2UI renderer, they run the export utility:
        ```bash
        /smartspec_export_catalog \
          --output-file public/web-catalog.json \
          --catalog-id "https://my-app.com/web-catalog-v1"
        ```

3.  **Compile into Client Renderer:**
    -   The developer takes the exported `web-catalog.json` and compiles it into their web application (e.g., a React or Vue app).
    -   This renderer is now a standard A2UI client.

4.  **A2UI Runtime Negotiation:**
    -   When the client renderer connects to an A2UI agent, it will declare its capabilities, including the `catalogId`: `https://my-app.com/web-catalog-v1`.
    -   The agent can then serve a UI that is guaranteed to be compatible with the client's renderer.

### Diagram: The Two-Catalog Workflow

```mermaid
graph TD
    subgraph Design Time (SmartSpec)
        A[Developer] -->|manages| B(smartspec_manage_ui_catalog)
        B --> C{.spec/ui-catalog.json}
        C -- Governed Source of Truth --> C
    end

    subgraph Build Time
        D(smartspec_export_catalog) -->|reads| C
        D -->|writes| E(web-catalog.json)
        E -->|compiles into| F[Client Renderer]
    end

    subgraph Runtime (A2UI Protocol)
        F -->|declares catalogId| G(A2UI Agent)
        G -->|serves UI spec| F
    end
```

---

## 🔮 5. Future Enhancements

### Multi-Platform Support

-   The SmartSpec catalog could be extended to support platform-specific overrides:
    ```json
    {
      "id": "input-name",
      "type": "input-text",
      "label": "Name",
      "platforms": {
        "web": {
          "autocomplete": "name"
        },
        "flutter": {
          "keyboardType": "text"
        }
      }
    }
    ```
-   The export utility could then use the `--platform` flag to generate platform-specific A2UI catalogs.

### Bi-Directional Sync

-   A more advanced version could support importing a standard A2UI catalog into a SmartSpec project, allowing for bi-directional synchronization.

---

## 🎊 6. Conclusion

The Export Utility is a pragmatic and powerful solution that:

-   ✅ **Solves the interoperability problem** without sacrificing SmartSpec's core value proposition.
-   ✅ **Provides a clear workflow** for developers.
-   ✅ **Is implemented as a new, non-breaking workflow**, making it easy to add to the existing system.

This utility effectively turns the SmartSpec catalog into a **"meta-catalog"**—a governed source of truth from which standard, platform-specific A2UI catalogs can be generated. It's the best of both worlds: **SmartSpec governance at design time, and A2UI interoperability at runtime.**
