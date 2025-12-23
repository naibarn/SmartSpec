---
description: Convert spec.md (or plan.md) → tasks.md with duplication prevention and strict-verifier-compatible evidence hooks.
version: 7.1.3
workflow: /smartspec_generate_tasks
category: core
---

# smartspec_generate_tasks

> **Canonical path:** `.smartspec/workflows/smartspec_generate_tasks.md`
> **Version:** 7.1.3
> **Status:** Active
> **Category:** core

## Purpose

Generate or **normalize** `tasks.md` from:

- `specs/<category>/<spec-id>/spec.md`
- `specs/<category>/<spec-id>/plan.md`
- `specs/<category>/<spec-id>/ui-spec.json` (A2UI)

This workflow is the canonical producer of `tasks.md` that downstream workflows can trust:

- `/smartspec_verify_tasks_progress_strict`
- `/smartspec_report_implement_prompter`
- `/smartspec_quality_gate`

**Critical requirement:** The generated `tasks.md` MUST minimize strict-verifier false-negatives by emitting **machine-parseable evidence hooks** (lines that begin with `evidence:`).

---

## File locations (IMPORTANT)

- **Governance/config/index:** `.spec/`
  - `.spec/smartspec.config.yaml`
  - `.spec/SPEC_INDEX.json`
  - `.spec/registry/**`
  - `.spec/reports/**`
- **Workflow docs:** `.smartspec/workflows/**`
- **Project helper scripts (preferred):** `.smartspec/scripts/**`
  - Example helpers (optional, if present):
    - `.smartspec/scripts/detect_duplicates.py`
    - `.smartspec/scripts/validate_tasks_enhanced.py`

**Hard rule:** the workflow MUST NOT assume `.spec/scripts/**` exists. If a helper script is missing, it MUST log a warning and continue in preview; for `--apply`, missing validator MUST hard-fail (to prevent writing invalid `tasks.md`).

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

Primary input is positional and MUST exist:

- `specs/<category>/<spec-id>/spec.md`
- or `specs/<category>/<spec-id>/plan.md`
- or `specs/<category>/<spec-id>/ui-spec.json`

### Input validation (mandatory)

- Input MUST resolve under `specs/**`.
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
| `--apply` | No | Enable writes to governed artifacts (`specs/**/tasks.md`) |
| `--validate-only` | No | Generate preview + validate only (no writes) |
| `--skip-duplication-check` | No | Skip duplication check (NOT recommended) |
| `--registry-roots` | No | Extra registry directories to check for duplicates (comma-separated) |

---

## Behavior

### 1) Determine target paths

Given `specs/<category>/<spec-id>/<input>`:

- target governed file: `specs/<category>/<spec-id>/tasks.md`
- preview file: `.spec/reports/generate-tasks/<run-id>/preview/<spec-id>/tasks.md`
- patch (best effort): `.spec/reports/generate-tasks/<run-id>/diff/<spec-id>.patch`

### 2) Pre-generation duplication check (recommended)

If a helper exists, the workflow SHOULD run duplication detection:

```text
python3 .smartspec/scripts/detect_duplicates.py --registry-dir .spec/registry/ --threshold 0.8
```

Rules:

- If the script is missing, log a warning and continue.
- If duplicates are detected, MUST present them in preview output and require explicit user decision before proceeding.

### 3) Generate / normalize tasks

The workflow MUST produce a `tasks.md` that:

- has a **header table** at top (see template)
- has a `## Tasks` section with checkbox tasks
- uses **stable task IDs**: recommended `TSK-<spec-id>-NNN`
- includes `implements:` + `t_ref:` + `acceptance:` for each task
- emits **strict evidence hooks** as `evidence:` lines (see grammar)

#### Existing `tasks.md` handling (important)

If `specs/<category>/<spec-id>/tasks.md` already exists:

- MUST preserve existing task IDs when possible (do not renumber unless unavoidable).
- MUST normalize legacy formats into the canonical format (see “Legacy patterns to eliminate”).
- MUST NOT introduce new formatting that makes parsing harder (bold IDs, custom headings per task, etc.).

### 4) Post-generation validation (MANDATORY)

After generating preview and before applying, MUST validate the generated tasks using the project validator:

```text
python3 .smartspec/scripts/validate_tasks_enhanced.py --tasks .spec/reports/generate-tasks/<run-id>/preview/<spec-id>/tasks.md --spec specs/<category>/<spec-id>/spec.md
```

Rules:

- If the validator script is missing:
  - In preview: log warning and emit “validator missing” in report.
  - With `--apply`: **hard-fail** (do not write governed tasks).
- If validation fails: MUST NOT apply.
- If validation fails: MUST NOT edit `specs/**/tasks.md` in preview mode.

### 5) Apply (only with `--apply` and only if validation passes)

- Update `specs/<category>/<spec-id>/tasks.md`.
- MUST write atomically (temp + rename).
- MUST NOT modify other files.

---

## Evidence hook grammar (MUST)

Evidence lines MUST follow:

```text
evidence: <type> key=value key="value with spaces" ...
```

### Allowed types

- `code`
- `test`
- `docs`
- `ui`

### Key rules

- `path=` is REQUIRED for all types.
- `heading=` is ONLY allowed for `docs`.
- Evidence values with spaces MUST be quoted.
- Never emit placeholders like `path=???`.

### Examples

```md
evidence: code path=src/auth/service.ts symbol=AuthService

evidence: code path=src/routes/auth.ts contains="/auth/register"

evidence: test path=tests/auth.test.ts contains="should register" command="pnpm test auth"

evidence: docs path=docs/openapi.yaml contains="/auth/register"

evidence: docs path=README.md heading="Authentication"

evidence: ui path=apps/web/src/pages/Login.tsx contains="Sign in"
```

**Important mapping rule (reduces false-negatives):**

- If the artifact is a specification/contract/doc (e.g., `openapi.yaml`, `*.md`, `docs/**`), prefer `evidence: docs ...` (not `code`).

---

## Legacy patterns to eliminate (MUST NOT generate)

These formats cause verifier false-negatives and must be converted:

- Task IDs wrapped in bold: `- [ ] **TSK-...** ...`
- Per-task headings like `### TSK-...`
- Blocks like `**Evidence Hooks:**` followed by natural language bullets
- Evidence lines without the `evidence:` prefix

If any of the above are detected in an existing `tasks.md`, the workflow MUST normalize them into the canonical format.

---

## `tasks.md` templates (MUST)

### Header Template

```md
| spec-id | source | generated_by | updated_at |
|---|---|---|---|
| `<spec-id>` | `<spec.md|plan.md|ui-spec.json>` | `smartspec_generate_tasks:7.1.3` | `<ISO_DATETIME>` |
```

### Tasks Section Skeleton

```md
## Tasks

> Notes:
> - Checkbox [x] is not evidence. Evidence must be declared with `evidence:` lines.
> - Evidence values with spaces must be quoted, e.g. contains="hello world".
```

### Task Item Template (canonical)

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

- `<TASK-ID>` MUST be stable and unique (recommended: `TSK-<spec-id>-NNN`).
- Do NOT wrap the task title or ID in bold.

---

# End of workflow doc

