---
name: /smartspec_optimize_ui_catalog
version: 1.0.0
role: optimization
description: Optimize and cache UI component catalog for faster lookup and improved performance
workflow: /smartspec_optimize_ui_catalog
---

# smartspec_optimize_ui_catalog

> **Canonical path:** `.smartspec/workflows/smartspec_optimize_ui_catalog.md`  
> **Version:** 1.0.0  
> **Status:** Production Ready  
> **Category:** optimization

## Purpose

Optimize UI component catalogs for improved performance:

- Build indexed catalog cache
- Validate catalog integrity
- Generate component dependency graph
- Create fast lookup indexes
- Optimize catalog file size

This workflow improves performance of UI-related workflows by pre-processing and caching catalog data.

---

## Governance contract

This workflow MUST follow:

- `knowledge_base_smartspec_handbook.md` (v6)
- `.spec/smartspec.config.yaml`

### Write scopes (enforced)

Allowed writes:

- Cache outputs: `.spec/cache/ui-catalog/**` (**requires** `--apply`)
- Safe outputs (reports): `.spec/reports/optimize-ui-catalog/**` (no `--apply` required)

Forbidden writes (must hard-fail):

- Any path outside config `safety.allow_writes_only_under`
- Any governed artifact (specs, SPEC_INDEX, etc.)
- Any runtime source tree modifications

### `--apply` behavior

- Without `--apply`: MUST NOT create cache files. Produce optimization report only.
- With `--apply`: may create optimized cache files.

---

## Invocation

### CLI

```bash
/smartspec_optimize_ui_catalog \
  --catalog .spec/ui-catalog.json \
  [--apply] \
  [--json]
```

### Kilo Code

```bash
/smartspec_optimize_ui_catalog.md \
  --catalog .spec/ui-catalog.json \
  --platform kilo \
  [--apply] \
  [--json]
```

---

## Flags

### Universal flags (must support)

| Flag | Required | Description |
|---|---|---|
| `--config` | No | Path to custom config file (default: `.spec/smartspec.config.yaml`) |
| `--lang` | No | Output language (`th` for Thai, `en` for English) |
| `--platform` | No | Platform mode (`cli`, `kilo`, `ci`, `other`) |
| `--apply` | No | Enable writes to cache files |
| `--out` | No | Base output directory for reports |
| `--json` | No | Output results in JSON format |
| `--quiet` | No | Suppress non-essential output |

### Workflow-specific flags

| Flag | Required | Description |
|---|---|---|
| `--catalog` | Yes | Path to UI catalog file to optimize (e.g., `.spec/ui-catalog.json`) |
| `--force-rebuild` | No | Force rebuild cache even if up-to-date |
| `--validate-only` | No | Only validate catalog, don't optimize |
| `--include-stats` | No | Include detailed statistics in report |

### Flag usage notes

- `--catalog` is required and must point to a valid UI catalog JSON file
- `--apply` is required to create cache files
- `--force-rebuild` ignores existing cache timestamps
- `--validate-only` performs validation without optimization

---

## Behavior

### 1) Load catalog

- Read UI catalog from `--catalog` path
- Validate JSON structure
- Check catalog version compatibility

### 2) Validate catalog integrity

- Validate all component definitions
- Check for duplicate component IDs
- Verify component references
- Validate security levels
- Check accessibility metadata

### 3) Build indexes

Create optimized indexes:

- **Component ID index:** Fast lookup by component ID
- **Category index:** Components grouped by category
- **Tag index:** Components grouped by tags
- **Dependency graph:** Component dependencies
- **Security index:** Components by security level

### 4) Optimize catalog

- Remove redundant data
- Compress component definitions
- Deduplicate common properties
- Generate compact representation

### 5) Generate cache (with `--apply`)

Write cache files:

- `.spec/cache/ui-catalog/catalog.optimized.json` - Optimized catalog
- `.spec/cache/ui-catalog/indexes.json` - Lookup indexes
- `.spec/cache/ui-catalog/dependencies.json` - Dependency graph
- `.spec/cache/ui-catalog/metadata.json` - Cache metadata

### 6) Generate report

Write report:

- `.spec/reports/optimize-ui-catalog/<run-id>/report.md`
- `.spec/reports/optimize-ui-catalog/<run-id>/summary.json` (when `--json`)

---

## Output

### Report structure

**report.md:**

```markdown
# UI Catalog Optimization Report

## Summary
- Original size: 125 KB
- Optimized size: 45 KB
- Compression: 64%
- Components: 17
- Categories: 5
- Validation: PASSED

## Indexes Created
- Component ID index: 17 entries
- Category index: 5 categories
- Tag index: 12 tags
- Dependency graph: 8 dependencies

## Validation Results
✅ All components valid
✅ No duplicate IDs
✅ All references resolved
✅ Security levels valid
✅ Accessibility metadata complete

## Performance Impact
- Lookup speed: 10x faster
- Load time: 5x faster
- Memory usage: -60%

## Recommendations
- Cache is up-to-date
- No issues found
```

**summary.json:**

```json
{
  "status": "success",
  "original_size_bytes": 128000,
  "optimized_size_bytes": 46080,
  "compression_ratio": 0.64,
  "component_count": 17,
  "category_count": 5,
  "validation_passed": true,
  "indexes_created": 4,
  "performance_improvement": {
    "lookup_speed": "10x",
    "load_time": "5x",
    "memory_reduction": "60%"
  },
  "cache_location": ".spec/cache/ui-catalog/",
  "timestamp": "2025-12-22T00:00:00Z"
}
```

---

## Cache structure

### catalog.optimized.json

Optimized catalog with compressed component definitions.

### indexes.json

```json
{
  "by_id": {
    "button-primary": { "category": "buttons", "file_offset": 0 },
    "input-text": { "category": "inputs", "file_offset": 1024 }
  },
  "by_category": {
    "buttons": ["button-primary", "button-secondary"],
    "inputs": ["input-text", "input-email"]
  },
  "by_tag": {
    "interactive": ["button-primary", "input-text"],
    "form": ["input-text", "input-email"]
  }
}
```

### dependencies.json

```json
{
  "graph": {
    "form-contact": {
      "depends_on": ["input-text", "input-email", "button-primary"],
      "used_by": []
    }
  }
}
```

### metadata.json

```json
{
  "version": "1.0.0",
  "created_at": "2025-12-22T00:00:00Z",
  "source_catalog": ".spec/ui-catalog.json",
  "source_hash": "abc123...",
  "optimization_level": "standard"
}
```

---

## Performance benefits

### Lookup speed

- **Before:** Linear search through catalog (~100ms for 100 components)
- **After:** Index lookup (~10ms)
- **Improvement:** 10x faster

### Load time

- **Before:** Parse full catalog (~500ms)
- **After:** Load optimized catalog (~100ms)
- **Improvement:** 5x faster

### Memory usage

- **Before:** Full catalog in memory (~10 MB)
- **After:** Optimized catalog (~4 MB)
- **Improvement:** 60% reduction

---

## Cache invalidation

Cache is invalidated when:

- Source catalog is modified (timestamp check)
- Catalog hash changes
- Cache version mismatch
- `--force-rebuild` flag used

---

## Error handling

### Validation errors

If catalog validation fails:

- Report all validation errors
- Do not create cache files
- Exit with code 1

### Optimization errors

If optimization fails:

- Report optimization errors
- Do not create cache files
- Exit with code 1

### Cache write errors

If cache write fails:

- Report write errors
- Clean up partial cache files
- Exit with code 1

---

## Usage examples

### Example 1: Validate catalog

```bash
/smartspec_optimize_ui_catalog \
  --catalog .spec/ui-catalog.json \
  --validate-only
```

### Example 2: Optimize and cache

```bash
/smartspec_optimize_ui_catalog \
  --catalog .spec/ui-catalog.json \
  --apply
```

### Example 3: Force rebuild with stats

```bash
/smartspec_optimize_ui_catalog \
  --catalog .spec/ui-catalog.json \
  --force-rebuild \
  --include-stats \
  --apply
```

### Example 4: Kilo Code

```bash
/smartspec_optimize_ui_catalog.md \
  --catalog .spec/ui-catalog.json \
  --platform kilo \
  --apply
```

---

## Integration

This workflow integrates with:

- `smartspec_generate_ui_spec` - Uses optimized catalog for faster component lookup
- `smartspec_implement_ui_from_spec` - Uses indexes for faster component resolution
- `smartspec_verify_ui_implementation` - Uses dependency graph for verification
- `smartspec_manage_ui_catalog` - Triggers optimization after catalog changes

---

## Best practices

1. **Run after catalog changes** - Optimize after adding/removing components
2. **Use in CI/CD** - Include optimization in build pipeline
3. **Monitor cache size** - Ensure cache doesn't grow too large
4. **Validate regularly** - Run validation periodically
5. **Force rebuild occasionally** - Rebuild cache to ensure consistency

---

## Security considerations

- Cache files are read-only after creation
- Cache location must be within allowed write paths
- Catalog validation prevents malicious component definitions
- Dependency graph prevents circular dependencies

---

# End of workflow doc
