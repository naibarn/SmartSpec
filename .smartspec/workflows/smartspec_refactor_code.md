---
description: Refactor code safely with SmartSpec centralization (.spec) and UI JSON addendum
version: 5.2
---

# /smartspec_refactor_code

Refactor existing code while preserving behavioral correctness and maintaining alignment with SmartSpec canonical knowledge.

This workflow enforces SmartSpec centralization:
- **`.spec/` is the canonical project space** for index + registries.
- `.smartspec/` is tooling-only.
- Shared definitions must be aligned via **`.spec/registry/`**.
- **UI specs use `ui.json` as a design source of truth** for Penpot integration.

---

## What It Does

- Resolves canonical `SPEC_INDEX.json`.
- Loads shared registries.
- Identifies the target spec(s) and the scope of refactor.
- Creates a refactor plan that:
  - avoids cross-SPEC naming drift
  - preserves public contracts
  - improves maintainability/performance
  - separates UI structure from business logic when UI JSON is used
- Recommends test updates to maintain confidence.

---

## When to Use

- After implementation stabilized and needs cleanup.
- When multiple specs share patterns that should be consolidated.
- When UI code accidentally accumulated business logic.
- Before major releases to reduce technical debt.

---

## Inputs

- Target spec path (recommended) or a set of files/modules to refactor.
- Optional error/performance reports.

Expected adjacent files:
- `spec.md`
- `tasks.md` (if present)
- (UI specs) `ui.json`

---

## Outputs

- A structured refactor plan.
- Code change recommendations.
- Proposed test updates.
- Registry/index recommendations (non-destructive by default).

---

## Flags

- `--index` Path to SPEC_INDEX (optional)  
  default: auto-detect

- `--registry-dir` Registry directory (optional)  
  default: `.spec/registry`

- `--spec` Explicit spec path (optional)

- `--scope` Optional refactor scope hint  
  examples: `api`, `domain`, `infra`, `ui`, `tests`, `cross-spec-shared`

- `--mode` `recommend` | `safe-apply`  
  default: `recommend`

- `--strict` Fail on ambiguity (optional)

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
  echo "⚠️ SPEC_INDEX not found. Proceeding with local context only."
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

MODE="${FLAGS_mode:-recommend}"
SCOPE="${FLAGS_scope:-}"
```

### 0.3 Expected Registries (if present)

- `api-registry.json`
- `data-model-registry.json`
- `glossary.json`
- `critical-sections-registry.json`
- `patterns-registry.json` (optional)
- `ui-component-registry.json` (optional)

Canonical rules:
- Prefer refactoring code to match existing registry names.
- Do not rename shared contracts without a migration plan.

---

## 1) Identify Target Spec(s) and Refactor Surface

Priority:
1) `--spec` if provided.
2) If `INDEX_PATH` exists, choose by spec ID.
3) Otherwise, infer from file paths the user provided.

Determine refactor surface:
- APIs/Controllers
- Domain Models
- Services/Use cases
- Infrastructure
- Shared libraries/patterns
- UI components
- Tests

---

## 2) Read Inputs (Read-Only)

- Read `spec.md` and `tasks.md` if present.
- Extract:
  - stable public contracts
  - NFRs and performance constraints
  - security requirements
  - known shared patterns

If UI spec:
- Detect `ui.json`.

Do not rewrite `spec.md` or `ui.json` in this workflow.

---

## 3) Cross-SPEC Safety Gate

If `INDEX_PATH` exists:
- Verify that the refactor does not break dependency contracts.
- Identify other specs that depend on the target spec.

If registries exist:
- Ensure refactor does not introduce:
  - new API route names
  - new model names
  - new domain terms
  that conflict with canonical entries.

In `--strict` mode:
- Stop and report any ambiguous rename risk.

---

## 4) Refactor Goals and Allowed Changes

### 4.1 Always Allowed (Safe)

- Extract duplicated logic into internal helpers.
- Improve readability and structure.
- Reduce cyclomatic complexity.
- Add missing tests.
- Optimize hot paths **without changing externally observable behavior**.

### 4.2 Allowed With Care

- Rename internal symbols that are not part of shared contracts.
- Move files/folders while updating imports.

### 4.3 Requires Explicit Migration Plan

- Any change to:
  - public API signatures
  - event names
  - shared model shapes
  - cross-SPEC interfaces

When needed:
- Create a phased plan:
  - compatibility layer
  - dual support period
  - deprecation notes
  - registry update recommendation

---

## 5) Recommended Refactor Patterns

Use registries/patterns when available:

- Prefer `patterns-registry.json` / documented patterns rather than creating new architectural styles.
- Extract common cross-SPEC utilities into shared modules.
- Align DI, caching, error handling, logging patterns across specs.

If a pattern is missing but clearly repeated:
- Add a **recommendation** to create a shared pattern document.

---

## 6) UI JSON Addendum (Conditional)

Apply when:
- Spec category is `ui`, or
- `ui.json` exists.

Rules:
- `ui.json` is design-owned and remains JSON-based for Penpot.
- UI refactors must focus on:
  - component structure
  - props typing
  - rendering performance
  - accessibility improvements

Strict separation:
- Business logic belongs in:
  - services
  - hooks
  - controllers
  - domain layer

If UI code currently embeds heavy logic:
- Propose refactor steps:
  1) Identify logic blocks.
  2) Create service/hook abstractions.
  3) Replace UI logic with calls/orchestration.
  4) Add unit tests at the logic layer.
  5) Keep UI tests focused on state/render.

Component naming:
- If `ui-component-registry.json` exists:
  - align component names with registry.
  - do not invent new shared component names without recommendation.

If the project does not use UI JSON:
- Skip UI JSON checks without failing.

---

## 7) Test Alignment

Before applying refactors:
- Ensure baseline tests exist for critical behaviors.

During refactor:
- Update tests to reflect internal restructuring.
- Keep contract/API tests stable.

After refactor:
- Re-run:
  - unit tests
  - integration tests
  - contract tests
  - performance tests if SLAs exist

If new shared names would be required for tests:
- Flag as registry drift risk.

---

## 8) Mode Behavior

### `recommend` (default)

- Provide a refactor plan and prioritized steps.
- Highlight cross-SPEC risks.
- Output registry/index recommendations.

### `safe-apply`

Only apply changes when all are true:
- The refactor is internal-only or backward compatible.
- No registry conflicts are introduced.
- No dependency break is detected.
- UI JSON rules remain satisfied.

Never automatically:
- rename a registered shared API/model/term
- delete registry entries
- rewrite `ui.json`

---

## 9) Output Refactor Report

Include:

- Scope summary
- Detected shared dependencies
- Registry alignment status
- Proposed refactor steps (ordered)
- Risk assessment
- Test plan updates
- UI JSON compliance notes (if applicable)

---

## 10) Recommended Follow-ups

- `/smartspec_generate_tests` (ensure coverage)
- `/smartspec_verify_tasks_progress`
- `/smartspec_sync_spec_tasks --mode=additive` (after team review)
- `/smartspec_reindex_specs` (if spec paths or categories changed)

---

## Notes

- This workflow is designed to reduce technical debt without reintroducing cross-SPEC conflicts.
- `.spec/registry/` remains the shared canonical truth when present.
- Root `SPEC_INDEX.json` is treated as a legacy mirror.
