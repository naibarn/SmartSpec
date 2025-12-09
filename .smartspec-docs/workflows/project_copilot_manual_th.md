---
manual: /smartspec_project_copilot
version: 5.7
compatible_workflow_versions: 5.6.x
language: th
role: User guide for project-level SmartSpec copilot
---

# 1. ภาพรวม

`/smartspec_project_copilot` คือ workflow แบบ **เลขาโปรเจกต์ (project copilot)** ทำหน้าที่เป็นที่ปรึกษาระดับโปรเจกต์ อ่านข้อมูลจาก SmartSpec ทั้งชุดแล้วตอบคำถาม ที่ผู้ใช้ถามเป็นภาษาคน เช่น

- ตอนนี้โปรเจกต์คืบหน้าไปถึงไหนแล้ว?
- ระบบ billing / subscription คืบหน้าไปกี่ % แล้ว และต้องทำอะไรต่อ?
- จาก report CI / Security / Release นี้ ต้องทำอะไรต่อ?
- ควร run workflow ตัวไหนต่อ และใช้คำสั่งอย่างไร?

Copilot จะ:

- อ่าน `SPEC_INDEX`, registry, reports, และคู่มือของ workflow ต่าง ๆ
- วิเคราะห์สถานะเป็นราย service / domain
- สรุปเป็นภาษาคน พร้อมเสนอ **คำสั่ง /smartspec\_**\* ที่ run ได้จริง
- ถ้าอยู่บน Kilo และใช้ `--kilocode` จะคิดแบบ Orchestrator เน้นวางแผน/วิเคราะห์ ไม่เน้นเขียนโค้ดเอง

> สำคัญ: copilot เป็น NO-WRITE — ไม่แก้โค้ด, ไม่แก้ spec/plan/tasks เอง

---

# 2. What’s New ในคู่มือเวอร์ชันนี้ (v5.7)

- เพิ่ม use case แบบ “คุยเหมือน LLM/ChatGPT” อย่างละเอียด
- เพิ่มตัวอย่างระบบ **billing + subscription** แสดงการอ่านจาก `SPEC_INDEX` แล้วแปลเป็นคำสั่ง `/smartspec_generate_tasks` ที่ใช้ได้จริง
- อธิบายการทำงานแบบ **chunked context** (อ่านไฟล์ทีละส่วน ไม่เกิน \~500–800 บรรทัด)
- ชัดเจนขึ้นว่าถ้าใช้ `--kilocode` จะให้ Orchestrator เป็นคนวางแผนและแตกงาน

---

# 3. ใช้เมื่อไหร่ / ไม่ควรใช้เมื่อไหร่

## 3.1 ควรใช้เมื่อ

- อยากรู้สถานะโปรเจกต์แต่ไม่อยากจำ workflow ทุกตัว
- อยากดูความคืบหน้าของ service/domain บางตัว เช่น `billing`, `checkout`, `auth`
- มี report จาก workflow อื่นแล้ว แต่อ่านยาก อยากให้ช่วยอ่าน / สรุป / แนะนำสิ่งที่ต้องทำต่อ
- อยากขอ roadmap ระยะสั้นสำหรับ feature หรือผลิตภัณฑ์จากสถานะจริงปัจจุบัน
- อยากถามว่า “ควรใช้ workflow ตัวไหนต่อ” โดยไม่ต้องจำชื่อทั้งหมดเอง

## 3.2 ไม่ควรใช้เมื่อ

- ต้องการให้ระบบแก้ไฟล์จริง (โค้ด, spec, plan, tasks) → copilot ทำไม่ได้
- อยากใช้แทน workflow เฉพาะด้าน เช่น security audit, CI gate, UI audit
- ใช้เพื่อเลี่ยง approval จาก security / architecture

---

# 4. สิ่งที่ต้องมีในโปรเจกต์ก่อนใช้

อย่างน้อยควรมี:

1. โครงสร้าง SmartSpec พื้นฐาน
   - `.spec/SPEC_INDEX.json`
   - `.spec/registry/**` (รวมถึง `tool-version-registry.json` ถ้ามี)
   - `.spec/reports/**` (ถ้าเคยรัน workflow อื่นแล้ว)
2. ไฟล์ governance กลาง
   - `.smartspec/system_prompt_smartspec.md`
   - `.smartspec/knowledge_base_smartspec.md`
3. เอกสาร workflow
   - `.smartspec-docs/workflows/**` (manual TH/EN, example ของแต่ละ workflow)

ถ้าบางอย่างยังไม่มี copilot ควรแจ้งเป็น governance gap แล้วเสนอว่า ควรสร้าง/ติดตั้งอะไรเพิ่มก่อน

---

# 5. วิธีใช้แบบ “คุยเหมือนแชตกับ LLM”

สำหรับผู้ใช้ส่วนใหญ่ ไม่ต้องจำ flag หรือคำสั่งยาว ๆ เลย ให้คิดแบบนี้:

> เปิด `/smartspec_project_copilot` แล้ว **พิมพ์คำถามเป็นภาษาคน** ที่เหลือให้ copilot ไปอ่านข้อมูลในโปรเจกต์และ workflow docs ให้เอง

ด้านล่างคือ use case สำคัญที่เจอได้บ่อย

## 5.1 ถามความคืบหน้าทั้งโปรเจกต์ + % คร่าว ๆ ต่อ service

**สิ่งที่ผู้ใช้ทำ:**

- เปิด copilot แล้วพิมพ์:

> ตอนนี้โปรเจกต์พัฒนาถึงขั้นตอนไหนแล้ว มี service อะไรเสร็จแล้วบ้าง แต่ละ service เสร็จไปประมาณกี่เปอร์เซ็นต์ ถ้ายังไม่เสร็จ ช่วยบอกทีว่าควรทำอะไรต่อก่อน–หลัง

**สิ่งที่ copilot ควรทำ:**

- ใช้ `SPEC_INDEX` หา spec ทั้งหมดในโปรเจกต์
- อ่าน `spec.md`, `plan.md`, `tasks.md`, report ต่าง ๆ แบบ chunk ไม่เกิน \~500–800 บรรทัดต่อรอบ
- ประเมินความคืบหน้าเป็น phase (spec / plan / tasks / CI / security / UI / release)
- แสดง % คร่าว ๆ ต่อ service พร้อมอธิบายที่มาของตัวเลข
- เสนอสิ่งที่ควรทำต่อ (เช่น สร้าง tasks, รัน CI gate, ทำ security audit, รัน release readiness)

## 5.2 เน้นเฉพาะบาง service (ไม่ต้องรู้ `--project-scope`)

**ผู้ใช้ถาม:**

> ช่วยดูให้หน่อยว่าตอนนี้
>
> - payment-service เสร็จไปประมาณกี่ % แล้ว
> - checkout-service เสร็จไปประมาณกี่ % แล้ว
>
> แต่ละตัวเหลืองานอะไรสำคัญอยู่บ้าง แล้วช่วยจัดลำดับว่างานไหนควรทำต่อก่อน–หลัง

**copilot:**

- เดาว่า scope คือ `payment-service` + `checkout-service`
- ใช้ `SPEC_INDEX` หา spec ที่เกี่ยวข้องกับ 2 บริการนี้
- อ่านไฟล์เฉพาะส่วนที่เกี่ยวข้อง
- สรุปคืบหน้า + แนะนำ next step ราย service

## 5.3 แนบ report แล้วถามว่า “จาก report นี้ต้องทำอะไรต่อ”

**สถานการณ์:** มี report จาก `smartspec_ci_quality_gate` หรือ `smartspec_security_evidence_audit` แล้วอ่านไม่ออก

**ผู้ใช้ทำ:**

1. เปิด report → copy เนื้อหาสำคัญ
2. เปิด copilot แล้วพิมพ์:

> จาก report ด้านล่างนี้
>
> - ช่วยสรุปให้หน่อยว่าอะไรผ่าน / ไม่ผ่าน
> - มี blocker อะไรที่ต้องแก้ก่อนปล่อยจริง
> - เราควรทำอะไรต่อก่อน–หลัง
> - ถ้ามี workflow ที่ควรรันต่อ ช่วยบอกชื่อและเหตุผลด้วย
>
> (วางเนื้อหา report ต่อท้าย)

**copilot:**

- ตรวจว่ารายงานมาจาก workflow ไหน
- อ่านเนื้อหาแบบ chunk
- สรุปเป็นภาษาคน + ชี้ blocker
- แนะนำ workflow ที่ควร run ซ้ำ / run เพิ่ม เช่น CI gate อีกรอบ, security audit, release readiness

## 5.4 ขอ roadmap สั้น ๆ เป็นภาษาคน

**ผู้ใช้ถาม:**

> สมมติเราอยากปล่อย feature X เข้า production ภายใน 2 เดือน จากสภาพโปรเจกต์ตอนนี้ ช่วยทำ roadmap ให้หน่อยว่า
>
> - ภายใน 1–2 sprint ข้างหน้าเราควรโฟกัสอะไรบ้าง
> - ควรรัน workflow ตัวไหนในแต่ละช่วง
> - มีความเสี่ยงด้าน security / CI / UI / performance ตรงไหนที่ควรจัดการก่อน

**copilot:**

- ตรวจ spec/plan/tasks/report ที่เกี่ยวข้องกับ feature X
- แบ่งเป็น phase เช่น Spec/Plan → CI/Security → UI → Release
- ผูก phase กับ workflow เช่น
  - `smartspec_generate_spec`, `smartspec_generate_plan`
  - `smartspec_ci_quality_gate`, `smartspec_security_evidence_audit`
  - `smartspec_ui_validation`, `smartspec_ui_consistency_audit`
  - `smartspec_release_readiness`
- สรุปเป็น roadmap พร้อมรายการงานสำคัญ

---

# 6. Use case ระบบ Billing & Subscription (ตัวอย่างละเอียด)

use case นี้สำคัญเพราะแสดงวิธีที่ copilot ใช้ `SPEC_INDEX` + โครงไฟล์จริง → แปลเป็นคำสั่งที่รันได้ทันที

## 6.1 สภาพโปรเจกต์สมมติ

- ใน `.spec/SPEC_INDEX.json` พบว่า domain billing มี spec:
  - `spec-076-billing-system` → `specs/feature/spec-076-billing-system/spec.md`
  - `spec-090-billing-and-subscription-ui` → `specs/feature/spec-090-billing-and-subscription-ui/spec.md`
- ในแต่ละโฟลเดอร์มีไฟล์:
  - `spec.md` ✅
  - `plan.md` ✅
  - `tasks.md` ❌ ยังไม่มี

## 6.2 ผู้ใช้ถามเป็นภาษาคน

> อยากเช็คความคืบหน้าระบบ billing หน่อย ทั้งระบบ billing core และระบบเรียกเก็บเงินตาม subscription plan พัฒนาไปถึงขั้นตอนไหนแล้ว และควรทำอะไรต่อ

## 6.3 สิ่งที่ copilot ควรทำเบื้องหลัง

1. ใช้ `SPEC_INDEX` ค้นหาคำว่า `billing`, `subscription` → เจอ 2 spec ข้างต้น
2. เปิดดูโฟลเดอร์ของแต่ละ spec แล้วเช็กว่า **มีไฟล์อะไรแล้วบ้าง**
3. สรุปเป็น phase:
   - Spec phase       : 100% (มี `spec.md`)
   - Plan phase       : 100% (มี `plan.md`)
   - Tasks/Implementation plan : 0% (ยังไม่มี `tasks.md`)
4. ประเมินความคืบหน้าภาพรวมของระบบ billing ว่าอยู่ช่วง “พร้อมวางแผน implementation” แต่ยังไม่ define tasks
5. แนะนำสิ่งที่ควรทำต่อเป็น **คำสั่งที่ run ได้ทันที**

## 6.4 ตัวอย่างคำตอบที่คาดหวัง (ย่อ)

> **สรุปภาพรวมระบบ Billing & Subscription**
>
> - ระบบ billing ปัจจุบันมี 2 spec หลัก:
>   1. `spec-076-billing-system`
>   2. `spec-090-billing-and-subscription-ui`
> - ทั้งคู่มี `spec.md` และ `plan.md` แล้ว → phase spec/plan ถือว่า \~100%
> - ยังไม่พบ `tasks.md` → phase Implementation plan ยัง \~0%
>
> **สิ่งที่ควรทำต่อ:**
>
> 1. สร้าง `tasks.md` สำหรับ billing core
>
> ```bash
> /smartspec_generate_tasks specs/feature/spec-076-billing-system
> ```
>
> 2. สร้าง `tasks.md` สำหรับ Billing & Subscription UI
>
> ```bash
> /smartspec_generate_tasks specs/feature/spec-090-billing-and-subscription-ui
> ```
>
> ถ้าคุณรันคำสั่งเหล่านี้บน Kilo ให้เพิ่ม `--kilocode` ต่อท้ายทุกคำสั่ง เช่น
>
> ```bash
> /smartspec_generate_tasks specs/feature/spec-076-billing-system --kilocode
> /smartspec_generate_tasks specs/feature/spec-090-billing-and-subscription-ui --kilocode
> ```
>
> หลังจากสร้าง `tasks.md` แล้ว แนะนำให้รัน copilot อีกครั้งเพื่อตรวจ ความคืบหน้าระดับ tasks และวางแผน CI/security/UI ต่อไป

## 6.5 ตัวอย่างคำตอบที่คาดหวัง
```
/smartspec_project_copilot \
  --aspect=roadmap \
  --lang=th \
  --spec-path=specs/core/spec-core-UM-001/spec.md \
  "สรุปงานค้าง user management ที่ยังไม่เสร็จ และให้ตอบตามโครงสร้างต่อไปนี้:
   1) Status summary
   2) ปัญหาร้ายแรงและวิธีแก้ไข (Critical issues & remediation)
   3) แผนแก้ไขเป็นระยะ (Timeline / phased plan)
   4) คำสั่ง SmartSpec ที่ควรใช้ต่อไป (พร้อมตัวอย่างคำสั่ง /smartspec_... ที่รันได้จริง)
   5) Weakness & Risk Check"
```

---

# 7. การใช้ร่วมกับ Kilo (`--kilocode`)

เมื่อใช้คู่กับ Kilo และเพิ่ม `--kilocode`:

- copilot จะถูกมองเป็น workflow แบบ **Ask/Architect**
- Kilo Orchestrator เป็นคนช่วย:
  - วิเคราะห์ intent จากข้อความ
  - วางแผนว่าจะอ่านไฟล์ไหนบ้าง
  - อ่านไฟล์ทีละ chunk (\~300–600 บรรทัด) และสรุป
- copilot จะเน้นสรุปและแนะนำ ไม่เขียนโค้ดเอง

ตัวอย่างคำถามบวกคำสั่ง (เชิงแนวคิด):

```bash
/smartspec_project_copilot --kilocode
```

ข้อความที่พิมพ์ถาม:

> อยากรู้ว่าใน sprint นี้ สำหรับ service checkout ควรทำอะไรต่อบ้างเพื่อให้พร้อมปล่อย production ช่วยวางลำดับงาน และแนะนำ workflow ที่ควรใช้ให้หน่อย

copilot ควรตอบเป็นลำดับงาน เช่น

- ปรับ spec/plan ให้ครบ → `/smartspec_generate_spec`, `/smartspec_generate_plan`
- ตั้ง CI gate → `/smartspec_ci_quality_gate`
- เก็บ security evidence → `/smartspec_security_evidence_audit`
- ตรวจ UI → `/smartspec_ui_validation`, `/smartspec_ui_consistency_audit`
- ตรวจ readiness → `/smartspec_release_readiness`

พร้อมตัวอย่างคำสั่งที่แนะนำให้ใช้บน Kilo (มี `--kilocode` ต่อท้าย)

---

# 8. สรุป Do / Don’t

**ควรทำ**

- ใช้ copilot เป็นจุดเริ่มถามทุกอย่างเกี่ยวกับสถานะโปรเจกต์
- พิมพ์ถามเป็นภาษาคน แล้วให้ copilot แปลเป็น spec/plan/tasks/workflow ให้
- ถ้ามี report อยู่แล้วให้ copy มาวางแล้วถามว่า “จาก report นี้ต้องทำอะไรต่อ”
- ใช้ `--kilocode` เมื่อรันบน Kilo เพื่อให้ Orchestrator ช่วยจัดการ context และแผนงาน

**ไม่ควรทำ**

- คาดหวังให้ copilot แก้โค้ดหรือแก้ไฟล์ให้เอง (มันเป็น NO-WRITE)
- ใช้ copilot แทน security/architect review ทั้งหมด
- เพิกเฉยต่อคำเตือนเรื่อง version, CVE, design system ที่ copilot ชี้

---

# 9. Backward Compatibility Notes

- คู่มือนี้รองรับ workflow เวอร์ชัน `5.6.x` ทั้งช่วง
- ถ้าในอนาคตมี flag/ความสามารถใหม่เพิ่มเข้ามา ควรเพิ่มเข้าไปแบบ additive โดยไม่ลบตัวอย่าง/คำอธิบายเดิม

---

# 10. Troubleshooting พื้นฐาน

- ถ้า copilot ตอบว่าไม่พบ `SPEC_INDEX` → ตรวจว่า `.spec/SPEC_INDEX.json` มีจริงหรือไม่
- ถ้าบอกว่าไม่พบ registry สำคัญ (เช่น `tool-version-registry.json`) → ให้สร้างตาม ที่ KB แนะนำแล้วรัน copilot ใหม่
- ถ้าคำตอบดูไม่อัปเดตกับ workflow เวอร์ชันล่าสุด → ตรวจว่า `.smartspec` และ `.smartspec-docs` ถูกอัปเดตมาจาก distribution repo ล่าสุดแล้วหรือยัง

เมื่อมีข้อสงสัยเพิ่มเติม ให้ Platform/Architecture team ตรวจ version ของ KB, workflow และสคริปต์ติดตั้ง ก่อน debug เพิ่มเติมเสมอ

