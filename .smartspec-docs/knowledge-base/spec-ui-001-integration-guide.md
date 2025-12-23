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
