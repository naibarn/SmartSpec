---
workflow_id: smartspec_migrate_evidence_hooks
version: "6.5.1"
status: active
category: quality
platform_support:
  - cli
  - kilo
requires_apply: false
writes:
  - ".spec/reports/**"
  - "specs/**/tasks.md (only with --apply)"
---

# /smartspec_migrate_evidence_hooks

## Purpose
แปลง/ปรับรูปแบบ evidence ใน `specs/**/tasks.md` ให้เป็น **strict evidence hooks** ที่ workflow `/smartspec_verify_tasks_progress_strict` อ่านได้แน่นอน

รูปแบบ canonical ที่ต้องได้:

- `evidence: <code|test|docs|ui> key=value key="value with spaces" ...`

## Governance
- **Preview-first**: ถ้าไม่ใส่ `--apply` ต้อง **ห้ามแก้** ไฟล์ภายใต้ `specs/**` ทุกกรณี
- Output ที่อนุญาตใน preview: `.spec/reports/migrate-evidence-hooks/**`
- ถ้าใส่ `--apply` จึงจะเขียนกลับไปที่ `specs/**/tasks.md` ได้ (พร้อม backup + atomic write)

## Inputs
- `--tasks-file` (required): path ไปยัง `specs/<category>/<spec-id>/tasks.md`

## Outputs (always)
- Preview: `.spec/reports/migrate-evidence-hooks/<run-id>/preview/<tasks-file>`
- Diff: `.spec/reports/migrate-evidence-hooks/<run-id>/diff.patch`
- Report: `.spec/reports/migrate-evidence-hooks/<run-id>/report.md`

## Invocation

**CLI:**
```bash
/smartspec_migrate_evidence_hooks --tasks-file specs/<category>/<spec-id>/tasks.md
```

**Kilo Code:**
```bash
/smartspec_migrate_evidence_hooks.md --tasks-file specs/<category>/<spec-id>/tasks.md --platform kilo
```

## Apply mode

**CLI:**
```bash
/smartspec_migrate_evidence_hooks --tasks-file specs/<category>/<spec-id>/tasks.md --apply
```

**Kilo Code:**
```bash
/smartspec_migrate_evidence_hooks.md --tasks-file specs/<category>/<spec-id>/tasks.md --apply --platform kilo
```

## Implementation notes
- Script location (repo): `.smartspec/scripts/migrate_evidence_hooks.py`
- สคริปต์ต้องเป็น **read-only** ใน preview mode และต้องไม่รัน command ใด ๆ ใน evidence
- ถ้า script ไม่พบ ต้อง fail แบบชัดเจน (ห้ามสร้าง script ใน `.spec/scripts` หรือ root)

