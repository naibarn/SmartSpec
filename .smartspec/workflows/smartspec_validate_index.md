# SmartSpec Validate SPEC_INDEX Workflow
## Cross-Check SPEC_INDEX.json Integrity (v5.2 Centralization + Multi-Repo + UI Addendum)

---
description: |
  Validate SPEC_INDEX.json integrity and system health.

  v5.2 enhancements:
  - Canonical index location: .spec/SPEC_INDEX.json
  - Reads legacy root mirror when present
  - Uses .spec/registry as shared truth when available
  - Multi-repo-aware file existence checks
  - UI JSON addendum support
  - Safer validation for portfolio/planned specs

flags:
  - name: --fix
    description: Automatically fix issues that can be auto-fixed (metadata, dependents, timestamps)
    type: boolean
    default: false

  - name: --report
    description: Report detail level
    type: enum
    values: [summary, detailed]
    default: summary

  - name: --index
    description: Path to SPEC_INDEX.json file (optional). If omitted, SmartSpec will auto-detect.
    type: string
    optional: true

  - name: --output
    description: Output report file path (optional, defaults to .spec/reports/)
    type: string
    optional: true

  - name: --registry-dir
    description: Registry directory (optional)
    type: string
    default: .spec/registry

  - name: --workspace-roots
    description: |
      Comma-separated list of additional repo roots to search for spec files.
      Use this when SPEC_INDEX references specs located in sibling repos.
      Examples:
        --workspace-roots="../Smart-AI-Hub,../smart-ai-hub-enterprise-security"
    type: string
    optional: true

  - name: --repos-config
    description: |
      Path to a JSON config describing known repos and aliases.
      If provided, this takes precedence over --workspace-roots for resolution.
      Default suggested location: .spec/smartspec.repos.json
    type: string
    optional: true

  - name: --mode
    description: |
      Validation interpretation mode.
      - runtime: strict about missing files for active/stable/core specs
      - portfolio: allows planned/backlog specs to be missing without error
    type: enum
    values: [runtime, portfolio]
    default: portfolio

examples:
  - command: /smartspec_validate_index
    description: Validate with summary report (auto-detect canonical index)

  - command: /smartspec_validate_index --report=detailed
    description: Generate detailed report

  - command: /smartspec_validate_index --fix --report=detailed
    description: Validate and apply safe auto-fixes

  - command: /smartspec_validate_index --workspace-roots="../Smart-AI-Hub,../SmartSpec"
    description: Validate across multiple sibling repositories

  - command: /smartspec_validate_index --repos-config=.spec/smartspec.repos.json --mode=runtime
    description: Use structured multi-repo config and enforce stricter runtime rules

version: 5.2.0
author: SmartSpec Team
---

## Overview

This workflow validates SPEC_INDEX.json integrity and generates a comprehensive health report.

**Purpose:**
- Detect broken references, circular dependencies, duplicates
- Identify orphaned and stale specs
- Verify metadata consistency
- Verify dependents calculations
- Validate file existence across **multiple repos**
- Apply UI JSON addendum checks where applicable
- Provide actionable recommendations
- Auto-fix common safe issues

**Centralization Rules (v5.2):**
- **Canonical index:** `.spec/SPEC_INDEX.json`
- **Legacy mirror:** `SPEC_INDEX.json` at repo root (read-only unless explicitly migrated by other tools)
- **Shared registry:** `.spec/registry/` when present
- Tooling directory `.smartspec/` must not be treated as canonical spec storage.

---

## 0. Prerequisites

### 0.1 Resolve SPEC_INDEX Path

Search order:

1) `.spec/SPEC_INDEX.json` (canonical)
2) `SPEC_INDEX.json` (legacy root mirror)
3) `.smartspec/SPEC_INDEX.json` (deprecated)
4) `specs/SPEC_INDEX.json` (older layout)

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
  elif [ -f "specs/SPEC_INDEX.json" ]; then
    INDEX_PATH="specs/SPEC_INDEX.json"
  fi
fi

if [ ! -f "$INDEX_PATH" ]; then
  echo "❌ ERROR: SPEC_INDEX.json not found"
  echo "Checked (in order):"
  echo "  1) .spec/SPEC_INDEX.json (canonical)"
  echo "  2) SPEC_INDEX.json (legacy root mirror)"
  echo "  3) .smartspec/SPEC_INDEX.json (deprecated)"
  echo "  4) specs/SPEC_INDEX.json (older layout)"
  echo "Specify a custom path with:"
  echo "  /smartspec_validate_index --index=path/to/SPEC_INDEX.json"
  exit 1
fi

echo "✅ Found SPEC_INDEX at: $INDEX_PATH"
```

### 0.2 Resolve Registry Directory

```bash
REGISTRY_DIR="${FLAGS_registry_dir:-.spec/registry}"
REGISTRY_AVAILABLE=false

if [ -d "$REGISTRY_DIR" ]; then
  REGISTRY_AVAILABLE=true
  echo "✅ Registry detected at: $REGISTRY_DIR"
else
  echo "ℹ️ Registry not found at $REGISTRY_DIR (validation will continue without registry-backed checks)"
fi
```

### 0.3 Resolve Multi-Repo Search Roots

This workflow must support cases where specs are distributed across sibling repos.

Two ways to configure:

1) **Simple list** via `--workspace-roots`.
2) **Structured config** via `--repos-config`.

Recommended config file (optional): `.spec/smartspec.repos.json`

Example structure:

```json
{
  "version": "1.0",
  "repos": [
    { "id": "public", "root": "../Smart-AI-Hub" },
    { "id": "private", "root": "../smart-ai-hub-enterprise-security" },
    { "id": "tools", "root": "../SmartSpec" }
  ]
}
```

If neither is provided:
- The workflow will validate only within the current repo root.

---

## 1. Load SPEC_INDEX

```javascript
const fs = require('fs');
const path = require('path');

const indexPath = FLAGS.index || process.env.INDEX_PATH || '.spec/SPEC_INDEX.json';
const indexContent = fs.readFileSync(indexPath, 'utf-8');
let specIndex;

try {
  specIndex = JSON.parse(indexContent);
} catch (error) {
  console.error('❌ ERROR: Invalid JSON in SPEC_INDEX.json');
  console.error(error.message);
  process.exit(1);
}

console.log('✅ Loaded SPEC_INDEX.json');
console.log(`   Total specs: ${specIndex.specs?.length || 0}`);
```

---

## 2. Build Resolution Context

### 2.1 Determine Repo Roots

```javascript
function splitCsv(v) {
  return (v || '')
    .split(',')
    .map(s => s.trim())
    .filter(Boolean);
}

const cwdRoot = process.cwd();
let repoRoots = [cwdRoot];

// Structured config takes precedence
if (FLAGS.repos_config && fs.existsSync(FLAGS.repos_config)) {
  try {
    const cfg = JSON.parse(fs.readFileSync(FLAGS.repos_config, 'utf-8'));
    if (Array.isArray(cfg.repos)) {
      repoRoots = [cwdRoot, ...cfg.repos.map(r => r.root).filter(Boolean)];
    }
  } catch (e) {
    console.warn('⚠️ Failed to parse repos config, falling back to --workspace-roots.');
  }
}

// Append simple roots
const extraRoots = splitCsv(FLAGS.workspace_roots);
repoRoots = [...new Set([...repoRoots, ...extraRoots])]
  .map(r => path.resolve(cwdRoot, r));

console.log('ℹ️ Repo roots for file resolution:');
repoRoots.forEach(r => console.log(`   - ${r}`));
```

### 2.2 Resolve Expected Spec Artifact Paths

**Compatibility-first rule:**
- Existing SPEC_INDEX structure likely uses `spec.path` pointing to a folder.
- We must not require new fields.

So resolution tries:

1) `spec.path/spec.md` relative to each repo root.
2) If spec declares `spec_md_path`, treat it as an override.
3) For UI specs, also attempt `ui.json` checks.

---

## 3. Initialize Validation Results

```javascript
const mode = FLAGS.mode || 'portfolio';

const validationResults = {
  timestamp: new Date().toISOString(),
  indexPath,
  totalSpecs: specIndex.specs?.length || 0,
  mode,
  repoRoots,
  checks: {
    fileExistence: { passed: true, errors: [], warnings: [] },
    brokenReferences: { passed: true, errors: [], warnings: [] },
    circularDependencies: { passed: true, errors: [], warnings: [] },
    duplicates: { passed: true, errors: [], warnings: [] },
    orphanedSpecs: { passed: true, errors: [], warnings: [] },
    staleSpecs: { passed: true, errors: [], warnings: [] },
    metadataConsistency: { passed: true, errors: [], warnings: [] },
    dependentsCalculation: { passed: true, errors: [], warnings: [] },
    uiJsonCompliance: { passed: true, errors: [], warnings: [] }
  },
  summary: {
    totalChecks: 9,
    passedChecks: 0,
    errors: 0,
    warnings: 0,
    healthScore: 100
  },
  autoFixes: [],
  recommendations: []
};

console.log('✅ Initialized validation results');
```

---

## 4. Validation Check 1: File Existence (Multi-Repo Aware)

**Purpose:** Verify that all spec artifacts referenced in INDEX exist.

**Status-aware enforcement (to avoid forcing empty specs):**

- In `portfolio` mode:
  - Missing files for `planned | backlog | idea | draft` → **warning**
  - Missing files for `active | in-progress | stable | core` → **error**

- In `runtime` mode:
  - Missing files for anything except `deprecated` → **error**

If the spec object does not contain `status`, assume `active`.

```javascript
console.log('\n🔍 Check 1: File Existence (multi-repo)');
console.log('─'.repeat(50));

const fileExistenceErrors = [];
const fileExistenceWarnings = [];

function statusBucket(status) {
  const s = (status || 'active').toLowerCase();
  const planned = new Set(['planned','backlog','idea','draft']);
  const active = new Set(['active','in-progress','stable','core']);
  const deprecated = new Set(['deprecated','archived']);
  if (deprecated.has(s)) return 'deprecated';
  if (planned.has(s)) return 'planned';
  if (active.has(s)) return 'active';
  return 'active';
}

function resolveSpecFile(spec) {
  const override = spec.spec_md_path;
  if (override) {
    for (const root of repoRoots) {
      const p = path.resolve(root, override);
      if (fs.existsSync(p)) return p;
    }
  }

  const folder = spec.path || spec.folder || '';
  for (const root of repoRoots) {
    const p = path.resolve(root, folder, 'spec.md');
    if (fs.existsSync(p)) return p;
  }

  return null;
}

for (const spec of (specIndex.specs || [])) {
  const resolved = resolveSpecFile(spec);
  if (!resolved) {
    const bucket = statusBucket(spec.status);
    const expected = (spec.spec_md_path || path.join(spec.path || '', 'spec.md'));

    const issue = {
      type: 'file_not_found',
      specId: spec.id,
      specTitle: spec.title,
      expectedPath: expected,
      message: `Spec file not found in any configured repo root: ${expected}`,
      suggestion: 'Create spec file, adjust path, or update status if truly planned/backlog',
      severity: 'error'
    };

    if (mode === 'portfolio' && bucket === 'planned') {
      issue.severity = 'warning';
      fileExistenceWarnings.push(issue);
    } else if (bucket === 'deprecated') {
      issue.severity = 'warning';
      fileExistenceWarnings.push(issue);
    } else {
      fileExistenceErrors.push(issue);
    }
  }
}

validationResults.checks.fileExistence.errors = fileExistenceErrors;
validationResults.checks.fileExistence.warnings = fileExistenceWarnings;
validationResults.checks.fileExistence.passed = fileExistenceErrors.length === 0;

if (fileExistenceErrors.length === 0 && fileExistenceWarnings.length === 0) {
  console.log('✅ All required spec files exist');
} else {
  if (fileExistenceErrors.length) console.log(`❌ Missing required files: ${fileExistenceErrors.length}`);
  if (fileExistenceWarnings.length) console.log(`⚠️ Missing allowed-by-mode files: ${fileExistenceWarnings.length}`);
}
```

---

## 5. Validation Check 2: Broken References

Unchanged logic, but recommendations should consider status:
- If missing dependency is planned, warn rather than error in portfolio mode.

---

## 6. Validation Check 3: Circular Dependencies

Unchanged detection.

Recommended policy notes in report:
- `core` must not depend on `ui/feature` cyclically.

---

## 7. Validation Check 4: Duplicate Specs

Unchanged detection.

---

## 8. Validation Check 5: Orphaned Specs (Status-Aware)

In portfolio mode:
- Orphaned planned specs → info/warn
- Orphaned active/core → warning or error based on team policy

---

## 9. Validation Check 6: Stale Specs

Unchanged detection.

---

## 10. Validation Check 7: Metadata Consistency

This check is safe to auto-fix.

---

## 11. Validation Check 8: Dependents Calculation

This check is safe to auto-fix.

---

## 12. Validation Check 9: UI JSON Compliance (Conditional)

Apply when any of these are true:
- `spec.type === 'ui'` or `spec.spec_type === 'ui'`
- `spec.ui === true`
- folder contains `ui.json` in any repo root

Rules:
- `ui.json` is the design source of truth.
- `spec.md` may be missing for planned UI specs in portfolio mode.
- UI naming should align with `ui-component-registry.json` if present.

---

## 13. Report Generation

Default output directory:
- `.spec/reports/`

Filename pattern:
- `validation-report-<timestamp>.md`

---

## 14. Auto-Fix Guidelines

**What Can Be Auto-Fixed:**
- ✅ Metadata counts
- ✅ Dependents calculation
- ✅ Timestamps

**What Cannot Be Auto-Fixed:**
- ❌ Broken references
- ❌ Circular dependencies
- ❌ Duplicate specs
- ❌ Missing files

---

## 15. Best Practices

- For multi-repo projects, always supply one of:
  - `--workspace-roots`, or
  - `--repos-config`

- Use `--mode=portfolio` while building roadmap-level indexes.
- Use `--mode=runtime` before release gates.

---

## 16. Recommended Companion Workflows

- `/smartspec_reindex_specs` after major move/rename
- `/smartspec_sync_spec_tasks` after tasks/spec drift
- `/smartspec_fix_errors` for mechanical cleanup

