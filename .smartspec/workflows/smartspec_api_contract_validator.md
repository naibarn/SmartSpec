---
description: Validate API contracts and OpenAPI specifications.
version: 6.0.0
workflow: /smartspec_api_contract_validator
---

# smartspec_api_contract_validator

> **Version:** 6.1.1  
> **Status:** Proposed  
> **Category:** quality

## Purpose

Validate an API implementation against its defined contract (**OpenAPI v3 primary; GraphQL schema supported in limited mode—see Contract parsing rules**) to detect drift and ensure compliance.

This workflow performs static analysis of source code and contract files. It **does not** make live network calls to API endpoints.

It is a **reports-only** workflow, safe to run locally or in CI.

---

## Governance contract

This workflow MUST follow:

- `knowledge_base_smartspec_handbook.md` (v6)
- `.spec/smartspec.config.yaml`

### Write scopes (enforced)

Allowed writes (safe outputs only):

- Reports: `.spec/reports/api-contract-validation/**`

Forbidden writes (must hard-fail):

- Any path outside config `safety.allow_writes_only_under`
- Any path under config `safety.deny_writes_under`
- Any governed artifact (e.g., `specs/**`, `.spec/SPEC_INDEX.json`)
- Any runtime source tree modifications

### `--apply` behavior (universal flag)

- Accepted for compatibility with the universal flag contract.
- Must have **no effect** on write scopes.
- If provided, the workflow MUST note in the report header that `--apply` was ignored.

---

## Threat model (minimum)

This workflow must defend against:

- Path traversal / symlink escape on report writes or when reading source code/contracts.
- Secret leakage in reports (e.g., API keys, tokens found in contract examples or source code).
- Inaccurate results from parsing poorly-structured code or contracts.
- Accidental network usage (no external fetch).
- Runaway scans in large codebases (timeouts / CI cost spikes).

### Hardening requirements (MANDATORY)

- **No network access:** respect config `safety.network_policy.default=deny`.
- **No shell execution:** do not run arbitrary commands from inputs.
- **Path normalization (writes + reads):** reject traversal (`..`), absolute paths, and control characters on any user-supplied path.
- **No symlink escape:** do not read/write through symlinks that resolve outside allowed scopes.
- **Output root safety:** if `--out` is provided, it is a *requested* base root and MUST:
  - resolve under config `safety.allow_writes_only_under`
  - not fall under config `safety.deny_writes_under`
  - not be a runtime source folder
  - hard-fail with usage/config error (`exit 2`) if invalid
- **No remote refs / external fetch:** contract parsing MUST NOT fetch remote schemas; reject any `http(s)://` `$ref` or equivalent remote reference.
- **Timeouts & limits:** respect config `safety.content_limits` and bound scan scope.
- **Redaction:** respect config `safety.redaction` (patterns + secret file globs); never embed secrets in reports.
- **Excerpt policy:** do not paste large code/log dumps; reference file paths and symbols instead.
- **Output collision:** respect config `safety.output_collision` (never overwrite existing run folders).

---

## Invocation

### CLI

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

### Kilo Code

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

## Inputs

### Required

- `--contract <path>`: Path to the API contract file (e.g., OpenAPI v3 YAML/JSON, GraphQL schema).
- `--implementation-root <path>`: Path to the root directory of the API source code.

### Optional

- `--spec <spec.md>`: Scopes the validation against a specific spec for context.
- `--spec-id <id>`: Alternative to `--spec` when the project supports spec ID lookup.
- `--strict`: Fail the gate on any unmet MUST requirement (e.g., missing endpoint); otherwise, classify as warnings.
- `--out <path>`: Requested base output root (MUST pass Output root safety checks).

### Input validation (MANDATORY)

- `--contract` path must exist and be a valid, parsable API contract file.
- `--implementation-root` path must exist and be a directory.
- `--spec` (if provided) must exist and be a file.
- `--spec-id` (if provided) MUST match: `[a-z0-9_\-]{3,64}`.
- All paths must resolve within the project and not escape via symlinks.
- All user-supplied paths MUST reject traversal (`..`), absolute paths, and control characters.

### Contract parsing rules (MANDATORY)

- The workflow MUST NOT perform any network access while parsing contracts.

**OpenAPI `$ref` rules:**

- Reject remote refs (e.g., `http://`, `https://`).
- Allow only local file refs that resolve within the project root (no traversal, no symlink escape).

**GraphQL rules (limited mode):**

- Only schema parsing is guaranteed (Contract Parsable).
- REST-style endpoint coverage checks do not apply unless the project defines an explicit mapping (otherwise mark as `na` with rationale).

### Scan scope defaults (RECOMMENDED baseline)

Unless config overrides, the workflow SHOULD:

- ignore common vendor/build dirs: `node_modules/`, `dist/`, `build/`, `.git/`, `vendor/`, `.cache/`, `.next/`, `coverage/`
- enforce sane caps (and report them): max files, max bytes scanned, max depth, max time
- when limits are exceeded: emit a warning (or fail in `--strict` only if it invalidates MUST checks), and clearly state reduced coverage

---

## Flags

### Universal flags (must support)

- `--config <path>`
- `--lang <th|en>`
- `--platform <cli|kilo|ci|other>`
- `--apply` (ignored)
- `--out <path>`
- `--json`
- `--quiet`

### Workflow-specific flags

- `--contract <path>` (required)
- `--implementation-root <path>` (required)
- `--spec <path>` (optional)
- `--spec-id <id>` (optional)
- `--strict` (optional)

---

## Output structure

Outputs are always written under a run folder to prevent overwrites.

- Default root: `.spec/reports/api-contract-validation/<run-id>/...`
- If `--out` is provided, it is treated as a *requested* base output root and MUST pass Output root safety validation; otherwise `exit 2`.

### Exit codes

- `0`: Validation passed, or warnings were found (non-strict mode).
- `1`: Validation failed (strict mode) or a critical error occurred.
- `2`: Usage/config error (e.g., missing required flags, invalid/unsafe paths, disallowed remote refs).

---

## Checks (v6.1)

Each check MUST emit a stable ID (`ACV-xxx`).

### Preflight safety checks (always enforced)

- **ACV-000 Preflight Safety**: Validate paths, `--out` safety, and contract parsing rules (no remote refs, no network). Fail with `exit 2` on violation.

### MUST checks (fail in `--strict`)

- **ACV-001 Contract Parsable**: The `--contract` file is a valid and parsable OpenAPI/GraphQL document.
- **ACV-002 Endpoint Coverage**: Every path and method in the OpenAPI contract has a corresponding implementation found in the `--implementation-root`.
- **ACV-003 Path Parameter Mismatch**: The implementation of an endpoint correctly declares all path parameters defined in the OpenAPI contract.
- **ACV-004 Request Body Mismatch**: The implementation's request body handling aligns with the OpenAPI contract's `requestBody` schema (best-effort static analysis).

> Note: For GraphQL-only contracts, ACV-002..004 MAY be reported as `na` with a clear rationale unless the project provides an explicit mapping strategy.

### SHOULD checks (warn unless `--strict`)

- **ACV-101 Response Schema Drift**: The response objects returned in the code appear to be inconsistent with the response schemas in the contract (best-effort static analysis).
- **ACV-102 Missing Security Implementation**: Security schemes defined in the contract (e.g., `securitySchemes`) do not have corresponding middleware or handlers in the implementation.
- **ACV-103 Undocumented Endpoints**: Endpoints found in the implementation do not exist in the API contract.
- **ACV-104 Deprecation Mismatch**: An endpoint is marked as `deprecated` in the contract but the implementation does not reflect this (e.g., via logs or specific handling).

---

## Required content in `report.md`

The report MUST include:

1. **Summary**: Pass/Fail status, counts of endpoints checked, and number of errors/warnings.
2. **Scope**: Paths to the contract file, implementation root, and spec (if provided).
3. **Results Table**: A detailed table of all contract endpoints, their validation status, and a summary of findings.
4. **Error Details**: For each failure or warning, provide the endpoint, check ID, severity, and a clear rationale with file paths and line numbers where possible.
5. **Evidence Sources**: Which files were inspected.
6. **Recommended Next Commands**:
   - Recommend next steps that are guaranteed to exist in your project registry (`.spec/WORKFLOWS_INDEX.yaml`).
   - If suggesting a SmartSpec workflow, include both CLI + Kilo forms.
   - Safe default suggestions:
     - regenerate/confirm SPEC/contract alignment (update spec/contract)
     - run the standard implementation prompter (if the project uses it)

Example (if applicable):

CLI:
`/smartspec_report_implement_prompter --spec <spec.md> --tasks <tasks.md> --out <dir> --json`

Kilo:
`/smartspec_report_implement_prompter.md --spec <spec.md> --tasks <tasks.md> --out <dir> --json`

---

## `summary.json` schema (minimum)

```json
{
  "workflow": "smartspec_api_contract_validator",
  "version": "6.1.1",
  "run_id": "string",
  "status": "pass|fail|warn",
  "strict": true,
  "scope": {
    "contract_path": "...",
    "implementation_root": "...",
    "spec_id": "string|null"
  },
  "results": [
    {
      "check_id": "ACV-002",
      "endpoint": "POST /users",
      "status": "fail",
      "severity": "high",
      "why": "Endpoint defined in contract but no implementation found.",
      "details": null
    }
  ],
  "writes": {"reports": ["path"]},
  "next_steps": [{"cmd": "...", "why": "..."}]
}
```

---

# End of workflow doc

