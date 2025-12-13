# /smartspec_observability_configurator คู่มือ (v6.0, ภาษาไทย)

## ภาพรวม

workflow `/smartspec_observability_configurator` (v6.1.1) ถูกออกแบบมาเพื่อสร้างชุดการกำหนดค่าการสังเกตการณ์แบบครบถ้วนและดีที่สุดตามสเปคของโปรเจกต์ (`spec.md`) และข้อกำหนดที่ไม่ใช่ฟังก์ชัน (NFRs)

**วัตถุประสงค์:** เพื่อสร้างไฟล์การกำหนดค่าสำหรับเมตริก (Prometheus/Otel), การบันทึกล็อก, การติดตาม (Otel), การแจ้งเตือน, ตัวตรวจสอบ SLO/SLA และแดชบอร์ด โดยให้สอดคล้องกับสเปคของโปรเจกต์และมาตรฐานความปลอดภัย

**คุณสมบัติหลัก:**

1.  **Preview-First:** โดยค่าเริ่มต้น workflow จะสร้างเฉพาะรายงานและตัวอย่างงานพรีวิว (`bundle.preview/`)
2.  **Governed Writes:** การเขียนการกำหนดค่าจริงไปยังไดเรกทอรี runtime ต้องใช้ flags เฉพาะ (`--apply` และ `--write-runtime-config`) พร้อมการตรวจสอบเส้นทางอย่างเข้มงวด
3.  **Security Hardened:** มีการเสริมความปลอดภัยบังคับป้องกัน path traversal, การรั่วไหลของความลับ และรับประกันการเขียนแบบอะตอมมิก
4.  **Platform Agnostic:** รองรับแพลตฟอร์มการสังเกตการณ์หลัก ๆ (OpenTelemetry, Prometheus, Datadog)

**หมายเหตุเวอร์ชัน (v6.1.1):** เวอร์ชันนี้แก้ไขปัญหาการชนกันของ flags, นำการเสริมความปลอดภัย v6 มาใช้ (การทำ path normalization, ความปลอดภัยของ root output, การเขียนแบบอะตอมมิก), แนะนำ Change Plan artifacts และแทนที่การพรีวิวแบบเต็มเนื้อหาด้วย diffs/excerpts+hashes เพื่อความปลอดภัย

## การใช้งาน

### การใช้งาน CLI

workflow นี้ถูกเรียกใช้งานผ่าน SmartSpec Command Line Interface (CLI)

**ไวยากรณ์:**

```bash
/smartspec_observability_configurator [FLAGS]
```

#### ตัวอย่าง: การพรีวิวการกำหนดค่า

เพื่อสร้างชุดการกำหนดค่าการสังเกตการณ์สำหรับสเปค โดยกำหนดเป้าหมายเป็น OpenTelemetry โดยไม่ทำการเปลี่ยนแปลงใด ๆ:

```bash
/smartspec_observability_configurator \
  --spec specs/api-gateway/v2/spec.md \
  --obs-platform opentelemetry \
  --out .spec/reports/obs-config-run-123 \
  --json
```

#### ตัวอย่าง: การนำการกำหนดค่าไปใช้ (Governed Write)

เพื่อเขียนไฟล์การกำหนดค่าที่สร้างขึ้นไปยังไดเรกทอรีเป้าหมายที่ได้รับอนุมัติ (`config/observability/`) ซึ่งจำเป็นสำหรับการนำไปใช้งาน:

```bash
/smartspec_observability_configurator \
  --spec specs/api-gateway/v2/spec.md \
  --obs-platform opentelemetry \
  --target-dir config/observability/ \
  --write-runtime-config \
  --apply \
  --out .spec/reports/obs-config-run-124
```

### การใช้งาน Kilo Code

workflow สามารถถูกเรียกใช้งานภายในไฟล์ SmartSpec Kilo Code (เช่นไฟล์ `.md` ที่ใช้สำหรับ orchestration)

**ไวยากรณ์:**

```markdown
/smartspec_observability_configurator.md
  [FLAGS]
  --kilocode
```

#### ตัวอย่าง: การเรียกใช้งาน Kilo Code (พรีวิว)

```bash
/smartspec_observability_configurator.md \
  --spec specs/inventory-service/spec.md \
  --obs-platform datadog \
  --max-items 50 \
  --out .spec/reports/inventory-obs-preview \
  --kilocode
```

## กรณีการใช้งาน

### กรณีการใช้งาน 1: การสร้างการสังเกตการณ์สำหรับไมโครเซอร์วิสใหม่ (โหมดพรีวิว)

**สถานการณ์:** กำลังพัฒนาไมโครเซอร์วิส `payment-processor` ใหม่ ทีมต้องการสร้างการกำหนดค่าเมตริก Prometheus, แนวทางการบันทึกล็อกมาตรฐาน และแดชบอร์ดเริ่มต้นตาม `spec.md` ของบริการก่อนนำไปใช้งานจริง

**เป้าหมาย:** สร้างชุดพรีวิวเต็มรูปแบบและแผนการเปลี่ยนแปลงโดยไม่เขียนไฟล์ใด ๆ ลงในไดเรกทอรีการกำหนดค่า runtime

**คำสั่ง (CLI):**

```bash
/smartspec_observability_configurator \
  --spec services/payment-processor/spec.md \
  --obs-platform prometheus \
  --nfr-summary .spec/reports/nfr-perf-verifier/run-001/summary.json \
  --out .spec/reports/payment-processor-obs-preview
```

**ผลลัพธ์ที่คาดหวัง:**

*   รหัสออก `0`
*   ไดเรกทอรีใหม่ `.spec/reports/payment-processor-obs-preview/` ที่ประกอบด้วย:
    *   `report.md` รายละเอียดส่วนประกอบที่สร้างขึ้น
    *   `change_plan.md` แสดงไฟล์ที่เสนอให้เปลี่ยนแปลง (เช่น ชิ้นส่วน `prometheus.yml`, JSON ของแดชบอร์ด)
    *   `bundle.preview/` ที่เก็บไฟล์การกำหนดค่าที่สร้างขึ้นทั้งหมด
    *   **สำคัญ:** ไม่มีไฟล์ใดถูกเขียนนอกไดเรกทอรีรายงาน

### กรณีการใช้งาน 2: การนำการกำหนดค่าแจ้งเตือนด้วยเทมเพลตที่กำหนดเองไปใช้

**สถานการณ์:** ทีมความปลอดภัยต้องการให้บริการทั้งหมดใช้ชุดการแจ้งเตือนวิกฤตที่กำหนดมาตรฐานในเทมเพลต JSON ที่กำหนดเอง (`security_alerts.json`) การกำหนดค่าที่สร้างขึ้นต้องถูกเขียนไปยังไดเรกทอรีเป้าหมายที่ได้รับอนุมัติ (`config/monitoring/`)

**เป้าหมาย:** สร้างการกำหนดค่า, รวมเทมเพลตแจ้งเตือนที่กำหนดเอง (ซึ่งต้องผ่านการทำความสะอาดข้อมูล) และนำการเปลี่ยนแปลงไปใช้กับการกำหนดค่า runtime

**คำสั่ง (Kilo Code):**

```bash
/smartspec_observability_configurator.md \
  --spec specs/critical-service/spec.md \
  --obs-platform auto \
  --alert-template templates/security_alerts.json \
  --target-dir config/monitoring/ \
  --write-runtime-config \
  --apply \
  --kilocode
```

**ผลลัพธ์ที่คาดหวัง:**

*   workflow ดำเนินการตรวจสอบบังคับ (OBS-103 Template Sanitized)
*   รหัสออก `0`
*   ไฟล์การกำหนดค่าที่สร้างขึ้น (รวมถึงการแจ้งเตือนมาตรฐานที่ได้จากเทมเพลต) ถูกเขียนแบบอะตอมมิกภายใต้ `config/monitoring/`
*   `change_plan.md` ยืนยันไฟล์ที่เขียนไปยังตำแหน่งที่ควบคุม

### กรณีการใช้งาน 3: การตรวจสอบโหมดเข้มงวด

**สถานการณ์:** นักพัฒนาพยายามรัน workflow แต่ระบุเส้นทางไดเรกทอรีเป้าหมายไม่ถูกต้อง ทำให้ผิดสัญญาการกำกับดูแล (`target-dir` ไม่อยู่ใน allowlist)

**เป้าหมาย:** workflow ต้องล้มเหลวทันทีโดยไม่เริ่มสร้างหรือเขียนไฟล์ใด ๆ

**คำสั่ง (CLI):**

```bash
/smartspec_observability_configurator \
  --spec specs/my-service/spec.md \
  --obs-platform opentelemetry \
  --target-dir /tmp/unapproved-location/ \
  --write-runtime-config \
  --apply \
  --mode strict
```

**ผลลัพธ์ที่คาดหวัง:**

*   workflow ล้มเหลวทันทีในส่วนที่ 4.3 (Governed target-dir rules)
*   รหัสออก `2` (ข้อผิดพลาดการใช้งาน/การกำหนดค่า)
*   ข้อความแสดงข้อผิดพลาดแจ้งว่า `--target-dir` ที่ระบุไม่ผ่านการตรวจสอบตามสัญญาการกำกับดูแล

## พารามิเตอร์

พารามิเตอร์ (flags) ที่รองรับโดย workflow `/smartspec_observability_configurator` มีดังนี้:

| Flag | Category | Description | Required/Default |
| :--- | :--- | :--- | :--- |
| `--spec <path>` | Workflow | เส้นทางไปยังไฟล์ `spec.md` หรือโฟลเดอร์สเปคที่ใช้เป็นบริบทอินพุต | แนะนำ |
| `--nfr-summary <path>` | Workflow | เส้นทางทางเลือกไปยังสรุปหลักฐานประสิทธิภาพ/NFR (เช่น จาก `nfr-perf-verifier`) | ตัวเลือก |
| **`--obs-platform <platform>`** | Workflow | แพลตฟอร์มการสังเกตการณ์เป้าหมาย | ค่าเริ่มต้น: `auto` |
| `--target-dir <path>` | Workflow | ไดเรกทอรีเป้าหมายสำหรับการเขียนการกำหนดค่า runtime ที่ควบคุม | จำเป็นเมื่อใช้ `--apply` |
| **`--write-runtime-config`** | Workflow | **เปิดใช้งาน** การเขียนที่ควบคุมไปยัง `--target-dir` ต้องใช้ร่วมกับ `--apply` | ตัวเลือก (Gate) |
| `--dashboard-template <path>` | Workflow | เทมเพลตอินพุตทางเลือก (JSON/YAML) สำหรับการสร้างแดชบอร์ด | ตัวเลือก |
| `--alert-template <path>` | Workflow | เทมเพลตอินพุตทางเลือก (JSON/YAML) สำหรับการแจ้งเตือน/ตัวตรวจสอบ | ตัวเลือก |
| `--mode <normal|strict>` | Workflow | กำหนดโหมดการทำงาน `--strict` บังคับใช้การตรวจสอบเข้มงวด | ค่าเริ่มต้น: `normal` |
| `--max-items <int>` | Workflow | จำกัดจำนวนแดชบอร์ดหรือการแจ้งเตือนที่สร้าง | ตัวเลือก |
| `--config <path>` | Universal | เส้นทางไปยังไฟล์การกำหนดค่า SmartSpec | ตัวเลือก |
| `--lang <th|en>` | Universal | ภาษาของรายงานที่ส่งออก | ตัวเลือก |
| `--platform <cli|kilo|ci|other>` | Universal | โหมด runtime (สงวนไว้สำหรับการตรวจจับ runtime ภายใน) | ตัวเลือก |
| **`--apply`** | Universal | เปิดใช้งานการเขียนที่ควบคุม (workflow นี้ต้องใช้ร่วมกับ `--write-runtime-config`) | ตัวเลือก (Gate) |
| `--out <path>` | Universal | รากฐาน output สำหรับรายงานและพรีวิว ต้องปลอดภัย | ตัวเลือก |
| `--json` | Universal | ส่งออกรายงานและสรุปในรูปแบบ JSON | ตัวเลือก |
| `--quiet` | Universal | ปิดการแสดงผลที่ไม่จำเป็น | ตัวเลือก |

## ผลลัพธ์

workflow สร้างผลลัพธ์หลักสองประเภท คือ รายงาน/พรีวิวที่ปลอดภัย และไฟล์การกำหนดค่า runtime ที่ควบคุม

### ผลงาน Output ที่ปลอดภัย (เขียนเสมอ)

ไฟล์เหล่านี้ถูกเขียนไปยังโฟลเดอร์รันเฉพาะภายใต้เส้นทางที่ระบุโดย `--out` (ค่าเริ่มต้น: `.spec/reports/observability-configurator/<run-id>/`)

| Artifact | Description |
| :--- | :--- |
| `report.md` | รายงานรายละเอียดการสร้างและส่วนประกอบที่สร้างขึ้น |