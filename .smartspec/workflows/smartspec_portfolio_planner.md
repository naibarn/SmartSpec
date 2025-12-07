---
description: SmartSpec - Portfolio Planner (Centralization v1)
---

# SmartSpec Portfolio Planner

Workflow นี้ทำหน้าที่ “วางแผนระดับพอร์ตโฟลิโอ” จาก SPEC ทั้งระบบ  
โดยอาศัยข้อมูลจาก:

- `.spec/SPEC_INDEX.json` (canonical)
- `.spec/registry/*` (glossary, api, data-model, critical-sections, optional UI component registry)
- config ที่กำหนด policy ของ repo/public-private

เป้าหมายคือช่วยทีมจัดลำดับงานของระบบใหญ่หลายร้อย spec  
และลดปัญหา “ทำงานผิดลำดับ dependency” หรือ “ชน core private โดยไม่ตั้งใจ”

---

## User Input

```text
$ARGUMENTS
```

ตัวอย่าง:
- `/smartspec_portfolio_planner`
- `/smartspec_portfolio_planner --tag=security`
- `/smartspec_portfolio_planner --repo=public`
- `/smartspec_portfolio_planner --report=detailed`
- `/smartspec_portfolio_planner --export=roadmap.md`

---

## 0) Centralization Resolver (MANDATORY)

### 0.1 Resolve SPEC_INDEX

ลำดับ:
1) `--specindex`
2) `.spec/SPEC_INDEX.json`
3) `SPEC_INDEX.json`
4) `.smartspec/SPEC_INDEX.json`
5) `specs/SPEC_INDEX.json`

### 0.2 Resolve Config / Directories

Config precedence:
1) `--config-path`
2) `.spec/smartspec.config.json`
3) `.smartspec/smartspec.config.json`
4) defaults

Defaults:
- `SPEC_HUB_DIR = ".spec"`
- `REGISTRY_DIR = ".spec/registry"`
- `OUTPUT_DIR = ".smartspec"`

---

## 1) Load Portfolio Inputs

1) Load SPEC_INDEX.
2) Build normalized spec list:
   - `id, title, category, status, priority, tags, dependencies, repo, path`
3) Load registries for canonical domain groupings.

---

## 2) Portfolio Views

สร้างมุมมองหลักอย่างน้อย 4 แบบ:

### 2.1 Dependency Graph View

- จัดกลุ่ม:
  - **roots** (ไม่มี dependencies)
  - **core hubs** (มี dependents มาก)
  - **leaf features**
- สรุป “คอขวด” ที่ถ้าช้าแล้วจะบล็อกหลายทีม

### 2.2 Priority & Status View

- แยกตาม priority
- ระบุ spec ที่:
  - priority สูงแต่ยังไม่พร้อม (missing tasks/plan)

### 2.3 Repo Policy View (Public ↔ Private)

- ตรวจความสัมพันธ์:
  - public spec ที่ depend กับ private core
- สร้างข้อเสนอเชิง policy:
  - public ต้อง treat private เป็น external contract  
  - งานเปลี่ยนแปลง core ต้องเกิดใน private specs ก่อน

### 2.4 UI Track View

ถ้า category=ui:
- ตรวจว่า spec มี `ui.json` หรือมีไฟล์ Penpot artifact ใน `files`
- แยกงาน UI ออกจาก logic track ใน roadmap

---

## 3) Gap Detection (Portfolio-level)

ตรวจหาช่องว่างที่พบบ่อย:

- Spec ที่มี dependencies แต่ไม่มี plan
- Spec ที่มี plan แต่ไม่มี tasks
- Spec ที่เป็น deprecated แต่ยังมี dependents active
- Domain ที่มีศัพท์/โมเดล/endpoint ซ้ำชื่อแต่ต่างความหมาย (ใช้ registry ช่วย flag เบื้องต้น)

---

## 4) Output

สร้างรายงาน:

- Summary report (default)
- Detailed report (ถ้า `--report=detailed`)
- Optional export:
  - `roadmap.md`
  - `portfolio-risk.md`

เขียนไปที่:
- `${OUTPUT_DIR}/reports/portfolio/`

---

## 5) Guardrails

- Workflow นี้เป็น **read-only** ต่อ `.spec/`  
  ไม่แก้ index หรือ registry อัตโนมัติ
- ถ้าพบช่องว่าง:
  - ให้เสนอ workflow ถัดไปที่ควรรัน เช่น:
    - `/smartspec_reindex_specs`
    - `/smartspec_spec_lifecycle_manager`
    - `/smartspec_generate_plan`
    - `/smartspec_generate_tasks`

Context: $ARGUMENTS
