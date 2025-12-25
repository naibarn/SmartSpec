---
workflow_id: smartspec_migrate_evidence_hooks
version: "6.6.0"
status: active
category: maintenance
platform_support:
  - cli
  - kilo

# Governance
requires_apply: false

# Allowed writes (preview-only)
writes:
  preview_only:
    - ".spec/reports/migrate-evidence-hooks/**"
  governed_on_apply:
    - "specs/**/tasks.md"

network:
  default: deny
---

# /smartspec_migrate_evidence_hooks

## Objective

Migrate and normalize **legacy / non-canonical evidence hooks** inside a `specs/**/tasks.md` so that:

- strict validators accept the file
- `/smartspec_verify_tasks_progress_strict` can reliably detect implemented work
- false-negative verification (“ทำแล้วแต่ verify ไม่เจอ”) is reduced

This workflow is the **only** place that should auto-fix evidence formatting. Validators must remain read-only.

---

## Canonical evidence hook contract

### Required canonical syntax

Every evidence line MUST be parseable as:

`evidence: <type> <key>=<value> <key>=<value> ...`

- `<type>` MUST be one of: `code`, `test`, `docs`, `ui`
- Every token after `<type>` MUST be `key=value`
- Values with spaces MUST be wrapped in double quotes
- `path=` values MUST be repo-relative (no absolute paths, no `..`, no globs)

### Type semantics

- `code` evidence is for runtime / source files (e.g., `.ts`, `.go`, `.java`)
  - keys: `path`, `symbol`, `contains`, `regex`
- `test` evidence is for test/bench files + the command to run them
  - keys: `path`, `command`, `contains`, `regex`
  - IMPORTANT: `command` is **recorded only**, never executed
- `docs` evidence is for documentation / specs
  - keys: `path`, `heading`, `contains`, `regex`
- `ui` evidence is for UI artifacts (JSON mode)
  - keys: `path`, `selector`, `contains`, `regex`

### MUST fix these common legacy problems

1) **Command mistakenly placed into `path=`**

Bad:
- `evidence: test path="npm run build"`

Good:
- `evidence: test path=package.json command="npm run build"`

2) **Docs evidence mislabeled as code**

Bad:
- `evidence: code path=docs/accessibility-checklist.md heading="ARIA"`

Good:
- `evidence: docs path=docs/accessibility-checklist.md heading="ARIA"`

3) **Unsupported legacy types** (examples)

- `file_exists path=...` → `docs|code path=...`
- `api_route route=/... path=...` → `code path=... contains="/..."` (or `docs path=openapi.yaml contains=...` if no code path)
- `db_schema model=User path=prisma/schema.prisma` → `code path=prisma/schema.prisma contains="model User"`
- `command command="..."` → `test path=<anchor> command="..."`

---

## Governance contract

### Preview-first (default)

When **NOT** using `--apply`:

- MUST NOT modify `specs/**/tasks.md`
- MUST write ONLY to:
  - `.spec/reports/migrate-evidence-hooks/<run-id>/preview/**`
  - `.spec/reports/migrate-evidence-hooks/<run-id>/diff.patch`
  - `.spec/reports/migrate-evidence-hooks/<run-id>/report.md`

### Apply mode

When using `--apply`:

- MAY update exactly one governed file: the provided `specs/**/tasks.md`
- MUST create a backup under:
  - `.spec/reports/migrate-evidence-hooks/<run-id>/backup/**`
- MUST apply changes atomically (temp file + rename)
- MUST NOT create helper scripts (no root scripts, no `.spec/scripts/*`)

### Network policy

- Network deny-by-default.
- This workflow MUST NOT fetch or call external URLs.

---

## Implementation

### Script

- Canonical script path (repo):
  - `.smartspec/scripts/migrate_evidence_hooks.py`

Notes:
- The script MUST be the only writer.
- Validators (`validate_evidence_hooks.py`, `validate_tasks_enhanced.py`) MUST NOT perform edits.

---

## Invocation

### Preview

**CLI:**
```bash
/smartspec_migrate_evidence_hooks --tasks-file specs/core/spec-core-001-authentication/tasks.md
```

**Kilo Code:**
```bash
/smartspec_migrate_evidence_hooks.md --tasks-file specs/core/spec-core-001-authentication/tasks.md --platform kilo
```

### Apply

**CLI:**
```bash
/smartspec_migrate_evidence_hooks --tasks-file specs/core/spec-core-001-authentication/tasks.md --apply
```

**Kilo Code:**
```bash
/smartspec_migrate_evidence_hooks.md --tasks-file specs/core/spec-core-001-authentication/tasks.md --apply --platform kilo
```

---

## Required follow-up checks

After preview (or after apply), run both validators:

1) Evidence hook syntax
```bash
python3 .smartspec/scripts/validate_evidence_hooks.py --tasks specs/core/spec-core-001-authentication/tasks.md
```

2) Tasks structure
```bash
python3 .smartspec/scripts/validate_tasks_enhanced.py --tasks specs/core/spec-core-001-authentication/tasks.md
```

Then run strict verification:

**CLI:**
```bash
/smartspec_verify_tasks_progress_strict specs/core/spec-core-001-authentication/tasks.md --report-format both --json
```

**Kilo Code:**
```bash
/smartspec_verify_tasks_progress_strict.md specs/core/spec-core-001-authentication/tasks.md --report-format both --json --platform kilo
```

---

# End of file

