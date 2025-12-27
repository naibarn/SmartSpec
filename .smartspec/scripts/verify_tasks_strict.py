#!/usr/bin/env python3
"""
verify_tasks_strict.py (v2.0.0)

Strict evidence-only verification for tasks.md.
- Checkboxes are NOT authoritative.
- Evidence hooks MUST be canonical: `evidence: <type> key=value ...`
- Writes reports ONLY under: <out>/<run_id>/ (or default .spec/reports/verify-tasks-progress/<run_id>/)

Outputs:
- verification-report.json
- verification-report.md
- summary.json (compact; used by sync checkbox workflow)
"""

from __future__ import annotations

import argparse
import json
import re
import hashlib
import sys
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Import naming convention helper
sys.path.insert(0, str(Path(__file__).parent))
from naming_convention_helper import (
    load_naming_standard,
    validate_file_path,
    find_similar_files_with_naming
)


class TaskStatus(Enum):
    VERIFIED = "verified"
    NOT_VERIFIED = "not_verified"
    MISSING_EVIDENCE = "missing_evidence"
    INVALID_EVIDENCE = "invalid_evidence"
    INVALID_SCOPE = "invalid_scope"
    NEEDS_MANUAL = "needs_manual"
    NAMING_ISSUE = "naming_issue"  # Expected path violates naming convention
    NAMING_VIOLATION = "naming_violation"  # Found file violates naming convention


class EvidenceType(Enum):
    CODE = "code"
    TEST = "test"
    DOCS = "docs"
    UI = "ui"


ALLOWED_EVIDENCE_KEYS = {
    "path",
    "contains",
    "regex",
    "symbol",
    "heading",
    "selector",
    "command",
    # optional trace fields (ignore if present)
    "implements",
    "t_ref",
    "acceptance",
}


@dataclass
class EvidenceHook:
    raw: str
    type: Any  # EvidenceType or str if invalid
    params: Dict[str, str]
    line_number: int


@dataclass
class TaskResult:
    task_id: str
    title: str
    checkbox_status: str  # "[x]" or "[ ]"
    status: TaskStatus
    evidence_hooks: List[EvidenceHook]
    matched_hooks: List[EvidenceHook]
    reasons: List[str]
    line_number: int


def _now_utc_iso() -> str:
    return datetime.utcnow().isoformat(timespec="seconds") + "Z"


def _mk_run_id() -> str:
    # stable + sortable
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def _sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8", errors="ignore")).hexdigest()


class TasksVerifier:
    def __init__(self, workspace_root: str, tasks_md_path: str):
        self.workspace_root = Path(workspace_root).resolve()
        self.tasks_md_path = Path(tasks_md_path).resolve()

        self.max_file_size = 10 * 1024 * 1024  # 10MB
        self.max_excerpt_chars = 500

        self.spec_id = self._extract_spec_id()
        self.naming_standard = load_naming_standard(self.workspace_root)
        self.naming_issues: List[Dict] = []

    def _extract_spec_id(self) -> str:
        # Try header first
        try:
            for line in _read_text(self.tasks_md_path).splitlines():
                if "spec-id" in line.lower():
                    # be permissive: take value after spec-id if present
                    m = re.search(r"spec-id\s*\|\s*([A-Za-z0-9._:-]+)", line, re.IGNORECASE)
                    if m:
                        return m.group(1)
                    m = re.search(r"(spec-[a-z0-9._:-]+)", line, re.IGNORECASE)
                    if m:
                        return m.group(1)
        except Exception:
            pass

        # Fallback to folder segment like spec-core-001-authentication
        for part in self.tasks_md_path.parts:
            if part.startswith("spec-"):
                return part
        return "unknown"

    def parse_tasks(self) -> List[Tuple[str, str, str, int, List[Tuple[int, str]]]]:
        """
        Returns: List of (task_id, title, checkbox_status, line_number, evidence_lines[(line_no, text)])
        """
        tasks: List[Tuple[str, str, str, int, List[Tuple[int, str]]]] = []
        current: Optional[Tuple[str, str, str, int]] = None
        evidence_lines: List[Tuple[int, str]] = []

        lines = _read_text(self.tasks_md_path).splitlines()
        for i, line in enumerate(lines, 1):
            # Match: - [x] TSK-AUTH-001 [P] Title  OR  - [ ] TSK-AUTH-001 Title
            m = re.match(r"^\s*-\s*\[([xX ])\]\s+(TSK-[A-Z0-9]+-\d+)\s*(?:\[P\])?\s*(.+?)\s*$", line)
            if m:
                if current is not None:
                    task_id, title, chk, ln = current
                    tasks.append((task_id, title, chk, ln, evidence_lines.copy()))
                checkbox = "x" if m.group(1).lower() == "x" else " "
                task_id = m.group(2).strip()
                title = m.group(3).strip()
                current = (task_id, title, f"[{checkbox}]", i)
                evidence_lines = []
                continue

            if current is not None:
                # Evidence lines MUST start with evidence: or - evidence:
                if re.match(r"^\s*(?:-\s*)?evidence:\s+", line, re.IGNORECASE):
                    evidence_lines.append((i, line.strip()))

        if current is not None:
            task_id, title, chk, ln = current
            tasks.append((task_id, title, chk, ln, evidence_lines.copy()))
        return tasks

    def parse_evidence_hooks(self, evidence_lines: List[Tuple[int, str]]) -> List[EvidenceHook]:
        hooks: List[EvidenceHook] = []
        for ln, raw in evidence_lines:
            m = re.search(r"evidence:\s+(\w+)\s*(.*)$", raw, re.IGNORECASE)
            if not m:
                continue
            type_str = m.group(1).lower().strip()
            params_str = (m.group(2) or "").strip()

            # type
            try:
                et = EvidenceType(type_str)
            except ValueError:
                hooks.append(EvidenceHook(raw=raw, type=type_str, params={}, line_number=ln))
                continue

            # key=value parse (supports quoted values)
            params: Dict[str, str] = {}
            # allow: key="a b" OR key=a
            for pm in re.finditer(r'(\w+)=(?:"([^"]*)"|([^\s]+))', params_str):
                k = pm.group(1)
                v = pm.group(2) or pm.group(3) or ""
                params[k] = v

            hooks.append(EvidenceHook(raw=raw, type=et, params=params, line_number=ln))
        return hooks

    def _validate_path_scope(self, rel_path: str) -> Tuple[bool, Optional[str]]:
        # Must be repo-relative; deny traversal/absolute
        rp = (rel_path or "").strip().replace("\\", "/")
        if not rp:
            return False, "Missing path"
        if rp.startswith("/") or re.match(r"^[A-Za-z]:/", rp):
            return False, "Absolute path not allowed"
        if ".." in Path(rp).parts:
            return False, "Path traversal '..' not allowed"
        # Resolve against workspace
        abs_path = (self.workspace_root / rp).resolve()
        try:
            abs_path.relative_to(self.workspace_root)
        except ValueError:
            return False, "Path escapes workspace root"
        return True, None

    def _read_file_content(self, rel_path: str) -> Tuple[bool, Optional[str], Optional[str]]:
        ok, reason = self._validate_path_scope(rel_path)
        if not ok:
            return False, reason, None

        abs_path = (self.workspace_root / rel_path).resolve()
        try:
            if abs_path.is_dir():
                return False, "Path is a directory", None
            if not abs_path.exists():
                return False, "File not found", None
            if abs_path.stat().st_size > self.max_file_size:
                return False, "File too large", None

            # binary sniff
            with abs_path.open("rb") as f:
                chunk = f.read(8192)
                if b"\x00" in chunk:
                    return False, "Binary file", None

            return True, None, abs_path.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            return False, f"Read error: {e}", None

    def verify_hook(self, hook: EvidenceHook) -> Tuple[bool, List[str]]:
        if not isinstance(hook.type, EvidenceType):
            return False, [f"Invalid evidence type: {hook.type}"]

        # reject unknown keys (strict)
        for k in hook.params.keys():
            if k not in ALLOWED_EVIDENCE_KEYS:
                return False, [f"Unknown evidence key: {k}"]

        path = hook.params.get("path", "")
        ok, reason = self._validate_path_scope(path)
        if not ok:
            return False, [reason or "Invalid path"]
        
        # Check naming convention for expected path
        naming_result = validate_file_path(path, self.naming_standard)
        if not naming_result.compliant:
            # Log naming issue but continue verification
            self.naming_issues.append({
                'path': path,
                'issues': naming_result.issues,
                'type': 'expected_path'
            })

        if hook.type == EvidenceType.UI:
            # UI is not statically verifiable in this strict script
            return False, ["UI evidence requires manual verification"]

        success, read_reason, content = self._read_file_content(path)
        if not success:
            return False, [read_reason or "Read failed"]

        assert content is not None
        reasons: List[str] = []

        # contains
        if "contains" in hook.params and hook.params["contains"] not in content:
            return False, [f"contains not found: {hook.params['contains']}"]

        # regex
        if "regex" in hook.params:
            try:
                if not re.search(hook.params["regex"], content, re.MULTILINE):
                    return False, [f"regex not matched: {hook.params['regex']}"]
            except re.error as e:
                return False, [f"invalid regex: {e}"]

        # symbol (best-effort)
        if hook.type == EvidenceType.CODE and "symbol" in hook.params:
            sym = hook.params["symbol"]
            patterns = [
                rf"\bclass\s+{re.escape(sym)}\b",
                rf"\bfunction\s+{re.escape(sym)}\b",
                rf"\binterface\s+{re.escape(sym)}\b",
                rf"\btype\s+{re.escape(sym)}\b",
                rf"\bexport\s+.*\b{re.escape(sym)}\b",
            ]
            if not any(re.search(p, content) for p in patterns):
                return False, [f"symbol not found: {sym}"]

        # docs heading
        if hook.type == EvidenceType.DOCS and "heading" in hook.params:
            heading = hook.params["heading"]
            if not re.search(rf"^#+\s*{re.escape(heading)}\s*$", content, re.MULTILINE):
                return False, [f"heading not found: {heading}"]

        return True, reasons

    def verify_task(self, task_id: str, title: str, checkbox_status: str, line_number: int, evidence_lines: List[Tuple[int, str]]) -> TaskResult:
        hooks = self.parse_evidence_hooks(evidence_lines)
        if not hooks:
            return TaskResult(
                task_id=task_id,
                title=title,
                checkbox_status=checkbox_status,
                status=TaskStatus.MISSING_EVIDENCE,
                evidence_hooks=[],
                matched_hooks=[],
                reasons=["No evidence hooks found"],
                line_number=line_number,
            )

        matched: List[EvidenceHook] = []
        reasons: List[str] = []
        invalid = False
        has_ui = False

        for h in hooks:
            if isinstance(h.type, EvidenceType) and h.type == EvidenceType.UI:
                has_ui = True
            ok, rs = self.verify_hook(h)
            if ok:
                matched.append(h)
            else:
                reasons.extend([f"{h.raw}: {r}" for r in rs])
                if rs and (rs[0].startswith("Invalid evidence") or rs[0].startswith("Unknown evidence") or rs[0].startswith("Missing")):
                    invalid = True

        if invalid:
            st = TaskStatus.INVALID_EVIDENCE
        elif matched:
            st = TaskStatus.VERIFIED
        elif has_ui:
            st = TaskStatus.NEEDS_MANUAL
        else:
            st = TaskStatus.NOT_VERIFIED

        return TaskResult(
            task_id=task_id,
            title=title,
            checkbox_status=checkbox_status,
            status=st,
            evidence_hooks=hooks,
            matched_hooks=matched,
            reasons=reasons,
            line_number=line_number,
        )

    def verify_all(self) -> Dict[str, Any]:
        tasks = self.parse_tasks()
        results: List[TaskResult] = []
        for tid, title, chk, ln, evs in tasks:
            results.append(self.verify_task(tid, title, chk, ln, evs))

        counts = {s.value: 0 for s in TaskStatus}
        for r in results:
            counts[r.status.value] += 1

        total = len(results)
        verified = counts["verified"]
        verified_pct = round((verified / total * 100) if total else 0.0, 2)

        # full report
        full = {
            "workflow": "smartspec_verify_tasks_progress_strict",
            "version": "2.0.0",
            "spec_id": self.spec_id,
            "tasks_md_path": str(self.tasks_md_path.relative_to(self.workspace_root)),
            "verification_timestamp": _now_utc_iso(),
            "summary": {
                "total_tasks": total,
                "verified": verified,
                "not_verified": counts["not_verified"],
                "missing_evidence": counts["missing_evidence"],
                "invalid_evidence": counts["invalid_evidence"],
                "invalid_scope": counts["invalid_scope"],
                "needs_manual": counts["needs_manual"],
                "naming_issue": counts.get("naming_issue", 0),
                "naming_violation": counts.get("naming_violation", 0),
                "verified_percentage": verified_pct,
            },
            "naming_issues": self.naming_issues,
            "tasks": [
                {
                    "task_id": r.task_id,
                    "title": r.title,
                    "checkbox_status": r.checkbox_status,
                    "status": r.status.value,
                    "line_number": r.line_number,
                    "reasons": r.reasons,
                    "evidence": [{"raw": h.raw, "type": (h.type.value if isinstance(h.type, EvidenceType) else str(h.type)), "params": h.params, "line": h.line_number} for h in r.evidence_hooks],
                    "matched": [{"raw": h.raw, "type": h.type.value, "params": h.params, "line": h.line_number} for h in r.matched_hooks if isinstance(h.type, EvidenceType)],
                }
                for r in results
            ],
        }
        return full


def _md_report(full: Dict[str, Any]) -> str:
    s = full["summary"]
    lines = []
    lines.append("# Tasks Verification Report\n")
    lines.append(f"- Spec ID: `{full['spec_id']}`\n")
    lines.append(f"- Tasks File: `{full['tasks_md_path']}`\n")
    lines.append(f"- Time: {full['verification_timestamp']}\n\n")
    lines.append("## Summary\n\n")
    lines.append("| Metric | Count |\n|---|---|\n")
    lines.append(f"| Total | {s['total_tasks']} |\n")
    lines.append(f"| ✅ Verified | {s['verified']} |\n")
    lines.append(f"| ❌ Not Verified | {s['not_verified']} |\n")
    lines.append(f"| ⚠️ Missing Evidence | {s['missing_evidence']} |\n")
    lines.append(f"| 🚫 Invalid Evidence | {s['invalid_evidence']} |\n")
    lines.append(f"| 👤 Needs Manual | {s['needs_manual']} |\n")
    lines.append(f"| 📝 Naming Issue | {s.get('naming_issue', 0)} |\n")
    lines.append(f"| 🔤 Naming Violation | {s.get('naming_violation', 0)} |\n")
    lines.append(f"| **Verified %** | **{s['verified_percentage']}%** |\n")
    lines.append("\n")
    
    # Add naming issues section if any
    naming_issues = full.get("naming_issues", [])
    if naming_issues:
        lines.append("## Naming Convention Issues\n\n")
        for issue in naming_issues:
            lines.append(f"**{issue['path']}** ({issue['type']})\n")
            for problem in issue['issues']:
                lines.append(f"- {problem}\n")
            lines.append("\n")
        
        lines.append("### Recommendations\n\n")
        lines.append("1. Run naming convention validator:\n")
        lines.append("   ```bash\n")
        lines.append("   python3 .smartspec/scripts/validate_naming_convention.py --fix\n")
        lines.append("   ```\n\n")
        lines.append("2. Update tasks.md with corrected paths\n\n")
        lines.append("3. Re-run verification\n\n")
    
    return "".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Strict tasks progress verification (evidence-only)")
    ap.add_argument("tasks_md", help="Path to tasks.md")
    ap.add_argument("--workspace", default=".", help="Workspace root (default: .)")
    ap.add_argument("--out", default=".spec/reports/verify-tasks-progress", help="Reports root (default: .spec/reports/verify-tasks-progress)")
    ap.add_argument("--report-format", choices=["md", "json", "both"], default="both")
    ap.add_argument("--json", action="store_true", help="Print JSON to stdout (full report)")
    ap.add_argument("--quiet", action="store_true", help="Less console output")
    args = ap.parse_args()

    verifier = TasksVerifier(args.workspace, args.tasks_md)
    full = verifier.verify_all()

    # Always create a run folder under out
    run_id = _mk_run_id()
    out_root = Path(args.out)
    out_dir = out_root / run_id
    out_dir.mkdir(parents=True, exist_ok=True)

    # Write outputs
    if args.report_format in ("json", "both"):
        (out_dir / "verification-report.json").write_text(json.dumps(full, indent=2), encoding="utf-8")

    if args.report_format in ("md", "both"):
        (out_dir / "verification-report.md").write_text(_md_report(full), encoding="utf-8")

    # summary.json for sync workflow
    summary = {
        "workflow": "smartspec_verify_tasks_progress_strict",
        "version": "2.0.0",
        "run_id": run_id,
        "generated_at": full["verification_timestamp"],
        "inputs": {"tasks_path": full["tasks_md_path"], "spec_id": full["spec_id"]},
        "totals": {
            "tasks": full["summary"]["total_tasks"],
            "verified": full["summary"]["verified"],
            "not_verified": full["summary"]["not_verified"],
            "manual": full["summary"]["needs_manual"],
            "missing_hooks": full["summary"]["missing_evidence"],
            "invalid_scope": full["summary"]["invalid_scope"],
        },
        # minimal per-task mapping for sync
        "results": [
            {
                "task_id": t["task_id"],
                "title": t["title"],
                "checked": (t["checkbox_status"] == "[x]"),
                "verified": (t["status"] == "verified"),
                "status": t["status"],
            }
            for t in full["tasks"]
        ],
        "writes": {"reports": [str(out_dir / "verification-report.md"), str(out_dir / "verification-report.json"), str(out_dir / "summary.json")]},
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    if args.json:
        print(json.dumps(full, indent=2))

    if not args.quiet:
        s = full["summary"]
        print(f"✅ Wrote reports to: {out_dir}")
        print(f"  Total: {s['total_tasks']}, Verified: {s['verified']} ({s['verified_percentage']}%)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
