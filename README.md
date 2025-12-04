# SmartSpec: From Vague Idea to Production-Ready Code

**The AI-native framework for building reliable software, faster.**

---

SmartSpec is a command-line tool that bridges the gap between a high-level idea and a fully implemented, production-grade software project. It uses a series of structured workflows to guide AI agents and developers, ensuring quality, consistency, and speed from start to finish.

Whether you're a solo developer using Cursor for "vibe coding" or a team using Kilo Code for autonomous implementation, SmartSpec provides the architectural backbone that transforms chaotic AI-assisted development into a predictable, high-quality process.

---

## 🤔 Why SmartSpec? The Problem with Modern AI-Powered Development

AI coding assistants (like ChatGPT, Claude, Gemini, and Cursor) are incredibly powerful but often operate in a vacuum. They lack the high-level context, architectural constraints, and long-term vision required for building robust applications. This leads to common problems:

- **Inconsistent Quality:** Code quality varies wildly depending on the prompt and the AI's interpretation.
- **Architectural Drift:** The AI might choose a library or pattern that violates the project's architecture.
- **Lost Context:** The AI forgets previous decisions, security requirements, or business rules.
- **"Vibe Coding" Chaos:** It feels fast, but the lack of a structured plan results in technical debt, bugs, and difficult maintenance.

**SmartSpec solves this by acting as the "Orchestrator" or "System Architect" for your AI coding partner.** It provides the structured, long-term memory and architectural guidance that AI agents lack, turning chaotic "vibe coding" into a streamlined, predictable, and high-quality process.

| | **Traditional "Vibe Coding"** | **SmartSpec-Powered Development** |
| :--- | :--- | :--- |
| **Starting Point** | Vague idea, a few prompts | A structured, validated **SPEC** document |
| **Process** | Ad-hoc, reactive, prompt-by-prompt | **SPEC → PLAN → TASKS → CODE** (Systematic) |
| **Quality** | Inconsistent, depends on prompt quality | **Consistently High:** Enforced by validation rules |
| **Architecture** | Often ignored or inconsistent | **Enforced:** Architectural choices are baked into the SPEC |
| **Speed** | Feels fast initially, slows down due to rework | **Sustainably Fast:** Reduces rework and technical debt |
| **Outcome** | A collection of code snippets | A production-ready, maintainable application |

---

## 💡 How It Works: The Core Workflow

SmartSpec enforces a simple yet powerful workflow that transforms a high-level idea into production-ready code. This structure is designed to be intuitive for developers and easily parsable by LLMs.

```
┌─────────────┐
│  Your Idea  │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────────────────────┐
│  1. /smartspec_generate_spec.md → spec.md                            │
│     (System Overview, Data Model, API Spec,             │
│      Business Rules, Security, Performance)             │
└──────┬──────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────┐
│  2. /smartspec_generate_plan.md → plan.md                            │
│     (High-level phases, timeline, milestones)           │
└──────┬──────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────┐
│  3. /smartspec_generate_tasks.md → tasks.md                          │
│     (Detailed task breakdown with checkboxes)           │
└──────┬──────────────────────────────────────────────────┘
       │
       ├──────────────────────────────────────────────────┐
       │                                                   │
       ▼                                                   ▼
┌──────────────────────────┐                  ┌──────────────────────────┐
│ 4a. /smartspec_generate_implement_prompt.md     │                  │ 4b. /smartspec_implement_tasks.md     │
│     (For Cursor/Claude)  │                  │     (For Kilo Code)      │
│                          │                  │                          │
│  → Copy prompt to tool   │                  │  → Autonomous execution  │
│  → Vibe code manually    │                  │  → Auto progress track   │
└──────────────────────────┘                  └──────────────────────────┘
       │                                                   │
       └───────────────────┬───────────────────────────────┘
                           │
                           ▼
                  ┌────────────────┐
                  │ Production Code│
                  └────────────────┘
```

### The Steps in Detail

1.  **`/smartspec_generate_spec.md`**: **From Idea to Blueprint**
    - You start with a high-level feature idea (e.g., "Build a credit purchase system for a fintech app").
    - SmartSpec asks a series of targeted questions (about domain, security, performance) and generates a comprehensive **SPEC** document. This is the project's single source of truth, containing:
        - System Overview
        - Architecture Summary
        - Data Model (with ER diagrams)
        - API Specification
        - Feature Definitions & Use Cases
        - Business Rules
        - Security Requirements (STRIDE analysis)
        - Performance Requirements

2.  **`/smartspec_generate_plan.md`**: **From Blueprint to Strategy**
    - The SPEC is fed into the planning workflow.
    - SmartSpec creates a high-level, phased implementation **PLAN**, outlining the major stages of development (e.g., Phase 1: Database & API, Phase 2: Frontend, Phase 3: Testing & Deployment).
    - This plan includes timeline estimates and dependencies between phases.

3.  **`/smartspec_generate_tasks.md`**: **From Strategy to Actionable Tasks**
    - The PLAN is broken down into a detailed `tasks.md` file.
    - Each task has:
        - A unique Task ID (e.g., `T001`)
        - A clear description
        - Acceptance criteria
        - Effort estimation (hours)
        - Dependencies on other tasks
        - A checkbox for tracking completion (`[ ]` or `[x]`)

4.  **`/smartspec_generate_implement_prompt.md` or `/smartspec_implement_tasks.md`**: **From Tasks to Code**
    - **Option A (Manual Vibe Coding):** Run `/smartspec_generate_implement_prompt.md --task T001` to generate a context-rich, optimized prompt for your AI coding assistant of choice (Cursor, Claude, VSCode, Antigravity). This prompt contains all the necessary context from the SPEC and previous tasks. You paste it into your tool and implement the task.
    - **Option B (Autonomous Implementation):** Run `/smartspec_implement_tasks.md` to let an autonomous agent like Kilo Code execute the implementation, tracking progress and validating outputs automatically.

5.  **`/smartspec_reverse_to_spec.md` (Bonus)**: **From Existing Code to a SmartSpec Blueprint**
    - Have an existing project? This workflow reverse-engineers your codebase (TypeScript/Prisma for now) to generate a SPEC file, allowing you to adopt SmartSpec mid-project.

---

## 🚀 Supercharge Your Vibe Coding: The SmartSpec Workflow

SmartSpec isn't here to replace your favorite tools; it's here to make them better. It transforms "vibe coding" from a chaotic sprint into a structured, high-velocity development process. Here's how it fits into your existing workflow:

### The Concept: Plan the Work, then Vibe the Work

Instead of jumping straight into coding with a vague idea, you take **5-10 minutes upfront** to generate a SPEC and a `tasks.md` file with SmartSpec. This small investment pays massive dividends:

- **AI agents get the context they need** to make good architectural decisions.
- **You get a roadmap** that prevents you from getting lost in the weeds.
- **Quality is enforced** through validation rules baked into the SPEC.

**Your new workflow looks like this:**

1.  **Plan (5-10 mins):** Run `/smartspec_generate_spec.md` and `/smartspec_generate_tasks.md`.
2.  **Vibe (Your usual coding time):** Use the generated prompts to code with your favorite AI assistant.
3.  **Ship:** Deploy production-ready code, not a collection of hacks.

This simple change provides the structure and context AI needs to perform at its best, making your "vibe coding" sessions more productive and the results more reliable.

---

### Example Workflows: SmartSpec + Your Favorite Tools

Here are some popular development setups and how SmartSpec integrates with them:

#### **1. The Power User: `Cursor` / `VSCode + Claude` / `Antigravity`**

This workflow is for developers who want maximum control while still leveraging AI for heavy lifting.

**Setup:**
- Install SmartSpec (see below)
- Use your existing Cursor, VSCode + Claude extension, or Antigravity setup

**Workflow:**

1.  **Generate Tasks:** Run `/smartspec_generate_tasks.md` to get your `tasks.md` file.
2.  **Generate a Prompt:** Run `/smartspec_generate_implement_prompt.md --task T001` to get a detailed, context-rich prompt for the first task.
3.  **Paste & Vibe:** Paste the prompt into Cursor, VSCode, or Antigravity. The AI now has all the context (data models, API specs, business rules, security requirements) it needs.
4.  **Implement & Verify:** Use your skills to guide the AI, refactor, and test the code.
5.  **Mark as Done:** Check off the task in `tasks.md` (change `[ ]` to `[x]`).
6.  **Repeat:** Run `/smartspec_generate_implement_prompt.md --task T002` for the next task. SmartSpec automatically includes context from completed tasks, so the AI "remembers" what you've already built.

**Why This Works:**

| Tool | How SmartSpec Helps |
| :--- | :--- |
| **Cursor** | Provides deep, project-wide context that Cursor's `@file` feature might miss. Ensures architectural consistency across all AI-generated code. |
| **VSCode + Claude** | Turns a simple chat interface into a powerful, context-aware development partner. The generated prompts are optimized for Claude's strengths. |
| **Google Antigravity** | Provides the structured plan and context needed to make Antigravity's large-scale code generation reliable and maintainable. |

---

#### **2. The Automator: `Kilo Code`**

This workflow is for developers who want to automate as much of the implementation as possible.

**Setup:**
- Install SmartSpec (see below)
- Install Kilo Code

**Workflow:**

1.  **Generate Tasks:** Run `/smartspec_generate_tasks.md`.
2.  **Generate Kilo Prompt:** Run `/smartspec_generate_implement_prompt.md --kilocode` to create a master prompt for Kilo Code's Orchestrator mode.
3.  **Execute:** Let Kilo Code run the implementation autonomously. It will:
    - Follow the `tasks.md` file
    - Execute tasks sequentially
    - Track its own progress (checking off tasks)
    - Validate outputs against the SPEC
4.  **Review:** Come back to review the completed code, which was built according to the high-quality standards defined in the SPEC.

**Why This Works:**

Kilo Code excels at autonomous execution when given clear instructions. SmartSpec provides those instructions in a format Kilo Code understands perfectly, resulting in high-quality, hands-off implementation.

---

#### **3. The Hybrid Approach (Most Common)**

Mix and match based on the task's complexity. This is the most flexible and powerful workflow.

**Workflow:**

1.  **Automate the Grunt Work:** Use `Kilo Code` to implement the boilerplate and straightforward tasks (e.g., database setup, CRUD endpoints, basic authentication).
    ```bash
    kilo code implement tasks.md --tasks T001-T010
    ```

2.  **Vibe the Complex Parts:** For the core business logic, a tricky UI component, or something that requires creative problem-solving, switch to `Cursor` or `VSCode`. Generate a prompt for that specific task:
    ```bash
    /smartspec_generate_implement_prompt.md --task T011
    ```
    Paste it into your tool and implement it manually.

3.  **Return to Automation:** Once the complex part is done, let Kilo Code finish the rest.
    ```bash
    kilo code implement tasks.md --tasks T012-T050 --skip-completed
    ```

**Why This Works:**

SmartSpec seamlessly supports this by maintaining the state in the `tasks.md` file. It knows what's done and provides the right context, no matter which tool you use. You get the speed of automation where it makes sense and the control of manual coding where it's needed.

---

## 🚀 Getting Started: Installation

Get up and running in under a minute. The installer automatically detects your AI coding environment (Kilo Code, Roo Code, Claude Code) and sets up the workflows.

**Unix / macOS / Linux:**
```bash
curl -fsSL https://raw.githubusercontent.com/naibarn/SmartSpec/main/.smartspec/scripts/install.sh | bash
```

**Windows (PowerShell):**
```powershell
iwr -useb https://raw.githubusercontent.com/naibarn/SmartSpec/main/.smartspec/scripts/install.ps1 | iex
```

**What it does:**
- ✅ Auto-detects your platforms (Kilo Code, Roo Code, Claude Code)
- ✅ Downloads workflows to `.smartspec/workflows/`
- ✅ Creates symlinks (or copies) to platform directories
- ✅ Sets up auto-sync (if using copies)
- ✅ Ready to use in 30 seconds!

### Updating SmartSpec

To get the latest workflows and features:

**If using symlinks (automatic):**
```bash
cd .smartspec/workflows
git pull
# Changes reflect immediately in all platforms
```

**If using copies (manual sync):**
```bash
cd .smartspec/workflows
git pull
cd ../..
.smartspec/sync.sh      # Unix/Mac/Linux
.smartspec/sync.ps1     # Windows
```

### Uninstalling

```bash
bash .smartspec/scripts/uninstall.sh
```

Or manually:
```bash
rm -rf .smartspec .kilocode/workflows .roo/commands .claude/commands
```

---

## 📖 Core Commands

SmartSpec is designed to be LLM-friendly. You can interact with it using natural language, but here are the core commands for structured interaction.

| Command | Description | When to Use |
| :--- | :--- | :--- |
| `/smartspec_generate_spec.md <path>` | Creates a new, comprehensive SPEC document from a high-level idea. | At the very beginning of a new project or feature. |
| `/smartspec_generate_plan.md <spec_path>` | Creates a high-level, phased project plan from a SPEC. | After the SPEC is finalized and you need a strategic overview. |
| `/smartspec_generate_tasks.md <spec_path>` | Breaks down a SPEC into a detailed, actionable `tasks.md` checklist. | After the SPEC is ready and you want to start coding. |
| `/smartspec_generate_implement_prompt.md <tasks_path>` | Generates a context-rich prompt for a specific task. | Your main command during "vibe coding" with Cursor, VSCode, etc. |
| `/smartspec_implement_tasks.md <tasks_path>` | Autonomously implements tasks using an agent like Kilo Code. | When you want to automate implementation. |
| `/smartspec_reverse_to_spec.md <src_path>` | Reverse-engineers an existing codebase into a SPEC document. | When you want to apply SmartSpec to an existing project. |
| `/smartspec_sync_spec_tasks.md` | Synchronizes a `tasks.md` file with its source SPEC. | If you manually change the SPEC and need to update the tasks. |
| `/smartspec_verify_tasks_progress.md <tasks_path>` | Verifies and tracks progress of implementation tasks. | To get a status report on your project. |

---

## 🎯 Quick Start Example: Building a Credit Purchase Feature

Let's walk through a complete example to see SmartSpec in action.

### Step 1: Generate the SPEC

```bash
/smartspec_generate_spec.md specs/credit-purchase/spec.md
```

You'll be asked a series of questions:
- **Domain:** `fintech`
- **Profile:** `financial`
- **Security:** `stride-full`
- **Performance:** `full`

SmartSpec generates a comprehensive `spec.md` file with:
- System overview
- Data model (User, Credit, Transaction tables)
- API endpoints (POST /api/credit/purchase)
- Business rules (minimum purchase amount, payment validation)
- Security requirements (PCI DSS guidance, authentication, rate limiting)
- Performance targets (P95 < 500ms, 100 TPS)

### Step 2: Generate Tasks

```bash
/smartspec_generate_tasks.md specs/credit-purchase/spec.md
```

SmartSpec creates `tasks.md` with tasks like:
- `[ ] T001: Setup database schema (Prisma)`
- `[ ] T002: Implement Credit model`
- `[ ] T003: Create POST /api/credit/purchase endpoint`
- `[ ] T004: Implement payment gateway integration (Stripe)`
- `[ ] T005: Add authentication middleware`
- `[ ] T006: Add rate limiting`
- `[ ] T007: Write unit tests`
- `[ ] T008: Write integration tests`

### Step 3: Implement (Choose Your Path)

**Option A: Autonomous (Kilo Code)**
```bash
/smartspec_implement_tasks.md specs/credit-purchase/tasks.md
```
Let Kilo Code do the work. Come back to review.

**Option B: Manual (Cursor/VSCode)**
```bash
/smartspec_generate_implement_prompt.md specs/credit-purchase/tasks.md --task T001
```
Copy the prompt to Cursor and implement T001. Repeat for each task.

**Option C: Hybrid**
```bash
# Automate the boilerplate
kilo code implement tasks.md --tasks T001-T003

# Manually implement the payment logic (complex)
/smartspec_generate_implement_prompt.md tasks.md --task T004
# (paste into Cursor)

# Automate the rest
kilo code implement tasks.md --tasks T005-T008 --skip-completed
```

### Step 4: Verify Progress

```bash
/smartspec_verify_tasks_progress.md specs/credit-purchase/tasks.md
```

Get a status report:
```
✅ Phase 1: Database Setup (100%)
✅ Phase 2: API Implementation (100%)
⏳ Phase 3: Testing (50%)
   ✅ T007: Unit tests
   [ ] T008: Integration tests

Overall: 87.5% complete (7/8 tasks)
```

---

## 🧩 Advanced Features

### Profiles: Tailored SPECs for Different Project Types

SmartSpec uses **Profiles** to generate SPECs appropriate for your project's complexity.

| Profile | Best For | What It Includes |
| :--- | :--- | :--- |
| `basic` | Simple CRUD apps, prototypes | Minimal sections, no STRIDE, basic performance |
| `backend-service` | Scalable backend services | Full API spec, moderate security, integrations |
| `financial` | Fintech, billing, payments | Audit logging, PCI DSS guidance, full STRIDE |
| `full` | Enterprise-grade systems | Maximum detail, all sections, strict validation |

**How to use:**
When running `/smartspec_generate_spec.md`, you'll be prompted to choose a profile. Or set a default in `smartspec.config.json`:
```json
{
  "profile": "financial"
}
```

---

### Domains: Specialized Content for Your Industry

SmartSpec automatically adds domain-specific content to your SPEC.

| Domain | What It Adds |
| :--- | :--- |
| `fintech` | PCI DSS guidance, audit logging, financial data protection |
| `healthcare` | HIPAA compliance notes, PHI handling, consent management |
| `iot` | Device identity, OTA updates, offline-first patterns |
| `ai` | Model evaluation, dataset governance, bias mitigation |
| `realtime` | Low-latency SLA guidance, WebSocket patterns |
| `batch` | Throughput requirements, ETL safety, idempotency |
| `internal` | Relaxed security, flexible patterns (for internal tools) |

**How to use:**
Specify the domain when running `/smartspec_generate_spec.md`, or set it in `smartspec.config.json`:
```json
{
  "domain": "fintech"
}
```

---

### Configuration Files: Project & Organization Defaults

SmartSpec uses two levels of configuration:

**1. Project-level (`smartspec.config.json` in project root):**
```json
{
  "profile": "financial",
  "domain": "fintech",
  "security": "stride-full",
  "performance": "full"
}
```

**2. Organization-level (`.smartspec/config.json`):**
```json
{
  "defaultProfile": "backend-service",
  "enforceSecurity": true,
  "allowModeOverride": false
}
```

This ensures consistency across all projects in your organization.

---

### Meta-Tags: Protecting Critical Sections

Use meta-tags to prevent SmartSpec from overwriting critical sections during updates.

```markdown
<!-- @critical security -->
This security section will never be overwritten.
<!-- @end -->
```

Supported meta-tags:
- `@critical security`
- `@critical config`
- `@critical legal`
- `@critical audit`
- `@no-edit`

---

## 🏛️ For the LLM: How to Read This Repository

This section provides a structured guide for Large Language Models to understand and utilize this project effectively.

### Project Goal

SmartSpec is a CLI-based framework that provides structure, context, and architectural governance to AI-driven software development. It achieves this through a series of interdependent workflows that transform a high-level requirement into implemented code, ensuring quality and consistency.

### Key Artifacts

1.  **SPEC Document (`spec.md`):** The single source of truth. It defines the system's architecture, data models, API contracts, business rules, and security requirements. It is generated by `/smartspec_generate_spec.md`.
2.  **Task List (`tasks.md`):** A checklist of implementation tasks derived from the SPEC. It includes task IDs, descriptions, dependencies, and effort estimates. It is generated by `/smartspec_generate_tasks.md`.
3.  **Workflows (`.kilocode/workflows/`):** These are the core logic of SmartSpec. Each file defines a command (e.g., `smartspec_generate_spec.md`). They are written in Markdown and contain instructions, templates, and logic for the Kilo Code engine to execute.
4.  **Configuration (`.smartspec/config.json`):** A project-level configuration file that defines default profiles, domains, and security levels to ensure consistency.

### Core Principles for Analysis

- **Follow the Workflow:** To understand the project, trace the flow of data: `spec.md` → `plan.md` → `tasks.md` → implementation prompts.
- **Workflows are the Source of Truth:** The logic for each command is defined in the corresponding workflow file in the `.kilocode/workflows` directory. Analyze these files to understand the exact behavior of each command.
- **SPEC is the Blueprint:** When asked to implement a feature or fix a bug, always refer to the `spec.md` file first. It contains the authoritative requirements.
- **`tasks.md` Tracks State:** The `tasks.md` file, with its checkboxes (`[ ]` or `[x]`), is the canonical record of implementation progress.

### How to Generate Effective Prompts

When a user asks you to "implement task T005", follow this process:

1.  **Read the SPEC:** Load the `spec.md` file to understand the overall system.
2.  **Read the Task:** Find task T005 in `tasks.md` to understand the specific requirement.
3.  **Check Dependencies:** Look at the task's dependencies. If it depends on T001-T004, check if those are marked `[x]` (completed). If not, warn the user.
4.  **Generate Context:** Include relevant sections from the SPEC in your response:
    - Data models (if the task involves database changes)
    - API specifications (if the task involves API changes)
    - Business rules (if the task involves logic)
    - Security requirements (always)
5.  **Provide Code:** Generate the code to implement the task, following the architectural patterns defined in the SPEC.
6.  **Update State:** Remind the user to mark the task as complete (`[x]`) in `tasks.md`.

---

## 🐛 Troubleshooting

| Problem | Solution |
| :--- | :--- |
| **SPEC missing sections** | Re-run `/smartspec_generate_spec.md` with the appropriate profile (e.g., `full` instead of `basic`). |
| **Validation errors** | Check the ERROR-level rules in the output. Common issues: missing security for financial domains, missing retry logic for external APIs. |
| **Implementation prompt missing tasks** | Re-run `/smartspec_generate_tasks.md` to ensure the `tasks.md` file is up-to-date. |
| **Tasks out of sync with SPEC** | Run `/smartspec_sync_spec_tasks.md` to synchronize them. |
| **Domain mismatch warnings** | Check your `smartspec.config.json` file and ensure the domain matches your project type. |

---

## 🗺️ Roadmap

- **Plugin SDK:** Allow developers to create custom workflows and profiles.
- **Template Marketplace:** Share and discover SPEC templates for common use cases.
- **Automatic Diagram Renderer:** Generate architecture diagrams from SPECs.
- **Integration with Kilo Cloud:** Cloud-based execution and collaboration.
- **Unified Multi-SPEC Architecture:** Manage multiple SPECs in a single project (e.g., microservices).

---

## 📄 License

SmartSpec is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for full details.

This means you are free to:
- ✅ Use SmartSpec for commercial and non-commercial projects
- ✅ Modify and adapt SmartSpec to your needs
- ✅ Distribute SmartSpec and your modifications
- ✅ Use SmartSpec in proprietary software

---

**Built with ❤️ for the AI-native development era.**
