| manual_name | manual_version | compatible_workflow | compatible_workflow_versions | role |
| --- | --- | --- | --- | --- |
| /smartspec_ui_validation คู่มือ (TH) | 5.6 | /smartspec_ui_validation | 5.6.2 – 5.6.x | คู่มือผู้ใช้/ผู้ปฏิบัติงาน (frontend, QA, UX, release, platform) |

# /smartspec_ui_validation คู่มือ (v5.6, ภาษาไทย)

## 1. ภาพรวม

คู่มือนี้อธิบายวิธีการใช้งาน workflow:

> `/smartspec_ui_validation v5.6.x` (เช่น 5.6.2, 5.6.3, 5.6.4)

workflow นี้เป็น **ชั้นการกำกับดูแลสำหรับความถูกต้องและการตรวจสอบ UI**  
โดยมุ่งเน้นที่:

- ตรวจสอบว่า UI ที่พัฒนาขึ้น **ตรงกับสเปค / UI JSON / UX flows** หรือไม่  
- ประเมินระดับการ **ตรวจสอบความถูกต้องของ UI** ในด้านต่าง ๆ ได้แก่  
  - พฤติกรรมและ flows (เส้นทางปกติ + กรณีขอบเขต)  
  - สถานะข้อผิดพลาดและการตรวจสอบข้อมูลนำเข้า  
  - การเข้าถึง (a11y)  
  - การทดสอบ visual regression / snapshot  
  - การแปลภาษา (i18n) / การปรับให้เหมาะสมกับท้องถิ่น  
  - การผสมผสานระหว่างสภาพแวดล้อมและอุปกรณ์ต่าง ๆ  
- สร้าง **รายงานการตรวจสอบ UI** ต่อหน่วย UI (route/screen/flow)  
  พร้อมสถานะและสัญญาณ `blocking_for_release`  
- ตั้งแต่ v5.6.3 เป็นต้นไป ยังอ่าน **metadata `ui.json` ที่สร้างโดย AI**  
  (แหล่งที่มา, สถานะการตรวจสอบ, เวอร์ชันระบบออกแบบ, preset สไตล์) เพื่อ  
  ประเมินความน่าเชื่อถือของแต่ละสเปค UI  
- ตั้งแต่ v5.6.4 เป็นต้นไป รวมถึง **หลักฐานความปลอดภัยและการพึ่งพา**  
  (โดยเฉพาะสำหรับ React/Next.js/RSC, Node/npm) และบริบทของ **ระบบออกแบบ &  
  รายการคอมโพเนนต์** ในโมเดลความเสี่ยง (โดยไม่เพิ่ม flags ใหม่หรือเปลี่ยนพฤติกรรม NO-WRITE)

> **หมายเหตุสำคัญ:**  
> - workflow นี้ **ไม่** รันการทดสอบหรือเปิดเบราว์เซอร์/อุปกรณ์  
> - workflow นี้ **ไม่** แก้ไขโค้ด, config หรือไฟล์ทดสอบใด ๆ  
> - workflow นี้อ่านเฉพาะ artifacts ที่มีอยู่ (สเปค, UI JSON, รายงานทดสอบ,  
>   รายงานความปลอดภัย/การพึ่งพา, รายการต่าง ๆ) และสังเคราะห์มุมมองการกำกับดูแล

### 1.1 ทำไมคุณถึงต้องใช้ workflow นี้

หากไม่มีชั้นการกำกับดูแลการตรวจสอบ UI ที่มีโครงสร้าง ทีมงานมักเผชิญกับปัญหา:

- flows สำคัญที่ถูกสมมติว่าทดสอบแล้วแต่จริง ๆ ไม่มีการครอบคลุมจริง  
- ขาดการทดสอบกรณีขอบเขตและสถานะข้อผิดพลาด/การตรวจสอบข้อมูลนำเข้า  
- รายงาน a11y มีอยู่ในระบบ CI แต่ไม่มีการเชื่อมโยงชัดเจนกับ flows/screens  
- การทดสอบ visual regression มีแต่ไม่ชัดเจนว่าเกี่ยวข้องกับหน้าจอธุรกิจสำคัญใด  
- ช่องว่าง i18n ที่ locale สำคัญไม่ได้รับการตรวจสอบอย่างเหมาะสม  
- บอร์ดปล่อยงานเห็นแค่เปอร์เซ็นต์ "ผ่านการทดสอบ" ใน CI โดยไม่มีการเชื่อมโยงกับสเปค UI หรือ flows  
- ในระบบที่ `ui.json` สร้างโดย AI โดยปริยาย:  
  - บาง flows ใช้สเปคที่เขียนโดย AI ที่ไม่มีมนุษย์ตรวจสอบ  
  - ไม่มีวิธีการที่เป็นโครงสร้างเพื่อดูว่า flows ไหนพึ่งพาสเปค AI ที่ยังไม่ผ่านการตรวจสอบมากที่สุด  
- ในสแต็คเว็บสมัยใหม่ (React/Next.js/RSC) ที่มีการเปลี่ยนแปลง dependencies อย่างรวดเร็ว:  
  - รายงานความปลอดภัย/SCA มีอยู่แต่ไม่ได้เชื่อมโยงกับ flows UI สำคัญ  
  - React Server Components หรือ `react-server-dom-*` ถูกใช้โดยไม่มีการกำกับดูแลเรื่องเวอร์ชันแพตช์และความเสี่ยงข้อมูลรั่วไหลที่ชัดเจน

`/smartspec_ui_validation` เชื่อมโยง:

> **สเปค / UI JSON (รวมถึงที่สร้างโดย AI) ↔ การนำไปใช้ ↔ รายงานทดสอบ & ความปลอดภัย**

เข้าเป็นรายงานเดียวที่ตอบคำถาม:

> "ก่อนการปล่อยงานนี้ flows UI สำคัญของเราถูกตรวจสอบความถูกต้องดีแค่ไหน และช่องว่างอยู่ที่ไหน?"  
> และ  
> "เรากำลังพึ่งพา `ui.json` ที่สร้างโดย AI ที่ยังไม่ผ่านการตรวจสอบ หรือขาดหลักฐานความปลอดภัย/การพึ่งพาสำหรับ flows ที่สำคัญจริง ๆ ที่ไหนบ้าง?"

### 1.2 ประโยชน์ของการใช้งาน

- สร้าง **ภาษากลางร่วมกัน** สำหรับทีม frontend, QA, UX, ความปลอดภัย และการปล่อยงาน  
- แสดง **สถานะการตรวจสอบความถูกต้องต่อหน่วย UI** ในรูปแบบที่มีโครงสร้าง  
- ชัดเจนต่อ flow ว่า:  
  - สเปค/UI JSON มาจาก AI หรือมนุษย์  
  - สเปคได้รับการตรวจสอบหรือไม่  
  - โครงสร้าง `ui.json` ดูแข็งแรงหรืออ่อนแอ  
  - มีหลักฐานความปลอดภัย/การพึ่งพาสำหรับสแต็คเว็บ UI หรือไม่  
- ช่วยให้บอร์ดปล่อยงานตัดสินใจ:  
  - flows ไหนพร้อมปล่อย  
  - flows ไหนต้องการทดสอบเพิ่มเติมหรือทำงานด้านความปลอดภัย  
  - จุดไหนยอมรับความเสี่ยงพร้อมเหตุผลชัดเจน  
- สร้าง **หลักฐานตรวจสอบ (audit artifact)** ที่แสดงว่าการตรวจสอบ UI (รวมถึงความน่าเชื่อถือของสเปค AI, a11y, i18n และหลักฐานความปลอดภัย) ถูกตรวจสอบก่อนปล่อยงาน

### 1.3 ความเสี่ยงหากไม่ใช้ (หรือไม่มีการกำกับดูแลเทียบเท่า)

- ปล่อย flows สำคัญ (login/checkout/consent) โดยไม่มีการครอบคลุมการทดสอบจริง  
- ปล่อยปัญหาการเข้าถึงที่ขัดขวางโดยไม่รู้ตัว  
- พบข้อผิดพลาด i18n ช้าใน production เพราะ locale ไม่ได้รับการตรวจสอบอย่างเป็นระบบ  
- พึ่งพา `ui.json` ที่สร้างโดย AI เป็นแหล่งข้อมูลหลักโดยไม่มีความชัดเจนว่า flows ไหนยังไม่ผ่านการตรวจสอบ  
- ไม่มีหลักฐานชัดเจนว่า flows หรือหน้าจอใดผ่านการตรวจสอบ ทำให้การสื่อสารกับผู้บริหาร/ผู้ตรวจสอบยากขึ้น  
- สำหรับสแต็ค React/Next.js/RSC ปล่อย flows สำคัญโดย:  
  - ใช้ dependencies ที่ล้าสมัยหรือมีช่องโหว่  
  - ขาดหลักฐาน SCA/lockfile/registry ที่ชัดเจน  
  - หรือใช้ RSC/`react-server-dom-*` ที่ยังไม่ผ่านการตรวจสอบใน UI ที่มีความสำคัญสูง

---

## 2. อะไรใหม่ใน v5.6

### 2.1 โมเดลสถานะต่อหน่วย UI

แต่ละหน่วย UI มีโมเดลสถานะที่สอดคล้องกัน รวมถึง:

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

### 2.2 กฎโหมดเข้มงวดที่ชัดเจน

ใน `--safety-mode=strict`:

- สำหรับหน่วยที่มี `criticality` เป็น {CRITICAL, HIGH}:  
  - หากขาดหรือไม่ทราบสถานะการตรวจสอบพฤติกรรมหรือการครอบคลุมสเปค → บล็อกการปล่อย  
  - หาก `accessibility_status=ISSUES_BLOCKING` → บล็อกการปล่อย  
  - หาก `visual_regression_status=NONE/UNKNOWN` สำหรับหน่วยที่สำคัญทางสายตา → โดยปกติจะบล็อก  
  - หาก `i18n_status=NONE/UNKNOWN` สำหรับ locale ที่จำเป็น → โดยปกติจะบล็อก  
  - หาก `cross_env_status=PARTIAL/NONE` ในกรณีที่ต้องใช้หลายสภาพแวดล้อม/อุปกรณ์ → มีผลต่อความเสี่ยงและอาจบล็อก

### 2.3 การกำหนดระดับความสำคัญ (Criticality)

ระดับความสำคัญได้จาก:

- รายการ (เช่น `.spec/registry/*` ที่ระบุ flows สำคัญ)  
- แท็กในสเปค / UI JSON (เช่น `critical: true`, `importance: "high"`)  
- การระบุชัดเจนผ่าน `--ui-critical-targets`

ถ้าไม่มีการกำหนด หน่วยจะตั้งค่าเริ่มต้นเป็น `MEDIUM` หรือ `LOW` พร้อมหมายเหตุว่าความสำคัญไม่แน่นอน

### 2.4 ความสัมพันธ์กับความพร้อมปล่อยงาน

- รายงานจะสร้าง `blocking_for_release` เป็น **สัญญาณการกำกับดูแลเพิ่มเติม** สำหรับ `/smartspec_release_readiness` และ workflow อื่น ๆ  
- ไม่ได้แทนที่ workflow อื่น แต่รายการที่บล็อกควรได้รับการพูดคุยและแก้ไขอย่างชัดเจน (หรือยอมรับความเสี่ยงอย่างเป็นทางการ) โดยผู้ตัดสินใจปล่อยงาน

### 2.5 สัญญาณ `ui.json` ที่สร้างโดย AI (เพิ่มใน v5.6.3)

ตั้งแต่ v5.6.3 เป็นต้นไป แต่ละหน่วย UI ยังมีสัญญาณเกี่ยวกับคุณภาพและความน่าเชื่อถือของ `ui.json` ที่สร้างโดย AI:

- `ui_spec_origin = AI | HUMAN | MIXED | UNKNOWN`  
  - ระบุว่าสเปค/UI JSON ส่วนใหญ่สร้างโดย AI, เขียนโดยมนุษย์ หรือผสมกัน  
- `ui_spec_review_status = UNREVIEWED | DESIGNER_APPROVED | OVERRIDDEN | UNKNOWN`  
  - ได้จาก `meta.review_status` หรือรายชื่อ; แสดงว่าสเปคได้รับการตรวจสอบหรือไม่  
- `ui_json_quality_status = STRONG | OK | WEAK | BROKEN | UNKNOWN`  
  - สรุปความสมบูรณ์และความสอดคล้องของ `ui.json` เทียบกับระบบออกแบบและ flows

เพิ่ม flag ใหม่:

- `--ui-json-ai-strict`  
  - เปิดใช้งานกฎเข้มงวดสำหรับ UI JSON ที่สร้างโดย AI  
  - เมื่อ flow มีความสำคัญ/สูง และ `ui_spec_origin=AI` พร้อม `ui_spec_review_status=UNREVIEWED` หรือ `ui_json_quality_status` ต่ำ จะเพิ่มความเสี่ยงและอาจกลายเป็น `blocking_for_release` ในโหมดเข้มงวด

### 2.6 v5.6.4: ชี้แจงเรื่องความปลอดภัย & ระบบออกแบบ

v5.6.4 **ไม่** เพิ่ม flags ใหม่หรือเปลี่ยนแปลงพฤติกรรม CLI เดิม  
แต่เพิ่มการชี้แจงการกำกับดูแลเพื่อให้ workflow:

- อ่าน **หลักฐานความปลอดภัย & การพึ่งพา** สำหรับสแต็คเว็บ UI (React/Next.js/RSC, Node/npm) เมื่อมี (เช่น รายงาน SCA, `tool-version-registry.json`, สรุปประตูความปลอดภัยใน CI, lockfiles)  
  และสะท้อนหลักฐานที่ขาดหายหรือล้าสมัยใน `risk_level` และ `blocking_for_release` โดยเฉพาะสำหรับหน่วยที่สำคัญ/สูงในโหมดเข้มงวด  
- ถือว่า RSC / `react-server-dom-*` เป็น **พื้นผิวความเสี่ยงสูง** ที่ต้องมีการกำกับดูแลเรื่องแพตช์และความเสี่ยงข้อมูลรั่วไหลก่อนพิจารณาว่า flows สำคัญปลอดภัย  
- ใช้ **ระบบออกแบบ & รายการคอมโพเนนต์** เป็นบริบทมากกว่าการบังคับใช้สไตล์ เช่น:  
  - ให้ความสำคัญกับ `AppButton`/`AppCard` มากกว่าส่วนประกอบไลบรารีดิบใน flows สำคัญ  
  - ตรวจสอบว่ารัฐของเลย์เอาต์/แพทเทิร์นที่จำเป็น (loading/empty/error) ได้รับการตรวจสอบจริง

การเปลี่ยนแปลงทั้งหมดเป็น **แบบเสริม** และเข้ากันได้กับ v5.6.2–v5.6.3 อย่างสมบูรณ์

---

## 3. หมายเหตุความเข้ากันได้ย้อนหลัง

- คู่มือ v5.6 นี้ครอบคลุม `/smartspec_ui_validation` ตั้งแต่  
  **v5.6.2 เป็นต้นไป** รวมถึง **v5.6.4**  
- `--strict` ยังคงเป็นนามแฝงของ `--safety-mode=strict`  
- v5.6.3 เพิ่ม `--ui-json-ai-strict` และสัญญาณ AI (`ui_spec_origin`, `ui_spec_review_status`, `ui_json_quality_status`) ในลักษณะเสริม  
- v5.6.4 เพิ่มการชี้แจงเรื่อง **ความปลอดภัย/การพึ่งพา** และ **ระบบออกแบบ** โดยไม่เปลี่ยน flags หรือการรับประกัน NO-WRITE

---

## 4. แนวคิดหลัก

### 4.1 หน่วย UI คืออะไร?

หน่วย UI โดยทั่วไปคือ:

- route (เช่น `/checkout`, `/login`)  
- หน้าจอ/เพจ (เช่น "Profile Screen")  
- flow ของผู้ใช้ (เช่น "Checkout Flow", "Password Reset Flow")

แต่ละหน่วยจะได้รับบันทึกสถานะโดยใช้ฟิลด์ที่ระบุไว้ข้างต้น

### 4.2 ความสำคัญ (Criticality)

ความสำคัญสะท้อนถึงความสำคัญของหน่วย UI เช่น:

- CRITICAL  
  - login, checkout, payment, consent, กู้คืนบัญชี  
  - flows ที่มีผลกระทบทางกฎหมายหรือกฎระเบียบเข้มงวด  
- HIGH  
  - flows ที่มีผลกระทบต่อการแปลงหรือธุรกิจสูง  
- MEDIUM / LOW  
  - flows ที่สำคัญน้อยกว่าแต่ยังเกี่ยวข้อง

ความสำคัญได้จาก:

- รายการ (critical flows, SLOs)  
- แท็กในสเปค / UI JSON  
- การระบุชัดเจนผ่าน `--ui-critical-targets`

### 4.3 สัญญาณจาก `ui.json` ที่สร้างโดย AI

สำหรับระบบที่ AI สร้าง `ui.json` โดยปริยาย แต่ละหน่วย UI ยังมี:

- `ui_spec_origin` → แหล่งที่มาของสเปค (AI vs มนุษย์ vs ผสม)  
- `ui_spec_review_status` → สถานะการตรวจสอบสเปค  
- `ui_json_quality_status` → คุณภาพโครงสร้างของ `ui.json`

สัญญาณเหล่านี้ถูกรวมกับสถานะอื่น ๆ เพื่อคำนวณ `risk_level` และ `blocking_for_release` โดยเฉพาะในโหมดเข้มงวดและเมื่อเปิดใช้ `--ui-json-ai-strict`

### 4.4 ขอบเขตเฉพาะการกำกับดูแล

workflow นี้ **ไม่**:

- รันเครื่องมือเช่น cypress/playwright/jest หรืออื่น ๆ  
- สร้างหรือแก้ไขไฟล์ทดสอบ  
- ออกคำสั่งทดสอบที่พร้อมรันโดยอัตโนมัติ

workflow นี้อ่านเฉพาะสเปค/UI JSON + รายงานทดสอบ & ความปลอดภัย และสร้างสรุปการกำกับดูแล

---

## 5. ตัวอย่างเริ่มต้นอย่างรวดเร็ว

### 5.1 ตรวจสอบ UI หน้า checkout (เว็บ)

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

### 5.2 โหมดเข้มงวดสำหรับ flows login + consent พร้อม AI UI JSON เข้มงวด

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

### 5.3 โครงการ UI แบบ inline (ไม่มี UI JSON)

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

## 6. ตารางสรุป CLI / Flags

- ขอบเขต & ป้ายกำกับ  
  - `--spec-ids`  
  - `--ui-targets`  
  - `--ui-critical-targets`  
  - `--include-dependencies`  
  - `--run-label`  
- สเปค UI & การนำไปใช้  
  - `--ui-spec-paths`  
  - `--ui-impl-paths`  
  - `--ui-json-mode=auto|required|disabled`  
  - `--ui-json-ai-strict` (เข้มงวดกับ `ui.json` ที่สร้างโดย AI)  
- รายงานทดสอบ & artifacts  
  - `--ui-test-report-paths`  
  - `--ui-snapshot-report-paths`  
  - `--ui-accessibility-report-paths`  
  - `--ui-i18n-report-paths`  
- สภาพแวดล้อม & แพลตฟอร์ม  
  - `--target-envs`  
  - `--target-browsers`  
  - `--target-devices`  
- Multi-repo & ความปลอดภัย  
  - `--workspace-roots`  
  - `--repos-config`  
  - `--registry-dir`, `--registry-roots`  
  - `--index`, `--specindex`  
  - `--safety-mode=normal|strict` (`--strict`)  
- ผลลัพธ์ & KiloCode  
  - `--report-format=md|json`  
  - `--report-dir`  
  - `--stdout-summary`  
  - `--kilocode`, `--nosubtasks`

---

## 7. การอ่านรายงานการตรวจสอบ UI

โครงสร้างทั่วไป:

1. **ภาพรวมขอบเขต**  
   - spec-ids, สภาพแวดล้อม, เบราว์เซอร์, อุปกรณ์  
   - วันที่, ป้ายกำกับการรัน

2. **ตารางสถานะต่อหน่วย UI**  
   - สำหรับแต่ละ `unit_id`:  
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

3. **ช่องว่าง & ความเสี่ยง**  
   - หน่วยที่เน้นด้วย `risk_level=HIGH/CRITICAL` หรือ `blocking_for_release=true`  
   - ให้ความสนใจพิเศษกับหน่วยที่:  
     - `ui_spec_origin=AI` และ `ui_spec_review_status=UNREVIEWED`  
     - `ui_json_quality_status=WEAK/BROKEN`  
     - ขาดหลักฐานความปลอดภัย/การพึ่งพาสำหรับ UI React/Next.js/RSC

4. **สรุป**  
   - นับจำนวนตามระดับความเสี่ยง  
   - นับจำนวนตามบล็อกกับไม่บล็อก

> หมายเหตุ: เมื่อ `--report-format=json` โครงสร้าง JSON เป็นแบบมาตรฐาน  
> รายงาน markdown ควรสะท้อนฟิลด์เดียวกันเพื่อรองรับเครื่องมือ

---

## 8. ตัวอย่างการใช้งาน KiloCode

### 8.1 Kilo สำหรับเว็บ + แอปมือถือ

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

- Orchestrator จะแยกงานตาม spec-id/กลุ่ม flow  
- โหมด Code อ่านรายงานแบบอ่านอย่างเดียว  
- ผลลัพธ์ถูกรวมต่อหน่วยในรายงานสุดท้าย

### 8.2 ปิด subtasks สำหรับขอบเขตเล็ก

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

## 9. ตัวอย่าง Multi-repo / Multi-registry

### 9.1 Monorepo ที่มีหลายแอป frontend

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

### 9.2 Multi-repo, หลายทีม

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

## 10. UI JSON กับ Inline UI

### 10.1 JSON-first UI

- หน้าจอ/flows ถูกกำหนดในไฟล์เช่น:  
  - `.spec/ui/<app>.ui.json` หรือไฟล์ที่คล้ายกัน  
- workflow ถือว่า UI JSON เป็น **แหล่งข้อมูลหลัก**  
- เมื่อใช้ `--ui-json-mode=required` แล้ว UI JSON หายไป:  
  - ถือเป็นช่องว่างการตรวจสอบสำหรับ `spec_coverage_status` และ `ui_json_quality_status`  
- สำหรับ UI JSON ที่สร้างโดย AI แนะนำให้เติมฟิลด์ meta เสมอ เช่น:  
  - `source`, `generator`, `design_system_version`, `style_preset`, `review_status`

### 10.2 Inline UI / เลือกไม่ใช้

- ไม่มี UI JSON แยกต่างหาก; สเปคอยู่ใน markdown/docs  
- ใช้ `--ui-json-mode=disabled`  
- workflow ยังสร้างรายงานจากสเปค + รายงานทดสอบ

---

## 11. ประโยชน์และความเสี่ยงของการไม่ใช้

### 11.1 ประโยชน์ของการใช้

- เห็นภาพชัดเจนว่า UI ถูกตรวจสอบความถูกต้องอย่างละเอียดแค่ไหนต่อ flow/หน้าจอ  
- ชัดเจนว่าแต่ละ flow พึ่งพา `ui.json` ที่สร้างโดย AI มากน้อยแค่ไหน และผ่านการตรวจสอบหรือไม่  
- ช่วยให้การประชุมปล่อยงานดีขึ้น: ไม่ใช่แค่ "ผ่านการทดสอบ X%" แต่เป็น "flows สำคัญครอบคลุมระดับ Y พร้อมคุณภาพ AI UI JSON Z และหลักฐานความปลอดภัย E"  
- ช่วยจัดลำดับความสำคัญงานทดสอบ, a11y, i18n และการปรับปรุงความปลอดภัย/การพึ่งพาได้ง่ายขึ้น

### 11.2 ความเสี่ยงหากไม่ใช้

- ปล่อย flows สำคัญที่มีการตรวจสอบไม่ดีหรือไม่ทราบ  
- ปล่อย flows ที่ `ui.json` สร้างโดย AI และยัง `UNREVIEWED`  
- สร้างหนี้เทคนิค UX/a11y/i18n แบบเงียบ ๆ  
- ขาดหลักฐานว่าความถูกต้องของ UI และความปลอดภัยได้รับการตรวจสอบก่อนปล่อยงาน

---

## 12. คำถามที่พบบ่อย / การแก้ไขปัญหา

**Q1: ถ้าเรามีการทดสอบ UI หรืิอรายงานแทบไม่มีเลย จะทำอย่างไร?**  
workflow ยังสามารถรันได้แต่จะมาร์กสถานะหลายอย่างเป็น `NONE`/`UNKNOWN`  
ซึ่งเป็นสัญญาณชัดเจนว่าควรลงทุนทำการทดสอบ UI ก่อนปล่อยงานใหญ่ โดยเฉพาะ flows สำคัญ

**Q2: workflow จะแก้ไขโค้ดหรือสร้างเทสให้เราหรือไม่?**  
ไม่ workflow จะแจ้งแค่ช่องว่างการตรวจสอบ คุณสามารถใช้ prompt/รูปแบบ workflow อื่นเพื่อสร้างเทสได้

**Q3: ควรใช้โหมดเข้มงวดเสมอหรือไม่?**  
ไม่เสมอไป ใช้ `strict` กับ flows ที่มี `criticality` สูง (login, checkout, payment, consent, identity ฯลฯ) โดยเฉพาะเมื่อ `ui.json` สร้างโดย AI และยัง `UNREVIEWED`

**Q4: workflow นี้แทนที่เครื่องมือความปลอดภัยหรือ SCA ได้ไหม?**  
ไม่ได้ workflow อ่านรายงานความปลอดภัย/การพึ่งพาที่มีอยู่และรวมไว้ในภาพรวมความเสี่ยงของหน่วย UI  
คุณยังต้องมี workflow ความปลอดภัยและ CI gates แยกต่างหาก

---

## 13. หมายเหตุความปลอดภัย & การพึ่งพา (Web/React/Next.js/RSC)

ส่วนนี้สรุปวิธีที่ `/smartspec_ui_validation` ทำงานร่วมกับการกำกับดูแลความปลอดภัยและการพึ่งพาสแต็คเว็บสมัยใหม่ ตามที่ชี้แจงใน v5.6.4

- workflow **ไม่เคยรัน** เครื่องมือความปลอดภัยเอง (ไม่มี `npm audit`, ไม่มีรันเทส)  
  อ่านเฉพาะ artifacts ที่มีอยู่  
- เมื่อ UI ใช้ React/Next.js/RSC หรือสแต็คคล้ายกัน (สังเกตจากสเปค, รายการ หรือรายงาน) workflow จะ:  
  - ถือว่า **RSC / `react-server-dom-*`** เป็นพื้นผิวความเสี่ยงสูงที่ต้องมีฐานแพตช์และตรวจสอบความเสี่ยงข้อมูลรั่วไหลอย่างชัดเจน โดยเฉพาะสำหรับหน่วย CRITICAL/HIGH  
  - มองหาหลักฐานเช่น:  
    - รายงาน SCA/ช่องโหว่  
    - snapshot การพึ่งพา/สรุป lockfile  
    - รายงานประตูความปลอดภัยใน CI  
    - `tool-version-registry.json` กลางสำหรับ React/Next.js/Node  
  - หากหลักฐานเหล่านี้ขาดหายหรือล้าสมัยสำหรับหน่วย UI CRITICAL/HIGH อาจ:  
    - เพิ่ม `risk_level`  
    - ตั้ง `blocking_for_release=true` ในโหมดเข้มงวด (พร้อมคำอธิบายใน `notes`)  
- workflow แยกความถูกต้องของ UI ออกจากความปลอดภัยของ dependencies แต่แสดงทั้งสองอย่างในรายงานต่อหน่วยเดียวกัน

**แนวทางปฏิบัติที่ดีที่สุด:** รัน workflow นี้ควบคู่กับ pipeline ความปลอดภัย/SCA ปกติ เพื่อให้บอร์ดปล่อยงานเห็นภาพรวม: การตรวจสอบ UI + หลักฐานความปลอดภัยตาม flow

---

## 14. หมายเหตุระบบออกแบบ & รายการคอมโพเนนต์

v5.6.4 ชี้แจงเพิ่มเติมว่า workflow ใช้ระบบออกแบบและรายการคอมโพเนนต์เป็นบริบทการกำกับดูแลอย่างไร:

- เมื่อมีรายการเช่น `design-tokens-registry.json`, `ui-component-registry.json`, `app-component-registry.json`, หรือ `patterns-registry.json` ใน `.spec/registry/`:  
  - workflow ถือว่าเป็นข้อมูลนำเข้าเพื่ออธิบาย **โครงสร้าง UI และคอมโพเนนต์ที่ตั้งใจใช้** ไม่ใช่แค่คำแนะนำเรื่องสไตล์  
  - workflow **ไม่** ตรวจสอบสี/ระยะห่างโดยตรง (งานนี้เป็นของ workflow ตรวจสอบความสอดคล้อง UI) แต่จะ:  
    - ให้ความสำคัญกับคอมโพเนนต์ระดับแอป (`AppButton`, `AppCard` ฯลฯ) มากกว่าส่วนประกอบไลบรารีดิบใน flows สำคัญ หากรายการระบุการใช้งานนั้น  
    - แจ้งใน `notes` เมื่อหน่วย CRITICAL/HIGH ดูเหมือนพึ่งพาส่วนประกอบไลบรารีดิบมากกว่าห่อหุ้มระดับแอป  
- สำหรับ flows ที่ครอบคลุมโดยรายการเลย์เอาต์/แพทเทิร์น (เช่น เลย์เอาต์ workspace, ตัวดู AI run, สถานะ standardized empty/loading/error):  
  - การขาดการทดสอบสถานะหลักในแพทเทิร์นเหล่านั้นควรลด `error_state_coverage_status` และเพิ่ม `risk_level`

**สรุป:** workflow นี้ถือว่าระบบออกแบบและรายการคอมโพเนนต์เป็นส่วนหนึ่งของ **พื้นผิวการกำกับดูแล** รอบการตรวจสอบ UI  
ใช้ร่วมกับ workflow ความสอดคล้อง UI เพื่อรักษาความสอดคล้องทั้งพฤติกรรมและภาษาภาพ

---

จบคู่มือ `/smartspec_ui_validation v5.6.x` (ภาษาไทย) ปรับปรุงสำหรับ workflow v5.6.4