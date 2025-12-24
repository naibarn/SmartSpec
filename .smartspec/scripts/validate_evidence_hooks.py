#!/usr/bin/env python3
"""validate_evidence_hooks.py (v7.0.0)

Strict validator for SmartSpec evidence hooks inside a tasks.md file.

Evidence hook (canonical):
  evidence: <type> key=value key=value ...

Supported strict types:
  - code
  - test
  - docs
  - ui

Key rules:
  - No stray tokens (every token after <type> MUST be key=value)
  - path= is REQUIRED for all strict types
  - Values with spaces MUST be quoted (double quotes recommended)
  - Only a limited set of keys are allowed per type (see ALLOWED_KEYS)
  - Disallow dangerous/ambiguous paths (absolute, traversal, glob)

Outputs:
  - Always prints a human-readable report to stdout.
  - Optionally writes report files under --out.

This tool does NOT execute commands. It only validates formatting and safety.
"""

from __future__ import annotations

import argparse
import json
import re
import shlex
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple


STRICT_TYPES = {"code", "test", "docs", "ui"}

ALLOWED_KEYS: Dict[str, set[str]] = {
    "code": {"path", "symbol", "contains", "regex"},
    "test": {"path", "command", "contains", "regex"},
    "docs": {"path", "heading", "contains", "regex"},
    "ui": {"path", "selector", "contains", "regex"},
}

# Keys that count as a "matcher" (presence reduces false-negatives).
MATCHER_KEYS = {"contains", "symbol", "heading", "selector", "regex", "command"}

# Treat these command-like prefixes as suspicious if used as path= values.
SUSPICIOUS_PATH_PREFIXES = {
    "npm",
    "pnpm",
    "yarn",
    "bun",
    "npx",
    "node",
    "python",
    "python3",
    "pip",
    "pip3",
    "docker",
    "docker-compose",
    "compose",
    "make",
    "pytest",
    "go",
    "cargo",
    "mvn",
    "gradle",
    "java",
    "dotnet",
    "swagger-cli",
}

RE_EVIDENCE_LINE = re.compile(r"^\s*evidence:\s+(?P<payload>.*)$", re.IGNORECASE)


@dataclass
class HookIssue:
    code: str
    message: str


@dataclass
class HookFinding:
    line: int
    raw: str
    issues: List[HookIssue]


@dataclass
class Report:
    file: str
    total_hooks: int
    valid_hooks: int
    invalid_hooks: int
    validity: float
    hooks_with_warnings: int
    invalid: List[HookFinding]
    warnings: List[HookFinding]


def _is_absolute_or_traversal(p: str) -> bool:
    p = p.strip().replace("\\", "/")
    if p.startswith("/"):
        return True
    if re.match(r"^[A-Za-z]:/", p):
        return True
    if p == ".." or p.startswith("../") or "/../" in p:
        return True
    return False


def _contains_glob(p: str) -> bool:
    return any(ch in p for ch in ["*", "?", "[", "]"])


def _parse_payload(payload: str) -> Tuple[Optional[str], Dict[str, str], List[HookIssue]]:
    issues: List[HookIssue] = []

    try:
        tokens = shlex.split(payload, posix=True)
    except Exception as e:
        return None, {}, [HookIssue("shlex_error", f"Unable to parse evidence payload: {e}")]

    if not tokens:
        return None, {}, [HookIssue("empty_payload", "Evidence payload is empty")]

    hook_type = tokens[0].strip().lower()
    if hook_type not in STRICT_TYPES:
        issues.append(HookIssue("invalid_type", f"Unsupported evidence type '{tokens[0]}'. Allowed: {sorted(STRICT_TYPES)}"))

    kv: Dict[str, str] = {}
    for t in tokens[1:]:
        if "=" not in t:
            issues.append(
                HookIssue(
                    "stray_token",
                    f"Stray token not allowed (quote values with spaces). Token: '{t}'",
                )
            )
            continue
        k, v = t.split("=", 1)
        k = k.strip()
        v = v.strip()
        if not k:
            issues.append(HookIssue("bad_key", f"Empty key in token '{t}'"))
            continue
        if k in kv:
            issues.append(HookIssue("dup_key", f"Duplicate key '{k}'"))
            continue
        kv[k] = v

    return hook_type, kv, issues


def _validate_hook(hook_type: Optional[str], kv: Dict[str, str]) -> Tuple[List[HookIssue], List[HookIssue]]:
    """Return (errors, warnings)."""
    errors: List[HookIssue] = []
    warnings: List[HookIssue] = []

    ht = (hook_type or "").lower()

    # Type validation
    if ht not in STRICT_TYPES:
        errors.append(HookIssue("invalid_type", "Evidence type must be one of code|test|docs|ui"))
        return errors, warnings

    # Key allowlist
    allowed = ALLOWED_KEYS[ht]
    for k in kv.keys():
        if k not in allowed:
            errors.append(HookIssue("bad_key", f"Key '{k}' not allowed for type '{ht}'. Allowed: {sorted(allowed)}"))

    # Required path
    if "path" not in kv or not kv.get("path", "").strip():
        errors.append(HookIssue("missing_path", "Missing required key: path=<repo-relative-path>"))
        return errors, warnings

    path_val = kv["path"].strip().strip('"')

    # Path safety
    if _is_absolute_or_traversal(path_val):
        errors.append(HookIssue("unsafe_path", f"Path must be repo-relative and must not traverse: path={kv['path']}"))

    if _contains_glob(path_val):
        errors.append(HookIssue("glob_path", f"Glob patterns are not allowed in path=: {kv['path']}"))

    # Disallow command-like prefixes as path= (common mistake)
    first = path_val.split("/", 1)[0].strip().lower()
    if first in SUSPICIOUS_PATH_PREFIXES:
        errors.append(
            HookIssue(
                "suspicious_path",
                f"path= looks like a command prefix ('{first}'). For commands use: evidence: test path=<anchor> command=\"...\"",
            )
        )

    # docs vs code mismatch: heading should be docs-only (already enforced by allowlist)

    # Warning: no matcher key
    if not any(k in kv for k in MATCHER_KEYS):
        warnings.append(
            HookIssue(
                "no_matcher",
                "No matcher key (contains/symbol/heading/selector/regex/command). Allowed, but may cause false-negatives if the file moves or content changes.",
            )
        )

    # Warning: directory-like path
    if path_val.endswith("/"):
        warnings.append(
            HookIssue(
                "dir_path",
                "path= ends with '/'. Evidence against directories is allowed but often weak; prefer a concrete file.",
            )
        )

    return errors, warnings


def validate_file(tasks_path: Path) -> Report:
    text = tasks_path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()

    invalid: List[HookFinding] = []
    warnings: List[HookFinding] = []

    total = 0
    for i, line in enumerate(lines, start=1):
        m = RE_EVIDENCE_LINE.match(line)
        if not m:
            continue
        total += 1
        payload = m.group("payload").strip()

        hook_type, kv, parse_issues = _parse_payload(payload)
        errors, warns = _validate_hook(hook_type, kv) if not parse_issues else ([], [])

        all_errors = [*parse_issues, *errors]
        if all_errors:
            invalid.append(HookFinding(i, line.rstrip("\n"), all_errors))
            continue

        if warns:
            warnings.append(HookFinding(i, line.rstrip("\n"), warns))

    valid = total - len(invalid)
    validity = (valid / total * 100.0) if total else 100.0

    return Report(
        file=str(tasks_path),
        total_hooks=total,
        valid_hooks=valid,
        invalid_hooks=len(invalid),
        validity=validity,
        hooks_with_warnings=len(warnings),
        invalid=invalid,
        warnings=warnings,
    )


def _render_report_text(r: Report, max_items: int = 400) -> str:
    out: List[str] = []
    out.append("=" * 60)
    out.append("EVIDENCE HOOK VALIDATION REPORT")
    out.append("=" * 60)
    out.append(f"File: {r.file}")
    out.append("")
    out.append("Summary:")
    out.append(f"  Total evidence hooks: {r.total_hooks}")
    out.append(f"  Valid hooks: {r.valid_hooks}")
    out.append(f"  Invalid hooks: {r.invalid_hooks}")
    out.append(f"  Validity: {r.validity:.1f}%")
    out.append(f"  Hooks with warnings: {r.hooks_with_warnings}")

    if r.invalid:
        out.append("")
        out.append("=" * 60)
        out.append(f"INVALID EVIDENCE HOOKS ({len(r.invalid)}):")
        out.append("=" * 60)
        for f in r.invalid[:max_items]:
            out.append("")
            out.append(f"Line {f.line}:")
            out.append(f"  Content: {f.raw.strip()}")
            out.append("  Issues:")
            for iss in f.issues:
                out.append(f"    - {iss.message}")
        if len(r.invalid) > max_items:
            out.append("")
            out.append(f"... truncated ({len(r.invalid) - max_items} more invalid hooks)")

    if r.warnings:
        out.append("")
        out.append("=" * 60)
        out.append(f"WARNINGS ({len(r.warnings)} hooks):")
        out.append("=" * 60)
        for f in r.warnings[:max_items]:
            out.append("")
            out.append(f"Line {f.line}:")
            out.append(f"  Content: {f.raw.strip()}")
            out.append("  Warnings:")
            for iss in f.issues:
                out.append(f"    - {iss.message}")
        if len(r.warnings) > max_items:
            out.append("")
            out.append(f"... truncated ({len(r.warnings) - max_items} more warnings)")

    out.append("")
    return "\n".join(out)


def _write_outputs(report: Report, out_dir: Path, report_format: str) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    if report_format in {"md", "both"}:
        # Use fenced blocks for machine-like sections inside Markdown
        md = []
        md.append("# Evidence Hook Validation Report\n")
        md.append(f"- File: `{report.file}`\n")
        md.append(f"- Total: **{report.total_hooks}**\n")
        md.append(f"- Valid: **{report.valid_hooks}**\n")
        md.append(f"- Invalid: **{report.invalid_hooks}**\n")
        md.append(f"- Validity: **{report.validity:.1f}%**\n")
        md.append(f"- Hooks with warnings: **{report.hooks_with_warnings}**\n")

        if report.invalid:
            md.append("\n## Invalid hooks\n")
            for f in report.invalid:
                md.append(f"- Line {f.line}: `{f.raw.strip()}`\n")
                for iss in f.issues:
                    md.append(f"  - {iss.code}: {iss.message}\n")

        if report.warnings:
            md.append("\n## Warnings\n")
            for f in report.warnings:
                md.append(f"- Line {f.line}: `{f.raw.strip()}`\n")
                for iss in f.issues:
                    md.append(f"  - {iss.code}: {iss.message}\n")

        (out_dir / "verification-report.md").write_text("".join(md), encoding="utf-8")

    if report_format in {"json", "both"}:
        # Convert dataclasses to JSON-serializable structures
        def finding_to_dict(f: HookFinding) -> dict:
            return {
                "line": f.line,
                "raw": f.raw,
                "issues": [asdict(i) for i in f.issues],
            }

        payload = {
            "file": report.file,
            "summary": {
                "total_hooks": report.total_hooks,
                "valid_hooks": report.valid_hooks,
                "invalid_hooks": report.invalid_hooks,
                "validity": report.validity,
                "hooks_with_warnings": report.hooks_with_warnings,
            },
            "invalid": [finding_to_dict(x) for x in report.invalid],
            "warnings": [finding_to_dict(x) for x in report.warnings],
        }
        (out_dir / "verification-report.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _parse_args(argv: Sequence[str]) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Validate canonical SmartSpec evidence hooks in a tasks.md file")

    # Compatibility: accept either positional or --tasks.
    ap.add_argument("tasks", nargs="?", help="Path to tasks.md (positional)")
    ap.add_argument("--tasks", dest="tasks_flag", help="Path to tasks.md")

    ap.add_argument("--out", default=None, help="Optional output directory for report files")
    ap.add_argument(
        "--report-format",
        default="md",
        choices=["md", "json", "both"],
        help="Write report format under --out (default: md).",
    )
    ap.add_argument("--max-items", type=int, default=400, help="Max invalid/warning items to print (default: 400)")
    ap.add_argument("--quiet", action="store_true", help="Only exit code, no stdout report")
    ap.add_argument("--version", action="store_true", help="Print version and exit")

    args = ap.parse_args(list(argv))
    if args.version:
        print("validate_evidence_hooks.py v7.0.0")
        raise SystemExit(0)

    tasks = args.tasks_flag or args.tasks
    if not tasks:
        ap.error("Missing tasks file. Provide positional <tasks.md> or --tasks <tasks.md>")

    args.tasks_path = Path(tasks)
    return args


def main(argv: Sequence[str]) -> int:
    args = _parse_args(argv)

    if not args.tasks_path.exists():
        print(f"❌ tasks file not found: {args.tasks_path}")
        return 2

    report = validate_file(args.tasks_path)

    if not args.quiet:
        print(_render_report_text(report, max_items=args.max_items))

    if args.out:
        out_dir = Path(args.out)
        _write_outputs(report, out_dir=out_dir, report_format=args.report_format)

    return 0 if report.invalid_hooks == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
