# /smartspec_security_threat_modeler Manual (v6.0, English)

## Overview

The `/smartspec_security_threat_modeler` workflow is a quality assurance tool designed to automatically generate a preliminary security threat model by analyzing the content of a SmartSpec (`spec.md`) and its corresponding plan (`plan.md`).

**Purpose:** To identify and document potential security risks early in the development lifecycle, producing a structured `threats.md` artifact using standard methodologies like STRIDE or DREAD.

**Version:** 6.1.0
**Category:** Quality
**Governance:** This is a **governed write** workflow, requiring the `--apply` flag to modify the project’s specification directory by creating or updating `threats.md`.

---

## Usage

### CLI (Command Line Interface)

The CLI invocation is used for direct execution within the project environment.

```bash
/smartspec_security_threat_modeler \
  <path/to/spec.md> \
  [--framework <STRIDE|DREAD>] \
  [--apply] \
  [--json]
```

### Kilo Code

Kilo Code usage is typically embedded within other SmartSpec workflows or CI/CD pipelines.

```bash
/smartspec_security_threat_modeler.md \
  specs/<category>/<spec-id>/spec.md \
  [--framework <STRIDE>] \
  [--apply] \
  [--json]
```

---

## Use Cases

### Use Case 1: Generating a Preliminary Threat Model (Preview Mode)

**Scenario:** A developer wants to see the initial security threat analysis for a new authentication service specification (`specs/auth/auth-v1/spec.md`) before committing to the findings.

**Goal:** Generate the threat model report without modifying the project files.

**CLI Command:**
```bash
/smartspec_security_threat_modeler specs/auth/auth-v1/spec.md --framework STRIDE --json
```

**Expected Result:**
1.  The workflow reads `specs/auth/auth-v1/spec.md` (and `plan.md` if present).
2.  A detailed report, including a preview of the generated `threats.md`, is written to `.spec/reports/security-threat-model/<run-id>/report.json`.
3.  A summary JSON output is printed to stdout.
4.  The file `specs/auth/auth-v1/threats.md` is **not** created or modified.

**Kilo Code:**
```kilo
# Preview the threat model for the authentication service using STRIDE
/smartspec_security_threat_modeler.md specs/auth/auth-v1/spec.md --framework STRIDE
```

### Use Case 2: Applying the Threat Model Artifact

**Scenario:** The threat model preview has been reviewed and approved. The security team now wants to commit the findings to the specification directory.

**Goal:** Create the `threats.md` artifact in the specification folder.

**CLI Command:**
```bash
/smartspec_security_threat_modeler specs/auth/auth-v1/spec.md --framework STRIDE --apply
```

**Expected Result:**
1.  The workflow performs the analysis.
2.  The file `specs/auth/auth-v1/threats.md` is created or updated atomically with the structured threat model content.
3.  The exit code is `0` (Success).

**Kilo Code:**
```kilo
# Apply the threat model, creating the threats.md file
/smartspec_security_threat_modeler.md specs/auth/auth-v1/spec.md --apply
```

### Use Case 3: Using an Alternative Framework

**Scenario:** The project requires the use of the DREAD framework for risk assessment instead of the default STRIDE.

**Goal:** Generate the threat model using the DREAD framework.

**CLI Command:**
```bash
/smartspec_security_threat_modeler specs/data/storage-v2/spec.md --framework DREAD --apply
```

**Expected Result:**
1.  The workflow analyzes the spec using the DREAD methodology (Damage, Reproducibility, Exploitability, Affected Users, Discoverability).
2.  `specs/data/storage-v2/threats.md` is created, detailing threats categorized and assessed by DREAD criteria.

---

## Parameters

### Positional Arguments (Inputs)

| Parameter | Required | Description |
| :--- | :--- | :--- |
| `spec_md` | Yes | Path to the primary `spec.md` file to be analyzed. Must reside under `specs/**`. |
| `plan.md` | No | If present in the same directory as `spec.md`, it is automatically used as additional context for the analysis. |

### Flags (Parameters)

| Flag | Category | Default | Description |
| :--- | :--- | :--- | :--- |
| `--framework <STRIDE\|DREAD>` | Workflow-Specific | `STRIDE` | Specifies the threat modeling framework to use for analysis and reporting. |
| `--apply` | Universal | None | **Required** to perform governed writes (create/update `threats.md`). Without this, the workflow runs in preview mode. |
| `--json` | Universal | None | Outputs the summary results in machine-readable JSON format to stdout. |
| `--config <path>` | Universal | Default config path | Specifies a custom configuration file path. |
| `--lang <th\|en>` | Universal | `en` | Specifies the language for output messages and generated text. |
| `--platform <cli\|kilo\|ci\|other>` | Universal | Derived | Specifies the execution environment. |
| `--out <path>` | Universal | `.spec/reports/...` | Specifies an alternative output path for reports and previews. |
| `--quiet` | Universal | None | Suppresses non-critical output messages. |

---

## Output

### Governed Artifact (Requires `--apply`)

*   **File:** `specs/<category>/<spec-id>/threats.md`
*   **Description:** A structured Markdown file containing the preliminary threat model, including a summary table and detailed entries for each identified threat (e.g., T-001, T-002). The structure adheres to the defined format, including Threat Category, Description, Asset at Risk, Affected Component, and Suggested Mitigation.

### Report and Preview Artifacts (Always Generated)

*   **Location:** `.spec/reports/security-threat-model/<run-id>/`
*   **Contents:**
    *   **Report:** Detailed logs, analysis findings, and the full content of the proposed `threats.md` file (preview).
    *   **Summary JSON:** A `summary.json` file detailing the run status, threat counts by category, and recommended next steps.

### `summary.json` Schema Excerpt

The output JSON includes a summary of the threats identified:

```json
{
  "status": "success",
  "applied": true,
  "scope": { ... },
  "summary": {
    "threat_counts": {
      "spoofing": 2,
      "tampering": 1,
      "repudiation": 3,
      "information_disclosure": 4,
      "denial_of_service": 1,
      "elevation_of_privilege": 2
    }
  },
  "writes": { ... },
  "next_steps": [
    {
      "cmd": "/smartspec_generate_tasks --spec <spec.md> --context <threats.md>",
      "why": "Generate security tasks based on the identified threats."
    }
  ]
}
```

---

## Notes & Related Workflows

### Non-Destructive Merge

If `threats.md` already exists, the workflow is designed to perform a non-destructive merge. It will attempt to integrate new findings while preserving existing, manually-edited entries within the file, respecting the defined structure.

### Hardening Requirements

This workflow adheres to strict security hardening requirements, including:
*   No external network access (`safety.network_policy.default=deny`).
*   Redaction of sensitive data based on configuration patterns.
*   Strict enforcement of read and write scopes to prevent path traversal.

### Related Workflows

*   `/smartspec_generate_tasks`: Use this workflow *after* generating `threats.md` to automatically convert the identified security threats into actionable development tasks.
*   `/smartspec_analyze_compliance`: Used for checking the generated `threats.md` against organizational security policies or regulatory standards.

---
*Last updated: SmartSpec v6.0*