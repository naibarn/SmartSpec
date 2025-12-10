---
name: /smartspec_portfolio_planner
version: 5.7.0
role: portfolio/governance
write_guard: NO-WRITE
purpose: Plan and prioritize a SmartSpec portfolio using full v5.6–v5.7 governance (multi-repo, multi-registry, UI JSON signals, safety-mode, chain-readiness).
version_notes:
  - v5.2: initial portfolio planner
  - v5.6: multi-repo + multi-registry baseline
  - v5.7.0: governance alignment (UI JSON signals, stricter cross-repo safety, chain-readiness v5.7); backward-compatible; documentation-only update
---

# /smartspec_portfolio_planner (v5.7.0)

Generate a **portfolio-level roadmap** and governance-aware prioritization across many SmartSpec specs. Applies full SmartSpec v5.7 rules:
- canonical index resolution
- merged primary + supplemental registry view
- multi-repo mapping
- conflict/duplication detection
- UI JSON governance signals
- safety-mode gating
- chain readiness for `/smartspec_generate_spec` + `/smartspec_generate_tasks` v5.7

---
## 1) Core Governance Principles
- `.spec/` = canonical governance space
- `.spec/SPEC_INDEX.json` = canonical index
- `.spec/registry/` = primary naming source
- root `SPEC_INDEX.json` = legacy mirror
- `.smartspec/` = tooling-only

---
## 2) Responsibilities
- Load complete portfolio scope via SPEC_INDEX
- Build dependency DAG
- Detect cycles + external dependencies
- Perform registry gap/duplication analysis
- Detect cross-repo ownership ambiguity
- Provide portfolio-level sequencing + governance notes
- Output roadmap + audit report

---
## 3) Inputs
- SPEC_INDEX
- primary registry directory
- supplemental registries (`--registry-roots`)
- multi-repo configuration (`--repos-config` preferred)
- spec files
- optional UI JSON metadata for UI consistency

---
## 4) Outputs
- roadmap + sequencing report
- dependency DAG summary
- cross-repo risk list
- registry gap analysis
- UI JSON governance indicators
- output location:
  - `.spec/reports/portfolio-planner/`

---
## 5) Flags
### 5.1 Mode (legacy semantics retained)
```
--mode=<portfolio|runtime>
```
- `portfolio` (default): broad program-level governance
- `runtime`: CI-style strict validation

### 5.2 Safety (v5.7)
```
--safety-mode=<strict|dev>
--strict
```
- strict = escalate cross-repo collisions
- dev = allow warnings

### 5.3 Index
```
--index=<path>
--specindex=<path>   # legacy alias
```

### 5.4 Registries
```
--registry-dir=<dir>
--registry-roots=<csv>
```

### 5.5 Multi-repo
```
--workspace-roots=<csv>
--repos-config=<path>
```
`--repos-config` = preferred

### 5.6 Scope Selection
```
--categories=<csv>
--spec-ids=<csv>
--include-drafts=<true|false>
```

### 5.7 Output
```
--output=<path>
--report=<summary|detailed>
--dry-run
```

---
## 6) Canonical Context Resolution
### 6.1 SPEC_INDEX detection order
1. `.spec/SPEC_INDEX.json`
2. `SPEC_INDEX.json`
3. `.smartspec/SPEC_INDEX.json`
4. `specs/SPEC_INDEX.json`

### 6.2 Registry View
- load primary registry
- load supplemental registries read-only
- precedence = primary > supplemental

### 6.3 Multi-repo Roots
- use `--repos-config` when provided
- else combine `--workspace-roots` + current repo
- validate repo mapping against index

---
## 7) Load Portfolio Scope
If index exists:
- filter by categories/spec-ids if provided
Else:
- scan `specs/` roots
- recommend running `/smartspec_reindex_specs`

---
## 8) Dependency Graph & Sequencing
- build full dependency DAG
- detect cycles
- detect unresolved dependencies
- treat missing external repos as ownership ambiguity

Strict mode:
- unresolved dependencies = blocking

---
## 9) Registry Gap + Duplication Analysis (v5.7)
Identify:
- shared names missing in primary registry
- names only in supplemental registries → likely external owners
- same-name/different-meaning conflicts
- same-meaning/different-name duplicates

Strict mode:
- collisions = blocking

dev mode:
- collisions downgraded to warnings

---
## 10) UI JSON Governance (when UI specs exist)
Check UI JSON metadata:
- `source`, `generator`, `generated_at`
- `design_system_version`, `style_preset`, `review_status`

Check alignment with UI component registry when present.

Missing UI JSON for UI specs:
- runtime → blocking
- portfolio → warning

---
## 11) Roadmap Generation
Plan phases:
- foundation work
- shared model/API migration steps
- dependency-driven milestones
- cross-team sequencing

Add governance overlays:
- ownership ambiguity hotspots
- registry gap priorities
- UI consistency actions

---
## 12) Report Structure
- index used
- multi-repo roots
- registry dirs
- portfolio scope summary
- dependency DAG
- registry gap results
- cross-repo risks
- UI JSON governance signals
- chain readiness for:
  - `/smartspec_generate_spec v5.7`
  - `/smartspec_generate_tasks v5.7`

Output: `.spec/reports/portfolio-planner/`

---
## 13) Follow-ups
- `/smartspec_validate_index`
- `/smartspec_global_registry_audit`
- `/smartspec_generate_spec`
- `/smartspec_generate_plan`
- `/smartspec_generate_tasks`
- `/smartspec_sync_spec_tasks --mode=additive`

---
## 14) Legacy Flags Inventory
Kept:
- `--mode`, `--index`, `--specindex`, `--registry-dir`, `--report`, `--dry-run`

Additive (v5.7):
- `--registry-roots`
- `--workspace-roots`
- `--repos-config`
- `--safety-mode`

No legacy behavior removed; all updates are additive and backward-compatible.

