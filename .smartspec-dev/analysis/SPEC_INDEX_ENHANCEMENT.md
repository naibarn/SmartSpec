# SPEC_INDEX.json Enhancement Design
## Auto-Creation, Auto-Update, Validation & Cross-Check

**Version:** 1.0.0  
**Date:** 2025-01-04  
**Status:** 🎨 DESIGN PHASE

---

## 🔍 Current Problems

### 1. **No Auto-Creation**
**Problem:**
- SPEC_INDEX.json must be created manually
- New users don't know how to create it
- Workflows fail if it doesn't exist

**Impact:**
- ❌ Poor user experience
- ❌ Workflows stop with errors
- ❌ Manual work required

---

### 2. **No Auto-Update**
**Problem:**
- Create/edit spec → SPEC_INDEX not updated
- Manual update required every time
- Easy to forget → INDEX becomes stale

**Impact:**
- ❌ Stale index
- ❌ Wrong paths/titles
- ❌ Broken references

---

### 3. **No Reference Validation**
**Problem:**
- Spec can reference non-existent specs
- No validation at creation time
- Broken references discovered later

**Impact:**
- ❌ Broken dependencies
- ❌ Implementation blocked
- ❌ Wasted time

---

### 4. **No Cross-Check Tool**
**Problem:**
- No way to check system-wide consistency
- Can't detect:
  - Missing specs
  - Broken references
  - Duplicate specs
  - Orphaned specs

**Impact:**
- ❌ System integrity unknown
- ❌ Hard to maintain
- ❌ Errors accumulate

---

### 5. **No Duplicate Detection**
**Problem:**
- Multiple specs for same feature
- Redundant work
- Confusion about which to use

**Impact:**
- ❌ Wasted effort
- ❌ Inconsistency
- ❌ Maintenance burden

---

## 🎯 Solution Overview

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    SPEC_INDEX.json                          │
│                  (Central Registry)                         │
│                                                             │
│  {                                                          │
│    "version": "5.0",                                        │
│    "specs": [...],                                          │
│    "metadata": {                                            │
│      "last_updated": "...",                                 │
│      "total_specs": 42,                                     │
│      "validation": {...}                                    │
│    }                                                        │
│  }                                                          │
└─────────────────────────────────────────────────────────────┘
                           ▲
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   generate   │  │     edit     │  │   validate   │
│     spec     │  │     spec     │  │     index    │
│              │  │              │  │              │
│ Auto-create  │  │ Auto-update  │  │  Cross-check │
│ Auto-update  │  │  Validate    │  │   Detect     │
└──────────────┘  └──────────────┘  └──────────────┘
```

---

## 📐 Detailed Solutions

### Solution 1: Auto-Creation

**When:** First time generating a spec

**Logic:**
```
IF SPEC_INDEX.json does NOT exist:
  1. Create .smartspec/ directory (if not exists)
  2. Create SPEC_INDEX.json with initial structure
  3. Add current spec as first entry
  4. Log: "✅ Created SPEC_INDEX.json"
  
ELSE:
  Continue with existing INDEX
```

**Initial Structure:**
```json
{
  "version": "5.0",
  "created": "2025-01-04T10:30:00Z",
  "last_updated": "2025-01-04T10:30:00Z",
  "specs": [
    {
      "id": "spec-core-001",
      "title": "Authentication System",
      "path": "specs/core/spec-001-auth",
      "repo": "private",
      "status": "draft",
      "version": "0.1.0",
      "created": "2025-01-04T10:30:00Z",
      "updated": "2025-01-04T10:30:00Z",
      "author": "John Doe",
      "dependencies": [],
      "dependents": []
    }
  ],
  "metadata": {
    "total_specs": 1,
    "by_status": {
      "draft": 1,
      "active": 0,
      "deprecated": 0
    },
    "by_repo": {
      "private": 1,
      "public": 0
    },
    "validation": {
      "last_validated": "2025-01-04T10:30:00Z",
      "status": "valid",
      "errors": [],
      "warnings": []
    }
  }
}
```

**Implementation:**
- Add to `smartspec_generate_spec.md` workflow
- Step 1.1: Check if SPEC_INDEX exists
- Step 1.2: If not, create with initial structure
- Step 1.3: Continue with spec generation

---

### Solution 2: Auto-Update

**When:** After generating or editing a spec

**Logic:**
```
AFTER spec generation/edit:
  1. Load SPEC_INDEX.json
  2. Find entry by spec ID
  3. IF found:
       Update existing entry (title, path, version, updated, etc.)
     ELSE:
       Add new entry
  4. Update metadata (total_specs, last_updated, etc.)
  5. Save SPEC_INDEX.json
  6. Log: "✅ Updated SPEC_INDEX.json"
```

**Update Fields:**
```javascript
// Fields to update
{
  "title": spec.title,              // From spec frontmatter
  "path": spec.path,                // Relative path
  "status": spec.status,            // draft/active/deprecated
  "version": spec.version,          // From spec
  "updated": new Date().toISOString(),
  "author": spec.author,
  "dependencies": spec.dependencies, // From Related Specs section
  "dependents": []                  // Calculated later
}

// Fields to keep
{
  "id": existing.id,                // Never change
  "repo": existing.repo,            // Never change
  "created": existing.created       // Never change
}
```

**Implementation:**
- Add to `smartspec_generate_spec.md` workflow
- Step 15: After spec generation
- Step 15.1: Update SPEC_INDEX
- Step 15.2: Validate and save

---

### Solution 3: Reference Validation

**When:** During spec generation/edit

**Two Modes:**

#### Mode A: Validate Only (Default)
```
WHEN user specifies dependencies:
  1. Load SPEC_INDEX.json
  2. For each dependency ID:
     - Check if exists in INDEX
     - IF NOT found:
       ⚠️ WARNING: "spec-xxx-999 not found in SPEC_INDEX"
       ⚠️ "This spec may not exist or INDEX is stale"
       ⚠️ "Continue? [Y/n]"
  3. Continue with spec generation
  4. Add dependencies to spec (even if not found)
```

#### Mode B: Auto-Add (Optional Flag: --auto-add-refs)
```
WHEN user specifies dependencies AND --auto-add-refs:
  1. Load SPEC_INDEX.json
  2. For each dependency ID:
     - Check if exists in INDEX
     - IF NOT found:
       ⚠️ WARNING: "spec-xxx-999 not found"
       ❓ "Add to SPEC_INDEX as placeholder? [Y/n]"
       
       IF user confirms:
         Add placeholder entry:
         {
           "id": "spec-xxx-999",
           "title": "[PLACEHOLDER - TO BE CREATED]",
           "path": "TBD",
           "repo": "unknown",
           "status": "placeholder",
           "version": "0.0.0",
           "created": now,
           "updated": now,
           "dependencies": [],
           "dependents": [current_spec_id]
         }
  3. Continue with spec generation
```

**Benefits:**
- ✅ Early warning about missing specs
- ✅ Option to add placeholders
- ✅ Track what needs to be created
- ✅ Better planning

**Implementation:**
- Add to `smartspec_generate_spec.md` workflow
- Step 13.1: Validate dependencies
- Step 13.2: Optionally add placeholders
- Step 13.3: Continue with spec

---

### Solution 4: Cross-Check Tool

**New Workflow:** `smartspec_validate_index.md`

**Purpose:**
- Validate SPEC_INDEX.json integrity
- Detect broken references
- Detect duplicate specs
- Detect orphaned specs
- Generate health report

**Command:**
```bash
/smartspec_validate_index [--fix] [--report=detailed]
```

**Checks:**

#### Check 1: File Existence
```
FOR each spec IN SPEC_INDEX:
  spec_path = spec.path + "/spec.md"
  
  IF file NOT exists:
    ERROR: "Spec file not found: {spec_path}"
    SUGGEST: "Remove from INDEX or create spec file"
```

#### Check 2: Broken References
```
FOR each spec IN SPEC_INDEX:
  FOR each dep IN spec.dependencies:
    IF dep NOT IN SPEC_INDEX:
      ERROR: "{spec.id} references non-existent {dep}"
      SUGGEST: "Create {dep} or remove reference"
```

#### Check 3: Circular Dependencies
```
dependency_graph = build_graph(SPEC_INDEX)

IF has_cycle(dependency_graph):
  ERROR: "Circular dependency detected"
  cycles = find_cycles(dependency_graph)
  SHOW: "Cycle: {' → '.join(cycles)} → {cycles[0]}"
  SUGGEST: "Break the cycle by removing one dependency"
```

#### Check 4: Duplicate Specs
```
// By ID
duplicates_by_id = find_duplicates(SPEC_INDEX, by="id")
IF duplicates_by_id:
  ERROR: "Duplicate spec IDs found: {duplicates_by_id}"
  SUGGEST: "Merge or rename duplicate specs"

// By Title (similar)
similar_titles = find_similar(SPEC_INDEX, by="title", threshold=0.8)
IF similar_titles:
  WARNING: "Similar spec titles found:"
  FOR each pair IN similar_titles:
    SHOW: "  - {pair[0].id}: {pair[0].title}"
    SHOW: "  - {pair[1].id}: {pair[1].title}"
    SHOW: "  Similarity: {pair.similarity * 100}%"
  SUGGEST: "Review if these are duplicates"

// By Path
duplicates_by_path = find_duplicates(SPEC_INDEX, by="path")
IF duplicates_by_path:
  ERROR: "Multiple specs at same path: {duplicates_by_path}"
  SUGGEST: "Move one spec to different path"
```

#### Check 5: Orphaned Specs
```
// Specs with no dependents and not referenced by any spec
FOR each spec IN SPEC_INDEX:
  IF spec.dependents.length == 0:
    IF NOT referenced_by_any_spec(spec.id):
      IF spec.status != "core":
        WARNING: "{spec.id} is orphaned (no dependents)"
        SUGGEST: "Review if this spec is still needed"
```

#### Check 6: Stale Specs
```
FOR each spec IN SPEC_INDEX:
  days_since_update = (now - spec.updated) / (24*60*60*1000)
  
  IF days_since_update > 180 AND spec.status == "draft":
    WARNING: "{spec.id} not updated for {days_since_update} days"
    SUGGEST: "Review and update or deprecate"
```

#### Check 7: Metadata Consistency
```
// Count specs
actual_count = SPEC_INDEX.specs.length
metadata_count = SPEC_INDEX.metadata.total_specs

IF actual_count != metadata_count:
  ERROR: "Metadata mismatch: actual={actual_count}, metadata={metadata_count}"
  IF --fix:
    SPEC_INDEX.metadata.total_specs = actual_count
    SAVE SPEC_INDEX
    LOG: "✅ Fixed metadata count"

// Count by status
actual_by_status = count_by(SPEC_INDEX.specs, "status")
metadata_by_status = SPEC_INDEX.metadata.by_status

IF actual_by_status != metadata_by_status:
  ERROR: "Status counts mismatch"
  IF --fix:
    SPEC_INDEX.metadata.by_status = actual_by_status
    SAVE SPEC_INDEX
    LOG: "✅ Fixed status counts"
```

#### Check 8: Dependents Calculation
```
// Recalculate dependents for all specs
FOR each spec IN SPEC_INDEX:
  spec.dependents = []

FOR each spec IN SPEC_INDEX:
  FOR each dep IN spec.dependencies:
    dep_spec = find_spec(dep)
    IF dep_spec:
      dep_spec.dependents.push(spec.id)

IF --fix:
  SAVE SPEC_INDEX
  LOG: "✅ Recalculated dependents"
```

**Output Report:**

```markdown
# SPEC_INDEX Validation Report
**Date:** 2025-01-04 10:30:00
**SPEC_INDEX:** .smartspec/SPEC_INDEX.json
**Total Specs:** 42

---

## ✅ Summary

- **Status:** ⚠️ WARNINGS FOUND
- **Errors:** 2
- **Warnings:** 5
- **Passed Checks:** 6/8

---

## ❌ Errors (2)

### 1. Broken Reference
**Spec:** spec-feature-005 (Payment Gateway)
**Issue:** References non-existent spec-core-999
**Suggestion:** Create spec-core-999 or remove reference

### 2. Duplicate Path
**Specs:** spec-feature-010, spec-feature-011
**Issue:** Both use path "specs/feature/spec-010-notifications"
**Suggestion:** Move one spec to different path

---

## ⚠️ Warnings (5)

### 1. Orphaned Spec
**Spec:** spec-feature-020 (Legacy API)
**Issue:** No dependents, not referenced by any spec
**Suggestion:** Review if still needed

### 2. Similar Titles
**Specs:** spec-feature-015, spec-feature-016
**Titles:**
  - spec-feature-015: "User Authentication"
  - spec-feature-016: "User Authorization"
**Similarity:** 85%
**Suggestion:** Review if these are duplicates

### 3. Stale Spec
**Spec:** spec-feature-008 (Analytics Dashboard)
**Issue:** Not updated for 245 days
**Suggestion:** Review and update or deprecate

### 4. Metadata Mismatch
**Issue:** Actual count (42) != Metadata count (40)
**Fix Available:** Yes (--fix flag)

### 5. Dependents Not Calculated
**Issue:** Some specs have empty dependents array
**Fix Available:** Yes (--fix flag)

---

## ✅ Passed Checks (6)

1. ✅ All spec files exist
2. ✅ No circular dependencies
3. ✅ No duplicate IDs
4. ✅ No duplicate paths (except 1 error above)
5. ✅ All dependencies exist (except 1 error above)
6. ✅ Metadata version correct

---

## 🔧 Auto-Fix Available

Run with `--fix` flag to automatically fix:
- Metadata counts
- Dependents calculation
- Timestamps

Cannot auto-fix (manual action required):
- Broken references
- Duplicate paths
- Orphaned specs

---

## 📊 Statistics

**By Status:**
- Draft: 15
- Active: 25
- Deprecated: 2

**By Repo:**
- Private: 40
- Public: 2

**By Category:**
- Core: 5
- Feature: 30
- Infrastructure: 7

**Dependency Depth:**
- Max depth: 4 levels
- Average depth: 2.1 levels

**Health Score:** 85/100
- Deductions:
  - Errors: -10 (2 errors × 5 points)
  - Warnings: -5 (5 warnings × 1 point)

---

## 🎯 Recommendations

### High Priority
1. Fix broken reference in spec-feature-005
2. Resolve duplicate path for spec-feature-010/011

### Medium Priority
3. Review orphaned spec-feature-020
4. Update stale spec-feature-008
5. Run with --fix to update metadata

### Low Priority
6. Review similar titles (spec-feature-015/016)
7. Consider deprecating old specs

---

## 🚀 Next Steps

1. **Fix Errors:**
   ```bash
   # Fix broken reference
   /smartspec_edit_spec specs/feature/spec-005-payment
   # Remove spec-core-999 from dependencies
   
   # Fix duplicate path
   /smartspec_edit_spec specs/feature/spec-011-notifications-v2
   # Move to different path
   ```

2. **Run Auto-Fix:**
   ```bash
   /smartspec_validate_index --fix
   ```

3. **Review Warnings:**
   ```bash
   # Review orphaned spec
   /smartspec_view_spec specs/feature/spec-020-legacy-api
   
   # Update stale spec
   /smartspec_edit_spec specs/feature/spec-008-analytics
   ```

4. **Re-validate:**
   ```bash
   /smartspec_validate_index
   ```

---

**Report saved to:** .smartspec/reports/validation-report-20250104-103000.md
```

**Implementation:**
- Create new workflow: `smartspec_validate_index.md`
- Implement all 8 checks
- Generate detailed report
- Support --fix flag for auto-fixes
- Support --report=detailed for full report

---

### Solution 5: Duplicate Detection

**Algorithm:**

```javascript
function detectDuplicates(specs) {
  const duplicates = {
    by_id: [],
    by_path: [],
    by_title_exact: [],
    by_title_similar: []
  };
  
  // By ID
  const ids = specs.map(s => s.id);
  duplicates.by_id = findDuplicates(ids);
  
  // By Path
  const paths = specs.map(s => s.path);
  duplicates.by_path = findDuplicates(paths);
  
  // By Title (exact)
  const titles = specs.map(s => s.title.toLowerCase());
  duplicates.by_title_exact = findDuplicates(titles);
  
  // By Title (similar - Levenshtein distance)
  for (let i = 0; i < specs.length; i++) {
    for (let j = i + 1; j < specs.length; j++) {
      const similarity = calculateSimilarity(
        specs[i].title,
        specs[j].title
      );
      
      if (similarity > 0.8) { // 80% similar
        duplicates.by_title_similar.push({
          spec1: specs[i],
          spec2: specs[j],
          similarity: similarity
        });
      }
    }
  }
  
  return duplicates;
}

function calculateSimilarity(str1, str2) {
  // Levenshtein distance algorithm
  const len1 = str1.length;
  const len2 = str2.length;
  const matrix = [];
  
  for (let i = 0; i <= len1; i++) {
    matrix[i] = [i];
  }
  
  for (let j = 0; j <= len2; j++) {
    matrix[0][j] = j;
  }
  
  for (let i = 1; i <= len1; i++) {
    for (let j = 1; j <= len2; j++) {
      const cost = str1[i - 1] === str2[j - 1] ? 0 : 1;
      matrix[i][j] = Math.min(
        matrix[i - 1][j] + 1,
        matrix[i][j - 1] + 1,
        matrix[i - 1][j - 1] + cost
      );
    }
  }
  
  const distance = matrix[len1][len2];
  const maxLen = Math.max(len1, len2);
  return 1 - (distance / maxLen);
}
```

**Integration:**
- Add to `smartspec_validate_index.md` workflow
- Check 4: Duplicate Detection
- Report all types of duplicates
- Suggest actions

---

## 🔄 Workflow Integration

### Modified Workflows (2)

#### 1. smartspec_generate_spec.md

**Changes:**

**Step 1.1: Check and Create SPEC_INDEX** (NEW)
```
IF SPEC_INDEX.json does NOT exist:
  1. Create .smartspec/ directory
  2. Create SPEC_INDEX.json with initial structure
  3. Log: "✅ Created SPEC_INDEX.json"

Load SPEC_INDEX.json into SPEC_REGISTRY
```

**Step 13.1: Validate Dependencies** (ENHANCED)
```
FOR each dependency IN spec.dependencies:
  IF dependency NOT IN SPEC_REGISTRY:
    ⚠️ WARNING: "{dependency} not found in SPEC_INDEX"
    
    IF --auto-add-refs flag:
      ❓ "Add as placeholder? [Y/n]"
      IF yes:
        Add placeholder to SPEC_REGISTRY
```

**Step 15: Update SPEC_INDEX** (NEW)
```
AFTER spec generation:
  1. Load SPEC_INDEX.json
  2. Find entry by spec.id
  3. IF found:
       Update entry (title, path, version, updated, etc.)
     ELSE:
       Add new entry
  4. Update metadata
  5. Save SPEC_INDEX.json
  6. Log: "✅ Updated SPEC_INDEX.json"
```

---

#### 2. smartspec_generate_tasks.md

**Changes:**

**Step 0.2: Check and Create SPEC_INDEX** (ENHANCED)
```
IF SPEC_INDEX.json does NOT exist:
  ⚠️ WARNING: "SPEC_INDEX.json not found"
  ❓ "Create new SPEC_INDEX.json? [Y/n]"
  
  IF yes:
    Create SPEC_INDEX.json with initial structure
    Add current spec
    Log: "✅ Created SPEC_INDEX.json"
  ELSE:
    Continue without SPEC_INDEX
    Log: "⚠️ Continuing without dependency resolution"
```

---

### New Workflows (1)

#### 3. smartspec_validate_index.md (NEW)

**Purpose:** Validate SPEC_INDEX.json integrity

**Command:**
```bash
/smartspec_validate_index [--fix] [--report=detailed]
```

**Workflow:**
```
1. Load SPEC_INDEX.json
2. Run 8 validation checks:
   - File existence
   - Broken references
   - Circular dependencies
   - Duplicate specs
   - Orphaned specs
   - Stale specs
   - Metadata consistency
   - Dependents calculation
3. Generate report
4. IF --fix:
     Apply auto-fixes
     Save SPEC_INDEX.json
5. Output report
```

---

## 📊 Impact Analysis

### Before (Current State)

**SPEC_INDEX Management:**
- ❌ Manual creation required
- ❌ Manual updates required
- ❌ No validation
- ❌ No cross-check
- ❌ No duplicate detection

**User Experience:**
- 😞 Frustrating (manual work)
- 🐛 Error-prone (easy to forget)
- 🔍 Hard to maintain (no tools)
- ⏱️ Time-consuming (manual checks)

**System Health:**
- ❓ Unknown integrity
- 🔗 Broken references possible
- 📦 Duplicates accumulate
- 🗑️ Orphaned specs undetected

---

### After (Enhanced State)

**SPEC_INDEX Management:**
- ✅ Auto-creation
- ✅ Auto-update
- ✅ Validation on create/edit
- ✅ Cross-check tool
- ✅ Duplicate detection

**User Experience:**
- 😊 Seamless (automatic)
- ✅ Reliable (validated)
- 🔧 Easy to maintain (tools provided)
- ⚡ Fast (automated checks)

**System Health:**
- ✅ Known integrity (validation report)
- 🔗 No broken references (validated)
- 📦 No duplicates (detected and reported)
- 🗑️ Orphaned specs identified

---

## 🎯 Success Criteria

### Must Have ✅

- [ ] Auto-create SPEC_INDEX.json on first spec
- [ ] Auto-update SPEC_INDEX.json on spec create/edit
- [ ] Validate dependencies during spec generation
- [ ] New workflow: smartspec_validate_index
- [ ] 8 validation checks implemented
- [ ] Duplicate detection working
- [ ] Detailed validation report

### Should Have 💡

- [ ] --auto-add-refs flag for placeholders
- [ ] --fix flag for auto-fixes
- [ ] --report=detailed for full report
- [ ] Health score calculation
- [ ] Recommendations in report

### Nice to Have 🌟

- [ ] Interactive mode for validation
- [ ] Dashboard for SPEC_INDEX health
- [ ] Automated validation on commit (git hook)
- [ ] Integration with CI/CD

---

## 📅 Implementation Plan

### Phase 1: Auto-Creation & Auto-Update (Week 1)

**Tasks:**
1. ✅ Design solution (this document)
2. ⏳ Modify smartspec_generate_spec.md
   - Add Step 1.1: Check and create SPEC_INDEX
   - Add Step 15: Update SPEC_INDEX
3. ⏳ Modify smartspec_generate_tasks.md
   - Enhance Step 0.2: Check and create SPEC_INDEX
4. ⏳ Test with real specs
5. ⏳ Document changes

**Deliverables:**
- Modified workflows (2)
- Test cases
- Documentation

---

### Phase 2: Reference Validation (Week 2)

**Tasks:**
1. ⏳ Enhance smartspec_generate_spec.md
   - Add Step 13.1: Validate dependencies
   - Add --auto-add-refs flag support
2. ⏳ Implement placeholder creation
3. ⏳ Test validation logic
4. ⏳ Document flag usage

**Deliverables:**
- Enhanced validation
- Placeholder support
- Documentation

---

### Phase 3: Cross-Check Tool (Week 3)

**Tasks:**
1. ⏳ Create smartspec_validate_index.md workflow
2. ⏳ Implement 8 validation checks
3. ⏳ Implement duplicate detection algorithm
4. ⏳ Implement report generation
5. ⏳ Test with real SPEC_INDEX
6. ⏳ Document workflow

**Deliverables:**
- New workflow
- Validation checks (8)
- Report template
- Documentation

---

### Phase 4: Auto-Fix & Polish (Week 4)

**Tasks:**
1. ⏳ Implement --fix flag
2. ⏳ Implement auto-fixes for:
   - Metadata counts
   - Dependents calculation
   - Timestamps
3. ⏳ Implement health score calculation
4. ⏳ Enhance report with recommendations
5. ⏳ Test all features
6. ⏳ Final documentation

**Deliverables:**
- Auto-fix feature
- Health score
- Complete documentation
- User guide

---

## 🔧 Technical Details

### SPEC_INDEX.json Schema (Enhanced)

```typescript
interface SpecIndex {
  version: string;                    // "5.0"
  created: string;                    // ISO 8601 timestamp
  last_updated: string;               // ISO 8601 timestamp
  specs: Spec[];
  metadata: Metadata;
}

interface Spec {
  id: string;                         // "spec-core-001"
  title: string;                      // "Authentication System"
  path: string;                       // "specs/core/spec-001-auth"
  repo: string;                       // "private" | "public"
  status: SpecStatus;                 // "draft" | "active" | "deprecated" | "placeholder"
  version: string;                    // "1.0.0"
  created: string;                    // ISO 8601 timestamp
  updated: string;                    // ISO 8601 timestamp
  author: string;                     // "John Doe"
  dependencies: string[];             // ["spec-core-002", ...]
  dependents: string[];               // ["spec-feature-005", ...]
}

type SpecStatus = "draft" | "active" | "deprecated" | "placeholder";

interface Metadata {
  total_specs: number;
  by_status: Record<SpecStatus, number>;
  by_repo: Record<string, number>;
  validation: ValidationMetadata;
}

interface ValidationMetadata {
  last_validated: string;             // ISO 8601 timestamp
  status: "valid" | "warnings" | "errors";
  errors: ValidationError[];
  warnings: ValidationWarning[];
  health_score: number;               // 0-100
}

interface ValidationError {
  type: string;                       // "broken_reference" | "duplicate_path" | ...
  spec_id: string;                    // Affected spec
  message: string;                    // Error description
  suggestion: string;                 // How to fix
}

interface ValidationWarning {
  type: string;                       // "orphaned" | "stale" | "similar_title" | ...
  spec_id: string;                    // Affected spec
  message: string;                    // Warning description
  suggestion: string;                 // Recommendation
}
```

---

### Validation Check Details

#### Check 1: File Existence
```typescript
function validateFileExistence(specs: Spec[]): ValidationError[] {
  const errors: ValidationError[] = [];
  
  for (const spec of specs) {
    const specPath = `${spec.path}/spec.md`;
    
    if (!fileExists(specPath)) {
      errors.push({
        type: "file_not_found",
        spec_id: spec.id,
        message: `Spec file not found: ${specPath}`,
        suggestion: "Remove from INDEX or create spec file"
      });
    }
  }
  
  return errors;
}
```

#### Check 2: Broken References
```typescript
function validateReferences(specs: Spec[]): ValidationError[] {
  const errors: ValidationError[] = [];
  const specIds = new Set(specs.map(s => s.id));
  
  for (const spec of specs) {
    for (const dep of spec.dependencies) {
      if (!specIds.has(dep)) {
        errors.push({
          type: "broken_reference",
          spec_id: spec.id,
          message: `${spec.id} references non-existent ${dep}`,
          suggestion: `Create ${dep} or remove reference`
        });
      }
    }
  }
  
  return errors;
}
```

#### Check 3: Circular Dependencies
```typescript
function validateCircularDependencies(specs: Spec[]): ValidationError[] {
  const errors: ValidationError[] = [];
  const graph = buildDependencyGraph(specs);
  const cycles = findCycles(graph);
  
  for (const cycle of cycles) {
    errors.push({
      type: "circular_dependency",
      spec_id: cycle[0],
      message: `Circular dependency: ${cycle.join(' → ')} → ${cycle[0]}`,
      suggestion: "Break the cycle by removing one dependency"
    });
  }
  
  return errors;
}

function buildDependencyGraph(specs: Spec[]): Map<string, string[]> {
  const graph = new Map<string, string[]>();
  
  for (const spec of specs) {
    graph.set(spec.id, spec.dependencies);
  }
  
  return graph;
}

function findCycles(graph: Map<string, string[]>): string[][] {
  const cycles: string[][] = [];
  const visited = new Set<string>();
  const stack = new Set<string>();
  
  function dfs(node: string, path: string[]) {
    if (stack.has(node)) {
      // Found cycle
      const cycleStart = path.indexOf(node);
      cycles.push(path.slice(cycleStart));
      return;
    }
    
    if (visited.has(node)) {
      return;
    }
    
    visited.add(node);
    stack.add(node);
    path.push(node);
    
    const neighbors = graph.get(node) || [];
    for (const neighbor of neighbors) {
      dfs(neighbor, [...path]);
    }
    
    stack.delete(node);
  }
  
  for (const node of graph.keys()) {
    if (!visited.has(node)) {
      dfs(node, []);
    }
  }
  
  return cycles;
}
```

#### Check 4: Duplicate Detection
```typescript
function validateDuplicates(specs: Spec[]): {
  errors: ValidationError[];
  warnings: ValidationWarning[];
} {
  const errors: ValidationError[] = [];
  const warnings: ValidationWarning[] = [];
  
  // By ID
  const idCounts = countBy(specs, 'id');
  for (const [id, count] of Object.entries(idCounts)) {
    if (count > 1) {
      errors.push({
        type: "duplicate_id",
        spec_id: id,
        message: `Duplicate spec ID: ${id} (${count} occurrences)`,
        suggestion: "Merge or rename duplicate specs"
      });
    }
  }
  
  // By Path
  const pathCounts = countBy(specs, 'path');
  for (const [path, count] of Object.entries(pathCounts)) {
    if (count > 1) {
      errors.push({
        type: "duplicate_path",
        spec_id: specs.find(s => s.path === path)!.id,
        message: `Multiple specs at path: ${path}`,
        suggestion: "Move one spec to different path"
      });
    }
  }
  
  // By Title (similar)
  for (let i = 0; i < specs.length; i++) {
    for (let j = i + 1; j < specs.length; j++) {
      const similarity = calculateSimilarity(
        specs[i].title,
        specs[j].title
      );
      
      if (similarity > 0.8) {
        warnings.push({
          type: "similar_title",
          spec_id: specs[i].id,
          message: `Similar titles: "${specs[i].title}" and "${specs[j].title}" (${Math.round(similarity * 100)}% similar)`,
          suggestion: "Review if these are duplicates"
        });
      }
    }
  }
  
  return { errors, warnings };
}
```

---

## 📚 Documentation Updates

### README.md

**Add section:**

```markdown
### SPEC_INDEX.json Management

SmartSpec V5 automatically manages SPEC_INDEX.json:

**Auto-Creation:**
- First spec generation creates SPEC_INDEX.json automatically
- No manual setup required

**Auto-Update:**
- Every spec create/edit updates SPEC_INDEX.json
- Keeps index synchronized with specs

**Validation:**
- Dependencies validated during spec generation
- Warnings for missing specs
- Option to add placeholders

**Cross-Check:**
- Use `/smartspec_validate_index` to check system health
- Detects broken references, duplicates, orphaned specs
- Generates detailed health report
- Auto-fix available for common issues

**Example:**
```bash
# Generate spec (auto-creates/updates INDEX)
/smartspec_generate_spec "Authentication System" --profile=technical

# Validate INDEX
/smartspec_validate_index

# Validate and auto-fix
/smartspec_validate_index --fix

# Detailed report
/smartspec_validate_index --report=detailed
```
```

---

## 🎉 Summary

**Problems Solved: 5**
1. ✅ Auto-creation of SPEC_INDEX.json
2. ✅ Auto-update on spec create/edit
3. ✅ Reference validation during generation
4. ✅ Cross-check tool for system health
5. ✅ Duplicate detection

**Workflows Modified: 2**
1. smartspec_generate_spec.md
2. smartspec_generate_tasks.md

**Workflows Created: 1**
1. smartspec_validate_index.md (NEW)

**Features Added: 10**
1. Auto-create SPEC_INDEX
2. Auto-update SPEC_INDEX
3. Dependency validation
4. Placeholder support (--auto-add-refs)
5. 8 validation checks
6. Duplicate detection
7. Health score calculation
8. Auto-fix (--fix)
9. Detailed report (--report=detailed)
10. Recommendations

**Impact:**
- 😊 Better user experience (automatic)
- ✅ Higher reliability (validated)
- 🔧 Easier maintenance (tools provided)
- 📊 Known system health (reports)

---

**Status:** 🎨 DESIGN COMPLETE  
**Next:** 💻 IMPLEMENTATION  
**Timeline:** 4 weeks (4 phases)
