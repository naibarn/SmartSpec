# Workflow: /smartspec_report_implement_prompter.md

> **Status:** Revised (Governance-aligned)
> **Purpose:** Generate implementation-ready prompts from **strict verification reports** without polluting engine or project source folders.

---

## 1. Design Intent (What changed & why)
This revision enforces **clear separation of concerns**:

- **Engine code** stays in `scripts/` (versioned, not temporary)
- **Kilo Code registration artifacts** live in `.kilocode/workflows/` (cache-like, deletable)
- **Runtime outputs** are written **only** to `.smartspec/prompts/<spec-id>/`

This prevents:
- Accidental writes to `scripts/`
- Perceived "garbage" accumulation
- Mixing workflow engines with user artifacts

---

## 2. Read / Write Boundaries (Hard Rules)

### Read-only inputs
- `specs/**/spec.md`
- `specs/**/tasks.md`
- strict verification report (`*.json`)

### Allowed write locations (ONLY)
```
.smartspec/prompts/<spec-id>/
```

### Forbidden write locations
- `scripts/`
- `specs/`
- `.spec/`
- `.kilocode/workflows/`

> Any runtime write outside `.smartspec/prompts/` is a **bug**.

---

## 3. Output Directory Resolution (Mandatory)

### Resolution order
1. Explicit `--output`
2. Default: `.smartspec/prompts/<spec-id>`

### Guardrail
If resolved output path:
- contains `/scripts`
- equals project root
- is outside `.smartspec/prompts`

→ **Abort with error**

---

## 4. Usage Examples (CLI / Non‑Kilo Code)

> ใช้กรณีรันจาก terminal ปกติ, CI, หรือ environment ที่ **ไม่ใช่ Kilo Code**

### Example 1 — ใช้งานแบบมาตรฐาน (แนะนำ)
```bash
/smartspec_report_implement_prompter \
  --spec specs/feature/spec-002-user-management/spec.md \
  --tasks specs/feature/spec-002-user-management/tasks.md \
  --report .spec/reports/verify-tasks-progress/spec-002-user-management-strict.json \
  --output .smartspec/prompts/spec-002-user-management
```

ผลลัพธ์:
- ระบบจะสร้างไฟล์ prompt เฉพาะใน `.smartspec/prompts/spec-002-user-management/`
- **จะไม่สร้างหรือแก้ไขไฟล์ใด ๆ** ใน `scripts/`, `specs/`, `.spec/`

### Example 2 — ไม่ระบุ `--output`
```bash
/smartspec_report_implement_prompter \
  --spec specs/feature/spec-002-user-management/spec.md \
  --tasks specs/feature/spec-002-user-management/tasks.md \
  --report .spec/reports/verify-tasks-progress/spec-002-user-management-strict.json
```

ผลลัพธ์:
- ระบบจะใช้ค่า default: `.smartspec/prompts/spec-002-user-management`

---

## 5. Usage Examples (Kilo Code Mode)

> ใช้เมื่อรันผ่าน **Kilo Code** เท่านั้น
> 
> **กฎบังคับ:**
> - ต้องใช้ชื่อ workflow ลงท้ายด้วย `.md`
> - ต้องใส่ `--kilocode`

### Example 3 — Kilo Code (มาตรฐาน)
```bash
/smartspec_report_implement_prompter.md \
  --spec specs/feature/spec-002-user-management/spec.md \
  --tasks specs/feature/spec-002-user-management/tasks.md \
  --report .spec/reports/verify-tasks-progress/spec-002-user-management-strict.json \
  --output .smartspec/prompts/spec-002-user-management \
  --kilocode
```

สิ่งที่ Kilo Code จะทำเพิ่มเติม:
- ตรวจสอบ permission (`chmod +x`) ของ workflow wrapper
- สร้าง/อัปเดต symlink ใน `.kilocode/workflows/`

> ไฟล์ใน `.kilocode/workflows/` ถือเป็น **registration cache** สามารถลบได้ตลอด

---

## 6. Generated Structure

## 5. Kilo Code Usage (Required Pattern)

```bash
/smartspec_report_implement_prompter.md \
  --spec specs/feature/<spec-id>/spec.md \
  --tasks specs/feature/<spec-id>/tasks.md \
  --report .spec/reports/verify-tasks-progress/<spec-id>-strict.json \
  --output .smartspec/prompts/<spec-id> \
  --kilocode
```

> `.kilocode/workflows/` artifacts (chmod / symlink) are **registration cache** and may be safely deleted.

---

## 6. Generated Structure

```
.smartspec/prompts/<spec-id>/
  README.md
  api-cluster.md
  tests-cluster.md
  docs-cluster.md
  deploy-cluster.md
```

No other files are generated.

---

## 7. Task Classification Logic (Unchanged)
- **unsynced** → checkbox sync only
- **simple** → inline implementation hints
- **complex** → clustered by domain (API / Tests / Docs / Deploy)

---

## 8. Idempotency & Cleanup

- Re-running the workflow **overwrites prompts** for the same `<spec-id>`
- Safe to delete:
  - `.kilocode/workflows/smartspec_*`
  - `.smartspec/prompts/<spec-id>`

- Never delete:
  - `scripts/`

---

## 9. Non-Goals (Explicit)

This workflow does **NOT**:
- Modify `spec.md` or `tasks.md`
- Sync checkboxes
- Perform verification

Use:
- `/smartspec_verify_tasks_progress_strict`
- `/smartspec_sync_tasks_checkboxes`

---

## 10. Canonical Execution Flow

```
STRICT VERIFY
  ↓
IMPLEMENT PROMPTER (this workflow)
  ↓
CODE CHANGES
  ↓
STRICT VERIFY
  ↓
SYNC CHECKBOXES
```

---

## 11. Compliance Checklist
- [x] CLI-first
- [x] Kilo Code compatible
- [x] No engine pollution
- [x] Output isolated & deletable
- [x] Governance-aligned

---

**End of workflow specification**

