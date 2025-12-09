name: /smartspec_generate_tasks
version: 5.6.4
role: tasks-generation/execution
write_guard: ALLOW-WRITE
purpose: Generate high-quality `tasks.md` from one or more existing
         specs with v5.6 centralization, multi-repo/multi-registry
         safety, UI mode alignment, KiloCode-compatible orchestration,
         and web/AI/data-aware guardrails (including React/Next.js/RSC/
         Node/npm, AI/LLM features, and data-sensitivity rules).

---

## 1) Summary

`/smartspec_generate_tasks` generates or updates `tasks.md` for one or
more specs while enforcing SmartSpec centralization rules and providing
LLM-safe, duplication-resistant guidance.

It is the execution-planning step in the v5.6 chain:

1. `/smartspec_generate_spec`
2. `/smartspec_generate_plan`
3. `/smartspec_generate_tasks`
4. `/smartspec_sync_spec_tasks`

Core goals:

- produce tasks that are:
  - consistent with the target spec(s) and plan(s);
  - aligned with SPEC_INDEX dependency graph;
  - aligned with cross-spec registries and cross-repo ownership;
- prevent cross-SPEC drift and duplication:
  - avoid re-inventing shared names and entities;
  - reuse shared patterns instead of duplicating;
  - respect ownership for shared APIs/models/terms/UI components;
- support UI workflows:
  - JSON-first UI (`ui.json`) when appropriate;
  - inline UI mode when explicitly requested or inferred;
- provide fine-grained tasks and subtasks by default:
  - atomic subtasks (`T0001.1` style);
  - explicit dependency graph;
- support multi-repo/multi-registry validation and reuse:
  - cross-repo spec resolution using `--repos-config` and
    `--workspace-roots`;
  - primary vs supplemental registry precedence and conflict surfacing;
- apply modern web and AI/data guardrails:
  - React/Next.js/RSC/Node/npm dependency and security tasks;
  - AI/LLM prompt and logging safety tasks;
  - data-sensitivity and secret/PII propagation guardrails.

> **Execution-focused but governance-aware**
>
> - This workflow **may write** `tasks.md` and reports in the current
>   repo (subject to `--dry-run`/`--nogenerate` and safety modes).
> - It **does not** modify specs, tests, code, or registries.
> - It focuses on tasks, sequencing, and guard rails, not on specific
>   command lines or CI configuration.

**v5.6 baseline (retained):**

- multi-repo and multi-registry flags;
- reuse vs create resource semantics;
- cross-repo anti-duplication and chain ownership hints;
- JSON vs inline UI mode;
- strict vs dev mode via `--mode`.

**v5.6.3 (additive hardening, retained):**

- Added:
  - explicit Modes section (role, write_guard, safety, UI, Kilo);
  - `--safety-mode` and `--strict` as aliases for `--mode`;
  - KiloCode support via `--kilocode` and `--nosubtasks`;
  - React/Next.js/RSC/Node/npm guardrails based on
    `tool-version-registry.json` and web-stack detection;
  - design-system/App-component-aware UI tasks;
  - AI/LLM feature and data-sensitivity aware tasks;
  - Secret/PII propagation guardrails for `tasks.md` and reports;
  - optional `--report-dir` and `--stdout-summary` flags.

**v5.6.4 (patch-level tightening):**

- Added canonical section layout consistent with other v5.6.4 workflows
  (plan/spec):
  - Canonical Folders & File Placement.
  - KiloCode Support (Meta-Flag).
  - Inline Detection Rules.
  - Best Practices.
- Clarified audit metadata expectations for reports.
- Clarified behavior when `tool-version-registry.json` is missing for
  web stacks: tasks must bootstrap/refresh the registry under a
  responsible owner.
- Added explicit `safety_status` header recommendation for `tasks.md`.
- Strengthened guidance on avoiding secret/PII propagation into
  `tasks.md` and reports (with redaction/cleanup tasks).

---

## 2) When to Use

Use `/smartspec_generate_tasks` when:

- you have one or more **existing specs** and (optionally) plans, and
  you want `tasks.md` as an execution-ready breakdown;
- you want tasks aligned with:
  - centralization and registry rules;
  - UI mode (JSON-first vs inline);
  - multi-repo ownership boundaries;
- you are implementing or maintaining:
  - React/Next.js/Node-based services;
  - AI/LLM-driven features or copilots;
  - data flows with sensitive/regulated data;
- you need tasks that are compatible with CI/CD and governance gates.

Do **not** use this workflow to:

- author or repair specs (use `/smartspec_generate_spec`);
- generate plans (use `/smartspec_generate_plan`);
- directly modify registry definitions (use appropriate registry
  workflows or manual governance).

---

## 3) Inputs / Outputs

### 3.1 Inputs (artifacts, read-only)

- **Target spec path** (recommended)
  - e.g. `specs/checkout/spec.md`.

- **SPEC_INDEX** (if present)
  - `.spec/SPEC_INDEX.json` (canonical)
  - `SPEC_INDEX.json` at repo root (legacy mirror)
  - `.smartspec/SPEC_INDEX.json` (deprecated)
  - `specs/SPEC_INDEX.json` (older layout)

- **Registries**
  - primary: `.spec/registry/` by default
  - supplemental: directories from `--registry-roots`
  - includes, when present:
    - `api-registry.json`
    - `data-model-registry.json`
    - `glossary.json`
    - `ui-component-registry.json`
    - `app-component-registry.json`
    - `design-tokens-registry.json`
    - `patterns-registry.json`
    - `tool-version-registry.json` (for frameworks/tools baselines)

- **Optional plan**
  - `plan.md` next to `spec.md` (if exists) as sequencing/context
    input.

- **Optional UI artifacts**
  - `ui.json` or other UI JSON, when `UI_MODE=json`.

- **Multi-repo context**
  - `--workspace-roots` and/or `--repos-config` for resolving specs in
    other repos (read-only).

### 3.2 Inputs (flags)

All CLI flags are described in **Section 5**.

### 3.3 Outputs

- **tasks.md**
  - by default, `tasks.md` next to the target `spec.md`.
  - contains:
    - global implementation rules;
    - top-level tasks (T001, T002, ...);
    - subtasks (T001.1, T001.2, ...) when subtasks are enabled;
    - resource usage metadata (reuse vs create, chain_owner, registry);
    - UI tasks aligned with resolved UI mode;
    - cross-SPEC/cross-repo warnings and tasks;
    - web-stack/AI/data-sensitivity-specific guardrail tasks;
    - version pinning and `safety_status` header.

- **Report** (recommended)
  - default directory: `.spec/reports/generate-tasks/`.
  - includes at least:
    - index path used;
    - registry directories used;
    - workspace roots / repos-config used;
    - safety mode;
    - UI mode;
    - spec path/IDs;
    - detection of web stacks, AI/LLM features, data-sensitivity;
    - whether `tool-version-registry.json` was present & used;
    - summary of reuse/create decisions;
    - any secret/PII flags or redaction tasks;
    - audit metadata:
      - workflow name & version;
      - SmartSpec KB version/hash (if available);
      - key flags (`--safety-mode`/`--mode`, `--kilocode`, `--index`,
        `--registry-dir`);
      - timestamp.

When `--dry-run` or `--nogenerate` is enabled, no files are written;
`tasks.md` and report content are simulated/printed only.

---

## 4) Modes

### 4.1 Role & write guard

- Role: **tasks-generation/execution**
- Write guard: **ALLOW-WRITE**, constrained to:
  - `tasks.md` next to the target `spec.md`;
  - `.spec/reports/generate-tasks/` (or `--report-dir`).
- Specs, registries, and sibling repos are always **read-only**.

### 4.2 Safety mode vs legacy `--mode`

Supported flags:

- `--mode=<strict|dev>`
  - original flag; retained for backward compatibility.
- `--safety-mode=<strict|dev>`
  - alias; preferred in newer workflows.
- `--strict`
  - alias for `--safety-mode=strict`.

Resolution rules:

- If both `--mode` and `--safety-mode` are provided and conflict,
  implementations should treat this as an error and fail fast.
- If only one is provided, it defines the safety mode.
- Default: `strict`.

Semantics:

- `strict`
  - suitable for CI/prod gating;
  - requires critical context (index + registries) when policy expects;
  - enforces cross-repo ownership clarity and avoids unsafe web-stack
    combinations;
  - may treat severe conflicts as blocking, or mark `safety_status`
    as `UNSAFE`.

- `dev`
  - best-effort generation for early-phase or local work;
  - inserts high-visibility warnings into `tasks.md` and reports when
    context is incomplete;
  - may add bootstrap tasks to create/repair missing governance
    artifacts (indexes, registries);
  - generated tasks in `dev` mode should be treated as **non-final**;
  - tasks generated with `dev` must set `safety_status=DEV-ONLY` in
    the header and **must not** be used as-is for production/release
    gating without review and, ideally, strict-mode regeneration.

### 4.3 UI mode

Controlled by:

- `--ui-mode=<auto|json|inline>`
- `--no-ui-json` (alias for `inline`)

`UI_MODE` affects which UI tasks are generated:

- `json` → JSON-first UI (`ui.json` as primary source);
- `inline` → spec-embedded UI requirements (no `ui.json` dependency);
- `auto` → infer from spec, index, and presence of `ui.json`.

### 4.4 KiloCode mode

When called with `--kilocode` under a Kilo environment:

- effective role: **Ask/Architect** for orchestration;
- Orchestrator-per-task rule:
  - before generating tasks for each target spec, delegate to
    Orchestrator to decompose spec into task blocks;
  - unless `--nosubtasks` is set, subtasks are ON by default;
- code/tool mode performs file I/O and parsing.

If `--kilocode` is provided but Kilo is not detected:

- treat as no-op meta-flag and run in normal single-flow mode.

If Orchestrator is unavailable:

- `strict`: fail fast with a clear infra error;
- `dev`: may degrade to single-flow while logging the degradation in
  the report.

---

## 5) Flags

> **Non-removal guarantee:** All flags from v5.6 are preserved.

### 5.1 Index / Registry

- `--index=<path>`
  - Override automatic SPEC_INDEX detection.

- `--specindex=<path>`
  - Alias for `--index`.

- `--registry-dir=<path>`
  - Primary registry directory.
  - Default: `.spec/registry`.

- `--registry-roots=<csv>`
  - Additional registry directories to load read-only.
  - Primary vs supplemental registry precedence:
    - primary (`--registry-dir`) is authoritative;
    - supplemental (`--registry-roots`) are validation-only.

### 5.2 Multi-Repo Resolution

- `--workspace-roots=<csv>`
  - Comma-separated list of additional repo roots.

- `--repos-config=<path>`
  - JSON mapping of repo IDs to filesystem roots.
  - Preferred over `--workspace-roots`.
  - Suggested path: `.spec/smartspec.repos.json`.

### 5.3 Execution & Safety

- `--dry-run`
- `--nogenerate`
  - Both mean: generate tasks to stdout (or report) without writing.

- `--mode=<strict|dev>`
- `--safety-mode=<strict|dev>`
- `--strict`
  - Safety mode control as described in 4.2.

- `--report-dir=<path>`
  - Override default `.spec/reports/generate-tasks/`.

- `--stdout-summary`
  - Emit a short summary at the end (scope, safety mode,
    `safety_status`, key warnings).

### 5.4 Subtask Control

- `--nosubtasks`
  - Disable automatic subtask decomposition.
  - Default: subtasks ON.

### 5.5 UI Mode

- `--ui-mode=<auto|json|inline>`
- `--no-ui-json`
  - alias for `--ui-mode=inline`.

### 5.6 Kilo / subtasks

- `--kilocode`
  - enable Kilo semantics when running under Kilo.

---

## 6) Canonical Folders & File Placement

### 6.1 SPEC_INDEX detection

Detection order:

1. `.spec/SPEC_INDEX.json`
2. `SPEC_INDEX.json` at repo root
3. `.smartspec/SPEC_INDEX.json`
4. `specs/SPEC_INDEX.json`

If `--index`/`--specindex` is provided, it overrides detection.

If no index is found:

- `strict`:
  - generation should add a high-severity or blocking task to
    initialize and validate SPEC_INDEX; `safety_status` should be at
    most `DEV-ONLY` or `UNSAFE` depending on severity;
- `dev`:
  - may proceed with local-only assumptions but must emit a Phase 0
    bootstrap task for SPEC_INDEX initialization.

### 6.2 Registries

- Primary registry directory: `.spec/registry/` or `--registry-dir`.
- Supplemental registries: directories from `--registry-roots`
  (read-only).

If a shared name is defined in any loaded registry:

- tasks must treat it as **reused**, not as a new shared entity to
  create.

When `tool-version-registry.json` exists in the primary registry:

- treat it as the authoritative description of allowed and minimum
  patched tool/framework versions (including React/Next.js/Node).
- tasks must:
  - avoid recommending versions below configured `min_patch`;
  - avoid downgrades across series except as explicit emergency
    rollbacks with justification;
  - surface incompatible combinations as tasks for consolidation.

When a registry that is clearly relevant (for example,
`tool-version-registry.json` in a React/Next.js/Node stack) is missing
or obviously stale:

- tasks must include Phase 0 work to create or refresh that registry
  under the appropriate owner (platform/security) rather than silently
  assuming defaults.

### 6.3 Tasks files

- Default location for single-spec runs:
  - `specs/<category>/<spec-id>/tasks.md`.
- For multi-spec scopes (if supported by the caller):
  - behavior must be documented in report and stdout summary, with
    explicit paths for each `tasks.md` created.

Every generated or updated `tasks.md` should include at least:

- a header block with spec IDs, index path, generated_at,
  `safety_status`, and safety mode.

### 6.4 Reports

- Default directory: `.spec/reports/generate-tasks/`.
- Suggested file naming pattern:
  - `<timestamp>_<spec-id>_generate-tasks.{md|json}`.

The workflow must **not** create new top-level directories outside
`.spec/` or `specs/` by default.

---

## 7) Multi-repo / Multi-registry Rules

1. Use `--repos-config` when available to map logical repo IDs to
   filesystem roots.
2. Use `--workspace-roots` as a simpler fallback list of sibling
   repositories.
3. When resolving dependencies from SPEC_INDEX:
   - search current repo first;
   - then repos from `--repos-config`;
   - then `--workspace-roots`.
4. Dependencies that resolve to other repos are treated as **external
   owners**:
   - tasks must prefer reuse (client/integration) over re-creating
     equivalent functionality.
5. For entities already present in registries (APIs, models, terms,
   components):
   - tasks must not schedule creation of conflicting shared entities;
   - instead, they must schedule integration, adapter, or migration
     work.
6. Conflicts between primary and supplemental registries must be
   surfaced as explicit tasks for reconciliation, preferring the
   platform/global registry as a starting point.

---

## 8) Identify Target Spec(s) & Dependencies

- Validate target `spec.md` path.
- Resolve spec ID via SPEC_INDEX when available.
- Read dependency info from:
  - SPEC_INDEX;
  - spec content;
  - plan (if present).
- Label dependencies as critical or non-critical based on registries
  and spec metadata.

Strict vs dev:

- `strict`:
  - unresolved **critical** dependencies should produce blocking or
    high-severity tasks (e.g., `T000 — Resolve missing dependency
    spec`) and avoid create-type tasks for those entities.

- `dev`:
  - may proceed with explicit warning and bootstrap tasks.

---

## 9) Read Spec (Read-only) & Ownership Gate

Parse spec (and plan, if present) for:

- scope, functional and non-functional requirements;
- APIs, models, domain terms;
- UI surfaces and flows;
- integrations and external dependencies;
- web stack hints (React/Next.js/Node/RSC/etc.);
- AI/LLM feature hints (chat, copilots, agents, etc.);
- data-sensitivity hints (PII, financial/health, regulated data);
- ownership & reuse signals (e.g., "reuses shared API X").

Use registries to classify each entity as:

- owned by this spec;
- owned by another spec (same repo);
- owned by another spec (other repo);
- unknown.

Apply cross-repo anti-duplication:

- if owner spec in another repo is resolved:
  - generate `reuse` tasks with explicit integration boundaries;
  - do not generate parallel `create` tasks for equivalent logic.

---

## 10) Task Structure & Resource Usage Metadata

### 10.1 Top-level tasks & subtasks

Preserve and extend categories such as:

1. Setup & Baseline
2. Core Implementation
3. Cross-SPEC Shared Work
4. Integrations
5. Testing
6. Observability & Ops
7. Security
8. UI & UX
9. AI/LLM & Data-Sensitivity (when applicable)

Top-level IDs: `T001`, `T002`, …

Subtasks:

- default: ON, generating atomic subtasks (`T001.1`, `T001.2`, …) with
  explicit dependencies where ordering matters;
- `--nosubtasks`: generate only top-level tasks without subtask IDs.

### 10.2 Resource usage metadata

Each task/subtask should include a metadata block, for example:

```yaml
Resource usage:
  type: reuse | create
  chain_owner:
    api_owner: <spec-id|null>
    model_owner: <spec-id|null>
    pattern_owner: <spec-id|null>
    terminology_owner: <spec-id|null>
  registry:
    api: <entry-id|null>
    model: <entry-id|null>
    ui_component: <entry-id|null>
  files:
    - <path-or-glob>
  justification: <short description>
  repo_context:
    owner_repo: <id|unknown>
    consumer_repo: <id|current>
```

Rules:

- `type: reuse`
  - must reference canonical owner;
  - if `owner_repo != consumer_repo`, specify import/integration
    boundaries and protocols.

- `type: create`
  - must justify creation (e.g., "no registry entry found");
  - must confirm entity is not present in any loaded registry.

---

## 11) UI Addendum (Mode-Dependent)

Apply when the spec is UI-related or references UI surfaces.

### 11.1 JSON-first UI (`UI_MODE=json`)

Tasks should include:

- generate or validate `ui.json` for the scope:
  - ensure it uses canonical component names from
    `ui-component-registry.json` / `app-component-registry.json`;
  - ensure it references design tokens instead of hard-coded styles;
- map UI nodes to components:
  - prefer App-level components (e.g., `AppButton`, `AppCard`,
    `AppInput`, `AppDialog`, `AppEmptyState`, `AppErrorState`);
- separation of concerns:
  - keep business logic out of `ui.json`;
  - domain rules live in spec and code, not in layout metadata;
- consistency & UX:
  - use existing layout patterns from `patterns-registry.json`;
  - handle loading/empty/error states via standard components.

### 11.2 Inline UI (`UI_MODE=inline`)

Tasks should include:

- implement modern responsive layouts per spec;
- reuse shared components and patterns rather than bespoke UI;
- keep layout/state and domain logic separated;
- adopt design tokens and App-level components even without `ui.json`.

### 11.3 UI Governance & AI-generated UI JSON

Where AI-generated `ui.json` or UI governance reports exist, tasks
should:

- review UI surfaces with `ui_spec_origin=AI` &
  `ui_spec_review_status=UNREVIEWED`;
- remediate where `ui_json_quality_status` is WEAK or BROKEN;
- schedule UI consistency/validation workflows (by name) where needed;
- never assume AI-generated UI JSON is production-ready without human
  review.

---

## 12) Web Stack Security & Dependency Guardrails

When the spec (or registries) indicate React/Next.js/Node/RSC usage:

1. **Tool-version-registry integration**
   - read `tool-version-registry.json` when present;
   - generate tasks to:
     - keep dependencies at or above `min_patch` for each allowed
       series;
     - avoid disallowed downgrade paths;
     - converge multiple services on compatible series where possible.

2. **Missing or stale tool-version registry**
   - if web stack is present but `tool-version-registry.json` is
     missing or clearly obsolete, generate Phase 0 tasks to:
     - create or refresh the registry under platform/security;
     - populate minimum patched baselines according to policy.

3. **RSC and `react-server-dom-*` surfaces**
   - tasks to:
     - review data crossing RSC boundaries;
     - validate serialization and streaming safety;
     - ensure access control and auth checks at server actions.

4. **SSR/Edge runtimes**
   - tasks to:
     - validate environment variables and secrets are not leaked;
     - harden headers and caching behavior;
     - confirm that sensitive data does not flow into client bundles.

5. **CI/release guardrails**
   - tasks to:
     - maintain lockfiles (`package-lock.json`, `yarn.lock`,
       `pnpm-lock.yaml`);
     - run dependency scanners (`npm audit`/SCA);
     - configure dependency bots (Dependabot/Renovate/etc.);
     - compare runtime tool versions to registry baselines in CI.

---

## 13) AI & Data-Sensitivity Guardrails

When the spec includes AI/LLM features:

- tasks must:
  - define prompt and context construction rules (including safe data);
  - implement prompt injection defenses and instruction hierarchy;
  - define logging and trace policies that exclude secrets/PII;
  - run red-team style tests for adversarial prompts and edge cases.

When the spec handles sensitive data:

- tasks must:
  - classify data and apply anonymization/masking where appropriate;
  - ensure secrets/PII do not appear in:
    - `tasks.md` examples;
    - logs or stack traces copied into tasks;
    - any persistently stored prompt templates;
  - integrate external data-protection tooling (DLP, secret scanners)
    where required by policy.

---

## 14) Global Guard Rails in `tasks.md`

Generated `tasks.md` should start with an implementation rules block,
for example:

```markdown
> IMPLEMENTATION RULES
> - Load and read all referenced specs, plans, and registries before coding.
> - NEVER reimplement shared APIs, models, or UI components that have existing owners.
> - Cross-repo owners MUST be reused through defined import/integration boundaries.
> - Follow Resource usage metadata strictly (reuse vs create).
> - Respect resolved UI mode (json/inline) and design-system guidance.
> - If any referenced SPEC or PLAN is updated after generated_at, STOP and regenerate tasks.md.
> - If contradictions between spec.md/plan.md and tasks.md are found, STOP and reconcile.
> - tasks.md IS the primary execution plan, but spec.md remains the source-of-truth for requirements.
> - Do NOT place secrets, access tokens, passwords, or PII in tasks.md, examples, or logs.
```

---

## 15) Version Pinning & Safety Header

Include a version pinning header at the top of `tasks.md`, such as:

```yaml
Tasks metadata:
  spec_id: <spec-id>
  spec_version: <front-matter | git-hash | UNKNOWN>
  index_path: <SPEC_INDEX path | UNKNOWN>
  generated_at: <timestamp>
  generated_by: /smartspec_generate_tasks v5.6.4
  safety_mode: strict | dev
  safety_status: SAFE | UNSAFE | DEV-ONLY
```

Rules:

- `safety_status=SAFE` only when strict mode finds no blocking issues.
- `safety_status=UNSAFE` when strict mode finds unresolved conflicts
  or missing critical context.
- `safety_status=DEV-ONLY` for dev mode runs or exploratory tasks.

Tasks should include a rule that if any referenced spec or plan updates
after `generated_at`, `tasks.md` must be regenerated.

---

## 16) Reconciliation Task

All generated `tasks.md` should include a reconciliation task, for
example:

```markdown
T999 — SPEC/PLAN/TASK Alignment Review
- Verify there are no contradictions between spec.md, plan.md (if present), and tasks.md.
- Confirm cross-repo reuse directives remain consistent.
- Confirm web-stack, AI, and data-sensitivity guardrails are implemented as planned.
- Update spec or plan first if misalignment is found, then regenerate tasks.md.
```

---

## 17) Weakness & Risk Check (Quality Gate)

Before treating `/smartspec_generate_tasks v5.6.4` as complete, verify:

1. **Write safety**
   - `--dry-run`/`--nogenerate` prevent all writes;
   - writes are limited to `tasks.md` and reports under `.spec/`.

2. **Index & registry correctness**
   - SPEC_INDEX detection order is followed;
   - primary vs supplemental registries are respected;
   - shared entities are reused, not duplicated.

3. **Multi-repo safety**
   - sibling repos are read-only;
   - external owners are modeled as `reuse` tasks, not duplicated
     implementations.

4. **UI governance**
   - UI mode is consistent with other workflows;
   - JSON-first tasks use design tokens and App-level components;
   - no business logic is encoded in `ui.json` tasks.

5. **Safety-mode behavior**
   - strict/dev semantics match expectations;
   - conflicts and missing context are surfaced via `safety_status` and
     explicit tasks.

6. **Web-stack guardrails**
   - React/Next.js/RSC/Node/npm tasks respect registry baselines;
   - RSC/SSR/Edge and `react-server-dom-*` have explicit guard tasks;
   - missing `tool-version-registry.json` leads to registry bootstrap
     tasks.

7. **Design-system alignment**
   - App-level components and design tokens are preferred over raw
     components and ad-hoc styles.

8. **AI & data-sensitivity**
   - AI/LLM features yield prompt/logging/injection/red-team tasks;
   - sensitive data yields classification/masking and DLP/secret
     scanner integration tasks.

9. **Secret/PII propagation**
   - generation avoids inserting secrets/PII/logs;
   - suspicious content is flagged in the report for human redaction.

10. **KiloCode support**
    - `--kilocode` and `--nosubtasks` behave as documented;
    - Orchestrator-per-task rule is honored under Kilo.

---

## 18) Legacy Flags Inventory

- **Kept (legacy behavior):**
  - `--index`
  - `--specindex`
  - `--registry-dir`
  - `--registry-roots`
  - `--workspace-roots`
  - `--repos-config`
  - `--dry-run`
  - `--nogenerate`
  - `--nosubtasks`
  - `--mode`
  - `--ui-mode`
  - `--no-ui-json`

- **New additive flags (v5.6.x):**
  - `--safety-mode`
  - `--strict`
  - `--report-dir`
  - `--stdout-summary`
  - `--kilocode`

No legacy flag is removed; `--mode` remains supported and mapped to
`safety-mode` semantics.

---

## 19) KiloCode Support (Meta-Flag)

As a tasks-generation workflow, `/smartspec_generate_tasks` must
support KiloCode semantics without depending on them.

- Accepts `--kilocode` as a meta-flag.
- Under Kilo:
  - Orchestrator coordinates per-spec tasks-generation steps;
  - Code/tool mode reads specs, plans, indexes, registries, and writes
    `tasks.md` and reports;
  - write guard and safety-mode rules apply as in non-Kilo mode.
- Under non-Kilo:
  - `--kilocode` is treated as a no-op.

### 19.1 Orchestrator loop (Kilo + subtasks)

For each spec (or group of specs) in scope, in dependency order:

1. Resolve index/registry context.
2. Resolve multi-repo dependencies.
3. Read spec(s) and optional plan(s).
4. Detect web stacks, AI/LLM features, and data-sensitivity markers.
5. Build a high-level task graph.
6. Decompose into tasks and subtasks (unless `--nosubtasks`).
7. Attach resource usage metadata and ownership info.
8. Apply UI, web-stack, AI, and data-sensitivity guardrails.
9. Compute `safety_status` for the scope and propagate it into headers
   and reports.

Subtasks are ON by default; `--nosubtasks` can disable them.

---

## 20) Inline Detection Rules

The workflow must not call other SmartSpec workflows programmatically.
Instead, it:

- detects environment markers for Kilo/ClaudeCode/Antigravity from the
  system context;
- checks for `--kilocode` in arguments;
- detects web stack usage by:
  - inspecting specs and optional dependency files (when available)
    for references to React, Next.js, Node, RSC/server actions,
    `react-server-dom-*`, SSR/Edge runtimes;
  - considering hints in SPEC_INDEX or registries;
- detects AI/LLM features by:
  - scanning specs and plans for AI/LLM descriptions (chat, copilots,
    agents, prompt-based flows, etc.);
- detects data sensitivity by:
  - scanning specs for references to PII, financial/health data,
    trade secrets, or regulated zones;
- only **recommends** follow-up workflows (for example,
  `/smartspec_generate_plan`, `/smartspec_release_readiness`,
  `/smartspec_ui_validation`, `/smartspec_ui_consistency_audit`) in
  human-readable text;
- never invokes other workflows directly.

---

## 21) Best Practices

- For CI/prod-bound work, use `--safety-mode=strict` or
  `--mode=strict`.
- Use `--dry-run` or `--nogenerate` the first time in a repo to verify
  index/registry resolution.
- Keep `.spec/SPEC_INDEX.json` and `.spec/registry/` up to date; add
  tasks to repair them when they lag behind reality.
- Prefer `--repos-config` under `.spec/` for multi-repo setups.
- Decide on UI mode (JSON-first vs inline) early per spec and keep it
  consistent across related specs.
- Treat `tasks.md` as an execution contract:
  - always include header with `safety_status`;
  - ensure T999 reconciliation is reviewed before major work.
- For web stacks (React/Next.js/Node/RSC):
  - keep dependencies aligned with `tool-version-registry.json`;
  - always include tasks for RSC/SSR/Edge hardening.
- For AI/LLM features:
  - treat the model as untrusted; plan guardrails and red-team-style
    testing;
  - never include real user data, secrets, or PII as examples in
    `tasks.md`.
- For sensitive or regulated data:
  - assume external protection tooling (DLP, secret scanners, SCA)
    complements this workflow;
  - make those dependencies explicit in tasks.

---

## 22) For the LLM / Step-by-step Flow & Stop Conditions

### 22.1 Step-by-step flow

1. Parse flags and environment:
   - `--index`/`--specindex`, `--registry-dir`, `--registry-roots`,
     `--workspace-roots`, `--repos-config`, `--mode`, `--safety-mode`,
     `--strict`, `--dry-run`, `--nogenerate`, `--ui-mode`,
     `--no-ui-json`, `--kilocode`, `--nosubtasks`, `--report-dir`,
     `--stdout-summary`.

2. Resolve SPEC_INDEX following canonical order; set local-spec-only
   mode and bootstrap tasks if missing.

3. Resolve registries and detect presence/absence of
   `tool-version-registry.json` and design-system registries.

4. Resolve multi-repo roots via `--repos-config` and
   `--workspace-roots`.

5. Identify target spec(s) and read each `spec.md` (and `plan.md`, if
   available).

6. Detect:
   - web stack usage (React/Next.js/Node/RSC/etc.);
   - AI/LLM features;
   - data-sensitivity.

7. Use SPEC_INDEX and registries to resolve dependencies and ownership;
   classify entities as reuse/create.

8. Build a category-structured task outline and generate top-level
   tasks.

9. Unless `--nosubtasks`, decompose into subtasks with explicit
   ordering and dependency metadata.

10. Attach resource usage metadata to each task/subtask.

11. Resolve `UI_MODE` and apply the UI addendum to generate appropriate
    UI tasks.

12. Apply web-stack guardrail tasks, including registry baselines,
    RSC/SSR/Edge hardening, and CI/dependency hygiene.

13. Apply AI & data-sensitivity tasks where applicable.

14. Insert global implementation rules and version pinning header,
    including `safety_status`.

15. Insert reconciliation task T999.

16. Perform a best-effort scan of generated text for obvious
    secret/PII/log content; avoid adding or mark for redaction.

17. If not `--dry-run`/`--nogenerate`, write `tasks.md` and report to
    canonical locations; otherwise simulate and print.

18. If `--stdout-summary` is set, print a summary of scope, safety
    mode, `safety_status`, index/registry paths, and key warnings.

### 22.2 Stop conditions

The workflow must stop after:

- completing write/simulated-write operations in the current repo; and
- emitting the report and optional stdout summary.

It must **not**:

- modify `spec.md`, `plan.md`, or registry definitions;
- write into sibling repos;
- invoke other SmartSpec workflows programmatically.

