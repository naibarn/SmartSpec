"""
Orchestrator Agent - Main development loop coordinator.

This agent knows all 59 workflows and coordinates the entire
development lifecycle.
"""

from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

from .workflow_loader import WorkflowCatalog, Workflow
from .tasks_parser import parse_tasks_file
from .router_enhanced import decide_next, get_step_recommendation
from .security import (
    sanitize_spec_id,
    sanitize_workflow_name,
    sanitize_platform,
    validate_workflow_params,
    InvalidInputError,
    PathTraversalError
)


@dataclass
class WorkflowRecommendation:
    """Recommendation for next workflow"""
    workflow: Workflow
    reason: str
    priority: str  # "critical", "high", "normal", "low"
    estimated_time: str
    command: str
    warnings: List[str]
    tips: List[str]


class OrchestratorAgent:
    """
    Orchestrator Agent - Coordinates development lifecycle.
    
    Capabilities:
    - Know all 59 workflows
    - Understand development loop
    - Determine current state
    - Select appropriate workflow
    - Handle workflow sequence
    """
    
    def __init__(self, workflows_dir: str = "/home/ubuntu/SmartSpec/.smartspec/workflows"):
        self.catalog = WorkflowCatalog(workflows_dir)
        self.state_dir = Path(".spec/state")
        self.state_dir.mkdir(parents=True, exist_ok=True)
    
    def read_state(self, spec_id: str) -> Dict[str, Any]:
        """
        Read current state for a spec.
        
        Args:
            spec_id: Spec ID (will be sanitized)
            
        Raises:
            InvalidInputError: If spec_id is invalid
        """
        # Sanitize input
        spec_id = sanitize_spec_id(spec_id)
        
        Returns:
            State dict with all relevant information
        """
        state = {
            "spec_id": spec_id,
            "has_spec": False,
            "has_plan": False,
            "has_tasks": False,
            "implementation_status": "NOT_STARTED",
            "tasks_total": 0,
            "tasks_completed": 0,
            "tasks_completion_rate": 0.0,
            "needs_sync": False,
            "has_tests": False,
            "tests_passed": False,
            "quality_gate_passed": False,
            "has_docs": False,
            "errors": [],
            "warnings": []
        }
        
        # Check if spec exists
        spec_file = Path("specs") / spec_id / "spec.md"
        state["has_spec"] = spec_file.exists()
        
        # Check if plan exists
        plan_file = Path("specs") / spec_id / "plan.md"
        state["has_plan"] = plan_file.exists()
        
        # Check if tasks exists
        tasks_file = Path("specs") / spec_id / "tasks.md"
        state["has_tasks"] = tasks_file.exists()
        
        # Parse tasks.md to get progress
        if state["has_tasks"]:
            tasks_info = parse_tasks_file(tasks_file)
            state["tasks_total"] = tasks_info["total"]
            state["tasks_completed"] = tasks_info["completed"]
            state["tasks_completion_rate"] = tasks_info["completion_rate"]
            
            # Determine implementation status
            if tasks_info["completed"] == 0:
                state["implementation_status"] = "NOT_STARTED"
            elif tasks_info["completed"] < tasks_info["total"]:
                state["implementation_status"] = "IN_PROGRESS"
            else:
                state["implementation_status"] = "COMPLETED"
        
        # Check implementation report
        implement_report = Path(".spec/reports/implement-tasks") / spec_id / "summary.json"
        if implement_report.exists():
            # Check timestamp to determine if needs sync
            import json
            try:
                with open(implement_report) as f:
                    report_data = json.load(f)
                    # If report exists but completion rate < 100%, might need sync
                    if state["tasks_completion_rate"] < 1.0:
                        state["needs_sync"] = True
            except:
                pass
        
        # Check tests
        tests_dir = Path("specs") / spec_id / "tests"
        state["has_tests"] = tests_dir.exists() and any(tests_dir.glob("*.test.*"))
        
        # Check test results
        test_report = Path(".spec/reports/test-suite") / spec_id / "results.json"
        if test_report.exists():
            import json
            try:
                with open(test_report) as f:
                    test_data = json.load(f)
                    state["tests_passed"] = test_data.get("passed", False)
            except:
                pass
        
        # Check quality gate
        quality_report = Path(".spec/reports/quality-gate") / spec_id / "report.json"
        if quality_report.exists():
            import json
            try:
                with open(quality_report) as f:
                    quality_data = json.load(f)
                    state["quality_gate_passed"] = quality_data.get("passed", False)
            except:
                pass
        
        # Check docs
        docs_file = Path("specs") / spec_id / "README.md"
        state["has_docs"] = docs_file.exists()
        
        return state
    
    def recommend_next_workflow(self, spec_id: str) -> Optional[WorkflowRecommendation]:
        """
        Recommend next workflow based on current state.
        
        Returns:
            WorkflowRecommendation or None if all done
        """
        # Read current state
        state = self.read_state(spec_id)
        
        # Use catalog's recommend_workflow (basic)
        workflow = self.catalog.recommend_workflow(state)
        
        if workflow is None:
            return None
        
        # Get enhanced recommendation from router
        router_recommendation = get_step_recommendation(state)
        
        # Build command
        command = self._build_command(workflow, spec_id, state)
        
        # Build recommendation
        recommendation = WorkflowRecommendation(
            workflow=workflow,
            reason=router_recommendation.get("reason", "Next step in development loop"),
            priority=router_recommendation.get("priority", "normal"),
            estimated_time=router_recommendation.get("estimated_time", "Unknown"),
            command=command,
            warnings=router_recommendation.get("warnings", []),
            tips=router_recommendation.get("tips", [])
        )
        
        return recommendation
    
      def _build_command(self, workflow: Workflow, spec_id: str, state: Dict) -> str:
        """Build command string for workflow"""
        from .security import quote_for_shell
        
        # Sanitize spec_id (already sanitized in recommend_workflow, but double-check)
        spec_id = sanitize_spec_id(spec_id)"
        # Base command
        cmd = f"/{workflow.name}.md"
        
        # Add spec-specific arguments
        # Use quote_for_shell to prevent command injection
        safe_spec_id = quote_for_shell(spec_id)
        
        if workflow.name == "smartspec_generate_spec":
            cmd += f" \\\n  --spec-id {safe_spec_id}"
        
        elif workflow.name == "smartspec_generate_plan":
            cmd += f" \\\n  specs/{safe_spec_id}/spec.md"
        
        elif workflow.name == "smartspec_generate_tasks":
            cmd += f" \\\n  specs/{safe_spec_id}/plan.md"
        
        elif workflow.name == "smartspec_implement_tasks":
            cmd += f" \\\n  specs/{safe_spec_id}/tasks.md"
            cmd += f" \\\n  --apply"
            cmd += f" \\\n  --out .spec/reports/implement-tasks/{safe_spec_id}"
        
        elif workflow.name == "smartspec_sync_tasks_checkboxes":
            cmd += f" \\\n  specs/{safe_spec_id}/tasks.md"
            cmd += f" \\\n  --apply"
            cmd += f" \\\n  --out .spec/reports/sync-tasks/{safe_spec_id}"
        
        elif workflow.name == "smartspec_generate_tests":
            cmd += f" \\\n  specs/{safe_spec_id}/spec.md"
            cmd += f" \\\n  --out specs/{safe_spec_id}/tests"
        
        elif workflow.name == "smartspec_test_suite_runner":
            cmd += f" \\\n  specs/{safe_spec_id}/tests"
            cmd += f" \\\n  --out .spec/reports/test-suite/{safe_spec_id}"
        
        elif workflow.name == "smartspec_quality_gate":
            cmd += f" \\\n  --spec-id {safe_spec_id}"
            cmd += f" \\\n  --out .spec/reports/quality-gate/{safe_spec_id}"
        
        elif workflow.name == "smartspec_docs_generator":
            cmd += f" \\\n  specs/{safe_spec_id}"
            cmd += f" \\\n  --out specs/{safe_spec_id}/README.md"
        
        # Add common flags
        cmd += f" \\\n  --json"
        cmd += f" \\\n  --platform kilo"
        
        return cmd
    
    def get_workflow_by_name(self, name: str) -> Optional[Workflow]:
        """Get workflow by name"""
        return self.catalog.get(name)
    
    def search_workflows(self, query: str) -> List[Workflow]:
        """Search workflows"""
        return self.catalog.search(query)
    
    def get_core_loop(self) -> List[Workflow]:
        """Get core development loop workflows"""
        return self.catalog.get_core_development_loop()
    
    def summary(self) -> str:
        """Get agent summary"""
        return f"""Orchestrator Agent Summary
{'=' * 50}
Workflows loaded: {len(self.catalog.workflows)}
Categories: {len(self.catalog.list_categories())}

Capabilities:
- Know all 59 workflows
- Understand development loop
- Recommend next workflow
- Build workflow commands
- Track state

Status: Ready
"""


# Example usage
if __name__ == "__main__":
    # Create agent
    agent = OrchestratorAgent()
    
    # Print summary
    print(agent.summary())
    print()
    
    # Test with example spec
    spec_id = "spec-core-001-authentication"
    
    print(f"Analyzing spec: {spec_id}")
    print("-" * 50)
    
    # Read state
    state = agent.read_state(spec_id)
    print(f"State:")
    print(f"  has_spec: {state['has_spec']}")
    print(f"  has_plan: {state['has_plan']}")
    print(f"  has_tasks: {state['has_tasks']}")
    print(f"  implementation_status: {state['implementation_status']}")
    print(f"  tasks_completed: {state['tasks_completed']} / {state['tasks_total']}")
    print(f"  completion_rate: {state['tasks_completion_rate']:.0%}")
    print()
    
    # Get recommendation
    recommendation = agent.recommend_next_workflow(spec_id)
    
    if recommendation:
        print(f"Recommendation:")
        print(f"  Workflow: {recommendation.workflow.name}")
        print(f"  Reason: {recommendation.reason}")
        print(f"  Priority: {recommendation.priority}")
        print(f"  Estimated Time: {recommendation.estimated_time}")
        print()
        print(f"Command:")
        print(recommendation.command)
    else:
        print("All done! No more workflows needed.")
