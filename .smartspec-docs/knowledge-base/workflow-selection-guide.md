# Knowledge Base: Workflow Selection Guide

## 1. Introduction

SmartSpec offers a powerful suite of workflows. This guide provides a clear decision-making framework to help you select the most appropriate workflow for your specific task, ensuring you get the right output for your needs.

## 2. The Core Question: What is Your Goal?

The first and most important question to ask is: **What is your primary goal?**

-   **A. Generating a new UI from a prompt?**
-   **B. Modernizing a legacy `tasks.md` file with old evidence formats?**

Your answer to this question is the primary driver for your workflow choice.

## 3. The Decision Tree

Use this visual decision tree to navigate your choice. Start at the top and answer the questions to arrive at the recommended workflow.

```mermaid
graph TD
    A[Start: What is your goal?] --> B{Generating UI?};
    B -->|Yes| C{A standalone form?};
    B -->|No, modernizing tasks.md| H[/smartspec_migrate_evidence_hooks];

    C -->|Yes| E{Are you using the RJSF library?};
    C -->|No, a full page/component| F[/smartspec_generate_ui_spec];

    E -->|Yes| G[/smartspec_generate_rjsf_schema];
    E -->|No, I have a custom A2UI renderer| F;

    subgraph Legend
        I[Decision Point]
        J[Recommended Workflow]
    end

    style I fill:#f9f,stroke:#333,stroke-width:2px
    style J fill:#bbf,stroke:#333,stroke-width:2px
```

### How to Read the Decision Tree

1.  **Start:** Begin by defining your goal. Are you generating a new UI, or are you working with an existing `tasks.md` file?
2.  **Generating UI?:** If your goal is to generate a UI, follow the "Yes" path. If your goal is to update a `tasks.md` file that has old, descriptive evidence, your clear choice is `/smartspec_migrate_evidence_hooks`.
3.  **Standalone Form?:** If you are generating UI, the next question is whether you are building just a form. If so, proceed to the next decision. Otherwise, use `/smartspec_generate_ui_spec`.
4.  **Using RJSF?:** If you are building a form, the final question is about your rendering engine. For the **RJSF library**, use `/smartspec_generate_rjsf_schema`. For a **custom A2UI renderer**, use `/smartspec_generate_ui_spec`.

## 4. Rule of Thumb: A Quick Guide

For a faster decision, use this simple rule of thumb:

| If your goal is to... | And your context is... | Then use... |
| :--- | :--- | :--- |
| Build a **form** | Using **React JSON Schema Form (RJSF)** | `/smartspec_generate_rjsf_schema` |
| Build a **form** | Using a **custom A2UI renderer** | `/smartspec_generate_ui_spec` |
| Build **anything else** (page, component) | Using a **custom A2UI renderer** | `/smartspec_generate_ui_spec` |
| Modernize **`tasks.md`** | Legacy evidence needs converting | `/smartspec_migrate_evidence_hooks` |

> In short: For UI generation, unless you are specifically targeting the RJSF library, your default choice should be **`/smartspec_generate_ui_spec`**. For `tasks.md` maintenance, use **`/smartspec_migrate_evidence_hooks`**.

## 5. Summary of Outputs

Remember that each workflow serves a distinct purpose and produces a different output.

-   **`/smartspec_generate_rjsf_schema`**
    -   **Output:** `schema.json` + `uiSchema.json`
    -   **For:** RJSF Renderer

-   **`/smartspec_generate_ui_spec`**
    -   **Output:** `ui-spec.json`
    -   **For:** A2UI Renderer

-   **`/smartspec_migrate_evidence_hooks`**
    -   **Output:** An updated `tasks.md` file
    -   **For:** Enabling automated task verification

Choosing the correct workflow from the start will prevent compatibility issues and ensure a smooth development process. When in doubt, refer to this guide and the [UI JSON Formats Comparison](ui-json-formats-comparison.md) guide.
