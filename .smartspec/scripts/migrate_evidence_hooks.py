#!/usr/bin/env python3
"""migrate_evidence_hooks.py (v6.5.3)

SmartSpec helper script used by `/smartspec_migrate_evidence_hooks`.

Goals
- Preview-first: default behavior MUST NOT modify governed artifacts.
- Governed writes require `--apply`.
- Output artifacts only under `.spec/reports/**` in preview mode.
- Normalize legacy evidence formatting and convert non-strict evidence hooks
  into strict-verifier compatible hooks: code|test|docs|ui.

Why this exists
- Strict verifier (`smartspec_verify_tasks_progress_strict`) only understands:
  `evidence: code|test|docs|ui key=value ...`
- Legacy tasks often include:
  - bullets like `- evidence: ...`
  - unsupported types like `file_exists`, `api_route`, `db_schema`, `command`
  - broken strict-ish hooks where values with spaces are not quoted, e.g.
    `command=npx prisma validate` (breaks shlex parsing and causes false negatives)

This script:
- normalizes bullet evidence into canonical `evidence:` (no leading `-`)
- converts unsupported types into strict types
- repairs broken strict-ish hooks by re-hydrating unquoted values
  (joins stray tokens onto the previous key for keys like command/contains/etc.)
- converts command-ish evidence into `evidence: test path=<anchor> command="..."`

IMPORTANT
- This script does NOT call the network.
- This script does NOT run commands in evidence; it only records them.

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

# Keys that may legitimately contain spaces (must be quoted in the final output)
SPACE_TOLERANT_KEYS = {"command", "contains", "regex", "heading", "selector", "symbol"}

# Common command prefixes that should NEVER appear as path= values.
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

RE_EVIDENCE_CANON = re.compile(r"^\s*evidence:\s+(?P<payload>.*)$", re.IGNORECASE)
RE_EVIDENCE_BULLET = re.compile(r"^\s*-\s*evidence:\s+(?P<payload>.*)$", re.IGNORECASE)


@dataclass
class EvidenceFix:
    line_no: int
    before: str
    after: str
    reason: str


def _safe_rel_path(p: str) -> str:
    p = p.strip().strip('"').strip("'").replace("\\", "/")
    if p.startswith("./"):
        p = p[2:]
    return p


def _is_glob_path(p: str) -> bool:
    return any(ch in p for ch in ["*", "?", "[", "]"])


def _is_abs_or_traversal(p: str) -> bool:
    if not p:
        return True
    p = _safe_rel_path(p)
    if p.startswith("/") or re.match(r"^[A-Za-z]:/", p):
        return True
    if ".." in p.split("/"):
        return True
    return False


def _quote_if_needed(v: str) -> str:
    v = v.strip()
    if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
        return v
    if any(ch.isspace() for ch in v) or '"' in v:
        v = v.replace('"', '\\"')
        return f'"{v}"'
    return v


def _shlex_split(payload: str) -> Tuple[List[str], Optional[str]]:
    try:
        return shlex.split(payload, posix=True), None
    except Exception as e:
        return [], f"shlex_error:{e}"


def _parse_payload_lenient(payload: str) -> Tuple[str, Dict[str, str], Optional[str]]:
    """Lenient parser that repairs unquoted values with spaces.

    Example input (broken):
      test path=... command=npx prisma validate

    Tokens become:
      ['test','path=...','command=npx','prisma','validate']

    We join stray tokens ('prisma','validate') onto the last key (command).
    """
    tokens, err = _shlex_split(payload)
    if err:
        return "", {}, err
    if not tokens:
        return "", {}, "empty_payload"

    hook_type = tokens[0]
    kv: Dict[str, str] = {}
    last_key: Optional[str] = None
    stray: List[str] = []

    for t in tokens[1:]:
        if "=" in t:
            k, v = t.split("=", 1)
            k = k.strip()
            kv[k] = v.strip()
            last_key = k
            continue

        if last_key and last_key in SPACE_TOLERANT_KEYS:
            kv[last_key] = (kv.get(last_key, "").rstrip() + " " + t).strip()
        else:
            stray.append(t)

    if stray:
        return hook_type, kv, f"stray_tokens:{stray}"

    return hook_type, kv, None


def _anchor_path_for_command(cmd: str, project_root: Path) -> str:
    cmd_l = cmd.lower().strip()

    if cmd_l.startswith(("npm ", "pnpm ", "yarn ", "bun ", "npx ")):
        return "package.json" if (project_root / "package.json").exists() else "package.json"

    if "prisma" in cmd_l:
        return "prisma/schema.prisma"

    if "openapi" in cmd_l or "swagger" in cmd_l:
        for cand in [
            "openapi.yaml",
            "openapi.yml",
            "openapi.json",
            "swagger.yaml",
            "swagger.yml",
            "swagger.json",
        ]:
            if (project_root / cand).exists():
                return cand
        return "openapi.yaml"

    if cmd_l.startswith(("pytest", "python ", "python3 ")):
        for cand in ["pyproject.toml", "requirements.txt", "setup.cfg"]:
            if (project_root / cand).exists():
                return cand
        return "pyproject.toml"

    if cmd_l.startswith("docker"):
        if (project_root / "Dockerfile").exists():
            return "Dockerfile"
        return "docker-compose.yml" if (project_root / "docker-compose.yml").exists() else "docker-compose.yml"

    return "README.md" if (project_root / "README.md").exists() else "package.json"


def _render_payload(hook_type: str, kv: Dict[str, str]) -> str:
    ht = hook_type.strip().lower()

    if "path" in kv:
        kv = dict(kv)
        kv["path"] = _safe_rel_path(kv["path"]).rstrip("/")

    ordered: List[str] = []
    if "path" in kv:
        ordered.append("path")
    ordered.extend(sorted(k for k in kv.keys() if k != "path"))

    parts = [ht]
    for k in ordered:
        parts.append(f"{k}={_quote_if_needed(kv[k])}")
    return " ".join(parts)


def _convert_commandish_payload(raw_payload: str, project_root: Path) -> Optional[Tuple[str, str]]:
    raw = raw_payload.strip()
    if re.match(r"^(code|test|docs|ui)\b", raw, re.IGNORECASE):
        return None

    first = raw.split()[0].lower() if raw.split() else ""
    if first in SUSPICIOUS_PATH_PREFIXES:
        cmd = raw
        anchor = _anchor_path_for_command(cmd, project_root)
        return (f"test path={anchor} command={_quote_if_needed(cmd)}", "converted_commandish_to_test")

    return None


def _convert_unsupported_to_strict(hook_type: str, kv: Dict[str, str], project_root: Path) -> Tuple[Optional[str], str]:
    ht = hook_type.strip().lower()

    if ht in STRICT_TYPES:
        return None, "already_strict"

    if ht in {"file_exists", "file"}:
        p = kv.get("path") or kv.get("file") or ""
        p = _safe_rel_path(p)
        if not p:
            return None, "missing_path"
        if p.lower().endswith((".md", ".markdown", ".rst", ".txt", ".yaml", ".yml", ".json")):
            return f"docs path={p}", "mapped_file_exists_to_docs"
        return f"code path={p}", "mapped_file_exists_to_code"

    if ht in {"api_route", "route", "endpoint"}:
        p = _safe_rel_path(kv.get("path", ""))
        route = kv.get("route") or kv.get("url") or kv.get("endpoint") or ""
        if not route:
            return None, "missing_route"
        if not p:
            anchor = _anchor_path_for_command("openapi", project_root)
            return f"docs path={anchor} contains={_quote_if_needed(route)}", "mapped_api_route_to_docs_contains"
        return f"code path={p} contains={_quote_if_needed(route)}", "mapped_api_route_to_code_contains"

    if ht in {"db_schema", "schema", "prisma"}:
        p = _safe_rel_path(kv.get("path", "")) or "prisma/schema.prisma"
        model = kv.get("model") or kv.get("table") or ""
        if model:
            return f"code path={p} contains={_quote_if_needed(model)}", "mapped_db_schema_to_code_contains"
        return f"code path={p}", "mapped_db_schema_to_code"

    if ht in {"command", "cmd", "shell"}:
        cmd = kv.get("command") or kv.get("cmd") or ""
        if not cmd:
            return None, "missing_command"
        anchor = _anchor_path_for_command(cmd, project_root)
        return f"test path={anchor} command={_quote_if_needed(cmd)}", "mapped_command_to_test_command"

    return None, f"unknown_type:{ht}"


def _repair_strict(hook_type: str, kv: Dict[str, str], project_root: Path) -> Tuple[str, str]:
    ht = hook_type.strip().lower()

    if ht not in STRICT_TYPES:
        # unknown type: preserve as docs contains (best-effort)
        anchor = _anchor_path_for_command("openapi", project_root)
        return _render_payload("docs", {"path": anchor, "contains": f"{hook_type} {kv}"}), "unknown_type_to_docs_contains"

    if "path" not in kv:
        # missing path -> treat as command-ish reference
        cmd = f"{hook_type} " + " ".join([f"{k}={v}" for k, v in kv.items()])
        anchor = _anchor_path_for_command(cmd, project_root)
        return _render_payload("test", {"path": anchor, "command": cmd}), "missing_path_to_test_command"

    p = _safe_rel_path(kv.get("path", ""))

    if _is_abs_or_traversal(p) or _is_glob_path(p):
        cmd = f"{hook_type} " + " ".join([f"{k}={v}" for k, v in kv.items()])
        anchor = _anchor_path_for_command(cmd, project_root)
        return _render_payload("test", {"path": anchor, "command": cmd}), "unsafe_path_to_test_command"

    first = p.split("/", 1)[0].lower() if p else ""
    if first in SUSPICIOUS_PATH_PREFIXES:
        cmd = p
        anchor = _anchor_path_for_command(cmd, project_root)
        return _render_payload("test", {"path": anchor, "command": cmd}), "command_in_path_to_test_command"

    # directory shorthand
    if ht == "code" and p.endswith("/"):
        kv2 = dict(kv)
        kv2["path"] = p.rstrip("/")
        kv2.setdefault("symbol", "Directory")
        return _render_payload("code", kv2), "directory_path_added_symbol_directory"

    # docs vs code mismatch when heading is present
    if ht == "code" and "heading" in kv:
        if p.lower().endswith((".md", ".markdown", ".rst", ".txt", ".yaml", ".yml", ".json")):
            return _render_payload("docs", dict(kv, path=p)), "converted_code_heading_to_docs"

    return _render_payload(ht, dict(kv, path=p)), "normalized"


def transform_tasks_md(content: str, project_root: Path) -> Tuple[str, List[EvidenceFix]]:
    lines = content.splitlines(keepends=True)
    fixes: List[EvidenceFix] = []

    for idx, line in enumerate(lines, start=1):
        m_b = RE_EVIDENCE_BULLET.match(line)
        m_c = RE_EVIDENCE_CANON.match(line)
        if not (m_b or m_c):
            continue

        payload = (m_b or m_c).group("payload").strip()
        indent = re.match(r"^\s*", line).group(0)

        # 1) command-ish line
        cmdish = _convert_commandish_payload(payload, project_root)
        if cmdish:
            new_payload, reason = cmdish
            new_line = f"{indent}evidence: {new_payload}\n"
            fixes.append(EvidenceFix(idx, line.rstrip("\n"), new_line.rstrip("\n"), reason))
            lines[idx - 1] = new_line
            continue

        # 2) parse leniently
        hook_type, kv, parse_error = _parse_payload_lenient(payload)

        if parse_error and parse_error.startswith("shlex_error"):
            cmd = payload
            anchor = _anchor_path_for_command(cmd, project_root)
            new_payload = _render_payload("test", {"path": anchor, "command": cmd})
            new_line = f"{indent}evidence: {new_payload}\n"
            fixes.append(EvidenceFix(idx, line.rstrip("\n"), new_line.rstrip("\n"), f"replaced_unparseable:{parse_error}"))
            lines[idx - 1] = new_line
            continue

        # 3) unsupported types -> strict
        converted, reason = _convert_unsupported_to_strict(hook_type, kv, project_root)
        if converted:
            new_line = f"{indent}evidence: {converted}\n"
            fixes.append(EvidenceFix(idx, line.rstrip("\n"), new_line.rstrip("\n"), reason))
            lines[idx - 1] = new_line
            continue

        # 4) strict normalize/repairs
        repaired_payload, r_reason = _repair_strict(hook_type, kv, project_root)
        new_line = f"{indent}evidence: {repaired_payload}\n"

        if new_line.rstrip("\n") != line.rstrip("\n"):
            fixes.append(EvidenceFix(idx, line.rstrip("\n"), new_line.rstrip("\n"), r_reason))
            lines[idx - 1] = new_line
            continue

        # 5) normalize bullet prefix
        if m_b:
            new_line2 = f"{indent}evidence: {payload}\n"
            fixes.append(EvidenceFix(idx, line.rstrip("\n"), new_line2.rstrip("\n"), "normalized_bullet_evidence"))
            lines[idx - 1] = new_line2

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


def write_report(out_dir: Path, tasks_rel: str, apply: bool, fixes: List[EvidenceFix]) -> None:
    lines: List[str] = []
    lines.append("# migrate-evidence-hooks report\n")
    lines.append(f"\n- tasks: {tasks_rel}\n")
    lines.append(f"- apply: {apply}\n")
    lines.append(f"- fixes: {len(fixes)}\n")
    lines.append("\n## outputs\n")
    lines.append(f"- preview: `{out_dir}/preview/{tasks_rel}`\n")
    lines.append(f"- diff: `{out_dir}/diff.patch`\n")
    lines.append(f"- report: `{out_dir}/report.md`\n")

    if fixes:
        lines.append("\n## changes (first 200)\n")
        for f in fixes[:200]:
            lines.append(f"- L{f.line_no}: {f.reason}\n")
            lines.append(f"  - before: `{f.before.strip()}`\n")
            lines.append(f"  - after:  `{f.after.strip()}`\n")
        if len(fixes) > 200:
            lines.append(f"- ... {len(fixes) - 200} more\n")

    (out_dir / "report.md").write_text("".join(lines), encoding="utf-8")


def ensure_specs_scoped(tasks_file: Path) -> None:
    parts = [p.replace("\\", "/") for p in tasks_file.parts]
    if "specs" not in parts:
        raise SystemExit(f"Refusing: tasks file must be under specs/**. Got: {tasks_file}")


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

    run_id = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    out_dir = Path(args.out) / run_id
    out_dir.mkdir(parents=True, exist_ok=True)

    tasks_rel = tasks_file.as_posix()
    preview_path = out_dir / "preview" / tasks_rel
    preview_path.parent.mkdir(parents=True, exist_ok=True)
    preview_path.write_text(modified, encoding="utf-8")

    diff_text = unified_diff(original, modified, fromfile=f"a/{tasks_rel}", tofile=f"b/{tasks_rel}")
    (out_dir / "diff.patch").write_text(diff_text, encoding="utf-8")

    write_report(out_dir, tasks_rel=tasks_rel, apply=bool(args.apply), fixes=fixes)

    if args.apply:
        backup = tasks_file.with_suffix(tasks_file.suffix + f".backup.{run_id}")
        backup.write_text(original, encoding="utf-8")
        atomic_write(tasks_file, modified)
        print(f"OK: applied {len(fixes)} fixes to {tasks_file}")
        print(f"OK: backup: {backup}")
    else:
        print("OK: preview only (no governed writes)")
        print(f"OK: preview: {preview_path}")

    print(f"OK: report: {out_dir / 'report.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
