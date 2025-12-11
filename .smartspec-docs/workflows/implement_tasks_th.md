# คู่มือ SmartSpec — /smartspec_implement_tasks (ภาษาไทย, ฉบับบังคับใช้ v5.7.2)

คู่มือนี้เป็นฉบับที่ปรับปรุงตามสเปก **บังคับใช้จริง (enforced version)** ของ workflow `/smartspec_implement_tasks` ซึ่งรวมถึงกฎใหม่ที่สำคัญ:

- `--require-orchestrator` ต้องถูกบังคับใช้อย่างจริงจัง
- เมื่อใช้คู่กับ `--kilocode` → ระบบต้องตรวจว่า Orchestrator Mode **เปิดอยู่จริง**
- หากสัญญาณ Orchestrator **ขาด / false / ไม่ทราบสถานะ** → ให้ถือว่า “ไม่เปิด”
- ในโหมด `strict` → ต้อง **หยุดทำงานทันที (fail fast)** พร้อม error
- ในโหมด `dev` → ต้องแสดงคำเตือนหนัก และอาจหยุดหรือทำงานแบบลดคุณภาพ
- ห้าม fallback แบบเงียบโดยเด็ดขาด

คู่มือนี้สอดคล้อง 100% กับ workflow ที่ถูกอัปเดตแล้วในระบบของคุณ

---

# 1. ภาพรวม

`/smartspec_implement_tasks` ใช้สำหรับ **ลงมือแก้ไขและสร้างโค้ดจริง** ตามรายการงานใน `tasks.md` โดยต้องเคารพกฎสำคัญของ SmartSpec ได้แก่:

- ระเบียบ SPEC_INDEX
- ขอบเขตเจ้าของงานข้ามรีโป
- กฎ registry & multi-repo
- กฎ UI (design tokens, App components, ui.json)
- กฎเว็บสแตก (React / Next.js / RSC / Node)
- ความปลอดภัยด้านข้อมูล & AI
- การทำงานร่วมกับ KiloCode และ Orchestrator Mode

นี่คือเวอร์ชันที่นำกฎทั้งหมดไปบังคับใช้จริง ไม่ใช่แค่คำแนะนำ

---

# 2. อัปเดตสำคัญใน v5.7.2 (ฉบับบังคับใช้)

## 2.1 การบังคับใช้ `--require-orchestrator`
เมื่อรันร่วมกับ `--kilocode` กฎต่อไปนี้ต้องถูกบังคับ:

> **หาก Orchestrator Mode ไม่ได้รายงานว่า active อย่างชัดเจน → ต้องถือว่า Orchestrator = ไม่เปิด และต้อง fail ใน strict mode ทันที**

สิ่งที่ถือว่า “active อย่างชัดเจน”
```
env.orchestrator_active = true
```
หรือ flag ที่มีความหมายเทียบเท่าจาก Kilo

### หากสถานะ Orchestrator เป็น:
- missing (ไม่มีสัญญาณ)
- false
- unknown (ไม่รู้สถานะ)

→ ถือว่า **ปิดอยู่**

### ผลลัพธ์เมื่อ Orchestrator = ปิด

**โหมด strict:**
- หยุด run ทันที (fail fast)
- แสดง error ชัดเจน เช่น:
  > "ต้องการ Orchestrator Mode (`--require-orchestrator`) แต่ไม่พบว่าถูกเปิดใช้งาน กรุณาเปิดใน Kilo UI"

**โหมด dev:**
- เตือนหนัก
- เลือกหยุดหรือรันต่อแบบลดคุณภาพได้ แต่ต้องแจ้งชัดเจนว่า “ไม่ได้อยู่ในโหมด Orchestrator”

---

## 2.2 ไม่รองรับ auto-switch
Kilo Code **จะไม่สลับเข้าสู่ Orchestrator Mode ให้อัตโนมัติ** ไม่ว่าผู้ใช้จะส่ง flag อะไรก็ตาม

ผู้ใช้ต้องเปิดโหมด Orchestrator ด้วยปุ่มใน UI ก่อนเสมอ

Workflow ไม่มีสิทธิ์สั่งให้ IDE เปลี่ยนโหมด

---

## 2.3 การปรับขั้นตอน Step 1.a
ตอนนี้ workflow จะตรวจสอบสถานะ Orchestrator **ก่อนเริ่มทำงานใด ๆ**

---

# 3. อินพุต / เอาต์พุต

## อินพุต
- `tasks.md` (จำเป็น)
- `spec.md` / `plan.md` / `ui.json` (เสริม)
- SPEC_INDEX, รายการ registry, multi-repo config

## เอาต์พุต
- โค้ดที่ถูกปรับปรุงใน repo ปัจจุบัน
- การอัปเดต checkbox / หมายเหตุใน `tasks.md`
- รายงานการ implement (หากเปิดใช้)

---

# 4. รายละเอียด flag (อัปเดต)

### Flags สำหรับ Orchestrator
```
--kilocode
--require-orchestrator
```

### ความปลอดภัย
```
--safety-mode=strict | dev
--strict
```

### ตรวจสอบผลก่อนแก้จริง
```
--validate-only
--dry-run
```

### เลือก task
```
--task
--tasks
--range
--from
--skip-completed
--resume
```

### multi-repo
```
--workspace-roots
--repos-config
--registry-dir
--registry-roots
```

---

# 5. พฤติกรรมของ Orchestrator (ฉบับบังคับจริง)

## 5.1 ใช้ `--kilocode` อย่างเดียว
- Workflow จะพยายามใช้ Orchestrator หากเปิดอยู่
- ถ้า Orchestrator ไม่เปิด → ใช้ linear mode พร้อมคำเตือน

## 5.2 ใช้ `--kilocode --require-orchestrator`
นี่คือกฎใหม่แบบบังคับใช้:

หากสัญญาณ Orchestrator Active เป็น:
- ไม่มี
- false
- ไม่รู้สถานะ

→ ต้องถือว่า Orchestrator = ปิด

### strict mode:
- หยุด run ทันที
- แจ้ง error ชัดเจน เช่น:
  > "ต้องการ Orchestrator Mode แต่ไม่เปิดอยู่ กรุณาเปิดใน Kilo UI แล้วลองใหม่"

### dev mode:
- เตือนหนักมาก
- อาจจะรันต่อแบบ non-Orchestrator แต่ต้องแจ้งให้ทราบอย่างชัดเจน

ห้าม fallback แบบเงียบโดยเด็ดขาด

---

# 6. ตัวอย่างคำสั่ง

### คำสั่งที่แนะนำบน Kilo
```
/smartspec_implement_tasks specs/.../tasks.md \
  --kilocode --require-orchestrator --safety-mode=strict
```

### ตรวจสอบก่อนแก้จริง
```
/smartspec_implement_tasks specs/.../tasks.md --validate-only
```

### เลือก task เดียว
```
/smartspec_implement_tasks specs/.../tasks.md --task=3 \
  --kilocode --require-orchestrator
```

---

# 7. การแก้ปัญหา

### ❗ Orchestrator ไม่เปิด
จะเกิด error:
> "ต้องการ Orchestrator Mode (`--require-orchestrator`) แต่ไม่พบว่าถูกเปิดใช้งาน"

วิธีแก้:
1. เปิด Kilo UI
2. กดเลือก Orchestrator Mode
3. รันคำสั่งอีกครั้ง

### ❗ Kilo แจ้ง Edit Unsuccessful
- Workflow จะลดขนาด scope
- แนะนำให้ split task หรือ retry ทีละส่วน

---

# 8. แนวทางที่ดีที่สุด

### ⭐ ผู้ใช้ Kilo ควรใช้เสมอ
```
--kilocode --require-orchestrator --safety-mode=strict
```

### ⭐ ต้องเปิด Orchestrator Mode ก่อนเสมอ
Kilo จะไม่สลับให้เอง

### ⭐ แนะนำให้รัน validate-only ก่อนบน repo ใหญ่

### ⭐ แบ่ง task ให้ชัดเจนและไม่กว้างเกินไป

---

# END OF THAI MANUAL

