# Knowledge Base: Choosing the Right UI JSON Format

## 1. Introduction: Not All UI JSON is the Same

SmartSpec provides powerful workflows for generating UI specifications from high-level prompts. However, it is crucial to understand that these workflows can produce **two distinct types of UI JSON**, each designed for a different purpose and a different rendering engine. A common point of confusion is the difference between the output of `/smartspec_generate_rjsf_schema` and `/smartspec_generate_ui_spec`.

This guide provides a clear comparison between the two formats, their intended use cases, and a decision-making framework to help you choose the correct workflow for your needs.

## 2. The Two Formats: RJSF vs. A2UI Spec

At a high level, the distinction is simple:

-   **RJSF Schema:** A format specifically for generating **forms** using the **React JSON Schema Form (RJSF)** library.
-   **A2UI Spec:** A general-purpose, declarative UI specification format for rendering **any UI structure** (not just forms) using a compatible **A2UI renderer**.

### Comparison Table

| Feature | `/smartspec_generate_rjsf_schema` | `/smartspec_generate_ui_spec` |
| :--- | :--- | :--- |
| **Primary Use Case** | Generating complex **forms** | Generating **any UI component or page** |
| **Output Files** | `schema.json` and `uiSchema.json` | A single `ui-spec.json` file |
| **Rendering Engine** | **React JSON Schema Form (RJSF)** [1] | Any **A2UI-compliant renderer** |
| **Scope** | Limited to form elements (inputs, validation, layout) | Can describe any UI element (layouts, cards, tables, etc.) |
| **Data Binding** | Implicitly bound to form data state | Explicitly bound to any API/state via `bindings` |
| **Governance** | Ungoverned artifact (quick prototyping) | Governed artifact (part of the official spec) |

## 3. Deep Dive: Understanding the Differences

### `/smartspec_generate_rjsf_schema`

This workflow is a **specialized tool for form generation**. It leverages the popular RJSF library to handle the complexities of form state management, validation, and rendering.

**When to use it:**
-   You need to build a complex form with validation quickly.
-   Your project already uses or can easily incorporate the RJSF library.
-   You are focused on the form itself, not its integration with a larger, declarative UI.

> **Warning:** The output of this workflow is **only compatible with an RJSF renderer**. Attempting to use these schemas with a generic A2UI renderer will fail, as the formats are completely different.

### `/smartspec_generate_ui_spec`

This is the **core workflow for A2UI development**. It produces a rich, declarative specification that can describe an entire application interface, from a single button to a complex dashboard.

**When to use it:**
-   You are building a UI that is more than just a form.
-   You need to bind UI elements to various data sources (APIs, application state).
-   You are following a full A2UI methodology where the UI spec is a governed, version-controlled artifact.
-   You have an A2UI-compliant renderer.

> **Warning:** The `ui-spec.json` produced by this workflow requires a **compatible A2UI renderer**. It is not a drop-in replacement for RJSF schemas and will not work with the RJSF library directly.

## 4. Decision Framework: Which Workflow Should I Use?

Use this simple decision tree to select the correct workflow:

1.  **Is my primary goal to build a form?**
    -   **Yes:** Proceed to question 2.
    -   **No, I am building a page, a component, or a full UI:** Use `/smartspec_generate_ui_spec`.

2.  **Am I using or planning to use the React JSON Schema Form (RJSF) library to render this form?**
    -   **Yes:** Use `/smartspec_generate_rjsf_schema`. This is the most direct path.
    -   **No, I am using a custom A2UI renderer:** Use `/smartspec_generate_ui_spec`. You can still describe a form in your prompt, but the output will be a standard A2UI spec that your renderer can understand.

### Rule of Thumb

-   If your prompt sounds like **"Create a form that..."** and you want a quick, standalone solution, think **RJSF**.
-   If your prompt sounds like **"Create a page that contains..."** and you need to bind elements to data, think **A2UI**.

## 5. Conclusion: The Right Tool for the Job

Both `/smartspec_generate_rjsf_schema` and `/smartspec_generate_ui_spec` are powerful tools, but they are not interchangeable. Understanding their distinct purposes and output formats is key to using SmartSpec effectively.

-   Use **`/smartspec_generate_rjsf_schema`** for rapid, RJSF-based form development.
-   Use **`/smartspec_generate_ui_spec`** for comprehensive, declarative, and data-bound UI generation within an A2UI architecture.

By choosing the right workflow, you can avoid compatibility issues and leverage the full power of SmartSpec to accelerate your UI development.

---

## References

[1] Mozilla. *React JSON Schema Form*. [https://rjsf-team.github.io/react-jsonschema-form/](https://rjsf-team.github.io/react-jsonschema-form/)
