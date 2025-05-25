"""
Tests for AGOR validation module.
"""

import pytest

from agor.exceptions import ValidationError
from agor.validation import (
    validate_branch_name,
    validate_compression_format,
    validate_repository_url,
)


class TestRepositoryUrlValidation:
    """Test repository URL validation."""

    def test_valid_https_url(self):
        """Test valid HTTPS repository URLs."""
        valid_urls = [
            "https://github.com/user/repo.git",
            "https://github.com/user/repo",
            "https://gitlab.com/user/repo.git",
        ]

        for url in valid_urls:
            result = validate_repository_url(url)
            assert result == url

    def test_valid_ssh_url(self):
        """Test valid SSH repository URLs."""
        valid_urls = [
            "git@github.com:user/repo.git",
            "ssh://git@github.com/user/repo.git",
        ]

        for url in valid_urls:
            result = validate_repository_url(url)
            assert result == url

    def test_valid_local_path(self):
        """Test valid local repository paths."""
        valid_paths = [
            "/path/to/repo",
            "./relative/path",
            "../parent/path",
        ]

        for path in valid_paths:
            result = validate_repository_url(path)
            assert result == path

    def test_invalid_url(self):
        """Test invalid repository URLs."""
        invalid_urls = [
            "",
            "not-a-url",
            "http://",
            "ftp://example.com/repo",
        ]

        for url in invalid_urls:
            with pytest.raises(ValidationError):
                validate_repository_url(url)


class TestBranchNameValidation:
    """Test branch name validation."""

    def test_valid_branch_names(self):
        """Test valid branch names."""
        valid_names = [
            "main",
            "feature/new-feature",
            "bugfix-123",
            "release/v1.0.0",
        ]

        for name in valid_names:
            result = validate_branch_name(name)
            assert result == name

    def test_invalid_branch_names(self):
        """Test invalid branch names."""
        invalid_names = [
            "",
            "branch with spaces",
            "branch..with..dots",
            "branch/with/../dots",
        ]

        for name in invalid_names:
            with pytest.raises(ValidationError):
                validate_branch_name(name)


class TestCompressionFormatValidation:
    """Test compression format validation."""

    def test_valid_formats(self):
        """Test valid compression formats."""
        valid_formats = ["zip", "gz", "bz2"]

        for fmt in valid_formats:
            result = validate_compression_format(fmt)
            assert result == fmt

    def test_invalid_formats(self):
        """Test invalid compression formats."""
        invalid_formats = ["", "rar", "7z", "invalid"]

        for fmt in invalid_formats:
            with pytest.raises(ValidationError):
                validate_compression_format(fmt)
