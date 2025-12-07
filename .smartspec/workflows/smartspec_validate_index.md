---
description: Validate SPEC Index (centralization-aware)
---

# /smartspec_validate_index

Validate the project's SPEC_INDEX integrity and optionally auto-fix common issues.
This workflow is compatible with SmartSpec centralization:
- `.spec/` is the canonical project governance space.
- `.smartspec/` is tooling space (deprecated as a canonical index location).

## What It Does

- Validates the structure and consistency of `SPEC_INDEX.json`
- Checks for common index integrity issues:
  - Missing or duplicated spec IDs
  - Path mismatches
  - Broken dependencies
  - Registry reference mismatches (if registries exist)
- Produces a health score
- Optionally auto-fixes safe issues with `--fix`

## When to Use

- Before major releases
- After bulk spec changes
- Weekly/monthly health checks
- When suspecting INDEX issues
- After team handover

## Expected Outcome

- Validation report (`.md`)
- Health score (0-100)
- List of errors and warnings
- Recommendations for fixes
- Auto-fixed INDEX (if `--fix` flag)

---

## Flags

- `--index` Path to SPEC_INDEX.json   
  default: `.spec/SPEC_INDEX.json`

- `--output` Output report path (optional)  
  default directory: `.spec/reports/`

- `--fix` Auto-fix safe issues (optional)

- `--strict` Fail on warnings (optional)

---

## 0. Prerequisites

### 0.1 Check SPEC_INDEX Exists

```bash
# Resolve SPEC_INDEX path
INDEX_PATH="${FLAGS_index:-}"

if [ -z "$INDEX_PATH" ]; then
  if [ -f ".spec/SPEC_INDEX.json" ]; then
    INDEX_PATH=".spec/SPEC_INDEX.json"
  elif [ -f "SPEC_INDEX.json" ]; then
    INDEX_PATH="SPEC_INDEX.json"
  elif [ -f ".smartspec/SPEC_INDEX.json" ]; then
    INDEX_PATH=".smartspec/SPEC_INDEX.json" # deprecated
  fi
fi

if [ -z "$INDEX_PATH" ] || [ ! -f "$INDEX_PATH" ]; then
  echo "❌ ERROR: SPEC_INDEX.json not found"
  echo ""
  echo "Checked (in order):"
  echo "  1) .spec/SPEC_INDEX.json (canonical)"
  echo "  2) SPEC_INDEX.json (legacy root mirror)"
  echo "  3) .smartspec/SPEC_INDEX.json (deprecated)"
  echo ""
  echo "Please ensure SPEC_INDEX exists or specify correct path:"
  echo "  /smartspec_validate_index --index=path/to/SPEC_INDEX.json"
  exit 1
fi

echo "✅ Found SPEC_INDEX at: $INDEX_PATH"
```

### 0.2 Load SPEC_INDEX

```javascript
const fs = require('fs');
const path = require('path');

const FLAGS = globalThis.FLAGS || {};

const resolveIndexPath = () => {
  if (FLAGS.index && fs.existsSync(FLAGS.index)) return FLAGS.index;

  if (fs.existsSync('.spec/SPEC_INDEX.json')) return '.spec/SPEC_INDEX.json';
  if (fs.existsSync('SPEC_INDEX.json')) return 'SPEC_INDEX.json';
  if (fs.existsSync('.smartspec/SPEC_INDEX.json')) return '.smartspec/SPEC_INDEX.json'; // deprecated

  // default fallback (should not reach here due to bash precheck)
  return '.spec/SPEC_INDEX.json';
};

const indexPath = resolveIndexPath();
const indexContent = fs.readFileSync(indexPath, 'utf-8');

let specIndex;
try {
  specIndex = JSON.parse(indexContent);
} catch (error) {
  console.error('❌ ERROR: Invalid JSON in SPEC_INDEX.json');
  console.error(error.message);
  process.exit(1);
}
```

---

## 1. Validate Index Structure

Check required top-level fields (example):
- `version`
- `specs[]`
- `last_updated` (if used)
- `public_specs_count`, `private_specs_count`, `total_specs` (if used)

Rules:
- `total_specs` should equal `specs.length`  
  or be auto-corrected when `--fix`
- `public + private` should equal `total_specs`  
  when these fields are present

---

## 2. Validate Spec Entries

Validate each spec item:
- Unique `id`
- Valid `path`
- Type/category consistency
- Dependency references must exist

Recommended checks:
- Duplicate IDs
- Path points to existing `spec.md`
- No circular dependency (warning-level unless `--strict`)

---

## 3. Cross-Check with Registries (if present)

If registries exist under:
- `.spec/registry/`

Then validate:
- API names referenced in specs exist in `api-registry.json`
- Domain terms match `glossary.json`
- Data models match `data-model-registry.json`
- Critical sections match `critical-sections-registry.json`

Do not invent new registry entries in validate mode.  
Only recommend additions or fix when `--fix` is safe.

---

## 4. Output Report

Default output directory:
- `.spec/reports/`

Example naming:
- `SPEC_INDEX_VALIDATION_REPORT.md`

Include:
- Health score
- Errors & warnings
- Suggested fixes
- Detected canonical/legacy index path

---

## 5. Auto-Fix (Optional)

Enabled only with:
- `--fix`

Safe auto-fix examples:
- Recompute `total_specs` from `specs.length`
- Recompute `public_specs_count` + `private_specs_count` if fields exist
- Normalize obvious path formatting issues (non-destructive)

Never:
- Rewrite `spec.md`
- Delete spec entries without explicit user instruction

---

## Notes

- Canonical index is `.spec/SPEC_INDEX.json`
- Root `SPEC_INDEX.json` is allowed for legacy projects
- `.smartspec/SPEC_INDEX.json` is deprecated and should not be created for new projects

