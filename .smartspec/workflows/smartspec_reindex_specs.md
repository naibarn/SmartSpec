---
description: Re-index SPEC_INDEX.json by scanning all specs and their related files
globs: ["specs/**/*.md", "src/**/*.ts", "src/**/*.tsx", ".smartspec/SPEC_INDEX.json"]
---

# Re-Index Specs and Update SPEC_INDEX.json

You are an expert in analyzing project structure and maintaining metadata. Your task is to scan all specs in the project, identify their related source files, and update `SPEC_INDEX.json` to ensure it's accurate and up-to-date.

## Input

You will receive:
1. **Options** (optional):
   - `--spec <spec-path>` - Re-index specific spec only (e.g., `specs/feature/spec-004-financial-system`)
   - `--verify` - Verify SPEC_INDEX.json without making changes
   - `--external-repo <path>` - Include files from external repository (for shared services)
   - `--force` - Force re-index even if spec hasn't changed

## Your Task

### Phase 1: Scan Specs

1. **Load Current SPEC_INDEX.json**
   ```bash
   cat .smartspec/SPEC_INDEX.json
   ```
   - Parse existing index
   - Note last update timestamps
   - Identify specs that may be outdated

2. **Find All Specs**
   ```bash
   # Find all spec.md files
   find specs -name "spec.md" -type f
   ```
   
   **For each spec found:**
   - Extract spec directory path (e.g., `specs/feature/spec-004-financial-system`)
   - Extract spec ID from directory name or spec.md content
   - Check if spec exists in current SPEC_INDEX.json
   - Check if spec.md has been modified since last index

3. **Display Scan Results**
   ```
   🔍 Spec Scan Results:
   
   📊 Summary:
     Total specs found: 45
     New specs (not in index): 3
     Modified specs (outdated): 7
     Up-to-date specs: 35
   
   🆕 New Specs:
     - specs/feature/spec-046-notification-system
     - specs/feature/spec-047-analytics-dashboard
     - specs/backend/spec-048-data-pipeline
   
   📝 Modified Specs:
     - specs/feature/spec-004-financial-system (modified 2 days ago)
     - specs/feature/spec-012-user-profile (modified 1 day ago)
     ...
   ```

### Phase 2: Analyze Each Spec

For each spec that needs indexing:

1. **Read Spec Content**
   ```bash
   cat specs/feature/spec-004-financial-system/spec.md
   ```
   
   **Extract metadata:**
   - Spec ID (from filename or content)
   - Spec title
   - Spec description
   - Services mentioned
   - Models mentioned
   - APIs mentioned
   - Dependencies on other specs

2. **Identify Related Files**
   
   **Strategy 1: Parse spec.md for file references**
   - Look for code blocks with file paths
   - Look for "Files to modify/create" sections
   - Look for import statements in code examples
   
   **Strategy 2: Search for spec ID in source code**
   ```bash
   # Search for spec ID in comments
   grep -r "spec-004" src/ --include="*.ts" --include="*.tsx"
   ```
   
   **Strategy 3: Analyze tasks.md**
   ```bash
   cat specs/feature/spec-004-financial-system/tasks.md
   ```
   - Extract file paths from task descriptions
   - Extract file paths from implementation notes
   
   **Strategy 4: Infer from service/model names**
   - If spec mentions "CreditService" → look for `src/services/credit.service.ts`
   - If spec mentions "Transaction" model → look for `src/models/transaction.model.ts`
   - If spec mentions "/api/credit" → look for `src/controllers/credit.controller.ts`

3. **Verify File Existence**
   ```bash
   # Check if identified files actually exist
   for file in "${files[@]}"; do
     if [ -f "$file" ]; then
       echo "✅ $file"
     else
       echo "⚠️  $file (mentioned but not found)"
     fi
   done
   ```
   
   **Handle missing files:**
   - If file is mentioned in spec but doesn't exist → mark as "planned" (not yet implemented)
   - Only include existing files in SPEC_INDEX.json
   - Log missing files for reference

4. **Check External Repositories**
   
   If `--external-repo` option is provided:
   ```bash
   # Search in external repo for shared services
   grep -r "spec-004" /path/to/external-repo/src/ --include="*.ts"
   ```
   
   **Include external files:**
   - Prefix external files with repo identifier
   - Example: `@shared/services/common-auth.service.ts`
   - Track external repo path in metadata

5. **Extract Dependencies**
   
   **From spec.md:**
   - Look for "Dependencies" or "Prerequisites" section
   - Look for references to other spec IDs
   
   **From source files:**
   - Analyze imports in related files
   - If `credit.service.ts` imports from `auth.service.ts`
   - And `auth.service.ts` belongs to `spec-001-auth`
   - Then `spec-004` depends on `spec-001`

6. **Display Analysis Results**
   ```
   📋 Spec: spec-004-financial-system
   
   📁 Related Files (8 files):
     ✅ src/services/credit.service.ts
     ✅ src/services/payment.service.ts
     ✅ src/models/transaction.model.ts
     ✅ src/models/credit-score.model.ts
     ✅ src/controllers/credit.controller.ts
     ✅ src/utils/financial-calculator.ts
     ✅ src/validators/transaction.validator.ts
     ✅ src/types/financial.types.ts
   
   🔗 Dependencies (2 specs):
     - spec-001-auth (for authentication)
     - spec-002-database (for data models)
   
   🌐 External Files (1 file):
     - @shared/services/common-payment.service.ts
   ```

### Phase 3: Update SPEC_INDEX.json

1. **Backup Current Index**
   ```bash
   cp .smartspec/SPEC_INDEX.json .smartspec/SPEC_INDEX.json.backup-$(date +%Y%m%d-%H%M%S)
   ```

2. **Build New Index Structure**
   ```json
   {
     "version": "1.0",
     "last_updated": "2024-01-15T10:30:00Z",
     "project_root": "/path/to/project",
     "external_repos": {
       "shared": "/path/to/shared-repo"
     },
     "specs": {
       "spec-004-financial-system": {
         "spec_id": "spec-004-financial-system",
         "title": "Financial System",
         "spec_path": "specs/feature/spec-004-financial-system/spec.md",
         "tasks_path": "specs/feature/spec-004-financial-system/tasks.md",
         "files": [
           "src/services/credit.service.ts",
           "src/services/payment.service.ts",
           "src/models/transaction.model.ts",
           "src/models/credit-score.model.ts",
           "src/controllers/credit.controller.ts",
           "src/utils/financial-calculator.ts",
           "src/validators/transaction.validator.ts",
           "src/types/financial.types.ts"
         ],
         "external_files": [
           "@shared/services/common-payment.service.ts"
         ],
         "dependencies": [
           "spec-001-auth",
           "spec-002-database"
         ],
         "last_indexed": "2024-01-15T10:30:00Z",
         "status": "implemented"
       }
     }
   }
   ```

3. **Merge with Existing Index**
   - Keep specs that are still valid
   - Update specs that have changed
   - Add new specs
   - Mark removed specs as "archived" (don't delete)

4. **Validate Index**
   ```bash
   # Check JSON syntax
   cat .smartspec/SPEC_INDEX.json | jq . > /dev/null
   
   # Verify all file paths exist
   # Verify all dependency specs exist
   # Check for circular dependencies
   ```

5. **Write Updated Index**
   ```bash
   cat > .smartspec/SPEC_INDEX.json << 'EOF'
   {
     "version": "1.0",
     ...
   }
   EOF
   ```

### Phase 4: Generate Report

Create an index report: `.smartspec/reindex-report-YYYYMMDD-HHMMSS.md`

```markdown
# Spec Re-Index Report

Generated: YYYY-MM-DD HH:MM:SS

## Summary

- **Total Specs**: 45
- **New Specs Added**: 3
- **Specs Updated**: 7
- **Specs Unchanged**: 35
- **Archived Specs**: 2

## New Specs

### spec-046-notification-system
- **Path**: specs/feature/spec-046-notification-system
- **Files**: 5 files
  - src/services/notification.service.ts
  - src/models/notification.model.ts
  - src/controllers/notification.controller.ts
  - src/utils/email-sender.ts
  - src/types/notification.types.ts
- **Dependencies**: spec-001-auth, spec-003-user-management

### spec-047-analytics-dashboard
- **Path**: specs/feature/spec-047-analytics-dashboard
- **Files**: 8 files
- **Dependencies**: spec-004-financial-system, spec-012-user-profile

[List all new specs]

## Updated Specs

### spec-004-financial-system
- **Reason**: Modified 2 days ago
- **Changes**:
  - Added: src/utils/interest-calculator.ts
  - Removed: src/utils/old-calculator.ts (file deleted)
  - Updated dependencies: Added spec-005-reporting

### spec-012-user-profile
- **Reason**: Modified 1 day ago
- **Changes**:
  - Added: src/services/avatar.service.ts
  - Added external file: @shared/services/image-processor.service.ts

[List all updated specs]

## Archived Specs

### spec-010-legacy-payment
- **Reason**: Spec directory removed
- **Action**: Marked as archived in index

## External Repositories

### @shared
- **Path**: /path/to/shared-repo
- **Files Used**: 3 files
  - @shared/services/common-payment.service.ts (used by spec-004)
  - @shared/services/common-auth.service.ts (used by spec-001)
  - @shared/services/image-processor.service.ts (used by spec-012)

## Validation Results

✅ All file paths verified
✅ All dependencies exist
✅ No circular dependencies detected
✅ JSON syntax valid

## Index Statistics

- **Total Files Indexed**: 234 files
- **Average Files per Spec**: 5.2 files
- **Specs with External Dependencies**: 8 specs
- **Specs with No Dependencies**: 12 specs

## Backup

Previous index backed up to:
- .smartspec/SPEC_INDEX.json.backup-20240115-103000

## Next Steps

1. Review the updated SPEC_INDEX.json
2. Verify external repository paths are correct
3. Run quality workflows on updated specs:
   - /smartspec_fix_errors <spec-path>
   - /smartspec_generate_tests <spec-path>
   - /smartspec_refactor_code <spec-path>
```

### Phase 5: Display Summary

```
✅ Re-Index Complete!

📊 Results:
  Total Specs: 45
  New: 3
  Updated: 7
  Unchanged: 35
  Archived: 2

📁 Files Indexed:
  Total: 234 files
  Average per spec: 5.2 files

🌐 External Repos:
  @shared: 3 files

📝 Reports:
  - Index: .smartspec/SPEC_INDEX.json
  - Report: .smartspec/reindex-report-YYYYMMDD.md
  - Backup: .smartspec/SPEC_INDEX.json.backup-YYYYMMDD

💡 Next Steps:
  1. Review SPEC_INDEX.json
  2. Verify external repo paths
  3. Run quality workflows on updated specs
  4. Commit changes: git add .smartspec/SPEC_INDEX.json
```

## File Detection Strategies

### Strategy 1: Parse Spec Content

Look for file references in spec.md:

```markdown
## Implementation

Files to create/modify:
- src/services/credit.service.ts
- src/models/transaction.model.ts
```

### Strategy 2: Search by Spec ID

```bash
# Find files that reference this spec in comments
grep -r "spec-004" src/ --include="*.ts" -l
```

### Strategy 3: Analyze Tasks

Parse tasks.md for file paths:

```markdown
- [ ] Implement CreditService in src/services/credit.service.ts
- [ ] Create Transaction model in src/models/transaction.model.ts
```

### Strategy 4: Service/Model Name Inference

If spec mentions:
- "CreditService" → search for `src/services/credit.service.ts`
- "Transaction model" → search for `src/models/transaction.model.ts`
- "POST /api/credit" → search for `src/controllers/credit.controller.ts`

### Strategy 5: Git History

```bash
# Find files modified around the same time as spec
git log --since="2024-01-01" --name-only --pretty=format: specs/feature/spec-004-financial-system/
```

## Handling External Repositories

### Configuration

Add external repo paths to `.smartspec/config.json`:

```json
{
  "external_repos": {
    "shared": {
      "path": "/path/to/shared-repo",
      "description": "Shared services repository"
    },
    "common": {
      "path": "/path/to/common-lib",
      "description": "Common library"
    }
  }
}
```

### Usage

```bash
# Re-index with external repo
/smartspec_reindex_specs --external-repo /path/to/shared-repo

# Re-index specific spec with external repo
/smartspec_reindex_specs --spec specs/feature/spec-004 --external-repo /path/to/shared-repo
```

### External File Format

In SPEC_INDEX.json:

```json
{
  "spec-004-financial-system": {
    "files": [
      "src/services/credit.service.ts"
    ],
    "external_files": [
      "@shared/services/common-payment.service.ts",
      "@common/utils/validator.ts"
    ]
  }
}
```

## Important Notes

- Always backup SPEC_INDEX.json before updating
- Verify all file paths exist before adding to index
- Handle missing files gracefully (mark as planned)
- Support multiple external repositories
- Detect circular dependencies and warn
- Preserve manual edits in SPEC_INDEX.json where possible
- Use timestamps to track when each spec was last indexed
- Archive removed specs instead of deleting them
- Validate JSON syntax after updates
- Generate detailed reports for audit trail

## Example Usage

```bash
# Re-index all specs
/smartspec_reindex_specs

# Re-index specific spec
/smartspec_reindex_specs --spec specs/feature/spec-004-financial-system

# Verify index without changes
/smartspec_reindex_specs --verify

# Re-index with external repo
/smartspec_reindex_specs --external-repo /path/to/shared-repo

# Force re-index even if unchanged
/smartspec_reindex_specs --force

# Re-index specific spec with external repo
/smartspec_reindex_specs --spec specs/feature/spec-004 --external-repo /path/to/shared-repo
```
