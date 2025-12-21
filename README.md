[🇬🇧 English](README.md) | [🇹🇭 ภาษาไทย](README_th.md)

---

# SmartSpec: The AI-Native Development Framework

![SmartSpec 100% Workflow Loop Completeness](smartspec_100_completeness_infographic.png)

**SmartSpec is a structured, production-grade framework that brings quality, consistency, and speed to your AI-powered development workflow.** It transforms your initial ideas into high-quality, production-ready code by orchestrating a clear, repeatable process: **SPEC → PLAN → TASKS → PROMPT → IMPLEMENT**.

---

## 🔄 100% Workflow Loop Completeness

SmartSpec now provides **end-to-end coverage** of the entire software development lifecycle with 8 critical workflow loops:

1.  **Happy Path Loop:** From ideation to production monitoring.
2.  **Debugging Loop:** For identifying and fixing issues during testing.
3.  **Incident Response Loop:** For managing and resolving production incidents.
4.  **Continuous Improvement Loop:** To feed production data back into development.
5.  **Rollback Loop:** For safe and automated deployment rollbacks.
6.  **Dependency Management Loop:** For proactive dependency scanning and updates.
7.  **Code Quality Loop:** For automated code smell detection and refactoring.
8.  **Performance Optimization Loop:** For profiling and resolving performance bottlenecks.

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

## 🗂️ Core Workflows & Commands

SmartSpec V6 consolidates its powerful features into a streamlined set of workflows, organized by function. These commands form the backbone of the **SPEC → PLAN → TASKS → IMPLEMENT** lifecycle.

### Core Development

| Command | Description |
| :--- | :--- |
| [`/smartspec_generate_spec`](.smartspec-docs/guides/GENERATE_SPEC_GUIDE.md) | Create or refine a `spec.md` using **SPEC-first** governance. |
| [`/smartspec_generate_spec_from_prompt`](.smartspec-docs/guides/GENERATE_SPEC_FROM_PROMPT_GUIDE.md) | Generate **one or more starter specs** from a natural-language requirement prompt **with reuse-first intelligence**. |
| [`/smartspec_generate_plan`](.smartspec-docs/guides/GENERATE_PLAN_GUIDE.md) | Generate or refine `plan.md` from `spec.md` in a **dependency-aware**, **reuse-first**, **safe-by-default** way. |
| [`/smartspec_generate_tasks`](.smartspec-docs/guides/GENERATE_TASKS_GUIDE.md) | Generate or refine `tasks.md` from `spec.md` (or `plan.md`) in a **verification-ready** format. |
| [`/smartspec_implement_tasks`](.smartspec-docs/guides/IMPLEMENT_TASKS_GUIDE.md) | Implement code changes strictly from tasks.md with SmartSpec v6 governance. |

### Production & Operations

| Command | Description |
| :--- | :--- |
| [`/smartspec_production_monitor`](.smartspec-docs/guides/PRODUCTION_MONITOR_GUIDE.md) | Monitor production health and alert on SLO breaches. |
| [`/smartspec_incident_response`](.smartspec-docs/guides/INCIDENT_RESPONSE_GUIDE.md) | Manage production incidents from triage to post-mortem. |
| [`/smartspec_rollback`](.smartspec-docs/guides/ROLLBACK_GUIDE.md) | Plan and execute safe, automated deployment rollbacks. |
| [`/smartspec_feedback_aggregator`](.smartspec-docs/guides/FEEDBACK_AGGREGATOR_GUIDE.md) | Aggregate production feedback into the development cycle. |

### Maintenance & Optimization

| Command | Description |
| :--- | :--- |
| [`/smartspec_dependency_updater`](.smartspec-docs/guides/DEPENDENCY_UPDATER_GUIDE.md) | Scan for outdated dependencies and plan safe updates. |
| [`/smartspec_refactor_planner`](.smartspec-docs/guides/REFACTOR_PLANNER_GUIDE.md) | Detect code smells and plan refactoring efforts. |
| [`/smartspec_performance_profiler`](.smartspec-docs/guides/PERFORMANCE_PROFILER_GUIDE.md) | Profile code to find and plan performance optimizations. |

### Quality & Testing

| Command | Description |
| :--- | :--- |
| [`/smartspec_verify_tasks_progress_strict`](.smartspec-docs/workflows/verify_tasks_progress_strict.md) | Verify progress for a given `tasks.md` using **evidence-only checks**. |
| [`/smartspec_sync_tasks_checkboxes`](.smartspec-docs/workflows/tasks_checkboxes.md) | Synchronize `tasks.md` checkbox markers (`[x]` / `[ ]`) to match the **latest strict verification report**. |
| [`/smartspec_generate_tests`](.smartspec-docs/workflows/generate_tests.md) | Generate test artifacts/suggestions (prompts/scripts/reports). |
| [`/smartspec_quality_gate`](.smartspec-docs/workflows/ci_quality_gate.md) | A consolidated quality gate workflow. |
| [`/smartspec_test_report_analyzer`](.smartspec-docs/workflows/test_report_analyzer.md) | Analyze test results and produce a higher-level diagnostic report. |
| [`/smartspec_test_suite_runner`](.smartspec-docs/workflows/test_suite_runner.md) | Execute a project's test suite and generate a standardized report. |

### Project Management & Support

| Command | Description |
| :--- | :--- |
| [`/smartspec_project_copilot`](.smartspec-docs/workflows/project_copilot_manual.md) | The **read-only front door** into a SmartSpec-enabled repo. |
| [`/smartspec_code_assistant`](.smartspec-docs/workflows/code_assistant.md) | A single, consolidated helper workflow for various assistance tasks. |
| [`/smartspec_report_implement_prompter`](.smartspec-docs/workflows/report_implement_prompter.md) | Generate **implementation prompt packs** from verification reports. |

---

## 🚀 Quick Start

### 1. Installation & Updates

**To install for the first time or update to the latest version:**

Use the following command for your operating system. The script will automatically handle both new installations and updates.

**Unix / macOS / Linux:**
```bash
curl -fsSL https://raw.githubusercontent.com/naibarn/SmartSpec/main/.smartspec/scripts/install.sh | bash
```

**Windows (PowerShell):**
```powershell
irm https://raw.githubusercontent.com/naibarn/SmartSpec/main/.smartspec/scripts/install.ps1 | iex
```

### 2. The Core Workflow

This is the core loop of SmartSpec. It's simple, powerful, and keeps your project on track.

![The SmartSpec Workflow](.smartspec-assets/images/SmartSpec-Pict.png)

---

## 🤔 Why SmartSpec? A New Paradigm for AI-Driven Development

"Vibe Coding" with AI is fast but often leads to inconsistent, low-quality results. SmartSpec provides the structure and guardrails needed for professional development without sacrificing speed.

![AI-Driven Specification & Development Methodologies](.smartspec-assets/images/Spec-DrivenDevelopment.png)

---

## 🏛️ For the LLM

**Repository Goal:** This repository contains the SmartSpec framework, an AI-native development methodology. Your primary goal is to understand its workflows and commands to assist users.

**Key Files:**
- `README.md`: High-level overview.
- `.smartspec-docs/guides/`: Detailed user guides for each workflow. This is your **primary source of truth** for command usage.
- `.smartspec/workflows/`: The master workflow definitions. **Always edit workflows here, not in platform-specific folders.**

When a user asks how to use a command, first consult the corresponding file in `.smartspec-docs/guides/` to provide a detailed, accurate answer.

---

## 🎓 Learning & Support

- **[Troubleshooting Guide](.smartspec-docs/guides/troubleshooting.md)** - Solve common errors and issues.
- **[SmartSpec Copilot](https://chatgpt.com/g/g-6936ffad015c81918e006a9ee2077074-smartspec-copilot)** - Your interactive guide to the SmartSpec ecosystem.

---

## 📝 Release Notes

Detailed changes for each version are tracked in:

- **[v6.0.6 Release Notes](.smartspec-docs/release-notes/RELEASE_NOTES_v6.0.6.md)** (New)
- **[v6.0 Release Notes](.smartspec-docs/release-notes/RELEASE_NOTES_v6.0.md)**
- **[v5.7 Release Notes](.smartspec-docs/release-notes/smart_spec_release_notes_v_5_7.md)**
- **[v5.6 Release Notes](.smartspec-docs/release-notes/smartspec_v_56_release_notes_en.md)**
- **[v5.2 Release Notes](.smartspec-docs/release-notes/RELEASE_NOTES_v5.2.md)**


---

## 📊 Infographic Generation Prompt

The infographic in this README was generated using AI. You can find the exact prompt used for generation in the following file:

- **[Infographic Prompt](INFOGRAPHIC_PROMPT.md)**
