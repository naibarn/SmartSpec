---
description: Generate an implementation prompt for AI coding tools using SmartSpec centralization (.spec) and UI JSON addendum
version: 5.2
---

# /smartspec_generate_implement_prompt

Generate a high-quality **implementation prompt** for AI coding tools (Claude Code, Roo Code, Kilo Code, Gemini CLI, Antigravity, etc.) that ensures consistent, conflict-resistant execution aligned with SmartSpec v5.2 centralization.

This workflow enforces:
- **`.spec/` as the canonical project-owned space**
- **`.spec/SPEC_INDEX.json` as canonical index** when available
- **`.spec/registry/` as shared source of truth**
- `.smartspec/` as tooling-only
- **UI specs use `ui.json` as design source of truth** for Penpot integration

---

## What It Does

- Resolves canonical index and registry locations.
- Reads the target `spec.md` and `tasks.md`.
- Collects dependency and shared-knowledge slices.
- Applies UI JSON addendum rules conditionally.
- Generates a structured prompt that:
  - prevents re-inventing shared names
  - prevents cross-SPEC contract drift
  - enforces dependency-first implementation order
  - keeps UI design separate from business logic

---

## When to Use

- Right before starting implementation with an AI coding agent.
- After `tasks.md` has been generated and reviewed.
- When coordinating across multiple specs or repos.

---

## Inputs

- Target spec path (recommended)
  - Example: `specs/core/spec-core-004-rate-limiting/spec.md`

- Expected adjacent files:
  - `tasks.md`
  - (UI specs) `ui.json`

---

## Outputs

- An implementation-ready prompt text.
- Optional tool-specific notes (e.g., for Gemini TOML conversion by sync scripts).

---

## Flags

- `--index` Path to SPEC_INDEX (optional)  
  default: auto-detect

- `--registry-dir` Registry directory (optional)  
  default: `.spec/registry`

- `--spec` Explicit spec path (optional)

- `--tasks` Explicit tasks path (optional)

- `--focus` Optional focus hint  
  examples: `api`, `model`, `service`, `ui`, `tests`, `observability`, `security`

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
- The prompt must reference canonical names from these registries where available.
- If the implementation will require a new shared name, list it explicitly as a **pending registry addition**.

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

Do not rewrite these inputs.

---

## 3) Compile Cross-SPEC Context

If `INDEX_PATH` exists:

- Load dependency IDs for the target spec.
- Summarize the minimum required knowledge from dependencies:
  - shared API prefixes
  - shared models
  - cross-cutting security/observability constraints

If registries exist:

- Extract only relevant slices of:
  - APIs
  - models
  - glossary terms
  - critical sections
  - patterns

Keep the prompt compact and actionable.

---

## 4) Consistency Gate (Pre-Prompt)

Validate before generating the final prompt:

- Task dependency order does not conflict with SPEC_INDEX.
- Names in tasks/spec match registries (when present).
- No duplicated/conflicting namespace is implied.

In `--strict` mode:
- Stop and list conflicts with suggested resolutions.

---

## 5) UI JSON Addendum (Conditional)

Apply when **any** of these are true:
- Spec category is `ui` in the index.
- `ui.json` exists in the spec folder.
- The spec explicitly mentions Penpot/UI JSON workflow.

Prompt rules:

1) Treat `ui.json` as **design-owned**.
2) Do **not** embed business logic inside UI JSON.
3) Separate work into three tracks:
   - UI design alignment (with UI team)
   - Component implementation
   - Business logic/services
4) If `ui-component-registry.json` exists:
   - component names must match registry.
5) If the project does not use UI JSON:
   - do not fail
   - keep UI instructions text-based in `spec.md`.

---

## 6) Prompt Structure (Tool-Agnostic)

The generated implementation prompt must follow this structure:

1) **Role & Objective**
   - You are implementing SmartSpec: `<SPEC_ID> - <TITLE>`

2) **Canonical Context**
   - SPEC_INDEX path used (or NONE)
   - Registry directory used (or NONE)

3) **Non-Negotiable Constraints**
   - Do not invent new shared names when registries exist.
   - Do not change public contracts without a migration plan.
   - Respect dependency order.

4) **Spec Summary**
   - Scope
   - Key FRs
   - Key NFRs

5) **Dependencies**
   - What must already exist
   - What must be integrated

6) **Canonical Names (Do Not Rename)**
   - APIs
   - Models
   - Terms
   - Patterns

7) **Implementation Tasks (Ordered)**
   - Derived from `tasks.md`

8) **Testing Expectations**
   - Unit / Integration / Contract / Security / Performance
   - UI tests when applicable

9) **UI JSON Rules (if applicable)**
   - Mapping constraints
   - Logic separation

10) **Open Questions / Pending Registry Additions**

11) **Definition of Done**

---

## 7) Example Implementation Prompt Template

```text
You are implementing SmartSpec: <SPEC_ID> - <TITLE>.

Canonical context:
- SPEC_INDEX: <INDEX_PATH or NONE>
- Registry dir: <REGISTRY_DIR or NONE>

Hard rules:
- Use canonical names from registries when available.
- Do not introduce new shared API/model/term names without listing them under "Pending Registry Additions".
- Respect dependency order from SPEC_INDEX.
- Do not alter public contracts without a phased migration plan.

Spec objectives:
- <short bullet list>

Dependencies:
- <dep-1> (why it matters)
- <dep-2> ...

Canonical names to use:
- APIs: <list>
- Models: <list>
- Terms: <list>
- Patterns: <list>

Implementation order (from tasks.md):
1) <task group 1>
2) <task group 2>
...

Testing:
- Unit: ...
- Integration: ...
- Contract: ...
- Security: ...
- Performance: ... (if SLAs exist)

UI (only if category=ui or ui.json exists):
- Treat ui.json as design-owned.
- Map UI nodes to components using registry names when available.
- Keep business logic outside UI JSON.

Pending Registry Additions:
- <item 1> (evidence from spec/tasks)

Definition of Done:
- All tasks completed
- No registry drift introduced
- Tests green
- UI JSON rules satisfied when applicable
```

---

## 8) Recommended Follow-ups

- `/smartspec_generate_cursor_prompt` (if you want a Cursor-tailored variant)
- `/smartspec_generate_tests`
- `/smartspec_verify_tasks_progress`
- `/smartspec_sync_spec_tasks --mode=additive` (after review)

---

## Notes

- This workflow ensures AI agents receive the same centralized truth your team uses.
- `.spec/` remains the canonical project-owned source of shared knowledge.
- Root `SPEC_INDEX.json` is treated as a legacy mirror.

