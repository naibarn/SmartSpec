#!/usr/bin/env python3
"""validate_tasks_enhanced.py

Strict-ish validator for SmartSpec tasks.md.

Goals:
- Detect invalid/legacy formats that break strict verification.
- Enforce canonical evidence hook grammar: `evidence: <type> key=value ...`.
- Catch common causes of verify false-negatives:
  - bold task IDs
  - legacy "Evidence Hooks" blocks
  - evidence lines missing the `evidence:` prefix
  - illegal key usage (e.g., heading= on non-docs)
  - missing required sections / header table

This script intentionally does NOT modify files.

Exit code:
- 0 if valid
- 1 if invalid

Usage:
  python3 validate_tasks_enhanced.py --tasks specs/<cat>/<spec-id>/tasks.md [--spec specs/<cat>/<spec-id>/spec.md]

"""

from __future__ import annotations

import argparse
import dataclasses
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


EVIDENCE_TYPES = {"code", "test", "docs", "ui"}

ALLOWED_KEYS = {
    "code": {"path", "symbol", "contains", "regex"},
    "test": {"path", "contains", "regex", "command"},
    "docs": {"path", "contains", "heading", "regex"},
    "ui": {"path", "contains", "selector", "regex"},
}

RE_TASK_LINE = re.compile(r"^\s*-\s*\[(?P<chk>[ xX])\]\s+(?P<id>[A-Za-z0-9][A-Za-z0-9._:-]*)(\s+|\s*$)(?P<title>.*)$")
RE_KV = re.compile(
    r"(?P<k>[A-Za-z_][A-Za-z0-9_-]*)=(?P<v>\"[^\"]*\"|'[^']*'|[^\s]+)"
)
RE_EVIDENCE = re.compile(r"^\s*evidence:\s+(?P<type>[a-z]+)\s*(?P<rest>.*)$")

# legacy patterns to hard-fail
RE_LEGACY_EVIDENCE_HEADER = re.compile(r"^\s*\*\*?Evidence Hooks\*\*?:\s*$", re.IGNORECASE)
RE_LEGACY_EVIDENCE_BULLET = re.compile(
    r"^\s*-\s*(Code|Test|Docs|UI)\s*:\s*(?P<body>.+)$", re.IGNORECASE
)
RE_BOLD_TASK_ID = re.compile(r"^\s*-\s*\[[ xX]\]\s+\*\*(?P<id>[^*]+)\*\*\s+")


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
    raw_lines: List[str]


def _strip_quotes(s: str) -> str:
    if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
        return s[1:-1]
    return s


def parse_evidence(line: str, line_no: int) -> Tuple[Optional[Evidence], Optional[str]]:
    m = RE_EVIDENCE.match(line)
    if not m:
        return None, None

    etype = m.group("type").strip()
    rest = m.group("rest") or ""

    if etype not in EVIDENCE_TYPES:
        return None, f"Line {line_no}: invalid evidence type '{etype}'"

    kv: Dict[str, str] = {}
    for km in RE_KV.finditer(rest):
        k = km.group("k")
        v = _strip_quotes(km.group("v"))
        kv[k] = v

    # Basic key validation
    allowed = ALLOWED_KEYS[etype]

    if "path" not in kv or not kv["path"].strip():
        return None, f"Line {line_no}: evidence '{etype}' missing required key 'path'"

    # Unknown keys
    unknown = set(kv.keys()) - allowed
    if unknown:
        return None, f"Line {line_no}: evidence '{etype}' has unknown keys: {sorted(unknown)}"

    # heading= rule
    if "heading" in kv and etype != "docs":
        return None, f"Line {line_no}: key 'heading' is only allowed for evidence type 'docs'"

    # At least one matcher besides path is recommended, but not required for some docs.
    # Still, for code/test/ui we require at least one matcher to reduce false-positives.
    if etype in {"code", "test", "ui"}:
        if not ({"symbol", "contains", "regex", "selector"} & set(kv.keys())):
            return None, f"Line {line_no}: evidence '{etype}' should include one of symbol/contains/regex/selector (path alone is too weak)"

    return Evidence(etype=etype, kv=kv, raw=line.rstrip("\n"), line_no=line_no), None


def parse_tasks_md(text: str) -> Tuple[List[Task], List[str]]:
    errors: List[str] = []
    tasks: List[Task] = []

    lines = text.splitlines()

    # 1) Header table presence (simple heuristic)
    header_ok = False
    for i in range(min(len(lines), 25)):
        if lines[i].strip().startswith("| spec-id "):
            header_ok = True
            break
    if not header_ok:
        errors.append("Missing header table (expected a table starting with '| spec-id |' within top 25 lines).")

    # 2) Must contain '## Tasks'
    if not any(l.strip() == "## Tasks" for l in lines):
        errors.append("Missing required section heading: '## Tasks'.")

    # 3) Hard fail on legacy patterns that break verifier
    for idx, l in enumerate(lines, start=1):
        if RE_BOLD_TASK_ID.match(l):
            errors.append(
                f"Line {idx}: legacy format: task id is bolded (**ID**). Use '- [ ] ID Title' (no bold)."
            )
        if RE_LEGACY_EVIDENCE_HEADER.match(l):
            errors.append(
                f"Line {idx}: legacy evidence block header 'Evidence Hooks:' detected. Replace with canonical 'evidence:' lines."
            )
        if RE_LEGACY_EVIDENCE_BULLET.match(l):
            errors.append(
                f"Line {idx}: legacy evidence bullet detected ('Code/Test/Docs/UI: ...'). Replace with canonical 'evidence:' line."
            )

    # 4) Parse tasks
    current: Optional[Task] = None

    for idx, l in enumerate(lines, start=1):
        tm = RE_TASK_LINE.match(l)
        if tm:
            # flush previous
            if current:
                tasks.append(current)

            task_id = tm.group("id")
            title = (tm.group("title") or "").strip()
            checked = tm.group("chk").strip().lower() == "x"
            current = Task(
                task_id=task_id,
                title=title,
                checked=checked,
                line_no=idx,
                evidence=[],
                raw_lines=[l],
            )
            continue

        if current is None:
            continue

        # accumulate raw lines for this task (until next task)
        if l.strip() == "":
            current.raw_lines.append(l)
            continue

        current.raw_lines.append(l)

        ev, ev_err = parse_evidence(l, idx)
        if ev_err:
            errors.append(ev_err)
        if ev:
            current.evidence.append(ev)

    if current:
        tasks.append(current)

    # 5) Task-level checks
    if not tasks:
        errors.append("No tasks found. Expected lines like '- [ ] TSK-... Title'.")

    seen: Dict[str, int] = {}
    for t in tasks:
        if t.task_id in seen:
            errors.append(
                f"Duplicate task id '{t.task_id}' at line {t.line_no} (previous at line {seen[t.task_id]})."
            )
        else:
            seen[t.task_id] = t.line_no

        # Encourage at least one evidence hook per task
        if not t.evidence:
            errors.append(
                f"Task '{t.task_id}' (line {t.line_no}) has no canonical evidence lines. Add 'evidence:' hooks."
            )

    return tasks, errors


def extract_t_refs_from_spec(spec_text: str) -> List[str]:
    # Conservative extraction: T001, T010, etc.
    # Adjust as needed for your spec conventions.
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
    parsed_tasks, errors = parse_tasks_md(tasks_text)

    warnings: List[str] = []

    # Optional spec checks
    if args.spec:
        spec_path = Path(args.spec)
        if not spec_path.exists():
            warnings.append(f"Spec file not found: {spec_path} (skipping traceability check)")
        else:
            spec_text = spec_path.read_text(encoding="utf-8", errors="replace")
            t_refs_spec = extract_t_refs_from_spec(spec_text)
            if t_refs_spec:
                # Does tasks mention any t_ref at all?
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
        print("Validate tasks against requirements")
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
