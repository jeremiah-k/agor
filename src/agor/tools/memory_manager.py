"""
Memory Manager Module for AGOR Development Tooling

This module contains all memory branch operations and cross-branch commit functionality
extracted from dev_tooling.py for better organization and maintainability.

Functions:
- commit_to_memory_branch: Cross-branch memory commits
- auto_commit_memory: Automated memory operations
- Memory branch creation and management
"""

import tempfile
import os
from pathlib import Path
from typing import Optional

from agor.tools.git_operations import run_git_command, safe_git_push, get_file_timestamp


def get_empty_tree_hash() -> str:
    """
    Get the empty tree hash for the current repository.

    This function computes the empty tree hash dynamically to support
    both SHA-1 and SHA-256 repositories in a cross-platform way.

    Returns:
        Empty tree hash as string
    """
    # Method 1: Create empty tree using write-tree with empty index
    temp_index_fd, temp_index_path = tempfile.mkstemp(suffix=".index", prefix="empty_tree_")
    temp_index_file = Path(temp_index_path)

    try:
        # Close the file descriptor but keep the file
        os.close(temp_index_fd)

        # Create a minimal empty index file
        with open(temp_index_file, 'wb') as f:
            # Write minimal git index header (version 2, 0 entries)
            f.write(b'DIRC')  # signature
            f.write(b'\x00\x00\x00\x02')  # version 2
            f.write(b'\x00\x00\x00\x00')  # 0 entries
            # Add SHA-1 checksum of the header (20 bytes of zeros for simplicity)
            f.write(b'\x00' * 20)

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
    Commit content to a memory branch without switching from current branch.
    
    This function creates memory branches 1 commit behind HEAD (not orphan branches)
    for easier navigation and merge prevention.
    
    Args:
        file_content: Content to commit
        file_name: Name of file to create/update
        branch_name: Target memory branch (auto-generated if None)
        commit_message: Commit message (auto-generated if None)
    
    Returns:
        True if successful, False otherwise
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
        success, _ = run_git_command(["rev-parse", "--verify", f"refs/heads/{branch_name}"])
        branch_exists = success
        
        if not branch_exists:
            # Create new memory branch with empty tree (only .agor files)
            print(f"📝 Creating new memory branch: {branch_name}")

            # Create empty tree for memory branch (no project files)
            # Get empty tree hash for current repository (supports both SHA-1 and SHA-256)
            empty_tree_hash = get_empty_tree_hash()

            # Create initial commit with empty tree
            success, initial_commit = run_git_command([
                "commit-tree", empty_tree_hash, "-m", f"Initialize memory branch {branch_name}"
            ])
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

            print(f"✅ Created memory branch {branch_name} with empty tree (commit: {initial_commit[:8]})")

        # Step 2: Create temporary file with content
        temp_file = None
        try:
            temp_fd, temp_path = tempfile.mkstemp(suffix=".tmp", prefix="agor_memory_")
            temp_file = Path(temp_path)
            
            # Write content to temporary file
            with os.fdopen(temp_fd, 'w', encoding='utf-8') as f:
                f.write(file_content)
            
            # Step 3: Add file to git index for the memory branch
            success, blob_hash = run_git_command(["hash-object", "-w", str(temp_file)])
            if not success:
                print("❌ Failed to create blob object")
                return False
            blob_hash = blob_hash.strip()
            
            # Step 4: Get current tree of memory branch
            success, tree_hash = run_git_command(["rev-parse", f"{branch_name}^{{tree}}"])
            if not success:
                # If branch has no commits, use the computed empty tree hash
                tree_hash = empty_tree_hash
            else:
                tree_hash = tree_hash.strip()
            
            # Step 5: Create new tree with our file
            # Create a temporary index file
            temp_index_fd, temp_index_path = tempfile.mkstemp(suffix=".index", prefix="agor_")
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
                success, ui_output = run_git_command([
                    "update-index", "--add", "--cacheinfo", "100644", blob_hash, f".agor/{file_name}"
                ], env=env)
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
            
            success, new_commit = run_git_command([
                "commit-tree", new_tree_hash, "-p", parent_commit, "-m", commit_message
            ])
            if not success:
                print("❌ Failed to create commit")
                return False
            new_commit = new_commit.strip()
            
            # Step 7: Update branch reference
            success, _ = run_git_command([
                "update-ref", f"refs/heads/{branch_name}", new_commit
            ])
            if not success:
                print("❌ Failed to update branch reference")
                return False
            
            # Step 8: Push memory branch (optional, don't fail if this doesn't work)
            # Use safe push for memory branches too, but don't fail the whole operation
            if not safe_git_push(branch_name=branch_name):
                print(
                    f"⚠️  Failed to push memory branch {branch_name} (local commit succeeded)"
                )
            
            print(f"✅ Successfully committed .agor/{file_name} to memory branch {branch_name}")
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
    Automatically commit content to memory branch with standardized naming.
    
    Args:
        content: Memory content to commit
        memory_type: Type of memory (e.g., 'session_start', 'progress', 'completion')
        agent_id: Agent identifier
    
    Returns:
        True if successful, False otherwise
    """
    print(f"💾 Auto-committing memory: {memory_type} for {agent_id}")
    
    # Create standardized file name
    file_name = f"{agent_id}-memory.md"
    
    # Create commit message
    commit_message = f"Memory update: {memory_type} for {agent_id}"
    
    # Commit to memory branch
    return commit_to_memory_branch(
        file_content=content,
        file_name=file_name,
        commit_message=commit_message
    )
