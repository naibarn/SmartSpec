# SmartSpec v5.6 — TASKS Generation Manual (Multi-Repo + Multi-Registry Aligned)

> This manual keeps the original SmartSpec manual style while reflecting the **/smartspec_generate_tasks v5.6** workflow.
>
> - All essential behaviors from earlier manuals are preserved.
> - Enhancements focus on **multi-repo**, **multi-registry**, and end-to-end consistency with **/smartspec_generate_spec v5.6**.
> - Subtasks remain enabled by default to maximize LLM reliability.

---

# 1. Summary

The `/smartspec_generate_tasks` command generates `tasks.md` from a SmartSpec `spec.md`.

In v5.6, this workflow is designed to be:

- The **primary execution blueprint** for implementation
- Cross-SPEC aligned via `SPEC_INDEX.json`
- Registry-aware for shared APIs, models, glossary, patterns, and UI components
- **Multi-repo safe** (prevents duplicate implementations across repos)
- **Multi-registry aware** (validates against supplemental registries)
- LLM-safe through atomic subtasks, explicit dependencies, and strong guard rails

---

# 2. Usage

```bash
/smartspec_generate_tasks <path_to_spec.md> [options...]
```

Examples:

```bash
/smartspec_generate_tasks specs/checkout/spec.md
/smartspec_generate_tasks specs/profile/spec.md --nosubtasks
/smartspec_generate_tasks specs/ui/cart/spec.md --ui-mode=inline --mode=dev

# Multi-repo tasks generation
/smartspec_generate_tasks specs/checkout/spec.md \
  --repos-config=.spec/smartspec.repos.json \
  --registry-roots="../repo-a/.spec/registry,../repo-b/.spec/registry"

# Lightweight multi-repo mode
/smartspec_generate_tasks specs/checkout/spec.md \
  --workspace-roots="../Repo-A,../Repo-B"
```

---

# 3. Output Location

By default:

```text
<same-folder-as-spec>/tasks.md
```

---

# 4. Workflow Mode (Strict vs Dev)

```bash
--mode=<strict|dev>
```

- `strict` (default)
  - Recommended for production/CI.
  - Requires critical context when expected by project policy.
  - Enforces cross-repo ownership clarity.
  - Requires at least a scoped repository scan.

- `dev`
  - Recommended for early-stage projects and local iteration.
  - Allows best-effort tasks generation if context is incomplete.
  - Inserts high-visibility warnings in `tasks.md`.
  - Adds bootstrap tasks for missing governance artifacts.

---

# 5. Index & Registry Options

## 5.1 SPEC_INDEX Path

```bash
--index=<path_to_SPEC_INDEX.json>
--specindex=<path_to_SPEC_INDEX.json>   # legacy alias
```

Behavior:
- Overrides automatic index detection.
- Enables explicit cross-SPEC dependency alignment.

## 5.2 Primary Registry Directory

```bash
--registry-dir=<dir>
```

Default:
- `.spec/registry`

Behavior:
- Used as the **authoritative** registry source for shared names.

---

# 6. Multi-Registry Options (NEW)

## 6.1 Supplemental Registry Roots

```bash
--registry-roots=<csv>
```

Purpose:
- Load additional registry directories **read-only** for cross-repo validation.
- Detect shared entities defined outside the current repo.

Precedence rules:
1) The primary registry (`--registry-dir`) is authoritative.
2) Supplemental registries (`--registry-roots`) inform warnings and anti-duplication checks.

If an entity exists only in a supplemental registry:
- Tasks should prefer `Resource usage: reuse`.
- The workflow should emit warnings if the spec attempts to create an equivalent entity.

---

# 7. Multi-Repo Options (NEW)

These flags mirror `/smartspec_generate_spec v5.6` and `/smartspec_validate_index`.

## 7.1 Workspace Roots

```bash
--workspace-roots=<csv>
```

Behavior:
- Adds sibling repo roots to search for dependency specs.

## 7.2 Repos Config

```bash
--repos-config=<path>
```

Behavior:
- Uses a structured mapping of repo IDs to physical roots.
- Takes precedence over `--workspace-roots`.

Suggested default:
- `.spec/smartspec.repos.json`

---

# 8. Dry Run

```bash
--dry-run
--nogenerate   # alias
```

Behavior:
- Analyze specs and show tasks that would be generated.
- Do not write files.

---

# 9. Subtask Control (DEFAULT = ON)

```bash
--nosubtasks
```

Behavior:
- Generate only top-level tasks (T001, T002, ...).

Default:
- Subtasks are generated automatically to prevent LLM drift.

Subtask format:
- `T001.1, T001.2, ...`

Each subtask should include dependencies when logical ordering exists.

---

# 10. UI Mode Options

```bash
--ui-mode=<auto|json|inline>
--no-ui-json      # alias for inline
```

- `auto` (default)
  - Resolves UI mode from index category, `ui.json`, and explicit UI JSON references.

- `json`
  - UI design is driven by `ui.json`.
  - Tasks will include generating/validating `ui.json` and mapping UI nodes to components.

- `inline`
  - UI requirements remain in code/spec without a `ui.json` contract.
  - Tasks will still enforce modern responsive design and UI/logic separation.

LLMs must not override the resolved UI mode.

---

# 11. What SmartSpec Generates

Top-level categories:

```text
T001 — Setup & Baseline
T002 — Core Implementation
T003 — Cross-SPEC Shared Work
T004 — Integrations
T005 — Testing
T006 — Observability & Operations
T007 — Security & Compliance
T008 — UI & UX
```

---

# 12. Resource Usage (Multi-Repo Aware)

Every task/subtask includes:

```yaml
Resource usage:
  type: reuse | create
  chain_owner:
    api_owner: <spec-id|null>
    model_owner: <spec-id|null>
    pattern_owner: <spec-id|null>
    terminology_owner: <spec-id|null>
  registry:
    api: <name if applicable>
    model: <name if applicable>
    ui_component: <name if applicable>
  files:
    - <paths when known>
  justification: <required for create>
  repo_context:
    owner_repo: <id|unknown>
    consumer_repo: <id|current>
```

Rules:
- `reuse` → MUST call/import canonical implementations.
- `create` → MUST justify creation and confirm no equivalent exists in any loaded registry view.
- When `owner_repo != consumer_repo`, tasks must specify the import/integration boundary.

---

# 13. Guard Rails in tasks.md

Generated `tasks.md` begins with global rules that enforce:
- Loading referenced specs + registries before coding
- No reimplementation of shared entities
- Cross-repo reuse when owners live in another repository
- Strict adherence to Resource usage
- Respect for resolved UI mode
- Version pinning and regeneration policy when upstream specs change

---

# 14. Version Pinning

Generated tasks include:

```text
Generated from SPEC:
  id: <spec-id>
  version: <front-matter | git hash | UNKNOWN>
  source: <front-matter | git | unknown>
  generated_at: <timestamp>
```

Rule:
- If any referenced spec updates after `generated_at`, STOP and regenerate `tasks.md`.

---

# 15. Troubleshooting

| Issue | Likely Cause | Fix |
|------|--------------|-----|
| Tasks suggest duplicate logic across repos | Multi-repo roots not provided | Add `--repos-config` or `--workspace-roots` and reload dependency specs |
| Shared names mismatch | Only local registry loaded | Add `--registry-roots` or define a shared registry strategy |
| Strict mode blocks generation | Missing critical governance context | Initialize `.spec/SPEC_INDEX.json` and primary registries or use `--mode=dev` for bootstrap |

---

# 16. Final Notes

This manual reflects the v5.6 workflow and keeps the original SmartSpec style.

The recommended chain for multi-repo projects is:

1) `/smartspec_validate_index --repos-config=... --registry-roots=...`
2) `/smartspec_generate_spec ... --repos-config=... --registry-roots=...`
3) `/smartspec_generate_tasks ... --repos-config=... --registry-roots=...`

This ensures consistent governance across repositories and minimizes duplicate implementations.

