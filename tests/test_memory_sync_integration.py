"""
Integration tests for memory sync workflows in agent coordination.

Tests the production integration of memory sync with agent initialization,
completion, and coordination workflows.
"""

import shutil
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from agor.strategy import StrategyManager
from agor.tools.agent_coordination import AgentCoordinationHelper


class TestMemorySyncIntegration:
    """Test memory sync integration with agent workflows."""

    @pytest.fixture
    def temp_project(self):
        """Create a temporary project directory for testing."""
        temp_dir = Path(tempfile.mkdtemp())
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def strategy_manager(self, temp_project):
        """Create a StrategyManager instance for testing."""
        return StrategyManager(project_root=temp_project)

    @pytest.fixture
    def agent_helper(self, temp_project):
        """Create an AgentCoordinationHelper instance for testing."""
        return AgentCoordinationHelper(project_root=temp_project)

    def test_strategy_initialization_includes_memory_sync(
        self, strategy_manager, temp_project
    ):
        """Test that strategy initialization includes memory sync setup."""
        # Initialize coordination
        strategy_manager.init_coordination("test task", 3)

        # Verify .agor directory was created
        agor_dir = temp_project / ".agor"
        assert agor_dir.exists()

        # Verify memory manager has memory sync capabilities
        assert strategy_manager.memory_manager is not None

    def test_agent_discovery_initializes_memory_sync(self, agent_helper, temp_project):
        """Test that agent discovery initializes memory sync."""
        # Create .agor directory first
        agor_dir = temp_project / ".agor"
        agor_dir.mkdir()

        # Mock memory sync to avoid actual Git operations
        with patch("agor.tools.agent_coordination.MemorySyncManager") as mock_memory:
            mock_instance = MagicMock()
            mock_instance.get_active_memory_branch.return_value = "test-branch"
            mock_memory.return_value = mock_instance

            # Discover situation should initialize memory sync
            agent_helper.discover_current_situation("agent1")

            # Verify MemorySyncManager was called
            mock_memory.assert_called_once()

    def test_agent_completion_saves_memory_state(self, agent_helper, temp_project):
        """Test that agent completion saves memory state."""
        # Create .agor directory
        agor_dir = temp_project / ".agor"
        agor_dir.mkdir()

        # Mock memory sync to avoid actual Git operations
        with patch("agor.tools.agent_coordination.MemorySyncManager") as mock_memory:
            mock_instance = MagicMock()
            mock_instance.get_active_memory_branch.return_value = "test-branch"
            mock_instance.auto_sync_on_shutdown.return_value = True
            mock_memory.return_value = mock_instance

            # Complete agent work
            success = agent_helper.complete_agent_work("agent1", "Test completion")

            # Verify completion was successful
            assert success

            # Verify auto_sync_on_shutdown was called with correct parameters
            mock_instance.auto_sync_on_shutdown.assert_called_once_with(
                target_branch_name="test-branch",
                commit_message="agent1: Test completion",
                push_changes=True,
                restore_original_branch=None,
            )

    def test_strategy_status_shows_memory_sync_info(
        self, strategy_manager, temp_project, capsys
    ):
        """Test that strategy status includes memory sync information."""
        # Initialize coordination to create .agor directory
        strategy_manager.init_coordination("test task", 3)

        # Mock memory sync to control output
        with patch.object(
            strategy_manager.memory_manager, "memory_sync_manager", MagicMock()
        ):
            with patch.object(
                strategy_manager.memory_manager,
                "active_memory_branch_name",
                "test-branch",
            ):
                # Show status
                strategy_manager.show_status()

                # Capture output
                captured = capsys.readouterr()

                # Verify memory sync status is shown
                assert "Memory Sync" in captured.out
                assert "test-branch" in captured.out

    def test_memory_sync_graceful_failure(self, agent_helper, temp_project):
        """Test that memory sync failures don't break agent workflows."""
        # Create .agor directory
        agor_dir = temp_project / ".agor"
        agor_dir.mkdir()

        # Mock memory sync to simulate failure
        with patch("agor.tools.agent_coordination.MemorySyncManager") as mock_memory:
            mock_instance = MagicMock()
            mock_instance.get_active_memory_branch.return_value = "test-branch"
            mock_instance.auto_sync_on_shutdown.return_value = False  # Simulate failure
            mock_memory.return_value = mock_instance

            # Complete agent work should still succeed even if memory sync fails
            success = agent_helper.complete_agent_work("agent1", "Test completion")

            # Completion should report failure due to memory sync issue
            assert not success

    def test_memory_sync_without_agor_directory(self, agent_helper, temp_project):
        """Test memory sync behavior when .agor directory doesn't exist."""
        # Don't create .agor directory

        # Agent completion should still work without .agor directory
        success = agent_helper.complete_agent_work("agent1", "Test completion")

        # Should succeed even without .agor directory
        assert success

    def test_memory_sync_initialization_error_handling(
        self, agent_helper, temp_project, capsys
    ):
        """Test error handling during memory sync initialization."""
        # Create .agor directory
        agor_dir = temp_project / ".agor"
        agor_dir.mkdir()

        # Mock MemorySyncManager to raise an exception
        with patch(
            "agor.tools.agent_coordination.MemorySyncManager",
            side_effect=Exception("Test error"),
        ):
            # Agent discovery should handle the error gracefully
            result = agent_helper.discover_current_situation("agent1")

            # Should still return a result
            assert result is not None

            # Should show warning message
            captured = capsys.readouterr()
            assert "memory sync initialization warning" in captured.out

    def test_parallel_divergent_strategy_with_memory_sync(
        self, strategy_manager, temp_project
    ):
        """Test that parallel divergent strategy works with memory sync."""
        # Set up parallel divergent strategy
        strategy_manager.setup_parallel_divergent("test parallel task", 3)

        # Verify .agor directory structure
        agor_dir = temp_project / ".agor"
        assert agor_dir.exists()
        # Verify memory manager is initialized
        assert strategy_manager.memory_manager is not None

    def test_memory_sync_with_multiple_agents(self, temp_project):
        """Test memory sync coordination with multiple agents."""
        # Create multiple agent helpers
        agent1 = AgentCoordinationHelper(project_root=temp_project)
        agent2 = AgentCoordinationHelper(project_root=temp_project)

        # Create .agor directory
        agor_dir = temp_project / ".agor"
        agor_dir.mkdir()

        # Mock memory sync for both agents
        with patch("agor.tools.agent_coordination.MemorySyncManager") as mock_memory:
            mock_instance = MagicMock()
            mock_instance.get_active_memory_branch.return_value = "test-branch"
            mock_instance.auto_sync_on_shutdown.return_value = True
            mock_memory.return_value = mock_instance

            # Both agents should be able to complete work
            success1 = agent1.complete_agent_work("agent1", "Agent 1 completion")
            success2 = agent2.complete_agent_work("agent2", "Agent 2 completion")

            assert success1
            assert success2

            # Verify both agents called memory sync
            assert mock_instance.auto_sync_on_shutdown.call_count == 2


if __name__ == "__main__":
    pytest.main([__file__])
