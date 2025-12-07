# /smartspec_portfolio_planner.md

## Overview

**Portfolio Planner** is a governance-level SmartSpec workflow that helps you understand and plan work across **many SPECS at once**.
It builds a portfolio view from the canonical index and registries to reduce large-project risks such as:

- Implementing features before their dependencies are ready
- Divergent naming across teams
- Public specs accidentally driving changes inside private/core specs
- UI work drifting away from design artifacts

This workflow is **read-only** for `.spec/` by default.
It produces reports and recommended next actions.

---

## When to Use

### ✅ Use it when you:

- Have a **large project** with dozens/hundreds of SPECS
- Need a **dependency-aware roadmap**
- Want to group work by **tag**, **category**, or **repo**
- Are preparing for a major milestone or release
- Need early visibility into **cross-SPEC risks**

### ❌ Skip it when you:

- Are working on a small single-feature change
- Only need spec-scoped tasks (use `/smartspec_generate_tasks.md`)

---

## Inputs & Resolution Rules

Portfolio Planner follows the same centralization resolver as other workflows.

### 1) SPEC_INDEX resolution order

1. `--specindex="<path>"`
2. `.spec/SPEC_INDEX.json`
3. `SPEC_INDEX.json` (legacy)
4. `.smartspec/SPEC_INDEX.json` (legacy)
5. `specs/SPEC_INDEX.json` (legacy)

### 2) Config resolution order

1. `--config-path="<path>"`
2. `.spec/smartspec.config.json`
3. `.smartspec/smartspec.config.json`
4. Built-in defaults

### 3) Default directories

- `SPEC_HUB_DIR = ".spec"`
- `REGISTRY_DIR = ".spec/registry"`
- `OUTPUT_DIR = ".smartspec"`

---

## Command Usage

### Basic

```bash
/smartspec_portfolio_planner
```

### Filter by tag

```bash
/smartspec_portfolio_planner --tag=security
```

### Filter by repo

```bash
/smartspec_portfolio_planner --repo=public
```

### Detailed report

```bash
/smartspec_portfolio_planner --report=detailed
```

### Export a roadmap file

```bash
/smartspec_portfolio_planner --export=roadmap.md
```

---

## Key Outputs

Reports are written to:

```
.smartspec/reports/portfolio/
```

Recommended output files:

- `portfolio-summary-<timestamp>.md`
- `portfolio-detailed-<timestamp>.md` (when `--report=detailed`)
- `roadmap.md` (when `--export=...`)

---

## What the Report Should Contain

### 1) Dependency view

- Root specs
- Core hubs (many dependents)
- Leaf features

### 2) Priority & readiness

- High-priority specs missing plan/tasks
- Specs that should be sequenced earlier

### 3) Public ↔ Private policy highlights

- Public specs depending on private/core contracts
- Recommendations to keep changes inside the correct repo

### 4) UI track view

If a spec is `category=ui`:

- Check for a Penpot-editable design artifact (`ui.json` or configured filename)
- Flag missing design files as **warnings** (legacy UI mode)
- Recommend splitting work into:
  - Design tasks
  - Binding tasks
  - Logic tasks

---

## Best Practices

- Run Portfolio Planner:
  - Before creating tasks for large feature bundles
  - After merging branches that add/remove specs
  - Before major releases
- Treat its output as a **decision aid**:
  - It should tell you which spec-scoped workflows to run next

---

## Common Follow-up Workflows

Based on report results, you may want to run:

- `/smartspec_reindex_specs.md`
- `/smartspec_validate_index.md`
- `/smartspec_generate_plan.md`
- `/smartspec_generate_tasks.md`
- `/smartspec_spec_lifecycle_manager.md`
- `/smartspec_global_registry_audit.md`

---

## Troubleshooting

### “SPEC_INDEX not found”

Ensure you have a canonical index at:

- `.spec/SPEC_INDEX.json`

If you are migrating from legacy layout, run:

```bash
/smartspec_generate_spec "First Spec" --repair-legacy
```

---

## Summary

Portfolio Planner gives you an **executive view** of your SmartSpec system:
dependencies, priorities, repo boundaries, and UI readiness.
It reduces surprise work and helps align many teams under one consistent plan.
