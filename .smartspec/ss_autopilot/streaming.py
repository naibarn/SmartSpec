"""
Streaming Module - Real-time progress updates

Provides:
- Progress streaming for workflows
- Real-time status updates
- Event broadcasting
- WebSocket support (future)

Author: SmartSpec Team
Date: 2025-12-26
Version: 1.0.0
"""

import time
import json
from typing import Dict, Any, Optional, Callable, Iterator
from dataclasses import dataclass, asdict
from datetime import datetime
import threading
from queue import Queue, Empty

from .error_handler import with_error_handling
from .advanced_logger import get_logger


@dataclass
class ProgressEvent:
    """Progress event data"""
    event_type: str  # "start", "progress", "complete", "error"
    workflow_id: str
    thread_id: str
    step: str
    progress: float  # 0.0 to 1.0
    message: str
    timestamp: float
    metadata: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict())


class ProgressStreamer:
    """
    Streams progress updates for workflows.
    
    Features:
    - Real-time progress updates
    - Event broadcasting
    - Multiple subscribers
    - Thread-safe operations
    """
    
    def __init__(self):
        """Initialize progress streamer"""
        self.logger = get_logger("progress_streamer")
        self.subscribers: Dict[str, Queue] = {}
        self._lock = threading.Lock()
        
        self.logger.info("ProgressStreamer initialized")
    
    @with_error_handling
    def subscribe(self, subscriber_id: str) -> Queue:
        """
        Subscribe to progress updates.
        
        Args:
            subscriber_id: Unique subscriber ID
            
        Returns:
            Queue for receiving events
        """
        with self._lock:
            if subscriber_id in self.subscribers:
                self.logger.warning(f"Subscriber {subscriber_id} already exists")
                return self.subscribers[subscriber_id]
            
            queue = Queue(maxsize=1000)
            self.subscribers[subscriber_id] = queue
            
            self.logger.info(f"Subscriber {subscriber_id} subscribed")
            
            return queue
    
    @with_error_handling
    def unsubscribe(self, subscriber_id: str):
        """
        Unsubscribe from progress updates.
        
        Args:
            subscriber_id: Subscriber ID
        """
        with self._lock:
            if subscriber_id in self.subscribers:
                del self.subscribers[subscriber_id]
                self.logger.info(f"Subscriber {subscriber_id} unsubscribed")
    
    @with_error_handling
    def publish(self, event: ProgressEvent):
        """
        Publish progress event to all subscribers.
        
        Args:
            event: Progress event
        """
        with self._lock:
            for subscriber_id, queue in self.subscribers.items():
                try:
                    queue.put_nowait(event)
                except:
                    self.logger.warning(f"Failed to publish to {subscriber_id}")
            
            self.logger.debug(
                "Event published",
                event_type=event.event_type,
                workflow_id=event.workflow_id,
                step=event.step
            )
    
    @with_error_handling
    def stream_events(
        self,
        subscriber_id: str,
        timeout: float = 1.0
    ) -> Iterator[ProgressEvent]:
        """
        Stream events for a subscriber.
        
        Args:
            subscriber_id: Subscriber ID
            timeout: Timeout for each event
            
        Yields:
            Progress events
        """
        queue = self.subscribe(subscriber_id)
        
        try:
            while True:
                try:
                    event = queue.get(timeout=timeout)
                    yield event
                    
                    # Stop on complete or error
                    if event.event_type in ["complete", "error"]:
                        break
                        
                except Empty:
                    continue
                    
        finally:
            self.unsubscribe(subscriber_id)


# ============================================================================
# Global Streamer Instance
# ============================================================================

_streamer = ProgressStreamer()


def get_streamer() -> ProgressStreamer:
    """Get global progress streamer instance"""
    return _streamer


# ============================================================================
# Workflow Progress Tracker
# ============================================================================

class WorkflowProgressTracker:
    """
    Tracks and streams workflow progress.
    
    Features:
    - Automatic progress calculation
    - Step tracking
    - Time estimation
    - Event publishing
    """
    
    def __init__(
        self,
        workflow_id: str,
        thread_id: str,
        total_steps: int,
        streamer: Optional[ProgressStreamer] = None
    ):
        """
        Initialize progress tracker.
        
        Args:
            workflow_id: Workflow ID
            thread_id: Thread ID
            total_steps: Total number of steps
            streamer: Progress streamer (optional)
        """
        self.workflow_id = workflow_id
        self.thread_id = thread_id
        self.total_steps = total_steps
        self.current_step = 0  # int - for counting
        self.current_step_name = ""  # str - for display
        self.streamer = streamer or get_streamer()
        self.start_time = time.time()
        
        self.logger = get_logger("workflow_progress_tracker")
        
        # Publish start event
        self._publish_event("start", "Workflow started", 0.0)
    
    def _publish_event(
        self,
        event_type: str,
        message: str,
        progress: float,
        step: str = "",
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Publish progress event"""
        event = ProgressEvent(
            event_type=event_type,
            workflow_id=self.workflow_id,
            thread_id=self.thread_id,
            step=step,
            progress=progress,
            message=message,
            timestamp=time.time(),
            metadata=metadata
        )
        
        self.streamer.publish(event)
    
    @with_error_handling
    def start_step(self, step_name: str):
        """
        Mark step as started.
        
        Args:
            step_name: Step name
        """
        self.current_step += 1
        self.current_step_name = step_name
        progress = self.current_step / self.total_steps
        
        self._publish_event(
            "progress",
            f"Starting step: {step_name}",
            progress,
            step=step_name
        )
        
        self.logger.info(
            f"Step {self.current_step}/{self.total_steps} started",
            step=step_name,
            progress=f"{progress*100:.1f}%"
        )
    
    @with_error_handling
    def complete_step(self, step_name: str, result: Any = None):
        """
        Mark step as completed.
        
        Args:
            step_name: Step name
            result: Step result (optional)
        """
        progress = self.current_step / self.total_steps
        
        metadata = {}
        if result:
            metadata["result"] = str(result)[:100]  # Truncate
        
        self._publish_event(
            "progress",
            f"Completed step: {step_name}",
            progress,
            step=step_name,
            metadata=metadata
        )
        
        self.logger.info(
            f"Step {self.current_step}/{self.total_steps} completed",
            step=step_name,
            progress=f"{progress*100:.1f}%"
        )
    
    @with_error_handling
    def complete_workflow(self, message: str = "Workflow completed"):
        """
        Mark workflow as completed.
        
        Args:
            message: Completion message
        """
        elapsed = time.time() - self.start_time
        
        metadata = {
            "elapsed_time": elapsed,
            "total_steps": self.total_steps
        }
        
        self._publish_event(
            "complete",
            message,
            1.0,
            metadata=metadata
        )
        
        self.logger.info(
            "Workflow completed",
            workflow_id=self.workflow_id,
            elapsed=f"{elapsed:.2f}s"
        )
    
    @with_error_handling
    def fail_workflow(self, error: str):
        """
        Mark workflow as failed.
        
        Args:
            error: Error message
        """
        progress = self.current_step / self.total_steps
        
        metadata = {
            "error": error,
            "failed_at_step": self.current_step
        }
        
        self._publish_event(
            "error",
            f"Workflow failed: {error}",
            progress,
            metadata=metadata
        )
        
        self.logger.error(
            "Workflow failed",
            workflow_id=self.workflow_id,
            error=error
        )


# Export all
__all__ = [
    'ProgressEvent',
    'ProgressStreamer',
    'WorkflowProgressTracker',
    'get_streamer',
]
