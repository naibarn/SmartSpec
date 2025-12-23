#!/usr/bin/env python3
"""SmartSpec Migrate Evidence Hooks (Enhanced - Kilo/Antigravity Compatible)

Purpose
-------
Convert legacy/descriptive evidence and non-compliant evidence types in a tasks.md
into verifier-friendly, parseable evidence hooks.

Key improvements in this version
-------------------------------
1) Evidence line parsing is more tolerant:
   - Accepts both "- evidence: ..." and "evidence: ..." (dash optional)
   - Accepts "- **Evidence:** ..." legacy bullet format
   - Task ID no longer requires "TSK-" prefix (uses first token after checkbox)

2) Safer non-compliant conversions:
   - Only converts `command` evidence when we can map it to a real, existing file.
   - If conversion cannot be done safely, we DO NOT modify that line (prevents
     generating misleading hooks that might cause false positives).

3) Apply step preserves the original list marker style:
   - Keeps indentation and whether the original evidence line had a leading "- "

Notes
-----
- This tool is for migrating tasks.md formatting/evidence strings. It does NOT run
  tests/commands (strict verifier should be evidence-only).
- Use preview mode first (default). Use --apply to modify the file.

"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

try:
    import shlex
except Exception:  # pragma: no cover
    shlex = None


NON_COMPLIANT_TYPES: Set[str] = {"file_exists", "test_exists", "command"}


def _now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _norm_rel_path(p: str) -> str:
    """Normalize a likely-relative path to POSIX style (for markdown hooks)."""
    p = (p or "").strip().strip('"\'')
    p = p.replace("\\", "/")
    # collapse duplicate slashes
    p = re.sub(r"/+$", "", p)
    p = re.sub(r"/{2,}", "/", p)
    return p


class ProjectContext:
    """Scans and indexes project files for evidence validation/correction."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.all_files: Set[str] = set()  # POSIX relpaths
        self.symbol_index: Dict[str, List[str]] = {}
        self.package_index: Dict[str, List[str]] = {}
        self._scan_project()

    def _scan_project(self) -> None:
        print("🔍 Scanning project files.")

        ignore_dirs = {
            ".git",
            "node_modules",
            ".next",
            "dist",
            "build",
            "out",
            "coverage",
            "__pycache__",
            ".venv",
            "venv",
            ".spec/reports",
            ".smartspec/cache",
            ".smartspec/logs",
        }

        file_count = 0
        for root, dirs, files in os.walk(self.project_root):
            # Remove ignored directories from search
            rel_root = Path(root).resolve()
            try:
                rel = rel_root.relative_to(self.project_root.resolve()).as_posix()
            except Exception:
                rel = ""

            # Filter dirs
            filtered = []
            for d in dirs:
                cand = (Path(rel) / d).as_posix() if rel else d
                if cand in ignore_dirs or d in ignore_dirs:
                    continue
                filtered.append(d)
            dirs[:] = filtered

            for file in files:
                file_path = Path(root) / file
                try:
                    rel_path = file_path.relative_to(self.project_root).as_posix()
                except Exception:
                    continue

                self.all_files.add(rel_path)
                file_count += 1

                # Index selected source files for symbols/packages
                if file.endswith((".ts", ".tsx", ".js", ".jsx", ".py")):
                    self._index_file(file_path, rel_path)

        print(f"✅ Indexed {file_count} files")
        print(f"✅ Found {len(self.symbol_index)} unique symbols")
        print(f"✅ Found {len(self.package_index)} package references")

    def _index_file(self, file_path: Path, rel_path: str) -> None:
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")

            # TS/JS exports
            for match in re.finditer(
                r"(?:export\s+)?(?:async\s+)?(?:function|class|const|let|var)\s+(\w+)",
                content,
            ):
                sym = match.group(1)
                self.symbol_index.setdefault(sym, []).append(rel_path)

            # Python defs/classes
            for match in re.finditer(r"(?:def|class)\s+(\w+)", content):
                sym = match.group(1)
                self.symbol_index.setdefault(sym, []).append(rel_path)

            # Package imports (small, useful subset)
            packages = [
                "bcrypt",
                "jsonwebtoken",
                "jose",
                "redis",
                "ioredis",
                "bull",
                "bullmq",
                "winston",
                "pino",
                "express",
                "fastify",
                "koa",
            ]
            for pkg in packages:
                # JS/TS imports
                if re.search(rf"from\s+['\"]{re.escape(pkg)}['\"]", content) or re.search(
                    rf"require\(['\"]{re.escape(pkg)}['\"]\)",
                    content,
                ):
                    self.package_index.setdefault(pkg, []).append(rel_path)
                # Python imports
                if re.search(rf"(?:import|from)\s+{re.escape(pkg)}\b", content):
                    self.package_index.setdefault(pkg, []).append(rel_path)
        except Exception:
            return

    def _prefer_root_level(self, candidates: List[str]) -> Optional[str]:
        if not candidates:
            return None
        # Prefer root-level files (no slash), then shortest path
        root_level = [c for c in candidates if "/" not in c]
        if root_level:
            return sorted(root_level, key=len)[0]
        return sorted(candidates, key=len)[0]

    def find_file(self, partial_path: str) -> Optional[str]:
        """Find a file by path or basename; returns normalized relpath if found."""
        partial_path = _norm_rel_path(partial_path)
        if not partial_path:
            return None

        # Exact match
        if partial_path in self.all_files:
            return partial_path

        # Try with common extensions (if user provided no ext)
        base = partial_path
        if Path(base).suffix == "":
            for ext in [
                ".ts",
                ".tsx",
                ".js",
                ".jsx",
                ".py",
                ".json",
                ".yaml",
                ".yml",
                ".md",
                ".toml",
                ".ini",
            ]:
                cand = f"{base}{ext}"
                if cand in self.all_files:
                    return cand

        # Basename match
        basename = Path(partial_path).name
        basename_matches = [f for f in self.all_files if Path(f).name == basename]
        chosen = self._prefer_root_level(basename_matches)
        if chosen:
            return chosen

        # Suffix match (endswith)
        suffix_matches = [f for f in self.all_files if f.endswith(partial_path)]
        chosen = self._prefer_root_level(suffix_matches)
        if chosen:
            return chosen

        return None

    def find_any(self, basenames: List[str]) -> Optional[str]:
        """Find first existing file among candidate basenames."""
        for name in basenames:
            hit = self.find_file(name)
            if hit:
                return hit
        return None

    def find_symbol_file(self, symbol: str) -> Optional[str]:
        symbol = (symbol or "").strip()
        if not symbol:
            return None
        if symbol in self.symbol_index and self.symbol_index[symbol]:
            return self.symbol_index[symbol][0]
        return None

    def find_package_file(self, package: str) -> Optional[str]:
        package = (package or "").strip()
        if not package:
            return None
        for pkg, files in self.package_index.items():
            if pkg.lower() == package.lower() and files:
                return files[0]
        return None


@dataclass
class EvidenceLineStyle:
    indent: str
    list_marker: str  # "- " or "" (dash optional)


@dataclass
class TaskEvidence:
    task_id: str
    title: str
    description: str
    evidence_text: str  # WITHOUT leading "evidence:" prefix for standardized evidence lines
    line_num: int
    raw_line: str
    style: EvidenceLineStyle
    is_non_compliant: bool = False

    suggested_hook: Optional[str] = None  # FULL hook, e.g. "evidence: code path=..."
    validation_reason: Optional[str] = None


def _extract_style(line: str) -> EvidenceLineStyle:
    m = re.match(r"^(\s*)(-\s+)?", line)
    indent = m.group(1) if m else ""
    list_marker = m.group(2) or ""
    return EvidenceLineStyle(indent=indent, list_marker=list_marker)


def parse_tasks_file(file_path: Path) -> List[TaskEvidence]:
    """Parse tasks.md file and collect evidence entries requiring migration."""

    lines = file_path.read_text(encoding="utf-8").splitlines(keepends=True)

    tasks: List[TaskEvidence] = []

    current_task_id: Optional[str] = None
    current_title: Optional[str] = None
    current_description: Optional[str] = None

    # Task line: - [ ] <ID> <Title>
    # (ID is the first token after checkbox; not restricted to TSK-)
    task_pattern = re.compile(r"^\s*-\s*\[[ xX]\]\s+(\S+)\s+(.+?)\s*$")

    # Evidence lines:
    #   - evidence: <type> key=value ...
    #   evidence: <type> ...
    # Dash is optional.
    evidence_pattern = re.compile(r"^\s*(?:-\s*)?evidence:\s*(.+?)\s*$", re.IGNORECASE)

    # Legacy descriptive evidence bullet:
    #   - **Evidence:** <free text>
    descriptive_pattern = re.compile(r"^\s*(?:-\s*)?\*\*Evidence:\*\*\s*(.+?)\s*$")

    for i, line in enumerate(lines, 1):
        task_match = task_pattern.match(line)
        if task_match:
            current_task_id = task_match.group(1).strip()
            current_title = task_match.group(2).strip()
            current_description = current_title
            continue

        if not current_task_id:
            continue

        # Standard evidence line
        ev_match = evidence_pattern.match(line)
        if ev_match:
            ev_body = ev_match.group(1).strip()

            # If the file already had a full hook (unlikely here), strip it
            if ev_body.lower().startswith("evidence:"):
                ev_body = ev_body[9:].strip()

            parts = ev_body.split(maxsplit=1)
            ev_type = parts[0] if parts else ""

            style = _extract_style(line)
            tasks.append(
                TaskEvidence(
                    task_id=current_task_id,
                    title=current_title or "",
                    description=current_description or "",
                    evidence_text=ev_body,
                    line_num=i,
                    raw_line=line,
                    style=style,
                    is_non_compliant=(ev_type in NON_COMPLIANT_TYPES),
                )
            )
            continue

        # Legacy descriptive evidence
        desc_match = descriptive_pattern.match(line)
        if desc_match:
            desc = desc_match.group(1).strip()
            # Only capture if it's NOT already a standardized hook
            if not desc.lower().startswith("evidence:"):
                style = _extract_style(line)
                tasks.append(
                    TaskEvidence(
                        task_id=current_task_id,
                        title=current_title or "",
                        description=current_description or "",
                        evidence_text=desc,
                        line_num=i,
                        raw_line=line,
                        style=style,
                        is_non_compliant=False,
                    )
                )

    return tasks


def _parse_kv(params_str: str) -> Dict[str, str]:
    """Parse key=value pairs; tolerates quoted values."""
    params_str = (params_str or "").strip()
    if not params_str:
        return {}

    # Prefer shlex for quotes if available
    if shlex is not None:
        try:
            tokens = shlex.split(params_str)
            out: Dict[str, str] = {}
            for tok in tokens:
                if "=" not in tok:
                    continue
                k, v = tok.split("=", 1)
                out[k.strip()] = v.strip().strip('"\'')
            if out:
                return out
        except Exception:
            pass

    # Fallback regex
    out: Dict[str, str] = {}
    for match in re.finditer(r"(\w+)=([^\s]+(?:\s+[^\s=]+)*?)(?=\s+\w+=|$)", params_str):
        k = match.group(1)
        v = match.group(2).strip().strip('"\'')
        out[k] = v
    return out


def convert_non_compliant_evidence(
    evidence_text: str, context: ProjectContext
) -> Tuple[Optional[str], str]:
    """Convert non-compliant evidence types into verifier-friendly hooks.

    Returns:
      (suggested_hook | None, reason)

    If None is returned, caller should NOT modify the file for that line.
    """

    evidence_text = (evidence_text or "").strip()
    if not evidence_text:
        return None, "Empty evidence"

    parts = evidence_text.split(maxsplit=1)
    ev_type = parts[0]
    params_str = parts[1] if len(parts) > 1 else ""
    params = _parse_kv(params_str)

    # --- file_exists ---
    if ev_type == "file_exists":
        path = _norm_rel_path(params.get("path", ""))
        if not path:
            return None, "file_exists missing path="

        actual = context.find_file(path)
        if actual:
            path = actual
        # Heuristic: test folder implies test
        if "test" in path.lower() or "__tests__" in path.lower() or path.lower().endswith((".spec.ts", ".test.ts", ".spec.tsx", ".test.tsx", ".spec.js", ".test.js")):
            return f"evidence: test path={path}", "Converted file_exists → test"
        # Docs files
        if path.lower().endswith((".md", ".rst")):
            return f"evidence: docs path={path}", "Converted file_exists → docs"
        return f"evidence: code path={path}", "Converted file_exists → code"

    # --- test_exists ---
    if ev_type == "test_exists":
        path = _norm_rel_path(params.get("path", ""))
        if not path:
            return None, "test_exists missing path="

        actual = context.find_file(path)
        if actual:
            path = actual

        hook = f"evidence: test path={path}"
        name = (params.get("name") or "").strip()
        if name:
            hook += f" contains=\"{name}\""
        return hook, "Converted test_exists → test (name → contains)"

    # --- command ---
    if ev_type == "command":
        cmd = (params.get("cmd") or "").strip()
        if not cmd:
            return None, "command missing cmd="

        cmd_l = cmd.lower()

        # TypeScript compile
        if "tsc" in cmd_l or "typescript" in cmd_l:
            hit = context.find_any(["tsconfig.json", "tsconfig.base.json", "tsconfig.build.json"])
            if hit:
                return f"evidence: code path={hit}", f"Converted command → code ({hit})"
            return None, "No tsconfig found to safely convert tsc command"

        # ESLint
        if "eslint" in cmd_l or re.search(r"\blint\b", cmd_l):
            hit = context.find_any(
                [
                    "eslint.config.js",
                    "eslint.config.mjs",
                    ".eslintrc.js",
                    ".eslintrc.cjs",
                    ".eslintrc.json",
                    ".eslintrc.yaml",
                    ".eslintrc.yml",
                ]
            )
            if hit:
                return f"evidence: code path={hit}", f"Converted command → code ({hit})"
            # fallback to package.json (node lint script)
            pkg = context.find_file("package.json")
            if pkg:
                return f"evidence: code path={pkg} contains=\"scripts\"", "Converted command → code (package.json scripts)"
            return None, "No eslint config/package.json found to safely convert lint command"

        # Prettier
        if "prettier" in cmd_l:
            hit = context.find_any(
                [
                    ".prettierrc",
                    ".prettierrc.json",
                    ".prettierrc.yml",
                    ".prettierrc.yaml",
                    "prettier.config.js",
                    "prettier.config.cjs",
                ]
            )
            if hit:
                return f"evidence: code path={hit}", f"Converted command → code ({hit})"
            return None, "No prettier config found to safely convert prettier command"

        # Jest / Vitest / Pytest
        if "jest" in cmd_l:
            hit = context.find_any(["jest.config.js", "jest.config.ts", "jest.config.cjs", "package.json"])
            if hit:
                return f"evidence: code path={hit}", f"Converted command → code ({hit})"
            return None, "No jest config found to safely convert"

        if "vitest" in cmd_l:
            hit = context.find_any(["vitest.config.ts", "vitest.config.js", "package.json"])
            if hit:
                return f"evidence: code path={hit}", f"Converted command → code ({hit})"
            return None, "No vitest config found to safely convert"

        if "pytest" in cmd_l:
            hit = context.find_any(["pytest.ini", "pyproject.toml", "tox.ini"])
            if hit:
                return f"evidence: code path={hit}", f"Converted command → code ({hit})"
            return None, "No pytest config found to safely convert"

        # Go / Rust / Java
        if re.search(r"\bgo\s+test\b", cmd_l):
            hit = context.find_any(["go.mod"])
            if hit:
                return f"evidence: code path={hit}", "Converted go test → code (go.mod)"
            return None, "No go.mod found to safely convert go test"

        if "cargo test" in cmd_l:
            hit = context.find_any(["Cargo.toml"])
            if hit:
                return f"evidence: code path={hit}", "Converted cargo test → code (Cargo.toml)"
            return None, "No Cargo.toml found to safely convert cargo test"

        if "mvn" in cmd_l or "maven" in cmd_l:
            hit = context.find_any(["pom.xml"])
            if hit:
                return f"evidence: code path={hit}", "Converted mvn → code (pom.xml)"
            return None, "No pom.xml found to safely convert mvn"

        if "gradle" in cmd_l:
            hit = context.find_any(["build.gradle", "build.gradle.kts"])
            if hit:
                return f"evidence: code path={hit}", "Converted gradle → code (build.gradle*)"
            return None, "No build.gradle found to safely convert gradle"

        # Markdownlint (docs)
        if "markdownlint" in cmd_l:
            # If a path param exists, use it; else fall back to README.md if present
            p = _norm_rel_path(params.get("path", ""))
            if p:
                actual = context.find_file(p)
                if actual:
                    return f"evidence: docs path={actual}", "Converted markdownlint → docs (path)"
            readme = context.find_any(["README.md", "readme.md"])
            if readme:
                return f"evidence: docs path={readme}", "Converted markdownlint → docs (README)"
            return None, "No docs file found to safely convert markdownlint"

        # Unknown/unsafe
        return None, "Cannot safely convert command evidence (requires manual migration)"

    return None, f"Unknown non-compliant type: {ev_type}"


def validate_evidence_hook(
    hook: str, context: ProjectContext
) -> Tuple[bool, str, Optional[str]]:
    """Validate an evidence hook and suggest corrections if needed.

    Returns: (is_valid, reason, corrected_hook)
    """

    hook = (hook or "").strip()
    if not hook.startswith("evidence:"):
        return False, "Hook must start with 'evidence:'", None

    parts = hook[9:].strip().split(maxsplit=1)
    if not parts:
        return False, "Missing evidence type", None

    hook_type = parts[0]
    params_str = parts[1] if len(parts) > 1 else ""

    if hook_type in NON_COMPLIANT_TYPES:
        return False, f"Non-compliant type: {hook_type} (not supported by verifier)", None

    params = _parse_kv(params_str)

    # Helper: rewrite with corrected path
    def _rewrite_with_path(new_path: str) -> str:
        new_path = _norm_rel_path(new_path)
        corrected = f"evidence: {hook_type} path={new_path}"
        # preserve optional fields
        for k in ("contains", "heading", "component"):
            if k in params:
                v = params[k]
                if " " in v or "\t" in v:
                    corrected += f" {k}=\"{v}\""
                else:
                    corrected += f" {k}={v}"
        return corrected

    if hook_type in {"code", "test", "docs"}:
        if "path" not in params:
            return False, "Missing required 'path' parameter", None

        orig = _norm_rel_path(params["path"])
        actual = context.find_file(orig)
        if not actual:
            return False, f"File not found: {orig}", None

        if actual != orig:
            return False, f"Path corrected: {orig} -> {actual}", _rewrite_with_path(actual)

        return True, "Valid", None

    if hook_type == "ui":
        # UI verification often needs manual; we can still validate referenced component
        if "component" in params:
            comp = params["component"].strip()
            actual = context.find_symbol_file(comp)
            if not actual:
                return False, f"Component not found: {comp}", None
        return True, "Valid (UI may require manual verification)", None

    # Unknown types are not validated here (the verifier may still support more types)
    return True, "Not validated by migrator (type-specific checks not implemented)", None


def _rewrite_evidence_line(original_line: str, style: EvidenceLineStyle, new_hook: str) -> str:
    """Rewrite a single evidence line while preserving indentation and dash style."""
    # Always write as standardized evidence hook line (not **Evidence:**)
    # Preserve whether original had list marker.
    new_hook = new_hook.strip()
    if not new_hook.startswith("evidence:"):
        new_hook = f"evidence: {new_hook}"
    return f"{style.indent}{style.list_marker}{new_hook}\n"


def apply_changes(file_path: Path, tasks: List[TaskEvidence]) -> None:
    """Apply suggested hook replacements to the tasks file."""

    ts = _now_stamp()
    backup_path = file_path.parent / f"{file_path.stem}.backup.{ts}{file_path.suffix}"
    shutil.copy2(file_path, backup_path)
    print(f"✅ Backup created: {backup_path}")

    try:
        lines = file_path.read_text(encoding="utf-8").splitlines(keepends=True)

        replacements: Dict[int, str] = {}
        styles: Dict[int, EvidenceLineStyle] = {}
        originals: Dict[int, str] = {}

        for t in tasks:
            if t.suggested_hook:
                replacements[t.line_num] = t.suggested_hook
                styles[t.line_num] = t.style
                originals[t.line_num] = t.raw_line

        modified: List[str] = []
        for idx, line in enumerate(lines, 1):
            if idx in replacements:
                modified.append(_rewrite_evidence_line(line, styles[idx], replacements[idx]))
            else:
                modified.append(line)

        file_path.write_text("".join(modified), encoding="utf-8")
        print(f"✅ Applied {len(replacements)} changes to {file_path}")
        print(f"✅ Backup available at: {backup_path}")

    except Exception as e:
        print(f"❌ Error applying changes: {e}")
        print("🔄 Restoring from backup.")
        shutil.copy2(backup_path, file_path)
        print("✅ File restored from backup")
        raise


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Migrate descriptive evidence and fix non-compliant evidence types"
    )
    parser.add_argument("--tasks-file", required=True, help="Path to tasks.md file")
    parser.add_argument(
        "--project-root",
        default=".",
        help="Project root directory for file validation (default: current directory)",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply changes to the file (default: preview only)",
    )
    parser.add_argument(
        "--auto-convert",
        action="store_true",
        help="Automatically convert non-compliant evidence types (no LLM needed)",
    )

    args = parser.parse_args()

    tasks_file = Path(args.tasks_file)
    project_root = Path(args.project_root).resolve()

    if not tasks_file.exists():
        print(f"❌ Error: File not found: {tasks_file}")
        sys.exit(1)
    if not project_root.exists():
        print(f"❌ Error: Project root not found: {project_root}")
        sys.exit(1)

    print(f"📁 Project root: {project_root}")

    context = ProjectContext(project_root)

    print(f"📖 Reading tasks from: {tasks_file}")
    entries = parse_tasks_file(tasks_file)

    if not entries:
        print("✅ No evidence lines found to migrate.")
        sys.exit(0)

    non_compliant = [e for e in entries if e.is_non_compliant]
    descriptive = [e for e in entries if not e.is_non_compliant and not e.evidence_text.lower().startswith(tuple(["code ", "test ", "docs ", "ui "]))]

    print(f"Found {len(non_compliant)} non-compliant evidence hooks")
    print(f"Found {len(descriptive)} descriptive evidence entries")

    proposed: List[TaskEvidence] = []

    # Convert non-compliant evidence
    if non_compliant:
        print("\n🔧 Converting non-compliant evidence types")
        for i, task in enumerate(non_compliant, 1):
            print(f"  [{i}/{len(non_compliant)}] {task.task_id}", end=" ")

            suggested, reason = convert_non_compliant_evidence(task.evidence_text, context)
            if not suggested:
                task.suggested_hook = None
                task.validation_reason = reason
                print("(skip)")
                continue

            # Validate and attempt path correction
            ok, v_reason, corrected = validate_evidence_hook(suggested, context)
            if corrected:
                suggested = corrected
            task.suggested_hook = suggested
            task.validation_reason = f"{reason}; {v_reason}" if v_reason else reason

            if ok:
                proposed.append(task)
                print("✓")
            else:
                # If invalid after correction attempts, do not apply automatically
                task.suggested_hook = None
                print("(invalid)")

    # Descriptive evidence conversion requires an LLM; this script does not implement it.
    if descriptive and not args.auto_convert:
        print("\nℹ️  Descriptive evidence requires AI conversion (not implemented in this script).")
        print("    Use the SmartSpec workflow /smartspec_migrate_evidence_hooks for AI-assisted conversion.")

    # Preview
    if proposed:
        print("\n" + "=" * 80)
        print("PROPOSED CHANGES (showing up to first 20)")
        print("=" * 80)

        for t in proposed[:20]:
            print(f"\nTask: {t.task_id} - {t.title}")
            print("─" * 80)
            print(f"- OLD: evidence: {t.evidence_text}")
            print(f"+ NEW: {t.suggested_hook}")
            if t.validation_reason:
                print(f"  Reason: {t.validation_reason}")
            print("─" * 80)

        if len(proposed) > 20:
            print(f"\n... and {len(proposed) - 20} more changes")

        print(f"\nTotal changes proposed: {len(proposed)}")
    else:
        print("\n✅ No safe changes proposed.")

    # Apply
    if args.apply and proposed:
        print("\n⚠️  You are about to modify the file!")
        print("Countdown: ", end="", flush=True)
        for j in range(3, 0, -1):
            print(f"{j}...", end="", flush=True)
            time.sleep(1)
        print("GO!")

        apply_changes(tasks_file, proposed)
        print("\n✅ Done! Changes applied.")

    elif not args.apply and proposed:
        print("\nTo apply these changes, run with --apply flag")


if __name__ == "__main__":
    main()
