# `/smartspec_report_implement_prompter` Workflow (Updated for Kilo Code `.md` + `--kilocode`)

> **Version:** 1.0.3  
> **Status:** Stable (paired with strict verifier)  
> **Scope of this update:** Clarify Kilo Code usage and require that any commands rendered into prompts **respect `.md` suffix + `--kilocode`** when the workflow itself is invoked with `--kilocode`.

---

## 1. Metadata & Governance

| Field              | Value                                      |
|--------------------|--------------------------------------------|
| Workflow ID        | smartspec_report_implement_prompter        |
| Version            | 1.0.3                                      |
| Category           | Evidence-Driven Implementation Support     |
| Status             | Stable (paired with strict verifier)       |
| Write Guard        | NO-WRITE (spec/tasks/registries/UI)        |
| Primary Consumer   | Kilo Code / IDE assistants                 |
| Required KB        | SmartSpec KB V2                            |

> **Write Guard**  
> This workflow MUST NOT modify `spec.md`, `tasks.md`, registries, UI schema files, or any source/test/docs/deploy artifacts. It MAY write **prompt files only** under a non-critical directory (e.g. `.smartspec/prompts/<spec-id>/`).

---

## 2. Purpose

This workflow acts as a **bridge between strict verification reports and implementation tools (e.g., Kilo Code, IDE AIs)**.

It:

1. Reads the **strict verification JSON report** produced by:
   - `/smartspec_verify_tasks_progress_strict`
2. Correlates it with:
   - `spec.md` (requirements)
   - `tasks.md` (implementation tasks)
3. Identifies:
   - Tasks that are incomplete, partial, false-positive, or unsynced
   - Critical missing components (API, tests, docs, deployment, etc.)
4. Generates **implementation-focused prompt files** (Markdown or JSON) for IDE AIs / Kilo Code to use as highly targeted instructions.

---

## 3. Typical Usage

### 3.1 CLI / Shell usage

1. **Run strict verification** (CLI example):

```bash
/smartspec_verify_tasks_progress_strict \
  --tasks specs/feature/<spec-id>/tasks.md \
  --report-format=json \
  --report .spec/reports/verify-tasks-progress/<spec-id>-verification-report.json
```

2. **Generate implementation prompts from the report**:

```bash
/smartspec_report_implement_prompter \
  --spec specs/feature/<spec-id>/spec.md \
  --tasks specs/feature/<spec-id>/tasks.md \
  --report .spec/reports/verify-tasks-progress/<spec-id>-verification-report.json \
  --output .smartspec/prompts/<spec-id>/
```

3. Open the generated prompt files and use them as **input prompts** for AI-assisted implementation.

4. After implementing changes, rerun strict verifier and optionally sync checkboxes:

```bash
/smartspec_verify_tasks_progress_strict \
  --tasks specs/feature/<spec-id>/tasks.md \
  --report-format=both

/smartspec_sync_tasks_checkboxes \
  --tasks specs/feature/<spec-id>/tasks.md \
  --report .spec/reports/verify-tasks-progress/<spec-id>-verification-report.json \
  --mode=auto
```

### 3.2 Kilo Code usage (CRITICAL UPDATE)

When invoked from **Kilo Code**, orchestrated workflows MUST use the **`.md`-suffixed command + `--kilocode` flag**. This applies both to:

- The command that launches this workflow, and
- Any SmartSpec commands that this workflow writes into generated prompts.

**Kilo Code invocation example:**

```bash
/smartspec_report_implement_prompter.md \
  --spec specs/feature/<spec-id>/spec.md \
  --tasks specs/feature/<spec-id>/tasks.md \
  --report .spec/reports/verify-tasks-progress/<spec-id>-verification-report.json \
  --output .smartspec/prompts/<spec-id>/ \
  --kilocode
```

If `--kilocode` is present, **all commands rendered into prompts MUST use Kilo-style syntax**:

```bash
/smartspec_verify_tasks_progress_strict.md \
  specs/feature/<spec-id>/tasks.md \
  --kilocode \
  --report-format=both

/smartspec_sync_tasks_checkboxes.md \
  specs/feature/<spec-id>/tasks.md \
  --kilocode
```

If `--kilocode` is **not** provided, rendered commands MUST use standard CLI syntax (no `.md` and no `--kilocode`).

---

## 4. CLI Definition

### 4.1 Command

```bash
/smartspec_report_implement_prompter \
  --spec <path/to/spec.md> \
  --tasks <path/to/tasks.md> \
  --report <path/to/strict-json-report> \
  [--output <dir>] \
  [--cluster <cluster-name-or-all>] \
  [--language <th|en>] \
  [--workspace-roots <paths>] \
  [--repos-config <path>] \
  [--evidence-config <path>] \
  [--dry-run] \
  [--format markdown|json] \
  [--max-tasks-per-prompt <int>] \
  [--max-chars-per-prompt <int>] \
  [--kilocode]
```

### 4.2 Kilo Code Command (orchestrated)

Kilo Code will typically invoke the **`.md` variant**:

```bash
/smartspec_report_implement_prompter.md \
  --spec <path/to/spec.md> \
  --tasks <path/to/tasks.md> \
  --report <path/to/strict-json-report> \
  --output <dir> \
  --kilocode
```

### 4.3 Flags (summary)

- `--spec` (required)  
  Path to the feature `spec.md`.

- `--tasks` (required)  
  Path to `tasks.md` for the same spec.

- `--report` (required)  
  Path to the JSON report generated by `/smartspec_verify_tasks_progress_strict`.

- `--output` (optional)  
  Directory where prompt `.md` files will be written. If omitted, prompts MAY be printed to stdout or returned through the host environment; implementations SHOULD support both.

- `--cluster` (optional)  
  One of: `api`, `tests`, `docs`, `deploy`, `all` (default: `all`). Filters which domain clusters to generate prompts for.

- `--language` (optional)  
  `th` (Thai) or `en` (English). Default follows locale rules in Section 18/24.

- `--workspace-roots`, `--repos-config` (optional)  
  Required for multi-repo resolution; must mirror strict verifier configuration.

- `--evidence-config` (optional)  
  Path to evidence-config JSON that refines cluster/evidence mapping.

- `--dry-run` (optional)  
  When present, **no files are written**. Instead, a summary of what *would* be generated is printed.

- `--format` (optional)  
  `markdown` (default) or `json`. In `json` mode, structured output suitable for IDE sidebars / UI.

- `--max-tasks-per-prompt`, `--max-chars-per-prompt` (optional)  
  Override defaults (15 tasks, 35,000 chars).

- `--kilocode` (optional but IMPORTANT)  
  Indicates that the workflow is being run under Kilo Code. When set, **all commands embedded in prompts must use `.md` + `--kilocode` syntax**.

---

## 5. Inputs & Data Sources

*(Same as previous version, retained for completeness; focus of this update is on Kilo Code command rendering and does not change core behavior.)*

1. **Strict JSON Report** (required)  
   - Produced by `/smartspec_verify_tasks_progress_strict`.
   - Contains summary, per-task verdicts, and evidence details.

2. **`spec.md`** (required)  
   - Provides feature context, architecture, and domain language.

3. **`tasks.md`** (required)  
   - Provides task titles, descriptions, phases, and acceptance criteria.

---

## 6. Core Behavior & Algorithm (excerpted)

1. Parse CLI args (including `--kilocode`).
2. Load strict report JSON, `spec.md`, and `tasks.md`.
3. Classify tasks into `unsynced_only`, `simple_not_started`, and `complex_cluster` according to governance.
4. Group complex tasks into domain clusters (`api`, `tests`, `docs`, `deploy`).
5. For each cluster, build prompt content using official templates.
6. When constructing any **embedded SmartSpec commands** (strict verify, sync, re-run prompter), use the **`Command Rendering Rules`** below.
7. Emit prompts either as Markdown files under `.smartspec/prompts/<spec-id>/` or as JSON (when `--format json`).

---

## 7. Command Rendering Rules (NEW + IMPORTANT)

### 7.1 Overview

This workflow frequently emits **"what to run next"** commands inside prompts, for example:

- Rerun strict verifier
- Sync checkboxes
- Re-run this workflow with narrowed clusters

These commands MUST respect the environment:

- Standard CLI → no `.md`, no `--kilocode`  
- Kilo Code (`--kilocode` provided) → **`.md` suffix + `--kilocode` required**

### 7.2 Environment Detection

- If CLI args include `--kilocode` → set `env.kilocode = true`.
- Else → `env.kilocode = false`.

No other auto-detection is required; **the presence of `--kilocode` is the single source of truth**.

### 7.3 Render Strict Verify Command

Given:

- `tasks_path` (required)

The rendered command MUST be:

- **Standard CLI** (`env.kilocode = false`):

  ```bash
  /smartspec_verify_tasks_progress_strict \
    --tasks ${tasks_path} \
    --report-format=both
  ```

- **Kilo Code** (`env.kilocode = true`):

  ```bash
  /smartspec_verify_tasks_progress_strict.md \
    ${tasks_path} \
    --kilocode \
    --report-format=both
  ```

### 7.4 Render Sync Checkboxes Command

Given:

- `tasks_path` (required)

The rendered command MUST be:

- **Standard CLI**:

  ```bash
  /smartspec_sync_tasks_checkboxes \
    --tasks ${tasks_path}
  ```

- **Kilo Code**:

  ```bash
  /smartspec_sync_tasks_checkboxes.md \
    ${tasks_path} \
    --kilocode
  ```

### 7.5 Render This Workflow (Re-run Prompter)

When a prompt suggests re-running this workflow (e.g., with different clusters), it MUST render:

- **Standard CLI**:

  ```bash
  /smartspec_report_implement_prompter \
    --spec ${spec_path} \
    --tasks ${tasks_path} \
    --report ${report_path} \
    --cluster ${cluster}
  ```

- **Kilo Code**:

  ```bash
  /smartspec_report_implement_prompter.md \
    --spec ${spec_path} \
    --tasks ${tasks_path} \
    --report ${report_path} \
    --cluster ${cluster} \
    --kilocode
  ```

### 7.6 Template Integration

Prompt templates MUST NOT hard-code commands. Instead, they MUST use placeholders:

```markdown
## After Implementation

- Run strict verifier:

  ```bash
  {{verify_command}}
  ```

- If all tasks in this prompt are complete, sync checkboxes:

  ```bash
  {{sync_command}}
  ```
```

During rendering, the implementation MUST compute `verify_command` and `sync_command` using the rules above and inject them into the template.

---

## 8. Prompt Templates (Excerpted)

### 8.1 API Cluster Template (excerpt)

```markdown
# Kilo Code Implementation Prompt — API Cluster

<!--
Prompt-Generation-ID: {{uuid}}
Spec-ID: {{spec_id}}
Report-Version: {{strict_report_version}}
Generated-At: {{timestamp_iso8601}}
-->

## Tasks Covered
{{task_list}}

## Context
- Spec: {{spec_path}}
- Tasks: {{tasks_path}}
- Report: {{report_path}}
- Tech stack: {{stack_detected}}

## Strict Report Summary
{{cluster_diagnostics}}

## Required Implementations
1. Review these existing files:
   {{related_source_files}}
2. Implement / fix the following endpoints:
   {{endpoint_list}}
3. Follow these rules:
   - Use existing middleware patterns
   - Reuse domain services
   - Follow the existing error model

## After Implementation
- Run tests: {{test_command}}
- Re-run strict verifier:

  ```bash
  {{verify_command}}
  ```

- If everything in this prompt is complete, sync tasks:

  ```bash
  {{sync_command}}
  ```
```

> **Kilo Code Note:** When `--kilocode` is provided to this workflow, `verify_command` and `sync_command` MUST be rendered using the `.md` + `--kilocode` form.

---

## 9. Locale Resolution (Reminder)

Locale resolution is unchanged: `--language` > spec header > body-language ratio > platform default (Kilo Code → `th`) > fallback `en`.

Prompts may therefore contain Thai or English text, but **embedded commands must still follow the environment-specific rules in Section 7**.

---

## 10. Backward Compatibility

- Existing behavior for non-Kilo environments is preserved.  
- Existing paths, flags, and governance remain valid.  
- This update is **additive** and only:
  - Adds `--kilocode` as an input flag, and
  - Specifies how **rendered commands** must adapt to this flag.

No changes are required for pipelines that call `/smartspec_report_implement_prompter` without `--kilocode`.

---

**End of `/smartspec_report_implement_prompter` workflow specification (v1.0.3, Kilo Code aware).**

