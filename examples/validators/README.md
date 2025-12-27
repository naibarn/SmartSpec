# Validator Sample Files

This directory contains sample files for testing and learning validators.

## Directory Structure

```
validators/
├── good/           # Valid, complete examples
├── bad/            # Examples with errors (for testing)
├── empty/          # Minimal examples (for practice)
└── README.md       # This file
```

## Sample Files

### Good Examples (Complete & Valid)

These files pass all validation checks and serve as reference implementations.

| File | Validator | Description |
|------|-----------|-------------|
| `good/sample-spec-from-prompt.md` | validate_spec_from_prompt.py | Complete user authentication specification |
| `good/sample-generate-spec.md` | validate_generate_spec.py | Complete technical specification with API docs |

**Usage:**
```bash
# Validate good examples (should pass)
python3 ~/.smartspec/.smartspec/scripts/validate_spec_from_prompt.py good/sample-spec-from-prompt.md
python3 ~/.smartspec/.smartspec/scripts/validate_generate_spec.py good/sample-generate-spec.md
```

**Expected Output:**
```
✅ All required checks passed!
```

---

### Bad Examples (With Errors)

These files intentionally contain errors for testing and learning purposes.

| File | Validator | Errors |
|------|-----------|--------|
| `bad/sample-spec-from-prompt.md` | validate_spec_from_prompt.py | Missing sections: architecture, implementation, assumptions, constraints, risks |
| `bad/sample-generate-spec.md` | validate_generate_spec.py | Missing sections: architecture, data models, implementation, testing |

**Usage:**
```bash
# Validate bad examples (should fail)
python3 ~/.smartspec/.smartspec/scripts/validate_spec_from_prompt.py bad/sample-spec-from-prompt.md
python3 ~/.smartspec/.smartspec/scripts/validate_generate_spec.py bad/sample-generate-spec.md
```

**Expected Output:**
```
## Summary
- **Errors:** 5
- **Warnings:** 2

## Errors
- Missing required section: architecture
- Missing required section: implementation
...
```

**Auto-fix:**
```bash
# Apply auto-fix to add missing sections
python3 ~/.smartspec/.smartspec/scripts/validate_spec_from_prompt.py bad/sample-spec-from-prompt.md --apply
```

---

### Empty Examples (For Practice)

These files contain minimal content for hands-on practice.

| File | Validator | Description |
|------|-----------|-------------|
| `empty/sample-spec-from-prompt.md` | validate_spec_from_prompt.py | Minimal spec template |

**Usage:**
```bash
# Start with empty template
cp empty/sample-spec-from-prompt.md my-spec.md

# Edit and add content
vim my-spec.md

# Validate
python3 ~/.smartspec/.smartspec/scripts/validate_spec_from_prompt.py my-spec.md

# Auto-fix to add missing sections
python3 ~/.smartspec/.smartspec/scripts/validate_spec_from_prompt.py my-spec.md --apply
```

---

## Quick Start Tutorial

### 1. Download Sample Files

```bash
# Clone repository
git clone https://github.com/naibarn/SmartSpec.git
cd SmartSpec/examples/validators
```

### 2. Validate Good Example

```bash
python3 ../../.smartspec/scripts/validate_spec_from_prompt.py good/sample-spec-from-prompt.md
```

**Expected:** ✅ All checks passed

### 3. Validate Bad Example

```bash
python3 ../../.smartspec/scripts/validate_spec_from_prompt.py bad/sample-spec-from-prompt.md
```

**Expected:** ❌ Errors found

### 4. Apply Auto-fix

```bash
# Create a copy first
cp bad/sample-spec-from-prompt.md test-spec.md

# Apply auto-fix
python3 ../../.smartspec/scripts/validate_spec_from_prompt.py test-spec.md --apply
```

**Expected:** ✅ Sections added

### 5. Verify Fixes

```bash
python3 ../../.smartspec/scripts/validate_spec_from_prompt.py test-spec.md
```

**Expected:** ✅ All checks passed (with info messages about placeholders)

---

## Learning Exercises

### Exercise 1: Basic Validation

**Objective:** Learn to validate and fix specifications

**Steps:**
1. Copy empty template: `cp empty/sample-spec-from-prompt.md exercise1.md`
2. Add basic content (problem, solution, requirements)
3. Validate: `python3 ../../.smartspec/scripts/validate_spec_from_prompt.py exercise1.md`
4. Apply auto-fix: Add `--apply` flag
5. Fill in TODO placeholders
6. Validate again

**Success Criteria:**
- [ ] File created
- [ ] Validation run
- [ ] Auto-fix applied
- [ ] At least 3 sections completed
- [ ] Final validation passes

---

### Exercise 2: Compare Examples

**Objective:** Understand the difference between good and bad specs

**Steps:**
1. Open `good/sample-spec-from-prompt.md`
2. Open `bad/sample-spec-from-prompt.md`
3. Compare the two files
4. Identify missing sections in bad example
5. Validate both files
6. Compare validation reports

**Questions:**
- What sections are missing in the bad example?
- What makes the good example "good"?
- How detailed should each section be?

---

### Exercise 3: Fix Bad Example

**Objective:** Practice fixing validation errors

**Steps:**
1. Copy bad example: `cp bad/sample-spec-from-prompt.md exercise3.md`
2. Validate to see errors
3. Apply auto-fix
4. Fill in all TODO placeholders with real content
5. Validate again
6. Ensure 0 errors

**Success Criteria:**
- [ ] All errors fixed
- [ ] All TODO replaced with content
- [ ] Validation passes
- [ ] No info messages

---

## Validation Commands Reference

### Basic Validation (Preview Mode)

```bash
# Just check, don't modify
python3 ~/.smartspec/.smartspec/scripts/validate_spec_from_prompt.py file.md
```

### Auto-fix Mode

```bash
# Check and automatically fix issues
python3 ~/.smartspec/.smartspec/scripts/validate_spec_from_prompt.py file.md --apply
```

### Generate Report

```bash
# Save validation report to file
python3 ~/.smartspec/.smartspec/scripts/validate_spec_from_prompt.py file.md --output report.md
```

### Specify Repository Root

```bash
# Validate with custom repo root
python3 ~/.smartspec/.smartspec/scripts/validate_spec_from_prompt.py file.md --repo-root /path/to/repo
```

---

## Tips & Best Practices

### 1. Always Preview First

```bash
# Preview changes before applying
python3 validate_spec.py file.md

# Review the report, then apply
python3 validate_spec.py file.md --apply
```

### 2. Use Version Control

```bash
# Commit before auto-fix
git add file.md
git commit -m "Before auto-fix"

# Apply auto-fix
python3 validate_spec.py file.md --apply

# Review changes
git diff file.md

# Commit if satisfied
git add file.md
git commit -m "After auto-fix"
```

### 3. Replace TODO Placeholders

Auto-fix adds TODO placeholders. Always replace them with real content:

```markdown
## Architecture

TODO: Add architecture details  ← Replace this!
```

### 4. Validate Regularly

```bash
# Add to your workflow
smartspec generate_spec_from_prompt "Create user auth"
python3 validate_spec_from_prompt.py .spec/requirements/spec.md --apply
```

### 5. Use Good Examples as Templates

```bash
# Copy good example as starting point
cp good/sample-spec-from-prompt.md my-new-spec.md

# Modify for your needs
vim my-new-spec.md

# Validate
python3 validate_spec_from_prompt.py my-new-spec.md
```

---

## Troubleshooting

### Issue: "File not found"

**Solution:**
```bash
# Use absolute path
python3 ~/.smartspec/.smartspec/scripts/validate_spec_from_prompt.py $(pwd)/file.md

# Or navigate to directory first
cd /path/to/files
python3 ~/.smartspec/.smartspec/scripts/validate_spec_from_prompt.py file.md
```

### Issue: "Permission denied"

**Solution:**
```bash
# Make script executable
chmod +x ~/.smartspec/.smartspec/scripts/validate_spec_from_prompt.py

# Or use python3 explicitly
python3 ~/.smartspec/.smartspec/scripts/validate_spec_from_prompt.py file.md
```

### Issue: "File too large"

**Solution:**
- File size limit: 10 MB
- Split large files into multiple files
- Remove unnecessary content

### Issue: "Invalid file type"

**Solution:**
- Only `.md` and `.json` files supported
- Rename file to `.md` extension
- Ensure file is text-based

---

## Next Steps

1. **Complete Exercises:** Work through all 3 exercises
2. **Read Documentation:** Check [VALIDATORS_README.md](../../.smartspec/scripts/VALIDATORS_README.md)
3. **Try Interactive Tutorial:** Follow [INTERACTIVE_TUTORIAL_EXAMPLE.md](../../.smartspec/INTERACTIVE_TUTORIAL_EXAMPLE.md)
4. **Integrate into Workflow:** Set up pre-commit hooks
5. **Create Custom Validators:** Extend for your needs

---

## Resources

- [Validators Documentation](../../.smartspec/scripts/VALIDATORS_README.md)
- [Interactive Tutorial](../../.smartspec/INTERACTIVE_TUTORIAL_EXAMPLE.md)
- [Knowledge Base](../../.smartspec/knowledge_base_validators.md)
- [GitHub Repository](https://github.com/naibarn/SmartSpec)

---

**Last Updated:** 2024-12-27
**Maintained by:** SmartSpec Team
