#!/usr/bin/env python3
"""validate_evidence_hooks.py (v2.0.0)

Validates evidence hooks inside a SmartSpec tasks.md file.

Why this exists
- Strict verifier workflows (e.g. /smartspec_verify_tasks_progress_strict) rely on
  *parseable* evidence hooks.
- The most common false-negative cause is "implement แล้ว แต่ verify ไม่เจอ" because
  evidence hooks are syntactically valid-ish but semantically wrong (e.g. path is a command).

Canonical evidence hook (minimum)
  evidence: <type> <key>=<value> <key>=<value> ...

Supported types:
  - code  (requires: path)
  - test  (requires: path)
  - docs  (requires: path)
  - ui    (requires: screen)

Common keys:
  - code: symbol, contains
  - test: command, contains
  - docs: heading, contains
  - ui: route, component, states, selector, contains

NOTE
- This script does NOT execute any commands.
- This script does NOT modify files.

Exit codes
- 0: no invalid hooks
- 1: one or more invalid hooks
- 2: runtime error
"""

from __future__ import annotations

import argparse
import json
import re
import shlex
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple


STRICT_TYPES = {"code", "test", "docs", "ui"}

# Values that strongly indicate someone accidentally placed a command into path=...
SUSPICIOUS_PATH_PREFIXES = {
    "npm",
    "pnpm",
    "yarn",
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
    "bun",
}

RE_EVIDENCE_ANYWHERE = re.compile(r"evidence:\s*(.+)$", re.IGNORECASE)
RE_MD_CODE_FENCE = re.compile(r"^\s*```")


@dataclass
class Hook:
    line_no: int
    raw_line: str
    payload: str


@dataclass
class HookValidation:
    valid: bool
    issues: List[str]
    hook_type: Optional[str] = None
    kv: Optional[Dict[str, str]] = None


def _looks_like_glob(p: str) -> bool:
    return any(ch in p for ch in ("*", "?", "[", "]"))


def _is_abs_or_traversal(p: str) -> bool:
    p = p.replace("\\", "/")
    if p.startswith("/"):
        return True
    if re.match(r"^[A-Za-z]:/", p):
        return True
    if p == ".." or p.startswith("../") or "/../" in p:
        return True
    return False


def _first_segment(p: str) -> str:
    p = p.strip().replace("\\", "/")
    seg = p.split("/", 1)[0].strip().strip('"')
    return seg.lower()


def parse_hooks_from_markdown(md: str) -> List[Hook]:
    """Extract evidence hooks from tasks markdown.

    We intentionally *do not* rely on indentation:
    - evidence may appear as a plain line, a bullet, or inside a table cell.

    We also skip fenced code blocks to avoid false positives in examples.
    """

    hooks: List[Hook] = []
    in_fence = False

    for i, line in enumerate(md.splitlines(), start=1):
        if RE_MD_CODE_FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        m = RE_EVIDENCE_ANYWHERE.search(line)
        if not m:
            continue

        payload = m.group(1).strip()
        # Normalize "- evidence:" into "evidence:" by just capturing the payload
        hooks.append(Hook(line_no=i, raw_line=line.rstrip("\n"), payload=payload))

    return hooks


def _shlex_split(payload: str) -> Tuple[List[str], Optional[str]]:
    try:
        return shlex.split(payload, posix=True), None
    except Exception as e:
        return [], f"shlex_error:{e}"


def _parse_kv(tokens: List[str]) -> Tuple[Dict[str, str], List[str]]:
    kv: Dict[str, str] = {}
    issues: List[str] = []

    for t in tokens:
        if "=" not in t:
            issues.append(f"Stray token '{t}' (expected key=value).")
            continue
        k, v = t.split("=", 1)
        k = k.strip()
        v = v.strip()
        if not k:
            issues.append("Empty key in key=value token.")
            continue
        kv[k] = v

    return kv, issues


def validate_hook_payload(payload: str) -> HookValidation:
    tokens, err = _shlex_split(payload)
    if err:
        return HookValidation(False, ["Unparseable evidence payload", err])

    if not tokens:
        return HookValidation(False, ["Empty evidence payload"])  # nothing to do

    hook_type = tokens[0].strip().lower()
    if hook_type not in STRICT_TYPES:
        return HookValidation(False, [f"Unsupported evidence type '{hook_type}' (expected one of: {sorted(STRICT_TYPES)})"], hook_type=hook_type)

    kv, kv_issues = _parse_kv(tokens[1:])
    issues = list(kv_issues)

    # Required keys
    if hook_type in {"code", "test", "docs"}:
        if "path" not in kv:
            issues.append("Missing required key: path=")
    if hook_type == "ui":
        if "screen" not in kv:
            issues.append("Missing required key: screen=")

    # Disallow placeholders
    for k, v in kv.items():
        if "???" in v or "TODO" in v.upper():
            issues.append(f"Placeholder detected in {k}={v!r}")

    # Path semantics (only for types that have path)
    if "path" in kv:
        p = kv["path"].strip().strip('"')

        if _is_abs_or_traversal(p):
            issues.append("path must be repo-relative and must not contain '..' or be absolute")

        if _looks_like_glob(p):
            issues.append("glob patterns are not allowed in path=")

        # Biggest false-negative driver: command accidentally placed into path
        first = _first_segment(p)
        if first in SUSPICIOUS_PATH_PREFIXES:
            issues.append(
                "path looks like a command (e.g. npm/pnpm/yarn). Use: evidence: test path=<anchor-file> command=\"<command>\""
            )

    # Type-key compatibility checks (strict, to prevent confusing hooks)
    if hook_type == "code" and "heading" in kv:
        issues.append("code evidence must not use heading=. If this points to docs/spec, use: evidence: docs ... heading=\"...\"")

    if hook_type == "docs" and "symbol" in kv:
        issues.append("docs evidence must not use symbol=. If this is code, use: evidence: code ... symbol=<Symbol>")

    # Quoting rules: values with spaces must be quoted (shlex would already have parsed them)
    # We can still warn if the raw payload contains unquoted spaces in a value, but that is hard to reconstruct.

    return HookValidation(valid=(len(issues) == 0), issues=issues, hook_type=hook_type, kv=kv)


def validate_tasks_file(path: Path) -> Tuple[Dict, int]:
    content = path.read_text(encoding="utf-8", errors="ignore")
    hooks = parse_hooks_from_markdown(content)

    invalid: List[Dict] = []
    valid_count = 0

    for h in hooks:
        v = validate_hook_payload(h.payload)
        if v.valid:
            valid_count += 1
            continue
        invalid.append(
            {
                "line": h.line_no,
                "content": h.raw_line.strip(),
                "payload": h.payload,
                "issues": v.issues,
            }
        )

    report = {
        "file": str(path),
        "summary": {
            "total_evidence_hooks": len(hooks),
            "valid_hooks": valid_count,
            "invalid_hooks": len(invalid),
            "validity": (valid_count / len(hooks) * 100.0) if hooks else 100.0,
        },
        "invalid": invalid,
    }

    exit_code = 0 if len(invalid) == 0 else 1
    return report, exit_code


def render_human_report(report: Dict) -> str:
    file_path = report["file"]
    s = report["summary"]
    invalid = report.get("invalid", [])

    lines: List[str] = []
    lines.append("=" * 60)
    lines.append("EVIDENCE HOOK VALIDATION REPORT")
    lines.append("=" * 60)
    lines.append(f"File: {file_path}")
    lines.append("")
    lines.append("Summary:")
    lines.append(f"  Total evidence hooks: {s['total_evidence_hooks']}")
    lines.append(f"  Valid hooks: {s['valid_hooks']}")
    lines.append(f"  Invalid hooks: {s['invalid_hooks']}")
    lines.append(f"  Validity: {s['validity']:.1f}%")

    if invalid:
        lines.append("")
        lines.append("=" * 60)
        lines.append(f"INVALID EVIDENCE HOOKS ({len(invalid)}):")
        lines.append("=" * 60)
        lines.append("")

        # Avoid flooding terminal
        max_show = 200
        for item in invalid[:max_show]:
            lines.append(f"Line {item['line']}:")
            lines.append(f"  Content: {item['content']}")
            lines.append("  Issues:")
            for iss in item["issues"]:
                lines.append(f"    - {iss}")
            lines.append("")
        if len(invalid) > max_show:
            lines.append(f"... {len(invalid) - max_show} more invalid hooks omitted ...")

    return "\n".join(lines) + "\n"


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Validate evidence hooks in tasks.md")
    ap.add_argument("--tasks", required=True, help="Path to tasks.md")
    ap.add_argument("--json", action="store_true", help="Output JSON")

    args = ap.parse_args(argv)

    tasks_path = Path(args.tasks)
    if not tasks_path.exists():
        print(f"❌ tasks file not found: {tasks_path}", file=sys.stderr)
        return 2

    try:
        report, exit_code = validate_tasks_file(tasks_path)
    except Exception as e:
        print(f"❌ validation error: {e}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render_human_report(report), end="")

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
