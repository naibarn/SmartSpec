---
description: Validate SPEC_INDEX and enforce SmartSpec centralization + UI JSON addendum
version: 5.2
---

# /smartspec_validate_index

Validate the project SPEC_INDEX and its linked specs/registries to ensure consistency, prevent cross-SPEC drift, and enforce SmartSpec v5.2 centralization.

This workflow establishes a single, consistent interpretation of where canonical project truth lives:
- **`.spec/` is project-owned canonical space**
- **`.spec/SPEC_INDEX.json` is the canonical index**
- **`.spec/registry/` contains shared registries** used by all workflows
- `.smartspec/` is tooling-only and must not become a source of project truth

UI Design Addendum:
- When UI specs exist, **UI design source of truth is `ui.json`** to support Penpot workflows.

---

## What It Validates

1) SPEC_INDEX file integrity
2) Spec metadata consistency
3) Dependency graph correctness
4) Cross-SPEC namespace safety
5) Registry alignment (if registries exist)
6) UI JSON compliance (conditional)

---

## When to Use

- After adding/removing specs
- After running `/smartspec_reindex_specs`
- Before generating plans/tasks/tests at scale
- Before major releases

---

## Inputs

- Optional explicit index path
- Existing spec folders under `specs/**/`
- Optional registries under `.spec/registry/`

---

## Outputs

- Validation report (default: `.spec/reports/validate-index/`)
- Recommendations for corrective workflows

---

## Flags

- `--index` Path to SPEC_INDEX (optional)  
  default: auto-detect

- `--registry-dir` Registry directory (optional)  
  default: `.spec/registry`

- `--report-dir` Output report directory (optional)  
  default: `.spec/reports/validate-index/`

- `--strict` Fail on warnings (optional)

---

## 0) Resolve Canonical Index & Registry

### 0.1 Resolve SPEC_INDEX (Single Source of Truth)

Detection order:

1) `.spec/SPEC_INDEX.json` (canonical)  
2) `SPEC_INDEX.json` (legacy root mirror)  
3) `.smartspec/SPEC_INDEX.json` (deprecated)  
4) `specs/SPEC_INDEX.json` (older layout)

```bash
INDEX_PATH="${FLAGS_index:-}"

if [ -z "$INDEX_PATH" ]; then
  if [ -f ".spec/SPEC_INDEX.json" ]; then
    INDEX_PATH=".spec/SPEC_INDEX.json"
  elif [ -f "SPEC_INDEX.json" ]; then
    INDEX_PATH="SPEC_INDEX.json"
  elif [ -f ".smartspec/SPEC_INDEX.json" ]; then
    INDEX_PATH=".smartspec/SPEC_INDEX.json" # deprecated
  elif [ -f "specs/SPEC_INDEX.json" ]; then
    INDEX_PATH="specs/SPEC_INDEX.json"
  fi
fi

if [ -n "$INDEX_PATH" ] && [ -f "$INDEX_PATH" ]; then
  echo "✅ Using SPEC_INDEX: $INDEX_PATH"
else
  echo "❌ SPEC_INDEX not found. Validation cannot proceed."
  exit 1
fi
```

### 0.2 Resolve Registry Directory

```bash
REGISTRY_DIR="${FLAGS_registry_dir:-.spec/registry}"
REGISTRY_AVAILABLE=false

if [ -d "$REGISTRY_DIR" ]; then
  REGISTRY_AVAILABLE=true
fi

REPORT_DIR="${FLAGS_report_dir:-.spec/reports/validate-index}"
mkdir -p "$REPORT_DIR"

STRICT="${FLAGS_strict:-false}"
```

### 0.3 Expected Registries (if present)

- `api-registry.json`
- `data-model-registry.json`
- `glossary.json`
- `critical-sections-registry.json`
- `patterns-registry.json` (optional)
- `ui-component-registry.json` (optional)

Rules:
- Registries are authoritative for cross-SPEC shared names.
- If a registry exists, index + specs must not contradict it.

---

## 1) Load SPEC_INDEX

Validate JSON structure:
- Ensure required top-level fields exist per your established schema.
- Ensure `specs` list is present and an array.

Normalize for evaluation:
- Treat `path` as repository-relative.

---

## 2) Validate Spec Entries

For each spec entry:

- `id` must be unique.
- `path` must exist and contain `spec.md`.
- `category` must be a valid known category.
- `status` must be a known status label.

Cross-check with actual files:
- Folder existence
- `spec.md` existence

---

## 3) Validate Dependency Graph

- Each dependency must reference a valid `id`.
- Warn on:
  - missing dependencies
  - category violations (if your system has rules)
  - circular dependencies

If `--strict`:
- Treat circular dependencies as errors.

---

## 4) Cross-SPEC Namespace Safety

Detect potential conflicts across all indexed specs:

- API namespace overlaps (based on spec metadata or registry)
- Data model naming collisions
- Domain term collisions

Rules:
- If registries exist, they are the primary baseline.
- If registries do not exist, base conflicts on:
  - explicit spec declarations
  - tasks signals if available

Output:
- A conflict list with recommended remediation:
  - `/smartspec_sync_spec_tasks --mode=additive`
  - `/smartspec_refactor_code`
  - targeted spec repairs

---

## 5) Registry Alignment Checks (Conditional)

If `REGISTRY_AVAILABLE=true`:

- Validate that:
  - APIs referenced by multiple specs map to `api-registry.json`
  - Shared models map to `data-model-registry.json`
  - Shared terms map to `glossary.json`
  - Cross-cutting requirements map to `critical-sections-registry.json`

Rules:
- Do not auto-write registry changes in this workflow.
- Provide recommendations only.

---

## 6) UI JSON Addendum (Conditional)

Apply UI validation when **any** of these are true:

- A spec category is `ui` in SPEC_INDEX
- The spec folder contains `ui.json`

### 6.1 UI Source of Truth

- `ui.json` is the UI design artifact (Penpot-aligned).
- `spec.md` provides rules, constraints, and mapping notes.

### 6.2 Enforced Checks

For UI specs detected:

- Ensure `ui.json` exists (warn if missing).
- Ensure the index category is `ui` (warn if mismatched).
- If `ui-component-registry.json` exists:
  - ensure component names referenced in UI specs/tasks align.

### 6.3 Non-UI Projects

If the project does not use UI JSON:
- Do not fail.
- Skip these checks unless a UI spec is explicitly declared.

---

## 7) Legacy Compatibility Rules

- If both `.spec/SPEC_INDEX.json` and root `SPEC_INDEX.json` exist:
  - Treat `.spec/` as canonical.
  - Root is a mirror.
  - Warn if they diverge.

- If only root exists:
  - Validation proceeds.
  - Recommend migrating to `.spec/` canonical by running:
    - `/smartspec_reindex_specs`

- If `.smartspec/SPEC_INDEX.json` exists:
  - Mark as deprecated.
  - Recommend removal after canonical migration.

---

## 8) Report

Write a structured report into `REPORT_DIR` containing:

- Index path used
- Spec counts by category/status
- Missing/invalid paths
- Dependency findings
- Namespace conflict summary
- Registry alignment summary (if present)
- UI JSON compliance summary (if applicable)

---

## 9) Recommended Follow-ups

Depending on findings:

- `/smartspec_reindex_specs`
- `/smartspec_generate_spec --repair-legacy --repair-additive-meta`
- `/smartspec_sync_spec_tasks --mode=additive`
- `/smartspec_generate_plan`
- `/smartspec_generate_tasks`
- `/smartspec_generate_tests`

---

## Notes

- This workflow is the primary "gatekeeper" for SmartSpec centralization.
- It ensures all other workflows operate on a consistent canonical foundation.
- `.spec/registry/` remains the shared canonical truth when present.
- Root `SPEC_INDEX.json` is treated as legacy mirror.

