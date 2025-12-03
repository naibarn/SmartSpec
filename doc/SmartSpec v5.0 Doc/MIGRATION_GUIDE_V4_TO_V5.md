# Migration Guide: SmartSpec v4.0 → v5.0

**Date:** December 3, 2025  
**Status:** Complete  
**Difficulty:** Easy (100% backward compatible)

---

## 🎯 Overview

SmartSpec v5.0 is **100% backward compatible** with v4.0. All v4.0 commands work in v5.0.

**Key Improvements:**
- More flexible with profiles
- Better control over sections
- Domain-based intelligence
- Organized output structure

---

## 📊 What Changed

### ✅ Added Features (New in v5.0)

| Feature | v4.0 | v5.0 |
|---------|------|------|
| Profiles | ❌ None | ✅ 4 profiles |
| Meta Tags | ❌ Keyword detection | ✅ Precise tags |
| Compact Mode | ❌ Full only | ✅ 5-section option |
| Domains | ❌ None | ✅ 8 domains |
| DI Control | Auto only | ✅ none/minimal/full |
| STRIDE Levels | Full only | ✅ basic/full |
| Force Update | ❌ | ✅ Selective updates |
| Consistency | ❌ | ✅ Validation rules |
| Config File | ❌ | ✅ Project/org config |

### 🔄 Changed Behavior

**v4.0:** Auto-detect everything, fixed structure
**v5.0:** Choose profile, customize sections

**Default Behavior:**
```bash
# v4.0
smartspec new my-service
→ Full auto-detection

# v5.0 (same command)
smartspec new my-service
→ Uses --profile=full (backward compatible)
```

### 🚫 Nothing Removed

All v4.0 features work in v5.0!

---

## 🚀 Migration Paths

### Path 1: No Changes (Recommended)

**Best for:** Teams happy with v4.0

```bash
# Keep using v4.0 commands
smartspec new my-service

# v5.0 uses --profile=full by default
# Behavior identical to v4.0
```

**Result:** Zero changes needed ✅

---

### Path 2: Gradual Adoption

**Best for:** Teams wanting flexibility

**Step 1:** Start using profiles for new SPECs
```bash
# New internal tools
smartspec new admin-tool --profile=basic

# New microservices
smartspec new order-service --profile=backend-service

# Financial systems
smartspec new payment-api --profile=financial
```

**Step 2:** Existing SPECs stay unchanged

**Step 3:** Migrate when convenient

**Result:** Mix of v4.0 and v5.0 styles ✅

---

### Path 3: Full Migration

**Best for:** Teams wanting full v5.0 benefits

**Step 1:** Add meta tags to existing SPECs
```bash
smartspec migrate specs/ --add-meta-tags --recursive
```

**Step 2:** Create config file
```bash
smartspec init-config
```

**Step 3:** Update workflows
```bash
# Old workflow
smartspec new my-service

# New workflow
smartspec new my-service --profile=backend-service
```

**Result:** Full v5.0 adoption ✅

---

## 🔧 Adding Meta Tags to Existing SPECs

### Manual Method

Edit your SPEC and add tags:

```markdown
<!-- @critical security -->
## Security Threat Model (STRIDE)
...content...
<!-- @end-critical -->

<!-- @critical config -->
## Configuration Schema
...content...
<!-- @end-critical -->

<!-- @critical di -->
## Dependency Injection Pattern
...content...
<!-- @end-critical -->

<!-- @critical monitoring -->
## Monitoring & Observability
...content...
<!-- @end-critical -->
```

### Automated Method

```bash
# Single file
smartspec migrate specs/feature/spec-004/spec.md --add-meta-tags

# Directory
smartspec migrate specs/ --add-meta-tags --recursive

# Dry run first
smartspec migrate specs/ --add-meta-tags --recursive --dry-run
```

### Verification

```bash
smartspec validate specs/feature/spec-004/spec.md
```

Expected output:
```
✅ Meta tags found: 4
  - security (STRIDE model)
  - config (Configuration Schema)
  - di (Dependency Injection)
  - monitoring (Observability)

✅ SPEC is v5.0 compatible
```

---

## 📝 Updating Workflows

### Before (v4.0)

```bash
# Create SPEC
smartspec new payment-service

# Edit SPEC
smartspec edit specs/feature/spec-004/spec.md

# Generate tasks
smartspec generate-tasks specs/feature/spec-004/spec.md
```

### After (v5.0 - Recommended)

```bash
# Create SPEC with profile
smartspec new payment-service --profile=financial

# Edit SPEC with force-update
smartspec edit specs/feature/spec-004/spec.md \
  --force-update=stride \
  --validate-consistency

# Generate tasks (unchanged)
smartspec generate-tasks specs/feature/spec-004/spec.md
```

### Benefits

- ✅ More control over sections
- ✅ Selective critical section updates
- ✅ Consistency validation
- ✅ Appropriate detail level

---

## ⚙️ Creating Configuration Files

### Step 1: Initialize

```bash
smartspec init-config
```

Creates:
- `smartspec.config.json` (project config)
- `.smartspec/config.json` (organization config)

### Step 2: Customize

**Project Config** (`smartspec.config.json`):
```json
{
  "version": "5.0.0",
  "defaults": {
    "profile": "backend-service",
    "security": "stride-basic",
    "di": "full"
  },
  "organization": {
    "name": "My Company",
    "defaultAuthor": "Engineering Team"
  }
}
```

**Organization Config** (`.smartspec/config.json`):
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
  },
  "output": {
    "directory": ".smartspec/",
    "createBackups": true
  }
}
```

### Step 3: Commit

```bash
git add smartspec.config.json
git add .smartspec/config.json
git commit -m "Add SmartSpec v5.0 configuration"
```

---

## 🎓 Training Team

### Quick Start Guide for Team

**For Simple Tools:**
```bash
smartspec new tool-name --profile=basic --mode=compact
```

**For Standard Services:**
```bash
smartspec new service-name --profile=backend-service
```

**For Financial Systems:**
```bash
smartspec new payment-name --profile=financial
```

**For Updates:**
```bash
smartspec edit spec.md --validate-consistency
```

### Cheat Sheet

Create `SMARTSPEC_CHEATSHEET.md`:
```markdown
# SmartSpec v5.0 Cheat Sheet

## Profiles
- basic: Simple tools (5 sections)
- backend-service: Standard service (10 sections)
- financial: Critical system (13+ sections)

## Common Commands
smartspec new NAME --profile=TYPE
smartspec edit spec.md --force-update=SECTION
smartspec validate spec.md

## Flags
--mode=compact          # Short SPEC
--security=stride-basic # Security table
--domain=DOMAIN         # Auto-configure for domain
--validate-consistency  # Check alignment
```

---

## 📊 Migration Checklist

### Pre-Migration

- [ ] Read v5.0 documentation
- [ ] Review existing SPECs
- [ ] Identify critical sections
- [ ] Test v5.0 on sample SPEC
- [ ] Plan rollout strategy

### During Migration

- [ ] Update SmartSpec to v5.0
- [ ] Create configuration files
- [ ] Add meta tags to existing SPECs
- [ ] Test workflows
- [ ] Train team

### Post-Migration

- [ ] Verify all SPECs work
- [ ] Update documentation
- [ ] Monitor for issues
- [ ] Collect feedback
- [ ] Optimize configuration

---

## 🔍 Common Migration Scenarios

### Scenario 1: Team of 5, Small Project

**Recommendation:** Path 1 (No Changes)

```bash
# Keep using v4.0 commands
smartspec new my-service
```

**Reason:** Not worth the effort for small team

---

### Scenario 2: Growing Team, Multiple Projects

**Recommendation:** Path 2 (Gradual Adoption)

```bash
# New projects: Use profiles
smartspec new new-service --profile=backend-service

# Existing projects: Keep as-is
```

**Reason:** Get benefits without disruption

---

### Scenario 3: Large Team, Established Process

**Recommendation:** Path 3 (Full Migration)

```bash
# 1. Add meta tags
smartspec migrate specs/ --add-meta-tags --recursive

# 2. Create configs
smartspec init-config

# 3. Update all workflows
```

**Reason:** Maximize v5.0 benefits

---

### Scenario 4: Critical Systems Only

**Recommendation:** Use v5.0 for critical only

```bash
# Financial systems: v5.0
smartspec new payment --profile=financial

# Other systems: v4.0
smartspec new internal-tool
```

**Reason:** Better control for critical systems

---

## 🐛 Troubleshooting Migration

### Issue: Meta Tags Not Working

**Symptom:** Force update still blocked

**Solution:**
```bash
# Verify meta tags
smartspec validate spec.md

# Check format
<!-- @critical security -->
...
<!-- @end-critical -->
```

---

### Issue: Config Not Loaded

**Symptom:** Defaults not applied

**Solution:**
```bash
# Check config location
ls smartspec.config.json
ls .smartspec/config.json

# Validate config
smartspec validate-config
```

---

### Issue: Profiles Not Available

**Symptom:** "Unknown profile" error

**Solution:**
```bash
# List available profiles
smartspec list-profiles

# Use correct name
--profile=backend-service
# NOT: --profile=backend
```

---

### Issue: Backward Compatibility Broken

**Symptom:** v4.0 commands fail

**Solution:**
```bash
# Should never happen!
# Report as bug

# Workaround: Use --profile=full
smartspec new service --profile=full
```

---

## 📈 Migration Timeline

### Week 1: Planning
- Review documentation
- Test on sample SPECs
- Choose migration path
- Plan training

### Week 2: Setup
- Update SmartSpec
- Create configs
- Add meta tags to critical SPECs
- Document changes

### Week 3: Training
- Train team
- Create cheat sheets
- Run workshops
- Answer questions

### Week 4: Rollout
- Start using v5.0 for new SPECs
- Monitor issues
- Collect feedback
- Adjust as needed

### Ongoing
- Gradually migrate existing SPECs
- Refine configuration
- Share best practices

---

## ✅ Success Criteria

**You've successfully migrated when:**

1. ✅ Team uses profiles for new SPECs
2. ✅ Critical SPECs have meta tags
3. ✅ Configuration files in place
4. ✅ No v4.0 vs v5.0 confusion
5. ✅ Team prefers v5.0 flexibility

**Metrics to Track:**
- % SPECs using profiles
- % SPECs with meta tags
- Time saved on SPEC creation
- Team satisfaction

---

## 🎉 Benefits After Migration

**Before v4.0:**
- ❌ One size fits all
- ❌ Can't update critical sections
- ❌ Keywords cause false positives
- ❌ No consistency checks

**After v5.0:**
- ✅ Right-sized SPECs
- ✅ Selective updates allowed
- ✅ Precise meta tags
- ✅ Automated validation
- ✅ Configuration management

---

## 📞 Support During Migration

**Questions?**
- Read: SMARTSPEC_V5_DOCUMENTATION.md
- Check: smartspec.config.json examples
- Ask: Team leads

**Issues?**
- Check troubleshooting section
- Validate configuration
- Report bugs

**Feedback?**
- Share what works
- Report pain points
- Suggest improvements

---

**Migration Guide Version:** 1.0  
**SmartSpec Version:** 5.0.0  
**Last Updated:** December 3, 2025
