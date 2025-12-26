# Verify Report Action Guide

**Version:** 1.0.0  
**Date:** 2025-12-26  
**Purpose:** แนะนำ workflow ที่เหมาะสมสำหรับการแก้ไขปัญหาที่ verify report แจ้ง

---

## Overview

หลังจากรัน `/smartspec_verify_tasks_progress_strict` แล้วได้ report ที่แจ้งปัญหา ควรใช้ workflow ไหนต่อไป?

---

## 🚀 NEW: Automated Solution (Recommended)

**Best Approach:** ใช้ `/smartspec_report_implement_prompter` เพื่อสร้าง prompts สำหรับแก้ไขปัญหาอัตโนมัติ!

```bash
# Step 1: Verify and get report
/smartspec_verify_tasks_progress_strict tasks.md --json --out reports/

# Step 2: Generate fix prompts automatically
/smartspec_report_implement_prompter \
  --verify-report reports/latest/summary.json \
  --tasks tasks.md

# Output: .spec/prompts/latest/
#   ├── README.md (summary + priority order)
#   ├── not_implemented.md (if any)
#   ├── missing_tests.md (if any)
#   ├── naming_issues.md (if any)
#   └── ... (other categories)

# Step 3: Follow generated prompts
cat .spec/prompts/latest/README.md

# Step 4: Implement fixes and verify
/smartspec_verify_tasks_progress_strict tasks.md
```

**Benefits:**
- ✅ **Automatic category detection** - ไม่ต้องเลือก workflow เอง
- ✅ **Priority-based ordering** - จัดลำดับความสำคัญให้อัตโนมัติ
- ✅ **Actionable prompts** - คำแนะนำที่ชัดเจนสำหรับแต่ละปัญหา
- ✅ **Single workflow** - ใช้ workflow เดียวสำหรับทุกปัญหา
- ✅ **No manual decision** - ไม่ต้องตัดสินใจเอง

**Documentation:** `.smartspec/workflows/smartspec_report_implement_prompter.md` (v7.1.0)

---

## Manual Approach (Alternative)

**คำตอบขึ้นอยู่กับ Problem Category ที่ report แจ้ง**

ถ้าต้องการแก้ไขด้วยตนเอง ให้ดู workflow ที่แนะนำด้านล่าง:

---

## Problem Categories & Recommended Workflows

### 1. 📝 Naming Issues

**ปัญหา:** ไฟล์มีอยู่แต่ชื่อไม่ตรงกับ evidence

**Report แสดง:**
```
## 📝 Naming Issues

### [x] TASK-001: Implement CheckpointManager

**Test Evidence:**
- ❌ Line 7: `tests/ss_autopilot/test_checkpoint_manager.py`
  - Reason: anchor not found
  - Similar files found:
    - `test_agent_wrapper.py` (65% similar)

**Recommendations:**
→ Update evidence path to: /home/ubuntu/SmartSpec/tests/ss_autopilot/test_agent_wrapper.py
   OR rename file to match evidence
```

**แนวทางแก้ไข:**

#### Option A: แก้ไข evidence ใน tasks.md (แนะนำ)

**Workflow:** ไม่ต้องใช้ workflow - แก้ไขด้วยตนเอง

**Steps:**
1. เปิด `tasks.md`
2. แก้ไข evidence path ให้ตรงกับไฟล์จริง
3. Save
4. รัน verify อีกครั้งเพื่อยืนยัน

**ตัวอย่าง:**
```markdown
# Before
- evidence: test path="tests/ss_autopilot/test_checkpoint_manager.py" contains="test_save"

# After
- evidence: test path="tests/ss_autopilot/test_agent_wrapper.py" contains="test_save"
```

#### Option B: Rename ไฟล์ให้ตรงกับ evidence

**Workflow:** ไม่ต้องใช้ workflow - rename ด้วยตนเอง

**Steps:**
1. Rename ไฟล์ให้ตรงกับ evidence
2. อัปเดต imports ที่เกี่ยวข้อง
3. รัน tests เพื่อยืนยัน
4. รัน verify อีกครั้ง

**คำเตือน:** ระวัง breaking changes ถ้าไฟล์ถูก import ที่อื่น

---

### 2. ❌ Not Implemented

**ปัญหา:** ไม่มีไฟล์ทั้ง code และ test

**Report แสดง:**
```
## ❌ Not Implemented

### [ ] TASK-002: Add parallel execution

**Code Evidence:**
- ❌ Line 10: `smartspec/ss_autopilot/parallel_execution.py`
  - Reason: file not found

**Test Evidence:**
- ❌ Line 11: `tests/ss_autopilot/test_parallel_execution.py`
  - Reason: file not found

**Recommendations:**
→ Create implementation file: smartspec/ss_autopilot/parallel_execution.py
→ Create test file: tests/ss_autopilot/test_parallel_execution.py
```

**แนวทางแก้ไข:**

#### Workflow: `/smartspec_implement_tasks`

**Purpose:** Implement code changes from tasks.md

**Usage:**
```bash
/smartspec_implement_tasks <path/to/tasks.md> [--task-ids TASK-002]
```

**What it does:**
1. อ่าน task จาก tasks.md
2. สร้างไฟล์ตาม evidence
3. Implement code ตาม task description
4. เพิ่ม evidence hooks
5. รัน tests (ถ้ามี)

**After implementation:**
```bash
# Verify again
/smartspec_verify_tasks_progress_strict <path/to/tasks.md>
```

**Alternative:** Manual implementation
1. สร้างไฟล์ตาม evidence path
2. Implement code
3. เพิ่ม tests
4. รัน verify

---

### 3. ⚠️ Missing Tests

**ปัญหา:** มี code แต่ไม่มี test

**Report แสดง:**
```
## ⚠️ Missing Tests

### [x] TASK-003: Add caching layer

**Code Evidence:**
- ✅ Line 15: `smartspec/ss_autopilot/cache.py`
  - Symbol found: CacheManager

**Test Evidence:**
- ❌ Line 16: `tests/ss_autopilot/test_cache.py`
  - Reason: file not found

**Recommendations:**
→ Create test file: tests/ss_autopilot/test_cache.py
→ Add test for CacheManager
```

**แนวทางแก้ไข:**

#### Workflow: `/smartspec_generate_tests`

**Purpose:** Generate test artifacts/suggestions

**Usage:**
```bash
/smartspec_generate_tests <module-path> [--output tests/]
```

**What it does:**
1. วิเคราะห์ code ที่ต้องการ test
2. สร้าง test template
3. แนะนำ test cases
4. สร้างไฟล์ test

**Example:**
```bash
# Generate tests for cache.py
/smartspec_generate_tests .smartspec/ss_autopilot/cache.py --output tests/ss_autopilot/
```

**After generation:**
```bash
# Run tests
pytest tests/ss_autopilot/test_cache.py

# Verify again
/smartspec_verify_tasks_progress_strict <path/to/tasks.md>
```

**Alternative:** Manual test creation
1. สร้าง `test_cache.py`
2. เขียน test cases
3. รัน pytest
4. รัน verify

---

### 4. ⚠️ Missing Code

**ปัญหา:** มี test แต่ไม่มี code (ไม่ค่อยเกิด แต่เป็นไปได้)

**Report แสดง:**
```
## ⚠️ Missing Code

### [ ] TASK-004: Add validation

**Code Evidence:**
- ❌ Line 20: `smartspec/ss_autopilot/validator.py`
  - Reason: file not found

**Test Evidence:**
- ✅ Line 21: `tests/ss_autopilot/test_validator.py`
  - Contains found: test_validate_input

**Recommendations:**
→ Create implementation file: smartspec/ss_autopilot/validator.py
→ Implement code to pass existing tests
```

**แนวทางแก้ไข:**

#### Workflow: `/smartspec_implement_tasks`

**Usage:**
```bash
/smartspec_implement_tasks <path/to/tasks.md> --task-ids TASK-004
```

**What it does:**
1. อ่าน task และ existing tests
2. สร้างไฟล์ implementation
3. Implement code เพื่อให้ tests pass

**After implementation:**
```bash
# Run tests to verify
pytest tests/ss_autopilot/test_validator.py

# Verify again
/smartspec_verify_tasks_progress_strict <path/to/tasks.md>
```

---

### 5. 🔍 Symbol Issues

**ปัญหา:** มีไฟล์แต่ไม่มี symbol ที่ระบุ

**Report แสดง:**
```
## 🔍 Symbol Issues

### [x] TASK-005: Add logger

**Code Evidence:**
- ❌ Line 25: `smartspec/ss_autopilot/logger.py`
  - Reason: symbol not found: AdvancedLogger
  - File exists but symbol missing

**Recommendations:**
→ Add symbol to file: AdvancedLogger
→ OR update evidence to use existing symbol
```

**แนวทางแก้ไข:**

#### Option A: เพิ่ม symbol ที่ขาด

**Workflow:** `/smartspec_implement_tasks`

**Usage:**
```bash
/smartspec_implement_tasks <path/to/tasks.md> --task-ids TASK-005
```

**What it does:**
1. เปิดไฟล์ที่มีอยู่
2. เพิ่ม symbol ที่ขาด
3. Implement code

#### Option B: แก้ไข evidence ให้ตรงกับ symbol ที่มี

**Workflow:** ไม่ต้องใช้ workflow - แก้ไขด้วยตนเอง

**Steps:**
1. เปิด `tasks.md`
2. แก้ไข evidence symbol ให้ตรงกับที่มีในไฟล์
3. รัน verify อีกครั้ง

---

### 6. 📄 Content Issues

**ปัญหา:** มีไฟล์และ symbol แต่ content ไม่ตรง

**Report แสดง:**
```
## 📄 Content Issues

### [x] TASK-006: Add error handling

**Code Evidence:**
- ❌ Line 30: `smartspec/ss_autopilot/error_handler.py`
  - Reason: contains not found: "with_error_handling"
  - File and symbol exist but content missing

**Recommendations:**
→ Add missing content: "with_error_handling"
→ OR update evidence to match existing content
```

**แนวทางแก้ไข:**

#### Option A: เพิ่ม content ที่ขาด

**Workflow:** `/smartspec_implement_tasks`

**Usage:**
```bash
/smartspec_implement_tasks <path/to/tasks.md> --task-ids TASK-006
```

**What it does:**
1. เปิดไฟล์ที่มีอยู่
2. เพิ่ม content ที่ขาด
3. Verify content

#### Option B: แก้ไข evidence ให้ตรงกับ content ที่มี

**Workflow:** ไม่ต้องใช้ workflow - แก้ไขด้วยตนเอง

**Steps:**
1. เปิด `tasks.md`
2. แก้ไข evidence contains/regex ให้ตรงกับที่มีในไฟล์
3. รัน verify อีกครั้ง

---

## Priority-Based Action Plan

Report จะจัดลำดับความสำคัญให้อัตโนมัติ:

### Priority 1: Critical Issues (ทำก่อน)

**ปัญหา:** Tasks ที่ mark [x] แต่ verification failed

**Action:**
1. ตรวจสอบว่าทำจริงหรือยัง
2. ถ้ายังไม่เสร็จ: Update checkbox เป็น [ ]
3. ถ้าเสร็จแล้ว: แก้ไข evidence หรือ implementation

**Workflow:**
- `/smartspec_sync_tasks_checkboxes` - Sync checkbox states
- `/smartspec_implement_tasks` - Complete implementation

---

### Priority 2: Missing Features (ทำต่อ)

**ปัญหา:** Tasks ที่ยังไม่มี implementation

**Action:**
1. Implement code ตาม tasks.md
2. เพิ่ม tests
3. Verify

**Workflow:**
- `/smartspec_implement_tasks` - Implement code
- `/smartspec_generate_tests` - Generate tests

---

### Priority 3: Symbol/Content Issues (แก้ไขรายละเอียด)

**ปัญหา:** มีไฟล์แต่ขาด symbol หรือ content

**Action:**
1. เพิ่ม symbol/content ที่ขาด
2. หรือแก้ไข evidence ให้ตรง

**Workflow:**
- `/smartspec_implement_tasks` - Add missing parts
- Manual edit - Update evidence

---

### Priority 4: Naming Issues (แก้ไขสุดท้าย)

**ปัญหา:** ชื่อไฟล์ไม่ตรงกับ evidence

**Action:**
1. แก้ไข evidence path
2. หรือ rename ไฟล์

**Workflow:**
- Manual edit - Update evidence or rename files

---

## Complete Workflow Sequence

### Scenario 1: เริ่มต้นจากศูนย์ (No implementation)

```bash
# 1. Verify current state
/smartspec_verify_tasks_progress_strict tasks.md

# Report shows: Not Implemented (Priority 2)

# 2. Implement tasks
/smartspec_implement_tasks tasks.md

# 3. Generate tests
/smartspec_generate_tests <module-path>

# 4. Run tests
pytest tests/

# 5. Verify again
/smartspec_verify_tasks_progress_strict tasks.md

# Report shows: Verified ✅
```

---

### Scenario 2: มี code แต่ไม่มี tests

```bash
# 1. Verify current state
/smartspec_verify_tasks_progress_strict tasks.md

# Report shows: Missing Tests (Priority 2)

# 2. Generate tests
/smartspec_generate_tests <module-path>

# 3. Run tests
pytest tests/

# 4. Verify again
/smartspec_verify_tasks_progress_strict tasks.md

# Report shows: Verified ✅
```

---

### Scenario 3: มี implementation แต่ checkbox ไม่ตรง

```bash
# 1. Verify current state
/smartspec_verify_tasks_progress_strict tasks.md

# Report shows: Critical Issues (Priority 1)
# - TASK-001: Marked [x] but failed
# - TASK-002: Marked [ ] but verified

# 2. Sync checkboxes
/smartspec_sync_tasks_checkboxes tasks.md --report-json <verify-report.json>

# 3. Verify again
/smartspec_verify_tasks_progress_strict tasks.md

# Report shows: Verified ✅
```

---

### Scenario 4: Naming issues

```bash
# 1. Verify current state
/smartspec_verify_tasks_progress_strict tasks.md

# Report shows: Naming Issues (Priority 4)
# - Similar file found: test_agent_wrapper.py

# 2. Manual fix (choose one):
# Option A: Update evidence in tasks.md
vim tasks.md  # Update evidence path

# Option B: Rename file
mv tests/ss_autopilot/test_agent_wrapper.py tests/ss_autopilot/test_checkpoint_manager.py

# 3. Verify again
/smartspec_verify_tasks_progress_strict tasks.md

# Report shows: Verified ✅
```

---

## Quick Reference Table

| Problem Category | Workflow | Manual Action | Priority |
|:---|:---|:---|:---:|
| **Not Implemented** | `/smartspec_implement_tasks` | Create files | 2 |
| **Missing Tests** | `/smartspec_generate_tests` | Write tests | 2 |
| **Missing Code** | `/smartspec_implement_tasks` | Implement code | 2 |
| **Naming Issues** | - | Update evidence or rename | 4 |
| **Symbol Issues** | `/smartspec_implement_tasks` | Add symbol or update evidence | 3 |
| **Content Issues** | `/smartspec_implement_tasks` | Add content or update evidence | 3 |
| **Critical (marked [x] but failed)** | `/smartspec_sync_tasks_checkboxes` | Complete implementation | 1 |

---

## Best Practices

### 1. Always Verify After Changes

```bash
# After any implementation
/smartspec_verify_tasks_progress_strict tasks.md
```

### 2. Fix Critical Issues First

ทำ Priority 1 ก่อนเสมอ (tasks ที่ mark [x] แต่ failed)

### 3. Use Workflow Automation

ใช้ workflows แทนการแก้ไขด้วยตนเอง เมื่อเป็นไปได้

### 4. Keep Evidence Accurate

อัปเดต evidence ให้ตรงกับ implementation จริง

### 5. Run Tests Before Verify

```bash
# Run tests first
pytest tests/

# Then verify
/smartspec_verify_tasks_progress_strict tasks.md
```

---

## Troubleshooting

### Q: Report แสดง "Not Implemented" แต่ไฟล์มีอยู่แล้ว

**A:** ตรวจสอบ:
1. Path ใน evidence ถูกต้องหรือไม่
2. Symbol/contains ตรงกับในไฟล์หรือไม่
3. ไฟล์อยู่ใน repo root หรือไม่

### Q: หลังจาก implement แล้ว verify ยัง fail

**A:** ตรวจสอบ:
1. Evidence syntax ถูกต้องหรือไม่
2. Path relative to repo root
3. Symbol/contains spelling ถูกต้อง
4. ไฟล์ถูก commit แล้วหรือยัง

### Q: Fuzzy matching แนะนำไฟล์ผิด

**A:** 
1. Ignore คำแนะนำ
2. ตรวจสอบไฟล์จริงด้วยตนเอง
3. แก้ไข evidence ให้ตรง

### Q: ควร fix naming issue หรือ implement ใหม่

**A:** ขึ้นอยู่กับ:
- ถ้าไฟล์ที่คล้ายกันเป็นไฟล์ที่ต้องการ → Fix naming
- ถ้าไฟล์ที่คล้ายกันไม่เกี่ยวข้อง → Implement ใหม่

---

## Related Workflows

### Core Workflows

1. **`/smartspec_verify_tasks_progress_strict`**
   - Verify task progress with evidence
   - Generate detailed report

2. **`/smartspec_implement_tasks`**
   - Implement code from tasks.md
   - Create files and add code

3. **`/smartspec_generate_tests`**
   - Generate test artifacts
   - Create test templates

4. **`/smartspec_sync_tasks_checkboxes`**
   - Sync checkbox states
   - Update tasks.md based on verification

### Supporting Workflows

5. **`/smartspec_test_suite_runner`**
   - Run test suite
   - Generate test report

6. **`/smartspec_test_report_analyzer`**
   - Analyze test results
   - Identify failures

7. **`/smartspec_hotfix_assistant`**
   - Quick fixes for critical issues
   - Emergency patches

---

## Summary

**Decision Tree:**

```
Verify Report
    │
    ├─ Priority 1: Critical (marked [x] but failed)
    │   └─> /smartspec_sync_tasks_checkboxes
    │       OR /smartspec_implement_tasks (complete)
    │
    ├─ Priority 2: Not Implemented / Missing Tests / Missing Code
    │   ├─> Not Implemented
    │   │   └─> /smartspec_implement_tasks
    │   ├─> Missing Tests
    │   │   └─> /smartspec_generate_tests
    │   └─> Missing Code
    │       └─> /smartspec_implement_tasks
    │
    ├─ Priority 3: Symbol/Content Issues
    │   └─> /smartspec_implement_tasks (add missing)
    │       OR Manual edit (update evidence)
    │
    └─ Priority 4: Naming Issues
        └─> Manual edit (update evidence or rename)
```

**Key Takeaway:**
- **Not Implemented / Missing Code** → `/smartspec_implement_tasks`
- **Missing Tests** → `/smartspec_generate_tests`
- **Critical Issues** → `/smartspec_sync_tasks_checkboxes`
- **Naming/Symbol/Content** → Manual edit หรือ `/smartspec_implement_tasks`

---

**Version:** 1.0.0  
**Last Updated:** 2025-12-26  
**Status:** Ready for Use ✅
