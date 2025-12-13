# /smartspec_ci_quality_gate คู่มือ (v6.0, ภาษาไทย)

## ภาพรวม

workflow `/smartspec_quality_gate` (เวอร์ชัน 6.0.0) เป็น quality gate ที่รวมและพร้อมใช้งานในสภาพแวดล้อมการผลิต เพื่อทดแทน workflow รุ่นเก่า: `smartspec_ci_quality_gate` และ `smartspec_release_readiness`

**วัตถุประสงค์:** เพื่อทำการตรวจสอบคุณภาพอย่างครบถ้วนตามสัญญาการกำกับดูแล SmartSpec, การตั้งค่า และ artifacts ต่างๆ โดยเป็น workflow แบบอ่านอย่างเดียวที่สร้าง **รายงานเท่านั้น** ทำให้ปลอดภัยที่จะรันในสภาพแวดล้อม Continuous Integration (CI) หรือรันแบบ local

**คุณสมบัติหลัก:**

*   **Profiles:** รองรับโหมดหลักสองแบบ คือ `ci` (ตรวจสอบเร็วในช่วงต้น) และ `release` (ตรวจสอบลึกเน้นความพร้อมสำหรับการปล่อย)
*   **ความปลอดภัย:** บังคับใช้ขอบเขตการเขียนอย่างเข้มงวด, ปฏิเสธการเชื่อมต่อเครือข่าย และปกปิดความลับ เพื่อให้สอดคล้องกับ threat model ของ SmartSpec
*   **การกำหนดขอบเขต:** สามารถรันแบบทั่วทั้ง repository (global) หรือกำหนดขอบเขตเฉพาะสเปคเดียว (`--spec` หรือ `--spec-id`)

## การใช้งาน

### การใช้งาน CLI

workflow นี้เรียกใช้งานโดยตรงผ่าน command line interface

```bash
/smartspec_quality_gate \
  --profile <ci|release> \
  [--spec <path/to/spec.md>|--spec-id <id>] \
  [--out <output-root>] \
  [--json] \
  [--strict]
```

### การใช้งาน Kilo Code

เมื่อผนวก workflow นี้เข้ากับ workflow SmartSpec อื่น ๆ หรือ pipeline ของ Kilo Code ให้ใช้สกุล `.md` ในการเรียกใช้งาน:

```bash
/smartspec_quality_gate.md \
  --profile <ci|release> \
  [--spec <path/to/spec.md>|--spec-id <id>] \
  [--out <output-root>] \
  [--json] \
  [--strict]
```

## กรณีการใช้งาน

### กรณีการใช้งาน 1: ตรวจสอบคุณภาพ CI แบบเร็ว (CLI)

**สถานการณ์:** นักพัฒนาต้องการรันการตรวจสอบคุณภาพอย่างรวดเร็วบนสเปคที่สร้างใหม่ (`specs/feature/new_api.md`) ก่อนรวมสาขา โดยเน้นความเร็วและความสมเหตุสมผลของการตั้งค่า

**คำสั่ง:**

```bash
/smartspec_quality_gate \
  --profile ci \
  --spec specs/feature/new_api.md \
  --strict \
  --json
```

**ผลลัพธ์ที่คาดหวัง:**

1.  รายงานถูกสร้างไว้ที่ `.spec/reports/quality-gate/ci/<run-id>/` (เช่น `report.md`)
2.  สรุปแบบ machine-readable ถูกสร้างที่ `summary.json` ในโฟลเดอร์รัน
3.  workflow ตรวจสอบความสมเหตุสมผลของการตั้งค่า (เช่น `network_policy.default=deny`)
4.  หากมีข้อกำหนด MUST ใด ๆ ล้มเหลว (เช่น ขาดการตรวจสอบ evidence discipline) exit code จะเป็น `1` (fail) เนื่องจากมี flag `--strict`

### กรณีการใช้งาน 2: ตรวจสอบความพร้อมสำหรับการปล่อย (Kilo Code)

**สถานการณ์:** pipeline การปล่อยต้องการตรวจสอบให้แน่ใจว่าทุกข้อกำกับดูแลและความปลอดภัยครบถ้วนสำหรับ repository ทั้งหมดก่อนการ deploy

**โค้ด Kilo Code:**

```kilo
# รันโปรไฟล์ release แบบทั่วทั้ง repo
run: /smartspec_quality_gate.md
  --profile release
  --out ./release_audit_results
  --strict
```

**ผลลัพธ์ที่คาดหวัง:**

1.  workflow รันแบบ global ตรวจสอบทุกสเปคและ artifacts การกำกับดูแล
2.  รายงานผลลัพธ์ถูกเขียนที่ `./release_audit_results/release/<run-id>/...`
3.  workflow ทำการตรวจสอบเชิงลึก รวมถึงตรวจสอบว่ามีรายงาน Security Evidence Audit และแผน NFR/Perf สำหรับฟีเจอร์ที่เกี่ยวข้อง
4.  หากตรวจสอบไม่ผ่าน `report.md` จะมีคำแนะนำขั้นตอนถัดไป เช่น การรัน `/smartspec_security_evidence_audit`

### กรณีการใช้งาน 3: ตรวจสอบทั่วไปแบบไม่เข้มงวด พร้อมผลลัพธ์กำหนดเอง (CLI)

**สถานการณ์:** ผู้ใช้ต้องการตรวจสอบสุขภาพทั่วไปของ repository โดยอนุญาตให้มีคำเตือน แต่ต้องการเก็บผลลัพธ์ในไดเรกทอรีชั่วคราวเฉพาะ

**คำสั่ง:**

```bash
/smartspec_quality_gate \
  --profile ci \
  --out /tmp/qg_scan_results
```

**ผลลัพธ์ที่คาดหวัง:**

1.  workflow รันแบบ global (ไม่มี `--spec` หรือ `--spec-id`)
2.  รายงานผลลัพธ์ถูกเขียนที่ `/tmp/qg_scan_results/ci/<run-id>/...`
3.  workflow จะ exit ด้วย code `0` (ผ่าน) แม้ว่าการตรวจสอบ SHOULD ล้มเหลว ตราบใดที่ไม่มีการล้มเหลวใน MUST เพราะไม่ได้ระบุ `--strict`

## พารามิเตอร์

workflow `/smartspec_quality_gate` รองรับทั้ง universal flags และ workflow-specific flags

| Flag | Category | Required | Description |
| :--- | :--- | :--- | :--- |
| `--profile <ci|release>` | Workflow-Specific | ใช่ | กำหนดชุดของการตรวจสอบที่จะรัน `ci` คือเร็ว, `release` คือครบถ้วน |
| `--spec <path>` | Workflow-Specific | ไม่ใช่ | กำหนดขอบเขตการตรวจสอบคุณภาพเป็นไฟล์สเปคเดียว (เช่น `specs/feature/api.md`) |
| `--spec-id <id>` | Workflow-Specific | ไม่ใช่ | กำหนดขอบเขตการตรวจสอบโดยใช้ specification ID (แก้ไขผ่าน `.spec/SPEC_INDEX.json`) |
| `--strict` | Workflow-Specific | ไม่ใช่ | หากระบุ workflow จะล้มเหลวเมื่อมีข้อกำหนด MUST ใด ๆ ไม่ผ่าน (exit code 1) |
| `--config <path>` | Universal | ไม่ใช่ | เส้นทางไปยังไฟล์การตั้งค่า SmartSpec (ค่าเริ่มต้น: `.spec/smartspec.config.yaml`) |
| `--lang <th|en>` | Universal | ไม่ใช่ | ภาษาสำหรับการสร้างรายงาน |
| `--platform <cli|kilo|ci|other>` | Universal | ไม่ใช่ | ตัวระบุแพลตฟอร์มตามบริบท |
| `--apply` | Universal | ไม่ใช่ | รับไว้เพื่อความเข้ากันได้กับสัญญา แต่ **ถูกละเลย** (ไม่มีผลต่อขอบเขตการเขียน) |
| `--out <path>` | Universal | ไม่ใช่ | โฟลเดอร์ฐานสำหรับรายงานผลลัพธ์ |
| `--json` | Universal | ไม่ใช่ | สร้างไฟล์ `summary.json` แบบ machine-readable |
| `--quiet` | Universal | ไม่ใช่ | ปิดการแสดงผลที่ไม่สำคัญบนคอนโซล |

**หมายเหตุการตรวจสอบข้อมูลเข้า:**

*   หากระบุทั้ง `--spec` และ `--spec-id` จะเกิดความล้มเหลวแบบ hard failure (exit code 2)
*   เส้นทาง `--out` ต้องเป็นไดเรกทอรี, ต้อง resolve อยู่ภายใต้ allowlist ของ config และไม่สามารถหลุดออกนอกผ่าน symlink หรือ resolve ภายใต้ denylist path ได้

## ผลลัพธ์

workflow จะสร้างรายงานเท่านั้น โดยเขียนไว้ในโฟลเดอร์รันที่ไม่ซ้ำกัน (`<run-id>`) ภายใน output root ที่เลือก

### การเลือก output root

| Condition | Output Path Structure |
| :--- | :--- |
| กรณีระบุ `--out` | `<out>/<profile>/<run-id>/` |
| กรณีไม่ระบุ `--out` | `.spec/reports/quality-gate/<profile>/<run-id>/` |

### Artifacts

| Artifact | Description | Condition |
| :--- | :--- | :--- |
| `report.md` | รายงาน quality gate ที่อ่านโดยมนุษย์ รวมเหตุผล, สถานะ และคำแนะนำขั้นตอนถัดไป | สร้างเสมอ (ยกเว้นถูกบล็อกโดยความปลอดภัยการเขียน) |
| `summary.json` | สรุปแบบ machine-readable ของการรัน ตาม schema ที่กำหนด | สร้างเมื่อระบุ `--json` |
| `artifacts/*` | ไฟล์สนับสนุนเพิ่มเติม (เช่น ส่วนตัดตอน config ที่ถูกปกปิด) | ขึ้นอยู่กับการตรวจสอบเฉพาะ |

### Exit Codes

| Code | Status | Description |
| :--- | :--- | :--- |
| `0` | ผ่าน | ตรวจสอบผ่านทั้งหมด หรือมีเพียงคำเตือน (เมื่อไม่ใช้โหมด `--strict`) |
| `1` | ล้มเหลว | ข้อกำหนด MUST ล้มเหลว หรือ gate ล้มเหลวเพราะโหมด `--strict` |
| `2` | ข้อผิดพลาดการใช้งาน | flag ไม่ถูกต้อง, path ไม่ถูกต้อง หรือข้อผิดพลาด config (เช่น ไฟล์ registry หาย) |

## หมายเหตุ & Workflow ที่เกี่ยวข้อง

### พฤติกรรมของ universal flag

flag สากล `--apply` รับไว้เพื่อความเข้ากันได้กับสัญญา แต่ **ไม่มีผล** กับ workflow นี้ เพราะเป็น workflow แบบอ่านอย่างเดียวและถูกควบคุมด้วยข้อจำกัดขอบเขตการเขียนอย่างเข้มงวด รายงานจะระบุว่า `--apply` ถูกละเลย

### การแมปการเลิกใช้

workflow นี้เป็นตัวแทนรวมสำหรับ workflow v5:

*   `smartspec_ci_quality_gate` ถูกแทนที่ด้วย `/smartspec_quality_gate --profile=ci`
*   `smartspec_release_readiness` ถูกแทนที่ด้วย `/smartspec_quality_gate --profile=release`

### ขั้นตอนถัดไปที่แนะนำ

`report.md` และ `summary.json` มักจะแนะนำให้รัน workflow SmartSpec อื่น ๆ เพื่อแก้ไขช่องว่างที่พบ เช่น:

*   `/smartspec_verify_tasks_progress_strict` (เมื่อกำหนดขอบเขตและมีงานที่ต้องติดตาม)
*   `/smartspec_security_evidence_audit` (สำหรับช่องว่างในโปรไฟล์ release)
*   `/smartspec_nfr_perf_planner` (เมื่อขาดหลักฐานด้านประสิทธิภาพ)

---
*อัปเดตล่าสุด: SmartSpec v6.0*