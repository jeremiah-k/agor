import pathlib
import subprocess
import sys
from datetime import datetime
from typing import List, Optional

from agor.git_binary import git_manager
from agor.settings import settings


class MemorySyncManager:
    """Manages the synchronization of the memory file with a remote git repository."""

    MEMORY_BRANCH_PREFIX = "agor/mem/"  # Updated prefix

    def __init__(self, repo_path: Optional[pathlib.Path] = None):
        """
        Initializes the MemorySyncManager.

        Args:
            repo_path: The path to the git repository. If None, defaults to the current working directory.
        """
        self.repo_path = repo_path if repo_path else pathlib.Path().resolve()
        self.git_binary = git_manager.get_git_binary()
        self.memory_file_relative_path = settings.memory_file

    def _run_git_command(self, command: List[str]) -> str:
        """
        Runs a git command and returns its output.

        Args:
            command: A list of strings representing the git command and its arguments.

        Returns:
            The stdout of the git command.

        Raises:
            RuntimeError: If the git command fails.
        """
        try:
            process = subprocess.run(
                [self.git_binary] + command,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True,
            )
            return process.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Error running git command: {' '.join(command)}", file=sys.stderr)
            print(f"Stdout: {e.stdout}", file=sys.stderr)
            print(f"Stderr: {e.stderr}", file=sys.stderr)
            raise RuntimeError(f"Git command failed: {' '.join(command)}") from e
        except FileNotFoundError:
            print(f"Error: Git binary not found at {self.git_binary}", file=sys.stderr)
            raise

    def generate_memory_branch_name(self) -> str:
        """Generates a unique name for the memory branch."""
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
        return f"{self.MEMORY_BRANCH_PREFIX}{timestamp}"

    def sync_memory_with_remote(self) -> None:
        """Synchronizes the memory file with the remote repository."""
        pass

    def _get_current_branch(self) -> Optional[str]:
        """Gets the current active git branch."""
        try:
            branch_name = self._run_git_command(["rev-parse", "--abbrev-ref", "HEAD"])
            if branch_name != "HEAD":
                return branch_name.strip()
            else:
                # Detached HEAD state
                return None
        except RuntimeError:
            # Command failed or other issue
            return None

    def _create_memory_branch(self, branch_name: str) -> bool:
        """
        Creates a new memory branch using simplified approach (HEAD~1).

        Creates branch from HEAD~1 to ensure it's unmergeable with working branches
        but avoids complex orphan branch conflicts.

        Args:
            branch_name: The name for the new memory branch.

        Returns:
            True if the branch was created successfully, False otherwise.
        """
        try:
            # Create branch from 1 commit behind HEAD (simplified approach)
            # This makes it unmergeable but avoids orphan branch complexity
            self._run_git_command(["checkout", "-b", branch_name, "HEAD~1"])

            # Create .agor directory if it doesn't exist
            agor_dir = self.repo_path / ".agor"
            agor_dir.mkdir(exist_ok=True)

            # Create an initial commit with .agor directory
            self._run_git_command(["add", ".agor"])
            self._run_git_command(
                [
                    "commit",
                    "--allow-empty",
                    "-m",
                    f"Initial commit for memory branch {branch_name}",
                ]
            )

            return True
        except RuntimeError:
            # If any git command fails, _run_git_command will raise RuntimeError
            print(f"Failed to create memory branch '{branch_name}'.", file=sys.stderr)
            return False

    def _switch_to_branch(self, branch_name: str) -> bool:
        """
        Switches to the specified git branch.

        Args:
            branch_name: The name of the branch to switch to.

        Returns:
            True if the switch was successful, False otherwise.
        """
        try:
            self._run_git_command(["checkout", branch_name])
            return True
        except RuntimeError:
            print(f"Failed to switch to branch '{branch_name}'.", file=sys.stderr)
            return False

    def list_memory_branches(self, remote: bool = False) -> List[str]:
        """
        Lists local or remote memory branches.

        Args:
            remote: If True, lists remote branches, otherwise lists local branches.

        Returns:
            A list of memory branch names.
        """
        command: List[str]
        if remote:
            command = [
                "branch",
                "--remote",
                "--list",
                f"origin/{self.MEMORY_BRANCH_PREFIX}*",
            ]
        else:
            command = ["branch", "--list", f"{self.MEMORY_BRANCH_PREFIX}*"]

        try:
            output = self._run_git_command(command)
            branches = []
            for line in output.splitlines():
                branch_name = line.strip()
                if branch_name.startswith("* "):
                    branch_name = branch_name[
                        2:
                    ]  # Remove "* " prefix for current branch

                if remote:
                    # Remote branches are listed as "origin/agor/mem/..."
                    # We want to return "agor/mem/..."
                    if branch_name.startswith(f"origin/{self.MEMORY_BRANCH_PREFIX}"):
                        branch_name = branch_name[len("origin/") :]

                if branch_name:  # Ensure no empty strings are added
                    branches.append(branch_name)
            return list(set(branches))  # Return unique branch names
        except RuntimeError:
            print(
                f"Failed to list {'remote' if remote else 'local'} memory branches.",
                file=sys.stderr,
            )
            return []

    def _add_and_commit_memory_file(self, commit_message: str) -> bool:
        """
        Adds and commits the memory file to the current branch.

        Args:
            commit_message: The commit message to use.

        Returns:
            True if the file was added and committed successfully (or if there were no changes),
            False otherwise.
        """
        try:
            # Add the memory file
            self._run_git_command(["add", str(self.memory_file_relative_path)])

            # Commit the changes
            try:
                self._run_git_command(["commit", "-m", commit_message])
            except RuntimeError as e:
                # Check if commit failed due to "nothing to commit"
                # The actual error message might vary slightly depending on git version and configuration.
                # Common phrases include "nothing to commit", "no changes added to commit".
                # We access the underlying CalledProcessError's stderr if available.
                original_exception = e.__cause__
                if isinstance(original_exception, subprocess.CalledProcessError):
                    if (
                        "nothing to commit" in original_exception.stderr.lower()
                        or "no changes added to commit"
                        in original_exception.stderr.lower()
                    ):
                        print(
                            f"No changes to commit for memory file '{self.memory_file_relative_path}'.",
                            file=sys.stdout,
                        )
                        return True  # Considered a success in this context
                # If it's a different error, re-raise to be caught by the outer try-except
                raise e

            return True
        except RuntimeError as e:
            # This catches errors from `git add` or other errors from `git commit`
            print(
                f"Failed to add/commit memory file '{self.memory_file_relative_path}': {e}",
                file=sys.stderr,
            )
            return False

    def get_active_memory_branch(self) -> Optional[str]:
        """
        Gets the current active memory branch, if any.

        Returns:
            The name of the active memory branch if the current branch is a memory branch,
            otherwise None.
        """
        current_branch = self._get_current_branch()
        if current_branch and current_branch.startswith(self.MEMORY_BRANCH_PREFIX):
            return current_branch
        return None

    def _push_memory_branch_to_remote(
        self, branch_name: str, force: bool = False
    ) -> bool:
        """
        Pushes the specified local branch to the remote 'origin'.

        Args:
            branch_name: The name of the local branch to push.
            force: If True, uses '--force' with the push command.

        Returns:
            True if the push was successful, False otherwise.
        """
        command = ["push", "origin", branch_name]
        if force:
            command.append("--force")

        try:
            self._run_git_command(command)
            print(
                f"Branch '{branch_name}' pushed to remote successfully {'(forced)' if force else ''}.",
                file=sys.stdout,
            )
            return True
        except RuntimeError:
            print(
                f"Failed to push branch '{branch_name}' to remote {'(forced)' if force else ''}.",
                file=sys.stderr,
            )
            return False

    def _pull_and_rebase_memory_branch(self, branch_name: str) -> bool:
        """
        Pulls updates from the remote for the given branch and rebases the
        local branch onto the fetched version.

        Args:
            branch_name: The name of the memory branch to pull and rebase.

        Returns:
            True if the pull and rebase was successful, False otherwise.
        """
        command = ["pull", "--rebase", "origin", branch_name]
        try:
            self._run_git_command(command)
            print(
                f"Successfully pulled and rebased branch '{branch_name}' from origin.",
                file=sys.stdout,
            )
            return True
        except RuntimeError:
            # This can happen due to network issues, or conflicts that git cannot auto-resolve.
            print(
                f"Failed to pull and rebase branch '{branch_name}' from origin.",
                file=sys.stderr,
            )
            return False

    def ensure_memory_branch_exists(
        self, branch_name: str, switch_if_exists: bool = True, attempt_pull: bool = True
    ) -> bool:
        """
        Ensures a specific memory branch exists, by checking locally, then remotely,
        or creating it new. Optionally switches to it and pulls updates.

        Args:
            branch_name: The name of the memory branch to ensure exists.
            switch_if_exists: If True and the branch exists (locally or pulled from remote),
                              switch to it. If a new branch is created, it's typically
                              checked out automatically by _create_memory_branch.
            attempt_pull: If True and the branch exists locally or is checked out from remote,
                          attempt to pull and rebase updates from origin.

        Returns:
            True if the branch exists (or was created) and is ready for use (potentially switched to),
            False otherwise.
        """
        local_branches = self.list_memory_branches(remote=False)
        if branch_name in local_branches:
            print(f"Branch '{branch_name}' already exists locally.", file=sys.stdout)
            if (
                self._get_current_branch() != branch_name
            ):  # Only pull/switch if not already on it
                if attempt_pull:
                    if not self._pull_and_rebase_memory_branch(branch_name):
                        print(
                            f"Warning: Failed to pull and rebase existing local branch '{branch_name}'. Continuing...",
                            file=sys.stderr,
                        )

                if switch_if_exists:
                    if not self._switch_to_branch(branch_name):
                        print(
                            f"Error: Failed to switch to existing local branch '{branch_name}'.",
                            file=sys.stderr,
                        )
                        return False
            elif attempt_pull:  # Already on the branch, just try to pull
                if not self._pull_and_rebase_memory_branch(branch_name):
                    print(
                        f"Warning: Failed to pull and rebase current branch '{branch_name}'. Continuing...",
                        file=sys.stderr,
                    )
            return True

        remote_branches = self.list_memory_branches(remote=True)
        if branch_name in remote_branches:
            print(
                f"Branch '{branch_name}' found on remote 'origin'. Attempting to check out...",
                file=sys.stdout,
            )
            try:
                # Try simple checkout first (git might auto-setup tracking)
                self._run_git_command(["checkout", branch_name])
                print(
                    f"Successfully checked out branch '{branch_name}' from remote.",
                    file=sys.stdout,
                )
            except RuntimeError:
                try:
                    # Fallback to explicit tracking setup
                    self._run_git_command(
                        ["checkout", "-b", branch_name, f"origin/{branch_name}"]
                    )
                    print(
                        f"Successfully checked out branch '{branch_name}' from remote by creating local tracking branch.",
                        file=sys.stdout,
                    )
                except RuntimeError as e_checkout:
                    print(
                        f"Error: Failed to checkout branch '{branch_name}' from remote: {e_checkout}",
                        file=sys.stderr,
                    )
                    return False

            # At this point, checkout was successful
            if attempt_pull:  # Usually desired after checking out a remote branch
                if not self._pull_and_rebase_memory_branch(branch_name):
                    print(
                        f"Warning: Failed to pull and rebase branch '{branch_name}' after checking out from remote. The branch may not be up-to-date.",
                        file=sys.stderr,
                    )
            return True

        # If not found locally or remotely, create it
        print(
            f"Branch '{branch_name}' not found locally or on remote. Creating new branch.",
            file=sys.stdout,
        )
        if self._create_memory_branch(branch_name):
            # _create_memory_branch already checks out the branch
            print(
                f"Successfully created and checked out new branch '{branch_name}'.",
                file=sys.stdout,
            )
            # No explicit switch needed here as _create_memory_branch handles it.
            # No pull needed as it's a new local branch.
            return True
        else:
            # Error message already printed by _create_memory_branch
            return False

    def delete_local_branch(self, branch_name: str, force: bool = False) -> bool:
        """
        Deletes a local git branch.

        Args:
            branch_name: The name of the local branch to delete.
            force: If True, uses '-D' (force delete) instead of '-d'.

        Returns:
            True if the branch was deleted successfully, False otherwise.
        """
        current_branch = self._get_current_branch()
        if current_branch == branch_name:
            print(
                f"Error: Cannot delete the current active branch '{branch_name}'. Switch to another branch first.",
                file=sys.stderr,
            )
            return False

        command = ["branch"]
        if force:
            command.append("-D")
        else:
            command.append("-d")
        command.append(branch_name)

        try:
            self._run_git_command(command)
            print(
                f"Local branch '{branch_name}' deleted successfully {'(forced)' if force else ''}.",
                file=sys.stdout,
            )
            return True
        except RuntimeError:
            # Error message from _run_git_command already prints details
            print(
                f"Failed to delete local branch '{branch_name}' {'(forced)' if force else ''}.",
                file=sys.stderr,
            )
            return False

    def delete_remote_branch(self, branch_name: str) -> bool:
        """
        Deletes a remote git branch on 'origin'.

        Args:
            branch_name: The name of the remote branch to delete.
                         This should be the plain branch name, e.g., "memory/sync/mybranch",
                         not "origin/memory/sync/mybranch".

        Returns:
            True if the remote branch was deleted successfully, False otherwise.
        """
        command = ["push", "origin", "--delete", branch_name]
        try:
            self._run_git_command(command)
            print(
                f"Remote branch '{branch_name}' deleted successfully from origin.",
                file=sys.stdout,
            )
            return True
        except RuntimeError:
            # Error message from _run_git_command already prints details
            print(
                f"Failed to delete remote branch '{branch_name}' from origin.",
                file=sys.stderr,
            )
            return False

    def _resolve_conflicts_if_any(self) -> None:
        """Handles any merge conflicts that may arise."""
        pass

    def _cleanup_local_memory_branch(
        self, branch_name: str, original_branch: Optional[str]
    ) -> None:
        """Cleans up the local memory branch after synchronization."""
        pass

    def auto_sync_on_startup(self, preferred_branch_name: Optional[str] = None) -> bool:
        """
        Automatically determines and switches to the appropriate memory branch on startup.
        It can use a preferred branch, find the latest existing one, or create a new one.
        It also ensures the branch is pulled and the memory file's presence is checked.

        Args:
            preferred_branch_name: If provided, this specific memory branch will be used.

        Returns:
            True if a memory branch was successfully determined, ensured, and switched to.
            False if any critical step in preparing the memory branch fails.
        """
        target_branch_name: str
        original_branch = self._get_current_branch()

        if preferred_branch_name:
            if not preferred_branch_name.startswith(self.MEMORY_BRANCH_PREFIX):
                target_branch_name = self.MEMORY_BRANCH_PREFIX + preferred_branch_name
                print(
                    f"Preferred branch name '{preferred_branch_name}' was missing prefix. Using '{target_branch_name}'.",
                    file=sys.stdout,
                )
            else:
                target_branch_name = preferred_branch_name
            print(
                f"Using preferred memory branch: '{target_branch_name}'.",
                file=sys.stdout,
            )
        else:
            print(
                "No preferred memory branch specified. Determining most recent or creating new.",
                file=sys.stdout,
            )
            local_branches = self.list_memory_branches(remote=False)
            remote_branches = self.list_memory_branches(remote=True)

            all_potential_branches = sorted(
                list(set(local_branches + remote_branches)), reverse=True
            )

            if all_potential_branches:
                target_branch_name = all_potential_branches[0]
                print(
                    f"Found existing memory branches. Using most recent: '{target_branch_name}'.",
                    file=sys.stdout,
                )
            else:
                target_branch_name = self.generate_memory_branch_name()
                print(
                    f"No existing memory branches found. Generated new name: '{target_branch_name}'.",
                    file=sys.stdout,
                )

        # Ensure the target branch exists, is up-to-date, and switch to it.
        # switch_if_exists=True is crucial here. attempt_pull=True ensures it's updated.
        if not self.ensure_memory_branch_exists(
            target_branch_name, switch_if_exists=True, attempt_pull=True
        ):
            print(
                f"Error: Failed to ensure memory branch '{target_branch_name}' is ready.",
                file=sys.stderr,
            )
            if (
                original_branch and original_branch != self._get_current_branch()
            ):  # Check if branch actually changed
                print(
                    f"Attempting to switch back to original branch '{original_branch}'.",
                    file=sys.stdout,
                )
                if not self._switch_to_branch(original_branch):
                    print(
                        f"Error: Failed to switch back to original branch '{original_branch}'.",
                        file=sys.stderr,
                    )
            return False

        # Post-switch check for the memory file
        memory_file_abs_path = self.repo_path / self.memory_file_relative_path
        if not memory_file_abs_path.exists():
            # This is a warning because the memory system might create it on demand.
            # However, if it's an existing branch, it's unexpected.
            print(
                f"Warning: Memory file '{self.memory_file_relative_path}' not found on branch '{target_branch_name}'.",
                file=sys.stderr,
            )
            print(f"Expected at: '{memory_file_abs_path}'", file=sys.stderr)
            # Depending on strictness, one might return False here. For now, it's a warning.
        else:
            print(
                f"Memory file '{self.memory_file_relative_path}' is available on branch '{target_branch_name}'.",
                file=sys.stdout,
            )

        print(
            f"Successfully synchronized to memory branch '{target_branch_name}'.",
            file=sys.stdout,
        )
        return True

    def auto_sync_on_shutdown(
        self,
        target_branch_name: str,
        commit_message: str,
        push_changes: bool = True,
        restore_original_branch: Optional[str] = None,
    ) -> bool:
        """
        Saves the current memory state to the specified memory branch,
        optionally pushes to remote, and restores the original branch.

        Args:
            target_branch_name: The memory branch to save changes to.
            commit_message: The commit message for saving the memory.
            push_changes: If True, attempts to push the changes to the remote.
            restore_original_branch: If provided, switches back to this branch after operations.

        Returns:
            True if memory was successfully committed locally.
            False if critical operations like switching to the memory branch,
            committing, or restoring the original branch (if specified) failed.
        """
        current_active_branch = self._get_current_branch()

        # 1. Switch to Target Memory Branch (if not already on it)
        if current_active_branch != target_branch_name:
            print(
                f"Current branch is '{current_active_branch}'. Switching to '{target_branch_name}' for shutdown sync.",
                file=sys.stdout,
            )
            if not self._switch_to_branch(target_branch_name):
                print(
                    f"Error: Failed to switch to memory branch '{target_branch_name}' for shutdown sync.",
                    file=sys.stderr,
                )
                # Attempt to restore original_branch if it was provided and different from the current (failed) branch
                if (
                    restore_original_branch
                    and restore_original_branch != self._get_current_branch()
                ):
                    print(
                        f"Attempting to switch back to '{restore_original_branch}' due to earlier failure.",
                        file=sys.stdout,
                    )
                    if not self._switch_to_branch(restore_original_branch):
                        print(
                            f"Critical Error: Failed to restore original branch '{restore_original_branch}' after failing to switch to target.",
                            file=sys.stderr,
                        )
                return False
            print(
                f"Successfully switched to memory branch '{target_branch_name}' for saving.",
                file=sys.stdout,
            )
        else:
            print(
                f"Already on target memory branch '{target_branch_name}'. No switch needed for saving.",
                file=sys.stdout,
            )

        # 2. Commit Memory Files
        print(
            f"Attempting to commit memory file on branch '{target_branch_name}'.",
            file=sys.stdout,
        )
        if not self._add_and_commit_memory_file(commit_message):
            print(
                f"Error: Failed to commit memory file on branch '{target_branch_name}'.",
                file=sys.stderr,
            )
            if restore_original_branch:
                print(
                    f"Attempting to switch back to '{restore_original_branch}' due to commit failure.",
                    file=sys.stdout,
                )
                if not self._switch_to_branch(restore_original_branch):
                    print(
                        f"Critical Error: Failed to restore original branch '{restore_original_branch}' after commit failure.",
                        file=sys.stderr,
                    )
            return False
        # _add_and_commit_memory_file prints "No changes to commit..." if that's the case, which is fine.
        print(
            f"Memory file successfully processed (committed or no changes) on branch '{target_branch_name}'.",
            file=sys.stdout,
        )

        # 3. Push Changes to Remote
        if push_changes:
            print(
                f"Attempting to push memory branch '{target_branch_name}' to remote.",
                file=sys.stdout,
            )
            if not self._push_memory_branch_to_remote(target_branch_name):
                # This is a warning, not a failure of the whole process if local commit succeeded.
                print(
                    f"Warning: Failed to push memory branch '{target_branch_name}' to remote. Changes are saved locally.",
                    file=sys.stderr,
                )
            else:
                print(
                    f"Successfully pushed memory branch '{target_branch_name}' to remote.",
                    file=sys.stdout,
                )
        else:
            print("Skipping push to remote as per configuration.", file=sys.stdout)

        # 4. Restore Original Branch (Optional)
        if (
            restore_original_branch
            and restore_original_branch != self._get_current_branch()
        ):
            # self._get_current_branch() should be target_branch_name here
            print(
                f"Attempting to switch back to original branch '{restore_original_branch}'.",
                file=sys.stdout,
            )
            if not self._switch_to_branch(restore_original_branch):
                current_branch_after_fail = self._get_current_branch()
                print(
                    f"Critical Error: Failed to switch back to original branch '{restore_original_branch}' after memory sync. Repository is currently on '{current_branch_after_fail}'.",
                    file=sys.stderr,
                )
                return False
            print(
                f"Successfully switched back to original branch '{restore_original_branch}'.",
                file=sys.stdout,
            )
        elif (
            restore_original_branch
            and restore_original_branch == self._get_current_branch()
        ):
            print(
                f"Already on the original branch '{restore_original_branch}'. No switch back needed.",
                file=sys.stdout,
            )

        print(
            f"Shutdown sync for memory branch '{target_branch_name}' completed.",
            file=sys.stdout,
        )
        return True
