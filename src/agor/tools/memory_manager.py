"""
Memory Manager Module for AGOR Development Tools

This module contains all memory branch operations and cross-branch commit functionality
extracted from dev_tools.py for better organization and maintainability.

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
    Get the empty tree hash for the current repository.

    This function computes the empty tree hash dynamically to support
    both SHA-1 and SHA-256 repositories in a cross-platform way.

    Returns:
        Empty tree hash as string
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
    Commit file content to a memory branch in the Git repository without switching branches.
    
    Creates or updates a memory branch under the `.agor/` directory, initializing the branch with an empty commit if it does not exist. The function writes the provided file content to the specified file within the memory branch, creates a new commit, and updates the branch reference. The current working branch remains unchanged throughout the operation. Attempts to push the memory branch after committing, but push failures do not cause the operation to fail.
    
    Parameters:
        file_content (str): Content to be committed to the memory branch.
        file_name (str): Name of the file to create or update within the memory branch.
        branch_name (Optional[str]): Target memory branch name. If not provided, a name is auto-generated.
        commit_message (Optional[str]): Commit message. If not provided, a message is auto-generated.
    
    Returns:
        bool: True if the commit operation succeeds, False otherwise.
    """
    print("🛡️  Safe memory commit: staying on current branch")

    # Verify we can determine current branch (for safety, but don't store it)
    success, current_branch_output = run_git_command(["branch", "--show-current"])
    if not success:
        print(f"❌ Cannot determine current branch. Error: {current_branch_output}")
        return False

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
            success, initial_commit_output = run_git_command(
                [
                    "commit-tree",
                    empty_tree_hash,
                    "-m",
                    f"Initialize memory branch {branch_name}",
                ]
            )
            if not success:
                print(f"❌ Failed to create initial commit for memory branch. Error: {initial_commit_output}")
                return False
            initial_commit = initial_commit_output.strip()

            # Create branch reference pointing to initial empty commit
            success, update_ref_output = run_git_command(
                ["update-ref", f"refs/heads/{branch_name}", initial_commit]
            )
            if not success:
                print(f"❌ Failed to create branch reference. Error: {update_ref_output}")
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
            print(f"   Hashing file content for {file_name}...")
            success, blob_hash_output = run_git_command(["hash-object", "-w", str(temp_file)])
            if not success:
                print(f"❌ Failed to create blob object from temp file. Error: {blob_hash_output}")
                return False
            blob_hash = blob_hash_output.strip()
            print(f"   Blob hash created: {blob_hash[:12]}")

            # Step 4: Get current tree of memory branch
            print(f"   Getting current tree for memory branch {branch_name}...")
            success, tree_hash_output = run_git_command(
                ["rev-parse", f"{branch_name}^{{tree}}"]
            )
            if not success:
                print(f"   Warning: Could not parse tree for {branch_name}. Assuming empty tree. Error: {tree_hash_output}")
                tree_hash = get_empty_tree_hash()
            else:
                tree_hash = tree_hash_output.strip()
            print(f"   Using tree hash: {tree_hash[:12]}")

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
                print(f"   Reading tree {tree_hash[:12]} into temporary index...")
                success, rt_output = run_git_command(["read-tree", tree_hash], env=env)
                if not success:
                    print(f"❌ `git read-tree` failed for tree {tree_hash}. Error: {rt_output}")
                    return False
                print(f"   Tree read successfully.")

                # Add our file to index
                # Note: file_name should already include .agor/ prefix if needed
                print(f"   Adding file {file_name} (blob {blob_hash[:12]}) to temporary index...")
                success, ui_output = run_git_command(
                    [
                        "update-index",
                        "--add",
                        "--cacheinfo",
                        "100644",
                        blob_hash,
                        file_name,
                    ],
                    env=env,
                )
                if not success:
                    print(f"❌ Failed to update index with file {file_name}. Error: {ui_output}")
                    return False
                print(f"   Index updated successfully with {file_name}.")

                # Write new tree
                print(f"   Writing new tree from temporary index...")
                success, new_tree_hash_output = run_git_command(["write-tree"], env=env)
                if not success:
                    print(f"❌ Failed to write new tree. Error: {new_tree_hash_output}")
                    return False
                new_tree_hash = new_tree_hash_output.strip()
                print(f"   New tree created: {new_tree_hash[:12]}")

            finally:
                # Clean up temporary index
                if temp_index_file.exists():
                    temp_index_file.unlink()

            # Step 6: Create commit on memory branch
            print(f"   Getting parent commit for branch {branch_name}...")
            success, parent_commit_output = run_git_command(["rev-parse", branch_name])
            if not success:
                print(f"❌ Failed to get parent commit for {branch_name}. Error: {parent_commit_output}")
                return False
            parent_commit = parent_commit_output.strip()
            print(f"   Parent commit: {parent_commit[:12]}")

            print(f"   Creating new commit with tree {new_tree_hash[:12]} and parent {parent_commit[:12]}...")
            success, new_commit_output = run_git_command(
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
                print(f"❌ Failed to create new commit object. Error: {new_commit_output}")
                return False
            new_commit = new_commit_output.strip()
            print(f"   New commit created: {new_commit[:12]}")

            # Step 7: Update branch reference
            print(f"   Updating branch reference {branch_name} to point to new commit {new_commit[:12]}...")
            success, update_ref_output_final = run_git_command(
                ["update-ref", f"refs/heads/{branch_name}", new_commit]
            )
            if not success:
                print(f"❌ Failed to update branch reference {branch_name}. Error: {update_ref_output_final}")
                return False

            # Step 8: Push memory branch (optional, don't fail if this doesn't work)
            # Use safe push for memory branches too, but don't fail the whole operation
            if not safe_git_push(branch_name=branch_name):
                print(
                    f"⚠️  Failed to push memory branch {branch_name} (local commit succeeded)"
                )

            print(
                f"✅ Successfully committed {file_name} to memory branch {branch_name}"
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


def auto_commit_memory(
    content: str, memory_type: str, agent_id: str, memory_branch: str = None
) -> bool:
    """
    Automatically commit content to main memory branch with agent directory structure.

    Args:
        content: Memory content to commit
        memory_type: Type of memory (e.g., 'session_start', 'progress', 'completion')
        agent_id: Agent identifier (will be sanitized for security)
        memory_branch: Optional specific memory branch. If not provided, uses main memory branch.

    Returns:
        True if successful, False otherwise
    """
    # Import sanitization function from utils (centralized location)
    from agor.utils import sanitize_slug

    # Sanitize inputs to prevent injection attacks
    safe_agent_id = sanitize_slug(agent_id)
    safe_memory_type = sanitize_slug(memory_type)

    print(f"💾 Auto-committing memory: {safe_memory_type} for {safe_agent_id}")

    # Use main memory branch with agent directory structure
    if memory_branch is None:
        memory_branch = "agor/mem/main"

    # Create standardized file name with sanitized components in agent directory
    file_name = f"agents/{safe_agent_id}/{safe_agent_id}-memory.md"

    # Create commit message with sanitized components
    commit_message = f"Memory update: {safe_memory_type} for {safe_agent_id}"

    # Commit to main memory branch with agent directory structure
    return commit_to_memory_branch(
        file_content=content,
        file_name=file_name,
        branch_name=memory_branch,
        commit_message=commit_message,
    )


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
    Lists all memory branches in the repository without switching the current branch.

    If available, uses the MemorySync class to retrieve both local and remote memory branches.
    Falls back to parsing Git branch output if MemorySync is unavailable or fails.

    Args:
        repo_path: Optional path to the repository. Defaults to the current working directory.

    Returns:
        A sorted list of memory branch names, or an empty list if none are found or on failure.
    """
    if repo_path is None:
        repo_path = Path.cwd()

    try:
        from agor.memory_sync import MemorySyncManager

        # Create MemorySyncManager instance with current repo path
        memory_sync = MemorySyncManager(repo_path=repo_path)

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
