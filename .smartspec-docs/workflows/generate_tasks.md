| manual_name | manual_version | compatible_workflow | compatible_workflow_versions |
|-------------|----------------|---------------------|------------------------------|
| /smartspec_generate_tasks Manual (EN) | 6.0 | /smartspec_generate_tasks | 6.0.x |

# /smartspec_generate_tasks Manual (v6.0, English)

## 1. Overview

This manual explains how to use the workflow:

The `/smartspec_generate_tasks` workflow generates or refines `tasks.md` from `spec.md` (or `plan.md`) in a **verification-ready** format.

**Purpose:** Convert spec.md (or plan.md) → tasks.md (verification-ready; preserves IDs/checkboxes; reports always written). This workflow is the canonical source for creating tasks that downstream workflows can trust, including verify_tasks_progress_strict, report_implement_prompter, and quality_gate.

**Version:** 6.0.2  
**Category:** core

---

## 2. Usage

This workflow supports invocation via the Command Line Interface (CLI) and Kilo Code (internal scripting environment).

### 🔗 CLI Usage

The CLI invocation requires specifying the target spec.md or plan.md file as a positional argument.

```bash
/smartspec_generate_tasks <spec_or_plan_md> \
  [--json] \
  [--apply]
```

### Kilo Code Usage

The Kilo Code invocation is identical to the CLI structure, typically used within automated pipelines or internal scripts.

**Important:** When using Kilo Code, you MUST include `--platform kilo` flag.

```bash
/smartspec_generate_tasks.md \
  <spec_or_plan_md> \
  [--json] \
  [--apply] \
  --platform kilo
```

---

## 3. Use Cases

### Use Case 1: Generating Tasks from a Specification (CLI)

**Scenario:** A developer has completed a specification for a "User Authentication Service" (`specs/auth/user_auth_service/spec.md`) and needs to generate an actionable task list for implementation.

**Command:**

```bash
/smartspec_generate_tasks specs/auth/user_auth_service/spec.md
```

**Expected Result:**

1. The workflow loads `specs/auth/user_auth_service/spec.md`.
2. It analyzes the spec content and generates verification-ready tasks.
3. A preview bundle is written to `.spec/reports/generate-tasks/<run-id>/`.
4. The preview includes `tasks_preview.md` with unique task IDs and evidence hooks.
5. No governed writes occur (no `--apply` flag).
6. Exit code `0` (Success).

### Use Case 2: Generating Tasks from a Plan (Kilo Code)

**Scenario:** A CI pipeline has generated a plan file (`specs/payments/checkout/plan.md`) and needs to create tasks based on the plan phases. The tasks should be applied immediately.

**Command (Kilo Code Snippet):**

```bash
/smartspec_generate_tasks.md \
  specs/payments/checkout/plan.md \
  --apply \
  --platform kilo
```

**Expected Result:**

1. The workflow loads `specs/payments/checkout/plan.md`.
2. It locates the sibling `spec.md` for richer context.
3. Tasks are generated based on plan phases with proper dependencies.
4. A preview bundle is written to `.spec/reports/generate-tasks/<run-id>/`.
5. With `--apply`, the tasks file is written to `specs/payments/checkout/tasks.md`.
6. Exit code `0` (Success).

### Use Case 3: Refining Existing Tasks (Preserving Checkboxes) (CLI)

**Scenario:** A team has partially completed tasks in `specs/notifications/email_service/tasks.md`. The spec was updated with new requirements, and the tasks need to be regenerated while preserving completed checkboxes.

**Command:**

```bash
/smartspec_generate_tasks specs/notifications/email_service/spec.md \
  --apply
```

**Expected Result:**

1. The workflow loads the existing `specs/notifications/email_service/tasks.md`.
2. It identifies completed tasks (checked checkboxes) by their unique IDs.
3. New tasks are generated based on the updated spec.
4. Completed tasks are preserved with their checkboxes intact.
5. Obsolete tasks are marked as deprecated rather than deleted.
6. The updated `tasks.md` is written with `--apply`.
7. Exit code `0` (Success).

### Use Case 4: JSON Output for Programmatic Processing (CLI)

**Scenario:** A developer needs to integrate task generation into a custom tool that requires structured JSON output for downstream processing.

**Command:**

```bash
/smartspec_generate_tasks specs/api/rest_api/spec.md \
  --json
```

**Expected Result:**

1. The workflow loads `specs/api/rest_api/spec.md`.
2. Tasks are generated in verification-ready format.
3. A preview bundle is written to `.spec/reports/generate-tasks/<run-id>/`.
4. The output includes `summary.json` with structured task metadata.
5. No governed writes occur (no `--apply` flag).
6. Exit code `0` (Success).

### Use Case 5: Refusing Application Due to Secret Leakage (CLI)

**Scenario:** A user attempts to generate tasks, but the spec content accidentally includes an API key. The workflow should detect this and refuse to apply the tasks.

**Command:**

```bash
/smartspec_generate_tasks specs/integrations/third_party_api/spec.md \
  --apply
```

**Expected Result:**

1. The workflow loads `specs/integrations/third_party_api/spec.md`.
2. It generates tasks preview.
3. The content matches a configured redaction pattern (e.g., API key).
4. The workflow redacts the value in the preview/report output.
5. The workflow **refuses** to proceed with the `--apply` operation.
6. A detailed `report.md` is generated, noting the secret detection.
7. Exit code `1` (Validation Fail).

---

## 4. Parameters

The following parameters and flags control the execution and behavior of the `/smartspec_generate_tasks` workflow.

### Required Parameters

| Parameter | Type | Description | Validation |
| :--- | :--- | :--- | :--- |
| `<spec_or_plan_md>` | `<path>` | Path to spec.md or plan.md file to generate tasks from. | Must resolve under `specs/**` and must not escape via symlink. |

### Universal Flags

| Flag | Description | Default | Platform Support |
| :--- | :--- | :--- | :--- |
| `--config` | Path to the SmartSpec configuration file. | `.spec/smartspec.config.yaml` | `cli` \| `kilo` \| `ci` \| `other` |
| `--lang` | Language for report generation (e.g., `th`, `en`). | (System default) | `cli` \| `kilo` \| `ci` \| `other` |
| `--platform` | Execution platform context. **Required for Kilo Code.** | (Inferred) | `cli` \| `kilo` \| `ci` \| `other` |
| `--apply` | Enables governed writes (modifying `specs/**/tasks.md`). | `false` | `cli` \| `kilo` \| `ci` \| `other` |
| `--out` | Base path for safe outputs (reports/previews). | `.spec/reports/generate-tasks/` | `cli` \| `kilo` \| `ci` \| `other` |
| `--json` | Output the primary summary in JSON format (`summary.json`). | `false` | `cli` \| `kilo` \| `ci` \| `other` |
| `--quiet` | Suppress standard output logs. | `false` | `cli` \| `kilo` \| `ci` \| `other` |

---

## 5. Output

The workflow generates two types of output artifacts: Safe Preview Bundles (always) and Governed Artifacts (only with `--apply`).

### Safe Preview Bundle (Always Generated)

A unique run folder is created under the report path (default: `.spec/reports/generate-tasks/<run-id>/`).

**Contents:**

| File Path | Description |
| :--- | :--- |
| `tasks_preview.md` | The generated tasks content (before apply). |
| `summary.json` | (If `--json` is used) Structured task metadata and validation results. |
| `report.md` | Detailed analysis including task count, evidence hooks, and security scan results. |
| `diff.md` | (If refining existing tasks) Diff showing changes from current version. |

### Governed Artifacts (Only with `--apply`)

| File Path | Description |
| :--- | :--- |
| `specs/**/tasks.md` | The generated or refined tasks file written to the governed location. |

---

## 6. Notes

- **Verification-ready Format:** Tasks are generated with unique IDs and evidence hooks for downstream verification workflows.
- **Checkbox Preservation:** When refining existing tasks, completed checkboxes are preserved based on task IDs.
- **Non-destructive Updates:** Obsolete tasks are marked as deprecated rather than deleted to maintain audit trail.
- **Secret Protection:** Any content matching configured redaction patterns will block the `--apply` operation.
- **Network Policy:** This workflow respects `safety.network_policy.default=deny` and does not make external network requests.
- **Symlink Safety:** If `safety.disallow_symlink_writes=true`, the workflow will refuse writes through symlinks.
- **Kilo Code Platform:** When using Kilo Code, always include `--platform kilo` to ensure proper context and logging.
- **Canonical Chain:** This workflow is part of the core SmartSpec chain: validate_index → generate_spec → generate_plan → **generate_tasks** → verify_tasks_progress_strict → sync_tasks_checkboxes → report_implement_prompter.

---

**End of Manual**
