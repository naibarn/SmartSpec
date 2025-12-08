# `/smartspec_generate_tests`

**Automatically generate comprehensive test suites for a specific spec, ensuring coverage targets are met while maintaining test quality and consistency.**

---

## v5.2 Alignment Notes

This manual preserves the original behavior of `/smartspec_generate_tests` and adds clarifications for SmartSpec **v5.2 centralization**.

- **Project-owned canonical space:** `.spec/`
- **Canonical index (preferred):** `.spec/SPEC_INDEX.json`
- **Shared registries (optional):** `.spec/registry/`
- **Legacy mirror (optional):** `SPEC_INDEX.json` at repo root
- **Deprecated tooling index:** `.smartspec/SPEC_INDEX.json`

The generate-tests workflow is **spec-scoped**. When it needs the list of files for a spec, it should resolve the index in this order unless `--index` is provided:

1) `.spec/SPEC_INDEX.json`  
2) `SPEC_INDEX.json` (root legacy mirror)  
3) `.smartspec/SPEC_INDEX.json` (deprecated fallback)  
4) `specs/SPEC_INDEX.json` (older layout)

### UI JSON Addendum (optional)

If the target spec is a UI spec and your project adopts Penpot JSON-first UI:

- `ui.json` remains the **design source of truth**.
- This workflow should generate tests for **engineering-owned code**, not rewrite `ui.json`.
- UI logic should be tested via component bindings and state/interaction tests defined in tasks.

Projects that do not use UI JSON are not affected.

---

## 1. Summary

This workflow automatically generates a comprehensive test suite for a specific spec. It analyzes your current implementation, test coverage, and expected behavior defined in the spec and tasks. It then produces or expands tests across unit, integration, and end-to-end levels.

The workflow is designed to be **non-destructive**. It **appends** new tests instead of overwriting, preventing test duplication and preserving existing test logic.

### ✅ Primary Use Cases

- Automatically achieve a coverage target (e.g., 80%, 90%)
- Generate missing unit or integration tests
- Detect uncovered areas from spec-scoped implementation
- Improve test quality while maintaining spec alignment

---

## 2. Usage

```bash
/smartspec_generate_tests <spec_directory> [options...]
```

---

## 3. Parameters & Options

### **Primary Argument**

| Name | Type | Required? | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `spec_directory` | `string` | ✅ Yes | Path to the spec folder | `specs/feature/spec-004-financial-system` |

### **Coverage Options**

| Option | Type | Default | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `--target` | `number` | `80` | Target coverage percentage | `--target 90` |
| `--baseline` | `number` | Auto detect | Treat coverage below this as priority | `--baseline 60` |

### **Filtering Options**

| Option | Type | Default | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `--file` | `string` | All files | Generate tests only for a specific file | `--file src/services/payment.service.ts` |
| `--type` | `string` | `all` | Test type: `unit`, `integration`, `e2e` | `--type unit` |
| `--only-uncovered` | `flag` | `false` | Focus only on uncovered code | `--only-uncovered` |

### **Execution Options**

| Option | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `--append` | `flag` | `true` | Append new tests instead of overwriting |
| `--dry-run` | `flag` | `false` | Preview test generation without writing files |
| `--strict` | `flag` | `false` | Fail if coverage target cannot be reached |

### **Index Options (v5.2 compatible)**

| Option | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `--index` | `string` | auto-detect | Override SPEC_INDEX path |
| `--specindex` | `string` | alias | Legacy-compatible alias for `--index` |

---

## 4. Examples

### Generate Tests to Reach 80% Coverage

```bash
/smartspec_generate_tests specs/feature/spec-004-financial-system
```

### Generate Tests to Reach 90% Coverage

```bash
/smartspec_generate_tests specs/feature/spec-004-financial-system --target 90
```

### Generate Tests for Specific File

```bash
/smartspec_generate_tests specs/feature/spec-004-financial-system --file src/services/payment.service.ts
```

### Generate Only Unit Tests

```bash
/smartspec_generate_tests specs/feature/spec-004-financial-system --type unit
```

### Focus on Uncovered Code Only

```bash
/smartspec_generate_tests specs/feature/spec-004-financial-system --only-uncovered
```

### Dry Run (Preview Tests)

```bash
/smartspec_generate_tests specs/feature/spec-004-financial-system --dry-run
```

---

## 5. How It Works

### Phase 1: Analyze Current Coverage (Spec-Scoped)

**1. Load SPEC_INDEX.json**

_v5.2 note:_ When `--index` is not provided, prefer the canonical index at `.spec/SPEC_INDEX.json`, then fall back to the root mirror, then deprecated tooling locations.

```json
{
  "specs": {
    "spec-004-financial-system": {
      "files": [
        "src/services/credit.service.ts",
        "src/services/payment.service.ts",
        "src/models/transaction.model.ts"
      ]
    }
  }
}
```

**2. Extract Spec-Scoped Files**

The workflow uses this list to limit test generation to only files relevant to the current spec.

**3. Run Coverage Tooling**

Example (TypeScript + Jest):

```bash
npm test -- --coverage --collectCoverageFrom=\
  src/services/credit.service.ts,\
  src/services/payment.service.ts,\
  src/models/transaction.model.ts
```

---

### Phase 2: Identify Missing Test Scenarios

The workflow analyzes:

- Missing unit tests for functions/methods
- Missing integration tests across services
- Missing edge-case coverage
- Missing tests matching acceptance criteria

---

### Phase 3: Generate Tests (Append-Only)

The workflow generates tests in a style consistent with your project’s conventions.

Key behavior:

- **Appends** new tests to existing files
- Avoids duplicating previously tested cases
- Groups tests by feature and scenario

---

### Phase 4: Verify Coverage Improvement

After generation:

1. Re-run coverage
2. Compare against target
3. Summarize outcomes

---

## 6. Test Structure Strategy

The workflow attempts to generate tests in this priority order:

1) Unit tests for pure logic
2) Service integration tests
3) API-level tests
4) UI interaction tests (only when relevant)

---

## 7. Quality & Non-Destructive Rules

### Append-Only Safety

This workflow is designed to **append** new tests instead of overwriting existing test code.

Why this matters:

- Prevents losing handcrafted test logic
- Reduces merge conflicts
- Preserves historical test intent

### Duplicate Prevention

Before writing new tests:

- Scan existing test names and describe blocks
- Compare scenario signatures
- Skip duplicates

---

## 8. Coverage Growth Strategy

Recommended incremental approach:

```bash
# Start from 70%
/smartspec_generate_tests specs/feature/spec-004 --target 70

# Increase to 80%
/smartspec_generate_tests specs/feature/spec-004 --target 80

# Finally aim for 90%
/smartspec_generate_tests specs/feature/spec-004 --target 90
```

---

## 9. Best Practices

### 1. Generate Tests After a Verified Implementation Slice

```bash
# Implement a safe chunk
/smartspec_implement_tasks specs/feature/spec-004/tasks.md --range=1-6 --skip-completed

# Verify progress
/smartspec_verify_tasks_progress specs/feature/spec-004/spec.md

# Generate tests
/smartspec_generate_tests specs/feature/spec-004 --target 80
```

### 2. Review Generated Tests

```bash
# Generate tests
/smartspec_generate_tests specs/feature/spec-004

# Review
/git diff

# Adjust edge cases manually
# Then run tests
npm test
```

### 3. Verify Coverage

```bash
# Generate tests
/smartspec_generate_tests specs/feature/spec-004 --target 90

# Run tests with coverage
npm test -- --coverage

# Verify target reached
```

---

## 10. Troubleshooting

### Issue: Tests not appending correctly

**Cause:** Test file structure or naming conventions differ from expected patterns.

**Fix:**

- Ensure the workflow is run with `--append` (default).
- Review generated output in `--dry-run` first.

---

### Issue: Coverage not increasing

**Cause:** The uncovered code may require integration-level scenarios that unit tests cannot reach.

**Fix:**

- Use `--type integration`.
- Expand the spec acceptance criteria if needed.

---

### Issue: Duplicate tests generated

**Cause:** Existing tests may not follow consistent naming conventions.

**Fix:**

- Normalize naming.
- Regenerate using `--only-uncovered`.

---

## 11. Related Workflows

- `/smartspec_generate_tasks`
- `/smartspec_implement_tasks`
- `/smartspec_verify_tasks_progress`
- `/smartspec_fix_errors`
- `/smartspec_refactor_code`

---

## 12. Summary

`/smartspec_generate_tests` is a spec-scoped, append-only test generator that helps your teams quickly reach meaningful coverage targets without destroying existing test suites.

In SmartSpec v5.2, it respects canonical index resolution, optional shared registries, and the UI JSON addendum when your project adopts Penpot-driven UI workflows.

