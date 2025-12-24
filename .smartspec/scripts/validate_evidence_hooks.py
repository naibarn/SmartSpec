#!/usr/bin/env python3
"""validate_evidence_hooks.py (v2.2.2)

Canonical Evidence Hook Validator for SmartSpec tasks.md

Validates that evidence hooks follow a strict, shlex-parseable canonical format
compatible with strict verifiers.

Canonical evidence hook line:
  evidence: <code|test|docs|ui> key=value key="value with spaces" ...

Key guarantees:
- No stray tokens: every token after type MUST be key=value.
- Values containing spaces MUST be quoted.
- Only supported evidence types: code|test|docs|ui.
- Required key: path= for all types.
- Path must be repo-relative (no absolute, no traversal, no globs).
- **Path must not contain whitespace** (commands belong in command=).

This script:
- DOES NOT execute any commands.
- DOES NOT use the network.

Exit codes:
- 0: valid (warnings allowed)
- 1: invalid hooks found (or warnings treated as errors)
- 2: usage or file error

"""

from __future__ import annotations

import argparse
import json
import re
import shlex
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple


STRICT_TYPES = {"code", "test", "docs", "ui"}

ALLOWED_KEYS: Dict[str, set[str]] = {
    "code": {"path", "symbol", "contains", "regex"},
    "test": {"path", "command", "contains", "regex"},
    "docs": {"path", "heading", "contains", "regex"},
    "ui": {"path", "selector", "contains", "regex"},
}

# Keys that make evidence more robust than "file exists".
MATCHER_KEYS = {"contains", "symbol", "heading", "selector", "regex", "command"}

# Common command prefixes; should not appear as path roots or as the first word.
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

RE_EVIDENCE = re.compile(r"^\s*evidence:\s+(?P<payload>.*)$", re.IGNORECASE)
RE_EVIDENCE_BULLET = re.compile(r"^\s*-\s*evidence:\s+(?P<payload>.*)$", re.IGNORECASE)


@dataclass
class Issue:
    severity: str  # "error" | "warning"
    message: str


@dataclass
class HookResult:
    line_no: int
    content: str
    issues: List[Issue]

    @property
    def is_valid(self) -> bool:
        return not any(i.severity == "error" for i in self.issues)

    @property
    def has_warnings(self) -> bool:
        return any(i.severity == "warning" for i in self.issues)


def _safe_rel_path(p: str) -> str:
    p = p.strip().strip('"').strip("'").replace("\\", "/")
    if p.startswith("./"):
        p = p[2:]
    return p


def _is_abs_or_traversal(p: str) -> bool:
    if not p:
        return True
    p = _safe_rel_path(p)
    if p.startswith("/") or re.match(r"^[A-Za-z]:/", p):
        return True
    if ".." in p.split("/"):
        return True
    return False


def _has_glob(p: str) -> bool:
    return any(ch in p for ch in ("*", "?", "[", "]"))


def _split_payload_strict(payload: str) -> Tuple[List[str], Optional[str]]:
    try:
        return shlex.split(payload, posix=True), None
    except Exception as e:
        return [], f"shlex_error:{e}"


def _parse_tokens(tokens: Sequence[str]) -> Tuple[str, Dict[str, str], List[str]]:
    if not tokens:
        return "", {}, []

    hook_type = tokens[0]
    kv: Dict[str, str] = {}
    stray: List[str] = []

    for t in tokens[1:]:
        if "=" not in t:
            stray.append(t)
            continue
        k, v = t.split("=", 1)
        kv[k.strip()] = v.strip()

    return hook_type, kv, stray


def _first_word(s: str) -> str:
    s = s.strip()
    if not s:
        return ""
    return s.split()[0]


def validate_hook_line(line_no: int, raw_line: str) -> Optional[HookResult]:
    m = RE_EVIDENCE.match(raw_line)
    bullet = False
    if not m:
        m = RE_EVIDENCE_BULLET.match(raw_line)
        bullet = bool(m)
    if not m:
        return None

    payload = m.group("payload").strip()
    issues: List[Issue] = []

    if not payload:
        issues.append(Issue("error", "Empty evidence payload"))
        return HookResult(line_no, raw_line.rstrip("\n"), issues)

    if bullet:
        issues.append(Issue("warning", "Evidence is written as a list item (- evidence: ...). Prefer canonical 'evidence:' line."))

    tokens, err = _split_payload_strict(payload)
    if err:
        issues.append(Issue("error", f"Does not parse with shlex ({err}). Quote values with spaces."))
        return HookResult(line_no, raw_line.rstrip("\n"), issues)

    hook_type, kv, stray = _parse_tokens(tokens)

    if stray:
        issues.append(Issue("error", f"Stray tokens not allowed (quote values with spaces): {stray}"))

    ht = hook_type.strip().lower()
    if ht not in STRICT_TYPES:
        issues.append(Issue("error", f"Unknown evidence type: {hook_type} (allowed: code|test|docs|ui)"))
        return HookResult(line_no, raw_line.rstrip("\n"), issues)

    if "path" not in kv or not kv.get("path"):
        issues.append(Issue("error", "Missing required key: path"))
        return HookResult(line_no, raw_line.rstrip("\n"), issues)

    raw_path = kv.get("path", "")

    # Hard rule: path must not contain whitespace.
    # Commands belong in command= (test) or as matchers (contains/regex), not in path.
    if re.search(r"\s", raw_path):
        issues.append(Issue("error", f"path contains whitespace; path must be a repo file path, not a command: {raw_path}"))

    path_val = _safe_rel_path(raw_path)

    if _is_abs_or_traversal(path_val):
        issues.append(Issue("error", f"Path must be repo-relative and not traversal/absolute: {raw_path}"))

    if _has_glob(path_val):
        issues.append(Issue("error", f"Glob patterns not allowed in path=: {raw_path}"))

    # Reject commands stuffed into path.
    root_segment = path_val.split("/", 1)[0].lower() if path_val else ""
    first_word = _first_word(path_val).lower() if path_val else ""
    if root_segment in SUSPICIOUS_PATH_PREFIXES or first_word in SUSPICIOUS_PATH_PREFIXES:
        issues.append(
            Issue(
                "error",
                f"path looks like a command. Put the command under command= and use a real file under path=: {raw_path}",
            )
        )

    allowed = ALLOWED_KEYS.get(ht, set())
    unknown_keys = sorted(k for k in kv.keys() if k not in allowed)
    if unknown_keys:
        issues.append(Issue("warning", f"Unknown keys for type={ht}: {unknown_keys}. Allowed keys: {sorted(allowed)}"))

    if not any(k in kv for k in MATCHER_KEYS):
        issues.append(Issue("warning", "No matcher key (contains/symbol/heading/selector/regex/command). Allowed, but may cause false-negative if file moves."))

    if ht == "code" and "heading" in kv:
        issues.append(Issue("warning", "heading= is typically used with docs evidence; consider switching to type=docs."))

    if ht == "test" and "command" in kv and not kv["command"].strip():
        issues.append(Issue("error", "command= is present but empty"))

    return HookResult(line_no, raw_line.rstrip("\n"), issues)


def validate_file(tasks_path: Path) -> List[HookResult]:
    lines = tasks_path.read_text(encoding="utf-8", errors="ignore").splitlines(True)
    results: List[HookResult] = []
    for i, line in enumerate(lines, start=1):
        r = validate_hook_line(i, line)
        if r:
            results.append(r)
    return results


def print_report(tasks_path: Path, results: List[HookResult], *, show_warnings: bool = True) -> None:
    total = len(results)
    invalid = [r for r in results if not r.is_valid]
    valid = [r for r in results if r.is_valid]
    warn = [r for r in results if r.has_warnings]

    validity = (len(valid) / total * 100.0) if total else 100.0

    print("=" * 60)
    print("EVIDENCE HOOK VALIDATION REPORT")
    print("=" * 60)
    print(f"File: {tasks_path.as_posix()}")
    print()
    print("Summary:")
    print(f"  Total evidence hooks: {total}")
    print(f"  Valid hooks: {len(valid)}")
    print(f"  Invalid hooks: {len(invalid)}")
    print(f"  Validity: {validity:.1f}%")
    print(f"  Hooks with warnings: {len(warn)}")
    print()

    if invalid:
        print("=" * 60)
        print(f"INVALID EVIDENCE HOOKS ({len(invalid)}):")
        print("=" * 60)
        print()
        for r in invalid:
            print(f"Line {r.line_no}:")
            print(f"  Content: {r.content.strip()}")
            print("  Issues:")
            for iss in r.issues:
                if iss.severity == "error":
                    print(f"    - {iss.message}")
            print()

    if show_warnings and warn:
        print("=" * 60)
        print(f"WARNINGS ({len(warn)} hooks):")
        print("=" * 60)
        print()
        for r in warn:
            warn_msgs = [i.message for i in r.issues if i.severity == "warning"]
            if not warn_msgs:
                continue
            print(f"Line {r.line_no}:")
            print(f"  Content: {r.content.strip()}")
            for msg in warn_msgs:
                print(f"    - {msg}")
            print()


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate canonical SmartSpec evidence hooks in tasks.md")
    ap.add_argument("tasks_file", help="Path to tasks.md (typically specs/**/tasks.md or a preview under .spec/reports/**)")
    ap.add_argument("--json", action="store_true", help="Output JSON summary")
    ap.add_argument("--quiet", action="store_true", help="Suppress non-essential output")
    ap.add_argument("--no-warnings", action="store_true", help="Do not print warning details")
    ap.add_argument("--fail-on-warnings", action="store_true", help="Return non-zero if any warnings")
    args = ap.parse_args()

    tasks_path = Path(args.tasks_file)
    if not tasks_path.exists():
        print(f"ERROR: file not found: {tasks_path}")
        return 2

    results = validate_file(tasks_path)

    invalid = [r for r in results if not r.is_valid]
    warn = [r for r in results if r.has_warnings]

    if args.json:
        payload = {
            "file": tasks_path.as_posix(),
            "total": len(results),
            "valid": len(results) - len(invalid),
            "invalid": len(invalid),
            "warnings": len(warn),
            "invalid_lines": [
                {
                    "line": r.line_no,
                    "content": r.content.strip(),
                    "issues": [{"severity": i.severity, "message": i.message} for i in r.issues],
                }
                for r in invalid
            ],
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        if not args.quiet:
            print_report(tasks_path, results, show_warnings=not args.no_warnings)

    if invalid:
        return 1
    if args.fail_on_warnings and warn:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
