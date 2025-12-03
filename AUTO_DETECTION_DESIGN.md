# ออกแบบระบบ Auto-Detection สำหรับ Domain และ Modes

## ปัญหาที่ต้องแก้ไข

ปัจจุบัน user ต้องระบุ parameters เอง:
- `--domain=fintech|healthcare|iot|ai|realtime|batch|internal`
- `--di=none|minimal|full|auto`
- `--security=none|basic|stride-basic|stride-full|auto`
- `--performance=none|basic|full|auto`

**ปัญหา:**
- User ไม่รู้ว่าควรเลือก domain/mode ไหน
- อาจเลือกผิดทำให้ SPEC ไม่เหมาะสม
- ต้องมีความรู้เกี่ยวกับแต่ละ domain/mode

**วิธีแก้:**
เพิ่มระบบ auto-detection ที่อ่านบริบทของ SPEC และกำหนด domain/modes ให้อัตโนมัติ

---

## 1. Domain Auto-Detection

### 1.1 Detection Logic

อ่านบริบทจาก:
1. **Title/Name** ของ SPEC
2. **Overview/Purpose** section
3. **Features** list
4. **Keywords** ที่เกี่ยวข้อง

### 1.2 Domain Detection Rules

#### Fintech Domain
**Keywords:**
- payment, billing, invoice, credit, debit, transaction, ledger
- financial, money, currency, wallet, balance, refund
- stripe, paypal, promptpay, banking, accounting
- PCI DSS, compliance, audit trail, immutable log

**Example:**
```
Title: "Payment Processing System"
Features: ["Credit purchase", "Billing cycle", "Invoice generation"]
→ Domain: fintech
```

#### Healthcare Domain
**Keywords:**
- patient, medical, health, hospital, clinic, doctor
- diagnosis, treatment, prescription, appointment
- HIPAA, PHI, medical record, healthcare
- EHR, EMR, telemedicine

**Example:**
```
Title: "Patient Records Management"
Features: ["Medical history", "Prescription tracking"]
→ Domain: healthcare
```

#### IoT Domain
**Keywords:**
- device, sensor, telemetry, gateway, edge
- MQTT, CoAP, firmware, OTA update
- real-time data, streaming, time-series
- embedded, hardware, connectivity

**Example:**
```
Title: "Telemetry Ingestion Service"
Features: ["Device data collection", "Sensor monitoring"]
→ Domain: iot
```

#### AI Domain
**Keywords:**
- model, training, inference, dataset, ML, AI
- neural network, deep learning, prediction
- LLM, GPT, embedding, vector, RAG
- model evaluation, accuracy, F1 score

**Example:**
```
Title: "AI Agent Service"
Features: ["Model inference", "RAG system"]
→ Domain: ai
```

#### Realtime Domain
**Keywords:**
- real-time, streaming, websocket, SSE, pub/sub
- low latency, P99 < 100ms, event-driven
- message queue, kafka, redis stream
- live updates, push notification

**Example:**
```
Title: "Live Chat Service"
Features: ["Real-time messaging", "WebSocket connection"]
→ Domain: realtime
```

#### Batch Domain
**Keywords:**
- batch processing, ETL, data pipeline, cron job
- scheduled task, bulk operation, import/export
- data warehouse, analytics, reporting
- throughput, high volume, parallel processing

**Example:**
```
Title: "Daily Report Generator"
Features: ["Batch data processing", "Scheduled reports"]
→ Domain: batch
```

#### Internal Domain
**Keywords:**
- internal tool, admin panel, dashboard
- prototype, POC, MVP, simple CRUD
- low security, relaxed requirements
- quick development, minimal compliance

**Example:**
```
Title: "Admin Report Tool"
Features: ["Simple data export", "Internal use only"]
→ Domain: internal
```

### 1.3 Multi-Domain Detection

บาง SPEC อาจมีหลาย domain:

```
Title: "Financial AI Recommendation System"
Keywords: ["payment", "credit", "ML model", "prediction"]
→ Primary Domain: fintech
→ Secondary Domain: ai
→ Apply: fintech security + AI-specific requirements
```

---

## 2. DI Mode Auto-Detection

### 2.1 Detection Logic

อ่านบริบทจาก:
1. **Architecture** complexity
2. **Service** count
3. **Dependencies** count
4. **Testing** requirements

### 2.2 DI Mode Rules

#### DI = none
**Conditions:**
- Simple CRUD tool
- Single file/module
- No external services
- Prototype/POC
- Domain: internal

**Example:**
```
Title: "Simple Report Exporter"
Architecture: "Single script"
Domain: internal
→ DI Mode: none
```

#### DI = minimal
**Conditions:**
- 1-3 services
- Basic dependencies (DB only)
- Simple architecture
- Low complexity

**Example:**
```
Title: "User Profile Service"
Services: ["UserService", "Database"]
→ DI Mode: minimal
```

#### DI = full
**Conditions:**
- 4+ services
- Multiple dependencies
- Complex architecture
- Domain: fintech, healthcare (high compliance)
- Testing: comprehensive

**Example:**
```
Title: "Payment Processing System"
Services: ["PaymentService", "BillingService", "CreditService", "AuditService"]
Domain: fintech
→ DI Mode: full
```

---

## 3. Security Mode Auto-Detection

### 3.1 Detection Logic

อ่านบริบทจาก:
1. **Domain** type
2. **Data sensitivity**
3. **Compliance** requirements
4. **External integrations**

### 3.2 Security Mode Rules

#### Security = none
**Conditions:**
- Domain: internal
- No sensitive data
- Prototype/POC
- No external access

**Example:**
```
Title: "Internal Dashboard"
Domain: internal
Data: "Non-sensitive metrics"
→ Security Mode: none
```

#### Security = basic
**Conditions:**
- Standard web service
- Low-medium sensitivity
- Basic authentication
- No compliance requirements

**Example:**
```
Title: "Blog API"
Features: ["User posts", "Comments"]
→ Security Mode: basic
```

#### Security = stride-basic
**Conditions:**
- Medium sensitivity
- User data handling
- Standard compliance
- External API integration

**Example:**
```
Title: "User Management Service"
Features: ["User profiles", "Authentication"]
→ Security Mode: stride-basic
```

#### Security = stride-full
**Conditions:**
- Domain: fintech, healthcare
- High sensitivity (PII, PHI, financial)
- Compliance: PCI DSS, HIPAA
- Critical business impact
- External payment/medical integration

**Example:**
```
Title: "Payment Processing System"
Domain: fintech
Compliance: ["PCI DSS"]
→ Security Mode: stride-full
```

---

## 4. Performance Mode Auto-Detection

### 4.1 Detection Logic

อ่านบริบทจาก:
1. **Domain** type
2. **Expected load**
3. **Latency requirements**
4. **Throughput requirements**

### 4.2 Performance Mode Rules

#### Performance = none
**Conditions:**
- Domain: internal
- Low usage (< 100 users)
- No SLA requirements
- Prototype/POC

**Example:**
```
Title: "Internal Admin Tool"
Domain: internal
Users: "< 50"
→ Performance Mode: none
```

#### Performance = basic
**Conditions:**
- Standard web service
- Medium usage (100-10K users)
- Basic SLA (99% uptime)
- Standard latency (< 1s)

**Example:**
```
Title: "Blog API"
Users: "1000-5000"
→ Performance Mode: basic
```

#### Performance = full
**Conditions:**
- Domain: fintech, realtime, iot
- High usage (> 10K users)
- Strict SLA (99.9%+ uptime)
- Low latency (P99 < 200ms)
- High throughput requirements

**Example:**
```
Title: "Payment Processing System"
Domain: fintech
Users: "> 100K"
SLA: "99.95% uptime"
→ Performance Mode: full
```

---

## 5. Implementation in Workflow

### 5.1 Auto-Detection Process

```markdown
## 1.2 Auto-Detect Domain and Modes (NEW)

If user doesn't specify --domain, --di, --security, or --performance:

### Step 1: Extract Context
- Read SPEC title, overview, features, keywords
- Extract existing SPEC content if editing

### Step 2: Detect Domain
- Apply domain detection rules
- Match keywords against domain patterns
- Determine primary and secondary domains

### Step 3: Detect DI Mode
- Analyze architecture complexity
- Count services and dependencies
- Apply DI mode rules

### Step 4: Detect Security Mode
- Check domain type
- Analyze data sensitivity
- Check compliance requirements
- Apply security mode rules

### Step 5: Detect Performance Mode
- Check domain type
- Analyze expected load
- Check SLA requirements
- Apply performance mode rules

### Step 6: Show Detection Results
```
✅ Auto-detected configuration:
📊 Domain: fintech (detected from: payment, billing, credit keywords)
🔧 DI Mode: full (4+ services detected)
🛡️ Security: stride-full (fintech domain + PCI DSS compliance)
⚡ Performance: full (high-volume financial system)

💡 To override, use:
--domain=healthcare --di=minimal --security=basic --performance=basic
```
```

### 5.2 Override Mechanism

User สามารถ override auto-detection:

```bash
# Auto-detect all
/smartspec_generate_spec.md

# Override domain only
/smartspec_generate_spec.md --domain=healthcare

# Override all
/smartspec_generate_spec.md --domain=iot --di=minimal --security=basic --performance=full
```

### 5.3 Confidence Score

แสดง confidence level ของการ detect:

```
✅ Auto-detected configuration (Confidence: HIGH):
📊 Domain: fintech (95% confidence)
   Matched keywords: payment(3), billing(2), credit(4), invoice(2)

🔧 DI Mode: full (90% confidence)
   Services detected: 4
   Dependencies: 8

🛡️ Security: stride-full (100% confidence)
   Domain: fintech (requires stride-full)
   Compliance: PCI DSS detected

⚡ Performance: full (85% confidence)
   Domain: fintech (high-volume expected)
   Keywords: throughput, SLA, P99
```

---

## 6. Fallback Strategy

### 6.1 Low Confidence Detection

ถ้า confidence < 70%:

```
⚠️ Auto-detection confidence is LOW (65%)
📊 Domain: fintech (65% confidence)

Suggested alternatives:
1. healthcare (45% confidence)
2. ai (30% confidence)

Please confirm or override:
--domain=fintech  (recommended)
--domain=healthcare
--domain=ai
```

### 6.2 Ambiguous Detection

ถ้าตรวจพบหลาย domain ที่ confidence ใกล้เคียงกัน:

```
⚠️ Multiple domains detected:
1. fintech (55% confidence) - payment, billing keywords
2. ai (50% confidence) - model, inference keywords

This appears to be a multi-domain system.
Primary domain: fintech
Secondary domain: ai

Configuration applied:
- Security: stride-full (from fintech)
- Performance: full (from fintech)
- Additional: AI-specific requirements

To change primary domain: --domain=ai
```

---

## 7. Testing Auto-Detection

### Test Cases

#### Test 1: Clear Fintech
```
Input: "Payment Processing System with Stripe integration"
Expected: domain=fintech, di=full, security=stride-full, performance=full
```

#### Test 2: Clear Healthcare
```
Input: "Patient Medical Records Management"
Expected: domain=healthcare, di=full, security=stride-full, performance=basic
```

#### Test 3: Simple Internal Tool
```
Input: "Admin Report Generator"
Expected: domain=internal, di=none, security=none, performance=none
```

#### Test 4: Multi-Domain
```
Input: "Financial AI Recommendation System"
Expected: domain=fintech (primary), ai (secondary), di=full, security=stride-full, performance=full
```

#### Test 5: Ambiguous
```
Input: "Data Processing Service"
Expected: Ask user to clarify (batch vs realtime vs ai)
```

---

## 8. Benefits

1. **User-Friendly:** ไม่ต้องเข้าใจ domain/modes ทั้งหมด
2. **Accurate:** ใช้ context-based detection
3. **Flexible:** สามารถ override ได้
4. **Transparent:** แสดง confidence และเหตุผล
5. **Safe:** Fallback เมื่อไม่แน่ใจ
