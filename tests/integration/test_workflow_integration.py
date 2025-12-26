"""
Integration Tests - Full Workflow Testing

Tests complete workflows from start to finish.

Author: SmartSpec Team
Date: 2025-12-26
"""

import pytest
import time
from typing import Dict, Any

# Import modules to test
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..', '.smartspec'))

from ss_autopilot.orchestrator_agent import OrchestratorAgent
from ss_autopilot.status_agent import StatusAgent
from ss_autopilot.intent_parser_agent import IntentParserAgent
from ss_autopilot.workflow_loader import WorkflowCatalog
from ss_autopilot.checkpoint_manager import CheckpointManager
from ss_autopilot.streaming import WorkflowProgressTracker, get_streamer
from ss_autopilot.background_jobs import get_executor
from ss_autopilot.parallel_execution import ParallelExecutor, ParallelTask
from ss_autopilot.human_in_the_loop import get_interrupt_manager, request_approval


class TestWorkflowIntegration:
    """Integration tests for complete workflows"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup for each test"""
        self.orchestrator = OrchestratorAgent()
        self.status_agent = StatusAgent()
        self.intent_parser = IntentParserAgent()
        self.workflow_catalog = WorkflowCatalog()
        self.checkpoint_manager = CheckpointManager()
        
        yield
        
        # Cleanup
        pass
    
    def test_spec_creation_workflow(self):
        """Test: Create spec workflow"""
        spec_id = "spec-test-001"
        
        # 1. Parse intent
        intent = self.intent_parser.parse("Create a new spec for user authentication")
        assert intent is not None
        assert "spec" in intent.lower() or "create" in intent.lower()
        
        # 2. Load workflow
        workflow = self.workflow_catalog.get("spec_creation")
        assert workflow is not None
        
        # 3. Execute workflow (simulated)
        state = {
            "spec_id": spec_id,
            "intent": intent,
            "step": "SPEC"
        }
        
        # Save checkpoint
        checkpoint_id = self.checkpoint_manager.save_checkpoint(
            workflow_id=spec_id,
            thread_id="thread-test-001",
            state=state,
            step="SPEC",
            status="running"
        )
        
        assert checkpoint_id is not None
        
        # 4. Verify checkpoint
        checkpoint = self.checkpoint_manager.load_checkpoint(checkpoint_id)
        assert checkpoint is not None
        assert checkpoint.state["spec_id"] == spec_id
    
    def test_parallel_task_execution(self):
        """Test: Parallel task execution"""
        # Create tasks
        tasks = [
            ParallelTask(
                task_id=f"task-{i}",
                task_type="TEST_TASK",
                input_data={"value": i}
            )
            for i in range(10)
        ]
        
        # Define task function
        def execute_task(task: ParallelTask) -> Dict[str, Any]:
            value = task.input_data["value"]
            time.sleep(0.1)  # Simulate work
            return {"result": value * 2}
        
        # Execute in parallel
        executor = ParallelExecutor(max_workers=4)
        result = executor.execute_parallel(
            tasks=tasks,
            task_func=execute_task,
            workflow_id="test-parallel",
            thread_id="thread-test-002"
        )
        
        # Verify
        assert result.total_tasks == 10
        assert result.completed_tasks == 10
        assert result.failed_tasks == 0
        assert len(result.results) == 10
    
    def test_checkpoint_resume(self):
        """Test: Resume from checkpoint"""
        spec_id = "spec-test-002"
        thread_id = "thread-test-003"
        
        # 1. Save checkpoint
        state = {
            "spec_id": spec_id,
            "step": "PLAN",
            "progress": 0.5
        }
        
        checkpoint_id = self.checkpoint_manager.save_checkpoint(
            workflow_id=spec_id,
            thread_id=thread_id,
            state=state,
            step="PLAN",
            status="running"
        )
        
        # 2. Load checkpoint
        checkpoint = self.checkpoint_manager.load_checkpoint(checkpoint_id)
        
        # 3. Verify
        assert checkpoint is not None
        assert checkpoint.state["spec_id"] == spec_id
        assert checkpoint.state["step"] == "PLAN"
        assert checkpoint.state["progress"] == 0.5
        
        # 4. Resume workflow
        resumed_state = checkpoint.state
        resumed_state["progress"] = 1.0
        
        # 5. Save updated checkpoint
        checkpoint_id2 = self.checkpoint_manager.save_checkpoint(
            workflow_id=spec_id,
            thread_id=thread_id,
            state=resumed_state,
            step="PLAN",
            status="completed"
        )
        
        # 6. Verify
        checkpoint2 = self.checkpoint_manager.load_checkpoint(checkpoint_id2)
        assert checkpoint2.state["progress"] == 1.0
    
    def test_progress_streaming(self):
        """Test: Progress streaming"""
        workflow_id = "test-streaming"
        thread_id = "thread-test-004"
        
        # Create tracker
        tracker = WorkflowProgressTracker(
            workflow_id=workflow_id,
            thread_id=thread_id,
            total_steps=3
        )
        
        # Track progress
        tracker.start_step("STEP1")
        time.sleep(0.1)
        tracker.complete_step("STEP1")
        
        tracker.start_step("STEP2")
        time.sleep(0.1)
        tracker.complete_step("STEP2")
        
        tracker.start_step("STEP3")
        time.sleep(0.1)
        tracker.complete_step("STEP3")
        
        tracker.complete_workflow()
        
        # Verify (basic check - events were published)
        assert tracker.current_step == "STEP3"
    
    def test_background_job_execution(self):
        """Test: Background job execution"""
        
        def long_running_task(duration: float) -> str:
            time.sleep(duration)
            return f"Completed after {duration}s"
        
        # Submit job
        executor = get_executor(num_workers=2)
        job_id = executor.submit_job(
            func=long_running_task,
            args=(0.5,),
            workflow_id="test-bg-job",
            thread_id="thread-test-005"
        )
        
        # Wait for completion
        result = executor.wait_for_job(job_id, timeout=2.0)
        
        # Verify
        assert result is not None
        assert "Completed" in result
    
    def test_human_interrupt_workflow(self):
        """Test: Human interrupt workflow"""
        workflow_id = "test-interrupt"
        thread_id = "thread-test-006"
        
        manager = get_interrupt_manager()
        
        # Create interrupt
        interrupt_id = manager.create_interrupt(
            interrupt_type=manager.InterruptType.APPROVAL,
            workflow_id=workflow_id,
            thread_id=thread_id,
            step="DEPLOY",
            message="Approve deployment?",
            context={"environment": "test"}
        )
        
        # Resolve interrupt (simulate user response)
        resolved = manager.resolve_interrupt(interrupt_id, response=True)
        
        # Verify
        assert resolved is True
        
        interrupt = manager.get_interrupt(interrupt_id)
        assert interrupt["status"] == "resolved"
        assert interrupt["response"] is True
    
    def test_error_recovery(self):
        """Test: Error recovery with checkpoints"""
        spec_id = "spec-test-003"
        thread_id = "thread-test-007"
        
        # 1. Save checkpoint before error
        state = {
            "spec_id": spec_id,
            "step": "IMPLEMENT",
            "progress": 0.3
        }
        
        checkpoint_id = self.checkpoint_manager.save_checkpoint(
            workflow_id=spec_id,
            thread_id=thread_id,
            state=state,
            step="IMPLEMENT",
            status="running"
        )
        
        # 2. Simulate error
        try:
            raise RuntimeError("Simulated error")
        except RuntimeError as e:
            # Save error checkpoint
            error_checkpoint_id = self.checkpoint_manager.save_checkpoint(
                workflow_id=spec_id,
                thread_id=thread_id,
                state=state,
                step="IMPLEMENT",
                status="failed",
                error=str(e)
            )
        
        # 3. Recover from checkpoint
        checkpoint = self.checkpoint_manager.load_checkpoint(checkpoint_id)
        
        # 4. Verify
        assert checkpoint is not None
        assert checkpoint.state["progress"] == 0.3
        
        # 5. Resume from checkpoint
        resumed_state = checkpoint.state
        resumed_state["progress"] = 1.0
        
        recovery_checkpoint_id = self.checkpoint_manager.save_checkpoint(
            workflow_id=spec_id,
            thread_id=thread_id,
            state=resumed_state,
            step="IMPLEMENT",
            status="completed"
        )
        
        # 6. Verify recovery
        recovery_checkpoint = self.checkpoint_manager.load_checkpoint(recovery_checkpoint_id)
        assert recovery_checkpoint.state["progress"] == 1.0
        assert recovery_checkpoint.status == "completed"


class TestEndToEnd:
    """End-to-end tests for complete user journeys"""
    
    def test_complete_spec_workflow(self):
        """Test: Complete spec creation to deployment"""
        spec_id = "spec-e2e-001"
        thread_id = "thread-e2e-001"
        
        # 1. Create spec
        orchestrator = OrchestratorAgent()
        state = orchestrator.read_state(spec_id)
        
        # 2. Track progress
        tracker = WorkflowProgressTracker(
            workflow_id=spec_id,
            thread_id=thread_id,
            total_steps=5
        )
        
        # 3. Execute steps
        steps = ["SPEC", "PLAN", "IMPLEMENT", "TEST", "DEPLOY"]
        
        for step in steps:
            tracker.start_step(step)
            time.sleep(0.1)  # Simulate work
            tracker.complete_step(step)
        
        tracker.complete_workflow()
        
        # 4. Verify
        assert tracker.current_step == "DEPLOY"
    
    def test_parallel_workflow_with_checkpoints(self):
        """Test: Parallel execution with checkpointing"""
        workflow_id = "parallel-e2e-001"
        thread_id = "thread-e2e-002"
        
        # 1. Save initial checkpoint
        checkpoint_manager = CheckpointManager()
        state = {
            "workflow_id": workflow_id,
            "tasks": list(range(10))
        }
        
        checkpoint_id = checkpoint_manager.save_checkpoint(
            workflow_id=workflow_id,
            thread_id=thread_id,
            state=state,
            step="PARALLEL_START",
            status="running"
        )
        
        # 2. Execute tasks in parallel
        tasks = [
            ParallelTask(
                task_id=f"task-{i}",
                task_type="E2E_TASK",
                input_data={"value": i}
            )
            for i in range(10)
        ]
        
        def execute_task(task: ParallelTask) -> Dict[str, Any]:
            value = task.input_data["value"]
            time.sleep(0.05)
            return {"result": value * 3}
        
        executor = ParallelExecutor(max_workers=4)
        result = executor.execute_parallel(
            tasks=tasks,
            task_func=execute_task,
            workflow_id=workflow_id,
            thread_id=thread_id
        )
        
        # 3. Save completion checkpoint
        state["results"] = result.results
        checkpoint_id2 = checkpoint_manager.save_checkpoint(
            workflow_id=workflow_id,
            thread_id=thread_id,
            state=state,
            step="PARALLEL_COMPLETE",
            status="completed"
        )
        
        # 4. Verify
        assert result.completed_tasks == 10
        checkpoint = checkpoint_manager.load_checkpoint(checkpoint_id2)
        assert len(checkpoint.state["results"]) == 10


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
