# `/smartspec_generate_ui_implementation` - สร้างการ Implement UI

| ข้อมูล | ค่า |
|--------|-----|
| **Workflow ID** | `smartspec_generate_ui_implementation` |
| **หมวดหมู่** | UI / A2UI |
| **เวอร์ชัน** | 6.0.0+ |
| **ต้องใช้ `--apply`** | ใช่ |
| **รองรับแพลตฟอร์ม** | CLI, Kilo Code |

---

## ภาพรวม

สร้างโค้ดการ implement UI เฉพาะแพลตฟอร์มจาก A2UI specification workflow นี้แปลงไฟล์ `ui-spec.json` ที่ไม่ขึ้นกับแพลตฟอร์มให้เป็นโค้ด UI พร้อมใช้งานสำหรับแพลตฟอร์มเป้าหมายของคุณ (Web/React, Flutter, React Native ฯลฯ)

โค้ดที่สร้างขึ้นรวมถึงโครงสร้าง component, styling, data bindings, event handlers และ accessibility attributes ทั้งหมดปฏิบัติตาม best practices สำหรับแพลตฟอร์มเป้าหมาย

---

## การใช้งาน

### CLI

```bash
/smartspec_generate_ui_implementation \
  --spec specs/feature/spec-001-booking/ui-spec.json \
  --output src/ui/booking \
  --target-platform web
```

### Kilo Code

```bash
/smartspec_generate_ui_implementation.md \
  --spec specs/feature/spec-001-booking/ui-spec.json \
  --output src/ui/booking \
  --target-platform web \
  --platform kilo
```

---

## กรณีการใช้งาน

### 1. สร้าง React Web Implementation

**สถานการณ์:** สร้าง React components จาก UI specification

**คำสั่ง:**
```bash
/smartspec_generate_ui_implementation \
  --spec specs/feature/spec-001-booking/ui-spec.json \
  --output src/ui/booking \
  --target-platform web \
  --framework react \
  --typescript
```

**ผลลัพธ์ที่คาดหวัง:** React components พร้อม TypeScript, hooks และ styled-components

### 2. สร้าง Flutter Mobile Implementation

**สถานการณ์:** สร้าง Flutter widgets สำหรับ mobile app

**คำสั่ง:**
```bash
/smartspec_generate_ui_implementation \
  --spec specs/feature/spec-002-dashboard/ui-spec.json \
  --output lib/ui/dashboard \
  --target-platform flutter \
  --state-management bloc
```

**ผลลัพธ์ที่คาดหวัง:** Flutter widgets พร้อม BLoC pattern และ Material Design

### 3. สร้างพร้อม Custom Styling

**สถานการณ์:** สร้าง UI พร้อม custom design system

**คำสั่ง:**
```bash
/smartspec_generate_ui_implementation \
  --spec specs/feature/spec-003-profile/ui-spec.json \
  --output src/ui/profile \
  --target-platform web \
  --style-system custom \
  --theme-file src/theme/custom-theme.ts
```

**ผลลัพธ์ที่คาดหวัง:** Components ที่ใช้ custom design tokens และ theme

---

## พารามิเตอร์

### พารามิเตอร์ที่จำเป็น

| พารามิเตอร์ | ประเภท | คำอธิบาย |
|-------------|--------|----------|
| `--spec` | path | เส้นทางไปยังไฟล์ UI specification JSON |
| `--output` | path | ไดเรกทอรีผลลัพธ์สำหรับโค้ดที่สร้างขึ้น |
| `--target-platform` | string | แพลตฟอร์มเป้าหมาย: web, flutter, mobile |

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
| `--framework` | string | auto | Framework: react, vue, angular, flutter, react-native |
| `--typescript` | boolean | false | สร้างโค้ด TypeScript (สำหรับ web platforms) |
| `--style-system` | string | from config | วิธีการ styling: css-modules, styled-components, tailwind, material |
| `--state-management` | string | auto | State management: hooks, redux, bloc, provider |
| `--theme-file` | path | - | เส้นทางไปยังไฟล์ custom theme/design tokens |
| `--catalog` | path | .spec/ui-catalog.json | เส้นทางไปยัง component catalog |
| `--include-tests` | boolean | false | สร้าง unit tests สำหรับ components |
| `--include-stories` | boolean | false | สร้าง Storybook stories (web เท่านั้น) |

---

## ผลลัพธ์

### ตำแหน่งรายงาน
```
.spec/reports/generate-ui-implementation/<run-id>/
├── report.md              # สรุปที่อ่านได้
├── report.json            # ข้อมูลที่เครื่องอ่านได้
└── preview/
    ├── components/        # Preview ของ components ที่สร้าง
    └── structure.md       # ภาพรวมโครงสร้างไฟล์
```

### ไฟล์ที่สร้างขึ้น (พร้อม `--apply`)

**สำหรับ Web/React:**
```
<output-dir>/
├── components/
│   ├── BookingForm.tsx
│   ├── BookingForm.module.css
│   └── index.ts
├── hooks/
│   └── useBookingForm.ts
└── types/
    └── booking.types.ts
```

**สำหรับ Flutter:**
```
<output-dir>/
├── widgets/
│   ├── booking_form.dart
│   └── booking_form_state.dart
├── models/
│   └── booking_model.dart
└── bloc/
    ├── booking_bloc.dart
    └── booking_event.dart
```

---

## ฟีเจอร์การสร้างโค้ด

### โครงสร้าง Component
- ✅ Component hierarchy จาก spec
- ✅ Props/parameters พร้อม types
- ✅ State management setup
- ✅ Event handlers และ callbacks

### Styling
- ✅ Styling เฉพาะแพลตฟอร์ม
- ✅ Responsive design
- ✅ การบูรณาการ theme
- ✅ การใช้ design tokens

### Accessibility
- ✅ ARIA attributes (web)
- ✅ Semantic markup
- ✅ Keyboard navigation
- ✅ รองรับ screen reader

### Data Binding
- ✅ Form validation
- ✅ Data flow setup
- ✅ API integration hooks
- ✅ Error handling

---

## ข้อกำหนดเบื้องต้น

**จำเป็น:**
- ไฟล์ UI specification ที่ถูกต้อง (`ui-spec.json`)
- A2UI เปิดใช้งานใน config
- สภาพแวดล้อมการพัฒนาแพลตฟอร์มเป้าหมายตั้งค่าแล้ว

**ไม่บังคับ:**
- Component catalog สำหรับการนำกลับมาใช้
- Custom theme/design system
- Testing framework สำหรับการสร้าง test

---

## หมายเหตุ

1. **Preview ก่อน:** ควรรันโดยไม่มี `--apply` เพื่อตรวจสอบโครงสร้างโค้ดที่สร้างขึ้น
2. **Platform Best Practices:** โค้ดที่สร้างขึ้นปฏิบัติตามแบบแผนเฉพาะแพลตฟอร์ม
3. **การบูรณาการ Catalog:** นำ components ที่มีอยู่จาก catalog กลับมาใช้เมื่อเป็นไปได้
4. **การปรับแต่ง:** ใช้ `--theme-file` เพื่อบูรณาการกับ design system ที่มีอยู่
5. **การทดสอบ:** ใช้ `--include-tests` เพื่อสร้าง unit tests พร้อมกับ components
6. **Storybook:** ใช้ `--include-stories` สำหรับเอกสาร component (web เท่านั้น)
7. **Type Safety:** ใช้ `--typescript` สำหรับ React components ที่ปลอดภัยด้าน type

---

## Workflows ที่เกี่ยวข้อง

- [`/smartspec_generate_ui_spec`](./generate_ui_spec_th.md) - สร้าง UI specification
- [`/smartspec_verify_ui_implementation`](./ui_validation_manual_th.md) - ตรวจสอบการ implementation
- [`/smartspec_ui_test_generator`](./ui_test_generator_th.md) - สร้าง UI tests
- [`/smartspec_ui_catalog_generator`](./ui_catalog_generator_th.md) - สร้าง component catalog

---

**สำหรับข้อมูลเพิ่มเติม ดูที่ [เอกสาร A2UI](../../README-A2UI.md)**
