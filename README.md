# SmartSpec: The AI-Native Development Framework

![SmartSpec Production-Grade Orchestration System](.smartspec-assets/images/SmartSpec-Pict4.png)

**SmartSpec is a structured, production-grade framework that brings quality, consistency, and speed to your AI-powered development workflow.** It transforms your initial ideas into high-quality, production-ready code by orchestrating a clear, repeatable process: **SPEC → PLAN → TASKS → PROMPT → IMPLEMENT**.

---

## ✨ Supported Platforms

SmartSpec V5 supports your favorite AI coding platforms with a single-command installation:

- **Kilo Code** - For autonomous AI agent-driven development.
- **Claude Code** - For deep analysis with sub-agents.
- **Cursor / VSCode / Google Antigravity** - For supercharging your manual "vibe coding" workflow.
- **Roo Code** - For safety-first, workflow-driven development.

---

## 🚀 Quick Start

### 1. Installation

Get up and running in 30 seconds.

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
- `.kilocode/workflows/`: The underlying workflow definitions.

When a user asks how to use a command, first consult the corresponding file in `.smartspec-docs/workflows/` to provide a detailed, accurate answer.

---

## Troubleshooting

**Command not found:**
- Ensure the installation script ran correctly and that `~/.smartspec/bin` is in your shell's `PATH`.
- Restart your terminal or source your shell profile file (e.g., `source ~/.zshrc`).
