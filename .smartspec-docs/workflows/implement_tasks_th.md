# คู่มือ SmartSpec — /smartspec_implement_tasks (จากไฟล์ที่อัปโหลด, ฉบับพร้อมแก้ไข)

ด้านล่างนี้คือเนื้อหาจากไฟล์ที่คุณอัปโหลด (`implement_tasks_th.md`) โดยถูกย้ายเข้ามาใน Canvas เพื่อให้สามารถแก้ไขและปรับปรุงได้ตรงไฟล์นี้เท่านั้น (ไม่ยุ่งกับไฟล์อื่น):

---
# คู่มือ SmartSpec — /smartspec_implement_tasks (ฉบับเต็ม ภาษาไทย, v5.7.2 บังคับใช้)

> **นี่คือคู่มือฉบับสมบูรณ์** ซึ่งได้รวมเนื้อหาดั้งเดิมทั้งหมดของคู่มือ implement tasks (เวอร์ชันเก่า) เข้ากับกฎใหม่ที่ถูกบังคับใช้ใน v5.7.2 โดยไม่ลบเนื้อหาเก่า และจัดโครงสร้างให้เป็นระเบียบ อ่านง่าย ใช้งานจริงได้ทันที

รวม:
- ตัวอย่างการใช้งานทุกแบบ (tasks, ranges, phases)
- การเลือก implement แบบละเอียด
- Best practices เดิมและใหม่
- การทำงานร่วมกับ Kilo & Orchestrator Mode
- Error cases & วิธีแก้

---
# 1. ภาพรวม
`/smartspec_implement_tasks` คือ workflow สำหรับ **ลงมือแก้ไขโค้ดจริง** ตามรายการใน `tasks.md` ภายใต้กฎของ SmartSpec เช่น:
- ขอบเขต SPEC_INDEX
- multi-repo governance
- registry rules
- UI governance (design tokens, App components)
- web-stack guardrails
- กฎความปลอดภัยด้านข้อมูล
- การทำงานร่วมกับ Kilo / Roo / Claude / Antigravity / Gemini

คู่มือนี้ครอบคลุมวิธีใช้งานทุกรูปแบบ ตั้งแต่ task เดี่ยว จนถึง phase-based implementation

---
# 2. แนวคิดสำคัญ
- `tasks.md` คือรายการงานที่ต้องทำ
- checkbox ✓ = ทำเสร็จแล้ว
- implement workflow = ลงมือแก้ไฟล์จริง
- flags ใช้เลือก task, phase, range
- safety mode ควบคุมความเข้มงวดของกฎ
- Kilo Orchestrator ช่วยปรับปรุงคุณภาพการแก้ไฟล์

---
# 3. พฤติกรรมใหม่ใน v5.7.2 (บังคับใช้จริง)
## 3.1 การบังคับใช้ `--require-orchestrator`
เมื่อรันร่วมกับ `--kilocode` กฎใหม่คือ:

> **ต้องมีสัญญาณอย่างชัดเจนว่า Orchestrator Mode เปิดอยู่ (`env.orchestrator_active=true`)**

ถ้าไม่พบสัญญาณ หรือเป็น false / unknown → ถือว่า “ปิด”

ผลลัพธ์:
- **strict → หยุดทันที (fail-fast)**
- **dev → เตือนหนัก อาจหยุดหรือทำงานแบบลดคุณภาพ**

## 3.2 ไม่ auto-switch
ไม่ว่าผู้ใช้ใส่ flag อะไรก็ตาม Kilo จะ **ไม่สลับโหมดให้เอง**
ต้องกดเปิดโหมด Orchestrator จาก UI เท่านั้น

## 3.3 เพิ่มกฎใน Step 1.a
ก่อนเริ่มทำงาน จะตรวจสถานะ Orchestrator → ถ้าต้องการและไม่เปิด → หยุดทันที

---
# 4. อินพุต/เอาต์พุต
## อินพุต
- `tasks.md` (จำเป็น)
- `spec.md`, `plan.md`, `ui.json` (เสริม)

## เอาต์พุต
- โค้ดใหม่/แก้ไขแล้วใน repo ปัจจุบัน
- อัปเดต checkbox ใน `tasks.md`
- รายงานสรุป

---
# 5. รายละเอียด flags
## เลือก task
```
--task=T003
--tasks=T001,T003,T005
--range=T001-T004
--from=T006
--skip-completed
--resume
```

## ความปลอดภัย
```
--safety-mode=strict
--safety-mode=dev
--strict
```

## ตรวจสอบก่อนแก้จริง
```
--validate-only
--dry-run
```

## สำหรับ Kilo
```
--kilocode
--require-orchestrator
```

## multi-repo
```
--workspace-roots
--repos-config
--registry-dir
--registry-roots
```

---
# 6. ตัวอย่างเลือก Task แบบละเอียด
## 6.1 Task เดี่ยว
```
--task=T003
```

## 6.2 หลาย task
```
--tasks=T002,T004,T007
```

## 6.3 range
### 1) ปิดทั้งสองด้าน
```
--range=T003-T007
```

### 2) เปิดด้านท้าย
```
--from=T005
```

### 3) ผสมหลาย pattern
```
--tasks=1,3 --range=5-9
```

## 6.4 skip
```
--skip-completed
```

## 6.5 resume
```
--resume
```

---
# 7. Implement ตาม Phase
ใน `tasks.md` อาจมี phase กำกับ เช่น:
```
## Phase: setup
## Phase: api
## Phase: ui
```
เลือกเฉพาะ phase:
```
--phase=ui
--phases=api,ui
```
หรือผสมกับ range:
```
--phase=backend --from=4
```

---
# 8. การทำงานร่วมกับ Kilo (เต็มรูปแบบ)
## 8.1 `--kilocode`
- เปิดพฤติกรรมแก้ไฟล์แบบรู้บริบทของ Kilo
- ถ้า Orchestrator ไม่เปิด → ทำงานแบบ linear พร้อมแจ้งเตือน

## 8.2 `--kilocode --require-orchestrator`
กฎบังคับ:
- ต้องมี `env.orchestrator_active=true`
- ถ้าไม่พบ → ถือว่า Orchestrator ปิด
- strict = หยุดทันที
- dev = เตือนหนักมาก

## 8.3 ต้องเปิด Orchestrator Mode เอง
Kilo จะ **ไม่สลับโหมดให้เอง**

---
# 9. คำสั่งที่แนะนำ
## แนะนำบน Kilo
```
/smartspec_implement_tasks tasks.md \
  --kilocode --require-orchestrator --safety-mode=strict
```

## ตรวจสอบก่อนแก้จริง
```
--validate-only
```

---
# 10. ลำดับการทำงาน
1. โหลด tasks.md
2. ประมวลผล flags
3. ตรวจ SPEC_INDEX และ registry
4. (Kilo) ตรวจ Orchestrator
5. ลงมือแก้ไฟล์
6. อัปเดต tasks.md
7. สรุปผล

---
# 11. กรณี Error
## 11.1 Orchestrator ไม่เปิด (strict)
```
ERROR: ต้องการ Orchestrator Mode แต่ไม่เปิด
```

## 11.2 แก้ไฟล์ไม่สำเร็จ
- ลด scope อัตโนมัติ
- แนะนำให้ split task

## 11.3 เลือก task ผิดรูปแบบ
แจ้ง error สำหรับ:
- range ว่าง
- ตัวเลขไม่ถูกต้อง
- ช่วงกลับด้าน

## 11.4 SPEC_INDEX ละเมิดขอบเขต
หยุดทำงานทันที

---
# 12. ตัวอย่างขั้นสูง
## 12.1 ทำเฉพาะ API
```
--phase=api --skip-completed
```

## 12.2 ทำเฉพาะ task ใหม่วันนี้
```
--from=last
```
(หากมี metadata รองรับ)

## 12.3 ผสมหลายรูปแบบ
```
--tasks=1,4,9 --range=10-15 --skip-completed
```

## 12.4 Resume บน Kilo
```
--resume --kilocode --require-orchestrator
```
ถ้าไม่เปิด Orchestrator → หยุด

---
# 13. แนวทางที่ดีที่สุด
- เปิด Orchestrator เมื่อใช้ Kilo
- ใช้ validate-only กับงานใหญ่
- แบ่ง task ให้เหมาะสม
- ใช้ phase เพื่อจัดลำดับ
- หลีกเลี่ยง task ยาวหรือกำกวม

---
# END OF FULL THAI MANUAL