# smartspec_export_catalog

## ภาพรวม
**เวอร์ชัน:** 1.0.0  
**หมวดหมู่:** A2UI

ส่งออก UI catalog ของ SmartSpec เป็นรูปแบบ A2UI v0.8 มาตรฐาน เพื่อให้สามารถทำงานร่วมกับ A2UI renderers ภายนอกได้ โดยยังคงรักษา governance model ของ SmartSpec ไว้เป็น source of truth

## วัตถุประสงค์
Workflow นี้เชื่อมช่องว่างระหว่าง component catalog แบบ server-side ที่มี governance ของ SmartSpec กับ catalog model แบบ client-side ของ A2UI ทำให้ components ที่จัดการใน SmartSpec สามารถใช้งานได้กับ A2UI renderer ใดๆ ที่เป็นไปตามมาตรฐาน และเปิดเส้นทางที่ชัดเจนจาก SmartSpec governance ไปสู่ความสามารถในการทำงานร่วมกับ A2UI ecosystem

## การใช้งาน

### Command Line Interface
```bash
/smartspec_export_catalog \
  --output-file public/web-catalog.json \
  --catalog-id "https://my-app.com/web-catalog-v1" \
  --output-format a2ui-v0.8
```

### Kilo Code
```
ส่งออก catalog เป็นรูปแบบ A2UI สำหรับ web platform
```

## กรณีการใช้งาน

### 1. การ Deploy Web Application
**สถานการณ์:** คุณสร้าง component library โดยใช้ SmartSpec governance และตอนนี้ต้องการ deploy เป็น web application โดยใช้ A2UI renderer มาตรฐาน

**คำสั่ง:**
```bash
/smartspec_export_catalog \
  --input-catalog .spec/ui-catalog.json \
  --output-file public/web-catalog.json \
  --catalog-id "https://myapp.com/catalogs/web-v1" \
  --output-format a2ui-v0.8 \
  --platform web
```

**ผลลัพธ์:** ไฟล์ A2UI catalog มาตรฐานที่สามารถ compile เข้าไปใน React, Vue หรือ vanilla JavaScript web renderer ของคุณได้

---

### 2. การ Deploy แบบ Multi-Platform
**สถานการณ์:** คุณต้องการ deploy component library เดียวกันไปยังทั้ง web และ Flutter platforms

**คำสั่ง:**
```bash
# ส่งออกสำหรับ web
/smartspec_export_catalog \
  --output-file dist/web-catalog.json \
  --catalog-id "https://myapp.com/catalogs/web-v1" \
  --platform web

# ส่งออกสำหรับ Flutter
/smartspec_export_catalog \
  --output-file dist/flutter-catalog.json \
  --catalog-id "https://myapp.com/catalogs/flutter-v1" \
  --platform flutter
```

**ผลลัพธ์:** A2UI catalogs สองไฟล์ที่เฉพาะเจาะจงสำหรับแต่ละ platform โดยแต่ละไฟล์ถูกปรับให้เหมาะสมกับ renderer ปลายทางของมัน

---

### 3. การ Migrate แบบค่อยเป็นค่อยไป
**สถานการณ์:** คุณกำลัง migrate จากระบบ UI แบบกำหนดเองไปยัง A2UI และต้องการทดสอบความเข้ากันได้ก่อนที่จะ commit อย่างเต็มที่

**คำสั่ง:**
```bash
/smartspec_export_catalog \
  --output-file test/a2ui-catalog.json \
  --catalog-id "https://myapp.com/catalogs/test-v1" \
  --include-metadata
```

**ผลลัพธ์:** A2UI catalog ที่มี metadata ของ SmartSpec รวมอยู่เป็น comments ทำให้คุณสามารถตรวจสอบการแปลงและ debug ปัญหาใดๆ ได้

## พารามิเตอร์

### พารามิเตอร์ที่จำเป็น

| พารามิเตอร์ | ประเภท | คำอธิบาย |
|:-----------|:------|:---------|
| `--output-file` | string | เส้นทางที่จะเขียน A2UI catalog ที่ส่งออก (เช่น `public/web-catalog.json`) |
| `--catalog-id` | string | ตัวระบุเฉพาะสำหรับ catalog ที่ส่งออก โดยทั่วไปเป็น URL (เช่น `https://my-app.com/web-catalog-v1`) |
| `--output-format` | string | รูปแบบเป้าหมาย ปัจจุบันรองรับเฉพาะ `a2ui-v0.8` |

### พารามิเตอร์เสริม

| พารามิเตอร์ | ประเภท | ค่าเริ่มต้น | คำอธิบาย |
|:-----------|:------|:----------|:---------|
| `--input-catalog` | string | `.spec/ui-catalog.json` | เส้นทางไปยังไฟล์ SmartSpec catalog |
| `--platform` | string | (ไม่มี) | ตัวกรอง platform สำหรับ catalogs แบบ multi-platform (เช่น `web`, `flutter`, `mobile`) |
| `--include-metadata` | boolean | `false` | รวม metadata ของ SmartSpec เป็น comments ในผลลัพธ์ |

## ผลลัพธ์

Workflow นี้สร้าง:

1. **A2UI v0.8 Catalog Definition Document** (ไฟล์ JSON)
   - A2UI catalog ที่ถูกต้องพร้อม `catalogId` และ array `components`
   - แต่ละ component มี `id`, `type` และ object `properties`
   - Properties รวมถึง `type`, `description` และค่า `default`

2. **Transformation Report** (ผลลัพธ์ใน console)
   - จำนวน components ที่ส่งออก
   - จำนวน properties ที่แมป
   - คำเตือนหรือฟิลด์ที่ข้ามไป

### ตัวอย่างไฟล์ผลลัพธ์
```json
{
  "catalogId": "https://my-app.com/web-catalog-v1",
  "version": "0.8",
  "components": [
    {
      "id": "input-name",
      "type": "TextInput",
      "properties": {
        "label": {
          "type": "string",
          "description": "The text label for the component.",
          "default": "Name"
        },
        "required": {
          "type": "boolean",
          "description": "Whether the input is required.",
          "default": true
        },
        "placeholder": {
          "type": "string",
          "description": "Placeholder text for the input.",
          "default": "Enter your name"
        }
      }
    }
  ]
}
```

## ตรรกะการแปลง

### การแมป Component Type

| SmartSpec Type | A2UI Type |
|:---------------|:----------|
| `input-text` | `TextInput` |
| `input-email` | `EmailInput` |
| `button-primary` | `Button` |
| `data-table` | `Table` |
| `card` | `Card` |
| `modal` | `Modal` |

### การแมป Property

| SmartSpec Property | A2UI Property | หมายเหตุ |
|:-------------------|:--------------|:---------|
| `label` | `properties.label.default` | แมปเป็นค่า default |
| `required` | `properties.required.default` | แมปเป็นค่า default |
| `placeholder` | `properties.placeholder.default` | แมปเป็นค่า default |
| `validation` | (ไม่ส่งออก) | Metadata สำหรับ governance เท่านั้น |
| `complexity` | (ไม่ส่งออก) | Metadata สำหรับ governance เท่านั้น |
| `tags` | (ไม่ส่งออก) | Metadata สำหรับ governance เท่านั้น |

## Workflows ที่เกี่ยวข้อง

- **smartspec_manage_ui_catalog**: จัดการ SmartSpec catalog ต้นทางก่อนส่งออก
- **smartspec_generate_ui_spec**: สร้าง UI specs โดยใช้ SmartSpec catalog
- **smartspec_ui_component_audit**: ตรวจสอบ components ก่อนส่งออกเพื่อให้แน่ใจว่ามีคุณภาพ

## แนวทางปฏิบัติที่ดี

1. **ใส่เวอร์ชันใน Catalog ID**: ใช้ URL ที่มีเวอร์ชัน (เช่น `-v1`, `-v2`) ใน `catalog-id` เพื่อติดตาม breaking changes
2. **ส่งออกระหว่าง Build**: รวมขั้นตอนการส่งออกเข้าไปใน CI/CD pipeline ของคุณ
3. **เก็บ SmartSpec เป็น Source of Truth**: แก้ไข SmartSpec catalog เสมอ จากนั้นจึงส่งออกใหม่
4. **ทดสอบหลังส่งออก**: ตรวจสอบ catalog ที่ส่งออกกับ renderer ปลายทางของคุณก่อน deployment
5. **บันทึกความแตกต่างของ Platform**: ถ้าใช้ multi-platform ให้บันทึก properties ที่เฉพาะเจาะจงสำหรับแต่ละ platform

## หมายเหตุ

- Catalog ที่ส่งออกเป็น **derived artifact** SmartSpec catalog ยังคงเป็น source of truth
- Governance metadata (กฎ validation, complexity, tags) ถูกยกเว้นจาก A2UI export โดยตั้งใจ
- สำหรับการรองรับ multi-platform ให้ส่งออก catalogs แยกสำหรับแต่ละ platform
- `catalog-id` ควรปฏิบัติตามหลักการ URI และมีเวอร์ชันสำหรับ breaking changes

## ดูเพิ่มเติม

- [A2UI Export Utility Design](../../docs/guides/A2UI_EXPORT_UTILITY_DESIGN.md)
- [SmartSpec-Flavored A2UI](../../docs/guides/A2UI_SMARTSPEC_FLAVOR.md)
- [A2UI v0.8 Specification](https://a2ui.org/specification/v0.8-a2ui/)
