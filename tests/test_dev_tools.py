"""
Comprehensive unit tests for AGOR dev_tools module.

This test suite covers all functionality in the dev_tools module including:
- Snapshot creation and agent handoffs
- Memory management operations  
- Git operations and utilities
- Workspace status and health checks
- Checklist and workflow functions
- Output formatting and validation
- Agent coordination and cleanup

Testing Framework: pytest (as specified in pyproject.toml)
"""

import pytest
from unittest.mock import Mock, patch
import os
import sys
from datetime import datetime

# Add the src directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import the dev_tools module
from agor.tools import dev_tools

# -----------------------
# Fixtures for test data
# -----------------------

@pytest.fixture
def mock_git_success():
    """Fixture providing successful git command mock."""
    mock_result = Mock()
    mock_result.returncode = 0
    mock_result.stdout = "success"
    mock_result.stderr = ""
    return mock_result

@pytest.fixture
def mock_git_failure():
    """Fixture providing failed git command mock."""
    mock_result = Mock()
    mock_result.returncode = 1
    mock_result.stdout = ""
    mock_result.stderr = "git command failed"
    return mock_result

@pytest.fixture
def sample_agent_id():
    """Fixture providing a test agent ID."""
    return "test_agent_12345_1234567890"

@pytest.fixture
def sample_memory_branch():
    """Fixture providing a test memory branch name."""
    return "agor/mem/main"

@pytest.fixture
def sample_snapshot_data():
    """Fixture providing sample snapshot data."""
    return {
        "title": "Test Development Snapshot",
        "context": "Testing snapshot creation functionality",
        "next_steps": ["Continue testing", "Review implementation", "Add more tests"],
        "agent_id": "test_agent_123",
        "custom_branch": None
    }

@pytest.fixture
def sample_handoff_data():
    """Fixture providing sample handoff data."""
    return {
        "task_description": "Complete testing implementation",
        "work_completed": ["Created test fixtures", "Implemented core tests"],
        "next_steps": ["Add edge case tests", "Review test coverage"],
        "files_modified": ["tests/test_dev_tools.py"],
        "context_notes": "All core functionality tested",
        "brief_context": "Test implementation in progress"
    }

@pytest.fixture
def temp_workspace(tmp_path):
    """Fixture providing a temporary workspace directory."""
    workspace = tmp_path / "test_workspace"
    workspace.mkdir()
    (workspace / "sample.py").write_text("print('test')")
    (workspace / "README.md").write_text("# Test Project")
    return workspace

@pytest.fixture
def mock_current_timestamp():
    """Fixture providing a consistent timestamp for testing."""
    return "2024-01-01T12:00:00Z"

@pytest.fixture(autouse=True)
def reset_global_state():
    """Auto-used fixture to reset any global state between tests."""
    yield
    # Reset global variables or caches if needed

# ------------------------------
# Tests for main API functions
# ------------------------------

class TestMainAPIFunctions:
    """Test suite for main API functions in dev_tools."""
    
    @patch('agor.tools.dev_tools.create_snapshot')
    def test_create_development_snapshot_success(self, mock_create_snapshot, sample_snapshot_data):
        mock_create_snapshot.return_value = True
        result = dev_tools.create_development_snapshot(
            title=sample_snapshot_data["title"],
            context=sample_snapshot_data["context"],
            next_steps=sample_snapshot_data["next_steps"],
            agent_id=sample_snapshot_data["agent_id"]
        )
        assert result is True
        mock_create_snapshot.assert_called_once_with(
            sample_snapshot_data["title"],
            sample_snapshot_data["context"],
            sample_snapshot_data["next_steps"],
            sample_snapshot_data["agent_id"],
            None
        )
    
    @patch('agor.tools.dev_tools.create_snapshot')
    def test_create_development_snapshot_failure(self, mock_create_snapshot, sample_snapshot_data):
        mock_create_snapshot.return_value = False
        result = dev_tools.create_development_snapshot(
            title=sample_snapshot_data["title"],
            context=sample_snapshot_data["context"]
        )
        assert result is False
        mock_create_snapshot.assert_called_once()
    
    def test_create_development_snapshot_with_empty_title(self):
        with patch('agor.tools.dev_tools.create_snapshot') as mock_create:
            mock_create.return_value = True
            _ = dev_tools.create_development_snapshot(title="", context="Test context")
            mock_create.assert_called_once_with("", "Test context", None, None, None)
    
    @patch('agor.tools.dev_tools.create_seamless_handoff')
    def test_generate_seamless_agent_handoff_success(self, mock_handoff, sample_handoff_data):
        expected = ("handoff_content", "formatted_prompt")
        mock_handoff.return_value = expected
        result = dev_tools.generate_seamless_agent_handoff(
            task_description=sample_handoff_data["task_description"],
            work_completed=sample_handoff_data["work_completed"],
            next_steps=sample_handoff_data["next_steps"],
            files_modified=sample_handoff_data["files_modified"],
            context_notes=sample_handoff_data["context_notes"],
            brief_context=sample_handoff_data["brief_context"]
        )
        assert result == expected
        mock_handoff.assert_called_once_with(
            task_description=sample_handoff_data["task_description"],
            work_completed=sample_handoff_data["work_completed"],
            next_steps=sample_handoff_data["next_steps"],
            files_modified=sample_handoff_data["files_modified"],
            context_notes=sample_handoff_data["context_notes"],
            brief_context=sample_handoff_data["brief_context"]
        )
    
    @patch('agor.tools.dev_tools.generate_mandatory_session_end_prompt')
    def test_generate_session_end_prompt_with_defaults(self, mock_prompt):
        mock_prompt.return_value = "Session completed successfully"
        result = dev_tools.generate_session_end_prompt()
        assert result == "Session completed successfully"
        mock_prompt.assert_called_once_with("Session completion", "Work session completed")

    @patch('agor.tools.dev_tools.generate_mandatory_session_end_prompt')
    def test_generate_session_end_prompt_with_custom_params(self, mock_prompt):
        mock_prompt.return_value = "Custom session end prompt"
        result = dev_tools.generate_session_end_prompt(
            task_description="Custom task completed",
            brief_context="Custom context provided"
        )
        assert result == "Custom session end prompt"
        mock_prompt.assert_called_once_with("Custom task completed", "Custom context provided")
    
    @patch('agor.tools.dev_tools.generate_agent_handoff_prompt')
    def test_generate_project_handoff_prompt(self, mock_prompt):
        mock_prompt.return_value = "Project handoff prompt generated"
        result = dev_tools.generate_project_handoff_prompt(
            task_description="Complete project handoff",
            snapshot_content="Snapshot data",
            memory_branch="agor/mem/main",
            environment={"test": True},
            brief_context="Project context"
        )
        assert result == "Project handoff prompt generated"
        mock_prompt.assert_called_once_with(
            task_description="Complete project handoff",
            snapshot_content="Snapshot data",
            memory_branch="agor/mem/main",
            environment={"test": True},
            brief_context="Project context"
        )

# -------------------------------
# Tests for convenience wrappers
# -------------------------------

class TestConvenienceFunctions:
    """Test suite for convenience wrapper functions."""
    
    @patch('agor.tools.dev_tools.quick_commit_push')
    def test_quick_commit_and_push_success(self, mock_commit_push):
        mock_commit_push.return_value = True
        result = dev_tools.quick_commit_and_push("Test commit message", "🚀")
        assert result is True
        mock_commit_push.assert_called_once_with("Test commit message", "🚀")

    @patch('agor.tools.dev_tools.quick_commit_push')
    def test_quick_commit_and_push_with_default_emoji(self, mock_commit_push):
        mock_commit_push.return_value = True
        result = dev_tools.quick_commit_and_push("Test commit")
        assert result is True
        mock_commit_push.assert_called_once_with("Test commit", "🔧")

    @patch('agor.tools.dev_tools.quick_commit_push')
    def test_quick_commit_and_push_failure(self, mock_commit_push):
        mock_commit_push.return_value = False
        result = dev_tools.quick_commit_and_push("Failed commit")
        assert result is False
        mock_commit_push.assert_called_once()
    
    @patch('agor.tools.dev_tools.auto_commit_memory')
    def test_commit_memory_to_branch_success(self, mock_auto_commit):
        mock_auto_commit.return_value = True
        result = dev_tools.commit_memory_to_branch(content="Memory content", memory_type="snapshot", agent_id="test_agent")
        assert result is True
        mock_auto_commit.assert_called_once_with("Memory content", "snapshot", "test_agent")
    
    @patch('agor.tools.dev_tools.auto_commit_memory')
    def test_commit_memory_to_branch_with_defaults(self, mock_auto_commit):
        mock_auto_commit.return_value = True
        result = dev_tools.commit_memory_to_branch(content="Default memory content", memory_type="log")
        assert result is True
        mock_auto_commit.assert_called_once_with("Default memory content", "log", "dev")
    
    def test_get_snapshot_guidelines_summary_with_print(self, capsys):
        result = dev_tools.get_snapshot_guidelines_summary(print_output=True)
        captured = capsys.readouterr()
        assert "AGOR Snapshot Guidelines Summary" in result
        assert "AGOR Snapshot Guidelines Summary" in captured.out
        assert "Core Purpose" in result
        assert "Key Functions for Snapshots" in result
    
    def test_get_snapshot_guidelines_summary_without_print(self, capsys):
        result = dev_tools.get_snapshot_guidelines_summary(print_output=False)
        captured = capsys.readouterr()
        assert "AGOR Snapshot Guidelines Summary" in result
        assert captured.out == ""
    
    def test_display_memory_architecture_info_with_print(self, capsys):
        result = dev_tools.display_memory_architecture_info(print_output=True)
        captured = capsys.readouterr()
        assert "AGOR Memory Architecture Summary" in result
        assert "AGOR Memory Architecture Summary" in captured.out
        assert "Memory Branch Naming" in result
    
    def test_display_memory_architecture_info_without_print(self, capsys):
        result = dev_tools.display_memory_architecture_info(print_output=False)
        captured = capsys.readouterr()
        assert "AGOR Memory Architecture Summary" in result
        assert captured.out == ""

# -------------------------------------
# Tests for content processing & format
# -------------------------------------

class TestContentProcessing:
    """Test suite for content processing and formatting functions."""
    
    @patch('agor.tools.dev_tools.detick_content')
    def test_process_content_for_codeblock(self, mock_detick):
        input_content = "Some content with ```code``` blocks"
        mock_detick.return_value = "Some content with code blocks"
        result = dev_tools.process_content_for_codeblock(input_content)
        assert result == "Some content with code blocks"
        mock_detick.assert_called_once_with(input_content)
    
    @patch('agor.tools.dev_tools.retick_content')
    def test_restore_content_from_codeblock(self, mock_retick):
        input_content = "Some content with code blocks"
        mock_retick.return_value = "Some content with ```code``` blocks"
        result = dev_tools.restore_content_from_codeblock(input_content)
        assert result == "Some content with ```code``` blocks"
        mock_retick.assert_called_once_with(input_content)
    
    def test_validate_output_formatting_compliant_content(self):
        compliant_content = "This is clean content without issues"
        result = dev_tools.validate_output_formatting(compliant_content)
        assert result["is_compliant"] is True
        assert result["has_codeblocks"] is False
        assert result["has_triple_backticks"] is False
        assert result["detick_needed"] is False
        assert len(result["issues"]) == 0
    
    def test_validate_output_formatting_with_codeblocks(self):
        content = "Content with ```python\ncode here\n``` blocks"
        result = dev_tools.validate_output_formatting(content)
        assert result["has_codeblocks"] is True
        assert result["has_triple_backticks"] is True
        assert result["detick_needed"] is True
        assert "triple backticks" in str(result["issues"])
        assert "detick_content()" in str(result["suggestions"])
    
    def test_validate_output_formatting_handoff_content(self):
        content = "This is a handoff prompt with ```code```"
        result = dev_tools.validate_output_formatting(content)
        assert result["is_compliant"] is False
        assert "handoff prompts must be deticked" in str(result["issues"]).lower()
    
    @patch('agor.tools.dev_tools.detick_content')
    def test_apply_output_formatting(self, mock_detick):
        mock_detick.return_value = "Content with backticks"
        result = dev_tools.apply_output_formatting("Content with ```backticks```", "test")
        assert result == "``\nContent with backticks\n``"
        mock_detick.assert_called_once()
    
    @patch('agor.tools.dev_tools.apply_output_formatting')
    def test_generate_formatted_output(self, mock_apply):
        mock_apply.return_value = "``\nFormatted content\n``"
        result = dev_tools.generate_formatted_output("Raw content", "general")
        assert result == "``\nFormatted content\n``"
        mock_apply.assert_called_once_with("Raw content", "general")
    
    @patch('agor.tools.dev_tools.generate_formatted_output')
    def test_generate_handoff_prompt_output(self, mock_generate):
        mock_generate.return_value = "``\nHandoff prompt\n``"
        result = dev_tools.generate_handoff_prompt_output("Raw handoff content")
        assert result == "``\nHandoff prompt\n``"
        mock_generate.assert_called_once_with("Raw handoff content", "handoff_prompt")

# ------------------------------------
# Tests for git branch & cleanup ops
# ------------------------------------

class TestGitBranchOperations:
    """Test suite for git branch operations and parsing."""
    
    def test_parse_git_branches_with_memory_branches(self):
        output = """
        * main
          feature/test
          agor/mem/main
          agor/mem/agent_123
          remotes/origin/main
          remotes/origin/agor/mem/main
          remotes/origin/agor/mem/agent_456
        """
        local, remote = dev_tools._parse_git_branches(output)
        assert "agor/mem/main" in local and "agor/mem/agent_123" in local
        assert "agor/mem/main" in remote and "agor/mem/agent_456" in remote
        assert len(local) == 2 and len(remote) == 2
    
    def test_parse_git_branches_empty_output(self):
        local, remote = dev_tools._parse_git_branches("")
        assert local == [] and remote == []
    
    def test_parse_git_branches_no_memory_branches(self):
        output = """
        * main
          feature/test
          remotes/origin/main
          remotes/origin/feature/test
        """
        local, remote = dev_tools._parse_git_branches(output)
        assert local == [] and remote == []
    
    @patch('agor.tools.dev_tools.run_git_command')
    def test_delete_local_branches_success(self, mock_git):
        mock_git.return_value = (True, "Branch deleted")
        results = {"deleted_local": [], "failed": []}
        dev_tools._delete_local_branches(["agor/mem/test1","agor/mem/test2"], results)
        assert len(results["deleted_local"]) == 2 and not results["failed"]
    
    @patch('agor.tools.dev_tools.run_git_command')
    def test_delete_local_branches_failure(self, mock_git):
        mock_git.return_value = (False, "Permission denied")
        results = {"deleted_local": [], "failed": []}
        dev_tools._delete_local_branches(["agor/mem/test1"], results)
        assert not results["deleted_local"]
        assert "local:agor/mem/test1" in results["failed"]
    
    @patch('agor.tools.dev_tools.run_git_command')
    def test_delete_remote_branches_success(self, mock_git):
        mock_git.return_value = (True, "Remote branch deleted")
        results = {"deleted_remote": [], "failed": []}
        dev_tools._delete_remote_branches(["agor/mem/remote1","agor/mem/remote2"], results)
        assert len(results["deleted_remote"]) == 2 and not results["failed"]
    
    @patch('agor.tools.dev_tools.run_git_command')
    def test_delete_remote_branches_permission_denied(self, mock_git):
        mock_git.return_value = (False, "Permission denied error")
        results = {"deleted_remote": [], "failed": []}
        dev_tools._delete_remote_branches(["agor/mem/remote1"], results)
        assert not results["deleted_remote"]
        assert "permission_denied" in results["failed"][0]
    
    @patch('agor.tools.dev_tools.run_git_command')
    def test_delete_remote_branches_network_error(self, mock_git):
        mock_git.return_value = (False, "Network connection failed")
        results = {"deleted_remote": [], "failed": []}
        dev_tools._delete_remote_branches(["agor/mem/remote1"], results)
        assert not results["deleted_remote"]
        assert "network_error" in results["failed"][0]

# --------------------------------------------
# Tests for memory management & agent helpers
# --------------------------------------------

class TestMemoryManagement:
    """Test suite for memory management and agent functions."""
    
    def test_generate_unique_agent_id_format(self):
        agent_id = dev_tools.generate_unique_agent_id()
        assert agent_id.startswith("agent_")
        parts = agent_id.split("_")
        assert len(parts) == 3 and len(parts[1]) == 8 and parts[2].isdigit()
    
    def test_generate_unique_agent_id_uniqueness(self):
        assert dev_tools.generate_unique_agent_id() != dev_tools.generate_unique_agent_id()
    
    def test_generate_agent_id_calls_unique_generator(self):
        with patch('agor.tools.dev_tools.generate_unique_agent_id') as mock_unique:
            mock_unique.return_value = "test_agent_id"
            assert dev_tools.generate_agent_id() == "test_agent_id"
            mock_unique.assert_called_once()
    
    def test_get_main_memory_branch_default(self):
        assert dev_tools.get_main_memory_branch() == "agor/mem/main"
    
    def test_get_main_memory_branch_custom(self):
        assert dev_tools.get_main_memory_branch("custom/branch") == "custom/branch"
    
    def test_get_agent_directory_path(self):
        assert dev_tools.get_agent_directory_path("test_agent_123") == ".agor/agents/test_agent_123/"
    
    @patch('agor.tools.dev_tools.generate_agent_id')
    @patch('agor.tools.dev_tools.get_current_timestamp')
    @patch('agor.tools.dev_tools.commit_memory_to_branch')
    def test_initialize_agent_workspace_success(self, mock_commit, mock_ts, mock_gen):
        mock_gen.return_value = "test_agent_123"
        mock_ts.return_value = "2024-01-01T12:00:00Z"
        mock_commit.return_value = True
        success, aid, branch = dev_tools.initialize_agent_workspace()
        assert success and aid == "test_agent_123" and branch == "agor/mem/main"
        assert mock_commit.call_count == 2
    
    @patch('agor.tools.dev_tools.commit_memory_to_branch')
    def test_initialize_agent_workspace_with_params(self, mock_commit):
        mock_commit.return_value = True
        success, aid, branch = dev_tools.initialize_agent_workspace(agent_id="custom_agent", custom_branch="custom/branch")
        assert success and aid == "custom_agent" and branch == "custom/branch"
    
    @patch('agor.tools.dev_tools.commit_memory_to_branch')
    def test_initialize_agent_workspace_failure(self, mock_commit):
        mock_commit.return_value = False
        success, aid, branch = dev_tools.initialize_agent_workspace(agent_id="test_agent")
        assert not success and aid == "test_agent" and branch == "agor/mem/main"
    
    @patch('agor.tools.dev_tools.commit_memory_to_branch')
    def test_initialize_agent_workspace_exception(self, mock_commit):
        mock_commit.side_effect = Exception("Commit failed")
        success, aid, branch = dev_tools.initialize_agent_workspace(agent_id="test_agent")
        assert not success and aid == "test_agent" and branch == "agor/mem/main"
    
    def test_get_or_create_agent_id_file_create_new(self):
        with patch.multiple(
            'pathlib.Path',
            mkdir=Mock(),
            exists=Mock(return_value=False),
            read_text=Mock(),
            write_text=Mock()
        ), patch('tempfile.gettempdir', return_value="/tmp"), \
           patch('agor.tools.dev_tools.generate_unique_agent_id', return_value="new_agent_123"):
            result = dev_tools.get_or_create_agent_id_file()
            assert result == "new_agent_123"
    
    @patch('tempfile.gettempdir')
    @patch('pathlib.Path.read_text')
    @patch('pathlib.Path.exists')
    def test_get_or_create_agent_id_file_read_existing(self, mock_exists, mock_read, mock_temp):
        mock_temp.return_value = "/tmp"
        mock_exists.return_value = True
        mock_read.return_value = "existing_agent_456"
        assert dev_tools.get_or_create_agent_id_file() == "existing_agent_456"

# ------------------------------------------------
# Tests for workflow prompts, validation & guides
# ------------------------------------------------

class TestWorkflowAndValidation:
    """Test suite for workflow and validation functions."""
    
    @patch('agor.tools.dev_tools.get_current_timestamp')
    @patch('agor.tools.dev_tools.get_main_memory_branch')
    def test_generate_workflow_prompt_template_minimal(self, mock_branch, mock_ts):
        mock_ts.return_value = "2024-01-01T12:00:00Z"
        mock_branch.return_value = "agor/mem/main"
        result = dev_tools.generate_workflow_prompt_template("Test task")
        assert "# 🎯 AGOR Agent Task: Test task" in result
        assert "2024-01-01T12:00:00Z" in result
        assert "agor/mem/main" in result
    
    def test_generate_workflow_prompt_template_custom_branch(self):
        result = dev_tools.generate_workflow_prompt_template("Custom task", memory_branch="custom/mem/branch")
        assert "custom/mem/branch" in result
        assert "# 🎯 AGOR Agent Task: Custom task" in result
    
    def test_generate_workflow_prompt_template_no_bookend(self):
        result = dev_tools.generate_workflow_prompt_template("Test task", include_bookend=False)
        assert "Session Start Requirements" not in result
        assert "Development Guidelines" in result
    
    def test_generate_workflow_prompt_template_no_explicit_requirements(self):
        result = dev_tools.generate_workflow_prompt_template("Test task", include_explicit_requirements=False)
        assert "MANDATORY SESSION END REQUIREMENTS" not in result
        assert "Success Criteria" in result
    
    def test_validate_agor_workflow_completion_complete(self):
        result = dev_tools.validate_agor_workflow_completion(
            work_completed=["Task 1","Task 2"],
            files_modified=["file1.py","file2.md"],
            has_snapshot=True,
            has_handoff_prompt=True
        )
        assert result["is_complete"] and result["score"] == 10
    
    def test_validate_agor_workflow_completion_incomplete(self):
        result = dev_tools.validate_agor_workflow_completion(
            work_completed=[],
            files_modified=[],
            has_snapshot=False,
            has_handoff_prompt=False
        )
        assert not result["is_complete"] and result["score"] == 0
        assert "Create development snapshot" in str(result["missing_requirements"])
    
    def test_validate_agor_workflow_completion_partial(self):
        result = dev_tools.validate_agor_workflow_completion(
            work_completed=["Some work"],
            files_modified=["file.py"],
            has_snapshot=True,
            has_handoff_prompt=False
        )
        assert not result["is_complete"] and result["score"] == 7
    
    @patch('agor.tools.dev_tools.get_current_timestamp')
    def test_get_workflow_optimization_tips(self, mock_ts):
        mock_ts.return_value = "2024-01-01T12:00:00Z"
        result = dev_tools.get_workflow_optimization_tips()
        assert "AGOR Workflow Optimization Tips" in result
    
    def test_get_agor_initialization_guide(self):
        result = dev_tools.get_agor_initialization_guide()
        assert "AGOR INITIALIZATION GUIDE" in result
    
    def test_get_snapshot_requirements(self):
        result = dev_tools.get_snapshot_requirements()
        assert "SNAPSHOT REQUIREMENTS" in result

# ---------------------------------------
# Edge cases, error handling & sanitization
# ---------------------------------------

class TestEdgeCasesAndErrorHandling:
    """Test suite for edge cases and error handling scenarios."""
    
    def test_validate_output_formatting_edge_cases(self):
        with pytest.raises(AttributeError):
            dev_tools.validate_output_formatting(None)
        assert dev_tools.validate_output_formatting("")["is_compliant"]
        assert dev_tools.validate_output_formatting("   \n\t  ")["is_compliant"]
        assert dev_tools.validate_output_formatting("Special chars: @#$%^&*()")["is_compliant"]
    
    def test_memory_branch_operations_with_invalid_input(self):
        assert dev_tools.get_agent_directory_path("") == ".agor/agents//"
        with pytest.raises(TypeError):
            dev_tools.get_agent_directory_path(None)
    
    @patch('agor.tools.dev_tools.sanitize_slug')
    def test_agent_id_sanitization(self, mock_sanitize):
        mock_sanitize.return_value = "sanitized_agent_id"
        with patch('tempfile.gettempdir'), patch('pathlib.Path.mkdir'), patch('pathlib.Path.write_text'):
            result = dev_tools.get_or_create_agent_id_file("unsafe@agent#id")
            mock_sanitize.assert_called_once()
            assert result == "sanitized_agent_id"
    
    @patch('agor.tools.dev_tools.test_tooling')
    def test_test_all_tools_success(self, mock_tooling):
        mock_tooling.return_value = True
        assert dev_tools.test_all_tools() is True
    
    @patch('agor.tools.dev_tools.test_tooling')
    def test_test_all_tools_failure(self, mock_tooling):
        mock_tooling.return_value = False
        assert dev_tools.test_all_tools() is False
    
    @patch('agor.tools.dev_tools.detect_environment')
    def test_detect_current_environment(self, mock_detect):
        expected = {"platform": "linux", "python_version": "3.9"}
        mock_detect.return_value = expected
        assert dev_tools.detect_current_environment() == expected

# ------------------------------
# Integration-style test flows
# ------------------------------

class TestIntegrationScenarios:
    """Integration-style tests for complex workflows."""
    
    @patch('agor.tools.dev_tools.create_development_snapshot')
    @patch('agor.tools.dev_tools.generate_session_end_prompt')
    @patch('agor.tools.dev_tools.apply_output_formatting')
    def test_complete_session_workflow(self, mock_format, mock_prompt, mock_snapshot):
        mock_snapshot.return_value = True
        mock_prompt.return_value = "Session end prompt"
        mock_format.return_value = "``\nFormatted prompt\n``"
        assert dev_tools.create_development_snapshot(title="Test Session", context="Session context", next_steps=["Step 1","Step 2"])
        assert dev_tools.generate_session_end_prompt(task_description="Test task", brief_context="Test context") == "Session end prompt"
        assert dev_tools.apply_output_formatting("Session end prompt", "handoff") == "``\nFormatted prompt\n``"

# ----------------------------------
# Performance and stress scenarios
# ----------------------------------

@pytest.mark.slow
class TestPerformanceScenarios:
    """Performance tests for dev_tools functionality."""
    
    def test_large_content_formatting(self):
        large_content = "x" * (1024*1024)
        with patch('agor.tools.dev_tools.detick_content') as mock_detick:
            mock_detick.return_value = large_content
            start = datetime.now()
            result = dev_tools.apply_output_formatting(large_content, "test")
            duration = (datetime.now() - start).total_seconds()
            assert duration < 5.0
            assert len(result) > len(large_content)
    
    def test_multiple_agent_id_generation_performance(self):
        start = datetime.now()
        ids = [dev_tools.generate_unique_agent_id() for _ in range(100)]
        duration = (datetime.now() - start).total_seconds()
        assert duration < 1.0
        assert len(set(ids)) == 100