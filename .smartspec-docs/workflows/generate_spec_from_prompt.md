| manual_name | manual_version | compatible_workflow | compatible_workflow_versions | role |
| --- | --- | --- | --- | --- |
| /smartspec_generate_spec_from_prompt Manual (EN) | 5.6 | /smartspec_generate_spec_from_prompt | 5.6.x | developer/operator manual (feature bootstrap, product, frontend, backend) |

# /smartspec_generate_spec_from_prompt Manual (v5.6, English)

## 1. Overview

This manual explains how to use the workflow:

> `/smartspec_generate_spec_from_prompt v5.6.x`

The workflow creates **starter `spec.md` files directly from a natural language prompt**, using your existing SmartSpec project structure as context. It is designed for:

- teams that have an idea or feature description but **no spec yet**, and
- users who want a **simple, one-command way** to bootstrap specs before refining them.

Key properties:

- role: Execution (writes new `spec.md` files)
- write_guard: ALLOW-WRITE, but **limited to `specs/**` and optional SPEC_INDEX updates**
- safety-mode: normal, with **no destructive edits to existing specs**

Typical flow:

1. You describe the feature in Thai or English in a single prompt.
2. The workflow analyses the prompt + project context and decides:
   - which category to use (e.g. `ecommerce`, `miniapp`, `admin`),
   - how many specs are needed (1–3 by default, up to 5 with a flag),
   - unique `spec-id`s for each spec.
3. It creates one or more folders under `specs/<category>/<spec-id>/spec.md`.
4. You then run `/smartspec_generate_spec --spec-ids=<id>` to refine each spec.

> **Important:** This workflow is a **bootstrap step only**. For ongoing work,
> `/smartspec_generate_spec` remains the primary spec refinement workflow.

---

## 2. What’s New in v5.6

`/smartspec_generate_spec_from_prompt` is a **new workflow in the 5.6 line**. It does not replace any existing workflow.

### 2.1 Prompt → multi-spec bootstrap

- Takes a single prompt and can generate **1–5 specs** for a feature.
- Auto-splits big features (e.g. ecommerce shop) into logical specs like:
  - `ecommerce_shop_front`
  - `ecommerce_checkout_flow`
  - `ecommerce_order_billing`

### 2.2 Safe write scope

- Writes only under `specs/**`.
- Never overwrites an existing `spec.md`.
- If a `spec-id` already exists, a suffixed id (e.g. `_v2`) is used and called out in the summary.

### 2.3 Explicit SPEC_INDEX updates

- SPEC_INDEX is **never modified automatically**.
- Only when `--update-index` is provided and `.spec/SPEC_INDEX.json` is found and writable will the workflow append entries.
- Otherwise, it prints JSON snippets for manual insertion into the index.

### 2.4 SPEC-first content

The generated specs follow the **SPEC-first rules from the governance knowledge base**, including:

- context and goals,
- user roles and journeys,
- screens and flows,
- external integrations (payments, auth, AI, etc.),
- data models and persistence hints,
- non-functional requirements (SEO, performance, security, observability),
- v2+ enhancement ideas.

---

## 3. Backward Compatibility Notes

- New in v5.6; no legacy behaviour to preserve.
- No flags or behaviours are removed from other workflows.
- Follows the same semantics for:
  - `--workspace-roots`, `--repos-config`,
  - `--registry-dir`, `--registry-roots`,
  - `--specindex`, `--kilocode`,
  as other SmartSpec workflows.

---

## 4. Core Concepts

### 4.1 Starter specs vs refined specs

- **Starter spec** (this workflow):
  - Created from a prompt + light project context.
  - Detailed enough to plan tasks and discuss with stakeholders.
  - Not yet fully aligned with all project-wide constraints.

- **Refined spec** (`/smartspec_generate_spec`):
  - Uses more project files, registries, and prior specs.
  - Ensures consistency and governance across the portfolio.

### 4.2 Categories & `spec-id`s

The workflow tries to infer a suitable category and spec-id from:

- existing entries in `.spec/SPEC_INDEX.json`,
- existing `specs/<category>/<spec-id>/` patterns,
- keywords in your prompt.

If nothing matches, it falls back to a safe default category (e.g. `feature`) and a slugged `spec-id` built from your prompt.

### 4.3 Auto-splitting features

By default (`--max-specs=3`), a large feature may be split into multiple specs. Example splits:

- `*_front` vs `*_checkout` vs `*_billing`
- `*_user_app` vs `*_admin_console`
- `*_core_flow` vs `*_advanced_features`

This keeps each spec focused and easier to implement.

---

## 5. Quick Start Examples

### 5.1 First-time ecommerce website spec (single repo)

```bash
/smartspec_generate_spec_from_prompt \
  "Create a modern ecommerce website with strong SEO, showing featured products and product images on the home page, allowing users to add items to a cart, proceed to checkout, place an order, and receive an invoice with payment instructions."


Typical result (summary):

- Created:
  - `specs/ecommerce/ecommerce_shop_front/spec.md`
  - `specs/ecommerce/ecommerce_checkout_flow/spec.md`
  - `specs/ecommerce/ecommerce_order_billing/spec.md`
- Recommended follow-up commands:
  - `/smartspec_generate_spec --spec-ids=ecommerce_shop_front`
  - `/smartspec_generate_spec --spec-ids=ecommerce_checkout_flow`
  - `/smartspec_generate_spec --spec-ids=ecommerce_order_billing`

### 5.2 Single-spec mode

If you prefer a single spec for the whole feature:

```bash
/smartspec_generate_spec_from_prompt \
  "สร้าง website ecommerce ตั้งแต่หน้าแคตตาล็อกจนถึง invoice แบบครบวงจร" \
  --max-specs=1
```

Result:

- Created: `specs/ecommerce/ecommerce_shop_full/spec.md`
- Next: `/smartspec_generate_spec --spec-ids=ecommerce_shop_full`

### 5.3 Miniapp with AI integration (e.g. Kie.ai)

```bash
/smartspec_generate_spec_from_prompt \
  "สร้าง miniapp ให้ผู้ใช้ upload รูปภาพ 5 รูป + พิมพ์ข้อความภาษาไทย แล้วใช้ Kie.ai / Google Nano Banana Pro แปลงข้อความเป็น prompt ที่สมบูรณ์และเจนภาพกลับมา พร้อมหน้า gallery เก็บประวัติ"
```

Result (example split):

- `specs/miniapp/miniapp_nano_banana_core/spec.md`
- `specs/miniapp/miniapp_nano_banana_gallery/spec.md`

Next steps:

- `/smartspec_generate_spec --spec-ids=miniapp_nano_banana_core`
- `/smartspec_generate_spec --spec-ids=miniapp_nano_banana_gallery`

### 5.4 Kilo usage (project-wide context)

```bash
/smartspec_generate_spec_from_prompt.md \
  "สร้าง mobile + web app สำหรับ membership พร้อมระบบแต้มสะสม" \
  --kilocode
```

On Kilo:

- Orchestrator can split work by spec-id if multiple specs are required.
- Code mode writes only under `specs/**`.

---

## 6. CLI / Flags Cheat Sheet

- **Core**
  - positional prompt (required)
  - `--spec-category=<category>`
  - `--max-specs=<n>` (default: 3, range 1–5)
  - `--output-dir=<path>` (default: `specs`)
- **Index & multi-repo**
  - `--update-index` (append to `.spec/SPEC_INDEX.json` when safe)
  - `--specindex=<path>`
  - `--workspace-roots=<paths>`
  - `--repos-config=<path>`
- **Registries (read-only)**
  - `--registry-dir=<path>`
  - `--registry-roots=<paths>`
- **Safety & Kilo**
  - `--dry-run`
  - `--kilocode`

Remember: leaving out all flags is valid and recommended for first-time users.

---

## 7. Best Practices

1. **Write a rich prompt**
   - Describe:
     - target users,
     - key flows/screens,
     - integrations (payments, AI, auth),
     - SEO/performance expectations.

2. **Use `--dry-run` when unsure**
   - See planned categories/spec-ids before creating files.

3. **Review each generated spec once**
   - Check that splits make sense.
   - Adjust naming if needed.

4. **Always follow up with `/smartspec_generate_spec`**
   - This aligns the starter specs with the rest of the project.

5. **Combine with project copilot**
   - After generating specs, use `/smartspec_project_copilot` to see how
     they fit into the overall roadmap and which workflows to run next.

---

## 8. FAQ / Troubleshooting

**Q1: It created too many specs. What should I do?**  
Use `--max-specs=1` or `2` to limit splits. You can also merge scopes manually in the generated specs.

**Q2: It says SPEC_INDEX was not updated. Is that a problem?**  
No; your specs still exist under `specs/**`. You can either:

- re-run with `--update-index`, or
- copy the printed JSON snippets into `.spec/SPEC_INDEX.json` manually.

**Q3: Can I overwrite an existing spec?**  
This workflow intentionally **never overwrites** existing `spec.md`. If you really need to, edit the file manually or use a different workflow under controlled conditions.

**Q4: How detailed are the generated specs?**  
They aim to be detailed enough to drive planning and implementation, but you should expect to refine them using `generate_spec` and normal review processes.

---

End of `/smartspec_generate_spec_from_prompt v5.6.x` manual (English).

