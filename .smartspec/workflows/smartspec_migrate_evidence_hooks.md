---
workflow_id: smartspec_migrate_evidence_hooks
version: "7.1.1"
status: active
category: maintenance
platform_support:
  - cli
  - kilo
requires_apply: false
writes:
  - ".spec/reports/**"
  - "specs/**/tasks.md (ONLY with --apply)"
---

# /smartspec_migrate_evidence_hooks

## Purpose
Normalize legacy evidence hooks ใน `tasks.md` ให้กลายเป็น **canonical evidence hooks** ที่ strict verifier / strict validator อ่านได้จริง เพื่อลดปัญหา verify false-negative.

เป้าหมายหลัก:
- แก้เคส evidence เก่าที่มี **unquoted values with spaces** (เช่น `command=npx prisma validate`) ให้เป็น `command="..."`
- แก้เคส `test` evidence ที่ไม่มี `path=` (เติม anchor ให้)
- แปลง evidence ที่เป็น “command-ish line” ให้เป็น `evidence: test path=<anchor> command="..."`
- เปลี่ยน `code + heading` ที่ชี้ไปไฟล์เอกสาร/สเปค ให้เป็น `docs` เพื่อหลีกเลี่ยง mismatch

---

## Governance contract (MUST)

### Preview-first (MUST)
- Default mode (ไม่มี `--apply`) ต้องเป็น **preview-only**.
- Preview-only MUST NOT modify any governed files under `specs/**`.
- Preview artifacts MUST be written only under `.spec/reports/migrate-evidence-hooks/<run-id>/`.

### Governed writes (MUST)
- การแก้ไฟล์จริงภายใต้ `specs/**` ต้องทำเฉพาะเมื่อใส่ `--apply`.
- With `--apply`: MAY write ONLY `specs/**/tasks.md`.
- With `--apply`: MUST write atomically (temp + rename) และสร้าง backup.

### Refuse unsafe apply (MUST)
- MUST refuse `--apply` หาก `--tasks-file` ชี้ไปไฟล์ภายใต้ `.spec/reports/**` (ไฟล์ preview).

### No network / no shell (MUST)
- Workflow นี้ต้องทำงานได้โดยไม่ต้องใช้ network.
- ห้าม execute คำสั่งใด ๆ จาก evidence (command เป็นเพียง metadata).

### Script location (MUST)
- Maintained script MUST be referenced only under `.smartspec/scripts/`.
- `.spec/` เป็นพื้นที่ outputs/reports เท่านั้น

---

## Inputs

### Required
- `--tasks-file`: path ไปยัง `specs/**/tasks.md`

### Optional
- `--project-root`: default `.`

---

## Flags
- `--apply`: apply การแก้ไขลง `specs/**/tasks.md` (governed write)

---

## Outputs (always)
Outputs MUST be under `.spec/reports/migrate-evidence-hooks/<run-id>/`:
- `preview/<original-path>`: tasks ที่ถูก normalize แล้ว (preview)
- `diff.patch`: unified diff ระหว่าง original กับ preview
- `report.md`: สรุปการแก้ไข

---

## Canonical evidence hook rules (target output)
ทุก evidence line ต้องเป็น:

- `evidence: <code|test|docs|ui> key=value key="value with spaces" ...`

Constraints:
- `path=` ต้องเป็น repo-relative path (ห้ามเป็นคำสั่ง)
- ถ้า value มีช่องว่าง → ต้อง quote ด้วย double quotes
- `test` ต้องมี `path=` เสมอ (เป็น anchor file) แม้จะมี `command=`

---

## Implementation
Workflow นี้ต้องเรียก script canonical ต่อไปนี้เท่านั้น:

```bash
python3 .smartspec/scripts/migrate_evidence_hooks.py --tasks-file <specs/**/tasks.md> --project-root . [--apply]
```

---

## Invocation

### Preview-only (recommended first)

**CLI:**
```bash
/smartspec_migrate_evidence_hooks --tasks-file specs/<category>/<spec-id>/tasks.md
```

**Kilo Code:**
```bash
/smartspec_migrate_evidence_hooks.md --tasks-file specs/<category>/<spec-id>/tasks.md --platform kilo
```

### Apply (writes governed)

**CLI:**
```bash
/smartspec_migrate_evidence_hooks --tasks-file specs/<category>/<spec-id>/tasks.md --apply
```

**Kilo Code:**
```bash
/smartspec_migrate_evidence_hooks.md --tasks-file specs/<category>/<spec-id>/tasks.md --apply --platform kilo
```

---

## Recommended follow-up
หลัง preview หรือ apply ให้ run validators เพื่อยืนยันว่า evidence parse ได้:

1) Evidence hook validation:
```bash
python3 .smartspec/scripts/validate_evidence_hooks.py specs/<category>/<spec-id>/tasks.md
```

2) Tasks structure validation:
```bash
python3 .smartspec/scripts/validate_tasks_enhanced.py specs/<category>/<spec-id>/tasks.md --spec specs/<category>/<spec-id>/spec.md
```

3) Strict progress verify:

**CLI:**
```bash
/smartspec_verify_tasks_progress_strict specs/<category>/<spec-id>/tasks.md
```

**Kilo Code:**
```bash
/smartspec_verify_tasks_progress_strict.md specs/<category>/<spec-id>/tasks.md --platform kilo
```

---

## Troubleshooting

### “ยัง invalid เยอะหลัง migrate”
- ตรวจดูว่า evidence บางบรรทัดเป็นคนละ pattern (เช่น `evidence:` อยู่ใน code block) — ควรแก้ต้นทาง generator ให้ output canonical ตั้งแต่แรก
- ถ้า `command=` ยังไม่ quote แปลว่า line ไม่ผ่าน shlex หรือถูก embed ในรูปแบบอื่น ให้แก้ tasks formatting ให้เป็น plain markdown line

### “validate-only แต่ไปแก้ไฟล์จริง”
- ถือว่า workflow/script ผิด governance ต้องแก้ให้ preview-only ไม่แตะ `specs/**` เมื่อไม่มี `--apply`

