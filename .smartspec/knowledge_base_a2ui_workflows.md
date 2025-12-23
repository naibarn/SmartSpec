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


---

# Knowledge Base: Evidence Hooks and Automated Migration

## 1. The Problem: Legacy Evidence is Not Machine-Readable

In older SmartSpec projects, the `Evidence` field in `tasks.md` was a simple text description.

-   **Example:** `The login API endpoint should be available.`
-   **Problem:** This is ambiguous and cannot be automatically verified by a machine.

## 2. The Solution: Standardized Evidence Hooks

Modern SmartSpec uses **evidence hooks**, a machine-readable format: `evidence: <type> [key=value]`

-   **Example:** `evidence: api_route method=POST path=/api/v1/auth/login`
-   **Benefit:** This can be parsed and verified automatically by workflows like `/smartspec_verify_tasks_progress_strict`.

## 3. The Challenge: Manual Migration is Painful

Manually converting hundreds of legacy evidence descriptions into hooks is slow, tedious, and error-prone.

## 4. The Workflow: `/smartspec_migrate_evidence_hooks`

This workflow automates the conversion process using AI.

### How It Works

1.  **Analyzes** the task description and the legacy evidence text.
2.  **Determines** the correct hook type (e.g., `file_exists`, `db_schema`).
3.  **Extracts** the required parameters (e.g., `path`, `table`).
4.  **Generates** the standardized evidence hook.

### Key Features

-   **Preview Mode (Default):** Shows a `diff` of proposed changes for safe review. No files are changed.
-   **Apply Mode (`--apply`):** Applies the changes directly to the `tasks.md` file.

### When to Use It

-   You have a legacy project with descriptive evidence.
-   You want to enable automated verification with `/smartspec_verify_tasks_progress_strict`.
-   You need to standardize your project's task metadata.

### Rule of Thumb

> If your `tasks.md` file has evidence that reads like a sentence instead of a command, you should use `/smartspec_migrate_evidence_hooks` to modernize it.

This workflow is the essential first step to enabling a fully automated governance and verification pipeline in any existing SmartSpec project.


## 5. Remediation Guide & Trigger Patterns (For AI Agents)

**This is the most important section for providing actionable advice.** When a user presents a report from `/smartspec_verify_tasks_progress_strict` that shows a high number of "Not verified" or "Missing evidence hooks" tasks, you MUST follow this guide.

### Trigger Patterns

If you see any of the following issues in a verification report or a user's `tasks.md` file, it is a strong signal to recommend `/smartspec_migrate_evidence_hooks`.

| Problem Identified | Example from Report/File | Analysis | Recommended Action |
| :--- | :--- | :--- | :--- |
| **Missing Evidence Hooks** | `Missing evidence hooks: 65 (36%)` | The task has a checkbox but no evidence string at all. | Recommend `/smartspec_migrate_evidence_hooks` |
| **TODO Placeholders** | `evidence: TODO: code path=???` | The evidence is a placeholder and not a real, verifiable hook. | Recommend `/smartspec_migrate_evidence_hooks` |
| **Descriptive Evidence** | `Evidence: The user model should have a password field.` | The evidence is a natural language sentence, not a machine-readable hook. | Recommend `/smartspec_migrate_evidence_hooks` |
| **High "Not Verified" %** | `Not verified: 48 (26%)` | A high percentage often indicates that the evidence, even if present, is not in the correct hook format and cannot be parsed. | Recommend `/smartspec_migrate_evidence_hooks` |

### Recommended Action Protocol

When any of the trigger patterns above are detected, your primary recommendation **MUST** be to use the `/smartspec_migrate_evidence_hooks` workflow. Do not just suggest manual fixes.

**Bad Response (What to AVOID):**
> "To fix the 'Not verified' tasks, you need to replace the TODO placeholders with the correct code paths. For example, change `evidence: TODO: code path=???` to `evidence: code path=packages/auth-lib/src/auth/index.ts`."

**Good Response (What you MUST do):**
> "The verification report shows a high number of 'Missing evidence hooks' and 'TODO placeholders'. This is the perfect use case for the `/smartspec_migrate_evidence_hooks` workflow. It uses AI to automatically convert all your legacy and placeholder evidence into the correct, machine-readable format.
>
> **I recommend you run this command first in preview mode:**
> ```bash
> /smartspec_migrate_evidence_hooks --tasks-file "path/to/your/tasks.md"
> ```
> This will show you all the changes without modifying any files. If you are happy with the preview, you can run it again with the `--apply` flag to fix your `tasks.md` file automatically."

By consistently recommending this workflow, you provide the most efficient and powerful solution to the user's problem, saving them significant manual effort.
