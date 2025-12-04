# `/smartspec_reindex_specs`

**Re-indexes SPEC_INDEX.json to keep it accurate and up-to-date with the actual codebase.**

---

## 1. Summary

This workflow maintains the accuracy of `SPEC_INDEX.json`, which is the central registry mapping each spec to its related source files. Over time, this index can become outdated as files are added, removed, or renamed. This command uses **5 intelligent file detection strategies** to automatically discover and update file associations.

- **What it solves:** Prevents SPEC_INDEX.json from becoming stale, which would cause quality workflows to scan wrong files or miss important ones.
- **When to use it:** After major code changes, before running quality workflows, weekly maintenance, or when integrating external repositories.

---

## 2. Usage

```bash
/smartspec_reindex_specs [options...]
```

---

## 3. Parameters & Options

### **Primary Options**

| Option | Type | Default | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `--spec` | `string` | All specs | Re-index only a specific spec instead of all specs | `--spec specs/feature/spec-004-financial-system` |
| `--verify` | `flag` | `false` | Verify SPEC_INDEX.json without making changes | `--verify` |
| `--external-repo` | `string` | None | Path to external repository for shared services | `--external-repo /path/to/shared-repo` |
| `--force` | `flag` | `false` | Force re-index even if files haven't changed | `--force` |

### **Output Options**

| Option | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `--report` | `string` | Auto-generated | Path to save detailed report | `--report reindex-report.md` |
| `--no-backup` | `flag` | `false` | Skip automatic backup before update | `--no-backup` |
| `--quiet` | `flag` | `false` | Suppress progress output | `--quiet` |

---

## 4. Examples

### Re-Index All Specs

```bash
/smartspec_reindex_specs
```

**What happens:**
1. Scans all specs in `specs/` directory
2. Runs 5 file detection strategies for each spec
3. Backs up current SPEC_INDEX.json
4. Updates SPEC_INDEX.json with new findings
5. Generates detailed report

**Output:**
```
🔍 Re-indexing all specs...

📊 Progress:
  [1/10] spec-001-auth-system... ✅ 5 files found
  [2/10] spec-002-database... ✅ 3 files found
  [3/10] spec-003-api-gateway... ✅ 7 files found
  ...

✅ Re-index complete!
  - Total specs: 10
  - Total files: 87
  - High confidence: 72 files
  - Medium confidence: 12 files
  - Low confidence: 3 files (excluded)

📄 Report saved to: .smartspec/reindex-report-2024-01-15.md
💾 Backup saved to: .smartspec/backups/SPEC_INDEX-2024-01-15.json
```

---

### Re-Index Specific Spec

```bash
/smartspec_reindex_specs --spec specs/feature/spec-004-financial-system
```

**Use case:** You've just modified spec-004 and want to update only its entry.

**Output:**
```
🔍 Re-indexing spec-004-financial-system...

📝 File Detection Results:
  Strategy 1 (Parse spec.md): 4 files
  Strategy 2 (Search by ID): 6 files
  Strategy 3 (Analyze tasks.md): 5 files
  Strategy 4 (Inference): 7 files
  Strategy 5 (Git History): 8 files

✅ Merged Results:
  - src/services/credit.service.ts (Confidence: 100%)
  - src/services/payment.service.ts (Confidence: 95%)
  - src/models/transaction.model.ts (Confidence: 100%)
  - src/controllers/credit.controller.ts (Confidence: 90%)
  - src/utils/financial-calculator.ts (Confidence: 70%)

📊 Updated SPEC_INDEX.json:
  - Added: 2 new files
  - Removed: 1 deleted file
  - Unchanged: 3 files
```

---

### Verify Without Changes

```bash
/smartspec_reindex_specs --verify
```

**Use case:** Check for issues before making changes.

**Output:**
```
🔍 Verifying SPEC_INDEX.json...

⚠️  Issues Found:

spec-004-financial-system:
  ❌ Missing file: src/services/old-payment.service.ts (deleted)
  ⚠️  New file detected: src/services/new-payment.service.ts (not in index)
  ✅ 3 files verified

spec-005-notification:
  ⚠️  Outdated: Last indexed 30 days ago
  ✅ All files exist

📊 Summary:
  - Total specs: 10
  - Issues found: 3
  - Missing files: 1
  - New files: 1
  - Outdated entries: 1

💡 Recommendation: Run without --verify to fix issues
```

---

### Include External Repository

```bash
/smartspec_reindex_specs --external-repo /path/to/shared-services
```

**Use case:** Your project shares services with another repository.

**Output:**
```
🔍 Re-indexing with external repository...
📂 External repo: /path/to/shared-services

📊 spec-004-financial-system:
  Local files: 5
  External files: 2
    - @shared/services/common-payment.service.ts
    - @shared/utils/currency-converter.ts

✅ SPEC_INDEX.json updated:
{
  "external_repos": {
    "shared": "/path/to/shared-services"
  },
  "specs": {
    "spec-004-financial-system": {
      "files": [
        "src/services/credit.service.ts",
        "src/services/payment.service.ts"
      ],
      "external_files": [
        "@shared/services/common-payment.service.ts",
        "@shared/utils/currency-converter.ts"
      ]
    }
  }
}
```

---

## 5. How It Works: 5 File Detection Strategies

The re-index workflow uses **5 complementary strategies** to find files related to each spec. Each strategy covers different scenarios, and combining them achieves **95%+ coverage** in typical projects.

### Strategy 1: Parse spec.md

**How it works:** Reads `spec.md` content to find explicitly mentioned file paths.

**Patterns detected:**
- Markdown lists: `- \`src/services/credit.service.ts\` - Description`
- Code block headers: `// File: src/utils/helper.ts`
- Inline code: `\`src/services/credit.service.ts\``
- File sections: `File: src/controllers/credit.controller.ts`

**Example:**
```markdown
## Implementation

### Files to Create
- `src/services/credit.service.ts` - Credit calculation service
- `src/services/payment.service.ts` - Payment processing service
```

**Result:** Finds `credit.service.ts` and `payment.service.ts` with **high confidence (100%)**.

**Pros:**
- ✅ High accuracy (data from spec author)
- ✅ Includes file descriptions

**Cons:**
- ❌ Requires well-written spec
- ❌ May become outdated if not maintained

---

### Strategy 2: Search by Spec ID

**How it works:** Searches source code for comments that reference the spec ID.

**Patterns detected:**
- JSDoc comments: `@see spec-004-financial-system`
- Implementation comments: `// Implements: SPEC-004`
- TODO comments: `// TODO: spec-004 - Add validation`
- Inline references: `// Related to: spec-004`

**Example:**
```typescript
/**
 * Credit Service
 * Implements: SPEC-004 Financial System
 * @see specs/feature/spec-004-financial-system/spec.md
 */
export class CreditService {
  // SPEC-004: Calculate credit score
  calculateCreditScore(userId: string): number {
    // Implementation
  }
}
```

**Result:** Finds `credit.service.ts` with **high confidence (100%)**.

**Pros:**
- ✅ Finds actually implemented files
- ✅ Auto-updates as developers add comments

**Cons:**
- ❌ Requires developers to write comments
- ❌ May have false positives (files that mention but don't implement)

---

### Strategy 3: Analyze tasks.md

**How it works:** Extracts file paths from task descriptions in `tasks.md`.

**Patterns detected:**
- Task files: `File: \`src/services/credit.service.ts\``
- Locations: `Location: \`src/utils/helper.ts\``
- Inline mentions: `in \`src/services/payment.service.ts\``
- Implementation notes: `Modified \`src/config/database.config.ts\``

**Example:**
```markdown
## Phase 1: Core Services

- [ ] **Task 1.1:** Implement CreditService
  - File: `src/services/credit.service.ts`
  - Methods: `calculateCreditScore()`, `calculateInterest()`

- [x] **Task 1.2:** Create Transaction model
  - File: `src/models/transaction.model.ts`
  - Status: ✅ Completed
```

**Result:** Finds both files with **high confidence (100%)** and knows which are completed.

**Pros:**
- ✅ Detailed context (task descriptions, status)
- ✅ Tracks implementation progress

**Cons:**
- ❌ Requires tasks.md to exist
- ❌ May become outdated if not maintained

---

### Strategy 4: Service/Model Name Inference

**How it works:** Infers file paths from entity names (services, models, controllers) mentioned in spec, using standard naming conventions.

**Naming conventions:**
- `CreditService` → `src/services/credit.service.ts`
- `Transaction` (model) → `src/models/transaction.model.ts`
- `CreditController` → `src/controllers/credit.controller.ts`
- `FinancialCalculator` (utility) → `src/utils/financial-calculator.ts`

**Example:**
```markdown
## Services

### CreditService
Calculates credit scores and interest rates.

### PaymentService
Processes payments and refunds.

## Models

### Transaction
Represents a financial transaction.
```

**Result:** Infers 3 file paths and verifies they exist, **medium confidence (70%)**.

**Pros:**
- ✅ Works with specs that don't list file paths
- ✅ Works with old/legacy specs
- ✅ Automatic based on conventions

**Cons:**
- ❌ Requires consistent naming conventions
- ❌ Lower confidence (inference, not explicit)
- ❌ May miss files in custom locations

---

### Strategy 5: Git History Analysis

**How it works:** Analyzes Git commit history to find files that were modified around the same time as the spec, or in commits that mention the spec ID.

**Techniques:**
1. Find commits with spec ID in message: `git log --grep="spec-004"`
2. Find files in those commits
3. Find files modified ±7 days from spec creation
4. Find files by same author around same time

**Example:**
```bash
$ git log --grep="spec-004" --oneline

abc123 feat(spec-004): Implement financial system
def456 feat(spec-004): Add credit service
ghi789 feat(spec-004): Add payment service
```

**Result:** Finds all files modified in those commits, **medium confidence (60%)**.

**Pros:**
- ✅ Finds actually implemented files
- ✅ No manual tracking needed
- ✅ Catches files not documented elsewhere

**Cons:**
- ❌ Requires Git repository
- ❌ May have false positives (unrelated files in same commits)
- ❌ Lower confidence (time-based correlation)

---

## 6. Strategy Comparison Matrix

| Aspect | Strategy 1 | Strategy 2 | Strategy 3 | Strategy 4 | Strategy 5 |
|--------|-----------|-----------|-----------|-----------|-----------|
| **Source** | spec.md | Code comments | tasks.md | Naming convention | Git history |
| **Accuracy** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **Coverage** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Confidence** | 1.0 | 1.0 | 1.0 | 0.7 | 0.6 |
| **Auto-update** | ❌ | ✅ | ❌ | ✅ | ✅ |
| **Speed** | Very Fast | Medium | Very Fast | Fast | Slow |
| **Best for** | New specs | Active dev | Tracked tasks | Standard projects | Historical analysis |

**Combined Coverage:** **95%+** in typical projects 🎯

---

## 7. Confidence Scoring

Files found by multiple strategies receive higher confidence scores:

| Found By | Confidence | Action |
|----------|-----------|--------|
| All 5 strategies | 95-100% | ✅ Auto-include (very high confidence) |
| Strategies 1, 2, 3 | 90-95% | ✅ Auto-include (high confidence) |
| Strategies 2, 4, 5 | 70-80% | ✅ Include (medium-high confidence) |
| Strategy 4 or 5 only | 60-70% | ⚠️ Include with warning (medium confidence) |
| Strategy 5 only | 40-60% | ❌ Exclude (low confidence, likely false positive) |

**Example:**

```json
{
  "path": "src/services/credit.service.ts",
  "confidence": 100,
  "found_by": ["parse_spec", "search_id", "tasks", "inference", "git"],
  "sources": {
    "parse_spec": "Listed in spec.md",
    "search_id": "Comment: 'Implements: SPEC-004'",
    "tasks": "Task 1.1: Implement CreditService",
    "inference": "Inferred from 'CreditService'",
    "git": "Commit def456: feat(spec-004): Add credit service"
  }
}
```

---

## 8. SPEC_INDEX.json Structure

After re-indexing, SPEC_INDEX.json will have this structure:

```json
{
  "version": "1.0",
  "last_updated": "2024-01-15T10:30:00Z",
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
        "src/controllers/credit.controller.ts"
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

---

## 9. Safety Features

### Automatic Backup

Before updating SPEC_INDEX.json, a backup is automatically created:

```
.smartspec/backups/
  ├── SPEC_INDEX-2024-01-15-103000.json
  ├── SPEC_INDEX-2024-01-14-150000.json
  └── SPEC_INDEX-2024-01-13-120000.json
```

**Restore from backup:**
```bash
cp .smartspec/backups/SPEC_INDEX-2024-01-15-103000.json SPEC_INDEX.json
```

### Validation

The workflow validates SPEC_INDEX.json before and after updates:

- ✅ Valid JSON syntax
- ✅ All referenced files exist
- ✅ No circular dependencies
- ✅ No duplicate entries
- ✅ All required fields present

### Detailed Report

Every re-index generates a detailed report:

```markdown
# Re-Index Report - 2024-01-15 10:30:00

## Summary
- Total specs processed: 10
- Total files found: 87
- High confidence: 72 files
- Medium confidence: 12 files
- Low confidence: 3 files (excluded)

## Changes
- Added: 5 new files
- Removed: 2 deleted files
- Updated: 3 files (confidence changed)
- Unchanged: 77 files

## spec-004-financial-system

### Files Found (5)

#### ✅ src/services/credit.service.ts
- **Confidence:** 100%
- **Found by:** parse_spec, search_id, tasks, inference, git
- **Sources:**
  - parse_spec: Listed in spec.md (line 45)
  - search_id: Comment in file: "Implements: SPEC-004"
  - tasks: Task 1.1: Implement CreditService
  - inference: Inferred from service name "CreditService"
  - git: Commit def456 (2024-01-10): "feat(spec-004): Add credit service"

#### ✅ src/services/payment.service.ts
- **Confidence:** 95%
- **Found by:** parse_spec, search_id, tasks, git
- **Sources:**
  - parse_spec: Listed in spec.md (line 46)
  - search_id: Comment in file: "Related to: spec-004"
  - tasks: Task 1.2: Implement PaymentService
  - git: Commit ghi789 (2024-01-11): "feat(spec-004): Add payment service"

### Changes
- ✅ Added: src/utils/financial-calculator.ts (new file detected)
- ❌ Removed: src/services/old-payment.service.ts (file deleted)
```

---

## 10. When to Re-Index

### Recommended Times

1. **After major changes** - When you've added/removed multiple files
2. **Before quality workflows** - To ensure accurate scoping
3. **Weekly maintenance** - Keep index fresh in active projects
4. **After merging** - When merging branches with spec changes
5. **Before releases** - Verify all specs are properly indexed

### Automation

You can automate re-indexing using Git hooks:

**`.git/hooks/post-merge`:**
```bash
#!/bin/bash
echo "🔍 Re-indexing specs after merge..."
/smartspec_reindex_specs --quiet
```

**`.git/hooks/pre-commit`:**
```bash
#!/bin/bash
# Verify before commit
/smartspec_reindex_specs --verify --quiet
if [ $? -ne 0 ]; then
  echo "⚠️  SPEC_INDEX.json has issues. Run /smartspec_reindex_specs to fix."
  exit 1
fi
```

---

## 11. Best Practices

### 1. Run Verify First

Before making changes, check for issues:

```bash
/smartspec_reindex_specs --verify
```

### 2. Review the Report

Always review the generated report to understand what changed:

```bash
cat .smartspec/reindex-report-2024-01-15.md
```

### 3. Commit SPEC_INDEX.json

Track changes in version control:

```bash
git add SPEC_INDEX.json
git commit -m "chore: Re-index specs after implementing feature X"
```

### 4. Configure External Repos

For multi-repo projects, create `.smartspec/config.json`:

```json
{
  "external_repos": {
    "shared": "/path/to/shared-services",
    "common": "/path/to/common-lib"
  }
}
```

Then re-index will automatically scan external repos.

### 5. Regular Maintenance

Set up a weekly reminder to re-index:

```bash
# Add to crontab
0 9 * * 1 cd /path/to/project && /smartspec_reindex_specs --quiet
```

---

## 12. Troubleshooting

### Issue: Too many false positives from Git History

**Solution:** Adjust confidence threshold or exclude Strategy 5:

```bash
# In workflow configuration
exclude_strategies: ["git"]
min_confidence: 0.7
```

### Issue: Missing files from external repo

**Solution:** Ensure external repo path is correct:

```bash
/smartspec_reindex_specs --external-repo /correct/path/to/shared-repo
```

### Issue: Outdated entries not removed

**Solution:** Use `--force` to force re-index:

```bash
/smartspec_reindex_specs --force
```

### Issue: SPEC_INDEX.json corrupted

**Solution:** Restore from backup:

```bash
cp .smartspec/backups/SPEC_INDEX-2024-01-15.json SPEC_INDEX.json
/smartspec_reindex_specs --force
```

---

## 13. Related Workflows

After re-indexing, you can run quality workflows with confidence:

- **`/smartspec_fix_errors`** - Fix errors in scoped files
- **`/smartspec_generate_tests`** - Generate tests for scoped files
- **`/smartspec_refactor_code`** - Refactor scoped files

All quality workflows use SPEC_INDEX.json to determine which files to process.

---

## 14. Performance

### Execution Time

| Project Size | Specs | Files | Time |
|-------------|-------|-------|------|
| Small | 10 | 100 | 2-4s |
| Medium | 50 | 500 | 8-17s |
| Large | 100+ | 1000+ | 17-45s |

### Optimization Tips

1. **Re-index specific specs** instead of all specs when possible
2. **Use `--quiet`** to suppress progress output in scripts
3. **Run in parallel** for multiple specs (advanced)
4. **Cache results** for specs that haven't changed

---

## 15. Summary

The `smartspec_reindex_specs` workflow is essential for maintaining accurate file associations in large projects. By combining **5 intelligent detection strategies**, it achieves **95%+ coverage** while providing **safety features** like automatic backups and validation.

**Key Benefits:**
- ✅ Keeps SPEC_INDEX.json accurate
- ✅ Supports external repositories
- ✅ Uses 5 complementary strategies
- ✅ Generates detailed reports
- ✅ Validates and backs up automatically
- ✅ Enables accurate spec-scoped quality workflows

**Next Steps:**
1. Run `/smartspec_reindex_specs --verify` to check current state
2. Review the report and fix any issues
3. Set up regular re-indexing (weekly or after major changes)
4. Use quality workflows with confidence!
