# SmartSpec: The AI-Native Development Framework

**The structured workflow that brings quality, consistency, and speed to your AI-powered development.**

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
iwr -useb https://raw.githubusercontent.com/naibarn/SmartSpec/main/.smartspec/scripts/install.ps1 | iex
```

### 2. The 3-Step Workflow

1.  **Generate a SPEC:** Create a comprehensive blueprint for your feature.
    ```bash
    /smartspec_generate_spec.md specs/my-feature/spec.md
    ```

2.  **Generate Tasks:** Get a detailed checklist of implementation tasks.
    ```bash
    /smartspec_generate_tasks.md specs/my-feature/spec.md
    ```

3.  **Generate a Prompt & Vibe:** Get a context-rich prompt for your AI tool.
    ```bash
    /smartspec_generate_implement_prompt.md specs/my-feature/tasks.md --task T001
    ```

---

## 🤔 Why SmartSpec? From Vibe Coding Chaos to Structured Velocity

AI coding is fast, but it's often chaotic. SmartSpec provides the architectural backbone that AI agents lack.

| | **Traditional "Vibe Coding"** | **SmartSpec-Powered Development** |
| :--- | :--- | :--- |
| **Process** | Ad-hoc, prompt-by-prompt | **SPEC → TASKS → CODE** (Systematic) |
| **Quality** | Inconsistent | **Consistently High** (Enforced by SPEC) |
| **Architecture** | Ignored or drifts | **Enforced** (Defined in SPEC) |
| **Outcome** | Code snippets, tech debt | Production-ready application |

---

## 📖 Core Commands

Here are the core workflows. Click the link for full documentation on each command, including all parameters, options, and examples.

| Command | Description | Full Documentation |
| :--- | :--- | :--- |
| `/smartspec_generate_spec.md` | Creates a new SPEC document from an idea. | [📄 View Docs](.smartspec-docs/workflows/generate_spec.md) |
| `/smartspec_generate_plan.md` | Creates a high-level project plan from a SPEC. | [📄 View Docs](.smartspec-docs/workflows/generate_plan.md) |
| `/smartspec_generate_tasks.md` | Breaks down a SPEC into a detailed `tasks.md` checklist. | [📄 View Docs](.smartspec-docs/workflows/generate_tasks.md) |
| `/smartspec_generate_implement_prompt.md` | Generates a context-rich prompt for your AI assistant. | [📄 View Docs](.smartspec-docs/workflows/generate_implement_prompt.md) |
| `/smartspec_implement_tasks.md` | Autonomously implements tasks using an AI agent. | [📄 View Docs](.smartspec-docs/workflows/implement_tasks.md) |
| `/smartspec_reverse_to_spec.md` | Reverse-engineers an existing codebase into a SPEC. | [📄 View Docs](.smartspec-docs/workflows/reverse_to_spec.md) |
| `/smartspec_sync_spec_tasks.md` | Synchronizes a `tasks.md` file with its source SPEC. | [📄 View Docs](.smartspec-docs/workflows/sync_spec_tasks.md) |
| `/smartspec_verify_tasks_progress.md` | Verifies and tracks the progress of implementation. | [📄 View Docs](.smartspec-docs/workflows/verify_tasks_progress.md) |

---

## 💡 Vibe Coding Workflows

SmartSpec integrates seamlessly with your favorite tools.

### The Concept: Plan the Work, then Vibe the Work

Take 5-10 minutes upfront to generate a `spec.md` and `tasks.md`. This small investment provides the roadmap and context your AI assistant needs to perform at its best.

### Example Workflows

#### **1. The Power User: `Cursor` / `VSCode + Claude` / `Antigravity`**

1.  **Generate Tasks:** `/smartspec_generate_tasks.md`
2.  **Generate a Prompt:** `/smartspec_generate_implement_prompt.md --task T001`
3.  **Paste & Vibe:** Paste the context-rich prompt into your tool.
4.  **Implement & Verify:** Guide the AI, refactor, and test.
5.  **Mark as Done:** Check off the task in `tasks.md`.
6.  **Repeat:** Generate a prompt for the next task.

#### **2. The Automator: `Kilo Code`**

1.  **Generate Tasks:** `/smartspec_generate_tasks.md`
2.  **Execute Autonomously:** `/smartspec_implement_tasks.md`
3.  **Review:** Come back to review the completed, high-quality code.

---

## 🧩 Advanced Features

### Profiles: Tailored SPECs for Different Project Types

| Profile | Best For |
| :--- | :--- |
| `basic` | Simple CRUD apps, prototypes |
| `backend-service` | Scalable backend services |
| `financial` | Fintech, billing, payments |
| `full` | Enterprise-grade systems |

### Domains: Specialized Content for Your Industry

| Domain | What It Adds |
| :--- | :--- |
| `fintech` | PCI DSS guidance, audit logging |
| `healthcare` | HIPAA compliance notes, PHI handling |
| `iot` | Device identity, OTA updates |
| `ai` | Model evaluation, bias mitigation |

---

## 🏛️ For the LLM: How to Read This Repository

- **Project Goal:** To provide structure and architectural governance to AI-driven software development.
- **Key Artifacts:** `spec.md` (the blueprint), `tasks.md` (the checklist), `.kilocode/workflows/` (the logic), `.smartspec-docs/` (the documentation).
- **Core Principle:** Follow the workflow: `spec.md` → `tasks.md` → implementation. To understand a command, read its corresponding file in `.smartspec-docs/workflows/`.

---

## 📄 License

Licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.
