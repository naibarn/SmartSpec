---
description: Refine spec.md (SPEC-first) with deterministic preview/diff + completeness/reuse
  checks.
version: 6.0.3
workflow: /smartspec_generate_spec
---

# smartspec_generate_spec

> **Canonical path:** `.smartspec/workflows/smartspec_generate_spec.md`  
> **Version:** 6.0.3  
> **Status:** Production Ready  
> **Category:** core

## Purpose

Create or refine a `spec.md` using **SPEC-first** governance.

This workflow is the canonical entry point for:

- refining an existing spec by `--spec` or `--spec-ids` (governed)
- enforcing spec completeness (UX/UI baseline + NFRs)
- enforcing reuse-first behavior (avoid duplicates)
- producing an auditable preview + diff before any governed writes
- **populating the component registry** (`.spec/registry/**`)

It is **safe-by-default** and writes governed artifacts only when explicitly applied.

---

## File Locations (Important for AI Agents)

**All SmartSpec configuration and registry files are located in the `.spec/` folder:**

- **Config:** `.spec/smartspec.config.yaml` (NOT `smartspec.config.yaml` at root)
- **Spec Index:** `.spec/SPEC_INDEX.json` (NOT `SPEC_INDEX.json` at root)
- **Registry:** `.spec/registry/` (component registry, reuse index)
- **Reports:** `.spec/reports/` (workflow outputs, previews, diffs)
- **Scripts:** `.spec/scripts/` (automation scripts)

**When searching for these files, ALWAYS use the `.spec/` prefix from project root.**

---

## Governance contract

This workflow MUST follow:

- `knowledge_base_smartspec_handbook.md` (v6)
- `.spec/smartspec.config.yaml`

### Write scopes (enforced)

Allowed writes:

- Governed specs: `specs/**` (**requires** `--apply`)
- Governed registry: `.spec/SPEC_INDEX.json` (**requires** `--apply` and allowlisted)
- **Component registry:** `.spec/registry/**` (**requires** `--apply`)
- Safe outputs (previews/reports): `.spec/reports/generate-spec/**` (no `--apply` required)

Forbidden writes (must hard-fail):

- Any path outside config `safety.allow_writes_only_under`
- Any path under config `safety.deny_writes_under` (excluding `.spec/registry/**`)
- Any runtime source tree modifications

### `--apply` behavior

- Without `--apply`:
  - MUST NOT create/modify `specs/**`, `.spec/SPEC_INDEX.json`, or `.spec/registry/**`.
  - MUST write a deterministic preview bundle to `.spec/reports/`.

- With `--apply`:
  - MAY update target `spec.md` and required companion reference files.
  - MAY update `.spec/SPEC_INDEX.json` **only if** allowlisted.
  - MAY update `.spec/registry/**` files.

---

## Behavior

### 1) Read inputs

- Parse spec.md to extract requirements.
- Load existing registry files for context.

### 2) Refine Spec & Extract Registry Information (MANDATORY)

- Refine `spec.md` based on requirements.
- **Parse the refined spec.md** to extract:
  - API endpoints (method, path, description, status codes)
  - Data models (name, fields, description)
  - Terminology (terms, definitions, categories)
  - Critical sections (sections marked as immutable)

### 3) Preview & Report (Always)

Write:

- `.spec/reports/generate-spec/<run-id>/preview/spec.md`
- `.spec/reports/generate-spec/<run-id>/preview/registry/api-registry.json`
- `.spec/reports/generate-spec/<run-id>/preview/registry/data-model-registry.json`
- `.spec/reports/generate-spec/<run-id>/preview/registry/glossary.json`
- `.spec/reports/generate-spec/<run-id>/preview/registry/critical-sections-registry.json`
- `.spec/reports/generate-spec/<run-id>/diff/spec.patch` (best-effort)
- `.spec/reports/generate-spec/<run-id>/report.md`
- `.spec/reports/generate-spec/<run-id>/summary.json` (if `--json`)

### 4) Validate Preview (MANDATORY)

After generating the preview and before applying, the AI agent **MUST** validate the generated spec and registry files.

**Validation Command:**
```bash
python3 .spec/scripts/validate_spec.py \
  --spec .spec/reports/generate-spec/<run-id>/preview/spec.md \
  --registry .spec/reports/generate-spec/<run-id>/preview/registry/
```

**Validation Rules:**
- **Exit Code `0` (Success):** The spec and registry are valid. The agent may proceed with `--apply`.
- **Exit Code `1` (Failure):** The spec or registry is invalid. The agent **MUST NOT** use `--apply`.
- The full output from the validation script **MUST** be included in `report.md`.

### 5) Apply (only with `--apply` and if validation passes)

- Update `specs/<category>/<spec-id>/spec.md`.
- Update `.spec/SPEC_INDEX.json` (if allowlisted).
- Update `.spec/registry/api-registry.json`.
- Update `.spec/registry/data-model-registry.json`.
- Update `.spec/registry/glossary.json`.
- Update `.spec/registry/critical-sections-registry.json`.

---

## 11) Registry Generation (For AI Agent Implementation)

To ensure a complete and consistent component registry, the AI agent executing this workflow MUST use the following templates and logic when generating registry files.

### 11.1 Merge Logic

When updating registry files, the agent MUST:

1. **Load the existing registry file** from `.spec/registry/`.
2. **Load the new entries** extracted from the refined `spec.md`.
3. **Merge new entries** into the existing registry:
   - Add new items (endpoints, models, terms) if they don't exist.
   - Update existing items if the `owner_spec` matches the current spec.
   - Preserve items owned by other specs.
   - Detect and report conflicts (e.g., same API path with different owner).
4. **Update `last_updated` and `specs_included`** fields.
5. **Write the merged content** to the preview directory.

### 11.2 `api-registry.json` Template

```json
{
  "version": "1.0.3",
  "last_updated": "<ISO_DATETIME>",
  "source": "smartspec_generate_spec",
  "specs_included": ["<spec-id>", ...],
  "endpoints": [
    {
      "method": "POST",
      "path": "/api/v1/auth/register",
      "description": "User registration",
      "owner_spec": "<spec-id>",
      "status_codes": [201, 400, 409, 429]
    }
  ]
}
```

### 11.3 `data-model-registry.json` Template

```json
{
  "version": "1.0.2",
  "last_updated": "<ISO_DATETIME>",
  "source": "smartspec_generate_spec",
  "specs_included": ["<spec-id>", ...],
  "models": [
    {
      "name": "User",
      "description": "Primary user profile entity",
      "owner_spec": "<spec-id>",
      "shared_with": ["<other-spec-id>"],
      "fields": ["id", "email", "name", ...]
    }
  ]
}
```

### 11.4 `glossary.json` Template

```json
{
  "version": "1.0.2",
  "last_updated": "<ISO_DATETIME>",
  "source": "smartspec_generate_spec",
  "specs_included": ["<spec-id>", ...],
  "terms": [
    {
      "term": "JWT",
      "definition": "JSON Web Token - Stateless access token",
      "owner_spec": "<spec-id>",
      "category": "authentication"
    }
  ]
}
```

### 11.5 `critical-sections-registry.json` Template

```json
{
  "version": "1.0.2",
  "last_updated": "<ISO_DATETIME>",
  "source": "smartspec_generate_spec",
  "specs_included": ["<spec-id>", ...],
  "sections": [
    {
      "spec_id": "<spec-id>",
      "title": "Security Threat Model (STRIDE)",
      "location": "Section 3.1",
      "hash": "stride-threat-model",
      "allow_update": false,
      "reason": "Core security requirements - changes require security review"
    }
  ]
}
```

---

# End of workflow doc
