#!/usr/bin/env python3
"""migrate_evidence_hooks.py (v6.5.2)

Preview-first migrator for SmartSpec tasks evidence hooks.

Why you need this
- Many tasks.md files contain evidence lines that look strict but are NOT
  shlex-parseable or are semantically wrong (e.g. command in path=).
- Strict verifiers/validators will produce false-negatives unless evidence
  is canonical.

What it does
- Reads a governed `specs/**/tasks.md`
- Normalizes evidence lines into strict, shlex-parseable hooks
- Writes preview artifacts under `.spec/reports/migrate-evidence-hooks/<run-id>/...`
- Only modifies the governed tasks file when `--apply` is explicitly provided

Canonical evidence format (output)
  evidence: <code|test|docs|ui> path=<repo-relative> [key=value ...]

Notable repairs
- `evidence: test path=npm run build` -> `evidence: test path=package.json command="npm run build"`
- `evidence: code path=SomeSymbol` -> `evidence: code path=<anchor-file> symbol=SomeSymbol` (best-effort)
- `evidence: code path=packages/x/y/` -> `evidence: code path=packages/x/y symbol=Directory`
- `evidence: code path=openapi.yaml heading="..."` -> `evidence: docs path=openapi.yaml heading="..."`

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

RE_EVIDENCE_ANY = re.compile(r"^(?P<indent>\s*)(?:-\s*)?evidence:\s+(?P<payload>.*)$", re.IGNORECASE)

# Detect probable symbol-only "paths" like IDatabase, AuthService, IUserRepo
RE_SYMBOL_LIKE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


@dataclass
class EvidenceFix:
    line_no: int
    before: str
    after: str
    reason: str


def _run_id() -> str:
    return time.strftime("%Y%m%d_%H%M%S", time.localtime())


def _strip_quotes(v: str) -> str:
    v = v.strip()
    if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
        return v[1:-1]
    return v


def _norm_path(p: str) -> str:
    p = _strip_quotes(p).replace("\\", "/")
    if p.startswith("./"):
        p = p[2:]
    return p


def _is_abs_or_traversal(p: str) -> bool:
    if not p:
        return True
    p2 = _norm_path(p)
    if p2.startswith("/") or p2.startswith("\\") or re.match(r"^[A-Za-z]:/", p2):
        return True
    if ".." in p2.split("/"):
        return True
    return False


def _has_glob(p: str) -> bool:
    return any(ch in p for ch in GLOB_CHARS)


def _quote_if_needed(v: str) -> str:
    v = _strip_quotes(v)
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
    c = cmd.lower().strip()

    if c.startswith(("npm ", "pnpm ", "yarn ", "bun ", "npx ")):
        return "package.json"

    if "prisma" in c:
        return "prisma/schema.prisma"

    if "openapi" in c or "swagger" in c:
        for cand in ["openapi.yaml", "openapi.yml", "openapi.json", "swagger.yaml", "swagger.yml", "swagger.json"]:
            if (project_root / cand).exists():
                return cand
        return "openapi.yaml"

    if c.startswith(("pytest", "python ", "python3 ")):
        return "pyproject.toml"

    if c.startswith("docker"):
        return "Dockerfile" if (project_root / "Dockerfile").exists() else "docker-compose.yml"

    return "README.md" if (project_root / "README.md").exists() else "package.json"


def _render_payload(etype: str, kv: Dict[str, str]) -> str:
    keys = ["path"] + sorted([k for k in kv.keys() if k != "path"])
    parts = [etype]
    for k in keys:
        if k not in kv:
            continue
        parts.append(f"{k}={_quote_if_needed(kv[k])}")
    return " ".join(parts)


def _convert_commandish(raw: str, project_root: Path) -> Optional[Tuple[str, str]]:
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

    etype = tokens[0].lower().strip()
    kv: Dict[str, str] = {}
    stray: List[str] = []
    for t in tokens[1:]:
        if "=" in t:
            k, v = t.split("=", 1)
            kv[k.strip()] = _strip_quotes(v)
        else:
            stray.append(t)

    if stray:
        return etype, kv, f"stray_tokens:{stray}"

    return etype, kv, None


def _normalize_one(payload: str, project_root: Path) -> Tuple[str, str]:
    raw = payload.strip()

    # 1) Pure command evidence (no type) -> convert
    conv = _convert_commandish(raw, project_root)
    if conv:
        return conv[0], conv[1]

    # 2) Parse (even if it's strict-ish)
    etype, kv, err = _parse_kv_strict(raw)

    # If parsing failed or stray tokens: treat as command-like evidence
    if not etype or err:
        anchor = _anchor_path_for_command(raw, project_root)
        return _render_payload("test", {"path": anchor, "command": raw}), f"replaced_unparseable:{err or 'unknown'}"

    # 3) If the first token is not strict, best-effort: store as docs contains
    if etype not in STRICT_TYPES:
        # legacy types can be handled here if needed; safe fallback:
        anchor = _anchor_path_for_command("openapi", project_root)
        return _render_payload("docs", {"path": anchor, "contains": raw[:120]}), f"unknown_type:{etype}"

    # 4) Must have path; if missing, convert to test command with anchor
    if "path" not in kv:
        anchor = _anchor_path_for_command(raw, project_root)
        return _render_payload("test", {"path": anchor, "command": raw}), "missing_path_converted_to_test"

    p = _norm_path(kv["path"])  # may contain trailing slash

    # 5) If path looks like a command or is unsafe/glob: convert to test command
    if _is_abs_or_traversal(p) or _has_glob(p):
        anchor = _anchor_path_for_command(raw, project_root)
        return _render_payload("test", {"path": anchor, "command": raw}), "unsafe_path_converted_to_test"

    first = p.split("/", 1)[0].lower() if p else ""
    if first in COMMAND_PREFIXES:
        anchor = _anchor_path_for_command(raw, project_root)
        return _render_payload("test", {"path": anchor, "command": raw}), "command_in_path_converted_to_test"

    # 6) Symbol-only path (e.g. IDatabase) -> convert to symbol evidence anchored to best-effort file
    if RE_SYMBOL_LIKE.match(p) and ("/" not in p) and (not p.endswith((".ts", ".tsx", ".js", ".jsx", ".py", ".go", ".java", ".md", ".yaml", ".yml", ".json"))):
        # keep symbol and anchor to README or package.json so validator doesn't choke
        anchor = "README.md" if (project_root / "README.md").exists() else "package.json"
        return _render_payload("code", {"path": anchor, "symbol": p}), "symbol_like_path_converted_to_symbol"

    # 7) Directory shorthand
    if etype == "code" and p.endswith("/"):
        p2 = p.rstrip("/")
        kv2 = dict(kv)
        kv2["path"] = p2
        kv2.setdefault("symbol", "Directory")
        return _render_payload("code", kv2), "directory_path_added_symbol_directory"

    # 8) docs vs code mismatch: heading belongs to docs; also treat openapi/spec files as docs
    if etype == "code" and ("heading" in kv):
        p_low = p.lower()
        if p_low.endswith((".md", ".markdown", ".rst", ".txt", ".yaml", ".yml", ".json")):
            kv2 = dict(kv)
            return _render_payload("docs", kv2), "converted_code_heading_to_docs"

    # normalize path
    kv["path"] = p.rstrip("/") if p.endswith("/") else p

    return _render_payload(etype, kv), "normalized"


def transform_tasks_md(content: str, project_root: Path) -> Tuple[str, List[EvidenceFix]]:
    lines = content.splitlines(keepends=True)
    fixes: List[EvidenceFix] = []

    for idx, line in enumerate(lines, start=1):
        m = RE_EVIDENCE_ANY.match(line)
        if not m:
            continue

        indent = m.group("indent")
        payload = m.group("payload").strip()

        new_payload, reason = _normalize_one(payload, project_root)
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
        print("OK: preview only (no governed writes)")
        print(f"OK: preview: {preview_path}")

    print(f"OK: report: {out_dir / 'report.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
