# /smartspec_report_implement_prompter Manual (v6.0, English)

## Overview

The `/smartspec_report_implement_prompter` workflow (v6.0.0) is a **Production Ready** tool designed to generate comprehensive **implementation prompt packs** for Large Language Models (LLMs).

**Purpose:** To consolidate input from a specification (`.spec`), associated tasks, and optionally, strict verification reports, into a structured, safe, and actionable set of prompts.

**Key Features:**

1.  **Safety First:** Enforces strict governance contracts, ensuring outputs are safe (prompts only) and never modify governed artifacts or source trees.
2.  **Redaction & Excerpt Policy:** Automatically redacts secrets and adheres to content limits to prevent proprietary code or sensitive information leakage.
3.  **Target Profiles:** Supports `generic` (for general LLMs) and `cursor` (optimized for Cursor workflows) prompt packaging.
4.  **Replacement:** This workflow replaces the legacy prompt generators (`smartspec_generate_implement_prompt` and `smartspec_generate_cursor_prompt`) removed in SmartSpec v6.

## Usage

### CLI Usage

Execute the workflow directly from the command line, providing the required specification and tasks files.

```bash
/smartspec_report_implement_prompter \
  --spec <path/to/spec.md> \
  --tasks <path/to/tasks.md> \
  [--verify-report <path/to/verify-report-dir-or-file>] \
  [--target <generic|cursor>] \
  [--out <output-root>] \
  [--json] \
  [--strict]
```

### Kilo Code Usage

For execution within the SmartSpec Kilo runtime environment, the invocation is identical to the CLI usage.

```bash
/smartspec_report_implement_prompter.md \
  --spec <path/to/spec.md> \
  --tasks <path/to/tasks.md> \
  [--verify-report <path/to/verify-report-dir-or-file>] \
  [--target <generic|cursor>] \
  [--out <output-root>] \
  [--json] \
  [--strict]
```

## Use Cases

### Use Case 1: Standard Implementation Prompt Generation (Generic Target)

**Scenario:** A developer needs a standard, safe prompt pack for a new feature documented in `specs/feature_x.md`, with implementation broken down in `specs/tasks_x.md`. The output should be placed in a custom location.

**CLI Command:**

```bash
/smartspec_report_implement_prompter \
  --spec specs/feature_x.md \
  --tasks specs/tasks_x.md \
  --target generic \
  --out ./my_prompt_runs/feature_x_v1 \
  --json
```

**Expected Result:**

A new directory structure is created under `./my_prompt_runs/feature_x_v1/<generic>/<run-id>/` containing the prompt pack files (`README.md`, `prompts/00_system_and_rules.md`, etc.) and a `meta/summary.json` file detailing the run. The prompt pack emphasizes constraints and evidence for general LLM use.

### Use Case 2: Cursor Prompt Generation with Verification Report

**Scenario:** The implementation tasks for feature `auth_refactor` have been partially completed and verified using the strict verification workflow. The resulting report is available at `.spec/reports/verify-tasks-progress/auth_refactor_latest/`. The developer needs a Cursor-optimized prompt pack to continue the work, failing if the report cannot be integrated correctly.

**Kilo Code Command:**

```bash
/smartspec_report_implement_prompter.md \
  --spec specs/auth_refactor.md \
  --tasks specs/auth_tasks.md \
  --verify-report .spec/reports/verify-tasks-progress/auth_refactor_latest/summary.json \
  --target cursor \
  --strict
```

**Expected Result:**

1.  A prompt pack is generated under `.smartspec/prompts/auth_refactor/cursor/<run-id>/`.
2.  The prompt pack is optimized for Cursor, featuring shorter, chunked prompts and explicit file path hints.
3.  The verification report content (progress, failures, evidence) is integrated into the prompt structure (likely in `20_plan_of_attack.md` or `50_tests_and_verification.md`).
4.  If the `--verify-report` path is invalid or the report is malformed, the workflow exits with code `1` due to the `--strict` flag.

### Use Case 3: Generating Prompts for CI/CD Pipeline (Quiet Mode)

**Scenario:** The workflow is integrated into a CI/CD pipeline that only needs the output path and summary JSON, suppressing standard console output.

**CLI Command:**

```bash
/smartspec_report_implement_prompter \
  --spec specs/ci_update.md \
  --tasks specs/ci_tasks.md \
  --json \
  --quiet
```

**Expected Result:**

The workflow runs silently. Upon successful completion, the path to the generated prompt pack and the contents of `meta/summary.json` are made available to the pipeline, typically via standard output (if not suppressed by the calling environment).

## Parameters

| Flag | Category | Required | Description |
| :--- | :--- | :--- | :--- |
| `--spec <path>` | Workflow Specific | Yes | Path to the specification file (`.md`). Must resolve under `specs/**`. |
| `--tasks <path>` | Workflow Specific | Yes | Path to the tasks file (`.md`). Must resolve under `specs/**`. |
| `--verify-report <path>` | Workflow Specific | No | Path to the strict verification report directory or JSON summary file. Recommended source: `.spec/reports/verify-tasks-progress/**`. |
| `--target <generic|cursor>` | Workflow Specific | No | Packaging profile for the prompt pack. Default is `generic`. |
| `--strict` | Workflow Specific | No | If set, the workflow fails (exit code 1) if critical prompt pack requirements (e.g., valid report integration) are missing. |
| `--out <path>` | Universal | No | Base output root directory. Must be a directory path under an allowed write scope. |
| `--json` | Universal | No | Output a `meta/summary.json` file detailing the run results and next steps. |
| `--config <path>` | Universal | No | Path to the configuration file. Default: `.spec/smartspec.config.yaml`. |
| `--lang <th|en>` | Universal | No | Language for output messages. |
| `--platform <cli|kilo|ci|other>` | Universal | No | Platform context. |
| `--apply` | Universal | No | Accepted for compatibility, but has **no effect** on write scopes (ignored). |
| `--quiet` | Universal | No | Suppress standard output messages. |

## Output

The workflow produces a secure, structured prompt pack within a unique run folder to prevent collision.

### Output Location

1.  **If `--out` is provided:** `<out>/<target>/<run-id>/`
2.  **If `--out` is NOT provided:** `.smartspec/prompts/<spec-id>/<target>/<run-id>/`

### Output Artifacts (Prompt Pack Structure)

The run folder contains the following mandatory and recommended files:

| File Path | Status | Description |
| :--- | :--- | :--- |
| `README.md` | Mandatory | Contains spec/tasks paths, target profile, constraints, and mandatory security notes. |
| `prompts/00_system_and_rules.md` | Mandatory | Defines the LLM's role and operational rules. |
| `prompts/10_context.md` | Mandatory | Provides necessary background context from the spec. |
| `prompts/20_plan_of_attack.md` | Mandatory | Outlines the strategy, potentially incorporating verification results. |
| `prompts/30_tasks_breakdown.md` | Mandatory | Detailed breakdown of implementation tasks. |
| `prompts/40_risks_and_guards.md` | Mandatory | Highlights potential risks and necessary safeguards. |
| `prompts/50_tests_and_verification.md` | Recommended | Details testing procedures and verification steps. |
| `meta/summary.json` | Optional (if `--json`) | Structured JSON summary of the run, inputs, redaction status, and next steps. |

## Notes & Related Workflows

### Security and Governance Notes

*   **Safe Output Only:** This workflow is strictly limited to writing prompts under `.smartspec/prompts/**`. It cannot modify any source code, governed artifacts (like `SPEC_INDEX.json`), or reports.
*   **Redaction:** Secrets detected in inputs (based on `safety.redaction` configuration) are redacted before being included in the prompt pack.
*   **Ignored Flag:**