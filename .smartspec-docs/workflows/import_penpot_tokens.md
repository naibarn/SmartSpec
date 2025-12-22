_**Note:** This is the user manual for the `smartspec_import_penpot_tokens` workflow. For the technical workflow definition, please see [`.smartspec/workflows/smartspec_import_penpot_tokens.md`](../../.smartspec/workflows/smartspec_import_penpot_tokens.md)._

# Workflow: smartspec_import_penpot_tokens

## 1. Overview

The `smartspec_import_penpot_tokens` workflow is a powerful tool designed to bridge the gap between design and development by automating the import of design tokens from **Penpot**, an open-source design and prototyping platform. This workflow allows you to directly translate your design system created in Penpot into a functional `theme.json` file for your SmartSpec A2UI applications.

By automating this process, you can ensure that your development environment is always in sync with the latest design decisions, eliminating manual errors and significantly speeding up the design-to-code process.

## 2. Key Features

- **Direct Penpot Integration:** Import tokens directly from Penpot using its API or from an exported JSON file.
- **Automatic Token Mapping:** Intelligently maps Penpot's color libraries, text styles, and components to the SmartSpec `theme.json` structure.
- **Flexible Merge Strategies:** Provides control over how imported tokens are merged with an existing theme, allowing you to either merge, overwrite, or append new tokens.
- **Seamless Workflow:** Integrates perfectly with `smartspec_manage_theme` and other A2UI workflows.

## 3. Penpot Integration

This workflow offers two methods for importing tokens from Penpot.

### Method 1: Import from File

This is the simplest method. You can export your Penpot design file as a JSON file and provide it to the workflow.

**How to export from Penpot:**
1.  Open your design file in Penpot.
2.  Navigate to the **Main Menu** (top-left corner).
3.  Select **Export**.
4.  Choose the **Export as JSON** option.
5.  Save the file to your project.

### Method 2: Import from API

For a more automated and continuous integration setup, you can import tokens directly from the Penpot API. This method requires you to provide your Penpot instance URL, project ID, file ID, and an access token.

**How to get an API access token:**
1.  In Penpot, go to your **Settings** or user profile.
2.  Find the **Access Tokens** or **API** section.
3.  Generate a new access token with the necessary permissions.
4.  Copy the token securely. It is recommended to store it as an environment variable rather than hardcoding it in your commands.

## 4. Parameters

The workflow's behavior is controlled by the following parameters.

### Required Parameters

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `--source` | string | The source of the Penpot tokens. Must be either `file` or `api`. |

### Optional Parameters

| Parameter | Type | Description | Required For |
| :--- | :--- | :--- | :--- |
| `--input-file` | string | The path to the exported Penpot JSON file. | `file` source |
| `--penpot-url` | string | The URL of your Penpot instance. Defaults to `https://design.penpot.app`. | `api` source |
| `--project-id` | string | The ID of your Penpot project. | `api` source |
| `--file-id` | string | The ID of the Penpot file containing the design tokens. | `api` source |
| `--access-token` | string | Your Penpot API access token. | `api` source |
| `--merge-strategy` | string | Defines how to handle conflicts with an existing theme. Defaults to `merge`. | All sources |
| `--theme-file` | string | The path to the `theme.json` file. Defaults to `.spec/theme.json`. | All sources |

### Merge Strategies

The `--merge-strategy` parameter gives you fine-grained control over the import process:

- **`merge` (Default):** Combines the imported tokens with the existing theme. If a token already exists, its current value is preserved.
- **`overwrite`:** Completely replaces the existing theme with the imported tokens. Use this with caution, as it will delete any custom tokens you may have added.
- **`append`:** Only adds new tokens from the Penpot file. Existing tokens are skipped and left untouched.

## 5. Example Usage

Here are some common scenarios for using this workflow.

### Use Case 1: Bootstrapping a New Project from a Penpot Design

You have a complete design system in Penpot and want to create a new `theme.json` from it.

**Command:**
```bash
# First, export your Penpot file to design/design-system.json

/smartspec_import_penpot_tokens \
  --source file \
  --input-file design/design-system.json \
  --merge-strategy overwrite
```

**Result:** A new `theme.json` is created at `.spec/theme.json`, containing all the colors, typography, and component styles from your Penpot file.

### Use Case 2: Syncing Design Updates from the Penpot API

Your design team has updated the brand colors in Penpot, and you want to sync these changes into your existing theme without losing your custom tokens.

**Command:**
```bash
# Assumes PENPOT_TOKEN is an environment variable
/smartspec_import_penpot_tokens \
  --source api \
  --project-id "a1b2c3d4-e5f6-7890-abcd-ef1234567890" \
  --file-id "f1e2d3c4-b5a6-9870-fedc-ba0987654321" \
  --access-token $PENPOT_TOKEN \
  --merge-strategy merge
```

**Result:** The workflow fetches the latest tokens from the Penpot API. It updates any changed tokens and adds new ones, but preserves any existing tokens that were not part of the import, thanks to the `merge` strategy.

### Use Case 3: Appending New Component Styles

Your team has designed a new set of components in Penpot, and you want to add them to your theme without affecting the existing tokens.

**Command:**
```bash
/smartspec_import_penpot_tokens \
  --source file \
  --input-file design/new-components.json \
  --merge-strategy append
```

**Result:** Only the new component styles from the Penpot file are added to your `theme.json`. All existing tokens and component styles remain unchanged.

## 6. Token Mapping Logic

The workflow uses intelligent mapping to convert Penpot's structure to the SmartSpec theme format.

| Penpot Element | SmartSpec Path | Mapping Logic |
| :--- | :--- | :--- |
| Color Libraries | `tokens.colors.*` | The library name is normalized (e.g., "Primary Colors" becomes `primary`). Color names with numbers (e.g., "Blue 500") are mapped to the corresponding shade. |
| Text Styles | `tokens.typography.*` | Style names are normalized. Font family, size, weight, and line height are extracted and placed in the appropriate typography sub-sections. |
| Components | `components.*.variants.*` | Penpot components are mapped to component variants in the theme, allowing you to reuse them in your UI specs. |

## 7. Related Workflows

- **`smartspec_manage_theme`**: After importing, you can use this workflow to further manage, validate, or export your theme.
- **`smartspec_generate_ui_spec`**: This workflow consumes the `theme.json` file to generate A2UI specifications with consistent styling.
