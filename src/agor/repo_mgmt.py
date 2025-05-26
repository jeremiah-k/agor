import os
import shutil
import subprocess
import tarfile
import tempfile
from pathlib import Path
from urllib.parse import urlparse

from plumbum.cmd import git
from tqdm import tqdm

from .settings import settings


def is_github_url(value: str) -> bool:
    if Path(value).exists() and Path(value).is_dir():
        return False
    parsed = urlparse(value)
    if parsed.netloc == "github.com" and parsed.scheme in ["http", "https"]:
        return True
    # Check for shorthand notation
    elif "/" in value and not parsed.scheme and not parsed.netloc:
        return True
    return False


def valid_git_repo(value: str) -> str:
    if (
        Path(value).exists()
        and Path(value).is_dir()
        and (Path(value) / ".git").is_dir()
    ):
        return value
    elif is_github_url(str(value)):
        if "github.com" not in str(value):
            # Convert shorthand to full URL
            value = f"https://github.com/{value}"
        return value
    else:
        raise ValueError(
            f"'{value}' is neither an existing directory nor a valid GitHub URL."
        )


def get_clone_url(val: str) -> str:
    """
    Returns the URL to clone the repo.
    """
    if Path(val).exists() and Path(val).is_dir():
        # file:// makes --depth work on local clones
        return f"file://{Path(val).resolve()}"
    elif is_github_url(val):
        if "github.com" not in val:
            return f"https://github.com/{val}.git"
        else:
            return f"{val}.git"
    else:
        raise ValueError(f"'{val}' is not a valid GitHub URL.")


def clone_git_repo_to_temp_dir(
    git_repo: str,
    shallow: bool = True,
    branch: str = None,
    all_branches: bool = False,
    branches: list = None,
    main_only: bool = False,
) -> Path:
    is_local = True
    if is_github_url(git_repo):
        # Clone the repo to a temporary directory
        local_repo = Path(tempfile.mkdtemp())
        is_local = False
    else:
        local_repo = Path(git_repo)

        # Ensure the directory exists and contains a .git folder
        if not local_repo.exists() or not local_repo.is_dir():
            raise ValueError(f"'{local_repo}' is not a valid directory.")
        if not (local_repo / ".git").exists():
            raise ValueError(f"'{local_repo}' does not contain a .git folder.")

    # Create a temporary directory
    temp_dir = Path(tempfile.mkdtemp())

    # Clone the git repo to the temporary directory
    clone_command = ["clone"]

    # Handle branch selection with new simplified logic
    if main_only:
        # Clone only main/master branch
        if shallow:
            clone_command.extend(["--depth", str(settings.default_shallow_depth)])
        # Try to determine main/master branch
        if is_local:
            # For local repos, check what the default branch is
            try:
                default_branch = (
                    git["symbolic-ref", "refs/remotes/origin/HEAD"](
                        cwd=local_repo.resolve()
                    )
                    .strip()
                    .split("/")[-1]
                )
            except (OSError, subprocess.CalledProcessError):
                # Fallback to common default branches
                try:
                    git["show-ref", "--verify", "--quiet", "refs/heads/main"](
                        cwd=local_repo.resolve()
                    )
                    default_branch = "main"
                except (OSError, subprocess.CalledProcessError):
                    default_branch = "master"
        else:
            # For remote repos, try to get default branch
            try:
                head_ref = git[
                    "ls-remote", "--symref", get_clone_url(git_repo), "HEAD"
                ]()
                default_branch = "main"  # Default fallback
                for line in head_ref.splitlines():
                    if "ref:" in line and "HEAD" in line:
                        parts = line.split()
                        if len(parts) >= 2:
                            ref_path = parts[1]
                            default_branch = ref_path.split("/")[-1]
                            break
            except (OSError, subprocess.CalledProcessError):
                default_branch = "main"

        print(f"Cloning only main/master branch: {default_branch}")
        clone_command.extend(["--branch", default_branch])
    elif branches and len(branches) > 0:
        # Clone main/master plus additional branches - use all branches approach for simplicity
        print(f"Cloning main/master plus additional branches: {branches}")
        clone_command.append("--bare")
        all_branches = True  # Set flag for later processing
    elif all_branches:
        # For all branches, we need to fetch everything
        print("Cloning all branches with --bare option")
        # Using --bare instead of --mirror for better compatibility
        clone_command.append("--bare")
    elif shallow:
        # Default behavior (current branch for local repos or default branch for remote repos)
        clone_command.extend(["--depth", str(settings.default_shallow_depth)])
        if is_local:
            checked_out_branch = git["rev-parse", "--abbrev-ref", "HEAD"](
                cwd=local_repo.resolve()
            ).strip()
            if checked_out_branch:
                print(
                    f"Cloning default branch: {checked_out_branch} (current branch in local repo)"
                )
                clone_command.extend(["--branch", checked_out_branch])
        else:
            # For remote repos, try to determine the default branch
            try:
                # Use ls-remote to get the HEAD reference without needing a local clone
                head_ref = git[
                    "ls-remote", "--symref", get_clone_url(git_repo), "HEAD"
                ]()
                # Parse the output to get the default branch name
                default_branch = None
                for line in head_ref.splitlines():
                    if "ref:" in line and "HEAD" in line:
                        # Format is typically: ref: refs/heads/main\tHEAD
                        parts = line.split()
                        if len(parts) >= 2:
                            ref_path = parts[1]
                            default_branch = ref_path.split("/")[-1]
                            break

                if default_branch:
                    print(
                        f"Cloning default branch from remote repository: {default_branch}"
                    )
                else:
                    print(
                        "Cloning default branch from remote repository (branch name could not be determined)"
                    )
            except Exception as e:
                print(
                    f"Cloning default branch from remote repository (error determining branch name: {e})"
                )

    clone_command.extend(
        [
            get_clone_url(git_repo),
            str(temp_dir),
        ]
    )
    git[clone_command]()

    # If multiple branches were specified, fetch them after the initial clone
    if branches and len(branches) > 1 and not all_branches:
        print("Fetching additional branches after initial clone")
        for additional_branch in branches[1:]:
            if additional_branch:
                print(f"Fetching branch: {additional_branch}")
                git["fetch", "origin", additional_branch](cwd=temp_dir)
                # Create local branch tracking the remote branch
                print(f"Creating local branch for: {additional_branch}")
                git["checkout", "-b", additional_branch, f"origin/{additional_branch}"](
                    cwd=temp_dir
                )

        # Return to the first branch
        if branches[0]:
            print(f"Returning to first branch: {branches[0]}")
            git["checkout", branches[0]](cwd=temp_dir)

    # If all branches were specified, convert bare repo to normal repo with all branches
    if all_branches:
        print("Converting bare repo to normal repo with all branches")
        try:
            # List all remote branches
            try:
                # For bare repos, we need to use a different approach to list branches
                branches_output = git[
                    "for-each-ref", "--format=%(refname:short)", "refs/heads/"
                ](cwd=temp_dir)
                if branches_output.strip():
                    print(f"Available branches in repository:\n{branches_output}")
                else:
                    # Try alternative method
                    branches_output = git["branch"](cwd=temp_dir)
                    if branches_output.strip():
                        print(f"Available branches in repository:\n{branches_output}")
                    else:
                        print(
                            "No branches found using standard methods, trying remote branches..."
                        )
                        branches_output = git[
                            "for-each-ref", "--format=%(refname:short)", "refs/remotes/"
                        ](cwd=temp_dir)
                        if branches_output.strip():
                            print(f"Available remote branches:\n{branches_output}")
                        else:
                            print("No branches found in repository")
                            branches_output = ""
            except Exception as e:
                print(f"Error listing branches: {e}")
                try:
                    # Try alternative method for listing branches
                    branches_output = git["show-ref", "--heads"](cwd=temp_dir)
                    print(f"Branches found using show-ref:\n{branches_output}")
                except Exception as e2:
                    print(f"Error listing branches with alternative method: {e2}")
                    branches_output = ""

            # Create a new temp directory for the full repo
            full_repo_dir = Path(tempfile.mkdtemp())

            # Clone the bare repo to a normal repo with all branches
            git["clone", str(temp_dir), str(full_repo_dir)]()

            # Fetch all branches
            try:
                git["fetch", "--all"](cwd=full_repo_dir)
                print("Successfully fetched all branches")
            except Exception as e:
                print(f"Error fetching all branches: {e}")

            # Get all branch names (strip origin/ prefix and remove HEAD)
            branch_lines = branches_output.strip().split("\n")
            branch_names = []
            for line in branch_lines:
                branch = line.strip()
                if branch and "HEAD" not in branch:
                    # Remove 'origin/' prefix
                    branch_name = branch.replace("origin/", "").strip()
                    if branch_name:  # Only add non-empty branch names
                        branch_names.append(branch_name)

            # Create local branches for all remote branches
            if branch_names:
                print(
                    f"Found {len(branch_names)} branches to process: {', '.join(branch_names)}"
                )
                for branch_name in branch_names:
                    try:
                        print(f"Creating local branch for: {branch_name}")
                        git["checkout", "-b", branch_name, f"origin/{branch_name}"](
                            cwd=full_repo_dir
                        )
                    except Exception as e:
                        # Check if the error is because the branch already exists
                        if "already exists" in str(e):
                            print(
                                f"Branch {branch_name} already exists, checking it out"
                            )
                            try:
                                # Just checkout the existing branch
                                git["checkout", branch_name](cwd=full_repo_dir)
                            except Exception as e2:
                                print(
                                    f"Error checking out existing branch {branch_name}: {e2}"
                                )
                        else:
                            print(f"Error creating branch {branch_name}: {e}")
            else:
                print("No valid branch names found to process")

            # Checkout the default branch (usually main or master)
            default_branch = "main"
            try:
                git["checkout", default_branch](cwd=full_repo_dir)
            except Exception:
                try:
                    git["checkout", "master"](cwd=full_repo_dir)
                except Exception as e:
                    print(f"Error checking out default branch: {e}")

            # Replace the temp_dir with the full repo dir
            shutil.rmtree(temp_dir)
            temp_dir = full_repo_dir
        except Exception as e:
            print(f"Error processing all branches: {e}")

    git["gc"](cwd=temp_dir)

    return temp_dir


def clone_repository(repo_url: str, target_path: Path, depth: int = None) -> None:
    """
    Clone a repository to a target path.

    Args:
        repo_url: URL or path of the repository to clone
        target_path: Path where to clone the repository
        depth: Depth for shallow clone (None for full clone)
    """
    # Use the existing clone_git_repo_to_temp_dir function but move result to target
    temp_dir = clone_git_repo_to_temp_dir(
        repo_url, shallow=depth is not None, main_only=False, all_branches=True
    )

    # Move the cloned repo to the target path
    if target_path.exists():
        shutil.rmtree(target_path)
    shutil.move(str(temp_dir), str(target_path))


def get_branches(repo_path: Path) -> list[str]:
    """
    Get list of all branches in a repository.

    Args:
        repo_path: Path to the git repository

    Returns:
        List of branch names
    """
    try:
        # Get all local branches
        result = git["branch", "-a"](cwd=repo_path)
        branches = []
        for line in result.strip().split("\n"):
            line = line.strip()
            if line and not line.startswith("*"):
                # Remove leading * and whitespace, and remote prefixes
                branch = line.replace("*", "").strip()
                if branch.startswith("remotes/origin/"):
                    branch = branch.replace("remotes/origin/", "")
                if branch and branch != "HEAD":
                    branches.append(branch)
            elif line.startswith("*"):
                # Current branch
                branch = line.replace("*", "").strip()
                if branch and branch != "HEAD":
                    branches.append(branch)

        # Remove duplicates and return
        return list(set(branches))
    except Exception as e:
        print(f"Error getting branches: {e}")
        return ["main"]  # Fallback to main branch


def tar_directory(path_to_directory: Path, compression="gz") -> Path:
    # Ensure the directory exists
    if not path_to_directory.exists() or not path_to_directory.is_dir():
        raise ValueError(f"'{path_to_directory}' is not a valid directory.")

    # Validate compression type
    if compression not in ["gz", "bz2"]:
        raise ValueError(
            f"Invalid compression type: {compression}. Choose from 'gz' or 'bz2'."
        )

    # Create a temporary tar file
    tar_fd, tar_file = tempfile.mkstemp(suffix=f".tar.{compression}")
    os.close(tar_fd)  # Close the file descriptor

    # Get the total number of files to compress for progress reporting
    total_files = sum(len(files) for _, _, files in os.walk(path_to_directory))

    with tarfile.open(tar_file, f"w:{compression}") as tar:
        with tqdm(
            total=total_files, desc=f"Compressing {path_to_directory.name}"
        ) as pbar:
            for root, _dirs, files in os.walk(path_to_directory):
                for file in files:
                    absolute_file_path = os.path.join(root, file)
                    relative_file_path = os.path.relpath(
                        absolute_file_path, path_to_directory
                    )
                    tar.add(absolute_file_path, arcname=relative_file_path)
                    pbar.update()

    return Path(tar_file)
