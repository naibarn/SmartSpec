---
description: Convert spec.md (or plan.md) → tasks.md with duplication prevention and strict-verifier-compatible evidence hooks.
version: 7.1.1
workflow: smartspec_generate_tasks
category: core
---

# smartspec_generate_tasks

> **Canonical path:** `.smartspec/workflows/smartspec_generate_tasks.md`
> **Version:** 7.1.1
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

## File locations (Important)

All SmartSpec configuration and registry files are located in the `.spec/` folder:

- Config: `.spec/smartspec.config.yaml`
- Spec Index: `.spec/SPEC_INDEX.json`
- Registry: `.spec/registry/`
- Reports: `.spec/reports/`
- Scripts: `.spec/scripts/`

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
- Any path under config `safety.deny_writes_under` (e.g., `.spec/registry/**`, `.spec/cache/**`)
- Any runtime source tree modifications

### `--apply` behavior

- Without `--apply`:
  - MUST NOT modify `specs/**/tasks.md`.
  - MUST write a deterministic preview bundle to `.spec/reports/`.
- With `--apply`:
  - MAY update or create `specs/**/tasks.md`.
  - MUST NOT modify any other governed files.

---


---

## Inputs

### Positional

- `--spec` (positional):
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
| `--spec` | Yes (positional) | Spec/plan/ui-spec path |
| `--apply` | No | Enable writes to governed artifacts (`tasks.md`) |
| `--validate-only` | No | Run validation + preview without writing governed files |
| `--skip-duplication-check` | No | Skip pre-generation duplication check (not recommended) |
| `--registry-roots` | No | Extra registry directories to check (comma-separated) |

---

## Behavior

### 1) Pre-generation duplication validation (MANDATORY)

Before generating tasks, the agent MUST check for existing similar tasks in other specs.

**Validation Command:**

```bash
python3 .spec/scripts/detect_duplicates.py \
  --registry-dir .spec/registry/ \
  --threshold 0.8
```

**Validation Rules:**

- Exit `0`: proceed.
- Exit `1`: duplicates found; MUST present duplicates and require explicit user decision before proceeding.

### 2) Produce task graph

- Convert scope into milestones + tasks.
- Ensure every milestone has verifiable outputs.
- Ensure every task has at least **one** machine-parseable evidence hook line (`evidence:`).

### 3) Evidence hook policy (MUST)

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

**Rule:** generator SHOULD prefer `symbol=` or `contains=` over directory-only hooks.

### 4) Existing `tasks.md` merge + normalization (MANDATORY)

If `specs/<category>/<spec-id>/tasks.md` already exists:

The workflow MUST treat it as the starting point and produce a refined output that:

1) **Preserves stable task IDs** (do not renumber existing tasks unless unavoidable)
2) **Avoids duplication** (do not re-add already existing tasks)
3) **Preserves human notes** that do not conflict with canonical format
4) **Normalizes evidence format** to strict-verifier-compatible lines

#### 4.1 Non-canonical evidence that MUST be normalized

Any of the following MUST be normalized in preview output:

- `- **Evidence Hooks:**` blocks
- `- **Evidence:** <free text>` bullets
- legacy/non-compliant evidence types like `file_exists`, `test_exists`, `command`

#### 4.2 Normalization rule

- Convert non-canonical evidence into canonical `evidence:` lines wherever it is safe.
- If safe conversion is not possible, keep the original note AND add a remediation note in the report recommending:

  - `/smartspec_migrate_evidence_hooks --tasks-file <tasks.md>`

> IMPORTANT: MUST NOT generate placeholders like `path=???` or `COMMAND_NOT_SUPPORTED`.

### 5) Preview & report (always)

Write:

- `.spec/reports/generate-tasks/<run-id>/preview/<spec-id>/tasks.md`
- `.spec/reports/generate-tasks/<run-id>/diff/<spec-id>.patch` (best-effort)
- `.spec/reports/generate-tasks/<run-id>/report.md`
- `.spec/reports/generate-tasks/<run-id>/summary.json` (if `--json`)

### 6) Post-generation validation (MANDATORY)

After generating preview and before applying, MUST validate tasks.

**Validation Command:**

```bash
python3 .smartspec/scripts/validate_tasks_enhanced.py \
  --tasks .spec/reports/generate-tasks/<run-id>/preview/<spec-id>/tasks.md \
  --spec specs/<category>/<spec-id>/spec.md \
  --check-duplicates --threshold 0.8
```

**Validation Rules:**

- Exit `0`: may proceed with `--apply`.
- Exit `1`: MUST NOT apply; include validator output in `report.md`.

### 7) Apply (only with `--apply` and if validation passes)

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
| `<spec-id>` | `<spec.md|plan.md|ui-spec.json>` | `smartspec_generate_tasks:7.1.1` | `<ISO_DATETIME>` |
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
  evidence: test path=<repo/rel/test> contains="<assertion phrase>"
  evidence: docs path=<repo/rel/doc.md> heading="<Heading>"
```

Rules:

- `<TASK-ID>` MUST be stable and unique (recommended: `TSK-<spec-id>-NNN`)
- Do NOT wrap the task title in bold (keeps parsing simple)
- Evidence lines MUST contain `evidence:` and follow `type key=value` format

---

# End of workflow doc
```

