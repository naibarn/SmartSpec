# /smartspec_ui_component_audit Manual (v6.0, English)

## Overview

The `/smartspec_ui_component_audit` workflow performs **static analysis** on frontend source code to audit adherence to a defined Design System.

**Purpose:**
1.  Verify the correct usage of the specified component library (e.g., MUI, Ant Design).
2.  Ensure adherence to design tokens (colors, spacing, typography).
3.  Perform best-effort static checks for Web Content Accessibility Guidelines (WCAG) compliance.

**Version:** 6.1.1
**Category:** Quality Assurance
**Nature:** Reports-only. This workflow does not run the application, fetch network resources, or modify source code. The `--apply` flag is accepted but ignored.

---

## Usage

### CLI Usage

The workflow is invoked directly from the command line, requiring the source root, component library name, and the design token baseline file.

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

### Kilo Code Usage

For integration within SmartSpec markdown specifications or interactive environments, use the Kilo Code invocation.

```bash
/smartspec_ui_component_audit.md \
  --source-root <path/to/src> \
  --component-library <mui|antd|chakra|other> \
  --design-tokens <path/to/tokens.json> \
  [--wcag-level <AA|AAA>] \
  [--strict] \
  [--out <output-root>] \
  [--json] \
  --kilocode
```

---

## Use Cases

### Use Case 1: Standard Design System Compliance Audit

**Scenario:** A development team needs a quick audit of their `src/` directory against the MUI component library and their standard design token file (`design/tokens.json`), aiming for WCAG AA compliance.

**Goal:** Generate a standard report showing all errors and warnings.

**CLI Command:**

```bash
/smartspec_ui_component_audit \
  --source-root src/frontend \
  --component-library mui \
  --design-tokens config/design/tokens.json \
  --wcag-level AA
```

**Expected Result:**
A new directory is created under `.spec/reports/ui-component-audit/<run-id>/` containing:
1.  `report.md`: A human-readable report summarizing findings, including instances of hardcoded colors (UCA-101) or deprecated MUI component usage (UCA-002).
2.  `summary.json`: A machine-readable JSON summary detailing the status (e.g., `status: "warn"` if only warnings are found) and all findings.
3.  Exit code `0` (since `--strict` was not used).

### Use Case 2: Strict Audit for Pre-Release Gate

**Scenario:** Before merging a major feature branch, the CI/CD pipeline must enforce strict compliance. Any finding (error or warning) must result in a failure. The team uses Chakra UI and requires WCAG AAA compliance for critical components.

**Goal:** Fail the workflow immediately if any non-passing finding is detected, outputting results to a custom directory.

**Kilo Code Command:**

```bash
/smartspec_ui_component_audit.md \
  --source-root feature/new-dashboard/src \
  --component-library chakra \
  --design-tokens config/design/tokens_v2.json \
  --wcag-level AAA \
  --strict \
  --out ci/audit_results \
  --kilocode
```

**Expected Result:**
1.  The workflow executes with heightened sensitivity (WCAG AAA).
2.  If a hardcoded spacing value (UCA-102) is found, the workflow will immediately exit with code `1` (Audit failed).
3.  Reports are written to `ci/audit_results/<run-id>/`.
4.  If the scan hits the configured file limit, a `UCA-290 Reduced Coverage` warning is logged in the report.

### Use Case 3: JSON Output for Integration

**Scenario:** An external dashboard needs the raw output of the audit in JSON format for visualization and tracking.

**Goal:** Run a standard audit and output the primary result artifact as a single JSON object to STDOUT, suppressing other output.

**CLI Command:**

```bash
/smartspec_ui_component_audit \
  --source-root src/app \
  --component-library antd \
  --design-tokens assets/tokens.json \
  --json \
  --quiet
```

**Expected Result:**
1.  The `summary.json` content is written directly to STDOUT.
2.  No other messages or the `report.md` are generated or printed (due to `--quiet`).
3.  The workflow still writes the report artifacts to the default or specified `--out` location, but the primary output is redirected to STDOUT in JSON format.

---

## Parameters

The following parameters and flags are available for the workflow.

| Flag | Category | Required | Description | Values | Default |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `--source-root` | Workflow | Yes | Root directory of the frontend source code to audit. | `<path>` | N/A |
| `--component-library` | Workflow | Yes | Component library in use. | `mui`, `antd`, `chakra`, `other` | N/A |
| `--design-tokens` | Workflow | Yes | Path to the JSON file containing the design token baseline. | `<path/to/tokens.json>` | N/A |
| `--wcag-level` | Workflow | No | Target WCAG compliance level for accessibility checks. | `AA`, `AAA` | `AA` |
| `--strict` | Workflow | No | If set, the workflow fails (`exit 1`) on any warning or error. | Boolean flag | Disabled |
| `--apply` | Universal | No | Accepted for compatibility but **ignored**. | Boolean flag | Disabled |
| `--out` | Universal | No | Requested base output root. Must comply with safety constraints. | `<path>` | `.spec/reports/ui-component-audit/` |
| `--json` | Universal | No | Output the primary result artifact (`summary.json`) to STDOUT. | Boolean flag | Disabled |
| `--quiet` | Universal | No | Suppress non-essential output (useful with `--json`). | Boolean flag | Disabled |
| `--config` | Universal | No | Path to the SmartSpec configuration file. | `<path>` | `.spec/smartspec.config.yaml` |
| `--lang` | Universal | No | Output language for reports. | `th`, `en` | `en` |
| `--platform` | Universal | No | Execution platform context. | `cli`, `kilo`, `ci`, `other` | `cli` |

---

## Output Artifacts

The workflow generates reports under a unique run folder to prevent collision.

**Default Output Root:** `.spec/reports/ui-component_audit/<run-id>/`

| Artifact | Format | Description |
| :--- | :--- | :--- |
| `report.md` | Markdown | The human-readable detailed audit report, structured with a summary, detailed findings (errors/warnings), and next steps. |
| `summary.json` | JSON | Machine-readable summary of the audit, including run metadata, scope, and structured lists of all findings (`errors`, `warnings`, `na`). |

**Exit Codes:**

*   **0:** Audit passed, or only warnings were found (non-strict mode).
*   **1:** Audit failed (strict mode) or critical failures were found.
*   **2:** Usage/config error (e.g., invalid path, safety violation).

---

## Notes & Related Workflows

### Static Analysis Limitations
This workflow relies solely on static code analysis. It cannot account for:
*   Runtime theme switching or dynamic style calculations.
*   Styles applied via complex logic or external libraries not directly analyzed.
*   Accessibility issues requiring user interaction (e.g., keyboard navigation focus order).

Findings related to color contrast (UCA-204) are based on the static token definitions and disclosed assumptions about foreground/background pairing.

### Related Workflows

*   **`/smartspec_dependency_vulnerability_scan`**: For auditing security vulnerabilities in project dependencies.
*   **`/smartspec_code_style_linter`**: For enforcing general code style and formatting rules.
*   **`/smartspec_design_token_validator`**: A dedicated workflow for validating the structure and consistency of the design token file itself.

---
*Last updated: SmartSpec v6.0*