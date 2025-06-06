"""
Development Tooling for AGOR - Quick Commit/Push and Memory Operations

Provides utility functions for frequent commits and cross-branch memory operations
to streamline development workflow and memory management.
"""

import os
import subprocess
import tempfile
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
                # Create new memory branch without switching
                print(f"📝 Creating new memory branch: {branch_name}")

                # Create empty tree using cross-platform method
                # Create a temporary empty file for cross-platform compatibility
                temp_empty_file = None
                try:
                    temp_fd, temp_empty_path = tempfile.mkstemp(
                        prefix="agor_empty_", suffix=".tmp"
                    )
                    os.close(temp_fd)  # Close immediately, we just need an empty file
                    temp_empty_file = Path(temp_empty_path)

                    success, empty_tree = self._run_git_command(
                        ["hash-object", "-t", "tree", str(temp_empty_file)]
                    )
                    if not success:
                        # Alternative method for empty tree
                        success, empty_tree = self._run_git_command(["write-tree"])
                        if not success:
                            print("❌ Failed to create empty tree")
                            return False
                finally:
                    # Clean up temporary file
                    if temp_empty_file and temp_empty_file.exists():
                        try:
                            temp_empty_file.unlink()
                        except Exception as e:
                            print(f"⚠️  Failed to cleanup temporary empty file: {e}")
                empty_tree = empty_tree.strip()

                # Create initial commit
                success, initial_commit = self._run_git_command(
                    [
                        "commit-tree",
                        empty_tree,
                        "-m",
                        f"Initial commit for memory branch {branch_name}",
                    ]
                )
                if not success:
                    print("❌ Failed to create initial commit")
                    return False
                initial_commit = initial_commit.strip()

                # Create branch reference
                success, _ = self._run_git_command(
                    ["update-ref", f"refs/heads/{branch_name}", initial_commit]
                )
                if not success:
                    print("❌ Failed to create branch reference")
                    return False

                print(f"✅ Created memory branch {branch_name}")

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
            success, _ = self._run_git_command(["push", "origin", branch_name])
            if not success:
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
        Prepare content for use in single codeblock prompts by escaping nested codeblocks.

        This function reduces triple backticks (```) to double backticks (``) to prevent
        formatting issues when the content is placed inside a single codeblock for agent transitions.

        When agents create snapshots for transitions, the content often contains code examples
        with triple backticks. If this content is then placed inside a single codeblock
        (as required for agent initialization prompts), the nested triple backticks break
        the formatting and create visual garbage in the UI.

        Args:
            content: Raw content that may contain codeblocks

        Returns:
            Content with escaped codeblocks safe for single codeblock usage
        """
        # Replace triple backticks with double backticks to prevent codeblock nesting issues
        escaped_content = content.replace("```", "``")

        # Also handle any quadruple backticks that might exist (from previous escaping)
        escaped_content = escaped_content.replace("````", "```")

        return escaped_content


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
    """Prepare content for single codeblock prompts by escaping nested codeblocks."""
    return dev_tools.prepare_prompt_content(content)


def detect_environment() -> dict:
    """
    Detects the current AGOR environment and returns a dictionary of configuration details.
    
    Returns:
        A dictionary containing environment mode, platform, git and pyenv availability, AGOR version, and Python version.
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
    """Get standardized agent dependency installation commands with fallback."""
    return """# Install ONLY the dependencies needed for agent dev tooling (NOT requirements.txt)
python3 -m pip install pydantic pydantic-settings || {
    echo "⚠️ pip install failed, trying .pyenv venv fallback"
    if [ -d ".pyenv" ]; then
        source .pyenv/bin/activate
        python3 -m pip install pydantic pydantic-settings
    else
        echo "❌ No .pyenv directory found, creating virtual environment"
        python3 -m venv .pyenv
        source .pyenv/bin/activate
        python3 -m pip install pydantic pydantic-settings
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
    Generates a dynamic codeblock prompt containing the current environment, AGOR version, task description, installation instructions, protocol initialization guidance, and optional previous work context.
    
    Args:
        task_description: Description of the task to be performed.
        environment: Optional dictionary with environment details; if not provided, environment is auto-detected.
        include_snapshot: Optional string containing previous work context to include in the prompt.
    
    Returns:
        A formatted string suitable for use as a codeblock prompt, including environment and setup information.
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
    Updates version strings in documentation and source files to the specified or current AGOR version.
    
    If no target version is provided, attempts to use the AGOR package version, falling back to "0.4.1" if unavailable. Searches for common version reference patterns in predefined files and replaces them with the target version. Returns a list of files that were updated.
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
    """Get current checklist status."""
    if _agent_checklist:
        return _agent_checklist.get_status()
    return {"status": "no_checklist"}


def enforce_session_end() -> bool:
    """Enforce session end procedures."""
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
    SAFE agent memory update with memory branch support - never switches branches.

    Args:
        agent_id: Agent identifier
        memory_type: Type of memory update (progress, decision, etc.)
        content: Memory content to add
        memory_branch: Memory branch to use (auto-generated if None)

    Returns:
        True if successful, False otherwise
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
