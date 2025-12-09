---
workflow: /smartspec_project_copilot
version: 5.6.2
role: project-level governance / advisor / workflow router / roadmap planner
write_guard: NO-WRITE
status: stable
compatible_kb:
  - SmartSpec Workflow & Manual Guardrails v5.6+ (this KB)
---

# 1. Summary

`/smartspec_project_copilot` is a **project-level copilot** for SmartSpec.
It reads SmartSpec artifacts, registries, and reports, then answers
natural-language questions such as:

- "How far along is this project?"
- "Which services are ready for release?"
- "What should we do next after this CI/security/UI report?"
- "Which SmartSpec workflows should I run next?"

This workflow is **governance-only**:
- It **does not modify** code, specs, tasks, or registries.
- It **summarises**, **assesses progress**, and **recommends** concrete
  next steps and ready-to-run commands.
- Under `--kilocode` it uses **Kilo Orchestrator mode** conceptually to
  analyse intent, plan chunked reads, and combine summaries into advice.


# 2. When to Use

Use `/smartspec_project_copilot` when you:

- Want a single entry point to understand project status without learning
  each `/smartspec_*` workflow.
- Want to know progress by service/domain (e.g., "billing", "checkout")
  across phases (spec, plan, tasks, CI, security, UI, release).
- Need help interpreting dense SmartSpec reports and deciding what to do next.
- Want a short-term roadmap for a feature or product based on current
  SmartSpec artifacts and reports.
- Want natural-language routing to the right SmartSpec workflows, with
  example commands and flags.

Do **not** use this workflow when you:

- Expect it to directly edit code/spec/tasks (it is strictly NO-WRITE).
- Want to bypass specialist workflows such as security audits, CI gates,
  or performance verifiers.
- Intend to bypass human approvals for security/architecture decisions.


# 3. Inputs & Outputs

## 3.1 Inputs

- Natural-language questions in any supported language (TH/EN encouraged).
- Optional flags (see Section 5) to:
  - narrow project scope;
  - focus on specific aspects (status, roadmap, security, CI, UI, perf);
  - point to specific reports or custom index/registry locations;
  - control output format and language.

## 3.2 Readable artifacts (RAG sources)

When answering, the copilot may read:

- **Index**
  - `.spec/SPEC_INDEX.json` (primary)
  - legacy mirrors per KB Section 5.1, if present.

- **Registries** under `.spec/registry/`:
  - `tool-version-registry.json`
  - `design-tokens-registry.json`
  - `ui-component-registry.json`
  - `app-component-registry.json`
  - `patterns-registry.json`
  - other registries relevant to the question.

- **Specs & adjacent files**
  - `specs/<category>/<spec-id>/spec.md`
  - `plan.md`, `tasks.md`, `ui.json` in the same folder.

- **Reports** under `.spec/reports/<workflow-name>/...`:
  - CI quality gate, security evidence audit, release readiness, UI audits,
    NFR/perf verifiers, etc.

- **Workflow specs & manuals**
  - `.smartspec/workflows/smartspec_*.md` (workflow definitions, flags,
    usage, examples).
  - `.smartspec-docs/workflows/**` (manuals and examples for workflows).

All reading is **read-only** and follows chunking rules (Section 9.3).

## 3.3 Outputs

- Human-readable summary of project/feature/service status.
- Progress per phase (spec, plan, tasks, CI, security, UI, release) with
  rough percentage estimates when feasible.
- Highlighted risks and blockers (Weakness & Risk Check style).
- Recommended next steps and **ready-to-run commands** for relevant
  `/smartspec_*` workflows, including example flags.
- Optional JSON/machine-readable structure when `--output-format json|mixed`
  is used.


# 4. Modes

## 4.1 Role & write guard

- Role: Governance / Advisor / Router.
- Write guard: **NO-WRITE**.
  - May read files and reports.
  - May generate summaries and recommendations.
  - Must **not** modify code, specs, tasks, or registries.

## 4.2 Safety modes

- `--safety-mode conservative` (default)
  - Conservative recommendations, extra warnings for security/version issues.
- `--safety-mode balanced`
  - Balanced risk vs velocity.
- `--safety-mode aggressive`
  - More opinionated suggestions, but still within KB guardrails.

`--strict` is a legacy alias for `--safety-mode conservative`.

## 4.3 Kilo / Orchestrator interaction

When `--kilocode` is present:

- Conceptual Kilo mode: **Orchestrator (Ask/Architect)**.
- Orchestrator is responsible for:
  - interpreting natural-language intent;
  - planning which files/registries/reports to read;
  - orchestrating chunked reads as described in Section 9.3;
  - combining summaries into a final human/JSON answer.
- Code mode (if used under the hood) is only for:
  - reading and slicing files into chunks;
  - generating short summaries of those chunks.
- The workflow remains NO-WRITE even under Kilo.


# 5. Flags

All flags are additive; none may be removed in future versions.

## 5.1 Scope & focus

- `--project-scope <pattern>`
  - Focus on a subset of services/specs/domains (e.g. `billing`,
    `payment-service`, `apps/console`).
- `--focus <aspect>`
  - `status`    → overall progress/status (default).
  - `roadmap`   → prioritised next steps and phases.
  - `workflows` → recommended workflows to run.
  - `reports`   → interpret existing reports.
  - `security`  → security-focused view.
  - `ci`        → CI and quality gate focus.
  - `ui`        → UI/design-system focus.
  - `perf`      → NFR/performance focus.
- `--reports <list>`
  - Comma-separated workflow names whose reports should be prioritised.

## 5.2 Index / registry / reports roots

- `--index` / `--specindex`
  - Override index path; defaults to detection order in KB Section 5.1.
- `--registry-dir <path>`
  - Primary registry root. Default: `.spec/registry`.
- `--registry-roots <paths>`
  - Additional read-only registries (e.g., platform-level).
- `--reports-root <path>`
  - Default: `.spec/reports`.

## 5.3 Multi-repo / workspace

- `--workspace-roots <paths>`
  - Multiple repo roots to scan for specs and `.spec/` folders.
- `--repos-config <path>`
  - Structured multi-repo config; takes precedence over
    `--workspace-roots`.

## 5.4 Knowledge & docs

- `--system-prompt-path <path>`
  - Default: `.smartspec/system_prompt_smartspec.md`.
- `--kb-path <path>`
  - Default: `.smartspec/knowledge_base_smartspec.md`.
- `--docs-root <path>`
  - Default: `.smartspec-docs/workflows`.

## 5.5 Output

- `--output-format <mode>`
  - `human` → narrative answer.
  - `json`  → machine-readable answer only.
  - `mixed` → human + JSON appendix.
- `--lang <code>`
  - `th`, `en`, or `th-en` (bilingual summary).
- `--run-label <string>`
  - Optional label stored in reports (if any are written).

## 5.6 Safety & misc

- `--safety-mode <level>`
- `--strict` → alias for `--safety-mode conservative`.
- `--kilocode` → Kilo-aware behaviour (see Section 6).


# 6. KiloCode Support (Meta-Flag)

- `--kilocode` is always accepted.
- For this workflow, `--kilocode` means:
  - adopt a Kilo-oriented mental model: Orchestrator-led, Ask/Architect;
  - assume Kilo constraints such as ~800-line context per LLM call;
  - prefer high-level reasoning and planning over code synthesis;
  - when suggesting commands for other workflows, include `--kilocode`
    when the environment suggests they will also run under Kilo.

The workflow must not assume Kilo is always available; if Kilo is not
present, `--kilocode` becomes a no-op hint and is mentioned as such in
summaries.


# 7. Canonical Folders & File Placement

This workflow follows KB Section 5:

- Index:
  - prefer `.spec/SPEC_INDEX.json`.
- Registries:
  - `.spec/registry/**` as primary;
  - `--registry-roots` as supplemental, read-only.
- Specs:
  - `specs/<category>/<spec-id>/spec.md` as primary spec locations,
    with adjacent `plan.md`, `tasks.md`, `ui.json`.
- Reports:
  - `.spec/reports/<workflow-name>/` for reports from other workflows.

If key artifacts are missing (no index, no registry, no reports), the copilot
must treat this as a governance gap and call it out explicitly.


# 8. Multi-repo & Multi-registry Rules

- Respect `--repos-config` over `--workspace-roots`.
- Treat `--registry-dir` as authoritative; `--registry-roots` are
  read-only validation sources.
- When detecting duplicate entities across registries (APIs, models,
  components, tokens), highlight them as reuse opportunities and potential
  conflicts; recommend consolidation tasks instead of creating new copies.


# 9. Weakness & Risk Check (Built-in)

Every answer must embed a brief **Weakness & Risk Check**, including:

1. Gaps in specs/plans/tasks for the scope in question.
2. Missing or outdated reports (CI, security, UI, perf, release readiness).
3. Registry gaps (missing tool-version registry, design tokens, component
   registries, patterns, etc.).
4. React/Next.js/RSC/version risks when relevant (per KB Section 18 & 19).
5. Design-system/UI governance issues when relevant (per KB Section 20).
6. Multi-repo/registry conflicts or divergence.

The copilot must:
- call these out clearly; and
- connect them to concrete next steps and recommended workflows.


# 10. Legacy Flags Inventory

Because `/smartspec_project_copilot` is introduced in the 5.6 series, the
initial inventory is:

- Kept as-is:
  - `--project-scope`
  - `--focus`
  - `--reports`
  - `--index` / `--specindex`
  - `--workspace-roots`
  - `--repos-config`
  - `--registry-dir`
  - `--registry-roots`
  - `--reports-root`
  - `--system-prompt-path`
  - `--kb-path`
  - `--docs-root`
  - `--output-format`
  - `--lang`
  - `--run-label`
  - `--safety-mode`
  - `--kilocode`

- Kept as legacy alias:
  - `--strict` → `--safety-mode conservative`.

- New additive flags in 5.6.2:
  - none (this version refines behaviour & guardrails only).

Future versions must only **add** flags or behaviours; no removals.


# 11. Examples (User-facing)

These examples are illustrative; actual invocation syntax depends on the
host tool (Kilo/Roo/Claude/Antigravity/Gemini).

## 11.1 Quick project status (no flags)

User runs:

> `/smartspec_project_copilot`

and asks in natural language:

> ตอนนี้โปรเจกต์พัฒนาถึงขั้นตอนไหนแล้ว
> มี service อะไรเสร็จแล้วบ้าง
> แต่ละ service เสร็จไปประมาณกี่เปอร์เซ็นต์
> และควรทำอะไรต่อก่อน–หลัง

The copilot:
- discovers relevant specs via `SPEC_INDEX`;
- inspects `spec.md`/`plan.md`/`tasks.md` and key reports per service;
- estimates progress % per phase;
- recommends next workflows and actions.

## 11.2 Billing & subscription progress example

User asks (no flags required):

> อยากเช็คความคืบหน้าระบบ billing หน่อย
> ทั้งระบบ billing core และการเรียกเก็บเงินตาม subscription plan
> พัฒนาไปถึงขั้นตอนไหนแล้ว และต้องทำอะไรต่อ

The copilot should:

1. Use `SPEC_INDEX` to find specs with billing/subscription in their names,
   e.g.:
   - `spec-076-billing-system`
   - `spec-090-billing-and-subscription-ui`.
2. Inspect folders:
   - both have `spec.md` and `plan.md`.
   - both are missing `tasks.md`.
3. Conclude (for example):
   - Spec phase ~100%.
   - Planning phase ~100%.
   - Implementation planning ~0%.
4. Respond in plain language with recommended commands, such as:

```bash
/smartspec_generate_tasks specs/feature/spec-076-billing-system
/smartspec_generate_tasks specs/feature/spec-090-billing-and-subscription-ui
```

If the environment suggests Kilo, the copilot should also show the Kilo
variants:

```bash
/smartspec_generate_tasks specs/feature/spec-076-billing-system --kilocode
/smartspec_generate_tasks specs/feature/spec-090-billing-and-subscription-ui --kilocode
```

## 11.3 Interpreting a CI or security report

User pastes a CI/security report and asks:

> จาก report นี้ เราต้องทำอะไรต่อ
> มี blocker อะไรบ้างที่ต้องแก้ก่อนปล่อย production

The copilot should:
- recognise which workflow generated the report (e.g., `ci_quality_gate`,
  `security_evidence_audit`);
- read only the relevant parts of the report in chunks;
- summarise passes/failures and highlight blockers;
- recommend next steps and follow-up workflows.


# 12. Best Practices

- Treat this workflow as the **front door** to SmartSpec for most users.
- Encourage natural-language questions; do not require users to know
  flags or individual workflow names.
- Use chunked reading consistently for large files and reports.
- When recommending commands, prefer canonical paths and include
  `--kilocode` when Kilo is in play.
- Always surface important risks (security, versions, design system)
  together with actionable next steps.


# 13. For the LLM / Stop Conditions

This section is binding for the model that executes this workflow.

## 13.1 General duties

- Always honour NO-WRITE: never propose direct edits to code/spec/tasks.
- Always perform a Weakness & Risk Check before final answers.
- Prefer reading from real artifacts (index, registries, specs, reports,
  workflow docs) instead of guessing.

## 13.2 Kilo & context management

When `--kilocode` is present or the environment suggests Kilo:

1. Assume an **Orchestrator** mental model.
2. Respect a hard limit of ~800 lines of combined input context per call.
3. Use chunked reading for large files:
   - read at most ~300–600 lines per chunk;
   - immediately summarise each chunk into a short note;
   - discard the raw text from the active prompt and reason from notes.
4. Prefer reading only the sections most relevant to the question.
5. If context is still insufficient after reasonable chunking, say so and
   suggest concrete next actions (e.g., run more workflows, create missing
   plans/specs, or narrow the scope).

These principles also apply outside Kilo as good practice.

## 13.3 Progress & "what next" questions

When the user asks about progress of a system/domain/service (e.g., billing,
subscription, authentication, a specific app):

1. Use `SPEC_INDEX` to find related specs and their folders.
2. For each relevant spec folder, inspect the presence of:
   - `spec.md`
   - `plan.md`
   - `tasks.md`
   - relevant reports under `.spec/reports/**`.
3. Approximate progress by phase and, if meaningful, as rough percentages.
4. Explain the reasoning (which files/evidence you used).
5. Recommend specific next steps and ready-to-run commands for other
   workflows, using flags and examples from their `.smartspec/workflows`
   specs and manuals.
6. When appropriate and under Kilo, include `--kilocode` in those example
   commands.

## 13.4 Workflow-introspection

When you recommend `/smartspec_*` workflows:

- Look up their definitions in `.smartspec/workflows/smartspec_*.md`.
- Prefer flags and usage patterns that are explicitly documented there.
- Do not invent new flags or modes unless the user explicitly defines them.
- Do not attempt to "call" those workflows programmatically; only output
  textual recommendations and example commands.

## 13.5 Stop conditions

Stop and return an answer when:

- You have:
  - summarised the relevant status/progress;
  - highlighted the main risks/gaps;
  - proposed concrete next steps and example commands; and
  - included a brief Weakness & Risk Check.

If you cannot confidently answer even after reasonable chunked reading of the
most relevant artifacts, state clearly that the information is insufficient
and suggest what artifacts/workflows the user should create or run next.

