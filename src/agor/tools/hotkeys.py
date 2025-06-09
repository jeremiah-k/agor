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
    """
    Performs a quick git commit and push with a timestamped message and optional emoji.
    
    Args:
        message: The commit message to use.
        emoji: An optional emoji to prepend to the commit message. Defaults to "🔧".
    
    Returns:
        True if the commit and push were successful, False otherwise.
    """
    return quick_commit_push(message, emoji)


def auto_commit_memory_wrapper(
    content: str, memory_type: str, agent_id: str = "dev"
) -> bool:
    """
    Commits the provided memory content to a designated memory branch.
    
    Args:
        content: The memory content to commit.
        memory_type: The type or category of memory being committed.
        agent_id: Identifier for the agent associated with the memory (default is "dev").
    
    Returns:
        True if the commit was successful, False otherwise.
    """
    return auto_commit_memory(content, memory_type, agent_id)


def test_tooling_wrapper() -> bool:
    """
    Runs all development tooling tests and returns whether they succeeded.
    
    Returns:
        True if all tooling tests pass, False otherwise.
    """
    return test_tooling()


def get_timestamp() -> str:
    """
    Returns the current UTC timestamp as a string.
    """
    return get_current_timestamp()


def detick_content_wrapper(content: str) -> str:
    """
    Replaces all triple backticks in the input content with double backticks.
    
    This allows the content to be safely embedded within a single code block without breaking formatting.
    
    Args:
        content: The string containing code or text to be processed.
    
    Returns:
        The content with all triple backticks replaced by double backticks.
    """
    return detick_content(content)


def retick_content_wrapper(content: str) -> str:
    """
    Converts double backticks in the input content to triple backticks for standard code block formatting.
    
    Args:
        content: Text containing double backticks to be converted.
    
    Returns:
        The content with all double backticks replaced by triple backticks.
    """
    return retick_content(content)


def get_project_status() -> dict:
    """
    Gathers and returns detailed project status information including git branch, commit, uncommitted changes, environment details, and a timestamp.
    
    Returns:
        A dictionary with keys for current branch, commit hash, change status, git status output, environment information, any environment detection errors, and the current timestamp.
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
    Formats and returns a markdown string displaying the current project status.
    
    The output includes timestamp, git branch, commit hash, environment mode and platform, AGOR version, git status (including uncommitted changes if present), and any environment detection errors.
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
    Returns a concise one-line summary of the current git branch, commit hash, and whether there are uncommitted changes.
    
    Intended for quick display via hotkeys.
    """
    status = get_project_status()

    return f"Branch: {status.get('current_branch', 'unknown')} | Commit: {status.get('current_commit', 'unknown')} | Changes: {'Yes' if status.get('has_changes', False) else 'No'}"


def emergency_commit(message: str = "Emergency commit - work in progress") -> bool:
    """
    Performs an emergency git commit and push with a default or provided message and an alert emoji.
    
    Args:
        message: The commit message to use. Defaults to "Emergency commit - work in progress".
    
    Returns:
        True if the commit and push were successful, False otherwise.
    """
    return quick_commit_push(message, "🚨")


def safe_branch_check() -> tuple[bool, str]:
    """
    Determines whether the current git branch is safe for operations.
    
    A branch is considered unsafe if its name is one of: "main", "master", "production", or "prod".
    
    Returns:
        A tuple containing a boolean indicating branch safety and the current branch name.
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
    Performs a comprehensive health check of the workspace and returns a summary.
    
    The health check evaluates git branch safety, uncommitted changes, environment detection, and the presence of the `.agor` directory. The result includes a timestamp, overall status, lists of issues and warnings, and environment information if available.
    
    Returns:
        A dictionary containing the health check results, including status, issues, warnings, and environment details.
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
    Formats and returns a markdown summary of the current workspace health.
    
    The output includes overall status with an emoji, timestamp, environment details, lists of issues and warnings if present, and a message indicating all systems are operational when appropriate.
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
