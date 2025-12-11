# คู่มือ SmartSpec Workflow
## `/smartspec_report_implement_prompter`
### รุ่น 1.0.2 — ฉบับภาษาไทย

---

## 1. ภาพรวม (Overview)
`/smartspec_report_implement_prompter` คือ Workflow ประเภท Utility ใน SmartSpec ที่ออกแบบมาเพื่อ **แปลง Strict Verification Report ให้เป็นชุดพรอมต์** สำหรับส่งให้ AI Coding Assistant (เช่น Kilo Code, Claude Code, Google Antigravity) ช่วยเขียนโค้ดแก้ไขงานที่ยังไม่สมบูรณ์ให้ตรงจุดที่สุด

โดย Workflow นี้จะอ่าน:
- ไฟล์ **strict report (.json)** จาก `/smartspec_verify_tasks_progress_strict`
- ไฟล์ **spec.md** ของฟีเจอร์
- ไฟล์ **tasks.md** ของฟีเจอร์

และผลลัพธ์คือ:
- ไฟล์ **README สรุปงานที่ยังต้องแก้ตาม strict verifier**
- ไฟล์พรอมต์สำหรับแต่ละโดเมน เช่น:
  - API
  - Tests
  - Documentation
  - Deployment

ซึ่งสามารถคัดลอกไปใช้กับ AI Coding Assistant โดยตรงได้ทันที

---

## 2. ความสามารถหลัก (Key Features)
### ✔ อ่าน strict report ได้ครบถ้วน
รองรับ verdict, evidence, phase, critical task, cluster

### ✔ สร้างพรอมต์ที่พร้อมใช้งาน
เป็นไฟล์ markdown เนื้อหาชัดเจน บอกให้ Kilo Code ทำงานเป็นขั้นตอน

### ✔ จัดกลุ่มงานอัตโนมัติ (Domain Clustering)
- API
- Tests
- Docs
- Deploy

### ✔ แยกงานง่าย-ยาก
- ถ้าเป็นงานง่าย → แนะนำใช้ `/smartspec_implement_tasks`
- ถ้าเป็นงานซับซ้อน → สร้างพรอมต์ละเอียดให้เลย

### ✔ รองรับ multi-repo
รวมถึง flags: `--workspace-roots`, `--repos-config`

### ✔ ตรวจจับเทคโนโลยีอัตโนมัติ
Fastify, NestJS, Spring Boot, FastAPI, Go ฯลฯ

### ✔ รองรับ output ทั้ง Markdown / JSON
ดีสำหรับ UI และ IDE

### ✔ มี Metadata กำกับเพื่อใช้ Audit
เช่น Prompt ID, timestamp, report version

---

## 3. วิธีใช้งานโดยย่อ (Typical Workflow)

### ขั้นตอนที่ 1 — รัน Strict Verification
```bash
/smartspec_verify_tasks_progress_strict \
  --spec specs/feature/<spec-id>/spec.md \
  --report-format=json \
  --report .spec/reports/verify-tasks-progress/<spec-id>-verification-report.json
```

### ขั้นตอนที่ 2 — สร้างชุดพรอมต์
```bash
/smartspec_report_implement_prompter \
  --spec specs/feature/<spec-id>/spec.md \
  --tasks specs/feature/<spec-id>/tasks.md \
  --report .spec/reports/verify-tasks-progress/<spec-id>-verification-report.json \
  --output .smartspec/prompts/<spec-id>/
```

### ขั้นตอนที่ 3 — เปิดไฟล์พรอมต์ใน Kilo Code
ไฟล์ที่สร้างอาจมี:
- `api-implementation-prompt.md`
- `testing-prompt.md`
- `documentation-prompt.md`
- `deployment-prompt.md`

เพียงคัดลอกเนื้อหาไปวางใน AI Coding Assistant แล้วให้มันเริ่มเขียนโค้ดให้

### ขั้นตอนที่ 4 — รัน Strict Verification อีกครั้ง
```bash
/smartspec_verify_tasks_progress_strict --spec specs/feature/<spec-id>/spec.md
```

### ขั้นตอนที่ 5 — Sync Checkboxes
```bash
/smartspec_sync_tasks_checkboxes \
  --tasks specs/feature/<spec-id>/tasks.md \
  --report .spec/reports/verify-tasks-progress/<spec-id>-verification-report.json \
  --mode=auto
```

---

## 4. รายละเอียดคำสั่ง (CLI Reference)

```bash
/smartspec_report_implement_prompter \
  --spec <path/to/spec.md> \
  --tasks <path/to/tasks.md> \
  --report <path/to/strict-json-report> \
  [--output <directory>] \
  [--cluster api|tests|docs|deploy|all] \
  [--workspace-roots <paths>] \
  [--repos-config <path>] \
  [--evidence-config <path>] \
  [--language th|en] \
  [--dry-run] \
  [--format markdown|json] \
  [--max-tasks-per-prompt N] \
  [--max-chars-per-prompt N]
```

### ค่า Mandatory
| Flag | ความหมาย |
|------|-----------|
| `--spec` | ไฟล์ SPEC ของฟีเจอร์ |
| `--tasks` | ไฟล์ TASKS ของฟีเจอร์ |
| `--report` | strict JSON report จาก strict verifier |

### ค่า Optional
| Flag | ใช้ทำอะไร |
|------|------------|
| `--output` | โฟลเดอร์ปลายทางสำหรับไฟล์ prompt |
| `--cluster` | Gen เฉพาะโดเมนที่ต้องการ |
| `--workspace-roots`, `--repos-config` | ใช้กับ multi-repo |
| `--evidence-config` | Override evidence rules |
| `--language` | ตั้งภาษา output |
| `--dry-run` | แสดงผลลัพธ์จำลองโดยไม่เขียนไฟล์ |
| `--format` | เลือก output เป็น Markdown หรือ JSON |
| `--max-tasks-per-prompt` | จำกัดจำนวน task ต่อไฟล์ |
| `--max-chars-per-prompt` | จำกัดความยาวไฟล์ |

---

## 5. โครงสร้างไฟล์ Output (Prompt Structure)
เมื่อใช้ `--output` จะได้โฟลเดอร์เช่น:
```
.smartspec/prompts/<spec-id>/
  ├── README.md
  ├── api-implementation-prompt.md
  ├── testing-prompt.md
  ├── documentation-prompt.md
  ├── deployment-prompt.md
```

ถ้ามีงานจำนวนมาก อาจถูก split อัตโนมัติ:
```
  testing-prompt-1.md
  testing-prompt-2.md
```

ถ้าไม่มีงานต้องทำ:
```
  README.md (สรุปว่าไม่มี task ค้าง)
```

---

## 6. การจัดประเภทของงาน (Task Classification)
ระบบจะจัดงานออกเป็น 3 ประเภท:

### ✔ `unsynced_only`
งานเสร็จแล้ว แค่ checkbox ไม่ตรง → ใช้ `/smartspec_sync_tasks_checkboxes`

### ✔ `simple_not_started`
งานง่าย ยังไม่เริ่ม ไม่ critical → ใช้ `/smartspec_implement_tasks`

### ✔ `complex_cluster`
งานซับซ้อน / critical → **สร้างพรอมต์ให้** เช่น API, tests, docs, deploy

---

## 7. Domain Cluster
แต่ละงานจะถูกจัดไปอยู่ในหนึ่งในกลุ่มต่อไปนี้:

| Cluster | ความหมาย |
|---------|-----------|
| **api** | route/endpoint/controller เป็นต้น |
| **tests** | unit/integration/performance tests |
| **docs** | OpenAPI, Swagger, technical docs |
| **deploy** | K8s, manifests, monitoring, CI/CD |

ผู้ใช้สามารถ override mapping ได้โดยสร้างไฟล์:
```
.smartspec/prompts/cluster-overrides.json
```

---

## 8. ระบบเลือกภาษา (Locale Handling)
ลำดับความสำคัญ:
1. ค่า `--language`
2. Header ใน spec.md
3. ตรวจภาษาจาก spec/tasks (>20% เป็นไทย → ใช้ไทย)
4. Platform (เช่น Kilo Code → ค่าเริ่มต้นเป็นไทย)
5. Fallback → อังกฤษ

---

## 9. ตรวจจับเทคโนโลยี (Tech Stack Detection)
Workflow จะตรวจจากไฟล์โปรเจกต์ เช่น:
- Fastify → พบใน `package.json`
- NestJS → พบ `@nestjs/common`
- Spring Boot → พบ `src/main/java`
- FastAPI → พบ `fastapi.FastAPI`
- Go → พบ routing library ตาม `go.mod`

แล้วจะปรับข้อความในพรอมต์ให้เข้ากับ stack นั้นโดยอัตโนมัติ

---

## 10. Metadata ของพรอมต์ (Prompt Metadata)
ทุกไฟล์พรอมต์จะมีข้อมูลกำกับ เช่น:
```
<!--
Prompt-Generation-ID: <uuid>
Spec-ID: <spec-id>
Report-Version: <strict-report-version>
Generated-At: <timestamp>
-->
```
ช่วยเรื่อง traceability

---

## 11. ตัวอย่างพรอมต์ (Example)
```markdown
# API Implementation Prompt — Phone Verification (T047–T048)

## บริบท
Spec: specs/feature/spec-002-user-management/spec.md
Tasks: specs/feature/spec-002-user-management/tasks.md
Report: .spec/reports/verify-tasks-progress/spec-002-user-management-verification-report.json
Tech Stack: Fastify + Prisma

## สรุปปัญหา
- ขาด endpoint: POST /auth/phone/send-otp
- ขาด endpoint: POST /auth/phone/verify-otp
- Service มีอยู่แล้ว แต่ route ยังไม่เชื่อม

## สิ่งที่ต้องให้ Kilo Code ทำ
1. เปิดดูโครงสร้าง route ใน `src/routes/`
2. เพิ่ม 2 endpoint ลงใน `users.routes.ts`
3. เรียกใช้งาน phoneVerificationService
4. อัปเดต model ของ user ว่า verified แล้ว
5. เพิ่ม integration test แบบง่าย

## หลังจากทำเสร็จ
- รัน test
- รัน strict verifier อีกครั้ง
```

---

## 12. Error Handling
Workflow จัดการสิ่งต่อไปนี้:
- ไม่มีไฟล์ report
- เวอร์ชัน report สูงเกินที่รองรับ
- task ไม่ตรงกับ tasks.md
- ไม่พบ acceptance criteria
- cluster ไม่มีงานต้องทำ

ระบบจะแสดงคำเตือนพร้อมคำแนะนำแก้ไข

---

## 13. กรณีแนะนำ (Use Cases)
### ใช้เมื่อ:
- strict verifier แจ้ง incomplete จำนวนมาก
- งานซับซ้อน แก้ยาก
- มีหลายโดเมนต้องแก้พร้อมกัน

### ไม่จำเป็นเมื่อ:
- งานครบหมดแล้ว
- เหลือแค่ sync checkbox

---

## 14. บทสรุป
`/smartspec

