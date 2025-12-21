# SmartSpec A2UI Phase 4: Integration

## Overview

Phase 4 integrates A2UI workflows with existing SmartSpec core workflows, enabling seamless UI development within the SmartSpec governance framework.

## Integration Points

### 1. SPEC_INDEX Integration ✅

**Updated Workflow:** `smartspec_reindex_specs`

**Changes:**
- Now indexes `specs/**/ui-spec.json` (A2UI specifications)
- UI specs appear in `.spec/SPEC_INDEX.json` under `ui_specs` array
- UI category added to spec categories

**Impact:**
- UI specs are now discoverable via SPEC_INDEX
- `smartspec_project_copilot` can answer questions about UI specs
- UI specs participate in spec governance

**Template:** `.spec/SPEC_INDEX.template.json` created

---

### 2. Tasks Integration ✅

**Updated Workflows:**
- `smartspec_generate_tasks`
- `smartspec_implement_tasks`

**Changes:**

**generate_tasks:**
- Accepts `ui-spec.json` as input (in addition to `spec.md`)
- Generates UI implementation tasks from A2UI specifications
- UI tasks follow same governance as backend tasks

**implement_tasks:**
- Recognizes UI components (including A2UI) in duplication checking
- Implements UI tasks with same governance as backend tasks

**Impact:**
- UI development follows same task-driven workflow as backend
- UI tasks appear in `tasks.md` alongside backend tasks
- UI implementation is governed and auditable

---

### 3. Verification Integration ✅

**Updated Workflow:** `smartspec_verify_tasks_progress_strict`

**Changes:**
- Enhanced `ui` evidence type to support A2UI specs
- Checks `ui-spec.json` validity
- Verifies component catalog adherence
- High confidence verification for valid A2UI implementations

**Impact:**
- UI tasks can be automatically verified
- UI verification follows same evidence-based approach as backend
- UI quality gates integrated with overall quality gates

---

### 4. Documentation Integration ✅

**Updated Workflow:** `smartspec_docs_generator`

**Changes:**
- New mode: `ui-docs`
- Generates UI component documentation from A2UI specs
- Includes component catalog, usage examples, accessibility notes

**Impact:**
- UI documentation generated automatically
- UI docs integrated with project documentation
- Component catalog documented for team reference

---

## Usage Examples

### Example 1: Full UI Development Lifecycle

```bash
# 1. Generate UI spec
/smartspec_generate_ui_spec \
  --requirements "User profile page with avatar, name, email fields" \
  --output specs/feature/spec-003-profile/ui-spec.json

# 2. Review and apply
/smartspec_generate_ui_spec \
  --requirements "User profile page with avatar, name, email fields" \
  --output specs/feature/spec-003-profile/ui-spec.json \
  --apply

# 3. Reindex specs (includes UI spec)
/smartspec_reindex_specs --apply

# 4. Generate tasks from UI spec
/smartspec_generate_tasks \
  --spec specs/feature/spec-003-profile/ui-spec.json

# 5. Review and apply tasks
/smartspec_generate_tasks \
  --spec specs/feature/spec-003-profile/ui-spec.json \
  --apply

# 6. Implement UI from tasks
/smartspec_implement_tasks \
  specs/feature/spec-003-profile/tasks.md \
  --platform web \
  --apply

# 7. Verify UI implementation
/smartspec_verify_tasks_progress_strict \
  specs/feature/spec-003-profile/tasks.md

# 8. Generate UI documentation
/smartspec_docs_generator \
  --mode ui-docs \
  --spec specs/feature/spec-003-profile/ui-spec.json \
  --target-dir docs/ui \
  --write-docs \
  --apply
```

### Example 2: Kilo Code Workflow

```bash
# Generate UI spec
/smartspec_generate_ui_spec.md \
  --requirements "Dashboard with charts and metrics" \
  --output specs/feature/spec-004-dashboard/ui-spec.json \
  --platform kilo \
  --apply

# Generate tasks
/smartspec_generate_tasks.md \
  --spec specs/feature/spec-004-dashboard/ui-spec.json \
  --platform kilo \
  --apply

# Implement UI
/smartspec_implement_tasks.md \
  specs/feature/spec-004-dashboard/tasks.md \
  --platform kilo \
  --apply
```

---

## Benefits

### For Developers

1. **Unified Workflow:** Same workflow for backend and frontend
2. **Automatic Verification:** UI tasks verified automatically
3. **Documentation:** UI docs generated automatically
4. **Governance:** UI development follows same governance as backend

### For Teams

1. **Consistency:** Same process for all development
2. **Traceability:** UI specs → tasks → implementation → verification
3. **Quality:** UI quality gates integrated with overall gates
4. **Auditability:** UI changes tracked and auditable

### For Organizations

1. **Compliance:** UI development governed and auditable
2. **Efficiency:** Reduced manual work with automation
3. **Quality:** Consistent quality across backend and frontend
4. **Visibility:** UI specs discoverable and indexed

---

## Integration Status

| Integration Point | Status | Workflows Updated |
|---|---|---|
| SPEC_INDEX | ✅ Complete | smartspec_reindex_specs |
| Tasks | ✅ Complete | smartspec_generate_tasks, smartspec_implement_tasks |
| Verification | ✅ Complete | smartspec_verify_tasks_progress_strict |
| Documentation | ✅ Complete | smartspec_docs_generator |

---

## Next Steps

Phase 4 is complete! A2UI is now fully integrated with SmartSpec core workflows.

**Optional Enhancements:**
- Add UI-specific quality gates
- Create UI-specific templates
- Add UI performance metrics
- Integrate with design tools

---

## Technical Details

### SPEC_INDEX Schema

```json
{
  "specs": [...],
  "ui_specs": [
    {
      "spec_id": "spec-003-profile",
      "title": "User Profile UI",
      "category": "ui",
      "status": "approved",
      "path": "specs/feature/spec-003-profile/ui-spec.json"
    }
  ],
  "categories": [
    {
      "id": "ui",
      "name": "User Interface",
      "description": "UI specifications (A2UI format)"
    }
  ]
}
```

### Evidence Hook Example

```markdown
- [ ] **TSK-PROFILE-001: Implement profile form**
  - **Evidence Hooks:**
    - `evidence: ui screen=ProfileForm component=ProfileForm states=loading,error,success`
    - `evidence: code path=src/ui/profile/ProfileForm.ts`
    - `evidence: test path=src/ui/profile/ProfileForm.test.ts`
```

### Documentation Mode

```bash
/smartspec_docs_generator \
  --mode ui-docs \
  --spec specs/feature/spec-003-profile/ui-spec.json \
  --target-dir docs/ui \
  --write-docs \
  --apply
```

Generates:
- `docs/ui/components/ProfileForm.md`
- `docs/ui/catalog.md`
- `docs/ui/accessibility.md`

---

## Version Information

- **Phase:** 4 (Integration)
- **SmartSpec Version:** v6.3.6
- **A2UI Version:** v0.8
- **Date:** December 22, 2025

---

**Phase 4 Status:** ✅ **COMPLETE**

A2UI is now fully integrated with SmartSpec! 🎉
