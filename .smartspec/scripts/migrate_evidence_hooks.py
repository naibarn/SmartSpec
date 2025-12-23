#!/usr/bin/env python3
"""SmartSpec Evidence Hook Migration (v6.4.1)

This script upgrades legacy/descriptive evidence into strict-verifier-compatible hooks.

Primary target compatibility:
  - /smartspec_verify_tasks_progress_strict
  - evidence types must be one of: code|test|docs|ui

Design goals
------------
- Preview-first (default): show what would change without modifying tasks.md
- Apply mode (--apply): rewrite tasks.md in-place (atomic) to standardized evidence lines
- Preserve formatting where possible (indent, bullets, tables)
- Avoid false evidence: only auto-convert when we can extract a plausible repo-relative path

NOTE
----
The official workflow may use an AI model for higher-fidelity conversion.
This script implements safe heuristics so you always get deterministic migrations.

"""

from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import shutil
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


VALID_TYPES = {"code", "test", "docs", "ui"}


_TASK_RE = re.compile(r"^\s*-\s*\[[ xX]\]\s+(\S+)(?:\s+.*)?$")

# Detect evidence blocks and legacy patterns
_EVIDENCE_INLINE_RE = re.compile(r"(?i)\bevidence\s*:\s*(.+)$")
_LEGACY_TYPES = {
    "file_exists",
    "file_contains",
    "test_exists",
    "command",
    "api_route",
    "db_schema",
    "gh_commit",
}

# Path-ish tokens often present in descriptive evidence
_PATH_TOKEN_RE = re.compile(
    r"(?P<path>(?:[a-zA-Z0-9_\-]+/)*[a-zA-Z0-9_\-]+\.(?:ts|tsx|js|jsx|py|go|rs|java|kt|cs|rb|php|md|yaml|yml|json|toml|sql|prisma))"
)

_ROUTE_RE = re.compile(r"(?P<route>/[a-zA-Z0-9_\-/]+)")


@dataclass
class Replacement:
    line_no: int
    original: str
    updated: str


def _read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="ignore")


def _write_atomic(path: Path, content: str) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    tmp.replace(path)


def _guess_strict_type_from_path(path: str) -> str:
    low = path.lower()
    if "/test" in low or low.endswith((".spec.ts", ".test.ts", ".spec.js", ".test.js")):
        return "test"
    if low.endswith((".md", ".rst")):
        return "docs"
    return "code"


def _normalize_evidence_line(raw: str) -> Optional[str]:
    """Return canonical 'evidence: <type> key=value ...' or None if cannot normalize."""

    raw = raw.strip()

    # Support lines like:
    # - evidence: ...
    # evidence: ...
    # | **Evidence:** evidence: ... |
    m = _EVIDENCE_INLINE_RE.search(raw)
    if not m:
        return None

    payload = m.group(1).strip().rstrip("|").strip()

    # If payload already starts with strict types, keep it
    parts = payload.split()
    if not parts:
        return None

    first = parts[0]

    # If already strict type
    if first in VALID_TYPES:
        return f"evidence: {payload}"

    # Legacy hook style like: file_exists path=...
    if first in _LEGACY_TYPES:
        # Try to map to strict types
        # Prefer existing path=... token
        path_m = re.search(r"\bpath=(\S+)", payload)
        if path_m:
            p = path_m.group(1).strip('"\'')
            strict_t = _guess_strict_type_from_path(p)
            # Map file_exists/test_exists to just existence (medium in verifier)
            if first in {"file_exists", "test_exists"}:
                if strict_t == "test":
                    return f"evidence: test path={p}"
                if strict_t == "docs":
                    return f"evidence: docs path={p}"
                return f"evidence: code path={p}"

            # Map file_contains to contains
            if first == "file_contains":
                content_m = re.search(r"\b(content|contains)=([^\n]+)$", payload)
                contains_val = None
                if content_m:
                    contains_val = content_m.group(2).strip().strip('"\'')
                if strict_t == "test":
                    if contains_val:
                        return f"evidence: test path={p} contains=\"{contains_val}\""
                    return f"evidence: test path={p}"
                if strict_t == "docs":
                    if contains_val:
                        return f"evidence: docs path={p} contains=\"{contains_val}\""
                    return f"evidence: docs path={p}"
                if contains_val:
                    return f"evidence: code path={p} contains=\"{contains_val}\""
                return f"evidence: code path={p}"

            # Map api_route/db_schema to code contains
            if first in {"api_route", "db_schema"}:
                # route=/foo or model=User etc.
                if first == "api_route":
                    r_m = re.search(r"\b(route|path_route)=([^\s]+)", payload)
                    if r_m:
                        rv = r_m.group(2).strip().strip('"\'')
                        return f"evidence: code path={p} contains=\"{rv}\""
                if first == "db_schema":
                    mdl_m = re.search(r"\b(model|table)=([^\s]+)", payload)
                    if mdl_m:
                        mv = mdl_m.group(2).strip().strip('"\'')
                        return f"evidence: code path={p} contains=\"{mv}\""
                return f"evidence: code path={p}"

        # If no path=, attempt to extract a path-like token
        p2 = _PATH_TOKEN_RE.search(payload)
        if p2:
            p = p2.group("path")
            strict_t = _guess_strict_type_from_path(p)
            if strict_t == "test":
                return f"evidence: test path={p}"
            if strict_t == "docs":
                return f"evidence: docs path={p}"
            return f"evidence: code path={p}"

        return None

    # If payload is free text, attempt heuristic extraction
    p = _PATH_TOKEN_RE.search(payload)
    if not p:
        return None

    path = p.group("path")
    strict_t = _guess_strict_type_from_path(path)

    # If a route is mentioned, add contains
    route_m = _ROUTE_RE.search(payload)
    if route_m and strict_t == "code":
        route = route_m.group("route")
        return f"evidence: code path={path} contains=\"{route}\""

    if strict_t == "test":
        return f"evidence: test path={path}"
    if strict_t == "docs":
        return f"evidence: docs path={path}"
    return f"evidence: code path={path}"


def _preserve_prefix(original_line: str) -> Tuple[str, str, str]:
    """Return (leading_ws, bullet_prefix, core_text)

    bullet_prefix includes '- ' if present.
    """
    m = re.match(r"^(\s*)(-\s+)?(.*)$", original_line)
    if not m:
        return "", "", original_line
    return m.group(1) or "", m.group(2) or "", m.group(3) or ""


def migrate_tasks_text(tasks_text: str) -> Tuple[str, List[Replacement]]:
    lines = tasks_text.splitlines(True)
    reps: List[Replacement] = []

    for i, line in enumerate(lines):
        if "evidence" not in line.lower():
            continue

        normalized = _normalize_evidence_line(line)
        if not normalized:
            continue

        lead, bullet, _ = _preserve_prefix(line.rstrip("\n"))

        # Keep table rows intact: if line starts with '|', don't force bullet
        if line.lstrip().startswith("|"):
            # Replace only the evidence substring inside the row, keep other cells
            low = line.lower()
            pos = low.find("evidence:")
            if pos >= 0:
                prefix = line[:pos]
                suffix = "\n" if line.endswith("\n") else ""
                new_line = prefix + normalized + suffix
            else:
                new_line = line
        else:
            # Use same bullet marker style as original
            prefix = f"{lead}{bullet}" if bullet else f"{lead}"
            new_line = f"{prefix}{normalized}\n"

        if new_line != line:
            reps.append(Replacement(line_no=i + 1, original=line.rstrip("\n"), updated=new_line.rstrip("\n")))
            lines[i] = new_line

    return "".join(lines), reps


def make_diff(old: str, new: str, filename: str) -> str:
    return "".join(
        difflib.unified_diff(
            old.splitlines(True),
            new.splitlines(True),
            fromfile=f"a/{filename}",
            tofile=f"b/{filename}",
        )
    )


def main() -> int:
    ap = argparse.ArgumentParser(description="Migrate tasks.md evidence to strict-verifier-compatible evidence hooks")
    ap.add_argument("--tasks-file", required=True, help="Path to tasks.md")
    ap.add_argument("--apply", action="store_true", help="Apply changes to tasks.md (default: preview)")
    ap.add_argument("--model", default="gpt-4.1-mini", help="(Workflow) AI model name for conversion")
    ap.add_argument("--out", default=".spec/reports/migrate-evidence-hooks", help="Output root for preview artifacts")
    ap.add_argument("--json", action="store_true", help="Write summary.json")
    ap.add_argument("--quiet", action="store_true", help="Reduce logs")

    args = ap.parse_args()

    tasks_path = Path(args.tasks_file).resolve()
    if not tasks_path.exists():
        print(f"ERROR: tasks file not found: {tasks_path}", file=sys.stderr)
        return 2

    old_text = _read_text(tasks_path)
    new_text, reps = migrate_tasks_text(old_text)

    run_id = datetime.now().strftime("migrate_%Y%m%d_%H%M%S")
    out_root = Path(args.out).resolve() if Path(args.out).is_absolute() else (Path(".") / args.out).resolve()
    run_dir = out_root / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    diff_text = make_diff(old_text, new_text, tasks_path.as_posix())
    (run_dir / "preview.diff").write_text(diff_text, encoding="utf-8")

    summary = {
        "workflow": "smartspec_migrate_evidence_hooks",
        "version": "6.4.1",
        "run_id": run_id,
        "generated_at": datetime.now().isoformat(),
        "inputs": {"tasks_file": str(tasks_path), "apply": bool(args.apply), "model": args.model},
        "changes": [{"line": r.line_no, "from": r.original, "to": r.updated} for r in reps],
        "counts": {"replacements": len(reps)},
        "writes": {
            "reports": [str(run_dir / "preview.diff")] + ([str(run_dir / "summary.json")] if args.json else [])
        },
    }

    if args.json:
        (run_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    if not reps:
        if not args.quiet:
            print("No changes suggested.")
        return 0

    if not args.quiet:
        print(f"Suggested replacements: {len(reps)}")
        print(f"Preview diff: {run_dir / 'preview.diff'}")

    if not args.apply:
        return 0

    # Apply: backup then atomic write
    backup = tasks_path.with_suffix(tasks_path.suffix + f".backup.{run_id}")
    shutil.copy2(tasks_path, backup)

    _write_atomic(tasks_path, new_text)

    if not args.quiet:
        print(f"Applied changes. Backup: {backup}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
