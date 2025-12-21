# SmartSpec: The AI-Native Development Framework

![SmartSpec 100% Workflow Loop Completeness](.smartspec-assets/infographics/smartspec_100_completeness_infographic.png)

**SmartSpec is a structured, production-grade framework that brings quality, consistency, and speed to your AI-powered development workflow.** It transforms your initial ideas into high-quality, production-ready code by orchestrating a clear, repeatable process: **SPEC → PLAN → TASKS → PROMPT → IMPLEMENT**.

---

## 🔄 100% Workflow Loop Completeness

SmartSpec now provides **end-to-end coverage** of the entire software development lifecycle with 8 critical, interconnected workflow loops. This ensures that every phase, from initial idea to production maintenance, is handled by a dedicated, intelligent, and automated process.

1.  **Happy Path Loop (9 phases):** The core development cycle, taking an idea from `Ideation → Deploy → Monitor`. This loop covers specification, planning, task generation, implementation, and deployment.
2.  **Debugging Loop (5 phases):** Activates when a test fails. This loop guides the developer through a structured process of `Test Failure → Fix → Verify` to ensure issues are resolved systematically.
3.  **Incident Response Loop (6 phases):** Manages production issues from `Alert → Triage → Resolve`. It provides a clear workflow for handling incidents, from initial notification to resolution and post-mortem.
4.  **Continuous Improvement Loop (6 phases):** Feeds production data and user feedback back into the development cycle using a `Metrics → Feedback → Update` flow, ensuring the product evolves based on real-world usage.
5.  **Rollback Loop (5 phases):** Provides a safe and automated process for reverting deployments in case of failure, following a `Failure → Decision → Execute` path to minimize downtime.
6.  **Dependency Management Loop (6 phases):** Proactively keeps the project secure and up-to-date by following a `Scan → Analyze → Update` process for all third-party dependencies.
7.  **Code Quality Loop (6 phases):** Automatically detects code smells, technical debt, and areas for improvement, then plans and executes refactoring with an `Analyze → Refactor → Verify` cycle.
8.  **Performance Optimization Loop (6 phases):** Identifies and resolves performance bottlenecks by following a `Profile → Optimize → Measure` workflow, ensuring the application runs efficiently.

---

## ✨ Supported Platforms

SmartSpec V6 supports your favorite AI coding platforms with a single-command installation:

- **Kilo Code** - For autonomous AI agent-driven development.
- **Claude Code** - For deep analysis with sub-agents.
- **Google Antigravity** - For agentic IDE with autonomous agents.
- **Gemini CLI** - For terminal-based AI coding assistant.
- **Cursor / VSCode** - For supercharging your manual "vibe coding" workflow.
- **Roo Code** - For safety-first, workflow-driven development.

---

## ⚠️ Critical: Preview-First Workflow Pattern

**SmartSpec follows a strict preview-first approach to prevent accidental file modifications.** This is a core safety principle that ensures you always review changes before they are applied.

### How It Works

#### Step 1: Run Without `--apply` (Preview Mode)

When you run a workflow **without** the `--apply` flag, SmartSpec generates a **preview report** showing what changes will be made, but **does not modify any files**.

**CLI:**
```bash
/smartspec_generate_spec --spec specs/feature/spec-001/spec.md
```

**Kilo Code:**
```bash
/smartspec_generate_spec.md --spec specs/feature/spec-001/spec.md --platform kilo
```

**Result:** A report is generated at `.spec/reports/generate-spec/<run-id>/` showing:
- What will be changed
- Why it will be changed
- Preview of the new content

#### Step 2: Review the Report Carefully

**Read the generated report thoroughly:**
- Check if the proposed changes are correct
- Verify that no unintended modifications will occur
- Ensure the changes align with your requirements

**Report location:**
```
.spec/reports/<workflow-name>/<run-id>/
├── report.md          # Human-readable summary
├── report.json        # Machine-readable data
└── preview/           # Preview of changes
```

#### Step 3: Run Again With `--apply` (Apply Mode)

**Only after you are confident the changes are correct**, run the same command again with the `--apply` flag.

**CLI:**
```bash
/smartspec_generate_spec --spec specs/feature/spec-001/spec.md --apply
```

**Kilo Code:**
```bash
/smartspec_generate_spec.md --spec specs/feature/spec-001/spec.md --apply --platform kilo
```

**Result:** SmartSpec now **actually modifies the files** as shown in the preview.

### Why This Matters

✅ **Safety:** Prevents accidental overwrites or incorrect modifications  
✅ **Transparency:** You always know exactly what will change before it happens  
✅ **Control:** You make the final decision to apply changes  
✅ **Auditability:** Every change is documented in reports before being applied  

### Workflows That Require `--apply`

The following workflows modify **governed artifacts** (specs, plans, tasks) and **require `--apply`** to make actual changes:

- `smartspec_generate_spec` - Modifies `spec.md`
- `smartspec_generate_plan` - Modifies `plan.md`
- `smartspec_generate_tasks` - Modifies `tasks.md`
- `smartspec_implement_tasks` - Modifies source code
- `smartspec_sync_tasks_checkboxes` - Modifies `tasks.md` checkboxes

### Workflows That Don't Need `--apply`

Some workflows only generate **reports or prompts** (safe outputs) and don't need `--apply`:

- `smartspec_project_copilot` - Read-only analysis
- `smartspec_verify_tasks_progress_strict` - Generates verification report
- `smartspec_report_implement_prompter` - Generates implementation prompts
- `smartspec_test_report_analyzer` - Analyzes test results

### Remember

🔴 **Never use `--apply` on the first run**  
🟡 **Always review the preview report**  
🟢 **Only use `--apply` when you're confident**

---

## 🚀 New Feature: SmartSpec Copilot — Your Dedicated SmartSpec Help Assistant

**SmartSpec version >6.0** introduces **SmartSpec Copilot**, an always-available interactive assistant built using OpenAI CustomGPT. It allows users to interact with SmartSpec in natural language to understand workflows, debug issues, and navigate the full SmartSpec lifecycle with far less friction.

Copilot responds in English or any language you prefer, including Thai.
It is now the official support channel for learning and using SmartSpec.  [**[Links]**](https://chatgpt.com/g/g-6936ffad015c81918e006a9ee2077074-smartspec-copilot)

---

## 🚀 Quick Start: Your First Workflow

Here's a complete example showing the **preview-first pattern** in action:

### Example: Creating a New Specification

#### 1️⃣ First Run: Preview Mode (No `--apply`)

**CLI:**
```bash
/smartspec_generate_spec --spec specs/feature/spec-001-user-auth/spec.md
```

**Kilo Code:**
```bash
/smartspec_generate_spec.md --spec specs/feature/spec-001-user-auth/spec.md --platform kilo
```

**What happens:**
- ✅ SmartSpec analyzes your requirements
- ✅ Generates a preview report at `.spec/reports/generate-spec/<run-id>/`
- ❌ **Does NOT create or modify** `spec.md` yet

#### 2️⃣ Review the Report

```bash
# Open and read the report
cat .spec/reports/generate-spec/<run-id>/report.md

# Check the preview
cat .spec/reports/generate-spec/<run-id>/preview/spec.md
```

**Questions to ask yourself:**
- ❓ Does the spec cover all requirements?
- ❓ Are the NFRs (security, performance) included?
- ❓ Is the structure correct?
- ❓ Are there any errors or omissions?

#### 3️⃣ Second Run: Apply Mode (With `--apply`)

**Only after you're satisfied with the preview:**

**CLI:**
```bash
/smartspec_generate_spec --spec specs/feature/spec-001-user-auth/spec.md --apply
```

**Kilo Code:**
```bash
/smartspec_generate_spec.md --spec specs/feature/spec-001-user-auth/spec.md --apply --platform kilo
```

**What happens:**
- ✅ SmartSpec **creates** `specs/feature/spec-001-user-auth/spec.md`
- ✅ Updates `.spec/SPEC_INDEX.json`
- ✅ Generates final report

### 🎯 Key Takeaway

**Two-step process:**
1. **Preview** (no `--apply`) → Review report → Decide
2. **Apply** (with `--apply`) → Changes are made

**This pattern applies to most SmartSpec workflows!**

---

## 🗂️ All 40 Workflows & Commands

SmartSpec V6 consolidates its powerful features into a streamlined set of 40 workflows, organized by function. These commands form the backbone of the **SPEC → PLAN → TASKS → IMPLEMENT** lifecycle.

**⚠️ Remember:** Most workflows follow the **preview-first pattern** — run without `--apply` first to review, then run with `--apply` to apply changes.

### Core Development (5 Workflows)

| Command | Description |
| :--- | :--- |
| [`/smartspec_generate_spec`](.smartspec-docs/workflows/generate_spec.md) | Create or refine a `spec.md` using **SPEC-first** governance. |
| [`/smartspec_generate_spec_from_prompt`](.smartspec-docs/workflows/generate_spec_from_prompt.md) | Generate **one or more starter specs** from a natural-language requirement prompt **with reuse-first intelligence**. |
| [`/smartspec_generate_plan`](.smartspec-docs/workflows/generate_plan.md) | Generate or refine `plan.md` from `spec.md` in a **dependency-aware**, **reuse-first**, **safe-by-default** way. |
| [`/smartspec_generate_tasks`](.smartspec-docs/workflows/generate_tasks.md) | Generate or refine `tasks.md` from `spec.md` (or `plan.md`) in a **verification-ready** format. |
| [`/smartspec_implement_tasks`](.smartspec-docs/workflows/implement_tasks.md) | Implement code changes strictly from tasks.md with SmartSpec v6 governance. |

### Production & Operations (8 Workflows)

| Command | Description |
| :--- | :--- |
| [`/smartspec_deployment_planner`](.smartspec-docs/workflows/deployment_planner.md) | Plan deployment strategy and generate release artifacts. |
| [`/smartspec_release_tagger`](.smartspec-docs/workflows/release_tagger.md) | Create and push version tags for releases. |
| [`/smartspec_production_monitor`](.smartspec-docs/guides/PRODUCTION_MONITOR_GUIDE.md) | Monitor production health and alert on SLO breaches. |
| [`/smartspec_observability_configurator`](.smartspec-docs/workflows/observability_configurator.md) | Configure monitoring, logging, and tracing. |
| [`/smartspec_incident_response`](.smartspec-docs/guides/INCIDENT_RESPONSE_GUIDE.md) | Manage production incidents from triage to post-mortem. |
| [`/smartspec_hotfix_assistant`](.smartspec-docs/workflows/hotfix_assistant.md) | Guide the creation and deployment of emergency hotfixes. |
| [`/smartspec_rollback`](.smartspec-docs/guides/ROLLBACK_GUIDE.md) | Plan and execute safe, automated deployment rollbacks. |
| [`/smartspec_feedback_aggregator`](.smartspec-docs/guides/FEEDBACK_AGGREGATOR_GUIDE.md) | Aggregate production feedback into the development cycle. |

### Maintenance & Optimization (8 Workflows)

| Command | Description |
| :--- | :--- |
| [`/smartspec_dependency_updater`](.smartspec-docs/guides/DEPENDENCY_UPDATER_GUIDE.md) | Scan for outdated dependencies and plan safe updates. |
| [`/smartspec_refactor_planner`](.smartspec-docs/guides/REFACTOR_PLANNER_GUIDE.md) | Detect code smells and plan refactoring efforts. |
| [`/smartspec_performance_profiler`](.smartspec-docs/guides/PERFORMANCE_PROFILER_GUIDE.md) | Profile code to find and plan performance optimizations. |
| [`/smartspec_data_migration_generator`](.smartspec-docs/workflows/data_migration_generator.md) | Generate database migration scripts from data model changes. |
| [`/smartspec_design_system_migration_assistant`](.smartspec-docs/workflows/design_system_migration_assistant.md) | Assist in migrating to a new design system or component library. |
| [`/smartspec_reindex_specs`](.smartspec-docs/workflows/reindex_specs.md) | Rebuild the spec index for improved search and reuse. |
| [`/smartspec_reindex_workflows`](.smartspec-docs/workflows/smartspec_reindex_workflows.md) | Rebuild the workflow index for the copilot. |
| [`/smartspec_validate_index`](.smartspec-docs/workflows/validate_index.md) | Validate the integrity of spec and workflow indexes. |

### Quality & Testing (12 Workflows)

| Command | Description |
| :--- | :--- |
| [`/smartspec_generate_tests`](.smartspec-docs/workflows/generate_tests.md) | Generate test artifacts/suggestions (prompts/scripts/reports). |
| [`/smartspec_test_suite_runner`](.smartspec-docs/workflows/test_suite_runner.md) | Execute a project's test suite and generate a standardized report. |
| [`/smartspec_test_report_analyzer`](.smartspec-docs/workflows/test_report_analyzer.md) | Analyze test results and produce a higher-level diagnostic report. |
| [`/smartspec_quality_gate`](.smartspec-docs/workflows/ci_quality_gate.md) | A consolidated quality gate workflow for CI pipelines. |
| [`/smartspec_verify_tasks_progress_strict`](.smartspec-docs/workflows/verify_tasks_progress_strict.md) | Verify progress for a given `tasks.md` using **evidence-only checks**. |
| [`/smartspec_sync_tasks_checkboxes`](.smartspec-docs/workflows/tasks_checkboxes.md) | Synchronize `tasks.md` checkbox markers (`[x]` / `[ ]`) to match the **latest strict verification report**. |
| [`/smartspec_api_contract_validator`](.smartspec-docs/workflows/api_contract_validator.md) | Validate API implementation against its OpenAPI/Swagger contract. |
| [`/smartspec_data_model_validator`](.smartspec-docs/workflows/data_model_validator.md) | Validate database schema against the defined data models. |
| [`/smartspec_ui_component_audit`](.smartspec-docs/workflows/ui_component_audit.md) | Audit UI components for consistency and adherence to design system. |
| [`/smartspec_ui_validation`](.smartspec-docs/workflows/ui_validation_manual.md) | Validate UI implementation against design mockups or specs. |
| [`/smartspec_nfr_perf_planner`](.smartspec-docs/workflows/nfr_perf_planner.md) | Plan performance tests based on Non-Functional Requirements. |
| [`/smartspec_nfr_perf_verifier`](.smartspec-docs/workflows/nfr_perf_verifier.md) | Verify system performance against NFRs. |

### Security (2 Workflows)

| Command | Description |
| :--- | :--- |
| [`/smartspec_security_audit_reporter`](.smartspec-docs/workflows/security_audit_reporter.md) | Run security audits and generate reports. |
| [`/smartspec_security_threat_modeler`](.smartspec-docs/workflows/security_threat_modeler.md) | Analyze specs to identify and model potential security threats. |

### Project Management & Support (5 Workflows)

| Command | Description |
| :--- | :--- |
| [`/smartspec_project_copilot`](.smartspec-docs/workflows/project_copilot_manual.md) | The **read-only front door** into a SmartSpec-enabled repo. |
| [`/smartspec_code_assistant`](.smartspec-docs/workflows/code_assistant.md) | A single, consolidated helper workflow for various assistance tasks. |
| [`/smartspec_report_implement_prompter`](.smartspec-docs/workflows/report_implement_prompter.md) | Generate **implementation prompt packs** from verification reports. |
| [`/smartspec_docs_generator`](.smartspec-docs/workflows/docs_generator.md) | Generate project documentation from specs and code comments. |
| [`/smartspec_docs_publisher`](.smartspec-docs/workflows/docs_publisher.md) | Publish generated documentation to a static site or wiki. |

---

## 📊 Infographic Generation Prompt

The infographic in this README was generated using AI. For a detailed breakdown of all 8 workflow loops and the prompt used to generate the infographic, see the following documents:

- **[Workflow Loops Explained](.smartspec-docs/reports/WORKFLOW_LOOPS_EXPLAINED.md)** - A comprehensive guide to each loop.
- **[Infographic Generation Prompt](.smartspec-docs/reports/INFOGRAPHIC_GENERATION_PROMPT.md)** - The exact prompt used for AI generation.
