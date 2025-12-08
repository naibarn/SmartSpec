---
manual_name: /smartspec_ci_quality_gate Manual (TH)
manual_version: 5.6
compatible_workflow: /smartspec_ci_quality_gate
compatible_workflow_versions: 5.6.2 – 5.6.x
role: user/operator manual (release managers, tech leads, senior ICs)
---

# /smartspec_ci_quality_gate คู่มือการใช้งาน (v5.6, ภาษาไทย)

## 1. ภาพรวม (Overview)

คู่มือนี้อธิบายวิธีใช้งาน workflow:

> `/smartspec_ci_quality_gate v5.6.2`

หน้าที่ของ workflow นี้คือช่วยตอบคำถามว่า:

> “จากมุมมองของ SmartSpec ตอนนี้ **CI pipeline** ของเรามี
> checks และ gates ที่สอดคล้องกับ spec / tasks / registry ครบหรือยัง
> ควรเพิ่ม/ปรับอะไรบ้าง และจะแปลงเป็น CI matrix แบบไหน?”

ลักษณะสำคัญ:

- เป็น **quality / governance workflow** (ไม่ใช่ executor)
- มี `write_guard: NO-WRITE`
  - **ไม่แก้ไข** CI YAML, code, spec, หรือ tasks
  - ทำแค่ **อ่าน** artifacts แล้วสร้าง **CI plan + quality gate definition**
  - เซฟไฟล์ผลลัพธ์ใต้ `.spec/ci/`

จุดประสงค์หลัก:

- สร้าง **CI matrix** ที่ผูกกับ SmartSpec อย่างเป็นระบบ
- กำหนด **minimum quality gates** ที่ทุกทีมควรมีตามประเภท spec
- ช่วยให้ **release readiness** มี evidence จาก CI ที่ชัดเจนและสอดคล้องกัน

---

## 2. What’s New in v5.6

เวอร์ชัน 5.6.2 ของ workflow นี้เพิ่ม/ล็อกพฤติกรรมสำคัญดังนี้:

### 2.1 Strict mode ที่ “มีผลจริง”

- `--safety-mode=strict` (หรือ `--strict`) จะทำให้:
  - test types (unit / integration / contract / security / perf) ที่ระบุ
    ใน spec หรือ tasks แต่ CI ไม่มีเลย → ต้องถูก mark เป็น **required gate**
  - coverage thresholds ที่ spec / policy กำหนดห้ามถูกลดลงในแผน CI
  - การเปลี่ยน shared APIs/models ที่ไม่มี contract tests → ถูกมองเป็น
    CI gating risk ระดับบังคับ

### 2.2 แยก Required vs Proposed checks ใน CI plan

- output ของ workflow จะแยกส่วนเป็น:
  - `Required checks` → มาจาก
    - spec / tasks
    - registry
    - baseline policy ตามประเภท spec
  - `Proposed checks` → ข้อเสนอเพิ่มเติม/การ harden pipeline
- ป้องกันไม่ให้ “ข้อเสนอ” ถูกเข้าใจผิดเป็น requirement

### 2.3 Cross-repo + shared assets พร้อม CI owner

- ใช้ registry (รวมถึง file-ownership ถ้ามี) เพื่อระบุว่าใครเป็น
  **CI owner** ของ shared asset เช่น shared API/model
- pipeline อื่นที่ใช้ shared asset เดียวกันจะถูกแนะนำให้รันแค่
  checks แบบเบา ๆ (เช่น smoke) ลด duplicate heavy suite

### 2.4 UI governance + UI JSON opt-out แบบไม่กำกวม

- แยก JSON-first UI vs inline UI ตาม:
  - การมี `ui.json` ข้าง `spec.md`
  - field/config ใน SPEC_INDEX หรือ project config
- ถ้ามี **UI JSON opt-out** ระดับ project/spec family
  - แผน CI จะ **ไม่บังคับ** job ฝั่ง `ui.json`
  - แต่ยังเสนอ UI test ที่เหมาะกับ inline UI

### 2.5 Baseline CI dimensions ตามประเภท spec

เพื่อกันไม่ให้ CI matrix บางตัว “บางเกินไป” เพราะ spec/tasks เขียนไม่ครบ:

- มี baseline สำหรับ spec type เช่น
  - API/service → lint + unit + integration + contract + coverage
  - library/shared model → lint + unit + contract
  - infra/config → lint infra + validation
- normal mode: ขาด baseline = recommendation
- strict mode: ขาด baseline = required gate

### 2.6 Alignment กับ `/smartspec_release_readiness`

- CI plan ที่สร้างขึ้นถูกออกแบบให้เป็น **หลักฐานหลัก**
  สำหรับ workflow `/smartspec_release_readiness`
- critical gaps ใน CI = potential critical risks ตอน release readiness

---

## 3. Backward Compatibility Notes

- Manual v5.6 ฉบับนี้ใช้กับ `/smartspec_ci_quality_gate` เวอร์ชัน
  **5.6.2 เป็นต้นไป** (5.6.x)
- Workflow นี้เป็นตัวใหม่ (ไม่มี manual legacy ของ CI quality gate ก่อนหน้า)
- กติกาที่สืบทอดมาจาก SmartSpec core:
  - ไม่แก้ code, spec, tasks, registry (NO-WRITE)
  - ใช้ multi-repo flags (`--workspace-roots`, `--repos-config`,
    `--registry-dir`, `--registry-roots`, `--index`, `--specindex`) ให้ตรงกับ
    workflow อื่น
  - รองรับ `--kilocode` โดยอยู่ใน Ask/Architect + Orchestrator-per-dimension

ถ้ามีการอัปเดต workflow patch-level (5.6.3, 5.6.4, …)
แต่ไม่เปลี่ยน semantics ของ flags/modes หลัก
manual ฉบับนี้ยังใช้ได้อยู่

---

## 4. แนวคิดหลัก (Core Concepts)

### 4.1 CI matrix จากมุมมอง SmartSpec

- แต่ละ spec-id → มี requirements ด้านคุณภาพของตัวเอง:
  - ต้องมี unit/integration/contract tests หรือไม่
  - ต้องมี coverage เท่าไร
  - มี security/perf/UI checks ไหม
- workflow จะอ่านจาก:
  - `spec.md`
  - `tasks.md`
  - registries
  - policy baseline ตามประเภท spec

แล้วสรุปเป็น **CI matrix** ที่ map:

- spec → jobs
- jobs → stages
- stages → gates ต่อ environment (`dev` / `staging` / `prod`)

### 4.2 Evidence ที่ workflow ใช้

- SPEC_INDEX (canonical ที่ `.spec/SPEC_INDEX.json`)
- spec + tasks ของ spec-id ใน scope
- registries ต่าง ๆ
- CI config เดิม (ถ้าให้ path)
- test reports / coverage reports เดิม (ถ้าระบุ path)

### 4.3 Scope = ชุดของ spec-id

- ใช้ `--spec-ids=<id1,id2,...>` เป็นหลัก
- สามารถขยายด้วย `--include-dependencies` ผ่าน SPEC_INDEX + registry
- **ห้ามเดา spec-id นอก SPEC_INDEX**

### 4.4 Spec type และ baseline

workflow จะพยายาม infer `spec type` เช่น:

- API/service
- library/shared
- infra/config

แล้วใช้ baseline CI dimensions ต่อ type เพื่อไม่ให้ CI matrix บางเกิน

---

## 5. Quick Start (ตัวอย่างใช้งานเร็ว ๆ)

### 5.1 Single repo, basic CI plan

```bash
smartspec_ci_quality_gate \
  --spec-ids=checkout_api,order_core \
  --ci-label=monorepo-main \
  --target-envs=dev,staging,prod \
  --ci-system=github_actions \
  --ci-output-format=md \
  --stdout-summary
```

ผลลัพธ์:

- ไฟล์: `.spec/ci/ci_quality_gate_monorepo-main.md`
- มีตารางแสดงว่าในแต่ละ environment ต้องมี jobs อะไรบ้าง เช่น
  - lint
  - unit
  - integration
  - contract
  - coverage gate

### 5.2 Strict mode สำหรับ production pipeline

```bash
smartspec_ci_quality_gate \
  --spec-ids=payments_gateway \
  --ci-label=payments-prod-ci \
  --target-envs=prod \
  --ci-system=gitlab_ci \
  --safety-mode=strict \
  --stdout-summary
```

ใน strict mode:

- ถ้า spec/tasks บอกว่าต้องมี contract test แต่ CI config ไม่มีเลย
  → แผน CI จะ mark เป็น required gate
- ถ้า coverage ใน CI ปัจจุบันต่ำกว่าที่ spec/policy กำหนด
  → mark เป็น required improvement

### 5.3 Multi-repo และ shared registry

```bash
smartspec_ci_quality_gate \
  --spec-ids=teamA_payments,teamB_notifications \
  --ci-label=multi-team-ci \
  --target-envs=staging,prod \
  --repos-config=.spec/repos.yaml \
  --registry-dir=.spec/registry \
  --registry-roots="../platform/.spec/registry" \
  --ci-system=generic \
  --ci-output-format=yaml
```

กรณีนี้:

- CI plan จะ map spec แต่ละตัวไปที่ repo/service ที่เป็นเจ้าของ
- ใช้ platform registry เพื่อตรวจว่า shared API/model ไหนต้องมี
  contract tests และ pipeline ไหนควรเป็น CI owner

---

## 6. CLI / Flags Cheat Sheet

> เน้นมุมมองคนใช้จริง รายละเอียดเชิงลึกดูใน workflow spec

### 6.1 Scope & label

- `--spec-ids=<id1,id2,...>`
  - ระบุ spec-id ใน scope (ต้องมีใน SPEC_INDEX)
- `--include-dependencies`
  - ขยาย scope ตาม dependency จาก registry + SPEC_INDEX
- `--ci-label=<string>`
  - label ที่จะใช้ตั้งชื่อไฟล์แผน CI เช่น `monorepo-main`

### 6.2 CI environment & system

- `--target-envs="dev,staging,prod"`
- `--ci-system=github_actions|gitlab_ci|azure_pipelines|circleci|generic`
- `--ci-config-paths=".github/workflows/*.yml;ci/*.yaml"`
- `--test-report-paths="reports/tests/*.xml;coverage/*.json"`

### 6.3 Multi-repo & registry

- `--workspace-roots`
- `--repos-config`
- `--registry-dir`
- `--registry-roots`
- `--index`, `--specindex`

### 6.4 Safety / kilocode / output

- `--safety-mode=normal|strict` (หรือ `--strict`)
- `--kilocode`, `--nosubtasks`
- `--ci-output-format=md|json|yaml`
- `--ci-output-dir=.spec/ci`
- `--stdout-summary`

---

## 7. วิธีตัดสิน Required vs Proposed Checks

### 7.1 แหล่งที่มาของ Required checks

สิ่งที่จะถูกจัดเป็น `Required` จะต้องมาจากอย่างน้อยหนึ่งในนี้:

- ระบุใน `spec.md` หรือ `tasks.md` อย่างชัดเจน
- ระบุใน registry (เช่นต้องมี contract test สำหรับ shared API X)
- baseline CI dimensions ตาม spec type
- policy กลางที่ทีมกำหนดไว้ (ถ้า encode ลง SPEC_INDEX/config)

### 7.2 Strict mode vs Normal mode

- `normal`:
  - ขาด test type หรือ baseline → ขึ้นเป็นข้อเสนอ (Proposed) ก่อน
- `strict`:
  - ขาด test type ที่ spec/registry/baseline ระบุ → ต้องเป็น Required gate
  - coverage ต่ำกว่ามาตรฐาน → Required improvement
  - ไม่มี contract test สำหรับ shared asset ที่ถูกแก้ → CI gating risk

---

## 8. KiloCode Usage Examples

### 8.1 Governance mode บน Kilo

```bash
smartspec_ci_quality_gate \
  --spec-ids=billing_core \
  --ci-label=billing-ci \
  --target-envs=dev,prod \
  --kilocode \
  --safety-mode=strict \
  --stdout-summary
```

ภายใต้ Kilo:

- Orchestrator จะแยก dimension เช่น lint / unit / integration / contract
  แล้วให้ Code mode อ่าน artifacts แบบ read-only
- กลับมา Orchestrator เพื่อรวมเป็น CI plan เดียว
- ไม่มี write operation เกิดขึ้น

### 8.2 ปิด subtasks

```bash
smartspec_ci_quality_gate \
  --spec-ids=small_feature \
  --ci-label=small-ci \
  --target-envs=staging \
  --kilocode \
  --nosubtasks
```

- ยังใช้ kilocode semantics อยู่ แต่ลดการแตก subtasks ลง เหมาะกับ
  scope เล็ก ๆ

---

## 9. Multi-repo / Multi-registry Usage Examples

### 9.1 Monorepo + platform registry

```bash
smartspec_ci_quality_gate \
  --spec-ids=search_api \
  --ci-label=search-ci \
  --target-envs=dev,prod \
  --repos-config=.spec/repos.yaml \
  --registry-dir=.spec/registry \
  --registry-roots="../platform/.spec/registry" \
  --ci-system=github_actions
```

- ใช้ repos-config เพื่อ map spec → service/job
- ใช้ platform registry เพื่อตรวจ shared API/model

### 9.2 หลายทีมหลาย repo

```bash
smartspec_ci_quality_gate \
  --spec-ids=teamA_payments,teamB_notifications \
  --ci-label=multi-team-ci \
  --target-envs=prod \
  --workspace-roots="../teamA;../teamB" \
  --registry-dir=../platform/.spec/registry \
  --safety-mode=strict
```

- CI plan จะระบุว่า shared asset ใดอยู่ภายใต้เจ้าของ (CI owner) repo ไหน
- และ pipeline ของทีมอื่นควรมี checks แค่ระดับ smoke/regression ที่จำเป็น

---

## 10. UI JSON vs Inline UI ในมุม CI

### 10.1 โปรเจกต์ JSON-first UI

```bash
smartspec_ci_quality_gate \
  --spec-ids=web_checkout \
  --ci-label=web-checkout-ci \
  --target-envs=staging,prod \
  --ci-system=github_actions
```

- ถ้า SPEC_INDEX/config บอกว่าใช้ JSON-first UI
  - แผน CI จะเสนอ jobs เช่น:
    - validate `ui.json` (schema/structure)
    - visual regression / snapshot
    - alignment กับ `ui-component-registry`
- ใน strict mode การไม่มี job เหล่านี้จะถูก mark เป็น required gate

### 10.2 โปรเจกต์ opt-out จาก JSON-first UI

```bash
smartspec_ci_quality_gate \
  --spec-ids=admin_portal \
  --ci-label=admin-ci \
  --target-envs=staging \
  --ci-system=generic
```

- ถ้า SPEC_INDEX/config ระบุ opt-out ชัดเจน
  - แผน CI จะไม่บังคับ `ui.json` validation
  - แต่ยังเสนอ end-to-end UI tests ตาม flow/หน้าจอที่ระบุใน spec

---

## 11. Best Practices & Anti-patterns

### 11.1 Best Practices

- ระบุ `--spec-ids` ชัดเจนทุกครั้ง
- ใช้ `--ci-label` ให้ตรงกับชื่อ pipeline จริงในระบบ CI
- ใน multi-repo ให้ใช้ `--repos-config` ถ้าเป็นไปได้
- ใช้ `--safety-mode=strict` กับ pipeline โปรดักชัน
- เก็บไฟล์ CI plan เป็นส่วนหนึ่งของ repo หรือ CI artifacts
- review CI plan คู่กับรายงาน `/smartspec_release_readiness` เสมอ

### 11.2 Anti-patterns

- ปล่อยให้ workflow เดา scope หรือ mapping job ↔ spec จากชื่ออย่างเดียว
- ใช้ `READY_WITH_RISKS` หรือ CI matrix ที่มีช่องว่าง โดยไม่ได้อ่าน details
- คาดหวังว่า workflow จะไปแก้ CI YAML ให้เอง
- สร้าง contract suite ซ้ำหลายที่โดยไม่มี CI owner ชัดเจน

---

## 12. FAQ / Troubleshooting

### Q1: ทำไม CI plan บอกว่าขาด contract tests ทั้งที่เรามี integration tests อยู่แล้ว?

เพราะ:

- integration tests ทดสอบ end-to-end behavior
- contract tests เน้นตรวจ interface/สัญญากับ client/service อื่น

ถ้า registry ระบุว่า API/โมเดลนี้เป็น shared asset
workflow จะคาดหวังให้มี contract tests เฉพาะสำหรับ asset นั้น

### Q2: ถ้าผมไม่อยาก strict ขนาดนั้น ควรใช้ mode ไหน?

- ใช้ `--safety-mode=normal`
- gaps หลายอย่างจะถูกลงหมวด `Proposed checks` แทนที่จะเป็น required
ให้ทีมใช้ judgment เองว่าจะ implement เมื่อไร

### Q3: ทำไมมี `unmapped_ci_jobs` ในรายงาน?

เพราะ:

- workflow ไม่สามารถ map job เหล่านั้นไปยัง spec-id ใดได้อย่างชัดเจน
- คุณอาจต้อง:
  - เพิ่ม mapping ลง SPEC_INDEX / repos-config
  - หรือยอมรับว่าเป็น legacy job/utility job ที่อยู่นอก SmartSpec scope

### Q4: ต้องแก้ CI YAML ตาม plan ทุกอย่างเลยไหม?

ไม่จำเป็น:

- `Required checks` คือส่วนที่ควร align ให้ครบตาม spec/policy
- `Proposed checks` คือข้อเสนอ สามารถทำทีหลังเป็น technical debt ได้

### Q5: ควรเรียกใช้ `/smartspec_ci_quality_gate` บ่อยแค่ไหน?

แนะนำ:

- ทุกครั้งที่เพิ่ม spec/service ใหม่
- ทุกครั้งที่ปรับ policy ด้านคุณภาพองค์กร
- เป็นระยะ ๆ (เช่น ทุก quarter) เพื่อตรวจว่า CI ยัง align กับ spec จริง

---

จบคู่มือภาษาไทยสำหรับ `/smartspec_ci_quality_gate v5.6.2` ถ้ามีการเพิ่มความสามารถใหม่ ๆ (เช่น รองรับ artifact ประเภทใหม่ หรือเปลี่ยนเกณฑ์ baseline/strict) ควรออก manual v5.7 แยก โดยระบุช่วงเวอร์ชัน workflow ที่รองรับให้ชัดเจน

