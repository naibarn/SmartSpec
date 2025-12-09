---
manual_name: /smartspec_ui_consistency_audit Manual (TH)
manual_version: 5.6
compatible_workflow: /smartspec_ui_consistency_audit
compatible_workflow_versions: 5.6.2 – 5.6.x
role: user/operator manual (design system, frontend, UX, QA, release, platform)
---

# /smartspec_ui_consistency_audit คู่มือการใช้งาน (v5.6, ภาษาไทย)

## 1. ภาพรวม (Overview)

คู่มือนี้อธิบายวิธีใช้งาน workflow:

> `/smartspec_ui_consistency_audit v5.6.2+`

workflow นี้เป็น **ชั้น governance สำหรับตรวจความสม่ำเสมอของ UI** (UI design & UX consistency) โดยเน้น:

- ตรวจว่า UI ที่ implement แล้ว **ใช้ design system / design tokens / component library อย่างสม่ำเสมอ** หรือไม่
- ดูความ **สอดคล้องของ pattern** ระหว่างหน้าจอ/flow ต่าง ๆ เช่น
  - สี / typography / spacing / radius / shadow
  - การใช้ component เดียวกันในบริบทคล้ายกัน
  - state (hover, focus, disabled, loading)
  - theming (light/dark mode, multi-brand)
- เทียบกับ **design system registry / brand guideline / UI JSON / spec**
- สร้าง **UI consistency audit report** ต่อ UI unit (เช่น route/screen/flow)
  พร้อม field `risk_level` และ `blocking_for_release` สำหรับใช้ใน release governance
- ตั้งแต่ v5.6.2 มีการรองรับ **AI-generated `ui.json`** เต็มรูปแบบ
  - origin (AI / human / mixed)
  - review status
  - design system version / style preset
  - คุณภาพของ `ui.json` (strong/weak/broken)

> **สำคัญ:**
> - workflow นี้เป็น **verification/governance + NO-WRITE**
> - ไม่แก้โค้ด ไม่แก้ CSS/Theme ไม่สร้าง PR หรือ patch ใด ๆ
> - ไม่รัน test / ไม่เปิด browser/device
> - ทำหน้าที่อ่าน artifacts แล้วสรุปความสม่ำเสมอ + ข้อเสี่ยงด้าน design system

### 1.1 ใช้ต่างจาก /smartspec_ui_validation ยังไง

- `/smartspec_ui_consistency_audit`
  - เน้น **design & pattern consistency**
  - เช่น ใช้สี/spacing/token ถูกต้องไหม, มี hard-coded style หรือเปล่า, dark mode พังไหม
- `/smartspec_ui_validation`
  - เน้น **correctness & coverage**
  - เช่น behavior ตรง spec ไหม, test ครอบคลุมไหม, a11y/i18n/visual regression เป็นอย่างไร

ทั้งสองตัวควรใช้ร่วมกัน เพื่อได้ภาพ UI governance ที่ครบทั้ง
**หน้าตา + พฤติกรรม + coverage**

### 1.2 ทำไมต้องใช้ workflow นี้

ถ้าไม่มีชั้น audit ด้าน UI consistency มักเกิดปัญหา:

- design system มี แต่แต่ละทีมใช้ไม่ตรงกัน → UI ดูคนละยุค คนละแบรนด์
- มี design tokens แล้ว แต่โค้ดยัง hard-code สี / spacing เต็มไปหมด
- dark mode หรือ multi-brand theme ไม่สม่ำเสมอ ระหว่างหน้า/flow
- AI generate `ui.json` ไปเรื่อย แต่ไม่มีใครรู้ว่า flow ไหนใช้ preset/version ไหน
- naming ของ component / token ไม่สอดคล้อง → maintenance ยาก และทำให้ AI สร้างของแปลก ๆ ต่อ

`/smartspec_ui_consistency_audit` ช่วยให้คุณได้ภาพรวมว่า

> "UI ของเราในแต่ละ flow/screen ใช้ design system ถูกและทันสมัยแค่ไหน?"  
> "UI ที่ AI ช่วย generate อยู่ในมาตรฐาน design system หรือยัง?"

### 1.3 ความเสี่ยงหากไม่ใช้ (หรือเทียบเท่า)

- มี design system แต่ถูกละเลยแบบเงียบ ๆ → UI แตกเป็นหลาย style
- AI generate UI JSON ที่ไม่ align กับ design system แต่ไม่มีใครรู้
- dark mode/branding มีปัญหาเฉพาะบางหน้า → ดูไม่เป็นมืออาชีพ หรืออ่านไม่ออก
- เวลา redesign หรือเปลี่ยน theme ใหม่ การ refactor UI จะยากและเสี่ยงสูงมาก

---

## 2. What’s New in v5.6

### 2.1 Status model ต่อ UI unit

แต่ละ UI unit (screen/route/flow/component group) จะมี field อย่างน้อย:

- `unit_id`
- `criticality = CRITICAL | HIGH | MEDIUM | LOW | UNKNOWN`
- `ui_spec_origin = AI | HUMAN | MIXED | UNKNOWN`
- `ui_spec_review_status = UNREVIEWED | DESIGNER_APPROVED | OVERRIDDEN | UNKNOWN`
- `ui_json_quality_status = STRONG | OK | WEAK | BROKEN | UNKNOWN`
- `design_system_alignment_status = GOOD | MINOR_DRIFT | MAJOR_DRIFT | UNKNOWN`
- `token_usage_status = CONSISTENT | MIXED | HARD_CODED | UNKNOWN`
- `spacing_consistency_status = CONSISTENT | MINOR_ISSUES | MAJOR_ISSUES | UNKNOWN`
- `typography_consistency_status = CONSISTENT | MINOR_ISSUES | MAJOR_ISSUES | UNKNOWN`
- `component_pattern_consistency_status = CONSISTENT | PARTIAL | FRAGMENTED | UNKNOWN`
- `state_handling_consistency_status = GOOD | MINOR_ISSUES | MAJOR_ISSUES | UNKNOWN`
- `dark_mode_consistency_status = NOT_APPLICABLE | CONSISTENT | PARTIAL | BROKEN | UNKNOWN`
- `naming_consistency_status = GOOD | MINOR_ISSUES | MAJOR_ISSUES | UNKNOWN`
- `risk_level = LOW | MEDIUM | HIGH | CRITICAL`
- `blocking_for_release = true | false`
- `notes`

### 2.2 AI-generated `ui.json` เป็น first-class citizen

ตั้งแต่ v5.6.2:

- อ่าน `meta` จาก `ui.json` เช่น:
  - `source` (ai/human/mixed)
  - `generator`
  - `design_system_version`
  - `style_preset`
  - `review_status`
- แปลงมาเป็น field: `ui_spec_origin`, `ui_spec_review_status`, `ui_json_quality_status`
- สามารถเปิด flag `--ui-json-ai-strict` เพื่อเข้มกับเคส AI generate เป็นพิเศษ

### 2.3 Strict mode ที่คำนึงถึง AI & design system

ใน `--safety-mode=strict` โดยเฉพาะ unit ที่ `criticality in {CRITICAL, HIGH}`:

- ถ้า `design_system_alignment_status=MAJOR_DRIFT` → มีแนวโน้มเป็น blocking
- ถ้า `token_usage_status=HARD_CODED` ในพื้นที่สำคัญ → เสี่ยงสูง
- ถ้า `dark_mode_consistency_status=BROKEN` ในระบบที่ต้องรองรับ dark mode → blocking
- ถ้า `ui_spec_origin=AI` และ `ui_spec_review_status=UNREVIEWED`
  หรือ `ui_json_quality_status=WEAK/BROKEN` → เสี่ยงสูง, อาจเป็น `blocking_for_release`
- ถ้าตรวจพบ business logic ฝังใน `ui.json` (เช่น if/else, role check) ถือเป็น governance issue หนัก

---

## 3. Backward Compatibility Notes

- manual v5.6 นี้รองรับ `/smartspec_ui_consistency_audit` ตั้งแต่ **v5.6.2 เป็นต้นไป** (5.6.x)
- ไม่มีการลบ flag เก่า มีแต่เพิ่ม (`--ui-json-ai-strict` ฯลฯ)
- semantics เรื่อง status model และ strict mode ถูกเพิ่มแบบ additive

---

## 4. Core Concepts

### 4.1 UI unit

อาจหมายถึง:

- route เช่น `/checkout`, `/login`
- screen เช่น "Profile Screen"
- flow เช่น "Checkout Flow", "Onboarding Wizard"
- component group เช่น "Form Controls", "Primary Buttons"

### 4.2 Criticality

ระดับความสำคัญของ UI unit ใช้งานจาก:

- registry กลาง (เช่น `.spec/registry/` บอกว่า flow ไหน critical)
- tag ใน spec / UI JSON
- override ด้วย `--ui-critical-targets` (จาก workflow validation หรือ release chain)

### 4.3 Design system alignment

workflow จะดูว่า UI ใช้ของเหล่านี้ตรงตาม design system หรือไม่:

- สี / spacing / radius / shadow จาก tokens
- typography scale
- component และ pattern (เช่น primary button, card, dialog)
- state (hover, focus, disabled, loading)
- theme (light/dark, multi-brand)

### 4.4 AI-generated `ui.json`

กรณีที่ `ui.json` ถูก generate โดย AI เป็นส่วนใหญ่:

- `ui_spec_origin` = AI
- `ui_spec_review_status` = UNREVIEWED / DESIGNER_APPROVED ตาม meta
- `ui_json_quality_status` จะสะท้อนว่าโครง ui.json นั้นดูดีแค่ไหน

สำหรับ flow สำคัญ (CRITICAL/HIGH) ถ้า `origin=AI + UNREVIEWED` หรือ `quality=WEAK/BROKEN`
→ ถือว่าเป็นสัญญาณเสียงดังมากในรายงาน

---

## 5. Quick Start Examples

### 5.1 Audit consistency ของ web portal + design system

```bash
smartspec_ui_consistency_audit \
  --spec-ids=web_portal \
  --run-label=web-portal-ui-consistency \
  --ui-spec-paths=".spec/ui/**/*.json" \
  --ui-impl-paths="apps/web/src/**/*.{tsx,jsx,vue}" \
  --design-tokens-paths="design-system/tokens/**/*.json" \
  --design-system-doc-paths="design-system/docs/**/*.md" \
  --theme-config-paths="design-system/themes/**/*.json" \
  --target-envs=web \
  --target-brands=default \
  --report-format=md \
  --stdout-summary
```

### 5.2 เข้มเป็นพิเศษกับ AI-generated `ui.json` ของ flow สำคัญ

```bash
smartspec_ui_consistency_audit \
  --spec-ids=checkout_service \
  --run-label=checkout-ui-consistency-ai-strict \
  --ui-spec-paths=".spec/ui/**/*.json" \
  --ui-impl-paths="apps/checkout/src/**/*.{tsx,jsx}" \
  --design-tokens-paths="design-system/tokens/**/*.json" \
  --design-system-doc-paths="design-system/docs/**/*.md" \
  --theme-config-paths="design-system/themes/**/*.json" \
  --target-envs=web \
  --ui-json-ai-strict \
  --safety-mode=strict \
  --report-format=json \
  --stdout-summary
```

### 5.3 โปรเจกต์ legacy ไม่มี UI JSON แยก

```bash
smartspec_ui_consistency_audit \
  --spec-ids=legacy_portal \
  --run-label=legacy-ui-consistency \
  --ui-json-mode=disabled \
  --ui-spec-paths="specs/ui/**/*.md" \
  --ui-impl-paths="src/**/*.tsx" \
  --design-tokens-paths="design-system/tokens/**/*.json" \
  --report-format=md
```

---

## 6. CLI / Flags Cheat Sheet

- Scope & label
  - `--spec-ids`
  - `--ui-targets`
  - `--include-dependencies`
  - `--run-label`
- UI spec & implementation
  - `--ui-spec-paths`
  - `--ui-impl-paths`
  - `--ui-json-mode=auto|required|disabled`
  - `--ui-json-ai-strict`
- Design system & tokens
  - `--design-tokens-paths`
  - `--design-system-doc-paths`
  - `--theme-config-paths`
- Environment & brand
  - `--target-envs`
  - `--target-brands`
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

## 7. วิธีอ่าน UI Consistency Audit Report

รายงานทั่วไปจะมีโครงประมาณนี้:

1. **Scope overview**
   - spec-ids, envs, brands, ฯลฯ
   - run-label, timestamp

2. **Per-UI-unit table**
   - ต่อ `unit_id` จะแสดง field เช่น:
     - `criticality`
     - `ui_spec_origin`
     - `ui_spec_review_status`
     - `ui_json_quality_status`
     - `design_system_alignment_status`
     - `token_usage_status`
     - `spacing_consistency_status`
     - `typography_consistency_status`
     - `component_pattern_consistency_status`
     - `state_handling_consistency_status`
     - `dark_mode_consistency_status`
     - `naming_consistency_status`
     - `risk_level`
     - `blocking_for_release`
     - `notes`

3. **Gaps & risks**
   - เน้น unit ที่:
     - `risk_level=HIGH/CRITICAL`
     - `blocking_for_release=true`
     - `ui_spec_origin=AI` + `ui_spec_review_status=UNREVIEWED`
     - `ui_json_quality_status=WEAK/BROKEN`
     - `design_system_alignment_status=MAJOR_DRIFT`
     - `token_usage_status=HARD_CODED` ในพื้นที่สำคัญ

4. **Summary**
   - จำนวน unit ตาม risk level
   - จำนวน unit ที่ blocking vs non-blocking

ถ้าใช้ `--report-format=json` → JSON เป็น canonical และ `.md` ต้อง map field เดียวกัน
เพื่อให้ tooling อ่านต่อได้ง่าย

---

## 8. KiloCode Usage Examples

### 8.1 ใช้บน Kilo กับหลายแอปพร้อมกัน

```bash
smartspec_ui_consistency_audit \
  --spec-ids=web_portal,admin_portal \
  --include-dependencies \
  --run-label=portal-ui-consistency \
  --ui-spec-paths=".spec/ui/**/*.json" \
  --ui-impl-paths="apps/**/src/**/*.{tsx,jsx}" \
  --design-tokens-paths="design-system/tokens/**/*.json" \
  --design-system-doc-paths="design-system/docs/**/*.md" \
  --kilocode \
  --stdout-summary
```

บน Kilo:

- Orchestrator จะแตก subtasks ต่อ spec-id / กลุ่ม UI
- code-mode อ่านไฟล์ทั้งหมดแบบ read-only
- รวมผลเป็น per-unit status + summary

### 8.2 ปิด subtasks สำหรับ scope เล็ก

```bash
smartspec_ui_consistency_audit \
  --spec-ids=small_widget_service \
  --run-label=small-widget-ui-consistency \
  --ui-spec-paths=".spec/ui/small_widget/*.json" \
  --ui-impl-paths="apps/small_widget/src/**/*.{tsx,jsx}" \
  --kilocode \
  --nosubtasks
```

---

## 9. Multi-repo / Multi-registry Examples

### 9.1 Monorepo ที่มีหลาย frontend app

```bash
smartspec_ui_consistency_audit \
  --spec-ids=web_portal,admin_portal \
  --run-label=portal-ui-consistency \
  --repos-config=.spec/repos.yaml \
  --registry-dir=.spec/registry \
  --ui-spec-paths=".spec/ui/**/*.json" \
  --ui-impl-paths="apps/**/src/**/*.{tsx,jsx}" \
  --report-format=md
```

### 9.2 หลาย repo หลายทีม

```bash
smartspec_ui_consistency_audit \
  --spec-ids=teamA_web,teamB_mobile \
  --run-label=web-mobile-ui-consistency \
  --workspace-roots="../teamA;../teamB" \
  --registry-dir=../platform/.spec/registry \
  --ui-spec-paths="../teamA/.spec/ui/**/*.json;../teamB/.spec/ui/**/*.json" \
  --ui-impl-paths="../teamA/apps/web/src/**/*.{tsx,jsx};../teamB/apps/mobile/src/**/*.{tsx,jsx}" \
  --report-format=json
```

---

## 10. UI JSON vs Inline UI

### 10.1 JSON-first UI

- ใช้ไฟล์อย่าง `.spec/ui/<app>.ui.json` เป็น source-of-truth
- audit จะ treat `ui.json` เป็นแหล่งความจริงหลัก
- ถ้าใช้ `--ui-json-mode=required` แล้วไม่พบ `ui.json` → ถือเป็น gap
- แนะนำให้ `ui.json` จาก AI ใส่ meta ให้ครบ:
  - `source`, `generator`, `design_system_version`, `style_preset`, `review_status`

### 10.2 Inline UI / opt-out

- ถ้าโปรเจกต์ไม่ใช้ `ui.json` แยก
- ใช้ `--ui-json-mode=disabled`
- audit จะอิงจาก markdown spec + design system docs เป็นหลัก

---

## 11. ข้อดีของการใช้ vs ความเสี่ยงถ้าไม่ใช้

### 11.1 ข้อดีของการใช้

- เห็นชัดว่า UI ในระบบใช้ design system ตรงแค่ไหน
- ตรวจได้ว่า AI-generated `ui.json` มีคุณภาพและ alignment แค่ไหน
- ลดโอกาสที่ UI จะดู "หลุดระบบ" หรือย้อนยุคในบางหน้า
- ทำให้การ redesign / เปลี่ยน theme ในอนาคตง่ายขึ้น เพราะ base consistency ดี

### 11.2 ความเสี่ยงถ้าไม่ใช้

- design system เป็นแค่เอกสาร ไม่มีการ monitor การใช้งานจริง
- AI generate UI ที่ไม่สอดคล้องกับแบรนด์ แต่หลุดไปถึง production
- dark mode / multi-brand พังเฉพาะบางหน้า โดยไม่มีใครเห็นภาพรวม
- ขยายระบบ UI ไปเรื่อย ๆ แล้ว refactor ยากมากในอนาคต

---

## 12. FAQ / Troubleshooting

**Q1: ถ้าเรายังไม่มี design tokens/ระบบ design system เต็ม ๆ จะใช้ workflow นี้ได้ไหม?**  
ได้ แต่ value จะลดลงบ้าง โดย audit จะเน้น consistency เชิงโครงสร้าง/ naming มากกว่าเรื่อง tokens รายละเอียด

**Q2: workflow นี้จะช่วย generate design system ใหม่ให้เลยไหม?**  
ไม่ใช่หน้าที่ของ workflow นี้ มันช่วยบอกว่าใช้ของที่มีอยู่ดีแค่ไหน ถ้าต้องการออกแบบ design system ใหม่ ต้องทำผ่าน process/team แยก

**Q3: ควรใช้ร่วมกับ workflow อะไรอีกบ้าง?**  
แนะนำใช้คู่กับ `/smartspec_ui_validation` (ด้าน correctness & coverage) และ `/smartspec_release_readiness` (ด้าน release gate).

---

จบคู่มือภาษาไทยสำหรับ `/smartspec_ui_consistency_audit v5.6.2+`.
หากในอนาคตมีการปรับ status model หรือกติกา strict mode อย่างมีนัยสำคัญ ควรออก manual v5.7 และระบุช่วงเวอร์ชัน workflow ที่รองรับให้ชัดเจน

