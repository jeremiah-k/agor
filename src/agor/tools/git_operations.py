"""
Git Operations Module for AGOR Development Tooling

This module contains all git-related functionality extracted from dev_tooling.py
for better organization and maintainability.

Functions:
- safe_git_push: Safe git push with upstream checking and protected branch validation
- Git command execution utilities
- Timestamp generation for git operations
"""

import subprocess
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple


def get_current_timestamp() -> str:
    """
    Returns the current UTC timestamp formatted as "YYYY-MM-DD HH:MM UTC".
    """
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")


def get_file_timestamp() -> str:
    """
    Returns the current UTC timestamp formatted for safe use in filenames.
    
    The timestamp is formatted as "YYYY-MM-DD_HHMM".
    """
    return datetime.utcnow().strftime("%Y-%m-%d_%H%M")


def get_precise_timestamp() -> str:
    """
    Returns the current UTC timestamp including seconds, formatted as "YYYY-MM-DD HH:MM:SS UTC".
    """
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")


def get_ntp_timestamp() -> str:
    """
    Returns the current UTC timestamp from an NTP server, formatted as "YYYY-MM-DD HH:MM UTC".
    
    If the NTP server is unreachable or an error occurs, falls back to the local system time.
    """
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
        return get_current_timestamp()


def run_git_command(command: list, env: Optional[dict] = None) -> Tuple[bool, str]:
    """
    Executes a git command and returns whether it succeeded along with its output or error message.
    
    Args:
        command: List of arguments for the git command, excluding the 'git' executable.
        env: Optional dictionary of environment variables to use for the command.
    
    Returns:
        A tuple containing a boolean indicating success, and the command's output or error message.
    """
    try:
        # Detect git binary using shutil.which for better cross-platform compatibility
        git_binary = shutil.which("git")
        if git_binary is None:
            git_binary = "git"  # Fallback

        full_command = [git_binary] + command
        result = subprocess.run(
            full_command,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=Path.cwd(),
            env=env
        )
        
        if result.returncode == 0:
            return True, result.stdout
        return False, f"Git error: {result.stderr}"
            
    except subprocess.TimeoutExpired:
        return False, "Git command timed out"
    except Exception as e:
        return False, f"Git command failed: {str(e)}"


def safe_git_push(
    branch_name: Optional[str] = None, 
    force: bool = False, 
    explicit_force: bool = False
) -> bool:
    """
    Performs a git push with safety checks to prevent accidental data loss or conflicts.
    
    This function enforces safe push practices by:
    - Determining the current branch if not specified.
    - Preventing force pushes to protected branches (`main`, `master`, `develop`, `production`).
    - Requiring explicit confirmation for force pushes.
    - Fetching from the remote to detect upstream changes and aborting if the remote has new commits not present locally (unless forced).
    - Adding `--set-upstream` if pushing to a new remote branch.
    
    Args:
        branch_name: The branch to push. If not provided, uses the current branch.
        force: If True, attempts a force push (requires explicit_force=True).
        explicit_force: Must be True to allow force pushing.
    
    Returns:
        True if the push succeeds, False otherwise.
    """
    print("🛡️  Safe git push: performing safety checks...")
    
    # Get current branch if not specified
    if not branch_name:
        success, current_branch = run_git_command(["branch", "--show-current"])
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
    success, output = run_git_command(["fetch", "origin", branch_name])
    if not success:
        print(f"⚠️  Failed to fetch from remote: {output}")
        print("Proceeding with push (remote may not exist yet)")
    
    # Step 2: Check if upstream has changes we don't have
    success, local_commit = run_git_command(["rev-parse", "HEAD"])
    if not success:
        print("❌ Cannot get local commit hash")
        return False
    local_commit = local_commit.strip()
    
    success, remote_commit = run_git_command(["rev-parse", f"origin/{branch_name}"])
    remote_branch_exists = success

    if success:
        remote_commit = remote_commit.strip()
        if local_commit != remote_commit and not force:
            # Check if we're behind
            success, merge_base = run_git_command(["merge-base", "HEAD", f"origin/{branch_name}"])
            if success and merge_base.strip() == local_commit:
                print("🚨 UPSTREAM CHANGES DETECTED: Remote has commits we don't have")
                print("You need to pull and merge/rebase before pushing")
                print(f"Run: git pull origin {branch_name}")
                return False

    # Step 3: Perform the push
    push_command = ["push", "origin", branch_name]

    # If remote branch doesn't exist, add --set-upstream for first push
    if not remote_branch_exists:
        push_command.extend(["--set-upstream"])
    if force:
        push_command.append("--force")
        print(f"⚠️  FORCE PUSHING to {branch_name} (explicit_force=True)")
    else:
        print(f"✅ Safe pushing to {branch_name}")
    
    success, output = run_git_command(push_command)
    if not success:
        print(f"❌ Push failed: {output}")
        return False
    
    print(f"✅ Successfully pushed to {branch_name}")
    return True


def quick_commit_push(message: str, emoji: str = "🔧") -> bool:
    """
    Stages all changes, commits with a timestamped message, and safely pushes to the remote repository.
    
    Args:
        message: The commit message to include.
        emoji: An emoji to prefix the commit message.
    
    Returns:
        True if the commit and push were successful or if there were no changes to commit; False otherwise.
    """
    timestamp = get_current_timestamp()
    full_message = f"{emoji} {message} - {timestamp}"

    print(f"🚀 Quick commit/push: {emoji} {message}")

    # Add all changes
    success, output = run_git_command(["add", "."])
    if not success:
        print(f"❌ Failed to add files: {output}")
        return False

    # Commit
    success, output = run_git_command(["commit", "-m", full_message])
    if not success:
        # Check if it's just "nothing to commit"
        if "nothing to commit" in output.lower():
            print("✅ No changes to commit (working directory clean)")
            return True
        print(f"❌ Failed to commit: {output}")
        return False
    
    # Safe push
    if not safe_git_push():
        print("❌ Safe push failed")
        return False
    
    print(f"✅ Successfully committed and pushed at {timestamp}")
    return True
