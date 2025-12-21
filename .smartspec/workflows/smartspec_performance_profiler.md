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

- `--run-profile`: **(Required)** Run the performance profiling
- `--scenario <name>`: Run a specific performance scenario (e.g., `high-load`, `api-stress-test`)
- `--profiler <name>`: Use a specific profiler (e.g., `pprof`, `jprofiler`)
- `--min-gain <percentage>`: Report only optimizations with a minimum expected performance gain
