---
description: Convert spec.md (or plan.md) → tasks.md with duplication prevention and strict-verifier-compatible evidence hooks.
version: 7.1.2
workflow: /smartspec_generate_tasks
category: core
---

# smartspec_generate_tasks

> **Canonical path:** `.smartspec/workflows/smartspec_generate_tasks.md`
> **Version:** 7.1.2
> **Status:** Active
> **Category:** core

## Purpose

Generate or refine `tasks.md` from `spec.md` (or `plan.md`) or `ui-spec.json` (A2UI) with:

- **reuse-first / duplication prevention**
- **preview-first governance**
- **strict-verifier-compatible evidence hooks** (machine-parseable `evidence:` lines)

This workflow is the canonical producer of `tasks.md` that downstream workflows can trust:

- `/smartspec_verify_tasks_progress_strict`
- `/smartspec_report_implement_prompter`
- `/smartspec_quality_gate`

**Critical requirement:** The generated `tasks.md` MUST reduce false negatives in strict verification.

---

## Governance contract

This workflow MUST follow:

- `knowledge_base_smartspec_handbook.md`
- `.spec/smartspec.config.yaml` (config-first)

### Write scopes (enforced)

Allowed writes:

- Governed specs: `specs/**` (**requires** `--apply`)
- Safe outputs (previews/reports): `.spec/reports/generate-tasks/**` (no `--apply` required)

Forbidden writes (must hard-fail):

- Any path outside config `safety.allow_writes_only_under`
- Any path under config `safety.deny_writes_under`
- Any runtime source tree modifications

### `--apply` behavior

- Without `--apply` (or with `--validate-only`):
  - MUST NOT modify any file under `specs/**`.
  - MUST write a deterministic preview bundle to `.spec/reports/generate-tasks/**`.
  - If validation fails, MUST NOT “auto-fix” by editing `specs/**/tasks.md`.
- With `--apply`:
  - MAY update or create `specs/**/tasks.md`.
  - MUST NOT modify any other governed files.
  - MUST write atomically (temp + rename) and must not escape via symlink.

---

## Invocation

### CLI

```text
/smartspec_generate_tasks <specs/<category>/<spec-id>/spec.md|.../plan.md|.../ui-spec.json> [--apply] [--validate-only] [--json]
```

### Kilo Code

```text
/smartspec_generate_tasks.md <specs/<category>/<spec-id>/spec.md|.../plan.md|.../ui-spec.json> [--apply] [--validate-only] [--json] --platform kilo
```

---

## Inputs

### Positional

Primary input is positional:

- `specs/<category>/<spec-id>/spec.md`
- or `specs/<category>/<spec-id>/plan.md`
- or `specs/<category>/<spec-id>/ui-spec.json`

### Input validation (mandatory)

- Input MUST exist.
- Must resolve under `specs/**`.
- Must not escape via symlink.
- Derive `spec-id` from folder name.

---

## Flags

### Universal flags (must support)

| Flag | Required | Description |
|---|---|---|
| `--config` | No | Path to config (default: `.spec/smartspec.config.yaml`) |
| `--lang` | No | `th` \| `en` \| `auto` |
| `--platform` | No | `cli` \| `kilo` \| `ci` \| `other` |
| `--out` | No | Base output directory (must pass safety checks) |
| `--json` | No | Emit machine-readable summary JSON |
| `--quiet` | No | Reduce logs |

### Workflow-specific flags

| Flag | Required | Description |
|---|---|---|
| `--apply` | No | Enable writes to governed artifacts (`tasks.md`) |
| `--validate-only` | No | Run preview + validation only (no writes to `specs/**`) |
| `--skip-duplication-check` | No | Skip duplication check (not recommended) |
| `--registry-roots` | No | Extra registry directories to check (comma-separated) |

---

## Behavior

### 1) Determine target paths

Given `specs/<category>/<spec-id>/<input>`:

- target governed file: `specs/<category>/<spec-id>/tasks.md`
- preview file: `.spec/reports/generate-tasks/<run-id>/preview/<spec-id>/tasks.md`
- best-effort patch: `.spec/reports/generate-tasks/<run-id>/diff/<spec-id>.patch`

### 2) Pre-generation duplication validation (recommended)

If project scripts exist, the agent SHOULD run duplication detection before generating tasks.

Recommended command (if present):

```text
python3 .smartspec/scripts/detect_duplicates.py --registry-dir .spec/registry/ --threshold 0.8
```

Rules:

- If the script is missing, log a warning and continue.
- If duplicates are detected, MUST present duplicates and require explicit user decision before proceeding.

### 3) Produce task graph

- Convert scope into milestones + tasks.
- Ensure every milestone has verifiable outputs.
- Ensure every task has at least **one** machine-parseable evidence hook line (`evidence:`).

### 4) Evidence hook policy (MUST)

To prevent “implement แล้ว แต่ verify ไม่เจอ”, tasks MUST include evidence hooks that are:

- **specific** (file path + `symbol`/`contains`/`heading` when applicable)
- **repo-relative** (no absolute paths)
- **quote-safe** (values with spaces MUST use double quotes)

Canonical line syntax:

- `evidence: <type> <key>=<value> <key>=<value> ...`

Evidence types MUST align with strict verifier:

- `code` (required: `path`; optional: `symbol`, `contains`)
- `test` (required: `path`; optional: `contains`, `command`)
- `docs` (required: `path`; optional: `heading`, `contains`)
- `ui` (required: `screen`; optional: `route`, `component`, `states`)

**Hard rule:**

- `path=` MUST be a repo-relative path (no spaces). Do NOT put shell commands into `path=`.
- If you want to record a command, use `command="..."` on `test` evidence.

### 5) Existing `tasks.md` merge + normalization (MANDATORY)

If `specs/<category>/<spec-id>/tasks.md` already exists:

The workflow MUST treat it as the starting point and produce a refined output that:

1) **Preserves stable task IDs** (do not renumber existing tasks unless unavoidable)
2) **Avoids duplication** (do not re-add already existing tasks)
3) **Preserves human notes** that do not conflict with canonical format
4) **Normalizes evidence format** to strict-verifier-compatible `evidence:` lines

Non-canonical evidence that MUST be normalized:

- `**Evidence Hooks:**` blocks
- `**Evidence:** <free text>` bullets
- legacy/non-compliant evidence types like `file_exists`, `test_exists`, `command`, `api_route`, `db_schema`

Normalization rule:

- Convert non-canonical evidence into canonical `evidence:` lines wherever it is safe.
- If safe conversion is not possible, keep the original note AND add a remediation note in the report recommending:

  - `/smartspec_migrate_evidence_hooks --tasks-file <tasks.md>`

> IMPORTANT: MUST NOT generate placeholders like `path=???` or `COMMAND_NOT_SUPPORTED`.

### 6) Preview & report (always)

Write:

- `.spec/reports/generate-tasks/<run-id>/preview/<spec-id>/tasks.md`
- `.spec/reports/generate-tasks/<run-id>/diff/<spec-id>.patch` (best-effort)
- `.spec/reports/generate-tasks/<run-id>/report.md`
- `.spec/reports/generate-tasks/<run-id>/summary.json` (if `--json`)

### 7) Post-generation validation (MANDATORY)

After generating the preview and before applying, MUST validate the generated tasks using the project validator:

```text
python3 .smartspec/scripts/validate_tasks_enhanced.py --tasks .spec/reports/generate-tasks/<run-id>/preview/<spec-id>/tasks.md --spec specs/<category>/<spec-id>/spec.md
```

Notes:

- `--strict-sections` is OPTIONAL. If enabled, it requires legacy sections.
- If validation fails, MUST NOT apply.
- If validation fails, MUST NOT edit `specs/**/tasks.md` in preview mode. Emit fixes as report notes/patch.

### 8) Apply (only with `--apply` and only if validation passes)

- Update `specs/<category>/<spec-id>/tasks.md`.
- MUST write atomically (temp + rename).
- MUST NOT modify other files.

---

## Recommended next steps

- Implement: `/smartspec_implement_tasks <tasks.md>`
- Strict verify: `/smartspec_verify_tasks_progress_strict <tasks.md>`
- Sync checkboxes: `/smartspec_sync_tasks_checkboxes <tasks.md> --apply`

---

## `tasks.md` templates (MUST)

### Header Template

```md
| spec-id | source | generated_by | updated_at |
|---|---|---|---|
| `<spec-id>` | `<spec.md|plan.md|ui-spec.json>` | `smartspec_generate_tasks:7.1.2` | `<ISO_DATETIME>` |
```

### Tasks Section Skeleton

```md
## Tasks

> Notes:
> - Checkbox [x] is not evidence. Evidence must be declared with `evidence:` lines.
> - Evidence values with spaces must be quoted, e.g. contains="hello world".
```

### Task Item Template (Verifier-compatible)

```md
- [ ] <TASK-ID> <Task title>
  implements: <feature|story|component>
  t_ref: <Txxx|REQ-xxx|NFR-xxx|UI-xxx>
  acceptance:
    - <bullet>
    - <bullet>
  evidence: code path=<repo/rel/file> symbol=<SymbolName>
  evidence: test path=<repo/rel/test-file> contains="<assertion phrase>" command="<optional test command>"
  evidence: docs path=<repo/rel/doc.md> heading="<Heading>"
```

Rules:

- `<TASK-ID>` MUST be stable and unique (recommended: `TSK-<spec-id>-NNN`)
- Do NOT wrap the task title in bold (keeps parsing simple)
- Evidence lines MUST contain `evidence:` and follow `type key=value` format

---

# End of workflow doc
```
