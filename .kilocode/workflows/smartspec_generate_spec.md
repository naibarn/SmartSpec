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
1. `smartspec.config.json` (if exists - project-specific)
2. `.smartspec/config.json` (if exists - organization-wide)
3. `.smartspec/SPEC_INDEX.json` (if exists - for dependency resolution)
4. Built-in defaults

Parse flags from $ARGUMENTS and merge with config.

### 1.1 Load SPEC_INDEX.json for Dependency Resolution

If `.smartspec/SPEC_INDEX.json` exists:
- Load the entire spec index into memory
- This will be used to resolve spec dependencies with full path and repo information
- Structure: `{ "specs": [{ "id": "...", "title": "...", "path": "...", "repo": "..." }] }`

If file doesn't exist:
- Dependencies will be listed without path/repo information
- Show warning in output

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
7. **Security Threat Model (STRIDE)** - Full by default
8. **Performance Requirements** - Full metrics
9. **Configuration Schema** - Complete
10. Implementation Guide
11. Testing Strategy (comprehensive)
12. Monitoring & Observability (detailed)
13. Examples (multiple scenarios)
14. Related Specs

**Automatically includes:**
- ✅ STRIDE threat model (full)
- ✅ Performance Requirements (P50/P95/P99, TPS, SLA)
- ✅ Audit logging requirements
- ✅ Idempotency requirements
- ✅ Data integrity checks
- ✅ Disaster recovery
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

### 7.6 domain=internal

Reduce requirements:
- Lower SLA expectations
- Simpler security
- Minimal performance tracking

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

### 12.1 smartspec.config.json

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
2. Project config (smartspec.config.json)
3. Organization config (.smartspec/config.json)
4. Built-in defaults (lowest)

---

## 13. Generate SPEC Based on Profile & Flags

### 13.1 Assemble Sections

Based on:
- Selected profile
- Flags (--security, --di, --performance)
- Domain hints
- Config file settings

### 13.1.1 Resolve Spec Dependencies (NEW)

If the SPEC includes dependencies (Related Specs section):

1. **Extract dependency IDs** from user input or existing SPEC
2. **Look up each dependency** in SPEC_INDEX.json
3. **Format each dependency** as:
   ```
   - **{spec_id}** - {description} - Spec Path: "{path}/spec.md" Repo: {repo}
   ```
4. **Group by category**:
   - Core Dependencies (category: "core")
   - Feature Specs (category: "feature")
   - Infrastructure Specs (category: "infrastructure")

**Example output:**
```markdown
## 19. Related Specs

### 19.1. Core Dependencies
- **spec-core-001-authentication** - User authentication for financial operations - Spec Path: "specs/core/spec-core-001-authentication/spec.md" Repo: private
- **spec-core-002-authorization** - RBAC for admin financial operations - Spec Path: "specs/core/spec-core-002-authorization/spec.md" Repo: private

### 19.2. Feature Specs
- **spec-002-user-management** - User profile and account management - Spec Path: "specs/feature/spec-002-user-management/spec.md" Repo: public
```

**Error handling:**
- If spec not found in SPEC_INDEX.json:
  ```
  - **spec-unknown-001** - [NOT FOUND IN SPEC_INDEX] - Spec Path: "N/A" Repo: unknown
  ```
- If SPEC_INDEX.json doesn't exist:
  ```
  ⚠️ Warning: SPEC_INDEX.json not found. Dependencies listed without path/repo information.
  
  ## 19. Related Specs
  - **spec-core-001-authentication** - User authentication for financial operations
  ```

### 13.2 Apply Meta Tags

Insert meta tags for critical sections.

### 13.3 Apply Mode

If compact mode: condense to 5 sections.
If standard mode: full detail.

### 13.4 Run Validation

If --validate-consistency: check rules.

### 13.5 Write Output

- Primary: spec.md
- Backup: .smartspec/backups/ (unless --no-backup)
- Report: .smartspec/reports/ (unless --no-report)

---

## 14. Report Output

### 14.1 Standard Report (Thai)

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
