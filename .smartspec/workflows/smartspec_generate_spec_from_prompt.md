---
description: Bootstrap starter specs from a natural-language prompt (ideation-first;
  reuse-first; reference-pack aware; no-network).
version: 7.0.0
workflow: /smartspec_generate_spec_from_prompt
---

# smartspec_generate_spec_from_prompt

> **Canonical path:** `.smartspec/workflows/smartspec_generate_spec_from_prompt.md`  
> **Version:** 7.0.0  
> **Status:** Production Ready  
> **Category:** spec-gen

## Purpose

Refine a **vague idea or natural-language prompt** into one or more **production-ready starter specs** with reuse-first intelligence.

This workflow MUST:

- **Handle both vague ideas and clear requirements** through an integrated ideation phase.
- **Ask clarifying questions** if the prompt is too ambiguous.
- **Perform feasibility analysis** and propose alternative solutions.
- **Detect overlaps** against all registries and existing specs.
- **Prefer reuse + references** over creating duplicates.
- **Produce UX/UI-ready specs** suitable for production planning.
- **Capture references** in a structured, auditable way.

It writes governed artifacts only when explicitly applied.

---

## Behavior (Vibe Coding)

This workflow operates in a sequence of phases:

### Phase 1: Prompt Analysis & Ideation (NEW)

1.  **Analyze Prompt Clarity:** Determine if the prompt is a vague idea or a clear requirement.
2.  **If Vague Idea:**
    -   **Initiate Ideation Sub-Workflow:**
        -   Identify core problem and user personas.
        -   Brainstorm potential solutions and features.
        -   Perform high-level feasibility analysis.
        -   **Ask clarifying questions** to the user to refine the idea.
        -   Generate a **Refined Requirements Document**.
    -   **Replace Original Prompt:** Use the refined requirements as the new prompt for the next phase.
3.  **If Clear Requirement:** Proceed to Phase 2.

### Phase 2: Reuse & Duplication Check (Enhanced)

1.  **Load All Registries:** Load all 8 registries (`api`, `data-model`, `ui-components`, `services`, etc.).
2.  **Compute Similarity:** Use `detect_duplicates.py` to check for semantic similarity against all registry entries and existing specs.
3.  **Classify Matches:** Use configured thresholds to classify matches (strong, medium, weak).
4.  **Propose Action:**
    -   **Strong Match:** Propose reuse and generate a delta/extension plan.
    -   **Medium Match:** Propose new spec but include references and justification.
    -   **No Match:** Proceed to generate a new spec.

### Phase 3: Spec Generation

1.  **Generate Spec Content:** Create a complete `spec.md` based on the (refined) prompt and reuse analysis.
2.  **Enforce Quality Contracts:** Ensure the spec includes all required sections (user stories, UI/UX, NFRs, etc.).
3.  **Extract Registry Items:** Identify all new components (APIs, data models, UI components, etc.) to be added to the registries.
4.  **Create Reference Index:** Build the `REFERENCE_INDEX.yaml` for all external inspirations.

### Phase 4: Preview & Validation

1.  **Write Preview Bundle:** Create a preview of all files (`spec.md`, registry updates) in a safe report directory.
2.  **Run Enhanced Validation:** Execute `validate_spec_enhanced.py` on the preview bundle.
3.  **Report Results:** Generate `report.md` with validation status, reuse analysis, and next steps.

### Phase 5: Apply (with `--apply`)

1.  **Check Validation:** The workflow MUST refuse to apply if the validation in the preview phase failed.
2.  **Write Governed Artifacts:**
    -   Create the new spec folder: `specs/<category>/<spec-id>/`
    -   Write `spec.md` and `references/**` files.
3.  **Update Registries:**
    -   For each registry, load the existing file, merge the new items, and write it back.
    -   This MUST be an atomic operation.
4.  **Update Spec Index:** Update `.spec/SPEC_INDEX.json`.

---

## Governance contract

This workflow MUST follow:

- `knowledge_base_smartspec_handbook.md` (v7)
- `.spec/smartspec.config.yaml`

### Write scopes (enforced)

Allowed writes:

- Governed specs: `specs/<category>/<spec-id>/**` (**requires** `--apply`)
- **Governed registries:** `.spec/registry/*.json` (**requires** `--apply`)
- Governed index: `.spec/SPEC_INDEX.json` (**requires** `--apply`)
- Safe outputs (previews/reports): `.spec/reports/spec-from-prompt/**` (no `--apply` required)

Forbidden writes (must hard-fail):

- Any path outside config `safety.allow_writes_only_under`
- Any runtime source tree modifications

---

## Flags (New in v7.0.0)

- `--interactive`: Force interactive mode for clarifying questions, even in non-interactive environments.
- `--skip-ideation`: Skip the ideation phase if the user is confident the prompt is clear.

---

## `summary.json` schema (Updated for v7.0.0)

```json
{
  "workflow": "smartspec_generate_spec_from_prompt",
  "version": "7.0.0",
  "run_id": "string",
  "applied": false,
  "ideation": {
    "was_vague": true,
    "questions_asked": 3,
    "refined_prompt_hash": "..."
  },
  "inputs": {"prompt": "string", "spec_category": "string", "refs": "string|null"},
  "reuse": {
    "strong_matches": [{"spec_id": "...", "score": 0.0}],
    "medium_matches": [{"spec_id": "...", "score": 0.0}],
    "decision": "reuse|new",
    "why": "..."
  },
  "validation": {
    "passed": false,
    "errors": 0,
    "warnings": 0
  },
  "writes": {"reports": ["path"], "specs": ["path"], "registry": ["path"]},
  "next_steps": [{"cmd": "...", "why": "..."}]
}
```

---

# End of workflow doc
