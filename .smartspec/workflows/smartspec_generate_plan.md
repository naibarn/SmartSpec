---
description: Generate a multi-SPEC implementation plan with SmartSpec v5.6 centralization, UI mode alignment, and multi-repo/multi-registry safety
version: 5.6
---

# /smartspec_generate_plan

Generate a high-level, dependency-aware plan for implementing one or more SmartSpec specifications.

This workflow **preserves all v5.2 planning behavior** and extends it to align with the v5.6 chain across **spec → tasks → sync** in multi-repo environments.

Recommended chain for large programs:

1) `/smartspec_validate_index`  
2) `/smartspec_generate_spec`  
3) `/smartspec_generate_plan`  
4) `/smartspec_generate_tasks`  
5) `/smartspec_sync_spec_tasks`

---

## Core Assumptions (Unchanged)

- **`.spec/` is the canonical project-owned space** for shared truth.
- **`.spec/SPEC_INDEX.json` is the canonical index** when available.
- **`.spec/registry/` is the shared source of truth** for APIs, models, terms, and patterns.
- `.smartspec/` is tooling-only.
- Root `SPEC_INDEX.json` may exist as a legacy mirror.

---

## New v5.6 Alignment Goals

This plan workflow must:

1) Produce plans that are **task-ready** (i.e., can safely drive `/smartspec_generate_tasks`).
2) Prevent cross-SPEC and cross-repo drift, especially around shared names.
3) Respect UI mode resolution so UI sequencing matches both SPEC and TASKS rules.
4) Remain conservative when registry/index context is incomplete.

---

## What It Does

- Resolves canonical index and registries.
- Builds an optional multi-repo/multi-registry context.
- Accepts a target spec or group of specs.
- Builds a dependency-first plan covering:
  - architecture milestones
  - implementation phases
  - testing and validation
  - cross-SPEC shared work
  - UI design-to-component-to-logic alignment (when applicable)
- Prevents the plan from introducing new cross-SPEC naming drift.
- Emits reconciliation steps when governance alignment is missing.

---

## When to Use

- At the start of a new feature initiative.
- When onboarding a team to a large spec portfolio.
- Before generating detailed tasks.
- After reindexing or major refactors.
- When specs or registries are distributed across **two or more repos**.

---

## Inputs

- Target spec path (recommended).
  - Example: `specs/core/spec-core-004-rate-limiting/spec.md`

- Or a spec ID list (when index is available).

- Optional context files already present in the spec folder:
  - `tasks.md`
  - (UI specs) `ui.json`

---

## Outputs

- A plan document:
  - `plan.md` next to the target `spec.md`, or
  - a consolidated plan for multi-spec scope.

- Plan recommendations for registry alignment.

- Plan report under:
  - `.spec/reports/generate-plan/`

---

## Flags

### Index / Registry

- `--index` Path to SPEC_INDEX (optional)  
  default: auto-detect

- `--specindex` Legacy alias for `--index` (optional)

- `--registry-dir` Primary registry directory (optional)  
  default: `.spec/registry`

- `--registry-roots` Comma-separated list of supplemental registry directories (optional)
  - Loaded **read-only** for cross-repo validation.

### Multi-Repo Resolution (NEW)

- `--workspace-roots` Comma-separated additional repo roots (optional)

- `--repos-config` JSON mapping of repo IDs to roots (optional)  
  - Takes precedence over `--workspace-roots`.
  - Recommended path: `.spec/smartspec.repos.json`

### Scope Selection

- `--spec` Explicit spec path (optional)

- `--spec-ids` Comma-separated spec IDs (optional)

### Output

- `--output` Output plan path (optional)

### Safety

- `--safety-mode=<strict|dev>` (NEW)
  - `strict` (default): fail when ambiguity would cause cross-repo duplication risk in the plan.
  - `dev`: continue with high-visibility warnings.

- `--strict` Legacy alias for strict gating (optional)

- `--dry-run` Print plan only (do not write file)

### UI Mode (Optional Alignment Control)

- `--ui-mode=<auto|json|inline>`
  - Default: `auto`
  - Aligns planning assumptions to the same UI rules used by SPEC and TASKS.

---

## 0) Resolve Canonical Index, Registries, and Multi-Repo Roots

### 0.1 Resolve SPEC_INDEX (Single Source of Truth)

Detection order:

1) `.spec/SPEC_INDEX.json` (canonical)  
2) `SPEC_INDEX.json` (legacy root mirror)  
3) `.smartspec/SPEC_INDEX.json` (deprecated)  
4) `specs/SPEC_INDEX.json` (older layout)

If no index exists:

- Planning proceeds in **local-spec-only** mode.
- The plan must include a Phase 0 step recommending:
  - `/smartspec_reindex_specs`
  - and `/smartspec_validate_index`

### 0.2 Resolve Primary Registry Directory

Default:

- `.spec/registry`

### 0.3 Resolve Supplemental Registry Roots (NEW)

- Load `--registry-roots` read-only when provided.

Registry precedence:

1) Primary registry (`--registry-dir`) is authoritative.
2) Supplemental registries (`--registry-roots`) are validation sources.

If the plan detects a shared name that is defined in any loaded registry view:

- The plan must treat that name as **reused**.
- The plan must not schedule creation of a duplicate shared entity.

### 0.4 Resolve Multi-Repo Search Roots (NEW)

- If `--repos-config` exists:
  - validate repo IDs referenced by target specs in the index.
- If only `--workspace-roots` exists:
  - scan for dependency specs using path resolution.

---

## 1) Identify Planning Scope

Priority:

1) `--spec` if provided.
2) If `--spec-ids` provided and index exists, resolve them.
3) If index exists, allow selecting groups by category and dependency chain.
4) Otherwise, require a spec path.

---

## 2) Read Spec(s) (Read-Only)

For each target spec:

- Read `spec.md`.
- Extract:
  - scope and objectives
  - functional requirements
  - non-functional requirements (SLA, performance, security)
  - dependencies
  - API/model/term hints
  - UI markers (category=ui, `ui.json`, or explicit UI JSON mentions)

Do not rewrite specs in this workflow.

---

## 3) Build Dependency Graph for Planning

If index exists:

- Use index dependency graph as the primary source.
- Confirm local spec dependencies do not contradict index.

If index does not exist:

- Infer a minimal dependency order from:
  - explicit spec text
  - folder structure
  - known core/security precedence patterns

Multi-repo rule:

- If a dependency spec resolves to another repo:
  - the plan must mark it as **external dependency**.
  - include a “reuse-not-rebuild” note.

---

## 4) Centralization Consistency Gate (Multi-Registry Aware)

Before writing a plan:

- Confirm that shared names referenced by multiple specs appear in registries when available.
- Detect naming drift across target specs and across supplemental registries.

If drift is detected:

- Add a **blocking plan item** for reconciliation.

In strict safety mode:

- Stop when drift would cause ambiguous ownership or duplicate shared work.

---

## 5) Plan Structure

Generate a plan with phases aligned to dependencies.

### 5.1 Phase 0: Foundations

- Confirm canonical index location.
- Confirm registry presence.
- Run `/smartspec_validate_index` if applicable.
- If multi-repo flags are used:
  - include a short “cross-repo governance readiness” checklist.

### 5.2 Phase 1: Shared Contracts & Patterns

- Identify reusable patterns across target specs.
- Plan extraction or adoption of shared interfaces where required.
- Ensure no planned shared name conflicts with any loaded registry.

### 5.3 Phase 2: Core Domain & Data

- Implement or refine shared models.
- Ensure model names align to registry.
- If a model is owned in another repo:
  - plan integration rather than re-creation.

### 5.4 Phase 3: Service/Use Case Layer

- Implement business logic in stable layers.
- Define integration boundaries.
- Call out cross-SPEC services that should be reused.

### 5.5 Phase 4: API & Integration

- Implement endpoints aligned with `api-registry.json`.
- Add contract tests.
- If an API is owned elsewhere:
  - plan client/adaptor work rather than server duplication.

### 5.6 Phase 5: Observability & Security

- Integrate logging/metrics/tracing.
- Apply auth/authz, rate limiting, auditing specs if present.

### 5.7 Phase 6: UI (Conditional)

Only include when UI addendum applies.

---

## 6) UI Addendum (v5.6)

Apply when any of these are true:

- A target spec category is `ui` in the index.
- A target spec folder contains `ui.json`.
- The spec explicitly mentions a design JSON workflow.

Planning rules:

1) **Design-first sequencing**
   - Ensure a plan step exists for UI team or system to produce/update `ui.json` when UI_MODE=json.

2) **Component mapping gate**
   - Plan a step to map UI nodes/frames to components.
   - If `ui-component-registry.json` exists, require name alignment.

3) **Logic separation**
   - Business logic must be planned outside UI JSON.
   - UI layer orchestrates rendering/state only.

4) **Inline UI mode support**
   - When UI_MODE=inline, keep UI requirements and UX guidance inside `spec.md`.
   - Still plan for modern, consistent UI/UX implementation.

---

## 7) Testing Strategy in the Plan

For each phase, outline test expectations:

- Unit tests for domain logic.
- Integration tests for service/data boundaries.
- Contract/API tests for external interfaces.
- Performance tests when SLAs exist.
- UI/component tests when UI addendum applies.

---

## 8) Output Rules

Default output path:

- Next to the primary target spec:
  - `plan.md`

If `--output` provided:

- Write to that path.

If `--dry-run`:

- Print only.

---

## 9) Plan Quality Gates (v5.6)

A valid plan must include:

- Clear dependency ordering.
- Explicit cross-SPEC shared work when detected.
- Registry alignment notes.
- Cross-repo reuse notes when dependencies resolve to other repos.
- UI separation steps when applicable.
- Recommended follow-up workflows.

---

## 10) Recommended Follow-ups

- `/smartspec_generate_tasks`
- `/smartspec_generate_tests`
- `/smartspec_implement_tasks`
- `/smartspec_verify_tasks_progress`
- `/smartspec_sync_spec_tasks --mode=additive` (after review)

---

## Notes

- This workflow is conservative to avoid introducing new cross-SPEC or cross-repo conflicts in planning.
- Multi-repo and multi-registry flags are optional for single-repo projects but strongly recommended for shared-platform architectures.
- The plan should never schedule creation of a shared entity that is already defined in any loaded registry view.
- Root `SPEC_INDEX.json` remains a legacy mirror; `.spec/SPEC_INDEX.json` is canonical when present.

