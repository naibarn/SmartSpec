#!/usr/bin/env python3
"""migrate_evidence_hooks.py (v6.5.1)

Preview-first migrator for SmartSpec tasks evidence hooks.

What it does
- Reads a governed `specs/**/tasks.md`
- Normalizes evidence lines into strict, shlex-parseable hooks
- Writes preview artifacts under `.spec/reports/migrate-evidence-hooks/<run-id>/...`
- Only modifies the governed tasks file when `--apply` is explicitly provided

Canonical evidence format (output)
  evidence: <code|test|docs|ui> key=value key="value with spaces" ...

Key behaviors (to reduce verify false-negatives)
- Normalizes `- evidence: ...` into `evidence: ...` (no bullet)
- Converts command-like evidence (e.g. `evidence: npm run build`) into:
    evidence: test path=<anchor-file> command="npm run build"
- Converts unsupported legacy types into strict types (best-effort)
- Prevents unsafe paths (absolute, traversal, glob patterns) from becoming path=

Safety
- No network.
- Does not run commands.
- In preview mode, does not write to governed files.
"""

from __future__ import annotations

import argparse
import difflib
import os
import re
import shlex
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple


STRICT_TYPES = {"code", "test", "docs", "ui"}

# Common command prefixes that should NEVER appear as path= values.
COMMAND_PREFIXES = {
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
    "pytest",
    "make",
    "docker",
    "docker-compose",
    "compose",
    "go",
    "cargo",
    "mvn",
    "gradle",
    "java",
    "dotnet",
    "swagger-cli",
}

GLOB_CHARS = set("*?[]")

# Matches both canonical and bullet evidence lines.
RE_EVIDENCE_ANY = re.compile(r"^(?P<indent>\s*)(?:-\s*)?evidence:\s+(?P<payload>.*)$", re.IGNORECASE)

# Minimal legacy patterns (used only for best-effort conversions)
RE_LEGACY_BULLET_TYPED = re.compile(r"^\s*-\s*(Code|Test|Docs|UI)\s*:\s*(?P<body>.+)$", re.IGNORECASE)


@dataclass
class EvidenceFix:
    line_no: int
    before: str
    after: str
    reason: str


def _run_id() -> str:
    return time.strftime("%Y%m%d_%H%M%S", time.localtime())


def _norm_path(p: str) -> str:
    p = p.strip().strip('"').strip("'").replace("\\", "/")
    if p.startswith("./"):
        p = p[2:]
    return p


def _is_abs_or_traversal(p: str) -> bool:
    if not p:
        return True
    p2 = _norm_path(p)
    if p2.startswith("/") or p2.startswith("\\") or re.match(r"^[A-Za-z]:/", p2):
        return True
    if ".." in Path(p2).parts:
        return True
    return False


def _has_glob(p: str) -> bool:
    return any(ch in p for ch in GLOB_CHARS)


def _quote_if_needed(v: str) -> str:
    v = v.strip().strip('"').strip("'")
    if any(ch.isspace() for ch in v) or any(ch in v for ch in ['"', "=", "\\"]):
        v = v.replace('"', '\\"')
        return f'"{v}"'
    return v


def _shlex_split(payload: str) -> Tuple[List[str], Optional[str]]:
    try:
        return shlex.split(payload), None
    except ValueError as e:
        return [], str(e)


def _anchor_path_for_command(cmd: str, project_root: Path) -> str:
    """Choose a stable file to anchor a test evidence command."""
    c = cmd.lower().strip()

    if c.startswith(("npm ", "pnpm ", "yarn ", "bun ", "npx ")):
        if (project_root / "package.json").exists():
            return "package.json"
        return "package.json"

    if "prisma" in c:
        if (project_root / "prisma/schema.prisma").exists():
            return "prisma/schema.prisma"
        return "prisma/schema.prisma"

    if "openapi" in c or "swagger" in c:
        for cand in ["openapi.yaml", "openapi.yml", "openapi.json", "swagger.yaml", "swagger.yml", "swagger.json"]:
            if (project_root / cand).exists():
                return cand
        return "openapi.yaml"

    if c.startswith(("pytest", "python ", "python3 ")):
        for cand in ["pyproject.toml", "requirements.txt", "setup.cfg"]:
            if (project_root / cand).exists():
                return cand
        return "pyproject.toml"

    if c.startswith("docker"):
        if (project_root / "Dockerfile").exists():
            return "Dockerfile"
        for cand in ["docker-compose.yml", "docker-compose.yaml"]:
            if (project_root / cand).exists():
                return cand
        return "Dockerfile"

    return "README.md" if (project_root / "README.md").exists() else "package.json"


def _render_payload(etype: str, kv: Dict[str, str]) -> str:
    # Stable ordering: path first, then the rest sorted.
    keys = ["path"] + sorted([k for k in kv.keys() if k != "path"])
    parts = [etype]
    for k in keys:
        if k not in kv:
            continue
        parts.append(f"{k}={_quote_if_needed(kv[k])}")
    return " ".join(parts)


def _convert_commandish(payload: str, project_root: Path) -> Optional[Tuple[str, str]]:
    """Convert raw command evidence into strict test evidence."""
    raw = payload.strip()
    first = raw.split()[0].lower() if raw.split() else ""
    if first in COMMAND_PREFIXES:
        anchor = _anchor_path_for_command(raw, project_root)
        return _render_payload("test", {"path": anchor, "command": raw}), "converted_commandish_to_test"
    return None


def _parse_kv_strict(payload: str) -> Tuple[str, Dict[str, str], Optional[str]]:
    tokens, err = _shlex_split(payload)
    if err:
        return "", {}, f"shlex_error:{err}"
    if not tokens:
        return "", {}, "empty"
    etype = tokens[0].lower()
    kv: Dict[str, str] = {}
    stray: List[str] = []
    for t in tokens[1:]:
        if "=" not in t:
            stray.append(t)
            continue
        k, v = t.split("=", 1)
        kv[k.strip()] = v.strip()
    if stray:
        return etype, kv, f"stray_tokens:{' '.join(stray)}"
    return etype, kv, None


def _best_effort_convert_legacy_typed(line: str, project_root: Path) -> Optional[Tuple[str, str]]:
    m = RE_LEGACY_BULLET_TYPED.match(line)
    if not m:
        return None
    typ = m.group(1).lower()
    body = m.group("body").strip()

    # Minimal heuristics
    if typ in {"code", "docs"}:
        # If it looks like a path, treat as path
        if "/" in body or body.endswith((".ts", ".tsx", ".js", ".jsx", ".py", ".go", ".java", ".md", ".yaml", ".yml", ".json")):
            et = "docs" if body.endswith((".md", ".yaml", ".yml", ".json")) else "code"
            return _render_payload(et, {"path": body}), "converted_legacy_typed_bullet"

    if typ == "test":
        # If looks like a command, turn into command evidence
        conv = _convert_commandish(body, project_root)
        if conv:
            return conv[0], "converted_legacy_test_command"

    # Can't safely infer
    return None


def _normalize_one_evidence(payload: str, project_root: Path) -> Tuple[str, str]:
    # 1) If the entire payload is command-like: convert
    conv = _convert_commandish(payload, project_root)
    if conv:
        return conv[0], conv[1]

    # 2) Parse strict payload
    etype, kv, err = _parse_kv_strict(payload)

    # Unparseable or stray tokens -> convert whole payload into command evidence (best-effort)
    if not etype or err:
        anchor = _anchor_path_for_command(payload, project_root)
        return _render_payload("test", {"path": anchor, "command": payload}), f"replaced_unparseable:{err or 'unknown'}"

    # Unsupported type -> map to strict types when possible
    if etype not in STRICT_TYPES:
        # Simple legacy mapping
        if etype in {"file_exists", "file"}:
            p = _norm_path(kv.get("path", "") or kv.get("file", ""))
            if not p:
                anchor = _anchor_path_for_command("openapi", project_root)
                return _render_payload("docs", {"path": anchor, "contains": payload[:80]}), "legacy_file_exists_missing_path"
            kind = "docs" if p.endswith((".md", ".yaml", ".yml", ".json")) else "code"
            return _render_payload(kind, {"path": p}), "legacy_file_exists_mapped"

        if etype in {"api_route", "route", "endpoint"}:
            route = kv.get("route") or kv.get("endpoint") or kv.get("url") or ""
            p = _norm_path(kv.get("path", ""))
            if not route:
                return _render_payload("docs", {"path": _anchor_path_for_command("openapi", project_root), "contains": payload[:80]}), "legacy_route_missing_value"
            if not p:
                return _render_payload("docs", {"path": _anchor_path_for_command("openapi", project_root), "contains": route}), "legacy_route_to_docs"
            return _render_payload("code", {"path": p, "contains": route}), "legacy_route_to_code"

        if etype in {"db_schema", "schema", "prisma"}:
            p = _norm_path(kv.get("path", "") or "prisma/schema.prisma")
            model = kv.get("model") or kv.get("table") or ""
            out_kv = {"path": p}
            if model:
                out_kv["contains"] = model
            return _render_payload("code", out_kv), "legacy_schema_to_code"

        if etype in {"command", "cmd", "shell", "verification"}:
            cmd = kv.get("command") or kv.get("cmd") or payload
            anchor = _anchor_path_for_command(cmd, project_root)
            return _render_payload("test", {"path": anchor, "command": cmd}), "legacy_command_to_test"

        # Unknown type: convert to docs with contains (safe fallback)
        return _render_payload("docs", {"path": _anchor_path_for_command("openapi", project_root), "contains": payload[:80]}), f"unknown_type:{etype}"

    # Normalize path and safety
    if "path" in kv:
        kv["path"] = _norm_path(kv["path"])
        p = kv["path"]

        # If path is unsafe, do NOT keep it as path=
        if _is_abs_or_traversal(p) or _has_glob(p):
            anchor = _anchor_path_for_command(payload, project_root)
            return _render_payload("test", {"path": anchor, "command": payload}), "unsafe_path_converted_to_test_command"

        # If path starts with a command prefix, it's likely wrong
        first = p.split("/", 1)[0].lower()
        if first in COMMAND_PREFIXES:
            anchor = _anchor_path_for_command(payload, project_root)
            return _render_payload("test", {"path": anchor, "command": payload}), "command_in_path_converted_to_test_command"

    # Fix: heading= is docs-only; if code uses heading and looks like docs file, convert
    if etype == "code" and "heading" in kv:
        p = kv.get("path", "")
        if p.endswith((".md", ".yaml", ".yml", ".json")):
            return _render_payload("docs", kv), "converted_code_heading_to_docs"

    return _render_payload(etype, kv), "normalized"


def transform_tasks_md(content: str, project_root: Path) -> Tuple[str, List[EvidenceFix]]:
    lines = content.splitlines(keepends=True)
    fixes: List[EvidenceFix] = []

    for idx, line in enumerate(lines, start=1):
        # Convert minimal typed legacy bullets (optional)
        legacy = _best_effort_convert_legacy_typed(line, project_root)
        if legacy:
            payload, reason = legacy
            indent = re.match(r"^\s*", line).group(0)
            new_line = f"{indent}evidence: {payload}\n"
            fixes.append(EvidenceFix(idx, line.rstrip("\n"), new_line.rstrip("\n"), reason))
            lines[idx - 1] = new_line
            continue

        m = RE_EVIDENCE_ANY.match(line)
        if not m:
            continue

        indent = m.group("indent")
        payload = m.group("payload").strip()

        new_payload, reason = _normalize_one_evidence(payload, project_root)
        new_line = f"{indent}evidence: {new_payload}\n"

        if new_line != line:
            fixes.append(EvidenceFix(idx, line.rstrip("\n"), new_line.rstrip("\n"), reason))
            lines[idx - 1] = new_line

    return "".join(lines), fixes


def unified_diff(old: str, new: str, fromfile: str, tofile: str) -> str:
    return "".join(
        difflib.unified_diff(
            old.splitlines(keepends=True),
            new.splitlines(keepends=True),
            fromfile=fromfile,
            tofile=tofile,
        )
    )


def atomic_write(path: Path, content: str) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    os.replace(tmp, path)


def ensure_specs_scoped(tasks_file: Path) -> None:
    # Guard: tasks.md should be under specs/**
    parts = [p.replace("\\", "/") for p in tasks_file.parts]
    if "specs" not in parts:
        raise SystemExit(f"Refusing: tasks file must be under specs/**. Got: {tasks_file}")


def write_report(out_dir: Path, tasks_rel: str, apply: bool, fixes: List[EvidenceFix], preview_path: Path) -> None:
    lines: List[str] = []
    lines.append("# migrate-evidence-hooks report\n")
    lines.append(f"\n- tasks: {tasks_rel}\n")
    lines.append(f"- apply: {apply}\n")
    lines.append(f"- fixes: {len(fixes)}\n")
    lines.append("\n## outputs\n")
    lines.append(f"- preview: `{preview_path}`\n")
    lines.append(f"- diff: `{out_dir / 'diff.patch'}`\n")
    lines.append(f"- report: `{out_dir / 'report.md'}`\n")

    if fixes:
        lines.append("\n## changes (first 200)\n")
        for f in fixes[:200]:
            lines.append(f"- L{f.line_no}: {f.reason}\n")
            lines.append(f"  - before: `{f.before.strip()}`\n")
            lines.append(f"  - after:  `{f.after.strip()}`\n")
        if len(fixes) > 200:
            lines.append(f"- ... {len(fixes) - 200} more\n")

    (out_dir / "report.md").write_text("".join(lines), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Preview-first evidence hook migrator")
    ap.add_argument("--tasks-file", required=True, help="Path to specs/**/tasks.md")
    ap.add_argument("--project-root", default=".", help="Repo root")
    ap.add_argument("--out", default=".spec/reports/migrate-evidence-hooks", help="Report root")
    ap.add_argument("--apply", action="store_true", help="Apply changes to governed tasks.md")
    args = ap.parse_args()

    project_root = Path(args.project_root).resolve()
    tasks_file = Path(args.tasks_file)

    if not project_root.exists():
        print(f"ERROR: project root not found: {project_root}")
        return 2
    if not tasks_file.exists():
        print(f"ERROR: tasks file not found: {tasks_file}")
        return 2

    ensure_specs_scoped(tasks_file)

    original = tasks_file.read_text(encoding="utf-8", errors="ignore")
    modified, fixes = transform_tasks_md(original, project_root)

    run_id = _run_id()
    out_dir = Path(args.out) / run_id
    out_dir.mkdir(parents=True, exist_ok=True)

    # Preview mirrors original relative path
    tasks_rel = tasks_file.as_posix()
    preview_path = out_dir / "preview" / tasks_rel
    preview_path.parent.mkdir(parents=True, exist_ok=True)
    preview_path.write_text(modified, encoding="utf-8")

    diff_text = unified_diff(original, modified, fromfile=f"a/{tasks_rel}", tofile=f"b/{tasks_rel}")
    (out_dir / "diff.patch").write_text(diff_text, encoding="utf-8")

    write_report(out_dir, tasks_rel=tasks_rel, apply=bool(args.apply), fixes=fixes, preview_path=preview_path)

    if args.apply:
        backup = tasks_file.with_suffix(tasks_file.suffix + f".backup.{run_id}")
        backup.write_text(original, encoding="utf-8")
        atomic_write(tasks_file, modified)
        print(f"OK: applied {len(fixes)} fixes to {tasks_file}")
        print(f"OK: backup: {backup}")
    else:
        print(f"OK: preview only (no governed writes)")
        print(f"OK: preview: {preview_path}")

    print(f"OK: report: {out_dir / 'report.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
