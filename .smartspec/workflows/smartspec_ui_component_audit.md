---
description: Audit UI components for consistency and best practices.
version: 6.0.0
workflow: /smartspec_ui_component_audit
---

# smartspec_ui_component_audit

> **Version:** 6.1.1  
> **Status:** Proposed  
> **Category:** quality

## Purpose

Audit frontend source code against a defined Design System, focusing on:

1) **Component library usage** correctness (e.g., MUI / Ant Design / Chakra)
2) **Design token adherence** (colors, spacing, typography)
3) **Accessibility (WCAG)** best-effort static checks

This workflow performs **static analysis only**. It **does not** run the app, does **not** fetch network resources, and does **not** modify code.

It is a **reports-only** workflow.

---

## Governance contract

This workflow MUST follow:

- `knowledge_base_smartspec_handbook.md` (v6)
- `.spec/smartspec.config.yaml`

### Write scopes (enforced)

Allowed writes (safe outputs only):

- Reports: `.spec/reports/ui-component-audit/**`

Forbidden writes (must hard-fail):

- Any path outside config `safety.allow_writes_only_under`
- Any path under config `safety.deny_writes_under`
- Any governed artifact (e.g., `specs/**`, `.spec/SPEC_INDEX.json`, `.spec/WORKFLOWS_INDEX.yaml`)
- Any runtime source tree modifications

### `--apply` behavior (universal flag)

- Accepted for compatibility but **ignored**.
- The report header MUST note that `--apply` was ignored if provided.

---

## Threat model (minimum)

This workflow must defend against:

- Path traversal / symlink escape via `--source-root` and token file paths.
- Secret leakage into reports (e.g., tokens embedded in `.env`, config snippets).
- Runaway scans / CI cost spikes due to large repos.
- Accidental network usage.

### Hardening requirements (MANDATORY)

- **No network access:** Respect `safety.network_policy.default=deny`.
- **No shell execution:** Do not run arbitrary commands from inputs.
- **Path normalization (reads + writes):** Reject traversal (`..`), absolute paths, and control characters on any user-supplied path.
- **No symlink escape (reads + writes):** Do not read/write through symlinks that resolve outside allowed scopes.
- **Read scope enforcement:** All reads MUST remain within project root (or configured workspace roots if supported).
- **Output root safety:** If `--out` is provided, it is a *requested* base output root and MUST:
  - resolve under config `safety.allow_writes_only_under`
  - not fall under config `safety.deny_writes_under`
  - not be a runtime source folder
  - hard-fail with usage/config error (`exit 2`) if invalid
- **Redaction:** Apply `safety.redaction` patterns to all report outputs.
- **Excerpt policy:** Do not paste large file contents; include short excerpts only when necessary.
- **Output collision:** Respect `safety.output_collision` (never overwrite existing run folders).
- **Bounded scanning:** Respect config `safety.content_limits` (max files/bytes/time).

---

## Invocation

### CLI

```bash
/smartspec_ui_component_audit \
  --source-root <path/to/src> \
  --component-library <mui|antd|chakra|other> \
  --design-tokens <path/to/tokens.json> \
  [--wcag-level <AA|AAA>] \
  [--strict] \
  [--out <output-root>] \
  [--json]
```

### Kilo Code

```bash
/smartspec_ui_component_audit.md \
  --source-root <path/to/src> \
  --component-library <mui|antd|chakra|other> \
  --design-tokens <path/to/tokens.json> \
  [--wcag-level <AA|AAA>] \
  [--strict] \
  [--out <output-root>] \
  [--json] \
  --platform kilo
```

---

## Inputs

### Required

- `--source-root <path>`: Root directory of the frontend source code to audit.
- `--component-library <name>`: Component library in use (e.g., `mui`, `antd`, `chakra`).
- `--design-tokens <path>`: Token file path (JSON baseline).

### Optional

- `--wcag-level <AA|AAA>`: Defaults to `AA`.

### Input validation (MANDATORY)

- `--source-root` MUST exist and be a directory.
- `--design-tokens` MUST exist and be a valid JSON file.
- All user-supplied paths MUST reject traversal (`..`), absolute paths, and control characters.
- All resolved paths MUST remain within project root and MUST NOT escape via symlinks.

---

## Flags

### Universal flags (must support)

- `--config <path>`
- `--lang <th|en>`
- `--platform <cli|kilo|ci|other>`
- `--apply` (ignored)
- `--out <path>`
- `--json`
- `--quiet`

### Workflow-specific flags

- `--source-root <path>` (required)
- `--component-library <name>` (required)
- `--design-tokens <path>` (required)
- `--strict` (optional)
- `--wcag-level <AA|AAA>` (optional)

### Scan scope defaults (RECOMMENDED baseline)

Unless config overrides, the workflow SHOULD ignore:

- `node_modules/`, `.git/`, `dist/`, `build/`, `.next/`, `.cache/`, `coverage/`, `storybook-static/`

If limits are reached, the workflow MUST emit `UCA-290 Reduced Coverage` and lower confidence for affected findings.

---

## Output structure

Outputs are always written under a run folder to prevent overwrites.

- Default root: `.spec/reports/ui-component-audit/<run-id>/...`
- If `--out` is provided, it is treated as a *requested* base output root and MUST pass Output root safety validation; otherwise `exit 2`.

Artifacts:

- `report.md`
- `summary.json`

### Exit codes

- `0`: Audit passed, or only warnings were found (non-strict mode).
- `1`: Audit failed (strict mode) or critical failures were found.
- `2`: Usage/config error.

---

## Checks (v6.1)

Each check MUST emit a stable ID (`UCA-xxx`).

### Preflight safety checks (always enforced)

- **UCA-000 Preflight Safety**: Validate paths, `--out` safety, read/write constraints (path normalization + no symlink escape), and scan limits. Fail with `exit 2` on violation.

### Component Library Checks (MUST)

- **UCA-001 Disallowed Component Import**: Detect imports from disallowed paths (e.g., internal component paths like `@mui/material/Button/Button` instead of `@mui/material/Button`).
- **UCA-002 Deprecated Component Usage**: Flag usage of components marked as `@deprecated` in library definitions (best-effort).

### Design Token Checks (MUST)

- **UCA-101 Hardcoded Color**: Detect hardcoded color values (e.g., `#FFF`, `rgb(0,0,0)`) instead of using a token.
- **UCA-102 Hardcoded Spacing**: Detect hardcoded spacing values (e.g., `margin: '10px'`) instead of a token.
- **UCA-103 Hardcoded Font Size**: Detect hardcoded font sizes (e.g., `fontSize: '14px'`) instead of a token.

### Accessibility Checks (SHOULD, unless `--strict`)

- **UCA-201 Missing Image Alt Text**: Flag `<img>` elements missing an `alt` attribute.
- **UCA-202 Missing Form Label**: Flag form inputs (`<input>`, `<textarea>`) not associated with a `<label>`.
- **UCA-203 Invalid ARIA Props**: Detect incorrect or misspelled ARIA attributes (e.g., `aria-labledby` instead of `aria-labelledby`).
- **UCA-204 Insufficient Color Contrast**: Check color tokens for WCAG AA/AAA contrast compliance.
  - MUST disclose assumptions about token pairing (foreground/background) and treat uncertain cases as `warn`.
- **UCA-205 Non-interactive Element with Handler**: Flag non-interactive elements (e.g., `<div>`, `<span>`) with click handlers missing `role` and `tabIndex`.

### Meta / quality-of-result checks (warnings)

- **UCA-290 Reduced Coverage**: Limits reached or directories skipped; reduced confidence.
- **UCA-291 Unsupported Pattern**: Some files/patterns could not be reliably parsed; mark affected checks as `na`.

---

## Accuracy / assumptions (MANDATORY disclosure)

Because this is static analysis, the workflow MUST disclose:

- parsing/stack assumptions (framework/style system)
- token pairing logic used for contrast checks
- limitations for runtime theme switching, conditional classes, and computed styles

When uncertain, prefer `warn` or `na` instead of overconfident `fail`.

---

## `report.md` Artifact Structure

```markdown
# UI Component Audit Report

**Run ID:** <run-id>

## 1. Summary

- **Overall Status:** Fail (4 errors, 2 warnings)
- **Source Root:** `src/`
- **Component Library:** MUI

| Category              | Errors | Warnings |
| :-------------------- | :----- | :------- |
| Design Tokens         | 3      | 0        |
| Accessibility         | 1      | 2        |
| Component Library     | 0      | 0        |

## 2. Detailed Findings

### 🔴 Errors (High Priority)

- **[UCA-101] Hardcoded Color**
  - **File:** `src/components/Header.tsx:25:12`
  - **Finding:** Found hardcoded color `#FFFFFF`. Should use a design token like `theme.palette.common.white`.
  - **Code:** `<Box sx={{ backgroundColor: '#FFFFFF' }}>`

- **[UCA-205] Non-interactive Element with Handler**
  - **File:** `src/components/Card.tsx:15:8`
  - **Finding:** A `<div>` element has an `onClick` handler but is missing `role="button"` and `tabIndex="0"`.
  - **Code:** `<div onClick={handleClick}>`

### 🟡 Warnings (Medium Priority)

- **[UCA-201] Missing Image Alt Text**
  - **File:** `src/pages/Profile.tsx:30:5`
  - **Finding:** The `<img>` element for the user avatar is missing an `alt` attribute.
  - **Code:** `<img src={user.avatarUrl} />`

---

## 3. Next Steps

- Recommend next steps that are guaranteed to exist in your project registry (`.spec/WORKFLOWS_INDEX.yaml`).
- If suggesting a SmartSpec workflow, include both CLI + Kilo forms.

Template (replace with real registry-backed commands):

CLI:
`/<workflow_name> <primary-input> [--out <dir>] [--json]`

Kilo:
`/<workflow_name>.md <primary-input> [--out <dir>] [--json] --platform kilo`
```

---

## `summary.json` schema (minimum)

```json
{
  "workflow": "smartspec_ui_component_audit",
  "version": "6.1.1",
  "run_id": "string",
  "status": "pass|fail|warn",
  "scope": {
    "source_root": "string",
    "component_library": "string",
    "design_tokens": "string",
    "wcag_level": "AA|AAA",
    "limits": {
      "max_files": 0,
      "max_bytes": 0,
      "max_seconds": 0
    }
  },
  "results": {
    "errors": [
      {
        "check_id": "UCA-101",
        "category": "Design Tokens",
        "file": "src/components/Header.tsx",
        "line": 25,
        "details": "Found hardcoded color '#FFFFFF'."
      }
    ],
    "warnings": [
      {
        "check_id": "UCA-201",
        "category": "Accessibility",
        "file": "src/pages/Profile.tsx",
        "line": 30,
        "details": "The <img> element is missing an 'alt' attribute."
      }
    ],
    "na": []
  },
  "meta": {
    "reduced_coverage": false,
    "redactions_applied": 0
  },
  "writes": {"reports": ["path/to/report.md", "path/to/summary.json"]}
}
```

---

# End of workflow doc

