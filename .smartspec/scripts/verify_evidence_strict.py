#!/usr/bin/env python3
"""verify_evidence_strict.py (v5.3.2)

Read-only strict evidence verifier for SmartSpec tasks.

Purpose
- Read tasks.md
- For each task, evaluate its `evidence:` lines against the repo tree
- Produce a verification summary and per-task details

Safety / governance
- Read-only. Never modifies repo files.
- Never runs commands in evidence. `command=` is informational only.

Evidence schema (canonical)
  evidence: <type> key=value key="value with spaces" ...

Types and keys
- code: path, symbol, contains, regex
- test: path, contains, regex, command
- docs: path, heading, contains, regex
- ui:   path, selector, contains, regex

Verifier policy
- A task is VERIFIED if ANY evidence line matches.
- Accepts both `evidence:` and `- evidence:` lines.
- Directory shorthand:
  - If `code path=<dir>/` OR the path points to an existing directory:
    treat as directory evidence.
  - If `contains`/`regex` present, run a bounded scan.

Limitations
- evidence-only: does not understand code semantics beyond textual matching.
- directory scan is bounded to avoid repo-wide expensive scans.
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import re
import shlex
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

EVIDENCE_TYPES = {"code", "test", "docs", "ui"}
NON_COMPLIANT_TYPES = {"file_exists", "test_exists", "command"}

ALLOWED_KEYS = {
    "code": {"path", "symbol", "contains", "regex"},
    "test": {"path", "contains", "regex", "command"},
    "docs": {"path", "heading", "contains", "regex"},
    "ui": {"path", "selector", "contains", "regex"},
}

RE_TASK_LINE = re.compile(
    r"^\s*-\s*\[(?P<chk>[ xX])\]\s+(?P<id>[A-Za-z0-9][A-Za-z0-9._:-]*)(\s+|\s*$)(?P<title>.*)$"
)
RE_EVIDENCE_LINE = re.compile(r"^\s*(?:-\s*)?evidence:\s+(?P<payload>.+?)\s*$", re.IGNORECASE)

GLOB_CHARS = set("*?[]")


@dataclasses.dataclass
class Evidence:
    etype: str
    kv: Dict[str, str]
    raw: str
    line_no: int


@dataclasses.dataclass
class EvidenceResult:
    ok: bool
    reason: str
    evidence: Evidence


@dataclasses.dataclass
class TaskResult:
    task_id: str
    title: str
    line_no: int
    evidence_results: List[EvidenceResult]

    @property
    def ok(self) -> bool:
        return any(er.ok for er in self.evidence_results) if self.evidence_results else False


def _strip_quotes(v: str) -> str:
    v = v.strip()
    if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
        return v[1:-1]
    return v


def _safe_rel_path(p: str) -> str:
    p = _strip_quotes(p).replace("\\", "/").lstrip("./")
    return p


def _contains_glob(p: str) -> bool:
    return any(ch in p for ch in GLOB_CHARS)


def _shlex(payload: str) -> Tuple[List[str], Optional[str]]:
    try:
        return shlex.split(payload), None
    except ValueError as e:
        return [], str(e)


def parse_evidence(payload: str, line_no: int) -> Tuple[Optional[Evidence], Optional[str]]:
    tokens, err = _shlex(payload)
    if err:
        return None, f"L{line_no}: tokenization error: {err}"
    if not tokens:
        return None, f"L{line_no}: empty evidence payload"

    etype = tokens[0].strip().lower()
    if etype not in EVIDENCE_TYPES:
        return None, f"L{line_no}: invalid evidence type '{etype}'"

    kv: Dict[str, str] = {}
    stray: List[str] = []
    for t in tokens[1:]:
        if "=" in t:
            k, v = t.split("=", 1)
            kv[k.strip()] = _strip_quotes(v)
        else:
            stray.append(t)

    if stray:
        return None, f"L{line_no}: stray tokens not allowed: {stray}"

    unknown = [k for k in kv.keys() if k not in ALLOWED_KEYS[etype]]
    if unknown:
        return None, f"L{line_no}: unknown keys for {etype}: {unknown}"

    if "path" not in kv:
        return None, f"L{line_no}: missing required key path="

    kv["path"] = _safe_rel_path(kv["path"])

    if kv["path"].startswith("/") or ".." in kv["path"].split("/"):
        return None, f"L{line_no}: invalid path (absolute/traversal): {kv['path']}"

    if _contains_glob(kv["path"]):
        return None, f"L{line_no}: glob path not supported in strict mode: {kv['path']}"

    return Evidence(etype=etype, kv=kv, raw=payload, line_no=line_no), None


def _read_text(path: Path, max_bytes: int = 2_000_000) -> str:
    try:
        data = path.read_bytes()
    except Exception:
        return ""
    if len(data) > max_bytes:
        data = data[:max_bytes]
    try:
        return data.decode("utf-8", errors="ignore")
    except Exception:
        return ""


def _match_contains(text: str, needle: str) -> bool:
    return needle in text


def _match_regex(text: str, pattern: str) -> bool:
    try:
        return re.search(pattern, text, flags=re.MULTILINE) is not None
    except re.error:
        return False


def _bounded_walk(root: Path, max_files: int = 2500) -> Iterable[Path]:
    count = 0
    for p in root.rglob("*"):
        if p.is_file():
            yield p
            count += 1
            if count >= max_files:
                return


def _verify_file_match(path: Path, contains: Optional[str], regex: Optional[str], symbol: Optional[str]) -> Tuple[bool, str]:
    if not path.exists() or not path.is_file():
        return False, "file not found"

    txt = _read_text(path)

    if contains is not None and not _match_contains(txt, contains):
        return False, "contains not found"

    if regex is not None and not _match_regex(txt, regex):
        return False, "regex not matched"

    if symbol is not None and symbol and symbol != "Directory":
        if symbol not in txt:
            return False, "symbol not found"

    return True, "matched"


def _verify_directory(root: Path, contains: Optional[str], regex: Optional[str], repo_root: Path) -> Tuple[bool, str]:
    if not root.exists() or not root.is_dir():
        return False, "directory not found"

    if not (contains or regex):
        return True, "directory exists"

    for f in _bounded_walk(root):
        txt = _read_text(f)
        if contains and _match_contains(txt, contains):
            return True, f"found contains in {f.relative_to(repo_root)}"
        if regex and _match_regex(txt, regex):
            return True, f"found regex in {f.relative_to(repo_root)}"

    return False, "no match found in directory scan"


def verify_code(repo_root: Path, ev: Evidence) -> EvidenceResult:
    raw_path = ev.kv["path"]
    path = repo_root / raw_path

    symbol = ev.kv.get("symbol")
    contains = ev.kv.get("contains")
    regex = ev.kv.get("regex")

    # Directory shorthand
    if raw_path.endswith("/"):
        path = repo_root / raw_path.rstrip("/")
        ok, why = _verify_directory(path, contains=contains, regex=regex, repo_root=repo_root)
        return EvidenceResult(ok, why, ev)

    if symbol == "Directory" or (path.exists() and path.is_dir()):
        ok, why = _verify_directory(path, contains=contains, regex=regex, repo_root=repo_root)
        return EvidenceResult(ok, why, ev)

    ok, why = _verify_file_match(path, contains=contains, regex=regex, symbol=symbol)
    return EvidenceResult(ok, why, ev)


def verify_docs(repo_root: Path, ev: Evidence) -> EvidenceResult:
    path = repo_root / ev.kv["path"]
    if not path.exists() or not path.is_file():
        return EvidenceResult(False, f"file not found: {ev.kv['path']}", ev)

    txt = _read_text(path)

    if "heading" in ev.kv:
        h = ev.kv["heading"].strip()
        if re.search(r"^#+\s+" + re.escape(h) + r"\s*$", txt, flags=re.MULTILINE) is None:
            return EvidenceResult(False, "heading not found", ev)

    if "contains" in ev.kv and not _match_contains(txt, ev.kv["contains"]):
        return EvidenceResult(False, "contains not found", ev)

    if "regex" in ev.kv and not _match_regex(txt, ev.kv["regex"]):
        return EvidenceResult(False, "regex not matched", ev)

    return EvidenceResult(True, "matched", ev)


def verify_test(repo_root: Path, ev: Evidence) -> EvidenceResult:
    path = repo_root / ev.kv["path"]
    if not path.exists():
        return EvidenceResult(False, f"anchor not found: {ev.kv['path']}", ev)

    if path.is_file():
        txt = _read_text(path)
        if "contains" in ev.kv and not _match_contains(txt, ev.kv["contains"]):
            return EvidenceResult(False, "contains not found", ev)
        if "regex" in ev.kv and not _match_regex(txt, ev.kv["regex"]):
            return EvidenceResult(False, "regex not matched", ev)

    return EvidenceResult(True, "matched", ev)


def verify_ui(repo_root: Path, ev: Evidence) -> EvidenceResult:
    path = repo_root / ev.kv["path"]
    if not path.exists() or not path.is_file():
        return EvidenceResult(False, f"file not found: {ev.kv['path']}", ev)

    txt = _read_text(path)

    if "selector" in ev.kv and ev.kv["selector"] not in txt:
        return EvidenceResult(False, "selector not found", ev)
    if "contains" in ev.kv and not _match_contains(txt, ev.kv["contains"]):
        return EvidenceResult(False, "contains not found", ev)
    if "regex" in ev.kv and not _match_regex(txt, ev.kv["regex"]):
        return EvidenceResult(False, "regex not matched", ev)

    return EvidenceResult(True, "matched", ev)


def verify_one(repo_root: Path, ev: Evidence) -> EvidenceResult:
    if ev.etype == "code":
        return verify_code(repo_root, ev)
    if ev.etype == "docs":
        return verify_docs(repo_root, ev)
    if ev.etype == "test":
        return verify_test(repo_root, ev)
    if ev.etype == "ui":
        return verify_ui(repo_root, ev)
    return EvidenceResult(False, "unknown evidence type", ev)


def verify_tasks(repo_root: Path, tasks_path: Path) -> List[TaskResult]:
    logger.info(f"Starting verification: {tasks_path}")
    text = tasks_path.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()

    results: List[TaskResult] = []

    current_id = ""
    current_title = ""
    current_line = 0
    current_evs: List[Evidence] = []

    def flush() -> None:
        nonlocal current_id, current_title, current_line, current_evs
        if not current_id:
            return
        ev_results: List[EvidenceResult] = []
        for ev in current_evs:
            ev_results.append(verify_one(repo_root, ev))
        results.append(TaskResult(current_id, current_title, current_line, ev_results))
        current_id, current_title, current_line, current_evs = "", "", 0, []

    for i, line in enumerate(lines, 1):
        m = RE_TASK_LINE.match(line)
        if m:
            flush()
            current_id = m.group("id")
            current_title = (m.group("title") or "").strip()
            current_line = i
            continue

        m2 = RE_EVIDENCE_LINE.match(line)
        if m2 and current_id:
            payload = m2.group("payload").strip()
            ev, _err = parse_evidence(payload, i)
            if ev:
                current_evs.append(ev)
            else:
                current_evs.append(Evidence("code", {"path": ""}, raw=payload, line_no=i))

    flush()
    return results


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("tasks", help="Path to tasks.md")
    ap.add_argument("--repo-root", default=".", help="Repo root")
    ap.add_argument("--json", action="store_true", help="Emit JSON report")
    ap.add_argument("--out", default=".smartspec/reports/verify-tasks-progress", help="Output directory")
    args = ap.parse_args()

    repo_root = Path(args.repo_root).resolve()
    tasks_path = Path(args.tasks).resolve()

    results = verify_tasks(repo_root, tasks_path)

    summary = {
        "tasks_total": len(results),
        "tasks_ok": sum(1 for r in results if r.ok),
        "tasks_fail": sum(1 for r in results if not r.ok),
    }

    # Generate reports
    from datetime import datetime
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = Path(args.out) / run_id
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # Write summary.json
    summary_data = {
        "run_id": run_id,
        "timestamp": datetime.now().isoformat(),
        "tasks_file": str(tasks_path),
        "verified": summary["tasks_ok"],
        "total": summary["tasks_total"],
        "not_verified": summary["tasks_fail"],
        "tasks": [{"id": r.task_id, "ok": r.ok, "why": r.evidence_results[0].reason if r.evidence_results else ""} for r in results]
    }
    with open(out_dir / "summary.json", "w") as f:
        json.dump(summary_data, f, indent=2)
    
    # Write report.md
    with open(out_dir / "report.md", "w") as f:
        f.write(f"# Task Verification Report\n\n")
        f.write(f"**Generated:** {datetime.now().isoformat()}\n")
        f.write(f"**Run ID:** {run_id}\n")
        f.write(f"**Tasks File:** {tasks_path}\n\n")
        f.write(f"## Summary\n\n")
        f.write(f"- **Total Tasks:** {summary['tasks_total']}\n")
        f.write(f"- **Verified:** {summary['tasks_ok']}\n")
        f.write(f"- **Not Verified:** {summary['tasks_fail']}\n\n")
        f.write(f"## Task Details\n\n")
        for r in results:
            status = "✅" if r.ok else "❌"
            f.write(f"### {status} {r.task_id}\n")
            if not r.ok:
                f.write(f"**Evidence Issues:**\n")
                for er in r.evidence_results:
                    if not er.ok:
                        f.write(f"- Line {er.evidence.line_no}: {er.reason}\n")
            f.write(f"\n")
    
    logger.info(f"Reports written to: {out_dir}")
    logger.info(f"  - {out_dir / 'report.md'}")
    logger.info(f"  - {out_dir / 'summary.json'}")

    if args.json:
        print(
            json.dumps(
                {"summary": summary, "tasks": [dataclasses.asdict(r) for r in results]},
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print(f"tasks_total={summary['tasks_total']} ok={summary['tasks_ok']} fail={summary['tasks_fail']}")
        for r in results:
            if r.ok:
                continue
            print(f"FAIL {r.task_id} (L{r.line_no}) {r.title}")
            for er in r.evidence_results:
                print(f"  - {('OK' if er.ok else 'NO')} L{er.evidence.line_no}: {er.evidence.raw} :: {er.reason}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
