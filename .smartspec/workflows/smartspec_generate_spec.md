name: /smartspec_generate_spec
version: 5.6.3
role: spec-generation/authoring
write_guard: ALLOW-WRITE
purpose: Generate or repair SmartSpec `spec.md` files with v5.6
         alignment for high-quality task generation, centralization
         (`.spec`), registry governance, UI mode controls, multi-repo
         safety, KiloCode-compatible orchestration, and
         React/Next.js/Node/npm-aware security, dependency, and
         AI/prompt guardrails.

---

## 1) Summary

`/smartspec_generate_spec` creates new `spec.md` documents or repairs
existing ones while enforcing SmartSpec centralization and
**task-readiness**.

This workflow upgrades the original v5.6 behavior and keeps full
backward compatibility while adding explicit support for:

- Specs that drive robust `tasks.md` generation.
- Explicit ownership and reuse rules aligned with registries.
- Registry-driven governance for shared entities.
- UI mode (JSON-first vs inline) resolution that is consistent with
  downstream TASKS generation.
- Multi-repo projects without duplicated implementations.
- KiloCode orchestration semantics (`--kilocode`).

**New in 5.6.2 (kept in 5.6.3, additive only):**

- When the target spec describes a React/Next.js/Node/npm stack,
  the generated/updated `spec.md` must include security &
  dependency guardrails aligned with the SmartSpec governance KB:
  - detection of React/Next.js/RSC/SSR/Edge usage;
  - RSC and `react-server-dom-*` treated as high risk;
  - alignment with `.spec/registry/tool-version-registry.json`
    (if present) for minimum patched versions and allowed series;
  - CI/dependency hygiene tasks (lockfiles, `npm audit`/SCA,
    dependency bots) as non-functional requirements.
- UI specs must align with design tokens and UI/App-level component
  registries when present, avoiding ad-hoc styles and raw library
  components where App-level components exist.

**New in 5.6.3 (further additive tightening):**

- Explicit AI/prompt safety checks: specs and `ui.json` must not
  contain secrets/PII and must follow AI-safety rules from the KB.
- Multi-repo / multi-registry conflict **severity** guidance:
  critical conflicts are blocking under `strict` safety mode.
- Clarified registry additive update behavior for concurrent edits.
- KiloCode failure/degradation behavior for Orchestrator issues.
- Stronger linkage between UI specs and App-level components/design
  tokens in design systems.

The workflow may **write** files (specs, centralization artifacts,
reports) inside the current repo, subject to safety and `--dry-run`
controls.

---

## 2) When to Use

Use `/smartspec_generate_spec` when you need to:

- Create a **new spec** under `specs/**/` for a feature/service/module.
- Migrate or **repair legacy specs** to align with v5.6 centralization.
- Harmonize naming and ownership across multiple specs or repos.
- Prepare specs that will later drive:
  - `/smartspec_generate_plan`
  - `/smartspec_generate_tasks`
  - `/smartspec_generate_tests`
- Support projects where specs live across **multiple repos**, while
  avoiding duplication and enforcing registry-based ownership.
- Ensure that specs for **React/Next.js/Node/npm**-based services
  include modern security and dependency guardrails (RSC,
  CVE/patch baselines, CI checks, data-boundary rules).
- Ensure AI-assisted specs and UI metadata are safe from
  secret/PII leakage and follow AI-prompt governance.

Do **not** use this workflow to:

- Mass-edit non-spec documentation (use dedicated docs tooling).
- Directly modify `tasks.md` (use `/smartspec_generate_tasks` or
  related workflows).
- Bypass project policies for index/registry ownership.

---

## 3) Inputs / Outputs

### 3.1 Inputs (artifacts, read/write)

**Target spec path (recommended)**

- Example: `specs/core/spec-core-004-rate-limiting/spec.md`
- Determines where the new/updated spec is written.

**Optional context files**

- `plan.md`
- `tasks.md`
- Dependency specs (from SPEC_INDEX dependencies)
- (UI) `ui.json` or other UI spec files (depending on `--ui-mode`)
- Registries under `.spec/registry/`, including:
  - `tool-version-registry.json` (tool/framework versions and
     minimum patched baselines)
  - `design-tokens-registry.json`
  - `ui-component-registry.json`
  - `app-component-registry.json` (if present)
  - other registries defined in the governance KB.

### 3.2 Inputs (flags)

All CLI flags are described in **Section 5)**.

### 3.3 Outputs

Depending on flags and safety mode, this workflow may produce:

- A new or updated `spec.md` under `specs/**/`.
- Centralization companion artifacts (when policy allows):
  - `.spec/SPEC_INDEX.json` (minimal stub only when policy explicitly
    requires it and when safe to create)
  - `.spec/registry/*.json` (recommendations by default; optionally
    additive writes)
- Reports under `.spec/reports/generate-spec/`, including:
  - index path used
  - registry directory used
  - multi-repo roots used
  - safety mode
  - UI mode
  - extracted entities summary
  - ownership notes
  - cross-SPEC conflicts and cross-repo duplication risks
  - UI JSON compliance and design-system alignment notes
  - React/Next.js/Node/npm guardrail notes (if applicable)
  - tool-version-registry usage (if applicable)
  - AI/prompt safety and PII/secret screening notes
  - recommended follow-up workflows

When `--dry-run` is enabled, **no files are written**; all outputs are
printed or simulated only.

---

## 4) Modes

### 4.1 Role & write guard

- Role: **spec-generation/authoring (execution)**
- Write guard: **ALLOW-WRITE**, with the following constraints:
  - Writes are limited to the current repo root and its `.spec/` and
    `specs/` directories, plus the explicit target spec path.
  - Sibling repos discovered via `--workspace-roots` or
    `--repos-config` are treated as **read-only** for this workflow.
  - `--dry-run` forces a read-only simulation of all changes.

### 4.2 Safety mode (strict vs dev)

Controlled by `--safety-mode` (`strict` default) and legacy alias
`--strict`.

- `strict` (default)
  - Requires critical registries when mandated by project policy.
  - Blocks on unresolved cross-SPEC conflicts that affect shared names.
  - Requires explicit ownership clarity for shared entities.
  - Requires anti-duplication notes when cross-repo dependencies exist.
  - For React/Next.js/Node/npm stacks, strongly recommends
    adhering to tool-version-registry baselines and failing
    or clearly marking specs that target unpatched tool versions.
  - Treats certain registry conflicts (e.g., critical API/model
    duplicates) as **blocking**, see Section 11.

- `dev`
  - Allows spec generation even if registries are incomplete.
  - Inserts strong warnings into reports and (optionally) the spec.
  - Recommends follow-up actions to initialize index/registries.
  - For React/Next.js/Node/npm stacks, may allow temporary
    exceptions but must record them in the spec/report as
    explicit TODOs or exception notes (with ownership).

### 4.3 UI mode (JSON-first vs inline)

Controlled by `--ui-mode` and alias `--no-ui-json`.

- `auto` (default)
- `json` – JSON-driven UI specs (`ui.json` as primary UI source)
- `inline` – inline UI documentation only (no required `ui.json`)

UI mode is resolved by precedence in **Section 6.3**.

### 4.4 KiloCode mode

When `--kilocode` is present and the environment is Kilo:

- Effective role: **Ask/Architect**
- Write guard: **ALLOW-WRITE**, but all writes are still governed by
  `--dry-run` and safety-mode rules.
- Must follow **Kilo Orchestrator-per-task rule**:
  - Before each top-level task (each target spec), switch to
    Orchestrator and decompose subtasks.
  - Subtasks typically include:
    - resolve index/registry context
    - resolve multi-repo spec dependencies
    - read existing spec (if any)
    - generate or repair spec sections
    - extract entities and registry recommendations
    - (for web stacks) identify React/Next.js/Node/npm usage and
      apply security/dependency guardrails.
- Default under Kilo: **subtasks ON**, unless `--nosubtasks` is set.

If `--kilocode` is passed but Kilo is not detected, treat it as a
no-op meta-flag and run a single-flow version of the same logic.

If Orchestrator is unavailable or misconfigured:

- In `strict` safety mode:
  - treat as an **infra failure**; prefer to stop with a clear error
    and report entry rather than silently degrading behavior.
- In `dev` safety mode:
  - may degrade to a single-flow behavior while:
    - marking the degradation clearly in the report, and
    - recommending follow-up remediation.

---

## 5) Flags

> **Non-removal guarantee:** No existing flags or semantics from the
> original v5.6 spec are removed. New behavior is strictly additive.

### 5.1 Index / Registry

- `--index=<path>`
  - Path to SPEC_INDEX (optional).
  - Default: auto-detect in canonical order (see **6.1**).

- `--specindex=<path>` (NEW, alias)
  - Exact alias for `--index` (kept for cross-workflow consistency).

- `--registry-dir=<path>`
  - Registry directory.
  - Default: `.spec/registry`.

- `--registry-roots="<path1>;<path2>;..."`
  - Additional registry roots (read-only), e.g. shared or platform
    registries.
  - The workflow:
    - treats `--registry-dir` as primary and writable (subject to
      safety + mode).
    - treats `--registry-roots` as read-only validation sources.

### 5.2 Multi-repo resolution (existing)

- `--workspace-roots=<csv>`
  - Comma-separated list of additional repo roots to search for spec
  files.
  - Used when SPEC_INDEX references specs in sibling repos.

- `--repos-config=<path>`
  - Path to a JSON config describing known repos and aliases.
  - Preferred over `--workspace-roots` when available.
  - Suggested default: `.spec/smartspec.repos.json`.

### 5.3 Generation / Repair (existing)

- `--new`
  - Force new spec generation (even if a spec file exists).

- `--repair-legacy`
  - Read an existing `spec.md` and generate missing centralization
  artifacts as needed.
  - Must not remove or rewrite core legacy content.

- `--repair-additive-meta`
  - Allows adding new, clearly marked metadata blocks when necessary
  for compatibility and task-readiness.
  - Must not change the meaning of existing sections.

### 5.4 Registry update mode (legacy-compatible)

- `--mode=<recommend|additive>`
  - `recommend` (default): registries receive suggestions only.
  - `additive`: append-only updates to registry files.
  - Never delete, rename, or restructure registry entries automatically.
  - In environments where registry files may be updated concurrently
    (e.g., multiple branches or automation), prefer minimal,
    line-level append operations and rely on VCS conflict resolution
    over wholesale rewrites.

### 5.5 Safety / Strictness

- `--safety-mode=<strict|dev>`
  - Default: `strict`.

- `--strict`
  - Legacy boolean alias; if provided, equivalent to
    `--safety-mode=strict`.

- `--dry-run`
  - Print output only; do not write any files.

### 5.6 UI mode

- `--ui-mode=<auto|json|inline>`
  - `auto` (default) – detect from context.
  - `json` – force JSON-driven UI spec.
  - `inline` – force inline UI documentation.

- `--no-ui-json`
  - Alias for `--ui-mode=inline`.

### 5.7 Output & reporting (clarified)

- `--report-dir=<path>`
  - Overrides default `.spec/reports/generate-spec/`.

- `--stdout-summary`
  - Print a short summary (index path, registry dir, entities count,
    warnings) to stdout at the end.

### 5.8 Kilo / subtasks

- `--kilocode`
  - Enable KiloCode semantics and Orchestrator-per-task behavior.

- `--nosubtasks`
  - Disable Orchestrator auto-subtasking under Kilo, preserving a
    single-flow behavior while still respecting `--kilocode` metadata.

---

## 6) Canonical Folders & File Placement

### 6.1 SPEC_INDEX detection order (single source of truth)

Detection order (unchanged, made explicit):

1. `.spec/SPEC_INDEX.json` (canonical)
2. `SPEC_INDEX.json` at repo root (legacy mirror)
3. `.smartspec/SPEC_INDEX.json` (deprecated)
4. `specs/SPEC_INDEX.json` (older layout)

If none are found:

- `strict`: generation may proceed in **local-only mode**, but the
  report MUST include a prominent warning that the project lacks a
  canonical SPEC_INDEX.
- `dev`: generation may proceed with warnings and suggestions to
  initialize an index.

### 6.2 Registries

- Primary registry dir: `.spec/registry/`.
- Additional read-only registries: `--registry-roots`.

Standard registry filenames (if present):

- `api-registry.json`
- `data-model-registry.json`
- `glossary.json`
- `critical-sections-registry.json`
- `patterns-registry.json` (optional)
- `ui-component-registry.json` (optional)
- `app-component-registry.json` (optional, recommended)
- `file-ownership-registry.json` (optional, recommended)
- `tool-version-registry.json` (optional, recommended for
  React/Next.js/Node and other tools)

### 6.3 Spec & UI file locations

- Specs:
  - `specs/<category>/<spec-id>/spec.md` (canonical for generated/updated
    specs).
- UI specs:
  - JSON-first: `.spec/ui/**` or sibling `ui.json` within spec
    directory, as governed by project conventions.
  - Inline: UI sections remain inside `spec.md`.

UI mode resolution precedence (applied when `--ui-mode=auto`):

1. Explicit `--ui-mode` flag (if provided) overrides everything.
2. `--no-ui-json` implies `inline`.
3. If SPEC_INDEX exists and the spec category is `ui`:
   - default to `json` unless the spec folder explicitly opts out
     (e.g., via a local marker).
4. If `ui.json` exists next to the spec path:
   - `json`.
5. If the spec text references UI JSON/Penpot workflow:
   - default to `json`.
6. Otherwise:
   - `inline`.

### 6.4 Reports

- Default: `.spec/reports/generate-spec/`.
- File name pattern: `<timestamp>_<run-label>_generate-spec.{md|json}`.

### 6.5 Write boundaries

This workflow MUST NOT:

- write into sibling repos discovered via `--workspace-roots` or
  `--repos-config`.
- overwrite non-spec documentation unexpectedly.

It MAY write or create:

- `spec.md` under `specs/**/`.
- `.spec/SPEC_INDEX.json` stubs **only when** required by policy and
  when safe.
- `.spec/registry/*.json` (append-only when `--mode=additive`).
- `.spec/reports/generate-spec/**`.

---

## 7) Weakness & Risk Check (Quality Gate)

Before treating `/smartspec_generate_spec v5.6.3` as complete, confirm:

1. **Write safety**
   - `--dry-run` is respected (no writes).
   - Writes stay inside current repo root.

2. **Index/registry correctness**
   - SPEC_INDEX detection order is followed.
   - Registries are never deleted/renamed automatically.

3. **Multi-repo safety**
   - Sibling repos are read-only.
   - Cross-repo dependencies trigger explicit reuse vs implement notes.

4. **UI mode governance**
   - `UI_MODE` is resolved consistently.
   - UI JSON creation (when allowed) is minimal, declarative, and
     **free of business logic**.

5. **Registry extraction behavior**
   - `--mode=recommend` vs `--mode=additive` behavior is preserved.
   - Append-only semantics are used for additive updates and do not
     silently discard concurrent changes.

6. **Legacy compatibility**
   - All existing flags remain supported.
   - No essential behavior from the original spec is removed.

7. **KiloCode support**
   - `--kilocode` and `--nosubtasks` behave as documented.
   - Orchestrator-per-task rule is respected under Kilo.
   - Orchestrator failure/degradation is reported clearly, respecting
     `strict` vs `dev` semantics.

8. **React/Next.js/Node/npm security & dependency guardrails**
   - When the target spec uses these stacks, the generated/updated spec:
     - identifies React/Next.js usage, routing mode (pages/app),
       SSR/Edge, RSC/server actions, and any `react-server-dom-*`
       dependencies;
     - incorporates security and dependency NFRs that align with
       tool-version-registry policy (if present) or current
       advisories from the governance KB;
     - includes tasks for dependency hygiene (lockfiles,
       `npm audit`/SCA, dependency bot configuration) and auditing of
       RSC boundaries where applicable;
     - reflects CVE guardrails (e.g., baselines encoded in the
       tool-version registry) without hardcoding specific version
       numbers in the workflow.

9. **Design-system alignment**
   - When design tokens and UI/App component registries exist, the
     spec:
     - references App-level components instead of raw library
       components where appropriate;
     - avoids hard-coded styles in favor of tokens;
     - captures layout/UX patterns in line with the patterns registry.

10. **AI & prompt safety**
    - Specs and any associated `ui.json`:
      - do not embed secrets, tokens, passwords, private keys, or
        PII directly in text, examples, or metadata;
      - do not copy raw logs/stack traces that might contain secrets;
      - follow the AI/prompt governance rules in the KB for
        injection-resistance and prompt hygiene.
    - If potential secret/PII fields are detected, the run must
      record redaction or follow-up tasks in the report.

11. **Multi-repo / multi-registry conflict severity**
    - Critical entities (e.g., APIs, data models, critical sections)
      that appear with conflicting definitions across registries
      are:
      - treated as **blocking** under `strict` safety mode;
      - surfaced as high-severity warnings under `dev`, with
        explicit ownership and resolution notes.
    - Non-critical naming conflicts are at least reported and not
      silently ignored.

12. **Registry concurrency and integrity**
    - Additive registry writes:
      - do not overwrite unrelated registry content;
      - behave predictably under concurrent edits, relying on VCS or
        other tooling for conflict resolution;
      - never silently drop entries from other changes.

---

## 8) Legacy Flags Inventory

- **Kept as-is (from original 5.6 spec)**:
  - `--index`
  - `--registry-dir`
  - `--workspace-roots`
  - `--repos-config`
  - `--new`
  - `--repair-legacy`
  - `--repair-additive-meta`
  - `--mode`
  - `--safety-mode`
  - `--strict`
  - `--dry-run`
  - `--ui-mode`
  - `--no-ui-json`

- **New aliases / additive flags (introduced in 5.6.1, unchanged in 5.6.3)**:
  - `--specindex` (alias for `--index`)
  - `--registry-roots`
  - `--report-dir`
  - `--stdout-summary`
  - `--kilocode`
  - `--nosubtasks`

---

## 9) KiloCode Support (Meta-Flag)

As a spec-generation workflow:

- Accepts `--kilocode` as a meta-flag.
- Under Kilo:
  - Use Orchestrator to coordinate per-spec tasks.
  - Enforce subtasks **ON by default**, with `--nosubtasks` as opt-out.
  - Keep writes scoped and safety-mode honors (e.g., `strict` vs `dev`,
    `--dry-run`).
  - Ensure React/Next.js/Node/npm guardrail steps are included in the
    decomposition when relevant.
  - Apply AI/prompt safety checks when reading or generating content.
- In non-Kilo environments:
  - Treat `--kilocode` as no-op.

Kilo roles:

- Orchestrator: decides spec order, dependency gathering, registry
  checks, web-stack detection, AI-safety checks.
- Code/Tool mode: performs file reads, structured extraction, and
  write/simulate writes.

If Orchestrator cannot be used:

- `strict`: prefer failing fast with a clear infra error.
- `dev`: allow degraded single-flow behavior with explicit notes.

---

## 10) Inline Detection Rules

The workflow must **not** call other SmartSpec workflows programmatically.
Instead, it:

- Detects environment (Kilo/ClaudeCode/Antigravity) via system context.
- Checks for `--kilocode` flag.
- Detects React/Next.js/Node/npm context by:
  - reading existing spec text (if any) for framework references;
  - reviewing `package.json`/lockfiles (when available);
  - using SPEC_INDEX metadata if it encodes stack information.
- Detects AI-assistance and potential secret/PII exposure by
  scanning specs and `ui.json` for obvious secret patterns.
- Suggests follow-up workflows only in the human-readable report,
  not via tool invocation.

---

## 11) Multi-repo / Multi-registry Rules

1. **Use `--repos-config` when available** to map logical repo IDs to
   physical roots.
2. **Use `--workspace-roots`** as a simpler backup list of sibling
   repositories.
3. When resolving dependency specs from SPEC_INDEX:
   - search current repo first;
   - then repos from `--repos-config`;
   - then `--workspace-roots`.
4. Cross-repo anti-duplication:
   - When a dependency spec is resolved outside the current repo:
     - the generated/updated spec MUST include an explicit
       "Reuse vs. Implement" note for each shared entity, stating:
       - which repo owns the canonical implementation;
       - where the contract/interface is defined;
       - what must be reused/integrated rather than reimplemented.
5. Multi-registry rules:
   - `--registry-dir` is primary.
   - `--registry-roots` are read-only; conflicts should be reported,
     not silently overridden.
   - `tool-version-registry.json` in the primary registry is treated
     as authoritative for tool/framework version policy; supplemental
     registries may be used for validation but not for downgrades.
6. Conflict severity:
   - Critical registry entries (e.g., entries marked as high-importance
     in the KB or registry metadata) that conflict across registries
     must be treated as:
     - blocking in `strict` mode;
     - high-priority warnings with clear ownership and resolution
       tasks in `dev` mode.

---

## 12) UI Addendum (UI JSON & Inline UI)

This workflow must align with JSON-first UI governance, AI usage
patterns, and design system + web-stack guardrails.

### 12.1 JSON-first UI

When `UI_MODE=json`:

- `ui.json` is the **design source of truth** for UI structure.
- `ui.json` SHOULD contain:
  - layout structure;
  - component mapping metadata;
  - design token references;
  - props hints.
- `ui.json` MUST NOT contain business logic, such as:
  - user role checks;
  - complex conditional flows;
  - database or service logic.

If generating a new UI spec and project policy allows creating
`ui.json`:

- Create a minimal, declarative `ui.json` that:
  - uses canonical component names from design system/registry.
  - references design tokens (not hard-coded values).
  - leaves behavior and business logic in `spec.md` or downstream code.

For React/Next.js projects:

- Component names in `ui.json` SHOULD be drawn from
  `ui-component-registry.json` or `app-component-registry.json`
  (e.g., `AppButton`, `AppCard`, etc.) rather than raw library
  components, whenever such App-level wrappers exist.

### 12.2 Inline UI

When `UI_MODE=inline`:

- Do not require `ui.json`.
- Keep UI requirements inside `spec.md`, including:
  - UI/UX goals.
  - Responsive expectations.
  - Design system alignment expectations.
- When a design system exists, prefer describing UI in terms of
  design tokens and App components rather than raw styles.

### 12.3 AI-generated UI JSON metadata (optional but recommended)

When AI is used to generate `ui.json`, it is recommended that
`ui.json` include a `meta` block:

```jsonc
{
  "meta": {
    "source": "ai",
    "generator": "kilo-code-vX",
    "generated_at": "<timestamp>",
    "design_system_version": "<ds-version>",
    "style_preset": "<style-preset-id>",
    "review_status": "unreviewed"
  },
  "screens": [ /* ... */ ]
}
```

`/smartspec_generate_spec` does not enforce this but SHOULD:

- Avoid overwriting existing `meta` blocks.
- Add minimal `meta` only when clearly missing and when project policy
  allows AI-assisted generation.

### 12.4 Web Stack Security & Dependency Guardrails (React/Next.js/RSC/Node/npm)

When the target spec indicates use of React, Next.js, or a related
web stack (including SSR/Edge, RSC/server actions, or
`react-server-dom-*` packages), this workflow MUST:

1. **Detect the stack characteristics**, including:
   - whether React is used and which major/series (when known);
   - whether Next.js (or similar) is used and which routing mode
     (`pages` vs `app` router);
   - whether SSR/Edge runtimes are enabled;
   - whether RSC or server actions are used;
   - whether any `react-server-dom-*` dependencies are present.

2. **Ensure the generated/updated spec includes explicit content**:
   - In **Non-functional Requirements / Security** sections:
     - dependency baselines driven by tool-version-registry when
       available (e.g., "React/Next.js must meet or exceed the
       minimum patched level configured in
       `.spec/registry/tool-version-registry.json`");
     - explicit mention that RSC and `react-server-dom-*` are treated
       as high-risk surfaces, with tasks to review and constrain data
       crossing RSC boundaries;
     - tasks to avoid unsafe patterns (e.g. untrusted HTML injection,
       leaking secrets into client bundles or UI JSON, bypassing
       framework CSRF/XSS protections).
   - In **CI / Release / Security** sections:
     - tasks for maintaining lockfiles (`package-lock.json`,
       `yarn.lock`, `pnpm-lock.yaml`);
     - regular dependency audits via `npm audit` and/or SCA tools;
     - dependency-bot configuration (e.g., Dependabot/Renovate) with
       a clear policy for handling high/critical vulnerabilities;
     - tasks to monitor and apply patches for relevant advisories
       affecting this stack, as captured in the governance KB and
       tool-version registry.

3. **Integrate with `tool-version-registry.json` when present**:
   - Read minimum patched levels and allowed series from
     `.spec/registry/tool-version-registry.json`.
   - Ensure the spec:
     - does not recommend versions below the configured `min_patch`;
     - treats downgrades below the minimum patch level as exceptional
       and requiring human approval with expiry;
     - supports staggered upgrades across services while keeping all
       in a patched range.

4. **Fallback when `tool-version-registry.json` is missing**:
   - Do not fail silently.
   - Add tasks to:
     - create/adopt `.spec/registry/tool-version-registry.json`
       owned by platform/security;
     - populate it with current minimum patched baselines for
       React/ReactDOM/Next/Node as governed by the KB.
   - Reference official advisories and existing security baselines
     in the spec until the registry is available.

### 12.5 Design-System & Component-Registry Alignment

When the project has a design system and UI/App-level component
registries (e.g., MUI-based):

- Treat design tokens and App components as the primary API:
  - Prefer components from `app-component-registry.json`
    (e.g., `AppButton`, `AppCard`, `AppInput`, `AppTable`,
    `AppDialog`, `AppEmptyState`, `AppErrorState`, `AppSectionHeader`)
    over raw library components.
  - Use `design-tokens-registry.json` for colors, spacing, radius,
    typography, shadows, and motion instead of hard-coded values.
  - Reference layout patterns from `patterns-registry.json` where
    available (e.g., standard workspace/AI-run layouts).
- Generated/updated specs SHOULD:
  - list canonical App-level components for each UI surface;
  - define loading/empty/error states via standard components
    (e.g., `AppSkeleton`, `AppEmptyState`, `AppErrorState`);
  - avoid mixing conflicting visual styles (e.g. sharp and very
    rounded corners) without design rationale;
  - include tasks to update Storybook or similar documentation,
    if the project uses it, so that UI spec, implementation, and
    visual examples stay in sync.

### 12.6 AI & Prompt Safety for Specs and UI Metadata

For any AI-assisted content (spec sections, `ui.json`, or other
metadata):

- Do not include secrets, API keys, passwords, access tokens, or PII
  in:
  - spec fields;
  - examples;
  - `ui.json` props or `meta` blocks;
  - logs or error text copied into specs.
- Follow the AI/prompt governance rules in the SmartSpec KB:
  - design prompts to avoid prompt injection leaks;
  - avoid echoing sensitive context back into specs or reports;
  - keep logs and reports free from sensitive payloads.
- If AI-generated text appears to contain sensitive data, the
  workflow should:
  - avoid writing it into files where possible; or
  - clearly mark it for redaction/cleanup with assigned ownership
    in the report.

---

## 13) Best Practices

- Prefer `--safety-mode=strict` for production-critical specs.
- Use `--dry-run` when experimenting with new flags or multi-repo
  configurations.
- Initialize `.spec/SPEC_INDEX.json` and `.spec/registry/` early in
  the project lifecycle.
- For UI-heavy specs:
  - decide early whether JSON-first (`ui.json`) or inline is preferred.
  - keep business logic out of UI JSON.
  - align all naming with UI/App component registries.
- For multi-repo projects:
  - maintain `--repos-config` under `.spec/`.
  - avoid defining the same entity in multiple repos; use registry and
  ownership notes instead.
- For React/Next.js/Node/npm stacks:
  - always reflect tool-version-registry constraints in the
    Non-functional Requirements and CI/Release sections of the spec;
  - treat RSC and `react-server-dom-*` as high-risk; ensure there
    are tasks for data-boundary and serialization reviews;
  - keep React/Next.js/Node in supported, patched ranges as defined
    by the KB/registry, and avoid hardcoding specific version numbers
    in the workflow.
- For AI-assisted specs and UI:
  - treat the AI as an untrusted generator needing human review;
  - avoid copying raw logs / error messages into specs;
  - ensure no secrets/PII are stored in specs, tasks, or UI JSON.

---

## 14) For the LLM / Step-by-step Flow & Stop Conditions

### 14.1 Step-by-step flow

1. **Resolve flags & environment**
   - parse `--index`/`--specindex`, `--registry-dir`, `--registry-roots`,
     `--workspace-roots`, `--repos-config`, `--mode`, `--safety-mode`,
     `--strict`, `--ui-mode`, `--no-ui-json`, `--dry-run`,
     `--kilocode`, `--nosubtasks`, `--report-dir`.

2. **Resolve SPEC_INDEX**
   - detect index path in canonical order.
   - if none found, set local-only mode and note warnings based on
     safety mode.

3. **Resolve registry directories**
   - ensure `.spec/registry/` exists when allowed and not in dry-run.
   - record additional `--registry-roots` as read-only.
   - detect presence of `tool-version-registry.json` and other
     registries (design tokens, UI/App components, etc.).

4. **Resolve multi-repo roots**
   - build a list of repo roots from:
     - current working directory;
     - `--repos-config` (preferred);
     - `--workspace-roots` (fallback).

5. **Identify target spec & context**
   - if target spec path is provided, validate folder structure.
   - if creating a new spec without a path, recommend using
     `/smartspec_reindex_specs` or provide a coherent folder proposal
     in the report.
   - if SPEC_INDEX exists, check for existing spec with same ID/path.

6. **Resolve dependencies**
   - if SPEC_INDEX exists, read dependencies for the target spec.
   - resolve dependency `spec.md` across repo roots.
   - if unresolved and `strict`:
     - mark blocking warnings in report.
   - if unresolved and `dev`:
     - continue with TODO notes.

7. **Determine UI mode**
   - resolve `UI_MODE` following precedence in 6.3.

8. **Read existing spec (if present)**
   - parse existing `spec.md`.
   - preserve all core sections and legacy explanations.
   - in `--repair-legacy`/`--repair-additive-meta`:
     - add missing required sections and metadata blocks additively.

9. **Detect web stack characteristics (if applicable)**
   - look for React/Next.js/Node/npm usage via:
     - spec text (keywords such as "React", "Next.js", "RSC",
       "server actions", "SSR", "Edge runtime");
     - dependencies (e.g., `package.json`, lockfiles when they are
       available); and
     - SPEC_INDEX metadata or registry hints.
   - record whether:
     - React is present, and major/series if known;
     - Next.js is present, along with routing mode and SSR/Edge usage;
     - RSC/server actions / `react-server-dom-*` are used.

10. **Framework-specific security checks (web / React / Next.js)**
    - If the spec uses React/Next.js/Node/npm:
      - ensure there is a clear section (or subsection) in the spec
        for framework & dependency guardrails as described in 12.4;
      - align required versions and patching strategy with policy
        from `tool-version-registry.json` when present;
      - insert tasks for CI/dependency hygiene and RSC boundary
        reviews when missing.
    - In `strict` mode:
      - treat missing or incomplete guardrail sections as blocking
        or requiring explicit TODOs with owners and timelines.

11. **Generate or repair spec content**
    - for new specs:
      - generate all core sections (Overview, Scope, Functional/Non-
        functional requirements, Architecture, Data Models, APIs,
        Security, Observability, Rollout/Migration, Testing Strategy,
        Ownership & Reuse, Dependency Mapping).
    - for repairs:
      - insert/add missing sections and clarifications without
        changing existing meaning.
    - integrate React/Next.js guardrails if Step 9/10 flagged a web
      stack.

12. **Integrate tool-version-registry policy (if present)**
    - read `.spec/registry/tool-version-registry.json` (or from
      `--registry-roots`) for the relevant tools (React, ReactDOM,
      Next.js, Node, etc.).
    - ensure the spec:
      - does not recommend versions below the minimum patched levels;
      - treats downgrades as exceptional with explicit human approval;
      - allows newer patched series consistent with policy.

13. **Align UI with design system (if applicable)**
    - if UI/design tokens/app-component registries exist:
      - ensure UI sections (JSON-first or inline) reference App-level
        components and tokens instead of raw components and hard-coded
        values.
      - confirm loading/empty/error states are specified using
        standard components.
      - keep alignment with patterns registry where applicable.

14. **Apply AI & prompt safety checks**
    - scan generated/updated spec and `ui.json` (if any) for:
      - obvious secret/PII patterns;
      - raw logs or stack traces.
    - if suspicious content is found:
      - avoid including it when possible; otherwise, mark it for
        redaction/cleanup with an owner in the report.

15. **Extract entities & registry recommendations**
    - identify APIs, models, terms, critical sections, patterns, UI
      components.
    - based on `--mode`:
      - `recommend`: output suggestions only in report.
      - `additive`: append missing entries to registries (no deletions or
        renames).

16. **Write outputs**
    - if not `--dry-run`:
      - write/update `spec.md`.
      - optionally create `.spec/SPEC_INDEX.json` stub if policy
        requires.
      - optionally update `.spec/registry/*.json` in additive mode.
      - write report file to `.spec/reports/generate-spec/` (or
        `--report-dir`).
    - if `--dry-run`:
      - simulate writes and include intended changes in
        report/stdout.

17. **Stdout summary**
    - if `--stdout-summary`:
      - print scope, index path, registry dir, count of extracted
        entities, and key warnings, including:
        - whether React/Next.js/Node/npm stacks were detected;
        - whether tool-version-registry and design-system registries
          were used;
        - whether AI/prompt safety checks flagged any issues.

### 14.2 Stop conditions

The workflow MUST stop after:

- finishing all write/simulate-write operations within the current repo.
- emitting the report and any stdout summary.

It MUST NOT:

- write to sibling repos.
- delete or rename registry entries.
- invoke other SmartSpec workflows programmatically.

