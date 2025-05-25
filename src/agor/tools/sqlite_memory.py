"""
SQLite-based memory management for AGOR agents.

Provides structured database storage for agent memories, coordination logs,
and persistent state management. This is an experimental feature that enables
more sophisticated memory patterns than simple markdown files.
"""

import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional


class SQLiteMemoryManager:
    """
    SQLite-based memory management for AGOR agents.

    Provides structured storage for:
    - Agent memories and context
    - Coordination logs and handoffs
    - Project state and progress tracking
    - Cross-agent communication
    """

    def __init__(self, db_path: str = ".agor/memory.db"):
        """Initialize SQLite memory manager."""
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()

    def _init_database(self):
        """Initialize database schema."""
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript(
                """
                -- Agent memories table
                CREATE TABLE IF NOT EXISTS agent_memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    agent_id TEXT NOT NULL,
                    memory_type TEXT NOT NULL,  -- 'context', 'decision', 'learning', 'handoff'
                    content TEXT NOT NULL,
                    metadata TEXT,  -- JSON metadata
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                
                -- Coordination logs table
                CREATE TABLE IF NOT EXISTS coordination_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    from_agent TEXT,
                    to_agent TEXT,
                    message_type TEXT NOT NULL,  -- 'handoff', 'status', 'request', 'response'
                    content TEXT NOT NULL,
                    metadata TEXT,  -- JSON metadata
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                
                -- Project state table
                CREATE TABLE IF NOT EXISTS project_state (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT UNIQUE NOT NULL,
                    value TEXT NOT NULL,
                    description TEXT,
                    updated_by TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                
                -- Handoffs table
                CREATE TABLE IF NOT EXISTS handoffs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    handoff_id TEXT UNIQUE NOT NULL,
                    from_agent TEXT NOT NULL,
                    to_agent TEXT,
                    status TEXT DEFAULT 'active',  -- 'active', 'received', 'completed'
                    problem_description TEXT NOT NULL,
                    work_completed TEXT,
                    commits_made TEXT,
                    files_modified TEXT,
                    current_status TEXT,
                    next_steps TEXT,
                    context_notes TEXT,
                    git_branch TEXT,
                    git_commit TEXT,
                    agor_version TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                
                -- Indexes for performance
                CREATE INDEX IF NOT EXISTS idx_agent_memories_agent_id ON agent_memories(agent_id);
                CREATE INDEX IF NOT EXISTS idx_agent_memories_type ON agent_memories(memory_type);
                CREATE INDEX IF NOT EXISTS idx_coordination_logs_agents ON coordination_logs(from_agent, to_agent);
                CREATE INDEX IF NOT EXISTS idx_handoffs_status ON handoffs(status);
                CREATE INDEX IF NOT EXISTS idx_handoffs_agents ON handoffs(from_agent, to_agent);
            """
            )

    def add_memory(
        self,
        agent_id: str,
        memory_type: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> int:
        """Add a memory entry for an agent."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                INSERT INTO agent_memories (agent_id, memory_type, content, metadata)
                VALUES (?, ?, ?, ?)
                """,
                (
                    agent_id,
                    memory_type,
                    content,
                    json.dumps(metadata) if metadata else None,
                ),
            )
            return cursor.lastrowid

    def get_memories(
        self, agent_id: str, memory_type: Optional[str] = None, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Retrieve memories for an agent."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row

            if memory_type:
                cursor = conn.execute(
                    """
                    SELECT * FROM agent_memories 
                    WHERE agent_id = ? AND memory_type = ?
                    ORDER BY created_at DESC LIMIT ?
                    """,
                    (agent_id, memory_type, limit),
                )
            else:
                cursor = conn.execute(
                    """
                    SELECT * FROM agent_memories 
                    WHERE agent_id = ?
                    ORDER BY created_at DESC LIMIT ?
                    """,
                    (agent_id, limit),
                )

            return [dict(row) for row in cursor.fetchall()]

    def log_coordination(
        self,
        from_agent: str,
        to_agent: Optional[str],
        message_type: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> int:
        """Log coordination message between agents."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                INSERT INTO coordination_logs (from_agent, to_agent, message_type, content, metadata)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    from_agent,
                    to_agent,
                    message_type,
                    content,
                    json.dumps(metadata) if metadata else None,
                ),
            )
            return cursor.lastrowid

    def get_coordination_logs(
        self,
        agent_id: Optional[str] = None,
        message_type: Optional[str] = None,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """Retrieve coordination logs."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row

            conditions = []
            params = []

            if agent_id:
                conditions.append("(from_agent = ? OR to_agent = ?)")
                params.extend([agent_id, agent_id])

            if message_type:
                conditions.append("message_type = ?")
                params.append(message_type)

            where_clause = " AND ".join(conditions) if conditions else "1=1"
            params.append(limit)

            cursor = conn.execute(
                f"""
                SELECT * FROM coordination_logs 
                WHERE {where_clause}
                ORDER BY created_at DESC LIMIT ?
                """,
                params,
            )

            return [dict(row) for row in cursor.fetchall()]

    def set_project_state(
        self,
        key: str,
        value: str,
        description: Optional[str] = None,
        updated_by: Optional[str] = None,
    ):
        """Set project state value."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO project_state (key, value, description, updated_by, updated_at)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
                """,
                (key, value, description, updated_by),
            )

    def get_project_state(self, key: str) -> Optional[Dict[str, Any]]:
        """Get project state value."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM project_state WHERE key = ?", (key,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def create_handoff(
        self,
        handoff_id: str,
        from_agent: str,
        problem_description: str,
        work_completed: str,
        commits_made: str,
        files_modified: str,
        current_status: str,
        next_steps: str,
        context_notes: str,
        git_branch: str,
        git_commit: str,
        agor_version: str,
        to_agent: Optional[str] = None,
    ) -> int:
        """Create a new handoff record."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                INSERT INTO handoffs (
                    handoff_id, from_agent, to_agent, problem_description,
                    work_completed, commits_made, files_modified, current_status,
                    next_steps, context_notes, git_branch, git_commit, agor_version
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    handoff_id,
                    from_agent,
                    to_agent,
                    problem_description,
                    work_completed,
                    commits_made,
                    files_modified,
                    current_status,
                    next_steps,
                    context_notes,
                    git_branch,
                    git_commit,
                    agor_version,
                ),
            )
            return cursor.lastrowid

    def update_handoff_status(
        self, handoff_id: str, status: str, to_agent: Optional[str] = None
    ):
        """Update handoff status."""
        with sqlite3.connect(self.db_path) as conn:
            if to_agent:
                conn.execute(
                    """
                    UPDATE handoffs 
                    SET status = ?, to_agent = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE handoff_id = ?
                    """,
                    (status, to_agent, handoff_id),
                )
            else:
                conn.execute(
                    """
                    UPDATE handoffs 
                    SET status = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE handoff_id = ?
                    """,
                    (status, handoff_id),
                )

    def get_handoffs(
        self, status: Optional[str] = None, agent_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Retrieve handoffs."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row

            conditions = []
            params = []

            if status:
                conditions.append("status = ?")
                params.append(status)

            if agent_id:
                conditions.append("(from_agent = ? OR to_agent = ?)")
                params.extend([agent_id, agent_id])

            where_clause = " AND ".join(conditions) if conditions else "1=1"

            cursor = conn.execute(
                f"""
                SELECT * FROM handoffs 
                WHERE {where_clause}
                ORDER BY created_at DESC
                """,
                params,
            )

            return [dict(row) for row in cursor.fetchall()]

    def search_memories(
        self,
        query: str,
        agent_id: Optional[str] = None,
        memory_type: Optional[str] = None,
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        """Search memories by content."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row

            conditions = ["content LIKE ?"]
            params = [f"%{query}%"]

            if agent_id:
                conditions.append("agent_id = ?")
                params.append(agent_id)

            if memory_type:
                conditions.append("memory_type = ?")
                params.append(memory_type)

            where_clause = " AND ".join(conditions)
            params.append(limit)

            cursor = conn.execute(
                f"""
                SELECT * FROM agent_memories 
                WHERE {where_clause}
                ORDER BY created_at DESC LIMIT ?
                """,
                params,
            )

            return [dict(row) for row in cursor.fetchall()]

    def get_database_stats(self) -> Dict[str, int]:
        """Get database statistics."""
        with sqlite3.connect(self.db_path) as conn:
            stats = {}

            # Count records in each table
            for table in [
                "agent_memories",
                "coordination_logs",
                "project_state",
                "handoffs",
            ]:
                cursor = conn.execute(f"SELECT COUNT(*) FROM {table}")
                stats[table] = cursor.fetchone()[0]

            return stats


# Convenience functions for common operations
def get_memory_manager(db_path: str = ".agor/memory.db") -> SQLiteMemoryManager:
    """Get a SQLite memory manager instance."""
    return SQLiteMemoryManager(db_path)


def log_agent_action(
    agent_id: str, action: str, details: str, metadata: Optional[Dict[str, Any]] = None
):
    """Log an agent action to memory."""
    manager = get_memory_manager()
    manager.add_memory(agent_id, "action", f"{action}: {details}", metadata)


def log_agent_decision(
    agent_id: str,
    decision: str,
    reasoning: str,
    metadata: Optional[Dict[str, Any]] = None,
):
    """Log an agent decision to memory."""
    manager = get_memory_manager()
    manager.add_memory(
        agent_id, "decision", f"Decision: {decision}\nReasoning: {reasoning}", metadata
    )


def log_coordination_message(
    from_agent: str, to_agent: str, message: str, message_type: str = "communication"
):
    """Log coordination message between agents."""
    manager = get_memory_manager()
    manager.log_coordination(from_agent, to_agent, message_type, message)


# Template for SQLite memory hotkeys
SQLITE_MEMORY_HOTKEYS = """
🗄️ **SQLite Memory Commands (Experimental):**
mem-add) add memory entry
mem-get) retrieve memories  
mem-search) search memory content
coord-log) log coordination message
state-set) set project state
state-get) get project state
handoff-create) create database handoff
handoff-status) update handoff status
db-stats) show database statistics
"""
