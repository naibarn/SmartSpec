# คู่มือเวิร์กโฟลว์: /smartspec_report_implement_prompter.md

> **สถานะ:** ปรับปรุงแล้ว (สอดคล้อง Governance)
> **วัตถุประสงค์:** สร้างชุดพรอมต์สำหรับการ implement จาก **strict verification report** โดยเขียนไฟล์ผลลัพธ์เฉพาะใน `.smartspec/prompts/<spec-id>/` และไม่ปะปนกับโค้ดหลักของโปรเจกต์

---

## 1. เจตนาการออกแบบ
เอกสารนี้ถูกปรับให้ “ชัดเจนเรื่องขอบเขต” เพื่อไม่ให้เกิดความเข้าใจผิดว่าการรัน workflow สร้างขยะในระบบ:

- **โค้ดของ workflow (engine)** อยู่ใน `scripts/` เท่านั้น (เป็นโค้ดหลัก, มี version control)
- **ไฟล์ลงทะเบียนของ Kilo Code** อยู่ใน `.kilocode/workflows/` (เป็น cache/registration ลบได้)
- **ผลลัพธ์ที่ workflow สร้าง** จะเขียน **เฉพาะ** ใน `.smartspec/prompts/<spec-id>/`

---

## 2. ขอบเขตการอ่านและการเขียนไฟล์

### 2.1 ไฟล์อินพุต (อ่านอย่างเดียว)
- `specs/**/spec.md`
- `specs/**/tasks.md`
- strict verification report (`*.json`) จาก `/smartspec_verify_tasks_progress_strict`

### 2.2 โฟลเดอร์ที่อนุญาตให้เขียน (เขียนได้ “ที่เดียว”)
```
.smartspec/prompts/<spec-id>/
```

### 2.3 โฟลเดอร์ต้องห้าม (ห้ามเขียนโดยเด็ดขาด)
- `scripts/`
- `specs/`
- `.spec/`
- `.kilocode/workflows/`

> หากพบว่ามีการเขียนไฟล์นอก `.smartspec/prompts/` ในช่วง runtime ให้ถือว่าเป็น **บั๊ก**

---

## 3. การกำหนดโฟลเดอร์ Output

### 3.1 ลำดับการเลือกโฟลเดอร์
1. ค่า `--output` ที่ผู้ใช้ระบุ
2. ค่าเริ่มต้น: `.smartspec/prompts/<spec-id>`

### 3.2 Guardrail (บังคับ)
หาก output path ที่ resolve แล้ว:
- มีคำว่า `/scripts`
- ชี้ไปที่ project root
- อยู่นอก `.smartspec/prompts`

→ ต้อง **ยกเลิกการทำงานพร้อม error**

---

## 4. ตัวอย่างการใช้งาน (CLI / ไม่ใช้ Kilo Code)
> ใช้กรณีรันจาก terminal ปกติ, CI, หรือ environment ที่ **ไม่ใช่ Kilo Code**

### 4.1 ตัวอย่าง: ใช้งานแบบมาตรฐาน (แนะนำ)
```bash
/smartspec_report_implement_prompter \
  --spec specs/feature/spec-002-user-management/spec.md \
  --tasks specs/feature/spec-002-user-management/tasks.md \
  --report .spec/reports/verify-tasks-progress/spec-002-user-management-strict.json \
  --output .smartspec/prompts/spec-002-user-management
```

ผลลัพธ์:
- สร้างไฟล์ prompt เฉพาะใน `.smartspec/prompts/spec-002-user-management/`
- ไม่สร้าง/ไม่แก้ไขไฟล์ใน `scripts/`, `specs/`, `.spec/`, `.kilocode/`

### 4.2 ตัวอย่าง: ไม่ระบุ `--output`
```bash
/smartspec_report_implement_prompter \
  --spec specs/feature/spec-002-user-management/spec.md \
  --tasks specs/feature/spec-002-user-management/tasks.md \
  --report .spec/reports/verify-tasks-progress/spec-002-user-management-strict.json
```

ผลลัพธ์:
- ใช้ค่าเริ่มต้น: `.smartspec/prompts/spec-002-user-management`

---

## 5. ตัวอย่างการใช้งาน (Kilo Code)
> ใช้เมื่อรันผ่าน **Kilo Code** เท่านั้น

**กฎบังคับ:**
- ต้องใช้ชื่อ workflow ลงท้ายด้วย `.md`
- ต้องใส่ `--kilocode`

### 5.1 ตัวอย่าง: Kilo Code (มาตรฐาน)
```bash
/smartspec_report_implement_prompter.md \
  --spec specs/feature/spec-002-user-management/spec.md \
  --tasks specs/feature/spec-002-user-management/tasks.md \
  --report .spec/reports/verify-tasks-progress/spec-002-user-management-strict.json \
  --output .smartspec/prompts/spec-002-user-management \
  --kilocode
```

หมายเหตุ:
- Kilo Code อาจแสดงขั้นตอน `chmod +x` และ `ln -sf` ภายใต้ `.kilocode/workflows/`
- นี่คือ **registration cache** ไม่ใช่ output ของ workflow และลบได้ตลอด

---

## 6. โครงสร้างไฟล์ผลลัพธ์ที่สร้าง
```
.smartspec/prompts/<spec-id>/
  README.md
  api-cluster.md
  tests-cluster.md
  docs-cluster.md
  deploy-cluster.md
```

> Workflow นี้จะไม่สร้างไฟล์ผลลัพธ์ในตำแหน่งอื่น

---

## 7. การจัดประเภทงาน
- **unsynced** → งานเสร็จแล้ว แต่ checkbox ยังไม่ตรง → ให้ใช้ `/smartspec_sync_tasks_checkboxes`
- **simple** → งานง่าย → ให้ implement โดยตรง (หรือใช้ workflow ที่ทีมกำหนด)
- **complex** → งานซับซ้อน/critical → จัดกลุ่มเป็นโดเมน (API / Tests / Docs / Deploy) แล้วสร้าง prompt ให้

---

## 8. รันซ้ำและการล้างของชั่วคราว
- รันซ้ำจะ **เขียนทับ** ไฟล์ prompt สำหรับ `<spec-id>` เดิม
- ลบได้อย่างปลอดภัย:
  - `.kilocode/workflows/smartspec_*`
  - `.smartspec/prompts/<spec-id>`
- ห้ามลบ:
  - `scripts/` (เป็นโค้ดหลักของ workflow engine)

---

## 9. สิ่งที่ workflow นี้ “ไม่ทำ”
Workflow นี้ **ไม่**:
- แก้ไข `spec.md` หรือ `tasks.md`
- ทำ verification แทน strict verifier
- sync checkbox ให้เอง

ให้ใช้ workflow ต่อไปนี้:
- `/smartspec_verify_tasks_progress_strict`
- `/smartspec_sync_tasks_checkboxes`

---

## 10. ลำดับการใช้งานที่แนะนำ (Canonical Flow)
```
STRICT VERIFY
  ↓
REPORT IMPLEMENT PROMPTER (workflow นี้)
  ↓
CODE CHANGES
  ↓
STRICT VERIFY
  ↓
SYNC CHECKBOXES
```

---

## 11. เช็คลิสต์ความสอดคล้อง (Compliance Checklist)
- [x] แยก engine / cache / output ชัดเจน
- [x] เขียนไฟล์เฉพาะ `.smartspec/prompts/`
- [x] รองรับ CLI และ Kilo Code
- [x] ลดความสับสนเรื่องไฟล์ตกค้าง

---

**จบคู่มือเวิร์กโฟลว์**