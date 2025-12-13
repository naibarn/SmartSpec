| manual_name | manual_version | compatible_workflow | compatible_workflow_versions |
|-------------|----------------|---------------------|------------------------------|
| /smartspec_generate_plan Manual (EN) | 6.0 | /smartspec_generate_plan | 6.0.x |

# /smartspec_generate_plan Manual (v6.0, English)

## 1. Overview

This manual explains how to use the workflow:

The `/smartspec_generate_plan` workflow generates or refines `plan.md` from `spec.md` in a **dependency-aware**, **reuse-first**, **safe-by-default** way.

**Purpose:** Convert spec.md → plan.md (preview-first; dependency-aware; reuse-first; governed apply). This workflow sits in the canonical chain between spec generation and task generation, ensuring that implementation plans are properly structured and validated before execution.

**Version:** 6.0.5  
**Category:** core

---

## 2. Usage

This workflow supports invocation via the Command Line Interface (CLI) and Kilo Code (internal scripting environment).

### 🔗 CLI Usage

The CLI invocation requires specifying the target spec.md file as a positional argument.

```bash
/smartspec_generate_plan <spec_md> \
  [--apply] \
  [--ui-mode auto|json|inline] \
  [--safety-mode strict|dev] \
  [--plan-layout per-spec|consolidated] \
  [--run-label "..."] \
  [--json]
```

### Kilo Code Usage

The Kilo Code invocation is identical to the CLI structure, typically used within automated pipelines or internal scripts.

**Important:** When using Kilo Code, you MUST include `--platform kilo` flag.

```bash
/smartspec_generate_plan.md \
  <spec_md> \
  [--apply] \
  [--ui-mode auto|json|inline] \
  [--safety-mode strict|dev] \
  [--plan-layout per-spec|consolidated] \
  [--run-label "..."] \
  [--json] \
  --platform kilo
```

---

## 3. Use Cases

### Use Case 1: Generating a Plan from a New Specification (CLI)

**Scenario:** A product manager has just created a new specification for a "Notification Service" (`specs/services/notification_service/spec.md`) and needs to generate an implementation plan. The plan should be reviewed before being applied.

**Command:**

```bash
/smartspec_generate_plan specs/services/notification_service/spec.md
```

**Expected Result:**

1. The workflow loads `specs/services/notification_service/spec.md`.
2. It analyzes the spec content and identifies implementation phases.
3. A preview bundle is written to `.spec/reports/generate-plan/<run-id>/`.
4. The preview includes `plan_preview.md` with dependency-aware phase ordering.
5. No governed writes occur (no `--apply` flag).
6. Exit code `0` (Success).

### Use Case 2: Applying a Plan with UI Mode Configuration (Kilo Code)

**Scenario:** A CI pipeline needs to generate and apply a plan for a spec with JSON-based UI components. The plan should enforce JSON UI mode and be applied immediately after validation.

**Command (Kilo Code Snippet):**

```bash
/smartspec_generate_plan.md \
  specs/ui/dashboard/spec.md \
  --apply \
  --ui-mode json \
  --platform kilo
```

**Expected Result:**

1. The workflow loads `specs/ui/dashboard/spec.md`.
2. It generates a plan with UI phases configured for JSON mode.
3. A preview bundle is written to `.spec/reports/generate-plan/<run-id>/`.
4. With `--apply`, the plan is written to `specs/ui/dashboard/plan.md`.
5. The plan includes proper UI governance annotations.
6. Exit code `0` (Success).

### Use Case 3: Detecting Reuse Opportunities (CLI)

**Scenario:** A developer is creating a plan for a new "Payment Processing" feature. The workflow should detect that a similar "Payment Gateway" component already exists in the spec index and suggest reuse.

**Command:**

```bash
/smartspec_generate_plan specs/payments/payment_processing/spec.md \
  --json
```

**Expected Result:**

1. The workflow loads `.spec/SPEC_INDEX.json` and scans for similar components.
2. It detects an existing "Payment Gateway" component.
3. The preview includes a **Reuse Recommendation** section.
4. The output `summary.json` contains reuse suggestions with component IDs.
5. No governed writes occur (no `--apply` flag).
6. Exit code `0` (Success with recommendations).

### Use Case 4: Consolidated Plan Layout for Multi-Spec Projects (Kilo Code)

**Scenario:** A team is working on a large project with multiple related specs. They need a consolidated plan that combines all specs into a single implementation roadmap.

**Command (Kilo Code Snippet):**

```bash
/smartspec_generate_plan.md \
  specs/project/main_spec.md \
  --apply \
  --plan-layout consolidated \
  --run-label "Q1-2024-Release" \
  --platform kilo
```

**Expected Result:**

1. The workflow loads `specs/project/main_spec.md` and related specs.
2. It generates a consolidated plan with all phases merged and dependency-ordered.
3. The plan includes a run label "Q1-2024-Release" for tracking.
4. A preview bundle is written to `.spec/reports/generate-plan/<run-id>/`.
5. With `--apply`, the consolidated plan is written to `specs/project/plan.md`.
6. Exit code `0` (Success).

### Use Case 5: Refusing Application Due to Secret Leakage (CLI)

**Scenario:** A user attempts to generate a plan, but the spec content accidentally includes a database connection string. The workflow should detect this and refuse to apply the plan.

**Command:**

```bash
/smartspec_generate_plan specs/backend/api_service/spec.md \
  --apply
```

**Expected Result:**

1. The workflow loads `specs/backend/api_service/spec.md`.
2. It generates a plan preview.
3. The content matches a configured redaction pattern (e.g., database credentials).
4. The workflow redacts the value in the preview/report output.
5. The workflow **refuses** to proceed with the `--apply` operation.
6. A detailed `report.md` is generated, noting the secret detection.
7. Exit code `1` (Validation Fail).

---

## 4. Parameters

The following parameters and flags control the execution and behavior of the `/smartspec_generate_plan` workflow.

### Required Parameters

| Parameter | Type | Description | Validation |
| :--- | :--- | :--- | :--- |
| `<spec_md>` | `<path>` | Path to the spec.md file to generate a plan from. | Must resolve under `specs/**` and must not escape via symlink. |

### Universal Flags

| Flag | Description | Default | Platform Support |
| :--- | :--- | :--- | :--- |
| `--config` | Path to the SmartSpec configuration file. | `.spec/smartspec.config.yaml` | `cli` \| `kilo` \| `ci` \| `other` |
| `--lang` | Language for report generation (e.g., `th`, `en`). | (System default) | `cli` \| `kilo` \| `ci` \| `other` |
| `--platform` | Execution platform context. **Required for Kilo Code.** | (Inferred) | `cli` \| `kilo` \| `ci` \| `other` |
| `--apply` | Enables governed writes (modifying `specs/**/plan.md`). | `false` | `cli` \| `kilo` \| `ci` \| `other` |
| `--out` | Base path for safe outputs (reports/previews). | `.spec/reports/generate-plan/` | `cli` \| `kilo` \| `ci` \| `other` |
| `--json` | Output the primary summary in JSON format (`summary.json`). | `false` | `cli` \| `kilo` \| `ci` \| `other` |
| `--quiet` | Suppress standard output logs. | `false` | `cli` \| `kilo` \| `ci` \| `other` |

### Workflow-Specific Flags

| Flag | Description | Default | Platform Support |
| :--- | :--- | :--- | :--- |
| `--ui-mode` | UI governance mode (`auto`, `json`, `inline`). | `auto` | `cli` \| `kilo` \| `ci` \| `other` |
| `--safety-mode` | Safety validation level (`strict`, `dev`). | `strict` | `cli` \| `kilo` \| `ci` \| `other` |
| `--plan-layout` | Plan structure (`per-spec`, `consolidated`). | `per-spec` | `cli` \| `kilo` \| `ci` \| `other` |
| `--run-label` | Custom label for this plan generation run. | (Auto-generated) | `cli` \| `kilo` \| `ci` \| `other` |

---

## 5. Output

The workflow generates two types of output artifacts: Safe Preview Bundles (always) and Governed Artifacts (only with `--apply`).

### Safe Preview Bundle (Always Generated)

A unique run folder is created under the report path (default: `.spec/reports/generate-plan/<run-id>/`).

**Contents:**

| File Path | Description |
| :--- | :--- |
| `plan_preview.md` | The generated plan content (before apply). |
| `dependency_graph.md` | Visual representation of phase dependencies. |
| `summary.json` | (If `--json` is used) Structured plan metadata and validation results. |
| `report.md` | Detailed analysis including reuse recommendations and security scan results. |
| `patch.diff` | (If refining existing plan) Diff showing changes from current version. |

### Governed Artifacts (Only with `--apply`)

| File Path | Description |
| :--- | :--- |
| `specs/**/plan.md` | The generated or refined plan file written to the governed location. |

---

## 6. Notes

- **Preview-first:** Always review the preview bundle before using `--apply` to ensure the plan meets expectations.
- **Dependency-aware:** The workflow automatically orders phases based on explicit dependencies in the spec.
- **Reuse-first:** The workflow actively detects opportunities to reuse existing components from the spec index.
- **UI Mode Alignment:** Plan sequencing aligns with UI governance mode (`auto`, `json`, `inline`).
- **Secret Protection:** Any content matching configured redaction patterns will block the `--apply` operation.
- **Network Policy:** This workflow respects `safety.network_policy.default=deny` and does not make external network requests.
- **Symlink Safety:** If `safety.disallow_symlink_writes=true`, the workflow will refuse writes through symlinks.
- **Kilo Code Platform:** When using Kilo Code, always include `--platform kilo` to ensure proper context and logging.
- **Canonical Chain:** This workflow is part of the core SmartSpec chain: validate_index → generate_spec → **generate_plan** → generate_tasks → verify_tasks_progress_strict → sync_tasks_checkboxes → report_implement_prompter.

---

**End of Manual**
