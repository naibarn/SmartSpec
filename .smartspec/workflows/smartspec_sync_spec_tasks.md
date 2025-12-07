---
description: Sync spec metadata and tasks into canonical index/registries with SmartSpec v5.2 centralization and UI JSON addendum
version: 5.2
---

# /smartspec_sync_spec_tasks

Synchronize spec metadata and task-derived signals into the **canonical SmartSpec centralized layer** to keep large projects consistent and conflict-resistant.

This workflow enforces SmartSpec v5.2 centralization:
- **`.spec/` is the canonical project-owned space** for shared truth.
- **`.spec/SPEC_INDEX.json` is the canonical index**.
- **`.spec/registry/` is the shared source of truth** for cross-SPEC names.
- `SPEC_INDEX.json` at repo root is a **legacy mirror**.
- `.smartspec/` is tooling-only.
- **UI specs use `ui.json` as the design source of truth** for Penpot integration.

---

## What It Does

- Resolves canonical index and registry locations.
- Reads one or more target specs and their adjacent `tasks.md`.
- Updates safe, non-destructive fields in the canonical index.
- Validates and aligns shared names using registries (if present).
- Produces recommendations or append-only registry updates depending on mode.
- Applies UI JSON addendum rules conditionally.
- Optionally updates the legacy root mirror after canonical updates.

---

## When to Use

- After generating or updating `tasks.md`.
- When multiple teams are working across many specs.
- After finishing a milestone and you want index/registry truth to reflect reality.
- During migration to v5.2 centralization.

---

## Inputs

- Target spec path (recommended)
  - Example: `specs/core/spec-core-004-rate-limiting/spec.md`

- Expected adjacent files:
  - `tasks.md`
  - (UI specs) `ui.json`

- Optional existing index/registries.

---

## Outputs

- **Canonical index updates:** `.spec/SPEC_INDEX.json`
- **Optional legacy mirror updates:** `SPEC_INDEX.json` (root)
- **Registry recommendations or additive updates** under `.spec/registry/`
- Sync report under `.spec/reports/sync-spec-tasks/`

---

## Flags

### Index / Registry

- `--index` Path to SPEC_INDEX (optional)  
  default: auto-detect

- `--registry-dir` Registry directory (optional)  
  default: `.spec/registry`

### Target Selection

- `--spec` Explicit spec path (optional)

- `--spec-ids` Comma-separated spec IDs (optional, requires index)

### Sync Behavior

- `--mode` `recommend` | `additive`  
  default: `recommend`

- `--mirror-root` `true|false`  
  default: `true` if a root mirror already exists, else `false`

### Safety

- `--strict` Fail on ambiguous conflicts (optional)

- `--dry-run` Print planned changes only (do not write files)

---

## 0) Resolve Canonical Index & Registry

### 0.1 Resolve SPEC_INDEX (Single Source of Truth)

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

CANONICAL_OUT=".spec/SPEC_INDEX.json"
mkdir -p ".spec"

if [ -n "$INDEX_IN" ] && [ -f "$INDEX_IN" ]; then
  echo "✅ Using SPEC_INDEX input: $INDEX_IN"
else
  echo "⚠️ SPEC_INDEX not found. A canonical index may be bootstrapped in additive migration flows."
  INDEX_IN=""
fi

REGISTRY_DIR="${FLAGS_registry_dir:-.spec/registry}"
mkdir -p "$REGISTRY_DIR"

MODE="${FLAGS_mode:-recommend}"
STRICT="${FLAGS_strict:-false}"
DRY_RUN="${FLAGS_dry_run:-false}"

MIRROR_ROOT_FLAG="${FLAGS_mirror_root:-}"
MIRROR_ROOT=false
if [ -n "$MIRROR_ROOT_FLAG" ]; then
  [ "$MIRROR_ROOT_FLAG" = "true" ] && MIRROR_ROOT=true || MIRROR_ROOT=false
else
  [ -f "SPEC_INDEX.json" ] && MIRROR_ROOT=true || MIRROR_ROOT=false
fi

REPORT_DIR=".spec/reports/sync-spec-tasks"
mkdir -p "$REPORT_DIR"
```

### 0.2 Expected Registries (if present)

- `api-registry.json`
- `data-model-registry.json`
- `glossary.json`
- `critical-sections-registry.json`
- `patterns-registry.json` (optional)
- `ui-component-registry.json` (optional)

Registry rules:
- Treat existing registry entries as canonical shared names.
- Do not rename or delete entries automatically.
- In `additive` mode, allow **append-only** updates with clear evidence from specs.

---

## 1) Identify Target Spec(s)

Priority:

1) `--spec` if provided.
2) `--spec-ids` if provided and `INDEX_IN` exists.
3) If index exists, allow selecting by category or dependency chain.
4) Otherwise, require a spec path.

Default tasks location:
- `tasks.md` next to `spec.md`.

---

## 2) Read Inputs (Read-Only)

For each target spec:

- Read `spec.md`.
- Read `tasks.md` if present.
- Detect `ui.json` (if present).

Extract syncable signals:
- Spec ID/title/category cues
- Dependency references
- Status hints from tasks (planned/in-progress/done)
- Shared APIs/models/terms referenced
- Cross-cutting requirements

This workflow must not rewrite `spec.md` or `tasks.md`.

---

## 3) Consistency Gate Before Sync

### 3.1 Index vs Local Spec

If `INDEX_IN` exists:
- Ensure the target spec path and ID align.
- Ensure dependency lists do not conflict.

If conflicts exist:
- In `--strict` mode: stop.
- Otherwise: record a reconciliation recommendation.

### 3.2 Registry vs Local Usage

If registry files exist:
- Validate that shared names referenced in specs/tasks match registries.

If conflicts exist:
- Prefer updating local code/tasks/spec usage to match registry.
- Do not auto-rename registry entries.

---

## 4) Update Canonical Index (Safe Fields)

Write updates to `CANONICAL_OUT` using your existing schema.

Safe updates include:

- `path` normalization
- `dependencies` alignment (when clear)
- `category` correction (only when confidently inferred)
- `status` updates when tasks indicate stable completion evidence
- Count recomputation

Rules:
- The canonical index must remain backward compatible with your existing workflow ecosystem.
- Do not introduce schema-breaking fields.

If `INDEX_IN` is empty:
- Bootstrapping behavior should be minimal and conservative.
- Recommend running `/smartspec_reindex_specs` for a full rebuild.

---

## 5) Registry Alignment

### 5.1 Recommend Mode (default)

- Do not write registries.
- Output:
  - missing APIs/models/terms
  - suggested canonical names
  - mismatch warnings

### 5.2 Additive Mode

- Append missing entries only when:
  - the spec clearly declares them as shared
  - multiple specs reference them, or
  - the index classifies them as cross-cutting

Never:
- delete entries
- rename entries
- auto-merge conflicting definitions

---

## 6) UI JSON Addendum (Conditional)

Apply when **any** of these are true:

- Spec category is `ui` in the index
- The spec folder contains `ui.json`
- The spec explicitly mentions Penpot/UI JSON workflow

Rules:

1) **UI design source of truth is JSON** (`ui.json`).
2) Treat `ui.json` as design-owned.
3) Do not embed business logic in UI JSON.
4) `spec.md` and `tasks.md` may reference UI nodes/components but must not contradict `ui.json`.

Checks:

- If `ui.json` exists:
  - ensure index category is `ui` (warn if not)
- If `ui-component-registry.json` exists:
  - verify component names used in UI specs/tasks align
- If UI JSON is missing for a declared UI spec:
  - warn and recommend creation

Non-UI projects:
- Do not fail.
- Skip UI checks unless a spec explicitly declares itself as UI.

---

## 7) Optional Root Mirror Update

If `MIRROR_ROOT=true`:

- After writing canonical index, write a mirror copy to `SPEC_INDEX.json`.
- Record in report that root index is legacy.

Do NOT write `.smartspec/SPEC_INDEX.json`.

---

## 8) Reporting

Write a structured report in `REPORT_DIR` including:

- Index input path used
- Canonical output path
- Mirror policy
- Specs processed
- Safe fields updated
- Registry recommendations/changes (by mode)
- UI JSON compliance summary (if applicable)
- Follow-up recommendations

---

## 9) Recommended Follow-ups

- `/smartspec_validate_index`
- `/smartspec_generate_plan`
- `/smartspec_generate_tasks`
- `/smartspec_generate_tests`
- `/smartspec_verify_tasks_progress`
- `/smartspec_reindex_specs` (when large-scale structural changes occurred)

---

## Notes

- This workflow is the primary "bridge" between working specs/tasks and the centralized truth.
- It is intentionally conservative to avoid cross-team conflicts.
- `.spec/SPEC_INDEX.json` remains the canonical single source of truth.
- Root `SPEC_INDEX.json` is maintained as a legacy mirror only when needed.

