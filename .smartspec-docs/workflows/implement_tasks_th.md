# /smartspec_implement_tasks คู่มือ (v6.0, ภาษาไทย)

## ภาพรวม

workflow `/smartspec_implement_tasks` คือแกนกลางของระบบ SmartSpec ที่ทำหน้าที่เป็นเครื่องมือหลักในการดำเนินการเปลี่ยนแปลงโค้ด โดยมีวัตถุประสงค์หลักเพื่อดำเนินการเปลี่ยนแปลงโค้ดตามงานที่กำหนดไว้อย่างเคร่งครัดในไฟล์ `tasks.md`

workflow นี้ทำงานภายใต้การกำกับดูแลของ SmartSpec v6 อย่างเข้มงวด โดยเน้นรูปแบบการทำงานแบบ tasks-first, การควบคุมการเขียนอย่างปลอดภัย, การอ่านข้อมูลจากหลาย repository ในโหมดอ่านอย่างเดียว และการบังคับให้มีการรายงานผลเพื่อเป็นหลักฐาน นอกจากนี้ยังบังคับใช้มาตรการความปลอดภัยขั้นสูงสำหรับ privileged-ops (เช่น no-shell, allowlist, timeouts) และถูกออกแบบมาเพื่อรวมเข้ากับ Kilo Code Orchestrator ได้อย่างราบรื่นสำหรับการดำเนินการที่ซับซ้อนและหลายขั้นตอน

**เวอร์ชัน:** 6.2.0  
**บทบาท:** การดำเนินการ/การประมวลผล

---

## การใช้งาน

### การใช้งาน CLI

workflow นี้ถูกเรียกใช้งานผ่าน command line โดยต้องระบุพาธของไฟล์ `tasks.md` เป็นพารามิเตอร์ตำแหน่งหลัก การดำเนินการเขียนไฟล์ต้องมีการยืนยันแบบสองชั้นอย่างชัดเจน (`--apply` และ `--write-code`)

**ไวยากรณ์พื้นฐาน (สำหรับตรวจสอบเท่านั้น):**

```bash
/smartspec_implement_tasks <tasks.md_path> [flags]
```

**ตัวอย่าง (การนำการเปลี่ยนแปลงไปใช้):**

```bash
/smartspec_implement_tasks specs/feature_x/my_spec/tasks.md \
  --apply \
  --write-code \
  --tasks T001,T002 \
  --safety-mode strict
```

### การใช้งานกับ Kilo Code

เมื่อรันภายใต้ Kilo Code ต้องใช้ flag `--kilocode` สำหรับงานที่ซับซ้อน workflow จะบังคับให้มีการแยกย่อย sub-task ตามกฎของ Kilo Orchestrator (Invariants 0.2, 0.4) ผู้ใช้ Kilo Code มักใช้สกุลไฟล์ `.md` เพื่อความชัดเจน แม้ว่าการประมวลผลจะเหมือนกัน

**ไวยากรณ์พื้นฐาน (Kilo Code):**

```bash
/smartspec_implement_tasks.md <tasks.md_path> --kilocode [flags]
```

**ตัวอย่าง (การดำเนินการแบบ Orchestrated):**

ตัวอย่างนี้บังคับให้ใช้ Orchestrator และนำการเปลี่ยนแปลงไปใช้ โดยสมมติว่ากำลังรันใน sub-task เดียวของ Kilo ที่มุ่งเน้นช่วงงานเฉพาะ

```bash
/smartspec_implement_tasks.md specs/feature_x/my_spec/tasks.md \
  --kilocode \
  --require-orchestrator \
  --apply \
  --write-code \
  --range 5-10 \
  --json
```

---

## กรณีการใช้งาน

### กรณีการใช้งาน 1: การตรวจสอบแผนการดำเนินงาน (Dry Run)

**สถานการณ์:** นักพัฒนาต้องการยืนยันว่า workflow สามารถแยกวิเคราะห์ tasks, ระบุไฟล์เป้าหมาย และสร้างแผนการเปลี่ยนแปลงได้โดยไม่แก้ไขโค้ดหรือสถานะของ tasks ใดๆ

**วัตถุประสงค์:** สร้างไฟล์ `change_plan.md` และ `report.md` ในโหมดตรวจสอบเท่านั้น

**คำสั่ง CLI:**

```bash
/smartspec_implement_tasks specs/api_refactor/v2/tasks.md \
  --validate-only \
  --tasks T005 \
  --out .spec/reports/api_refactor_v2_T005_dryrun
```

**ผลลัพธ์ที่คาดหวัง:**

1. รหัสออก (exit code) เป็น `0`  
2. ไม่มีการเปลี่ยนแปลงใดๆ กับซอร์สโค้ดหรือไฟล์ `tasks.md`  
3. โฟลเดอร์ผลลัพธ์ `.spec/reports/api_refactor_v2_T005_dryrun` ประกอบด้วย:  
    * `report.md`: รายละเอียดขั้นตอนการดำเนินการที่เสนอสำหรับ T005  
    * `change_plan.md`: คำอธิบายเชิงโครงสร้างของการแก้ไขไฟล์ที่ *จะ* เกิดขึ้น  
    * `summary.json`: สถานะถูกระบุว่า `"status": "success"`, `"applied": false`

### กรณีการใช้งาน 2: การดำเนินการชุดงานพร้อมเขียนโค้ด

**สถานการณ์:** แผนได้รับการอนุมัติแล้ว นักพัฒนาต้องการดำเนินการ tasks T001, T002 และ T003 ซึ่งเกี่ยวข้องกับการแก้ไขซอร์สโค้ดและอัปเดตช่องทำเครื่องหมายใน `tasks.md`

**วัตถุประสงค์:** นำการเปลี่ยนแปลงโค้ดไปใช้, อัปเดตช่องทำเครื่องหมาย และสร้างรายงานขั้นสุดท้าย

**คำสั่ง CLI:**

```bash
/smartspec_implement_tasks specs/ui_update/dark_mode/tasks.md \
  --apply \
  --write-code \
  --tasks T001,T002,T003 \
  --safety-mode strict
```

**ผลลัพธ์ที่คาดหวัง:**

1. รหัสออก (exit code) เป็น `0` (ถ้าสำเร็จ)  
2. ไฟล์ซอร์สโค้ด (code/tests) ถูกแก้ไขตามแผนการดำเนินงานสำหรับ T001-T003  
3. ช่องทำเครื่องหมายที่เกี่ยวข้องกับ T001, T002 และ T003 ใน `tasks.md` ถูกทำเครื่องหมายว่าสำเร็จแล้ว (`[x]`)  
4. รายงานถูกสร้างขึ้นโดยระบุรายละเอียดการเปลี่ยนแปลงที่นำไปใช้ พร้อมกับไฟล์ `summary.json` ที่แสดง `"applied": true` และรายการไฟล์ที่ถูกแก้ไขในส่วน `writes`

### กรณีการใช้งาน 3: การ Orchestration ของ Kilo และการเข้าถึงเครือข่าย

**สถานการณ์:** รันภายใต้ Kilo Code การดำเนินการต้องดึง dependency ภายนอกใหม่ (เข้าถึงเครือข่าย) เพื่อทำงานให้เสร็จสมบูรณ์สำหรับ task T010 การรันต้องถูก orchestration

**วัตถุประสงค์:** ดำเนินการ T010 พร้อมอนุญาตให้เข้าถึงเครือข่าย ภายใต้การควบคุมของ Kilo Orchestrator

**คำสั่ง Kilo Code:**

```bash
/smartspec_implement_tasks.md specs/deps_upgrade/tasks.md \
  --kilocode \
  --require-orchestrator \
  --apply \
  --write-code \
  --task T010 \
  --allow-network
```

**ผลลัพธ์ที่คาดหวัง:**

1. workflow ตรวจสอบบริบทของ Kilo Orchestrator หากไม่พบจะล้มเหลวทันทีเนื่องจาก `--require-orchestrator`  
2. อนุญาตการเข้าถึงเครือข่ายชั่วคราวสำหรับการแก้ไข/ดึง dependency  
3. ดำเนินการ task T010 โดยแก้ไขโค้ดและอาจรวมถึงไฟล์ lock  
4. ส่งคืนการควบคุมให้กับ Kilo Orchestrator หลังจาก sub-task เสร็จสิ้น เพื่อให้ Orchestrator ตัดสินใจขั้นตอนถัดไป (เช่น การรันการตรวจสอบ)  
5. สร้างรายงานที่ระบุการใช้ `--allow-network`

---

## พารามิเตอร์

พารามิเตอร์ (flags) ที่รองรับโดย `/smartspec_implement_tasks` มีดังนี้:

| Category | Flag | Type | Description | Default |
| :--- | :--- | :--- | :--- | :--- |
| **Inputs** | Positional | Path | พาธไปยังไฟล์ `tasks.md` | จำเป็นต้องระบุ |
| **Inputs** | `--tasks-path` | Path | เขียนทับพาธตำแหน่งสำหรับ `tasks.md` | - |
| **Inputs** | `--spec-path` | Path | เขียนทับการตรวจจับอัตโนมัติของ `spec.md` | ตรวจจับอัตโนมัติ |
| **Inputs** | `--spec-id` | String | ระบุ spec ผ่าน `SPEC_INDEX.json` | - |
| **Task Selection** | `--task <n>` | String | เลือก task เดี่ยวตามหมายเลข (เช่น T001) | - |
| **Task Selection** | `--tasks <csv>` | CSV | เลือกหลาย task โดยใช้รายการคั่นด้วยจุลภาค | - |
| **Task Selection** | `--range <a-b>` | Range | เลือกช่วงของ tasks (เช่น 5-10) | - |
| **Task Selection** | `--from <n>` | Int | เริ่มดำเนินการจากหมายเลข task `n` | - |
| **Task Selection** | `--start-from <Tnnn>` | String | ชื่อเรียกเดิมสำหรับเริ่มจาก task ID เฉพาะ | - |
| **Task Selection** | `--skip-completed` | Flag | ข้าม tasks ที่ทำเครื่องหมายว่าสำเร็จแล้ว | ค่าเริ่มต้น |
| **Task Selection** | `--force-all` | Flag | ดำเนินการทุก task โดยไม่สนสถานะสำเร็จ | - |
| **Task Selection** | `--resume` | Flag | พยายามดำเนินการต่อจากรันที่ค้างไว้ก่อนหน้า | - |
| **Phases** | `--phase <n>` | Int | เลือก tasks ที่ติดแท็กด้วยหมายเลข phase เฉพาะ | - |
| **Phases** | `--phases <csv>` | CSV | เลือก tasks ที่ติดแท็กด้วยหลาย phase | - |
| **Phases** | `--phase-range <a-b>` | Range | เลือก tasks ในช่วง phase | - |
| **Write Gates** | `--apply` | Flag | **Gate 1:** เปิดใช้งานการเขียนที่มีการกำกับดูแล (รายงาน, หมายเหตุ/ช่องทำเครื่องหมายใน `tasks.md`) | ปิดใช้งาน |
| **Write Gates** | `--write-code` | Flag | **Gate 2:** ยืนยันการแก้ไข runtime source trees (ต้องใช้ `--apply`) | ปิดใช้งาน |
| **Safety/Preview** | `--validate-only` | Flag | รันในโหมด dry-run (ไม่เขียนโค้ดหรือสถานะ task) | - |
| **Safety/Preview** | `--dry-run` | Flag | ชื่อเรียกแทนของ `--validate-only` | - |
| **Safety/Preview** | `--safety-mode <strict|dev>` | String | กำหนดระดับความปลอดภัยของการกำกับดูแล | `strict` |
| **Safety/Preview** | `--strict` | Flag | ชื่อเรียกแทนของ `--safety-mode strict` | - |
| **Kilo/Orchestrator** | `--kilocode` | Flag | เปิดใช้งาน semantics การรวมกับ Kilo | ปิดใช้งาน |
| **Kilo/Orchestrator** | ... | ... | ... | ... |