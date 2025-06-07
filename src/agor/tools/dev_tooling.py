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
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

# Import from specialized modules for modular organization
try:
    from .git_operations import (
        get_current_timestamp as _get_current_timestamp,
        get_file_timestamp as _get_file_timestamp,
        get_precise_timestamp as _get_precise_timestamp,
        get_ntp_timestamp as _get_ntp_timestamp,
        run_git_command as _run_git_command,
        safe_git_push as _safe_git_push,
        quick_commit_push as _quick_commit_push
    )

    from .memory_manager import (
        commit_to_memory_branch as _commit_to_memory_branch,
        auto_commit_memory as _auto_commit_memory
    )

    from .agent_handoffs import (
        detick_content,
        retick_content,
        generate_handoff_prompt_only,
        generate_mandatory_session_end_prompt,
        generate_meta_feedback
    )

    from .dev_testing import (
        test_tooling as _test_tooling,
        detect_environment,
        get_agent_dependency_install_commands,
        generate_dynamic_installation_prompt
    )

    MODULAR_IMPORTS_AVAILABLE = True

except ImportError as e:
    # Fallback for development or when modules aren't available
    print(f"⚠️  Modular imports not available: {e}")
    MODULAR_IMPORTS_AVAILABLE = False

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


class DevTooling:
    """Development utilities for AGOR development workflow."""

    def __init__(self, repo_path: Optional[Path] = None):
        """Initialize development tooling."""
        self.repo_path = repo_path if repo_path else Path.cwd()
        self.git_binary = git_manager.get_git_binary()

    def _run_git_command(
        self, command: list[str], env: Optional[dict[str, str]] = None
    ) -> tuple[bool, str]:
        """
        Run a git command and return success status and output.

        Args:
            command: Git command arguments
            env: Optional environment variables to add

        Returns:
            Tuple of (success, output)
        """
        try:
            # Prepare environment - always copy current env, update if provided
            cmd_env = os.environ.copy()
            if env:
                cmd_env.update(env)

            result = subprocess.run(
                [self.git_binary] + command,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True,
                env=cmd_env,
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

    def safe_git_push(
        self,
        branch_name: Optional[str] = None,
        force: bool = False,
        explicit_force: bool = False
    ) -> bool:
        """
        Safe git push with upstream checking and protected branch validation.

        This function implements safety checks to prevent dangerous git operations:
        - Always pulls before pushing to check for upstream changes
        - Prevents force pushes to protected branches (main, master, develop)
        - Requires explicit confirmation for force pushes
        - Fails safely if upstream changes require merge/rebase

        Args:
            branch_name: Target branch (default: current branch)
            force: Whether to force push (requires explicit_force=True for safety)
            explicit_force: Must be True to enable force push (safety check)

        Returns:
            True if successful, False otherwise
        """
        print("🛡️  Safe git push: performing safety checks...")

        # Get current branch if not specified
        if not branch_name:
            success, current_branch = self._run_git_command(["branch", "--show-current"])
            if not success:
                print("❌ Cannot determine current branch")
                return False
            branch_name = current_branch.strip()

        # Protected branches - never allow force push
        protected_branches = ["main", "master", "develop", "production"]
        if force and branch_name in protected_branches:
            print(f"🚨 SAFETY VIOLATION: Force push to protected branch '{branch_name}' is not allowed")
            print(f"Protected branches: {', '.join(protected_branches)}")
            return False

        # Force push safety check
        if force and not explicit_force:
            print("🚨 SAFETY VIOLATION: Force push requires explicit_force=True")
            print("This prevents accidental force pushes that could lose work")
            return False

        # Step 1: Fetch to check for upstream changes
        print("📡 Fetching from remote to check for upstream changes...")
        success, output = self._run_git_command(["fetch", "origin", branch_name])
        if not success:
            print(f"⚠️  Failed to fetch from remote: {output}")
            print("Proceeding with push (remote may not exist yet)")

        # Step 2: Check if upstream has changes we don't have
        success, local_commit = self._run_git_command(["rev-parse", "HEAD"])
        if not success:
            print("❌ Cannot get local commit hash")
            return False
        local_commit = local_commit.strip()

        success, remote_commit = self._run_git_command(["rev-parse", f"origin/{branch_name}"])
        if success:
            remote_commit = remote_commit.strip()
            if local_commit != remote_commit and not force:
                # Check if we're behind
                success, merge_base = self._run_git_command(["merge-base", "HEAD", f"origin/{branch_name}"])
                if success and merge_base.strip() == local_commit:
                    print("🚨 UPSTREAM CHANGES DETECTED: Remote has commits we don't have")
                    print("You need to pull and merge/rebase before pushing")
                    print("Run: git pull origin {branch_name}")
                    return False

        # Step 3: Perform the push
        push_command = ["push", "origin", branch_name]
        if force:
            push_command.append("--force")
            print(f"⚠️  FORCE PUSHING to {branch_name} (explicit_force=True)")
        else:
            print(f"✅ Safe pushing to {branch_name}")

        success, output = self._run_git_command(push_command)
        if not success:
            print(f"❌ Push failed: {output}")
            return False

        print(f"✅ Successfully pushed to {branch_name}")
        return True

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

        # Safe push
        if not self.safe_git_push():
            print("❌ Safe push failed")
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
        SAFE memory branch commit using git plumbing - NEVER switches branches.

        Uses low-level git commands to commit files to memory branch without
        changing the current working branch or working directory.

        Args:
            file_path: Path to file to commit (relative to repo root)
            branch_name: Target memory branch
            commit_message: Commit message

        Returns:
            True if successful, False otherwise (fallback to regular commit)
        """
        try:
            # SAFETY CHECK: Never switch branches in memory operations
            success, current_branch = self._run_git_command(
                ["branch", "--show-current"]
            )
            if not success:
                print(
                    "⚠️  Cannot determine current branch - aborting memory commit for safety"
                )
                return False

            original_branch = current_branch.strip()
            print(f"🛡️  Safe memory commit: staying on {original_branch}")

            # Check if file exists
            full_file_path = self.repo_path / file_path
            if not full_file_path.exists():
                print(f"❌ File does not exist: {file_path}")
                return False

            # Step 1: Create blob object for the file
            success, blob_hash = self._run_git_command(
                ["hash-object", "-w", str(full_file_path)]
            )
            if not success:
                print("❌ Failed to create blob object")
                return False
            blob_hash = blob_hash.strip()

            # Step 2: Check if memory branch exists
            success, _ = self._run_git_command(
                ["rev-parse", "--verify", f"refs/heads/{branch_name}"]
            )
            branch_exists = success

            if not branch_exists:
                # Create new memory branch 1 commit behind HEAD (not orphan)
                print(f"📝 Creating new memory branch: {branch_name}")

                # Get HEAD commit to create branch 1 commit behind
                success, head_commit = self._run_git_command(["rev-parse", "HEAD"])
                if not success:
                    print("❌ Failed to get HEAD commit")
                    return False
                head_commit = head_commit.strip()

                # Get parent of HEAD (1 commit behind)
                success, parent_commit = self._run_git_command(["rev-parse", "HEAD~1"])
                if not success:
                    # If no parent (first commit), use HEAD itself
                    print("⚠️  No parent commit found, using HEAD as base")
                    parent_commit = head_commit
                else:
                    parent_commit = parent_commit.strip()

                # Create branch reference pointing to parent commit
                success, _ = self._run_git_command(
                    ["update-ref", f"refs/heads/{branch_name}", parent_commit]
                )
                if not success:
                    print("❌ Failed to create branch reference")
                    return False

                print(f"✅ Created memory branch {branch_name} (1 commit behind HEAD: {parent_commit[:8]})")

            # Step 3: Get current commit of memory branch
            success, parent_commit = self._run_git_command(
                ["rev-parse", f"refs/heads/{branch_name}"]
            )
            if not success:
                print("❌ Failed to get parent commit")
                return False
            parent_commit = parent_commit.strip()

            # Step 4: Create tree with the new file
            # Use git update-index to stage the file in a temporary index
            temp_index = None
            try:
                # Create unique temporary index file to avoid collisions
                temp_fd, temp_index_path = tempfile.mkstemp(
                    prefix="agor_memory_index_",
                    suffix=".tmp",
                    dir=self.repo_path / ".git",
                )
                os.close(temp_fd)  # Close file descriptor, we only need the path
                temp_index = Path(temp_index_path)

                # Read current tree into temporary index
                success, _ = self._run_git_command(
                    ["read-tree", f"{branch_name}^{{tree}}"],
                    env={"GIT_INDEX_FILE": str(temp_index)},
                )
                if not success:
                    print("❌ Failed to read current tree")
                    return False

                # Add our file to the temporary index
                success, _ = self._run_git_command(
                    [
                        "update-index",
                        "--add",
                        "--cacheinfo",
                        "100644",
                        blob_hash,
                        file_path,
                    ],
                    env={"GIT_INDEX_FILE": str(temp_index)},
                )
                if not success:
                    print("❌ Failed to update index")
                    return False

                # Write tree from temporary index
                success, new_tree = self._run_git_command(
                    ["write-tree"], env={"GIT_INDEX_FILE": str(temp_index)}
                )
                if not success:
                    print("❌ Failed to write tree")
                    return False
                new_tree = new_tree.strip()

            finally:
                # Ensure cleanup of temporary index file
                if temp_index and temp_index.exists():
                    try:
                        temp_index.unlink()
                    except Exception as e:
                        print(f"⚠️  Failed to cleanup temporary index: {e}")

            # Step 5: Create commit object
            success, new_commit = self._run_git_command(
                ["commit-tree", new_tree, "-p", parent_commit, "-m", commit_message]
            )
            if not success:
                print("❌ Failed to create commit")
                return False
            new_commit = new_commit.strip()

            # Step 6: Update branch reference
            success, _ = self._run_git_command(
                ["update-ref", f"refs/heads/{branch_name}", new_commit]
            )
            if not success:
                print("❌ Failed to update branch reference")
                return False

            # Step 7: Push memory branch (optional, don't fail if this doesn't work)
            # Use safe push for memory branches too, but don't fail the whole operation
            if not self.safe_git_push(branch_name=branch_name):
                print(
                    f"⚠️  Failed to push memory branch {branch_name} (local commit succeeded)"
                )

            print(
                f"✅ Successfully committed {file_path} to memory branch {branch_name}"
            )
            return True

        except Exception as e:
            print(f"❌ Memory branch commit failed: {e}")
            return False

    def _read_from_memory_branch(
        self, file_path: str, branch_name: str
    ) -> Optional[str]:
        """
        SAFE memory branch read - NEVER switches branches.

        Reads file content from memory branch without changing current working branch.

        Args:
            file_path: Path to file to read (relative to repo root)
            branch_name: Source memory branch

        Returns:
            File content as string if successful, None otherwise
        """
        try:
            # SAFETY CHECK: Verify we're not switching branches
            success, current_branch = self._run_git_command(
                ["branch", "--show-current"]
            )
            if not success:
                print(
                    "⚠️  Cannot determine current branch - aborting memory read for safety"
                )
                return None

            original_branch = current_branch.strip()

            # Check if memory branch exists
            success, _ = self._run_git_command(
                ["rev-parse", "--verify", f"refs/heads/{branch_name}"]
            )
            if not success:
                print(f"⚠️  Memory branch {branch_name} does not exist")
                return None

            # Read file from memory branch using git show
            success, content = self._run_git_command(
                ["show", f"{branch_name}:{file_path}"]
            )
            if not success:
                print(f"⚠️  File {file_path} not found in memory branch {branch_name}")
                return None

            # Verify we're still on the original branch
            success, check_branch = self._run_git_command(["branch", "--show-current"])
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

    def list_memory_branches(self) -> list[str]:
        """
        List all memory branches without switching branches.

        Uses the existing memory_sync.py implementation to avoid code duplication.

        Returns:
            List of memory branch names
        """
        try:
            from agor.memory_sync import MemorySync

            # Create MemorySync instance with current repo path
            memory_sync = MemorySync(repo_path=str(self.repo_path))

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
                success, branches_output = self._run_git_command(["branch", "-a"])
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
**AGOR Version**: 0.4.1 development

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

    def prepare_prompt_content(self, content: str) -> str:
        """
        Escapes nested codeblocks in content for safe inclusion within a single codeblock prompt.

        Replaces triple backticks with double backticks to prevent formatting issues when embedding code examples inside a single codeblock, ensuring agent transition prompts render correctly.

        Args:
            content: The input string potentially containing codeblocks.

        Returns:
            The content with codeblocks escaped for single codeblock usage.
        """
        # Replace triple backticks with double backticks to prevent codeblock nesting issues
        escaped_content = content.replace("```", "``")

        # Also handle any quadruple backticks that might exist (from previous escaping)
        escaped_content = escaped_content.replace("````", "```")

        return escaped_content

    def detick_content(self, content: str) -> str:
        """
        Converts all triple backticks in the content to double backticks for safe embedding within a single codeblock.

        Args:
            content: The text in which to replace triple backticks.

        Returns:
            The content with all triple backticks replaced by double backticks.
        """
        return self.prepare_prompt_content(content)

    def retick_content(self, content: str) -> str:
        """
        Converts isolated double backticks in the content back to triple backticks.

        This reverses the detick operation, restoring standard Markdown code block formatting while avoiding unintended replacements in sequences of multiple backticks.

        Args:
            content: The string in which to restore triple backticks.

        Returns:
            The content with isolated double backticks replaced by triple backticks.
        """
        import re

        # Convert double backticks back to triple backticks (retick)
        # Use regex with negative lookbehind/lookahead to match only isolated double backticks
        processed = re.sub(r"(?<!`)``(?!`)", "```", content)
        return processed

    def generate_agent_handoff_prompt(
        self,
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

        timestamp = self.get_current_timestamp()

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
        processed_prompt = self.prepare_prompt_content(prompt)

        return processed_prompt

    def generate_processed_output(
        self, content: str, output_type: str = "general"
    ) -> str:
        """
        Processes content for safe inclusion within a single codeblock, adding a descriptive header.

        Converts triple backticks to double backticks to prevent formatting issues when embedding codeblocks, and prepends a header indicating the output type.

        Args:
            content: The content to process, which may include triple backticks.
            output_type: A label describing the type of output (e.g., "snapshot", "pr_description", "prompt").

        Returns:
            The processed content with backticks converted and a header added for single codeblock usage.
        """
        # Apply backtick processing
        processed_content = self.prepare_prompt_content(content)

        # Add header comment for clarity
        header = f"# Processed {output_type.replace('_', ' ').title()} - Ready for Single Codeblock Usage\n\n"

        return header + processed_content

    def generate_complete_project_outputs(self, request: HandoffRequest) -> dict:
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
            if request.generate_snapshot or request.generate_handoff_prompt:
                handoff_outputs = generate_final_handoff_outputs(
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
                processed_pr = self.generate_processed_output(
                    request.pr_description, "pr_description"
                )
                outputs["pr_description"] = processed_pr

            # Generate release notes if requested and provided
            if request.generate_release_notes and request.release_notes:
                processed_release_notes = self.generate_processed_output(
                    request.release_notes, "release_notes"
                )
                outputs["release_notes"] = processed_release_notes

            # Add convenience method for displaying selected outputs
            outputs["display_all"] = self._format_all_outputs_display(outputs)

            return outputs

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to generate selected project outputs: {e}",
            }

    def _format_all_outputs_display(self, outputs: dict) -> str:
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


def prepare_prompt_content(content: str) -> str:
    """
    Escapes nested codeblocks in the given content to ensure safe inclusion within a single codeblock prompt.

    Replaces triple backticks with double backticks to prevent formatting issues when embedding code within codeblocks.
    """
    return dev_tools.prepare_prompt_content(content)


def detick_content(content: str) -> str:
    """
    Replaces all triple backticks in the content with double backticks for safe embedding within a single codeblock.
    """
    return dev_tools.detick_content(content)


def retick_content(content: str) -> str:
    """
    Converts double backticks (``) in the content back to triple backticks (```) for standard codeblock formatting.

    Args:
        content: The string content with double backticks to be converted.

    Returns:
        The content with double backticks replaced by triple backticks.
    """
    return dev_tools.retick_content(content)


def generate_agent_handoff_prompt(
    task_description: str,
    snapshot_content: str = None,
    memory_branch: str = None,
    environment: dict = None,
    brief_context: str = None,
) -> str:
    """
    Generates a formatted agent handoff prompt for seamless transfer between agents.

    The prompt includes task description, optional snapshot content, memory branch details, environment information, and brief context. Triple backticks in the content are automatically converted to double backticks to ensure safe embedding within single codeblocks.

    Args:
        task_description: Description of the current task or work order.
        snapshot_content: Optional snapshot or summary of the current project state.
        memory_branch: Optional name of the memory branch containing relevant files.
        environment: Optional dictionary with environment details (e.g., platform, versions).
        brief_context: Optional concise context or summary for the next agent.

    Returns:
        A processed string containing the complete handoff prompt, ready for agent consumption.
    """
    return dev_tools.generate_agent_handoff_prompt(
        task_description, snapshot_content, memory_branch, environment, brief_context
    )


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
    from agor.tools.snapshot_templates import generate_snapshot_document

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

        timestamp = dev_tools.get_timestamp_for_files()
        snapshot_file = snapshot_dir / f"{timestamp}_handoff_snapshot.md"
        snapshot_file.write_text(snapshot_content)

        # Use safe cross-branch commit that NEVER switches branches
        relative_path = f".agor/snapshots/{timestamp}_handoff_snapshot.md"
        commit_message = f"📸 Agent handoff snapshot: {task_description[:50]}"

        if dev_tools._commit_to_memory_branch(
            relative_path, memory_branch, commit_message
        ):
            print(f"✅ Snapshot safely committed to memory branch: {memory_branch}")
        else:
            print("⚠️ Cross-branch commit failed, using regular commit as fallback")
            dev_tools.quick_commit_push(commit_message, "📸")
            memory_branch = None

    except Exception as e:
        memory_branch = None
        print(f"⚠️ Memory sync not available: {e}, proceeding without memory branch")

        # Fallback: regular commit to current branch
        try:
            dev_tools.quick_commit_push(
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
    handoff_prompt = dev_tools.generate_agent_handoff_prompt(
        task_description=task_description,
        snapshot_content=snapshot_content,
        memory_branch=memory_branch,
        brief_context=brief_context,
    )

    return snapshot_content, handoff_prompt


def detect_environment() -> dict:
    """
    Detects the current AGOR environment and returns configuration details.

    Returns:
        A dictionary with keys for environment mode, platform, git and pyenv availability, AGOR version, and Python version.
    """
    environment = {
        "mode": "unknown",
        "platform": "unknown",
        "has_git": False,
        "has_pyenv": False,
        "agor_version": "unknown",
        "python_version": "unknown",
    }

    # Detect Python version
    import sys

    environment["python_version"] = (
        f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    )

    # Detect AGOR version
    try:
        from agor import __version__

        environment["agor_version"] = __version__
    except ImportError:
        environment["agor_version"] = "development"

    # Check for git
    import shutil

    if shutil.which("git"):
        environment["has_git"] = True

    # Check for .pyenv directory
    if Path(".pyenv").exists():
        environment["has_pyenv"] = True

    # Detect environment mode - check env vars first to avoid misclassification in containers
    if "AUGMENTCODE_LOCAL" in os.environ:
        environment["mode"] = "augmentcode_local"
        environment["platform"] = "augmentcode_local_agent"
    elif "AUGMENTCODE_REMOTE" in os.environ:
        environment["mode"] = "augmentcode_remote"
        environment["platform"] = "augmentcode_remote_agent"
    elif Path("src/agor/tools").exists():
        environment["mode"] = "development"
        environment["platform"] = "local_development"
    elif Path("/tmp/agor").exists():
        environment["mode"] = "standalone"
        environment["platform"] = "remote_agent"
    else:
        environment["mode"] = "bundle"
        environment["platform"] = "upload_based"

    return environment


def get_agent_dependency_install_commands() -> str:
    """
    Returns shell commands for installing agent development tooling dependencies, with automatic fallback to a `.pyenv` virtual environment if standard installation fails.
    """
    return """# Install ONLY the dependencies needed for agent dev tooling (NOT requirements.txt)
python3 -m pip install -r src/agor/tools/agent-requirements.txt || {
    echo "⚠️ pip install failed, trying .pyenv venv fallback"
    if [ -d ".pyenv" ]; then
        source .pyenv/bin/activate
        python3 -m pip install -r src/agor/tools/agent-requirements.txt
    else
        echo "❌ No .pyenv directory found, creating virtual environment"
        python3 -m venv .pyenv
        source .pyenv/bin/activate
        python3 -m pip install -r src/agor/tools/agent-requirements.txt
    fi
}"""


def generate_dynamic_installation_prompt(environment: dict = None) -> str:
    """
    Generates installation instructions tailored to the detected AGOR environment.

    If no environment dictionary is provided, the function detects the current environment and produces a Markdown-formatted setup guide. The instructions include environment details, mode-specific installation steps, and troubleshooting tips for common issues.

    Args:
        environment: Optional dictionary describing the current environment. If not provided, the environment is auto-detected.

    Returns:
        A Markdown string containing environment-specific installation and troubleshooting instructions.
    """
    if environment is None:
        environment = detect_environment()

    base_instructions = """# 🛠️ Environment-Specific AGOR Setup

## Detected Environment
"""

    # Add environment details
    base_instructions += f"""- **Mode**: {environment['mode']}
- **Platform**: {environment['platform']}
- **AGOR Version**: {environment['agor_version']}
- **Python Version**: {environment['python_version']}
- **Git Available**: {'✅' if environment['has_git'] else '❌'}
- **Virtual Environment**: {'✅ .pyenv found' if environment['has_pyenv'] else '❌ No .pyenv'}

## Installation Instructions

"""

    # Add mode-specific instructions
    if environment["mode"] == "development":
        dev_install_commands = get_agent_dependency_install_commands()
        base_instructions += f"""### Development Mode Setup
```bash
# Install development dependencies
python3 -m pip install -r requirements.txt

{dev_install_commands}

# Test development tooling
python3 -c "
import sys
sys.path.insert(0, 'src')
from agor.tools.dev_tooling import test_tooling
test_tooling()
"
```
"""
    elif environment["mode"] == "augmentcode_local":
        local_install_commands = get_agent_dependency_install_commands()
        base_instructions += f"""### AugmentCode Local Agent Setup
```bash
# Dependencies should be automatically available
# Verify memory manager dependencies
python3 -c "import pydantic, pydantic_settings; print('✅ Dependencies OK')"

# If missing, install with fallback
{local_install_commands}
```
"""
    elif environment["mode"] == "standalone":
        standalone_install_commands = get_agent_dependency_install_commands()
        base_instructions += f"""### Standalone Mode Setup
```bash
# Install dependencies from requirements.txt
python3 -m pip install -r requirements.txt

{standalone_install_commands}

# Test AGOR tooling
python3 -c "
import sys
sys.path.insert(0, 'src')
from agor.tools.dev_tooling import test_tooling
test_tooling()
"
```
"""
    else:
        base_instructions += """### Standard Setup
```bash
# Install AGOR if not already installed
pipx install agor

# Verify installation
agor --version
```
"""

    # Add troubleshooting section
    base_instructions += """
## Troubleshooting

### Memory Manager Issues
If you encounter pydantic type errors:
```bash
pip install pydantic pydantic-settings --upgrade
```

### Git Issues
If git commands fail:
```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

---
*Generated dynamically based on environment detection*
"""

    return base_instructions


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
    if environment is None:
        environment = detect_environment()

    timestamp = dev_tools.get_current_timestamp()

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
    timestamp = dev_tools.get_precise_timestamp()
    log_entry = f"{agent_id}: {timestamp} - {message}\n"

    if not memory_branch:
        memory_branch = f"agor/mem/{dev_tools.get_timestamp_for_files()}"

    print(f"📝 Logging to agentconvo.md: {agent_id} - {message}")

    # Create agentconvo.md content
    agentconvo_content = f"""# Agent Communication Log

Format: [AGENT-ID] [TIMESTAMP] - [STATUS/QUESTION/FINDING]

## Communication History

{log_entry}
"""

    # Write agentconvo.md file to current working directory
    agentconvo_path = dev_tools.repo_path / ".agor" / "agentconvo.md"
    agentconvo_path.parent.mkdir(parents=True, exist_ok=True)

    # Append to existing file or create new one
    if agentconvo_path.exists():
        with open(agentconvo_path, "a") as f:
            f.write(log_entry)
    else:
        agentconvo_path.write_text(agentconvo_content)

    # Try to commit to memory branch using new safe system
    if dev_tools._commit_to_memory_branch(
        ".agor/agentconvo.md",
        memory_branch,
        f"Update agentconvo.md: {agent_id} - {message}",
    ):
        print(f"✅ Agentconvo logged to memory branch {memory_branch}")
        return True
    else:
        # Fallback: regular commit to current branch
        print("⚠️  Memory branch commit failed, using regular commit")
        return dev_tools.quick_commit_push(
            f"Update agentconvo.md: {agent_id} - {message}", "💬"
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
    memory_file = f".agor/{agent_id.lower()}-memory.md"
    timestamp = dev_tools.get_current_timestamp()

    if not memory_branch:
        memory_branch = f"agor/mem/{dev_tools.get_timestamp_for_files()}"

    print(f"🧠 Updating {agent_id} memory: {memory_type}")

    # Create or update memory content
    memory_entry = f"""
## {memory_type.title()} - {timestamp}

{content}

---
"""

    # Write memory file to current working directory
    memory_path = dev_tools.repo_path / memory_file
    memory_path.parent.mkdir(parents=True, exist_ok=True)

    # Append to existing file or create new one
    if memory_path.exists():
        with open(memory_path, "a") as f:
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
        memory_path.write_text(initial_content)

    # Try to commit to memory branch using new safe system
    if dev_tools._commit_to_memory_branch(
        memory_file, memory_branch, f"Update {agent_id} memory: {memory_type}"
    ):
        print(f"✅ Agent memory logged to memory branch {memory_branch}")
        return True
    else:
        # Fallback: regular commit to current branch
        print("⚠️  Memory branch commit failed, using regular commit")
        return dev_tools.quick_commit_push(
            f"Update {agent_id} memory: {memory_type}", "🧠"
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
    return dev_tools.generate_processed_output(content, output_type)


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

    Processes outputs for safe embedding in single codeblocks, based on the configuration provided in the HandoffRequest. No temporary files are created on disk.

    Args:
        request: Contains configuration and flags indicating which outputs to generate.

    Returns:
        A dictionary with the requested outputs, each processed for single codeblock usage.
    """
    return dev_tools.generate_complete_project_outputs(request)


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


def generate_meta_feedback(
    current_project: str = None,
    agor_issues_encountered: list = None,
    suggested_improvements: list = None,
    workflow_friction_points: list = None,
    positive_experiences: list = None
) -> dict:
    """
    Generate AGOR meta feedback for continuous improvement.

    This function creates feedback about AGOR itself while working on other projects.
    The output includes a link to submit feedback to the AGOR meta repository.

    Args:
        current_project: Name/description of the project you're working on
        agor_issues_encountered: List of issues or problems with AGOR
        suggested_improvements: List of suggestions for improving AGOR
        workflow_friction_points: List of workflow friction points
        positive_experiences: List of positive experiences with AGOR

    Returns:
        Dictionary with processed meta feedback ready for single codeblock usage
    """
    try:
        from datetime import datetime

        # Prepare meta feedback content
        feedback_content = f"""# 🔄 AGOR Meta Feedback

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}
**Current Project**: {current_project or 'Not specified'}
**Feedback Type**: User Experience & Improvement Suggestions

## 📋 AGOR Usage Context

**Project Being Worked On**: {current_project or 'Not specified'}
**AGOR Version**: 0.4.2+
**Usage Pattern**: {detect_environment()['mode']}

## 🎯 Issues Encountered

{_format_feedback_list(agor_issues_encountered, 'No issues reported')}

## 💡 Suggested Improvements

{_format_feedback_list(suggested_improvements, 'No suggestions provided')}

## 🚧 Workflow Friction Points

{_format_feedback_list(workflow_friction_points, 'No friction points identified')}

## ✅ Positive Experiences

{_format_feedback_list(positive_experiences, 'No positive experiences noted')}

## 🔗 Submit This Feedback

**To submit this feedback for AGOR improvement:**

1. **Copy this entire feedback** (it's already processed for single codeblock usage)
2. **Visit**: https://github.com/jeremiah-k/agor-meta/issues/new
3. **Paste the feedback** as the issue description
4. **Add a descriptive title** like "AGOR Feedback: [Brief Description]"
5. **Submit the issue** to help improve AGOR for everyone

## 🎯 How This Helps

Your feedback helps improve AGOR by:
- Identifying real-world usage patterns and friction points
- Gathering suggestions from actual users working on diverse projects
- Building a knowledge base of common issues and solutions
- Prioritizing development efforts based on user needs
- Creating a community-driven improvement process

**Thank you for helping make AGOR better!** 🚀

---
*This meta feedback was generated automatically using AGOR's dev tooling*
*Generated while working on: {current_project or 'unspecified project'}*
"""

        # Process the content for single codeblock usage
        processed_content = prepare_prompt_content(feedback_content)

        return {
            'success': True,
            'meta_feedback': processed_content,
            'github_url': 'https://github.com/jeremiah-k/agor-meta/issues/new',
            'instructions': 'Copy the meta_feedback content and paste it at the GitHub URL to submit feedback'
        }

    except Exception as e:
        return {
            'success': False,
            'error': f'Failed to generate meta feedback: {str(e)}'
        }


def _format_feedback_list(items: list, default_message: str) -> str:
    """Format a list of feedback items."""
    if not items:
        return f"- {default_message}"

    return '\n'.join(f"- {item}" for item in items)


def generate_mandatory_session_end_prompt(
    work_completed: list,
    current_status: str,
    next_agent_instructions: list = None,
    critical_context: str = None,
    files_modified: list = None
) -> dict:
    """
    Generate mandatory session end prompt for agent coordination.

    This function MUST be called before ending any agent session to ensure
    proper coordination and context preservation for the next agent or session.

    Args:
        work_completed: List of work items completed in this session
        current_status: Current status of the project/task
        next_agent_instructions: Specific instructions for the next agent
        critical_context: Critical context that must be preserved
        files_modified: List of files that were modified

    Returns:
        Dictionary with processed session end prompt ready for coordination
    """
    try:
        from datetime import datetime

        # Prepare session end content
        session_end_content = f"""# 🔄 MANDATORY SESSION END - Agent Coordination Required

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}
**Session Type**: Agent Handoff Required
**AGOR Version**: 0.4.2+

## 📋 WORK COMPLETED THIS SESSION

{_format_feedback_list(work_completed, 'No work completed')}

## 📊 CURRENT PROJECT STATUS

**Status**: {current_status or 'Status not provided'}

## 📁 FILES MODIFIED

{_format_feedback_list(files_modified, 'No files modified')}

## 🎯 INSTRUCTIONS FOR NEXT AGENT/SESSION

{_format_feedback_list(next_agent_instructions, 'No specific instructions provided')}

## 🧠 CRITICAL CONTEXT TO PRESERVE

{critical_context or 'No critical context provided'}

## 🔧 ENVIRONMENT SETUP FOR CONTINUATION

# Pull latest changes
git pull origin work-0.4.3-2

# Install dependencies
python3 -m pip install -r src/agor/tools/agent-requirements.txt

# Read updated documentation
- src/agor/tools/README_ai.md (2-role system)
- src/agor/tools/AGOR_INSTRUCTIONS.md (meta mode hotkey)

## ⚠️ CRITICAL REQUIREMENTS FOR NEXT SESSION

1. **Review this session's work** - Understand what was completed
2. **Continue from current status** - Don't restart or duplicate work
3. **Use our dev tooling** - All coordination must use our backtick processing
4. **Create return prompts** - Every session must end with coordination output
5. **Focus on productivity** - Substantial progress, not just note-passing

## 🚀 IMMEDIATE NEXT STEPS

1. Review completed work and current status
2. Continue development from where this session left off
3. Make substantial progress on remaining tasks
4. Generate return prompt using our dev tooling before ending

## 📞 COORDINATION PROTOCOL

**When you complete your work, you MUST run:**

``python
python3 -c "
import sys
sys.path.insert(0, 'src')
from agor.tools.dev_tooling import generate_mandatory_session_end_prompt

outputs = generate_mandatory_session_end_prompt(
    work_completed=['List what you completed'],
    current_status='Current project status',
    next_agent_instructions=['Instructions for next agent'],
    critical_context='Important context to preserve',
    files_modified=['Files you modified']
)
print(outputs['session_end_prompt'])
"
``

**This ensures continuous productivity and proper coordination!**

---

*This session end prompt was generated automatically to ensure coordination*
*Next agent: Continue productive work and generate your own session end prompt*
"""

        # Process the content for single codeblock usage
        processed_content = prepare_prompt_content(session_end_content)

        return {
            'success': True,
            'session_end_prompt': processed_content,
            'instructions': 'Copy the session_end_prompt content for agent coordination'
        }

    except Exception as e:
        return {
            'success': False,
            'error': f'Failed to generate session end prompt: {str(e)}'
        }


# =============================================================================
# CONVENIENCE FUNCTIONS FOR BACKWARD COMPATIBILITY AND EASY ACCESS
# =============================================================================

def get_timestamp() -> str:
    """Get current timestamp - convenience function for backward compatibility."""
    if MODULAR_IMPORTS_AVAILABLE:
        return _get_current_timestamp()
    else:
        return datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")


def get_current_timestamp() -> str:
    """Get current timestamp - convenience function for backward compatibility."""
    return get_timestamp()


def get_file_timestamp() -> str:
    """Get file-safe timestamp - convenience function for backward compatibility."""
    if MODULAR_IMPORTS_AVAILABLE:
        return _get_file_timestamp()
    else:
        return datetime.utcnow().strftime("%Y-%m-%d_%H%M")


def get_precise_timestamp() -> str:
    """Get precise timestamp - convenience function for backward compatibility."""
    if MODULAR_IMPORTS_AVAILABLE:
        return _get_precise_timestamp()
    else:
        return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")


def get_ntp_timestamp() -> str:
    """Get NTP timestamp - convenience function for backward compatibility."""
    if MODULAR_IMPORTS_AVAILABLE:
        return _get_ntp_timestamp()
    else:
        return get_timestamp()


def quick_commit_push(message: str, emoji: str = "🔧") -> bool:
    """Quick commit and push - convenience function for backward compatibility."""
    if MODULAR_IMPORTS_AVAILABLE:
        return _quick_commit_push(message, emoji)
    else:
        # Fallback implementation
        dev_tools = DevTooling()
        return dev_tools.quick_commit_push(message, emoji)


def auto_commit_memory(content: str, memory_type: str, agent_id: str = "dev") -> bool:
    """Auto-commit memory - convenience function for backward compatibility."""
    if MODULAR_IMPORTS_AVAILABLE:
        return _auto_commit_memory(content, memory_type, agent_id)
    else:
        # Fallback implementation
        dev_tools = DevTooling()
        return dev_tools.auto_commit_memory(content, memory_type, agent_id)


def test_tooling() -> bool:
    """Test development tooling - convenience function for backward compatibility."""
    if MODULAR_IMPORTS_AVAILABLE:
        return _test_tooling()
    else:
        # Fallback implementation
        print("🧪 Testing AGOR Development Tooling...")
        try:
            dev_tools = DevTooling()
            timestamp = dev_tools.get_current_timestamp()
            print(f"📅 Current timestamp: {timestamp}")

            success, output = dev_tools._run_git_command(["--version"])
            if success:
                print(f"✅ Git working: {output}")
            else:
                print(f"❌ Git issue: {output}")
                return False

            print("🎉 Development tooling test completed successfully!")
            return True
        except Exception as e:
            print(f"❌ Development tooling test failed: {e}")
            return False


# Global instance for convenience
_dev_tools_instance = None


def get_dev_tools() -> 'DevTooling':
    """Get global DevTooling instance - convenience function."""
    global _dev_tools_instance
    if _dev_tools_instance is None:
        _dev_tools_instance = DevTooling()
    return _dev_tools_instance
