---
description: Generate or repair SmartSpec spec with v5.6 alignment for high-quality tasks generation, centralization (.spec), registry governance, UI mode controls, and multi-repo resolution
version: 5.6
---

# /smartspec_generate_spec

Create a new `spec.md` or repair an existing one while enforcing SmartSpec centralization and producing **task-ready, LLM-safe, cross-SPEC–consistent** specifications.

This workflow upgrades v5.5 behavior and aligns it more deeply with the TASKS philosophy:

- **Specs must be unambiguous enough to generate excellent `tasks.md`.**
- **Ownership and reuse rules must be explicit.**
- **Registries remain canonical for shared names.**
- **UI mode must be resolved consistently with tasks generation.**
- **Multi-repo projects must be supported without causing duplicate implementations.**
- **No essential legacy behavior is removed.**

---

## Core Assumptions

- **`.spec/` is the canonical project-owned space**.
- **`.spec/SPEC_INDEX.json` is the canonical index** when available.
- **Root `SPEC_INDEX.json` may exist as a legacy mirror** and must not be treated as the primary source when `.spec/SPEC_INDEX.json` exists.
- **`.spec/registry/` is the shared source of truth** for cross-SPEC names.
- `.smartspec/` is tooling-only.

UI governance:

- UI specs may use `ui.json` as a design source of truth.
- The workflow supports both JSON-driven UI and inline UI documentation.

Multi-repo governance:

- A project may distribute specs across sibling repositories.
- The `repo` field inside SPEC_INDEX identifies logical ownership, but file resolution requires explicit root mapping when repos are separate.

---

## What It Does

Depending on flags and context, this workflow will:

1) Resolve canonical index, registry, and multi-repo roots.
2) Read existing spec context and dependencies.
3) Generate a new `spec.md` from a description or target path.
4) Or **repair a legacy spec** without breaking existing content.
5) Extract cross-SPEC entities (APIs, models, terms, critical sections, patterns, UI components) to **recommend** or **append (additive)** registry updates.
6) Apply UI rules in a mode consistent with TASKS generation.
7) Add minimal, safe metadata if needed to make the spec **task-ready**.
8) Produce a report that highlights cross-repo dependencies and anti-duplication guidance.

---

## When to Use

- Creating a new spec under `specs/**/`.
- Migrating a project to centralization.
- Repairing legacy specs.
- Harmonizing naming across multiple teams/specs.
- Preparing specs that will later drive LLM-based implementation.
- Projects where specs may live across **two or more repos**.

---

## Inputs

- Target spec path (recommended)
  - Example: `specs/core/spec-core-004-rate-limiting/spec.md`

- Optional context files:
  - `plan.md`
  - `tasks.md`
  - dependency specs

- (UI specs) optional `ui.json`

---

## Outputs

- A new or updated `spec.md`.
- Centralization companion artifacts (when allowed):
  - `.spec/SPEC_INDEX.json` (minimal stub only when policy requires it)
  - `.spec/registry/*.json` (recommendations by default)
  - Reports under `.spec/reports/`

---

## Flags

### Index / Registry

- `--index` Path to SPEC_INDEX (optional)
  - default: auto-detect

- `--registry-dir` Registry directory (optional)
  - default: `.spec/registry`

### Multi-Repo Resolution (NEW)

These flags align with `/smartspec_validate_index` multi-repo behavior.

- `--workspace-roots=<csv>`
  - Comma-separated list of additional repo roots to search for spec files.
  - Use when SPEC_INDEX references specs located in sibling repos.
  - Example:
    - `--workspace-roots="../Smart-AI-Hub,../smart-ai-hub-enterprise-security"`
  - optional

- `--repos-config=<path>`
  - Path to a JSON config describing known repos and aliases.
  - If provided, this takes precedence over `--workspace-roots`.
  - Default suggested location: `.spec/smartspec.repos.json`
  - optional

  Example structure:

  ```json
  {
    "version": "1.0",
    "repos": [
      { "id": "public",  "root": "../Smart-AI-Hub" },
      { "id": "private", "root": "../smart-ai-hub-enterprise-security" },
      { "id": "tools",   "root": "../SmartSpec" }
    ]
  }
  ```

### Generation / Repair

- `--new` Force new spec generation (optional)

- `--repair-legacy`
  - Read an existing `spec.md` as read-only and generate missing companion centralization artifacts as needed.
  - Must not remove or rewrite core legacy content.

- `--repair-additive-meta`
  - Allows adding new, clearly marked metadata blocks when necessary for compatibility and task-readiness.
  - Must not change the meaning of existing sections.

### Registry Update Mode (Legacy-Compatible)

- `--mode` `recommend` | `additive`
  - Controls whether registries receive only recommendations or safe append-only updates.
  - default: `recommend`

### Safety / Strictness (Aligns with TASKS)

> NOTE: This is intentionally named **not** to conflict with the existing `--mode` flag.

- `--safety-mode=<type>`

  Options:
  - `strict` - Production/CI-grade gating (default)
  - `dev`    - Best-effort mode for early-phase projects

  Behavior (strict):
  - Requires critical registries when present by project policy.
  - Fails on unresolved cross-SPEC conflicts when they affect shared names.
  - Requires explicit ownership clarity for shared entities.
  - Requires explicit anti-duplication notes when cross-repo dependencies exist.

  Behavior (dev):
  - Allows spec generation even if registries are incomplete.
  - Inserts strong warnings in the report.
  - Recommends immediate follow-ups to initialize index/registries.

- `--strict` (legacy boolean)
  - If provided, treat as equivalent to `--safety-mode=strict` behavior for conflict gating.

- `--dry-run` Print output only (do not write files)

### UI Mode (Consistent with TASKS)

- `--ui-mode=<mode>`
- `--no-ui-json` (alias for `--ui-mode=inline`)

Modes:

- `auto`   - Detect based on index category, `ui.json` presence, or explicit UI JSON references (default)
- `json`   - Force JSON-driven UI spec
- `inline` - Force inline UI documentation (no required `ui.json`)

---

## 0) Resolve Canonical Index, Registry, and Multi-Repo Context

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

REG_MODE="${FLAGS_mode:-recommend}"
REPAIR_LEGACY="${FLAGS_repair_legacy:-false}"
REPAIR_ADDITIVE_META="${FLAGS_repair_additive_meta:-false}"
SAFETY_MODE="${FLAGS_safety_mode:-strict}"
STRICT_BOOL="${FLAGS_strict:-false}"
UI_MODE="${FLAGS_ui_mode:-auto}"
DRY_RUN="${FLAGS_dry_run:-false}"

if [ "$STRICT_BOOL" = "true" ]; then
  SAFETY_MODE="strict"
fi
```

### 0.3 Expected Registries (if present)

- `api-registry.json`
- `data-model-registry.json`
- `glossary.json`
- `critical-sections-registry.json`
- `patterns-registry.json` (optional)
- `ui-component-registry.json` (optional)
- `file-ownership-registry.json` (optional, recommended)

Rules:

- If a name already exists in registry, **reuse it**.
- If a new item is discovered:
  - `recommend`: output suggestions only.
  - `additive`: append missing entries only.
- Never delete, rename, or restructure registry entries automatically.

### 0.4 Resolve Multi-Repo Search Roots (NEW)

This workflow must support cases where specs are distributed across sibling repos.

Two ways to configure:

1) **Simple list** via `--workspace-roots`.
2) **Structured config** via `--repos-config`.

If neither is provided:

- The workflow will resolve and generate spec content only within the current repo root.

Resolution intent:

- Use multi-repo roots to:
  - locate dependency specs
  - confirm ownership boundaries
  - avoid duplicate designs and redundant code

Implementation hint (pseudo-code):

```javascript
function splitCsv(v) {
  return (v || '')
    .split(',')
    .map(s => s.trim())
    .filter(Boolean);
}

const cwdRoot = process.cwd();
let repoRoots = [cwdRoot];

if (FLAGS.repos_config && fs.existsSync(FLAGS.repos_config)) {
  try {
    const cfg = JSON.parse(fs.readFileSync(FLAGS.repos_config, 'utf-8'));
    if (Array.isArray(cfg.repos)) {
      repoRoots = [cwdRoot, ...cfg.repos.map(r => r.root).filter(Boolean)];
    }
  } catch (e) {
    console.warn('⚠️ Failed to parse repos config, falling back to --workspace-roots.');
  }
}

const extraRoots = splitCsv(FLAGS.workspace_roots);
repoRoots = [...new Set([...repoRoots, ...extraRoots])];
```

---

## 1) Identify Target Spec and Context

- If user provided a spec path:
  - Validate file exists (for repair).
  - Ensure parent folder matches expected naming patterns.

- If creating a new spec and no path is provided:
  - Recommend using `/smartspec_reindex_specs` or provide a coherent folder proposal.

- If `INDEX_PATH` is available:
  - Validate whether a spec with the same ID or path already exists.
  - If yes, warn and switch to repair or refuse creation unless explicitly forced.

---

## 2) Resolve Dependency Graph

If `INDEX_PATH` exists:

- Extract declared dependencies for the target spec.
- For each dependency ID:
  - Locate its `path` entry.
  - Attempt to resolve the physical `spec.md` across:
    - current repo root
    - `--repos-config` roots (if provided)
    - `--workspace-roots` list (if provided)

If dependencies cannot be resolved:

- `SAFETY_MODE=strict`:
  - add a blocking warning in the report.
  - require the spec to state a fallback integration plan.

- `SAFETY_MODE=dev`:
  - continue but add explicit TODO notes.

---

## 3) Determine UI Mode

Set `UI_MODE` using this precedence:

1) Explicit `--ui-mode` flag.
2) `--no-ui-json` implies `inline`.
3) If `INDEX_PATH` exists and the spec category is `ui`:
   - default to `json` unless the spec folder explicitly opts out.
4) If `ui.json` exists next to the spec:
   - `json`.
5) If the spec text references UI JSON/Penpot workflow:
   - `json`.
6) Otherwise:
   - `inline`.

---

## 4) Read Existing Spec (Repair or Context)

- Never delete existing sections.
- Preserve headings, clarity, and legacy explanations.
- Extract:
  - scope
  - functional requirements
  - non-functional requirements (SLA, performance, security)
  - dependencies
  - API contracts
  - data models
  - domain terms
  - UI sections
  - ownership notes and reuse directives

When `--repair-additive-meta` is enabled:

- You may insert clearly marked blocks such as:
  - **Ownership & Reuse**
  - **Cross-SPEC Registry Alignment**
  - **UI Mode Declaration**
  - **Task-Readiness Checklist**

These blocks must not contradict existing content.

---

## 5) Cross-SPEC & Cross-Repo Consistency Gates

If `INDEX_PATH` is available:

- Ensure dependency IDs and relationships in the spec align with SPEC_INDEX.
- Check naming collisions across:
  - API routes
  - model names
  - shared terms
  - UI component identifiers (when UI specs are involved)

If `REGISTRY_DIR` exists:

- Validate that:
  - API names referenced in the spec match `api-registry.json`
  - models match `data-model-registry.json`
  - terms match `glossary.json`
  - critical sections match `critical-sections-registry.json`

Cross-repo anti-duplication requirement:

- When any dependency is resolved outside the current repo root:
  - The spec must include an **explicit "Reuse vs. Implement" note** for each shared entity.
  - It must state:
    - which repo owns the canonical implementation
    - where the interface/contract is defined
    - what must be imported or called instead of re-implemented

Strict vs dev interpretation:

- `strict`:
  - unresolved shared-name conflicts are blocking.
  - missing ownership clarity for shared entities is blocking.

- `dev`:
  - allow generation but add high-visibility warnings.

---

## 6) Generate or Improve Spec Content

### 6.1 New Spec Generation

When `--new` is enabled or when creating a missing spec:

- Use the existing project structure and naming patterns.
- Include all core sections expected by legacy SmartSpec:
  - Overview
  - Scope
  - Goals / Non-goals
  - Functional Requirements
  - Non-functional Requirements
  - Architecture (high-level)
  - Data Models
  - API Contracts
  - Error Handling
  - Security
  - Observability
  - Rollout / Migration (if applicable)
  - Testing Strategy
  - Ownership & Reuse
  - Dependency Mapping

### 6.2 Repair Legacy Specs

When `--repair-legacy` is enabled:

- Treat the existing `spec.md` as read-only for core content.
- Only:
  - fill missing critical sections when required by centralization policy
  - add small clarifying notes when legacy text is ambiguous
  - add an Ownership & Reuse block if none exists
  - add UI mode declaration if UI-related content exists

---

## 7) Registry Extraction & Recommendations

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
  - Require the report to show a diff summary.

If registry files are missing:

- `SAFETY_MODE=strict`:
  - require a "Registry Initialization" paragraph in the spec.
  - recommend running:
    - `/smartspec_validate_index`
    - `/smartspec_reindex_specs`

- `SAFETY_MODE=dev`:
  - allow spec generation with a warning.

---

## 8) UI JSON Addendum (Mode-Dependent)

### 8.1 JSON-Driven UI

Apply when `UI_MODE=json`.

Rules:

1) UI design source of truth is `ui.json`.
2) `ui.json` should contain:
   - layout structure
   - component mapping metadata
   - design token references
   - props hints
3) No business logic in UI JSON.
4) `spec.md` should:
   - explain component responsibilities
   - document logic boundaries
   - link to `ui.json`

If a UI spec is being newly generated and `UI_MODE=json`:

- Create a minimal initial `ui.json` when project policy allows file creation.
- The initial JSON must:
  - use canonical component names where available
  - include design token references
  - avoid business logic entirely

### 8.2 Inline UI Specs

Apply when `UI_MODE=inline`.

- Do not require `ui.json`.
- Keep UI requirements inside `spec.md`.
- Ensure the spec still states:
  - UI/UX goals
  - responsive expectations
  - design token or system alignment if defined at project level

---

## 9) Output & Reporting

Default report directory:

- `.spec/reports/generate-spec/`

Include:

- Index path used
- Registry directory used
- Multi-repo roots used (if any)
- Safety mode
- UI mode
- Extracted entities summary
- Ownership clarity notes
- Cross-SPEC conflict warnings
- Cross-repo duplication risks
- UI JSON compliance notes
- Versioning status
- Recommended follow-up workflows

---

## 10) Recommended Follow-ups

- `/smartspec_validate_index`
- `/smartspec_reindex_specs`
- `/smartspec_generate_plan`
- `/smartspec_generate_tasks`
- `/smartspec_generate_tests`
- `/smartspec_sync_spec_tasks --mode=additive`

---

## Notes

- This workflow preserves compatibility with the existing SPEC_INDEX-driven pipeline.
- It introduces task-readiness improvements without turning specs into tasks.
- `.spec/registry/` remains canonical when present.
- Root `SPEC_INDEX.json` can remain as a legacy mirror.
- UI mode and safety mode are intentionally named to avoid conflicts with the existing registry update `--mode` flag.
- Multi-repo flags are optional and safe to omit for single-repo projects.

