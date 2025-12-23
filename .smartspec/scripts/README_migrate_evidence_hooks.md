# migrate_evidence_hooks.py - Usage Guide

## Overview

This script converts descriptive evidence in `tasks.md` files to standardized evidence hooks that can be verified by `smartspec_verify_tasks_progress_strict`.

**Key Features:**
- ✅ Project file scanning and indexing
- ✅ Symbol and package detection (bcrypt, JWT, Redis, BullMQ, Winston, Vault, etc.)
- ✅ **Automatic conversion of non-compliant evidence types** (file_exists, test_exists, command)
- ✅ Evidence hook validation
- ✅ Auto-correction of incorrect paths
- ✅ **No OpenAI package dependency** - Works in Kilo/Antigravity environment

---

## Quick Start

### Fix Non-Compliant Evidence Types (Recommended)

Most common use case: Your `tasks.md` already has `evidence:` hooks, but uses types that the verifier doesn't recognize.

```bash
python3 .smartspec/scripts/migrate_evidence_hooks.py \
  --tasks-file "specs/core/spec-001/tasks.md" \
  --project-root . \
  --auto-convert \
  --apply
```

**What it does:**
- ✅ Detects `file_exists`, `test_exists`, `command` evidence types
- ✅ Converts them to `code`, `test`, `docs` (verifier-compliant)
- ✅ Validates file paths exist in your project
- ✅ Shows preview before applying changes

---

## Usage Modes

### Mode 1: Auto-Convert (No LLM Required) ⭐ **Recommended**

Automatically fixes non-compliant evidence types without requiring AI/LLM.

```bash
python3 .smartspec/scripts/migrate_evidence_hooks.py \
  --tasks-file "specs/core/spec-001/tasks.md" \
  --project-root . \
  --auto-convert
```

**Conversion Rules:**

| Before (Non-Compliant) | After (Compliant) | Rule |
|------------------------|-------------------|------|
| `evidence: file_exists path=src/auth/` | `evidence: code path=src/auth/` | file_exists → code |
| `evidence: file_exists path=tests/unit/` | `evidence: test path=tests/unit/` | file_exists → test (if "test" in path) |
| `evidence: test_exists path=tests/auth.test.ts name=login` | `evidence: test path=tests/auth.test.ts contains="login"` | test_exists → test (name → contains) |
| `evidence: command cmd=npx tsc --noEmit` | `evidence: code path=tsconfig.json` | command → code (infer config file) |
| `evidence: command cmd=yamllint file.yaml` | `evidence: code path=file.yaml` | command → code (use file path) |
| `evidence: command cmd=markdownlint file.md` | `evidence: docs path=file.md` | command → docs (markdown files) |

**Example Output:**
```
🔍 Scanning project files...
✅ Indexed 452 files

📖 Reading tasks from: tasks.md
Found 73 non-compliant evidence hooks

🔧 Converting non-compliant evidence types...
  [1/73] Converting TSK-AUTH-001... ✓
  ...

STATISTICS:
  ✅ Valid hooks: 45
  🔧 Auto-corrected: 20
  ⚠️  Needs manual review: 8
```

---

### Mode 2: Interactive (For Descriptive Evidence)

For evidence that's still in natural language format (not yet `evidence:` hooks).

```bash
python3 .smartspec/scripts/migrate_evidence_hooks.py \
  --tasks-file "specs/core/spec-001/tasks.md" \
  --project-root . \
  --interactive
```

**Workflow:**
1. Script writes prompt to `/tmp/evidence_prompt_TSK-XXX.txt`
2. You call your LLM (via Kilo/Antigravity/etc.)
3. You write response to `/tmp/evidence_response_TSK-XXX.txt`
4. Press Enter to continue

---

## Command Line Options

```
--tasks-file <path>       Path to tasks.md file (required)
--project-root <path>     Project root for file validation (default: .)
--auto-convert            Automatically convert non-compliant types (no LLM)
--interactive             Interactive mode for LLM-based conversion
--apply                   Apply changes to file (default: preview only)
```

---

## Examples

### Example 1: Preview changes (safe)
```bash
python3 .smartspec/scripts/migrate_evidence_hooks.py \
  --tasks-file "specs/core/spec-core-001-authentication/tasks.md" \
  --project-root . \
  --auto-convert
```

### Example 2: Apply changes
```bash
python3 .smartspec/scripts/migrate_evidence_hooks.py \
  --tasks-file "specs/core/spec-core-001-authentication/tasks.md" \
  --project-root . \
  --auto-convert \
  --apply
```

### Example 3: Different project root
```bash
python3 .smartspec/scripts/migrate_evidence_hooks.py \
  --tasks-file "../my-project/specs/tasks.md" \
  --project-root "../my-project" \
  --auto-convert \
  --apply
```

---

## Output

### Statistics
```
================================================================================
STATISTICS for tasks.md
================================================================================
Non-compliant evidence converted: 73

Validation results:
  ✅ Valid hooks: 45
  🔧 Auto-corrected: 20
  ⚠️  Needs manual review: 8
================================================================================
```

### Preview
```
================================================================================
PREVIEW: Proposed changes for tasks.md
================================================================================

Task: TSK-AUTH-001 - Create core library structure
────────────────────────────────────────────────────────────────────────────────
- OLD: evidence: file_exists path=packages/auth-lib/src/auth/
+ NEW: evidence: code path=packages/auth-lib/src/auth/
  Reason: Converted file_exists to code
────────────────────────────────────────────────────────────────────────────────

Task: TSK-AUTH-010 - Configure Redis for session storage
────────────────────────────────────────────────────────────────────────────────
- OLD: evidence: test_exists path=tests/integration/redis.test.ts name=redis_connection
+ NEW: evidence: test path=tests/integration/redis.test.ts contains="redis_connection"
  Reason: Converted test_exists to test (name → contains)
────────────────────────────────────────────────────────────────────────────────

Task: TSK-AUTH-021 - Generate TypeScript types from OpenAPI
────────────────────────────────────────────────────────────────────────────────
- OLD: evidence: command cmd=npx tsc --noEmit expected_exit=0
+ NEW: evidence: code path=tsconfig.json
  Reason: Converted command to code (tsc → tsconfig.json)
────────────────────────────────────────────────────────────────────────────────
```

---

## Validation & Auto-Correction

The script performs automatic validation and correction:

### 1. File Existence Check
```
Generated: evidence: code path=src/auth.ts
Validated: ❌ File not found: src/auth.ts
Found:     ✅ src/auth/index.ts exists
Corrected: evidence: code path=src/auth/index.ts
```

### 2. Package Detection
```
Task: "Implement bcrypt hashing"
Evidence: "Use bcrypt library"
Detected: bcrypt package imported in packages/auth-lib/src/crypto/password.util.ts
Generated: evidence: code path=packages/auth-lib/src/crypto/password.util.ts contains="bcrypt"
```

### 3. Symbol Lookup
```
Generated: evidence: code symbol=VaultClient
Validated: ❌ No path provided
Found:     ✅ VaultClient in packages/auth-lib/src/config/vault.client.ts
Corrected: evidence: code path=packages/auth-lib/src/config/vault.client.ts symbol=VaultClient
```

---

## Non-Compliant Evidence Types

### Why are they non-compliant?

The `smartspec_verify_tasks_progress_strict` workflow only recognizes these evidence types:
- ✅ `code` - Source code files
- ✅ `test` - Test files
- ✅ `ui` - UI components/screens
- ✅ `docs` - Documentation files

These types are **NOT recognized** by the verifier:
- ❌ `file_exists` - Verifier doesn't check file existence
- ❌ `test_exists` - Verifier doesn't check test existence
- ❌ `command` - Verifier doesn't execute commands

**Result:** Tasks with these types will be marked as `not_verified` ❌

---

## Conversion Details

### `file_exists` → `code` or `test`

**Before:**
```markdown
- evidence: file_exists path=packages/auth-lib/src/auth/
```

**After:**
```markdown
- evidence: code path=packages/auth-lib/src/auth/
```

**Logic:**
- If path contains "test" → convert to `test`
- Otherwise → convert to `code`

---

### `test_exists` → `test`

**Before:**
```markdown
- evidence: test_exists path=tests/integration/redis.test.ts name=redis_connection
```

**After:**
```markdown
- evidence: test path=tests/integration/redis.test.ts contains="redis_connection"
```

**Logic:**
- Keep `path` parameter
- Convert `name` → `contains`
- Remove other parameters

---

### `command` → `code` or `docs`

**Before:**
```markdown
- evidence: command cmd=npx tsc --noEmit expected_exit=0
```

**After:**
```markdown
- evidence: code path=tsconfig.json
```

**Logic:**
- `tsc` → `tsconfig.json`
- `eslint` / `lint` → `.eslintrc.js`
- `prettier` → `.prettierrc`
- `yamllint` + path → `code path=<file>`
- `markdownlint` + path → `docs path=<file>`
- Other commands → `code path=COMMAND_NOT_SUPPORTED contains="<cmd>"`

---

## Integration with Kilo/Antigravity

### Option A: Use Auto-Convert (Recommended)

No need for LLM! Just run with `--auto-convert`:

```bash
# In Kilo/Antigravity environment
python3 .smartspec/scripts/migrate_evidence_hooks.py \
  --tasks-file tasks.md \
  --project-root . \
  --auto-convert \
  --apply
```

### Option B: Manual LLM Calls (For Descriptive Evidence)

1. Run script in interactive mode
2. For each prompt:
   ```bash
   # Read prompt
   cat /tmp/evidence_prompt_TSK-XXX.txt
   
   # Call your LLM (via Kilo, Antigravity, or any other tool)
   kilo ask "$(cat /tmp/evidence_prompt_TSK-XXX.txt)" > /tmp/evidence_response_TSK-XXX.txt
   
   # Press Enter in script
   ```

---

## Troubleshooting

### Issue: "Found 0 non-compliant evidence hooks"
**Cause:** Evidence is still in descriptive format (not `evidence:` prefix)  
**Solution:** Use `--interactive` mode instead of `--auto-convert`

### Issue: "File not found" warnings
**Cause:** File doesn't exist in project yet  
**Solution:** This is expected for planned tasks. Review and adjust manually if needed.

### Issue: "Needs manual review"
**Cause:** Script couldn't validate the file path  
**Solution:** Common cases:
- File doesn't exist in project (yet to be created)
- Path is ambiguous or incorrect
- Need to create the file first

### Issue: "COMMAND_NOT_SUPPORTED"
**Cause:** Command type couldn't be inferred  
**Solution:** Manually edit the evidence hook to point to the relevant file

---

## Best Practices

1. **Always preview first** (without `--apply`)
2. **Use correct project-root** for accurate file validation
3. **Review auto-corrected hooks** before applying
4. **Backup is automatic** - `.md.backup` file created before changes
5. **Commit frequently** - Commit after each successful migration
6. **Use --auto-convert first** - Fixes most issues without LLM

---

## Workflow Recommendation

```bash
# Step 1: Preview changes
python3 .smartspec/scripts/migrate_evidence_hooks.py \
  --tasks-file tasks.md \
  --project-root . \
  --auto-convert

# Step 2: Review output
# Check STATISTICS and PREVIEW sections

# Step 3: Apply changes
python3 .smartspec/scripts/migrate_evidence_hooks.py \
  --tasks-file tasks.md \
  --project-root . \
  --auto-convert \
  --apply

# Step 4: Verify
/smartspec_verify_tasks_progress_strict tasks.md

# Step 5: Commit
git add tasks.md
git commit -m "fix: convert evidence hooks to verifier-compliant format"
git push
```

---

## See Also

- Workflow definition: `.smartspec/workflows/smartspec_migrate_evidence_hooks.md`
- English manual: `.smartspec-docs/workflows/migrate_evidence_hooks.md`
- Thai manual: `.smartspec-docs/workflows/migrate_evidence_hooks_th.md`
- Verifier workflow: `.smartspec/workflows/smartspec_verify_tasks_progress_strict.md`
