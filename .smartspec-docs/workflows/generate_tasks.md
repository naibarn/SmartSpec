# SmartSpec Manual: /smartspec_generate_tasks

This guide explains how to generate a high-quality `tasks.md` from a feature specification using SmartSpec.

---

## What this command does

`/smartspec_generate_tasks` converts a feature spec into a structured task plan that is ready for implementation and verification.

It typically produces:

- A `tasks.md` file with:
  - Phases
  - Task IDs (T001, T002, …)
  - Dependencies
  - Expected files to create/edit
  - Acceptance criteria
  - Suggested validation commands

Depending on your project conventions, it may also propose or generate supporting artifacts referenced by tasks (e.g., OpenAPI, data-model notes).

---

## Required input

You must provide a path to a SPEC document (usually `spec.md`).

```bash
/smartspec_generate_tasks specs/feature/spec-005-promo-system/spec.md
```

---

## Output location

By default, SmartSpec should create:

```text
specs/feature/<spec-name>/tasks.md
```

in the same folder as the input spec.

---

## SPEC_INDEX.json resolution (updated)

SmartSpec uses a SPEC index (when available) to resolve cross-spec dependencies and references.

When you do **not** provide a custom index path, the expected lookup order is:

1. `SPEC_INDEX.json` at the repository root (preferred)
2. `.smartspec/SPEC_INDEX.json` (fallback)

If no index is found:

- The command should warn clearly.
- It should still be able to generate `tasks.md` without failing.

---

## Common options (recommended)

> Your implementation may support a subset of these. This manual documents the expected behavior aligned with the updated workflows.

### 1) Dry-run / planning-only mode

```bash
/smartspec_generate_tasks specs/feature/spec-005-promo-system/spec.md --nogenerate
```

Expected behavior:

- Analyze the spec.
- Show what tasks and files would be generated.
- Do not write files.

### 2) Use a specific spec index

```bash
/smartspec_generate_tasks specs/feature/spec-005-promo-system/spec.md --specindex SPEC_INDEX.json
```

---

## Best practices

### Keep specs explicit for integrations

If the spec includes external dependencies (auth, payments, messaging), include:

- The expected service name
- API prefix/path
- Token/auth patterns (if applicable)
- Link to an existing authoritative spec

This reduces assumption prompts later.

### Use consistent task structure

A strong `tasks.md` should include for each task:

- Files to create/edit
- Clear acceptance criteria
- A validation command (if the task is testable)

---

## Example: Typical generate flow

```bash
# 1) Write or update your spec
#    specs/feature/spec-005-promo-system/spec.md

# 2) Generate tasks
/smartspec_generate_tasks specs/feature/spec-005-promo-system/spec.md

# 3) Review the task plan
#    specs/feature/spec-005-promo-system/tasks.md
```

---

## How this command fits the system

- Use this first to produce `tasks.md`.
- Then implement with:

  ```bash
  /smartspec_implement_tasks specs/feature/spec-005-promo-system/tasks.md
  ```

- Finally verify with:

  ```bash
  /smartspec_verify_tasks_progress specs/feature/spec-005-promo-system/tasks.md
  ```

---

## Troubleshooting

### “SPEC_INDEX.json not found”

This should not block generation.

Recommended fix:

- Create or move the index to repository root:

  ```text
  SPEC_INDEX.json
  ```

### Generated tasks feel too vague

Improve spec clarity:

- Add a short architecture section.
- Add explicit file/module expectations.
- Add acceptance criteria per major capabilities.

---

## Summary

Use `/smartspec_generate_tasks` to turn a well-defined spec into an actionable plan.  
A clear spec and a root-level `SPEC_INDEX.json` will significantly improve task quality and reduce assumption prompts downstream.
