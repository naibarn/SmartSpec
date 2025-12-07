---
description: SmartSpec - Global Registry Audit (Centralization v1)
---

# SmartSpec Global Registry Audit

Workflow นี้แก้ช่องโหว่ “semantic drift ข้ามทั้งระบบ”  
โดยสแกน registry + SPEC + tasks เพื่อหา:

- ชื่อโมเดล/ฟิลด์ซ้ำความหมาย
- endpoint ซ้ำ pattern
- glossary synonyms ที่ควร consolidate
- UI component naming drift (ถ้ามี ui-component-registry)

ผลลัพธ์คือรายงานและข้อเสนอ alignment tasks แบบเป็นระบบ

---

## User Input

```text
$ARGUMENTS
```

ตัวอย่าง:
- `/smartspec_global_registry_audit`
- `/smartspec_global_registry_audit --scope=security`
- `/smartspec_global_registry_audit --report=detailed`
- `/smartspec_global_registry_audit --emit-alignment-tasks`

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

Defaults:
- `SPEC_HUB_DIR = ".spec"`
- `REGISTRY_DIR = ".spec/registry"`
- `OUTPUT_DIR = ".smartspec"`

---

## 1) Load Canonical Registries

โหลดอย่างน้อย:
- `glossary.json`
- `data-model-registry.json`
- `api-registry.json`
- `critical-sections-registry.json`

Optional:
- `ui-component-registry.json`

---

## 2) Load System Specs

1) Read SPEC_INDEX.
2) For each spec entry:
   - เก็บ:
     - id, category, repo, status, dependencies, path
   - หา `spec.md` และ `tasks.md` (best-effort)

---

## 3) Audit Dimensions

### 3.1 Glossary Audit

- หา:
  - คำที่สะกดต่างแต่ใช้แทนกัน
  - คำที่ใช้ข้ามหลาย spec แต่ยังไม่มี canonical entry
- สร้างข้อเสนอ:
  - add canonical term
  - add aliases

### 3.2 Data Model Audit

- เปรียบเทียบ:
  - registries vs ระบุใน spec/tasks
- flag:
  - field names ที่มีความหมายเดียวแต่ canonical ต่าง
  - entity ที่ถูกประกาศซ้ำ

### 3.3 API Audit

- ตรวจ route patterns
- ตรวจ naming ของ resource/service

### 3.4 Critical Sections Coverage

- ตรวจว่า spec สำคัญในโดเมนเสี่ยงสูง  
  มี critical sections ตามมาตรฐานทีมครบหรือไม่

### 3.5 UI Audit (Special)

ถ้า category=ui:
- ตรวจว่ามี `ui.json`
- ตรวจว่า component ที่อ้างใน spec/tasks
  สอดคล้องกับ ui-component-registry (ถ้ามี)

---

## 4) Output Types

### 4.1 Audit Report (default)

เขียนไปที่:
- `${OUTPUT_DIR}/reports/registry-audit/`

สรุป:
- Drift hotspots
- Candidate merges
- Spec owners ที่เกี่ยวข้อง

### 4.2 Emit Alignment Tasks (optional)

ถ้า `--emit-alignment-tasks`:
- สร้างไฟล์ข้อเสนอในรูปแบบ md/json ต่อ spec:
  - `alignment-tasks.<spec-id>.md`
- **ไม่แก้ tasks.md เดิมอัตโนมัติ**  
  ให้ทีม review ก่อน

---

## 5) Guardrails

- Read-only ต่อ registries โดย default
- ห้ามเปลี่ยน canonical definitions อัตโนมัติในระบบใหญ่
- ต้องแสดงเหตุผลและ spec owners ที่เกี่ยวข้องเสมอ

Context: $ARGUMENTS
