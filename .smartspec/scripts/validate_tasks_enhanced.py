#!/usr/bin/env python3
"""SmartSpec Tasks Validation Script (v7.2.1)

Fixes in v7.2.1
---------------
- Correctly scopes the "## Tasks" section: does NOT stop at subheadings like "### Milestone".
  It stops only at the next heading with level <= the Tasks heading level.
- Broader task-id acceptance (still conservative):
  - accepts common IDs like T001, SEC-001, REQ-001, UI-001, TSK-..., TASK-...
  - still avoids treating random words as task IDs
- Path normalization improvements:
  - normalizes Windows backslashes to forward slashes
  - allows leading ./

What this validates
-------------------
- tasks.md has a header table: spec-id | source | generated_by | updated_at
- tasks.md has a Tasks section
- each task item is parseable and has a stable unique ID
- each task has at least one strict evidence hook line:
    evidence: <type> key=value key="value with spaces"
  Types allowed: code|test|docs|ui
- evidence is semantically safe:
  - path= must look like a repo-relative path (not a command)
  - no absolute paths, no traversal
  - UI evidence must include screen=

Compatibility notes
-------------------
This validator supports BOTH:
1) New strict format tasks:
   - [ ] TSK-... Title
     evidence: code path=... contains="..."
2) Legacy format tasks:
   - [ ] **TSK-... Title**
     **Evidence Hooks:**
       - Code: ...
       - Verification: Run ...

But: legacy "Evidence Hooks" and "Verification" lines are NOT treated as strict evidence.
If strict evidence lines are missing, the task is INVALID for strict verification.

Usage:
  python3 validate_tasks_enhanced.py --tasks <path_to_tasks.md> [--spec <path_to_spec.md>] [--strict-sections]

Exit codes:
  0 - Valid
  1 - Invalid (errors)
  2 - Invalid args / file not found
"""

from __future__ import annotations

import argparse
import re
import shlex
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


# -----------------------------
# Spec parser (optional)
# -----------------------------


class SpecParser:
    """Parses spec.md to extract requirements and references."""

    def __init__(self, spec_path: Path):
        self.spec_path = spec_path
        self.content = ""
        self.sec_requirements: Dict[str, str] = {}
        self.t_references: Set[str] = set()

    def parse(self) -> bool:
        if not self.spec_path.exists():
            return False

        self.content = self.spec_path.read_text(encoding="utf-8", errors="ignore")
        self._extract_sec_requirements()
        self._extract_t_references()
        return True

    def _extract_sec_requirements(self) -> None:
        # Pattern: SEC-001 (Title): description...
        pattern = r"SEC-(\d{3})\s*\([^)]+\):\s*([^\n]+)"
        for sec_num, description in re.findall(pattern, self.content):
            sec_id = f"SEC-{sec_num}"
            self.sec_requirements[sec_id] = description.strip()

    def _extract_t_references(self) -> None:
        # Pattern: T001, T010, etc.
        for t_num in re.findall(r"\bT(\d{3})\b", self.content):
            self.t_references.add(f"T{t_num}")


# -----------------------------
# Tasks parsing
# -----------------------------


VALID_EVIDENCE_TYPES = {"code", "test", "docs", "ui"}

# Suspicious command starters that must NOT appear in path=
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
}

# Task line formats supported
TASK_LINE_NEW = re.compile(r"^\s*-\s*\[([ xX])\]\s+(\S+)\s*(.*?)\s*$")
TASK_LINE_LEGACY_BOLD = re.compile(r"^\s*-\s*\[([ xX])\]\s+\*\*([^*]+)\*\*\s*$")


@dataclass
class TaskBlock:
    task_id: str
    title: str
    checked: bool
    start_line: int
    block_text: str
    evidence_lines: List[str]


_ID_STRICT_PATTERNS = [
    # Common SmartSpec-ish IDs
    re.compile(r"^TSK-[a-zA-Z0-9_\-]+-\d{2,4}$"),
    re.compile(r"^TSK-[a-zA-Z0-9_\-]+$"),
    # Common requirement IDs
    re.compile(r"^(SEC|REQ|NFR|UI)-\d{3,4}$"),
    # Simple ticket IDs
    re.compile(r"^T\d{3,4}$"),
    re.compile(r"^TASK-\d{1,6}$"),
]


def looks_like_task_id(token: str) -> bool:
    tok = (token or "").strip()
    if not tok:
        return False
    if len(tok) > 64:
        return False
    if re.fullmatch(r"[-_]+", tok):
        return False

    for pat in _ID_STRICT_PATTERNS:
        if pat.match(tok):
            return True

    # Conservative fallback: must contain '-' AND a digit
    if "-" in tok and any(ch.isdigit() for ch in tok):
        return True

    return False


def split_task_blocks(tasks_text: str) -> List[TaskBlock]:
    """Split tasks.md into task blocks under the Tasks section."""

    # Locate Tasks section and its heading level
    m = re.search(r"^(#{1,6})\s+Tasks\s*$", tasks_text, re.IGNORECASE | re.MULTILINE)
    if not m:
        return []

    tasks_level = len(m.group(1))
    start = m.end()

    # Stop only at next heading with level <= tasks_level
    next_section = re.search(rf"^#{{1,{tasks_level}}}\s+\S", tasks_text[start:], re.MULTILINE)
    end = start + next_section.start() if next_section else len(tasks_text)

    section = tasks_text[start:end]
    lines = section.splitlines()

    blocks: List[TaskBlock] = []
    cur_lines: List[str] = []
    cur_id: Optional[str] = None
    cur_title: str = ""
    cur_checked: bool = False
    cur_start_line: int = 0

    def flush() -> None:
        nonlocal cur_lines, cur_id, cur_title, cur_checked, cur_start_line
        if cur_id:
            block_text = "\n".join(cur_lines)
            evidence = extract_evidence_lines(block_text)
            blocks.append(
                TaskBlock(
                    task_id=cur_id,
                    title=cur_title,
                    checked=cur_checked,
                    start_line=cur_start_line,
                    block_text=block_text,
                    evidence_lines=evidence,
                )
            )
        cur_lines = []
        cur_id = None
        cur_title = ""
        cur_checked = False
        cur_start_line = 0

    # Track original line numbers within full doc
    doc_lines = tasks_text.splitlines()
    tasks_header_line = 1
    for idx, dl in enumerate(doc_lines, 1):
        if re.match(r"^#{1,6}\s+Tasks\s*$", dl, re.IGNORECASE):
            tasks_header_line = idx
            break

    for i, line in enumerate(lines, 1):
        m1 = TASK_LINE_NEW.match(line)
        if m1:
            possible_id = m1.group(2)
            if looks_like_task_id(possible_id):
                flush()
                cur_checked = (m1.group(1).lower() == "x")
                cur_id = possible_id
                cur_title = (m1.group(3) or "").strip()
                cur_start_line = tasks_header_line + i
                cur_lines = [line]
                continue

        m2 = TASK_LINE_LEGACY_BOLD.match(line)
        if m2:
            flush()
            cur_checked = (m2.group(1).lower() == "x")
            title_full = m2.group(2).strip()
            tid = extract_task_id_from_text(title_full)
            cur_id = tid or (title_full.split()[0] if title_full.split() else title_full)
            cur_title = title_full
            cur_start_line = tasks_header_line + i
            cur_lines = [line]
            continue

        if cur_id:
            cur_lines.append(line)

    flush()
    return blocks


def extract_task_id_from_text(text: str) -> Optional[str]:
    for tok in re.split(r"\s+", text.strip()):
        if looks_like_task_id(tok):
            return tok.strip()
    for tok in re.split(r"\s+", text.strip()):
        if "-" in tok and any(ch.isdigit() for ch in tok):
            return tok.strip()
    return None


def extract_evidence_lines(block_text: str) -> List[str]:
    evidence: List[str] = []
    for line in block_text.splitlines():
        low = line.lower()
        if "evidence:" not in low:
            continue

        start = 0
        while True:
            pos = low.find("evidence:", start)
            if pos < 0:
                break
            frag = line[pos:].strip()
            frag = frag.rstrip().rstrip("|").rstrip()
            evidence.append(frag)
            start = pos + len("evidence:")

    return evidence


def parse_header_ok(tasks_text: str) -> bool:
    header_pattern = r"\|\s*spec-id\s*\|\s*source\s*\|\s*generated_by\s*\|\s*updated_at\s*\|"
    return bool(re.search(header_pattern, tasks_text, re.IGNORECASE))


# -----------------------------
# Evidence parsing + validation
# -----------------------------


def parse_evidence_hook(raw: str) -> Tuple[str, Dict[str, str]]:
    raw = raw.strip()
    if not raw.lower().startswith("evidence:"):
        raise ValueError("evidence line must start with 'evidence:'")

    payload = raw[len("evidence:") :].strip()
    if not payload:
        raise ValueError("empty evidence payload")

    tokens = shlex.split(payload)
    if not tokens:
        raise ValueError("cannot parse evidence")

    ev_type = tokens[0]
    if ev_type not in VALID_EVIDENCE_TYPES:
        raise ValueError(f"invalid evidence type: {ev_type}")

    params: Dict[str, str] = {}
    for t in tokens[1:]:
        if "=" not in t:
            continue
        k, v = t.split("=", 1)
        params[k.strip()] = v.strip()

    return ev_type, params


def _normalize_path(p: str) -> str:
    p = (p or "").strip().strip('"\'')
    p = p.replace("\\", "/")
    if p.startswith("./"):
        p = p[2:]
    p = re.sub(r"/{2,}", "/", p)
    return p


def _is_rel_path(p: str) -> bool:
    p = _normalize_path(p)
    if not p:
        return False
    if p.startswith("/") or re.match(r"^[a-zA-Z]:/", p):
        return False
    if ".." in Path(p).parts:
        return False
    return True


def _looks_like_command_path(p: str) -> bool:
    p = _normalize_path(p)
    if any(ch.isspace() for ch in p):
        return True
    first = p.strip().split("/", 1)[0].lower()
    return first in SUSPICIOUS_PATH_PREFIXES


def validate_evidence(raw: str) -> Tuple[bool, str]:
    try:
        ev_type, params = parse_evidence_hook(raw)
    except Exception as e:
        return False, f"unparseable evidence: {e}"

    if ev_type in {"code", "test", "docs"}:
        path = _normalize_path(params.get("path", ""))
        if not path:
            return False, "missing required path= for code/test/docs evidence"
        if not _is_rel_path(path):
            return False, f"invalid path (must be repo-relative, no traversal): {path}"
        if _looks_like_command_path(path):
            return False, f"path looks like a command (use command= instead): path={path}"

        if path.endswith("/"):
            if "contains" not in params and "symbol" not in params and "heading" not in params:
                return False, "directory path evidence must include contains=/symbol=/heading= to be verifiable"

    if ev_type == "ui":
        if "screen" not in params or not params.get("screen"):
            return False, "ui evidence requires screen="

    return True, "ok"


# -----------------------------
# Validator
# -----------------------------


class TasksValidator:
    SECRET_PATTERNS = [
        r"api[_-]?key\s*[:=]\s*[\"\']?[a-zA-Z0-9]{20,}",
        r"password\s*[:=]\s*[\"\']?[^\"\'\s]{8,}",
        r"token\s*[:=]\s*[\"\']?[a-zA-Z0-9]{20,}",
        r"secret\s*[:=]\s*[\"\']?[a-zA-Z0-9]{20,}",
    ]

    LEGACY_SECTIONS = [
        "Readiness Checklist",
        "Evidence Mapping",
        "Open Questions",
    ]

    TRACEABILITY_SECTIONS = [
        "Requirement Traceability Matrix",
        "Security Requirements Coverage",
        "Functional Requirements Coverage",
    ]

    def __init__(self, tasks_path: Path, spec_parser: Optional[SpecParser], strict_sections: bool):
        self.tasks_path = tasks_path
        self.spec_parser = spec_parser
        self.strict_sections = strict_sections

        self.content = ""
        self.errors: List[str] = []
        self.warnings: List[str] = []

        self.task_ids: Set[str] = set()
        self.rtm_sec_requirements: Set[str] = set()
        self.rtm_t_references: Set[str] = set()

    def validate(self) -> Tuple[bool, List[str], List[str]]:
        if not self.tasks_path.exists():
            self.errors.append(f"Tasks file not found: {self.tasks_path}")
            return False, self.errors, self.warnings

        self.content = self.tasks_path.read_text(encoding="utf-8", errors="ignore")

        self._validate_header()
        self._validate_tasks_section_exists()
        self._validate_tasks_blocks()
        self._validate_no_secrets()

        self._validate_legacy_sections_optional()

        if self.spec_parser:
            self._validate_traceability_optional()

        return len(self.errors) == 0, self.errors, self.warnings

    def _validate_header(self) -> None:
        if not parse_header_ok(self.content):
            self.errors.append("Missing required header table with fields: spec-id, source, generated_by, updated_at")

    def _validate_tasks_section_exists(self) -> None:
        if not re.search(r"^#{1,6}\s+Tasks\s*$", self.content, re.IGNORECASE | re.MULTILINE):
            self.errors.append("Missing required section: Tasks")

    def _validate_tasks_blocks(self) -> None:
        blocks = split_task_blocks(self.content)
        if not blocks:
            self.errors.append("No task items found in Tasks section")
            return

        for b in blocks:
            if b.task_id in self.task_ids:
                self.errors.append(f"Duplicate Task ID found: {b.task_id} (line ~{b.start_line})")
            else:
                self.task_ids.add(b.task_id)

            if not b.evidence_lines:
                self.errors.append(f"{b.task_id}: Missing strict evidence hooks (no 'evidence:' lines found)")
                continue

            any_ok = False
            for ev in b.evidence_lines:
                ok, msg = validate_evidence(ev)
                if ok:
                    any_ok = True
                else:
                    self.errors.append(f"{b.task_id}: {msg} (evidence: {ev})")

            if not any_ok:
                self.errors.append(f"{b.task_id}: No valid evidence hooks found")

    def _validate_no_secrets(self) -> None:
        for pattern in self.SECRET_PATTERNS:
            if re.search(pattern, self.content, re.IGNORECASE):
                self.errors.append(
                    f"Potential secret detected (pattern: {pattern[:40]}...). Secrets must not be present in tasks.md"
                )

    def _validate_legacy_sections_optional(self) -> None:
        for sec in self.LEGACY_SECTIONS:
            pattern = rf"^#{{1,6}}\s+{re.escape(sec)}\s*$"
            if not re.search(pattern, self.content, re.IGNORECASE | re.MULTILINE):
                if self.strict_sections:
                    self.errors.append(f"Missing required section (strict): {sec}")
                else:
                    self.warnings.append(f"Missing legacy section (optional): {sec}")

    def _validate_traceability_optional(self) -> None:
        found_any = any(
            re.search(rf"^#{{1,6}}\s+{re.escape(s)}\s*$", self.content, re.IGNORECASE | re.MULTILINE)
            for s in self.TRACEABILITY_SECTIONS
        )
        if not found_any:
            self.warnings.append("Traceability sections not found; skipping spec coverage checks")
            return

        sec_coverage_match = re.search(
            r"^#{{1,6}}\s+Security\s+Requirements\s+Coverage.*?(?=^#{{1,6}}\s+|\Z)",
            self.content,
            re.MULTILINE | re.DOTALL | re.IGNORECASE,
        )
        if sec_coverage_match:
            self.rtm_sec_requirements = set(re.findall(r"(SEC-\d{3})", sec_coverage_match.group(0)))

        t_coverage_match = re.search(
            r"^#{{1,6}}\s+Functional\s+Requirements\s+Coverage.*?(?=^#{{1,6}}\s+|\Z)",
            self.content,
            re.MULTILINE | re.DOTALL | re.IGNORECASE,
        )
        if t_coverage_match:
            self.rtm_t_references = set(re.findall(r"(T\d{3,4})", t_coverage_match.group(0)))

        missing_sec = set(self.spec_parser.sec_requirements.keys()) - self.rtm_sec_requirements
        if missing_sec:
            for sec_id in sorted(missing_sec):
                self.errors.append(
                    f"SEC requirement not in RTM: {sec_id} ({self.spec_parser.sec_requirements[sec_id][:60]}...)"
                )

        missing_t = self.spec_parser.t_references - {t[:4] for t in self.rtm_t_references}
        if missing_t:
            if len(missing_t) > 10:
                self.warnings.append(
                    f"{len(missing_t)} T-references from spec.md not found in RTM (showing 10): {', '.join(sorted(list(missing_t))[:10])}..."
                )
            else:
                for t_id in sorted(missing_t):
                    self.warnings.append(f"T-reference not in RTM: {t_id}")


# -----------------------------
# CLI
# -----------------------------


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate SmartSpec tasks.md (strict evidence hooks)")
    parser.add_argument("--tasks", required=True, help="Path to tasks.md")
    parser.add_argument("--spec", help="Path to spec.md (optional, enables RTM checks if sections exist)")
    parser.add_argument(
        "--strict-sections",
        action="store_true",
        help="Require legacy sections (Readiness Checklist, Evidence Mapping, Open Questions). Default: warn only.",
    )

    args = parser.parse_args()

    tasks_path = Path(args.tasks)
    if not tasks_path.exists():
        print(f"Error: tasks file not found: {tasks_path}", file=sys.stderr)
        return 2

    spec_parser: Optional[SpecParser] = None
    if args.spec:
        spec_path = Path(args.spec)
        spec_parser = SpecParser(spec_path)
        if not spec_parser.parse():
            print(f"Error: could not parse spec file: {spec_path}", file=sys.stderr)
            return 2

    validator = TasksValidator(tasks_path, spec_parser, strict_sections=bool(args.strict_sections))
    is_valid, errors, warnings = validator.validate()

    print("\n" + "=" * 60)
    print("SmartSpec Tasks Validation Report")
    print("=" * 60)
    print(f"Tasks File: {tasks_path}")
    if args.spec:
        print(f"Spec File:  {args.spec}")
    print()

    if spec_parser:
        print("📊 Spec Analysis:")
        print(f"  - SEC Requirements: {len(spec_parser.sec_requirements)}")
        print(f"  - T-References:     {len(spec_parser.t_references)}")
        print()

    print("📊 Tasks Analysis:")
    print(f"  - Total Tasks Parsed: {len(validator.task_ids)}")
    print()

    if errors:
        print(f"❌ ERRORS ({len(errors)}):")
        for e in errors:
            print(f"  - {e}")
        print()

    if warnings:
        print(f"⚠️  WARNINGS ({len(warnings)}):")
        for w in warnings:
            print(f"  - {w}")
        print()

    if is_valid:
        print("✅ Tasks file is VALID for strict evidence verification")
        print("=" * 60 + "\n")
        return 0

    print("❌ Tasks file is INVALID - please fix errors above")
    print("=" * 60 + "\n")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
