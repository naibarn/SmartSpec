---
description: Generate tasks.md from spec(s) with SmartSpec centralization (.spec), v5.6 cross-repo + multi-registry alignment, UI mode controls, and LLM-safe guardrails
version: 5.6
---

# /smartspec_generate_tasks

Generate a high-quality `tasks.md` from one or more existing specs while enforcing SmartSpec centralization rules and providing **LLM-safe, duplication-resistant** implementation guidance.

This v5.6 workflow preserves all essential behavior from v5.5 and earlier versions while adding **multi-repo** and **multi-registry** support to ensure that the chain:

> `/smartspec_generate_spec` → `/smartspec_generate_tasks`

remains consistent across projects that split specs and shared logic into two or more repositories.

---

## Goals

1. Produce `tasks.md` that is consistent with:
   - the target spec(s)
   - cross-spec registries
   - dependency graph in SPEC_INDEX
   - cross-repo ownership boundaries

2. Prevent cross-SPEC drift:
   - avoid re-inventing names
   - avoid conflicting API/model/term/UI definitions
   - reuse shared patterns instead of duplicating
   - respect ownership for shared entities

3. Support UI workflows:
   - JSON-driven UI (`ui.json`) for UI specs (default)
   - inline UI mode when explicitly requested

4. Provide fine-grained tasks and subtasks by default:
   - atomic subtasks (T0001.1 style)
   - explicit dependency graph

5. Provide multi-repo and multi-registry validation:
   - ensure referenced specs can be resolved across sibling repos
   - ensure shared registries are loaded consistently
   - reduce duplicate implementations across repos

---

## Inputs

- A target spec path (recommended):
  - e.g. `specs/checkout/spec.md`

- Optional flags:
  - index/registry overrides
  - strict/dev mode
  - UI mode
  - subtask control
  - multi-repo and multi-registry roots

---

## Outputs

- `tasks.md` next to the target `spec.md` by default.

- The generated file includes:
  - global guard rails
  - top-level tasks
  - automatic subtasks (default)
  - resource usage metadata
  - chain ownership hints when applicable
  - UI tasks aligned to UI mode
  - cross-SPEC/cross-repo warnings or blocking tasks
  - version pinning block

---

## Flags

### Index / Registry

- `--index=<path>`
  - Override automatic SPEC_INDEX detection.

- `--specindex=<path>`
  - Alias for `--index` (legacy-friendly).

- `--registry-dir=<path>`
  - Primary registry directory.
  - Default: `.spec/registry`

### Multi-Repo Resolution (NEW in v5.6)

These flags are aligned with `/smartspec_validate_index` and `/smartspec_generate_spec v5.6`.

- `--workspace-roots=<csv>`
  - Comma-separated list of additional repo roots to search for spec files.
  - Use when SPEC_INDEX references specs that live in sibling repos.
  - Example:
    - `--workspace-roots="../Smart-AI-Hub,../smart-ai-hub-enterprise-security"`

- `--repos-config=<path>`
  - JSON mapping of repo IDs to physical roots.
  - Suggested default path: `.spec/smartspec.repos.json`
  - Takes precedence over `--workspace-roots`.

  Example structure:
  ```json
  {
    "version": "1.0",
    "repos": [
      { "id": "public",  "root": "../Smart-AI-Hub" },
      { "id": "private", "root": "../smart-ai-hub-enterprise-security" }
    ]
  }
  ```

### Multi-Registry Resolution (NEW in v5.6)

- `--registry-roots=<csv>`
  - Additional registry directories to load **read-only** for cross-repo validation.
  - Use when each repo maintains a local registry that must be reconciled.
  - Example:
    - `--registry-roots="../repo-a/.spec/registry,../repo-b/.spec/registry"`

Notes:
- The workflow should treat `--registry-dir` as the **primary** registry.
- `--registry-roots` are **supplemental** validation sources.

### Execution Control

- `--dry-run` / `--nogenerate`
  - Print tasks without writing files.

### Subtask Control

- `--nosubtasks`
  - Disable automatic subtask decomposition.
  - Default: subtasks ON.

### Workflow Strictness

- `--mode=<strict|dev>`

  - `strict` (default):
    - Production/CI-grade gating.
    - Requires critical context (index + API/model registries) when project policy expects them.
    - Requires at least scoped repository scan.
    - Enforces cross-repo ownership clarity.

  - `dev`:
    - Best-effort generation for early-phase or local work.
    - Inserts high-visibility warnings into `tasks.md` when context is incomplete.
    - Adds bootstrap tasks to initialize missing governance artifacts.

### UI Mode

- `--ui-mode=<auto|json|inline>`
- `--no-ui-json` (alias for inline)

---

## 0) Resolve Canonical Index, Registries, and Multi-Repo Roots

### 0.1 Resolve SPEC_INDEX

Detection order:
1. `.spec/SPEC_INDEX.json` (canonical)
2. `SPEC_INDEX.json` (legacy root mirror)
3. `.smartspec/SPEC_INDEX.json` (deprecated)
4. `specs/SPEC_INDEX.json` (older layout)

If `--index/--specindex` is provided, it overrides detection.

### 0.2 Resolve Primary Registry Directory

Default:
- `.spec/registry`

Override:
- `--registry-dir`

### 0.3 Resolve Supplemental Registry Roots

If `--registry-roots` is provided:
- Parse CSV into a list of directories.
- Load each directory read-only.

### 0.4 Registry View & Precedence (NEW)

The workflow must construct a merged validation view:

1) **Primary registry** (`--registry-dir`)
2) **Supplemental registries** (`--registry-roots`, read-only)

Rules:
- If a name exists in the primary registry, it is authoritative.
- If a name exists only in a supplemental registry:
  - treat it as a **cross-repo candidate**
  - emit warnings if the target spec attempts to create a duplicate entity

### 0.5 Resolve Multi-Repo Roots

If `--repos-config` is provided:
- Load JSON.
- Construct repo root list using configured `root` values.
- Validate mapping for any `repo` labels used by SPEC_INDEX entries.

If `--workspace-roots` is provided:
- Add these roots to the search list.

If neither is provided:
- Use current repo root only.

---

## 1) Identify Target Spec(s)

- Validate the target `spec.md` path.
- Resolve spec ID via SPEC_INDEX when available.
- Identify dependencies from index and from spec content.

---

## 2) Resolve Dependency Specs Across Repos (NEW)

When a dependency ID is present:

- Use SPEC_INDEX to obtain `path` and `repo` labels (if present).
- Attempt to locate the physical `spec.md` across:
  - current repo root
  - `repos-config` roots
  - `workspace-roots`

Strict vs dev:

- `strict`:
  - If a **critical dependency** (shared API/model owner) cannot be resolved:
    - Insert a blocking task `T000 — Resolve missing dependency spec`.
    - Avoid generating create-type tasks for those shared entities.

- `dev`:
  - Insert warnings and allow partial planning.

---

## 3) Read Spec in Read-Only Mode

Extract:
- scope
- functional requirements
- non-functional requirements
- dependencies
- APIs
- data models
- domain terms
- UI sections

Also collect **ownership and reuse signals**.

---

## 4) Cross-SPEC & Cross-Repo Ownership Gate

### 4.1 Registry Ownership Validation

For each shared entity referenced by the spec:

- Determine whether it is:
  - owned by this spec
  - owned by another spec (same repo)
  - owned by another spec (different repo)
  - unknown

### 4.2 Chain Ownership (Compatible with v5.5)

Where applicable, tasks should capture chain ownership hints:

```yaml
chain_owner:
  api_owner: <spec-id|null>
  model_owner: <spec-id|null>
  pattern_owner: <spec-id|null>
  terminology_owner: <spec-id|null>
```

### 4.3 Cross-Repo Anti-Duplication Rule (NEW)

If a referenced owner spec is resolved in another repo:

- The workflow must:
  - prefer `type: reuse` tasks
  - add explicit notes detailing:
    - which repo owns the canonical implementation
    - where to import/call from
- It must **not** generate parallel create-type tasks for equivalent logic.

---

## 5) Generate Top-Level Tasks

Preserve the established categories:

1. Setup & Baseline
2. Core Implementation
3. Cross-SPEC Shared Work
4. Integrations
5. Testing
6. Observability & Ops
7. Security
8. UI & UX

IDs:
- `T001`, `T002`, …

---

## 6) Automatic Subtask Decomposition (Default)

By default:

- Each top-level task is decomposed into atomic subtasks:
  - `T002.1`, `T002.2`, …

- Subtasks must include explicit dependencies when logical ordering exists.

Disable via:
- `--nosubtasks`

---

## 7) Resource Usage Metadata (Multi-Repo Aware)

Every task/subtask must include:

```yaml
Resource usage:
  type: reuse | create
  chain_owner:
    api_owner: ...
    model_owner: ...
    pattern_owner: ...
    terminology_owner: ...
  registry:
    api: ...
    model: ...
    ui_component: ...
  files:
    - ...
  justification: ...
  repo_context:
    owner_repo: <id|unknown>
    consumer_repo: <id|current>
```

Rules:

- `reuse`:
  - MUST call/import the canonical implementation.
  - If owner_repo is different from consumer_repo, the task must state the import/integration boundary.

- `create`:
  - MUST justify creation.
  - MUST confirm the entity is not present in **any** loaded registry view.

---

## 8) Repository Scan (Scoped)

In `strict` mode:
- Perform at least a **scoped** scan within the bounded context.

Optional extension:
- When multi-repo roots are provided, implementations may run a **light cross-repo scan** for naming collisions and duplicated service stubs.

If potential duplicates are found:
- Insert a warning and convert create-type tasks to reuse-type where appropriate.

---

## 9) UI Addendum (Mode-Dependent)

### 9.1 JSON Mode

Tasks must include:
- Generate or validate `ui.json` first.
- Map UI nodes to components.
- Enforce design token usage.
- Extract business logic from UI.

### 9.2 Inline Mode

Tasks must include:
- Modern responsive layout tasks.
- Shared component reuse tasks.
- Container/logic separation tasks.

---

## 10) Global Guard Rails (Inserted into tasks.md)

The generated `tasks.md` must start with:

```markdown
> IMPLEMENTATION RULES
> - Load and read all referenced specs and registries before coding.
> - NEVER reimplement shared APIs, models, or UI components that have existing owners.
> - Cross-repo owners MUST be reused through defined import/integration boundaries.
> - Follow Resource usage strictly (reuse vs create).
> - Respect resolved UI mode (json/inline).
> - If any referenced SPEC is updated after generation time, STOP and regenerate tasks.md.
> - If contradictions between spec.md and tasks.md are found, STOP and reconcile.
> - tasks.md IS the primary execution plan.
```

---

## 11) Version Pinning

Generated tasks must include:

```markdown
Generated from SPEC:
  id: <spec-id>
  version: <front-matter | git hash | UNKNOWN>
  source: <front-matter | git | unknown>
  generated_at: <timestamp>

If any referenced spec updates after generated_at:
  STOP and regenerate tasks.md.
```

---

## 12) Reconciliation Task

In all modes, the workflow should add:

```markdown
T999 — SPEC/TASK Alignment Review
```

Purpose:
- verify no contradiction between spec and tasks
- confirm cross-repo reuse directives remain consistent

---

## Notes

- `.spec/` remains canonical for index and registries when present.
- `.smartspec/` is tooling only.
- Multi-repo flags are optional and safe to omit for single-repo projects.
- Multi-registry roots are validation-only sources by default.
- This v5.6 workflow is designed to be fully consistent with `/smartspec_generate_spec v5.6`.

