# SmartSpec Validators - Cross-Reference Index

**Last Updated:** 2024-12-27
**Version:** 2.0

---

## Quick Navigation

### Documentation
- [Main README](../README.md#validators-5-scripts--new) - Overview in main docs
- [Validators README](scripts/VALIDATORS_README.md) - Complete guide
- [Knowledge Base](knowledge_base_validators.md) - Detailed knowledge base
- [This Index](VALIDATORS_INDEX.md) - Cross-references

### Reports
- [Fixes Completion Report](../FIXES_COMPLETION_REPORT.md) - Technical details
- [Final Report (Thai)](../FINAL_REPORT_TH.md) - Summary in Thai
- [Audit Report](../VALIDATORS_AUDIT_REPORT.md) - Security audit
- [Critical Issues Analysis](../CRITICAL_ISSUES_ANALYSIS.md) - Issue analysis

### Code
- [Base Validator](scripts/base_validator.py) - Base class
- [Unit Tests](scripts/test_base_validator.py) - Test suite
- [Validators](scripts/) - All validator scripts

---

## Validators by Workflow

### Core Development Workflows

| Workflow | Validator | Documentation | Status |
|----------|-----------|---------------|--------|
| generate_spec_from_prompt | validate_spec_from_prompt.py | [Guide](scripts/VALIDATORS_README.md#1-validate_spec_from_promptpy-) | ✅ v2.0 |
| generate_spec | validate_generate_spec.py | [Guide](scripts/VALIDATORS_README.md#2-validate_generate_specpy) | ✅ v1.1 |
| generate_plan | validate_generate_plan.py | [Guide](scripts/VALIDATORS_README.md#3-validate_generate_planpy) | ✅ v1.1 |
| generate_tests | validate_generate_tests.py | [Guide](scripts/VALIDATORS_README.md#4-validate_generate_testspy) | ✅ v1.1 |
| generate_ui_spec | validate_ui_spec.py | [Guide](scripts/VALIDATORS_README.md#5-validate_ui_specpy) | ✅ Prod |

---

## Validators by Feature

### Security Features

| Feature | Implementation | Documentation | Status |
|---------|----------------|---------------|--------|
| Path Traversal Prevention | base_validator.py:68-85 | [Security](knowledge_base_validators.md#1-path-traversal-prevention) | ✅ |
| File Size Limit | base_validator.py:99-109 | [Security](knowledge_base_validators.md#2-file-size-limit-dos-protection) | ✅ |
| File Type Validation | base_validator.py:73-78 | [Security](knowledge_base_validators.md#3-file-type-validation) | ✅ |
| TOCTOU Protection | base_validator.py:111-121 | [Security](knowledge_base_validators.md#4-toctou-protection) | ✅ |
| Symlink Resolution | base_validator.py:61 | [Security](knowledge_base_validators.md#5-additional-security) | ✅ |

### Validation Features

| Feature | Implementation | Documentation | Status |
|---------|----------------|---------------|--------|
| Structure Validation | base_validator.py:163-195 | [Validation](knowledge_base_validators.md#usage-patterns) | ✅ |
| Naming Validation | base_validator.py:197-220 | [Validation](scripts/VALIDATORS_README.md#common-features) | ✅ |
| Auto-fix Logic | base_validator.py:222-242 | [Auto-fix](knowledge_base_validators.md#2-auto-fix-pattern) | ✅ |
| Report Generation | base_validator.py:280-320 | [Reports](scripts/VALIDATORS_README.md#common-features) | ✅ |

---

## Documentation by Topic

### Getting Started

1. [Quick Start](../README.md#validators-5-scripts--new) - 5-minute intro
2. [Installation](scripts/VALIDATORS_README.md#installation) - Setup guide
3. [Usage Examples](scripts/VALIDATORS_README.md#usage-examples) - Common patterns
4. [Best Practices](knowledge_base_validators.md#best-practices) - Recommended usage

### Advanced Topics

1. [Architecture](knowledge_base_validators.md#architecture) - System design
2. [Security](knowledge_base_validators.md#security-features) - Security details
3. [Testing](knowledge_base_validators.md#testing) - Test suite
4. [Performance](knowledge_base_validators.md#performance) - Performance metrics

### Troubleshooting

1. [Common Issues](scripts/VALIDATORS_README.md#troubleshooting) - FAQ
2. [Error Messages](knowledge_base_validators.md#troubleshooting) - Error guide
3. [Migration Guide](scripts/VALIDATORS_README.md#migration-guide) - Upgrade guide

---

## Related Workflows

### Workflow Documentation

| Workflow | Manual | Knowledge Base | Example |
|----------|--------|----------------|---------|
| generate_spec_from_prompt | [Manual](../.smartspec-docs/workflows/generate_spec_from_prompt.md) | [KB](knowledge_base_validators.md#1-validate_spec_from_promptpy) | [Example](scripts/VALIDATORS_README.md#basic-validation) |
| generate_spec | [Manual](../.smartspec-docs/workflows/generate_spec.md) | [KB](knowledge_base_validators.md#2-validate_generate_specpy) | [Example](scripts/VALIDATORS_README.md#usage-examples) |
| generate_plan | [Manual](../.smartspec-docs/workflows/generate_plan.md) | [KB](knowledge_base_validators.md#3-validate_generate_planpy) | [Example](scripts/VALIDATORS_README.md#batch-validation) |
| generate_tests | [Manual](../.smartspec-docs/workflows/generate_tests.md) | [KB](knowledge_base_validators.md#4-validate_generate_testspy) | [Example](scripts/VALIDATORS_README.md#cicd-integration) |
| generate_ui_spec | [Manual](../.smartspec-docs/workflows/generate_ui_spec.md) | [KB](knowledge_base_validators.md#5-validate_ui_specpy) | [Example](scripts/VALIDATORS_README.md#generate-report) |

---

## Code References

### Base Class

| Component | File | Lines | Documentation |
|-----------|------|-------|---------------|
| BaseValidator | base_validator.py | 1-413 | [Guide](knowledge_base_validators.md#architecture) |
| Security | base_validator.py | 40-121 | [Security](knowledge_base_validators.md#security-features) |
| Parsing | base_validator.py | 123-161 | [Parsing](scripts/VALIDATORS_README.md#common-features) |
| Validation | base_validator.py | 163-220 | [Validation](knowledge_base_validators.md#usage-patterns) |
| Auto-fix | base_validator.py | 222-242 | [Auto-fix](scripts/VALIDATORS_README.md#auto-fix-capabilities) |
| Reports | base_validator.py | 280-320 | [Reports](knowledge_base_validators.md#1-basic-validation) |

### Specific Validators

| Validator | File | Lines | Base Class | Documentation |
|-----------|------|-------|------------|---------------|
| SpecFromPrompt | validate_spec_from_prompt.py | 1-180 | ✅ Yes | [Guide](scripts/VALIDATORS_README.md#1-validate_spec_from_promptpy-) |
| GenerateSpec | validate_generate_spec.py | 1-419 | ❌ No | [Guide](scripts/VALIDATORS_README.md#2-validate_generate_specpy) |
| GeneratePlan | validate_generate_plan.py | 1-526 | ❌ No | [Guide](scripts/VALIDATORS_README.md#3-validate_generate_planpy) |
| GenerateTests | validate_generate_tests.py | 1-538 | ❌ No | [Guide](scripts/VALIDATORS_README.md#4-validate_generate_testspy) |
| UISpec | validate_ui_spec.py | - | ❌ No | [Guide](scripts/VALIDATORS_README.md#5-validate_ui_specpy) |

### Tests

| Test Suite | File | Tests | Coverage | Documentation |
|------------|------|-------|----------|---------------|
| Base Validator | test_base_validator.py | 19 | 100% | [Testing](knowledge_base_validators.md#testing) |
| Security | test_base_validator.py | 6 | 100% | [Security Tests](knowledge_base_validators.md#unit-tests) |
| Parsing | test_base_validator.py | 3 | 100% | [Parsing Tests](knowledge_base_validators.md#unit-tests) |
| Validation | test_base_validator.py | 4 | 100% | [Validation Tests](knowledge_base_validators.md#unit-tests) |
| Auto-fix | test_base_validator.py | 3 | 100% | [Auto-fix Tests](knowledge_base_validators.md#unit-tests) |
| Integration | test_base_validator.py | 3 | 100% | [Integration Tests](knowledge_base_validators.md#unit-tests) |

---

## Reports and Analysis

### Completion Reports

| Report | Topic | Language | Audience |
|--------|-------|----------|----------|
| [FIXES_COMPLETION_REPORT.md](../FIXES_COMPLETION_REPORT.md) | Technical details of v2.0 | English | Developers |
| [FINAL_REPORT_TH.md](../FINAL_REPORT_TH.md) | Summary of changes | Thai | All users |
| [FINAL_SUMMARY.md](../FINAL_SUMMARY.md) | Quick summary | Thai | Management |

### Audit Reports

| Report | Topic | Focus | Status |
|--------|-------|-------|--------|
| [VALIDATORS_AUDIT_REPORT.md](../VALIDATORS_AUDIT_REPORT.md) | Security audit | Security | ✅ Complete |
| [CRITICAL_ISSUES_ANALYSIS.md](../CRITICAL_ISSUES_ANALYSIS.md) | Issue analysis | Problems & Solutions | ✅ Complete |
| [AUDIT_SUMMARY_TH.md](../AUDIT_SUMMARY_TH.md) | Audit summary | Overview (Thai) | ✅ Complete |

---

## Version History

### v2.0 (2024-12-27) - Major Update

**Changes:**
- ✅ Fixed auto-fix logic bug
- ✅ Added security features
- ✅ Created base class
- ✅ Reduced code 69%
- ✅ Added 19 unit tests

**Documentation:**
- [Fixes Report](../FIXES_COMPLETION_REPORT.md)
- [Final Report](../FINAL_REPORT_TH.md)
- [Changelog](scripts/VALIDATORS_README.md#changelog)

### v1.1 (2024-12-27) - Bug Fix

**Changes:**
- ✅ Fixed auto-fix in 3 validators

**Documentation:**
- [Changelog](scripts/VALIDATORS_README.md#version-11-2024-12-27)

### v1.0 (2024-12-26) - Initial Release

**Changes:**
- ✅ Created 4 new validators
- ✅ 100% coverage

**Documentation:**
- [Initial README](scripts/old-validators/)
- [Changelog](scripts/VALIDATORS_README.md#version-10-2024-12-26)

---

## Integration Points

### With SmartSpec Workflows

```
generate_spec_from_prompt
    ↓
validate_spec_from_prompt.py
    ↓
generate_plan
    ↓
validate_generate_plan.py
    ↓
generate_tasks
    ↓
generate_tests
    ↓
validate_generate_tests.py
```

**Documentation:**
- [Integration Guide](knowledge_base_validators.md#integration-with-smartspec-workflows)
- [Workflow Integration](scripts/VALIDATORS_README.md#best-practices)

### With CI/CD

```yaml
# .github/workflows/validate.yml
- name: Validate Specs
  run: |
    find .spec -name "*.md" -exec python3 .smartspec/scripts/validate_spec_from_prompt.py {} \;
```

**Documentation:**
- [CI/CD Integration](scripts/VALIDATORS_README.md#cicd-integration)
- [Best Practices](knowledge_base_validators.md#4-use-in-cicd)

### With Pre-commit Hooks

```bash
# .git/hooks/pre-commit
for file in $(git diff --cached --name-only | grep '\.spec.*\.md$'); do
    python3 .smartspec/scripts/validate_spec_from_prompt.py "$file" || exit 1
done
```

**Documentation:**
- [Pre-commit Integration](scripts/VALIDATORS_README.md#use-in-pre-commit-hooks)
- [Best Practices](knowledge_base_validators.md#2-use-in-pre-commit-hooks)

---

## Quick Reference

### Common Commands

```bash
# Preview validation
python3 validate_spec_from_prompt.py spec.md

# Apply fixes
python3 validate_spec_from_prompt.py spec.md --apply

# Generate report
python3 validate_spec_from_prompt.py spec.md --output report.md

# With repo root
python3 validate_spec_from_prompt.py spec.md --repo-root /path/to/repo

# Run tests
python3 test_base_validator.py

# Batch validation
for file in .spec/**/*.md; do
    python3 validate_spec_from_prompt.py "$file"
done
```

### Common Issues

| Issue | Solution | Documentation |
|-------|----------|---------------|
| Auto-fix not working | Use `--apply` flag | [Troubleshooting](scripts/VALIDATORS_README.md#issue-auto-fix-not-working) |
| File outside repo | Use `--repo-root` flag | [Troubleshooting](scripts/VALIDATORS_README.md#issue-file-outside-repository-error) |
| File too large | Split or compress | [Troubleshooting](scripts/VALIDATORS_README.md#issue-file-too-large-error) |
| Invalid file type | Use .md or .json | [Troubleshooting](scripts/VALIDATORS_README.md#issue-invalid-file-type) |

---

## External Links

### GitHub

- [SmartSpec Repository](https://github.com/naibarn/SmartSpec)
- [Validators Directory](https://github.com/naibarn/SmartSpec/tree/main/.smartspec/scripts)
- [Issues](https://github.com/naibarn/SmartSpec/issues)
- [Pull Requests](https://github.com/naibarn/SmartSpec/pulls)

### Related Projects

- [LangGraph](https://github.com/langchain-ai/langgraph) - Multi-agent orchestration
- [LangChain](https://github.com/langchain-ai/langchain) - LLM framework

---

## Support

### Documentation

1. **Start here:** [Main README](../README.md#validators-5-scripts--new)
2. **Complete guide:** [Validators README](scripts/VALIDATORS_README.md)
3. **Deep dive:** [Knowledge Base](knowledge_base_validators.md)
4. **This index:** Cross-references and navigation

### Getting Help

1. Check error messages (they're descriptive!)
2. Search this index
3. Check [Troubleshooting](scripts/VALIDATORS_README.md#troubleshooting)
4. Check [FAQ](knowledge_base_validators.md#troubleshooting)
5. Open an issue on GitHub

---

**Last Updated:** 2024-12-27
**Maintained by:** SmartSpec Team
**Status:** Production Ready
