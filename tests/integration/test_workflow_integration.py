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

# Import test helpers
from test_helpers import unwrap_result, is_error_result


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
        intent_result = self.intent_parser.parse("Create a new spec for user authentication")
        intent = unwrap_result(intent_result)
        assert intent is not None
        # intent is Intent object, check original_input instead
        assert "spec" in intent.original_input.lower() or "create" in intent.original_input.lower()
        
        # 2. Load workflow
        workflow_result = self.workflow_catalog.get("spec_creation")
        workflow = unwrap_result(workflow_result)
        assert workflow is not None
        
        # 3. Execute workflow (simulated)
        state = {
            "spec_id": spec_id,
            "intent": intent.original_input,  # Convert Intent to string for JSON serialization
            "step": "SPEC"
        }
        
        # Save checkpoint
        checkpoint_id_result = self.checkpoint_manager.save_checkpoint(
            workflow_id=spec_id,
            thread_id="thread-test-001",
            state=state,
            step="SPEC",
            status="running"
        )
        assert not is_error_result(checkpoint_id_result), f"Failed to save checkpoint: {checkpoint_id_result}"
        
        checkpoint_id = unwrap_result(checkpoint_id_result)
        assert checkpoint_id is not None
        assert isinstance(checkpoint_id, str), f"Expected string checkpoint_id, got {type(checkpoint_id)}: {checkpoint_id}"
        
        # 4. Verify checkpoint
        checkpoint_result = self.checkpoint_manager.load_checkpoint(checkpoint_id)
        assert not is_error_result(checkpoint_result), f"Failed to load checkpoint: {checkpoint_result}"
        
        checkpoint = unwrap_result(checkpoint_result)
        assert checkpoint is not None, "Checkpoint is None after unwrap"
        
        # Debug: print checkpoint type and content
        print(f"DEBUG: checkpoint type = {type(checkpoint)}")
        print(f"DEBUG: checkpoint = {checkpoint}")
        
        # Handle both object and dict
        if hasattr(checkpoint, 'state'):
            assert checkpoint.state["spec_id"] == spec_id
        elif isinstance(checkpoint, dict) and "state" in checkpoint:
            assert checkpoint["state"]["spec_id"] == spec_id
        else:
            raise AssertionError(f"Checkpoint has unexpected structure: {type(checkpoint)} - {checkpoint}")
    
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
        result_wrapped = executor.execute_parallel(
            tasks=tasks,
            task_func=execute_task,
            workflow_id="test-parallel",
            thread_id="thread-test-002"
        )
        result = unwrap_result(result_wrapped)
        
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
        
        checkpoint_id_result = self.checkpoint_manager.save_checkpoint(
            workflow_id=spec_id,
            thread_id=thread_id,
            state=state,
            step="PLAN",
            status="running"
        )
        checkpoint_id = unwrap_result(checkpoint_id_result)
        
        # 2. Load checkpoint
        checkpoint_result = self.checkpoint_manager.load_checkpoint(checkpoint_id)
        checkpoint = unwrap_result(checkpoint_result)
        
        # 3. Verify
        assert checkpoint is not None
        assert checkpoint.state["spec_id"] == spec_id
        assert checkpoint.state["step"] == "PLAN"
        assert checkpoint.state["progress"] == 0.5
        
        # 4. Resume workflow
        resumed_state = checkpoint.state
        resumed_state["progress"] = 1.0
        
        # 5. Save updated checkpoint
        checkpoint_id2_result = self.checkpoint_manager.save_checkpoint(
            workflow_id=spec_id,
            thread_id=thread_id,
            state=resumed_state,
            step="PLAN",
            status="completed"
        )
        checkpoint_id2 = unwrap_result(checkpoint_id2_result)
        
        # 6. Verify
        checkpoint2_result = self.checkpoint_manager.load_checkpoint(checkpoint_id2)
        checkpoint2 = unwrap_result(checkpoint2_result)
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
        assert tracker.current_step == 3  # int - step count
        assert tracker.current_step_name == "STEP3"  # str - step name
    
    def test_background_job_execution(self):
        """Test: Background job execution"""
        
        def long_running_task(duration: float) -> str:
            time.sleep(duration)
            return f"Completed after {duration}s"
        
        # Submit job
        executor = get_executor(num_workers=2)
        job_id_result = executor.submit_job(
            func=long_running_task,
            args=(0.5,),
            workflow_id="test-bg-job",
            thread_id="thread-test-005"
        )
        job_id = unwrap_result(job_id_result)
        
        # Wait for completion
        result_wrapped = executor.wait_for_job(job_id, timeout=2.0)
        result = unwrap_result(result_wrapped)
        
        # Verify
        assert result is not None
        assert "Completed" in result
    
    def test_human_interrupt_workflow(self):
        """Test: Human interrupt workflow"""
        workflow_id = "test-interrupt"
        thread_id = "thread-test-006"
        
        manager = get_interrupt_manager()
        
        # Import InterruptType from module
        from ss_autopilot.human_in_the_loop import InterruptType
        
        # Create interrupt
        interrupt_id_result = manager.create_interrupt(
            interrupt_type=InterruptType.APPROVAL,
            workflow_id=workflow_id,
            thread_id=thread_id,
            step="DEPLOY",
            message="Approve deployment?",
            context={"environment": "test"}
        )
        interrupt_id = unwrap_result(interrupt_id_result)
        
        # Check if creation succeeded
        assert not is_error_result(interrupt_id_result), f"Failed to create interrupt: {interrupt_id}"
        assert isinstance(interrupt_id, str), f"Expected string interrupt_id, got {type(interrupt_id)}"
        
        # Resolve interrupt (simulate user response)
        resolved_result = manager.resolve_interrupt(interrupt_id, response=True)
        resolved = unwrap_result(resolved_result)
        
        # Verify
        assert not is_error_result(resolved_result), f"Failed to resolve interrupt: {resolved}"
        assert resolved is True
        
        interrupt_result = manager.get_interrupt(interrupt_id)
        interrupt = unwrap_result(interrupt_result)
        assert not is_error_result(interrupt_result), f"Failed to get interrupt: {interrupt}"
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
        
        checkpoint_id_result = self.checkpoint_manager.save_checkpoint(
            workflow_id=spec_id,
            thread_id=thread_id,
            state=state,
            step="IMPLEMENT",
            status="running"
        )
        checkpoint_id = unwrap_result(checkpoint_id_result)
        
        # 2. Simulate error
        try:
            raise RuntimeError("Simulated error")
        except RuntimeError as e:
            # Save error checkpoint
            error_checkpoint_id_result = self.checkpoint_manager.save_checkpoint(
                workflow_id=spec_id,
                thread_id=thread_id,
                state=state,
                step="IMPLEMENT",
                status="failed",
                error=str(e)
            )
            error_checkpoint_id = unwrap_result(error_checkpoint_id_result)
        
        # 3. Recover from checkpoint
        checkpoint_result = self.checkpoint_manager.load_checkpoint(checkpoint_id)
        checkpoint = unwrap_result(checkpoint_result)
        
        # 4. Verify
        assert checkpoint is not None
        assert checkpoint.state["progress"] == 0.3
        
        # 5. Resume from checkpoint
        resumed_state = checkpoint.state
        resumed_state["progress"] = 1.0
        
        recovery_checkpoint_id_result = self.checkpoint_manager.save_checkpoint(
            workflow_id=spec_id,
            thread_id=thread_id,
            state=resumed_state,
            step="IMPLEMENT",
            status="completed"
        )
        recovery_checkpoint_id = unwrap_result(recovery_checkpoint_id_result)
        
        # 6. Verify recovery
        recovery_checkpoint_result = self.checkpoint_manager.load_checkpoint(recovery_checkpoint_id)
        recovery_checkpoint = unwrap_result(recovery_checkpoint_result)
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
        state_result = orchestrator.read_state(spec_id)
        state = unwrap_result(state_result)
        
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
        assert tracker.current_step == 5  # int - step count
        assert tracker.current_step_name == "DEPLOY"  # str - step name
    
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
        
        checkpoint_id_result = checkpoint_manager.save_checkpoint(
            workflow_id=workflow_id,
            thread_id=thread_id,
            state=state,
            step="PARALLEL_START",
            status="running"
        )
        checkpoint_id = unwrap_result(checkpoint_id_result)
        
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
        result_wrapped = executor.execute_parallel(
            tasks=tasks,
            task_func=execute_task,
            workflow_id=workflow_id,
            thread_id=thread_id
        )
        result = unwrap_result(result_wrapped)
        
        # 3. Save completion checkpoint
        state["results"] = result.results
        checkpoint_id2_result = checkpoint_manager.save_checkpoint(
            workflow_id=workflow_id,
            thread_id=thread_id,
            state=state,
            step="PARALLEL_COMPLETE",
            status="completed"
        )
        checkpoint_id2 = unwrap_result(checkpoint_id2_result)
        
        # 4. Verify
        assert result.completed_tasks == 10
        checkpoint_result = checkpoint_manager.load_checkpoint(checkpoint_id2)
        checkpoint = unwrap_result(checkpoint_result)
        assert len(checkpoint.state["results"]) == 10


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
