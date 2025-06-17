"""
AGOR Snapshot Management Module

This module handles all snapshot-related functionality including:
- Snapshot creation and management
- Agent handoff snapshot generation
- Seamless handoff coordination
- Snapshot template integration

All functions use absolute imports for better reliability.
"""

from dataclasses import dataclass
from pathlib import Path

from agor.tools.agent_handoffs import detick_content
from agor.tools.dev_testing import (
    detect_environment,
    get_agent_dependency_install_commands,
)

# Use absolute imports to prevent E0402 errors
from agor.tools.git_operations import (
    get_current_timestamp,
    get_file_timestamp,
    run_git_command,
)
from agor.tools.memory_manager import commit_to_memory_branch
from agor.tools.snapshot_templates import generate_snapshot_document


@dataclass
class HandoffRequest:
    """Configuration object for handoff operations to reduce parameter count."""

    task_description: str
    work_completed: list = None
    next_steps: list = None
    files_modified: list = None
    context_notes: str = None
    brief_context: str = None
    pr_title: str = None
    pr_description: str = None
    release_notes: str = None
    # Output selection flags for flexible generation
    generate_snapshot: bool = True
    generate_handoff_prompt: bool = True
    generate_pr_description: bool = True
    generate_release_notes: bool = True

    def __post_init__(self):
        """
        Ensures all optional fields are initialized to empty lists or strings if not provided.

        This method sets default empty values for fields that may be None after dataclass initialization, preventing issues with mutable defaults.
        """
        if self.work_completed is None:
            self.work_completed = []
        if self.next_steps is None:
            self.next_steps = []
        if self.files_modified is None:
            self.files_modified = []
        if self.context_notes is None:
            self.context_notes = ""
        if self.brief_context is None:
            self.brief_context = ""


def create_snapshot(
    title: str, context: str, agent_id: str = None, custom_branch: str = None
) -> bool:
    """Create development snapshot in agent's directory within main memory branch."""
    # Import all required functions at the top to avoid per-call overhead
    from agor.tools.dev_tools import (
        generate_agent_id,
        get_agent_directory_path,
        get_main_memory_branch,
    )
    from agor.utils import sanitize_slug

    timestamp_str = get_file_timestamp()

    # Generate agent ID if not provided
    if agent_id is None:
        agent_id = generate_agent_id()
    else:
        agent_id = sanitize_slug(agent_id)

    # Get memory branch and agent directory
    memory_branch = get_main_memory_branch(custom_branch)
    agent_dir = get_agent_directory_path(agent_id)

    # Snapshot file path within agent's directory
    safe_title = sanitize_slug(title.lower())
    snapshot_filename = f"{timestamp_str}_{safe_title}_snapshot.md"
    snapshot_file = f"{agent_dir}snapshots/{snapshot_filename}"
    # Get current git info
    success_branch, current_branch_val = run_git_command(["branch", "--show-current"])
    current_branch = current_branch_val.strip() if success_branch else "unknown"

    success_commit, current_commit_val = run_git_command(
        ["rev-parse", "--short", "HEAD"]
    )
    current_commit = current_commit_val.strip() if success_commit else "unknown"

    # Get AGOR version from environment
    try:
        version = detect_environment().get("agor_version", "0.5.0 development")
    except Exception:
        version = "0.5.0 development"

    current_time_for_snapshot = get_current_timestamp()
    snapshot_content = f"""# 📸 {title} Development Snapshot
**Generated**: {current_time_for_snapshot}
**Agent ID**: {agent_id}
**Agent**: Augment Agent (Software Engineering)
**Branch**: {current_branch}
**Commit**: {current_commit}
**AGOR Version**: {version}

## 🎯 Development Context

{context}

## 📋 Next Steps
[To be filled by continuing agent]

## 🔄 Git Status
- **Current Branch**: {current_branch}
- **Last Commit**: {current_commit}
- **Timestamp**: {current_time_for_snapshot}

---

## 🎼 **For Continuation Agent**

If you're picking up this work:
1. Review this snapshot and current progress
2. Check git status and recent commits
3. Continue from the next steps outlined above

**Remember**: Use quick_commit_push() for frequent commits during development.
"""

    # Write snapshot file locally for reference (will be ignored by .gitignore)
    repo_path = Path.cwd()
    snapshot_path = repo_path / snapshot_file
    snapshot_path.parent.mkdir(parents=True, exist_ok=True)
    snapshot_path.write_text(snapshot_content)

    # Commit snapshot to agent's directory in main memory branch (NEVER switches branches)
    commit_message = f"📸 Create development snapshot: {title} (Agent: {agent_id})"

    success = commit_to_memory_branch(
        file_content=snapshot_content,
        file_name=snapshot_file,
        branch_name=memory_branch,
        commit_message=commit_message,
    )

    if success:
        print(f"✅ Snapshot committed to memory branch: {snapshot_filename}")
    else:
        print("❌ Failed to commit snapshot to memory branch")

    return success


def generate_agent_handoff_prompt(
    task_description: str,
    snapshot_content: str = None,
    memory_branch: str = None,
    environment: dict = None,
    brief_context: str = None,
) -> str:
    """
    Generates a formatted agent handoff prompt for seamless transitions between agents.

    Creates a comprehensive prompt including environment details, setup instructions, memory branch access, task overview, brief context, and previous work context if provided. Applies automatic backtick processing to ensure safe embedding within single codeblocks.

    Args:
        task_description: Description of the task for the next agent.
        snapshot_content: Optional content summarizing previous agent work.
        memory_branch: Optional name of the memory branch for coordination.
        environment: Optional environment information; auto-detected if not provided.
        brief_context: Optional brief background for quick orientation.

    Returns:
        A processed prompt string ready for use in a single codeblock.
    """
    if environment is None:
        environment = detect_environment()

    timestamp = get_current_timestamp()

    # Start building the prompt
    prompt = f"""# 🤖 AGOR Agent Handoff

**Generated**: {timestamp}
**Environment**: {environment.get('mode', 'unknown')} ({environment.get('platform', 'unknown')})
**AGOR Version**: {environment.get('agor_version', 'unknown')}
"""

    # Add memory branch information if available
    if memory_branch:
        prompt += f"""**Memory Branch**: {memory_branch}
"""

    prompt += f"""
## Task Overview
{task_description}
"""

    # Add brief context if provided
    if brief_context:
        prompt += f"""
## Quick Context
{brief_context}
"""

    # Add environment-specific setup
    prompt += f"""
## Environment Setup
{get_agent_dependency_install_commands()}

## AGOR Initialization
Read these files to understand the system:
- src/agor/tools/README_ai.md (role selection and initialization)
- src/agor/tools/AGOR_INSTRUCTIONS.md (operational guide)
- src/agor/tools/index.md (documentation index)

Select appropriate role:
- SOLO DEVELOPER: Code analysis, implementation, technical work
- PROJECT COORDINATOR: Planning and multi-agent coordination
- AGENT WORKER: Task execution and following instructions
"""

    # Add memory branch access if applicable
    if memory_branch:
        prompt += f"""
## Memory Branch Access
Your coordination files are stored on memory branch: {memory_branch}

Access previous work context:
```bash
# View memory branch contents
git show {memory_branch}:.agor/
git show {memory_branch}:.agor/snapshots/
```
"""

    # Add snapshot content if provided
    if snapshot_content:
        prompt += f"""
## Previous Work Context
{snapshot_content}
"""

    prompt += """
## Getting Started
1. Initialize your environment using the setup commands above
2. Read the AGOR documentation files
3. Select your role based on the task requirements
4. Review any previous work context provided
5. Begin work following AGOR protocols

Remember: Always create a snapshot before ending your session using the dev tools.

---
*This handoff prompt was generated automatically with environment detection and backtick processing*
"""

    # Apply backtick processing to prevent formatting issues
    processed_prompt = detick_content(prompt)

    return processed_prompt


def create_seamless_handoff(
    task_description: str,
    work_completed: list = None,
    next_steps: list = None,
    files_modified: list = None,
    context_notes: str = None,
    brief_context: str = None,
) -> tuple[str, str]:
    """
    Generates a comprehensive agent handoff by creating a project snapshot and a formatted handoff prompt.

    This function automates the agent handoff process by generating a detailed snapshot of the current work, attempting to commit it to a dedicated memory branch with a safe fallback, and producing a ready-to-use handoff prompt with formatting safeguards. Both the snapshot content and the prompt are returned for immediate use.

    Args:
        task_description: Description of the task being handed off.
        work_completed: List of completed work items.
        next_steps: List of next steps for the receiving agent.
        files_modified: List of files that were modified.
        context_notes: Additional context notes.
        brief_context: Brief verbal background for quick orientation.

    Returns:
        Tuple of (snapshot_content, handoff_prompt) both ready for immediate use.
    """
    # Set defaults for optional parameters
    if work_completed is None:
        work_completed = []
    if next_steps is None:
        next_steps = []
    if files_modified is None:
        files_modified = []
    if context_notes is None:
        context_notes = ""
    if brief_context is None:
        brief_context = ""

    # Generate agent ID for this handoff
    from agor.tools.dev_tools import generate_agent_id, get_agent_directory_path

    agent_id = generate_agent_id()

    # Get agent directory path for proper file structure
    agent_dir = get_agent_directory_path(agent_id)

    # Generate comprehensive snapshot using snapshot_templates
    snapshot_content = generate_snapshot_document(
        problem_description=task_description,
        work_completed=work_completed,
        commits_made=[],  # Will be filled by git log if needed
        current_status="Ready for handoff",
        next_steps=next_steps,
        files_modified=files_modified,
        context_notes=context_notes,
        agent_role="SOLO DEVELOPER",
        snapshot_reason="Agent handoff coordination",
        agent_id=agent_id,
    )

    # Attempt to commit snapshot to main memory branch with agent directory structure
    memory_branch = None
    try:
        # Use main memory branch with agent directory structure
        memory_branch = "agor/mem/main"
        timestamp_str = get_file_timestamp()

        success = commit_to_memory_branch(
            file_content=snapshot_content,
            file_name=f"{agent_dir}snapshots/{timestamp_str}_handoff_snapshot.md",
            branch_name=memory_branch,
            commit_message=f"📸 Handoff snapshot for {agent_id}",
        )

        if success:
            print(f"✅ Snapshot committed to memory branch: {memory_branch}")
        else:
            print("⚠️ Memory branch commit failed, continuing with handoff prompt")
            memory_branch = None

    except Exception as e:
        print(f"⚠️ Memory branch operation failed: {e}")
        memory_branch = None

    # Generate handoff prompt
    handoff_prompt = generate_agent_handoff_prompt(
        task_description=task_description,
        snapshot_content=snapshot_content,
        memory_branch=memory_branch,
        brief_context=brief_context,
    )

    return snapshot_content, handoff_prompt


def generate_handoff_snapshot(
    task_description: str,
    work_completed: list = None,
    next_steps: list = None,
    files_modified: list = None,
    context_notes: str = None,
    agent_id: str = None,
) -> str:
    """
    Generate a comprehensive handoff snapshot using the snapshot template system.

    Args:
        task_description: Description of the task being handed off.
        work_completed: List of completed work items.
        next_steps: List of next steps for the receiving agent.
        files_modified: List of files that were modified.
        context_notes: Additional context notes.
        agent_id: Optional agent ID. If not provided, generates a new one.

    Returns:
        Formatted snapshot content ready for use.
    """
    # Set defaults for optional parameters
    if work_completed is None:
        work_completed = []
    if next_steps is None:
        next_steps = []
    if files_modified is None:
        files_modified = []
    if context_notes is None:
        context_notes = ""

    # Generate agent ID if not provided
    if agent_id is None:
        from agor.tools.dev_tools import generate_agent_id

        agent_id = generate_agent_id()

    # Generate snapshot using template system
    snapshot_content = generate_snapshot_document(
        problem_description=task_description,
        work_completed=work_completed,
        commits_made=[],  # Can be enhanced to get actual git commits
        current_status="Ready for agent handoff",
        next_steps=next_steps,
        files_modified=files_modified,
        context_notes=context_notes,
        agent_role="SOLO DEVELOPER",
        snapshot_reason="Agent coordination and handoff",
        agent_id=agent_id,
    )

    return snapshot_content


def generate_mandatory_session_end_prompt(
    task_description: str = "Session completion",
    brief_context: str = "Work session completed",
) -> str:
    """
    Generate a mandatory session end prompt for agent coordination.

    This function creates a standardized prompt that agents must use when ending sessions,
    ensuring proper handoff and coordination protocols are followed.

    Args:
        task_description: Description of the completed task.
        brief_context: Brief context about the session.

    Returns:
        Formatted session end prompt ready for use.
    """
    # Create a basic snapshot for the session
    snapshot_content = generate_handoff_snapshot(
        task_description=task_description,
        work_completed=["Session work completed"],
        next_steps=["Review session output", "Continue with next tasks"],
        context_notes=brief_context,
    )

    # Generate the handoff prompt
    handoff_prompt = generate_agent_handoff_prompt(
        task_description=f"Session End: {task_description}",
        snapshot_content=snapshot_content,
        brief_context=brief_context,
    )

    return handoff_prompt


def create_snapshot_legacy(title: str, context: str) -> bool:
    """
    Create development snapshot using legacy format.

    This function maintains compatibility with older snapshot creation patterns
    while using the new modular architecture.

    Args:
        title: Snapshot title
        context: Snapshot context

    Returns:
        True if successful, False otherwise
    """
    from agor.tools.dev_testing import detect_environment

    # Generate agent ID for legacy compatibility
    from agor.tools.dev_tools import generate_agent_id, get_agent_directory_path
    from agor.tools.git_operations import (
        get_current_timestamp,
        get_file_timestamp,
        quick_commit_push,
        run_git_command,
    )
    from agor.utils import sanitize_slug

    agent_id = generate_agent_id()
    agent_dir = get_agent_directory_path(agent_id)

    timestamp_str = get_file_timestamp()
    safe_title = sanitize_slug(title.lower())
    snapshot_file = f"{agent_dir}snapshots/{timestamp_str}_{safe_title}_snapshot.md"

    # Get current git info
    success_branch, current_branch_val = run_git_command(["branch", "--show-current"])
    current_branch = current_branch_val.strip() if success_branch else "unknown"

    success_commit, current_commit_val = run_git_command(
        ["rev-parse", "--short", "HEAD"]
    )
    current_commit = current_commit_val.strip() if success_commit else "unknown"

    # Get version from environment
    try:
        version = detect_environment().get("agor_version", "0.4.4 development")
    except Exception:
        version = "0.4.4 development"

    current_time_for_snapshot = get_current_timestamp()
    snapshot_content = f"""# 📸 {title} Development Snapshot
**Generated**: {current_time_for_snapshot}
**Agent**: Augment Agent (Software Engineering)
**Branch**: {current_branch}
**Commit**: {current_commit}
**AGOR Version**: {version}

## 🎯 Development Context

{context}

## 📋 Next Steps
[To be filled by continuing agent]

## 🔄 Git Status
- **Current Branch**: {current_branch}
- **Last Commit**: {current_commit}
- **Timestamp**: {current_time_for_snapshot}

---

## 🎼 **For Continuation Agent**

If you're picking up this work:
1. Review this snapshot and current progress
2. Check git status and recent commits
3. Continue from the next steps outlined above

**Remember**: Use quick_commit_push() for frequent commits during development.
"""

    # Write snapshot file
    repo_path = Path.cwd()
    snapshot_path = repo_path / snapshot_file
    snapshot_path.parent.mkdir(parents=True, exist_ok=True)
    snapshot_path.write_text(snapshot_content)

    # Commit and push snapshot
    return quick_commit_push(f"📸 Create development snapshot: {title}", "📸")
