---
manual_name: /smartspec_generate_tasks Manual (TH)
manual_version: 5.6
compatible_workflow: /smartspec_generate_tasks
compatible_workflow_versions: 5.6.2 – 5.6.4
role: user/operator manual (tech lead, architect, platform, spec owner)
---

# /smartspec_generate_tasks คู่มือการใช้งาน (v5.6, ภาษาไทย)

## 1. ภาพรวม (Overview)

คู่มือนี้อธิบายวิธีใช้งาน workflow:

> `/smartspec_generate_tasks v5.6.x` (เช่น v5.6.4)

workflow นี้มีหน้าที่ **สร้าง/อัปเดต `tasks.md` จาก spec (และ plan ถ้ามี)**  
โดยเน้น:

- ยึดตาม SmartSpec v5.6 **centralization**:
  - ใช้ SPEC_INDEX และ registry เป็นตัวกลาง
  - ไม่สร้าง entity ซ้ำข้าม spec / repo
- รองรับ **multi-repo / multi-registry**:
  - ใช้ `--workspace-roots`, `--repos-config`, `--registry-roots`
  - เคารพ owner ของ API/model/term/UI component จาก repo อื่น
- จัด alignment กับ **UI mode**:
  - JSON-first (`ui.json`) vs inline UI ใน `spec.md`
- สร้าง tasks ที่:
  - แยกเป็นหมวดงาน + subtasks (`T001.1` ฯลฯ)
  - มี metadata เรื่อง reuse/create, owner, registry, repo context
- วาง **guardrail สำหรับ web/AI/data**:
  - React/Next.js/RSC/Node/npm (อิง `tool-version-registry.json` ถ้ามี)
  - AI/LLM (prompt safety, logging, injection, red-teaming)
  - data-sensitivity (PII/financial/health/secret) และห้ามใส่ข้อมูลจริงใน `tasks.md`

> **สำคัญ:**  
> - workflow นี้มี `write_guard: ALLOW-WRITE` แต่เขียนได้เฉพาะ:
>   - `tasks.md` ข้าง ๆ `spec.md`
>   - report ใต้ `.spec/reports/generate-tasks/` (หรือ `--report-dir`)
> - ไม่แตะต้อง `spec.md`, `plan.md`, registry หรือไฟล์ใน repo อื่น

---

## 2. ใช้เมื่อไร (When to Use)

ใช้ `/smartspec_generate_tasks` เมื่อ:

- มี **spec (และ plan)** อยู่แล้ว และอยากได้ `tasks.md` ที่:
  - แตกเป็นงานย่อยพร้อมลำดับ
  - align กับ SPEC_INDEX + registry + multi-repo ownership
- กำลังจะ implement:
  - service/web app (React/Next.js/Node/RSC)
  - feature AI/LLM เช่น copilot, in-app chat
  - data flow ที่มีข้อมูลอ่อนไหว / ถูกกำกับดูแล
- ต้องการ `tasks.md` ที่เอาไปต่อกับ:
  - CI/CD, governance gate, release readiness

**ไม่ควรใช้** workflow นี้เพื่อ:

- แก้ `spec.md` (ให้ใช้ `/smartspec_generate_spec`)
- สร้าง/แก้ `plan.md` (ใช้ `/smartspec_generate_plan`)
- แก้หรือเขียน registry โดยตรง

---

## 3. What’s New ใน v5.6.x (สำหรับ generate_tasks)

### 3.1 จุดเด่น v5.6 (ฐานเดิม)

- รองรับ multi-repo/multi-registry:
  - `--workspace-roots`, `--repos-config`, `--registry-roots`
- สร้าง tasks แยกหมวด + subtasks (atomic) พร้อม dependency graph
- มี resource usage metadata:
  - `type: reuse | create`
  - owner spec / owner repo
  - registry entry ที่เกี่ยวข้อง

### 3.2 v5.6.3 (hardening เพิ่มเติม)

- เพิ่ม section Modes (role, write_guard, safety, UI, Kilo)
- เพิ่ม `--safety-mode` / `--strict` เป็น alias ของ `--mode` แบบเก่า
- เพิ่ม KiloCode support (`--kilocode`, `--nosubtasks`)
- เพิ่ม guardrail สำหรับ:
  - React/Next.js/RSC/Node/npm (อ่าน `tool-version-registry.json`)
  - design system / App component / UI JSON
  - AI/LLM + data-sensitivity
- เพิ่ม `--report-dir`, `--stdout-summary`

### 3.3 v5.6.4 (patch-level tightening ล่าสุด)

- โครง section align กับ workflow ตัวอื่น (spec/plan):
  - Canonical Folders & File Placement
  - KiloCode Support (Meta-Flag)
  - Inline Detection Rules
  - Best Practices
- เน้นให้ report มี audit metadata ชัด (workflow version, flags, index, registry, timestamp)
- ถ้าใช้ web stack แต่ไม่มี `tool-version-registry.json`:
  - ต้องมี tasks bootstrap/refresh registry โดย owner ที่เหมาะสม (platform/security)
- แนะนำให้ `tasks.md` มี header field `safety_status` เสมอ
- เพิ่ม guard เรื่องห้ามให้ secrets/PII หลุดเข้ามาใน `tasks.md` และ report (ให้ generate task เกี่ยวกับ redaction/cleanup แทน)

---

## 4. แนวคิดหลัก (Core Concepts)

### 4.1 SPEC_INDEX & Registry

- `SPEC_INDEX`:
  - ไฟล์ mapping spec ทั้งระบบ + dependency graph
- `registry`:
  - แหล่งเก็บ entity กลาง เช่น API, data model, glossary, UI component, pattern, tool baseline
- generate_tasks จะใช้สิ่งเหล่านี้เพื่อ:
  - รู้ว่า spec ไหนเป็น owner ของ API/model/term
  - ตัดสินว่า task ควรเป็น **reuse** หรือ **create**
  - หลีกเลี่ยงการสร้าง entity ซ้ำ

### 4.2 Multi-repo / Multi-registry

- ใช้ flag:
  - `--workspace-roots` (list path repo พี่น้อง)
  - `--repos-config` (ไฟล์ JSON mapping repo ID → path)
  - `--registry-dir` (primary registry)
  - `--registry-roots` (registry เสริม – read-only)
- rule สำคัญ:
  - current repo: เขียน `tasks.md` / report ได้
  - sibling repos: **read-only เสมอ**
  - entity ที่มีใน registry อยู่แล้ว → ต้อง reuse ไม่ใช่สร้างใหม่

### 4.3 Safety Mode (`strict` vs `dev`)

- flag:
  - `--mode=strict|dev` (ของเดิม)
  - `--safety-mode=strict|dev` (ของใหม่ แนะนำ)
  - `--strict` = alias ของ `strict`

**strict**

- ใช้สำหรับ CI / งานที่มุ่งสู่ production
- ถ้า context สำคัญหายไป (index, registry, web-stack baseline) ให้:
  - mark `safety_status=UNSAFE` หรือ
  - ใส่ blocking task + declare ว่าใช้ใน prod ไม่ได้
- ห้ามปล่อยให้มีการแนะนำเวอร์ชัน framework ที่ต่ำกว่า `min_patch`

**dev**

- ใช้สำหรับ prototype, local dev, sandbox
- อนุญาตให้ context ไม่ครบได้ แต่:
  - ต้องใส่ warning + TODO Bootstrap tasks ให้ครบ
  - ตั้ง `safety_status=DEV-ONLY`
  - ห้ามใช้ `tasks.md` นี้ไป gating prod โดยตรง

### 4.4 UI Mode (`auto|json|inline`)

- `--ui-mode=auto|json|inline`
- `--no-ui-json` = alias ของ `inline`
- ผลต่อ tasks:
  - `json`: เน้นงานเกี่ยวกับ `ui.json`, component mapping, design tokens, patterns, review AI-generated UI JSON
  - `inline`: เน้นงาน implement UI ตามที่บรรยายใน `spec.md`, แต่ว่ายังเน้น reuse design system / App component

### 4.5 Web Stack (React/Next.js/RSC/Node/npm)

ถ้า spec/plan บอกว่ามีการใช้:

- React, ReactDOM
- Next.js (SSR/SSG/Edge)
- RSC / server actions / `react-server-dom-*`

tasks จะต้อง:

- อ่าน `tool-version-registry.json` ถ้ามี
- สร้าง tasks เกี่ยวกับ:
  - ไม่ให้ version ต่ำกว่า `min_patch`
  - แก้ fragmentation ของ version ระหว่าง service ต่าง ๆ
  - รัน SCA+`npm audit` / lockfile maintenance / bot updates
  - review boundary ของ RSC/SSR/Edge (data, access control, headers, caching)

ถ้าใช้ stack เหล่านี้แต่ registry ยังไม่มีหรือเก่ามาก:

- ต้องมี Phase 0 task เพื่อ bootstrap / refresh registry โดย owner (platform/security)

### 4.6 AI/LLM & Data-sensitivity

ถ้า spec มี AI/LLM:

- ต้องมี tasks ด้าน:
  - การออกแบบ prompt & context (ข้อมูลอะไรเข้าได้/ห้ามเข้า)
  - ป้องกัน prompt-injection + instruction hierarchy
  - logging/tracing แบบไม่มี secret/PII
  - red-team test / worst-case prompt

ถ้ามีข้อมูลอ่อนไหว:

- ต้องมี tasks:
  - data classification + masking/anonymization
  - ห้ามนำ log หรือ snippet ที่มีข้อมูลจริงไปแปะใน `tasks.md`
  - integrate DLP / secret scanner / compliance tool ตาม policy

---

## 5. Quick Start – ตัวอย่างคำสั่งพื้นฐาน

### 5.1 สร้าง `tasks.md` สำหรับ spec เดียว (strict mode)

```bash
smartspec_generate_tasks \
  specs/checkout/spec.md \
  --index=.spec/SPEC_INDEX.json \
  --registry-dir=.spec/registry \
  --safety-mode=strict \
  --ui-mode=auto \
  --stdout-summary
```

Output:

- `specs/checkout/tasks.md`
- report ใต้ `.spec/reports/generate-tasks/`

### 5.2 ดูผลก่อนโดยไม่เขียนไฟล์ (dry-run)

```bash
smartspec_generate_tasks \
  specs/legacy/spec-legacy-001/spec.md \
  --index=.spec/SPEC_INDEX.json \
  --registry-dir=.spec/registry \
  --safety-mode=dev \
  --dry-run \
  --stdout-summary
```

- แสดง `tasks.md` จำลองบน stdout
- ใช้ตรวจ logic/guardrail ก่อนเขียนไฟล์จริง

### 5.3 ใช้ dev mode บนโปรเจกต์ที่ index/registry ยังไม่ครบ

```bash
smartspec_generate_tasks \
  specs/newapp/spec-newapp-001/spec.md \
  --safety-mode=dev \
  --ui-mode=inline \
  --stdout-summary
```

- จะมี Phase 0 task ให้ bootstrap SPEC_INDEX / registry ให้ครบก่อนใช้จริง

---

## 6. Cheat Sheet – Flags สำคัญ

- Index / Registry
  - `--index`, `--specindex`
  - `--registry-dir`
  - `--registry-roots`
- Multi-repo
  - `--workspace-roots`
  - `--repos-config`
- Execution / Safety
  - `--mode=strict|dev`
  - `--safety-mode=strict|dev`
  - `--strict`
  - `--dry-run`
  - `--nogenerate`
  - `--report-dir`
  - `--stdout-summary`
- UI
  - `--ui-mode=auto|json|inline`
  - `--no-ui-json`
- Kilo / subtasks
  - `--kilocode`
  - `--nosubtasks`

---

## 7. ตัวอย่าง Multi-repo / Multi-registry

### 7.1 Monorepo หลาย service

```bash
smartspec_generate_tasks \
  specs/billing/spec-bill-002-invoice/spec.md \
  --index=.spec/SPEC_INDEX.json \
  --registry-dir=.spec/registry \
  --workspace-roots="." \
  --safety-mode=strict \
  --stdout-summary
```

- ใช้ SPEC_INDEX เดียวใน monorepo
- ใช้ registry กลาง `.spec/registry/` เป็น owner map

### 7.2 หลาย repo + registry กลาง

```bash
smartspec_generate_tasks \
  specs/notifications/spec-notif-003-email/spec.md \
  --index=../platform/.spec/SPEC_INDEX.json \
  --registry-dir=.spec/registry \
  --registry-roots="../platform/.spec/registry" \
  --workspace-roots="../platform;../billing" \
  --repos-config=.spec/smartspec.repos.json \
  --safety-mode=strict \
  --stdout-summary
```

- treat spec ใน repo ปัจจุบันเป็น consumer
- owner ของ API/model บางตัวอยู่ใน `../platform` → tasks จะเน้น reuse/integration

---

## 8. ตัวอย่าง UI Mode

### 8.1 JSON-first UI (มี `ui.json`)

```bash
smartspec_generate_tasks \
  specs/web/spec-web-001-dashboard/spec.md \
  --index=.spec/SPEC_INDEX.json \
  --registry-dir=.spec/registry \
  --ui-mode=json \
  --safety-mode=strict \
  --stdout-summary
```

- tasks จะรวมงาน:
  - ตรวจ/สร้าง/อัปเดต `ui.json`
  - mapping ไปยัง App components, design tokens, patterns
  - review AI-generated UI JSON ถ้ามี metadata ว่า origin=AI

### 8.2 Inline UI (ไม่มี `ui.json`)

```bash
smartspec_generate_tasks \
  specs/legacy/spec-legacy-ui-001/spec.md \
  --index=.spec/SPEC_INDEX.json \
  --registry-dir=.spec/registry \
  --ui-mode=inline \
  --safety-mode=strict \
  --stdout-summary
```

- tasks จะเน้น:
  - implement UI ตามคำอธิบายใน spec
  - reuse design tokens / App components
  - ไม่บังคับให้มี `ui.json`

---

## 9. โครง `tasks.md` ที่คาดหวัง

### 9.1 Global Implementation Rules

`tasks.md` ควรเริ่มต้นด้วยบล็อค rule เช่น:

```markdown
> IMPLEMENTATION RULES
> - อ่าน spec.md, plan.md (ถ้ามี) และ registry ที่เกี่ยวข้องให้ครบก่อนเริ่มเขียนโค้ด
> - ห้าม reimplement API/model/UI component ที่มี owner ชัดเจนใน registry/SPEC_INDEX
> - ถ้ามี cross-repo owner ให้ reuse ผ่าน boundary/integration ที่กำหนดเท่านั้น
> - ทำตาม Resource usage metadata (reuse/create) อย่างเคร่งครัด
> - เคารพ UI mode (json/inline) และ design system เสมอ
> - ถ้า spec หรือ plan ถูกแก้หลังจาก generated_at → ต้อง regenerate tasks.md ใหม่
> - ถ้าเจอความขัดแย้งระหว่าง spec/plan/tasks → หยุดและทำ T999 Reconciliation ก่อน
> - ห้ามใส่ secret / token / password / PII ลงใน tasks.md หรือ example ใด ๆ
```

### 9.2 Header Metadata

ตัวอย่าง header:

```yaml
Tasks metadata:
  spec_id: <spec-id>
  spec_version: <front-matter | git-hash | UNKNOWN>
  index_path: <SPEC_INDEX path | UNKNOWN>
  generated_at: <timestamp>
  generated_by: /smartspec_generate_tasks v5.6.4
  safety_mode: strict | dev
  safety_status: SAFE | UNSAFE | DEV-ONLY
```

Rule:

- `SAFE` เฉพาะตอน strict mode + ไม่มี conflict/blocker
- `UNSAFE` เมื่อ strict เจอปัญหาหนัก (conflict owner, web-stack ไม่ปลอดภัย, index/registry fail)
- `DEV-ONLY` สำหรับ dev mode หรือรันบน context ที่ไม่ครบ

### 9.3 หมวดงานและ Subtasks

หมวดหลัก (อาจแตกต่างตามสภาพจริง):

1. Setup & Baseline
2. Core Implementation
3. Cross-SPEC / Shared Work
4. Integrations
5. Testing
6. Observability & Ops
7. Security
8. UI & UX
9. AI/LLM & Data-Sensitivity (ถ้ามี)

Subtasks (`T001.1`, `T001.2`, …) จะ:

- แบ่งงานให้ atomic พอสำหรับ estimation/assign
- ระบุ dependency ระหว่าง task ที่ต้องทำก่อน-หลัง

---

## 10. ตัวอย่าง Resource Usage Metadata

ภายในแต่ละ task/subtask แนะนำให้มี metadata แนวนี้:

```yaml
Resource usage:
  type: reuse | create
  chain_owner:
    api_owner: <spec-id|null>
    model_owner: <spec-id|null>
    pattern_owner: <spec-id|null>
    terminology_owner: <spec-id|null>
  registry:
    api: <entry-id|null>
    model: <entry-id|null>
    ui_component: <entry-id|null>
  files:
    - <path-or-glob>
  justification: <short description>
  repo_context:
    owner_repo: <id|unknown>
    consumer_repo: <id|current>
```

---

## 11. Reconciliation Task (T999)

ทุก `tasks.md` ควรมี task สุดท้าย เช่น:

```markdown
T999 — SPEC/PLAN/TASK Alignment Review
- ตรวจว่า spec.md, plan.md (ถ้ามี) และ tasks.md ไม่ขัดแย้งกัน
- ตรวจว่า directive reuse/create ยัง align กับ registry/SPEC_INDEX
- ตรวจว่า guardrail web-stack, AI, data-sensitivity ถูก implement ตามที่ระบุใน task
- ถ้าพบ mismatch ให้แก้ spec/plan ก่อน แล้ว regenerate tasks.md
```

---

## 12. KiloCode Usage Examples

### 12.1 ใช้ Kilo สร้าง tasks พร้อม orchestrator

```bash
smartspec_generate_tasks \
  specs/payments/spec-pay-001-checkout/spec.md \
  --index=.spec/SPEC_INDEX.json \
  --registry-dir=.spec/registry \
  --kilocode \
  --stdout-summary
```

เมื่อรันบน Kilo:

- Orchestrator จะแบ่ง subtasks ต่อ spec ตาม dependency order
- code-mode จะอ่าน spec/plan/index/registry แล้วเขียน `tasks.md` ตาม guardrail

### 12.2 ปิด subtasks เมื่อ scope เล็ก

```bash
smartspec_generate_tasks \
  specs/tools/spec-tools-001-linter/spec.md \
  --index=.spec/SPEC_INDEX.json \
  --registry-dir=.spec/registry \
  --kilocode \
  --nosubtasks \
  --stdout-summary
```

---

## 13. Best Practices

- สำหรับงานที่มุ่งสู่ production:
  - ใช้ `--safety-mode=strict` เสมอ
  - ตรวจ `safety_status` ใน header ให้เป็น `SAFE`
- ใช้ `--dry-run` หรือ `--nogenerate` ครั้งแรกที่รันใน repo ใหม่
- ดูแล `.spec/SPEC_INDEX.json` และ `.spec/registry/` ให้ทันสมัย
- ตั้ง `--repos-config` ใต้ `.spec/` ในระบบ multi-repo เพื่อลด path brittle
- ตัดสินใจเรื่อง UI mode ต่อ spec ให้ชัดเจน แล้วใช้ให้สอดคล้อง
- สำหรับ web stack:
  - align dependency กับ `tool-version-registry.json`
  - ใส่ tasks เรื่อง RSC/SSR/Edge hardening เสมอ
- สำหรับ AI/LLM:
  - treat model เป็น untrusted → ต้องมี guardrail + red-team test
  - ห้ามใช้ data จริงใน example/prompt/template ใน `tasks.md`
- สำหรับข้อมูลอ่อนไหว:
  - ระบุ data classification + masking ใน spec แล้วให้ tasks สะท้อนตามนั้น
  - เชื่อมต่อกับ DLP / secret scanner / SCA tool ให้ครบ

---

## 14. FAQ สั้น ๆ

**Q: ถ้ายังไม่มี SPEC_INDEX จะทำยังไง?**  
A: ใช้ได้ โดยเฉพาะใน `--safety-mode=dev` ก่อน แล้วดูว่ามี Phase 0 task ให้ bootstrap SPEC_INDEX  
สำหรับ production แนะนำให้สร้าง SPEC_INDEX ให้เรียบร้อยก่อน แล้ว regenerate tasks อีกครั้ง

**Q: สามารถเขียน `tasks.md` ข้าม repo ได้ไหม?**  
A: ไม่ได้ workflow จำกัดให้เขียนใน repo ปัจจุบันเท่านั้น repo อื่นเป็น read-only เสมอ

**Q: ต้องมี plan.md ก่อน generate_tasks เสมอไหม?**  
A: ไม่จำเป็น แต่ถ้ามี `plan.md` อยู่แล้ว tasks จะ align กับ phase/sequence ที่ plan กำหนดไว้ดีกว่า

**Q: ใช้ Kilo แล้ว behavior ต่างจากไม่ใช้ยังไง?**  
A: ภาพรวมเหมือนกัน แต่บน Kilo Orchestrator จะช่วยแตก subtasks ให้เป็นระบบมากขึ้น (โดยเฉพาะเวลารันหลาย spec พร้อมกัน)

---

