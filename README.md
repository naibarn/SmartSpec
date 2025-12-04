# SmartSpec V5 — Production‑Grade Documentation

SmartSpec V5 is a **next‑generation Specification Orchestration System** designed for high‑integrity software projects. It unifies:
- Specification generation (SPEC)
- Task planning (tasks.md)
- Kilo Code implementation prompts
- Multi‑domain architecture patterns
- Validation, compliance, and performance governance

This README is written as a **production‑grade guide**, integrating all capabilities from the full **SmartSpec V5 Documentation**, including advanced features such as Profiles, Domain Detection, Config Files, Meta‑Tags, Validation Rules, and Migration Behavior.

---

# 🧭 1. What is SmartSpec V5?
SmartSpec V5 is a framework that standardizes how complex software specifications are:
- **Created** (SPEC)
- **Validated** (Architect Validation Engine)
- **Expanded** into implementation tasks (tasks.md)
- **Converted** into executable prompts (Kilo Code prompts)

V5 includes:
- A modular architecture
- Domain‑specific enhancements
- Strong validation and compliance rules
- Human‑readable but machine‑optimized outputs
- Built‑in enterprise governance

---

# ⚡ 2. V5 Core Capabilities
### ✔ Multi‑Profile SPEC generation
### ✔ Domain‑driven specialization (fintech, healthcare, IoT, AI, etc.)
### ✔ Configurable DI, Security, and Performance levels
### ✔ Auto‑validation engine with error levels
### ✔ Force‑update and partial‑update modes
### ✔ Meta‑Tag protected sections (never overwritten)
### ✔ Compact mode and Full mode
### ✔ Project‑level and Organization‑level configuration files
### ✔ V4 → V5 migration compatibility

---

# 🏗️ 3. System Architecture Overview
```
 ┌──────────────────────────────┐
 │        User / Developer      │
 └───────────────┬──────────────┘
                 │ CLI / UI
 ┌───────────────▼──────────────────────────────┐
 │             SmartSpec V5 Engine              │
 ├───────────────────────────┬──────────────────┤
 │  SPEC Generator (Profiles)│ Domain Engine    │
 │  SPEC Updater             │ DI/Security Mode │
 │  SPEC Validator           │ Performance Mode │
 ├───────────────────────────┼──────────────────┤
 │          Task Generator (tasks.md)           │
 ├───────────────────────────┼──────────────────┤
 │         Kilo Code Prompt Generator           │
 └───────────────────────────┴──────────────────┘
```

---

# 🧩 4. Profiles System (V5)
Profiles define the **template structure**, **mandatory sections**, and **validation rules**.

### Available Profiles
- `basic` – simple CRUD / small backend services
- `backend-service` – scalable services with integrations
- `financial` – ledger, credit, billing, audit‑required systems
- `full` – enterprise‑grade SPEC, maximum safety & detail

### Choose a profile
```bash
/smartspec_generate_spec.md specs/feature/spec-XXX-your-feature/spec.md
```
Then select the desired profile (basic, backend-service, financial, or full) when prompted.

---

# 🌐 5. Domains (Auto‑Applied Enhancements)
Domains add specialized content to SPECs.

### Supported Domains
- `fintech` → adds STRIDE‑full, audit logging, PCI DSS guidance
- `healthcare` → HIPAA data protection notes
- `iot` → device identity, OTA update safety
- `ai` → model evaluation, dataset governance
- `realtime` → low‑latency SLA guidance
- `batch` → throughput and ETL safety
- `internal` → relaxed security & flexible patterns

### How to apply
```bash
/smartspec_generate_spec.md specs/feature/spec-XXX-your-feature/spec.md
```
Then specify the domain (fintech, healthcare, iot, ai, realtime, batch, or internal) when prompted.

---

# 🔒 6. Meta‑Tags (Write‑Protected Sections)
SmartSpec V5 respects protected regions using meta‑tags.

Example:
```md
<!-- @critical security -->
This security section will never be overwritten.
```

Supported meta‑tags:
- `@critical security`
- `@critical config`
- `@critical legal`
- `@critical audit`
- `@no-edit`

These ensure updates will **never remove essential sections**.

---

# 🧱 7. Dependency Injection Control Modes
V5 allows flexible DI patterns.

### Modes
- `--di=none` → no DI section
- `--di=minimal` → lightweight DI
- `--di=auto` → recommended DI pattern (default)
- `--di=full` → full DI pattern with interfaces & examples

### Example
Run `/smartspec_generate_spec.md` and specify DI mode (none, minimal, auto, or full) when prompted.

---

# 🛡️ 8. Security Modes
Available modes:
- `stride-basic` → basic security coverage
- `stride-full` → comprehensive security coverage

Run `/smartspec_generate_spec.md` and specify security mode when prompted.

`stride-full` includes:
- full threat table
- tampering protection
- replay‑attack notes
- non‑repudiation patterns

---

# 🚀 9. Performance Modes
Available modes:
- `basic` → basic performance requirements
- `full` → comprehensive performance requirements

Run `/smartspec_generate_spec.md` and specify performance mode when prompted.

`performance=full` adds:
- P50 / P95 / P99 targets
- throughput requirements
- SLA uptime
- queue/DB performance baselines
- load testing requirements

---

# ⚙️ 10. Configuration Files (Project & Org Level)
SmartSpec V5 uses two config layers.

### 1) Project‑level config
`smartspec.config.json`
```
{
  "profile": "financial",
  "domain": "fintech",
  "security": "stride-full",
  "performance": "full"
}
```

### 2) Organization‑level config
`.smartspec/config.json`
```
{
  "defaultProfile": "backend-service",
  "enforceSecurity": true,
  "allowModeOverride": false
}
```

---

# 📦 11. Compact Mode
For minimal SPECs, run `/smartspec_generate_spec.md` and specify compact mode when prompted.

Compact mode removes:
- examples
- deep STRIDE details
- implementation guides

Useful for:
- rapid prototyping
- internal‑only designs

---

# 📜 12. Force Update System
Used when SPEC sections became outdated.

To force update specific sections:
1. Run `/smartspec_generate_spec.md`
2. Specify force-update options when prompted:
   - `stride` → update security section only
   - `performance,config` → update multiple sections
   - `all` → update all sections

---

# 🧪 13. Validation System (Automatic Checks)
Validation runs on SPEC generation & update.

### ERROR‑level (must fix)
- missing security for financial domain
- missing retry logic for external APIs
- missing configuration schema
- invalid/missing STRIDE when required

### WARNING‑level
- domain mismatch
- deprecated template sections

Validation ensures outputs are **safe, consistent, and complete**.

---

# 🔄 14. Migration Guide (V4 → V5)
SmartSpec V5 preserves V4 behavior but adds stricter defaults.

### Improvements in V5
- profiles system
- domain‑aware enhancements
- protected meta‑tags
- performance/security controls
- validation engine

### Update older SPECs
Run `/smartspec_generate_spec.md` with your existing SPEC to upgrade to V5 format.

This adds missing:
- Non‑Goals
- Domain content
- Performance requirements
- STRIDE enhancements

---

# 🛠️ 15. Workflow Summary
SmartSpec V5 ships with seven main workflows.

### 1) Generate SPEC
```bash
/smartspec_generate_spec.md <spec_path>
```
Example: `/smartspec_generate_spec.md specs/feature/spec-004-financial-system/spec.md`

Outputs a new SmartSpec v5‑format SPEC.

### 2) Generate Plan
```bash
/smartspec_generate_plan.md <spec_path>
```
Example: `/smartspec_generate_plan.md specs/feature/spec-004-financial-system/spec.md`

Generates project plan from SPEC requirements.

### 3) Generate Tasks
```bash
/smartspec_generate_tasks.md <spec_path>
```
Example: `/smartspec_generate_tasks.md specs/feature/spec-004-financial-system/spec.md`

Converts SPEC → tasks.md with checkboxes and subtasks.

### 4) Generate Implementation Prompt
```bash
/smartspec_generate_implement_prompt.md <tasks_path> [options]
```
Example: `/smartspec_generate_implement_prompt.md specs/feature/spec-004-financial-system/tasks.md`

Converts tasks.md → implementation prompt with platform-specific instructions.

**Options:**
- `--phase 1` or `--phase 1-3` → Filter specific phases
- `--tasks T001-T010` → Filter specific tasks
- `--kilocode` → Generate for Kilo Code (auto subtasks, mode switching)
- `--claude` → Generate for Claude Code (sub agents, interactive) [default]
- `--roocode` → Generate for Roo Code
- `--specindex="path"` → Custom SPEC_INDEX path

**Output:** `implement-prompt-<spec-id>-<timestamp>.md`

### 5) Implement Tasks (Auto)
```bash
/smartspec_implement_tasks.md <tasks_path|prompt_path|folder> [options]
```
Example: `/smartspec_implement_tasks.md specs/feature/spec-004-financial-system/tasks.md`

Auto-implement tasks with safety constraints, progress tracking, and validation.

**Options:**
- `--phase 1-3` → Implement specific phases only
- `--tasks T001-T010` → Implement specific tasks only
- `--resume` → Continue from last checkpoint
- `--skip-completed` → Skip checked tasks [default]
- `--force-all` → Re-implement all tasks (ignore checkboxes)
- `--validate-only` → Validate only, no implementation

**Features:**
- ✅ Progress tracking (updates checkboxes in tasks.md)
- ✅ Checkpoint system (every 5 tasks)
- ✅ Resume functionality
- ✅ Dependency checking
- ✅ Safety constraints enforcement
- ✅ Comprehensive reporting

### 6) Generate Cursor/Antigravity Prompts
```bash
/smartspec_generate_cursor_prompt.md <tasks_path> --task <task_selection> [options]
```
Example: `/smartspec_generate_cursor_prompt.md specs/feature/spec-004-financial-system/tasks.md --task T001`

Generates user-friendly prompts from tasks.md for Cursor/Antigravity vibe coding.

**Options:**
- `--task T001` → Single task
- `--task T001,T002,T003` → Multiple tasks (comma-separated)
- `--task T001-T010` → Task range
- `--task T050 --breakdown` → Auto-breakdown large tasks (>8h)
- `--subtask T050.1,T050.2` → Specific subtasks
- `--skip-completed` → Skip tasks marked [x]
- `--antigravity` → Optimize for Antigravity (default: cursor)
- `--all` → Generate one prompt per task

**Features:**
- ✅ Simple, non-technical prompts
- ✅ Step-by-step instructions
- ✅ Context preservation (previous tasks, dependencies)
- ✅ Code structure examples
- ✅ Platform-specific tips (Cursor/Antigravity)
- ✅ Subtask breakdown for large tasks
- ✅ Hybrid workflow support (switch between platforms)

**Output:** `cursor-prompt-<tasks>.md` or multiple files with `--all`

### 7) Sync SPEC and Tasks
```bash
/smartspec_sync_spec_tasks.md <spec_path> <tasks_path>
```
Example: `/smartspec_sync_spec_tasks.md specs/feature/spec-004-financial-system/spec.md specs/feature/spec-004-financial-system/tasks.md`

Synchronizes SPEC with tasks.md to ensure consistency.

### 8) Verify Tasks Progress
```bash
/smartspec_verify_tasks_progress.md <tasks_path>
```
Example: `/smartspec_verify_tasks_progress.md specs/feature/spec-004-financial-system/tasks.md`

Verifies and tracks progress of implementation tasks.

---

# 📚 16. Knowledge Base Files
Stored in `.smartspec/` directory.

Includes:
- DI Pattern Template
- Security STRIDE Template
- Performance Requirements
- Implementation Checklist
- SPEC Structure & Rules
- Domain Enhancement Packs

---

# 🧪 17. Example Usage
### Create a fintech SPEC
```bash
/smartspec_generate_spec.md specs/feature/spec-004-financial-system/spec.md
```
Then specify in conversation: financial profile, fintech domain, stride-full security, full performance

### Generate project plan
```bash
/smartspec_generate_plan.md specs/feature/spec-004-financial-system/spec.md
```
Creates structured project plan from SPEC requirements.

### Generate tasks from SPEC
```bash
/smartspec_generate_tasks.md specs/feature/spec-004-financial-system/spec.md
```
Generates detailed task breakdown with checkboxes and subtasks.

### Generate Implementation Prompt
```bash
/smartspec_generate_implement_prompt.md specs/feature/spec-004-financial-system/tasks.md
```
Generates implementation prompts from tasks.md with platform-specific instructions.

**For Kilo Code:**
```bash
/smartspec_generate_implement_prompt.md specs/feature/spec-004-financial-system/tasks.md --kilocode
```

**For Claude Code (default):**
```bash
/smartspec_generate_implement_prompt.md specs/feature/spec-004-financial-system/tasks.md --claude
```

**For specific phases/tasks:**
```bash
/smartspec_generate_implement_prompt.md specs/feature/spec-004-financial-system/tasks.md --phase 1-2 --tasks T001-T010
```

### Auto-Implement Tasks
```bash
/smartspec_implement_tasks.md specs/feature/spec-004-financial-system/tasks.md
```
Auto-implement tasks with safety constraints and progress tracking.

### Generate Cursor Prompts (Vibe Coding)
```bash
# Single task
/smartspec_generate_cursor_prompt.md specs/feature/spec-004-financial-system/tasks.md --task T001

# Multiple tasks
/smartspec_generate_cursor_prompt.md specs/feature/spec-004-financial-system/tasks.md --task T001-T005

# Large task with breakdown
/smartspec_generate_cursor_prompt.md specs/feature/spec-004-financial-system/tasks.md --task T050 --breakdown

# Skip completed tasks
/smartspec_generate_cursor_prompt.md specs/feature/spec-004-financial-system/tasks.md --task T011-T020 --skip-completed
```
Generates simple, user-friendly prompts for Cursor/Antigravity.

**Hybrid Workflow Example:**
```bash
# Phase 1: Use Kilo Code (autonomous)
kilo code implement tasks.md --task T001-T010

# Phase 2: Switch to Cursor (manual control)
/smartspec_generate_cursor_prompt.md tasks.md --task T011-T015 --skip-completed
# Copy prompt to Cursor and implement

# Phase 3: Back to Kilo Code
kilo code implement tasks.md --task T016-T050 --skip-completed
```

**Resume from checkpoint:**
```bash
/smartspec_implement_tasks.md specs/feature/spec-004-financial-system/tasks.md --resume
```

**Implement specific phase:**
```bash
/smartspec_implement_tasks.md specs/feature/spec-004-financial-system/tasks.md --phase 1
```

**Validate only:**
```bash
/smartspec_implement_tasks.md specs/feature/spec-004-financial-system/tasks.md --validate-only
```

### Sync SPEC with tasks
```bash
/smartspec_sync_spec_tasks.md specs/feature/spec-004-financial-system/spec.md specs/feature/spec-004-financial-system/tasks.md
```
Ensures SPEC and tasks.md are synchronized.

### Verify implementation progress
```bash
/smartspec_verify_tasks_progress.md specs/feature/spec-004-financial-system/tasks.md
```
Tracks and validates task completion status.

---

# 🧭 18. Troubleshooting
- **SPEC missing sections** → run `/smartspec_generate_spec.md` with appropriate profile
- **Validation errors** → check ERROR‑level rules in output
- **Implementation prompt missing tasks** → re‑run `/smartspec_generate_tasks.md`
- **Tasks out of sync** → run `/smartspec_sync_spec_tasks.md`
- **Domain mismatch** → check `smartspec.config.json`

---

# 🗺️ 19. Roadmap
- Plugin SDK
- Template Marketplace
- Automatic Diagram Renderer
- Integration with Kilo Cloud
- Unified Multi‑SPEC Architecture Projects

---

# 🏁 20. License

SmartSpec is licensed under the **MIT License**.

This means you are free to:
- ✅ Use SmartSpec for commercial and non-commercial projects
- ✅ Modify and adapt SmartSpec to your needs
- ✅ Distribute SmartSpec and your modifications
- ✅ Use SmartSpec in proprietary software

See the [LICENSE](LICENSE) file for full details.

---

## MIT License Summary

```
MIT License

Copyright (c) 2025 SmartSpec Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

