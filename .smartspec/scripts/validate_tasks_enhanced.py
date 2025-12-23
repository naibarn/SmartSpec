#!/usr/bin/env python3
"""validate_tasks_enhanced.py (v7.2.6)

Strict-ish validator for SmartSpec tasks.md.

New in v7.2.6
-------------
- Explicitly flags bullet evidence lines (`- evidence: ...`) as invalid, because strict verifiers
  typically require the line to start with `evidence:`.

Retains v7.2.4 protections
-------------------------
- shlex-based evidence payload parsing (quote/space safety)
- blocks contains=exists
- blocks glob characters in path= (* ? [ ])
- blocks legacy Evidence Hooks / Evidence / Code: bullets
- blocks duplicate '## Tasks'
- blocks noise lines like '$/a' inside Tasks section

Exit code:
- 0 if valid
- 1 if invalid

Usage:
  python3 validate_tasks_enhanced.py --tasks specs/<cat>/<spec-id>/tasks.md [--spec specs/<cat>/<spec-id>/spec.md] [--json]
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
RE_EVIDENCE = re.compile(r"^\s*evidence:\s+(?P<payload>.*)$", re.IGNORECASE)
RE_BULLET_EVIDENCE = re.compile(r"^\s*[-*]\s+evidence:\s+.+$", re.IGNORECASE)

# legacy patterns to hard-fail
RE_LEGACY_EVIDENCE_HOOKS = re.compile(r"^\s*\*\*?Evidence Hooks\*\*?:\s*$", re.IGNORECASE)
RE_LEGACY_EVIDENCE = re.compile(r"^\s*\*\*?Evidence\*\*?:\s*.+$", re.IGNORECASE)
RE_LEGACY_EVIDENCE_BULLET = re.compile(r"^\s*-\s*(Code|Test|Docs|UI)\s*:\s*.+$", re.IGNORECASE)
RE_BOLD_TASK_ID = re.compile(r"^\s*-\s*\[[ xX]\]\s+\*\*[^*]+\*\*\s+")

# noise lines
RE_NOISE = re.compile(r"^\s*\$/.+\s*$")


@dataclasses.dataclass
class Evidence:
    etype: str
    kv: Dict[str, str]
    raw: str
    line_no: int


@dataclasses.dataclass
class Task:
    task_id: str
    title: str
    checked: bool
    line_no: int
    evidence: List[Evidence]


def _normalize_path(p: str) -> str:
    p = (p or "").strip().strip('"\'')
    p = p.replace("\\", "/")
    if p.startswith("./"):
        p = p[2:]
    p = re.sub(r"/{2,}", "/", p)
    return p


def _has_glob(p: str) -> bool:
    return any(ch in p for ch in ["*", "?", "[", "]"])


def _is_rel_path(p: str) -> bool:
    p = _normalize_path(p)
    if not p:
        return False
    if p.startswith("/") or re.match(r"^[a-zA-Z]:/", p):
        return False
    if ".." in p.split("/"):
        return False
    if any(ch.isspace() for ch in p):
        return False
    return True


def _looks_like_command_path(p: str) -> bool:
    p = _normalize_path(p)
    first = p.split("/", 1)[0].lower() if p else ""
    return first in SUSPICIOUS_PATH_PREFIXES


def parse_evidence(line: str, line_no: int) -> Tuple[Optional[Evidence], Optional[str]]:
    m = RE_EVIDENCE.match(line)
    if not m:
        return None, None

    payload = (m.group("payload") or "").strip()
    if not payload:
        return None, f"Line {line_no}: empty evidence payload"

    try:
        tokens = shlex.split(payload)
    except Exception as e:
        return None, (
            f"Line {line_no}: evidence payload not parseable (quote error): {e}. "
            "Tip: wrap JSON fragments in single quotes, e.g. contains='\\\"node\\\": \\\"22.x\\\"'"
        )

    if not tokens:
        return None, f"Line {line_no}: evidence payload empty"

    etype = tokens[0].strip().lower()
    if etype not in EVIDENCE_TYPES:
        return None, f"Line {line_no}: invalid evidence type '{etype}'"

    kv: Dict[str, str] = {}
    stray: List[str] = []

    for tok in tokens[1:]:
        if "=" not in tok:
            stray.append(tok)
            continue
        k, v = tok.split("=", 1)
        k = k.strip()
        v = v.strip()
        if not k:
            stray.append(tok)
            continue
        kv[k] = v

    if stray:
        return None, (
            f"Line {line_no}: evidence has stray tokens {stray}. "
            "This usually means your value contains quotes/spaces and must be quoted/escaped."
        )

    allowed = ALLOWED_KEYS[etype]

    if "path" not in kv or not kv["path"].strip():
        return None, f"Line {line_no}: evidence '{etype}' missing required key 'path'"

    unknown = set(kv.keys()) - allowed
    if unknown:
        return None, f"Line {line_no}: evidence '{etype}' has unknown keys: {sorted(unknown)}"

    if "heading" in kv and etype != "docs":
        return None, f"Line {line_no}: key 'heading' is only allowed for evidence type 'docs'"

    # placeholder matcher
    if "contains" in kv:
        cv = kv["contains"].strip().strip('"\'').lower()
        if cv == "exists":
            return None, f"Line {line_no}: contains=exists is not allowed (use regex=\".\" for existence-only proof)"

    # path safety
    path = kv.get("path", "")
    if not _is_rel_path(path):
        return None, f"Line {line_no}: invalid path (must be repo-relative, no traversal/spaces): {path}"
    if _looks_like_command_path(path):
        return None, f"Line {line_no}: path looks like a command (use command= instead): path={path}"
    if _has_glob(path):
        return None, f"Line {line_no}: glob characters are not allowed in path= (use concrete file path): path={path}"

    # require matcher for code/test/ui
    if etype in {"code", "test", "ui"}:
        if not (MATCHER_KEYS[etype] & set(kv.keys())):
            return None, (
                f"Line {line_no}: evidence '{etype}' must include one of {sorted(MATCHER_KEYS[etype])} "
                "(path alone is too weak)"
            )

    return Evidence(etype=etype, kv=kv, raw=line.rstrip("\n"), line_no=line_no), None


def _find_tasks_section_bounds(lines: List[str]) -> Tuple[Optional[int], Optional[int]]:
    start = None
    for i, l in enumerate(lines):
        if l.strip() == "## Tasks":
            start = i
            break
    if start is None:
        return None, None

    end = len(lines)
    for j in range(start + 1, len(lines)):
        if re.match(r"^#\s+\S", lines[j]):
            end = j
            break
    return start, end


def parse_tasks_md(text: str) -> Tuple[List[Task], List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []
    tasks: List[Task] = []

    lines = text.splitlines()

    # header table presence
    header_ok = any(l.strip().lower().startswith("| spec-id ") for l in lines[:25])
    if not header_ok:
        errors.append("Missing header table (expected a table starting with '| spec-id |' within top 25 lines).")

    # must contain '## Tasks' exactly once
    tasks_headers = [i for i, l in enumerate(lines, start=1) if l.strip() == "## Tasks"]
    if not tasks_headers:
        errors.append("Missing required section heading: '## Tasks'.")
    elif len(tasks_headers) > 1:
        errors.append(f"Duplicate '## Tasks' headings found at lines: {tasks_headers}. Normalize to a single section.")

    # explicit error for '- evidence:' lines
    for idx, l in enumerate(lines, start=1):
        if RE_BULLET_EVIDENCE.match(l):
            errors.append(
                f"Line {idx}: bullet evidence '- evidence:' is not allowed. Use an indented 'evidence:' line (no leading '-')."
            )

    # hard-fail legacy patterns
    for idx, l in enumerate(lines, start=1):
        if RE_BOLD_TASK_ID.match(l):
            errors.append(f"Line {idx}: legacy format: task id is bolded (**ID**). Use '- [ ] ID Title' (no bold).")
        if RE_LEGACY_EVIDENCE_HOOKS.match(l):
            errors.append(f"Line {idx}: legacy evidence block header 'Evidence Hooks:' detected. Replace with canonical 'evidence:' lines.")
        if RE_LEGACY_EVIDENCE.match(l):
            errors.append(f"Line {idx}: legacy '**Evidence:**' line detected. Replace with canonical 'evidence:' lines.")
        if RE_LEGACY_EVIDENCE_BULLET.match(l):
            errors.append(f"Line {idx}: legacy evidence bullet detected ('Code/Test/Docs/UI: ...'). Replace with canonical 'evidence:' line.")

    # noise lines inside Tasks section
    s, e = _find_tasks_section_bounds(lines)
    if s is not None:
        for idx in range(s + 1, e):
            if RE_NOISE.match(lines[idx]):
                errors.append(f"Line {idx+1}: stray noise line in Tasks section: {lines[idx].strip()}")

    current: Optional[Task] = None

    for idx, l in enumerate(lines, start=1):
        tm = RE_TASK_LINE.match(l)
        if tm:
            if current:
                tasks.append(current)
            task_id = tm.group("id")
            title = (tm.group("title") or "").strip()
            checked = tm.group("chk").strip().lower() == "x"
            current = Task(task_id=task_id, title=title, checked=checked, line_no=idx, evidence=[])
            continue

        if current is None:
            continue

        ev, ev_err = parse_evidence(l, idx)
        if ev_err:
            errors.append(ev_err)
        if ev:
            current.evidence.append(ev)

    if current:
        tasks.append(current)

    if not tasks:
        errors.append("No tasks found. Expected lines like '- [ ] TSK-... Title'.")

    # duplicate IDs + require evidence per task
    seen: Dict[str, int] = {}
    for t in tasks:
        if t.task_id in seen:
            errors.append(f"Duplicate task id '{t.task_id}' at line {t.line_no} (previous at line {seen[t.task_id]}).")
        else:
            seen[t.task_id] = t.line_no

        if not t.evidence:
            errors.append(f"Task '{t.task_id}' (line {t.line_no}) has no canonical evidence lines. Add 'evidence:' hooks.")

    return tasks, errors, warnings


def extract_t_refs_from_spec(spec_text: str) -> List[str]:
    return sorted(set(re.findall(r"\bT\d{3,4}\b", spec_text)))


def extract_t_refs_from_tasks(tasks_text: str) -> List[str]:
    return sorted(set(re.findall(r"\bt_ref:\s*([A-Za-z0-9._:-]+)", tasks_text)))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tasks", required=True, help="Path to tasks.md")
    ap.add_argument("--spec", required=False, help="Optional path to spec.md for traceability checks")
    ap.add_argument("--json", action="store_true", help="Emit JSON summary")
    args = ap.parse_args()

    tasks_path = Path(args.tasks)
    if not tasks_path.exists():
        print(f"ERROR: tasks file not found: {tasks_path}")
        return 1

    tasks_text = tasks_path.read_text(encoding="utf-8", errors="replace")
    parsed_tasks, errors, warnings = parse_tasks_md(tasks_text)

    # optional spec check
    if args.spec:
        spec_path = Path(args.spec)
        if not spec_path.exists():
            warnings.append(f"Spec file not found: {spec_path} (skipping traceability check)")
        else:
            spec_text = spec_path.read_text(encoding="utf-8", errors="replace")
            t_refs_spec = extract_t_refs_from_spec(spec_text)
            if t_refs_spec:
                t_refs_tasks = extract_t_refs_from_tasks(tasks_text)
                missing = [t for t in t_refs_spec if t not in t_refs_tasks]
                if missing:
                    warnings.append(
                        f"T_references from spec.md not found in tasks t_ref lines: {', '.join(missing[:50])}"
                        + (" ..." if len(missing) > 50 else "")
                    )

    valid = len(errors) == 0

    if args.json:
        out = {
            "valid": valid,
            "task_count": len(parsed_tasks),
            "errors": errors,
            "warnings": warnings,
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print("Validate tasks against requirements (strict evidence + hygiene)")
        if warnings:
            print(f"\nWARNINGS ({len(warnings)}):")
            for w in warnings:
                print(f"  - {w}")
        if errors:
            print(f"\nERRORS ({len(errors)}):")
            for e in errors:
                print(f"  - {e}")

        if valid:
            print("\n✓ Tasks file is VALID")
        else:
            print("\n✗ Tasks file is INVALID - please fix errors above")

    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
