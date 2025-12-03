# SmartSpec v5.0 - Complete Documentation

**Version:** 5.0.0  
**Release Date:** December 3, 2025  
**Status:** Production Ready

---

## 🎯 What's New in v5.0

### Major Features

**1. Profiles System**
- `--profile=basic` - Minimal 5-section SPEC
- `--profile=backend-service` - Standard microservice
- `--profile=financial` - Critical system with full security
- `--profile=full` - Backward compatible with v4.0

**2. Meta Tags for Critical Sections**
```markdown
<!-- @critical security -->
<!-- @critical config -->
```
Precise identification, no keyword guessing

**3. Compact Mode**
- `--mode=compact` - 5 sections only
- Perfect for simple tools and prototypes

**4. Domain-Based Detection**
- `--domain=healthcare` - Auto HIPAA compliance
- `--domain=iot` - High throughput patterns
- `--domain=fintech` - Full financial requirements
- 8 domains supported

**5. Flexible DI Pattern**
- `--no-di` - Skip DI entirely
- `--di=minimal` - Brief mention only
- `--di=full` - Complete documentation

**6. Two-Level STRIDE**
- `--security=stride-basic` - Table format (10 lines)
- `--security=stride-full` - Comprehensive (100+ lines)

**7. Force Update Critical**
- `--force-update=stride,config` - Allow specific updates
- `--force-update=all` - Update everything

**8. Organized Output**
```
.smartspec/
├── backups/
├── reports/
├── registry/
└── trace.log
```

**9. Consistency Validation**
- `--validate-consistency` - Check section alignment
- 5+ validation rules

**10. Configuration File**
- `smartspec.config.json` - Project settings
- `.smartspec/config.json` - Organization defaults

---

## 📋 Quick Start

### Basic Usage

**1. Simple Tool (Minimal SPEC):**
```bash
smartspec new report-tool --profile=basic --mode=compact
```

**2. Standard Microservice:**
```bash
smartspec new user-service --profile=backend-service
```

**3. Financial System:**
```bash
smartspec new payment-processor --profile=financial
```

**4. With Domain:**
```bash
smartspec new telemetry-api --domain=iot
```

---

## 🎓 Profiles Guide

### Profile: basic

**When to Use:**
- Simple CRUD operations
- Internal tools
- Prototypes
- Quick documentation

**Sections (5 only):**
1. Header (minimal)
2. Overview
3. Architecture Summary
4. API or Data Model
5. Acceptance Criteria

**Excludes:**
- DI Pattern
- Testing Strategy
- Monitoring
- Security (unless specified)
- Performance Requirements

**Example:**
```bash
smartspec new expense-reporter \
  --profile=basic \
  --mode=compact
```

**Result:** 5-page SPEC, quick to create, easy to maintain

---

### Profile: backend-service

**When to Use:**
- REST APIs
- Microservices
- Background workers
- Most backend projects

**Sections (10):**
1. Header
2. Technology Stack
3. Dependency Injection Pattern
4. Overview
5. When to Use
6. Architecture
7. Implementation Guide
8. Testing Requirements
9. Monitoring
10. Examples

**Auto-Includes:**
- ✅ DI Pattern (full)
- ✅ Basic security
- ✅ Basic performance metrics
- ✅ Configuration schema (if detected)

**Example:**
```bash
smartspec new order-service \
  --profile=backend-service \
  --security=stride-basic
```

**Result:** Professional backend SPEC with testability built-in

---

### Profile: financial

**When to Use:**
- Payment systems
- Credit/billing systems
- Ledger services
- Any system handling money

**Sections (13+):**
1. Header
2. Technology Stack
3. Dependency Injection Pattern (MANDATORY)
4. Overview
5. When to Use / NOT to Use
6. Architecture (detailed)
7. **Security Threat Model (STRIDE-Full)**
8. **Performance Requirements (Full)**
9. Configuration Schema
10. Implementation Guide
11. Testing Strategy (comprehensive)
12. Monitoring & Observability
13. Examples
14. Related Specs

**Auto-Includes:**
- ✅ STRIDE threat model (full 100+ lines)
- ✅ Performance Requirements (P50/P95/P99, TPS, SLA)
- ✅ Audit logging requirements
- ✅ Idempotency patterns
- ✅ Data integrity checks
- ✅ Disaster recovery
- ✅ Compliance notes

**Example:**
```bash
smartspec new credit-purchase \
  --profile=financial
```

**Result:** Production-ready financial system SPEC

---

### Profile: full

**When to Use:**
- Backward compatibility with v4.0
- When unsure which profile to use
- Maximum flexibility

**Behavior:**
- Auto-detect all features
- Include all optional sections
- Same as SmartSpec v4.0

**Example:**
```bash
smartspec new complex-system --profile=full
```

---

## 🔍 Domain Guide

### Domain: healthcare

**Auto-Includes:**
- Privacy & HIPAA compliance
- Audit logging (mandatory)
- Real-time requirements
- Data retention policies

**Performance Profile:**
- P50: < 100ms
- P95: < 200ms
- P99: < 500ms
- Uptime: 99.95%

**Example:**
```bash
smartspec new patient-records-api \
  --domain=healthcare \
  --profile=backend-service
```

---

### Domain: iot

**Auto-Includes:**
- High throughput requirements
- Telemetry patterns
- Batch processing
- Edge computing notes

**Performance Profile:**
- Throughput: 1,000-10,000 msgs/sec
- Batch processing supported
- Data retention: 90 days

**Example:**
```bash
smartspec new sensor-ingestion \
  --domain=iot \
  --performance=full
```

---

### Domain: fintech

**Same as `--profile=financial`**

Automatically includes all financial system requirements.

---

### Domain: internal

**Auto-Adjusts:**
- Lower SLA (95%)
- Basic security
- Minimal performance tracking
- Simplified requirements

**Example:**
```bash
smartspec new admin-dashboard \
  --domain=internal \
  --profile=backend-service
```

---

## 🛠️ Flags Reference

### Profile Selection
```bash
--profile=basic              # Minimal SPEC
--profile=backend-service    # Standard microservice
--profile=financial          # Critical system
--profile=full               # All features (default)
```

### Mode Selection
```bash
--mode=standard              # Full detail (default)
--mode=compact               # 5 sections only
```

### Security Control
```bash
--security=none              # No security section
--security=basic             # Basic considerations
--security=stride-basic      # STRIDE table (10 lines)
--security=stride-full       # Complete STRIDE (100+ lines)
--security=auto              # Auto-detect (default)
```

### DI Pattern Control
```bash
--di=none                    # No DI section
--no-di                      # Shorthand for --di=none
--di=minimal                 # Brief mention
--di=full                    # Complete documentation
--di=auto                    # Auto-detect (default)
```

### Performance Control
```bash
--performance=none           # No performance section
--performance=basic          # Key metrics only
--performance=full           # Complete requirements
--performance=auto           # Auto-detect (default)
```

### Domain Hints
```bash
--domain=healthcare          # Medical systems
--domain=iot                 # IoT/telemetry
--domain=logistics           # Supply chain
--domain=ai                  # ML systems
--domain=fintech             # Financial tech
--domain=saas                # SaaS apps
--domain=internal            # Internal tools
--domain=realtime            # WebSocket/streaming
--domain=batch               # Batch processing
```

### Force Update
```bash
--force-update=all                    # Update all critical sections
--force-update=stride                 # Allow STRIDE update only
--force-update=stride,config,di       # Multiple sections
```

### Output Control
```bash
--no-backup                  # Don't create backups
--no-report                  # Don't generate reports
--output-dir=custom/path     # Custom output directory
```

### Validation
```bash
--validate-consistency       # Check section alignment
--no-validation             # Skip validation
```

### Other
```bash
--nogenerate                # Dry run (show plan only)
--specindex=path/index.json # Custom SPEC index
```

---

## 📝 Usage Examples

### Example 1: Simple CRUD Tool

```bash
smartspec new expense-tracker \
  --profile=basic \
  --mode=compact \
  --no-di
```

**Result:**
- 5 sections
- No DI Pattern
- No performance requirements
- Perfect for internal tools

---

### Example 2: REST API

```bash
smartspec new product-catalog-api \
  --profile=backend-service \
  --security=basic
```

**Result:**
- 10 sections
- DI Pattern included
- Basic security
- Standard monitoring

---

### Example 3: Payment System

```bash
smartspec new payment-gateway \
  --profile=financial
```

**Result:**
- 13+ sections
- STRIDE-Full security
- Full performance metrics
- Audit logging
- Idempotency patterns
- Production-ready

---

### Example 4: IoT Telemetry

```bash
smartspec new device-telemetry \
  --domain=iot \
  --profile=backend-service
```

**Result:**
- Backend service structure
- High throughput requirements
- Batch processing patterns
- Time-series considerations

---

### Example 5: Healthcare API

```bash
smartspec new medical-records-api \
  --domain=healthcare \
  --security=stride-full
```

**Result:**
- HIPAA compliance notes
- Audit logging mandatory
- Real-time requirements
- Privacy protections
- Full STRIDE model

---

### Example 6: Update Existing SPEC

```bash
smartspec edit specs/feature/spec-004/spec.md \
  --force-update=stride,config \
  --validate-consistency
```

**Result:**
- Allow STRIDE and Config updates
- Preserve other critical sections
- Validate consistency after update

---

## 🔄 Migration from v4.0 to v5.0

### Backward Compatibility

v5.0 is **100% backward compatible** with v4.0:

```bash
# v4.0 command
smartspec new my-service

# Works in v5.0 (uses --profile=full by default)
smartspec new my-service
```

### Converting v4.0 SPECs

**Option 1: Add Meta Tags**
```bash
smartspec migrate specs/old/spec.md --add-meta-tags
```

**Option 2: Re-profile**
```bash
smartspec edit specs/old/spec.md --profile=backend-service
```

**Option 3: Manual**
Add meta tags manually:
```markdown
<!-- @critical security -->
## Security Threat Model
...
<!-- @end-critical -->
```

### Benefits of Migration

**Before (v4.0):**
- Critical sections detected by keywords
- False positives possible
- Hard to customize

**After (v5.0):**
- Precise meta tags
- Easy force updates
- Flexible profiles

---

## ⚙️ Configuration File

### Project Config: `smartspec.config.json`

Place in project root:

```json
{
  "version": "5.0.0",
  "defaults": {
    "profile": "backend-service",
    "security": "basic",
    "di": "full"
  },
  "organization": {
    "name": "My Company",
    "defaultAuthor": "SmartSpec v5.0 | Engineering Team"
  }
}
```

### Organization Config: `.smartspec/config.json`

Shared across projects:

```json
{
  "version": "5.0.0",
  "profiles": {
    "backend-service": {
      "security": "stride-basic",
      "performance": "full"
    }
  },
  "validation": {
    "enabled": true
  }
}
```

### Priority

1. Command-line flags (highest)
2. Project config
3. Organization config
4. Built-in defaults (lowest)

---

## ✅ Consistency Validation

### Rules Checked

**Rule 1: API Coverage**
- APIs in Architecture must have examples
- Severity: WARN

**Rule 2: Queue Metrics**
- Queue mentioned → must have queue metrics
- Severity: ERROR

**Rule 3: Integration Tests**
- Transactions → must have integration tests
- Severity: WARN

**Rule 4: Retry Policy**
- External API → must have retry/backoff
- Severity: WARN

**Rule 5: Security Section**
- Authentication → must have security
- Severity: ERROR

### Example Output

```
🔍 Consistency Check Results:

❌ ERROR: Queue mentioned but no queue performance metrics
⚠️  WARN: API /api/v1/users has no example
⚠️  WARN: External API mentioned but no retry policy
✅ PASS: Security section present for authentication
✅ PASS: DI pattern included

Summary: 1 error, 2 warnings, 8 checks passed

Continue anyway? (y/n)
```

---

## 📊 Comparison: v4.0 vs v5.0

| Feature | v4.0 | v5.0 |
|---------|------|------|
| Profiles | None | 4 profiles |
| Meta Tags | ❌ | ✅ |
| Compact Mode | ❌ | ✅ |
| Domains | ❌ | 8 domains |
| DI Control | Auto only | none/minimal/full/auto |
| STRIDE Levels | Full only | basic/full |
| Force Update | ❌ | ✅ |
| Consistency Check | ❌ | ✅ |
| Config File | ❌ | ✅ |
| Backward Compat | N/A | ✅ 100% |

---

## 🎓 Best Practices

### When to Use Each Profile

**Use `basic`:**
- ✅ Simple CRUD
- ✅ Internal tools (< 10 users)
- ✅ Prototypes
- ✅ Quick documentation
- ❌ Production systems
- ❌ Customer-facing services

**Use `backend-service`:**
- ✅ REST APIs
- ✅ Microservices
- ✅ Background workers
- ✅ Most production services
- ❌ Financial systems
- ❌ Healthcare systems

**Use `financial`:**
- ✅ Payment processing
- ✅ Billing systems
- ✅ Credit/ledger
- ✅ Any system with money
- ❌ Non-critical systems

**Use `full`:**
- ✅ Complex systems
- ✅ When unsure
- ✅ v4.0 compatibility

---

### Domain Selection

**Always use domain if:**
- Healthcare data (use `healthcare`)
- IoT/sensors (use `iot`)
- Payment/money (use `fintech`)
- Real-time critical (use `realtime`)

**Skip domain if:**
- Standard backend service
- Domain not listed
- Requirements unclear

---

### Security Level

**Use `none`:**
- Internal tools only
- Development/testing
- NOT for production

**Use `basic`:**
- Standard services
- Non-sensitive data
- Internal APIs

**Use `stride-basic`:**
- Customer-facing services
- Some sensitive data
- Production systems

**Use `stride-full`:**
- Financial systems
- Healthcare systems
- Critical infrastructure
- Compliance required

---

### DI Pattern

**Use `--no-di`:**
- Frontend-only
- Static sites
- Scripts

**Use `minimal`:**
- Simple services
- Few dependencies

**Use `full`:**
- Complex services (default)
- Multiple dependencies
- High testability needed

---

## 🐛 Troubleshooting

### Issue: Wrong Profile Auto-Selected

**Solution:**
```bash
smartspec new my-service --profile=backend-service
```
Explicitly specify profile.

---

### Issue: Too Much Detail

**Solution:**
```bash
smartspec new my-tool --profile=basic --mode=compact
```
Use basic profile + compact mode.

---

### Issue: Missing Security Section

**Solution:**
```bash
smartspec new my-api --security=stride-basic
```
Explicitly request security.

---

### Issue: Can't Update Critical Section

**Solution:**
```bash
smartspec edit spec.md --force-update=stride
```
Use force-update flag.

---

### Issue: Detection Wrong

**Solution:**
1. Use explicit flags
2. Update keywords in config
3. Use domain hints

---

## 📞 Support

### Documentation
- This file: Complete guide
- Config template: `smartspec.config.json`
- Examples: See Usage Examples section

### Issues
- Report detection errors
- Suggest keyword improvements
- Request new domains
- Share feedback

---

## 🔮 Future (v5.1+)

**Planned:**
- [ ] Custom plugins
- [ ] Diagram generation
- [ ] Template library
- [ ] AI-assisted detection
- [ ] Visual SPEC editor

---

**Version:** 5.0.0  
**Status:** Production Ready  
**Backward Compatible:** 100%  
**Release Date:** December 3, 2025
