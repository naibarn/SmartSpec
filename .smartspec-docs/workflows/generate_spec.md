# /smartspec_generate_spec Manual (v6.0, English)

## Overview

The `/smartspec_generate_spec` workflow is the canonical entry point for creating, refining, and validating specification documents (`spec.md`) within the SmartSpec ecosystem, adhering strictly to **SPEC-first** governance principles.

**Purpose:** To ensure specifications are complete, adhere to defined standards (UX/UI baseline, NFRs), and enforce reuse-first behavior to prevent duplication. It operates safely by default, providing auditable previews and diffs before any governed artifacts are written.

**Version:** 6.0.2
**Category:** core

---

## Usage

This workflow supports invocation via the Command Line Interface (CLI) and Kilo Code (internal scripting environment).

### CLI Usage

The CLI invocation requires specifying the target specification either by file path or by ID(s).

```bash
/smartspec_generate_spec \
  (--spec <path/to/spec.md> | --spec-ids <id1,id2,...>) \
  [--json] \
  [--apply]
```

### Kilo Code Usage

The Kilo Code invocation is identical to the CLI structure, typically used within automated pipelines or internal scripts.

```bash
/smartspec_generate_spec.md \
  (--spec <path/to/spec.md> | --spec-ids <id1,id2,...>) \
  [--json] \
  [--apply]
```

---

## Use Cases

### Use Case 1: Refining an Existing Specification (CLI)

**Scenario:** A product manager needs to update the existing specification for the "User Profile Service" (`specs/profile/profile_service.md`) and ensure it meets the accessibility baseline requirements defined in the configuration. The changes should be applied immediately after validation.

**Command:**

```bash
/smartspec_generate_spec \
  --spec specs/profile/profile_service.md \
  --apply
```

**Expected Result:**

1.  The workflow loads `specs/profile/profile_service.md`.
2.  It analyzes the content against the Spec Completeness Contract (e.g., checks for accessibility notes, NFRs).
3.  A safe preview bundle is written to `.spec/reports/generate-spec/<run-id>/...`.
4.  If no security violations (secrets) or mandatory failures are detected, the workflow proceeds with the governed write (`--apply`).
5.  `specs/profile/profile_service.md` is updated in-place with refined content/structure.
6.  The `.spec/SPEC_INDEX.json` is updated (if allowlisted) with the latest metadata.
7.  Exit code `0` (Success).

### Use Case 2: Generating a Preview for Multiple Specs (Kilo Code)

**Scenario:** A CI pipeline needs to validate two newly created specifications identified by IDs `FEAT-1001` and `BUG-045` before they are merged. The pipeline requires the output in JSON format for downstream processing but must *not* apply any changes to the source files.

**Command (Kilo Code Snippet):**

```bash
# Workflow is invoked without --apply for safety check
/smartspec_generate_spec.md \
  --spec-ids FEAT-1001,BUG-045 \
  --json \
  --out /tmp/spec_validation_report
```

**Expected Result:**

1.  The workflow resolves `FEAT-1001` and `BUG-045` paths using `.spec/SPEC_INDEX.json`.
2.  It performs completeness and duplication checks for both specs.
3.  A safe preview bundle is written to `/tmp/spec_validation_report/<run-id>/...`.
4.  The primary output is a `summary.json` file containing validation results, security checks, and next steps.
5.  No files under `specs/**` or `.spec/SPEC_INDEX.json` are modified.
6.  Exit code `0` (Success).

### Use Case 3: Refusing Application Due to Secret Leakage (CLI)

**Scenario:** A user attempts to refine a spec, but the generated content (preview) accidentally includes a string matching a configured redaction pattern (e.g., a test API key).

**Command:**

```bash
/smartspec_generate_spec \
  --spec specs/new_feature.md \
  --apply
```

**Expected Result:**

1.  The workflow generates the preview content.
2.  The content matches a configured redaction pattern (`safety.redaction`).
3.  The workflow redacts the value in the preview/report output.
4.  The workflow **refuses** to proceed with the `--apply` operation, as mandated by the Secret-blocking rule.
5.  A detailed `report.md` is generated, noting the secret detection and apply refusal.
6.  Exit code `1` (Validation Fail).

---

## Parameters

The following parameters and flags control the execution and behavior of the `/smartspec_generate_spec` workflow.

### Required (One-of)

| Parameter | Type | Description | Validation |
| :--- | :--- | :--- | :--- |
| `--spec` | `<path>` | Path to a single spec file to refine. | Must resolve under `specs/**`. Cannot be used with `--spec-ids`. |
| `--spec-ids` | `<csv>` | Comma-separated list of spec IDs to refine. | IDs must match `safety.spec_id_regex` and exist in `.spec/SPEC_INDEX.json`. Cannot be used with `--spec`. |

### Universal Flags

| Flag | Description | Default |
| :--- | :--- | :--- |
| `--config` | Path to the SmartSpec configuration file. | `.spec/smartspec.config.yaml` |
| `--lang` | Language for report generation (e.g., `th`, `en`). | (System default) |
| `--platform` | Execution platform context (`cli`, `kilo`, `ci`, etc.). | (Inferred) |
| `--apply` | Enables governed writes (modifying `specs/**` and potentially the index). | `false` |
| `--out` | Base path for safe outputs (reports/previews). | `.spec/reports/generate-spec/` |
| `--json` | Output the primary summary in JSON format (`summary.json`). | `false` |
| `--quiet` | Suppress standard output logs. | `false` |

### Workflow-Specific Flags

| Flag | Description |
| :--- | :--- |
| `--spec` | (See Required Inputs) |
| `--spec-ids` | (See Required Inputs) |

---

## Output

The workflow generates two types of output artifacts: Safe Preview Bundles (always) and Governed Artifacts (only with `--apply`).

### Safe Preview Bundle (Always Generated)

A unique run folder is created under the report path (default: `.spec/reports/generate-spec/<run-id>/`).

| Artifact | Description |
| :--- | :--- |
| `preview/<spec-id>/spec.md` | The proposed, refined version of the specification. |
| `diff/<spec-id>.patch` | A best-effort patch file showing changes between the current and proposed spec. |
| `report.md` | A human-readable report detailing validation, completeness, reuse findings, and security notes. |
| `summary.json` | Structured JSON output of the run results (if `--json` is set). |

### Governed Output (Only with `--apply`)

1.  **Target Spec Update:** The original `spec.md` file is updated in-place.
2.  **Reference Files:** Missing required companion reference files (e.g., `references/decisions.md`) are created within the spec folder.
3.  **Index Update:** If the index is allowlisted, `.spec/SPEC_INDEX.json` is updated with current metadata (title, summary, tags).

### Exit Codes

| Code | Status | Description |
| :--- | :--- | :--- |
| `0` | Success | The workflow completed successfully (preview generated or changes applied). |
| `1` | Validation Fail | Input validation error, missing spec ID, unsafe path detection, or secret detected (refusing apply). |
| `2` | Usage/Config Error | Error in configuration loading or command usage. |

---

## Notes & Related Workflows

### Governance and Safety

*   **Safe-by-Default:** No files under `specs/**` or the registry are modified unless the `--apply` flag is explicitly set.
*   **Secret Blocking:** The workflow strictly enforces the Secret-blocking rule. If generated content matches redaction patterns, the workflow will redact the output but refuse to apply the changes (Exit Code 1).
*   **Reuse Policy:** The workflow actively detects probable duplication against existing specs in the index and mandates surfacing this as a **Reuse Warning** in the report/preview, preventing silent forks.

### Related Workflows

*   `/smartspec_generate_plan`: Used to generate implementation plans based on a validated spec.
*   `/smartspec_generate_