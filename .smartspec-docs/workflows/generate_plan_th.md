---
manual_name: /smartspec_generate_plan Manual (TH)
manual_version: 5.6
compatible_workflow: /smartspec_generate_plan
compatible_workflow_versions: 5.6.2 – 5.6.x
role: user/operator manual (architect, tech lead, PM, platform, spec owner)
---

# /smartspec_generate_plan คู่มือการใช้งาน (v5.6, ภาษาไทย)

## 1. ภาพรวม (Overview)

คู่มือนี้อธิบายวิธีใช้งาน workflow:

> `/smartspec_generate_plan v5.6.x` (เช่น v5.6.2)

workflow นี้เป็น **ชั้นวางแผน (planning layer)** ใน SmartSpec chain
สำหรับสร้าง/อัปเดตเอกสารแผนงานระดับสูง (`plan.md`) ที่มีลำดับ
งานตาม dependency และพร้อมใช้ต่อกับ workflow สร้าง tasks.

ลำดับ chain หลัก:

1. `/smartspec_validate_index`
2. `/smartspec_generate_spec`
3. `/smartspec_generate_plan`
4. `/smartspec_generate_tasks`
5. `/smartspec_sync_spec_tasks`

เป้าหมายหลักของ `/smartspec_generate_plan` คือ:

- สร้างแผนที่ **พร้อมต่อท่อไป generate_tasks ได้ทันที**
- ลดความเสี่ยงเรื่องความซ้ำซ้อนของ entity ข้าม spec / ข้าม repo
- เคารพ **UI mode** (JSON-first vs inline) ให้สอดคล้องกับ spec และ
  workflow UI อื่น ๆ
- ทำงานแบบ **governance-aware**: ไม่เดา requirement ใหม่โดยไม่บอก
- รองรับ multi-repo / multi-registry อย่างปลอดภัย
- รองรับ KiloCode (`--kilocode`) และ Orchestrator-per-task

> **Note v5.6.2**
> - เพิ่มแนวคิด `safety_status = SAFE | UNSAFE | DEV-ONLY` ในแผนและ
>   report
> - เพิ่ม `--run-label`, `--plan-layout` เพื่อให้การ track plan run
>   ชัดเจน
> - เพิ่มกติกาการใช้สัญญาณจาก AI UI JSON / UI workflows
> - ไม่ลบ flag เดิมออกแม้แต่ตัวเดียว เพิ่มทุกอย่างแบบ additive

---

## 2. ใช้เมื่อไร (When to Use)

ใช้ `/smartspec_generate_plan` เมื่อ:

- เริ่ม feature/program ใหม่ที่เกี่ยวข้องกับหลาย spec
- อยากสร้างภาพรวมงาน (phases) ก่อนสลายเป็น tasks
- เตรียมจะเรียก `/smartspec_generate_tasks` กับหลาย spec พร้อมกัน
- ต้อง re-plan หลังมีการเปลี่ยน ownership, refactor, หรือ reindex
- มี multi-repo หลายทีมใช้ registry ร่วมกัน และต้องการแผนที่ไม่
  ทำให้เกิด entity ซ้ำ

ไม่ควรใช้เมื่อ:

- ต้องการแค่ generate tasks ของ spec เดียวที่ scope ชัดเจน →
  ใช้ `/smartspec_generate_tasks` ตรง ๆ ก็พอ
- ต้องการแก้ไข `spec.md` หรือ `tasks.md` โดยตรง → ใช้ workflow
  อื่น
- องค์กรกำหนดว่าต้องเขียนแผนด้วยมืออย่างเดียว (เช่น เหตุผล
  ด้าน audit)

---

## 3. แนวคิดสำคัญ (Core Concepts)

### 3.1 SPEC_INDEX และ registry

- `SPEC_INDEX` = แผนที่กลางของ spec ทั้งระบบ
- `registry` = แหล่งรวม entity ที่ควร reuse ไม่ใช่สร้างซ้ำ เช่น
  - API registry
  - data model registry
  - glossary
  - critical sections
  - UI component registry

`/smartspec_generate_plan` ใช้ index + registry เพื่อ:

- รู้ว่า spec ไหนมี dependency กันยังไง
- รู้ว่า entity ไหนเป็นของกลาง ห้ามสร้างใหม่ทับ

### 3.2 Safety mode และ safety_status

- `--safety-mode=strict` (ค่าเริ่มต้น)
  - เข้มเรื่อง ownership และ duplication
  - ถ้ามี ambiguity หรือ conflict ที่อาจทำให้สร้าง entity ซ้ำ →
    แผนจะถูก mark เป็น `safety_status=UNSAFE` หรือไม่อนุญาตให้
    treat ว่า "พร้อม run" โดยอัตโนมัติ
- `--safety-mode=dev`
  - เหมาะกับ sandbox / PoC / exploration
  - ยอมปล่อยแผนแม้ index/registry ยังไม่ครบ แต่จะติด `DEV-ONLY`
  - ไม่ควรใช้ DEV-ONLY plan เป็นแผน release โดยไม่ review

ทุกแผนต้องมี header ที่มีอย่างน้อย:

- spec_ids ที่อยู่ใน scope
- path ของ SPEC_INDEX ที่ใช้
- run-label (ถ้ามี)
- timestamp
- `safety_status = SAFE | UNSAFE | DEV-ONLY`

### 3.3 Alignment ระหว่าง spec ↔ plan ↔ tasks

- `spec.md` คือ source-of-truth ของ requirement
- แผนต้อง **ไม่แต่ง requirement ใหม่เองเงียบ ๆ**
- ถ้า spec ไม่ชัด → แผนควรสร้าง task/phase ว่า "ต้องเติม/แก้
  spec ก่อน" (ไม่ใช่เดา requirement แทนทีม)
- `/smartspec_generate_tasks` ควรอ้างอิงทั้ง spec และ plan ร่วมกัน

### 3.4 UI mode และ AI UI JSON

- รองรับ `--ui-mode=auto|json|inline`
- ถ้า `json` → จะถือว่าใช้ JSON-first UI (มี `ui.json` เป็นแหล่ง
  design หลัก)
- ถ้า `inline` → UI อยู่ใน `spec.md` ไม่บังคับให้มี `ui.json`
- แผนต้องวางขั้นตอนให้ถูกกับ UI mode เช่น
  - มี phase สำหรับ create/review `ui.json` เมื่อเป็น JSON-first
  - ถ้ามีสัญญาณจาก workflow UI อื่น เช่น
    `ui_spec_origin`, `ui_spec_review_status`,
    `ui_json_quality_status` → ต้องมี phase สำหรับ review/remediation

---

## 4. Inputs / Outputs

### 4.1 Inputs (Artifacts)

- SPEC_INDEX (ถ้ามี)
- registry หลายชุด (primary + supplemental)
- `spec.md` ของ spec ที่จะวางแผน
- `plan.md` เดิม (ถ้ามี) เพื่อใช้ซ่อม/ต่อยอด
- `tasks.md` / report อื่น ๆ (อ่านเพื่อเข้าใจบริบท ไม่แก้)
- รายงาน/metadata จาก UI workflows (ถ้ามี) เพื่อใช้สร้าง phase
  review UI

### 4.2 Inputs (Flags ที่ใช้บ่อย)

- scope
  - `--spec=<path>`
  - `--spec-ids=<id1,id2,...>`
- index & registry
  - `--index`, `--specindex`
  - `--registry-dir`, `--registry-roots`
- multi-repo
  - `--workspace-roots`
  - `--repos-config`
- identity & layout
  - `--run-label`
  - `--plan-layout=per-spec|consolidated`
  - `--output`
- safety & UI
  - `--safety-mode`, `--strict`, `--dry-run`
  - `--ui-mode`
- reporting & Kilo
  - `--report-dir`, `--stdout-summary`
  - `--kilocode`, `--nosubtasks`

### 4.3 Outputs

- `plan.md` (หรือไฟล์ตาม `--output`) พร้อม header safety_status
- รายงานใน `.spec/reports/generate-plan/` (หรือ `--report-dir`)
  - มีรายละเอียด index/registry/scope/safety_status/คำเตือน

---

## 5. ตัวอย่างการใช้งาน (Quick Start)

### 5.1 วางแผนให้ spec เดียวแบบ strict

```bash
smartspec_generate_plan \
  --spec=specs/payments/spec-pay-001-checkout/spec.md \
  --index=.spec/SPEC_INDEX.json \
  --registry-dir=.spec/registry \
  --safety-mode=strict \
  --run-label=checkout-v2-planning \
  --stdout-summary
```

ผลลัพธ์:
- สร้าง/อัปเดต `plan.md` ข้าง `spec.md`
- ใส่ header `safety_status` และ run-label
- สร้าง report ใต้ `.spec/reports/generate-plan/`

### 5.2 scope หลาย spec + plan แยกต่อ spec

```bash
smartspec_generate_plan \
  --spec-ids=payments.checkout,identity.login \
  --index=.spec/SPEC_INDEX.json \
  --registry-dir=.spec/registry \
  --plan-layout=per-spec \
  --safety-mode=strict \
  --run-label=release-2024Q4 \
  --stdout-summary
```

ผลลัพธ์:
- เขียน `plan.md` ข้าง `spec.md` ของแต่ละ spec
- ใช้ dependency graph จาก SPEC_INDEX เพื่อจัดลำดับ phase

### 5.3 วางแผนแบบ consolidated ให้เป็นไฟล์เดียว

```bash
smartspec_generate_plan \
  --spec-ids=payments.checkout,identity.login \
  --index=.spec/SPEC_INDEX.json \
  --registry-dir=.spec/registry \
  --plan-layout=consolidated \
  --output=plans/release-2024Q4-plan.md \
  --run-label=release-2024Q4 \
  --safety-mode=strict \
  --stdout-summary
```

---

## 6. Multi-repo / Multi-registry Examples

### 6.1 Monorepo หลาย service

```bash
smartspec_generate_plan \
  --spec-ids=billing.invoice,notifications.email \
  --index=.spec/SPEC_INDEX.json \
  --registry-dir=.spec/registry \
  --workspace-roots="." \
  --plan-layout=per-spec \
  --safety-mode=strict \
  --stdout-summary
```

### 6.2 หลาย repo หลายทีม + platform registry กลาง

```bash
smartspec_generate_plan \
  --spec-ids=teamA.web_portal,teamB.mobile_app \
  --specindex=../platform/.spec/SPEC_INDEX.json \
  --registry-dir=.spec/registry \
  --registry-roots="../platform/.spec/registry" \
  --workspace-roots="../platform,../teamA,../teamB" \
  --repos-config=.spec/smartspec.repos.json \
  --plan-layout=consolidated \
  --output=.spec/plans/cross-team-2024Q4.md \
  --safety-mode=strict \
  --stdout-summary
```

ในแผนจะมี note ชัดเจนว่าบาง spec/entity เป็น **external dependency**
และต้อง reuse จาก repo อื่น ไม่ใช่สร้างใหม่

---

## 7. UI JSON vs Inline UI Examples

### 7.1 UI JSON-first + AI ui.json

```bash
smartspec_generate_plan \
  --spec=specs/web/spec-web-001-dashboard/spec.md \
  --index=.spec/SPEC_INDEX.json \
  --registry-dir=.spec/registry \
  --ui-mode=json \
  --run-label=dashboard-ui-v3 \
  --safety-mode=strict \
  --stdout-summary
```

แผนที่สร้างควรมี phase อย่างน้อย:
- Align `ui.json` กับ design system / UI registry
- Review AI-generated `ui.json` (ถ้า meta บอกว่า `source=ai` และ
  `review_status=unreviewed`)
- แยก logic ระหว่าง layout vs business rules

### 7.2 Legacy UI (inline)

```bash
smartspec_generate_plan \
  --spec=specs/legacy/spec-legacy-ui-001/spec.md \
  --index=.spec/SPEC_INDEX.json \
  --registry-dir=.spec/registry \
  --ui-mode=inline \
  --safety-mode=dev \
  --run-label=legacy-ui-cleanup \
  --stdout-summary
```

กรณีนี้แผนจะเน้น phase ที่เกี่ยวกับการ refactor UI จาก spec เดิม
โดยไม่บังคับให้มี `ui.json` แต่ยังสามารถแนะนำให้ค่อย ๆ ย้ายไป
JSON-first ในอนาคตได้

---

## 8. การใช้บน KiloCode (Kilo)

### 8.1 ใช้ Kilo วางแผนหลาย spec พร้อมกัน

```bash
smartspec_generate_plan \
  --spec-ids=payments.checkout,identity.login \
  --index=.spec/SPEC_INDEX.json \
  --registry-dir=.spec/registry \
  --kilocode \
  --plan-layout=per-spec \
  --run-label=release-2024Q4 \
  --safety-mode=strict \
  --stdout-summary
```

บน Kilo:

- Orchestrator จะสร้าง subtasks ต่อ spec โดยจัดลำดับตาม dependency
  จาก SPEC_INDEX
- code-mode จะอ่าน spec/index/registry แล้ว generate plan ราย spec
- ถ้า scope ใดได้ `safety_status=UNSAFE` → run รวมถือว่า UNSAFE

### 8.2 ปิด subtasks ในเคสเล็ก

```bash
smartspec_generate_plan \
  --spec=specs/tools/spec-tools-001-linter/spec.md \
  --index=.spec/SPEC_INDEX.json \
  --registry-dir=.spec/registry \
  --kilocode \
  --nosubtasks \
  --run-label=tools-linter-plan \
  --stdout-summary
```

---

## 9. Best Practices

- ใช้ `--safety-mode=strict` สำหรับงานที่ส่งผลต่อ production
- ใช้ `--dry-run` ครั้งแรกในแต่ละ repo หรือ config ใหม่ ๆ
- รักษา `.spec/SPEC_INDEX.json` และ `.spec/registry/` ให้ทันสมัย
  และใช้แผนช่วยวาง phase ยกเครื่องถ้าล้าสมัย
- สื่อสารให้ทีมเข้าใจ concept `safety_status`:
  - SAFE → ใช้ต่อ generate_tasks / execution ได้ (หลัง review พอสมควร)
  - UNSAFE → ต้องแก้ conflict/ambiguity ก่อน
  - DEV-ONLY → ใช้ใน sandbox/PoC เท่านั้น
- ให้ความสำคัญกับ alignment spec ↔ plan → ถ้าไม่ตรง ให้แก้ spec
  ก่อนแล้วค่อย regenerate plan

---

## 10. Risks หากไม่ใช้ (หรือใช้ผิดวิธี)

- chain spec → plan → tasks แตกออกจากกัน ทำให้ทีมทำงานคนละ
  version ของความจริง
- เกิด entity ซ้ำข้าม repo โดยไม่มีใครเห็นในมุมมองแผนรวม
- UI ที่มาจาก AI ui.json ถูกปล่อยผ่านโดยไม่มี phase review
- multi-repo ที่ไม่มี note เรื่อง reuse-not-rebuild นำไปสู่ drift
  และ bug ระยะยาว

---

## 11. FAQ / Troubleshooting

**Q1: ถ้าไม่มี SPEC_INDEX เลย ใช้ได้ไหม?**  
ใช้ได้ แผนจะอยู่ในโหมด local-spec-only และจะมี Phase 0
ให้ตั้งค่า index/registry ก่อนใช้ต่อใน production

**Q2: ถ้าตอนนี้ยังไม่อยากใช้ UI JSON / ai ui.json ต้องทำอย่างไร?**  
ใช้ `--ui-mode=inline` ได้ แล้วค่อยค่อย migrate ไป JSON-first
เมื่อทีมพร้อม

**Q3: safety_status ต้องเชื่อถือแค่ไหน?**  
ถือเป็น signal แรกสำหรับ CI / release board โดยเฉพาะ SAFE vs
UNSAFE ใน strict mode แต่ควรมี human review ก่อนเสมอสำหรับงาน
ใหญ่

**Q4: workflow นี้ไปแก้ spec หรือ tasks ให้ไหม?**  
ไม่ แค่สร้าง/อัปเดตแผน (`plan.md`) และ report เท่านั้น spec กับ
tasks จะถูก generate/แก้ผ่าน workflow เฉพาะทางอื่น

---

จบคู่มือภาษาไทยสำหรับ `/smartspec_generate_plan v5.6.2 – 5.6.x`.
หากมีการเปลี่ยน semantics ของ safety-mode, plan-layout, UI mode หรือ
multi-repo behavior อย่างมีนัยสำคัญ ควรออก manual v5.7 ใหม่พร้อมระบุ
ช่วงเวอร์ชัน workflow ที่รองรับให้ชัดเจน

