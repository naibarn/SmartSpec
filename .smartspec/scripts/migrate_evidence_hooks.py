#!/usr/bin/env python3
"""migrate_evidence_hooks.py (v6.6.1)

Preview-first normalizer for SmartSpec evidence hooks in tasks.md.

Why you need this
- Strict verifier + validate_evidence_hooks require canonical hooks:

  evidence: <code|test|docs|ui> key=value key="value with spaces" ...

- The biggest real-world breakage is **unquoted values with spaces**:
  - BAD:  evidence: test path=... command=npx prisma validate
  - GOOD: evidence: test path=... command="npx prisma validate"

This script repairs that (and other legacy patterns) deterministically.

Governance (MUST)
- Default: preview-only (no governed writes)
- Governed writes require `--apply`
- Outputs in preview mode only under `.spec/reports/migrate-evidence-hooks/**`
- When `--apply`, only `specs/**/tasks.md` may be updated

Safety
- No network.
- No executing commands.

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

# Keys that may legitimately contain spaces; if tokens are split, we join them.
SPACE_TOLERANT_KEYS = {"command", "contains", "regex", "heading", "selector", "symbol"}

# Heuristic: tokens that should never be interpreted as a file path prefix.
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
    return any(ch in p for ch in ["*", "?", "[", "]"])


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


def _parse_payload_lenient(payload: str) -> Tuple[str, Dict[str, str], Optional[str]]:
    """Lenient parse that repairs unquoted values with spaces.

    Example (broken):
      test path=... command=npx prisma validate
    Tokens:
      ['test','path=...','command=npx','prisma','validate']
    We join stray tokens onto last SPACE_TOLERANT_KEYS key (command).
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

    # normalize path
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
    """Convert payload that is basically a command into strict test evidence."""
    raw = raw_payload.strip()
    if not raw:
        return None

    # Already looks strict
    if re.match(r"^(code|test|docs|ui)\b", raw, re.IGNORECASE):
        return None

    first = raw.split()[0].lower() if raw.split() else ""
    if first in SUSPICIOUS_PATH_PREFIXES:
        anchor = _anchor_path_for_command(raw, project_root)
        return (_render_payload("test", {"path": anchor, "command": raw}), "converted_commandish_to_test")

    return None


def _fix_test_missing_path(ht: str, kv: Dict[str, str], project_root: Path) -> Tuple[Optional[Dict[str, str]], str]:
    if ht != "test":
        return None, "not_test"
    if "path" in kv and kv.get("path"):
        return None, "has_path"

    # if there's a command, add a stable anchor
    cmd = kv.get("command") or ""
    if cmd:
        anchor = _anchor_path_for_command(cmd, project_root)
        kv2 = dict(kv)
        kv2["path"] = anchor
        return kv2, "added_anchor_path_for_test"

    # no command either -> cannot recover
    return None, "missing_path_and_command"


def _maybe_switch_code_heading_to_docs(ht: str, kv: Dict[str, str]) -> Tuple[Optional[Tuple[str, Dict[str, str]]], str]:
    if ht != "code":
        return None, "not_code"
    if "heading" not in kv:
        return None, "no_heading"

    p = kv.get("path", "")
    if p.lower().endswith((".md", ".markdown", ".rst", ".txt", ".yaml", ".yml", ".json")):
        return ("docs", dict(kv)), "switched_code_to_docs_for_heading"

    return None, "not_docs_like_path"


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

        # 1) command-ish line like "npm run build"
        cmdish = _convert_commandish_payload(raw_payload, project_root)
        if cmdish:
            new_payload, reason = cmdish
            new_line = f"{indent}evidence: {new_payload}\n"
            fixes.append(EvidenceFix(idx, line.rstrip("\n"), new_line.rstrip("\n"), reason))
            lines[idx - 1] = new_line
            continue

        # 2) lenient parse (repairs unquoted multi-word values)
        ht, kv, perr = _parse_payload_lenient(raw_payload)
        if perr and perr.startswith("shlex_error"):
            # salvage: wrap whole payload as command
            anchor = _anchor_path_for_command(raw_payload, project_root)
            new_payload = _render_payload("test", {"path": anchor, "command": raw_payload})
            new_line = f"{indent}evidence: {new_payload}\n"
            fixes.append(EvidenceFix(idx, line.rstrip("\n"), new_line.rstrip("\n"), f"replaced_unparseable:{perr}"))
            lines[idx - 1] = new_line
            continue

        ht_l = ht.strip().lower()

        # 3) If it isn't strict, try best-effort conversion by wrapping as test command.
        if ht_l not in STRICT_TYPES:
            anchor = _anchor_path_for_command(raw_payload, project_root)
            new_payload = _render_payload("test", {"path": anchor, "command": raw_payload})
            new_line = f"{indent}evidence: {new_payload}\n"
            fixes.append(EvidenceFix(idx, line.rstrip("\n"), new_line.rstrip("\n"), f"unknown_type_to_test_command:{ht_l}"))
            lines[idx - 1] = new_line
            continue

        # 4) fix test missing path
        if ht_l == "test":
            kv_fix, reason = _fix_test_missing_path(ht_l, kv, project_root)
            if kv_fix:
                new_payload = _render_payload(ht_l, kv_fix)
                new_line = f"{indent}evidence: {new_payload}\n"
                fixes.append(EvidenceFix(idx, line.rstrip("\n"), new_line.rstrip("\n"), reason))
                lines[idx - 1] = new_line
                continue

        # 5) normalize path safety; if unsafe -> wrap as test command
        p = kv.get("path", "")
        p_norm = _safe_rel_path(p)
        if _is_abs_or_traversal(p_norm) or _has_glob(p_norm):
            anchor = _anchor_path_for_command(raw_payload, project_root)
            new_payload = _render_payload("test", {"path": anchor, "command": raw_payload})
            new_line = f"{indent}evidence: {new_payload}\n"
            fixes.append(EvidenceFix(idx, line.rstrip("\n"), new_line.rstrip("\n"), "unsafe_path_wrapped_as_test_command"))
            lines[idx - 1] = new_line
            continue

        kv = dict(kv)
        kv["path"] = p_norm

        first = p_norm.split("/", 1)[0].lower() if p_norm else ""
        if first in SUSPICIOUS_PATH_PREFIXES:
            anchor = _anchor_path_for_command(raw_payload, project_root)
            new_payload = _render_payload("test", {"path": anchor, "command": raw_payload})
            new_line = f"{indent}evidence: {new_payload}\n"
            fixes.append(EvidenceFix(idx, line.rstrip("\n"), new_line.rstrip("\n"), "command_token_in_path_wrapped"))
            lines[idx - 1] = new_line
            continue

        # 6) switch code+heading on docs-like files
        switched, sw_reason = _maybe_switch_code_heading_to_docs(ht_l, kv)
        if switched:
            new_type, new_kv = switched
            new_payload = _render_payload(new_type, new_kv)
            new_line = f"{indent}evidence: {new_payload}\n"
            fixes.append(EvidenceFix(idx, line.rstrip("\n"), new_line.rstrip("\n"), sw_reason))
            lines[idx - 1] = new_line
            continue

        # 7) re-render to canonical (quotes, ordering)
        new_payload = _render_payload(ht_l, kv)
        new_line = f"{indent}evidence: {new_payload}\n"

        # normalize bullet prefix
        if m_b or (new_line.rstrip("\n") != line.rstrip("\n")):
            reason = "normalized_bullet" if m_b else "canonicalized"
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


def main() -> int:
    ap = argparse.ArgumentParser(description="Migrate/normalize evidence hooks in tasks.md (preview-first)")
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

    # Refuse applying to preview files
    if args.apply and ".spec/reports/" in tasks_file.as_posix():
        print("ERROR: refusing --apply on preview file under .spec/reports/**")
        return 2

    if args.apply:
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
