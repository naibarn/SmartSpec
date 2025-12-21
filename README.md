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

## 🚀 New Feature: SmartSpec Copilot — Your Dedicated SmartSpec Help Assistant

**SmartSpec version >6.0** introduces **SmartSpec Copilot**, an always-available interactive assistant built using OpenAI CustomGPT. It allows users to interact with SmartSpec in natural language to understand workflows, debug issues, and navigate the full SmartSpec lifecycle with far less friction.

Copilot responds in English or any language you prefer, including Thai.
It is now the official support channel for learning and using SmartSpec.  [**[Links]**](https://chatgpt.com/g/g-6936ffad015c81918e006a9ee2077074-smartspec-copilot)

---

## 🗂️ All 40 Workflows & Commands

SmartSpec V6 consolidates its powerful features into a streamlined set of 40 workflows, organized by function. These commands form the backbone of the **SPEC → PLAN → TASKS → IMPLEMENT** lifecycle.

### Core Development (5 Workflows)

| Command | Description |
| :--- | :--- |
| [`/smartspec_generate_spec`](.smartspec-docs/workflows/generate_spec_guide.md) | Create or refine a `spec.md` using **SPEC-first** governance. |
| [`/smartspec_generate_spec_from_prompt`](.smartspec-docs/workflows/generate_spec_from_prompt_guide.md) | Generate **one or more starter specs** from a natural-language requirement prompt **with reuse-first intelligence**. |
| [`/smartspec_generate_plan`](.smartspec-docs/workflows/generate_plan_guide.md) | Generate or refine `plan.md` from `spec.md` in a **dependency-aware**, **reuse-first**, **safe-by-default** way. |
| [`/smartspec_generate_tasks`](.smartspec-docs/workflows/generate_tasks_guide.md) | Generate or refine `tasks.md` from `spec.md` (or `plan.md`) in a **verification-ready** format. |
| [`/smartspec_implement_tasks`](.smartspec-docs/workflows/implement_tasks_guide.md) | Implement code changes strictly from tasks.md with SmartSpec v6 governance. |

### Production & Operations (8 Workflows)

| Command | Description |
| :--- | :--- |
| [`/smartspec_deployment_planner`](.smartspec-docs/workflows/deployment_planner_guide.md) | Plan deployment strategy and generate release artifacts. |
| [`/smartspec_release_tagger`](.smartspec-docs/workflows/release_tagger_guide.md) | Create and push version tags for releases. |
| [`/smartspec_production_monitor`](.smartspec-docs/workflows/production_monitor_guide.md) | Monitor production health and alert on SLO breaches. |
| [`/smartspec_observability_configurator`](.smartspec-docs/workflows/observability_configurator_guide.md) | Configure monitoring, logging, and tracing. |
| [`/smartspec_incident_response`](.smartspec-docs/workflows/incident_response_guide.md) | Manage production incidents from triage to post-mortem. |
| [`/smartspec_hotfix_assistant`](.smartspec-docs/workflows/hotfix_assistant_guide.md) | Guide the creation and deployment of emergency hotfixes. |
| [`/smartspec_rollback`](.smartspec-docs/workflows/rollback_guide.md) | Plan and execute safe, automated deployment rollbacks. |
| [`/smartspec_feedback_aggregator`](.smartspec-docs/workflows/feedback_aggregator_guide.md) | Aggregate production feedback into the development cycle. |

### Maintenance & Optimization (8 Workflows)

| Command | Description |
| :--- | :--- |
| [`/smartspec_dependency_updater`](.smartspec-docs/workflows/dependency_updater_guide.md) | Scan for outdated dependencies and plan safe updates. |
| [`/smartspec_refactor_planner`](.smartspec-docs/workflows/refactor_planner_guide.md) | Detect code smells and plan refactoring efforts. |
| [`/smartspec_performance_profiler`](.smartspec-docs/workflows/performance_profiler_guide.md) | Profile code to find and plan performance optimizations. |
| [`/smartspec_data_migration_generator`](.smartspec-docs/workflows/data_migration_generator_guide.md) | Generate database migration scripts from data model changes. |
| [`/smartspec_design_system_migration_assistant`](.smartspec-docs/workflows/design_system_migration_assistant_guide.md) | Assist in migrating to a new design system or component library. |
| [`/smartspec_reindex_specs`](.smartspec-docs/workflows/reindex_specs_guide.md) | Rebuild the spec index for improved search and reuse. |
| [`/smartspec_reindex_workflows`](.smartspec-docs/workflows/reindex_workflows_guide.md) | Rebuild the workflow index for the copilot. |
| [`/smartspec_validate_index`](.smartspec-docs/workflows/validate_index_guide.md) | Validate the integrity of spec and workflow indexes. |

### Quality & Testing (12 Workflows)

| Command | Description |
| :--- | :--- |
| [`/smartspec_generate_tests`](.smartspec-docs/workflows/generate_tests_guide.md) | Generate test artifacts/suggestions (prompts/scripts/reports). |
| [`/smartspec_test_suite_runner`](.smartspec-docs/workflows/test_suite_runner_guide.md) | Execute a project's test suite and generate a standardized report. |
| [`/smartspec_test_report_analyzer`](.smartspec-docs/workflows/test_report_analyzer_guide.md) | Analyze test results and produce a higher-level diagnostic report. |
| [`/smartspec_quality_gate`](.smartspec-docs/workflows/ci_quality_gate_guide.md) | A consolidated quality gate workflow for CI pipelines. |
| [`/smartspec_verify_tasks_progress_strict`](.smartspec-docs/workflows/verify_tasks_progress_strict_guide.md) | Verify progress for a given `tasks.md` using **evidence-only checks**. |
| [`/smartspec_sync_tasks_checkboxes`](.smartspec-docs/workflows/tasks_checkboxes_guide.md) | Synchronize `tasks.md` checkbox markers (`[x]` / `[ ]`) to match the **latest strict verification report**. |
| [`/smartspec_api_contract_validator`](.smartspec-docs/workflows/api_contract_validator_guide.md) | Validate API implementation against its OpenAPI/Swagger contract. |
| [`/smartspec_data_model_validator`](.smartspec-docs/workflows/data_model_validator_guide.md) | Validate database schema against the defined data models. |
| [`/smartspec_ui_component_audit`](.smartspec-docs/workflows/ui_component_audit_guide.md) | Audit UI components for consistency and adherence to design system. |
| [`/smartspec_ui_validation`](.smartspec-docs/workflows/ui_validation_guide.md) | Validate UI implementation against design mockups or specs. |
| [`/smartspec_nfr_perf_planner`](.smartspec-docs/workflows/nfr_perf_planner_guide.md) | Plan performance tests based on Non-Functional Requirements. |
| [`/smartspec_nfr_perf_verifier`](.smartspec-docs/workflows/nfr_perf_verifier_guide.md) | Verify system performance against NFRs. |

### Security (2 Workflows)

| Command | Description |
| :--- | :--- |
| [`/smartspec_security_audit_reporter`](.smartspec-docs/workflows/security_audit_reporter_guide.md) | Run security audits and generate reports. |
| [`/smartspec_security_threat_modeler`](.smartspec-docs/workflows/security_threat_modeler_guide.md) | Analyze specs to identify and model potential security threats. |

### Project Management & Support (5 Workflows)

| Command | Description |
| :--- | :--- |
| [`/smartspec_project_copilot`](.smartspec-docs/workflows/project_copilot_guide.md) | The **read-only front door** into a SmartSpec-enabled repo. |
| [`/smartspec_code_assistant`](.smartspec-docs/workflows/code_assistant_guide.md) | A single, consolidated helper workflow for various assistance tasks. |
| [`/smartspec_report_implement_prompter`](.smartspec-docs/workflows/report_implement_prompter_guide.md) | Generate **implementation prompt packs** from verification reports. |
| [`/smartspec_docs_generator`](.smartspec-docs/workflows/docs_generator_guide.md) | Generate project documentation from specs and code comments. |
| [`/smartspec_docs_publisher`](.smartspec-docs/workflows/docs_publisher_guide.md) | Publish generated documentation to a static site or wiki. |

---

## 📊 Infographic Generation Prompt

The infographic in this README was generated using AI. For a detailed breakdown of all 8 workflow loops and the prompt used to generate the infographic, see the following documents:

- **[Workflow Loops Explained](.smartspec-docs/reports/WORKFLOW_LOOPS_EXPLAINED.md)** - A comprehensive guide to each loop.
- **[Infographic Generation Prompt](.smartspec-docs/reports/INFOGRAPHIC_GENERATION_PROMPT.md)** - The exact prompt used for AI generation.
