# UPDATED KNOWLEDGE BASE – `knowledge_base_smart_spec.md`
## Governance Additive Extension (Includes `/smartspec_report_implement_prompter`)

> **NOTE:** This update is *additive* and maintains full backward compatibility. No original rules are altered or removed. New workflow, governance rules, and chain integration are appended according to KB policy.

---
# 1. SmartSpec Governance Overview (Unchanged)
*(Original content preserved; omitted here for brevity. Sections below extend the KB.)*

---
# 2. NEW WORKFLOW CLASSIFICATION
## `/smartspec_report_implement_prompter`
**Category:** Evidence-Driven Implementation Support Workflow (Post-Strict-Verification Layer)

### Purpose
This workflow converts strict verification reports into actionable implementation prompts, designed for IDE-based AI copilots. It supports domain clustering, multi-repo environments, evidence configuration, and stack detection.

### Position in SmartSpec Lifecycle
This workflow executes **after strict verification** and before sync:
```
SPEC → PLAN → TASKS → IMPLEMENT → VERIFY (strict)
        ↓
   OPTIONAL: /smartspec_report_implement_prompter
        ↓
SYNC → DELIVERY
```

### Key Capabilities
- Reads strict JSON report (version-aware)
- Performs domain clustering (API / Tests / Docs / Deploy)
- Identifies simple vs complex implementation gaps
- Generates prompts per cluster
- Supports multi-repo flags & evidence-config
- Supports localization (EN/TH)
- Supports stack detection (Fastify, NestJS, Spring Boot, FastAPI, Go, etc.)

---
# 3. GOVERNANCE RULES FOR `/smartspec_report_implement_prompter`

## 3.1 Write Guard Classification
```
write_guard: NO-WRITE (core artifacts)
```
### Forbidden Writes
The workflow **must not modify**:
- `spec.md`
- `tasks.md`
- registry directories under `.smartspec/registries`
- UI schemas
- Source code (src/)
- Test suites (tests/)
- Documentation (docs/)
- Deployment manifests / infra files

### Allowed Writes
This workflow may write **only auxiliary prompt files**:
```
.smartspec/prompts/<spec-id>/
```
This directory is explicitly **outside governed artifacts**.

---
# 4. MULTI-REPO GOVERNANCE SUPPORT
This workflow must accept and honor the same path-resolution context as strict verifier:
```
--workspace-roots <paths>
--repos-config <path>
```
Failure to provide these flags in multi-repo mode must emit a warning.

The workflow must resolve:
- spec path
- tasks path
- strict report path
…using the workspace graph defined by SmartSpec.

---
# 5. STRICT REPORT VERSIONING GOVERNANCE
Strict report may evolve. Workflow must:
- Read `report.version` if present.
- If missing → treat as Version 1.
- If version > supported → issue warning.
- Parse evidence fields in a schema-tolerant manner.

---
# 6. EVIDENCE CONFIG GOVERNANCE
Workflow must detect evidence configuration:
```
--evidence-config <file>
```
or
```
.smartspec/evidence-config/<spec-id>.json
```
Rules:
- Evidence rules override default clustering.
- Evidence rules may define custom test/doc/deploy directories.

---
# 7. CLUSTER OVERRIDE SYSTEM
Projects may override cluster assignments.
```
.smartspec/prompts/cluster-overrides.json
```
Overrides take highest precedence.
Invalid cluster names must issue warnings.

---
# 8. TASK CLASSIFICATION GOVERNANCE
Tasks must be classified into:

### 8.1 `unsynced_only`
- Evidence complete but checkbox unsynced.
- Must recommend `/smartspec_sync_tasks_checkboxes`.

### 8.2 `simple_not_started`
- Phase NOT_STARTED
- Not critical
- Not containing complexity indicators
- Recommend `/smartspec_implement_tasks`

### 8.3 `complex_cluster`
Includes tasks that:
- Appear in strict report `critical_missing_components`, or
- Lack core evidence (API, tests, docs, deploy), or
- Contain complexity keywords, or
- Belong to complex domain phases (Security, Payment, Integration, Deployment)

=> Must generate a dedicated prompt.

---
# 9. PROMPT GENERATION GOVERNANCE
Prompt output must:
- Use official SmartSpec prompt templates
- Include metadata:
```
Prompt-Generation-ID
Spec-ID
Report-Version
Generated-At
```
- Support markdown or JSON output
- Support automatic splitting when exceeding limits

Limits:
```
max_tasks_per_prompt = 15
max_chars_per_prompt = 35000
```

---
# 10. LOCALE GOVERNANCE
Locale resolution must follow priority:
1. `--language`
2. `Language:` header in spec
3. Body-language ratio (Thai > 20% → TH)
4. Platform default (Kilo Code → TH)
5. Default fallback → EN

---
# 11. TECH STACK DETECTION GOVERNANCE
Workflow should detect stack using project files:
- Fastify via `package.json`
- NestJS via import patterns
- Spring Boot via Java entrypoints
- FastAPI via Python imports
- Go frameworks via `go.mod`

Prompt wording must adapt to framework.

---
# 12. PROJECT COPILOT INTEGRATION
`/smartspec_project_copilot` must recommend this workflow when:
- strict verifier reports critical missing components
- phases are partial
- complex gaps detected

UI recommendation:
```
"Strict verification found complex gaps. Generate IDE prompts using /smartspec_report_implement_prompter?"
```

---
# 13. ERROR HANDLING GOVERNANCE
Workflow must handle safely:
- Missing strict report
- Unsupported report version
- Task ID mismatch (warn, not fail)
- Missing acceptance criteria (warn)
- Empty clusters (skip generation)

---
# 14. EDGE CASES
## 14.1 All Tasks Complete
Create only:
```
README.md (summary: no remaining tasks)
```

## 14.2 Large Reports (>200 tasks or >2MB)
Workflow must:
- Use streaming parser
- Limit prompt generation to complex tasks unless explicitly overridden

---
# END OF KB EXTENSION (knowledge_base_smart_spec.md)

