| manual_name | manual_version | compatible_workflow | compatible_workflow_versions |
|-------------|----------------|---------------------|------------------------------|
| /smartspec_deployment_planner Manual (EN) | 6.0 | /smartspec_deployment_planner | 6.0.x |

# /smartspec_deployment_planner Manual (v6.0, English)

## 1. Overview

The `/smartspec_deployment_planner` workflow generates deployment plans from specifications and implementation tasks.

**Purpose:** Generate deployment plans from specifications, defining deployment strategies, rollout phases, and rollback procedures.

**Version:** 6.0  
**Category:** operations-deployment

---

## 2. Usage

### 🔗 CLI Usage

```bash
/smartspec_deployment_planner \
  <spec_md> \
  [--strategy <blue-green|canary|rolling>] \
  [--apply]
```

### Kilo Code Usage

**Important:** When using Kilo Code, you MUST include `--platform kilo` flag.

```bash
/smartspec_deployment_planner.md \
  <spec_md> \
  [--strategy <blue-green|canary|rolling>] \
  [--apply] \
  --platform kilo
```

---

## 3. Use Cases

### Use Case 1: Generating Deployment Plan (CLI)

**Scenario:** Generate deployment plan for new API.

**Command:**

```bash
/smartspec_deployment_planner specs/api/v2_endpoints/spec.md \
  --strategy blue-green
```

**Expected Result:**

1. Deployment plan generated.
2. Exit code `0` (Success).

### Use Case 2: Canary Deployment (Kilo Code)

**Scenario:** Plan canary deployment strategy.

**Command (Kilo Code Snippet):**

```bash
/smartspec_deployment_planner.md \
  specs/services/recommendation/spec.md \
  --strategy canary \
  --apply \
  --platform kilo
```

**Expected Result:**

1. Canary deployment plan generated and saved.
2. Exit code `0` (Success).

### Use Case 3: Rolling Deployment (CLI)

**Scenario:** Plan rolling deployment.

**Command:**

```bash
/smartspec_deployment_planner specs/frontend/dashboard/spec.md \
  --strategy rolling \
  --json
```

**Expected Result:**

1. Rolling deployment plan with JSON output.
2. Exit code `0` (Success).

---

## 4. Parameters

### Required Parameters

| Parameter | Type | Description | Validation |
| :--- | :--- | :--- | :--- |
| `<spec_md>` | `<path>` | Path to spec.md file. | Must resolve under `specs/**`. |

### Universal Flags

| Flag | Description | Default | Platform Support |
| :--- | :--- | :--- | :--- |
| `--platform` | Execution platform. **Required for Kilo Code.** | (Inferred) | `cli` \| `kilo` \| `ci` \| `other` |
| `--apply` | Save deployment plan. | `false` | `cli` \| `kilo` \| `ci` \| `other` |
| `--json` | Output in JSON format. | `false` | `cli` \| `kilo` \| `ci` \| `other` |

### Workflow-Specific Flags

| Flag | Description | Default | Platform Support |
| :--- | :--- | :--- | :--- |
| `--strategy` | Deployment strategy: `blue-green`, `canary`, `rolling`. | `rolling` | `cli` \| `kilo` \| `ci` \| `other` |

---

## 5. Output

### Output Files

| File Path | Description |
| :--- | :--- |
| `.spec/reports/deployment-planner/<run-id>/deployment_plan.md` | Deployment plan. |
| `specs/**/deployment/plan.md` | Saved deployment plan (with `--apply`). |

---

## 6. Notes

- **Platform Flag:** When using Kilo Code, always include `--platform kilo`.

---

**End of Manual**
