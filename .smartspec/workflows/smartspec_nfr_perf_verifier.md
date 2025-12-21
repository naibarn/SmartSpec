---
name: /smartspec_nfr_perf_verifier
version: 6.1.1
role: verify
write_guard: REPORTS-ONLY
purpose: Verify NFR performance/reliability compliance using existing evidence artifacts
  (perf reports, metrics exports, logs). Does not run tests. Outputs verifier reports
  only.
version_notes:
- v6.1.1: Align with SmartSpec v6 governance; resolve NO-WRITE/output mismatch; mandatory
    hardening (path safety + symlink escape); deterministic evidence selection; evidence
    trust rules; redaction + excerpt policy; universal flags.
description: Verify NFR/performance evidence (reports).
workflow: /smartspec_nfr_perf_verifier
---


# /smartspec_nfr_perf_verifier (v6.1.1)

Verifier workflow that evaluates whether declared **performance / reliability NFRs** are **MET / NOT_MET / UNKNOWN** based on **existing evidence**.

- **Does not** run performance tests.
- **Does not** connect to production systems.
- **Does not** modify specs/tasks/registries/CI/code.
- **Writes reports only** under `.spec/reports/**`.

---

## 0) Governance contract

This workflow MUST follow:

- `knowledge_base_smartspec_handbook.md` (v6)
- `.spec/smartspec.config.yaml`

### 0.1 Write scopes (enforced)

Allowed writes (safe outputs only):

- Reports: `.spec/reports/nfr-perf-verifier/**`

Forbidden writes (must hard-fail):

- Any path outside config `safety.allow_writes_only_under`
- Any path under config `safety.deny_writes_under`
- Any governed artifact (e.g., `specs/**`, `.spec/SPEC_INDEX.json`, `.spec/WORKFLOWS_INDEX.yaml`)
- Any runtime source tree modifications

### 0.2 `--apply` behavior (universal flag)

- Accepted for compatibility with the universal flag contract.
- Must have **no effect** on write scopes.
- If provided, the report header MUST note that `--apply` was ignored.

---

## 1) Threat model (minimum)

This workflow must defend against:

- Path traversal / symlink escape when reading evidence or writing reports.
- Secret/PII leakage into reports from logs/metrics.
- Spoofed or untrusted evidence files being treated as authoritative.
- Wrong-environment / wrong-time-window evidence being selected.
- Unbounded scans / CI cost spikes from broad globs.
- Accidental network usage.

### 1.1 Hardening requirements (MANDATORY)

- **No network access:** respect config `safety.network_policy.default=deny`.
- **No shell execution:** do not run arbitrary commands from inputs.
- **Path normalization (reads + writes):** reject traversal (`..`), absolute paths, and control characters on any user-supplied path.
- **No symlink escape (reads + writes):** do not read/write through symlinks that resolve outside allowed scopes.
- **Read scope enforcement:** reads MUST stay within project root or configured workspace roots.
- **Timeouts & limits:** respect config `safety.content_limits` and bound scan scope.
- **Redaction:** respect config `safety.redaction` (patterns + secret file globs); never embed secrets in outputs.
- **Excerpt policy:** do not paste large raw logs/metrics; include minimal snippets and prefer structured summaries.
- **Output collision:** respect config `safety.output_collision` (never overwrite existing run folders).
- **Output root safety (`--out`):** if provided, it is a requested base output root and MUST:
  - resolve under config `safety.allow_writes_only_under`
  - not fall under config `safety.deny_writes_under`
  - not be a runtime source folder
  - hard-fail with usage/config error (`exit 2`) if invalid

---

## 2) Inputs

### 2.1 Primary input (positional-first)

- `spec_md` (required): `specs/<category>/<spec-id>/spec.md`

### 2.2 Evidence sources (read-only)

Evidence can be supplied explicitly or discovered from known report locations.

**Explicit (preferred for CI determinism):**

- `--evidence-manifest <path>`: JSON manifest describing evidence files + metadata.

**Direct globs (fallback):**

- `--perf-report-paths <glob[,glob...]>`
- `--metrics-export-paths <glob[,glob...]>`
- `--log-paths <glob[,glob...]>`
- `--nfr-policy-paths <glob[,glob...]>`

**Known report roots (optional discovery):**

- `.spec/reports/nfr-perf-planner/**/plan.json` (planner output)
- `.spec/reports/**` (other tool outputs)

### 2.3 Multi-repo wiring (optional)

Configuration-first wiring:

- `--repos-config <path>` (preferred)
- `--workspace-roots <csv>` (fallback)
- `--registry-roots <csv>` (supplemental registries; read-only)
- `--index <path>` (SPEC_INDEX override; read-only)

---

## 3) Input validation (MANDATORY)

- `spec_md` MUST exist and be a file.
- All provided paths and expanded glob matches MUST:
  - resolve within project root or allowed workspace roots
  - be rejected if they escape via symlink
  - be rejected if they contain traversal (`..`), are absolute, or contain control characters
- If `--evidence-manifest` is provided:
  - it MUST be valid JSON
  - it MUST list evidence entries with `path` + `type` + `env` + `generated_at` (minimum)
  - all evidence paths listed MUST pass the same read-scope validation
- If evidence globs are provided:
  - each glob MUST match at least 1 file (else `exit 2`)
- If no evidence is provided and discovery finds none:
  - in normal mode: status becomes `UNKNOWN` with `NFRV-204 Reduced Evidence`
  - in strict mode: hard-fail (`exit 1`) because verifier cannot evaluate requirements

---

## 4) Evidence trust rules (MANDATORY)

Evidence is trusted only if all conditions below hold:

1) **Location trust**
- Evidence MUST reside under:
  - project root, OR
  - configured workspace roots

2) **Metadata minimum**
- Evidence MUST have at least:
  - `env` (e.g., `dev|staging|prod|other`)
  - `generated_at` (ISO 8601 recommended)
  - `tool` or `source` identifier

3) **Environment match**
- If `--target-env` is provided, evidence `env` MUST match or map to it.
- Otherwise, evidence MUST declare `env`, and the verifier MUST report which envs were evaluated.

4) **Time window match**
- If `--time-window` is provided, evidence `generated_at` MUST fall within the window.
- Evidence outside the window MUST NOT be used for MET decisions (it may be listed as discarded).

If any rule fails, evidence MUST be treated as **untrusted** and excluded from MET decisions.

---

## 5) Deterministic evidence selection (MANDATORY)

When multiple candidate evidence files match:

- Prefer entries from `--evidence-manifest` over globs.
- Prefer files with complete metadata over incomplete.
- Select the latest deterministically:
  - sort by `generated_at` (descending), then by path (lexicographic)
  - choose the first matching candidate per `(type, env)` bucket

The report MUST record:

- selected evidence
- discarded candidates and why (wrong env/window, missing metadata, untrusted path)

---

## 6) Flags

### 6.1 Universal flags (must support)

- `--config <path>`
- `--lang <th|en>`
- `--platform <cli|kilo|ci|other>`
- `--apply` (ignored)
- `--out <path>`
- `--json`
- `--quiet`

### 6.2 Workflow-specific flags

- `--evidence-manifest <path>`: Preferred deterministic evidence input.
- `--perf-report-paths <glob[,glob...]>`
- `--metrics-export-paths <glob[,glob...]>`
- `--log-paths <glob[,glob...]>`
- `--nfr-policy-paths <glob[,glob...]>`
- `--target-env <dev|staging|prod|other>`
- `--time-window <7d|30d|90d|iso_start..iso_end>`
- `--mode <normal|strict>`: default `normal`.
- `--strict`: alias for `--mode=strict`.
- `--report-format <md|json|both>`: default `md`.
- `--stdout-summary`: Print a short summary to stdout (still writes reports).
- `--max-evidence-files <int>`: Cap evidence files scanned per type (bounded scanning).

---

## 7) Invocation

### CLI

```bash
/smartspec_nfr_perf_verifier \
  specs/<category>/<spec-id>/spec.md \
  [--evidence-manifest .spec/reports/nfr-evidence/<run-id>/evidence.json] \
  [--target-env prod] \
  [--time-window 30d] \
  [--mode strict] \
  [--report-format both] \
  [--stdout-summary] \
  [--out <output-root>] \
  [--json]
```

### Kilo Code

```bash
/smartspec_nfr_perf_verifier.md \
  specs/<category>/<spec-id>/spec.md \
  [--evidence-manifest .spec/reports/nfr-evidence/<run-id>/evidence.json] \
  [--target-env prod] \
  [--time-window 30d] \
  [--mode strict] \
  [--report-format both] \
  [--stdout-summary] \
  [--out <output-root>] \
  [--json] \
  --platform kilo
```

---

## 8) Outputs

Default report directory:

```
.spec/reports/nfr-perf-verifier/<run-id>/
```

Artifacts:

- `report.md` (default)
- `report.json` (when `--report-format=json|both`)
- `summary.json` (always)

---

## 9) NFR extraction (inputs)

NFR sources:

- `spec.md` sections: NFR, SLA, SLO, Performance, Reliability, UX Performance
- NFR policy files (from `--nfr-policy-paths`)
- `.spec/SPEC_INDEX.json` (references)
- registries (SLO registry when present)

Each extracted NFR MUST be normalized to:

```json
{
  "id": "NFR-...",
  "category": "latency|throughput|error_rate|availability|ux|reliability|other",
  "threshold": "string",
  "environment": "dev|staging|prod|other",
  "criticality": "low|medium|high",
  "source_path": "string"
}
```

If an NFR has no ID, the workflow MUST synthesize a stable derived ID and record derivation in the report.

---

## 10) Evaluation model

For each NFR, compute:

- `status`: `MET | NOT_MET | UNKNOWN`
- `confidence`: `high | medium | low`
- `evidence_used`: list of evidence items selected
- `why`: short rationale

Rules:

- **MET** requires trusted evidence that matches `env` + `time-window` and supports the threshold.
- **NOT_MET** requires trusted evidence that contradicts the threshold.
- **UNKNOWN** when evidence is missing, untrusted, or insufficient.

In strict mode:

- Any `UNKNOWN` for `criticality=high` MUST cause overall `status=fail`.

---

## 11) Checks

Each check MUST emit a stable ID (`NFRV-xxx`).

### Preflight safety checks (always enforced)

- **NFRV-000 Preflight Safety**: Validate `--out`, all paths, glob expansions, read/write constraints (path normalization + no symlink escape), and limits. Fail with `exit 2` on violation.

### MUST checks

- **NFRV-101 Inputs Parsable**: Spec/policies parse enough to extract NFRs.
- **NFRV-102 Evidence Parsable**: Evidence inputs parse enough to extract metrics.
- **NFRV-103 Evidence Trusted**: Evidence used for decisions passes trust rules (location + metadata + env/window match).

### SHOULD checks (warnings)

- **NFRV-201 Coverage Gaps**: NFRs with no matching evidence → `UNKNOWN`.
- **NFRV-202 Wrong Env Evidence**: Evidence exists but env mismatch.
- **NFRV-203 Outside Time Window**: Evidence exists but outside the requested window.
- **NFRV-204 Reduced Evidence**: Limits reached or evidence too large; reduced confidence.
- **NFRV-205 Redactions Applied**: Redactions performed; report includes count only.

### Exit codes

- `0`: Verification complete; no strict blocking issues.
- `1`: Strict blocking issue (e.g., critical NFR is NOT_MET or UNKNOWN), or overall status fail.
- `2`: Usage/config error (unsafe paths, invalid globs/manifest, disallowed output root).

---

## 12) `report.md` required content

The report MUST include:

1. **Header**: spec-id, run-id, mode, target env/window, and whether `--apply` was ignored.
2. **Evidence selection log**: selected vs discarded candidates + reasons.
3. **NFR results table**: NFR ID, threshold, status, confidence, evidence refs.
4. **Release risk**: summary highlighting critical gaps.
5. **Redaction note**: what was redacted (pattern IDs only), counts, no raw secrets.

---

## 13) `summary.json` schema (minimum)

```json
{
  "workflow": "smartspec_nfr_perf_verifier",
  "version": "6.1.1",
  "run_id": "string",
  "status": "pass|fail|warn",
  "mode": "normal|strict",
  "scope": {
    "spec_path": "string",
    "target_env": "string|null",
    "time_window": "string|null"
  },
  "summary": {
    "nfr_count": 0,
    "met": 0,
    "not_met": 0,
    "unknown": 0,
    "reduced_evidence": false
  },
  "warnings": [
    {"check_id": "NFRV-204", "message": "string"}
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

