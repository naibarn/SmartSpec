# SmartSpec Scripts Index

**Version:** 1.0.0  
**Date:** 2025-12-26  
**Purpose:** Complete reference for all SmartSpec utility scripts

---

## 📋 All Scripts

### 1. Verification Scripts

#### verify_evidence_enhanced.py ✅ **RECOMMENDED**

**Purpose:** Enhanced evidence verification with problem categorization and actionable suggestions

**Status:** ✅ Production Ready (v1.0.0)

**Features:**
- 6 problem categories (Not Implemented, Missing Tests, Missing Code, Naming Issues, Symbol Issues, Content Issues)
- Fuzzy file matching (finds similar files)
- Root cause analysis
- Actionable suggestions
- Priority ordering (1-4)
- Enhanced JSON output
- Separate code/test tracking

**Usage:**
```bash
python3 .smartspec/scripts/verify_evidence_enhanced.py \
  tasks.md \
  --repo-root . \
  --json \
  --out reports/
```

**Parameters:**
- `tasks_file` - Path to tasks.md
- `--repo-root` - Repository root directory (default: .)
- `--json` - Output JSON summary
- `--out` - Output directory for reports (default: reports/)

**Output:**
- `report.md` - Human-readable report with categories
- `summary.json` - Machine-readable summary for automation
- Problem categorization
- Similar files suggestions
- Priority-based action items

**Documentation:**
- Full guide: `README_verify_evidence_enhanced.md` (TODO)
- Action guide: `VERIFY_REPORT_ACTION_GUIDE.md`
- Troubleshooting: `TROUBLESHOOTING_DECISION_TREE.md`

---

#### verify_evidence_strict.py ⚠️ **DEPRECATED**

**Purpose:** Basic evidence verification (old version)

**Status:** ⚠️ Deprecated - Use `verify_evidence_enhanced.py` instead

**Migration:** See `VERIFY_EVIDENCE_MIGRATION_GUIDE.md` (TODO)

---

### 2. Prompt Generation Scripts

#### generate_prompts_from_verify_report.py ✅ **RECOMMENDED**

**Purpose:** Generate category-specific implementation prompts from verify reports

**Status:** ✅ Production Ready (v1.0.0)

**Features:**
- Reads verify report JSON
- Categorizes tasks automatically
- Generates category-specific prompts
- Template-based generation
- Priority ordering
- Category filtering
- Priority filtering
- JSON output support

**Usage:**
```bash
# Basic usage
python3 .smartspec/scripts/generate_prompts_from_verify_report.py \
  --verify-report reports/latest/summary.json \
  --tasks tasks.md

# Filter by category
python3 .smartspec/scripts/generate_prompts_from_verify_report.py \
  --verify-report reports/latest/summary.json \
  --tasks tasks.md \
  --category missing_tests

# Filter by priority
python3 .smartspec/scripts/generate_prompts_from_verify_report.py \
  --verify-report reports/latest/summary.json \
  --tasks tasks.md \
  --priority 1
```

**Parameters:**
- `--verify-report` - Path to verify report JSON
- `--tasks` - Path to tasks.md
- `--category` - Filter by category (optional)
- `--priority` - Filter by priority 1-4 (optional)
- `--output-dir` - Output directory (default: .spec/prompts/)
- `--template-dir` - Custom templates directory (optional)
- `--json` - Output JSON metadata

**Categories:**
- `not_implemented` - No files exist
- `missing_tests` - Code exists, tests missing
- `missing_code` - Tests exist, code missing
- `naming_issue` - File names don't match
- `symbol_issue` - Required symbols missing
- `content_issue` - Required content missing

**Output:**
- `README.md` - Overview and priority order
- `not_implemented.md` - Implementation prompts
- `missing_tests.md` - Test generation prompts
- `missing_code.md` - Code implementation prompts
- `naming_issues.md` - Naming fix instructions
- `symbol_issues.md` - Symbol addition prompts
- `content_issues.md` - Content addition prompts
- `meta/summary.json` - Metadata (if --json)

**Documentation:**
- Full guide: `PROMPTER_USAGE_GUIDE.md`
- Templates: `.smartspec/templates/verify_report_prompts/`
- Problem matrix: `PROBLEM_SOLUTION_MATRIX.md`

---

### 3. Migration Scripts

#### migrate_evidence_hooks.py

**Purpose:** Migrate old evidence format to new format

**Status:** ✅ Stable

**Usage:**
```bash
python3 .smartspec/scripts/migrate_evidence_hooks.py \
  tasks.md \
  --backup
```

**Documentation:** `README_migrate_evidence_hooks.md`

---

### 4. Installation Scripts

#### install.sh

**Purpose:** Install SmartSpec on Unix/macOS/Linux

**Status:** ✅ Stable

**Usage:**
```bash
curl -fsSL https://raw.githubusercontent.com/naibarn/SmartSpec/main/.smartspec/scripts/install.sh | bash
```

---

#### install.ps1

**Purpose:** Install SmartSpec on Windows

**Status:** ✅ Stable

**Usage:**
```powershell
irm https://raw.githubusercontent.com/naibarn/SmartSpec/main/.smartspec/scripts/install.ps1 | iex
```

---

## 🔄 Workflow Integration

### Complete Verification Workflow

```bash
# Step 1: Verify
python3 .smartspec/scripts/verify_evidence_enhanced.py \
  tasks.md --repo-root . --json --out reports/

# Step 2: Generate prompts
python3 .smartspec/scripts/generate_prompts_from_verify_report.py \
  --verify-report reports/latest/summary.json \
  --tasks tasks.md

# Step 3: Review
cat .spec/prompts/latest/README.md

# Step 4: Implement
# (Follow prompts in category files)

# Step 5: Verify again
python3 .smartspec/scripts/verify_evidence_enhanced.py \
  tasks.md --repo-root .
```

---

## 📊 Script Comparison

| Script | Purpose | Status | Output | Use When |
|:---|:---|:---:|:---|:---|
| `verify_evidence_enhanced.py` | Verify tasks | ✅ Active | Report + JSON | Always (primary verification) |
| `verify_evidence_strict.py` | Verify tasks | ⚠️ Deprecated | Basic report | Never (use enhanced) |
| `generate_prompts_from_verify_report.py` | Generate prompts | ✅ Active | Category prompts | After verification |
| `migrate_evidence_hooks.py` | Migrate format | ✅ Stable | Updated tasks.md | One-time migration |
| `install.sh` | Install | ✅ Stable | Installed system | First time / update |
| `install.ps1` | Install (Windows) | ✅ Stable | Installed system | First time / update |

---

## 🎯 Quick Reference

### When to Use Each Script

**Starting a new project:**
```bash
# 1. Install SmartSpec
curl -fsSL https://raw.githubusercontent.com/naibarn/SmartSpec/main/.smartspec/scripts/install.sh | bash

# 2. Create tasks.md
# (Use SmartSpec workflows)

# 3. Verify
python3 .smartspec/scripts/verify_evidence_enhanced.py tasks.md --json

# 4. Generate prompts
python3 .smartspec/scripts/generate_prompts_from_verify_report.py \
  --verify-report reports/latest/summary.json --tasks tasks.md
```

**Checking progress:**
```bash
python3 .smartspec/scripts/verify_evidence_enhanced.py tasks.md
```

**Fixing issues:**
```bash
# Generate prompts for specific category
python3 .smartspec/scripts/generate_prompts_from_verify_report.py \
  --verify-report reports/latest/summary.json \
  --tasks tasks.md \
  --category not_implemented
```

**Migrating old format:**
```bash
python3 .smartspec/scripts/migrate_evidence_hooks.py tasks.md --backup
```

---

## 🔗 Related Documentation

### Guides
- `VERIFY_REPORT_ACTION_GUIDE.md` - What to do after verification
- `PROMPTER_USAGE_GUIDE.md` - How to use prompter
- `PROBLEM_SOLUTION_MATRIX.md` - Quick problem → solution reference
- `TROUBLESHOOTING_DECISION_TREE.md` - Interactive troubleshooting

### Workflow Documentation
- `workflows/smartspec_verify_tasks_progress_strict.md` - Verification workflow
- `workflows/smartspec_report_implement_prompter.md` - Prompter workflow

### Templates
- `.smartspec/templates/verify_report_prompts/` - Prompt templates

---

## 📝 Script Development

### Adding a New Script

1. Create script in `.smartspec/scripts/`
2. Add shebang: `#!/usr/bin/env python3`
3. Make executable: `chmod +x script.py`
4. Add to this index
5. Create README if complex
6. Add tests (optional but recommended)

### Script Standards

- Python 3.11+
- Use argparse for CLI
- Include --help
- Return exit codes (0 = success, 1 = error)
- Log to stderr, output to stdout
- Support --json for automation
- Include version in --version

---

## 🐛 Troubleshooting

### Script not found
```bash
ls -la .smartspec/scripts/
git pull origin main
```

### Permission denied
```bash
chmod +x .smartspec/scripts/*.py
```

### Python version
```bash
python3 --version
# If not found, use python3
```

### Module not found
```bash
pip3 install -r requirements.txt
```

---

## 📚 Additional Resources

- **Main README:** `../README.md`
- **Workflows:** `../workflows/`
- **Documentation:** `../.smartspec-docs/`
- **Templates:** `../templates/`

---

**Version:** 1.0.0  
**Date:** 2025-12-26  
**Status:** ✅ Production Ready
