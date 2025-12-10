---
name: /smartspec_fix_errors
version: 5.7.0
role: fix/governance
write_guard: ALLOW-WRITE
purpose: Analyze implementation errors (build/test/integration/UI) and propose or apply fixes aligned with SmartSpec v5.6–v5.7 centralized governance (multi-repo, multi-registry, UI JSON, anti-duplication).
version_notes:
  - v5.2: initial error-fix workflow with SmartSpec centralization
  - v5.7.0: governance alignment with v5.6–v5.7 (multi-repo, multi-registry, safety-mode); behavior remains backward-compatible; additive-only writes
---

# /smartspec_fix_errors

Analyze implementation errors (build failures, test failures, runtime errors, integration issues) and propose or apply fixes aligned with the canonical SmartSpec knowledge layer.

This workflow enforces SmartSpec centralization:
- `.spec/` is the canonical project space for shared truth.
- `.spec/SPEC_INDEX.json` is the canonical index.
- `.spec/registry/` is the source of shared definitions.
- `.smartspec/` is tooling-only.
- UI specs use `ui.json` as the design source of truth for JSON-first / Penpot integrations.

> **Write guard & scope (v5.7.0 clarification)**
> - Role: **fix/governance**.
> - Modes:
>   - `recommend`: NO-WRITE (analysis + plan only).
>   - `additive-meta`: ALLOW-WRITE for **additive metadata only** in central files if the implementation supports it (never destructive).
> - This workflow MUST NOT directly edit business logic, tests, or UI components; it only edits governance/metadata where allowed.

---

## 1) What It Does

- Resolves canonical SPEC_INDEX.
- Loads shared registries (primary + supplemental) in a merged view.
- Identifies relevant spec(s) for the error context.
- Cross-checks expected behavior against `spec.md` and `tasks.md`.
- Classifies errors and detects root causes:
  - implementation defects
  - cross-SPEC naming drift
  - contract mismatches
  - missing dependencies
  - incorrect test assumptions
  - UI JSON vs component misalignment
- Produces a **safe, spec-aligned fix plan** with optional additive metadata updates.

---

## 2) When to Use

- CI failures after implementing a SPEC.
- Local build/test failures.
- Integration regressions across multiple specs.
- UI mismatches between design and runtime components.
- After large refactors or dependency updates.

Not for:
- designing new specs (use `/smartspec_generate_spec`).
- broad refactor planning (use `/smartspec_refactor_code`).

---

## 3) Inputs

- Error logs or failure summaries (e.g., test output, stack traces).
- Target spec path (recommended) and/or failing file paths.

Expected adjacent files:
- `spec.md`
- `tasks.md` (if present)
- `ui.json` (for UI specs)

Optional governance inputs:
- `.spec/SPEC_INDEX.json`
- `.spec/registry/*.json`
- supplemental registries from sibling repos (via `--registry-roots`).

---

## 4) Outputs

- A structured **fix report**, including:
  - error summary
  - root-cause hypothesis
  - evidence from spec/tasks/index/registries
  - proposed fixes
  - risk level
  - registry/contract alignment notes
  - UI JSON compliance notes (if applicable)
- Optional **additive metadata changes** (e.g., tagging tests or specs) when in `additive-meta` mode and allowed by the host implementation.

Reports SHOULD be written under:
- `.spec/reports/smartspec_fix_errors/`

---

## 5) Flags

### 5.1 Index / Registry (v5.7-aligned)

- `--index`  
  Path to SPEC_INDEX (optional). Default: auto-detect via canonical order.

- `--specindex`  
  Legacy alias for `--index`.

- `--registry-dir`  
  Primary registry directory (optional). Default: `.spec/registry`.

- `--registry-roots`  
  Supplemental registry dirs, semicolon- or comma-separated (optional).  
  All supplemental registries are **read-only** and used to detect cross-repo duplicate naming / ownership ambiguity.

### 5.2 Multi-Repo (v5.7)

- `--workspace-roots`  
  Semicolon- or comma-separated repo roots to search (optional).

- `--repos-config`  
  Path to structured repo config (optional).  
  Takes precedence over `--workspace-roots`. Recommended value: `.spec/smartspec.repos.json`.

### 5.3 Target Selection

- `--spec`  
  Explicit spec path (optional).

- `--tasks`  
  Explicit tasks path (optional).

- `--error-log`  
  Path(s) or glob(s) to error logs (optional; else errors supplied via stdin / prompt).

### 5.4 Mode & Safety

- `--mode`  
  `recommend` | `additive-meta` (default: `recommend`).

- `--safety-mode`  
  `strict` | `dev` (default: `strict`).

- `--strict`  
  Legacy alias for `--safety-mode=strict`.

- `--dry-run`  
  Simulate any additive changes without writing files; still produce report.

### 5.5 Output

- `--report-dir`  
  Output report directory (optional). Default: `.spec/reports/smartspec_fix_errors/`.

- `--report-format`  
  `md` | `json` (default: `md`).

---

## 6) 0) Resolve Canonical Index & Registry

### 6.1 SPEC_INDEX (Single Source of Truth)

Detection order:

1. `.spec/SPEC_INDEX.json` (canonical)
2. `SPEC_INDEX.json` (legacy root mirror)
3. `.smartspec/SPEC_INDEX.json` (deprecated)
4. `specs/SPEC_INDEX.json` (older layout)

If none found:
- continue with local context only; record the gap in the report.
- under `--safety-mode=strict`, downgrade confidence and highlight as a governance issue.

### 6.2 Registry View

1. Load primary registry from `--registry-dir`.
2. If provided, load `--registry-roots` as read-only.

Rules:
- primary registry entries are canonical.
- supplemental registries detect cross-repo naming collisions and ownership ambiguity.

---

## 7) 1) Identify Target Spec(s)

Priority:

1. Use `--spec` / `--tasks` if provided.
2. If SPEC_INDEX exists, attempt to select spec by ID matching failing areas.
3. Otherwise, infer candidate spec(s) from file paths of failing tests/code.

Default tasks location:
- `tasks.md` alongside `spec.md`.

Ambiguous mapping:
- under `dev` safety-mode: list multiple candidate specs with rationale.
- under `strict` safety-mode: stop and report ambiguity as a blocking issue.

---

## 8) 2) Read Spec + Tasks (Read-Only)

- Read `spec.md`.
- Read `tasks.md` when present.
- Extract from spec/tasks:
  - expected APIs and endpoints
  - model definitions and contracts
  - NFRs and performance constraints
  - security requirements
  - UI rules for visual/behavioral expectations

No modifications are made to these files in this workflow.

---

## 9) 3) Error Classification

Classify each error into one or more buckets:

1. **Build/Type Errors**
2. **Unit Test Failures**
3. **Integration/Contract Failures**
4. **Performance Regression**
5. **Security Enforcement Gaps**
6. **UI/Component Mismatch**
7. **Cross-SPEC Naming Drift**
8. **Environment/Config Mismatch** (v5.7 addition)

Classification is used to choose appropriate fix strategies.

---

## 10) 4) Cross-SPEC Consistency Gate

If SPEC_INDEX exists:
- confirm that dependent specs are present and properly implemented.
- detect if an upstream spec changed shared contracts without coordinated updates.

If registries exist:
- compare:
  - endpoints referenced in failing tests/code
  - model names
  - domain terms
  - critical event names

If mismatch is detected:
- under `--safety-mode=strict` / `--strict`:
  - treat as a blocking inconsistency; recommend cross-spec reconciliation.
- under `dev` safety-mode:
  - propose a fix plan and mark risk as high.

Supplemental registries:
- use them to spot external/other-repo owners of APIs/models/terms.
- discourage local re-definitions for externally owned concepts.

---

## 11) 5) Fix Strategy by Error Type

### 11.1 Build/Type Errors

- Align types/interfaces with canonical models from `data-model-registry.json`.
- If local types diverged:
  - update the implementation to match registry.
  - only recommend registry additions when new shared types are clearly required and not duplicates.

### 11.2 Unit Test Failures

- Confirm each test expectation maps to a spec requirement.
- If a test asserts behavior not described in spec:
  - either mark test as suspect, or
  - propose adding explicit spec coverage, not silently changing implementation.

### 11.3 Integration/Contract Failures

- Ensure API routes and semantics match `api-registry.json`.
- Validate request/response shapes.
- If two specs disagree on contract:
  - propose a reconciliation plan (versioning, compatibility layer).

### 11.4 Performance Regression

- Compare measured metrics to spec SLAs.
- Recommend targeted optimizations aligned with architectural patterns.
- Never relax SLAs without explicit spec changes.

### 11.5 Security Enforcement Gaps

- Verify that auth/authz checks exist at appropriate layers.
- Check that security rules align with security/core specs.
- Recommend non-invasive fixes (e.g., middleware/hooks) over ad hoc checks.

### 11.6 UI/Component Mismatch

- If `ui.json` exists:
  - ensure component IDs/names match UI JSON and `ui-component-registry.json`.
  - prefer adjusting runtime code to align with design.
- If design vs runtime diverge drastically:
  - suggest explicit designer-engineer reconciliation.

### 11.7 Cross-SPEC Naming Drift

- Prefer converging on the canonical registry term.
- If migration needed:
  - design a phased plan (dual support, deprecations).
  - recommend using `/smartspec_sync_spec_tasks --mode=additive` to propagate tasks.

### 11.8 Env/Config Mismatch (v5.7)

- When failures only occur in certain environments:
  - check config vs spec assumptions.
  - propose environment-specific config updates rather than code-only fixes.

---

## 12) 6) UI JSON Addendum (Conditional)

Apply when:
- spec category is `ui`, or
- `ui.json` exists.

Rules:
- `ui.json` is design-owned and declarative.
- UI JSON must not contain business logic.
- Business logic should live in services/hooks/domain layers.

When fixing errors:
- do NOT move logic into UI JSON.
- if UI JSON and code disagree:
  - treat UI JSON as primary design intent, but confirm with designers when large changes are implied.

For v5.7, when `ui.json` includes `meta`:
- treat fields like `source`, `generator`, `generated_at`, `design_system_version`, `style_preset`, `review_status` as signals of:
  - AI vs human origin
  - review status
  - design-system version alignment

Unreviewed AI-generated UI JSON for critical flows:
- should raise risk level, especially under `--safety-mode=strict`.

---

## 13) 7) Mode Behavior

### 13.1 `recommend` (default)

- Produce a fix plan only.
- Output registry/index recommendations as **suggestions**, not changes.
- NEVER write to central files.

### 13.2 `additive-meta`

- May propose and, if host implementation allows, apply **additive** metadata updates, such as:
  - tagging specs with error-related metadata
  - adding links to incident/bug IDs
  - adding non-breaking annotations in registries.

- MUST NOT:
  - delete or rename registry entries automatically.
  - alter core `spec.md` behavior descriptions.
  - change UI JSON beyond metadata, and only if explicitly allowed.

`--dry-run`:
- simulate `additive-meta` writes but only emit the report, no file changes.

`--safety-mode=strict`:
- prefer recommendations and require human confirmation even for additive metadata.

---

## 14) 8) Output Fix Report

The report SHOULD include:

- error classification summary
- mapped spec(s) and tasks
- evidence from index/registries
- fix strategies per error class
- risks: `LOW | MEDIUM | HIGH | CRITICAL`
- notes on:
  - cross-SPEC impacts
  - registry alignment
  - UI JSON / design alignment
  - environment/config sensitivity

When `--report-format=json`, the JSON schema should mirror these fields to support automation.

---

## 15) 9) Recommended Follow-ups

- `/smartspec_verify_tasks_progress`
- `/smartspec_generate_tests`
- `/smartspec_refactor_code`
- `/smartspec_sync_spec_tasks --mode=additive`
- `/smartspec_release_readiness` (for pre-release checks)

---

## 16) Weakness & Risk Check (v5.7.0)

Before treating this workflow as stable in a repo, validate that:

1. It never introduces destructive changes to registry/spec/index/UI JSON.
2. It respects `.spec/` as canonical and uses mirrors only for compatibility.
3. It clearly differentiates between `recommend` and `additive-meta` modes.
4. It uses `--safety-mode` and `--strict` to gate risky operations.
5. It handles multi-repo and multi-registry correctly (no local forks of external concepts).
6. It treats AI-generated UI JSON as higher risk when unreviewed.
7. It logs ambiguity and high-risk findings in the report instead of guessing.

---

## 17) Legacy Flags Inventory

- **Kept (legacy):**
  - `--index`
  - `--registry-dir`
  - `--spec`
  - `--tasks`
  - `--mode`
  - `--strict` (alias for `--safety-mode=strict`)

- **New additive (v5.7.0):**
  - `--specindex` (alias)
  - `--registry-roots`
  - `--workspace-roots`
  - `--repos-config`
  - `--safety-mode`
  - `--dry-run`
  - `--report-dir`
  - `--report-format`

No legacy flags are removed or repurposed.

