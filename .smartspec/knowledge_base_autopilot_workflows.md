# Knowledge Base: SmartSpec Autopilot Workflows

**Version:** 1.0.0  
**Date:** 2025-12-26  
**Status:** Production Ready

---

## Overview

SmartSpec Autopilot เป็นระบบ workflow execution ที่ขับเคลื่อนด้วย LangGraph และ Agent-based architecture ซึ่งเพิ่มความสามารถในการทำงานแบบอัตโนมัติ, parallel execution, checkpointing, และ human-in-the-loop

---

## Core Features

### 1. Parallel Execution (parallel_execution.py)

**คำอธิบาย:** รัน tasks หลายตัวพร้อมกันเพื่อเพิ่มความเร็ว

**การใช้งาน:**
```python
from ss_autopilot.parallel_execution import ParallelExecutor

executor = ParallelExecutor(max_workers=4)
tasks = [task1, task2, task3, task4]
results = executor.execute_parallel(tasks)
```

**Use Cases:**
- รัน tests หลายไฟล์พร้อมกัน
- Generate หลาย specs พร้อมกัน
- Validate หลาย tasks พร้อมกัน

**Parameters:**
- `max_workers` (int): จำนวน workers สูงสุด (default: 4)
- `timeout` (int): timeout ต่อ task (วินาที)
- `retry_failed` (bool): retry tasks ที่ fail หรือไม่

**Best Practices:**
- ใช้ max_workers = CPU cores สำหรับ CPU-bound tasks
- ใช้ max_workers = 10-20 สำหรับ I/O-bound tasks
- ตั้ง timeout เพื่อป้องกัน tasks ค้าง

---

### 2. Checkpointing (checkpoint_manager.py)

**คำอธิบาย:** บันทึกและกู้คืน workflow state เพื่อ resume จากจุดที่หยุด

**การใช้งาน:**
```python
from ss_autopilot.checkpoint_manager import CheckpointManager

manager = CheckpointManager(db_path=".spec/checkpoints.db")

# Save checkpoint
checkpoint_id = manager.save_checkpoint(
    workflow_name="implement_tasks",
    state={"current_task": 5, "total_tasks": 10},
    metadata={"spec_id": "spec-001"}
)

# Resume from checkpoint
checkpoint = manager.load_checkpoint(checkpoint_id)
state = checkpoint.state
```

**Use Cases:**
- Resume long-running workflows หลัง interruption
- Rollback เมื่อเกิด error
- Debug workflow state ที่จุดต่างๆ

**Checkpoint Structure:**
- `workflow_name` (str): ชื่อ workflow
- `state` (dict): workflow state (JSON-serializable)
- `metadata` (dict): ข้อมูลเพิ่มเติม
- `timestamp` (datetime): เวลาที่บันทึก

**Best Practices:**
- Save checkpoint ก่อนและหลัง critical steps
- ใช้ meaningful checkpoint IDs
- Clean up old checkpoints เป็นประจำ

---

### 3. Progress Streaming (streaming.py)

**คำอธิบาย:** ติดตาม workflow progress แบบ real-time

**การใช้งาน:**
```python
from ss_autopilot.streaming import ProgressStreamer

streamer = ProgressStreamer()

# Start tracking
streamer.start_workflow("implement_tasks", total_steps=10)

# Update progress
for i in range(10):
    streamer.update_progress(
        current_step=i+1,
        step_name=f"Task {i+1}",
        status="in_progress"
    )
    # Do work...
    streamer.update_progress(
        current_step=i+1,
        step_name=f"Task {i+1}",
        status="completed"
    )

# Complete
streamer.complete_workflow()
```

**Progress Events:**
- `workflow_started` - workflow เริ่มทำงาน
- `step_started` - step เริ่มทำงาน
- `step_progress` - step กำลังทำงาน (มี % progress)
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

**การใช้งาน:**
```python
from ss_autopilot.human_in_the_loop import HumanInterruptManager, InterruptType

manager = HumanInterruptManager()

# Create interrupt
interrupt_id = manager.create_interrupt(
    workflow_name="implement_tasks",
    interrupt_type=InterruptType.APPROVAL,
    message="Review generated code before applying",
    context={"files": ["src/auth.py", "src/user.py"]},
    timeout=3600  # 1 hour
)

# Wait for response
response = manager.wait_for_response(interrupt_id, timeout=3600)

if response["action"] == "approve":
    # Continue workflow
    pass
elif response["action"] == "reject":
    # Cancel workflow
    pass
elif response["action"] == "modify":
    # Apply modifications and continue
    modifications = response.get("modifications", {})
```

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

**การใช้งาน:**
```python
from ss_autopilot.dynamic_routing import DynamicRouter

router = DynamicRouter()

# Route based on intent
next_agent = router.route(
    intent="implement_feature",
    context={"spec_type": "api", "language": "python"}
)

# Execute routed agent
result = next_agent.execute(context)
```

**Routing Strategies:**
- **Intent-based:** route ตาม user intent
- **Context-based:** route ตาม workflow context
- **Capability-based:** route ตาม agent capabilities
- **Load-based:** route ตาม agent load

**Best Practices:**
- Define clear routing rules
- Monitor routing decisions
- Fallback to default agent เมื่อไม่แน่ใจ

---

### 6. Agent Wrapper (agent_wrapper.py)

**คำอธิบาย:** Wrap agents ด้วย common features (logging, caching, rate limiting, etc.)

**การใช้งาน:**
```python
from ss_autopilot.agent_wrapper import AgentWrapper

wrapped_agent = AgentWrapper(
    agent=my_agent,
    agent_name="implement_agent",
    enable_logging=True,
    enable_caching=True,
    enable_rate_limiting=True,
    enable_profiling=True
)

# Use like normal agent
result = wrapped_agent.execute(task)
```

**Features:**
- **Logging:** ติดตาม agent operations
- **Caching:** cache results เพื่อเพิ่มความเร็ว
- **Rate Limiting:** จำกัด requests ต่อเวลา
- **Profiling:** วัด performance
- **Input Validation:** validate inputs ก่อนประมวลผล
- **Error Handling:** handle errors อย่างสม่ำเสมอ

**Best Practices:**
- Enable caching สำหรับ idempotent operations
- ใช้ rate limiting สำหรับ external API calls
- Enable profiling เพื่อ optimize performance

---

## Workflow Integration Patterns

### Pattern 1: Long-Running Workflow with Checkpoints

```python
from ss_autopilot.checkpoint_manager import CheckpointManager
from ss_autopilot.streaming import ProgressStreamer

manager = CheckpointManager()
streamer = ProgressStreamer()

# Start workflow
streamer.start_workflow("implement_tasks", total_steps=100)

# Save initial checkpoint
checkpoint_id = manager.save_checkpoint(
    workflow_name="implement_tasks",
    state={"current_task": 0, "total_tasks": 100}
)

try:
    for i in range(100):
        # Update progress
        streamer.update_progress(current_step=i+1, step_name=f"Task {i+1}")
        
        # Do work
        result = process_task(i)
        
        # Save checkpoint every 10 tasks
        if (i+1) % 10 == 0:
            manager.save_checkpoint(
                workflow_name="implement_tasks",
                state={"current_task": i+1, "total_tasks": 100, "results": results}
            )
    
    streamer.complete_workflow()
except Exception as e:
    # Can resume from last checkpoint
    checkpoint = manager.load_checkpoint(checkpoint_id)
    resume_from = checkpoint.state["current_task"]
```

### Pattern 2: Parallel Execution with Progress Tracking

```python
from ss_autopilot.parallel_execution import ParallelExecutor
from ss_autopilot.streaming import ProgressStreamer

executor = ParallelExecutor(max_workers=4)
streamer = ProgressStreamer()

tasks = [task1, task2, task3, task4, task5]
streamer.start_workflow("parallel_tasks", total_steps=len(tasks))

def task_with_progress(task, index):
    streamer.update_progress(current_step=index+1, step_name=task.name)
    result = task.execute()
    streamer.update_progress(current_step=index+1, status="completed")
    return result

results = executor.execute_parallel(
    [(task_with_progress, task, i) for i, task in enumerate(tasks)]
)

streamer.complete_workflow()
```

### Pattern 3: Human-in-the-Loop Approval

```python
from ss_autopilot.human_in_the_loop import HumanInterruptManager, InterruptType

manager = HumanInterruptManager()

# Generate code
generated_code = generate_implementation(spec)

# Request human review
interrupt_id = manager.create_interrupt(
    workflow_name="implement_tasks",
    interrupt_type=InterruptType.REVIEW,
    message="Review generated implementation",
    context={
        "files": generated_code.files,
        "changes": generated_code.diff,
        "tests": generated_code.tests
    }
)

# Wait for response
response = manager.wait_for_response(interrupt_id, timeout=3600)

if response["action"] == "approve":
    apply_changes(generated_code)
elif response["action"] == "modify":
    modifications = response["modifications"]
    modified_code = apply_modifications(generated_code, modifications)
    apply_changes(modified_code)
else:
    cancel_workflow()
```

---

## CLI Integration

### Autopilot Run

```bash
# Run workflow with autopilot
/autopilot_run <workflow-name> <args> --checkpoint --parallel --max-workers 4

# Examples
/autopilot_run smartspec_implement_tasks specs/core/spec-001/tasks.md --checkpoint --parallel
/autopilot_run smartspec_generate_tests specs/core/spec-001/spec.md --checkpoint
```

**Flags:**
- `--checkpoint` - Enable checkpointing
- `--parallel` - Enable parallel execution
- `--max-workers N` - Set number of parallel workers
- `--resume CHECKPOINT_ID` - Resume from checkpoint
- `--human-approval` - Require human approval at key steps

### Autopilot Status

```bash
# Check workflow status
/autopilot_status <workflow-name> [checkpoint-id]

# Examples
/autopilot_status smartspec_implement_tasks
/autopilot_status smartspec_implement_tasks checkpoint-abc123
```

**Output:**
- Current workflow state
- Progress percentage
- Current step
- Pending human interrupts
- Available checkpoints

### Autopilot Ask

```bash
# Respond to human interrupt
/autopilot_ask <interrupt-id> --action <approve|reject|modify> [--modifications <json>]

# Examples
/autopilot_ask interrupt-xyz789 --action approve
/autopilot_ask interrupt-xyz789 --action modify --modifications '{"file": "src/auth.py", "changes": [...]}'
```

---

## Configuration

### smartspec.config.yaml

```yaml
autopilot:
  # Parallel execution
  parallel:
    enabled: true
    max_workers: 4
    timeout: 300  # seconds per task
  
  # Checkpointing
  checkpointing:
    enabled: true
    db_path: .spec/checkpoints.db
    auto_cleanup: true
    retention_days: 30
  
  # Progress streaming
  streaming:
    enabled: true
    update_interval: 1  # seconds
  
  # Human-in-the-loop
  human_in_the_loop:
    enabled: true
    default_timeout: 3600  # 1 hour
    notification_channels:
      - slack
      - email
  
  # Agent wrapper
  agent_wrapper:
    logging: true
    caching: true
    rate_limiting: true
    profiling: true
```

---

## Best Practices

### 1. Checkpointing Strategy
- Save checkpoints before/after critical operations
- Clean up old checkpoints regularly
- Use meaningful checkpoint IDs
- Store minimal state (avoid large objects)

### 2. Parallel Execution
- Profile first to identify parallelizable tasks
- Set appropriate max_workers based on task type
- Handle failures gracefully (retry or skip)
- Monitor resource usage

### 3. Progress Tracking
- Update progress frequently for better UX
- Use descriptive step names
- Report errors immediately
- Provide time estimates when possible

### 4. Human-in-the-Loop
- Use sparingly (only for critical decisions)
- Provide clear context and options
- Set reasonable timeouts
- Allow modifications, not just approve/reject

### 5. Error Handling
- Use checkpoints to enable recovery
- Log all errors with context
- Provide actionable error messages
- Implement retry logic for transient failures

---

## Troubleshooting

### Checkpoint Not Found
**Problem:** Cannot load checkpoint  
**Solution:** Check checkpoint ID, ensure DB path is correct, verify checkpoint wasn't cleaned up

### Parallel Execution Timeout
**Problem:** Tasks timing out in parallel execution  
**Solution:** Increase timeout, reduce max_workers, check for deadlocks

### Human Interrupt Expired
**Problem:** Human interrupt timed out  
**Solution:** Increase timeout, implement notification system, allow re-triggering

### Progress Not Updating
**Problem:** Progress stuck or not updating  
**Solution:** Check streaming configuration, ensure update_progress is called, verify no blocking operations

---

## Migration Guide

### From Manual Workflows to Autopilot

**Before:**
```bash
/smartspec_generate_spec prompt.md --apply
/smartspec_generate_plan specs/core/spec-001/spec.md --apply
/smartspec_generate_tasks specs/core/spec-001/plan.md --apply
/smartspec_implement_tasks specs/core/spec-001/tasks.md --apply
```

**After:**
```bash
/autopilot_run smartspec_generate_spec prompt.md --checkpoint --human-approval
# Autopilot automatically chains: SPEC → PLAN → TASKS → IMPLEMENT
# With checkpoints, progress tracking, and human approval at key steps
```

---

## API Reference

See individual module documentation:
- `parallel_execution.py` - Parallel task execution
- `checkpoint_manager.py` - Workflow checkpointing
- `streaming.py` - Progress streaming
- `human_in_the_loop.py` - Human interrupts
- `dynamic_routing.py` - Agent routing
- `agent_wrapper.py` - Agent enhancement

---

**Last Updated:** 2025-12-26  
**Version:** 1.0.0  
**Status:** Production Ready ✅
