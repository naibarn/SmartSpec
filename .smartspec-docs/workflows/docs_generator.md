# /smartspec_docs_generator Manual (v6.0, English)

## Overview

The `/smartspec_docs_generator` workflow (v6.1.1) is designed to generate comprehensive project documentation bundles, including API documentation, user guides, and architecture diagrams, by leveraging signals from specifications, registries, and code sources.

**Purpose:** Generate project documentation bundles (API docs, user guide, architecture diagrams) from spec/registry/code signals.

**Key Features:**

1.  **Preview-First:** By default, the workflow operates in preview mode, writing reports only to `.spec/reports/docs-generator/**`.
2.  **Governed Writes:** Writing documentation files directly into the repository (e.g., `docs/`) requires explicit opt-in using the `--apply` and `--write-docs` flags, ensuring compliance with the defined governance contract.
3.  **Security Hardening:** Includes mandatory path normalization, no symlink escape, output root safety, atomic writes, and strict network/external tool policies.

**Supported Modes:**
*   `api-docs`: Generates API reference documentation.
*   `user-guide`: Generates flows, setup, and troubleshooting guides.
*   `architecture-diagram`: Generates diagram source files and rendered outputs (best-effort).

**Version Notes (v6.1.1):** Adds v6 hardening (path normalization, output safety, atomic writes), replaces full previews with change plans/diffs, introduces explicit `--write-docs` gate, and enforces network/external tool policies.

## Usage

### CLI Usage

The CLI is the primary interface for invoking the workflow.

#### Preview Mode (Reports Only)

This is the default safe mode. It generates all documentation artifacts into a preview bundle within the report directory and creates a detailed change plan, but does not modify the source documentation directory.

```bash
/smartspec_docs_generator \
  --mode api-docs \
  --spec specs/api/auth-service/spec.md \
  --out .spec/reports/docs-generator/api-doc-run-1 \
  --json
```

#### Apply Mode (Governed Writes)

To write generated documentation files to the target repository directory (e.g., `docs/`), you must explicitly enable the governance gates: `--apply` and `--write-docs`.

```bash
/smartspec_docs_generator \
  --mode user-guide \
  --spec specs/user/onboarding/spec.md \
  --target-dir docs/guides \
  --write-docs \
  --apply \
  --out .spec/reports/docs-generator/user-guide-apply-run \
  --config .spec/smartspec.config.yaml
```

### Kilo Code Usage

Kilo Code allows invoking the workflow within a controlled, declarative environment.

```python
# In a Kilo Code file (.kilocode)
/smartspec_docs_generator.md \
  --mode architecture-diagram \
  --spec specs/arch/data-pipeline/spec.md \
  --out .spec/reports/docs-generator/arch-diagram-preview \
  --json \
  --kilocode
```

## Use Cases

### Use Case 1: Generating API Documentation (Preview)

**Scenario:** A developer needs to review the generated OpenAPI reference documentation for a new microservice specification before committing the output to the main documentation branch.

**Goal:** Generate `api-docs` preview bundle and change plan without writing to the `docs/` directory.

**CLI Command:**

```bash
/smartspec_docs_generator \
  --mode api-docs \
  --spec specs/services/payment-gateway/spec.md \
  --schema-source http://internal.schema.svc/payment-api.json \
  --allow-network \
  --out .spec/reports/docs-generator/payment-api-preview \
  --json
```

**Expected Result:**

1.  A new report folder is created: `.spec/reports/docs-generator/payment-api-preview/`.
2.  The report contains `summary.json`, `report.md`, and `change_plan.md`.
3.  The `bundle.preview/` directory contains the generated API documentation files (e.g., `api-reference.md`).
4.  The `summary.json` shows `mode: preview` and `status: ok`.
5.  Check **DOC-002 Network Gate** passes (due to `--allow-network`).

### Use Case 2: Applying a Generated User Guide

**Scenario:** The SmartSpec team has finalized the user onboarding flow specification and needs to commit the generated user guide directly to the `docs/` folder in the repository.

**Goal:** Generate and atomically write the `user-guide` documentation to `docs/user-guides/`.

**CLI Command:**

```bash
/smartspec_docs_generator \
  --mode user-guide \
  --spec specs/flows/onboarding/spec.md \
  --target-dir docs/user-guides \
  --write-docs \
  --apply \
  --out .spec/reports/docs-generator/onboarding-apply
```

**Expected Result:**

1.  The workflow validates that `--apply` and `--write-docs` are set, enabling governed writes.
2.  The workflow validates that `docs/user-guides` is an allowed target directory.
3.  The generated user guide files are written atomically (temp+rename) into `docs/user-guides/`.
4.  The `summary.json` reports `mode: apply`, `files_to_write: N`, and checks **DOC-001 Apply Gate** and **DOC-202 Atomic Writes** pass.

### Use Case 3: Generating Architecture Diagrams (Kilo Code)

**Scenario:** A CI pipeline step, defined in Kilo Code, needs to generate architecture diagram source files based on a specification, enforcing strict quality limits.

**Goal:** Generate `architecture-diagram` preview, enforcing a maximum output size limit.

**Kilo Code Invocation:**

```python
# Invoked via CI system
/smartspec_docs_generator.md \
  --mode architecture-diagram \
  --spec specs/arch/microservices/spec.md \
  --max-bytes 524288 \
  --strict \
  --out .spec/reports/docs-generator/microservices-arch \
  --kilocode
```

**Expected Result:**

1.  The architecture diagram source and rendered output preview are generated in the report directory.
2.  If the generated output exceeds 524288 bytes (512 KB), the workflow emits check **DOC-204 Reduced Coverage** (limits hit) and potentially exits with code 1 if the `--strict` mode deems the reduced coverage a failure.
3.  The report confirms that external tool policies (DOC-203) were followed for diagram rendering.

## Parameters

The following parameters (flags) control the behavior and inputs of the `/smartspec_docs_generator` workflow.

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `--mode` | `<api-docs\|user-guide\|architecture-diagram>` | Yes | Defines the type of documentation to generate. |
| `--spec` | `<path>` | No | Path to the primary specification file (e.g., `specs/<category>/<spec-id>/spec.md`). |
| `--tasks` | `<path>` | No | Optional tasks context (read-only). |
| `--registry-roots` | `<csv>` | No | Optional override for registry root paths. |
| `--index` | `<path>` | No | Optional index override path. |
| `--template` | `<path>` | No | Optional docs template path (md/yaml/json). |
| `--schema-source` | `<path\|url>` | No | Optional source for OpenAPI/GraphQL schema. |
| `--allow-network` | `(flag)` | No | Required if `--schema-source` is a URL, enables network access for fetching remote schemas. |
| `--target-dir` | `<path>` | No (Required for apply) | Destination directory for docs when applying (e.g., `docs/`). Canonical name. |
| `--write-docs` | `(flag)` | No (Required for apply) | **Governed gate.** Enables writes to `--target-dir` (requires `--apply`). |
| `--max-pages` | `<int>` | No | Bounding limit: maximum number of output pages/files. |
| `--max-bytes` | `<int>` | No | Bounding limit: maximum total size of generated output. |
| `--max-seconds` | `<int>` | No | Bounding limit: maximum time allowed for generation. |
| `--mode` | `<normal\|strict>` | No | Content quality mode (default `normal`). |
| `--strict` | `(flag)` | No | Alias for `--mode strict`. |
| `--config` | `<path>` | No | Path to the SmartSpec configuration file. |
| `--lang` | `<th\|en>` | No | Language for generated content/