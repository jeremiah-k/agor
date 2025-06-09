"""
AGOR Development Tooling - Main Interface Module

This module provides the main interface for AGOR development utilities.
It imports functionality from specialized modules for better organization:

- snapshots: Snapshot creation and agent handoff functionality
- hotkeys: Hotkey helpers and workflow convenience functions
- checklist: Checklist generation and workflow validation
- git_operations: Safe git operations and timestamp utilities
- memory_manager: Cross-branch memory commits and branch management
- agent_handoffs: Agent coordination and handoff utilities
- dev_testing: Testing utilities and environment detection

Provides a clean API interface while keeping individual modules under 500 LOC.
"""

from pathlib import Path
from typing import Dict, List, Optional

from agor.tools.agent_handoffs import detick_content, retick_content
from agor.tools.checklist import (
    check_git_workflow_status,
    generate_development_checklist,
    generate_git_workflow_report,
    generate_handoff_checklist,
    generate_progress_report,
    validate_workflow_completion,
)
from agor.tools.dev_testing import detect_environment, test_tooling

# Use absolute imports to prevent E0402 errors
from agor.tools.git_operations import (
    get_current_timestamp,
    quick_commit_push,
    run_git_command,
)
from agor.tools.hotkeys import (
    display_project_status,
    display_workspace_health,
    emergency_commit,
    get_project_status,
    quick_status_check,
    workspace_health_check,
)
from agor.tools.memory_manager import auto_commit_memory

# Import from new modular components
from agor.tools.snapshots import (
    create_seamless_handoff,
    create_snapshot,
    generate_agent_handoff_prompt,
    generate_mandatory_session_end_prompt,
)

# Handle imports for both installed and development environments
try:
    from agor.git_binary import git_manager
except ImportError:
    # Development environment - fallback to basic git
    print("⚠️  Using fallback git binary (development mode)")

    class FallbackGitManager:
        def get_git_binary(self):
            import shutil

            git_path = shutil.which("git")
            if not git_path:
                raise RuntimeError("Git not found in PATH")
            return git_path

    git_manager = FallbackGitManager()


# Main API Functions - Core Interface
# ===================================


def create_development_snapshot(title: str, context: str) -> bool:
    """Create development snapshot - main API function."""
    return create_snapshot(title, context)


def generate_seamless_agent_handoff(
    task_description: str,
    work_completed: list = None,
    next_steps: list = None,
    files_modified: list = None,
    context_notes: str = None,
    brief_context: str = None,
) -> tuple[str, str]:
    """Generate seamless agent handoff - main API function."""
    return create_seamless_handoff(
        task_description=task_description,
        work_completed=work_completed,
        next_steps=next_steps,
        files_modified=files_modified,
        context_notes=context_notes,
        brief_context=brief_context,
    )


def generate_session_end_prompt(
    task_description: str = "Session completion",
    brief_context: str = "Work session completed",
) -> str:
    """Generate mandatory session end prompt - main API function."""
    return generate_mandatory_session_end_prompt(task_description, brief_context)


def generate_project_handoff_prompt(
    task_description: str,
    snapshot_content: str = None,
    memory_branch: str = None,
    environment: dict = None,
    brief_context: str = None,
) -> str:
    """Generate project handoff prompt - main API function."""
    return generate_agent_handoff_prompt(
        task_description=task_description,
        snapshot_content=snapshot_content,
        memory_branch=memory_branch,
        environment=environment,
        brief_context=brief_context,
    )


# Convenience Functions - Wrapper API
# ===================================


def quick_commit_and_push(message: str, emoji: str = "🔧") -> bool:
    """Quick commit and push wrapper."""
    return quick_commit_push(message, emoji)


def commit_memory_to_branch(
    content: str, memory_type: str, agent_id: str = "dev"
) -> bool:
    """Auto-commit memory wrapper."""
    return auto_commit_memory(content, memory_type, agent_id)


def test_development_tooling() -> bool:
    """Test development tooling wrapper."""
    return test_tooling()


def get_current_timestamp_formatted() -> str:
    """Get formatted timestamp wrapper."""
    return get_current_timestamp()


def process_content_for_codeblock(content: str) -> str:
    """Process content for safe codeblock embedding."""
    return detick_content(content)


def restore_content_from_codeblock(content: str) -> str:
    """Restore content from codeblock processing."""
    return retick_content(content)


# Status and Health Check Functions
# =================================


def get_workspace_status() -> dict:
    """Get comprehensive workspace status."""
    return get_project_status()


def display_workspace_status() -> str:
    """Display formatted workspace status."""
    return display_project_status()


def get_quick_status() -> str:
    """Get quick status summary."""
    return quick_status_check()


def perform_workspace_health_check() -> dict:
    """Perform comprehensive workspace health check."""
    return workspace_health_check()


def display_health_check_results() -> str:
    """Display formatted health check results."""
    return display_workspace_health()


def emergency_save(message: str = "Emergency commit - work in progress") -> bool:
    """Emergency commit for quick saves."""
    return emergency_commit(message)


# Checklist and Workflow Functions
# ================================


def create_development_checklist(task_type: str = "general") -> str:
    """Create development checklist for task type."""
    return generate_development_checklist(task_type)


def create_handoff_checklist() -> str:
    """Create agent handoff checklist."""
    return generate_handoff_checklist()


def validate_workflow(checklist_items: List[str]) -> Dict[str, any]:
    """Validate workflow completion against checklist."""
    return validate_workflow_completion(checklist_items)


def create_progress_report(validation_results: Dict[str, any]) -> str:
    """Create formatted progress report."""
    return generate_progress_report(validation_results)


def check_git_workflow() -> Dict[str, any]:
    """Check git workflow status."""
    return check_git_workflow_status()


def display_git_workflow_status() -> str:
    """Display git workflow status report."""
    return generate_git_workflow_report()


# Memory Management Functions
# ===========================


def list_memory_branches(repo_path: Optional[Path] = None) -> List[str]:
    """
    List all memory branches without switching branches.

    Args:
        repo_path: Optional repository path (defaults to current directory)

    Returns:
        List of memory branch names
    """
    if repo_path is None:
        repo_path = Path.cwd()

    try:
        from agor.memory_sync import MemorySync

        # Create MemorySync instance with current repo path
        memory_sync = MemorySync(repo_path=str(repo_path))

        # Get both local and remote memory branches
        local_branches = memory_sync.list_memory_branches(remote=False)
        remote_branches = memory_sync.list_memory_branches(remote=True)

        # Combine and deduplicate
        all_branches = list(set(local_branches + remote_branches))
        return sorted(all_branches)

    except Exception as e:
        print(f"❌ Failed to list memory branches: {e}")
        # Fallback to simple implementation if memory_sync fails
        try:
            success, branches_output = run_git_command(["branch", "-a"])
            if not success:
                return []

            memory_branches = []
            for line in branches_output.split("\n"):
                line = line.strip()
                if line.startswith("*"):
                    line = line[1:].strip()
                if line.startswith("remotes/origin/"):
                    line = line.replace("remotes/origin/", "")

                if line.startswith("agor/mem/"):
                    memory_branches.append(line)

            return memory_branches
        except Exception:
            return []


def read_from_memory_branch(
    file_path: str, branch_name: str, repo_path: Optional[Path] = None
) -> Optional[str]:
    """
    SAFE memory branch read - NEVER switches branches.

    Reads file content from memory branch without changing current working branch.

    Args:
        file_path: Path to file to read (relative to repo root)
        branch_name: Source memory branch
        repo_path: Optional repository path (defaults to current directory)

    Returns:
        File content as string if successful, None otherwise
    """
    if repo_path is None:
        repo_path = Path.cwd()

    try:
        success, current_branch = run_git_command(["branch", "--show-current"])
        if not success:
            print(
                "⚠️  Cannot determine current branch - aborting memory read for safety"
            )
            return None

        original_branch = current_branch.strip()

        # Check if memory branch exists
        success, _ = run_git_command(
            ["rev-parse", "--verify", f"refs/heads/{branch_name}"]
        )
        if not success:
            print(f"⚠️  Memory branch {branch_name} does not exist")
            return None

        # Read file from memory branch using git show
        success, content = run_git_command(["show", f"{branch_name}:{file_path}"])
        if not success:
            print(f"⚠️  File {file_path} not found in memory branch {branch_name}")
            return None

        # Verify we're still on the original branch
        success, check_branch = run_git_command(["branch", "--show-current"])
        if success and check_branch.strip() != original_branch:
            print(
                f"🚨 SAFETY VIOLATION: Branch changed from {original_branch} to {check_branch.strip()}"
            )
            return None

        print(f"✅ Successfully read {file_path} from memory branch {branch_name}")
        return content

    except Exception as e:
        print(f"❌ Memory branch read failed: {e}")
        return None


# Utility Functions
# =================


def detect_current_environment() -> dict:
    """Detect current development environment."""
    return detect_environment()


def test_all_tooling() -> bool:
    """Test all development tooling components."""
    return test_tooling()
