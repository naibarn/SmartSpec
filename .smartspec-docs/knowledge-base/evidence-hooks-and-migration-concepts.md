> **Key Insight:** Standardized evidence hooks are the backbone of automated verification in SmartSpec. They transform human-readable descriptions into machine-verifiable facts, enabling workflows like `/smartspec_verify_tasks_progress_strict` to function.

## 1. The Evolution of Evidence in SmartSpec

To understand the importance of `smartspec_migrate_evidence_hooks`, it's crucial to see the journey of how "evidence" has been defined within SmartSpec.

### Phase 1: Descriptive Evidence (Legacy)

In early versions, the `Evidence` field in `tasks.md` was a free-form text description. Its purpose was to guide a human developer or reviewer.

**Example:**
```markdown
| **Task:** Create the user login endpoint. |
| **Evidence:** A POST route should exist at /api/v1/auth/login. |
```

**Limitations:**
-   **Not Machine-Readable:** An AI or a script cannot programmatically check if this condition is met.
-   **Ambiguous:** "should exist" can be interpreted in various ways.
-   **Blocks Automation:** This approach makes fully automated task verification impossible.

### Phase 2: Standardized Evidence Hooks (Modern)

To enable true automation and governance, SmartSpec introduced **evidence hooks**. These are structured, machine-readable strings that follow a consistent format: `evidence: <type> [key=value]...`

**Example:**
```markdown
| **Task:** Create the user login endpoint. |
| **Evidence:** evidence: api_route method=POST path=/api/v1/auth/login |
```

**Advantages:**
-   **Machine-Readable:** A verification script can parse this hook, make an API call or check a file, and return a `true`/`false` result.
-   **Unambiguous:** The intent is explicit and precise.
-   **Enables Automation:** This is the key that unlocks workflows like `/smartspec_verify_tasks_progress_strict`.

## 2. The Migration Challenge

Many long-running projects using SmartSpec have hundreds or thousands of tasks with legacy descriptive evidence. Manually converting them to the new hook format is:

-   **Time-Consuming:** A developer would need to read each task and manually write the correct hook.
-   **Error-Prone:** It's easy to make typos in paths, method names, or table identifiers.
-   **A Barrier to Modernization:** The sheer effort required often prevents teams from adopting newer, more powerful verification workflows.

## 3. The Solution: `/smartspec_migrate_evidence_hooks`

This workflow was created specifically to solve the migration challenge. It uses AI to bridge the gap between human language and machine-readable hooks.

### Core Functionality

1.  **AI-Powered Parsing:** It analyzes the context of the task (`TSK-ID`, `Description`) and the natural language `Evidence` text.
2.  **Intelligent Hook Selection:** The AI determines the most appropriate hook type (e.g., `file_exists`, `db_schema`, `api_route`).
3.  **Precise Parameter Extraction:** It extracts the necessary parameters (e.g., `path`, `table`, `column`, `method`).
4.  **Safe Preview Mode:** By default, it only shows a `diff` of the proposed changes, allowing for human review before any files are modified.
5.  **Automated Application:** The `--apply` flag allows for in-place updates to the `tasks.md` file, automating the entire conversion process.

### Example Transformation

| Before (Legacy) | After (Modern, via AI) |
| :--- | :--- |
| `The database schema for 'users' must include an 'email_verified_at' timestamp.` | `evidence: db_schema table=users column=email_verified_at` |
| `Check that the main config file has a key for the JWT secret.` | `evidence: config_key file=config/app.json key=jwt_secret` |
| `The main entrypoint for the React app should be at src/index.tsx.` | `evidence: file_exists path=src/index.tsx` |

## 4. Problem/Solution Mapping

This table explicitly maps common problems to the solution provided by this workflow.

| Problem | Bad Solution (Manual) | Good Solution (Automated) |
| :--- | :--- | :--- |
| **Descriptive Evidence** | Manually rewrite each line. | `/smartspec_migrate_evidence_hooks` |
| **TODO Placeholders** | Find and replace all TODOs. | `/smartspec_migrate_evidence_hooks` |
| **Low Verification Score** | Manually debug each "Not verified" task. | `/smartspec_migrate_evidence_hooks` to fix formats, then re-run verification. |
| **Inconsistent Paths** | Manually correct every path. | `/smartspec_migrate_evidence_hooks` (The AI is trained to infer correct root-relative paths). |

## 5. Architectural Impact

By automating this migration, `/smartspec_migrate_evidence_hooks` provides a critical service with significant architectural impact:

-   **Unlocks Automated Governance:** It's the entry point to using the strict verification ecosystem.
-   **Improves Data Quality:** It standardizes project metadata, making it more reliable and consistent.
-   **Reduces Technical Debt:** It helps clear legacy cruft from `tasks.md` files, making them cleaner and more maintainable.
-   **Accelerates Modernization:** It removes the primary blocker for teams wanting to adopt modern SmartSpec practices.

In summary, this workflow is not just a utility; it's a strategic tool for ensuring the long-term health, verifiability, and automation potential of any SmartSpec-driven project.
