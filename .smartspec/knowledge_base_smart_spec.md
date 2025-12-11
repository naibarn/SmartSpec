# Knowledge Base — SmartSpec Core Governance (Updated v5.7.2)

This is the **updated version** of `knowledge_base_smart_spec.md`, modified to align with:
- The new workflow `/smartspec_implement_tasks` v5.7.2
- The introduction of `--require-orchestrator`
- New best practices for Kilo Orchestrator usage
- Additive governance rules (no breaking semantics)

All changes are **additive**, and original semantics are preserved unless explicitly extended.

---

# 1. SmartSpec — Sources of Truth

SmartSpec operates on four layers of truth:

1. **SPEC files**: `spec.md`, `plan.md`, `tasks.md`
2. **SPEC_INDEX** (canonical index)
3. **Registries** for APIs, Models, UI components, shared entities
4. **Workflows** under `.smartspec/workflows/`

If conflicts exist:
- Governance documents override workflows
- Workflows override SPEC artifacts
- SPEC artifacts override implementation

---

# 2. Canonical Repository Layout

(Terms preserved from original KB)

```
/specs/<category>/<spec-id>/
    spec.md
    plan.md
    tasks.md

/.spec/
    SPEC_INDEX.json
    registry/

/.smartspec/workflows/
```

---

# 3. Workflow Chain (SPEC → PLAN → TASKS → IMPLEMENT)

```
/smartspec_generate_spec
/smartspec_generate_plan
/smartspec_generate_tasks
/smartspec_implement_tasks
```

Rules:
- Must run in the correct order
- Each workflow validates artifacts before moving forward
- Implementation must never override governance rules

---

# 4. Environments & Modes

SmartSpec works across:
- Kilo Code
- Claude Code
- Google Antigravity
- CLI

Workflows may detect, but **must not control**, which IDE or execution engine is active.

## 4.1 KiloCode Integration

When running under Kilo:
- Workflows may support Orchestrator-per-task execution
- Workflows must accept `--kilocode`

### **(Updated)** — Recommendation for Implement Phase
When using `/smartspec_implement_tasks` inside Kilo, SmartSpec **strongly recommends**:

```
--kilocode --require-orchestrator
```

Reason:
- Orchestrator Mode provides stable multi-file editing
- Prevents context-loss issues in Kilo
- Ensures per-task execution and consistent check-in
- Reduces ambiguity and edit collisions

Without Orchestrator, Kilo often fails on:
- Large diffs
- Multi-file edits
- Ambiguous context
- Conflicting patches

Thus, for all implement workflows:

> **If `--kilocode` is used, SmartSpec recommends also using `--require-orchestrator` for maximum stability and correctness.**

This is a **best practice**, not a breaking rule.

---

# 5. SPEC_INDEX Governance

(Same as original with minor clarifications)

- SPEC_INDEX is the official index of all specs
- Workflows must never modify SPEC_INDEX
- Detection order:
  1. `.spec/SPEC_INDEX.json`
  2. `SPEC_INDEX.json` at repo root
  3. `.smartspec/SPEC_INDEX.json` (legacy)
  4. `specs/SPEC_INDEX.json` (older pattern)

---

# 6. Registries

Rules unchanged.

- Registry entries describe canonical shared entities
- Implementation must reuse entries, not duplicate them
- Workflows may validate against multiple registries but write only to the primary registry

---

# 7. UI Governance

Rules unchanged but expanded:
- UI must be consistent with design tokens
- App-level components preferred over raw UI library components
- `ui.json` may define layout, not business logic

---

# 8. Multi-Repo Rules

No major changes.

- All external repos discovered via `--workspace-roots` or `--repos-config` are **read-only**
- No workflow may modify sibling repos

---

# 9. Safety Modes

(Summary retained)

### strict mode
- conservative
- blocks when governance artifacts are missing
- ideal for production branches

### dev mode
- permissive
- allows incomplete governance with warnings

---

# 10. Implementation Governance

Implementation workflows (especially `/smartspec_implement_tasks`) must:
- obey SPEC_INDEX boundaries
- obey registry ownership rules
- enforce AI/data-sensitivity guardrails
- enforce web-stack (React/Next/RSC/Node) baselines
- write only inside the current repo
- update `tasks.md` safely

### (Updated) — Orchestrator Requirement Best Practice
For Kilo users running implementation:

```
/smartspec_implement_tasks ... --kilocode --require-orchestrator
```

This minimizes failures caused by:
- Large multi-file edit batches
- Ambiguous diffs
- Kilo context resets
- Unstable patching logic

---

# 11. Failure Handling Principles

Unchanged except additional Kilo rules.

### New guidance:
If a Kilo edit fails:
- Do not stop instantly
- Narrow the scope
- Retry with smaller ranges
- Provide explicit next-step options

---

# 12. Cross-Workflow Behavior

- Workflows may reference each other but **must not call each other**
- Must guide users to use the correct workflow path
- Must respect `--validate-only` always

---

# 13. Best Practices (Updated)

### ⭐ Implement phase (most important update)
Use this pattern:
```
--kilocode --require-orchestrator --safety-mode=strict
```

### ⭐ Why?
- Ensures Orchestrator Mode is active
- Prevents unstable edits
- Improves accuracy of multi-file changes
- Reduces cognitive load and failures

### ⭐ Additional Practices
- Use `--validate-only` before running on a large repo
- Keep SPEC_INDEX and registry updated
- Keep tasks small and precise

---

# 14. Security Rules

Unchanged:
- No secrets in code or prompts
- PII must be masked
- AI prompts treated as untrusted input

---

# 15. Appendix

This KB remains fully backward-compatible.
All new features (`--require-orchestrator`) are additive.

# END

