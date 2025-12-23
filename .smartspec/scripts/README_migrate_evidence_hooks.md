# migrate_evidence_hooks.py - Usage Guide

## Overview

This script converts descriptive evidence in `tasks.md` files to standardized evidence hooks that can be verified by `smartspec_verify_tasks_progress_strict`.

**Key Features:**
- ✅ Project file scanning and indexing
- ✅ Symbol and package detection (bcrypt, JWT, Redis, BullMQ, Winston, Vault, etc.)
- ✅ Evidence hook validation
- ✅ Auto-correction of incorrect paths
- ✅ **No OpenAI package dependency** - Works in Kilo/Antigravity environment

---

## Usage Modes

### Mode 1: Interactive (Recommended for Kilo/Antigravity)

In this mode, the script writes prompts to files and waits for you to provide LLM responses.

```bash
python3 .smartspec/scripts/migrate_evidence_hooks.py \
  --tasks-file "specs/core/spec-001/tasks.md" \
  --project-root . \
  --interactive
```

**Workflow:**
1. Script scans project files
2. For each task with descriptive evidence:
   - Script writes prompt to `/tmp/evidence_prompt_TSK-XXX.txt`
   - You read the prompt
   - You call your LLM (via Kilo/Antigravity/etc.)
   - You write the response to `/tmp/evidence_response_TSK-XXX.txt`
   - Press Enter to continue
3. Script validates and auto-corrects the generated hooks
4. Script shows preview of all changes

**Example:**
```bash
# Run script
$ python3 .smartspec/scripts/migrate_evidence_hooks.py \
    --tasks-file tasks.md \
    --project-root . \
    --interactive

# Script output:
================================================================================
PROMPT for TSK-AUTH-024:
================================================================================
Prompt written to: /tmp/evidence_prompt_TSK-AUTH-024.txt

Please:
1. Read the prompt from: /tmp/evidence_prompt_TSK-AUTH-024.txt
2. Generate the evidence hook using your LLM
3. Write the response to: /tmp/evidence_response_TSK-AUTH-024.txt
4. Press Enter when done...
================================================================================

# You do:
$ cat /tmp/evidence_prompt_TSK-AUTH-024.txt
# (read the prompt)

# Call your LLM (e.g., via Kilo)
$ echo "evidence: code path=packages/auth-lib/src/crypto/password.util.ts contains=\"bcrypt\"" > /tmp/evidence_response_TSK-AUTH-024.txt

# Press Enter in the script terminal
# Script continues...
```

---

### Mode 2: Batch Processing (For environments with OpenAI API)

If you have OpenAI API key configured, you can use the batch mode (requires modifying the script to add back OpenAI client).

---

## Command Line Options

```
--tasks-file <path>       Path to tasks.md file (required)
--project-root <path>     Project root for file validation (default: .)
--interactive             Interactive mode for external LLM processing
--apply                   Apply changes to file (default: preview only)
```

---

## Examples

### Example 1: Preview changes (safe)
```bash
python3 .smartspec/scripts/migrate_evidence_hooks.py \
  --tasks-file "specs/core/spec-core-001-authentication/tasks.md" \
  --project-root . \
  --interactive
```

### Example 2: Apply changes
```bash
python3 .smartspec/scripts/migrate_evidence_hooks.py \
  --tasks-file "specs/core/spec-core-001-authentication/tasks.md" \
  --project-root . \
  --interactive \
  --apply
```

---

## Output

### Statistics
```
================================================================================
STATISTICS for tasks.md
================================================================================
Total tasks with descriptive evidence: 100

Validation results:
  ✅ Valid hooks: 45
  🔧 Auto-corrected: 40
  ⚠️  Needs manual review: 15
================================================================================
```

### Preview
```
================================================================================
PREVIEW: Proposed changes for tasks.md
================================================================================

Task: TSK-AUTH-024 - Implement bcrypt password hashing
────────────────────────────────────────────────────────────────────────────────
- OLD: The bcrypt library should be imported and used for password hashing
+ NEW: evidence: code path=packages/auth-lib/src/crypto/password.util.ts contains="bcrypt"
  Status: CORRECTED - Path validated and corrected
────────────────────────────────────────────────────────────────────────────────
```

---

## Validation & Auto-Correction

The script performs automatic validation and correction:

### 1. File Existence Check
```
Generated: evidence: code path=src/auth.ts contains="bcrypt"
Validated: ❌ File not found: src/auth.ts
Corrected: evidence: code path=packages/auth-lib/src/auth/password.ts contains="bcrypt"
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
Generated: evidence: code path=VaultClient symbol=getSecret
Validated: ❌ No path, only symbol
Found: VaultClient in packages/auth-lib/src/config/vault.client.ts
Corrected: evidence: code path=packages/auth-lib/src/config/vault.client.ts symbol=VaultClient
```

---

## Integration with Kilo/Antigravity

### Option A: Manual LLM Calls

1. Run script in interactive mode
2. For each prompt:
   ```bash
   # Read prompt
   cat /tmp/evidence_prompt_TSK-XXX.txt
   
   # Call your LLM (via Kilo, Antigravity, or any other tool)
   kilo ask "$(cat /tmp/evidence_prompt_TSK-XXX.txt)" > /tmp/evidence_response_TSK-XXX.txt
   
   # Press Enter in script
   ```

### Option B: Automated with Wrapper Script

Create a wrapper script that automates the LLM calls:

```bash
#!/bin/bash
# wrapper.sh

PROMPT_FILE=$1
RESPONSE_FILE=$2

# Call your LLM
kilo ask "$(cat $PROMPT_FILE)" > "$RESPONSE_FILE"
```

Then modify the script to call this wrapper automatically.

---

## Troubleshooting

### Issue: "openai package not installed"
**Solution:** Use `--interactive` mode instead. This version doesn't require OpenAI package.

### Issue: "File not found" warnings
**Solution:** This is expected. The script will auto-correct paths using project scanning.

### Issue: "Needs manual review"
**Solution:** Review the suggested hook and manually adjust if needed. Common cases:
- File doesn't exist in project (yet to be created)
- Ambiguous evidence description
- Multiple possible interpretations

---

## Best Practices

1. **Always preview first** (without `--apply`)
2. **Review auto-corrected hooks** before applying
3. **Use project-root parameter** for accurate file validation
4. **Backup is automatic** - `.md.backup` file created before changes
5. **Commit frequently** - Commit after each successful migration

---

## See Also

- Workflow definition: `.smartspec/workflows/smartspec_migrate_evidence_hooks.md`
- English manual: `.smartspec-docs/workflows/migrate_evidence_hooks.md`
- Thai manual: `.smartspec-docs/workflows/migrate_evidence_hooks_th.md`
- Verifier workflow: `.smartspec/workflows/smartspec_verify_tasks_progress_strict.md`
