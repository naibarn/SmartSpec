"""
Enhanced CLI entry point for SmartSpec Autopilot.

This is an enhanced version with better platform support, user-friendly status.md,
and simplified commands.

Usage:
    ss-autopilot run --spec-id spec-core-001-authentication
    ss-autopilot run --spec-id spec-core-001-authentication --platform kilo
    ss-autopilot status --spec-id spec-core-001-authentication
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Dict, Any

from .platform import detect_platform, get_platform_info
from .router import decide_next
from .commands import build_slash_command, default_out_dir
from .status_writer import StatusWriter
from .report_enhancer import ReportEnhancer


def load_config() -> Dict[str, Any]:
    """Load configuration from .autopilot/config.yaml or config/autopilot.yaml"""
    import yaml
    
    # Try .autopilot/config.yaml first (project-specific)
    config_paths = [
        Path(".autopilot/config.yaml"),
        Path("config/autopilot.yaml"),
        Path(__file__).parent.parent.parent / "config" / "autopilot.yaml"
    ]
    
    for config_path in config_paths:
        if config_path.exists():
            with open(config_path) as f:
                return yaml.safe_load(f)
    
    # Default config
    return {
        "paths": {
            "workflows_dir": ".smartspec/workflows",
            "scripts_dir": ".smartspec/scripts",
            "reports_dir": ".spec/reports",
            "ai_specs_dir": "ai_specs"
        },
        "runner": {
            "type": "ide"
        },
        "commands": {
            "kilo": {
                "generate_spec": "/smartspec_generate_spec.md --platform kilo",
                "generate_plan": "/smartspec_generate_plan.md --platform kilo",
                "generate_tasks": "/smartspec_generate_tasks.md --platform kilo",
                "implement_tasks": "/smartspec_implement_tasks.md --platform kilo",
            }
        },
        "defaults": {
            "lang": "auto",
            "json": True
        }
    }


def read_spec_state(spec_id: str, reports_dir: Path) -> Dict[str, Any]:
    """Read state for a specific spec from reports"""
    state = {
        "spec_id": spec_id,
        "has_spec": False,
        "has_plan": False,
        "has_tasks": False,
        "did_implement": False,
        "did_sync_tasks": False,
        "did_test_suite": False,
        "did_quality_gate": False,
        "errors": []
    }
    
    # Check if spec file exists
    spec_file = Path("specs") / spec_id / "spec.md"
    state["has_spec"] = spec_file.exists()
    
    # Check if plan exists
    plan_file = Path("specs") / spec_id / "plan.md"
    state["has_plan"] = plan_file.exists()
    
    # Check if tasks exist
    tasks_file = Path("specs") / spec_id / "tasks.md"
    state["has_tasks"] = tasks_file.exists()
    state["tasks_path"] = str(tasks_file)
    state["spec_path"] = str(spec_file)
    
    # Check implementation report
    implement_report = reports_dir / "implement-tasks" / spec_id / "summary.json"
    if implement_report.exists():
        import json
        try:
            with open(implement_report) as f:
                data = json.load(f)
                if data.get("status") == "success":
                    state["did_implement"] = True
                else:
                    state["errors"].append(f"Implementation failed: {data.get('error', 'Unknown error')}")
        except:
            pass
    
    # Check sync report
    sync_report = reports_dir / "sync-tasks" / spec_id / "summary.json"
    if sync_report.exists():
        import json
        try:
            with open(sync_report) as f:
                data = json.load(f)
                if data.get("status") == "success":
                    state["did_sync_tasks"] = True
        except:
            pass
    
    return state


def get_completed_steps(state: Dict[str, Any]) -> list[str]:
    """Get list of completed steps"""
    completed = []
    if state.get("has_spec"):
        completed.append("SPEC")
    if state.get("has_plan"):
        completed.append("PLAN")
    if state.get("has_tasks"):
        completed.append("TASKS")
    if state.get("did_implement"):
        completed.append("IMPLEMENT")
    if state.get("did_sync_tasks"):
        completed.append("SYNC_TASKS")
    if state.get("did_test_suite"):
        completed.append("TEST_SUITE")
    if state.get("did_quality_gate"):
        completed.append("QUALITY_GATE")
    return completed


def cmd_run(args):
    """Run Autopilot to determine next step and generate status.md"""
    
    # Load config
    cfg = load_config()
    
    # Detect platform
    platform = args.platform or detect_platform()
    print(f"🔍 Detected platform: {platform}")
    
    # Get platform info
    platform_info = get_platform_info(platform)
    print(f"📱 Platform: {platform_info['name']}")
    
    # Read spec state
    reports_dir = Path(cfg["paths"]["reports_dir"])
    state = read_spec_state(args.spec_id, reports_dir)
    state["platform"] = platform
    
    # Determine next step
    next_step = decide_next(state)
    print(f"🎯 Next step: {next_step}")
    
    if next_step == "STOP":
        print("✅ All steps completed!")
        
        # Write complete status
        ai_specs_dir = cfg["paths"]["ai_specs_dir"]
        writer = StatusWriter(ai_specs_dir)
        writer.write_complete_status(args.spec_id, platform)
        
        print(f"📄 Status written to: {ai_specs_dir}/status.md")
        return
    
    # Generate command
    workflow_key = {
        "SPEC": "generate_spec",
        "PLAN": "generate_plan",
        "TASKS": "generate_tasks",
        "IMPLEMENT": "implement_tasks",
        "SYNC_TASKS": "sync_tasks_checkboxes",
        "TEST_SUITE": "test_suite_runner",
        "QUALITY_GATE": "quality_gate",
    }.get(next_step)
    
    # Build command
    if workflow_key:
        outdir = default_out_dir(workflow_key.replace("_", "-"), args.spec_id)
        
        # Build args based on workflow
        if workflow_key == "implement_tasks":
            cmd_args = [state["tasks_path"], "--apply", "--out", outdir, "--json"]
        elif workflow_key == "sync_tasks_checkboxes":
            cmd_args = [state["tasks_path"], "--out", outdir, "--json", "--apply"]
        else:
            cmd_args = [state["spec_path"], "--out", outdir, "--json"]
        
        command = build_slash_command(cfg, platform, workflow_key, *cmd_args)
    else:
        command = "# No command generated"
    
    print(f"📝 Command: {command}")
    
    # Write status.md
    ai_specs_dir = cfg["paths"]["ai_specs_dir"]
    writer = StatusWriter(ai_specs_dir)
    completed_steps = get_completed_steps(state)
    
    writer.write_status(
        spec_id=args.spec_id,
        current_step=next_step,
        command=command,
        completed_steps=completed_steps,
        errors=state.get("errors", []),
        platform=platform
    )
    
    print(f"📄 Status written to: {ai_specs_dir}/status.md")
    print(f"\n✨ Next: Open {ai_specs_dir}/status.md to see what to do next!")


def cmd_status(args):
    """Show current status"""
    
    # Load config
    cfg = load_config()
    
    # Read status.md
    ai_specs_dir = Path(cfg["paths"]["ai_specs_dir"])
    status_file = ai_specs_dir / "status.md"
    
    if not status_file.exists():
        print(f"❌ No status file found. Run: ss-autopilot run --spec-id {args.spec_id}")
        return
    
    # Print status
    with open(status_file) as f:
        print(f.read())


def cmd_init(args):
    """Initialize Autopilot in current project"""
    
    print("🚀 Initializing SmartSpec Autopilot...")
    
    # Create .autopilot directory
    autopilot_dir = Path(".autopilot")
    autopilot_dir.mkdir(exist_ok=True)
    print(f"✅ Created {autopilot_dir}/")
    
    # Create logs directory
    logs_dir = autopilot_dir / "logs"
    logs_dir.mkdir(exist_ok=True)
    print(f"✅ Created {logs_dir}/")
    
    # Create ai_specs directory
    ai_specs_dir = Path("ai_specs")
    ai_specs_dir.mkdir(exist_ok=True)
    print(f"✅ Created {ai_specs_dir}/")
    
    # Copy default config
    import yaml
    import shutil
    
    default_config_path = Path(__file__).parent.parent.parent / "config" / "autopilot.yaml"
    project_config_path = autopilot_dir / "config.yaml"
    
    if default_config_path.exists() and not project_config_path.exists():
        shutil.copy(default_config_path, project_config_path)
        print(f"✅ Created {project_config_path}")
    
    # Create state.json
    state_file = autopilot_dir / "state.json"
    if not state_file.exists():
        import json
        initial_state = {
            "version": "1.0",
            "specs": {}
        }
        with open(state_file, "w") as f:
            json.dump(initial_state, f, indent=2)
        print(f"✅ Created {state_file}")
    
    print("\n✨ Autopilot initialized successfully!")
    print("\n📚 Next steps:")
    print("  1. Run: ss-autopilot run --spec-id <your-spec-id>")
    print("  2. Open: ai_specs/status.md")
    print("  3. Follow the instructions!")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="SmartSpec Autopilot - Automated workflow orchestration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Initialize Autopilot in current project
  ss-autopilot run --spec-id <spec-id> --init
  
  # Run Autopilot to determine next step
  ss-autopilot run --spec-id spec-core-001-authentication
  
  # Run with specific platform
  ss-autopilot run --spec-id spec-core-001-authentication --platform kilo
  
  # Show current status
  ss-autopilot status --spec-id spec-core-001-authentication
"""
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # init command
    parser_init = subparsers.add_parser("init", help="Initialize Autopilot in current project")
    parser_init.set_defaults(func=cmd_init)
    
    # run command
    parser_run = subparsers.add_parser("run", help="Run Autopilot to determine next step")
    parser_run.add_argument("--spec-id", required=True, help="Spec ID (e.g., spec-core-001-authentication)")
    parser_run.add_argument("--platform", choices=["kilo", "antigravity", "claude"], help="Platform (auto-detect if not specified)")
    parser_run.set_defaults(func=cmd_run)
    
    # status command
    parser_status = subparsers.add_parser("status", help="Show current status")
    parser_status.add_argument("--spec-id", required=True, help="Spec ID")
    parser_status.set_defaults(func=cmd_status)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == "__main__":
    main()
