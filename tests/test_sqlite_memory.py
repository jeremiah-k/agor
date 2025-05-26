"""
Comprehensive tests for SQLite memory management system.

Tests all SQLite memory functionality to ensure parity with markdown-based
memory system and proper integration with AGOR coordination protocols.
"""

import json
import sqlite3
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from agor.tools.sqlite_memory import (
    SQLiteMemoryManager,
    get_memory_manager,
    log_agent_action,
    log_agent_decision,
    log_coordination_message,
)


class TestSQLiteMemoryManager:
    """Test SQLite memory manager core functionality."""

    def setup_method(self):
        """Set up test database for each test."""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = Path(self.temp_dir) / "test_memory.db"
        self.manager = SQLiteMemoryManager(str(self.db_path))

    def teardown_method(self):
        """Clean up test database."""
        if self.db_path.exists():
            self.db_path.unlink()

    def test_database_initialization(self):
        """Test that database is properly initialized with correct schema."""
        # Verify database file exists
        assert self.db_path.exists()

        # Verify all tables exist
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
            tables = {row[0] for row in cursor.fetchall()}

        expected_tables = {
            "agent_memories",
            "coordination_logs",
            "project_state",
            "handoffs"
        }
        assert expected_tables.issubset(tables)

    def test_add_memory_basic(self):
        """Test adding basic memory entries."""
        # Add memory without metadata
        memory_id = self.manager.add_memory(
            "agent-1", "decision", "Chose React for frontend"
        )
        assert isinstance(memory_id, int)
        assert memory_id > 0

        # Add memory with metadata
        metadata = {"confidence": 0.8, "alternatives": ["Vue", "Angular"]}
        memory_id2 = self.manager.add_memory(
            "agent-1", "context", "Frontend framework analysis", metadata
        )
        assert memory_id2 > memory_id

    def test_get_memories(self):
        """Test retrieving memories for agents."""
        # Add test memories
        self.manager.add_memory("agent-1", "decision", "Decision 1")
        self.manager.add_memory("agent-1", "context", "Context 1")
        self.manager.add_memory("agent-2", "decision", "Decision 2")

        # Get all memories for agent-1
        memories = self.manager.get_memories("agent-1")
        assert len(memories) == 2
        assert all(m["agent_id"] == "agent-1" for m in memories)

        # Get specific memory type
        decisions = self.manager.get_memories("agent-1", memory_type="decision")
        assert len(decisions) == 1
        assert decisions[0]["memory_type"] == "decision"
        assert decisions[0]["content"] == "Decision 1"

        # Test limit
        limited = self.manager.get_memories("agent-1", limit=1)
        assert len(limited) == 1

    def test_search_memories(self):
        """Test memory search functionality."""
        # Add searchable memories
        self.manager.add_memory("agent-1", "decision", "Chose React for frontend")
        self.manager.add_memory("agent-1", "context", "Backend uses Node.js")
        self.manager.add_memory("agent-2", "decision", "React components structure")

        # Search across all agents
        results = self.manager.search_memories("React")
        assert len(results) == 2
        assert all("React" in r["content"] for r in results)

        # Search for specific agent
        agent_results = self.manager.search_memories("React", agent_id="agent-1")
        assert len(agent_results) == 1
        assert agent_results[0]["agent_id"] == "agent-1"

        # Search by memory type
        type_results = self.manager.search_memories("React", memory_type="decision")
        assert len(type_results) == 2
        assert all(r["memory_type"] == "decision" for r in type_results)

    def test_coordination_logging(self):
        """Test coordination message logging."""
        # Log coordination message
        log_id = self.manager.log_coordination(
            "agent-1", "agent-2", "handoff", "Passing frontend work to you"
        )
        assert isinstance(log_id, int)

        # Retrieve coordination logs
        logs = self.manager.get_coordination_logs("agent-1")
        assert len(logs) == 1
        assert logs[0]["from_agent"] == "agent-1"
        assert logs[0]["to_agent"] == "agent-2"
        assert logs[0]["message_type"] == "handoff"

        # Test filtering by message type
        handoff_logs = self.manager.get_coordination_logs(
            "agent-1", message_type="handoff"
        )
        assert len(handoff_logs) == 1

    def test_project_state_management(self):
        """Test project state storage and retrieval."""
        # Set project state
        state_data = {
            "current_phase": "implementation",
            "active_agents": ["agent-1", "agent-2"],
            "completion_percentage": 45
        }
        self.manager.set_project_state("development_status", state_data)

        # Get project state
        retrieved_state = self.manager.get_project_state("development_status")
        assert retrieved_state == state_data

        # Test non-existent state
        missing_state = self.manager.get_project_state("non_existent")
        assert missing_state is None

        # Update existing state
        updated_data = {"current_phase": "testing", "completion_percentage": 75}
        self.manager.set_project_state("development_status", updated_data)

        final_state = self.manager.get_project_state("development_status")
        assert final_state == updated_data

    def test_handoff_management(self):
        """Test handoff creation and management."""
        # Create handoff
        handoff_id = self.manager.create_handoff(
            handoff_id="handoff-001",
            from_agent="agent-1",
            problem_description="Implement user authentication",
            work_completed="Created login form and validation",
            commits_made="abc123, def456",
            files_modified="auth.js, login.html",
            current_status="70% complete",
            next_steps="Add password reset functionality",
            context_notes="Using JWT tokens",
            git_branch="feature/auth",
            git_commit="abc123",
            agor_version="0.2.4",
            to_agent="agent-2"
        )
        assert isinstance(handoff_id, int)

        # Get handoff
        handoff = self.manager.get_handoff("handoff-001")
        assert handoff is not None
        assert handoff["from_agent"] == "agent-1"
        assert handoff["to_agent"] == "agent-2"
        assert handoff["status"] == "active"

        # Update handoff status
        self.manager.update_handoff_status("handoff-001", "received")
        updated_handoff = self.manager.get_handoff("handoff-001")
        assert updated_handoff["status"] == "received"

        # List handoffs for agent
        agent_handoffs = self.manager.get_agent_handoffs("agent-1")
        assert len(agent_handoffs) == 1
        assert agent_handoffs[0]["handoff_id"] == "handoff-001"

    def test_database_stats(self):
        """Test database statistics functionality."""
        # Add some test data
        self.manager.add_memory("agent-1", "decision", "Test decision")
        self.manager.log_coordination("agent-1", "agent-2", "message", "Test message")
        self.manager.set_project_state("test_state", {"value": 1})
        self.manager.create_handoff(
            "test-handoff", "agent-1", "Test problem", "Test work",
            "commit1", "file1.py", "In progress", "Continue work",
            "Test notes", "main", "commit1", "0.2.4"
        )

        # Get stats
        stats = self.manager.get_database_stats()
        assert stats["agent_memories"] == 1
        assert stats["coordination_logs"] == 1
        assert stats["project_state"] == 1
        assert stats["handoffs"] == 1

    def test_metadata_handling(self):
        """Test JSON metadata storage and retrieval."""
        metadata = {
            "confidence": 0.9,
            "tags": ["frontend", "react"],
            "related_files": ["app.js", "index.html"],
            "nested": {"key": "value", "number": 42}
        }

        # Add memory with complex metadata
        memory_id = self.manager.add_memory(
            "agent-1", "decision", "Complex decision", metadata
        )

        # Retrieve and verify metadata
        memories = self.manager.get_memories("agent-1")
        retrieved_memory = memories[0]

        # Metadata should be parsed back from JSON
        assert retrieved_memory["metadata"] == json.dumps(metadata)
        parsed_metadata = json.loads(retrieved_memory["metadata"])
        assert parsed_metadata == metadata

    def test_memory_types(self):
        """Test different memory types are handled correctly."""
        memory_types = ["context", "decision", "learning", "handoff", "action"]

        for i, mem_type in enumerate(memory_types):
            self.manager.add_memory(
                "agent-1", mem_type, f"Content for {mem_type} {i}"
            )

        # Verify all types are stored
        all_memories = self.manager.get_memories("agent-1")
        stored_types = {m["memory_type"] for m in all_memories}
        assert stored_types == set(memory_types)

        # Test filtering by each type
        for mem_type in memory_types:
            type_memories = self.manager.get_memories("agent-1", memory_type=mem_type)
            assert len(type_memories) == 1
            assert type_memories[0]["memory_type"] == mem_type


class TestConvenienceFunctions:
    """Test convenience functions for common operations."""

    def setup_method(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = Path(self.temp_dir) / "test_memory.db"

    def teardown_method(self):
        """Clean up test environment."""
        if self.db_path.exists():
            self.db_path.unlink()

    @patch('agor.tools.sqlite_memory.get_memory_manager')
    def test_log_agent_action(self, mock_get_manager):
        """Test log_agent_action convenience function."""
        mock_manager = SQLiteMemoryManager(str(self.db_path))
        mock_get_manager.return_value = mock_manager

        # Test action logging
        log_agent_action("agent-1", "commit", "Added new feature", {"files": 3})

        # Verify memory was added
        memories = mock_manager.get_memories("agent-1", memory_type="action")
        assert len(memories) == 1
        assert "commit: Added new feature" in memories[0]["content"]

    @patch('agor.tools.sqlite_memory.get_memory_manager')
    def test_log_agent_decision(self, mock_get_manager):
        """Test log_agent_decision convenience function."""
        mock_manager = SQLiteMemoryManager(str(self.db_path))
        mock_get_manager.return_value = mock_manager

        # Test decision logging
        log_agent_decision(
            "agent-1",
            "Use React",
            "Better component reusability",
            {"confidence": 0.8}
        )

        # Verify decision was logged
        memories = mock_manager.get_memories("agent-1", memory_type="decision")
        assert len(memories) == 1
        content = memories[0]["content"]
        assert "Decision: Use React" in content
        assert "Reasoning: Better component reusability" in content

    @patch('agor.tools.sqlite_memory.get_memory_manager')
    def test_log_coordination_message(self, mock_get_manager):
        """Test log_coordination_message convenience function."""
        mock_manager = SQLiteMemoryManager(str(self.db_path))
        mock_get_manager.return_value = mock_manager

        # Test coordination logging
        log_coordination_message(
            "agent-1", "agent-2", "Handoff complete", "handoff"
        )

        # Verify coordination was logged
        logs = mock_manager.get_coordination_logs("agent-1")
        assert len(logs) == 1
        assert logs[0]["content"] == "Handoff complete"
        assert logs[0]["message_type"] == "handoff"


class TestSQLiteMemoryIntegration:
    """Test SQLite memory integration with AGOR systems."""

    def setup_method(self):
        """Set up integration test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.agor_dir = Path(self.temp_dir) / ".agor"
        self.agor_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.agor_dir / "memory.db"
        self.manager = SQLiteMemoryManager(str(self.db_path))

    def teardown_method(self):
        """Clean up integration test environment."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_agor_directory_integration(self):
        """Test SQLite memory works within .agor directory structure."""
        # Verify database is created in correct location
        assert self.db_path.exists()
        assert self.db_path.parent == self.agor_dir

        # Test memory operations work in AGOR context
        self.manager.add_memory("agent-1", "context", "Working in .agor directory")
        memories = self.manager.get_memories("agent-1")
        assert len(memories) == 1

    def test_handoff_integration(self):
        """Test handoff integration with AGOR handoff system."""
        # Create handoff that matches AGOR handoff format
        handoff_data = {
            "handoff_id": "2024-01-27_143022_auth-implementation",
            "from_agent": "agent-1",
            "to_agent": "agent-2",
            "problem_description": "Implement user authentication system",
            "work_completed": "Created login form, validation logic, and JWT integration",
            "commits_made": "abc123: Add login form\ndef456: Implement JWT auth",
            "files_modified": "auth.js, login.html, middleware/auth.js",
            "current_status": "Authentication flow complete, needs password reset",
            "next_steps": "1. Add password reset functionality\n2. Add email verification\n3. Add 2FA support",
            "context_notes": "Using JWT tokens with 24h expiry. Database schema in migrations/001_auth.sql",
            "git_branch": "feature/authentication",
            "git_commit": "def456",
            "agor_version": "0.2.4"
        }

        # Create handoff
        handoff_id = self.manager.create_handoff(**handoff_data)
        assert isinstance(handoff_id, int)

        # Verify handoff can be retrieved
        retrieved = self.manager.get_handoff(handoff_data["handoff_id"])
        assert retrieved["problem_description"] == handoff_data["problem_description"]
        assert retrieved["git_branch"] == handoff_data["git_branch"]

    def test_memory_parity_with_markdown(self):
        """Test that SQLite memory provides equivalent functionality to markdown memory."""
        # Test agent memory equivalent to agent{N}-memory.md
        agent_memories = [
            ("agent-1", "context", "Current task: Implement frontend"),
            ("agent-1", "decision", "Chose React over Vue for better ecosystem"),
            ("agent-1", "learning", "Learned about React hooks performance"),
            ("agent-2", "context", "Working on backend API"),
            ("agent-2", "decision", "Using Express.js for REST API")
        ]

        for agent_id, mem_type, content in agent_memories:
            self.manager.add_memory(agent_id, mem_type, content)

        # Verify agent-specific memory retrieval (equivalent to reading agent1-memory.md)
        agent1_memories = self.manager.get_memories("agent-1")
        assert len(agent1_memories) == 3
        assert all(m["agent_id"] == "agent-1" for m in agent1_memories)

        # Test coordination logging equivalent to agentconvo.md
        coordination_messages = [
            ("agent-1", "agent-2", "communication", "Starting frontend work"),
            ("agent-2", "agent-1", "question", "What API endpoints do you need?"),
            ("agent-1", "agent-2", "response", "Need /auth and /users endpoints")
        ]

        for from_agent, to_agent, msg_type, message in coordination_messages:
            self.manager.log_coordination(from_agent, to_agent, msg_type, message)

        # Verify coordination retrieval
        agent1_coords = self.manager.get_coordination_logs("agent-1")
        assert len(agent1_coords) >= 2  # agent-1 sent 2 messages

        # Test project state equivalent to memory.md
        project_state = {
            "task": "Build web application",
            "team_size": 2,
            "current_phase": "implementation",
            "key_decisions": ["React frontend", "Express backend"],
            "completion": 0.6
        }
        self.manager.set_project_state("project_overview", project_state)

        retrieved_state = self.manager.get_project_state("project_overview")
        assert retrieved_state == project_state


class TestSQLiteMemoryErrorHandling:
    """Test error handling and edge cases."""

    def setup_method(self):
        """Set up error handling tests."""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = Path(self.temp_dir) / "test_memory.db"

    def teardown_method(self):
        """Clean up error handling tests."""
        if self.db_path.exists():
            self.db_path.unlink()

    def test_invalid_database_path(self):
        """Test handling of invalid database paths."""
        # Test with read-only directory (if possible)
        invalid_path = "/root/readonly/memory.db"

        # Should handle gracefully or create in valid location
        try:
            manager = SQLiteMemoryManager(invalid_path)
            # If it succeeds, verify it works
            manager.add_memory("test", "context", "test content")
        except (PermissionError, OSError):
            # Expected for truly invalid paths
            pass

    def test_malformed_json_metadata(self):
        """Test handling of malformed JSON in metadata."""
        manager = SQLiteMemoryManager(str(self.db_path))

        # Add memory with valid metadata
        manager.add_memory("agent-1", "context", "test", {"valid": "json"})

        # Manually corrupt metadata in database
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "UPDATE agent_memories SET metadata = ? WHERE agent_id = ?",
                ("invalid json {", "agent-1")
            )

        # Should handle gracefully when retrieving
        memories = manager.get_memories("agent-1")
        assert len(memories) == 1
        # Metadata should be returned as string even if invalid JSON
        assert memories[0]["metadata"] == "invalid json {"

    def test_empty_search_queries(self):
        """Test search with empty or invalid queries."""
        manager = SQLiteMemoryManager(str(self.db_path))

        # Add test data
        manager.add_memory("agent-1", "context", "test content")

        # Test empty search (should match all content)
        results = manager.search_memories("")
        assert len(results) == 1  # Should match all content

        # Test search that matches content
        results = manager.search_memories("test")
        assert len(results) == 1

        # Test search that doesn't match
        results = manager.search_memories("nonexistent")
        assert len(results) == 0

    def test_nonexistent_handoff_operations(self):
        """Test operations on non-existent handoffs."""
        manager = SQLiteMemoryManager(str(self.db_path))

        # Get non-existent handoff
        handoff = manager.get_handoff("non-existent")
        assert handoff is None

        # Update non-existent handoff status
        # Should handle gracefully (no error, no effect)
        manager.update_handoff_status("non-existent", "completed")

        # Verify no handoffs exist
        stats = manager.get_database_stats()
        assert stats["handoffs"] == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
