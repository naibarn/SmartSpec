#!/usr/bin/env python3
"""validate_evidence_hooks.py (v2.0.0)

Evidence Hook Validation Script (SmartSpec)

This validator checks that evidence hooks in tasks.md follow a canonical,
machine-parseable format that works with strict verification.

Canonical format (accepted):
  evidence: <code|docs|test|ui> path=<repo-relative> [key=value ...]

Examples (valid):
  evidence: code path=packages/auth-lib/tsconfig.json
  evidence: code path=packages/auth-lib/src symbol=Directory
  evidence: code path=packages/auth-service/src/routes/auth.routes.ts symbol=AuthRoutes
  evidence: docs path=docs/deployment.md heading="Deployment"
  evidence: test path=package.json command="npm run build"
  evidence: ui path=apps/web/src/pages/login.tsx selector="#login-form"

Key differences vs legacy validators:
- Allows path-only hooks (existence checks). Emits a WARNING (not ERROR)
  because matcher-less hooks can cause false-negatives if the file is renamed.
- Uses shlex parsing so quoted values with spaces are supported.
- Flags common false-negative sources (command in path=, traversal/glob paths).

Exit codes:
- 0: no invalid hooks
- 1: has invalid hooks
"""

from __future__ import annotations

import re
import shlex
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple


EVIDENCE_TYPES = {"code", "docs", "test", "ui"}

ALLOWED_KEYS = {
    "code": {"path", "symbol", "contains", "regex"},
    "docs": {"path", "heading", "contains", "regex"},
    "test": {"path", "command", "contains", "regex"},
    "ui": {"path", "selector", "contains", "regex"},
}

MATCHER_KEYS = {
    "code": {"symbol", "contains", "regex"},
    "docs": {"heading", "contains", "regex"},
    "test": {"command", "contains", "regex"},
    "ui": {"selector", "contains", "regex"},
}

COMMAND_PREFIXES = {
    "npm",
    "pnpm",
    "yarn",
    "npx",
    "bun",
    "node",
    "python",
    "python3",
    "pip",
    "pip3",
    "pytest",
    "make",
    "docker",
    "docker-compose",
    "compose",
    "go",
    "cargo",
    "mvn",
    "gradle",
    "java",
    "dotnet",
    "swagger-cli",
}

RE_EVIDENCE_LINE = re.compile(r"^\s*(?:-\s*)?evidence:\s+(?P<payload>.+?)\s*$", re.IGNORECASE)


@dataclass
class Hook:
    line_num: int
    content: str


@dataclass
class HookResult:
    hook: Hook
    valid: bool
    issues: List[str]
    warnings: List[str]


def _shlex(payload: str) -> Tuple[List[str], str | None]:
    try:
        return shlex.split(payload), None
    except ValueError as e:
        return [], str(e)


def _strip_quotes(v: str) -> str:
    v = v.strip()
    if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
        return v[1:-1]
    return v


def _normalize_path(p: str) -> str:
    p = _strip_quotes(p).replace("\\", "/")
    if p.startswith("./"):
        p = p[2:]
    return p


def parse_evidence_hooks(content: str) -> List[Hook]:
    hooks: List[Hook] = []
    for i, line in enumerate(content.split("\n"), 1):
        m = RE_EVIDENCE_LINE.match(line)
        if m:
            hooks.append(Hook(line_num=i, content=line.strip()))
    return hooks


def validate_one(hook: Hook) -> HookResult:
    issues: List[str] = []
    warnings: List[str] = []

    # payload = everything after "evidence:"
    payload = hook.content.split("evidence:", 1)[1].strip()

    tokens, err = _shlex(payload)
    if err:
        return HookResult(hook, False, [f"Tokenization error: {err}"], [])

    if not tokens:
        return HookResult(hook, False, ["Empty evidence payload"], [])

    etype = tokens[0].lower().strip()
    if etype not in EVIDENCE_TYPES:
        return HookResult(hook, False, [f"Invalid evidence type: {etype}"], [])

    kv: Dict[str, str] = {}
    stray: List[str] = []
    for t in tokens[1:]:
        if "=" not in t:
            stray.append(t)
            continue
        k, v = t.split("=", 1)
        kv[k.strip()] = _strip_quotes(v.strip())

    if stray:
        # This is the most common failure when someone writes: path=npm run build
        issues.append(f"Stray tokens not allowed (quote values with spaces): {stray}")

    # key allowlist
    for k in kv.keys():
        if k not in ALLOWED_KEYS[etype]:
            issues.append(f"Invalid key '{k}' for type '{etype}'")

    if "path" not in kv:
        issues.append("Missing required key: path=")
        return HookResult(hook, False, issues, warnings)

    path = _normalize_path(kv["path"])
    kv["path"] = path

    # path sanity checks
    if not path:
        issues.append("Empty path=")

    if path.startswith("/") or re.match(r"^[A-Za-z]:/", path):
        issues.append("Absolute path is not allowed")

    if ".." in path.split("/"):
        issues.append("Path traversal (..) is not allowed")

    if any(ch in path for ch in ["*", "?", "[", "]"]):
        issues.append("Glob patterns are not allowed in path=")

    first = path.split("/", 1)[0].lower() if path else ""
    if first in COMMAND_PREFIXES:
        issues.append(f"Path appears to be a command; use command= and keep path= as an anchor file: {path}")

    # command should be quoted if it contains spaces (shlex already handled quoting, but we warn if likely wrong)
    if etype == "test" and "command" in kv:
        if not kv["command"].strip():
            issues.append("command= is empty")

    # matcher policy: allow path-only but warn
    if not (set(kv.keys()) & MATCHER_KEYS[etype]):
        warnings.append(
            "No matcher key (contains/symbol/heading/selector/regex/command). Allowed, but may cause false-negative if file moves."
        )

    # code directory shorthand: allow, but recommend symbol=Directory
    if etype == "code":
        if path.endswith("/") and kv.get("symbol") != "Directory":
            warnings.append("Directory path should set symbol=Directory for bounded scan/existence.")

    valid = len(issues) == 0
    return HookResult(hook, valid, issues, warnings)


def generate_report(tasks_path: Path) -> Tuple[List[HookResult], str]:
    content = tasks_path.read_text(encoding="utf-8", errors="ignore")
    hooks = parse_evidence_hooks(content)

    results: List[HookResult] = []
    for h in hooks:
        results.append(validate_one(h))

    valid = [r for r in results if r.valid]
    invalid = [r for r in results if not r.valid]

    # Print report in a style similar to the previous script
    lines: List[str] = []
    lines.append("=" * 60)
    lines.append("EVIDENCE HOOK VALIDATION REPORT")
    lines.append("=" * 60)
    lines.append(f"File: {tasks_path}")
    lines.append("")
    lines.append("Summary:")
    lines.append(f"  Total evidence hooks: {len(results)}")
    lines.append(f"  Valid hooks: {len(valid)}")
    lines.append(f"  Invalid hooks: {len(invalid)}")
    lines.append(f"  Validity: {(len(valid) / len(results) * 100) if results else 0:.1f}%")

    # warnings summary
    warn_count = sum(1 for r in results if r.warnings)
    lines.append(f"  Hooks with warnings: {warn_count}")

    if invalid:
        lines.append("")
        lines.append("=" * 60)
        lines.append(f"INVALID EVIDENCE HOOKS ({len(invalid)}):")
        lines.append("=" * 60)

        for r in invalid:
            lines.append("")
            lines.append(f"Line {r.hook.line_num}:")
            lines.append(f"  Content: {r.hook.content}")
            lines.append("  Issues:")
            for issue in r.issues:
                lines.append(f"    - {issue}")

    # Show warnings (first 80) to help cleanup, but don't fail.
    warnings_list = [r for r in results if r.warnings]
    if warnings_list:
        lines.append("")
        lines.append("=" * 60)
        lines.append(f"WARNINGS ({len(warnings_list)} hooks):")
        lines.append("=" * 60)
        shown = 0
        for r in warnings_list:
            if shown >= 80:
                lines.append(f"... truncated ({len(warnings_list) - shown} more)")
                break
            lines.append("")
            lines.append(f"Line {r.hook.line_num}:")
            lines.append(f"  Content: {r.hook.content}")
            for w in r.warnings:
                lines.append(f"    - {w}")
            shown += 1

    lines.append("")
    lines.append("=" * 60)

    return results, "\n".join(lines)


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: validate_evidence_hooks.py <path-to-tasks.md>")
        return 1

    tasks_path = Path(sys.argv[1])
    if not tasks_path.exists():
        print(f"Error: File not found: {tasks_path}")
        return 1

    results, report_text = generate_report(tasks_path)
    print(report_text)

    invalid = [r for r in results if not r.valid]
    if invalid:
        return 1

    print("✅ All evidence hooks are valid (warnings may remain).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
