manual_name: /smartspec_generate_spec Manual (EN)
manual_version: 5.6
compatible_workflow: /smartspec_generate_spec
compatible_workflow_versions: 5.6.1 – 5.6.x
role: user/operator manual (architect, backend/frontend lead, platform, spec owner)
---

# /smartspec_generate_spec Manual (v5.6, English)

## 1. Overview

This manual describes how to use the workflow:

> `/smartspec_generate_spec v5.6.x` (e.g., v5.6.1)

The workflow is an **execution workflow for creating/repairing `spec.md` files**, with a focus on:

- shaping specs so they work well with the v5.6 SmartSpec chain:
  - `/smartspec_generate_plan`
  - `/smartspec_generate_tasks`
  - `/smartspec_generate_tests`
  - `/smartspec_release_readiness`
- enforcing **centralization** via `.spec/`, `SPEC_INDEX`, and registries
- handling **multi-repo / multi-registry** projects safely, avoiding duplicate entities
- supporting **UI modes** for both JSON-first UI (`ui.json`) and inline UI inside `spec.md`
- working cleanly with **KiloCode** (`--kilocode`) using the Orchestrator-per-task rule
- preparing specs for **modern stacks and safety constraints**:
  - React/Next.js/RSC/Node/npm baselines (via `tool-version-registry.json`)
  - AI/LLM feature safety (prompt, logging, injection resistance)
  - data-sensitivity classification and protection

> **Important:**
> - This workflow has `write_guard: ALLOW-WRITE`, but writes are constrained to the **current repo only**.
> - It always respects `--dry-run`; when enabled, no files are written.
> - No existing flags or behaviors are removed; all additions are **strictly additive**.

### 1.1 When to use it

Use `/smartspec_generate_spec` when you want to:

- create a **new spec** under `specs/**/` that follows the SmartSpec standard
- **repair / upgrade legacy specs** to v5.6 alignment (without changing their original meaning)
- add missing metadata/sections required by downstream workflows
  (ownership, dependencies, migration, UI mode, **framework/AI/data-safety sections**, etc.)
- prepare specs so they can drive the chain:
  - spec → plan → tasks → tests → release readiness
- support cross-repo environments using SPEC_INDEX and registries without duplicating entities

Do **not** use this workflow to:

- mass-edit non-spec docs (e.g., README, ADRs)
- edit `tasks.md` directly (use `/smartspec_generate_tasks` and related workflows instead)

### 1.2 Problems this workflow solves

Common pain points without this workflow:

- specs are written in inconsistent formats, making task generation poor or incomplete
- no SPEC_INDEX / registries → unclear ownership and duplicate entities across repos
- UI specs are unclear: JSON-first or inline text? → confusion for both humans and AI
- multi-repo setups: different teams independently define the same API/model/glossary terms
- modern stacks (React/Next/AI) lack clearly documented **baseline versions, safety requirements, and data handling**

`/smartspec_generate_spec` gives you specs that are **ready to plug into the rest of the SmartSpec chain** safely.

---

## 2. What’s New in v5.6

### 2.1 Alignment with the v5.6 SmartSpec chain

Specs generated/updated by this workflow are shaped to work well with:

- spec → plan → tasks → tests → release readiness

Key sections are emphasized so downstream workflows can operate effectively, e.g.:

- Functional / Non-functional Requirements
- Ownership & Reuse
- Dependencies & Integrations
- Data Models / APIs
- Security / Observability / Rollout / Migration

### 2.2 Structured multi-repo / multi-registry support

- Supports `--workspace-roots` and `--repos-config` to resolve specs across multiple repos safely.
- Uses `--registry-dir` (primary) plus `--registry-roots` (read-only) for shared/platform registries.
- Enforces explicit **Reuse vs Implement** notes when your spec touches entities owned by other repos.

### 2.3 UI mode governance (JSON-first vs inline)

- Supports `--ui-mode=auto|json|inline` plus `--no-ui-json` alias.
- Has a clear precedence for deciding whether a spec should:
  - be JSON-first (with `ui.json` as a primary UI spec), or
  - rely on inline UI documentation in `spec.md`.
- Aligns with JSON-first UI governance from other UI-related workflows.

### 2.4 KiloCode support and Orchestrator-per-task

- Supports `--kilocode` and `--nosubtasks` flags.
- In Kilo environments, uses the Orchestrator to handle each spec as a top-level task with subtasks like:
  - resolving index/registry context
  - resolving multi-repo dependencies
  - reading legacy spec content
  - generating/repairing sections
  - extracting entities and registry recommendations
- This improves safety and structure when generating many specs at once.

### 2.5 New output & reporting controls

- `--report-dir` lets you configure where reports are written.
- `--stdout-summary` prints a short summary at the end of a run.
- Reports live under `.spec/reports/generate-spec/` by default and include:
  - index & registry paths used
  - safety-mode, UI mode
  - multi-repo context
  - extracted entities
  - ownership notes and warnings

### 2.6 v5.6.x Hardening: Framework, AI, and Data Safety

Later 5.6.x versions (same manual) clarify that specs should also:

- declare **web stack baselines** when using React/Next.js/RSC/Node/npm:
  - reference tool baselines from `tool-version-registry.json` when available
  - document the expected version ranges and upgrade rules
- define **AI/LLM safety sections** when features involve LLMs:
  - prompt construction rules and allowed context
  - injection-resistance strategy and fallback behaviors
  - logging/telemetry rules which **exclude secrets/PII**
- include **data-sensitivity classification** when handling PII/financial/health/trade-secret data:
  - classification levels and masking rules
  - storage/retention constraints and access controls

These additions keep `/smartspec_generate_spec` aligned with the upgraded
`/smartspec_generate_plan`, `/smartspec_generate_tasks`, and `/smartspec_implement_tasks`.

---

## 3. Backward Compatibility Notes

- This manual targets `/smartspec_generate_spec` from **v5.6.1 onward** (5.6.x).
- All **existing flags are preserved**, including:
  - `--index`, `--registry-dir`, `--workspace-roots`, `--repos-config`,
    `--new`, `--repair-legacy`, `--repair-additive-meta`, `--mode`,
    `--safety-mode`, `--strict`, `--dry-run`, `--ui-mode`, `--no-ui-json`.
- New flags are **aliases or additive options**, e.g.:
  - `--specindex`, `--registry-roots`, `--report-dir`, `--stdout-summary`,
    `--kilocode`, `--nosubtasks`.
- Semantics like `dev` vs `strict` safety mode and `recommend` vs `additive` registry mode are unchanged.
- New guidance on **React/Next/AI/data-safety** is additive and does not change existing flags.

---

## 4. Core Concepts

### 4.1 SPEC_INDEX and registries

- `SPEC_INDEX` is the central map of all specs.
- `registries` are the central catalogs for entities that should be reused, such as:
  - APIs
  - data models
  - glossary terms
  - critical sections
  - UI components/patterns
  - (optionally) tool baselines, via `tool-version-registry.json`

`/smartspec_generate_spec` reads the index and registries to:

- decide where new specs should live in the tree
- know which entities must **not** be redefined locally
- recommend registry updates (depending on `--mode=recommend|additive`)

### 4.2 UI mode

Three modes:

- `auto` (default)
  - The workflow infers UI mode from context (SPEC_INDEX, spec folder, `ui.json` presence, etc.).
- `json`
  - JSON-first UI; `ui.json` is the primary source of truth for layout and structure.
- `inline`
  - UI is documented inside `spec.md`; no `ui.json` is required.

### 4.3 Safety mode

- `--safety-mode=strict` (default)
  - Enforces stricter rules on registries, ownership, cross-SPEC conflicts, and modern stack baselines.
- `--safety-mode=dev`
  - Relaxed mode for dev/sandbox/PoC scenarios.
  - Still adds warnings in reports and optionally in specs.

### 4.4 Multi-repo

- Uses `--repos-config` plus `--workspace-roots` to understand where other specs live.
- When a spec in your repo references entities owned elsewhere:
  - the spec must clearly state **where to reuse** and must not silently reimplement the entity.

### 4.5 Web stack, AI, and Data Safety in Specs

Specs that involve:

- **React/Next.js/RSC/Node/npm** should include:
  - a “Tech stack & versions” subsection with intended major/minor versions (aligned to `tool-version-registry.json` where present)
  - constraints about supported deployment modes (SSR, SSG, Edge, RSC)

- **AI/LLM features** should include:
  - a “AI/LLM behavior & safety” subsection with prompt rules, injection-resistance strategy, and logging boundaries

- **Sensitive data** should include:
  - a “Data classification & protection” subsection describing classifications, masking strategy, and retention rules

These sections power safer downstream plans, tasks, and implementation.

### 4.6 Write guard

- `write_guard = ALLOW-WRITE`.
- Writes are allowed only in:
  - `specs/**/spec.md`
  - `.spec/` (index, registries, reports)
- Sibling repos (discovered via `--workspace-roots` / `--repos-config`) are always **read-only**.

---

## 5. Quick Start Examples

### 5.1 Create a new spec for a payment service (strict mode)

```bash
smartspec_generate_spec \
  specs/payments/spec-pay-001-checkout/spec.md \
  --index=.spec/SPEC_INDEX.json \
  --registry-dir=.spec/registry \
  --safety-mode=strict \
  --ui-mode=auto \
  --stdout-summary
```

### 5.2 Repair a legacy spec to align with v5.6 (dry-run)

```bash
smartspec_generate_spec \
  specs/legacy/spec-legacy-001/spec.md \
  --repair-legacy \
  --repair-additive-meta \
  --index=.spec/SPEC_INDEX.json \
  --registry-dir=.spec/registry \
  --safety-mode=dev \
  --dry-run \
  --stdout-summary
```

### 5.3 Use dev mode for a new project without index/registries yet

```bash
smartspec_generate_spec \
  specs/newapp/spec-newapp-001/spec.md \
  --safety-mode=dev \
  --mode=recommend \
  --report-dir=.spec/reports/generate-spec/ \
  --stdout-summary
```

---

## 6. CLI / Flags Cheat Sheet

- Index & registries
  - `--index`
  - `--specindex` (alias for `--index`)
  - `--registry-dir`
  - `--registry-roots`
- Multi-repo
  - `--workspace-roots`
  - `--repos-config`
- Generation / repair
  - `--new`
  - `--repair-legacy`
  - `--repair-additive-meta`
- Registry update mode
  - `--mode=recommend|additive`
- Safety
  - `--safety-mode=strict|dev`
  - `--strict` (alias for `--safety-mode=strict`)
  - `--dry-run`
- UI mode
  - `--ui-mode=auto|json|inline`
  - `--no-ui-json`
- Output & Kilo
  - `--report-dir`
  - `--stdout-summary`
  - `--kilocode`
  - `--nosubtasks`

---

## 7. Multi-repo / Multi-registry Examples

### 7.1 Monorepo with multiple services

```bash
smartspec_generate_spec \
  specs/billing/spec-bill-002-invoice/spec.md \
  --index=.spec/SPEC_INDEX.json \
  --registry-dir=.spec/registry \
  --workspace-roots="." \
  --mode=recommend \
  --stdout-summary
```

### 7.2 Multi-repo, multi-team with a shared platform registry

```bash
smartspec_generate_spec \
  specs/notifications/spec-notif-003-email/spec.md \
  --specindex=../platform/.spec/SPEC_INDEX.json \
  --registry-dir=.spec/registry \
  --registry-roots="../platform/.spec/registry" \
  --workspace-roots="../platform;../billing" \
  --repos-config=.spec/smartspec.repos.json \
  --mode=additive \
  --safety-mode=strict \
  --stdout-summary
```

---

## 8. UI JSON vs Inline UI Examples

### 8.1 JSON-first UI (with ui.json)

```bash
smartspec_generate_spec \
  specs/web/spec-web-001-dashboard/spec.md \
  --ui-mode=json \
  --index=.spec/SPEC_INDEX.json \
  --registry-dir=.spec/registry \
  --stdout-summary
```

In this configuration, the spec is expected to have a companion
`ui.json` (either existing or generated/repaired according to policy),
with declarative structure/layout and **no embedded business logic**.

### 8.2 Inline UI (no ui.json)

```bash
smartspec_generate_spec \
  specs/legacy/spec-legacy-ui-001/spec.md \
  --ui-mode=inline \
  --index=.spec/SPEC_INDEX.json \
  --registry-dir=.spec/registry \
  --stdout-summary
```

Here UI is described directly in `spec.md`, and the workflow will **not**
attempt to require or create `ui.json`.

---

## 9. Use Case Examples – Updating Existing Specs

These examples show how to **modify existing spec files** using
`/smartspec_generate_spec` so that they match v5.6.x guardrails.

### 9.1 Upgrade an existing Next.js frontend spec with security baselines

**Scenario**

You have:

- `specs/web/spec-web-001-dashboard/spec.md`
- It’s already about a Next.js dashboard, but:
  - framework versions are unclear
  - RSC/Edge usage is undocumented
  - there’s no explicit data-sensitivity section

**Command**

```bash
smartspec_generate_spec \
  specs/web/spec-web-001-dashboard/spec.md \
  --index=.spec/SPEC_INDEX.json \
  --registry-dir=.spec/registry \
  --safety-mode=strict \
  --ui-mode=json \
  --repair-legacy \
  --repair-additive-meta \
  --stdout-summary
```

**What you should expect in the updated spec**

- A clearer “Tech stack & versions” section, aligned with
  `tool-version-registry.json` (if present).
- Explicit subsections for:
  - RSC/SSR/Edge usage and constraints
  - Data-sensitivity classification and redaction rules
- Ownership notes for shared UI components from UI/App component registries.

---

### 9.2 Align a domain API spec with platform-wide registries

**Scenario**

You have `specs/billing/spec-bill-002-invoice/spec.md` which defines
its own “CustomerProfile” model, but a **platform-wide** model already
exists in a registry.

**Command**

```bash
smartspec_generate_spec \
  specs/billing/spec-bill-002-invoice/spec.md \
  --index=.spec/SPEC_INDEX.json \
  --registry-dir=.spec/registry \
  --registry-roots="../platform/.spec/registry" \
  --repair-legacy \
  --repair-additive-meta \
  --safety-mode=strict \
  --stdout-summary
```

**Expected changes**

- The spec will be reshaped so:
  - it references the shared `CustomerProfile` model from the platform registry,
    rather than redefining it locally;
  - Ownership & Reuse section clearly notes: “Reuses platform model X”.
- Downstream workflows will then generate plans/tasks that **reuse** the platform model,
  not create a duplicate.

---

### 9.3 Update an existing AI copilot spec with safety and logging details

**Scenario**

You have `specs/ai/spec-ai-001-editor-copilot/spec.md` which describes

