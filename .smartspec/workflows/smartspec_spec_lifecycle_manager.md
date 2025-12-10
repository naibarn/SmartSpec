---
name: /smartspec_spec_lifecycle_manager
version: 5.7.0
role: lifecycle/governance
write_guard: NO-WRITE
purpose: Manage SmartSpec spec lifecycle states (draft → ready → active → deprecated → archived) with full v5.6–v5.7 governance: multi-repo, multi-registry, safety-mode, UI JSON signals, chain-readiness.
version_notes:
  - v5.6: baseline lifecycle with multi-repo/registry safety
  - v5.7.0: governance alignment; expanded safety; UI JSON signals; chain-readiness; backward-compatible; documentation-only
---

# /smartspec_spec_lifecycle_manager (v5.7.0)

Lifecycle controller for SmartSpec specs, enforcing:
- canonical index
- multi-repo governance
- registry consistency
- UI JSON readiness
- dependency safety

States:
- **draft**
- **ready**
- **active**
- **deprecated**
- **archived**

Actions are non-destructive and metadata‑only.

---
## 1) Responsibilities
- detect canonical SPEC_INDEX
- validate spec completeness
- validate dependencies + cross-SPEC alignment
- validate registry coverage + ownership
- validate UI JSON metadata for UI categories
- promote/demote spec lifecycle states safely
- generate lifecycle report

---
## 2) Flags
### Index / Registry
- `--index` (alias: `--specindex`)
- `--registry-dir`
- `--registry-roots` (supplemental; read-only)

### Multi-repo
- `--workspace-roots`
- `--repos-config` (preferred)

### Lifecycle
- `--spec`
- `--target-state=<draft|ready|active|deprecated|archived>`

### Safety
- `--safety-mode=<strict|dev>` (default: strict)
- `--strict` alias
- `--dry-run`

### Reporting
- `--report=<summary|detailed>`

---
## 3) Canonical Index Resolution
Order:
1. `.spec/SPEC_INDEX.json`
2. `SPEC_INDEX.json`
3. `.smartspec/SPEC_INDEX.json`
4. `specs/SPEC_INDEX.json`

Missing index:
- strict → block
- dev → warning

---
## 4) Multi-repo Resolution
- use repos-config when available
- otherwise merge workspace-roots + current repo
- ensure index `repo:` matches mapping

Strict mode:
- mismatch = blocking

---
## 5) Registry Validation
- load primary registry
- load supplemental registries read‑only
- classify collisions:
  - same-name/different-meaning
  - same-meaning/different-name
  - ownership ambiguity

Strict mode:
- collisions block promotion

---
## 6) UI JSON Governance
For UI specs:
- require `ui.json`
- validate metadata:
  - `source`, `generator`, `generated_at`
  - `design_system_version`, `style_preset`, `review_status`

Missing UI JSON:
- strict → blocking for ready/active

---
## 7) State Transition Rules
### draft → ready
Requires:
- spec completeness
- tasks present
- no dependency gaps
- no registry collisions
- UI JSON present (UI specs)

### ready → active
Requires:
- passing tests
- validated dependencies
- no unresolved ownership ambiguity
- no blocking registry conflicts

### active → deprecated
Allowed when:
- successor spec indicated
- no hard conflicts introduced

### deprecated → archived
Allowed when:
- dependencies removed
- safe references confirmed

---
## 8) Reporting
Report includes:
- spec ID + current state
- target state
- index context
- multi-repo context
- registry view
- UI JSON readiness
- dependency readiness
- blocking vs warning issues

Output: `.spec/reports/spec-lifecycle-manager/`

---
## 9) Follow-ups
- `/smartspec_validate_index`
- `/smartspec_global_registry_audit`
- `/smartspec_reindex_specs`
- `/smartspec_generate_tasks`
- `/smartspec_release_readiness`

---
## 10) Legacy Flags Inventory
Kept:
- `--index`, `--specindex`, `--registry-dir`, `--spec`, `--report`, `--strict`, `--dry-run`

Additive (v5.7):
- `--registry-roots`
- `--workspace-roots`
- `--repos-config`
- `--safety-mode`

No legacy behavior removed.

