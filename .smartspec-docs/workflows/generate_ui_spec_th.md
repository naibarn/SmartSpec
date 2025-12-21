# `/smartspec_generate_ui_spec` - สร้าง UI Specification

| ข้อมูล | ค่า |
|--------|-----|
| **Workflow ID** | `smartspec_generate_ui_spec` |
| **หมวดหมู่** | UI / A2UI |
| **เวอร์ชัน** | 6.0.0+ |
| **ต้องใช้ `--apply`** | ใช่ |
| **รองรับแพลตฟอร์ม** | CLI, Kilo Code |

---

## ภาพรวม

สร้าง UI specification ที่เป็นไปตาม A2UI จาก requirements ภาษาธรรมชาติ workflow นี้สร้าง UI specification ที่มีการกำกับดูแลและไม่ขึ้นกับแพลตฟอร์มในรูปแบบ A2UI ซึ่งทำหน้าที่เป็น single source of truth สำหรับการ implement UI ข้ามหลายแพลตฟอร์ม (Web, Flutter, React ฯลฯ)

ไฟล์ `ui-spec.json` ที่สร้างขึ้นจะปฏิบัติตามข้อกำหนด A2UI v0.8 และรวมถึงโครงสร้าง component, layout, styling, interactions และ accessibility requirements

---

## การใช้งาน

### CLI

```bash
/smartspec_generate_ui_spec \
  --requirements "สร้างฟอร์มจองร้านอาหารพร้อม date picker, time selector, จำนวนผู้เข้าร่วม และคำขอพิเศษ" \
  --spec specs/feature/spec-001-booking/ui-spec.json
```

### Kilo Code

```bash
/smartspec_generate_ui_spec.md \
  --requirements "สร้างฟอร์มจองร้านอาหารพร้อม date picker, time selector, จำนวนผู้เข้าร่วม และคำขอพิเศษ" \
  --spec specs/feature/spec-001-booking/ui-spec.json \
  --platform kilo
```

---

## กรณีการใช้งาน

### 1. สร้าง UI Spec จาก Requirements

**สถานการณ์:** สร้าง UI specification สำหรับฟีเจอร์ฟอร์มจองใหม่

**คำสั่ง:**
```bash
/smartspec_generate_ui_spec \
  --requirements "สร้างฟอร์มจองร้านอาหารพร้อม date picker, time selector, จำนวนผู้เข้าร่วม และคำขอพิเศษ" \
  --spec specs/feature/spec-001-booking/ui-spec.json \
  --target-platform web \
  --accessibility wcag-aa
```

**ผลลัพธ์ที่คาดหวัง:** ไฟล์ `ui-spec.json` ที่สมบูรณ์พร้อม form components, validation rules และ accessibility attributes

### 2. สร้าง UI Spec พร้อมการอ้างอิง Design

**สถานการณ์:** สร้าง UI specification จาก design mockup

**คำสั่ง:**
```bash
/smartspec_generate_ui_spec \
  --requirements "ทำ dashboard layout ตาม mockup" \
  --spec specs/feature/spec-002-dashboard/ui-spec.json \
  --mockup designs/dashboard-mockup.png \
  --style material
```

**ผลลัพธ์ที่คาดหวัง:** UI specification ที่ตรงกับ design mockup พร้อม Material Design components

### 3. การสร้าง UI Spec แบบ Interactive

**สถานการณ์:** สร้าง UI spec พร้อมการปรับแต่งแบบวนซ้ำ

**คำสั่ง:**
```bash
/smartspec_generate_ui_spec \
  --requirements "สร้างหน้าแก้ไขโปรไฟล์ผู้ใช้" \
  --spec specs/feature/spec-003-profile/ui-spec.json \
  --interactive \
  --context-spec specs/feature/spec-003-profile/spec.md
```

**ผลลัพธ์ที่คาดหวัง:** เซสชันแบบโต้ตอบที่คุณสามารถปรับแต่ง UI spec ตาม preview และ feedback

---

## พารามิเตอร์

### พารามิเตอร์ที่จำเป็น

| พารามิเตอร์ | ประเภท | คำอธิบาย |
|-------------|--------|----------|
| `--requirements` | string | UI requirements ภาษาธรรมชาติ (inline หรือ file path) |
| `--spec` | path | เส้นทางสำหรับบันทึกไฟล์ ui-spec.json ที่สร้างขึ้น |

### Flags ทั่วไป

| Flag | ประเภท | ค่าเริ่มต้น | คำอธิบาย |
|------|--------|-------------|----------|
| `--apply` | boolean | false | นำการเปลี่ยนแปลงไปใช้ (ไม่มี flag นี้จะทำงานใน preview mode) |
| `--platform` | string | cli | แพลตฟอร์ม: cli, kilo |
| `--verbose` | boolean | false | เปิดใช้งาน verbose output |
| `--dry-run` | boolean | false | จำลองโดยไม่ทำการเปลี่ยนแปลง |
| `--report-dir` | path | auto | ไดเรกทอรีรายงานแบบกำหนดเอง |
| `--force` | boolean | false | บังคับเขียนทับไฟล์ที่มีอยู่ |

### Flags เฉพาะ Workflow

| Flag | ประเภท | ค่าเริ่มต้น | คำอธิบาย |
|------|--------|-------------|----------|
| `--target-platform` | string | web | แพลตฟอร์มเป้าหมาย: web, flutter, mobile, all |
| `--catalog` | path | .spec/ui-catalog.json | เส้นทางไปยัง component catalog |
| `--style` | string | from config | Style preset: material, fluent, custom |
| `--accessibility` | string | from config | ระดับ accessibility: basic, wcag-aa, wcag-aaa |
| `--interactive` | boolean | false | เปิดใช้งาน interactive mode พร้อมการปรับแต่ง |
| `--context-spec` | path | - | เส้นทางไปยัง functional spec สำหรับ context |
| `--mockup` | path | - | เส้นทางไปยัง design mockup/reference image |

---

## ผลลัพธ์

### ตำแหน่งรายงาน
```
.spec/reports/generate-ui-spec/<run-id>/
├── report.md              # สรุปที่อ่านได้
├── report.json            # ข้อมูลที่เครื่องอ่านได้
└── preview/
    ├── ui-spec.json       # Preview ของ spec ที่สร้าง
    └── mockup.png         # Visual preview (ถ้ามี)
```

### ไฟล์ที่สร้างขึ้น (พร้อม `--apply`)
- `<spec-path>` - ไฟล์ UI specification JSON ที่เป็นไปตาม A2UI

### โครงสร้าง UI Spec
```json
{
  "version": "0.8",
  "metadata": { ... },
  "components": [ ... ],
  "layout": { ... },
  "styling": { ... },
  "interactions": [ ... ],
  "accessibility": { ... },
  "validation": { ... }
}
```

---

## ข้อกำหนดเบื้องต้น

**จำเป็น:**
- A2UI ต้องเปิดใช้งานใน `.spec/smartspec.config.yaml` (`a2ui.enabled: true`)
- UI component catalog ต้องมีอยู่ (`.spec/ui-catalog.json`) หรือ preset ต้องถูกกำหนดค่า

**ไม่บังคับ:**
- Functional specification ที่มีอยู่สำหรับ context
- Design references หรือ mockups
- Accessibility requirements

---

## หมายเหตุ

1. **Preview ก่อน:** ควรรันโดยไม่มี `--apply` ก่อนเสมอเพื่อตรวจสอบ UI spec ที่สร้างขึ้น
2. **รูปแบบ Requirements:** สามารถเป็น inline string หรือเส้นทางไปยังไฟล์ requirements
3. **Platform Agnostic:** Spec ที่สร้างขึ้นทำงานได้ทั้ง web, mobile และ desktop platforms
4. **การนำ Catalog กลับมาใช้:** นำ components จาก catalog ที่มีอยู่กลับมาใช้โดยอัตโนมัติ
5. **Accessibility:** ปฏิบัติตามแนวทาง WCAG เมื่อระบุ `--accessibility`
6. **Interactive Mode:** ใช้ `--interactive` สำหรับการปรับแต่งแบบวนซ้ำพร้อม visual feedback
7. **การบูรณาการ Design:** ใช้ `--mockup` เพื่อสร้าง spec จากไฟล์ design

---

## Workflows ที่เกี่ยวข้อง

- [`/smartspec_generate_ui_implementation`](./generate_ui_implementation_th.md) - สร้างโค้ด UI จาก spec
- [`/smartspec_ui_catalog_generator`](./ui_catalog_generator_th.md) - สร้าง component catalog
- [`/smartspec_ui_validation`](./ui_validation_manual_th.md) - ตรวจสอบการ implement UI
- [`/smartspec_ui_component_audit`](./ui_component_audit_th.md) - ตรวจสอบ UI components

---

**สำหรับข้อมูลเพิ่มเติม ดูที่ [เอกสาร A2UI](../../README-A2UI.md)**
