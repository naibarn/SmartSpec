---
description: Rebuild SPEC_INDEX from all specs with SmartSpec v5.2 centralization, multi-repo scanning, and UI JSON addendum awareness
version: 5.2
---

# /smartspec_reindex_specs

Rebuild (or regenerate) the project `SPEC_INDEX.json` by scanning all spec folders and consolidating metadata, while enforcing SmartSpec v5.2 centralization rules.

This version is **multi-repo-aware** to support ecosystems where specs are distributed across sibling repositories (e.g., public + private).

---

## Core Principles (v5.2)

- **Project-owned canonical space:** `.spec/`
- **Canonical index:** `.spec/SPEC_INDEX.json`
- **Legacy mirror (optional):** `SPEC_INDEX.json` at repo root
- **Deprecated tooling index:** `.smartspec/SPEC_INDEX.json` (read-only if present)
- **Shared registries (optional):** `.spec/registry/`
- **UI design source of truth (when applicable):** `ui.json` (Penpot-aligned)

This workflow **does not rewrite any `spec.md`**.

---

## What It Does

- Scans all specs under `specs/**/spec.md` across configured repo roots.
- Rebuilds a consistent `specs[]` list using your existing schema.
- Validates:
  - ID uniqueness
  - path correctness
  - category/status sanity
  - dependency integrity
- Detects UI specs via `ui.json` and category hints.
- Writes canonical index to `.spec/SPEC_INDEX.json`.
- Optionally updates legacy root mirror.
- Produces a reindex report under `.spec/reports/reindex-specs/`.

---

## When to Use

- After adding/removing multiple specs across repos.
- After reorganizing spec folders.
- When index counts or dependencies look inconsistent.
- Before major releases.

---

## Inputs

- Existing specs under `specs/**/` in one or multiple repos.
- Optional existing index for bootstrapping legacy fields.

---

## Outputs

- **Canonical:** `.spec/SPEC_INDEX.json`
- **Optional legacy mirror:** `SPEC_INDEX.json` (root)
- **Report:** `.spec/reports/reindex-specs/`

---

## Flags

### Index I/O

- `--index` Existing SPEC_INDEX path (optional)
  - default: auto-detect

- `--output-index` Path to write the rebuilt canonical index (optional)
  - default: `.spec/SPEC_INDEX.json`

- `--mirror-root` Also write/update `SPEC_INDEX.json` at repo root (optional)
  - default: `true` if a root mirror already exists, else `false`

### Multi-Repo Support

- `--workspace-roots`
  - Comma-separated list of additional repo roots to scan.
  - Example:
    - `--workspace-roots="../Smart-AI-Hub,../smart-ai-hub-enterprise-security"`

- `--repos-config`
  - Path to a JSON config describing known repos and aliases.
  - Recommended location:
    - `.spec/smartspec.repos.json`

  Example structure:

  ```json
  {
    "version": "1.0",
    "repos": [
      { "id": "public", "root": "../Smart-AI-Hub" },
      { "id": "private", "root": "../smart-ai-hub-enterprise-security" }
    ]
  }
  ```

### Reporting / Safety

- `--report-dir` Output report directory (optional)
  - default: `.spec/reports/reindex-specs/`

- `--strict` Fail on warnings (optional)

- `--dry-run` Print rebuilt index summary only (do not write files)

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
DRY_RUN="${FLAGS_dry_run:-false}"
```

---

## 1) Resolve Multi-Repo Scan Roots

This workflow may need to scan specs across multiple sibling repos.

Priority rules:

1) If `--repos-config` is provided and valid → use it.
2) Else if `--workspace-roots` is provided → use it.
3) Else → fallback to current repo root only.

Implementation intent:

- The scan roots are used **only for reading**.
- Index outputs are still written to the current repo’s `.spec/` unless you explicitly change `--output-index`.

---

## 2) Scan Specs Across Roots

### 2.1 Spec discovery

For each repo root in scan roots:

- Find all `specs/**/spec.md`.
- Record:
  - absolute file path (internal)
  - repo-relative folder path
  - inferred spec ID

### 2.2 Resolve canonical index `path` values

Compatibility-first rule:

- Your existing schema expects `path` to be repository-relative.
- In a multi-repo system, this workflow must **not break** the schema.

Therefore:

- Preserve the `path` exactly as found under each repo root’s internal structure:
  - e.g., `specs/core/spec-core-001-authentication/`

- Do **not** attempt to embed absolute paths into `path`.

- If you need explicit repo ownership later, handle it via optional metadata fields that do not break existing workflows (e.g., `repo_scope`) — but do not require them here.

---

## 3) Normalize and Validate

### 3.1 ID Uniqueness (Global)

- IDs must be unique across **all scanned roots**.
- If duplicates exist:
  - report them as errors
  - recommend explicit differentiation policy (e.g., public vs private aliasing)

### 3.2 Path Integrity

- Each index entry must point to a folder containing `spec.md` in at least one scanned root.

### 3.3 Category Sanity

- Categories should be consistent with your existing taxonomy.
- If a UI spec has `ui.json`, but category is not `ui`:
  - warn (or error in `--strict`).

### 3.4 Dependency Integrity

- Each dependency must reference a discovered spec ID.
- Warn on circular dependencies.

---

## 4) Preserve Schema Compatibility

When `INDEX_IN` exists:

- Use it to preserve fields required by production workflows.
- Do not change top-level schema shape.

Rules:

- Prefer newly scanned truth for:
  - `path`
  - `dependencies` (when clearly declared)
  - `category` when confidently inferred

---

## 5) Build Canonical Index

- Compose a new `SPEC_INDEX.json` compatible with your existing structure.
- Recompute counts.
- Ensure stable ordering where helpful (e.g., by category then ID).

Write to:

- `CANONICAL_OUT` (default `.spec/SPEC_INDEX.json`).

---

## 6) Optional Root Mirror Update

If `MIRROR_ROOT=true`:

- Write a mirror copy to `SPEC_INDEX.json`.

Rules:

- Root mirror is legacy.
- Write it **after** canonical output.

Never write `.smartspec/SPEC_INDEX.json`.

---

## 7) UI JSON Addendum (Index-Level Awareness)

This workflow does not validate UI JSON deeply, but must:

- Detect UI specs by:
  - category = `ui`, OR
  - `ui.json` presence in any scan root.

- Emit warnings when:
  - `ui.json` is missing for a declared UI spec.
  - category mismatches UI JSON presence.

If the project does not use UI JSON:

- Do not fail.
- Only warn when a spec explicitly declares itself as UI.

---

## 8) Report

Write a structured report to `REPORT_DIR` containing:

- Index input path used (if any)
- Canonical output path
- Scan roots used
- Spec counts by category/status
- Duplicate ID findings
- Missing path findings
- Dependency graph summary
- UI specs detected and category alignment

---

## 9) Recommended Follow-ups

- `/smartspec_validate_index --workspace-roots=...`
- `/smartspec_generate_plan`
- `/smartspec_generate_tasks`
- `/smartspec_sync_spec_tasks --mode=additive` (after review)

---

## Notes

- `.spec/SPEC_INDEX.json` is the canonical single source of truth for the current repo.
- This workflow can *read* specs across repos to rebuild a more accurate index without breaking your established schema.
- For public/private split strategies, use the portfolio/lifecycle workflows to add governance layers without schema breakage.

