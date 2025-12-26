"""
Human-in-the-Loop - Interactive workflow control

Provides:
- Human approval checkpoints
- User input collection
- Workflow pause/resume
- Decision points
- LangGraph interrupt integration

Author: SmartSpec Team
Date: 2025-12-26
Version: 1.0.0
"""

import time
from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import threading
from queue import Queue, Empty

from langgraph.types import interrupt

from .error_handler import with_error_handling
from .advanced_logger import get_logger
from .streaming import ProgressEvent, get_streamer


class InterruptType(Enum):
    """Type of interrupt"""
    APPROVAL = "approval"  # Requires approval to continue
    INPUT = "input"  # Requires user input
    DECISION = "decision"  # Requires user decision
    REVIEW = "review"  # Requires user review


@dataclass
class HumanInterrupt:
    """Human interrupt data"""
    interrupt_id: str
    interrupt_type: InterruptType
    workflow_id: str
    thread_id: str
    step: str
    message: str
    context: Dict[str, Any]
    options: Optional[List[str]] = None  # For decisions
    created_at: float = field(default_factory=time.time)
    resolved_at: Optional[float] = None
    response: Any = None
    status: str = "pending"  # pending, resolved, cancelled
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "interrupt_id": self.interrupt_id,
            "interrupt_type": self.interrupt_type.value,
            "workflow_id": self.workflow_id,
            "thread_id": self.thread_id,
            "step": self.step,
            "message": self.message,
            "context": self.context,
            "options": self.options,
            "created_at": self.created_at,
            "resolved_at": self.resolved_at,
            "response": self.response,
            "status": self.status
        }


class HumanInterruptManager:
    """
    Manages human interrupts in workflows.
    
    Features:
    - Create interrupts
    - Wait for responses
    - Resolve interrupts
    - Track interrupt history
    """
    
    def __init__(self):
        """Initialize interrupt manager"""
        self.logger = get_logger("human_interrupt_manager")
        self.interrupts: Dict[str, HumanInterrupt] = {}
        self.response_queues: Dict[str, Queue] = {}
        self._lock = threading.Lock()
        
        self.logger.info("HumanInterruptManager initialized")
    
    @with_error_handling
    def create_interrupt(
        self,
        interrupt_type: InterruptType,
        workflow_id: str,
        thread_id: str,
        step: str,
        message: str,
        context: Dict[str, Any],
        options: Optional[List[str]] = None
    ) -> str:
        """
        Create a human interrupt.
        
        Args:
            interrupt_type: Type of interrupt
            workflow_id: Workflow ID
            thread_id: Thread ID
            step: Current step
            message: Message to show user
            context: Additional context
            options: Options for decisions
            
        Returns:
            Interrupt ID
        """
        interrupt_id = f"{workflow_id}_{thread_id}_{int(time.time() * 1000)}"
        
        interrupt = HumanInterrupt(
            interrupt_id=interrupt_id,
            interrupt_type=interrupt_type,
            workflow_id=workflow_id,
            thread_id=thread_id,
            step=step,
            message=message,
            context=context,
            options=options
        )
        
        with self._lock:
            self.interrupts[interrupt_id] = interrupt
            self.response_queues[interrupt_id] = Queue()
        
        # Publish event
        event = ProgressEvent(
            event_type="progress",
            workflow_id=workflow_id,
            thread_id=thread_id,
            step=step,
            progress=0.0,
            message=f"Waiting for human input: {message}",
            timestamp=time.time(),
            metadata={"interrupt_id": interrupt_id, "interrupt_type": interrupt_type.value}
        )
        get_streamer().publish(event)
        
        self.logger.info(
            f"Interrupt created: {interrupt_id}",
            type=interrupt_type.value,
            user_message=message
        )
        
        return interrupt_id
    
    @with_error_handling
    def wait_for_response(
        self,
        interrupt_id: str,
        timeout: Optional[float] = None
    ) -> Any:
        """
        Wait for user response to interrupt.
        
        Args:
            interrupt_id: Interrupt ID
            timeout: Timeout in seconds (None = wait forever)
            
        Returns:
            User response
            
        Raises:
            TimeoutError: If timeout exceeded
        """
        with self._lock:
            if interrupt_id not in self.response_queues:
                raise ValueError(f"Interrupt {interrupt_id} not found")
            
            queue = self.response_queues[interrupt_id]
        
        self.logger.info(f"Waiting for response to interrupt {interrupt_id}")
        
        try:
            response = queue.get(timeout=timeout)
            
            self.logger.info(f"Received response for interrupt {interrupt_id}")
            
            return response
            
        except Empty:
            raise TimeoutError(f"Timeout waiting for response to interrupt {interrupt_id}")
    
    @with_error_handling
    def resolve_interrupt(
        self,
        interrupt_id: str,
        response: Any
    ) -> bool:
        """
        Resolve an interrupt with user response.
        
        Args:
            interrupt_id: Interrupt ID
            response: User response
            
        Returns:
            True if resolved, False if not found
        """
        with self._lock:
            if interrupt_id not in self.interrupts:
                return False
            
            interrupt = self.interrupts[interrupt_id]
            queue = self.response_queues[interrupt_id]
            
            # Update interrupt
            interrupt.response = response
            interrupt.resolved_at = time.time()
            interrupt.status = "resolved"
            
            # Send response to waiting thread
            queue.put(response)
        
        # Publish event
        event = ProgressEvent(
            event_type="progress",
            workflow_id=interrupt.workflow_id,
            thread_id=interrupt.thread_id,
            step=interrupt.step,
            progress=1.0,
            message=f"Interrupt resolved: {interrupt.message}",
            timestamp=time.time(),
            metadata={"interrupt_id": interrupt_id, "response": str(response)[:100]}
        )
        get_streamer().publish(event)
        
        self.logger.info(
            f"Interrupt resolved: {interrupt_id}",
            response=str(response)[:100]
        )
        
        return True
    
    @with_error_handling
    def cancel_interrupt(self, interrupt_id: str) -> bool:
        """
        Cancel an interrupt.
        
        Args:
            interrupt_id: Interrupt ID
            
        Returns:
            True if cancelled, False if not found
        """
        with self._lock:
            if interrupt_id not in self.interrupts:
                return False
            
            interrupt = self.interrupts[interrupt_id]
            
            interrupt.status = "cancelled"
            interrupt.resolved_at = time.time()
        
        self.logger.info(f"Interrupt cancelled: {interrupt_id}")
        
        return True
    
    @with_error_handling
    def get_interrupt(self, interrupt_id: str) -> Optional[Dict[str, Any]]:
        """
        Get interrupt details.
        
        Args:
            interrupt_id: Interrupt ID
            
        Returns:
            Interrupt dict or None
        """
        with self._lock:
            interrupt = self.interrupts.get(interrupt_id)
            if not interrupt:
                return None
            return interrupt.to_dict()
    
    @with_error_handling
    def list_pending_interrupts(
        self,
        workflow_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        List pending interrupts.
        
        Args:
            workflow_id: Filter by workflow ID (optional)
            
        Returns:
            List of interrupt dicts
        """
        with self._lock:
            interrupts = [
                i for i in self.interrupts.values()
                if i.status == "pending"
            ]
            
            if workflow_id:
                interrupts = [i for i in interrupts if i.workflow_id == workflow_id]
            
            return [i.to_dict() for i in interrupts]


# ============================================================================
# Convenience Functions
# ============================================================================

@with_error_handling
def request_approval(
    workflow_id: str,
    thread_id: str,
    step: str,
    message: str,
    context: Dict[str, Any],
    timeout: Optional[float] = None
) -> bool:
    """
    Request human approval to continue.
    
    Args:
        workflow_id: Workflow ID
        thread_id: Thread ID
        step: Current step
        message: Approval message
        context: Additional context
        timeout: Timeout in seconds
        
    Returns:
        True if approved, False if rejected
        
    Example:
        >>> approved = request_approval(
        ...     "spec-001",
        ...     "thread-123",
        ...     "DEPLOY",
        ...     "Deploy to production?",
        ...     {"environment": "production"}
        ... )
    """
    manager = get_interrupt_manager()
    
    interrupt_id = manager.create_interrupt(
        interrupt_type=InterruptType.APPROVAL,
        workflow_id=workflow_id,
        thread_id=thread_id,
        step=step,
        message=message,
        context=context
    )
    
    response = manager.wait_for_response(interrupt_id, timeout=timeout)
    
    return bool(response)


@with_error_handling
def request_input(
    workflow_id: str,
    thread_id: str,
    step: str,
    message: str,
    context: Dict[str, Any],
    timeout: Optional[float] = None
) -> Any:
    """
    Request input from user.
    
    Args:
        workflow_id: Workflow ID
        thread_id: Thread ID
        step: Current step
        message: Input prompt
        context: Additional context
        timeout: Timeout in seconds
        
    Returns:
        User input
        
    Example:
        >>> spec_name = request_input(
        ...     "spec-001",
        ...     "thread-123",
        ...     "SPEC",
        ...     "Enter spec name:",
        ...     {}
        ... )
    """
    manager = get_interrupt_manager()
    
    interrupt_id = manager.create_interrupt(
        interrupt_type=InterruptType.INPUT,
        workflow_id=workflow_id,
        thread_id=thread_id,
        step=step,
        message=message,
        context=context
    )
    
    response = manager.wait_for_response(interrupt_id, timeout=timeout)
    
    return response


@with_error_handling
def request_decision(
    workflow_id: str,
    thread_id: str,
    step: str,
    message: str,
    options: List[str],
    context: Dict[str, Any],
    timeout: Optional[float] = None
) -> str:
    """
    Request decision from user.
    
    Args:
        workflow_id: Workflow ID
        thread_id: Thread ID
        step: Current step
        message: Decision prompt
        options: List of options
        context: Additional context
        timeout: Timeout in seconds
        
    Returns:
        Selected option
        
    Example:
        >>> choice = request_decision(
        ...     "spec-001",
        ...     "thread-123",
        ...     "PLAN",
        ...     "Choose deployment strategy:",
        ...     ["blue-green", "canary", "rolling"],
        ...     {}
        ... )
    """
    manager = get_interrupt_manager()
    
    interrupt_id = manager.create_interrupt(
        interrupt_type=InterruptType.DECISION,
        workflow_id=workflow_id,
        thread_id=thread_id,
        step=step,
        message=message,
        context=context,
        options=options
    )
    
    response = manager.wait_for_response(interrupt_id, timeout=timeout)
    
    return str(response)


# ============================================================================
# Global Manager Instance
# ============================================================================

_manager: Optional[HumanInterruptManager] = None
_manager_lock = threading.Lock()


def get_interrupt_manager() -> HumanInterruptManager:
    """Get global interrupt manager instance"""
    global _manager
    
    with _manager_lock:
        if _manager is None:
            _manager = HumanInterruptManager()
        
        return _manager


# Export all
__all__ = [
    'InterruptType',
    'HumanInterrupt',
    'HumanInterruptManager',
    'request_approval',
    'request_input',
    'request_decision',
    'get_interrupt_manager',
]
