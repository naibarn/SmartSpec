# /smartspec_api_contract_validator Manual (v6.0, English)

## Overview

The `/smartspec_api_contract_validator` workflow is designed to validate an API implementation against its defined contract (primarily **OpenAPI v3**; **GraphQL schema** is supported in a limited mode).

**Purpose:** To detect **API drift** by statically analyzing source code and contract files, ensuring that the implemented API adheres strictly to the agreed-upon specification.

**Key Features:**
*   **Non-intrusive:** Performs static analysis only; no live network calls are made.
*   **Reports-Only:** Safe to run in local development or CI/CD pipelines.
*   **Strict Governance:** Enforces mandatory hardening requirements, including path safety and network denial.

**Version:** 6.1.1

---

## Usage

### CLI Usage

The workflow is executed directly via the command-line interface, requiring the contract path and the root of the implementation source code.

```bash
/smartspec_api_contract_validator \
  --contract <path/to/openapi.yaml> \
  --implementation-root <path/to/src> \
  [--spec <path/to/spec.md>] \
  [--spec-id <id>] \
  [--out <output-root>] \
  [--json] \
  [--strict]
```

### Kilo Code Usage

For integration within SmartSpec's declarative environment (e.g., in a `.spec/workflow.kilo` file), use the Kilo Code invocation format.

```bash
/smartspec_api_contract_validator.md \
  --contract <path/to/openapi.yaml> \
  --implementation-root <path/to/src> \
  [--spec <path/to/spec.md>] \
  [--spec-id <id>] \
  [--out <output-root>] \
  [--json] \
  [--strict]
```

---

## Use Cases

### Use Case 1: Standard API Drift Check in CI

**Scenario:** A development team wants to ensure that a recent commit to the `api/src` directory did not introduce any endpoints or parameter changes that violate the official `openapi.yaml` contract. The validation should fail the build if any critical MUST checks are violated.

**Goal:** Run a strict validation and output results to the default report directory.

**CLI Command:**

```bash
/smartspec_api_contract_validator \
  --contract ./specs/v1/openapi.yaml \
  --implementation-root ./api/src \
  --strict
```

**Expected Result:**
*   If all MUST checks (ACV-001 to ACV-004) pass, exit code is `0`. Warnings (SHOULD checks) are reported but do not cause failure.
*   If an endpoint from `openapi.yaml` is missing in `./api/src` (ACV-002), the workflow exits with code `1` due to the `--strict` flag.
*   A detailed report is generated under `.spec/reports/api-contract-validation/<run-id>/report.md`.

### Use Case 2: Scoped Validation with Custom Output

**Scenario:** A technical writer is validating the API implementation for a specific feature documented in `user_onboarding.md`. They need the output in JSON format for automated parsing and want to store the report in a temporary directory.

**Goal:** Validate against the contract, link the results to a specific spec document, and output JSON to a custom, safe location.

**Kilo Code Invocation:**

```bash
/smartspec_api_contract_validator.md \
  --contract ./specs/v2/api.json \
  --implementation-root ./services/onboarding \
  --spec ./docs/user_onboarding.md \
  --out ./temp/validation_results \
  --json
```

**Expected Result:**
*   The workflow performs validation, using the `user_onboarding.md` spec path for context in the report.
*   The output artifacts (`report.md`, `summary.json`) are written under `./temp/validation_results/<run-id>/`.
*   The primary output is the `summary.json` file, containing structured validation results.
*   The workflow validates that `./temp/validation_results` adheres to the **Output root safety** requirements.

### Use Case 3: GraphQL Schema Check

**Scenario:** The project uses GraphQL. The team needs to ensure the service implementation correctly exposes the types defined in the GraphQL schema, understanding that REST-specific checks will be marked as not applicable (`na`).

**Goal:** Validate the implementation against the GraphQL schema.

**CLI Command:**

```bash
/smartspec_api_contract_validator \
  --contract ./schema/graphql.sdl \
  --implementation-root ./graphql/resolvers \
  --quiet
```

**Expected Result:**
*   Check **ACV-001 (Contract Parsable)** confirms the schema is valid.
*   Checks ACV-002, ACV-003, and ACV-004 are reported as `na` in the report, with a rationale stating that REST-style endpoint coverage checks are not applicable without an explicit mapping strategy.
*   The report focuses on structural drift and type definition consistency (best-effort static analysis).

---

## Parameters

The following parameters (flags) are supported by the workflow:

| Flag | Category | Description | Mandatory | Validation/Notes |
| :--- | :--- | :--- | :--- | :--- |
| `--contract <path>` | Workflow-Specific | Path to the API contract file (OpenAPI, GraphQL schema). | Yes | Must exist and be parsable. No remote refs allowed. |
| `--implementation-root <path>` | Workflow-Specific | Path to the root directory of the API source code. | Yes | Must exist and be a directory. |
| `--spec <path>` | Workflow-Specific | Scopes the validation against a specific spec document for context. | No | Must exist if provided. |
| `--spec-id <id>` | Workflow-Specific | Alternative to `--spec` for projects using spec ID lookup. | No | Must match regex `[a-z0-9_\-]{3,64}`. |
| `--strict` | Workflow-Specific | If set, the workflow fails (exit code 1) on any unmet MUST requirement (ACV-001 to ACV-004). | No | Default behavior is to classify MUST violations as warnings. |
| `--out <path>` | Universal | Requested base output root. | No | Must pass **Output root safety** checks. Default: `.spec/reports/api-contract-validation/`. |
| `--config <path>` | Universal | Path to the SmartSpec configuration file. | No | |
| `--lang <th|en>` | Universal | Language preference for reports. | No | |
| `--platform <cli|kilo|ci|other>` | Universal | Contextual platform identifier. | No | |
| `--apply` | Universal | Accepted for compatibility but has **no effect** (ignored). | No | |
| `--json` | Universal | Output the primary summary in JSON format (`summary.json`). | No | |
| `--quiet` | Universal | Suppress non-critical output to stdout/stderr. | No | |

---

## Output

The workflow generates output artifacts within a unique run folder to prevent collision.

**Default Output Root:**
`.spec/reports/api-contract-validation/<run-id>/`

If `--out <path>` is provided, the output is rooted there, provided the path is safe and valid.

### Output Artifacts

1.  **`report.md` (Mandatory)**
    A human-readable report containing:
    *   Summary (Pass/Fail status, counts).
    *   Scope details (contract path, root path).
    *   A detailed results table of all contract endpoints and their validation status.
    *   Detailed error explanations, including check ID, severity, file paths, and line numbers.
    *   Recommended next steps (SmartSpec commands).

2.  **`summary.json` (If `--json` is used)**
    A machine-readable summary following the defined schema, useful for CI/CD integration and automated parsing.

### Exit Codes

| Code | Meaning | Condition |
| :--- | :--- | :--- |
| `0` | Success | Validation passed, or only warnings were found (non-strict mode). |
| `1` | Failure | Validation failed due to a critical error or a MUST check failure in `--strict` mode. |
| `2` | Usage/Config Error | Invalid invocation, missing required flags, unsafe path usage, or violation of governance rules (e.g., remote reference in contract). |

---

## Notes & Related Workflows

### Contract Parsing Limitations

*   **No Network Access:** The workflow strictly enforces network denial during contract parsing. Remote `$ref` references (e.g., `http://`, `https://`) in OpenAPI specifications will cause a hard failure (`exit 2`). Only local file references are permitted, provided they resolve safely within the project.
*   **GraphQL Support:** GraphQL validation