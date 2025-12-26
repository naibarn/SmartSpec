#!/usr/bin/env python3
"""verify_evidence_enhanced.py (v6.0.0)

Enhanced evidence verifier for SmartSpec tasks with detailed root cause analysis.

New Features (v6.0.0):
- Separate tracking of code vs test evidence
- Checkbox status tracking  
- Fuzzy file matching for similar filenames
- Problem categorization (not_implemented, missing_tests, naming_issue, etc.)
- Root cause analysis
- Actionable suggestions per task
- Enhanced summary statistics
- Grouped report format by problem category

Purpose:
- Read tasks.md
- For each task, evaluate its `evidence:` lines against the repo tree
- Categorize problems and provide detailed analysis
- Generate actionable recommendations

Safety / governance:
- Read-only. Never modifies repo files.
- Never runs commands in evidence. `command=` is informational only.
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import re
import shlex
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple
from enum import Enum
from difflib import SequenceMatcher
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

EVIDENCE_TYPES = {"code", "test", "docs", "ui"}

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


class ProblemCategory(Enum):
    """Categories of problems found in task verification"""
    NOT_IMPLEMENTED = "not_implemented"
    MISSING_TESTS = "missing_tests"
    MISSING_CODE = "missing_code"
    NAMING_ISSUE = "naming_issue"
    SYMBOL_ISSUE = "symbol_issue"
    CONTENT_ISSUE = "content_issue"
    VERIFIED = "verified"


@dataclasses.dataclass
class FileInfo:
    """Information about a file check"""
    exists: bool
    size: Optional[int] = None
    path: Optional[Path] = None
    similar_files: List[Path] = dataclasses.field(default_factory=list)


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
    file_info: Optional[FileInfo] = None


@dataclasses.dataclass
class TaskResult:
    task_id: str
    title: str
    line_no: int
    checked: bool
    code_evidence: List[EvidenceResult] = dataclasses.field(default_factory=list)
    test_evidence: List[EvidenceResult] = dataclasses.field(default_factory=list)
    docs_evidence: List[EvidenceResult] = dataclasses.field(default_factory=list)
    ui_evidence: List[EvidenceResult] = dataclasses.field(default_factory=list)

    @property
    def all_evidence(self) -> List[EvidenceResult]:
        return self.code_evidence + self.test_evidence + self.docs_evidence + self.ui_evidence

    @property
    def ok(self) -> bool:
        all_ev = self.all_evidence
        if not all_ev:
            return False
        return all(er.ok for er in all_ev)

    @property
    def category(self) -> ProblemCategory:
        if self.ok:
            return ProblemCategory.VERIFIED

        has_code = len(self.code_evidence) > 0
        has_test = len(self.test_evidence) > 0
        
        code_files_exist = any(er.file_info and er.file_info.exists for er in self.code_evidence) if has_code else False
        test_files_exist = any(er.file_info and er.file_info.exists for er in self.test_evidence) if has_test else False

        code_has_similar = any(er.file_info and er.file_info.similar_files for er in self.code_evidence) if has_code else False
        test_has_similar = any(er.file_info and er.file_info.similar_files for er in self.test_evidence) if has_test else False

        if not code_files_exist and not test_files_exist:
            if code_has_similar or test_has_similar:
                return ProblemCategory.NAMING_ISSUE
            return ProblemCategory.NOT_IMPLEMENTED
        
        if code_files_exist and not test_files_exist:
            if test_has_similar:
                return ProblemCategory.NAMING_ISSUE
            return ProblemCategory.MISSING_TESTS
        
        if test_files_exist and not code_files_exist:
            if code_has_similar:
                return ProblemCategory.NAMING_ISSUE
            return ProblemCategory.MISSING_CODE
        
        if code_files_exist or test_files_exist:
            if any("symbol not found" in er.reason for er in self.all_evidence):
                return ProblemCategory.SYMBOL_ISSUE
            if any("contains not found" in er.reason or "regex not matched" in er.reason for er in self.all_evidence):
                return ProblemCategory.CONTENT_ISSUE
            if code_has_similar or test_has_similar:
                return ProblemCategory.NAMING_ISSUE

        return ProblemCategory.NOT_IMPLEMENTED


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


def find_similar_files(repo_root: Path, target_path: str, threshold: float = 0.6) -> List[Path]:
    """Find files with similar names using fuzzy matching"""
    target_file = Path(target_path).name
    target_dir = Path(target_path).parent
    
    search_dir = repo_root / target_dir
    if not search_dir.exists():
        search_dir = repo_root / target_dir.parent
    
    if not search_dir.exists():
        return []
    
    similar = []
    for file in search_dir.rglob("*"):
        if file.is_file():
            similarity = SequenceMatcher(None, target_file, file.name).ratio()
            if similarity >= threshold and file.name != target_file:
                similar.append(file)
    
    similar.sort(key=lambda f: SequenceMatcher(None, target_file, f.name).ratio(), reverse=True)
    return similar[:5]


def get_file_info(repo_root: Path, path_str: str) -> FileInfo:
    """Get detailed information about a file"""
    path = repo_root / path_str
    
    if path.exists():
        if path.is_file():
            size = path.stat().st_size
            return FileInfo(exists=True, size=size, path=path, similar_files=[])
        elif path.is_dir():
            return FileInfo(exists=True, size=None, path=path, similar_files=[])
    
    similar = find_similar_files(repo_root, path_str)
    return FileInfo(exists=False, size=None, path=None, similar_files=similar)


def _verify_file_match(path: Path, contains: Optional[str], regex: Optional[str], symbol: Optional[str], file_info: FileInfo) -> Tuple[bool, str]:
    if not file_info.exists or not path.is_file():
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

    file_info = get_file_info(repo_root, raw_path)

    if raw_path.endswith("/"):
        path = repo_root / raw_path.rstrip("/")
        ok, why = _verify_directory(path, contains=contains, regex=regex, repo_root=repo_root)
        return EvidenceResult(ok, why, ev, file_info)

    if symbol == "Directory" or (path.exists() and path.is_dir()):
        ok, why = _verify_directory(path, contains=contains, regex=regex, repo_root=repo_root)
        return EvidenceResult(ok, why, ev, file_info)

    ok, why = _verify_file_match(path, contains=contains, regex=regex, symbol=symbol, file_info=file_info)
    return EvidenceResult(ok, why, ev, file_info)


def verify_docs(repo_root: Path, ev: Evidence) -> EvidenceResult:
    raw_path = ev.kv["path"]
    path = repo_root / raw_path
    file_info = get_file_info(repo_root, raw_path)

    if not file_info.exists or not path.is_file():
        return EvidenceResult(False, f"file not found: {ev.kv['path']}", ev, file_info)

    txt = _read_text(path)

    if "heading" in ev.kv:
        h = ev.kv["heading"].strip()
        if re.search(r"^#+\s+" + re.escape(h) + r"\s*$", txt, flags=re.MULTILINE) is None:
            return EvidenceResult(False, "heading not found", ev, file_info)

    if "contains" in ev.kv and not _match_contains(txt, ev.kv["contains"]):
        return EvidenceResult(False, "contains not found", ev, file_info)

    if "regex" in ev.kv and not _match_regex(txt, ev.kv["regex"]):
        return EvidenceResult(False, "regex not matched", ev, file_info)

    return EvidenceResult(True, "matched", ev, file_info)


def verify_test(repo_root: Path, ev: Evidence) -> EvidenceResult:
    raw_path = ev.kv["path"]
    path = repo_root / raw_path
    file_info = get_file_info(repo_root, raw_path)

    if not file_info.exists:
        return EvidenceResult(False, f"anchor not found: {ev.kv['path']}", ev, file_info)

    if path.is_file():
        txt = _read_text(path)
        if "contains" in ev.kv and not _match_contains(txt, ev.kv["contains"]):
            return EvidenceResult(False, "contains not found", ev, file_info)
        if "regex" in ev.kv and not _match_regex(txt, ev.kv["regex"]):
            return EvidenceResult(False, "regex not matched", ev, file_info)

    return EvidenceResult(True, "matched", ev, file_info)


def verify_ui(repo_root: Path, ev: Evidence) -> EvidenceResult:
    raw_path = ev.kv["path"]
    path = repo_root / raw_path
    file_info = get_file_info(repo_root, raw_path)

    if not file_info.exists or not path.is_file():
        return EvidenceResult(False, f"file not found: {ev.kv['path']}", ev, file_info)

    txt = _read_text(path)

    if "selector" in ev.kv and ev.kv["selector"] not in txt:
        return EvidenceResult(False, "selector not found", ev, file_info)
    if "contains" in ev.kv and not _match_contains(txt, ev.kv["contains"]):
        return EvidenceResult(False, "contains not found", ev, file_info)
    if "regex" in ev.kv and not _match_regex(txt, ev.kv["regex"]):
        return EvidenceResult(False, "regex not matched", ev, file_info)

    return EvidenceResult(True, "matched", ev, file_info)


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
    current_checked = False
    current_code_evs: List[Evidence] = []
    current_test_evs: List[Evidence] = []
    current_docs_evs: List[Evidence] = []
    current_ui_evs: List[Evidence] = []

    def flush() -> None:
        nonlocal current_id, current_title, current_line, current_checked
        nonlocal current_code_evs, current_test_evs, current_docs_evs, current_ui_evs
        
        if not current_id:
            return
        
        code_results = [verify_one(repo_root, ev) for ev in current_code_evs]
        test_results = [verify_one(repo_root, ev) for ev in current_test_evs]
        docs_results = [verify_one(repo_root, ev) for ev in current_docs_evs]
        ui_results = [verify_one(repo_root, ev) for ev in current_ui_evs]
        
        results.append(TaskResult(
            task_id=current_id,
            title=current_title,
            line_no=current_line,
            checked=current_checked,
            code_evidence=code_results,
            test_evidence=test_results,
            docs_evidence=docs_results,
            ui_evidence=ui_results
        ))
        
        current_id, current_title, current_line, current_checked = "", "", 0, False
        current_code_evs, current_test_evs, current_docs_evs, current_ui_evs = [], [], [], []

    for i, line in enumerate(lines, 1):
        m = RE_TASK_LINE.match(line)
        if m:
            flush()
            current_id = m.group("id")
            current_title = (m.group("title") or "").strip()
            current_line = i
            current_checked = m.group("chk").lower() == "x"
            continue

        m2 = RE_EVIDENCE_LINE.match(line)
        if m2 and current_id:
            payload = m2.group("payload").strip()
            ev, _err = parse_evidence(payload, i)
            if ev:
                if ev.etype == "code":
                    current_code_evs.append(ev)
                elif ev.etype == "test":
                    current_test_evs.append(ev)
                elif ev.etype == "docs":
                    current_docs_evs.append(ev)
                elif ev.etype == "ui":
                    current_ui_evs.append(ev)

    flush()
    return results


def generate_suggestions(task: TaskResult) -> List[str]:
    """Generate actionable suggestions for a task"""
    suggestions = []
    category = task.category

    if category == ProblemCategory.NOT_IMPLEMENTED:
        suggestions.append(f"⚠️ Task is marked [{('x' if task.checked else ' ')}] but no implementation or test files exist")
        if task.checked:
            suggestions.append("→ Update checkbox to [ ] until implementation is complete")
        
        for er in task.code_evidence:
            if not er.ok:
                suggestions.append(f"→ Create implementation file: {er.evidence.kv['path']}")
        
        for er in task.test_evidence:
            if not er.ok:
                suggestions.append(f"→ Create test file: {er.evidence.kv['path']}")

    elif category == ProblemCategory.MISSING_TESTS:
        suggestions.append("✓ Implementation exists but test files are missing")
        for er in task.test_evidence:
            if not er.ok:
                if er.file_info and er.file_info.similar_files:
                    similar = er.file_info.similar_files[0]
                    try:
                        rel_path = similar.relative_to(similar.parents[len(list(similar.parents))-1])
                        suggestions.append(f"→ Found similar test file: {rel_path}")
                    except:
                        suggestions.append(f"→ Found similar test file: {similar.name}")
                    suggestions.append(f"→ Update evidence to use: {similar.name}")
                else:
                    suggestions.append(f"→ Create test file: {er.evidence.kv['path']}")

    elif category == ProblemCategory.NAMING_ISSUE:
        suggestions.append("⚠️ Files exist but names don't match evidence")
        for er in task.all_evidence:
            if not er.ok and er.file_info and er.file_info.similar_files:
                similar = er.file_info.similar_files[0]
                suggestions.append(f"→ Found similar file: {similar.name}")
                suggestions.append(f"→ Update evidence path to: {similar}")
                suggestions.append(f"   OR rename file to match evidence: {er.evidence.kv['path']}")

    elif category == ProblemCategory.SYMBOL_ISSUE:
        suggestions.append("⚠️ File exists but symbol not found")
        for er in task.code_evidence:
            if "symbol not found" in er.reason:
                symbol = er.evidence.kv.get("symbol", "")
                suggestions.append(f"→ Symbol '{symbol}' not found in {er.evidence.kv['path']}")
                if er.file_info and er.file_info.exists:
                    suggestions.append(f"   File exists ({er.file_info.size} bytes)")
                suggestions.append(f"→ Check if symbol is exported or has a different name")

    elif category == ProblemCategory.CONTENT_ISSUE:
        suggestions.append("⚠️ File exists but content doesn't match")
        for er in task.all_evidence:
            if "contains not found" in er.reason:
                contains = er.evidence.kv.get("contains", "")
                suggestions.append(f"→ String '{contains}' not found in {er.evidence.kv['path']}")
            elif "regex not matched" in er.reason:
                regex = er.evidence.kv.get("regex", "")
                suggestions.append(f"→ Regex pattern '{regex}' not matched in {er.evidence.kv['path']}")

    return suggestions


def write_enhanced_report(results: List[TaskResult], tasks_path: Path, out_dir: Path, run_id: str):
    """Write enhanced report with detailed analysis"""
    from datetime import datetime
    from collections import defaultdict

    by_category = defaultdict(list)
    for r in results:
        by_category[r.category].append(r)

    total = len(results)
    verified = len(by_category[ProblemCategory.VERIFIED])
    not_verified = total - verified
    marked_done_but_failed = sum(1 for r in results if r.checked and not r.ok)

    missing_files = defaultdict(int)
    for r in results:
        if not r.ok:
            for er in r.all_evidence:
                if not er.ok and not (er.file_info and er.file_info.exists):
                    missing_files[er.evidence.kv['path']] += 1

    most_common_missing = sorted(missing_files.items(), key=lambda x: x[1], reverse=True)[:10]

    with open(out_dir / "report.md", "w") as f:
        f.write(f"# Enhanced Task Verification Report\n\n")
        f.write(f"**Generated:** {datetime.now().isoformat()}\n")
        f.write(f"**Run ID:** {run_id}\n")
        f.write(f"**Tasks File:** {tasks_path}\n")
        f.write(f"**Script Version:** v6.0.0 (Enhanced)\n\n")
        
        f.write(f"## Executive Summary\n\n")
        f.write(f"- **Total Tasks:** {total}\n")
        f.write(f"- **Verified:** {verified} ({verified*100//total if total > 0 else 0}%)\n")
        f.write(f"- **Not Verified:** {not_verified} ({not_verified*100//total if total > 0 else 0}%)\n")
        f.write(f"- **Critical Issues:** {marked_done_but_failed} tasks marked [x] but not verified\n\n")
        
        f.write(f"### Breakdown by Problem Category\n\n")
        for cat in ProblemCategory:
            count = len(by_category[cat])
            if count > 0:
                pct = count * 100 // total if total > 0 else 0
                f.write(f"- **{cat.value.replace('_', ' ').title()}:** {count} tasks ({pct}%)\n")
        
        if most_common_missing:
            f.write(f"\n### Most Common Missing Files\n\n")
            for file, count in most_common_missing:
                f.write(f"- `{file}` — affects {count} task(s)\n")
        
        f.write(f"\n---\n\n")
        
        category_order = [
            (ProblemCategory.NOT_IMPLEMENTED, "❌ Not Implemented", "Tasks with no implementation or test files"),
            (ProblemCategory.MISSING_TESTS, "⚠️ Missing Tests", "Tasks with implementation but no test files"),
            (ProblemCategory.NAMING_ISSUE, "📝 Naming Issues", "Tasks where files exist but names don't match evidence"),
            (ProblemCategory.SYMBOL_ISSUE, "🔍 Symbol Issues", "Tasks where files exist but symbols not found"),
            (ProblemCategory.CONTENT_ISSUE, "📄 Content Issues", "Tasks where files exist but content doesn't match"),
            (ProblemCategory.MISSING_CODE, "⚠️ Missing Code", "Tasks with tests but no implementation"),
        ]
        
        for cat, title, desc in category_order:
            tasks = by_category[cat]
            if not tasks:
                continue
            
            f.write(f"## {title}\n\n")
            f.write(f"*{desc}*\n\n")
            f.write(f"**Count:** {len(tasks)} tasks\n\n")
            
            for r in tasks:
                checkbox = "x" if r.checked else " "
                f.write(f"### [{checkbox}] {r.task_id}: {r.title}\n\n")
                
                if r.code_evidence:
                    f.write(f"**Code Evidence:**\n")
                    for er in r.code_evidence:
                        status = "✅" if er.ok else "❌"
                        f.write(f"- {status} Line {er.evidence.line_no}: `{er.evidence.kv['path']}`\n")
                        if not er.ok:
                            f.write(f"  - Reason: {er.reason}\n")
                            if er.file_info:
                                if er.file_info.exists:
                                    f.write(f"  - File exists ({er.file_info.size} bytes)\n")
                                elif er.file_info.similar_files:
                                    f.write(f"  - Similar files found:\n")
                                    for sim in er.file_info.similar_files[:3]:
                                        f.write(f"    - `{sim.name}`\n")
                    f.write("\n")
                
                if r.test_evidence:
                    f.write(f"**Test Evidence:**\n")
                    for er in r.test_evidence:
                        status = "✅" if er.ok else "❌"
                        f.write(f"- {status} Line {er.evidence.line_no}: `{er.evidence.kv['path']}`\n")
                        if not er.ok:
                            f.write(f"  - Reason: {er.reason}\n")
                            if er.file_info:
                                if er.file_info.exists:
                                    f.write(f"  - File exists ({er.file_info.size} bytes)\n")
                                elif er.file_info.similar_files:
                                    f.write(f"  - Similar files found:\n")
                                    for sim in er.file_info.similar_files[:3]:
                                        f.write(f"    - `{sim.name}`\n")
                    f.write("\n")
                
                suggestions = generate_suggestions(r)
                if suggestions:
                    f.write(f"**Recommendations:**\n")
                    for sug in suggestions:
                        f.write(f"{sug}\n")
                    f.write("\n")
                
                f.write("---\n\n")
        
        verified_tasks = by_category[ProblemCategory.VERIFIED]
        if verified_tasks:
            f.write(f"## ✅ Verified Tasks\n\n")
            f.write(f"**Count:** {len(verified_tasks)} tasks\n\n")
            f.write(f"All evidence verified successfully for these tasks:\n\n")
            for r in verified_tasks:
                f.write(f"- {r.task_id}: {r.title}\n")
            f.write("\n")
        
        f.write(f"## 📋 Recommended Actions\n\n")
        
        if marked_done_but_failed > 0:
            f.write(f"### Priority 1: Fix Critical Issues ({marked_done_but_failed} tasks)\n\n")
            f.write(f"These tasks are marked [x] as done but verification failed:\n\n")
            critical_tasks = [r for r in results if r.checked and not r.ok]
            for r in critical_tasks:
                f.write(f"- {r.task_id}: {r.title}\n")
            f.write(f"\n**Action:** Review these tasks and either:\n")
            f.write(f"1. Complete the implementation\n")
            f.write(f"2. Update checkbox to [ ] until complete\n\n")
        
        not_impl = by_category[ProblemCategory.NOT_IMPLEMENTED]
        if not_impl:
            f.write(f"### Priority 2: Implement Missing Features ({len(not_impl)} tasks)\n\n")
            if most_common_missing:
                f.write(f"Focus on these files to fix multiple tasks:\n\n")
                for file, count in most_common_missing[:5]:
                    f.write(f"- Create `{file}` → fixes {count} task(s)\n")
            f.write("\n")
        
        missing_tests = by_category[ProblemCategory.MISSING_TESTS]
        if missing_tests:
            f.write(f"### Priority 3: Add Missing Tests ({len(missing_tests)} tasks)\n\n")
            for r in missing_tests:
                f.write(f"- {r.task_id}: Create tests for {r.title}\n")
            f.write("\n")
        
        naming = by_category[ProblemCategory.NAMING_ISSUE]
        if naming:
            f.write(f"### Priority 4: Fix Naming Issues ({len(naming)} tasks)\n\n")
            f.write(f"Update evidence in tasks.md to use correct filenames\n\n")

    summary_data = {
        "workflow": "smartspec_verify_tasks_progress_enhanced",
        "version": "6.0.0",
        "run_id": run_id,
        "generated_at": datetime.now().isoformat(),
        "inputs": {
            "tasks_path": str(tasks_path),
        },
        "totals": {
            "tasks": total,
            "verified": verified,
            "not_verified": not_verified,
            "marked_done_but_failed": marked_done_but_failed,
        },
        "by_category": {
            cat.value: len(by_category[cat]) for cat in ProblemCategory
        },
        "most_common_missing_files": [
            {"file": file, "count": count} for file, count in most_common_missing
        ],
        "tasks": [
            {
                "task_id": r.task_id,
                "title": r.title,
                "checked": r.checked,
                "verified": r.ok,
                "category": r.category.value,
                "code_evidence_count": len(r.code_evidence),
                "test_evidence_count": len(r.test_evidence),
                "suggestions": generate_suggestions(r),
            }
            for r in results
        ]
    }
    
    with open(out_dir / "summary.json", "w") as f:
        json.dump(summary_data, f, indent=2, ensure_ascii=False)


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

    from datetime import datetime
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = Path(args.out) / run_id
    out_dir.mkdir(parents=True, exist_ok=True)
    
    write_enhanced_report(results, tasks_path, out_dir, run_id)
    
    logger.info(f"Enhanced reports written to: {out_dir}")
    logger.info(f"  - {out_dir / 'report.md'}")
    logger.info(f"  - {out_dir / 'summary.json'}")

    total = len(results)
    verified = sum(1 for r in results if r.ok)
    not_verified = total - verified
    
    print(f"\n{'='*60}")
    print(f"VERIFICATION SUMMARY")
    print(f"{'='*60}")
    print(f"Total Tasks:     {total}")
    print(f"Verified:        {verified} ({verified*100//total if total > 0 else 0}%)")
    print(f"Not Verified:    {not_verified} ({not_verified*100//total if total > 0 else 0}%)")
    print(f"{'='*60}\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
