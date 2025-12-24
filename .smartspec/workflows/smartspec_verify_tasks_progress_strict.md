---
workflow_id: smartspec_verify_tasks_progress_strict
version: "7.3.1"
status: active
category: verification
platform_support:
  - cli
  - kilo
requires_apply: false
writes:
  - ".spec/reports/**"
---

# /smartspec_verify_tasks_progress_strict

## Purpose
Verify ความคืบหน้า/ความสมบูรณ์ของแต่ละ task แบบ **strict** โดยอาศัย **evidence hooks** (ไม่เชื่อ checkbox) เพื่อกันปัญหา “implement แล้วแต่ verify ไม่พบ code” (false-negative) และกัน “ติ๊กแล้วแต่ยังไม่ทำจริง” (false-positive).

หลักการ:
- ✅ **Evidence-first**: status ของ task ต้องมาจาก evidence เท่านั้น
- ❌ **No checkbox trust**: `- [x]` ไม่ถือว่าเสร็จเอง

---

## Governance contract (MUST)

### Read-only (MUST)
- Workflow นี้ต้องเป็น **read-only** ต่อ codebase
- MUST NOT modify any file under `specs/**` หรือที่ใด ๆ นอกจากรายงานใน `.spec/reports/**`
- MUST NOT create scripts ใน repo root หรือโฟลเดอร์อื่น

### No network / no shell (MUST)
- MUST NOT require network
- MUST NOT execute any command จาก evidence (`command=` เป็น metadata เท่านั้น)

### Report-only outputs (MUST)
- MUST write outputs only under:
  - `.spec/reports/verify-tasks-progress/<run-id>/`

---

## Inputs

### Required
- Positional: path ไปยัง `tasks.md`
  - แนะนำให้ใช้ `specs/<category>/<spec-id>/tasks.md`

### Optional
- `--spec <spec.md>`: (optional) ใช้ช่วย cross-check references หรือ section mappings (ถ้ามี implement ในตัว workflow)

---

## Evidence Hook Requirements (MUST)
Strict verifier นี้รองรับเฉพาะ evidence hooks แบบ canonical:

### Canonical format
- `evidence: <code|test|docs|ui> key=value key="value with spaces" ...`

### Supported types + keys
- `code`: `path` (required), optional `contains`, `regex`, `symbol`
- `docs`: `path` (required), optional `heading`, `contains`, `regex`
- `ui`: `path` (required), optional `selector`, `contains`, `regex`
- `test`: `path` (required), optional `command`, `contains`, `regex`

### Hard rules (causes invalid)
- `path=` MUST be repo-relative (ห้าม absolute/traversal)
- `path=` MUST NOT be a command token (เช่น `npm`, `npx`, `docker`)
- ห้าม glob ใน `path=` เช่น `src/**/*.ts`
- ถ้า value มีช่องว่าง MUST quote เช่น `command="npx prisma validate"`

### Strong recommendation (reduces false-negative)
- `code/docs/ui` ควรมี matcher อย่างน้อย 1 ตัว (`contains/regex/symbol/heading/selector`) ไม่ใช่แค่ `path` อย่างเดียว
- `docs` ควรใช้ `heading=` เมื่ออ้าง section สำคัญ
- `test` ถ้ามี `command=` ควรมี `path=` เป็น anchor file เสมอ

---

## Verification logic (expected)

> หมายเหตุ: verifier นี้ “ตรวจ evidence” ไม่ใช่การ build/run test จริง

### For `code/docs/ui`
- PASS เมื่อ:
  - file/anchor `path` exists
  - และถ้ามี matcher:
    - `contains`: พบ substring
    - `regex`: match
    - `symbol`: พบชื่อ symbol (best-effort; อาจเป็น contains/regex ภายใน)
    - `heading`: พบ heading (เฉพาะ docs)
    - `selector`: พบ selector (เฉพาะ ui; อาจเป็น contains/regex ภายใน)

### For `test`
- PASS เมื่อ:
  - anchor `path` exists
  - และถ้ามี `contains/regex` ตรวจในไฟล์ anchor
  - `command=` ไม่ถูกรัน (record-only)

---

## Outputs
Workflow MUST write:
- `.spec/reports/verify-tasks-progress/<run-id>/report.md`
- `.spec/reports/verify-tasks-progress/<run-id>/report.json`

Report SHOULD include:
- Summary: total tasks, verified complete, incomplete, invalid evidence
- Per-task breakdown:
  - Task ID, title
  - Evidence hooks: pass/fail พร้อมเหตุผล
  - “missing files” list (ถ้ามี)

---

## Invocation

### Verify (recommended)

**CLI:**
```bash
/smartspec_verify_tasks_progress_strict specs/<category>/<spec-id>/tasks.md
```

**Kilo Code:**
```bash
/smartspec_verify_tasks_progress_strict.md specs/<category>/<spec-id>/tasks.md --platform kilo
```

### Verify + cross-check spec references (optional)

**CLI:**
```bash
/smartspec_verify_tasks_progress_strict specs/<category>/<spec-id>/tasks.md --spec specs/<category>/<spec-id>/spec.md
```

**Kilo Code:**
```bash
/smartspec_verify_tasks_progress_strict.md specs/<category>/<spec-id>/tasks.md --spec specs/<category>/<spec-id>/spec.md --platform kilo
```

---

## Common false-negative causes (and fixes)

1) `command=` ไม่ quote
- Fix: `command="..."`

2) ใช้ `test path=npm run build` (เอาคำสั่งไปใส่ใน path)
- Fix: `evidence: test path=package.json command="npm run build"`

3) ใช้ `code` แต่ใส่ `heading=` และชี้ไปไฟล์เอกสาร
- Fix: เปลี่ยนเป็น `docs`

4) มีแต่ `path=` ไม่มี matcher ทำให้ verify เปราะบาง
- Fix: เพิ่ม `contains/regex/heading/symbol/selector`

---

## Related workflows
- `/smartspec_generate_tasks` (ต้องผลิต evidence hooks แบบ canonical)
- `/smartspec_migrate_evidence_hooks` (ซ่อม legacy hooks ให้ canonical)

