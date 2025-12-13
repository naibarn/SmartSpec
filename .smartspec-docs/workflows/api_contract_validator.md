| manual_name | manual_version | compatible_workflow | compatible_workflow_versions |
|-------------|----------------|---------------------|------------------------------|
| /smartspec_api_contract_validator Manual (EN) | 6.0 | /smartspec_api_contract_validator | 6.0.x |

# /smartspec_api_contract_validator Manual (v6.0, English)

## 1. Overview

The `/smartspec_api_contract_validator` workflow validates API contracts against specifications and ensures compliance with defined interfaces.

**Purpose:** Validate API contracts against specifications, ensuring endpoints, parameters, and responses match defined interfaces.

**Version:** 6.0  
**Category:** quality-testing

---

## 2. Usage

### 🔗 CLI Usage

```bash
/smartspec_api_contract_validator \
  <spec_md> \
  [--contract-file <path>] \
  [--strict]
```

### Kilo Code Usage

**Important:** When using Kilo Code, you MUST include `--platform kilo` flag.

```bash
/smartspec_api_contract_validator.md \
  <spec_md> \
  [--contract-file <path>] \
  [--strict] \
  --platform kilo
```

---

## 3. Use Cases

### Use Case 1: Validating API Contract (CLI)

**Scenario:** A developer needs to validate that API implementation matches the contract.

**Command:**

```bash
/smartspec_api_contract_validator specs/api/rest_endpoints/spec.md \
  --contract-file api/openapi.yaml
```

**Expected Result:**

1. The workflow loads spec and contract files.
2. It validates endpoints, parameters, and responses.
3. A validation report is generated.
4. Exit code `0` if valid, `1` if violations found.

### Use Case 2: Strict Validation Mode (Kilo Code)

**Scenario:** A CI pipeline requires strict contract validation.

**Command (Kilo Code Snippet):**

```bash
/smartspec_api_contract_validator.md \
  specs/api/graphql/spec.md \
  --strict \
  --platform kilo
```

**Expected Result:**

1. Strict validation is performed.
2. Any discrepancies cause failure.
3. Exit code `0` if perfect match, `1` if any issues.

### Use Case 3: JSON Output for Integration (CLI)

**Scenario:** Integration with external tools requires JSON output.

**Command:**

```bash
/smartspec_api_contract_validator specs/api/webhooks/spec.md \
  --json
```

**Expected Result:**

1. Validation is performed.
2. Output includes `validation.json` with structured results.
3. Exit code `0` (Success).

---

## 4. Parameters

### Required Parameters

| Parameter | Type | Description | Validation |
| :--- | :--- | :--- | :--- |
| `<spec_md>` | `<path>` | Path to spec.md file. | Must resolve under `specs/**`. |

### Universal Flags

| Flag | Description | Default | Platform Support |
| :--- | :--- | :--- | :--- |
| `--config` | Path to configuration file. | `.spec/smartspec.config.yaml` | `cli` \| `kilo` \| `ci` \| `other` |
| `--platform` | Execution platform. **Required for Kilo Code.** | (Inferred) | `cli` \| `kilo` \| `ci` \| `other` |
| `--json` | Output in JSON format. | `false` | `cli` \| `kilo` \| `ci` \| `other` |

### Workflow-Specific Flags

| Flag | Description | Default | Platform Support |
| :--- | :--- | :--- | :--- |
| `--contract-file` | Path to API contract file (OpenAPI, GraphQL schema, etc.). | (Auto-detect) | `cli` \| `kilo` \| `ci` \| `other` |
| `--strict` | Enable strict validation mode. | `false` | `cli` \| `kilo` \| `ci` \| `other` |

---

## 5. Output

### Output Files

| File Path | Description |
| :--- | :--- |
| `.spec/reports/api-contract-validator/<run-id>/validation.md` | Validation report. |

---

## 6. Notes

- **Platform Flag:** When using Kilo Code, always include `--platform kilo`.
- **Strict Mode:** Use `--strict` for zero-tolerance validation.

---

**End of Manual**
