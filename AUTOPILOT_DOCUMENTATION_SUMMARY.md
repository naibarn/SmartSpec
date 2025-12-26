# SmartSpec Autopilot Documentation Summary

**Date:** 2025-12-26  
**Version:** 1.0.0  
**Status:** ✅ Complete

---

## Overview

เอกสารนี้สรุปการสร้าง knowledge base และการอัปเดต system prompt สำหรับ SmartSpec Autopilot workflows ที่เพิ่มเข้ามาในวันนี้

---

## Files Created/Updated

### 1. knowledge_base_autopilot_workflows.md (NEW)
**Path:** `.smartspec/knowledge_base_autopilot_workflows.md`  
**Size:** 15,234 bytes  
**Status:** ✅ Created

**เนื้อหา:**
- **Overview:** แนะนำ SmartSpec Autopilot และ architecture
- **Core Features:**
  1. Parallel Execution - รัน tasks พร้อมกัน
  2. Checkpointing - บันทึกและกู้คืน workflow state
  3. Progress Streaming - ติดตาม progress แบบ real-time
  4. Human-in-the-Loop - รอ human input/approval
  5. Dynamic Routing - route ไปยัง agents ที่เหมาะสม
  6. Agent Wrapper - เพิ่ม features (logging, caching, rate limiting)

- **Integration Patterns:**
  - Long-running workflow with checkpoints
  - Parallel execution with progress tracking
  - Human-in-the-loop approval

- **CLI Integration:**
  - `/autopilot_run` - รัน workflow พร้อม autopilot features
  - `/autopilot_status` - ตรวจสอบ workflow status
  - `/autopilot_ask` - ตอบ human interrupts

- **Configuration:** ตัวอย่าง `smartspec.config.yaml`
- **Best Practices:** แนวทางการใช้งานแต่ละ feature
- **Troubleshooting:** แก้ปัญหาที่พบบ่อย
- **Migration Guide:** จาก manual workflows ไปยัง autopilot

---

### 2. system_prompt_smartspec.md (UPDATED)
**Path:** `.smartspec/system_prompt_smartspec.md`  
**Version:** v6.5.0 (จาก v6.4.0)  
**Size:** 7,096 bytes / 8,000 limit (88.7%) ✅  
**Status:** ✅ Updated

**การเปลี่ยนแปลง:**

#### Section 0: Knowledge sources
- เพิ่ม `knowledge_base_autopilot_workflows.md` เป็น source #3

#### Section 6: Autopilot workflows (NEW)
เพิ่ม section ใหม่ทั้งหมดเกี่ยวกับ autopilot:

**6.1) Autopilot Run**
```bash
/autopilot_run <workflow> <args> [--checkpoint] [--parallel] [--max-workers N] [--human-approval]
```

**Flags:**
- `--checkpoint` - Enable checkpointing
- `--parallel` - Enable parallel execution
- `--max-workers N` - Set parallel workers
- `--resume CHECKPOINT_ID` - Resume from checkpoint
- `--human-approval` - Require human approval

**6.2) Autopilot Status**
```bash
/autopilot_status <workflow-name> [checkpoint-id]
```

**6.3) Autopilot Ask**
```bash
/autopilot_ask <interrupt-id> --action <approve|reject|modify> [--modifications <json>]
```

**6.4) When to use Autopilot**
- Long-running workflows (>5 min) → `--checkpoint`
- Multi-task workflows (>10 tasks) → `--parallel`
- Critical operations → `--human-approval`

#### Section 7: Progress/status questions
- เพิ่ม routing ไปยัง `/autopilot_status` สำหรับ autopilot workflows

#### Section 8: Context Detection
- เพิ่มการตรวจสอบ active checkpoints ใน `.spec/checkpoints.db`

#### Section 11: New features
- เพิ่มคำแนะนำให้ใช้ `/autopilot_run` สำหรับ complex specs

#### Section 12: Directory Structure
- เพิ่ม `.spec/checkpoints.db` เป็น write location

---

## Autopilot Features Documented

### 1. Parallel Execution (parallel_execution.py)
**คำอธิบาย:** รัน tasks หลายตัวพร้อมกันเพื่อเพิ่มความเร็ว

**Use Cases:**
- รัน tests หลายไฟล์พร้อมกัน
- Generate หลาย specs พร้อมกัน
- Validate หลาย tasks พร้อมกัน

**Best Practices:**
- ใช้ max_workers = CPU cores สำหรับ CPU-bound tasks
- ใช้ max_workers = 10-20 สำหรับ I/O-bound tasks
- ตั้ง timeout เพื่อป้องกัน tasks ค้าง

---

### 2. Checkpointing (checkpoint_manager.py)
**คำอธิบาย:** บันทึกและกู้คืน workflow state เพื่อ resume จากจุดที่หยุด

**Use Cases:**
- Resume long-running workflows หลัง interruption
- Rollback เมื่อเกิด error
- Debug workflow state ที่จุดต่างๆ

**Best Practices:**
- Save checkpoint ก่อนและหลัง critical steps
- ใช้ meaningful checkpoint IDs
- Clean up old checkpoints เป็นประจำ

---

### 3. Progress Streaming (streaming.py)
**คำอธิบาย:** ติดตาม workflow progress แบบ real-time

**Progress Events:**
- `workflow_started` - workflow เริ่มทำงาน
- `step_started` - step เริ่มทำงาน
- `step_progress` - step กำลังทำงาน
- `step_completed` - step เสร็จสิ้น
- `workflow_completed` - workflow เสร็จสิ้น
- `workflow_failed` - workflow ล้มเหลว

**Best Practices:**
- Update progress บ่อยๆ เพื่อ UX ที่ดี
- ใช้ meaningful step names
- Report errors ทันทีเมื่อเกิด

---

### 4. Human-in-the-Loop (human_in_the_loop.py)
**คำอธิบาย:** หยุด workflow เพื่อรอ human input/approval

**Interrupt Types:**
- `APPROVAL` - ขอ approval ก่อนดำเนินการต่อ
- `INPUT` - ขอ input จาก user
- `REVIEW` - ขอ review ผลลัพธ์
- `DECISION` - ขอตัดสินใจเลือกทาง

**Use Cases:**
- Review generated code ก่อน apply
- Approve breaking changes
- Choose between alternative implementations
- Provide missing information

**Best Practices:**
- ใช้ timeout เพื่อป้องกัน workflow ค้าง
- Provide clear context และ options
- Allow modifications ไม่ใช่แค่ approve/reject

---

### 5. Dynamic Routing (dynamic_routing.py)
**คำอธิบาย:** Route workflow ไปยัง agents ที่เหมาะสมตาม context

**Routing Strategies:**
- Intent-based routing
- Context-based routing
- Capability-based routing
- Load-based routing

**Best Practices:**
- Define clear routing rules
- Monitor routing decisions
- Fallback to default agent เมื่อไม่แน่ใจ

---

### 6. Agent Wrapper (agent_wrapper.py)
**คำอธิบาย:** Wrap agents ด้วย common features

**Features:**
- Logging - ติดตาม operations
- Caching - cache results
- Rate Limiting - จำกัด requests
- Profiling - วัด performance
- Input Validation - validate inputs
- Error Handling - handle errors

**Best Practices:**
- Enable caching สำหรับ idempotent operations
- ใช้ rate limiting สำหรับ external API calls
- Enable profiling เพื่อ optimize performance

---

## CLI Commands Summary

### /autopilot_run
รัน workflow พร้อม autopilot features

**Syntax:**
```bash
/autopilot_run <workflow-name> <args> [flags]
```

**Flags:**
- `--checkpoint` - Enable checkpointing
- `--parallel` - Enable parallel execution
- `--max-workers N` - Set parallel workers (default: 4)
- `--resume CHECKPOINT_ID` - Resume from checkpoint
- `--human-approval` - Require human approval

**Examples:**
```bash
# CLI
/autopilot_run smartspec_implement_tasks specs/core/spec-001/tasks.md --checkpoint --parallel

# Kilo Code
/autopilot_run.md smartspec_implement_tasks specs/core/spec-001/tasks.md --checkpoint --parallel --platform kilo
```

---

### /autopilot_status
ตรวจสอบ workflow status และ progress

**Syntax:**
```bash
/autopilot_status <workflow-name> [checkpoint-id]
```

**Output:**
- Current workflow state
- Progress percentage
- Current step
- Pending human interrupts
- Available checkpoints

**Examples:**
```bash
/autopilot_status smartspec_implement_tasks
/autopilot_status smartspec_implement_tasks checkpoint-abc123
```

---

### /autopilot_ask
ตอบ human interrupt (approval/review request)

**Syntax:**
```bash
/autopilot_ask <interrupt-id> --action <approve|reject|modify> [--modifications <json>]
```

**Actions:**
- `approve` - อนุมัติและดำเนินการต่อ
- `reject` - ปฏิเสธและยกเลิก workflow
- `modify` - แก้ไขและดำเนินการต่อ

**Examples:**
```bash
/autopilot_ask interrupt-xyz789 --action approve
/autopilot_ask interrupt-xyz789 --action modify --modifications '{"file": "src/auth.py", "changes": [...]}'
```

---

## Integration Patterns

### Pattern 1: Long-Running Workflow with Checkpoints
```python
from ss_autopilot.checkpoint_manager import CheckpointManager
from ss_autopilot.streaming import ProgressStreamer

manager = CheckpointManager()
streamer = ProgressStreamer()

# Start workflow with checkpoint
checkpoint_id = manager.save_checkpoint(workflow_name="implement", state={...})

# Process with progress updates
for i in range(100):
    streamer.update_progress(current_step=i+1)
    # Do work...
    if (i+1) % 10 == 0:
        manager.save_checkpoint(workflow_name="implement", state={...})

streamer.complete_workflow()
```

### Pattern 2: Parallel Execution with Progress
```python
from ss_autopilot.parallel_execution import ParallelExecutor
from ss_autopilot.streaming import ProgressStreamer

executor = ParallelExecutor(max_workers=4)
streamer = ProgressStreamer()

tasks = [task1, task2, task3, task4]
results = executor.execute_parallel(
    [(process_with_progress, task, i) for i, task in enumerate(tasks)]
)
```

### Pattern 3: Human-in-the-Loop Approval
```python
from ss_autopilot.human_in_the_loop import HumanInterruptManager, InterruptType

manager = HumanInterruptManager()

# Generate and request review
generated_code = generate_implementation(spec)
interrupt_id = manager.create_interrupt(
    workflow_name="implement",
    interrupt_type=InterruptType.REVIEW,
    message="Review generated code",
    context={"files": generated_code.files}
)

# Wait for response
response = manager.wait_for_response(interrupt_id, timeout=3600)

if response["action"] == "approve":
    apply_changes(generated_code)
elif response["action"] == "modify":
    apply_modifications(generated_code, response["modifications"])
```

---

## Configuration Example

### smartspec.config.yaml
```yaml
autopilot:
  parallel:
    enabled: true
    max_workers: 4
    timeout: 300
  
  checkpointing:
    enabled: true
    db_path: .spec/checkpoints.db
    auto_cleanup: true
    retention_days: 30
  
  streaming:
    enabled: true
    update_interval: 1
  
  human_in_the_loop:
    enabled: true
    default_timeout: 3600
    notification_channels:
      - slack
      - email
  
  agent_wrapper:
    logging: true
    caching: true
    rate_limiting: true
    profiling: true
```

---

## Migration Guide

### From Manual to Autopilot

**Before (Manual):**
```bash
/smartspec_generate_spec prompt.md --apply
/smartspec_generate_plan specs/core/spec-001/spec.md --apply
/smartspec_generate_tasks specs/core/spec-001/plan.md --apply
/smartspec_implement_tasks specs/core/spec-001/tasks.md --apply
```

**After (Autopilot):**
```bash
/autopilot_run smartspec_generate_spec prompt.md --checkpoint --human-approval
# Autopilot automatically chains: SPEC → PLAN → TASKS → IMPLEMENT
# With checkpoints, progress tracking, and human approval
```

---

## Git Commits

### Commit 1: f7d7e3d
**Message:** docs: Add autopilot knowledge base and update system prompt

**Files Changed:**
- `.smartspec/knowledge_base_autopilot_workflows.md` (NEW)
- `.smartspec/system_prompt_smartspec.md` (UPDATED)

**Changes:**
- +770 lines (knowledge base + system prompt updates)
- -200 lines (system prompt optimization)

---

## Verification

### File Sizes
✅ `knowledge_base_autopilot_workflows.md`: 15,234 bytes  
✅ `system_prompt_smartspec.md`: 7,096 bytes (88.7% of 8,000 limit)

### Content Coverage
✅ All 6 autopilot features documented  
✅ CLI integration documented  
✅ Integration patterns provided  
✅ Configuration examples included  
✅ Best practices documented  
✅ Troubleshooting guide included  
✅ Migration guide provided

### System Prompt Updates
✅ Autopilot section added (Section 6)  
✅ Knowledge source added (Section 0)  
✅ Progress routing updated (Section 7)  
✅ Context detection updated (Section 8)  
✅ New feature recommendations updated (Section 11)  
✅ Directory structure updated (Section 12)

---

## Status

✅ **Documentation Complete**  
✅ **System Prompt Updated (v6.5.0)**  
✅ **Under 8,000 character limit**  
✅ **Committed to GitHub**  
✅ **Production Ready**

---

**Repository:** https://github.com/naibarn/SmartSpec  
**Latest Commit:** f7d7e3d  
**Branch:** main  
**Date:** 2025-12-26
