"""
AGOR Development Tooling - Main Interface Module

This module provides the main interface for AGOR development utilities.
It imports functionality from specialized modules for better organization:

- git_operations: Safe git operations and timestamp utilities
- memory_manager: Cross-branch memory commits and branch management
- agent_handoffs: Agent coordination and handoff utilities
- dev_testing: Testing utilities and environment detection

Provides utility functions for frequent commits and cross-branch memory operations
to streamline development workflow and memory management.
"""

import os
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

# Import from specialized modules for modular organization
from .git_operations import (
    get_current_timestamp,
    get_file_timestamp,
    get_precise_timestamp,
    run_git_command,
    quick_commit_push
)

from .memory_manager import commit_to_memory_branch

from .agent_handoffs import detick_content

# Note: dev_testing functions are imported locally where needed to avoid redefinition conflicts

from .snapshot_templates import generate_snapshot_document # Added for create_seamless_handoff

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

        success, current_branch = run_git_command(
            ["branch", "--show-current"]
        )
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
        success, content = run_git_command(
            ["show", f"{branch_name}:{file_path}"]
        )
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


def list_memory_branches(repo_path: Optional[Path] = None) -> list[str]:
    """
    List all memory branches without switching branches.

    Uses the existing memory_sync.py implementation to avoid code duplication.

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

# DevTooling class has been removed and converted to standalone functions
# All methods are now available as module-level functions


# Convenience functions
def quick_commit_push_wrapper(message: str, emoji: str = "🔧") -> bool:
    """Quick commit and push with timestamp."""
    # Import to avoid name collision
    from agor.tools.git_operations import quick_commit_push as git_quick_commit_push
    return git_quick_commit_push(message, emoji)


def auto_commit_memory_wrapper(content: str, memory_type: str, agent_id: str = "dev") -> bool:
    """Auto-commit memory to memory branch."""
    # Import to avoid name collision
    from agor.tools.memory_manager import auto_commit_memory as memory_auto_commit
    return memory_auto_commit(content, memory_type, agent_id)


def create_snapshot(title: str, context: str) -> bool:
    """Create development snapshot."""
    # Imports are already at the top of the file:
    # from .git_operations import (_get_current_timestamp, _get_file_timestamp,
    #                              _run_git_command, _quick_commit_push)
    # from .snapshot_templates import generate_snapshot_document (This needs to be added)
    # For now, assuming generate_snapshot_document is available or will be added.
    # We also need Path from pathlib, which is already imported.

    # Replicating logic from DevTooling.create_development_snapshot
    timestamp_str = get_file_timestamp()  # Use direct name
    snapshot_file = (
        f".agor/snapshots/{timestamp_str}_{title.lower().replace(' ', '-')}_snapshot.md"
    )

    # Get current git info
    success_branch, current_branch_val = run_git_command(["branch", "--show-current"]) # Use direct name
    current_branch = current_branch_val.strip() if success_branch else "unknown"

    success_commit, current_commit_val = run_git_command(["rev-parse", "--short", "HEAD"]) # Use direct name
    current_commit = current_commit_val.strip() if success_commit else "unknown"

    # Assuming AGOR_VERSION is a global or accessible constant, or we fetch it.
    # For now, let's keep the hardcoded version as in the original, or retrieve it if possible.
    # It was "0.4.1 development" in the original method.
    # Let's try to get it from detect_environment
    try:
        version = detect_environment().get("agor_version", "0.4.1 development")
    except Exception:
        version = "0.4.1 development"


    # The original DevTooling.create_development_snapshot used a specific f-string format.
    # snapshot_templates.generate_snapshot_document might have a different structure.
    # The instruction is: "if `create_snapshot` calls `snapshot_templates.generate_snapshot_document` AND `git_operations.quick_commit_push` directly"
    # This implies we should ideally use `generate_snapshot_document`.
    # However, `generate_snapshot_document` has a different signature:
    # (problem_description, work_completed, commits_made, current_status, next_steps, files_modified, context_notes, agent_role, snapshot_reason)
    # The current `create_snapshot(title, context)` only takes title and context.
    # We need to adapt. Let's use `title` as `snapshot_reason` and `context` as `problem_description` or `context_notes`.

    # Option 1: Stick to the original content structure for now, then adapt to generate_snapshot_document if required.
    # Option 2: Try to use generate_snapshot_document directly.
    # Given the instructions, let's try to use `generate_snapshot_document`.
    # We'll need to map `title` and `context` appropriately.
    # Let `title` be `snapshot_reason` and `context` be `context_notes`.
    # `problem_description` can be derived from title or context.

    # For now, to keep changes minimal and focused on removing dev_tools dependency,
    # I will replicate the existing snapshot content generation logic first.
    # Then, in a subsequent step or if this fails, I will adapt to snapshot_templates.generate_snapshot_document.

    current_time_for_snapshot = get_current_timestamp() # Use direct name
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
    # repo_path should be Path.cwd() if dev_tools instance is not used.
    # The original DevTooling class used self.repo_path which defaulted to Path.cwd()
    repo_path = Path.cwd()
    snapshot_path = repo_path / snapshot_file
    snapshot_path.parent.mkdir(parents=True, exist_ok=True)
    snapshot_path.write_text(snapshot_content)

    # Commit and push snapshot
    return quick_commit_push(f"📸 Create development snapshot: {title}", "📸") # Use direct name


def test_tooling_wrapper() -> bool:
    """Test all development tooling functions."""
    # Import to avoid name collision
    from agor.tools.dev_testing import test_tooling as dev_test_tooling
    return dev_test_tooling()


# Timestamp utilities
def get_timestamp() -> str:
    """Get current UTC timestamp."""
    return get_current_timestamp() # Use direct name (imported from git_operations)





def detick_content_wrapper(content: str) -> str:
    """
    Replaces all triple backticks in the content with double backticks for safe embedding within a single codeblock.
    """
    # Import to avoid name collision
    from agor.tools.agent_handoffs import detick_content as handoff_detick_content
    return handoff_detick_content(content)


def retick_content_wrapper(content: str) -> str:
    """
    Converts double backticks (``) in the content back to triple backticks (```) for standard codeblock formatting.

    Args:
        content: The string content with double backticks to be converted.

    Returns:
        The content with double backticks replaced by triple backticks.
    """
    # Import to avoid name collision
    from agor.tools.agent_handoffs import retick_content as handoff_retick_content
    return handoff_retick_content(content)


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
        environment = detect_environment() # from .dev_testing

    timestamp = get_current_timestamp() # from .git_operations

    # Start building the prompt
    prompt = f"""# 🤖 AGOR Agent Handoff

**Generated**: {timestamp}
**Environment**: {environment['mode']} ({environment['platform']})
**AGOR Version**: {environment['agor_version']}
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
    # get_agent_dependency_install_commands is imported from .dev_testing
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

Remember: Always create a snapshot before ending your session using the dev tooling.

---
*This handoff prompt was generated automatically with environment detection and backtick processing*
"""

    # Apply backtick processing to prevent formatting issues
    processed_prompt = detick_content(prompt) # Use direct name

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
        A tuple containing the snapshot content and the processed handoff prompt.
    """
    # generate_snapshot_document is now imported at the top.

    # Generate comprehensive snapshot
    snapshot_content = generate_snapshot_document(
        problem_description=task_description,
        work_completed=work_completed or [],
        commits_made=[],  # Will be filled by git context
        current_status="Ready for handoff",
        next_steps=next_steps or [],
        files_modified=files_modified or [],
        context_notes=context_notes or "",
        agent_role="Handoff Agent",
        snapshot_reason="Agent transition handoff",
    )

    # Attempt to save snapshot to memory branch using safe cross-branch commit
    memory_branch = None
    try:
        from agor.memory_sync import MemorySync

        memory_sync = MemorySync()
        memory_branch = memory_sync.generate_memory_branch_name()

        # Create snapshot file in current working directory
        snapshot_dir = Path(".agor/snapshots")
        snapshot_dir.mkdir(parents=True, exist_ok=True)

        timestamp_str = get_file_timestamp() # Use direct name
        snapshot_file = snapshot_dir / f"{timestamp_str}_handoff_snapshot.md"
        snapshot_file.write_text(snapshot_content)

        # Use safe cross-branch commit that NEVER switches branches
        commit_message = f"📸 Agent handoff snapshot: {task_description[:50]}"

        # Read the snapshot content to commit to memory branch
        snapshot_content_for_commit = snapshot_file.read_text()

        if commit_to_memory_branch( # Use direct name
            file_content=snapshot_content_for_commit,
            file_name=f"{timestamp_str}_handoff_snapshot.md",
            branch_name=memory_branch,
            commit_message=commit_message
        ):
            print(f"✅ Snapshot safely committed to memory branch: {memory_branch}")
        else:
            print("⚠️ Cross-branch commit failed, using regular commit as fallback")
            quick_commit_push(commit_message, "📸") # Use direct name
            memory_branch = None

    except Exception as e:
        memory_branch = None
        print(f"⚠️ Memory sync not available: {e}, proceeding without memory branch")

        # Fallback: regular commit to current branch
        try:
            quick_commit_push( # Use direct name
                f"📸 Agent handoff snapshot: {task_description[:50]}", "📸"
            )
        except Exception as fallback_error:
            print(f"⚠️ Fallback commit also failed: {fallback_error}")

    # Verify we're still on the original branch (should never change)
    try:
        import subprocess

        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            check=True,
        )
        current_branch = result.stdout.strip()
        print(f"✅ Branch safety verified: {current_branch}")

        # Warn if we're on a memory branch (should never happen with safe commit)
        if current_branch.startswith("agor/mem/"):
            print("🚨 CRITICAL: Branch safety violation detected!")
        elif current_branch == "main":
            print(
                "⚠️ WARNING: Currently on main branch - consider using a feature branch"
            )
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Could not verify branch status: {e}")
    except Exception as e:
        print(f"⚠️ Unexpected error checking branch status: {e}")

    # Generate handoff prompt with automatic backtick processing
    # This now calls the global generate_agent_handoff_prompt which is already refactored
    handoff_prompt = generate_agent_handoff_prompt(
        task_description=task_description,
        snapshot_content=snapshot_content,
        memory_branch=memory_branch,
        brief_context=brief_context,
    )

    return snapshot_content, handoff_prompt


# Removed redefined functions - use imports from specialized modules instead


def generate_dynamic_codeblock_prompt(
    task_description: str, environment: dict = None, include_snapshot: str = None
) -> str:
    """
    Generates a formatted codeblock prompt with environment details, AGOR version, task description, setup instructions, protocol guidance, and optional previous work context.

    Args:
        task_description: The description of the task to be performed.
        environment: Optional dictionary with environment details; auto-detected if not provided.
        include_snapshot: Optional string containing previous work context to include in the prompt.

    Returns:
        A Markdown-formatted string suitable for use as a codeblock prompt, including environment and setup information.
    """
    # Import locally to avoid redefinition conflicts
    from .dev_testing import detect_environment, generate_dynamic_installation_prompt

    if environment is None:
        environment = detect_environment()

    timestamp = get_current_timestamp()

    prompt = f"""# 🚀 AGOR Dynamic Codeblock Prompt

**Generated**: {timestamp}
**Environment**: {environment['mode']} ({environment['platform']})
**AGOR Version**: {environment['agor_version']}

## Task Description
{task_description}

## Environment Setup
{generate_dynamic_installation_prompt(environment)}

## AGOR Protocol Initialization
Please read these key files to understand the system:
1. Read src/agor/tools/README_ai.md for role selection and initialization
2. Read src/agor/tools/AGOR_INSTRUCTIONS.md for comprehensive instructions
3. Read src/agor/tools/index.md for quick reference lookup

After reading these files, help me select the appropriate role:
- SOLO DEVELOPER: For code analysis, implementation, and technical work
- PROJECT COORDINATOR: For planning and multi-agent coordination
- AGENT WORKER: For executing specific tasks and following instructions

Environment: {environment['platform']}
Mode: {environment['mode']}
"""

    if include_snapshot:
        prompt += f"""
## Previous Work Context
{include_snapshot}
"""

    prompt += """
## Next Steps
[Add your specific project instructions and requirements here]

---
*This prompt was generated dynamically with current environment detection and version information*
"""

    return prompt


def update_version_references(target_version: str = None) -> list:
    """
    Updates version strings in documentation and source files to the specified or detected AGOR version.

    If no version is provided, uses the AGOR package version or defaults to "0.4.1". Searches predefined files for common version reference patterns and replaces them with the target version.

    Returns:
        A list of file paths that were updated.
    """
    if target_version is None:
        try:
            from agor import __version__

            target_version = __version__
        except ImportError:
            target_version = "0.4.1"  # fallback

    updated_files = []
    version_patterns = [
        (r"agor, version \d+\.\d+\.\d+", f"agor, version {target_version}"),
        (r"\*\*AGOR Version\*\*: \d+\.\d+\.\d+", f"**AGOR Version**: {target_version}"),
        (r"version \d+\.\d+\.\d+ development", f"version {target_version} development"),
    ]

    # Files that commonly contain version references
    version_files = [
        "docs/quick-start.md",
        "src/agor/tools/dev_tooling.py",
        "README.md",
        "docs/bundle-mode.md",
    ]

    for file_path in version_files:
        file_path_obj = Path(file_path)
        if file_path_obj.exists():
            content = file_path_obj.read_text()
            original_content = content

            for pattern, replacement in version_patterns:
                import re

                content = re.sub(pattern, replacement, content)

            if content != original_content:
                try:
                    file_path_obj.write_text(content)
                    updated_files.append(file_path)
                    print(f"✅ Updated version references in {file_path}")
                except Exception as e:
                    print(f"❌ Failed to update {file_path}: {e}")

    return updated_files


# Agent Internal Checklist System
class AgentChecklist:
    """Internal agent checklist for tracking mandatory procedures."""

    def __init__(self, agent_role: str = "solo_developer"):
        self.agent_role = agent_role
        self.session_id = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        self.mandatory_items = self._get_mandatory_items()
        self.completed_items = set()
        self.snapshot_created = False

    def _get_mandatory_items(self) -> dict:
        """Get mandatory checklist items based on role."""
        base_items = {
            "read_docs": "Read AGOR documentation",
            "git_setup": "Configure git and create feature branch",
            "frequent_commits": "Commit and push frequently",
            "create_snapshot": "Create snapshot before session end",
            "update_coordination": "Update coordination files",
        }

        role_items = {
            "solo_developer": {
                "analyze_codebase": "Perform codebase analysis",
                "test_changes": "Test all changes",
            },
            "project_coordinator": {
                "select_strategy": "Select development strategy",
                "coordinate_team": "Set up team coordination",
            },
            "agent_worker": {
                "receive_task": "Receive task from coordinator",
                "report_completion": "Report task completion",
            },
        }

        base_items.update(role_items.get(self.agent_role, {}))
        return base_items

    def mark_complete(self, item_id: str, auto_trigger: bool = True):
        """Mark checklist item as complete."""
        if item_id in self.mandatory_items:
            self.completed_items.add(item_id)
            if auto_trigger:
                self._auto_trigger(item_id)

    def _auto_trigger(self, item_id: str):
        """Auto-trigger validation for checklist items."""
        if item_id == "git_setup":
            self._verify_git_setup()
        elif item_id == "frequent_commits":
            self._check_commit_frequency()
        elif item_id == "create_snapshot":
            self.snapshot_created = True

    def _verify_git_setup(self):
        """Verify git configuration."""
        try:
            import subprocess

            # Check git config
            result = subprocess.run(
                ["git", "config", "user.name"], capture_output=True, text=True
            )
            if not result.stdout.strip():
                print("⚠️  Git user.name not configured")
                return False

            result = subprocess.run(
                ["git", "config", "user.email"], capture_output=True, text=True
            )
            if not result.stdout.strip():
                print("⚠️  Git user.email not configured")
                return False

            # Check if on feature branch
            result = subprocess.run(
                ["git", "branch", "--show-current"], capture_output=True, text=True
            )
            current_branch = result.stdout.strip()

            if current_branch in ["main", "master"]:
                print("⚠️  Working on main branch - should create feature branch")
                return False

            print(f"✅ Git setup verified - on branch: {current_branch}")
            return True
        except Exception as e:
            print(f"⚠️  Git verification failed: {e}")
            return False

    def _check_commit_frequency(self):
        """Check if commits are frequent enough."""
        try:
            import subprocess

            result = subprocess.run(
                ["git", "log", "--oneline", "-5", "--since=1 hour ago"],
                capture_output=True,
                text=True,
            )
            commits = (
                len(result.stdout.strip().split("\n")) if result.stdout.strip() else 0
            )
            if commits < 2:
                print("💡 Reminder: Consider committing more frequently")
            else:
                print(f"✅ Good commit frequency: {commits} recent commits")
        except Exception as e:
            print(f"⚠️  Commit frequency check failed: {e}")

    def get_status(self) -> dict:
        """Get checklist status."""
        total = len(self.mandatory_items)
        completed = len(self.completed_items)
        incomplete = [
            item for item in self.mandatory_items if item not in self.completed_items
        ]

        return {
            "completion_percentage": (completed / total) * 100 if total > 0 else 0,
            "completed": completed,
            "total": total,
            "incomplete": incomplete,
            "snapshot_created": self.snapshot_created,
            "can_end_session": len(incomplete) == 0 and self.snapshot_created,
        }

    def enforce_session_end(self) -> bool:
        """Enforce mandatory procedures before session end."""
        status = self.get_status()

        if not status["can_end_session"]:
            print("🚨 Cannot end session - incomplete mandatory items:")
            for item in status["incomplete"]:
                print(f"  ❌ {self.mandatory_items[item]}")

            if not status["snapshot_created"]:
                print("  ❌ Snapshot not created")

            return False

        print("✅ All mandatory procedures complete - session can end")
        return True


# Global agent checklist instance
_agent_checklist = None


def init_agent_checklist(role: str = "solo_developer") -> AgentChecklist:
    """Initialize agent checklist for session."""
    global _agent_checklist
    _agent_checklist = AgentChecklist(role)
    print(
        f"📋 Internal checklist created for {role} with {len(_agent_checklist.mandatory_items)} items"
    )
    return _agent_checklist


def mark_checklist_complete(item_id: str):
    """Mark checklist item as complete."""
    if _agent_checklist:
        _agent_checklist.mark_complete(item_id)


def get_checklist_status() -> dict:
    """
    Retrieves the current status of the agent checklist.

    Returns:
        A dictionary containing checklist completion status and related information, or
        {"status": "no_checklist"} if no checklist is initialized.
    """
    if _agent_checklist:
        return _agent_checklist.get_status()
    return {"status": "no_checklist"}


def enforce_session_end() -> bool:
    """
    Checks if all mandatory agent session tasks are complete and enforces session end requirements.

    Returns:
        True if the session can end (all checklist items complete and snapshot created), False otherwise.
    """
    if _agent_checklist:
        return _agent_checklist.enforce_session_end()
    return True


# New hotkey processing functions
def process_progress_report_hotkey(
    task_description: str = "", progress: str = "50%"
) -> str:
    """Process progress-report hotkey and create progress report snapshot."""
    from agor.tools.snapshot_templates import (
        generate_progress_report_snapshot,
        save_progress_report_snapshot,
    )

    # Get user input for progress report details
    if not task_description:
        task_description = input("📊 Enter current task description: ")
    if progress == "50%":
        progress = input("📈 Enter progress percentage (e.g., 75%): ")

    work_completed = []
    print("✅ Enter completed work items (press Enter on empty line to finish):")
    while True:
        item = input("  - ")
        if not item:
            break
        work_completed.append(item)

    blockers = []
    print("🚧 Enter current blockers (press Enter on empty line to finish):")
    while True:
        blocker = input("  - ")
        if not blocker:
            break
        blockers.append(blocker)

    next_steps = []
    print("🔄 Enter next immediate steps (press Enter on empty line to finish):")
    while True:
        step = input("  - ")
        if not step:
            break
        next_steps.append(step)

    # Generate and save progress report
    report_content = generate_progress_report_snapshot(
        current_task=task_description,
        progress_percentage=progress,
        work_completed=work_completed,
        current_blockers=blockers,
        next_immediate_steps=next_steps,
        commits_made=["Recent commits from git log"],
        files_modified=["Files from git status"],
        agent_role="Solo Developer",
        estimated_completion_time=input("⏱️ Estimated completion time: ") or "Unknown",
        additional_notes=input("💡 Additional notes: ") or "None",
    )

    snapshot_file = save_progress_report_snapshot(report_content, task_description)
    print(f"📊 Progress report snapshot created: {snapshot_file}")

    # Mark checklist item complete
    mark_checklist_complete("create_snapshot")

    return str(snapshot_file)


def process_work_order_hotkey(task_description: str = "") -> str:
    """Process work-order hotkey and create work order snapshot."""
    from agor.tools.snapshot_templates import (
        generate_work_order_snapshot,
        save_work_order_snapshot,
    )

    # Get user input for work order details
    if not task_description:
        task_description = input("📋 Enter task description: ")

    requirements = []
    print("📋 Enter task requirements (press Enter on empty line to finish):")
    while True:
        req = input("  - ")
        if not req:
            break
        requirements.append(req)

    acceptance_criteria = []
    print("✅ Enter acceptance criteria (press Enter on empty line to finish):")
    while True:
        criteria = input("  - ")
        if not criteria:
            break
        acceptance_criteria.append(criteria)

    files_to_modify = []
    print("📁 Enter files to modify (press Enter on empty line to finish):")
    while True:
        file = input("  - ")
        if not file:
            break
        files_to_modify.append(file)

    # Generate and save work order
    order_content = generate_work_order_snapshot(
        task_description=task_description,
        task_requirements=requirements,
        acceptance_criteria=acceptance_criteria,
        files_to_modify=files_to_modify,
        reference_materials=[
            input("📚 Reference materials: ") or "See project documentation"
        ],
        coordinator_id=input("👤 Coordinator ID: ") or "Project Coordinator",
        assigned_agent_role=input("🤖 Assigned agent role: ") or "Agent Worker",
        priority_level=input("⚡ Priority level (High/Medium/Low): ") or "Medium",
        estimated_effort=input("⏱️ Estimated effort: ") or "Unknown",
        deadline=input("📅 Deadline: ") or "None specified",
        context_notes=input("🧠 Context notes: ") or "None",
    )

    snapshot_file = save_work_order_snapshot(order_content, task_description)
    print(f"📋 Work order snapshot created: {snapshot_file}")

    # Mark checklist item complete
    mark_checklist_complete("create_snapshot")

    return str(snapshot_file)


def process_create_pr_hotkey(pr_title: str = "") -> str:
    """Process create-pr hotkey and generate PR description for user to copy."""
    from agor.tools.snapshot_templates import (
        generate_pr_description_snapshot,
        save_pr_description_snapshot,
    )

    # Get user input for PR description details
    if not pr_title:
        pr_title = input("🔀 Enter PR title: ")

    pr_description = input("📝 Enter PR description: ")

    work_completed = []
    print("✅ Enter completed work items (press Enter on empty line to finish):")
    while True:
        item = input("  - ")
        if not item:
            break
        work_completed.append(item)

    testing_completed = []
    print("🧪 Enter testing completed (press Enter on empty line to finish):")
    while True:
        test = input("  - ")
        if not test:
            break
        testing_completed.append(test)

    breaking_changes = []
    print("⚠️ Enter breaking changes (press Enter on empty line to finish):")
    while True:
        change = input("  - ")
        if not change:
            break
        breaking_changes.append(change)

    # Get git information using proper git manager
    try:
        git_binary = git_manager.get_git_binary()
        commits = (
            subprocess.check_output([git_binary, "log", "--oneline", "-10"], text=True)
            .strip()
            .split("\n")
        )
        files_changed = (
            subprocess.check_output(
                [git_binary, "diff", "--name-only", "main"], text=True
            )
            .strip()
            .split("\n")
        )
    except Exception as err:
        commits = [f"Git error: {err}"]
        files_changed = ["<unknown>"]
    # Get additional PR details
    target_branch = input("🎯 Target branch (default: main): ") or "main"

    reviewers_input = input("👥 Requested reviewers (comma-separated): ")
    reviewers_requested = reviewers_input.split(",") if reviewers_input.strip() else []

    issues_input = input("🔗 Related issues (comma-separated): ")
    related_issues = issues_input.split(",") if issues_input.strip() else []

    # Generate and save PR description snapshot
    pr_content = generate_pr_description_snapshot(
        pr_title=pr_title,
        pr_description=pr_description,
        work_completed=work_completed,
        commits_included=commits,
        files_changed=files_changed,
        testing_completed=testing_completed,
        breaking_changes=breaking_changes,
        agent_role="Solo Developer",
        target_branch=target_branch,
        reviewers_requested=reviewers_requested,
        related_issues=related_issues,
    )

    snapshot_file = save_pr_description_snapshot(pr_content, pr_title)
    print(f"🔀 PR description snapshot created: {snapshot_file}")
    print(
        "📋 User can copy the PR description from the snapshot to create the actual pull request"
    )

    # Mark checklist item complete
    mark_checklist_complete("create_snapshot")

    return str(snapshot_file)


def log_to_agentconvo(agent_id: str, message: str, memory_branch: str = None) -> bool:
    """
    SAFE agentconvo logging with memory branch support - never switches branches.

    Args:
        agent_id: Agent identifier
        message: Message to log
        memory_branch: Memory branch to use (auto-generated if None)

    Returns:
        True if successful, False otherwise
    """
    timestamp = get_precise_timestamp() # Use direct name
    log_entry = f"{agent_id}: {timestamp} - {message}\n"

    if not memory_branch:
        memory_branch = f"agor/mem/{get_file_timestamp()}" # Use direct name

    print(f"📝 Logging to agentconvo.md: {agent_id} - {message}")

    # Create agentconvo.md content
    agentconvo_content = f"""# Agent Communication Log

Format: [AGENT-ID] [TIMESTAMP] - [STATUS/QUESTION/FINDING]

## Communication History

{log_entry}
"""
    # Determine repo_path, assuming Path.cwd() as DevTooling did.
    repo_path = Path.cwd()
    agentconvo_path = repo_path / ".agor" / "agentconvo.md"
    agentconvo_path.parent.mkdir(parents=True, exist_ok=True)

    # Append to existing file or create new one
    if agentconvo_path.exists():
        with open(agentconvo_path, "a") as f:
            f.write(log_entry)
    else:
        agentconvo_path.write_text(agentconvo_content)

    # Try to commit to memory branch using new safe system
    # commit_to_memory_branch is from .memory_manager
    # quick_commit_push is from .git_operations
    # Read the agentconvo content to commit to memory branch
    agentconvo_content_for_commit = agentconvo_path.read_text()

    if commit_to_memory_branch( # Use direct name
        file_content=agentconvo_content_for_commit,
        file_name="agentconvo.md",
        branch_name=memory_branch,
        commit_message=f"Update agentconvo.md: {agent_id} - {message}"
    ):
        print(f"✅ Agentconvo logged to memory branch {memory_branch}")
        return True
    else:
        # Fallback: regular commit to current branch
        print("⚠️  Memory branch commit failed, using regular commit")
        return quick_commit_push( # Use direct name
            message=f"Update agentconvo.md: {agent_id} - {message}", emoji="💬"
        )


def update_agent_memory(
    agent_id: str, memory_type: str, content: str, memory_branch: str = None
) -> bool:
    """
    Appends a memory entry for an agent to a dedicated memory file and commits it to a memory branch without switching branches.

    If committing to the memory branch fails, falls back to a regular commit on the current branch. Returns True if the update and commit succeed, otherwise False.

    Args:
        agent_id: Identifier for the agent whose memory is being updated.
        memory_type: Category of the memory entry (e.g., progress, decision).
        content: The memory content to append.
        memory_branch: Optional memory branch name; auto-generated if not provided.

    Returns:
        True if the memory update and commit succeed, False otherwise.
    """
    memory_file_relative_path = f".agor/{agent_id.lower()}-memory.md"
    timestamp = get_current_timestamp() # Use direct name

    if not memory_branch:
        memory_branch = f"agor/mem/{get_file_timestamp()}" # Use direct name

    print(f"🧠 Updating {agent_id} memory: {memory_type}")

    # Create or update memory content
    memory_entry = f"""
## {memory_type.title()} - {timestamp}

{content}

---
"""

    # Write memory file to current working directory
    repo_path = Path.cwd() # Assuming Path.cwd() as DevTooling did
    memory_path_absolute = repo_path / memory_file_relative_path
    memory_path_absolute.parent.mkdir(parents=True, exist_ok=True)

    # Append to existing file or create new one
    if memory_path_absolute.exists():
        with open(memory_path_absolute, "a") as f:
            f.write(memory_entry)
    else:
        initial_content = f"""# {agent_id.title()} Memory Log

## Current Task
[Describe the task you're working on]

## Decisions Made
- [Key architectural choices]
- [Implementation approaches]

## Files Modified
- [List of changed files with brief description]

## Problems Encountered
- [Issues hit and how resolved]

## Next Steps
- [What needs to be done next]

{memory_entry}
"""
        memory_path_absolute.write_text(initial_content)

    # Try to commit to memory branch using new safe system
    # commit_to_memory_branch is from .memory_manager
    # quick_commit_push is from .git_operations
    # Read the memory content to commit to memory branch
    memory_content_for_commit = memory_path_absolute.read_text()

    if commit_to_memory_branch( # Use direct name
        file_content=memory_content_for_commit,
        file_name=f"{agent_id.lower()}-memory.md",
        branch_name=memory_branch,
        commit_message=f"Update {agent_id} memory: {memory_type}"
    ):
        print(f"✅ Agent memory logged to memory branch {memory_branch}")
        return True
    else:
        # Fallback: regular commit to current branch
        print("⚠️  Memory branch commit failed, using regular commit")
        return quick_commit_push( # Use direct name
            message=f"Update {agent_id} memory: {memory_type}", emoji="🧠"
        )


# Convenience functions for the new handoff system
def generate_processed_output(content: str, output_type: str = "general") -> str:
    """
    Processes content for safe inclusion in a single codeblock, adding a header indicating the output type.

    Args:
        content: The content to process.
        output_type: A label describing the type of output (e.g., "handoff", "snapshot").

    Returns:
        The processed content with backtick escaping and a descriptive header.
    """
    # Replicating DevTooling.generate_processed_output's logic
    # prepare_prompt_content (which is what DevTooling.prepare_prompt_content did) is now detick_content
    processed_content = detick_content(content) # Use direct name

    header = f"# Processed {output_type.replace('_', ' ').title()} - Ready for Single Codeblock Usage\n\n"
    return header + processed_content


def generate_final_handoff_outputs(
    task_description: str,
    work_completed: list = None,
    next_steps: list = None,
    files_modified: list = None,
    context_notes: str = None,
    brief_context: str = None,
    pr_title: str = None,
    pr_description: str = None,
) -> dict:
    """
    Generates all final outputs for an agent handoff, including snapshot, handoff prompt, and optionally PR description, with automatic backtick processing for safe codeblock embedding.

    Args:
        task_description: Description of the current task or handoff context.
        work_completed: List of completed work items to include in the outputs.
        next_steps: List of recommended next steps for the agent.
        files_modified: List of files changed during the task.
        context_notes: Additional context or notes relevant to the handoff.
        brief_context: Short summary of the context for quick reference.
        pr_title: Title for the pull request, if generating a PR description.
        pr_description: Description for the pull request, if generating a PR description.

    Returns:
        A dictionary containing the generated outputs:
            - 'snapshot': Processed snapshot content.
            - 'handoff_prompt': Processed handoff prompt.
            - 'pr_description': Processed PR description (if provided).
            - 'success': Boolean indicating success.
            - 'message': Status or error message.
            - 'error': Error details if generation fails.
    """
    outputs = {}

    try:
        # Generate handoff using the seamless handoff system
        snapshot_content, handoff_prompt = create_seamless_handoff(
            task_description=task_description,
            work_completed=work_completed or [],
            next_steps=next_steps or [],
            files_modified=files_modified or [],
            context_notes=context_notes or "",
            brief_context=brief_context or "",
        )

        # Process outputs for single codeblock usage
        outputs["snapshot"] = generate_processed_output(snapshot_content, "snapshot")
        outputs["handoff_prompt"] = generate_processed_output(
            handoff_prompt, "handoff_prompt"
        )

        # Generate PR description if provided
        if pr_title and pr_description:
            processed_pr = generate_processed_output(pr_description, "pr_description")
            outputs["pr_description"] = processed_pr

        outputs["success"] = True
        outputs["message"] = (
            "All outputs generated successfully with backtick processing"
        )

    except Exception as e:
        outputs["success"] = False
        outputs["error"] = str(e)
        outputs["message"] = f"Failed to generate outputs: {e}"

    return outputs


def generate_complete_project_outputs(request: HandoffRequest) -> dict:
    """
    Generates selected project outputs such as snapshot, handoff prompt, PR description, and release notes in memory.

    Processes outputs for safe embedding in single codeblocks, based on the configuration and flags in the provided HandoffRequest. Returns a dictionary containing the requested outputs and a combined display string. No temporary files are created.

    Args:
        request: HandoffRequest specifying content, context, and which outputs to generate.

    Returns:
        Dictionary with processed outputs (e.g., 'snapshot', 'handoff_prompt', 'pr_description', 'release_notes') and a combined display string under 'display_all'. Includes 'success' and 'message' keys indicating operation status.
    """
    try:
        outputs = {
            "success": True,
            "message": "Selected outputs generated successfully",
        }

        # Generate snapshot and handoff prompt if requested
        # generate_final_handoff_outputs is a global refactored function
        # generate_processed_output is a global refactored function
        if request.generate_snapshot or request.generate_handoff_prompt:
            handoff_outputs = generate_final_handoff_outputs( # global function
                task_description=request.task_description,
                work_completed=request.work_completed,
                next_steps=request.next_steps,
                files_modified=request.files_modified,
                context_notes=request.context_notes,
                brief_context=request.brief_context,
                pr_title=(
                    request.pr_title if request.generate_pr_description else None
                ),
                pr_description=(
                    request.pr_description
                    if request.generate_pr_description
                    else None
                ),
            )

            if not handoff_outputs["success"]:
                return handoff_outputs

            # Add only requested outputs
            if request.generate_snapshot and "snapshot" in handoff_outputs:
                outputs["snapshot"] = handoff_outputs["snapshot"]
            if (
                request.generate_handoff_prompt
                and "handoff_prompt" in handoff_outputs
            ):
                outputs["handoff_prompt"] = handoff_outputs["handoff_prompt"]
            if (
                request.generate_pr_description
                and "pr_description" in handoff_outputs
            ):
                outputs["pr_description"] = handoff_outputs["pr_description"]

        # Generate standalone PR description if requested but not generated above
        elif request.generate_pr_description and request.pr_description:
            processed_pr = generate_processed_output( # global function
                request.pr_description, "pr_description"
            )
            outputs["pr_description"] = processed_pr

        # Generate release notes if requested and provided
        if request.generate_release_notes and request.release_notes:
            processed_release_notes = generate_processed_output( # global function
                request.release_notes, "release_notes"
            )
            outputs["release_notes"] = processed_release_notes

        # Add convenience method for displaying selected outputs
        # _format_all_outputs_display_static is the module-level helper defined previously
        outputs["display_all"] = _format_all_outputs_display_static(outputs)

        return outputs

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to generate selected project outputs: {e}",
        }


# This is the helper method that was inside DevTooling class
def _format_all_outputs_display_static(outputs: dict) -> str:
    """
    Formats all generated project outputs into a single display string.

    Combines handoff prompt, PR description, and release notes into a unified, human-readable format suitable for display or copying, with headers and usage instructions.
    """
    display_parts = []

    display_parts.append(
        "🚀 Complete Project Outputs - All Processed for Single Codeblock Usage"
    )
    display_parts.append("=" * 80)

    if "handoff_prompt" in outputs:
        display_parts.append("\n📸 FINAL SNAPSHOT & HANDOFF PROMPT")
        display_parts.append("=" * 80)
        display_parts.append(outputs["handoff_prompt"])

    if "pr_description" in outputs:
        display_parts.append("\n📋 FINAL PR DESCRIPTION")
        display_parts.append("=" * 80)
        display_parts.append(outputs["pr_description"])

    if "release_notes" in outputs:
        display_parts.append("\n📦 FINAL RELEASE NOTES")
        display_parts.append("=" * 80)
        display_parts.append(outputs["release_notes"])

    display_parts.append(
        "\n🎉 All outputs generated and processed for single codeblock usage!"
    )
    display_parts.append(
        "Use 'agor retick' to restore triple backticks when needed for external usage."
    )

    return "\n".join(display_parts)


# Now refactor generate_complete_project_outputs itself
# This is a separate search/replace block for clarity, applied after the helper is defined.
# The search for `generate_complete_project_outputs` will be in a new block.

def generate_pr_description_only(
    task_description: str,
    pr_title: str,
    pr_description: str,
    work_completed: list = None,
) -> dict:
    """
    Generates a processed pull request description for a given task.

    Creates a PR description output using the provided task description, PR title, PR description, and optionally a list of completed work. Other outputs such as snapshots, handoff prompts, or release notes are not generated.

    Args:
        task_description: Description of the task or feature for the PR.
        pr_title: Title for the pull request.
        pr_description: Detailed description for the pull request.
        work_completed: Optional list of completed work items to include.

    Returns:
        A dictionary containing the processed PR description and related output fields.
    """
    request = HandoffRequest(
        task_description=task_description,
        work_completed=work_completed,
        pr_title=pr_title,
        pr_description=pr_description,
        generate_snapshot=False,
        generate_handoff_prompt=False,
        generate_pr_description=True,
        generate_release_notes=False,
    )
    return generate_complete_project_outputs(request)


def generate_release_notes_only(
    task_description: str, release_notes: str, work_completed: list = None
) -> dict:
    """
    Generates release notes output for a given task without producing other handoff artifacts.

    Args:
        task_description: Description of the completed task or release.
        release_notes: The release notes content to be included.
        work_completed: Optional list of completed work items to provide context.

    Returns:
        A dictionary containing the processed release notes and related output fields.
    """
    request = HandoffRequest(
        task_description=task_description,
        work_completed=work_completed,
        release_notes=release_notes,
        generate_snapshot=False,
        generate_handoff_prompt=False,
        generate_pr_description=False,
        generate_release_notes=True,
    )
    return generate_complete_project_outputs(request)


def generate_handoff_prompt_only(
    task_description: str,
    work_completed: list = None,
    next_steps: list = None,
    brief_context: str = None,
) -> dict:
    """
    Generates a handoff prompt for agent transition based on the provided task details.

    Args:
        task_description: Description of the current task or work order.
        work_completed: Optional list of completed work items.
        next_steps: Optional list of recommended next steps.
        brief_context: Optional brief context or summary for the handoff.

    Returns:
        A dictionary containing the generated handoff prompt and related output fields.
    """
    request = HandoffRequest(
        task_description=task_description,
        work_completed=work_completed,
        next_steps=next_steps,
        brief_context=brief_context,
        generate_snapshot=False,
        generate_handoff_prompt=True,
        generate_pr_description=False,
        generate_release_notes=False,
    )
    return generate_complete_project_outputs(request)


# Removed redefined functions - use imports from agent_handoffs.py instead


# =============================================================================
# CONVENIENCE FUNCTIONS FOR BACKWARD COMPATIBILITY AND EASY ACCESS
# =============================================================================

def get_timestamp() -> str:
    """Get current timestamp - convenience function for backward compatibility."""
    return get_current_timestamp()

# All other functions are imported from specialized modules to avoid redefinition conflicts
