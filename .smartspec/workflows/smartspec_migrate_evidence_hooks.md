---
workflow_id: smartspec_migrate_evidence_hooks
version: "6.4.3"
status: active
category: a2ui
platform_support:
  - cli
  - kilo
requires_apply: false
---

# /smartspec_migrate_evidence_hooks

## 1. Description

Migrates legacy/descriptive evidence in a `tasks.md` file to **strict-verifier-compatible** evidence hooks:

- `evidence: code ...`
- `evidence: test ...`
- `evidence: docs ...`
- `evidence: ui ...`

This workflow exists because legacy `tasks.md` files often include ambiguous text like:

- `**Evidence Hooks:**\n- Code: ...` (not machine-parseable)
- `Code: <path> contains <text>` (not in `evidence:` grammar)
- `**Evidence:** ...` (free text)

**Primary target:** make `tasks.md` compatible with `/smartspec_verify_tasks_progress_strict` and reduce false-negatives.

---

## 2. Governance contract

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

## 3. Invocation

### CLI

```bash
/smartspec_migrate_evidence_hooks --tasks-file specs/<category>/<spec-id>/tasks.md
```

### Kilo Code

```bash
/smartspec_migrate_evidence_hooks.md --tasks-file specs/<category>/<spec-id>/tasks.md --platform kilo
```

---

## 4. Parameters

| Parameter | Type | Description | Required |
| :--- | :--- | :--- | :--- |
| `--tasks-file` | `string` | Path to the `tasks.md` file to migrate. | Yes |
| `--apply` | `boolean` | If true, applies changes directly to the file. Defaults to false (preview). | No |
| `--out` | `string` | Optional output directory base (must pass safety checks). | No |

---

## 5. Evidence compatibility policy (MUST)

### 5.1 Types

To prevent “implement แล้ว แต่ verify ไม่เจอ”, migrated hooks MUST use strict verifier types:

- `code`
- `test`
- `docs`
- `ui`

### 5.2 Key rules

- `path=` is REQUIRED.
- `heading=` is ONLY allowed for `docs`.
- Values with spaces MUST be quoted.
- Never emit placeholders like `path=???`.

### 5.3 Quote-safe rules (CRITICAL)

If the value contains quotes/spaces (e.g. JSON fragment), migration MUST rewrite it so it becomes a single token.

Preferred pattern:

```md
evidence: code path=package.json contains='"node": "22.x"'
```

### 5.4 Fix rules for known false-negative patterns

The workflow MUST detect and fix these patterns:

- `contains=exists` or `contains="exists"`
  - Replace with `regex="."` (existence-only proof) and drop `contains`.

- Glob paths in `path=` (e.g. `**/*.test.ts`)
  - Mark as invalid and emit a remediation note (glob expansion is verifier-specific).
  - Preferred fix: replace with concrete file(s) or adjust to folder + matcher only if verifier supports directory scans.

- `heading=` on evidence types other than `docs`
  - Convert to `evidence: docs ... heading="..."` when safe.

---

## 6. Legacy formats the workflow MUST convert

### 6.1 Legacy block header

If the task contains something like:

- `Evidence Hooks:`
- `**Evidence Hooks:**`
- `Evidence:`
- `**Evidence:**`

the workflow MUST remove the legacy header and replace the contents with canonical `evidence:` lines.

### 6.2 Legacy bullet patterns (deterministic conversions)

The workflow MUST detect and convert these patterns even without AI:

- `- Code: <path> contains "<text>"` → `evidence: code path=<path> contains="<text>"`
- `- Test: <path> contains "<text>"` → `evidence: test path=<path> contains="<text>"`
- `- Docs: <path> heading "<h>"` → `evidence: docs path=<path> heading="<h>"`
- `- UI: <path> contains "<text>"` → `evidence: ui path=<path> contains="<text>"`

If the legacy line is ambiguous (missing path, missing matcher), it MUST be preserved as a note and the report MUST flag it for manual remediation.

---

## 7. Outputs

### Preview (default)

- Writes preview artifacts under `.spec/reports/migrate-evidence-hooks/<run-id>/**`.
- Does NOT modify `tasks.md`.

### Apply (`--apply`)

- Updates the governed `tasks.md` file.
- Must be atomic (temp + rename).
- Must preserve task IDs and checkbox state.

---

## 8. Implementation

Implemented in: `.smartspec/scripts/migrate_evidence_hooks.py`

---

# End of workflow doc

