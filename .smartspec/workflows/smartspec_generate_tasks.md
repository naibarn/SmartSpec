---
workflow_id: smartspec_generate_tasks
version: "7.2.1"
status: active
category: core
platform_support:
  - cli
  - kilo
requires_apply: false
writes:
  - ".spec/reports/**"
  - "specs/**/tasks.md (ONLY with --apply)"
---

# /smartspec_generate_tasks

## Purpose
Generate/merge `tasks.md` from SmartSpec `spec.md` (or `plan.md` / `ui-spec.json`) with **preview-first governance** and **strict evidence hooks** that are compatible with `smartspec_verify_tasks_progress_strict`.

Primary outcomes:
- Preview bundle under `.spec/reports/generate-tasks/**`
- `tasks.md` preview that passes strict validators
- Optional governed update of `specs/**/tasks.md` only when `--apply`

---

## Governance contract (MUST)

### Preview-first (MUST)
- Default mode and `--validate-only` MUST NOT modify any file under `specs/**`.
- Without `--apply`, this workflow MUST only write to `.spec/reports/**`.

### Governed writes (MUST)
- With `--apply`, may update/create ONLY:
  - `specs/<category>/<spec-id>/tasks.md`
- MUST write atomically (temp + rename).
- MUST create a backup copy under the run report folder.

### Script hygiene (MUST)
- MUST NOT create ad-hoc scripts anywhere (repo root or otherwise).
- Maintained scripts MUST be referenced only from `.smartspec/scripts/`.
- `.spec/` is outputs/reports only.

### No network / no shell (MUST)
- MUST NOT use the network.
- MUST NOT use `sh -c` or non-allowlisted shells.

---

## Inputs

### Positional input (required)
- `specs/<category>/<spec-id>/spec.md`
- OR `specs/<category>/<spec-id>/plan.md`
- OR `specs/<category>/<spec-id>/ui-spec.json`

The workflow MUST resolve the spec root folder as:
- `specs/<category>/<spec-id>/`

---

## Flags
- `--apply`: write governed `specs/**/tasks.md` (ONLY after preview validates)
- `--validate-only`: preview + validation only (no governed writes)
- `--json`: add machine-readable summary to report folder

---

## Outputs
All outputs MUST be written under:
- `.spec/reports/generate-tasks/<run-id>/`

Files:
- `preview/<spec-folder>/tasks.md`
- `diff/<spec-id>.patch`
- `report.md`
- `report.json` (when `--json`)
- `backup/<spec-folder>/tasks.md` (ONLY when `--apply`)

---

## Canonical `tasks.md` format (MUST)

### Required structure
1) Title (H1)
2) Header table (2 columns) near the top (within ~80 lines)
3) `## Tasks`
4) Tasks are markdown checkboxes with stable IDs

Example:
```md
# Authentication Tasks

| Key | Value |
| --- | --- |
| Spec | specs/core/spec-core-001-authentication/spec.md |
| Updated | 2025-12-24 |

## Tasks

### Phase 1: Foundations
- [ ] TSK-AUTH-001 Initialize auth service skeleton
  evidence: code path=packages/auth-service/package.json contains="\"name\": \"auth-service\""
  evidence: test path=packages/auth-service/package.json command="npm test"
```

---

## Evidence hooks (MUST)
This workflow MUST produce evidence hooks that pass `.smartspec/scripts/validate_evidence_hooks.py`.

### Canonical line format
- `evidence: <code|test|docs|ui> key=value key="value with spaces" ...`

### Allowed types + keys
- `code`: `path` (required), optional `symbol|contains|regex`
- `docs`: `path` (required), optional `heading|contains|regex`
- `ui`: `path` (required), optional `selector|contains|regex`
- `test`: `path` (required), optional `command|contains|regex`

### Hard rules (MUST)
- `path=` MUST be a repo-relative file path.
- **`path=` MUST NOT contain whitespace.**
  - ✅ `path=package.json`
  - ❌ `path="npm run build"`
- `path=` MUST NOT be a command token (e.g., `npm`, `npx`, `docker`, `docker-compose`, ...).
- Glob patterns are forbidden in `path=` (e.g., `src/**/*.ts`).
- Any value containing spaces MUST be quoted.

### Test evidence rule (prevents verify false-negative)
If the evidence is a command, it MUST be recorded in `command=` and anchored with a real file in `path=`.

Examples:
- ✅ `evidence: test path=package.json command="npm run build"`
- ✅ `evidence: test path=prisma/schema.prisma command="npx prisma validate"`
- ✅ `evidence: test path=docker-compose.yml command="docker-compose up"`
- ❌ `evidence: test path="npm run build"`
- ❌ `evidence: test path=npm run build`

### Docs-vs-code rule (prevents mismatch)
If you need `heading=...` and the file is docs/spec-like (`.md/.yaml/.yml/.json/.txt`), use `docs` evidence, not `code`.

---

## Procedure (what the agent MUST do)

### Step 0 — Resolve spec folder
- Derive spec root folder `specs/<category>/<spec-id>/`.

### Step 1 — Read inputs
- Read the positional input.
- Also read `spec.md` in the folder when present (even if input is `plan.md`) to ensure coverage.
- If `specs/<category>/<spec-id>/tasks.md` exists, read it for merge.

### Step 2 — Generate tasks (in-memory)
- Generate a normalized tasks list.
- Preserve existing Task IDs where semantic match exists.
- New tasks MUST use the same project ID scheme.

### Step 3 — Normalize evidence (in-memory) (MUST)
Before writing preview, normalize any evidence into canonical form:

**IMPORTANT:** All file paths in evidence MUST follow naming convention standard:
- Load naming convention from `.smartspec/standards/naming-convention.md`
- Validate that evidence paths follow kebab-case convention
- Add naming convention guidance to task descriptions
- See "Naming Convention Integration" section below for details

1) Quote values with spaces:
- `command=npx prisma validate` → `command="npx prisma validate"`

2) Convert command-ish evidence into canonical test evidence:
- `evidence: npm run build` → `evidence: test path=package.json command="npm run build"`

3) Fix **path-as-command** (critical):
- `evidence: test path="npm run build"` → `evidence: test path=package.json command="npm run build"`
- `evidence: test path=npm run build` → `evidence: test path=package.json command="npm run build"`

4) Ensure `test` always has `path=`:
- If a test evidence has `command=` but no `path=`, add a stable anchor file path.

5) Switch `code`→`docs` when using `heading=` on docs-like files.

> Hint: The canonical migrator/normalizer lives at `.smartspec/scripts/migrate_evidence_hooks.py`.
> Generator implementations SHOULD reuse the same normalization logic.

### Step 4 — Write preview bundle
Write to `.spec/reports/generate-tasks/<run-id>/`:
- `preview/<spec-folder>/tasks.md`
- `diff/<spec-id>.patch`
- `report.md`
- `report.json` (optional)

### Step 5 — Validate preview (MUST)
Run validators on the **preview** tasks file:

1) Evidence hooks:
```bash
python3 .smartspec/scripts/validate_evidence_hooks.py .spec/reports/generate-tasks/<run-id>/preview/<spec-folder>/tasks.md
```

2) Tasks structure:
```bash
python3 .smartspec/scripts/validate_tasks_enhanced.py .spec/reports/generate-tasks/<run-id>/preview/<spec-folder>/tasks.md --spec specs/<category>/<spec-id>/spec.md
```

If any validator fails:
- MUST exit non-zero
- MUST NOT apply changes

### Step 6 — Apply (ONLY if `--apply`)
- Create backup:
  - `.spec/reports/generate-tasks/<run-id>/backup/<spec-folder>/tasks.md`
- Atomic replace:
  - `specs/<category>/<spec-id>/tasks.md`

---

## Invocation

### Validate-only (preview-first)

**CLI:**
```bash
/smartspec_generate_tasks specs/<category>/<spec-id>/spec.md --validate-only
```

**Kilo Code:**
```bash
/smartspec_generate_tasks.md specs/<category>/<spec-id>/spec.md --validate-only --platform kilo
```

### Apply (governed write)

**CLI:**
```bash
/smartspec_generate_tasks specs/<category>/<spec-id>/spec.md --apply
```

**Kilo Code:**
```bash
/smartspec_generate_tasks.md specs/<category>/<spec-id>/spec.md --apply --platform kilo
```

---

## Troubleshooting

### "validate-only แต่ไปแก้ tasks.md จริง"
- Hard violation. STOP and treat the run as failed.

### "Validator ผ่าน แต่ verifier ยังหาไม่เจอ"
- Usually indicates weak evidence (path-only) or wrong evidence type.
- Add matchers (`contains/regex/symbol/heading/selector`) and ensure docs use `docs`.

### "ยังมี test path ที่เป็นคำสั่ง"
- This is invalid under v7.2.1.
- Fix by moving the command into `command=` and using a real file for `path=`.

---

## Related workflows
- `/smartspec_migrate_evidence_hooks` (normalize legacy evidence)
- `/smartspec_verify_tasks_progress_strict` (strict verific

---

## Naming Convention Integration

### Purpose

Ensure all generated evidence paths follow SmartSpec naming convention standard to prevent naming issues during implementation and verification.

### Requirements (MUST)

1. **Load Naming Convention Standard**
   - Read `.smartspec/standards/naming-convention.md`
   - Parse naming rules (kebab-case, suffixes, directories)
   - Use standard throughout task generation

2. **Validate Evidence Paths**
   - All evidence paths MUST follow naming convention
   - Check kebab-case format
   - Check appropriate suffixes (`.service.ts`, `.provider.ts`, etc.)
   - Check correct directory placement

3. **Add Naming Guidance to Tasks**
   - Include naming convention hints in task descriptions
   - Specify expected file type and suffix
   - Indicate correct directory placement

### Task Format with Naming Convention

**Standard format:**
```markdown
### Phase 1: Foundations

- [ ] TSK-AUTH-001 Initialize auth service skeleton
  
  **Naming Convention:**
  - Use kebab-case: `auth-service.ts`
  - Use service suffix: `.service.ts` for business logic
  - Place in services/: Business logic and core functionality
  
  **Evidence:**
  - code: path=packages/auth-service/src/services/auth-service.ts
  - test: path=packages/auth-service/tests/unit/services/auth-service.test.ts
```

**Enhanced format (with architecture):**
```markdown
### Phase 1: Foundations

- [ ] TSK-AUTH-057 Integrate SMS provider
  
  Implement SMS provider integration for sending verification codes.
  
  **Architecture:**
  - **Package:** `auth-lib` (Shared code, utilities, models)
  - **Directory:** `providers/` (External integrations)
  - **File Type:** Provider (External service integration)
  
  **Naming Convention:**
  - Use kebab-case: `sms-provider.ts`
  - Use provider suffix: `.provider.ts` for external integrations
  - Place in providers/: External service integrations
  - Follow pattern: `{service-name}-provider.ts`
  
  **Evidence:**
  - code: path=packages/auth-lib/src/providers/sms-provider.ts
  - test: path=packages/auth-lib/tests/unit/providers/sms-provider.test.ts
  
  **Implementation Notes:**
  - Follow naming convention strictly
  - Create file at exact path specified
  - Do not rename or move files without updating tasks.md
```

### Validation Rules

**Evidence path validation:**

1. **Kebab-case check:**
   ```python
   # Filename must be kebab-case
   filename = Path(evidence_path).name
   if not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*\.[a-z]+(\.[a-z]+)?$', filename):
       raise NamingConventionError(f"Not kebab-case: {filename}")
   ```

2. **Suffix check:**
   ```python
   # File must have appropriate suffix
   suffixes = {
       'service': '.service.ts',
       'provider': '.provider.ts',
       'client': '.client.ts',
       'controller': '.controller.ts',
       'middleware': '.middleware.ts',
       'util': '.util.ts',
       'model': '.model.ts',
       # ... more suffixes
   }
   
   file_type = detect_file_type(filename, suffixes)
   if not file_type:
       warnings.append(f"Missing or invalid suffix: {filename}")
   ```

3. **Directory check:**
   ```python
   # File should be in correct directory
   expected_dir = get_expected_directory(file_type)
   actual_dir = Path(evidence_path).parent.name
   if actual_dir != expected_dir:
       warnings.append(f"Wrong directory: expected {expected_dir}, got {actual_dir}")
   ```

### Integration with Other Workflows

**Downstream workflows that depend on naming convention:**

1. **`/smartspec_execute_prompts_batch`**
   - Reads naming convention from tasks
   - Validates file paths during implementation
   - Enforces naming convention strictly

2. **`/smartspec_verify_tasks_progress_strict`**
   - Checks naming convention compliance
   - Reports violations separately
   - Suggests fixes for non-compliant files

3. **`/smartspec_fix_naming_issues`**
   - Uses naming convention for matching
   - Suggests compliant alternatives
   - Auto-fixes violations when possible

### Example Implementation

**Python helper function:**

```python
def add_naming_convention_guidance(task: Dict, evidence_path: str) -> str:
    """Add naming convention guidance to task description"""
    
    # Parse evidence path
    path = Path(evidence_path)
    filename = path.name
    directory = path.parent.name
    package = extract_package_name(path)
    
    # Detect file type
    file_type = detect_file_type(filename)
    
    # Get naming rules
    case_rule = "Use kebab-case"
    suffix_rule = f"Use {file_type} suffix: .{file_type}.ts"
    directory_rule = f"Place in {directory}/: {get_directory_purpose(directory)}"
    
    # Generate guidance
    guidance = f"""
**Naming Convention:**
- {case_rule}: `{filename}`
- {suffix_rule}
- {directory_rule}
"""
    
    return guidance
```

### Benefits

1. **Prevention**
   - Catch naming issues at task generation time
   - Prevent implementation mistakes
   - Reduce verification failures

2. **Clarity**
   - Clear naming expectations
   - Explicit file type and location
   - Consistent across all tasks

3. **Automation**
   - Automated validation
   - Automated guidance generation
   - Seamless integration with other workflows

### Validation Command

**Validate generated tasks:**
```bash
# After generating tasks, validate naming convention
python3 .smartspec/scripts/validate_naming_convention.py \
  --check-tasks .spec/reports/generate-tasks/<run-id>/preview/<spec-folder>/tasks.md
```

**Expected output:**
```
✅ All evidence paths follow naming convention
✅ All tasks include naming guidance
✅ Tasks ready for implementation
```

### Related Tools

- `/smartspec_validate_naming_convention` - Validate naming convention compliance
- `/smartspec_enrich_tasks` - Add naming convention to existing tasks
- `/smartspec_fix_naming_issues` - Fix naming issues in evidence paths

---

## Version History

### v7.2.2 (2025-12-27)
- Added naming convention integration
- Added naming guidance to task format
- Added validation rules for evidence paths
- Enhanced task template with architecture and naming sections

### v7.2.1 (Previous)
- Evidence hooks validation
- Preview-first governance
- Strict evidence format
