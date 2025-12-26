---
name: /smartspec_docs_generator
version: 6.1.1
role: documentation
write_guard: REPORTS-ONLY+GOVERNED-WRITE-WITH-APPLY
purpose: Generate project documentation bundles (API docs, user guide, architecture
  diagrams) from spec/registry/code signals. Preview-first; default writes reports
  only; governed writes to repo docs require explicit opt-in and config allowlist.
version_notes:
- v6.1.1: Adds v6 hardening (path normalization + no symlink escape + output root
    safety + atomic writes); replaces full-content previews with change plan + diff/excerpt+hash;
    introduces explicit --write-docs gate for repo writes; adds network gate (--allow-network)
    and external tool allowlist/no-shell policy; aligns chain integration with deployment_planner/release_tagger/test
    workflows; updates Kilo examples to include --platform kilo.
description: Generate technical documentation from specs and code.
workflow: /smartspec_docs_generator
---


# /smartspec_docs_generator (v6.1.1)

Generate documentation artifacts from SmartSpec sources and project structure.

Supported modes:

- `api-docs`: generate API reference (OpenAPI/GraphQL summaries, endpoint tables, examples)
- `user-guide`: generate user/operator guide (flows, setup, troubleshooting)
- `architecture-diagram`: generate diagram source files + rendered outputs (best-effort)
- `ui-docs`: generate UI component documentation from A2UI specs (component catalog, usage examples, accessibility notes)

This workflow is **preview-first**:

- Default: writes **reports only** under `.spec/reports/docs-generator/**`.
- With `--apply` + `--write-docs`: may write docs into a governed target directory (e.g., `docs/`).

It does **not** install dependencies.

---

## 0) Governance contract

This workflow MUST follow:

- `knowledge_base_smartspec_handbook.md` (v6)
- `.spec/smartspec.config.yaml`

### 0.1 Write scopes (enforced)

**Always allowed writes (safe outputs):**

- Reports: `.spec/reports/docs-generator/**`
- Optional prompts: `.spec/prompts/**`
- Optional generated scripts: `.smartspec/generated-scripts/**`

**Governed writes (ONLY with `--apply` AND `--write-docs`):**

- Documentation files under a validated `--target-dir` (example: `docs/`).

**Forbidden writes (must hard-fail):**

- Any path outside config `safety.allow_writes_only_under`
- Any path under config `safety.deny_writes_under`
- Any governed artifact not explicitly targeted (e.g., `specs/**`, `.spec/SPEC_INDEX.json`, `.spec/WORKFLOWS_INDEX.yaml`)
- Any runtime source tree modification unless `--write-docs` is set

### 0.2 `--apply` behavior

- Without `--apply`: MUST NOT write governed outputs.
- With `--apply`: governed writes are still disabled unless `--write-docs` is also set.

---

## 1) Threat model (minimum)

This workflow must defend against:

- Path traversal / symlink escape on any read/write path.
- Secret leakage into generated docs and reports.
- DoS / runaway output from huge specs/logs/schemas.
- Tooling injection when rendering diagrams.
- Network misuse when fetching remote schemas.

---

## 2) Security hardening (MANDATORY)

- **No shell execution:** do not build shell command strings.
- **Path normalization (reads + writes):** reject traversal (`..`), absolute paths, and control characters.
- **No symlink escape (reads + writes):** realpath MUST remain within allowed scopes.
- **Output collision:** respect `safety.output_collision` (never overwrite existing run folders).
- **Redaction:** apply `safety.redaction` patterns to all report outputs.
- **Excerpt policy:** do not paste full generated docs into reports; use diff summaries + excerpts + hashes.
- **Bounded scanning:** enforce file count/byte/time limits from config; emit `DOC-204 Reduced Coverage` when limits are hit.
- **Atomic writes (governed):** for `--apply` writes, use temp+rename.

### 2.1 Output root safety (`--out`) (MANDATORY)

If `--out` is provided, it is a *requested* base output root and MUST:

- resolve under config `safety.allow_writes_only_under`
- not fall under config `safety.deny_writes_under`
- hard-fail (`exit 2`) if invalid

### 2.2 Network policy (MANDATORY)

- Default network access MUST be denied.
- Remote schema fetch is allowed only when `--allow-network` is set.
- If the runtime cannot enforce deny, the workflow MUST emit `DOC-206 Network Not Enforced`.

### 2.3 External tool policy (architecture diagrams)

If diagram rendering requires external tools:

- MUST spawn without a shell
- MUST be allowlisted by name (e.g., `manus-render-diagram`, `mmdc`, `dot`), as configured
- MUST enforce timeouts
- MUST restrict inputs/outputs to the run folder (preview) or validated `--target-dir` (apply)

If tool policy cannot be satisfied, render step MUST be skipped and recorded as reduced coverage.

---

## 3) Inputs

### 3.1 Primary inputs

- `--mode <api-docs|user-guide|architecture-diagram|ui-docs>` (required)
- `--spec <path>`: recommended `specs/<category>/<spec-id>/spec.md` (best-effort accepted)

### 3.2 Optional inputs

- `--tasks <path>`: optional tasks context (read-only)
- `--registry-roots <csv>` / `--index <path>`: optional overrides (read-only; config-first)
- `--template <path>`: optional docs template (md/yaml/json) treated as untrusted data
- `--schema-source <path|url>`: optional OpenAPI/GraphQL source
- `--allow-network`: required if `--schema-source` is a URL

### 3.3 Governed write target

- `--target-dir <path>`: destination for docs when applying (example: `docs/`)
- `--write-docs`: enables governed writes to `--target-dir` (requires `--apply`)

> Compatibility: legacy flag `--output-dir` MAY be accepted as an alias for `--target-dir`, but `--target-dir` is canonical.

---

## 4) Input validation (MANDATORY)

All user-supplied paths (`--spec`, `--tasks`, `--template`, `--schema-source` when path, `--target-dir`, `--out`) MUST:

- reject traversal (`..`), absolute paths, and control characters
- resolve within project root and MUST NOT escape via symlinks

If `--apply` is set:

- `--write-docs` MUST be set
- `--target-dir` MUST be set and MUST be validated:
  - resolves under config allowlist
  - not under denylist
  - is not a symlink

If `--schema-source` is a URL:

- `--allow-network` MUST be set
- URL MUST be https
- any auth headers/tokens MUST NOT be accepted via flags (use placeholders)

If any validation fails: `exit 2`.

---

## 5) Flags

### 5.1 Universal flags (must support)

- `--config <path>`
- `--lang <th|en>`
- `--platform <cli|kilo|ci|other>`
- `--apply`
- `--out <path>`
- `--json`
- `--quiet`

### 5.2 Workflow-specific flags

- `--mode <api-docs|user-guide|architecture-diagram|ui-docs>` (required)
- `--spec <path>`
- `--tasks <path>`
- `--template <path>`
- `--schema-source <path|url>`
- `--allow-network`
- `--target-dir <path>` (governed)
- `--write-docs` (governed gate)
- `--max-pages <int>` / `--max-bytes <int>` / `--max-seconds <int>`
- `--mode <normal|strict>` / `--strict` (content quality mode; default normal)

---

## 6) Invocation

### CLI (preview)

```bash
/smartspec_docs_generator \
  --mode api-docs \
  --spec specs/<category>/<spec-id>/spec.md \
  --out .spec/reports/docs-generator \
  --json
```

### CLI (apply to docs/; explicit opt-in)

```bash
/smartspec_docs_generator \
  --mode user-guide \
  --spec specs/<category>/<spec-id>/spec.md \
  --target-dir docs \
  --write-docs \
  --apply \
  --out .spec/reports/docs-generator \
  --json
```

### Kilo Code

```bash
/smartspec_docs_generator.md \
  --mode architecture-diagram \
  --spec specs/<category>/<spec-id>/spec.md \
  --out .spec/reports/docs-generator \
  --json \
  --platform kilo
```

---

## 7) Preview-first outputs

All runs produce a unique run folder.

- Default report root: `.spec/reports/docs-generator/<run-id>/...`

Artifacts (safe outputs):

- `report.md`
- `summary.json`
- `change_plan.md` (always)
- `change_plan.json` (when `--json`)
- `bundle.preview/` (generated docs preview files)
- `bundle.patch/` (patch-style diffs vs existing docs, best-effort)
- `bundle.hashes.json` (content hashes of preview files)

Governed outputs (only with `--apply` + `--write-docs`):

- files written under `--target-dir` (same relative names as `bundle.preview/`)

### Exit codes

- `0`: Generated successfully (preview or apply).
- `1`: Strict-mode blocking issue (e.g., missing required inputs, unsafe template).
- `2`: Usage/config error (unsafe paths, invalid output root, invalid target-dir, network gate violation).

---

## 8) Checks

Each check MUST emit a stable ID (`DOC-xxx`).

### Preflight safety

- **DOC-000 Preflight Safety**: validate path normalization + no symlink escape + `--out` safety.
- **DOC-001 Apply Gate**: apply requires `--apply` + `--write-docs` + valid `--target-dir`.
- **DOC-002 Network Gate**: URL schema fetch requires `--allow-network`.

### Content quality

- **DOC-101 Spec Parsable**: can extract needed doc sections.
- **DOC-102 Template Sanitized**: templates are parsed and sanitized; secrets removed/placeholdered.
- **DOC-103 Secret/PII Safety**: redaction applied; no secrets embedded in outputs.

### Preview/apply

- **DOC-201 Change Plan Present**: change plan lists all files with diff summary + hashes.
- **DOC-202 Atomic Writes**: apply uses atomic writes.
- **DOC-203 External Tool Policy**: diagram tools allowlisted, no-shell, timeout.
- **DOC-204 Reduced Coverage**: limits hit; reduced confidence.
- **DOC-206 Network Not Enforced**: environment cannot enforce network deny.

---

## 9) Interoperability with other workflows (alignment)

This workflow should integrate with the release/deploy chain as **evidence** and should not claim completion without verification.

Recommended evidence hooks (if your policy requires them):

- Strict verification summary:
  - `.spec/reports/verify-tasks-progress/<run-id>/summary.json`
- Deployment planner summary:
  - `.spec/reports/deployment-planner/<run-id>/summary.json`
- Test runner/analyzer summaries (optional):
  - `.spec/reports/test-suite-runner/<run-id>/summary.json`
  - `.spec/reports/test-report-analyzer/<run-id>/summary.json`

Docs generator output evidence:

- `.spec/reports/docs-generator/<run-id>/summary.json`

Deployment planner may reference this evidence in a deployment checklist.

---

## 10) Core logic

1) **Preflight**: validate flags, paths, network gate, and limits.
2) **Parse context**: read spec/tasks/registries (bounded).
3) **Generate preview bundle** based on `--mode`.
4) **Sanitize**: placeholder secrets/URLs; apply redaction policy.
5) **Create Change Plan**:
   - list target file paths
   - provide patch diffs if possible
   - otherwise provide excerpt + hash
6) **Apply (optional)**:
   - only when `--apply` + `--write-docs`
   - write files atomically under `--target-dir`
7) **Write report + summary**.

---

## 11) `summary.json` schema (minimum)

```json
{
  "workflow": "smartspec_docs_generator",
  "version": "6.1.1",
  "run_id": "string",
  "mode": "preview|apply",
  "status": "ok|warn|error",
  "scope": {
    "doc_mode": "api-docs|user-guide|architecture-diagram",
    "spec": "string",
    "target_dir": "string|null",
    "write_docs": false,
    "allow_network": false
  },
  "summary": {
    "files_previewed": 0,
    "files_to_write": 0,
    "redactions_applied": 0,
    "reduced_coverage": false
  },
  "checks": [
    {"check_id": "DOC-201", "status": "pass|warn|fail|na", "message": "string"}
  ],
  "writes": {
    "reports": [
      "path/to/report.md",
      "path/to/summary.json",
      "path/to/change_plan.md",
      "path/to/bundle.hashes.json"
    ],
    "governed": [
      "<target-dir>/..."
    ]
  }
}
```

---


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

### Flag usage notes

- **Config-first approach:** Prefer setting defaults in `.spec/smartspec.config.yaml` to minimize command-line flags
- **Positional arguments:** When supported, use positional arguments for primary inputs (e.g., spec path) instead of flags
- **Boolean flags:** Flags without values are boolean (presence = true, absence = false)
- **Path safety:** All path arguments must pass safety validation (no directory traversal, symlink escape, or absolute paths outside project)
- **Secret handling:** Never pass secrets as flag values; use `env:VAR_NAME` references or config file

# End of workflow doc
