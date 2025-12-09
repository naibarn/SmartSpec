---
manual_name: /smartspec_data_migration_governance Manual (TH)
manual_version: 5.6
compatible_workflow: /smartspec_data_migration_governance
compatible_workflow_versions: 5.6.2 – 5.6.x
role: user/operator manual (data platform, infra, security, product, release)
---

# /smartspec_data_migration_governance คู่มือการใช้งาน (v5.6, ภาษาไทย)

## 1. ภาพรวม (Overview)

คู่มือนี้อธิบายวิธีใช้งาน workflow:

> `/smartspec_data_migration_governance v5.6.2`

workflow นี้ทำหน้าที่เป็น **ชั้น governance** สำหรับงาน data migration:

- ตรวจความสอดคล้องของแผน/การย้ายข้อมูลกับ
  - data model / schema evolution
  - data classification (critical/high/medium/low)
  - data privacy / retention / residency policy
- ประเมินว่ามี **backup / rollback / verification / data quality check** เพียงพอหรือไม่
- ประเมิน **risk level ต่อแต่ละ migration unit** (table/dataset/shard/tenant segment)
- แนะนำ `blocking_for_release` เป็นสัญญาณประกอบการตัดสินใจ release

### 1.1 ความจำเป็นที่ต้องใช้ workflow นี้

การย้ายข้อมูล (data migration) มีความเสี่ยงสูงเป็นพิเศษ เพราะ:

- ถ้าพลาด อาจกระทบ **ข้อมูลลูกค้า** หรือ **ข้อมูลธุรกิจหลัก** แบบย้อนกลับยาก
- migration จำนวนมากถูกทำแบบ “script ครั้งเดียวแล้วลืม” ไม่เหลือหลักฐานว่าเคย review risk
- หน่วยงานกำกับ (regulator/auditor) มักต้องการเห็น
  - ว่ามี **backup/rollback** จริง
  - ว่าการย้ายข้อมูลไม่ละเมิด **policy/กฎหมาย** ที่กำหนด

`/smartspec_data_migration_governance` ช่วยรวบรวม context เหล่านี้
แล้วให้มุมมองเชิง governance ที่เป็นระบบและ repeatable

### 1.2 ข้อดีของการใช้

- ได้มุมมองรวมว่า migration ครั้งนี้:
  - กระทบ dataset/table ไหนบ้าง
  -แต่ละ unit มี backup/rollback/verification แค่ไหน
  -ผิด/เสี่ยง policy ตรงไหน
- สร้าง `blocking_for_release` เป็น input ให้
  `/smartspec_release_readiness` และ chain การ approve release
- ทำให้การคุยกับ data owner, security, compliance ง่ายขึ้น
  เพราะทุกคนเห็นภาพเดียวกันในรายงานเดียว
- กลายเป็นหลักฐาน (artifact) ว่า
  - migration ผ่านการพิจารณาด้านความเสี่ยงแล้ว

### 1.3 สิ่งผิดพลาดที่มักเกิดขึ้นถ้าไม่ใช้ (หรือไม่มี governance layer แบบนี้)

- ย้ายข้อมูลโดยไม่มี **backup/rollback** ที่ชัด →
  - พลาดครั้งเดียว ต้อง rollback แบบ manual / ใช้เวลาเยอะ
- ลืมคำนึงถึง **data classification** →
  - ย้ายข้อมูล critical/PII ไปยัง environment/region ที่ไม่อนุญาต
- ไม่ตรวจ **data quality หลัง migration** →
  - รายงานธุรกิจผิด, dashboard เพี้ยน, ML model เสีย
- ไม่มี artifact แสดงว่าเคย review risk →
  - ตอบ regulator / auditor ยาก
- กรณี **multi-tenant**:
  - เสี่ยงย้ายข้อมูลผิด tenant, ผิดระบบ segmentation

workflow นี้ไม่ได้การันตีว่าปลอดภัย 100% แต่ช่วยลดโอกาสผิดพลาดแบบ
"ลืมคิดประเด็นสำคัญ" ลงอย่างมาก

---

## 2. What’s New in v5.6

### 2.1 Status model ต่อ migration unit

เพิ่มโมเดลสถานะชัดเจน เช่น:

- `coverage_status = IN_SCOPE | OUT_OF_SCOPE | UNKNOWN`
- `backup_status = PRESENT | PARTIAL | NONE | UNKNOWN`
- `rollback_status = PRESENT | WEAK | NONE | UNKNOWN`
- `verification_status = STRONG | BASIC | NONE | UNKNOWN`
- `policy_alignment_status = ALIGNED | RISKY_BUT_JUSTIFIED | VIOLATES | UNKNOWN`
- `residency_risk_status = NONE | POTENTIAL | CONFIRMED | UNKNOWN`
- `migration_style = IN_PLACE | BACKFILL | DUAL_WRITE | OTHER | UNKNOWN`
- `migration_volume = SMALL | MEDIUM | LARGE | UNKNOWN`
- `multi_tenant_risk = NONE | POTENTIAL | CONFIRMED | UNKNOWN`
- `risk_level = LOW | MEDIUM | HIGH | CRITICAL`
- `blocking_for_release = true | false`

### 2.2 Strict-mode rules ที่ชัดเจน

ใน `--safety-mode=strict`:

- ถ้า `data_class in {critical, high}` และ
  - `backup_status=NONE/UNKNOWN` → blocking
  - `rollback_status=NONE/UNKNOWN` → blocking
  - `policy_alignment_status=VIOLATES` → blocking
  - `residency_risk_status=CONFIRMED` และ policy ไม่อนุญาต → blocking
  - `verification_status=NONE` + `migration_volume=LARGE` หรือ
    `migration_style` เสี่ยง → ส่วนใหญ่ควร blocking

### 2.3 การพิจารณา style/volume/multi-tenant

- นำ `migration_style`, `migration_volume`, `multi_tenant_risk` มาใช้เป็น
  ปัจจัยเสริมในการคำนวณ `risk_level` และ `blocking_for_release`

### 2.4 ความสัมพันธ์กับ release readiness

- รายงานจาก workflow นี้ไม่ override การตัดสินใจ release
- แต่ `blocking_for_release` ถูกออกแบบให้ใช้ร่วมกับ
  `/smartspec_release_readiness` และ workflow governance อื่น

---

## 3. Backward Compatibility Notes

- Manual v5.6 นี้รองรับ `/smartspec_data_migration_governance`
  ตั้งแต่ **v5.6.2 เป็นต้นไป** (5.6.x)
- ไม่มีการลบ/เปลี่ยนค่าสถานะหรือ flag เดิม (workflow นี้เป็นตัวใหม่)
- `--strict` ยังคงเป็น alias ของ `--safety-mode=strict`

---

## 4. Core Concepts

### 4.1 Migration unit

หน่วยที่ใช้ประเมิน governance ต่อ 1 ชิ้น เช่น:

- table หรือ view
- dataset หรือ partition
- shard / tenant segment

แต่ละ unit จะมีชุด status ที่กล่าวไปข้างต้นเพื่อให้เห็นภาพว่า

- scope ครอบคลุมไหม
- มี backup/rollback ไหม
- ผิด policy / residency หรือไม่
- เสี่ยง multi-tenant หรือไม่

### 4.2 Risk model & blocking_for_release

- `risk_level` และ `blocking_for_release` คือการสังเคราะห์จาก
  - data class
  - backup/rollback/verification
  - policy/residency alignment
  - volume/style/multi-tenant
- strict-mode จะใช้กฎที่เข้มงวดกว่า normal-mode

### 4.3 Governance-only

workflow นี้:

- ไม่สร้าง/แก้ SQL หรือ ETL จริง
- ไม่รัน migration job
- ไม่แตะ config/database จริง
- ทำหน้าที่แค่ **อ่านเอกสาร/สคริปต์** แล้วสรุป risk + gap

---

## 5. Quick Start Examples

### 5.1 ตรวจ data migration สำหรับ user table (prod)

```bash
smartspec_data_migration_governance \
  --spec-ids=user_service \
  --run-label=user-table-migration-prod \
  --data-model-paths="schemas/user/*.sql" \
  --migration-plan-paths="docs/migration/user_table/*.md" \
  --migration-script-paths="migrations/user/*.sql" \
  --data-policy-paths=".spec/policies/data/*.md" \
  --report-format=md \
  --stdout-summary
```

### 5.2 ใช้ strict mode กับ PII-critical dataset

```bash
smartspec_data_migration_governance \
  --spec-ids=payments_service \
  --run-label=payments-pii-migration \
  --data-model-paths="schemas/payments/*.sql" \
  --migration-plan-paths="docs/migration/payments/*.md" \
  --migration-script-paths="migrations/payments/*.sql" \
  --data-policy-paths=".spec/policies/data/*.md" \
  --source-env=prod \
  --target-env=prod \
  --region-pairs="eu-central-1:eu-central-1" \
  --safety-mode=strict \
  --report-format=json \
  --stdout-summary
```

### 5.3 รวม cross-service migration

```bash
smartspec_data_migration_governance \
  --spec-ids=orders_service,inventory_service \
  --include-dependencies \
  --run-label=orders-inventory-migration \
  --repos-config=.spec/repos.yaml \
  --registry-dir=.spec/registry \
  --migration-plan-paths="docs/migration/**/*.md" \
  --migration-script-paths="migrations/**/*.sql" \
  --report-format=md
```

---

## 6. CLI / Flags Cheat Sheet

- Scope & label
  - `--spec-ids`
  - `--include-dependencies`
  - `--run-label`
- Migration artifacts
  - `--migration-plan-paths`
  - `--migration-script-paths`
  - `--pipeline-config-paths`
  - `--data-model-paths`
- Policy & classification
  - `--data-policy-paths`
  - `--registry-dir`, `--registry-roots`
- Environment & residency
  - `--source-env`, `--target-env`
  - `--region-pairs`
- Evidence of runs/tests
  - `--migration-report-paths`
  - `--data-quality-report-paths`
  - `--audit-log-paths`
- Multi-repo & index & safety
  - `--workspace-roots`
  - `--repos-config`
  - `--index`, `--specindex`
  - `--safety-mode=normal|strict` (`--strict`)
- Output & KiloCode
  - `--report-format=md|json`
  - `--report-dir`
  - `--stdout-summary`
  - `--kilocode`, `--nosubtasks`

---

## 7. วิธีอ่านรายงานที่ได้

รายงานจะแบ่งออกเป็น:

1. **Scope overview**
   - service/spec-id ที่เกี่ยวข้อง
   - environment/region
   - summary สั้น ๆ ของ migration

2. **Per-unit status table**
   - แสดงค่าต่าง ๆ:
     - `unit_id`, `data_class`, `coverage_status`, `backup_status`,
       `rollback_status`, `verification_status`,
       `policy_alignment_status`, `residency_risk_status`,
       `migration_style`, `migration_volume`, `multi_tenant_risk`,
       `risk_level`, `blocking_for_release`, `notes`

3. **Gaps & risks**
   - list unit ที่เป็น risk สูง โดยเรียงตาม `risk_level` และ `blocking_for_release`

4. **Summary**
   - นับจำนวน unit ในแต่ละ risk level
   - นับจำนวนที่ blocking vs non-blocking

---

## 8. KiloCode Usage Examples

### 8.1 ใช้กับ Kilo สำหรับ migration ชุดใหญ่

```bash
smartspec_data_migration_governance \
  --spec-ids=billing_service,invoice_service \
  --include-dependencies \
  --run-label=billing-invoice-migration \
  --migration-plan-paths="docs/migration/**/*.md" \
  --migration-script-paths="migrations/**/*.sql" \
  --data-policy-paths=".spec/policies/data/*.md" \
  --kilocode \
  --stdout-summary
```

บน Kilo:

- Orchestrator จะประมวลผลทีละ migration scope (spec-id/group)
- แตก subtasks เพื่อตรวจ backup, rollback, verification, policy
- code-mode อ่านไฟล์ทั้งหมดแบบ read-only

### 8.2 ปิด subtasks ใน scope เล็ก

```bash
smartspec_data_migration_governance \
  --spec-ids=small_service \
  --run-label=small-migration \
  --migration-plan-paths="docs/migration/small_service/*.md" \
  --kilocode \
  --nosubtasks
```

---

## 9. Multi-repo / Multi-registry Examples

### 9.1 Monorepo หลาย service

```bash
smartspec_data_migration_governance \
  --spec-ids=search_service,analytics_service \
  --run-label=search-analytics-migration \
  --repos-config=.spec/repos.yaml \
  --registry-dir=.spec/registry \
  --migration-plan-paths="docs/migration/**/*.md" \
  --migration-script-paths="migrations/**/*.sql" \
  --report-format=md
```

### 9.2 หลาย repo หลายทีม

```bash
smartspec_data_migration_governance \
  --spec-ids=teamA_users,teamB_subscriptions \
  --run-label=users-subscriptions-migration \
  --workspace-roots="../teamA;../teamB" \
  --registry-dir=../platform/.spec/registry \
  --migration-plan-paths="../teamA/docs/migration/**/*.md;../teamB/docs/migration/**/*.md" \
  --migration-script-paths="../teamA/migrations/**/*.sql;../teamB/migrations/**/*.sql"
```

---

## 10. UI / UX Data Migration

ถ้า migration กระทบข้อมูลที่เกี่ยวกับ UI เช่น:

- user preferences
- UI config
- feature flags / personalization

ควรให้ความสำคัญเพิ่มเติม:

- consistency ของ UI state หลัง migration (user แต่ละคน/segment เห็นของถูกต้องไหม)
- ไม่หลุด PII/ข้อมูลส่วนตัว ในการย้าย/เก็บ log
- mapping ระหว่าง UI governance (UI JSON-first หรือ inline) กับ data store ที่เกี่ยวข้อง

---

## 11. ข้อดีของการใช้ vs ความเสี่ยงหากไม่ใช้

### 11.1 ข้อดีของการใช้

- ลดความเสี่ยง human error ในการ “ลืมคิด” ประเด็นสำคัญ
- มีภาษากลาง (status model) ที่ทุกทีมเข้าใจตรงกัน
- ช่วยให้การ review ของ data owner, security, compliance มีโครงสร้าง
- ตรวจความพร้อมก่อน release ได้เป็นระบบ (ผ่าน `blocking_for_release`)

### 11.2 ความเสี่ยงหากไม่ใช้ (หรือไม่มี governance แบบนี้)

- migration ที่ไม่มี backup/rollback ชัดเจน → rollback ยากหากผิดพลาด
- migration ที่ข้าม region/เขตข้อมูลโดยไม่เช็ค policy → เสี่ยงไม่สอดคล้องกับกฎหมาย/สัญญา
- multi-tenant migration ที่ไม่ตรวจ isolation → เสี่ยงข้อมูลลูกค้าปะปนกัน
- ไม่มีรายงานที่แสดงว่าเคย review risk → ตอบ auditor / regulator ลำบาก

---

## 12. FAQ / Troubleshooting

**Q1: ถ้าไม่มี migration plan เป็นเอกสารเลย ใช้ workflow นี้ได้ไหม?**  
ได้ แต่ผลลัพธ์จะมี `coverage_status=UNKNOWN` เยอะ และเป็นสัญญาณว่าควรทำ
migration plan ให้ชัดก่อน

**Q2: workflow นี้รับประกันว่า migration ปลอดภัยแน่ ๆ ไหม?**  
ไม่ใช่การันตี 100% แต่ช่วยลด blind spot และให้สัญญาณเชิง governance
ว่าตรงไหนควรปิดช่องโหว่ก่อนเดินหน้า

**Q3: ต้องใช้ strict mode ตลอดไหม?**  
ไม่จำเป็น แต่แนะนำใช้ strict กับ migration ที่กระทบ
- ข้อมูล critical/high
- ข้อมูลที่มีภาระด้านกฎหมาย/regulation สูง

---

จบคู่มือภาษาไทยสำหรับ `/smartspec_data_migration_governance v5.6.2`.
ถ้าในอนาคตมีการเปลี่ยน semantics หลัก (เช่น status model หรือ strict-mode rules)
ควรออก manual v5.7 และระบุช่วงเวอร์ชัน workflow ที่รองรับให้ชัดเจน
