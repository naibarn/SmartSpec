| manual_name | manual_version | compatible_workflow | compatible_workflow_versions | role |
| --- | --- | --- | --- | --- |
| /smartspec_generate_spec_from_prompt Manual (TH) | 5.6 | /smartspec_generate_spec_from_prompt | 5.6.x | คู่มือผู้พัฒนา/ผู้ใช้งาน (เริ่มต้นสร้าง SPEC ครั้งแรกจาก prompt) |

# /smartspec_generate_spec_from_prompt คู่มือการใช้งาน (v5.6, ภาษาไทย)

## 1. ภาพรวม (Overview)

คู่มือนี้อธิบายการใช้งาน workflow:

> `/smartspec_generate_spec_from_prompt v5.6.x`

หน้าที่ของ workflow นี้คือ **สร้างไฟล์ `spec.md` ตั้งต้นจากข้อความ requirement ที่ผู้ใช้พิมพ์มา (prompt)** โดยอาศัยโครงสร้างโปรเจกต์ SmartSpec ที่มีอยู่แล้วเป็นบริบท เช่น โฟลเดอร์ `specs/**` และ `.spec/SPEC_INDEX.json` เป็นต้น

คุณสามารถพิมพ์ requirement เป็นภาษาไทยหรือภาษาอังกฤษก็ได้ แล้วให้ workflow ช่วย:

1. วิเคราะห์ว่าควรจัดกลุ่มอยู่ใน category ไหน (เช่น `ecommerce`, `miniapp`, `admin`)
2. ตั้งชื่อ `spec-id` ให้เหมาะสมและไม่ซ้ำของเดิม
3. สร้างโฟลเดอร์และไฟล์ `spec.md` 1–หลายไฟล์ให้อัตโนมัติ
4. แนะนำคำสั่ง `/smartspec_generate_spec` เพื่อใช้ปรับแต่ง SPEC ให้สมบูรณ์ยิ่งขึ้น

> **สำคัญ:** workflow นี้ใช้สำหรับ **สร้าง SPEC ครั้งแรก** เท่านั้น  
> เมื่อได้ไฟล์ `spec.md` แล้ว ให้ใช้ `/smartspec_generate_spec` เพื่อ refine ต่อทุกครั้ง

คุณสมบัติหลัก:

- role: Execution (เขียนไฟล์ใหม่)
- write_guard: ALLOW-WRITE แต่จำกัดเฉพาะ `specs/**` และการอัปเดต SPEC_INDEX เมื่อสั่ง `--update-index` เท่านั้น
- safety-mode: `normal` และ **ไม่ลบ/ไม่เขียนทับ `spec.md` เดิมเด็ดขาด**

---

## 2. มีอะไรใหม่ใน v5.6 (What’s New)

`/smartspec_generate_spec_from_prompt` เป็น workflow ใหม่ในชุดเวอร์ชัน 5.6

### 2.1 แปลง prompt → หลาย SPEC อัตโนมัติ

- รับ requirement หนึ่งชุด แล้วสามารถสร้าง SPEC ได้ **1–5 ไฟล์** ตามขนาดงาน
- ถ้า feature ใหญ่มาก (เช่น ecommerce shop ครบ flow) จะช่วยแตกเป็นส่วน ๆ เช่น
  - `ecommerce_shop_front`
  - `ecommerce_checkout_flow`
  - `ecommerce_order_billing`

### 2.2 ปลอดภัยต่อไฟล์เดิม

- เขียนไฟล์ได้เฉพาะใต้ `specs/**`
- เช็กก่อนเสมอว่ามี `spec-id` นี้อยู่แล้วหรือไม่
  - ถ้ามี `spec.md` อยู่แล้ว → **จะไม่เขียนทับ** แต่สร้างชื่อใหม่ เช่น `*_v2` แทน
- สรุปผลให้ใน output ว่าสร้างไฟล์อะไรบ้าง

### 2.3 อัปเดต SPEC_INDEX แบบ opt‑in

- โดยค่าเริ่มต้น **จะไม่แตะ `.spec/SPEC_INDEX.json`** เพื่อลดความเสี่ยง
- ถ้าต้องการให้เพิ่ม entry อัตโนมัติ ให้ใส่ `--update-index`
- ถ้าไม่ใส่ flag นี้ workflow จะพิมพ์ JSON ตัวอย่างให้เอาไปวางใน SPEC_INDEX เองภายหลัง

### 2.4 เนื้อหา SPEC ตั้งต้นแบบ SPEC-first

เนื้อหา `spec.md` ที่สร้างขึ้นจะพยายามทำตามแนวทาง SPEC-first ใน knowledge base ได้แก่:

- บริบทและเป้าหมายของ feature
- user roles และ user journey หลัก
- หน้าจอ/flow ที่สำคัญ
- การเชื่อมต่อระบบอื่น (เช่น payment, auth, AI, Kie.ai, ฯลฯ)
- data model / ตารางหลัก / แนวทางใช้ ORM (เช่น Prisma) ในระดับคร่าว ๆ
- NFR เช่น SEO, performance, latency, observability, security / privacy
- ไอเดียเวอร์ชันถัดไป (v2+) เช่น gallery, preset, advanced UX

---

## 3. หมายเหตุเรื่องความเข้ากันได้ย้อนหลัง (Backward Compatibility)

- เป็น workflow ใหม่ ไม่มี behaviour เดิมให้ต้องรักษา
- ไม่แตะหรือเปลี่ยน semantics ของ `/smartspec_generate_spec` หรือ workflow อื่น ๆ
- ใช้ semantics เดียวกับ workflow ชุด 5.6 ในเรื่อง
  - `--workspace-roots`, `--repos-config`,
  - `--registry-dir`, `--registry-roots`,
  - `--specindex`, `--kilocode` (ถ้าใช้งานผ่าน Kilo)

---

## 4. แนวคิดหลัก (Core Concepts)

### 4.1 SPEC ตั้งต้น vs SPEC ที่ refine แล้ว

- **SPEC ตั้งต้น** (สร้างด้วย workflow นี้)
  - ได้มาจาก prompt + context โปรเจกต์พอประมาณ
  - ใช้สำหรับคุยกับทีม product / design / dev ว่า scope คืออะไร
  - อาจยังไม่ลงลึกเรื่อง dependency / design system ทั้งหมด

- **SPEC ที่ refine แล้ว** (ปรับด้วย `/smartspec_generate_spec`)
  - ใช้ข้อมูลเพิ่มเติมจาก registry, SPEC_INDEX, spec อื่น ๆ ในโปรเจกต์
  - เน้นความสอดคล้องกับ governance, design system, security, ฯลฯ

### 4.2 category และ `spec-id`

workflow จะพยายามเดา category และ `spec-id` จาก:

- entries ที่มีอยู่ใน `.spec/SPEC_INDEX.json`
- โฟลเดอร์ภายใต้ `specs/**`
- คำสำคัญใน prompt (เช่น "shop", "checkout", "miniapp")

ถ้าดูแล้วไม่เข้า category ไหนชัดเจน จะ fallback ไปที่ category อย่าง `feature` และสร้าง slug จากชื่อ prompt ให้

### 4.3 การ split SPEC อัตโนมัติ

ค่าเริ่มต้น `--max-specs=3` หมายถึง ถ้างานใหญ่ workflow สามารถแยกออกเป็น 3 SPEC เช่น:

- `*_front` / `*_checkout` / `*_billing`
- หรือ `*_user_app` / `*_admin_console`

ถ้าอยากบังคับให้รวมเป็น SPEC เดียว ใช้ `--max-specs=1`

---

## 5. ตัวอย่างการใช้งาน (Quick Start Examples)

### 5.1 สร้าง SPEC สำหรับเว็บไซต์ ecommerce ครั้งแรก

```bash
/smartspec_generate_spec_from_prompt \
  "สร้าง website ที่สวยงาม ทันสมัย มี SEO ที่ดี แสดงรายการสินค้าและรูปภาพสินค้าบนหน้าแรก มีให้กดใส่ตะกร้า แล้วไปหน้า checkout สร้าง order และ invoice พร้อมรายละเอียดการโอนเงิน"
```

ผลลัพธ์ตัวอย่าง (สรุป):

- สร้าง:
  - `specs/ecommerce/ecommerce_shop_front/spec.md`
  - `specs/ecommerce/ecommerce_checkout_flow/spec.md`
  - `specs/ecommerce/ecommerce_order_billing/spec.md`
- คำสั่งขั้นถัดไปที่แนะนำ:
  - `/smartspec_generate_spec --spec-ids=ecommerce_shop_front`
  - `/smartspec_generate_spec --spec-ids=ecommerce_checkout_flow`
  - `/smartspec_generate_spec --spec-ids=ecommerce_order_billing`

### 5.2 บังคับให้เป็น SPEC เดียว

```bash
/smartspec_generate_spec_from_prompt \
  "สร้าง website ecommerce ตั้งแต่หน้าแคตตาล็อกจนถึง invoice แบบครบวงจร" \
  --max-specs=1
```

ผลลัพธ์:

- `specs/ecommerce/ecommerce_shop_full/spec.md`
- ขั้นถัดไป: `/smartspec_generate_spec --spec-ids=ecommerce_shop_full`

### 5.3 miniapp + AI (เช่น Kie.ai / Google Nano Banana Pro)

```bash
/smartspec_generate_spec_from_prompt \
  "สร้าง miniapp ให้ผู้ใช้ upload รูปภาพได้สูงสุด 5 รูป + พิมพ์ข้อความภาษาไทย แล้วให้ระบบแปลงข้อความไทยเป็น prompt แบบละเอียดสำหรับ Google Nano Banana Pro ผ่าน Kie.ai พร้อมหน้า gallery เก็บประวัติและแก้ไขรูปได้"
```

ตัวอย่างการ split:

- `specs/miniapp/miniapp_nano_banana_core/spec.md`
- `specs/miniapp/miniapp_nano_banana_gallery/spec.md`

### 5.4 ใช้งานบน Kilo

```bash
/smartspec_generate_spec_from_prompt.md \
  "สร้าง mobile + web app สำหรับระบบสมาชิกและสะสมแต้ม" \
  --kilocode
```

บน Kilo:

- Orchestrator สามารถแบ่งงานตาม spec-id ได้เอง
- Code mode เขียนไฟล์ใหม่เฉพาะใต้ `specs/**`

---

## 6. สรุป flag สำคัญ (CLI / Flags Cheat Sheet)

- **ใช้บ่อยที่สุด**
  - prompt แบบข้อความ (argument หลัก)
  - `--max-specs=<n>` (ค่าเริ่มต้น 3,ช่วง 1–5)
  - `--spec-category=<category>` (ถ้าอยากบังคับ category)
- **เกี่ยวกับ index และ multi-repo**
  - `--update-index` (ให้เพิ่มข้อมูลลง `.spec/SPEC_INDEX.json` อัตโนมัติ)
  - `--specindex=<path>`
  - `--workspace-roots=<paths>`
  - `--repos-config=<path>`
- **registry (อ่านอย่างเดียว)**
  - `--registry-dir=<path>`
  - `--registry-roots=<paths>`
- **ความปลอดภัย & Kilo**
  - `--dry-run` (ดูแผนก่อนสร้างไฟล์จริง)
  - `--kilocode` (กรณีรันบน Kilo Code)

สำหรับผู้ใช้ใหม่ แนะนำให้เริ่มจาก:

```bash
/smartspec_generate_spec_from_prompt "<คำอธิบาย feature ของคุณ>"
```

แบบไม่ใส่ flag ใด ๆ ก่อน

---

## 7. แนวทางใช้งานที่แนะนำ (Best Practices)

1. **เขียน prompt ให้ละเอียดพอสมควร**
   - ระบุกลุ่มผู้ใช้, flow หลัก, ฟังก์ชันสำคัญ, integration, NFR คร่าว ๆ
2. **ใช้ `--dry-run` ถ้าไม่มั่นใจเรื่องการ split**
   - ดูก่อนว่าจะสร้างกี่ SPEC และชื่ออะไรบ้าง
3. **เปิดดู `spec.md` ที่สร้างและอ่านคร่าว ๆ ทุกไฟล์**
   - ถ้า split แปลกไป สามารถเปลี่ยนชื่อ/ย้าย scope เองได้
4. **รัน `/smartspec_generate_spec` ต่อทุกครั้ง**
   - เพื่อให้ SPEC ตั้งต้นเข้าเฟรม governance และ design system ของโปรเจกต์
5. **ใช้คู่กับ `/smartspec_project_copilot`**
   - หลังสร้าง SPEC สามารถให้ project copilot ช่วยดูภาพรวม ว่า
     มี SPEC ใหม่ไหนบ้าง และควรวิ่ง workflow ไหนต่อ

---

## 8. FAQ / คำถามที่พบบ่อย

**ถาม: ถ้ามันสร้าง SPEC เยอะเกินไปทำยังไง?**  
ตอบ: ลด `--max-specs` เหลือ 1 หรือ 2 แล้วรันใหม่ หรือรวม scope เองใน `spec.md`

**ถาม: SPEC_INDEX ไม่ถูกอัปเดตอัตโนมัติจะมีปัญหาไหม?**  
ตอบ: ไม่มีปัญหากับตัว SPEC เอง (ไฟล์อยู่ครบ) เพียงแต่เครื่องมือบางตัวอาจไม่เห็น SPEC ใหม่นี้จนกว่าคุณจะ:

- รันใหม่พร้อม `--update-index`, หรือ
- นำ JSON snippet ที่ workflow พิมพ์ให้ ไปวางใน `.spec/SPEC_INDEX.json` เอง

**ถาม: อยากเขียนทับ SPEC เดิมได้ไหม?**  
ตอบ: workflow นี้ตั้งใจ **ไม่เขียนทับ** เพื่อความปลอดภัย ถ้าจำเป็นต้องแก้ ใช้วิธีแก้ไขไฟล์ด้วยตัวเองหรือออกแบบ workflow เฉพาะกิจ

**ถาม: SPEC ที่สร้างละเอียดแค่ไหน?**  
ตอบ: ละเอียดพอสำหรับใช้วางแผนงานและคุยกับทีมได้ทันที แต่ควรใช้
`/smartspec_generate_spec` ช่วย refine ต่อให้สอดคล้องกับระบบทั้งหมด

---

จบคู่มือ `/smartspec_generate_spec_from_prompt v5.6.x` (ภาษาไทย)

