"""
Integration tests for memory system parity between markdown and SQLite.

Tests that both memory systems provide equivalent functionality and can
be used interchangeably in AGOR coordination workflows.
"""

import json
import tempfile
from pathlib import Path

import pytest

from agor.tools.memory_migration import MemoryMigrationManager
from agor.tools.sqlite_memory import SQLiteMemoryManager


class TestMemorySystemParity:
    """Test parity between markdown and SQLite memory systems."""

    def setup_method(self):
        """Set up test environment with both memory systems."""
        self.temp_dir = tempfile.mkdtemp()
        self.agor_dir = Path(self.temp_dir) / ".agor"
        self.agor_dir.mkdir(parents=True, exist_ok=True)

        # Initialize SQLite memory system
        self.sqlite_manager = SQLiteMemoryManager(str(self.agor_dir / "memory.db"))

        # Initialize migration manager
        self.migration_manager = MemoryMigrationManager(self.agor_dir)

    def teardown_method(self):
        """Clean up test environment."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_agent_memory_parity(self):
        """Test that agent memories work equivalently in both systems."""
        # Test data representing typical agent memory usage
        agent_memories = [
            ("agent-1", "context", "Working on user authentication system"),
            ("agent-1", "decision", "Chose JWT tokens over sessions for scalability"),
            ("agent-1", "learning", "Learned about bcrypt security best practices"),
            ("agent-2", "context", "Implementing frontend components"),
            ("agent-2", "decision", "Using React hooks for state management"),
        ]

        # Add memories to SQLite system
        for agent_id, mem_type, content in agent_memories:
            self.sqlite_manager.add_memory(agent_id, mem_type, content)

        # Migrate to markdown
        stats = self.migration_manager.migrate_sqlite_to_markdown()
        assert stats["agent_memory_files"] == 2  # agent-1 and agent-2

        # Verify markdown files were created
        agent1_file = self.agor_dir / "agent-1-memory.md"
        agent2_file = self.agor_dir / "agent-2-memory.md"
        assert agent1_file.exists()
        assert agent2_file.exists()

        # Verify content in markdown files
        agent1_content = agent1_file.read_text()
        assert "user authentication system" in agent1_content
        assert "JWT tokens" in agent1_content
        assert "bcrypt security" in agent1_content

        agent2_content = agent2_file.read_text()
        assert "frontend components" in agent2_content
        assert "React hooks" in agent2_content

        # Clear SQLite and migrate back from markdown
        self.sqlite_manager = SQLiteMemoryManager(str(self.agor_dir / "memory_new.db"))
        self.migration_manager.sqlite_manager = self.sqlite_manager

        stats = self.migration_manager.migrate_markdown_to_sqlite()
        assert stats["agent_memories"] >= 5  # Should have migrated memories

        # Verify memories are back in SQLite
        agent1_memories = self.sqlite_manager.get_memories("agent-1")
        agent2_memories = self.sqlite_manager.get_memories("agent-2")
        assert len(agent1_memories) == 3
        assert len(agent2_memories) == 2

    def test_coordination_logging_parity(self):
        """Test that coordination logging works equivalently in both systems."""
        # Test coordination messages
        coordination_data = [
            ("agent-1", "agent-2", "handoff", "Passing authentication work to you"),
            ("agent-2", "agent-1", "question", "What database schema should I use?"),
            ("agent-1", "agent-2", "response", "Use the schema in migrations/001_auth.sql"),
            ("agent-2", "all", "status", "Frontend authentication UI is complete"),
        ]

        # Add to SQLite
        for from_agent, to_agent, msg_type, message in coordination_data:
            self.sqlite_manager.log_coordination(from_agent, to_agent, msg_type, message)

        # Migrate to markdown
        stats = self.migration_manager.migrate_sqlite_to_markdown()
        assert stats["coordination_entries"] == 4

        # Verify agentconvo.md was created
        agentconvo_file = self.agor_dir / "agentconvo.md"
        assert agentconvo_file.exists()

        content = agentconvo_file.read_text()
        assert "Passing authentication work" in content
        assert "What database schema" in content
        assert "migrations/001_auth.sql" in content
        assert "Frontend authentication UI" in content

        # Test bidirectional sync
        stats = self.migration_manager.sync_systems("bidirectional")
        assert stats["total_synced"] > 0

    def test_project_state_parity(self):
        """Test that project state management works equivalently in both systems."""
        # Complex project state data
        project_state = {
            "task": "Build secure web application with authentication",
            "team_configuration": {
                "size": 3,
                "roles": ["backend", "frontend", "security"],
                "active_agents": ["agent-1", "agent-2", "agent-3"]
            },
            "current_phase": "implementation",
            "key_decisions": [
                "Use JWT for authentication",
                "React for frontend",
                "PostgreSQL for database",
                "Docker for deployment"
            ],
            "completion_metrics": {
                "backend": 0.7,
                "frontend": 0.5,
                "security": 0.3,
                "overall": 0.5
            },
            "next_milestones": [
                "Complete authentication system",
                "Implement user dashboard",
                "Security audit and testing"
            ]
        }

        # Store in SQLite
        self.sqlite_manager.set_project_state("project_overview", project_state)

        # Migrate to markdown
        stats = self.migration_manager.migrate_sqlite_to_markdown()
        assert stats["project_state_entries"] == 1

        # Verify memory.md was created
        memory_file = self.agor_dir / "memory.md"
        assert memory_file.exists()

        content = memory_file.read_text()
        assert "secure web application" in content
        assert "JWT for authentication" in content

        # Migrate back to SQLite
        new_sqlite = SQLiteMemoryManager(str(self.agor_dir / "memory_test.db"))
        new_migration = MemoryMigrationManager(self.agor_dir)
        new_migration.sqlite_manager = new_sqlite

        stats = new_migration.migrate_markdown_to_sqlite()
        assert stats["project_state"] >= 1

        # Verify data integrity
        retrieved_state = new_sqlite.get_project_state("project_overview")
        assert retrieved_state is not None
        assert "task" in retrieved_state

    def test_handoff_system_parity(self):
        """Test that handoff management works equivalently in both systems."""
        # Create comprehensive handoff
        handoff_data = {
            "handoff_id": "2024-01-27_auth-handoff",
            "from_agent": "agent-1",
            "to_agent": "agent-2",
            "problem_description": "Complete user authentication system implementation",
            "work_completed": "Created JWT middleware, login/logout endpoints, password hashing",
            "commits_made": "abc123: Add JWT middleware\ndef456: Implement login endpoint\nghi789: Add password hashing",
            "files_modified": "auth/middleware.js, routes/auth.js, models/user.js, tests/auth.test.js",
            "current_status": "Authentication flow working, needs frontend integration",
            "next_steps": "1. Create login/register forms\n2. Integrate with React app\n3. Add error handling\n4. Write integration tests",
            "context_notes": "JWT secret is in .env file. Database migrations in migrations/ folder. API docs in docs/auth.md",
            "git_branch": "feature/authentication",
            "git_commit": "ghi789",
            "agor_version": "0.2.4"
        }

        # Create handoff in SQLite
        handoff_id = self.sqlite_manager.create_handoff(**handoff_data)
        assert isinstance(handoff_id, int)

        # Migrate to markdown
        stats = self.migration_manager.migrate_sqlite_to_markdown()
        assert stats["handoff_files"] == 1

        # Verify handoff file was created
        handoff_dir = self.agor_dir / "handoffs"
        assert handoff_dir.exists()

        handoff_files = list(handoff_dir.glob("*.md"))
        assert len(handoff_files) == 1

        handoff_content = handoff_files[0].read_text()
        assert "user authentication system" in handoff_content
        assert "JWT middleware" in handoff_content
        assert "feature/authentication" in handoff_content

        # Test handoff status updates
        self.sqlite_manager.update_handoff_status("2024-01-27_auth-handoff", "received")
        updated_handoff = self.sqlite_manager.get_handoff("2024-01-27_auth-handoff")
        assert updated_handoff["status"] == "received"

    def test_memory_search_parity(self):
        """Test that memory search works equivalently in both systems."""
        # Add diverse memories for search testing
        memories = [
            ("agent-1", "context", "Working on React frontend with TypeScript"),
            ("agent-1", "decision", "Chose Material-UI for component library"),
            ("agent-2", "context", "Implementing Node.js backend API"),
            ("agent-2", "decision", "Using Express.js framework for REST API"),
            ("agent-3", "learning", "Learned about React hooks and context API"),
        ]

        for agent_id, mem_type, content in memories:
            self.sqlite_manager.add_memory(agent_id, mem_type, content)

        # Test various search queries
        react_results = self.sqlite_manager.search_memories("React")
        assert len(react_results) == 2

        api_results = self.sqlite_manager.search_memories("API")
        assert len(api_results) == 3  # "backend API", "REST API", "context API"

        agent1_react = self.sqlite_manager.search_memories("React", agent_id="agent-1")
        assert len(agent1_react) == 1

        decision_results = self.sqlite_manager.search_memories("framework", memory_type="decision")
        assert len(decision_results) == 1

        # Migrate to markdown and verify search capability through file content
        self.migration_manager.migrate_sqlite_to_markdown()

        agent1_file = self.agor_dir / "agent-1-memory.md"
        content = agent1_file.read_text()
        assert "React frontend" in content
        assert "Material-UI" in content

    def test_system_interchangeability(self):
        """Test that systems can be used interchangeably without data loss."""
        # Start with markdown system
        self._create_sample_markdown_files()

        # Migrate to SQLite
        stats = self.migration_manager.migrate_markdown_to_sqlite()
        original_counts = {
            "memories": stats["agent_memories"],
            "coordination": stats["coordination_logs"],
            "state": stats["project_state"]
        }

        # Work with SQLite system
        self.sqlite_manager.add_memory("agent-3", "context", "New work in SQLite")
        self.sqlite_manager.log_coordination("agent-3", "agent-1", "status", "SQLite system working")

        # Migrate back to markdown
        stats = self.migration_manager.migrate_sqlite_to_markdown(overwrite_existing=True)

        # Verify no data loss and new data included
        agent3_file = self.agor_dir / "agent-3-memory.md"
        assert agent3_file.exists()

        content = agent3_file.read_text()
        assert "New work in SQLite" in content

        agentconvo_file = self.agor_dir / "agentconvo.md"
        content = agentconvo_file.read_text()
        assert "SQLite system working" in content

        # Migrate back to SQLite again
        new_sqlite = SQLiteMemoryManager(str(self.agor_dir / "final_test.db"))
        final_migration = MemoryMigrationManager(self.agor_dir)
        final_migration.sqlite_manager = new_sqlite

        stats = final_migration.migrate_markdown_to_sqlite()

        # Verify all data is preserved
        all_memories = new_sqlite.get_memories("agent-3")
        assert len(all_memories) >= 1

        coordination_logs = new_sqlite.get_coordination_logs("agent-3")
        assert len(coordination_logs) >= 1

    def _create_sample_markdown_files(self):
        """Create sample markdown files for testing."""
        # Create agent memory files
        agent1_memory = self.agor_dir / "agent-1-memory.md"
        agent1_memory.write_text("""# AGENT-1 Memory File

## Current Task
Implementing user authentication system

## Decisions Made
- Chose JWT tokens for session management
- Using bcrypt for password hashing
- Implementing rate limiting for login attempts

## Files Modified
- auth/middleware.js
- routes/auth.js
- models/user.js

## Next Steps
- Add password reset functionality
- Implement 2FA support
- Write comprehensive tests
""")

        agent2_memory = self.agor_dir / "agent-2-memory.md"
        agent2_memory.write_text("""# AGENT-2 Memory File

## Current Task
Building React frontend components

## Decisions Made
- Using Material-UI for component library
- Implementing React hooks for state management
- Adding TypeScript for type safety

## Progress
- Login form component complete
- User dashboard in progress
- API integration 70% done
""")

        # Create agentconvo.md
        agentconvo = self.agor_dir / "agentconvo.md"
        agentconvo.write_text("""# Agent Communication Log

Format: [AGENT-ID] [TIMESTAMP] - [STATUS/QUESTION/FINDING]

## Communication History

[agent-1] [2024-01-27 10:00] - Starting authentication system implementation
[agent-2] [2024-01-27 10:15] - Beginning frontend component development
[agent-1] [2024-01-27 11:30] - JWT middleware complete, testing in progress
[agent-2] [2024-01-27 12:00] - Login form component ready for integration
[agent-1] [2024-01-27 14:00] - Authentication API endpoints complete
[agent-2] [2024-01-27 15:30] - Frontend integration successful, testing UI flows
""")

        # Create memory.md
        memory = self.agor_dir / "memory.md"
        memory.write_text("""# Project Memory

## Task
Build secure web application with user authentication

## Team Configuration
- Agents: 2
- Initialized: 2024-01-27 09:00:00

## Key Decisions
- JWT-based authentication
- React frontend with Material-UI
- Node.js/Express backend
- PostgreSQL database

## Current State
- Authentication system: 80% complete
- Frontend components: 60% complete
- Integration testing: In progress
""")

        # Create handoff directory and file
        handoff_dir = self.agor_dir / "handoffs"
        handoff_dir.mkdir(exist_ok=True)

        handoff_file = handoff_dir / "2024-01-27_143022_auth-implementation.md"
        handoff_file.write_text("""# 🤝 Agent Handoff Document

**Handoff ID**: 2024-01-27_143022_auth-implementation
**From**: agent-1
**To**: agent-2
**Status**: active
**Created**: 2024-01-27 14:30:22

## Problem Description
Complete user authentication system implementation and integrate with frontend

## Work Completed
- JWT middleware implementation
- Login/logout API endpoints
- Password hashing with bcrypt
- Basic rate limiting
- Unit tests for auth functions

## Commits Made
abc123: Add JWT middleware
def456: Implement login endpoint
ghi789: Add password hashing and rate limiting

## Files Modified
- auth/middleware.js
- routes/auth.js
- models/user.js
- tests/auth.test.js

## Current Status
Authentication backend is complete and tested. Ready for frontend integration.

## Next Steps
1. Create login/register forms in React
2. Integrate forms with authentication API
3. Add error handling and user feedback
4. Implement password reset functionality
5. Add comprehensive integration tests

## Context Notes
JWT secret is stored in .env file. Database migrations are in migrations/ folder.
API documentation is in docs/auth.md. Rate limiting is set to 5 attempts per minute.

## Git Information
**Branch**: feature/authentication
**Commit**: ghi789

**AGOR Version**: 0.2.4
""")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
