---
description: Generate implementation prompt packs with 100% duplication prevention.
version: 7.1.0
workflow: /smartspec_report_implement_prompter
---

# smartspec_report_implement_prompter

> **Canonical path:** `.smartspec/workflows/smartspec_report_implement_prompter.md`  
> **Version:** 7.1.0  
> **Status:** Production Ready  
> **Category:** prompter

## Purpose

Generate **implementation prompt packs** from a spec and tasks, with **100% duplication prevention** and **reuse-first** governance.

This workflow replaces legacy prompt generators and ensures that all generated prompts are aware of existing components, preventing the creation of duplicates.

**NEW in v7.1.0:** Supports **verify reports** from `verify_evidence_enhanced.py` to automatically generate category-specific prompts for fixing verification issues.

It produces **prompts only** (safe outputs) and never modifies governed artifacts or runtime source trees.

---

## Governance contract

This workflow MUST follow:

- `knowledge_base_smartspec_handbook.md` (v6)
- `.spec/smartspec.config.yaml`

### Write scopes (enforced)

Allowed writes (safe outputs only):

- Prompts: `.spec/prompts/**`

Forbidden writes (must hard-fail):

- Any path outside allowlist from config
- Any governed artifact (e.g., `specs/**`, `.spec/SPEC_INDEX.json`, `.spec/WORKFLOWS_INDEX.yaml`)
- Reports output (this workflow does not write to `.spec/reports/**`)
- Any runtime source tree modifications

### `--apply` behavior (universal flag)

- Accepted for compatibility with the universal flag contract.
- Must have **no effect** on write scopes.
- If provided, the workflow MUST note in the prompt pack header and JSON summary that `--apply` was ignored.

---

## Flags

### Universal flags (must support)

All SmartSpec workflows support these universal flags:

| Flag | Required | Description |
|---|---|---|
| `--config` | No | Path to custom config file (default: `.spec/smartspec.config.yaml`) |
| `--lang` | No | Output language (`th` for Thai, `en` for English, `auto` for automatic detection) |
| `--platform` | No | Platform mode (`cli` for CLI, `kilo` for Kilo Code, `ci` for CI/CD, `other` for custom integrations) |
| `--out` | No | Base output directory for reports and generated files (must pass safety checks) |
| `--json` | No | Output results in JSON format for machine parsing and automation |
| `--quiet` | No | Suppress non-essential output, showing only errors and critical information |

### Workflow-specific flags

Flags specific to `/smartspec_report_implement_prompter`:

| Flag | Required | Description |
|---|---|---|
| `--spec` | No* | Path to the spec.md file (e.g., `specs/feature/spec-001/spec.md`) |
| `--tasks` | Yes | Path to the tasks.md file (e.g., `specs/feature/spec-001/tasks.md`) |
| `--verify-report` | No | Path to verify report JSON from verify_evidence_enhanced.py |
| `--apply` | No | Accepted for compatibility but has no effect (prompts are safe outputs) |
| `--skip-duplication-check` | No | Skip pre-generation duplication validation (not recommended) |
| `--registry-roots` | No | Additional registry directories to check for duplicates (comma-separated) |
| `--prompt-style` | No | Style of generated prompts (detailed|concise|structured, default: detailed) |
| `--category` | No | Generate prompts for specific category only (not_implemented|missing_tests|naming_issue|symbol_issue|content_issue|missing_code) |
| `--priority` | No | Generate prompts for specific priority only (1|2|3|4) |

**Note:** `--spec` is required unless `--verify-report` is provided. When using `--verify-report`, spec information is optional.

### Flag usage notes

- **Config-first approach:** Prefer setting defaults in `.spec/smartspec.config.yaml` to minimize command-line flags
- **Boolean flags:** Flags without values are boolean (presence = true, absence = false)
- **Path safety:** All path arguments must pass safety validation (no directory traversal, symlink escape, or absolute paths outside project)
- **Secret handling:** Never pass secrets as flag values; use `env:VAR_NAME` references or config file
- **Duplication prevention:** Never use `--skip-duplication-check` unless explicitly instructed
- **Safe outputs:** This workflow only writes to `.spec/prompts/**`, no `--apply` gate needed

---

## Behavior

### 1) Pre-Generation Validation (MANDATORY)

Before generating prompts, the AI agent **MUST** check for existing similar components.

**Validation Command:**
```bash
python3 .smartspec/scripts/detect_duplicates.py \
  --registry-dir .spec/registry/ \
  --threshold 0.8
```

**Validation Rules:**
- **Exit Code `0` (Success):** No duplicates found. The agent may proceed.
- **Exit Code `1` (Failure):** Potential duplicates found. The agent **MUST**:
  - Present the duplicates to the user.
  - Ask the user to:
    a) Reuse existing components
    b) Justify creating new components
    c) Cancel and review existing specs
  - **MUST NOT** proceed until the user confirms.

### 2) Generate prompt pack

**Mode A: Spec-based (Traditional)**
- Generate implementation prompt packs from a spec and tasks.
- Requires: `--spec` and `--tasks`

**Mode B: Verify Report-based (NEW in v7.1.0)**
- Generate category-specific prompts from verify reports.
- Requires: `--verify-report` and `--tasks`
- Optional: `--category` or `--priority` to filter

**Verify Report Format:**

The workflow expects JSON output from `verify_evidence_enhanced.py`:

```json
{
  "totals": {
    "total_tasks": 10,
    "verified": 7,
    "not_verified": 3
  },
  "by_category": {
    "not_implemented": 2,
    "missing_tests": 1
  },
  "tasks": [
    {
      "task_id": "TASK-001",
      "title": "Implement feature",
      "category": "not_implemented",
      "priority": 2,
      "suggestions": [
        "→ Create file: path/to/file.py"
      ]
    }
  ]
}
```

**Category-Specific Prompts:**

When using `--verify-report`, the workflow generates separate prompts for each problem category:

1. **not_implemented.md** - Tasks with no implementation or tests
2. **missing_tests.md** - Tasks with code but no tests
3. **missing_code.md** - Tasks with tests but no code
4. **naming_issues.md** - Tasks with naming mismatches
5. **symbol_issues.md** - Tasks with missing symbols
6. **content_issues.md** - Tasks with missing content

**Priority Ordering:**

Prompts are ordered by priority:
- Priority 1: Critical (marked [x] but failed)
- Priority 2: Missing features
- Priority 3: Symbol/content issues
- Priority 4: Naming issues

### 3) Post-Generation Validation (MANDATORY)

After generating the prompt pack, the AI agent **MUST** validate the generated prompts.

**Validation Command:**
```bash
python3 .smartspec/scripts/validate_prompts.py \
  --prompts .spec/prompts/<spec-id>/<target>/<run-id>/ \
  --registry .spec/registry/ \
  --check-duplicates --threshold 0.8
```

**Validation Rules:**
- **Exit Code `0` (Success):** The prompt pack is valid.
- **Exit Code `1` (Failure):** The prompt pack is invalid. The agent **MUST NOT** use the generated prompts.
- The full output from the validation script **MUST** be included in the `README.md` of the prompt pack.

---

## Output structure

### Output root selection

To prevent accidental overwrites, outputs are always written under a run folder.

- If `--out` is provided, treat it as a **base output root** and write under:
  - `<out>/<target>/<run-id>/README.md`
  - `<out>/<target>/<run-id>/prompts/*.md`
  - `<out>/<target>/<run-id>/meta/summary.json` (if `--json`)

- If `--out` is not provided, default to:
  - `.spec/prompts/<spec-id>/<target>/<run-id>/...`

---

# End of workflow doc


---

## Usage Examples

### Example 1: Generate Prompts from Verify Report

```bash
# Step 1: Verify tasks
/smartspec_verify_tasks_progress_strict tasks.md \
  --out .spec/reports/verify/ \
  --json

# Output: .spec/reports/verify/20251226_082102/summary.json
# Report shows: 3 not verified (2 not_implemented, 1 missing_tests)

# Step 2: Generate prompts from report
/smartspec_report_implement_prompter \
  --verify-report .spec/reports/verify/20251226_082102/summary.json \
  --tasks tasks.md \
  --out .spec/prompts/

# Output: .spec/prompts/20251226_083000/
#   ├── README.md (summary + priority order)
#   ├── not_implemented.md (2 tasks, Priority 2)
#   ├── missing_tests.md (1 task, Priority 2)
#   └── meta/summary.json

# Step 3: Review prompts
cat .spec/prompts/20251226_083000/README.md

# Step 4: Implement fixes (follow prompts)
# Follow instructions in each category file

# Step 5: Verify again
/smartspec_verify_tasks_progress_strict tasks.md
# Expected: All verified ✅
```

---

### Example 2: Generate Prompts for Specific Category

```bash
# Generate prompts for missing tests only
/smartspec_report_implement_prompter \
  --verify-report report.json \
  --tasks tasks.md \
  --category missing_tests

# Output: Only missing_tests.md generated
```

---

### Example 3: Generate Prompts for Specific Priority

```bash
# Generate prompts for Priority 1 (Critical) only
/smartspec_report_implement_prompter \
  --verify-report report.json \
  --tasks tasks.md \
  --priority 1

# Output: Only Priority 1 tasks included
```

---

### Example 4: Traditional Mode (Spec-based)

```bash
# Generate prompts from spec (traditional mode)
/smartspec_report_implement_prompter \
  --spec specs/feature/spec-001/spec.md \
  --tasks specs/feature/spec-001/tasks.md

# Output: Implementation prompts based on spec
```

---

## Prompt Pack Structure

When using `--verify-report`, the output structure is:

```
.spec/prompts/<run-id>/
├── README.md                    # Summary and priority order
├── not_implemented.md           # Tasks with no implementation (if any)
├── missing_tests.md             # Tasks with no tests (if any)
├── missing_code.md              # Tasks with tests but no code (if any)
├── naming_issues.md             # Tasks with naming mismatches (if any)
├── symbol_issues.md             # Tasks with missing symbols (if any)
├── content_issues.md            # Tasks with missing content (if any)
└── meta/
    ├── summary.json             # Machine-readable summary
    └── report_source.json       # Original verify report
```

**README.md** contains:
- Executive summary
- Priority-ordered task list
- Category breakdown
- Quick start guide
- Verification commands

---

## Integration with Verify Workflow

### Complete Workflow Sequence

```bash
# 1. Verify current state
/smartspec_verify_tasks_progress_strict tasks.md --json --out reports/

# 2. Generate fix prompts
/smartspec_report_implement_prompter \
  --verify-report reports/latest/summary.json \
  --tasks tasks.md

# 3. Implement fixes (follow generated prompts)

# 4. Verify again
/smartspec_verify_tasks_progress_strict tasks.md

# 5. Repeat if needed
```

---

## Best Practices

### 1. Always Use JSON Output

```bash
# Generate JSON for automation
/smartspec_verify_tasks_progress_strict tasks.md --json
```

### 2. Review Prompts Before Implementation

```bash
# Read README first
cat .spec/prompts/latest/README.md

# Then review each category
```

### 3. Implement by Priority

Follow the priority order in README.md:
1. Priority 1: Critical (marked [x] but failed)
2. Priority 2: Missing features
3. Priority 3: Symbol/content issues
4. Priority 4: Naming issues

### 4. Verify After Each Category

```bash
# After implementing not_implemented.md
/smartspec_verify_tasks_progress_strict tasks.md

# After implementing missing_tests.md
/smartspec_verify_tasks_progress_strict tasks.md
```

### 5. Keep Prompts for Reference

```bash
# Don't delete prompt packs
# They serve as implementation documentation
```

---

## Troubleshooting

### Q: No prompts generated

**A:** Check verify report:
- Does it have `not_verified > 0`?
- Is the JSON format correct?
- Use `--json` flag in verify command

### Q: Wrong category assigned

**A:** Check verify report categories:
- Review `by_category` field
- Verify evidence in tasks.md
- Re-run verify with `--json`

### Q: Prompts too generic

**A:** Use `--prompt-style detailed`:
```bash
/smartspec_report_implement_prompter \
  --verify-report report.json \
  --tasks tasks.md \
  --prompt-style detailed
```

### Q: Want to regenerate specific category

**A:** Use `--category` flag:
```bash
/smartspec_report_implement_prompter \
  --verify-report report.json \
  --tasks tasks.md \
  --category missing_tests
```

---

## Template Customization

### Custom Template Directory

```bash
# Use custom templates
/smartspec_report_implement_prompter \
  --verify-report report.json \
  --tasks tasks.md \
  --template-dir .smartspec/custom_templates/
```

### Template Variables

Available in all templates:
- `{{task_id}}` - Task ID
- `{{title}}` - Task title
- `{{priority}}` - Priority level
- `{{category}}` - Problem category
- `{{code_path}}` - Code file path
- `{{test_path}}` - Test file path
- `{{code_symbol}}` - Required code symbol
- `{{test_symbol}}` - Required test symbol
- `{{suggestions}}` - Report suggestions
- `{{similar_files}}` - Similar files found

---

## Version History

### v7.1.0 (2025-12-26)
- ✅ Added `--verify-report` flag
- ✅ Added category-specific prompt generation
- ✅ Added priority-based ordering
- ✅ Added 6 prompt templates
- ✅ Added `--category` and `--priority` filters

### v7.0.0
- Initial release
- Spec-based prompt generation
- Duplication prevention

---

