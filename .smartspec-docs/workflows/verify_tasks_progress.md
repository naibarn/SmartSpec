---
description: SmartSpec Verify Tasks Progress Guide (v5.2)
version: 5.2
last_updated: 2025-12-08
---

# `/smartspec_verify_tasks_progress`

**Analyze real implementation progress against a spec and its tasks, highlight gaps, and prevent cross-SPEC drift.**

This manual preserves the legacy intent of the workflow and adds clarifications for **SmartSpec v5.2 centralization**, optional **UI JSON addendum**, and the clarified delivery loop.

---

## v5.2 Alignment Notes

SmartSpec v5.2 separates tooling from project-owned truth.

- **Project-owned canonical space:** `.spec/`
- **Canonical index (preferred):** `.spec/SPEC_INDEX.json`
- **Shared registries (optional):** `.spec/registry/`
- **Legacy mirror (optional):** `SPEC_INDEX.json` at repo root
- **Deprecated tooling index:** `.smartspec/SPEC_INDEX.json`

Unless you override with `--index`, this workflow should resolve SPEC_INDEX in this order:

1) `.spec/SPEC_INDEX.json` (canonical)  
2) `SPEC_INDEX.json` (root legacy mirror)  
3) `.smartspec/SPEC_INDEX.json` (deprecated fallback)  
4) `specs/SPEC_INDEX.json` (older layout)

Reports should be written under the project-owned reporting area:

- **Default:** `.spec/reports/verify-tasks-progress/`

### Multi-Repo note

Most teams use multi-repo resolution primarily for **validate** and **reindex**. This verification workflow typically operates within the current repo unless your local implementation extends it.

---

## 1. Summary

`/smartspec_verify_tasks_progress` is a read-mostly verification workflow. It compares:

- the intended outcomes from `spec.md`
- the executable breakdown in `tasks.md`
- the real codebase changes

and produces a structured report showing what is complete, incomplete, missing, or potentially drifting from shared rules.

**Primary benefits:**

- Keeps implementation aligned with the spec
- Detects missing acceptance criteria early
- Prevents duplicate or conflicting implementations across specs
- Provides a clean checkpoint before generating tests or merging large PRs

---

## 2. Usage

```bash
/smartspec_verify_tasks_progress <spec_or_tasks_path> [options...]
```

Where `<spec_or_tasks_path>` can be:

- a direct `spec.md` path (recommended)
- a direct `tasks.md` path
- a spec folder (if your implementation supports folder inference)

---

## 3. Parameters & Options

### Primary Argument

| Name | Type | Required? | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `spec_or_tasks_path` | `string` | ✅ Yes | Path to `spec.md`, `tasks.md`, or spec folder | `specs/core/spec-core-004-rate-limiting/spec.md` |

### Scope Options

| Option | Type | Default | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `--phase` | `number` | All | Verify tasks only for a specific phase | `--phase 1` |
| `--phases` | `string` | All | Verify multiple phases | `--phases 1,2` |
| `--range` | `string` | All | Verify a range of task numbers | `--range 5-12` |
| `--only-open` | `flag` | `false` | Focus on unchecked tasks | `--only-open` |

### Reporting Options

| Option | Type | Default | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `--report` | `string` | `summary` | `summary` or `detailed` | `--report detailed` |
| `--report-dir` | `string` | `.spec/reports/verify-tasks-progress/` | Custom report directory | `--report-dir .spec/reports/verify/` |
| `--output` | `string` | auto | Custom output file path | `--output progress-rate.md` |
| `--dry-run` | `flag` | `false` | Print findings without writing files | `--dry-run` |

### Index / Registry Options (v5.2 compatible)

| Option | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `--index` | `string` | auto-detect | Override SPEC_INDEX path |
| `--specindex` | `string` | alias | Legacy-compatible alias for `--index` |
| `--registry-dir` | `string` | `.spec/registry` | Override registry directory |

### Strictness

| Option | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `--strict` | `flag` | `false` | Treat high-risk drift signals as errors |

---

## 4. Output Placement Rules

By default, the workflow writes reports to:

```text
.spec/reports/verify-tasks-progress/
```

This keeps verification artifacts in the project-owned space and avoids cluttering tooling folders.

---

## 5. Examples

### 5.1 Verify a Spec

```bash
/smartspec_verify_tasks_progress specs/core/spec-core-004-rate-limiting/spec.md
```

### 5.2 Verify Using Tasks Path

```bash
/smartspec_verify_tasks_progress specs/core/spec-core-004-rate-limiting/tasks.md
```

### 5.3 Verify Only Phase 1

```bash
/smartspec_verify_tasks_progress specs/core/spec-core-004-rate-limiting/spec.md --phase 1
```

### 5.4 Focus on Open Tasks

```bash
/smartspec_verify_tasks_progress specs/core/spec-core-004-rate-limiting/spec.md --only-open --report detailed
```

### 5.5 Dry Run

```bash
/smartspec_verify_tasks_progress specs/core/spec-core-004-rate-limiting/spec.md --dry-run
```

---

## 6. How It Works (Conceptual)

1) **Resolve the spec context**
   - If you pass `tasks.md`, infer the adjacent `spec.md`.
   - If you pass `spec.md`, infer the adjacent `tasks.md`.

2) **Load the canonical index** (when present)
   - Use v5.2 canonical-first resolution.

3) **Load shared registries** (if present)
   - APIs
   - data models
   - glossary
   - critical sections
   - patterns (optional)
   - UI components (optional)

4) **Map tasks to real files**
   - Prefer file lists declared in the index entry for the spec.

5) **Check evidence in code**
   - Look for implementation markers described in tasks.
   - Confirm acceptance criteria signals where feasible.

6) **Compute completion confidence**
   - Mark tasks as:
     - implemented
     - partially implemented
     - not implemented
     - blocked

7) **Generate a summary and recommendations**

This workflow should not invent shared names or systems.

---

## 7. Drift and Conflict Signals

The workflow flags risks such as:

- tasks implemented with names that contradict registries
- new APIs/models added without registry alignment (if your policy requires it)
- implementations that appear duplicated across sibling specs
- UI components implemented without matching UI design references (when UI JSON is used)

In large programs, treat these as early warning signals.

---

## 8. UI Design Addendum (Conditional)

If the target spec is a UI spec and your project adopts Penpot JSON-first UI:

- `ui.json` should exist for active UI specs.
- The verification report should confirm:
  - component naming alignment with `ui-component-registry.json` (if present)
  - separation of UI structure vs business logic
  - whether tasks are correctly mapped to components

This workflow should not rewrite `ui.json`.

Projects without UI JSON are not affected.

---

## 9. Best Practices

### Recommended delivery loop

```bash
# Implement a safe slice
/smartspec_implement_tasks specs/core/spec-core-004-rate-limiting/tasks.md --range=1-6 --skip-completed

# Verify progress
/smartspec_verify_tasks_progress specs/core/spec-core-004-rate-limiting/spec.md --report detailed

# Fix mechanical errors if needed
/smartspec_fix_errors specs/core/spec-core-004-rate-limiting/

# Generate or extend tests
/smartspec_generate_tests specs/core/spec-core-004-rate-limiting/ --target 80

# Sync safe metadata back to index
/smartspec_sync_spec_tasks --spec=specs/core/spec-core-004-rate-limiting/spec.md
```

### Use strict mode strategically

- Use `--strict` for:
  - core specs
  - pre-release checks
  - cross-cutting concerns

---

## 10. Troubleshooting

| Issue | Likely Cause | Fix |
| :--- | :--- | :--- |
| **Tasks not found** | `tasks.md` missing or renamed | Create tasks using `/smartspec_generate_tasks` or correct the path. |
| **Spec not found** | Path incorrect | Provide the full path to `spec.md`. |
| **Verification misses files** | Index entry file list is outdated | Run `/smartspec_reindex_specs` and then re-verify. |
| **UI warnings in non-UI project** | Incorrect category marking | Adjust the spec category in the index. |

---

## 11. Related Workflows

- `/smartspec_generate_tasks`
- `/smartspec_implement_tasks`
- `/smartspec_fix_errors`
- `/smartspec_generate_tests`
- `/smartspec_sync_spec_tasks`
- `/smartspec_validate_index`

---

## 12. Summary

`/smartspec_verify_tasks_progress` is your execution checkpoint. It confirms whether real code reflects the plan in `tasks.md` and the intent of `spec.md`, while consulting canonical indexes and optional registries to prevent cross-SPEC contradictions.

In SmartSpec v5.2, it aligns with `.spec/` centralization and the optional UI JSON design flow, helping teams keep delivery fast without losing architectural coherence.

