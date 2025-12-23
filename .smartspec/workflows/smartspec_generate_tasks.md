---
description: Convert spec.md (or plan.md) → tasks.md with duplication prevention and strict-verifier-compatible evidence hooks.
version: 7.1.4
workflow: /smartspec_generate_tasks
category: core
---

# smartspec_generate_tasks

> **Canonical path:** `.smartspec/workflows/smartspec_generate_tasks.md`
> **Version:** 7.1.4
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

**Hard rule:** the workflow MUST NOT assume `.spec/scripts/**` exists.

- If a helper script is missing, it MUST log a warning and continue in preview.
- For `--apply`, missing validator MUST hard-fail (to prevent writing invalid `tasks.md`).

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

## Behavior (summary)

1) Determine target paths (governed + preview)
2) Optional duplication check (if helper exists)
3) Generate/normalize tasks in canonical format
4) Validate preview using `.smartspec/scripts/validate_tasks_enhanced.py`
5) Apply only if `--apply` and validation passes

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

### Required / allowed keys

- All types: `path` (required)
- `code`: `symbol`, `contains`, `regex`
- `test`: `contains`, `regex`, `command`
- `docs`: `contains`, `heading`, `regex`
- `ui`: `contains`, `selector`, `regex`

### Hard rules (prevent verify false-negatives)

- `heading=` is ONLY allowed for `docs`.
- `path=` MUST be repo-relative (no absolute paths, no traversal, no spaces).
- Do NOT put shell commands into `path=`.
- For `code/test/ui`: `path` alone is too weak. Provide at least one matcher (`contains|symbol|regex|selector`).

---

## Quote-safe encoding rules (CRITICAL)

Many repos store config/spec content in JSON/YAML where the exact text contains quotes.
If you write an evidence line like:

```md
evidence: code path=package.json contains="node": "22.x"
```

…it will almost certainly break strict parsing (the value is not a single token) and cause the verifier to reject the evidence line.

### Correct patterns

**Pattern A (recommended): wrap the entire fragment in single quotes**

```md
evidence: code path=package.json contains='"node": "22.x"'
```

**Pattern B: escape inner quotes inside a double-quoted value**

```md
evidence: code path=package.json contains="\"node\": \"22.x\""
```

**Pattern C: avoid quotes by searching for a stable key only (weaker but sometimes ok)**

```md
evidence: code path=package.json contains="\"node\""
```

### Generator rule (MUST)

When generating evidence hooks:

- If `contains` includes `"` or `:` with surrounding quotes, ALWAYS emit Pattern A or B.
- NEVER emit a `contains=` value that would become multiple tokens under shell-style splitting.

---

## Mapping rule (reduces false-negatives)

If the artifact is a specification/contract/doc (e.g., `openapi.yaml`, `*.md`, `docs/**`), prefer:

- `evidence: docs ...`

(not `code`).

---

## Legacy patterns to eliminate (MUST NOT generate)

These formats cause verifier false-negatives and MUST be normalized:

- Task IDs wrapped in bold: `- [ ] **TSK-...** ...`
- Per-task headings like `### TSK-...`
- Blocks like `**Evidence Hooks:**` followed by natural language bullets
- Evidence lines without the `evidence:` prefix

---

## Post-generation validation (MANDATORY)

After generating preview and before applying, validate using the project validator:

```text
python3 .smartspec/scripts/validate_tasks_enhanced.py --tasks .spec/reports/generate-tasks/<run-id>/preview/<spec-id>/tasks.md --spec specs/<category>/<spec-id>/spec.md
```

- If validator missing:
  - Preview: warn + report
  - Apply: hard-fail

---

## Apply (only with --apply)

- Update `specs/<category>/<spec-id>/tasks.md` atomically (temp + rename).
- MUST NOT modify other files.

---

# End of workflow doc

