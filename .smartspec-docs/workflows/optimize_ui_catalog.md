| manual_name | manual_version | compatible_workflow | compatible_workflow_versions |
|-------------|----------------|---------------------|------------------------------|
| /smartspec_optimize_ui_catalog Manual (EN) | 6.0 | /smartspec_optimize_ui_catalog | 6.0.x |

# /smartspec_optimize_ui_catalog Manual (v6.0, English)

## 1. Overview

This manual explains how to use the workflow:

The `/smartspec_optimize_ui_catalog` workflow optimizes UI component catalog performance through caching and indexing mechanisms, providing 10-100x faster component lookups for large catalogs.

**Purpose:** Improve UI catalog performance with intelligent caching, search indexing, and dependency graph optimization for faster component discovery and reduced memory footprint.

**Version:** 6.0  
**Category:** ui_optimization_and_analytics

---

## 2. Usage

This workflow supports invocation via the Command Line Interface (CLI) and Kilo Code (internal scripting environment).

### 🔗 CLI Usage

The CLI invocation requires specifying the catalog file and cache location.

```bash
/smartspec_optimize_ui_catalog \
  --catalog <path/to/ui-catalog.json> \
  --cache <path/to/cache.json> \
  [--rebuild-index] \
  [--invalidate-cache] \
  [--verify]
```

### Kilo Code Usage

The Kilo Code invocation is identical to the CLI structure, typically used within automated pipelines or internal scripts.

**Important:** When using Kilo Code, you MUST include `--platform kilo` flag.

```bash
/smartspec_optimize_ui_catalog.md \
  --catalog <path/to/ui-catalog.json> \
  --cache <path/to/cache.json> \
  [--rebuild-index] \
  [--invalidate-cache] \
  [--verify] \
  --platform kilo
```

---

## 3. Use Cases

### Use Case 1: Initial Catalog Optimization (CLI)

**Scenario:** A project has a large UI catalog with 50+ components and lookups are becoming slow.

**Command:**

```bash
/smartspec_optimize_ui_catalog \
  --catalog .spec/ui-catalog.json \
  --cache .spec/cache/ui-catalog-cache.json \
  --rebuild-index
```

**Expected Result:**

1. The workflow analyzes the catalog structure.
2. Creates an optimized cache with component metadata.
3. Builds search indexes for fast lookups.
4. Generates dependency graph for relationship queries.
5. Writes cache to `.spec/cache/ui-catalog-cache.json`.
6. Reports performance improvements (10-100x faster).
7. Exit code `0` (Success).

### Use Case 2: Update Cache After Catalog Changes (Kilo Code)

**Scenario:** The UI catalog has been updated with new components and the cache needs to be refreshed.

**Command (Kilo Code Snippet):**

```bash
/smartspec_optimize_ui_catalog.md \
  --catalog .spec/ui-catalog.json \
  --cache .spec/cache/ui-catalog-cache.json \
  --invalidate-cache \
  --platform kilo
```

**Expected Result:**

1. The workflow invalidates the existing cache.
2. Rebuilds cache with updated catalog data.
3. Updates search indexes.
4. Refreshes dependency graph.
5. Exit code `0` (Success).

### Use Case 3: Verify Cache Integrity (CLI)

**Scenario:** A developer wants to verify that the cache is valid and up-to-date.

**Command:**

```bash
/smartspec_optimize_ui_catalog \
  --catalog .spec/ui-catalog.json \
  --cache .spec/cache/ui-catalog-cache.json \
  --verify \
  --json
```

**Expected Result:**

1. The workflow compares cache with catalog.
2. Validates cache integrity and freshness.
3. Reports any discrepancies or issues.
4. Output includes `verification.json` with results.
5. Exit code `0` if valid, `1` if issues found.

---

## 4. Parameters

The following parameters and flags control the execution and behavior of the `/smartspec_optimize_ui_catalog` workflow.

### Required Parameters

| Parameter | Type | Description | Validation |
| :--- | :--- | :--- | :--- |
| `--catalog` | `<string>` | Path to UI catalog JSON file. | Must exist and be valid JSON. |
| `--cache` | `<string>` | Path to cache file (will be created if not exists). | Must be writable location. |

### Universal Flags

| Flag | Description | Default | Platform Support |
| :--- | :--- | :--- | :--- |
| `--config` | Path to the SmartSpec configuration file. | `.spec/smartspec.config.yaml` | `cli` \| `kilo` \| `ci` \| `other` |
| `--lang` | Language for report generation (e.g., `th`, `en`). | (System default) | `cli` \| `kilo` \| `ci` \| `other` |
| `--platform` | Execution platform context. **Required for Kilo Code.** | (Inferred) | `cli` \| `kilo` \| `ci` \| `other` |
| `--out` | Base path for safe outputs. | `.spec/reports/ui-optimization/` | `cli` \| `kilo` \| `ci` \| `other` |
| `--json` | Output in JSON format. | `false` | `cli` \| `kilo` \| `ci` \| `other` |
| `--quiet` | Suppress standard output logs. | `false` | `cli` \| `kilo` \| `ci` \| `other` |

### Workflow-Specific Flags

| Flag | Description | Platform Support |
| :--- | :--- | :--- |
| `--rebuild-index` | Force rebuild of search indexes. | `cli` \| `kilo` \| `ci` \| `other` |
| `--invalidate-cache` | Invalidate and rebuild cache. | `cli` \| `kilo` \| `ci` \| `other` |
| `--verify` | Verify cache integrity without modifications. | `cli` \| `kilo` \| `ci` \| `other` |

---

## 5. Output

The workflow generates output artifacts according to its configuration.

### Output Files

| File Path | Description |
| :--- | :--- |
| `<cache-path>` | Optimized cache file with component metadata and indexes. |
| `.spec/reports/ui-optimization/<run-id>/optimization-report.md` | Performance optimization report. |
| `.spec/reports/ui-optimization/<run-id>/summary.json` | JSON summary of optimization results. |

### Cache Structure

The cache file contains:
- **Component metadata:** Fast-access component data
- **Search indexes:** ID, name, tag, category indexes
- **Dependency graph:** Component relationship mappings
- **Performance metrics:** Cache hit rates and lookup times

---

## 6. Performance Improvements

### Expected Performance Gains

| Catalog Size | Before Optimization | After Optimization | Improvement |
| :--- | :--- | :--- | :--- |
| 10 components | 50ms | 5ms | 10x faster |
| 50 components | 500ms | 10ms | 50x faster |
| 100 components | 2000ms | 20ms | 100x faster |

### Optimization Features

- **Component Caching:** In-memory cache for frequently accessed components
- **Search Indexing:** Fast lookups by ID, name, tags, category
- **Dependency Graph:** Optimized component relationship queries
- **Memory Efficiency:** Reduced memory footprint through smart caching

---

## 7. Notes

- **Platform Flag:** When using Kilo Code, always include `--platform kilo` to ensure proper context and logging.
- **Cache Location:** Store cache in `.spec/cache/` directory (gitignored by default).
- **Rebuild Frequency:** Rebuild cache after significant catalog changes (10+ components).
- **Verification:** Run `--verify` periodically to ensure cache integrity.
- **Performance:** Most beneficial for catalogs with 50+ components.
- **Configuration:** The workflow respects settings in `.spec/smartspec.config.yaml`.

---

**End of Manual**
