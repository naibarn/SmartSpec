# SmartSpec Workflow Manual
## `/smartspec_reindex_workflows`
### Version 1.0.0 — English Edition

---

# 1. Overview
`/smartspec_reindex_workflows` is the official SmartSpec workflow responsible for building and refreshing the **WORKFLOW_INDEX.json**, a centralized index of all SmartSpec workflows available within a repository or multi-repository workspace.

It is the workflow-level counterpart of `/smartspec_reindex_specs` (which manages SPEC_INDEX.json).

This workflow:
- Discovers workflow spec files under `.smartspec/workflows/`
- Extracts governance metadata (role, category, write_guard, flags, versions)
- Normalizes and aggregates these into `WORKFLOW_INDEX.json`
- Produces human-readable and machine-readable reports
- Supports multi-repo resolution and safe write-guard rules

---
# 2. Purpose
The primary goals of this workflow are:

- Provide a **unified map** of all available SmartSpec workflows
- Allow SmartSpec UI, Project Copilot, and IDE integrations to identify workflows, their capabilities, required flags, categories, and dependencies
- Maintain consistency and governance across workflow definitions
- Enable future tooling:
  - workflow validation (`/smartspec_validate_workflows`)
  - workflow discovery interfaces
  - automation pipelines

---
# 3. Workflow Position in the SmartSpec Ecosystem
```
           +-------------------------+
           | .smartspec/workflows/*.md|
           +-------------+-----------+
                         |
                         v
        /smartspec_reindex_workflows
                         |
                         v
          +---------------------------+
          | WORKFLOW_INDEX.json       |
          +---------------------------+
                         |
                         v
      Recommended consumers:
      - /smartspec_project_copilot
      - SmartSpec UI / IDE integrations
      - Automation pipelines
```

This workflow never modifies SPEC, TASKS, source code, tests, or deployment files.
It writes only:
- `.smartspec/WORKFLOW_INDEX.json`
- Reports under `.spec/reports/reindex-workflows/`

---
# 4. Responsibilities
`/smartspec_reindex_workflows` must:

1. **Discover** all workflow spec files
2. **Parse** workflow metadata (id, version, role, write-guard, flags, dependencies)
3. **Normalize** metadata into a canonical format
4. **Resolve paths** in single-repo or multi-repo mode
5. **Detect conflicts** such as duplicate workflow IDs
6. **Write the canonical index** as WORKFLOW_INDEX.json
7. **Generate reports** summarizing issues or conflicts

---
# 5. Input Sources
The workflow gathers data from:
- `.smartspec/workflows/` (default root)
- existing WORKFLOW_INDEX.json (optional)
- `--workspace-roots` and `--repos-config` (multi-repo environments)
- optional custom governance or evidence configs (read-only)

All inputs are **read-only**, except the final index file and reports.

---
# 6. Outputs
### 6.1 Primary Output
```
.smartspec/WORKFLOW_INDEX.json
```

### 6.2 Optional Mirror Output
If enabled:
```
WORKFLOW_INDEX.json (repo root)
```

### 6.3 Reports
```
.spec/reports/reindex-workflows/<timestamp>-report.md
.spec/reports/reindex-workflows/<timestamp>-report.json
```

---
# 7. CLI Usage
### Basic usage
```bash
/smartspec_reindex_workflows --report=summary
```

### Multi-repo example
```bash
/smartspec_reindex_workflows \
  --workspace-roots=.,../service-a,../service-b \
  --repos-config=.smartspec/repos-config.json \
  --report=detailed
```

### Dry-run example
```bash
/smartspec_reindex_workflows --dry-run --report=detailed
```

---
# 8. CLI Flags Reference

## 8.1 Output Flags
| Flag | Purpose |
|------|---------|
| `--out=<path>` | Set custom output location for WORKFLOW_INDEX.json |
| `--mirror-root=<true|false>` | Write an additional mirror file at repo root |

## 8.2 Discovery Flags
| Flag | Purpose |
|------|---------|
| `--workflow-roots=<csv>` | Override workflow directories (default: `.smartspec/workflows`) |
| `--include-internal=<true|false>` | Include internal or experimental workflows |

## 8.3 Multi-Repo Flags
| Flag | Purpose |
|------|---------|
| `--workspace-roots=<csv>` | Required in multi-repo contexts |
| `--repos-config=<path>` | Preferred source of workspace metadata |

## 8.4 Safety / Output Behavior
| Flag | Purpose |
|------|---------|
| `--report=<summary|detailed>` | Level of report detail |
| `--dry-run` | Build index in memory without writing output |
| `--safety-mode=<strict|dev>` | Control error-handling strictness |
| `--strict` | Alias for `--safety-mode=strict` |

## 8.5 Filtering
| Flag | Purpose |
|------|---------|
| `--include-status=<csv>` | Include workflows with certain statuses (e.g., stable,beta) |
| `--exclude-status=<csv>` | Exclude workflows (e.g., deprecated) |
| `--include-platforms=<csv>` | Include workflows supporting specific platforms |

---
# 9. Workflow Metadata Schema
Each workflow entry in `WORKFLOW_INDEX.json` contains:

- `id` — canonical workflow id (e.g., `smartspec_report_implement_prompter`)
- `name` — full CLI name (`/smartspec_report_implement_prompter`)
- `version` — workflow version
- `role` — operational role (e.g., `support/implement`)
- `category` — high-level grouping
- `status` — `stable`, `beta`, `deprecated`, etc.
- `description` — brief purpose
- `write_guard` — allowed write permissions
- `source_file` — path to workflow spec
- `supported_platforms` — e.g., `["kilocode", "claudecode", "antigravity"]`
- `cli`:
  - `binary` — execution name
  - `required_flags[]`
  - `optional_flags[]`
- `tags[]` — free-form descriptors
- `depends_on[]` — upstream workflows
- `produces[]` — output file patterns
- `last_updated` — timestamp

---
# 10. Conflict Detection
The workflow checks for:
- duplicate workflow IDs
- conflicting roles or write guards
- mismatched CLI names
- invalid or missing workflow spec files

Behavior varies by safety mode:
- **strict** → block index writing on severe conflicts
- **dev** → allow index generation but mark conflicting entries

---
# 11. Large Workspace Handling
For large or multi-repo projects:
- streaming or chunked parsing is recommended
- index writing remains atomic
- warnings are issued for inconsistent repo configurations

---
# 12. Consumption by Other Tools
### 12.1 `/smartspec_project_copilot`
Uses WORKFLOW_INDEX.json to:
- recommend next workflows
- display workflow metadata
- generate CLI examples

### 12.2 SmartSpec UI / IDE Integrations
Use the index to:
- list available workflows
- filter by category, role, platform, status
- build command templates for the user

### 12.3 Automation Pipelines
Useful for CI steps like:
- validating workflow definitions
- checking workflow completeness
- ensuring workflow governance alignment

---
# 13. Error Handling
The workflow must:
- warn about missing or unreadable workflow roots
- warn for undefined or unsupported fields
- detect missing required CLI flags in specs
- record all issues in the final report

In strict mode, fatal errors abort index generation.

---
# 14. Best Practices
- Keep workflow specs versioned and organized under `.smartspec/workflows/`
- Re-run this workflow whenever workflow specs are added, removed, or modified
- Use `--dry-run` in CI to detect metadata conflicts early
- Use detailed reports during development

---
# 15. Summary
`/smartspec_reindex_workflows` is the governance-backed mechanism for producing a unified, structured workflow index. It strengthens:
- Workflow discoverability
- Governance enforcement
- IDE and UI integrations
- Automation pipelines

By maintaining `WORKFLOW_INDEX.json`, SmartSpec gains a powerful, future-proof foundation for workflow orchestration.

---
End of Manual.