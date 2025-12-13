| manual_name | manual_version | compatible_workflow | compatible_workflow_versions |
|-------------|----------------|---------------------|------------------------------|
| /smartspec_generate_spec_from_prompt Manual (EN) | 6.0 | /smartspec_generate_spec_from_prompt | 6.0.x |

# /smartspec_generate_spec_from_prompt Manual (v6.0, English)

## 1. Overview

This manual explains how to use the workflow:

The `/smartspec_generate_spec_from_prompt` workflow generates **one or more starter specs** from a natural-language requirement prompt **with reuse-first intelligence**.

**Purpose:** Generate one or more starter specs from a natural-language requirement prompt with reuse-first intelligence. This workflow detects overlaps against the spec index, prefers reuse over duplication, and produces UX/UI-ready specs suitable for production planning.

**Version:** 6.0.1  
**Category:** spec-gen

---

## 2. Usage

This workflow supports invocation via the Command Line Interface (CLI) and Kilo Code (internal scripting environment).

### 🔗 CLI Usage

The CLI invocation requires specifying a natural-language prompt describing the desired specification.

```bash
/smartspec_generate_spec_from_prompt \
  --prompt "<requirement_description>" \
  [--category <category>] \
  [--update-index] \
  [--json] \
  [--apply]
```

### Kilo Code Usage

The Kilo Code invocation is identical to the CLI structure, typically used within automated pipelines or internal scripts.

**Important:** When using Kilo Code, you MUST include `--platform kilo` flag.

```bash
/smartspec_generate_spec_from_prompt.md \
  --prompt "<requirement_description>" \
  [--category <category>] \
  [--update-index] \
  [--json] \
  [--apply] \
  --platform kilo
```

---

## 3. Use Cases

### Use Case 1: Generating a Spec from a Simple Prompt (CLI)

**Scenario:** A product manager wants to create a specification for a new "Password Reset" feature based on a brief description.

**Command:**

```bash
/smartspec_generate_spec_from_prompt \
  --prompt "Users should be able to reset their password via email link with 24-hour expiration"
```

**Expected Result:**

1. The workflow analyzes the prompt and identifies key requirements.
2. It checks `.spec/SPEC_INDEX.json` for similar existing specs.
3. A preview bundle is written to `.spec/reports/spec-from-prompt/<run-id>/`.
4. The preview includes one or more starter specs with UX/UI baseline sections.
5. No governed writes occur (no `--apply` flag).
6. Exit code `0` (Success).

### Use Case 2: Creating a Spec with Category and Index Update (Kilo Code)

**Scenario:** A CI pipeline needs to generate a spec for a new "Payment Gateway Integration" feature, categorize it under "integrations", and update the spec index immediately.

**Command (Kilo Code Snippet):**

```bash
/smartspec_generate_spec_from_prompt.md \
  --prompt "Integrate Stripe payment gateway with support for credit cards, Apple Pay, and Google Pay" \
  --category integrations \
  --update-index \
  --apply \
  --platform kilo
```

**Expected Result:**

1. The workflow generates a spec based on the prompt.
2. The spec is categorized under `specs/integrations/`.
3. A preview bundle is written to `.spec/reports/spec-from-prompt/<run-id>/`.
4. With `--apply`, the spec folder and files are created.
5. With `--update-index`, the `.spec/SPEC_INDEX.json` is updated (if allowlisted).
6. Exit code `0` (Success).

### Use Case 3: Detecting Reuse Opportunities (CLI)

**Scenario:** A developer wants to create a spec for "User Profile Management", but a similar "User Profile Service" spec already exists. The workflow should detect this and suggest reuse.

**Command:**

```bash
/smartspec_generate_spec_from_prompt \
  --prompt "Allow users to view and edit their profile information including name, email, and avatar" \
  --json
```

**Expected Result:**

1. The workflow analyzes the prompt and scans `.spec/SPEC_INDEX.json`.
2. It detects an existing "User Profile Service" spec with similar purpose.
3. The preview includes a **Reuse Recommendation** section.
4. The output `summary.json` contains reuse suggestions with spec IDs.
5. No governed writes occur (no `--apply` flag).
6. Exit code `0` (Success with recommendations).

### Use Case 4: Generating Multiple Specs from Complex Prompt (CLI)

**Scenario:** A product manager provides a complex prompt describing multiple related features. The workflow should generate separate specs for each feature.

**Command:**

```bash
/smartspec_generate_spec_from_prompt \
  --prompt "Build a notification system with email, SMS, and push notifications. Include user preferences for notification channels and delivery schedules." \
  --apply
```

**Expected Result:**

1. The workflow analyzes the prompt and identifies multiple distinct features.
2. It generates separate specs: "Notification Service", "Notification Preferences", "Notification Delivery".
3. Each spec includes UX/UI baseline sections and references to related specs.
4. A preview bundle is written to `.spec/reports/spec-from-prompt/<run-id>/`.
5. With `--apply`, all spec folders and files are created.
6. Exit code `0` (Success).

### Use Case 5: Refusing Application Due to Secret Leakage (CLI)

**Scenario:** A user provides a prompt that accidentally includes a database connection string. The workflow should detect this and refuse to apply the spec.

**Command:**

```bash
/smartspec_generate_spec_from_prompt \
  --prompt "Create API service connecting to postgres://user:pass@db.example.com/prod" \
  --apply
```

**Expected Result:**

1. The workflow generates a spec preview.
2. The content matches a configured redaction pattern (e.g., database credentials).
3. The workflow redacts the value in the preview/report output.
4. The workflow **refuses** to proceed with the `--apply` operation.
5. A detailed `report.md` is generated, noting the secret detection.
6. Exit code `1` (Validation Fail).

---

## 4. Parameters

The following parameters and flags control the execution and behavior of the `/smartspec_generate_spec_from_prompt` workflow.

### Required Parameters

| Parameter | Type | Description | Validation |
| :--- | :--- | :--- | :--- |
| `--prompt` | `<string>` | Natural-language description of the desired specification. | Must not be empty. |

### Universal Flags

| Flag | Description | Default | Platform Support |
| :--- | :--- | :--- | :--- |
| `--config` | Path to the SmartSpec configuration file. | `.spec/smartspec.config.yaml` | `cli` \| `kilo` \| `ci` \| `other` |
| `--lang` | Language for report generation (e.g., `th`, `en`). | (System default) | `cli` \| `kilo` \| `ci` \| `other` |
| `--platform` | Execution platform context. **Required for Kilo Code.** | (Inferred) | `cli` \| `kilo` \| `ci` \| `other` |
| `--apply` | Enables governed writes (creating spec folders and files). | `false` | `cli` \| `kilo` \| `ci` \| `other` |
| `--out` | Base path for safe outputs (reports/previews). | `.spec/reports/spec-from-prompt/` | `cli` \| `kilo` \| `ci` \| `other` |
| `--json` | Output the primary summary in JSON format (`summary.json`). | `false` | `cli` \| `kilo` \| `ci` \| `other` |
| `--quiet` | Suppress standard output logs. | `false` | `cli` \| `kilo` \| `ci` \| `other` |

### Workflow-Specific Flags

| Flag | Description | Default | Platform Support |
| :--- | :--- | :--- | :--- |
| `--category` | Target category for the generated spec(s). | (Auto-inferred) | `cli` \| `kilo` \| `ci` \| `other` |
| `--update-index` | Update `.spec/SPEC_INDEX.json` with new spec entries (requires `--apply`). | `false` | `cli` \| `kilo` \| `ci` \| `other` |

---

## 5. Output

The workflow generates two types of output artifacts: Safe Preview Bundles (always) and Governed Artifacts (only with `--apply`).

### Safe Preview Bundle (Always Generated)

A unique run folder is created under the report path (default: `.spec/reports/spec-from-prompt/<run-id>/`).

**Contents:**

| File Path | Description |
| :--- | :--- |
| `preview/<spec-id>/spec.md` | The generated spec content (before apply). |
| `summary.json` | (If `--json` is used) Structured spec metadata and reuse recommendations. |
| `report.md` | Detailed analysis including reuse detection and security scan results. |
| `references.yaml` | Structured references to related specs and external resources. |

### Governed Artifacts (Only with `--apply`)

| File Path | Description |
| :--- | :--- |
| `specs/<category>/<spec-id>/spec.md` | The generated spec file(s) written to the governed location. |
| `.spec/SPEC_INDEX.json` | Updated spec index (only if `--update-index` and allowlisted). |

---

## 6. Notes

- **Reuse-first Intelligence:** The workflow actively detects overlaps with existing specs and recommends reuse over duplication.
- **UX/UI-ready Specs:** Generated specs include all required sections for production planning (states, accessibility, responsive design, microcopy).
- **Multiple Specs:** Complex prompts may result in multiple related specs being generated.
- **Reference Capture:** External references (UX/UI/API) are captured in a structured, auditable format.
- **Secret Protection:** Any content matching configured redaction patterns will block the `--apply` operation.
- **Network Policy:** This workflow respects `safety.network_policy.default=deny` and does not make external network requests.
- **Index Update:** Use `--update-index` with `--apply` to automatically update the spec index (requires allowlist configuration).
- **Kilo Code Platform:** When using Kilo Code, always include `--platform kilo` to ensure proper context and logging.

---

**End of Manual**
