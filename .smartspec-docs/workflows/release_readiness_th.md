---
manual_name: /smartspec_release_readiness Manual
manual_version: 5.6
compatible_workflow: /smartspec_release_readiness
compatible_workflow_versions: 5.6.2 – 5.6.x
role: user/operator manual (release managers, tech leads, senior ICs)
---

# /smartspec_release_readiness Manual (v5.6)

## 1. Overview

This manual explains **how to use** the workflow:

> `/smartspec_release_readiness v5.6.2`

Its job isช่วยคุณตอบคำถามว่า:

> “ชุดงานในสโคปนี้ **พร้อมปล่อยจริงไหม** (ทั้งในมุม spec, tasks, NFR, compat, multi-repo, UI) หรือยังมีรูรั่วอะไรอยู่บ้าง?”

Workflow นี้เป็น **verification / governance** และเป็น **NO-WRITE** 100%:

- ไม่แตะโค้ด
- ไม่แก้ spec / tasks
- ไม่แก้ registry
- ทำแค่: อ่านทุกอย่าง แล้วออกเป็น **release readiness report** ใน `.spec/reports/...`

มันถูกออกแบบให้เป็น **ด่านสุดท้ายก่อน deploy** หรือก่อน promote ไป staging/production ในระบบที่ใช้ SmartSpec เป็นแกนกลาง

---

## 2. What’s New in v5.6

แมนนวลนี้ครอบคลุมเวอร์ชัน workflow **v5.6.2** ซึ่งเพิ่ม/ล็อกพฤติกรรมสำคัญเพิ่มจากแนวคิดดิบ ๆ ใน coverage summary:

### 2.1 เกณฑ์ READY / READY_WITH_RISKS / BLOCKED ที่ชัดเจน

- นิยามว่าเมื่อไหร่ **ห้าม** ให้สถานะ `READY` เช่น
  - มี breaking API/data contract โดยไม่มี migration/compat plan + tasks
  - NFR สำคัญยังไม่มี evidence เลย
  - config ที่จำเป็นต่อ `--target-env` ขาดหาย
- และอธิบายว่า `--safety-mode=strict` ต้องทำให้ issue พวกนี้ **ดันสถานะขึ้นไปอย่างน้อย** `READY_WITH_RISKS` หรือถึงขั้น `BLOCKED` ได้

### 2.2 แยกบทบาทกับ Data Migration Governance ชัดเจน

- release readiness:
  - เช็กแค่ **มี/ไม่มี** migration requirements + tasks + artifacts ที่ผูกกับ spec
  - ถ้าไม่มีในกรณีที่ควรมี → นับเป็น risk / blocking condition
- ส่วนการออกแบบ / execute migration workflow จริง ๆ จะไปอยู่ใน
  - `/smartspec_data_migration_governance` (แยกต่างหาก)

### 2.3 ทำให้ `--safety-mode` / `--strict` “มีผลจริง”

- `--safety-mode=normal` (default)
  - ยอมรับ `READY_WITH_RISKS` ได้ ขึ้นกับ policy ทีม
- `--safety-mode=strict` หรือ `--strict`
  - ถ้ามี critical risk ใด ๆ อยู่ (NFR, compat, migration, security, duplication ที่หนัก) → ห้ามออกผล `READY` ให้ spec นั้น หรือ release รวม

### 2.4 ห้ามเดา spec-id นอก SPEC_INDEX

- ถ้าไม่ได้ระบุ `--spec-ids` และไม่มี mapping จาก SPEC_INDEX/config ที่ชัดเจน:
  - workflow จะ **ไม่เดา** scope จากไฟล์ที่มัน “เห็น” เอง
  - ให้ถาม (Ask/Architect mode) หรือหยุดพร้อมแจ้งว่า scope ไม่ชัดเจน

### 2.5 Cross-repo duplication check เป็น first-class citizen

- มีขั้นตอนเฉพาะสำหรับเช็กว่า release นี้กำลังสร้าง **การซ้ำซ้อน** ของ:
  - shared API
  - shared data model
  - shared policy
  - shared UI component
- ใช้ข้อมูลจาก primary + supplemental registries เพื่อช่วยตัดสินใจ

### 2.6 UI governance + UI JSON opt-out ที่ไม่กำกวม

- แยกเคส **JSON-first UI** vs **inline UI** ชัดเจน
- ถ้าโปรเจกต์มีการ **opt-out** จาก JSON-first UI (เช่นระบุใน SPEC_INDEX หรือ config):
  - workflow ต้องเคารพการตัดสินใจนั้น
  - ไม่ถือว่าไม่มี `ui.json` เป็น defect โดยตัวมันเอง

### 2.7 Guardrail กัน AI เติม / ตัด NFR เอง

- กำชับว่า workflow ต้อง:
  - ไม่เพิ่ม NFR ใหม่เข้าไปเอง
  - ไม่เปลี่ยนค่า SLA ที่ระบุใน spec
  - ไม่ตัด NFR เดิมออกจากการพิจารณา
- ถ้ามีข้อเสนอ (proposal) เพิ่มเติม ต้องแยกออกจาก verdict readiness ชัดเจน

---

## 3. Backward Compatibility Notes

- Manual v5.6 นี้รองรับ workflow `/smartspec_release_readiness` **ตั้งแต่ 5.6.2 เป็นต้นไป**
- Workflow นี้เป็น **ตัวใหม่** ใน family SmartSpec: ไม่มีแมนนวล legacy ก่อนหน้าให้ต้อง migrate
- กติกาหลักที่สืบทอดจากระบบเดิม:
  - ไม่แตะ spec / tasks / โค้ด (NO-WRITE)
  - ใช้ index/registry + multi-repo flags ร่วมกับ workflow อื่นแบบเดียวกัน
  - รองรับ `--kilocode` เหมือน workflow governance อื่น ๆ

ถ้าคุณอัปเดต workflow patch (เช่นจาก 5.6.2 → 5.6.3) โดยไม่เปลี่ยน flag/mode หลัก แมนนวลฉบับนี้ยังถือว่าใช้ร่วมได้อยู่

---

## 4. Core Concepts (เข้าใจภาพก่อนลงมือใช้)

### 4.1 Release scope = ชุด spec-id

- ทุกครั้งที่ใช้ workflow นี้ ต้องมี “เซ็ตของ spec-id” ที่จะปล่อยจริง
- scope จะถูกอ่านจาก:
  - `--spec-ids=<id1,id2,...>`
  - และถ้าเปิด `--include-dependencies` จะขยายเพิ่มจาก registries + SPEC_INDEX

### 4.2 Evidence = สิ่งที่ workflow อ่านได้

- spec + tasks
- registries (API / data-model / ui-component / critical-sections / ownership)
- test results / coverage (ถ้าระบุตำแหน่งชัดเจนในระบบคุณ)
- env/config files ตาม `--env-config-paths`

### 4.3 Readiness dimensions (มุมที่ workflow เช็ก)

ต่อ spec-id หนึ่งตัว workflow จะมองหลายแกน:

1. NFR & SLA vs evidence
2. Task completion (โดยเฉพาะ test / security / migration / ops / UI)
3. Environment & configuration สำหรับ `--target-env`
4. Backward compatibility (API, data model, migrations)
5. Cross-repo duplication (ใช้ registry)
6. UI governance (JSON-first vs inline, opt-out หรือไม่)

### 4.4 Status 3 ระดับ

ต่อ spec และต่อ release ทั้งชุด จะมี status 3 แบบ:

- `READY`
- `READY_WITH_RISKS`
- `BLOCKED`

โดยมีเกณฑ์บังคับ (จะอธิบายใน Section 7) ว่ากรณีไหน **ห้าม** เป็น `READY`

---

## 5. Quick Start (วิธีใช้แบบสั้นที่สุด)

### 5.1 Single-repo, basic case

กรณีโครงการเล็ก ๆ มี repo เดียว, index canonical, ไม่ยุ่ง multi-repo:

```bash
smartspec_release_readiness \
  --spec-ids=checkout_api,order_core \
  --release-label=2025.12.09-prod \
  --target-env=prod \
  --env-config-paths="config/*.yaml" \
  --report-format=md \
  --stdout-summary
```

ผลลัพธ์:

- ไฟล์รายงาน เช่น:
  - `.spec/reports/smartspec_release_readiness/2025-12-09T13-05_checkout_api+order_core.md`
- ใน stdout จะสรุปประมาณว่า:
  - overall status = `READY_WITH_RISKS`
  - 2 specs, 1 READY, 1 READY_WITH_RISKS, 0 BLOCKED

### 5.2 Single-repo + strict mode

```bash
smartspec_release_readiness \
  --spec-ids=checkout_api \
  --release-label=v1.4.0-rc1 \
  --target-env=staging \
  --safety-mode=strict \
  --stdout-summary
```

กรณีนี้:

- ถ้า checkout_api ยังมี NFR สำคัญไม่มี evidence → ห้ามให้สถานะ `READY`
- อย่างต่ำต้องเป็น `READY_WITH_RISKS` หรือ `BLOCKED`

### 5.3 Multi-repo, multi-registry, include dependencies

```bash
smartspec_release_readiness \
  --spec-ids=payments_gateway \
  --include-dependencies \
  --release-label=pay-2025.12.15 \
  --target-env=prod \
  --repos-config=.spec/repos_config.yaml \
  --registry-dir=.spec/registry \
  --registry-roots="../shared/.spec/registry;../legacy/.spec/registry" \
  --env-config-paths="config/*.yaml;infra/*.tf" \
  --report-format=json
```

เคสนี้รายงานจะ:

- ขยาย scope ไปยัง spec อื่นที่ payments_gateway พึ่งพา (เช่น core_billing, user_profile) ตาม registry + SPEC_INDEX
- แสดง cross-repo impact ว่ามี asset ไหนถูก reuse vs มีความเสี่ยงจะ duplicate
- เซฟรายงานแบบ JSON เผื่อให้ CI/CD หรือ dashboard system ไปอ่านต่อ

---

## 6. CLI / Flags Cheat Sheet (มุมคนใช้งาน)

> รายละเอียดลึกอยู่ใน workflow spec แต่ตรงนี้สรุปจากมุมมองผู้ใช้

### 6.1 Scope และ release metadata

- `--spec-ids=<id1,id2,...>`
  - ระบุ spec ที่อยู่ใน release นี้
  - **ต้อง** เป็น spec-id ที่มีใน SPEC_INDEX เท่านั้น

- `--include-dependencies`
  - ให้ workflow ขยาย scope ตาม dependency จาก registry + SPEC_INDEX

- `--release-label=<string>`
  - ชื่อ release ที่อยากให้ไปโผล่ในชื่อไฟล์รายงาน + heading ข้างใน

### 6.2 Environment & config

- `--target-env=<env>`
  - `dev`, `staging`, `prod`, หรือ environment อื่นๆ

- `--env-config-paths="<glob1>;<glob2>"`
  - path ของ config / infra เช่น `config/*.yaml;infra/*.tf`

### 6.3 Index / registry / multi-repo

- `--workspace-roots` / `--repos-config`
  - ใช้ `--repos-config` ถ้ามี (ละเอียดกว่า)
  - ใช้ `--workspace-roots` เมื่อแค่บอก root คร่าว ๆ

- `--registry-dir`
  - ที่อยู่ primary registry (ปกติคือ `.spec/registry`)

- `--registry-roots`
  - registry เพิ่มเติมแบบ read-only (เช่น shared monorepo อื่น)

- `--index`, `--specindex`
  - ใช้ override ถ้า SPEC_INDEX ไม่ได้อยู่ในตำแหน่ง canonical

### 6.4 Safety / kilocode / output

- `--safety-mode=normal|strict` (หรือ `--strict`)
  - `normal` = สบาย ๆ แต่อย่างน้อยก็ยังเตือน risk
  - `strict` = ใช้เป็น **gate จริง** สำหรับ critical risk

- `--kilocode`
  - ให้ workflow ทำตัวแบบรู้จัก Kilo (Ask/Architect + Orchestrator-per-check) แต่ก็ยัง NO-WRITE

- `--nosubtasks`
  - ปิดฟีเจอร์ auto subtasks (แต่อีกหลายเคสแนะนำให้เปิดไว้)

- `--report-format=md|json`
- `--report-dir=<path>`
- `--stdout-summary`

---

## 7. How Readiness Is Decided (เกณฑ์ตัดสินสถานะ)

### 7.1 ระดับ spec-id

ต่อ spec หนึ่งตัว workflow จะสรุปว่ามันเป็น:

- `READY`
- `READY_WITH_RISKS`
- `BLOCKED`

ด้วยกติกาขั้นต่ำ:

1. **ห้าม READY ถ้า**
   - NFR สำคัญ (เช่น latency, availability, data loss) ไม่มี evidence เลย
   - มี breaking API/data contract change ที่ไม่มี migration/compat plan + tasks
   - config สำคัญสำหรับ `--target-env` ขาดหายหรือไม่ชัดเจน

2. ภายใต้ `--safety-mode=strict` / `--strict`
   - ถ้าเจอ critical risk ใด ๆ ในหมวด:
     - NFR
     - compat/migration
     - security
     - cross-repo duplication ที่รุนแรง
     - ops/observability ที่ขาดจนกระทบ production
   - สถานะ spec ต้องอย่างน้อย `READY_WITH_RISKS` หรือ `BLOCKED`

3. ถ้าไม่มี risk ระดับ critical และ risk ที่เหลือเล็กน้อย → `READY` ได้

### 7.2 ระดับ release ทั้งชุด

- workflow จะ aggregate ทุก spec แล้วสรุปสถานะรวม
- ถ้ามีแม้แต่หนึ่ง spec เป็น `BLOCKED` → release โดยรวม **ควรถือเป็น BLOCKED**
- ถ้ามีหลาย spec เป็น `READY_WITH_RISKS` → รายงานจะระบุ clearly ว่า release นี้พร้อมแต่มีอะไรที่ต้องรับความเสี่ยง

---

## 8. KiloCode Usage Examples

### 8.1 Governance-only, Ask/Architect mode

```bash
smartspec_release_readiness \
  --spec-ids=billing_core \
  --release-label=billing-1.2.0 \
  --target-env=prod \
  --kilocode \
  --safety-mode=strict \
  --stdout-summary
```

ภายใต้ Kilo:

- workflow จะใช้ Orchestrator แยก sub-check ของ NFR, compat, UI, ฯลฯ
- ไม่มีสิทธิ์แก้อะไร (NO-WRITE) แม้ว่าจะอยู่ใน Code mode ตอนอ่านไฟล์

### 8.2 ปิด subtasks (สำหรับเคสเล็ก ๆ)

```bash
smartspec_release_readiness \
  --spec-ids=small_feature \
  --target-env=staging \
  --kilocode \
  --nosubtasks
```

- เคสนี้ workflow จะยังรู้ว่ารันอยู่บน Kilo แต่จะไม่แตกย่อยเป็น subtasks เยอะ ๆ
- เหมาะกับ release เล็ก ๆ ที่ไม่อยากให้ pipeline มี reasoning steps เยอะเกินจำเป็น

---

## 9. Multi-repo / Multi-registry Usage Examples

### 9.1 Monorepo + shared registry

```bash
smartspec_release_readiness \
  --spec-ids=search_api \
  --include-dependencies \
  --repos-config=.spec/repos.yaml \
  --registry-dir=.spec/registry \
  --registry-roots="../platform/.spec/registry" \
  --target-env=prod
```

- `repos-config` บอกว่า search_api อยู่ repo ไหน และพึ่งพา repo ไหนอีกบ้าง
- registry หลักกับ registry เสริมใช้ร่วมกันในการ detect duplicate ของ shared model

### 9.2 หลายทีม หลาย repo

```bash
smartspec_release_readiness \
  --spec-ids=teamA_payments,teamB_notifications \
  --workspace-roots="../teamA;../teamB" \
  --registry-dir=../platform/.spec/registry \
  --target-env=prod \
  --safety-mode=strict
```

- เคสนี้ค่าที่น่าสนใจคือ cross-repo duplication:
  - เช่น ทั้งทีม A/B ต่างสร้าง Notification model ของตัวเอง ทั้งที่ platform มี shared model อยู่แล้ว → จะขึ้นเตือนในรายงาน

---

## 10. UI JSON vs Inline UI Examples

### 10.1 โปรเจกต์ JSON-first UI

สมมุติใน SPEC_INDEX หรือ config มี field ระบุว่า project นี้ใช้ JSON-first UI:

```bash
smartspec_release_readiness \
  --spec-ids=web_checkout \
  --target-env=prod \
  --env-config-paths="config/*.yaml" \
  --stdout-summary
```

ในรายงานสำหรับ `web_checkout` จะมี:

- UI mode: `json-first`
- เช็กว่า `ui.json` มีอยู่และสอดคล้องกับ spec หรือไม่
- ถ้าไม่มี `ui.json` เลย ทั้งที่ project policy บอกว่า JSON-first → อย่างน้อยเป็น `READY_WITH_RISKS` ด้าน UI (หรือ `BLOCKED` ถ้า strict/policy กำหนด)

### 10.2 โปรเจกต์ opt-out จาก UI JSON separation

กรณีโปรเจกต์ระบุชัดว่าขอใช้ inline UI (เช่น field ใน SPEC_INDEX หรือ config):

```bash
smartspec_release_readiness \
  --spec-ids=admin_portal \
  --target-env=staging
```

- workflow จะ **เคารพ opt-out** นั้น
- จะไม่ mark ว่า “ไม่มี `ui.json` = defect” แต่จะเช็กแทนว่า:
  - `spec.md` อธิบาย flow / component / UX constraints ดีพอไหม
  - tasks ครอบคลุมงาน UI สำคัญหรือไม่

---

## 11. Best Practices & Anti-patterns

### 11.1 Best Practices

- ระบุ `--spec-ids` ให้ชัดในทุกครั้งที่รัน (ลดโอกาส scope เพี้ยน)
- ใช้ `--release-label` ให้ consistent ระหว่าง code, CI, และรายงาน
- รัน `verify_tasks_progress` ก่อน แล้วค่อยรัน release readiness
- ใน multi-repo ให้ใช้ `--repos-config` เป็นหลัก
- เปิด `--safety-mode=strict` บน pipeline จริงใน environment ที่ critical

### 11.2 Anti-patterns

- ปล่อยให้ workflow เดา scope จากไฟล์ (ห้ามทำ)
- ใช้ผล `READY_WITH_RISKS` โดยไม่อ่านรายละเอียด risk ข้างใน
- คาดหวังว่า workflow นี้จะออกแบบ/รัน data migration ให้เอง
- ละเลย registry แล้วไปสร้าง shared model ใหม่ซ้ำ ๆ ทุก repo

---

## 12. FAQ / Troubleshooting

### Q1: ทำไม spec บางตัวได้สถานะ `BLOCKED` ทั้งที่ dev บอกว่า "พร้อมแล้ว"?

เช็กสิ่งเหล่านี้:

- มี NFR สำคัญที่ไม่มี evidence เลยหรือไม่
- มี breaking API/data model change ที่ไม่มี migration/compat plan+tasks หรือเปล่า
- config สำหรับ `--target-env` ครบไหม
- อยู่ใน `--safety-mode=strict` หรือไม่ (strict จะเข้มกว่าปกติ)

### Q2: อยากให้ปล่อยได้แม้มี risk เล็กน้อย ควรทำอย่างไร?

- ใช้ `--safety-mode=normal`
- ปล่อยให้รายงานสรุปเป็น `READY_WITH_RISKS`
- ให้ release manager / tech lead อ่าน risk section แล้วตัดสินใจเอง

### Q3: ทำไมรายงานบอกว่า scope ไม่ชัด / ขอให้ระบุ spec-ids?

- เพราะ workflow **ห้ามเดา** spec-id นอก SPEC_INDEX
- ให้ระบุ `--spec-ids` ให้ชัด หรือสร้าง config/mapping ที่บอกว่า branch นี้เกี่ยวข้องกับ spec อะไร

### Q4: ทำไม UI ถึงถูก mark เป็น risk ทั้งที่ทีมเรายังไม่ได้ใช้ JSON-first?

- เช็กว่ามีการ opt-out อย่างเป็นทางการหรือยัง (ใน SPEC_INDEX หรือ config)
- ถ้ายังไม่มี แต่ทีมตัดสินใจแล้ว → ควรบันทึกลง config ให้ workflow มองเห็น

### Q5: ต้อง commit report ลง git ไหม?

- แนะนำให้ commit หรือเก็บเป็น CI artifact อย่างน้อยสำหรับ release สำคัญ
- จะช่วยเวลาย้อนดูเหตุผลการตัดสินใจเมื่อเกิด incident ทีหลัง

---

จบ manual v5.6 สำหรับ `/smartspec_release_readiness` หากมีการเพิ่มฟีเจอร์ใหม่ใน workflow (เช่น รองรับ artifact ใหม่ หรือเปลี่ยนเกณฑ์ strict) ควรออก manual v5.7 แยก โดยยังอ้างอิง workflow patch 5.6.x/5.7.x ให้ชัดเจนไม่สับสน
