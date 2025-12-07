---
description: Generate a Cursor-ready implementation prompt using SmartSpec centralization (.spec) and UI JSON addendum
version: 5.2
---

# /smartspec_generate_cursor_prompt

Generate a high-quality **Cursor IDE prompt** for implementing a SmartSpec spec with full alignment to:
- canonical `.spec/SPEC_INDEX.json`
- shared `.spec/registry/`
- project-local tasks/specs
- UI JSON addendum when applicable

This workflow ensures that Cursor receives a complete, conflict-resistant context package so that implementation does not re-invent shared names or contradict other specs.

---

## What It Does

- Resolves canonical index and registry locations.
- Reads the target `spec.md` and `tasks.md`.
- Collects cross-SPEC context (dependencies, shared terms, models, APIs).
- Injects UI JSON rules when UI specs exist.
- Generates a concise but comprehensive prompt optimized for Cursor.

---

## When to Use

- Right before starting implementation in Cursor.
- After tasks have been generated and reviewed.
- When working within a multi-repo or large multi-SPEC system.

---

## Inputs

- Target spec path (recommended)
  - Example: `specs/core/spec-core-004-rate-limiting/spec.md`

- Expected adjacent files:
  - `tasks.md`
  - (UI specs) `ui.json`

---

## Outputs

- A Cursor-ready prompt text.
- Optional suggested file list / checklist for Cursor.

---

## Flags

- `--index` Path to SPEC_INDEX (optional)  
  default: auto-detect

- `--registry-dir` Registry directory (optional)  
  default: `.spec/registry`

- `--spec` Explicit spec path (optional)

- `--tasks` Explicit tasks path (optional)

- `--focus` Optional focus hint for Cursor  
  examples: `api`, `model`, `service`, `ui`, `tests`

- `--strict` Fail when canonical context is missing or conflicts are detected (optional)

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
  echo "⚠️ SPEC_INDEX not found. Prompt will be generated from local context only."
  INDEX_PATH=""
fi
```

### 0.2 Resolve Registry Directory

```bash
REGISTRY_DIR="${FLAGS_registry_dir:-.spec/registry}"

if [ ! -d "$REGISTRY_DIR" ]; then
  echo "⚠️ Registry directory not found at $REGISTRY_DIR"
fi

FOCUS="${FLAGS_focus:-}"
```

### 0.3 Expected Registries (if present)

- `api-registry.json`
- `data-model-registry.json`
- `glossary.json`
- `critical-sections-registry.json`
- `patterns-registry.json` (optional)
- `ui-component-registry.json` (optional)

Rules:
- Any shared-name used in the prompt must match registries when available.
- Any discovered new shared-name must be listed under **"Open Questions / Registry Additions"** in the prompt.

---

## 1) Identify Target Spec/Tasks

Priority:
1) `--spec` / `--tasks` if provided.
2) If `INDEX_PATH` exists, select spec by ID.
3) Otherwise, require a spec path.

Default tasks location:
- `tasks.md` next to `spec.md`.

---

## 2) Read Inputs (Read-Only)

- Read `spec.md`.
- Read `tasks.md`.
- If UI spec:
  - detect and read `ui.json`.

Do not rewrite these files.

---

## 3) Compile Cross-SPEC Context

If `INDEX_PATH` exists:
- Load dependency IDs for the target spec.
- For each dependency:
  - summarize expected shared interfaces and constraints.

If registries exist:
- Extract only relevant slices of:
  - APIs
  - models
  - domain terms
  - critical sections
  - patterns

Keep the prompt concise—do not dump full registry contents.

---

## 4) Consistency Gate (Pre-Prompt)

Validate before generating the final prompt:

- Task dependency order does not conflict with SPEC_INDEX.
- Names referenced in tasks/spec match registries.
- No duplicated or conflicting namespace is introduced in the prompt.

In `--strict` mode:
- stop and list the conflicts.

---

## 5) UI JSON Addendum (Conditional)

Apply when **any** of these are true:
- Spec category is `ui` in the index.
- `ui.json` exists in the spec folder.
- The spec explicitly mentions Penpot/UI JSON workflow.

Prompt rules for Cursor:

1) Treat `ui.json` as **design-owned**.
2) Do **not** encode business logic in UI JSON.
3) Separate implementation instructions into:
   - UI component mapping
   - UI rendering/state orchestration
   - Non-UI business logic layers
4) If `ui-component-registry.json` exists:
   - require component naming to match registry.
5) If the project does not use UI JSON:
   - do not fail
   - keep UI instructions text-based in `spec.md`.

---

## 6) Prompt Format (Cursor-Optimized)

The generated prompt must follow this structure:

1) **Project Context**
   - repo scope
   - relevant architecture notes

2) **Target Spec**
   - ID, title, location
   - objectives

3) **Dependencies**
   - required specs to implement/understand first

4) **Canonical Names (Do Not Rename)**
   - key APIs
   - key models
   - key domain terms

5) **Implementation Tasks (Ordered)**
   - derived from `tasks.md`

6) **Testing Expectations**
   - unit/integration/contract/perf
   - UI tests when applicable

7) **UI JSON Rules (if applicable)**
   - mapping constraints
   - separation of logic

8) **Open Questions / Registry Additions**
   - list any missing shared items that require team approval

9) **Definition of Done**
   - code + tests + consistency checks passed

---

## 7) Example Output Snippet (Template)

Use this template to generate the final Cursor prompt:

```text
You are implementing SmartSpec: <SPEC_ID> - <TITLE>.

Canonical context:
- SPEC_INDEX: <INDEX_PATH or NONE>
- Registry dir: <REGISTRY_DIR or NONE>

Do not invent new shared API/model/term names if registries provide canonical entries.
If you must introduce a new shared item, list it under "Open Questions / Registry Additions".

Implementation order:
1) <task group 1>
2) <task group 2>
...

Testing:
- Unit: ...
- Integration: ...
- Contract: ...
- Performance: ... (if SLAs exist)

UI (only if ui.json exists or category=ui):
- Treat ui.json as design-owned.
- Map UI nodes to components using registry names when available.
- Keep business logic outside UI JSON.

Definition of Done:
- All tasks completed
- No registry drift introduced
- Tests green
```

---

## 8) Recommended Follow-ups

- `/smartspec_generate_implement_prompt`
- `/smartspec_generate_tests`
- `/smartspec_verify_tasks_progress`
- `/smartspec_sync_spec_tasks --mode=additive` (after review)

---

## Notes

- This workflow exists to reduce prompt ambiguity and prevent Cursor from re-deriving shared truths.
- `.spec/` remains the canonical project-owned source of shared knowledge.
- Root `SPEC_INDEX.json` is treated as a legacy mirror.

