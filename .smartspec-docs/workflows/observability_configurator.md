_# SmartSpec Workflow: Observability Configurator

**Workflow:** `/smartspec_observability_configurator`  
**Version:** 6.1.1

## 1. Overview

This workflow generates configuration for observability tools (like Prometheus, Grafana, or Datadog) based on the metrics, logging, and tracing requirements defined in a `spec.md`.

## 2. Key Features

- **Spec-Driven Configuration:** Translates high-level observability requirements into concrete tool configurations.
- **Multi-Tool Support:** Can generate configs for different observability platforms.
- **Dashboard and Alert Generation:** Can create draft dashboard configurations and alert rules.

## 3. Usage

```bash
/smartspec_observability_configurator   specs/my-service/spec.md   --tool datadog   --apply
```
_