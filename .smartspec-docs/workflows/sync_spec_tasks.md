---
description: SmartSpec Sync Spec-Tasks Manual (v5.6)
version: 5.6
last_updated: 2025-12-08
---

# `/smartspec_sync_spec_tasks`

Synchronize an existing `tasks.md` with its source `spec.md` and optionally propagate **safe, additive signals** into the canonical index and registries.

This v5.6 manual preserves the original v5.2 intent and readability:

- Keep `spec.md` and `tasks.md` aligned without destroying legacy clarity.
- Preserve completed tasks whenever possible.
- Prevent drift and duplicate implementations.

And adds v5.6 alignment features:

- Multi-repo resolution
- Multi-registry validation with clear precedence
- Safety-mode consistent with the v5.6 chain
- UI mode awareness where `ui.json` workflows exist

---

## v5.6 Alignment Notes

SmartSpec v5.6 continues the separation between project-owned truth and tooling:

- **Project-owned canonical space:** `.spec/`
- **Canonical index:** `.spec/SPEC_INDEX.json`
- **Shared registries:** `.spec/registry/`
- **Legacy root mirror:** `SPEC_INDEX.json` (optional)
- **Deprecated tooling index:** `.smartspec/` should not be used as a source of truth

### Canonical Index Auto-Detect Order

1) `.spec/SPEC_INDEX.json`  
2) `SPEC_INDEX.json`  
3) `.smartspec/SPEC_INDEX.json` (deprecated)  
4) `specs/SPEC_INDEX.json`

### Multi-Repo & Multi-Registry (NEW)

To keep the chain consistent across two or more repositories, v5.6 introduces a common flag set shared with:

- `/smartspec_validate_index`
- `/smartspec_generate_spec`
- `/smartspec_generate_plan`
- `/smartspec_generate_tasks`

---

## 1. Summary

`/smartspec_sync_spec_tasks` is a **maintenance** workflow that:

1) Reads `spec.md` and `tasks.md` (read-only inputs).
2) Updates `tasks.md` to reflect spec changes while preserving progress.
3) Detects cross-SPEC and cross-repo conflicts that could cause implementation duplication.
4) Optionally syncs safe, additive metadata signals into:
   - `.spec/SPEC_INDEX.json`
   - `.spec/registry/*`
5) Produces a structured report for review.

This workflow must never remove essential legacy explanations from `tasks.md`.

---

## 2. Usage

```bash
/smartspec_sync_spec_tasks <tasks_path> [options...]
```

Common alternatives (implementation-dependent):

```bash
/smartspec_sync_spec_tasks --spec <spec_path>
/smartspec_sync_spec_tasks --tasks <tasks_path>
```

---

## 3. Inputs & Outputs

### Inputs

- `spec.md`
- `tasks.md`
- (UI specs) optional `ui.json`
- Optional index + registries

### Outputs

- Updated `tasks.md` (unless `--dry-run`)
- Optional canonical index updates: `.spec/SPEC_INDEX.json`
- Optional legacy mirror updates: `SPEC_INDEX.json`
- Registry recommendations or additive updates (mode-dependent)
- Report: `.spec/reports/sync-spec-tasks/`

---

## 4. Modes

```bash
--mode=<sync-only|additive|index-only>
```

- **sync-only** (default)
  - Update `tasks.md` to reflect `spec.md`.
  - Do not write index/registry changes.

- **additive**
  - Sync tasks and allow **append-only** metadata updates to index/registries.
  - Must never delete or rename existing shared entries.
  - **Multi-registry safeguard:** if a conflicting entry exists in any loaded registry view, downgrade to recommendation-only.

- **index-only**
  - Skip tasks rewrite.
  - Sync safe signals to the canonical index only.

---

## 5. Key Flags

### 5.1 Index & Registry

```bash
--index=<path>
--specindex=<path>          # legacy alias
--registry-dir=<dir>        # primary authoritative registry
--registry-roots=<csv>      # supplemental registries (read-only)
```

Registry precedence:

1) `--registry-dir` is authoritative.
2) `--registry-roots` are validation sources to prevent cross-repo duplication.

### 5.2 Multi-Repo

```bash
--workspace-roots=<csv>
--repos-config=<path>
```

- `--repos-config` takes precedence over `--workspace-roots`.
- Recommended location: `.spec/smartspec.repos.json`.

### 5.3 Safety

```bash
--safety-mode=<strict|dev>
--strict                    # legacy alias
```

- `strict` (default)
  - Stop when ambiguity would cause duplicate shared entities across repos.

- `dev`
  - Proceed but add high-visibility warnings to the report and tasks.

### 5.4 Preview

```bash
--dry-run
```

---

## 6. How Sync Works (High-Level)

1) Resolve canonical index path.
2) Load primary registry and optional supplemental registries.
3) Build multi-repo search roots when configured.
4) Read target `spec.md` and `tasks.md`.
5) Compare scope, requirements, dependencies, APIs, models, terms, and UI markers.
6) Reconcile tasks:
   - add missing tasks for new requirements
   - preserve completed tasks when still valid
   - deprecate tasks only when the spec explicitly removes the requirement
7) If `--mode=additive`, propose append-only index/registry updates with safeguards.
8) Write output and report.

---

## 7. UI Design Addendum

UI alignment applies when any of these are true:

- Index category is `ui`
- `ui.json` exists in the spec folder
- Spec text declares JSON-driven UI workflows

Rules:

- `ui.json` is the design source of truth in JSON mode.
- The sync should ensure tasks include:
  - UI JSON validation/update steps
  - component mapping steps
  - logic separation tasks
- If `ui-component-registry.json` exists, validate naming alignment.

---

## 8. Best Practices

### Single Repo

```bash
/smartspec_sync_spec_tasks specs/.../tasks.md
```

### Two or More Repos

```bash
/smartspec_sync_spec_tasks specs/.../tasks.md \
  --repos-config=.spec/smartspec.repos.json \
  --registry-dir=.spec/registry \
  --registry-roots="../Repo-A/.spec/registry,../Repo-B/.spec/registry"
```

---

## 9. Recommended Follow-Up Workflows

- `/smartspec_validate_index`
- `/smartspec_generate_plan`
- `/smartspec_generate_tests`
- `/smartspec_verify_tasks_progress`
- `/smartspec_reindex_specs`

---

## 10. For the LLM

When implementing using a synced `tasks.md`:

- Read all referenced specs and registries first.
- Treat cross-repo owners as **reuse-only** unless the tasks explicitly justify `create`.
- Do not introduce new shared names that conflict with any loaded registry view.
- Respect UI mode resolution.
- If tasks and spec contradict, stop and request reconciliation.

---

## 11. Summary

`/smartspec_sync_spec_tasks v5.6` is a conservative alignment tool. It keeps execution plans consistent with evolving specs while protecting large multi-repo programs from duplicated implementations and shared-name drift.

