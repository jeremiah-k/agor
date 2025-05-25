"""
Tests for AGOR bundler module.
"""

import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from agor.bundler import BundleBuilder, create_bundle


class TestBundleBuilder:
    """Test the BundleBuilder class."""

    def test_init_with_defaults(self):
        """Test bundle builder initialization with default values."""
        builder = BundleBuilder("https://github.com/user/repo.git")

        assert builder.repo_url == "https://github.com/user/repo.git"
        assert builder.depth == 5  # default from settings
        assert builder.branches is None
        assert builder.compression_format == "zip"  # default from settings
        assert builder.preserve_history is False
        assert builder.main_only is False

    def test_init_with_custom_values(self):
        """Test bundle builder initialization with custom values."""
        builder = BundleBuilder(
            "https://github.com/user/repo.git",
            depth=10,
            branches=["main", "develop"],
            compression_format="gz",
            preserve_history=True,
            main_only=True,
        )

        assert builder.depth == 10
        assert builder.branches == ["main", "develop"]
        assert builder.compression_format == "gz"
        assert builder.preserve_history is True
        assert builder.main_only is True

    @pytest.mark.asyncio
    async def test_bundle_creation_workflow(self):
        """Test the complete bundle creation workflow."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            output_path = temp_path / "test_bundle.zip"

            builder = BundleBuilder("https://github.com/user/repo.git")

            # Mock the internal methods to avoid actual git operations
            with patch.object(builder, "_clone_repository") as mock_clone, patch.object(
                builder, "_get_branches_to_include"
            ) as mock_branches, patch.object(
                builder, "_prepare_bundle_directory"
            ) as mock_prepare, patch.object(
                builder, "_add_agor_tools"
            ) as mock_tools, patch.object(
                builder, "_create_archive"
            ) as mock_archive:

                # Setup mocks
                mock_clone.return_value = temp_path / "repo"
                mock_branches.return_value = ["main"]
                mock_prepare.return_value = temp_path / "bundle"
                mock_archive.return_value = output_path

                # Run bundle creation
                result = await builder.bundle(output_path)

                # Verify result
                assert result == output_path

                # Verify method calls
                mock_clone.assert_called_once()
                mock_branches.assert_called_once()
                mock_prepare.assert_called_once()
                mock_tools.assert_called_once()
                mock_archive.assert_called_once()


class TestCreateBundleFunction:
    """Test the create_bundle convenience function."""

    @pytest.mark.asyncio
    async def test_create_bundle_with_defaults(self):
        """Test create_bundle function with default parameters."""
        with patch("agor.bundler.BundleBuilder") as mock_builder_class:
            mock_builder = Mock()
            mock_builder.bundle.return_value = Path("test_bundle.zip")
            mock_builder_class.return_value = mock_builder

            result = await create_bundle("https://github.com/user/repo.git")

            # Verify builder was created and bundle was called
            mock_builder_class.assert_called_once_with(
                "https://github.com/user/repo.git"
            )
            mock_builder.bundle.assert_called_once_with(None)
            assert result == Path("test_bundle.zip")

    @pytest.mark.asyncio
    async def test_create_bundle_with_custom_options(self):
        """Test create_bundle function with custom options."""
        with patch("agor.bundler.BundleBuilder") as mock_builder_class:
            mock_builder = Mock()
            mock_builder.bundle.return_value = Path("custom_bundle.gz")
            mock_builder_class.return_value = mock_builder

            output_path = Path("custom_bundle.gz")
            result = await create_bundle(
                "https://github.com/user/repo.git",
                output_path=output_path,
                compression_format="gz",
                depth=10,
            )

            # Verify builder was created with custom options
            mock_builder_class.assert_called_once_with(
                "https://github.com/user/repo.git", compression_format="gz", depth=10
            )
            mock_builder.bundle.assert_called_once_with(output_path)
            assert result == Path("custom_bundle.gz")
