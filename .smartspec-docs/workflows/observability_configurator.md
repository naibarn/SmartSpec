# /smartspec_observability_configurator Manual (v6.0, English)

## Overview

The `/smartspec_observability_configurator` workflow (v6.1.1) is designed to generate a complete, best-effort observability configuration bundle based on project specifications (`spec.md`) and Non-Functional Requirements (NFRs).

**Purpose:** To generate configuration files for metrics (Prometheus/Otel), logs, tracing (Otel), alerts, SLO/SLA monitors, and dashboards, ensuring alignment with project specifications and security standards.

**Key Features:**

1.  **Preview-First:** By default, it only generates reports and preview artifacts (`bundle.preview/`).
2.  **Governed Writes:** Actual configuration writes to the runtime directory require explicit flags (`--apply` AND `--write-runtime-config`) and strict path validation.
3.  **Security Hardened:** Incorporates mandatory security hardening against path traversal, secret leakage, and ensures atomic writes.
4.  **Platform Agnostic:** Supports major observability platforms (OpenTelemetry, Prometheus, Datadog).

**Version Notes (v6.1.1):** This version fixes a flag collision, implements v6 hardening (path normalization, output root safety, atomic writes), introduces Change Plan artifacts, and replaces full-content previews with diffs/excerpts+hashes for security.

## Usage

### CLI Usage

The workflow is executed via the SmartSpec Command Line Interface (CLI).

**Syntax:**

```bash
/smartspec_observability_configurator [FLAGS]
```

#### Example: Previewing Configuration

To generate the observability configuration bundle for a specification, targeting OpenTelemetry, without applying any changes:

```bash
/smartspec_observability_configurator \
  --spec specs/api-gateway/v2/spec.md \
  --obs-platform opentelemetry \
  --out .spec/reports/obs-config-run-123 \
  --json
```

#### Example: Applying Configuration (Governed Write)

To write the generated configuration files to an approved target directory (`config/observability/`), required for deployment:

```bash
/smartspec_observability_configurator \
  --spec specs/api-gateway/v2/spec.md \
  --obs-platform opentelemetry \
  --target-dir config/observability/ \
  --write-runtime-config \
  --apply \
  --out .spec/reports/obs-config-run-124
```

### Kilo Code Usage

The workflow can be invoked within a SmartSpec Kilo Code file (e.g., a `.md` file used for orchestration).

**Syntax:**

```markdown
/smartspec_observability_configurator.md
  [FLAGS]
  --kilocode
```

#### Example: Kilo Code Invocation (Preview)

```bash
/smartspec_observability_configurator.md \
  --spec specs/inventory-service/spec.md \
  --obs-platform datadog \
  --max-items 50 \
  --out .spec/reports/inventory-obs-preview \
  --kilocode
```

## Use Cases

### Use Case 1: Generating Observability for a New Microservice (Preview Mode)

**Scenario:** A new `payment-processor` microservice is being developed. The team needs to generate Prometheus metrics configuration, standard logging guidance, and default dashboards based on the service's `spec.md` before deployment.

**Goal:** Generate a full preview bundle and a change plan without writing any files to the runtime configuration directory.

**Command (CLI):**

```bash
/smartspec_observability_configurator \
  --spec services/payment-processor/spec.md \
  --obs-platform prometheus \
  --nfr-summary .spec/reports/nfr-perf-verifier/run-001/summary.json \
  --out .spec/reports/payment-processor-obs-preview
```

**Expected Result:**

*   Exit code `0`.
*   A new directory `.spec/reports/payment-processor-obs-preview/` containing:
    *   `report.md` detailing generated components.
    *   `change_plan.md` showing the proposed files (e.g., `prometheus.yml` snippets, dashboard JSON).
    *   `bundle.preview/` containing the full generated configuration files.
    *   **Crucially:** No files written outside the report directory.

### Use Case 2: Applying Alert Configuration with a Custom Template

**Scenario:** The security team requires all services to use a standardized set of critical alerts defined in a custom JSON template (`security_alerts.json`). The generated configuration must be written to the approved target directory (`config/monitoring/`).

**Goal:** Generate configuration, incorporate the custom alert template (which must be sanitized), and apply the changes to the runtime configuration.

**Command (Kilo Code):**

```bash
/smartspec_observability_configurator.md \
  --spec specs/critical-service/spec.md \
  --obs-platform auto \
  --alert-template templates/security_alerts.json \
  --target-dir config/monitoring/ \
  --write-runtime-config \
  --apply \
  --kilocode
```

**Expected Result:**

*   The workflow runs mandatory checks (OBS-103 Template Sanitized).
*   Exit code `0`.
*   The generated configuration files (including the standardized alerts derived from the template) are written atomically under `config/monitoring/`.
*   `change_plan.md` confirms the files written to the governed location.

### Use Case 3: Strict Mode Validation

**Scenario:** A developer attempts to run the workflow but provides an invalid path for the target directory, violating the governance contract (`target-dir` is not in the allowlist).

**Goal:** The workflow must immediately hard-fail before any generation or writing occurs.

**Command (CLI):**

```bash
/smartspec_observability_configurator \
  --spec specs/my-service/spec.md \
  --obs-platform opentelemetry \
  --target-dir /tmp/unapproved-location/ \
  --write-runtime-config \
  --apply \
  --mode strict
```

**Expected Result:**

*   The workflow immediately fails during Section 4.3 (Governed target-dir rules).
*   Exit code `2` (Usage/config error).
*   An error message indicating that the provided `--target-dir` failed validation against the governance contract.

## Parameters

The following parameters (flags) are supported by the `/smartspec_observability_configurator` workflow:

| Flag | Category | Description | Required/Default |
| :--- | :--- | :--- | :--- |
| `--spec <path>` | Workflow | Path to `spec.md` or a specification folder used as input context. | Recommended |
| `--nfr-summary <path>` | Workflow | Optional path to performance/NFR evidence summary (e.g., from `nfr-perf-verifier`). | Optional |
| **`--obs-platform <platform>`** | Workflow | The target observability platform. | Default: `auto` |
| `--target-dir <path>` | Workflow | Target directory for governed runtime configuration writes. | Required for `--apply` |
| **`--write-runtime-config`** | Workflow | **Enables** governed writes to `--target-dir`. Must be used with `--apply`. | Optional (Gate) |
| `--dashboard-template <path>` | Workflow | Optional template input (JSON/YAML) for dashboard generation. | Optional |
| `--alert-template <path>` | Workflow | Optional template input (JSON/YAML) for alerts/monitors. | Optional |
| `--mode <normal|strict>` | Workflow | Sets the operational mode. `--strict` enforces stricter validation. | Default: `normal` |
| `--max-items <int>` | Workflow | Cap the number of generated dashboards or alerts. | Optional |
| `--config <path>` | Universal | Path to the SmartSpec configuration file. | Optional |
| `--lang <th|en>` | Universal | Output language for reports. | Optional |
| `--platform <cli|kilo|ci|other>` | Universal | Runtime mode (reserved for internal runtime detection). | Optional |
| **`--apply`** | Universal | Enables governed write operations (requires `--write-runtime-config` for this workflow). | Optional (Gate) |
| `--out <path>` | Universal | Requested base output root for reports and previews. Must be safe. | Optional |
| `--json` | Universal | Output reports and summaries in JSON format. | Optional |
| `--quiet` | Universal | Suppress non-essential output. | Optional |

## Output

The workflow produces two main types of output artifacts: safe reports/previews and governed runtime configuration files.

### Safe Output Artifacts (Always Written)

These are written to the unique run folder under the path specified by `--out` (default: `.spec/reports/observability-configurator/<run-id>/`).

| Artifact | Description |
| :--- | :--- |
| `report.md`