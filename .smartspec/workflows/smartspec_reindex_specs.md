---
description: Rebuild SPEC_INDEX from all specs with SmartSpec centralization (.spec) and UI JSON addendum awareness
version: 5.2
---

# /smartspec_reindex_specs

Rebuild (or regenerate) the project `SPEC_INDEX.json` by scanning all spec folders and consolidating metadata, while enforcing SmartSpec v5.2 centralization rules.

This workflow assumes:
- **`.spec/` is the canonical project-owned space** for shared truth.
- **`.spec/SPEC_INDEX.json` is the canonical index**.
- `SPEC_INDEX.json` at repo root is a **legacy mirror**.
- `.smartspec/SPEC_INDEX.json` is **deprecated** and must not be created for new projects.
- **`.spec/registry/`** may exist and is used for cross-SPEC naming reference.
- UI specs may have **`ui.json`** as the design source of truth.

---

## What It Does

- Scans all specs under `specs/**/spec.md`.
- Rebuilds a consistent `specs[]` list using your existing schema.
- Validates:
  - ID uniqueness
  - path correctness
  - category/status sanity
  - dependency integrity
- Detects UI specs via `ui.json` and category hints.
- Writes canonical index to `.spec/SPEC_INDEX.json`.
- Optionally updates legacy root mirror.
- Produces a reindex report under `.spec/reports/`.

---

## When to Use

- After adding/removing multiple specs.
- After reorganizing spec folders.
- When counts or dependencies look inconsistent.
- Before major releases.

---

## Inputs

- Existing specs under `specs/**/`.
- Optional existing index for bootstrapping legacy fields.

---

## Outputs

- **Canonical:** `.spec/SPEC_INDEX.json`
- **Optional legacy mirror:** `SPEC_INDEX.json` (root)
- Report: `.spec/reports/reindex-specs/`

---

## Flags

- `--index` Existing SPEC_INDEX path (optional)  
  default: auto-detect

- `--output-index` Path to write the rebuilt canonical index (optional)  
  default: `.spec/SPEC_INDEX.json`

- `--mirror-root` Also write/update `SPEC_INDEX.json` at repo root (optional)  
  default: `true` if a root mirror already exists, else `false`

- `--report-dir` Output report directory (optional)  
  default: `.spec/reports/reindex-specs/`

- `--strict` Fail on warnings (optional)

---

## 0) Resolve Index Paths (Single Source of Truth)

Detection order:

1) `.spec/SPEC_INDEX.json` (canonical)  
2) `SPEC_INDEX.json` (legacy root mirror)  
3) `.smartspec/SPEC_INDEX.json` (deprecated)  
4) `specs/SPEC_INDEX.json` (older layout)

```bash
INDEX_IN="${FLAGS_index:-}"

if [ -z "$INDEX_IN" ]; then
  if [ -f ".spec/SPEC_INDEX.json" ]; then
    INDEX_IN=".spec/SPEC_INDEX.json"
  elif [ -f "SPEC_INDEX.json" ]; then
    INDEX_IN="SPEC_INDEX.json"
  elif [ -f ".smartspec/SPEC_INDEX.json" ]; then
    INDEX_IN=".smartspec/SPEC_INDEX.json" # deprecated
  elif [ -f "specs/SPEC_INDEX.json" ]; then
    INDEX_IN="specs/SPEC_INDEX.json"
  fi
fi

CANONICAL_OUT="${FLAGS_output_index:-.spec/SPEC_INDEX.json}"

REPORT_DIR="${FLAGS_report_dir:-.spec/reports/reindex-specs}"
mkdir -p "$REPORT_DIR"
mkdir -p "$(dirname "$CANONICAL_OUT")"

MIRROR_ROOT_FLAG="${FLAGS_mirror_root:-}"
MIRROR_ROOT=false
if [ -n "$MIRROR_ROOT_FLAG" ]; then
  [ "$MIRROR_ROOT_FLAG" = "true" ] && MIRROR_ROOT=true || MIRROR_ROOT=false
else
  [ -f "SPEC_INDEX.json" ] && MIRROR_ROOT=true || MIRROR_ROOT=false
fi

STRICT="${FLAGS_strict:-false}"
```

---

## 1) Scan Specs

- Find all `spec.md` files under `specs/**/spec.md`.
- For each spec folder:
  - infer or read spec ID
  - read title/name
  - read category/status if present
  - read declared dependencies if present
  - detect UI marker if `ui.json` exists

Rules:
- The spec folder path becomes the authoritative `path` field.
- This workflow must **not rewrite any `spec.md`**.

---

## 2) Normalize and Validate

### 2.1 ID Uniqueness

- Fail if duplicated IDs are found.

### 2.2 Path Integrity

- Each index entry must point to an existing folder containing `spec.md`.

### 2.3 Category Sanity

- Categories should be consistent with your existing taxonomy.
- If a UI spec has `ui.json`, but category is not `ui`:
  - warn (or error in `--strict`).

### 2.4 Dependency Integrity

- Each dependency must reference a discovered spec ID.
- Warn on circular dependency chains.

---

## 3) Preserve Schema Compatibility

When `INDEX_IN` exists:
- Use it only to preserve fields that your production workflows already rely on.
- Do not change the overall top-level schema shape.

Rules:
- Prefer newly scanned truth for:
  - `path`
  - `dependencies`
  - `category` when confidently inferred

---

## 4) Build Canonical Index

- Compose a new `SPEC_INDEX.json` compatible with your existing structure.
- Recompute counts.
- Ensure stable ordering where helpful (e.g., by category then ID).

Write to:
- `CANONICAL_OUT` (default `.spec/SPEC_INDEX.json`).

---

## 5) Optional Root Mirror Update

If `MIRROR_ROOT=true`:
- Write a mirror copy to `SPEC_INDEX.json`.

Rules:
- The root mirror must be treated as **legacy**.
- Warn if root mirror diverged from canonical in previous versions.

Do NOT write `.smartspec/SPEC_INDEX.json`.

---

## 6) UI JSON Addendum (Index-Level Awareness)

This workflow does not validate UI JSON deeply, but must:

- Detect UI specs by:
  - category = `ui`, OR
  - `ui.json` presence.

- Emit warnings when:
  - `ui.json` is missing for a declared UI spec.
  - category mismatches UI JSON presence.

- Ensure the index entry remains compatible with the UI team workflow.

If the project does not use UI JSON:
- Do not fail.
- Only warn when a spec explicitly declares itself as UI.

---

## 7) Report

Write a structured report to `REPORT_DIR` containing:

- Index input path used (if any)
- Canonical output path
- Spec counts by category/status
- Duplicate ID findings
- Missing path findings
- Dependency graph summary
- UI specs detected and category alignment

---

## 8) Recommended Follow-ups

- `/smartspec_validate_index`
- `/smartspec_generate_plan`
- `/smartspec_generate_tasks`
- `/smartspec_sync_spec_tasks --mode=additive` (after review)

---

## Notes

- `.spec/SPEC_INDEX.json` is the canonical single source of truth.
- Root `SPEC_INDEX.json` is a legacy mirror for backward compatibility.
- This workflow is safe for large projects and prevents index drift.

