# /smartspec_generate_plan Manual (v6.0, English)

## Overview

The `/smartspec_generate_plan` workflow (v6.0.5) is a core component of the SmartSpec toolchain responsible for converting a detailed specification (`spec.md`) into an actionable implementation plan (`plan.md`).

This workflow operates in a **preview-first**, **dependency-aware**, and **reuse-first** manner, ensuring safety and governance before applying any changes. It is designed to generate a structured, phase-based plan that aligns with specified UI governance modes and adheres strictly to the SmartSpec governance contract and hardening requirements.

**Purpose:** Convert `spec.md` → `plan.md` (preview-first; dependency-aware; reuse-first; governed apply).
**Version:** 6.0.5

## Usage

### CLI Usage

The workflow is invoked via the command line, requiring the path to the target `spec.md` file as a positional argument.

```bash
/smartspec_generate_plan <spec_md> [--apply] [--ui-mode auto|json|inline] [--safety-mode strict|dev] [--plan-layout per-spec|consolidated] [--run-label "..."] [--json]
```

**Example (Preview Mode):**
To generate a plan preview for a specific specification in strict mode:
```bash
/smartspec_generate_plan specs/feature/user-auth/spec.md --ui-mode auto --safety-mode strict
```

**Example (Apply Mode):**
To generate and immediately write the plan, using the `dev` safety mode:
```bash
/smartspec_generate_plan specs/feature/user-auth/spec.md --apply --safety-mode dev
```

### Kilo Code Usage

For integration within SmartSpec's internal scripting environment (Kilo Code), the workflow is invoked using a specific syntax.

```bash
/smartspec_generate_plan.md \
  specs/<category>/<spec-id>/spec.md \
  --kilocode \
  [--apply] [--ui-mode auto|json|inline] [--safety-mode strict|dev] [--plan-layout per-spec|consolidated] [--run-label "..."] [--json]
```

**Example (Kilo Code):**
```kilocode
# Generate plan for the search feature, ensuring consolidated layout
/smartspec_generate_plan.md specs/core/search-engine/spec.md \
  --kilocode \
  --plan-layout consolidated \
  --ui-mode json
```

## Use Cases

### Use Case 1: Generating a New Plan (Preview)

**Scenario:** A developer has just finished writing a new specification for a "Notification Service" and wants to review the generated implementation plan before committing to it. They require the default strict safety checks.

**CLI Command:**
```bash
/smartspec_generate_plan specs/service/notification-service/spec.md --ui-mode auto --run-label "Initial Review"
```

**Expected Result:**
1.  No changes are made to `specs/service/notification-service/plan.md`.
2.  A new report folder is created, e.g., `.spec/reports/generate-plan/<run-id>/`.
3.  The folder contains:
    *   `preview/notification-service/plan.md` (the proposed plan).
    *   `report.md` detailing the inputs, safety status (`SAFE` or `UNSAFE`), and reuse summary.
    *   If the plan is marked `UNSAFE`, `report.md` will list blockers and Phase 0 remediation steps.

**Kilo Code Command:**
```kilocode
/smartspec_generate_plan.md specs/service/notification-service/spec.md \
  --kilocode \
  --ui-mode auto \
  --run-label "Initial Review"
```

### Use Case 2: Applying a Plan with Developer Override

**Scenario:** The plan generated in the preview was marked `UNSAFE` because of ambiguous registry references. The developer, understanding the risk, chooses to proceed in `dev` mode to allow the plan to be written with explicit TODOs for the ambiguities.

**CLI Command:**
```bash
/smartspec_generate_plan specs/service/notification-service/spec.md --apply --safety-mode dev
```

**Expected Result:**
1.  The workflow proceeds, marking the plan internally as `safety_status=DEV-ONLY`.
2.  The file `specs/service/notification-service/plan.md` is updated atomically.
3.  The generated `plan.md` includes the header block with `safety_status: DEV-ONLY`.
4.  Ambiguous items are replaced with explicit TODOs within the plan phases.
5.  A summary report is still generated in the reports directory.

**Kilo Code Command:**
```kilocode
/smartspec_generate_plan.md specs/service/notification-service/spec.md \
  --kilocode \
  --apply \
  --safety-mode dev
```

### Use Case 3: Redrafting an Existing Plan (Non-Destructive Merge)

**Scenario:** The original `plan.md` for the "Payment Gateway" feature contains manual notes added by the team. The underlying `spec.md` was slightly modified. The team needs to regenerate the plan while preserving their manual notes.

**CLI Command:**
```bash
/smartspec_generate_plan specs/finance/payment-gateway/spec.md --apply --safety-mode strict
```

**Expected Result:**
1.  The workflow reads the existing `plan.md`.
2.  The new plan is generated, attempting to merge changes non-destructively.
3.  User-authored sections and notes are preserved where possible.
4.  If a phase is no longer relevant due to spec changes, it is marked as `Deprecated` in the updated `plan.md`, not silently deleted.
5.  The updated `plan.md` is written to disk.

## Parameters

The following parameters (flags) control the behavior and output of the `/smartspec_generate_plan` workflow.

| Flag | Category | Description | Default | Values | Required |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **spec\_md** | Positional Input | Path to the `spec.md` file under `specs/**`. | N/A | File path | Yes |
| **--apply** | Universal | If present, the generated plan is written to `specs/**/plan.md`. Otherwise, only a safe preview is generated. | (Absent) | Boolean | No |
| **--ui-mode** | Workflow Specific | Governs how the plan handles UI components and review sequencing. | `auto` | `auto`, `json`, `inline` | No |
| **--safety-mode** | Workflow Specific | Controls the strictness of checks against registries and dependencies. | `strict` | `strict`, `dev` | No |
| **--plan-layout** | Workflow Specific | Defines how the plan structure is organized (relevant for multi-spec projects). | `per-spec` | `per-spec`, `consolidated` | No |
| **--run-label** | Workflow Specific | An optional string label to identify the current run in reports. | (None) | String | No |
| **--json** | Universal | If present, outputs the run summary as a JSON object to stdout and generates `summary.json`. | (Absent) | Boolean | No |
| **--config** | Universal | Path to the SmartSpec configuration file. | `.spec/smartspec.config.yaml` | File path | No |
| **--lang** | Universal | Language setting for outputs (e.g., reports). | (System default) | `th`, `en` | No |
| **--platform** | Universal | Contextual platform identifier for the run. | `cli` | `cli`, `kilo`, `ci`, `other` | No |
| **--out** | Universal | Base directory for safe report outputs. | `.spec/reports/generate-plan/` | Directory path | No |
| **--quiet** | Universal | Suppress non-critical output to stdout. | (Absent) | Boolean | No |

## Output

The workflow produces safe preview bundles regardless of the `--apply` flag, and conditionally writes the governed artifact.

### Safe Preview Bundle (Always)

All safe outputs are written under a unique run folder, typically located at `.spec/reports/generate-plan/<run-id>/`.

| Artifact | Location | Description |
| :--- | :--- | :--- |
| **Preview Plan** | `<run-id>/preview/<spec-id>/plan.md` | The full, proposed `plan.md` content. |
| **Diff Patch** | `<run-id>/diff/<spec-id>.patch` | A best-effort patch file showing changes against the existing `plan.md`. |
| **Report** | `<run-id>/report.md` | A human-readable report detailing inputs, modes, safety status, reuse summary, blockers, and next steps. |
| **Summary JSON** | `<run-id>/summary.json` |