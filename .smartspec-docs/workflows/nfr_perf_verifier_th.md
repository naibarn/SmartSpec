---
manual_name: /smartspec_nfr_perf_verifier Manual (TH)
manual_version: 5.6
compatible_workflow: /smartspec_nfr_perf_verifier
compatible_workflow_versions: 5.6.2 – 5.6.x
role: user/operator manual (SRE, platform, tech leads, performance owners)
---

# /smartspec_nfr_perf_verifier คู่มือการใช้งาน (v5.6, ภาษาไทย)

## 1. ภาพรวม (Overview)

คู่มือนี้อธิบายวิธีใช้งาน workflow:

> `/smartspec_nfr_perf_verifier v5.6.2`

เพื่อใช้ตรวจสอบว่า **Non-Functional Requirements (NFR)** และ
**performance / reliability targets** ที่เขียนไว้ใน spec / policy

- มีหลักฐานรองรับจริงหรือไม่
- หลักฐานนั้นบอกว่า **ผ่าน (MET)**, **ไม่ผ่าน (NOT_MET)**
  หรือ **ยังไม่รู้ (UNKNOWN)**

ลักษณะสำคัญของ workflow นี้:

- บทบาท: **verification / governance** (ไม่ใช่ test runner)
- `write_guard: NO-WRITE`
  - ไม่รัน perf/load test เพิ่มเติม
  - ไม่แก้ spec / tasks / CI / code
  - อ่าน artifacts ต่าง ๆ แบบ read-only แล้วสร้าง **NFR verification report**
- **Verifier-only:**
  - ไม่ออกแบบ/perf plan
  - ไม่ generate tasks จาก NFR
  - งานวางแผนให้ `/smartspec_nfr_perf_planner` รับผิดชอบต่างหาก

ใช้ workflow นี้เป็น “เลเยอร์ evidence” ก่อนถึง
`/smartspec_release_readiness` และใช้ monitor health NFR ของระบบในระยะยาว

---

## 2. What’s New in v5.6

เวอร์ชัน 5.6.2 ของ verifier นี้มีจุดเด่นสำคัญ:

### 2.1 Verifier-only แยกจาก planner ชัดเจน

- ยืนยันชัด ๆ ว่า **ไม่** ทำหน้าที่วางแผนหรือ generate perf tasks
- อ้างอิง `/smartspec_nfr_perf_planner` เป็น workflow ฝั่ง planner โดยตรง
- ลดการซ้อน scope และความสับสนของทีม

### 2.2 รูปแบบ report ที่ชัดเจนมากขึ้น

- มีโครงสร้างเบื้องต้นของ report ที่แนะนำ:
  - `NFR inventory` (ชนิด, scope, criticality, target, source)
  - `NFR evaluations` (MET / NOT_MET / UNKNOWN + `blocking_for_release`)
  - `nfr_design_gaps` (จุดที่ยังไม่มี NFR) + `proposed_nfrs` (ข้อเสนอ)
  - `regression_status` ต่อ NFR (IMPROVED / UNCHANGED / REGRESSED / UNKNOWN)
  - summary ตาม spec-id / env / criticality

### 2.3 Strict mode ที่ส่งสัญญาณ “blocking” ให้ release readiness ได้ตรง ๆ

- `--safety-mode=strict` (หรือ `--strict`) ทำให้:
  - critical NFR ที่ **ไม่มี evidence เลย** →
    - สถานะ: `UNKNOWN (CRITICAL GAP)`
    - `blocking_for_release=true`
  - critical NFR ที่ `NOT_MET` → `blocking_for_release=true`
- นี่ทำให้ `/smartspec_release_readiness` อ่าน field เดียวแล้วรู้ว่า
  NFR ตัวไหนควรถูกมองเป็น blocking risk ในการปล่อย

### 2.4 รองรับ multi-service / end-to-end NFR

- เพิ่ม field:
  - `scope: local | end_to_end`
  - `involved_services` + per-service sub-status
- ทำให้เห็นภาพว่า NFR ตัวเดียวอาจครอบหลาย service และสถานะของแต่ละตัวเป็นอย่างไร

### 2.5 Regression vs baseline window

- ใช้ `--baseline-window` เพื่อคำนวณ `regression_status` ต่อ NFR
  - `IMPROVED`, `UNCHANGED`, `REGRESSED`, หรือ `UNKNOWN`
- ไม่ทำให้ MET → NOT_MET อัตโนมัติจาก regression เพียงอย่างเดียว
  แต่รายงานเป็น risk แยกต่างหาก

---

## 3. Backward Compatibility Notes

- Manual v5.6 นี้ใช้กับ `/smartspec_nfr_perf_verifier` ตั้งแต่
  **เวอร์ชัน 5.6.2 เป็นต้นไป** (5.6.x)
- ไม่มีการลบ flag หรือ behavior เดิม (workflow ใหม่ในตระกูล NFR)
- การใช้ `--strict` ยังคงเป็น alias ของ `--safety-mode=strict`
- semantics ด้าน multi-repo / `--kilocode` / canonical folders
  สอดคล้องกับ workflow governance ตัวอื่น เช่น
  `/smartspec_release_readiness`, `/smartspec_ci_quality_gate`

หากมี patch ใหม่ในตระกูล 5.6.x ที่ไม่เปลี่ยน semantics หลัก
manual ฉบับนี้ยังถือว่าใช้ได้

---

## 4. แนวคิดหลัก (Core Concepts)

### 4.1 NFR inventory

- NFR มาจาก:
  - `spec.md`
  - `tasks.md` (ถ้ามี section NFR)
  - SPEC_INDEX
  - NFR policy files
  - registry ที่เกี่ยวข้อง เช่น slo-registry
- แต่ละ NFR ควรมีข้อมูลอย่างน้อย:
  - ชื่อ / id
  - category (latency, throughput, availability, error_budget, resource, UX)
  - scope: `local` vs `end_to_end`
  - target/threshold
  - criticality (critical/high/medium/low)
  - แหล่งอ้างอิง

### 4.2 สถานะ: MET / NOT_MET / UNKNOWN

- `MET`
  - มี evidence ที่ชัดว่า metric ที่วัดสอดคล้องหรือดีกว่า target
- `NOT_MET`
  - มี evidence ชัดว่า metric ไม่ถึง target
- `UNKNOWN`
  - ไม่มี evidence หรือมีแต่ไม่พอจะสรุป
- `UNKNOWN (CRITICAL GAP)`
  - กรณีเป็น critical NFR + ไม่มี evidence เลย โดยเฉพาะใน strict mode

### 4.3 blocking_for_release

- field ที่บอกว่า NFR นั้นควรถูกมองเป็น **blocking risk** หรือไม่
- คำนึงถึง:
  - criticality
  - status (MET / NOT_MET / UNKNOWN)
  - safety-mode (`normal` vs `strict`)

---

## 5. Quick Start (ตัวอย่างคำสั่ง)

### 5.1 ตรวจ NFR สำหรับ service เดียวใน staging

```bash
smartspec_nfr_perf_verifier \
  --spec-ids=checkout_api \
  --target-env=staging \
  --run-label=checkout-staging-nfr \
  --nfr-policy-paths=".spec/policies/nfr/*.md" \
  --perf-report-paths="reports/perf/checkout/*.json" \
  --metrics-export-paths="metrics/checkout/*.json" \
  --report-format=md \
  --stdout-summary
```

ผลลัพธ์:

- รายงานที่: `.spec/reports/smartspec_nfr_perf_verifier/<timestamp>_checkout-staging-nfr.md`
- สรุป NFR ของ `checkout_api` บน environment `staging`

### 5.2 ใช้ strict mode ก่อนปล่อย production

```bash
smartspec_nfr_perf_verifier \
  --spec-ids=payments_gateway \
  --target-env=prod \
  --run-label=payments-prod-nfr \
  --perf-report-paths="reports/perf/payments/*.json" \
  --metrics-export-paths="metrics/payments/*.json" \
  --safety-mode=strict \
  --report-format=json \
  --stdout-summary
```

ใน strict mode:

- critical NFR ที่ไม่มี evidence → `UNKNOWN (CRITICAL GAP)` + blocking
- critical NFR ที่ NOT_MET → blocking

### 5.3 เปรียบเทียบ regression จาก baseline

```bash
smartspec_nfr_perf_verifier \
  --spec-ids=search_api \
  --target-env=prod \
  --run-label=search-prod-nfr \
  --perf-report-paths="reports/perf/search/*.json" \
  --metrics-export-paths="metrics/search/*.json" \
  --time-window=7d \
  --baseline-window=30d \
  --report-format=md
```

รายงานจะระบุ `regression_status` ต่อ NFR เปรียบเทียบระหว่าง
ช่วง 7 วันล่าสุดกับ baseline 30 วัน

---

## 6. CLI / Flags Cheat Sheet

### 6.1 Scope & labeling

- `--spec-ids=<id1,id2,...>`
- `--include-dependencies`
- `--run-label=<string>`

### 6.2 Environment & time

- `--target-env=dev|staging|prod|...`
- `--time-window=24h|7d|30d|...`
- `--baseline-window=7d|30d|...`

### 6.3 Evidence paths

- `--nfr-policy-paths="..."`
- `--perf-report-paths="..."`
- `--metrics-export-paths="..."`

### 6.4 Multi-repo / registry / index

- `--workspace-roots`
- `--repos-config`
- `--registry-dir`
- `--registry-roots`
- `--index`, `--specindex`

### 6.5 Safety / kilocode / output

- `--safety-mode=normal|strict` (หรือ `--strict`)
- `--kilocode`, `--nosubtasks`
- `--report-format=md|json`
- `--report-dir=.spec/reports/smartspec_nfr_perf_verifier/`
- `--stdout-summary`

---

## 7. วิธีตีความ MET / NOT_MET / UNKNOWN

### 7.1 MET

- มีตัวเลขชัดเจน เช่น:
  - P95 latency <= target
  - error rate ต่ำกว่า threshold
  - availability สูงกว่าที่กำหนด

### 7.2 NOT_MET

- metric แย่กว่าที่กำหนดอย่างชัดเจน
- ต้องมีคนพิจารณาว่าจะ delay release หรือไม่ (แต่จากมุม governance
  จะถือเป็นความเสี่ยงชัดเจน)

### 7.3 UNKNOWN

- ไม่มี test หรือ metrics ที่ผูกกับ NFR นั้นเลย
- หรือมีข้อมูลแต่ไม่เพียงพอ (data incomplete, noisy, ช่วงเวลาสั้นเกินไป)

### 7.4 UNKNOWN (CRITICAL GAP)

- กรณี NFR เป็น critical ตาม metadata/policy
- ไม่มี evidence เลย โดยเฉพาะใน strict mode
- ควรถือว่า **ไม่พร้อมปล่อย** จนกว่าจะมี evidence ใหม่

---

## 8. KiloCode Usage Examples

### 8.1 ใช้บน Kilo เพื่อตรวจ NFR ของ core service

```bash
smartspec_nfr_perf_verifier \
  --spec-ids=core_billing \
  --target-env=prod \
  --run-label=core-billing-nfr \
  --perf-report-paths="reports/perf/core_billing/*.json" \
  --metrics-export-paths="metrics/core_billing/*.json" \
  --safety-mode=strict \
  --kilocode \
  --stdout-summary
```

บน Kilo:

- Orchestrator จะ loop ตาม NFR category (latency, availability, ฯลฯ)
- Code mode แยก parse report ตาม category แบบ read-only
- กลับมาสรุปเป็น status ต่อ NFR พร้อม `blocking_for_release`

### 8.2 ปิด subtasks

```bash
smartspec_nfr_perf_verifier \
  --spec-ids=small_feature \
  --target-env=staging \
  --run-label=small-feature-nfr \
  --kilocode \
  --nosubtasks
```

- ยังใช้ kilocode semantics อยู่ แต่ใช้ reasoning flow เดียว
  เหมาะกับ scope เล็ก ๆ

---

## 9. Multi-repo / Multi-registry Usage Examples

### 9.1 Monorepo หลาย service

```bash
smartspec_nfr_perf_verifier \
  --spec-ids=search_api,ranking_service \
  --target-env=prod \
  --run-label=search-stack-nfr \
  --repos-config=.spec/repos.yaml \
  --registry-dir=.spec/registry \
  --perf-report-paths="reports/perf/**/*.json" \
  --metrics-export-paths="metrics/**/*.json" \
  --safety-mode=strict
```

- ใช้ repos-config + registry ในการ map NFR end-to-end
- แสดงบริการที่เกี่ยวข้องกับ NFR เดียวกัน พร้อม per-service status

### 9.2 หลาย repo / หลายทีม

```bash
smartspec_nfr_perf_verifier \
  --spec-ids=teamA_checkout,teamB_payments \
  --target-env=staging \
  --run-label=checkout-payments-nfr \
  --workspace-roots="../teamA;../teamB" \
  --registry-dir=../platform/.spec/registry \
  --perf-report-paths="../teamA/reports/perf/**/*.json;../teamB/reports/perf/**/*.json" \
  --metrics-export-paths="../teamA/metrics/**/*.json;../teamB/metrics/**/*.json"
```

- รายงานจะแสดง NFR ที่ cross-team พร้อมระบุว่า evidence มาจาก repo ไหน

---

## 10. ตัวอย่าง NFR ฝั่ง UI/UX

### 10.1 Page load / LCP / TTI

หาก spec ระบุ NFR เช่น:

- LCP < 2.5s บน 95th percentile
- TTI < 5s

และคุณส่ง metrics export เช่น Web Vitals หรือ synthetic monitoring เข้ามา
workflow จะ:

- map metric → NFR
- สรุปว่า MET / NOT_MET / UNKNOWN

UI governance (JSON-first vs inline) ใช้แค่เป็น context ว่า UI อยู่ตรงไหน
แต่ไม่เปลี่ยนเกณฑ์ pass/fail ของ NFR

---

## 11. Best Practices & Anti-patterns

### 11.1 Best Practices

- เขียน NFR ให้ชัดใน spec/policy ก่อนใช้ verifier
- ใช้ `--safety-mode=strict` กับบริการที่ critical ต่อธุรกิจ
- รัน verifier เป็นระยะ (เช่นรายสัปดาห์) ไม่ใช่เฉพาะก่อน release
- เก็บรายงานไว้ใน version control หรือ CI artifacts
- อ่านผลคู่กับ `/smartspec_ci_quality_gate` และ `/smartspec_release_readiness`

### 11.2 Anti-patterns

- คิดว่า “ไม่มี evidence แปลว่าปลอดภัย” → จริง ๆ คือ UNKNOWN หรือ CRITICAL GAP
- ละเลย NFR ที่ `UNKNOWN (CRITICAL GAP)` แล้วปล่อย release ต่อ
- ให้ workflow เดา spec-id หรือ mapping เองจากชื่อไฟล์แปลก ๆ

---

## 12. FAQ / Troubleshooting

### Q1: ถ้าไม่มี perf test / metrics เลย จะเกิดอะไรขึ้น?

- NFR ส่วนใหญ่จะได้สถานะ `UNKNOWN`
- ถ้าเป็น critical NFR ใน strict mode → `UNKNOWN (CRITICAL GAP)` + blocking
- แนะนำให้ย้อนกลับไปใช้ `/smartspec_nfr_perf_planner` + เติม test
  และเชื่อมเข้ากับ `/smartspec_ci_quality_gate`

### Q2: ทำไม NFR บางข้อถูก mark เป็น MET แต่ regression_status เป็น REGRESSED?

- เพราะยัง “ผ่าน target” แต่แย่ลงจาก baseline อย่างมีนัยสำคัญ
- ควรถือเป็น early warning ว่าถ้าแนวโน้มนี้ต่อเนื่อง อาจกลายเป็น NOT_MET ในอนาคต

### Q3: ถ้าผลออกมา NOT_MET แต่เราจำเป็นต้องปล่อย release?

- workflow แค่รายงานความเสี่ยงและข้อเท็จจริง
- การยก exception หรือ accept risk เป็น process ระดับองค์กร
  ที่ควรถูกบันทึกไว้นอก workflow นี้

---

จบคู่มือภาษาไทยสำหรับ `/smartspec_nfr_perf_verifier v5.6.2`.
หากมีการเพิ่มความสามารถสำคัญ (เช่น support metrics format ใหม่ หรือเปลี่ยน semantics ของ strict mode) ควรออก manual v5.7 แยก และระบุช่วงเวอร์ชัน workflow ที่รองรับให้ชัดเจน

