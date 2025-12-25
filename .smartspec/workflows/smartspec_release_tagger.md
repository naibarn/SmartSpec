---
name: /smartspec_release_tagger
version: 6.1.1
role: release
write_guard: REPORTS-ONLY
purpose: Create a git tag and (optionally) a GitHub/GitLab release using evidence-first
  inputs. Preview-first; privileged operations require --apply and explicit network
  allow.
version_notes:
- v6.1.1: v6 hardening (path normalization + no symlink escape + output root safety
    + spec-id constraints); ban shell execution; strict validation for version/commit;
    remote verification is MUST; redaction + excerpt policy; aligns inputs/outputs
    with deployment_planner + verify/run/analyzer workflows.
description: Manage release tags and versioning.
workflow: /smartspec_release_tagger
---


# /smartspec_release_tagger (v6.1.1)

Create a release tag and optionally publish a release entry (GitHub/GitLab).

This is a **privileged** workflow:

- It executes allowlisted CLIs (`git`, `gh`, `glab`) in **no-shell** mode.
- It may require network access for remote verification and publishing.

It is **preview-first**:

- Default: produces a report describing exactly what would happen.
- With `--apply`: performs tagging and optional publishing.

Writes are **reports-only** under `.spec/reports/**`.

---

## 0) Governance contract

This workflow MUST follow:

- `knowledge_base_smartspec_handbook.md` (v6)
- `.spec/smartspec.config.yaml`

### 0.1 Write scopes (enforced)

Allowed writes (safe outputs only):

- Reports: `.spec/reports/release-tagger/**`

Forbidden writes (must hard-fail):

- Any path outside config `safety.allow_writes_only_under`
- Any path under config `safety.deny_writes_under`
- Any governed artifact (e.g., `specs/**`, `.spec/SPEC_INDEX.json`, `.spec/WORKFLOWS_INDEX.yaml`)

### 0.2 `--apply` behavior

- Without `--apply`: MUST NOT create tags, push tags, or publish releases.
- With `--apply`: MAY create/push/publish, but ONLY after all safety + evidence gates pass.

---

## 1) Threat model (minimum)

This workflow must defend against:

- Command injection via version/tag/paths.
- Publishing to the wrong remote.
- Unauthorized release (leaked credentials, wrong repo).
- Secret leakage in reports (tokens in env, CLIs, release notes).
- Path traversal / symlink escape when reading `--release-notes` or evidence summaries.

### 1.1 Hardening requirements (MANDATORY)

- **No shell execution:** MUST spawn processes without a shell (no `sh -c`, no string interpolation).
- **Allowlisted binaries only:** `git`, `gh`, `glab` (exact names) and ONLY for documented subcommands.
- **Path normalization (reads + writes):** reject traversal (`..`), absolute paths, and control characters.
- **No symlink escape (reads):** do not read through symlinks that resolve outside allowed scopes.
- **Output root safety (`--out`):** if provided, requested base output root MUST:
  - resolve under config allowlist
  - not fall under config denylist
  - hard-fail with `exit 2` if invalid
- **Redaction:** apply configured redaction patterns to all reports.
- **Excerpt policy:** never paste full release notes or full command output; include short excerpts only.
- **Timeouts:** enforce timeouts for every external command.
- **Network policy:** default deny; network may be used only when `--allow-network` is set.
  - If the runtime cannot enforce deny, the workflow MUST emit `RLT-206 Network Not Enforced`.

### 1.2 Identifier constraints (MANDATORY)

- `spec-id` (if used) MUST match: `^[a-z0-9_\-]{3,64}$`.
- `--version` MUST match a safe SemVer pattern (allow optional leading `v`):
  - `^v?(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$`
- `--commit-sha` MUST match: `^[0-9a-f]{7,40}$`.

The workflow MUST normalize the tag name to `v<major>.<minor>.<patch>...` (single canonical form) and record the normalization.

---

## 2) Interoperability with other workflows (consistency gates)

This workflow is designed to consume artifacts produced by the workflows you updated recently.

### 2.1 Evidence-first inputs (recommended)

Provide these inputs to ensure the tag reflects verified work:

- `--verify-summary` (preferred): strict task verification summary
  - Expected path convention: `.spec/reports/verify-tasks-progress/<run-id>/summary.json`
- `--deployment-summary` (recommended): deployment planner summary
  - Expected path convention: `.spec/reports/deployment-planner/<run-id>/summary.json`
- Optional quality gates (if your release policy requires them):
  - test runner: `.spec/reports/test-suite-runner/<run-id>/summary.json`
  - test analyzer: `.spec/reports/test-report-analyzer/<run-id>/summary.json`
  - perf verifier: `.spec/reports/nfr-perf-verifier/<run-id>/summary.json`

In `--mode=strict`, the workflow MUST block if required evidence is missing.

### 2.2 Release notes source (aligned with deployment_planner)

Preferred `--release-notes` inputs:

- Governed: `specs/<category>/<spec-id>/deployment/release_notes.md`
- Or preview output: `.spec/reports/deployment-planner/<run-id>/release_notes.preview.md`

The workflow MUST:

- read release notes as data
- avoid embedding full content in reports
- record only a short excerpt + content hash

---

## 3) Inputs

### 3.1 Required

- `--version <semver>`: Release version.
- `--commit-sha <sha>`: Commit to tag.

### 3.2 Optional

- `--spec-id <id>`: Used only for display + evidence mapping (must satisfy constraints).
- `--release-notes <path>`: Markdown file.
- `--remote <name>`: Default `origin`.
- `--provider <git-only|github|gitlab>`: Default `git-only`.
- `--allow-network`: Required to verify remote tags and publish releases.
- `--mode <normal|strict>`: Default `normal`.
- `--strict`: Alias for `--mode=strict`.

Evidence inputs (recommended):

- `--verify-summary <path>`
- `--deployment-summary <path>`
- `--test-runner-summary <path>`
- `--test-analyzer-summary <path>`
- `--perf-verifier-summary <path>`

---

## 4) Flags

### 4.1 Universal flags (must support)

- `--config <path>`
- `--lang <th|en>`
- `--platform <cli|kilo|ci|other>`
- `--apply`
- `--out <path>`
- `--json`
- `--quiet`

### 4.2 Workflow-specific flags

- `--version <semver>` (required)
- `--commit-sha <sha>` (required)
- `--spec-id <id>`
- `--release-notes <path>`
- `--remote <name>`
- `--provider <git-only|github|gitlab>`
- `--allow-network`
- `--mode <normal|strict>` / `--strict`
- `--verify-summary <path>`
- `--deployment-summary <path>`
- `--test-runner-summary <path>`
- `--test-analyzer-summary <path>`
- `--perf-verifier-summary <path>`

---

## 5) Invocation

### CLI (preview)

```bash
/smartspec_release_tagger \
  --version v1.2.3 \
  --commit-sha <sha> \
  --spec-id <spec-id> \
  --release-notes specs/<category>/<spec-id>/deployment/release_notes.md \
  --verify-summary .spec/reports/verify-tasks-progress/<run-id>/summary.json \
  --deployment-summary .spec/reports/deployment-planner/<run-id>/summary.json \
  --out .spec/reports/release-tagger \
  --json
```

### CLI (apply: create tag; optionally publish)

```bash
/smartspec_release_tagger \
  --version v1.2.3 \
  --commit-sha <sha> \
  --spec-id <spec-id> \
  --release-notes specs/<category>/<spec-id>/deployment/release_notes.md \
  --verify-summary .spec/reports/verify-tasks-progress/<run-id>/summary.json \
  --deployment-summary .spec/reports/deployment-planner/<run-id>/summary.json \
  --remote origin \
  --provider github \
  --allow-network \
  --apply \
  --out .spec/reports/release-tagger \
  --json
```

### Kilo Code

```bash
/smartspec_release_tagger.md \
  --version v1.2.3 \
  --commit-sha <sha> \
  --spec-id <spec-id> \
  --release-notes specs/<category>/<spec-id>/deployment/release_notes.md \
  --verify-summary .spec/reports/verify-tasks-progress/<run-id>/summary.json \
  --deployment-summary .spec/reports/deployment-planner/<run-id>/summary.json \
  --remote origin \
  --provider github \
  --allow-network \
  --apply \
  --out .spec/reports/release-tagger \
  --json \
  --platform kilo
```

---

## 6) Output structure

Outputs are written under a unique run folder.

- Default root: `.spec/reports/release-tagger/<run-id>/...`
- If `--out` is provided, it is treated as a requested base output root and MUST pass Output root safety validation; otherwise `exit 2`.

Artifacts:

- `report.md`
- `summary.json`

---

## 7) Remote verification (MANDATORY)

Before applying any changes, the workflow MUST:

- confirm the remote exists (`git remote get-url <remote>`)
- record the remote host (and in strict mode, verify against an allowlist from config if present)
- verify the commit exists and is a commit object (`git cat-file -e <sha>^{commit}`)
- verify the tag does not already exist locally or on the remote
  - remote check requires `--allow-network`

If remote checks cannot run (no network), the workflow MUST:

- in normal mode: warn and proceed only with **local tag creation** if configured to allow
- in strict mode: block (`exit 1`)

---

## 8) Checks

Each check MUST emit a stable ID (`RLT-xxx`).

### Preflight safety

- **RLT-000 Preflight Safety**: path normalization + no symlink escape + output root safety.
- **RLT-001 Inputs Valid**: version/sha/spec-id satisfy constraints and normalization.

### Evidence gates

- **RLT-101 Verify Evidence Present**:
  - strict: `--verify-summary` required
  - normal: if missing, mark release as "unverified" in report
- **RLT-102 Deployment Evidence Present**:
  - strict: `--deployment-summary` required
  - normal: warn if missing
- **RLT-103 Quality Gates Optional**: if gate summaries provided, record pass/fail/warn

### Remote & publish

- **RLT-201 Remote Verified**: remote URL verified; tag does not exist.
- **RLT-202 Network Policy**: network allowed only with `--allow-network` (or warn RLT-206).
- **RLT-203 Publish Provider Allowed**: provider is allowed and credentials are not leaked.

### Output hygiene

- **RLT-301 Redactions Applied**: report includes redaction counts only.
- **RLT-302 Release Notes Excerpt Only**: only excerpt + hash recorded.

### Exit codes

- `0`: Preview generated or apply completed.
- `1`: Strict-mode blocking issue (missing evidence, remote verification failed).
- `2`: Usage/config error (unsafe paths, invalid version/sha, disallowed output root).

---

## 9) Core logic

1) **Preflight** (RLT-000..001): validate identifiers, paths, and `--out` safety.
2) **Load evidence** (RLT-101..103): read summaries (bounded), validate their `workflow`/`run_id` fields.
3) **Read release notes** (optional): bounded read, redact, record excerpt + hash.
4) **Prepare plan**: compute planned `git` / `gh` / `glab` operations.
5) **Remote verification** (RLT-201): run local checks always; remote checks only with `--allow-network`.
6) **Preview report**: write `report.md` + `summary.json`.
7) **Apply** (only with `--apply`):
   - create annotated tag on the specified commit
   - push tag (requires `--allow-network`)
   - optionally publish a release entry (provider-specific; requires `--allow-network`)
8) **Finalize**: write final status and (if published) release URL.

---

## 10) `summary.json` schema (minimum)

```json
{
  "workflow": "smartspec_release_tagger",
  "version": "6.1.1",
  "run_id": "string",
  "mode": "preview|apply",
  "status": "ok|warn|error",
  "scope": {
    "spec_id": "string|null",
    "version": "string",
    "tag": "string",
    "commit_sha": "string",
    "remote": "string",
    "provider": "git-only|github|gitlab",
    "allow_network": false
  },
  "evidence": {
    "verify_summary": "string|null",
    "deployment_summary": "string|null",
    "test_runner_summary": "string|null",
    "test_analyzer_summary": "string|null",
    "perf_verifier_summary": "string|null"
  },
  "results": {
    "remote_verified": false,
    "tag_created": false,
    "tag_pushed": false,
    "release_published": false,
    "release_url": "string|null"
  },
  "warnings": [
    {"check_id": "RLT-206", "message": "string"}
  ],
  "writes": {"reports": ["path/to/report.md", "path/to/summary.json"]}
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

