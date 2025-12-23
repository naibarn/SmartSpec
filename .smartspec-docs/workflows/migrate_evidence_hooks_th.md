# คู่มือ: /smartspec_migrate_evidence_hooks

## 1. ภาพรวม

**`/smartspec_migrate_evidence_hooks`** คือ workflow ที่ขับเคลื่อนด้วย AI ซึ่งออกแบบมาเพื่อแปลง "Evidence" (หลักฐาน) ที่เป็นข้อความบรรยายในไฟล์ `tasks.md` ให้เป็น evidence hooks ที่เป็นมาตรฐานและเครื่องคอมพิวเตอร์สามารถอ่านได้โดยอัตโนมัติ

เครื่องมือนี้มีความสำคัญอย่างยิ่งในการปรับปรุงโปรเจกต์ SmartSpec รุ่นเก่าให้ทันสมัย และเปิดใช้งาน workflow การตรวจสอบอัตโนมัติ เช่น `/smartspec_verify_tasks_progress_strict`

## 2. ปัญหาที่แก้ไข

ในไฟล์ `tasks.md` รุ่นเก่าๆ ส่วนของ "Evidence" มักจะเป็นช่องที่ให้ใส่ข้อความอิสระ:

```markdown
| **Evidence:** user model ควรมีฟิลด์ `last_login` |
```

ข้อความนี้มนุษย์อ่านเข้าใจง่าย แต่เครื่องคอมพิวเตอร์ไม่สามารถตรวจสอบโดยอัตโนมัติได้ เพื่อแก้ปัญหานี้ SmartSpec ได้นำเสนอ **evidence hooks** ที่เป็นมาตรฐานขึ้นมา:

```markdown
| **Evidence:** evidence: db_schema table=users column=last_login |
```

การแปลงข้อความบรรยายเหล่านี้ด้วยตนเองสำหรับ task หลายร้อยรายการเป็นงานที่น่าเบื่อและเสี่ยงต่อความผิดพลาด workflow นี้จะช่วยทำให้กระบวนการดังกล่าวเป็นไปโดยอัตโนมัติ

## 3. การทำงาน

workflow นี้ใช้โมเดล AI เพื่อวิเคราะห์ task และ evidence ที่เป็นข้อความบรรยายอย่างชาญฉลาด จากนั้นจึงสร้าง evidence hook ที่แม่นยำขึ้นมา

1.  **วิเคราะห์ `tasks.md`:** อ่านไฟล์ที่ระบุและระบุ task ทั้งหมดที่มี evidence เป็นข้อความบรรยาย
2.  **แปลงด้วย AI:** สำหรับแต่ละ task ที่ระบุ จะส่งรายละเอียด task และข้อความ evidence ไปยังโมเดล AI
3.  **สร้าง Hook:** AI จะได้รับ prompt ให้เลือกรูปแบบ hook ที่เหมาะสมที่สุด (เช่น `file_exists`, `file_contains`, `api_route`) และสร้าง hook ที่สอดคล้องกัน
4.  **แสดงตัวอย่าง หรือปรับใช้จริง:**
    -   **โหมด Preview (ค่าเริ่มต้น):** แสดงผลลัพธ์แบบ `diff` เพื่อให้เห็นการเปลี่ยนแปลงที่เสนอ โดยไม่แก้ไขไฟล์ต้นฉบับ ทำให้สามารถตรวจสอบได้อย่างปลอดภัย
    -   **โหมด Apply (`--apply`):** แก้ไขไฟล์ `tasks.md` โดยตรง โดยแทนที่ข้อความบรรยายเก่าด้วย hooks ที่สร้างขึ้นใหม่

## 4. พารามิเตอร์

| พารามิเตอร์ | ประเภท | คำอธิบาย | จำเป็น |
| :--- | :--- | :--- | :--- |
| `--tasks-file` | `string` | พาธไปยังไฟล์ `tasks.md` ที่ต้องการแปลง | ใช่ |
| `--apply` | `boolean` | หากเป็น `true` จะปรับใช้การเปลี่ยนแปลงกับไฟล์โดยตรง ค่าเริ่มต้นคือ `false` (โหมด preview) | ไม่ |
| `--model` | `string` | โมเดล AI ที่ใช้ในการแปลง (เช่น `gpt-4.1-mini`) ค่าเริ่มต้นคือ `gpt-4.1-mini` | ไม่ |

## 5. คู่มือการใช้งานทีละขั้นตอน

### ขั้นตอนที่ 1: รันในโหมด Preview (แนะนำ)

เริ่มต้นด้วยโหมด preview เสมอ เพื่อให้แน่ใจว่า AI สร้าง hooks ได้ถูกต้อง นี่เป็นการทำงานแบบอ่านอย่างเดียวที่ปลอดภัย

```bash
/smartspec_migrate_evidence_hooks \
  --tasks-file "specs/core/spec-core-001-authentication/tasks.md"
```

ตรวจสอบผลลัพธ์อย่างละเอียด `diff` จะแสดง evidence เก่า (`-`) และ hook ใหม่ที่เสนอ (`+`) อย่างชัดเจน

```diff
--- a/specs/core/spec-core-001-authentication/tasks.md
+++ b/specs/core/spec-core-001-authentication/tasks.md
@@ -150,7 +150,7 @@
 | TSK-AUTH-020 | Create OpenAPI Specification | The full OpenAPI 3.0 specification for all authentication endpoints. |
-| **Evidence:** The openapi.yaml file should be present in the /docs directory. |
+| **Evidence:** evidence: file_exists path=docs/openapi.yaml |
 --------------------------------------------------------------------------------
```

### ขั้นตอนที่ 2: ตรวจสอบข้อเสนอแนะ

-   **hooks ถูกต้องหรือไม่?** `file_exists` เหมาะสมหรือไม่? พาธถูกต้องหรือไม่?
-   **AI มั่นใจแค่ไหน?** หาก AI ไม่แน่ใจ อาจสร้าง hook เช่น `evidence: file_exists path=MANUAL_REVIEW_REQUIRED` ซึ่งคุณจะต้องแก้ไขด้วยตนเอง
-   **มีข้อผิดพลาดหรือไม่?** AI มีประสิทธิภาพสูงแต่ก็ไม่สมบูรณ์แบบ ควรตรวจสอบพาธไฟล์และตัวระบุต่างๆ อีกครั้ง

### ขั้นตอนที่ 3: ปรับใช้การเปลี่ยนแปลง

เมื่อคุณพอใจกับผลลัพธ์ในโหมด preview แล้ว ให้รันคำสั่งอีกครั้งพร้อมกับ flag `--apply` workflow จะรอ 5 วินาที เพื่อให้คุณมีโอกาสสุดท้ายในการยกเลิก (ด้วย `Ctrl+C`)

```bash
/smartspec_migrate_evidence_hooks \
  --tasks-file "specs/core/spec-core-001-authentication/tasks.md" \
  --apply
```

หลังจากรันคำสั่ง ไฟล์ `tasks.md` จะได้รับการอัปเดต

## 6. ประเภท Evidence ที่รองรับ

AI ได้รับการฝึกฝนให้สร้าง hook ประเภททั่วไปดังต่อไปนี้:

-   `evidence: file_exists path=<path>`
-   `evidence: file_contains path=<path> content=<text>`
-   `evidence: api_route method=<GET|POST|PUT|DELETE> path=<route>`
-   `evidence: db_schema table=<table_name> [column=<column_name>]`
-   `evidence: gh_commit repo=<repo> sha=<commit_sha>`
-   `evidence: test_exists path=<test_file> name=<test_name>`
-   `evidence: config_key file=<config_file> key=<key_name>`

## 7. แนวทางปฏิบัติที่ดีที่สุด

-   **Version Control:** รัน workflow นี้บน Git branch ที่สะอาดเสมอ เพื่อให้คุณสามารถตรวจสอบและย้อนกลับการเปลี่ยนแปลงได้อย่างง่ายดาย
-   **รัน Preview ก่อน:** อย่ารันด้วย `--apply` ในครั้งแรก preview คือตาข่ายความปลอดภัยของคุณ
-   **ทำซ้ำ:** สำหรับไฟล์ขนาดใหญ่ คุณสามารถรันการแปลง แก้ไขข้อผิดพลาดด้วยตนเอง แล้วจึง commit การเปลี่ยนแปลง
-   **ใช้ร่วมกับการตรวจสอบ:** หลังจากแปลงแล้ว ให้รัน `/smartspec_verify_tasks_progress_strict` เพื่อดูประโยชน์ของการตรวจสอบอัตโนมัติได้ทันที

ด้วยการใช้ `/smartspec_migrate_evidence_hooks` คุณสามารถเร่งกระบวนการปรับปรุงโปรเจกต์ของคุณให้ทันสมัย และปลดล็อกพลังของระบบนิเวศการกำกับดูแลอัตโนมัติของ SmartSpec ได้อย่างเต็มที่
