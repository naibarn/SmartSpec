---
manual_name: /smartspec_nfr_perf_planner Manual (TH)
manual_version: 5.6
compatible_workflow: /smartspec_nfr_perf_planner
compatible_workflow_versions: 5.6.2 – 5.6.x
role: user/operator manual (SRE, platform, tech leads, performance owners)
---

# /smartspec_nfr_perf_planner คู่มือการใช้งาน (v5.6, ภาษาไทย)

## 1. ภาพรวม (Overview)

คู่มือนี้อธิบายวิธีใช้งาน workflow:

> `/smartspec_nfr_perf_planner v5.6.2`

หน้าที่ของ workflow นี้คือช่วย

> "เปลี่ยน NFR / SLO ที่มีอยู่แล้ว ให้กลายเป็น **performance / load /
> reliability test tasks** ที่ทีมสามารถเอาไปใส่ใน `tasks.md` หรือระบบ
> plan อื่น ๆ ได้อย่างเป็นระบบ"

ลักษณะสำคัญ:

- บทบาท: **design / planning / prompt-generating**
- `write_guard: NO-WRITE`
  - ไม่แก้ `tasks.md`, CI, หรือ code โดยตรง
  - สร้างแค่ **ข้อเสนอ (proposals)** เป็น perf plan
- ออกแบบมาให้ทำงานคู่กับ:
  - `/smartspec_nfr_perf_verifier` (ตัวตรวจว่า NFR ผ่านจริงไหม)

สั้น ๆ:

- **planner** = สร้าง tasks/perf plan จาก NFR
- **verifier** = ตรวจผลจาก test และ metrics ว่า NFR ผ่านไหม

---

## 2. What’s New in v5.6

เวอร์ชัน 5.6.2 ของ planner เน้นอุดช่องโหว่ และแยกขอบเขตจาก verifier ชัดเจน:

### 2.1 แยก planner vs verifier ชัดเจน

- planner มีหน้าที่ "เสนอ" tasks, scenarios, plans เท่านั้น
- ไม่ไปตีความผล test (ปล่อยให้ verifier ทำ)
- ไม่พยายามประกาศ NFR ใหม่แบบ official

### 2.2 ป้องกันการเขียนทับ / แก้ไฟล์จริง

- `write_guard: NO-WRITE` ระดับ workflow
- ผลลัพธ์หลักถูกเขียนเป็นไฟล์ **plan** ใต้:
  - `.spec/suggestions/smartspec_nfr_perf_planner/<timestamp>_<plan-label>.{md|json}`
- การนำเนื้อหาไป merge ใน `tasks.md` หรือ CI ต้องทำโดยคนหรือ tooling แยกต่างหาก

### 2.3 เคารพ NFR เดิม ไม่ไปแก้ threshold

- NFR ที่ใช้วางแผนต้องมาจาก:
  - spec / SPEC_INDEX / policy / registry
- ข้อเสนอ NFR ใหม่ → ต้องอยู่ใน section `proposed_nfrs` แบบ non-binding

### 2.4 Multi-repo + shared service safety

- ใช้ `--repos-config` + registry เพื่อรู้ว่า service ไหนเป็นเจ้าของ
- heavy scenario มักเสนอให้รันใน repo เจ้าของ shared service
- repo อื่นจะได้แค่ smoke/light perf ตามความเหมาะสม

### 2.5 safety-mode สำหรับการวางแผน

- `normal`: เสนอได้ทั้ง tasks หลัก + optional / experimental
- `strict`: เน้นครอบคลุม NFR ให้ครบและกันไม่ให้เสนอ scenario ที่
  ขัดกับ policy โดยไม่ติดป้ายเตือน

---

## 3. Backward Compatibility Notes

- Manual v5.6 นี้ใช้กับ `/smartspec_nfr_perf_planner` ตั้งแต่
  **v5.6.2 เป็นต้นไป** (5.6.x)
- ไม่มีการลบ flag หรือ behavior เดิม (workflow นี้เป็นตัวใหม่)
- `--strict` ยังคงเป็น alias ของ `--safety-mode=strict`
- รูปแบบ path / canonical folders สอดคล้องกับ workflow อื่นใน SmartSpec

---

## 4. แนวคิดหลัก (Core Concepts)

### 4.1 NFR → Testable criteria → Tasks

ลำดับการคิดของ planner:

1. อ่าน NFR จาก spec / SPEC_INDEX / policy
2. แปลงเป็น **criteria ที่วัดได้** เช่น:
   - P95 latency <= 300ms ที่โหลด X req/s
   - error rate < 0.1% ภายใต้ traffic ประจำวัน
3. จาก criteria → สร้าง **perf/load tasks** เช่น:
   - สร้าง k6 scenario A สำหรับ path /checkout
   - รัน soak test 2 ชม. ที่ 70% ของ peak traffic

### 4.2 Perf plan vs tasks.md

- perf plan คือไฟล์ข้อเสนอ (proposal)
- `tasks.md` คือความจริงที่ทีม commit แล้ว
- planner จะช่วยลดงาน manual แปลง NFR → task แต่ไม่เขียนลง `tasks.md` ตรง ๆ

### 4.3 ความสัมพันธ์กับ verifier

- planner ต้องออกแบบ tasks ในแบบที่:
  - ถ้า test ถูกสร้างและรันตาม plan →
    `/smartspec_nfr_perf_verifier` สามารถอ่าน report/metrics และ map กลับไปที่ NFR ได้ง่าย

---

## 5. Quick Start (ตัวอย่างคำสั่ง)

### 5.1 วางแผน perf tasks ให้ service เดียว

```bash
smartspec_nfr_perf_planner \
  --spec-ids=checkout_api \
  --plan-label=checkout-perf-plan \
  --nfr-policy-paths=".spec/policies/nfr/*.md" \
  --target-envs=staging,prod \
  --preferred-tools=k6,jmeter \
  --intensity-level=normal \
  --plan-format=md \
  --stdout-summary
```

ผลลัพธ์:

- แผนงานที่: `.spec/suggestions/smartspec_nfr_perf_planner/<timestamp>_checkout-perf-plan.md`
- ระบุ NFR → proposed tasks ต่อ environment

### 5.2 วางแผนแบบ strict สำหรับ core service

```bash
smartspec_nfr_perf_planner \
  --spec-ids=core_payments \
  --plan-label=core-payments-perf \
  --target-envs=staging,prod \
  --safety-mode=strict \
  --preferred-tools=k6 \
  --intensity-level=heavy \
  --stdout-summary
```

ใน strict mode:

- พยายามให้ทุก critical NFR มี tasks อย่างน้อย 1–2 รายการ
- tasks ที่จำเป็นสำหรับ evidence ของ critical NFR จะถูก mark เป็น priority สูง

---

## 6. CLI / Flags Cheat Sheet

### 6.1 Scope & labeling

- `--spec-ids=<id1,id2,...>`
- `--include-dependencies`
- `--plan-label=<string>`

### 6.2 NFR & policy

- `--nfr-policy-paths="..."`

### 6.3 Multi-repo / registry / index / safety

- `--workspace-roots`
- `--repos-config`
- `--registry-dir`
- `--registry-roots`
- `--index`, `--specindex`
- `--safety-mode=normal|strict` (หรือ `--strict`)

### 6.4 Planning options

- `--target-envs="dev,staging,prod"`
- `--preferred-tools="k6,jmeter,locust,gatling"`
- `--intensity-level=<light|normal|heavy>`
- `--max-tasks-per-nfr=<int>`

### 6.5 Output & KiloCode

- `--plan-format=md|json`
- `--plan-dir=.spec/suggestions/smartspec_nfr_perf_planner/`
- `--stdout-summary`
- `--kilocode`, `--nosubtasks`

---

## 7. วิธีอ่าน perf plan

ในไฟล์แผน (md/json) มักประกอบด้วย:

- ราย spec-id และ environment
- NFR → tasks mapping
- รายละเอียดแต่ละ task เช่น:
  - ประเภท: load / stress / soak / spike / chaos_reliability / latency_sampling
  - target env
  - tool hint (จาก `--preferred-tools`)
  - intensity / duration
  - acceptance criteria
  - ความสัมพันธ์กับ existing task (extends / duplicate_of)
  - `required` vs `optional`

ข้อเสนอทั้งหมดเป็น **proposals** — ทีมสามารถเลือกบางส่วนไปรับใช้ได้

---

## 8. KiloCode Usage Examples

### 8.1 ใช้ planner บน Kilo

```bash
smartspec_nfr_perf_planner \
  --spec-ids=checkout_api \
  --plan-label=checkout-perf-plan \
  --target-envs=staging,prod \
  --preferred-tools=k6 \
  --kilocode \
  --stdout-summary
```

บน Kilo:

- Orchestrator จะแตก NFR ทีละตัวออกเป็น candidate scenarios
- Code mode ตรวจ `tasks.md` ปัจจุบันเพื่อเลี่ยง duplication
- Orchestrator รวมเป็น perf plan ชุดเดียว

### 8.2 ปิด subtasks

```bash
smartspec_nfr_perf_planner \
  --spec-ids=small_service \
  --plan-label=small-service-perf \
  --target-envs=staging \
  --kilocode \
  --nosubtasks
```

- ใช้ reasoning เดียวตรง ๆ ไม่แตก subtasks เพิ่ม เหมาะกับ scope เล็ก

---

## 9. Multi-repo / Shared Service Examples

### 9.1 Monorepo หลาย service

```bash
smartspec_nfr_perf_planner \
  --spec-ids=search_api,ranking_service \
  --plan-label=search-stack-perf \
  --target-envs=staging,prod \
  --repos-config=.spec/repos.yaml \
  --registry-dir=.spec/registry \
  --preferred-tools=k6,locust
```

- ใช้ registry + repos-config เพื่อตัดสินว่า scenario ใดควรอยู่ service ไหน
- ลดการสร้าง heavy scenario ซ้ำซ้อนในหลาย repo

### 9.2 Shared service/platform

```bash
smartspec_nfr_perf_planner \
  --spec-ids=platform_auth \
  --plan-label=platform-auth-perf \
  --target-envs=prod \
  --registry-dir=.spec/registry \
  --safety-mode=strict
```

- heavy scenario จะถูกเสนอให้รันใน repo เจ้าของ `platform_auth`
- แนะนำแค่ smoke/light checks ใน consumer services

---

## 10. UI/UX Perf Tasks

หาก spec มี NFR ฝั่ง UI/UX เช่น:

- LCP, TTI, input latency

planner จะ:

- เสนอ tasks เช่น:
  - synthetic journey สำหรับ flow หลัก
  - เก็บ Web Vitals ผ่าน synthetic/real-user monitoring
- เคารพ UI governance จาก SPEC_INDEX/config:
  - ถ้า project ใช้ JSON-first UI → อาจเสนอให้วัดแต่ละ screen/flow ตาม `ui.json`
  - ถ้า opt-out → จะไม่สร้าง task ที่ผูกกับ `ui.json` แต่ยังเสนอ E2E/UX perf ได้

---

## 11. Best Practices & Anti-patterns

### 11.1 Best Practices

- ใช้ planner หลังจาก NFR ชัดเจนแล้ว (ไม่ใช่ตอนที่ NFR ยังลอย ๆ)
- ทบทวน perf plan ร่วมกันในทีม แล้วค่อย merge tasks สำคัญไปที่ `tasks.md`
- ให้ `plan-label` สื่อถึง release/initiative ที่เกี่ยวข้อง
- ใช้ `--safety-mode=strict` สำหรับ service ที่ critical
- เก็บ perf plans ใน version control

### 11.2 Anti-patterns

- คิดว่า planner จะปรับ spec/NFR ให้เอง (จริง ๆ ทำไม่ได้)
- merge ทุก task จาก plan ลง `tasks.md` โดยไม่ review
- ละเลย existing tasks แล้วสร้าง scenario ซ้ำซ้อน

---

## 12. FAQ / Troubleshooting

### Q1: ถ้าไม่มี NFR เลย planner จะทำอะไรได้บ้าง?

- อาจเสนอแค่ `proposed_nfrs` และตัวอย่าง perf tasks ระดับ generic
- ควรกลับไปเติม NFR ที่ spec/policy ก่อน แล้วค่อยรัน planner ใหม่

### Q2: ถ้ามี perf tasks อยู่แล้ว planner จะซ้ำไหม?

- planner พยายามอ่าน `tasks.md` เพื่อลด duplication
- หากจำเป็นต้องมี task เพิ่ม จะ mark ความสัมพันธ์ (extends/refines) แทน duplicate เฉย ๆ

### Q3: จำเป็นต้องใช้ทั้ง planner และ verifier ไหม?

- ไม่บังคับ แต่แนะนำ:
  - planner ช่วยออกแบบ coverage
  - verifier ช่วยตรวจว่าของที่ลงมือทำจริงได้ผลตาม NFR หรือไม่

---

จบคู่มือภาษาไทยสำหรับ `/smartspec_nfr_perf_planner v5.6.2`.
หากต่อไปมีการอัปเวอร์ชันที่เปลี่ยน semantics หรือเพิ่มโหมดสำคัญ
ควรออก manual v5.7 แยกพร้อมบอกช่วงเวอร์ชันที่รองรับให้ชัดเจน

