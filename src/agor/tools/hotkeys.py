"""
AGOR Hotkey and Workflow Helper Module

This module provides hotkey helpers and workflow convenience functions for AGOR.
Includes quick action wrappers, status helpers, and coordination utilities.

All functions use absolute imports for better reliability.
"""

from pathlib import Path

from agor.tools.agent_handoffs import detick_content, retick_content
from agor.tools.dev_testing import detect_environment, test_tooling

# Use absolute imports to prevent E0402 errors
from agor.tools.git_operations import (
    get_current_timestamp,
    quick_commit_push,
    run_git_command,
)
from agor.tools.memory_manager import auto_commit_memory


def quick_commit_push_wrapper(message: str, emoji: str = "🔧") -> bool:
    """Quick commit and push with timestamp."""
    return quick_commit_push(message, emoji)


def auto_commit_memory_wrapper(
    content: str, memory_type: str, agent_id: str = "dev"
) -> bool:
    """Auto-commit memory to memory branch."""
    return auto_commit_memory(content, memory_type, agent_id)


def test_tooling_wrapper() -> bool:
    """Test all development tooling functions."""
    return test_tooling()


def get_timestamp() -> str:
    """Get current UTC timestamp."""
    return get_current_timestamp()


def detick_content_wrapper(content: str) -> str:
    """
    Replaces all triple backticks in the content with double backticks for safe embedding within a single codeblock.
    """
    return detick_content(content)


def retick_content_wrapper(content: str) -> str:
    """
    Converts double backticks (``) in the content back to triple backticks (```) for standard codeblock formatting.

    Args:
        content: The string content with double backticks to be converted.

    Returns:
        The content with double backticks replaced by triple backticks.
    """
    return retick_content(content)


def get_project_status() -> dict:
    """
    Get comprehensive project status information.

    Returns:
        Dictionary containing project status details.
    """
    status = {}

    # Get current branch
    success_branch, current_branch_val = run_git_command(["branch", "--show-current"])
    status["current_branch"] = (
        current_branch_val.strip() if success_branch else "unknown"
    )

    # Get current commit
    success_commit, current_commit_val = run_git_command(
        ["rev-parse", "--short", "HEAD"]
    )
    status["current_commit"] = (
        current_commit_val.strip() if success_commit else "unknown"
    )

    # Get git status
    success_status, git_status_val = run_git_command(["status", "--porcelain"])
    status["has_changes"] = bool(git_status_val.strip()) if success_status else False
    status["git_status"] = git_status_val.strip() if success_status else ""

    # Get environment info
    try:
        env_info = detect_environment()
        status.update(env_info)
    except Exception as e:
        status["environment_error"] = str(e)

    # Get timestamp
    status["timestamp"] = get_current_timestamp()

    return status


def display_project_status() -> str:
    """
    Display formatted project status information.

    Returns:
        Formatted status string ready for display.
    """
    status = get_project_status()

    status_display = f"""# 📊 Project Status

**Timestamp**: {status.get('timestamp', 'unknown')}
**Branch**: {status.get('current_branch', 'unknown')}
**Commit**: {status.get('current_commit', 'unknown')}
**Environment**: {status.get('mode', 'unknown')} ({status.get('platform', 'unknown')})
**AGOR Version**: {status.get('agor_version', 'unknown')}

## Git Status
"""

    if status.get("has_changes", False):
        status_display += f"""**Changes Detected**: Yes
```
{status.get('git_status', 'No details available')}
```
"""
    else:
        status_display += "**Changes Detected**: No uncommitted changes\n"

    if "environment_error" in status:
        status_display += (
            f"\n**Environment Error**: {status.get('environment_error', 'unknown')}\n"
        )

    return status_display


def quick_status_check() -> str:
    """
    Quick status check for hotkey use.

    Returns:
        Brief status summary.
    """
    status = get_project_status()

    return f"Branch: {status.get('current_branch', 'unknown')} | Commit: {status.get('current_commit', 'unknown')} | Changes: {'Yes' if status.get('has_changes', False) else 'No'}"


def emergency_commit(message: str = "Emergency commit - work in progress") -> bool:
    """
    Emergency commit function for quick saves.

    Args:
        message: Commit message (defaults to emergency message).

    Returns:
        True if commit successful, False otherwise.
    """
    return quick_commit_push(message, "🚨")


def safe_branch_check() -> tuple[bool, str]:
    """
    Check if current branch is safe for operations.

    Returns:
        Tuple of (is_safe, branch_name).
    """
    success, current_branch_val = run_git_command(["branch", "--show-current"])
    if not success:
        return False, "unknown"

    current_branch = current_branch_val.strip()

    # Consider main/master branches as potentially unsafe for direct work
    unsafe_branches = ["main", "master", "production", "prod"]
    is_safe = current_branch not in unsafe_branches

    return is_safe, current_branch


def workspace_health_check() -> dict:
    """
    Comprehensive workspace health check.

    Returns:
        Dictionary with health check results.
    """
    health = {
        "timestamp": get_current_timestamp(),
        "overall_status": "healthy",
        "issues": [],
        "warnings": [],
    }

    # Check git status
    is_safe, branch = safe_branch_check()
    if not is_safe:
        health["warnings"].append(f"Working on potentially unsafe branch: {branch}")

    # Check for uncommitted changes
    status = get_project_status()
    if status.get("has_changes", False):
        health["warnings"].append("Uncommitted changes detected")

    # Check environment
    try:
        env_info = detect_environment()
        health["environment"] = env_info
    except Exception as e:
        health["issues"].append(f"Environment detection failed: {e}")
        health["overall_status"] = "degraded"

    # Check AGOR directory structure
    agor_dir = Path.cwd() / ".agor"
    if not agor_dir.exists():
        health["warnings"].append("No .agor directory found - may need initialization")

    # Set overall status based on issues
    if health["issues"]:
        health["overall_status"] = "unhealthy"
    elif health["warnings"]:
        health["overall_status"] = "warning"

    return health


def display_workspace_health() -> str:
    """
    Display formatted workspace health check.

    Returns:
        Formatted health check string.
    """
    health = workspace_health_check()

    status_emoji = {
        "healthy": "✅",
        "warning": "⚠️",
        "degraded": "🔶",
        "unhealthy": "❌",
    }

    display = f"""# {status_emoji.get(health['overall_status'], '❓')} Workspace Health Check

**Status**: {health['overall_status'].title()}
**Timestamp**: {health['timestamp']}
"""

    if health.get("environment"):
        env = health["environment"]
        display += f"**Environment**: {env.get('mode', 'unknown')} ({env.get('platform', 'unknown')})\n"

    if health["issues"]:
        display += "\n## 🚨 Issues\n"
        for issue in health["issues"]:
            display += f"- {issue}\n"

    if health["warnings"]:
        display += "\n## ⚠️ Warnings\n"
        for warning in health["warnings"]:
            display += f"- {warning}\n"

    if health["overall_status"] == "healthy" and not health["warnings"]:
        display += "\n## 🎉 All Systems Operational\nWorkspace is healthy and ready for development.\n"

    return display
