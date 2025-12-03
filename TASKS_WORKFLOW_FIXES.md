# Tasks Workflow Fixes - Summary

## สรุปการแก้ไข

### ปัญหาที่พบ (จากไฟล์ที่ user แนบ)

1. **ความไม่สมบูรณ์ (~45% coverage)**
   - Credit core flows: 20%
   - Payment flows: 10%
   - Billing system: 10%
   - Cost analytics: 5%
   - Security: 30%
   - APIs: 10%
   - DB schema: 25%

2. **โครงสร้างไม่ชัดเจน**
   - ไม่มี checkbox format `- [ ]`
   - ไม่มี Task ID (T001, T002)
   - ไม่มี time estimates
   - ไม่มี subtasks
   - ไม่มีการป้องกัน context overflow

3. **Missing Components**
   - Business logic ไม่ครบ
   - API endpoints ขาดหาย
   - Security features ไม่สมบูรณ์
   - Database schema ไม่ครบ
   - Testing ไม่ครอบคลุม

---

## การแก้ไขที่ทำ

### 1. เพิ่ม Complete Coverage Requirements (Section 4.2.1)

**เพิ่ม checklist สำหรับตรวจสอบความครบถ้วน:**
- Business Logic (100%)
- API Endpoints (100%)
- Security (100%)
- Database (100%)
- Testing (100%)

**Validation process:**
1. Read SPEC completely
2. List ALL requirements
3. Map each requirement to task(s)
4. Verify no gaps
5. Add missing tasks if needed

**Rule:** If coverage < 90%, STOP and add missing tasks

### 2. ปรับปรุง Phase Structure (Section 4.2)

**เพิ่ม Standard 10-Phase Structure:**

1. Phase 1: Foundation & Setup
2. Phase 2: Database Schema & Core Models
3. Phase 3: Authentication & Authorization
4. Phase 4: Credit Management Core
5. Phase 5: Payment Integration
6. Phase 6: Billing System
7. Phase 7: Cost Management & Analytics
8. Phase 8: Security & Compliance
9. Phase 9: API Layer & Integration
10. Phase 10: Testing & Deployment

**Rules:**
- 10-task maximum per phase (MANDATORY)
- 5-task minimum per phase
- Clear logical grouping

### 3. เพิ่ม Task Format with Checkboxes (Section 7.2)

**New format:**
```markdown
- [ ] **T00X: [Task Title]** (Xh)

  **Description:**
  [Concrete, actionable details]
  
  **Subtasks:**
  - [ ] T00X.1: [Subtask 1] (2h)
  - [ ] T00X.2: [Subtask 2] (3h)
  - [ ] T00X.3: [Subtask 3] (2h)
  
  **Acceptance Criteria:**
  - [ ] [Criterion 1]
  - [ ] [Criterion 2]
  - [ ] Tests pass with >80% coverage
  - [ ] No TypeScript errors
  - [ ] Documentation updated
```

### 4. เพิ่ม Task Sizing Rules (Section 7.2.1)

**🚨 MANDATORY: Prevent Context Overflow**

**Small Task (2-4h):**
- Single file/function
- Output: <200 lines
- Context: <5K tokens
- Subtasks: 0-2

**Medium Task (4-8h):**
- 2-3 files
- Output: 200-500 lines
- Context: 5-10K tokens
- Subtasks: 2-4 (REQUIRED)

**Large Task (8-16h):**
- Multiple components
- Output: 500-1000 lines
- Context: 10-20K tokens
- Subtasks: 4-6 (MANDATORY)

**❌ TOO LARGE (>16h):**
- NOT ALLOWED
- MUST split into 2+ tasks

**Context Overflow Prevention Checklist:**
- [ ] Task requires reading <5 files
- [ ] Task description <500 words
- [ ] Task has <6 subtasks
- [ ] Task output <1000 lines
- [ ] Task can be completed without reading entire codebase

### 5. เพิ่ม Subtask Breakdown Rules (Section 7.2.2)

**When to create subtasks:**
1. Task > 8h (MANDATORY)
2. Task involves >3 files (MANDATORY)
3. Task has multiple logical steps (RECOMMENDED)
4. Task requires multiple skills (RECOMMENDED)

**Subtask format:**
```markdown
- [ ] T00X.1: [Specific, actionable name] (2h)
  - Description: [Clear, focused description]
  - Files: `path/to/file.ts`
  - Output: [What this produces]
```

**Subtask sizing:**
- Each: 1-4h
- Total per task: 2-6
- If >6 needed: Split parent task

---

## ผลลัพธ์ที่คาดหวัง

### Before (ปัญหา)
- ❌ Coverage ~45%
- ❌ ไม่มี checkbox
- ❌ ไม่มี Task ID
- ❌ ไม่มี subtasks
- ❌ Context overflow
- ❌ งานใหญ่เกินไป
- ❌ คลุมเครือ

### After (แก้ไขแล้ว)
- ✅ Coverage 100% (enforced)
- ✅ Checkbox format `- [ ]`
- ✅ Task ID (T001-T100)
- ✅ Time estimates (Xh)
- ✅ Subtasks (2-6 per task)
- ✅ Context overflow prevention
- ✅ Task sizing rules (2-16h)
- ✅ Clear, actionable descriptions
- ✅ 10-phase structure
- ✅ Complete validation checklist

---

## ตัวอย่าง Task ที่ถูกต้อง

```markdown
## Phase 4: Credit Management Core (Week 4-5)

- [ ] **T031: Implement Credit Reserve Flow** (8h)

  **Description:**
  Implement the credit reservation flow that temporarily locks user credits
  for pending operations. Ensures credits cannot be double-spent while
  waiting for transaction confirmation.
  
  **Subtasks:**
  - [ ] T031.1: Create reserve() method in CreditService (2h)
    - Files: `src/services/credit.service.ts`
    - Logic: Check balance, create reservation, update reserved_balance
  - [ ] T031.2: Implement reservation timeout worker (2h)
    - Files: `src/workers/credit-reservation-timeout.worker.ts`
    - Logic: BullMQ job to auto-release expired reservations
  - [ ] T031.3: Add reserve API endpoint (2h)
    - Files: `src/routes/credit.routes.ts`, `src/controllers/credit.controller.ts`
    - Endpoint: POST /api/v1/credit/reserve
  - [ ] T031.4: Write tests (2h)
    - Files: `tests/credit-reserve.test.ts`
    - Coverage: Happy path, insufficient balance, timeout, idempotency
  
  **Files:**
  - CREATE: `src/services/credit.service.ts` (~150 lines - SMALL)
  - CREATE: `src/workers/credit-reservation-timeout.worker.ts` (~80 lines - SMALL)
  - EDIT: `src/routes/credit.routes.ts` (add 25 lines - SMALL)
  - CREATE: `tests/credit-reserve.test.ts` (~200 lines - MEDIUM)
  
  **Dependencies:**
  - T021: RBAC middleware (must complete)
  - T011: Credit balance table (must complete)
  - T004: BullMQ setup (must complete)
  
  **Acceptance Criteria:**
  - [ ] Reserve API endpoint implemented
  - [ ] Reserved balance tracked separately
  - [ ] Automatic release after timeout
  - [ ] Idempotency key support
  - [ ] Tests pass with >85% coverage
  - [ ] No TypeScript errors
  - [ ] API documentation updated
  
  **Validation:**
  ```bash
  tsc --noEmit
  npm test -- tests/credit-reserve.test.ts
  npm run lint
  ```
  
  **Expected Outcome:**
  Users can reserve credits for pending operations. System prevents
  double-spending. Expired reservations auto-release.
```

---

## สรุป

การแก้ไขครั้งนี้ทำให้ generate tasks workflow:

1. **สมบูรณ์:** Coverage 100% ของ SPEC requirements
2. **ชัดเจน:** Checkbox format, Task ID, time estimates
3. **ปลอดภัย:** Context overflow prevention
4. **ใช้งานได้:** Subtasks สำหรับงานใหญ่
5. **มาตรฐาน:** 10-phase structure
6. **ตรวจสอบได้:** Validation checklist ครบถ้วน

ผลลัพธ์: tasks.md ที่สร้างจะมีคุณภาพสูง พร้อมใช้งานกับ Kilo Code และป้องกัน infinite loops
