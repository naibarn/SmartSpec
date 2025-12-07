---
description: Generate or repair SmartSpec spec with v5.2 centralization (.spec) and UI JSON addendum
version: 5.2
---

# /smartspec_generate_spec

Create a new `spec.md` or repair an existing one while enforcing SmartSpec v5.2 centralization and preventing cross-SPEC conflicts.

This workflow assumes:
- **`.spec/` is the canonical project-owned space**.
- **`.spec/SPEC_INDEX.json` is the canonical index** when available.
- **`.spec/registry/` is the shared source of truth** for cross-SPEC names.
- `.smartspec/` is tooling-only.
- **UI specs use `ui.json` as design source of truth** to support Penpot-based collaboration.

This workflow is compatible with the existing `SPEC_INDEX.json` schema already used in production and aims to preserve legacy behavior while introducing centralization upgrades.

---

## What It Does

Depending on mode, this workflow will:

1) Resolve canonical index and registry paths.
2) Read existing spec context and dependencies.
3) Generate a new `spec.md` (when creating a new spec).
4) Or **repair a legacy spec** without breaking existing content.
5) Extract cross-SPEC entities (APIs, models, terms, critical sections, patterns, UI components) to **recommend** or **additively update** registries.
6) Ensure UI JSON addendum rules are respected when UI specs exist.

---

## When to Use

- Creating a new spec under `specs/**/`.
- Migrating a project to v5.2 centralization.
- Repairing legacy specs that predate `.spec/registry`.
- Harmonizing naming across multiple teams/specs.

---

## Inputs

- Target spec path (recommended)
  - Example: `specs/core/spec-core-004-rate-limiting/spec.md`

- Optional context files:
  - `plan.md`
  - `tasks.md`
  - dependency specs

- (UI specs) `ui.json`

---

## Outputs

- A new or updated `spec.md` (depending on mode).
- Centralization companion files (when allowed):
  - `.spec/SPEC_INDEX.json` (if missing and creation is required by migration flows)
  - `.spec/registry/*.json` (recommendations by default)
  - Reports under `.spec/reports/`

---

## Flags

### Index / Registry

- `--index` Path to SPEC_INDEX (optional)  
  default: auto-detect

- `--registry-dir` Registry directory (optional)  
  default: `.spec/registry`

### Generation / Repair Modes

- `--new` Force new spec generation (optional)

- `--repair-legacy`  
  Read an existing `spec.md` as read-only and **generate missing companion centralization artifacts** as needed.  
  Must not remove or rewrite core legacy content.

- `--repair-additive-meta`  
  Allows adding new, clearly marked metadata sections to `spec.md` when necessary for v5.2 compatibility.  
  Must not change the meaning of existing sections.

- `--mode` `recommend` | `additive`  
  Controls whether registries receive only recommendations or safe append-only updates.  
  default: `recommend`

### Safety

- `--strict` Fail on unresolved cross-SPEC conflicts (optional)

- `--dry-run` Print output only (do not write files)

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
  echo "⚠️ SPEC_INDEX not found. Generation may proceed in local-only mode."
  INDEX_PATH=""
fi
```

### 0.2 Resolve Registry Directory

```bash
REGISTRY_DIR="${FLAGS_registry_dir:-.spec/registry}"
mkdir -p "$REGISTRY_DIR"

MODE="${FLAGS_mode:-recommend}"
REPAIR_LEGACY="${FLAGS_repair_legacy:-false}"
REPAIR_ADDITIVE_META="${FLAGS_repair_additive_meta:-false}"
STRICT="${FLAGS_strict:-false}"
DRY_RUN="${FLAGS_dry_run:-false}"
```

### 0.3 Expected Registries (if present)

- `api-registry.json`
- `data-model-registry.json`
- `glossary.json`
- `critical-sections-registry.json`
- `patterns-registry.json` (optional)
- `ui-component-registry.json` (optional)

Registry rules:
- Treat registry entries as canonical shared names.
- Prefer aligning new specs to registry rather than introducing new shared names.
- In `additive` mode, allow **append-only** updates with clear evidence from specs.

---

## 1) Identify Target Spec

- Validate the spec path.
- Determine spec folder root.

If creating a new spec:
- Ensure the spec ID does not already exist in the index.
- Confirm category and naming conventions.

---

## 2) Load Existing Context

When `INDEX_PATH` is available:
- Load:
  - existing spec entry (if present)
  - dependencies
  - related categories

When registries exist:
- Load relevant slices of:
  - APIs
  - models
  - terms
  - critical sections
  - patterns

---

## 3) Read Legacy Spec (if present)

If `spec.md` exists and `--repair-legacy` is enabled:

- Treat the file as read-only.
- Extract:
  - core requirements
  - non-functional constraints
  - declared APIs/models/terms
  - implied dependencies
  - UI notes

No destructive edits are allowed.

If `--repair-additive-meta` is also enabled:
- You may add new metadata blocks that do not modify existing meaning.
- The added block should be clearly labeled, e.g.,
  - "v5.2 Centralization Additive Metadata"

---

## 4) Cross-SPEC Consistency Gate

### 4.1 Index Consistency

If `INDEX_PATH` exists:
- Ensure the target spec ID and path align with index expectations.
- Ensure dependencies referenced in the spec match the index graph.

### 4.2 Registry Consistency

If registries exist:
- Validate that APIs/models/terms used in the spec are either:
  - already registered, or
  - explicitly local-only.

If a conflict exists:
- In `--strict` mode: stop.
- Otherwise: generate a resolution recommendation.

---

## 5) Generate or Repair Spec Content

### 5.1 New Spec Generation

When creating a new `spec.md`:

Include consistent sections aligned with your existing schema usage:

- Overview
- Goals & Non-Goals
- Scope
- Dependencies
- Functional Requirements
- Non-Functional Requirements
- Data Models
- API Contracts
- Security Considerations
- Observability
- Testing Strategy
- Migration / Backward Compatibility (when relevant)
- UI Section (conditional)

### 5.2 Legacy Repair

With `--repair-legacy`:

- Do not rewrite core narrative sections.
- Only:
  - add missing headers if necessary
  - add a new additive metadata section (only if `--repair-additive-meta`)
  - generate companion centralization artifacts outside `spec.md`

---

## 6) Centralization Companion Artifacts

### 6.1 Index Presence

This workflow does not fully rebuild the index.

If no index exists:
- Recommend running `/smartspec_reindex_specs`.
- In migration scenarios, you may create a minimal `.spec/SPEC_INDEX.json` stub only when required by your system policy.

### 6.2 Registry Updates

Extract discovered entities from the spec:
- APIs
- Models
- Terms
- Critical sections
- Patterns
- UI components (if applicable)

Mode behavior:

- `recommend` (default):
  - Do not write registries.
  - Output suggested additions.

- `additive`:
  - Append missing entries only.
  - Never delete or rename existing entries automatically.

---

## 7) UI JSON Addendum (Conditional)

Apply when **any** of these are true:
- The spec category is `ui` in the index.
- The spec folder contains `ui.json`.
- The spec explicitly mentions Penpot/UI JSON workflow.

Rules:

1) **UI design source of truth is JSON** (`ui.json`).
2) `ui.json` should contain:
   - layout structure
   - component mapping metadata
   - design tokens references
   - props hints
3) **No business logic in UI JSON**.
4) `spec.md` should:
   - explain component responsibilities
   - document logic boundaries
   - link to `ui.json`

### 7.1 Repair Behavior for UI

If `--repair-legacy` and the UI spec lacks `ui.json`:
- Do not fail.
- Recommend creating `ui.json`.
- If your project policy allows additive file creation in repair mode:
  - create a minimal placeholder `ui.json` only when explicitly requested by the user or when your automation rules allow it.

### 7.2 UI Component Registry

If `ui-component-registry.json` exists:
- Prefer component names from registry.
- List any missing components under recommendations.

### 7.3 Non-UI Projects

If the project does not use UI JSON:
- Do not fail.
- Keep UI-related content inside `spec.md`.
- Recommend future adoption only if beneficial.

---

## 8) Output & Reporting

Default report directory:
- `.spec/reports/generate-spec/`

Include:
- Index path used
- Registries detected
- Extracted entities summary
- Conflict warnings
- UI JSON compliance notes (if applicable)
- Recommended follow-up workflows

---

## 9) Recommended Follow-ups

- `/smartspec_validate_index`
- `/smartspec_reindex_specs`
- `/smartspec_generate_plan`
- `/smartspec_generate_tasks`
- `/smartspec_generate_tests`
- `/smartspec_sync_spec_tasks --mode=additive`

---

## Notes

- This workflow preserves compatibility with your existing SPEC_INDEX-driven pipeline.
- The goal is to introduce centralization **without breaking legacy working behavior**.
- `.spec/registry/` is the shared canonical truth when present.
- Root `SPEC_INDEX.json` remains a legacy mirror.

