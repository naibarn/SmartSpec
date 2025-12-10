---
name: /smartspec_verify_tasks_progress
version: 5.7.0
role: verification/governance
write_guard: NO-WRITE
purpose: Verify real implementation progress against tasks/specs and the SmartSpec centralized layer under full v5.6–v5.7 governance (multi-repo, multi-registry, safety-mode, UI JSON addendum).
version_notes:
  - v5.2: initial verify-tasks workflow
  - v5.6: centralization + multi-repo / multi-registry alignment
  - v5.7.0: governance alignment; UI metadata signals; expanded safety; backward-compatible; documentation-only update
---

# /smartspec_verify_tasks_progress (v5.7.0)

Verify real implementation progress against `tasks.md`, `spec.md`, and the canonical SmartSpec centralized knowledge layer.

This workflow keeps all v5.6 behavior【preserved from spec】 while aligning with the broader v5.7 governance suite:

- centralization: `.spec/`, SPEC_INDEX, `.spec/registry/`
- multi-repo: `--repos-config`, `--workspace-roots`
- multi-registry: primary + supplemental registries with precedence
- safety-mode: `strict` vs `dev` semantics
- UI JSON: design-owned source of truth, with metadata signals

> **Scope:**
> - Read-only with respect to code/spec/tasks/registries/UI JSON.
> - Writes only **reports** under `.spec/reports/verify-tasks-progress/` unless `--dry-run`.

---
## 1) What It Does

- Resolve canonical index and registry locations.
- Build a merged registry validation view (primary + supplemental).
- Identify the target spec and its adjacent tasks.
- Verify progress using evidence from:
  - task status markers
  - code structure changes
  - test coverage signals
  - configuration and documentation updates
- Detect cross-SPEC and cross-repo drift risks.
- Validate UI separation rules when UI JSON is present.
- Produce a progress report and next-step recommendations.

(Behavior consistent with the v5.6 description.)

---
## 2) When to Use

- Daily/weekly progress reviews.
- Before merging a large PR.
- Before cutting a release.
- After `/smartspec_implement_tasks`.
- After cross-repo dependency updates.

---
## 3) Inputs

- Target spec path (recommended), e.g.:
  - `specs/core/spec-core-004-rate-limiting/spec.md`

Expected adjacent files:

- `tasks.md`
- (UI specs) `ui.json`

Governance inputs:

- `.spec/SPEC_INDEX.json`
- `.spec/registry/*.json`
- supplemental registries from sibling repos (via `--registry-roots`)

---
## 4) Outputs

- Structured progress report under:
  - `.spec/reports/verify-tasks-progress/`
- Optional summary printed to console / stdout.

Optional future extension (implementation-dependent):

- JSON-formatted report (when `--report-format=json` is supported).

---
## 5) Flags (v5.7-aligned)

### 5.1 Index / Registry

- `--index=<path>`  
  Path to SPEC_INDEX (optional); default: auto-detect.

- `--specindex=<path>`  
  Legacy alias for `--index`.

- `--registry-dir=<path>`  
  Primary registry directory (optional); default: `.spec/registry`.

- `--registry-roots=<csv>`  
  Supplemental registry dirs (comma- or semicolon-separated).  
  **Read-only** validation sources to prevent cross-repo duplicate naming.

### 5.2 Multi-Repo

- `--workspace-roots=<csv>`  
  Repo roots to search for additional specs.

- `--repos-config=<path>`  
  Structured repo config; takes precedence over `--workspace-roots`.  
  Recommended: `.spec/smartspec.repos.json`.

### 5.3 Target Selection

- `--spec=<path>`  
  Explicit spec path (optional).

- `--tasks=<path>`  
  Explicit tasks path (optional).

Implementation MAY also support:

- `--spec-id=<id>`  
  index-based selection (tool-specific).

### 5.4 Reporting

- `--report-dir=<path>`  
  Output report directory (optional); default: `.spec/reports/verify-tasks-progress/`.

- `--report=<summary|detailed>`  
  default: `summary`.

- `--report-format=<md|json>` (optional, additive in v5.7)  
  default: `md` when supported.

### 5.5 Safety / Preview

- `--safety-mode=<strict|dev>`  
  default: `strict`.

- `--strict`  
  Legacy alias for `--safety-mode=strict`.

- `--dry-run`  
  Print report only (no file writes).

---
## 6) 0) Resolve Canonical Index & Registry

### 6.1 SPEC_INDEX (Single Source of Truth)

Detection order:

1. `.spec/SPEC_INDEX.json` (canonical)  
2. `SPEC_INDEX.json` (legacy root mirror)  
3. `.smartspec/SPEC_INDEX.json` (deprecated)  
4. `specs/SPEC_INDEX.json` (older layout)

If no index:

- Proceed with local-only context.
- Record missing index as governance gap in the report.

In `strict` safety-mode:

- downgrade confidence and mark some cross-SPEC checks as **incomplete**.

### 6.2 Registry View

1. Load primary registry from `--registry-dir` when present.  
2. Load `--registry-roots` as read-only.

Precedence rules:

- Primary registry entries are authoritative.
- Supplemental registries detect collisions and ownership ambiguity.

### 6.3 Multi-Repo Roots

- Build repo root list using `--repos-config` when present.
- Otherwise merge `--workspace-roots` with the current repo.

Multi-repo metadata (e.g. `repo` field in index) should be used to:

- find specs across repos safely,
- understand cross-repo dependencies.

---
## 7) 1) Identify Target Spec/Tasks

Priority:

1. Use `--spec` / `--tasks` when provided.
2. If index exists and implementation supports it, select by spec ID.
3. Otherwise require explicit spec path.

Default tasks location:

- `tasks.md` next to `spec.md`.

Ambiguity handling:

- `strict` safety-mode: treat ambiguous resolution as **blocking** and report it.
- `dev` safety-mode: list candidates and proceed with lower-confidence checks.

---
## 8) 2) Read Inputs (Read-Only)

- Read `spec.md`.
- Read `tasks.md` when present.
- Detect `ui.json` when present.

Rules:

- Never rewrite spec/tasks/UI JSON in this workflow.
- This workflow is verification-only.

---
## 9) 3) Build Verification Checklist

Checklist dimensions:

1. **Task completion**  
   Are tasks marked complete **and** supported by evidence?

2. **Contract correctness**  
   Are APIs/models/events implemented per spec + registry?

3. **Test coverage**  
   Are tests present for critical paths and NFRs?

4. **NFR fulfillment**  
   Logging/metrics/tracing/security/rate limiting where required.

5. **Cross-SPEC alignment**  
   Are dependent specs reasonably in-sync?

6. **Cross-repo reuse correctness**  
   Is reuse vs duplication aligned with registries?

7. **UI compliance (if applicable)**  
   Is UI correctly aligned with UI JSON and UI component registry?

---
## 10) 4) Validate Dependency Readiness

If index is available:

- Cross-check declared dependencies of the target spec.
- Warn if:
  - a dependency spec is missing key artifacts (e.g. tests, tasks).  
  - tasks attempt to implement dependent features out-of-order.

In `strict` safety-mode:

- Treat major dependency ordering or missing-critical-artifact issues as **errors**.

---
## 11) 5) Registry Alignment Checks

If registries exist:

- Verify that names referenced in spec/tasks and (where inferable) code align with the merged registry view:
  - API names / route prefixes
  - model names
  - domain terms
  - critical cross-cutting sections
  - shared patterns
  - UI component names (when UI registry exists)

Cross-repo safeguard:

- If the same name appears in a supplemental registry with conflicting meaning:
  - mark as **ownership ambiguity**,
  - recommend governance reconciliation,
  - discourage local "new shared name" creation.

Under `strict` safety-mode + `mode=runtime` (if implemented):

- treat unresolved ownership ambiguity as **blocking**.

---
## 12) 6) Evidence-Based Progress Evaluation

Distinguish between:

- **Declared progress**: checklist/checkboxes, status markers.
- **Observed progress**: code/tests/config/evidence.

### 12.1 Task Status Signals

- Parse `tasks.md` status markers.
- Highlight:
  - completed tasks with weak/no evidence,
  - partially completed tasks,
  - blocked tasks,
  - missing tasks for obvious work items.

### 12.2 Code Structure Signals

Best-effort structural hints (implementation-dependent):

- module/service presence for major feature groups,
- API/controller endpoints for declared routes,
- data model definitions for declared models,
- shared utilities used where registry recommends reuse.

### 12.3 Test Signals

- unit tests for domain logic,
- integration/contract tests for key flows,
- performance tests when SLAs exist.

### 12.4 NFR Signals

When NFRs are present in spec:

- ensure evidence for logging/metrics/tracing,
- ensure security/rate-limiting/auditing where specified.

---
## 13) 7) UI JSON Addendum (v5.7)

Apply when any of:

- SPEC_INDEX category for spec is `ui`,
- `ui.json` exists in the spec folder,
- spec explicitly mentions Penpot/UI JSON.

UI rules:

- UI design source of truth is `ui.json`.
- `ui.json` is **design-owned** and must not contain business logic.

Metadata expectations (when present):

- `meta.source` (e.g. `ai`, `human`, `mixed`),
- `meta.generator`,
- `meta.generated_at`,
- `meta.design_system_version`,
- `meta.style_preset`,
- `meta.review_status` (`unreviewed`, `designer_approved`, `overridden`, ...).

Checks:

- UI implementation should align with `ui.json` structure and component naming.
- `tasks.md` should include items about:
  - mapping components to UI JSON definitions,
  - extracting business logic out of UI components.

If UI specs are active but `ui.json` is missing:

- treat as **high-visibility warning** (portfolio) or **error** (runtime+strict, if applied in CI).

Unreviewed AI-generated UI JSON for critical flows:

- should elevate risk level under `strict` safety-mode.

---
## 14) 8) Report Schema (Suggested)

Suggested report fields:

- spec ID/title/path
- tasks path
- index path used (or NONE)
- primary registry dir
- supplemental registry roots
- multi-repo roots / repos-config summary
- declared vs observed completion summary
- dependency readiness
- registry alignment status
- UI compliance status
- risk level: `LOW | MEDIUM | HIGH | CRITICAL`
- recommended next tasks

When `--report-format=json` is supported, use a JSON structure mirroring these fields.

---
## 15) 9) Recommended Follow-Ups

- `/smartspec_fix_errors`
- `/smartspec_generate_tests`
- `/smartspec_refactor_code`
- `/smartspec_sync_spec_tasks`
- `/smartspec_global_registry_audit` (for large naming drift)
- `/smartspec_validate_index`

---
## 16) Weakness & Risk Check (v5.7.0)

Before treating this workflow spec as stable:

1. Confirm it never mutates spec/tasks/registries/UI JSON.
2. Confirm `.spec/` is treated as canonical for index & registry.
3. Confirm safety-mode gates high-risk ambiguity (especially cross-repo naming and missing index/registries).
4. Confirm UI JSON is always design-owned and logic-free.
5. Confirm reports clearly distinguish declared vs observed progress.
6. Confirm multi-repo and multi-registry behavior matches other v5.7 workflows.

---
## 17) Legacy Flags Inventory

**Kept (legacy):**

- `--index`
- `--specindex`
- `--registry-dir`
- `--registry-roots`
- `--workspace-roots`
- `--repos-config`
- `--spec`
- `--tasks`
- `--report-dir`
- `--report`
- `--safety-mode`
- `--strict`
- `--dry-run`

**Additive (v5.7 suggestion, optional to implement):**

- `--report-format`

No legacy behavior is removed or weakened.

