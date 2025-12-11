---
name: /smartspec_reindex_workflows
version: 1.0.0
role: index/governance
write_guard: ALLOW-WRITE (index-only)
purpose: Build and refresh WORKFLOW_INDEX.json with SmartSpec governance rules (multi-repo, write-guards, roles, categories, CLI flags, platforms) while preserving full backward compatibility across workflow specs.
version_notes:
  - v1.0.0: initial release; parallel to /smartspec_reindex_specs v5.7.0; workflow-index-only writes; JSON schema stable but extensible
---

# /smartspec_reindex_workflows (v1.0.0)

Rebuild or refresh the **WORKFLOW_INDEX.json** file with SmartSpec workflow-governance rules:
- discover all workflow specs under `.smartspec/workflows/`
- parse workflow metadata (id, name, version, role, write_guard, CLI flags)
- normalize into a single canonical `WORKFLOW_INDEX.json`
- support multi-repo via `--workspace-roots` and `--repos-config`
- never modify workflow spec files themselves

This command is the workflow-analogue of `/smartspec_reindex_specs`, but operates on **workflow definitions**, not feature specs.

---
## 1) Responsibilities

`/smartspec_reindex_workflows` must:

- discover all workflow spec files (e.g. `.smartspec/workflows/*.md`)
- rebuild a canonical, deterministic **WORKFLOW_INDEX** structure
- preserve stable workflow IDs and categories when unchanged
- populate safe metadata fields:
  - id, CLI name, version, role, category, status
  - write_guard
  - source_file
  - supported_platforms
  - core CLI flags (required/optional)
  - dependency hints (depends_on / produces)
- detect duplicates / conflicts (e.g. same id, different role)
- write `WORKFLOW_INDEX.json` under `.smartspec/`
- emit a human-readable report under `.spec/reports/reindex-workflows/`

The workflow must not attempt to validate every semantic detail; deeper validations are delegated to future `/smartspec_validate_workflows` (if present).

---
## 2) Inputs

- workflow roots (explicit or default `.smartspec/workflows/`)
- existing WORKFLOW_INDEX.json (if any)
- multi-repo configuration (workspace-roots & repos-config)
- optional registry or governance files (read-only)

Inputs may be discovered automatically when not provided explicitly.

---
## 3) Outputs

- `.smartspec/WORKFLOW_INDEX.json` (canonical, primary)
- optional root mirror `WORKFLOW_INDEX.json` (when requested or legacy mirror exists)
- report under `.spec/reports/reindex-workflows/` (markdown + JSON)

`WORKFLOW_INDEX.json` must be written atomically where practical (write to temp file then move).

---
## 4) Flags

### 4.1 Output
- `--out=<path>` (default `.smartspec/WORKFLOW_INDEX.json`)
- `--mirror-root=<true|false>` (default `false`)

### 4.2 Discovery
- `--workflow-roots=<csv>` (default `.smartspec/workflows`)
- `--include-internal=<true|false>` (include `internal`/`experimental` workflows; default `true`)

### 4.3 Multi-Repo
- `--workspace-roots=<csv>`
- `--repos-config=<path>` (preferred)

### 4.4 Safety / Output
- `--report=<summary|detailed>` (default `summary`)
- `--dry-run` (compute index, emit report, but do not write WORKFLOW_INDEX.json)
- `--safety-mode=<strict|dev>` (default `strict`)
- `--strict` (alias for `--safety-mode=strict`)

### 4.5 Filtering
- `--include-status=<csv>` (e.g. `stable,beta`)
- `--exclude-status=<csv>` (e.g. `deprecated,internal-only`)
- `--include-platforms=<csv>` (e.g. `kilocode,claudecode`)

---
## 5) Canonical Index Resolution

Resolution order for existing WORKFLOW_INDEX:

1. `.smartspec/WORKFLOW_INDEX.json`
2. `WORKFLOW_INDEX.json` at repo root

Missing index → generate a new one.

In `strict` safety mode, a missing index is logged as a governance warning but does not block reindexing.

---
## 6) Multi-Repo Resolution

Prefer `--repos-config` when provided. Else:
- merge `--workspace-roots` with current repo location
- ensure workflow `source_file` paths are recorded as repo-relative

In strict mode:
- mismatched repo hints (if present) should raise warnings
- invalid `source_file` paths (no longer exist) must be flagged

---
## 7) Workflow Discovery

Scan all workflow roots for files matching SmartSpec workflow spec patterns, typically:
- `.smartspec/workflows/*.md`

Rules:
- ignore non-workflow files
- support legacy naming formats (e.g. `smartspec-*.md`)
- never mutate workflow spec files

---
## 8) Build Index Entries

For each workflow spec, extract or infer:
- `id` — canonical workflow id (e.g. `smartspec_report_implement_prompter`)
- `name` — CLI name (e.g. `/smartspec_report_implement_prompter`)
- `version` — workflow spec version
- `role` — e.g. `verify/strict`, `support/implement`, `index/governance`, `ui/generator`
- `category` — higher-level grouping (e.g. `verification`, `verification-support`, `spec-generation`, `ui`, `index`)
- `status` — `stable`, `beta`, `deprecated`, `internal-only`
- `description` — short purpose text
- `write_guard` — `NO-WRITE`, `TASKS-ONLY`, `REGISTRY-ONLY`, `UI-ONLY`, `ALLOW-WRITE (index-only)`
- `source_file` — path to workflow spec file
- `supported_platforms` — e.g. `["kilocode", "claudecode", "antigravity"]`
- `cli`:
  - `binary` — CLI entrypoint name
  - `required_flags[]`
  - `optional_flags[]`
- `tags[]` — free-form keywords (e.g. `strict`, `prompt`, `ide`, `index`, `multi-repo`)
- `depends_on[]` — IDs of other workflows it relies on
- `produces[]` — output path patterns (e.g. `.spec/reports/verify-tasks-progress/*.json`)
- `last_updated` — ISO timestamp if present or derivable

When fields are missing, the workflow should infer safe defaults where possible and record omissions in the report.

---
## 9) Duplicate & Conflict Checks

`/smartspec_reindex_workflows` must detect:
- duplicate IDs with conflicting definitions
- multiple workflows mapped to the same CLI name
- conflicting write_guards for the same ID

In `strict` mode:
- conflicting IDs are treated as **blocking** (index is not written)
- non-blocking issues (e.g. inconsistent tags) are recorded as warnings

In `dev` mode:
- conflicting IDs may be included in the report but index generation may proceed with last-writer-wins, clearly marked as non-canonical.

---
## 10) Write Canonical Index

Default output path:
```
.smartspec/WORKFLOW_INDEX.json
```

Rules:
- schema must remain backward compatible across minor versions
- atomic write where possible (write temp file then move)
- never write into `.spec/SPEC_INDEX.json` or any SPEC index file

When `--mirror-root=true`:
- write `WORKFLOW_INDEX.json` to repo root as a mirror
- do not treat missing mirror as error

---
## 11) Reporting

A report must be written under:
```
.spec/reports/reindex-workflows/
```

Depending on `--report` flag:
- `summary` — counts, basic issues, next steps
- `detailed` — full workflow list + per-workflow diagnostics

Report should include:
- output path
- mirror policy
- workflow roots
- number of workflows discovered
- duplicates/conflicts
- invalid or missing fields
- recommended next steps, e.g.:
  - `/smartspec_validate_workflows` (if available)
  - `/smartspec_project_copilot` to explore workflows

---
## 12) Safety & Governance

- This workflow is allowed to **write index files only** (`WORKFLOW_INDEX.json` and its mirror) and reports under `.spec/reports/`.
- It may not modify any workflow spec, feature spec, tasks, registry, or UI schema.
- In `strict` mode, severe conflicts should prevent index writing.

---
## 13) Example Usage

### 13.1 Basic reindex
```bash
/smartspec_reindex_workflows \
  --report=summary
```

### 13.2 Detailed, multi-repo
```bash
/smartspec_reindex_workflows \
  --workspace-roots=.,../service-a,../service-b \
  --repos-config=.smartspec/repos-config.json \
  --report=detailed
```

### 13.3 Dry-run for CI
```bash
/smartspec_reindex_workflows \
  --dry-run \
  --report=detailed \
  --safety-mode=strict
```

---
## 14) Integration Guidance

- SmartSpec UIs and IDE integrations may use `WORKFLOW_INDEX.json` to:
  - list available workflows
  - show metadata (status, categories, write_guard)
  - construct CLI commands based on `cli` metadata
- `/smartspec_project_copilot` should consult `WORKFLOW_INDEX.json` when recommending next-step workflows to the user.

---
## 15) Legacy & Backward Compatibility

- This workflow does not alter existing SPEC indexes or registries.
- It may coexist with older tools unaware of `WORKFLOW_INDEX.json`.
- Future versions may extend index schema but must preserve existing fields.

---

End of `/smartspec_reindex_workflows` specification.
