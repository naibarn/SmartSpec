| manual_name | manual_version | compatible_workflow | compatible_workflow_versions | role |
| --- | --- | --- | --- | --- |
| /smartspec_ui_validation Manual (TH) | 5.6 | /smartspec_ui_validation | 5.6.2 – 5.6.x | user/operator manual (frontend, QA, UX, release, platform) |

# /smartspec_ui_validation คู่มือการใช้งาน (v5.6, ภาษาไทย)


## 1. ภาพรวม (Overview)

คู่มือนี้อธิบายวิธีใช้งาน workflow:

> `/smartspec_ui_validation v5.6.x` (เช่น 5.6.2, 5.6.3, 5.6.4)

workflow นี้เป็น **ชั้น governance ด้าน UI correctness & validation** มีหน้าที่หลักคือ:

- ตรวจว่า UI ที่ implement แล้ว **สอดคล้องกับ spec / UI JSON / UX flow** แค่ไหน
- ประเมินว่า **การทดสอบ UI** ครอบคลุมแค่ไหนในมิติ:
  - behavior / flow (happy path + edge case)
  - error states / input validation
  - accessibility (a11y)
  - visual regression / snapshot
  - i18n / localization
  - cross-environment / cross-device (web/mobile/browser/device)
- สร้าง **UI validation report** ต่อ UI unit (เช่น route/screen/flow) พร้อมสถานะและ
  field `blocking_for_release` เป็นสัญญาณต่อ release readiness
- ตั้งแต่ v5.6.3 ขึ้นไป ยังอ่าน **metadata ของ `ui.json` ที่ AI generate**
  (เช่น origin, review status, design system version, style preset)
  เพื่อช่วยประเมินว่าเราควรเชื่อถือ spec จาก AI แค่ไหนในแต่ละ flow
- ตั้งแต่ v5.6.4 เพิ่มการมอง **หลักฐานด้าน security & dependency**
  (โดยเฉพาะกรณี React/Next.js/RSC, Node/npm) และใช้
  **design system / component registry** เป็นบริบทในการประเมินความเสี่ยง
  (โดยไม่เพิ่ม flag ใหม่ และยังคง NO-WRITE ตามเดิม)

> **สำคัญ:**
> - workflow นี้ **ไม่รัน test**, ไม่เปิด browser/device และไม่แก้โค้ดหรือ config
> - อ่านเฉพาะ **artifacts, test reports, security/dependency reports และ registries**
>   ที่มีอยู่แล้ว แล้วสรุปเป็น governance view

### 1.1 ทำไมต้องใช้ workflow นี้

ถ้าไม่มี governance ด้าน UI validation ที่ชัดเจน มักเกิดปัญหาแบบนี้:

- UI บาง flow ไม่เคยถูกทดสอบเลย แต่ทีมเข้าใจผิดว่ามี test แล้ว
- edge case / error state ไม่ถูกครอบคลุม
- accessibility ถูกปล่อยผ่าน เพราะไม่มีใครรวมผล a11y report มาให้เห็นในภาพเดียว
- visual regression/ snapshot มีแต่ไม่มีใครรู้ว่าครอบคลุม flow ไหนบ้าง
- i18n / locale สำคัญ (เช่น ภาษา EN/TH/JP) ไม่ถูก test ครบทุก flow
- release board เห็นแค่ test summary ใน CI แต่ไม่รู้ mapping กับ spec/UI JSON
- ในระบบที่ `ui.json` ถูก generate โดย AI เป็นหลัก:
  - บาง flow ใช้ spec ที่ AI เขียนแบบยังไม่เคยมีคน review
  - คุณไม่รู้เลยว่า flow ไหนเชื่อถือได้มากน้อยต่างกันอย่างไร
- ในระบบ web สมัยใหม่ (React/Next.js/RSC, Node/npm):
  - มี SCA report, lockfile, security gate อยู่แล้ว แต่ไม่ได้โยงกับ UI flow ที่ critical
  - ใช้ React Server Components หรือ `react-server-dom-*` ในพื้นที่สำคัญ
    โดยไม่มี governance เรื่องเวอร์ชันที่ patch แล้วหรือการป้องกันข้อมูลรั่ว

`/smartspec_ui_validation` ช่วยเชื่อม:

> spec/UI JSON (รวมถึงที่ AI generate) ↔ implementation ↔ test & security reports

ให้กลายเป็นรายงานเดียวที่ตอบคำถามว่า

> "ก่อน release รอบนี้ UI ที่ critical ถูก validate ครบในระดับที่องค์กรยอมรับหรือยัง?"
> และ  
> "เรากำลังฝากชีวิตไว้กับ `ui.json` ที่ AI เขียน + dependency/surface เสี่ยง
> ที่ยังไม่มีหลักฐาน security ครบกี่จุด?"

### 1.2 ข้อดีของการใช้

- ทำให้ **frontend, QA, UX, security, release** คุยกันบนภาษากลางชุดเดียว
- เห็น **coverage และ gap ต่อ UI unit** อย่างเป็นระบบ
- เห็นชัดด้วยว่าในแต่ละ flow:
  - spec/UI JSON มาจาก AI หรือคน
  - ผ่าน review แล้วหรือยัง
  - คุณภาพโครงสร้าง `ui.json` อยู่ระดับไหน
  - มีหลักฐาน security/dependency รองรับ stack เว็บหรือไม่
- ช่วยให้ release board ตัดสินใจได้ว่า:
  - flow ไหนพร้อม
  - flow ไหนต้องเพิ่ม test / security ก่อน
  - case ไหนสามารถ accept risk ได้พร้อมเหตุผล
- กลายเป็น **artifact สำหรับ audit** ว่า UI สำคัญถูก review ทั้งในแง่ validation
  และ security evidence ก่อนปล่อยจริง

### 1.3 ความเสี่ยงหากไม่ใช้ (หรือไม่มี layer นี้)

- ปล่อย UI critical (เช่น login/checkout/consent) โดยไม่มี test ครบ → prod incident ด้าน UX
- ปล่อย accessibility issue ที่ควร blocking → เสี่ยงเรื่อง compliance / usability
- ปล่อย i18n bug กินเวลาทีหลัง เพราะไม่มีใครเห็นว่า locale ไหนไม่มี coverage
- ปล่อยให้ `ui.json` ที่ AI generate แบบไม่เคยถูก review เป็น source of truth โดยไม่มีใครรู้ว่า flow ไหนเสี่ยง
- ไม่มีเอกสารแสดงว่าหน้าไหนผ่าน/ไม่ผ่าน validation → ตอบคำถาม management และ auditor ยาก
- สำหรับ stack React/Next.js/RSC:
  - ใช้ dependency ที่มีช่องโหว่หรือเวอร์ชันล้าหลังใน flow critical
  - ไม่มี SCA/lockfile/tool-version-registry รองรับ
  - ใช้ RSC/`react-server-dom-*` โดยไม่มีหลักฐานว่ามีการตรวจ data leakage หรือ CVE ที่เกี่ยวข้อง

---

## 2. What’s New in v5.6

### 2.1 Status model ต่อ UI unit ที่ชัดเจน

เพิ่ม field ต่อ UI unit เช่น:

- `criticality = CRITICAL | HIGH | MEDIUM | LOW | UNKNOWN`
- `spec_coverage_status = FULL | PARTIAL | NONE | UNKNOWN`
- `behavior_validation_status = STRONG | BASIC | NONE | UNKNOWN`
- `error_state_coverage_status = COMPREHENSIVE | PARTIAL | NONE | UNKNOWN`
- `input_validation_coverage_status = COMPREHENSIVE | PARTIAL | NONE | UNKNOWN`
- `accessibility_status = GOOD | ISSUES_NON_BLOCKING | ISSUES_BLOCKING | UNKNOWN`
- `visual_regression_status = COVERED | PARTIAL | NONE | UNKNOWN`
- `i18n_status = COVERED | PARTIAL | NONE | UNKNOWN`
- `cross_env_status = COVERED | PARTIAL | NONE | UNKNOWN`
- `risk_level = LOW | MEDIUM | HIGH | CRITICAL`
- `blocking_for_release = true | false`

### 2.2 กติกา strict-mode ที่ formal

`--safety-mode=strict` จะเข้มสำหรับ `criticality in {CRITICAL, HIGH}` เช่น:

- ถ้าไม่มี/ไม่ชัดทั้ง spec coverage หรือ behavior validation → blocking
- ถ้า a11y มี `ISSUES_BLOCKING` → blocking
- ถ้า visual regression / i18n ไม่มี coverage ใน flow ที่จำเป็น → โดยทั่วไป blocking
- ถ้า cross_env coverage ไม่ครบตาม `--target-envs/browsers/devices` ที่ต้องมี → มีผลต่อ blocking

### 2.3 การ derive criticality

- ใช้ข้อมูลจาก registry / spec / UI JSON ที่ mark ว่า flow/screen นี้ critical
- มี flag `--ui-critical-targets` สำหรับ override เพิ่มเติม
- ถ้าไม่มีข้อมูลเลย → default criticality เป็น MEDIUM/LOW พร้อม note ว่าไม่แน่ชัด

### 2.4 ความสัมพันธ์กับ release readiness

- report นี้สร้าง `blocking_for_release` เป็น **สัญญาณเพิ่ม** สำหรับ
  `/smartspec_release_readiness` และ workflow governance อื่น ๆ
- ไม่ override การตัดสินใจของ workflow อื่น แต่ควรถูกอ่านและตอบสนองอย่างเป็นทางการ

### 2.5 สัญญาณจาก AI-generated `ui.json` (เพิ่มใน v5.6.3)

ตั้งแต่ v5.6.3 ขึ้นไป รายงานจะเพิ่ม field สำหรับอ่านคุณภาพและความน่าเชื่อถือของ
`ui.json` โดยเฉพาะเคสที่ AI generate ได้แก่:

- `ui_spec_origin = AI | HUMAN | MIXED | UNKNOWN`
  - ใช้บอกว่า spec/UI JSON มาจาก AI, คน หรือผสม
- `ui_spec_review_status = UNREVIEWED | DESIGNER_APPROVED | OVERRIDDEN | UNKNOWN`
  - ใช้จาก `meta.review_status` เพื่อรู้ว่า spec ผ่านสายตา designer/ทีม UX หรือยัง
- `ui_json_quality_status = STRONG | OK | WEAK | BROKEN | UNKNOWN`
  - สรุปคุณภาพโครงสร้าง `ui.json` เช่น ครบ flow/states ไหม สอดคล้องกับ spec แค่ไหน

พร้อมทั้งมี flag เพิ่มเติม:

- `--ui-json-ai-strict`
  - เปิดโหมดเข้มสำหรับ UI ที่ `ui.json` มาจาก AI โดยเฉพาะ
  - ถ้า flow นั้น critical/high และยัง `UNREVIEWED` หรือ `ui_json_quality_status` ต่ำ
    → risk จะถูกดันขึ้น และมีโอกาสเป็น `blocking_for_release` ใน strict mode

### 2.6 v5.6.4: Security & design-system clarifications

v5.6.4 **ไม่ได้เพิ่ม flag ใหม่** หรือเปลี่ยน semantics เดิม แต่เพิ่มคำอธิบายด้าน
governance เพื่อให้ workflow:

- อ่าน **หลักฐานด้าน security & dependency** สำหรับ stack เว็บที่เกี่ยวกับ UI
  (React/Next.js/RSC, Node/npm) เช่น SCA report, `tool-version-registry.json`,
  CI security gate summaries, lockfile snapshot แล้วสะท้อนผลใน `risk_level` และ
  `blocking_for_release` โดยเฉพาะ unit ที่ CRITICAL/HIGH และอยู่ใน strict mode
- treat การใช้ RSC / `react-server-dom-*` เป็น surface ที่ **ต้องระวังเป็นพิเศษ**
  ต้องมีหลักฐานว่าใช้เวอร์ชันที่ patch แล้ว และผ่านการ review เรื่อง data leakage
  ก่อนจะมองว่า flow critical นั้นปลอดภัยพอ
- ใช้ **design system / component registry** เป็นบริบทในการประเมิน เช่น:
  - flow สำคัญควรใช้ `AppButton`/`AppCard` ฯลฯ แทนการเรียก component จาก library ตรง ๆ
  - loading/empty/error states ที่ design system ระบุว่าต้องมี ก็ควรถูก test ด้วย

การเปลี่ยนแปลงนี้เป็นแบบ **additive** และ backward compatible กับ v5.6.2–5.6.3

---

## 3. Backward Compatibility Notes

- manual v5.6 นี้รองรับ `/smartspec_ui_validation` ตั้งแต่ **v5.6.2 เป็นต้นไป**
  รวมถึง **v5.6.4**
- `--strict` ยังคงเป็น alias ของ `--safety-mode=strict`
- v5.6.3 เพิ่ม flag `--ui-json-ai-strict` และสัญญาณใหม่จาก AI-generated `ui.json`
  ในลักษณะ additive (ไม่ทับ semantics เดิม)
- v5.6.4 เพิ่มคำอธิบายด้าน **security/dependency** และ **design system**
  โดยไม่แตะ flag และ NO-WRITE

---

## 4. Core Concepts

### 4.1 UI unit คืออะไร

โดยทั่วไปคือหนึ่งในต่อไปนี้:

- route (เช่น `/checkout`, `/login`)
- screen/page (เช่น "Profile Screen")
- flow (เช่น "Checkout Flow", "Password Reset Flow")

แต่ละ unit จะถูกประเมินด้วย status model ด้านบน

### 4.2 Criticality

ระดับความสำคัญของ UI unit เช่น:

- CRITICAL
  - login, checkout, consent, payment, account recovery
  - flow ที่มีผลต่อ legal/compliance สูง
- HIGH
  - ส่วนที่กระทบ conversion, revenue, หรือ core UX
- MEDIUM / LOW
  - ส่วนที่สำคัญรองลงมา

criticality ถูก derive จาก:

- registry กลาง (เช่น `.spec/registry/*` ที่บอก critical flows)
- tag ใน spec/UI JSON
- flag `--ui-critical-targets`

### 4.3 Signals จาก AI-generated `ui.json`

สำหรับระบบที่ใช้ AI generate `ui.json` เป็นหลัก แต่ละ unit จะมีสัญญาณเพิ่ม:

- `ui_spec_origin` → แหล่งที่มาของ spec
- `ui_spec_review_status` → ผ่าน review หรือยัง
- `ui_json_quality_status` → ประสิทธิภาพโครงสร้าง `ui.json`

สิ่งเหล่านี้จะถูกใช้ร่วมกับ status อื่น ๆ ในการคำนวณ `risk_level` และ
`blocking_for_release` โดยเฉพาะใน strict mode และเมื่อเปิด `--ui-json-ai-strict`

### 4.4 Governance-only

workflow นี้ไม่ทำสิ่งต่อไปนี้:

- ไม่รัน cypress/playwright/jest/อื่น ๆ
- ไม่สร้าง/แก้ test file
- ไม่ emit คำสั่ง test runner แบบพร้อมรัน แล้วถือว่า "approved"

ทำหน้าที่เพียงอ่าน spec/UI JSON + test & security reports
แล้วสรุป governance

---

## 5. Quick Start Examples

### 5.1 ตรวจ UI validation สำหรับ checkout flow (web)

```bash
smartspec_ui_validation \
  --spec-ids=checkout_service \
  --run-label=checkout-ui-pre-release \
  --ui-spec-paths=".spec/ui/**/*.json" \
  --ui-test-report-paths=".reports/ui/e2e/**/*.json" \
  --ui-snapshot-report-paths=".reports/ui/snapshot/**/*.json" \
  --ui-accessibility-report-paths=".reports/ui/a11y/**/*.json" \
  --ui-i18n-report-paths=".reports/ui/i18n/**/*.json" \
  --target-envs=web \
  --target-browsers=chromium,firefox \
  --report-format=md \
  --stdout-summary
```

### 5.2 ใช้ strict mode กับ login + consent flow และเข้มกับ AI UI JSON

```bash
smartspec_ui_validation \
  --spec-ids=identity_service \
  --run-label=login-consent-ui-strict \
  --ui-critical-targets=login,consent_flow \
  --ui-spec-paths=".spec/ui/**/*.json" \
  --ui-test-report-paths=".reports/ui/e2e/**/*.json" \
  --ui-accessibility-report-paths=".reports/ui/a11y/**/*.json" \
  --target-envs=web \
  --target-browsers=chromium,firefox,safari \
  --safety-mode=strict \
  --ui-json-ai-strict \
  --report-format=json \
  --stdout-summary
```

### 5.3 โปรเจกต์ที่ไม่ใช้ UI JSON (inline UI)

```bash
smartspec_ui_validation \
  --spec-ids=legacy_portal \
  --run-label=legacy-portal-ui-validation \
  --ui-json-mode=disabled \
  --ui-spec-paths="specs/ui/**/*.md" \
  --ui-test-report-paths=".reports/ui/e2e/**/*.json" \
  --report-format=md
```

---

## 6. CLI / Flags Cheat Sheet

- Scope & label
  - `--spec-ids`
  - `--ui-targets`
  - `--ui-critical-targets`
  - `--include-dependencies`
  - `--run-label`
- UI spec & implementation
  - `--ui-spec-paths`
  - `--ui-impl-paths`
  - `--ui-json-mode=auto|required|disabled`
  - `--ui-json-ai-strict` (เพิ่มความเข้มกับ AI-generated `ui.json`)
- Test & report artifacts
  - `--ui-test-report-paths`
  - `--ui-snapshot-report-paths`
  - `--ui-accessibility-report-paths`
  - `--ui-i18n-report-paths`
- Environment & platform
  - `--target-envs`
  - `--target-browsers`
  - `--target-devices`
- Multi-repo & safety
  - `--workspace-roots`
  - `--repos-config`
  - `--registry-dir`, `--registry-roots`
  - `--index`, `--specindex`
  - `--safety-mode=normal|strict` (`--strict`)
- Output & KiloCode
  - `--report-format=md|json`
  - `--report-dir`
  - `--stdout-summary`
  - `--kilocode`, `--nosubtasks`

---

## 7. วิธีอ่าน UI Validation Report

รายงานจะมีโครงประมาณนี้:

1. **Scope overview**
   - spec-ids, envs, browsers, devices ที่เกี่ยวข้อง
   - วันที่, run-label

2. **Per-UI-unit table**
   - ต่อ `unit_id` แสดง field:
     - `criticality`
     - `ui_spec_origin`
     - `ui_spec_review_status`
     - `ui_json_quality_status`
     - `spec_coverage_status`
     - `behavior_validation_status`
     - `error_state_coverage_status`
     - `input_validation_coverage_status`
     - `accessibility_status`
     - `visual_regression_status`
     - `i18n_status`
     - `cross_env_status`
     - `risk_level`
     - `blocking_for_release`
     - `notes`

3. **Gaps & risks**
   - highlight unit ที่ `risk_level=HIGH/CRITICAL` หรือ `blocking_for_release=true`
   - ให้ความสำคัญกับ unit ที่:
     - `ui_spec_origin=AI` และ `ui_spec_review_status=UNREVIEWED`
     - `ui_json_quality_status=WEAK/BROKEN`
     - ไม่มีหรือมีหลักฐาน security/dependency ที่ล้าสมัยสำหรับ UI stack เช่น React/Next.js/RSC

4. **Summary**
   - จำนวน unit ตาม risk level
   - จำนวนที่ blocking vs non-blocking

> หมายเหตุ: ถ้าใช้ `--report-format=json` → โครงสร้าง JSON คือ canonical
> ส่วน `.md` ต้อง mapping field เหมือนกันเพื่อง่ายต่อ tooling

---

## 8. KiloCode Usage Examples

### 8.1 ใช้บน Kilo กับ web+mobile app

```bash
smartspec_ui_validation \
  --spec-ids=mobile_app,web_portal \
  --include-dependencies \
  --run-label=web-mobile-ui-validation \
  --ui-spec-paths=".spec/ui/**/*.json" \
  --ui-test-report-paths=".reports/ui/e2e/**/*.json" \
  --ui-accessibility-report-paths=".reports/ui/a11y/**/*.json" \
  --target-envs=web,ios,android \
  --kilocode \
  --stdout-summary
```

บน Kilo:

- Orchestrator จะแตก subtasks ต่อ spec-id / flow group
- code-mode อ่าน report ทั้งหมดแบบ read-only
- รวมผลเป็น per-unit status + summary

### 8.2 ปิด subtasks ใน scope เล็ก

```bash
smartspec_ui_validation \
  --spec-ids=small_widget_service \
  --run-label=small-widget-ui-validation \
  --ui-spec-paths=".spec/ui/small_widget/*.json" \
  --ui-test-report-paths=".reports/ui/e2e/small_widget/**/*.json" \
  --kilocode \
  --nosubtasks
```

---

## 9. Multi-repo / Multi-registry Examples

### 9.1 Monorepo ที่มีหลาย frontend app

```bash
smartspec_ui_validation \
  --spec-ids=web_portal,admin_portal \
  --run-label=portal-ui-validation \
  --repos-config=.spec/repos.yaml \
  --registry-dir=.spec/registry \
  --ui-spec-paths=".spec/ui/**/*.json" \
  --ui-test-report-paths=".reports/ui/e2e/**/*.json" \
  --report-format=md
```

### 9.2 หลาย repo หลายทีม

```bash
smartspec_ui_validation \
  --spec-ids=teamA_web,teamB_mobile \
  --run-label=web-mobile-crossflow-validation \
  --workspace-roots="../teamA;../teamB" \
  --registry-dir=../platform/.spec/registry \
  --ui-spec-paths="../teamA/.spec/ui/**/*.json;../teamB/.spec/ui/**/*.json" \
  --ui-test-report-paths="../teamA/.reports/ui/e2e/**/*.json;../teamB/.reports/ui/e2e/**/*.json"
```

---

## 10. UI JSON vs Inline UI

### 10.1 JSON-first UI

- โครงสร้างหน้าจอและ flow ถูกนิยามในไฟล์เช่น
  - `.spec/ui/<app>.ui.json` หรือไฟล์ที่คล้ายกัน
- workflow จะ
  - treat UI JSON เป็น **source หลัก**
  - ถ้า `--ui-json-mode=required` แล้ว JSON หาย →
    - ถือเป็น gap ใน `spec_coverage_status` และ `ui_json_quality_status`
  - ถ้าเป็น UI ที่ AI generate แนะนำให้กรอก meta ให้ครบเสมอ
    (source, generator, design_system_version, style_preset,
    review_status)

### 10.2 Inline UI / opt-out

- ไม่มี UI JSON แยก → spec อยู่ใน markdown / docs อื่น
- ใช้ `--ui-json-mode=disabled`
- workflow ยังสามารถสร้าง report ได้จาก spec + test report เช่นเดิม

---

## 11. ข้อดีของการใช้ vs ความเสี่ยงถ้าไม่ใช้

### 11.1 ข้อดีของการใช้

- มองเห็นภาพรวมว่า UI validation ครอบคลุมเท่าไรต่อ flow/screen
- เห็นว่าแต่ละ flow พึ่งพา `ui.json` จาก AI มากน้อยแค่ไหน และผ่าน review หรือยัง
- ช่วยให้ release meeting มีข้อมูลเชิงโครงสร้าง ไม่ใช่แค่ "test pass 95%"
- ทำให้การ prioritize งานเพิ่ม test/a11y/i18n และปรับปรุง dependency/security ง่ายขึ้น

### 11.2 ความเสี่ยงหากไม่ใช้

- ปล่อย flow สำคัญที่ไม่มี test หรือ coverage เพียงพอ
- ปล่อย flow สำคัญที่ `ui.json` ถูก generate โดย AI และยังไม่เคยมีมนุษย์ review
- สร้าง technical debt ด้าน UX และ a11y แบบเงียบ ๆ
- ไม่มีหลักฐานว่าก่อน release มีการ review DPI/UI correctness และ
  security posture จริง

---

## 12. FAQ / Troubleshooting

**Q1: ถ้าเราไม่มี UI test/report เลย workflow จะทำอะไรได้บ้าง?**  
ยังสามารถสรุป status บางส่วนได้ (เช่น `spec_coverage_status`) แต่จะมี
`*_status=UNKNOWN/NONE` จำนวนมาก ถือเป็นสัญญาณว่าควรลงทุนทำ UI test

**Q2: workflow นี้จะแก้ code หรือ generate test ให้เลยไหม?**  
ไม่ใช่หน้าที่ของ workflow นี้ มันแค่ชี้ว่า gap อยู่ตรงไหน ถ้าอยากให้ช่วยร่าง test case
สามารถใช้ prompt อื่น หรือ workflow สำหรับ test generation แยกต่างหาก

**Q3: ต้องใช้ strict mode เสมอไหม?**  
ไม่จำเป็น แต่แนะนำใช้ strict กับ flow ที่ `criticality` สูง (จาก registry/spec)
เช่น login, checkout, payment, consent, identity โดยเฉพาะเมื่อ
`ui.json` ถูก generate โดย AI และยัง `UNREVIEWED`

**Q4: workflow นี้แทนที่เครื่องมือ security หรือ SCA ได้ไหม?**  
ไม่ได้ มันแค่อ่านผล security/dependency ที่มีอยู่แล้ว แล้วนำไปประกอบในภาพรวม
ของแต่ละ UI unit คุณยังต้องใช้ workflow/process ด้าน security โดยเฉพาะควบคู่กัน

---

## 13. Security & Dependency Notes (Web/React/Next.js/RSC)

สรุปวิธีที่ `/smartspec_ui_validation` เชื่อมกับเรื่อง security และ dependency
สำหรับ web stack สมัยใหม่ (ตามที่อัปเดตใน v5.6.4):

- workflow **ไม่รัน** เครื่องมือ security เอง (ไม่มี `npm audit`, ไม่มี test runner)
  ใช้อ่าน artifacts ที่มีอยู่แล้วเท่านั้น
- เมื่อ UI implementation ใช้ React/Next.js/RSC หรือ stack ใกล้เคียง
  (ดูจาก spec, registry, report):
  - มองว่า **RSC / `react-server-dom-*`** เป็น surface เสี่ยงสูงโดยค่าเริ่มต้น โดยเฉพาะ
    ใน UI unit ที่ CRITICAL/HIGH
  - มองหาหลักฐาน เช่น:
    - SCA/vulnerability report
    - lockfile snapshot / dependency summary
    - CI security gate report
    - `tool-version-registry.json` กลาง สำหรับ React/Next.js/Node
  - ถ้าไม่มีหรือเก่ามาก ใน unit ที่ CRITICAL/HIGH อาจทำให้:
    - ยกระดับ `risk_level`
    - และใน strict mode อาจตั้ง `blocking_for_release=true` พร้อมอธิบายใน `notes`
- workflow แยก **UI correctness** ออกจาก **dependency safety**
  แต่ทำให้คุณเห็นสองอย่างนี้ใน report เดียวกัน

**คำแนะนำ:** รัน workflow นี้คู่กับ pipeline security/SCA ปกติ
เพื่อให้ release board เห็นภาพรวมทั้ง UI validation และ security evidence ต่อ flow

---

## 14. Design-System & Component Registry Notes

v5.6.4 ยังเพิ่มความชัดเจนเรื่องการใช้ design system และ component registry
เป็นบริบทด้าน governance:

- เมื่อมี registry เช่น `design-tokens-registry.json`,
  `ui-component-registry.json`, `app-component-registry.json`,
  `patterns-registry.json` อยู่ใต้ `.spec/registry/`:
  - workflow มองสิ่งเหล่านี้เป็น input ที่บอก **โครงสร้างและ component ที่ควรใช้**
    ไม่ใช่แค่คำแนะนำด้านสไตล์
  - workflow ไม่ตรวจสี/spacing ตรง ๆ (ให้ workflow ด้าน UI consistency ทำ)
    แต่จะ:
    - พิจารณาว่า flow สำคัญใช้ App-level component เช่น `AppButton`, `AppCard`
      ตาม registry หรือยัง
    - ใส่ `notes` หาก CRITICAL/HIGH unit ใช้ component จาก UI library ตรง ๆ
      แทน App component อย่างมีนัยสำคัญ
- ใน flow ที่มี layout/pattern registry ครอบ (เช่น workspace layout, AI run viewer,
  empty/loading/error pattern):
  - ถ้าขาด test สำหรับ state สำคัญตาม pattern
    → ลด `error_state_coverage_status` และดัน `risk_level` ขึ้น

**สรุป:** workflow นี้ใช้ design system และ component registry เป็นส่วนหนึ่งของ
**governance surface** รอบ ๆ UI validation ใช้คู่กับ workflow ด้าน UI consistency
เพื่อให้ทั้ง behavior และ visual language เดินไปด้วยกัน

---

จบคู่มือภาษาไทยสำหรับ `/smartspec_ui_validation v5.6.x` ที่อัปเดตให้สอดคล้องกับ
workflow v5.6.4

