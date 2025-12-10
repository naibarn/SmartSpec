# SmartSpec v5.7.0 – SPEC-First Autogeneration & Governance Upgrade

> **Status:** Draft release notes for the current `main` branch  
> **Scope:** Workflows, governance knowledge base, manuals, and docs

---

## 1. Highlights

- 🆕 **New workflow: `/smartspec_generate_spec_from_prompt`**  
  Bootstrap one or more `spec.md` files directly from a natural language prompt, with automatic splitting for larger features.

- 🧠 **Unified Governance Knowledge Base**  
  Merged the previous SmartSpec KBs into a single file:  
  `.smartspec/knowledge_base_smart_spec.md` (v5.7) – now the single source of truth for all workflows.

- 📘 **Install & Usage KB kept separate**  
  `.smartspec/knowledge_base_smartspec_install_and_usage.md` now focuses solely on installation and core usage (SPEC → PLAN → TASKS → IMPLEMENT).

- ✅ **UI governance upgrade for `/smartspec_ui_validation` (v5.6.4)**  
  Incorporates security/dependency evidence and design-system registries into the risk model, without adding new flags or changing NO-WRITE behavior.

- 🌐 **English/Thai manuals split and aligned**  
  All major workflows now have dedicated EN/TH manuals with the same structure and standard header tables.

---

## 2. New Features

### 2.1 `/smartspec_generate_spec_from_prompt` – From prompt to SPEC

New workflow for **first-time SPEC creation** from a natural language prompt:

- **Input:** a single prompt (English or Thai) describing the desired feature/app, e.g.:

  ```bash
  /smartspec_generate_spec_from_prompt \
    "Create a modern ecommerce website with strong SEO, a product list with images on the home page, a cart, a checkout flow, order creation, and an invoice page with payment instructions."
  ```

- **Core behavior:**
  - Reads project context: `specs/**`, `.spec/SPEC_INDEX.json`, registries.
  - Infers a suitable category (e.g. `ecommerce`, `miniapp`, `feature`) and 1–5 `spec-id`s.
  - Creates **new starter specs** under:
    - `specs/<category>/<spec-id>/spec.md`
  - **Never overwrites** an existing `spec.md`:
    - if a spec-id already exists, it generates a suffixed id (e.g. `_v2`) and explains why in the summary.
  - Optionally updates `.spec/SPEC_INDEX.json` **only** when `--update-index` is provided and the file is writable.

- **Write scope:**
  - `ALLOW-WRITE`, but strictly limited to:
    - creating new folders/files under `specs/**`, and
    - appending to SPEC_INDEX when `--update-index` is set.

- **Simple UX by default:**
  - No flags required for basic usage.
  - `--max-specs` (default `3`, range `1–5`) controls how many specs are generated.
  - `--max-specs=1` forces a single-spec design.

- **Intended chain:**
  - Bootstrap once with:
    - `/smartspec_generate_spec_from_prompt "<feature description>"`
  - Then refine with:
    - `/smartspec_generate_spec --spec-ids=<id>`
    - followed by `generate_plan`, `generate_tasks`, `implement_tasks`, etc.

---

## 3. Governance & Knowledge Base Changes

### 3.1 Unified Governance KB – `knowledge_base_smart_spec.md v5.7`

The previous governance KBs have been merged into:

- `.smartspec/knowledge_base_smart_spec.md` – **the single governance KB**.

This file now covers:

- Versioning and zero-feature-removal policy.
- Canonical project structure:
  - `.smartspec/`, `.spec/`, `specs/**`
- Workflow roles, write-guards, and safety-modes.
- KiloCode behavior:
  - `--kilocode`, `--nosubtasks`, Orchestrator semantics.
- Multi-repo and registry rules.
- SPEC-first design and spec-autogeneration patterns, including the new workflow:
  - `/smartspec_generate_spec_from_prompt`
- Workflow and manual authoring guidelines.
- UI governance and design-system rules.
- Security and dependency guardrails (React/Next.js/RSC, Node/npm, AI).
- RAG/context-reading limits and workflow catalog overview.

### 3.2 Install & Usage KB remains separate

- `.smartspec/knowledge_base_smartspec_install_and_usage.md` stays focused on:
  - Installing/updating SmartSpec.
  - High-level usage of the SPEC → PLAN → TASKS → IMPLEMENT chain.
  - Basic workflow usage patterns.

This keeps the system prompt compact (< 8,000 characters) while centralizing details in the KB.

---

## 4. Workflow Improvements

### 4.1 `/smartspec_ui_validation` v5.6.4

The UI validation workflow has been enhanced at the governance level:

- **Security & dependency evidence (web stacks):**
  - Reads existing artifacts for React/Next.js/RSC & Node/npm (SCA reports, lockfile summaries, `tool-version-registry.json`, CI security gates).
  - Treats missing or clearly outdated evidence as increased risk for CRITICAL/HIGH UI units, especially in `--safety-mode=strict`.

- **RSC as a high-risk surface:**
  - React Server Components and `react-server-dom-*` usage are treated as high-risk for data leakage and patch-level safety.
  - Critical flows using RSC should have explicit governance and up-to-date versions configured in registries.

- **Design-system & component registry context:**
  - Reads design-system/registry files under `.spec/registry/**`.
  - Prefers App-level components (`AppButton`, `AppCard`, etc.) over raw UI library components for critical flows.
  - Uses patterns/layout registries to reason about missing tests for key states (loading, empty, error).

> No flags were added, and no write behavior changed. All changes are **additive** and backward compatible with v5.6.2–v5.6.3.

### 4.2 Manuals and documentation alignment

- Updated `/smartspec_ui_validation` manuals:
  - English and Thai manuals separated and aligned.
  - English manual examples use English prompts only.
  - Added sections on:
    - AI-generated `ui.json` governance,
    - security/dependency evidence,
    - design-system & component registry usage.

- Added new manuals for `/smartspec_generate_spec_from_prompt`:
  - EN and TH manuals with:
    - Overview, What’s New, Core Concepts.
    - Quick start examples (ecommerce, miniapps, Kie.ai/Nano Banana Pro).
    - CLI/flags cheat sheet.
    - Best practices and FAQ.

---

## 5. System Prompt & Assistant Behavior

- The system prompt has been refactored to:
  - Always load:
    - `.smartspec/knowledge_base_smart_spec.md` (merged governance KB),
    - `.smartspec/knowledge_base_smartspec_install_and_usage.md` (install/usage KB).
  - Treat **all feature/miniapp questions** as SPEC-first tasks:
    - Propose `spec-id` and path (e.g. `specs/ecommerce/ecommerce_shop_front/spec.md`).
    - Either:
      - generate a strong starter `spec.md` directly (in Canvas/file), or
      - recommend using `/smartspec_generate_spec_from_prompt`.
    - Always suggest 3–5 potential improvements to the spec and invite refinements.

- Long outputs (specs/manuals/workflows) are meant to be generated into separate documents (Canvas/files), with chat replies summarizing and linking to the generated artifacts.

---

## 6. README & Docs Updates

- **README**:
  - Updated Core Commands table to include:

    ```md
    | `/smartspec_generate_spec_from_prompt.md` | Bootstrap one or more starter SPEC files directly from a natural language prompt. | [Details](.smartspec-docs/workflows/generate_spec_from_prompt.md) |
    ```

- **Docs:**
  - New and updated manuals under `.smartspec-docs/workflows/`.
  - Governance KBs consolidated and referenced consistently from the system prompt.

---

## 7. Breaking Changes

- **No breaking changes.**
  - No existing flags were removed.
  - No existing CLI semantics were changed.
  - All additions are backward compatible with the previous 5.6.x workflows.

---

## 8. Upgrade Notes

1. **Update SmartSpec binaries/scripts** as described in the README (install script or platform-specific instructions).
2. **Replace governance KB files:**
   - Put the merged `knowledge_base_smart_spec.md` into `.smartspec/`.
   - Keep `knowledge_base_smartspec_install_and_usage.md` as-is.
   - Optionally archive any older KB files as `*_legacy.md`.
3. **Add the new workflow:**
   - Place `smartspec_generate_spec_from_prompt.md` in `.smartspec/workflows/`.
   - Add its manual(s) under `.smartspec-docs/workflows/`.
   - Add the workflow to `README.md`’s Core Commands table.
4. **Run `/smartspec_project_copilot`** after upgrading:
   - To review project status and see how new specs and governance rules fit into your existing SPEC/PLAN/TASKS pipeline.

---

If you’d like, you can also create a shorter, bullet-point style `CHANGELOG` from this document for tagging and GitHub releases.