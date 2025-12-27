# SmartSpec Autopilot CLI (LangGraph + Kilo Code CLI)

เอกสารนี้เป็น **ข้อสรุปเชิงสถาปัตยกรรมและแผนพัฒนาแบบละเอียด** สำหรับการสร้าง

> **SmartSpec Autopilot CLI**
> โดยใช้ **LangGraph เป็น Orchestrator (Control Plane)**
> และใช้ **Kilo Code CLI เป็น Worker (Execution Plane)**

เป้าหมายคือทำให้ระบบ:
- ทำงานกับ SmartSpec เดิมได้ 100%
- รันได้บน **Windows / Linux / macOS**
- รองรับ **Multi-Agent / Parallel Execution**
- รองรับ **Multi-LLM / Multi-Provider ต่อโหมด**
- รันอัตโนมัติยาว ๆ (overnight / autopilot)
- หลุดกฎ SmartSpec ได้ยาก (system-enforced)

---

## 1. เหตุผลในการเลือกสถาปัตยกรรมนี้

### ปัญหาที่พบจากการใช้ Kilo Code CLI เพียงอย่างเดียว
- Agent พยายามตัดสินใจเอง → หลุดกฎง่าย (preview/apply/validator)
- คุม parallel agents ยาก (ชนไฟล์ / ชนสcope)
- คุม long-running workflow (budget, resume, stop condition) ได้ไม่ดี

### จุดแข็งของ LangGraph
- State machine / workflow orchestration
- Persistence & checkpoint (resume ได้)
- Parallelism + fan-out / fan-in
- Tool gating (policy enforcement)

### จุดแข็งของ Kilo Code CLI
- เก่งด้าน coding agent + repo manipulation
- รองรับ workflow markdown (`/command.md`)
- มี auto mode, parallel mode, branch isolation

**ข้อสรุป**
> ใช้ LangGraph เป็น “สมองและผู้คุมกฎ”
> และใช้ Kilo Code CLI เป็น “แรงงานเขียนโค้ด”

---

## 2. ภาพรวมสถาปัตยกรรม (High-Level)

ระบบ SmartSpec Autopilot เวอร์ชัน Product-grade จะถูกออกแบบเป็น **Control Plane + Execution Plane + Experience Plane (UI)** โดยผู้ใช้ปลายทาง **จะไม่เห็น Kilo Code CLI** แต่ใช้งานผ่าน SmartSpec UI ที่เป็นมิตรและทันสมัย

### 2.1 Experience Plane (Custom UI – Primary Interface)

ผู้ใช้จะโต้ตอบกับระบบผ่าน **Custom UI** (Desktop/Web) ที่ออกแบบมาเพื่อ non‑dev:
- พิมพ์สิ่งที่ต้องการเป็น **Natural Language Prompt**
- ดู dashboard, progress, timeline แบบเรียลไทม์
- ไม่จำเป็นต้องรู้ workflow, code หรือ CLI

### 2.2 Control Plane (LangGraph Orchestrator)
- ตีความ intent จาก prompt
- เลือก workflow SmartSpec ที่เหมาะสม
- แตกงาน → work items
- จัดการ policy, budget, parallelism, resume

### 2.3 Execution Plane (Kilo Code CLI Workers)
- ทำงานเบื้องหลังแบบ invisible
- เขียนโค้ด / รัน tests / แก้ error
- ทำงานใน branch/worktree แยก

```
┌────────────────────────────────────┐
│ SmartSpec UI (Desktop / Web / CLI) │
│ - Prompt-based UX (non-dev)        │
│ - Dashboard / Timeline / Agents    │
└──────────────┬─────────────────────┘
               │
┌──────────────▼─────────────────────┐
│ LangGraph Orchestrator              │
│ - Intent → Workflow                 │
│ - Policy / Budget / Locks           │
│ - Parallel Agent Scheduler          │
└──────────────┬─────────────────────┘
               │ work items
        ┌──────▼────────┐   ┌────────▼───────┐
        │ Kilo Worker A │   │ Kilo Worker B  │   (parallel)
        │ branch/auth   │   │ branch/billing │
        └───────────────┘   └────────────────┘
```

┌─────────────────────────────┐
│  SmartSpec CLI / UI (Tauri) │
│  /autopilot_run /ask /status│
└──────────────┬──────────────┘
               │
┌──────────────▼──────────────┐
│ LangGraph Orchestrator      │
│ - Intent Parser             │
│ - Workflow Selector         │
│ - Policy Gate               │
│ - Parallel Scheduler        │
│ - Model Router              │
│ - Checkpoint Manager        │
└──────────────┬──────────────┘
               │ work items
        ┌──────▼───────┐  ┌──────▼───────┐
        │ Kilo Worker  │  │ Kilo Worker  │   (parallel)
        │ branch A     │  │ branch B     │
        └──────────────┘  └──────────────┘

```

---

## 3. บทบาทของ Agent แต่ละตัว

### 3.1 Intent Parser Agent
- รับคำถามภาษา Thai / English
- แปลงเป็น intent (status / run / ask)
- ดึง context จาก SmartSpec project state

### 3.2 Orchestrator Agent (LangGraph)
- รู้ workflow ทั้งหมดของ SmartSpec (59 workflows)
- แนะนำหรือเลือก workflow ที่ถูกต้อง
- แตก workflow → work items
- คุม policy และ stop conditions

### 3.3 Worker Agent (Kilo CLI)
- รับ work item ที่ชัดเจน (scope จำกัด)
- เขียน/แก้โค้ดใน branch/worktree ของตัวเอง
- รัน tests / validators ที่ถูก allowlist
- ส่งผลลัพธ์ (diff, logs, status) กลับ

### 3.4 Verifier / Gate Agent
- ตรวจ validator
- ตรวจ test results
- ตัดสินใจว่าจะ apply / merge / retry / abort

---

## 4. การแยก LLM ตามโหมด (Multi-Model Routing)

### เป้าหมาย
- Orchestrator → Grok
- Code → GLM
- Debug → Claude
- Verify → GPT-4.x (หรืออื่น ๆ)

### รูปแบบ config (models.yaml)
```yaml
models:
  orchestrator:
    provider: xai
    model: grok-2
  code:
    provider: zhipu
    model: glm-4.5
  debug:
    provider: anthropic
    model: claude-3.7-sonnet
  verifier:
    provider: openai
    model: gpt-4.1
```

LangGraph จะเลือก model ตาม role ของ node
> ❗ ไม่พึ่ง UI memory หรือ sticky mode อย่างเดียว

---

## 5. Policy Layer (หัวใจที่กันหลุดกฎ)

### 5.1 Write Scope Guard
| โหมด | เขียนไฟล์ได้ |
|----|--------------|
| Preview | `.spec/reports/**` เท่านั้น |
| Apply | เฉพาะไฟล์เป้าหมาย (เช่น `specs/**/plan.md`) |

### 5.2 Validator Gate (บังคับด้วยระบบ)
- ทุก workflow ที่ระบุ validator
- ถ้า validator fail → ห้าม apply / merge
- Agent ไม่มีสิทธิ override

### 5.3 Command Allowlist
อนุญาตเฉพาะ:
- python / pytest / uv / poetry
- ruff / mypy
- git (status, diff, commit)
- SmartSpec validator scripts

ปฏิเสธ:
- `sh -c`
- network commands
- shell injection

### 5.4 Budget & Stop Conditions
- test fail pattern เดิมซ้ำ N ครั้ง → stop
- เขียนไฟล์เกิน X ต่อ work item → split
- เวลารวมเกินกำหนด → graceful stop + report

---

## 6. Parallel Agents (ทำงานไม่ซ้ำซ้อน)

### 6.1 Task Sharding
- แตกตาม spec-id (`spec-core-001-*`)
- หรือแตกตาม phase/module

### 6.2 Lock Strategy
- lock ระดับ `specs/<spec-id>/**`
- worker อื่นห้ามแตะสcope ที่ lock อยู่

### 6.3 Branch / Worktree Isolation
- worker แต่ละตัวทำงานใน branch ของตัวเอง
- merge หลัง verifier ผ่านเท่านั้น

---

## 7. Cross-Platform (Windows / Linux / macOS)

### ข้อกำหนด
- Python 3.8+
- LangGraph >= 0.2.x
- LangGraph Checkpoint >= 0.2.x
- Git
- Kilo Code CLI

### แนวทางพัฒนา
- ไม่ใช้ shell-specific syntax
- ใช้ argument-based process execution
- ใช้ path abstraction (pathlib)
- รองรับ `pipx`, `uv`, `poetry`

---

## 8. User Experience (Custom UI – ทางเลือกที่ 3)

### 8.1 เป้าหมาย UX
- ผู้ใช้ **ไม่ต้องรู้เรื่อง code / git / branch / workflow**
- พิมพ์แค่ “สิ่งที่อยากได้” → ระบบทำงานต่อเอง
- เหมือนใช้ "AI Project Manager + AI Engineering Team"

### 8.2 หน้าจอหลัก (Main Dashboard)
- Project overview (specs ทั้งหมด)
- Completion %, ETA, pending work
- Cost overview (LLM usage)

### 8.3 Agent Timeline View
- แสดง agent ทุกตัวที่กำลังทำงาน
- สถานะ: `Queued / Running / Blocked / Done / Failed`
- Timeline แบบ event stream (thinking / coding / testing)

### 8.4 Agent Inspector (Switch ดู agent)
- เลือกดู agent แต่ละตัวได้
- เห็นว่า agent:
  - แก้ไฟล์อะไร
  - อยู่ branch ไหน
  - รัน test อะไร
  - error ล่าสุดคืออะไร

### 8.5 Branch & Merge Awareness
- agent ทุกตัวทำงานใน branch แยก
- UI แสดง mapping: agent → branch → scope
- **ไม่มีการ auto-merge**
- ตัดสินใจ merge ภายหลัง (manual หรือ verifier agent)

### 8.6 Error Handling แบบ Autopilot
- ถ้า agent พบ error:
  - UI แสดง error + สาเหตุ (ภาษาเข้าใจง่าย)
  - ระบบสลับเข้า Debug agent อัตโนมัติ
  - ทำ retry จนจบหรือจนถึง stop condition

### 8.7 Non‑Dev Friendly Mode
- ไม่มีคำว่า workflow / validator / branch ให้ผู้ใช้เห็น
- ผู้ใช้เห็นเพียง:
  - “ระบบกำลังแก้ปัญหา X”
  - “แก้ไขสำเร็จ / ต้องการการตัดสินใจจากคุณ”

---


## 9. Backend Platform & Cost Control

### 9.1 Authentication & Authorization
- ผู้ใช้ login ผ่าน SmartSpec UI
- Token-based auth (JWT / OAuth)
- ผูก user → project → budget

### 9.2 LLM Cost Control
- กำหนด budget ต่อ user / project / run
- Orchestrator ตรวจ token usage ทุก step
- ถ้าเกิน budget → pause + notify

### 9.3 MCP Server Integration
- SmartSpec ใช้ MCP server เป็น gateway:
  - ติดต่อ LLM providers
  - ติดต่อ tools ภายนอก
- ทำให้:
  - เปลี่ยน provider ได้โดยไม่กระทบ client
  - enforce policy ระดับองค์กร

---

## 10. Roadmap การพัฒนา (ลำดับที่แนะนำ)

### Phase 1 – Autopilot Core
- LangGraph Orchestrator (intent → workflow)
- Model Router (multi‑LLM per role)
- Policy Gate (write / validate / command)

### Phase 2 – Invisible Workers
- Kilo CLI worker integration
- Branch/worktree isolation
- Validator + retry loop

### Phase 3 – Parallel Intelligence
- Agent scheduler
- Lock manager
- Conflict‑free parallel execution

### Phase 4 – Product UI
- Dashboard / Timeline / Agent Inspector
- Non‑dev UX
- Progress & ETA

### Phase 5 – Platform & Scale
- AuthN/AuthZ
- LLM cost governance
- MCP server integration
- SaaS readiness

---

## 11. Product Vision (สรุป)

> ผู้ใช้บอก "อยากได้อะไร"
> 
> SmartSpec Autopilot จัดการทุกขั้นตอน:
> - วางแผน
> - แบ่งงาน
> - ให้ agent ทำพร้อมกัน
> - แก้ error เอง
> - คุมงบและความเสี่ยง
> 
> แล้วส่งมอบ **งานที่เสร็จแล้ว** ให้ผู้ใช้

นี่ไม่ใช่แค่ CLI หรือ AI tool
แต่คือ **AI Engineering Operating System** สำหรับโปรเจกต์ขนาดใหญ่

---

## 12. UX Flow & Screen-by-Screen Design (รายละเอียด)

### 12.1 User Journey (Non-Dev First)
1. ผู้ใช้เปิด SmartSpec Autopilot UI
2. เลือกหรือสร้าง Project
3. พิมพ์ Prompt เช่น:
   > "สร้างระบบ Authentication สำหรับ SaaS ตาม spec-core-001"
4. ระบบตอบกลับด้วย:
   - สิ่งที่จะทำ (Plan Summary)
   - จำนวน agent ที่จะใช้
   - ETA คร่าว ๆ
5. ผู้ใช้กด **Start Autopilot**
6. ระบบทำงานต่อเนื่องโดยอัตโนมัติจนงานเสร็จ

---

### 12.2 Main Dashboard Screen
- รายการ Projects
- Progress (%) ต่อ project
- Active agents count
- Cost usage (วันนี้ / โปรเจกต์นี้)
- ปุ่ม: `View Details`

---

### 12.3 Autopilot Run View
- Overall Progress Bar
- Phase breakdown (Spec → Plan → Tasks → Implement → Verify)
- Estimated Time Remaining

---

### 12.4 Agent Timeline View
- Card ต่อ agent (Agent A, Agent B, ...)
- สถานะ: Queued / Running / Debugging / Done / Failed
- Timeline events:
  - started task
  - edited file
  - ran tests
  - error encountered

---

### 12.5 Agent Inspector Panel
- Current Task
- Branch name
- Files touched
- Last command run
- Last error (ถ้ามี)
- Action: `Pause / Resume / Kill Agent`

---

## 13. Backend Technical Specification (API & Contracts)

### 13.1 Core Services
- **API Gateway** (FastAPI / NestJS)
- **LangGraph Orchestrator Service**
- **Worker Manager (Kilo CLI Runner)**
- **MCP Gateway Server**

---

### 13.2 Key API Endpoints

```http
POST /api/autopilot/run
GET  /api/autopilot/status/{run_id}
GET  /api/autopilot/events/{run_id}   (stream)
POST /api/autopilot/ask
POST /api/autopilot/cancel/{run_id}
```

---

### 13.3 Event Streaming Schema (UI)
```json
{
  "timestamp": "2025-01-01T10:30:22Z",
  "agent_id": "agent-auth-01",
  "status": "running",
  "event": "running pytest",
  "details": {}
}
```

---

### 13.4 Worker Execution Contract
- Orchestrator → Worker:
  - task description
  - allowed paths
  - branch name
- Worker → Orchestrator:
  - diff summary
  - test results
  - error reports

---

## 14. MVP Scope (สร้างให้เสร็จและใช้งานได้เร็ว)

### 14.1 MVP Goals
- ใช้งานได้จริงกับ SmartSpec project
- รัน Autopilot ได้ end-to-end
- Non-dev ใช้ได้

---

### 14.2 MVP Features (ต้องมี)
- Prompt-based Autopilot Run
- Dashboard + Progress
- Agent Timeline (read-only)
- Single-agent → Multi-agent (2–3 agents)
- Branch isolation
- Validator gate

---

### 14.3 MVP Features (ตัดออกก่อน)
- Auto-merge to main
- Fine-grained cost analytics
- Advanced permissions
- External tool marketplace

---

### 14.4 MVP Tech Stack (แนะนำ)
- UI: Tauri + React + Tailwind + Framer Motion
- Backend: Python + FastAPI + LangGraph
- Workers: Kilo Code CLI
- Storage: SQLite → Postgres
- Streaming: WebSocket / SSE

---

## 15. Final Vision

> SmartSpec Autopilot คือ
> "AI Team ที่คุณจ้างครั้งเดียว แล้วทำงานให้คุณตลอด"

ไม่ต้องรู้ code
ไม่ต้องรู้ workflow
ไม่ต้อง debug เอง

คุณแค่บอกเป้าหมาย
ระบบจัดการทุกอย่างจนเสร็จ
