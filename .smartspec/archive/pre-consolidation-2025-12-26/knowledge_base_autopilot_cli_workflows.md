# Knowledge Base: Autopilot CLI Workflows

**Version:** 1.0.0  
**Date:** 2025-12-26  
**Status:** Production Ready

---

## Overview

Autopilot workflows เป็นชุดคำสั่ง CLI ที่ใช้ Multi-Agent System เพื่อช่วยในการพัฒนา SmartSpec โดยอัตโนมัติ ประกอบด้วย 3 workflows หลัก:

1. **`/autopilot_run`** - รับคำแนะนำ workflow ถัดไปจาก Orchestrator Agent
2. **`/autopilot_status`** - ตรวจสอบสถานะและความคืบหน้าของ spec
3. **`/autopilot_ask`** - ถามคำถามด้วยภาษาธรรมชาติ

---

## 1. /autopilot_run - Workflow Recommendation

### คำอธิบาย

ระบบ Orchestrator Agent ที่วิเคราะห์สถานะปัจจุบันของ spec และแนะนำ workflow ถัดไปที่ควรรัน พร้อมคำสั่งที่พร้อมใช้งาน

### วิธีใช้งาน

#### Syntax
```bash
/autopilot_run.md <spec-id> [--auto] --platform <kilo|antigravity|claude>
```

#### Parameters
- `<spec-id>` (required) - Spec ID ที่ต้องการวิเคราะห์
- `--auto` (optional) - รันคำสั่งทันทีโดยไม่ต้องยืนยัน
- `--platform` (required) - Platform ที่ใช้งาน (kilo, antigravity, claude)

---

### ตัวอย่างการใช้งาน

#### Example 1: รับคำแนะนำ workflow ถัดไป

**สถานการณ์:** มี spec.md และ plan.md แล้ว ต้องการรู้ว่าควรทำอะไรต่อ

```bash
/autopilot_run.md spec-core-001-authentication --platform kilo
```

**Output:**
```
🤖 Orchestrator Agent

## Recommendation

**Workflow:** smartspec_generate_tasks  
**Reason:** Plan exists but tasks.md not found - need to generate task list  
**Priority:** high  
**Estimated Time:** 15 minutes

## Current State

- ✅ spec.md exists
- ✅ plan.md exists
- ❌ tasks.md not found

## Next Step

Generate task list from plan.md to start implementation.

## 🚀 Command

```bash
/smartspec_generate_tasks.md \
  specs/spec-core-001-authentication/plan.md \
  --apply \
  --out specs/spec-core-001-authentication/tasks.md \
  --json \
  --platform kilo
```

**Run this command?** [y/N]
```

**การใช้งาน:** กด `y` เพื่อรันคำสั่งทันที หรือ copy คำสั่งไปรันเองภายหลัง

---

#### Example 2: Auto-continue mode (รันทันทีไม่ต้องยืนยัน)

**สถานการณ์:** ต้องการให้ระบบรันคำสั่งทันทีโดยไม่ถาม

```bash
/autopilot_run.md spec-core-001-authentication --auto --platform kilo
```

**Output:**
```
🤖 Orchestrator Agent

Workflow: smartspec_implement_tasks
Reason: Continue implementation (5/12 tasks completed, 42%)

✅ Command ready to execute!

/smartspec_implement_tasks.md \
  specs/spec-core-001-authentication/tasks.md \
  --apply \
  --out .spec/reports/implement-tasks/spec-core-001-authentication \
  --json \
  --platform kilo

⏳ Executing...
```

**คำเตือน:** ใช้ `--auto` อย่างระมัดระวัง เพราะจะรันคำสั่งทันทีโดยไม่ถาม

---

#### Example 3: เริ่มต้นจากศูนย์ (ยังไม่มี spec.md)

**สถานการณ์:** สร้าง spec ใหม่ ยังไม่มีไฟล์อะไรเลย

```bash
/autopilot_run.md spec-core-003-new-feature --platform kilo
```

**Output:**
```
🤖 Orchestrator Agent

## Recommendation

**Workflow:** smartspec_generate_spec  
**Reason:** No spec.md found - need to generate specification first  
**Priority:** critical  
**Estimated Time:** 30 minutes

## Current State

- ❌ spec.md not found
- ❌ plan.md not found
- ❌ tasks.md not found

## Next Step

Generate specification document first.

## 💡 Tips

- Start with a clear feature description
- Include user stories and acceptance criteria
- Define APIs and data models

## 🚀 Command

```bash
/smartspec_generate_spec.md \
  "Create authentication system with JWT tokens, user registration, login, logout, and password reset" \
  --out specs/spec-core-003-new-feature/spec.md \
  --json \
  --platform kilo
```

**Run this command?** [y/N]
```

---

#### Example 4: กำลัง implement อยู่ (tasks.md มี checkboxes)

**สถานการณ์:** implement tasks ไปแล้ว 5/12 tasks

```bash
/autopilot_run.md spec-core-001-authentication --platform kilo
```

**Output:**
```
🤖 Orchestrator Agent

## Recommendation

**Workflow:** smartspec_implement_tasks  
**Reason:** Continue implementation (5/12 tasks completed, 42%)  
**Priority:** high  
**Estimated Time:** 140 minutes

## Current State

- ✅ spec.md exists
- ✅ plan.md exists
- ✅ tasks.md exists (12 tasks)
- ⚠️  Implementation in progress (5/12 completed)

## Next Step

Continue implementing remaining 7 tasks.

## ⚠️  Warnings

- Checkboxes might not match actual code (consider syncing first)

## 💡 Tips

- Run sync_tasks_checkboxes if unsure about progress
- Focus on one task at a time
- Test after each task

## 🚀 Command

```bash
/smartspec_implement_tasks.md \
  specs/spec-core-001-authentication/tasks.md \
  --apply \
  --out .spec/reports/implement-tasks/spec-core-001-authentication \
  --json \
  --platform kilo
```

**Run this command?** [y/N]
```

---

### Decision Logic (ตรรกะการตัดสินใจ)

Orchestrator Agent ใช้ state machine ในการตัดสินใจ:

```
START
  ↓
has_spec? → NO → recommend: smartspec_generate_spec
  ↓ YES
has_plan? → NO → recommend: smartspec_generate_plan
  ↓ YES
has_tasks? → NO → recommend: smartspec_generate_tasks
  ↓ YES
implementation_status?
  ↓ NOT_STARTED → recommend: smartspec_implement_tasks
  ↓ IN_PROGRESS
    ↓
  needs_sync? → YES → recommend: smartspec_sync_tasks_checkboxes
    ↓ NO
  completion_rate < 100%? → YES → recommend: smartspec_implement_tasks
    ↓ NO (100%)
  has_tests? → NO → recommend: smartspec_generate_tests
    ↓ YES
  tests_passing? → NO → recommend: fix_tests
    ↓ YES
  has_docs? → NO → recommend: smartspec_generate_docs
    ↓ YES
  deployed? → NO → recommend: smartspec_deploy
    ↓ YES
  DONE ✅
```

---

### Use Cases

#### Use Case 1: ไม่รู้ว่าควรทำอะไรต่อ
```bash
/autopilot_run.md spec-core-001 --platform kilo
```
→ ได้คำแนะนำ workflow ถัดไปพร้อมเหตุผล

#### Use Case 2: Continuous Development
```bash
/autopilot_run.md spec-core-001 --auto --platform kilo
```
→ รัน workflow ถัดไปทันทีโดยอัตโนมัติ

#### Use Case 3: เริ่มต้น spec ใหม่
```bash
/autopilot_run.md spec-new-feature --platform kilo
```
→ แนะนำให้เริ่มจาก generate_spec

---

## 2. /autopilot_status - Status Query

### คำอธิบาย

ตรวจสอบสถานะและความคืบหน้าของ spec โดย Status Agent พร้อม progress bar, tasks ที่เหลือ, และคำแนะนำ

### วิธีใช้งาน

#### Syntax
```bash
/autopilot_status.md <spec-id> [--query <question>] --platform <kilo|antigravity|claude>
```

#### Parameters
- `<spec-id>` (required) - Spec ID ที่ต้องการตรวจสอบ
- `--query` (optional) - คำถามเฉพาะเจาะจง
- `--platform` (required) - Platform ที่ใช้งาน

---

### ตัวอย่างการใช้งาน

#### Example 1: Full status report

**สถานการณ์:** ต้องการดูสถานะโดยรวมของ spec

```bash
/autopilot_status.md spec-core-001-authentication --platform kilo
```

**Output:**
```
📊 Status Agent

## ความคืบหน้า

**Tasks ที่เสร็จแล้ว:** 5 / 12 (42%)

████████░░░░░░░░░░░░ 42%

## Tasks ที่เหลือ

- Task 6: Implement logout API
- Task 7: Add password reset endpoint
- Task 8: Create user profile API
- Task 9: Implement JWT refresh token
- Task 10: Add rate limiting
- Task 11: Write integration tests
- Task 12: Update API documentation

## Next Steps

1. Continue implementing remaining APIs (Tasks 6-9)
2. Add security features (Task 10)
3. Write tests (Task 11)
4. Update documentation (Task 12)

## Estimated Time

⏱️  **Remaining:** ~140 minutes (20 min/task × 7 tasks)

## ⚠️  Warnings

- No tests written yet (Task 11 pending)
- Documentation needs update (Task 12 pending)

## 💡 Recommendations

- Focus on core APIs first (Tasks 6-9)
- Add tests incrementally after each API
- Update docs as you go
```

---

#### Example 2: Query เฉพาะเจาะจง

**สถานการณ์:** ต้องการถามคำถามเฉพาะ

```bash
/autopilot_status.md spec-core-001-authentication --query "เหลืออะไรบ้าง?" --platform kilo
```

**Output:**
```
📊 Status Agent

## Tasks ที่เหลือ (7 tasks)

1. **Task 6:** Implement logout API
   - Endpoint: POST /api/auth/logout
   - Clear JWT token
   - Return success response

2. **Task 7:** Add password reset endpoint
   - Endpoint: POST /api/auth/reset-password
   - Send reset email
   - Validate reset token

3. **Task 8:** Create user profile API
   - Endpoint: GET /api/user/profile
   - Return user info
   - Require authentication

... (และอีก 4 tasks)

## Summary

เหลืออีก **7 tasks** (58%) ประมาณ **140 นาที**
```

---

#### Example 3: ตรวจสอบ spec ที่เสร็จแล้ว

**สถานการณ์:** spec implement เสร็จแล้ว ต้องการดูสถานะ

```bash
/autopilot_status.md spec-core-002-authorization --platform kilo
```

**Output:**
```
📊 Status Agent

## ความคืบหน้า

**Tasks ที่เสร็จแล้ว:** 15 / 15 (100%)

████████████████████ 100% ✅

## Status

✅ **All tasks completed!**

## Verification

- ✅ All checkboxes marked
- ✅ Implementation verified
- ✅ Tests passing
- ✅ Documentation updated

## Next Steps

1. Run final verification: `/smartspec_verify_tasks_progress_strict.md`
2. Deploy to staging
3. Run E2E tests
4. Deploy to production

## 🎉 Congratulations!

Spec is ready for deployment!
```

---

#### Example 4: ตรวจสอบหลาย specs พร้อมกัน

**สถานการณ์:** ต้องการดูสถานะของหลาย specs

```bash
# Spec 1
/autopilot_status.md spec-core-001 --platform kilo

# Spec 2
/autopilot_status.md spec-core-002 --platform kilo

# Spec 3
/autopilot_status.md spec-feat-001 --platform kilo
```

**Output (สรุป):**
```
spec-core-001: 42% (5/12 tasks) - In Progress
spec-core-002: 100% (15/15 tasks) - Completed ✅
spec-feat-001: 0% (0/8 tasks) - Not Started
```

---

### Use Cases

#### Use Case 1: Daily standup
```bash
/autopilot_status.md spec-core-001 --platform kilo
```
→ ดูความคืบหน้าและ tasks ที่เหลือ

#### Use Case 2: Before starting work
```bash
/autopilot_status.md spec-core-001 --query "ควรทำอะไรต่อ?" --platform kilo
```
→ ได้คำแนะนำว่าควรเริ่มจาก task ไหน

#### Use Case 3: Project review
```bash
/autopilot_status.md spec-core-001 --platform kilo
```
→ ดูภาพรวมของโปรเจค

---

## 3. /autopilot_ask - Natural Language Query

### คำอธิบาย

ถามคำถามด้วยภาษาธรรมชาติ (ไทยหรืออังกฤษ) และ Intent Parser Agent จะ route ไปยัง agent ที่เหมาะสมโดยอัตโนมัติ

### วิธีใช้งาน

#### Syntax
```bash
/autopilot_ask.md "<your question>" --platform <kilo|antigravity|claude>
```

#### Parameters
- `"<question>"` (required) - คำถามเป็นภาษาธรรมชาติ
- `--platform` (required) - Platform ที่ใช้งาน

---

### ตัวอย่างการใช้งาน

#### Example 1: ถามความคืบหน้า

**คำถาม:** "spec-core-001 งานถึงไหนแล้ว?"

```bash
/autopilot_ask.md "spec-core-001 งานถึงไหนแล้ว?" --platform kilo
```

**Output:**
```
💬 Intent Parser Agent

**Type:** status_query  
**Target Agent:** status  
**Confidence:** 95%  
**Spec ID:** spec-core-001

🔀 Routing to: Status Agent

📊 Status Agent

**Tasks ที่เสร็จแล้ว:** 5 / 12 (42%)

████████░░░░░░░░░░░░ 42%

เหลืออีก 7 tasks (ประมาณ 140 นาที)
```

---

#### Example 2: ถามว่าควรทำอะไรต่อ

**คำถาม:** "spec-core-001 ควรทำอะไรต่อ?"

```bash
/autopilot_ask.md "spec-core-001 ควรทำอะไรต่อ?" --platform kilo
```

**Output:**
```
💬 Intent Parser Agent

**Type:** recommendation_query  
**Target Agent:** orchestrator  
**Confidence:** 90%  
**Spec ID:** spec-core-001

🔀 Routing to: Orchestrator Agent

🤖 Orchestrator Agent

## Recommendation

**Workflow:** smartspec_implement_tasks  
**Reason:** Continue implementation (5/12 tasks, 42%)

## Command

```bash
/smartspec_implement_tasks.md \
  specs/spec-core-001/tasks.md \
  --apply \
  --platform kilo
```
```

---

#### Example 3: ถามเกี่ยวกับ spec ที่ยังไม่มี

**คำถาม:** "spec-new-feature มีหรือยัง?"

```bash
/autopilot_ask.md "spec-new-feature มีหรือยัง?" --platform kilo
```

**Output:**
```
💬 Intent Parser Agent

**Type:** existence_query  
**Target Agent:** status  
**Confidence:** 85%  
**Spec ID:** spec-new-feature

🔀 Routing to: Status Agent

📊 Status Agent

❌ **Spec not found:** spec-new-feature

**Did you mean:**
- spec-feat-001-user-profile
- spec-feat-002-notifications

**Or create new spec:**

```bash
/smartspec_generate_spec.md \
  "your feature description" \
  --out specs/spec-new-feature/spec.md \
  --platform kilo
```
```

---

#### Example 4: ถามภาษาอังกฤษ

**คำถาม:** "What's the progress of spec-core-001?"

```bash
/autopilot_ask.md "What's the progress of spec-core-001?" --platform kilo
```

**Output:**
```
💬 Intent Parser Agent

**Type:** status_query  
**Target Agent:** status  
**Confidence:** 95%  
**Spec ID:** spec-core-001

🔀 Routing to: Status Agent

📊 Status Agent

**Completed Tasks:** 5 / 12 (42%)

████████░░░░░░░░░░░░ 42%

7 tasks remaining (~140 minutes)
```

---

#### Example 5: ถามคำถามซับซ้อน

**คำถาม:** "spec-core-001 เหลืออะไรบ้าง และควรเริ่มจากไหน?"

```bash
/autopilot_ask.md "spec-core-001 เหลืออะไรบ้าง และควรเริ่มจากไหน?" --platform kilo
```

**Output:**
```
💬 Intent Parser Agent

**Type:** complex_query (status + recommendation)  
**Target Agents:** status, orchestrator  
**Confidence:** 80%  
**Spec ID:** spec-core-001

🔀 Routing to: Status Agent → Orchestrator Agent

📊 Status Agent

**Tasks ที่เหลือ:**
- Task 6: Implement logout API
- Task 7: Add password reset
- Task 8: Create user profile API
... (และอีก 4 tasks)

🤖 Orchestrator Agent

**คำแนะนำ:** เริ่มจาก Task 6 (Implement logout API) เพราะเป็น core feature และไม่ depend กับ tasks อื่น

**Command:**

```bash
/smartspec_implement_tasks.md \
  specs/spec-core-001/tasks.md \
  --apply \
  --platform kilo
```
```

---

### Supported Query Types

Intent Parser Agent รองรับคำถามหลายประเภท:

#### 1. Status Queries (ถามความคืบหน้า)
- "งานถึงไหนแล้ว?"
- "progress เท่าไหร่?"
- "What's the status?"
- "เหลืออะไรบ้าง?"

→ Routes to: **Status Agent**

#### 2. Recommendation Queries (ถามคำแนะนำ)
- "ควรทำอะไรต่อ?"
- "What should I do next?"
- "เริ่มจากไหนดี?"
- "Next step?"

→ Routes to: **Orchestrator Agent**

#### 3. Existence Queries (ถามว่ามีหรือไม่)
- "มี spec นี้หรือยัง?"
- "Does this spec exist?"
- "หา spec ไม่เจอ"

→ Routes to: **Status Agent**

#### 4. Complex Queries (คำถามซับซ้อน)
- "เหลืออะไรบ้าง และควรเริ่มจากไหน?"
- "Show progress and next steps"

→ Routes to: **Multiple Agents**

---

### Use Cases

#### Use Case 1: Quick status check
```bash
/autopilot_ask.md "spec-core-001 งานถึงไหนแล้ว?" --platform kilo
```
→ ได้ progress และ tasks ที่เหลือ

#### Use Case 2: Get recommendation
```bash
/autopilot_ask.md "spec-core-001 ควรทำอะไรต่อ?" --platform kilo
```
→ ได้คำแนะนำ workflow ถัดไป

#### Use Case 3: Find spec
```bash
/autopilot_ask.md "หา spec เกี่ยวกับ authentication" --platform kilo
```
→ ค้นหา spec ที่เกี่ยวข้อง

---

## Workflow Comparison

| Feature | /autopilot_run | /autopilot_status | /autopilot_ask |
|:---|:---:|:---:|:---:|
| **Purpose** | Recommend next workflow | Check progress | Natural language query |
| **Input** | Spec ID | Spec ID | Natural language question |
| **Output** | Workflow command | Progress report | Routed answer |
| **Agent** | Orchestrator | Status | Intent Parser → Any |
| **Use When** | Don't know what to do next | Want to check progress | Want to ask freely |
| **Auto-execute** | Yes (with `--auto`) | No | No |
| **Language** | English only | Thai/English output | Thai/English input |

---

## Best Practices

### 1. เมื่อไหร่ควรใช้ workflow ไหน

**ใช้ `/autopilot_run` เมื่อ:**
- ✅ ไม่รู้ว่าควรทำอะไรต่อ
- ✅ ต้องการคำสั่งที่พร้อมรัน
- ✅ ต้องการ auto-execute

**ใช้ `/autopilot_status` เมื่อ:**
- ✅ ต้องการดูความคืบหน้า
- ✅ ต้องการดู tasks ที่เหลือ
- ✅ ต้องการประมาณเวลา

**ใช้ `/autopilot_ask` เมื่อ:**
- ✅ ต้องการถามคำถามอิสระ
- ✅ ไม่แน่ใจว่าควรใช้ workflow ไหน
- ✅ ต้องการคำตอบแบบ conversational

### 2. Workflow Combination Patterns

#### Pattern 1: Daily Development Flow
```bash
# 1. Check status
/autopilot_status.md spec-core-001 --platform kilo

# 2. Get recommendation
/autopilot_run.md spec-core-001 --platform kilo

# 3. Execute (if recommended)
# ... run the recommended workflow ...

# 4. Check status again
/autopilot_status.md spec-core-001 --platform kilo
```

#### Pattern 2: Natural Language Flow
```bash
# 1. Ask about progress
/autopilot_ask.md "spec-core-001 งานถึงไหนแล้ว?" --platform kilo

# 2. Ask what to do next
/autopilot_ask.md "spec-core-001 ควรทำอะไรต่อ?" --platform kilo

# 3. Execute recommended workflow
# ... run the workflow ...
```

#### Pattern 3: Continuous Development
```bash
# Loop until done
while true; do
  /autopilot_run.md spec-core-001 --auto --platform kilo
  sleep 60  # Wait 1 minute between runs
done
```

### 3. Tips & Tricks

#### Tip 1: Use `--auto` carefully
```bash
# ❌ Don't use --auto blindly
/autopilot_run.md spec-core-001 --auto --platform kilo

# ✅ Check status first, then use --auto
/autopilot_status.md spec-core-001 --platform kilo
/autopilot_run.md spec-core-001 --auto --platform kilo
```

#### Tip 2: Combine with other workflows
```bash
# Check status
/autopilot_status.md spec-core-001 --platform kilo

# Sync checkboxes if needed
/smartspec_sync_tasks_checkboxes.md specs/spec-core-001/tasks.md --apply --platform kilo

# Get recommendation
/autopilot_run.md spec-core-001 --platform kilo
```

#### Tip 3: Use natural language for complex queries
```bash
# Instead of multiple commands
/autopilot_status.md spec-core-001 --platform kilo
/autopilot_run.md spec-core-001 --platform kilo

# Use single natural language query
/autopilot_ask.md "spec-core-001 เหลืออะไรบ้าง และควรทำอะไรต่อ?" --platform kilo
```

---

## Troubleshooting

### Issue 1: "Spec not found"

**Problem:** Autopilot ไม่เจอ spec

**Solution:**
```bash
# Check if spec exists
ls -la specs/spec-core-001/

# If not exists, create it
/smartspec_generate_spec.md "your feature" --platform kilo
```

### Issue 2: "Recommendation doesn't make sense"

**Problem:** Orchestrator แนะนำ workflow ที่ไม่เหมาะสม

**Solution:**
```bash
# Sync checkboxes first
/smartspec_sync_tasks_checkboxes.md specs/spec-core-001/tasks.md --apply --platform kilo

# Then get recommendation again
/autopilot_run.md spec-core-001 --platform kilo
```

### Issue 3: "Intent Parser confidence low"

**Problem:** Intent Parser ไม่แน่ใจว่าคำถามหมายถึงอะไร (confidence < 60%)

**Solution:**
```bash
# Be more specific
/autopilot_ask.md "spec-core-001 tasks ที่เสร็จแล้วกี่ tasks?" --platform kilo

# Or use direct workflow
/autopilot_status.md spec-core-001 --platform kilo
```

---

## Configuration

### smartspec.config.yaml

```yaml
autopilot:
  # Orchestrator Agent
  orchestrator:
    enabled: true
    auto_execute: false  # Don't auto-execute by default
    confidence_threshold: 0.7
  
  # Status Agent
  status:
    enabled: true
    show_progress_bar: true
    show_estimated_time: true
  
  # Intent Parser Agent
  intent_parser:
    enabled: true
    confidence_threshold: 0.6
    supported_languages: [th, en]
    fallback_agent: status
```

---

## API Reference

### Orchestrator Agent
- **Input:** Spec ID
- **Output:** Workflow recommendation + command
- **Decision:** Based on spec state (spec/plan/tasks/implementation)

### Status Agent
- **Input:** Spec ID + optional query
- **Output:** Progress report + tasks + recommendations
- **Data:** From tasks.md checkboxes

### Intent Parser Agent
- **Input:** Natural language question
- **Output:** Routed to appropriate agent
- **Routing:** Based on intent classification (status/recommendation/existence)

---

## Related Documentation

- `knowledge_base_autopilot_workflows.md` - Autopilot execution features
- `.smartspec/workflows/autopilot_run.md` - Full workflow documentation
- `.smartspec/workflows/autopilot_status.md` - Full workflow documentation
- `.smartspec/workflows/autopilot_ask.md` - Full workflow documentation

---

**Last Updated:** 2025-12-26  
**Version:** 1.0.0  
**Status:** Production Ready ✅
