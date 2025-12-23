#!/usr/bin/env python3

import os
import json
import argparse
import sys
from openai import OpenAI

# Initialize the OpenAI client
# The client will automatically pick up the OPENAI_API_KEY and OPENAI_BASE_URL from the environment
client = OpenAI()

SYSTEM_PROMPT = """
You are an expert in creating form configurations for React JSON Schema Form (RJSF). Your task is to take a user's natural language prompt and generate two valid JSON objects: a `JSON Schema` and a `UI Schema`.

**Constraints & Rules:**
1.  You MUST return a single JSON object as your response.
2.  This JSON object MUST contain two top-level keys: `json_schema` and `ui_schema`.
3.  The value of `json_schema` MUST be a valid JSON Schema object defining the form's data structure and validation rules.
4.  The value of `ui_schema` MUST be a valid RJSF UI Schema object defining the form's layout, widgets, and ordering.
5.  Pay close attention to user requests for specific widgets (e.g., `password`, `textarea`), validation (e.g., `minLength`, `format: email`), and field order (`ui:order`).
6.  If the user requests a password confirmation field, you MUST implement the custom validation logic within the JSON schema as described in RJSF documentation, using `dependencies`.
7.  Do not include any explanatory text or markdown formatting in your response. The output must be a raw, parsable JSON object.

**Example Output Format:**
```json
{
  "json_schema": {
    "title": "A registration form",
    "description": "A simple form example.",
    "type": "object",
    "required": ["firstName", "lastName"],
    "properties": {
      "firstName": {
        "type": "string",
        "title": "First name"
      },
      "lastName": {
        "type": "string",
        "title": "Last name"
      }
    }
  },
  "ui_schema": {
    "firstName": {
      "ui:autofocus": true,
      "ui:emptyValue": ""
    },
    "lastName": {
      "ui:emptyValue": ""
    }
  }
}
```
"""

def generate_schemas(prompt: str, model: str):
    """Generates schemas using the specified AI model."""
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            response_format={"type": "json_object"}
        )
        response_content = completion.choices[0].message.content
        return json.loads(response_content)
    except Exception as e:
        print(f"Error: Failed to generate schemas from AI model: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Generates JSON Schema and UI Schema for RJSF from a natural language prompt.")
    parser.add_argument("--prompt", required=True, help="A detailed natural language description of the form.")
    parser.add_argument("--output-dir", required=True, help="The directory where the generated files will be saved.")
    parser.add_argument("--schema-filename", default="schema.json", help="The filename for the output JSON Schema.")
    parser.add_argument("--uischema-filename", default="uiSchema.json", help="The filename for the output UI Schema.")
    parser.add_argument("--model", default="gemini-2.5-flash", help="The AI model to use for schema generation.")

    args = parser.parse_args()

    print(f"Generating RJSF schemas for prompt: \"{args.prompt[:50]}...\"")

    # Generate the schemas
    generated_json = generate_schemas(args.prompt, args.model)

    # Validate the response structure
    if 'json_schema' not in generated_json or 'ui_schema' not in generated_json:
        print("Error: The AI response did not contain the expected 'json_schema' and 'ui_schema' keys.", file=sys.stderr)
        print(f"Received: {generated_json}", file=sys.stderr)
        sys.exit(1)

    json_schema = generated_json['json_schema']
    ui_schema = generated_json['ui_schema']

    # Create the output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Define output paths
    schema_path = os.path.join(args.output_dir, args.schema_filename)
    uischema_path = os.path.join(args.output_dir, args.uischema_filename)

    # Write the files
    try:
        with open(schema_path, 'w') as f:
            json.dump(json_schema, f, indent=2)
        print(f"✅ Successfully wrote JSON Schema to: {schema_path}")

        with open(uischema_path, 'w') as f:
            json.dump(ui_schema, f, indent=2)
        print(f"✅ Successfully wrote UI Schema to: {uischema_path}")

    except IOError as e:
        print(f"Error: Failed to write schema files: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
