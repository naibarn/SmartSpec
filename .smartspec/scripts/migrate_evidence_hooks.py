#!/usr/bin/env python3
"""migrate_evidence_hooks.py (v6.4.4)

Deterministically migrate/normalize SmartSpec tasks.md into strict evidence-hook format.

What v6.4.4 adds
-----------------
1) Structural normalization (safe, deterministic):
   - Convert YAML front-matter (--- ... ---) to the canonical header table.
   - Ensure exactly one '## Tasks' heading exists.
   - Remove known noise lines inside Tasks section (e.g. '$/a').

2) Evidence line normalization:
   - Convert bullet evidence lines like '- evidence: ...' to 'evidence: ...'.

3) Existing v6.4.3 behavior retained:
   - Convert legacy Evidence Hooks / Evidence / Code: bullets into canonical evidence lines.
   - Fix known false-negative patterns:
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

No network.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import difflib
import re
import shlex
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple


# -----------------------------
# Regexes
# -----------------------------

RE_TASK_LINE = re.compile(r"^(?P<indent>\s*)-\s*\[[ xX]\]\s+(?P<id>\S+)\s+.*$")
RE_EVIDENCE_LINE = re.compile(r"^(?P<indent>\s*)evidence:\s+(?P<payload>.*)$", re.IGNORECASE)
RE_BULLET_EVIDENCE_LINE = re.compile(r"^(?P<indent>\s*)[-*]\s+evidence:\s+(?P<payload>.*)$", re.IGNORECASE)

RE_LEGACY_HOOKS_HEADER = re.compile(r"^\s*(\*\*\s*)?Evidence Hooks(\s*\*\*)?\s*:\s*$", re.IGNORECASE)
RE_LEGACY_EVIDENCE_HEADER = re.compile(r"^\s*(\*\*\s*)?Evidence(\s*\*\*)?\s*:\s*(?P<body>.*)$", re.IGNORECASE)
RE_LEGACY_BULLET = re.compile(r"^\s*[-*]\s*(?P<kind>Code|Test|Docs|UI)\s*:\s*(?P<body>.+)$", re.IGNORECASE)

RE_NOISE = re.compile(r"^\s*\$/.+\s*$")

RE_PATH_LIKE = re.compile(
    r"\b([A-Za-z0-9_./-]+\.(ts|tsx|js|jsx|py|go|java|kt|rs|md|yaml|yml|json|sql|prisma))\b"
)
RE_PATH = re.compile(r"\bpath\s*=\s*(?P<p>[^\s]+)")
RE_QUOTED = re.compile(r"\"([^\"]*)\"|'([^']*)'")

RE_HEADER_TABLE = re.compile(r"^\|\s*spec-id\s*\|\s*source\s*\|\s*generated_by\s*\|\s*updated_at\s*\|\s*$", re.IGNORECASE)
RE_MD_HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


# -----------------------------
# Helpers
# -----------------------------


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


def _parse_front_matter(lines: List[str]) -> Tuple[Dict[str, str], int]:
    """Parse YAML-ish front matter if present.

    Returns (kv, end_index_exclusive). If not present, returns ({}, 0).
    """
    if not lines or lines[0].strip() != "---":
        return {}, 0

    kv: Dict[str, str] = {}
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return kv, i + 1
        # simple key: value pairs only
        m = re.match(r"^\s*([A-Za-z0-9_-]+)\s*:\s*(.*?)\s*$", lines[i])
        if not m:
            continue
        k, v = m.group(1), m.group(2)
        v = v.strip().strip('"').strip("'")
        kv[k] = v

    # No closing ---
    return {}, 0


def _ensure_header_table(lines: List[str]) -> Tuple[List[str], List[str]]:
    """Ensure canonical header table exists near top.

    - If already present, return unchanged.
    - If YAML front matter exists, convert it to table and remove the front matter.
    """
    notes: List[str] = []

    # If header table already exists in first 40 lines, keep.
    for i in range(min(40, len(lines))):
        if RE_HEADER_TABLE.match(lines[i].strip()):
            return lines, notes

    kv, end_idx = _parse_front_matter(lines)
    if end_idx > 0:
        # Convert front matter → header table
        spec_id = kv.get("spec_id") or kv.get("spec-id") or kv.get("specId") or "<spec-id>"
        source = kv.get("source") or "<spec.md>"
        generated_by = kv.get("generated_by") or kv.get("generated-by") or kv.get("generatedBy") or "smartspec_generate_tasks"
        updated_at = kv.get("updated_at") or kv.get("updated-at") or kv.get("updatedAt") or "<ISO_DATETIME>"

        header = [
            "| spec-id | source | generated_by | updated_at |",
            "|---|---|---|---|",
            f"| {spec_id} | {source} | {generated_by} | {updated_at} |",
            "",
        ]

        new_lines = header + lines[end_idx:]
        notes.append("converted YAML front-matter to canonical header table")
        return new_lines, notes

    # No front matter and no header table: insert a minimal table at top.
    header = [
        "| spec-id | source | generated_by | updated_at |",
        "|---|---|---|---|",
        "| <spec-id> | <spec.md> | smartspec_migrate_evidence_hooks | <ISO_DATETIME> |",
        "",
    ]
    notes.append("inserted missing canonical header table (placeholders need manual fill)")
    return header + lines, notes


def _count_exact_heading(lines: List[str], heading: str) -> List[int]:
    return [i for i, l in enumerate(lines) if l.strip() == heading]


def _ensure_single_tasks_heading(lines: List[str]) -> Tuple[List[str], List[str]]:
    """Ensure exactly one '## Tasks' heading exists.

    - If missing: insert after header table.
    - If duplicated: keep first, remove subsequent exact duplicates.
    """
    notes: List[str] = []
    idxs = _count_exact_heading(lines, "## Tasks")

    if not idxs:
        # Insert after header table (assume header table is at top; insert after first blank after header)
        insert_at = 0
        # find end of table if present
        for i in range(min(15, len(lines))):
            if lines[i].startswith("| "):
                insert_at = i + 1
                continue
        # move to first blank line after header table
        for j in range(insert_at, min(insert_at + 10, len(lines))):
            if lines[j].strip() == "":
                insert_at = j + 1
                break

        lines = lines[:insert_at] + ["## Tasks", ""] + lines[insert_at:]
        notes.append("inserted missing '## Tasks' heading")
        return lines, notes

    if len(idxs) > 1:
        keep = idxs[0]
        to_remove = set(idxs[1:])
        new_lines: List[str] = []
        for i, l in enumerate(lines):
            if i in to_remove and l.strip() == "## Tasks":
                continue
            new_lines.append(l)
        notes.append(f"removed duplicate '## Tasks' headings at lines {[x+1 for x in idxs[1:]]}")
        return new_lines, notes

    return lines, notes


def _tasks_section_bounds(lines: List[str]) -> Tuple[Optional[int], Optional[int]]:
    """Return (start, end) indices for the Tasks section content.

    start: index of '## Tasks'
    end: index of next heading with level <= 2 (i.e., '#', '##') or EOF
    """
    start_idxs = _count_exact_heading(lines, "## Tasks")
    if not start_idxs:
        return None, None
    start = start_idxs[0]

    end = len(lines)
    for i in range(start + 1, len(lines)):
        m = RE_MD_HEADING.match(lines[i])
        if not m:
            continue
        level = len(m.group(1))
        if level <= 2:
            end = i
            break

    return start, end


def _remove_noise_in_tasks(lines: List[str]) -> Tuple[List[str], List[str]]:
    notes: List[str] = []
    s, e = _tasks_section_bounds(lines)
    if s is None:
        return lines, notes

    new_lines: List[str] = []
    removed = 0
    for i, l in enumerate(lines):
        if s < i < e and RE_NOISE.match(l):
            removed += 1
            continue
        new_lines.append(l)

    if removed:
        notes.append(f"removed {removed} noise lines inside Tasks section")

    return new_lines, notes


def _parse_evidence_payload(payload: str) -> Tuple[Optional[str], List[str], Optional[str]]:
    try:
        tokens = shlex.split(payload)
    except Exception as e:
        return None, [], str(e)
    if not tokens:
        return None, [], "empty"
    etype = tokens[0].lower()
    return etype, tokens, None


def _fix_contains_or_heading_multitoken(payload: str) -> str:
    """Fix evidence payload where contains=/heading= value spills into multiple tokens.

    Strategy:
    - If shlex tokenization fails or yields stray tokens, try to salvage by wrapping
      the remainder of the line after contains=/heading= in single quotes.
    """
    for key in ("contains=", "heading="):
        idx = payload.find(key)
        if idx < 0:
            continue
        before = payload[:idx]
        after = payload[idx + len(key) :].strip()
        if not after:
            return payload
        if after.startswith("'") or after.startswith('"'):
            return payload
        return before + key + _quote_single(after)
    return payload


def _rewrite_evidence_payload(payload: str) -> Tuple[str, List[str]]:
    """Normalize one evidence payload. Returns (new_payload, notes)."""
    notes: List[str] = []

    etype, tokens, err = _parse_evidence_payload(payload)
    if err is not None:
        fixed = _fix_contains_or_heading_multitoken(payload)
        etype2, tokens2, err2 = _parse_evidence_payload(fixed)
        if err2 is None:
            payload = fixed
            etype, tokens = etype2, tokens2
            notes.append("fixed: quote/space tokenization")
        else:
            notes.append(f"invalid evidence (unparseable): {err}")
            return payload, notes

    stray = [t for t in tokens[1:] if "=" not in t]
    if stray:
        fixed = _fix_contains_or_heading_multitoken(payload)
        etype2, tokens2, err3 = _parse_evidence_payload(fixed)
        if err3 is None and not [t for t in tokens2[1:] if "=" not in t]:
            payload = fixed
            etype, tokens = etype2, tokens2
            notes.append("fixed: stray tokens by quoting remainder")
        else:
            notes.append(f"invalid evidence (stray tokens): {stray}")
            return payload, notes

    # Build kv map
    kv: Dict[str, str] = {}
    for t in tokens[1:]:
        k, v = t.split("=", 1)
        kv[k] = v

    # Fix contains=exists
    if "contains" in kv:
        cv = kv["contains"].strip().strip('"\'').lower()
        if cv == "exists":
            kv.pop("contains", None)
            kv.setdefault("regex", '"."')
            notes.append("fixed: replaced contains=exists with regex=\".\"")

    # Fix glob path (do not guess file list)
    if "path" in kv:
        p = _normalize_path_token(kv["path"])
        kv["path"] = p
        if _has_glob(p):
            notes.append(f"needs manual fix: glob path not supported: {p}")

    # Fix heading= on non-docs
    if "heading" in kv and (etype or "") != "docs":
        path_val = _normalize_path_token(kv.get("path", ""))
        if path_val.endswith(".md") or "docs/" in path_val or path_val.endswith("openapi.yaml"):
            etype = "docs"
            notes.append("fixed: converted evidence type to docs because heading= is docs-only")
        else:
            notes.append("needs manual fix: heading= only allowed for docs")

    # Rebuild payload
    rebuilt: List[str] = [etype or "code"]
    if "path" in kv:
        rebuilt.append(f"path={kv['path']}")
    for k in sorted(k for k in kv.keys() if k != "path"):
        rebuilt.append(f"{k}={kv[k]}")

    return " ".join(rebuilt), notes


def _convert_legacy_bullet_to_evidence(kind: str, body: str) -> Optional[str]:
    kind_l = kind.lower()
    etype = {"code": "code", "test": "test", "docs": "docs", "ui": "ui"}.get(kind_l)
    if not etype:
        return None

    # Find a path
    path = None
    m = RE_PATH_LIKE.search(body)
    if m:
        path = m.group(1)
    m2 = RE_PATH.search(body)
    if m2:
        path = m2.group("p")
    if not path:
        return None

    # Find a quoted matcher (best-effort)
    contains = None
    qm = RE_QUOTED.search(body)
    if qm:
        contains = qm.group(1) or qm.group(2)

    parts = [etype, f"path={_normalize_path_token(path)}"]
    if contains:
        parts.append(f"contains={_quote_single(contains)}")
    else:
        parts.append('regex="."')

    return " ".join(parts)


# -----------------------------
# Main migration
# -----------------------------


def migrate(text: str) -> Tuple[str, List[str]]:
    orig_lines = text.splitlines()
    notes: List[str] = []

    # 1) Ensure header table (convert front matter if present)
    lines, n1 = _ensure_header_table(orig_lines)
    notes += n1

    # 2) Ensure single ## Tasks heading
    lines, n2 = _ensure_single_tasks_heading(lines)
    notes += n2

    # 3) Remove noise lines inside Tasks section
    lines, n3 = _remove_noise_in_tasks(lines)
    notes += n3

    # 4) Evidence normalization + legacy conversions
    out: List[str] = []
    current_task_indent = ""
    in_legacy_block = False

    for i, line in enumerate(lines, start=1):
        tm = RE_TASK_LINE.match(line)
        if tm:
            in_legacy_block = False
            current_task_indent = tm.group("indent") + "  "
            out.append(line)
            continue

        # Convert bullet-evidence to evidence
        bem = RE_BULLET_EVIDENCE_LINE.match(line)
        if bem:
            payload = bem.group("payload")
            new_payload, ln_notes = _rewrite_evidence_payload(payload)
            out.append(f"{bem.group('indent')}evidence: {new_payload}")
            notes.append(f"L{i}: normalized '- evidence:' to 'evidence:'")
            for n in ln_notes:
                notes.append(f"L{i}: {n}")
            continue

        # Legacy headers
        if RE_LEGACY_HOOKS_HEADER.match(line):
            in_legacy_block = True
            notes.append(f"L{i}: removed legacy Evidence Hooks header")
            continue

        em = RE_LEGACY_EVIDENCE_HEADER.match(line)
        if em:
            body = (em.group("body") or "").strip()
            mpath = RE_PATH_LIKE.search(body)
            if mpath:
                path = _normalize_path_token(mpath.group(1))
                payload = f"docs path={path} regex=\".\""
                new_payload, ln_notes = _rewrite_evidence_payload(payload)
                out.append(f"{current_task_indent}evidence: {new_payload}")
                notes.append(f"L{i}: converted legacy Evidence: → evidence: docs")
                for n in ln_notes:
                    notes.append(f"L{i}: {n}")
            else:
                out.append(f"{current_task_indent}note: legacy Evidence could not be converted; please add strict evidence hooks")
                notes.append(f"L{i}: legacy Evidence not convertible")
            continue

        bm = RE_LEGACY_BULLET.match(line)
        if bm:
            kind = bm.group("kind")
            body = bm.group("body")
            converted = _convert_legacy_bullet_to_evidence(kind, body)
            if converted:
                new_payload, ln_notes = _rewrite_evidence_payload(converted)
                out.append(f"{current_task_indent}evidence: {new_payload}")
                notes.append(f"L{i}: converted legacy bullet {kind} → evidence")
                for n in ln_notes:
                    notes.append(f"L{i}: {n}")
            else:
                out.append(f"{current_task_indent}note: legacy bullet not convertible; please add strict evidence")
                notes.append(f"L{i}: legacy bullet not convertible")
            continue

        # Canonical evidence line
        evm = RE_EVIDENCE_LINE.match(line)
        if evm:
            indent = evm.group("indent")
            payload = evm.group("payload")
            new_payload, ln_notes = _rewrite_evidence_payload(payload)
            out.append(f"{indent}evidence: {new_payload}")
            for n in ln_notes:
                notes.append(f"L{i}: {n}")
            continue

        out.append(line)

    return "\n".join(out) + "\n", notes


# -----------------------------
# IO
# -----------------------------


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
