# SmartSpec UI Guide (Penpot JSON-First)
Version: 1.0  
Last updated: 2025-12-07

This document explains how to design and build **UI category specs** in SmartSpec
under the **centralization model**, with special care for Penpot-based collaboration.

It is written for teams that want:
- A **design source of truth** that UI designers can edit directly,
- A stable linkage between **Penpot components ↔ code components**,
- Minimal naming drift across large multi-spec projects.

---

## 1) Goals of a UI Spec

A UI Spec should:
1) Define the UI/UX scope of a feature clearly.  
2) Allow the UI team to **edit design via Penpot** through a JSON artifact.  
3) Allow developers to implement UI without inventing new component names or structures.  
4) Reduce drift between:  
   - Design (Penpot)  
   - Spec narrative  
   - Code components  
   - Shared registries  

---

## 2) Key Definitions

### 2.1 UI JSON = Design Source of Truth

For UI-category specs, the **UI JSON file** is the authoritative record of:
- Layout/frames,
- Component bindings (design-to-code mapping),
- Design token references.

### 2.2 spec.md = Narrative & Rules

`spec.md` focuses on:
- Problem statement and goals,
- Scope / Non-goals,
- UX rules,
- Accessibility requirements,
- UX performance targets,
- Dependencies and contracts.

It should **not** duplicate low-level design-tool structures.

---

## 3) Standard File Structure

Recommended structure:

```
specs/ui/<spec-id>/
  spec.md
  tasks.md            # optional but strongly recommended
  ui.json
  assets/             # optional
```

> The UI JSON filename can be customized via config,  
> but each UI spec must have **one primary design JSON artifact**.

Suggested config:

```json
{
  "ui_spec": {
    "ui_json_name": "ui.json",
    "component_registry": "ui-component-registry.json"
  }
}
```

---

## 4) Separation of Concerns (Non-negotiable)

**Golden rule:**
- `ui.json` = design + structure + bindings + token references
- Business logic / data fetching / permissions / validation rules belong in:
  - code components,
  - hooks/store,
  - services/API clients,
  - and optionally described in `spec.md`.

### 4.1 What must NOT be inside `ui.json`

- Domain business rules (complex if/else logic)
- Side-effectful API behavior
- Detailed permission logic
- Pricing/credit calculations
- Non-UI validation rules

### 4.2 What can be inside `ui.json`

- High-level UI state slots that influence layout:
  - loading / empty / error (as UI states),
- Component binding metadata,
- Design tokens references.

---

## 5) Registries for UI (Recommended)

To prevent component-name fragmentation, add an optional UI registry:

`.spec/registry/ui-component-registry.json`

Minimal structure:

```json
{
  "version": "1.0.0",
  "last_updated": "2025-12-07T00:00:00Z",
  "components": [
    {
      "canonical_name": "UserAvatar",
      "penpot_component_id": "penpot:component:xxx",
      "code_component_path": "src/components/user/UserAvatar.tsx",
      "owned_by_spec": "spec-ui-xxx",
      "aliases": []
    }
  ]
}
```

**Usage rules**
- `generate-spec` / `generate-tasks` may create new entries.  
- `implement-*` / `verify-*` / `refactor-*` must treat this registry as **read-only**.
- If a spec or tasks mention a component not in the registry:
  - create a **registration task**.

---

## 6) Naming Conventions

### 6.1 Screens & Features

- Prefer canonical terms from the global glossary.
- Use user-facing language rather than technical internal names.

### 6.2 Components

- Use `PascalCase`.
- If the component is shared across specs:
  - register it in the UI component registry.

---

## 7) UI Specs and SPEC_INDEX

In large systems, UI specs frequently depend on core specs such as:
- authentication,
- authorization,
- audit logging,
- domain data contracts.

Rules:
- UI specs should **consume core contracts**,
  not modify core logic indirectly.
- If a UI flow requires a core contract change:
  - update/create the core spec first,
  - then update the dependent UI spec.

---

## 8) UI End-to-End Workflow (Recommended Order)

1) **generate-spec**
   - Create `spec.md` + a minimal `ui.json` template.
   - Register the spec in `.spec/SPEC_INDEX.json`.

2) **generate-plan**
   - Plan milestones with three tracks:
     - design,
     - component binding,
     - logic/implementation.

3) **generate-tasks**
   - Split tasks into three explicit groups:
     1) **Design tasks** (UI team / Penpot)
     2) **Binding tasks** (Penpot → code mapping)
     3) **Logic tasks** (developer-owned)

4) **generate-implement-prompt / generate-cursor-prompt**
   - Include canonical constraints from:
     - UI registry,
     - glossary,
     - API/data registries when relevant.

5) **implement-tasks**
   - Treat `ui.json` as **design-owned**.
   - Edit only when tasks explicitly require it.

6) **generate-tests**
   - Focus on:
     - component tests,
     - accessibility checks,
     - optional visual regression if used by the team.

7) **verify-tasks-progress**
   - Verify both:
     - task completion,
     - centralization consistency (names, bindings).

8) **refactor-code**
   - Move any accidental business logic out of UI layers.
   - Avoid `ui.json` edits unless a task states otherwise.

9) **sync_spec_tasks / fix_errors**
   - Prevent drift between spec ↔ tasks ↔ design artifacts.

10) **validate-index / reindex-specs**
   - Ensure every UI spec has a valid `ui.json`.

---

## 9) Recommended Templates

### 9.1 UI spec.md sections

- Overview
- User scenarios / personas (if applicable)
- Scope / Non-goals
- UX rules
- Accessibility baseline
- UX performance targets
- Dependencies (IDs from SPEC_INDEX)
- Design artifacts
  - `ui.json` path

### 9.2 Minimal ui.json (suggested anchors)

Your exact Penpot JSON format may differ.
These anchors help automation and linking:

```json
{
  "ui_spec_id": "spec-ui-xxx",
  "version": "0.1.0",
  "penpot": {
    "project_id": "optional",
    "file_id": "optional"
  },
  "screens": [
    {
      "name": "User Profile",
      "screen_id": "penpot:frame:xxx",
      "components": [
        {
          "canonical_name": "UserAvatar",
          "penpot_component_id": "penpot:component:yyy"
        }
      ]
    }
  ],
  "tokens": {
    "ref": "design-tokens-v1"
  }
}
```

---

## 10) Migration for Teams Not Using UI JSON Yet

To avoid disrupting legacy projects:

### 10.1 Legacy UI Mode

If `category=ui` exists but no `ui.json`:
- Tools should run in **legacy UI mode**.
- This should be a **WARN**, not a FAIL.
- Generate optional migration tasks.

### 10.2 Suggested Migration Steps

1) Add a minimal `ui.json` template.  
2) Map 1–2 core screens first.  
3) Register only the components you actually use.  
4) Expand design details incrementally.

---

## 11) Common Mistakes

1) **Developers modify `ui.json` without tasks.**  
   → Causes conflicts for the UI team in Penpot.

2) **Component names multiply across specs.**  
   → Registry missing or not enforced via tasks.

3) **UI specs attempt to change private/core contracts directly.**  
   → Must be handled through the core/private spec first.

4) **Tasks do not split design/binding/logic.**  
   → Leads to unclear ownership and poor estimation.

---

## 12) Pre-Merge Review Checklist

- [ ] UI spec includes both `spec.md` and `ui.json`.
- [ ] `ui.json` contains **no business logic**.
- [ ] Referenced components are:
      - in the UI component registry, or
      - have explicit registration tasks.
- [ ] Dependencies in `spec.md` match SPEC_INDEX.
- [ ] Core changes are implemented via core specs, not UI specs.
- [ ] Accessibility acceptance criteria are present.

---

## 13) Example UI Tasks

**Design track**
- [ ] D001: Update layout & flow in `ui.json` via Penpot export sync.
- [ ] D002: Confirm contrast and typography tokens.

**Binding track**
- [ ] B001: Map Penpot `UserAvatar` → `src/components/user/UserAvatar.tsx`.
- [ ] B002: Register component in `ui-component-registry.json`.

**Logic track**
- [ ] L001: Implement `useUserProfile()` hook.
- [ ] L002: Wire API client + error states.
- [ ] L003: Add permission guard for profile edit.

---

## 14) Summary

Penpot JSON-first UI Specs enable true parallel collaboration:
- UI team controls design artifacts,
- Developers implement stable, registry-backed components,
- The system reduces naming drift across large portfolios.

The core principles are:
1) `ui.json` is the design source of truth.  
2) Business logic lives in code and narrative docs.  
3) Registry-first naming for components.  
4) Workflows must split UI tasks into clear tracks.
