# Performance Requirements for Financial Transaction System

This document defines the **Performance, Reliability, and Capacity Requirements** for a financial credit, promo, ledger, and orchestration system. It is written as a standalone module that can be included inside any SmartSpec v4-compliant SPEC.

---

## 1. Latency Targets (API Gateway → Core Service)
All latency metrics are measured at the service boundary, including authorization, validation, and orchestration overhead.

### 1.1 SLO Latency Objectives
- **P50**: `< 150 ms`
- **P90**: `< 250 ms`
- **P95**: `< 300 ms`
- **P99**: `< 600 ms`

### 1.2 Notes
- Applies to: credit
deduction, credit purchase, promo redemption, settlement, ledger recording.
- Excludes: third-party gateway latency (reported separately).
- Retry-related delays must be isolated from user-facing latency.

---

## 2. Throughput Capacity
Defines maximum sustainable load and peak traffic load.

### 2.1 Normal Operating Load
- **50–200 TPS** sustained API throughput
- Queue worker processing: **≥ 50 jobs/sec** sustained

### 2.2 Peak Load Scenarios
- Promo events / flash sale: **500–1,000 TPS**
- Bulk ledger settlement: **5,000+ operations/minute**
- Queue worker burst: **≥ 200 jobs/sec**

### 2.3 Required Behaviors
- Service must not degrade batch worker throughput due to API spikes.
- Queue processing shall autoscale horizontally within 30 seconds.

---

## 3. Availability & SLA
These values define the reliability expectations of the financial core service.

### 3.1 Uptime Requirements
- **99.9% monthly uptime** for all credit/ledger/promo services
- **Zero financial data loss** is acceptable under all circumstances

### 3.2 Recovery Objectives
- **RTO** (Recovery Time Objective): `≤ 5 minutes`
- **RPO** (Recovery Point Objective): `0` (ledger must never lose data)

### 3.3 Degraded Mode
Service must support limited functionality during partial outages:
- Read-only balance queries allowed
- Write operations routed to fallback queue or delayed mode
- Promo redemption temporarily disabled if risk of multi-redeem exists

---

## 4. Database Performance Baselines
### 4.1 Query Targets
- Write latency: `< 10 ms`
- Read latency: `< 5 ms`
- Transaction commit latency: `< 20 ms`

### 4.2 Isolation & Integrity
- Transactions must run at **SERIALIZABLE** or equivalent custom pattern (optimistic locking with retries allowed)
- Idempotency keys required for all write paths

### 4.3 Capacity
- Ledger table expected growth: **10M–200M rows** per year
- Must support horizontal partitioning or archival strategy

---

## 5. Queue & Worker Baselines
### 5.1 Queue Delay
- Average queue delay: `< 100 ms`
- P99 queue delay: `< 500 ms`

### 5.2 Retry Logic
- Max retries: **3 attempts**
- On final failure → send to **DLQ** (Dead Letter Queue)
- DLQ threshold: **< 1%** of total messages

### 5.3 Worker Requirements
- Worker cold start: `< 1 second`
- Must support parallel job execution
- Must provide idempotent job execution for all financial operations

---

## 6. Third-Party Gateway Performance (If Applicable)
### 6.1 Allowable External Latency
- Third-party P95 latency: `< 900 ms`
- Third-party P99 latency: `< 2,000 ms`

### 6.2 Circuit Breaker
- Activate when:
  - Error rate > **5%** over rolling 1 minute
  - Latency > **3 seconds** over P99

---

## 7. Load Testing Requirements
### 7.1 Scenarios
- Read-heavy test: 80% GET, 20% POST
- Write-heavy test: 70% POST, 30% GET
- Promo peak test: burst 1,000–2,000 TPS
- Saga orchestration test: 10k concurrent workflows

### 7.2 Pass Criteria
- No financial inconsistency
- No duplicate ledger entries
- No more than 0.01% failed transactions
- P99 latency within defined thresholds

---

## 8. Metrics & Alerting
### 8.1 Required Metrics
- `api_latency_p50`, `api_latency_p95`, `api_latency_p99`
- `queue_delay_p50`, `queue_delay_p99`
- `db_write_latency`, `db_read_latency`
- `worker_success_rate`, `worker_failure_rate`
- `ledger_anomaly_count`

### 8.2 Critical Alerts
- P99 latency > threshold for 5 minutes
- Queue delay > 1 second
- DB commit failures > 0.1%
- DLQ entries > 1%
- Saga compensation rate > expected baseline

---

## 9. Compliance
These performance expectations follow:
- SmartSpec v4.0 Reliability Standards
- Financial Transaction Integrity Guidelines
- Internal Engineering SLAs

---

1️⃣ Performance section (P50/P95/P99, Throughput, SLA ฯลฯ)
จำเป็นต้องมีไหม?

คำตอบ: ขึ้นกับประเภทของระบบ

✅ “ควรมี / เกือบต้องมีแน่นอน” ถ้า SPEC เป็นแบบนี้

ประเภท SPEC ที่ควรมี Performance Requirements แบบละเอียด:

ระบบการเงิน / เครดิต / เลดเจอร์ / Payment / Billing

มีเงินเกี่ยวข้อง

มี Saga, queue, DB write-heavy

ถ้าช้า / เด้ง / duplicate = เสียเงินจริง
→ แบบนี้ควรมี Latency target + Throughput + SLA + Queue/DB baseline ชัด ๆ

Backend service ที่เป็น “platform core”

Auth, session, rate limiting, audit logging, central ledger

ถ้าล่ม = ทุก service อื่นพัง
→ ควรระบุ SLA / latency / error budget

API ที่ต้องรองรับโหลดสูง / event พิเศษ

Flash sale, topup event, mass notification, bulk job
→ ต้องมี throughput + peak scenario, load test plan

ระบบที่มี queue/worker เป็นหัวใจ

Orchestrator, workflow engine, report generator, ETL
→ ต้องมี: queue delay target, DLQ threshold, max retries, worker throughput

กรณีของคุณ
SPEC ที่คุยกันก่อนหน้าเป็น Financial / Credit / Ledger + Orchestrator
แบบนี้ผมจะถือว่า “ควรมี” performance section
ไม่ใช่แค่ nice-to-have แล้ว แต่คือ “ทำให้ spec สมบูรณ์ระดับ production”

🟡 “มีแบบย่อๆ พอ” ได้ ถ้า SPEC เป็นแบบนี้

Internal tools, batch report ที่ไม่ critical เวลาไม่ real-time มาก

ระบบ admin บางอย่างที่ user น้อย, ใช้เฉพาะทีมในบริษัท

Service backend ที่ไม่ได้เป็น critical path และรับโหลดไม่เยอะ

ในเคสนี้อาจเขียนแค่:

“ไม่จำเป็นต้อง optimize latency ระดับมิลลิวินาที”

“รองรับ 10–20 TPS ก็พอ”

“SLA ตามระบบหลัก ไม่ต้องระบุเอง”

❌ “ไม่จำเป็นต้องมี” ได้เลย ถ้า SPEC เป็นแบบนี้

Library ภายใน (utility, helpers, เอาไว้ใช้ในโค้ดอื่น)

Design spec ที่เป็น UI/UX, content, static page

SPEC ที่เป็นแค่ data contract หรือ schema sharing (เช่น JSON schema, protobuf schema)

สำหรับแบบนี้ ไม่ต้องใส่ P50/P95/P99 ก็ได้ จะเยอะเกินไป