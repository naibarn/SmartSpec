---
name: /smartspec_generate_cursor_prompt
version: 5.7.0
role: prompt-generation/governance
write_guard: NO-WRITE
purpose: Generate a Cursor‑ready implementation prompt aligned with SmartSpec v5.6–v5.7 governance, including multi-repo, multi-registry, UI JSON metadata, and anti-duplication guardrails.
version_notes:
  - v5.2: initial Cursor prompt workflow
  - v5.6.x: upgraded chain (multi-repo, multi-registry, UI JSON addendum)
  - v5.7.0: full governance alignment; documentation-only update; preserves non-breaking behavior
---

# 1) Summary
`/smartspec_generate_cursor_prompt` produces a **Cursor‑optimized implementation prompt** using:
- canonical SmartSpec centralization rules (`.spec/`, SPEC_INDEX, registry precedence),
- multi-repo + multi-registry resolution,
- strict reuse-over-rebuild rules,
- UI JSON metadata + design-system alignment (JSON-first UI governance),
- anti‑duplication guardrails,
- optional safety-mode.

This workflow is **governance-only** and **NO-WRITE**. It never edits code, specs, tasks, or UI JSON.

---
# 2) When to Use
Use right before implementation inside Cursor IDE:
- after `spec.md` + `tasks.md` are finalized,
- after dependencies are clarified,
- when building in multi-repo systems sharing registries,
- when UI JSON metadata is present.

Not for:
- generating tasks,
- validating UI behavior (use `/smartspec_ui_validation`),
- implementing code (use `/smartspec_implement_tasks`).

---
# 3) Inputs / Outputs
## Inputs (read-only)
- target `spec.md`
- adjacent `tasks.md`
- optional `ui.json` with metadata
- `.spec/SPEC_INDEX.json` (canonical)
- `.spec/registry/*.json` (primary)
- supplemental registries via `--registry-roots`
- multi-repo mapping via `--repos-config` / `--workspace-roots`

## Outputs
- Cursor‑ready implementation prompt text
- optional report under `.spec/reports/generate-cursor-prompt/`

---
# 4) Flags
## Index / Registry
- `--index` / `--specindex`
- `--registry-dir` (default: `.spec/registry`)
- `--registry-roots` (read-only supplemental registries)

## Multi-Repo
- `--workspace-roots`
- `--repos-config` (preferred for repo mapping)

## Target Selection
- `--spec`
- `--tasks`

## UI Governance
- `--ui-mode=<auto|json|inline>`
- `--no-ui-json` (alias for inline)

## Safety
- `--safety-mode=<strict|dev>` (default: strict)
- `--strict` (legacy alias)

## Output
- `--output=<path>`
- `--report=<summary|detailed>`

---
# 5) Canonical Index & Registry Resolution
1. SPEC_INDEX detection order:
   1) `.spec/SPEC_INDEX.json` (canonical)
   2) `SPEC_INDEX.json` at repo root (legacy mirror)
   3) `.smartspec/SPEC_INDEX.json` (deprecated)
   4) `specs/SPEC_INDEX.json` (older layout)

2. Registry precedence:
   - primary registry is authoritative,
   - supplemental registries are read-only for collision detection.

3. Multi-repo roots come from:
   - `--repos-config` (preferred),
   - else `--workspace-roots` + current repo.

---
# 6) Read Inputs (NO-WRITE)
- load `spec.md`, `tasks.md`, and optional `ui.json`
- never modify artifacts
- detect cross-spec references via SPEC_INDEX & registries

---
# 7) Cross-SPEC & Cross-Repo Context
- load dependent specs when resolvable via index
- load shared items from registries:
  - APIs, models, domain terms,
  - critical sections,
  - patterns,
  - UI component registry (if exists)
- treat supplemental registry definitions as **external ownership**

---
# 8) Pre-Prompt Consistency Gate
Checks:
1. dependency order does not contradict SPEC_INDEX
2. referenced names exist in registry
3. cross-repo naming collisions
4. UI mode consistency (JSON-first vs inline)
5. missing metadata in `ui.json` when UI JSON mode applies

Strict mode rules:
- fail early on ownership ambiguity
- block introduction of new shared names without governance clarification
- block missing UI JSON metadata for critical UI specs

---
# 9) UI JSON Addendum (v5.7‑aligned)
Applied when:
- spec category = `ui`, or
- `ui.json` exists, or
- UI JSON workflow is declared.

Expectations:
- UI JSON is **design-owned**, declarative, logic-free
- required metadata fields:
  - `source`, `generator`, `generated_at`,
  - `design_system_version`,
  - `style_preset`,
  - `review_status`
- map UI nodes → components using UI component registry
- verify naming alignment & separation of business logic

If metadata missing → raise risk (strict mode: blocking).

---
# 10) Prompt Structure (Cursor‑Optimized)
The generator must build a prompt with sections:
1. **Project Context**
2. **Target Spec (ID/title/path)**
3. **Dependencies & required understanding**
4. **Canonical Names (must not rename)**
5. **Implementation Tasks (ordered from tasks.md)**
6. **Testing expectations**
7. **UI JSON rules** (if applicable)
8. **Open Questions / Registry Additions**
9. **Definition of Done**

---
# 11) Anti-Duplication Guardrails
The prompt must instruct Cursor:
- never re-invent shared APIs/models/terms
- never create parallel versions of registry-owned items
- treat supplemental-registry items as externally owned
- if a new shared name is needed → list under “Open Questions / Registry Additions”

Strict mode: introducing a new shared name is discouraged unless explicitly justified.

---
# 12) Recommended Cursor Prompt Template (Generated)
The workflow may emit a structured template including:
- files to read first (`spec.md`, `tasks.md`, registries, UI JSON)
- canonical constraints from SPEC_INDEX
- task-by-task execution order
- test strategy
- UI JSON mapping rules
- open questions + definition of done

No direct patches or code modifications.

---
# 13) Best Practices
- run after `/smartspec_generate_tasks`
- pair with `/smartspec_generate_implement_prompt` for tool-agnostic flows
- keep registries current
- ensure UI JSON metadata is valid and reviewed when AI-generated

---
# 14) Flow & Stop Conditions
1. resolve flags
2. load index, registries, multi-repo view
3. read spec/tasks
4. gather dependencies
5. consistency gate
6. assemble prompt sections
7. write report/prompt (unless `--dry-run`)

Stop when:
- strict-mode violations occur
- missing canonical context cannot be recovered

Write guard: NO-WRITE (except emitting prompt/report).

