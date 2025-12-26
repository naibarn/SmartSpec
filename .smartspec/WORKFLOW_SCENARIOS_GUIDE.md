# SmartSpec Workflow Scenarios & Best Practices Guide

**Version:** 6.2.0  
**Purpose:** Practical guidance for common scenarios and parameter combinations  
**Audience:** AI agents and users seeking workflow usage recommendations

---

## How to Use This Guide

This guide provides **scenario-based recommendations** for using SmartSpec workflows effectively. Each scenario includes:

- **Context:** When to use this approach
- **Recommended workflow(s):** Which workflows to use
- **Parameter combinations:** Specific flags and their purposes
- **Command examples:** Both CLI and Kilo Code
- **Best practices:** Tips for optimal results
- **Common pitfalls:** What to avoid

### Important: Dual-Syntax Requirement

**When answering user questions about workflow usage, ALWAYS provide BOTH syntaxes:**

1. **CLI syntax:** `/workflow_name <args> --flags`
2. **Kilo Code syntax:** `/workflow_name.md <args> --flags --platform kilo`

**Example:**

**CLI:**
```bash
/smartspec_generate_spec --spec specs/feature/spec-001/spec.md --apply
```

**Kilo Code:**
```bash
/smartspec_generate_spec.md --spec specs/feature/spec-001/spec.md --apply --platform kilo
```

**Rules:**
- MUST show both syntaxes for every workflow command recommendation
- Kilo Code MUST include `--platform kilo` flag
- Use code blocks for clarity
- If a scenario below shows only one syntax, generate the other syntax following this pattern

### Important: Directory Structure and Design Principle

**CRITICAL:** SmartSpec follows a strict separation between read-only and read-write directories:

- **`.smartspec/`** = Read-Only (workflows, scripts, knowledge) - ❌ NEVER write here
- **`.spec/`** = Read-Write (reports, specs, registry) - ✅ ALWAYS write reports here

**All workflow outputs MUST go to `.spec/reports/`**, NOT `.smartspec/reports/`.

**Correct:**
```bash
--out .spec/reports/implement-tasks/spec-core-001-auth
```

**Incorrect:**
```bash
--out .smartspec/reports/...  ❌ (violates read-only principle)
```

For detailed explanation, see Section 0.5 in `knowledge_base_smartspec_handbook.md`.

---

## Table of Contents

1. [Starting a New Feature](#1-starting-a-new-feature)
2. [Implementing from Specifications](#2-implementing-from-specifications)
3. [Validating Implementation Progress](#3-validating-implementation-progress)
4. [API Contract Validation](#4-api-contract-validation)
5. [Production Deployment](#5-production-deployment)
6. [Security Auditing](#6-security-auditing)
7. [Performance Optimization](#7-performance-optimization)
8. [Emergency Hotfix](#8-emergency-hotfix)
9. [Documentation Generation](#9-documentation-generation)
10. [CI/CD Integration](#10-cicd-integration)

---

## 1. Starting a New Feature

### Context
You have a feature idea but no formal specification yet.

### Recommended Workflow
`smartspec_generate_spec_from_prompt` → `smartspec_generate_spec`

### Step 1: Generate Draft Spec

**CLI:**
```bash
/smartspec_generate_spec_from_prompt \
  "User authentication system with OAuth2, JWT tokens, and role-based access control" \
  --out .spec/reports/generate-spec-from-prompt \
  --json
```

**Kilo Code:**
```bash
/smartspec_generate_spec_from_prompt.md \
  "User authentication system with OAuth2, JWT tokens, and role-based access control" \
  --out .spec/reports/generate-spec-from-prompt \
  --json \
  --platform kilo
```

**Parameter Explanation:**
- `--out`: Where to save the draft spec (safe output, no `--apply` needed)
- `--json`: Machine-readable output for automation

### Step 2: Human Review and Edit
Manually review and refine the generated draft at:
`.spec/reports/generate-spec-from-prompt/<run-id>/draft_spec.md`

### Step 3: Finalize Spec

**CLI:**
```bash
/smartspec_generate_spec \
  --spec specs/feature/spec-003-auth-system/spec.md \
  --apply
```

**Kilo Code:**
```bash
/smartspec_generate_spec.md \
  --spec specs/feature/spec-003-auth-system/spec.md \
  --apply \
  --platform kilo
```

**Parameter Explanation:**
- `--apply`: Required because spec.md is a governed artifact
- `--spec`: Path to the spec file to refine

### Best Practices
✅ Keep prompts focused and specific  
✅ Include NFRs (performance, security, scalability) in prompt  
✅ Always human-review before finalizing  
✅ Use `--apply` only after review  

### Common Pitfalls
❌ Skipping human review  
❌ Vague prompts leading to unclear specs  
❌ Forgetting to specify NFRs  

---

## 2. Implementing from Specifications

### Context
You have a finalized spec and want to implement it.

### Recommended Workflow
`smartspec_generate_plan` → `smartspec_generate_tasks` → `smartspec_implement_tasks`

### Step 1: Generate Plan

**CLI:**
```bash
/smartspec_generate_plan \
  specs/feature/spec-003-auth-system/spec.md \
  --apply
```

**Parameter Explanation:**
- Positional argument: spec.md path
- `--apply`: Required (plan.md is governed)

### Step 2: Generate Tasks

**CLI:**
```bash
/smartspec_generate_tasks \
  specs/feature/spec-003-auth-system/spec.md \
  --apply
```

**Parameter Explanation:**
- Positional argument: spec.md path
- `--apply`: Required (tasks.md is governed)

### Step 3: Implement (Validation Only First)

**CLI:**
```bash
/smartspec_implement_tasks \
  specs/feature/spec-003-auth-system/tasks.md \
  --validate-only \
  --out .spec/reports/implement-tasks/spec-003 \
  --json
```

**Parameter Explanation:**
- `--validate-only`: Preview changes without writing
- `--out`: Where to save validation report
- `--json`: Structured output

### Step 4: Implement (Actual Changes)

**CLI:**
```bash
/smartspec_implement_tasks \
  specs/feature/spec-003-auth-system/tasks.md \
  --apply \
  --out .spec/reports/implement-tasks/spec-003 \
  --json
```

**Parameter Explanation:**
- `--apply`: Required for actual code changes (governed artifacts)

### Best Practices
✅ Always run `--validate-only` first  
✅ Review change_plan.md before applying  
✅ Use `--allow-network` only when needed (dependency installation)  
✅ Commit after each successful implementation  

### Common Pitfalls
❌ Skipping validation step  
❌ Not reviewing change plan  
❌ Not using `--apply` for actual changes  

---

## 3. Validating Implementation Progress

### Context
You want to check which tasks are actually complete (not just checked off).

### Recommended Workflow
`smartspec_verify_tasks_progress_strict` → `smartspec_sync_tasks_checkboxes`

### Step 1: Strict Verification

**CLI:**
```bash
/smartspec_verify_tasks_progress_strict \
  specs/feature/spec-003-auth-system/tasks.md \
  --out .spec/reports/verify-tasks-progress/spec-003 \
  --json
```

**Kilo Code:**
```bash
/smartspec_verify_tasks_progress_strict.md \
  specs/feature/spec-003-auth-system/tasks.md \
  --out .spec/reports/verify-tasks-progress/spec-003 \
  --json \
  --platform kilo
```

**Parameter Explanation:**
- Positional argument: tasks.md path
- `--out`: Where to save verification report (safe output)
- `--json`: Machine-readable results

### Step 2: Sync Checkboxes

**CLI:**
```bash
/smartspec_sync_tasks_checkboxes \
  specs/feature/spec-003-auth-system/tasks.md \
  --apply
```

**Parameter Explanation:**
- `--apply`: Required (tasks.md is governed)

### Best Practices
✅ Never trust checkboxes alone  
✅ Run strict verification before claiming completion  
✅ Sync checkboxes to reflect actual progress  
✅ Include verification in CI pipeline  

### Common Pitfalls
❌ Manually checking boxes without evidence  
❌ Assuming [x] means done  
❌ Skipping verification before deployment  

---

## 4. API Contract Validation

### Context
You have an OpenAPI spec and want to validate implementation against it.

### Recommended Workflow
`smartspec_api_contract_validator`

### For Development (Warnings OK)

**CLI:**
```bash
/smartspec_api_contract_validator \
  --contract openapi.yaml \
  --implementation-root src/api \
  --spec specs/feature/spec-003-auth-system/spec.md \
  --out .spec/reports/api-contract-validation \
  --json
```

**Parameter Explanation:**
- `--contract`: Path to OpenAPI/GraphQL schema
- `--implementation-root`: Where your API code lives
- `--spec`: Optional, for context
- No `--strict`: Warnings won't fail the check

### For CI/CD (Strict Mode)

**CLI:**
```bash
/smartspec_api_contract_validator \
  --contract openapi.yaml \
  --implementation-root src/api \
  --strict \
  --json
```

**Parameter Explanation:**
- `--strict`: Fail on any MUST requirement violation
- `--json`: Machine-readable for CI parsing

### Best Practices
✅ Use `--strict` in CI/CD  
✅ Use non-strict in development  
✅ Keep contract and spec in sync  
✅ Run validation before merging  

### Common Pitfalls
❌ Using `--strict` too early (blocks development)  
❌ Not running validation in CI  
❌ Contract and implementation drift  

---

## 5. Production Deployment

### Context
You want to plan and execute a production deployment.

### Recommended Workflow
`smartspec_deployment_planner` → `smartspec_release_tagger`

### Step 1: Plan Deployment

**CLI:**
```bash
/smartspec_deployment_planner \
  --environment prod \
  --spec specs/feature/spec-003-auth-system/spec.md \
  --out .spec/reports/deployment-planner \
  --json
```

**Parameter Explanation:**
- `--environment`: Target environment (dev|staging|prod)
- `--spec`: Optional, for context
- `--out`: Where to save deployment plan

### Step 2: Create Release Tag

**CLI:**
```bash
/smartspec_release_tagger \
  --version v1.2.0 \
  --json
```

**Parameter Explanation:**
- `--version`: Semantic version tag (e.g., v1.2.0)
- `--json`: Structured output

### Best Practices
✅ Always plan before deploying  
✅ Use semantic versioning  
✅ Tag releases consistently  
✅ Review deployment plan with team  

### Common Pitfalls
❌ Deploying without a plan  
❌ Inconsistent version numbering  
❌ Skipping staging environment  

---

## 6. Security Auditing

### Context
You want to scan for vulnerabilities and model threats.

### Recommended Workflow
`smartspec_security_audit_reporter` → `smartspec_security_threat_modeler`

### Step 1: Security Audit

**CLI:**
```bash
/smartspec_security_audit_reporter \
  --scope all \
  --out .spec/reports/security-audit \
  --json
```

**Parameter Explanation:**
- `--scope`: What to audit (all|dependencies|code|config)
- `--out`: Where to save audit report

### Step 2: Threat Modeling

**CLI:**
```bash
/smartspec_security_threat_modeler \
  --spec specs/feature/spec-003-auth-system/spec.md \
  --out .spec/reports/security-threat-model \
  --json
```

**Parameter Explanation:**
- `--spec`: Spec to analyze for threats
- `--out`: Where to save threat model

### Best Practices
✅ Run security audit regularly (weekly/monthly)  
✅ Threat model before implementation  
✅ Address high-severity issues immediately  
✅ Include security checks in CI  

### Common Pitfalls
❌ Running security audit only once  
❌ Ignoring dependency vulnerabilities  
❌ Not threat modeling sensitive features  

---

## 7. Performance Optimization

### Context
You want to profile code and plan performance improvements.

### Recommended Workflow
`smartspec_performance_profiler` → `smartspec_refactor_planner`

### Step 1: Profile Performance

**CLI:**
```bash
/smartspec_performance_profiler \
  --target src/api/auth \
  --out .spec/reports/performance-profiler \
  --json
```

**Parameter Explanation:**
- `--target`: Path to code/module to profile
- `--out`: Where to save profiling report

### Step 2: Plan Refactoring

**CLI:**
```bash
/smartspec_refactor_planner \
  --target src/api/auth \
  --out .spec/reports/refactor-planner \
  --json
```

**Parameter Explanation:**
- `--target`: Path to code to analyze
- `--out`: Where to save refactoring plan

### Best Practices
✅ Profile before optimizing  
✅ Focus on bottlenecks identified by profiler  
✅ Plan refactoring before making changes  
✅ Measure performance after changes  

### Common Pitfalls
❌ Premature optimization  
❌ Optimizing without profiling data  
❌ Refactoring without a plan  

---

## 8. Emergency Hotfix

### Context
Production issue requires immediate fix.

### Recommended Workflow
`smartspec_incident_response` → `smartspec_hotfix_assistant` → `smartspec_rollback` (if needed)

### Step 1: Incident Triage

**CLI:**
```bash
/smartspec_incident_response \
  --incident-id INC-2025-001 \
  --mode triage \
  --out .spec/reports/incident-response \
  --json
```

**Parameter Explanation:**
- `--incident-id`: Unique incident identifier
- `--mode`: Operation mode (triage|investigate|postmortem)
- `--out`: Where to save incident report

### Step 2: Hotfix Planning

**CLI:**
```bash
/smartspec_hotfix_assistant \
  --incident-id INC-2025-001 \
  --out .spec/reports/hotfix-assistant \
  --json
```

**Parameter Explanation:**
- `--incident-id`: Link to incident
- `--out`: Where to save hotfix plan

### Step 3: Rollback (If Needed)

**CLI:**
```bash
/smartspec_rollback \
  --environment prod \
  --version v1.1.9 \
  --out .spec/reports/rollback \
  --json
```

**Parameter Explanation:**
- `--environment`: Target environment
- `--version`: Version to roll back to
- `--out`: Where to save rollback plan

### Best Practices
✅ Document incident immediately  
✅ Follow hotfix process  
✅ Test hotfix in staging first (if possible)  
✅ Write post-mortem after resolution  

### Common Pitfalls
❌ Rushing without a plan  
❌ Not documenting the incident  
❌ Skipping post-mortem  

---

## 9. Documentation Generation

### Context
You want to generate and publish technical documentation.

### Recommended Workflow
`smartspec_docs_generator` → `smartspec_docs_publisher`

### Step 1: Generate Documentation

**CLI:**
```bash
/smartspec_docs_generator \
  --mode api-docs \
  --spec specs/feature/spec-003-auth-system/spec.md \
  --out .spec/reports/docs-generator \
  --json
```

**Parameter Explanation:**
- `--mode`: Type of docs (api-docs|user-guide|dev-guide)
- `--spec`: Spec to generate docs from
- `--out`: Where to save generated docs

### Step 2: Publish Documentation

**CLI:**
```bash
/smartspec_docs_publisher \
  --docs-dir .spec/reports/docs-generator/<run-id>/bundle.preview \
  --publish-platform github-pages \
  --version v1.2.0 \
  --allow-network \
  --apply \
  --json
```

**Parameter Explanation:**
- `--docs-dir`: Path to generated documentation
- `--publish-platform`: Where to publish (github-pages|wiki|s3)
- `--version`: Version tag for docs
- `--allow-network`: Required for publishing
- `--apply`: Required for write operations

### Best Practices
✅ Generate docs from specs (single source of truth)  
✅ Version documentation with releases  
✅ Publish to accessible platform  
✅ Keep docs in sync with code  

### Common Pitfalls
❌ Manual documentation (gets outdated)  
❌ Not versioning docs  
❌ Publishing without review  

---

## 10. CI/CD Integration

### Context
You want to integrate SmartSpec workflows into CI/CD pipeline.

### Recommended Workflows
Multiple workflows with `--json` and `--strict` flags

### Quality Gate (CI)

**CLI:**
```bash
/smartspec_quality_gate \
  --strict \
  --out .spec/reports/quality-gate \
  --json
```

**Parameter Explanation:**
- `--strict`: Fail CI on any quality warning
- `--json`: Machine-readable for CI parsing

### Test Suite Runner (CI)

**CLI:**
```bash
/smartspec_test_suite_runner \
  --suite all \
  --out .spec/reports/test-suite-runner \
  --json
```

**Parameter Explanation:**
- `--suite`: Which tests to run (unit|integration|e2e|all)
- `--json`: Structured output for CI

### API Contract Validation (CI)

**CLI:**
```bash
/smartspec_api_contract_validator \
  --contract openapi.yaml \
  --implementation-root src/api \
  --strict \
  --json
```

**Parameter Explanation:**
- `--strict`: Fail CI on contract violations
- `--json`: Machine-readable output

### Best Practices
✅ Use `--json` for all CI workflows  
✅ Use `--strict` for quality gates  
✅ Fail fast on critical issues  
✅ Generate reports for every run  

### Common Pitfalls
❌ Not using `--json` (hard to parse)  
❌ Too lenient quality gates  
❌ Not failing CI on violations  

---

## Universal Flags Reference

These flags are supported by all workflows:

| Flag | Purpose | When to Use |
|---|---|---|
| `--config <path>` | Custom config file | Non-standard project structure |
| `--lang <th\|en>` | Output language | Thai or English output |
| `--platform <cli\|kilo\|ci\|other>` | Platform mode | Kilo Code: use `--platform kilo` |
| `--apply` | Enable writes to governed artifacts | Modifying specs/plans/tasks/indexes |
| `--out <path>` | Output directory | Custom report location |
| `--json` | JSON output | CI/CD, automation, parsing |
| `--quiet` | Suppress non-essential output | CI/CD, scripts |

---

## Parameter Combination Patterns

### Read-Only Workflows (Reports/Analysis)
```bash
workflow_name \
  [inputs] \
  --out <path> \
  --json
```
- No `--apply` needed
- Safe to run anytime

### Governed Artifact Writers (Specs/Plans/Tasks)
```bash
workflow_name \
  [inputs] \
  --apply
```
- `--apply` required
- Preview before applying

##### Runtime Tree Writes (Code/Config)
```bash
workflow_name \
  [inputs] \
  --apply
```
- `--apply` required for governed artifacts
- Some workflows may require additional flags (check workflow docs)
- Always validate firstirst

### Network Operations (Fetch/Push/Publish)
```bash
workflow_name \
  [inputs] \
  --allow-network \
  --apply
```
- `--allow-network` required
- Use only when necessary

### CI/CD Integration
```bash
workflow_name \
  [inputs] \
  --strict \
  --json
```
- `--strict`: Fail on warnings
- `--json`: Machine-readable

---

## Troubleshooting Common Issues

### Issue: "Missing required flag --apply"
**Cause:** Trying to modify governed artifacts without `--apply`  
**Solution:** Add `--apply` flag

### Issue: "Permission denied writing to runtime tree"
**Cause:** Missing required flag or permission  
**Solution:** Check workflow documentation for required flags

### Issue: "Network access denied"
**Cause:** Workflow needs network but `--allow-network` not provided  
**Solution:** Add `--allow-network` flag

### Issue: "Workflow not found"
**Cause:** Using `.md` extension without `--platform kilo`  
**Solution:** Add `--platform kilo` for Kilo Code

### Issue: "Invalid output path"
**Cause:** Output path outside allowed write scopes  
**Solution:** Use path under `.spec/reports/` or `.spec/prompts/`

---

## Best Practices Summary

### General Principles
1. **Evidence-first:** Never claim progress without verification
2. **Preview-first:** Always validate before applying
3. **Config-first:** Use config defaults, minimize flags
4. **Secure-by-default:** No secrets in CLI, use env vars

### Workflow Execution
1. **Read-only first:** Run analysis/validation workflows first
2. **Two-gate writes:** Use `--apply` + specific write flags
3. **Network minimal:** Use `--allow-network` only when needed
4. **Strict in CI:** Use `--strict` for quality gates

### Documentation
1. **Single source:** Generate docs from specs
2. **Version everything:** Tag releases and docs
3. **Keep in sync:** Update docs with code changes

### Security
1. **Audit regularly:** Run security workflows weekly/monthly
2. **Threat model early:** Before implementing sensitive features
3. **Fix high-severity:** Address critical issues immediately

---

**Guide Version:** 6.2.0  
**Last Updated:** December 21, 2025  
**Maintained by:** SmartSpec Team
