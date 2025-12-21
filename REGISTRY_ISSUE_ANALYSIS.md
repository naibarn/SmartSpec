# Registry Files Not Created - Root Cause Analysis

**Date:** 21 December 2025  
**Workflow:** `smartspec_generate_spec` v6.0.2  
**Issue:** Registry files not created in `.spec/registry/`

---

## Problem Statement

When running `smartspec_generate_spec`, the workflow does not create registry files in `.spec/registry/` despite documentation indicating that registry should be maintained.

---

## Expected Registry Files

Based on the provided registry backup, the following files should be created/updated:

### 1. `.spec/registry/api-registry.json`

Tracks API endpoints across all specs:
- `method`, `path`, `description`
- `owner_spec`, `status_codes`
- Optional: `rate_limit`

### 2. `.spec/registry/data-model-registry.json`

Tracks data models/entities:
- `name`, `description`, `owner_spec`
- `shared_with` (array of spec IDs)
- `fields` (array of field names)
- Optional: `indexes`

### 3. `.spec/registry/glossary.json`

Tracks terminology and definitions:
- `term`, `definition`, `owner_spec`
- `category` (security, authentication, compliance, etc.)
- Optional: `aliases`, `shared_with`

### 4. `.spec/registry/critical-sections-registry.json`

Tracks sections that cannot be auto-updated:
- `spec_id`, `title`, `location`
- `hash`, `allow_update`, `reason`
- `last_verified`

---

## Root Cause Analysis

### 1. Registry Writes Are Forbidden

**Location:** `.smartspec/workflows/smartspec_generate_spec.md` Line 62

```markdown
Forbidden writes (must hard-fail):
- Any path outside config `safety.allow_writes_only_under`
- Any path under config `safety.deny_writes_under` (e.g., `.spec/registry/**`)
- Any runtime source tree modifications
```

**Impact:** Workflow explicitly forbids writing to `.spec/registry/**`

### 2. No Registry Generation Behavior

**Location:** `.smartspec/workflows/smartspec_generate_spec.md` Behavior section

The workflow does not include:
- Parsing spec.md for endpoints/models/terms
- Extracting registry-relevant information
- Creating/updating registry files
- Merging with existing registry data

### 3. Inconsistent Documentation

**Contradiction 1:**
- Line 36: "**Registry:** `.spec/registry/` (component registry, reuse index)"
- Line 62: Registry is in **forbidden writes**

**Contradiction 2:**
- Line 281: `summary.json` includes `"registry": ["path"]` in writes
- Behavior section: No mention of registry file creation

**Contradiction 3:**
- Line 56: "Governed registry: `.spec/SPEC_INDEX.json`" (allowed)
- Line 62: `.spec/registry/**` (forbidden)

### 4. No Registry Templates

The workflow documentation does not include:
- Templates for registry file structure
- Examples of registry entries
- Merge/update logic for existing registry

### 5. No Validation

The workflow does not validate:
- Whether registry files were created
- Whether registry entries are complete
- Whether registry is consistent with spec.md

---

## Impact

### Current State

When `smartspec_generate_spec` runs:
1. ✅ Creates/updates `spec.md`
2. ✅ Updates `.spec/SPEC_INDEX.json` (if allowlisted)
3. ❌ Does NOT create/update `.spec/registry/api-registry.json`
4. ❌ Does NOT create/update `.spec/registry/data-model-registry.json`
5. ❌ Does NOT create/update `.spec/registry/glossary.json`
6. ❌ Does NOT create/update `.spec/registry/critical-sections-registry.json`

### Consequences

**1. No Reuse Detection:**
- Cannot detect duplicate API endpoints across specs
- Cannot detect duplicate data models
- Cannot enforce shared terminology

**2. No Duplication Prevention:**
- Specs may define the same endpoint with different contracts
- Specs may define the same entity with different fields
- Terms may have inconsistent definitions

**3. No Cross-Spec Validation:**
- Cannot validate that shared entities have consistent fields
- Cannot validate that API contracts are compatible
- Cannot track which specs share which components

**4. Manual Registry Maintenance:**
- Registry must be manually created/updated
- High risk of registry becoming stale
- No automated synchronization with specs

---

## Solution Design

### 1. Update Governance Contract

**Change Line 56-62 from:**
```markdown
Allowed writes:
- Governed specs: `specs/**` (**requires** `--apply`)
- Governed registry: `.spec/SPEC_INDEX.json` (**requires** `--apply` and allowlisted)
- Safe outputs (previews/reports): `.spec/reports/generate-spec/**` (no `--apply` required)

Forbidden writes (must hard-fail):
- Any path outside config `safety.allow_writes_only_under`
- Any path under config `safety.deny_writes_under` (e.g., `.spec/registry/**`)
- Any runtime source tree modifications
```

**To:**
```markdown
Allowed writes:
- Governed specs: `specs/**` (**requires** `--apply`)
- Governed registry: `.spec/SPEC_INDEX.json` (**requires** `--apply` and allowlisted)
- Component registry: `.spec/registry/**` (**requires** `--apply`)
- Safe outputs (previews/reports): `.spec/reports/generate-spec/**` (no `--apply` required)

Forbidden writes (must hard-fail):
- Any path outside config `safety.allow_writes_only_under`
- Any path under config `safety.deny_writes_under` (excluding `.spec/registry/**`)
- Any runtime source tree modifications
```

### 2. Add Registry Generation Behavior

Add new section in Behavior:

**Step 5: Extract Registry Information (MANDATORY)**

After generating spec.md preview, the workflow MUST:

1. **Parse spec.md** to extract:
   - API endpoints (method, path, description, status codes)
   - Data models (name, fields, description)
   - Terminology (terms, definitions, categories)
   - Critical sections (sections marked as immutable)

2. **Load existing registry files** (if present):
   - `.spec/registry/api-registry.json`
   - `.spec/registry/data-model-registry.json`
   - `.spec/registry/glossary.json`
   - `.spec/registry/critical-sections-registry.json`

3. **Merge new entries** with existing registry:
   - Add new endpoints/models/terms
   - Update existing entries if owner_spec matches
   - Preserve entries from other specs
   - Detect conflicts (same name, different owner)

4. **Write registry previews**:
   - `.spec/reports/generate-spec/<run-id>/preview/registry/api-registry.json`
   - `.spec/reports/generate-spec/<run-id>/preview/registry/data-model-registry.json`
   - `.spec/reports/generate-spec/<run-id>/preview/registry/glossary.json`
   - `.spec/reports/generate-spec/<run-id>/preview/registry/critical-sections-registry.json`

**Step 6: Apply Registry (only with --apply)**

If `--apply` is set and validation passes:
- Update `.spec/registry/api-registry.json`
- Update `.spec/registry/data-model-registry.json`
- Update `.spec/registry/glossary.json`
- Update `.spec/registry/critical-sections-registry.json`

### 3. Add Registry Templates

Add templates for each registry file showing:
- Required fields
- Optional fields
- Example entries
- Merge logic

### 4. Add Registry Validation

Create validation script:
```bash
python3 .spec/scripts/validate_registry.py \
  --spec specs/<category>/<spec-id>/spec.md \
  --registry .spec/registry/
```

Validation checks:
- All API endpoints from spec are in api-registry.json
- All data models from spec are in data-model-registry.json
- All terms from spec are in glossary.json
- No duplicate entries with different owners
- No orphaned entries (owner_spec doesn't exist)

### 5. Update summary.json Schema

Add registry information:
```json
{
  "registry": {
    "endpoints_added": 5,
    "models_added": 3,
    "terms_added": 7,
    "critical_sections_added": 2,
    "conflicts_detected": 0
  },
  "writes": {
    "reports": ["path"],
    "specs": ["path"],
    "registry": [
      ".spec/registry/api-registry.json",
      ".spec/registry/data-model-registry.json",
      ".spec/registry/glossary.json",
      ".spec/registry/critical-sections-registry.json"
    ]
  }
}
```

---

## Implementation Plan

1. ✅ Analyze workflow documentation
2. ✅ Identify root causes
3. ⏳ Update workflow documentation
4. ⏳ Create validation script
5. ⏳ Test with example spec
6. ⏳ Commit and push changes
7. ⏳ Report findings

---

**Status:** Root cause identified, ready to implement solution
