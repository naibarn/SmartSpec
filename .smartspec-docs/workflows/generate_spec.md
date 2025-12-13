| manual_name | manual_version | compatible_workflow | compatible_workflow_versions |
|-------------|----------------|---------------------|------------------------------|
| /smartspec_generate_spec Manual (EN) | 6.0 | /smartspec_generate_spec | 6.0.x |

# /smartspec_generate_spec Manual (v6.0, English)

## 1. Overview

This manual explains how to use the workflow:

The `/smartspec_generate_spec` workflow is the canonical entry point for creating, refining, and validating specification documents (`spec.md`) within the SmartSpec ecosystem, adhering strictly to **SPEC-first** governance principles.

**Purpose:** To ensure specifications are complete, adhere to defined standards (UX/UI baseline, NFRs), and enforce reuse-first behavior to prevent duplication. It operates safely by default, providing auditable previews and diffs before any governed artifacts are written.

**Version:** 6.0.2  
**Category:** core

---

## 2. Usage

This workflow supports invocation via the Command Line Interface (CLI) and Kilo Code (internal scripting environment).

### 🔗 CLI Usage

The CLI invocation requires specifying the target specification either by file path or by ID(s).

```bash
/smartspec_generate_spec \
  (--spec <path/to/spec.md> | --spec-ids <id1,id2,...>) \
  [--json] \
  [--apply]
```

### Kilo Code Usage

The Kilo Code invocation is identical to the CLI structure, typically used within automated pipelines or internal scripts.

**Important:** When using Kilo Code, you MUST include `--platform kilo` flag.

```bash
/smartspec_generate_spec.md \
  (--spec <path/to/spec.md> | --spec-ids <id1,id2,...>) \
  [--json] \
  [--apply] \
  --platform kilo
```

---

## 3. Use Cases

### Use Case 1: Refining an Existing Specification (CLI)

**Scenario:** A product manager needs to update the existing specification for the "User Profile Service" (`specs/profile/profile_service.md`) and ensure it meets the accessibility baseline requirements defined in the configuration. The changes should be applied immediately after validation.

**Command:**

```bash
/smartspec_generate_spec \
  --spec specs/profile/profile_service.md \
  --apply
```

**Expected Result:**

1. The workflow loads `specs/profile/profile_service.md`.
2. It analyzes the content against the Spec Completeness Contract (e.g., checks for accessibility notes, NFRs).
3. A safe preview bundle is written to `.spec/reports/generate-spec/<run-id>/...`.
4. If no security violations (secrets) or mandatory failures are detected, the workflow proceeds with the governed write (`--apply`).
5. `specs/profile/profile_service.md` is updated in-place with refined content/structure.
6. The `.spec/SPEC_INDEX.json` is updated (if allowlisted) with the latest metadata.
7. Exit code `0` (Success).

### Use Case 2: Generating a Preview for Multiple Specs (Kilo Code)

**Scenario:** A CI pipeline needs to validate two newly created specifications identified by IDs `FEAT-1001` and `BUG-045` before they are merged. The pipeline requires the output in JSON format for downstream processing but must *not* apply any changes to the source files.

**Command (Kilo Code Snippet):**

```bash
/smartspec_generate_spec.md \
  --spec-ids FEAT-1001,BUG-045 \
  --json \
  --out /tmp/spec_validation_report \
  --platform kilo
```

**Expected Result:**

1. The workflow resolves `FEAT-1001` and `BUG-045` paths using `.spec/SPEC_INDEX.json`.
2. It performs completeness and duplication checks for both specs.
3. A safe preview bundle is written to `/tmp/spec_validation_report/<run-id>/...`.
4. The primary output is a `summary.json` file containing validation results, security checks, and next steps.
5. No files under `specs/**` or `.spec/SPEC_INDEX.json` are modified.
6. Exit code `0` (Success).

### Use Case 3: Refusing Application Due to Secret Leakage (CLI)

**Scenario:** A user attempts to refine a spec, but the generated content (preview) accidentally includes a string matching a configured redaction pattern (e.g., a test API key).

**Command:**

```bash
/smartspec_generate_spec \
  --spec specs/new_feature.md \
  --apply
```

**Expected Result:**

1. The workflow generates the preview content.
2. The content matches a configured redaction pattern (`safety.redaction`).
3. The workflow redacts the value in the preview/report output.
4. The workflow **refuses** to proceed with the `--apply` operation, as mandated by the Secret-blocking rule.
5. A detailed `report.md` is generated, noting the secret detection and apply refusal.
6. Exit code `1` (Validation Fail).

### Use Case 4: Creating a New Specification from Scratch (CLI)

**Scenario:** A developer wants to create a new specification for a "Payment Gateway Integration" feature. The spec file doesn't exist yet, so the workflow will create it based on the completeness contract.

**Command:**

```bash
/smartspec_generate_spec \
  --spec specs/integrations/payment_gateway.md \
  --apply
```

**Expected Result:**

1. The workflow detects that `specs/integrations/payment_gateway.md` does not exist.
2. It generates a new spec with all required sections (user stories, journeys, UI/UX baseline, NFRs, etc.).
3. A preview is written to `.spec/reports/generate-spec/<run-id>/...`.
4. With `--apply`, the new spec file is created at `specs/integrations/payment_gateway.md`.
5. The `.spec/SPEC_INDEX.json` is updated with the new spec entry (if allowlisted).
6. Exit code `0` (Success).

### Use Case 5: Detecting Duplicate Specifications (Kilo Code)

**Scenario:** A team member attempts to create a new spec for "User Authentication", but a similar spec already exists in the index. The workflow should detect this duplication and provide guidance.

**Command (Kilo Code Snippet):**

```bash
/smartspec_generate_spec.md \
  --spec specs/auth/user_authentication.md \
  --platform kilo
```

**Expected Result:**

1. The workflow loads `.spec/SPEC_INDEX.json` and computes similarity against existing specs.
2. It detects a strong match with an existing spec (e.g., `specs/security/authentication_service.md`).
3. A **Reuse Warning** section is added to the preview.
4. A decision record is created in `references/decisions.md` recommending consolidation.
5. The workflow does not auto-merge specs but provides guidance for manual review.
6. No governed writes occur (no `--apply` flag).
7. Exit code `0` (Success with warnings).

---

## 4. Parameters

The following parameters and flags control the execution and behavior of the `/smartspec_generate_spec` workflow.

### Required (One-of)

| Parameter | Type | Description | Validation |
| :--- | :--- | :--- | :--- |
| `--spec` | `<path>` | Path to a single spec file to refine. | Must resolve under `specs/**`. Cannot be used with `--spec-ids`. |
| `--spec-ids` | `<csv>` | Comma-separated list of spec IDs to refine. | IDs must match `safety.spec_id_regex` and exist in `.spec/SPEC_INDEX.json`. Cannot be used with `--spec`. |

### Universal Flags

| Flag | Description | Default | Platform Support |
| :--- | :--- | :--- | :--- |
| `--config` | Path to the SmartSpec configuration file. | `.spec/smartspec.config.yaml` | `cli` \| `kilo` \| `ci` \| `other` |
| `--lang` | Language for report generation (e.g., `th`, `en`). | (System default) | `cli` \| `kilo` \| `ci` \| `other` |
| `--platform` | Execution platform context. **Required for Kilo Code.** | (Inferred) | `cli` \| `kilo` \| `ci` \| `other` |
| `--apply` | Enables governed writes (modifying `specs/**` and potentially the index). | `false` | `cli` \| `kilo` \| `ci` \| `other` |
| `--out` | Base path for safe outputs (reports/previews). | `.spec/reports/generate-spec/` | `cli` \| `kilo` \| `ci` \| `other` |
| `--json` | Output the primary summary in JSON format (`summary.json`). | `false` | `cli` \| `kilo` \| `ci` \| `other` |
| `--quiet` | Suppress standard output logs. | `false` | `cli` \| `kilo` \| `ci` \| `other` |

### Workflow-Specific Flags

| Flag | Description | Platform Support |
| :--- | :--- | :--- |
| `--spec` | Path to a single spec file to refine. (See Required Inputs) | `cli` \| `kilo` \| `ci` \| `other` |
| `--spec-ids` | Comma-separated list of spec IDs to refine. (See Required Inputs) | `cli` \| `kilo` \| `ci` \| `other` |

---

## 5. Output

The workflow generates two types of output artifacts: Safe Preview Bundles (always) and Governed Artifacts (only with `--apply`).

### Safe Preview Bundle (Always Generated)

A unique run folder is created under the report path (default: `.spec/reports/generate-spec/<run-id>/`).

**Contents:**

| File Path | Description |
| :--- | :--- |
| `preview.md` | The refined spec content (before apply). |
| `diff.md` | A diff showing changes from the current version. |
| `summary.json` | (If `--json` is used) Structured validation results. |
| `report.md` | Detailed analysis including completeness checks, reuse warnings, and security scan results. |

### Governed Artifacts (Only with `--apply`)

| File Path | Description |
| :--- | :--- |
| `specs/**/*.md` | The refined spec file(s) written to the governed location. |
| `.spec/SPEC_INDEX.json` | Updated spec index (only if allowlisted in config). |

---

## 6. Notes

- **SPEC-first Governance:** This workflow enforces strict governance principles. Always review the preview bundle before using `--apply`.
- **Reuse-first Behavior:** The workflow actively detects duplication and encourages consolidation over creating redundant specs.
- **Secret Protection:** Any content matching configured redaction patterns will block the `--apply` operation to prevent accidental secret leakage.
- **Network Policy:** This workflow respects `safety.network_policy.default=deny` and does not make external network requests.
- **Symlink Safety:** If `safety.disallow_symlink_writes=true`, the workflow will refuse writes through symlinks.
- **Kilo Code Platform:** When using Kilo Code, always include `--platform kilo` to ensure proper context and logging.

---

**End of Manual**
