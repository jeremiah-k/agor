"""
AGOR Hotkey and Workflow Helper Module

This module provides hotkey helpers and workflow convenience functions for AGOR.
Includes quick action wrappers, status helpers, and coordination utilities.

All functions use absolute imports for better reliability.
"""

from pathlib import Path

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
    """Test all development tools functions."""
    return test_tooling()


def get_timestamp() -> str:
    """Get current UTC timestamp."""
    return get_current_timestamp()


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
    Returns a formatted markdown summary of the current workspace health.

    The summary includes overall status, timestamp, environment details, issues, warnings, and a message if all systems are operational.
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


def generate_meta_feedback_hotkey(
    feedback_type: str = "workflow_issue",
    feedback_content: str = "",
    severity: str = "medium",
    component: str = "general",
) -> str:
    """
    Generates formatted meta feedback about AGOR for quick submission.

    If no feedback content is provided, a default prompt is used. Returns an error message if feedback generation fails.
    """
    try:
        from agor.tools.agent_handoffs import generate_meta_feedback

        if not feedback_content:
            feedback_content = "Please provide specific feedback about AGOR functionality, workflow, or user experience."

        return generate_meta_feedback(
            feedback_type=feedback_type,
            feedback_content=feedback_content,
            severity=severity,
            component=component,
        )
    except Exception as e:
        return f"❌ Failed to generate meta feedback: {e}"


def system_health_check_hotkey() -> str:
    """
    Performs a comprehensive system health check and returns a detailed markdown report.

    The report summarizes workspace health, project status, development tools, memory system availability, issues, warnings, and provides recommendations for maintaining optimal AGOR performance. Returns an error message if the health check fails.
    """
    try:
        # Get workspace health
        workspace_health = workspace_health_check()

        # Get project status
        project_status = get_project_status()

        # Check dev tools
        tooling_status = "✅ Available"
        try:
            test_result = test_tooling()
            if not test_result:
                tooling_status = "⚠️ Some issues detected"
        except Exception:
            tooling_status = "❌ Failed to test"

        # Check memory system
        memory_status = "✅ Available"
        try:
            from agor.tools.memory_manager import list_memory_branches

            branches = list_memory_branches()
            memory_status = f"✅ Available ({len(branches)} memory branches)"
        except Exception:
            memory_status = "❌ Failed to access"

        # Generate comprehensive report
        health_report = f"""# 🏥 AGOR System Health Check

**Timestamp**: {get_current_timestamp()}
**Overall Status**: {workspace_health['overall_status'].title()}

## 📊 Component Status

### Git & Workspace
- **Current Branch**: {project_status.get('current_branch', 'unknown')}
- **Current Commit**: {project_status.get('current_commit', 'unknown')}
- **Uncommitted Changes**: {'Yes' if project_status.get('has_changes', False) else 'No'}
- **Branch Safety**: {'✅ Safe' if workspace_health.get('branch_safe', True) else '⚠️ Potentially unsafe'}

### Environment
- **Mode**: {project_status.get('mode', 'unknown')}
- **Platform**: {project_status.get('platform', 'unknown')}
- **AGOR Version**: {project_status.get('agor_version', 'unknown')}

### Development Tools
- **Dev Tools**: {tooling_status}
- **Memory System**: {memory_status}
- **Environment Detection**: {'✅ Working' if 'environment_error' not in project_status else '❌ Failed'}

## 🚨 Issues & Warnings

"""

        if workspace_health.get("issues"):
            health_report += "### Issues\n"
            for issue in workspace_health["issues"]:
                health_report += f"- ❌ {issue}\n"
            health_report += "\n"

        if workspace_health.get("warnings"):
            health_report += "### Warnings\n"
            for warning in workspace_health["warnings"]:
                health_report += f"- ⚠️ {warning}\n"
            health_report += "\n"

        if not workspace_health.get("issues") and not workspace_health.get("warnings"):
            health_report += "✅ No issues or warnings detected\n\n"

        health_report += """## 💡 Recommendations

Based on the health check:

1. **Regular Commits**: Commit work frequently to prevent data loss
2. **Branch Management**: Use feature branches for development work
3. **Memory Sync**: Ensure memory branches are accessible for coordination
4. **Environment Monitoring**: Keep development environment stable
5. **Tool Maintenance**: Test dev tools regularly for reliability

---

**System health checks help maintain optimal AGOR performance.**
"""

        return health_report

    except Exception as e:
        return f"❌ System health check failed: {e}"


def quick_meta_feedback_bug(bug_description: str, component: str = "general") -> str:
    """
    Generates a formatted bug report meta feedback entry with medium severity.

    Args:
        bug_description: Description of the bug to report.
        component: The component where the bug was found.

    Returns:
        A formatted string representing the bug report feedback.
    """
    return generate_meta_feedback_hotkey(
        feedback_type="bug",
        feedback_content=bug_description,
        severity="medium",
        component=component,
    )


def quick_meta_feedback_enhancement(
    enhancement_idea: str, component: str = "general"
) -> str:
    """
    Submits a quick enhancement suggestion as meta feedback.

    Args:
        enhancement_idea: Description of the proposed enhancement.
        component: The component or area related to the enhancement.

    Returns:
        A formatted string containing the enhancement suggestion feedback.
    """
    return generate_meta_feedback_hotkey(
        feedback_type="enhancement",
        feedback_content=enhancement_idea,
        severity="medium",
        component=component,
    )


def quick_meta_feedback_success(success_story: str, component: str = "general") -> str:
    """
    Generates a formatted success story meta feedback report for AGOR.

    Args:
        success_story: Description of the successful workflow or outcome.
        component: The component associated with the success story.

    Returns:
        A formatted string containing the success story feedback.
    """
    return generate_meta_feedback_hotkey(
        feedback_type="success_story",
        feedback_content=success_story,
        severity="low",
        component=component,
    )
