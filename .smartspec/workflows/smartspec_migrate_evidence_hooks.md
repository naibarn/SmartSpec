---
workflow_id: smartspec_migrate_evidence_hooks
version: "6.4.4"
status: active
category: a2ui
platform_support:
  - cli
  - kilo
requires_apply: false
---

# /smartspec_migrate_evidence_hooks

## Description

Migrates legacy/descriptive evidence in a `tasks.md` file to **strict-verifier-compatible** evidence hooks:

- `evidence: code ...`
- `evidence: test ...`
- `evidence: docs ...`
- `evidence: ui ...`

Also performs **safe structural normalization** to reduce validation/verification false-negatives.

---

## Governance contract

- Preview-first by default.
- Governed file writes require `--apply`.

### Write scopes

Allowed writes:

- Safe outputs (preview reports): `.spec/reports/migrate-evidence-hooks/**`

Allowed governed writes (ONLY with `--apply`):

- `specs/**/tasks.md`

Forbidden writes:

- Any other governed artifacts (spec.md, plan.md, registries)
- Any path outside config allowlist / inside denylist

---

## Invocation

### CLI

```bash
/smartspec_migrate_evidence_hooks --tasks-file specs/<category>/<spec-id>/tasks.md
```

### Kilo Code

```bash
/smartspec_migrate_evidence_hooks.md --tasks-file specs/<category>/<spec-id>/tasks.md --platform kilo
```

---

## Parameters

| Parameter | Type | Description | Required |
| :--- | :--- | :--- | :--- |
| `--tasks-file` | `string` | Path to the `tasks.md` file to migrate. | Yes |
| `--apply` | `boolean` | If true, applies changes directly to the file. Defaults to false (preview). | No |
| `--out` | `string` | Optional output directory base (must pass safety checks). | No |

---

## Structural normalization (NEW in 6.4.4)

These fixes are deterministic and safe:

1) **YAML front-matter → Header table**

If the file begins with:

```md
---
spec_id: ...
source: ...
---
```

…it is converted into the canonical header table:

```md
| spec-id | source | generated_by | updated_at |
|---|---|---|---|
| <spec-id> | <source> | <generated_by> | <updated_at> |
```

2) **Ensure exactly one `## Tasks`**

- If missing: insert `## Tasks` after the header.
- If duplicated: keep the first, remove later duplicates.

3) **Remove noise lines inside Tasks section**

- Lines like `$/a` inside Tasks are removed.

---

## Evidence normalization (NEW in 6.4.4)

1) **Bullet-evidence normalization**

Convert:

```md
- evidence: code path=... contains="..."
```

to:

```md
evidence: code path=... contains="..."
```

This is critical because strict verifier/validator only counts lines that start with `evidence:`.

---

## Evidence compatibility policy

### Types

- `code`
- `test`
- `docs`
- `ui`

### Key rules

- `path=` is REQUIRED.
- `heading=` is ONLY allowed for `docs`.
- Values with spaces MUST be quoted.
- Never emit placeholders like `path=???`.

### Quote-safe rules

If a value contains quotes/spaces (JSON fragment), migration MUST rewrite it so it becomes a single token.

Preferred:

```md
evidence: code path=package.json contains='"node": "22.x"'
```

### Fix rules for known false-negative patterns

- `contains=exists` → replace with `regex="."` (existence-only proof)
- Glob characters in `path=` → keep but flag as needing manual remediation (do not guess file list)
- `heading=` on non-docs → convert to docs when safe, otherwise flag

---

## Outputs

### Preview (default)

- Writes preview artifacts under `.spec/reports/migrate-evidence-hooks/<run-id>/**`.
- Does NOT modify `tasks.md`.

### Apply (`--apply`)

- Updates the governed `tasks.md` file.
- Must be atomic (temp + rename).
- Must preserve task IDs and checkbox state.

---

## Implementation

Implemented in: `.smartspec/scripts/migrate_evidence_hooks.py` (v6.4.4)

---

# End of workflow doc

