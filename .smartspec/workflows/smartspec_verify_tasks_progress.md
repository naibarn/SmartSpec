---
description: Verify implementation progress against tasks/specs with SmartSpec v5.2 centralization and UI JSON addendum
version: 5.2
---

# /smartspec_verify_tasks_progress

Verify real implementation progress against `tasks.md`, `spec.md`, and the canonical SmartSpec centralized knowledge layer.

This workflow enforces SmartSpec v5.2 centralization:
- **`.spec/` is the canonical project-owned space**.
- **`.spec/SPEC_INDEX.json` is the canonical index**.
- **`.spec/registry/` is the shared source of truth**.
- `SPEC_INDEX.json` at repo root is a **legacy mirror**.
- `.smartspec/` is tooling-only.
- **UI specs use `ui.json` as the design source of truth** for Penpot integration.

---

## What It Does

- Resolves canonical index and registry locations.
- Identifies the target spec and its adjacent tasks.
- Verifies progress using evidence from:
  - task status markers
  - code structure changes
  - test coverage signals
  - configuration and documentation updates
- Detects cross-SPEC drift risks.
- Validates UI separation rules when UI JSON is present.
- Produces a progress report and next-step recommendations.

---

## When to Use

- During daily/weekly progress reviews.
- Before merging a large PR.
- Before cutting a release.
- After running `/smartspec_implement_tasks`.

---

## Inputs

- Target spec path (recommended)
  - Example: `specs/core/spec-core-004-rate-limiting/spec.md`

- Expected adjacent files:
  - `tasks.md`
  - (UI specs) `ui.json`

---

## Outputs

- A structured progress report under:
  - `.spec/reports/verify-tasks-progress/`
- Optional summary printed to console.

---

## Flags

- `--index` Path to SPEC_INDEX (optional)  
  default: auto-detect

- `--registry-dir` Registry directory (optional)  
  default: `.spec/registry`

- `--report-dir` Output report directory (optional)  
  default: `.spec/reports/verify-tasks-progress/`

- `--spec` Explicit spec path (optional)

- `--tasks` Explicit tasks path (optional)

- `--strict` Fail on warnings or ambiguous completion signals (optional)

- `--dry-run` Print report only (do not write files)

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
  echo "⚠️ SPEC_INDEX not found. Verification will proceed with local evidence only."
  INDEX_PATH=""
fi
```

### 0.2 Resolve Registry Directory

```bash
REGISTRY_DIR="${FLAGS_registry_dir:-.spec/registry}"
REGISTRY_AVAILABLE=false

if [ -d "$REGISTRY_DIR" ]; then
  REGISTRY_AVAILABLE=true
fi

REPORT_DIR="${FLAGS_report_dir:-.spec/reports/verify-tasks-progress}"
mkdir -p "$REPORT_DIR"

STRICT="${FLAGS_strict:-false}"
DRY_RUN="${FLAGS_dry_run:-false}"
```

### 0.3 Expected Registries (if present)

- `api-registry.json`
- `data-model-registry.json`
- `glossary.json`
- `critical-sections-registry.json`
- `patterns-registry.json` (optional)
- `ui-component-registry.json` (optional)

Rules:
- If registries exist, they are authoritative for shared-name verification.
- This workflow does not rewrite registries.

---

## 1) Identify Target Spec/Tasks

Priority:

1) Use `--spec` / `--tasks` if provided.
2) If `INDEX_PATH` exists, allow selecting a spec by ID.
3) Otherwise, require a spec path.

Default tasks location:
- `tasks.md` next to `spec.md`.

---

## 2) Read Inputs (Read-Only)

- Read `spec.md`.
- Read `tasks.md` if present.
- Detect `ui.json` if present.

Do not rewrite these files.

---

## 3) Build Verification Checklist

Create a spec-aligned checklist to evaluate evidence for:

1) **Task completion**
2) **Contract correctness**
3) **Test coverage**
4) **NFR fulfillment**
5) **Cross-SPEC alignment**
6) **UI compliance (if applicable)**

---

## 4) Validate Dependency Readiness

If `INDEX_PATH` exists:

- Cross-check spec dependencies.
- Warn if:
  - a dependency spec is not implemented or is missing critical artifacts.
  - tasks appear to implement dependent features out of order.

In `--strict` mode:
- Treat major dependency-order violations as errors.

---

## 5) Registry Alignment Checks (Conditional)

If `REGISTRY_AVAILABLE=true`:

- Verify that names referenced in the target spec/tasks (and observed in code, when inferable) match registries:
  - API names/route prefixes
  - model names
  - domain terms
  - critical cross-cutting sections

If mismatch detected:
- Prefer that implementation aligns to registry.
- Record drift warnings.

This workflow does not rename registry entries.

---

## 6) Evidence-Based Progress Evaluation

The verification should distinguish between:

- **Declared progress** (task checkboxes, status labels)
- **Observed progress** (code/tests/config changes)

### 6.1 Task Status Signals

- Parse `tasks.md` status markers.
- Identify blocked or missing tasks.

### 6.2 Code Structure Signals

Best-effort checks:
- Modules/services created for major task groups.
- API/controller presence for declared endpoints.
- Data model definitions aligned with spec.

### 6.3 Test Signals

- Unit tests present for domain logic.
- Integration/contract tests present for critical flows.
- Performance tests present when SLAs exist.

### 6.4 NFR Signals

When spec includes NFRs:
- Verify evidence exists for:
  - logging
  - metrics
  - tracing
  - security enforcement
  - rate limiting / auditing as applicable

---

## 7) UI JSON Addendum (Conditional)

Apply when **any** of these are true:

- Spec category is `ui` in SPEC_INDEX
- `ui.json` exists in the spec folder
- The spec explicitly mentions Penpot/UI JSON workflow

Rules:

1) **UI design source of truth is JSON** (`ui.json`).
2) Treat `ui.json` as design-owned.
3) Do not embed business logic in UI JSON.
4) Verify that UI implementation aligns with `ui.json` component structure.

Checks:

- If `ui.json` exists:
  - confirm `tasks.md` includes component mapping and logic separation tasks.

- If `ui-component-registry.json` exists:
  - verify that component names used in tasks/implementation match registry.

- If a UI spec is declared but `ui.json` is missing:
  - warn and recommend creation.

Non-UI projects:
- Do not fail.
- Skip UI checks unless a spec explicitly declares itself as UI.

---

## 8) Progress Scoring (Optional Heuristic)

Provide a qualitative summary per major task group:

- Not started
- In progress
- Blocked
- Functionally complete (tests missing)
- Complete (with tests)

Avoid overstating completion without evidence.

---

## 9) Report

Write a structured report to `REPORT_DIR` including:

- Index path used
- Registry availability
- Target spec/tasks paths
- Dependency findings
- Task status summary
- Evidence summary (code/tests/NFR)
- Cross-SPEC drift warnings
- UI JSON compliance summary (if applicable)
- Recommended next actions

If `--dry-run`:
- Print the report only.

---

## 10) Recommended Follow-ups

Depending on findings:

- `/smartspec_fix_errors`
- `/smartspec_generate_tests`
- `/smartspec_refactor_code`
- `/smartspec_sync_spec_tasks --mode=additive` (after review)
- `/smartspec_validate_index`

---

## Notes

- This workflow is intentionally conservative to prevent false completion claims.
- `.spec/SPEC_INDEX.json` is canonical; root index remains a legacy mirror.
- `.spec/registry/` is the authoritative shared-name source when present.

