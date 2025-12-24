---
workflow_id: smartspec_generate_tasks
version: "7.1.3"
status: active
category: core
platform_support:
  - cli
  - kilo
requires_apply: false
writes:
  - ".spec/reports/**"
  - "specs/**/tasks.md (only with --apply)"
---

# /smartspec_generate_tasks

## Purpose
Generate หรือ refine `tasks.md` จาก `spec.md` (หรือ `plan.md` / `ui-spec.json`) โดยเน้น:

- **preview-first governance**
- **evidence hook เป็น machine-parseable** เพื่อลด verify false-negative
- **merge ได้** เมื่อมี `tasks.md` อยู่แล้ว (คง task IDs เดิม + normalize รูปแบบ)

## Governance contract (สำคัญ)
- Without `--apply` (รวมถึง `--validate-only`):
  - MUST NOT modify any file under `specs/**`
  - MUST only write outputs under `.spec/reports/generate-tasks/**`
  - MUST NOT auto-fix โดยไปแก้ `specs/**/tasks.md` (แม้ validation fail)
- With `--apply`:
  - MAY update/create `specs/<category>/<spec-id>/tasks.md`
  - MUST write atomically (temp+rename)
  - MUST NOT write outside `specs/<category>/<spec-id>/tasks.md`

> หมายเหตุ: เอกสารนี้ตั้งใจหลีกเลี่ยงการใส่บรรทัดที่ทำให้ agent ตีความผิดว่าเป็น “คำสั่งให้สร้าง/รันสคริปต์ย่อย”

## Inputs (positional)
Primary input is positional (ต้องอยู่ใต้ `specs/**`):

- `specs/<category>/<spec-id>/spec.md`
- หรือ `specs/<category>/<spec-id>/plan.md`
- หรือ `specs/<category>/<spec-id>/ui-spec.json`

## Flags
- `--apply`: อนุญาตให้เขียน `specs/**/tasks.md`
- `--validate-only`: ทำ preview + validation เท่านั้น (no governed writes)

## Outputs
- Preview: `.spec/reports/generate-tasks/<run-id>/preview/<spec-id>/tasks.md`
- Diff/Patch: `.spec/reports/generate-tasks/<run-id>/diff/<spec-id>.patch`
- Report: `.spec/reports/generate-tasks/<run-id>/report.md`

## Evidence hook policy (MUST)
Generated tasks MUST use canonical evidence lines only:

- `evidence: code path=... symbol=...`
- `evidence: code path=... contains="..."`
- `evidence: docs path=... heading="..."`
- `evidence: test path=... command="..."` (command เป็น informational เท่านั้น)
- `evidence: ui path=... selector="..."`

Hard rules:
- `path=` ต้องเป็น repo-relative path (ห้ามเป็นคำสั่ง)
- ถ้า value มีช่องว่าง ต้องใส่ double quotes
- ห้ามใช้ glob ใน `path=` เช่น `src/**/*.ts`
- ถ้าเป็นเอกสาร/สเปค (เช่น `openapi.yaml`) และต้องการ `heading=` ให้ใช้ `docs` ไม่ใช่ `code`

## Invocation

**CLI:**
```bash
/smartspec_generate_tasks specs/<category>/<spec-id>/spec.md --validate-only
```

**Kilo Code:**
```bash
/smartspec_generate_tasks.md specs/<category>/<spec-id>/spec.md --validate-only --platform kilo
```

## Apply mode

**CLI:**
```bash
/smartspec_generate_tasks specs/<category>/<spec-id>/spec.md --apply
```

**Kilo Code:**
```bash
/smartspec_generate_tasks.md specs/<category>/<spec-id>/spec.md --apply --platform kilo
```

## Implementation notes
- Validation script (repo): `.smartspec/scripts/validate_tasks_enhanced.py`
- Evidence normalization helper (repo): `.smartspec/scripts/migrate_evidence_hooks.py`
- ห้ามสร้าง script ที่ root หรือ `.spec/scripts` (path canonical คือ `.smartspec/scripts/**`)

