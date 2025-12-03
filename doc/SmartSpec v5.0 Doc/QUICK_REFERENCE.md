# SmartSpec v5.0 - Quick Reference Card

---

## 🚀 Quick Commands

```bash
# Basic tool
smartspec new NAME --profile=basic --mode=compact

# Standard service
smartspec new NAME --profile=backend-service

# Financial system
smartspec new NAME --profile=financial

# With domain
smartspec new NAME --domain=iot

# Edit with force update
smartspec edit spec.md --force-update=stride
```

---

## 📦 Profiles

| Profile | Sections | Use Case |
|---------|----------|----------|
| **basic** | 5 | Simple tools, CRUD |
| **backend-service** | 10 | Most services, APIs |
| **financial** | 13+ | Payment, billing |
| **full** | All | v4.0 compat |

---

## 🎛️ Flags

### Profile
```
--profile=basic|backend-service|financial|full
```

### Mode
```
--mode=standard|compact
```

### Security
```
--security=none|basic|stride-basic|stride-full|auto
```

### DI Pattern
```
--di=none|minimal|full|auto
--no-di  (same as --di=none)
```

### Performance
```
--performance=none|basic|full|auto
```

### Domain
```
--domain=healthcare|iot|logistics|ai|fintech|saas|internal
```

### Force Update
```
--force-update=all
--force-update=stride,config,di
```

### Output
```
--no-backup
--no-report
--output-dir=PATH
```

### Validation
```
--validate-consistency
--no-validation
```

---

## 🌍 Domains

| Domain | Auto-Adds |
|--------|-----------|
| **healthcare** | HIPAA, audit, privacy |
| **iot** | High throughput, batch |
| **logistics** | High SLA, tracking |
| **ai** | Latency, GPU, models |
| **fintech** | Same as financial profile |
| **saas** | Scalability, multi-tenant |
| **internal** | Lower requirements |

---

## 📝 Common Patterns

### Simple Internal Tool
```bash
smartspec new admin-dashboard \
  --profile=basic \
  --mode=compact \
  --domain=internal \
  --no-di
```

### REST API
```bash
smartspec new products-api \
  --profile=backend-service \
  --security=stride-basic
```

### Payment System
```bash
smartspec new checkout-service \
  --profile=financial
```

### IoT Service
```bash
smartspec new telemetry-collector \
  --domain=iot \
  --profile=backend-service
```

### Healthcare API
```bash
smartspec new patient-api \
  --domain=healthcare \
  --security=stride-full
```

---

## 🔧 Meta Tags

```markdown
<!-- @critical security -->
## Security Threat Model
...
<!-- @end-critical -->

<!-- @critical config -->
## Configuration Schema
...
<!-- @end-critical -->

<!-- @critical di -->
## Dependency Injection
...
<!-- @end-critical -->

<!-- @critical monitoring -->
## Monitoring
...
<!-- @end-critical -->
```

---

## ⚙️ Config File

**Project:** `smartspec.config.json`
```json
{
  "version": "5.0.0",
  "defaults": {
    "profile": "backend-service",
    "security": "basic",
    "di": "full"
  }
}
```

**Organization:** `.smartspec/config.json`
```json
{
  "validation": {
    "enabled": true
  },
  "output": {
    "createBackups": true
  }
}
```

---

## ✅ Consistency Rules

| Rule | Check |
|------|-------|
| API Coverage | APIs in Architecture → Examples |
| Queue Metrics | Queue mentioned → queue metrics |
| Integration Tests | Transactions → integration tests |
| Retry Policy | External API → retry/backoff |
| Security Section | Auth mentioned → security |

---

## 📊 When to Use What

### Profile Selection

```
Simple tool (< 100 users)
→ --profile=basic

Standard backend service
→ --profile=backend-service

Financial/Payment system
→ --profile=financial

Unsure / Complex
→ --profile=full
```

### Security Level

```
Internal only
→ --security=none

Standard service
→ --security=basic

Production customer-facing
→ --security=stride-basic

Financial/Healthcare/Critical
→ --security=stride-full
```

### DI Pattern

```
Frontend / Scripts
→ --no-di

Simple service (few deps)
→ --di=minimal

Complex service (many deps)
→ --di=full
```

---

## 🔄 Migration from v4.0

**100% Backward Compatible!**

```bash
# v4.0 command still works
smartspec new my-service

# v5.0 uses --profile=full by default
```

**Add meta tags:**
```bash
smartspec migrate specs/ --add-meta-tags --recursive
```

**Create config:**
```bash
smartspec init-config
```

---

## 🐛 Troubleshooting

**Wrong profile?**
```bash
# Explicit profile
smartspec new NAME --profile=backend-service
```

**Too much detail?**
```bash
# Use compact
smartspec new NAME --profile=basic --mode=compact
```

**Can't update critical?**
```bash
# Force update
smartspec edit spec.md --force-update=stride
```

**Detection wrong?**
```bash
# Use explicit flags
smartspec new NAME --domain=TYPE --security=LEVEL
```

---

## 💡 Pro Tips

1. **Start with basic**, upgrade later if needed
2. **Use domains** for auto-configuration
3. **Add meta tags** to existing SPECs
4. **Create config file** for consistency
5. **Validate** with --validate-consistency
6. **Use compact mode** for prototypes
7. **Force update** when needed

---

## 📚 Documentation

- **SMARTSPEC_V5_DOCUMENTATION.md** - Complete guide
- **MIGRATION_GUIDE_V4_TO_V5.md** - Migration guide
- **SMARTSPEC_V5_SUMMARY_TH.md** - Thai summary
- **smartspec.config.json** - Config template
- **performance-domains.json** - Domain rules

---

## 🎯 Quick Decision Tree

```
Is it financial/payment?
  YES → --profile=financial
  NO  → Continue

Is it simple CRUD/tool?
  YES → --profile=basic --mode=compact
  NO  → Continue

Is it standard backend?
  YES → --profile=backend-service
  NO  → --profile=full
```

---

**Version:** 5.0.0  
**Keep this handy!**  
**Print and post near desk 📌**
