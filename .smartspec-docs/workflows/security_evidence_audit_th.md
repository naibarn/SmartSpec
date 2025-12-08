---
manual_name: /smartspec_security_evidence_audit Manual (TH)
manual_version: 5.6
compatible_workflow: /smartspec_security_evidence_audit
compatible_workflow_versions: 5.6.2 – 5.6.x
role: user/operator manual (security, platform, SRE, tech leads)
---

# /smartspec_security_evidence_audit คู่มือการใช้งาน (v5.6, ภาษาไทย)

## 1. ภาพรวม (Overview)

คู่มือนี้อธิบายวิธีใช้งาน workflow:

> `/smartspec_security_evidence_audit v5.6.2`

หน้าที่ของ workflow นี้คือช่วยตอบคำถามว่า

> "Security requirements ที่เราสัญญาไว้ มี **หลักฐานจริงและสดใหม่** รองรับแค่ไหน
> มีช่องโหว่หรือช่องว่างตรงไหนบ้าง และอะไรควรถูกมองเป็นความเสี่ยงก่อน release?"

ลักษณะสำคัญ:

- บทบาท: **verification / governance** (ไม่ใช่ scanner)
- `write_guard: NO-WRITE`
  - ไม่รัน SAST/DAST เอง
  - ไม่แก้ spec / tasks / CI / code / config
  - อ่านหลักฐานแบบ read-only แล้วสร้าง **security evidence report**
- **Verifier-only:**
  - ไม่ generate test / pipeline / config ใหม่
  - งาน remediation, เพิ่ม test, ปรับ CI ให้ `smartspec_ci_quality_gate` และ workflow อื่นทำต่อ
- **ไม่ดึง secrets เข้ามาในรายงาน:**
  - รายงาน **ห้าม** copy ค่า secret/password/token/key จาก log/report ตรง ๆ
  - อนุญาตแค่บันทึกว่า "พบ secret ในไฟล์ X" แบบไม่โชว์ค่า

ใช้ workflow นี้เป็นเลเยอร์ evidence security ก่อน `/smartspec_release_readiness`
และใช้ใน audit ภายใน/ภายนอก หรือ risk review ได้

---

## 2. What’s New in v5.6

### 2.1 Evidence freshness (ไม่ใช้แต่ผลสแกนเก่า ๆ)

- เพิ่มแนวคิด **evidence_freshness_status** ต่อ requirement:
  - `FRESH` – หลักฐานอยู่ในช่วงอายุที่ยอมรับได้ (เทียบกับ `--evidence-max-age`)
  - `STALE` – หลักฐานเก่ากว่าที่กำหนด
  - `UNKNOWN` – ไม่รู้ timestamp หรือไม่เกี่ยวกับเวลา
- ทำให้เห็นว่า coverage จากสแกน/เทสต์นั้น **ยังสด** หรือ **หมดอายุ** แล้ว

### 2.2 Strict mode + stale evidence semantics

- ใน `--safety-mode=strict`:
  - critical requirement + `coverage_status=NONE` → blocking
  - critical requirement + `HAS_OPEN_FINDINGS` → blocking
  - critical requirement + `evidence_freshness_status=STALE`
    → ถือว่าแทบไม่มี evidence ปัจจุบัน → เอนไปทาง blocking เว้นแต่มี mitigation

### 2.3 ป้องกันการหลุด secrets ในรายงาน

- ระบุชัดว่า:
  - report ห้ามแสดง secret / token / password / private key
  - ให้ระบุตำแหน่งและประเภทปัญหา แต่อย่า copy ค่า

### 2.4 มุมมอง coverage & finding ชัดขึ้น

- ต่อ requirement แต่ละข้อจะมีอย่างน้อย:
  - `coverage_status` = `COVERED | PARTIAL | NONE | UNKNOWN`
  - `finding_status` = `NO_KNOWN_FINDINGS | HAS_OPEN_FINDINGS | UNKNOWN`
  - `evidence_freshness_status` = `FRESH | STALE | UNKNOWN`
  - `blocking_for_release` = true/false

---

## 3. Backward Compatibility Notes

- Manual v5.6 นี้ใช้กับ `/smartspec_security_evidence_audit` ตั้งแต่
  **v5.6.2 เป็นต้นไป** (5.6.x)
- ไม่มีการลบ flag หรือ behavior เดิม (workflow นี้เป็นตัวใหม่ในสาย security)
- `--strict` ยังคงเป็น alias ของ `--safety-mode=strict`
- รูปแบบ path / canonical folders / multi-repo / `--kilocode`
  align กับ workflow ใหญ่ตัวอื่น เช่น
  - `/smartspec_release_readiness`
  - `/smartspec_ci_quality_gate`

---

## 4. แนวคิดหลัก (Core Concepts)

### 4.1 Security requirement inventory

Requirement จะถูกดึงมาจาก:

- spec (`spec.md`)
- SPEC_INDEX
- security policy / baseline
- registry ที่เกี่ยวข้อง เช่น security-registry, data-classification

ต่อ requirement ควรประกอบด้วย:

- id/name
- category (เช่น authn, authz, data_at_rest, data_in_transit,
  input_validation, secrets, dependency_vulns, infra_network,
  logging_monitoring, compliance)
- data classification/sensitivity (ถ้ามี)
- criticality (`critical` / `high` / `medium` / `low`)
- source (spec / policy / registry)

### 4.2 coverage_status

- `COVERED` – มีหลักฐานชัดเจน เช่น:
  - test suite ที่ออกแบบมาเพื่อ requirement นี้
  - รายงานสแกนล่าสุดที่สะอาดในส่วนที่เกี่ยวข้อง
- `PARTIAL` – มี evidence บางส่วน แต่ไม่ครอบคลุมทั้งหมด
- `NONE` – ไม่พบ evidence ที่ผูกกับ requirement
- `UNKNOWN` – ไม่สามารถตัดสินได้ (ข้อมูลขาดหรือ parsing ไม่แน่ใจ)

### 4.3 finding_status

- `NO_KNOWN_FINDINGS` – ไม่มี finding เปิดอยู่ใน evidence ชุดนั้น
- `HAS_OPEN_FINDINGS` – มีช่องโหว่/issue ที่ยังไม่ถูกปิด
- `UNKNOWN` – ไม่สามารถสรุปได้จาก evidence ที่มี

### 4.4 evidence_freshness_status

- `FRESH` – อายุ evidence อยู่ในช่วง `--evidence-max-age`
- `STALE` – เกินกว่าที่กำหนด
- `UNKNOWN` – timestamp ไม่ชัด / ไม่เกี่ยวกับเวลา (เช่น spec)

### 4.5 blocking_for_release

- flag ระบุว่า requirement นั้น ๆ ควรถูกมองเป็น **blocking risk** หรือไม่
- พิจารณา:
  - criticality
  - coverage_status
  - finding_status
  - evidence_freshness_status
  - safety-mode (`normal` vs `strict`)

---

## 5. Quick Start (ตัวอย่างคำสั่ง)

### 5.1 Audit security สำหรับ service เดียวใน staging

```bash
smartspec_security_evidence_audit \
  --spec-ids=checkout_api \
  --target-env=staging \
  --run-label=checkout-staging-security \
  --security-policy-paths=".spec/policies/security/*.md" \
  --sast-report-paths="reports/sast/checkout/*.json" \
  --dast-report-paths="reports/dast/checkout/*.json" \
  --dependency-report-paths="reports/deps/checkout/*.json" \
  --report-format=md \
  --stdout-summary
```

ผลลัพธ์:

- รายงานที่:
  `.spec/reports/smartspec_security_evidence_audit/<timestamp>_checkout-staging-security.md`
- สรุป requirement ความปลอดภัยของ `checkout_api` บน staging

### 5.2 Audit ก่อนปล่อย production แบบ strict

```bash
smartspec_security_evidence_audit \
  --spec-ids=payments_gateway \
  --target-env=prod \
  --run-label=payments-prod-security \
  --security-policy-paths=".spec/policies/security/*.md" \
  --sast-report-paths="reports/sast/payments/*.json" \
  --dast-report-paths="reports/dast/payments/*.json" \
  --dependency-report-paths="reports/deps/payments/*.json" \
  --evidence-max-age=30d \
  --safety-mode=strict \
  --report-format=json \
  --stdout-summary
```

ใน strict mode + evidence-max-age:

- critical + ไม่มี evidence → blocking
- critical + HAS_OPEN_FINDINGS → blocking
- critical + evidence เก่ากว่า 30 วัน → มองว่าไม่มี evidence ปัจจุบัน → มักจะ blocking

### 5.3 ใช้ log และ IaC reports ประกอบ

```bash
smartspec_security_evidence_audit \
  --spec-ids=admin_portal \
  --target-env=prod \
  --run-label=admin-portal-security \
  --iac-report-paths="reports/iac/admin/**/*.json" \
  --audit-log-paths="logs/security/admin_portal/*.json" \
  --report-format=md
```

- ใช้ IaC reports เพื่อตรวจ infra/config
- ใช้ audit logs ดูการใช้สิทธิ์ admin / access log

---

## 6. CLI / Flags Cheat Sheet

### 6.1 Scope & labeling

- `--spec-ids=<id1,id2,...>`
- `--include-dependencies`
- `--run-label=<string>`

### 6.2 Environment, time & evidence age

- `--target-env=dev|staging|prod|...`
- `--time-window=24h|7d|30d|...`
- `--evidence-max-age=30d|90d|...`

### 6.3 Security requirement & policy

- `--security-policy-paths="..."`

### 6.4 Evidence paths

- `--sast-report-paths="..."`
- `--dast-report-paths="..."`
- `--dependency-report-paths="..."`
- `--container-report-paths="..."`
- `--iac-report-paths="..."`
- `--security-test-report-paths="..."`
- `--audit-log-paths="..."`

### 6.5 Multi-repo / registry / index / safety

- `--workspace-roots`
- `--repos-config`
- `--registry-dir`
- `--registry-roots`
- `--index`, `--specindex`
- `--safety-mode=normal|strict` (หรือ `--strict`)

### 6.6 Kilo / output

- `--kilocode`, `--nosubtasks`
- `--report-format=md|json`
- `--report-dir` (ดีฟอลต์:
  `.spec/reports/smartspec_security_evidence_audit/`)
- `--stdout-summary`

---

## 7. วิธีตีความ coverage / findings / freshness

### 7.1 ตัวอย่างสถานะ "ดี" สำหรับ critical requirement

- `coverage_status = COVERED`
- `finding_status = NO_KNOWN_FINDINGS`
- `evidence_freshness_status = FRESH`
- ใน strict mode: มักจะไม่ blocking

### 7.2 ตัวอย่างที่มีช่องโหว่

- `coverage_status = NONE` → ไม่มีหลักฐานเลย
- `coverage_status = PARTIAL` + finding เปิดอยู่ → เสี่ยง
- `evidence_freshness_status = STALE` → สแกนเก่า/เทสต์เก่า
- `HAS_OPEN_FINDINGS` → ช่องโหว่/issue ยังไม่ถูกปิด

### 7.3 UNKNOWN vs NONE

- `NONE` = เรารู้ว่าไม่มี evidence ที่เกี่ยวข้อง
- `UNKNOWN` = ไม่แน่ใจเพราะข้อมูลไม่ครบ / parsing format ไม่เข้าใจ

ใน strict mode สำหรับ critical:

- `NONE` และ `STALE` ส่วนใหญ่ต้องถือว่าเป็น risk สูง

---

## 8. KiloCode Usage Examples

### 8.1 ใช้ audit บน Kilo สำหรับ core service

```bash
smartspec_security_evidence_audit \
  --spec-ids=core_auth \
  --target-env=prod \
  --run-label=core-auth-security \
  --security-policy-paths=".spec/policies/security/*.md" \
  --sast-report-paths="reports/sast/core_auth/*.json" \
  --dast-report-paths="reports/dast/core_auth/*.json" \
  --dependency-report-paths="reports/deps/core_auth/*.json" \
  --evidence-max-age=30d \
  --safety-mode=strict \
  --kilocode \
  --stdout-summary
```

บน Kilo:

- Orchestrator จะ loop ตาม security domain (authn, authz, data_protection ฯลฯ)
- Code mode อ่าน reports แบบ read-only
- Orchestrator สรุป coverage / freshness / risk ต่อ domain

### 8.2 ปิด subtasks

```bash
smartspec_security_evidence_audit \
  --spec-ids=small_service \
  --target-env=staging \
  --run-label=small-service-security \
  --kilocode \
  --nosubtasks
```

- ใช้ reasoning เดียวตรง ๆ ไม่แตก subtasks เพิ่ม เหมาะกับ scope เล็ก

---

## 9. Multi-repo / Multi-registry Examples

### 9.1 Monorepo หลาย service

```bash
smartspec_security_evidence_audit \
  --spec-ids=search_api,ranking_service \
  --target-env=prod \
  --run-label=search-stack-security \
  --repos-config=.spec/repos.yaml \
  --registry-dir=.spec/registry \
  --sast-report-paths="reports/sast/**/*.json" \
  --dast-report-paths="reports/dast/**/*.json" \
  --dependency-report-paths="reports/deps/**/*.json" \
  --safety-mode=strict
```

- ใช้ repos-config + registry map requirement ที่ข้ามหลาย service
- แสดงความครอบคลุมและ risk ต่อ service/domain

### 9.2 หลาย repo / หลายทีม

```bash
smartspec_security_evidence_audit \
  --spec-ids=teamA_checkout,teamB_payments \
  --target-env=staging \
  --run-label=checkout-payments-security \
  --workspace-roots="../teamA;../teamB" \
  --registry-dir=../platform/.spec/registry \
  --sast-report-paths="../teamA/reports/sast/**/*.json;../teamB/reports/sast/**/*.json" \
  --dast-report-paths="../teamA/reports/dast/**/*.json;../teamB/reports/dast/**/*.json" \
  --dependency-report-paths="../teamA/reports/deps/**/*.json;../teamB/reports/deps/**/*.json"
```

- รายงานจะบอก requirement cross-team และ evidence มาจาก repo ไหน

---

## 10. UI Security Examples

ตัวอย่าง requirement สำหรับ UI เช่น:

- ป้องกัน XSS (Content Security Policy, output encoding)
- ป้องกัน CSRF (token, SameSite cookie)
- ป้องกัน clickjacking (X-Frame-Options, CSP frame-ancestors)
- ใช้ secure cookies (Secure, HttpOnly, SameSite)

workflow จะพยายาม:

- map requirement เหล่านี้เข้ากับ evidence เช่น:
  - scanner report (XSS/CSRF findings)
  - security headers จาก gateway/backend
  - UI security tests/regression tests
- UI governance (JSON-first / inline / opt-out) ใช้เป็น context หา component
  แต่ไม่เปลี่ยนเกณฑ์ว่า requirement ผ่านหรือยัง

---

## 11. Best Practices & Anti-patterns

### 11.1 Best Practices

- เขียน security requirements ให้ชัดใน spec/policy ก่อน
- เปิดให้ SAST/DAST/dep scan เริ่มรันใน CI ก่อนใช้ audit เป็นหลักฐาน
- ใช้ `--safety-mode=strict` กับระบบที่ critical / sensitive data สูง
- ตั้ง `--evidence-max-age` ให้เหมาะ (เช่น 30–90 วัน ตาม risk profile)
- เก็บรายงานเป็น artifact (เช่นแนบกับ release หรือเก็บใน repo)
- ใช้ผลร่วมนกับ `/smartspec_release_readiness` และ
  `/smartspec_ci_quality_gate` ในการตัดสินใจ

### 11.2 Anti-patterns

- คิดว่า “มีสแกนครั้งหนึ่งเมื่อปีที่แล้ว” = ยังปลอดภัยอยู่ (evidence stale มาก)
- ไม่เขียน requirement แต่หวังให้ workflow เดา requirement เอง
- เอา output จาก audit ไปใช้เป็นข้ออ้างว่า "ผ่าน audit" โดยไม่มี process
  risk acceptance ที่ชัดเจน

---

## 12. FAQ / Troubleshooting

### Q1: ถ้าไม่มี report หรือ log อะไรเลย audit จะให้ผลอย่างไร?

- ส่วนใหญ่ requirement จะได้ `coverage_status=NONE` หรือ `UNKNOWN`
- ใน strict mode สำหรับ critical จะกลายเป็น critical gap / blocking
- แนะนำให้เพิ่ม scanner/test ผ่าน `/smartspec_ci_quality_gate` ก่อน

### Q2: ถ้า evidence เป็นไฟล์เก่ามาก ๆ โดยไม่มี timestamp ชัดเจน?

- `evidence_freshness_status` จะเป็น `UNKNOWN`
- manual แนะนำให้ treat เป็น risk และปรับ process ให้เก็บ timestamp ชัดเจน

### Q3: ถ้าพบ secrets ใน log/รายงาน?

- audit จะอธิบายว่า **พบ secret ในไฟล์ X** แต่ไม่ copy ค่า secret
- การ rotate/clean up/ปิดช่องทาง log นั้นเป็นงานของทีม security/infra

---

จบคู่มือภาษาไทยสำหรับ `/smartspec_security_evidence_audit v5.6.2`.
หากต่อไปมีการเปลี่ยน semantics สำคัญ (เช่น การคิด evidence age หรือการ map
finding) ควรออก manual v5.7 และระบุช่วงเวอร์ชัน workflow ที่รองรับให้ชัดเจน

