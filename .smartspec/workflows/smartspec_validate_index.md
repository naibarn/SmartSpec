---
name: /smartspec_validate_index
version: 5.7.0
role: validate/governance
write_guard: NO-WRITE
purpose: Validate SPEC_INDEX.json and registry/multi-repo governance alignment under SmartSpec v5.6–v5.7.
version_notes:
  - v5.6: multi-repo/multi-registry validator introduced
  - v5.7.0: governance alignment update; expanded safety gates; backward-compatible
---

# /smartspec_validate_index (v5.7.0)

This workflow validates the **SPEC_INDEX.json** ecosystem:
- canonical index rules
- multi-repo mapping
- multi-registry validation
- cross-SPEC dependency graph
- registry collision checks
- UI JSON governance indicators

It is the **first gate** before:
1. `/smartspec_generate_spec`
2. `/smartspec_generate_tasks`

Only **safe auto-fixes** are allowed.

---
## 1) Responsibilities
- Detect canonical SPEC_INDEX
- Validate index structure + dependency graph
- Validate repo-mapping correctness (repos-config preferred)
- Validate registry completeness + collisions across repo roots
- Validate UI JSON presence/metadata for UI specs
- Produce readiness assessment
- Apply safe metadata fixes when `--fix` is set

---
## 2) Flags
### Index / Registry
- `--index` (alias: `--specindex`)
- `--registry-dir` (default `.spec/registry`)
- `--registry-roots` supplemental read-only registries

### Multi-Repo
- `--workspace-roots`
- `--repos-config` (preferred)

### Validation Mode
- `--mode=runtime | portfolio` (default: portfolio)
  - **runtime**: strict blocking errors
  - **portfolio**: warnings allowed

### Fix & Reporting
- `--fix` (safe metadata fixes only)
- `--report=summary | detailed`

### Safety
- `--safety-mode=<strict|dev>` (default: strict)
- `--strict` alias
- `--dry-run`

---
## 3) Canonical Index Resolution
Detection order:
1. `.spec/SPEC_INDEX.json` (canonical)
2. `SPEC_INDEX.json` (root mirror)
3. `.smartspec/SPEC_INDEX.json` (deprecated)
4. `specs/SPEC_INDEX.json` (legacy)

Canonical output is always the first.

If no index:
- `runtime` → blocking
- `portfolio` → warning

---
## 4) Multi-Repo Resolution
Order:
1. current repo
2. repos-config (preferred)
3. workspace-roots

Checks:
- Index `repo:` fields must match repos-config
- Missing mappings:
  - `runtime` → blocking
  - `portfolio` → warning

---
## 5) Registry Resolution
Primary registry:
- from `--registry-dir` or default

Supplemental registries:
- from `--registry-roots` (read-only)

Checks:
- Cross-repo naming collisions (API, models, terms, components)
- Conflicting definitions:
  - `runtime` → blocking
  - `portfolio` → warning

---
## 6) Index Integrity Checks
Validate:
- unique spec IDs
- paths exist (multi-repo aware)
- valid status values
- dependencies resolve to real specs
- no cycles in dependency graph

Missing spec files:
- `runtime` → blocking
- `portfolio` → warning

---
## 7) UI JSON Governance Checks
For UI specs:
- `ui.json` existence
- metadata expectations (v5.7):
  - `source`, `generator`, `generated_at`
  - `design_system_version`, `style_preset`, `review_status`
- do not modify UI JSON

Missing UI JSON where required:
- warning (portfolio)
- blocking (runtime)

---
## 8) Cross-Workflow Alignment
Validator ensures readiness for:
- generate_spec
- generate_tasks

Checks:
- registry completeness (to avoid name duplication)
- repo mapping correctness
- index paths + dependency correctness

---
## 9) Safe Auto-Fix Rules (`--fix`)
Allowed:
- normalize timestamps
- repair optional metadata
- infer safe dependents

Forbidden:
- renaming spec IDs
- modifying dependency semantics
- altering registry definitions
- editing UI JSON

Dry run:
- show intended fixes only

---
## 10) Report Contents
- index path used
- multi-repo mapping
- registry directories
- missing specs
- dependency issues
- repo mapping issues
- registry collisions
- UI JSON governance gaps
- readiness summary for downstream workflows

---
## 11) Examples
- `/smartspec_validate_index`
- `/smartspec_validate_index --report=detailed`
- `/smartspec_validate_index --fix --report=detailed`
- `/smartspec_validate_index --repos-config=.spec/smartspec.repos.json`
- `/smartspec_validate_index --registry-roots="../RepoA/.spec/registry" --report=detailed`

---
## 12) Legacy Flags Inventory
Kept:
- `--index`, `--specindex`, `--registry-dir`, `--fix`, `--report`, `--mode`

Additive (v5.7):
- `--registry-roots`, `--workspace-roots`, `--repos-config`, `--safety-mode`, `--dry-run`

No legacy behavior removed.

