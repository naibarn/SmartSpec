---
description: Rebuild or refresh SPEC_INDEX with SmartSpec v5.6 centralization, multi-repo resolution, and optional multi-registry readiness checks
version: 5.6
---

# /smartspec_reindex_specs

Reindex all SmartSpec specifications and rebuild the project’s SPEC_INDEX in a way that is compatible with the v5.6 chain:

1) `/smartspec_validate_index`  
2) `/smartspec_generate_spec`  
3) `/smartspec_generate_plan`  
4) `/smartspec_generate_tasks`  
5) `/smartspec_sync_spec_tasks`

This workflow **preserves all essential v5.2 reindex capabilities**, including multi-root scanning, safe schema handling, and legacy mirror support, while adding:

- Optional **multi-registry readiness checks**
- Optional **repo hint enrichment**
- A consistent flag surface with other v5.6 workflows

---

## Core Principles (Unchanged)

- **`.spec/` is the canonical project-owned space**.
- **`.spec/SPEC_INDEX.json` is the canonical index** when present.
- Root `SPEC_INDEX.json` may be maintained as a **legacy mirror**.
- `.smartspec/` is tooling-only.
- The reindexer must remain schema-compatible with existing downstream tools.

---

## New v5.6 Goals

1) Ensure the index is sufficient for stable `generate_spec` and `generate_tasks` output.
2) Support multi-repo portfolios without creating ambiguous ownership.
3) Provide early detection of cross-repo naming drift via optional registry awareness.
4) Avoid any destructive behavior to specs or registries.

---

## What It Does

- Scans one or more spec roots.
- Builds or refreshes a unified SPEC_INDEX.
- Preserves stable spec IDs and categories.
- Updates safe metadata such as:
  - paths
  - dependency lists (when clearly declared)
  - status (when policy allows)
  - timestamps
- Optionally validates multi-repo mapping integrity when configured.
- Optionally emits registry readiness warnings.
- Writes canonical index to `.spec/SPEC_INDEX.json`.
- Optionally writes/updates the legacy root mirror.

---

## When to Use

- First-time SmartSpec setup.
- After adding many new specs.
- After major folder restructuring.
- Before adopting multi-repo governance.
- When index mismatches or missing entries are suspected.

---

## Inputs

- Spec roots (default or provided)
- Existing index files (optional)
- Optional multi-repo configuration
- Optional registry directories (validation-only)

---

## Outputs

- `.spec/SPEC_INDEX.json` (canonical)
- `SPEC_INDEX.json` (legacy mirror, optional)
- Report under:
  - `.spec/reports/reindex-specs/`

---

## Flags

### Index Targets

- `--out=<path>`
  - Output path for the generated index.
  - Default: `.spec/SPEC_INDEX.json`

- `--mirror-root=<true|false>`
  - Write a mirror copy to root `SPEC_INDEX.json`.
  - Default: `true` if a legacy mirror already exists, else `false`.

### Spec Discovery

- `--roots=<csv>`
  - Comma-separated list of spec roots to scan.
  - Default: `specs/` (and any legacy roots your project supports).

- `--include-drafts=<true|false>`
  - Include draft specs in the index.

### Multi-Repo Resolution (v5.6-aligned)

- `--workspace-roots=<csv>`
  - Additional repo roots to scan for specs.
  - Use when specs are distributed across sibling repos.

- `--repos-config=<path>`
  - JSON config mapping repo IDs to physical roots.
  - Takes precedence over `--workspace-roots`.
  - Recommended path: `.spec/smartspec.repos.json`

- `--specindex=<path>`
  - Legacy alias for `--index` in workflows that accept it.
  - For reindex, this flag may be accepted only as an input hint (implementation choice).

### Optional Multi-Registry Readiness (NEW)

> Reindex remains index-focused. Registry checks are **warning-only** by default.

- `--registry-dir=<path>`
  - Primary registry directory (authoritative for naming in other workflows).
  - Default: `.spec/registry` when present.

- `--registry-roots=<csv>`
  - Supplemental registries for read-only validation.
  - Useful in multi-repo platforms.

Behavior:
- Load registries to inform **index-level warnings** only.
- Do not write registries in this workflow.

### Optional Repo Hint Enrichment (NEW, Non-Breaking)

- `--emit-repo-hints=<true|false>`
  - When enabled, the reindexer may infer a lightweight `repo` hint for each spec entry
    based on which root it was discovered in.

Rules:
- Must remain backward compatible.
- If your current index schema already supports a `repo` field, populate it.
- If not, emit repo hints **only in the report**.

### Safety & Output

- `--fix` (if supported in your legacy implementation)
  - Apply safe normalization to index metadata.

- `--report=<summary|detailed>`

- `--dry-run`
  - Print output without writing files.

---

## 0) Resolve Multi-Repo Search Roots

Construct the spec discovery roots in this order:

1) Current repo root
2) `--repos-config` roots (if provided)
3) `--workspace-roots` (if provided)
4) `--roots` spec directories under each repo root

If `--repos-config` is provided:

- Validate that it is parseable.
- Record repo IDs and roots in the report.

---

## 1) Discover Specs

For each resolved repo root:

- Scan for `spec.md` files under the configured spec roots.
- Support legacy folder patterns when they exist.

Rules:
- Never modify spec contents.
- Keep discovery deterministic (stable ordering).

---

## 2) Build Index Entries

For each discovered spec:

- Extract stable metadata:
  - id (from front-matter if present, else derived per legacy rules)
  - title
  - category
  - status
  - dependencies (declared)
  - path

- Prefer the spec’s own explicit dependency declarations.
- When ambiguous, avoid inferring cross-cutting dependencies.

---

## 3) Duplicate & Conflict Checks

Detect and report:

- Duplicate spec IDs
- Multiple specs claiming the same stable path
- Category conflicts

Severity handling (consistent with validate chain):

- In single-repo usage, these are typically blocking for reindex output.
- In multi-repo usage, duplicate IDs across repos must be treated as high-severity.

---

## 4) Optional Registry Readiness Warnings

If `--registry-dir` or `--registry-roots` are provided:

- Load read-only registry views.
- Emit warnings if:
  - index contains multiple specs that appear to define the same shared API/model/term family
    without clear ownership hints.
  - a spec category implies shared UI components but no UI registry is available.

This step must remain **warning-only** to avoid turning reindex into a heavy governance gate.

---

## 5) Write Canonical Index

Default output:

- `.spec/SPEC_INDEX.json`

Rules:
- Preserve schema stability.
- Do not introduce breaking fields.
- If `repo` is a supported field in your schema:
  - populate only when `--emit-repo-hints=true`.

---

## 6) Optional Root Mirror

If `--mirror-root=true`:

- Write a mirror copy to `SPEC_INDEX.json`.
- Mark in the report that the root index is a legacy mirror.

Do NOT write `.smartspec/SPEC_INDEX.json`.

---

## 7) Reporting

Write a report in `.spec/reports/reindex-specs/` including:

- Canonical output path used
- Mirror policy
- Repo roots scanned
- Spec roots scanned
- Duplicate ID/path findings
- Optional repo hint summary
- Optional registry readiness warnings
- Recommended next steps:
  - `/smartspec_validate_index`
  - `/smartspec_generate_spec`
  - `/smartspec_generate_plan`
  - `/smartspec_generate_tasks`

---

## Notes

- This v5.6 reindex workflow is intentionally conservative.
- It supports multi-repo discovery without forcing a single unified registry strategy.
- Registry flags are included to surface early warnings, not to enforce ownership changes.
- The primary governance gates remain:
  - `/smartspec_validate_index v5.6 alignment`
  - `/smartspec_generate_spec v5.6`
  - `/smartspec_generate_tasks v5.6`

