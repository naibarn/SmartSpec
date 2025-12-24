#!/usr/bin/env python3
"""validate_tasks_enhanced.py (v1.5.0)

SmartSpec Tasks Validator (structure + references)

Validates that a tasks.md file follows the expected SmartSpec structure.

What this validator checks (high signal):
- Header table exists near the top (| Key | Value |).
- Required section: '## Tasks'.
- Task checkbox lines exist and have stable IDs.
- No duplicate task IDs.
- Evidence lines are properly indented beneath a task and start with 'evidence:'
  (Canonical evidence formatting details are validated by validate_evidence_hooks.py).
- Optional: verify referenced IDs (e.g., T001...) exist in spec.md, if --spec provided.

Governance
- READ-ONLY: MUST NOT modify any files.
- No network.

Exit codes
- 0: valid (warnings may exist unless --fail-on-warnings)
- 1: invalid
- 2: usage / file errors
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


# Basic structure
RE_H1 = re.compile(r"^#\s+.+")
RE_SECTION_TASKS = re.compile(r"^##\s+Tasks\s*$")

# Markdown table rows like: | Key | Value |
RE_TABLE_ROW = re.compile(r"^\|\s*[^|]+\s*\|\s*[^|]+\s*\|\s*$")

# Task checkbox line, capturing ID and title
# Example: - [ ] TSK-AUTH-001 Implement ...
RE_TASK_LINE = re.compile(
    r"^\s*-\s*\[(?P<chk>[ xX])\]\s+(?P<id>[A-Za-z0-9][A-Za-z0-9._:-]*)\b(\s+|\s*$)(?P<title>.*)$"
)

# Evidence line (indent recommended but we validate relationship)
RE_EVIDENCE_LINE = re.compile(r"^\s*evidence:\s+.+$", re.IGNORECASE)

# Spec reference tokens (customize as needed; supports T001, T010, etc.)
RE_SPEC_REF = re.compile(r"\bT\d{3,4}\b")


@dataclass
class Issue:
    level: str  # ERROR/WARN
    message: str
    line_no: Optional[int] = None


def read_text(path: Path) -> List[str]:
    return path.read_text(encoding="utf-8", errors="ignore").splitlines()


def find_header_table(lines: List[str], max_scan: int = 80) -> Tuple[int, int]:
    """Return (row_count, first_row_line_no) within first max_scan lines."""
    row_count = 0
    first_row = 0
    for i, line in enumerate(lines[:max_scan], start=1):
        if RE_TABLE_ROW.match(line.strip()):
            row_count += 1
            if first_row == 0:
                first_row = i
    return row_count, first_row


def extract_tasks(lines: List[str]) -> Tuple[List[Tuple[int, str, str]], List[Issue]]:
    """Return list of (line_no, task_id, title) and issues."""
    issues: List[Issue] = []
    tasks: List[Tuple[int, str, str]] = []

    for i, line in enumerate(lines, start=1):
        m = RE_TASK_LINE.match(line)
        if not m:
            continue
        task_id = m.group("id")
        title = (m.group("title") or "").strip()
        if not title:
            issues.append(Issue("WARN", f"Task '{task_id}' has empty title", i))
        tasks.append((i, task_id, title))

    if not tasks:
        issues.append(Issue("ERROR", "No task checkbox lines found (expected '- [ ] TSK-...' lines)", None))

    return tasks, issues


def validate_evidence_nesting(lines: List[str]) -> List[Issue]:
    """Ensure evidence lines appear under a task (not at top-level wandering).

    Heuristic:
    - Evidence must occur AFTER at least one task line.
    - Evidence should be indented more than the task line.

    This validator does NOT validate evidence canonical tokens (done elsewhere).
    """
    issues: List[Issue] = []

    last_task_line_no: Optional[int] = None
    last_task_indent: Optional[int] = None

    for i, line in enumerate(lines, start=1):
        task_m = RE_TASK_LINE.match(line)
        if task_m:
            last_task_line_no = i
            last_task_indent = len(line) - len(line.lstrip(" "))
            continue

        if RE_EVIDENCE_LINE.match(line):
            if last_task_line_no is None:
                issues.append(Issue("ERROR", "Evidence line appears before any task", i))
                continue

            indent = len(line) - len(line.lstrip(" "))
            if last_task_indent is not None and indent <= last_task_indent:
                issues.append(
                    Issue(
                        "WARN",
                        "Evidence line is not indented under its task (recommended indent deeper than task bullet)",
                        i,
                    )
                )

    return issues


def validate_unique_ids(tasks: List[Tuple[int, str, str]]) -> List[Issue]:
    issues: List[Issue] = []
    seen: Dict[str, int] = {}
    for line_no, task_id, _ in tasks:
        if task_id in seen:
            issues.append(Issue("ERROR", f"Duplicate task ID: {task_id} (also at line {seen[task_id]})", line_no))
        else:
            seen[task_id] = line_no
    return issues


def validate_required_sections(lines: List[str]) -> List[Issue]:
    issues: List[Issue] = []

    if not any(RE_H1.match(l.strip()) for l in lines[:10]):
        issues.append(Issue("WARN", "Missing H1 title near top (# ...)", None))

    if not any(RE_SECTION_TASKS.match(l.strip()) for l in lines):
        issues.append(Issue("ERROR", "Missing required section header: '## Tasks'", None))

    row_count, first_row = find_header_table(lines)
    if row_count < 2:
        issues.append(Issue("ERROR", "Missing header table near top (expected at least 2 rows like '| Key | Value |')", first_row or None))

    return issues


def extract_spec_refs(lines: List[str]) -> Set[str]:
    refs: Set[str] = set()
    for line in lines:
        refs.update(RE_SPEC_REF.findall(line))
    return refs


def validate_spec_refs(tasks_lines: List[str], spec_path: Path) -> List[Issue]:
    issues: List[Issue] = []
    if not spec_path.exists():
        issues.append(Issue("ERROR", f"Spec file not found: {spec_path}", None))
        return issues

    spec_lines = read_text(spec_path)
    spec_refs = extract_spec_refs(spec_lines)
    task_refs = extract_spec_refs(tasks_lines)

    missing = sorted(r for r in task_refs if r not in spec_refs)
    if missing:
        # Warning (not error) because refs may intentionally point to other docs.
        issues.append(Issue("WARN", f"References in tasks not found in spec.md: {', '.join(missing[:120])}", None))
        if len(missing) > 120:
            issues.append(Issue("WARN", f"... plus {len(missing) - 120} more missing references", None))

    return issues


def print_issues(path: Path, issues: List[Issue]) -> None:
    errors = [i for i in issues if i.level == "ERROR"]
    warns = [i for i in issues if i.level == "WARN"]

    print("=" * 60)
    print("TASKS STRUCTURE VALIDATION")
    print("=" * 60)
    print(f"File: {path.as_posix()}")
    print(f"Errors: {len(errors)} | Warnings: {len(warns)}")
    print("=" * 60)

    for it in issues:
        loc = f" (line {it.line_no})" if it.line_no else ""
        print(f"{it.level}: {it.message}{loc}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate SmartSpec tasks.md structure (read-only)")
    ap.add_argument("tasks_file", help="Path to tasks.md")
    ap.add_argument("--spec", help="Optional spec.md path to check references", default=None)
    ap.add_argument("--json", action="store_true", help="Output JSON")
    ap.add_argument("--fail-on-warnings", action="store_true", help="Return non-zero if warnings exist")
    ap.add_argument("--quiet", action="store_true", help="Only print summary (or JSON)")
    args = ap.parse_args()

    tasks_path = Path(args.tasks_file)
    if not tasks_path.exists():
        print(f"ERROR: tasks file not found: {tasks_path}")
        return 2

    tasks_lines = read_text(tasks_path)

    issues: List[Issue] = []
    issues.extend(validate_required_sections(tasks_lines))

    tasks, task_issues = extract_tasks(tasks_lines)
    issues.extend(task_issues)

    if tasks:
        issues.extend(validate_unique_ids(tasks))

    issues.extend(validate_evidence_nesting(tasks_lines))

    if args.spec:
        issues.extend(validate_spec_refs(tasks_lines, Path(args.spec)))

    errors = [i for i in issues if i.level == "ERROR"]
    warns = [i for i in issues if i.level == "WARN"]

    if args.json:
        payload = {
            "file": tasks_path.as_posix(),
            "errors": [{"line": i.line_no, "message": i.message} for i in errors],
            "warnings": [{"line": i.line_no, "message": i.message} for i in warns],
            "counts": {"errors": len(errors), "warnings": len(warns)},
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        if not args.quiet:
            print_issues(tasks_path, issues)
        else:
            print(f"{tasks_path.as_posix()} :: errors={len(errors)} warnings={len(warns)}")

    if errors:
        return 1
    if args.fail_on_warnings and warns:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
