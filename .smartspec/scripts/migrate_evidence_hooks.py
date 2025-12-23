#!/usr/bin/env python3
"""migrate_evidence_hooks.py (v6.4.3)

Deterministically migrate/normalize evidence in SmartSpec tasks.md into strict evidence hooks.

Key goals
---------
- Convert legacy blocks (Evidence Hooks / Evidence / Code: bullets) into `evidence:` lines.
- Fix known strict-verifier false-negative patterns:
  - unparseable evidence due to unescaped quotes / multi-token values
  - contains=exists placeholder
  - glob paths in path=
  - heading= on non-docs

Safety & governance
-------------------
- Default is preview: write outputs under `.spec/reports/migrate-evidence-hooks/<run-id>/...` only.
- Writes to `specs/**/tasks.md` require --apply.
- Atomic write on apply (temp + replace).

Usage
-----
  python3 migrate_evidence_hooks.py --tasks-file specs/<cat>/<spec-id>/tasks.md [--apply]

This script does not depend on network.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import difflib
import os
import re
import shlex
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple


RE_TASK_LINE = re.compile(r"^(?P<indent>\s*)-\s*\[[ xX]\]\s+(?P<id>\S+)\s+.*$")
RE_EVIDENCE_LINE = re.compile(r"^(?P<indent>\s*)evidence:\s+(?P<payload>.*)$", re.IGNORECASE)

RE_LEGACY_HOOKS_HEADER = re.compile(r"^\s*(\*\*\s*)?Evidence Hooks(\s*\*\*)?\s*:\s*$", re.IGNORECASE)
RE_LEGACY_EVIDENCE_HEADER = re.compile(r"^\s*(\*\*\s*)?Evidence(\s*\*\*)?\s*:\s*(?P<body>.*)$", re.IGNORECASE)
RE_LEGACY_BULLET = re.compile(r"^\s*[-*]\s*(?P<kind>Code|Test|Docs|UI)\s*:\s*(?P<body>.+)$", re.IGNORECASE)

# Best-effort path extract
RE_PATH = re.compile(r"\bpath\s*=\s*(?P<p>[^\s]+)")
RE_QUOTED = re.compile(r"\"([^\"]*)\"|'([^']*)'")


def _run_id() -> str:
    return _dt.datetime.utcnow().strftime("%Y%m%d_%H%M%S")


def _is_tasks_md_path(p: Path) -> bool:
    s = str(p).replace("\\", "/")
    return s.endswith("tasks.md") and "/specs/" in f"/{s.strip('/')}/"


def _normalize_path_token(p: str) -> str:
    p = (p or "").strip().strip('"\'')
    p = p.replace("\\", "/")
    if p.startswith("./"):
        p = p[2:]
    p = re.sub(r"/{2,}", "/", p)
    return p


def _has_glob(p: str) -> bool:
    return any(ch in p for ch in ["*", "?", "[", "]"])


def _quote_single(s: str) -> str:
    # Safe for shlex: wrap in single quotes; escape embedded single quotes.
    if s is None:
        s = ""
    return "'" + s.replace("'", "'\\''") + "'"


def _fix_contains_or_heading_multitoken(payload: str) -> str:
    """Fix evidence payload where contains=/heading= value spills into multiple tokens.

    Strategy:
    - If shlex tokenization fails or yields stray tokens, try to salvage by wrapping
      the remainder of the line after contains=/heading= in single quotes.
    """

    # Prefer fixing contains= first, then heading=
    for key in ("contains=", "heading="):
        idx = payload.find(key)
        if idx < 0:
            continue

        before = payload[:idx]
        after = payload[idx + len(key) :].strip()
        if not after:
            return payload

        # If it already starts with a quote, leave it.
        if after.startswith("'") or after.startswith('"'):
            return payload

        # Wrap the whole remainder; evidence grammar allows key to be last.
        fixed = before + key + _quote_single(after)
        return fixed

    return payload


def _parse_evidence_payload(payload: str) -> Tuple[Optional[str], List[str], Optional[str]]:
    """Returns (etype, tokens, error)."""
    try:
        tokens = shlex.split(payload)
    except Exception as e:
        return None, [], str(e)
    if not tokens:
        return None, [], "empty"
    etype = tokens[0].lower()
    return etype, tokens, None


def _rewrite_evidence_line(indent: str, payload: str) -> Tuple[str, List[str]]:
    """Normalize one evidence payload. Returns (new_line, notes)."""

    notes: List[str] = []

    # First attempt: strict parse
    etype, tokens, err = _parse_evidence_payload(payload)

    if err is not None:
        # Try to fix multi-token contains/heading
        fixed_payload = _fix_contains_or_heading_multitoken(payload)
        etype, tokens, err2 = _parse_evidence_payload(fixed_payload)
        if err2 is None:
            notes.append("fixed: quote/space tokenization")
            payload = fixed_payload
        else:
            # Last resort: keep original, but add a note
            notes.append(f"invalid evidence (unparseable): {err}")
            return f"{indent}evidence: {payload}", notes

    # If tokens beyond type contain stray tokens (non key=value), attempt fix
    stray = [t for t in tokens[1:] if "=" not in t]
    if stray:
        fixed_payload = _fix_contains_or_heading_multitoken(payload)
        etype2, tokens2, err3 = _parse_evidence_payload(fixed_payload)
        if err3 is None and not [t for t in tokens2[1:] if "=" not in t]:
            notes.append("fixed: stray tokens by quoting remainder")
            payload = fixed_payload
            etype, tokens = etype2, tokens2
        else:
            notes.append(f"invalid evidence (stray tokens): {stray}")
            return f"{indent}evidence: {payload}", notes

    # Build kv map
    kv = {}
    for t in tokens[1:]:
        k, v = t.split("=", 1)
        kv[k] = v

    # Fix contains=exists
    if "contains" in kv:
        cv = kv["contains"].strip().strip('"\'').lower()
        if cv == "exists":
            kv.pop("contains", None)
            # Add regex matcher for existence-only proof
            kv.setdefault("regex", '"."')
            notes.append("fixed: replaced contains=exists with regex=\".\"")

    # Fix glob path
    if "path" in kv:
        p = _normalize_path_token(kv["path"])
        if _has_glob(p):
            notes.append(f"needs manual fix: glob path not supported: {p}")
            # Keep the glob but annotate; do not guess concrete files.

    # Fix heading= on non-docs (best-effort)
    if "heading" in kv and etype != "docs":
        # Convert type to docs when there is a strong signal it's documentation.
        path_val = _normalize_path_token(kv.get("path", ""))
        if path_val.endswith(".md") or "docs/" in path_val or path_val.endswith("openapi.yaml"):
            etype = "docs"
            notes.append("fixed: converted evidence type to docs because heading= is docs-only")
        else:
            notes.append("needs manual fix: heading= only allowed for docs")

    # Rebuild payload with stable ordering: type first, then path, then others
    ordered_keys = []
    if "path" in kv:
        ordered_keys.append("path")
    for k in sorted(k for k in kv.keys() if k != "path"):
        ordered_keys.append(k)

    rebuilt = [etype]
    for k in ordered_keys:
        rebuilt.append(f"{k}={kv[k]}")

    return f"{indent}evidence: " + " ".join(rebuilt), notes


def _convert_legacy_bullet_to_evidence(kind: str, body: str) -> Optional[str]:
    kind = kind.lower()
    etype = {"code": "code", "test": "test", "docs": "docs", "ui": "ui"}.get(kind)
    if not etype:
        return None

    # Try to find a path and a matcher.
    path = None
    m = re.search(r"\b([A-Za-z0-9_./-]+\.(ts|tsx|js|jsx|py|go|java|kt|rs|md|yaml|yml|json|sql|prisma))\b", body)
    if m:
        path = m.group(1)

    m2 = RE_PATH.search(body)
    if m2:
        path = m2.group("p")

    if not path:
        return None

    # contains "..." extraction
    contains = None
    qm = RE_QUOTED.search(body)
    if qm:
        contains = qm.group(1) or qm.group(2)

    # Build payload; quote contains safely if needed
    parts = [etype, f"path={_normalize_path_token(path)}"]
    if contains:
        parts.append(f"contains={_quote_single(contains)}")
    else:
        # existence-only proof as a fallback
        parts.append('regex="."')

    return "evidence: " + " ".join(parts)


def migrate(text: str) -> Tuple[str, List[str]]:
    lines = text.splitlines()
    out: List[str] = []
    notes: List[str] = []

    in_legacy_block = False
    current_task_indent = ""

    for i, line in enumerate(lines, start=1):
        # Track task indent
        tm = RE_TASK_LINE.match(line)
        if tm:
            in_legacy_block = False
            current_task_indent = tm.group("indent") + "  "  # evidence lines should be indented under task
            out.append(line)
            continue

        # Legacy Evidence Hooks header
        if RE_LEGACY_HOOKS_HEADER.match(line):
            in_legacy_block = True
            notes.append(f"L{i}: removed legacy Evidence Hooks header")
            continue

        # Legacy **Evidence:** line
        em = RE_LEGACY_EVIDENCE_HEADER.match(line)
        if em:
            body = (em.group("body") or "").strip()
            # Attempt to convert if it looks like a bullet content
            # Heuristic: if it contains a path-like token, convert to docs evidence.
            mpath = re.search(r"\b([A-Za-z0-9_./-]+\.(md|yaml|yml|json))\b", body)
            if mpath:
                path = mpath.group(1)
                payload = f"docs path={_normalize_path_token(path)} regex=\".\""
                new_line, ln_notes = _rewrite_evidence_line(current_task_indent, payload)
                out.append(new_line)
                notes.append(f"L{i}: converted legacy Evidence: → evidence: docs ({', '.join(ln_notes) if ln_notes else 'ok'})")
            else:
                # Preserve as a note
                out.append(f"{current_task_indent}note: legacy Evidence could not be converted; please add strict evidence hooks")
                notes.append(f"L{i}: legacy Evidence not convertible")
            continue

        # Legacy bullets inside a legacy block
        bm = RE_LEGACY_BULLET.match(line)
        if bm:
            kind = bm.group("kind")
            body = bm.group("body")
            converted = _convert_legacy_bullet_to_evidence(kind, body)
            if converted:
                payload = converted[len("evidence: ") :]
                new_line, ln_notes = _rewrite_evidence_line(current_task_indent, payload)
                out.append(new_line)
                notes.append(f"L{i}: converted legacy bullet {kind} → evidence ({', '.join(ln_notes) if ln_notes else 'ok'})")
                continue
            # Not convertible
            out.append(f"{current_task_indent}note: legacy bullet not convertible; please add strict evidence")
            notes.append(f"L{i}: legacy bullet not convertible")
            continue

        # Canonical evidence line: normalize/fix
        evm = RE_EVIDENCE_LINE.match(line)
        if evm:
            indent = evm.group("indent")
            payload = evm.group("payload")
            new_line, ln_notes = _rewrite_evidence_line(indent, payload)
            out.append(new_line)
            for n in ln_notes:
                notes.append(f"L{i}: {n}")
            continue

        # Default: pass through
        out.append(line)

    return "\n".join(out) + "\n", notes


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _atomic_write(path: Path, content: str) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    _write_text(tmp, content)
    tmp.replace(path)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tasks-file", required=True)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--out", default=".spec/reports/migrate-evidence-hooks")
    args = ap.parse_args()

    tasks_path = Path(args.tasks_file)
    if not tasks_path.exists():
        print(f"ERROR: tasks file not found: {tasks_path}")
        return 2

    if not _is_tasks_md_path(tasks_path):
        print("ERROR: for safety, --tasks-file must be under specs/** and end with tasks.md")
        return 2

    original = tasks_path.read_text(encoding="utf-8", errors="replace")
    migrated, notes = migrate(original)

    rid = _run_id()
    out_base = Path(args.out) / rid
    preview_path = out_base / "preview" / tasks_path.as_posix()
    report_path = out_base / "report.md"
    diff_path = out_base / "diff.patch"

    _write_text(preview_path, migrated)

    diff = "\n".join(
        difflib.unified_diff(
            original.splitlines(),
            migrated.splitlines(),
            fromfile=str(tasks_path),
            tofile=str(tasks_path) + " (migrated)",
            lineterm="",
        )
    )
    _write_text(diff_path, diff + "\n")

    report_lines = [
        f"# Migrate Evidence Hooks Report ({rid})",
        "",
        f"Target: `{tasks_path}`",
        f"Apply: `{bool(args.apply)}`",
        "",
        "## Notes",
    ]
    if notes:
        report_lines += [f"- {n}" for n in notes]
    else:
        report_lines.append("- No changes needed")

    report_lines += [
        "",
        "## Outputs",
        f"- Preview: `{preview_path}`",
        f"- Diff: `{diff_path}`",
        "",
        "## Next steps",
        "- Run the strict tasks validator on the preview file.",
        "- If satisfied, re-run with --apply.",
    ]
    _write_text(report_path, "\n".join(report_lines) + "\n")

    if args.apply:
        _atomic_write(tasks_path, migrated)
        print(f"Applied: updated {tasks_path}")
    else:
        print(f"Preview written: {preview_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
