---
description: SmartSpec - Spec Lifecycle Manager (Centralization v1)
---

# SmartSpec Spec Lifecycle Manager

Workflow นี้จัดการวงจรชีวิตของ SPEC แบบ “ระดับระบบใหญ่”  
เพื่อแก้ช่องโหว่ที่ SPEC จำนวนมากถูกตั้งเป็น active ตลอด  
หรือ category=deprecated แต่ยังถูกใช้งานโดยไม่รู้ตัว

---

## User Input

```text
$ARGUMENTS
```

ตัวอย่าง:
- `/smartspec_spec_lifecycle_manager --spec-id=spec-120 --set-status=deprecated`
- `/smartspec_spec_lifecycle_manager --spec-id=spec-045 --set-status=archived`
- `/smartspec_spec_lifecycle_manager --category=deprecated --report-only`
- `/smartspec_spec_lifecycle_manager --auto-propagate`

---

## 0) Centralization Resolver (MANDATORY)

### 0.1 Resolve SPEC_INDEX

ลำดับ:
1) `--specindex`
2) `.spec/SPEC_INDEX.json`
3) `SPEC_INDEX.json`
4) `.smartspec/SPEC_INDEX.json`
5) `specs/SPEC_INDEX.json`

### 0.2 Resolve Config / Directories

Defaults:
- `SPEC_HUB_DIR = ".spec"`
- `REGISTRY_DIR = ".spec/registry"`
- `OUTPUT_DIR = ".smartspec"`

---

## 1) Load Index & Build Dependency Map

1) Load SPEC_INDEX.
2) Build:
   - `deps_of[spec]`
   - `dependents_of[spec]`

---

## 2) Status Model (Schema-Preserving)

Workflow นี้พยายาม **ไม่บังคับเปลี่ยน schema เดิม**  
แต่จะใช้แนวทาง additive:

- ถ้า index มี field `status` อยู่แล้ว → ใช้ field นี้
- ถ้ายังไม่มี → ใช้การอัปเดต `category` แบบมีมาตรฐาน  
  และพิมพ์คำแนะนำให้ทีมเพิ่ม status ในอนาคต

ค่าที่แนะนำ:
- `draft`
- `active`
- `deprecated`
- `archived`

---

## 3) Operations

### 3.1 Set Status for a Spec

เมื่อใช้:
- `--spec-id=<id> --set-status=<status>`

ต้อง:
1) ตรวจว่า spec มีอยู่จริง
2) เปลี่ยน status/category ตาม policy
3) สร้างบันทึกใน report:
   - เหตุผล
   - ผลกระทบต่อ dependents

### 3.2 Batch Mode

รองรับ:
- `--category=<value>`
- `--tag=<value>`
- `--repo=<public|private>`

---

## 4) Propagation Rules (แก้ช่องโหว่หลัก)

ถ้า `--auto-propagate`:

### 4.1 Deprecation Impact

เมื่อ spec ถูก deprecated:
- ถ้ามี dependents ที่ยัง active:
  - สร้าง “impact list”
  - แนะนำให้:
    - สร้าง replacement spec
    - หรือ migrate dependencies ออกจาก spec เดิม
- ห้าม auto-change dependents status โดยไม่แจ้ง

### 4.2 Public ↔ Private Policy

- ถ้า private core ถูก deprecated:
  - ต้อง flag public specs ที่ depend ทั้งหมดเป็น “at-risk”
- ถ้า public spec ถูก deprecated:
  - private specs ไม่ควร depend ย้อนกลับ (warn)

### 4.3 UI Policy Hook

ถ้า category=ui:
- ตรวจว่า `ui.json` อยู่ใน files
- ถ้า deprecated:
  - แนะนำ archive Penpot artifact พร้อม/หลัง archive code components

---

## 5) Write Outputs

โดยดีฟอลต์:
- เขียนเฉพาะ index ที่ canonical:
  - `.spec/SPEC_INDEX.json`

Optional compatibility:
- ถ้า repo ยังต้องใช้ root index:
  - อาจสร้าง mirror `SPEC_INDEX.json` แบบ read-only note  
    เมื่อ user ใส่ `--write-legacy-mirror`

---

## 6) Reports

เขียนไปที่:
- `${OUTPUT_DIR}/reports/lifecycle/`

ต้องมี:
- Summary of changes
- Impact analysis
- Suggested next workflows

Context: $ARGUMENTS
