---
description: SmartSpec Implement Tasks Guide (v5.2)
version: 5.2
last_updated: 2025-12-08
---

# SmartSpec Manual: /smartspec_implement_tasks

This guide explains how to use `/smartspec_implement_tasks`.

It has been **updated for SmartSpec v5.2** to align with:

- Canonical project-owned space: `.spec/`
- Canonical index: `.spec/SPEC_INDEX.json`
- Shared registries (optional): `.spec/registry/`
- Legacy root mirror: `SPEC_INDEX.json`
- Deprecated tooling index: `.smartspec/SPEC_INDEX.json`
- Optional UI JSON addendum for Penpot-aligned UI specs

The workflow remains backward-compatible with the established `SPEC_INDEX.json` schema and preserves all safe, still-valid instructions from earlier manuals.

---

## What this command does

`/smartspec_implement_tasks` executes implementation work **based on an existing `tasks.md`**.

It is designed to:

- Read tasks in a controlled scope
- Implement code changes for the selected tasks
- Avoid re-inventing shared entities by consulting canonical index/registries when available
- Update task checkboxes under defined rules
- Produce a required final summary per run

This workflow is the core execution engine after you have completed spec and task generation.

---

## Allowed file changes

The workflow may:

- Create or edit files listed in tasks
- Create new supporting files when tasks explicitly require them
- Update task checkboxes according to the rules below
- Add implementation notes when your team’s conventions allow it

The workflow should **not**:

- Rewrite `spec.md` unless a task explicitly requires an additive metadata update
- Invent new shared API/model/domain names that conflict with registries or other specs
- Move project-owned canonical artifacts into tooling folders

---

## Required input

Provide a path to `tasks.md`:

```bash
/smartspec_implement_tasks specs/feature/spec-005-promo-system/tasks.md
```

### Tasks file can be inside a folder

You can reference a nested tasks file path directly:

```bash
/smartspec_implement_tasks specs/feature/spec-004-financial-system/tasks.md
```

---

## Index and registry resolution (v5.2)

`/smartspec_implement_tasks` should **not** guess shared names, models, or API shapes when your project already defines them elsewhere.

In v5.2, the implementation flow is expected to resolve shared truth in this order (unless you pass `--index` explicitly):

1) `.spec/SPEC_INDEX.json` (canonical)  
2) `SPEC_INDEX.json` at repo root (legacy mirror)  
3) `.smartspec/SPEC_INDEX.json` (deprecated tooling index)  
4) `specs/SPEC_INDEX.json` (older layout)

If `.spec/registry/` is present, the workflow should read it to validate that tasks reference canonical:

- API names and namespaces
- data model names
- domain terms
- critical sections / cross-cutting constraints
- patterns (if your project uses a patterns registry)
- UI component names (if your project uses a UI component registry)

This workflow typically operates within the **current repo**; multi-repo resolution is usually handled upstream by validation and reindexing.

---

## UI design addendum (conditional)

If the spec is categorized as UI or includes `ui.json`:

- Treat `ui.json` as the design source of truth (Penpot-aligned).
- Implement or bind reusable components and separate business logic from UI structure.
- Do not rewrite `ui.json` unless a task explicitly requires an engineering-owned change.

Projects that do not use UI JSON are not affected.

---

## Task scope selection (updated)

This workflow supports precise implementation scope to keep large projects safe and fast.

### 1) Single task

Implement a single task by its index number.

```bash
/smartspec_implement_tasks specs/feature/spec-004-financial-system/tasks.md --task=7
```

### 2) Multiple tasks

```bash
/smartspec_implement_tasks specs/feature/spec-004-financial-system/tasks.md --tasks=7,8,9
```

### 3) Task ranges

```bash
/smartspec_implement_tasks specs/feature/spec-004-financial-system/tasks.md --range=7-12
```

### 4) Start from a task

```bash
/smartspec_implement_tasks specs/feature/spec-004-financial-system/tasks.md --from=10
```

### 5) Skip completed tasks (recommended)

```bash
/smartspec_implement_tasks specs/feature/spec-004-financial-system/tasks.md --skip-completed
```

### 6) Resume

```bash
/smartspec_implement_tasks specs/feature/spec-004-financial-system/tasks.md --resume
```

---

## Phase filtering (added)

Use phase filtering when your tasks are grouped into phases.

### 1) A single phase

```bash
/smartspec_implement_tasks specs/feature/spec-004-financial-system/tasks.md --phase=1
```

### 2) Multiple phases

```bash
/smartspec_implement_tasks specs/feature/spec-004-financial-system/tasks.md --phases=1,2
```

### 3) A phase range

```bash
/smartspec_implement_tasks specs/feature/spec-004-financial-system/tasks.md --phase-range=1-3
```

---

## Implementation modes

### Standard Mode

The default mode for most users.

### Orchestrator Mode (if available)

If your environment supports Orchestrator integration, you may enable it with:

```bash
/smartspec_implement_tasks specs/feature/spec-004-financial-system/tasks.md --kilocode
```

Expected behavior:

- The workflow attempts to activate Orchestrator.
- If Orchestrator cannot be activated, it should fall back to Standard Mode with a warning.

---

## Evidence-first implementation rules

When tasks refer to cross-spec behavior or existing system capabilities, the workflow should:

1. Read any explicitly referenced supporting specs.
2. Resolve spec IDs using (v5.2 canonical-first):
   - `.spec/SPEC_INDEX.json` (canonical)
   - `SPEC_INDEX.json` at repository root (legacy mirror)
   - `.smartspec/SPEC_INDEX.json` (deprecated fallback)
3. Search the codebase for real evidence:
   - middleware/guards
   - API clients/gateway config
   - existing domain models
   - existing UI component implementations (for UI specs)
4. Only propose new constructs when evidence and registry checks confirm no conflict.

---

## Checkbox update rules

The workflow should only check a task if:

- The required files or code changes are completed.
- The implementation matches the acceptance criteria.
- Any required tests (if listed) are created or updated.

For partial completion, the workflow may add implementation notes without checking the box.

---

## Required final summary (per run)

Each run must end with a concise summary that includes:

- Tasks attempted
- Tasks completed
- Files changed/created
- Open risks or blockers
- Suggested next command

---

## Examples

### Example 1: Phase-based implementation

```bash
# Implement Phase 1 only
/smartspec_implement_tasks specs/feature/spec-004-financial-system/tasks.md --phase=1 --skip-completed

# Continue to Phase 2 only
/smartspec_implement_tasks specs/feature/spec-004-financial-system/tasks.md --phase=2 --skip-completed
```

### Example 2: Safe iterative loop

```bash
# 1) Implement a chunk (prefer Orchestrator if available)
/smartspec_implement_tasks specs/feature/spec-004-financial-system/tasks.md --range=1-6 --skip-completed --kilocode

# 2) Verify current status (read-only)
/smartspec_verify_tasks_progress specs/feature/spec-004-financial-system/spec.md

# 3) Fix specific errors (if needed)
/smartspec_fix_errors specs/feature/spec-004-financial-system

# 4) Continue implementation
/smartspec_implement_tasks specs/feature/spec-004-financial-system/tasks.md --resume
```

### Example 3: Validate only for a phase

```bash
/smartspec_implement_tasks specs/feature/spec-004-financial-system/tasks.md --phase=1 --validate-only
```

---

## SPEC_INDEX.json resolution (v5.2)

When the workflow needs to map cross-spec dependencies or scoped files, it should resolve the index in this order:

1. Prefer `.spec/SPEC_INDEX.json` (canonical).
2. Fall back to root `SPEC_INDEX.json` (legacy mirror).
3. Fall back to `.smartspec/SPEC_INDEX.json` (deprecated tooling index).
4. Finally, check `specs/SPEC_INDEX.json` if your project still uses the older layout.

If no index is found:

- Log a warning.
- Continue with best-effort implementation **only** for self-contained tasks.
- Recommend running `/smartspec_validate_index` or `/smartspec_reindex_specs` for multi-spec or shared-domain work.

---

## Troubleshooting

### Orchestrator does not appear even with `--kilocode`

Expected behavior after the update:

- You should see a warning indicating Orchestrator could not be activated.
- The workflow should fall back to Standard Mode and continue.

### “SPEC_INDEX.json not found”

Expected behavior in SmartSpec v5.2:

- Prefer canonical `.spec/SPEC_INDEX.json`.
- Fall back to root `SPEC_INDEX.json` (legacy mirror).
- Fall back to `.smartspec/SPEC_INDEX.json` (deprecated tooling index).
- If no index is found, continue with a warning **only** when your tasks are fully self-contained; otherwise the workflow should recommend running:
  - `/smartspec_validate_index` and/or `/smartspec_reindex_specs`.

This ensures implementation does not invent shared API/model/term names that already exist in the registry or other specs.

---

## Summary

Use `/smartspec_implement_tasks` to implement a well-defined subset of tasks safely and efficiently.

In v5.2, the workflow should consult the canonical index and optional registries to avoid cross-SPEC conflicts, respect UI JSON ownership when applicable, and always provide an evidence-based final summary.

`--kilocode` enables Orchestrator attempts, and the system must gracefully fall back when Orchestrator is unavailable.

