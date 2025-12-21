# `/smartspec_ui_catalog_generator` - สร้าง UI Component Catalog

| ข้อมูล | ค่า |
|--------|-----|
| **Workflow ID** | `smartspec_ui_catalog_generator` |
| **หมวดหมู่** | UI / A2UI |
| **เวอร์ชัน** | 6.0.0+ |
| **ต้องใช้ `--apply`** | ใช่ |
| **รองรับแพลตฟอร์ม** | CLI, Kilo Code |

---

## ภาพรวม

สร้าง UI component catalog ที่ครอบคลุมจาก UI specifications และ implementations ที่มีอยู่ workflow นี้สแกนโปรเจกต์ของคุณเพื่อหา UI components วิเคราะห์โครงสร้างและการใช้งาน และสร้างหรืออัปเดตไฟล์ `.spec/ui-catalog.json` ที่ทำหน้าที่เป็น component library สำหรับ A2UI workflows

Catalog ที่สร้างขึ้นรวมถึง component definitions, variants, properties, accessibility features และตัวอย่างการใช้งาน

---

## การใช้งาน

### CLI

```bash
/smartspec_ui_catalog_generator \
  --scan-dir src/ui \
  --output .spec/ui-catalog.json
```

### Kilo Code

```bash
/smartspec_ui_catalog_generator.md \
  --scan-dir src/ui \
  --output .spec/ui-catalog.json \
  --platform kilo
```

---

## กรณีการใช้งาน

### 1. สร้าง Catalog จาก Components ที่มีอยู่

**สถานการณ์:** สร้าง catalog จาก React components ที่มีอยู่

**คำสั่ง:**
```bash
/smartspec_ui_catalog_generator \
  --scan-dir src/components \
  --target-platform web \
  --framework react \
  --output .spec/ui-catalog.json
```

**ผลลัพธ์ที่คาดหวัง:** Catalog ที่สมบูรณ์พร้อม components, props และ usage patterns ที่ค้นพบทั้งหมด

### 2. อัปเดต Catalog ด้วย Components ใหม่

**สถานการณ์:** เพิ่ม components ที่สร้างใหม่เข้าไปใน catalog ที่มีอยู่

**คำสั่ง:**
```bash
/smartspec_ui_catalog_generator \
  --scan-dir src/components/new \
  --merge \
  --output .spec/ui-catalog.json
```

**ผลลัพธ์ที่คาดหวัง:** Catalog ที่มีอยู่ได้รับการอัปเดตด้วย components ใหม่โดยรักษารายการที่มีอยู่ไว้

### 3. สร้าง Catalog จาก UI Specs

**สถานการณ์:** สร้าง catalog จากไฟล์ UI specification

**คำสั่ง:**
```bash
/smartspec_ui_catalog_generator \
  --scan-specs specs/feature/*/ui-spec.json \
  --include-variants \
  --output .spec/ui-catalog.json
```

**ผลลัพธ์ที่คาดหวัง:** Catalog ที่สร้างจาก spec definitions รวมถึง component variants ทั้งหมด

---

## พารามิเตอร์

### พารามิเตอร์ที่จำเป็น

| พารามิเตอร์ | ประเภท | คำอธิบาย |
|-------------|--------|----------|
| `--scan-dir` หรือ `--scan-specs` | path | ไดเรกทอรีที่จะสแกนหา components หรือ specs pattern |
| `--output` | path | เส้นทางผลลัพธ์สำหรับไฟล์ catalog |

### Flags ทั่วไป

| Flag | ประเภท | ค่าเริ่มต้น | คำอธิบาย |
|------|--------|-------------|----------|
| `--apply` | boolean | false | นำการเปลี่ยนแปลงไปใช้ (ไม่มี flag นี้จะทำงานใน preview mode) |
| `--platform` | string | cli | แพลตฟอร์ม: cli, kilo |
| `--verbose` | boolean | false | เปิดใช้งาน verbose output |
| `--dry-run` | boolean | false | จำลองโดยไม่ทำการเปลี่ยนแปลง |
| `--report-dir` | path | auto | ไดเรกทอรีรายงานแบบกำหนดเอง |
| `--force` | boolean | false | บังคับเขียนทับ catalog ที่มีอยู่ |

### Flags เฉพาะ Workflow

| Flag | ประเภท | ค่าเริ่มต้น | คำอธิบาย |
|------|--------|-------------|----------|
| `--target-platform` | string | auto | แพลตฟอร์มเป้าหมาย: web, flutter, mobile |
| `--framework` | string | auto | Framework: react, vue, angular, flutter |
| `--merge` | boolean | false | ผสานกับ catalog ที่มีอยู่แทนที่จะแทนที่ |
| `--include-variants` | boolean | true | รวม component variants ใน catalog |
| `--include-examples` | boolean | true | รวมตัวอย่างการใช้งาน |
| `--include-accessibility` | boolean | true | รวม accessibility metadata |
| `--exclude-pattern` | string | - | Glob pattern สำหรับไฟล์ที่จะยกเว้น |
| `--category-mapping` | path | - | ไฟล์ category mapping แบบกำหนดเอง |
| `--security-level` | string | review-required | ระดับความปลอดภัยเริ่มต้น: safe, trusted, review-required |

---

## ผลลัพธ์

### ตำแหน่งรายงาน
```
.spec/reports/ui-catalog-generator/<run-id>/
├── report.md              # สรุปที่อ่านได้
├── report.json            # ข้อมูลที่เครื่องอ่านได้
└── preview/
    ├── catalog.json       # Preview ของ catalog ที่สร้าง
    ├── components.md      # รายการ component
    └── statistics.json    # สถิติ catalog
```

### ไฟล์ที่สร้างขึ้น (พร้อม `--apply`)
- `.spec/ui-catalog.json` - UI component catalog ที่สมบูรณ์

### โครงสร้าง Catalog
```json
{
  "version": "0.8",
  "metadata": {
    "generated": "2025-12-22T...",
    "component_count": 42,
    "platform": "web"
  },
  "categories": {
    "input": [...],
    "layout": [...],
    "data": [...],
    "feedback": [...],
    "overlay": [...],
    "basic": [...]
  },
  "components": [
    {
      "id": "button",
      "name": "Button",
      "category": "basic",
      "variants": [...],
      "properties": [...],
      "accessibility": {...},
      "examples": [...]
    }
  ]
}
```

---

## ฟีเจอร์ Catalog

### การค้นหา Component
- ✅ การตรวจจับ component อัตโนมัติ
- ✅ การดึง props/properties
- ✅ การระบุ variant
- ✅ การวิเคราะห์ dependency

### การดึง Metadata
- ✅ เอกสาร component
- ✅ ตัวอย่างการใช้งาน
- ✅ ฟีเจอร์ accessibility
- ✅ ความเข้ากันได้ของแพลตฟอร์ม

### การจัดหมวดหมู่
- ✅ การกำหนด category อัตโนมัติ
- ✅ Custom category mapping
- ✅ ความสัมพันธ์ของ component
- ✅ การจัดประเภทความปลอดภัย

### การตรวจสอบ
- ✅ Schema validation
- ✅ การตรวจจับรายการซ้ำ
- ✅ ความสอดคล้องของการตั้งชื่อ
- ✅ Accessibility compliance

---

## ข้อกำหนดเบื้องต้น

**จำเป็น:**
- A2UI เปิดใช้งานใน config
- Source code หรือ UI specs สำหรับสแกน
- สิทธิ์เขียนไปยังไดเรกทอรี `.spec/`

**ไม่บังคับ:**
- Catalog ที่มีอยู่สำหรับการผสาน
- Custom category mapping
- เอกสาร component

---

## หมายเหตุ

1. **Preview ก่อน:** ควรรันโดยไม่มี `--apply` เพื่อตรวจสอบ components ที่ค้นพบ
2. **Merge Mode:** ใช้ `--merge` เพื่อเพิ่มเข้าไปใน catalog ที่มีอยู่โดยไม่สูญเสียรายการ
3. **การยกเว้น:** ใช้ `--exclude-pattern` เพื่อข้ามไฟล์ test, stories ฯลฯ
4. **ความปลอดภัย:** Components มีระดับความปลอดภัยเริ่มต้นเป็น `review-required`
5. **การตรวจจับแพลตฟอร์ม:** Framework และ platform จะถูกตรวจจับอัตโนมัติเมื่อเป็นไปได้
6. **Variants:** Component variants จะถูกระบุและจัดทำ catalog โดยอัตโนมัติ
7. **Accessibility:** ฟีเจอร์ WCAG compliance จะถูกดึงออกมาเมื่อมีอยู่
8. **การอัปเดต:** รันใหม่เพื่ออัปเดต catalog เมื่อ components เปลี่ยนแปลง

---

## Workflows ที่เกี่ยวข้อง

- [`/smartspec_generate_ui_spec`](./generate_ui_spec_th.md) - สร้าง UI specification
- [`/smartspec_optimize_ui_catalog`](./optimize_ui_catalog_th.md) - เพิ่มประสิทธิภาพ catalog
- [`/smartspec_ui_component_audit`](./ui_component_audit_th.md) - ตรวจสอบ components
- [`/smartspec_manage_ui_catalog`](./ui_catalog_generator_th.md) - จัดการ catalog ด้วยตนเอง

---

**สำหรับข้อมูลเพิ่มเติม ดูที่ [เอกสาร A2UI](../../README-A2UI.md)**
