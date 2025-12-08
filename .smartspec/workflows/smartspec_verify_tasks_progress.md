---
description: Verify implementation progress against tasks/specs with SmartSpec v5.6 centralization, multi-repo + multi-registry alignment, safety-mode, and UI JSON addendum
version: 5.6
---

# /smartspec_verify_tasks_progress

Verify real implementation progress against `tasks.md`, `spec.md`, and the canonical SmartSpec centralized knowledge layer.

This v5.6 workflow preserves the original v5.2 intent and structure while extending it to match the upgraded chain (spec → plan → tasks → implement → verify) for multi-repo and multi-registry programs.

SmartSpec centralization remains unchanged:

- **`.spec/` is the canonical project-owned space**.
- **`.spec/SPEC_INDEX.json` is the canonical index**.
- **`.spec/registry/` is the shared source of truth**.
- `SPEC_INDEX.json` at repo root is a **legacy mirror**.
- `.smartspec/` is tooling-only.
- **UI specs use `ui.json` as the design source of truth** for Penpot integration.

---

## What It Does

- Resolves canonical index and registry locations.
- Builds a merged registry validation view (primary + supplemental).
- Identifies the target spec and its adjacent tasks.
- Verifies progress using evidence from:
  - task status markers
  - code structure changes
  - test coverage signals
  - configuration and documentation updates
- Detects cross-SPEC and cross-repo drift risks.
- Validates UI separation rules when UI JSON is present.
- Produces a progress report and next-step recommendations.

---

## When to Use

- During daily/weekly progress reviews.
- Before merging a large PR.
- Before cutting a release.
- After running `/smartspec_implement_tasks`.
- After cross-repo dependency updates.

---

## Inputs

- Target spec path (recommended)
  - Example: `specs/core/spec-core-004-rate-limiting/spec.md`

- Expected adjacent files:
  - `tasks.md`
  - (UI specs) `ui.json`

- Optional governance inputs:
  - `.spec/SPEC_INDEX.json`
  - `.spec/registry/*.json`
  - supplemental registries from sibling repos

---

## Outputs

- A structured progress report under:
  - `.spec/reports/verify-tasks-progress/`
- Optional summary printed to console.

---

## Flags

### Index / Registry (v5.6-aligned)

- `--index` Path to SPEC_INDEX (optional)  
  default: auto-detect

- `--specindex` Legacy alias for `--index`

- `--registry-dir` Primary registry directory (optional)  
  default: `.spec/registry`

- `--registry-roots` Supplemental registry dirs, comma-separated (optional)
  - **Read-only validation sources** to prevent cross-repo duplicate naming.

### Multi-Repo (NEW alignment)

- `--workspace-roots` Comma-separated repo roots to search (optional)

- `--repos-config` Path to structured repo config (optional)
  - takes precedence over `--workspace-roots`
  - recommended: `.spec/smartspec.repos.json`

### Target Selection

- `--spec` Explicit spec path (optional)

- `--tasks` Explicit tasks path (optional)

### Reporting

- `--report-dir` Output report directory (optional)  
  default: `.spec/reports/verify-tasks-progress/`

- `--report` `summary` | `detailed` (optional)
  default: `summary`

### Safety / Preview

- `--safety-mode` `strict` | `dev` (optional)
  default: `strict`

- `--strict` Legacy alias for strict gating

- `--dry-run` Print report only (do not write files)

---

## 0) Resolve Canonical Index & Registry

### 0.1 Resolve SPEC_INDEX (Single Source of Truth)

Detection order:

1) `.spec/SPEC_INDEX.json` (canonical)  
2) `SPEC_INDEX.json` (legacy root mirror)  
3) `.smartspec/SPEC_INDEX.json` (deprecated)  
4) `specs/SPEC_INDEX.json` (older layout)

### 0.2 Resolve Registry View

1) Load primary registry from `--registry-dir`.
2) If provided, load `--registry-roots` as **read-only**.

**Precedence rules:**

- Primary registry entries are authoritative.
- Supplemental registries are used to detect collisions and ownership ambiguity.

### 0.3 Resolve Multi-Repo Roots

- Build repo root list using `--repos-config` if present.
- Otherwise merge `--workspace-roots` with the current repo.

---

## 1) Identify Target Spec/Tasks

Priority:

1) Use `--spec` / `--tasks` if provided.
2) If index exists, allow selecting by spec ID (implementation-dependent).
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
6) **Cross-repo reuse correctness**
7) **UI compliance (if applicable)**

---

## 4) Validate Dependency Readiness

If index is available:

- Cross-check spec dependencies.
- Warn if:
  - a dependency spec is missing critical artifacts
  - tasks appear to implement dependent features out of order

In `--safety-mode=strict`:

- Treat major dependency-order violations as errors.

---

## 5) Registry Alignment Checks (Conditional)

If registries are available:

- Verify that names referenced in the target spec/tasks (and observed in code when inferable) match the merged registry view:
  - API names/route prefixes
  - model names
  - domain terms
  - critical cross-cutting sections
  - shared patterns
  - UI component names (if UI registry exists)

**v5.6 cross-repo safeguard:**

- If the same name exists in a supplemental registry with a conflicting meaning, the report must:
  - mark it as an ownership ambiguity
  - recommend governance reconciliation
  - discourage local “new shared name” creation

---

## 6) Evidence-Based Progress Evaluation

The verification must distinguish between:

- **Declared progress** (task checkboxes, status labels)
- **Observed progress** (code/tests/config changes)

### 6.1 Task Status Signals

- Parse `tasks.md` status markers.
- Identify blocked, missing, or newly introduced tasks.

### 6.2 Code Structure Signals

Best-effort checks may include:

- Modules/services created for major task groups.
- API/controller presence for declared endpoints.
- Data model definitions aligned with spec and registries.
- Shared utility usage when tasks prefer reuse.

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
4) Verify that UI implementation aligns with `ui.json` structure.

Checks:

- If `ui.json` exists:
  - confirm `tasks.md` includes component mapping and logic separation tasks.

- If `ui-component-registry.json` exists:
  - verify that component names used in tasks/implementation match the registry.

- If UI specs are active but `ui.json` is missing:
  - add a high-visibility warning.

---

## 8) Report Schema (Suggested)

A v5.6 report should include:

- Spec ID/title/path
- Tasks path
- Index path used (or NONE)
- Primary registry dir
- Supplemental registry roots
- Multi-repo roots or config used
- Declared vs observed completion summary
- Dependency readiness
- Registry alignment status
- UI compliance (if applicable)
- Recommended next tasks

---

## 9) Recommended Follow-Ups

- `/smartspec_fix_errors`
- `/smartspec_generate_tests`
- `/smartspec_sync_spec_tasks`
- `/smartspec_global_registry_audit` (for large drift)
- `/smartspec_validate_index`

---

## Notes

- This workflow is intentionally conservative.
- It must not mark tasks “done” solely based on checkbox state without any observed evidence.
- In multi-repo programs, lack of `--registry-roots` should reduce confidence scoring and be recorded explicitly in the report.

