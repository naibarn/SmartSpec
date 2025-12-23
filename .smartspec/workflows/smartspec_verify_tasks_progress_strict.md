---
description: "Strict evidence-only verification using parseable evidence hooks (evidence: type key=value...)."
version: 6.2.2
workflow: /smartspec_verify_tasks_progress_strict
category: verify
---

# smartspec_verify_tasks_progress_strict

> **Canonical path:** `.smartspec/workflows/smartspec_verify_tasks_progress_strict.md`
> **Version:** 6.2.2
> **Category:** verify
> **Writes:** reports only (`.spec/reports/**`)

## Purpose

Verify progress for a given `tasks.md` using **evidence-only checks**.

This workflow MUST:

- Treat checkboxes as **non-authoritative** (they are not evidence)
- Verify each task via explicit evidence hooks (`code|test|ui|docs`)
- Produce an auditable report under `.spec/reports/verify-tasks-progress/**`
- Never modify `tasks.md` (checkbox updates belong to `/smartspec_sync_tasks_checkboxes`)

---

## Governance contract

This workflow MUST follow:

- `knowledge_base_smartspec_handbook.md`
- `.spec/smartspec.config.yaml` (config-first)

### Write scopes (enforced)

Allowed writes:

- Safe outputs (reports): `.spec/reports/verify-tasks-progress/**`

Forbidden writes (must hard-fail):

- Any governed file under `specs/**`
- `.spec/SPEC_INDEX.json`, `.spec/WORKFLOWS_INDEX.yaml`
- Any path outside config `safety.allow_writes_only_under`
- Any path under config `safety.deny_writes_under`
- Any runtime source tree modifications

### Network policy

- MUST respect config `safety.network_policy.default=deny`.
- MUST NOT fetch external URLs referenced in tasks/spec.

---

## Evidence hook grammar (MUST)

Evidence lines MUST be parseable:

```text
evidence: <type> key=value key="value with spaces" ...
```

### Allowed types

- `code`
- `test`
- `docs`
- `ui`

### Allowed keys (strict)

All types:

- `path` (required)

Additional keys:

- `code`: `symbol`, `contains`, `regex`
- `test`: `contains`, `regex`, `command`
- `docs`: `contains`, `heading` (**only docs may use `heading`**), `regex`
- `ui`: `contains`, `selector`, `regex`

---

## Evidence lint rules (reduce false-negatives)

The verifier MUST mark an evidence line as **invalid** (and therefore cannot complete the task) if any of these occur:

1) **Unparseable payload**
   - Any evidence line that cannot be tokenized using shell-style parsing (shlex-like) is invalid.
   - Common cause: JSON/YAML fragments with quotes not wrapped/escaped.

2) **Illegal key usage**
   - `heading=` on non-`docs` evidence is invalid.

3) **Glob path**
   - `path` containing `*`, `?`, `[` or `]` is invalid unless the implementation explicitly supports glob expansion.
   - Remediation: replace with a concrete file path or use `/smartspec_migrate_evidence_hooks`.

4) **Weak/placeholder matchers**
   - `contains=exists` (or `contains="exists"`) is invalid.
   - Remediation: replace with a real fragment (`contains=`) or use `regex="."` for existence-only proof.

5) **Path safety**
   - Absolute paths, traversal (`..`), or paths that look like commands are invalid.

The report MUST include remediation hints for each invalid evidence line.

---

## Legacy compatibility (bounded)

Some `tasks.md` files contain legacy evidence blocks like:

- `Evidence Hooks:` / `**Evidence Hooks:**`
- bullets like `- Code: <path> contains "..."`
- `**Evidence:** <free text>`

Policy:

- If a legacy line can be deterministically converted into a canonical hook (Code/Test/Docs/UI + path + matcher), the verifier MAY treat it as equivalent.
- Otherwise, legacy evidence is invalid.

**Strong recommendation:** normalize using `/smartspec_migrate_evidence_hooks`.

---

## Invocation

### CLI

```bash
/smartspec_verify_tasks_progress_strict <path/to/tasks.md> [--report-format <md|json|both>] [--json]
```

### Kilo Code

```bash
/smartspec_verify_tasks_progress_strict.md <path/to/tasks.md> [--report-format <md|json|both>] [--json] --platform kilo
```

---

## Outputs

- `.spec/reports/verify-tasks-progress/<run-id>/report.md`
- `.spec/reports/verify-tasks-progress/<run-id>/summary.json`

---

## Implementation

Implemented in: `.smartspec/scripts/verify_evidence_strict.py`

---

# End of workflow doc

