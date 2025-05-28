"""
SQLite-based memory management for AGOR agents.

Provides structured database storage for agent memories, coordination logs,
and persistent state management. This is an experimental feature that enables
more sophisticated memory patterns than simple markdown files.
"""

import json
import os
import sqlite3
import sys # For printing errors/info
from pathlib import Path
from typing import Any, Dict, List, Optional

from agor.memory_sync import MemorySyncManager
try:
    from agor.utils import get_git_root
except ImportError:
    get_git_root = None


def resolve_memory_db_path(db_path: str = ".agor/memory.db") -> str:
    """
    Resolve the correct path for the SQLite memory database.

    Handles different environments:
    - Bundle mode: Look for project directory in /tmp/
    - Standalone mode: Use current working directory
    - Explicit path: Use as-is if absolute

    Args:
        db_path: Default or requested database path

    Returns:
        Resolved absolute path to the database
    """
    # If absolute path provided, use as-is
    if os.path.isabs(db_path):
        return db_path

    # Try to detect bundle mode vs standalone mode
    current_dir = Path.cwd()

    # Bundle mode detection: look for /tmp/agor_tools/ or similar patterns
    if "/tmp" in str(current_dir) or any(
        p.name == "agor_tools" for p in current_dir.parents
    ):
        # Bundle mode: find the project directory
        # Look for .git directory to identify project root
        project_dir = None

        # Check current directory and parents for .git
        for check_dir in [current_dir] + list(current_dir.parents):
            if (check_dir / ".git").exists():
                project_dir = check_dir
                break

        # If no .git found, look in /tmp for project directories
        if not project_dir:
            tmp_path = Path("/tmp")
            if tmp_path.exists():
                for item in tmp_path.iterdir():
                    if item.is_dir() and (item / ".git").exists():
                        project_dir = item
                        break

        # Default to current directory if no project found
        if not project_dir:
            project_dir = current_dir

        resolved_path = project_dir / db_path
    else:
        # Standalone mode: use current directory
        resolved_path = current_dir / db_path

    return str(resolved_path.resolve())


class SQLiteMemoryManager:
    """
    SQLite-based memory management for AGOR agents.

    Provides structured storage for:
    - Agent memories and context
    - Coordination logs and snapshots
    - Project state and progress tracking
    - Cross-agent communication
    """

    def __init__(self, db_path: str = ".agor/memory.db"):
        """Initialize SQLite memory manager."""
        # Resolve path if it's not already absolute
        if not os.path.isabs(db_path):
            db_path = resolve_memory_db_path(db_path)

        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        # Initialize MemorySyncManager
        repo_root_path: Optional[Path] = None
        if get_git_root:
            try:
                # Assuming get_git_root returns a Path object or string
                resolved_git_root = get_git_root(start_path=self.db_path.parent)
                if resolved_git_root:
                    repo_root_path = Path(resolved_git_root)
                else:
                    print("SQLiteMemoryManager: get_git_root() did not return a path. Defaulting repo_path for MemorySyncManager to current directory.", file=sys.stderr)
                    repo_root_path = Path(".") # Fallback
            except Exception as e:
                print(f"SQLiteMemoryManager: Error calling get_git_root: {e}. Defaulting repo_path for MemorySyncManager to current directory.", file=sys.stderr)
                repo_root_path = Path(".") # Fallback
        else:
            print("SQLiteMemoryManager: agor.utils.get_git_root not available. Defaulting repo_path for MemorySyncManager to current directory. Git sync features might be limited.", file=sys.stderr)
            repo_root_path = Path(".") # Fallback
        
        self.memory_sync_manager = MemorySyncManager(repo_path=repo_root_path)
        self.active_memory_branch_name: Optional[str] = None
        # Store original branch before any sync operations change it
        self.original_branch_before_sync: Optional[str] = self.memory_sync_manager._get_current_branch()

        print(f"SQLiteMemoryManager: Original branch is '{self.original_branch_before_sync}'. Attempting startup sync...", file=sys.stdout)
        startup_success = self.memory_sync_manager.auto_sync_on_startup()

        if startup_success:
            self.active_memory_branch_name = self.memory_sync_manager.get_active_memory_branch()
            print(f"SQLiteMemoryManager: Successfully synced with memory branch '{self.active_memory_branch_name}'.", file=sys.stdout)
        else:
            print(f"SQLiteMemoryManager: CRITICAL - Failed to sync with memory branch on startup. Using local memory.db if available. Original branch was '{self.original_branch_before_sync}'.", file=sys.stderr)
            # Potentially, one might want to ensure we are on original_branch_before_sync if startup failed.
            # However, auto_sync_on_startup already attempts to restore original branch on its own failure.

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
                    memory_type TEXT NOT NULL,  -- 'context', 'decision', 'learning', 'snapshot'
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
                    message_type TEXT NOT NULL,  -- 'snapshot', 'status', 'request', 'response'
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

                -- Snapshots table (formerly Handoffs)
                CREATE TABLE IF NOT EXISTS snapshots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    snapshot_id TEXT UNIQUE NOT NULL, -- formerly handoff_id
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
                CREATE INDEX IF NOT EXISTS idx_snapshots_status ON snapshots(status); -- formerly idx_handoffs_status
                CREATE INDEX IF NOT EXISTS idx_snapshots_agents ON snapshots(from_agent, to_agent); -- formerly idx_handoffs_agents
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
        value: Any,
        description: Optional[str] = None,
        updated_by: Optional[str] = None,
    ):
        """Set project state value."""
        # Convert value to JSON string if it's not already a string
        if not isinstance(value, str):
            value = json.dumps(value)

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO project_state (key, value, description, updated_by, updated_at)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
                """,
                (key, value, description, updated_by),
            )

    def get_project_state(self, key: str) -> Optional[Any]:
        """Get project state value."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT value FROM project_state WHERE key = ?", (key,)
            )
            result = cursor.fetchone()
            if result:
                try:
                    # Try to parse as JSON, fall back to string
                    return json.loads(result[0])
                except json.JSONDecodeError:
                    return result[0]
            return None

    def create_snapshot(
        self,
        snapshot_id: str, # formerly handoff_id
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
        """Create a new snapshot record."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                INSERT INTO snapshots (
                    snapshot_id, from_agent, to_agent, problem_description,
                    work_completed, commits_made, files_modified, current_status,
                    next_steps, context_notes, git_branch, git_commit, agor_version
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    snapshot_id,
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

    def update_snapshot_status(
        self, snapshot_id: str, status: str, to_agent: Optional[str] = None
    ):
        """Update snapshot status."""
        with sqlite3.connect(self.db_path) as conn:
            if to_agent:
                conn.execute(
                    """
                    UPDATE snapshots
                    SET status = ?, to_agent = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE snapshot_id = ?
                    """,
                    (status, to_agent, snapshot_id),
                )
            else:
                conn.execute(
                    """
                    UPDATE snapshots
                    SET status = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE snapshot_id = ?
                    """,
                    (status, snapshot_id),
                )

    def get_snapshots(
        self, status: Optional[str] = None, agent_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Retrieve snapshots."""
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
                SELECT * FROM snapshots
                WHERE {where_clause}
                ORDER BY created_at DESC
                """,
                params,
            )

            return [dict(row) for row in cursor.fetchall()]

    def get_snapshot(self, snapshot_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific snapshot by ID."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM snapshots WHERE snapshot_id = ?", (snapshot_id,)
            )
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_agent_snapshots(self, agent_id: str) -> List[Dict[str, Any]]:
        """Get all snapshots for a specific agent (sent or received)."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                """
                SELECT * FROM snapshots
                WHERE from_agent = ? OR to_agent = ?
                ORDER BY created_at DESC
                """,
                (agent_id, agent_id),
            )
            return [dict(row) for row in cursor.fetchall()]

    def _get_connection(self):
        """Get database connection (for migration utilities)."""
        return sqlite3.connect(self.db_path)

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
                "snapshots", # formerly handoffs
            ]:
                cursor = conn.execute(f"SELECT COUNT(*) FROM {table}")
                stats[table] = cursor.fetchone()[0]

            return stats

    def shutdown_and_sync(self, commit_message: Optional[str] = None, restore_original_branch_override: Optional[str] = None) -> bool:
        """
        Shuts down the memory manager, syncing the memory.db file with the remote repository.

        Args:
            commit_message: Optional custom commit message for the sync.
            restore_original_branch_override: Optionally override the branch to restore after sync.
                                               If None, restores the branch active before startup sync.

        Returns:
            True if the shutdown sync was successful (local commit succeeded), False otherwise.
        """
        if not self.active_memory_branch_name:
            print("SQLiteMemoryManager: No active memory branch set. Cannot perform shutdown sync.", file=sys.stderr)
            return False

        default_commit_msg = f"Automated memory sync to branch {self.active_memory_branch_name}."
        final_commit_message = commit_message if commit_message else default_commit_msg

        branch_to_restore = restore_original_branch_override if restore_original_branch_override else self.original_branch_before_sync
        
        print(f"SQLiteMemoryManager: Initiating shutdown sync for branch '{self.active_memory_branch_name}'. Commit: '{final_commit_message}'. Restore to: '{branch_to_restore}'", file=sys.stdout)

        sync_result = self.memory_sync_manager.auto_sync_on_shutdown(
            target_branch_name=self.active_memory_branch_name,
            commit_message=final_commit_message,
            push_changes=True,  # Assuming push is desired on shutdown
            restore_original_branch=branch_to_restore
        )

        if sync_result:
            print("SQLiteMemoryManager: Shutdown sync successful.", file=sys.stdout)
        else:
            print("SQLiteMemoryManager: Shutdown sync failed. Check logs from MemorySyncManager.", file=sys.stderr)
        
        return sync_result


# Convenience functions for common operations
def get_memory_manager(db_path: str = ".agor/memory.db") -> SQLiteMemoryManager:
    """Get a SQLite memory manager instance with proper path resolution."""
    resolved_path = resolve_memory_db_path(db_path)
    return SQLiteMemoryManager(resolved_path)


def validate_sqlite_setup(db_path: str = ".agor/memory.db") -> tuple[bool, str]:
    """
    Validate that SQLite memory setup is working correctly.

    Args:
        db_path: Database path to test

    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        resolved_path = resolve_memory_db_path(db_path)

        # Test creating a manager and basic operations
        manager = SQLiteMemoryManager(resolved_path)

        # Test write operation
        test_id = manager.add_memory(
            "test-agent", "validation", "SQLite validation test", {"test": True}
        )

        # Test read operation
        memories = manager.get_memories("test-agent", memory_type="validation")

        if not memories or len(memories) == 0:
            return False, f"Failed to retrieve test memory from {resolved_path}"

        # Clean up test data
        with sqlite3.connect(resolved_path) as conn:
            conn.execute("DELETE FROM agent_memories WHERE id = ?", (test_id,))

        return True, f"SQLite memory system validated at {resolved_path}"

    except Exception as e:
        return False, f"SQLite validation failed: {e}"


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
snapshot-create) create database snapshot
snapshot-status) update snapshot status
db-stats) show database statistics
sqlite-validate) validate setup and path resolution
"""
