# SmartSpec: AI-Native Development Framework

**The structured workflow that brings quality, consistency, and speed to your AI-powered development.**

---

## 🚀 Quick Start

### 1. What is SmartSpec?

SmartSpec is a command-line tool that orchestrates AI coding assistants (like Cursor, Claude, Kilo Code) by providing them with a structured plan. It turns chaotic "vibe coding" into a predictable, high-quality process.

**It solves the core problem of AI development: AI agents lack long-term context and architectural vision.** SmartSpec provides that vision.

### 2. How it Works: The 3-Step Workflow

1.  **Generate a SPEC:**
    ```bash
    /smartspec_generate_spec.md <path_to_spec>
    ```
    Answer a few questions to get a comprehensive blueprint (`spec.md`) for your feature.

2.  **Generate Tasks:**
    ```bash
    /smartspec_generate_tasks.md <path_to_spec>
    ```
    Get a detailed checklist of implementation tasks (`tasks.md`).

3.  **Generate a Prompt & Vibe:**
    ```bash
    /smartspec_generate_implement_prompt.md <path_to_tasks> --task T001
    ```
    Get a context-rich prompt for your favorite AI tool and start coding.

### 3. Installation

Get up and running in 30 seconds.

**Unix / macOS / Linux:**
```bash
curl -fsSL https://raw.githubusercontent.com/naibarn/SmartSpec/main/.smartspec/scripts/install.sh | bash
```

**Windows (PowerShell):**
```powershell
iwr -useb https://raw.githubusercontent.com/naibarn/SmartSpec/main/.smartspec/scripts/install.ps1 | iex
```

---

## 🤔 Why SmartSpec? From Vibe Coding Chaos to Structured Velocity

AI coding is fast, but it's often chaotic. SmartSpec brings the structure needed for sustainable speed.

| | **Traditional "Vibe Coding"** | **SmartSpec-Powered Development** |
| :--- | :--- | :--- |
| **Process** | Ad-hoc, prompt-by-prompt | **SPEC → TASKS → CODE** (Systematic) |
| **Quality** | Inconsistent | **Consistently High** (Enforced by SPEC) |
| **Architecture** | Ignored or drifts | **Enforced** (Defined in SPEC) |
| **Outcome** | Code snippets, tech debt | Production-ready application |

<details>
<summary>Click to expand for detailed workflows and advanced features</summary>

---

## 💡 Detailed Workflow: Supercharge Your Vibe Coding

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

#### **3. The Hybrid Approach (Most Common)**

- **Automate the Grunt Work:** Use `/smartspec_implement_tasks.md --tasks T001-T010` for boilerplate.
- **Vibe the Complex Parts:** Use `/smartspec_generate_implement_prompt.md --task T011` for core logic in Cursor/VSCode.
- **Return to Automation:** Let the agent finish the rest.

---

## 📖 Core Commands

| Command | Description | Full Documentation |
| :--- | :--- | :--- |
| `/smartspec_generate_spec.md <path>` | Creates a new SPEC document from a high-level idea. | [📄 View Docs](.smartspec-docs/workflows/generate_spec.md) |
| `/smartspec_generate_plan.md <spec_path>` | Creates a high-level project plan from a SPEC. | [📄 View Docs](.smartspec-docs/workflows/generate_plan.md) |
| `/smartspec_generate_tasks.md <spec_path>` | Breaks down a SPEC into a detailed `tasks.md` checklist. | [📄 View Docs](.smartspec-docs/workflows/generate_tasks.md) |
| `/smartspec_generate_implement_prompt.md <tasks_path>` | Generates a context-rich prompt for a specific task. | [📄 View Docs](.smartspec-docs/workflows/generate_implement_prompt.md) |
| `/smartspec_implement_tasks.md <tasks_path>` | Autonomously implements tasks using an agent like Kilo Code. | [📄 View Docs](.smartspec-docs/workflows/implement_tasks.md) |
| `/smartspec_reverse_to_spec.md <src_path>` | Reverse-engineers an existing codebase into a SPEC. | [📄 View Docs](.smartspec-docs/workflows/reverse_to_spec.md) |
| `/smartspec_sync_spec_tasks.md` | Synchronizes a `tasks.md` file with its source SPEC. | [📄 View Docs](.smartspec-docs/workflows/sync_spec_tasks.md) |
| `/smartspec_verify_tasks_progress.md <tasks_path>` | Verifies and tracks progress of implementation tasks. | [📄 View Docs](.smartspec-docs/workflows/verify_tasks_progress.md) |

---

## 🎯 Quick Start Example: Building a Credit Purchase Feature

1.  **Generate the SPEC:**
    ```bash
    /smartspec_generate_spec.md specs/credit-purchase/spec.md
    ```
    (Choose `fintech` domain, `financial` profile)

2.  **Generate Tasks:**
    ```bash
    /smartspec_generate_tasks.md specs/credit-purchase/spec.md
    ```
    This creates `tasks.md` with tasks like `T001: Setup database schema`, `T002: Create POST /api/credit/purchase endpoint`, etc.

3.  **Implement (Hybrid Approach):**
    ```bash
    # Automate the boilerplate
    /smartspec_implement_tasks.md specs/credit-purchase/tasks.md --tasks T001-T003

    # Manually implement the payment logic
    /smartspec_generate_implement_prompt.md specs/credit-purchase/tasks.md --task T004
    # (paste into Cursor)
    ```

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

### Configuration & Meta-Tags

- **Project Config:** Use `smartspec.config.json` to set default profiles and domains.
- **Org Config:** Use `.smartspec/config.json` for organization-wide rules.
- **Meta-Tags:** Use `<!-- @critical security -->` to protect sections from being overwritten.

---

## 🏛️ For the LLM: How to Read This Repository

- **Project Goal:** To provide structure and architectural governance to AI-driven software development.
- **Key Artifacts:** `spec.md` (the blueprint), `tasks.md` (the checklist), `.kilocode/workflows/` (the logic).
- **Core Principle:** Follow the workflow: `spec.md` → `tasks.md` → implementation.

---

## 🐛 Troubleshooting

| Problem | Solution |
| :--- | :--- |
| **SPEC missing sections** | Re-run `/smartspec_generate_spec.md` with a more comprehensive profile (e.g., `full`). |
| **Tasks out of sync** | Run `/smartspec_sync_spec_tasks.md`. |
| **Validation errors** | Check the ERROR-level rules in the output. |

---

## 📄 License

Licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

</details>
