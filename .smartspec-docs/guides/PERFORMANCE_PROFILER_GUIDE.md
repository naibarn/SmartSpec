# Guide: smartspec_performance_profiler

## 📚 Overview

`/smartspec_performance_profiler` is a specialized workflow for identifying and planning the resolution of performance bottlenecks in the codebase.

**Key Features:**
- ✅ Integrates with profiling tools (e.g., `pprof`, `JProfiler`) to collect performance data
- ✅ Analyzes profiling data to identify bottlenecks (CPU, memory, I/O)
- ✅ Suggests optimization strategies with estimated performance gains
- ✅ Generates performance optimization plans
- ✅ Creates tasks for optimization work in `tasks.md`

---

## 🎯 Basic Usage

This workflow is typically run by performance engineers or developers when a performance issue is suspected.

### Running a Profile

```bash
/smartspec_performance_profiler --run-profile --scenario api-stress-test
```

**Behavior:**
1.  Runs the `api-stress-test` performance scenario.
2.  Collects profiling data.
3.  Generates a report in `.spec/reports/performance/` with identified bottlenecks.

### Creating Optimization Tasks

```bash
/smartspec_performance_profiler --run-profile --apply --min-gain 10
```

**Behavior:**
1.  Runs the default performance profile.
2.  Generates a report.
3.  Creates a `tasks.md` file with tasks for all optimization opportunities that are expected to yield at least a 10% performance gain.

---

## ⚙️ Workflow Cycle

1.  **Profile:** The workflow runs the application with a profiler to collect data.
2.  **Analyze:** It analyzes the data to find hotspots and bottlenecks.
3.  **Plan:** It generates detailed optimization plans.
4.  **Taskify:** With `--apply`, it creates a `tasks.md` file.
5.  **Implement:** Developers use the plans and tasks to implement the optimizations.

---

## 🚩 Flags

- `--run-profile`: **(Required)** Run the performance profiling.
- `--scenario <name>`: Run a specific performance scenario (e.g., `high-load`, `api-stress-test`).
- `--profiler <name>`: Use a specific profiler (e.g., `pprof`, `jprofiler`).
- `--min-gain <percentage>`: Report only optimizations with a minimum expected performance gain.
- `--apply`: Create a `tasks.md` file with optimization tasks.
