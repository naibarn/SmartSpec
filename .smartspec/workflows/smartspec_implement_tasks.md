---
description: Implement tasks with SmartSpec v5.6 centralization, multi-repo + multi-registry alignment, KiloCode Orchestrator support, safety-mode, and UI JSON addendum
version: 5.6
last_updated: 2025-12-08
---

# /smartspec_implement_tasks

Implement code changes based on `tasks.md` and `spec.md` while enforcing SmartSpec centralization and preventing cross-SPEC drift.

This v5.6 workflow preserves the full v5.2 intent and user-facing capabilities, including KiloCode support via `--kilocode`, and extends the command to align with the v5.6 chain for multi-repo and multi-registry programs.

SmartSpec centralization remains unchanged:

- **`.spec/` is the canonical project-owned space** for shared truth.
- **`.spec/SPEC_INDEX.json` is the canonical index**.
- **`.spec/registry/` is the shared naming source of truth**.
- `SPEC_INDEX.json` at repo root is a **legacy mirror**.
- `.smartspec/` is tooling-only.
- **UI specs may use `ui.json` as design source of truth** for Penpot integration.

---

## What It Does

- Resolves canonical `SPEC_INDEX.json`.
- Loads shared registries (primary + supplemental when configured).
- Builds multi-repo search context when configured.
- Reads target `spec.md`, `tasks.md`, and relevant dependency specs.
- Validates naming consistency before coding.
- Implements tasks in a dependency-safe order.
- Generates or updates tests aligned with spec + registries.
- Applies UI JSON addendum rules conditionally.
- Produces a required final summary per run.

---

## When to Use

- After `tasks.md` has been generated and reviewed.
- During active implementation of a SPEC.
- When working in large multi-SPEC and/or multi-repo projects to avoid conflicts.
- When you want KiloCode Orchestrator-driven subtask execution.

---

## Inputs

- Target tasks path (recommended)
  - Example: `specs/core/spec-core-004-rate-limiting/tasks.md`

- Expected adjacent files:
  - `spec.md`
  - (UI specs) `ui.json`

- Optional governance context:
  - `.spec/SPEC_INDEX.json`
  - `.spec/registry/*.json`
  - supplemental registries from sibling repos

---

## Outputs

- Code changes in the repository
- Updated or newly created tests
- Optional implementation notes
- Non-destructive registry/addendum recommendations

---

## Flags

### Index / Registry (v5.6-aligned)

- `--index` Path to SPEC_INDEX (optional)  
  default: auto-detect

- `--specindex` Legacy alias for `--index`

- `--registry-dir` Primary registry directory (optional)  
  default: `.spec/registry`

- `--registry-roots` Supplemental registry dirs, comma-separated (optional)
  - **Read-only validation sources** used to prevent cross-repo duplicate naming.

Registry precedence:

1) Primary registry (`--registry-dir`) is authoritative.
2) Supplemental registries (`--registry-roots`) are validation sources.

### Multi-Repo (v5.6-aligned)

- `--workspace-roots` Comma-separated repo roots to search (optional)

- `--repos-config` Structured repo config path (optional)
  - takes precedence over `--workspace-roots`
  - recommended: `.spec/smartspec.repos.json`

### Target Selection & Scope

- `--spec` Explicit spec path (optional)
- `--tasks` Explicit tasks path (optional)

#### Task scope selection (backward compatible)

This workflow supports precise implementation scope.

- `--task=<n>` Implement a single task by index number
- `--tasks=<csv>` Implement multiple tasks
- `--range=<a-b>` Implement a task range
- `--from=<n>` Start from a task index
- `--start-from=<Tnnn>` Legacy task-ID form
  - Alias for `--from` when tasks are numbered by ID (e.g., `T033`)

#### Completion mode flags

- `--skip-completed` Skip checked tasks (**default**)
- `--force-all` Ignore checkboxes and re-implement all tasks

#### Resume / Checkpoint

- `--resume` Resume using the last safe checkpoint (if supported)

### Phase Filtering (if your tasks use phases) (if your tasks use phases)

- `--phase=<n>`
- `--phases=<csv>`
- `--phase-range=<a-b>`

### Focus

- `--focus=<api|model|ui|tests|migration|observability|security>`

### Safety / Preview

- `--safety-mode=<strict|dev>` (optional)
  default: `strict`

- `--strict` Legacy alias for strict gating

- `--validate-only` Validate readiness without writing code

- `--architect`
  - Use Architect Mode for system design before implementation.
  - When used with `--kilocode`, Orchestrator may still decide to call Architect first.

### KiloCode Integration (RESTORED + REQUIRED BACKWARD COMPATIBILITY) (RESTORED + REQUIRED BACKWARD COMPATIBILITY)

- `--kilocode`
  - Enable KiloCode-optimized execution.
  - The workflow attempts to activate **KiloCode Orchestrator** when available.
  - If Orchestrator cannot be activated, the workflow must fall back to Standard Mode with a warning.

#### Orchestrator Subtasks Rule

When `--kilocode` is enabled and Orchestrator is available:

- The execution should follow a **per-task loop**:
  1) Switch to **Orchestrator** for each top-level SmartSpec task.
  2) Request subtask breakdown using the SmartSpec numbering convention.
     - Example: `T0001 → T0001.1, T0001.2, ...`
  3) Confirm registry + ownership boundaries.
  4) Switch to **Code** for implementation.
  5) Return to Orchestrator for the next top-level task.

- Subtask decomposition is expected to be ON by default in KiloCode contexts.

---

## 0) Resolve Canonical Index & Registry

### 0.1 Resolve SPEC_INDEX (Single Source of Truth)

Detection order:

1) `.spec/SPEC_INDEX.json` (canonical)  
2) `SPEC_INDEX.json` (legacy root mirror)  
3) `.smartspec/SPEC_INDEX.json` (deprecated)  
4) `specs/SPEC_INDEX.json` (older layout)

### 0.2 Resolve Registry Directory

- Default primary registry: `.spec/registry`
- Load `--registry-roots` (if provided) read-only.

---

## 1) Identify Target Spec/Tasks

Priority:

1) Use `--tasks` / `--spec` if provided.
2) Otherwise infer `spec.md` adjacent to `tasks.md`.
3) If index exists, allow selecting by spec ID (implementation-dependent).

---

## 2) Read Spec + Tasks (Read-Only Inputs)

- Read `spec.md`.
- Read `tasks.md`.
- Detect `ui.json` when applicable.

The workflow may update task checkboxes only under the checkbox rules below.

---

## 3) Pre-Implementation Consistency Gate

Before coding, verify:

1) **Dependency alignment** between spec/tasks and index.
2) **Namespace & naming alignment** with the merged registry view.
3) **Pattern reuse** when a patterns registry exists.
4) **Cross-repo owner boundaries** when dependencies resolve outside the current repo.

In `--safety-mode=strict`:

- Stop when a new shared-name creation would likely conflict with any loaded registry view.

---

## 4) Implementation Strategy

Implement tasks in a dependency-safe order:

1) Shared interfaces/contracts (only when explicitly required and registry-aligned)
2) Domain models
3) Service/use case layer
4) API/controllers
5) Observability
6) Security
7) UI components (if applicable)

---

## 5) UI JSON Addendum (Conditional)

Apply when any of these are true:

- Spec category is `ui` in SPEC_INDEX.
- `ui.json` exists in the spec folder.
- The spec explicitly mentions Penpot/UI JSON flow.

Rules:

- `ui.json` is design-owned.
- Treat `ui.json` as read-only unless tasks explicitly require an engineering-owned change.
- No business logic in UI JSON.

Required checks:

- Component mapping
- Logic separation
- Design handoff integrity

---

## 6) Testing Expectations

Generate/update tests aligned with tasks and registries:

- Unit tests for domain logic
- Integration tests for service + data access
- Contract tests for APIs
- Performance tests when SLAs exist

---

## 7) Checkbox Update Rules

Check a task only if:

- Required code changes are complete.
- Acceptance criteria are satisfied.
- Required tests (if listed) are created or updated.

For partial completion:

- Add implementation notes without checking the box.

---

## 8) Post-Implementation Validation

Before marking tasks complete:

- Verify the final names used match registries.
- Record any unavoidable new shared definitions for later additive governance review.

Recommended follow-up:

- `/smartspec_verify_tasks_progress`
- `/smartspec_sync_spec_tasks --mode=additive`

---

## 9) Required Final Summary

Each run must end with a concise summary including:

- Tasks attempted/completed
- Files changed/created
- Registry alignment status
- UI JSON compliance notes (if applicable)
- Open risks/blockers
- Suggested next command

---

## Notes

- `--kilocode` is a long-standing user-facing capability and must remain supported for backward compatibility.
- Multi-repo and multi-registry flags bring this execution workflow into full alignment with the v5.6 governance chain.
- The workflow is conservative by design to prevent cross-SPEC and cross-repo duplication.

