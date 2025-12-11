# คู่มือ SmartSpec Workflow
## `/smartspec_reindex_workflows`
### รุ่น 1.0.0 — ฉบับภาษาไทย

---

# 1. ภาพรวม (Overview)
`/smartspec_reindex_workflows` คือ Workflow อย่างเป็นทางการของ SmartSpec ที่ทำหน้าที่สร้างและอัปเดตไฟล์ **WORKFLOW_INDEX.json** ซึ่งเป็น “สารบัญกลางของ Workflow ทั้งหมด” ที่มีอยู่ในโปรเจกต์ (รองรับทั้ง single-repo และ multi-repo)

Workflow นี้ทำหน้าที่คล้ายกับ `/smartspec_reindex_specs` ที่สร้าง SPEC_INDEX.json
แต่ใช้กับ **Workflow** แทน **SPEC**

สิ่งที่ workflow นี้ทำ:
- ค้นหาไฟล์สเปก workflow ทั้งหมดใน `.smartspec/workflows/`
- อ่าน metadata ด้าน governance ของแต่ละ workflow
  - role, category, write_guard
  - version, status
  - CLI flags
  - dependencies/produces
- รวมข้อมูลเป็น index เดียวในรูปแบบมาตรฐาน
- เขียนรายงานแบบ markdown และ JSON
- ทำงานร่วมกับ multi-repo ได้

---
# 2. วัตถุประสงค์หลัก
Workflow นี้ถูกออกแบบมาเพื่อ:

- สร้าง “แผนที่รวมของ Workflow ทั้งหมด” ในระบบ SmartSpec
- ให้ SmartSpec UI, Project Copilot และ IDE integrations ใช้อ้างอิง
- รักษามาตรฐาน governance ให้ workflow ทุกตัวมีข้อมูลครบถ้วน
- รองรับ automation ขั้นสูง เช่น:
  - การตรวจสอบ workflow (`/smartspec_validate_workflows` ในอนาคต)
  - ระบบแนะนำ workflow ให้อัตโนมัติ
  - Workflow discovery

---
# 3. ตำแหน่งใน Ecosystem ของ SmartSpec
```
.smartspec/workflows/*.md
          │
          ▼
/smartspec_reindex_workflows
          │
          ▼
.smartspec/WORKFLOW_INDEX.json
          │
          ▼
ใช้โดย:
- /smartspec_project_copilot
- SmartSpec UI และ IDE
- ระบบอัตโนมัติ (CI/CD)
```

Workflow นี้ **จะไม่แก้ไขไฟล์สเปกหรือโค้ดใด ๆ**
จะเขียนเฉพาะ:
- `.smartspec/WORKFLOW_INDEX.json`
- ไฟล์รายงานใน `.spec/reports/reindex-workflows/`

---
# 4. หน้าที่ของ Workflow
`/smartspec_reindex_workflows` ต้องดำเนินการดังนี้:

1. ค้นหาไฟล์ workflow spec ทั้งหมด
2. อ่าน metadata (id, version, write_guard, flags)
3. แปลงข้อมูลเป็น schema มาตรฐานใน index
4. รองรับ multi-repo path resolution
5. ตรวจจับปัญหา เช่น ไอดีชนกัน หรือข้อมูลขัดแย้ง
6. สร้างไฟล์ WORKFLOW_INDEX.json อย่างเป็นทางการ
7. เขียนรายงานชี้สถานะและปัญหาที่พบ

---
# 5. แหล่งข้อมูลที่ Workflow ใช้
Workflow นี้จะอ่านข้อมูลจาก:
- `.smartspec/workflows/` (ค่าเริ่มต้น)
- WORKFLOW_INDEX.json เดิม (ถ้ามี)
- `--workspace-roots`, `--repos-config` (เมื่อใช้ multi-repo)
- ไฟล์ governance หรือ evidence-config อื่น ๆ (แบบ read-only)

Workflow ไม่มีสิทธิ์แก้ไขไฟล์เหล่านี้โดยตรง (นอกจาก index และรายงาน)

---
# 6. สิ่งที่ Workflow สร้างออกมา (Outputs)
### 6.1 ไฟล์หลัก
```
.smartspec/WORKFLOW_INDEX.json
```

### 6.2 ไฟล์ Mirror (อาจเปิดใช้เพิ่ม)
```
WORKFLOW_INDEX.json (ที่ repo root)
```

### 6.3 ไฟล์รายงาน
```
.spec/reports/reindex-workflows/<timestamp>.md
.spec/reports/reindex-workflows/<timestamp>.json
```

---
# 7. ตัวอย่างการใช้งานคำสั่ง (CLI)
### ใช้งานแบบปกติ
```bash
/smartspec_reindex_workflows --report=summary
```

### กรณี multi-repo
```bash
/smartspec_reindex_workflows \
  --workspace-roots=.,../service-a,../service-b \
  --repos-config=.smartspec/repos-config.json \
  --report=detailed
```

### Dry-run (ไม่เขียนไฟล์จริง ใช้ตรวจสอบใน CI)
```bash
/smartspec_reindex_workflows --dry-run --report=detailed
```

---
# 8. รายละเอียด Flags

## 8.1 ส่วนของ Output
| Flag | ความหมาย |
|------|-----------|
| `--out=<path>` | ระบุตำแหน่งไฟล์ WORKFLOW_INDEX.json |
| `--mirror-root=<true|false>` | สร้างไฟล์ mirror ที่ repo root |

## 8.2 ส่วนของ Discovery
| Flag | ความหมาย |
|------|-----------|
| `--workflow-roots=<csv>` | ระบุโฟลเดอร์ workflow (ค่าเริ่มต้น `.smartspec/workflows`) |
| `--include-internal=<true|false>` | รวม workflow แบบ internal/experimental ด้วยหรือไม่ |

## 8.3 Multi-Repo
| Flag | ความหมาย |
|------|-----------|
| `--workspace-roots=<csv>` | ระบุ root หลาย repo |
| `--repos-config=<path>` | ไฟล์ graph ของ multi-repo |

## 8.4 ความปลอดภัยและรูปแบบ Output
| Flag | ความหมาย |
|------|-----------|
| `--report=<summary|detailed>` | เลือกระดับรายละเอียดของรายงาน |
| `--dry-run` | สร้าง index ในหน่วยความจำ (ไม่เขียนไฟล์จริง) |
| `--safety-mode=<strict|dev>` | strict = เจอ conflict จะหยุดการเขียนไฟล์ |
| `--strict` | alias ของ strict mode |

## 8.5 การกรองข้อมูล
| Flag | ใช้ทำอะไร |
|------|-----------|
| `--include-status=<csv>` | include เฉพาะ workflow ที่มี status ตามที่กำหนด |
| `--exclude-status=<csv>` | exclude workflow ตาม status |
| `--include-platforms=<csv>` | include เฉพาะ workflow ที่รองรับ platform เหล่านี้ |

---
# 9. โครงสร้าง Metadata ของ Workflow ใน Index
ข้อมูล 1 รายการของ workflow จะประกอบด้วย:

- `id`
- `name` (CLI name)
- `version`
- `role` เช่น `support/implement`, `verify/strict`
- `category` เช่น `verification`, `index`, `ui`, `support`
- `status` เช่น `stable`, `beta`, `deprecated`
- `description`
- `write_guard`
- `source_file`
- `supported_platforms[]`
- `cli.required_flags[]`
- `cli.optional_flags[]`
- `tags[]`
- `depends_on[]`
- `produces[]`
- `last_updated`

---
# 10. การตรวจจับปัญหา (Conflict Detection)
Workflow นี้ต้องตรวจจับ:
- workflow ID ซ้ำกัน
- write_guard ขัดแย้งกัน
- CLI name ซ้ำกัน
- workflow spec ไม่สมบูรณ์หรือหายไป

ใน strict mode → ปัญหาเหล่านี้จะ “บล็อกการเขียน index ใหม่”
ใน dev mode → จะอนุญาตให้สร้าง index ได้ แต่บันทึกคำเตือนในรายงาน

---
# 11. การรองรับ Workspace ใหญ่หรือ Multi-Repo
Workflow รองรับ workspace ขนาดใหญ่ได้โดย:
- ใช้การสแกนแบบไหล (streaming)
- เขียนไฟล์แบบ atomic (ปลอดภัยจากการ commit ครึ่ง ๆ กลาง ๆ)
- เตือนเมื่อพบ path หรือ repo config ไม่สอดคล้องกัน

---
# 12. การนำ Index ไปใช้
### 12.1 `/smartspec_project_copilot`
ใช้เพื่อ:
- แสดงรายการ workflow
- แนะนำ workflow ถัดไปที่เหมาะสม
- สร้าง CLI ตัวอย่างให้ผู้ใช้

### 12.2 SmartSpec UI / IDE
- แสดงรายการ workflow
- กรองตาม role/category/platform
- ช่วยสร้างคำสั่งให้ผู้ใช้

### 12.3 ระบบอัตโนมัติ (CI/CD)
ใช้ตรวจสอบ:
- ว่า workflow spec ครบหรือไม่
- ว่ามี workflow deprecated หรือ conflict หรือไม่

---
# 13. การจัดการ Error
Workflow ต้อง:
- เตือนเมื่อหา workflow root ไม่พบ
- เตือนเมื่อ metadata ไม่ครบ
- เตือน workflow ที่มีฟิลด์ขัดแย้งกัน
- สร้างรายงานเพื่อแก้ไข

ใน strict mode → error รุนแรงจะหยุดการเขียนไฟล์

---
# 14. แนวทางปฏิบัติที่ดี
- เก็บ workflow spec ไว้ใน `.smartspec/workflows/` เท่านั้น
- รัน workflow นี้ทุกครั้งที่มีการเพิ่ม/ลบ/แก้ workflow spec
- ใช้ `--dry-run` ใน CI เพื่อป้องกันปัญหา workflow governance
- ใช้ detailed report ระหว่างพัฒนา

---
# 15. สรุป
`/smartspec_reindex_workflows` เป็น workflow ระดับ governance ที่ใช้สร้าง **WORKFLOW_INDEX.json** ซึ่งเป็นฐานข้อมูลสำคัญของระบบ SmartSpec สำหรับ:
- การค้นหา workflow
- การแนะนำ workflow ให้ผู้ใช้
- การทำงานร่วมกับ IDE และ UI
- การตรวจสอบ governance ของ workflow

Workflow นี้ช่วยให้ SmartSpec มีความเป็นระบบมากขึ้น และพร้อมรองรับ automation ขั้นสูงในอนาคต

---
**End of Manual**