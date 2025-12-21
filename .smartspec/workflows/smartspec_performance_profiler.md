# smartspec_performance_profiler

---

## 📝 Frontmatter (YAML)

```yaml
version: 1.0.0
workflow_id: smartspec_performance_profiler
summary: "Automated performance profiling and optimization planning"
author: Manus AI
license: MIT

# Governance & Safety
safety:
  allow_writes_only_under:
    - ".spec/reports/performance/"
    - ".spec/reports/previews/"
  deny_writes_under:
    - ".git/"
    - ".smartspec/"
    - "src/"

# AI Agent Configuration
ai_config:
  persona: "Performance engineer focused on system optimization"
  capabilities:
    - performance_profiling
    - bottleneck_analysis
    - optimization_strategy

# Universal Flags Support
flags:
  - "--help"
  - "--version"
  - "--dry-run"
  - "--apply"
  - "--verbose"
```

---

## 📚 Overview

`/smartspec_performance_profiler` is a specialized workflow for identifying and planning the resolution of performance bottlenecks in the codebase.

**Key Features:**
- ✅ Integrates with profiling tools (e.g., `pprof`, `JProfiler`) to collect performance data
- ✅ Analyzes profiling data to identify bottlenecks (CPU, memory, I/O)
- ✅ Suggests optimization strategies with estimated performance gains
- ✅ Generates performance optimization plans
- ✅ Creates tasks for optimization work in `tasks.md`

---

## 🎯 Behavior

### 1. Run Performance Profile
- The agent runs the application with a profiler attached
- It collects performance data under a specific load or scenario
- It saves the profiling data to `.spec/reports/performance/`

### 2. Analyze Profiling Data
- The agent analyzes the profiling data to identify hotspots and bottlenecks
- It visualizes the data (e.g., flame graphs) to pinpoint performance issues

### 3. Generate Optimization Plan
- For each identified bottleneck, the agent generates an optimization plan
- The plan includes:
  - A description of the bottleneck
  - The proposed optimization strategy (e.g., "Cache database queries", "Use a more efficient algorithm")
  - Expected performance improvement
  - Verification and testing plan

### 4. Create Optimization Tasks (with --apply)
- If `--apply` is used, the agent creates a new `tasks.md` file with tasks for each optimization item
- Each task is linked to the optimization plan and includes clear performance targets

---

## ⚙️ Governance Contract

- **Allowed writes:** `.spec/reports/performance/`, `.spec/reports/previews/`
- **Forbidden writes:** `.git/`, `.smartspec/`, `src/`
- **--apply required:** To create tasks.md

---

## 🚩 Flags

### Universal flags (must support)

All SmartSpec workflows support these universal flags:

| Flag | Required | Description |
|---|---|---|
| `--config` | No | Path to custom config file (default: `.spec/smartspec.config.yaml`) |
| `--lang` | No | Output language (`th` for Thai, `en` for English, `auto` for automatic detection) |
| `--platform` | No | Platform mode (`cli` for CLI, `kilo` for Kilo Code, `ci` for CI/CD, `other` for custom integrations) |
| `--out` | No | Base output directory for reports and generated files (must pass safety checks) |
| `--json` | No | Output results in JSON format for machine parsing and automation |
| `--quiet` | No | Suppress non-essential output, showing only errors and critical information |

### Workflow-specific flags

Flags specific to `/smartspec_performance_profiler`:

| Flag | Required | Description |
|---|---|---|
| `--run-profile` | Yes | Run the performance profiling with configured profiler |
| `--target` | Yes | Path to code/module to profile (e.g., `src/api/auth`) |
| `--scenario` | No | Run a specific performance scenario (high-load, api-stress-test, normal-usage) |
| `--profiler` | No | Use a specific profiler (pprof, jprofiler, py-spy, perf, default: auto-detect) |
| `--min-gain` | No | Report only optimizations with a minimum expected performance gain (percentage, e.g., 10) |
| `--apply` | No | Enable creation of tasks.md with optimization tasks |
| `--dry-run` | No | Perform profiling and analysis without creating any tasks (preview mode) |
| `--help` | No | Show help message and usage examples |
| `--version` | No | Show workflow version information |
| `--verbose` | No | Show detailed profiling output including all measurements |

### Flag usage notes

- **Config-first approach:** Prefer setting defaults in `.spec/smartspec.config.yaml` to minimize command-line flags
- **Boolean flags:** Flags without values are boolean (presence = true, absence = false)
- **Path safety:** All path arguments must pass safety validation (no directory traversal, symlink escape, or absolute paths outside project)
- **Secret handling:** Never pass secrets as flag values; use `env:VAR_NAME` references or config file
- **Preview-first:** Use `--dry-run` to preview optimization recommendations before using `--apply`
- **Profiler selection:** Use `--profiler auto` to let the workflow detect the best profiler for your stack
