---
description: SmartSpec Reindex Specs Manual (v5.6)
version: 5.6
last_updated: 2025-12-08
---

# SmartSpec Reindex Specs Guide

Rebuild or refresh the project’s `SPEC_INDEX.json` by scanning existing spec folders.

This v5.6 manual preserves the original reindex style:

- Non-destructive discovery
- Schema stability
- Support for legacy mirrors
- Multi-repo scanning

And adds optional v5.6 readiness enhancements to improve the full chain:

- Multi-registry warning-only checks
- Optional repo-hint enrichment
- UI-aware index warnings

---

## Key Concepts

### SmartSpec Centralization

- **Canonical project-owned layer:** `.spec/`
- **Canonical index:** `.spec/SPEC_INDEX.json`
- **Shared registries:** `.spec/registry/`
- **Legacy mirror:** `SPEC_INDEX.json` (optional)
- `.smartspec/` is tooling-only

### Why Reindexing Matters

Reindexing ensures:

- Specs are discoverable by stable IDs.
- Dependencies are visible and consistent across teams.
- Downstream workflows (generate_spec/plan/tasks/sync) operate on the same portfolio map.

---

## 1. Summary

`/smartspec_reindex_specs`:

1) Discovers `spec.md` files under configured roots.
2) Extracts stable metadata such as:
   - spec id
   - title
   - category
   - status
   - dependencies
   - path
3) Detects duplicate IDs and path conflicts.
4) Writes the canonical index to `.spec/SPEC_INDEX.json`.
5) Optionally writes the legacy root mirror.
6) Produces a report that can be used as the governance starting point.

---

## 2. Usage

```bash
/smartspec_reindex_specs [options...]
```

Examples:

```bash
# Basic reindex
/smartspec_reindex_specs

# Multi-repo reindex
/smartspec_reindex_specs \
  --repos-config=.spec/smartspec.repos.json \
  --roots="specs" \
  --mirror-root=true

# Warning-only registry readiness
/smartspec_reindex_specs \
  --registry-dir=.spec/registry \
  --registry-roots="../Repo-A/.spec/registry,../Repo-B/.spec/registry"
```

---

## 3. What Reindexing Produces

By default:

- **Canonical index:** `.spec/SPEC_INDEX.json`

Optionally:

- **Legacy mirror:** `SPEC_INDEX.json` at repo root

Reports:

- `.spec/reports/reindex-specs/`

---

## 4. Key Flags

### 4.1 Index Output

```bash
--out=<path>                 # or --output-index if supported
--mirror-root=<true|false>
```

Defaults:

- `--out` → `.spec/SPEC_INDEX.json`
- `--mirror-root` → `true` only when a root mirror already exists

### 4.2 Spec Discovery

```bash
--roots=<csv>
--include-drafts=<true|false>
```

Default roots:

- `specs/` (plus any legacy project roots your system supports)

### 4.3 Multi-Repo

```bash
--workspace-roots=<csv>
--repos-config=<path>
```

- `--repos-config` takes precedence over `--workspace-roots`.

### 4.4 Optional Multi-Registry Readiness (Warning-Only)

```bash
--registry-dir=<dir>
--registry-roots=<csv>
```

Behavior:

- Load registries read-only to emit early warnings such as:
  - potential shared-name ambiguity
  - likely cross-repo naming drift
- This does not modify registry files.

### 4.5 Optional Repo Hint Enrichment

```bash
--emit-repo-hints=<true|false>
```

Rules:

- Must remain backward compatible.
- If your index schema supports a `repo` field:
  - populate it when enabled.
- Otherwise:
  - include repo hints in the report only.

### 4.6 Reporting & Safety

```bash
--report=<summary|detailed>
--dry-run
--strict
```

---

## 5. How Reindexing Works (High-Level)

1) Build repo root search list:
   - current repo
   - `--repos-config` roots
   - `--workspace-roots` roots
2) Scan configured spec roots under each repo root.
3) Extract stable metadata from each spec.
4) Detect duplicates and conflicts.
5) Optionally load registries for readiness warnings.
6) Write canonical index and optional mirror.
7) Emit a structured report.

---

## 6. UI-Aware Index Notes

To reduce UI drift:

- If a spec includes `ui.json` but is not categorized as `ui`, reindex should warn.
- If a spec is categorized `ui` but lacks `ui.json` in JSON-first projects, reindex should warn.

---

## 7. Best Practices

### Single Repo

```bash
/smartspec_reindex_specs --report=detailed
```

### Two or More Repos

```bash
/smartspec_reindex_specs \
  --repos-config=.spec/smartspec.repos.json \
  --roots="specs" \
  --report=detailed
```

Use registry readiness warnings when migrating to strict chain governance:

```bash
/smartspec_reindex_specs \
  --registry-dir=.spec/registry \
  --registry-roots="../Repo-A/.spec/registry,../Repo-B/.spec/registry"
```

---

## 8. Recommended Follow-Up Workflows

- `/smartspec_validate_index`
- `/smartspec_generate_spec`
- `/smartspec_generate_plan`
- `/smartspec_generate_tasks`
- `/smartspec_sync_spec_tasks`

---

## 9. For the LLM

When consuming a newly reindexed portfolio:

- Treat `.spec/SPEC_INDEX.json` as canonical.
- Do not rely on `.smartspec/` for governance.
- Use registries for shared naming before suggesting any new shared entity.
- If duplicate IDs are reported, stop and reconcile ownership.

---

## 10. Summary

`/smartspec_reindex_specs v5.6` provides a stable, non-destructive foundation for large SmartSpec portfolios and enables reliable multi-repo governance with optional warning-only registry readiness hooks.

