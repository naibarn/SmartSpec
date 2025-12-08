---
description: Generate an implementation prompt for AI coding from SmartSpec v5.6 tasks/specs with multi-repo + multi-registry alignment, UI mode support, and anti-duplication guardrails
version: 5.6
last_updated: 2025-12-08
---

# /smartspec_generate_implement_prompt

Generate a high-quality, tool-agnostic implementation prompt that instructs an LLM to implement a spec safely and consistently using the canonical SmartSpec chain.

This workflow is designed to reduce implementation drift, prevent duplicate shared code creation, and preserve the detailed execution intent captured in `tasks.md`.

This v5.6 document preserves the original v5.2 structure and intent while aligning with the upgraded chain:

1) `/smartspec_validate_index`
2) `/smartspec_generate_spec`
3) `/smartspec_generate_plan`
4) `/smartspec_generate_tasks`
5) `/smartspec_sync_spec_tasks`
6) `/smartspec_generate_implement_prompt`
7) `/smartspec_implement_tasks`
8) `/smartspec_verify_tasks_progress`

---

## What It Does

- Resolves canonical index and registry locations.
- Builds a merged registry validation view (primary + supplemental).
- Builds multi-repo search context when configured.
- Reads `spec.md`, `tasks.md`, and related referenced artifacts.
- Compiles cross-SPEC dependency context.
- Applies a pre-prompt consistency gate.
- Outputs a structured implementation prompt that:
  - is faithful to tasks sequencing
  - emphasizes reuse over reinvention
  - includes UI/UX rules when relevant
  - includes testing and verification expectations

---

## When to Use

- Immediately before running `/smartspec_implement_tasks`.
- When a human engineer wants an LLM-friendly implementation brief.
- After significant changes to `spec.md` or `tasks.md`.
- In multi-repo programs where shared APIs/models/registries must not be duplicated.

---

## Inputs

- Target spec path (recommended)
  - Example: `specs/core/spec-core-004-rate-limiting/spec.md`

- Expected adjacent files:
  - `tasks.md`
  - (UI specs) `ui.json`

- Optional governance context:
  - `.spec/SPEC_INDEX.json`
  - `.spec/registry/*.json`
  - supplemental registries in sibling repos

- Optional supporting artifacts referenced by spec/tasks:
  - datamodel files
  - API contracts
  - UI component registries
  - architecture diagrams (if text-linked)

---

## Outputs

- An implementation prompt file or console output (implementation-dependent).
- A report under:
  - `.spec/reports/generate-implement-prompt/`

---

## Flags

### Index / Registry (v5.6-aligned)

- `--index` Path to SPEC_INDEX (optional)  
  default: auto-detect

- `--specindex` Legacy alias for `--index`

- `--registry-dir` Primary registry directory (optional)  
  default: `.spec/registry`

- `--registry-roots` Supplemental registry roots (optional)
  - Comma-separated
  - **Read-only validation sources**

Registry precedence:

1) Primary registry (`--registry-dir`) is authoritative.
2) Supplemental registries (`--registry-roots`) are used to detect collisions and ownership ambiguity.

### Multi-Repo (NEW alignment)

- `--workspace-roots` Comma-separated repo roots (optional)

- `--repos-config` Path to structured repo config (optional)
  - Takes precedence over `--workspace-roots`
  - Recommended: `.spec/smartspec.repos.json`

### Target Selection

- `--spec` Explicit `spec.md` path (optional)

- `--tasks` Explicit `tasks.md` path (optional)

### UI Mode (Optional)

- `--ui-mode=<auto|json|inline>`
- `--no-ui-json` Alias for inline mode (optional)

### Safety / Preview

- `--safety-mode=<strict|dev>` (optional)
  default: `strict`

- `--strict` Legacy alias

- `--dry-run` Print prompt/report without writing files

### Tool Targeting (Optional)

Use these flags when you want the generated prompt to be optimized for a specific AI coding environment.

- `--kilocode`
  - Generate a KiloCode-optimized implementation prompt format.
  - This flag must be **non-breaking** and should not remove any tool-agnostic guardrails.
  - When enabled, the prompt may include:
    - a short “KiloCode Execution Notes” block
    - explicit file-read sequencing
    - stricter stop conditions for shared-name collisions

If no tool-targeting flag is provided, the workflow outputs a **tool-agnostic** prompt.

### Output

- `--output` Path for prompt output (optional)

- `--report` `summary|detailed` (optional)

---

## 0) Resolve Canonical Index & Registry

### 0.1 Resolve SPEC_INDEX (Single Source of Truth)

Detection order:

1) `.spec/SPEC_INDEX.json` (canonical)  
2) `SPEC_INDEX.json` (legacy root mirror)  
3) `.smartspec/SPEC_INDEX.json` (deprecated)  
4) `specs/SPEC_INDEX.json` (older layout)

### 0.2 Resolve Registry View

1) Load primary registry from `--registry-dir`.
2) If provided, load `--registry-roots` as read-only.

### 0.3 Expected Registries (if present)

- `api-registry.json`
- `data-model-registry.json`
- `glossary.json`
- `critical-sections-registry.json`
- `patterns-registry.json` (optional)
- `ui-component-registry.json` (optional)
- `file-ownership-registry.json` (optional)

---

## 1) Identify Target Spec/Tasks

Priority:

1) Use `--spec` / `--tasks` when provided.
2) Otherwise infer `tasks.md` adjacent to `spec.md`.
3) If index exists, enable spec ID resolution (implementation-dependent).

---

## 2) Read Inputs (Read-Only)

- Read `spec.md`.
- Read `tasks.md`.
- Detect `ui.json` if present.
- Load dependency specs when resolvable.

The workflow must not rewrite spec/tasks.

---

## 3) Compile Cross-SPEC Context

When an index exists:

- Load upstream dependency specs.
- Load cross-cutting core specs referenced by category or registry relationships.

In multi-repo mode:

- Resolve dependency specs across `--repos-config` or `--workspace-roots`.
- Mark them as **external owners** where applicable.

---

## 4) Consistency Gate (Pre-Prompt)

Before generating the prompt, confirm:

1) **Dependencies are declared** and not contradictory between spec and index.
2) **Shared names** referenced in spec/tasks are not colliding with any loaded registry view.
3) **Ownership & Reuse** instructions exist for high-impact shared APIs/models/terms.
4) UI mode is resolvable when UI addendum applies.

In `--safety-mode=strict`:

- If ownership ambiguity is detected for a shared name that appears in supplemental registries but not in the primary registry, the workflow must:
  - add an explicit “ownership clarification required” block in the prompt
  - strongly discourage local creation of a new shared definition

---

## 5) UI JSON Addendum (Conditional)

Apply when any of these are true:

- Spec category is `ui` in SPEC_INDEX
- `ui.json` exists
- The spec declares a JSON-driven UI workflow

UI rules to add into the prompt:

1) `ui.json` is the design source of truth in JSON mode.
2) Map UI nodes/frames to components.
3) Use `ui-component-registry.json` when present.
4) Keep business logic out of UI JSON.
5) Ensure the UI is modern, consistent, and coherent with project-wide patterns.

---

## 6) KiloCode Mode Switching Strategy (v5.6)

When `--kilocode` is enabled, the generated prompt must explicitly instruct the agent to **actively switch between KiloCode modes** to maximize quality and reduce drift.

This section restores and expands the intent implied in the legacy manual (v5.2) that KiloCode execution benefits from Orchestrator-driven subtask management.

### 6.1 Recommended Mode Flow

The prompt should recommend this default order for most SmartSpec implementations:

1) **Architect**
   - Read spec, tasks, index, and registries.
   - Summarize constraints, dependencies, and reuse boundaries.
   - Confirm UI mode (`json` vs `inline`) when applicable.

2) **Orchestrator** (primary execution coordinator)
   - Build the master execution map using the existing SmartSpec task IDs.
   - Prepare a live checklist that anticipates subtask numbering.

3) **Code**
   - Implement with tight adherence to the Orchestrator plan.

4) **Debug**
   - Fix failing tests and contract mismatches.

5) **Ask** (as-needed)
   - Clarify ambiguous requirements or cross-repo ownership conflicts.

### 6.2 Per-Task Orchestrator Switch (Critical for Subtasks)

KiloCode can trigger reliable **automatic subtask decomposition** only when the agent is operating in **Orchestrator** mode.

Therefore, when `--kilocode` is enabled, the prompt must instruct a **repeatable per-task loop**:

1) **Switch to Orchestrator** before starting each top-level SmartSpec task.
2) In Orchestrator, restate the task ID and scope, then request subtask breakdown using the SmartSpec numbering convention.
   - Example intent:
     - “For task `T0001`, break into `T0001.1`, `T0001.2`, … aligned with the spec and registries.”
3) Confirm the subtasks match:
   - dependencies
   - ownership/reuse boundaries
   - registry naming
   - UI mode constraints (if applicable)
4) **Switch to Code** to implement the approved subtasks in order.
5) **Return to Orchestrator** when moving to the next top-level task.

This loop prevents the LLM from skipping decomposition and reduces drift during long implementations.

### 6.3 Subtask Behavior

- **Default behavior in v5.6 remains: subtask decomposition ON** for KiloCode prompts.
- Use `--nosubtasks` only when:
  - tasks are already highly granular, or
  - the implementation environment cannot handle multi-level checklists.

### 6.3 Anti-Duplication Emphasis for Orchestrator

The prompt should explicitly remind Orchestrator to:

- Load and respect the merged registry view.
- Treat names found in any registry as existing shared assets.
- Avoid scheduling creation of new shared APIs/models/terms when ownership appears external.

---

## 7) Prompt Structure (Tool-Agnostic)

A v5.6 implementation prompt should contain:

1) **Purpose & scope**
2) **Files to read first** (must include):
   - target `spec.md`
   - target `tasks.md`
   - dependency specs
   - relevant registries
   - any referenced datamodel or API contract files
3) **Non-negotiable constraints**
   - reuse-over-rebuild rules
   - registry alignment rules
   - cross-repo owner boundaries
4) **Task execution order**
   - follow task IDs and subtask numbering
5) **Implementation guidance**
   - architecture boundaries
   - data and API rules
6) **Testing expectations**
7) **Verification and acceptance checks**
8) **Stop conditions**
   - when tasks contradict specs
   - when a shared-name collision is detected

---

## 7) Anti-Duplication Guardrails (v5.6)

The prompt must explicitly instruct the LLM to:

- Treat names found in any loaded registry view as **existing shared assets**.
- Prefer calling or importing shared code from owner specs.
- Avoid creating new parallel datamodels, API registries, or policy rules when ownership is already declared elsewhere.
- Search for existing utilities or patterns created by upstream specs before writing new code.

---

## 8) Example Implementation Prompt Template

The workflow may output a template like the following (illustrative):

- Read these files first:
  - `<spec.md>`
  - `<tasks.md>`
  - `<dependency spec.md>`
  - `.spec/SPEC_INDEX.json`
  - `.spec/registry/api-registry.json`
  - `.spec/registry/data-model-registry.json`
  - `.spec/registry/glossary.json`
  - `ui.json` (if present)

- Follow tasks in order. Use the exact task/subtask IDs as headings in your implementation notes.
- If a task says “reuse” or references an owner spec, do not create a new implementation.
- If you detect a naming collision with any registry, stop and report.

---

## 9) Recommended Follow-ups

- `/smartspec_implement_tasks`
- `/smartspec_generate_tests`
- `/smartspec_verify_tasks_progress`
- `/smartspec_fix_errors`
- `/smartspec_sync_spec_tasks`

---

## Notes

- This workflow is a **prompt generator**, not an implementation engine.
- Its primary purpose is to preserve the clarity of `tasks.md` and prevent LLM drift.
- Multi-repo and multi-registry flags are optional in single-repo environments but strongly recommended for platform programs.
- Do not remove or compress essential explanatory content originating from tasks/specs when assembling the final prompt.

