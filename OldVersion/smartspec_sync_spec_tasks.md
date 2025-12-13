---
name: /smartspec_sync_spec_tasks
version: 5.7.0
role: sync/governance
write_guard: ALLOW-WRITE
purpose: Synchronize spec metadata and task-derived signals into the canonical SmartSpec centralized layer with full v5.6–v5.7 governance: multi-repo, multi-registry, safety-mode, UI JSON governance.
version_notes:
  - v5.6: multi-repo/multi-registry sync upgrade
  - v5.7.0: governance alignment update; additive-only writes; backward-compatible
---

# /smartspec_sync_spec_tasks

Synchronize **spec metadata** and **task-derived signals** into SmartSpec’s centralized truth:
- `.spec/SPEC_INDEX.json` (canonical index)
- `.spec/registry/` (canonical registries)

Supports:
- multi-repo resolution
- multi-registry validation
- UI JSON governance
- safety-mode gating (strict/dev)

NO destructive writes are allowed.

---
## 1) What It Does
- Resolve canonical index & registry directories.
- Merge primary + supplemental registries.
- Resolve multi-repo structure (repos-config preferred).
- Read target spec(s) + tasks.
- Sync safe index fields (path, status, dependencies, counts).
- Recommend or apply additive registry updates.
- Validate cross-SPEC ownership & naming.
- Validate UI JSON alignment when applicable.
- Produce sync report under `.spec/reports/sync-spec-tasks/`.

---
## 2) When to Use
- After updating tasks.
- After large-scale work on multiple specs.
- Before plan generation or release readiness.
- During governance migrations.

---
## 3) Inputs
- `spec.md` (required)
- `tasks.md` (recommended)
- `ui.json` (UI specs only)
- `.spec/SPEC_INDEX.json`
- `.spec/registry/*.json`
- supplemental registries via `--registry-roots`
- multi-repo mappings via `--repos-config` / `--workspace-roots`

---
## 4) Outputs
- Updated canonical index (`.spec/SPEC_INDEX.json`)
- Optional updated root mirror (`SPEC_INDEX.json`)
- Additive registry entries (mode-dependent)
- Sync report

---
## 5) Flags
### Index / Registry
- `--index` (alias: `--specindex`)
- `--registry-dir` (default `.spec/registry`)
- `--registry-roots` supplemental read-only registries

### Multi-Repo
- `--workspace-roots`
- `--repos-config` (preferred)

### Target Selection
- `--spec`
- `--spec-ids`

### Sync Behavior
- `--mode= recommend | additive` (default: recommend)
- `--mirror-root=<true|false>`

### Safety
- `--safety-mode=<strict|dev>` (default: strict)
- `--strict` alias
- `--dry-run`

---
## 6) Canonical Index Resolution
Detection order:
1. `.spec/SPEC_INDEX.json` (canonical)
2. `SPEC_INDEX.json` (root mirror)
3. `.smartspec/SPEC_INDEX.json` (deprecated)
4. `specs/SPEC_INDEX.json` (legacy)

Canonical output is always written to:
- `.spec/SPEC_INDEX.json`

Root mirror updated only when:
- requested or
- already exists.

---
## 7) Registry Resolution
- Primary registry = authoritative.
- Supplemental registries = read-only.
- Cross-registry collision → warning or block (strict).
- Never delete/rename entries.
- Additive mode adds entries only when clearly new + unambiguous.

---
## 8) Multi-Repo Resolution
- Prefer `--repos-config` for deterministic mapping.
- Else derive roots from `--workspace-roots` + current repo.
- Validate repo IDs in index.
- Never write into sibling repos.

---
## 9) Identify Target Specs
Priority:
1. `--spec`
2. `--spec-ids`
3. index mapping
4. else: require explicit selection

Tasks location: `tasks.md` next to `spec.md`.

---
## 10) Read Inputs (Read-Only)
Extract:
- title, category, dependencies
- cross-spec references
- shared names
- task progress signals
- UI JSON metadata (when exists)

---
## 11) Consistency Gate
### Index vs Spec
- path/ID mismatch
- category mismatch
- dependency mismatch

### Registry vs Spec/Tasks
- undefined shared names
- conflicting names in supplemental registries

Strict mode:
- block ambiguous updates
- require manual review via report

---
## 12) Safe Index Updates
Allowed fields:
- normalized `path`
- `repo` (when resolvable)
- dependencies (non-ambiguous)
- `status` (inferred from tasks)
- count fields

Not allowed:
- renaming spec IDs
- redefining dependencies when ambiguous
- destructive field removal

---
## 13) Registry Alignment
### recommend (default)
- output suggestions only
- detect missing APIs, models, terms

### additive
- append-only new entries when:
  - clearly shared
  - not found in any registry
  - conflict-free

Strict mode:
- disallow new shared entries when any collision detected across supplemental registries.

---
## 14) UI JSON Alignment
Apply when:
- UI spec category
- `ui.json` exists
- spec references UI JSON workflow

Rules:
- UI JSON is design-owned
- metadata expectations (v5.7):
  - `source`, `generator`, `generated_at`
  - `design_system_version`
  - `style_preset`
  - `review_status`

Checks:
- component names align with component registry
- warn when UI JSON required but missing
- do not modify UI JSON in this workflow

---
## 15) Optional Root Mirror Update
Only copy canonical index → root mirror when:
- `--mirror-root=true`, or
- mirror exists

Do NOT write `.smartspec/SPEC_INDEX.json`.

---
## 16) Reporting
Report fields:
- index input/output
- registry dirs
- supplemental registry dirs
- multi-repo roots
- specs processed
- index updates
- registry suggestions/changes
- UI JSON checks
- collisions + ambiguity
- follow-up recommendations

---
## 17) Follow-ups
- `/smartspec_validate_index`
- `/smartspec_generate_plan`
- `/smartspec_generate_tasks`
- `/smartspec_generate_tests`
- `/smartspec_verify_tasks_progress`
- `/smartspec_reindex_specs`

---
## 18) Legacy Flags Inventory
Kept:
- `--index`, `--specindex`, `--registry-dir`, `--spec`, `--mode`, `--strict`, `--mirror-root`, `--dry-run`

Additive (v5.7):
- `--registry-roots`
- `--workspace-roots`
- `--repos-config`
- `--safety-mode`

No legacy behavior removed.

