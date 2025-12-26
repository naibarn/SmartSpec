---
description: Assist in migrating between design systems (e.g., MUI to Ant Design).
version: 6.0.0
workflow: /smartspec_design_system_migration_assistant
---

# smartspec_design_system_migration_assistant

> **Version:** 6.1.1  
> **Status:** Proposed  
> **Category:** migration

## Purpose

Assist a controlled migration from one UI component library / design token system to another by generating **deterministic patches** and **risk-scored change sets**.

This workflow supports two modes:

- **Preview mode (default):** produces diffs and reports only (no code changes).
- **Apply mode (`--apply`):** performs governed code modifications **within approved source roots**, with backups and atomic writes.

It does **not** run the application, does **not** execute network calls, and does **not** install dependencies.

---

## Governance contract

This workflow MUST follow:

- `knowledge_base_smartspec_handbook.md` (v6)
- `.spec/smartspec.config.yaml`

### Write scopes (enforced)

**Always allowed writes (safe outputs):**

- Reports: `.spec/reports/design-system-migration/**`
- Prompts (optional): `.spec/prompts/**`
- Generated scripts (optional): `.smartspec/generated-scripts/**`

**Governed writes (ONLY with `--apply`):**

- Source code under `--source-root` (and optional additional roots) **after** path safety checks.

**Forbidden writes (must hard-fail):**

- Any path outside config `safety.allow_writes_only_under`
- Any path under config `safety.deny_writes_under`
- Any governed artifact not explicitly targeted (e.g., `specs/**`, `.spec/SPEC_INDEX.json`, `.spec/WORKFLOWS_INDEX.yaml`)
- Any writes to dependency caches / package managers (`node_modules/`, `.pnpm-store/`, etc.)

### `--apply` behavior

- Without `--apply`: MUST NOT modify source code.
- With `--apply`: MAY modify source code, but ONLY within allowed source roots and only via the atomic-write rules below.
- The report MUST declare whether `--apply` was used.

---

## Threat model (minimum)

This workflow must defend against:

- Path traversal / symlink escape on any read/write path (audit reports, token files, source roots, output roots).
- Secret leakage into reports (tokens/keys in `.env`, configs, or logs).
- Untrusted input artifacts (spoofed audit reports / token maps) leading to arbitrary file reads or wrong migrations.
- Incorrect refactors causing UI regressions.
- Data loss from partial writes.

### Hardening requirements (MANDATORY)

- **No network access:** Respect `safety.network_policy.default=deny`.
- **No shell execution:** Do not run arbitrary commands from inputs.
- **Path normalization (reads + writes):** Reject traversal (`..`), absolute paths, and control characters on any user-supplied path.
- **No symlink escape (reads + writes):** Do not read/write through symlinks that resolve outside allowed scopes.
- **Read scope enforcement:** All reads MUST remain within project root (or configured workspace roots if supported).
- **Output collision:** Respect `safety.output_collision` (never overwrite existing run folders).
- **Redaction:** Apply `safety.redaction` to all reports and patches; never include secrets.
- **Excerpt policy:** Do not paste large file contents; include minimal snippets.

### Output root safety (`--out`) (MANDATORY)

If `--out` is provided, it is a *requested* base output root and MUST:

- resolve under config `safety.allow_writes_only_under`
- not fall under config `safety.deny_writes_under`
- not be a runtime source folder
- hard-fail with usage/config error (`exit 2`) if invalid

---

## Inputs

### Required

- `--source-root <path>`: Root directory of UI source code to migrate.
- `--from <name>`: Source design system/library identifier (e.g., `mui`, `antd`, `chakra`, `custom`).
- `--to <name>`: Target design system/library identifier.

### Recommended (for accuracy)

- `--audit-summary <path>`: Path to a `smartspec_ui_component_audit` `summary.json` (used for token paths and findings).
- `--token-map <path>`: Explicit mapping file (JSON/YAML) defining token and component mappings.

### Optional

- `--include-globs <glob[,glob...]>`: Restrict migration to matching files.
- `--exclude-globs <glob[,glob...]>`: Exclude files.
- `--framework <react|next|vue|svelte|auto>`
- `--style-system <css|sass|css-modules|tailwind|css-in-js|auto>`
- `--max-files <int>` / `--max-bytes <int>` / `--max-seconds <int>`: Bounded scanning.
- `--confidence-threshold <high|medium>`: Minimum confidence required for auto-apply transformations (default: `high`).
- `--apply-scope <high_only|high_and_medium>`: Default `high_only`.

### Input validation (MANDATORY)

- `--source-root` MUST exist and be a directory.
- If provided, `--audit-summary` MUST be valid JSON and pass trust rules (below).
- If provided, `--token-map` MUST be a readable file and parse successfully.
- All paths MUST reject traversal (`..`), absolute paths, and control characters.
- All resolved paths MUST remain within project root and MUST NOT escape via symlinks.

---

## Audit report trust rules (MANDATORY)

If `--audit-summary` is used, it is trusted only if:

- `workflow == "smartspec_ui_component_audit"`
- `version` is present
- `run_id` is present
- its file path resolves within project root and does not escape via symlinks

Any token paths extracted from the audit scope (e.g., `scope.design_tokens`) MUST be treated as **untrusted inputs** and MUST be re-validated with the same path safety rules before being read.

If trust validation fails: hard-fail (`exit 2`).

---

## Approach and confidence model

### Structured transforms (MUST)

- For JS/TS/JSX/TSX, transformations MUST be **AST-based** (codemod style). Regex-only replacements are NOT allowed in apply mode.
- For CSS/Sass/CSS Modules, transformations MUST be token-aware parsing (or conservative replacements limited to declared token contexts).

### Confidence levels

Each proposed change MUST be labeled:

- **high**: deterministic mapping and safe context (e.g., known component import rename, token literal within style prop)
- **medium**: likely mapping but may need review (e.g., heuristic variant mapping)
- **low**: ambiguous; MUST be preview-only (never auto-applied)

Apply policy:

- Default: apply **high** confidence only.
- If `--apply-scope=high_and_medium`: medium may be applied but MUST be listed separately and MUST include extra evidence in the report.

---

## Preview-first workflow (MANDATORY)

1) Generate a complete patch set and report in preview mode.
2) Only after review, run again with `--apply` to apply changes.

In apply mode, the workflow MUST still generate the patch set and report, and include an applied-vs-proposed summary.

---

## Backups and atomic writes (MANDATORY)

When `--apply` is used:

- **Backup MUST** be created before modifying each file:
  - store pre-image copies under `.spec/reports/design-system-migration/<run-id>/backups/...`
  - store file hash manifest (sha256) before/after in `file_manifest.json`
- **Atomic write MUST** be used:
  - write to a temp file in the same directory, fsync (if available), then rename
- **No partial apply:** if an error occurs mid-run, the workflow MUST stop and report exactly which files were changed and where backups are.

---

## Invocation

### CLI

```bash
/smartspec_design_system_migration_assistant \
  --source-root <path/to/ui> \
  --from mui \
  --to custom \
  [--audit-summary .spec/reports/ui-component-audit/<run-id>/summary.json] \
  [--token-map .smartspec/mappings/design-tokens.json] \
  [--framework auto] \
  [--style-system auto] \
  [--confidence-threshold high] \
  [--apply-scope high_only] \
  [--out <output-root>] \
  [--json]
```

### Kilo Code

```bash
/smartspec_design_system_migration_assistant.md \
  --source-root <path/to/ui> \
  --from mui \
  --to custom \
  [--audit-summary .spec/reports/ui-component-audit/<run-id>/summary.json] \
  [--token-map .smartspec/mappings/design-tokens.json] \
  [--framework auto] \
  [--style-system auto] \
  [--confidence-threshold high] \
  [--apply-scope high_only] \
  [--out <output-root>] \
  [--json] \
  --platform kilo
```

Apply mode example:

```bash
/smartspec_design_system_migration_assistant \
  --source-root <path/to/ui> \
  --from mui \
  --to custom \
  --audit-summary .spec/reports/ui-component-audit/<run-id>/summary.json \
  --token-map .smartspec/mappings/design-tokens.json \
  --apply \
  --out .spec/reports/design-system-migration
```

---

## Output structure

Outputs are written under a unique run folder.

- Default root: `.spec/reports/design-system-migration/<run-id>/...`
- If `--out` is provided, it is treated as a *requested* base output root and MUST pass Output root safety validation; otherwise `exit 2`.

Artifacts:

- `report.md`
- `summary.json`
- `changes.patch` (unified patch for all changes)
- `changes/` (per-file diffs)
- `backups/` (apply mode only)
- `file_manifest.json` (apply mode only; hashes before/after)

### Exit codes

- `0`: Preview generated (or apply completed) successfully.
- `1`: Apply blocked due to strict/confidence rules or migration failures.
- `2`: Usage/config error (unsafe paths, invalid audit summary, invalid token map, invalid globs).

---

## Checks

Each check MUST emit a stable ID (`DSM-xxx`).

### Preflight safety checks (always enforced)

- **DSM-000 Preflight Safety**: Validate paths, `--out` safety, read/write constraints (path normalization + no symlink escape), and scan limits. Fail with `exit 2` on violation.
- **DSM-001 Audit Summary Trusted**: If provided, validate audit summary trust rules.
- **DSM-002 Token Paths Trusted**: Any token paths sourced from audit summary are re-validated; reject unsafe.

### MUST checks (apply blocking)

- **DSM-101 Transform Engine Safe**: AST-based transforms are enabled for JS/TS/JSX/TSX in apply mode.
- **DSM-102 Confidence Threshold**: No changes below the confidence threshold are applied.
- **DSM-103 Backup + Atomic Write**: Backups and atomic writes are enabled in apply mode.

### SHOULD checks (warnings)

- **DSM-201 Reduced Coverage**: Limits reached or some files were skipped.
- **DSM-202 Unsupported Pattern**: Some files/patterns could not be reliably transformed; listed as manual follow-ups.
- **DSM-203 Potential Behavior Change**: Change may alter runtime behavior (e.g., event handlers, layout assumptions); flagged for review.

---

## `report.md` required content

The report MUST include:

1. **Header**: run-id, from/to, source-root, framework/style system, whether `--apply` was used.
2. **Scope**: scanned file counts, include/exclude globs, ignored dirs, limits.
3. **Trust & safety**: audit summary trust result, token path validation, redaction counts.
4. **Change plan**:
   - grouped by confidence (high/medium/low)
   - counts per change type (imports, components, tokens, css)
5. **Patch summary**: where to find `changes.patch` and per-file diffs.
6. **Manual follow-ups**: list of files needing human edits.
7. **Rollback** (apply mode): backup location + how to restore.
8. **Recommended next commands**:
   - MUST be registry-backed (`.spec/WORKFLOWS_INDEX.yaml`).
   - If suggesting a SmartSpec workflow, include both CLI + Kilo forms.

---

## `summary.json` schema (minimum)

```json
{
  "workflow": "smartspec_design_system_migration_assistant",
  "version": "6.1.1",
  "run_id": "string",
  "mode": "preview|apply",
  "status": "ok|warn|error",
  "scope": {
    "source_root": "string",
    "from": "string",
    "to": "string",
    "audit_summary_path": "string|null",
    "token_map_path": "string|null",
    "confidence_threshold": "high|medium",
    "apply_scope": "high_only|high_and_medium"
  },
  "summary": {
    "files_scanned": 0,
    "files_changed": 0,
    "high_confidence_changes": 0,
    "medium_confidence_changes": 0,
    "low_confidence_changes": 0,
    "reduced_coverage": false
  },
  "changes": [
    {
      "file": "string",
      "confidence": "high|medium|low",
      "change_type": "import|component|token|css|other",
      "why": "string",
      "evidence": [{"ref": "string"}]
    }
  ],
  "writes": {
    "reports": [
      "path/to/report.md",
      "path/to/summary.json",
      "path/to/changes.patch"
    ]
  }
}
```

---

# End of workflow doc

