---
description: Generate tasks.md from spec(s) with SmartSpec centralization (.spec) and UI JSON addendum
version: 5.2
---

# /smartspec_generate_tasks

Generate a high-quality `tasks.md` from one or more existing specs while enforcing SmartSpec centralization rules.

This workflow assumes:
- **Canonical project governance lives in `.spec/`**
- `.smartspec/` is a **tooling workspace** (not a source of project truth)
- Shared knowledge must be resolved via **`.spec/SPEC_INDEX.json` + `.spec/registry/`**

---

## Goals

1) Produce `tasks.md` that is consistent with:
   - existing specs
   - cross-spec registries
   - dependency graph in SPEC_INDEX

2) Prevent cross-SPEC drift:
   - avoid re-inventing names
   - avoid conflicting API / model / term definitions
   - reuse shared patterns instead of duplicating

3) Support UI JSON addendum:
   - UI specs always keep UI design in JSON
   - ensure tasks separate UI design vs component vs logic

---

## Inputs

- A target spec path (recommended)
  - Example: `specs/core/spec-core-004-rate-limiting/spec.md`

- Optional flags:
  - `--index=<path>`
  - `--registry-dir=<path>`
  - `--dry-run`

---

## Outputs

- `tasks.md` next to the target `spec.md` (preferred)
- Or a consolidated tasks file for multi-spec batch modes

---

## Flags

- `--index` Path to SPEC_INDEX  
  default: auto-detect

- `--registry-dir` Path to registry directory  
  default: `.spec/registry`

- `--dry-run` Generate tasks in output only (do not write file)

---

## 0) Load Canonical Index & Registry Context

### 0.1 Resolve SPEC_INDEX (Single Source of Truth)

Auto-detect order:

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
  echo "⚠️ SPEC_INDEX not found. Continue with local-spec-only mode."
  INDEX_PATH=""
fi
```

### 0.2 Resolve Registry Directory

```bash
REGISTRY_DIR="${FLAGS_registry_dir:-.spec/registry}"

if [ ! -d "$REGISTRY_DIR" ]; then
  echo "⚠️ Registry directory not found at $REGISTRY_DIR"
  echo "   Continue with best-effort extraction from existing specs."
fi
```

### 0.3 Registry Files (if present)

Expected canonical registries:

- `api-registry.json`
- `data-model-registry.json`
- `glossary.json`
- `critical-sections-registry.json`
- `patterns-registry.json` (optional)
- `ui-component-registry.json` (optional)

Rules:
- If a name already exists in registry, **reuse it**.
- If a new item is discovered, **append to registry only when in additive mode**  
  (this workflow defaults to recommend-only, not auto-write).

---

## 1) Identify Target Spec(s)

- If user provided a spec path:
  - Validate file exists.
- Else:
  - Use `SPEC_INDEX` to list available specs and ask user to select.

---

## 2) Read Spec in Read-Only Mode

- Never rewrite existing `spec.md` here.
- Extract:
  - scope
  - functional requirements
  - non-functional requirements (SLA, performance, security)
  - dependencies
  - API contracts (if any)
  - data models
  - domain terms
  - UI sections (if category=ui or ui.json exists)

---

## 3) Cross-SPEC Consistency Checks

If `INDEX_PATH` is available:

- Ensure dependency entries in tasks match `SPEC_INDEX` graph.
- Check naming collisions:
  - API routes
  - model names
  - shared terms
- If a conflict is detected:
  - add a **blocking task**
  - propose resolution aligned with registry

If `REGISTRY_DIR` exists:

- Validate that:
  - API names referenced in tasks match `api-registry.json`
  - models match `data-model-registry.json`
  - terms match `glossary.json`

---

## 4) Generate Tasks Structure

Recommended structure:

1) **Setup & Baseline**
   - repo prep
   - environment
   - required tools

2) **Core Implementation Tasks**
   - separated into modules
   - aligned with spec sections

3) **Cross-SPEC Shared Work**
   - shared interfaces
   - shared patterns
   - shared libraries

4) **Testing**
   - unit
   - integration
   - contract tests
   - performance tests (if SLA exists)

5) **Observability / Ops**
   - logging
   - metrics
   - tracing
   - dashboards

6) **Security**
   - auth/authz integration
   - threat-mitigation tasks

---

## 5) UI JSON Addendum (Conditional)

This section applies when **any** of these are true:
- The target spec category is `ui` in SPEC_INDEX
- The spec folder contains `ui.json`
- The spec explicitly mentions Penpot/UI JSON workflow

Rules:
- UI design source of truth is **`ui.json`**
- Tasks must separate:
  - **Design tasks** (owned by UI team)
  - **Component tasks**
  - **Logic tasks**
- Do not embed business logic inside UI JSON

Required task patterns:

- **UI JSON validation**
  - schema check
  - component ID uniqueness
  - naming consistency with `ui-component-registry.json` if present

- **Component mapping**
  - map UI nodes → component names
  - verify component names match registry or propose additions

- **Logic extraction**
  - if spec implies logic inside UI layer
  - create task to move logic into service/controller layer

---

## 6) Output Rules

- Default write target:
  - `specs/**/tasks.md` next to the spec

- If `--dry-run`:
  - print tasks in output only

---

## 7) Quality Gates Before Finalize

Generated tasks must include checks for:

- Index alignment (if index exists)
- Registry alignment (if registry exists)
- No invented duplicate naming
- Clear dependency ordering
- UI separation rules (when UI addendum applies)

---

## Example Success Log

- ✅ Loaded SPEC_INDEX: `.spec/SPEC_INDEX.json`
- ✅ Loaded registries from `.spec/registry`
- ✅ No namespace conflicts
- ✅ UI JSON rules applied (ui.json found)
- ✅ tasks.md generated

---

## Notes

- `.spec/` holds project truth (index + registries).
- `.smartspec/` is tooling-only; do not create new canonical project files there.
- This workflow prefers **recommendations over auto-write** for registries
  to avoid unintended cross-team conflicts.
