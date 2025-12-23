# Workflow: /smartspec_generate_rjsf_schema

**Generates JSON Schema and UI Schema for React JSON Schema Form (RJSF) from a natural language prompt.**

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

## 4. Example Usage

### Generate a User Registration Form

**Command:**
```bash
/smartspec_generate_rjsf_schema \
  --prompt "Create a user registration form. It needs an email field (must be a valid email), a password field with a minimum length of 8 characters, a password confirmation field that must match the password, and an optional checkbox to subscribe to the newsletter. The password fields should use a password widget. Order the fields as email, password, confirm password, then the newsletter." \
  --output-dir "src/config/forms/registration/"
```

**Result:**
- A `schema.json` file is created in the output directory with the data structure and validation rules.
- A `uiSchema.json` file is created with the specified field order and password widgets.

---

### Generate a Settings Form with a Dropdown

**Command:**
```bash
/smartspec_generate_rjsf_schema \
  --prompt "Create a user profile settings form. Include a read-only username field, an editable bio field using a textarea widget, and a dropdown to select a notification preference (None, Email, SMS)." \
  --output-dir "src/config/forms/settings/"
```

**Result:**
- The `schema.json` will define the `notification_preference` field as an `enum`.
- The `uiSchema.json` will define the `bio` field with `"ui:widget": "textarea"`.

## 5. Notes

- The quality of the generated schemas is highly dependent on the detail and clarity of the `--prompt`. Be as specific as possible about validation, widgets, and field order.
- For very complex forms with conditional logic, you may need to manually edit the generated files for fine-tuning.
- This workflow is a powerful tool for rapid prototyping and can be integrated into a larger process where an AI agent designs and builds forms dynamically.
