# SmartSpec V5 — Production‑Grade Documentation

SmartSpec V5 is a **next‑generation Specification Orchestration System** designed for high‑integrity software projects. It unifies:
- Specification generation (SPEC)
- Task planning (tasks.md)
- Kilo Code implementation prompts
- Multi‑domain architecture patterns
- Validation, compliance, and performance governance

This README is written as a **production‑grade guide**, integrating all capabilities from the full **SmartSpec V5 Documentation**, including advanced features such as Profiles, Domain Detection, Config Files, Meta‑Tags, Validation Rules, and Migration Behavior.

---

# 🧭 1. What is SmartSpec V5?
SmartSpec V5 is a framework that standardizes how complex software specifications are:
- **Created** (SPEC)
- **Validated** (Architect Validation Engine)
- **Expanded** into implementation tasks (tasks.md)
- **Converted** into executable prompts (Kilo Code prompts)

V5 includes:
- A modular architecture
- Domain‑specific enhancements
- Strong validation and compliance rules
- Human‑readable but machine‑optimized outputs
- Built‑in enterprise governance

---

# ⚡ 2. V5 Core Capabilities
### ✔ Multi‑Profile SPEC generation
### ✔ Domain‑driven specialization (fintech, healthcare, IoT, AI, etc.)
### ✔ Configurable DI, Security, and Performance levels
### ✔ Auto‑validation engine with error levels
### ✔ Force‑update and partial‑update modes
### ✔ Meta‑Tag protected sections (never overwritten)
### ✔ Compact mode and Full mode
### ✔ Project‑level and Organization‑level configuration files
### ✔ V4 → V5 migration compatibility

---

# 🏗️ 3. System Architecture Overview
```
 ┌──────────────────────────────┐
 │        User / Developer      │
 └───────────────┬──────────────┘
                 │ CLI / UI
 ┌───────────────▼──────────────────────────────┐
 │             SmartSpec V5 Engine              │
 ├───────────────────────────┬──────────────────┤
 │  SPEC Generator (Profiles)│ Domain Engine    │
 │  SPEC Updater             │ DI/Security Mode │
 │  SPEC Validator           │ Performance Mode │
 ├───────────────────────────┼──────────────────┤
 │          Task Generator (tasks.md)           │
 ├───────────────────────────┼──────────────────┤
 │         Kilo Code Prompt Generator           │
 └───────────────────────────┴──────────────────┘
```

---

# 🧩 4. Profiles System (V5)
Profiles define the **template structure**, **mandatory sections**, and **validation rules**.

### Available Profiles
- `basic` – simple CRUD / small backend services
- `backend-service` – scalable services with integrations
- `financial` – ledger, credit, billing, audit‑required systems
- `full` – enterprise‑grade SPEC, maximum safety & detail

### Choose a profile
```
/spec create financial
/spec update financial
```

---

# 🌐 5. Domains (Auto‑Applied Enhancements)
Domains add specialized content to SPECs.

### Supported Domains
- `fintech` → adds STRIDE‑full, audit logging, PCI DSS guidance
- `healthcare` → HIPAA data protection notes
- `iot` → device identity, OTA update safety
- `ai` → model evaluation, dataset governance
- `realtime` → low‑latency SLA guidance
- `batch` → throughput and ETL safety
- `internal` → relaxed security & flexible patterns

### How to apply
```
/spec create financial --domain=fintech
```

---

# 🔒 6. Meta‑Tags (Write‑Protected Sections)
SmartSpec V5 respects protected regions using meta‑tags.

Example:
```md
<!-- @critical security -->
This security section will never be overwritten.
```

Supported meta‑tags:
- `@critical security`
- `@critical config`
- `@critical legal`
- `@critical audit`
- `@no-edit`

These ensure updates will **never remove essential sections**.

---

# 🧱 7. Dependency Injection Control Modes
V5 allows flexible DI patterns.

### Modes
- `--di=none` → no DI section
- `--di=minimal` → lightweight DI
- `--di=auto` → recommended DI pattern (default)
- `--di=full` → full DI pattern with interfaces & examples

### Example
```
/spec update full --di=auto
```

---

# 🛡️ 8. Security Modes
```
--security=stride-basic
--security=stride-full
```

`stride-full` includes:
- full threat table
- tampering protection
- replay‑attack notes
- non‑repudiation patterns

---

# 🚀 9. Performance Modes
```
--performance=basic
--performance=full
```

`performance=full` adds:
- P50 / P95 / P99 targets
- throughput requirements
- SLA uptime
- queue/DB performance baselines
- load testing requirements

---

# ⚙️ 10. Configuration Files (Project & Org Level)
SmartSpec V5 uses two config layers.

### 1) Project‑level config
`smartspec.config.json`
```
{
  "profile": "financial",
  "domain": "fintech",
  "security": "stride-full",
  "performance": "full"
}
```

### 2) Organization‑level config
`.smartspec/config.json`
```
{
  "defaultProfile": "backend-service",
  "enforceSecurity": true,
  "allowModeOverride": false
}
```

---

# 📦 11. Compact Mode
For minimal SPECs:
```
/spec create financial --mode=compact
```
Removes:
- examples
- deep STRIDE details
- implementation guides

Useful for:
- rapid prototyping
- internal‑only designs

---

# 📜 12. Force Update System
Used when SPEC sections became outdated.

Examples:
```
/spec update full --force-update=stride
/spec update financial --force-update=performance,config
/spec update full --force-update=all
```

---

# 🧪 13. Validation System (Automatic Checks)
Validation runs on SPEC generation & update.

### ERROR‑level (must fix)
- missing security for financial domain
- missing retry logic for external APIs
- missing configuration schema
- invalid/missing STRIDE when required

### WARNING‑level
- domain mismatch
- deprecated template sections

Validation ensures outputs are **safe, consistent, and complete**.

---

# 🔄 14. Migration Guide (V4 → V5)
SmartSpec V5 preserves V4 behavior but adds stricter defaults.

### Improvements in V5
- profiles system
- domain‑aware enhancements
- protected meta‑tags
- performance/security controls
- validation engine

### Update older SPECs
```
/spec upgrade v5
```
Adds missing:
- Non‑Goals
- Domain content
- Performance requirements
- STRIDE enhancements

---

# 🛠️ 15. Workflow Summary
SmartSpec V5 ships with three main workflows.

### 1) Generate SPEC
```
/spec create <profile> --domain=<domain>
```
Outputs a new SmartSpec v5‑format SPEC.

### 2) Generate Tasks
```
/spec tasks <path>
```
Converts SPEC → tasks.md

### 3) Generate Kilo Prompt
```
/spec kilo <path>
```
Converts tasks.md → kilo prompt with full safety constraints.

---

# 📚 16. Knowledge Base Files
Stored in `.smartspec/` directory.

Includes:
- DI Pattern Template
- Security STRIDE Template
- Performance Requirements
- Implementation Checklist
- SPEC Structure & Rules
- Domain Enhancement Packs

---

# 🧪 17. Example Usage
### Create a fintech SPEC
```
/spec create financial --domain=fintech --security=stride-full --performance=full
```

### Update a SPEC with strict validation
```
/spec update full --force-update=config,performance
```

### Generate tasks from SPEC
```
/spec tasks specs/feature/spec-004-financial-system/spec.md
```

### Generate Kilo Code prompt
```
/spec kilo specs/feature/spec-004-financial-system/tasks.md
```

---

# 🧭 18. Troubleshooting
- **SPEC missing sections** → run `/spec update full`
- **Validation errors** → check ERROR‑level rules in output
- **Kilo prompt missing tasks** → re‑generate tasks.md
- **Domain mismatch** → check `smartspec.config.json`

---

# 🗺️ 19. Roadmap
- Plugin SDK
- Template Marketplace
- Automatic Diagram Renderer
- Integration with Kilo Cloud
- Unified Multi‑SPEC Architecture Projects

---

# 🏁 20. License
Internal proprietary documentation. Do not distribute.

