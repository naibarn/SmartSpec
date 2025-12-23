---
title: 'SmartSpec Generate RJSF Schema'
workflow_id: 'smartspec_generate_rjsf_schema'
version: '1.0.0'
author: 'Manus AI'
description: 'Generates JSON Schema and UI Schema for React JSON Schema Form (RJSF) from a natural language prompt.'
---

## 1. Overview

This workflow automates the creation of complex form configurations for **React JSON Schema Form (RJSF)**. It takes a high-level, natural language description of a form and generates the two critical files required by RJSF: the data schema (`schema.json`) and the UI layout schema (`uiSchema.json`). This significantly accelerates form development by abstracting away the complexities of the JSON Schema standard.

## 2. Category

`ui_generation`

## 3. Parameters

### Required Parameters

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `--prompt` | string | A detailed natural language description of the form, including fields, types, validation rules, and UI hints (e.g., "use a password widget"). |
| `--output-dir` | string | The directory where the generated `schema.json` and `uiSchema.json` files will be saved. |

### Optional Parameters

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `--schema-filename` | string | `schema.json` | The filename for the output JSON Schema. |
| `--uischema-filename` | string | `uiSchema.json` | The filename for the output UI Schema. |
| `--model` | string | `gemini-2.5-flash` | The AI model to use for schema generation. Allows for selecting more powerful models for complex forms. |

## 4. Execution Logic

1.  **Prompt Analysis:** The workflow sends the user's prompt to the specified AI model.
2.  **Schema Generation:** The AI is instructed to generate two distinct JSON objects in a single response:
    *   A valid **JSON Schema** that defines the form's data structure, types, and validation rules (e.g., `required`, `minLength`, `format`).
    *   A **UI Schema** that defines the form's layout and widgets for RJSF (e.g., `ui:widget`, `ui:order`).
3.  **JSON Parsing & Validation:** The workflow parses the AI's response, extracts the two JSON objects, and validates their structure.
4.  **File Output:** The validated `schema.json` and `uiSchema.json` are written to the specified `--output-dir`.

## 5. Example Usage

### CLI

```bash
# Generate a user registration form
/smartspec_generate_rjsf_schema \
  --prompt "Create a user registration form. It needs an email field (must be a valid email), a password field with a minimum length of 8 characters, a password confirmation field that must match the password, and an optional checkbox to subscribe to the newsletter. The password fields should use a password widget. Order the fields as email, password, confirm password, then the newsletter." \
  --output-dir "src/config/forms/registration/"
```

### Kilo Code

```kilo
// Generate a settings form
smartspec_generate_rjsf_schema(
  prompt: "Create a user profile settings form. Include a read-only username field, an editable bio field using a textarea widget, and a dropdown to select a notification preference (None, Email, SMS).",
  output_dir: "src/config/forms/settings/"
)
```

## 6. Use Cases

-   **Rapid Prototyping:** Quickly generate complex forms for new features.
-   **Dynamic Form Generation:** Allow agents or systems to create forms on the fly based on contextual needs.
-   **Empowering Non-Developers:** Enable product managers or designers to define form structures using natural language.

## 7. Related Workflows

-   `smartspec_generate_ui_spec`: For generating non-form, dynamic UI components.
-   `smartspec_manage_theme`: For managing the theme that will be applied to the rendered RJSF form.

## 8. Implementation

Implemented in: `.smartspec/scripts/generate_rjsf_schema.py`

## 9. Notes

-   The quality of the output is highly dependent on the detail and clarity of the `--prompt`.
-   For very complex forms, it may be beneficial to use a more advanced model (e.g., `gpt-4.1-mini`) by specifying the `--model` parameter.
-   The generated schemas can be further edited manually for fine-tuning.
