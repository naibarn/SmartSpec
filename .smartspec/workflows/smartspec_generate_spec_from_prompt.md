# /smartspec_generate_spec_from_prompt v5.6.0

## Summary

Generate one or more starter `spec.md` files directly from a natural language
prompt, using existing project structure as context.

This workflow is designed for **first-time spec creation** from a prompt. After
it creates starter specs, you should refine them with
`/smartspec_generate_spec`.

- role: Execution
- write_guard: ALLOW-WRITE (limited to `specs/**` and optional SPEC_INDEX
  updates)
- safety-mode: normal (no destructive edits to existing specs)

Key safety constraints:

- Never delete or overwrite existing `spec.md` files.
- Only create new spec folders/files under `specs/**`.
- SPEC_INDEX is updated **only when explicitly requested** via
  `--update-index`.

---

## When to Use

Use this workflow when:

- you have an idea/requirement like:

  > "สร้าง website ที่สวยงาม ทันสมัย มี SEO ที่ดี แสดงรายการสินค้าและรูปภาพ\
  > บนหน้าแรก มีตะกร้าสินค้า / checkout / order / invoice"

- and your project does **not yet** have a detailed `spec.md` for it.

It is **not** meant to replace `/smartspec_generate_spec`. Instead:

1. Run `/smartspec_generate_spec_from_prompt` once to create starter specs.
2. Then use `/smartspec_generate_spec --spec-ids=<...>` to refine and keep
   them aligned with the broader project.

---

## Inputs & Outputs

### Inputs

- **Positional prompt (required)**  
  Natural language requirement, in Thai or English.

  ```bash
  /smartspec_generate_spec_from_prompt "<requirement text>"
  ```

- Optional context from the project (auto-detected, no flags required):
  - `.spec/SPEC_INDEX.json` or other index locations (see "Folders").
  - Existing `specs/**/spec.md` naming patterns.
  - Registries under `.spec/registry/**` for design systems and tools.

### Outputs

- One or more new folders under `specs/<category>/<spec-id>/` with:
  - `spec.md` – a **complete starter spec**, aligned with governance rules.

- Optional SPEC_INDEX update:
  - If `--update-index` is passed and `.spec/SPEC_INDEX.json` exists and is
    writable, the workflow appends new entries.
  - Without `--update-index`, it **does not modify** SPEC_INDEX and instead
    prints JSON snippets the user can paste in manually.

This keeps the workflow safe for first-time use in existing projects.

---

## Modes (Role, Write Guard, Safety)

- **Role**: Ask/Architect + Implement (spec writer).
- **write_guard**: ALLOW-WRITE, strictly limited to:
  - creating new folders under `specs/**`,
  - creating new `spec.md` files,
  - appending to `.spec/SPEC_INDEX.json` **only** when `--update-index` is
    set.
- **safety-mode**:
  - `normal` only; this workflow does not support aggressive overwrite.
  - It must **never overwrite an existing `spec.md`**; when a spec-id already
    exists, it creates a suffixed `spec-id` and explains the decision.

---

## CLI Usage & Flags

### 1) Simple usage (recommended)

```bash
/smartspec_generate_spec_from_prompt "สร้าง website ที่สวยงาม ทันสมัย มี SEO ที่ดี..."
```

The workflow will:

1. Inspect the project to understand existing categories/spec IDs.
2. Derive a suitable category and `spec-id` or multiple spec-ids.
3. Generate starter specs under `specs/<category>/<spec-id>/`.
4. Print which files were created and how to refine them with
   `/smartspec_generate_spec`.

### 2) Optional flags (kept minimal)

To keep the user experience simple, flags are optional and limited:

- `--spec-category=<category>`  
  Override the inferred category (e.g. `ecommerce`, `miniapp`, `admin`).

- `--max-specs=<n>` (default: `3`, range `1–5`)  
  Maximum number of specs to split into when the feature is large.

- `--output-dir=<path>` (default: `specs`)  
  Root folder where new specs are created.

- `--update-index`  
  When set, append new spec entries to `.spec/SPEC_INDEX.json` if found and
  writable. Without this flag, SPEC_INDEX is never modified.

- `--dry-run`  
  Show planned categories, spec-ids, and a short outline **without** writing
  any files.

- `--specindex=<path>`  
  Override auto-detected SPEC_INDEX location.

- `--workspace-roots=<paths>`  
  Optional multi-repo support. Semantics match other workflows: a `;`-separated
  list of workspace roots to search for `specs/**` and indexes.

- `--repos-config=<path>`  
  Optional multi-repo layout configuration, same semantics as in other
  workflows.

- `--registry-dir=<path>` / `--registry-roots=<paths>`  
  Optional overrides for design-system and tool registries; used read-only to
  suggest UI stacks and patterns.

- `--kilocode`  
  Enable Kilo Orchestrator behaviour according to governance rules.

### 3) Kilo usage

```bash
/smartspec_generate_spec_from_prompt.md \
  "สร้าง website ที่สวยงาม ทันสมัย มี SEO ที่ดี..." \
  --kilocode
```

On Kilo:

- Orchestrator can split work by spec-id if multiple specs are created.
- Code mode writes new `spec.md` files under `specs/**` only.

---

## Canonical Folders & File Placement

This workflow must respect the standard layout:

- Specs:

  ```text
  specs/<category>/<spec-id>/spec.md
  ```

- SPEC index (auto-detection order, unless `--specindex` is set):

  1. `.spec/SPEC_INDEX.json`
  2. `SPEC_INDEX.json` at repo root
  3. `.smartspec/SPEC_INDEX.json`
  4. `specs/SPEC_INDEX.json`
  
  If none is found:
  - create spec folders/files anyway, and
  - print a warning with a suggestion to create `.spec/SPEC_INDEX.json`.

- Registries (read-only):

  - `.spec/registry/**` are used to:
    - infer design systems and UI stacks,
    - prefer App components and patterns over raw UI components,
    - suggest patterns for layout and states.

---

## Behaviour & Step-by-step Flow

1. **Read context & KBs**  
   - Load governance and install/usage KBs.  
   - Detect SPEC index and existing spec naming patterns.

2. **Parse the prompt**  
   - Extract key domains:
     - product/feature (e.g. ecommerce shop),
     - core flows (home, catalog, cart, checkout, orders, invoices),
     - external integrations (payments, email, AI, etc.),
     - SEO, performance, NFR-related hints.

3. **Decide category & `spec-id`(s)**  
   - Infer `category` (e.g. `ecommerce`, `feature`, `miniapp`) from:
     - existing categories in SPEC_INDEX,
     - keywords in the prompt.
   - Construct slugged `spec-id`s, e.g.:
     - `ecommerce_shop_front`
     - `ecommerce_checkout_flow`
     - `ecommerce_order_billing`
   - Keep the number of specs ≤ `--max-specs`.

4. **Ensure uniqueness & safety**  
   - Check for existing folders under `specs/<category>/<spec-id>/`:
     - if a folder with `spec.md` exists → DO NOT overwrite.
       - choose a new spec-id with a numeric suffix, e.g.
         `ecommerce_shop_front_v2`.
       - mention this clearly in the output.

5. **Generate starter `spec.md` content**  
   For each new spec:

   - Write a detailed SPEC including, where relevant:
     - context & goals,
     - user roles & journeys,
     - screens & flows (with modern UI guidance),
     - external integrations (auth, payments, AI, etc.),
     - data models and persistence,
     - NFR (SEO, performance, security, observability),
     - v2+ enhancements.

   - The content must follow the SPEC-first and miniapp rules described in the
     governance KB.  
   - It MUST be strong enough to drive `/smartspec_generate_spec`,
     `/smartspec_generate_plan`, and downstream workflows.

6. **Write files & optionally update SPEC_INDEX**  
   - Create folders and `spec.md` under `specs/<category>/<spec-id>/`.
   - If `--update-index` is set and `.spec/SPEC_INDEX.json` is available and
     writable:
     - append entries for each new spec-id.
   - Otherwise:
     - print JSON snippets that the user can paste into SPEC_INDEX.

7. **Output summary & next steps**  
   - List each created spec with:
     - folder path,
     - short description,
     - recommended next command, e.g.:

       ```bash
       /smartspec_generate_spec --spec-ids=ecommerce_shop_front
       ```

   - Suggest running, as appropriate:
     - `/smartspec_generate_plan`,
     - `/smartspec_generate_tasks`,
     - `/smartspec_generate_tests`,
     - `/smartspec_ci_quality_gate`,
     - `/smartspec_release_readiness` after implementation.

---

## KiloCode Support (Meta-Flag)

- Flag: `--kilocode` (universal, required by governance).

Behaviour under Kilo:

- Role remains Execution but write scope is still limited to `specs/**` and
  optional SPEC_INDEX updates when `--update-index` is set.
- Orchestrator-per-task is allowed and may split by spec-id when multiple
  specs are generated.
- `--nosubtasks` (if supported globally) must disable Orchestrator split.

The workflow must **not** enable Orchestrator unless `--kilocode` is present.

---

## Weakness & Risk Check

Before finishing, the workflow should self-assess and report:

- **Prompt quality dependence**  
  - Weak/ambiguous prompts may produce poor specs.  
  - Mitigation: suggest 3–5 ways the user could refine their prompt or the
    generated specs.

- **Context mismatch**  
  - If SPEC_INDEX or registries are missing/outdated, inferred categories and
    data models may not match reality.  
  - Mitigation: surface clear warnings and encourage running
    `/smartspec_project_copilot` and `/smartspec_generate_spec` to align.

- **Security & data sensitivity**  
  - Prompts may contain sensitive data; avoid logging them verbatim into
    long-lived reports.  
  - Use placeholders for secrets/tokens in any suggested integrations.

- **Oversplitting vs undersplitting**  
  - Auto-splitting into too many specs can fragment the design; not splitting
    enough can create monolithic specs.  
  - Mitigation: explain the split rationale and suggest alternative splits in
    the summary.

- **Write-scope safety**  
  - Re-affirm in the summary that no existing `spec.md` files were modified
    and that SPEC_INDEX was only changed if `--update-index` was provided.

---

## Legacy Flags Inventory

This is a **new** workflow in v5.6.0, so:

- Kept: N/A
- Alias: N/A
- New:
  - positional prompt argument (required),
  - `--spec-category`,
  - `--max-specs`,
  - `--output-dir`,
  - `--update-index`,
  - `--dry-run`,
  - `--specindex`,
  - `--workspace-roots`,
  - `--repos-config`,
  - `--registry-dir`, `--registry-roots`,
  - `--kilocode` (universal).

All flags are additive and do not conflict with existing workflows.

---

## Quick Start Examples

### 1) Simple ecommerce website (single repo)

```bash
/smartspec_generate_spec_from_prompt \
  "สร้าง website ที่สวยงาม ทันสมัย มี SEO ที่ดี แสดงรายการสินค้าและรูปภาพสินค้าบนหน้าแรก มีให้กดใส่ตะกร้า แล้วไปหน้า checkout สร้าง order และ invoice พร้อมรายละเอียดการโอนเงิน"
```

Example output (summary):

- Created:
  - `specs/ecommerce/ecommerce_shop_front/spec.md`
  - `specs/ecommerce/ecommerce_checkout_flow/spec.md`
  - `specs/ecommerce/ecommerce_order_billing/spec.md`
- Next steps:
  - `/smartspec_generate_spec --spec-ids=ecommerce_shop_front`
  - `/smartspec_generate_spec --spec-ids=ecommerce_checkout_flow`
  - `/smartspec_generate_spec --spec-ids=ecommerce_order_billing`

### 2) Force everything into a single spec

```bash
/smartspec_generate_spec_from_prompt \
  "สร้าง website ecommerce ตั้งแต่หน้าแคตตาล็อกจนถึง invoice แบบครบวงจร" \
  --max-specs=1
```

### 3) Kilo usage

```bash
/smartspec_generate_spec_from_prompt.md \
  "สร้าง miniapp ให้ผู้ใช้ upload รูป + พิมพ์ข้อความไทย แล้วยิงไป Kie.ai" \
  --kilocode
```

On Kilo, Orchestrator may split by spec-id, but writes remain limited to
`specs/**` plus optional SPEC_INDEX updates controlled by `--update-index`.

---

End of `/smartspec_generate_spec_from_prompt` workflow spec v5.6.0.

