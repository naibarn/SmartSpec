"""
Enhanced router with support for partial implementation and edge cases.

This router handles:
- Partial implementation (IN_PROGRESS state)
- Checkbox mismatches (needs_sync)
- Smart recommendations based on completion rate
"""

from typing import Dict, Any, Literal

from .error_handler import with_error_handling

Step = Literal[
    "SPEC", 
    "PLAN", 
    "TASKS", 
    "IMPLEMENT", 
    "SYNC_TASKS", 
    "TEST_SUITE", 
    "QUALITY_GATE", 
    "FIX_ERRORS",
    "VERIFY",
    "STOP"
]


@with_error_handling
def decide_next(state: Dict[str, Any]) -> Step:
    """
    Decide next step based on enhanced state with error handling.
    
    Handles:
    - Partial implementation (IN_PROGRESS)
    - Checkbox mismatches (needs_sync)
    - Smart recommendations based on completion rate
    
    Args:
        state: Enhanced state with:
            - has_spec: bool
            - has_plan: bool
            - has_tasks: bool
            - implementation_status: "NOT_STARTED" | "IN_PROGRESS" | "COMPLETED"
            - tasks_completion_rate: float (0.0 to 1.0)
            - needs_sync: bool
            - did_sync_tasks: bool
            - did_test_suite: bool
            - did_quality_gate: bool
            - errors: list[str]
    
    Returns:
        Next step to execute or error dict
    """
    try:
        # Check if has errors
        if state.get("errors"):
            return "FIX_ERRORS"
        
        # Base artifacts
        if not state.get("has_spec", False):
            return "SPEC"
        
        if not state.get("has_plan", False):
            return "PLAN"
        
        if not state.get("has_tasks", False):
            return "TASKS"
        
        # Get implementation status
        impl_status = state.get("implementation_status", "NOT_STARTED")
        completion_rate = state.get("tasks_completion_rate", 0.0)
        needs_sync = state.get("needs_sync", False)
        
        # Handle different implementation statuses
        if impl_status == "NOT_STARTED":
            # No implementation yet → start implementing
            return "IMPLEMENT"
        
        elif impl_status == "IN_PROGRESS":
            # Partial implementation - handle carefully
            
            # If needs sync → sync first to get accurate state
            # This ensures checkboxes match actual code before continuing
            if needs_sync and not state.get("did_sync_tasks", False):
                return "SYNC_TASKS"
            
            # If less than 50% done → continue implementing
            # Focus on getting more work done before syncing
            if completion_rate < 0.5:
                return "IMPLEMENT"
            
            # If 50-99% done → recommend sync first, then continue
            # At this point, it's worth syncing to ensure accuracy
            elif completion_rate < 1.0:
                if not state.get("did_sync_tasks", False):
                    return "SYNC_TASKS"
                else:
                    return "IMPLEMENT"
            
            # If 100% done (but still IN_PROGRESS) → verify
            # This shouldn't happen, but handle it gracefully
            else:
                return "VERIFY"
        
        elif impl_status == "COMPLETED":
            # All tasks completed - move to post-implementation steps
            
            # Sync if needed or not done yet
            if needs_sync or not state.get("did_sync_tasks", False):
                return "SYNC_TASKS"
            
            # Run tests (if enabled)
            if state.get("enable_test_suite", True) and not state.get("did_test_suite", False):
                return "TEST_SUITE"
            
            # Quality gate (if enabled)
            if state.get("enable_quality_gate", True) and not state.get("did_quality_gate", False):
                return "QUALITY_GATE"
            
            # All done!
            return "STOP"
        
        # Fallback
        return "STOP"
    
    except Exception as e:
        # On any error, default to STOP to prevent infinite loops
        return "STOP"


@with_error_handling
def get_step_recommendation(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get detailed recommendation for next step with error handling.
    
    Returns:
        Dict with recommendation or error dict:
        {
            "step": "IMPLEMENT",
            "reason": "5 out of 12 tasks completed (42%)",
            "priority": "high",
            "estimated_time": "2-4 hours",
            "warnings": ["Consider syncing after reaching 50% completion"],
            "tips": ["Focus on completing related tasks together"]
        }
    """
    try:
        next_step_result = decide_next(state)
        
        # Check if decide_next returned an error
        if isinstance(next_step_result, dict) and next_step_result.get("error"):
            return {
                "step": "STOP",
                "reason": "Error determining next step",
                "priority": "none",
                "estimated_time": "0 minutes",
                "warnings": [next_step_result.get("message", "Unknown error")],
                "tips": []
            }
        
        # Extract next_step from result
        if isinstance(next_step_result, dict) and next_step_result.get("success"):
            next_step = next_step_result["result"]
        else:
            next_step = next_step_result
        
        impl_status = state.get("implementation_status", "NOT_STARTED")
        completion_rate = state.get("tasks_completion_rate", 0.0)
        tasks_completed = state.get("tasks_completed", 0)
        tasks_total = state.get("tasks_total", 0)
        needs_sync = state.get("needs_sync", False)
        
        # Build recommendation
        recommendation = {
            "step": next_step,
            "reason": "",
            "priority": "normal",
            "estimated_time": "",
            "warnings": [],
            "tips": []
        }
        
        try:
            if next_step == "IMPLEMENT":
                if impl_status == "NOT_STARTED":
                    recommendation["reason"] = "No tasks implemented yet"
                    recommendation["priority"] = "high"
                    recommendation["estimated_time"] = f"{tasks_total * 20} minutes"
                elif impl_status == "IN_PROGRESS":
                    tasks_remaining = tasks_total - tasks_completed
                    recommendation["reason"] = f"{tasks_completed} out of {tasks_total} tasks completed ({completion_rate:.0%})"
                    recommendation["priority"] = "high"
                    recommendation["estimated_time"] = f"{tasks_remaining * 20} minutes"
                    
                    if completion_rate >= 0.5 and not state.get("did_sync_tasks", False):
                        recommendation["warnings"].append("Consider syncing after reaching 50% completion")
                    
                    if needs_sync:
                        recommendation["warnings"].append("Tasks.md checkboxes might not match actual code")
                        recommendation["tips"].append("Run sync_tasks_checkboxes to verify progress")
            
            elif next_step == "SYNC_TASKS":
                if needs_sync:
                    recommendation["reason"] = "Tasks.md checkboxes might not match actual code"
                    recommendation["priority"] = "high"
                else:
                    recommendation["reason"] = "Sync checkboxes with actual implementation"
                    recommendation["priority"] = "normal"
                
                recommendation["estimated_time"] = "2-5 minutes"
                recommendation["tips"].append("This will update checkboxes to match actual code")
            
            elif next_step == "VERIFY":
                recommendation["reason"] = "All tasks marked complete, but verification needed"
                recommendation["priority"] = "high"
                recommendation["estimated_time"] = "5-10 minutes"
            
            elif next_step == "TEST_SUITE":
                recommendation["reason"] = "Implementation complete, ready for testing"
                recommendation["priority"] = "normal"
                recommendation["estimated_time"] = "10-30 minutes"
            
            elif next_step == "QUALITY_GATE":
                recommendation["reason"] = "Tests passed, ready for quality gate check"
                recommendation["priority"] = "normal"
                recommendation["estimated_time"] = "5-15 minutes"
            
            elif next_step == "STOP":
                recommendation["reason"] = "All steps completed successfully!"
                recommendation["priority"] = "none"
                recommendation["estimated_time"] = "0 minutes"
        
        except Exception as e:
            recommendation["warnings"].append(f"Error building recommendation: {str(e)}")
        
        return recommendation
    
    except Exception as e:
        # Return default recommendation on error
        return {
            "step": "STOP",
            "reason": f"Error: {str(e)}",
            "priority": "none",
            "estimated_time": "0 minutes",
            "warnings": [str(e)],
            "tips": []
        }


# Example usage
if __name__ == "__main__":
    try:
        # Test Case 1: Partial implementation (42%)
        print("Test Case 1: Partial Implementation (42%)")
        state1 = {
            "has_spec": True,
            "has_plan": True,
            "has_tasks": True,
            "implementation_status": "IN_PROGRESS",
            "tasks_total": 12,
            "tasks_completed": 5,
            "tasks_completion_rate": 0.42,
            "needs_sync": False,
            "did_sync_tasks": False
        }
        
        next_step_result = decide_next(state1)
        if isinstance(next_step_result, dict) and next_step_result.get("success"):
            next_step = next_step_result["result"]
        else:
            next_step = next_step_result
        
        recommendation_result = get_step_recommendation(state1)
        if isinstance(recommendation_result, dict) and recommendation_result.get("success"):
            recommendation = recommendation_result["result"]
        else:
            recommendation = recommendation_result
        
        print(f"  Next Step: {next_step}")
        print(f"  Reason: {recommendation['reason']}")
        print(f"  Priority: {recommendation['priority']}")
        print(f"  Estimated Time: {recommendation['estimated_time']}")
        print()
        
        # Test Case 2: Needs sync
        print("Test Case 2: Needs Sync")
        state2 = {
            "has_spec": True,
            "has_plan": True,
            "has_tasks": True,
            "implementation_status": "IN_PROGRESS",
            "tasks_total": 12,
            "tasks_completed": 8,
            "tasks_completion_rate": 0.67,
            "needs_sync": True,
            "did_sync_tasks": False
        }
        
        next_step_result = decide_next(state2)
        if isinstance(next_step_result, dict) and next_step_result.get("success"):
            next_step = next_step_result["result"]
        else:
            next_step = next_step_result
        
        recommendation_result = get_step_recommendation(state2)
        if isinstance(recommendation_result, dict) and recommendation_result.get("success"):
            recommendation = recommendation_result["result"]
        else:
            recommendation = recommendation_result
        
        print(f"  Next Step: {next_step}")
        print(f"  Reason: {recommendation['reason']}")
        print(f"  Priority: {recommendation['priority']}")
        print(f"  Warnings: {recommendation['warnings']}")
        print()
        
        # Test Case 3: Almost done (92%)
        print("Test Case 3: Almost Done (92%)")
        state3 = {
            "has_spec": True,
            "has_plan": True,
            "has_tasks": True,
            "implementation_status": "IN_PROGRESS",
            "tasks_total": 12,
            "tasks_completed": 11,
            "tasks_completion_rate": 0.92,
            "needs_sync": False,
            "did_sync_tasks": False
        }
        
        next_step_result = decide_next(state3)
        if isinstance(next_step_result, dict) and next_step_result.get("success"):
            next_step = next_step_result["result"]
        else:
            next_step = next_step_result
        
        recommendation_result = get_step_recommendation(state3)
        if isinstance(recommendation_result, dict) and recommendation_result.get("success"):
            recommendation = recommendation_result["result"]
        else:
            recommendation = recommendation_result
        
        print(f"  Next Step: {next_step}")
        print(f"  Reason: {recommendation['reason']}")
        print(f"  Priority: {recommendation['priority']}")
        print()
    
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        import traceback
        traceback.print_exc()
