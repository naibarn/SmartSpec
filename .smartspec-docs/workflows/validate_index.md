# smartspec_validate_index

Validate SPEC_INDEX.json integrity and generate comprehensive health report.

---

## Summary

This workflow performs comprehensive validation of SPEC_INDEX.json to ensure:
- All referenced files exist
- No broken dependencies
- No circular dependencies
- No duplicate spec IDs
- Metadata is complete and consistent
- Health score calculation

**When to Use:**
- Before major releases
- After bulk spec changes
- Weekly/monthly maintenance
- When suspecting INDEX issues
- After team handover

---

## Parameters

### `--fix`
**Type:** boolean  
**Default:** false  
**Description:** Automatically fix issues that can be auto-fixed (metadata, dependents)

### `--report`
**Type:** enum (`summary` | `detailed`)  
**Default:** `summary`  
**Description:** Report detail level

### `--index`
**Type:** string  
**Default:** `.smartspec/SPEC_INDEX.json`  
**Description:** Path to SPEC_INDEX.json file

### `--output`
**Type:** string  
**Optional:** true  
**Description:** Output report file path (defaults to `.smartspec/reports/`)

---

## Examples

### Basic Validation
```bash
/smartspec_validate_index
```

**Output:**
```
✅ SPEC_INDEX.json is valid
📊 Health Score: 95/100
⚠️ 2 warnings found
```

---

### Validate and Auto-Fix
```bash
/smartspec_validate_index --fix
```

**Output:**
```
✅ Fixed 3 issues:
  - Updated dependents for spec-001
  - Removed broken reference: spec-999
  - Fixed metadata for spec-004
  
📊 Health Score: 100/100
```

---

### Detailed Report
```bash
/smartspec_validate_index --report=detailed
```

**Output:**
```
📊 Validation Report

✅ Passed Checks:
  - File existence: 10/10 specs
  - No circular dependencies
  - No duplicates

⚠️ Warnings:
  - spec-001: Orphaned (no dependents)
  - spec-004: Stale (last updated 2 years ago)

❌ Errors:
  - spec-002: Broken reference: spec-999
```

---

### Custom Output
```bash
/smartspec_validate_index --fix --report=detailed --output=validation.md
```

**Output:**
```
✅ Report saved to: validation.md
📊 Health Score: 98/100
```

---

## How It Works

### Phase 1: Load and Parse INDEX

1. **Load SPEC_INDEX.json**
   - Read from specified path
   - Parse JSON
   - Validate JSON syntax

2. **Extract Specs**
   - Build spec registry
   - Extract metadata
   - Build dependency graph

---

### Phase 2: Run Validation Checks

#### 1. File Existence Checks
Verify all referenced files exist:
- Spec files (`spec.md`)
- Implementation files (`spec.files[]`)
- External files (`spec.external_files[]`)

**Example:**
```json
{
  "spec-004": {
    "path": "specs/feature/spec-004/spec.md",
    "files": ["src/services/credit.service.ts"]
  }
}
```

**Checks:**
- ✅ `specs/feature/spec-004/spec.md` exists?
- ✅ `src/services/credit.service.ts` exists?

---

#### 2. Broken Reference Detection
Verify all dependencies exist in INDEX:

**Example:**
```json
{
  "spec-004": {
    "dependencies": ["spec-001", "spec-999"]
  }
}
```

**Checks:**
- ✅ `spec-001` exists in INDEX?
- ❌ `spec-999` does NOT exist → **Broken reference!**

---

#### 3. Circular Dependency Detection
Detect circular dependency chains:

**Example:**
```json
{
  "spec-001": {"dependencies": ["spec-002"]},
  "spec-002": {"dependencies": ["spec-003"]},
  "spec-003": {"dependencies": ["spec-001"]}
}
```

**Result:**
- ❌ Circular: spec-001 → spec-002 → spec-003 → spec-001

---

#### 4. Duplicate Spec Detection
Find duplicate spec IDs:

**Example:**
```json
{
  "spec-004": {...},
  "spec-004": {...}  // ← Duplicate!
}
```

---

#### 5. Orphaned Spec Detection
Find specs with no dependencies and no dependents:

**Example:**
```json
{
  "spec-001": {"dependencies": []},  // No dependencies
  "spec-002": {"dependencies": ["spec-003"]}
  // spec-001 has no dependents → Orphaned!
}
```

---

#### 6. Stale Spec Detection
Find specs not updated recently:

**Example:**
```json
{
  "spec-004": {
    "last_updated": "2023-01-01"  // 2 years ago!
  }
}
```

---

#### 7. Metadata Consistency
Verify required metadata fields:

**Required fields:**
- `path`
- `version`
- `status`
- `files`
- `dependencies`

**Example:**
```json
{
  "spec-004": {
    "path": "specs/feature/spec-004/spec.md",
    "version": "1.0.0",
    "status": "DRAFT"
    // ← Missing "files" field!
  }
}
```

---

#### 8. Dependents Calculation
Verify `dependents` field is accurate:

**Example:**
```json
{
  "spec-001": {
    "dependents": ["spec-002", "spec-003"]
  },
  "spec-002": {
    "dependencies": ["spec-001"]  // ✅ Correct
  },
  "spec-003": {
    "dependencies": ["spec-004"]  // ❌ Wrong! Should be spec-001
  }
}
```

---

### Phase 3: Calculate Health Score

**Scoring (0-100):**
- File existence: 20 points
- No broken references: 15 points
- No circular dependencies: 15 points
- No duplicates: 10 points
- Metadata complete: 15 points
- Dependents accurate: 10 points
- No orphaned specs: 10 points
- No stale specs: 5 points

**Example:**
```
File existence: 20/20 ✅
No broken references: 15/15 ✅
No circular dependencies: 15/15 ✅
No duplicates: 10/10 ✅
Metadata complete: 15/15 ✅
Dependents accurate: 10/10 ✅
No orphaned specs: 5/10 ⚠️ (1 orphaned)
No stale specs: 3/5 ⚠️ (1 stale)

Total: 93/100
```

---

### Phase 4: Auto-Fix (if --fix flag)

**Auto-fixable issues:**
1. **Metadata inconsistencies**
   - Add missing fields
   - Fix field types

2. **Dependents calculation**
   - Recalculate from dependencies
   - Update all specs

3. **Broken references** (optional)
   - Remove if spec doesn't exist
   - Or prompt user to add missing spec

**Not auto-fixable:**
- Circular dependencies (requires manual review)
- Stale specs (requires manual update)
- Orphaned specs (may be intentional)

---

### Phase 5: Generate Report

#### Summary Report (default):
```
✅ SPEC_INDEX.json Validation Complete

📊 Health Score: 92/100

✅ Passed Checks (5):
  - File existence: 15/15 specs
  - No circular dependencies
  - No duplicates
  - Metadata complete
  - Dependents calculated

⚠️ Warnings (2):
  - spec-001: Orphaned (no dependents)
  - spec-012: Stale (last updated 18 months ago)

❌ Errors (0)

💡 Recommendations:
  1. Review orphaned spec: spec-001
  2. Update stale spec: spec-012
  3. Run: /smartspec_validate_index --fix
```

---

#### Detailed Report (--report=detailed):
```markdown
# SPEC_INDEX.json Validation Report

**Generated:** 2025-12-04 23:45  
**Index Path:** .smartspec/SPEC_INDEX.json  
**Total Specs:** 15

---

## Health Score: 92/100

### Score Breakdown:
- File Existence: 100% (15/15)
- No Broken References: 100% (0 broken)
- No Circular Dependencies: 100% (0 circular)
- No Duplicates: 100% (0 duplicates)
- Metadata Complete: 100% (15/15)
- Dependents Calculated: 100% (15/15)
- No Orphaned Specs: 93% (1 orphaned)
- No Stale Specs: 93% (1 stale)

---

## ✅ Passed Checks

### 1. File Existence (15/15)
All spec files and referenced files exist.

### 2. No Broken References
All dependencies reference valid specs.

[... detailed breakdown ...]

---

## ⚠️ Warnings (2)

### 1. Orphaned Spec: spec-001-authentication
- **Path:** specs/core/spec-001-authentication/spec.md
- **Issue:** No other specs depend on this spec
- **Impact:** Low (may be intentional)
- **Recommendation:** Verify if standalone

### 2. Stale Spec: spec-012-subscription
- **Path:** specs/feature/spec-012-subscription/spec.md
- **Last Updated:** 2023-06-15 (18 months ago)
- **Impact:** Medium (may be outdated)
- **Recommendation:** Review and update

---

## 💡 Recommendations

1. Review orphaned specs
2. Update stale specs
3. Run auto-fix: `/smartspec_validate_index --fix`

---

## 📊 Dependency Graph

```
spec-001-authentication (orphaned)

spec-002-user-management
  └─ depends on: spec-001-authentication

spec-004-financial-system
  ├─ depends on: spec-001-authentication
  ├─ depends on: spec-002-user-management
  └─ depends on: spec-012-subscription
```
```

---

## Use Cases

### Use Case 1: Before Release
```bash
# Validate before deploying to production
/smartspec_validate_index --report=detailed --output=pre-release-validation.md

# Review report
cat pre-release-validation.md

# Fix issues
/smartspec_validate_index --fix

# Verify again
/smartspec_validate_index
```

---

### Use Case 2: After Bulk Changes
```bash
# After adding/removing many specs
/smartspec_validate_index --fix

# Output:
# ✅ Fixed 5 issues:
#   - Updated dependents for 3 specs
#   - Removed 2 broken references
```

---

### Use Case 3: Weekly Maintenance
```bash
# Schedule weekly validation
/smartspec_validate_index --report=detailed --output=.smartspec/reports/weekly-$(date +%Y%m%d).md

# Review warnings and errors
# Fix stale specs
# Update orphaned specs
```

---

### Use Case 4: Troubleshooting
```bash
# When workflows fail with dependency errors
/smartspec_validate_index --fix --report=detailed

# Check for circular dependencies
# Check for broken references
# Fix and retry workflows
```

---

## Best Practices

### 1. Run Before Major Releases
Always validate INDEX before deploying to production.

### 2. Schedule Regular Checks
Run weekly or monthly to catch issues early.

### 3. Use --fix Carefully
Review what will be fixed before using `--fix` flag.

### 4. Keep Reports
Save detailed reports for audit trail.

### 5. Fix Warnings Promptly
Don't ignore warnings - they may become errors.

---

## Troubleshooting

### Issue: "SPEC_INDEX.json not found"
**Solution:**
```bash
# Specify custom path
/smartspec_validate_index --index=path/to/SPEC_INDEX.json

# Or create INDEX first
/smartspec_reindex_specs
```

---

### Issue: "Invalid JSON syntax"
**Solution:**
```bash
# Validate JSON syntax
cat .smartspec/SPEC_INDEX.json | jq .

# Fix syntax errors manually
# Or regenerate INDEX
/smartspec_reindex_specs
```

---

### Issue: "Many broken references"
**Solution:**
```bash
# Auto-fix broken references
/smartspec_validate_index --fix

# Or manually review and fix
# Check if specs were deleted or renamed
```

---

### Issue: "Circular dependencies detected"
**Solution:**
```bash
# Cannot auto-fix - requires manual review
/smartspec_validate_index --report=detailed

# Review dependency chain
# Break the cycle by removing one dependency
```

---

## Output Files

### Summary Report (console)
Printed to console by default.

### Detailed Report (.md file)
Saved to `.smartspec/reports/validation-YYYYMMDD-HHMMSS.md` by default.

### Updated INDEX (if --fix)
Backup saved to `.smartspec/SPEC_INDEX.json.backup-YYYYMMDD-HHMMSS`.

---

## Related Workflows

- `/smartspec_reindex_specs` - Re-index SPEC_INDEX.json
- `/smartspec_verify_tasks_progress` - Verify task completion
- `/smartspec_fix_errors` - Fix code errors

---

## Next Steps

After validation:
1. Review warnings and errors
2. Run `/smartspec_validate_index --fix` to auto-fix
3. Manually fix issues that cannot be auto-fixed
4. Re-run validation to verify
5. Continue with implementation workflows
