# Knowledge Base: Workflow Selection Guide

## 1. Introduction

SmartSpec offers a powerful suite of workflows for UI generation. This guide provides a clear decision-making framework to help you select the most appropriate workflow for your specific task, ensuring you get the right output for your needs.

## 2. The Core Question: What Are You Building?

The first and most important question to ask is: **What is the primary purpose of the UI I am trying to create?**

-   **A. A standalone, complex form?**
-   **B. A component, page, or entire UI that needs to be data-bound?**

Your answer to this question is the primary driver for your workflow choice.

## 3. The Decision Tree

Use this visual decision tree to navigate your choice. Start at the top and answer the questions to arrive at the recommended workflow.

```mermaid
graph TD
    A[Start: What are you building?] --> B{A standalone form?};
    B -->|Yes| C{Are you using the RJSF library?};
    B -->|No, a full page/component| D[/smartspec_generate_ui_spec];

    C -->|Yes| E[/smartspec_generate_rjsf_schema];
    C -->|No, I have a custom A2UI renderer| D;

    subgraph Legend
        F[Decision Point]
        G[Recommended Workflow]
    end

    style F fill:#f9f,stroke:#333,stroke-width:2px
    style G fill:#bbf,stroke:#333,stroke-width:2px
```

### How to Read the Decision Tree

1.  **Start:** Begin by defining your goal.
2.  **Standalone Form?:** If your goal is simply to create a form (e.g., for a contact page, a settings panel), follow the "Yes" path. If you are building anything else (a dashboard, a card, a layout), follow the "No" path directly to `/smartspec_generate_ui_spec`.
3.  **Using RJSF?:** If you are building a form, the next critical question is about your rendering engine. If you are using the popular **React JSON Schema Form (RJSF)** library, the clear choice is `/smartspec_generate_rjsf_schema`. If you are using a custom A2UI renderer, you should still use `/smartspec_generate_ui_spec` and describe the form in the prompt.

## 4. Rule of Thumb: A Quick Guide

For a faster decision, use this simple rule of thumb:

| If your goal is to... | And your renderer is... | Then use... |
| :--- | :--- | :--- |
| Build a **form** | **React JSON Schema Form (RJSF)** | `/smartspec_generate_rjsf_schema` |
| Build a **form** | A **custom A2UI renderer** | `/smartspec_generate_ui_spec` |
| Build **anything else** (page, component, layout) | A **custom A2UI renderer** | `/smartspec_generate_ui_spec` |

> In short: Unless you are specifically targeting the RJSF library, your default choice should always be **`/smartspec_generate_ui_spec`**.

## 5. Summary of Outputs

Remember that each workflow produces a different output for a different renderer.

-   **`/smartspec_generate_rjsf_schema`**
    -   **Output:** `schema.json` + `uiSchema.json`
    -   **For:** RJSF Renderer

-   **`/smartspec_generate_ui_spec`**
    -   **Output:** `ui-spec.json`
    -   **For:** A2UI Renderer

Choosing the correct workflow from the start will prevent compatibility issues and ensure a smooth development process. When in doubt, refer to this guide and the [UI JSON Formats Comparison](ui-json-formats-comparison.md) guide.
