#!/usr/bin/env python3
"""validate_tasks_enhanced.py (v7.2.5)

Strict-ish validator for SmartSpec tasks.md.

Design goals
- Validate structure + strict evidence hooks without modifying governed artifacts.
- Reduce verify false-negatives by enforcing parseable evidence lines.
- Accept both `evidence:` and `- evidence:` (canonicalize internally).
- Reject legacy evidence blocks (`**Evidence Hooks:**`, `- Code: ...` bullets).
- Reject glob paths in path= and suspicious command-looking path=.

Exit code
- 0: valid
- 1: invalid (errors)
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import re
import shlex
from pathlib import Path
from typing import Dict, List, Optional, Tuple

EVIDENCE_TYPES = {"code", "test", "docs", "ui"}

ALLOWED_KEYS = {
    "code": {"path", "symbol", "contains", "regex"},
    "test": {"path", "contains", "regex", "command"},
    "docs": {"path", "contains", "heading", "regex"},
    "ui": {"path", "contains", "selector", "regex"},
}

MATCHER_KEYS = {
    "code": {"symbol", "contains", "regex"},
    "test": {"contains", "regex"},
    "docs": {"contains", "heading", "regex"},
    "ui": {"contains", "selector", "regex"},
}

SUSPICIOUS_PATH_PREFIXES = {
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

RE_TASK_LINE = re.compile(
    r"^\s*-\s*\[(?P<chk>[ xX])\]\s+(?P<id>[A-Za-z0-9][A-Za-z0-9._:-]*)(\s+|\s*$)(?P<title>.*)$"
)

# Accept bullet evidence too
RE_EVIDENCE = re.compile(r"^\s*(?:-\s*)?evidence:\s+(?P<payload>.*)$", re.IGNORECASE)

# Legacy patterns to hard-fail
RE_LEGACY_EVIDENCE_HOOKS = re.compile(r"^\s*\*\*?Evidence Hooks\*\*?:\s*$", re.IGNORECASE)
RE_LEGACY_EVIDENCE = re.compile(r"^\s*\*\*?Evidence\*\*?:\s*.+$", re.IGNORECASE)
RE_LEGACY_EVIDENCE_BULLET = re.compile(r"^\s*-\s*(Code|Test|Docs|UI)\s*:\s*.+$", re.IGNORECASE)

# Noise lines often produced by agents
RE_NOISE = re.compile(r"^\s*\$/.+\s*$")


@dataclasses.dataclass
class Finding:
    errors: List[str]
    warnings: List[str]


def _shlex(payload: str) -> Tuple[List[str], Optional[str]]:
    try:
        return shlex.split(payload), None
    except ValueError as e:
        return [], str(e)


def _strip_quotes(v: str) -> str:
    v = v.strip()
    if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
        return v[1:-1]
    return v


def _parse_evidence(payload: str, line_no: int) -> Tuple[Optional[Dict[str, str]], Optional[str], Optional[str]]:
    tokens, err = _shlex(payload)
    if err:
        return None, None, f"L{line_no}: evidence tokenization error: {err}"
    if not tokens:
        return None, None, f"L{line_no}: empty evidence payload"

    etype = tokens[0].strip().lower()
    if etype not in EVIDENCE_TYPES:
        return None, None, f"L{line_no}: invalid evidence type '{etype}'"

    kv: Dict[str, str] = {}
    stray: List[str] = []
    for t in tokens[1:]:
        if "=" in t:
            k, v = t.split("=", 1)
            kv[k.strip()] = _strip_quotes(v.strip())
        else:
            stray.append(t)

    if stray:
        return None, None, f"L{line_no}: invalid evidence (stray tokens): {stray}"

    for k in kv.keys():
        if k not in ALLOWED_KEYS[etype]:
            return None, None, f"L{line_no}: invalid key '{k}' for type '{etype}'"

    if "path" not in kv:
        return None, None, f"L{line_no}: missing required key 'path'"

    path = kv["path"].replace("\\", "/").lstrip("./")
    kv["path"] = path

    if path.startswith("/") or path.startswith("\\") or ".." in path.split("/"):
        return None, None, f"L{line_no}: invalid path (absolute/traversal): {path}"

    if any(ch in path for ch in ["*", "?", "[", "]"]):
        return None, None, f"L{line_no}: glob path is not supported in path=: {path}"

    first = path.split("/", 1)[0].lower() if path else ""
    if first in SUSPICIOUS_PATH_PREFIXES:
        return None, None, f"L{line_no}: path looks like a command (not a file path): {path}"

    if not (set(kv.keys()) & MATCHER_KEYS[etype]):
        # allow but warn
        return kv, etype, f"L{line_no}: warning: no matcher key (contains/symbol/heading/selector/regex); may cause false-negative"

    return kv, etype, None


def validate_tasks(tasks_path: Path) -> Finding:
    errors: List[str] = []
    warnings: List[str] = []

    if not tasks_path.exists():
        return Finding(errors=[f"Tasks file not found: {tasks_path}"], warnings=[])

    text = tasks_path.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()

    if not re.search(r"\|\s*spec-id\s*\|\s*source\s*\|\s*generated_by\s*\|\s*updated_at\s*\|", text, re.IGNORECASE):
        errors.append("Missing required header table with fields: spec-id | source | generated_by | updated_at")

    if not re.search(r"^##\s+Tasks\s*$", text, re.MULTILINE):
        errors.append("Missing required section heading: '## Tasks'")

    current_task_line = 0
    evidence_count = 0

    for i, line in enumerate(lines, 1):
        if RE_LEGACY_EVIDENCE_HOOKS.match(line) or RE_LEGACY_EVIDENCE.match(line) or RE_LEGACY_EVIDENCE_BULLET.match(line):
            errors.append(f"L{i}: legacy evidence format detected; must use strict 'evidence:' lines")

        if RE_NOISE.match(line):
            errors.append(f"L{i}: noise line detected inside tasks.md: {line.strip()}")

        m_task = RE_TASK_LINE.match(line)
        if m_task:
            if current_task_line and evidence_count == 0:
                errors.append(f"L{current_task_line}: task has no strict evidence lines")
            current_task_line = i
            evidence_count = 0
            continue

        m_ev = RE_EVIDENCE.match(line)
        if m_ev:
            payload = m_ev.group("payload").strip()
            kv, _etype, msg = _parse_evidence(payload, i)
            if kv is None:
                errors.append(msg or f"L{i}: invalid evidence")
            else:
                evidence_count += 1
                if msg:
                    warnings.append(msg)

    if current_task_line and evidence_count == 0:
        errors.append(f"L{current_task_line}: task has no strict evidence lines")

    return Finding(errors=errors, warnings=warnings)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tasks", required=True, help="Path to tasks.md")
    ap.add_argument("--json", action="store_true", help="Emit JSON summary")
    args = ap.parse_args()

    finding = validate_tasks(Path(args.tasks))

    if args.json:
        print(json.dumps(dataclasses.asdict(finding), ensure_ascii=False, indent=2))
    else:
        if finding.errors:
            print("ERRORS:")
            for e in finding.errors:
                print(f"- {e}")
        if finding.warnings:
            print("WARNINGS:")
            for w in finding.warnings:
                print(f"- {w}")

    return 0 if not finding.errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
