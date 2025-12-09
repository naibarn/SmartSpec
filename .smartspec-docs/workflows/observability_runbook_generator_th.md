---
manual_name: /smartspec_observability_runbook_generator Manual (TH)
manual_version: 5.6
compatible_workflow: /smartspec_observability_runbook_generator
compatible_workflow_versions: 5.6.2 – 5.6.x
role: user/operator manual (SRE, platform, dev, on-call)
---

# /smartspec_observability_runbook_generator คู่มือการใช้งาน (v5.6, ภาษาไทย)

## 1. ภาพรวม (Overview)

คู่มือนี้อธิบายวิธีใช้งาน workflow:

> `/smartspec_observability_runbook_generator v5.6.2`

หน้าที่ของ workflow นี้คือช่วย

> "สร้าง **observability runbook** ที่สอดคล้องกับ spec / SLO / alert / dashboard
> เพื่อให้ on-call และ dev ใช้รับมือ incident ได้อย่างเป็นระบบ"

คุณสมบัติหลัก:

- บทบาท: **design / planning / runbook-generation**
- `write_guard: NO-WRITE`
  - ไม่แก้ `spec.md`, `tasks.md`, config, CI หรือ observability backend
  - สร้างเฉพาะ **ข้อเสนอ runbook** เป็นไฟล์ใน `.spec/suggestions/...`
- ทำงานบนข้อมูลต่อไปนี้ (แบบอ่านอย่างเดียว):
  - SPEC_INDEX, spec, SLO/NFR, service registries
  - alert rules, dashboards, log/trace config, runtime metrics config
- ออกแบบให้ทำงานร่วมกับ workflow อื่น เช่น
  - `/smartspec_release_readiness` (ดู readiness ทั้งระบบ)
  - `/smartspec_ci_quality_gate` (เพิ่ม/ปรับ quality & checks)

พูดสั้น ๆ:

- **generator นี้** ไม่ใช่เครื่องมือ runbook automation
- มันช่วยแปลงความรู้จาก spec + observability config → runbook ที่อ่านง่าย

---

## 2. What’s New in v5.6

จุดสำคัญของเวอร์ชัน 5.6.2:

### 2.1 Orchestrator-per-task (รองรับ Kilo เต็มรูปแบบ)

- เมื่อใช้ `--kilocode` และอยู่บน Kilo:
  - ก่อนสร้าง runbook ของแต่ละ spec-id จะใช้ Orchestrator แตก subtasks
  - default คือ **เปิด subtasks** (เว้นแต่ใช้ `--nosubtasks`)

### 2.2 Safety-mode สำหรับ runbook

- `--safety-mode=normal` (ดีฟอลต์):
  - อนุญาต suggestion แบบ exploratory ที่ไม่เสี่ยงสูง
  - แยกส่วน "standard" กับ "optional" ให้เห็นชัด
- `--safety-mode=strict` หรือ `--strict`:
  - ทุก SLO หรือ critical section ที่เป็น `critical/high` ต้อง
    - มี runbook coverage ขั้นต่ำ หรือ
    - ถูก mark เป็น `observability_gap`
  - ห้ามเสนอ step ที่เสี่ยง เช่น direct DB writes เป็น default path

### 2.3 กติกาเรื่องข้อมูลอ่อนไหว (secrets/PII)

- runbook ห้ามแสดง:
  - secret, token, password, private key
  - PII ที่อ่อนไหว (เช่น เลขบัตรเต็ม ๆ, national ID)
- สามารถพูดถึงได้แค่:
  - "พบข้อมูลอ่อนไหวใน log X" โดยไม่ copy ค่าออกมา

### 2.4 Multi-repo / multi-registry awareness

- ใช้ `--repos-config`, `--workspace-roots`, `--registry-dir`, `--registry-roots`
  เพื่อตีความ service topology และ ownership
- cross-service scenario จะบอกชัดว่าเกี่ยวกับ service ใดบ้าง และทีมไหนรับผิดชอบ

---

## 3. Backward Compatibility Notes

- Manual v5.6 นี้รองรับ `/smartspec_observability_runbook_generator`
  ตั้งแต่ **v5.6.2 เป็นต้นไป** (5.6.x)
- ไม่มีการลบหรือเปลี่ยนความหมายของ flag เดิม
- `--strict` ยังคงเป็น alias ของ `--safety-mode=strict`
- path และ canonical folders สอดคล้องกับ workflow ตระกูล SmartSpec อื่น

---

## 4. แนวคิดหลัก (Core Concepts)

### 4.1 Observability runbook คืออะไร

- เอกสาร/ไฟล์ที่อธิบาย:
  - อาการ (symptoms) / alert / SLO breach แบบต่าง ๆ
  - ควรเปิด dashboard/metric อะไรดู
  - ควรยิง log query / trace query อะไร
  - ขั้นตอนวิเคราะห์ (diagnosis steps)
  - ขั้นตอนบรรเทา/rollback (mitigation steps)
  - check-list หลัง incident

ใน workflow นี้ runbook เป็น **ข้อเสนอ** ที่ทีมสามารถ review + แก้เองก่อน
จะนำไปใช้เป็น runbook official

### 4.2 การ map SLO/NFR → runbook

ขั้นตอนความคิดหลัก:

1. อ่าน SLO/NFR จาก spec / SLO registry / policy
2. หา critical path / critical section ที่เกี่ยวข้อง
3. map ไปยัง observability config ที่มีอยู่ (alerts, dashboards, logs, traces)
4. ตีกรอบ incident scenario
5. เขียน runbook เป็นขั้น ๆ

### 4.3 Observability gap

- ถ้า SLO/NFR หรือ critical path ยังไม่มี alerts/dashboards/logs/traces
  ที่เหมาะสม
- generator จะใส่ section `observability_gap` เป็นข้อเสนอ
  ไม่ใช่ step ปัจจุบัน

---

## 5. Quick Start (ตัวอย่างคำสั่ง)

### 5.1 สร้าง runbook ให้ service เดียว

```bash
smartspec_observability_runbook_generator \
  --spec-ids=checkout_api \
  --runbook-label=checkout-observability \
  --alert-config-paths=".config/alerts/checkout/*.yml" \
  --dashboard-config-paths=".config/dashboards/checkout/*.json" \
  --log-config-paths=".config/logging/checkout/*.yml" \
  --trace-config-paths=".config/tracing/checkout/*.yml" \
  --runbook-format=md \
  --stdout-summary
```

ผลลัพธ์:

- runbook ที่
  `.spec/suggestions/smartspec_observability_runbook_generator/<timestamp>_checkout-observability.md`

### 5.2 ใช้ strict mode กับ core payments

```bash
smartspec_observability_runbook_generator \
  --spec-ids=core_payments \
  --runbook-label=core-payments-observability \
  --alert-config-paths=".config/alerts/core_payments/*.yml" \
  --dashboard-config-paths=".config/dashboards/core_payments/*.json" \
  --trace-config-paths=".config/tracing/core_payments/*.yml" \
  --safety-mode=strict \
  --runbook-format=json \
  --stdout-summary
```

ใน strict mode:

- ทุก critical/high SLO ต้องมี scenario หรือถูก mark ว่าเป็น `observability_gap`
- step ที่เสี่ยง (เช่น แก้ DB ตรง) จะไม่ถูกเสนอเป็น default

### 5.3 รวมหลาย service + dependencies

```bash
smartspec_observability_runbook_generator \
  --spec-ids=search_api,ranking_service \
  --include-dependencies \
  --runbook-label=search-stack-observability \
  --repos-config=.spec/repos.yaml \
  --registry-dir=.spec/registry \
  --alert-config-paths=".config/alerts/**/*.yml" \
  --dashboard-config-paths=".config/dashboards/**/*.json" \
  --runbook-format=md
```

- runbook จะครอบคลุมทั้ง search_api, ranking_service และ dependencies ที่สำคัญ

---

## 6. CLI / Flags Cheat Sheet

### 6.1 Scope & labeling

- `--spec-ids=<id1,id2,...>`
- `--include-dependencies`
- `--runbook-label=<string>`

### 6.2 Environment

- `--target-envs=dev,staging,prod,...`

### 6.3 Observability config paths

- `--alert-config-paths="..."`
- `--dashboard-config-paths="..."`
- `--log-config-paths="..."`
- `--trace-config-paths="..."`
- `--runtime-metrics-paths="..."`

### 6.4 Multi-repo / registry / index / safety

- `--workspace-roots`
- `--repos-config`
- `--registry-dir`
- `--registry-roots`
- `--index`, `--specindex`
- `--safety-mode=normal|strict` (หรือ `--strict`)

### 6.5 Output & KiloCode

- `--runbook-format=md|json`
- `--runbook-dir=.spec/suggestions/smartspec_observability_runbook_generator/`
- `--stdout-summary`
- `--kilocode`, `--nosubtasks`

---

## 7. วิธีอ่าน runbook ที่ generator สร้างให้

ในไฟล์ runbook มักมีโครงแบบนี้:

- Metadata
  - service/spec-id
  - owner/team
  - environments ที่เกี่ยวข้อง
- Scenario list
  - ตัวอย่าง: `slo_latency_breach`, `5xx_spike`, `cpu_saturation`, `db_latency`, `dependency_down`
- แต่ละ scenario จะมี:
  - อาการ (symptoms) / alert ที่เกี่ยวข้อง
  - metrics/dashboards ที่ควรดู
  - log/trace query ที่แนะนำ (ไม่โชว์ค่า PII/secret)
  - ขั้นตอน diagnosis ทีละข้อ
  - mitigation / rollback steps (ผ่านช่องทางที่ปลอดภัย เช่น deploy rollback, ปรับ traffic ผ่าน feature flag)
  - verification + checklist หลังแก้
- `observability_gap` section
  - บอก SLO/critical path ที่ยังไม่มี coverage ดีพอ

---

## 8. KiloCode Usage Examples

### 8.1 สร้าง runbook ขนาดใหญ่บน Kilo

```bash
smartspec_observability_runbook_generator \
  --spec-ids=checkout_api,inventory_api \
  --runbook-label=checkout-inventory-observability \
  --alert-config-paths=".config/alerts/**/*.yml" \
  --dashboard-config-paths=".config/dashboards/**/*.json" \
  --kilocode \
  --stdout-summary
```

บน Kilo:

- Orchestrator จะประมวลผลทีละ spec-id (top-level task)
- แต่ละ task แตก subtasks เช่น: รวบรวม SLO, match กับ alert, สร้าง scenario
- Code mode อ่าน config ทั้งหมดแบบ read-only
- Orchestrator รวมเป็น runbook เดียวสำหรับ label นี้

### 8.2 ปิด subtasks ในกรณี scope เล็ก

```bash
smartspec_observability_runbook_generator \
  --spec-ids=small_service \
  --runbook-label=small-service-observability \
  --alert-config-paths=".config/alerts/small_service/*.yml" \
  --kilocode \
  --nosubtasks
```

- ใช้ reasoning flow เดียวต่อ service
- เหมาะกับ service ขนาดเล็ก หรือทดลองใช้ครั้งแรก

---

## 9. Multi-repo / Multi-registry Examples

### 9.1 Monorepo หลาย service

```bash
smartspec_observability_runbook_generator \
  --spec-ids=search_api,ranking_service \
  --runbook-label=search-stack-observability \
  --repos-config=.spec/repos.yaml \
  --registry-dir=.spec/registry \
  --alert-config-paths=".config/alerts/**/*.yml" \
  --dashboard-config-paths=".config/dashboards/**/*.json" \
  --runtime-metrics-paths=".config/metrics/**/*.yml"
```

- ใช้ registry + repos-config เพื่อเข้าใจความสัมพันธ์ search ↔ ranking ↔ dependencies
- runbook จะชี้ว่าเวลามีปัญหา search error rate สูง
  - ต้องดู metrics จาก service ไหนบ้าง
  - call chain / dependency ใดเกี่ยวข้อง

### 9.2 cross-team / multi-repo

```bash
smartspec_observability_runbook_generator \
  --spec-ids=teamA_checkout,teamB_payments \
  --runbook-label=checkout-payments-observability \
  --workspace-roots="../teamA;../teamB" \
  --registry-dir=../platform/.spec/registry \
  --alert-config-paths="../teamA/.config/alerts/**/*.yml;../teamB/.config/alerts/**/*.yml" \
  --dashboard-config-paths="../teamA/.config/dashboards/**/*.json;../teamB/.config/dashboards/**/*.json"
```

- runbook จะบอกว่า incident ใดบ้างต้องประสานสองทีม
- ชัดเจนว่า metric / dashboard / log ของ team ไหนเกี่ยวข้อง

---

## 10. UI Observability Examples

สำหรับ UI-focused services:

- requirement เช่น:
  - page load time / Web Vitals (LCP, FID, CLS)
  - frontend error rate
  - latency ของ API ที่สำคัญต่อ UX

runbook อาจรวม:

- วิธีดู dashboard ของ Web Vitals / frontend errors
- mapping ระหว่างหน้าจอ/flow กับ backend API
- log/trace query สำหรับ route หรือ component สำคัญ

UI governance:

- ถ้า project ใช้ JSON-first UI (`ui.json`):
  - runbook สามารถอ้างอิงหน้าจอ/flow ตามโครงใน `ui.json`
- ถ้า opt-out / inline UI:
  - ไม่สมมติว่ามี `ui.json`
  - ยังสร้าง runbook แบบ E2E/flow-based จาก spec + observability config ได้

---

## 11. Best Practices & Anti-patterns

### 11.1 Best Practices

- ตั้ง SLO/NFR ให้ชัดก่อน แล้วค่อยใช้ generator สร้าง runbook
- รัน generator ใหม่เมื่อ:
  - มีการเปลี่ยนแปลง observability ครั้งใหญ่ (ย้าย dashboard, เปลี่ยน alert rules)
  - ก่อน release สำคัญ
- review runbook ร่วมกันกับ on-call/SRE ก่อนใช้งานจริง
- เก็บ runbook suggestions ใน version control
- ใช้ `--safety-mode=strict` กับบริการที่ critical

### 11.2 Anti-patterns

- หวังให้ generator สร้าง SLO/alert จาก 0 โดยไม่มีข้อมูลใน spec/policy
- copy ค่า secret/PII จาก log มาใส่ใน runbook
- ใช้ runbook เป็นสิ่งเดียวในการตัดสินใจ incident โดยไม่เคารพ process change/approval

---

## 12. FAQ / Troubleshooting

### Q1: ถ้ายังไม่มี alert / dashboard เลย จะได้ runbook ไหม?

- จะได้ runbook แต่จะมี `observability_gap` เยอะ
- เหมาะใช้เป็น input เพื่อเพิ่ม alerts/dashboards ก่อนจริงจัง

### Q2: ใช้กับ dev environment ได้ไหม?

- ได้ แต่ประโยชน์สูงสุดมักอยู่ที่ staging/prod
- ใน dev อาจใช้เพื่อทดลองโครง runbook/ปรับ naming metric/log ให้ดี

### Q3: ต้องใช้คู่กับ `/smartspec_release_readiness` เสมอไหม?

- ไม่บังคับ แต่แนะนำ
  - readiness บอกว่า feature/service พร้อมแค่ไหน
  - runbook บอกว่า ถ้ามีปัญหา จะ handle ยังไง

---

จบคู่มือภาษาไทยสำหรับ `/smartspec_observability_runbook_generator v5.6.2`.
หากอนาคตมีการเปลี่ยน semantics สำคัญหรือเพิ่มโหมดหลัก
ควรออก manual v5.7 แยก พร้อมระบุช่วงเวอร์ชัน workflow ที่รองรับให้ชัดเจน

