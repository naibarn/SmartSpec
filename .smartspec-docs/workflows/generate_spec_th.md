---
manual_name: /smartspec_generate_spec Manual (TH)
manual_version: 5.6
compatible_workflow: /smartspec_generate_spec
compatible_workflow_versions: 5.6.1 – 5.6.x
role: user/operator manual (architect, backend/frontend lead, platform, spec owner)
---

# /smartspec_generate_spec คู่มือการใช้งาน (v5.6, ภาษาไทย)

## 1. ภาพรวม (Overview)

คู่มือนี้อธิบายวิธีใช้งาน workflow:

> `/smartspec_generate_spec v5.6.x` (เช่น v5.6.1)

workflow นี้เป็น **ชั้น execution สำหรับสร้าง/ซ่อม `spec.md`** โดยเน้น:

- จัดโครง spec ให้พร้อมใช้กับ workflow รุ่น v5.6 อื่น ๆ เช่น
  - `/smartspec_generate_plan`
  - `/smartspec_generate_tasks`
  - `/smartspec_generate_tests`
  - `/smartspec_release_readiness`
- รักษา **centralization** ผ่าน `.spec/`, `SPEC_INDEX`, registry ต่าง ๆ
- ใส่บริบท **multi-repo / multi-registry** อย่างปลอดภัย ไม่สร้าง spec หรือ entity ซ้ำ
- รองรับ **UI mode** ทั้ง JSON-first (`ui.json`) และ inline UI ใน `spec.md`
- รองรับการใช้งานในโหมด KiloCode (`--kilocode`) พร้อม Orchestrator-per-task

> **สำคัญ:**
> - workflow นี้มี `write_guard: ALLOW-WRITE` แต่จำกัดการเขียนอยู่ใน repo ปัจจุบันเท่านั้น
> - เคารพ `--dry-run` เสมอ ถ้าเปิดจะไม่เขียนไฟล์จริง
> - ไม่ลบ flag/function เดิมใด ๆ ทั้งหมด behavior เก่าอยู่ครบ เพิ่มเฉพาะความสามารถใหม่แบบ additive

### 1.1 ใช้เมื่อไร

ใช้ `/smartspec_generate_spec` เมื่อคุณต้องการ:

- สร้าง spec ใหม่ภายใต้ `specs/**/` ให้ตรงมาตรฐาน SmartSpec
- ซ่อม/อัปเกรด spec เก่าให้เข้า v5.6 (แต่ไม่เปลี่ยน meaning เดิม)
- เพิ่ม metadata/section ที่ workflow อื่นต้องการ (เช่น ownership, dependency, migration, UI mode)
- เตรียม spec ให้พร้อมใช้กับ chain ของ generate_plan → generate_tasks → generate_tests
- รองรับการทำงานข้าม repo โดยอิง SPEC_INDEX และ registry

ไม่ควรใช้เพื่อ:

- แก้ไขเอกสารอื่นที่ไม่ใช่ `spec.md` (เช่น README, ADR) แบบ mass-edit
- แก้ `tasks.md` โดยตรง (ให้ใช้ workflow generate_tasks แยก)

### 1.2 ปัญหาที่ workflow นี้ช่วยแก้

- spec เขียนแบบกระจัดกระจาย ไม่มี structure → generate tasks ได้ไม่ดี/ไม่ครบ
- ไม่มี SPEC_INDEX / registry ทำให้ ownership ไม่ชัด ซ้ำซ้อนข้าม repo
- UI ไม่ชัดว่าใช้ JSON-first หรือ inline → สมอง AI/ทีมสับสน / generate ui.json มั่ว
- multi-repo: หลายทีมเขียน spec เอาเองจนเกิด entity ซ้ำ เช่น API, data model, glossary

`/smartspec_generate_spec` ทำให้คุณมี spec ที่ "พร้อมต่อท่อ" ไปยัง workflow อื่น ๆ ได้อย่างปลอดภัย

---

## 2. What’s New in v5.6

### 2.1 การจัดรูปแบบตาม SmartSpec v5.6 chain

- โครง spec ถูกออกแบบให้สอดคล้องกับ chain:
  - spec → plan → tasks → tests → release readiness
- เน้น section ที่ workflow downstream ใช้ได้จริง เช่น
  - Functional / Non-functional Requirements
  - Ownership & Reuse
  - Dependencies & Integration
  - Data Models / APIs
  - Security / Observability / Migration

### 2.2 รองรับ multi-repo / multi-registry อย่างเป็นระบบ

- รองรับ flag `--workspace-roots`, `--repos-config` เพื่อ map spec ข้าม repo แบบปลอดภัย
- เพิ่มการใช้ `--registry-dir` + `--registry-roots` แยก primary registry กับ registry เสริม (read-only)
- มี rule ชัดเจนเรื่อง **Reuse vs Implement** เมื่อเจอ entity ที่มี owner อยู่ใน repo อื่น

### 2.3 UI mode governance (JSON-first vs inline)

- รองรับ `--ui-mode=auto|json|inline` + alias `--no-ui-json`
- มี precedence ชัดว่าตัดสินยังไงว่า spec นี้ควรใช้ ui.json หรือ inline
- align กับแนวคิด JSON-first UI ที่ใช้ `ui.json` เป็น source-of-truth

### 2.4 KiloCode support + Orchestrator-per-task

- รองรับ `--kilocode`, `--nosubtasks`
- เมื่อทำงานบน Kilo จะใช้ Orchestrator ช่วยจัดการทีละ spec พร้อม subtasks
- ทำให้การสร้าง spec หลายตัวพร้อมกัน ปลอดภัยและมีโครงที่เสถียรกว่าให้ AI จัดการเองคนเดียว

### 2.5 Output & reporting แบบใหม่

- เพิ่ม `--report-dir` กำหนดที่เก็บ report ได้
- เพิ่ม `--stdout-summary` ให้สรุปผลสั้น ๆ ทาง stdout
- สร้าง report ใต้ `.spec/reports/generate-spec/` พร้อมรายละเอียด index/registry/safety-mode/UI mode

---

## 3. Backward Compatibility Notes

- คู่มือนี้ใช้กับ `/smartspec_generate_spec v5.6.1 – 5.6.x`
- flags เดิม **ยังใช้ได้ทั้งหมด**:
  - `--index`, `--registry-dir`, `--workspace-roots`, `--repos-config`,
    `--new`, `--repair-legacy`, `--repair-additive-meta`, `--mode`,
    `--safety-mode`, `--strict`, `--dry-run`, `--ui-mode`, `--no-ui-json`
- flags ใหม่เป็นเพียง **alias/ส่วนเสริม** เช่น
  - `--specindex`, `--registry-roots`, `--report-dir`, `--stdout-summary`,
    `--kilocode`, `--nosubtasks`
- behavior เดิม เช่น dev vs strict, recommend vs additive สำหรับ registry ยังเหมือนเดิม

---

## 4. Core Concepts

### 4.1 SPEC_INDEX และ registry

- `SPEC_INDEX` คือแผนที่กลางของ spec ทั้งระบบ
- `registry` คือแหล่งเก็บ entity กลางที่ควร reuse เช่น:
  - API, data model, glossary, critical sections, UI components
- generate_spec จะอ่าน index + registry เพื่อ:
  - รู้ว่า spec ใหม่ต้องไปอยู่ตรงไหนในโครง
  - รู้ว่า entity ไหนห้ามสร้างซ้ำ

### 4.2 UI mode

สามโหมดหลัก:

- `auto` (ค่าเริ่มต้น)
  - ให้ workflow ช่วยตัดสินจาก context ว่าควรใช้ json หรือ inline
- `json`
  - เน้น JSON-first UI → ใช้ `ui.json` เป็น source-of-truth ของ layout/structure
- `inline`
  - เขียนรายละเอียด UI อยู่ใน `spec.md` โดยไม่บังคับ ui.json

### 4.3 Safety mode

- `--safety-mode=strict` (default)
  - เข้มเรื่อง registry/ownership/cross-SPEC conflicts
- `--safety-mode=dev`
  - ผ่อนคลายขึ้นสำหรับ dev sandbox / PoC แต่จะใส่ warning ใน report/สเปก

### 4.4 Multi-repo

- ใช้ `--repos-config` + `--workspace-roots` เพื่อให้ generate_spec เข้าใจว่า spec อื่น ๆ อยู่ที่ไหน
- เมื่อ spec ใน repo เราอ้างถึง entity ที่ owner อยู่ใน repo อื่น:
  - spec ต้องสะท้อนว่า **ต้อง reuse** ไม่ใช่เขียนใหม่ซ้ำ

### 4.5 Write guard

- write_guard = `ALLOW-WRITE`
- เขียนได้เฉพาะใน
  - `specs/**/spec.md`
  - `.spec/` (index, registry, reports)
- ห้ามเขียนไปยัง repo อื่นที่เจอจาก workspace-roots/repos-config

---

## 5. Quick Start Examples

### 5.1 สร้าง spec ใหม่ใน service เดียว (strict mode)

```bash
smartspec_generate_spec \
  specs/payments/spec-pay-001-checkout/spec.md \
  --index=.spec/SPEC_INDEX.json \
  --registry-dir=.spec/registry \
  --safety-mode=strict \
  --ui-mode=auto \
  --stdout-summary
```

### 5.2 ซ่อม spec legacy ให้ align v5.6

```bash
smartspec_generate_spec \
  specs/legacy/spec-legacy-001/spec.md \
  --repair-legacy \
  --repair-additive-meta \
  --index=.spec/SPEC_INDEX.json \
  --registry-dir=.spec/registry \
  --safety-mode=dev \
  --dry-run \
  --stdout-summary
```

### 5.3 ใช้ dev mode เพื่อเริ่มต้นโปรเจกต์ใหม่ที่ยังไม่มี index/registry

```bash
smartspec_generate_spec \
  specs/newapp/spec-newapp-001/spec.md \
  --safety-mode=dev \
  --mode=recommend \
  --report-dir=.spec/reports/generate-spec/ \
  --stdout-summary
```

---

## 6. CLI / Flags Cheat Sheet

- Index & registry
  - `--index`, `--specindex` (alias)
  - `--registry-dir`
  - `--registry-roots`
- Multi-repo
  - `--workspace-roots`
  - `--repos-config`
- Generation / repair
  - `--new`
  - `--repair-legacy`
  - `--repair-additive-meta`
- Registry update mode
  - `--mode=recommend|additive`
- Safety
  - `--safety-mode=strict|dev`
  - `--strict`
  - `--dry-run`
- UI mode
  - `--ui-mode=auto|json|inline`
  - `--no-ui-json`
- Output & Kilo
  - `--report-dir`
  - `--stdout-summary`
  - `--kilocode`
  - `--nosubtasks`

---

## 7. Multi-repo / Multi-registry Examples

### 7.1 Monorepo ที่มีหลาย service

```bash
smartspec_generate_spec \
  specs/billing/spec-bill-002-invoice/spec.md \
  --index=.spec/SPEC_INDEX.json \
  --registry-dir=.spec/registry \
  --workspace-roots="." \
  --mode=recommend \
  --stdout-summary
```

### 7.2 หลาย repo หลายทีม + registry กลาง

```bash
smartspec_generate_spec \
  specs/notifications/spec-notif-003-email/spec.md \
  --specindex=../platform/.spec/SPEC_INDEX.json \
  --registry-dir=.spec/registry \
  --registry-roots="../platform/.spec/registry" \
  --workspace-roots="../platform;../billing" \
  --repos-config=.spec/smartspec.repos.json \
  --mode=additive \
  --safety-mode=strict \
  --stdout-summary
```

---

## 8. UI JSON vs Inline UI Examples

### 8.1 JSON-first UI (มี ui.json)

```bash
smartspec_generate_spec \
  specs/web/spec-web-001-dashboard/spec.md \
  --ui-mode=json \
  --index=.spec/SPEC_INDEX.json \
  --registry-dir=.spec/registry \
  --stdout-summary
```

ลักษณะนี้ spec จะคาดหวังให้มี `ui.json` คู่กัน (หรือถูกสร้าง/ซ่อมตาม policy) และระบุ
structure/layout ในมุม declarative โดยไม่มี business logic

### 8.2 Inline UI (ไม่มี ui.json)

```bash
smartspec_generate_spec \
  specs/legacy/spec-legacy-ui-001/spec.md \
  --ui-mode=inline \
  --index=.spec/SPEC_INDEX.json \
  --registry-dir=.spec/registry \
  --stdout-summary
```

กรณีนี้ UI จะถูกอธิบายใน `spec.md` โดยตรง และ workflow จะไม่พยายามบังคับให้มี `ui.json`

---

## 9. KiloCode Usage Examples

### 9.1 ใช้ Kilo สร้าง spec หลายตัวพร้อมกัน

```bash
smartspec_generate_spec \
  specs/payments/spec-pay-001-checkout/spec.md \
  --index=.spec/SPEC_INDEX.json \
  --registry-dir=.spec/registry \
  --kilocode \
  --stdout-summary
```

เมื่อรันบน Kilo:

- Orchestrator จะจัดการ subtasks เช่นอ่าน index, registry, spec เดิม
- code-mode จะทำการ generate/repair spec แบบยึด safety-mode และ write guard

### 9.2 ปิด subtasks เมื่อ scope เล็ก

```bash
smartspec_generate_spec \
  specs/tools/spec-tools-001-linter/spec.md \
  --index=.spec/SPEC_INDEX.json \
  --registry-dir=.spec/registry \
  --kilocode \
  --nosubtasks \
  --stdout-summary
```

---

## 10. Best Practices

- ใช้ `--safety-mode=strict` เป็นค่า default สำหรับ spec ที่มีผลต่อ production
- ใช้ `--dry-run` ก่อนรันจริงในครั้งแรกของแต่ละ repo/config
- ตั้ง `.spec/SPEC_INDEX.json` และ `.spec/registry/` ตั้งแต่ต้นของโปรเจกต์
- แยก owner ชัดเจนใน registry (API, model, UI component)
- ตัดสินใจเรื่อง UI mode ให้ชัดและใช้คงเส้นคงวาในทั้งระบบ
- สำหรับ AI-generated `ui.json`:
  - ใส่ meta (source, generator, design_system_version, style_preset, review_status)
  - หลีกเลี่ยงการ embed business logic ลงใน JSON

---

## 11. Risks if you don’t use (or misuse) this workflow

- spec กระจัดกระจาย ไม่รองรับ generate_plan/tasks/tests อย่างเสถียร
- entity สำคัญ (API/model/glossary) ถูกนิยามซ้ำหลายที่ ในหลาย repo
- UI spec ไม่ชัดว่าใช้ JSON-first หรือ inline → ทำให้ AI/ทีมใช้ pattern ไม่สอดคล้อง
- multi-repo dependency ถูกเขียนแบบ re-implement แทน reuse → เกิด drift และ bug

---

## 12. FAQ / Troubleshooting

**Q1: ถ้ายังไม่มี SPEC_INDEX หรือ registry เลย จะใช้ได้ไหม?**  
ใช้ได้ โดยเฉพาะใน `--safety-mode=dev` แต่ report จะเตือนว่าควรสร้าง index/registry ให้เรียบร้อย

**Q2: workflow นี้จะแก้ tasks.md ให้ด้วยไหม?**  
ไม่ใช่หน้าที่ของ `/smartspec_generate_spec` มันจะเตรียม spec ให้พร้อม แล้วให้ workflow อื่น
generate tasks/tests ต่อไป

**Q3: ต้องใช้ UI JSON เสมอไหม?**  
ไม่จำเป็น สามารถใช้ `--ui-mode=inline` สำหรับระบบ legacy หรือโปรเจกต์ที่ยังไม่พร้อม
ใช้ JSON-first UI ได้

**Q4: ใช้ Kilo แล้วจะไปเขียนไฟล์ใน repo อื่นไหม?**  
ไม่ ตัว workflow จำกัดการเขียนไว้เฉพาะ repo ปัจจุบันเท่านั้น repo อื่นที่พบจาก
`--workspace-roots`/`--repos-config` ถูกมองเป็น read-only เสมอ

---

จบคู่มือภาษาไทยสำหรับ `/smartspec_generate_spec v5.6.1 – 5.6.x`.
หากในอนาคตมีการเปลี่ยน semantics ของ safety-mode, UI mode หรือ multi-repo behavior
อย่างมีนัยสำคัญ ควรออก manual v5.7 ใหม่พร้อมระบุช่วงเวอร์ชัน workflow ที่รองรับให้ชัดเจน

