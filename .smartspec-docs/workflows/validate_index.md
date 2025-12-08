---
description: SmartSpec Validate Index Guide (v5.2)
version: 5.2
last_updated: 2025-12-07
---

# SmartSpec Validate Index Guide

This guide explains how to use `/smartspec_validate_index` in SmartSpec v5.2.

Validate Index is the primary **health gate** for your specification ecosystem. It checks that `SPEC_INDEX.json` accurately represents your real specs, dependencies, and shared knowledge rules—without introducing new conflicts.

SmartSpec v5.2 introduces a clearer separation between tooling and project-owned truth and adds **multi-repo awareness** to better reflect real-world architectures where public and private specs live in separate repositories.

---

## Key Concepts

### SmartSpec Centralization (v5.2)

SmartSpec v5.2 separates **tooling** from **project-owned truth**.

- **Project-owned canonical space:** `.spec/`
- **Canonical index:** `.spec/SPEC_INDEX.json`
- **Shared registries (optional):** `.spec/registry/`
- **Legacy root mirror:** `SPEC_INDEX.json`
- **Deprecated tooling index:** `.smartspec/SPEC_INDEX.json`

The validation workflow is designed to remain compatible with your existing `SPEC_INDEX.json` schema while enforcing safer, clearer rules.

### Portfolio vs Runtime Interpretation

Large systems often store roadmap/idea specs in the index before all files exist.

To avoid forcing low-quality placeholder specs, v5.2 introduces a shared interpretation model:

- `--mode=portfolio` (default)
  - Optimized for roadmap health.
  - Planned/backlog/idea/draft specs may be missing `spec.md` without being treated as hard errors.

- `--mode=runtime`
  - Optimized for delivery readiness.
  - Active/core/stable specs are expected to have resolvable artifacts and valid dependency chains.

If a spec has no explicit status, the validator assumes it is `active`.

### Multi-Repo Reality

Many SmartSpec programs split specs across sibling repositories (e.g., public + private).

In v5.2, `/smartspec_validate_index` can check file existence across these repos using:

- `--workspace-roots`
- `--repos-config`

If you do not provide multi-repo configuration, validation runs against the **current repo only**.

### UI Design Addendum (Optional)

When your portfolio includes UI specs:

- **UI design source of truth** is `ui.json` inside the UI spec folder.
- `spec.md` documents constraints, mapping, and logic boundaries.
- UI JSON should not contain business logic.

UI checks are conditional and will not break projects that do not use UI JSON.

---

## What Validate Index Checks

The workflow performs structural checks such as:

1) **File existence** (status-aware)
2) **Broken references** (dependencies that point to missing IDs)
3) **Circular dependencies**
4) **Duplicate specs / conflicting identifiers**
5) **Orphaned specs** (status-aware)
6) **Stale specs** (optional heuristics)
7) **Metadata consistency**
8) **Dependents calculation correctness**
9) **UI JSON compliance** (conditional)

The validator is conservative by design. Its goal is to prevent your index and shared knowledge layer from drifting into contradictions.

---

## Inputs & Resolution Rules

### SPEC_INDEX auto-detection order

If you do not pass `--index`, SmartSpec resolves the index in this order:

1) `.spec/SPEC_INDEX.json` (canonical)
2) `SPEC_INDEX.json` (legacy root mirror)
3) `.smartspec/SPEC_INDEX.json` (deprecated)
4) `specs/SPEC_INDEX.json` (older layout)

### Default directories

- `REGISTRY_DIR = .spec/registry`
- **Reports default to** `.spec/reports/validate-index/`

---

## Command Reference

### Basic Validation

```bash
/smartspec_validate_index
```

### Detailed Report

```bash
/smartspec_validate_index --report=detailed
```

### Portfolio Mode (Recommended for Roadmaps)

```bash
/smartspec_validate_index --mode=portfolio --report=detailed
```

### Runtime Mode (Recommended Before Releases)

```bash
/smartspec_validate_index --mode=runtime --strict --report=detailed
```

### Multi-Repo Validation (Public + Private)

```bash
/smartspec_validate_index \
  --workspace-roots="../Smart-AI-Hub,../smart-ai-hub-enterprise-security" \
  --mode=portfolio \
  --report=detailed
```

### Use a Structured Multi-Repo Config

Create:

`.spec/smartspec.repos.json`

Example:

```json
{
  "version": "1.0",
  "repos": [
    { "id": "public", "root": "../Smart-AI-Hub" },
    { "id": "private", "root": "../smart-ai-hub-enterprise-security" }
  ]
}
```

Then run:

```bash
/smartspec_validate_index --repos-config=.spec/smartspec.repos.json --report=detailed
```

### Safe Auto-Fix Run

`--fix` is reserved for **safe, mechanical corrections**.

```bash
/smartspec_validate_index --fix --report=detailed
```

---

## Flags

### Index / Registry

- `--index`
  - Override SPEC_INDEX path.

- `--registry-dir`
  - Default: `.spec/registry`

### Multi-Repo

- `--workspace-roots`
  - Comma-separated list of additional repo roots to search for spec files.

- `--repos-config`
  - JSON config describing known repos and aliases.
  - Recommended: `.spec/smartspec.repos.json`

### Interpretation

- `--mode`
  - Values: `portfolio`, `runtime`
  - Default: `portfolio`

### Reporting

- `--report`
  - Values: `summary`, `detailed`
  - Default: `summary`

- `--output`
  - Optional custom report path

### Safety

- `--strict`
  - Treat high-risk warnings as errors.

- `--fix`
  - Apply safe auto-fixes.

- `--dry-run`
  - Print findings without writing files.

---

## What `--fix` Can and Cannot Do

### Safe auto-fixes

- Metadata count normalization
- Dependents calculation updates
- Timestamps / housekeeping fields (if applicable)

### Not auto-fixed

- Missing files
- Broken references
- Circular dependencies
- Duplicate IDs

These require human decisions to prevent low-quality placeholder specs or accidental contract changes.

---

## How to Interpret Common Findings

### High Missing File Count

In a roadmap-heavy index, this often means planned specs are listed without artifacts.

Recommended actions:

- Set explicit `status` values for planned/backlog specs.
- Use `--mode=portfolio` during roadmap phases.

### Broken References

This usually means:

- a dependency ID was renamed
- or a foundational spec is missing

Recommended actions:

- Run `/smartspec_reindex_specs` after folder moves.
- Confirm dependency IDs and correct them in the index.

### Circular Dependencies

Common causes:

- self-dependency entry mistakes
- bidirectional dependencies added during parallel development

Recommended actions:

- Remove self-loops.
- Convert one direction into a softer reference pattern.

### Large Orphan Counts

In portfolio mode, orphans are often a sign of early-stage idea volume.

In runtime mode, focus only on **active/core** orphaned specs.

---

## UI-Specific Validation Notes

The validator will perform UI checks when any of these are true:

- a spec is categorized as `ui`
- `spec.ui === true`
- `ui.json` exists in the spec folder

Typical UI warnings:

- A declared UI spec missing `ui.json`
- UI component names inconsistent with `ui-component-registry.json` (if present)

These checks remain conditional and should not fail non-UI projects.

---

## Recommended Follow-Up Workflows

- If the index looks stale or inconsistent:
  - `/smartspec_reindex_specs`

- If validation highlights cross-SPEC naming drift:
  - `/smartspec_global_registry_audit`

- If you need guided fixes:
  - `/smartspec_fix_errors` (spec-targeted or report-targeted)

- If tasks/specs changed and the index should reflect reality:
  - `/smartspec_sync_spec_tasks`

- If lifecycle transitions are needed:
  - `/smartspec_spec_lifecycle_manager`

---

## Best Practices

- Keep `.spec/SPEC_INDEX.json` as your canonical index.
- Use root `SPEC_INDEX.json` only as a legacy mirror.
- Run validation:
  - after adding/moving many specs
  - before major releases (`--mode=runtime`)
- For public/private setups, always supply:
  - `--workspace-roots` or `--repos-config`

---

## Troubleshooting

### “Validation shows many missing files but they exist in another repo”

Provide multi-repo configuration:

```bash
/smartspec_validate_index --workspace-roots="../PublicRepo,../PrivateRepo"
```

### “Health score is too harsh for early roadmap work”

Use portfolio mode:

```bash
/smartspec_validate_index --mode=portfolio
```

### “Root index is being updated unexpectedly”

Ensure your installation uses the v5.2 workflow and that you do not run legacy scripts that overwrite root mirrors.

---

## Summary

`/smartspec_validate_index` is the structural safety net of SmartSpec v5.2. It enforces index integrity with a practical, status-aware interpretation model, supports optional UI JSON governance, and can validate across sibling repositories so your reports match the real shape of your system.

