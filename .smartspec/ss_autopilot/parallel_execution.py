"""
Parallel Execution - LangGraph parallel task processing

Provides:
- Parallel task execution using LangGraph Send API
- Dynamic task spawning
- Result aggregation
- Error handling for parallel tasks
- Progress tracking

Author: SmartSpec Team
Date: 2025-12-26
Version: 1.0.0
"""

import time
from typing import Dict, Any, List, Callable, Optional
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

from langgraph.types import Send

from .error_handler import with_error_handling
from .advanced_logger import get_logger
from .streaming import ProgressEvent, get_streamer


@dataclass
class ParallelTask:
    """Parallel task data"""
    task_id: str
    task_type: str
    input_data: Dict[str, Any]
    status: str = "pending"  # pending, running, completed, failed
    result: Any = None
    error: Optional[str] = None
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "task_id": self.task_id,
            "task_type": self.task_type,
            "input_data": self.input_data,
            "status": self.status,
            "result": str(self.result)[:100] if self.result else None,
            "error": self.error,
            "started_at": self.started_at,
            "completed_at": self.completed_at
        }


@dataclass
class ParallelExecutionResult:
    """Result of parallel execution"""
    total_tasks: int
    completed_tasks: int
    failed_tasks: int
    results: List[Any]
    errors: List[str]
    execution_time: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "total_tasks": self.total_tasks,
            "completed_tasks": self.completed_tasks,
            "failed_tasks": self.failed_tasks,
            "results": [str(r)[:100] for r in self.results],
            "errors": self.errors,
            "execution_time": self.execution_time,
            "success_rate": self.completed_tasks / self.total_tasks if self.total_tasks > 0 else 0
        }


class ParallelExecutor:
    """
    Executes tasks in parallel using ThreadPoolExecutor.
    
    Features:
    - Parallel task execution
    - Result aggregation
    - Error handling
    - Progress tracking
    - Thread-safe operations
    """
    
    def __init__(self, max_workers: int = 4):
        """
        Initialize parallel executor.
        
        Args:
            max_workers: Maximum number of worker threads
        """
        self.logger = get_logger("parallel_executor")
        self.max_workers = max_workers
        self.tasks: Dict[str, ParallelTask] = {}
        self._lock = threading.Lock()
        
        self.logger.info(f"ParallelExecutor initialized with {max_workers} workers")
    
    @with_error_handling
    def execute_parallel(
        self,
        tasks: List[ParallelTask],
        task_func: Callable[[ParallelTask], Any],
        workflow_id: Optional[str] = None,
        thread_id: Optional[str] = None
    ) -> ParallelExecutionResult:
        """
        Execute tasks in parallel.
        
        Args:
            tasks: List of tasks to execute
            task_func: Function to execute for each task
            workflow_id: Workflow ID for progress tracking
            thread_id: Thread ID for progress tracking
            
        Returns:
            ParallelExecutionResult
        """
        start_time = time.time()
        
        # Store tasks
        with self._lock:
            for task in tasks:
                self.tasks[task.task_id] = task
        
        self.logger.info(f"Executing {len(tasks)} tasks in parallel")
        
        results = []
        errors = []
        completed = 0
        failed = 0
        
        # Execute tasks in parallel
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_task = {
                executor.submit(self._execute_task, task, task_func): task
                for task in tasks
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_task):
                task = future_to_task[future]
                
                try:
                    result = future.result()
                    
                    # Update task status
                    with self._lock:
                        task.status = "completed"
                        task.result = result
                        task.completed_at = time.time()
                    
                    results.append(result)
                    completed += 1
                    
                    self.logger.info(f"Task {task.task_id} completed")
                    
                except Exception as e:
                    # Update task status
                    with self._lock:
                        task.status = "failed"
                        task.error = str(e)
                        task.completed_at = time.time()
                    
                    errors.append(str(e))
                    failed += 1
                    
                    self.logger.error(f"Task {task.task_id} failed: {str(e)}")
                
                # Publish progress event
                if workflow_id and thread_id:
                    progress = (completed + failed) / len(tasks)
                    event = ProgressEvent(
                        event_type="progress",
                        workflow_id=workflow_id,
                        thread_id=thread_id,
                        step="PARALLEL_EXECUTION",
                        progress=progress,
                        message=f"Completed {completed + failed}/{len(tasks)} tasks",
                        timestamp=time.time()
                    )
                    get_streamer().publish(event)
        
        execution_time = time.time() - start_time
        
        result = ParallelExecutionResult(
            total_tasks=len(tasks),
            completed_tasks=completed,
            failed_tasks=failed,
            results=results,
            errors=errors,
            execution_time=execution_time
        )
        
        self.logger.info(
            f"Parallel execution complete: {completed}/{len(tasks)} succeeded, {failed} failed, {execution_time:.2f}s"
        )
        
        return result
    
    def _execute_task(self, task: ParallelTask, task_func: Callable) -> Any:
        """
        Execute a single task.
        
        Args:
            task: Task to execute
            task_func: Function to execute
            
        Returns:
            Task result
        """
        # Update status
        with self._lock:
            task.status = "running"
            task.started_at = time.time()
        
        # Execute function
        result = task_func(task)
        
        return result
    
    @with_error_handling
    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """
        Get task status.
        
        Args:
            task_id: Task ID
            
        Returns:
            Task status dict or None
        """
        with self._lock:
            task = self.tasks.get(task_id)
            if not task:
                return None
            return task.to_dict()


# ============================================================================
# LangGraph Integration
# ============================================================================

def create_parallel_tasks(
    task_type: str,
    inputs: List[Dict[str, Any]]
) -> List[Send]:
    """
    Create parallel tasks for LangGraph Send API.
    
    Args:
        task_type: Type of task (node name)
        inputs: List of input data for each task
        
    Returns:
        List of Send objects
    """
    sends = []
    
    for i, input_data in enumerate(inputs):
        # Create Send object for each task
        send = Send(
            node=task_type,
            arg=input_data
        )
        sends.append(send)
    
    return sends


def aggregate_parallel_results(
    results: List[Dict[str, Any]],
    aggregation_func: Optional[Callable] = None
) -> Dict[str, Any]:
    """
    Aggregate results from parallel tasks.
    
    Args:
        results: List of results from parallel tasks
        aggregation_func: Custom aggregation function (optional)
        
    Returns:
        Aggregated result
    """
    if aggregation_func:
        return aggregation_func(results)
    
    # Default aggregation: collect all results
    return {
        "total_results": len(results),
        "results": results,
        "success_count": sum(1 for r in results if r.get("success", True)),
        "failure_count": sum(1 for r in results if not r.get("success", True))
    }


# ============================================================================
# Example: Parallel Spec Generation
# ============================================================================

def parallel_spec_generation_example(spec_ids: List[str]) -> ParallelExecutionResult:
    """
    Example: Generate multiple specs in parallel.
    
    Args:
        spec_ids: List of spec IDs to generate
        
    Returns:
        ParallelExecutionResult
    """
    # Create tasks
    tasks = [
        ParallelTask(
            task_id=f"task-{i}",
            task_type="SPEC_GENERATION",
            input_data={"spec_id": spec_id}
        )
        for i, spec_id in enumerate(spec_ids)
    ]
    
    # Define task function
    def generate_spec(task: ParallelTask) -> Dict[str, Any]:
        spec_id = task.input_data["spec_id"]
        
        # Simulate spec generation
        time.sleep(0.5)  # Simulate work
        
        return {
            "spec_id": spec_id,
            "status": "generated",
            "content": f"Spec content for {spec_id}"
        }
    
    # Execute in parallel
    executor = ParallelExecutor(max_workers=4)
    result = executor.execute_parallel(
        tasks=tasks,
        task_func=generate_spec,
        workflow_id="parallel-spec-gen",
        thread_id="thread-123"
    )
    
    return result


# ============================================================================
# Example: Parallel Task Implementation
# ============================================================================

def parallel_task_implementation_example(tasks: List[Dict[str, Any]]) -> ParallelExecutionResult:
    """
    Example: Implement multiple tasks in parallel.
    
    Args:
        tasks: List of task definitions
        
    Returns:
        ParallelExecutionResult
    """
    # Create parallel tasks
    parallel_tasks = [
        ParallelTask(
            task_id=f"task-{i}",
            task_type="TASK_IMPLEMENTATION",
            input_data=task
        )
        for i, task in enumerate(tasks)
    ]
    
    # Define task function
    def implement_task(task: ParallelTask) -> Dict[str, Any]:
        task_data = task.input_data
        
        # Simulate task implementation
        time.sleep(1.0)  # Simulate work
        
        return {
            "task_id": task_data.get("id"),
            "status": "implemented",
            "code": f"# Code for task {task_data.get('id')}"
        }
    
    # Execute in parallel
    executor = ParallelExecutor(max_workers=4)
    result = executor.execute_parallel(
        tasks=parallel_tasks,
        task_func=implement_task,
        workflow_id="parallel-task-impl",
        thread_id="thread-456"
    )
    
    return result


# ============================================================================
# Global Executor Instance
# ============================================================================

_executor: Optional[ParallelExecutor] = None
_executor_lock = threading.Lock()


def get_parallel_executor(max_workers: int = 4) -> ParallelExecutor:
    """
    Get global parallel executor.
    
    Args:
        max_workers: Maximum number of worker threads
        
    Returns:
        ParallelExecutor instance
    """
    global _executor
    
    with _executor_lock:
        if _executor is None:
            _executor = ParallelExecutor(max_workers=max_workers)
        
        return _executor


# Export all
__all__ = [
    'ParallelTask',
    'ParallelExecutionResult',
    'ParallelExecutor',
    'create_parallel_tasks',
    'aggregate_parallel_results',
    'get_parallel_executor',
    'parallel_spec_generation_example',
    'parallel_task_implementation_example',
]
