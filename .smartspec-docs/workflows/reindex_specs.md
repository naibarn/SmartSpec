---
description: SmartSpec Reindex Specs Guide (v5.2)
version: 5.2
last_updated: 2025-12-07
---

# SmartSpec Reindex Specs Guide

This guide explains how to use `/smartspec_reindex_specs` in SmartSpec v5.2.

Reindexing rebuilds the project’s `SPEC_INDEX.json` by scanning existing spec folders and consolidating metadata into a canonical index. In v5.2, this workflow is designed to remain compatible with the existing `SPEC_INDEX.json` schema already used in production.

---

## Key Concepts

### SmartSpec Centralization (v5.2)

SmartSpec v5.2 separates **tooling files** from **project-owned truth**.

- **Project-owned canonical space:** `.spec/`
- **Canonical index:** `.spec/SPEC_INDEX.json`
- **Shared registries (optional):** `.spec/registry/`
- **Legacy root mirror:** `SPEC_INDEX.json`
- **Deprecated tooling index:** `.smartspec/SPEC_INDEX.json`

Reindexing writes the rebuilt index to the canonical location by default.

### Multi-Repo Reality

Many large projects distribute specs across sister repositories (e.g., public + private + tools). In v5.2, `/smartspec_reindex_specs` can **scan across multiple repo roots** to discover `specs/**/spec.md` while keeping the output schema stable.

Important intent:

- Multi-repo roots are used for **read-only discovery**.
- The canonical output is written to the **current repo** unless you override `--output-index`.

### UI Design Addendum

When the portfolio contains UI specs:

- The **UI design source of truth** is `ui.json` in the UI spec folder.
- `spec.md` documents constraints and mapping.
- UI JSON should not contain business logic.

The reindex workflow does not validate UI JSON deeply, but it detects UI markers to improve category correctness.

---

## What Reindexing Produces

By default, the workflow writes:

- **Canonical index:** `.spec/SPEC_INDEX.json`

Optionally, it can also write:

- **Legacy mirror:** `SPEC_INDEX.json` at repo root
  - Only recommended if your existing tools still read the root mirror.

It also generates a report under:

- **Default:** `.spec/reports/reindex-specs/`

---

## When to Use

- After adding/removing many specs
- After moving/renaming spec folders
- When dependencies or counts appear inconsistent
- After a multi-repo restructure
- Before major releases

---

## Inputs

The reindex workflow scans:

- `specs/**/spec.md`

It may also read an existing index to preserve legacy fields required by production:

- `.spec/SPEC_INDEX.json`
- `SPEC_INDEX.json` (root)

---

## Command Reference

### Basic Usage (Single Repo)

```bash
/smartspec_reindex_specs
```

### Reindex With Detailed Report

```bash
/smartspec_reindex_specs --report-dir=.spec/reports/reindex-specs --strict=false
```

### Multi-Repo Scan With Workspace Roots

```bash
/smartspec_reindex_specs \
  --workspace-roots="../Smart-AI-Hub,../smart-ai-hub-enterprise-security"
```

### Multi-Repo Scan With Config

```bash
/smartspec_reindex_specs \
  --repos-config=.spec/smartspec.repos.json
```

Example config:

```json
{
  "version": "1.0",
  "repos": [
    { "id": "public", "root": "../Smart-AI-Hub" },
    { "id": "private", "root": "../smart-ai-hub-enterprise-security" }
  ]
}
```

### Control Root Mirror

```bash
/smartspec_reindex_specs --mirror-root=true
/smartspec_reindex_specs --mirror-root=false
```

### Dry Run

```bash
/smartspec_reindex_specs --dry-run
```

---

## Flags

### Index Input / Output

- `--index`
  - Override the existing index path used for bootstrapping legacy fields.
  - If omitted, auto-detect order:
    1) `.spec/SPEC_INDEX.json`
    2) `SPEC_INDEX.json`
    3) `.smartspec/SPEC_INDEX.json` (deprecated)
    4) `specs/SPEC_INDEX.json`

- `--output-index`
  - Path for the rebuilt **canonical** index.
  - Default: `.spec/SPEC_INDEX.json`

- `--mirror-root`
  - Also write/update root `SPEC_INDEX.json`.
  - Default behavior:
    - `true` if a root mirror already exists
    - otherwise `false`

### Multi-Repo Support (v5.2)

- `--workspace-roots`
  - Comma-separated list of additional repo roots to scan.

- `--repos-config`
  - JSON config for structured multi-repo scanning.
  - Recommended location: `.spec/smartspec.repos.json`

If neither is provided, scanning is limited to the current repo.

### Reporting / Safety

- `--report-dir`
  - Default: `.spec/reports/reindex-specs/`

- `--strict`
  - Fail on warnings such as duplicate IDs or severe dependency anomalies.

- `--dry-run`
  - Print the rebuilt index summary without writing files.

---

## How Reindexing Handles Multi-Repo Output

Because your existing ecosystem relies on stable `SPEC_INDEX.json` shape, the reindex workflow keeps the index schema compatible by default.

- `path` values remain **repo-relative** (e.g., `specs/core/spec-core-001-authentication/`).
- The workflow does **not** embed absolute paths into `path`.

If you later want explicit public/private labeling, add optional fields through governance workflows rather than requiring them here.

---

## UI-Aware Index Notes

The reindex workflow will warn when:

- A spec appears to be UI (has `ui.json`) but category is not `ui`.
- A spec is categorized as `ui` but `ui.json` cannot be found.

These warnings are advisory and become stricter only when your team policy enables strict gating.

---

## Common Pitfalls

### Duplicate IDs Across Repos

When scanning multiple repos, you may discover duplicate spec IDs.

Recommended fixes:

- Rename one of the specs to avoid global ID collisions.
- Or introduce a governance rule for ID namespaces per repo (if your organization needs it).

### Unexpected Root Mirror Changes

If you do not want root `SPEC_INDEX.json` to be touched, explicitly set:

```bash
/smartspec_reindex_specs --mirror-root=false
```

---

## Recommended Follow-Up Workflows

- `/smartspec_validate_index --workspace-roots=...`
- `/smartspec_sync_spec_tasks --mode=additive` (after review)
- `/smartspec_spec_lifecycle_manager`
- `/smartspec_portfolio_planner`

---

## Best Practices

- Treat `.spec/SPEC_INDEX.json` as the single source of truth.
- Keep root `SPEC_INDEX.json` only as a legacy mirror for tools that still require it.
- When working across public/private repos, always provide:
  - `--workspace-roots` or `--repos-config`
  - so scanning reflects your real system.
- Run `/smartspec_validate_index` after large reindex operations.

---

## Summary

`/smartspec_reindex_specs` in v5.2 provides a safe, schema-compatible way to rebuild your index while respecting the new centralization model and the reality of multi-repo ecosystems. It strengthens planning and execution by ensuring all downstream workflows rely on a consistent, canonical index.

