# รายละเอียด `/smartspec_implement_tasks` และ `--skip-completed`

## 📚 ภาพรวม

`/smartspec_implement_tasks` เป็น workflow หลักสำหรับ **auto-implement tasks** ตาม `tasks.md` หรือ `implement-prompt.md`

**ความสามารถหลัก:**
- ✅ อ่าน tasks.md และ implement ทีละ task
- ✅ ตรวจสอบ checkbox status (`[x]` = เสร็จแล้ว, `[ ]` = ยังไม่เสร็จ)
- ✅ Skip tasks ที่เสร็จแล้ว (default behavior)
- ✅ Resume จากจุดที่หยุดไว้ (checkpoint/resume)
- ✅ Validate หลังทำแต่ละ task (compile, test, lint)
- ✅ Rollback อัตโนมัติถ้า validation fail
- ✅ Track progress และสร้าง report

---

## 🎯 การใช้งานพื้นฐาน

### 1. Implement ทั้งหมด (Skip completed)

```bash
/smartspec_implement_tasks specs/feature/spec-004-financial-system/tasks.md
```

**พฤติกรรม (Default):**
- Mode: `--skip-completed` (ข้าม tasks ที่ check แล้ว)
- Phase: ทุก phases
- Tasks: ทุก tasks (ที่ยังไม่เสร็จ)

**ตัวอย่าง tasks.md:**
```markdown
## Phase 1: Foundation

- [x] T001: Setup project structure (4h)
- [x] T002: Configure TypeScript (2h)
- [ ] T003: Setup database connection (3h)
- [ ] T004: Create base models (4h)

## Phase 2: Core Features

- [ ] T005: Implement CreditService (6h)
- [ ] T006: Implement PaymentService (5h)
```

**ผลลัพธ์:**
```
📊 Implementation Scope:
- Total tasks: 6
- Completed: 2 (T001, T002)
- Pending: 4 (T003-T006)
- Will implement: 4 tasks
- Estimated effort: 18 hours
- Mode: Skip completed ✅
```

**จะ implement:**
- ✅ T003: Setup database connection
- ✅ T004: Create base models
- ✅ T005: Implement CreditService
- ✅ T006: Implement PaymentService

**จะข้าม:**
- ❌ T001: Setup project structure (เสร็จแล้ว)
- ❌ T002: Configure TypeScript (เสร็จแล้ว)

---

### 2. Force Re-implement ทั้งหมด

```bash
/smartspec_implement_tasks specs/feature/spec-004/tasks.md --force-all
```

**พฤติกรรม:**
- **ไม่สนใจ checkbox status**
- Implement ทุก tasks ใหม่ทั้งหมด
- Overwrite ไฟล์ที่มีอยู่

**ใช้เมื่อไหร่:**
- ต้องการ re-implement ทั้งหมดใหม่
- Spec เปลี่ยนแปลงมาก
- ต้องการทดสอบ workflow

---

### 3. Implement เฉพาะ Phase

```bash
# Phase เดียว
/smartspec_implement_tasks specs/feature/spec-004/tasks.md --phase 2

# หลาย Phases
/smartspec_implement_tasks specs/feature/spec-004/tasks.md --phase 1,2,3

# Range of Phases
/smartspec_implement_tasks specs/feature/spec-004/tasks.md --phase 1-3
```

**ตัวอย่าง:**
```bash
/smartspec_implement_tasks specs/feature/spec-004/tasks.md --phase 2
```

**ผลลัพธ์:**
```
📊 Implementation Scope:
- Selected phases: Phase 2 only
- Tasks in Phase 2: 5 tasks (T010-T014)
- Completed: 2 tasks
- Will implement: 3 tasks (T012-T014)
- Estimated effort: 15 hours
```

---

### 4. Implement เฉพาะ Tasks

```bash
# Task เดียว
/smartspec_implement_tasks specs/feature/spec-004/tasks.md --tasks T005

# หลาย Tasks
/smartspec_implement_tasks specs/feature/spec-004/tasks.md --tasks T005,T006,T007

# Range of Tasks
/smartspec_implement_tasks specs/feature/spec-004/tasks.md --tasks T005-T010
```

**ตัวอย่าง:**
```bash
/smartspec_implement_tasks specs/feature/spec-004/tasks.md --tasks T005-T007
```

**ผลลัพธ์:**
```
📊 Implementation Scope:
- Selected tasks: T005-T007 (3 tasks)
- T005: Implement CreditService (6h) - Pending
- T006: Implement PaymentService (5h) - Completed ✅
- T007: Implement TransactionModel (4h) - Pending
- Will implement: 2 tasks (T005, T007)
- Will skip: 1 task (T006 - already completed)
- Estimated effort: 10 hours
```

---

### 5. Resume จากจุดที่หยุด

```bash
/smartspec_implement_tasks specs/feature/spec-004/tasks.md --resume
```

**พฤติกรรม:**
- อ่าน checkpoint file: `.smartspec-checkpoint.json`
- Resume จาก `next_task` ใน checkpoint
- Skip tasks ที่ทำไปแล้ว

**Checkpoint Structure:**
```json
{
  "timestamp": "2025-01-04T14:30:22Z",
  "spec_id": "spec-004-financial-system",
  "last_completed_task": "T015",
  "completed_tasks": ["T001", "T002", ..., "T015"],
  "failed_tasks": ["T010"],
  "skipped_tasks": ["T008"],
  "validation_status": {
    "compile": "PASS",
    "test": "PASS",
    "lint": "PASS"
  },
  "files_modified": ["src/index.ts", "src/models/User.ts"],
  "next_task": "T016"
}
```

**ตัวอย่าง:**
```
🔄 Resuming from checkpoint...

📊 Checkpoint Info:
- Last session: 2025-01-04 14:30:22
- Last completed: T015
- Next task: T016
- Failed tasks: T010 (will retry)
- Skipped tasks: T008 (dependencies not met)

📊 Implementation Scope:
- Total tasks: 45
- Already completed: 15 tasks
- Will implement: 30 tasks (T016-T045)
- Estimated effort: 120 hours
```

---

### 6. Combine Flags

```bash
# Resume + Skip completed + Specific phase
/smartspec_implement_tasks specs/feature/spec-004/tasks.md --resume --phase 3 --skip-completed

# Force all + Specific tasks
/smartspec_implement_tasks specs/feature/spec-004/tasks.md --force-all --tasks T001-T010

# Validate only (no implementation)
/smartspec_implement_tasks specs/feature/spec-004/tasks.md --validate-only
```

---

## 🔍 `--skip-completed` ทำงานอย่างไร

### Checkbox Status Detection

**ใน tasks.md:**
```markdown
## Phase 1: Foundation

- [x] T001: Setup project structure (4h)
  Description: Initialize project with proper folder structure
  Files:
    - CREATE: src/index.ts
    - CREATE: package.json

- [X] T002: Configure TypeScript (2h)
  Description: Setup TypeScript configuration
  Files:
    - CREATE: tsconfig.json

- [ ] T003: Setup database connection (3h)
  Description: Configure PostgreSQL connection
  Files:
    - CREATE: src/database/connection.ts
    - CREATE: src/database/config.ts

- [ ] T004: Create base models (4h)
  Description: Create User and Transaction models
  Files:
    - CREATE: src/models/User.ts
    - CREATE: src/models/Transaction.ts
```

### Parsing Logic

```typescript
interface Task {
  id: string;              // "T001"
  title: string;           // "Setup project structure"
  hours: number;           // 4
  completed: boolean;      // true if [x] or [X], false if [ ]
  phase: number;           // 1
  description: string;
  files: File[];
  dependencies: string[];
}

// Parse checkbox
function parseCheckbox(line: string): boolean {
  if (line.includes('- [x]') || line.includes('- [X]')) {
    return true;  // Completed
  }
  if (line.includes('- [ ]')) {
    return false; // Pending
  }
  throw new Error('Invalid checkbox format');
}
```

### Filtering Logic

```typescript
// Default: --skip-completed
function filterTasks(tasks: Task[], mode: string): Task[] {
  if (mode === '--skip-completed') {
    return tasks.filter(task => !task.completed);
  }
  
  if (mode === '--force-all') {
    return tasks; // Include all
  }
  
  return tasks.filter(task => !task.completed); // Default
}
```

### ตัวอย่างผลลัพธ์

**Before filtering:**
```
Total tasks: 4
- T001: ✅ Completed
- T002: ✅ Completed
- T003: ❌ Pending
- T004: ❌ Pending
```

**After filtering (--skip-completed):**
```
Filtered tasks: 2
- T003: ❌ Pending → Will implement
- T004: ❌ Pending → Will implement
```

**After filtering (--force-all):**
```
Filtered tasks: 4
- T001: ✅ Completed → Will re-implement
- T002: ✅ Completed → Will re-implement
- T003: ❌ Pending → Will implement
- T004: ❌ Pending → Will implement
```

---

## 🔄 Workflow Execution Flow

### Phase 1: Load & Parse

```
1. Load tasks.md
2. Parse YAML frontmatter
3. Parse all tasks
4. Check checkbox status
5. Build task registry

📊 Task Registry:
- Total: 45 tasks
- Completed: 15 tasks (checkbox [x])
- Pending: 30 tasks (checkbox [ ])
```

### Phase 2: Filter Scope

```
Apply filters:
1. Mode filter (--skip-completed or --force-all)
2. Phase filter (--phase X)
3. Task filter (--tasks X)
4. Resume filter (--resume)

📊 Filtered Tasks:
- Will implement: 10 tasks (T016-T025)
- Estimated effort: 40 hours
```

### Phase 3: Execute Tasks

```
For each task in filtered tasks:

1. Check dependencies
   ✅ All dependencies met → Continue
   ❌ Dependencies not met → Skip task

2. Implement task
   - Read task details
   - Load supporting files
   - Generate code
   - Create/edit files

3. Validate
   - Run TypeScript compiler
   - Run tests
   - Run linter
   
   ✅ All pass → Mark as completed
   ❌ Any fail → Rollback changes

4. Update checkpoint
   - Save progress
   - Update next_task
   - Save validation status

5. Update tasks.md
   - Change [ ] → [x]
   - Update timestamp
```

### Phase 4: Report

```
✅ Implementation Complete!

📊 Results:
- Tasks attempted: 10
- Tasks completed: 9
- Tasks failed: 1 (T020 - validation failed)
- Tasks skipped: 0

🧪 Validation:
- TypeScript: ✅ PASS
- Tests: ✅ 45/45 passing
- Linter: ✅ No errors

📁 Files:
- Created: 15 files
- Modified: 8 files
- Total changes: 2,345 lines

⏱️ Time:
- Estimated: 40 hours
- Actual: 38 hours (95% accuracy)

📝 Reports:
- Implementation report: specs/feature/spec-004/implementation-report-20250104.md
- Checkpoint: specs/feature/spec-004/.smartspec-checkpoint.json
```

---

## 💡 ประโยชน์ของ `--skip-completed`

### 1. ✅ ประหยัดเวลา

**ไม่ต้อง re-implement tasks ที่เสร็จแล้ว**

```
Without --skip-completed:
- Total tasks: 45
- Time: 180 hours (implement ทั้งหมดใหม่)

With --skip-completed (default):
- Completed tasks: 15 (skip)
- Pending tasks: 30 (implement)
- Time: 120 hours (ประหยัด 60 hours!)
```

### 2. ✅ ทำงานต่อเนื่องได้

**สามารถหยุดและทำต่อได้ทุกเมื่อ**

```
Day 1: Implement T001-T015 → Check [x]
Day 2: Run workflow → Auto skip T001-T015 → Start T016
Day 3: Run workflow → Auto skip T001-T020 → Start T021
```

### 3. ✅ ทำงานแบบ Incremental

**เพิ่ม tasks ใหม่ได้เรื่อยๆ โดยไม่กระทบของเก่า**

```markdown
## Phase 1: Foundation
- [x] T001: Setup project ✅
- [x] T002: Configure TypeScript ✅

## Phase 2: Core Features
- [x] T003: Implement CreditService ✅
- [ ] T004: Implement PaymentService ← Run workflow → Implement only this
- [ ] T005: Implement TransactionModel ← New task added
```

### 4. ✅ ทำงานแบบ Parallel

**หลายคนทำงานพร้อมกันได้**

```
Developer A: Implement T001-T010 → Check [x]
Developer B: Implement T011-T020 → Check [x]
Developer C: Run workflow → Auto skip T001-T020 → Start T021
```

### 5. ✅ Safe to Re-run

**Run workflow ซ้ำได้ไม่กี่ครั้งก็ได้**

```bash
# Run 1: Implement T001-T010
/smartspec_implement_tasks specs/feature/spec-004/tasks.md

# Run 2: Auto skip T001-T010, implement T011-T020
/smartspec_implement_tasks specs/feature/spec-004/tasks.md

# Run 3: Auto skip T001-T020, implement T021-T030
/smartspec_implement_tasks specs/feature/spec-004/tasks.md
```

**ไม่มีการ overwrite ไฟล์ที่ทำไว้แล้ว!** ✅

---

## 🎯 Use Cases

### Use Case 1: เริ่มต้นโปรเจคใหม่

```bash
# สร้าง spec และ tasks
/smartspec_generate_spec "Financial System"
/smartspec_generate_tasks specs/feature/spec-004-financial-system/spec.md

# Implement ทั้งหมด
/smartspec_implement_tasks specs/feature/spec-004-financial-system/tasks.md
```

**ผลลัพธ์:**
- Implement ทุก tasks (เพราะยังไม่มีอันไหนเสร็จ)
- สร้างไฟล์ทั้งหมดตาม spec
- Validate และ test

---

### Use Case 2: ทำงานต่อจากที่หยุดไว้

```bash
# Day 1: Implement Phase 1
/smartspec_implement_tasks specs/feature/spec-004/tasks.md --phase 1
# → T001-T010 completed ✅

# Day 2: Implement Phase 2 (auto skip Phase 1)
/smartspec_implement_tasks specs/feature/spec-004/tasks.md --phase 2
# → T011-T020 completed ✅

# Day 3: Implement remaining (auto skip Phase 1-2)
/smartspec_implement_tasks specs/feature/spec-004/tasks.md
# → T021-T045 completed ✅
```

---

### Use Case 3: แก้ไข Task ที่ Fail

```bash
# Run 1: T020 failed validation
/smartspec_implement_tasks specs/feature/spec-004/tasks.md
# → T001-T019 ✅, T020 ❌

# Fix T020 manually
# Edit src/services/payment.service.ts

# Run 2: Re-implement T020 only
/smartspec_implement_tasks specs/feature/spec-004/tasks.md --tasks T020 --force-all
# → T020 ✅

# Run 3: Continue with remaining tasks
/smartspec_implement_tasks specs/feature/spec-004/tasks.md
# → Auto skip T001-T020, implement T021-T045
```

---

### Use Case 4: เพิ่ม Tasks ใหม่

```markdown
## tasks.md (Before)
- [x] T001: Setup project
- [x] T002: Configure TypeScript
- [x] T003: Implement CreditService

## tasks.md (After - เพิ่ม T004, T005)
- [x] T001: Setup project
- [x] T002: Configure TypeScript
- [x] T003: Implement CreditService
- [ ] T004: Implement PaymentService ← NEW
- [ ] T005: Implement TransactionModel ← NEW
```

```bash
# Run workflow
/smartspec_implement_tasks specs/feature/spec-004/tasks.md

# ผลลัพธ์:
# - Skip T001-T003 (เสร็จแล้ว)
# - Implement T004-T005 (ใหม่)
```

---

### Use Case 5: Re-implement ทั้งหมดเมื่อ Spec เปลี่ยน

```bash
# Spec เปลี่ยนแปลงมาก → ต้องการ re-implement ทั้งหมด
/smartspec_implement_tasks specs/feature/spec-004/tasks.md --force-all

# ผลลัพธ์:
# - Re-implement ทุก tasks (ไม่สนใจ checkbox)
# - Overwrite ไฟล์ทั้งหมด
# - Validate ใหม่ทั้งหมด
```

---

## 🔧 Best Practices

### 1. ✅ ใช้ --skip-completed เป็น Default

```bash
# Good (default)
/smartspec_implement_tasks specs/feature/spec-004/tasks.md

# Explicit
/smartspec_implement_tasks specs/feature/spec-004/tasks.md --skip-completed
```

### 2. ✅ Check Tasks ทันทีหลัง Implement

```markdown
# Before
- [ ] T001: Setup project

# After implementation
- [x] T001: Setup project ← เปลี่ยนทันที
```

### 3. ✅ ใช้ --resume เมื่อ Workflow หยุดกลางคัน

```bash
# Workflow stopped at T015
/smartspec_implement_tasks specs/feature/spec-004/tasks.md --resume
# → Continue from T016
```

### 4. ✅ ใช้ --phase เมื่อทำทีละ Phase

```bash
# Implement Phase 1 first
/smartspec_implement_tasks specs/feature/spec-004/tasks.md --phase 1

# Then Phase 2
/smartspec_implement_tasks specs/feature/spec-004/tasks.md --phase 2
```

### 5. ✅ ใช้ --force-all เฉพาะเมื่อจำเป็น

```bash
# Only when:
# - Spec changed significantly
# - Need to re-implement everything
# - Testing workflow
/smartspec_implement_tasks specs/feature/spec-004/tasks.md --force-all
```

### 6. ✅ Validate Before Commit

```bash
# Run validation only (no implementation)
/smartspec_implement_tasks specs/feature/spec-004/tasks.md --validate-only

# If pass → Commit
git add .
git commit -m "feat: Implement spec-004 tasks T001-T045"
```

---

## 📊 Comparison: Skip vs Force

| Aspect | --skip-completed (Default) | --force-all |
|--------|---------------------------|-------------|
| **Checkbox** | Respect checkbox status | Ignore checkbox |
| **Completed tasks** | Skip | Re-implement |
| **Pending tasks** | Implement | Implement |
| **Files** | Create new, keep existing | Overwrite all |
| **Time** | Fast (only pending) | Slow (all tasks) |
| **Use case** | Continue work | Fresh start |
| **Safety** | Safe (no overwrite) | Destructive |

---

## ✅ สรุป

### `--skip-completed` (Default)

**ทำอะไร:**
- อ่าน checkbox status ใน tasks.md
- Skip tasks ที่มี `[x]` หรือ `[X]`
- Implement เฉพาะ tasks ที่มี `[ ]`

**ประโยชน์:**
1. ✅ ประหยัดเวลา (ไม่ทำซ้ำ)
2. ✅ ทำงานต่อเนื่องได้
3. ✅ ทำงานแบบ Incremental
4. ✅ ทำงานแบบ Parallel
5. ✅ Safe to re-run

**ใช้เมื่อไหร่:**
- ✅ ทำงานต่อจากที่หยุดไว้
- ✅ เพิ่ม tasks ใหม่
- ✅ แก้ไข tasks ที่ fail
- ✅ ทำงานทีละ phase

### `--force-all`

**ทำอะไร:**
- ไม่สนใจ checkbox status
- Re-implement ทุก tasks
- Overwrite ไฟล์ทั้งหมด

**ใช้เมื่อไหร่:**
- ❌ Spec เปลี่ยนแปลงมาก
- ❌ ต้องการเริ่มใหม่ทั้งหมด
- ❌ ทดสอบ workflow

---

**SmartSpec ใช้ `--skip-completed` เป็น default เพื่อความสะดวกและปลอดภัย!** 🎉
