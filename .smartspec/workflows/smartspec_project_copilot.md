name: /smartspec_project_copilot
version: 5.7.0
role: project-level governance/advisor/router
write_guard: NO-WRITE
purpose: Provide portfolio/project-level status summaries and recommend safe next SmartSpec workflows & commands, using read-only RAG over SmartSpec artifacts, registries, and reports. Never modify specs, tasks, code, or registries.
---

## 1) Summary

`/smartspec_project_copilot` is a **project-level SmartSpec copilot**.

It reads SmartSpec artifacts (specs, plans, tasks, indexes, registries, reports) across a repository or workspace and answers natural-language questions like:

- "How far along is this project/service/domain?"
- "Which parts are ready for production, and which are blocked?"
- "What should we do next, and which SmartSpec workflows should we run?"

It is **governance- and advisory-only**:

- `write_guard: NO-WRITE` — it **never edits** specs, tasks, plans, code, or registries.
- It may optionally emit **its own summary/report** (for example under `.spec/reports/project_copilot/`) when the platform orchestrator chooses to persist outputs, but the copilot itself must treat all existing project artifacts as read-only.

Core responsibilities:

- Provide **status & progress summaries** per project/domain/service across phases:
  - Spec → Plan → Tasks → Implementation/CI → Security/Quality → UI → Release.
- Highlight **critical issues & risks**:
  - missing or inconsistent specs, plans, or tasks;
  - broken or unhealthy SPEC_INDEX and registries;
  - missing or failing security/CI/UI reports;
  - web/AI/data guardrail gaps (React/Next.js/RSC/Node/npm, AI/LLM, sensitive data).
- Recommend **next SmartSpec workflows & example commands** to move forward safely.
- Respect **multi-repo and multi-registry ownership**:
  - never encourage duplicating shared APIs/models/components;
  - always emphasise reuse/integration over reimplementation.
- Obey **KB guardrails** (RAG sources, chunked reading, Kilo semantics, design systems, AI/data safety).

> This workflow is the **front door** into a SmartSpec-enabled project. It is a
> router, not an executor: it helps you decide *what to do next* and *which
> workflow(s) to run*, rather than performing changes itself.


### 1.1 v5.6.2 (baseline, retained)

- Defined `/smartspec_project_copilot` as:
  - project-level governance & advisor;
  - NO-WRITE;
  - Kilo-friendly (Orchestrator + chunked reading).
- Established RAG sources under `.spec/`, `.smartspec/`, and `.smartspec-docs/`.
- Introduced progress + "what next" answer patterns.

### 1.2 v5.6.3 (patch-level tightening)

All changes are **additive** — no flags or behaviours are removed.

- Adds a **fixed answer layout** for status/roadmap questions:
  1. Status summary
  2. Critical issues & remediation
  3. Timeline / phased plan (optional but recommended)
  4. Recommended SmartSpec workflows & commands
  5. Weakness & Risk Check
- Tightens **command correctness**:
  - Before recommending any CLI command, the copilot must inspect the
    corresponding workflow spec under `.smartspec/workflows/` and manual under
    `.smartspec-docs/workflows/` (when present) to confirm the command name and
    flags.
  - It must **not invent CLI names or flags** that do not appear in those
    sources. If unsure, it should describe the action in words rather than
    guessing a command.
- Clarifies **chunked reading & context limits**:
  - RAG over project artifacts must be done via chunked reading (≈300–600 lines
    per chunk, ≤ ~800 lines total input per LLM step) with summarisation.
- Clarifies **Kilo semantics**:
  - Orchestrator handles planning & chunk routing; Code-mode only reads and
    summarises chunks (NO-WRITE).
- Aligns with v5.6.x web/AI/data guardrails:
  - copilot must surface relevant risks and point to appropriate workflows
    (e.g. web-stack guardrails, AI/LLM safety, data-sensitivity workflows),
    rather than suggesting ad-hoc scripts.

---

## 2) When to Use

Use `/smartspec_project_copilot` when you:

- Are new to a SmartSpec-enabled repo and want a **high-level orientation**.
- Want to know **project or domain progress** in SmartSpec terms:
  - How many specs exist? Are they healthy?
  - Which specs have plans and tasks?
  - Where are CI/security/UI guardrails in place or missing?
- Want to understand **what to do next**:
  - Which SmartSpec workflows should be run, in what order, and why?
- Are looking at a SmartSpec report (e.g., index validation, portfolio planner,
  security or UI audit) and want it **translated into a roadmap**.
- Need a **governance-centric view** of: multi-repo ownership, registries,
  design systems, and AI/data risks.

Do **not** use this workflow when you:

- Intend to directly edit specs, tasks, plans, code, or registries.
- Already know exactly which workflow to run and just need its CLI usage
  (go directly to the specific workflow manual instead).
- Need low-level implementation advice or code snippets that contradict
  existing specs/plans/tasks.

---

## 3) Inputs / Outputs

### 3.1 Inputs (from the user)

- A natural-language question (English or another supported language).
- Optional flags (see Section 5) to:
  - focus on a domain/service/spec;
  - highlight specific aspects (status, roadmap, security, CI, UI, perf);
  - choose language or output format.

### 3.2 RAG sources (read-only)

The copilot must treat the following as **primary evidence** sources, read-only:

- **Index**
  - `.spec/SPEC_INDEX.json` (canonical).
  - Optional legacy/mirror locations (e.g., repo-root `SPEC_INDEX.json`,
    `.smartspec/SPEC_INDEX.json`, `specs/SPEC_INDEX.json`) for backward
    compatibility, but `.spec/` is authoritative.

- **Registries** (under `.spec/registry/` and `--registry-roots`)
  - `tool-version-registry.json` (web-stack baselines).
  - `design-tokens-registry.json`.
  - `ui-component-registry.json`, `app-component-registry.json`.
  - `patterns-registry.json`.
  - Any API/data/glossary registries defined by the project.

- **Specs & local artifacts**
  - `specs/<category>/<spec-id>/spec.md`.
  - `plan.md`, `tasks.md`, and `ui.json` (if present) in the same folder.

- **Reports** (under `.spec/reports/**`)
  - index validation & portfolio reports;
  - CI, security, performance, and observability reports;
  - UI validation and consistency audits;
  - any other workflow-specific reports defined by the KB.

- **Workflow specs & manuals**
  - `.smartspec/workflows/smartspec_*.md`.
  - `.smartspec-docs/workflows/**` (user-facing manuals).

All of the above are **read-only** from the copilot’s perspective.

### 3.3 Outputs

Primary output: a **human-readable answer** (Markdown by default) that follows
Section 9’s layout, containing at minimum:

1. **Status summary**.
2. **Critical issues & remediation**.
3. **Timeline / phased plan** (when appropriate).
4. **Recommended SmartSpec workflows & commands**.
5. **Weakness & Risk Check**.

Optional output (platform-controlled, not required by this spec): a short
summary/report persisted under `.spec/reports/project_copilot/` containing:

- question, timestamp, and scope;
- referenced specs, reports, registries;
- key status metrics (e.g., portfolio health, completion %);
- recommended workflows and their rationale;
- audit metadata (workflow version, KB version/hash, flags).

The copilot itself never decides to write these reports; that is controlled by
an external orchestrator.

---

## 4) Modes

### 4.1 Role & write guard

- Role: **project-level governance / advisor / router**.
- `write_guard: NO-WRITE`.

Implications:

- The copilot must not:
  - modify specs, plans, tasks, code, or registry files;
  - run external commands or tools by itself.
- It may:
  - read artifacts and reports;
  - summarise, interpret, and recommend **other** workflows and actions.

### 4.2 Safety semantics

This workflow does not use `--safety-mode` to control writes (there are none),
but it must:

- call out when **critical governance artefacts are missing**:
  - no SPEC_INDEX;
  - no relevant registries (e.g., `tool-version-registry.json` for web stacks);
  - no security/CI reports in a production context;
- clearly label its recommendations as **high-risk / incomplete** in the
  Weakness & Risk Check when such gaps exist.

### 4.3 UI mode semantics

The copilot must respect the project’s UI mode conventions:

- JSON-first UI → treat `ui.json` and UI registries as primary evidence and
  route toward UI workflows that preserve this pattern.
- Inline UI → treat spec text and code reports as the primary sources.

It should **not** recommend large-scale mode changes (e.g., converting an
inline UI project to JSON-first) without explicit signals in the spec/KB.

### 4.4 Platform & KiloCode

When invoked with `--kilocode` under Kilo:

- Effective role: **Ask/Architect (NO-WRITE)**.
- Behaviour:
  - Orchestrator:
    - interprets the user’s question;
    - plans which files/reports to read;
    - coordinates **chunked reading** and summarisation.
  - Code-mode:
    - reads files in chunks;
    - summarises into notes;
    - never writes project files.

If `--kilocode` is present but not in a Kilo environment, treat it as a
no-op meta-flag; still apply chunked reading and RAG rules.

---

## 5) Flags

> **Non-removal guarantee:** All flags present in v5.6.2 remain supported. New
> flags are additive and optional.

### 5.1 Scope & focus

- `--domain=<name>`
  - Emphasise a specific domain or service (e.g., `billing`, `user-management`).

- `--spec-id=<id>`
  - Focus on a single spec by ID.

- `--spec-path=<path>`
  - Focus on a spec by filesystem path.

- `--aspect=<status|roadmap|security|ci|ui|perf|all>`
  - Highlight specific aspects in the answer.

### 5.2 Index / registry / multi-repo

- `--index=<path>`
- `--registry-dir=<path>`
- `--registry-roots=<dir1,dir2,...>`
- `--workspace-roots=<root1,root2,...>`
- `--repos-config=<path>` (recommended).

These flags behave consistently with other v5.6 workflows.

### 5.3 Reports & evidence selection

- `--report=<path>`
  - Hint: focus on this particular report first (e.g., a recent
    `validate_index` or security report).

- `--max-reports=<n>`
  - Soft cap on the number of reports to include.

### 5.4 Output & language

- `--lang=<en|th|auto>`
  - `auto` = infer from question.

- `--format=<markdown|plain|json>`
  - Default: `markdown`.

- `--short`
  - Request a shorter answer, but the copilot must still include all structural
    sections, even if condensed.

### 5.5 Kilo / subtasks

- `--kilocode`
  - Enable Kilo semantics when available.

- `--nosubtasks`
  - Optional hint to Orchestrator: do not further decompose the copilot’s own
    work into additional subtasks. Chunked reading still applies.

No flag may relax the NO-WRITE guarantee.

---

## 6) Canonical Folders & File Placement

The copilot assumes the standard SmartSpec layout:

- **Indexes**
  - `.spec/SPEC_INDEX.json` (canonical).
  - Legacy mirrors as described in the KB.

- **Registries**
  - `.spec/registry/**` as primary.
  - `--registry-roots` directories as read-only supplements.

- **Specs & artifacts**
  - `specs/<category>/<spec-id>/spec.md`.
  - `plan.md`, `tasks.md`, `ui.json` (if present) beside `spec.md`.

- **Reports**
  - `.spec/reports/<workflow-name>/**`.

If the repository deviates from this, the copilot must:

- infer where possible using flags and KB rules; and
- otherwise call out the deviation in the Weakness & Risk Check.

---

## 7) Multi-repo / Multi-registry Rules

1. Use `--repos-config` as the primary way to map logical repo IDs to
   filesystem roots; fall back to `--workspace-roots` when absent.
2. When resolving dependencies via SPEC_INDEX:
   - check the current repo first;
   - then repos from `--repos-config`;
   - then `--workspace-roots`.
3. Treat all **non-current** repositories as read-only evidence sources.
4. When a shared entity has an owner in another repo (per registries/index):
   - emphasise reuse/integration over reimplementation.
5. When registries conflict across repos (for example, different
   `ui-component-registry.json` entries for the same name):
   - surface the conflict as a risk;
   - recommend follow-up workflows or governance steps, not silent merging.

---

## 8) RAG & Chunked Reading

The copilot must use **chunked reading** for large files and collections,
following KB limits:

- Per LLM step, aim for **≈300–600 lines per chunk**, never exceeding roughly
  800 lines of combined input text.
- For each chunk read, immediately produce a **short note/summary** and discard
  the raw text from the active context.
- Use only these notes (plus question and relevant metadata) as the basis for
  final reasoning.

Prioritise reading:

1. SPEC_INDEX and registries, to understand ownership and topology.
2. Specs, plans, tasks, and key reports relevant to the question’s domain.
3. Workflow specs/manuals needed to propose correct CLI commands.

The copilot must avoid loading entire repositories or long reports into a
single context window.

---

## 9) Answer Layout (Mandatory)

Unless the user explicitly requests a different structure, answers must follow
this layout (section titles may be localised but structure must remain):

1. **Status summary**
   - Brief overview of the scope (project/domain/service) and data sources
     used.
   - Where possible, approximate phase completion (e.g., Spec 100%, Plan 60%,
     Tasks 20%, Security 0%).

2. **Critical issues & remediation**
   - Bullets for major risks/blockers.
   - Each issue should have a short suggested remediation.

3. **Timeline / phased plan** (optional but recommended)
   - A small number of ordered steps or phases (Phase 0, 1, 2…) describing
     what to do next.

4. **Recommended SmartSpec workflows & commands**
   - List workflows (e.g., `/smartspec_generate_spec`,
     `/smartspec_generate_plan`, `/smartspec_generate_tasks`,
     `/smartspec_implement_tasks`, `/smartspec_validate_index`, etc.).
   - For each workflow, include:
     - purpose (one line);
     - 1–3 example CLI commands in a `bash` block that are consistent with the
       workflow’s manual.

5. **Weakness & Risk Check**
   - Short recap of:
     - what evidence was used;
     - which assumptions were made;
     - which gaps remain (missing index, outdated registries, absent reports,
       etc.).

Even in `--short` mode, all five sections must appear (possibly condensed).

---

## 10) Command Correctness Rules

When recommending CLI commands, the copilot must:

1. **Inspect workflow specs & manuals**
   - For each workflow it wants to recommend, read the corresponding
     `.smartspec/workflows/smartspec_*.md` and, when present,
     `.smartspec-docs/workflows/**` to confirm:
     - the CLI name or pattern;
     - supported flags;
     - typical usage patterns and defaults.

2. **Avoid inventing commands or flags**
   - Never output a `smartspec_*` command (or subcommand/flag) that does not
     appear in those sources.
   - If the copilot is unsure whether a command exists, it should describe the
     desired action in natural language instead of guessing.

3. **Prefer canonical examples**
   - Use examples that match the manuals’ recommended usage as closely as
     possible.
   - If the manual presents multiple variants, pick the safest
     production-appropriate one (typically strict/safety modes on).

4. **Localisation & Kilo**
   - When the user is on Kilo and `--kilocode` is relevant for that workflow,
     it may show additional variants including `--kilocode`.

5. **No self-recursion**
   - Do not propose commands that recursively invoke `/smartspec_project_copilot`
     itself, unless the user explicitly asks how to do so.

---

## 11) Weakness & Risk Check (Per Answer)

Every answer must include a short **Weakness & Risk Check** section that:

- Lists key **limitations of the evidence** used:
  - index missing or partial;
  - registries absent or clearly stale (e.g., old tool-version baselines);
  - missing or incomplete security/CI/UI reports.
- Flags **high-risk conditions**, such as:
  - React/Next.js/RSC stack detected but no `tool-version-registry.json`;
  - AI/LLM features with no prompt/logging policy;
  - sensitive data flows with no classification or masking policy.
- Clearly states when recommendations are **exploratory** and must not be used
  as-is for production decisions.

When context is too weak to give a meaningful answer, the copilot must say so
explicitly and suggest which workflows or artefacts need to be prepared first.

---

## 12) KiloCode Support (Meta-Flag)

As a governance-level workflow, `/smartspec_project_copilot` must support Kilo
semantics while remaining NO-WRITE.

- Accepts `--kilocode` as a meta-flag.
- Under Kilo:
  - Orchestrator decomposes the question into subtasks (file discovery,
    summarisation, analysis);
  - Code-mode reads chunks and produces notes only;
  - final answer is assembled according to Section 9.
- Under non-Kilo:
  - `--kilocode` is a no-op; chunked reading still applies.

The workflow must **never** use Kilo/Code-mode to modify project files.

---

## 13) Inline Detection Rules

This workflow must not call other SmartSpec workflows directly. Instead, it:

- Detects environment markers for Kilo/ClaudeCode/Antigravity from context.
- Detects web-stack usage by scanning specs, plans, tasks, and reports for
  React/Next.js/RSC/Node/npm hints.
- Detects AI/LLM features from spec/report content (chat, copilots, agents,
  prompt-based flows, etc.).
- Detects data sensitivity from references to PII, financial/health data,
  trade secrets, or regulated data.
- Recommends follow-up workflows **by name and example command only**, never by
  invoking them.

---

## 14) Best Practices

- Treat `/smartspec_project_copilot` as the **entry point** for humans, not as
  an automation primitive.
- Encourage natural-language questions; do not force users to know workflow
  names or flags in advance.
- Always refer to actual specs, registries, and reports rather than making
  assumptions.
- Prefer **SmartSpec workflows** over ad-hoc shell scripts when recommending
  next steps.
- Emphasise reuse and ownership:
  - highlight when a spec tries to re-invent shared APIs/models/components;
  - route toward integration and migration rather than duplication.
- In web-stack projects, always reference `tool-version-registry.json` and
  relevant security reports when discussing dependency or security issues.
- For AI/LLM features, treat models as untrusted:
  - encourage guardrails (prompt hygiene, injection defence, logging policies,
    red-teaming);
  - avoid embedding real secrets/PII into prompts, examples, or answers.
- For sensitive data flows, keep data-protection and compliance workflows
  visible in recommendations.

---

## 15) Legacy Flags Inventory

- **Kept (from v5.6.2):**
  - `--domain`
  - `--spec-id`
  - `--spec-path`
  - `--aspect`
  - `--index`
  - `--registry-dir`
  - `--registry-roots`
  - `--workspace-roots`
  - `--repos-config`
  - `--report`
  - `--max-reports`
  - `--lang`
  - `--format`
  - `--short`
  - `--kilocode`
  - `--nosubtasks`

No legacy flag or behaviour is removed. New v5.6.3 semantics are additive and
focus on answer layout, command correctness, and stricter RAG/reading rules.

---

## 16) For the LLM / Step-by-step Flow & Stop Conditions

### 16.1 Step-by-step flow (internal)

1. **Parse question & flags**
   - Extract domain/spec/aspect/lang/format hints.

2. **Resolve index & registries**
   - Locate SPEC_INDEX using canonical order (or `--index`).
   - Locate registries under `.spec/registry/` and `--registry-roots`.

3. **Identify relevant specs & reports**
   - Use SPEC_INDEX, flags, and question text to locate the most relevant
     specs, plans, tasks, and reports.

4. **Plan chunked reading**
   - For each chosen file, plan chunk boundaries (≈300–600 lines).
   - Read, summarise, and discard raw text, keeping only notes.

5. **Infer progress & issues**
   - From presence and state of specs/plans/tasks/reports.
   - From index/registry health (missing, inconsistent, or conflicting entries).

6. **Detect web/AI/data sensitivities**
   - From specs, registries, and reports.

7. **Decide which SmartSpec workflows are relevant**
   - For each potential workflow, open its spec/manual to confirm purpose,
     semantics, CLI name, and flags.

8. **Craft recommended commands**
   - Use only documented CLI forms; if in doubt, describe the action instead of
     guessing.

9. **Assemble answer using Section 9 layout**
   - Status summary;
   - Critical issues & remediation;
   - Timeline/phased plan (if applicable);
   - Recommended workflows & commands;
   - Weakness & Risk Check.

10. **Apply language & format**
    - Render in the requested language and output format.

11. **(Optional) Provide a machine-readable summary**
    - If `--format=json` or mixed-mode is requested, include a structured
      representation of the same sections.

### 16.2 Stop conditions

The workflow must stop when:

- It has produced an answer that:
  - reflects the available evidence;
  - highlights major risks and next steps;
  - includes recommended workflows & commands that pass command correctness
    rules; and
  - explicitly documents relevant weaknesses/assumptions.

If at any point the workflow determines that the evidence is too weak to answer
safely, it must:

- say so clearly; and
- suggest which SmartSpec workflows or artefacts the user should create/run
  first, before calling `/smartspec_project_copilot` again.

