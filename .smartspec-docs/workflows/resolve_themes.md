# Workflow: /smartspec_resolve_themes

**Merges multiple theme files into a single, resolved theme based on a specified hierarchy, enabling multi-level theming.**

---

## 1. Overview

This workflow implements a multi-level, hierarchical theme system, a core concept from `SPEC-UI-001`. It takes a base theme and a series of override themes, then performs a deep merge to produce a single, resolved `theme.json` file. This is essential for enabling white-labeling, company-specific branding, and user personalization.

## 2. Category

`ui_theming_and_design`

## 3. Parameters

### Required Parameters

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `--base-theme` | string | Path to the base or system-level theme file (lowest precedence). |
| `--override-themes` | list | A JSON string representing an ordered list of paths to theme files that will override the base. The last theme in the list has the highest precedence. |
| `--output-file` | string | Path to save the final, merged theme file. |

## 4. Example Usage

### Resolve Themes for a Specific User

**Command:**
```bash
/smartspec_resolve_themes \
  --base-theme "src/config/themes/system.theme.json" \
  --override-themes '[\
    "src/config/themes/company-acme.theme.json", \
    "src/config/themes/user-123.theme.json" \
  ]' \
  --output-file ".spec/resolved-theme.json"
```

**Result:**
- The `resolved-theme.json` file will contain a combination of all three themes. Any token present in `user-123.theme.json` will take precedence over `company-acme.theme.json`, which in turn takes precedence over `system.theme.json`.

---

### Create a Dark Mode Theme

**Command:**
```bash
/smartspec_resolve_themes \
  --base-theme "src/config/themes/system.theme.json" \
  --override-themes '["src/config/themes/dark-mode.theme.json"]' \
  --output-file "public/dark-theme.json"
```

**Result:**
- A `dark-theme.json` is created, containing the base system theme with the dark mode color palette merged on top.

## 5. Notes

- The `--override-themes` parameter must be a valid JSON array of strings. Use single quotes around the argument in bash to prevent shell expansion issues.
- The merge logic is deep, meaning nested objects are merged recursively. This allows for fine-grained control over theme modifications.
- If an override theme file is not found, a warning will be printed, and the workflow will continue. This allows for optional themes (e.g., a user theme that may or may not exist).
