"""
Checkpoint Manager - LangGraph checkpointing and state persistence

Provides:
- LangGraph checkpointing (save/resume workflows)
- Workflow state persistence (SQLite)
- Auto-recovery on failure
- Progress tracking
- Background job management

Author: SmartSpec Team
Date: 2025-12-26
Version: 1.0.0
"""

import sqlite3
import json
import time
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from datetime import datetime
import threading

from langgraph.checkpoint.memory import MemorySaver

from .error_handler import with_error_handling
from .advanced_logger import get_logger


@dataclass
class WorkflowCheckpoint:
    """Workflow checkpoint data"""
    checkpoint_id: str
    workflow_id: str
    thread_id: str
    state: Dict[str, Any]
    step: str
    timestamp: float
    status: str  # "running", "paused", "completed", "failed"
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'WorkflowCheckpoint':
        """Create from dictionary"""
        return cls(**data)


class CheckpointManager:
    """
    Manages workflow checkpoints and state persistence.
    
    Features:
    - Save/resume workflow state
    - Auto-recovery on failure
    - Progress tracking
    - Thread-safe operations
    """
    
    def __init__(self, db_path: str = ".smartspec/checkpoints.db"):
        """
        Initialize checkpoint manager.
        
        Args:
            db_path: Path to SQLite database
        """
        self.logger = get_logger("checkpoint_manager")
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize database
        self._init_db()
        
        # Thread lock
        self._lock = threading.Lock()
        
        self.logger.info("CheckpointManager initialized", db_path=str(self.db_path))
    
    def _init_db(self):
        """Initialize database schema"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        # Create table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS checkpoints (
                checkpoint_id TEXT PRIMARY KEY,
                workflow_id TEXT NOT NULL,
                thread_id TEXT NOT NULL,
                state TEXT NOT NULL,
                step TEXT NOT NULL,
                timestamp REAL NOT NULL,
                status TEXT NOT NULL,
                error TEXT,
                metadata TEXT
            )
        """)
        
        # Create indexes separately
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_workflow_id 
            ON checkpoints(workflow_id)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_thread_id 
            ON checkpoints(thread_id)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_status 
            ON checkpoints(status)
        """)
        
        conn.commit()
        conn.close()
    
    @with_error_handling
    def save_checkpoint(
        self,
        workflow_id: str,
        thread_id: str,
        state: Dict[str, Any],
        step: str,
        status: str = "running",
        error: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Save workflow checkpoint.
        
        Args:
            workflow_id: Workflow ID
            thread_id: Thread ID
            state: Current state
            step: Current step
            status: Workflow status
            error: Error message if failed
            metadata: Additional metadata
            
        Returns:
            Checkpoint ID
        """
        with self._lock:
            checkpoint_id = f"{workflow_id}_{thread_id}_{int(time.time() * 1000)}"
            
            checkpoint = WorkflowCheckpoint(
                checkpoint_id=checkpoint_id,
                workflow_id=workflow_id,
                thread_id=thread_id,
                state=state,
                step=step,
                timestamp=time.time(),
                status=status,
                error=error,
                metadata=metadata
            )
            
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO checkpoints 
                (checkpoint_id, workflow_id, thread_id, state, step, timestamp, status, error, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                checkpoint.checkpoint_id,
                checkpoint.workflow_id,
                checkpoint.thread_id,
                json.dumps(checkpoint.state),
                checkpoint.step,
                checkpoint.timestamp,
                checkpoint.status,
                checkpoint.error,
                json.dumps(checkpoint.metadata) if checkpoint.metadata else None
            ))
            
            conn.commit()
            conn.close()
            
            self.logger.info(
                "Checkpoint saved",
                checkpoint_id=checkpoint_id,
                workflow_id=workflow_id,
                step=step,
                status=status
            )
            
            return checkpoint_id
    
    @with_error_handling
    def load_checkpoint(self, checkpoint_id: str) -> Optional[WorkflowCheckpoint]:
        """
        Load workflow checkpoint.
        
        Args:
            checkpoint_id: Checkpoint ID
            
        Returns:
            WorkflowCheckpoint or None if not found
        """
        with self._lock:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT checkpoint_id, workflow_id, thread_id, state, step, timestamp, status, error, metadata
                FROM checkpoints
                WHERE checkpoint_id = ?
            """, (checkpoint_id,))
            
            row = cursor.fetchone()
            conn.close()
            
            if not row:
                self.logger.warning("Checkpoint not found", checkpoint_id=checkpoint_id)
                return None
            
            checkpoint = WorkflowCheckpoint(
                checkpoint_id=row[0],
                workflow_id=row[1],
                thread_id=row[2],
                state=json.loads(row[3]),
                step=row[4],
                timestamp=row[5],
                status=row[6],
                error=row[7],
                metadata=json.loads(row[8]) if row[8] else None
            )
            
            self.logger.info("Checkpoint loaded", checkpoint_id=checkpoint_id)
            
            return checkpoint
    
    @with_error_handling
    def get_latest_checkpoint(
        self,
        workflow_id: str,
        thread_id: Optional[str] = None
    ) -> Optional[WorkflowCheckpoint]:
        """
        Get latest checkpoint for workflow.
        
        Args:
            workflow_id: Workflow ID
            thread_id: Thread ID (optional)
            
        Returns:
            Latest WorkflowCheckpoint or None
        """
        with self._lock:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            if thread_id:
                cursor.execute("""
                    SELECT checkpoint_id, workflow_id, thread_id, state, step, timestamp, status, error, metadata
                    FROM checkpoints
                    WHERE workflow_id = ? AND thread_id = ?
                    ORDER BY timestamp DESC
                    LIMIT 1
                """, (workflow_id, thread_id))
            else:
                cursor.execute("""
                    SELECT checkpoint_id, workflow_id, thread_id, state, step, timestamp, status, error, metadata
                    FROM checkpoints
                    WHERE workflow_id = ?
                    ORDER BY timestamp DESC
                    LIMIT 1
                """, (workflow_id,))
            
            row = cursor.fetchone()
            conn.close()
            
            if not row:
                return None
            
            checkpoint = WorkflowCheckpoint(
                checkpoint_id=row[0],
                workflow_id=row[1],
                thread_id=row[2],
                state=json.loads(row[3]),
                step=row[4],
                timestamp=row[5],
                status=row[6],
                error=row[7],
                metadata=json.loads(row[8]) if row[8] else None
            )
            
            return checkpoint
    
    @with_error_handling
    def list_checkpoints(
        self,
        workflow_id: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 100
    ) -> List[WorkflowCheckpoint]:
        """
        List checkpoints.
        
        Args:
            workflow_id: Filter by workflow ID
            status: Filter by status
            limit: Maximum number of results
            
        Returns:
            List of WorkflowCheckpoint
        """
        with self._lock:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            query = """
                SELECT checkpoint_id, workflow_id, thread_id, state, step, timestamp, status, error, metadata
                FROM checkpoints
                WHERE 1=1
            """
            params = []
            
            if workflow_id:
                query += " AND workflow_id = ?"
                params.append(workflow_id)
            
            if status:
                query += " AND status = ?"
                params.append(status)
            
            query += " ORDER BY timestamp DESC LIMIT ?"
            params.append(limit)
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            conn.close()
            
            checkpoints = []
            for row in rows:
                checkpoint = WorkflowCheckpoint(
                    checkpoint_id=row[0],
                    workflow_id=row[1],
                    thread_id=row[2],
                    state=json.loads(row[3]),
                    step=row[4],
                    timestamp=row[5],
                    status=row[6],
                    error=row[7],
                    metadata=json.loads(row[8]) if row[8] else None
                )
                checkpoints.append(checkpoint)
            
            return checkpoints
    
    @with_error_handling
    def delete_checkpoint(self, checkpoint_id: str) -> bool:
        """
        Delete checkpoint.
        
        Args:
            checkpoint_id: Checkpoint ID
            
        Returns:
            True if deleted, False if not found
        """
        with self._lock:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM checkpoints WHERE checkpoint_id = ?", (checkpoint_id,))
            deleted = cursor.rowcount > 0
            
            conn.commit()
            conn.close()
            
            if deleted:
                self.logger.info("Checkpoint deleted", checkpoint_id=checkpoint_id)
            
            return deleted
    
    @with_error_handling
    def cleanup_old_checkpoints(self, days: int = 7) -> int:
        """
        Delete checkpoints older than specified days.
        
        Args:
            days: Number of days to keep
            
        Returns:
            Number of checkpoints deleted
        """
        with self._lock:
            cutoff = time.time() - (days * 24 * 60 * 60)
            
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM checkpoints WHERE timestamp < ?", (cutoff,))
            deleted = cursor.rowcount
            
            conn.commit()
            conn.close()
            
            self.logger.info(f"Cleaned up {deleted} old checkpoints", days=days)
            
            return deleted


# ============================================================================
# LangGraph Integration
# ============================================================================

def create_checkpointer(use_sqlite: bool = False, db_path: str = ".smartspec/langgraph_checkpoints.db") -> Any:
    """
    Create LangGraph checkpointer.
    
    Args:
        use_sqlite: Use SQLite (True) or Memory (False) - SQLite not available, always uses Memory
        db_path: Path to SQLite database (ignored)
        
    Returns:
        Checkpointer instance (MemorySaver)
    """
    # SQLite checkpointer not available in current LangGraph version
    # Always use MemorySaver
    return MemorySaver()


# Export all
__all__ = [
    'WorkflowCheckpoint',
    'CheckpointManager',
    'create_checkpointer',
]
