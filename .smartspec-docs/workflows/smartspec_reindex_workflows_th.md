# SmartSpec Workflow Manual  
## `/smartspec_reindex_workflows`  
### Version 1.0.0 — คู่มือ (TH)  

---  

# 1. ภาพรวม  
`/smartspec_reindex_workflows` คือ workflow อย่างเป็นทางการของ SmartSpec ที่รับผิดชอบในการสร้างและรีเฟรช **WORKFLOW_INDEX.json** ซึ่งเป็นดัชนีกลางของ workflow ทั้งหมดที่มีอยู่ใน repository หรือ workspace ที่มีหลาย repository  

workflow นี้เป็นคู่ขนานในระดับ workflow กับ `/smartspec_reindex_specs` (ซึ่งจัดการ SPEC_INDEX.json)  

workflow นี้:  
- ค้นหาไฟล์ workflow spec ภายใต้ `.smartspec/workflows/`  
- ดึงข้อมูล governance metadata (บทบาท, หมวดหมู่, write_guard, flags, เวอร์ชัน)  
- ทำ normalization และรวบรวมข้อมูลเหล่านี้เข้าเป็น `WORKFLOW_INDEX.json`  
- สร้างรายงานที่อ่านได้ทั้งโดยมนุษย์และเครื่อง  
- รองรับการแก้ไขปัญหาแบบ multi-repo และกฎ write-guard ที่ปลอดภัย  

---  
# 2. วัตถุประสงค์  
เป้าหมายหลักของ workflow นี้คือ:  

- ให้แผนที่ **แบบรวมศูนย์** ของ workflow SmartSpec ที่มีอยู่ทั้งหมด  
- อนุญาตให้ SmartSpec UI, Project Copilot และการผนวกรวม IDE สามารถระบุ workflow, ความสามารถ, flags ที่ต้องการ, หมวดหมู่ และการพึ่งพาได้  
- รักษาความสอดคล้องและ governance ในการกำหนด workflow  
- เปิดทางสำหรับเครื่องมือในอนาคต เช่น:  
  - การตรวจสอบ workflow (`/smartspec_validate_workflows`)  
  - อินเทอร์เฟซสำหรับค้นหา workflow  
  - pipeline อัตโนมัติ  

---  
# 3. ตำแหน่งของ Workflow ในระบบนิเวศ SmartSpec  
```
           +-------------------------+
           | .smartspec/workflows/*.md|
           +-------------+-----------+
                         |
                         v
        /smartspec_reindex_workflows
                         |
                         v
          +---------------------------+
          | WORKFLOW_INDEX.json       |
          +---------------------------+
                         |
                         v
      Recommended consumers:
      - /smartspec_project_copilot
      - SmartSpec UI / IDE integrations
      - Automation pipelines
```

workflow นี้จะไม่แก้ไข SPEC, TASKS, ซอร์สโค้ด, การทดสอบ หรือไฟล์ deployment ใดๆ  
จะเขียนเพียง:  
- `.smartspec/WORKFLOW_INDEX.json`  
- รายงานภายใต้ `.spec/reports/reindex-workflows/`  

---  
# 4. ความรับผิดชอบ  
`/smartspec_reindex_workflows` ต้อง:  

1. **ค้นหา** ไฟล์ workflow spec ทั้งหมด  
2. **แยกวิเคราะห์** metadata ของ workflow (id, version, role, write-guard, flags, dependencies)  
3. **ทำ normalization** metadata ให้อยู่ในรูปแบบมาตรฐาน  
4. **แก้ไขเส้นทาง** ในโหมด single-repo หรือ multi-repo  
5. **ตรวจจับความขัดแย้ง** เช่น workflow ID ซ้ำกัน  
6. **เขียนดัชนีมาตรฐาน** เป็น WORKFLOW_INDEX.json  
7. **สร้างรายงาน** สรุปปัญหาหรือความขัดแย้ง  

---  
# 5. แหล่งข้อมูลนำเข้า  
workflow รวบรวมข้อมูลจาก:  
- `.smartspec/workflows/` (root เริ่มต้น)  
- WORKFLOW_INDEX.json ที่มีอยู่แล้ว (ไม่บังคับ)  
- `--workspace-roots` และ `--repos-config` (สำหรับสภาพแวดล้อม multi-repo)  
- การกำหนด governance หรือ evidence แบบกำหนดเอง (อ่านอย่างเดียว)  

ข้อมูลนำเข้าทั้งหมดเป็น **อ่านอย่างเดียว** ยกเว้นไฟล์ดัชนีสุดท้ายและรายงาน  

---  
# 6. ผลลัพธ์  
### 6.1 ผลลัพธ์หลัก  
```
.smartspec/WORKFLOW_INDEX.json
```

### 6.2 ผลลัพธ์สำเนา (ถ้าเปิดใช้งาน)  
```
WORKFLOW_INDEX.json (repo root)
```

### 6.3 รายงาน  
```
.spec/reports/reindex-workflows/<timestamp>-report.md
.spec/reports/reindex-workflows/<timestamp>-report.json
```

---  
# 7. การใช้งาน CLI  
### การใช้งานพื้นฐาน  
```bash
/smartspec_reindex_workflows --report=summary
```

### ตัวอย่าง multi-repo  
```bash
/smartspec_reindex_workflows \
  --workspace-roots=.,../service-a,../service-b \
  --repos-config=.smartspec/repos-config.json \
  --report=detailed
```

### ตัวอย่าง dry-run  
```bash
/smartspec_reindex_workflows --dry-run --report=detailed
```

---  
# 8. อ้างอิง flags ของ CLI  

## 8.1 Output Flags  
| Flag | วัตถุประสงค์ |
|------|---------------|
| `--out=<path>` | กำหนดตำแหน่งผลลัพธ์ของ WORKFLOW_INDEX.json แบบกำหนดเอง |
| `--mirror-root=<true|false>` | เขียนไฟล์สำเนาเพิ่มเติมที่ root ของ repo |

## 8.2 Discovery Flags  
| Flag | วัตถุประสงค์ |
|------|---------------|
| `--workflow-roots=<csv>` | กำหนดโฟลเดอร์ workflow ใหม่ (ค่าเริ่มต้น: `.smartspec/workflows`) |
| `--include-internal=<true|false>` | รวม workflow ภายในหรือแบบทดลอง |

## 8.3 Multi-Repo Flags  
| Flag | วัตถุประสงค์ |
|------|---------------|
| `--workspace-roots=<csv>` | จำเป็นในบริบท multi-repo |
| `--repos-config=<path>` | แหล่งข้อมูล metadata ของ workspace ที่แนะนำ |

## 8.4 ความปลอดภัย / พฤติกรรมผลลัพธ์  
| Flag | วัตถุประสงค์ |
|------|---------------|
| `--report=<summary|detailed>` | ระดับความละเอียดของรายงาน |
| `--dry-run` | สร้างดัชนีในหน่วยความจำโดยไม่เขียนผลลัพธ์ |
| `--safety-mode=<strict|dev>` | ควบคุมความเข้มงวดของการจัดการข้อผิดพลาด |
| `--strict` | เป็น alias ของ `--safety-mode=strict` |

## 8.5 การกรอง  
| Flag | วัตถุประสงค์ |
|------|---------------|
| `--include-status=<csv>` | รวม workflow ที่มีสถานะบางอย่าง (เช่น stable,beta) |
| `--exclude-status=<csv>` | ยกเว้น workflow (เช่น deprecated) |
| `--include-platforms=<csv>` | รวม workflow ที่รองรับแพลตฟอร์มเฉพาะ |

---  
# 9. โครงสร้าง metadata ของ Workflow  
แต่ละรายการ workflow ใน `WORKFLOW_INDEX.json` ประกอบด้วย:  

- `id` — workflow id แบบมาตรฐาน (เช่น `smartspec_report_implement_prompter`)  
- `name` — ชื่อ CLI เต็มรูปแบบ (`/smartspec_report_implement_prompter`)  
- `version` — เวอร์ชันของ workflow  
- `role` — บทบาทการทำงาน (เช่น `support/implement`)  
- `category` — การจัดกลุ่มระดับสูง  
- `status` — `stable`, `beta`, `deprecated` เป็นต้น  
- `description` — วัตถุประสงค์โดยย่อ  
- `write_guard` — สิทธิ์การเขียนที่อนุญาต  
- `source_file` — เส้นทางไปยัง workflow spec  
- `supported_platforms` — เช่น `["kilocode", "claudecode", "antigravity"]`  
- `cli`:  
  - `binary` — ชื่อโปรแกรมที่ใช้รัน  
  - `required_flags[]`  
  - `optional_flags[]`  
- `tags[]` — คำอธิบายแบบอิสระ  
- `depends_on[]` — workflow ที่ต้องพึ่งพา  
- `produces[]` — รูปแบบไฟล์ผลลัพธ์  
- `last_updated` — เวลาที่อัปเดตล่าสุด  

---  
# 10. การตรวจจับความขัดแย้ง  
workflow จะตรวจสอบ:  
- workflow ID ซ้ำกัน  
- บทบาทหรือ write guard ที่ขัดแย้งกัน  
- ชื่อ CLI ที่ไม่ตรงกัน  
- ไฟล์ workflow spec ที่ไม่ถูกต้องหรือหายไป  

พฤติกรรมขึ้นอยู่กับโหมดความปลอดภัย:  
- **strict** → หยุดการเขียนดัชนีเมื่อพบความขัดแย้งรุนแรง  
- **dev** → อนุญาตให้สร้างดัชนีแต่ทำเครื่องหมายรายการที่ขัดแย้ง  

---  
# 11. การจัดการ workspace ขนาดใหญ่  
สำหรับโปรเจกต์ขนาดใหญ่หรือ multi-repo:  
- แนะนำให้ใช้การแยกวิเคราะห์แบบ streaming หรือแบ่งเป็นส่วน  
- การเขียนดัชนียังคงเป็น atomic  
- แจ้งเตือนเมื่อพบการตั้งค่า repo ที่ไม่สอดคล้องกัน  

---  
# 12. การนำไปใช้โดยเครื่องมืออื่น  
### 12.1 `/smartspec_project_copilot`  
ใช้ WORKFLOW_INDEX.json เพื่อ:  
- แนะนำ workflow ถัดไป  
- แสดง metadata ของ workflow  
- สร้างตัวอย่าง CLI  

### 12.2 SmartSpec UI / การผนวกรวม IDE  
ใช้ดัชนีเพื่อ:  
- แสดงรายการ workflow ที่มี  
- กรองตามหมวดหมู่, บทบาท, แพลตฟอร์ม, สถานะ  
- สร้างแม่แบบคำสั่งสำหรับผู้ใช้  

### 12.3 Automation Pipelines  
เหมาะสำหรับขั้นตอน CI เช่น:  
- ตรวจสอบความถูกต้องของการกำหนด workflow  
- ตรวจสอบความสมบูรณ์ของ workflow  
- รับรองความสอดคล้องกับ governance ของ workflow  

---  
# 13. การจัดการข้อผิดพลาด  
workflow ต้อง:  
- แจ้งเตือนเมื่อไม่พบหรือไม่สามารถอ่าน workflow roots  
- แจ้งเตือนสำหรับฟิลด์ที่ไม่กำหนดหรือไม่รองรับ  
- ตรวจจับการขาด flags CLI ที่จำเป็นใน spec  
- บันทึกปัญหาทั้งหมดในรายงานสุดท้าย  

ในโหมด strict ข้อผิดพลาดร้ายแรงจะยกเลิกการสร้างดัชนี  

---  
# 14. แนวทางปฏิบัติที่ดีที่สุด  
- เก็บ workflow specs ให้มีเวอร์ชันและจัดระเบียบภายใต้ `.smartspec/workflows/`  
- รัน workflow นี้ใหม่ทุกครั้งเมื่อมีการเพิ่ม, ลบ หรือแก้ไข workflow specs  
- ใช้ `--dry-run` ใน CI เพื่อตรวจจับความขัดแย้งของ metadata ตั้งแต่เนิ่นๆ  
- ใช้รายงานแบบละเอียดในระหว่างการพัฒนา  

---  
# 15. สรุป  
`/smartspec_reindex_workflows` คือกลไกที่ได้รับการสนับสนุนด้วย governance สำหรับสร้างดัชนี workflow แบบรวมศูนย์และมีโครงสร้าง ช่วยเสริม:  
- การค้นหา workflow  
- การบังคับใช้ governance  
- การผนวกรวม IDE และ UI  
- pipeline อัตโนมัติ  

ด้วยการรักษา `WORKFLOW_INDEX.json` SmartSpec จะมีฐานรากที่ทรงพลังและพร้อมสำหรับอนาคตในการจัดการ orchestration ของ workflow  

---  
สิ้นสุดคู่มือ