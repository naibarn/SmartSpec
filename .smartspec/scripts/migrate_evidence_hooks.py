#!/usr/bin/env python3
"""migrate_evidence_hooks.py (v6.6.2)

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
  - command-ish evidence like `evidence: npm run build`
  - broken strict lines like `evidence: test path="npm run build"`

This script:
- normalizes bullet evidence into canonical `evidence:` (no leading `-`)
- converts unsupported types into strict types
- converts command-ish evidence into `evidence: test path=<anchor> command="..."`
- repairs **test path-as-command** patterns into canonical form

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

# Keys that may legitimately contain whitespace.
SPACE_TOLERANT_KEYS = {"command", "contains", "regex", "heading", "selector", "symbol"}

# Common command prefixes that should NEVER appear as path= values.
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

RE_EVIDENCE_CANON = re.compile(r"^\s*evidence:\s+(?P<payload>.*)$", re.IGNORECASE)
RE_EVIDENCE_BULLET = re.compile(r"^\s*-\s*evidence:\s+(?P<payload>.*)$", re.IGNORECASE)


@dataclass
class EvidenceFix:
    line_no: int
    before: str
    after: str
    reason: str


def _safe_rel_path(p: str) -> str:
    """Normalize a candidate path into repo-relative forward-slash form."""
    p = p.strip().strip('"').strip("'").replace("\\", "/")
    if p.startswith("./"):
        p = p[2:]
    return p


def _is_abs_or_traversal(p: str) -> bool:
    if not p:
        return True
    p = _safe_rel_path(p)
    if p.startswith("/") or re.match(r"^[A-Za-z]:/", p):
        return True
    if ".." in p.split("/"):
        return True
    return False


def _has_glob(p: str) -> bool:
    return any(ch in p for ch in ("*", "?", "[", "]"))


def _first_word(s: str) -> str:
    s = s.strip()
    if not s:
        return ""
    return s.split()[0]


def _quote_if_needed(v: str) -> str:
    v = v.strip()
    if not v:
        return v
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


def _parse_payload_lenient(payload: str) -> Tuple[str, Dict[str, str], List[str], Optional[str]]:
    """Lenient parse that can join stray tokens onto the last whitespace-tolerant key.

    Returns:
      (hook_type, kv, stray_tokens, parse_error)

    Example (broken strict):
      test path=... command=npx prisma validate
    Tokens:
      ['test','path=...','command=npx','prisma','validate']
    We join onto command => command='npx prisma validate'

    Example (broken strict):
      test path=npm run build
    Tokens:
      ['test','path=npm','run','build']
    path is not tolerant, so 'run build' becomes stray_tokens.
    """
    tokens, err = _shlex_split(payload)
    if err:
        return "", {}, [], err
    if not tokens:
        return "", {}, [], "empty_payload"

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
        # Not fatal for us; caller may repair using stray tokens context.
        return hook_type, kv, stray, "stray_tokens"

    return hook_type, kv, [], None


def _anchor_path_for_command(cmd: str, project_root: Path) -> str:
    """Choose a stable file path to anchor test evidence."""
    cmd_l = cmd.lower().strip()

    if cmd_l.startswith(("npm ", "pnpm ", "yarn ", "bun ", "npx ")):
        if (project_root / "package.json").exists():
            return "package.json"
        return "package.json"

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
    """Render payload with stable key ordering (path first) and proper quoting."""
    ht = hook_type.strip().lower()

    ordered_keys: List[str] = []
    if "path" in kv:
        ordered_keys.append("path")
    ordered_keys.extend(sorted(k for k in kv.keys() if k != "path"))

    parts = [ht]
    for k in ordered_keys:
        parts.append(f"{k}={_quote_if_needed(kv[k])}")
    return " ".join(parts)


def _convert_commandish_payload(raw_payload: str, project_root: Path) -> Optional[Tuple[str, str]]:
    """Convert payload that looks like a command (e.g., `npm run build`) into strict test evidence."""
    raw = raw_payload.strip()
    if not raw:
        return None
    if re.match(r"^(code|test|docs|ui)\b", raw, re.IGNORECASE):
        return None

    first = raw.split()[0].lower() if raw.split() else ""
    if first in SUSPICIOUS_PATH_PREFIXES:
        cmd = raw
        anchor = _anchor_path_for_command(cmd, project_root)
        return (_render_payload("test", {"path": anchor, "command": cmd}), "converted_commandish_to_test")

    return None


def _convert_unsupported_to_strict(hook_type: str, kv: Dict[str, str], project_root: Path) -> Tuple[Optional[str], str]:
    """Convert non-strict hook types into strict types.

    Returns: (new_evidence_payload or None, reason)
    """
    ht = hook_type.strip().lower()

    if ht in STRICT_TYPES:
        return None, "already_strict"

    if ht in {"file_exists", "file"}:
        p = kv.get("path") or kv.get("file") or ""
        p = _safe_rel_path(p)
        if not p:
            return None, "missing_path"
        if p.lower().endswith((".md", ".markdown", ".rst", ".txt", ".yaml", ".yml", ".json")):
            return _render_payload("docs", {"path": p}), "mapped_file_exists_to_docs"
        return _render_payload("code", {"path": p}), "mapped_file_exists_to_code"

    if ht in {"api_route", "route", "endpoint"}:
        p = _safe_rel_path(kv.get("path", ""))
        route = kv.get("route") or kv.get("url") or kv.get("endpoint") or ""
        if not route:
            return None, "missing_route"
        if not p:
            anchor = _anchor_path_for_command("openapi", project_root)
            return _render_payload("docs", {"path": anchor, "contains": route}), "mapped_api_route_to_docs_contains"
        return _render_payload("code", {"path": p, "contains": route}), "mapped_api_route_to_code_contains"

    if ht in {"db_schema", "schema", "prisma"}:
        p = _safe_rel_path(kv.get("path", "")) or "prisma/schema.prisma"
        model = kv.get("model") or kv.get("table") or ""
        if model:
            return _render_payload("code", {"path": p, "contains": model}), "mapped_db_schema_to_code_contains"
        return _render_payload("code", {"path": p}), "mapped_db_schema_to_code"

    if ht in {"command", "cmd", "shell"}:
        cmd = kv.get("command") or kv.get("cmd") or ""
        if not cmd:
            return None, "missing_command"
        anchor = _anchor_path_for_command(cmd, project_root)
        return _render_payload("test", {"path": anchor, "command": cmd}), "mapped_command_to_test_command"

    return None, f"unknown_type:{ht}"


def _repair_strict_payload(raw_payload: str, hook_type: str, kv: Dict[str, str], stray: List[str], project_root: Path) -> Tuple[Optional[str], str]:
    """Repair strict evidence that is *syntactically* parseable but *semantically* wrong.

    Primary repair: test path-as-command.
    """
    ht = hook_type.strip().lower()

    if ht not in STRICT_TYPES:
        return None, "not_strict"

    # Ensure path exists
    if "path" not in kv or not kv.get("path"):
        return None, "missing_path"

    raw_path = kv.get("path", "")

    # (A) If path contains whitespace, it's not a path; treat it as a command.
    if re.search(r"\s", raw_path):
        cmd = raw_path.strip('"').strip("'")
        anchor = _anchor_path_for_command(cmd, project_root)
        merged = {"path": anchor, "command": kv.get("command", "") or cmd}
        # drop empty command from kv if present
        if not merged["command"].strip():
            merged["command"] = cmd
        return _render_payload("test", merged), "fixed_test_path_whitespace_to_command"

    path_norm = _safe_rel_path(raw_path)

    # (B) Reject unsafe paths, wrap as test command.
    if _is_abs_or_traversal(path_norm) or _has_glob(path_norm):
        anchor = _anchor_path_for_command(raw_payload, project_root)
        return _render_payload("test", {"path": anchor, "command": raw_payload}), "wrapped_unsafe_path_as_test_command"

    # (C) If path first word or first segment looks like a command, it is a command.
    first_seg = path_norm.split("/", 1)[0].lower() if path_norm else ""
    first_word = _first_word(path_norm).lower() if path_norm else ""
    if first_seg in SUSPICIOUS_PATH_PREFIXES or first_word in SUSPICIOUS_PATH_PREFIXES:
        # if this was `test path=npm run build` the actual command might be reconstructed
        if ht == "test":
            cmd_parts: List[str] = []
            if path_norm:
                cmd_parts.append(path_norm)
            if stray:
                cmd_parts.extend(stray)
            cmd = " ".join(cmd_parts).strip()
            if not cmd:
                cmd = raw_payload
            anchor = _anchor_path_for_command(cmd, project_root)
            return _render_payload("test", {"path": anchor, "command": cmd}), "fixed_test_path_command_token_to_command"

        anchor = _anchor_path_for_command(raw_payload, project_root)
        return _render_payload("test", {"path": anchor, "command": raw_payload}), "wrapped_commandish_path"

    # (D) code+heading for docs-like files => docs
    if ht == "code" and "heading" in kv:
        if path_norm.lower().endswith((".md", ".markdown", ".rst", ".txt", ".yaml", ".yml", ".json")):
            kv2 = dict(kv)
            kv2["path"] = path_norm
            return _render_payload("docs", kv2), "switched_code_to_docs_for_heading"

    # (E) Canonicalize (quotes + ordering + normalized path)
    kv2 = dict(kv)
    kv2["path"] = path_norm
    return _render_payload(ht, kv2), "canonicalized"


def transform_tasks_md(content: str, project_root: Path) -> Tuple[str, List[EvidenceFix]]:
    lines = content.splitlines(keepends=True)
    fixes: List[EvidenceFix] = []

    for idx, line in enumerate(lines, start=1):
        m_b = RE_EVIDENCE_BULLET.match(line)
        m_c = RE_EVIDENCE_CANON.match(line)
        if not (m_b or m_c):
            continue

        raw_payload = (m_b or m_c).group("payload").strip()
        indent = re.match(r"^\s*", line).group(0)

        # 1) command-ish top-level payload
        cmdish = _convert_commandish_payload(raw_payload, project_root)
        if cmdish:
            new_payload, reason = cmdish
            new_line = f"{indent}evidence: {new_payload}\n"
            fixes.append(EvidenceFix(idx, line.rstrip("\n"), new_line.rstrip("\n"), reason))
            lines[idx - 1] = new_line
            continue

        # 2) Parse payload (lenient)
        hook_type, kv, stray, parse_error = _parse_payload_lenient(raw_payload)

        # If shlex fails, salvage by wrapping as test command
        if parse_error and parse_error.startswith("shlex_error"):
            anchor = _anchor_path_for_command(raw_payload, project_root)
            new_payload = _render_payload("test", {"path": anchor, "command": raw_payload})
            new_line = f"{indent}evidence: {new_payload}\n"
            fixes.append(EvidenceFix(idx, line.rstrip("\n"), new_line.rstrip("\n"), f"replaced_unparseable:{parse_error}"))
            lines[idx - 1] = new_line
            continue

        # 3) Convert unsupported types
        converted, reason = _convert_unsupported_to_strict(hook_type, kv, project_root)
        if converted:
            new_line = f"{indent}evidence: {converted}\n"
            fixes.append(EvidenceFix(idx, line.rstrip("\n"), new_line.rstrip("\n"), reason))
            lines[idx - 1] = new_line
            continue

        # 4) Repair/canonicalize strict payloads (including path-as-command)
        repaired, r_reason = _repair_strict_payload(raw_payload, hook_type, kv, stray, project_root)
        if repaired:
            new_line = f"{indent}evidence: {repaired}\n"
            # If original was bullet form, still count as normalized
            reason = r_reason if not m_b else f"{r_reason}+normalized_bullet"
            if new_line.rstrip("\n") != line.rstrip("\n"):
                fixes.append(EvidenceFix(idx, line.rstrip("\n"), new_line.rstrip("\n"), reason))
                lines[idx - 1] = new_line
            elif m_b:
                fixes.append(EvidenceFix(idx, line.rstrip("\n"), new_line.rstrip("\n"), "normalized_bullet"))
                lines[idx - 1] = new_line
            continue

        # 5) Bullet normalization (fallback)
        if m_b:
            new_line = f"{indent}evidence: {raw_payload}\n"
            fixes.append(EvidenceFix(idx, line.rstrip("\n"), new_line.rstrip("\n"), "normalized_bullet"))
            lines[idx - 1] = new_line

    return "".join(lines), fixes


def write_report(out_dir: Path, tasks_rel: str, apply: bool, fixes: List[EvidenceFix]) -> None:
    report_lines: List[str] = []
    report_lines.append("# migrate-evidence-hooks report\n")
    report_lines.append(f"\n- Tasks: {tasks_rel}\n")
    report_lines.append(f"- Apply: {apply}\n")
    report_lines.append(f"- Fixes: {len(fixes)}\n")

    if fixes:
        report_lines.append("\n## Changes (first 300)\n")
        for f in fixes[:300]:
            report_lines.append(f"- L{f.line_no}: {f.reason}\n")
            report_lines.append(f"  - before: `{f.before.strip()}`\n")
            report_lines.append(f"  - after:  `{f.after.strip()}`\n")
        if len(fixes) > 300:
            report_lines.append(f"- ... truncated ({len(fixes) - 300} more)\n")

    report_lines.append("\n## Outputs\n")
    report_lines.append(f"- Preview: {out_dir}/preview/{tasks_rel}\n")
    report_lines.append(f"- Diff: {out_dir}/diff.patch\n")
    report_lines.append(f"- Report: {out_dir}/report.md\n")

    (out_dir / "report.md").write_text("".join(report_lines), encoding="utf-8")


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


def is_specs_scoped(path: Path) -> bool:
    parts = [p.replace("\\", "/") for p in path.parts]
    return "specs" in parts


def is_preview_path(path: Path) -> bool:
    return ".spec" in path.parts and "reports" in path.parts


def main() -> int:
    ap = argparse.ArgumentParser(description="Migrate/normalize evidence hooks in tasks.md (preview-first)")
    ap.add_argument("--tasks-file", required=True, help="Path to specs/**/tasks.md (or a preview file under .spec/reports/**)")
    ap.add_argument("--project-root", default=".", help="Project root (default: .)")
    ap.add_argument("--out", default=".spec/reports/migrate-evidence-hooks", help="Report root (default: .spec/reports/migrate-evidence-hooks)")
    ap.add_argument("--apply", action="store_true", help="Apply changes to governed tasks.md (default: preview only)")
    args = ap.parse_args()

    project_root = Path(args.project_root).resolve()
    tasks_file = Path(args.tasks_file)

    if not project_root.exists():
        print(f"ERROR: project root not found: {project_root}")
        return 2
    if not tasks_file.exists():
        print(f"ERROR: tasks file not found: {tasks_file}")
        return 2

    # Apply safety guards
    if args.apply:
        if is_preview_path(tasks_file):
            print("ERROR: refusing --apply on preview file under .spec/reports/**")
            return 2
        if not is_specs_scoped(tasks_file):
            print(f"ERROR: refusing --apply outside specs/**: {tasks_file}")
            return 2

    original = tasks_file.read_text(encoding="utf-8", errors="ignore")
    modified, fixes = transform_tasks_md(original, project_root)

    run_id = time.strftime("%Y%m%d_%H%M%S")
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
