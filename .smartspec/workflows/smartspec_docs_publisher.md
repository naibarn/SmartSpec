---
name: /smartspec_docs_publisher
version: 6.1.1
role: documentation/publishing
write_guard: REPORTS-ONLY
purpose: Publish documentation produced by docs_generator to GitHub Pages or Read
  the Docs using a safe, preview-first, no-shell, allowlisted approach. Writes reports
  only; uses a temporary workspace under the run folder.
version_notes:
- v6.1.1: Fixes universal flag collision by renaming workflow-specific platform flag;
    adds v6 hardening (path normalization + no symlink escape + output root safety);
    introduces explicit --allow-network gate and enforcement check; replaces "no local
    writes" contradiction with approved temp workspace under run folder; removes webhook
    URL flag in favor of env secret ref; bans shell execution and allowlists commands
    with timeouts; aligns integration with docs_generator v6.1.1 and release/deploy
    workflow evidence hooks.
description: Publish documentation to various platforms.
workflow: /smartspec_docs_publisher
---


# /smartspec_docs_publisher (v6.1.1)

Publish documentation to a hosting platform.

Supported publish platforms:

- GitHub Pages (via `gh-pages` branch)
- Read the Docs (via webhook trigger)

This workflow is **privileged** (may use network + VCS operations).

It is **preview-first**:

- Without `--apply`: generates a publish plan and the exact operations it would perform.
- With `--apply`: executes the plan after passing safety gates.

It is **reports-only**:

- Writes only under `.spec/reports/docs-publisher/**`.
- Any required workspace for clone/copy operations must live under the run folder.

---

## 0) Governance contract

This workflow MUST follow:

- `knowledge_base_smartspec_handbook.md` (v6)
- `.spec/smartspec.config.yaml`

### 0.1 Write scopes (enforced)

Allowed writes (safe outputs only):

- Reports: `.spec/reports/docs-publisher/**`

Allowed temporary workspace (safe output):

- `.spec/reports/docs-publisher/<run-id>/workspace/**`

Forbidden writes (must hard-fail):

- Any path outside config `safety.allow_writes_only_under`
- Any path under config `safety.deny_writes_under`
- Any governed artifact (e.g., `specs/**`, `.spec/SPEC_INDEX.json`, `.spec/WORKFLOWS_INDEX.yaml`)
- Any runtime source tree modifications

### 0.2 `--apply` behavior

- Without `--apply`: MUST NOT push branches, trigger webhooks, or publish.
- With `--apply`: MAY publish only after safety and network gates pass.

---

## 1) Threat model (minimum)

This workflow must defend against:

- command injection via branch names/paths/versions
- publishing to the wrong repository or branch
- secret leakage (tokens, webhook secrets) into reports or command logs
- path traversal / symlink escape on docs-dir or output roots
- destructive branch operations (wiping branch content)

---

## 2) Security hardening (MANDATORY)

### 2.1 Execution policy

- **No shell execution:** MUST spawn processes without a shell (no `sh -c`, no string interpolation).
- **Allowlisted binaries only:** `git` (exact name) only.
  - For Read the Docs, webhook trigger is performed via a built-in HTTP client library (not shelling out to `curl`).
- **Timeouts:** enforce timeouts for every external operation.

### 2.2 Network policy

- Default network access MUST be denied.
- Publishing requires explicit `--allow-network`.
- If the runtime cannot enforce deny, the workflow MUST emit `DPU-206 Network Not Enforced`.

### 2.3 Path safety

- **Path normalization (reads + writes):** reject traversal (`..`), absolute paths, and control characters.
- **No symlink escape (reads + writes):** realpath MUST remain within allowed scopes.
- **Output root safety (`--out`):** requested base output root MUST pass allow/deny validation; else `exit 2`.

### 2.4 Redaction and excerpt policy

- Apply configured redaction patterns to all captured output.
- Never print tokens, webhook secrets, or full webhook URLs containing secrets.
- Include only short excerpts of publish logs.

---

## 3) Flags (fixing the v6.1.0 collision)

> **Important:** Universal `--platform` remains reserved for runtime mode (`cli|kilo|ci|other`).
> The publish target is now **`--publish-platform`**.

### 3.1 Universal flags (must support)

- `--config <path>`
- `--lang <th|en>`
- `--platform <cli|kilo|ci|other>`
- `--apply`
- `--out <path>`
- `--json`
- `--quiet`

### 3.2 Workflow-specific flags

- `--docs-dir <path>` (required): directory containing built docs to publish.
- `--publish-platform <github-pages|readthedocs>` (required)
- `--version <semver>` (required): docs version label.
- `--allow-network` (required to publish)

GitHub Pages options:

- `--remote <name>` (default `origin`)
- `--github-branch <name>` (default `gh-pages`)
- `--publish-subdir <path>` (default `.`; optional)

Read the Docs options:

- `--rtd-webhook-secret-ref <env:NAME>` (required)
- `--rtd-project-slug <slug>` (required)

Mode:

- `--mode <normal|strict>` / `--strict`

---

## 4) Identifier constraints (MANDATORY)

- `--version` MUST match safe SemVer (allow optional leading `v`):
  - `^v?(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$`
- `--remote` MUST match: `^[A-Za-z0-9._\-]{1,64}$`
- `--github-branch` MUST match: `^[A-Za-z0-9._/\-]{1,128}$`
- `--rtd-project-slug` MUST match: `^[a-z0-9\-]{2,64}$`

---

## 5) Inputs and validation (MANDATORY)

### 5.1 `--docs-dir` validation

`--docs-dir` MUST:

- exist and be a directory
- pass path normalization and no symlink escape
- be contained within the project root
- contain at least one of:
  - `index.html`
  - `mkdocs.yml`
  - `sitemap.xml`
  - `README.md`

### 5.2 Docs provenance (alignment with docs_generator)

Recommended: point `--docs-dir` to output of `smartspec_docs_generator`:

- preview bundle: `.spec/reports/docs-generator/<run-id>/bundle.preview/`
- or governed docs directory after `docs_generator --apply --write-docs`

In `--mode=strict`, the workflow SHOULD require a `bundle.hashes.json` nearby or a `docs_generator` summary reference to ensure provenance.

### 5.3 Apply + network gate

- Publishing MUST require `--apply` and `--allow-network`.
- If missing:
  - preview-only mode continues and reports what would have been done.
  - apply mode hard-fails (`exit 2`).

### 5.4 Remote verification (GitHub Pages)

In apply mode, before any destructive operations, MUST:

- resolve `git remote get-url <remote>` and record it
- (strict) verify remote host against allowlist from config if available
- ensure the target branch name is not the main branch

---

## 6) Preview-first outputs

All runs produce a unique run folder.

- Default root: `.spec/reports/docs-publisher/<run-id>/...`

Artifacts:

- `report.md`
- `summary.json`
- `publish_plan.md` (always)
- `change_plan.md` (always; lists operations + files + hashes)
- `workspace/` (temp clone/worktree, only if needed)

---

## 7) Publish strategies

### 7.1 GitHub Pages (gh-pages branch)

**Workspace:** Use a temporary clone or worktree under `workspace/`.

Plan steps (apply mode):

1) Verify remote and branch safety.
2) Fetch remote branch.
3) Check out/create the publish branch in workspace.
4) Replace content under a controlled subdirectory (default root).
   - MUST NOT delete outside the publish subtree.
5) Commit with a standardized message including version.
6) Push to remote publish branch.

> Safety guard: never run `rm -rf` at repo root; only remove files under the publish subtree.

### 7.2 Read the Docs

**No git required** (preferred): trigger a webhook.

- The webhook secret MUST be provided by `--rtd-webhook-secret-ref env:NAME`.
- The workflow MUST NOT accept raw webhook URL as a flag.
- The workflow MUST redact any URLs in reports.

---

## 8) Checks

Each check MUST emit a stable ID (`DPU-xxx`).

### Preflight safety

- **DPU-000 Preflight Safety**: path normalization + no symlink escape + output root safety.
- **DPU-001 Flag Contract**: reject workflow-specific `--platform`; must use `--publish-platform`.
- **DPU-002 Apply Gate**: publishing requires `--apply`.
- **DPU-003 Network Gate**: publishing requires `--allow-network`.

### Content/provenance

- **DPU-101 Docs Dir Valid**: docs-dir exists and passes safety checks.
- **DPU-102 Provenance Present**: docs-generator evidence present (strict blocks if required).

### Remote/publish safety

- **DPU-201 Remote Verified**: remote URL recorded and validated.
- **DPU-202 Branch Safety**: branch is not main, and publish subtree is controlled.
- **DPU-206 Network Not Enforced**: environment cannot enforce deny.

### Output hygiene

- **DPU-301 Redactions Applied**: report includes redaction counts only.

### Exit codes

- `0`: Preview generated or publish completed.
- `1`: Strict-mode blocking issue.
- `2`: Usage/config error (unsafe paths, missing gates, invalid identifiers).

---

## 9) Invocation

### CLI (preview)

```bash
/smartspec_docs_publisher \
  --docs-dir .spec/reports/docs-generator/<run-id>/bundle.preview \
  --publish-platform github-pages \
  --version v1.2.3 \
  --remote origin \
  --github-branch gh-pages \
  --out .spec/reports/docs-publisher \
  --json
```

### CLI (apply: GitHub Pages)

```bash
/smartspec_docs_publisher \
  --docs-dir .spec/reports/docs-generator/<run-id>/bundle.preview \
  --publish-platform github-pages \
  --version v1.2.3 \
  --remote origin \
  --github-branch gh-pages \
  --allow-network \
  --apply \
  --out .spec/reports/docs-publisher \
  --json
```

### CLI (apply: Read the Docs)

```bash
/smartspec_docs_publisher \
  --docs-dir .spec/reports/docs-generator/<run-id>/bundle.preview \
  --publish-platform readthedocs \
  --version v1.2.3 \
  --rtd-project-slug my-project \
  --rtd-webhook-secret-ref env:RTD_WEBHOOK_SECRET \
  --allow-network \
  --apply \
  --out .spec/reports/docs-publisher \
  --json
```

### Kilo Code

```bash
/smartspec_docs_publisher.md \
  --docs-dir .spec/reports/docs-generator/<run-id>/bundle.preview \
  --publish-platform github-pages \
  --version v1.2.3 \
  --remote origin \
  --github-branch gh-pages \
  --allow-network \
  --apply \
  --out .spec/reports/docs-publisher \
  --json \
  --platform kilo
```

---

## 10) `summary.json` schema (minimum)

```json
{
  "workflow": "smartspec_docs_publisher",
  "version": "6.1.1",
  "run_id": "string",
  "mode": "preview|apply",
  "status": "ok|warn|error",
  "scope": {
    "docs_dir": "string",
    "publish_platform": "github-pages|readthedocs",
    "version": "string",
    "remote": "string|null",
    "github_branch": "string|null",
    "allow_network": false
  },
  "results": {
    "published": false,
    "publish_url": "string|null"
  },
  "warnings": [
    {"check_id": "DPU-206", "message": "string"}
  ],
  "writes": {
    "reports": [
      "path/to/report.md",
      "path/to/summary.json",
      "path/to/publish_plan.md",
      "path/to/change_plan.md"
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

