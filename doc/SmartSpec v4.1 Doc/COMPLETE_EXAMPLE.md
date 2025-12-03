# Complete Example - SmartSpec v4.0

**Scenario:** Building a complete payment processing system from scratch

**Time Required:** ~30 minutes (excluding implementation)

---

## Overview

This example walks through the **entire SmartSpec workflow** for a real-world project:

**Project:** Payment Processing System  
**Features:**
- Stripe integration
- Credit/debit card processing
- Subscription management
- Payment history
- Refunds

---

## Phase 1: Create Specification (5 minutes)

### Input

```
"Create a payment processing system with Stripe integration. 
Need to support:
- One-time payments
- Subscription billing
- Payment history
- Refund processing
- Webhook handling
- PCI compliance

Technology: Node.js, TypeScript, PostgreSQL, Stripe API"
```

### Execute

```bash
smartspec_generate_spec_v4
# Paste the input above
```

### Output

**File Created:** `specs/feature/spec-005-payment-system/spec.md`

**Contents Preview:**
```markdown
# SPEC-005: Payment Processing System

**Status:** DRAFT
**Version:** 1.0.0
**Author:** SmartSpec Architect v4.0
**Created:** 2025-12-03
**Last Updated:** 2025-12-03

---

## Overview

**Purpose:** Integrate Stripe payment processing for one-time and subscription payments

**Scope:**
- Payment processing (cards only)
- Subscription management
- Refund handling
- Webhook processing
- PCI compliance

**Non-Goals:**
- PayPal integration
- Cryptocurrency payments
- Invoice generation

**Key Features:**
- Stripe integration
- Secure payment processing
- Subscription billing
- Payment history tracking
- Automated refunds

---

## Technology Stack

**Stack B:** Node.js + TypeScript + PostgreSQL

**Core Technologies:**
- **Runtime:** Node.js 18 LTS
- **Framework:** Express 4.18
- **Language:** TypeScript 5.0
- **Database:** PostgreSQL 14
- **Payment Gateway:** Stripe API v2023-10-16

---

## Architecture

### Components

1. **Payment Service**
   - Process payments
   - Handle Stripe API calls
   - Validate payment methods

2. **Subscription Service**
   - Manage subscriptions
   - Handle billing cycles
   - Process renewals

3. **Webhook Handler**
   - Receive Stripe events
   - Process webhooks
   - Update payment status

4. **Database Layer**
   - Store payment records
   - Track subscriptions
   - Audit trail

---

## Implementation Guide

### Prerequisites
- Stripe account (test mode)
- Node.js 18+
- PostgreSQL 14+

### Configuration
- Stripe API keys (secret + publishable)
- Webhook signing secret
- Database connection

### Security
- **PCI Compliance:** Never store card details
- **Webhook Verification:** Verify Stripe signatures
- **API Keys:** Environment variables only

---

## Examples

### Example 1: One-Time Payment
```typescript
const payment = await processPayment({
  amount: 5000,  // $50.00
  currency: 'usd',
  customerId: 'cus_xxx',
  paymentMethod: 'pm_xxx'
});
```

### Example 2: Create Subscription
```typescript
const subscription = await createSubscription({
  customerId: 'cus_xxx',
  planId: 'price_xxx',
  trialDays: 14
});
```

---

## Related Specs

- **spec-core-001** - Authentication
- **spec-feature-002** - User Management
```

✅ **Spec Created Successfully**

---

## Phase 2: Generate Project Plan (3 minutes)

### Execute

```bash
smartspec_generate_plan specs/feature/spec-005-payment-system/spec.md
```

### Output

**File Created:** `specs/feature/spec-005-payment-system/plan.md`

**Contents Preview:**
```markdown
# Project Plan - Payment Processing System

**Generated:** 2025-12-03 14:30
**Author:** SmartSpec Architect v4.0
**Timeline:** 8 weeks
**Team Size:** 3-4 people

---

## Executive Summary

**Objective:** Build Stripe-integrated payment system  
**Duration:** 8 weeks  
**Critical Path:** Stripe integration → Webhook handling → Testing

---

## Milestones

### Milestone 1: Foundation (Weeks 1-2)
**Deliverables:**
- Database schema
- Core models (Payment, Subscription, Customer)
- Stripe API integration setup

**Success Criteria:**
- Can connect to Stripe test mode
- Database migrations complete
- Models defined

### Milestone 2: Payment Processing (Weeks 3-4)
**Deliverables:**
- One-time payment endpoint
- Payment validation
- Error handling
- Basic tests

**Success Criteria:**
- Can process test payments
- Proper error handling
- 80% test coverage

### Milestone 3: Subscriptions (Weeks 5-6)
**Deliverables:**
- Subscription management
- Billing cycle handling
- Subscription webhooks

**Success Criteria:**
- Can create/cancel subscriptions
- Webhooks processed correctly
- Billing cycles automated

### Milestone 4: Polish & Deploy (Weeks 7-8)
**Deliverables:**
- Full test coverage
- PCI compliance review
- Production deployment
- Documentation

**Success Criteria:**
- Test coverage ≥ 95%
- PCI requirements met
- Production ready

---

## Resource Requirements

**Team:**
- Backend Developer (2)
- DevOps Engineer (0.5)
- QA Engineer (0.5)

**Skills:**
- Node.js/TypeScript
- PostgreSQL
- Stripe API
- PCI compliance knowledge

---

## Risk Assessment

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Stripe API changes | HIGH | LOW | Use stable API version |
| PCI compliance | HIGH | MEDIUM | External audit |
| Webhook reliability | MEDIUM | MEDIUM | Retry mechanism |

---
```

✅ **Plan Created Successfully**

---

## Phase 3: Generate Implementation Tasks (5 minutes)

### Execute

```bash
smartspec_generate_tasks_v4 specs/feature/spec-005-payment-system/spec.md
```

### Output

**Files Created:**
1. `specs/feature/spec-005-payment-system/tasks.md`
2. `specs/feature/spec-005-payment-system/README.md` (auto-generated)
3. `specs/feature/spec-005-payment-system/data-model.md` (auto-generated)
4. `specs/feature/spec-005-payment-system/openapi.yaml` (auto-generated)
5. `specs/feature/spec-005-payment-system/test-plan.md` (auto-generated)

**tasks.md Preview:**
```markdown
# Implementation Tasks - Payment Processing System

**Generated:** 2025-12-03 14:35
**Author:** SmartSpec Architect v4.0
**Source SPEC:** SPEC-005 v1.0.0
**Total Phases:** 8
**Total Tasks:** 75
**Estimated Effort:** 320 hours (~8 weeks for 4 people)

---

## Supporting Documentation

**Available Files:**
- `spec.md` - Complete specification
- `plan.md` - Project plan
- `README.md` - Implementation guide (auto-generated)
- `data-model.md` - Data schemas (auto-generated)
- `openapi.yaml` - API specification (auto-generated)
- `test-plan.md` - Testing strategy (auto-generated)

**Related Specs:** (Resolved from SPEC_INDEX)
- **spec-core-001-authentication** (`specs/core/spec-core-001-authentication/spec.md`, repo: private) - Authentication System
- **spec-feature-002-user-management** (`specs/feature/spec-feature-002-user-management/spec.md`, repo: private) - User Management

---

## Phase Overview

| Phase | Tasks | Focus | Hours | Risk |
|-------|-------|-------|-------|------|
| Phase 1 | T001-T010 | Database & Models | 40 | LOW |
| Phase 2 | T011-T020 | Stripe Integration | 45 | MEDIUM |
| Phase 3 | T021-T030 | Payment Processing | 50 | HIGH |
| Phase 4 | T031-T040 | Subscription Service | 50 | HIGH |
| Phase 5 | T041-T050 | Webhook Handler | 40 | MEDIUM |
| Phase 6 | T051-T060 | Refund System | 35 | MEDIUM |
| Phase 7 | T061-T070 | Testing | 40 | LOW |
| Phase 8 | T071-T075 | Deployment | 20 | MEDIUM |

---

## Phase 1: Database & Models (T001-T010)

### Task T001: Create Database Schema (~4 hours)

**Description:**
Create PostgreSQL schema for payments, subscriptions, customers, and webhooks.

**Files:**

**CREATE: `src/database/schema.sql`** (~200 lines - MEDIUM)
- Tables: payments, subscriptions, customers, webhooks, refunds
- Indexes for performance
- Constraints for data integrity

**Supporting Files Referenced:**
- `data-model.md` → Use defined entities

**Dependencies:** None

**Acceptance Criteria:**
- [ ] All tables created
- [ ] Indexes defined
- [ ] Foreign keys set up
- [ ] Migration script ready

**Validation:**
```bash
psql -f src/database/schema.sql
psql -c "\dt"  # Verify tables
```

---

### Task T002: Create Payment Model (~3 hours)

**Description:**
TypeScript model for Payment entity with Zod validation.

**Files:**

**CREATE: `src/models/payment.ts`** (~150 lines - SMALL)
- Payment interface
- Zod schema for validation
- Status enum
- Helper methods

**Supporting Files Referenced:**
- `data-model.md` → Payment entity spec

**Dependencies:**
- T001 (Schema must exist)

**Acceptance Criteria:**
- [ ] Model matches schema
- [ ] Validation working
- [ ] TypeScript types correct

**Validation:**
```bash
tsc --noEmit
npm test -- payment.test.ts
```

---

[... continues for all 75 tasks ...]

---

## ⚡ CHECKPOINT: Phase 1 Complete

**Validation Required:**
- [ ] All 10 tasks completed
- [ ] TypeScript compilation passes
- [ ] All model tests passing
- [ ] Database migrations successful
- [ ] No linting errors

**Next Steps:** Continue to Phase 2: Stripe Integration

---
```

**data-model.md Preview:**
```markdown
# Data Model - Payment Processing System

**Generated:** 2025-12-03 14:35
**Author:** SmartSpec Architect v4.0

---

## Entities

### Payment
**Description:** Individual payment transaction

**Fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | UUID | Yes | Primary key |
| customerId | UUID | Yes | FK to customers |
| amount | Integer | Yes | Amount in cents |
| currency | String | Yes | ISO currency code |
| status | Enum | Yes | pending/succeeded/failed |
| stripePaymentIntentId | String | Yes | Stripe reference |
| createdAt | Timestamp | Yes | Creation time |

**Relationships:**
- Many-to-One: Payment → Customer
- One-to-One: Payment → Refund (optional)

---

### Subscription
**Description:** Recurring subscription

**Fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | UUID | Yes | Primary key |
| customerId | UUID | Yes | FK to customers |
| planId | String | Yes | Stripe plan ID |
| status | Enum | Yes | active/canceled/past_due |
| currentPeriodStart | Timestamp | Yes | Billing period start |
| currentPeriodEnd | Timestamp | Yes | Billing period end |

---

[... continues for all entities ...]
```

✅ **All Tasks & Supporting Files Generated**

---

## Phase 4: Generate Implementation Prompt (2 minutes)

### Execute

```bash
smartspec_generate_kilo_prompt_v4 specs/feature/spec-005-payment-system/tasks.md
```

### Output

**File Created:** `specs/feature/spec-005-payment-system/kilo-prompt.md`

**Contents Preview:**
```markdown
# Kilo Code / Claude Code Implementation: Payment Processing System

**Generated:** 2025-12-03 14:40
**Author:** SmartSpec Architect v4.0
**Total:** 8 phases, 75 tasks, 320 hours

---

## 📚 Supporting Documentation

**Available in Project Directory:**
- `spec.md` - Complete specification
- `tasks.md` - Detailed task list
- `plan.md` - Project plan
- `README.md` - Setup guide
- `data-model.md` - Database schemas
- `openapi.yaml` - API contracts
- `test-plan.md` - Testing strategy

**Related Specs:**
- **spec-core-001-authentication** (`specs/core/...`, repo: private) - Auth integration needed

**Read all documentation before starting.**

---

## 🚨 CRITICAL EXECUTION CONSTRAINTS

**HARD LIMITS:**
- Max 10 tasks per cycle
- Max 5 file edits per task
- Max 50 lines per str_replace
- Stop at 3 consecutive errors

**FILE STRATEGIES:**
- SMALL (<200 lines): Any method
- MEDIUM (200-500 lines): str_replace only
- LARGE (>500 lines): Surgical, max 50 lines

**VALIDATION REQUIRED AFTER EACH TASK:**
- TypeScript: `tsc --noEmit`
- Tests: `npm test`
- Lint: `npm run lint`

---

## 🔧 Execution Modes

### Mode 1: Kilo Code (Recommended)
```bash
kilo specs/feature/spec-005-payment-system/kilo-prompt.md
```

### Mode 2: Claude Code
Execute interactively, one phase at a time

---

## 📋 Phase 1: Database & Models (T001-T010)

### Task T001: Create Database Schema (~4 hours)

**Description:**
Create PostgreSQL schema using data-model.md specifications.

**Supporting Files:**
- `data-model.md` → Entity definitions

**Implementation:**
1. CREATE `src/database/schema.sql` (~200 lines - MEDIUM)
2. Use str_replace for edits

**Validation:**
```bash
psql -f src/database/schema.sql
```

**Acceptance:**
- [ ] Tables created
- [ ] Indexes defined

---

[... continues for all tasks ...]
```

✅ **Implementation Prompt Ready**

---

## Phase 5: Implementation (Variable Time)

### Option A: Using Kilo Code

```bash
cd specs/feature/spec-005-payment-system
kilo kilo-prompt.md
```

**Kilo Code will:**
- Execute tasks sequentially
- Validate after each task
- Stop at checkpoints
- Handle errors per recovery procedures

### Option B: Using Claude Code

```bash
# In terminal, start Claude Code
# Copy Phase 1 from kilo-prompt.md
# Execute tasks one by one
# Validate after each
```

---

## Phase 6: Track Progress (Ongoing)

### Check Progress After Each Phase

```bash
smartspec_verify_tasks_progress specs/feature/spec-005-payment-system/tasks.md
```

**Output:** `progress-report-20251203.md`

```markdown
# Implementation Progress Report

**Overall Progress:** 20/75 tasks complete (27%)

**Phase Progress:**
| Phase | Tasks | Complete | In Progress | Not Started |
|-------|-------|----------|-------------|-------------|
| Phase 1 | 10 | 10 | 0 | 0 | ✅ Done
| Phase 2 | 10 | 8 | 2 | 0 | 🟦 In Progress
| Phase 3 | 10 | 2 | 0 | 8 | 🟨 Started

---

## ⚠️ Blockers

1. **T018:** Stripe webhook signature verification failing
   - Impact: Blocks T019, T020
   - Action: Review Stripe documentation

---

## 📋 Recommendations

### Immediate Actions
1. Fix T018 blocker
2. Complete Phase 2 checkpoint
3. Start Phase 3 after validation
```

---

## Phase 7: Handle Spec Updates (As Needed)

### Scenario: Need to add PayPal integration

### Step 1: Update Spec

```bash
smartspec_generate_spec_v4 specs/feature/spec-005-payment-system/spec.md
# Add PayPal to requirements
```

### Step 2: Check Sync

```bash
smartspec_sync_spec_tasks specs/feature/spec-005-payment-system/spec.md
```

**Output:** `sync-report-20251204.md`

```markdown
# Sync Report

**Status:** OUT_OF_SYNC

**Critical Issues:**
1. **Missing Feature:** PayPal Integration
   - SPEC mentions PayPal
   - No tasks for PayPal

**Recommended Actions:**
- Add Phase 9: PayPal Integration (10 tasks)
- Update plan.md timeline (+2 weeks)
```

### Step 3: Update Tasks

```bash
# Manual or auto-update
# Add new phase for PayPal
```

### Step 4: Regenerate Prompt

```bash
smartspec_generate_kilo_prompt_v4 specs/feature/spec-005-payment-system/tasks.md
```

**Output:** `kilo-prompt-20251204-1530.md`

---

## Summary

### Complete Workflow Executed ✅

```
1. SPEC Created
   ↓
2. Plan Generated
   ↓
3. Tasks Generated (+ 5 supporting files)
   ↓
4. Implementation Prompt Created
   ↓
5. Implementation (Kilo/Claude Code)
   ↓
6. Progress Tracked
   ↓
7. Sync Checked (after spec update)
   ↓
8. Tasks Updated
   ↓
9. New Prompt Generated
```

### Files Created (Total: 11)

**Primary:**
1. spec.md
2. plan.md
3. tasks.md
4. kilo-prompt.md

**Auto-Generated Supporting:**
5. README.md
6. data-model.md
7. openapi.yaml
8. test-plan.md

**Reports:**
9. progress-report-*.md
10. sync-report-*.md
11. kilo-prompt-*.md (timestamped)

### Time Breakdown

- Spec creation: 5 min
- Plan generation: 3 min
- Tasks generation: 5 min
- Prompt generation: 2 min
- **Total planning: ~15 minutes**

- Implementation: ~320 hours (varies by team)
- Progress tracking: 2 min per check
- Sync checking: 2 min per check

---

## Key Takeaways

### ✅ What Worked Well

1. **Auto-generation saved time**
   - Supporting files created automatically
   - Consistent format
   - Ready to use

2. **Spec reference resolution**
   - Dependencies tracked
   - Full paths provided
   - Easy to navigate

3. **Progress tracking**
   - Clear status
   - Blockers identified
   - Actionable recommendations

4. **Sync checking**
   - Caught inconsistencies early
   - Suggested fixes
   - Prevented scope drift

### 💡 Lessons Learned

1. **Use --nogenerate first**
   - Review before generating
   - Catch issues early
   - Adjust as needed

2. **Keep SPEC_INDEX updated**
   - Critical for resolution
   - Update after new specs
   - Version control

3. **Track progress regularly**
   - Weekly checks minimum
   - After each phase
   - Identify blockers early

4. **Review supporting files**
   - Auto-generated are templates
   - Refine as needed
   - Keep updated

---

**End of Complete Example**

**Version:** 4.0.0  
**Scenario:** Payment Processing System  
**Completion:** Full lifecycle demonstrated
