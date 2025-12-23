#!/usr/bin/env python3
"""Strict evidence-only verifier for SmartSpec tasks.

Key goals:
- Reduce false negatives by using a single, quote-safe parser for evidence params.
- Reduce false positives by treating "path exists" as MEDIUM by default.
- Enforce handbook hardening: path normalization, no symlink escape, bounded scanning,
  safe output roots, and redaction.

Designed to be invoked by the SmartSpec workflow wrapper.
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime as _dt
import difflib
import hashlib
import json
import os
import re
import shlex
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


DEFAULT_CONFIG_PATH = ".spec/smartspec.config.yaml"
DEFAULT_REPORT_ROOT = ".spec/reports/verify-tasks-progress"

DEFAULT_LIMITS = {
    "max_files_to_scan": 4000,
    "max_total_bytes": 50 * 1024 * 1024,  # 50MB
    "max_verification_seconds": 20,
    "max_single_file_bytes": 2 * 1024 * 1024,  # 2MB
    "max_excerpt_chars": 240,
    "max_suggestions": 5,
}

DEFAULT_VERIFY_POLICY = {
    # By default, MEDIUM does NOT count as verified.
    "allow_medium_as_verified_for": [],  # e.g. ["docs"]
}


def _now_utc_iso() -> str:
    return _dt.datetime.utcnow().replace(tzinfo=_dt.timezone.utc).isoformat()


def _run_id() -> str:
    raw = f"{time.time_ns()}-{os.getpid()}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:12]


def _has_control_chars(s: str) -> bool:
    return any((ord(ch) < 32 and ch not in ("\t", "\n", "\r")) or ord(ch) == 127 for ch in s)


def _is_relative_safe_path(p: str) -> Tuple[bool, str]:
    if not p or _has_control_chars(p):
        return False, "invalid_path"
    if os.path.isabs(p) or re.match(r"^[a-zA-Z]:\\", p):
        return False, "absolute_path"
    parts = Path(p).parts
    if any(seg == ".." for seg in parts):
        return False, "path_traversal"
    return True, "ok"


def _is_binary_bytes(b: bytes) -> bool:
    return b"\x00" in b


def _try_load_yaml(path: Path) -> Dict[str, Any]:
    try:
        import yaml  # type: ignore

        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _deep_get(d: Dict[str, Any], dotted: str, default: Any) -> Any:
    cur: Any = d
    for key in dotted.split("."):
        if not isinstance(cur, dict) or key not in cur:
            return default
        cur = cur[key]
    return cur


def _as_list(x: Any) -> List[str]:
    if x is None:
        return []
    if isinstance(x, list):
        return [str(i) for i in x]
    return [str(x)]


def _compile_redactors(patterns: List[str]) -> List[re.Pattern[str]]:
    out: List[re.Pattern[str]] = []
    for p in patterns:
        try:
            out.append(re.compile(p))
        except re.error:
            continue
    return out


def _redact_text(text: str, redactors: List[re.Pattern[str]]) -> str:
    out = text
    for rx in redactors:
        out = rx.sub("[REDACTED]", out)
    return out


def _ensure_under_allowlist(path: Path, allow_roots: List[Path], deny_roots: List[Path]) -> Tuple[bool, str]:
    rp = path.resolve()

    for dr in deny_roots:
        drp = dr.resolve()
        if str(rp).startswith(str(drp) + os.sep) or rp == drp:
            return False, "denylist"

    if not allow_roots:
        return True, "ok"

    for ar in allow_roots:
        arp = ar.resolve()
        if str(rp).startswith(str(arp) + os.sep) or rp == arp:
            return True, "ok"

    return False, "not_under_allowlist"


@dataclasses.dataclass
class EvidenceResult:
    type: str
    raw: str
    matched: bool
    scope: str
    why: str
    pointer: str
    confidence: str
    excerpt: Optional[str] = None


@dataclasses.dataclass
class TaskResult:
    task_id: str
    title: str
    checked: bool
    status: str
    verified: bool
    confidence: str
    why: str
    evidence: List[EvidenceResult]
    suggested_hooks: List[str]


class StrictVerifier:
    def __init__(
        self,
        project_root: Path,
        tasks_path: Path,
        out_root: Path,
        report_format: str,
        want_json: bool,
        quiet: bool,
        config: Dict[str, Any],
    ) -> None:
        self.project_root = project_root.resolve()
        self.tasks_path = tasks_path
        self.out_root = out_root
        self.report_format = report_format
        self.want_json = want_json
        self.quiet = quiet

        self.limits = {
            **DEFAULT_LIMITS,
            **(_deep_get(config, "safety.content_limits", {}) or {}),
        }

        self.verify_policy = {
            **DEFAULT_VERIFY_POLICY,
            **(_deep_get(config, "verification.policy", {}) or {}),
        }

        self.allow_reads_only_under = [Path(p) for p in _as_list(_deep_get(config, "safety.allow_reads_only_under", []))]
        self.disallow_symlink_reads = bool(_deep_get(config, "safety.disallow_symlink_reads", True))

        redaction_patterns = _as_list(_deep_get(config, "safety.redaction", []))
        self.redactors = _compile_redactors(redaction_patterns)

        self._scan_files = 0
        self._scan_bytes = 0
        self._start_time = time.time()
        self.run_id = _run_id()

    def _budget_ok(self) -> Tuple[bool, str]:
        if self._scan_files > int(self.limits["max_files_to_scan"]):
            return False, "max_files"
        if self._scan_bytes > int(self.limits["max_total_bytes"]):
            return False, "max_bytes"
        if (time.time() - self._start_time) > float(self.limits["max_verification_seconds"]):
            return False, "timeout"
        return True, "ok"

    def _resolve_repo_path(self, rel: str) -> Tuple[Optional[Path], str]:
        ok, why = _is_relative_safe_path(rel)
        if not ok:
            return None, why

        candidate = self.project_root / rel
        try:
            resolved = candidate.resolve(strict=False)
        except Exception:
            return None, "resolve_failed"

        # must stay under project root
        if not (str(resolved).startswith(str(self.project_root) + os.sep) or resolved == self.project_root):
            return None, "invalid_scope"

        # optional read allowlist
        if self.allow_reads_only_under:
            allow_roots = [
                (self.project_root / p).resolve() if not os.path.isabs(str(p)) else p.resolve() for p in self.allow_reads_only_under
            ]
            ok2, why2 = _ensure_under_allowlist(resolved, allow_roots, [])
            if not ok2:
                return None, "invalid_scope"

        # symlink safety
        if self.disallow_symlink_reads:
            cur = self.project_root
            for part in Path(rel).parts:
                cur = cur / part
                try:
                    if cur.exists() and cur.is_symlink():
                        return None, "symlink_refused"
                except Exception:
                    return None, "symlink_check_failed"

        return resolved, "ok"

    def parse_evidence_line(self, line: str) -> Tuple[Optional[str], Dict[str, str], str]:
        raw = line.strip()
        m = re.search(r"\bevidence:\s*(.+)$", raw)
        if not m:
            return None, {}, "not_evidence"

        payload = m.group(1).strip()
        if not payload:
            return None, {}, "empty"

        try:
            tokens = shlex.split(payload)
        except ValueError:
            return None, {}, "malformed_quotes"

        if not tokens:
            return None, {}, "empty"

        ev_type = tokens[0].strip().lower()
        params: Dict[str, str] = {}
        for t in tokens[1:]:
            if "=" not in t:
                continue
            k, v = t.split("=", 1)
            params[k.strip().lower()] = v.strip()

        return ev_type, params, "ok"

    def _read_file_text(self, p: Path) -> Tuple[Optional[str], str]:
        try:
            st = p.stat()
            if st.st_size > int(self.limits["max_single_file_bytes"]):
                return None, "file_too_large"

            with p.open("rb") as f:
                b = f.read(int(self.limits["max_single_file_bytes"]) + 1)

            if _is_binary_bytes(b):
                return None, "binary_file"

            self._scan_bytes += len(b)
            ok, why = self._budget_ok()
            if not ok:
                return None, why

            return b.decode("utf-8", errors="ignore"), "ok"
        except FileNotFoundError:
            return None, "not_found"
        except PermissionError:
            return None, "permission"
        except Exception:
            return None, "read_error"

    def _search_in_path(self, p: Path, needle: str) -> Tuple[bool, str, Optional[str]]:
        if p.is_dir():
            for root, _, files in os.walk(p):
                ok, why = self._budget_ok()
                if not ok:
                    return False, why, None
                for fn in files:
                    ok, why = self._budget_ok()
                    if not ok:
                        return False, why, None
                    fp = Path(root) / fn
                    self._scan_files += 1
                    text, reason = self._read_file_text(fp)
                    if text is None:
                        continue
                    idx = text.find(needle)
                    if idx >= 0:
                        start = max(0, idx - int(self.limits["max_excerpt_chars"]) // 2)
                        end = min(len(text), start + int(self.limits["max_excerpt_chars"]))
                        excerpt = text[start:end]
                        return True, "ok", excerpt
            return False, "not_found", None

        text, reason = self._read_file_text(p)
        if text is None:
            return False, reason, None
        idx = text.find(needle)
        if idx >= 0:
            start = max(0, idx - int(self.limits["max_excerpt_chars"]) // 2)
            end = min(len(text), start + int(self.limits["max_excerpt_chars"]))
            excerpt = text[start:end]
            return True, "ok", excerpt
        return False, "not_found", None

    def _suggest_paths(self, missing_rel_path: str) -> List[str]:
        ok, _ = self._budget_ok()
        if not ok:
            return []

        basename = Path(missing_rel_path).name
        if not basename:
            return []

        candidates: List[str] = []
        max_sugs = int(self.limits["max_suggestions"])

        for root, _, files in os.walk(self.project_root):
            ok, _ = self._budget_ok()
            if not ok:
                break
            for fn in files:
                ok, _ = self._budget_ok()
                if not ok:
                    break
                self._scan_files += 1
                if fn == basename:
                    try:
                        rel = str(Path(root).joinpath(fn).resolve().relative_to(self.project_root))
                    except Exception:
                        continue
                    candidates.append(rel)
                    if len(candidates) >= max_sugs * 6:
                        break
            if len(candidates) >= max_sugs * 6:
                break

        ranked = sorted(
            candidates,
            key=lambda c: difflib.SequenceMatcher(a=missing_rel_path, b=c).ratio(),
            reverse=True,
        )

        out: List[str] = []
        for c in ranked:
            if c not in out:
                out.append(c)
            if len(out) >= max_sugs:
                break
        return out

    def _confidence_to_verified(self, conf: str, ev_type: str) -> bool:
        if conf == "high":
            return True
        if conf == "medium" and ev_type in set(self.verify_policy.get("allow_medium_as_verified_for", []) or []):
            return True
        return False

    def verify_evidence(self, ev_type: str, params: Dict[str, str], raw_line: str) -> Tuple[EvidenceResult, List[str]]:
        suggested_hooks: List[str] = []

        ev_type = (ev_type or "").strip().lower()
        if ev_type not in ("code", "test", "docs", "ui"):
            return (
                EvidenceResult(
                    type=ev_type or "unknown",
                    raw=raw_line,
                    matched=False,
                    scope="invalid",
                    why=f"Unsupported evidence type: {ev_type}",
                    pointer="",
                    confidence="low",
                ),
                [],
            )

        if ev_type in ("code", "test", "docs"):
            rel_path = params.get("path", "")
            if not rel_path:
                return (
                    EvidenceResult(
                        type=ev_type,
                        raw=raw_line,
                        matched=False,
                        scope="invalid",
                        why="Missing required param: path",
                        pointer="",
                        confidence="low",
                    ),
                    [],
                )

            resolved, scope = self._resolve_repo_path(rel_path)
            if resolved is None:
                for s in self._suggest_paths(rel_path):
                    sug = f"evidence: {ev_type} path={s}"
                    if "contains" in params:
                        sug += f" contains=\"{params['contains']}\""
                    if "symbol" in params:
                        sug += f" symbol={params['symbol']}"
                    if "heading" in params:
                        sug += f" heading=\"{params['heading']}\""
                    suggested_hooks.append(sug)

                return (
                    EvidenceResult(
                        type=ev_type,
                        raw=raw_line,
                        matched=False,
                        scope=scope,
                        why=f"Invalid/unsafe path scope: {rel_path}",
                        pointer=rel_path,
                        confidence="low",
                    ),
                    suggested_hooks,
                )

            if not resolved.exists():
                for s in self._suggest_paths(rel_path):
                    sug = f"evidence: {ev_type} path={s}"
                    if "contains" in params:
                        sug += f" contains=\"{params['contains']}\""
                    if "symbol" in params:
                        sug += f" symbol={params['symbol']}"
                    if "heading" in params:
                        sug += f" heading=\"{params['heading']}\""
                    suggested_hooks.append(sug)

                return (
                    EvidenceResult(
                        type=ev_type,
                        raw=raw_line,
                        matched=False,
                        scope="ok",
                        why=f"Path not found: {rel_path}",
                        pointer=str(resolved.relative_to(self.project_root)),
                        confidence="low",
                    ),
                    suggested_hooks,
                )

            contains = params.get("contains")
            symbol = params.get("symbol")
            heading = params.get("heading")

            search_token: Optional[str] = None
            if ev_type == "code":
                search_token = symbol or contains
            elif ev_type == "test":
                search_token = contains
            elif ev_type == "docs":
                search_token = heading or contains

            # path exists => MEDIUM at least
            if search_token:
                found, reason, excerpt = self._search_in_path(resolved, search_token)
                if found:
                    ex = _redact_text(excerpt or "", self.redactors) if excerpt else None
                    return (
                        EvidenceResult(
                            type=ev_type,
                            raw=raw_line,
                            matched=True,
                            scope="ok",
                            why=f"Matched content: {search_token}",
                            pointer=str(resolved.relative_to(self.project_root)),
                            confidence="high",
                            excerpt=ex,
                        ),
                        [],
                    )

                return (
                    EvidenceResult(
                        type=ev_type,
                        raw=raw_line,
                        matched=False,
                        scope=reason if reason != "ok" else "ok",
                        why=f"Path exists but content not found: {search_token}",
                        pointer=str(resolved.relative_to(self.project_root)),
                        confidence="medium",
                    ),
                    [],
                )

            return (
                EvidenceResult(
                    type=ev_type,
                    raw=raw_line,
                    matched=True,
                    scope="ok",
                    why="Path exists (no contains/symbol/heading provided)",
                    pointer=str(resolved.relative_to(self.project_root)),
                    confidence="medium",
                ),
                [],
            )

        # UI evidence
        screen = params.get("screen", "")
        route = params.get("route")
        component = params.get("component")
        states = params.get("states")

        if not screen:
            return (
                EvidenceResult(
                    type="ui",
                    raw=raw_line,
                    matched=False,
                    scope="invalid",
                    why="Missing required param: screen",
                    pointer="ui",
                    confidence="low",
                ),
                [],
            )

        def repo_search_literal(token: str) -> Tuple[bool, Optional[str]]:
            ok, _ = self._budget_ok()
            if not ok:
                return False, None
            for root, _, files in os.walk(self.project_root):
                ok, _ = self._budget_ok()
                if not ok:
                    return False, None
                for fn in files:
                    ok, _ = self._budget_ok()
                    if not ok:
                        return False, None
                    fp = Path(root) / fn
                    self._scan_files += 1
                    text, _ = self._read_file_text(fp)
                    if text is None:
                        continue
                    if token in text:
                        try:
                            rel = str(fp.resolve().relative_to(self.project_root))
                        except Exception:
                            rel = str(fp)
                        return True, rel
            return False, None

        static_hits: List[str] = []
        route_ptr = None
        comp_ptr = None

        route_ok = True
        if route:
            route_ok, route_ptr = repo_search_literal(route)
            if route_ok and route_ptr:
                static_hits.append(f"route:{route} in {route_ptr}")

        component_ok = False
        if component:
            component_ok, comp_ptr = repo_search_literal(component)
            if component_ok and comp_ptr:
                static_hits.append(f"component:{component} in {comp_ptr}")

        if component_ok and route_ok and states:
            pointer = comp_ptr or route_ptr or f"screen:{screen}"
            return (
                EvidenceResult(
                    type="ui",
                    raw=raw_line,
                    matched=True,
                    scope="ok",
                    why=f"Static UI signals found ({', '.join(static_hits)})",
                    pointer=pointer,
                    confidence="high",
                ),
                [],
            )

        pointer = comp_ptr or route_ptr or f"screen:{screen}"
        return (
            EvidenceResult(
                type="ui",
                raw=raw_line,
                matched=False,
                scope="needs_manual",
                why="UI evidence requires manual verification (insufficient static signals)",
                pointer=pointer,
                confidence="low",
            ),
            [],
        )

    def parse_tasks(self) -> Tuple[str, List[Dict[str, Any]]]:
        text, reason = self._read_file_text(self.tasks_path)
        if text is None:
            raise RuntimeError(f"Failed to read tasks: {reason}")

        lines = text.splitlines()

        spec_id = "unknown"
        for ln in lines[:40]:
            m = re.search(r"\b(spec[-_ ]?id)\s*[:=]\s*([a-z0-9_\-]{3,64})\b", ln, re.IGNORECASE)
            if m:
                spec_id = m.group(2)
                break
        if spec_id == "unknown":
            spec_id = self.tasks_path.parent.name

        tasks: List[Dict[str, Any]] = []
        current: Optional[Dict[str, Any]] = None

        # More permissive: any non-space token as ID
        task_re = re.compile(r"^\s*-\s*\[([ xX])\]\s+(\S+)\s+(.+?)\s*$")

        for i, ln in enumerate(lines, start=1):
            m = task_re.match(ln)
            if m:
                checked = (m.group(1).lower() == "x")
                task_id = m.group(2)
                title = m.group(3)
                current = {
                    "line": i,
                    "task_id": task_id,
                    "title": title,
                    "checked": checked,
                    "evidence_lines": [],
                }
                tasks.append(current)
                continue

            if current and re.search(r"\bevidence:\s*", ln):
                current["evidence_lines"].append(ln.strip())

        return spec_id, tasks

    def _render_report_md(self, summary: Dict[str, Any]) -> str:
        t = summary["totals"]
        lines: List[str] = []

        lines.append("# Verify Tasks Progress (Strict)\n\n")
        lines.append(f"- workflow: `{summary['workflow']}`\n")
        lines.append(f"- version: `{summary['version']}`\n")
        lines.append(f"- run_id: `{summary['run_id']}`\n")
        lines.append(f"- generated_at: `{summary['generated_at']}`\n")
        lines.append(f"- tasks: `{summary['inputs']['tasks_path']}`\n")
        lines.append(f"- spec_id: `{summary['inputs']['spec_id']}`\n")
        lines.append("\n---\n\n")

        lines.append("## Summary\n")
        lines.append(f"- total tasks: **{t['tasks']}**\n")
        lines.append(f"- verified done: **{t['verified']}**\n")
        lines.append(f"- not verified: **{t['not_verified']}**\n")
        lines.append(f"- needs manual check: **{t['manual']}**\n")
        lines.append(f"- missing evidence hooks: **{t['missing_hooks']}**\n")
        lines.append(f"- invalid evidence scope: **{t['invalid_scope']}**\n")
        lines.append("\n---\n\n")

        lines.append("## Per-task results\n")
        for r in summary["results"]:
            lines.append(f"### {r['task_id']} — {r['title']}\n")
            lines.append(f"- status: `{r['status']}`\n")
            lines.append(f"- confidence: `{r['confidence']}`\n")
            lines.append(f"- verified: `{r['verified']}`\n")
            if r.get("why"):
                lines.append(f"- why: {r['why']}\n")

            if r.get("evidence"):
                lines.append("\n**Evidence**\n")
                for e in r["evidence"]:
                    lines.append(
                        f"- `{e['type']}` `{e['confidence']}` matched={e['matched']} scope=`{e['scope']}`\n"
                        f"  - pointer: `{e.get('pointer','')}`\n"
                        f"  - why: {e.get('why','')}\n"
                    )
                    if e.get("excerpt"):
                        lines.append(f"  - excerpt: `{e['excerpt']}`\n")

            if r.get("suggested_hooks"):
                lines.append("\n**Suggested hooks**\n")
                for s in r["suggested_hooks"]:
                    lines.append(f"- {s}\n")

            lines.append("\n---\n")

        lines.append("\n## Remediation tips\n")
        lines.append("- If many tasks are `missing_hooks` or have placeholders, run: `/smartspec_migrate_evidence_hooks <tasks.md>`\n")
        lines.append("- Only update checkboxes via: `/smartspec_sync_tasks_checkboxes <tasks.md> --apply`\n")
        lines.append("\n---\n\n")

        lines.append("## Redaction note\n")
        lines.append("Report content may be redacted based on config safety.redaction patterns.\n")

        return "".join(lines)

    def run(self) -> Tuple[Dict[str, Any], str]:
        spec_id, parsed = self.parse_tasks()

        totals = {
            "tasks": 0,
            "verified": 0,
            "not_verified": 0,
            "manual": 0,
            "missing_hooks": 0,
            "invalid_scope": 0,
        }

        results: List[TaskResult] = []

        for t in parsed:
            totals["tasks"] += 1

            if not t["evidence_lines"]:
                totals["missing_hooks"] += 1
                results.append(
                    TaskResult(
                        task_id=t["task_id"],
                        title=t["title"],
                        checked=bool(t["checked"]),
                        status="missing_hooks",
                        verified=False,
                        confidence="low",
                        why="No evidence hooks found",
                        evidence=[],
                        suggested_hooks=[],
                    )
                )
                continue

            ev_results: List[EvidenceResult] = []
            suggested: List[str] = []

            for ln in t["evidence_lines"]:
                ev_type, params, parse_status = self.parse_evidence_line(ln)
                if parse_status != "ok" or ev_type is None:
                    ev_results.append(
                        EvidenceResult(
                            type="unknown",
                            raw=ln,
                            matched=False,
                            scope="invalid",
                            why=f"Evidence parse failed: {parse_status}",
                            pointer="",
                            confidence="low",
                        )
                    )
                    continue

                evr, sugs = self.verify_evidence(ev_type, params, ln)
                ev_results.append(evr)
                suggested.extend(sugs)

            conf = "low"
            if any(e.confidence == "high" for e in ev_results):
                conf = "high"
            elif any(e.confidence == "medium" for e in ev_results):
                conf = "medium"

            verified = any(self._confidence_to_verified(e.confidence, e.type) for e in ev_results)

            if any(e.scope == "invalid_scope" for e in ev_results):
                totals["invalid_scope"] += 1
                status = "invalid_scope"
            elif any(e.scope == "needs_manual" for e in ev_results):
                totals["manual"] += 1
                status = "needs_manual"
            elif verified:
                totals["verified"] += 1
                status = "verified"
            else:
                totals["not_verified"] += 1
                status = "not_verified"

            why = ""
            if status == "verified":
                why = "At least one evidence hook matched strongly (high confidence)"
            elif status == "needs_manual":
                why = "UI evidence requires manual confirmation"
            elif status == "invalid_scope":
                why = "One or more evidence hooks point outside allowed scope"
            else:
                strong = [e for e in ev_results if e.confidence in ("high", "medium")]
                why = "; ".join(f"{e.type}:{e.confidence}" for e in strong[:3]) if strong else "No evidence matched"

            red_evidence: List[EvidenceResult] = []
            for e in ev_results:
                red_evidence.append(
                    EvidenceResult(
                        type=e.type,
                        raw=_redact_text(e.raw, self.redactors),
                        matched=e.matched,
                        scope=e.scope,
                        why=_redact_text(e.why, self.redactors),
                        pointer=_redact_text(e.pointer, self.redactors),
                        confidence=e.confidence,
                        excerpt=_redact_text(e.excerpt, self.redactors) if e.excerpt else None,
                    )
                )

            results.append(
                TaskResult(
                    task_id=t["task_id"],
                    title=t["title"],
                    checked=bool(t["checked"]),
                    status=status,
                    verified=verified,
                    confidence=conf,
                    why=_redact_text(why, self.redactors),
                    evidence=red_evidence,
                    suggested_hooks=[_redact_text(s, self.redactors) for s in suggested[: int(self.limits["max_suggestions"]) ]],
                )
            )

        summary = {
            "workflow": "smartspec_verify_tasks_progress_strict",
            "version": "6.1.0",
            "run_id": self.run_id,
            "generated_at": _now_utc_iso(),
            "inputs": {
                "tasks_path": str(self.tasks_path),
                "spec_id": spec_id,
            },
            "totals": totals,
            "results": [
                {
                    "task_id": r.task_id,
                    "title": r.title,
                    "checked": r.checked,
                    "verified": r.verified,
                    "confidence": r.confidence,
                    "status": r.status,
                    "why": r.why,
                    "evidence": [dataclasses.asdict(e) for e in r.evidence],
                    "suggested_hooks": r.suggested_hooks,
                }
                for r in results
            ],
            "writes": {"reports": []},
            "next_steps": [
                {
                    "cmd": f"/smartspec_sync_tasks_checkboxes {self.tasks_path}",
                    "why": "Update checkboxes based on latest verification report (governed; requires --apply).",
                }
            ],
        }

        report_md = self._render_report_md(summary)
        return summary, report_md

    def write_outputs(self, summary: Dict[str, Any], report_md: str) -> List[Path]:
        run_dir = self.out_root / self.run_id
        run_dir.mkdir(parents=True, exist_ok=True)

        written: List[Path] = []

        report_path = run_dir / "report.md"
        report_path.write_text(report_md, encoding="utf-8")
        written.append(report_path)

        if self.want_json or self.report_format in ("json", "both"):
            summary_path = run_dir / "summary.json"
            summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
            written.append(summary_path)

        return written


def main(argv: List[str]) -> int:
    ap = argparse.ArgumentParser(description="SmartSpec strict evidence-only tasks verifier")

    ap.add_argument("tasks_md", help="Path to tasks.md")

    # Universal flags
    ap.add_argument("--config", default=DEFAULT_CONFIG_PATH)
    ap.add_argument("--lang", choices=["th", "en"], default="en")
    ap.add_argument("--platform", default="cli")
    ap.add_argument("--out", default=DEFAULT_REPORT_ROOT)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--quiet", action="store_true")

    # Workflow-specific
    ap.add_argument("--report-format", choices=["md", "json", "both"], default="both")

    # Internal
    ap.add_argument("--project-root", default=".")

    args = ap.parse_args(argv)

    tasks_path = Path(args.tasks_md)
    project_root = Path(args.project_root)

    config_path = Path(args.config)
    config = _try_load_yaml(config_path) if config_path.exists() else {}

    try:
        tasks_real = tasks_path.resolve(strict=True)
    except Exception:
        print("ERROR: tasks.md not found or unreadable", file=sys.stderr)
        return 1

    try:
        pr = project_root.resolve(strict=True)
    except Exception:
        print("ERROR: project root not found or unreadable", file=sys.stderr)
        return 2

    if not (str(tasks_real).startswith(str(pr) + os.sep) or tasks_real == pr):
        print("ERROR: tasks.md must be within project-root", file=sys.stderr)
        return 1

    rel_to_root = Path(".")
    try:
        rel_to_root = tasks_real.relative_to(pr)
    except Exception:
        pass

    if "specs" not in rel_to_root.parts:
        print("ERROR: tasks.md must resolve under specs/**", file=sys.stderr)
        return 1

    out_root = Path(args.out)
    out_root_abs = (pr / out_root).resolve() if not os.path.isabs(str(out_root)) else out_root.resolve()

    allow_writes = [Path(p) for p in _as_list(_deep_get(config, "safety.allow_writes_only_under", []))]
    deny_writes = [Path(p) for p in _as_list(_deep_get(config, "safety.deny_writes_under", []))]

    allow_roots_abs = [(pr / p).resolve() if not os.path.isabs(str(p)) else p.resolve() for p in allow_writes]
    deny_roots_abs = [(pr / p).resolve() if not os.path.isabs(str(p)) else p.resolve() for p in deny_writes]

    ok_out, why_out = _ensure_under_allowlist(out_root_abs, allow_roots_abs, deny_roots_abs)
    if not ok_out:
        print(f"ERROR: unsafe --out (reason={why_out}): {out_root_abs}", file=sys.stderr)
        return 1

    verifier = StrictVerifier(
        project_root=pr,
        tasks_path=tasks_real,
        out_root=out_root_abs,
        report_format=args.report_format,
        want_json=bool(args.json),
        quiet=bool(args.quiet),
        config=config,
    )

    try:
        summary, report_md = verifier.run()
        written = verifier.write_outputs(summary, report_md)
        summary["writes"]["reports"] = [str(p) for p in written]

        if not args.quiet:
            print(f"Wrote report: {written[0]}")
            if len(written) > 1:
                print(f"Wrote summary: {written[1]}")

        return 0

    except Exception as e:
        if not args.quiet:
            print(f"ERROR: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
