"""
Report enhancer for post-processing SmartSpec workflow reports.

This module adds Autopilot metadata to existing reports without modifying workflows.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any


class ReportEnhancer:
    """Post-process workflow reports to add Autopilot metadata"""
    
    # Workflow sequence and next steps
    WORKFLOW_SEQUENCE = {
        "smartspec_generate_spec": "smartspec_plan_implementation",
        "smartspec_plan_implementation": "smartspec_create_tasks",
        "smartspec_create_tasks": "smartspec_implement_tasks",
        "smartspec_implement_tasks": "smartspec_sync_tasks_checkboxes",
        "smartspec_sync_tasks_checkboxes": "smartspec_verify_implementation",
        "smartspec_verify_implementation": "smartspec_sync_spec",
        "smartspec_sync_spec": None,  # Complete
    }
    
    # Time estimates for each workflow
    TIME_ESTIMATES = {
        "smartspec_generate_spec": "5-10 minutes",
        "smartspec_plan_implementation": "5-10 minutes",
        "smartspec_create_tasks": "3-5 minutes",
        "smartspec_implement_tasks": "10-30 minutes",
        "smartspec_sync_tasks_checkboxes": "1-2 minutes",
        "smartspec_verify_implementation": "5-15 minutes",
        "smartspec_sync_spec": "2-3 minutes",
    }
    
    def __init__(self, reports_dir: str):
        self.reports_dir = Path(reports_dir)
    
    def enhance_report(self, workflow: str, spec_id: str) -> Dict[str, Any]:
        """
        Enhance a workflow report with Autopilot metadata.
        
        Args:
            workflow: Workflow name (e.g., "implement-tasks")
            spec_id: Spec ID (e.g., "spec-core-001-authentication")
            
        Returns:
            Enhanced summary dict (or None if report doesn't exist)
        """
        # Find report directory
        report_dir = self.reports_dir / workflow / spec_id
        summary_file = report_dir / "summary.json"
        
        if not summary_file.exists():
            return None
        
        # Read existing summary
        with open(summary_file) as f:
            summary = json.load(f)
        
        # If already has _autopilot metadata, return as-is
        if "_autopilot" in summary:
            return summary
        
        # Infer metadata
        metadata = self._infer_metadata(workflow, spec_id, summary, report_dir)
        
        # Add metadata
        summary["_autopilot"] = metadata
        
        # Write back
        with open(summary_file, "w") as f:
            json.dump(summary, f, indent=2)
        
        return summary
    
    def _infer_metadata(
        self,
        workflow: str,
        spec_id: str,
        summary: Dict[str, Any],
        report_dir: Path
    ) -> Dict[str, Any]:
        """Infer Autopilot metadata from report"""
        
        # Get workflow name (convert from directory name to workflow name)
        workflow_name = self._get_workflow_name(workflow)
        
        # Determine next workflow
        next_workflow = self.WORKFLOW_SEQUENCE.get(workflow_name)
        
        # Base metadata
        metadata = {
            "next_recommended_workflow": next_workflow,
            "quality_score": self._calculate_quality_score(summary, report_dir),
            "validation_passed": summary.get("status") == "success",
            "warnings": [],
            "estimated_time_next_step": self.TIME_ESTIMATES.get(next_workflow, "5-10 minutes") if next_workflow else "N/A"
        }
        
        # Add workflow-specific metadata
        if workflow == "implement-tasks":
            metadata.update(self._infer_implement_metadata(report_dir))
        elif workflow == "create-tasks":
            metadata.update(self._infer_tasks_metadata(report_dir))
        elif workflow == "sync-tasks":
            metadata.update(self._infer_sync_metadata(report_dir))
        
        return metadata
    
    def _get_workflow_name(self, workflow_dir: str) -> str:
        """Convert workflow directory name to workflow name"""
        mapping = {
            "generate-spec": "smartspec_generate_spec",
            "generate-plan": "smartspec_plan_implementation",
            "create-tasks": "smartspec_create_tasks",
            "implement-tasks": "smartspec_implement_tasks",
            "sync-tasks": "smartspec_sync_tasks_checkboxes",
            "verify-implementation": "smartspec_verify_implementation",
            "sync-spec": "smartspec_sync_spec",
        }
        return mapping.get(workflow_dir, f"smartspec_{workflow_dir.replace('-', '_')}")
    
    def _calculate_quality_score(self, summary: Dict[str, Any], report_dir: Path) -> float:
        """Calculate quality score based on report contents"""
        score = 0.5  # Base score
        
        # Success adds to score
        if summary.get("status") == "success":
            score += 0.3
        
        # Presence of detailed reports adds to score
        if (report_dir / "change_plan.md").exists():
            score += 0.1
        if (report_dir / "details.md").exists():
            score += 0.1
        
        return min(score, 1.0)
    
    def _infer_implement_metadata(self, report_dir: Path) -> Dict[str, Any]:
        """Infer metadata specific to implement-tasks workflow"""
        metadata = {}
        
        # Try to find files created/modified
        change_plan = report_dir / "change_plan.md"
        if change_plan.exists():
            # Parse change_plan.md to find files
            # (Simplified - in production, parse properly)
            metadata["files_created"] = []
            metadata["files_modified"] = []
        
        return metadata
    
    def _infer_tasks_metadata(self, report_dir: Path) -> Dict[str, Any]:
        """Infer metadata specific to create-tasks workflow"""
        metadata = {}
        
        # Try to count tasks
        # (Simplified - in production, parse tasks.md)
        metadata["task_count"] = 0
        
        return metadata
    
    def _infer_sync_metadata(self, report_dir: Path) -> Dict[str, Any]:
        """Infer metadata specific to sync-tasks workflow"""
        metadata = {}
        
        # Try to count completed tasks
        # (Simplified - in production, parse tasks.md)
        metadata["tasks_completed"] = 0
        metadata["tasks_total"] = 0
        
        return metadata
    
    def get_latest_report_metadata(self, spec_id: str) -> Dict[str, Any]:
        """
        Get metadata from the most recent workflow report for a spec.
        
        Args:
            spec_id: Spec ID
            
        Returns:
            Dict with metadata from latest report
        """
        # Check each workflow in reverse order
        workflows = list(self.WORKFLOW_SEQUENCE.keys())
        workflows.reverse()
        
        for workflow_name in workflows:
            workflow_dir = workflow_name.replace("smartspec_", "").replace("_", "-")
            report_dir = self.reports_dir / workflow_dir / spec_id
            summary_file = report_dir / "summary.json"
            
            if summary_file.exists():
                with open(summary_file) as f:
                    summary = json.load(f)
                    if "_autopilot" in summary:
                        return summary["_autopilot"]
        
        return {}
