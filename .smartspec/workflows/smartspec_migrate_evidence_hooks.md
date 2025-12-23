```md
---
workflow_id: smartspec_migrate_evidence_hooks
version: "6.4.1"
status: active
category: a2ui
platform_support:
  - cli
  - kilo
requires_apply: false
---

# /smartspec_migrate_evidence_hooks

## 1. Description

Migrates descriptive evidence in a `tasks.md` file to standardized evidence hooks.

This workflow addresses a critical gap in legacy `tasks.md` files where the evidence section contains natural language descriptions instead of the standardized `evidence: type key=value` format.

**Primary target:** compatibility with `/smartspec_verify_tasks_progress_strict`.

---

## 2. Why It's Important

- **Enables Automation:** Standardized hooks are machine-readable, allowing automated verification.
- **Improves Accuracy:** Reduces ambiguity of natural language; reduces false negatives.
- **Reduces Manual Effort:** Automates conversion of many tasks.
- **Maintains Consistency:** Enforces a single consistent evidence format.

---

## 3. How It Works

The workflow operates in two modes: **preview** and **apply**.

1) **Parsing:** Reads the target `tasks.md` and identifies tasks.
2) **Identification:** Finds evidence that is free-form text or legacy evidence that is not strict-verifier compatible.
3) **AI-Powered Conversion:** Converts descriptive evidence + task text into one or more standardized hooks.
4) **Suggestion Generation:** Emits **strict-verifier-compatible evidence lines** by default.
5) **Preview Mode (Default):** Shows a diff-like output; does **not** modify the original file.
6) **Apply Mode (`--apply`):** Modifies `tasks.md` by replacing descriptive evidence with standardized hooks.

---

## 4. Evidence Compatibility Policy (MUST)

To prevent “implement แล้ว แต่ verify ไม่เจอ”, the migrated hooks MUST default to strict verifier types:

- `code`
- `test`
- `docs`
- `ui`

### Mapping legacy concepts to strict types

If the AI would otherwise return evidence like `file_exists`, `api_route`, `db_schema`, etc., it MUST map them to strict-verifier hooks:

- `file_exists path=docs/openapi.yaml` → `evidence: docs path=docs/openapi.yaml`
- `api_route path=src/routes/auth.ts route=/auth/register` → `evidence: code path=src/routes/auth.ts contains="/auth/register"`
- `db_schema path=prisma/schema.prisma model=User` → `evidence: code path=prisma/schema.prisma contains="model User"`
- `file_contains path=README.md content=...` → `evidence: docs path=README.md contains="..."`

**Rule:** never emit placeholders like `path=???` or `COMMAND_NOT_SUPPORTED`.

---

## 5. Parameters

| Parameter | Type | Description | Required |
| :--- | :--- | :--- | :--- |
| `--tasks-file` | `string` | Path to the `tasks.md` file to migrate. | Yes |
| `--apply` | `boolean` | If true, applies changes directly to the file. Defaults to false (preview). | No |
| `--model` | `string` | AI model for conversion (e.g., `gpt-4.1-mini`). Defaults to `gpt-4.1-mini`. | No |

---

## 6. Example Usage

### Preview Changes

```bash
/smartspec_migrate_evidence_hooks \
  --tasks-file "specs/core/spec-core-001-authentication/tasks.md"
```

### Apply Changes

```bash
/smartspec_migrate_evidence_hooks \
  --tasks-file "specs/core/spec-core-001-authentication/tasks.md" \
  --apply
```

---

## 7. Output expectations

### Preview

- Prints a diff-like summary.
- Writes preview artifacts only under `.spec/reports/migrate-evidence-hooks/<run-id>/**`.

### Apply

- Updates the governed `tasks.md` file.
- Must be atomic (temp + rename).

---

## 8. Implementation

Implemented in: `.smartspec/scripts/migrate_evidence_hooks.py`

---

# End of workflow doc
```

