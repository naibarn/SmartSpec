---
description: Synchronize tasks.md with spec.md to detect inconsistencies and auto-update tasks when spec changes using SmartSpec v4.0.
---

## User Input

```text
$ARGUMENTS
```

Expected: `specs/feature/spec-004/spec.md` (will auto-find tasks.md)

## 0. Load Context

Read `.smartspec/` files + SPEC_INDEX

## 1. Resolve Paths

SPEC_PATH from $ARGUMENTS
TASKS_PATH = same directory as spec.md + `/tasks.md`

## 2. Parse Both Files

### 2.1 Parse SPEC
Extract:
- Key features
- Components/services
- API endpoints
- Database entities
- Security requirements
- Testing requirements
- Dependencies (related specs)
- Non-goals

### 2.2 Parse tasks.md
Extract:
- All tasks
- Features covered
- Components addressed
- Validation requirements

## 3. Compare & Detect Inconsistencies

### 3.1 Missing Features in tasks.md
```python
spec_features = extract_features(spec)
task_features = extract_features(tasks)

missing_features = spec_features - task_features

for feature in missing_features:
    inconsistencies.append({
        'type': 'MISSING_FEATURE',
        'severity': 'HIGH',
        'description': f'Feature "{feature}" in spec but not in tasks',
        'spec_section': find_section(spec, feature),
        'action': 'Add tasks for this feature'
    })
```

### 3.2 Outdated Task Descriptions
```python
# Check if spec section has been updated after tasks.md created
spec_updated_date = extract_update_date(spec)
tasks_generated_date = extract_generated_date(tasks)

if spec_updated_date > tasks_generated_date:
    # Deep compare descriptions
    for task in tasks:
        related_spec_content = find_related_spec_content(spec, task)
        if content_differs(task.description, related_spec_content):
            inconsistencies.append({
                'type': 'OUTDATED_DESCRIPTION',
                'severity': 'MEDIUM',
                'task_id': task.id,
                'description': 'Task description may be outdated',
                'action': 'Review and update task description'
            })
```

### 3.3 New Requirements
```python
# Find NEW sections or major changes in spec
new_sections = find_new_sections(spec, since=tasks_generated_date)

for section in new_sections:
    inconsistencies.append({
        'type': 'NEW_REQUIREMENT',
        'severity': 'HIGH',
        'section': section.title,
        'description': f'New section added: {section.title}',
        'action': 'Add tasks to cover this requirement'
    })
```

### 3.4 Removed Features (Non-Goals)
```python
# Check if any tasks cover features now in Non-Goals
non_goals = extract_non_goals(spec)

for task in tasks:
    if task_covers_non_goal(task, non_goals):
        inconsistencies.append({
            'type': 'COVERS_NON_GOAL',
            'severity': 'HIGH',
            'task_id': task.id,
            'description': 'Task covers feature now in Non-Goals',
            'action': 'Remove or modify this task'
        })
```

### 3.5 Dependency Mismatches
```python
# Check if related specs referenced correctly
spec_deps = extract_dependencies(spec)
task_deps = extract_dependencies(tasks)

missing_deps = spec_deps - task_deps
extra_deps = task_deps - spec_deps

# Report mismatches
```

## 4. Generate Sync Report

```markdown
# Spec-Tasks Synchronization Report

**Generated:** YYYY-MM-DD HH:mm
**Author:** SmartSpec Architect v4.0
**SPEC:** [path] (Updated: YYYY-MM-DD)
**Tasks:** [path] (Generated: YYYY-MM-DD)

---

## Summary

**Status:** [IN_SYNC | OUT_OF_SYNC | NEEDS_REVIEW]

**Inconsistencies Found:** XX

**Breakdown:**
- 🔴 Critical (HIGH): XX
- 🟡 Warning (MEDIUM): XX
- 🔵 Info (LOW): XX

---

## Critical Issues (HIGH)

### 1. Missing Feature: [Feature Name]

**Severity:** HIGH  
**Type:** MISSING_FEATURE

**Description:**
Feature "[Feature Name]" is defined in spec.md but has no corresponding tasks.

**SPEC Location:**
Section: [Section name]
Lines: [XX-YY]

**Recommended Action:**
Add 3-5 tasks to implement this feature:
- Task: Create [component] for [feature]
- Task: Implement [API endpoint]
- Task: Add tests for [feature]

**Suggested Phase:** Phase X (based on dependencies)

---

### 2. New Requirement: [Section]

**Severity:** HIGH
**Type:** NEW_REQUIREMENT

**Description:**
New section "[Section]" added to spec.md after tasks.md was generated.

**Added:** YYYY-MM-DD
**Tasks Generated:** YYYY-MM-DD

**Recommended Action:**
Review new requirement and add tasks if implementation needed.

---

## Warnings (MEDIUM)

### 1. Outdated Description: T015

**Severity:** MEDIUM
**Type:** OUTDATED_DESCRIPTION

**Description:**
Task T015 description may be outdated based on spec.md changes.

**SPEC Changed:** YYYY-MM-DD
**Section:** [Section name]

**Recommended Action:**
- Review spec.md section
- Update task description if needed
- Verify acceptance criteria still valid

---

## Auto-Fix Actions Available

### Action 1: Add Tasks for Missing Features

Would add XX new tasks:

**Phase X (New):**
- T0XX: Implement [feature 1]
- T0XX: Implement [feature 2]
- T0XX: Test [feature 1]

**Phase Y (Extend existing):**
- T0XX: Integrate [feature] with [existing]

### Action 2: Update Outdated Descriptions

Would update X task descriptions:
- T015: [Old] → [New]
- T023: [Old] → [New]

### Action 3: Remove Non-Goal Tasks

Would remove/modify X tasks:
- T042: Covers feature now in Non-Goals

---

## Recommendations

1. **Immediate Actions:**
   - [ ] Add tasks for X missing features
   - [ ] Review X outdated task descriptions
   - [ ] Remove/modify X non-goal tasks

2. **Review Required:**
   - [ ] Verify all acceptance criteria still valid
   - [ ] Check if phase structure needs adjustment
   - [ ] Validate dependencies still correct

3. **After Updates:**
   - [ ] Regenerate kilo-prompt.md
   - [ ] Update plan.md if timeline changes
   - [ ] Notify team of scope changes

---
```

## 5. Auto-Update tasks.md (Optional)

If inconsistencies found AND user confirms:

### 5.1 Add Missing Tasks
```python
for missing_feature in missing_features:
    new_tasks = generate_tasks_for_feature(missing_feature, spec)
    insert_tasks_in_appropriate_phase(tasks_md, new_tasks)
```

### 5.2 Update Descriptions
```python
for outdated_task in outdated_tasks:
    updated_description = extract_from_spec(spec, outdated_task)
    update_task_description(tasks_md, outdated_task.id, updated_description)
```

### 5.3 Mark Removed Tasks
```python
for non_goal_task in non_goal_tasks:
    mark_task_as_removed(tasks_md, non_goal_task.id, reason="Now in Non-Goals")
```

### 5.4 Update Header
```markdown
# Implementation Tasks - [Project]

**Generated:** [Original date]
**Last Synced:** YYYY-MM-DD HH:mm
**Sync Author:** SmartSpec Architect v4.0
**Sync Reason:** Spec updated with [changes]

**Sync Changes:**
- Added X tasks for new features
- Updated X task descriptions
- Removed/marked X tasks (Non-Goals)

---
```

## 6. Output

### 6.1 Write Sync Report
Path: Same directory as tasks.md
Filename: `sync-report-YYYYMMDD.md`

### 6.2 Update tasks.md (if confirmed)
Create backup: `tasks.backup-YYYYMMDD.md`
Update: `tasks.md`

## 7. Report (Thai)

```
🔄 ตรวจสอบความสอดคล้องระหว่าง spec.md และ tasks.md

📊 ผลการตรวจสอบ:

**สถานะ:** [IN_SYNC ✅ | OUT_OF_SYNC ⚠️]

**พบความไม่สอดคล้อง:** XX รายการ
- 🔴 Critical: XX (ต้องแก้ทันที)
- 🟡 Warning: XX (ควรแก้)
- 🔵 Info: XX (ตรวจสอบ)

📄 Sync Report: sync-report-YYYYMMDD.md

⚠️ ปัญหาสำคัญ:
1. Feature "[Name]" ใน spec แต่ไม่มี tasks
2. Section ใหม่ "[Name]" เพิ่มใน spec
3. Task T0XX มี description ที่ล้าสมัย

🔧 การแก้ไขอัตโนมัติ:

**สามารถ auto-fix:**
- เพิ่ม XX tasks สำหรับ features ใหม่
- Update XX task descriptions
- ลบ/ปรับ XX tasks (Non-Goals)

**ต้องการ auto-update tasks.md หรือไม่?**
- YES: ระบบจะสำรอง tasks.md และ update อัตโนมัติ
- NO: ใช้ sync report เพื่อ update manual

💡 คำแนะนำ:
1. อ่าน sync-report-YYYYMMDD.md ทั้งหมด
2. ตัดสินใจ update วิธีไหน (auto/manual)
3. หลัง update แล้ว regenerate kilo-prompt.md
4. Update plan.md ถ้า timeline เปลี่ยน

🔄 Auto-update command:
[Command with --auto-update flag]
```

Context: $ARGUMENTS

---

# UI Centralization Addendum (Penpot-first)

เอกสารนี้เป็นส่วนเสริมของ **SmartSpec Centralization Contract**  
เพื่อรองรับ **SPEC ประเภท UI** ที่มีข้อกำหนดพิเศษ:

- **UI design source of truth เป็น JSON** (เพื่อใช้กับ Penpot)
- ทีม UI ต้องสามารถแก้ UI ได้ตรงจากไฟล์นี้
- งานของทีม dev ต้องผูกกับ component/logic โดยไม่ทำให้ไฟล์ UI JSON ปน logic

ใช้ addendum นี้วางต่อท้าย contract ในทุก workflow ที่แตะ UI:
- generate-spec
- generate-plan
- generate-tasks
- implement-tasks
- verify-tasks-progress
- generate-tests
- refactor-code
- reverse-to-spec
- reindex-specs
- validate-index
- sync-spec-tasks
- fix-errors
- generate-implement-prompt / generate-cursor-prompt (ในส่วน canonical constraints)

---

## 1) UI File Model

สำหรับ UI spec ให้ถือว่าในโฟลเดอร์ spec มีไฟล์หลัก 2 ชั้น:

1) `spec.md`  
   - narrative, scope, non-goals, UX rules, accessibility, performance targets  
   - อ้างอิงไฟล์ UI JSON เป็น design artifact

2) `ui.json` (หรือชื่อที่ทีมกำหนดใน config)  
   - **Penpot-editable**  
   - เก็บ layout, components mapping, design tokens references  
   - **ห้าม** ใส่ business logic หรือ API behaviour ในไฟล์นี้

> ถ้าทีมต้องการชื่อไฟล์เฉพาะ ให้กำหนดใน config:
```json
{
  "ui_spec": {
    "ui_json_name": "ui.json",
    "component_registry": "ui-component-registry.json"
  }
}
```

---

## 2) Registry เพิ่มเติมสำหรับ UI (แนะนำ)

เพิ่มไฟล์ registry ใหม่แบบ optional:

- `.spec/registry/ui-component-registry.json`

โครงสร้างขั้นต่ำแนะนำ:
```json
{
  "version": "1.0.0",
  "last_updated": "ISO-8601",
  "components": [
    {
      "canonical_name": "UserAvatar",
      "penpot_component_id": "penpot:component:xxx",
      "code_component_path": "src/components/user/UserAvatar.tsx",
      "owned_by_spec": "spec-XXX",
      "aliases": []
    }
  ]
}
```

**กติกา:**
- ชื่อ component ใน tasks/implementation ต้องอ้าง `canonical_name` เป็นค่า default
- ถ้าพบชื่อใหม่:
  - generate-spec / generate-tasks สามารถเพิ่ม entry ใหม่ได้
  - implement / verify ต้องอ่านอย่างเดียว

---

## 3) UI Naming & Separation Rules (MUST)

### 3.1 Separation of Concerns

- `ui.json` = design + structure + bindings
- business logic / data fetching / permissions  
  ต้องอยู่ใน:
  - code components
  - service layer
  - hooks/store
  - หรือ spec.md ในส่วน logic description

### 3.2 Canonical-first

เมื่อ workflow ต้องเสนอชื่อ component:
1) เช็ค `ui-component-registry.json` (ถ้ามี)
2) เช็ค glossary (คำเรียกหน้าจอ/ฟีเจอร์)
3) ถ้ายังไม่มี:
   - เสนอชื่อใหม่แบบ `Proposed`
   - สร้าง task ให้ลงทะเบียน

---

## 4) Workflow-specific Enforcement

### 4.1 generate-spec (UI category)

ต้อง:
- ตรวจ/สร้าง `ui.json` template ขั้นต่ำ (ถ้ายังไม่มี)
- เพิ่ม `ui.json` ลงใน SPEC_INDEX `files` (ถ้าสคีมารองรับ)
- ระบุใน spec.md ว่า:
  - design source-of-truth = ui.json
  - logic อยู่ที่ code layer

### 4.2 generate-tasks

สำหรับ UI spec:
- สร้าง 3 กลุ่มงานแยกกันชัดเจน:

1) **Design tasks (UI team)**
   - ปรับ layout/flow ใน `ui.json` ผ่าน Penpot

2) **Component binding tasks**
   - map Penpot component → code component
   - อัปเดต `ui-component-registry.json` (ถ้าจำเป็น)

3) **Logic tasks (Dev team)**
   - สร้าง/แก้ hooks/services/state
   - ห้ามใส่ logic ใหม่ใน `ui.json`

### 4.3 implement-tasks / refactor-code

- Treat `ui.json` เป็น **design-owned**
- แก้ไขได้เฉพาะเมื่อ tasks ระบุชัดเจน
- ถ้าพบว่า logic ถูกฝังใน ui.json:
  - สร้าง refactor task เพื่อย้าย logic ออก

### 4.4 generate-tests

- อ้าง component canonical names
- สนับสนุนแนวทาง:
  - component tests
  - accessibility checks
  - visual regression (ถ้าทีมใช้)

---

## 5) Index & Validation Rules

### 5.1 SPEC_INDEX

สำหรับ UI spec:
- แนะนำให้มี field เสริมใน entry (ถ้าทีมอนุญาตแบบ additive):
```json
{
  "ui_artifacts": {
    "ui_json_path": "specs/ui/spec-123/ui.json",
    "penpot_project": "optional-string"
  }
}
```

ถ้าไม่เพิ่ม schema:
- ให้ใช้ `files` list แทน

### 5.2 validate-index / global-registry-audit

ต้องตรวจอย่างน้อย:
- UI spec ที่ category=ui ต้องมี `ui.json`
- ชื่อ component ที่ spec/tasks อ้าง ต้องสอดคล้องกับ registry

---

## 6) ผลลัพธ์ที่ต้องการ

- ทีม UI แก้ UI ได้โดยไม่ชนกับ dev logic
- ลดการแตกชื่อ component ซ้ำซ้อน
- UI specs กลายเป็นส่วนหนึ่งของ centralization ไม่ใช่โลกคู่ขนาน
