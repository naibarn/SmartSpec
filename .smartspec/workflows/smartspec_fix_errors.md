---
description: Fix implementation errors with SmartSpec centralization (.spec) and UI JSON addendum
version: 5.2
---

# /smartspec_fix_errors

Analyze implementation errors (build failures, test failures, runtime errors, integration issues) and propose or apply fixes aligned with the canonical SmartSpec knowledge layer.

This workflow enforces SmartSpec centralization:
- **`.spec/` is the canonical project space** for shared truth.
- `.smartspec/` is tooling-only.
- Shared definitions must be aligned via **`.spec/registry/`**.
- **UI specs use `ui.json` as the design source of truth** for Penpot integration.

---

## What It Does

- Resolves canonical `SPEC_INDEX.json`.
- Loads shared registries.
- Identifies the relevant spec(s) for the error context.
- Cross-checks expected behavior against `spec.md` + `tasks.md`.
- Detects root causes that may be:
  - implementation defects
  - cross-SPEC naming drift
  - contract mismatches
  - missing dependencies
  - incorrect test assumptions
  - UI JSON vs component misalignment
- Produces a **safe, spec-aligned fix plan**.

---

## When to Use

- CI failures after implementing a SPEC.
- Local build/test failures.
- Integration regressions across multiple specs.
- UI mismatches between design and runtime components.

---

## Inputs

- Error logs or failure summaries.
- Target spec path (recommended).

Expected adjacent files:
- `spec.md`
- `tasks.md` (if present)
- (UI specs) `ui.json`

---

## Outputs

- A structured fix plan.
- Recommended code changes.
- Recommendations for registry or index updates (non-destructive by default).
- Suggested follow-up workflows.

---

## Flags

- `--index` Path to SPEC_INDEX (optional)  
  default: auto-detect

- `--registry-dir` Registry directory (optional)  
  default: `.spec/registry`

- `--spec` Explicit spec path (optional)

- `--tasks` Explicit tasks path (optional)

- `--mode` `recommend` | `additive-meta`  
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
```

### 0.3 Expected Registries (if present)

- `api-registry.json`
- `data-model-registry.json`
- `glossary.json`
- `critical-sections-registry.json`
- `patterns-registry.json` (optional)
- `ui-component-registry.json` (optional)

Rules:
- Registry names are canonical.
- Prefer adjusting implementation to match registry over introducing new shared names.

---

## 1) Identify Target Spec(s)

Priority:
1) `--spec` / `--tasks` if provided.
2) If `INDEX_PATH` exists, select spec by ID matching the error area.
3) If ambiguous, resolve by folder context of failing files.

Default tasks location:
- `tasks.md` next to `spec.md`.

---

## 2) Read Spec + Tasks (Read-Only Inputs)

- Read `spec.md`.
- Read `tasks.md` if present.
- Extract:
  - expected APIs
  - model definitions
  - NFRs
  - security requirements
  - UI rules if applicable

Do not rewrite these files in this workflow.

---

## 3) Error Classification

Classify errors into one or more buckets:

1) **Build/Type Errors**
2) **Unit Test Failures**
3) **Integration/Contract Failures**
4) **Performance Regression**
5) **Security Enforcement Gaps**
6) **UI/Component Mismatch**
7) **Cross-SPEC Naming Drift**

---

## 4) Cross-SPEC Consistency Gate

If `INDEX_PATH` exists:
- Confirm that the failing spec's dependencies are implemented/available.
- Check whether an upstream spec changed shared contracts.

If registries exist:
- Compare:
  - endpoints referenced in failing tests/code
  - model names
  - domain terms

If mismatch detected:
- In `--strict` mode: stop and report conflict.
- Otherwise: provide a **conflict-resolution fix plan**.

---

## 5) Fix Strategy by Error Type

### 5.1 Build/Type Errors

- Prefer aligning types/interfaces with canonical models in `data-model-registry.json`.
- If local types diverged:
  - update code to match registry
  - generate a follow-up recommendation for registry additive updates only when the spec clearly requires new shared types

### 5.2 Unit Test Failures

- Verify the test expectation maps to a spec requirement.
- If the test assumed an unregistered name:
  - rename test to canonical name.

### 5.3 Integration/Contract Failures

- Confirm API route naming matches `api-registry.json` if present.
- Validate request/response schema expectations.
- If two specs disagree:
  - create a blocking reconciliation item.

### 5.4 Performance Regression

- Compare measured results against spec SLAs.
- Recommend optimizations aligned with intended architecture/patterns.
- Do not change SLAs unilaterally.

### 5.5 Security Enforcement Gaps

- Ensure auth/authz hooks are applied at the correct layers.
- Verify permission model aligns with security/core specs.

### 5.6 UI/Component Mismatch

- Check if `ui.json` exists.
- If yes:
  - verify component IDs/names used in code match UI JSON.
  - verify names match `ui-component-registry.json` when available.
  - prefer updating code to match design.
- If design and runtime diverge meaningfully:
  - create a UI-team handoff task.

### 5.7 Cross-SPEC Naming Drift

- Prefer consolidating to the canonical registry term.
- If a rename/migration is required:
  - propose a phased migration plan.
  - recommend running `/smartspec_sync_spec_tasks --mode=additive` after agreement.

---

## 6) UI JSON Addendum (Conditional)

Apply when:
- Spec category is `ui`, or
- `ui.json` exists.

Rules:
- `ui.json` is design-owned.
- Do not move business logic into UI JSON.
- If logic appears to be encoded at the UI boundary:
  - refactor logic into service/controller layers
  - keep UI testing focused on rendering and state orchestration

If the project does not use UI JSON:
- Skip UI checks without failing.

---

## 7) Mode Behavior

### `recommend` (default)

- Provide code fix suggestions.
- Output registry/index recommendations.
- Do not write shared files.

### `additive-meta`

- Allowed safe updates:
  - add missing non-breaking metadata in central files (when your system supports it)
- Never delete or rename registry entries automatically.
- Never rewrite existing `spec.md` contents.

---

## 8) Output Fix Report

Provide a structured report:

- Error summary
- Root cause hypothesis
- Evidence from spec/tasks/index
- Proposed fixes
- Risk level
- Registry alignment notes
- UI JSON compliance notes (if applicable)

---

## 9) Recommended Follow-ups

- `/smartspec_verify_tasks_progress`
- `/smartspec_generate_tests`
- `/smartspec_sync_spec_tasks --mode=additive` (after review)
- `/smartspec_refactor_code` (if structural fixes are needed)

---

## Notes

- This workflow is conservative and prioritizes preventing new cross-SPEC conflicts.
- Canonical shared truth is `.spec/registry/` when present.
- Root `SPEC_INDEX.json` is treated as a legacy mirror.

