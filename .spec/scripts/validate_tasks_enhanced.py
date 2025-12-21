#!/usr/bin/env python3
"""
SmartSpec Tasks Validation Script (Enhanced with Traceability)

Validates that tasks.md contains all required sections, proper task format,
evidence-first elements, and complete requirement traceability.

Usage:
    python3 validate_tasks_enhanced.py --tasks <path_to_tasks.md> [--spec <path_to_spec.md>]

Exit codes:
    0 - Tasks file is complete and valid
    1 - Tasks file is missing required sections or has errors
    2 - Invalid arguments or file not found
"""

import sys
import re
import argparse
from pathlib import Path
from typing import List, Tuple, Set, Dict, Optional


class SpecParser:
    """Parses spec.md to extract requirements and references."""
    
    def __init__(self, spec_path: Path):
        self.spec_path = spec_path
        self.content = ""
        self.sec_requirements: Dict[str, str] = {}
        self.t_references: Set[str] = set()
        
    def parse(self) -> bool:
        """Parse spec.md and extract requirements."""
        if not self.spec_path.exists():
            return False
        
        self.content = self.spec_path.read_text(encoding='utf-8')
        self._extract_sec_requirements()
        self._extract_t_references()
        return True
    
    def _extract_sec_requirements(self):
        """Extract SEC-XXX requirements from spec.md."""
        # Pattern: SEC-001, SEC-002, etc.
        pattern = r'SEC-(\d{3})\s*\([^)]+\):\s*([^\n]+)'
        matches = re.findall(pattern, self.content)
        
        for sec_num, description in matches:
            sec_id = f"SEC-{sec_num}"
            self.sec_requirements[sec_id] = description.strip()
    
    def _extract_t_references(self):
        """Extract T-references (T001, T010, etc.) from spec.md."""
        # Pattern: T001, T010, T014, etc.
        pattern = r'\bT(\d{3})\b'
        matches = re.findall(pattern, self.content)
        
        for t_num in matches:
            self.t_references.add(f"T{t_num}")


class TasksValidator:
    """Validates SmartSpec tasks.md files for completeness and traceability."""
    
    REQUIRED_HEADER_FIELDS = [
        "spec-id",
        "source",
        "generated_by",
        "updated_at"
    ]
    
    REQUIRED_SECTIONS = [
        "Readiness Checklist",
        "Tasks",
        "Evidence Mapping",
        "Open Questions"
    ]
    
    TRACEABILITY_SECTIONS = [
        "Requirement Traceability Matrix",
        "Security Requirements Coverage",
        "Functional Requirements Coverage"
    ]
    
    READINESS_CHECKLIST_ITEMS = [
        "stable, unique ID",
        "evidence hook",
        "TBD evidence",
        "acceptance criteria",
        "secrets"
    ]
    
    EVIDENCE_TYPES = ["Code:", "Test:", "UI:", "Docs:", "Verification:"]
    
    SECRET_PATTERNS = [
        r'api[_-]?key\s*[:=]\s*["\']?[a-zA-Z0-9]{20,}',
        r'password\s*[:=]\s*["\']?[^"\'\s]{8,}',
        r'token\s*[:=]\s*["\']?[a-zA-Z0-9]{20,}',
        r'secret\s*[:=]\s*["\']?[a-zA-Z0-9]{20,}'
    ]
    
    def __init__(self, tasks_path: str, spec_parser: Optional[SpecParser] = None):
        self.tasks_path = Path(tasks_path)
        self.spec_parser = spec_parser
        self.content = ""
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.task_ids: Set[str] = set()
        self.rtm_sec_requirements: Set[str] = set()
        self.rtm_t_references: Set[str] = set()
        
    def validate(self) -> Tuple[bool, List[str], List[str]]:
        """
        Validate the tasks.md file.
        
        Returns:
            Tuple of (is_valid, errors, warnings)
        """
        if not self.tasks_path.exists():
            self.errors.append(f"Tasks file not found: {self.tasks_path}")
            return False, self.errors, self.warnings
        
        self.content = self.tasks_path.read_text(encoding='utf-8')
        
        # Run all validation checks
        self._validate_header()
        self._validate_required_sections()
        self._validate_readiness_checklist()
        self._validate_tasks()
        self._validate_evidence_mapping()
        self._validate_tbd_consistency()
        self._validate_no_secrets()
        
        # Run traceability checks if spec.md is provided
        if self.spec_parser:
            self._validate_traceability_sections()
            self._validate_requirement_coverage()
        
        is_valid = len(self.errors) == 0
        return is_valid, self.errors, self.warnings
    
    def _validate_header(self):
        """Check that header table with required fields is present."""
        header_pattern = r'\|\s*spec-id\s*\|\s*source\s*\|\s*generated_by\s*\|\s*updated_at\s*\|'
        if not re.search(header_pattern, self.content, re.IGNORECASE):
            self.errors.append("Missing required header table with fields: spec-id, source, generated_by, updated_at")
            return
        
        header_match = re.search(header_pattern, self.content, re.IGNORECASE)
        if header_match:
            lines_after = self.content[header_match.end():].split('\n', 3)
            if len(lines_after) < 3:
                self.warnings.append("Header table found but no data row detected")
    
    def _validate_required_sections(self):
        """Check that all required sections are present."""
        for section in self.REQUIRED_SECTIONS:
            pattern = rf'^#{{1,3}}\s+{re.escape(section)}'
            if not re.search(pattern, self.content, re.MULTILINE | re.IGNORECASE):
                self.errors.append(f"Missing required section: {section}")
    
    def _validate_readiness_checklist(self):
        """Check that readiness checklist exists and has required items."""
        checklist_match = re.search(
            r'^#{{1,3}}\s+Readiness\s+Checklist.*?(?=^#{{1,3}}\s+|\Z)',
            self.content,
            re.MULTILINE | re.DOTALL | re.IGNORECASE
        )
        
        if not checklist_match:
            return
        
        checklist_content = checklist_match.group(0)
        
        for item in self.READINESS_CHECKLIST_ITEMS:
            if not re.search(re.escape(item), checklist_content, re.IGNORECASE):
                self.warnings.append(f"Readiness checklist missing item about: {item}")
    
    def _validate_tasks(self):
        """Check that tasks section has properly formatted task items."""
        tasks_match = re.search(
            r'^#{{1,3}}\s+Tasks.*?(?=^#{{1,3}}\s+|\Z)',
            self.content,
            re.MULTILINE | re.DOTALL | re.IGNORECASE
        )
        
        if not tasks_match:
            return
        
        tasks_content = tasks_match.group(0)
        
        task_items = re.findall(
            r'^-\s+\[([ x])\]\s+\*\*([^*]+)\*\*.*?(?=^-\s+\[|\Z)',
            tasks_content,
            re.MULTILINE | re.DOTALL
        )
        
        if not task_items:
            self.warnings.append("No task items found in Tasks section")
            return
        
        for checkbox_state, task_title in task_items:
            task_id_match = re.search(r'(TSK-[A-Z0-9]+-\d+)', task_title)
            if not task_id_match:
                self.errors.append(f"Task '{task_title[:50]}...' missing valid Task ID (TSK-<spec-id>-NNN)")
                continue
            
            task_id = task_id_match.group(1)
            
            if task_id in self.task_ids:
                self.errors.append(f"Duplicate Task ID found: {task_id}")
            else:
                self.task_ids.add(task_id)
            
            task_content_match = re.search(
                rf'^-\s+\[([ x])\]\s+\*\*{re.escape(task_title)}\*\*.*?(?=^-\s+\[|\Z)',
                tasks_content,
                re.MULTILINE | re.DOTALL
            )
            
            if task_content_match:
                task_content = task_content_match.group(0)
                
                if not re.search(r'\*\*Acceptance\s+Criteria:\*\*', task_content, re.IGNORECASE):
                    self.warnings.append(f"{task_id}: Missing 'Acceptance Criteria' section")
                
                if not re.search(r'\*\*Evidence\s+Hooks?:\*\*', task_content, re.IGNORECASE):
                    self.errors.append(f"{task_id}: Missing 'Evidence Hooks' section")
                else:
                    has_evidence_type = any(
                        re.search(re.escape(ev_type), task_content, re.IGNORECASE)
                        for ev_type in self.EVIDENCE_TYPES
                    )
                    if not has_evidence_type:
                        self.warnings.append(
                            f"{task_id}: Evidence Hooks section exists but no specific evidence type found "
                            f"(Code:, Test:, UI:, Docs:, Verification:)"
                        )
    
    def _validate_evidence_mapping(self):
        """Check that evidence mapping table exists and includes all task IDs."""
        evidence_match = re.search(
            r'^#{{1,3}}\s+Evidence\s+Mapping.*?(?=^#{{1,3}}\s+|\Z)',
            self.content,
            re.MULTILINE | re.DOTALL | re.IGNORECASE
        )
        
        if not evidence_match:
            return
        
        evidence_content = evidence_match.group(0)
        mapped_task_ids = set(re.findall(r'(TSK-[A-Z0-9]+-\d+)', evidence_content))
        
        for task_id in self.task_ids:
            if task_id not in mapped_task_ids:
                self.warnings.append(f"{task_id}: Found in Tasks section but missing from Evidence Mapping table")
        
        for mapped_id in mapped_task_ids:
            if mapped_id not in self.task_ids:
                self.warnings.append(f"{mapped_id}: Found in Evidence Mapping but not in Tasks section")
    
    def _validate_tbd_consistency(self):
        """Check that tasks with TBD evidence are listed in Open Questions section."""
        tbd_tasks = set()
        tasks_match = re.search(
            r'^#{{1,3}}\s+Tasks.*?(?=^#{{1,3}}\s+|\Z)',
            self.content,
            re.MULTILINE | re.DOTALL | re.IGNORECASE
        )
        
        if tasks_match:
            tasks_content = tasks_match.group(0)
            for task_id in self.task_ids:
                task_pattern = rf'{re.escape(task_id)}.*?(?=TSK-|^#{{1,3}}\s+|\Z)'
                task_match = re.search(task_pattern, tasks_content, re.DOTALL)
                if task_match and re.search(r'\bTBD\b', task_match.group(0), re.IGNORECASE):
                    tbd_tasks.add(task_id)
        
        questions_match = re.search(
            r'^#{{1,3}}\s+Open\s+Questions.*?(?=^#{{1,3}}\s+|\Z)',
            self.content,
            re.MULTILINE | re.DOTALL | re.IGNORECASE
        )
        
        if questions_match:
            questions_content = questions_match.group(0)
            listed_tbd_tasks = set(re.findall(r'(TSK-[A-Z0-9]+-\d+)', questions_content))
            
            for tbd_task in tbd_tasks:
                if tbd_task not in listed_tbd_tasks:
                    self.warnings.append(
                        f"{tbd_task}: Has TBD evidence but not listed in Open Questions section"
                    )
    
    def _validate_no_secrets(self):
        """Check for potential secrets in the content."""
        for pattern in self.SECRET_PATTERNS:
            matches = re.findall(pattern, self.content, re.IGNORECASE)
            if matches:
                self.errors.append(
                    f"Potential secret detected (pattern: {pattern[:30]}...). "
                    "Secrets must not be present in tasks.md"
                )
    
    def _validate_traceability_sections(self):
        """Check that traceability sections exist."""
        for section in self.TRACEABILITY_SECTIONS:
            pattern = rf'^#{{1,3}}\s+{re.escape(section)}'
            if not re.search(pattern, self.content, re.MULTILINE | re.IGNORECASE):
                self.errors.append(f"Missing required traceability section: {section}")
    
    def _validate_requirement_coverage(self):
        """Validate that all requirements from spec.md are covered in tasks.md."""
        if not self.spec_parser:
            return
        
        # Extract SEC requirements from RTM
        sec_coverage_match = re.search(
            r'^#{{1,3}}\s+Security\s+Requirements\s+Coverage.*?(?=^#{{1,3}}\s+|\Z)',
            self.content,
            re.MULTILINE | re.DOTALL | re.IGNORECASE
        )
        
        if sec_coverage_match:
            sec_coverage_content = sec_coverage_match.group(0)
            self.rtm_sec_requirements = set(re.findall(r'(SEC-\d{3})', sec_coverage_content))
        
        # Extract T-references from RTM
        t_coverage_match = re.search(
            r'^#{{1,3}}\s+Functional\s+Requirements\s+Coverage.*?(?=^#{{1,3}}\s+|\Z)',
            self.content,
            re.MULTILINE | re.DOTALL | re.IGNORECASE
        )
        
        if t_coverage_match:
            t_coverage_content = t_coverage_match.group(0)
            self.rtm_t_references = set(re.findall(r'(T\d{3})', t_coverage_content))
        
        # Check SEC requirements coverage
        missing_sec = set(self.spec_parser.sec_requirements.keys()) - self.rtm_sec_requirements
        if missing_sec:
            for sec_id in sorted(missing_sec):
                self.errors.append(
                    f"SEC requirement not in RTM: {sec_id} "
                    f"({self.spec_parser.sec_requirements[sec_id][:50]}...)"
                )
        
        # Check T-references coverage
        missing_t = self.spec_parser.t_references - self.rtm_t_references
        if missing_t:
            if len(missing_t) > 10:
                self.warnings.append(
                    f"{len(missing_t)} T-references from spec.md not found in RTM: "
                    f"{', '.join(sorted(list(missing_t))[:10])}..."
                )
            else:
                for t_id in sorted(missing_t):
                    self.warnings.append(f"T-reference not in RTM: {t_id}")


def main():
    parser = argparse.ArgumentParser(
        description='Validate SmartSpec tasks.md with optional spec.md traceability checks'
    )
    parser.add_argument(
        '--tasks',
        required=True,
        help='Path to tasks.md file'
    )
    parser.add_argument(
        '--spec',
        help='Path to spec.md file (optional, enables traceability validation)'
    )
    
    args = parser.parse_args()
    
    # Parse spec.md if provided
    spec_parser = None
    if args.spec:
        spec_parser = SpecParser(Path(args.spec))
        if not spec_parser.parse():
            print(f"Error: Could not parse spec file: {args.spec}", file=sys.stderr)
            sys.exit(2)
    
    # Validate tasks.md
    validator = TasksValidator(args.tasks, spec_parser)
    is_valid, errors, warnings = validator.validate()
    
    # Print results
    print(f"\n{'='*60}")
    print(f"SmartSpec Tasks Validation Report")
    print(f"{'='*60}")
    print(f"Tasks File: {args.tasks}")
    if args.spec:
        print(f"Spec File: {args.spec}")
    print()
    
    if spec_parser:
        print(f"📊 Spec Analysis:")
        print(f"  - SEC Requirements: {len(spec_parser.sec_requirements)}")
        print(f"  - T-References: {len(spec_parser.t_references)}")
        print()
        
        print(f"📊 Tasks Analysis:")
        print(f"  - Total Tasks: {len(validator.task_ids)}")
        print(f"  - SEC in RTM: {len(validator.rtm_sec_requirements)}")
        print(f"  - T-Refs in RTM: {len(validator.rtm_t_references)}")
        print()
    
    if errors:
        print(f"❌ ERRORS ({len(errors)}):")
        for error in errors:
            print(f"  - {error}")
        print()
    
    if warnings:
        print(f"⚠️  WARNINGS ({len(warnings)}):")
        for warning in warnings:
            print(f"  - {warning}")
        print()
    
    if is_valid:
        print("✅ Tasks file is VALID and complete!")
        print(f"{'='*60}\n")
        sys.exit(0)
    else:
        print("❌ Tasks file is INVALID - please fix errors above")
        print(f"{'='*60}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
