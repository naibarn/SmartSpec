---
description: Generate tests from spec(s) and tasks with SmartSpec centralization (.spec) and UI JSON addendum
version: 5.2
---

# /smartspec_generate_tests

Generate a comprehensive test plan and, where applicable, test scaffolding suggestions based on `spec.md`, `tasks.md`, `SPEC_INDEX`, and shared registries.

This workflow enforces SmartSpec centralization:
- **`.spec/` is the canonical project space** for index + registries.
- `.smartspec/` is tooling-only.
- Shared definitions must be aligned via **`.spec/registry/`**.
- **UI specs use `ui.json` as the design source of truth** for Penpot integration.

---

## What It Does

- Resolves canonical `SPEC_INDEX.json`.
- Loads shared registries.
- Reads target `spec.md` and `tasks.md`.
- Builds a test matrix covering:
  - unit tests
  - integration tests
  - contract/API tests
  - security tests
  - performance/SLA tests
  - UI/component tests (when applicable)
- Prevents re-invented naming by verifying registry alignment.
- Applies UI JSON addendum rules conditionally.

---

## When to Use

- After `tasks.md` generation.
- Before implementation starts.
- When expanding test coverage for large, multi-SPEC systems.
- During refactors to ensure parity with original requirements.

---

## Inputs

- Target spec path (recommended)
  - Example: `specs/core/spec-core-004-rate-limiting/spec.md`

- Expected adjacent files:
  - `tasks.md`
  - (UI specs) `ui.json`

---

## Outputs

- A test plan (recommended location: next to the spec)
  - `tests.md` or `test-plan.md`
- Optional test scaffolding recommendations
- Cross-SPEC consistency notes

---

## Flags

- `--index` Path to SPEC_INDEX (optional)  
  default: auto-detect

- `--registry-dir` Registry directory (optional)  
  default: `.spec/registry`

- `--spec` Explicit spec path (optional)

- `--tasks` Explicit tasks path (optional)

- `--output` Output test plan path (optional)

- `--strict` Fail on warnings (optional)

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
- Use registry names as canonical references in the test plan.
- If a test references a new shared API/model/term name:
  - flag it
  - recommend an additive registry sync.

---

## 1) Identify Target Spec/Tasks

Priority:
1) `--spec` / `--tasks` if provided.
2) If `INDEX_PATH` exists, allow selecting by spec ID.
3) Otherwise, require user to provide a spec path.

Default tasks location:
- `tasks.md` next to `spec.md`.

---

## 2) Read Inputs (Read-Only)

- Read `spec.md`.
- Read `tasks.md` if present.
- Collect NFRs (SLAs, performance, security).
- If UI spec:
  - detect `ui.json`.

This workflow does not rewrite these inputs.

---

## 3) Cross-SPEC Alignment Gate

If `INDEX_PATH` exists:
- Ensure tests do not assume features that conflict with dependencies.
- Validate that referenced dependent specs have compatible testing assumptions.

If registries exist:
- Confirm names used in tests match:
  - API registry
  - Model registry
  - Glossary

In `--strict` mode:
- Stop if cross-SPEC naming drift is detected.

---

## 4) Build Test Matrix

Construct a matrix with traceability to:
- Spec sections
- Task groups
- Registry entries

### 4.1 Unit Tests

- Domain logic
- Utility and validation rules
- Data transformations

### 4.2 Integration Tests

- Service layer interactions
- Database/repository integration
- Message/event buses (if applicable)

### 4.3 Contract / API Tests

- Endpoint behavior
- Request/response schemas
- Error codes
- Backward-compatible behavior

If `api-registry.json` exists:
- Ensure the plan names endpoints exactly as registered.

### 4.4 Security Tests

- Authentication/authorization enforcement points
- Rate limiting rules
- Audit logging completeness (when specified)
- Negative path validations

### 4.5 Performance / SLA Tests

When spec includes SLAs:
- Define measurable test cases
- Include target percentiles (e.g., p95) exactly as specified
- Include baseline data sets and load profiles

### 4.6 Observability Tests (Lightweight)

- Logging events present for critical flows
- Metrics emitted for key counters/latencies
- Traces connected across boundaries

### 4.7 UI / Component Tests (Conditional)

Apply when:
- Spec category is `ui`, or
- `ui.json` exists.

Focus areas:
- Component rendering
- State transitions
- Accessibility basics
- Visual regression targets (if your stack supports)

Avoid validating business rules solely in UI tests when those rules belong to service/domain layers.

---

## 5) UI JSON Addendum (Conditional)

Rules:
- Treat `ui.json` as **design-owned**.
- Tests should validate:
  - component IDs/names used in UI code match `ui.json`
  - component names align with `ui-component-registry.json` when present
- Do not require or encourage embedding logic inside `ui.json`.

If the project does not use UI JSON:
- Skip this section without failing.

---

## 6) Generate Test Plan Document

Recommended content:

1) Scope
2) Assumptions
3) Dependencies
4) Test Matrix (table)
5) Data/fixtures requirements
6) Tooling recommendations
7) Risks & gaps
8) Registry alignment notes
9) UI JSON compliance notes (if applicable)

Default output path:
- next to the spec:
  - `tests.md`

If `--output` provided:
- write to that path.

If `--dry-run`:
- print only.

---

## 7) Quality Gates

Before finalizing:
- Ensure every major spec section maps to at least one test group.
- Ensure tasks with high risk have explicit tests.
- Ensure shared names come from registries where available.
- Ensure UI tests are separated from business logic verification.

---

## 8) Recommended Follow-ups

- `/smartspec_verify_tasks_progress`
- `/smartspec_implement_tasks`
- `/smartspec_sync_spec_tasks --mode=additive` when new shared names are discovered

---

## Notes

- This workflow is intentionally conservative to avoid introducing cross-SPEC naming drift.
- `.spec/registry/` remains the canonical shared truth when present.
- Root `SPEC_INDEX.json` is treated as legacy mirror only.

