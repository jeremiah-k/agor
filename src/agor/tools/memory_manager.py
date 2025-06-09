"""
Memory Manager Module for AGOR Development Tooling

This module contains all memory branch operations and cross-branch commit functionality
extracted from dev_tooling.py for better organization and maintainability.

Functions:
- commit_to_memory_branch: Cross-branch memory commits
- auto_commit_memory: Automated memory operations
- Memory branch creation and management
"""

import os
import tempfile
from pathlib import Path
from typing import Optional

from agor.tools.git_operations import get_file_timestamp, run_git_command, safe_git_push


def get_empty_tree_hash() -> str:
    """
    Returns the empty tree hash for the current Git repository.
    
    Dynamically computes the empty tree hash to support both SHA-1 and SHA-256 repositories. Falls back to the known SHA-1 empty tree hash if dynamic computation fails.
    
    Returns:
        The empty tree hash as a string.
    """
    # Method 1: Create empty tree using write-tree with empty index
    temp_index_fd, temp_index_path = tempfile.mkstemp(
        suffix=".index", prefix="empty_tree_"
    )
    temp_index_file = Path(temp_index_path)

    try:
        # Close the file descriptor but keep the file
        os.close(temp_index_fd)

        # Create a minimal empty index file
        with open(temp_index_file, "wb") as f:
            # Write minimal git index header (version 2, 0 entries)
            f.write(b"DIRC")  # signature
            f.write(b"\x00\x00\x00\x02")  # version 2
            f.write(b"\x00\x00\x00\x00")  # 0 entries
            # Add SHA-1 checksum of the header (20 bytes of zeros for simplicity)
            f.write(b"\x00" * 20)

        empty_env = os.environ.copy()
        empty_env["GIT_INDEX_FILE"] = str(temp_index_file)
        success, output = run_git_command(["write-tree"], env=empty_env)
        if success:
            return output.strip()
    except Exception:
        pass
    finally:
        if temp_index_file.exists():
            temp_index_file.unlink()

    # Method 2: Use known SHA-1 hash as fallback (most repositories are SHA-1)
    return "4b825dc642cb6eb9a060e54bf8d69288fbee4904"


def commit_to_memory_branch(
    file_content: str,
    file_name: str,
    branch_name: Optional[str] = None,
    commit_message: Optional[str] = None,
) -> bool:
    """
    Commits content to a memory branch without switching the current Git branch.
    
    Creates or updates a memory branch by adding the specified file content under the `.agor/` directory, initializing the branch if it does not exist. The operation is performed entirely in the background, preserving the user's current branch and working state. Returns `True` if the commit and branch update succeed, or `False` if any step fails.
    
    Args:
        file_content: The content to write to the file in the memory branch.
        file_name: The name of the file to create or update under `.agor/` in the memory branch.
        branch_name: The target memory branch name. If not provided, a new branch is auto-generated.
        commit_message: The commit message to use. If not provided, a default message is generated.
    
    Returns:
        True if the memory commit succeeds, False otherwise.
    """
    print("🛡️  Safe memory commit: staying on current branch")

    # Get current branch to stay on it
    success, current_branch = run_git_command(["branch", "--show-current"])
    if not success:
        print("❌ Cannot determine current branch")
        return False
    current_branch = current_branch.strip()

    # Generate branch name if not provided
    if not branch_name:
        timestamp = get_file_timestamp()
        branch_name = f"agor/mem/{timestamp}"

    # Generate commit message if not provided
    if not commit_message:
        commit_message = f"Memory update: {file_name}"

    try:
        # Step 1: Check if memory branch exists
        success, _ = run_git_command(
            ["rev-parse", "--verify", f"refs/heads/{branch_name}"]
        )
        branch_exists = success

        if not branch_exists:
            # Create new memory branch with empty tree (only .agor files)
            print(f"📝 Creating new memory branch: {branch_name}")

            # Create empty tree for memory branch (no project files)
            # Get empty tree hash for current repository (supports both SHA-1 and SHA-256)
            empty_tree_hash = get_empty_tree_hash()

            # Create initial commit with empty tree
            success, initial_commit = run_git_command(
                [
                    "commit-tree",
                    empty_tree_hash,
                    "-m",
                    f"Initialize memory branch {branch_name}",
                ]
            )
            if not success:
                print("❌ Failed to create initial commit for memory branch")
                return False
            initial_commit = initial_commit.strip()

            # Create branch reference pointing to initial empty commit
            success, _ = run_git_command(
                ["update-ref", f"refs/heads/{branch_name}", initial_commit]
            )
            if not success:
                print("❌ Failed to create branch reference")
                return False

            print(
                f"✅ Created memory branch {branch_name} with empty tree (commit: {initial_commit[:8]})"
            )

        # Step 2: Create temporary file with content
        temp_file = None
        try:
            temp_fd, temp_path = tempfile.mkstemp(suffix=".tmp", prefix="agor_memory_")
            temp_file = Path(temp_path)

            # Write content to temporary file
            with os.fdopen(temp_fd, "w", encoding="utf-8") as f:
                f.write(file_content)

            # Step 3: Add file to git index for the memory branch
            success, blob_hash = run_git_command(["hash-object", "-w", str(temp_file)])
            if not success:
                print("❌ Failed to create blob object")
                return False
            blob_hash = blob_hash.strip()

            # Step 4: Get current tree of memory branch
            success, tree_hash = run_git_command(
                ["rev-parse", f"{branch_name}^{{tree}}"]
            )
            if not success:
                # If branch has no commits, use the computed empty tree hash
                tree_hash = empty_tree_hash
            else:
                tree_hash = tree_hash.strip()

            # Step 5: Create new tree with our file
            # Create a temporary index file
            temp_index_fd, temp_index_path = tempfile.mkstemp(
                suffix=".index", prefix="agor_"
            )
            os.close(temp_index_fd)
            temp_index_file = Path(temp_index_path)

            try:
                # Set temporary index
                env = os.environ.copy()
                env["GIT_INDEX_FILE"] = str(temp_index_file)

                # Initialize index (always read tree, even if empty)
                success, rt_output = run_git_command(["read-tree", tree_hash], env=env)
                if not success:
                    print(f"❌ `git read-tree` failed for {tree_hash}: {rt_output}")
                    return False

                # Add our file to index
                success, ui_output = run_git_command(
                    [
                        "update-index",
                        "--add",
                        "--cacheinfo",
                        "100644",
                        blob_hash,
                        f".agor/{file_name}",
                    ],
                    env=env,
                )
                if not success:
                    print(f"❌ Failed to update index: {ui_output}")
                    return False

                # Write new tree
                success, new_tree_hash = run_git_command(["write-tree"], env=env)
                if not success:
                    print("❌ Failed to write tree")
                    return False
                new_tree_hash = new_tree_hash.strip()

            finally:
                # Clean up temporary index
                if temp_index_file.exists():
                    temp_index_file.unlink()

            # Step 6: Create commit on memory branch
            success, parent_commit = run_git_command(["rev-parse", branch_name])
            if not success:
                print("❌ Failed to get parent commit")
                return False
            parent_commit = parent_commit.strip()

            success, new_commit = run_git_command(
                [
                    "commit-tree",
                    new_tree_hash,
                    "-p",
                    parent_commit,
                    "-m",
                    commit_message,
                ]
            )
            if not success:
                print("❌ Failed to create commit")
                return False
            new_commit = new_commit.strip()

            # Step 7: Update branch reference
            success, _ = run_git_command(
                ["update-ref", f"refs/heads/{branch_name}", new_commit]
            )
            if not success:
                print("❌ Failed to update branch reference")
                return False

            # Step 8: Push memory branch (optional, don't fail if this doesn't work)
            # Use safe push for memory branches too, but don't fail the whole operation
            if not safe_git_push(branch_name=branch_name):
                print(
                    f"⚠️  Failed to push memory branch {branch_name} (local commit succeeded)"
                )

            print(
                f"✅ Successfully committed .agor/{file_name} to memory branch {branch_name}"
            )
            return True

        finally:
            # Clean up temporary file
            if temp_file and temp_file.exists():
                try:
                    temp_file.unlink()
                except Exception as e:
                    print(f"⚠️  Failed to cleanup temporary file: {e}")

    except Exception as e:
        print(f"❌ Memory commit failed: {e}")
        return False


def auto_commit_memory(content: str, memory_type: str, agent_id: str) -> bool:
    """
    Commits memory content to a memory branch using standardized file naming and commit messages.
    
    Constructs a file name and commit message based on the provided memory type and agent ID, then commits the content to the appropriate memory branch.
    
    Args:
        content: The memory content to commit.
        memory_type: The type of memory event (e.g., 'session_start', 'progress', 'completion').
        agent_id: Identifier for the agent associated with the memory.
    
    Returns:
        True if the commit operation succeeds; False otherwise.
    """
    print(f"💾 Auto-committing memory: {memory_type} for {agent_id}")

    # Create standardized file name
    file_name = f"{agent_id}-memory.md"

    # Create commit message
    commit_message = f"Memory update: {memory_type} for {agent_id}"

    # Commit to memory branch
    return commit_to_memory_branch(
        file_content=content, file_name=file_name, commit_message=commit_message
    )


def read_from_memory_branch(
    file_path: str, branch_name: str, repo_path: Optional[Path] = None
) -> Optional[str]:
    """
    Reads the content of a file from a specified memory branch without switching branches.
    
    Ensures the current working branch remains unchanged throughout the operation. Returns the file content as a string if successful; otherwise, returns None.
    """
    if repo_path is None:
        repo_path = Path.cwd()

    try:
        from agor.tools.git_operations import run_git_command

        success, current_branch = run_git_command(["branch", "--show-current"])
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
        success, content = run_git_command(["show", f"{branch_name}:{file_path}"])
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
    Returns a sorted list of all memory branches (local and remote) in the repository without switching branches.
    
    If the primary method using MemorySync fails, falls back to parsing Git branch output to identify memory branches. Returns an empty list if no branches are found or on error.
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
            from agor.tools.git_operations import run_git_command

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
