---
description: Implement tasks with SmartSpec centralization (.spec) and UI JSON addendum
version: 5.2
---

# /smartspec_implement_tasks

Implement code changes based on `tasks.md` and `spec.md` while enforcing SmartSpec centralization and preventing cross-SPEC drift.

This workflow assumes:
- **`.spec/` is the canonical project space** for shared truth.
- `.smartspec/` is tooling-only.
- Shared names must be aligned via **`.spec/registry/`**.
- **UI specs use `ui.json` as design source of truth** for Penpot integration.

---

## What It Does

- Resolves canonical `SPEC_INDEX.json`.
- Loads shared registries.
- Reads target `spec.md` and `tasks.md`.
- Validates naming consistency before coding.
- Implements tasks in a dependency-safe order.
- Generates or updates tests aligned with spec + registries.
- Applies UI JSON addendum rules conditionally.

---

## When to Use

- After `tasks.md` has been generated and reviewed.
- During active implementation of a SPEC.
- When working in large multi-SPEC projects to avoid conflicts.

---

## Inputs

- Target spec path (recommended)
  - Example: `specs/core/spec-core-004-rate-limiting/spec.md`

- Expected adjacent files:
  - `tasks.md`
  - (UI specs) `ui.json`

---

## Outputs

- Code changes in the repository
- Updated or newly created tests
- Implementation notes (optional)
- Registry/addendum recommendations (non-destructive)

---

## Flags

- `--index` Path to SPEC_INDEX (optional)  
  default: auto-detect

- `--registry-dir` Registry directory (optional)  
  default: `.spec/registry`

- `--spec` Explicit spec path (optional)

- `--tasks` Explicit tasks path (optional)

- `--focus` Optional focus scope (e.g., `api`, `model`, `ui`, `tests`)

- `--strict` Fail on warnings (optional)

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
  echo "⚠️ SPEC_INDEX not found. Proceeding with local-spec-only context."
  INDEX_PATH=""
fi
```

### 0.2 Resolve Registry Directory

```bash
REGISTRY_DIR="${FLAGS_registry_dir:-.spec/registry}"

if [ ! -d "$REGISTRY_DIR" ]; then
  echo "⚠️ Registry directory not found at $REGISTRY_DIR"
  echo "   Proceeding with best-effort extraction from existing specs."
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
- Use registry names as canonical.
- Do not invent new shared names if a registry entry already exists.
- If new items are unavoidable, record them as **implementation notes** for later additive sync.

---

## 1) Identify Target Spec/Tasks

Priority:
1) `--spec` / `--tasks` if provided.
2) If `INDEX_PATH` exists, allow selecting by spec ID.
3) Otherwise, prompt user to provide a spec path.

Default tasks location:
- `tasks.md` next to `spec.md`.

---

## 2) Read Spec + Tasks (Read-Only Inputs)

- Read `spec.md`.
- Read `tasks.md`.
- If UI spec, check for `ui.json` in the same folder.

Do not rewrite these files during implementation.

---

## 3) Pre-Implementation Consistency Gate

Before coding, verify:

### 3.1 Dependency Alignment

If `INDEX_PATH` exists:
- The spec dependency list in tasks must match the dependency graph.
- If mismatch:
  - create a blocking note
  - do not proceed to cross-SPEC API/model naming changes until resolved

### 3.2 Namespace & Naming Alignment

If registries exist:
- APIs referenced in tasks must match `api-registry.json`.
- Models must match `data-model-registry.json`.
- Terms must match `glossary.json`.

If conflicts exist:
- In `--strict` mode: stop.
- Otherwise: implement only local changes that do not widen the conflict and record recommendations.

### 3.3 Pattern Reuse

If `patterns-registry.json` exists:
- Prefer shared patterns over new ad-hoc solutions.

---

## 4) Implementation Strategy

Implement tasks in this order:

1) **Shared Interfaces / Contracts**
   - Only when explicitly required by tasks and aligned with registries.

2) **Domain Models**
   - Use canonical names from registry.

3) **Service / Use Case Layer**
   - Keep business logic here (not in UI JSON).

4) **API / Controllers**
   - Ensure route names match registry.

5) **Observability**
   - Logging, metrics, tracing per spec NFRs.

6) **Security**
   - Auth/authz hooks
   - Rate limits
   - Audit trails if required

7) **UI Components** (if applicable)

---

## 5) UI JSON Addendum (Conditional)

Apply when any of these are true:
- Spec category is `ui` in SPEC_INDEX.
- `ui.json` exists in the spec folder.
- The spec explicitly mentions Penpot/UI JSON flow.

Rules:
- `ui.json` is **design-owned**.
- Treat `ui.json` as read-only for developers unless there is a controlled additive update policy.
- UI JSON must remain:
  - component structure
  - layout
  - props metadata
  - design tokens references
- **No business logic** embedded in UI JSON.

Required implementation checks:

### 5.1 Component Mapping

- Map UI nodes/frames to existing components.
- If `ui-component-registry.json` exists:
  - component names must match registry.
  - if missing, record an additive recommendation.

### 5.2 Logic Separation

- Implement logic in appropriate layers (hooks/services/controllers).
- The UI layer should only orchestrate calls and render state.

### 5.3 Design Handoff Integrity

- Do not “fix design” by coding a different UI than described.
- If mismatch is found:
  - create a task/note for UI team
  - align before finalizing UI tasks

If the project does not use UI JSON:
- Skip these checks without failing.

---

## 6) Testing Expectations

Generate/update tests aligned with tasks and registries:

- Unit tests for domain logic.
- Integration tests for service + data access.
- Contract tests for APIs.
- Performance tests when NFRs specify SLAs.

For UI specs:
- Component tests focusing on rendering and state.
- Avoid encoding business rules inside UI tests that should be verified at service level.

---

## 7) Post-Implementation Validation

Before marking tasks complete:

- Re-run quick consistency checks:
  - APIs/models/terms used match registries.
  - No new conflicting names introduced.

- If new shared definitions were introduced:
  - record them in implementation notes
  - recommend running `/smartspec_sync_spec_tasks --mode=additive`

---

## 8) Output Summary

Provide an implementation summary including:

- Tasks completed
- Files changed
- Any registry alignment warnings
- Any UI JSON compliance notes
- Recommended follow-up workflows:
  - `/smartspec_verify_tasks_progress`
  - `/smartspec_generate_tests` (if needed)
  - `/smartspec_sync_spec_tasks --mode=additive` (if new shared items emerged)

---

## Notes

- This workflow is conservative about shared-name creation to prevent cross-SPEC conflicts.
- The canonical truth for cross-SPEC definitions is `.spec/registry/` when present.
- `.spec/SPEC_INDEX.json` is the canonical index; root index is legacy mirror.

