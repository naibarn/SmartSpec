---
name: /smartspec_ci_quality_gate
version: 5.7.0
role: quality/governance
write_guard: NO-WRITE
purpose: Generate CI quality gates and a unified CI plan from SmartSpec (specs, tasks, registries, SPEC_INDEX) under SmartSpec v5.7 governance (multi-repo, multi-registry, safety‑mode, UI metadata signals, chain-readiness). This workflow is **read‑only** and does **not modify CI YAML**.
version_notes:
  - v5.6.2: baseline CI matrix + unified gate generator
  - v5.7.0: governance alignment; multi-repo/registry parity; stricter safety‑mode; UI JSON metadata; baseline CI dimensions; chain-readiness; fully backward‑compatible
---

# /smartspec_ci_quality_gate (v5.7.0)

This workflow derives a **CI plan** + **quality gates** from SmartSpec artifacts, ensuring CI systems (GitHub Actions, GitLab CI, Azure Pipelines, CircleCI, etc.) enforce the correct test categories, contract checks, coverage gates, and shared‑asset governance.

It is a **pure analysis workflow**:
- NO writes to CI config
- NO edits to code/specs/tasks/registries
- Writes **only** CI plan files under `.spec/ci/`

All v5.6.2 behavior is retained.

---
## 1) Responsibilities
- Load SPEC_INDEX, specs, tasks, registries
- Resolve multi‑repo + multi‑registry topology
- Detect spec types → derive baseline CI dimensions
- Map spec tasks to CI requirements
- Identify shared assets requiring contract tests
- Evaluate current CI configs (optional, read‑only)
- Generate a CI matrix + required/proposed checks
- Output CI plan in md/json/yaml (per flags)

---
## 2) When to Use
- After generating tests
- Before modifying CI pipelines
- Before release readiness
- To standardize CI quality gates across repos/services

---
## 3) Inputs
### 3.1 Artifacts (read‑only)
- SPEC_INDEX (canonical detection order)
- specs + tasks
- primary + supplemental registries
- optional UI JSON metadata
- optional CI configuration files
- optional test reports

### 3.2 Flags (see §5)
### 3.3 Outputs
- `.spec/ci/ci_quality_gate_<label>.{md|json|yaml}`
- optional stdout summary

---
## 4) Modes
- `NO-WRITE` enforced
- `--kilocode` → Ask/Architect + Orchestrator-per-dimension (read‑only)
- `--nosubtasks` disables subtask decomposition

---
## 5) Flags
### 5.1 Scope & Label
- `--spec-ids=<csv>`
- `--include-dependencies`
- `--ci-label=<string>` (required for output naming)

### 5.2 CI System
- `--ci-system=<github_actions|gitlab_ci|azure_pipelines|circleci|generic>`
- `--target-envs=<csv>`
- `--ci-config-paths=<glob>` (read‑only)
- `--test-report-paths=<glob>` (read‑only)

### 5.3 Multi-repo / Registry / Index
- `--workspace-roots=<csv>`
- `--repos-config=<path>` (preferred)
- `--registry-dir=<path>`
- `--registry-roots=<csv>` (read‑only supplements)
- `--index=<path>` / `--specindex=<legacy>`

### 5.4 Safety Mode
- `--safety-mode=<normal|strict>`
- `--strict` alias for `--safety-mode=strict`

### 5.5 Output
- `--ci-output-format=<md|json|yaml>` (default md)
- `--ci-output-dir=<path>` (default `.spec/ci/`)
- `--stdout-summary`

---
## 6) Canonical Detection (v5.7 rules)
### 6.1 SPEC_INDEX
1. `.spec/SPEC_INDEX.json`
2. `SPEC_INDEX.json`
3. `.smartspec/SPEC_INDEX.json`
4. `specs/SPEC_INDEX.json`

### 6.2 Registries
- primary: `.spec/registry/`
- supplemental: `--registry-roots` (read‑only)
- precedence: primary > supplemental

### 6.3 Multi-repo Roots
- prefer repos-config → structured mapping
- fallback to workspace-roots + current repo
- validate index `repo:` fields

---
## 7) Spec Scope Resolution
Use:
1. explicit `--spec-ids`
2. expand via `--include-dependencies` (registry + index)

No guessing missing IDs; raise clarity warnings.

---
## 8) Determine Spec Types & Baseline CI Dimensions
Per spec type:
- **API/service** → lint, unit, integration, contract, coverage
- **Shared model/library** → lint, unit, contract
- **Infra/ops** → config lint, schema checks
- **UI** → UI validation + UI tests (JSON-first vs inline rules)

Under strict mode:
- missing baseline dimensions → REQUIRED gates

---
## 9) Derive CI Requirements
From:
- spec tasks
- registry ownership (APIs/models/UI components)
- dependencies
- UI JSON metadata
- optional CI/test artifacts

Produce per-spec requirements:
- static analysis
- unit tests
- integration tests
- contract tests for shared assets
- coverage thresholds
- perf/security checks when tasks indicate
- UI checks (per UI governance mode)

---
## 10) Map to Existing CI Configs (Optional)
- inspect CI configs via `--ci-config-paths`
- identify unmapped CI jobs
- do not guess via fuzzy matching; list unmapped jobs

---
## 11) Safety Mode Application
- **normal** → missing checks = recommendations
- **strict** → missing baseline or critical checks = required gates

Critical examples:
- shared API changes without contract tests
- coverage below project policy
- missing UI validation under JSON-first policy

---
## 12) CI Matrix Construction
Dimensions:
- per spec-id
- per repo/service
- per target-env (`--target-envs`)

Sections in output:
- **Required checks**
- **Proposed checks**
- CI-system-specific suggestions
- unmapped CI jobs
- governance risks

---
## 13) Output Files
Write to:
- `.spec/ci/ci_quality_gate_<label>.md`
- Optionally `.json` or `.yaml` per `--ci-output-format`

Content:
- CI matrix
- required/proposed checks
- registry/ownership rationale
- UI governance
- baseline CI dimensions
- safety‑mode impacts
- summary + next steps

---
## 14) UI Addendum (v5.7)
For UI specs:
- detect UI mode (JSON-first vs inline)
- JSON-first → require UI JSON validation + UI snapshot tests
- inline UI → UI flow tests recommended
- respect project-level UI JSON opt-out
- use UI JSON metadata:
  - `source`, `generator`, `generated_at`
  - `design_system_version`, `style_preset`, `review_status`

Strict mode:
- missing required UI gates → blocking CI requirements

---
## 15) Governance & Risk Checks
Ensure:
- no write to CI configs
- no modification of spec/tasks/registries
- no invented spec IDs or derived jobs
- all shared-asset CI requirements align with registries
- missing registry entries produce warnings, not guesses
- CI plan aligns with release-readiness evidence types

---
## 16) Recommended Follow-Ups
- `/smartspec_release_readiness`
- `/smartspec_generate_tests`
- `/smartspec_verify_tasks_progress`
- `/smartspec_global_registry_audit`
- `/smartspec_validate_index`

---
## 17) Legacy Flags Inventory
Kept:
- `--strict` (alias)

Additive flags preserved from v5.6.2 → v5.7:
- all scope/CI/multi‑repo/registry/output/safety flags

No legacy behavior removed.

