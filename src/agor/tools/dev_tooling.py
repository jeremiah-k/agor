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


# Import memory branch utilities from memory_manager to avoid code duplication
from agor.tools.memory_manager import read_from_memory_branch, list_memory_branches


# Utility Functions
# =================


def detect_current_environment() -> dict:
    """Detect current development environment."""
    return detect_environment()


def test_all_tooling() -> bool:
    """Test all development tooling components."""
    return test_tooling()
