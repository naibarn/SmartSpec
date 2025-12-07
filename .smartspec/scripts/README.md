# SmartSpec: The AI-Native Development Framework

![SmartSpec Production-Grade Orchestration System](.smartspec-assets/images/SmartSpec-Pict4.png)

**SmartSpec is a structured, production-grade framework that brings quality, consistency, and speed to your AI-powered development workflow.** It transforms your initial ideas into high-quality, production-ready code by orchestrating a clear, repeatable process: **SPEC → PLAN → TASKS → PROMPT → IMPLEMENT**.

---

## ✨ Supported Platforms

SmartSpec V5 supports your favorite AI coding platforms with a single-command installation:

- **Kilo Code** - For autonomous AI agent-driven development.
- **Claude Code** - For deep analysis with sub-agents.
- **Google Antigravity** - For agentic IDE with autonomous agents.
- **Gemini CLI** - For terminal-based AI coding assistant.
- **Cursor / VSCode** - For supercharging your manual "vibe coding" workflow.
- **Roo Code** - For safety-first, workflow-driven development.

---

## 🚀 Quick Start

### 1. Installation & Updates

**To install for the first time:**

Use the following command for your operating system.

**To update to the latest version:**

Simply run the same installation command again. The script will automatically detect your existing installation and update it to the latest version, preserving your custom workflows.

**Note:** The installation script copies workflows from `.smartspec/workflows/` (master source) to platform-specific folders in your AI tools (typically under your home directory, e.g. `~/.kilocode/workflows`, `~/.roo/commands`, `~/.claude/commands`, `~/.agent/workflows`, `~/.gemini/commands`). For Gemini CLI, workflows are automatically converted from Markdown to TOML format. Always edit workflows in `.smartspec/workflows/` and run `.smartspec/sync.sh` to sync changes to all platforms.

**Unix / macOS / Linux:**
```bash
curl -fsSL https://raw.githubusercontent.com/naibarn/SmartSpec/main/.smartspec/scripts/install.sh | bash
```

**Windows (PowerShell):**
```powershell
irm https://raw.githubusercontent.com/naibarn/SmartSpec/main/.smartspec/scripts/install.ps1 | iex
```

### 2. The 3-Step Workflow

This is the core loop of SmartSpec. It's simple, powerful, and keeps your project on track.

![The SmartSpec Workflow](.smartspec-assets/images/SmartSpec-Pict.png)

---

## 🤔 Why SmartSpec? A New Paradigm for AI-Driven Development

"Vibe Coding" with AI is fast but often leads to inconsistent, low-quality results. SmartSpec provides the structure and guardrails needed for professional development without sacrificing speed.

![AI-Driven Specification & Development Methodologies](.smartspec-assets/images/Spec-DrivenDevelopment.png)

## Vibe coding tools comparison 
[**[Vibe coding comparison]**](.smartspec-docs/guides/vibe_coding_comparison.md)
---

## 🎯 What SmartSpec Does for Your Vibe-Coding Workflow

SmartSpec acts as a **structured engine** that transforms vibe-coding from chaotic to reliable, consistent, and production-grade. Here's how it improves your AI-powered development process:

### 1. 💡 Idea → SPEC Conversion

You provide a high-level idea or "vibe" for your project. SmartSpec generates a **complete specification** including:

- **Purpose & Goals** - What the system should achieve
- **Requirements** - Functional and non-functional requirements
- **Architecture Outline** - High-level system design
- **Constraints** - Technical limitations and boundaries
- **Domain Rules** - Business logic and validation rules

**Result:** Your vague idea becomes an engineering-ready specification.

### 2. 📋 SPEC → Plan / Tasks

SmartSpec breaks down the specification into actionable items:

- **Development Plan** - Phased implementation strategy
- **Granular Tasks** - Step-by-step work items with time estimates
- **Module Structure** - Clear file and component organization
- **Security & Performance Requirements** - Production-grade considerations

**Result:** No more "AI just writes random code" problem. You get a clear roadmap.

### 3. 🚀 Task → Implementation Prompts

SmartSpec auto-generates **high-quality prompts** that can be executed by AI coding agents:

- **"Implement Feature" Prompts** - Complete with context, requirements, and coding rules
- **"Create Component" Prompts** - With architecture guidance and best practices
- **"Refactor / Fix / Test" Prompts** - For maintenance and quality improvement

**Result:** Consistent, maintainable code across your entire project.

### 4. ✅ Auto-Validation & Governance

SmartSpec continuously checks your project for:

- **Missing Requirements** - Ensures nothing is overlooked
- **Security Gaps** - Identifies potential vulnerabilities
- **Domain Rules Compliance** - Validates business logic consistency
- **Structural Correctness** - Maintains clean architecture

**Result:** Your vibe-coding stays aligned with production standards.

### 5. 🔄 Supports Both Auto and Manual Workflows

**Auto-Mode (Full Agent):**
- AI implements tasks automatically
- Suitable for: Kilo Code, Claude Code, Roo Code
- Best for: Autonomous development with minimal human intervention

**Manual Mode (Copy-Paste):**
- SmartSpec prepares clean coding prompts
- Suitable for: Cursor, VSCode, Google Antigravity
- Best for: Interactive development with human oversight

**Result:** Both beginners and experienced developers can use SmartSpec effectively.

### 6. 🏢 Domain & Profile Support

SmartSpec includes specialized profiles for different domains:

- **CRUD Services** - Standard data management patterns
- **Backend Service Architecture** - Microservices, APIs, databases
- **Fintech / Healthcare / Enterprise** - Domain-specific rules and compliance
- **Performance + DI + Security Modes** - Production-grade patterns

**Result:** Generated specs and tasks are not generic—they adapt to your domain.

---

## 📖 Core Commands

Each command corresponds to a workflow that you can customize. Click on a command to see its detailed documentation.

| Command | Description | Full Docs |
| :--- | :--- | :--- |
| `/smartspec_generate_spec.md` | Create a structured SPEC from an idea. | [**[Details]**](.smartspec-docs/workflows/generate_spec.md) |
| `/smartspec_generate_plan.md` | Generate a high-level implementation plan. | [**[Details]**](.smartspec-docs/workflows/generate_plan.md) |
| `/smartspec_generate_tasks.md` | Break the plan into granular tasks. | [**[Details]**](.smartspec-docs/workflows/generate_tasks.md) |
| `/smartspec_generate_implement_prompt.md` | Create context-rich prompts for AI assistants. | [**[Details]**](.smartspec-docs/workflows/generate_implement_prompt.md) |
| `/smartspec_generate_cursor_prompt.md` | Generate user-friendly prompts for Cursor/Antigravity. | [**[Details]**](.smartspec-docs/workflows/generate_cursor_prompt.md) |
| `/smartspec_implement_tasks.md` | Execute tasks with an autonomous agent. | [**[Details]**](.smartspec-docs/workflows/implement_tasks.md) |
| `/smartspec_reverse_to_spec.md` | Reverse-engineer code into a SPEC. | [**[Details]**](.smartspec-docs/workflows/reverse_to_spec.md) |
| `/smartspec_sync_spec_tasks.md` | Sync changes between SPEC and tasks. | [**[Details]**](.smartspec-docs/workflows/sync_spec_tasks.md) |
| `/smartspec_verify_tasks_progress.md` | Verify task completion and code quality. | [**[Details]**](.smartspec-docs/workflows/verify_tasks_progress.md) |

---

## 🔧 Quality Improvement Commands

These workflows help maintain and improve code quality on a spec-scoped basis:

| Command | Description | Full Docs |
| :--- | :--- | :--- |
| `/smartspec_fix_errors.md` | Auto-fix compilation, type, and runtime errors. | [**[Details]**](.smartspec-docs/workflows/fix_errors.md) |
| `/smartspec_generate_tests.md` | Generate unit, integration, and e2e tests. | [**[Details]**](.smartspec-docs/workflows/generate_tests.md) |
| `/smartspec_refactor_code.md` | Refactor code to improve quality and reduce complexity. | [**[Details]**](.smartspec-docs/workflows/refactor_code.md) |
| `/smartspec_reindex_specs.md` | Re-index SPEC_INDEX.json to keep it accurate. | [**[Details]**](.smartspec-docs/workflows/reindex_specs.md) |
| `/smartspec_validate_index.md` | Validate SPEC_INDEX.json integrity and health. | [**[Details]**](.smartspec-docs/workflows/validate_index.md) |

**Note:** All quality workflows operate on a **spec-scoped basis** for optimal performance in large projects. See [SPEC_SCOPED_WORKFLOWS.md](.smartspec-docs/guides/SPEC_SCOPED_WORKFLOWS.md) for details.

**Troubleshooting:** 
- If workflows don't mark task checkboxes automatically, see [MANUAL_UPDATE_CHECKBOXES.md](.smartspec-docs/guides/MANUAL_UPDATE_CHECKBOXES.md) for manual update methods.
- To resume implementation from a specific task to the end, see [START_FROM_GUIDE.md](.smartspec-docs/guides/START_FROM_GUIDE.md) for `--start-from` parameter usage.

**Kilo Code Modes:**
- **[Kilo Code Complete Guide](.smartspec-docs/guides/KILO_CODE_COMPLETE_GUIDE.md)** - Complete guide for all 5 Kilo Code modes (Ask, Architect, Code, Debug, Orchestrator) and `--kilocode` flag usage.
- **[Ask Mode Guide](.smartspec-docs/guides/ASK_MODE_GUIDE.md)** - Analyze and understand before making decisions.
- **[Architect Mode Guide](.smartspec-docs/guides/ARCHITECT_MODE_GUIDE.md)** - Design system architecture and create implementation plans.
- **[Debug Mode Guide](.smartspec-docs/guides/DEBUG_MODE_GUIDE.md)** - Systematically diagnose and fix bugs and errors.
- **[Kilo Code Sub-Task Mode Guide](.smartspec-docs/guides/KILOCODE_MODE_GUIDE.md)** - Use Orchestrator Mode to break complex tasks into sub-tasks.


---

### Choosing the Right Prompt Generation Workflow

SmartSpec offers two distinct commands for generating prompts, each tailored for a different execution model. Understanding the difference is key to a smooth workflow.

| Feature | `/generate_implement_prompt` | `/generate_cursor_prompt` |
| :--- | :--- | :--- |
| **Target Platform** | **Kilo Code, Roo Code, Claude Code** | **Cursor, Google Antigravity** |
| **Execution Model** | 🤖 **Automated Execution** | 🧑‍💻 **Manual Copy/Paste** |
| **User Action** | Run `kilocode execute "<file>"` or `roo run "<file>"` | Copy each prompt section and paste it into the AI assistant. |
| **Output Format** | **One continuous document** with all context. | **One file with multiple, distinct prompt sections.** |
| **Prompt Philosophy** | Written for an **AI Agent** to execute autonomously. | Written for a **Human Developer** to guide an AI assistant. |
| **Best Use Case** | Implementing a sequence of related tasks in a single, powerful session. | Implementing tasks one-by-one in an interactive, "vibe coding" session. |
| **Analogy** | Giving a detailed project brief to a senior developer. | Writing a clear to-do list for a junior developer. |

**In short:** Use `generate_implement_prompt` for automated platforms and `generate_cursor_prompt` for interactive, manual coding.

---

## 🏛️ Architecture Overview

SmartSpec acts as an orchestration layer, separating the specification and planning phase from the code implementation phase. This ensures all development work is grounded in a clear, agreed-upon blueprint.

![SmartSpec Architecture](.smartspec-assets/images/SmartSpec-Pict2.png)

---

## 🧩 Advanced Features

SmartSpec is more than just a workflow; it's a complete orchestration system with features designed for enterprise-grade projects.

![SmartSpec Advanced Features](.smartspec-assets/images/SmartSpec-Pict3.png)

---

## 🏛️ For the LLM

**Repository Goal:** This repository contains the SmartSpec framework, an AI-native development methodology. Your primary goal is to understand its workflows and commands to assist users.

**Key Files:**
- `README.md`: High-level overview.
- `.smartspec-docs/workflows/`: Detailed documentation for each command. This is your **primary source of truth** for command usage, parameters, and examples.
- `.smartspec/workflows/`: The master workflow definitions. **Always edit workflows here, not in platform-specific folders.**

When a user asks how to use a command, first consult the corresponding file in `.smartspec-docs/workflows/` to provide a detailed, accurate answer.

---

## 🎓 Learning & Support

- **[Troubleshooting Guide](.smartspec-docs/guides/troubleshooting.md)** - Solve common errors and issues.

---

## Troubleshooting

For common issues and solutions, see the **[Troubleshooting Guide](.smartspec-docs/guides/troubleshooting.md)**.
