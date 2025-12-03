---
description: Generate comprehensive project plan (plan.md) from SPEC with milestones, resource allocation, and timeline estimation. Supports --specindex and --nogenerate.
handoffs:
  - label: Generate Tasks
    agent: smartspec.tasks
    prompt: Generate tasks.md from this plan
---

## User Input
```text
$ARGUMENTS
```

**Patterns:** 
- `specs/feature/spec-004/spec.md`
- `--specindex="path/index.json"` 
- `--nogenerate` (dry run)
- `--output=roadmap.md` (custom name)

## 0. Load SmartSpec Context

Read: `.smartspec/system_prompt.md`, `Knowledge-Base.md`, `constitution.md`, SPEC_INDEX

Parse flags:
- `--specindex` → Custom SPEC_INDEX path
- `--nogenerate` → DRY_RUN_MODE = true
- `--output` → Custom output name (default: plan.md)

## 1. Resolve Paths

Extract SPEC path, determine SPEC_INDEX path, set output: `SPEC_DIR/[output or plan.md]`

## 2. Analyze SPEC

Parse sections: metadata, overview, architecture, implementation, testing, dependencies

Extract: complexity, risks, external deps, team needs, timeline constraints

## 3. Generate Plan Structure

### Header
```markdown
# Project Plan - [Name]

**Generated:** YYYY-MM-DD HH:mm
**Author:** SmartSpec Architect v4.0
**Source:** [SPEC-ID] v[X.Y.Z]
**Status:** PLANNING

## Executive Summary
- Duration: X weeks (includes 20-25% buffer)
- Team: Y developers
- Complexity: [LEVEL]
- Risk: [LEVEL]

**Timeline Guidance:**
- Simple projects: 8-12 weeks
- Standard backend services: 12-16 weeks
- Financial systems: 16-22 weeks (includes compliance)
- Complex multi-service: 20-28 weeks

**Buffer Allocation:**
- Low complexity: +20% buffer
- Medium complexity: +25% buffer
- High complexity: +30% buffer
- Financial/compliance: +25-30% buffer

**Recommended Timeline for Financial System:**
- Core development: 12 weeks
- Testing & QA: 3 weeks
- Security & compliance: 3 weeks
- Buffer & contingency: 4 weeks
- **Total: 22 weeks**

Success Criteria: [from SPEC]
```

### Milestones
```markdown
## 🎯 Milestones

### M1: Foundation Complete (Week 3)

**Deliverables:**
- Project structure initialized
- Development environment running
- Database schema deployed
- Authentication system functional

**Acceptance Criteria:**
- [ ] All team members can run project locally
- [ ] Database migrations apply successfully
- [ ] Users can register and login
- [ ] JWT authentication works for protected endpoints
- [ ] Unit tests pass (>80% coverage)
- [ ] Integration tests pass for auth flow
- [ ] Code review completed
- [ ] Documentation updated (README, API docs)

**Quality Gates:**
- ✅ Zero critical bugs
- ✅ Linting passes with no errors
- ✅ Build succeeds in CI/CD
- ✅ Security scan passes (no high/critical vulnerabilities)

**Sign-off Required:** Tech Lead, DevOps

---

### M2: Core Features Complete (Week 10)

**Deliverables:**
- Credit management system (add, deduct, balance)
- Ledger system (immutable, hash-chained)
- Payment integration (Stripe/PromptPay)
- Saga orchestration (credit purchase, cost deduction)

**Acceptance Criteria:**
- [ ] Credit operations work correctly (add, deduct, reserve)
- [ ] Ledger entries are immutable and tamper-proof
- [ ] Hash chain validation passes
- [ ] Payment flow works end-to-end (test mode)
- [ ] Webhooks handled correctly
- [ ] Sagas execute successfully
- [ ] Saga compensation works on failure
- [ ] Idempotency prevents duplicate transactions
- [ ] Unit tests pass (>85% coverage)
- [ ] Integration tests pass for all flows
- [ ] Load testing shows acceptable performance

**Quality Gates:**
- ✅ Zero critical/high bugs
- ✅ P99 latency < 300ms for core operations
- ✅ No data integrity issues
- ✅ Security review passed
- ✅ Code coverage > 85%

**Performance Validation:**
- Credit operations: P95 < 100ms
- Payment processing: P99 < 500ms
- Saga execution: < 5 seconds

**Sign-off Required:** Tech Lead, Product Owner, QA Lead

---

### M3: Integration & Testing Complete (Week 16)

**Deliverables:**
- All services integrated
- API endpoints complete
- Admin dashboard functional
- Monitoring and alerting configured
- Security hardening complete

**Acceptance Criteria:**
- [ ] All API endpoints documented and tested
- [ ] End-to-end tests pass for critical flows
- [ ] Admin dashboard shows real-time data
- [ ] Monitoring dashboards configured (Grafana/Datadog)
- [ ] Alerts configured for critical metrics
- [ ] Security measures implemented:
  - [ ] Rate limiting active
  - [ ] HTTPS/TLS enforced
  - [ ] Input validation on all endpoints
  - [ ] SQL injection prevention verified
  - [ ] XSS prevention verified
- [ ] Compliance requirements met (PCI DSS if applicable)
- [ ] Penetration testing completed
- [ ] Load testing passed (1000 TPS sustained)

**Quality Gates:**
- ✅ Zero critical/high bugs
- ✅ All security scans pass
- ✅ Performance targets met
- ✅ API documentation complete
- ✅ Runbook documented

**Performance Validation:**
- System-wide P99: < 300ms
- Throughput: 1000 TPS sustained
- Error rate: < 0.1%
- Availability: > 99.9%

**Sign-off Required:** Tech Lead, Security Team, QA Lead, Product Owner

---

### M4: Production Ready (Week 22)

**Deliverables:**
- Production deployment successful
- Disaster recovery tested
- Operational runbooks complete
- Team training complete
- Go-live checklist verified

**Acceptance Criteria:**
- [ ] Production environment configured
- [ ] Database backups automated and tested
- [ ] Disaster recovery plan tested
- [ ] Rollback procedure tested
- [ ] Monitoring alerts verified in production
- [ ] On-call rotation established
- [ ] Incident response plan documented
- [ ] Operational runbooks complete:
  - [ ] Deployment procedure
  - [ ] Rollback procedure
  - [ ] Common troubleshooting
  - [ ] Scaling procedures
- [ ] Team trained on:
  - [ ] System architecture
  - [ ] Deployment process
  - [ ] Monitoring and alerting
  - [ ] Incident response
- [ ] Go-live checklist completed:
  - [ ] Production data migrated (if applicable)
  - [ ] DNS configured
  - [ ] SSL certificates installed
  - [ ] CDN configured (if applicable)
  - [ ] Rate limiting configured
  - [ ] Backup verified
  - [ ] Monitoring verified
  - [ ] Alerts verified
  - [ ] Stakeholders notified

**Quality Gates:**
- ✅ Zero critical bugs
- ✅ All production checks pass
- ✅ Disaster recovery tested successfully
- ✅ Performance validated in production
- ✅ Security audit passed

**Production Validation:**
- Smoke tests pass
- Health checks return 200
- Metrics flowing to monitoring
- Alerts triggering correctly
- Logs being collected

**Sign-off Required:** CTO, Tech Lead, DevOps Lead, Security Team, Product Owner

**Go/No-Go Decision Criteria:**
- All acceptance criteria met
- All quality gates passed
- Team ready for on-call
- Stakeholders aligned
- Rollback plan tested
```

### Phases
```markdown
## 📋 Phases

### Phase 1: Setup (Weeks 1-2)
Duration: 2 weeks | Team: 2-3 devs | Risk: LOW

**Objectives:**
- Initialize project structure
- Setup development environment
- Configure database
- Implement authentication foundation

**Task-Level Breakdown:**

#### 1.1 Project Initialization (2 days)
- [ ] Create repository structure
- [ ] Setup TypeScript configuration (tsconfig.json)
- [ ] Configure ESLint and Prettier
- [ ] Setup package.json with dependencies
- [ ] Configure build scripts (npm run build, dev, test)
- [ ] Setup .env.example with required variables
- [ ] Create README.md with setup instructions
- [ ] Configure .gitignore

**Exit Criteria:** 
- ✅ Project builds without errors
- ✅ Linting passes
- ✅ All team members can run locally

#### 1.2 Development Environment (2 days)
- [ ] Setup Docker Compose for local development
- [ ] Configure PostgreSQL container
- [ ] Configure Redis container
- [ ] Setup database migrations framework (Drizzle/Prisma)
- [ ] Create initial migration scripts
- [ ] Setup seed data for development
- [ ] Configure hot-reload for development
- [ ] Document environment setup in README

**Exit Criteria:**
- ✅ Docker Compose up runs successfully
- ✅ Database migrations apply cleanly
- ✅ Seed data loads correctly

#### 1.3 Database Schema (3 days)
- [ ] Design ER diagram (if not in SPEC)
- [ ] Create migration for core tables:
  - [ ] users table
  - [ ] sessions table
  - [ ] audit_log table
  - [ ] (Financial) credit_balance table
  - [ ] (Financial) ledger table
  - [ ] (Financial) transaction_log table
- [ ] Add indexes for performance
- [ ] Add constraints (FK, CHECK, UNIQUE)
- [ ] Create database functions/triggers if needed
- [ ] Test migrations (up and down)

**Exit Criteria:**
- ✅ All tables created successfully
- ✅ Constraints enforced
- ✅ Rollback works correctly

#### 1.4 Authentication Foundation (3 days)
- [ ] Install authentication libraries (Passport.js/JWT)
- [ ] Create User model
- [ ] Implement user registration endpoint
- [ ] Implement login endpoint (JWT generation)
- [ ] Implement JWT validation middleware
- [ ] Implement password hashing (bcrypt)
- [ ] Create auth service layer
- [ ] Write unit tests for auth service
- [ ] Write integration tests for auth endpoints

**Exit Criteria:**
- ✅ Users can register
- ✅ Users can login and receive JWT
- ✅ Protected endpoints reject invalid tokens
- ✅ Tests pass (>80% coverage)

**Dependencies:** 
- Dev environment access
- Database credentials
- JWT secret key

**Deliverables:** 
- Working development environment
- Database schema deployed
- Authentication functional
- Test suite passing

**Risks:**
- Database migration conflicts (LOW)
- Environment setup issues on different OS (MEDIUM)
- Mitigation: Detailed documentation, Docker standardization

---

### Phase 2: Core Domain Models (Weeks 4-7)
Duration: 4 weeks | Team: 3-4 devs | Risk: MEDIUM

**Objectives:**
- Implement core business models
- Setup service layer architecture
- Implement data access layer
- Add comprehensive validation

**Task-Level Breakdown:**

#### 2.0 Data Model Design (Financial) (3 days)
- [ ] Review SPEC Data Model section
- [ ] Refine ER diagram if needed
- [ ] Design table partitioning strategy:
  - [ ] transaction_log partitioned by month
  - [ ] ledger partitioned by year (if high volume)
- [ ] Design index strategy for performance
- [ ] Plan materialized views for reports
- [ ] Document schema migration plan
- [ ] Review with team and stakeholders

**Exit Criteria:**
- ✅ ER diagram approved
- ✅ Partitioning strategy defined
- ✅ Index plan documented
- ✅ Team aligned on schema

#### 2.1 Credit Service (Financial) (4 days)
- [ ] Create CreditBalance model
- [ ] Implement credit service:
  - [ ] getBalance(userId)
  - [ ] addCredit(userId, amount, sagaId)
  - [ ] deductCredit(userId, amount, sagaId)
  - [ ] reserveCredit(userId, amount, sagaId)
  - [ ] releaseReserve(userId, sagaId)
- [ ] Add optimistic locking (version field)
- [ ] Implement balance validation
- [ ] Add transaction support
- [ ] Write unit tests
- [ ] Write integration tests

**Exit Criteria:**
- ✅ All CRUD operations work
- ✅ Optimistic locking prevents race conditions
- ✅ Tests pass (>85% coverage)

#### 2.2 Ledger Service (Financial) (3 days)
- [ ] Create Ledger model (immutable)
- [ ] Implement ledger service:
  - [ ] recordEntry(userId, type, amount, referenceId)
  - [ ] getHistory(userId, filters)
  - [ ] calculateHash(entry)
  - [ ] verifyIntegrity(userId)
- [ ] Implement hash chain (blockchain-style)
- [ ] Add audit trail
- [ ] Prevent UPDATE/DELETE operations
- [ ] Write tests for immutability

**Exit Criteria:**
- ✅ Ledger entries are immutable
- ✅ Hash chain validates correctly
- ✅ Tampering detection works

#### 2.3 Payment Service Integration (4 days)
- [ ] Setup Stripe/PromptPay SDK
- [ ] Create Payment model
- [ ] Implement payment service:
  - [ ] createPaymentIntent(amount, userId)
  - [ ] confirmPayment(paymentId)
  - [ ] refundPayment(paymentId, amount)
  - [ ] handleWebhook(event)
- [ ] Add idempotency key support
- [ ] Implement retry logic with exponential backoff
- [ ] Add circuit breaker pattern
- [ ] Write tests (mock external API)

**Exit Criteria:**
- ✅ Payment flow works end-to-end
- ✅ Webhooks handled correctly
- ✅ Idempotency prevents duplicates

#### 2.4 Saga Orchestration (4 days)
- [ ] Create SagaState model
- [ ] Implement saga service:
  - [ ] createSaga(type, payload)
  - [ ] updateStep(sagaId, step)
  - [ ] markCompleted(sagaId)
  - [ ] markFailed(sagaId, error)
  - [ ] compensate(sagaId)
- [ ] Implement Credit Purchase Saga
- [ ] Implement Cost Deduction Saga
- [ ] Add timeout handling
- [ ] Add dead letter queue
- [ ] Write saga tests

**Exit Criteria:**
- ✅ Sagas execute successfully
- ✅ Compensation works on failure
- ✅ Timeouts trigger compensation

**Dependencies:**
- Phase 1 complete
- External API credentials (Stripe)

**Deliverables:**
- Core services implemented
- Saga orchestration working
- Comprehensive test coverage

**Risks:**
- External API integration complexity (MEDIUM)
- Saga compensation edge cases (HIGH)
- Mitigation: Extensive testing, monitoring

[Continue for all phases...]
```

### Resources
```markdown
## 👥 Resources

Required Roles:
- Backend: X devs
- Frontend: Y devs (if needed)
- DevOps: Z
- QA: W

Skills: [Tech stack from SPEC]

Time Allocation:
| Phase | Duration | Dev-Weeks | Calendar |
|-------|----------|-----------|----------|
| P1    | X weeks  | Y dev-wks | Z weeks  |
```

### Risks
```markdown
## ⚠️ Risks

HIGH:
- [Risk 1]: Impact [H/M/L], Prob [H/M/L]
  Mitigation: [Strategy]

MEDIUM:
- [Risk 2]: [Assessment]

Schedule Risks: [Dependencies, resources]
```

### Dependencies
```markdown
## 🔗 Dependencies

Internal (from SPEC_INDEX):
- **spec-core-001** (`path`, repo: private)
  Required: Phase X | Risk if delayed: [assessment]

External:
- Services: [List]
- Infrastructure: Database, cloud, CI/CD
```

### Timeline
```markdown
## 📅 Timeline

Week 1-2:  ████ Phase 1
Week 3-4:  ████ Phase 2
Week 5-6:  ████ Phase 3
...

Key Dates:
- Start: [Date]
- M1: [Date]
- M2: [Date]
- Launch: [Date]

Critical Path: [Tasks that cannot delay]
```

### Quality Gates
```markdown
## ✅ Quality Gates

Phase Completion:
- [ ] Code reviewed
- [ ] Tests >80% coverage
- [ ] No critical bugs
- [ ] Docs updated
- [ ] Performance met

Release Criteria:
- [ ] All features per SPEC
- [ ] Security audit passed
- [ ] Load testing done
- [ ] DR tested
- [ ] User docs complete
```

### Compliance & Security (Financial Systems)
```markdown
## 🔒 Compliance & Security

### PCI DSS Compliance (if processing credit cards)

**Requirements:**
- [ ] **Requirement 1:** Install and maintain firewall configuration
  - [ ] Network segmentation implemented
  - [ ] Firewall rules documented
  - [ ] Regular firewall review scheduled

- [ ] **Requirement 2:** Do not use vendor-supplied defaults
  - [ ] Default passwords changed
  - [ ] Unnecessary services disabled
  - [ ] Security parameters configured

- [ ] **Requirement 3:** Protect stored cardholder data
  - [ ] Cardholder data encrypted (AES-256)
  - [ ] Encryption keys managed securely (AWS KMS)
  - [ ] Data retention policy enforced
  - [ ] Secure deletion procedures

- [ ] **Requirement 4:** Encrypt transmission of cardholder data
  - [ ] TLS 1.3 enforced
  - [ ] Strong cryptography implemented
  - [ ] Certificate management process

- [ ] **Requirement 6:** Develop and maintain secure systems
  - [ ] Security patches applied monthly
  - [ ] Code review for security issues
  - [ ] Vulnerability scanning weekly
  - [ ] Penetration testing annually

- [ ] **Requirement 8:** Identify and authenticate access
  - [ ] Unique user IDs assigned
  - [ ] Strong password policy enforced
  - [ ] MFA implemented for admin access
  - [ ] Session timeout configured (15 minutes)

- [ ] **Requirement 10:** Track and monitor all access
  - [ ] Audit logs for all access
  - [ ] Log review daily
  - [ ] Log retention 1 year (online), 7 years (archive)
  - [ ] Time synchronization (NTP)

- [ ] **Requirement 11:** Regularly test security systems
  - [ ] Quarterly vulnerability scans
  - [ ] Annual penetration testing
  - [ ] IDS/IPS deployed
  - [ ] File integrity monitoring

**Timeline:**
- Week 8: Initial security assessment
- Week 10: Security controls implemented
- Week 12: Pre-assessment audit
- Week 14: Final PCI DSS audit

**Deliverables:**
- PCI DSS Self-Assessment Questionnaire (SAQ)
- Attestation of Compliance (AOC)
- Security policies documentation
- Audit evidence package

---

### SOC 2 Type II Compliance

**Trust Service Criteria:**

#### Security
- [ ] Access controls implemented (RBAC)
- [ ] Encryption at rest and in transit
- [ ] Vulnerability management program
- [ ] Incident response plan
- [ ] Security awareness training

#### Availability
- [ ] SLA: 99.95% uptime
- [ ] Redundancy and failover configured
- [ ] Disaster recovery tested
- [ ] Backup and restore tested
- [ ] Capacity planning documented

#### Processing Integrity
- [ ] Data validation on all inputs
- [ ] Transaction integrity checks
- [ ] Error handling and logging
- [ ] Reconciliation procedures
- [ ] Idempotency enforced

#### Confidentiality
- [ ] Data classification policy
- [ ] Encryption for sensitive data
- [ ] Access controls for confidential data
- [ ] Data retention and disposal policy
- [ ] Non-disclosure agreements

#### Privacy (if applicable)
- [ ] Privacy policy published
- [ ] Consent management
- [ ] Data subject rights (access, deletion)
- [ ] Privacy impact assessment
- [ ] Third-party data sharing controls

**Timeline:**
- Month 1-3: Control design and implementation
- Month 4-6: Control operation (observation period)
- Month 7: SOC 2 Type II audit

---

### GDPR Compliance (if handling EU data)

**Requirements:**
- [ ] **Lawful Basis:** Document legal basis for processing
- [ ] **Consent:** Obtain explicit consent where required
- [ ] **Data Minimization:** Collect only necessary data
- [ ] **Right to Access:** Implement data export functionality
- [ ] **Right to Erasure:** Implement account deletion
- [ ] **Right to Portability:** Provide data in machine-readable format
- [ ] **Data Protection Officer:** Appoint DPO (if required)
- [ ] **Privacy by Design:** Implement privacy controls from start
- [ ] **Data Breach Notification:** 72-hour notification process
- [ ] **Data Processing Agreements:** Sign DPAs with processors

**Implementation Tasks:**
- [ ] Privacy policy drafted and reviewed
- [ ] Cookie consent banner implemented
- [ ] Data mapping completed
- [ ] Data retention policy defined
- [ ] Data deletion workflows implemented
- [ ] Breach notification procedure documented

---

### Audit Logging Requirements

**What to Log:**
- [ ] All financial transactions (credit add/deduct)
- [ ] All authentication attempts (success/failure)
- [ ] All authorization failures
- [ ] All admin actions
- [ ] All data access (read/write/delete)
- [ ] All configuration changes
- [ ] All API calls (request/response)
- [ ] All errors and exceptions

**Log Format:**
```json
{
  "timestamp": "2025-12-03T14:30:00.000Z",
  "event_type": "CREDIT_DEDUCT",
  "user_id": "uuid",
  "ip_address": "1.2.3.4",
  "user_agent": "...",
  "request_id": "uuid",
  "action": "deduct_credit",
  "amount": 100.00,
  "status": "success",
  "metadata": { ... }
}
```

**Log Retention:**
- Hot storage: 30 days (searchable)
- Warm storage: 1 year (archived)
- Cold storage: 7 years (compliance)

**Log Security:**
- [ ] Logs encrypted at rest
- [ ] Logs immutable (append-only)
- [ ] Log access restricted (RBAC)
- [ ] Log integrity verification (hash)
- [ ] Log tampering alerts

---

### Security Testing Schedule

**Weekly:**
- [ ] Dependency vulnerability scan (npm audit, Snyk)
- [ ] SAST (Static Application Security Testing)
- [ ] Secret scanning (GitGuardian)

**Monthly:**
- [ ] DAST (Dynamic Application Security Testing)
- [ ] Security patch review and application
- [ ] Access review (remove unused accounts)

**Quarterly:**
- [ ] Vulnerability assessment
- [ ] Security training for team
- [ ] Incident response drill

**Annually:**
- [ ] Penetration testing (third-party)
- [ ] Security audit (SOC 2, PCI DSS)
- [ ] Disaster recovery test
- [ ] Business continuity test

---

### Security Incident Response

**Phases:**
1. **Detection:** Automated alerts, manual reports
2. **Containment:** Isolate affected systems
3. **Eradication:** Remove threat, patch vulnerability
4. **Recovery:** Restore services, verify integrity
5. **Lessons Learned:** Post-mortem, improve controls

**Severity Levels:**
- **P0 (Critical):** Data breach, system compromise - Response: Immediate
- **P1 (High):** Service outage, security vulnerability - Response: < 1 hour
- **P2 (Medium):** Performance degradation - Response: < 4 hours
- **P3 (Low):** Minor issues - Response: < 24 hours

**Notification Requirements:**
- Internal: Security team, management, legal
- External: Affected users, regulators (if required)
- Timeline: Within 72 hours for data breaches (GDPR)

---

### Compliance Checklist

**Pre-Launch:**
- [ ] Security audit completed
- [ ] Penetration testing passed
- [ ] Compliance requirements verified
- [ ] Privacy policy published
- [ ] Terms of service published
- [ ] Data processing agreements signed
- [ ] Security training completed
- [ ] Incident response plan tested
- [ ] Disaster recovery tested
- [ ] Legal review completed

**Post-Launch:**
- [ ] Continuous monitoring active
- [ ] Security alerts configured
- [ ] Compliance reporting scheduled
- [ ] Regular audits scheduled
- [ ] Security metrics tracked
```

### Communication
```markdown
## 📢 Communication

Daily: Standup (15m), Slack updates
Weekly: Progress report, risk review
Bi-weekly: Demo, retrospective

Metrics: Tasks completed, velocity, bugs, coverage, performance
```

## 4. Dry Run

If `--nogenerate`:
```markdown
# Plan Preview (DRY RUN)

Would generate: [PATH]
- Milestones: X
- Phases: Y  
- Duration: Z weeks
- Team: W devs
- Risk: [LEVEL]

To proceed: Remove --nogenerate
```
STOP if dry run

## 5. Write File

Write plan.md to output path

## 6. Report (Thai)

```
✅ สร้าง Project Plan เรียบร้อย

📁 ไฟล์: [PATH]
📊 Milestones: X | Phases: Y | Duration: Z weeks
👥 ทีม: W developers | Risk: [LEVEL]

🎯 Milestones:
- M1: Week X - Foundation
- M2: Week Y - Core
- M3: Week Z - Integration

⚠️ Risks: X HIGH, Y MEDIUM
💡 ระวัง: [Key risks]

🔄 ต่อไป:
1. Review plan.md
2. สร้าง tasks.md
3. Align ทีม
4. เริ่ม Phase 1
```

Context: $ARGUMENTS
