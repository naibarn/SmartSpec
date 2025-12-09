---

## manual: /smartspec\_project\_copilot version: 5.7 compatible\_workflow\_versions: 5.6.x language: en role: User guide for Project-level advisor / workflow router / roadmap planner

# 1. Overview

`/smartspec_project_copilot` is a **project-level copilot** for SmartSpec. It acts as a project "secretary" that reads SmartSpec artifacts and workflows, then answers natural-language questions such as:

- "How far along is this project?"
- "What is the progress of the billing / subscription features?"
- "Given this CI / security / release report, what should we do next?"
- "Which SmartSpec workflows should I run now, and with which commands?"

The copilot:

- reads `SPEC_INDEX`, registries, reports and workflow docs/manuals;
- understands intent from plain-language questions;
- summarises status by service/domain and by phase (spec, plan, tasks, CI, security, UI, release);
- proposes **ready-to-run **``** commands** with reasonable flags;
- on Kilo with `--kilocode`, behaves as an Orchestrator-style advisor, focusing on planning & analysis rather than code changes.

> Important: the copilot is NO-WRITE — it does not edit code, specs, plans, or tasks directly.

---

# 2. What’s New in this manual (v5.7)

- Adds detailed **chat-style use cases** (ask like ChatGPT, no flags needed).
- Adds a full **billing & subscription** example showing how the copilot uses `SPEC_INDEX` + folders → concrete `/smartspec_generate_tasks` commands.
- Documents **chunked context** behaviour (\~500–800 lines per call).
- Clarifies how `--kilocode` implies Orchestrator-led behaviour on Kilo.

---

# 3. When to Use / When Not to Use

## 3.1 Use this workflow when

- You want a single entry point instead of learning all `/smartspec_*` workflows.
- You want to see progress per service/domain (e.g. billing, checkout, authentication) across phases.
- You have reports from other workflows and want a unified interpretation and next-step plan.
- You want a short-term roadmap for a feature/product based on the actual current state.
- You want natural-language routing to the right workflows with example commands.

## 3.2 Do not use this workflow when

- You expect it to edit code/spec/plan/tasks (it is NO-WRITE).
- You want to skip specialist workflows (CI gate, security audit, performance verifier, UI audit).
- You want to bypass human approvals for security/architecture decisions.

---

# 4. Required Project Setup

For best results, your project should have:

1. Basic SmartSpec structure
   - `.spec/SPEC_INDEX.json`
   - `.spec/registry/**` (including `tool-version-registry.json` if present)
   - `.spec/reports/**` (from prior workflow runs)
2. Governance files
   - `.smartspec/system_prompt_smartspec.md`
   - `.smartspec/knowledge_base_smartspec.md`
3. Workflow documentation
   - `.smartspec-docs/workflows/**` (TH/EN manuals and workflow examples)

If any of these are missing, the copilot should treat that as a governance gap, call it out, and suggest installing/updating SmartSpec before you rely on its advice.

---

# 5. Chat-style usage (no flags required)

For most users, you **don’t need to know flags or options**. Think of this workflow as a project chat:

> Open `/smartspec_project_copilot` and ask questions in plain language.\
> The copilot will read the relevant SmartSpec artifacts and answer.

Below are common use cases.

## 5.1 Ask for overall progress + % per service

**User message:**

> Where is the project right now? Which services are already finished? Roughly what percentage is done for each service? For anything not finished yet, what should we do next, in which order?

**Copilot behaviour:**

- uses `SPEC_INDEX` to discover specs/services;
- reads `spec.md`, `plan.md`, `tasks.md` and key reports in **chunks** (no more than \~500–800 lines per call);
- estimates progress by phase (spec/plan/tasks/CI/security/UI/release);
- reports rough % per service with a short explanation of how it was derived;
- suggests concrete next steps (e.g. create tasks, run CI gate, run security audit, run release readiness).

## 5.2 Focus on a few services by name

**User message:**

> Please focus only on:
>
> - payment-service
> - checkout-service
>
> For each one, estimate roughly what % is done, list the important remaining work, and order the next actions by priority.

**Copilot behaviour:**

- treats the named services as the scope;
- finds related specs from `SPEC_INDEX`;
- reads only the relevant files and reports;
- summarises progress and proposes next steps per service.

## 5.3 Paste a report and ask “what should we do next?”

**Situation:** you have a CI/security/release report but it’s dense.

**User steps:**

1. Run the CI/security/release workflow as usual.
2. Copy the important parts of its report.
3. Open the copilot and ask:

> Based on the report below:
>
> - Summarise what passed and what failed
> - Highlight any blockers that must be fixed before release
> - Suggest what we should do next, in order
> - Tell me which SmartSpec workflows we should run next and why
>
> (then paste the report content here)

**Copilot behaviour:**

- recognises which workflow created the report;
- reads the relevant parts in chunks;
- summarises in human language;
- highlights blockers;
- recommends follow-up workflows and, when useful, example commands.

## 5.4 Ask for a short roadmap in plain language

**User message:**

> Assume we want to ship feature X to production within the next 2 months.\
> Given our current state, please propose a roadmap:
>
> - What should we focus on in the next 1–2 sprints?
> - Which workflows should we run at each phase?
> - What are the main risks (security / CI / UI / performance) we must address first?

**Copilot behaviour:**

- inspects specs/plans/tasks/reports related to feature X;
- organises work into phases, e.g. Spec/Plan → CI/Security → UI → Release;
- ties each phase to recommended workflows, e.g.:
  - `smartspec_generate_spec`, `smartspec_generate_plan`;
  - `smartspec_ci_quality_gate`, `smartspec_security_evidence_audit`;
  - `smartspec_ui_validation`, `smartspec_ui_consistency_audit`;
  - `smartspec_release_readiness`;
- produces a roadmap with prioritised tasks.

---

# 6. Billing & subscription progress example (detailed)

This example shows how the copilot should use `SPEC_INDEX` and actual folders to produce concrete, ready-to-run commands.

## 6.1 Example project state

Assume `.spec/SPEC_INDEX.json` shows the billing domain includes:

- `spec-076-billing-system` → `specs/feature/spec-076-billing-system/spec.md`
- `spec-090-billing-and-subscription-ui` → `specs/feature/spec-090-billing-and-subscription-ui/spec.md`

In each folder we have:

- `spec.md` ✅
- `plan.md` ✅
- `tasks.md` ❌ (missing)

## 6.2 User question (plain language)

> I’d like to check how far the billing system has progressed,\
> including subscription billing.\
> How far along are we, and what should we do next?

## 6.3 What the copilot should do internally

1. Use `SPEC_INDEX` to find specs related to `billing` / `subscription`.
2. Inspect those folders for `spec.md`, `plan.md`, `tasks.md` and any relevant reports.
3. Interpret progress by phase:
   - Spec phase       : 100% (specs exist)
   - Planning phase   : 100% (plans exist)
   - Implementation planning : 0% (no `tasks.md` yet)
4. Conclude that billing is ready for implementation planning but tasks have not been defined.
5. Recommend concrete next steps as ready-to-run commands.

## 6.4 Example answer (shortened)

> **Billing & Subscription progress overview**
>
> - The billing domain currently has two main specs:
>   1. `spec-076-billing-system`
>   2. `spec-090-billing-and-subscription-ui`
> - Both have `spec.md` and `plan.md` → spec/plan phases are \~100%.
> - Neither has `tasks.md` → implementation planning is \~0%.
>
> **Recommended next steps:**
>
> 1. Generate `tasks.md` for the core billing system:
>
> ```bash
> /smartspec_generate_tasks specs/feature/spec-076-billing-system
> ```
>
> 2. Generate `tasks.md` for the Billing & Subscription UI:
>
> ```bash
> /smartspec_generate_tasks specs/feature/spec-090-billing-and-subscription-ui
> ```
>
> If you run these commands on Kilo, add `--kilocode`:
>
> ```bash
> /smartspec_generate_tasks specs/feature/spec-076-billing-system --kilocode
> /smartspec_generate_tasks specs/feature/spec-090-billing-and-subscription-ui --kilocode
> ```
>
> After these tasks files are created, you can run the copilot again to reassess progress (including implementation tasks, CI, security and UI readiness).

---

# 7. Using with Kilo (`--kilocode`)

When you run the copilot with `--kilocode` on Kilo:

- It behaves as an **Ask/Architect** advisor.
- Kilo Orchestrator is conceptually responsible for:
  - interpreting natural-language intent;
  - planning which files/reports to read;
  - reading those files in chunks (\~300–600 lines) and summarising them;
  - feeding summaries back to the copilot for reasoning.
- The copilot focuses on **analysis and planning**, not code edits.

Example conceptual call:

```bash
/smartspec_project_copilot --kilocode
```

Example user message:

> For the checkout service, what should we do in this sprint\
> to be ready for production?\
> Please list the recommended workflows and tasks in order.

The copilot should respond with a phased plan, e.g.:

- clean up spec/plan → `smartspec_generate_spec`, `smartspec_generate_plan`
- establish CI gate → `smartspec_ci_quality_gate`
- gather security evidence → `smartspec_security_evidence_audit`
- align UI → `smartspec_ui_validation`, `smartspec_ui_consistency_audit`
- check release readiness → `smartspec_release_readiness`

and include example commands, often with `--kilocode` when appropriate.

---

# 8. Do’s and Don’ts

**Do**

- Use the copilot as your **front door** to SmartSpec.
- Ask questions in natural language; let the copilot translate to specs, plans, tasks and workflows.
- Paste reports and ask "what should we do next?" instead of reading raw JSON.
- Use `--kilocode` on Kilo for better orchestration and safe chunked context management.

**Don’t**

- Expect the copilot to edit code/spec/plan/tasks directly (it is NO-WRITE).
- Treat it as a replacement for human security/architecture review.
- Ignore warnings about versions, CVEs, design-system drift or missing registries.

---

# 9. Backward Compatibility Notes

- This manual targets `/smartspec_project_copilot` workflow versions `5.6.x`.
- Future additions must be **additive**: new flags and behaviours may be added but existing ones must not be removed.

---

# 10. Basic Troubleshooting

- **Copilot says **``** is missing**
  - Check that `.spec/SPEC_INDEX.json` exists.
- **Copilot reports missing registries**
  - Create `tool-version-registry.json`, design tokens, or component registries as recommended, then re-run the copilot.
- **Advice seems out-of-date**
  - Verify that `.smartspec` and `.smartspec-docs` have been updated from the latest SmartSpec distribution.

When in doubt, platform/architecture teams should confirm the installed SmartSpec version, KB version, and workflow versions before debugging further.

