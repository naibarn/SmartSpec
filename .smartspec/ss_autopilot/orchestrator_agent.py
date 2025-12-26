"""
Orchestrator Agent - Main development loop coordinator.

This agent knows all 63 workflows and coordinates the entire
development lifecycle.
"""

from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import json

from .workflow_loader import WorkflowCatalog, Workflow
from .tasks_parser import parse_tasks_file
from .router_enhanced import decide_next, get_step_recommendation
from .security import (
    sanitize_spec_id,
    sanitize_workflow_name,
    sanitize_platform,
    validate_workflow_params,
    InvalidInputError,
    PathTraversalError,
    quote_for_shell
)
from .error_handler import (
    safe_file_read,
    safe_file_write,
    with_error_handling,
    FileNotFoundError,
    SpecNotFoundError,
    WorkflowNotFoundError,
    get_user_friendly_error
)
from .advanced_logger import get_logger


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
    - Know all 63 workflows
    - Understand development loop
    - Determine current state
    - Select appropriate workflow
    - Handle workflow sequence
    """
    
    def __init__(self, workflows_dir: str = "/home/ubuntu/SmartSpec/.smartspec/workflows"):
        """
        Initialize Orchestrator Agent.
        
        Args:
            workflows_dir: Path to workflows directory
        """
        try:
            self.logger = get_logger("orchestrator_agent")
            self.catalog = WorkflowCatalog(workflows_dir)
            self.state_dir = Path(".spec/state")
            self.state_dir.mkdir(parents=True, exist_ok=True)
            self.logger.info("OrchestratorAgent initialized", workflows_dir=workflows_dir)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize OrchestratorAgent: {str(e)}")
    
    @with_error_handling
    def read_state(self, spec_id: str) -> Dict[str, Any]:
        """
        Read current state for a spec with comprehensive error handling.
        
        Args:
            spec_id: Spec ID (will be sanitized)
            
        Returns:
            State dict with all relevant information or error dict
            
        Raises:
            InvalidInputError: If spec_id is invalid
        """
        # Log operation start
        self.logger.info("Reading state", spec_id=spec_id)
        
        # Sanitize input
        try:
            spec_id = sanitize_spec_id(spec_id)
        except Exception as e:
            raise InvalidInputError(
                input_name="spec_id",
                input_value=spec_id,
                reason=str(e)
            )
        
        # Initialize state
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
        
        try:
            # Check if spec exists
            spec_file = Path("specs") / spec_id / "spec.md"
            state["has_spec"] = spec_file.exists()
            
            if not state["has_spec"]:
                state["warnings"].append(f"Spec file not found: {spec_file}")
            
            # Check if plan exists
            plan_file = Path("specs") / spec_id / "plan.md"
            state["has_plan"] = plan_file.exists()
            
            # Check if tasks exists
            tasks_file = Path("specs") / spec_id / "tasks.md"
            state["has_tasks"] = tasks_file.exists()
            
            # Parse tasks.md to get progress
            if state["has_tasks"]:
                try:
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
                except Exception as e:
                    state["errors"].append(f"Failed to parse tasks file: {str(e)}")
                    state["warnings"].append("Tasks file exists but could not be parsed")
            
            # Check implementation report
            implement_report = Path(".spec/reports/implement-tasks") / spec_id / "summary.json"
            if implement_report.exists():
                try:
                    result = safe_file_read(str(implement_report))
                    if result.get("success"):
                        report_data = json.loads(result["content"])
                        # If report exists but completion rate < 100%, might need sync
                        if state["tasks_completion_rate"] < 1.0:
                            state["needs_sync"] = True
                    else:
                        state["warnings"].append(f"Could not read implementation report: {result.get('message')}")
                except json.JSONDecodeError as e:
                    state["errors"].append(f"Invalid JSON in implementation report: {str(e)}")
                except Exception as e:
                    state["errors"].append(f"Error reading implementation report: {str(e)}")
            
            # Check tests
            tests_dir = Path("specs") / spec_id / "tests"
            try:
                state["has_tests"] = tests_dir.exists() and any(tests_dir.glob("*.test.*"))
            except Exception as e:
                state["errors"].append(f"Error checking tests directory: {str(e)}")
                state["has_tests"] = False
            
            # Check test results
            test_report = Path(".spec/reports/test-suite") / spec_id / "results.json"
            if test_report.exists():
                try:
                    result = safe_file_read(str(test_report))
                    if result.get("success"):
                        test_data = json.loads(result["content"])
                        state["tests_passed"] = test_data.get("passed", False)
                    else:
                        state["warnings"].append(f"Could not read test report: {result.get('message')}")
                except json.JSONDecodeError as e:
                    state["errors"].append(f"Invalid JSON in test report: {str(e)}")
                except Exception as e:
                    state["errors"].append(f"Error reading test report: {str(e)}")
            
            # Check quality gate
            quality_report = Path(".spec/reports/quality-gate") / spec_id / "report.json"
            if quality_report.exists():
                try:
                    result = safe_file_read(str(quality_report))
                    if result.get("success"):
                        quality_data = json.loads(result["content"])
                        state["quality_gate_passed"] = quality_data.get("passed", False)
                    else:
                        state["warnings"].append(f"Could not read quality report: {result.get('message')}")
                except json.JSONDecodeError as e:
                    state["errors"].append(f"Invalid JSON in quality report: {str(e)}")
                except Exception as e:
                    state["errors"].append(f"Error reading quality report: {str(e)}")
            
            # Check docs
            docs_file = Path("specs") / spec_id / "README.md"
            state["has_docs"] = docs_file.exists()
            
            return state
            
        except Exception as e:
            # Catch any unexpected errors
            state["errors"].append(f"Unexpected error reading state: {str(e)}")
            return state
    
    @with_error_handling
    def recommend_next_workflow(self, spec_id: str) -> Optional[WorkflowRecommendation]:
        """
        Recommend next workflow based on current state with error handling.
        
        Args:
            spec_id: Spec ID
            
        Returns:
            WorkflowRecommendation or None if all done, or error dict
        """
        try:
            # Read current state
            state_result = self.read_state(spec_id)
            
            # Check if read_state returned an error
            if isinstance(state_result, dict) and state_result.get("error"):
                return None
            
            # Extract state from result
            if isinstance(state_result, dict) and state_result.get("success"):
                state = state_result["result"]
            else:
                state = state_result
            
            # Use catalog's recommend_workflow (basic)
            try:
                workflow = self.catalog.recommend_workflow(state)
            except Exception as e:
                raise WorkflowNotFoundError(
                    workflow_name="<recommendation>",
                    available_workflows=[w.name for w in self.catalog.workflows[:5]]
                )
            
            if workflow is None:
                return None
            
            # Get enhanced recommendation from router
            try:
                router_recommendation = get_step_recommendation(state)
            except Exception as e:
                # Fallback to basic recommendation
                router_recommendation = {
                    "reason": "Next step in development loop",
                    "priority": "normal",
                    "estimated_time": "Unknown",
                    "warnings": [f"Could not get enhanced recommendation: {str(e)}"],
                    "tips": []
                }
            
            # Build command
            try:
                command = self._build_command(workflow, spec_id, state)
            except Exception as e:
                raise RuntimeError(f"Failed to build command: {str(e)}")
            
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
            
        except Exception as e:
            # Re-raise as AutopilotError for consistent error handling
            raise RuntimeError(f"Failed to recommend workflow: {str(e)}")
    
    def _build_command(self, workflow: Workflow, spec_id: str, state: Dict) -> str:
        """
        Build command string for workflow with proper escaping.
        
        Args:
            workflow: Workflow object
            spec_id: Spec ID (will be sanitized)
            state: Current state dict
            
        Returns:
            Command string with properly escaped arguments
        """
        try:
            # Sanitize spec_id (already sanitized in recommend_workflow, but double-check)
            spec_id = sanitize_spec_id(spec_id)
            
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
            
        except Exception as e:
            raise RuntimeError(f"Failed to build command: {str(e)}")
    
    @with_error_handling
    def get_workflow_by_name(self, name: str) -> Optional[Workflow]:
        """
        Get workflow by name with error handling.
        
        Args:
            name: Workflow name
            
        Returns:
            Workflow object or None if not found
        """
        try:
            # Sanitize workflow name
            name = sanitize_workflow_name(name)
            return self.catalog.get(name)
        except Exception as e:
            raise WorkflowNotFoundError(
                workflow_name=name,
                available_workflows=[w.name for w in self.catalog.workflows[:5]]
            )
    
    @with_error_handling
    def search_workflows(self, query: str) -> List[Workflow]:
        """
        Search workflows with error handling.
        
        Args:
            query: Search query
            
        Returns:
            List of matching workflows
        """
        try:
            return self.catalog.search(query)
        except Exception as e:
            # Return empty list on error
            return []
    
    def get_core_loop(self) -> List[Workflow]:
        """Get core development loop workflows"""
        try:
            return self.catalog.get_core_development_loop()
        except Exception as e:
            # Return empty list on error
            return []
    
    def summary(self) -> str:
        """Get agent summary"""
        try:
            workflow_count = len(self.catalog.workflows)
            category_count = len(self.catalog.list_categories())
        except Exception:
            workflow_count = 0
            category_count = 0
        
        return f"""Orchestrator Agent Summary
{'=' * 50}
Workflows loaded: {workflow_count}
Categories: {category_count}

Capabilities:
- Know all 63 workflows
- Understand development loop
- Recommend next workflow
- Build workflow commands
- Track state

Status: Ready
"""


# Example usage
if __name__ == "__main__":
    try:
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
        state_result = agent.read_state(spec_id)
        
        # Check for errors
        if isinstance(state_result, dict) and state_result.get("error"):
            print(f"Error: {get_user_friendly_error(state_result)}")
        else:
            # Extract state
            if isinstance(state_result, dict) and state_result.get("success"):
                state = state_result["result"]
            else:
                state = state_result
            
            print(f"State:")
            print(f"  has_spec: {state['has_spec']}")
            print(f"  has_plan: {state['has_plan']}")
            print(f"  has_tasks: {state['has_tasks']}")
            print(f"  implementation_status: {state['implementation_status']}")
            print(f"  tasks_completed: {state['tasks_completed']} / {state['tasks_total']}")
            print(f"  completion_rate: {state['tasks_completion_rate']:.0%}")
            
            if state.get("errors"):
                print(f"\n  Errors:")
                for error in state["errors"]:
                    print(f"    - {error}")
            
            if state.get("warnings"):
                print(f"\n  Warnings:")
                for warning in state["warnings"]:
                    print(f"    - {warning}")
            
            print()
            
            # Get recommendation
            recommendation_result = agent.recommend_next_workflow(spec_id)
            
            if isinstance(recommendation_result, dict) and recommendation_result.get("error"):
                print(f"Error: {get_user_friendly_error(recommendation_result)}")
            elif isinstance(recommendation_result, dict) and recommendation_result.get("success"):
                recommendation = recommendation_result["result"]
                
                if recommendation:
                    print(f"Recommendation:")
                    print(f"  Workflow: {recommendation.workflow.name}")
                    print(f"  Reason: {recommendation.reason}")
                    print(f"  Priority: {recommendation.priority}")
                    print(f"  Estimated Time: {recommendation.estimated_time}")
                    
                    if recommendation.warnings:
                        print(f"\n  Warnings:")
                        for warning in recommendation.warnings:
                            print(f"    - {warning}")
                    
                    if recommendation.tips:
                        print(f"\n  Tips:")
                        for tip in recommendation.tips:
                            print(f"    - {tip}")
                    
                    print()
                    print(f"Command:")
                    print(recommendation.command)
                else:
                    print("All done! No more workflows needed.")
            else:
                print("Could not get recommendation")
    
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        import traceback
        traceback.print_exc()
