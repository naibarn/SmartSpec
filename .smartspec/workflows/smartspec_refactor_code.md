---
name: /smartspec_refactor_code
version: 5.7.0
role: refactor/governance
write_guard: NO-WRITE
purpose: Provide a safe, governance‑aligned refactor workflow under SmartSpec v5.6–v5.7 (multi‑repo, multi‑registry, UI JSON governance, anti‑duplication).
version_notes:
  - v5.2: initial refactor workflow
  - v5.7.0: governance alignment update (documentation‑only, no breaking behavior)
---

# /smartspec_refactor_code

Refactor existing code while preserving behavioral correctness and maintaining alignment with SmartSpec centralized governance.

This workflow ensures:
- `.spec/` is the canonical project‑owned source of truth.
- `.spec/SPEC_INDEX.json` is the primary index.
- `.spec/registry/` holds all shared definitions.
- `.smartspec/` is tooling‑only.
- UI specs rely on `ui.json` for design‑owned declarative structure.
- Multi‑repo + multi‑registry rules (v5.6–v5.7) are applied.

---
## What It Does
- Resolves canonical index + registry hierarchy.
- Applies multi‑repo mapping + supplemental registries.
- Identifies refactor surface for the target spec.
- Validates contract stability against registries.
- Generates safe refactor plan.
- Highlights ambiguous or risky changes.
- Ensures separation of UI logic via UI JSON addendum.
- Enforces anti‑duplication rules for APIs/models/terms.

---
## When to Use
- Reduce technical debt after stabilization.
- Consolidate patterns across specs.
- Correct architectural drift.
- Prepare for major release.
- Extract UI logic into service/domain layers.

---
## Inputs
- Codebase
- Optional: `--spec`, `--scope`, performance/error reports

Expected adjacent files:
- `spec.md`
- `tasks.md`
- `ui.json` (if UI spec)

---
## Outputs
- Refactor plan
- Change recommendations
- Test update guidance
- Registry/index update suggestions (non‑destructive)
- Risk report

---
## Flags
### Index & Registry
- `--index`
- `--registry-dir` (default `.spec/registry`)
- `--registry-roots` supplemental read‑only registries

### Multi‑Repo
- `--workspace-roots`
- `--repos-config` (preferred)

### Refactor Control
- `--spec`
- `--scope`
- `--mode= recommend | safe-apply` (default: recommend)
- `--dry-run`
- `--safety-mode=<strict|dev>`
- `--strict` alias for `--safety-mode=strict`

---
## 0) Resolve Canonical Index & Registry
### 0.1 SPEC_INDEX detection order
1. `.spec/SPEC_INDEX.json` (canonical)
2. `SPEC_INDEX.json` (root mirror)
3. `.smartspec/SPEC_INDEX.json` (deprecated)
4. `specs/SPEC_INDEX.json` (older layout)

### 0.2 Registry hierarchy
- Primary registry: `--registry-dir`
- Supplemental registries: `--registry-roots` (read‑only)
- Detect cross‑repo name collisions + ownership ambiguity.

### 0.3 Multi‑repo resolution
- Prefer `--repos-config`
- Else build roots from `--workspace-roots` + current repo
- Never write into sibling repos unless governance explicitly allows

---
## 1) Identify Target Spec & Surface
Priority:
1. `--spec`
2. SPEC_INDEX mapping
3. Path inference

Refactor surface types:
- API / controllers
- Domain models
- Services & use cases
- Infra layers
- Shared libs
- UI components
- Tests

---
## 2) Read Inputs (Read‑Only)
Extract from `spec.md`, `tasks.md`:
- public contracts
- cross‑spec dependencies
- NFRs
- security requirements
- patterns

If UI spec exists:
- detect `ui.json`
- load UI metadata (v5.7 rules)

---
## 3) Cross‑SPEC Safety Gate
If index exists:
- ensure dependencies remain stable
- detect refactor actions that break contract surfaces

If registry exists:
- ensure no new API/model/term conflicts

Strict mode:
- stop when rename risk or cross‑repo ambiguity is detected

---
## 4) Refactor Rules
### 4.1 Always Safe
- extract duplicated logic
- improve readability
- reduce complexity
- add missing tests
- non‑breaking performance tuning

### 4.2 Safe With Care
- internal renames
- file moves with import corrections

### 4.3 Requires Migration Plan
- public API signature changes
- shared model modifications
- new shared terms

Migration plan includes:
- compatibility layer
- deprecation period
- registry update recommendation

---
## 5) Pattern Alignment
Use:
- `patterns-registry.json`
- cross‑spec utilities
- canonical error/logging/caching patterns

If repeated patterns detected:
- recommend adding a new pattern to registry (non‑destructive)

---
## 6) UI JSON Addendum
Apply when spec is UI or `ui.json` exists.

Rules:
- UI JSON is design‑owned and declarative
- No business logic allowed
- UI code refactors must:
  - remove embedded business logic
  - extract logic into hooks/services/domain
  - keep UI tests focused on render/state
  - avoid creating new shared component names unless recommended

If UI JSON missing but UI detected:
- recommend creating `ui.json`

v5.7 metadata expectation:
- `source`, `generator`, `generated_at`
- `design_system_version`
- `style_preset`
- `review_status`

---
## 7) Test Alignment
Before refactor:
- snapshot critical behavior

During refactor:
- update unit + integration tests

After refactor:
- revalidate:
  - contract tests
  - performance SLAs
  - UI tests (if applicable)

---
## 8) Mode Behavior
### recommend (default)
- produce plan only
- never modify files

### safe-apply
Allowed only when:
- no registry conflicts
- no dependency breakage
- UI JSON governance satisfied

Never auto‑modify:
- shared API/model names
- registry files
- `ui.json`

---
## 9) Output Report
Includes:
- refactor scope
- dependencies
- registry alignment
- proposed steps
- risks
- test plan
- UI JSON notes

---
## 10) Follow‑ups
- `/smartspec_generate_tests`
- `/smartspec_verify_tasks_progress`
- `/smartspec_sync_spec_tasks --mode=additive`
- `/smartspec_reindex_specs`

---
## 11) Legacy Flags Inventory
**Kept:**
- `--index`, `--registry-dir`, `--spec`, `--scope`, `--mode`, `--strict`

**Additive (v5.7):**
- `--registry-roots`
- `--workspace-roots`
- `--repos-config`
- `--safety-mode`
- `--dry-run`

No legacy behavior removed.

