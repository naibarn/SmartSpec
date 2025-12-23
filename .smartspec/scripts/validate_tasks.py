#!/usr/bin/env python3
"""
SmartSpec Tasks Validation Script

Validates that tasks.md contains all required sections, proper task format,
and evidence-first elements.

Usage:
    python3 validate_tasks.py <path_to_tasks.md>

Exit codes:
    0 - Tasks file is complete and valid
    1 - Tasks file is missing required sections or has errors
    2 - Invalid arguments or file not found
"""

import sys
import re
from pathlib import Path
from typing import List, Tuple, Set


class TasksValidator:
    """Validates SmartSpec tasks.md files for completeness and evidence-first compliance."""
    
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
    
    def __init__(self, tasks_path: str):
        self.tasks_path = Path(tasks_path)
        self.content = ""
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.task_ids: Set[str] = set()
        
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
        
        is_valid = len(self.errors) == 0
        return is_valid, self.errors, self.warnings
    
    def _validate_header(self):
        """Check that header table with required fields is present."""
        # Look for markdown table header
        header_pattern = r'\|\s*spec-id\s*\|\s*source\s*\|\s*generated_by\s*\|\s*updated_at\s*\|'
        if not re.search(header_pattern, self.content, re.IGNORECASE):
            self.errors.append("Missing required header table with fields: spec-id, source, generated_by, updated_at")
            return
        
        # Check if there's a data row after the header
        header_match = re.search(header_pattern, self.content, re.IGNORECASE)
        if header_match:
            # Look for the next line (should be separator) and then data row
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
            return  # Already flagged in _validate_required_sections
        
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
            return  # Already flagged in _validate_required_sections
        
        tasks_content = tasks_match.group(0)
        
        # Find all task items (lines starting with checkbox)
        task_items = re.findall(
            r'^-\s+\[([ x])\]\s+\*\*([^*]+)\*\*.*?(?=^-\s+\[|\Z)',
            tasks_content,
            re.MULTILINE | re.DOTALL
        )
        
        if not task_items:
            self.warnings.append("No task items found in Tasks section")
            return
        
        for checkbox_state, task_title in task_items:
            # Extract task ID from title
            task_id_match = re.search(r'(TSK-[A-Z0-9]+-\d+)', task_title)
            if not task_id_match:
                self.errors.append(f"Task '{task_title[:50]}...' missing valid Task ID (TSK-<spec-id>-NNN)")
                continue
            
            task_id = task_id_match.group(1)
            
            # Check for duplicate task IDs
            if task_id in self.task_ids:
                self.errors.append(f"Duplicate Task ID found: {task_id}")
            else:
                self.task_ids.add(task_id)
            
            # Find the full task content
            task_content_match = re.search(
                rf'^-\s+\[([ x])\]\s+\*\*{re.escape(task_title)}\*\*.*?(?=^-\s+\[|\Z)',
                tasks_content,
                re.MULTILINE | re.DOTALL
            )
            
            if task_content_match:
                task_content = task_content_match.group(0)
                
                # Check for Acceptance Criteria
                if not re.search(r'\*\*Acceptance\s+Criteria:\*\*', task_content, re.IGNORECASE):
                    self.warnings.append(f"{task_id}: Missing 'Acceptance Criteria' section")
                
                # Check for Evidence Hooks
                if not re.search(r'\*\*Evidence\s+Hooks?:\*\*', task_content, re.IGNORECASE):
                    self.errors.append(f"{task_id}: Missing 'Evidence Hooks' section")
                else:
                    # Check for at least one specific evidence type
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
            return  # Already flagged in _validate_required_sections
        
        evidence_content = evidence_match.group(0)
        
        # Find all task IDs in the evidence mapping table
        mapped_task_ids = set(re.findall(r'(TSK-[A-Z0-9]+-\d+)', evidence_content))
        
        # Check if all task IDs from Tasks section are in Evidence Mapping
        for task_id in self.task_ids:
            if task_id not in mapped_task_ids:
                self.warnings.append(f"{task_id}: Found in Tasks section but missing from Evidence Mapping table")
        
        # Check for task IDs in Evidence Mapping that don't exist in Tasks section
        for mapped_id in mapped_task_ids:
            if mapped_id not in self.task_ids:
                self.warnings.append(f"{mapped_id}: Found in Evidence Mapping but not in Tasks section")
    
    def _validate_tbd_consistency(self):
        """Check that tasks with TBD evidence are listed in Open Questions section."""
        # Find all tasks with TBD in evidence hooks
        tbd_tasks = set()
        tasks_match = re.search(
            r'^#{{1,3}}\s+Tasks.*?(?=^#{{1,3}}\s+|\Z)',
            self.content,
            re.MULTILINE | re.DOTALL | re.IGNORECASE
        )
        
        if tasks_match:
            tasks_content = tasks_match.group(0)
            # Find task IDs that have TBD in their content
            for task_id in self.task_ids:
                task_pattern = rf'{re.escape(task_id)}.*?(?=TSK-|^#{{1,3}}\s+|\Z)'
                task_match = re.search(task_pattern, tasks_content, re.DOTALL)
                if task_match and re.search(r'\bTBD\b', task_match.group(0), re.IGNORECASE):
                    tbd_tasks.add(task_id)
        
        # Check Open Questions section
        questions_match = re.search(
            r'^#{{1,3}}\s+Open\s+Questions.*?(?=^#{{1,3}}\s+|\Z)',
            self.content,
            re.MULTILINE | re.DOTALL | re.IGNORECASE
        )
        
        if questions_match:
            questions_content = questions_match.group(0)
            listed_tbd_tasks = set(re.findall(r'(TSK-[A-Z0-9]+-\d+)', questions_content))
            
            # Check if all TBD tasks are listed
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


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 validate_tasks.py <path_to_tasks.md>", file=sys.stderr)
        sys.exit(2)
    
    tasks_path = sys.argv[1]
    validator = TasksValidator(tasks_path)
    is_valid, errors, warnings = validator.validate()
    
    # Print results
    print(f"\n{'='*60}")
    print(f"SmartSpec Tasks Validation Report")
    print(f"{'='*60}")
    print(f"Tasks File: {tasks_path}\n")
    
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
