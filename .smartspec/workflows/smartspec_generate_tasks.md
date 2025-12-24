---
workflow_id: smartspec_generate_tasks
version: "7.2.0"
status: active
category: core
platform_support:
  - cli
  - kilo
requires_apply: false
writes:
  - ".spec/reports/**"
  - "specs/**/tasks.md (ONLY with --apply)"
---

# /smartspec_generate_tasks

## Purpose
Generate หรือ refine `tasks.md` จาก `spec.md` (หรือ `plan.md` / `ui-spec.json`) โดยเน้น:

- **preview-first governance** (validate-only / default = ไม่แตะไฟล์ governed)
- output `tasks.md` ที่ **strict evidence hook parse ได้จริง** เพื่อลด verify false-negative
- **merge ได้** เมื่อมี `tasks.md` อยู่แล้ว (คง task IDs เดิม + normalize รูปแบบ)

---

## Governance contract (MUST)

### Path scope (MUST)
- Input file MUST be under `specs/**`.
- Without `--apply`: MUST NOT modify any file under `specs/**`.
- With `--apply`: MAY write ONLY `specs/<category>/<spec-id>/tasks.md`.

### `--apply` behavior (MUST)

**Without `--apply` (includes `--validate-only`):**
- MUST NOT modify `specs/**/tasks.md`.
- MUST write preview bundle ONLY under `.spec/reports/generate-tasks/<run-id>/...`.
- MUST NOT create any helper scripts anywhere (เช่น `fix_evidence.py`) ไม่ว่าจะใน root หรือโฟลเดอร์ใด ๆ.
- MUST NOT attempt “auto-fix” โดยไปแก้ไฟล์จริง แม้ validation fail.

**With `--apply`:**
- MAY update/create `specs/<category>/<spec-id>/tasks.md`.
- MUST write atomically (temp+rename).
- MUST NOT modify any other governed files.

### No network / no shell (MUST)
- Workflow นี้ต้องทำงานได้โดยไม่ต้อง network. ถ้าขั้นตอนไหนต้อง network ให้แยก workflow และต้อง require `--allow-network`.
- ห้ามแนะนำ `sh -c` หรือการ run shell ที่ไม่ allowlisted.

### Script location (MUST)
- Maintained scripts MUST be referenced under `.smartspec/scripts/`.
- `.spec/` is reserved for reports/outputs only.

---

## Inputs
Primary input is positional (MUST exist) และต้องอยู่ใต้ `specs/**`:

- `specs/<category>/<spec-id>/spec.md`
- หรือ `specs/<category>/<spec-id>/plan.md`
- หรือ `specs/<category>/<spec-id>/ui-spec.json`

---

## Flags
- `--apply`: อนุญาตให้เขียน `specs/**/tasks.md`
- `--validate-only`: ทำ preview + validation เท่านั้น (no governed writes)
- `--json`: ให้ report มี summary เป็น JSON เพิ่ม

---

## Outputs
All outputs MUST be under `.spec/reports/generate-tasks/<run-id>/`:

- Preview tasks:
  - `.spec/reports/generate-tasks/<run-id>/preview/<spec-folder>/tasks.md`
- Patch (diff):
  - `.spec/reports/generate-tasks/<run-id>/diff/<spec-id>.patch`
- Report:
  - `.spec/reports/generate-tasks/<run-id>/report.md`
  - `.spec/reports/generate-tasks/<run-id>/report.json` (when `--json`)
- Optional backup bundle (only when `--apply`):
  - `.spec/reports/generate-tasks/<run-id>/backup/<spec-folder>/tasks.md`

---

## Evidence hook policy (MUST)
Generated tasks MUST use **canonical evidence hook** เท่านั้น:

### Canonical format
- `evidence: <code|test|docs|ui> key=value key="value with spaces" ...`

### Allowed types + keys
- `code`: `path` (required), optional `symbol`, `contains`, `regex`
- `test`: `path` (required), optional `command`, `contains`, `regex`
- `docs`: `path` (required), optional `heading`, `contains`, `regex`
- `ui`: `path` (required), optional `selector`, `contains`, `regex`

### Hard rules
- `path=` MUST be repo-relative path (ห้ามเป็นคำสั่ง)
- ถ้า value มีช่องว่าง MUST ใส่ double quotes เช่น:
  - ✅ `command="npx prisma validate"`
  - ❌ `command=npx prisma validate`
- ห้ามใช้ glob ใน `path=` เช่น `src/**/*.ts`
- ถ้าเป็น directory ให้ใช้ `symbol=Directory` (แนะนำ) แทนการพึ่งพา path ลงท้าย `/`
- ถ้าเป็นเอกสาร/สเปคและต้องการ `heading=` ให้ใช้ `docs` ไม่ใช่ `code` เช่น:
  - ✅ `evidence: docs path=openapi.yaml heading="OpenAPI"`

---

## Validation (MUST)
Workflow MUST validate the **preview tasks** ด้วยสคริปต์ canonical ใน repo:

1) Evidence hooks:
```bash
python3 .smartspec/scripts/validate_evidence_hooks.py .spec/reports/generate-tasks/<run-id>/preview/<spec-folder>/tasks.md
```

2) Tasks structure (header table / sections / IDs):
```bash
python3 .smartspec/scripts/validate_tasks_enhanced.py .spec/reports/generate-tasks/<run-id>/preview/<spec-folder>/tasks.md --spec specs/<category>/<spec-id>/spec.md
```

Validation rules:
- Fail เมื่อ evidence ไม่ parse ได้ (เช่น stray tokens เพราะไม่ได้ quote)
- Allow `path-only` evidence เป็น warning ได้ เพื่อไม่ตัด evidence แบบ existence ทิ้งแบบผิด ๆ

If any validator fails:
- MUST exit non-zero
- MUST NOT apply changes

---

## Invocation

### Validate-only (preview-first)

**CLI:**
```bash
/smartspec_generate_tasks specs/<category>/<spec-id>/spec.md --validate-only
```

**Kilo Code:**
```bash
/smartspec_generate_tasks.md specs/<category>/<spec-id>/spec.md --validate-only --platform kilo
```

### Apply (writes governed)

**CLI:**
```bash
/smartspec_generate_tasks specs/<category>/<spec-id>/spec.md --apply
```

**Kilo Code:**
```bash
/smartspec_generate_tasks.md specs/<category>/<spec-id>/spec.md --apply --platform kilo
```

---

## Behavior when `tasks.md` already exists
When `specs/<category>/<spec-id>/tasks.md` exists:

- In validate-only:
  - MUST read existing tasks for merge planning
  - MUST write merged result ONLY to preview path under `.spec/reports/**`
  - MUST NOT modify existing tasks file

- In apply:
  - MUST preserve existing task IDs where possible
  - MUST normalize evidence hooks to canonical format
  - MUST produce an atomic update to the tasks file

---

## Common failure modes and required handling

### 1) “validate-only แต่เหมือนแก้ tasks.md”
Hard violation: `--validate-only` MUST NOT modify any file under `specs/**`.

### 2) “สร้าง script เพิ่มใน root (fix_evidence.py)”
Hard violation: MUST NOT create ad-hoc scripts. If fixes are needed, they must be done in-memory and written only to `.spec/reports/**`.

### 3) “พยายามเรียกสคริปต์ใน .spec/scripts/”
Hard violation: `.spec/` is outputs only. Scripts must be in `.smartspec/scripts/`.

---

## Related workflows
- `/smartspec_migrate_evidence_hooks` (normalize existing tasks evidence; quote command/contains etc.)
- `/smartspec_verify_tasks_progress_strict` (read-only strict verify)

