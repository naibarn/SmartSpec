---
name: /smartspec_global_registry_audit
version: 5.7.0
role: audit/governance
write_guard: NO-WRITE
purpose: Audit all SmartSpec registries (primary + supplemental) for cross-SPEC and cross-repo naming integrity under SmartSpec v5.6–v5.7 governance.
version_notes:
  - v5.2: initial registry audit logic
  - v5.6: multi-repo + multi-registry audit baseline
  - v5.7.0: expanded governance (UI JSON signals, stricter cross-repo safety, chain-readiness v5.7); backward-compatible; documentation-only update
---

# /smartspec_global_registry_audit (v5.7.0)

Audit SmartSpec registries to detect:
- naming drift
- same-name/different-meaning conflicts
- same-meaning/different-name duplication
- cross-repo ownership ambiguity
- coverage gaps for shared entities

Applies full SmartSpec **v5.7 governance**:
- canonical index detection
- multi-repo mapping
- multi-registry merged view
- strict safety gating
- UI JSON governance indicators
- chain-readiness for `/smartspec_generate_spec`, `/smartspec_generate_tasks` v5.7

---
## 1) Responsibilities
- Resolve primary + supplemental registries.
- Build merged validation view with deterministic precedence.
- Load SPEC_INDEX for ownership + coverage.
- Classify conflicts.
- Detect cross-repo naming drift.
- Validate UI component registry alignment when present.
- Output audit report.

No mutations of registries are allowed.

---
## 2) Inputs
- primary registry directory (default: `.spec/registry`)
- supplemental registry directories (`--registry-roots`)
- SPEC_INDEX (auto-detected)
- optional multi-repo mapping via `--repos-config` or `--workspace-roots`

---
## 3) Outputs
- audit report under `.spec/reports/global-registry-audit/`
- severity summary (portfolio/runtime)
- chain-readiness notes

---
## 4) Flags
### 4.1 Mode (legacy semantics preserved)
```
--mode=<portfolio|runtime>
```
- **portfolio** (default): broad program-level audit
- **runtime**: CI-strict blocking for conflicts

### 4.2 Safety (v5.7)
```
--safety-mode=<strict|dev>
--strict
```
- `strict`: escalate cross-repo collisions to blocking
- `dev`: allow warnings with remediation guidance

`--strict` is alias for `--safety-mode=strict`.

### 4.3 Index
```
--index=<path>
--specindex=<path>   # legacy alias
```

### 4.4 Registry
```
--registry-dir=<dir>
--registry-roots=<csv>
```

### 4.5 Multi-repo
```
--workspace-roots=<csv>
--repos-config=<path>
```
`--repos-config` takes precedence.

### 4.6 Reporting
```
--report=<summary|detailed>
--dry-run
```

---
## 5) Canonical Index & Registry Resolution
### 5.1 SPEC_INDEX detection order
1. `.spec/SPEC_INDEX.json`
2. `SPEC_INDEX.json`
3. `.smartspec/SPEC_INDEX.json` (deprecated)
4. `specs/SPEC_INDEX.json` (legacy)

If missing:
- **runtime**: blocking
- **portfolio**: warning

### 5.2 Registry View
1. load primary registry (`--registry-dir`)
2. load supplemental registries (`--registry-roots`) read-only

**Precedence:** primary > supplemental

Detect:
- same-name/different-meaning
- same-meaning/different-name
- missing ownership signals

---
## 6) Multi-Repo Resolution (v5.7)
Order of preference:
1. current repo
2. `--repos-config`
3. `--workspace-roots`

Checks:
- Index `repo:` fields must match repo mapping
- Missing repo mapping = blocking under runtime

---
## 7) Registry Families to Audit
- `api-registry.json`
- `data-model-registry.json`
- `glossary.json`
- `critical-sections-registry.json`
- `patterns-registry.json` (optional)
- `ui-component-registry.json` (optional)
- `file-ownership-registry.json` (optional)

Optional registries missing → not errors.

---
## 8) Conflict Classification (v5.7)
### 8.1 Same Name, Different Meaning
- different signatures for same API
- divergent fields for same model
- inconsistent glossary definitions

### 8.2 Same Meaning, Different Name
- structurally identical models with different names
- duplicated APIs with equivalent semantics

### 8.3 Ownership Ambiguity
- registry entries referenced by multiple specs without owner
- supplemental-registry-owned entities not represented in primary registry

Severity depends on mode + safety-mode.

---
## 9) Coverage & Reference Analysis (Index-Aware)
When index present:
- compute which specs reference which shared entities
- detect high-frequency names missing in primary registry
- multi-repo: try resolving owner spec across repo roots

---
## 10) UI Governance Signals (v5.7 extension)
When UI component registry exists:
- examine component naming consistency
- cross-reference UI JSON metadata when available:
  - `source`, `generator`, `generated_at`
  - `design_system_version`
  - `style_preset`
  - `review_status`

If UI JSON exists but component registry missing:
- warn (portfolio) or block (runtime)

---
## 11) Severity Rules
### 11.1 Baseline (`--mode`)
- **runtime**:
  - cross-registry conflicts = blocking
  - ownership ambiguity for high-impact names = blocking
- **portfolio**:
  - conflicts = warning with remediation

### 11.2 Safety Overrides (`--safety-mode`)
- strict → escalate collisions to blocking
- dev → downgrade to warnings with explicit TODOs

---
## 12) Report Structure
- index path used
- primary registry path
- supplemental registry roots
- multi-repo summary
- conflicts by family
- ownership ambiguity list
- cross-repo collision report
- UI governance notes
- coverage gaps
- chain-readiness notes for v5.7 workflows:
  - `/smartspec_generate_spec`
  - `/smartspec_generate_tasks`

Output dir:
- `.spec/reports/global-registry-audit/`

---
## 13) Recommended Follow-ups
- `/smartspec_validate_index --report=detailed`
- `/smartspec_reindex_specs`
- `/smartspec_generate_spec`
- `/smartspec_generate_plan`
- `/smartspec_generate_tasks`
- `/smartspec_sync_spec_tasks --mode=additive`

---
## 14) Legacy Flags Inventory
**Kept:**
- `--mode`, `--index`, `--specindex`, `--registry-dir`, `--report`, `--dry-run`

**Additive (v5.7):**
- `--registry-roots`
- `--workspace-roots`
- `--repos-config`
- `--safety-mode`

Behavior remains backward-compatible; no destructive operations.