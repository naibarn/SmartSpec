# smartspec_implement_tasks Flags Clarification

ชี้แจงความเข้าใจผิดเกี่ยวกับ flags และ platform-specific features

---

## ❌ ความเข้าใจผิด: --kilocode และ --claude Flags

### คำถาม:
> `/smartspec_implement_tasks --kilocode` กับ `/smartspec_implement_tasks --claude` ต่างกันอย่างไร?

### คำตอบ:
**❌ ไม่มี flags เหล่านี้!**

`/smartspec_implement_tasks` **ไม่มี** platform-specific flags เช่น:
- ❌ `--kilocode`
- ❌ `--claude`
- ❌ `--cursor`
- ❌ `--roo`

---

## ✅ Flags ที่มีจริงใน smartspec_implement_tasks

### 1. `--phase <number|range>`
**ระบุ phase ที่ต้องการ implement**

```bash
# Implement phase 1 only
/smartspec_implement_tasks specs/feature/spec-004/tasks.md --phase 1

# Implement phases 1-3
/smartspec_implement_tasks specs/feature/spec-004/tasks.md --phase 1-3

# Implement phases 1,3,5
/smartspec_implement_tasks specs/feature/spec-004/tasks.md --phase 1,3,5
```

---

### 2. `--tasks <task_ids|range>`
**ระบุ tasks ที่ต้องการ implement**

```bash
# Implement T001 only
/smartspec_implement_tasks specs/feature/spec-004/tasks.md --tasks T001

# Implement T001-T010
/smartspec_implement_tasks specs/feature/spec-004/tasks.md --tasks T001-T010

# Implement T001,T003,T005
/smartspec_implement_tasks specs/feature/spec-004/tasks.md --tasks T001,T003,T005
```

---

### 3. `--resume`
**Continue from last checkpoint**

```bash
# Resume from last checkpoint
/smartspec_implement_tasks specs/feature/spec-004/tasks.md --resume
```

**ทำงานอย่างไร:**
- อ่าน checkpoint file (`.smartspec/checkpoints/spec-004-checkpoint.json`)
- หา task สุดท้ายที่ทำเสร็จ
- เริ่มจาก task ถัดไป

---

### 4. `--skip-completed` (Default)
**Skip tasks ที่ mark เสร็จแล้ว (checkbox = [x])**

```bash
# Skip completed tasks (default behavior)
/smartspec_implement_tasks specs/feature/spec-004/tasks.md

# หรือระบุชัดเจน
/smartspec_implement_tasks specs/feature/spec-004/tasks.md --skip-completed
```

**ทำงานอย่างไร:**
- อ่าน tasks.md
- ตรวจสอบ checkbox status
- `- [x] T001:` → Skip (เสร็จแล้ว)
- `- [ ] T002:` → Implement (ยังไม่เสร็จ)

---

### 5. `--force-all`
**Re-implement ทุก tasks (ignore checkboxes)**

```bash
# Re-implement all tasks
/smartspec_implement_tasks specs/feature/spec-004/tasks.md --force-all
```

**ทำงานอย่างไร:**
- Ignore checkbox status
- Implement ทุก tasks แม้จะ mark เสร็จแล้ว

**เมื่อไหร่ควรใช้:**
- ต้องการ re-implement ทั้งหมด
- Refactoring ครั้งใหญ่
- เปลี่ยน technology stack

---

### 6. `--validate-only`
**Validate only, ไม่ implement**

```bash
# Validate without implementing
/smartspec_implement_tasks specs/feature/spec-004/tasks.md --validate-only
```

**ทำงานอย่างไร:**
- Run validation commands only
- ไม่ implement code ใหม่
- แสดง errors/warnings

**เมื่อไหร่ควรใช้:**
- ตรวจสอบว่า code ปัจจุบันผ่าน validation หรือไม่
- ก่อน commit/push
- ก่อน deploy

---

## 🔄 Workflows ที่สับสนกับ implement_tasks

### 1. `/smartspec_generate_implement_prompt`
**สร้าง prompt สำหรับ AI platforms**

```bash
# สร้าง prompt สำหรับ Kilo Code
/smartspec_generate_implement_prompt specs/feature/spec-004 --platform kilocode

# สร้าง prompt สำหรับ Claude
/smartspec_generate_implement_prompt specs/feature/spec-004 --platform claude
```

**Platform options:**
- `kilocode` - Kilo Code format
- `claude` - Claude Code format
- `roo` - Roo Code format

**ผลลัพธ์:**
- สร้างไฟล์ `implement-prompt-spec-004.md`
- Copy prompt ไปใช้กับ AI platform

---

### 2. `/smartspec_generate_cursor_prompt`
**สร้าง prompt สำหรับ Cursor/Antigravity**

```bash
# สร้าง prompt สำหรับ Cursor
/smartspec_generate_cursor_prompt specs/feature/spec-004
```

**ผลลัพธ์:**
- สร้างไฟล์ `cursor-prompt-spec-004.md`
- Copy prompt ไปใช้กับ Cursor

---

## 📊 Comparison Table

| Feature | implement_tasks | generate_implement_prompt | generate_cursor_prompt |
|---------|----------------|---------------------------|------------------------|
| **Platform Flags** | ❌ ไม่มี | ✅ `--platform` | ❌ ไม่มี (Cursor only) |
| **Direct Implementation** | ✅ ใช่ | ❌ ไม่ใช่ (สร้าง prompt) | ❌ ไม่ใช่ (สร้าง prompt) |
| **Auto-Continue** | ✅ ใช่ | ⚠️ ขึ้นอยู่กับ platform | ⚠️ ขึ้นอยู่กับ platform |
| **Checkpoint/Resume** | ✅ `--resume` | ❌ ไม่มี | ❌ ไม่มี |
| **Skip Completed** | ✅ `--skip-completed` | ⚠️ ขึ้นอยู่กับ platform | ⚠️ ขึ้นอยู่กับ platform |
| **Phase Control** | ✅ `--phase` | ✅ `--phase` | ✅ `--phase` |
| **Task Control** | ✅ `--tasks` | ✅ `--tasks` | ✅ `--tasks` |
| **Validate Only** | ✅ `--validate-only` | ❌ ไม่มี | ❌ ไม่มี |

---

## 💡 ทำไม implement_tasks ไม่มี platform flags?

### เหตุผล:

1. **Platform-Agnostic Design**
   - `implement_tasks` ออกแบบให้ทำงานกับ AI agent
   - ไม่ขึ้นกับ platform เฉพาะ

2. **Direct Implementation**
   - Implement โดยตรงผ่าน AI agent
   - ไม่ต้องสร้าง prompt แยก

3. **Unified Workflow**
   - Workflow เดียวสำหรับทุก use cases
   - ไม่ต้องเลือก platform

---

## 🎯 Use Cases และ Workflows ที่ถูกต้อง

### Use Case 1: Implement with Direct Implementation

```bash
# ใช้ implement_tasks โดยตรง
/smartspec_implement_tasks specs/feature/spec-004/tasks.md
```

**ข้อดี:**
- ✅ Auto-continue
- ✅ Checkpoint/resume
- ✅ Skip completed
- ✅ Validation

---

### Use Case 2: Implement ด้วย Kilo Code

**Step 1: สร้าง prompt**
```bash
/smartspec_generate_implement_prompt specs/feature/spec-004 --platform kilocode
```

**Step 2: Copy prompt**
```bash
cat specs/feature/spec-004/implement-prompt-spec-004.md
```

**Step 3: Paste ใน Kilo Code**
- เปิด Kilo Code
- Paste prompt
- Run

**ข้อดี:**
- ✅ ใช้ Kilo Code ได้
- ⚠️ ต้อง manual copy-paste
- ⚠️ ไม่มี auto-continue (ต้อง restart ทุก 10 tasks)

---

### Use Case 3: Implement ด้วย Claude

**Step 1: สร้าง prompt**
```bash
/smartspec_generate_implement_prompt specs/feature/spec-004 --platform claude
```

**Step 2: Copy prompt**
```bash
cat specs/feature/spec-004/implement-prompt-spec-004.md
```

**Step 3: Paste ใน Claude**
- เปิด Claude
- Paste prompt
- Run

**ข้อดี:**
- ✅ ใช้ Claude ได้
- ⚠️ ต้อง manual copy-paste
- ⚠️ ไม่มี auto-continue

---

### Use Case 4: Implement ด้วย Cursor

**Step 1: สร้าง prompt**
```bash
/smartspec_generate_cursor_prompt specs/feature/spec-004
```

**Step 2: Copy prompt**
```bash
cat specs/feature/spec-004/cursor-prompt-spec-004.md
```

**Step 3: Paste ใน Cursor**
- เปิด Cursor
- กด Ctrl+L (Composer)
- Paste prompt
- Run

**ข้อดี:**
- ✅ ใช้ Cursor ได้
- ✅ User-friendly format
- ⚠️ ต้อง manual copy-paste

---

## ❌ ทำไม Kilo Code ไม่แตก Sub-Tasks ให้?

### คำถาม:
> กรณี --kilocode ก็ไม่เห็นแตก sub tasks ให้เลย

### คำตอบ:

**1. ไม่มี `--kilocode` flag**
- `implement_tasks` ไม่มี flag นี้
- ไม่มี platform-specific logic

**2. Sub-task splitting ไม่ใช่ feature ของ SmartSpec**
- SmartSpec แตก tasks เป็น granular tasks แล้ว (T001, T002, ...)
- ไม่มี "sub-task" ระดับต่ำกว่า

**3. Kilo Code มี hard limit 10 tasks/cycle**
- นี่คือข้อจำกัดของ Kilo Code เอง
- ไม่ใช่ SmartSpec

---

## ✅ วิธีแก้ปัญหา Kilo Code Hard Limit

### ปัญหา:
- Kilo Code หยุดทุก 10 tasks
- ต้อง restart manual

### วิธีแก้:

**Option 1: Use direct implementation (แนะนำ!)**
```bash
# ไม่มี hard limit, auto-continue
/smartspec_implement_tasks specs/feature/spec-004/tasks.md
```

**Option 2: แตก tasks เป็น batches**
```bash
# Batch 1: T001-T010
/smartspec_generate_implement_prompt specs/feature/spec-004 --platform kilocode --tasks T001-T010

# Batch 2: T011-T020
/smartspec_generate_implement_prompt specs/feature/spec-004 --platform kilocode --tasks T011-T020

# Batch 3: T021-T030
/smartspec_generate_implement_prompt specs/feature/spec-004 --platform kilocode --tasks T021-T030
```

**Option 3: ใช้ --phase แทน**
```bash
# Phase 1 only (usually < 10 tasks)
/smartspec_generate_implement_prompt specs/feature/spec-004 --platform kilocode --phase 1

# Phase 2 only
/smartspec_generate_implement_prompt specs/feature/spec-004 --platform kilocode --phase 2
```

---

## 📚 สรุป

### ✅ ข้อเท็จจริง:

1. **`implement_tasks` ไม่มี platform flags**
   - ไม่มี `--kilocode`, `--claude`, `--cursor`, `--roo`
   - Platform-agnostic design

2. **Flags ที่มีจริง:**
   - `--phase`, `--tasks`, `--resume`, `--skip-completed`, `--force-all`, `--validate-only`

3. **Sub-task splitting ไม่มี**
   - SmartSpec แตก tasks เป็น granular แล้ว
   - ไม่มี "sub-task" ระดับต่ำกว่า

4. **Kilo Code hard limit เป็นข้อจำกัดของ platform**
   - ไม่ใช่ SmartSpec
   - แก้ได้ด้วยการแตก batches หรือใช้ AI agent

---

### 🚀 คำแนะนำ:

**สำหรับโปรเจคขนาดใหญ่ (100+ tasks):**
- ✅ ใช้ `/smartspec_implement_tasks` (AI agent)
- ✅ Auto-continue, checkpoint/resume
- ✅ ไม่มี hard limit

**สำหรับโปรเจคเล็ก (< 20 tasks):**
- ⚠️ ใช้ `/smartspec_generate_implement_prompt` + Kilo/Claude
- ⚠️ Manual copy-paste
- ⚠️ ต้อง restart ถ้าเกิน 10 tasks

---

**ไฟล์นี้เป็นส่วนหนึ่งของ SmartSpec Documentation**  
**Repository:** https://github.com/naibarn/SmartSpec
