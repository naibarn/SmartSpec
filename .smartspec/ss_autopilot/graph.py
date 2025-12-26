from __future__ import annotations

from typing import Dict, Any

from langgraph.graph import StateGraph, END

from .router import decide_next
from .commands import build_slash_command, default_out_dir
from .runner import WorkflowRunner
from .status import append_status
from .error_handler import with_error_handling
from .advanced_logger import get_logger
from .agent_wrapper import wrap_agent
from .checkpoint_manager import create_checkpointer, CheckpointManager


@with_error_handling
def build_graph(cfg: Dict[str, Any]):
    """
    Build LangGraph workflow with error handling.
    
    Args:
        cfg: Configuration dict
        
    Returns:
        Compiled graph or error dict
    """
    try:
        logger = get_logger("graph")
        logger.info("Building LangGraph workflow")
        
        ai_specs_dir = cfg["paths"]["ai_specs_dir"]

        graph = StateGraph(dict)

        def check(state: Dict[str, Any]) -> Dict[str, Any]:
            """Check next step with error handling"""
            try:
                step = decide_next(state)
                state["step"] = step
                state["message"] = f"Next step: {step}"
            except Exception as e:
                state["step"] = "STOP"
                state["message"] = f"Error determining next step: {str(e)}"
            return state

        def run_spec(state: Dict[str, Any]) -> Dict[str, Any]:
            """Run spec generation with error handling"""
            try:
                runner = WorkflowRunner(cfg, ai_specs_dir)
                outdir = default_out_dir("generate-spec", state["spec_id"])
                cmd = build_slash_command(cfg, state["platform"], "generate_spec",
                                        state["spec_path"], "--out", outdir, "--json")
                res = runner.run(runner_type=state["runner_type"], cmd_for_human=cmd, shell_cmd=_shell_entry(cfg, "generate_spec"))
                append_status(ai_specs_dir, f"\n- SPEC scheduled/executed: ok={res.ok} rc={res.returncode}\n")
                state["message"] = "SPEC scheduled (IDE) or executed (shell). Rerun after completion."
            except Exception as e:
                state["message"] = f"Error running SPEC: {str(e)}"
                state["errors"] = state.get("errors", []) + [str(e)]
            return state

        def run_plan(state: Dict[str, Any]) -> Dict[str, Any]:
            """Run plan generation with error handling"""
            try:
                runner = WorkflowRunner(cfg, ai_specs_dir)
                outdir = default_out_dir("generate-plan", state["spec_id"])
                cmd = build_slash_command(cfg, state["platform"], "generate_plan",
                                        state["spec_path"], "--out", outdir, "--json")
                res = runner.run(runner_type=state["runner_type"], cmd_for_human=cmd, shell_cmd=_shell_entry(cfg, "generate_plan"))
                append_status(ai_specs_dir, f"\n- PLAN scheduled/executed: ok={res.ok} rc={res.returncode}\n")
                state["message"] = "PLAN scheduled (IDE) or executed (shell). Rerun after completion."
            except Exception as e:
                state["message"] = f"Error running PLAN: {str(e)}"
                state["errors"] = state.get("errors", []) + [str(e)]
            return state

        def run_tasks(state: Dict[str, Any]) -> Dict[str, Any]:
            """Run tasks generation with error handling"""
            try:
                runner = WorkflowRunner(cfg, ai_specs_dir)
                outdir = default_out_dir("generate-tasks", state["spec_id"])
                cmd = build_slash_command(cfg, state["platform"], "generate_tasks",
                                        state["spec_path"], "--out", outdir, "--json")
                res = runner.run(runner_type=state["runner_type"], cmd_for_human=cmd, shell_cmd=_shell_entry(cfg, "generate_tasks"))
                append_status(ai_specs_dir, f"\n- TASKS scheduled/executed: ok={res.ok} rc={res.returncode}\n")
                state["message"] = "TASKS scheduled (IDE) or executed (shell). Rerun after completion."
            except Exception as e:
                state["message"] = f"Error running TASKS: {str(e)}"
                state["errors"] = state.get("errors", []) + [str(e)]
            return state

        def implement_or_handoff(state: Dict[str, Any]) -> Dict[str, Any]:
            """Run implementation with error handling"""
            try:
                runner = WorkflowRunner(cfg, ai_specs_dir)
                outdir = default_out_dir("implement-tasks", state["spec_id"])
                cmd = build_slash_command(cfg, state["platform"], "implement_tasks",
                                        state["tasks_path"], "--apply",
                                        "--out", outdir, "--json")
                res = runner.run(runner_type=state["runner_type"], cmd_for_human=cmd, shell_cmd=_shell_entry(cfg, "implement_tasks"))
                append_status(ai_specs_dir, f"\n- IMPLEMENT scheduled/executed: ok={res.ok} rc={res.returncode}\n")
                state["did_implement"] = True if res.ok else state.get("did_implement", False)
                state["message"] = "IMPLEMENT written (IDE) or executed (shell). Next: sync/tests/quality gate."
            except Exception as e:
                state["message"] = f"Error running IMPLEMENT: {str(e)}"
                state["errors"] = state.get("errors", []) + [str(e)]
            return state

        def sync_tasks(state: Dict[str, Any]) -> Dict[str, Any]:
            """Run tasks sync with error handling"""
            try:
                runner = WorkflowRunner(cfg, ai_specs_dir)
                outdir = default_out_dir("sync-tasks", state["spec_id"])
                cmd = build_slash_command(cfg, state["platform"], "sync_tasks_checkboxes",
                                        state["tasks_path"], "--out", outdir, "--json", "--apply")
                res = runner.run(runner_type=state["runner_type"], cmd_for_human=cmd, shell_cmd=_shell_entry(cfg, "sync_tasks_checkboxes"))
                append_status(ai_specs_dir, f"\n- SYNC_TASKS scheduled/executed: ok={res.ok} rc={res.returncode}\n")
                state["did_sync_tasks"] = True if res.ok else state.get("did_sync_tasks", False)
                state["message"] = "Sync tasks checkboxes done (or scheduled)."
            except Exception as e:
                state["message"] = f"Error running SYNC_TASKS: {str(e)}"
                state["errors"] = state.get("errors", []) + [str(e)]
            return state

        def test_suite(state: Dict[str, Any]) -> Dict[str, Any]:
            """Run test suite with error handling"""
            try:
                runner = WorkflowRunner(cfg, ai_specs_dir)
                outdir = default_out_dir("test-suite", state["spec_id"])
                # Placeholders; user can adjust flags in IDE
                cmd = build_slash_command(cfg, state["platform"], "test_suite_runner",
                                        "--out", outdir, "--json")
                res = runner.run(runner_type=state["runner_type"], cmd_for_human=cmd, shell_cmd=_shell_entry(cfg, "test_suite_runner"))
                append_status(ai_specs_dir, f"\n- TEST_SUITE scheduled/executed: ok={res.ok} rc={res.returncode}\n")
                state["did_test_suite"] = True if res.ok else state.get("did_test_suite", False)
                state["message"] = "Test suite run scheduled/executed."
            except Exception as e:
                state["message"] = f"Error running TEST_SUITE: {str(e)}"
                state["errors"] = state.get("errors", []) + [str(e)]
            return state

        def quality_gate(state: Dict[str, Any]) -> Dict[str, Any]:
            """Run quality gate with error handling"""
            try:
                runner = WorkflowRunner(cfg, ai_specs_dir)
                outdir = default_out_dir("quality-gate", state["spec_id"])
                cmd = build_slash_command(cfg, state["platform"], "quality_gate",
                                        "--profile", "ci", "--out", outdir, "--json", "--strict")
                res = runner.run(runner_type=state["runner_type"], cmd_for_human=cmd, shell_cmd=_shell_entry(cfg, "quality_gate"))
                append_status(ai_specs_dir, f"\n- QUALITY_GATE scheduled/executed: ok={res.ok} rc={res.returncode}\n")
                state["did_quality_gate"] = True if res.ok else state.get("did_quality_gate", False)
                state["message"] = "Quality gate scheduled/executed."
            except Exception as e:
                state["message"] = f"Error running QUALITY_GATE: {str(e)}"
                state["errors"] = state.get("errors", []) + [str(e)]
            return state

        def stop(state: Dict[str, Any]) -> Dict[str, Any]:
            """Stop node"""
            state["step"] = "STOP"
            state["message"] = "Nothing to do (or waiting for IDE). Rerun after running the suggested command(s)."
            return state

        graph.add_node("CHECK", check)
        graph.add_node("SPEC", run_spec)
        graph.add_node("PLAN", run_plan)
        graph.add_node("TASKS", run_tasks)
        graph.add_node("IMPLEMENT", implement_or_handoff)
        graph.add_node("SYNC_TASKS", sync_tasks)
        graph.add_node("TEST_SUITE", test_suite)
        graph.add_node("QUALITY_GATE", quality_gate)
        graph.add_node("STOP", stop)

        graph.set_entry_point("CHECK")

        def route(state: Dict[str, Any]) -> str:
            """Route to next node"""
            step = state.get("step", "STOP")
            return step if step in {"SPEC","PLAN","TASKS","IMPLEMENT","SYNC_TASKS","TEST_SUITE","QUALITY_GATE"} else "STOP"

        graph.add_conditional_edges(
            "CHECK",
            route,
            {
                "SPEC": "SPEC",
                "PLAN": "PLAN",
                "TASKS": "TASKS",
                "IMPLEMENT": "IMPLEMENT",
                "SYNC_TASKS": "SYNC_TASKS",
                "TEST_SUITE": "TEST_SUITE",
                "QUALITY_GATE": "QUALITY_GATE",
                "STOP": "STOP",
            }
        )

        # End after one action; user can rerun to continue (works best with IDE slash-commands)
        for n in ["SPEC","PLAN","TASKS","IMPLEMENT","SYNC_TASKS","TEST_SUITE","QUALITY_GATE","STOP"]:
            graph.add_edge(n, END)

        # Add checkpointing
        checkpointer = create_checkpointer(use_sqlite=True)
        compiled = graph.compile(checkpointer=checkpointer)
        
        logger.info("LangGraph workflow built with checkpointing enabled")
        
        return compiled
    
    except Exception as e:
        raise RuntimeError(f"Failed to build graph: {str(e)}")


def _shell_entry(cfg: Dict[str, Any], key: str):
    """
    Get shell entry point with error handling.
    
    Args:
        cfg: Configuration dict
        key: Entry point key
        
    Returns:
        List of command parts or None
    """
    try:
        ep = cfg.get("runner", {}).get("workflow_entrypoints", {}).get(key) or ""
        if not ep:
            return None
        return ep.split()
    except Exception:
        return None
