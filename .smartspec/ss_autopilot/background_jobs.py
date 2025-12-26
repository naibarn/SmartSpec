"""
Background Jobs - Async workflow execution

Provides:
- Background job execution
- Job queue management
- Job status tracking
- Async workflow execution

Author: SmartSpec Team
Date: 2025-12-26
Version: 1.0.0
"""

import threading
import time
import uuid
from typing import Dict, Any, Optional, Callable, List
from dataclasses import dataclass, asdict
from datetime import datetime
from queue import Queue, Empty
from enum import Enum

from .error_handler import with_error_handling
from .advanced_logger import get_logger
from .checkpoint_manager import CheckpointManager
from .streaming import WorkflowProgressTracker, get_streamer


class JobStatus(Enum):
    """Job status enum"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Job:
    """Background job data"""
    job_id: str
    workflow_id: str
    thread_id: str
    func: Callable
    args: tuple
    kwargs: dict
    status: JobStatus
    created_at: float
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    result: Any = None
    error: Optional[str] = None
    progress: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary (without func)"""
        return {
            "job_id": self.job_id,
            "workflow_id": self.workflow_id,
            "thread_id": self.thread_id,
            "status": self.status.value,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "result": str(self.result)[:100] if self.result else None,
            "error": self.error,
            "progress": self.progress
        }


class BackgroundJobExecutor:
    """
    Executes workflows in background threads.
    
    Features:
    - Job queue management
    - Worker thread pool
    - Job status tracking
    - Progress monitoring
    """
    
    def __init__(
        self,
        num_workers: int = 2,
        checkpoint_manager: Optional[CheckpointManager] = None
    ):
        """
        Initialize background job executor.
        
        Args:
            num_workers: Number of worker threads
            checkpoint_manager: Checkpoint manager (optional)
        """
        self.logger = get_logger("background_jobs")
        self.num_workers = num_workers
        self.checkpoint_manager = checkpoint_manager or CheckpointManager()
        
        # Job queue and storage
        self.job_queue: Queue = Queue()
        self.jobs: Dict[str, Job] = {}
        self._lock = threading.Lock()
        
        # Worker threads
        self.workers: List[threading.Thread] = []
        self.running = False
        
        self.logger.info(f"BackgroundJobExecutor initialized with {num_workers} workers")
    
    def start(self):
        """Start worker threads"""
        if self.running:
            self.logger.warning("Executor already running")
            return
        
        self.running = True
        
        for i in range(self.num_workers):
            worker = threading.Thread(
                target=self._worker_loop,
                name=f"worker-{i}",
                daemon=True
            )
            worker.start()
            self.workers.append(worker)
        
        self.logger.info(f"Started {self.num_workers} worker threads")
    
    def stop(self, timeout: float = 5.0):
        """
        Stop worker threads.
        
        Args:
            timeout: Timeout for each worker
        """
        if not self.running:
            return
        
        self.running = False
        
        for worker in self.workers:
            worker.join(timeout=timeout)
        
        self.workers.clear()
        
        self.logger.info("Stopped all worker threads")
    
    def _worker_loop(self):
        """Worker thread main loop"""
        worker_name = threading.current_thread().name
        self.logger.info(f"{worker_name} started")
        
        while self.running:
            try:
                # Get job from queue (with timeout)
                try:
                    job = self.job_queue.get(timeout=1.0)
                except Empty:
                    continue
                
                # Execute job
                self._execute_job(job)
                
            except Exception as e:
                self.logger.error(f"{worker_name} error: {str(e)}")
        
        self.logger.info(f"{worker_name} stopped")
    
    def _execute_job(self, job: Job):
        """
        Execute a job.
        
        Args:
            job: Job to execute
        """
        job_id = job.job_id
        
        try:
            # Update status
            job.status = JobStatus.RUNNING
            job.started_at = time.time()
            
            self.logger.info(f"Executing job {job_id}")
            
            # Save checkpoint
            self.checkpoint_manager.save_checkpoint(
                workflow_id=job.workflow_id,
                thread_id=job.thread_id,
                state={"job_id": job_id},
                step="JOB_START",
                status="running"
            )
            
            # Execute function
            result = job.func(*job.args, **job.kwargs)
            
            # Update status
            job.status = JobStatus.COMPLETED
            job.completed_at = time.time()
            job.result = result
            job.progress = 1.0
            
            # Save checkpoint
            self.checkpoint_manager.save_checkpoint(
                workflow_id=job.workflow_id,
                thread_id=job.thread_id,
                state={"job_id": job_id, "result": str(result)[:100]},
                step="JOB_COMPLETE",
                status="completed"
            )
            
            self.logger.info(f"Job {job_id} completed")
            
        except Exception as e:
            # Update status
            job.status = JobStatus.FAILED
            job.completed_at = time.time()
            job.error = str(e)
            
            # Save checkpoint
            self.checkpoint_manager.save_checkpoint(
                workflow_id=job.workflow_id,
                thread_id=job.thread_id,
                state={"job_id": job_id},
                step="JOB_FAILED",
                status="failed",
                error=str(e)
            )
            
            self.logger.error(f"Job {job_id} failed: {str(e)}")
    
    @with_error_handling
    def submit_job(
        self,
        func: Callable,
        args: tuple = (),
        kwargs: dict = None,
        workflow_id: Optional[str] = None,
        thread_id: Optional[str] = None
    ) -> str:
        """
        Submit a job for background execution.
        
        Args:
            func: Function to execute
            args: Function arguments
            kwargs: Function keyword arguments
            workflow_id: Workflow ID (optional)
            thread_id: Thread ID (optional)
            
        Returns:
            Job ID
        """
        job_id = str(uuid.uuid4())
        workflow_id = workflow_id or f"workflow-{job_id}"
        thread_id = thread_id or f"thread-{job_id}"
        kwargs = kwargs or {}
        
        job = Job(
            job_id=job_id,
            workflow_id=workflow_id,
            thread_id=thread_id,
            func=func,
            args=args,
            kwargs=kwargs,
            status=JobStatus.PENDING,
            created_at=time.time()
        )
        
        with self._lock:
            self.jobs[job_id] = job
        
        self.job_queue.put(job)
        
        self.logger.info(f"Job {job_id} submitted")
        
        return job_id
    
    @with_error_handling
    def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """
        Get job status.
        
        Args:
            job_id: Job ID
            
        Returns:
            Job status dict or None
        """
        with self._lock:
            job = self.jobs.get(job_id)
            if not job:
                return None
            return job.to_dict()
    
    @with_error_handling
    def wait_for_job(self, job_id: str, timeout: Optional[float] = None) -> Optional[Any]:
        """
        Wait for job to complete.
        
        Args:
            job_id: Job ID
            timeout: Timeout in seconds (None = wait forever)
            
        Returns:
            Job result or None
        """
        start_time = time.time()
        
        while True:
            with self._lock:
                job = self.jobs.get(job_id)
                if not job:
                    return None
                
                if job.status == JobStatus.COMPLETED:
                    return job.result
                
                if job.status == JobStatus.FAILED:
                    raise RuntimeError(f"Job failed: {job.error}")
                
                if job.status == JobStatus.CANCELLED:
                    return None
            
            # Check timeout
            if timeout and (time.time() - start_time) > timeout:
                raise TimeoutError(f"Job {job_id} timeout after {timeout}s")
            
            time.sleep(0.1)
    
    @with_error_handling
    def cancel_job(self, job_id: str) -> bool:
        """
        Cancel a job.
        
        Args:
            job_id: Job ID
            
        Returns:
            True if cancelled, False if not found or already running
        """
        with self._lock:
            job = self.jobs.get(job_id)
            if not job:
                return False
            
            if job.status == JobStatus.PENDING:
                job.status = JobStatus.CANCELLED
                self.logger.info(f"Job {job_id} cancelled")
                return True
            
            return False
    
    @with_error_handling
    def list_jobs(
        self,
        status: Optional[JobStatus] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        List jobs.
        
        Args:
            status: Filter by status (optional)
            limit: Maximum number of results
            
        Returns:
            List of job status dicts
        """
        with self._lock:
            jobs = list(self.jobs.values())
        
        if status:
            jobs = [j for j in jobs if j.status == status]
        
        jobs.sort(key=lambda j: j.created_at, reverse=True)
        jobs = jobs[:limit]
        
        return [j.to_dict() for j in jobs]


# ============================================================================
# Global Executor Instance
# ============================================================================

_executor: Optional[BackgroundJobExecutor] = None
_executor_lock = threading.Lock()


def get_executor(num_workers: int = 2) -> BackgroundJobExecutor:
    """
    Get global background job executor.
    
    Args:
        num_workers: Number of worker threads
        
    Returns:
        BackgroundJobExecutor instance
    """
    global _executor
    
    with _executor_lock:
        if _executor is None:
            _executor = BackgroundJobExecutor(num_workers=num_workers)
            _executor.start()
        
        return _executor


def shutdown_executor(timeout: float = 5.0):
    """
    Shutdown global executor.
    
    Args:
        timeout: Timeout for workers
    """
    global _executor
    
    with _executor_lock:
        if _executor:
            _executor.stop(timeout=timeout)
            _executor = None


# Export all
__all__ = [
    'JobStatus',
    'Job',
    'BackgroundJobExecutor',
    'get_executor',
    'shutdown_executor',
]
