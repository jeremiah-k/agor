"""
Input validation functions for AGOR.
"""

import re
import urllib.parse
from pathlib import Path
from typing import List, Optional

from .constants import SUPPORTED_COMPRESSION_FORMATS
from .exceptions import ValidationError


def validate_repository_url(repo_url: str) -> str:
    """
    Validate and normalize repository URL.

    Args:
        repo_url: Repository URL or GitHub shorthand (user/repo)

    Returns:
        Normalized repository URL

    Raises:
        ValidationError: If the repository URL is invalid
    """
    if not repo_url or not repo_url.strip():
        raise ValidationError("Repository URL cannot be empty")

    repo_url = repo_url.strip()

    # Check for local paths first
    if repo_url.startswith(("/", "./", "../")) or Path(repo_url).exists():
        # This is a local path, return as-is
        return repo_url

    # Check for SSH URLs (git@host:user/repo.git)
    ssh_pattern = r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+:[a-zA-Z0-9._/-]+(?:\.git)?$"
    if re.match(ssh_pattern, repo_url):
        return repo_url

    # Check for GitHub shorthand (user/repo)
    github_shorthand_pattern = r"^[a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+$"
    if re.match(github_shorthand_pattern, repo_url):
        return f"https://github.com/{repo_url}.git"

    # Validate full URLs
    try:
        parsed = urllib.parse.urlparse(repo_url)
        if not parsed.scheme or not parsed.netloc:
            raise ValidationError(f"Invalid repository URL: {repo_url}")

        # Check for common git hosting patterns
        valid_schemes = ["http", "https", "git", "ssh"]
        if parsed.scheme not in valid_schemes:
            raise ValidationError(f"Unsupported URL scheme: {parsed.scheme}")

        return repo_url

    except Exception as e:
        raise ValidationError(f"Invalid repository URL: {repo_url} - {e}") from e


def validate_local_repository(repo_path: str) -> Path:
    """
    Validate local repository path.

    Args:
        repo_path: Local path to git repository

    Returns:
        Validated Path object

    Raises:
        ValidationError: If the path is invalid or not a git repository
    """
    if not repo_path or not repo_path.strip():
        raise ValidationError("Repository path cannot be empty")

    path = Path(repo_path.strip()).resolve()

    if not path.exists():
        raise ValidationError(f"Path does not exist: {path}")

    if not path.is_dir():
        raise ValidationError(f"Path is not a directory: {path}")

    # Check if it's a git repository
    git_dir = path / ".git"
    if not git_dir.exists():
        raise ValidationError(f"Not a git repository: {path}")

    return path


def validate_branch_name(branch_name: str) -> str:
    """
    Validate git branch name according to git naming rules.

    Args:
        branch_name: Branch name to validate

    Returns:
        Validated branch name

    Raises:
        ValidationError: If the branch name is invalid
    """
    if not branch_name or not branch_name.strip():
        raise ValidationError("Branch name cannot be empty")

    branch_name = branch_name.strip()

    # Git branch naming rules
    invalid_patterns = [
        r"\.\.",
        r"@{",
        r"\\",
        r"\s",
        r"~",
        r"\^",
        r":",
        r"\?",
        r"\*",
        r"\[",
        r"^\.",
        r"\.$",
        r"^-",
        r"/$",
        r"//",
        r"^@$",
    ]

    for pattern in invalid_patterns:
        if re.search(pattern, branch_name):
            raise ValidationError(f"Invalid branch name: {branch_name}")

    # Additional checks
    if len(branch_name) > 250:  # Reasonable limit
        raise ValidationError("Branch name too long (max 250 characters)")

    return branch_name


def validate_branch_list(branches: Optional[List[str]]) -> List[str]:
    """
    Validate a list of branch names.

    Args:
        branches: List of branch names to validate

    Returns:
        List of validated branch names

    Raises:
        ValidationError: If any branch name is invalid
    """
    if not branches:
        return []

    validated_branches = []
    for branch in branches:
        validated_branches.append(validate_branch_name(branch))

    return validated_branches


def validate_compression_format(format_name: str) -> str:
    """
    Validate compression format.

    Args:
        format_name: Compression format name

    Returns:
        Validated format name

    Raises:
        ValidationError: If the format is not supported
    """
    if not format_name or not format_name.strip():
        raise ValidationError("Compression format cannot be empty")

    format_name = format_name.strip().lower()

    if format_name not in SUPPORTED_COMPRESSION_FORMATS:
        raise ValidationError(
            f"Unsupported compression format: {format_name}. "
            f"Supported formats: {', '.join(SUPPORTED_COMPRESSION_FORMATS)}"
        )

    return format_name


def validate_file_path(file_path: str, must_exist: bool = True) -> Path:
    """
    Validate file path.

    Args:
        file_path: File path to validate
        must_exist: Whether the file must already exist

    Returns:
        Validated Path object

    Raises:
        ValidationError: If the path is invalid
    """
    if not file_path or not file_path.strip():
        raise ValidationError("File path cannot be empty")

    path = Path(file_path.strip()).resolve()

    if must_exist and not path.exists():
        raise ValidationError(f"File does not exist: {path}")

    if must_exist and not path.is_file():
        raise ValidationError(f"Path is not a file: {path}")

    return path
