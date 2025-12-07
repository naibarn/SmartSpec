---
description: Generate a multi-SPEC implementation plan with SmartSpec centralization (.spec) and UI JSON addendum
version: 5.2
---

# /smartspec_generate_plan

Generate a high-level, dependency-aware plan for implementing one or more SmartSpec specs.

This workflow enforces SmartSpec v5.2 centralization:
- **`.spec/` is the canonical project-owned space** for shared truth.
- **`.spec/SPEC_INDEX.json` is the canonical index** when available.
- **`.spec/registry/` is the shared source of truth** for APIs, models, terms, and patterns.
- `.smartspec/` is tooling-only.
- **UI specs use `ui.json` as design source of truth** for Penpot integration.

---

## What It Does

- Resolves canonical `SPEC_INDEX.json`.
- Loads shared registries.
- Accepts a target spec or a group of specs.
- Builds a dependency-first plan covering:
  - architecture milestones
  - implementation phases
  - testing and validation
  - cross-SPEC shared work
  - UI design-to-component-to-logic alignment (when applicable)
- Prevents the plan from introducing new cross-SPEC naming drift.

---

## When to Use

- At the start of a new feature initiative.
- When onboarding a team to a large spec portfolio.
- Before generating detailed tasks.
- After reindexing or major refactors.

---

## Inputs

- Target spec path (recommended).
  - Example: `specs/core/spec-core-004-rate-limiting/spec.md`

- Or a spec ID list (when index is available).

---

## Outputs

- A plan document:
  - `plan.md` next to the target `spec.md`, or
  - a consolidated plan for multi-spec scope.

- Plan recommendations for registry alignment.

---

## Flags

- `--index` Path to SPEC_INDEX (optional)  
  default: auto-detect

- `--registry-dir` Registry directory (optional)  
  default: `.spec/registry`

- `--spec` Explicit spec path (optional)

- `--spec-ids` Comma-separated spec IDs (optional)

- `--output` Output plan path (optional)

- `--strict` Fail on ambiguity (optional)

- `--dry-run` Print plan only (do not write file)

---

## 0) Resolve Canonical Index & Registry

### 0.1 Resolve SPEC_INDEX (Single Source of Truth)

Detection order:

1) `.spec/SPEC_INDEX.json` (canonical)  
2) `SPEC_INDEX.json` (legacy root mirror)  
3) `.smartspec/SPEC_INDEX.json` (deprecated)  
4) `specs/SPEC_INDEX.json` (older layout)

```bash
INDEX_PATH="${FLAGS_index:-}"

if [ -z "$INDEX_PATH" ]; then
  if [ -f ".spec/SPEC_INDEX.json" ]; then
    INDEX_PATH=".spec/SPEC_INDEX.json"
  elif [ -f "SPEC_INDEX.json" ]; then
    INDEX_PATH="SPEC_INDEX.json"
  elif [ -f ".smartspec/SPEC_INDEX.json" ]; then
    INDEX_PATH=".smartspec/SPEC_INDEX.json" # deprecated
  elif [ -f "specs/SPEC_INDEX.json" ]; then
    INDEX_PATH="specs/SPEC_INDEX.json"
  fi
fi

if [ -n "$INDEX_PATH" ] && [ -f "$INDEX_PATH" ]; then
  echo "✅ Using SPEC_INDEX: $INDEX_PATH"
else
  echo "⚠️ SPEC_INDEX not found. Planning will proceed in local-spec-only mode."
  INDEX_PATH=""
fi
```

### 0.2 Resolve Registry Directory

```bash
REGISTRY_DIR="${FLAGS_registry_dir:-.spec/registry}"

if [ ! -d "$REGISTRY_DIR" ]; then
  echo "⚠️ Registry directory not found at $REGISTRY_DIR"
  echo "   Planning will rely on spec-local definitions and avoid introducing new shared names."
fi
```

### 0.3 Expected Registries (if present)

- `api-registry.json`
- `data-model-registry.json`
- `glossary.json`
- `critical-sections-registry.json`
- `patterns-registry.json` (optional)
- `ui-component-registry.json` (optional)

Rules:
- Use registry names as canonical references in the plan.
- If the plan requires unregistered shared names:
  - flag a recommendation to run `/smartspec_sync_spec_tasks --mode=additive` after review.

---

## 1) Identify Planning Scope

Priority:

1) `--spec` if provided.
2) If `--spec-ids` provided and `INDEX_PATH` exists, resolve them.
3) If `INDEX_PATH` exists, allow selecting a group of specs by category or dependency chain.
4) Otherwise, prompt for a spec path.

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
  - UI markers (category=ui or `ui.json` presence)

Do not rewrite specs in this workflow.

---

## 3) Build Dependency Graph for Planning

If `INDEX_PATH` exists:
- Use index dependency graph as the primary source.
- Confirm local spec dependencies do not contradict index.

If `INDEX_PATH` does not exist:
- Infer a minimal dependency order from:
  - explicit spec text
  - folder structure
  - known core/security precedence patterns

---

## 4) Centralization Consistency Gate

Before writing a plan:

- Confirm that shared names referenced by multiple specs appear in registries when available.
- If the plan detects naming drift across specs:
  - add a **blocking plan item** for reconciliation.

In `--strict` mode:
- Stop when drift is unresolved.

---

## 5) Plan Structure

Generate a plan with phases aligned to dependencies.

### 5.1 Phase 0: Foundations

- Confirm canonical index location.
- Confirm registry presence.
- Run `/smartspec_validate_index` if applicable.

### 5.2 Phase 1: Shared Contracts & Patterns

- Identify reusable patterns across target specs.
- Plan extraction of shared interfaces where required.

### 5.3 Phase 2: Core Domain & Data

- Implement or refine shared models.
- Ensure model names align to registry.

### 5.4 Phase 3: Service/Use Case Layer

- Implement business logic in stable layers.
- Define integration boundaries.

### 5.5 Phase 4: API & Integration

- Implement endpoints aligned with `api-registry.json`.
- Add contract tests.

### 5.6 Phase 5: Observability & Security

- Integrate logging/metrics/tracing.
- Apply auth/authz and rate-limiting/ auditing specs if present.

### 5.7 Phase 6: UI (Conditional)

Only include this phase when UI addendum applies.

---

## 6) UI JSON Addendum (Conditional)

Apply when **any** of these are true:
- A target spec category is `ui` in the index.
- A target spec folder contains `ui.json`.
- The spec explicitly mentions Penpot/UI JSON workflow.

Planning rules:

1) **Design-first sequencing**
   - Ensure a plan step exists for UI team to produce or update `ui.json`.

2) **Component mapping gate**
   - Plan a step to map UI nodes/frames to components.
   - If `ui-component-registry.json` exists, require name alignment.

3) **Logic separation**
   - Explicitly plan to implement business logic outside UI JSON.
   - UI layer should orchestrate rendering and state only.

4) **Non-UI projects**
   - If no UI JSON is used in this project, do not fail.
   - Keep UI planning within `spec.md` and recommend future adoption if helpful.

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
- next to the primary target spec:
  - `plan.md`

If `--output` provided:
- write to that path.

If `--dry-run`:
- print only.

---

## 9) Plan Quality Gates

A valid plan must include:

- Clear dependency ordering.
- Explicit cross-SPEC shared work when detected.
- Registry alignment notes.
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

- This workflow is conservative to avoid introducing new cross-SPEC conflicts in planning.
- `.spec/registry/` remains the canonical shared truth when present.
- Root `SPEC_INDEX.json` is treated as a legacy mirror.

