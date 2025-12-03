# SmartSpec v4.1 - Conditional Sections Update

**Version:** 4.1.0
**Date:** December 3, 2025
**Purpose:** Add auto-detection for Performance Requirements and DI Pattern

---

## 🎯 What's New

### 1. Performance Requirements (Conditional)
**Auto-included when SPEC involves:**
- Financial/payment systems (credit, billing, ledger)
- High-load systems (queues, workers, orchestration)
- Critical path services (auth, core platform)
- Systems with specific SLA requirements

### 2. DI Pattern (Conditional)
**Auto-included when SPEC is:**
- Backend service (Node.js, Python, Java, Go)
- Has database operations
- Has external integrations
- Is a microservice

---

## 📋 Files Updated

### 1. Knowledge-Base.md
**Location:** `.smartspec/Knowledge-Base.md`
**Added:** Section 10 - Conditional Sections

**New Content:**
- 10.1 Performance Requirements Section
  - When to include criteria
  - Detection keywords
  - Template structure
  - When NOT to include

- 10.2 Dependency Injection Pattern Section
  - When to include criteria
  - Detection rules
  - Concise template for SPECs
  - When NOT to include

- 10.3 Auto-Detection Rules for Workflows
  - Keyword detection logic
  - Section placement rules

- 10.4 Examples
  - Financial system (include both)
  - Admin tool (DI only)
  - UI library (neither)

- 10.5 Content Customization
  - How to adjust templates

### 2. smartspec_generate_spec_v4.md
**Location:** workflows/smartspec_generate_spec_v4.md

**Updated Sections:**

**NEW MODE - Step 2: Analyze Requirements**
```python
def should_include_performance_requirements(requirements: str) -> bool:
    # Financial keywords
    financial_keywords = ['credit', 'payment', 'billing', 'ledger', ...]
    
    # Architecture keywords  
    architecture_keywords = ['saga', 'queue', 'orchestrator', ...]
    
    # Scale keywords
    scale_keywords = ['TPS', 'throughput', 'load', ...]
    
    # Critical keywords
    critical_keywords = ['SLA', 'uptime', 'availability', ...]
    
    # Return True if matches criteria
```

```python
def should_include_di_pattern(requirements: str) -> bool:
    # Backend service indicators
    backend_indicators = ['backend', 'service', 'API', ...]
    
    # Database indicators
    database_indicators = ['database', 'DB', 'PostgreSQL', ...]
    
    # Integration indicators
    integration_indicators = ['external API', 'third-party', ...]
    
    # Return True if backend with dependencies
```

**SPEC Generation - Conditional Insertion:**

**After Technology Stack (if INCLUDE_DI_PATTERN):**
```markdown
## Dependency Injection Pattern (MANDATORY)

Pattern Compliance: This service MUST implement DI Pattern

### Core Requirements
1. Constructor-Based Injection
2. Interface-Based Dependencies
3. Backward Compatibility

### Standard Dependencies
```typescript
export class ServiceName {
  constructor(
    database?: IDatabase,
    logger?: ILogger,
    cache?: ICache,
    config?: ServiceConfig
  ) {
    this.database = database || createDatabaseConnection();
    // ...
  }
}
```

### Testing Requirements
- Inject mock dependencies via constructor
- No jest.mock() for service dependencies
- Target coverage: ≥ 95%

### Benefits
- 100% test coverage achievable
- 60% maintenance reduction
- 83% debug time reduction
```

**After Implementation Guide (if INCLUDE_PERFORMANCE):**
```markdown
## Performance Requirements

### Latency Targets
- P50: < 150 ms
- P90: < 250 ms
- P95: < 300 ms
- P99: < 600 ms

### Throughput Capacity
**Normal Load:** 50-200 TPS sustained
**Peak Load:** [Define based on requirements]

### Availability & SLA
- Uptime: 99.9% monthly
- RTO: ≤ 5 minutes
- RPO: 0 (no data loss)

### Database Performance
- Write latency: < 10 ms
- Read latency: < 5 ms

### Queue & Worker (if applicable)
- Queue delay P99: < 500 ms
- Max retries: 3
- DLQ threshold: < 1%

### Metrics & Alerting
Required metrics: latency, throughput, error_rate
Critical alerts: P99 > threshold, error > 1%
```

---

## 🔍 Detection Logic Details

### Performance Requirements Detection

**Include if ANY of:**
1. Has financial keywords (credit, payment, billing, ledger, money)
2. Has architecture + scale (queue AND throughput, saga AND TPS)
3. Has critical keywords (SLA, uptime, real-time)

**Exclude if:**
- Internal tools (< 20 TPS mentioned)
- Admin systems (few users mentioned)
- Libraries/utilities
- UI/UX specs
- Data schemas only

### DI Pattern Detection

**Include if ALL of:**
1. Backend service (Node.js, Python, Java, Go mentioned)
2. AND (has database OR has integration)

**Exclude if:**
- Frontend only
- Static websites
- Pure schemas
- UI/UX designs

---

## 📝 Usage Examples

### Example 1: Financial Credit System

**User Input:**
```
Create SPEC for credit system with purchase, deduction, and ledger recording. 
Uses PostgreSQL and Redis. Needs to handle 200 TPS sustained, 1000 TPS peak.
```

**Detection:**
- Financial: ✅ (credit, purchase, ledger)
- Database: ✅ (PostgreSQL, Redis)
- Backend: ✅ (implied)
- Scale: ✅ (TPS mentioned)

**Result:**
- Include Performance Requirements: ✅
- Include DI Pattern: ✅

**SPEC Structure:**
1. Header
2. Technology Stack
3. **Dependency Injection Pattern** ← Auto-included
4. Overview
5. When to Use
6. Architecture
7. Implementation Guide
8. **Performance Requirements** ← Auto-included
9. Testing Strategy
10. Monitoring
11. Examples

---

### Example 2: Admin Dashboard Backend

**User Input:**
```
Create SPEC for admin dashboard backend API. Node.js with MongoDB.
For internal team of 5 admins. CRUD operations for user management.
```

**Detection:**
- Financial: ❌ (no financial keywords)
- Database: ✅ (MongoDB)
- Backend: ✅ (Node.js, API)
- Scale: ❌ (5 users - low traffic)

**Result:**
- Include Performance Requirements: ❌ (not critical/high-load)
- Include DI Pattern: ✅ (backend + database)

**SPEC Structure:**
1. Header
2. Technology Stack
3. **Dependency Injection Pattern** ← Auto-included
4. Overview
5. When to Use
6. Architecture
7. Implementation Guide
8. Testing Strategy
9. Monitoring
10. Examples

(No Performance Requirements - not needed for low-traffic admin tool)

---

### Example 3: React Component Library

**User Input:**
```
Create SPEC for React UI component library. Shared components for
forms, buttons, modals. TypeScript. No backend.
```

**Detection:**
- Financial: ❌
- Database: ❌
- Backend: ❌ (frontend only)

**Result:**
- Include Performance Requirements: ❌
- Include DI Pattern: ❌

**SPEC Structure:**
1. Header
2. Technology Stack
3. Overview
4. When to Use
5. Architecture (component structure)
6. Implementation Guide
7. Examples

(Neither conditional section included - frontend only)

---

## 🔄 Workflow Changes

### Before v4.1

**generate_spec workflow:**
1. Analyze requirements
2. Generate header
3. Generate standard sections (overview, architecture, etc.)
4. Done

**Result:** All SPECs have same structure, some missing important sections

---

### After v4.1

**generate_spec workflow:**
1. Analyze requirements
2. **Detect if Performance Requirements needed** ← NEW
3. **Detect if DI Pattern needed** ← NEW
4. Generate header
5. Generate Technology Stack
6. **If DI needed: Insert DI Pattern section** ← NEW
7. Generate Overview, When to Use
8. Generate Architecture
9. Generate Implementation Guide
10. **If Performance needed: Insert Performance Requirements** ← NEW
11. Generate Testing, Monitoring
12. Generate Examples
13. Done

**Result:** SPECs automatically include appropriate sections based on type/requirements

---

## ✅ Benefits

### For Users
- ✅ Don't need to remember to add Performance Requirements
- ✅ Don't need to remember to add DI Pattern
- ✅ Consistent SPEC quality
- ✅ Production-ready specs from start

### For Teams
- ✅ Financial systems always have SLA targets
- ✅ Backend services always document DI pattern
- ✅ Reduced spec review time
- ✅ Fewer implementation surprises

### For Quality
- ✅ No missing critical sections
- ✅ Standardized performance expectations
- ✅ Testability built-in (DI Pattern)
- ✅ Better production readiness

---

## 🎓 Best Practices

### When Creating SPECs

**DO:**
- ✅ Mention specific technologies (database names, frameworks)
- ✅ Describe scale requirements if known (TPS, concurrent users)
- ✅ Mention if system handles money/payments
- ✅ Describe critical path / SLA needs

**DON'T:**
- ❌ Be vague about system type
- ❌ Skip mentioning backend vs frontend
- ❌ Forget to mention integrations/dependencies

### Customizing Auto-Included Sections

**After generation:**
1. Review Performance Requirements thresholds
2. Adjust latency targets for specific service
3. Update DI Pattern dependencies to match actual services
4. Add service-specific metrics
5. Customize examples

**Templates are starting points** - always review and adjust!

---

## 🔮 Future Enhancements (v4.2+)

**Potential additions:**
- [ ] API Gateway Pattern (for services with >10 endpoints)
- [ ] Saga Pattern (for distributed transactions)
- [ ] CQRS Pattern (for read-heavy systems)
- [ ] Event Sourcing (for audit-heavy systems)
- [ ] Circuit Breaker (for services with external dependencies)

**Auto-detection for:**
- [ ] Microservices architecture
- [ ] Event-driven architecture
- [ ] Real-time systems (WebSocket)
- [ ] Batch processing systems

---

## 📞 Support

### If Detection is Wrong

**False Positive (included but shouldn't):**
1. Remove section manually
2. Update feedback to improve detection

**False Negative (should include but didn't):**
1. Add section manually using template from Knowledge Base
2. Update feedback to improve detection

### Template Customization

Templates in Knowledge Base can be customized per organization:
- `.smartspec/Knowledge-Base.md` - Section 10
- Adjust thresholds, metrics, patterns
- Update detection keywords

---

## 📊 Metrics & Tracking

**Track these in production:**
- % SPECs with Performance Requirements auto-included
- % SPECs with DI Pattern auto-included
- False positive rate (included but not needed)
- False negative rate (should include but didn't)
- Time saved vs manual specification

**Expected:**
- 80%+ correct detection rate
- 50%+ time saved on spec creation
- 90%+ production-ready specs from start

---

## 🎉 Summary

**v4.1 Update adds:**
1. ✅ Auto-detection for Performance Requirements
2. ✅ Auto-detection for DI Pattern
3. ✅ Smart conditional inclusion
4. ✅ Updated Knowledge Base with guidelines
5. ✅ Updated workflow with detection logic

**Result:** Higher quality SPECs with less manual effort!

---

**Version:** 4.1.0  
**Status:** Ready for use  
**Backward Compatible:** 100% (all v4.0 features retained)
