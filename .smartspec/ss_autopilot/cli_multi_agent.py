"""
Multi-Agent CLI - Unified command-line interface for all agents.

Usage:
    ss-autopilot run --spec-id <spec-id>
    ss-autopilot status --spec-id <spec-id> [--query <question>]
    ss-autopilot ask "<natural language query>"
"""

import sys
import argparse
from pathlib import Path


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="SmartSpec Multi-Agent System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Orchestrator (main loop)
  ss-autopilot run --spec-id spec-core-001
  
  # Status queries
  ss-autopilot status --spec-id spec-core-001
  ss-autopilot status --spec-id spec-core-001 --query "เหลืออะไรบ้าง?"
  
  # Natural language (via Intent Parser)
  ss-autopilot ask "spec-core-001 งานถึงไหนแล้ว?"
  ss-autopilot ask "เริ่มพัฒนา spec-core-002"
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Run command (Orchestrator)
    run_parser = subparsers.add_parser("run", help="Run orchestrator agent")
    run_parser.add_argument("--spec-id", required=True, help="Spec ID")
    run_parser.add_argument("--auto", action="store_true", help="Auto-continue without prompts")
    
    # Status command (Status Agent)
    status_parser = subparsers.add_parser("status", help="Query status")
    status_parser.add_argument("--spec-id", required=True, help="Spec ID")
    status_parser.add_argument("--query", help="Specific question")
    
    # Ask command (Intent Parser)
    ask_parser = subparsers.add_parser("ask", help="Natural language query")
    ask_parser.add_argument("query", help="Natural language query")
    
    # Parse args
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Execute command
    if args.command == "run":
        return cmd_run(args)
    elif args.command == "status":
        return cmd_status(args)
    elif args.command == "ask":
        return cmd_ask(args)
    else:
        print(f"Unknown command: {args.command}")
        return 1


def cmd_run(args):
    """Run orchestrator agent"""
    print(f"🤖 Orchestrator Agent")
    print(f"=" * 50)
    print(f"Spec ID: {args.spec_id}")
    print()
    
    # Import here to avoid circular imports
    sys.path.insert(0, str(Path(__file__).parent))
    
    try:
        # Load modules dynamically
        import importlib.util
        
        # Load orchestrator_agent
        spec = importlib.util.spec_from_file_location(
            "orchestrator_agent",
            Path(__file__).parent / "orchestrator_agent.py"
        )
        orchestrator_module = importlib.util.module_from_spec(spec)
        
        # Mock the imports
        import sys
        sys.modules['ss_autopilot.workflow_loader'] = type(sys)('workflow_loader')
        sys.modules['ss_autopilot.tasks_parser'] = type(sys)('tasks_parser')
        sys.modules['ss_autopilot.router_enhanced'] = type(sys)('router_enhanced')
        
        # Load workflow_loader first
        spec_wl = importlib.util.spec_from_file_location(
            "workflow_loader",
            Path(__file__).parent / "workflow_loader.py"
        )
        workflow_loader = importlib.util.module_from_spec(spec_wl)
        spec_wl.loader.exec_module(workflow_loader)
        sys.modules['ss_autopilot.workflow_loader'] = workflow_loader
        
        # Load tasks_parser
        spec_tp = importlib.util.spec_from_file_location(
            "tasks_parser",
            Path(__file__).parent / "tasks_parser.py"
        )
        tasks_parser = importlib.util.module_from_spec(spec_tp)
        spec_tp.loader.exec_module(tasks_parser)
        sys.modules['ss_autopilot.tasks_parser'] = tasks_parser
        
        # Load router_enhanced
        spec_re = importlib.util.spec_from_file_location(
            "router_enhanced",
            Path(__file__).parent / "router_enhanced.py"
        )
        router_enhanced = importlib.util.module_from_spec(spec_re)
        spec_re.loader.exec_module(router_enhanced)
        sys.modules['ss_autopilot.router_enhanced'] = router_enhanced
        
        # Now load orchestrator
        spec.loader.exec_module(orchestrator_module)
        
        # Create agent
        OrchestratorAgent = orchestrator_module.OrchestratorAgent
        agent = OrchestratorAgent()
        
        # Get recommendation
        recommendation = agent.recommend_next_workflow(args.spec_id)
        
        if recommendation is None:
            print("✅ All done! No more workflows needed.")
            return 0
        
        # Display recommendation
        print(f"📋 Recommendation")
        print(f"-" * 50)
        print(f"Workflow: {recommendation.workflow.name}")
        print(f"Reason: {recommendation.reason}")
        print(f"Priority: {recommendation.priority}")
        print(f"Estimated Time: {recommendation.estimated_time}")
        print()
        
        if recommendation.warnings:
            print(f"⚠️  Warnings:")
            for warning in recommendation.warnings:
                print(f"  - {warning}")
            print()
        
        if recommendation.tips:
            print(f"💡 Tips:")
            for tip in recommendation.tips:
                print(f"  - {tip}")
            print()
        
        print(f"🚀 Command:")
        print(f"-" * 50)
        print(recommendation.command)
        print()
        
        # Auto-continue?
        if not args.auto:
            response = input("Run this command? [y/N] ")
            if response.lower() != 'y':
                print("Cancelled.")
                return 0
        
        print("✅ Command ready to execute!")
        print("(In production, this would execute the workflow)")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


def cmd_status(args):
    """Query status"""
    print(f"📊 Status Agent")
    print(f"=" * 50)
    print(f"Spec ID: {args.spec_id}")
    if args.query:
        print(f"Query: {args.query}")
    print()
    
    try:
        # Load status_agent
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "status_agent",
            Path(__file__).parent / "status_agent.py"
        )
        status_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(status_module)
        
        # Create agent
        StatusAgent = status_module.StatusAgent
        agent = StatusAgent()
        
        # Query
        response = agent.query(args.spec_id, args.query or "")
        
        # Display response
        print(agent.format_response(response))
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


def cmd_ask(args):
    """Natural language query"""
    print(f"💬 Intent Parser Agent")
    print(f"=" * 50)
    print(f"Query: {args.query}")
    print()
    
    try:
        # Load intent_parser_agent
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "intent_parser_agent",
            Path(__file__).parent / "intent_parser_agent.py"
        )
        intent_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(intent_module)
        
        # Create agent
        IntentParserAgent = intent_module.IntentParserAgent
        agent = IntentParserAgent()
        
        # Parse intent
        intent = agent.parse(args.query)
        
        # Display intent
        print(agent.format_intent(intent))
        print()
        
        # Route to appropriate agent
        print(f"🔀 Routing to: {intent.target_agent}")
        print()
        
        if intent.target_agent == "status":
            # Call status agent
            return cmd_status(type('Args', (), {
                'spec_id': intent.spec_id or 'unknown',
                'query': intent.context.get('question', '')
            }))
        
        elif intent.target_agent == "orchestrator":
            # Call orchestrator
            return cmd_run(type('Args', (), {
                'spec_id': intent.spec_id or 'unknown',
                'auto': False
            }))
        
        else:
            print(f"⚠️  Agent '{intent.target_agent}' not yet implemented.")
            print(f"Coming in Phase 2 or 3!")
            return 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
