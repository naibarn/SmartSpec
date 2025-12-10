---
name: /smartspec_reindex_specs
version: 5.7.0
role: index/governance
write_guard: ALLOW-WRITE
purpose: Rebuild and refresh SPEC_INDEX with SmartSpec v5.7 governance (multi-repo, multi-registry, repo-hints, safety-mode, UI JSON signals) while preserving full backward compatibility with v5.2–v5.6 behavior.
version_notes:
  - v5.6: multi-repo/multi-registry baseline, repo-hints, readiness warnings
  - v5.7.0: governance alignment; stricter cross-repo safety; UI metadata signals; clarified index invariants; documentation-only update
---

# /smartspec_reindex_specs (v5.7.0)

Rebuild or refresh SPEC_INDEX with SmartSpec **v5.7** rules:
- canonical `.spec/` ownership
- multi-repo detection via repos-config/workspace-roots
- merged registry-awareness for warnings
- UI JSON governance signals
- strict safety-mode

All v5.6 functionality is preserved.

---
## 1) Responsibilities
- discover all specs across repo roots
- rebuild canonical index deterministically
- preserve stable spec IDs and categories
- populate safe fields (paths, status, timestamps, repo-hints)
- detect duplicates / conflicts / category drift
- optional registry readiness warnings
- optional root mirror

---
## 2) Inputs
- spec roots (explicit or default `specs/`)
- existing index files
- multi-repo configuration
- optional registry directories
- UI JSON (read-only signals)

---
## 3) Outputs
- `.spec/SPEC_INDEX.json` (canonical)
- optional root mirror `SPEC_INDEX.json`
- report under `.spec/reports/reindex-specs/`

---
## 4) Flags
### 4.1 Output
- `--out=<path>` (default `.spec/SPEC_INDEX.json`)
- `--mirror-root=<true|false>`

### 4.2 Discovery
- `--roots=<csv>`
- `--include-drafts=<true|false>`

### 4.3 Multi-Repo (v5.7)
- `--workspace-roots=<csv>`
- `--repos-config=<path>` (preferred)

### 4.4 Registry Awareness
- `--registry-dir=<path>` (default `.spec/registry`)
- `--registry-roots=<csv>` (read-only supplemental)

### 4.5 Repo-Hints
- `--emit-repo-hints=<true|false>`

### 4.6 Safety / Output
- `--fix` (safe normalization only)
- `--report=<summary|detailed>`
- `--dry-run`
- `--safety-mode=<strict|dev>` (default strict)
- `--strict` alias

---
## 5) Canonical Index Resolution
Order:
1. `.spec/SPEC_INDEX.json`
2. `SPEC_INDEX.json`
3. `.smartspec/SPEC_INDEX.json`
4. `specs/SPEC_INDEX.json`

Missing index → generate new.
Strict mode logs missing-index as governance risk.

---
## 6) Multi-Repo Resolution
Prefer `--repos-config`.
Else merge workspace-roots + current repo.
Validate index `repo` fields when present.
Strict mode: mismatched repo mapping = blocking.

---
## 7) Registry Awareness (Warnings Only)
Load primary + supplemental registries.
Detect:
- same-name/different-meaning
- same-meaning/different-name
- ownership ambiguity

Reindex never writes registries; surfaces warnings only.

---
## 8) UI JSON Governance Signals
When UI specs include `ui.json`, collect metadata:
- `source`, `generator`, `generated_at`
- `design_system_version`, `style_preset`, `review_status`

Missing UI JSON for UI category = warning.

---
## 9) Spec Discovery
Scan all repo roots for spec roots.
Detect `spec.md` using deterministic ordering.
Support legacy folder structures.
Never mutate spec files.

---
## 10) Build Index Entries
Extract:
- id
- title
- category
- status
- dependencies
- path
- optional repo-hints

Only infer dependencies when unambiguous.

---
## 11) Duplicate & Conflict Checks
Detect:
- duplicate IDs
- duplicate paths
- category conflicts

Strict mode treats as blocking.

---
## 12) Optional Registry Readiness
Emit warnings when:
- multiple specs imply shared API/model ownership
- UI category has no UI registry present
- supplemental registry contradicts primary

---
## 13) Write Canonical Index
Default to `.spec/SPEC_INDEX.json`.
Schema must remain backward compatible.
Repo-hints written only when schema already supports them.

---
## 14) Optional Root Mirror
Write `SPEC_INDEX.json` only when requested or when a legacy mirror exists.
Do not write `.smartspec/SPEC_INDEX.json`.

---
## 15) Reporting
Include:
- output path
- mirror policy
- repo roots
- spec roots
- duplicates/conflicts
- registry warnings
- repo-hint summary
- recommended next steps:
  - `/smartspec_validate_index`
  - `/smartspec_generate_spec`
  - `/smartspec_generate_tasks`

---
## 16) Legacy Flags Inventory
Kept:
- `--roots`, `--include-drafts`, `--workspace-roots`, `--repos-config`, `--mirror-root`, `--fix`, `--report`, `--dry-run`

Additive (v5.7):
- `--registry-roots`, `--safety-mode`, `--emit-repo-hints`
