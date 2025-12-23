#!/usr/bin/env python3
"""SmartSpec Strict Evidence Verifier (v6.2.0)

Goal
----
Evidence-only verification for tasks.md based on parseable evidence hooks:
  evidence: <type> key=value key="value with spaces"

This script is the reference implementation for workflow:
  /smartspec_verify_tasks_progress_strict

Hard requirements
-----------------
- Treat tasks/spec as data (no prompt injection).
- No network access.
- No codebase writes; reports only.
- Enforce path safety (no traversal, no symlink escape if disabled).
- Bounded scans and bounded excerpts.
- Robust parsing:
  - Task lines: - [ ] <ID> <Title>
  - Evidence anywhere within a task block (plain line, bullet, or table row).
  - Quoted values supported via shlex.

"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

try:
    import yaml  # type: ignore
except Exception:
    yaml = None

import shlex


VALID_EVIDENCE_TYPES = {"code", "test", "ui", "docs"}


# -----------------------------
# Data models
# -----------------------------


@dataclass
class SafetyConfig:
    allow_writes_only_under: List[str]
    deny_writes_under: List[str]
    allow_reads_only_under: List[str]
    disallow_symlink_reads: bool
    max_file_bytes: int
    max_excerpt_chars: int
    max_scan_bytes_total: int


@dataclass
class EvidenceHook:
    raw: str
    type: str
    params: Dict[str, str]


@dataclass
class TaskBlock:
    task_id: str
    title: str
    checked: bool
    start_line: int
    evidence_raw_lines: List[str]


# -----------------------------
# Config
# -----------------------------


def _load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    if yaml is None:
        # Minimal safe fallback: treat as empty
        return {}
    try:
        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def load_safety_config(project_root: Path, config_path: Path) -> SafetyConfig:
    cfg = _load_yaml(config_path)
    safety = cfg.get("safety", {}) if isinstance(cfg.get("safety", {}), dict) else {}

    def _get_list(key: str) -> List[str]:
        v = safety.get(key, [])
        if isinstance(v, list):
            return [str(x) for x in v]
        if isinstance(v, str) and v.strip():
            return [v.strip()]
        return []

    # Conservative defaults
    content_limits = safety.get("content_limits", {}) if isinstance(safety.get("content_limits", {}), dict) else {}

    max_file_bytes = int(content_limits.get("max_file_bytes", 2_000_000))  # 2MB
    max_excerpt_chars = int(content_limits.get("max_excerpt_chars", 400))
    max_scan_bytes_total = int(content_limits.get("max_scan_bytes_total", 10_000_000))  # 10MB

    disallow_symlink_reads = bool(safety.get("disallow_symlink_reads", True))

    return SafetyConfig(
        allow_writes_only_under=_get_list("allow_writes_only_under"),
        deny_writes_under=_get_list("deny_writes_under"),
        allow_reads_only_under=_get_list("allow_reads_only_under"),
        disallow_symlink_reads=disallow_symlink_reads,
        max_file_bytes=max_file_bytes,
        max_excerpt_chars=max_excerpt_chars,
        max_scan_bytes_total=max_scan_bytes_total,
    )


# -----------------------------
# Path safety
# -----------------------------


def _is_subpath(child: Path, parent: Path) -> bool:
    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except Exception:
        return False


def _safe_relpath(p: str) -> str:
    p = (p or "").strip().strip('"\'')
    p = p.replace("\\", "/")
    p = re.sub(r"/{2,}", "/", p)
    return p


def validate_tasks_path(tasks_path: Path, project_root: Path) -> None:
    if not tasks_path.exists():
        raise ValueError(f"tasks.md not found: {tasks_path}")

    # Must be under specs/**
    specs_root = project_root / "specs"
    if not _is_subpath(tasks_path, specs_root):
        raise ValueError("tasks.md must be under specs/**")

    # No symlink escape
    if tasks_path.is_symlink():
        raise ValueError("tasks.md must not be a symlink")


def validate_out_dir(out_dir: Path, project_root: Path, safety: SafetyConfig) -> None:
    # Normalize to project root
    out_dir = out_dir if out_dir.is_absolute() else (project_root / out_dir)

    # Must be inside project root
    if not _is_subpath(out_dir, project_root):
        raise ValueError("out dir must be under project root")

    # Denylist
    for deny in safety.deny_writes_under:
        deny_path = project_root / deny
        if _is_subpath(out_dir, deny_path):
            raise ValueError(f"out dir under denylist: {deny}")

    # Allowlist (if present)
    if safety.allow_writes_only_under:
        ok = False
        for allow in safety.allow_writes_only_under:
            allow_path = project_root / allow
            if _is_subpath(out_dir, allow_path):
                ok = True
                break
        if not ok:
            raise ValueError("out dir not under allowlist")


def validate_read_path(rel_path: str, project_root: Path, safety: SafetyConfig) -> Tuple[Path, str]:
    rel = _safe_relpath(rel_path)
    if not rel:
        raise ValueError("empty path")
    if rel.startswith("/") or re.match(r"^[a-zA-Z]:/", rel):
        raise ValueError("absolute paths are not allowed")
    if ".." in Path(rel).parts:
        raise ValueError("path traversal is not allowed")

    p = (project_root / rel).resolve()
    if not _is_subpath(p, project_root):
        raise ValueError("resolved path escapes project root")

    if safety.allow_reads_only_under:
        ok = False
        for allow in safety.allow_reads_only_under:
            allow_path = (project_root / allow).resolve()
            if _is_subpath(p, allow_path):
                ok = True
                break
        if not ok:
            raise ValueError("read path not under allowlist")

    # symlink check: refuse if any component is a symlink
    if safety.disallow_symlink_reads:
        cur = project_root.resolve()
        for part in Path(rel).parts:
            cur = (cur / part)
            if cur.exists() and cur.is_symlink():
                raise ValueError("symlink reads are disallowed")

    return p, rel


# -----------------------------
# Parsing helpers
# -----------------------------


_TASK_LINE_RE = re.compile(r"^\s*-\s*\[([ xX])\]\s+(\S+)(?:\s+(.*?))?\s*$")


def parse_spec_id(tasks_text: str, tasks_path: Path) -> str:
    # 1) Table header: | spec-id | ... | then next row contains value
    lines = tasks_text.splitlines()
    for i, line in enumerate(lines[:-1]):
        if "|" in line and "spec-id" in line.lower():
            # try next row
            nxt = lines[i + 1]
            cells = [c.strip() for c in nxt.strip().strip("|").split("|")]
            if cells and cells[0] and cells[0] != "<spec-id>":
                return cells[0].strip("` ")

    # 2) YAML-ish: spec_id: xxx
    m = re.search(r"^\s*spec[_-]id\s*:\s*([a-zA-Z0-9_\-]+)\s*$", tasks_text, re.MULTILINE)
    if m:
        return m.group(1)

    # 3) from folder name specs/<cat>/<spec-id>/tasks.md
    try:
        return tasks_path.parent.name
    except Exception:
        return "unknown"


def extract_task_blocks(tasks_text: str) -> List[TaskBlock]:
    lines = tasks_text.splitlines()
    blocks: List[TaskBlock] = []

    current: Optional[TaskBlock] = None

    def _flush() -> None:
        nonlocal current
        if current:
            blocks.append(current)
        current = None

    for idx, line in enumerate(lines, 1):
        m = _TASK_LINE_RE.match(line)
        if m:
            _flush()
            checked = m.group(1).lower() == "x"
            task_id = m.group(2)
            title = (m.group(3) or "").strip()
            current = TaskBlock(task_id=task_id, title=title, checked=checked, start_line=idx, evidence_raw_lines=[])
            continue

        if current is None:
            continue

        # Evidence can appear anywhere in the task block: bullet, plain, or in tables.
        if "evidence:" in line.lower():
            # May contain multiple evidence occurrences; capture each starting at evidence:
            low = line.lower()
            start = 0
            while True:
                pos = low.find("evidence:", start)
                if pos < 0:
                    break
                frag = line[pos:].strip()
                # Strip common table trailing pipes
                frag = frag.rstrip().rstrip("|").rstrip()
                current.evidence_raw_lines.append(frag)
                start = pos + len("evidence:")

    _flush()
    return blocks


def parse_evidence_hook(raw: str) -> EvidenceHook:
    raw = raw.strip()
    if not raw.lower().startswith("evidence:"):
        raise ValueError("not an evidence hook")

    payload = raw[len("evidence:") :].strip()
    if not payload:
        raise ValueError("empty evidence")

    # Use shlex to support quotes.
    tokens = shlex.split(payload)
    if not tokens:
        raise ValueError("cannot parse")

    ev_type = tokens[0]
    if ev_type not in VALID_EVIDENCE_TYPES:
        raise ValueError(f"invalid evidence type: {ev_type}")

    params: Dict[str, str] = {}
    for t in tokens[1:]:
        if "=" not in t:
            continue
        k, v = t.split("=", 1)
        params[k.strip()] = v.strip()

    return EvidenceHook(raw=raw, type=ev_type, params=params)


# -----------------------------
# Matching
# -----------------------------


def _read_text_bounded(path: Path, max_bytes: int) -> str:
    # Read as bytes then decode, bounded.
    data = path.read_bytes()[:max_bytes]
    try:
        return data.decode("utf-8", errors="ignore")
    except Exception:
        return ""


def match_code_evidence(hook: EvidenceHook, project_root: Path, safety: SafetyConfig, scan_budget: Dict[str, int]) -> Dict[str, Any]:
    params = hook.params
    if "path" not in params:
        return {"matched": False, "scope": "invalid", "why": "missing path"}

    rel_path = params["path"]
    try:
        abs_path, rel_norm = validate_read_path(rel_path, project_root, safety)
    except Exception as e:
        return {"matched": False, "scope": "invalid_scope", "why": str(e)}

    if not abs_path.exists():
        return {"matched": False, "scope": "ok", "why": f"file not found: {rel_norm}"}

    if abs_path.is_dir():
        # Bounded directory scan for contains/symbol.
        contains = params.get("contains")
        symbol = params.get("symbol")
        if not (contains or symbol):
            return {"matched": False, "scope": "ok", "why": "path is a directory; provide contains= or symbol= for strict match", "confidence": "low"}

        matched = False
        excerpt = None
        scanned_bytes = 0

        for root, _, files in os.walk(abs_path):
            for fn in files:
                p = Path(root) / fn
                # Budget
                if scan_budget["bytes"] <= 0:
                    return {"matched": False, "scope": "ok", "why": "scan budget exceeded", "confidence": "low"}

                try:
                    if p.stat().st_size > safety.max_file_bytes:
                        continue
                    text = _read_text_bounded(p, min(safety.max_file_bytes, scan_budget["bytes"]))
                    scanned_bytes += min(len(text.encode("utf-8", errors="ignore")), scan_budget["bytes"])
                    scan_budget["bytes"] -= scanned_bytes
                except Exception:
                    continue

                if symbol and re.search(rf"\b{re.escape(symbol)}\b", text):
                    matched = True
                    excerpt = f"symbol '{symbol}' found in {p.relative_to(project_root).as_posix()}"
                    break
                if contains and contains in text:
                    matched = True
                    excerpt = f"contains match in {p.relative_to(project_root).as_posix()}"
                    break

            if matched:
                break

        if matched:
            return {"matched": True, "scope": "ok", "why": "matched", "confidence": "high", "excerpt": excerpt}
        return {"matched": False, "scope": "ok", "why": "no match in directory scan", "confidence": "low"}

    # File
    try:
        size = abs_path.stat().st_size
    except Exception:
        size = 0

    if size > safety.max_file_bytes:
        return {"matched": False, "scope": "ok", "why": f"file too large (> {safety.max_file_bytes} bytes)", "confidence": "low"}

    # If no contains/symbol, we treat as medium (exists only)
    symbol = params.get("symbol")
    contains = params.get("contains")
    if not symbol and not contains:
        return {"matched": True, "scope": "ok", "why": "file exists (no symbol/contains provided)", "confidence": "medium"}

    # Bounded read
    if scan_budget["bytes"] <= 0:
        return {"matched": False, "scope": "ok", "why": "scan budget exceeded", "confidence": "low"}

    text = _read_text_bounded(abs_path, min(safety.max_file_bytes, scan_budget["bytes"]))
    scan_budget["bytes"] -= min(len(text.encode("utf-8", errors="ignore")), scan_budget["bytes"])  # conservative

    if symbol and re.search(rf"\b{re.escape(symbol)}\b", text):
        return {"matched": True, "scope": "ok", "why": f"symbol '{symbol}' found", "confidence": "high"}
    if contains and contains in text:
        return {"matched": True, "scope": "ok", "why": "contains found", "confidence": "high"}

    return {"matched": False, "scope": "ok", "why": "file exists but symbol/contains not found", "confidence": "medium"}


def match_test_evidence(hook: EvidenceHook, project_root: Path, safety: SafetyConfig, scan_budget: Dict[str, int]) -> Dict[str, Any]:
    # Same semantics as code, but default path existence is medium.
    params = hook.params
    if "path" not in params:
        return {"matched": False, "scope": "invalid", "why": "missing path"}

    rel_path = params["path"]
    try:
        abs_path, rel_norm = validate_read_path(rel_path, project_root, safety)
    except Exception as e:
        return {"matched": False, "scope": "invalid_scope", "why": str(e)}

    if not abs_path.exists() or abs_path.is_dir():
        return {"matched": False, "scope": "ok", "why": f"test file not found: {rel_norm}", "confidence": "low"}

    try:
        size = abs_path.stat().st_size
    except Exception:
        size = 0

    if size > safety.max_file_bytes:
        return {"matched": False, "scope": "ok", "why": f"file too large (> {safety.max_file_bytes} bytes)", "confidence": "low"}

    contains = params.get("contains")
    if not contains:
        return {"matched": True, "scope": "ok", "why": "file exists (no contains provided)", "confidence": "medium"}

    if scan_budget["bytes"] <= 0:
        return {"matched": False, "scope": "ok", "why": "scan budget exceeded", "confidence": "low"}

    text = _read_text_bounded(abs_path, min(safety.max_file_bytes, scan_budget["bytes"]))
    scan_budget["bytes"] -= min(len(text.encode("utf-8", errors="ignore")), scan_budget["bytes"])

    if contains in text:
        return {"matched": True, "scope": "ok", "why": "contains found", "confidence": "high"}

    return {"matched": False, "scope": "ok", "why": "file exists but contains not found", "confidence": "medium"}


def match_docs_evidence(hook: EvidenceHook, project_root: Path, safety: SafetyConfig, scan_budget: Dict[str, int]) -> Dict[str, Any]:
    params = hook.params
    if "path" not in params:
        return {"matched": False, "scope": "invalid", "why": "missing path"}

    rel_path = params["path"]
    try:
        abs_path, rel_norm = validate_read_path(rel_path, project_root, safety)
    except Exception as e:
        return {"matched": False, "scope": "invalid_scope", "why": str(e)}

    if not abs_path.exists() or abs_path.is_dir():
        return {"matched": False, "scope": "ok", "why": f"docs file not found: {rel_norm}", "confidence": "low"}

    try:
        size = abs_path.stat().st_size
    except Exception:
        size = 0

    if size > safety.max_file_bytes:
        return {"matched": False, "scope": "ok", "why": f"file too large (> {safety.max_file_bytes} bytes)", "confidence": "low"}

    heading = params.get("heading")
    contains = params.get("contains")

    if not heading and not contains:
        return {"matched": True, "scope": "ok", "why": "file exists (no heading/contains provided)", "confidence": "medium"}

    if scan_budget["bytes"] <= 0:
        return {"matched": False, "scope": "ok", "why": "scan budget exceeded", "confidence": "low"}

    text = _read_text_bounded(abs_path, min(safety.max_file_bytes, scan_budget["bytes"]))
    scan_budget["bytes"] -= min(len(text.encode("utf-8", errors="ignore")), scan_budget["bytes"])

    if heading:
        # naive heading match: markdown heading line contains heading text
        pat = re.compile(rf"^\s*#+\s+.*{re.escape(heading)}.*$", re.IGNORECASE | re.MULTILINE)
        if pat.search(text):
            return {"matched": True, "scope": "ok", "why": "heading found", "confidence": "high"}

    if contains and contains in text:
        return {"matched": True, "scope": "ok", "why": "contains found", "confidence": "high"}

    return {"matched": False, "scope": "ok", "why": "file exists but heading/contains not found", "confidence": "medium"}


def match_ui_evidence(hook: EvidenceHook, project_root: Path, safety: SafetyConfig, scan_budget: Dict[str, int]) -> Dict[str, Any]:
    # UI evidence is generally manual unless component can be found in code.
    params = hook.params
    screen = params.get("screen")
    component = params.get("component")

    if not screen:
        return {"matched": False, "scope": "invalid", "why": "missing screen"}

    if not component:
        return {"matched": False, "scope": "needs_manual", "why": "UI evidence requires manual validation (no component provided)", "confidence": "low"}

    # Bounded repo scan for component symbol. Prefer shallow scan to avoid big repos.
    # Only scan common UI roots if present.
    candidate_roots = [
        project_root / "apps",
        project_root / "packages",
        project_root / "src",
    ]

    def _iter_files() -> Iterable[Path]:
        for root in candidate_roots:
            if not root.exists() or not root.is_dir():
                continue
            for r, dirs, files in os.walk(root):
                # prune heavy dirs
                dirs[:] = [d for d in dirs if d not in {"node_modules", "dist", "build", ".next", "coverage"}]
                for fn in files:
                    if fn.endswith((".tsx", ".ts", ".jsx", ".js")):
                        yield Path(r) / fn

    sym_pat = re.compile(rf"\b{re.escape(component)}\b")

    for p in _iter_files():
        if scan_budget["bytes"] <= 0:
            return {"matched": False, "scope": "needs_manual", "why": "scan budget exceeded", "confidence": "low"}
        try:
            if p.stat().st_size > safety.max_file_bytes:
                continue
            text = _read_text_bounded(p, min(safety.max_file_bytes, scan_budget["bytes"]))
            scan_budget["bytes"] -= min(len(text.encode("utf-8", errors="ignore")), scan_budget["bytes"])
        except Exception:
            continue

        if sym_pat.search(text):
            rel = p.relative_to(project_root).as_posix()
            return {"matched": True, "scope": "ok", "why": f"component symbol '{component}' found in {rel}", "confidence": "medium"}

    return {"matched": False, "scope": "needs_manual", "why": f"component '{component}' not found in bounded scan", "confidence": "low"}


# -----------------------------
# Suggestions
# -----------------------------


def suggest_hooks(task: TaskBlock) -> List[str]:
    # Minimal, conservative suggestions.
    # (Real improvements should be done in tasks.md via generator or migration workflow.)
    base = task.task_id
    if "ui" in task.title.lower():
        return [f"evidence: ui screen={base} states=loading,error,success"]
    return [
        f"evidence: code path=<repo/rel/file> contains=\"{base}\"",
        f"evidence: test path=<repo/rel/test-file> contains=\"{base}\"",
    ]


# -----------------------------
# Reporting
# -----------------------------


def _run_id(tasks_path: Path) -> str:
    h = hashlib.sha256(str(tasks_path).encode("utf-8")).hexdigest()[:8]
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"verify_{ts}_{h}"


def write_report_md(out_dir: Path, results: Dict[str, Any]) -> None:
    lines: List[str] = []
    lines.append(f"# SmartSpec Strict Verify Report\n")
    lines.append(f"- **Workflow:** {results['workflow']}\n")
    lines.append(f"- **Version:** {results['version']}\n")
    lines.append(f"- **Generated:** {results['generated_at']}\n")
    lines.append(f"- **Run ID:** {results['run_id']}\n")
    lines.append(f"- **Tasks:** `{results['inputs']['tasks_path']}`\n")
    lines.append(f"- **Spec ID:** `{results['inputs']['spec_id']}`\n\n")

    t = results["totals"]
    lines.append("## Summary\n\n")
    lines.append("| Metric | Count |\n|---|---:|\n")
    lines.append(f"| Total Tasks | {t['tasks']} |\n")
    lines.append(f"| Verified Done | {t['verified']} |\n")
    lines.append(f"| Not Verified | {t['not_verified']} |\n")
    lines.append(f"| Needs Manual | {t['manual']} |\n")
    lines.append(f"| Missing Hooks | {t['missing_hooks']} |\n")
    lines.append(f"| Invalid Scope | {t['invalid_scope']} |\n\n")

    def _section(title: str, items: List[Dict[str, Any]]) -> None:
        if not items:
            return
        lines.append(f"## {title}\n\n")
        for it in items:
            lines.append(f"### {it['task_id']} — {it['title']}\n\n")
            lines.append(f"- Checked: `{it['checked']}`\n")
            lines.append(f"- Status: `{it['status']}`\n")
            lines.append(f"- Confidence: `{it['confidence']}`\n")
            lines.append(f"- Why: {it['why']}\n")
            if it.get("evidence"):
                lines.append("- Evidence:\n")
                for ev in it["evidence"]:
                    lines.append(f"  - `{ev['raw']}` → matched={ev['matched']} scope={ev['scope']} confidence={ev['confidence']}\n")
                    if ev.get("why"):
                        lines.append(f"    - why: {ev['why']}\n")
                    if ev.get("excerpt"):
                        lines.append(f"    - excerpt: {ev['excerpt']}\n")
            if it.get("suggested_hooks"):
                lines.append("- Suggested hooks:\n")
                for h in it["suggested_hooks"]:
                    lines.append(f"  - `{h}`\n")
            lines.append("\n")

    res = results["results"]
    _section("✅ Verified", [x for x in res if x["status"] == "verified"])
    _section("❌ Not Verified", [x for x in res if x["status"] == "not_verified"])
    _section("👁️ Needs Manual", [x for x in res if x["status"] == "needs_manual"])
    _section("⚠️ Missing Hooks", [x for x in res if x["status"] == "missing_hooks"])
    _section("⛔ Invalid Scope", [x for x in res if x["status"] == "invalid_scope"])

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "report.md").write_text("".join(lines), encoding="utf-8")


# -----------------------------
# Main
# -----------------------------


def main() -> int:
    ap = argparse.ArgumentParser(description="SmartSpec strict evidence-only verifier")
    ap.add_argument("tasks", help="Path to tasks.md (must be under specs/**)")
    ap.add_argument("--project-root", default=".", help="Project root (default: .)")
    ap.add_argument("--config", default=".spec/smartspec.config.yaml", help="Config path")
    ap.add_argument("--out", default=".spec/reports/verify-tasks-progress", help="Output root (reports)")
    ap.add_argument("--report-format", default="both", choices=["md", "json", "both"], help="Report format")
    ap.add_argument("--json", action="store_true", help="Emit summary.json")
    ap.add_argument("--quiet", action="store_true", help="Reduce logs")

    args = ap.parse_args()

    project_root = Path(args.project_root).resolve()
    tasks_path = Path(args.tasks).resolve()
    config_path = (project_root / args.config).resolve() if not Path(args.config).is_absolute() else Path(args.config).resolve()

    safety = load_safety_config(project_root, config_path)

    try:
        validate_tasks_path(tasks_path, project_root)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    out_root = Path(args.out)
    out_root_abs = (project_root / out_root).resolve() if not out_root.is_absolute() else out_root.resolve()

    try:
        validate_out_dir(out_root_abs, project_root, safety)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    tasks_text = tasks_path.read_text(encoding="utf-8", errors="ignore")
    spec_id = parse_spec_id(tasks_text, tasks_path)

    blocks = extract_task_blocks(tasks_text)

    scan_budget = {"bytes": safety.max_scan_bytes_total}

    results: List[Dict[str, Any]] = []
    totals = {"tasks": 0, "verified": 0, "not_verified": 0, "manual": 0, "missing_hooks": 0, "invalid_scope": 0}

    allow_medium_verified = False
    # Optional config override: safety.verify.allow_medium
    cfg = _load_yaml(config_path)
    try:
        allow_medium_verified = bool(cfg.get("safety", {}).get("verify", {}).get("allow_medium_verified", False))
    except Exception:
        allow_medium_verified = False

    for tb in blocks:
        totals["tasks"] += 1

        task_res: Dict[str, Any] = {
            "task_id": tb.task_id,
            "title": tb.title,
            "checked": tb.checked,
            "verified": False,
            "confidence": "low",
            "status": "not_verified",
            "why": "",
            "evidence": [],
            "suggested_hooks": [],
        }

        if not tb.evidence_raw_lines:
            task_res["status"] = "missing_hooks"
            task_res["why"] = "no evidence hooks found in task block"
            task_res["suggested_hooks"] = suggest_hooks(tb)
            totals["missing_hooks"] += 1
            results.append(task_res)
            continue

        matched_any = False
        any_invalid_scope = False
        any_needs_manual = False
        best_conf = "low"

        def _conf_rank(c: str) -> int:
            return {"low": 0, "medium": 1, "high": 2}.get(c, 0)

        for raw_ev in tb.evidence_raw_lines:
            ev_item: Dict[str, Any] = {
                "raw": raw_ev,
                "type": "",
                "pointer": "",
                "matched": False,
                "scope": "invalid",
                "why": "",
                "confidence": "low",
            }

            try:
                hook = parse_evidence_hook(raw_ev)
                ev_item["type"] = hook.type
            except Exception as e:
                ev_item["scope"] = "invalid"
                ev_item["why"] = str(e)
                task_res["evidence"].append(ev_item)
                continue

            # pointer
            if hook.type in {"code", "test", "docs"}:
                ev_item["pointer"] = hook.params.get("path", "")
            else:
                ev_item["pointer"] = hook.params.get("screen", "")

            if hook.type == "code":
                m = match_code_evidence(hook, project_root, safety, scan_budget)
            elif hook.type == "test":
                m = match_test_evidence(hook, project_root, safety, scan_budget)
            elif hook.type == "docs":
                m = match_docs_evidence(hook, project_root, safety, scan_budget)
            else:
                m = match_ui_evidence(hook, project_root, safety, scan_budget)

            ev_item.update({k: v for k, v in m.items() if k in {"matched", "scope", "why", "confidence", "excerpt"}})

            if ev_item.get("scope") == "invalid_scope":
                any_invalid_scope = True
            if ev_item.get("scope") == "needs_manual":
                any_needs_manual = True

            if ev_item.get("matched"):
                matched_any = True

            if _conf_rank(ev_item.get("confidence", "low")) > _conf_rank(best_conf):
                best_conf = ev_item.get("confidence", "low")

            task_res["evidence"].append(ev_item)

        task_res["confidence"] = best_conf

        if any_invalid_scope:
            task_res["status"] = "invalid_scope"
            task_res["why"] = "one or more evidence hooks point outside allowed scope"
            totals["invalid_scope"] += 1
            results.append(task_res)
            continue

        if best_conf == "high" and matched_any:
            task_res["verified"] = True
            task_res["status"] = "verified"
            task_res["why"] = "at least one evidence hook matched with high confidence"
            totals["verified"] += 1
            results.append(task_res)
            continue

        if allow_medium_verified and best_conf == "medium" and matched_any:
            task_res["verified"] = True
            task_res["status"] = "verified"
            task_res["why"] = "verified by medium confidence (config override)"
            totals["verified"] += 1
            results.append(task_res)
            continue

        if any_needs_manual and not matched_any:
            task_res["status"] = "needs_manual"
            task_res["why"] = "UI evidence could not be verified statically"
            totals["manual"] += 1
            results.append(task_res)
            continue

        task_res["status"] = "not_verified"
        task_res["why"] = "no evidence hook satisfied with high confidence"
        task_res["suggested_hooks"] = suggest_hooks(tb)
        totals["not_verified"] += 1
        results.append(task_res)

    run_id = _run_id(tasks_path)
    run_dir = out_root_abs / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    summary: Dict[str, Any] = {
        "workflow": "smartspec_verify_tasks_progress_strict",
        "version": "6.2.0",
        "run_id": run_id,
        "generated_at": datetime.now().isoformat(),
        "inputs": {"tasks_path": str(tasks_path), "spec_id": spec_id},
        "totals": totals,
        "results": results,
        "writes": {"reports": [str(run_dir / "report.md"), str(run_dir / "summary.json")]},
        "next_steps": [
            {
                "cmd": f"/smartspec_sync_tasks_checkboxes {tasks_path} --apply",
                "why": "Sync checkboxes after reviewing the verification report",
            }
        ],
    }

    if args.report_format in {"md", "both"}:
        write_report_md(run_dir, summary)

    if args.json or args.report_format in {"json", "both"}:
        (run_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    if not args.quiet:
        print(f"Wrote reports to: {run_dir}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
