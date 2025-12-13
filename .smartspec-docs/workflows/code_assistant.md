# /smartspec_code_assistant Manual (v6.0, English)

## Overview

The `/smartspec_code_assistant` workflow (Version 6.0.0) is a consolidated, multi-purpose helper tool designed to assist developers with implementation, error fixing, and code refactoring.

**Purpose:** This workflow replaces the legacy trio (`smartspec_implement_tasks`, `smartspec_fix_errors`, `smartspec_refactor_code`) by unifying their functionality under a single, secure interface controlled by the required `--mode` flag.

**Key Security Feature:** This workflow is strictly read-only concerning application source code. It **does not modify application runtime source trees**. It produces only **reports**, **prompts**, and optional **helper scripts** in designated, safe output directories, ensuring strict write-scope security.

## Usage

### Command Line Interface (CLI)

The workflow is invoked via the `smartspec_code_assistant` command, requiring the `--mode` flag to specify the desired operation.

```bash
/smartspec_code_assistant \
  --mode <implement|fix|refactor> \
  [--spec <path/to/spec.md>] \
  [--tasks <path/to/tasks.md>] \
  [--context <path/to/log-or-error.txt>] \
  [--out <output-root>] \
  [--json]
```

### Kilo Code

When integrated into a Kilo Code environment (e.g., a `.md` file execution), the invocation is similar:

```markdown
/smartspec_code_assistant.md \
  --mode <implement|fix|refactor> \
  [--spec <path/to/spec.md>] \
  [--tasks <path/to/tasks.md>] \
  [--context <path/to/log-or-error.txt>] \
  [--out <output-root>] \
  [--json]
```

## Parameters

The following flags and parameters control the workflow's behavior:

| Parameter | Required | Description | Applicable Modes |
| :--- | :--- | :--- | :--- |
| `--mode <implement|fix|refactor>` | **Yes** | Specifies the operational goal of the assistant. | All |
| `--spec <path>` | No | Path to the specification document (e.g., `specs/feature_x.md`). Recommended for `implement` and `refactor`. | implement, refactor |
| `--tasks <path>` | No | Path to the task list document. Recommended for `implement`. | implement |
| `--context <path>` | No | Path to external context (e.g., error logs, stack traces, bug reports). Recommended for `fix`. | All, especially fix |
| `--out <path>` | No | Overrides the default output root directory. Must resolve under allowed write scopes. | All |
| `--json` | No | Outputs a machine-readable `summary.json` alongside the primary report. | All |
| `--config <path>` | No | Path to the SmartSpec configuration file (Default: `.spec/smartspec.config.yaml`). | Universal |
| `--lang <th|en>` | No | Output language preference. | Universal |
| `--platform <cli|kilo|ci|other>` | No | Execution platform context. | Universal |
| `--apply` | No | Universal flag, but **ignored** by this workflow for security reasons. Safe outputs are always generated. | Universal (Ignored) |
| `--quiet` | No | Suppress non-essential console output. | Universal |

## Use Cases

### Use Case 1: Implementing a New Feature (`--mode=implement`)

**Scenario:** A developer needs a structured plan to implement a new user authentication feature defined in a specification file and a detailed task list.

**Command (CLI):**

```bash
/smartspec_code_assistant \
  --mode implement \
  --spec specs/auth/user_login.md \
  --tasks specs/auth/login_tasks.md \
  --out .smartspec/runs/auth_plan_v1
```

**Expected Result:**

The workflow analyzes the specification and tasks, then generates outputs under `.smartspec/runs/auth_plan_v1/`.

1.  **`report.md`:** Contains a task-by-task implementation plan, suggested file touchpoints, a risk list (e.g., handling password hashing), and a verification checklist.
2.  **`prompts/`:** A directory containing optimized, LLM-friendly prompts for the developer to use with external models (e.g., "Generate boilerplate for `auth_service.py` based on task 1").

### Use Case 2: Diagnosing and Fixing a Production Error (`--mode=fix`)

**Scenario:** A critical bug is reported. The developer has a stack trace and server logs saved in a file, and needs a quick diagnosis and proposed fix options.

**Command (Kilo Code):**

```markdown
/smartspec_code_assistant.md \
  --mode fix \
  --context /tmp/production_error_log_1234.txt \
  --json
```

**Expected Result:**

The workflow analyzes the log file, applies redaction policies, and generates a report and JSON summary in the default run directory (e.g., `.spec/reports/code-assistant/fix/<run-id>/`).

1.  **`report.md`:** Includes root-cause hypotheses (e.g., "Hypothesis 1: Off-by-one error in array indexing, Likelihood: High"), minimal-change fix options, and a regression risk assessment.
2.  **`summary.json`:** Provides a structured summary of the findings, risks, and recommendations, suitable for integration into CI/CD or issue tracking systems.

### Use Case 3: Planning a Major Refactoring (`--mode=refactor`)

**Scenario:** The team plans to migrate a legacy module to a new design pattern. The original specification is provided to ensure behavior parity.

**Command (CLI):**

```bash
/smartspec_code_assistant \
  --mode refactor \
  --spec specs/legacy/old_api.md \
  --out .smartspec/runs/refactor_api_plan
```

**Expected Result:**

The workflow generates a comprehensive refactoring plan under `.smartspec/runs/refactor_api_plan/`.

1.  **`report.md`:** Details a safe, step-by-step plan (small commits), suggested tests and checkpoints, and a detailed rollback plan.
2.  **`scripts/`:** May contain optional helper scripts, such as a preliminary sketch for a codemod tool to automate repetitive syntax changes.

## Output

The workflow produces artifacts exclusively within designated, safe write scopes.

### Output Artifacts

| Artifact | Description | Location (Default) |
| :--- | :--- | :--- |
| `report.md` | The primary human-readable output, containing analysis, findings, and recommendations. | `.spec/reports/code-assistant/<mode>/<run-id>/report.md` |
| `summary.json` | Structured, machine-readable summary of the run (only if `--json` is set). | `.spec/reports/code-assistant/<mode>/<run-id>/summary.json` |
| Prompts | Optimized, LLM-friendly text files for generating code snippets or documentation. | `.smartspec/prompts/code-assistant/<mode>/<run-id>/...` |
| Helper Scripts | Optional scripts (e.g., codemod sketches) generated for refactoring or implementation assistance. | `.smartspec/generated-scripts/code-assistant/<mode>/<run-id>/...` |

**Note on Output Root:** If the `--out <path>` flag is provided, all outputs are nested under that path, provided it is within the configured allowed write scopes.

### Required Content in `report.md`

Every report must contain the following sections:

1.  Context summary (redacted)
2.  Evidence sources (files/paths inspected)
3.  Findings (facts/evidence)
4.  Recommendations (ranked options)
5.  Risks & mitigations
6.  Suggested next commands (SmartSpec / tests)
7.  Output inventory (what files were written)

**Mandatory Security Notes (Footer):** The report footer must explicitly state:
*   No runtime source files were modified.
*   No governed artifacts were modified.
*   No scripts were executed.
*   Any use of `--apply` was ignored.
*   Any truncation/sampling of inputs occurred (due to context size caps).

## Notes & Related Workflows

### Security and Write Scope

This workflow strictly adheres to the governance contract:
*   It **cannot** write to source directories (`src/`, `app/`, etc.).
*   It **cannot** modify SmartSpec governed artifacts (`specs/**`, indices).
*   The `--apply` flag is accepted for compatibility but has **no effect** on write operations, ensuring the workflow remains safe and non-intrusive.

### Deprecation Mapping

This workflow is the consolidated replacement for the following legacy workflows (which are deprecated in v6):

|