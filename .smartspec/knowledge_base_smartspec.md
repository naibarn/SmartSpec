---
title: SmartSpec Workflow & Manual Guardrails (Kilo/Claude/Antigravity)
version: 5.6+ (security, tool-version registry, design-system aware)
purpose: Non-negotiable governance for SmartSpec workflows/manuals: prevent
         regression, mode errors, cross-repo duplication, folder drift,
         weak UI governance, and missing security/dependency/design-system
         guardrails.
---

# 1) Mission

This knowledge base defines **binding governance** for authoring and upgrading
SmartSpec workflows and manuals across:
- Kilo Code
- Claude Code
- Google Antigravity

Primary failures to prevent:
- removing or weakening legacy flags/behaviors
- breaking backward compatibility
- incorrect platform/mode defaults (esp. verify tasks running in Code mode)
- inconsistent multi-repo/multi-registry semantics
- duplicate shared implementation across repos
- unclear folder/file placement
- shortened manuals that lose essential explanations
- missing or weak security/dependency guardrails for modern web stacks
  (React, Next.js, RSC, Node, npm, etc.)
- design-system drift (e.g., ignoring design tokens, App-level components,
  or agreed UI patterns) especially for MUI/React-based UIs


# 2) Mandatory Quality Gate Before Final Output

Whenever the user requests **workflow/manual creation or improvement** you must
include a brief **Weakness & Risk Check** before finalizing your answer.

You must check for at least:
1. Missing flags or legacy aliases.
2. Ambiguous mode instructions (Kilo/Claude/Antigravity, Orchestrator vs Code).
3. Risks of AI implementation drift (plan/tasks diverging from spec).
4. Risks of cross-repo code/spec duplication.
5. Gaps in folder/file placement rules.
6. UI governance ambiguity (JSON vs inline, missing UI addendum).
7. Missing security / framework / dependency governance for the actual stack
   (React, Next.js, RSC, SSR/Edge, Node, npm ecosystem, etc.).
8. Missing or unclear CI/automation hooks for dependency & security checks
   (lockfiles, `npm audit`, SCA tools, dependency bots) when relevant.
9. Missing design-system governance when the project has design tokens,
   App-level components, or defined layout patterns (e.g., MUI-based systems).

You must **fix the highest-impact gaps** in the workflow before you consider a
workflow upgrade “done”. Manuals are updated **after** the workflow is sound.


# 3) Versioning Discipline

## 3.1 Workflow versioning

Workflows use **Major.Minor.Patch**:
- Examples: `5.6.1`, `5.6.2`.
- Patch = small fixes, restored flags, clarified modes, narrow bugfixes.
- Minor = meaningful capability additions, larger structural changes.

## 3.2 Manual versioning

Manuals use **Major.Minor**:
- Examples: `5.2`, `5.3`, `5.6`.
- Manuals may mention compatible workflow patch ranges.


# 4) Backward Compatibility Contract

## 4.1 Zero feature removal

- Do **not** remove flags/modes/steps/outputs.
- Do **not** weaken legacy behavior.
- Do **not** shorten essential explanations in manuals.

## 4.2 Legacy Flags Inventory requirement

Every upgraded workflow must include a section like:

> **Legacy Flags Inventory**
> - Kept as-is: ...
> - Kept as legacy alias: ...
> - New additive flags: ...

This makes it clear which flags are new vs legacy and guarantees no removal.


# 5) Canonical Folders & File Placement (Mandatory)

The canonical project-owned truth must live under `.spec/` when the layout
supports v5.x+.

## 5.1 Index

Detection order must be stated consistently:
1. `.spec/SPEC_INDEX.json` (canonical)
2. `SPEC_INDEX.json` at repo root (legacy mirror)
3. `.smartspec/SPEC_INDEX.json` (deprecated)
4. `specs/SPEC_INDEX.json` (older layout)

If no index is found, workflows should:
- fall back to local-spec-only behavior, and
- recommend creating/validating the index as part of the plan.

## 5.2 Registries

- Primary registry: `.spec/registry/`
- Typical registry files:
  - `api-registry.json`
  - `data-model-registry.json`
  - `glossary.json`
  - `critical-sections-registry.json`
  - `patterns-registry.json` (optional)
  - `ui-component-registry.json` (optional)
  - `file-ownership-registry.json` (optional)
  - `tool-version-registry.json` (NEW, see Section 19)

## 5.3 Specs and adjacent files

- `specs/<category>/<spec-id>/spec.md` (recommended primary spec path).
- Adjacent in the same folder:
  - `tasks.md`
  - `plan.md`
  - `ui.json` (for JSON-first UI)
  - any other spec-linked artifact.

## 5.4 Reports

- Reports must be project-owned under `.spec/`:
  - `.spec/reports/<workflow-name>/` (e.g.
    `.spec/reports/generate-plan/`, `.spec/reports/ci-quality-gate/`).
- Avoid using `.smartspec/` as default for reports.


# 6) Universal `--kilocode`

## 6.1 Must exist in every workflow

Users will add `--kilocode` by habit. Every workflow must accept and document
it. It may be a no-op outside Kilo but must be recognized.

## 6.2 Meta-flag semantics by role

### Prompt-generating workflows

- Role: generate prompts, not execute code.
- Behavior:
  - `--kilocode` can enable Kilo-optimized prompt formatting.
  - Must remain tool-agnostic and safe.

### Execution workflows

- Role: implement code, edit files, update tasks under ALLOW-WRITE.
- Behavior:
  - Prefer Orchestrator-led execution when available.
  - Obey Orchestrator-per-task rule (Section 9).

### Verification & governance workflows

- Role: validate, audit, analyze; no code changes.
- Behavior:
  - `--kilocode` must not change the workflow’s core role.
  - Effective mode: Ask/Architect.
  - Write guard: NO-WRITE.


# 7) Inline Platform/Mode Detection (No Cross-Workflow Calls)

Tools differ across environments. Workflows must **not** try to call other
SmartSpec workflows directly.

Rules:
- Do not invoke `/smartspec_*` workflows from inside another workflow spec.
- Instead, embed detection logic:
  - read environment/model/mode hints where available;
  - inspect flags (e.g., `--kilocode`) and context text.
- Recommendations to run other workflows are allowed **only as text** (for
  humans/CI to act on), not as tool calls.

If `--kilocode` is requested but Kilo is not present or detectable:
- treat it as a non-breaking no-op;
- stay tool-agnostic;
- mention in summary/report that Kilo was not detected.


# 8) Write-Guard Levels (Mandatory Definitions)

- **NO-WRITE**
  - No code changes.
  - No `spec.md` changes.
  - No `tasks.md` changes (including checkboxes).
  - May write reports/prompts/output files only.

- **READ-ONLY**
  - May generate prompts/spec drafts/plan drafts.
  - Must not modify code/spec/tasks directly.

- **ALLOW-WRITE**
  - May modify code.
  - May update tasks checkboxes under strict rules.

Defaults by role:
- Verification/Governance → NO-WRITE
- Prompt-generating → READ-ONLY
- Execution → ALLOW-WRITE


# 9) Kilo Orchestrator-per-Task Loop (Critical)

Automatic subtask splitting under Kilo is reliable only in Orchestrator mode.

Standard loop:
1. Switch to Orchestrator before each top-level task when subtasks are needed.
2. Ask Orchestrator to decompose tasks with SmartSpec numbering:
   - `T0001 → T0001.1, T0001.2, ...`
3. Confirm dependencies, ownership/reuse, registry alignment, UI/design
   constraints.
4. Switch to Code for implementation.
5. Switch back to Orchestrator for the next top-level task.

Default under Kilo:
- subtasks ON.
Opt-out:
- `--nosubtasks`.


# 10) Multi-Repo / Cross-Repo Verification

## 10.1 Flags

Workflows that interact with index/registry/spec discovery must align on:
- `--workspace-roots`
- `--repos-config`

`--repos-config` takes precedence when both are provided.

## 10.2 Cross-repo anti-duplication

If shared names/entities appear in any loaded registry:
- treat them as existing shared assets;
- prefer reuse/import/calls to owner specs;
- never create parallel shared models, APIs, or policies.

## 10.3 Registry precedence

- Primary registry (`--registry-dir`) is authoritative.
- Supplemental registries (`--registry-roots`) are read-only validation.


# 11) UI Governance (JSON-first vs Inline)

## 11.1 Decision rule

Before generating tasks, plans, or implementation prompts for UI:
- confirm whether the project uses JSON-first UI (`ui.json`) or inline UI.

## 11.2 JSON-first UI

- `ui.json` is the design source-of-truth.
- The system should attempt to generate a **complete, modern, coherent UI**
  via `ui.json` when JSON-first is chosen.
- User-driven manual tweaks to UI JSON are secondary fallback only.

Tasks must include:
- UI JSON creation/maintenance.
- component mapping.
- logic separation (no business logic in UI JSON).
- alignment with `ui-component-registry.json` and design tokens if present.
- security-conscious patterns (no unsafe HTML injection; no secrets or
  sensitive URLs in UI JSON; apply Section 18 guardrails for React/Next/RSC).

## 11.3 Inline UI

- Keep UI/UX requirements in `spec.md`.
- Still define clear modern UI/UX rules for layouts, spacing, and states.
- When inline UI is implemented in React/Next or similar frameworks, **all
  security & dependency guardrails in Section 18 apply**.

## 11.4 Opt-out parameter

- Workflows must provide a parameter to disable UI JSON separation if the user
  chooses to move from JSON-first back to inline UI.


# 12) Manuals: Preserve Structure + Add Examples

When updating manuals:
- preserve the legacy outline and explanatory density;
- never compress away clarity.

Every manual should include examples for:
- single-repo usage;
- multi-repo usage;
- multi-registry usage;
- Kilo usage with safe defaults;
- UI JSON vs inline UI;
- (when relevant) web framework security & dependency usage;
- (when relevant) design-system usage (tokens, App components, layout
  patterns).


# 13) Packaging Rule for Workflow Outputs

When responding with workflows:
- output **one workflow per file**;
- do not bundle into zip;
- use separate canvas/files where available.


# 14) Mandatory Next-Step Suggestions

After providing a workflow answer:
- always recommend at least one **next logical step** (e.g., which workflow to
  upgrade next, or which manual to adjust).
- when helpful, suggest more than one path (governance-first vs
  execution-first).


# 15) Tool-Targeting Symmetry Policy

- `--kilocode` is universal and required.
- Other tool flags (e.g., `--claude-code`, `--antigravity`) are optional.
- If introduced, they must:
  - follow zero-removal and alias rules;
  - not remove tool-agnostic behavior.


# 16) Required Sections for Any New/Upgraded Workflow

Every upgraded workflow must include (in some form):
1. Summary
2. When to Use
3. Inputs/Outputs
4. Modes (role + write_guard + safety-mode)
5. Flags (grouped)
6. Canonical Folders & File Placement
7. Weakness & Risk Check
8. Legacy Flags Inventory
9. KiloCode Support (Meta-Flag)
10. Inline Detection Rules
11. Multi-repo/multi-registry rules (if relevant)
12. UI addendum (if relevant)
13. Security & dependency guardrails (if any web/framework stack in scope)
14. Design-system & component-registry alignment (if design system exists)
15. Best Practices
16. For the LLM / Stop Conditions


# 17) Definition of Done Checklist

A workflow upgrade is complete only if:
- No legacy flags removed or weakened.
- `--kilocode` present and documented.
- Inline detection rules present (no cross-workflow calls).
- Role-based write guard documented.
- Canonical folder rules stated.
- Multi-repo/multi-registry flags aligned.
- UI governance rules clarified.
- Security & framework/dependency guardrails added when relevant
  (React/Next.js/RSC, SSR/Edge, npm ecosystem).
- Design-system governance addressed when relevant (MUI/App components,
  tokens, layout patterns).
- Manual updated with structure preserved and examples expanded.


# 18) Framework & Dependency Security Guardrails (React/Next.js/RSC Focus)

This section defines additional, **non-removable** security and dependency
rules for modern web stacks. It does not replace product security teams or
official advisories; it ensures SmartSpec outputs systematically surface the
right questions and tasks.

## 18.1 Scope

Apply this section whenever:
- Specs/tasks/plans touch React, Next.js, or React-based frameworks.
- The project uses SSR/Edge runtimes, server actions, or React Server
  Components (RSC).
- The dependency tree includes `react-server-dom-*` packages.
- The stack relies on npm/Yarn/pnpm for JS/TS dependencies.

## 18.2 Mandatory detection questions

For any relevant workflow (spec generation, planning, implementation,
verification, security audit, CI quality gate, release readiness, UI
workflows):
- Ask and document:
  - Is React used? Which major range (17/18/19+)?
  - Is Next.js or a similar framework used? Which routing mode (pages/app
    router)? SSR/Edge enabled?
  - Are RSC or server actions used?
  - Any `react-server-dom-*` dependencies?
  - Any known high-severity advisories affecting this stack now?

Answers must influence:
- Weakness & Risk Check;
- security tasks in plans;
- CI/dependency governance recommendations.

## 18.3 RSC / `react-server-dom-*` as high-risk

If the project uses RSC or any `react-server-dom-*` dependency:
- Treat this as **high-risk** (e.g., potential RCE and data exposure).
- Require tasks/checks to:
  - Update RSC-related packages/frameworks to patched versions based on
    official advisories.
  - Review RSC boundaries and data flows:
    - What data moves from server to client?
    - Are untrusted inputs passed into server components/actions?
    - Are secrets/credentials/internal data serialized across the RSC boundary?
  - Confirm no patterns allow arbitrary code execution via serialized payloads
    or dynamic code loading.
- For verification-style workflows:
  - require evidence of audits and patches;
  - require explicit mention of critical CVEs and mitigations.

## 18.4 Non-RSC React/Next.js projects

For React/Next.js without RSC:
- Emphasize risks in:
  - routing & middleware
  - auth/session management
  - SSR/Edge behavior
  - npm supply chain
- Workflows should:
  - add tasks to keep React/Next.js in a supported, patched range;
  - check official advisories for routing/auth/middleware vulnerabilities;
  - highlight secure configuration (auth guards, secure cookies, env config).

## 18.5 Dependency hygiene & CI governance (npm)

For npm/Yarn/pnpm stacks:
- Require/encourage:
  - lockfiles (`package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`).
  - regular dependency audits (`npm audit`, SCA tools such as Snyk, Trivy).
  - automated dependency update tooling (Dependabot, Renovate) in CI.
- CI/release workflows should:
  - fail or gate when critical/high vulnerabilities remain unresolved;
  - allow documented, time-bound exceptions only.

## 18.6 Safer UI/server integration patterns

Avoid patterns that:
- inject untrusted HTML into the DOM (`dangerouslySetInnerHTML`) without
  sanitization;
- embed secrets/tokens/internal URLs in client bundles or UI JSON;
- bypass framework CSRF/XSS/escaping protections.

Prefer patterns that:
- keep sensitive logic/data on the server;
- expose minimal, typed APIs;
- use framework security features (Next.js middleware, secure cookies, env
  vars).

UI-focused workflows must:
- treat AI-generated `ui.json` as security-sensitive;
- encourage review steps to detect unsafe widget/component configurations.

## 18.7 Documentation & evidence

Security/governance workflows (e.g., security evidence audit, CI gate,
release readiness) must request evidence such as:
- dependency audit reports;
- upgrade/patch logs for React/Next/RSC;
- configuration reviews (e.g., `next.config`, RSC usage notes).


## 18.8 CVE-2025-55182 React/Next.js baseline policy (urgent, additive)

For projects using React or Next.js, apply this **urgent, additive** policy for
CVE-2025-55182. It does not remove prior security rules; it adds a hard lower
bound for safe baselines.

- When a workflow/manual touches planning, implementation, or security for a
  React/Next.js project, you MUST:
  - Recommend upgrading to at least the patched versions (or newer patched
    releases) specified by current advisories (e.g., React 19.x minimum
    patched versions, Next 15.x patched releases).
  - Treat React 19.x versions **below the minimum patched level** and Next.js
    versions **below the patched baseline** as potentially unsafe.
  - Phrase guidance so that newer patched versions are always allowed (e.g.,
    "React 19.0.1 or later patched 19.x", "Next 15.2.6 or later patched 15.x",
    depending on the current official guidance).
- CI/release/security workflows should:
  - fail or block when React/ReactDOM/Next.js are below patched baselines for
    projects affected by this CVE (unless a time-bound exception is recorded);
  - request evidence (dependency reports, lockfile diffs, changelogs) to show
    the upgrade occurred.

(In practice, the **exact** version thresholds come from security advisories
and/or `tool-version-registry.json` in Section 19.)


# 19) Tool Version Registry & Upgrade Strategy

This section defines a central **tool version registry** and upgrade strategy
for frameworks/tools (React, ReactDOM, Next.js, Node, etc.). It is additive and
extends registry concepts in Section 5.

## 19.1 Tool version registry file

- Centralized registry path:
  - `.spec/registry/tool-version-registry.json`
- Ownership:
  - platform/architecture/security teams (write)
  - product/feature teams (read-only policy input)
- Purpose:
  - prevent uncontrolled divergence of tool/framework versions;
  - encode minimum patched versions and allowed series per tool;
  - coordinate gradual upgrades across services without breaking
    compatibility.

### 19.1.1 Example structure

```json
{
  "react": {
    "major": 19,
    "series": {
      "19.0.x": { "min_patch": "19.0.1" },
      "19.1.x": { "min_patch": "19.1.2" },
      "19.2.x": { "min_patch": "19.2.1" }
    },
    "allow_new_series": true,
    "disallow_downgrade": true,
    "notes": ["CVE-2025-55182 patched in these series"]
  },
  "react-dom": {
    "major": 19,
    "series": {
      "19.0.x": { "min_patch": "19.0.1" }
    },
    "disallow_downgrade": true
  },
  "next": {
    "major": 15,
    "series": {
      "15.2.x": { "min_patch": "15.2.6" }
    },
    "allow_new_series": true,
    "disallow_downgrade": true,
    "notes": ["Baseline for CVE mitigation"]
  },
  "node": {
    "supported_ranges": ["20.x LTS", "22.x LTS"],
    "disallow_downgrade": true
  }
}
```

> The exact values above are examples. Real thresholds must be maintained by
> platform/security teams and updated as advisories evolve.

## 19.2 Upgrade strategy & compatibility

Workflows/manuals that touch implementation, planning, or security for
services using these tools must:

1. **Read `tool-version-registry.json`** (when present) as the source of truth
   for allowed versions & minimum patches.
2. **Prevent downgrades**:
   - No service may be planned/implemented on a version below `min_patch` for
     its chosen major/minor series.
   - Once a service upgrades to a newer series (e.g., `19.1.x`), plans must
     not recommend rolling back to older series (e.g., `19.0.x`) except as a
     clearly documented emergency rollback.
3. **Allow staggered upgrades**:
   - New services may target newer series (e.g., `19.2.x`) if marked allowed.
   - Existing services may remain on older, still-patched series (e.g.,
     `19.0.x >= 19.0.1`) until they have capacity to upgrade.
   - Plans should make these differences explicit and schedule consolidation
     when too many series are active.
4. **Avoid incompatible fragmentation**:
   - Registries may mark disallowed combinations (e.g., microfrontends sharing
     a runtime must use compatible React/Next series).
   - Planning workflows must:
     - detect incompatible versions in shared contexts;
     - schedule upgrades so shared contexts converge onto compatible ranges.
5. **Integrate with CVE guardrails (Section 18.8)**:
   - For frameworks affected by CVEs, the registry MUST encode minimum patched
     series/versions.
   - Workflows should prefer reading thresholds from the registry instead of
     hardcoding numbers.

## 19.3 Multi-repo behavior

- Platform repo usually owns the canonical
  `.spec/registry/tool-version-registry.json`.
- Other repos read it via `--registry-roots` (read-only).
- Per-repo overrides are discouraged; if they exist they must:
  - be marked experimental/dev-only;
  - never undercut global `min_patch` thresholds.

## 19.4 Workflow expectations

- Spec/plan workflows (`generate_spec`, `generate_plan`, etc.) should:
  - surface relevant tool versions as NFRs;
  - recommend only versions that comply with the registry policy.
- CI/release/security workflows (`ci_quality_gate`, `security_evidence_audit`,
  `release_readiness`, etc.) should:
  - compare `package.json`/lockfiles against registry policy;
  - fail or warn when services fall below `min_patch` or diverge into
    disallowed combinations.

## 19.5 Fallback when tool-version-registry.json is missing

If `.spec/registry/tool-version-registry.json` does not exist:
- Workflows must **not fail silently**. They should:
  - fall back to:
    - security/CVE guardrails from Section 18;
    - official vendor advisories when reasoning about versions;
  - insert explicit plan/tasks to:
    - create/adopt `tool-version-registry.json` owned by platform/security;
    - populate it with `min_patch` thresholds, allowed series, and upgrade
      rules starting from current tools.
- CI/release/security workflows may still:
  - warn or block when tools fall below known safe baselines even without a
    registry;
  - highlight the missing registry as a governance gap.

This ensures short-term security while converging toward a centralized source
of truth for tool versions.


# 20) Design System & UI Pattern Governance (MUI/React & AI Products)

This section defines design-system guardrails, especially for MUI/React-based
UIs and AI-product UIs (e.g., Smart AI Hub). It does not dictate exact visual
style; it ensures consistency and alignment with agreed design systems.

## 20.1 Design tokens registry

Projects with a design system SHOULD maintain design tokens under:
- `.spec/registry/design-tokens-registry.json`

Example contents:
- color tokens (primary/secondary/success/warning/error/info/background/surface)
- spacing scale (e.g., 4/8/12/16/24/32)
- radius scale (e.g., 8/12/16)
- typography (title/body/caption hierarchy)
- shadows and elevations
- motion/animation tokens (duration, easing)

Workflows (spec/plan/UI) should:
- reference design tokens for spacing/radius/colors/shadows instead of
  suggesting ad-hoc values;
- encourage consolidating hard-coded styles into tokens.

## 20.2 UI component & App-level component registry

For MUI/React projects, define:
- `ui-component-registry.json` for base components; and/or
- `app-component-registry.json` for app-level wrappers (e.g., `AppButton`,
  `AppCard`, `AppInput`, `AppTable`, `AppDialog`, `AppEmptyState`,
  `AppErrorState`, `AppSectionHeader`).

Rules:
- App-level components are the **primary API** for new UI surfaces.
- Raw library components (e.g., MUI `Button`, `TextField`) should not be used
  directly in feature UIs unless explicitly allowed.
- UI-related workflows (validation/consistency) should:
  - check that UI specs/ui.json/implementation reference App-level components;
  - flag raw library components used directly in places where app-level
    components exist.

## 20.3 Layout patterns

Common patterns (especially for AI/workflow products) SHOULD be codified in:
- `patterns-registry.json` under `.spec/registry/`

Examples:
- **Workspace layout**:
  - left sidebar: projects/modules
  - top header: context + actions
  - main area: primary content
  - right panel: logs/run history/model settings
- **AI run pages**:
  - run pill/status (queued/running/succeeded/failed)
  - prompt/config panel
  - result viewer as primary focus
  - diff/compare output blocks

Workflows should:
- recognize patterns from the registry when generating UI specs/plans;
- prefer these patterns over ad-hoc layouts for new pages;
- plan remediation tasks when pages diverge significantly from standard
  patterns without good reason.

## 20.4 States: empty/loading/error

Design systems SHOULD define standard components or patterns for:
- loading (e.g., `AppSkeleton`)
- empty state (e.g., `AppEmptyState`)
- error state (e.g., `AppErrorState`)

UI workflows should:
- ensure significant views define these states explicitly in specs/ui.json;
- flag views that lack loading/empty/error definitions.

## 20.5 AI-product look & feel

For AI/Smart-product UIs, design tokens and patterns should typically favor:
- soft surfaces, rounded corners (e.g., radius 12–16)
- thin borders + subtle shadows
- generous spacing and breathing room
- result viewer and core content as the "hero" of the page

The KB does not mandate exact numbers, but workflows should:
- align recommendations with tokens/patterns;
- avoid contradictory styles (e.g., mixing sharp and very rounded corners
  without rationale).

## 20.6 Storybook / documentation

If the project uses Storybook or similar tools:
- spec/plan workflows may add tasks to:
  - document App-level components in Storybook;
  - showcase design tokens and patterns;
  - keep usage examples in sync with specs.

UI-related manuals should:
- explain how Storybook (or similar) ties into the SmartSpec chain;
- provide examples of correct vs incorrect component usage.

---

This knowledge base is binding for all SmartSpec workflow/manual answers.
System prompts should remain **short**, point to this KB for details, and avoid
copying long explanations that belong here or in manuals.


# 23) Project Copilot & Chunked Context Governance

This section defines additional guardrails for project-level copilot
workflows, especially `/smartspec_project_copilot`, and for other
verification/governance workflows that act as "meta-advisors" over
SmartSpec artifacts.

## 23.1 RAG sources for project copilots

Project-level copilots MUST treat the following as primary RAG sources when
answering questions about a project:
- `.spec/SPEC_INDEX.json` (and legacy mirrors, per Section 5.1)
- `.spec/registry/**` (including `tool-version-registry.json`, design tokens,
  component registries, patterns, data-model registries, etc.)
- `.spec/reports/<workflow-name>/**` for prior SmartSpec runs
- `.smartspec/workflows/*.md` (workflow specs: flags, usage, examples)
- `.smartspec-docs/workflows/**` (manuals, examples, best practices)

They must prefer **reading from these sources** over guessing behavior.

## 23.2 Kilo Orchestrator as the default for copilots

When `--kilocode` is present for project-level copilot workflows:
- Effective Kilo mode MUST be **Orchestrator (Ask/Architect)** by default.
- Code mode should only be used as a helper to:
  - read files in small chunks;
  - summarise those chunks;
  - never to modify code/spec/tasks (copilots remain NO-WRITE).
- The Orchestrator is responsible for:
  - understanding user intent from natural language;
  - planning which files/registries/reports to read;
  - orchestrating chunked reads and summaries;
  - combining summaries into final advice.

Copilot workflows must document this behavior explicitly in their Modes and
KiloCode Support sections.

## 23.3 Chunked file reading & 800-line context limit

To respect Kilo (and similar tools) context limits, and avoid fragile
"giant-context" prompts, copilots must:

- Treat ~800 lines as a hard upper bound for any single LLM call
  (combined input and relevant prior summaries).
- Use **chunked reading** for large files:
  - Read at most ~300–600 lines of raw content per chunk.
  - Immediately summarise each chunk into a short note (a few paragraphs or
    bullet points), then discard the raw text from the active prompt.
  - Use these notes as the primary material for later reasoning steps.
- Favour reading only the sections that matter for the current question:
  - e.g., for progress questions, focus on spec/plan/tasks and relevant
    reports for the requested domain/service.
  - Avoid loading unrelated files or entire repos.

Where tools already enforce line limits (e.g., Kilo limiting input/output to
≈800 lines per call), workflows must still apply these chunking rules so that
prompts remain robust and portable across tools.

## 23.4 Progress & "what should I do next" questions

When a user asks questions like:
- "How far along is the billing system?"
- "What is the progress of the subscription billing feature and what should we
   do next?"

Project copilots must:
1. Use `SPEC_INDEX` and registries to identify relevant specs/domains.
2. Inspect the corresponding folders to see which artifacts exist:
   - `spec.md`, `plan.md`, `tasks.md`, and any reports under
     `.spec/reports/<workflow-name>/...`.
3. Interpret progress by phase (e.g., spec/plan/tasks/CI/security/UI/release)
   and provide **rough percentages** with a short justification.
4. Recommend concrete next steps and show **ready-to-run commands** using the
   appropriate workflows, including canonical paths and important flags
   (e.g., `--kilocode` when running on Kilo).

Example pattern (illustrative only):
- Identify that `spec-076-billing-system` and
  `spec-090-billing-and-subscription-ui` are the relevant specs.
- Detect that both have `spec.md` and `plan.md` but no `tasks.md`.
- Explain that spec/plan are ~100% done but implementation planning is ~0%.
- Recommend running:
  - `/smartspec_generate_tasks specs/feature/spec-076-billing-system`
  - `/smartspec_generate_tasks specs/feature/spec-090-billing-and-subscription-ui`
  - and, when under Kilo, the same commands with `--kilocode` appended.

## 23.5 Workflow-introspection behavior

When recommending other workflows, copilots must:
- Read the relevant `.smartspec/workflows/smartspec_*.md` files to understand
  flags, usage, and examples.
- Prefer using the documented flag names and semantics from those specs.
- Avoid guessing undocumented flags or modes.

This introspection is **read-only** and respects the no-cross-workflow-call
rule: copilots may only output recommendations as text, not trigger other
workflows directly.

## 23.6 Fallback when context truly is insufficient

If, after chunked reading of the most relevant artifacts, a copilot still
cannot confidently answer:
- It must **say so explicitly** and describe what is missing
  (e.g., missing `SPEC_INDEX`, missing `plan.md`, no reports run yet).
- It should suggest very concrete next actions, such as:
  - "Run `/smartspec_generate_plan` for these specs first.";
  - "Create `tool-version-registry.json` and re-run the copilot.";
  - "Run `/smartspec_ci_quality_gate` and paste its report here for
     interpretation."

This keeps behaviour honest and encourages improving the project’s
SmartSpec/registry/report coverage over time.

## 24 SmartSpec Workflow Inventory (v5.6.x)

This KB governs the following SmartSpec workflows. Each workflow must obey
the general guardrails in this document (multi-repo, registries, UI mode,
Kilo semantics, web/AI/data safety, etc.).

- `smartspec_check_kilo_mode` – Detect and describe Kilo / non-Kilo context and
  how SmartSpec workflows should behave under KiloCode.

- `smartspec_ci_quality_gate` – CI-oriented quality gate that checks specs,
  tasks, tests, coverage and key reports before allowing merges/releases.

- `smartspec_data_migration_governance` – Plan and govern data migrations
  (domains, ownership, safety, backfill/rollback, audit requirements).

- `smartspec_fix_errors` – Suggest and apply **governed** fixes for issues
  found by index/registry/spec validation workflows (read KB before edits).

- `smartspec_generate_cursor_prompt` – Generate safe, contextual prompts for
  Cursor/Antigravity assistants (prompt hygiene + KB rules apply).

- `smartspec_generate_implement_prompt` – Generate implementation prompts for
  AI agents based on spec/plan/tasks with guardrails from this KB.

- `smartspec_generate_plan` – Create dependency-aware implementation plans
  from one or more specs (v5.6 chain step 3).

- `smartspec_generate_spec` – Turn ideas or reverse-engineered inputs into
  governed SmartSpec `spec.md` files.

- `smartspec_generate_tasks` – Generate `tasks.md` from existing specs/plans
  with centralization, UI mode, web/AI/data safety.

- `smartspec_generate_tests` – Generate test plans/specs based on existing
  specs/plans/tasks and quality gates.

- `smartspec_global_registry_audit` – Audit global registries (API, data,
  UI components, design tokens) for drift, conflicts, and gaps.

- `smartspec_implement_tasks` – Implement code/config based on `tasks.md`
  while respecting ownership, web/AI/data guardrails.

- `smartspec_nfr_perf_planner` – Plan non-functional performance work from
  specs, SLAs and architecture constraints.

- `smartspec_nfr_perf_verifier` – Verify performance/NFR targets via tests,
  benchmarks, and observability evidence.

- `smartspec_observability_runbook_generator` – Generate runbooks and
  observability guides from specs, SLOs and incidents.

- `smartspec_portfolio_planner` – Portfolio-level planner across many specs
  (dependencies, health scores, sequencing).

- `smartspec_project_copilot` – Project-level copilot/router that summarises
  status and recommends next SmartSpec workflows (NO-WRITE).

- `smartspec_refactor_code` – Governed refactoring based on specs and
  registries (ownership, safety, and tests).

- `smartspec_reindex_specs` – Rebuild SPEC_INDEX from the filesystem under
  KB rules (layout, ownership, multi-repo).

- `smartspec_release_readiness` – Evaluate whether a service/domain is ready
  for release based on specs, tests and reports.

- `smartspec_reverse_to_spec` – Reverse-engineer code/behavior into governed
  SmartSpecs (no secrets, no PII in specs).

- `smartspec_security_evidence_audit` – Collect and evaluate security
  evidence (threat models, scans, pen tests, controls).

- `smartspec_spec_lifecycle_manager` – Manage lifecycle of specs (draft,
  active, deprecated) and align downstream artifacts.

- `smartspec_sync_spec_tasks` – Sync changes between spec and tasks, keeping
  them consistent without losing history.

- `smartspec_ui_consistency_audit` – Check UIs against design tokens,
  component registries and patterns.

- `smartspec_ui_validation` – Check that critical flows and UIs have proper
  validation and UX guardrails.

- `smartspec_validate_index` – Validate SPEC_INDEX and registries (missing
  specs, circular deps, ownership, drift).

- `smartspec_verify_tasks_progress` – Verify that implemented code actually
  matches `tasks.md` and associated specs/plans/tests.





This knowledge base is binding for all SmartSpec workflow/manual answers.
System prompts should remain **short**, point to this KB for details, and avoid
copying long explanations that belong here or in manuals.

