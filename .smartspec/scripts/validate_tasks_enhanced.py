#!/usr/bin/env python3
"""validate_tasks_enhanced.py (v2.0.0)

Validates structural correctness of a SmartSpec tasks.md file.

Checks (errors)
- Header metadata table exists near the top and starts with: `| spec-id |`
- Required section heading exists: `## Tasks`
- Task items are parseable: `- [ ] <TASK-ID> <title>` / `- [x] <TASK-ID> <title>`
- Task IDs are unique
- Each task block contains at least one `evidence:` hook line (anywhere in block)
- Evidence hooks are syntactically + semantically compatible with strict verifier

Checks (warnings)
- Missing traceability fields (implements:, t_ref:, acceptance:)

Important governance note
- This script NEVER writes or modifies tasks.md. It is validator-only.

Exit codes
- 0: valid (no errors)
- 1: invalid (one or more errors)
- 2: runtime error
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Keep in sync with validate_evidence_hooks.py
STRICT_TYPES = {"code", "test", "docs", "ui"}
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

RE_HEADER_TABLE = re.compile(r"^\|\s*spec-id\s*\|", re.IGNORECASE)
RE_TASK = re.compile(r"^\s*-\s*\[(?P<chk>[ xX])\]\s+(?P<id>[^\s]+)\s*(?P<title>.*)$")
RE_EVIDENCE = re.compile(r"evidence:\s*(.+)$", re.IGNORECASE)
RE_MD_CODE_FENCE = re.compile(r"^\s*```")


@dataclass
class TaskBlock:
    task_id: str
    title: str
    start_line: int
    end_line: int
    lines: List[str]


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


def _split_evidence_payload(payload: str) -> Tuple[Optional[str], Dict[str, str], List[str]]:
    """Lightweight parser: evidence: <type> key=value ...

    NOTE: We intentionally avoid shlex to keep this validator fast and dependency-free.
    This means we validate quoting only approximately; the strict verifier uses a robust parser.
    """

    issues: List[str] = []
    payload = payload.strip()
    if not payload:
        return None, {}, ["Empty evidence payload"]

    parts = payload.split()
    if not parts:
        return None, {}, ["Empty evidence payload"]

    hook_type = parts[0].lower()
    if hook_type not in STRICT_TYPES:
        issues.append(f"Unsupported evidence type '{hook_type}'")
        return hook_type, {}, issues

    kv: Dict[str, str] = {}
    for token in parts[1:]:
        if "=" not in token:
            issues.append(f"Stray token '{token}' (expected key=value)")
            continue
        k, v = token.split("=", 1)
        kv[k.strip()] = v.strip()

    # required keys
    if hook_type in {"code", "test", "docs"} and "path" not in kv:
        issues.append("Missing required key: path=")
    if hook_type == "ui" and "screen" not in kv:
        issues.append("Missing required key: screen=")

    # placeholders
    for k, v in kv.items():
        if "???" in v or "TODO" in v.upper():
            issues.append(f"Placeholder detected in {k}={v!r}")

    # path semantics
    if "path" in kv:
        p = kv["path"].strip().strip('"')
        if _is_abs_or_traversal(p):
            issues.append("path must be repo-relative and must not contain '..' or be absolute")
        if _looks_like_glob(p):
            issues.append("glob patterns are not allowed in path=")
        if _first_segment(p) in SUSPICIOUS_PATH_PREFIXES:
            issues.append("path looks like a command; use command= with an anchor file path")

    # type-key mismatch
    if hook_type == "code" and "heading" in kv:
        issues.append("code must not use heading=; use docs ... heading=\"...\"")

    return hook_type, kv, issues


def find_header_table_line(lines: List[str], max_lines: int = 25) -> Optional[int]:
    for i, line in enumerate(lines[:max_lines], start=1):
        if RE_HEADER_TABLE.match(line.strip()):
            return i
    return None


def split_task_blocks(lines: List[str]) -> List[TaskBlock]:
    tasks: List[TaskBlock] = []

    indices: List[Tuple[int, re.Match]] = []
    for i, line in enumerate(lines, start=1):
        m = RE_TASK.match(line)
        if m:
            indices.append((i, m))

    for idx, (start_line, m) in enumerate(indices):
        end_line = (indices[idx + 1][0] - 1) if idx + 1 < len(indices) else len(lines)
        task_id = m.group("id").strip()
        title = (m.group("title") or "").strip()
        block_lines = lines[start_line - 1 : end_line]
        tasks.append(TaskBlock(task_id=task_id, title=title, start_line=start_line, end_line=end_line, lines=block_lines))

    return tasks


def extract_evidence_payloads(block: TaskBlock) -> List[Tuple[int, str]]:
    payloads: List[Tuple[int, str]] = []
    in_fence = False

    for offset, line in enumerate(block.lines):
        line_no = block.start_line + offset
        if RE_MD_CODE_FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        m = RE_EVIDENCE.search(line)
        if not m:
            continue
        payloads.append((line_no, m.group(1).strip()))

    return payloads


def validate_tasks_md(tasks_path: Path) -> Dict:
    content = tasks_path.read_text(encoding="utf-8", errors="ignore")
    lines = content.splitlines()

    errors: List[str] = []
    warnings: List[str] = []

    header_line = find_header_table_line(lines)
    if header_line is None:
        errors.append("Missing header table (expected a table starting with '| spec-id |' within top 25 lines).")

    if not any(line.strip() == "## Tasks" for line in lines):
        errors.append("Missing required section heading: '## Tasks'.")

    tasks = split_task_blocks(lines)
    if not tasks:
        errors.append("No task items found. Expected '- [ ] <TASK-ID> <title>' lines under '## Tasks'.")

    # Unique IDs
    seen: Dict[str, int] = {}
    for t in tasks:
        if t.task_id in seen:
            errors.append(f"Duplicate task id '{t.task_id}' (line {t.start_line}, previously at line {seen[t.task_id]}).")
        else:
            seen[t.task_id] = t.start_line

    # Per-task evidence validation
    invalid_hooks = 0
    total_hooks = 0

    for t in tasks:
        payloads = extract_evidence_payloads(t)
        if not payloads:
            errors.append(f"Task '{t.task_id}' (line {t.start_line}) has no evidence hooks. Add at least one 'evidence:' line.")
            continue

        # optional traceability
        joined = "\n".join(t.lines)
        if "implements:" not in joined:
            warnings.append(f"Task '{t.task_id}' missing 'implements:' (line {t.start_line}).")
        if "t_ref:" not in joined:
            warnings.append(f"Task '{t.task_id}' missing 't_ref:' (line {t.start_line}).")
        if "acceptance:" not in joined:
            warnings.append(f"Task '{t.task_id}' missing 'acceptance:' (line {t.start_line}).")

        for line_no, payload in payloads:
            total_hooks += 1
            _type, _kv, hook_issues = _split_evidence_payload(payload)
            if hook_issues:
                invalid_hooks += 1
                errors.append(
                    f"Invalid evidence hook at task '{t.task_id}' (line {line_no}): {payload} :: " + "; ".join(hook_issues)
                )

    result = {
        "file": str(tasks_path),
        "valid": len(errors) == 0,
        "task_count": len(tasks),
        "evidence_hooks": {
            "total": total_hooks,
            "invalid": invalid_hooks,
            "valid": total_hooks - invalid_hooks,
        },
        "errors": errors,
        "warnings": warnings,
    }

    return result


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Validate SmartSpec tasks.md structure + evidence hooks")
    ap.add_argument("--tasks", required=True, help="Path to tasks.md")
    ap.add_argument("--json", action="store_true", help="Output JSON")

    args = ap.parse_args(argv)

    tasks_path = Path(args.tasks)
    if not tasks_path.exists():
        print(f"❌ tasks file not found: {tasks_path}", file=sys.stderr)
        return 2

    try:
        result = validate_tasks_md(tasks_path)
    except Exception as e:
        print(f"❌ validation error: {e}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # Human output similar to earlier reports
        status = "PASSED" if result["valid"] else "FAILED"
        print(f"# validate_tasks_enhanced report")
        print(f"\nFile: {result['file']}")
        print(f"Status: {status}")
        print(f"Tasks: {result['task_count']}")
        eh = result["evidence_hooks"]
        print(f"Evidence hooks: {eh['valid']}/{eh['total']} valid")
        if result["errors"]:
            print("\nErrors:")
            for e in result["errors"][:200]:
                print(f"- {e}")
            if len(result["errors"]) > 200:
                print(f"- ... truncated ({len(result['errors']) - 200} more)")
        if result["warnings"]:
            print("\nWarnings:")
            for w in result["warnings"][:200]:
                print(f"- {w}")
            if len(result["warnings"]) > 200:
                print(f"- ... truncated ({len(result['warnings']) - 200} more)")

    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
