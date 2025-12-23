```md
---
description: Convert spec.md (or plan.md) → tasks.md with duplication prevention and verifier-compatible evidence hooks.
version: 7.1.0
workflow: /smartspec_generate_tasks
category: core
---

# smartspec_generate_tasks

> **Canonical path:** `.smartspec/workflows/smartspec_generate_tasks.md`
> **Version:** 7.1.0
> **Status:** Active
> **Category:** core

## Purpose

Generate or refine `tasks.md` from `spec.md` (or `plan.md`) or `ui-spec.json` (A2UI) with:

- **reuse-first / duplication prevention**
- **preview-first** governance
- **verifier-compatible evidence hooks** (machine-parseable `evidence:` lines)

This workflow is a canonical producer of `tasks.md` that downstream workflows can trust:

- `/smartspec_verify_tasks_progress_strict`
- `/smartspec_report_implement_prompter`
- `/smartspec_quality_gate`

**Critical requirement:** This workflow MUST generate tasks in a format that reduces false negatives in strict verification.

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
  - MAY create or update `specs/<category>/<spec-id>/tasks.md`.
  - MUST NOT modify any other governed files.

---

## Invocation

### CLI

```bash
/smartspec_generate_tasks <specs/<category>/<spec-id>/spec.md|.../plan.md|.../ui-spec.json> [--apply] [--validate-only] [--json]
```

### Kilo Code

```bash
/smartspec_generate_tasks.md <specs/<category>/<spec-id>/spec.md|.../plan.md|.../ui-spec.json> [--apply] [--validate-only] [--json] --platform kilo
```

---

## Inputs

### Positional

- `--spec` (positional primary input):
  - `specs/<category>/<spec-id>/spec.md`
  - or `specs/<category>/<spec-id>/plan.md`
  - or `specs/<category>/<spec-id>/ui-spec.json`

### Input validation (mandatory)

- Input MUST exist.
- Must resolve under `specs/**`.
- Must not escape via symlink.
- Must derive `spec-id` from folder name or file header (`^[a-z0-9_\-]{3,64}$`).

---

## Flags

### Universal flags (must support)

| Flag | Required | Description |
|---|---|---|
| `--config` | No | Config path (default: `.spec/smartspec.config.yaml`) |
| `--lang` | No | `th` \| `en` \| `auto` |
| `--platform` | No | `cli` \| `kilo` \| `ci` \| `other` |
| `--out` | No | Base output directory for reports (must pass safety checks) |
| `--json` | No | Emit machine-readable summary JSON |
| `--quiet` | No | Reduce logs |

### Workflow-specific flags

| Flag | Required | Description |
|---|---|---|
| `--apply` | No | Enable writes to governed artifacts (`tasks.md`) |
| `--validate-only` | No | Run preview + validation only (no writes to `specs/**`) |
| `--skip-duplication-check` | No | Skip pre-generation duplication validation (not recommended) |
| `--registry-roots` | No | Additional registry dirs to check for duplicates (comma-separated) |

### Flag usage notes

- **Config-first:** prefer setting defaults in `.spec/smartspec.config.yaml`.
- **Preview-first:** always run without `--apply` before applying.
- **No secrets:** never pass tokens/keys as CLI args.

---

## Behavior

### 0) Determine target paths

Given `specs/<category>/<spec-id>/<input>`:

- target governed file: `specs/<category>/<spec-id>/tasks.md`
- preview file: `.spec/reports/generate-tasks/<run-id>/preview/<spec-id>/tasks.md`
- best-effort patch: `.spec/reports/generate-tasks/<run-id>/diff/<spec-id>.patch`

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
- Exit `1`: present duplicates; user must decide reuse/justify/cancel; MUST NOT proceed without confirmation.

### 2) Produce task graph

- Convert scope into milestones + tasks.
- Ensure every milestone has verifiable outputs.
- Ensure every task has at least **one** machine-parseable evidence hook line (`evidence:`).

### 3) Evidence hook policy (MUST)

To prevent “implement แล้ว แต่ verify ไม่เจอ”, tasks MUST include evidence hooks that are:

- **specific** (file path + symbol/contains/heading when applicable)
- **repo-relative** (no absolute paths)
- **quote-safe** (values with spaces MUST use double quotes)

Canonical line syntax:

- `evidence: <type> <key>=<value> <key>=<value> ...`

Supported types MUST align with strict verifier:

- `code` (required: `path`; optional: `symbol`, `contains`)
- `test` (required: `path`; optional: `contains`, `command`)
- `docs` (required: `path`; optional: `heading`, `contains`)
- `ui` (required: `screen`; optional: `route`, `component`, `states`)

**Rule:** generator SHOULD prefer `symbol=` or `contains=` over directory-only hooks to reduce ambiguity.

### 4) Existing tasks.md merge + normalization (MANDATORY)

If `specs/<category>/<spec-id>/tasks.md` already exists:

The workflow MUST treat it as the starting point and produce a refined output that:

1) **Preserves stable task IDs** (do not renumber existing tasks unless necessary)
2) **Avoids duplication** (do not re-add already existing tasks)
3) **Preserves human notes** that do not conflict with canonical format
4) **Normalizes evidence format** to verifier-compatible lines

#### 4.1 What counts as “non-canonical evidence”

Any of the following patterns MUST be normalized in preview output:

- `- **Evidence Hooks:**` blocks
- `- **Evidence:** <free text>` bullets
- `- evidence: file_exists ...` / `test_exists ...` / `command ...` (legacy / non-compliant)

#### 4.2 Normalization rule

- In preview output, convert non-canonical evidence into canonical `evidence:` lines wherever it is safe to do so.
- If safe conversion is not possible, keep the original note AND add a clear remediation note in the report pointing to `/smartspec_migrate_evidence_hooks`.

> IMPORTANT: The workflow MUST NOT generate placeholder paths like `COMMAND_NOT_SUPPORTED` or `path=???` because it causes systematic false negatives.

#### 4.3 Apply semantics when file exists

- With `--apply`, the workflow MUST write a **fully normalized** `tasks.md` that follows the templates in §10.
- The workflow MUST generate a best-effort diff patch and include it in the report bundle.
- Writes MUST be atomic (temp + rename) and must not escape via symlink.

### 5) Preview & report (always)

Write:

- `.spec/reports/generate-tasks/<run-id>/preview/<spec-id>/tasks.md`
- `.spec/reports/generate-tasks/<run-id>/diff/<spec-id>.patch` (best-effort)
- `.spec/reports/generate-tasks/<run-id>/report.md`
- `.spec/reports/generate-tasks/<run-id>/summary.json` (if `--json`)

### 6) Post-generation validation (MANDATORY)

After generating the preview and before applying, the agent MUST validate the generated tasks.

**Validation Command:**

```bash
python3 .spec/scripts/validate_tasks_enhanced.py \
  --tasks .spec/reports/generate-tasks/<run-id>/preview/<spec-id>/tasks.md \
  --spec specs/<category>/<spec-id>/spec.md \
  --check-duplicates --threshold 0.8
```

**Validation Rules:**

- Exit `0`: may proceed with `--apply`.
- Exit `1`: MUST NOT apply; report must include full validator output.

**Additional MUST-checks** (validator responsibility):

- Every task has ≥ 1 `evidence:` line
- All `evidence:` lines parse as `type key=value ...`
- Evidence `path=` is relative and does not contain `..`
- Evidence type is in {`code`,`test`,`docs`,`ui`} (or explicitly allowed by config)

### 7) Apply (only with `--apply` and if validation passes)

- Update `specs/<category>/<spec-id>/tasks.md`.
- MUST NOT modify other files.

### 8) Recommended next steps (canonical chain)

After tasks are generated:

- implement: `/smartspec_implement_tasks <tasks.md>`
- strict verify: `/smartspec_verify_tasks_progress_strict <tasks.md>`
- sync checkboxes: `/smartspec_sync_tasks_checkboxes <tasks.md> --apply`

---

## Implementation notes (for agents)

- Duplication detection and tasks validation scripts are project-local and referenced explicitly in this workflow.
- Any workflow-generated helper scripts (if needed) MUST be written under `.smartspec/generated-scripts/**`.

---

## 10) `tasks.md` Content Templates (MUST)

The agent executing this workflow MUST output tasks using these templates.

### 10.1 Header Template

```markdown
| spec-id | source | generated_by | updated_at |
|---|---|---|---|
| `<spec-id>` | `<spec.md|plan.md|ui-spec.json>` | `smartspec_generate_tasks:7.1.0` | `<ISO_DATETIME>` |
```

### 10.2 Tasks Section Skeleton

```markdown
## Tasks

> Notes:
> - Checkbox [x] is not evidence. Evidence must be declared with `evidence:` lines.
> - Evidence values with spaces must be quoted, e.g. contains="hello world".
```

### 10.3 Task Item Template (Verifier-compatible)

Each task item under `## Tasks` MUST follow this template.

```markdown
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

- `<TASK-ID>` MUST be stable and unique within the spec (recommended: `TSK-<spec-id>-NNN`)
- Do NOT wrap the task title in bold (keeps parsing simple)
- Evidence lines MUST start with `evidence:` exactly

### 10.4 Evidence patterns (examples)

#### Code

```markdown
evidence: code path=packages/api/src/auth/login_handler.ts symbol=loginWithPassword
evidence: code path=packages/api/src/middleware/auth_jwt.ts contains="Authorization"
```

#### Tests

```markdown
evidence: test path=packages/api/test/auth/login.test.ts contains="returns 200 with access token"
evidence: test path=packages/api/test/auth/login.test.ts command="pnpm test --filter auth"
```

> `command` is never executed by strict verification; it is recorded as context only.

#### Docs

```markdown
evidence: docs path=docs/api/auth.md heading="POST /auth/login"
```

#### UI

```markdown
evidence: ui screen=Login route=/login component=LoginForm states=loading,error,success
```

---

## 11) Existing file upgrade guarantees

When the workflow is run against a spec that already has `tasks.md`, the preview output MUST:

- rewrite legacy **Evidence Hooks** blocks into canonical `evidence:` lines
- preserve the original intent and keep any human-readable notes as comments/notes
- maintain task IDs and ordering as much as possible

With `--apply`, the written `tasks.md` MUST conform to §10 templates.

If the workflow cannot safely convert some legacy evidence, it MUST:

- keep the original text
- add a remediation block in report.md recommending:

  - `/smartspec_migrate_evidence_hooks <tasks.md>`

---

# End of workflow doc
```

