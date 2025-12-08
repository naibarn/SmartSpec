# SmartSpec v5.6 — SPEC Generation Manual (Multi-Repo + Multi-Registry Aligned)

> This manual retains the original SmartSpec manual style while reflecting the **/smartspec_generate_spec v5.6** workflow.
>
> - All essential behaviors from earlier SPEC manuals are preserved.
> - Enhancements focus on **task-readiness**, **multi-repo**, and **multi-registry** consistency.
> - The manual is aligned end-to-end with:
>   - `/smartspec_validate_index v5.6 alignment`
>   - `/smartspec_generate_tasks v5.6`

---

# 1. Summary

The `/smartspec_generate_spec` command creates a new `spec.md` or repairs a legacy spec while enforcing SmartSpec centralization rules.

In v5.6, the SPEC workflow is designed to:

- Produce **task-ready specs** that are clear enough to generate high-quality `tasks.md`
- Prevent cross-SPEC and cross-repo duplication of:
  - APIs
  - data models
  - glossary terms
  - patterns
  - UI components
- Align naming and ownership with canonical registries
- Support both **single-repo** and **multi-repo** architectures
- Preserve legacy spec content in repair modes

---

# 2. Usage

```bash
/smartspec_generate_spec <path_to_spec.md> [options...]
```

Examples:

```bash
# New spec generation
/smartspec_generate_spec specs/core/spec-core-004-rate-limiting/spec.md --new

# Legacy repair (non-destructive)
/smartspec_generate_spec specs/legacy/spec.md --repair-legacy

# Add small meta blocks safely
/smartspec_generate_spec specs/legacy/spec.md --repair-legacy --repair-additive-meta

# Multi-repo spec generation with structured config
/smartspec_generate_spec specs/checkout/spec.md \
  --repos-config=.spec/smartspec.repos.json \
  --registry-roots="../Repo-A/.spec/registry,../Repo-B/.spec/registry"

# Lightweight multi-repo mode
/smartspec_generate_spec specs/checkout/spec.md \
  --workspace-roots="../Repo-A,../Repo-B"
```

---

# 3. Output Location

By default, SmartSpec writes or updates:

```text
<same-folder-as-target>/spec.md
```

Reports are written under:

```text
.spec/reports/generate-spec/
```

---

# 4. Index & Registry Options

## 4.1 SPEC_INDEX Path

```bash
--index=<path_to_SPEC_INDEX.json>
--specindex=<path_to_SPEC_INDEX.json>   # legacy alias (recommended support)
```

Behavior:
- Overrides automatic index detection.
- Enables explicit cross-SPEC dependency alignment.

## 4.2 Primary Registry Directory

```bash
--registry-dir=<dir>
```

Default:
- `.spec/registry`

Behavior:
- Treats this directory as the **authoritative** registry source for shared names.

---

# 5. Multi-Registry Options (NEW)

## 5.1 Supplemental Registry Roots

```bash
--registry-roots=<csv>
```

Purpose:
- Load additional registry directories **read-only** for cross-repo validation.
- Detect shared entities defined outside the current repository.

Precedence rules:
1) The primary registry (`--registry-dir`) is authoritative.
2) Supplemental registries (`--registry-roots`) are validation sources.

If an entity exists only in a supplemental registry:
- The spec should be written with explicit **Reuse vs. Local** intent.
- In strict safety mode, the workflow should warn against proposing a conflicting shared name.

---

# 6. Multi-Repo Options (NEW)

These flags align with `/smartspec_validate_index` and `/smartspec_generate_tasks`.

## 6.1 Workspace Roots

```bash
--workspace-roots=<csv>
```

Behavior:
- Adds sibling repo roots to search for dependency specs.
- Use when specs are distributed across multiple repositories.

## 6.2 Repos Config

```bash
--repos-config=<path>
```

Behavior:
- Uses a structured mapping of repo IDs to physical roots.
- Takes precedence over `--workspace-roots`.

Suggested default path:
- `.spec/smartspec.repos.json`

Recommended structure:

```json
{
  "version": "1.0",
  "repos": [
    { "id": "public",  "root": "../Repo-A" },
    { "id": "private", "root": "../Repo-B" }
  ]
}
```

---

# 7. Registry Update Mode (Legacy-Compatible)

```bash
--mode=<recommend|additive>
```

- `recommend` (default)
  - Do not write registries.
  - Output suggested additions to the report.

- `additive`
  - Append missing entries only.
  - Never delete, rename, or restructure existing entries.
  - Should provide a diff-style summary in the report.

---

# 8. Safety Mode (Strict vs Dev)

To avoid confusion with registry update mode, v5.6 uses a separate flag:

```bash
--safety-mode=<strict|dev>
--strict   # legacy boolean equivalent to strict
```

- `strict` (default)
  - Use for CI / shared branches / production-grade governance.
  - Requires ownership clarity for shared names.
  - Fails or blocks when cross-SPEC conflicts would create duplicate shared entities.
  - Requires explicit cross-repo reuse notes when dependencies live in another repo.

- `dev`
  - Use for early-stage projects or local iteration.
  - Allows best-effort spec generation.
  - Inserts high-visibility warnings in reports.
  - Recommends initializing missing index/registries.

---

# 9. UI Mode Options

```bash
--ui-mode=<auto|json|inline>
--no-ui-json       # alias for inline
```

- `auto` (default)
  - Resolves UI mode using precedence:
    1) explicit flags
    2) SPEC_INDEX category (UI)
    3) existing `ui.json`
    4) explicit UI JSON references in text
    5) fallback to `inline`

- `json`
  - UI design source of truth is `ui.json`.
  - The spec should link to `ui.json` and define UI/logic boundaries.

- `inline`
  - UI requirements remain inside `spec.md`.
  - The spec must still state UI/UX goals and conversation with design system or tokens when defined.

---

# 10. What SmartSpec Generates in Spec Content

When creating a new `spec.md`, SmartSpec includes the established core sections (legacy-consistent):

- Overview
- Goals & Non-Goals
- Scope
- Dependencies
- Functional Requirements
- Non-Functional Requirements
- High-level Architecture
- Data Models
- API Contracts
- Error Handling
- Security Considerations
- Observability
- Testing Strategy
- Migration / Backward Compatibility (when relevant)
- UI Section (conditional)
- Ownership & Reuse (recommended for task-readiness)

---

# 11. Task-Readiness Enhancements (v5.6)

To ensure excellent `tasks.md` downstream, the spec should contain concise, explicit hints:

1) **Ownership & Reuse notes**
   - Which APIs/models/components are reused from other specs
   - Which ones are local-only

2) **Dependency clarity**
   - Must match SPEC_INDEX when present

3) **UI boundary statements**
   - Clear separation of presentation vs domain logic

4) **Lightweight module intent**
   - Optional file or module boundaries when they prevent duplication

5) **Versioning readiness**
   - Prefer a front-matter `version:` field

These additions are intentionally lightweight to avoid making specs overly complex.

---

# 12. Cross-Repo Anti-Duplication Guidance

If a dependency is resolved from another repository:

- The spec must include explicit guidance clarifying:
  - the owner repo
  - the canonical spec ID
  - reuse expectations
  - what should NOT be reimplemented locally

This ensures that `/smartspec_generate_tasks` will correctly generate `reuse` tasks rather than parallel `create` tasks.

---

# 13. Legacy Repair Options

## 13.1 Non-Destructive Repair

```bash
--repair-legacy
```

Behavior:
- Treats the existing `spec.md` as read-only for core narrative.
- Extracts missing structure and centralization signals.
- Does not remove or rewrite original explanations.

## 13.2 Additive Metadata

```bash
--repair-additive-meta
```

Behavior:
- Allows insertion of a clearly labeled metadata block, for example:
  - "Centralization & Task-Readiness Additive Metadata"
- Must not change the meaning of any existing section.

---

# 14. Reports & Readiness Checklist

Reports are designed to help teams judge whether a spec is ready for tasks generation.

A typical report should include:
- Index path used
- Registry directory used
- Supplemental registry roots used
- Multi-repo roots used
- Safety mode
- UI mode
- Extracted entities summary
- Ownership clarity notes
- Cross-SPEC conflict warnings
- Cross-repo duplication risks
- Versioning status
- Recommended follow-up workflows

---

# 15. Recommended Chain for Multi-Repo Projects

To keep governance consistent across two or more repos:

1) `/smartspec_validate_index`  
   - with `--repos-config` and `--registry-roots`

2) `/smartspec_generate_spec`  
   - with the same multi-repo and multi-registry flags

3) `/smartspec_generate_tasks`  
   - with the same multi-repo and multi-registry flags

This ensures that shared ownership and naming rules remain consistent across the entire pipeline.

---

# 16. Troubleshooting

| Issue | Likely Cause | Fix |
|------|--------------|-----|
| Spec appears to redefine shared APIs/models | Only local registry loaded | Add `--registry-roots` or define a shared registry strategy |
| Dependencies cannot be resolved | Missing multi-repo roots | Add `--repos-config` or `--workspace-roots` |
| Strict mode blocks spec update | Ownership unclear | Add explicit Ownership & Reuse notes or run validate_index first |
| UI mode resolved unexpectedly | Ambiguous UI signals | Explicitly set `--ui-mode` |

---

# 17. Final Notes

This manual reflects **/smartspec_generate_spec v5.6** and maintains the original SmartSpec manual readability.

It is intentionally aligned with:
- `/smartspec_validate_index v5.6 alignment`
- `/smartspec_generate_tasks v5.6`

For single-repo projects, the new flags are optional.
For multi-repo platforms, they are strongly recommended to prevent duplicate implementations and naming drift.

