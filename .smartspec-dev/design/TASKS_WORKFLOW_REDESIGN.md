# Tasks Workflow Redesign

## ปัญหาที่พบ

### 1. ความไม่สมบูรณ์ (~45% coverage)

**ครอบคลุมดี (90-100%):**
- Foundation / Server / Infra

**ครอบคลุมไม่เพียงพอ (5-30%):**
- ❌ Credit core flows (20%)
- ❌ Payment flows (10%)
- ❌ Billing system (10%)
- ❌ Cost analytics (5%)
- ❌ Security (MFA, RBAC, compliance) (30%)
- ❌ APIs (public/internal) (10%)
- ❌ DB schema & migrations (25%)

### 2. Missing Components

**2.1 Business Logic:**
- Credit operations (reserve, commit, release)
- Payment flows
- Billing cycles
- Invoice generation
- Cost analytics
- Fraud prevention

**2.2 API Endpoints:**
- Public user APIs (balance, transaction history)
- Admin APIs (manual adjustment, refunds)
- Billing APIs (invoice, subscription)
- Payment webhook handlers

**2.3 Security:**
- MFA enforcement
- Role & permission middleware
- Audit trail for financial events
- Security monitoring automation

**2.4 Database:**
- Full DB schema creation (15+ tables)
- Migration tasks
- Indexing & partitioning

**2.5 Testing:**
- End-to-end credit/payment scenario tests
- Permission tests for each endpoint
- Fraud scenario tests

### 3. โครงสร้างไม่ชัดเจน

**ปัญหา:**
- ไม่มีการแยก Phase ชัดเจน
- Tasks ไม่มี checkbox `- [ ]`
- ไม่มี Task ID (T001, T002, ...)
- ไม่มี time estimate
- ไม่มี subtasks สำหรับงานใหญ่
- ไม่มีการป้องกัน context overflow

---

## โครงสร้างที่ถูกต้อง

### Format Template

```markdown
## Phase N: Phase Name (Week X-Y)

### Overview
Brief description of this phase's goals and deliverables.

### Prerequisites
- List of dependencies from previous phases

### Tasks

#### TN01: Task Name (Xh)
**Description:** Clear, specific description
**Acceptance Criteria:**
- [ ] Criterion 1
- [ ] Criterion 2

**Subtasks:**
- [ ] TN01.1: Subtask 1 (2h)
- [ ] TN01.2: Subtask 2 (3h)

**Dependencies:** T001, T002
**Files:** `path/to/file.ts`
```

### Task Sizing Rules

**Small Task (2-4h):**
- Single file or function
- Clear input/output
- No external dependencies

**Medium Task (4-8h):**
- Multiple related files
- Some integration work
- 2-3 subtasks

**Large Task (8-16h):**
- Multiple components
- Complex integration
- MUST break into 4-6 subtasks

**Too Large (>16h):**
- ❌ NOT ALLOWED
- MUST split into multiple tasks

### Context Overflow Prevention

**Rules:**
1. Each task MUST fit in <10K tokens context
2. If task requires reading >5 files, split it
3. If task has >6 subtasks, split it
4. If task description >500 words, split it

---

## Required Phases (10 phases)

### Phase 1: Foundation & Setup (Week 1)
- Infrastructure setup
- Database setup
- Basic auth
- Logging & monitoring

### Phase 2: Database Schema & Core Models (Week 2)
- All 15+ tables
- Migrations
- Prisma schema
- Seed data

### Phase 3: Authentication & Authorization (Week 3)
- JWT implementation
- RBAC middleware
- Permission matrix
- MFA enforcement

### Phase 4: Credit Management Core (Week 4-5)
- Credit balance service
- Reserve/Commit/Release flows
- Transaction ledger
- Idempotency

### Phase 5: Payment Integration (Week 6-7)
- Payment gateway integration
- Payment intent flow
- Webhook handlers
- Refund system

### Phase 6: Billing System (Week 8-9)
- Billing cycle engine
- Invoice generation
- Subscription management
- Payment method management

### Phase 7: Cost Management & Analytics (Week 10-11)
- Cost tracking
- Analytics pipeline
- Reporting APIs
- Forecasting

### Phase 8: Security & Compliance (Week 12-13)
- Audit logging
- Security monitoring
- Fraud detection
- Compliance checks (PCI DSS)

### Phase 9: API Layer & Integration (Week 14-15)
- Public APIs
- Admin APIs
- Internal APIs
- API documentation

### Phase 10: Testing & Deployment (Week 16)
- Integration tests
- E2E tests
- Performance tests
- Deployment automation

---

## Task Numbering Convention

```
TPNN: Task ID
│││
││└─ Task number within phase (01-99)
│└── Phase number (1-9, A for 10+)
└─── Task prefix
```

**Examples:**
- T101: Phase 1, Task 01
- T215: Phase 2, Task 15
- TA03: Phase 10, Task 03

---

## Acceptance Criteria Format

Each task MUST have clear acceptance criteria:

```markdown
**Acceptance Criteria:**
- [ ] Functionality: Feature works as specified
- [ ] Tests: Unit tests pass (>80% coverage)
- [ ] Documentation: Code comments and README updated
- [ ] Security: No security vulnerabilities
- [ ] Performance: Meets performance targets
```

---

## Subtask Breakdown Rules

**When to create subtasks:**
1. Task > 8h
2. Task involves >3 files
3. Task has multiple logical steps
4. Task requires multiple skills (DB + API + Tests)

**Subtask format:**
```markdown
- [ ] TXXX.1: Subtask name (2h)
  - Description
  - Files: `path/to/file.ts`
```

---

## Dependencies Management

**Format:**
```markdown
**Dependencies:**
- T101: Database setup (must complete first)
- T102: Auth middleware (parallel OK)
- spec-core-001: Authentication spec
```

**Types:**
- **Blocking:** Must complete before this task
- **Parallel:** Can work simultaneously
- **Spec:** External spec dependency

---

## Progress Tracking

**Checkbox states:**
- `- [ ]` Not started
- `- [x]` Completed
- `- [~]` In progress (optional)
- `- [!]` Blocked (optional)

**Metadata:**
```markdown
## Progress Summary

**Overall:** 45/100 tasks (45%)

**By Phase:**
- Phase 1: 7/7 (100%) ✅
- Phase 2: 12/15 (80%)
- Phase 3: 0/10 (0%)
...
```

---

## Example: Complete Task

```markdown
#### T401: Implement Credit Reserve Flow (8h)

**Description:**
Implement the credit reservation flow that temporarily locks user credits for pending operations. This ensures credits cannot be double-spent while waiting for transaction confirmation.

**Acceptance Criteria:**
- [ ] Reserve API endpoint implemented
- [ ] Reserved balance tracked separately from available balance
- [ ] Automatic release after timeout (configurable)
- [ ] Idempotency key support
- [ ] Unit tests (>85% coverage)
- [ ] Integration tests for reserve/commit/release flow
- [ ] API documentation updated

**Subtasks:**
- [ ] T401.1: Create reserve() method in CreditService (2h)
  - Files: `src/services/credit.service.ts`
  - Logic: Check balance, create reservation record, update reserved_balance
- [ ] T401.2: Implement reservation timeout worker (2h)
  - Files: `src/workers/credit-reservation-timeout.worker.ts`
  - Logic: BullMQ job to auto-release expired reservations
- [ ] T401.3: Add reserve API endpoint (2h)
  - Files: `src/routes/credit.routes.ts`, `src/controllers/credit.controller.ts`
  - Endpoint: POST /api/v1/credit/reserve
- [ ] T401.4: Write tests (2h)
  - Files: `tests/credit-reserve.test.ts`
  - Coverage: Happy path, insufficient balance, timeout, idempotency

**Dependencies:**
- T301: RBAC middleware (must complete)
- T201: Credit balance table (must complete)
- T104: BullMQ setup (must complete)
- spec-004: Financial system spec

**Files:**
- `src/services/credit.service.ts`
- `src/workers/credit-reservation-timeout.worker.ts`
- `src/routes/credit.routes.ts`
- `src/controllers/credit.controller.ts`
- `tests/credit-reserve.test.ts`

**Related Specs:**
- spec-004-financial-system/spec.md (Section 4.2: Credit Operations)
```

---

## Summary

**Key Improvements:**
1. ✅ Complete 10-phase structure
2. ✅ 100+ tasks covering all SPEC requirements
3. ✅ Clear task format with checkboxes
4. ✅ Task IDs and time estimates
5. ✅ Subtasks for large tasks
6. ✅ Acceptance criteria for each task
7. ✅ Dependencies tracking
8. ✅ Context overflow prevention
9. ✅ Progress tracking
10. ✅ Clear, actionable descriptions
