# `/smartspec_ui_test_generator` - สร้าง UI Tests

| ข้อมูล | ค่า |
|--------|-----|
| **Workflow ID** | `smartspec_ui_test_generator` |
| **หมวดหมู่** | UI / A2UI / Testing |
| **เวอร์ชัน** | 6.0.0+ |
| **ต้องใช้ `--apply`** | ใช่ |
| **รองรับแพลตฟอร์ม** | CLI, Kilo Code |

---

## ภาพรวม

สร้างการทดสอบ UI อัตโนมัติจาก UI specifications workflow นี้สร้าง test suites ที่ครอบคลุมรวมถึง unit tests, integration tests และ end-to-end tests ตาม A2UI specification ของคุณ การทดสอบครอบคลุม component rendering, user interactions, accessibility และ data flow

การทดสอบที่สร้างขึ้นปฏิบัติตาม best practices สำหรับแพลตฟอร์มเป้าหมายและ testing framework ของคุณ

---

## การใช้งาน

### CLI

```bash
/smartspec_ui_test_generator \
  --spec specs/feature/spec-001-booking/ui-spec.json \
  --output tests/ui/booking \
  --test-type all
```

### Kilo Code

```bash
/smartspec_ui_test_generator.md \
  --spec specs/feature/spec-001-booking/ui-spec.json \
  --output tests/ui/booking \
  --test-type all \
  --platform kilo
```

---

## กรณีการใช้งาน

### 1. สร้าง Test Suite ที่สมบูรณ์

**สถานการณ์:** สร้าง unit, integration และ E2E tests สำหรับฟอร์มจอง

**คำสั่ง:**
```bash
/smartspec_ui_test_generator \
  --spec specs/feature/spec-001-booking/ui-spec.json \
  --output tests/ui/booking \
  --test-type all \
  --framework jest \
  --include-accessibility
```

**ผลลัพธ์ที่คาดหวัง:** Test suite ที่สมบูรณ์พร้อม unit tests, integration tests, E2E tests และ accessibility tests

### 2. สร้าง Unit Tests เท่านั้น

**สถานการณ์:** สร้าง unit tests สำหรับ components แต่ละตัว

**คำสั่ง:**
```bash
/smartspec_ui_test_generator \
  --spec specs/feature/spec-002-dashboard/ui-spec.json \
  --output tests/unit/dashboard \
  --test-type unit \
  --coverage-target 80
```

**ผลลัพธ์ที่คาดหวัง:** Unit tests สำหรับแต่ละ component พร้อมเป้าหมาย coverage 80%

### 3. สร้าง E2E Tests พร้อม Visual Regression

**สถานการณ์:** สร้าง end-to-end tests พร้อมการเปรียบเทียบ screenshot

**คำสั่ง:**
```bash
/smartspec_ui_test_generator \
  --spec specs/feature/spec-003-profile/ui-spec.json \
  --output tests/e2e/profile \
  --test-type e2e \
  --framework playwright \
  --visual-regression
```

**ผลลัพธ์ที่คาดหวัง:** E2E tests พร้อม visual regression testing โดยใช้ Playwright

---

## พารามิเตอร์

### พารามิเตอร์ที่จำเป็น

| พารามิเตอร์ | ประเภท | คำอธิบาย |
|-------------|--------|----------|
| `--spec` | path | เส้นทางไปยังไฟล์ UI specification JSON |
| `--output` | path | ไดเรกทอรีผลลัพธ์สำหรับไฟล์ test |

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
| `--test-type` | string | all | ประเภทการทดสอบ: unit, integration, e2e, all |
| `--framework` | string | auto | Testing framework: jest, vitest, playwright, cypress, flutter_test |
| `--target-platform` | string | auto | แพลตฟอร์มเป้าหมาย: web, flutter, mobile |
| `--include-accessibility` | boolean | true | รวมการทดสอบ accessibility |
| `--include-visual` | boolean | false | รวมการทดสอบ visual regression |
| `--coverage-target` | number | 80 | เป้าหมาย code coverage เป็นเปอร์เซ็นต์ |
| `--mock-api` | boolean | true | สร้าง API mocks สำหรับการทดสอบ |
| `--test-data` | path | - | เส้นทางไปยังไฟล์ test data |
| `--parallel` | boolean | true | เปิดใช้งานการทดสอบแบบขนาน |

---

## ผลลัพธ์

### ตำแหน่งรายงาน
```
.spec/reports/ui-test-generator/<run-id>/
├── report.md              # สรุปที่อ่านได้
├── report.json            # ข้อมูลที่เครื่องอ่านได้
└── preview/
    ├── test-plan.md       # ภาพรวม test plan
    ├── coverage-map.json  # Coverage mapping
    └── tests/             # Preview ของไฟล์ test
```

### ไฟล์ที่สร้างขึ้น (พร้อม `--apply`)

**สำหรับ Web/React พร้อม Jest:**
```
<output-dir>/
├── unit/
│   ├── BookingForm.test.tsx
│   ├── DatePicker.test.tsx
│   └── __mocks__/
├── integration/
│   └── BookingFlow.test.tsx
├── e2e/
│   └── booking.spec.ts
├── accessibility/
│   └── booking-a11y.test.tsx
└── setup/
    ├── test-utils.ts
    └── mocks.ts
```

**สำหรับ Flutter:**
```
<output-dir>/
├── widget_test/
│   ├── booking_form_test.dart
│   └── date_picker_test.dart
├── integration_test/
│   └── booking_flow_test.dart
└── test_utils/
    └── test_helpers.dart
```

---

## ความครอบคลุมการทดสอบ

### Unit Tests
- ✅ Component rendering
- ✅ Props validation
- ✅ State management
- ✅ Event handlers
- ✅ Edge cases

### Integration Tests
- ✅ Component interaction
- ✅ Data flow
- ✅ Form submission
- ✅ API integration
- ✅ Error handling

### E2E Tests
- ✅ User workflows
- ✅ Navigation
- ✅ Multi-step processes
- ✅ Cross-browser testing
- ✅ Performance metrics

### Accessibility Tests
- ✅ WCAG compliance
- ✅ Keyboard navigation
- ✅ Screen reader support
- ✅ Color contrast
- ✅ Focus management

---

## ข้อกำหนดเบื้องต้น

**จำเป็น:**
- ไฟล์ UI specification ที่ถูกต้อง
- Testing framework ติดตั้งแล้ว
- Test runner กำหนดค่าแล้ว

**ไม่บังคับ:**
- ไฟล์ test data
- Mock API definitions
- Visual regression baseline images

---

## หมายเหตุ

1. **Preview ก่อน:** ควรรันโดยไม่มี `--apply` เพื่อตรวจสอบ test plan
2. **การตรวจจับ Framework:** Testing framework จะถูกตรวจจับอัตโนมัติจาก project config
3. **Coverage:** การทดสอบที่สร้างขึ้นมุ่งเป้าไปที่ coverage target ที่ระบุ
4. **Mocking:** API calls จะถูก mock โดยอัตโนมัติเว้นแต่จะปิดการใช้งาน
5. **Accessibility:** WCAG tests จะรวมอยู่ตามค่าเริ่มต้น
6. **Visual Regression:** ต้องการ baseline images สำหรับการเปรียบเทียบ
7. **Parallel Execution:** การทดสอบถูกกำหนดค่าสำหรับการทำงานแบบขนานตามค่าเริ่มต้น
8. **การบำรุงรักษา:** อัปเดตการทดสอบเมื่อ UI spec เปลี่ยนแปลง

---

## Workflows ที่เกี่ยวข้อง

- [`/smartspec_generate_ui_spec`](./generate_ui_spec_th.md) - สร้าง UI specification
- [`/smartspec_generate_ui_implementation`](./generate_ui_implementation_th.md) - สร้างโค้ด UI
- [`/smartspec_ui_accessibility_audit`](./ui_accessibility_audit_th.md) - ตรวจสอบ accessibility
- [`/smartspec_test_suite_runner`](./test_suite_runner_th.md) - รัน test suite

---

**สำหรับข้อมูลเพิ่มเติม ดูที่ [เอกสาร A2UI](../../README-A2UI.md)**
