#!/usr/bin/env python3
"""Normalize evidence hooks in tasks.md so validation passes.

Fixes:
1) `evidence: test command="..."`  -> add `path=<inferred or .>`
2) `evidence: test ... symbol=Directory` -> remove that key/value

Inference strategy (per task block):
- Find the first evidence path in the task block: `evidence: (code|test) ... path=...`
- Collapse it to a stable directory (keeps monorepo package/app root when possible)
- Use that as default path for test commands missing path
- If nothing can be inferred: path=.

Usage:
  python normalize_evidence_hooks.py <tasks.md> --in-place
  python normalize_evidence_hooks.py <tasks.md> --stdout
  python normalize_evidence_hooks.py <tasks.md> --check
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path, PurePosixPath

EVIDENCE_PATH_RE = re.compile(r"\bevidence:\s*(?:code|test)\s+[^\n]*?\bpath=([^\s]+)")
TEST_EVIDENCE_RE = re.compile(r"^(?P<prefix>\s*evidence:\s*test)(?P<body>\s+.*)$", re.IGNORECASE)


def _collapse_to_repo_root(path_str: str) -> str:
    """Heuristic: reduce a file path to a stable directory for running commands.

    Examples:
      packages/auth-lib/src/index.ts -> packages/auth-lib/
      apps/web/app/page.tsx         -> apps/web/
      auth-service/README.md        -> auth-service/
      ./                             -> .
    """
    p = path_str.strip().rstrip("/")
    if p in {".", "./"}:
        return "."

    parts = PurePosixPath(p).parts
    if not parts:
        return "."

    # Monorepo conventions: keep 2 segments
    if parts[0] in {"packages", "apps", "services", "libs"} and len(parts) >= 2:
        return f"{parts[0]}/{parts[1]}/"

    # If path is nested, keep the top folder
    return f"{parts[0]}/"


def _infer_default_path(task_lines: list[str]) -> str:
    # Prefer explicit evidence path in the same task block
    for line in task_lines:
        m = EVIDENCE_PATH_RE.search(line)
        if m:
            return _collapse_to_repo_root(m.group(1))

    # Fallback: any mention of common monorepo dirs
    for line in task_lines:
        m = re.search(r"\b(packages|apps|services|libs)/([A-Za-z0-9._-]+)/", line)
        if m:
            return f"{m.group(1)}/{m.group(2)}/"

    return "."


def _split_into_task_blocks(lines: list[str]) -> list[list[str]]:
    """Split markdown into blocks starting at task headings (best-effort).

    Keeps preamble (before first task) as its own block.
    """
    blocks: list[list[str]] = []
    current: list[str] = []

    def flush() -> None:
        nonlocal current
        if current:
            blocks.append(current)
            current = []

    header_re = re.compile(r"^##\s+\[[ xX]\]\s+TSK-|^##\s+TSK-", re.IGNORECASE)

    for line in lines:
        if header_re.match(line):
            flush()
        current.append(line)

    flush()
    return blocks


def _normalize_task_block(task_lines: list[str]) -> tuple[list[str], int]:
    edits = 0
    default_path = _infer_default_path(task_lines)
    out: list[str] = []

    for line in task_lines:
        # Remove symbol=Directory only for evidence: test lines
        if line.lstrip().lower().startswith("evidence: test") and "symbol=Directory" in line:
            new_line = re.sub(r"\s+symbol=Directory\b", "", line)
            if new_line != line:
                edits += 1
            line = new_line

        # Add missing path= for evidence: test lines that have command= but no path=
        m = TEST_EVIDENCE_RE.match(line)
        if m:
            body = m.group("body")
            has_command = "command=" in body
            has_path = re.search(r"\bpath=", body) is not None
            if has_command and not has_path:
                prefix = m.group("prefix")
                new_line = f"{prefix} path={default_path}{body}"
                # Normalize whitespace and ensure newline
                new_line = re.sub(r"\s+", " ", new_line).rstrip() + "\n"
                edits += 1
                out.append(new_line)
                continue

        out.append(line)

    return out, edits


def normalize_text(text: str) -> tuple[str, int]:
    lines = text.splitlines(keepends=True)
    blocks = _split_into_task_blocks(lines)

    total_edits = 0
    out_lines: list[str] = []

    for block in blocks:
        normalized, edits = _normalize_task_block(block)
        total_edits += edits
        out_lines.extend(normalized)

    return "".join(out_lines), total_edits


def main() -> int:
    ap = argparse.ArgumentParser(description="Normalize evidence hooks in SmartSpec tasks.md")
    ap.add_argument("tasks_path", help="Path to tasks.md to normalize")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--in-place", action="store_true", help="Rewrite the file in place")
    g.add_argument("--stdout", action="store_true", help="Print normalized output to stdout")
    g.add_argument("--check", action="store_true", help="Exit non-zero if changes would be made")
    args = ap.parse_args()

    try:
        original = Path(args.tasks_path).read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"ERROR: file not found: {args.tasks_path}", file=sys.stderr)
        return 2

    normalized, edits = normalize_text(original)

    if args.check:
        if edits > 0:
            print(f"normalize_evidence_hooks: would apply {edits} edits", file=sys.stderr)
            return 1
        print("normalize_evidence_hooks: no changes needed")
        return 0

    if args.stdout:
        sys.stdout.write(normalized)
        return 0

    # --in-place
    if normalized != original:
        Path(args.tasks_path).write_text(normalized, encoding="utf-8")
    print(f"normalize_evidence_hooks: applied {edits} edits to {args.tasks_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
