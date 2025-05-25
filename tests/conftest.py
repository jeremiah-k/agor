"""
Pytest configuration and fixtures for AGOR tests.
"""

import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_dir():
    """Provide a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def sample_repo_url():
    """Provide a sample repository URL for tests."""
    return "https://github.com/user/sample-repo.git"


@pytest.fixture
def sample_local_path(temp_dir):
    """Provide a sample local repository path for tests."""
    repo_path = temp_dir / "sample-repo"
    repo_path.mkdir()

    # Create a minimal git repository structure
    git_dir = repo_path / ".git"
    git_dir.mkdir()

    # Create some sample files
    (repo_path / "README.md").write_text("# Sample Repository")
    (repo_path / "src").mkdir()
    (repo_path / "src" / "main.py").write_text("print('Hello, World!')")

    return repo_path
