# SmartSpec Workflow: API Contract Validator

**Workflow:** `/smartspec_api_contract_validator`  
**Version:** 6.1.1

## 1. Overview

The API Contract Validator is a static analysis workflow that ensures your API implementation complies with its defined contract (e.g., OpenAPI v3). It detects "API drift"—where the code no longer matches the documentation—by comparing the source code against the contract file.

This workflow is a **reports-only** tool, meaning it is safe to run locally or in CI pipelines as it does not modify code or make live network calls.

## 2. Key Features

- **Drift Detection:** Identifies discrepancies between the API contract and the implementation.
- **Static Analysis:** Validates compliance without running the application or making network requests.
- **Multi-Contract Support:** Primarily supports OpenAPI v3, with limited support for GraphQL schemas.
- **Secure and Isolated:** Operates without network access and redacts secrets from reports.
- **CI/CD Friendly:** Designed to be a fast, reliable gate in your continuous integration pipeline.

## 3. How It Works

The workflow performs a series of checks, categorized as **MUST** (critical) and **SHOULD** (warnings):

1.  **Parses Inputs:** Reads the API contract and scans the implementation source code.
2.  **Endpoint Coverage:** Verifies that every endpoint in the contract is implemented in the code.
3.  **Parameter Matching:** Ensures path parameters in the code match the contract.
4.  **Request/Response Validation:** Statically analyzes request bodies and response objects for inconsistencies.
5.  **Undocumented Endpoints:** Flags any endpoints found in the code that are not defined in the contract.
6.  **Generates Report:** Produces a detailed `report.md` and `summary.json` with all findings.

## 4. Usage

### Command Line

```bash
/smartspec_api_contract_validator \
  --contract path/to/openapi.yaml \
  --implementation-root path/to/src \
  --strict
```

### Kilo Code

```bash
/smartspec_api_contract_validator.md \
  --contract path/to/openapi.yaml \
  --implementation-root path/to/src \
  --strict
```

## 5. Input and Flags

- **`--contract <path>` (Required):** Path to the API contract file (OpenAPI or GraphQL).
- **`--implementation-root <path>` (Required):** Path to the API source code directory.
- **`--strict` (Optional):** Fails the workflow (exit code 1) on any MUST-level violation. If omitted, violations are reported as warnings.
- **`--spec <spec.md>` (Optional):** Scopes the validation against a specific `spec.md` for additional context.
- **`--json` (Optional):** Outputs the report in JSON format.

## 6. Output: Validation Report

The workflow generates a detailed report in `.spec/reports/api-contract-validation/` containing:

- **Summary:** Pass/Fail status and a count of errors and warnings.
- **Scope:** Paths to the contract and source code that were analyzed.
- **Results Table:** A list of all endpoints and their validation status.
- **Error Details:** For each finding, it provides the check ID (e.g., `ACV-002`), severity, and a clear explanation with file paths and line numbers.

### Example Report Snippet

```markdown
### ACV-002: Endpoint Not Implemented

- **Severity:** High (FAIL in --strict mode)
- **Endpoint:** `POST /users`
- **Finding:** The endpoint is defined in `openapi.yaml` but no corresponding implementation was found in the `src/` directory.
```

## 7. Use Cases

- **Prevent Breaking Changes:** Catch unintended changes to the API before they reach production.
- **Maintain Documentation Quality:** Ensure API documentation is always synchronized with the code.
- **Automated Governance:** Enforce API standards and consistency across all microservices.
