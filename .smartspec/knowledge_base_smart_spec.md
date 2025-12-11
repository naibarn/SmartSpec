# SmartSpec Knowledge Base (Merged Governance) – v5.7

This knowledge base is the **single source of governance** for all SmartSpec
workflows, manuals, and specs. It merges the prior
`knowledge_base_smart_spec` and `knowledge_base_smartspec` documents.

It applies to:

- local SmartSpec CLI usage,
- Kilo Code / Claude Code / Antigravity integrations,
- project repositories that embed `.smartspec/` and `.spec/`.

Use this KB together with:

- `.smartspec/knowledge_base_smartspec_install_and_usage.md` – installation
  and basic usage guide.

---

## 1. Versioning & Backward Compatibility

- Workflows use **`Major.Minor.Patch`** (e.g., `5.6.3`).
  - Patch: small fixes, clarifications, or security updates.
  - Minor: new capabilities that remain backward compatible.
- Manuals use **`Major.Minor`** (e.g., `5.6`) and may reference a workflow
  patch range (e.g., `5.6.2–5.6.x`).
- **Zero feature removal rule**:
  - Do not remove or silently change behaviour of existing flags, modes,
    outputs, or workflows.
  - New behaviour must be **additive** (new flags, new sections,
    clarifications).
  - Deprecations require aliases, clear notes, and a migration path.

---

## 2. Project Structure & Canonical Paths

### 2.1 Core folders

SmartSpec-aware projects use the following canonical layout:

- `.smartspec/` – SmartSpec framework assets
  - `system_prompt_smartspec.md` – system prompt for AI assistants
  - `knowledge_base_smart_spec.md` – this governance KB
  - `knowledge_base_smartspec_install_and_usage.md` – install/usage KB
  - `workflows/` – workflow specs (`smartspec_<name>.md`)
  - `scripts/` – helper scripts for CI/runtime
  - `workflow.lst` – optional list of workflows to expose in docs
- `.spec/`
  - `SPEC_INDEX.json` – canonical index of spec IDs and paths
  - `registry/` – design tokens, component registries, tool-version
    registries, etc.
  - `reports/<workflow>/` – per-workflow reports
- `specs/<category>/<spec-id>/spec.md` – primary SPEC documents

### 2.2 SPEC index detection order

When a workflow needs SPEC_INDEX, it should search in this order unless a
flag overrides the path:

1. `.spec/SPEC_INDEX.json`
2. `SPEC_INDEX.json` at repo root
3. `.smartspec/SPEC_INDEX.json`
4. `specs/SPEC_INDEX.json`

If no index is found, workflows should:

- still operate on local `specs/**` where possible, and
- print a clear suggestion to create `.spec/SPEC_INDEX.json`.

---

## 3. Workflow Roles, Modes & Write Guards

Workflows are grouped by role:

1. **Governance / Verification**
   - Examples: project copilot, UI validation, release readiness.
   - Role: Ask/Architect / Governance.
   - **Write guard**: `NO-WRITE` – may not modify code/specs.
2. **Prompt-generating / planning**
   - Examples: generate_implement_prompt, generate_cursor_prompt.
   - Role: prompt producer.
   - **Write guard**: `READ-ONLY` – may emit prompts but not write files.
3. **Execution**
   - Examples: generate_spec, generate_plan, generate_tasks,
     implement_tasks, fix_errors, generate_tests.
   - Role: implement / edit project files.
   - **Write guard**: `ALLOW-WRITE`, but scope must be clearly constrained
     (e.g., only `specs/**`, only code under certain paths).

Each workflow spec must explicitly state:

- role,
- `write_guard`,
- `safety-mode` options and the effect of `strict`.

Workflows **must not call other workflows** from within their own spec.
They may recommend other workflows in prose and examples.

---

## 4. KiloCode Support & Modes

All workflows MUST accept the universal `--kilocode` flag.

- Under Kilo, workflows are orchestrated by the **Kilo Orchestrator**:
  - Reads repo state, splits work into subtasks, manages context.
- Default behaviour with `--kilocode`:
  - subtasks ON (orchestrator-per-task).
  - user may opt-out with `--nosubtasks` where supported.
- Write-scope under Kilo remains the same as local; `--kilocode` **does
  not** widen write access.

Governance/verification workflows (e.g., project_copilot, ui_validation)
remain **NO-WRITE** even under Kilo.

---

## 5. Multi-Repo & Registry Rules

To support monorepos and multi-repo workspaces, workflows may use:

- `--workspace-roots=<paths>` – `;`-separated list of workspace roots.
- `--repos-config=<path>` – describes repo layout and relations.
- `--registry-dir=<path>` – primary registry directory (authoritative).
- `--registry-roots=<paths>` – additional read-only registries.

Rules:

- The **primary registry** (from `--registry-dir` or `.spec/registry/`)
  is authoritative for design systems, components, and tool versions.
- Supplemental registries from `--registry-roots` are treated as
  read-only; workflows should prefer reuse over redefining entries.
- Cross-repo paths in flags (e.g., `--ui-spec-paths`, `--ui-test-report-paths`)
  must follow the same semantics as other workflows for consistency.

---

## 6. SPEC-first Design & Spec Autogeneration

Whenever a user asks how to **build or change a feature** (e.g., a
website, miniapp, flow, or integration), SmartSpec guidance MUST be
**SPEC-first**:

1. Map the request to the chain:

   ```text
   SPEC → PLAN → TASKS → IMPLEMENT → TESTS → QUALITY → RELEASE
   ```

2. Propose a `spec-id` and path:

   - e.g., `specs/ecommerce/ecommerce_shop_front/spec.md`
   - or multiple spec-ids when the feature is large.

3. Generate a **starter spec** that is detailed enough to:
   - run `/smartspec_generate_spec --spec-ids=<id>`,
   - run `generate_plan`, `generate_tasks`, and downstream workflows.

4. When features are large, split into 2–5 specs:
   - e.g. `*_front`, `*_checkout_flow`, `*_order_billing`, or
     `*_core`, `*_gallery`, `*_admin`.

5. Propose 3–5 concrete improvements at the end of each spec design
   (e.g., security, UX enhancements, observability, admin tools).

### 6.1 `/smartspec_generate_spec_from_prompt`

`/smartspec_generate_spec_from_prompt` is the **bootstrap workflow for first-time
spec creation from a natural language prompt**.

- Input: one prompt (Thai or English) that describes the desired feature/app.
- Behaviour:
  - inspects existing project structure (`specs/**`, SPEC_INDEX, registries),
  - infers a suitable category and 1–5 `spec-id`s for the feature,
  - creates **new starter `spec.md` files only under**
    `specs/<category>/<spec-id>/spec.md`,
  - **never overwrites** an existing `spec.md`; if a spec-id already exists,
    it creates a suffixed id (e.g. `_v2`) and explains this in the summary,
  - optionally appends to `.spec/SPEC_INDEX.json` **only when**
    `--update-index` is provided and the file is writable.
- Write scope: `ALLOW-WRITE`, but strictly limited to creating new spec
  folders/files under `specs/**` and optional SPEC_INDEX appends controlled by
  `--update-index`.
- Usage is intentionally simple for users:

  ```bash
  /smartspec_generate_spec_from_prompt "<feature description>"

  ```

- After running it, users should refine specs with
  `/smartspec_generate_spec --spec-ids=<id>`.

All SPEC-autogeneration (via prompt, copilot, or other tooling) must
adhere to this SPEC-first guidance.

---

## 7. Workflow Authoring Guidelines

When creating or updating a workflow (`.smartspec/workflows/smartspec_<name>.md`):

1. **Audit first**
   - Read existing workflow spec and manuals.
   - Read this KB and the install/usage KB.
2. **List critical gaps**
   - e.g., missing flags, unclear write-guard, security gaps,
     inconsistent folder usage.
3. **Fix additively**
   - Do not remove flags or change meanings.
   - Add clarifying sections instead.
4. **Required sections** (at minimum):
   - Summary
   - When to Use
   - Inputs & Outputs
   - Modes (role + write_guard + safety-mode)
   - Flags / CLI usage
   - Canonical Folders & File Placement
   - Behaviour & Step-by-step Flow
   - KiloCode Support (Meta-Flag)
   - Weakness & Risk Check
   - Legacy Flags Inventory
5. **Kilo & multi-repo semantics** must match this KB.
6. Do not embed business logic or spec content into registries; keep
   them as configuration/metadata.

---

## 8. Manual Authoring Guidelines

Manuals live typically under `.smartspec-docs/` and must:

- begin with a standard header table:

  ```md
  | manual_name | manual_version | compatible_workflow | compatible_workflow_versions | role |
  | --- | --- | --- | --- | --- |
  | /smartspec_<name> Manual (EN) | 5.6 | /smartspec_<name> | 5.6.x | ... |
  ```

- exist as **separate EN and TH files**, with aligned structure;
- preserve the legacy outline when upgrading;
- include sections such as:
  - Overview
  - What’s New
  - Backward Compatibility Notes
  - Core Concepts
  - Quick Start Examples
  - CLI / Flags Cheat Sheet
  - KiloCode Usage Examples
  - Multi-repo / multi-registry examples (if relevant)
  - Security & framework notes (for web/AI stacks)

Examples in EN manuals should use *English-only* prompts; Thai examples
belong in TH manuals.

---

## 9. UI Governance & Design Systems

For projects with design systems and component registries:

- Prefer **App-level components** (e.g., `AppButton`, `AppCard`) over raw
  library components, especially in critical flows.
- Store design tokens, component registries, layouts, and patterns under
  `.spec/registry/`.
- UI-related workflows (e.g., `ui_validation`, `ui_consistency_audit`)
  should:
  - treat registries as governance input (what is allowed/expected),
  - call out when critical flows diverge from App components or required
    layout patterns,
  - support both JSON-first UI (`ui.json`) and inline spec-driven UI.

When AI generates `ui.json`:

- Track origin (`AI`, `HUMAN`, `MIXED`) and review status where
  possible.
- Allow stricter rules (e.g., `--ui-json-ai-strict`) for flows that rely
  heavily on unreviewed AI UI.

---

## 10. Security & Dependency Guardrails

For modern web stacks (React, Next.js, React Server Components, Node,
`npm`):

- Treat RSC and `react-server-dom-*` usage as **high-risk surfaces**.
- Use `tool-version-registry.json` (or equivalent) to define minimum
  patched versions, especially when specific CVEs are known.
- Prefer using lockfiles (`package-lock.json`, `yarn.lock`, etc.) and
  SCA/security reports as evidence.
- Workflows should:
  - read existing security/SCA artifacts rather than running tools
    themselves (unless explicitly designed to do so),
  - surface missing or outdated evidence as part of risk assessment,
  - avoid logging secrets, tokens, or sensitive data.

For AI/LLM features and sensitive data:

- Avoid leaking PII/secrets into prompts, logs, reports, or `ui.json`.
- Respect prompt-governance rules (no implicit approval of prompts that
  bypass security controls).

---

## 11. RAG, Context Reading & Limits

Project-wide workflows (e.g., `/smartspec_project_copilot`) use
chunked-reading to stay within context limits:

- Typical chunk size: ~300–600 lines.
- Total lines per LLM call: ~800–1,000 lines max.
- Priorities for reading:
  - `.spec/SPEC_INDEX.json`
  - `.spec/registry/**`
  - `specs/**/spec.md`
  - `.spec/reports/**`
  - `.smartspec/workflows/**`
  - `.smartspec-docs/workflows/**` manuals

Answers from governance workflows should always end with:

- a status summary,
- critical issues & remediation suggestions,
- recommended next workflows + concrete CLI commands,
- a Weakness & Risk Check that calls out uncertainties and data gaps.

---

## 12. Workflow Catalog (5.6/5.7 Line)

This KB assumes the following families of workflows exist (names may be
slightly different depending on the repo, but semantics should match):

- **Project navigation & governance**
  - `/smartspec_project_copilot`
  - `/smartspec_release_readiness`
  - `/smartspec_ui_validation`
  - `/smartspec_ui_consistency_audit`
  - `/smartspec_security_evidence_audit`
  - `/smartspec_global_registry_audit`
- **Spec & planning**
  - `/smartspec_generate_spec_from_prompt`
  - `/smartspec_generate_spec`
  - `/smartspec_generate_plan`
  - `/smartspec_generate_tasks`
  - `/smartspec_spec_lifecycle_manager`
- **Implementation & quality**
  - `/smartspec_implement_tasks`
  - `/smartspec_fix_errors` – focused bug/error fixing, **can ingest implementation reports using `--report=<path>` (for example reports under `.spec/reports/implement-tasks/`) and auto-discover recent implementation reports when `--report` is not provided**.
  - `/smartspec_generate_tests`
  - `/smartspec_ci_quality_gate`
  - `/smartspec_data_migration_governance`
  - `/smartspec_observability_runbook_generator`
- **Index & registry maintenance**
  - `/smartspec_reindex_specs`
  - `/smartspec_validate_index`
  - `/smartspec_sync_spec_tasks`

Each individual workflow spec may add details, but **must not contradict
this KB** regarding versioning, write-guards, Kilo behaviour, and
security/design-system requirements.

---

## 13. Best Practices & Philosophy

- Prefer **SPEC-first** design and strong, concrete specs before
  implementation.
- Use SmartSpec as a chain, not a single tool: SPEC → PLAN → TASKS →
  IMPLEMENT → TESTS → QUALITY → RELEASE.
- When in doubt, choose conservative, backward-compatible behaviour over
  convenience.
- Reuse existing registries, design tokens, and components instead of
  reinventing them.
- Keep system prompts compact (<8,000 characters) and move detailed
  governance into this KB.

End of SmartSpec Knowledge Base (Merged Governance) – v5.7.

