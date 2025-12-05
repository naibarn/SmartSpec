---
description: SmartSpec v5.0 - Flexible SPEC generation with profiles, modes, and advanced options for all project types
version: 5.0.0
---

## User Input

```text
$ARGUMENTS
```

**Patterns:**
- NEW: "Create SPEC for payment system..."
- EDIT: `specs/feature/spec-004/spec.md`
- With profile: `--profile=financial`
- With mode: `--mode=compact`
- With flags: `--no-di --security=stride-basic`

---

## 0. Parse Command-Line Flags (NEW v5.0)

### 0.1 Profile Selection

```
--profile=<type>

Options:
  basic           - Minimal SPEC (Overview, Architecture, API/Data)
  backend-service - Standard backend (DI, testing, monitoring)
  financial       - Full security + performance (STRIDE, SLA, metrics)
  full            - All sections (default - v4.0 compatibility)
```

### 0.2 Mode Selection

```
--mode=<type>

Options:
  standard - Full SPEC with all details (default)
  compact  - Condensed 5-section SPEC for simple projects
```

### 0.3 Security Level

```
--security=<level>

Options:
  none         - No security section
  basic        - Basic security considerations
  stride-basic - STRIDE table (5-10 lines, key threats only)
  stride-full  - Complete STRIDE model (100+ lines, detailed)
  auto         - Auto-detect based on profile (default)
```

### 0.4 DI Pattern Control

```
--di=<level>

Options:
  full    - Complete DI pattern documentation (default for backend)
  minimal - Brief DI pattern mention
  none    - No DI pattern section
  auto    - Auto-detect based on project type (default)

Shorthand:
  --no-di  - Same as --di=none
```

### 0.5 Performance Requirements Control

```
--performance=<level>

Options:
  full    - Complete performance requirements
  basic   - Key metrics only (P99, TPS, uptime)
  none    - No performance section
  auto    - Auto-detect based on profile/domain (default)
```

### 0.6 Force Update Critical Sections

```
--force-update=<sections>

Options:
  all                          - Allow update all critical sections
  stride,config,di            - Allow specific sections
  none                        - Preserve all critical sections (default)
```

### 0.7 Output Organization

```
--no-backup        - Don't create backup files
--no-report        - Don't generate reports
--output-dir=<dir> - Custom output directory (default: .smartspec/)
```

### 0.8 Validation

```
--validate-consistency  - Check consistency between sections
--no-validation        - Skip validation checks
```

### 0.9 Domain Hints (NEW)

```
--domain=<type>

Options:
  healthcare - Real-time + privacy critical
  iot        - High throughput, telemetry
  logistics  - High SLA requirements
  ai         - Latency sensitive
  fintech    - Security + performance critical
  saas       - Scalability focused
  internal   - Lower requirements
```

---

## 1. Load SmartSpec Context

Read configuration in priority order:
1. `.smartspec/smartspec.config.json` (if exists - organization-wide)
2. `SPEC_INDEX.json` (if exists - for dependency resolution)
3. Built-in defaults

Parse flags from $ARGUMENTS and merge with config.

### 1.1 Load or Create SPEC_INDEX.json (Enhanced with Auto-Creation)

**Step 1: Check if SPEC_INDEX.json exists**

Check for `SPEC_INDEX.json`:
```bash
test -f SPEC_INDEX.json && echo "EXISTS" || echo "NOT_EXISTS"
```

**Step 2: If NOT exists, create it (Auto-Creation)**

If NOT_EXISTS:
```
1. Create SPEC_INDEX.json with initial structure (in project root):
   {
     "version": "5.0",
     "created": "<current_timestamp>",
     "last_updated": "<current_timestamp>",
     "specs": [],
     "metadata": {
       "total_specs": 0,
       "by_status": {
         "draft": 0,
         "active": 0,
         "deprecated": 0,
         "placeholder": 0
       },
       "by_repo": {},
       "validation": {
         "last_validated": "<current_timestamp>",
         "status": "valid",
         "errors": [],
         "warnings": [],
         "health_score": 100
       }
     }
   }

2. Log: "✅ Created SPEC_INDEX.json in project root"
```

**Step 3: Load SPEC_INDEX.json into memory**

If EXISTS (or just created):
- Read `SPEC_INDEX.json`
- Parse JSON structure
- Store in SPEC_REGISTRY for lookup
- Structure: `{ "specs": [{ "id": "...", "title": "...", "path": "...", "repo": "..." }] }`
- This will be used to resolve spec dependencies with full path and repo information

**Note:** With auto-creation, SPEC_INDEX.json will always exist after this step

---

## 2. Determine SPEC Structure (Profile-Based)

### 2.1 Profile: basic

**Sections:**
1. Header (minimal)
2. Overview (Purpose, Scope, Features)
3. Architecture Summary (high-level only)
4. API Specification OR Data Model (choose one)
5. Acceptance Criteria

**Excludes:**
- When to Use
- Detailed Implementation Guide
- Testing Strategy
- Monitoring
- Security (unless --security specified)
- Performance Requirements
- DI Pattern

**Use Cases:**
- Simple CRUD services
- Internal tools
- Prototypes
- Documentation-first projects

---

### 2.2 Profile: backend-service

**Sections:**
1. Header
2. Technology Stack
3. Dependency Injection Pattern (if --di≠none)
4. Overview
5. When to Use
6. Architecture
7. Implementation Guide (core steps)
8. Testing Requirements
9. Monitoring (basic metrics)
10. Examples

**Includes if detected:**
- Configuration Schema (if config mentioned)
- API Documentation (if REST/GraphQL)
- Database Schema (if DB mentioned)

**Excludes by default:**
- STRIDE Model (add with --security)
- Detailed Performance Requirements (add with --performance)

**Use Cases:**
- Standard microservices
- API services
- Backend workers
- Most backend projects

---

### 2.3 Profile: financial

**Sections (Full Critical System):**
1. Header
2. Technology Stack
3. Dependency Injection Pattern (MANDATORY)
4. Overview
5. When to Use / When NOT to Use
6. Architecture (detailed)
7. **Business Rules & Logic** - Usage limits, stacking rules, expiration behavior (NEW)
8. **Data Model & Schema** - Database schema, ER diagram
9. **API Specification** - Complete endpoint documentation with schemas
10. **External Integration Contracts** - Financial system, payment gateway integration (NEW)
11. **Security Threat Model (STRIDE)** - Full by default
12. **Performance Requirements** - Full metrics
13. **Idempotency Requirements** - Duplicate prevention, retry safety (NEW)
14. **Configuration Schema** - Complete
15. **Environment Configuration** - .env structure, per-environment overrides (NEW)
16. **Operational Requirements** - Deployment, DR, infrastructure (NEW)
17. Implementation Guide
18. Testing Strategy (comprehensive)
19. Monitoring & Observability (detailed)
20. Examples (multiple scenarios)
21. Related Specs

**Automatically includes:**
- ✅ Business Rules & Logic (usage limits, stacking, expiration)
- ✅ Data Model & Schema (tables, ER diagram)
- ✅ API Specification (complete endpoint docs)
- ✅ External Integration Contracts (request/response schemas, retry logic)
- ✅ STRIDE threat model (full)
- ✅ Performance Requirements (P50/P95/P99, TPS, SLA)
- ✅ Idempotency requirements (duplicate prevention, retry safety)
- ✅ Environment Configuration (.env, validation, per-env overrides)
- ✅ Operational Requirements (deployment topology, DR, infra)
- ✅ Audit logging requirements
- ✅ Data integrity checks
- ✅ Compliance notes

**Use Cases:**
- Payment systems
- Credit/billing systems
- Financial transactions
- Any system handling money

---

### 2.4 Profile: full (default)

**All v4.0 sections** - backward compatible

Same as current SmartSpec v4.0 behavior:
- Auto-detect Performance Requirements
- Auto-detect DI Pattern
- Auto-detect Security needs
- Include all optional sections

---

## 3. Mode Handling

### 3.1 Mode: standard (default)

Full detail for each section as per profile.

### 3.2 Mode: compact

**Condense to 5 core sections:**

```markdown
# SPEC-XXX: [Title]

**Status:** DRAFT
**Profile:** [Profile used]
**Mode:** COMPACT

---

## 1. Overview

**Purpose:** [One sentence]
**Scope:** [Key features list]
**Non-Goals:** [What's excluded]

---

## 2. Architecture Summary

**Pattern:** [e.g., REST API + PostgreSQL + Redis]
**Components:** [List major components]
**Data Flow:** [Simple diagram or description]

---

## 3. Technical Specification

### 3.1 API Endpoints (if applicable)

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | /api/v1/... | ... |
| POST | /api/v1/... | ... |

### 3.2 Data Model (if applicable)

**Key Entities:**
- Entity1: [Fields]
- Entity2: [Fields]

---

## 4. Constraints & Risk Notes

**Performance:**
- [Key constraint if applicable]

**Security:**
- [Key risk if applicable]

**Technical Debt:**
- [Known limitations]

---

## 5. Acceptance Tests

- [ ] Functional test 1
- [ ] Functional test 2
- [ ] Integration test
- [ ] Performance acceptable
- [ ] Security baseline met

---
```

**When to use compact mode:**
- Simple projects
- Internal tools
- Rapid prototyping
- When detailed SPEC is overkill

---

## 4. Security Level Handling

### 4.1 security=none

No security section included.

### 4.2 security=basic

```markdown
## Security Considerations

**Authentication:** [Method]
**Authorization:** [Approach]
**Data Protection:** [Encryption, sanitization]
**Key Risks:** [2-3 bullet points]

---
```

### 4.3 security=stride-basic

```markdown
## Security Threat Model (STRIDE-Basic)

| Threat | Risk | Mitigation |
|--------|------|------------|
| **Spoofing** | User impersonation | JWT + MFA |
| **Tampering** | Data modification | TLS + signatures |
| **Information Disclosure** | Data leaks | Encryption + access controls |
| **Denial of Service** | Unavailability | Rate limiting + scaling |

**Implementation:**
- [2-3 key security requirements]

---
```

### 4.4 security=stride-full

Full STRIDE model as in v4.0:
- Complete threat table (6 categories)
- Detailed mitigation strategies
- Implementation requirements
- Testing approach
- Compliance notes

**Enhanced for Fintech/Financial Domain:**

When `--domain=fintech` or `--profile=financial`, include additional security measures:

```markdown
## Security Threat Model (STRIDE-Full)

### Spoofing
- **JWT Validation:** Verify signature, expiration, issuer
- **API Key Rotation:** Automatic rotation every 90 days
- **MFA for Sensitive Operations:** Required for financial transactions > threshold
- **Device Fingerprinting:** Track and verify known devices

### Tampering
- **Ledger Tamper-Proof Design:**
  - Immutable ledger entries (no UPDATE/DELETE)
  - SHA-256 hash chain (blockchain-style)
  - Audit log integrity verification
  - Previous hash linkage for tamper detection
- **Request Signing:** HMAC-SHA256 for API requests
- **HTTPS/TLS Enforcement:** TLS 1.3 minimum
- **Database Constraints:** CHECK constraints prevent invalid states

### Repudiation
- **Comprehensive Audit Trail:**
  - All financial operations logged
  - IP address, user agent, request ID tracking
  - Timestamp with timezone (UTC)
  - Non-repudiation signatures for critical operations
- **Immutable Logs:** Append-only transaction log
- **7-Year Retention:** Compliance requirement

### Information Disclosure
- **Encryption at Rest:** AES-256 for sensitive data
- **Encryption in Transit:** TLS 1.3
- **PII Masking in Logs:** Credit card, SSN, account numbers masked
- **Secure Key Management:** AWS KMS / HashiCorp Vault
- **Data Classification:** PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED

### Denial of Service

**Rate Limiting Strategy:**

*Per-User Limits:*
- Standard users: 100 req/min
- Premium users: 500 req/min
- Admin users: 1000 req/min
- Service accounts: 5000 req/min

*Per-IP Limits:*
- Public endpoints: 1000 req/min
- Auth endpoints: 20 req/min (prevent brute force)
- Registration: 5 req/hour per IP

*Per-Endpoint Limits (Financial System):*
- `GET /api/balance`: 200 req/min per user
- `POST /api/credit/add`: 50 req/min per user
- `POST /api/credit/deduct`: 100 req/min per user
- `POST /api/payment`: 20 req/min per user
- `GET /api/transactions`: 100 req/min per user
- `POST /api/refund`: 10 req/min per user

*Implementation:*
- Technology: Redis for distributed rate limiting
- Algorithm: Sliding window counter
- Response: `429 Too Many Requests` with `Retry-After` header
- Bypass: Admin users can bypass with special header (logged)

*Burst Handling:*
- Allow burst up to 2x limit for 10 seconds
- Then enforce strict limit
- Burst tokens reset every minute

*Rate Limit Headers:*
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1701619200
```
- **Replay Attack Mitigation:**
  - Idempotency key required for mutations
  - Request timestamp validation (max 5 min skew)
  - Nonce-based replay prevention
  - Idempotency key expiration (24 hours)
- **Circuit Breaker Pattern:** Prevent cascade failures
- **Request Timeout:** 30s max
- **Connection Pooling:** Limit concurrent connections

### Elevation of Privilege
- **RBAC Enforcement:** Role-based access control
- **Principle of Least Privilege:** Minimal permissions
- **TOCTOU Race Condition Prevention:**
  - Optimistic locking (version field)
  - Database-level constraints
  - Transaction isolation level: SERIALIZABLE for critical operations
  - Row-level locking for balance updates
- **Credit Double-Spending Prevention:**
  - Atomic balance updates (BEGIN TRANSACTION)
  - Reserved balance mechanism
  - Distributed lock for critical operations (Redis)
  - Idempotency checks before deduction
- **Admin Action Audit:** All admin operations logged

### Saga-Specific Security (NEW)
- **Multi-Service Reconciliation:**
  - Saga state verification across services
  - Compensation idempotency (can retry safely)
  - Cross-service audit trail
  - Saga timeout detection (max 5 minutes)
- **Saga Timeout Handling:**
  - Automatic compensation on timeout
  - Dead letter queue for failed sagas
  - Manual intervention dashboard
- **Saga Replay Protection:**
  - Saga ID uniqueness check
  - Step completion verification
  - Prevent duplicate saga execution

### Financial-Specific Threats (NEW)

#### Double-Spending Attack
- **Prevention:**
  - Optimistic locking on credit_balance table
  - Check available balance before deduction
  - Reserve balance during pending operations
  - Atomic commit after all checks pass

#### Ledger Tampering
- **Prevention:**
  - Immutable ledger (no UPDATE/DELETE)
  - Hash chain verification
  - Periodic integrity checks
  - Alert on hash mismatch

#### Transaction Replay
- **Prevention:**
  - Idempotency key required
  - Request timestamp validation
  - Nonce tracking (Redis)
  - Duplicate detection within 24h window

#### Unauthorized Refunds
- **Prevention:**
  - Refund authorization workflow
  - Admin approval for refunds > threshold
  - Refund reason required
  - Audit trail for all refunds

### Compliance Requirements
- **PCI DSS Level 1:** If processing credit cards
- **SOC 2 Type II:** Security controls audit
- **GDPR:** If handling EU customer data
- **Data Residency:** Store data in approved regions

### Security Testing
- **Penetration Testing:** Annual third-party audit
- **Vulnerability Scanning:** Weekly automated scans
- **Dependency Audits:** Daily npm/pip audit
- **OWASP Top 10:** Coverage in test suite
- **Chaos Engineering:** Test failure scenarios
```

---

## 5. DI Pattern Handling

### 5.1 di=none or --no-di

Skip DI Pattern section entirely.

### 5.2 di=minimal

```markdown
## Dependency Injection

This service uses constructor-based dependency injection.

**Example:**
```typescript
export class ServiceName {
  constructor(database?, logger?) {
    this.database = database || createDefault();
    this.logger = logger || createDefault();
  }
}
```

**Testing:** Inject mocks via constructor for unit tests.

---
```

### 5.3 di=full (default for backend)

Complete DI Pattern section as in v4.0:
- Core requirements
- Interface-based dependencies
- Testing requirements
- Benefits
- Complete examples

---

## 6. Performance Requirements Handling

### 6.1 performance=none

Skip performance section.

### 6.2 performance=basic

```markdown
## Performance Requirements

**Latency:** P99 < [threshold]
**Throughput:** [X] TPS sustained
**Availability:** [X]% uptime

---
```

### 6.3 performance=full (default for financial)

Complete performance section as in v4.0:
- P50/P90/P95/P99 targets
- Throughput capacity (normal + peak)
- SLA requirements
- Database performance
- Queue/worker baselines
- Metrics & alerting
- Load testing requirements

**Enhanced: Service-Level Performance Breakdown**

For multi-service architectures (especially financial systems), include per-service performance targets:

```markdown
## Performance Requirements

### System-Wide Targets

**Latency:**
- P50: < 100ms
- P95: < 200ms
- P99: < 300ms

**Throughput:**
- Normal load: 1000 TPS
- Peak load: 3000 TPS

**Availability:**
- SLA: 99.95% uptime
- Max downtime: 4.38 hours/year

**Scalability:**
- Horizontal scaling: Auto-scale based on CPU > 70%
- Max instances: 20

---

### Per-Service Performance Targets

#### Credit Service

**Latency:**
- P50: < 50ms
- P95: < 100ms
- P99: < 150ms

**Throughput:**
- Target: 1000 TPS
- Peak: 2000 TPS

**Workload Characteristics:**
- High-frequency reads (balance queries)
- Medium-frequency writes (credit add/deduct)
- Critical path: User-facing operations

**Database:**
- Read queries: < 10ms (P95)
- Write queries: < 20ms (P95)
- Connection pool: 20-50 connections

**Caching:**
- Cache hit rate: > 80%
- Cache TTL: 60 seconds for balance
- Cache invalidation: On balance update

---

#### Payment Service

**Latency:**
- P50: < 100ms
- P95: < 200ms
- P99: < 300ms
- P99.9: < 500ms (includes external API calls)

**Throughput:**
- Target: 500 TPS
- Peak: 1000 TPS

**Workload Characteristics:**
- Low-frequency, high-value transactions
- External API dependency (Stripe, PromptPay)
- Retry logic for failed payments

**External API:**
- Stripe API timeout: 10s
- Retry attempts: 3
- Circuit breaker: Open after 5 failures

**Database:**
- Transaction isolation: SERIALIZABLE
- Lock timeout: 5s

---

#### Billing Service

**Latency:**
- P50: < 200ms
- P95: < 500ms
- P99: < 1000ms

**Throughput:**
- Target: 100 TPS
- Peak: 300 TPS

**Workload Characteristics:**
- Batch processing (invoice generation)
- Scheduled jobs (monthly billing cycles)
- Complex calculations (tax, proration)

**Batch Jobs:**
- Invoice generation: < 5 minutes for 10K users
- Billing cycle: < 30 minutes for 100K users

**Database:**
- Bulk insert: 1000 records/second
- Report queries: < 5s

---

#### Cost Management Service

**Latency:**
- P50: < 100ms
- P95: < 200ms
- P99: < 300ms

**Throughput:**
- Target: 200 TPS
- Peak: 500 TPS

**Workload Characteristics:**
- Analytics queries (cost reports)
- Aggregations (daily/monthly summaries)
- Real-time cost tracking

**Database:**
- Aggregation queries: < 2s
- Time-series data: Partitioned by month
- Materialized views: Refreshed every 5 minutes

**Caching:**
- Report cache: 5 minutes TTL
- Summary cache: 15 minutes TTL

---

### Database Performance

**PostgreSQL:**
- Connection pool: 50-100 connections per service
- Query timeout: 30s
- Statement timeout: 10s
- Idle transaction timeout: 60s

**Read Replicas:**
- 2 read replicas for read-heavy services
- Replication lag: < 1s

**Indexes:**
- All foreign keys indexed
- Composite indexes for common queries
- Partial indexes for filtered queries

**Monitoring:**
- Slow query log: > 100ms
- Long-running queries: > 5s
- Deadlock detection: Alert immediately

---

### Queue Performance

**Message Queue (Redis/RabbitMQ):**
- Message processing: < 100ms per message
- Queue depth: Alert if > 1000 messages
- Consumer lag: < 10 seconds

**Dead Letter Queue:**
- Max retries: 3
- Retry backoff: Exponential (1s, 5s, 30s)

---

### Monitoring & Alerting

**Metrics Collection:**
- Interval: 10 seconds
- Retention: 30 days (high-res), 1 year (aggregated)

**Alerts:**
- P99 latency > 500ms: Warning
- P99 latency > 1000ms: Critical
- Error rate > 1%: Warning
- Error rate > 5%: Critical
- Availability < 99.9%: Critical

---

### Load Testing Requirements

**Scenarios:**
1. **Normal Load:** 1000 TPS for 1 hour
2. **Peak Load:** 3000 TPS for 15 minutes
3. **Stress Test:** Increase until failure
4. **Endurance Test:** 1000 TPS for 24 hours
5. **Spike Test:** 0 → 5000 TPS in 10 seconds

**Acceptance Criteria:**
- All P99 targets met under normal load
- No errors under normal load
- Graceful degradation under peak load
- System recovers within 5 minutes after spike
```

**Customization:**
- Adjust service names based on SPEC context
- Add/remove services as needed
- Modify targets based on business requirements
- Include domain-specific workload characteristics

---

## 7. Domain-Based Enhancement

If `--domain` specified, adjust sections:

### 7.1 domain=healthcare

Auto-add:
- Privacy & HIPAA compliance notes
- Real-time requirements
- Audit logging (mandatory)
- Data retention policies

### 7.2 domain=iot

Auto-add:
- High throughput expectations
- Telemetry patterns
- Edge computing considerations
- Batch processing requirements

### 7.3 domain=logistics

Auto-add:
- High SLA requirements (99.9%+)
- Geographic distribution
- Real-time tracking needs
- Integration complexity

### 7.4 domain=ai

Auto-add:
- Latency sensitivity
- Model versioning
- Inference performance
- GPU/compute requirements

### 7.5 domain=fintech

Same as `--profile=financial`

**Additional Saga Patterns for Fintech:**

Automatically include comprehensive saga orchestration patterns:

```markdown
## Saga Orchestration Patterns

### 1. Credit Purchase Saga

**Flow:**
```
1. Reserve Credit → 2. Process Payment → 3. Commit Credit → 4. Update Ledger
```

**Compensation:**
```
4. Rollback Ledger ← 3. Rollback Credit ← 2. Refund Payment ← 1. Release Reserve
```

**Implementation:**
```typescript
class CreditPurchaseSaga {
  async execute(amount: number, userId: string, paymentMethod: string) {
    const sagaId = generateSagaId();
    
    try {
      // Step 1: Reserve credit
      await creditService.reserve(userId, amount, sagaId);
      
      // Step 2: Process payment
      const paymentId = await paymentService.charge(paymentMethod, amount, sagaId);
      
      // Step 3: Commit credit
      await creditService.commit(userId, amount, sagaId);
      
      // Step 4: Update ledger
      await ledgerService.record(userId, 'CREDIT', amount, paymentId);
      
      await sagaService.markCompleted(sagaId);
    } catch (error) {
      await this.compensate(sagaId, error);
      throw error;
    }
  }
  
  async compensate(sagaId: string, error: Error) {
    const saga = await sagaService.getState(sagaId);
    
    // Rollback in reverse order
    if (saga.currentStep >= 4) await ledgerService.rollback(sagaId);
    if (saga.currentStep >= 3) await creditService.rollback(sagaId);
    if (saga.currentStep >= 2) await paymentService.refund(saga.paymentId);
    if (saga.currentStep >= 1) await creditService.releaseReserve(sagaId);
    
    await sagaService.markCompensated(sagaId, error.message);
  }
}
```

### 2. Cost Deduction Saga

**Flow:**
```
1. Check Balance → 2. Reserve Credit → 3. Deduct Credit → 4. Update Ledger → 5. Execute Service
```

**Compensation:**
```
5. Rollback Service ← 4. Rollback Ledger ← 3. Restore Credit ← 2. Release Reserve
```

### 3. Refund Saga (NEW)

**Flow:**
```
1. Validate Refund → 2. Process Refund → 3. Add Credit → 4. Update Ledger → 5. Notify User
```

**Compensation:**
```
5. Cancel Notification ← 4. Rollback Ledger ← 3. Deduct Credit ← 2. Reverse Refund
```

**Types:**
- **Full Refund:** Refund entire transaction amount
- **Partial Refund:** Refund portion of transaction
- **Refund Compensation:** Handle failed refund attempts

**Implementation:**
```typescript
class RefundSaga {
  async execute(transactionId: string, amount: number, reason: string) {
    const sagaId = generateSagaId();
    
    try {
      // Step 1: Validate refund eligibility
      const transaction = await validateRefund(transactionId, amount);
      
      // Step 2: Process refund via payment provider
      const refundId = await paymentService.refund(transaction.paymentId, amount);
      
      // Step 3: Add credit back to user
      await creditService.add(transaction.userId, amount, sagaId);
      
      // Step 4: Update ledger
      await ledgerService.record(transaction.userId, 'REFUND', amount, refundId);
      
      // Step 5: Notify user
      await notificationService.send(transaction.userId, 'refund_completed', { amount });
      
      await sagaService.markCompleted(sagaId);
    } catch (error) {
      await this.compensate(sagaId, error);
      throw error;
    }
  }
}
```

### 4. Failed Payment Compensation Saga (NEW)

**Scenario:** Payment fails after credit was reserved

**Flow:**
```
1. Detect Payment Failure → 2. Release Reserved Credit → 3. Update Status → 4. Retry Logic
```

**Retry Strategy:**
- **Attempt 1:** Immediate retry
- **Attempt 2:** Retry after 5 seconds
- **Attempt 3:** Retry after 30 seconds
- **After 3 failures:** Move to dead letter queue, notify admin

**Implementation:**
```typescript
class FailedPaymentCompensationSaga {
  async execute(sagaId: string, retryCount: number = 0) {
    const saga = await sagaService.getState(sagaId);
    
    try {
      // Release reserved credit
      await creditService.releaseReserve(saga.userId, saga.amount, sagaId);
      
      // Update saga status
      await sagaService.updateStatus(sagaId, 'COMPENSATED');
      
      // Notify user of failure
      await notificationService.send(saga.userId, 'payment_failed', {
        amount: saga.amount,
        reason: saga.errorMessage
      });
      
    } catch (error) {
      if (retryCount < 3) {
        await this.scheduleRetry(sagaId, retryCount + 1);
      } else {
        await deadLetterQueue.add(sagaId, error);
        await alertService.notifyAdmin('saga_compensation_failed', { sagaId });
      }
    }
  }
}
```

### 5. Partial Apply Scenario (NEW)

**Scenario:** User has insufficient credit, apply partial amount

**Flow:**
```
1. Check Available Balance → 2. Calculate Partial Amount → 3. Apply Partial → 4. Create Debt Record
```

**Implementation:**
```typescript
class PartialApplySaga {
  async execute(userId: string, requestedAmount: number, serviceId: string) {
    const balance = await creditService.getBalance(userId);
    
    if (balance.available >= requestedAmount) {
      // Full deduction
      return await costDeductionSaga.execute(userId, requestedAmount, serviceId);
    } else if (balance.available > 0) {
      // Partial deduction
      const partialAmount = balance.available;
      const remainingAmount = requestedAmount - partialAmount;
      
      await creditService.deduct(userId, partialAmount, sagaId);
      await debtService.create(userId, remainingAmount, serviceId);
      await ledgerService.record(userId, 'PARTIAL_DEBIT', partialAmount, serviceId);
      
      return { applied: partialAmount, debt: remainingAmount };
    } else {
      throw new InsufficientCreditError('No credit available');
    }
  }
}
```

### 6. Idempotent Replay Flow (NEW)

**Purpose:** Ensure saga can be safely replayed without side effects

**Idempotency Key:**
```typescript
interface SagaRequest {
  idempotencyKey: string; // Client-provided unique key
  userId: string;
  amount: number;
  // ... other fields
}
```

**Implementation:**
```typescript
class IdempotentSagaExecutor {
  async execute(request: SagaRequest) {
    // Check if already processed
    const existing = await sagaService.findByIdempotencyKey(request.idempotencyKey);
    
    if (existing) {
      if (existing.status === 'COMPLETED') {
        // Return cached result
        return existing.result;
      } else if (existing.status === 'PENDING') {
        // Wait for completion
        return await this.waitForCompletion(existing.sagaId);
      } else if (existing.status === 'FAILED') {
        // Return cached error
        throw new Error(existing.errorMessage);
      }
    }
    
    // Create new saga with idempotency key
    const sagaId = await sagaService.create({
      idempotencyKey: request.idempotencyKey,
      type: 'CREDIT_PURCHASE',
      payload: request
    });
    
    // Execute saga
    return await this.executeSaga(sagaId, request);
  }
}
```

**Duplicate Request Detection:**
```typescript
// Redis-based duplicate detection
const isDuplicate = await redis.set(
  `idempotency:${idempotencyKey}`,
  sagaId,
  'EX', 86400, // 24 hour expiration
  'NX' // Only set if not exists
);

if (!isDuplicate) {
  const existingSagaId = await redis.get(`idempotency:${idempotencyKey}`);
  return await sagaService.getResult(existingSagaId);
}
```

### Saga Best Practices

1. **Idempotency:** All saga steps must be idempotent
2. **Timeout:** Set maximum saga execution time (5 minutes)
3. **Compensation:** Always implement compensation logic
4. **State Persistence:** Store saga state in database
5. **Monitoring:** Track saga success/failure rates
6. **Dead Letter Queue:** Handle permanently failed sagas
7. **Retry Logic:** Exponential backoff for transient failures
8. **Audit Trail:** Log all saga state transitions
```

---

**Role Terminology & Permissions (Fintech):**

Automatically include role definitions for financial systems:

```markdown
## Role Terminology & Permissions

### User Roles

#### 1. End User (ROLE_USER)
**Description:** Standard customer using the system

**Permissions:**
- View own balance
- Add credit (via payment)
- View own transaction history
- View own invoices
- Update own profile

**Restrictions:**
- Cannot view other users' data
- Cannot perform admin operations
- Cannot access system reports

---

#### 2. Premium User (ROLE_PREMIUM)
**Description:** Paid subscription customer

**Inherits:** ROLE_USER

**Additional Permissions:**
- Higher rate limits (500 req/min vs 100 req/min)
- Access to advanced features
- Priority support
- Export transaction history (CSV, PDF)

---

#### 3. Support Agent (ROLE_SUPPORT)
**Description:** Customer support team member

**Permissions:**
- View user profiles (read-only)
- View user transaction history (read-only)
- View user balance (read-only)
- Create support tickets
- Add notes to user accounts

**Restrictions:**
- Cannot modify user balance
- Cannot process refunds
- Cannot delete data
- All actions logged for audit

---

#### 4. Finance Manager (ROLE_FINANCE)
**Description:** Finance team member

**Permissions:**
- View all financial reports
- Process refunds (with approval)
- Generate invoices
- View all transactions
- Export financial data
- Reconcile accounts

**Restrictions:**
- Cannot modify system configuration
- Cannot manage users
- Cannot access technical logs

---

#### 5. Admin (ROLE_ADMIN)
**Description:** System administrator

**Permissions:**
- All ROLE_FINANCE permissions
- Manage users (create, update, disable)
- Modify user balances (with audit)
- Configure system settings
- View system logs
- Manage roles and permissions

**Restrictions:**
- Cannot delete audit logs
- Cannot bypass security controls
- All actions logged and alerted

---

#### 6. Super Admin (ROLE_SUPER_ADMIN)
**Description:** Technical team lead

**Permissions:**
- All ROLE_ADMIN permissions
- Access database directly (emergency only)
- Modify audit logs (emergency recovery only)
- Deploy system updates
- Access production servers

**Restrictions:**
- All actions require MFA
- All actions alerted to security team
- Emergency access logged and reviewed

---

### Permission Matrix

| Action | User | Premium | Support | Finance | Admin | Super Admin |
|--------|------|---------|---------|---------|-------|-------------|
| View own balance | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Add credit | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| View other user balance | ❌ | ❌ | ✅ (read) | ✅ | ✅ | ✅ |
| Modify user balance | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| Process refund | ❌ | ❌ | ❌ | ✅ (approval) | ✅ | ✅ |
| View financial reports | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| Manage users | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| System configuration | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| Database access | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |

---

### Role Assignment Rules

1. **Default Role:** New users get ROLE_USER
2. **Role Elevation:** Requires approval from ROLE_ADMIN or higher
3. **Role Downgrade:** Can be done by ROLE_ADMIN or higher
4. **Multiple Roles:** Users can have multiple roles (additive permissions)
5. **Temporary Roles:** Support temporary role elevation (e.g., 24 hours)

---

### Implementation

**Database Schema:**
```sql
CREATE TABLE roles (
  id UUID PRIMARY KEY,
  name VARCHAR(50) UNIQUE NOT NULL,
  description TEXT,
  permissions JSONB NOT NULL
);

CREATE TABLE user_roles (
  user_id UUID NOT NULL,
  role_id UUID NOT NULL,
  granted_by UUID NOT NULL,
  granted_at TIMESTAMP NOT NULL DEFAULT NOW(),
  expires_at TIMESTAMP,
  PRIMARY KEY (user_id, role_id)
);
```

**Permission Check:**
```typescript
function hasPermission(user: User, permission: string): boolean {
  return user.roles.some(role => 
    role.permissions.includes(permission)
  );
}

// Usage
if (!hasPermission(user, 'credit:modify')) {
  throw new ForbiddenError('Insufficient permissions');
}
```
```

### 7.6 domain=internal

Reduce requirements:
- Lower SLA expectations
- Simpler security
- Minimal performance tracking

---

### 7.7 API Specification (Backend Services)

For backend-service and financial profiles, auto-generate API specification:

```markdown
## API Specification

### Base URL
```
Production: https://api.example.com/v1
Staging: https://api-staging.example.com/v1
Development: http://localhost:3000/v1
```

### Authentication
All endpoints require JWT authentication unless marked as public.

**Header:**
```
Authorization: Bearer <jwt_token>
```

### Common Response Format

**Success Response:**
```json
{
  "success": true,
  "data": { ... },
  "meta": {
    "timestamp": "2025-12-03T14:30:00Z",
    "requestId": "req_abc123"
  }
}
```

**Error Response:**
```json
{
  "success": false,
  "error": {
    "code": "INSUFFICIENT_CREDIT",
    "message": "Insufficient credit balance",
    "details": {
      "required": 100.00,
      "available": 50.00
    }
  },
  "meta": {
    "timestamp": "2025-12-03T14:30:00Z",
    "requestId": "req_abc123"
  }
}
```

---

### Credit Management Endpoints

#### Get Balance
```http
GET /credit/balance
```

**Response:**
```json
{
  "success": true,
  "data": {
    "userId": "user_123",
    "balance": 1000.00,
    "reservedBalance": 50.00,
    "availableBalance": 950.00,
    "currency": "THB",
    "lastUpdated": "2025-12-03T14:30:00Z"
  }
}
```

---

#### Add Credit
```http
POST /credit/add
```

**Request:**
```json
{
  "amount": 100.00,
  "paymentMethod": "promptpay",
  "idempotencyKey": "idem_abc123"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "transactionId": "txn_abc123",
    "userId": "user_123",
    "amount": 100.00,
    "newBalance": 1100.00,
    "status": "completed",
    "createdAt": "2025-12-03T14:30:00Z"
  }
}
```

---

#### Deduct Credit
```http
POST /credit/deduct
```

**Request:**
```json
{
  "amount": 50.00,
  "reason": "Service usage",
  "metadata": {
    "serviceId": "svc_123",
    "usageType": "api_call"
  },
  "idempotencyKey": "idem_xyz789"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "transactionId": "txn_xyz789",
    "userId": "user_123",
    "amount": 50.00,
    "newBalance": 1050.00,
    "status": "completed",
    "createdAt": "2025-12-03T14:30:00Z"
  }
}
```

---

### Transaction History Endpoints

#### Get Transaction History
```http
GET /transactions?page=1&limit=20&type=credit
```

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `limit` (optional): Items per page (default: 20, max: 100)
- `type` (optional): Filter by type (credit, debit, refund)
- `startDate` (optional): Start date (ISO 8601)
- `endDate` (optional): End date (ISO 8601)

**Response:**
```json
{
  "success": true,
  "data": {
    "transactions": [
      {
        "id": "txn_abc123",
        "type": "credit",
        "amount": 100.00,
        "balance": 1100.00,
        "description": "Credit added via PromptPay",
        "createdAt": "2025-12-03T14:30:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 150,
      "totalPages": 8
    }
  }
}
```

---

### Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `INVALID_REQUEST` | 400 | Invalid request parameters |
| `UNAUTHORIZED` | 401 | Missing or invalid authentication |
| `FORBIDDEN` | 403 | Insufficient permissions |
| `NOT_FOUND` | 404 | Resource not found |
| `INSUFFICIENT_CREDIT` | 400 | Not enough credit balance |
| `DUPLICATE_TRANSACTION` | 409 | Duplicate idempotency key |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests |
| `INTERNAL_ERROR` | 500 | Internal server error |
| `SERVICE_UNAVAILABLE` | 503 | Service temporarily unavailable |

---

### Rate Limits

See [Rate Limiting Strategy](#rate-limiting-strategy) section.

---

### Idempotency

All mutation endpoints (POST, PUT, DELETE) support idempotency via `idempotencyKey`.

**Rules:**
- Key format: Any string up to 255 characters
- Key expiration: 24 hours
- Duplicate requests return cached response
- Different payload with same key returns 409 Conflict

**Example:**
```typescript
// First request
POST /credit/add
{
  "amount": 100.00,
  "idempotencyKey": "key_123"
}
// Response: 200 OK, transaction created

// Duplicate request (same key, same payload)
POST /credit/add
{
  "amount": 100.00,
  "idempotencyKey": "key_123"
}
// Response: 200 OK, returns cached result (no new transaction)

// Conflicting request (same key, different payload)
POST /credit/add
{
  "amount": 200.00,  // Different amount!
  "idempotencyKey": "key_123"
}
// Response: 409 Conflict
```
```

---

### 7.8 Business Rules & Logic (Financial Profile)

For financial profile, auto-generate comprehensive business rules:

```markdown
## Business Rules & Logic

### Usage Limits

**Per-User Limits:**
- Maximum redemptions per user: [Specify based on context]
- Redemption window: [e.g., 1 per day, 5 per month]
- Cooldown period: [e.g., 24 hours between redemptions]

**Per-Code Limits:**
- Global usage limit: [e.g., 1000 total redemptions]
- Per-user limit: [e.g., 1 redemption per user]
- Concurrent redemption handling: Database unique constraint

**Example:**
```typescript
interface UsageLimits {
  maxRedemptionsPerUser: number;      // e.g., 5
  redemptionWindowHours: number;      // e.g., 24
  globalUsageLimit: number;           // e.g., 1000
  perUserLimit: number;               // e.g., 1
}
```

---

### Stacking Rules

**Promo Code Stacking:**
- **Allowed:** [Yes/No]
- **Conditions:** [e.g., Maximum 2 codes per transaction]
- **Priority:** [e.g., Highest value first, FIFO]

**Campaign Overlap:**
- **Multiple qualifying campaigns:** [How to resolve - highest value, user choice, etc.]
- **Conflicting rules:** [Priority order]

**Example Scenarios:**

| Scenario | Behavior |
|----------|----------|
| User has code A (10 credits) and code B (20 credits) | Apply code B only (highest value) |
| User redeems code during active campaign | Code takes priority over campaign |
| Code and campaign both apply | Stack if allowed, otherwise code wins |

---

### Expiration Behavior

**Code Expiration:**
- `expiresAt` field: Exact expiration timestamp
- `null` expiration: [Never expires / Expires after 1 year / etc.]
- Grace period: [e.g., None / 24 hours after expiration]

**Redemption Deadline:**
- Code must be redeemed before `expiresAt`
- Expired codes return error: `PROMO_CODE_EXPIRED`
- No partial redemptions after expiration

**Campaign Expiration:**
- Campaign end date applies to all codes in campaign
- Individual code expiration takes precedence if earlier

---

### User Eligibility Rules

**New Users:**
- Eligible for "new user" codes only
- Defined as: [e.g., Registered within last 30 days, No prior transactions]

**Returning Users:**
- Eligible for "returning user" codes
- Defined as: [e.g., Registered > 30 days ago, Has prior transactions]

**User Segments:**
- Premium users: [Special codes or higher limits]
- Suspended users: [Cannot redeem codes]
- Banned users: [Blocked from all promotions]

---

### Edge Cases

**Concurrent Redemptions:**
- Same user, same code, simultaneous requests
- **Handling:** Database unique constraint prevents duplicates
- **Response:** First request succeeds, others return 409 Conflict

**Partial Failures:**
- Code validated but credit grant fails
- **Handling:** Mark redemption as "pending", retry via queue
- **User experience:** Show "processing" status

**Code Deactivation:**
- Admin deactivates code mid-campaign
- **Behavior:** Existing redemptions honored, new redemptions blocked
- **Notification:** [Yes/No - notify affected users]

**Usage Limit Reached:**
- Code reaches global usage limit during redemption
- **Handling:** Atomic check-and-increment
- **Response:** `PROMO_CODE_USAGE_LIMIT_REACHED`
```

---

### 7.9 External Integration Contracts (Financial Profile)

For financial profile with external integrations, generate detailed contracts:

```markdown
## External Integration Contracts

### Financial System Integration

**Purpose:** Grant credits to users after successful promo code redemption

**Endpoint:** `POST /api/v1/financial/credit/grant`

**Request Schema:**
```typescript
interface CreditGrantRequest {
  userId: string;              // User ID to receive credit
  amount: number;              // Credit amount (positive number)
  source: 'promo_code';        // Fixed value for promo redemptions
  sourceId: string;            // Promo code redemption ID
  idempotencyKey: string;      // Unique key for idempotent retry
  metadata: {
    promoCode: string;         // Original promo code
    campaignId?: string;       // Campaign ID if applicable
    redemptionTimestamp: string; // ISO 8601 timestamp
  };
}
```

**Response Schema:**

**Success (200 OK):**
```json
{
  "success": true,
  "data": {
    "transactionId": "txn_abc123",
    "userId": "user_123",
    "amount": 100.00,
    "newBalance": 1100.00,
    "status": "completed"
  }
}
```

**Error Responses:**

| HTTP Status | Error Code | Description | Retry? |
|-------------|------------|-------------|--------|
| 400 | `INVALID_REQUEST` | Invalid request parameters | No |
| 404 | `USER_NOT_FOUND` | User does not exist | No |
| 409 | `DUPLICATE_TRANSACTION` | Idempotency key conflict | No |
| 429 | `RATE_LIMIT_EXCEEDED` | Too many requests | Yes (backoff) |
| 500 | `INTERNAL_ERROR` | Internal server error | Yes (backoff) |
| 503 | `SERVICE_UNAVAILABLE` | Service temporarily down | Yes (backoff) |

---

### Retry Strategy

**Retry Policy:**
- **Max attempts:** 5
- **Backoff:** Exponential (2^attempt seconds)
- **Retry on:** 429, 500, 503, network errors
- **No retry on:** 400, 404, 409

**Implementation:**
```typescript
async function grantCreditWithRetry(
  request: CreditGrantRequest,
  maxAttempts: number = 5
): Promise<CreditGrantResponse> {
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await financialSystemClient.grantCredit(request);
    } catch (error) {
      const shouldRetry = [
        429, // Rate limit
        500, // Internal error
        503  // Service unavailable
      ].includes(error.status);
      
      if (!shouldRetry || attempt === maxAttempts) {
        throw error;
      }
      
      const backoffMs = Math.pow(2, attempt) * 1000;
      await sleep(backoffMs);
    }
  }
}
```

---

### Dead Letter Queue (DLQ) Policy

**When to DLQ:**
- All retry attempts exhausted
- Non-retryable errors (400, 404)
- Timeout after 5 minutes

**DLQ Processing:**
- Manual review required
- Alert sent to ops team
- User notified of pending credit

**DLQ Schema:**
```typescript
interface DLQMessage {
  originalRequest: CreditGrantRequest;
  error: {
    code: string;
    message: string;
    lastAttemptTimestamp: string;
  };
  attempts: number;
  enqueuedAt: string;
}
```

---

### Transaction Boundaries

**Atomicity Guarantee:**
1. Promo redemption record created (Promo System DB)
2. Credit grant job enqueued (Message Queue)
3. Credit granted (Financial System)

**Failure Scenarios:**

| Failure Point | Behavior | Recovery |
|---------------|----------|----------|
| After step 1, before step 2 | Redemption marked as "pending" | Retry job enqueue on next startup |
| After step 2, before step 3 | Job in queue | BullMQ retries automatically |
| Step 3 fails (retryable) | Job retries with backoff | Eventual success or DLQ |
| Step 3 fails (non-retryable) | Job moves to DLQ | Manual intervention required |

---

### Idempotency Requirements

**Cross-System Idempotency:**
- Promo System generates unique `idempotencyKey` per redemption
- Financial System MUST honor idempotency key
- Same key + same payload = return cached result
- Same key + different payload = return 409 Conflict

**Key Format:**
```typescript
const idempotencyKey = `promo_${redemptionId}_${userId}`;
```

**Expiration:** 24 hours (Financial System responsibility)
```

---

### 7.10 Environment Configuration (All Profiles)

For all profiles, generate environment configuration section:

```markdown
## Environment Configuration

### Environment Variables

**Required Variables:**

```bash
# Application
NODE_ENV=production              # Environment: development, staging, production
PORT=3000                        # Server port
LOG_LEVEL=info                   # Logging level: debug, info, warn, error

# Database
DATABASE_URL=postgresql://user:pass@host:5432/dbname
DATABASE_POOL_MIN=10             # Minimum connection pool size
DATABASE_POOL_MAX=100            # Maximum connection pool size
DATABASE_SSL=true                # Enable SSL for database connection

# Redis
REDIS_URL=redis://host:6379
REDIS_PASSWORD=secret            # Redis password (optional)
REDIS_DB=0                       # Redis database number (0-15)

# Authentication
JWT_SECRET=your-secret-key       # JWT signing secret (min 32 characters)
JWT_EXPIRY=24h                   # JWT token expiration

# External Services
FINANCIAL_SYSTEM_URL=https://api.financial.example.com
FINANCIAL_SYSTEM_API_KEY=key_xxx # API key for financial system

# Monitoring
METRICS_PORT=9090                # Prometheus metrics port
SENTRY_DSN=https://...           # Sentry error tracking DSN (optional)
```

**Optional Variables:**

```bash
# Feature Flags
ENABLE_PROMO_STACKING=false      # Allow multiple promo codes per transaction
ENABLE_CAMPAIGN_ANALYTICS=true   # Enable campaign analytics

# Rate Limiting
RATE_LIMIT_ENABLED=true          # Enable rate limiting
RATE_LIMIT_MAX_REQUESTS=100      # Max requests per window
RATE_LIMIT_WINDOW=3600           # Window in seconds (1 hour)

# Performance
CACHE_ENABLED=true               # Enable Redis caching
CACHE_TTL=300                    # Cache TTL in seconds (5 minutes)
```

---

### Configuration Validation

**Validation Schema:**

```typescript
import { z } from 'zod';

export const EnvSchema = z.object({
  // Application
  NODE_ENV: z.enum(['development', 'staging', 'production']),
  PORT: z.coerce.number().int().positive().default(3000),
  LOG_LEVEL: z.enum(['debug', 'info', 'warn', 'error']).default('info'),
  
  // Database
  DATABASE_URL: z.string().url(),
  DATABASE_POOL_MIN: z.coerce.number().int().positive().default(10),
  DATABASE_POOL_MAX: z.coerce.number().int().positive().default(100),
  DATABASE_SSL: z.coerce.boolean().default(true),
  
  // Redis
  REDIS_URL: z.string().url(),
  REDIS_PASSWORD: z.string().optional(),
  REDIS_DB: z.coerce.number().int().min(0).max(15).default(0),
  
  // Authentication
  JWT_SECRET: z.string().min(32),
  JWT_EXPIRY: z.string().regex(/^\d+[smhd]$/).default('24h'),
  
  // External Services
  FINANCIAL_SYSTEM_URL: z.string().url(),
  FINANCIAL_SYSTEM_API_KEY: z.string().min(10),
  
  // Monitoring
  METRICS_PORT: z.coerce.number().int().positive().default(9090),
  SENTRY_DSN: z.string().url().optional(),
  
  // Feature Flags
  ENABLE_PROMO_STACKING: z.coerce.boolean().default(false),
  ENABLE_CAMPAIGN_ANALYTICS: z.coerce.boolean().default(true),
  
  // Rate Limiting
  RATE_LIMIT_ENABLED: z.coerce.boolean().default(true),
  RATE_LIMIT_MAX_REQUESTS: z.coerce.number().int().positive().default(100),
  RATE_LIMIT_WINDOW: z.coerce.number().int().positive().default(3600),
  
  // Performance
  CACHE_ENABLED: z.coerce.boolean().default(true),
  CACHE_TTL: z.coerce.number().int().positive().default(300),
});

export type Env = z.infer<typeof EnvSchema>;

// Validate on startup
export function validateEnv(): Env {
  try {
    return EnvSchema.parse(process.env);
  } catch (error) {
    console.error('❌ Environment validation failed:');
    console.error(error.errors);
    process.exit(1);
  }
}
```

---

### Per-Environment Overrides

**Development (.env.development):**
```bash
NODE_ENV=development
LOG_LEVEL=debug
DATABASE_SSL=false
CACHE_ENABLED=false
RATE_LIMIT_ENABLED=false
```

**Staging (.env.staging):**
```bash
NODE_ENV=staging
LOG_LEVEL=info
DATABASE_URL=postgresql://user:pass@staging-db:5432/dbname
FINANCIAL_SYSTEM_URL=https://api-staging.financial.example.com
```

**Production (.env.production):**
```bash
NODE_ENV=production
LOG_LEVEL=warn
DATABASE_URL=postgresql://user:pass@prod-db:5432/dbname
DATABASE_POOL_MAX=200
FINANCIAL_SYSTEM_URL=https://api.financial.example.com
SENTRY_DSN=https://xxx@sentry.io/xxx
```

---

### Secure Secret Handling

**DO NOT commit secrets to version control!**

**Recommended Approaches:**

1. **Local Development:** `.env` file (gitignored)
2. **Staging/Production:** Secret management service
   - AWS Secrets Manager
   - Google Cloud Secret Manager
   - HashiCorp Vault
   - Kubernetes Secrets

**Example (AWS Secrets Manager):**
```typescript
import { SecretsManagerClient, GetSecretValueCommand } from '@aws-sdk/client-secrets-manager';

async function loadSecrets() {
  const client = new SecretsManagerClient({ region: 'ap-southeast-1' });
  const response = await client.send(
    new GetSecretValueCommand({ SecretId: 'prod/promo-system' })
  );
  
  const secrets = JSON.parse(response.SecretString!);
  
  process.env.JWT_SECRET = secrets.JWT_SECRET;
  process.env.DATABASE_URL = secrets.DATABASE_URL;
  process.env.FINANCIAL_SYSTEM_API_KEY = secrets.FINANCIAL_SYSTEM_API_KEY;
}
```
```

---

### 7.11 Operational Requirements (Financial Profile)

For financial profile, generate comprehensive operational requirements:

```markdown
## Operational Requirements

### Deployment Topology

**Architecture:**
- **Load Balancer:** AWS ALB / Google Cloud Load Balancer
- **Application Servers:** 3+ instances (multi-AZ)
- **Database:** PostgreSQL 16+ (primary + 2 read replicas)
- **Cache:** Redis 7+ cluster (3 nodes)
- **Message Queue:** Redis (same cluster or separate)

**Regions:**
- **Primary:** [e.g., ap-southeast-1 (Singapore)]
- **DR:** [e.g., ap-southeast-2 (Sydney)]

**High Availability:**
- **Application:** Auto-scaling group (min 3, max 10 instances)
- **Database:** Multi-AZ deployment with automatic failover
- **Redis:** Cluster mode with replication

**Diagram:**
```
                    ┌─────────────┐
                    │ Load Balancer│
                    └──────┬──────┘
                           │
           ┌───────────────┼───────────────┐
           │               │               │
      ┌────▼────┐     ┌────▼────┐     ┌────▼────┐
      │ App 1   │     │ App 2   │     │ App 3   │
      │ (AZ-A)  │     │ (AZ-B)  │     │ (AZ-C)  │
      └────┬────┘     └────┬────┘     └────┬────┘
           │               │               │
           └───────────────┼───────────────┘
                           │
              ┌────────────┴────────────┐
              │                         │
         ┌────▼────┐              ┌────▼────┐
         │ PostgreSQL│              │ Redis   │
         │ Primary   │              │ Cluster │
         │ + Replicas│              │ (3 nodes)│
         └───────────┘              └─────────┘
```

---

### Infrastructure Dependencies

**Required Services:**

| Service | Version | Purpose | Critical? |
|---------|---------|---------|----------|
| PostgreSQL | 16+ | Primary database | Yes |
| Redis | 7+ | Cache + Queue | Yes |
| Node.js | 22.x | Runtime | Yes |
| AWS ALB / GCP LB | Latest | Load balancing | Yes |
| Prometheus | 2.x | Metrics | No |
| Grafana | 10.x | Dashboards | No |
| Sentry | Latest | Error tracking | No |

**Network Requirements:**
- **Outbound:** HTTPS (443) to Financial System API
- **Inbound:** HTTP (80), HTTPS (443) from load balancer
- **Internal:** PostgreSQL (5432), Redis (6379)
- **Monitoring:** Prometheus (9090)

---

### Disaster Recovery

**Recovery Point Objective (RPO):** < 1 minute
- **Database:** Continuous replication to DR region
- **Redis:** Snapshot every 5 minutes
- **Application:** Stateless (no data loss)

**Recovery Time Objective (RTO):** < 5 minutes
- **Automated failover:** Database and Redis
- **Manual failover:** Application instances (DNS switch)

**Backup Strategy:**

**Database:**
- **Frequency:** Automated snapshots every 6 hours
- **Retention:** 30 days
- **Location:** S3 / Google Cloud Storage (cross-region)
- **Testing:** Monthly restore test

**Redis:**
- **Frequency:** RDB snapshots every 5 minutes
- **Retention:** 7 days
- **Location:** Persistent disk

**Application Config:**
- **Frequency:** On every change
- **Location:** Git repository + secret manager
- **Retention:** Indefinite (version controlled)

---

### Observability Retention Policies

**Logs:**
- **Retention:** 90 days (hot), 1 year (cold storage)
- **Storage:** CloudWatch Logs / Google Cloud Logging
- **Sampling:** 100% for errors, 10% for info

**Metrics:**
- **Retention:** 15 days (1-minute resolution), 1 year (5-minute resolution)
- **Storage:** Prometheus + long-term storage (Thanos / Cortex)

**Distributed Traces:**
- **Retention:** 7 days
- **Sampling:** 5% of requests (100% for errors)
- **Storage:** Jaeger / Google Cloud Trace

---

### API Versioning Strategy

**Versioning Scheme:** URL-based versioning

**Format:** `/api/v{major}/{resource}`

**Examples:**
- `/api/v1/promo-system/redeem`
- `/api/v2/promo-system/redeem`

**Backward Compatibility:**
- **Minor changes:** Additive only (new fields, new endpoints)
- **Major changes:** New version (breaking changes)
- **Deprecation:** 6 months notice, sunset after 12 months

**Version Support:**
- **Current version (v2):** Full support
- **Previous version (v1):** Maintenance mode (bug fixes only)
- **Deprecated versions:** No support

**Migration Path:**
```markdown
1. Announce new version (v2) with migration guide
2. Run v1 and v2 in parallel for 6 months
3. Mark v1 as deprecated (6 months notice)
4. Sunset v1 after 12 months total
```
```

---

## 8. Meta Tags for Critical Sections

### 8.1 Insert Meta Tags

For critical sections, add meta tags:

```markdown
<!-- @critical security -->
## Security Threat Model (STRIDE)
...
<!-- @end-critical -->

<!-- @critical config -->
## Configuration Schema
...
<!-- @end-critical -->

<!-- @critical di -->
## Dependency Injection Pattern
...
<!-- @end-critical -->

<!-- @critical monitoring -->
## Monitoring & Observability
...
<!-- @end-critical -->
```

### 8.2 Benefits

- Precise identification (no keyword guessing)
- Easier restoration
- Clear boundaries
- Allow selective updates with --force-update

---

## 9. Force Update Handling (EDIT mode)

### 9.1 Default Behavior

Preserve all critical sections (v4.0 behavior).

### 9.2 With --force-update=all

Allow updating ANY critical section without restoration.

### 9.3 With --force-update=stride,config

Allow updating ONLY specified sections:
- stride → STRIDE threat model
- config → Configuration schema
- di → DI pattern
- monitoring → Monitoring section

Other critical sections still preserved.

### 9.4 Meta Tag Override

```markdown
<!-- @critical security allow-update -->
## Security Threat Model
...
<!-- @end-critical -->
```

This section can be updated even without --force-update flag.

---

## 10. Consistency Validation (NEW)

If `--validate-consistency` specified:

### 10.1 Check Consistency Rules

**Rule 1: API in Architecture → Must appear in Examples**
```
FOR each API endpoint in Architecture:
  IF NOT found in Examples:
    WARN: "API {endpoint} defined but no example provided"
```

**Rule 2: Queue mentioned → Must have Queue metrics**
```
IF Architecture mentions "queue" OR "worker":
  IF Performance Requirements missing queue metrics:
    ERROR: "Queue mentioned but no queue performance metrics"
```

**Rule 3: Database transactions → Must have Integration Tests**
```
IF mentions "transaction" OR "ACID":
  IF Testing section lacks integration tests:
    WARN: "Transactions mentioned but no integration tests defined"
```

**Rule 4: External API → Must have Retry Policy**
```
IF mentions "external API" OR "third-party":
  IF Implementation Guide lacks retry/backoff:
    WARN: "External API mentioned but no retry policy defined"
```

**Rule 5: Authentication → Must have Security Section**
```
IF mentions "auth" OR "login" OR "JWT":
  IF no Security section:
    ERROR: "Authentication mentioned but no security section"
```

### 10.2 Report Consistency Issues

```
🔍 Consistency Check Results:

❌ ERROR: Authentication mentioned but no security section
⚠️  WARN: API /api/v1/users defined but no example provided
⚠️  WARN: Queue mentioned but no queue performance metrics
✅ PASS: All critical sections present
✅ PASS: Examples cover main features

Summary: 2 errors, 2 warnings, 10 checks passed
```

If errors found and `--validate-consistency` specified:
- Display report
- Ask user to fix or continue anyway

---

## 11. Output Organization (NEW)

### 11.1 Default Structure

```
.smartspec/
├── backups/
│   └── spec-004-financial-system/
│       ├── spec.backup-20251203-1430.md
│       └── spec.backup-20251203-1445.md
├── reports/
│   └── spec-004-financial-system/
│       ├── generation-report-20251203.md
│       └── validation-report-20251203.md
├── registry/
│   └── critical-sections-registry.json
├── config.json
└── trace.log
```

### 11.2 With --no-backup

Skip backups/ directory creation.

### 11.3 With --no-report

Skip reports/ directory creation.

### 11.4 With --output-dir=custom/path

Use custom directory instead of .smartspec/

---

## 12. Configuration File Support (NEW)

### 12.1 .smartspec/smartspec.config.json

```json
{
  "version": "5.0.0",
  "defaults": {
    "profile": "backend-service",
    "mode": "standard",
    "security": "auto",
    "di": "auto",
    "performance": "auto"
  },
  "organization": {
    "name": "Company Name",
    "defaultAuthor": "SmartSpec Architect v5.0"
  },
  "profiles": {
    "backend-service": {
      "includeSections": ["di", "testing", "monitoring"],
      "excludeSections": ["stride-full"],
      "security": "basic",
      "performance": "basic"
    },
    "financial": {
      "includeSections": ["stride-full", "performance-full", "audit"],
      "security": "stride-full",
      "performance": "full",
      "mandatory": ["di", "security", "performance"]
    }
  },
  "domains": {
    "healthcare": {
      "autoInclude": ["privacy", "audit", "realtime"],
      "compliance": ["HIPAA"],
      "performance": "full"
    },
    "iot": {
      "autoInclude": ["throughput", "telemetry"],
      "performance": "full"
    }
  },
  "validation": {
    "enabled": true,
    "rules": {
      "api-example-coverage": "warn",
      "queue-metrics": "error",
      "external-api-retry": "warn"
    }
  },
  "output": {
    "createBackups": true,
    "generateReports": true,
    "outputDir": ".smartspec/"
  }
}
```

### 12.2 Config Priority

1. Command-line flags (highest)
2. Organization config (.smartspec/smartspec.config.json)
3. Built-in defaults (lowest)

---

## 13. Generate SPEC Based on Profile & Flags

### 13.1 Assemble Sections

Based on:
- Selected profile
- Flags (--security, --di, --performance)
- Domain hints
- Config file settings

### 13.1.1 Resolve Spec Dependencies (MANDATORY)

🚨 **CRITICAL: Dependencies MUST include path and repo information** 🚨

**INSTRUCTION FOR AI:**
When generating Related Specs section, you MUST follow these steps:

---

**Step 1: Check if SPEC_INDEX.json exists**

Use `file` tool to check:
```bash
test -f SPEC_INDEX.json && echo "EXISTS" || echo "NOT_EXISTS"
```

---

**Step 2: Load SPEC_INDEX.json (if exists)**

If EXISTS:
```
1. Read SPEC_INDEX.json using `file` tool
2. Parse JSON structure: { "specs": [{ "id": "...", "title": "...", "path": "...", "repo": "..." }] }
3. Store in memory for lookup
```

If NOT_EXISTS:
```
- Show warning in output
- Dependencies will be listed WITHOUT path/repo (fallback mode)
```

---

**Step 3: Extract dependency IDs**

From user input or existing SPEC, extract:
- Core dependencies (e.g., spec-core-001-authentication)
- Feature specs (e.g., spec-002-user-management)
- Infrastructure specs (e.g., spec-infra-001-database)

---

**Step 4: Validate and look up each dependency in SPEC_INDEX.json (Enhanced with Smart Validation)**

**Helper Functions:**

```javascript
// Levenshtein Distance for fuzzy matching
function levenshteinDistance(str1, str2) {
  const len1 = str1.length;
  const len2 = str2.length;
  const matrix = Array(len1 + 1).fill(null).map(() => Array(len2 + 1).fill(0));
  
  for (let i = 0; i <= len1; i++) matrix[i][0] = i;
  for (let j = 0; j <= len2; j++) matrix[0][j] = j;
  
  for (let i = 1; i <= len1; i++) {
    for (let j = 1; j <= len2; j++) {
      const cost = str1[i - 1] === str2[j - 1] ? 0 : 1;
      matrix[i][j] = Math.min(
        matrix[i - 1][j] + 1,      // deletion
        matrix[i][j - 1] + 1,      // insertion
        matrix[i - 1][j - 1] + cost // substitution
      );
    }
  }
  
  return matrix[len1][len2];
}

// Smart Spec Search (4 levels)
function findSpec(dependencyId, SPEC_INDEX) {
  // Level 1: Exact match
  let spec = SPEC_INDEX.specs.find(s => s.id === dependencyId);
  if (spec) {
    return { spec, matchType: 'exact', confidence: 1.0 };
  }
  
  // Level 2: Fuzzy match (typo tolerance)
  const fuzzyMatches = SPEC_INDEX.specs
    .map(s => ({
      spec: s,
      distance: levenshteinDistance(dependencyId.toLowerCase(), s.id.toLowerCase())
    }))
    .filter(m => m.distance <= 3) // Max 3 character difference
    .sort((a, b) => a.distance - b.distance);
  
  if (fuzzyMatches.length > 0) {
    return {
      spec: fuzzyMatches[0].spec,
      matchType: 'fuzzy',
      confidence: 1 - (fuzzyMatches[0].distance / Math.max(dependencyId.length, fuzzyMatches[0].spec.id.length)),
      allMatches: fuzzyMatches.slice(0, 3)
    };
  }
  
  // Level 3: Partial match (substring)
  const partialMatches = SPEC_INDEX.specs
    .filter(s => 
      s.id.toLowerCase().includes(dependencyId.toLowerCase()) || 
      dependencyId.toLowerCase().includes(s.id.toLowerCase())
    )
    .map(s => ({
      spec: s,
      score: Math.max(
        dependencyId.toLowerCase().length / s.id.toLowerCase().length,
        s.id.toLowerCase().length / dependencyId.toLowerCase().length
      )
    }))
    .sort((a, b) => b.score - a.score);
  
  if (partialMatches.length > 0) {
    return {
      spec: partialMatches[0].spec,
      matchType: 'partial',
      confidence: partialMatches[0].score,
      allMatches: partialMatches.slice(0, 3)
    };
  }
  
  // Level 4: Semantic match (title similarity)
  const semanticMatches = SPEC_INDEX.specs
    .map(s => {
      const titleWords = s.title.toLowerCase().split(/[\s-_]+/);
      const depWords = dependencyId.toLowerCase().split(/[\s-_]+/);
      const overlap = depWords.filter(w => titleWords.some(tw => tw.includes(w) || w.includes(tw))).length;
      const score = overlap / Math.max(depWords.length, 1);
      return { spec: s, score };
    })
    .filter(m => m.score > 0.4) // >40% word overlap
    .sort((a, b) => b.score - a.score);
  
  if (semanticMatches.length > 0) {
    return {
      spec: semanticMatches[0].spec,
      matchType: 'semantic',
      confidence: semanticMatches[0].score,
      allMatches: semanticMatches.slice(0, 3)
    };
  }
  
  // Not found
  return { spec: null, matchType: 'none', confidence: 0, allMatches: [] };
}

// Auto-Correction for typos
function autoCorrect(dependencyId, SPEC_INDEX) {
  const candidates = SPEC_INDEX.specs
    .map(spec => ({
      spec: spec,
      distance: levenshteinDistance(dependencyId.toLowerCase(), spec.id.toLowerCase())
    }))
    .filter(c => c.distance <= 2) // Max 2 character difference
    .sort((a, b) => a.distance - b.distance);
  
  if (candidates.length === 0) {
    return { corrected: false };
  }
  
  const best = candidates[0];
  
  if (best.distance === 1 && candidates.length === 1) {
    // High confidence: only 1 candidate, 1 char difference
    return {
      corrected: true,
      confidence: 'high',
      original: dependencyId,
      correctedId: best.spec.id,
      spec: best.spec,
      autoApply: true
    };
  }
  
  if (best.distance <= 2 && candidates.length <= 3) {
    // Medium confidence: few candidates, 1-2 char difference
    return {
      corrected: true,
      confidence: 'medium',
      original: dependencyId,
      suggestions: candidates.slice(0, 3),
      autoApply: false
    };
  }
  
  return { corrected: false };
}

// Deprecated Spec Detection
function validateDeprecated(spec, SPEC_INDEX) {
  if (spec.status !== 'deprecated') {
    return { valid: true, deprecated: false };
  }
  
  // Method 1: Check metadata for replacement_id
  if (spec.metadata?.replacement_id) {
    const replacement = SPEC_INDEX.specs.find(
      s => s.id === spec.metadata.replacement_id
    );
    
    if (replacement) {
      return {
        valid: false,
        deprecated: true,
        replacement: replacement,
        method: 'metadata',
        autoFix: true
      };
    }
  }
  
  // Method 2: Find by version (v1 → v2)
  const versionMatch = spec.id.match(/-v(\d+)$/);
  if (versionMatch) {
    const currentVersion = parseInt(versionMatch[1]);
    const nextVersion = currentVersion + 1;
    const nextId = spec.id.replace(/-v\d+$/, `-v${nextVersion}`);
    
    const replacement = SPEC_INDEX.specs.find(s => s.id === nextId);
    if (replacement) {
      return {
        valid: false,
        deprecated: true,
        replacement: replacement,
        method: 'version',
        autoFix: true
      };
    }
  }
  
  // Method 3: Find by similar title (active status)
  const similarSpecs = SPEC_INDEX.specs
    .filter(s => 
      s.id !== spec.id &&
      s.status === 'active' &&
      levenshteinDistance(s.title.toLowerCase(), spec.title.toLowerCase()) < spec.title.length * 0.3
    )
    .sort((a, b) => new Date(b.updated) - new Date(a.updated));
  
  if (similarSpecs.length > 0) {
    return {
      valid: false,
      deprecated: true,
      replacement: similarSpecs[0],
      method: 'similarity',
      autoFix: false // Need user confirmation
    };
  }
  
  // Deprecated but no replacement found
  return {
    valid: false,
    deprecated: true,
    replacement: null,
    method: 'none',
    autoFix: false
  };
}
```

---

**Enhanced Validation Logic:**

For each dependency ID:
```javascript
console.log(`\n🔍 Validating: ${dependencyId}`);

// Step 1: Smart search
const searchResult = findSpec(dependencyId, SPEC_INDEX);
let finalSpec = searchResult.spec;
let warnings = [];

if (searchResult.matchType === 'exact') {
  console.log(`✅ Exact match found: ${finalSpec.id}`);
  
} else if (searchResult.matchType === 'fuzzy') {
  // Fuzzy match - possible typo
  const correction = autoCorrect(dependencyId, SPEC_INDEX);
  
  if (correction.corrected && correction.confidence === 'high' && FLAGS.auto_fix) {
    // Auto-correct with high confidence
    console.log(`✅ Auto-corrected: "${dependencyId}" → "${correction.correctedId}" (typo detected)`);
    finalSpec = correction.spec;
    warnings.push(`Auto-corrected from ${dependencyId}`);
    
  } else if (correction.corrected && correction.confidence === 'medium') {
    // Ask user to select
    console.log(`💡 Possible typo in "${dependencyId}". Did you mean:`);
    correction.suggestions.forEach((c, i) => {
      console.log(`   ${i+1}. ${c.spec.id} (${c.distance} char difference)`);
    });
    
    if (FLAGS.auto_fix) {
      // Use best match
      finalSpec = correction.suggestions[0].spec;
      console.log(`✅ Using: ${finalSpec.id}`);
      warnings.push(`Auto-selected ${finalSpec.id} (best match)`);
    } else {
      // Interactive mode
      const choice = await askUser('Select option (1-3) or 0 to use original:');
      if (choice > 0 && choice <= correction.suggestions.length) {
        finalSpec = correction.suggestions[choice - 1].spec;
        console.log(`✅ Using: ${finalSpec.id}`);
      } else {
        console.log(`⚠️ Using original: ${dependencyId} (not found)`);
        finalSpec = null;
      }
    }
  } else {
    console.log(`⚠️ Fuzzy match: ${finalSpec.id} (${Math.round(searchResult.confidence * 100)}% confidence)`);
    warnings.push(`Fuzzy match with ${searchResult.confidence.toFixed(2)} confidence`);
  }
  
} else if (searchResult.matchType === 'partial') {
  console.log(`⚠️ Partial match: ${finalSpec.id} (${Math.round(searchResult.confidence * 100)}% confidence)`);
  console.log(`   Original: ${dependencyId}`);
  
  if (!FLAGS.auto_fix) {
    const confirm = await askUser(`Use ${finalSpec.id}? [Y/n]`);
    if (!confirm) {
      finalSpec = null;
    }
  }
  warnings.push(`Partial match - verify correctness`);
  
} else if (searchResult.matchType === 'semantic') {
  console.log(`💡 Semantic match: ${finalSpec.id}`);
  console.log(`   Title: ${finalSpec.title}`);
  console.log(`   Confidence: ${Math.round(searchResult.confidence * 100)}%`);
  
  if (!FLAGS.auto_fix) {
    const confirm = await askUser(`Use ${finalSpec.id}? [Y/n]`);
    if (!confirm) {
      finalSpec = null;
    }
  }
  warnings.push(`Semantic match - verify functionality`);
  
} else {
  // Not found
  console.log(`❌ Not found: ${dependencyId}`);
  finalSpec = null;
}

// Step 2: Validate deprecated (if found)
if (finalSpec) {
  const deprecatedCheck = validateDeprecated(finalSpec, SPEC_INDEX);
  
  if (deprecatedCheck.deprecated) {
    console.log(`⚠️ DEPRECATED: ${finalSpec.id} is deprecated`);
    
    if (deprecatedCheck.replacement) {
      console.log(`✅ Replacement found: ${deprecatedCheck.replacement.id}`);
      console.log(`   Method: ${deprecatedCheck.method}`);
      
      if (deprecatedCheck.autoFix && FLAGS.auto_fix) {
        // Auto-replace
        console.log(`✅ Auto-replacing with ${deprecatedCheck.replacement.id}`);
        finalSpec = deprecatedCheck.replacement;
        warnings.push(`Replaced deprecated spec with ${finalSpec.id}`);
        
      } else if (deprecatedCheck.replacement) {
        // Ask user
        const replace = await askUser(`Use ${deprecatedCheck.replacement.id} instead? [Y/n]`);
        if (replace) {
          finalSpec = deprecatedCheck.replacement;
          console.log(`✅ Using: ${finalSpec.id}`);
        } else {
          warnings.push(`Using deprecated spec ${finalSpec.id}`);
        }
      }
    } else {
      console.log(`❌ No replacement found - manual review required`);
      warnings.push(`Deprecated spec with no replacement`);
    }
  }
}

// Step 3: Handle not found
if (!finalSpec) {
  console.warn(`⚠️ WARNING: ${dependencyId} not found in SPEC_INDEX`);
  console.warn(`⚠️ This spec may not exist or INDEX is stale`);
  
  // Check if --auto-add-refs flag is set
  if (FLAGS.auto_add_refs) {
    const addPlaceholder = await askUser(
      `Add ${dependencyId} to SPEC_INDEX as placeholder? [Y/n]`
    );
    
    if (addPlaceholder) {
      // Add placeholder to SPEC_INDEX
      const placeholder = {
        id: dependencyId,
        title: "[PLACEHOLDER - TO BE CREATED]",
        path: "TBD",
        repo: "unknown",
        status: "placeholder",
        version: "0.0.0",
        created: new Date().toISOString(),
        updated: new Date().toISOString(),
        author: "System",
        dependencies: [],
        dependents: [CURRENT_SPEC_ID],
        metadata: {
          created_by_workflow: "generate_spec",
          reason: "Referenced but not found"
        }
      };
      
      SPEC_INDEX.specs.push(placeholder);
      SPEC_INDEX.metadata.total_specs++;
      SPEC_INDEX.metadata.by_status.placeholder++;
      
      console.log(`✅ Added ${dependencyId} as placeholder`);
      finalSpec = placeholder;
      warnings.push(`Added as placeholder - needs to be created`);
    }
  }
}

// Step 4: Format output
if (finalSpec) {
  const warningStr = warnings.length > 0 ? ` ⚠️ ${warnings.join('; ')}` : '';
  const statusBadge = finalSpec.status === 'placeholder' ? ' [PLACEHOLDER]' : 
                      finalSpec.status === 'deprecated' ? ' [DEPRECATED]' : '';
  
  return `- **${finalSpec.id}**${statusBadge} - ${finalSpec.title} - Spec Path: "${finalSpec.path}/spec.md" Repo: ${finalSpec.repo}${warningStr}`;
} else {
  return `- **${dependencyId}** - [NOT FOUND IN SPEC_INDEX] - Spec Path: "N/A" Repo: unknown ⚠️ Manual review required`;
}

// OLD CODE (replaced by above):
// const spec = SPEC_INDEX.specs.find(s => s.id === dependencyId);

if (spec) {
  // Found in index
  if (spec.status === "placeholder") {
    // Warn about placeholder
    console.warn(`⚠️ WARNING: ${dependencyId} is a placeholder (not yet created)`);
  }
  return `- **${spec.id}** - ${spec.title} - Spec Path: "${spec.path}/spec.md" Repo: ${spec.repo}`;
  
} else {
  // Not found - validate and optionally add placeholder
  console.warn(`⚠️ WARNING: ${dependencyId} not found in SPEC_INDEX`);
  console.warn(`⚠️ This spec may not exist or INDEX is stale`);
  
  // Check if --auto-add-refs flag is set
  if (FLAGS.auto_add_refs) {
    // Ask user to add placeholder
    const addPlaceholder = await askUser(
      `Add ${dependencyId} to SPEC_INDEX as placeholder? [Y/n]`
    );
    
    if (addPlaceholder) {
      // Add placeholder to SPEC_INDEX
      const placeholder = {
        id: dependencyId,
        title: "[PLACEHOLDER - TO BE CREATED]",
        path: "TBD",
        repo: "unknown",
        status: "placeholder",
        version: "0.0.0",
        created: new Date().toISOString(),
        updated: new Date().toISOString(),
        author: "System",
        dependencies: [],
        dependents: [CURRENT_SPEC_ID]
      };
      
      SPEC_INDEX.specs.push(placeholder);
      SPEC_INDEX.metadata.total_specs++;
      SPEC_INDEX.metadata.by_status.placeholder++;
      
      console.log(`✅ Added ${dependencyId} as placeholder`);
      
      return `- **${dependencyId}** - [PLACEHOLDER - TO BE CREATED] - Spec Path: "TBD" Repo: unknown`;
    }
  }
  
  // Not found and not added as placeholder
  return `- **${dependencyId}** - [NOT FOUND IN SPEC_INDEX] - Spec Path: "N/A" Repo: unknown`;
}
```

**Validation Logic:**
1. ✅ If spec found and active → use it
2. ⚠️ If spec found but placeholder → warn user
3. ⚠️ If spec not found → warn user
4. ❓ If --auto-add-refs flag → ask to add placeholder
5. ✅ If user confirms → add placeholder to INDEX
6. ❌ If user declines → continue with "NOT FOUND" marker

---

**Step 5: Format each dependency (MANDATORY FORMAT)**

**✅ CORRECT FORMAT (with path and repo):**
```markdown
- **spec-core-001-authentication** - User authentication for financial operations - Spec Path: "specs/core/spec-core-001-authentication/spec.md" Repo: private
```

**❌ WRONG FORMAT (missing path and repo):**
```markdown
- **spec-core-001-authentication** - User authentication for financial operations
```

---

**Step 6: Group by category**

Group dependencies into sections:
- **Core Dependencies** (category: "core")
- **Feature Specs** (category: "feature")
- **Infrastructure Specs** (category: "infrastructure")

---

**Example output (CORRECT - with SPEC_INDEX.json):**

```markdown
## 8. Related Specs

### Core Dependencies
- **spec-core-001-authentication** - User authentication for financial operations - Spec Path: "specs/core/spec-core-001-authentication/spec.md" Repo: private
- **spec-core-002-authorization** - RBAC for admin financial operations - Spec Path: "specs/core/spec-core-002-authorization/spec.md" Repo: private
- **spec-core-003-audit-logging** - Audit trail for all financial transactions - Spec Path: "specs/core/spec-core-003-audit-logging/spec.md" Repo: private

### Feature Specs
- **spec-002-user-management** - User profile and account management - Spec Path: "specs/feature/spec-002-user-management/spec.md" Repo: public
- **spec-012-subscription-plans** - Subscription plan definitions - Spec Path: "specs/feature/spec-012-subscription-plans/spec.md" Repo: public

### Integration Points
- Payment gateway integration (Stripe, PayPal)
- Message queue for saga orchestration
- Redis for idempotency key storage
```

---

**Example output (FALLBACK - without SPEC_INDEX.json):**

```markdown
⚠️ **Warning:** SPEC_INDEX.json not found. Dependencies listed without path/repo information.

## 8. Related Specs

### Core Dependencies
- **spec-core-001-authentication** - User authentication for financial operations
- **spec-core-002-authorization** - RBAC for admin financial operations

### Feature Specs
- **spec-002-user-management** - User profile and account management
```

---

**Error handling:**

1. **Spec not found in SPEC_INDEX.json:**
   ```markdown
   - **spec-unknown-001** - [NOT FOUND IN SPEC_INDEX] - Spec Path: "N/A" Repo: unknown
   ```

2. **SPEC_INDEX.json doesn't exist:**
   ```markdown
   ⚠️ Warning: SPEC_INDEX.json not found. Dependencies listed without path/repo information.
   ```

3. **SPEC_INDEX.json is malformed:**
   ```markdown
   ⚠️ Error: SPEC_INDEX.json is malformed. Please fix the JSON syntax.
   ```

---

**⚠️ IMPORTANT REMINDERS:**

1. ✅ ALWAYS try to load SPEC_INDEX.json first
2. ✅ ALWAYS include "Spec Path" and "Repo" in dependency format
3. ✅ Use EXACT format: `- **{id}** - {description} - Spec Path: "{path}/spec.md" Repo: {repo}`
4. ✅ Group by category (Core, Feature, Infrastructure)
5. ✅ Show warning if SPEC_INDEX.json not found
6. ❌ NEVER output dependencies without path/repo unless SPEC_INDEX.json doesn't exist

### 13.1.2 Generate Data Model Section (NEW - Financial Profile Only)

If profile is `financial`, automatically include Data Model & Schema section:

**Section Structure:**
```markdown
## {N}. Data Model & Schema

### {N}.1 Core Tables

#### Ledger Table
```sql
CREATE TABLE ledger (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL,
  transaction_type VARCHAR(50) NOT NULL, -- CREDIT, DEBIT, REFUND
  amount DECIMAL(19,4) NOT NULL,
  balance_after DECIMAL(19,4) NOT NULL,
  reference_id UUID, -- Link to payment/invoice/transaction
  description TEXT,
  metadata JSONB,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  created_by UUID NOT NULL,
  
  -- Immutability & Tamper Detection
  is_immutable BOOLEAN DEFAULT TRUE,
  hash VARCHAR(64), -- SHA-256 for tamper detection
  previous_hash VARCHAR(64), -- Link to previous entry (blockchain-style)
  
  -- Indexes
  INDEX idx_ledger_user_id (user_id),
  INDEX idx_ledger_created_at (created_at),
  INDEX idx_ledger_reference_id (reference_id)
);
```

#### Credit Balance Table
```sql
CREATE TABLE credit_balance (
  user_id UUID PRIMARY KEY,
  balance DECIMAL(19,4) NOT NULL DEFAULT 0 CHECK (balance >= 0),
  reserved_balance DECIMAL(19,4) NOT NULL DEFAULT 0 CHECK (reserved_balance >= 0),
  available_balance DECIMAL(19,4) GENERATED ALWAYS AS (balance - reserved_balance) STORED,
  last_updated TIMESTAMP NOT NULL DEFAULT NOW(),
  version INT NOT NULL DEFAULT 1, -- Optimistic locking
  
  -- Constraints
  CONSTRAINT chk_balance_non_negative CHECK (balance >= reserved_balance)
);
```

#### Invoice Table
```sql
CREATE TABLE invoice (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL,
  invoice_number VARCHAR(50) UNIQUE NOT NULL,
  amount DECIMAL(19,4) NOT NULL,
  tax DECIMAL(19,4) NOT NULL DEFAULT 0,
  total DECIMAL(19,4) NOT NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'DRAFT', -- DRAFT, ISSUED, PAID, VOID, OVERDUE
  due_date DATE NOT NULL,
  issued_at TIMESTAMP,
  paid_at TIMESTAMP,
  voided_at TIMESTAMP,
  metadata JSONB,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
  
  -- Indexes
  INDEX idx_invoice_user_id (user_id),
  INDEX idx_invoice_status (status),
  INDEX idx_invoice_due_date (due_date)
);
```

#### Transaction Log (Audit Trail)
```sql
CREATE TABLE transaction_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  transaction_id UUID NOT NULL,
  event_type VARCHAR(50) NOT NULL, -- CREATED, UPDATED, COMPLETED, FAILED, REFUNDED
  user_id UUID NOT NULL,
  amount DECIMAL(19,4),
  status VARCHAR(20) NOT NULL,
  metadata JSONB,
  
  -- Audit Information
  ip_address INET,
  user_agent TEXT,
  request_id VARCHAR(100),
  
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  
  -- Indexes
  INDEX idx_txlog_transaction_id (transaction_id),
  INDEX idx_txlog_user_id (user_id),
  INDEX idx_txlog_created_at (created_at)
) PARTITION BY RANGE (created_at);
```

#### Saga State Table
```sql
CREATE TABLE saga_state (
  saga_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  saga_type VARCHAR(50) NOT NULL, -- CREDIT_PURCHASE, REFUND, PAYMENT, etc.
  current_step VARCHAR(50) NOT NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'PENDING', -- PENDING, COMPLETED, FAILED, COMPENSATING, COMPENSATED
  payload JSONB NOT NULL,
  compensation_data JSONB,
  error_message TEXT,
  retry_count INT NOT NULL DEFAULT 0,
  max_retries INT NOT NULL DEFAULT 3,
  
  started_at TIMESTAMP NOT NULL DEFAULT NOW(),
  completed_at TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
  
  -- Indexes
  INDEX idx_saga_type (saga_type),
  INDEX idx_saga_status (status),
  INDEX idx_saga_started_at (started_at)
);
```

### {N}.2 ER Diagram

```mermaid
erDiagram
    USER ||--o{ CREDIT_BALANCE : has
    USER ||--o{ LEDGER : records
    USER ||--o{ INVOICE : receives
    USER ||--o{ TRANSACTION_LOG : generates
    
    CREDIT_BALANCE {
        uuid user_id PK
        decimal balance
        decimal reserved_balance
        decimal available_balance
        int version
    }
    
    LEDGER {
        uuid id PK
        uuid user_id FK
        string transaction_type
        decimal amount
        decimal balance_after
        uuid reference_id
        string hash
        string previous_hash
    }
    
    INVOICE {
        uuid id PK
        uuid user_id FK
        string invoice_number UK
        decimal amount
        decimal tax
        decimal total
        string status
        date due_date
    }
    
    TRANSACTION_LOG {
        uuid id PK
        uuid transaction_id
        uuid user_id FK
        string event_type
        string status
        inet ip_address
    }
    
    SAGA_STATE {
        uuid saga_id PK
        string saga_type
        string current_step
        string status
        jsonb payload
        jsonb compensation_data
    }
    
    INVOICE ||--o{ LEDGER : generates
    SAGA_STATE ||--o{ TRANSACTION_LOG : tracks
```

### {N}.3 Data Integrity Rules

1. **Ledger Immutability**
   - No UPDATE or DELETE operations allowed
   - All entries are append-only
   - Hash chain ensures tamper detection

2. **Balance Consistency**
   - `available_balance = balance - reserved_balance`
   - All balance updates must be atomic
   - Optimistic locking prevents race conditions

3. **Audit Trail Completeness**
   - Every financial operation must create transaction log entry
   - Logs are partitioned by month for performance
   - Retention: 7 years (compliance requirement)

4. **Saga Reliability**
   - All saga steps must be idempotent
   - Compensation data stored for rollback
   - Automatic retry with exponential backoff
```

**Customization:**
- Adjust table names based on SPEC context
- Add domain-specific tables (e.g., Payment, Subscription)
- Include additional indexes based on query patterns
- Add partitioning strategy for high-volume tables

### 13.2 Apply Meta Tags

Insert meta tags for critical sections.

### 13.3 Apply Mode

If compact mode: condense to 5 sections.
If standard mode: full detail.

### 13.4 Run Validation

If --validate-consistency: check rules.

### 13.5 Write Output

#### 13.5.1 Backup Existing SPEC (MANDATORY - MUST EXECUTE WITH PROOF)

🚨 **CRITICAL: This step MUST be executed before writing new spec.md** 🚨

🔍 **PROOF REQUIRED: You MUST show actual command outputs, not just say "done"** 🔍

---

**INSTRUCTION FOR AI:**

You MUST perform the following backup steps using `shell` tool.

**⚠️ CRITICAL RULE: You MUST show the actual output from EVERY command below.**

**❌ DO NOT just say "Backup created" without showing proof.**
**❌ DO NOT just write "✅ Backup verified" without showing actual output.**
**✅ DO show the exact commands and their outputs.

---

**Step 1: Check if spec.md exists**

Execute using `shell` tool:
```bash
test -f spec.md && echo "EXISTS" || echo "NOT_EXISTS"
```

**👉 SHOW THE OUTPUT HERE in your response.**

If output is "NOT_EXISTS", skip to section 13.5.2.
If output is "EXISTS", proceed to Step 2.

---

**Step 2: Create backup directory and verify**

Execute using `shell` tool:
```bash
mkdir -p .smartspec/backups && ls -la .smartspec/ | grep backups
```

**👉 SHOW THE OUTPUT HERE in your response.**

You should see a line showing `backups` directory.

---

**Step 3: Create backup with timestamp**

Execute using `shell` tool:
```bash
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
BACKUP_FILE="spec.backup-${TIMESTAMP}.md"
cp spec.md ".smartspec/backups/${BACKUP_FILE}"
echo "📁 Backup filename: ${BACKUP_FILE}"
```

**👉 SHOW THE OUTPUT HERE in your response.**

You should see: `📁 Backup filename: spec.backup-YYYYMMDD-HHMMSS.md`

---

**Step 4: Verify backup was created (MANDATORY PROOF)**

🚨 **THIS IS THE MOST CRITICAL STEP** 🚨

Execute ALL of these commands using `shell` tool and show ALL outputs:

```bash
# Command 1: List all backup files with details
echo "=== Backup files ==="
ls -lh .smartspec/backups/

# Command 2: Verify specific backup exists
echo "=== Verification ==="
test -f ".smartspec/backups/${BACKUP_FILE}" && echo "✅ BACKUP FILE EXISTS" || echo "❌ BACKUP FILE NOT FOUND"

# Command 3: Show file size
echo "=== File size ==="
du -h ".smartspec/backups/${BACKUP_FILE}"

# Command 4: Show first 5 lines to prove it's the correct file
echo "=== First 5 lines of backup ==="
head -n 5 ".smartspec/backups/${BACKUP_FILE}"
```

**👉 SHOW THE OUTPUT FROM ALL 4 COMMANDS HERE in your response.**

**CRITICAL VALIDATION:**

You MUST see:
1. ✅ List of backup files (from `ls -lh`)
2. ✅ Message "✅ BACKUP FILE EXISTS" (NOT "❌ BACKUP FILE NOT FOUND")
3. ✅ File size (e.g., "24K")
4. ✅ First 5 lines of the backup file

If you see "❌ BACKUP FILE NOT FOUND" or any command fails:
1. ❌ STOP immediately
2. ❌ DO NOT proceed to section 13.5.2
3. ❌ DO NOT write new spec.md
4. ❌ Report error to user: "Backup failed. Cannot proceed."
5. ❌ Exit with error

---

**Step 5: Cleanup old backups (keep last 10)**

Optional but recommended:
```bash
cd .smartspec/backups && ls -t spec.backup-*.md | tail -n +11 | xargs -r rm 2>/dev/null
echo "🗑️  Cleanup: Keeping last 10 backups"
ls -lh
cd ../..
```

**👉 You may show the output if you execute this step.**

---

---

**✅ PROOF CHECKLIST (MUST COMPLETE BEFORE PROCEEDING):**

Before you proceed to section 13.5.2, verify you have shown:

- [ ] ✅ Output from Step 1: "EXISTS" or "NOT_EXISTS"
- [ ] ✅ Output from Step 2: Directory listing showing `backups`
- [ ] ✅ Output from Step 3: Backup filename (e.g., `spec.backup-20251204-000859.md`)
- [ ] ✅ Output from Step 4 Command 1: List of backup files
- [ ] ✅ Output from Step 4 Command 2: "✅ BACKUP FILE EXISTS"
- [ ] ✅ Output from Step 4 Command 3: File size
- [ ] ✅ Output from Step 4 Command 4: First 5 lines of backup

**If you cannot check ALL boxes above, GO BACK and execute the commands properly.**

---

**⚠️ CRITICAL REMINDERS:**

1. ✅ ALWAYS use `shell` tool to execute commands
2. ✅ ALWAYS show actual output from commands
3. ✅ NEVER just say "done" without showing proof
4. ✅ NEVER proceed if "❌ BACKUP FILE NOT FOUND"
5. ✅ NEVER skip backup unless user provides --no-backup flag
6. ❌ DO NOT write new spec.md if backup fails

---

**🔍 SELF-CHECK BEFORE PROCEEDING:**

Ask yourself:
1. Did I execute commands using `shell` tool? (Not just read the instructions)
2. Did I show actual output? (Not just say "Backup created")
3. Did I see "✅ BACKUP FILE EXISTS"? (Not "❌ BACKUP FILE NOT FOUND")
4. Did I show first 5 lines of backup file? (Proof it's the correct file)

If answer is NO to ANY question:
- ❌ STOP
- ❌ GO BACK
- ❌ Execute properly
- ❌ DO NOT proceed to section 13.5.2

---

**Skip backup (only if user explicitly requests):**

If user provides `--no-backup` flag, you may skip this entire section.
Otherwise, backup is MANDATORY.

---

**⚠️ IMPORTANT REMINDERS (LEGACY - REPLACED BY ABOVE):**

1. ✅ ALWAYS backup before writing new spec.md
2. ✅ VERIFY backup was created successfully
3. ✅ DO NOT proceed if backup fails
4. ✅ Use actual shell commands or file operations
5. ✅ Show backup filename in output
6. ❌ NEVER skip backup unless --no-backup flag provided

---

#### 13.5.2 Write New SPEC

Write generated content to spec.md:
```typescript
fs.writeFileSync(specPath, generatedContent, 'utf-8');
console.log(`✅ SPEC written: ${specPath}`);
```

---

#### 13.5.3 Generate Report (optional)

If `--no-report` not specified:
```typescript
const reportDir = path.join(specDir, '.smartspec/reports');
fs.mkdirSync(reportDir, { recursive: true });

const reportPath = path.join(reportDir, 'generation-report.md');
fs.writeFileSync(reportPath, reportContent, 'utf-8');
```

---

## 14. Update SPEC_INDEX.json (Auto-Update)

**After spec generation, automatically update SPEC_INDEX.json**

### 14.1 Load Current SPEC_INDEX

```javascript
const indexPath = 'SPEC_INDEX.json';
const specIndex = JSON.parse(fs.readFileSync(indexPath, 'utf-8'));
```

### 14.2 Find or Create Entry

```javascript
const specId = GENERATED_SPEC.id; // e.g., "spec-core-001"
let specEntry = specIndex.specs.find(s => s.id === specId);

if (!specEntry) {
  // New spec - create entry
  specEntry = {
    id: specId,
    title: GENERATED_SPEC.title,
    path: GENERATED_SPEC.path, // Relative path to spec directory
    repo: GENERATED_SPEC.repo || "private",
    status: GENERATED_SPEC.status || "draft",
    version: GENERATED_SPEC.version,
    created: new Date().toISOString(),
    updated: new Date().toISOString(),
    author: GENERATED_SPEC.author,
    dependencies: GENERATED_SPEC.dependencies || [],
    dependents: []
  };
  
  specIndex.specs.push(specEntry);
  console.log(`✅ Added ${specId} to SPEC_INDEX`);
  
} else {
  // Existing spec - update entry
  specEntry.title = GENERATED_SPEC.title;
  specEntry.path = GENERATED_SPEC.path;
  specEntry.status = GENERATED_SPEC.status || specEntry.status;
  specEntry.version = GENERATED_SPEC.version;
  specEntry.updated = new Date().toISOString();
  specEntry.author = GENERATED_SPEC.author;
  specEntry.dependencies = GENERATED_SPEC.dependencies || [];
  // Keep: id, repo, created, dependents (calculated separately)
  
  console.log(`✅ Updated ${specId} in SPEC_INDEX`);
}
```

### 14.3 Update Metadata

```javascript
// Update total count
specIndex.metadata.total_specs = specIndex.specs.length;

// Update by_status counts
const byStatus = {};
for (const spec of specIndex.specs) {
  byStatus[spec.status] = (byStatus[spec.status] || 0) + 1;
}
specIndex.metadata.by_status = byStatus;

// Update by_repo counts
const byRepo = {};
for (const spec of specIndex.specs) {
  byRepo[spec.repo] = (byRepo[spec.repo] || 0) + 1;
}
specIndex.metadata.by_repo = byRepo;

// Update last_updated
specIndex.last_updated = new Date().toISOString();

console.log(`✅ Updated SPEC_INDEX metadata`);
```

### 14.4 Recalculate Dependents

```javascript
// Clear all dependents
for (const spec of specIndex.specs) {
  spec.dependents = [];
}

// Recalculate dependents
for (const spec of specIndex.specs) {
  for (const depId of spec.dependencies) {
    const depSpec = specIndex.specs.find(s => s.id === depId);
    if (depSpec && !depSpec.dependents.includes(spec.id)) {
      depSpec.dependents.push(spec.id);
    }
  }
}

console.log(`✅ Recalculated dependents`);
```

### 14.5 Save SPEC_INDEX

```javascript
fs.writeFileSync(
  indexPath,
  JSON.stringify(specIndex, null, 2),
  'utf-8'
);

console.log(`✅ Saved SPEC_INDEX.json`);
```

### 14.6 Log Summary

```
✅ SPEC_INDEX.json updated:
- Spec: ${specId}
- Action: ${specEntry.created === specEntry.updated ? 'Added' : 'Updated'}
- Total specs: ${specIndex.metadata.total_specs}
- Dependencies: ${specEntry.dependencies.length}
- Dependents: ${specEntry.dependents.length}
```

---

## 15. Report Output

### 15.1 Standard Report (Thai)

```
✅ สร้าง SPEC เรียบร้อยแล้ว

📁 ไฟล์: specs/feature/spec-004-financial-system/spec.md
📊 Profile: financial
🎛️ Mode: standard
✍️ Author: SmartSpec Architect v5.0

📚 Sections Generated: 13
  ✅ Security: STRIDE-Full (auto-included from profile)
  ✅ Performance: Full metrics (auto-included from profile)
  ✅ DI Pattern: Full (mandatory for backend)
  
🔍 Consistency Check: 10/10 passed

💾 Backup: .smartspec/backups/spec-004.../spec.backup-20251203.md
📄 Report: .smartspec/reports/spec-004.../generation-report.md

🎯 ใช้ flags:
- Profile: financial (comprehensive)
- Security: stride-full (auto from profile)
- Performance: full (auto from profile)
- DI: full (mandatory)

⚙️ Customization available:
- Change profile: --profile=backend-service
- Reduce security: --security=stride-basic
- Compact mode: --mode=compact
- Skip DI: --no-di (not recommended for backend)

🔄 Next steps:
1. Review SPEC
2. Generate plan: smartspec generate-plan spec.md
3. Generate tasks: smartspec generate-tasks spec.md
```

### 14.2 Compact Mode Report

```
✅ สร้าง SPEC (Compact) เรียบร้อยแล้ว

📁 ไฟล์: specs/tools/admin-report/spec.md
📊 Profile: basic
🎛️ Mode: compact (5 sections only)

📚 Sections: 5
  1. Overview
  2. Architecture Summary
  3. API Specification
  4. Constraints & Risks
  5. Acceptance Tests

⚡ Quick & Simple - ใช้สำหรับ:
- Internal tools
- Simple CRUD
- Prototypes
- Quick documentation

🎯 To expand:
smartspec regenerate spec.md --mode=standard --profile=backend-service
```

---

## 15. Examples

### Example 1: Simple CRUD Tool

```bash
smartspec new report-exporter \
  --profile=basic \
  --mode=compact \
  --no-di
```

**Result:** 5-section compact SPEC, no DI, no performance, no security.

---

### Example 2: Standard Microservice

```bash
smartspec new user-service \
  --profile=backend-service \
  --security=basic
```

**Result:** Standard backend SPEC with DI, testing, monitoring, basic security.

---

### Example 3: Financial System

```bash
smartspec new payment-processing \
  --profile=financial \
  --domain=fintech
```

**Result:** Complete SPEC with STRIDE-full, performance-full, audit logging, compliance notes.

---

### Example 4: IoT Telemetry

```bash
smartspec new telemetry-ingestion \
  --profile=backend-service \
  --domain=iot \
  --performance=full
```

**Result:** Backend SPEC with IoT-specific throughput requirements, telemetry patterns.

---

### Example 5: Healthcare API

```bash
smartspec new patient-records-api \
  --profile=backend-service \
  --domain=healthcare \
  --security=stride-full
```

**Result:** Backend SPEC with HIPAA compliance notes, privacy requirements, audit logging, full STRIDE.

---

### Example 6: Update with Force

```bash
smartspec edit specs/feature/spec-004/spec.md \
  --force-update=stride,config
```

**Result:** Allow updating STRIDE and Config sections, preserve other critical sections.

---

## Appendix A: Flag Reference

```
Profiles:
  --profile=basic|backend-service|financial|full

Modes:
  --mode=standard|compact

Security:
  --security=none|basic|stride-basic|stride-full|auto

DI Pattern:
  --di=none|minimal|full|auto
  --no-di (shorthand for --di=none)

Performance:
  --performance=none|basic|full|auto

Domain Hints:
  --domain=healthcare|iot|logistics|ai|fintech|saas|internal

Force Update:
  --force-update=all|stride,config,di,monitoring

Output Control:
  --no-backup
  --no-report
  --output-dir=<path>

Validation:
  --validate-consistency
  --no-validation

Other:
  --specindex=<path>
  --nogenerate (dry run)
```

---

## Appendix B: Profile Comparison

| Feature | basic | backend-service | financial | full |
|---------|-------|-----------------|-----------|------|
| Sections | 5 | 10 | 13+ | All |
| DI Pattern | ❌ | ✅ | ✅ | Auto |
| Security | Optional | Basic | STRIDE-Full | Auto |
| Performance | ❌ | Basic | Full | Auto |
| Testing | Minimal | Standard | Comprehensive | Full |
| Use Case | Simple tools | Most services | Critical systems | Backward compat |

---

Context: $ARGUMENTS
