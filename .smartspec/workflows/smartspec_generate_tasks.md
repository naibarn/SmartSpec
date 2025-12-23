---
description: Convert spec.md (or plan.md) → tasks.md with duplication prevention and strict-verifier-compatible evidence hooks.
version: 7.1.5
workflow: /smartspec_generate_tasks
category: core
---

# smartspec_generate_tasks

> **Canonical path:** `.smartspec/workflows/smartspec_generate_tasks.md`
> **Version:** 7.1.5
> **Status:** Active
> **Category:** core

## Purpose

Generate or **normalize** `tasks.md` from:

- `specs/<category>/<spec-id>/spec.md`
- `specs/<category>/<spec-id>/plan.md`
- `specs/<category>/<spec-id>/ui-spec.json` (A2UI)

This workflow is the canonical producer of `tasks.md` that downstream workflows can trust.

---

## Governance: preview-first & hard gates

### Write scopes (enforced)

Allowed writes:

- Safe outputs: `.spec/reports/generate-tasks/**` (always allowed)

Governed writes (ONLY with `--apply`):

- `specs/**/tasks.md`

Forbidden writes (hard-fail):

- Any other governed files (`spec.md`, `plan.md`, registries)
- Any file creation in repo root
- Any file creation outside `.spec/reports/**` in preview mode

### Validate-only hard gate (MUST)

If `--validate-only` is present:

- MUST behave as preview mode.
- MUST NOT modify `specs/**` under any circumstance.
- MUST NOT attempt “auto-fix” by writing helper scripts (e.g. `fix_evidence.py`) anywhere.
- MUST output:
  - preview tasks file to `.spec/reports/generate-tasks/<run-id>/preview/<spec-id>/tasks.md`
  - report to `.spec/reports/generate-tasks/<run-id>/report.md`
  - (optional) patch to `.spec/reports/generate-tasks/<run-id>/diff/<spec-id>.patch`

If validation fails in validate-only mode:

- MUST NOT apply.
- MUST NOT edit `specs/**/tasks.md`.
- MUST report remediation steps.

> **Kilo-specific rule:**
> - When running with `--platform kilo` and `--validate-only`, the agent must **never** propose or perform writes outside `.spec/reports/**`.

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

## Evidence hook grammar (MUST)

```text
evidence: <type> key=value key="value with spaces" ...
```

### Allowed types

- `code`
- `test`
- `docs`
- `ui`

### Key rules

- `path=` is required.
- `heading=` only allowed for `docs`.
- `contains=exists` is forbidden (causes false negatives).
- `path` must not contain glob characters (`* ? [ ]`).

---

## Quote-safe encoding rules (CRITICAL)

If the evidence value includes quotes/spaces (JSON/YAML fragments), it MUST be emitted as a single token.

Preferred:

```md
evidence: code path=package.json contains='"node": "22.x"'
```

Alternative:

```md
evidence: code path=package.json contains="\"node\": \"22.x\""
```

---

## Validation (MANDATORY)

After producing preview tasks, validate using:

```text
python3 .smartspec/scripts/validate_tasks_enhanced.py --tasks .spec/reports/generate-tasks/<run-id>/preview/<spec-id>/tasks.md --spec specs/<category>/<spec-id>/spec.md
```

Apply is allowed only when:

- `--apply` is present
- AND validation passes

---

# End of workflow doc

