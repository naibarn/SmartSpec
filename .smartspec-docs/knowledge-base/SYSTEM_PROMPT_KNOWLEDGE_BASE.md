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
# Knowledge Base: AI-Powered Form Generation with RJSF

## 1. The Challenge of Dynamic Forms

Modern web applications often require complex, dynamic forms for tasks like user registration, settings configuration, or data entry. Building these forms manually is a time-consuming and error-prone process. Developers must handle:

-   **Data Structure:** Defining the shape of the form data.
-   **Validation:** Implementing rules (e.g., required fields, email format, password strength).
-   **UI Layout:** Arranging fields, choosing widgets (e.g., text input, dropdown, checkbox), and managing layout.
-   **State Management:** Handling form state, updates, and submissions.

**React JSON Schema Form (RJSF)** [1] is a powerful library that simplifies this by generating forms from a JSON Schema. However, writing these JSON schemas manually can still be a complex and verbose task.

## 2. The SmartSpec Solution: `/smartspec_generate_rjsf_schema`

> **Important:** This workflow is a specialized tool for generating form schemas for the **React JSON Schema Form (RJSF)** library. It does not produce a general-purpose A2UI specification. For a detailed comparison, please read the [UI JSON Formats Comparison Guide](ui-json-formats-comparison.md).

SmartSpec introduces the `/smartspec_generate_rjsf_schema` workflow to completely automate the creation of RJSF-compatible schemas from a single, high-level command. This workflow bridges the gap between a natural language requirement and a fully functional, production-ready form.

> By leveraging AI, this workflow allows developers to describe a form in plain English and receive the `schema.json` and `uiSchema.json` files needed to render it instantly.

### Key Capabilities

-   **Natural Language to Schema:** Translates prompts like "Create a login form with email and password" into a valid JSON Schema.
-   **Intelligent Validation:** Automatically infers and applies common validation rules (e.g., `format: "email"`, `minLength`).
-   **UI Widget Selection:** Understands UI hints in the prompt (e.g., "use a textarea for the bio") and generates the corresponding `uiSchema.json`.
-   **Field Ordering:** Respects ordering instructions provided in the prompt.
-   **Rapid Prototyping:** Enables developers to generate and test complex forms in seconds, not hours.

## 3. How It Works: The AI-Powered Pipeline

The workflow follows a sophisticated, multi-step process to ensure high-quality output:

1.  **Prompt Analysis:** An AI model first analyzes the user's `--prompt` to identify all form fields, their data types, validation requirements, and any UI-specific instructions.
2.  **Schema Generation:** Based on the analysis, the model generates the `schema.json` file. This file defines the data structure, properties, and validation constraints according to the JSON Schema standard [2].
3.  **UI Schema Generation:** The model then generates the `uiSchema.json` file. This file controls the look and feel of the form, specifying widget types, field order, and other presentation-level details.
4.  **Validation:** Both generated files are validated to ensure they are syntactically correct and conform to the RJSF specification.
5.  **File Output:** The validated `schema.json` and `uiSchema.json` are saved to the specified `--output-dir`.

### Example Breakdown

Consider the command:

```bash
/smartspec_generate_rjsf_schema \
  --prompt "Create a user registration form. Need an email field (must be valid email), a password field with minimum 8 characters, and an optional checkbox to subscribe to newsletter." \
  --output-dir "src/config/forms/registration/"
```

**The AI will infer:**
-   Three fields: `email`, `password`, `subscribe_newsletter`.
-   `email` should have `"type": "string"` and `"format": "email"`.
-   `password` should have `"type": "string"` and `"minLength": 8`.
-   `subscribe_newsletter` should have `"type": "boolean"`.
-   `email` and `password` are required fields, while `subscribe_newsletter` is not.

This results in a robust, validated form configuration without the developer needing to write a single line of JSON.

## 4. Scope and Limitations

It is critical to understand that `/smartspec_generate_rjsf_schema` is a **specialized tool**, not a general-purpose UI generator.

-   **Renderer-Specific:** The output is only compatible with the RJSF library or a renderer that explicitly supports its `schema` and `uiSchema` format.
-   **Form-Centric:** The workflow is designed exclusively for generating forms. It cannot be used to create other UI elements like cards, tables, or page layouts.
-   **No Data Binding:** The generated schemas do not contain data binding information. Data handling must be managed by the application code that uses the RJSF component.

## 5. Use Cases and Best Practices

### Ideal Use Cases

-   **Rapid Prototyping:** Quickly create functional forms to test user flows and gather feedback.
-   **Dynamic Configuration:** Generate forms on-the-fly based on user roles or application state.
-   **Onboarding and Registration:** Standardize and accelerate the creation of user sign-up and profile forms.
-   **Settings Panels:** Easily build complex settings pages with various input types.

### Best Practices

-   **Be Specific in Your Prompts:** The more detail you provide, the better the output. Include information about validation, widget preferences, and field order.
-   **Iterate and Refine:** Start with a simple prompt and progressively add more detail. Use the generated schemas as a base and refine them manually for highly complex or custom logic.
-   **Integrate into Larger Workflows:** Combine this workflow with others. For example, use `/smartspec_generate_ui_spec` to create a page that *uses* the form generated by this workflow.

---

## References

[1] Mozilla. *React JSON Schema Form*. [https://rjsf-team.github.io/react-jsonschema-form/](https://rjsf-team.github.io/react-jsonschema-form/)

[2] JSON Schema. *JSON Schema Specification*. [https://json-schema.org/](https://json-schema.org/)
# Knowledge Base: Integrating SPEC-UI-001 Workflows

## 1. Introduction: A Unified Architecture

The three new workflows—`/smartspec_generate_rjsf_schema`, `/smartspec_resolve_themes`, and `/smartspec_generate_component_registry`—are not just standalone tools. They are designed to work together as a cohesive system to fully realize the vision of a JSON-driven UI architecture as laid out in `SPEC-UI-001`. This guide demonstrates how these workflows can be integrated to create a powerful, automated, and scalable UI development pipeline.

## 2. Prerequisite: The A2UI Renderer

This entire architecture relies on a central component: the **A2UI Renderer**. This is a custom component in your application that is responsible for taking an A2UI `ui-spec.json` and rendering the corresponding UI. The renderer must be able to:

1.  **Parse the A2UI JSON:** Recursively traverse the JSON tree.
2.  **Map Components:** Use the `component-registry.ts` to map a `type` string (e.g., `"card"`) to its actual React component.
3.  **Apply Properties:** Pass the properties from the JSON (e.g., `title`, `children`) to the React component as props.
4.  **Handle Bindings:** Resolve data bindings to connect the UI to application state and API data.
5.  **Apply Themes:** Use the resolved theme to style the components.

> **Crucial:** The workflows described here generate the *specifications*, but you must have a renderer capable of interpreting them. This is a one-time investment that enables the entire JSON-driven UI paradigm.

## 3. The End-to-End Development Lifecycle

Here is a practical, step-by-step look at how these workflows fit into the development lifecycle of a new feature that includes a dynamic form.

### Step 1: Ensure the Component Registry is Up-to-Date

Before any development begins, and continuously throughout the project, the component registry must be kept in sync with the component library. This is a foundational step that should be automated.

**Workflow:** `/smartspec_generate_component_registry`

**Integration:** Run this command as a **pre-commit hook**.

```bash
# In your .husky/pre-commit file
/smartspec_generate_component_registry \
  --scan-dir "src/components/" \
  --output-file "src/config/component-registry.ts"
```

**Outcome:** The `component-registry.ts` is always up-to-date. The UI renderer will always know about every available component, preventing a common class of runtime errors.

### Step 2: Generate the Dynamic Form

A new feature requires a complex user settings form. Instead of writing the JSON schema by hand, the developer uses a natural language prompt.

**Workflow:** `/smartspec_generate_rjsf_schema`

**Integration:** A developer runs this command as a one-off task during feature development.

```bash
/smartspec_generate_rjsf_schema \
  --prompt "Create a user profile form with an editable bio (textarea), a read-only email, and a dropdown for language preference (English, Spanish, French)." \
  --output-dir "src/config/forms/user-profile/"
```

**Outcome:** The `schema.json` and `uiSchema.json` files are instantly created. The developer can now use a generic RJSF renderer component and pass these schemas to it, rendering a fully functional form in minutes.

### Step 3: Generate the UI Specification for the Page

The form needs to be placed within a larger page layout. The developer uses `/smartspec_generate_ui_spec` to create the A2UI JSON for the entire page.

**Workflow:** `/smartspec_generate_ui_spec`

**Integration:** A developer runs this command to create the page structure.

```bash
/smartspec_generate_ui_spec \
  --prompt "Create a two-column page. The left column has the user's avatar and name. The right column has a card with the title 'Profile Settings' and contains the user profile form." \
  --output-file ".spec/ui/user-settings-page.json"
```

**Outcome:** An A2UI JSON file is generated that describes the entire page layout, including a reference to the form generated in the previous step.

### Step 4: Resolve the Theme for the User Session

When a user logs in, the application needs to determine the correct theme to apply. This involves merging the system, company, and user-specific themes.

**Workflow:** `/smartspec_resolve_themes`

**Integration:** This workflow is called **dynamically by the application server** at the beginning of a user session.

```javascript
// Example server-side logic (e.g., in an Express.js middleware)

async function resolveUserTheme(user, company) {
  const command = `
    /smartspec_resolve_themes \
      --base-theme "./config/themes/system.json" \
      --override-themes '[ "./config/themes/company-${company.id}.json", "./config/themes/user-${user.id}.json" ]' \
      --output-file "./public/resolved-themes/session-${user.sessionId}.json"
  `;
  // Execute the command
  await exec(command);
  return `public/resolved-themes/session-${user.sessionId}.json`;
}
```

**Outcome:** A unique, fully resolved theme file is generated for the user's session. The path to this file is then passed to the frontend, which provides it to the A2UI renderer.

## 4. The Big Picture: A Fully Automated Flow

When combined, these workflows create a powerful and elegant system:

1.  The **Component Registry** is always in sync, thanks to automation.
2.  Developers can create complex, validated **Forms** in seconds using natural language.
3.  The overall **Page Layout** is also generated from high-level prompts.
4.  The entire UI is styled by a **Resolved Theme** that is dynamically generated for each user, enabling deep customization and white-labeling.

This integrated approach dramatically reduces boilerplate, eliminates common errors, and allows developers to build complex, customizable UIs at an unprecedented speed. It is the practical realization of the `SPEC-UI-001` architecture, powered by SmartSpec.
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
# Knowledge Base: Automated Component Registry

## 1. The Component Mapping Problem

In a JSON-driven UI architecture, such as the one described in `SPEC-UI-001`, the A2UI JSON payload contains declarative instructions on what to render. For example, a piece of JSON might say: `{"type": "card", "title": "Welcome"}`.

The UI renderer's job is to take this instruction and render the actual `Card` component from your component library. This requires a mapping mechanism—a way to connect the string `"card"` to the `Card` component implementation in your codebase. This mapping is handled by a **component registry**.

Manually maintaining this registry is a significant pain point in large-scale projects:

-   **Error-Prone:** Developers frequently forget to register new components, leading to runtime errors where the renderer doesn't know what to do with a given `type`.
-   **Tedious:** It's a repetitive, boilerplate task that adds friction to the development process.
-   **Synchronization Issues:** The registry can easily get out of sync with the actual component library, especially when components are renamed or deleted.

## 2. The SmartSpec Solution: `/smartspec_generate_component_registry`

The `/smartspec_generate_component_registry` workflow completely eliminates this manual step. It automates the creation and maintenance of the component registry file, ensuring it is always a perfect reflection of your component library.

> This workflow scans your component directories, identifies all exported components, and generates a registry file that maps component names to their implementations. It turns a tedious manual task into a reliable, automated process.

### How It Works

The workflow is designed to be simple to use but powerful in its execution:

1.  **Scan Directory:** It recursively scans the specified `--scan-dir` for all component files (e.g., `.tsx`, `.jsx`).
2.  **Parse Exports:** Using regular expressions, it parses the content of each file to identify all named exports. It is optimized for common patterns like `export const MyComponent = ...` and `export { MyComponent }`.
3.  **Generate Imports:** For each discovered component, it generates a corresponding import statement at the top of the output file.
4.  **Create Mapper:** It then creates a `ComponentMapper` object (or a simple JavaScript object) that maps the component's string name to its imported class or function.
5.  **Write File:** The complete registry, including all imports and the mapper object, is written to the specified `--output-file`.

### Example

Given a directory `src/components/` containing `Card.tsx` and `Button.tsx`, the command:

```bash
/smartspec_generate_component_registry \
  --scan-dir "src/components/" \
  --output-file "src/config/component-registry.ts"
```

Will generate a `component-registry.ts` file that looks something like this:

```typescript
// This file is auto-generated by SmartSpec. Do not edit manually.

import { Card } from '../components/Card';
import { Button } from '../components/Button';

export const ComponentMapper = {
  'Card': Card,
  'Button': Button,
};
```

This file can then be directly imported and used by your UI renderer.

## 3. Integrating with Your Development Workflow

To maximize the benefits of this workflow, it should be integrated directly into your development and CI/CD processes.

### Pre-Commit Hook

One of the most effective ways to use this workflow is to run it as a **pre-commit hook**. This ensures that the component registry is automatically updated every time a developer commits code. If a new component has been added, it will be registered before the code even reaches the remote repository.

Most modern projects use tools like **Husky** [1] to manage Git hooks. You can configure Husky to run the `generate_component_registry` command before each commit.

### CI/CD Pipeline

As an additional layer of safety, you can also add this workflow as a step in your Continuous Integration (CI) pipeline. This guarantees that the registry is always up-to-date in your production builds, even if a developer somehow bypasses the pre-commit hook.

## 4. Advanced Usage and Best Practices

### Base Registry

The workflow supports a `--base-registry` parameter, which allows you to include components from an external library (e.g., Material-UI, Ant Design) without needing to scan them. You can provide a JSON file that maps component names to their import sources, and the workflow will merge these with your locally scanned components.

### Best Practices

-   **Use Named Exports:** The workflow is optimized for named exports. Avoid default exports for components that you want to be automatically registered.
-   **Consistent Naming:** Ensure your component filenames and exported component names are consistent (e.g., `Card.tsx` exports a component named `Card`).
-   **Run It Automatically:** The real power of this workflow is unlocked when it is run automatically. Set it up in a pre-commit hook or CI pipeline to make it a seamless part of your development process.

By automating the component registry, you remove a significant source of friction and potential errors from your JSON-driven UI architecture, allowing your team to focus on what they do best: building great components.

---

## References

[1] Typicode. *Husky*. [https://typicode.github.io/husky/](https://typicode.github.io/husky/)
