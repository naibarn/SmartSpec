# /smartspec_generate_tests Manual (v6.0, English)

## Overview

The `/smartspec_generate_tests` workflow (v6.1.1) is a core component of SmartSpec's test planning and governance suite.

**Purpose:** To generate a comprehensive, SmartSpec-governed test plan (including test matrix, acceptance criteria, and required evidence) based on a primary specification (`spec.md`) and adjacent files (`tasks.md`, `ui.json`).

**Key Features:**

1.  **Governance Alignment:** Ensures the resulting test plan adheres to SmartSpec v6 governance standards, including strict security hardening and write scope enforcement.
2.  **Preview-First:** By default, it operates in a safe, reports-only mode, generating a detailed **Change Plan**. Application (writing the governed test plan) requires the `--apply` flag.
3.  **Comprehensive Scope:** Generates tests covering functional behavior, contracts, security, NFR/performance, observability, and UI components.
4.  **De-duplication:** Leverages registries and the `SPEC_INDEX` to avoid redundant tests and align with canonical definitions.

**Version:** 6.1.1

## Usage

This workflow supports both Command Line Interface (CLI) and Kilo Code execution. The primary input is the path to the `spec.md` file.

### CLI Usage

The workflow is invoked directly, passing the required positional argument first.

**Syntax:**

```bash
/smartspec_generate_tests <spec_md> [flags]
```

**Example (Reports Only):**

```bash
/smartspec_generate_tests specs/user-management/auth-service/spec.md \
  --mode strict \
  --plan-format both \
  --out .spec/reports/auth-test-run-1
```

**Example (Applying the Test Plan):**

```bash
/smartspec_generate_tests specs/user-management/auth-service/spec.md \
  --apply \
  --target-path specs/user-management/auth-service/testplan/v6_tests.md
```

### Kilo Code Usage

Kilo Code execution requires appending the `--kilocode` flag, which signals the environment to handle execution and output formatting appropriately.

**Syntax:**

```bash
/smartspec_generate_tests.md <spec_md> [flags] --kilocode
```

**Example (Reports Only):**

```bash
/smartspec_generate_tests.md specs/payment/checkout-flow/spec.md \
  --include-dependencies \
  --json \
  --kilocode
```

**Example (Applying the Test Plan):**

```bash
/smartspec_generate_tests.md specs/payment/checkout-flow/spec.md \
  --apply \
  --kilocode
```

---

## Use Cases

### Use Case 1: Generating a Test Plan for a New Feature (Reports Only)

**Scenario:** A new feature specification (`specs/api/v2/new-endpoint/spec.md`) has been written, along with detailed implementation tasks (`tasks.md`). The user wants to review the generated test plan and coverage gaps before committing the plan to the repository.

| Component | Detail |
| :--- | :--- |
| **Input Spec** | `specs/api/v2/new-endpoint/spec.md` |
| **Goal** | Generate a comprehensive preview in strict mode, including dependency checks. |

**CLI Command:**

```bash
/smartspec_generate_tests specs/api/v2/new-endpoint/spec.md \
  --strict \
  --include-dependencies \
  --plan-format both
```

**Expected Result:**

1.  Exit code `0` (unless strict mode blocks on a critical governance failure).
2.  A new report directory is created (e.g., `.spec/reports/generate-tests/<run-id>/`).
3.  The directory contains:
    *   `report.md` (detailed checks and summary).
    *   `change_plan.md` (stating that no files were written to governed paths).
    *   `tests.preview.md` and `tests.preview.json` (the full generated test matrix).
4.  The `report.md` includes a section detailing any **GT-201 Coverage Gaps** found.

### Use Case 2: Applying a Governed Test Plan

**Scenario:** The test plan for the Authentication Service (`specs/user-management/auth-service/spec.md`) has been reviewed and approved. The user needs to apply this plan, writing the final `tests.md` file into the designated `testplan` folder, ensuring the write operation is atomic and governed.

| Component | Detail |
| :--- | :--- |
| **Input Spec** | `specs/user-management/auth-service/spec.md` |
| **Goal** | Write the generated test plan to the governed path. |

**Kilo Code Command:**

```bash
/smartspec_generate_tests.md specs/user-management/auth-service/spec.md \
  --apply \
  --target-path testplan/auth_tests.md \
  --kilocode
```

**Expected Result:**

1.  The workflow performs preflight checks and generates the Change Plan.
2.  Since `--apply` is present, the Change Plan is executed.
3.  The file `specs/user-management/auth-service/testplan/auth_tests.md` is created atomically.
4.  The `summary.json` output confirms the governed write operation under the `writes.governed` array.

### Use Case 3: Generating a Plan with Overridden Input Paths

**Scenario:** A development team stores their UI specification (`ui_config.json`) and tasks (`dev_tasks.md`) in non-standard locations relative to the spec file.

| Component | Detail |
| :--- | :--- |
| **Input Spec** | `specs/frontend/dashboard/spec.md` |
| **Goal** | Generate a plan using specific paths for tasks and UI configuration. |

**CLI Command:**

```bash
/smartspec_generate_tests specs/frontend/dashboard/spec.md \
  --tasks ../../dev_tasks.md \
  --ui-json ./ui_config.json
```

**Expected Result:**

1.  The workflow successfully loads the specified `dev_tasks.md` and `ui_config.json`.
2.  The generated test matrix includes UI component tests derived from the provided `ui_config.json`.
3.  The `summary.json` confirms the non-default paths used in the `scope` object.

---

## Parameters

The `/smartspec_generate_tests` workflow accepts one required positional input and several optional flags.

### Positional Argument (Required)

| Parameter | Description |
| :--- | :--- |
| `<spec_md>` | The path to the primary specification file (e.g., `specs/<category>/<spec-id>/spec.md`). |

### Universal Flags (Governance and Environment)

| Flag | Description |
| :--- | :--- |
| `--config <path>` | Specifies the path to the SmartSpec configuration file. |
| `--lang <th|en>` | Sets the language for reports and generated content. |
| `--platform <cli|kilo|ci|other>` | Specifies the execution environment. |
| `--apply` | **MANDATORY for governed writes.** Executes the Change Plan, writing the test plan to the target path. |
| `--out <path>` | Overrides the default report output root (`.spec/reports/generate-tests/`). Must resolve under the configuration allowlist. |
| `--json` | Outputs the main report and change plan in JSON format in addition to Markdown. |
| `--quiet` | Suppresses non-critical console output. |

### Workflow-Specific Flags

| Flag | Description |
| :--- | :--- |
| `--tasks <path>` | Override the auto-discovered path for the adjacent `tasks.md` file (read-only). |
| `--ui-json <path>` | Override the auto-discovered path for the adjacent `ui.json` file (read-only). |
| `--mode <normal|strict>` | Sets the generation mode. Default is `normal`. |
| `--strict` | Alias for `--mode=strict`. In strict mode, missing required evidence hooks or registry misalignments result in a blocking failure (Exit Code 1). |
| `--plan-format <md|json|both>` | Specifies the format for the generated test plan preview files. Default is `md`. |
| `--target-path <path>` | Specifies the governed output path for the final `tests.md`. Only used with `--apply`. Default is `testplan/tests.md` under the spec folder. |
| `--include-dependencies`| Instructs the workflow to generate tests that specifically validate integration points with dependency specifications referenced in the `spec.md`. |
| `--max-tests <int>` | Caps the total number of generated test items (bounded output, defense against runaway scans). |

### Input Overrides (Read-Only)

