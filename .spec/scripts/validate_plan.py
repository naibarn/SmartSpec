#!/usr/bin/env python3
"""
SmartSpec Plan Validation Script

Validates that plan.md contains all required sections and evidence-first elements.

Usage:
    python3 validate_plan.py <path_to_plan.md>

Exit codes:
    0 - Plan is complete and valid
    1 - Plan is missing required sections or evidence
    2 - Invalid arguments or file not found
"""

import sys
import re
from pathlib import Path
from typing import List, Tuple


class PlanValidator:
    """Validates SmartSpec plan.md files for completeness and governance compliance."""
    
    REQUIRED_METADATA = [
        "spec-id",
        "workflow",
        "workflow_version",
        "ui_mode",
        "safety_mode",
        "safety_status",
        "generated_at"
    ]
    
    REQUIRED_GOVERNANCE_SECTIONS = [
        "Assumptions & Prerequisites",
        "Out of Scope",
        "Definition of Done"
    ]
    
    REQUIRED_DEPLOYMENT_SECTIONS = [
        "Rollout & Release Plan",
        "Rollback & Recovery Plan",
        "Data Retention & Privacy Operations"
    ]
    
    REQUIRED_PHASES = [
        "Phase 0",
        "Phase 1",
        "Phase 2",
        "Phase 3",
        "Phase 4",
        "Phase 5"
    ]
    
    REQUIRED_PHASE_ELEMENTS = [
        "objectives",
        "prerequisites",
        "deliverables",
        "risks",
        "acceptance criteria"
    ]
    
    def __init__(self, plan_path: str):
        self.plan_path = Path(plan_path)
        self.content = ""
        self.errors: List[str] = []
        self.warnings: List[str] = []
        
    def validate(self) -> Tuple[bool, List[str], List[str]]:
        """
        Validate the plan.md file.
        
        Returns:
            Tuple of (is_valid, errors, warnings)
        """
        if not self.plan_path.exists():
            self.errors.append(f"Plan file not found: {self.plan_path}")
            return False, self.errors, self.warnings
        
        self.content = self.plan_path.read_text(encoding='utf-8')
        
        # Run all validation checks
        self._validate_metadata()
        self._validate_governance_sections()
        self._validate_deployment_sections()
        self._validate_phases()
        self._validate_evidence_artifacts()
        self._validate_data_retention_specifics()
        self._validate_readiness_checklist()
        
        is_valid = len(self.errors) == 0
        return is_valid, self.errors, self.warnings
    
    def _validate_metadata(self):
        """Check that all required metadata fields are present."""
        for field in self.REQUIRED_METADATA:
            # Check for both YAML frontmatter and table format
            pattern = rf'({field}:|{field}\s*\|)'
            if not re.search(pattern, self.content, re.IGNORECASE):
                self.errors.append(f"Missing required metadata field: {field}")
    
    def _validate_governance_sections(self):
        """Check that all required governance sections are present."""
        for section in self.REQUIRED_GOVERNANCE_SECTIONS:
            # Check for markdown headers (## or ###)
            pattern = rf'^#{2,3}\s+{re.escape(section)}'
            if not re.search(pattern, self.content, re.MULTILINE | re.IGNORECASE):
                self.errors.append(f"Missing required governance section: {section}")
    
    def _validate_deployment_sections(self):
        """Check that all required deployment/operations sections are present."""
        for section in self.REQUIRED_DEPLOYMENT_SECTIONS:
            pattern = rf'^#{2,3}\s+{re.escape(section)}'
            if not re.search(pattern, self.content, re.MULTILINE | re.IGNORECASE):
                self.errors.append(f"Missing required deployment section: {section}")
    
    def _validate_phases(self):
        """Check that required phases are present and have necessary elements."""
        for phase in self.REQUIRED_PHASES:
            pattern = rf'^#{2,3}\s+{re.escape(phase)}'
            if not re.search(pattern, self.content, re.MULTILINE | re.IGNORECASE):
                self.warnings.append(f"Missing recommended phase: {phase}")
                continue
            
            # Extract phase content
            phase_match = re.search(
                rf'^#{2,3}\s+{re.escape(phase)}.*?(?=^#{2,3}\s+|\Z)',
                self.content,
                re.MULTILINE | re.DOTALL | re.IGNORECASE
            )
            
            if phase_match:
                phase_content = phase_match.group(0)
                
                # Check for required phase elements
                for element in self.REQUIRED_PHASE_ELEMENTS:
                    if not re.search(rf'\*\*{re.escape(element)}\*\*', phase_content, re.IGNORECASE):
                        self.warnings.append(f"{phase}: Missing recommended element '{element}'")
    
    def _validate_evidence_artifacts(self):
        """Check that completed phases have evidence artifacts."""
        # Find all phases marked as complete
        complete_phases = re.findall(
            r'^#{2,3}\s+(Phase \d+).*?Status:\s*(Complete|Completed)',
            self.content,
            re.MULTILINE | re.IGNORECASE
        )
        
        for phase_name, _ in complete_phases:
            # Check if this phase has evidence section
            phase_match = re.search(
                rf'^#{2,3}\s+{re.escape(phase_name)}.*?(?=^#{2,3}\s+|\Z)',
                self.content,
                re.MULTILINE | re.DOTALL | re.IGNORECASE
            )
            
            if phase_match:
                phase_content = phase_match.group(0)
                
                # Check for evidence section
                if not re.search(r'Evidence\s+(&|and)\s+Verification\s+Artifacts', phase_content, re.IGNORECASE):
                    self.errors.append(f"{phase_name}: Marked as complete but missing Evidence & Verification Artifacts")
                else:
                    # Check for specific evidence elements
                    if not re.search(r'Report\s+[Pp]ath', phase_content):
                        self.warnings.append(f"{phase_name}: Evidence section missing report path")
                    if not re.search(r'Run\s+ID', phase_content):
                        self.warnings.append(f"{phase_name}: Evidence section missing run_id")
    
    def _validate_data_retention_specifics(self):
        """Check that data retention section has specific policies per entity."""
        # Find data retention section
        retention_match = re.search(
            r'^#{2,3}\s+Data Retention & Privacy Operations.*?(?=^#{2,3}\s+|\Z)',
            self.content,
            re.MULTILINE | re.DOTALL | re.IGNORECASE
        )
        
        if retention_match:
            retention_content = retention_match.group(0)
            
            # Check for specific retention policies (e.g., "Session: 7 days")
            entity_policy_pattern = r'\w+:\s+\d+\s+(days?|months?|years?)'
            if not re.search(entity_policy_pattern, retention_content):
                self.warnings.append("Data Retention section should include specific policies per entity (e.g., 'Session: 7 days')")
            
            # Check for GDPR-related content
            if not re.search(r'GDPR', retention_content, re.IGNORECASE):
                self.warnings.append("Data Retention section should mention GDPR compliance")
    
    def _validate_readiness_checklist(self):
        """Check that plan includes readiness verification checklist."""
        if not re.search(r'Readiness\s+Verification\s+Checklist', self.content, re.IGNORECASE):
            self.errors.append("Missing required Readiness Verification Checklist")
        else:
            # Check for specific checklist items
            required_items = [
                "assumptions documented",
                "out-of-scope",
                "rollout plan",
                "data retention",
                "evidence artifacts",
                "security scan",
                "test coverage",
                "GDPR"
            ]
            
            for item in required_items:
                if not re.search(rf'\[\s*[x ]?\s*\].*{re.escape(item)}', self.content, re.IGNORECASE):
                    self.warnings.append(f"Readiness checklist missing item: {item}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 validate_plan.py <path_to_plan.md>", file=sys.stderr)
        sys.exit(2)
    
    plan_path = sys.argv[1]
    validator = PlanValidator(plan_path)
    is_valid, errors, warnings = validator.validate()
    
    # Print results
    print(f"\n{'='*60}")
    print(f"SmartSpec Plan Validation Report")
    print(f"{'='*60}")
    print(f"Plan: {plan_path}\n")
    
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
        print("✅ Plan is VALID and complete!")
        print(f"{'='*60}\n")
        sys.exit(0)
    else:
        print("❌ Plan is INVALID - please fix errors above")
        print(f"{'='*60}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
