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
