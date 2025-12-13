---
name: /smartspec_generate_tests
version: 5.7.0
role: test-generation/governance
write_guard: NO-WRITE
purpose: Generate a SmartSpec-governed test plan (and optional scaffolding guidance) aligned with v5.6–v5.7 rules: multi-repo, multi-registry, UI JSON governance, anti-duplication.
version_notes:
  - v5.2: initial test-generation workflow
  - v5.7.0: governance alignment; additive documentation update; no breaking behavior
---

# /smartspec_generate_tests

Generate a comprehensive **test plan** from `spec.md`, `tasks.md`, registries, SPEC_INDEX, and UI JSON, following SmartSpec centralized governance.

Enforces:
- `.spec/` is canonical project-owned truth.
- `.spec/SPEC_INDEX.json` is the primary index.
- `.spec/registry/` holds authoritative shared definitions.
- UI JSON is design-owned; business logic must not appear there.
- Multi-repo + multi-registry detection.
- Anti-duplication for APIs/models/terms.

---
## 1) What It Does
- Resolves canonical SPEC_INDEX.
- Loads primary + supplemental registries.
- Reads `spec.md`, `tasks.md`, optional `ui.json`.
- Builds a full **test matrix**:
  - unit tests
  - integration tests
  - API/contract tests
  - security tests
  - performance/SLA tests
  - observability tests
  - UI/component tests (when applicable)
- Ensures registry alignment for all referenced names.
- Applies UI JSON addendum rules.

---
## 2) When to Use
- After tasks generation, before implementation.
- When expanding test coverage.
- During refactors or release preparation.

---
## 3) Inputs
- `--spec` path (recommended)
- Expected adjacent files:
  - `tasks.md`
  - `ui.json` (if UI spec)
- Governance inputs:
  - `.spec/SPEC_INDEX.json`
  - `.spec/registry/*.json`
  - supplemental registries via `--registry-roots`

---
## 4) Outputs
- Test plan file (default: `tests.md` next to spec)
- Optional scaffolding suggestions
- Cross-SPEC alignment notes
- UI JSON compliance notes

---
## 5) Flags
### Index & Registry
- `--index` (alias: `--specindex`)
- `--registry-dir` (default `.spec/registry`)
- `--registry-roots` (read-only supplemental registries)

### Multi-Repo
- `--workspace-roots`
- `--repos-config` (preferred)

### Target Selection
- `--spec`
- `--tasks`

### Output
- `--output=<path>`
- `--report-format=md|json` (for optional summary)
- `--dry-run`
- `--safety-mode=<strict|dev>` (default: strict)
- `--strict` alias

---
## 6) Canonical Index & Registry Resolution
Detection order for SPEC_INDEX:
1. `.spec/SPEC_INDEX.json`
2. `SPEC_INDEX.json` (root mirror)
3. `.smartspec/SPEC_INDEX.json` (deprecated)
4. `specs/SPEC_INDEX.json` (legacy)

Registry rules:
- primary registry = authoritative
- supplemental registries = read-only; detect collisions + ownership ambiguity

Multi-repo:
- prefer `--repos-config`
- else derive from `--workspace-roots`

---
## 7) Identify Target Spec & Tasks
Priority:
1. Use explicit flags
2. SPEC_INDEX mapping
3. Require user selection when ambiguous

Default tasks path: `tasks.md` next to `spec.md`.

---
## 8) Read Inputs (Read-Only)
Extract from spec:
- behaviors
- contracts (API, models, events)
- dependencies
- NFRs (performance, security)
- UI description

Extract from tasks:
- task-level verifiable actions

If `ui.json` exists:
- load metadata and component map

---
## 9) Cross-SPEC Alignment Gate
- Ensure tests do not contradict dependency specs.
- Validate names against registry entries.
- Strict mode: block naming drift.
- Supplemental registries: detect external ownership.

---
## 10) Build Test Matrix (Core)
### 10.1 Unit Tests
- domain logic
- data transformations
- validation rules

### 10.2 Integration Tests
- service orchestration
- db/repo calls
- event/message flows

### 10.3 API / Contract Tests
- request/response structure
- status codes
- backward compatibility

### 10.4 Security Tests
- auth/authz
- rate-limiting
- audit logging

### 10.5 Performance / SLA Tests
- latency/throughput targets
- p95/p99 metrics
- baseline loads

### 10.6 Observability Tests
- logs for critical flows
- metrics emitted
- tracing continuity

### 10.7 UI / Component Tests
Applied when UI spec or `ui.json` exists.
- rendering and state
- accessibility
- component ID mapping to UI JSON
- avoid testing business logic in UI

---
## 11) UI JSON Addendum
- UI JSON is design-owned
- Metadata expectations (v5.7):
  - `source`, `generator`, `generated_at`
  - `design_system_version`
  - `style_preset`
  - `review_status`
- Tests should ensure runtime UI components match UI JSON definitions
- Do not enforce logic inside UI JSON

---
## 12) Generate Test Plan Document
Recommended sections:
1. Scope
2. Assumptions
3. Dependencies
4. Test Matrix (full table)
5. Fixtures
6. Tooling
7. Risks & gaps
8. Registry alignment notes
9. UI JSON compliance notes

Output:
- default: `tests.md`
- or user-defined via `--output`
- `--dry-run`: print only

---
## 13) Quality Gates
- full coverage of major spec sections
- high-risk tasks have explicit tests
- all shared names align with canonical registries
- UI tests cleanly separate presentation vs logic

---
## 14) Recommended Follow-ups
- `/smartspec_verify_tasks_progress`
- `/smartspec_implement_tasks`
- `/smartspec_sync_spec_tasks --mode=additive`
- `/smartspec_release_readiness`

---
## 15) Legacy Flags Inventory
**Kept:**
- `--index`, `--registry-dir`, `--spec`, `--tasks`, `--output`, `--dry-run`, `--strict`

**Additive (v5.7):**
- `--specindex`
- `--registry-roots`
- `--workspace-roots`
- `--repos-config`
- `--safety-mode`
- `--report-format`

No legacy behavior removed.

