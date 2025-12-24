---
workflow_id: smartspec_migrate_evidence_hooks
version: "6.6.0"
status: active
category: a2ui
platform_support:
  - cli
  - kilo
requires_apply: false
writes:
  - preview: ".spec/reports/migrate-evidence-hooks/**"
  - apply: "specs/**/tasks.md"  # governed; only with --apply
---

# /smartspec_migrate_evidence_hooks

## Purpose

Normalize / migrate legacy evidence into **strict-verifier-compatible evidence hooks** so that `/smartspec_verify_tasks_progress_strict` can reliably detect implemented work.

This workflow is designed to eliminate false-negatives caused by:
- bullet evidence (`- evidence:`)
- legacy types (`file_exists`, `api_route`, `db_schema`, `command`)
- command-ish evidence accidentally put into `path=`

**Output goal:** each task contains one or more canonical hooks:

- `evidence: code ...`
- `evidence: test ...`
- `evidence: docs ...`
- `evidence: ui ...`

## Governance contract (MUST)

- **Preview-first by default** (no governed writes).
- Governed writes under `specs/**` require `--apply`.
- All preview outputs MUST be written only under `.spec/reports/migrate-evidence-hooks/<run-id>/**`.
- MUST NOT create helper scripts in `.spec/scripts` or repo root.
- Network is deny-by-default.

## Canonical evidence hook policy (MUST)

### Required syntax

`evidence: <type> <key>=<value> <key>=<value> ...`

- `<type>` MUST be one of: `code`, `test`, `docs`, `ui`
- Values with spaces MUST be quoted with double quotes
- Paths MUST be repo-relative and MUST NOT contain `..`

### Type mapping rules (MUST)

When encountering legacy concepts, map to strict types:

- `file_exists path=docs/openapi.yaml` → `evidence: docs path=docs/openapi.yaml`
- `api_route route=/auth/register path=src/routes/auth.ts` → `evidence: code path=src/routes/auth.ts contains="/auth/register"`
- `db_schema path=prisma/schema.prisma model=User` → `evidence: code path=prisma/schema.prisma contains="model User"`
- `command command="npm test"` → `evidence: test path=package.json command="npm test"`

### Command-in-path fix (MUST)

If a `test` hook contains a command inside `path=...` (e.g. `evidence: test path="npm test"`) the workflow MUST convert it to:

`evidence: test path=<anchor-file> command="npm test"`

(Anchor file selection heuristics are implemented in the script.)

## Inputs

- `--tasks-file` (required): path to `specs/**/tasks.md`

## Outputs

### Preview mode (default)

Writes:
- `.spec/reports/migrate-evidence-hooks/<run-id>/preview/<tasks-file>`
- `.spec/reports/migrate-evidence-hooks/<run-id>/diff.patch`
- `.spec/reports/migrate-evidence-hooks/<run-id>/report.md`

### Apply mode (`--apply`)

- Atomically updates the governed tasks file at `specs/**/tasks.md`
- Writes a backup under `.spec/reports/migrate-evidence-hooks/<run-id>/backup/<tasks-file>`

## Implementation

- Script: `.smartspec/scripts/migrate_evidence_hooks.py`

## Usage

### Preview

**CLI:**
```bash
/smartspec_migrate_evidence_hooks \
  --tasks-file specs/core/spec-core-001-authentication/tasks.md
```

**Kilo Code:**
```bash
/smartspec_migrate_evidence_hooks.md \
  --tasks-file specs/core/spec-core-001-authentication/tasks.md \
  --platform kilo
```

### Apply

**CLI:**
```bash
/smartspec_migrate_evidence_hooks \
  --tasks-file specs/core/spec-core-001-authentication/tasks.md \
  --apply
```

**Kilo Code:**
```bash
/smartspec_migrate_evidence_hooks.md \
  --tasks-file specs/core/spec-core-001-authentication/tasks.md \
  --apply \
  --platform kilo
```

## Recommended follow-ups

1) Validate evidence hooks on the **preview** file:

```bash
python3 .smartspec/scripts/validate_evidence_hooks.py --tasks .spec/reports/migrate-evidence-hooks/<run-id>/preview/specs/core/spec-core-001-authentication/tasks.md
```

2) Run strict verification after applying:

```bash
/smartspec_verify_tasks_progress_strict specs/core/spec-core-001-authentication/tasks.md
```

---

# End of workflow doc

