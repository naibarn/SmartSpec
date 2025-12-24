---
workflow_id: smartspec_verify_tasks_progress_strict
version: "5.3.1"
status: active
category: verify
platform_support:
  - cli
  - kilo
requires_apply: false
writes:
  - ".spec/reports/**"
---

# /smartspec_verify_tasks_progress_strict

## Purpose
ตรวจสอบว่าแต่ละ task ใน `tasks.md` มี evidence ที่ **ค้นหาเจอจริงใน repo** เพื่อลดปัญหา “implement แล้ว แต่ verify ไม่พบ code”

## Inputs
- positional: `specs/<category>/<spec-id>/tasks.md`

## Evidence format (MUST)
Verifier รับเฉพาะบรรทัด evidence แบบ machine-parseable:

- `evidence: <code|test|docs|ui> key=value key="value with spaces" ...`

รองรับ `- evidence:` ด้วย (แต่จะ normalize เป็น `evidence:` ตอนประมวลผล)

## Matching policy (ลด false-negative)
- Task ถือว่า “ผ่าน” ถ้า evidence อย่างน้อย **1 บรรทัด** match
- `code`:
  - file exists + optional matcher (symbol/contains/regex)
  - ถ้า `symbol=Directory` จะ scan แบบ bounded ภายใน directory (จำกัดจำนวนไฟล์)
- `docs`:
  - file exists + optional `heading` (match แบบ loose: #/##/###)
- `test`:
  - `command=` เป็น informational เท่านั้น (ไม่ถูกรัน)
  - ตรวจ file anchor ที่ `path=` + optional matcher
- `ui`:
  - file exists + selector/contains/regex แบบ best-effort

## Governance
- Read-only (no writes)

## Invocation

**CLI:**
```bash
/smartspec_verify_tasks_progress_strict specs/<category>/<spec-id>/tasks.md
```

**Kilo Code:**
```bash
/smartspec_verify_tasks_progress_strict.md specs/<category>/<spec-id>/tasks.md --platform kilo
```

## Implementation notes
- Verifier script (repo): `.smartspec/scripts/verify_evidence_strict.py`
- ห้ามรัน `command=`; ใช้เพื่ออ้างอิงเท่านั้น

