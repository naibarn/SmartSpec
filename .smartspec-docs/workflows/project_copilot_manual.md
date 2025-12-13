# /smartspec_project_copilot Manual (v6.0, English)

## Overview

The `/smartspec_project_copilot` workflow (version 6.0.7) serves as the **read-only front door** and governance advisor for a SmartSpec-enabled project.

Its primary purpose is to answer project, domain, or specification-related questions by analyzing existing project artifacts (indexes, registries, specs, plans, tasks, and reports). Based on this evidence, it summarizes the project status and, crucially, routes the user to the **correct next SmartSpec workflows and commands** needed to advance the project.

**Key Characteristics:**

*   **Role:** Project-level governance, advisor, and router.
*   **Safety:** Strictly **NO-WRITE** (`write_guard: NO-WRITE`). It never modifies any project files, specs, or registries.
*   **Evidence-First:** Answers are derived only from existing project evidence, not inferred from simple checklists.
*   **Command-Correct:** It only recommends valid SmartSpec workflows and flags, preventing command hallucination.
*   **Category:** Utility.

## Usage

### CLI Usage

The copilot is invoked via the SmartSpec CLI, providing the user's question as the first argument.

```bash
/smartspec_project_copilot "<question>" \
  [--domain <name>] \
  [--spec-id <id>] \
  [--spec-path <path>] \
  [--aspect status|roadmap|security|ci|ui|perf|all] \
  [--report <path>] \
  [--format markdown|plain|json] \
  [--short] \
  [--repos-config <path>] \
  [--workspace-roots <root1,root2,...>] \
  [--registry-roots <dir1,dir2,...>] \
  [--out <safe_reports_root>] \
  [--json]
```

### Kilo Code Usage

When integrating the copilot into a Kilo Code environment (e.g., an IDE extension or platform), the `--kilocode` flag indicates the execution context.

```bash
/smartspec_project_copilot.md "<question>" --kilocode \
  [--domain <name>] [--spec-id <id>] [--spec-path <path>] [--aspect ...] \
  [--report <path>] [--format ...] [--short] \
  [--repos-config <path>] [--workspace-roots ...] [--registry-roots ...] \
  [--out <safe_reports_root>] \
  [--json]
```

## Use Cases

### Use Case 1: Checking Project Progress and Next Steps

**Scenario:** A project manager wants to know the current status of the `user-auth-v2` specification and what the immediate next steps should be.

**CLI Command:**

```bash
/smartspec_project_copilot "What is the status of the user-auth-v2 spec, and what should I do next?" \
  --spec-id user-auth-v2 \
  --aspect status
```

**Expected Result:**

The copilot scans the project, finds `specs/auth/user-auth-v2/spec.md`, and checks for associated `tasks.md` and reports.

1.  **Status Summary:** *The `user-auth-v2` specification is complete. Associated `tasks.md` exists but has not been verified since last week.*
2.  **Critical Issues:** *No critical issues found, but verification is stale.*
3.  **Recommended Workflows & Commands:**
    *   **To verify progress:** `/smartspec_verify_tasks_progress_strict specs/auth/user-auth-v2/tasks.md`
    *   **If verification fails:** `/smartspec_generate_code specs/auth/user-auth-v2/spec.md --language typescript`

### Use Case 2: Locating Security Vulnerabilities

**Scenario:** A security auditor needs a quick summary of any open security issues documented in reports or specifications, focusing on the `security` aspect.

**CLI Command:**

```bash
/smartspec_project_copilot "Are there any open security vulnerabilities or pending mitigations in the project?" \
  --aspect security \
  --format markdown
```

**Expected Result:**

The copilot scans `.spec/reports/**` for security-related reports and any `spec.md` files tagged with security concerns.

1.  **Status Summary:** *Two medium-severity findings are open: Insecure data transit (Report ID 456) and unpatched dependency (Report ID 789).*
2.  **Critical Issues:** *The unpatched dependency requires immediate attention.*
3.  **Recommended Workflows & Commands:**
    *   **To create a mitigation plan:** `/smartspec_generate_plan .spec/reports/security/report_789.json --type mitigation`
    *   **To update the dependency registry:** `/smartspec_update_registry --type dependencies --id vulnerable-lib`

### Use Case 3: Kilo Code Integration for Workflow Routing

**Scenario:** A developer using a Kilo-enabled IDE asks a general question about implementation progress.

**Kilo Code Command:**

```bash
/smartspec_project_copilot.md "Where are we on implementation? I don't see a tasks file." --kilocode
```

**Expected Result (Routing Rule Applied):**

Since the developer is unsure and no `tasks.md` path was provided, the mandatory routing rule for progress questions is triggered.

1.  **Status Summary:** *Cannot determine exact implementation progress without a verified task list.*
2.  **Critical Issues:** *Missing verifiable evidence for progress.*
3.  **Recommended Workflows & Commands:**
    *   **First, locate the relevant spec (e.g., `specs/feature/new_api/spec.md`).**
    *   **Then, generate tasks:** `/smartspec_generate_tasks specs/feature/new_api/spec.md --apply`
    *   **Finally, verify progress:** `/smartspec_verify_tasks_progress_strict specs/feature/new_api/tasks.md`

## Parameters

| Parameter/Flag | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| `<question>` | String | **MANDATORY.** The user's question or query for the copilot. | N/A |
| `--domain` | String | Filters the scope to a specific domain name. | All domains |
| `--spec-id` | String | Filters the scope to a specific specification ID. | All specs |
| `--spec-path` | Path | Filters the scope to a specific specification file path (e.g., `specs/auth/login/spec.md`). | All specs |
| `--aspect` | Enum | Narrows the focus of the answer. Valid values: `status`, `roadmap`, `security`, `ci`, `ui`, `perf`, `all`. | `all` |
| `--report` | Path | Directs the copilot to include a specific report file as primary evidence. | None |
| `--format` | Enum | Specifies the output format of the answer. Valid values: `markdown`, `plain`, `json`. | `markdown` |
| `--short` | Boolean | Requests a concise, brief answer. | False |
| `--repos-config` | Path | Path to the repository configuration file. | N/A |
| `--workspace-roots` | List[Path] | Comma-separated list of root directories to scan. | Current workspace |
| `--registry-roots` | List[Path] | Comma-separated list of directories containing read-only registries. | Default registries |
| `--out` | Path | Optional path for the orchestrator to write safe, temporary reports. | N/A |
| `--json` | Boolean | Output the entire result structure as JSON (overrides `--format`). | False |
| `--config` | Path | Path to the SmartSpec configuration file. | `.spec/smartspec.config.yaml` |
| `--lang` | Enum | Output language. Valid values: `en`, `th`, `auto`. | `auto` |
| `--platform` | Enum | Execution platform indicator. Valid values: `cli`, `kilo`, `ci`, `other`. | `cli` |
| `--quiet` | Boolean | Suppress non-essential output. | False |
| `--kilocode` | Boolean | Platform mode indicator (used in Kilo Code examples). | False |

## Output

The primary output is the advisory response, structured according to the mandatory layout:

1.  **Status summary:** A high-level overview of the scope.
2.  **Critical issues & remediation:** Any blocking problems found in the evidence.
3.  **Timeline / phased plan:** (Optional) A projected timeline based on existing plans/reports.
4.  **Recommended SmartSpec workflows & commands:** The most important section, providing verified, executable commands for the user's next action.
5.  **Weakness & Risk Check:** Transparency regarding any limitations (e.g., missing indexes, fallback behavior, redactions).

**Optional Persisted Output:**

If the orchestrator uses the `--out` flag