# UPDATED KNOWLEDGE BASE – `knowledge_base_smartspec_install_and_usage.md`
## Additive Extension for Workflow: `/smartspec_report_implement_prompter`
### Version: 1.0.2 — Installation & Usage Manual Extension

> **NOTE:** This update is *additive* and does **not** modify or override existing SmartSpec CLI rules. All original workflow definitions remain valid. This extension introduces the new workflow, usage patterns, flags, and lifecycle integration.

---
# 1. Overview (Unchanged Core)
*(Original installation and general workflow usage content preserved; new workflow added below.)*

---
# 2. NEW WORKFLOW ADDITION

# `/smartspec_report_implement_prompter`
### Classification
Evidence-Driven Implementation Prompt Generator (post-strict-verification helper)

### Purpose
This workflow reads the JSON output produced by `/smartspec_verify_tasks_progress_strict` and generates:
- A summarized set of implementation gaps
- Domain‑clustered implementation prompts (API / Tests / Docs / Deploy)
- Optional JSON outputs for UI/IDE integrations

It exists to reduce repetitive implement‑verify cycles by providing targeted, context‑aware AI‑consumable instructions.

---
# 3. Installation & Invocation
Since this is a first-party SmartSpec workflow, installation requires **no additional setup** beyond regular SmartSpec installation.

To use the workflow, run:
```bash
/smartspec_report_implement_prompter \
  --spec <path/to/spec.md> \
  --tasks <path/to/tasks.md> \
  --report <path/to/strict-report.json> \
  --output <directory>
```

---
# 4. Required & Optional Flags

## 4.1 Required Flags
| Flag | Description |
|------|-------------|
| `--spec` | Path to the SPEC file used during strict verification. |
| `--tasks` | Path to the corresponding TASKS file. |
| `--report` | Path to the strict verification JSON report. |

## 4.2 Optional Flags
| Flag | Purpose |
|------|---------|
| `--output` | Directory to write prompt files; optional but recommended. |
| `--cluster` | Limit generation to `api`, `tests`, `docs`, `deploy`, or `all`. |
| `--language` | Force output language (`th` or `en`). |
| `--workspace-roots` | Required for multi-repo resolution. |
| `--repos-config` | Required for multi-repo workspace graph binding. |
| `--evidence-config` | Custom evidence mapping for tasks or clusters. |
| `--dry-run` | Print what would be generated; create no files. |
| `--format` | Output format: `markdown` (default) or `json`. |
| `--max-tasks-per-prompt` | Override default limit (15). |
| `--max-chars-per-prompt` | Override default limit (35,000 chars). |

---
# 5. Multi‑Repo Usage Guidance
This workflow requires **the same workspace context** as the strict verifier.

### When working in a multi-repo setup:
```
--workspace-roots <paths> \
--repos-config <path/to/repos-config.json>
```
These flags ensure correct resolution of:
- SPEC path
- TASKS path
- Strict report path
- Evidence config path

If missing while multi-repo mode is detected → workflow must warn.

---
# 6. Evidence Config Usage
Some projects have custom evidence rules, e.g.:
- alternative test directories
- custom doc-generation locations
- domain-specific verification requirements

The workflow can read:
```
--evidence-config config.json
```
Or auto-discover:
```
.smartspec/evidence-config/<spec-id>.json
```
This affects cluster mapping and prompt instructions.

---
# 7. Output Directory Structure
If `--output` is provided, the workflow generates:
```
.smartspec/prompts/<spec-id>/
  ├── README.md
  ├── api-implementation-prompt.md
  ├── testing-prompt.md
  ├── documentation-prompt.md
  ├── deployment-prompt.md
```
When limits exceeded:
```
  testing-prompt-1.md
  testing-prompt-2.md
```
When no implementation is required:
```
  README.md (summary only)
```

---
# 8. Task Classification Rules (Usage Perspective)
Tasks in the strict report are categorized as:

### `unsynced_only`
Evidence complete; only checkbox mismatch.
Recommend:
```
/smartspec_sync_tasks_checkboxes
```

### `simple_not_started`
Not critical; implementation straightforward.
Recommend:
```
/smartspec_implement_tasks
```

### `complex_cluster`
Critical, ambiguous, or multi-file implementation required → Workflow generates prompts.

---
# 9. Integration with `/smartspec_project_copilot`
When the strict verifier shows:
- Critical missing components
- Partial phases
- Large numbers of incomplete tasks

The project copilot should recommend:
```
Run /smartspec_report_implement_prompter to generate IDE-ready implementation prompts.
```
This is officially supported UI guidance.

---
# 10. Localization Rules
Language resolved by:
1. `--language`
2. `Language:` header in spec
3. Spec/Tasks content ratio (>20% Thai → TH)
4. Platform default (Kilo Code → TH)
5. Default fallback → EN

---
# 11. Example Usage Scenarios

## Scene A: API endpoints incomplete
Strict report shows missing endpoints → Workflow produces `api-implementation-prompt.md`.

## Scene B: Entire testing phase incomplete
Workflow clusters all test tasks → Produces `testing-prompt.md`.

## Scene C: Deployment not ready
Missing K8s manifests / monitoring → Produces `deployment-prompt.md`.

## Scene D: All tasks implemented
Workflow outputs only README.md summarizing no remaining work.

---
# 12. JSON Output Mode
If run with:
```
--format json
```
Workflow emits structured JSON containing:
- clusters
- tasks per cluster
- rendered prompt body
- metadata

This enables consumption by IDE sidebars or SmartSpec UI modules.

---
# 13. Error Handling Behavior
Workflow must:
- Warn if strict report missing or unreadable
- Warn if report version > supported
- Warn if unresolved task IDs
- Warn if no clusters detected
- Continue safely with fallback behaviors

---
# 14. Large Report Handling
For reports exceeding thresholds:
- Use streaming parser
- Limit generation to complex tasks unless overridden by user flags

---
# END OF KB EXTENSION (`knowledge_base_smartspec_install_and_usage.md`)

