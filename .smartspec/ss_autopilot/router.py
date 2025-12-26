from __future__ import annotations

from typing import Dict, Any, Literal

Step = Literal["SPEC", "PLAN", "TASKS", "IMPLEMENT", "SYNC_TASKS", "TEST_SUITE", "QUALITY_GATE", "STOP"]

def decide_next(state: Dict[str, Any]) -> Step:
    # base artifacts
    if not state.get("has_spec"):
        return "SPEC"
    if not state.get("has_plan"):
        return "PLAN"
    if not state.get("has_tasks"):
        return "TASKS"

    # after tasks exist
    # If implementation hasn't been attempted, implement/handoff first
    if not state.get("did_implement", False):
        return "IMPLEMENT"

    # Optional post-implement stages (can be enabled/disabled by config flags in state)
    if state.get("enable_sync_tasks", True) and not state.get("did_sync_tasks", False):
        return "SYNC_TASKS"
    if state.get("enable_test_suite", True) and not state.get("did_test_suite", False):
        return "TEST_SUITE"
    if state.get("enable_quality_gate", True) and not state.get("did_quality_gate", False):
        return "QUALITY_GATE"

    return "STOP"
