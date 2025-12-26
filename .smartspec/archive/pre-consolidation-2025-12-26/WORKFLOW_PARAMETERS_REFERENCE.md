# SmartSpec Workflow Parameters Reference (v6.2.0)

This document provides a comprehensive reference for all parameters used in the 40 SmartSpec workflows. Each entry includes a description, version, parameter details, and usage examples.

---

## smartspec_api_contract_validator

**Description:** Validate API contracts and OpenAPI specifications.

**Version:** 6.0.0

### Universal Flags (Supported)

These flags are supported by this workflow:
`--apply`, `--json`, `--quiet`

### Usage Examples

**CLI:**
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

**Kilo Code:**
```bash
/smartspec_api_contract_validator.md \
  --contract <path/to/openapi.yaml> \
  --implementation-root <path/to/src> \
  [--spec <path/to/spec.md>] \
  [--spec-id <id>] \
  [--out <output-root>] \
  [--json] \
  [--strict] \
  --platform kilo
```

---

## smartspec_code_assistant

**Description:** Consolidated implementation helper (implement/fix/refactor) producing

**Version:** 6.0.0

### Universal Flags (Supported)

These flags are supported by this workflow:
`--apply`, `--json`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_code_assistant \
  --mode <implement|fix|refactor> \
  [--spec <path/to/spec.md>] \
  [--tasks <path/to/tasks.md>] \
  [--context <path/to/log-or-error.txt>] \
  [--out <output-root>] \
  [--json]
```

**Kilo Code:**
```bash
/smartspec_code_assistant.md \
  --mode <implement|fix|refactor> \
  [--spec <path/to/spec.md>] \
  [--tasks <path/to/tasks.md>] \
  [--context <path/to/log-or-error.txt>] \
  [--out <output-root>] \
  [--json] \
  --platform kilo
```

---

## smartspec_data_migration_generator

**Description:** Generate data migration scripts and documentation.

**Version:** 6.0.0

### Universal Flags (Supported)

These flags are supported by this workflow:
`--apply`, `--json`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_data_migration_generator \
  --report <path/to/validation-report.json> \
  --migration-tool <flyway|liquibase|raw-sql> \
  --output-dir <path/to/migrations> \
  [--allow-destructive] \
  [--apply]
```

**Kilo Code:**
```bash
/smartspec_data_migration_generator.md \
  --report .spec/reports/data-model-validation/<run-id>/summary.json \
  --migration-tool flyway \
  --output-dir db/migrations \
  --platform kilo
```

---

## smartspec_data_model_validator

**Description:** Validate data models and database schemas.

**Version:** 6.0.0

### Universal Flags (Supported)

These flags are supported by this workflow:
`--apply`, `--json`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_data_model_validator \
  specs/<category>/<spec-id>/spec.md \
  [--schema-files <glob[,glob...]>] \
  [--model-files <glob[,glob...]>] \
  [--migration-files <glob[,glob...]>] \
  [--dialect <postgres|mysql|sqlite|mssql|other>] \
  [--orm <prisma|typeorm|sequelize|django|rails|sqlalchemy|other>] \
  [--strict] \
  [--out <output-root>] \
  [--json]
```

**Kilo Code:**
```bash
/smartspec_data_model_validator.md \
  specs/<category>/<spec-id>/spec.md \
  [--schema-files <glob[,glob...]>] \
  [--model-files <glob[,glob...]>] \
  [--migration-files <glob[,glob...]>] \
  [--dialect <postgres|mysql|sqlite|mssql|other>] \
  [--orm <prisma|typeorm|sequelize|django|rails|sqlalchemy|other>] \
  [--strict] \
  [--out <output-root>] \
  [--json] \
  --platform kilo
```

---

## smartspec_dependency_updater

**Version:** 1.0.0

### Universal Flags (Supported)

These flags are supported by this workflow:
`--config`, `--json`, `--lang`, `--out`, `--platform`, `--quiet`

---

## smartspec_deployment_planner

**Description:** Generate deployment plans and checklists.

**Version:** 6.1.1

### Universal Flags (Supported)

These flags are supported by this workflow:
`--config`, `--json`, `--lang`, `--out`, `--platform`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_deployment_planner \
  specs/<category>/<spec-id>/spec.md \
  --verify-summary .spec/reports/verify-tasks-progress/<run-id>/summary.json \
  --target-env prod \
  --out .spec/reports/deployment-planner \
  --json
```

**CLI:**
```bash
/smartspec_deployment_planner \
  specs/<category>/<spec-id>/spec.md \
  --verify-summary .spec/reports/verify-tasks-progress/<run-id>/summary.json \
  --apply \
  --out .spec/reports/deployment-planner \
  --json
```

---

## smartspec_design_system_migration_assistant

**Description:** Assist in migrating between design systems (e.g., MUI to Ant Design).

**Version:** 6.0.0

### Usage Examples

**CLI:**
```bash
/smartspec_design_system_migration_assistant \
  --source-root <path/to/ui> \
  --from mui \
  --to custom \
  [--audit-summary .spec/reports/ui-component-audit/<run-id>/summary.json] \
  [--token-map .smartspec/mappings/design-tokens.json] \
  [--framework auto] \
  [--style-system auto] \
  [--confidence-threshold high] \
  [--apply-scope high_only] \
  [--out <output-root>] \
  [--json]
```

**Kilo Code:**
```bash
/smartspec_design_system_migration_assistant.md \
  --source-root <path/to/ui> \
  --from mui \
  --to custom \
  [--audit-summary .spec/reports/ui-component-audit/<run-id>/summary.json] \
  [--token-map .smartspec/mappings/design-tokens.json] \
  [--framework auto] \
  [--style-system auto] \
  [--confidence-threshold high] \
  [--apply-scope high_only] \
  [--out <output-root>] \
  [--json] \
  --platform kilo
```

---

## smartspec_docs_generator

**Description:** Generate technical documentation from specs and code.

**Version:** 6.1.1

### Universal Flags (Supported)

These flags are supported by this workflow:
`--config`, `--json`, `--lang`, `--out`, `--platform`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_docs_generator \
  --mode api-docs \
  --spec specs/<category>/<spec-id>/spec.md \
  --out .spec/reports/docs-generator \
  --json
```

**CLI:**
```bash
/smartspec_docs_generator \
  --mode user-guide \
  --spec specs/<category>/<spec-id>/spec.md \
  --target-dir docs \
  --write-docs \
  --apply \
  --out .spec/reports/docs-generator \
  --json
```

---

## smartspec_docs_publisher

**Description:** Publish documentation to various platforms.

**Version:** 6.1.1

### Universal Flags (Supported)

These flags are supported by this workflow:
`--config`, `--json`, `--lang`, `--out`, `--platform`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_docs_publisher \
  --docs-dir .spec/reports/docs-generator/<run-id>/bundle.preview \
  --publish-platform github-pages \
  --version v1.2.3 \
  --remote origin \
  --github-branch gh-pages \
  --out .spec/reports/docs-publisher \
  --json
```

**CLI:**
```bash
/smartspec_docs_publisher \
  --docs-dir .spec/reports/docs-generator/<run-id>/bundle.preview \
  --publish-platform github-pages \
  --version v1.2.3 \
  --remote origin \
  --github-branch gh-pages \
  --allow-network \
  --apply \
  --out .spec/reports/docs-publisher \
  --json
```

---

## smartspec_export_catalog

### Parameters

| Parameter | Status | Description |
|---|---|---|
| `--catalog-id` | Optional | Unique catalog identifier (URL) |
| `--include-metadata` | Optional | Include SmartSpec metadata (optional) |
| `--input-catalog` | Optional | Source SmartSpec catalog path |
| `--output-file` | Optional | Destination A2UI catalog path |
| `--output-format` | Optional | Target format (a2ui-v0.8) |
| `--platform` | Optional | Platform filter (optional) |

### Usage Examples

**CLI:**
```bash
/smartspec_export_catalog \
  --output-file public/web-catalog.json \
  --catalog-id "https://my-app.com/web-catalog-v1" \
  --output-format a2ui-v0.8
```

---

## smartspec_feedback_aggregator

**Description:** Aggregate feedback from multiple sources to drive continuous improvement.

**Version:** 1.0.0

### Parameters

| Parameter | Status | Description |
|---|---|---|
| `--help` | Optional | Show help message. |
| `--quiet` | Optional | Suppress all output except errors. |
| `--run-once` | Optional | Run the aggregation process once and exit. |
| `--verbose` | Optional | Enable verbose logging. |
| `--version` | Optional | Show version. |

### Usage Examples

**CLI:**
```bash
/smartspec_feedback_aggregator \
  --run-once
```

---

## smartspec_generate_multiplatform_ui

### Usage Examples

**CLI:**
```bash
/smartspec_generate_multiplatform_ui \
  --spec specs/feature/spec-002-contact/ui-spec.json \
  --platforms web,flutter \
  --web-renderer lit \
  --output-dir src/ui/contact \
  --apply
```

**Kilo Code:**
```bash
/smartspec_generate_multiplatform_ui.md \
  --spec specs/feature/spec-002-contact/ui-spec.json \
  --platforms web,flutter \
  --web-renderer lit \
  --output-dir src/ui/contact \
  --platform kilo \
  --apply
```

---

## smartspec_generate_plan

**Description:** Convert spec.md → plan.md (preview-first; dependency-aware; reuse-first;

**Version:** 6.0.6

### Universal Flags (Supported)

These flags are supported by this workflow:
`--apply`, `--json`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_generate_plan <spec_md> [--apply] [--ui-mode auto|json|inline] [--safety-mode strict|dev] [--plan-layout per-spec|consolidated] [--run-label "..."] [--json]
```

**Kilo Code:**
```bash
/smartspec_generate_plan.md \
  specs/<category>/<spec-id>/spec.md \
  --platform kilo \
  [--apply] [--ui-mode auto|json|inline] [--safety-mode strict|dev] [--plan-layout per-spec|consolidated] [--run-label "..."] [--json]
```

---

## smartspec_generate_spec

**Description:** Refine spec.md (SPEC-first) with 100% duplication prevention and reuse-first

**Version:** 7.0.0

### Universal Flags (Supported)

These flags are supported by this workflow:
`--config`, `--json`, `--lang`, `--out`, `--platform`, `--quiet`

---

## smartspec_generate_spec_from_prompt

**Description:** Bootstrap starter specs from a natural-language prompt (ideation-first;

**Version:** 7.0.0

### Parameters

| Parameter | Status | Description |
|---|---|---|
| `--interactive` | Optional | Force interactive mode for clarifying questions, even in non-interactive environments. |
| `--skip-ideation` | Optional | Skip the ideation phase if the user is confident the prompt is clear. |

---

## smartspec_generate_tasks

**Description:** Convert spec.md (or plan.md) → tasks.md with 100% duplication prevention.

**Version:** 7.0.0

### Universal Flags (Supported)

These flags are supported by this workflow:
`--config`, `--json`, `--lang`, `--out`, `--platform`, `--quiet`

---

## smartspec_generate_tests

**Description:** Generate test artifacts/suggestions (prompts/scripts/reports).

**Version:** 6.1.1

### Universal Flags (Supported)

These flags are supported by this workflow:
`--config`, `--json`, `--lang`, `--out`, `--platform`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_generate_tests \
  specs/<category>/<spec-id>/spec.md \
  [--mode strict] \
  [--plan-format both] \
  [--include-dependencies] \
  [--out .spec/reports/generate-tests/<label>] \
  [--json]
```

**CLI:**
```bash
/smartspec_generate_tests \
  specs/<category>/<spec-id>/spec.md \
  --apply \
  [--target-path specs/<category>/<spec-id>/testplan/tests.md] \
  [--out .spec/reports/generate-tests/<label>] \
  [--json]
```

---

## smartspec_generate_ui_spec

### Usage Examples

**CLI:**
```bash
/smartspec_generate_ui_spec \
  --requirements "Create restaurant booking form with date picker, time selector, guest count, and special requests" \
  --spec specs/feature/spec-001-booking/ui-spec.json
```

**Kilo Code:**
```bash
/smartspec_generate_ui_spec.md \
  --requirements "Create restaurant booking form with date picker, time selector, guest count, and special requests" \
  --spec specs/feature/spec-001-booking/ui-spec.json \
  --platform kilo
```

---

## smartspec_hotfix_assistant

**Description:** Assist in creating and managing hotfixes.

**Version:** 6.1.1

### Universal Flags (Supported)

These flags are supported by this workflow:
`--config`, `--json`, `--lang`, `--out`, `--platform`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_hotfix_assistant \
  --base-tag v1.2.3 \
  --hotfix-version v1.2.4 \
  --commit-sha <sha> \
  --remote origin \
  --main-branch main \
  --verify-summary .spec/reports/verify-tasks-progress/<run-id>/summary.json \
  --deployment-summary .spec/reports/deployment-planner/<run-id>/summary.json \
  --release-notes specs/<category>/<spec-id>/deployment/release_notes.md \
  --test-script test \
  --out .spec/reports/hotfix-assistant \
  --json
```

**CLI:**
```bash
/smartspec_hotfix_assistant \
  --base-tag v1.2.3 \
  --hotfix-version v1.2.4 \
  --commit-sha <sha> \
  --remote origin \
  --main-branch main \
  --allow-network \
  --require-tests-pass \
  --verify-summary .spec/reports/verify-tasks-progress/<run-id>/summary.json \
  --deployment-summary .spec/reports/deployment-planner/<run-id>/summary.json \
  --release-notes specs/<category>/<spec-id>/deployment/release_notes.md \
  --test-script test \
  --apply \
  --out .spec/reports/hotfix-assistant \
  --json
```

---

## smartspec_implement_tasks

**Description:** Implement code changes strictly from tasks.md with 100% duplication prevention and SmartSpec v7 governance.

**Version:** 7.0.0

### Universal Flags (Supported)

These flags are supported by this workflow:
`--config`, `--json`, `--lang`, `--out`, `--platform`, `--quiet`

---

## smartspec_implement_ui_from_spec

### Usage Examples

**CLI:**
```bash
/smartspec_implement_ui_from_spec \
  --spec specs/feature/spec-002-contact/ui-spec.json \
  --target-platform web \
  --renderer lit \
  --output-dir src/ui/contact \
  --apply
```

**Kilo Code:**
```bash
/smartspec_implement_ui_from_spec.md \
  --spec specs/feature/spec-002-contact/ui-spec.json \
  --target-platform web \
  --renderer lit \
  --output-dir src/ui/contact \
  --platform kilo \
  --apply
```

---

## smartspec_incident_response

**Description:** Manage production incidents from triage to resolution and post-mortem.

**Version:** 1.0.0

### Parameters

| Parameter | Status | Description |
|---|---|---|
| `--alert-payload` | Optional | The JSON payload of the alert that triggered the incident. |
| `--help` | Optional | Show help message. |
| `--quiet` | Optional | Suppress all output except errors. |
| `--verbose` | Optional | Enable verbose logging. |
| `--version` | Optional | Show version. |

### Usage Examples

**CLI:**
```bash
/smartspec_incident_response \
  --alert-payload <json-payload>
```

---

## smartspec_manage_ui_catalog

### Usage Examples

**CLI:**
```bash
/smartspec_manage_ui_catalog \
  --action add \
  --component-type slider \
  --component-def slider-component.json \
  --apply
```

**Kilo Code:**
```bash
/smartspec_manage_ui_catalog.md \
  --action add \
  --component-type slider \
  --component-def slider-component.json \
  --platform kilo \
  --apply
```

---

## smartspec_nfr_perf_planner

**Description:** Produce NFR/performance plan from spec (reports).

**Version:** 6.1.1

### Universal Flags (Supported)

These flags are supported by this workflow:
`--config`, `--json`, `--lang`, `--out`, `--platform`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_nfr_perf_planner \
  [--spec-ids <csv>] \
  [--include-dependencies] \
  [--nfr-policy-paths <glob[,glob...]>] \
  [--target-envs <csv>] \
  [--preferred-tools <csv>] \
  [--intensity-level <light|normal|heavy>] \
  [--max-tasks-per-nfr <int>] \
  [--plan-label <string>] \
  [--plan-format <md|json>] \
  [--safety-mode <normal|strict>] \
  [--stdout-summary] \
  [--nosubtasks] \
  [--out <output-root>] \
  [--json]
```

**Kilo Code:**
```bash
/smartspec_nfr_perf_planner.md \
  [--spec-ids <csv>] \
  [--include-dependencies] \
  [--nfr-policy-paths <glob[,glob...]>] \
  [--target-envs <csv>] \
  [--preferred-tools <csv>] \
  [--intensity-level <light|normal|heavy>] \
  [--max-tasks-per-nfr <int>] \
  [--plan-label <string>] \
  [--plan-format <md|json>] \
  [--safety-mode <normal|strict>] \
  [--stdout-summary] \
  [--nosubtasks] \
  [--out <output-root>] \
  [--json] \
  --platform kilo
```

---

## smartspec_nfr_perf_verifier

**Description:** Verify NFR/performance evidence (reports).

**Version:** 6.1.1

### Universal Flags (Supported)

These flags are supported by this workflow:
`--config`, `--json`, `--lang`, `--out`, `--platform`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_nfr_perf_verifier \
  specs/<category>/<spec-id>/spec.md \
  [--evidence-manifest .spec/reports/nfr-evidence/<run-id>/evidence.json] \
  [--target-env prod] \
  [--time-window 30d] \
  [--mode strict] \
  [--report-format both] \
  [--stdout-summary] \
  [--out <output-root>] \
  [--json]
```

**Kilo Code:**
```bash
/smartspec_nfr_perf_verifier.md \
  specs/<category>/<spec-id>/spec.md \
  [--evidence-manifest .spec/reports/nfr-evidence/<run-id>/evidence.json] \
  [--target-env prod] \
  [--time-window 30d] \
  [--mode strict] \
  [--report-format both] \
  [--stdout-summary] \
  [--out <output-root>] \
  [--json] \
  --platform kilo
```

---

## smartspec_observability_configurator

**Description:** Configure observability tools (logging, metrics, tracing).

**Version:** 6.1.1

### Universal Flags (Supported)

These flags are supported by this workflow:
`--config`, `--json`, `--lang`, `--out`, `--platform`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_observability_configurator \
  --spec specs/<category>/<spec-id>/spec.md \
  --obs-platform opentelemetry \
  --out .spec/reports/observability-configurator \
  --json
```

**CLI:**
```bash
/smartspec_observability_configurator \
  --spec specs/<category>/<spec-id>/spec.md \
  --obs-platform opentelemetry \
  --target-dir <path/approved/by/config> \
  --write-runtime-config \
  --apply \
  --out .spec/reports/observability-configurator \
  --json
```

---

## smartspec_optimize_ui_catalog

**Description:** Optimize and cache UI component catalog for faster lookup and improved performance

**Version:** 1.0.0

### Universal Flags (Supported)

These flags are supported by this workflow:
`--apply`, `--config`, `--json`, `--lang`, `--out`, `--platform`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_optimize_ui_catalog \
  --catalog .spec/ui-catalog.json \
  [--apply] \
  [--json]
```

**Kilo Code:**
```bash
/smartspec_optimize_ui_catalog.md \
  --catalog .spec/ui-catalog.json \
  --platform kilo \
  [--apply] \
  [--json]
```

---

## smartspec_performance_profiler

**Version:** 1.0.0

### Universal Flags (Supported)

These flags are supported by this workflow:
`--config`, `--json`, `--lang`, `--out`, `--platform`, `--quiet`

---

## smartspec_production_monitor

**Description:** Monitor production health, generate alerts, and feed metrics back into the SmartSpec ecosystem.

**Version:** 1.0.0

### Parameters

| Parameter | Status | Description |
|---|---|---|
| `--daemon` | Optional | Run continuously as a background process. |
| `--help` | Optional | Show help message. |
| `--quiet` | Optional | Suppress all output except errors. |
| `--run-once` | Optional | Run the monitoring check once and exit. |
| `--spec-id` | Optional | The ID of the spec to monitor. |
| `--verbose` | Optional | Enable verbose logging. |
| `--version` | Optional | Show version. |

### Usage Examples

**CLI:**
```bash
/smartspec_production_monitor \
  --spec-id <spec-id> \
  [--run-once] \
  [--daemon]
```

---

## smartspec_project_copilot

**Description:** Read-only project copilot that summarizes status and routes users to

**Version:** 6.0.7

### Universal Flags (Supported)

These flags are supported by this workflow:
`--json`, `--quiet`

### Usage Examples

**CLI:**
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

**Kilo Code:**
```bash
/smartspec_project_copilot.md "<question>" --platform kilo \
  [--domain <name>] [--spec-id <id>] [--spec-path <path>] [--aspect ...] \
  [--report <path>] [--format ...] [--short] \
  [--repos-config <path>] [--workspace-roots ...] [--registry-roots ...] \
  [--out <safe_reports_root>] \
  [--json]
```

---

## smartspec_quality_gate

**Description:** Consolidated quality gate (replaces ci_quality_gate + release_readiness).

**Version:** 6.0.0

### Universal Flags (Supported)

These flags are supported by this workflow:
`--apply`, `--json`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_quality_gate \
  --profile <ci|release> \
  [--spec <path/to/spec.md>|--spec-id <id>] \
  [--out <output-root>] \
  [--json] \
  [--strict]
```

**Kilo Code:**
```bash
/smartspec_quality_gate.md \
  --profile <ci|release> \
  [--spec <path/to/spec.md>|--spec-id <id>] \
  [--out <output-root>] \
  [--json] \
  [--strict] \
  --platform kilo
```

---

## smartspec_refactor_planner

**Version:** 1.0.0

### Universal Flags (Supported)

These flags are supported by this workflow:
`--config`, `--json`, `--lang`, `--out`, `--platform`, `--quiet`

---

## smartspec_reindex_specs

**Description:** Rebuild/refresh SPEC_INDEX.json from specs/** (non-destructive; reports

**Version:** 6.0.0

### Universal Flags (Supported)

These flags are supported by this workflow:
`--apply`, `--json`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_reindex_specs [--apply] [--json]
```

**Kilo Code:**
```bash
/smartspec_reindex_specs.md [--apply] [--json] \
  --platform kilo
```

---

## smartspec_reindex_workflows

**Description:** Rebuild/refresh WORKFLOWS_INDEX.yaml from .smartspec/workflows/** (non-destructive;

**Version:** 6.0.0

### Universal Flags (Supported)

These flags are supported by this workflow:
`--apply`, `--json`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_reindex_workflows [--apply] [--json]
```

**Kilo Code:**
```bash
/smartspec_reindex_workflows.md [--apply] [--json] \
  --platform kilo
```

---

## smartspec_release_tagger

**Description:** Manage release tags and versioning.

**Version:** 6.1.1

### Universal Flags (Supported)

These flags are supported by this workflow:
`--config`, `--json`, `--lang`, `--out`, `--platform`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_release_tagger \
  --version v1.2.3 \
  --commit-sha <sha> \
  --spec-id <spec-id> \
  --release-notes specs/<category>/<spec-id>/deployment/release_notes.md \
  --verify-summary .spec/reports/verify-tasks-progress/<run-id>/summary.json \
  --deployment-summary .spec/reports/deployment-planner/<run-id>/summary.json \
  --out .spec/reports/release-tagger \
  --json
```

**CLI:**
```bash
/smartspec_release_tagger \
  --version v1.2.3 \
  --commit-sha <sha> \
  --spec-id <spec-id> \
  --release-notes specs/<category>/<spec-id>/deployment/release_notes.md \
  --verify-summary .spec/reports/verify-tasks-progress/<run-id>/summary.json \
  --deployment-summary .spec/reports/deployment-planner/<run-id>/summary.json \
  --remote origin \
  --provider github \
  --allow-network \
  --apply \
  --out .spec/reports/release-tagger \
  --json
```

---

## smartspec_report_implement_prompter

**Description:** Generate implementation prompt packs with 100% duplication prevention.

**Version:** 7.0.0

### Universal Flags (Supported)

These flags are supported by this workflow:
`--config`, `--json`, `--lang`, `--out`, `--platform`, `--quiet`

### Usage Examples

**CLI:**
```bash
python3 .spec/scripts/validate_prompts.py \
  --prompts .spec/prompts/<spec-id>/<target>/<run-id>/ \
  --registry .spec/registry/ \
  --check-duplicates --threshold 0.8
```

---

## smartspec_rollback

**Description:** Safely roll back a failed deployment to a previous stable version.

**Version:** 1.0.0

### Parameters

| Parameter | Status | Description |
|---|---|---|
| `--auto-approve` | Optional | (Optional) Skip manual approval for high-risk rollbacks. Use with caution. |
| `--failed-deployment-id` | Optional | The ID of the deployment that failed. |
| `--help` | Optional | Show help message. |
| `--quiet` | Optional | Suppress all output except errors. |
| `--target-version` | Optional | (Optional) The specific version to roll back to. Defaults to the last known good version. |
| `--verbose` | Optional | Enable verbose logging. |
| `--version` | Optional | Show version. |

### Usage Examples

**CLI:**
```bash
/smartspec_rollback \
  --failed-deployment-id <id> \
  [--target-version <version>] \
  [--auto-approve]
```

---

## smartspec_security_audit_reporter

**Description:** Generate security audit reports.

**Version:** 6.0.0

### Universal Flags (Supported)

These flags are supported by this workflow:
`--apply`, `--json`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_security_audit_reporter \
  <path/to/spec.md> \
  [--report-format <summary|detailed>] \
  [--verify-summary <path/to/verify-tasks-progress-strict/summary.json>] \
  [--out <output-root>] \
  [--json]
```

**Kilo Code:**
```bash
/smartspec_security_audit_reporter.md \
  specs/<category>/<spec-id>/spec.md \
  [--report-format detailed] \
  [--verify-summary .spec/reports/verify-tasks-progress-strict/<run-id>/summary.json] \
  [--out <output-root>] \
  [--json] \
  --platform kilo
```

---

## smartspec_security_threat_modeler

**Description:** Model security threats and generate mitigation strategies.

**Version:** 6.0.0

### Universal Flags (Supported)

These flags are supported by this workflow:
`--apply`, `--json`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_security_threat_modeler \
  <path/to/spec.md> \
  [--framework <STRIDE|DREAD>] \
  [--apply] \
  [--json]
```

**Kilo Code:**
```bash
/smartspec_security_threat_modeler.md \
  specs/<category>/<spec-id>/spec.md \
  [--framework <STRIDE>] \
  [--apply] \
  [--json] \
  --platform kilo
```

---

## smartspec_sync_tasks_checkboxes

**Description:** Sync checkbox states in tasks.md using a strict verifier summary.json

**Version:** 6.0.0

### Parameters

| Parameter | Status | Description |
|---|---|---|
| `--apply` | Optional | - `--out <path>` (reports root; safe outputs only) |
| `--config` | Optional | (default `.spec/smartspec.config.yaml`) |
| `--json` | Optional | - `--quiet` |
| `--lang` | Optional | - `--platform <cli|kilo|ci|other>` |
| `--manual-policy` | Optional | (default `uncheck`) |
| `--recompute-parents` | Optional | (default `true`) |
| `--report-format` | Optional | (default `both`) |
| `--verify-report` | Required | strict verifier `summary.json` |

### Usage Examples

**CLI:**
```bash
/smartspec_sync_tasks_checkboxes <path/to/tasks.md> \
  --verify-report <path/to/summary.json> \
  [--manual-policy leave|uncheck] \
  [--recompute-parents true|false] \
  [--report-format md|json|both] \
  [--apply] [--json]
```

**Kilo Code:**
```bash
/smartspec_sync_tasks_checkboxes.md <path/to/tasks.md> \
  --platform kilo \
  --verify-report <path/to/summary.json> \
  [--manual-policy leave|uncheck] \
  [--recompute-parents true|false] \
  [--report-format md|json|both] \
  [--apply] [--json]
```

---

## smartspec_test_report_analyzer

**Description:** Analyze test reports and generate insights.

**Version:** 6.0.0

### Universal Flags (Supported)

These flags are supported by this workflow:
`--apply`, `--json`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_test_report_analyzer \
  --test-report .spec/reports/test-suite-runner/<run-id> \
  [--mode <normal|strict>] \
  [--max-log-bytes <int>] \
  [--max-junit-bytes <int>] \
  [--max-test-cases <int>] \
  [--out <output-root>] \
  [--json]
```

**Kilo Code:**
```bash
/smartspec_test_report_analyzer.md \
  --test-report .spec/reports/test-suite-runner/<run-id> \
  --mode normal \
  --out .spec/reports/test-report-analyzer \
  --json \
  --platform kilo
```

---

## smartspec_test_suite_runner

**Description:** Run test suites and generate reports.

**Version:** 6.0.0

### Universal Flags (Supported)

These flags are supported by this workflow:
`--apply`, `--json`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_test_suite_runner \
  --test-script <npm-script-name> \
  [--junit-report-path <relative/path/to/junit.xml>] \
  [--timeout 600] \
  [--allow-network] \
  [--out <output-root>] \
  [--json]
```

**Kilo Code:**
```bash
/smartspec_test_suite_runner.md \
  --test-script test:unit \
  --junit-report-path .spec/reports/test-suite-runner/_tmp/junit.xml \
  --timeout 600 \
  --out .spec/reports/test-suite-runner \
  --json \
  --platform kilo
```

---

## smartspec_ui_accessibility_audit

**Description:** Automated accessibility audit for A2UI implementations against WCAG 2.1 AA standards

**Version:** 1.0.0

### Universal Flags (Supported)

These flags are supported by this workflow:
`--config`, `--json`, `--lang`, `--out`, `--platform`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_ui_accessibility_audit \
  --spec specs/feature/spec-003-profile/ui-spec.json \
  --implementation src/ui/profile/ \
  [--json]
```

**Kilo Code:**
```bash
/smartspec_ui_accessibility_audit.md \
  --spec specs/feature/spec-003-profile/ui-spec.json \
  --implementation src/ui/profile/ \
  --platform kilo \
  [--json]
```

---

## smartspec_ui_agent

### Usage Examples

**CLI:**
```bash
/smartspec_ui_agent \
  --mode interactive \
  --context specs/feature/spec-002-contact
```

**Kilo Code:**
```bash
/smartspec_ui_agent.md \
  --mode interactive \
  --context specs/feature/spec-002-contact \
  --platform kilo
```

---

## smartspec_ui_analytics_reporter

**Description:** Track UI component usage, adoption metrics, and quality indicators across the project

**Version:** 1.0.0

### Universal Flags (Supported)

These flags are supported by this workflow:
`--config`, `--json`, `--lang`, `--out`, `--platform`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_ui_analytics_reporter \
  --catalog .spec/ui-catalog.json \
  --implementation src/ui/ \
  [--json]
```

**Kilo Code:**
```bash
/smartspec_ui_analytics_reporter.md \
  --catalog .spec/ui-catalog.json \
  --implementation src/ui/ \
  --platform kilo \
  [--json]
```

---

## smartspec_ui_component_audit

**Description:** Audit UI components for consistency and best practices.

**Version:** 6.0.0

### Universal Flags (Supported)

These flags are supported by this workflow:
`--apply`, `--json`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_ui_component_audit \
  --source-root <path/to/src> \
  --component-library <mui|antd|chakra|other> \
  --design-tokens <path/to/tokens.json> \
  [--wcag-level <AA|AAA>] \
  [--strict] \
  [--out <output-root>] \
  [--json]
```

**Kilo Code:**
```bash
/smartspec_ui_component_audit.md \
  --source-root <path/to/src> \
  --component-library <mui|antd|chakra|other> \
  --design-tokens <path/to/tokens.json> \
  [--wcag-level <AA|AAA>] \
  [--strict] \
  [--out <output-root>] \
  [--json] \
  --platform kilo
```

---

## smartspec_ui_performance_test

**Description:** Performance testing for UI implementations with metrics and benchmarks

**Version:** 1.0.0

### Universal Flags (Supported)

These flags are supported by this workflow:
`--config`, `--json`, `--lang`, `--out`, `--platform`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_ui_performance_test \
  --spec specs/feature/spec-003-profile/ui-spec.json \
  --implementation src/ui/profile/ \
  [--json]
```

**Kilo Code:**
```bash
/smartspec_ui_performance_test.md \
  --spec specs/feature/spec-003-profile/ui-spec.json \
  --implementation src/ui/profile/ \
  --platform kilo \
  [--json]
```

---

## smartspec_ui_validation

**Description:** UI audit/validation (includes consistency mode).

**Version:** 6.0.0

### Universal Flags (Supported)

These flags are supported by this workflow:
`--apply`, `--json`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_ui_validation \
  --mode <validation|consistency> \
  [--spec <path/to/spec.md>|--spec-id <id>] \
  [--scope <global|spec|ui-registry>] \
  [--out <output-root>] \
  [--json] \
  [--strict]
```

**Kilo Code:**
```bash
/smartspec_ui_validation.md \
  --mode <validation|consistency> \
  [--spec <path/to/spec.md>|--spec-id <id>] \
  [--scope <global|spec|ui-registry>] \
  [--out <output-root>] \
  [--json] \
  [--strict] \
  --platform kilo
```

---

## smartspec_validate_index

**Description:** Validate SPEC_INDEX and WORKFLOWS_INDEX integrity.

**Version:** 6.0.0

### Universal Flags (Supported)

These flags are supported by this workflow:
`--apply`, `--json`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_validate_index \
  [--out <output-root>] \
  [--json] \
  [--strict]
```

**Kilo Code:**
```bash
/smartspec_validate_index.md \
  [--out <output-root>] \
  [--json] \
  [--strict] \
  --platform kilo
```

---

## smartspec_verify_tasks_progress_strict

**Description:** 'Strict evidence-only verification using parseable evidence hooks (evidence:

**Version:** 6.0.0

### Universal Flags (Supported)

These flags are supported by this workflow:
`--json`, `--quiet`

### Usage Examples

**CLI:**
```bash
/smartspec_verify_tasks_progress_strict <path/to/tasks.md> [--report-format <md|json|both>] [--json]
```

**Kilo Code:**
```bash
/smartspec_verify_tasks_progress_strict.md <path/to/tasks.md> [--report-format <md|json|both>] [--json] \
  --platform kilo
```

---

## smartspec_verify_ui_implementation

### Usage Examples

**CLI:**
```bash
/smartspec_verify_ui_implementation \
  --spec specs/feature/spec-002-contact/ui-spec.json \
  --implementation src/ui/contact \
  --target-platform web
```

**Kilo Code:**
```bash
/smartspec_verify_ui_implementation.md \
  --spec specs/feature/spec-002-contact/ui-spec.json \
  --implementation src/ui/contact \
  --target-platform web \
  --platform kilo
```

---

