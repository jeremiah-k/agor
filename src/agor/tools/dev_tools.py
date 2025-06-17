"""
AGOR Development Tools - Main Interface Module

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

from typing import Dict, List, Tuple

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
    get_file_timestamp,
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
from agor.utils import sanitize_slug

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


def create_development_snapshot(
    title: str, context: str, agent_id: str = None, custom_branch: str = None
) -> bool:
    """Create development snapshot in agent's directory within main memory branch."""
    return create_snapshot(title, context, agent_id, custom_branch)


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


def test_development_tools() -> bool:
    """
    Test development tools wrapper.

    DEPRECATED: Use test_all_tools() instead.
    This function will be removed in a future version.
    """
    import warnings

    warnings.warn(
        "test_development_tools() is deprecated. Use test_all_tools() instead.",
        DeprecationWarning,
        stacklevel=2,
    )
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


def _parse_git_branches(branches_output: str) -> Tuple[List[str], List[str]]:
    """Parse git branch output to extract local and remote memory branches."""
    local_memory_branches = []
    remote_memory_branches = []

    for line in branches_output.split("\n"):
        line = line.strip()
        # Skip empty lines
        if not line:
            continue

        # Handle current branch marker
        if line.startswith("*"):
            line = line[1:].strip()

        # Process remote branches
        if line.startswith("remotes/origin/agor/mem/"):
            remote_branch = line[len("remotes/origin/") :]
            remote_memory_branches.append(remote_branch)
        # Process local branches
        elif line.startswith("agor/mem/"):
            local_memory_branches.append(line)

    return local_memory_branches, remote_memory_branches


def _delete_local_branches(branches: List[str], results: Dict) -> None:
    """Delete local memory branches and update results."""
    print(f"\n🗑️  Deleting {len(branches)} local memory branches...")
    for branch in branches:
        success, output = run_git_command(["branch", "-D", branch])
        if success:
            print(f"✅ Deleted local branch: {branch}")
            results["deleted_local"].append(branch)
        else:
            print(f"❌ Failed to delete local branch {branch}: {output}")
            results["failed"].append(f"local:{branch}")


def _delete_remote_branches(branches: List[str], results: Dict) -> None:
    """Delete remote memory branches and update results."""
    print(f"\n🌐 Deleting {len(branches)} remote memory branches...")
    for branch in branches:
        success, output = run_git_command(["push", "origin", "--delete", branch])
        if success:
            print(f"✅ Deleted remote branch: {branch}")
            results["deleted_remote"].append(branch)
        else:
            # Check for common network/permission issues
            if "Permission denied" in output or "Authentication failed" in output:
                print(f"🔒 Permission denied for remote branch {branch}: {output}")
                results["failed"].append(f"remote:{branch}:permission_denied")
            elif "Network" in output or "Connection" in output:
                print(f"🌐 Network error deleting remote branch {branch}: {output}")
                results["failed"].append(f"remote:{branch}:network_error")
            else:
                print(f"❌ Failed to delete remote branch {branch}: {output}")
                results["failed"].append(f"remote:{branch}:unknown_error")


def cleanup_memory_branches(
    dry_run: bool = True, confirm: bool = True
) -> Dict[str, List[str]]:
    """
    Safely cleanup all memory branches (local and remote).

    SAFETY: Only removes branches matching 'agor/mem/' pattern.

    Args:
        dry_run: If True, only shows what would be deleted without actually deleting
        confirm: If True, requires user confirmation before deletion

    Returns:
        Dictionary with 'deleted_local', 'deleted_remote', 'failed' lists
    """

    results = {"deleted_local": [], "deleted_remote": [], "failed": [], "skipped": []}

    print("🔍 Scanning for memory branches...")

    # Get all branches (local and remote)
    success, branches_output = run_git_command(["branch", "-a"])
    if not success:
        print("❌ Failed to list branches")
        return results

    local_memory_branches, remote_memory_branches = _parse_git_branches(branches_output)

    total_branches = len(local_memory_branches) + len(remote_memory_branches)

    if total_branches == 0:
        print("✅ No memory branches found to cleanup")
        return results

    print(
        f"📋 Found {len(local_memory_branches)} local and {len(remote_memory_branches)} remote memory branches"
    )

    if dry_run:
        print("\n🔍 DRY RUN - Would delete:")
        for branch in local_memory_branches:
            print(f"  📍 Local: {branch}")
        for branch in remote_memory_branches:
            print(f"  🌐 Remote: {branch}")
        print(
            f"\n💡 Run with dry_run=False to actually delete {total_branches} branches"
        )
        return results

    if confirm:
        print(f"\n⚠️  About to delete {total_branches} memory branches:")
        for branch in local_memory_branches:
            print(f"  📍 Local: {branch}")
        for branch in remote_memory_branches:
            print(f"  🌐 Remote: {branch}")

        response = input("\n❓ Continue with deletion? (yes/no): ").lower().strip()
        if response not in ["yes", "y"]:
            print("🚫 Cleanup cancelled by user")
            results["skipped"] = local_memory_branches + remote_memory_branches
            return results

    # Delete branches using helper functions
    _delete_local_branches(local_memory_branches, results)
    _delete_remote_branches(remote_memory_branches, results)

    # Summary
    total_deleted = len(results["deleted_local"]) + len(results["deleted_remote"])
    total_failed = len(results["failed"])

    print("\n📊 Cleanup Summary:")
    print(f"✅ Successfully deleted: {total_deleted} branches")
    print(f"❌ Failed to delete: {total_failed} branches")

    if total_failed == 0:
        print("🎉 All memory branches cleaned up successfully!")

    return results


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


# Security and Utility Functions
# ==============================


# sanitize_slug function now imported from agor.utils


def get_or_create_agent_id_file(agent_id: str = None) -> str:
    """
    Get or create agent ID from /tmp/agor/agent_id file for persistence across sessions.

    Note: This approach has limitations and should not be relied upon heavily.
    - Does not work reliably with Augment local agents
    - May not work on certain platforms
    - Users should monitor and modify as needed

    Args:
        agent_id: Optional agent ID to store. If not provided, reads from file or generates new one.

    Returns:
        Agent ID string
    """
    import tempfile
    from pathlib import Path

    # Use /tmp/agor/ directory for agent ID persistence
    tmp_agor_dir = Path(tempfile.gettempdir()) / "agor"
    agent_id_file = tmp_agor_dir / "agent_id"

    try:
        # Create directory if it doesn't exist
        tmp_agor_dir.mkdir(exist_ok=True)

        # If agent_id provided, store it
        if agent_id:
            sanitized_id = sanitize_slug(agent_id)
            agent_id_file.write_text(sanitized_id)
            return sanitized_id

        # Try to read existing agent ID
        if agent_id_file.exists():
            stored_id = agent_id_file.read_text().strip()
            if stored_id and len(stored_id) > 0:
                return sanitize_slug(stored_id)

        # Generate new agent ID if none exists
        new_agent_id = generate_unique_agent_id()
        sanitized_id = sanitize_slug(new_agent_id)
        agent_id_file.write_text(sanitized_id)

        print(f"📝 Created new agent ID file: {agent_id_file}")
        print(f"🆔 Agent ID: {sanitized_id}")
        print(
            "⚠️  Note: Agent identification has limitations and should not be relied upon heavily"
        )

        return sanitized_id

    except Exception as e:
        print(f"⚠️  Could not manage agent ID file: {e}")
        # Fallback to generating new ID
        return sanitize_slug(generate_unique_agent_id())


# Memory Management Functions
# ===========================


# Import memory branch utilities from memory_manager to avoid code duplication
# Note: read_from_memory_branch and list_memory_branches available if needed


def generate_unique_agent_id() -> str:
    """
    Generate a truly unique agent identifier for each agent session.

    Format: agent_{hash}_{timestamp} for uniqueness and readability.
    Each agent session gets its own directory in the main memory branch.

    Returns:
        A string agent ID in format 'agent_{hash}_{timestamp}' for unique identification.
    """
    import hashlib
    import os
    import time
    import uuid

    # Create truly unique identifier using multiple sources
    full_timestamp = str(
        int(time.time())
    )  # full epoch seconds for proper datetime conversion
    random_component = str(uuid.uuid4())[:8]  # random component
    process_id = str(os.getpid())  # process ID

    # Combine for uniqueness
    unique_string = f"{random_component}_{process_id}_{time.time()}"
    agent_hash = hashlib.md5(unique_string.encode()).hexdigest()[:8]

    # Format: agent_{hash}_{timestamp} with full timestamp for datetime compatibility
    agent_id = f"agent_{agent_hash}_{full_timestamp}"

    # Sanitize the agent ID before returning to ensure it's safe for use
    return sanitize_slug(agent_id)


def generate_agent_id() -> str:
    """
    Generate a unique agent ID for this agent session.

    Each agent session gets a unique ID - this is the correct behavior.
    """
    return generate_unique_agent_id()


def get_main_memory_branch(custom_branch: str = None) -> str:
    """
    Get the main memory branch name, with optional custom branch support.

    Args:
        custom_branch: Optional custom memory branch name. If not provided, uses 'agor/mem/main'.

    Returns:
        A string memory branch name (e.g., 'agor/mem/main' or custom branch).
    """
    if custom_branch:
        return custom_branch
    return "agor/mem/main"


def get_agent_directory_path(agent_id: str) -> str:
    """
    Get the agent's directory path within the .agor directory on memory branches.

    Args:
        agent_id: Agent identifier

    Returns:
        A string path like '.agor/agents/agent_{hash}_{timestamp}/' for the agent's directory.
    """
    return f".agor/agents/{agent_id}/"


def initialize_agent_workspace(
    agent_id: str = None, custom_branch: str = None
) -> tuple[bool, str, str]:
    """
    Initialize agent workspace in the main memory branch with directory structure.

    Args:
        agent_id: Optional agent ID. If not provided, generates a new one.
        custom_branch: Optional custom memory branch. Defaults to 'agor/mem/main'.

    Returns:
        A tuple containing (success, agent_id, memory_branch) for tracking agent identity.
    """
    if agent_id is None:
        agent_id = generate_agent_id()

    memory_branch = get_main_memory_branch(custom_branch)
    agent_dir = get_agent_directory_path(agent_id)

    try:
        from agor.tools.memory_manager import commit_to_memory_branch

        # Create agent initialization file
        agent_init_content = f"""# Agent Workspace: {agent_id}

**Agent ID**: {agent_id}
**Created**: {get_current_timestamp()}
**Memory Branch**: {memory_branch}
**Agent Directory**: {agent_dir}

## Agent Workspace Structure

This agent's workspace contains:
- `snapshots/` - Development snapshots and work progress
- `work_log.md` - Session work log and notes
- `agent_info.md` - Agent metadata and session information

## Coordination

- **Main Memory Branch**: {memory_branch}
- **Agent Directory**: {agent_dir}
- **Shared Coordination**: .agor/agentconvo.md
- **Project Memory**: .agor/memory.md

## Session Guidelines

- All work snapshots go in this agent's directory
- Reference other agents via their directories
- Use shared coordination files for cross-agent communication
- Create handoffs in `handoffs/pending/` for agent transitions
"""

        # Create shared coordination structure if it doesn't exist
        shared_agentconvo_content = f"""# Agent Conversation Log

**Memory Branch**: {memory_branch}
**Last Updated**: {get_current_timestamp()}

## Active Agents

- **{agent_id}**: Initialized at {get_current_timestamp()}

## Coordination Notes

Use this file for cross-agent communication and coordination.

## Memory Branch Structure

```
{memory_branch}/.agor/
├── agents/
│   ├── {agent_id}/
│   │   ├── snapshots/
│   │   ├── work_log.md
│   │   └── agent_info.md
├── agentconvo.md (shared communication)
├── memory.md (project memory)
└── strategy-active.md (current strategy)
```
"""

        # Commit agent initialization
        agent_success = commit_to_memory_branch(
            file_content=agent_init_content,
            file_name=f"{agent_dir}agent_info.md",
            branch_name=memory_branch,
            commit_message=f"Initialize agent workspace for {agent_id}",
        )

        # Commit shared coordination structure
        shared_success = commit_to_memory_branch(
            file_content=shared_agentconvo_content,
            file_name=".agor/agentconvo.md",
            branch_name=memory_branch,
            commit_message=f"Update shared coordination for agent {agent_id}",
        )

        if agent_success and shared_success:
            print(f"✅ Initialized agent workspace: {memory_branch}/{agent_dir}")
            print(f"🆔 Agent ID: {agent_id}")
            print(f"📁 Agent Directory: {agent_dir}")
        else:
            print("❌ Failed to initialize agent workspace")

        return agent_success and shared_success, agent_id, memory_branch

    except Exception as e:
        print(f"❌ Error initializing agent workspace: {e}")
        return False, agent_id, memory_branch


def cleanup_agent_directories(
    keep_current: bool = True,
    days_old: int = None,
    agent_pattern: str = None,
    custom_branch: str = None,
    current_agent_id: str = None,
) -> bool:
    """
    Intelligently clean up agent directories in the main memory branch.

    Args:
        keep_current: If True, keeps the current agent's directory
        days_old: Only remove directories older than this many days
        agent_pattern: Only remove agents matching this pattern (e.g., "agent_abc*")
        custom_branch: Custom memory branch to clean up
        current_agent_id: Explicit current agent ID (if not provided, reads from file)

    Returns:
        True if cleanup was successful, False otherwise
    """
    try:
        import os
        import subprocess
        from datetime import datetime, timedelta

        memory_branch = get_main_memory_branch(custom_branch)

        # Get current agent ID safely
        if keep_current:
            if current_agent_id:
                current_agent_id = sanitize_slug(current_agent_id)
            else:
                # Try to get from persistent file, don't generate new one
                current_agent_id = get_or_create_agent_id_file()

        print(f"🧹 Cleaning up agent directories in {memory_branch}")
        if current_agent_id:
            print(f"🆔 Keeping current agent: {current_agent_id}")

        # SAFETY: Capture current branch before any checkout operations
        original_branch_result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            cwd=".",
        )

        if original_branch_result.returncode != 0:
            print("❌ Could not determine current branch")
            return False

        original_branch = original_branch_result.stdout.strip()
        print(f"🔒 Current branch: {original_branch} (will restore after cleanup)")

        try:
            # Switch to memory branch to examine directories
            checkout_result = subprocess.run(
                ["git", "checkout", memory_branch],
                capture_output=True,
                text=True,
                cwd=".",
            )

            if checkout_result.returncode != 0:
                print(f"❌ Could not checkout memory branch {memory_branch}")
                return False

            # List agent directories
            agents_dir = "agents"
            if not os.path.exists(agents_dir):
                print(f"📁 No agents directory found in {memory_branch}")
                return True

            directories_removed = 0
            removed_directories = (
                []
            )  # Track removed directories for specific git staging

            for agent_dir in os.listdir(agents_dir):
                agent_path = os.path.join(agents_dir, agent_dir)

                # Skip if not a directory
                if not os.path.isdir(agent_path):
                    continue

                # Skip current agent if keeping it
                if keep_current and current_agent_id and agent_dir == current_agent_id:
                    print(f"⏭️  Keeping current agent directory: {agent_dir}")
                    continue

                # Check pattern matching
                if agent_pattern and not agent_dir.startswith(
                    agent_pattern.replace("*", "")
                ):
                    continue

                # Check age if specified
                if days_old:
                    try:
                        # Extract timestamp from agent_id (assuming agent_{hash}_{timestamp} format)
                        timestamp_str = agent_dir.split("_")[-1]
                        agent_timestamp = datetime.fromtimestamp(int(timestamp_str))
                        cutoff_date = datetime.now() - timedelta(days=days_old)

                        if agent_timestamp > cutoff_date:
                            print(f"⏭️  Keeping recent agent directory: {agent_dir}")
                            continue
                    except (ValueError, IndexError):
                        print(f"⚠️  Could not parse timestamp for {agent_dir}, skipping")
                        continue

                # Remove the directory
                import shutil

                try:
                    shutil.rmtree(agent_path)
                    print(f"✅ Removed agent directory: {agent_dir}")
                    directories_removed += 1
                    removed_directories.append(agent_path)  # Track for git staging
                except Exception as e:
                    print(f"❌ Failed to remove {agent_dir}: {e}")

            # Commit the cleanup - only stage specific removed directories
            if directories_removed > 0:
                # Stage only the specific directories that were removed
                for removed_dir in removed_directories:
                    subprocess.run(
                        ["git", "rm", "-r", "--cached", removed_dir],
                        cwd=".",
                    )
                subprocess.run(
                    [
                        "git",
                        "commit",
                        "-m",
                        f"🧹 Cleanup: Removed {directories_removed} agent directories",
                    ],
                    cwd=".",
                )

                # Push the cleanup
                subprocess.run(["git", "push", "origin", memory_branch], cwd=".")

            print(
                f"🧹 Cleanup complete: Removed {directories_removed} agent directories"
            )
            return True

        finally:
            # SAFETY: Always restore original branch regardless of success/failure
            try:
                restore_result = subprocess.run(
                    ["git", "checkout", original_branch],
                    capture_output=True,
                    text=True,
                    cwd=".",
                )
                if restore_result.returncode == 0:
                    print(f"🔒 Restored original branch: {original_branch}")
                else:
                    print(
                        f"⚠️  Failed to restore original branch {original_branch}: {restore_result.stderr}"
                    )
            except Exception as restore_error:
                print(
                    f"🚨 CRITICAL: Failed to restore original branch {original_branch}: {restore_error}"
                )

    except Exception as e:
        print(f"❌ Error during cleanup: {e}")
        return False


def check_pending_handoffs(custom_branch: str = None) -> list:
    """
    Check for pending handoffs in the main memory branch.

    Args:
        custom_branch: Optional custom memory branch

    Returns:
        List of pending handoff files
    """
    try:
        import os
        import subprocess

        memory_branch = get_main_memory_branch(custom_branch)

        # Capture current branch before switching
        original_branch_result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            cwd=".",
        )

        if original_branch_result.returncode != 0:
            print("❌ Could not determine current branch")
            return []

        original_branch = original_branch_result.stdout.strip()

        try:
            # Switch to memory branch to check handoffs
            checkout_result = subprocess.run(
                ["git", "checkout", memory_branch],
                capture_output=True,
                text=True,
                cwd=".",
            )

            if checkout_result.returncode != 0:
                print(f"❌ Could not checkout memory branch {memory_branch}")
                return []

            # Check for pending handoffs
            pending_dir = "handoffs/pending"
            if not os.path.exists(pending_dir):
                print("📁 No pending handoffs directory found")
                return []

            pending_handoffs = []
            for handoff_file in os.listdir(pending_dir):
                if handoff_file.endswith(".md"):
                    pending_handoffs.append(os.path.join(pending_dir, handoff_file))

            if pending_handoffs:
                print(f"📬 Found {len(pending_handoffs)} pending handoffs:")
                for handoff in pending_handoffs:
                    print(f"   - {handoff}")
            else:
                print("📭 No pending handoffs found")

            return pending_handoffs

        finally:
            # Always switch back to original branch
            try:
                restore_result = subprocess.run(
                    ["git", "checkout", original_branch],
                    capture_output=True,
                    text=True,
                    cwd=".",
                )
                if restore_result.returncode != 0:
                    print(
                        f"⚠️  Failed to restore original branch {original_branch}: {restore_result.stderr}"
                    )
            except Exception as restore_error:
                print(
                    f"🚨 CRITICAL: Failed to restore original branch {original_branch}: {restore_error}"
                )

    except Exception as e:
        print(f"❌ Error checking pending handoffs: {e}")
        return []


def create_handoff_prompt(
    agent_id: str,
    title: str,
    work_summary: str,
    next_steps: list,
    custom_branch: str = None,
) -> bool:
    """
    Create a handoff prompt in the pending handoffs directory.

    Args:
        agent_id: Current agent ID
        title: Handoff title
        work_summary: Summary of work completed
        next_steps: List of next steps for receiving agent
        custom_branch: Optional custom memory branch

    Returns:
        True if handoff was created successfully
    """
    try:
        from agor.tools.memory_manager import commit_to_memory_branch

        # Sanitize agent_id to ensure it's safe for use in paths
        agent_id = sanitize_slug(agent_id)

        memory_branch = get_main_memory_branch(custom_branch)
        agent_dir = get_agent_directory_path(agent_id)
        timestamp_str = get_file_timestamp()

        handoff_content = f"""# 🤝 Agent Handoff: {title}

**From Agent**: {agent_id}
**Created**: {get_current_timestamp()}
**Agent Directory**: {agent_dir}
**Memory Branch**: {memory_branch}

## Work Summary

{work_summary}

## Next Steps

{chr(10).join(f"- {step}" for step in next_steps)}

## Agent Context

- **Previous Agent Directory**: `{agent_dir}`
- **Snapshots Location**: `{agent_dir}snapshots/`
- **Work Log**: `{agent_dir}work_log.md`

## Instructions for Next Agent

1. **Initialize your workspace**: Use AGOR dev tools to create your agent directory
2. **Review previous work**: Check `{agent_dir}snapshots/` for context
3. **Update coordination**: Add your progress to `shared/agentconvo.md`
4. **Move this handoff**: When you start work, move this file to `handoffs/completed/`
5. **Create your own handoff**: When finished, create handoff in `handoffs/pending/`

## AGOR Actions Required

**Next agent should:**
- Use AGOR dev tools to initialize workspace
- Create snapshots in your own agent directory
- Update shared coordination files
- Generate properly formatted outputs in single codeblocks
"""

        handoff_filename = (
            f"handoffs/pending/{timestamp_str}_{agent_id}_to_next_agent.md"
        )

        success = commit_to_memory_branch(
            file_content=handoff_content,
            file_name=handoff_filename,
            branch_name=memory_branch,
            commit_message=f"🤝 Create handoff from {agent_id}: {title}",
        )

        if success:
            print(f"✅ Created handoff: {handoff_filename}")
        else:
            print("❌ Failed to create handoff")

        return success

    except Exception as e:
        print(f"❌ Error creating handoff: {e}")
        return False


def cleanup_agent_memory_branches(
    keep_current: bool = True, cleanup_local: bool = True, current_agent_id: str = None
) -> bool:
    """
    DEPRECATED: Clean up old agent memory branches from multi-branch era.

    NOTE: This function is deprecated since we now use single memory branch architecture.
    Use cleanup_agent_directories() instead for the new directory-based approach.

    Args:
        keep_current: If True, keeps the current agent's memory branch
        cleanup_local: If True, also cleans up local memory branches
        current_agent_id: Explicit current agent ID (prevents generating wrong ID)

    Returns:
        True if cleanup was successful, False otherwise
    """
    import warnings

    warnings.warn(
        "cleanup_agent_memory_branches() is deprecated. Use cleanup_agent_directories() instead.",
        DeprecationWarning,
        stacklevel=2,
    )

    try:
        import subprocess

        # Get current agent ID safely - don't generate new one
        if keep_current:
            if current_agent_id:
                current_agent_id = sanitize_slug(current_agent_id)
            else:
                # Try to get from persistent file
                current_agent_id = get_or_create_agent_id_file()
            print(f"🆔 Current agent ID: {current_agent_id}")

        branches_deleted = 0

        # Clean up local branches first
        if cleanup_local:
            print("🧹 Cleaning up local memory branches...")
            local_result = subprocess.run(
                ["git", "branch", "--list", "agor/mem/*"],
                capture_output=True,
                text=True,
                cwd=".",
            )

            if local_result.returncode == 0 and local_result.stdout.strip():
                for line in local_result.stdout.strip().split("\n"):
                    if line.strip():
                        branch = line.strip().replace("* ", "").strip()
                        # Skip current agent's branch if keeping it
                        if (
                            keep_current
                            and current_agent_id
                            and f"agor/mem/{current_agent_id}" in branch
                        ):
                            print(f"⏭️  Keeping current agent branch: {branch}")
                            continue

                        # Delete local branch
                        delete_result = subprocess.run(
                            ["git", "branch", "-D", branch],
                            capture_output=True,
                            text=True,
                            cwd=".",
                        )
                        if delete_result.returncode == 0:
                            print(f"✅ Deleted local memory branch: {branch}")
                            branches_deleted += 1
                        else:
                            print(f"❌ Failed to delete local memory branch: {branch}")

        # Clean up remote branches
        print("🧹 Cleaning up remote memory branches...")
        remote_result = subprocess.run(
            ["git", "branch", "-r", "--list", "origin/agor/mem/*"],
            capture_output=True,
            text=True,
            cwd=".",
        )

        if remote_result.returncode == 0 and remote_result.stdout.strip():
            for line in remote_result.stdout.strip().split("\n"):
                if line.strip():
                    branch = line.strip().replace("origin/", "")
                    # Skip current agent's branch if keeping it
                    if (
                        keep_current
                        and current_agent_id
                        and f"agor/mem/{current_agent_id}" in branch
                    ):
                        print(f"⏭️  Keeping current agent remote branch: {branch}")
                        continue

                    # Delete remote branch
                    delete_result = subprocess.run(
                        ["git", "push", "origin", "--delete", branch],
                        capture_output=True,
                        text=True,
                        cwd=".",
                    )
                    if delete_result.returncode == 0:
                        print(f"✅ Deleted remote memory branch: {branch}")
                        branches_deleted += 1
                    else:
                        print(f"❌ Failed to delete remote memory branch: {branch}")

        print(f"🧹 Cleaned up {branches_deleted} memory branches total")
        return True

    except Exception as e:
        print(f"❌ Error cleaning up memory branches: {e}")
        return False


def validate_output_formatting(content: str) -> dict:
    """
    Validates whether the provided content complies with AGOR output formatting standards.

    Checks for the presence of codeblocks, triple backticks, and proper codeblock wrapping. Identifies issues such as the need for deticking or incorrect formatting of handoff prompts, and provides suggestions for compliance.

    Args:
        content: The content string to validate.

    Returns:
        A dictionary containing compliance status, detected issues, suggestions for correction, and flags indicating codeblock and deticking requirements.
    """
    validation = {
        "is_compliant": True,
        "issues": [],
        "suggestions": [],
        "has_codeblocks": False,
        "has_triple_backticks": False,
        "detick_needed": False,
    }

    # Check for codeblock presence
    if "```" in content:
        validation["has_codeblocks"] = True
        validation["has_triple_backticks"] = True

        # Check if content has triple backticks that need deticking
        if content.count("```") > 0:
            validation["detick_needed"] = True
            validation["issues"].append(
                "Content contains triple backticks that may break codeblock rendering"
            )
            validation["suggestions"].append(
                "Process through detick_content() before wrapping in codeblocks"
            )

    # Check for proper codeblock wrapping indicators
    if (not content.startswith("``") or not content.endswith("``")) and validation[
        "has_codeblocks"
    ]:
        validation["is_compliant"] = False
        validation["issues"].append(
            "Content with codeblocks should be wrapped in double backticks"
        )
        validation["suggestions"].append(
            "Wrap entire content in double backticks for copy-paste safety"
        )

    # Check for handoff prompt indicators
    if ("handoff" in content.lower() or "session end" in content.lower()) and (
        not validation["has_codeblocks"] or validation["has_triple_backticks"]
    ):
        validation["is_compliant"] = False
        validation["issues"].append(
            "Handoff prompts must be deticked and wrapped in single codeblocks"
        )
        validation["suggestions"].append(
            "Use detick_content() and wrap in double backticks"
        )

    return validation


def apply_output_formatting(content: str, content_type: str = "general") -> str:
    """
    Formats content according to AGOR output standards for safe embedding and compliance.

    Deticks the input content to remove triple backticks and wraps the result in double backtick
    codeblocks for ALL content types to ensure consistent copy-paste workflow.

    Args:
        content: Raw content to format
        content_type: Type of content (for logging/debugging purposes)

    Returns:
        Formatted content wrapped in double backticks ready for copy-paste
    """
    # Process through detick to handle any triple backticks
    processed_content = detick_content(content)

    # ALWAYS wrap in codeblock for copy-paste workflow
    formatted_content = f"``\n{processed_content}\n``"

    return formatted_content


def generate_formatted_output(content: str, content_type: str = "general") -> str:
    """
    Generate properly formatted output for user copy-paste.

    This is the main function that should be used for ALL generated outputs
    that need to be presented to users for copy-paste.

    Args:
        content: Raw content to format
        content_type: Type of content being formatted

    Returns:
        Properly formatted content ready for copy-paste
    """
    return apply_output_formatting(content, content_type)


def generate_release_notes_output(release_notes_content: str) -> str:
    """
    Generate properly formatted release notes for copy-paste.

    NOTE: Keep release notes content BRIEF to avoid processing errors.
    Long content can cause the formatting process to fail.

    Args:
        release_notes_content: Raw release notes content (keep brief)

    Returns:
        Formatted release notes wrapped in codeblock
    """
    return generate_formatted_output(release_notes_content, "release_notes")


def generate_pr_description_output(pr_content: str) -> str:
    """
    Generate properly formatted PR description for copy-paste.

    NOTE: Keep PR description content BRIEF to avoid processing errors.
    Long content can cause the formatting process to fail.

    Args:
        pr_content: Raw PR description content (keep brief)

    Returns:
        Formatted PR description wrapped in codeblock
    """
    return generate_formatted_output(pr_content, "pr_description")


def generate_handoff_prompt_output(handoff_content: str) -> str:
    """
    Generate properly formatted handoff prompt for copy-paste.

    Args:
        handoff_content: Raw handoff prompt content

    Returns:
        Formatted handoff prompt wrapped in codeblock
    """
    return generate_formatted_output(handoff_content, "handoff_prompt")


# Utility Functions
# =================


def detect_current_environment() -> dict:
    """Detect current development environment."""
    return detect_environment()


def get_available_functions_reference() -> str:
    """
    Generate comprehensive reference of all AGOR development tools functions.

    This function dynamically inspects all AGOR modules and generates a complete
    reference guide that agents MUST call to understand available functionality.

    Returns:
        Formatted string containing all function references with descriptions
    """
    import inspect
    import sys

    from agor.tools import git_operations, memory_manager, snapshot_templates

    output = []
    output.append("# 🛠️ AGOR Development Tools Functions Reference")
    output.append("")
    output.append(
        "**MANDATORY READING: All available AGOR development tools functions**"
    )
    output.append("")
    output.append("This reference is generated dynamically from actual code.")
    output.append("Call this function to see all available capabilities.")
    output.append("")

    # Current module (dev_tools)
    current_module = sys.modules[__name__]

    modules = [
        ("dev_tools", current_module, "Main development interface - START HERE"),
        (
            "memory_manager",
            memory_manager,
            "Memory branch operations - Cross-branch commits",
        ),
        (
            "git_operations",
            git_operations,
            "Git command utilities - Safe git operations",
        ),
        (
            "snapshot_templates",
            snapshot_templates,
            "Snapshot generation - Work state capture",
        ),
    ]

    for module_name, module, description in modules:
        output.append(f"## {module_name} - {description}")
        output.append("")

        functions = []
        for name, obj in inspect.getmembers(module):
            if (
                callable(obj)
                and not name.startswith("_")
                and hasattr(obj, "__doc__")
                and obj.__doc__
                and name not in ["Optional", "Path", "Tuple", "datetime"]
            ):

                # Get first line of docstring
                doc = obj.__doc__.strip()
                first_line = doc.split("\n")[0].strip()

                # Skip type hints and imports
                if (
                    first_line
                    and not first_line.startswith("Optional")
                    and not first_line.startswith("Path")
                    and not first_line.startswith("Tuple")
                    and not first_line.startswith("datetime")
                ):
                    functions.append((name, first_line))

        # Sort functions alphabetically
        functions.sort()

        for func_name, description in functions:
            output.append(f"- **{func_name}()**: {description}")
        output.append("")

    output.append("## 🎯 Key Functions for Agents")
    output.append("")
    output.append("**Memory Operations:**")
    output.append("- commit_to_memory_branch() - Cross-branch memory commits")
    output.append("- list_memory_branches() - Find existing memory branches")
    output.append("- read_from_memory_branch() - Read from memory without switching")
    output.append("")
    output.append("**Development Workflow:**")
    output.append("- create_development_snapshot() - Comprehensive work snapshots")
    output.append("- generate_session_end_prompt() - Agent handoff prompts")
    output.append("- quick_commit_and_push() - Fast commit with timestamp")
    output.append("")
    output.append("**Analysis & Status:**")
    output.append("- get_workspace_status() - Project and git status")
    output.append("- detect_environment() - Environment detection")
    output.append("- test_all_tools() - Verify all functions work")
    output.append("")
    output.append(
        "**CRITICAL**: Always use these functions instead of manual git commands"
    )
    output.append("for memory operations and cross-branch commits.")

    return "\n".join(output)


def test_all_tools() -> bool:
    """
    Runs comprehensive tests on all development tools components.

    Returns:
        True if all tests pass successfully, otherwise False.
    """
    return test_tooling()


# Workflow Optimization Functions
# ===============================


def generate_workflow_prompt_template(
    task_description: str,
    memory_branch: str = None,
    include_bookend: bool = True,
    include_explicit_requirements: bool = True,
) -> str:
    """
    Generates an optimized workflow prompt template for AGOR agent tasks.

    Creates a detailed prompt incorporating the task description, memory branch reference, session start requirements, development guidelines, mandatory session end requirements (with example code), and success criteria. Supports options to include the bookend approach and explicit handoff requirements for seamless agent coordination.

    Args:
        task_description: Description of the agent's task.
        memory_branch: Optional memory branch name for context continuity; generated if not provided.
        include_bookend: Whether to include session start and end requirements.
        include_explicit_requirements: Whether to include explicit handoff and formatting requirements.

    Returns:
        A formatted prompt template string ready for agent use.
    """
    if memory_branch is None:
        memory_branch = get_main_memory_branch()

    prompt_template = f"""# 🎯 AGOR Agent Task: {task_description}

**Memory Branch**: {memory_branch}
**Generated**: {get_current_timestamp()}

## 📋 Task Description

{task_description}

"""

    if include_bookend:
        prompt_template += """## 🚀 Session Start Requirements

Before starting work:
1. Read AGOR documentation and understand the task
2. Create a development plan and approach
3. Set up your memory branch for snapshots

"""

    prompt_template += """## 🔧 Development Guidelines

- Use quick_commit_and_push() frequently during work
- Create progress snapshots for major milestones
- Test your changes thoroughly
- Document your implementation process

"""

    if include_explicit_requirements:
        prompt_template += f"""## ⚠️ MANDATORY SESSION END REQUIREMENTS

Your response MUST end with:

1. **Development Snapshot**: Use create_development_snapshot()
2. **Handoff Prompt**: Use generate_session_end_prompt()
3. **Proper Formatting**: Process through detick_content() and wrap in codeblocks

**Memory Branch Reference**: {memory_branch}

```python
# Required session end code:
from agor.tools.dev_tools import create_development_snapshot
from agor.tools.agent_handoffs import generate_session_end_prompt, detick_content

# Create snapshot
create_development_snapshot(
    title="Your work title",
    context="Detailed description of what you accomplished"
)

# Generate handoff prompt
handoff_prompt = generate_session_end_prompt(
    work_completed=["List your accomplishments"],
    current_status="Current project status",
    next_agent_instructions=["Instructions for next agent"],
    critical_context="Important context to preserve",
    files_modified=["Files you modified"]
)

# Format and output
processed_prompt = detick_content(handoff_prompt)
print("``")
print(processed_prompt)
print("``")
```

"""

    prompt_template += """## 🎯 Success Criteria

You will have succeeded when:
- All task objectives are completed
- Changes are tested and working
- Comprehensive snapshot is created
- Handoff prompt is generated and properly formatted
- Next agent has clear instructions to continue

---

**Remember**: AGOR's goal is seamless agent coordination. Your handoff prompt should enable the next agent to continue work without manual re-entry of context."""

    return prompt_template


def validate_agor_workflow_completion(
    work_completed: list,
    files_modified: list,
    has_snapshot: bool = False,
    has_handoff_prompt: bool = False,
) -> dict:
    """
    Validates workflow completion against AGOR standards and provides feedback.

    Checks for documentation of completed work, file modifications, development snapshot creation, and handoff prompt generation. Returns a dictionary with completeness status, score, identified issues, recommendations, and any missing requirements.
    """
    validation = {
        "is_complete": True,
        "score": 0,
        "max_score": 10,
        "issues": [],
        "recommendations": [],
        "missing_requirements": [],
    }

    # Check work completion documentation
    if work_completed and len(work_completed) > 0:
        validation["score"] += 2
    else:
        validation["is_complete"] = False
        validation["issues"].append("No work completion documented")
        validation["missing_requirements"].append("Document completed work items")

    # Check file modification tracking
    if files_modified and len(files_modified) > 0:
        validation["score"] += 2
    else:
        validation["issues"].append("No file modifications documented")
        validation["recommendations"].append("Track and document all file changes")

    # Check snapshot creation
    if has_snapshot:
        validation["score"] += 3
    else:
        validation["is_complete"] = False
        validation["issues"].append("Development snapshot not created")
        validation["missing_requirements"].append(
            "Create development snapshot with create_development_snapshot()"
        )

    # Check handoff prompt generation
    if has_handoff_prompt:
        validation["score"] += 3
    else:
        validation["is_complete"] = False
        validation["issues"].append("Handoff prompt not generated")
        validation["missing_requirements"].append(
            "Generate handoff prompt with generate_session_end_prompt()"
        )

    # Add recommendations based on score
    if validation["score"] < 5:
        validation["recommendations"].append("Review AGOR workflow optimization guide")
        validation["recommendations"].append(
            "Use workflow prompt templates for better compliance"
        )
    elif validation["score"] < 8:
        validation["recommendations"].append("Improve documentation completeness")
        validation["recommendations"].append("Ensure all requirements are met")
    else:
        validation["recommendations"].append("Excellent workflow compliance!")

    return validation


def get_workflow_optimization_tips() -> str:
    """
    Returns formatted AGOR workflow optimization tips, including best practices, common issues with solutions, helper function usage examples, and success metrics to improve agent workflow compliance and coordination.
    """
    tips = f"""# 🎯 AGOR Workflow Optimization Tips

**Generated**: {get_current_timestamp()}

## 🔄 Proven Strategies

### 1. The "Bookend" Approach
- Start sessions with clear requirements
- End sessions with mandatory deliverables
- Include explicit handoff instructions

### 2. Memory Branch Strategy
- Generate unique agent memory branch: `{get_main_memory_branch()}`
- Use for all snapshots and coordination
- Reference in handoff prompts for continuity

### 3. Output Formatting Compliance
- ALL handoff prompts must be deticked and wrapped in codeblocks
- Use `detick_content()` before wrapping in double backticks
- Test formatting with `validate_output_formatting()`

## 🚨 Common Issues to Avoid

❌ **Agent doesn't create handoff prompt**
✅ **Solution**: Include explicit requirements in prompt template

❌ **Context lost between agents**
✅ **Solution**: Always reference memory branches and previous work

❌ **Formatting breaks codeblocks**
✅ **Solution**: Use detick_content() and proper wrapping

## 🛠️ Helper Functions

```python
# Generate optimized prompt
prompt = generate_workflow_prompt_template(
    task_description="Your task",
    memory_branch="agor/mem/main"
)

# Validate completion
validation = validate_agor_workflow_completion(
    work_completed=["item1", "item2"],
    files_modified=["file1.py", "file2.md"],
    has_snapshot=True,
    has_handoff_prompt=True
)

# Check output formatting
formatting = validate_output_formatting(content)
```

## 🎯 Success Metrics

**Green flags** (workflow working well):
- Agents automatically create handoff prompts
- Context flows seamlessly between agents
- Minimal user intervention required
- Work continues without manual re-entry

**Red flags** (optimization needed):
- Repeatedly reminding agents about handoffs
- Context getting lost between sessions
- Manual re-entry of requirements
- Agents not following AGOR protocols

---

**Use these tips to maintain seamless AGOR coordination workflows.**
"""

    return tips
