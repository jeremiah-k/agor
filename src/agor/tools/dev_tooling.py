"""
Development Tooling for AGOR - Quick Commit/Push and Memory Operations

Provides utility functions for frequent commits and cross-branch memory operations
to streamline development workflow and memory management.
"""

import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional

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


class DevTooling:
    """Development utilities for AGOR development workflow."""

    def __init__(self, repo_path: Optional[Path] = None):
        """Initialize development tooling."""
        self.repo_path = repo_path if repo_path else Path.cwd()
        self.git_binary = git_manager.get_git_binary()

    def _run_git_command(self, command: list[str]) -> tuple[bool, str]:
        """
        Run a git command and return success status and output.

        Args:
            command: Git command arguments

        Returns:
            Tuple of (success, output)
        """
        try:
            result = subprocess.run(
                [self.git_binary] + command,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True,
            )
            return True, result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return False, f"Git error: {e.stderr.strip()}"
        except Exception as e:
            return False, f"Error: {str(e)}"

    def get_current_timestamp(self) -> str:
        """Get current UTC timestamp in AGOR format."""
        return datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    def get_timestamp_for_files(self) -> str:
        """Get timestamp suitable for filenames (no spaces or colons)."""
        return datetime.utcnow().strftime("%Y-%m-%d_%H%M")

    def get_precise_timestamp(self) -> str:
        """Get precise timestamp with seconds for detailed logging."""
        return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    def get_ntp_timestamp(self) -> str:
        """Get accurate timestamp from NTP server, fallback to local time."""
        try:
            import json
            import urllib.request

            with urllib.request.urlopen(
                "http://worldtimeapi.org/api/timezone/UTC", timeout=5
            ) as response:
                data = json.loads(response.read().decode())
                # Parse ISO format and convert to our format
                iso_time = data["datetime"][:19]  # Remove timezone info
                dt = datetime.fromisoformat(iso_time)
                return dt.strftime("%Y-%m-%d %H:%M UTC")
        except Exception:
            # Fallback to local time if NTP fails
            return self.get_current_timestamp()

    def quick_commit_push(self, message: str, emoji: str = "🔧") -> bool:
        """
        Commit and push in one operation with timestamp.

        Args:
            message: Commit message
            emoji: Emoji prefix for commit

        Returns:
            True if successful, False otherwise
        """
        timestamp = self.get_current_timestamp()
        full_message = f"{emoji} {message}\n\nTimestamp: {timestamp}"

        print(f"🚀 Quick commit/push: {emoji} {message}")

        # Add all changes
        success, output = self._run_git_command(["add", "."])
        if not success:
            print(f"❌ Failed to add files: {output}")
            return False

        # Commit
        success, output = self._run_git_command(["commit", "-m", full_message])
        if not success:
            if "nothing to commit" in output.lower():
                print("ℹ️  No changes to commit")
                return True
            print(f"❌ Failed to commit: {output}")
            return False

        # Push
        success, output = self._run_git_command(["push"])
        if not success:
            print(f"❌ Failed to push: {output}")
            return False

        print(f"✅ Successfully committed and pushed at {timestamp}")
        return True

    def auto_commit_memory(
        self, content: str, memory_type: str, agent_id: str = "dev"
    ) -> bool:
        """
        Create memory file and commit to memory branch without switching.

        Args:
            content: Memory content to store
            memory_type: Type of memory (context, decision, learning, etc.)
            agent_id: Agent identifier

        Returns:
            True if successful, False otherwise
        """
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        memory_branch = f"agor/mem/{timestamp}"
        memory_file = f".agor/{agent_id}-memory.md"

        print(f"💾 Auto-committing memory: {memory_type} for {agent_id}")

        # Create memory content with timestamp
        memory_content = f"""# {agent_id.title()} Memory Log

## {memory_type.title()} - {self.get_current_timestamp()}

{content}

---
*Auto-generated by AGOR dev tooling*
"""

        # Write memory file
        memory_path = self.repo_path / memory_file
        memory_path.parent.mkdir(parents=True, exist_ok=True)
        memory_path.write_text(memory_content)

        # Try cross-branch commit (advanced Git operations)
        if self._commit_to_memory_branch(
            memory_file, memory_branch, f"Add {memory_type} memory for {agent_id}"
        ):
            print(f"✅ Memory committed to branch {memory_branch}")
            return True
        else:
            # Fallback: regular commit to current branch
            print("⚠️  Cross-branch commit failed, using regular commit")
            return self.quick_commit_push(
                f"Add {memory_type} memory for {agent_id}", "💾"
            )

    def _commit_to_memory_branch(
        self, file_path: str, branch_name: str, commit_message: str
    ) -> bool:
        """
        Attempt to commit file to memory branch without switching branches.

        This uses advanced Git operations to commit to a different branch.

        Args:
            file_path: Path to file to commit
            branch_name: Target memory branch
            commit_message: Commit message

        Returns:
            True if successful, False otherwise
        """
        try:
            # Check if memory branch exists
            success, _ = self._run_git_command(["rev-parse", "--verify", branch_name])
            if not success:
                # Create orphan memory branch
                print(f"📝 Creating new memory branch: {branch_name}")
                success, _ = self._run_git_command(
                    ["checkout", "--orphan", branch_name]
                )
                if not success:
                    return False

                # Clear working directory and create initial commit
                success, _ = self._run_git_command(["rm", "-rf", "."])
                if not success:
                    return False

                success, _ = self._run_git_command(
                    [
                        "commit",
                        "--allow-empty",
                        "-m",
                        f"Initial commit for {branch_name}",
                    ]
                )
                if not success:
                    return False

                # Switch back to original branch
                success, _ = self._run_git_command(["checkout", "-"])
                if not success:
                    return False

            # Advanced Git operations for cross-branch commit
            # 1. Add file to index
            success, _ = self._run_git_command(["add", file_path])
            if not success:
                return False

            # 2. Create blob object
            success, blob_hash = self._run_git_command(["hash-object", "-w", file_path])
            if not success:
                return False

            # 3. Get current tree of memory branch
            success, tree_hash = self._run_git_command(
                ["rev-parse", f"{branch_name}^{{tree}}"]
            )
            if not success:
                return False

            # 4. Update index with new file
            success, _ = self._run_git_command(
                [
                    "update-index",
                    "--add",
                    "--cacheinfo",
                    "100644",
                    blob_hash.strip(),
                    file_path,
                ]
            )
            if not success:
                return False

            # 5. Write new tree
            success, new_tree = self._run_git_command(["write-tree"])
            if not success:
                return False

            # 6. Create commit object
            success, new_commit = self._run_git_command(
                [
                    "commit-tree",
                    new_tree.strip(),
                    "-p",
                    branch_name,
                    "-m",
                    commit_message,
                ]
            )
            if not success:
                return False

            # 7. Update branch reference
            success, _ = self._run_git_command(
                ["update-ref", f"refs/heads/{branch_name}", new_commit.strip()]
            )
            if not success:
                return False

            # 8. Push memory branch
            success, _ = self._run_git_command(["push", "origin", branch_name])
            if not success:
                print("⚠️  Failed to push memory branch, but local commit succeeded")

            return True

        except Exception as e:
            print(f"❌ Cross-branch commit failed: {e}")
            return False

    def create_development_snapshot(self, title: str, context: str) -> bool:
        """
        Create a comprehensive development snapshot.

        Args:
            title: Snapshot title
            context: Development context and progress

        Returns:
            True if successful, False otherwise
        """
        timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H%M")
        snapshot_file = (
            f".agor/snapshots/{timestamp}_{title.lower().replace(' ', '-')}_snapshot.md"
        )

        # Get current git info
        success, current_branch = self._run_git_command(["branch", "--show-current"])
        if not success:
            current_branch = "unknown"

        success, current_commit = self._run_git_command(
            ["rev-parse", "--short", "HEAD"]
        )
        if not success:
            current_commit = "unknown"

        snapshot_content = f"""# 📸 {title} Development Snapshot
**Generated**: {self.get_current_timestamp()}
**Agent**: Augment Agent (Software Engineering)
**Branch**: {current_branch.strip()}
**Commit**: {current_commit.strip()}
**AGOR Version**: 0.3.3 → 0.3.4 development

## 🎯 Development Context

{context}

## 📋 Next Steps
[To be filled by continuing agent]

## 🔄 Git Status
- **Current Branch**: {current_branch.strip()}
- **Last Commit**: {current_commit.strip()}
- **Timestamp**: {self.get_current_timestamp()}

---

## 🎼 **For Continuation Agent**

If you're picking up this work:
1. Review this snapshot and current progress
2. Check git status and recent commits
3. Continue from the next steps outlined above

**Remember**: Use quick_commit_push() for frequent commits during development.
"""

        # Write snapshot file
        snapshot_path = self.repo_path / snapshot_file
        snapshot_path.parent.mkdir(parents=True, exist_ok=True)
        snapshot_path.write_text(snapshot_content)

        # Commit and push snapshot
        return self.quick_commit_push(f"📸 Create development snapshot: {title}", "📸")

    def test_tooling(self) -> bool:
        """Test all development tooling functions to ensure they work properly."""
        print("🧪 Testing AGOR Development Tooling...")

        # Test timestamp functions
        print(f"📅 Current timestamp: {self.get_current_timestamp()}")
        print(f"📁 File timestamp: {self.get_timestamp_for_files()}")
        print(f"⏰ Precise timestamp: {self.get_precise_timestamp()}")
        print(f"🌐 NTP timestamp: {self.get_ntp_timestamp()}")

        # Test git binary access
        try:
            git_path = self.git_binary
            print(f"🔧 Git binary: {git_path}")

            # Test basic git command
            success, output = self._run_git_command(["--version"])
            if success:
                print(f"✅ Git working: {output}")
            else:
                print(f"❌ Git test failed: {output}")
                return False
        except Exception as e:
            print(f"❌ Git binary test failed: {e}")
            return False

        # Test repository status
        success, branch = self._run_git_command(["branch", "--show-current"])
        if success:
            print(f"🌿 Current branch: {branch}")
        else:
            print(f"⚠️  Could not determine branch: {branch}")

        success, status = self._run_git_command(["status", "--porcelain"])
        if success:
            if status.strip():
                print(
                    f"📝 Working directory has changes: {len(status.splitlines())} files"
                )
            else:
                print("✅ Working directory clean")

        print("🎉 Development tooling test completed successfully!")
        return True


# Global instance for easy access
dev_tools = DevTooling()


# Convenience functions
def quick_commit_push(message: str, emoji: str = "🔧") -> bool:
    """Quick commit and push with timestamp."""
    return dev_tools.quick_commit_push(message, emoji)


def auto_commit_memory(content: str, memory_type: str, agent_id: str = "dev") -> bool:
    """Auto-commit memory to memory branch."""
    return dev_tools.auto_commit_memory(content, memory_type, agent_id)


def create_snapshot(title: str, context: str) -> bool:
    """Create development snapshot."""
    return dev_tools.create_development_snapshot(title, context)


def test_tooling() -> bool:
    """Test all development tooling functions."""
    return dev_tools.test_tooling()


# Timestamp utilities
def get_timestamp() -> str:
    """Get current UTC timestamp."""
    return dev_tools.get_current_timestamp()


def get_file_timestamp() -> str:
    """Get timestamp suitable for filenames."""
    return dev_tools.get_timestamp_for_files()


def get_precise_timestamp() -> str:
    """Get precise timestamp with seconds."""
    return dev_tools.get_precise_timestamp()


def get_ntp_timestamp() -> str:
    """Get accurate timestamp from NTP server."""
    return dev_tools.get_ntp_timestamp()


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
        """
        Returns the set of mandatory checklist items for the current agent role.
        
        The checklist includes base items required for all roles, with additional items
        added based on whether the agent is a solo developer, project coordinator, or agent worker.
        """
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
        """
        Checks that git user.name and user.email are configured and verifies the current branch is not 'main' or 'master'.
        
        Returns:
            True if git is properly configured and on a non-main branch; False otherwise.
        """
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
        """
        Checks if at least two commits have been made in the last hour and prints a reminder if not.
        
        Prints a message indicating whether commit frequency is sufficient or suggests more frequent commits. If the check fails, prints a warning.
        """
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
        """
        Returns the current status of the checklist, including completion metrics, incomplete items, snapshot creation state, and session end eligibility.
        
        Returns:
            A dictionary with completion percentage, counts of completed and total items, a list of incomplete items, snapshot creation status, and whether the session can end.
        """
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
        """
        Checks if all mandatory checklist items are complete and enforces session end requirements.
        
        Prints incomplete items and snapshot status if requirements are not met. Returns True if the session can end, otherwise False.
        """
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
    """
    Initializes a new internal agent checklist for the current session based on the specified role.
    
    Args:
        role: The agent role for which to create the checklist (e.g., "solo_developer").
    
    Returns:
        An AgentChecklist instance configured for the given role.
    """
    global _agent_checklist
    _agent_checklist = AgentChecklist(role)
    print(
        f"📋 Internal checklist created for {role} with {len(_agent_checklist.mandatory_items)} items"
    )
    return _agent_checklist


def mark_checklist_complete(item_id: str):
    """
    Marks a checklist item as complete in the current agent checklist.
    
    Args:
        item_id: The identifier of the checklist item to mark as complete.
    """
    if _agent_checklist:
        _agent_checklist.mark_complete(item_id)


def get_checklist_status() -> dict:
    """
    Returns the current status of the global agent checklist.
    
    If no checklist is initialized, returns a dictionary indicating no checklist is present.
    """
    if _agent_checklist:
        return _agent_checklist.get_status()
    return {"status": "no_checklist"}


def enforce_session_end() -> bool:
    """
    Enforces end-of-session procedures using the current agent checklist.
    
    Returns:
        True if all checklist requirements are met and the session can end; otherwise, False.
    """
    if _agent_checklist:
        return _agent_checklist.enforce_session_end()
    return True


# New hotkey processing functions
def process_progress_report_hotkey(
    task_description: str = "", progress: str = "50%"
) -> str:
    """
    Prompts the user for progress report details and creates a progress report snapshot.
    
    Collects information about the current task, progress percentage, completed work, blockers, next steps, estimated completion time, and additional notes via user input. Generates and saves a progress report snapshot file, marks the corresponding checklist item as complete, and returns the file path of the created snapshot.
    """
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
    """
    Prompts the user for work order details and creates a work order snapshot file.
    
    Collects task description, requirements, acceptance criteria, files to modify, and additional metadata from user input. Generates and saves a work order snapshot, marks the corresponding checklist item as complete, and returns the path to the created snapshot file.
    
    Returns:
        The file path of the created work order snapshot.
    """
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
    """
    Handles the create-PR hotkey by collecting pull request details from the user, retrieving recent commits and changed files, generating a PR description snapshot, and marking the relevant checklist item as complete.
    
    Args:
        pr_title: Optional PR title. If not provided, prompts the user for input.
    
    Returns:
        The file path to the generated PR description snapshot.
    """
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
