#!/usr/bin/env python3
"""validate_tasks_enhanced.py (v2.2.0)

Enhanced structural validator for SmartSpec `tasks.md`.

Design goals
- Validator-only: MUST NOT modify any files.
- Compatible with SmartSpec preview-first governance.
- Catch the most common causes of verify false-negatives:
  - missing / malformed header table
  - missing `## Tasks`
  - tasks without evidence hooks
  - duplicate task IDs
  - evidence hooks present but syntactically invalid

What this validates (errors)
1) A header table exists near the top (default: within first 80 lines).
   Accepts either:
   - canonical 2-column table: `| Key | Value |` (recommended)
   - legacy 2-column: `| spec-id | ... |` (accepted, with warning)
2) A `## Tasks` heading exists.
3) Task lines exist and are parseable:
   - `- [ ] <TASK-ID> <title>`
   - `- [x] <TASK-ID> <title>`
4) Task IDs are unique.
5) Each task block contains at least one evidence hook line (anywhere in block):
   - `evidence: ...`
   - `- evidence: ...`
   - `| ... evidence: ... |` (table cell)
6) Evidence hooks are syntactically valid per canonical parser.

What this validates (warnings)
- Header table uses legacy form.
- Tasks missing optional traceability fields (implements:, t_ref:, acceptance:).
- Evidence hooks have no matcher keys (may be weak).

Exit codes
- 0: valid (no errors)
- 1: invalid (one or more errors)
- 2: runtime / usage error
"""

from __future__ import annotations

import argparse
import json
import re
import shlex
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple


# ---------- Evidence hook parsing (kept consistent with validate_evidence_hooks.py) ----------

STRICT_TYPES = {"code", "test", "docs", "ui"}

ALLOWED_KEYS: Dict[str, set[str]] = {
    "code": {"path", "symbol", "contains", "regex"},
    "test": {"path", "command", "contains", "regex"},
    "docs": {"path", "heading", "contains", "regex"},
    "ui": {"path", "selector", "contains", "regex"},
}

MATCHER_KEYS = {"contains", "symbol", "heading", "selector", "regex", "command"}

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

RE_EVIDENCE_ANYWHERE = re.compile(r"evidence:\s*(?P<payload>.+)$", re.IGNORECASE)
RE_MD_CODE_FENCE = re.compile(r"^\s*```")


@dataclass
class EvidenceIssue:
    code: str
    message: str


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
    return any(ch in p for ch in ("*", "?", "[", "]"))


def _parse_evidence_payload(payload: str) -> Tuple[Optional[str], Dict[str, str], List[EvidenceIssue]]:
    issues: List[EvidenceIssue] = []

    payload = payload.strip()
    if not payload:
        return None, {}, [EvidenceIssue("empty_payload", "Evidence payload is empty")]

    try:
        tokens = shlex.split(payload, posix=True)
    except Exception as e:
        return None, {}, [EvidenceIssue("shlex_error", f"Unable to parse evidence payload: {e}")]

    if not tokens:
        return None, {}, [EvidenceIssue("empty_payload", "Evidence payload is empty")]

    hook_type = tokens[0].strip().lower()
    if hook_type not in STRICT_TYPES:
        issues.append(
            EvidenceIssue(
                "invalid_type",
                f"Unsupported evidence type '{tokens[0]}'. Allowed: {sorted(STRICT_TYPES)}",
            )
        )
        return hook_type, {}, issues

    kv: Dict[str, str] = {}
    for t in tokens[1:]:
        if "=" not in t:
            issues.append(
                EvidenceIssue(
                    "stray_token",
                    f"Stray token not allowed (quote values with spaces). Token: '{t}'",
                )
            )
            continue
        k, v = t.split("=", 1)
        k = k.strip()
        v = v.strip()
        if not k:
            issues.append(EvidenceIssue("bad_key", f"Empty key in token '{t}'"))
            continue
        if k in kv:
            issues.append(EvidenceIssue("dup_key", f"Duplicate key '{k}'"))
            continue
        kv[k] = v

    # key allowlist
    allowed = ALLOWED_KEYS[hook_type]
    for k in kv.keys():
        if k not in allowed:
            issues.append(
                EvidenceIssue(
                    "bad_key",
                    f"Key '{k}' not allowed for type '{hook_type}'. Allowed: {sorted(allowed)}",
                )
            )

    # required path
    if "path" not in kv or not kv.get("path", "").strip():
        issues.append(EvidenceIssue("missing_path", "Missing required key: path=<repo-relative-path>"))
        return hook_type, kv, issues

    path_val = kv["path"].strip().strip('"')

    # path safety
    if _is_absolute_or_traversal(path_val):
        issues.append(EvidenceIssue("unsafe_path", f"Path must be repo-relative and must not traverse: path={kv['path']}"))

    if _contains_glob(path_val):
        issues.append(EvidenceIssue("glob_path", f"Glob patterns are not allowed in path=: {kv['path']}"))

    first = path_val.split("/", 1)[0].strip().lower()
    if first in SUSPICIOUS_PATH_PREFIXES:
        issues.append(
            EvidenceIssue(
                "suspicious_path",
                f"path= looks like a command prefix ('{first}'). Use: evidence: test path=<anchor> command=\"...\"",
            )
        )

    return hook_type, kv, issues


# ---------- Tasks parsing ----------

RE_TASK_LINE = re.compile(
    r"^\s*-\s*\[(?P<chk>[ xX])\]\s+(?P<id>[A-Za-z0-9][A-Za-z0-9._:-]*)\s*(?P<title>.*)$"
)

RE_HEADER_CANON = re.compile(r"^\|\s*key\s*\|\s*value\s*\|\s*$", re.IGNORECASE)
RE_HEADER_LEGACY = re.compile(r"^\|\s*spec-id\s*\|", re.IGNORECASE)


@dataclass
class TaskBlock:
    task_id: str
    title: str
    start_line: int
    end_line: int
    lines: List[str]


def _find_header_table(lines: List[str], search_limit: int) -> Tuple[Optional[int], Optional[str]]:
    """Returns (line_no, kind) where kind is 'canon' | 'legacy'."""
    for i, line in enumerate(lines[:search_limit], start=1):
        s = line.strip()
        if RE_HEADER_CANON.match(s):
            return i, "canon"
        if RE_HEADER_LEGACY.match(s):
            return i, "legacy"
    return None, None


def _has_tasks_heading(lines: List[str]) -> bool:
    return any(line.strip() == "## Tasks" for line in lines)


def _split_task_blocks(lines: List[str]) -> List[TaskBlock]:
    indices: List[Tuple[int, re.Match]] = []
    for i, line in enumerate(lines, start=1):
        m = RE_TASK_LINE.match(line)
        if m:
            indices.append((i, m))

    blocks: List[TaskBlock] = []
    for idx, (start, m) in enumerate(indices):
        end = (indices[idx + 1][0] - 1) if idx + 1 < len(indices) else len(lines)
        task_id = m.group("id").strip()
        title = (m.group("title") or "").strip()
        block_lines = lines[start - 1 : end]
        blocks.append(TaskBlock(task_id=task_id, title=title, start_line=start, end_line=end, lines=block_lines))

    return blocks


def _extract_evidence_from_block(block: TaskBlock) -> List[Tuple[int, str]]:
    """Extract evidence payloads from a task block.

    Evidence can appear as:
    - plain line: `evidence: ...`
    - bullet: `- evidence: ...`
    - in table cell: `| ... evidence: ... |`

    We skip fenced code blocks.
    """

    payloads: List[Tuple[int, str]] = []
    in_fence = False

    for offset, line in enumerate(block.lines):
        line_no = block.start_line + offset
        if RE_MD_CODE_FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        m = RE_EVIDENCE_ANYWHERE.search(line)
        if not m:
            continue
        payload = m.group("payload").strip()
        payloads.append((line_no, payload))

    return payloads


def validate_tasks_md(
    tasks_path: Path,
    header_search_limit: int = 80,
    require_traceability: bool = False,
) -> Dict:
    text = tasks_path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()

    errors: List[str] = []
    warnings: List[str] = []

    header_line, header_kind = _find_header_table(lines, search_limit=header_search_limit)
    if header_line is None:
        errors.append(
            f"Missing header table within first {header_search_limit} lines. Expected '| Key | Value |' (recommended) or legacy '| spec-id | ... |'."
        )
    elif header_kind == "legacy":
        warnings.append(f"Header table is legacy format (line {header_line}). Prefer canonical '| Key | Value |'.")

    if not _has_tasks_heading(lines):
        errors.append("Missing required heading: '## Tasks'.")

    blocks = _split_task_blocks(lines)
    if not blocks:
        errors.append("No tasks found. Expected lines like '- [ ] <TASK-ID> <title>' under '## Tasks'.")

    # duplicate IDs
    seen: Dict[str, int] = {}
    for b in blocks:
        if b.task_id in seen:
            errors.append(
                f"Duplicate task id '{b.task_id}' at line {b.start_line} (previously at line {seen[b.task_id]})."
            )
        else:
            seen[b.task_id] = b.start_line

    total_hooks = 0
    invalid_hooks = 0
    hooks_with_warnings = 0

    for b in blocks:
        payloads = _extract_evidence_from_block(b)
        if not payloads:
            errors.append(
                f"Task '{b.task_id}' (line {b.start_line}) has no evidence hooks. Add at least one 'evidence:' line."
            )
        else:
            for line_no, payload in payloads:
                total_hooks += 1
                ht, kv, hook_issues = _parse_evidence_payload(payload)
                if hook_issues:
                    invalid_hooks += 1
                    errors.append(
                        f"Invalid evidence hook at task '{b.task_id}' (line {line_no}): {payload} :: "
                        + "; ".join(i.message for i in hook_issues)
                    )
                    continue

                if not any(k in kv for k in MATCHER_KEYS):
                    hooks_with_warnings += 1
                    warnings.append(
                        f"Weak evidence (no matcher) at task '{b.task_id}' (line {line_no}): {payload}"
                    )

        # traceability fields (optional)
        joined = "\n".join(b.lines)
        miss = []
        if "implements:" not in joined:
            miss.append("implements")
        if "t_ref:" not in joined:
            miss.append("t_ref")
        if "acceptance:" not in joined:
            miss.append("acceptance")

        if miss:
            msg = f"Task '{b.task_id}' missing traceability fields: {', '.join(miss)} (line {b.start_line})."
            if require_traceability:
                errors.append(msg)
            else:
                warnings.append(msg)

    result = {
        "file": str(tasks_path),
        "valid": len(errors) == 0,
        "summary": {
            "task_count": len(blocks),
            "evidence_hooks": {
                "total": total_hooks,
                "invalid": invalid_hooks,
                "valid": total_hooks - invalid_hooks,
                "with_warnings": hooks_with_warnings,
            },
        },
        "errors": errors,
        "warnings": warnings,
    }

    return result


def _render_human(result: Dict, max_items: int = 250) -> str:
    out: List[str] = []
    out.append("=" * 60)
    out.append("TASKS STRUCTURE VALIDATION REPORT")
    out.append("=" * 60)
    out.append(f"File: {result['file']}")

    s = result["summary"]
    eh = s["evidence_hooks"]
    out.append("")
    out.append("Summary:")
    out.append(f"  Tasks: {s['task_count']}")
    out.append(f"  Evidence hooks: {eh['valid']}/{eh['total']} valid")
    out.append(f"  Evidence hooks with warnings: {eh['with_warnings']}")

    if result["errors"]:
        out.append("")
        out.append("Errors:")
        for e in result["errors"][:max_items]:
            out.append(f"  - {e}")
        if len(result["errors"]) > max_items:
            out.append(f"  - ... truncated ({len(result['errors']) - max_items} more)")

    if result["warnings"]:
        out.append("")
        out.append("Warnings:")
        for w in result["warnings"][:max_items]:
            out.append(f"  - {w}")
        if len(result["warnings"]) > max_items:
            out.append(f"  - ... truncated ({len(result['warnings']) - max_items} more)")

    out.append("")
    return "\n".join(out)


def _parse_args(argv: Sequence[str]) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Validate SmartSpec tasks.md structure and evidence hooks")

    # Compatibility: accept either positional or --tasks.
    ap.add_argument("tasks", nargs="?", help="Path to tasks.md (positional)")
    ap.add_argument("--tasks", dest="tasks_flag", help="Path to tasks.md")

    ap.add_argument("--header-search-limit", type=int, default=80, help="Search header table within first N lines (default: 80)")
    ap.add_argument("--require-traceability", action="store_true", help="Treat missing implements/t_ref/acceptance as errors")
    ap.add_argument("--json", action="store_true", help="Output JSON")
    ap.add_argument("--out", default=None, help="Optional directory to write report.json")
    ap.add_argument("--max-items", type=int, default=250, help="Max items to print (default: 250)")
    ap.add_argument("--quiet", action="store_true", help="No stdout report")
    ap.add_argument("--version", action="store_true", help="Print version and exit")

    args = ap.parse_args(list(argv))
    if args.version:
        print("validate_tasks_enhanced.py v2.2.0")
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

    try:
        result = validate_tasks_md(
            args.tasks_path,
            header_search_limit=args.header_search_limit,
            require_traceability=args.require_traceability,
        )
    except Exception as e:
        print(f"❌ validation error: {e}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif not args.quiet:
        print(_render_human(result, max_items=args.max_items))

    if args.out:
        out_dir = Path(args.out)
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "tasks-structure-report.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
