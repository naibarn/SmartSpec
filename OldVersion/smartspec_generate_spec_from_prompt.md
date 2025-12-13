name: /smartspec_generate_spec_from_prompt
version: 5.7.3
role: spec-generation/bootstrap
write_guard: ALLOW-WRITE (scoped)
purpose: Generate one or more starter `spec.md` files directly from a natural language prompt, aligned with SmartSpec SPEC-first governance, without overwriting existing specs and with optional SPEC_INDEX updates.

---

## 1) Summary

`/smartspec_generate_spec_from_prompt` generates one or more **starter** `spec.md` files directly from a natural-language prompt, using existing project structure as context.

This workflow is designed for **first-time spec creation** from a prompt. After it creates starter specs, you should refine them with `/smartspec_generate_spec`.

Key safety constraints:

- Never delete or overwrite existing `spec.md` files.
- Only create new spec folders/files under `specs/**`.
- SPEC_INDEX is updated **only when explicitly requested** via `--update-index`, and only in safe, governed locations.

Backward compatibility:

- All flags from v5.7.0 remain supported.
- `--workspace-roots` supports **both** comma (recommended) and semicolon separators.
- No destructive behavior is added.

---

## 1.1 Production Output Contract

To be considered production-grade, this workflow must always output a deterministic, auditable summary that includes:

- **Created artifacts** (absolute or repo-relative paths) for every new spec.
- **Collision decisions** (what existed, what suffix was applied).
- **Index change status**:
  - updated (and where), or
  - not updated (and why), plus JSON snippets if applicable.
- **Next steps** rendered in **two variants** (CLI + Kilo Code) and matching invocation mode.
- **Warnings** for:
  - missing SPEC_INDEX,
  - missing registries,
  - prompt redaction events,
  - multi-repo ambiguity.

### 1.1.1 Smart UX Guidance Output

In addition, the summary must always include a short section:

- **UX/UI improvement suggestions (3–7 items)** tailored to the user’s prompt.
  - Must be actionable (not generic).
  - Must be consistent with detected project stack/registries when available.
  - Must not contradict constraints implied by the prompt.

### 1.1.2 Reuse & Reference Output

To prevent redundant specs and duplicated components, the summary must also include:

- **Related existing specs found** (0..N): spec-id + path + why it matches.
- **Reuse decisions** for each major area (UI components, flows, integrations, data models):
  - reuse/link existing → reference, or
  - new → justify why new is required.
- If related specs exist: include **reference instructions** (what to reuse and where to read it).

The summary must not echo the full prompt; it must use a short sanitized intent summary.

---

## 2) When to Use

Use this workflow when:

- you have an idea/requirement like:

  > "Create a modern ecommerce website with strong SEO, a product list with images on the home page, a cart, a checkout flow, order creation, and an invoice page with payment instructions."

- and your project does **not yet** have a detailed `spec.md` for it.

This workflow does **not** replace `/smartspec_generate_spec`. Instead:

1. Run `/smartspec_generate_spec_from_prompt` once to create starter specs.
2. Then use `/smartspec_generate_spec --spec-ids=<...>` to refine and keep them aligned with the broader project.

---

## 3) Inputs & Outputs

### 3.1 Inputs

- **Positional prompt (required)**
  - Natural language requirement, in Thai or English.

### 3.2 Outputs

- One or more new folders under `specs/<category>/<spec-id>/` with:
  - `spec.md` – a **complete starter spec**, aligned with governance rules.

- Optional SPEC_INDEX update:
  - If `--update-index` is passed and a governed index exists and is writable, append new entries.
  - Without `--update-index`, do **not** modify SPEC_INDEX; print JSON snippets the user can paste in manually.

Security note:

- The workflow must avoid copying the full prompt verbatim into any long-lived report/output. Use a short, sanitized summary.

---

## 4) Modes (Role, Write Guard, Safety)

- **Role**: Ask/Architect + Implement (spec writer).

- **write_guard**: ALLOW-WRITE, strictly limited to:
  - creating **new** folders under `specs/**`,
  - creating **new** `spec.md` files,
  - appending to governed `.spec/SPEC_INDEX.json` **only** when `--update-index` is set and update can be performed safely.

- **Explicit non-goals (to respect KB write-guards)**:
  - Do not create or modify `tasks.md`.
  - Do not create or modify `design/`, `ui/`, `schema/`, `testplan/`.
  - Do not modify registries.
  - Do not modify any existing `spec.md`.

- **safety-mode**:
  - `normal` only; this workflow does not support aggressive overwrite.
  - It must **never overwrite an existing `spec.md`**; if a target folder exists, it must suffix the spec-id and explain the decision.

---

## 5) CLI Usage & Flags (Dual-Command Required)

> Documentation rule: every example must include **two** variants:
> - CLI (no `.md`, no `--kilocode`)
> - Kilo Code (`.md` + `--kilocode`)
>
> Rendering rule: if the user invoked this workflow with `--kilocode`, **all next-step commands printed by this workflow** must also use `.md` and include `--kilocode`.

### 5.1 Simple usage (recommended)

#### CLI Example

```bash
/smartspec_generate_spec_from_prompt \
  "Create a modern ecommerce website with strong SEO, a product list with images on the home page, a cart, a checkout flow, order creation, and an invoice page with payment instructions."
```

#### Kilo Code Example

```bash
/smartspec_generate_spec_from_prompt.md \
  "Create a modern ecommerce website with strong SEO, a product list with images on the home page, a cart, a checkout flow, order creation, and an invoice page with payment instructions." \
  --kilocode
```

### 5.2 Optional flags (kept minimal)

- `--spec-category=<category>`
  - Override the inferred category (e.g. `feature`, `ecommerce`, `miniapp`, `admin`).
  - If omitted and no reliable inference is possible, default to `feature` (canonical KB folder category).

- `--max-specs=<n>` (default: `3`, range `1–5`)
  - Maximum number of specs to split into when the feature is large.

- `--language=<th|en>`
  - Force output language for the generated starter specs.
  - If omitted: auto-detect based on prompt language; Kilo defaults to Thai.

- `--output-dir=<path>` (default: `specs`)
  - Root folder where new specs are created.
  - **Write-scope enforcement:** if this path resolves outside `specs/`, the workflow must:
    - refuse to write files,
    - behave as `--dry-run`, and
    - print a warning and the normalized safe target under `specs/`.

- `--update-index`
  - When set, append new spec entries to a governed SPEC_INDEX (see section 6).
  - Update must be **atomic** (read → merge → write/rename) and should use a simple file lock to avoid corruption when multiple Kilo subtasks run concurrently.
  - If locking/atomic update is not possible (or multi-repo roots are ambiguous), do **not** write; print JSON snippets instead.
  - Without this flag, SPEC_INDEX is never modified.

- `--dry-run`
  - Show planned categories, spec-ids, and a short outline **without** writing any files.

- `--specindex=<path>`
  - Override auto-detected SPEC_INDEX location for **reading**.
  - **Write safety:** `--update-index` must **not** write to arbitrary paths provided here.
    - If the override points to a non-governed location, the workflow prints JSON snippets instead.

- `--workspace-roots=<paths>`
  - Optional multi-repo support.
  - Accept both comma-separated (recommended) and semicolon-separated lists.
    - Example: `repo1,repo2` (recommended)
    - Example: `repo1;repo2` (back-compat)

- `--repos-config=<path>`
  - Optional multi-repo layout configuration.

- `--registry-dir=<path>` / `--registry-roots=<paths>`
  - Optional overrides for design-system and tool registries; used read-only to suggest UI stacks and patterns.

- `--kilocode`
  - Enable Kilo Orchestrator behaviour according to governance rules.

### 5.3 Multi-repo example

#### CLI Example

```bash
/smartspec_generate_spec_from_prompt \
  "Add user management: login, roles, permissions, and audit logs" \
  --repos-config repos.json \
  --workspace-roots repo1,repo2 \
  --max-specs=2
```

#### Kilo Code Example

```bash
/smartspec_generate_spec_from_prompt.md \
  "Add user management: login, roles, permissions, and audit logs" \
  --kilocode \
  --repos-config repos.json \
  --workspace-roots repo1,repo2 \
  --max-specs=2
```

---

## 6) Canonical Folders & File Placement

This workflow must respect the standard layout:

- Specs:

```text
specs/<category>/<spec-id>/spec.md
```

- SPEC index auto-detection order (unless `--specindex` is set for **read-only**):

1. `.spec/SPEC_INDEX.json`
2. `SPEC_INDEX.json` at repo root
3. `.smartspec/SPEC_INDEX.json`
4. `specs/SPEC_INDEX.json`

If none is found:

- create spec folders/files anyway, and
- print a warning with a suggestion to create `.spec/SPEC_INDEX.json`.

Governed write target for `--update-index`:

- **Only** `.spec/SPEC_INDEX.json` is a writable, governed target.
- If auto-detection finds another index location (e.g. `specs/SPEC_INDEX.json`), treat it as **read-only** for compatibility and context inference.
- If `--specindex=<path>` is provided:
  - Use it for **reading only**.
  - Never write to it, even with `--update-index`.

Concurrency + integrity rules for updates:

- Use a lock file next to the governed index: `.spec/SPEC_INDEX.json.lock`.
- If the lock cannot be acquired quickly, **do not write**; print JSON snippets instead.
- Perform atomic update:
  1) read current index,
  2) merge (dedupe by `spec_id`),
  3) write to temp file in the same directory,
  4) fsync if supported,
  5) rename temp → `.spec/SPEC_INDEX.json`.
- Always leave the index valid JSON (no partial writes).

In multi-repo mode:

- Only update indices that are **inside** detected workspace roots.
- If more than one writable `.spec/SPEC_INDEX.json` candidate exists and the primary root is ambiguous, **do not write**; print JSON snippets.

If the detected/overridden index is not a governed `.spec/SPEC_INDEX.json`, do not write; print JSON snippets.

- Registries (read-only):
  - `.spec/registry/**` are used to:
    - infer design systems and UI stacks,
    - prefer App components and patterns over raw UI components,
    - suggest patterns for layout and states.

---

## 7) Behaviour & Step-by-step Flow

1. **Read context & KBs**
   - Load governance and install/usage KBs.
   - Detect SPEC_INDEX and existing spec naming patterns.
   - Detect registry stacks (read-only) to prefer App components/patterns.
   - Build a **Related-Specs Catalog**:
     - read SPEC_INDEX entries and collect spec-ids + titles/keywords (whatever fields exist),
     - scan `specs/**/spec.md` headings to build a lightweight term index,
     - store as in-memory candidates for de-duplication.

2. **Parse the prompt (sanitized)**
   - Extract key domains:
     - product/feature,
     - core flows,
     - external integrations,
     - UI/UX inspirations and reference links (URLs, brand/style mentions),
     - NFR hints.
   - Redact obvious secrets/tokens if present; never echo full prompt in the final summary.

2.1 **Reference Intake (URLs, brands, style targets)**
   - Accept references in the prompt such as:
     - inspiration sites (e.g., Apple-like browsing experience),
     - UI shots (e.g., a Dribbble shot link),
     - third-party services/APIs (e.g., Freepik, Kie.ai, Google/Vertex AI Imagen).
   - Normalize and classify each reference into one of:
     - **Design inspiration** (visual/interaction patterns),
     - **Product/behavior benchmark** (experience quality targets),
     - **API/integration** (official docs required).

2.2 **Reference Research Requirement (must be sufficient to spec)**
   - For each **API/integration** reference:
     - Prefer official docs as primary sources.
     - Extract enough to write an implementable integration section:
       - auth method, base URL, endpoints, required fields, response shape, errors,
       - rate limits/quotas if documented,
       - pricing/cost notes if available,
       - data retention and storage rules,
       - recommended retries/timeouts and idempotency guidance.
   - For each **design inspiration / benchmark** reference:
     - Extract patterns (layout, hierarchy, spacing, typography intent, motion intent) without copying copyrighted assets.
     - Capture key UX behaviors: navigation model, search/filter patterns, progressive disclosure, performance perception patterns.

2.3 **Copyright & Brand-Safety Rule (no cloning)**
   - References like Apple.com or Dribbble shots must be treated as inspiration.
   - The generated spec must:
     - define *principles* and *patterns* to emulate,
     - require an original UI, and
     - avoid copying exact layouts/graphics/microcopy.

3. **Decide category & `spec-id`(s)** & `spec-id`(s)**
   - Infer `category` from:
     - existing categories in SPEC_INDEX (if present),
     - keywords in the prompt.
   - If inference is weak/ambiguous, default to **`feature`**.
   - Construct slugged `spec-id`s.
   - Keep number of specs ≤ `--max-specs`.
   - For each planned spec, generate a one-line intent summary.

3.1 **De-duplication & Reuse Check (SPEC_INDEX + existing specs)**
   - For each planned spec, search the Related-Specs Catalog for:
     - similar journeys/flows,
     - similar UI modules/components,
     - same integration/provider,
     - same core domain model.
   - If a strong match exists:
     - **do not create a new overlapping spec**;
     - instead, create a smaller spec focused on the delta (extension) and add explicit references (see section 5).
   - If partial overlap exists:
     - keep the new spec, but explicitly mark which parts must be reused and referenced.
   - Always explain the decision in the output summary.

4. **Ensure uniqueness & safety (folder-aware)**
   - Check for existing folders under `specs/<category>/<spec-id>/`:
     - If the folder exists (even if `spec.md` is missing) → treat as occupied.
     - Choose a new spec-id with a numeric suffix, e.g. `*_v2`, `*_v3`.
   - When creating a new folder, prefer an atomic/guarded create:
     - attempt to create the directory;
     - if it already exists (race), suffix and retry.
   - Mention the collision decision in output.

5. **Generate starter `spec.md` content**
   For each new spec, the generated `spec.md` must be **implementation-ready** and **UX-complete** (not just a feature list).

   Minimum required sections (include if relevant):

- **Context & Goals**
  - problem statement, success metrics, constraints.

- **Personas / Roles & Journeys**
  - primary/secondary users, key journeys and jobs-to-be-done.

- **Information Architecture**
  - navigation map, page hierarchy, permissions impact on navigation.

- **UI/UX Spec (must be concrete)**
  - screen list + flows (happy path + edge paths)
  - key components per screen (prefer App components/patterns inferred from registries)
  - interaction states: loading/empty/error/disabled/success
  - form UX: validation rules, inline errors, keyboard behavior
  - accessibility: focus order, ARIA intent, color contrast expectation, reduced motion
  - responsive behavior: breakpoints, mobile-first considerations
  - content/microcopy guidance: labels, helper text, error messages style

- **Reuse & References (must be explicit)**
  - **Related Specs**: list any existing spec(s) that overlap, with:
    - spec-id, path, and what to reuse.
  - **Reuse Directives** (non-optional rules):
    - what must be reused (component/flow/model/integration),
    - where it is defined (links/paths),
    - what is the delta in this spec.
  - **No-Duplicate Rule**: if an existing spec already defines a component/flow, this spec must reference it and describe only the delta.

- **System Behaviors**
  - auth/session rules, permissions, rate limiting expectations.

- **Data Model & Persistence**
  - entities, relationships, ids, timestamps, audit fields.

- **External Integrations (complete linkage info)**
  - provider(s), auth method, environments, secrets placeholders
  - request/response schemas (or pointers to schema source), idempotency
  - retries/timeouts, error mapping, webhook/event handling (if any)
  - operational notes: observability, alerting, dashboards
  - **Provider abstraction (if multiple vendors)**:
    - define a provider interface (e.g., `ImageGenProvider`) and configuration-driven routing
    - fallback strategy and cost/latency tradeoffs
    - consistent safety checks and content policy handling per provider

- **Reference Appendix (complete, structured)**
  - The spec must introduce a simple reference system so references are reusable and auditable.

  **Reference ID scheme**
  - `REF-UX-###` for UX/benchmark references (e.g., Apple-like browsing experience)
  - `REF-UI-###` for UI inspiration shots (e.g., a Dribbble dashboard shot)
  - `REF-API-###` for API/integration docs (e.g., Freepik image gen, Kie.ai image gen, Google Vertex AI Imagen)
  - `REF-SPEC-###` for internal reuse references to existing specs

  **How to reference inside the spec**
  - Every major UI/UX decision should cite at least one `REF-UX`/`REF-UI`.
  - Every integration detail must cite at least one `REF-API`.
  - Every reuse directive must cite at least one `REF-SPEC`.

  **Reference record template (repeat per ref)**
  - `id:` (e.g., `REF-API-001`)
  - `type:` (design inspiration / benchmark / api docs / internal spec)
  - `title:`
  - `source:` link(s)
  - `date_accessed:`
  - `what_to_emulate:` (principles/patterns)
  - `what_not_to_copy:` (copyright/brand constraints)
  - `extracted_requirements:` (bullets)
  - `implementation_notes:` (endpoints/auth/errors; or UI behaviors)

- **NFR (Non-functional requirements)**
  - performance targets, SEO requirements (if web), security/privacy, observability.

- **Analytics / Events (if product-facing)**
  - critical funnels, key events, dashboards.

- **Assumptions & Open Questions**
  - explicitly list what was assumed from prompt.
  - if critical ambiguity exists, ask 3–7 targeted questions in the spec.

- **Decision Log (international-quality)**
  - short table of key decisions: decision, options considered, rationale, tradeoffs.

- **Phased Delivery & Options (smart suggestions)**
  - propose 2–3 options aligned to prompt:
    1) MVP (fast/lean)
    2) Recommended (balanced)
    3) Premium (delight/scale)
  - each option must list: scope, UX impact, effort/risk notes.

Quality rule:

   - The content must follow the SPEC-first governance and be strong enough to drive `/smartspec_generate_spec` and `/smartspec_generate_plan`.

6. **Write files & optionally update SPEC_INDEX**
   - Validate write scope *before* creating any folders/files:
     - Resolve and normalize paths.
     - Reject `..` traversal.
     - Reject symlink escapes: if any parent directory resolves outside `specs/`, do not write.
   - New specs must be written under `specs/**` only.
   - If `--output-dir` resolves outside `specs/`, refuse writes and behave as `--dry-run`.

   - Create folders and `spec.md` under `specs/<category>/<spec-id>/`.

   - If `--update-index` is set:
     - Only append to governed `.spec/SPEC_INDEX.json` targets.
     - Use lock + atomic update (temp + rename).
     - If lock/atomic update cannot be guaranteed, print JSON snippets instead.

7. **Output summary & next steps (mode-correct commands)**
   - List each created spec with:
     - folder path,
     - short description,
     - **two** next-step commands (CLI + Kilo Code), and additionally:
       - clearly mark which one matches the user’s invocation mode.

   - Recommend the canonical chain:
     - refine SPEC → PLAN → TASKS

---

## 8) KiloCode Support (Meta-Flag)

- Flag: `--kilocode` (universal, required by governance).

Behaviour under Kilo:

- Orchestrator-per-task is allowed and may split by spec-id when multiple specs are generated.
- The workflow must **not** enable Orchestrator unless `--kilocode` is present.
- If the platform provides a global “disable subtasks” flag, it must be respected.

Command rendering requirement:

- When the workflow is invoked with `--kilocode`, it must output next-step commands using:
  - workflow names ending in `.md`, and
  - include `--kilocode`.

---

## 9) Security Hardening Checklist

Before writing anything, the workflow must enforce:

- **Path normalization**: resolve `--output-dir` and all computed paths with normalized absolute paths.
- **No path traversal**: reject `..` escapes anywhere in computed output paths.
- **No symlink escape**: if the resolved realpath of any target would land outside `specs/`, refuse writes.
- **Index update safety**: lock + atomic write. If not possible, print JSON snippets only.
- **Prompt redaction**: if the prompt contains obvious secrets/tokens/keys, redact them before writing into `spec.md` (use placeholders).

---

## 10) Optional Extensions (Non-core Workflows)

This workflow must avoid recommending commands that are not guaranteed by the core install.

- If you want to mention optional quality gates (tests/CI/release readiness), present them as **optional** and only if the workspace contains those workflows.
- Default next steps must stick to the core chain:
  - generate/refine SPEC → generate PLAN → generate TASKS.

### 10.1 Raising Output to International Standards

When generating specs, prefer globally accepted quality baselines:

- **Accessibility-first**: treat keyboard navigation and focus management as a first-class requirement.
- **State-complete UX**: every async UI must define loading/empty/error/success states.
- **Clear contracts**: integrations must define retries, idempotency, schema, and error mapping.
- **Decision transparency**: include a short Decision Log with tradeoffs and rationale.
- **No duplication**: reuse existing specs/components via explicit references, only spec the delta.
- **Evidence-based references**: references must be captured in a structured appendix and translated into implementable requirements.

When generating specs, prefer globally accepted quality baselines:

- **Accessibility-first**: treat keyboard navigation and focus management as a first-class requirement.
- **State-complete UX**: every async UI must define loading/empty/error/success states.
- **Clear contracts**: integrations must define retries, idempotency, schema, and error mapping.
- **Decision transparency**: include a short Decision Log with tradeoffs and rationale.
- **No duplication**: reuse existing specs/components via explicit references, only spec the delta.



This workflow must avoid recommending commands that are not guaranteed by the core install.

- If you want to mention optional quality gates (tests/CI/release readiness), present them as **optional** and only if the workspace contains those workflows.
- Default next steps must stick to the core chain:
  - generate/refine SPEC → generate PLAN → generate TASKS.

---

## 11) Weakness & Risk Check

Before finishing, the workflow should self-assess and report:

- **Prompt quality dependence**
  - Weak/ambiguous prompts may produce poor specs.
  - Mitigation: suggest 3–5 ways to refine the prompt or generated specs.

- **Context mismatch**
  - If SPEC_INDEX or registries are missing/outdated, inferred categories and models may not match reality.
  - Mitigation: surface clear warnings and encourage running:
    - `/smartspec_project_copilot` (CLI) / `/smartspec_project_copilot.md --kilocode`
    - `/smartspec_generate_spec` (CLI) / `/smartspec_generate_spec.md --kilocode`

- **Security & data sensitivity**
  - Prompts may contain sensitive data; avoid logging them verbatim into long-lived reports.
  - Use placeholders for secrets/tokens in any suggested integrations.
  - If secrets are detected: redact in output and warn.

- **Oversplitting vs undersplitting**
  - Too many specs can fragment the design; too few can create monoliths.
  - Mitigation: explain split rationale and suggest alternative split options.

- **Write-scope safety**
  - Re-affirm in the summary:
    - no existing `spec.md` files were modified,
    - SPEC_INDEX was only changed if `--update-index` was provided,
    - and only in governed locations.

---

## 12) Legacy Flags Inventory

This workflow was introduced in v5.7.0.

- Kept: all v5.7.0 flags
- Alias: N/A
- New in v5.7.1:
  - `--language=<th|en>` (optional)
  - Clarified `--workspace-roots` separators (comma recommended; semicolon allowed)
  - Tightened write-scope requirements for `--output-dir` and `--specindex` updates (governed only)

All changes are additive and preserve existing CLI usage.

---

## 13) Quick Start Examples (Dual-Command)

### 11.1 Simple ecommerce website (single repo)

#### CLI Example

```bash
/smartspec_generate_spec_from_prompt \
  "Create a modern ecommerce website with strong SEO, a product list with images on the home page, a cart, a checkout flow, order creation, and an invoice with payment instructions."
```

#### Kilo Code Example

```bash
/smartspec_generate_spec_from_prompt.md \
  "Create a modern ecommerce website with strong SEO, a product list with images on the home page, a cart, a checkout flow, order creation, and an invoice with payment instructions." \
  --kilocode
```

Example output (summary):

- Created:
  - `specs/ecommerce/ecommerce_shop_front/spec.md`
  - `specs/ecommerce/ecommerce_checkout_flow/spec.md`
  - `specs/ecommerce/ecommerce_order_billing/spec.md`

- Next steps (choose the line that matches how you ran this workflow):

  **CLI**
  - `/smartspec_generate_spec --spec-ids=ecommerce_shop_front`
  - `/smartspec_generate_plan --spec specs/ecommerce/ecommerce_shop_front/spec.md`
  - `/smartspec_generate_tasks --spec specs/ecommerce/ecommerce_shop_front/spec.md`

  **Kilo Code**
  - `/smartspec_generate_spec.md --spec-ids=ecommerce_shop_front --kilocode`
  - `/smartspec_generate_plan.md --spec specs/ecommerce/ecommerce_shop_front/spec.md --kilocode`
  - `/smartspec_generate_tasks.md --spec specs/ecommerce/ecommerce_shop_front/spec.md --kilocode`

### 11.2 Force everything into a single spec

#### CLI Example

```bash
/smartspec_generate_spec_from_prompt \
  "Create an end-to-end ecommerce website specification that covers catalog browsing, product search, cart, checkout, order management, and invoice generation in a single cohesive spec." \
  --max-specs=1
```

#### Kilo Code Example

```bash
/smartspec_generate_spec_from_prompt.md \
  "Create an end-to-end ecommerce website specification that covers catalog browsing, product search, cart, checkout, order management, and invoice generation in a single cohesive spec." \
  --kilocode \
  --max-specs=1
```

### 11.3 Miniapp with external AI image generation

#### CLI Example

```bash
/smartspec_generate_spec_from_prompt \
  "Create a miniapp where users can upload images and type a short description, then send the request to an external image generation API, with a basic history view." \
  --spec-category=miniapp
```

#### Kilo Code Example

```bash
/smartspec_generate_spec_from_prompt.md \
  "Create a miniapp where users can upload images and type a short description, then send the request to an external image generation API, with a basic history view." \
  --kilocode \
  --spec-category=miniapp
```

---

## 14) Patch Notes (v5.7.3)

- Added Production Output Contract (deterministic audit summary, no prompt echo).
- Default category fallback clarified to `feature` when inference is ambiguous.
- Hardened write-guard intent: explicitly forbids creating/modifying tasks/design/ui/schema/testplan/registries.
- Clarified Kilo subtask control as platform-level (no invented flags).

---

## 15) Patch Notes (v5.7.2)

- Added security hardening checklist: realpath/normalize, block traversal/symlink escape, atomic index updates.
- Clarified `--update-index` concurrency behavior in Kilo mode (lock or fallback to JSON snippets).
- Renumbered sections after inserting security hardening checklist.

---

## 16) Patch Notes (v5.7.1)

- Enforced documentation + output guidance for dual-command rendering.
- Clarified multi-repo delimiter handling for `--workspace-roots`.
- Tightened write-scope governance for `--output-dir` and SPEC_INDEX updates.
- Improved collision handling when target folder exists without `spec.md`.
- Added optional `--language` for deterministic locale control.

---

End of `/smartspec_generate_spec_from_prompt` workflow spec v5.7.3.

