---
description: Sync spec metadata and task-derived signals into canonical index/registries with SmartSpec v5.6 centralization, UI mode alignment, and multi-repo/multi-registry safety
version: 5.6
---

# /smartspec_sync_spec_tasks

Synchronize spec metadata and task-derived signals into the **canonical SmartSpec centralized layer** to keep large projects consistent, conflict-resistant, and aligned with the v5.6 chain:

1) `/smartspec_validate_index`  
2) `/smartspec_generate_spec`  
3) `/smartspec_generate_tasks`  
4) `/smartspec_sync_spec_tasks`

This workflow preserves all essential v5.2 behaviors while adding **multi-repo** and **multi-registry** awareness so that synchronization does not accidentally:

- infer incomplete ownership,
- create duplicate shared entries,
- or drift from cross-repo governance.

---

## Core Principles (v5.6)

- **`.spec/` is the canonical project-owned space** for shared truth.
- **`.spec/SPEC_INDEX.json` is the canonical index**.
- **`.spec/registry/` is the shared source of truth** for cross-SPEC names.
- `SPEC_INDEX.json` at repo root is a **legacy mirror**.
- `.smartspec/` is tooling-only.

UI alignment:

- UI specs may use `ui.json` as the design source of truth.
- v5.6 sync respects the resolved UI expectations from the spec/tasks chain.

Multi-repo alignment:

- Specs may be distributed across sibling repos.
- Index logical `repo` fields must be resolvable when `--repos-config` is provided.

Multi-registry alignment:

- A primary registry remains authoritative.
- Supplemental registries may be loaded read-only to prevent cross-repo duplication.

---

## What It Does

- Resolves canonical index and registry locations.
- Builds a multi-repo and multi-registry resolution context (when configured).
- Reads one or more target specs and their adjacent `tasks.md`.
- Updates safe, non-destructive fields in the canonical index.
- Validates and aligns shared names using registry views (if present).
- Produces recommendations or append-only registry updates depending on mode.
- Applies UI alignment rules conditionally.
- Optionally updates the legacy root mirror after canonical updates.

---

## When to Use

- After generating or updating `tasks.md`.
- When multiple teams are working across many specs.
- After finishing a milestone and you want index/registry truth to reflect reality.
- During migration to v5.6 chain governance.

---

## Inputs

- Target spec path (recommended)
  - Example: `specs/core/spec-core-004-rate-limiting/spec.md`

- Expected adjacent files:
  - `tasks.md`
  - (UI specs) optionally `ui.json`

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

- `--specindex` Legacy alias for `--index` (optional)

- `--registry-dir` Primary registry directory (optional)  
  default: `.spec/registry`

- `--registry-roots` Comma-separated list of supplemental registry directories (optional)
  - Loaded **read-only** for cross-repo validation.
  - Example:
    - `--registry-roots="../Repo-A/.spec/registry,../Repo-B/.spec/registry"`

### Multi-Repo Support (NEW)

- `--workspace-roots`
  - Comma-separated list of additional repo roots to search for referenced specs.

- `--repos-config`
  - Path to a JSON config mapping repo IDs to physical roots.
  - Takes precedence over `--workspace-roots`.
  - Recommended location: `.spec/smartspec.repos.json`

### Target Selection

- `--spec` Explicit spec path (optional)

- `--spec-ids` Comma-separated spec IDs (optional, requires index)

### Sync Behavior

- `--mode` `recommend` | `additive`  
  default: `recommend`

- `--mirror-root` `true|false`  
  default: `true` if a root mirror already exists, else `false`

### Safety

- `--safety-mode=<strict|dev>` (NEW, optional)
  - `strict` (default): fail on ambiguous cross-SPEC/cross-repo conflicts that could cause duplicate shared entries.
  - `dev`: continue but emit high-visibility warnings.

- `--strict` Legacy boolean alias for strict gating (optional)

- `--dry-run` Print planned changes only (do not write files)

---

## 0) Resolve Canonical Index, Registries, and Multi-Repo Roots

### 0.1 Resolve SPEC_INDEX (Single Source of Truth)

Detection order:

1) `.spec/SPEC_INDEX.json` (canonical)  
2) `SPEC_INDEX.json` (legacy root mirror)  
3) `.smartspec/SPEC_INDEX.json` (deprecated)  
4) `specs/SPEC_INDEX.json` (older layout)

```bash
INDEX_IN="${FLAGS_index:-${FLAGS_specindex:-}}"

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
  echo "⚠️ SPEC_INDEX not found. Sync will run in local-only mode and may recommend reindexing."
  INDEX_IN=""
fi
```

### 0.2 Resolve Primary Registry Directory

```bash
REGISTRY_DIR="${FLAGS_registry_dir:-.spec/registry}"
mkdir -p "$REGISTRY_DIR"
```

### 0.3 Resolve Supplemental Registry Roots (NEW)

```bash
REGISTRY_ROOTS_RAW="${FLAGS_registry_roots:-}"
# Parse CSV in implementation
```

Registry precedence:

1) **Primary registry** (`--registry-dir`) is authoritative.
2) **Supplemental registries** (`--registry-roots`) are read-only validation sources.

### 0.4 Expected Registries (if present)

- `api-registry.json`
- `data-model-registry.json`
- `glossary.json`
- `critical-sections-registry.json`
- `patterns-registry.json` (optional)
- `ui-component-registry.json` (optional)
- `file-ownership-registry.json` (optional, recommended)

Registry rules:

- Treat existing registry entries as canonical shared names.
- Do not rename or delete entries automatically.
- In `additive` mode, allow **append-only** updates with clear evidence from specs/tasks.
- When an entity exists only in a supplemental registry, default to **reuse** semantics.

### 0.5 Resolve Multi-Repo Search Roots (NEW)

Two ways to configure:

1) `--workspace-roots` (simple list)
2) `--repos-config` (structured mapping; takes precedence)

If neither is provided:

- The workflow resolves only within the current repo root.

If `--repos-config` is provided and the index uses `repo:` labels:

- Validate that every `repo` label used by target specs has a corresponding mapping.
- In strict safety mode, treat missing mappings as blocking warnings.

---

## 1) Identify Target Spec(s)

Priority:

1) `--spec` if provided.
2) `--spec-ids` if provided and `INDEX_IN` exists.
3) If index exists, allow selecting by category or dependency chain (implementation-specific).
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
- Task-level ownership/reuse hints

This workflow must not rewrite `spec.md` or `tasks.md`.

---

## 3) Consistency Gate Before Sync

### 3.1 Index vs Local Spec

If `INDEX_IN` exists:

- Ensure the target spec path and ID align.
- Ensure dependency lists do not conflict.

If conflicts exist:

- In strict safety mode (`--safety-mode=strict` or `--strict=true`): stop.
- Otherwise: record a reconciliation recommendation.

### 3.2 Registry View vs Local Usage (Multi-Registry Aware)

If registry files exist:

- Validate that shared names referenced in specs/tasks match registries.
- Check for name collisions across supplemental registries.

Rules:

- Prefer updating local usage to match registry.
- Do not auto-rename registry entries.
- In strict safety mode, do not add new shared entries when a conflicting name exists in any loaded registry view.

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
  - cross-repo reuse risk notes (when supplemental registries indicate existing owners)

### 5.2 Additive Mode

- Append missing entries only when:
  - the spec clearly declares them as shared
  - multiple specs reference them, or
  - the index classifies them as cross-cutting

Never:

- delete entries
- rename entries
- auto-merge conflicting definitions

Multi-registry safeguard:

- If an equivalent or conflicting entry exists in any supplemental registry, default to **recommend-only** even if `--mode=additive`.

---

## 6) UI Alignment (Conditional)

Apply when **any** of these are true:

- Spec category is `ui` in the index
- The spec folder contains `ui.json`
- The spec explicitly mentions Penpot/UI JSON workflow

Rules:

1) UI design source of truth may be JSON (`ui.json`) when the spec resolves to JSON mode.
2) Treat `ui.json` as design-owned.
3) Do not embed business logic in UI JSON.
4) `spec.md` and `tasks.md` may reference UI nodes/components but must not contradict `ui.json`.

Checks:

- If `ui.json` exists:
  - ensure index category is `ui` (warn if not)
- If `ui-component-registry.json` exists:
  - verify component names used in UI specs/tasks align
- If UI JSON is missing for a declared UI JSON-driven spec:
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

Write a structured report in `.spec/reports/sync-spec-tasks/` including:

- Index input path used
- Canonical output path
- Mirror policy
- Safety mode
- Registry directory used
- Supplemental registry roots used (if any)
- Multi-repo roots used (if any)
- Specs processed
- Safe fields updated
- Registry recommendations/changes (by mode)
- Cross-registry collision findings
- UI alignment summary (if applicable)
- Follow-up recommendations

---

## 9) Recommended Follow-ups

- `/smartspec_validate_index`
- `/smartspec_generate_plan`
- `/smartspec_generate_spec`
- `/smartspec_generate_tasks`
- `/smartspec_generate_tests`
- `/smartspec_verify_tasks_progress`
- `/smartspec_reindex_specs` (when large-scale structural changes occurred)

---

## Notes

- This workflow is the primary **bridge** between working specs/tasks and the centralized truth.
- It remains intentionally conservative to avoid cross-team and cross-repo conflicts.
- `.spec/SPEC_INDEX.json` remains the canonical single source of truth.
- Root `SPEC_INDEX.json` is maintained as a legacy mirror only when needed.
- Multi-repo and multi-registry flags are optional for single-repo projects but strongly recommended for shared-platform architectures.

