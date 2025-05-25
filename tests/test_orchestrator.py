"""
Tests for AGOR orchestrator module.
"""

import asyncio
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from agor.orchestrator import Orchestrator, create_bundle


class TestOrchestrator:
    """Test the Orchestrator class."""
    
    def test_init_with_defaults(self):
        """Test orchestrator initialization with default values."""
        orchestrator = Orchestrator("https://github.com/user/repo.git")
        
        assert orchestrator.repo_url == "https://github.com/user/repo.git"
        assert orchestrator.depth == 5  # default from settings
        assert orchestrator.branches is None
        assert orchestrator.compression_format == "zip"  # default from settings
        assert orchestrator.preserve_history is False
        assert orchestrator.main_only is False
    
    def test_init_with_custom_values(self):
        """Test orchestrator initialization with custom values."""
        orchestrator = Orchestrator(
            "https://github.com/user/repo.git",
            depth=10,
            branches=["main", "develop"],
            compression_format="gz",
            preserve_history=True,
            main_only=True,
        )
        
        assert orchestrator.depth == 10
        assert orchestrator.branches == ["main", "develop"]
        assert orchestrator.compression_format == "gz"
        assert orchestrator.preserve_history is True
        assert orchestrator.main_only is True
    
    @pytest.mark.asyncio
    async def test_bundle_creation_workflow(self):
        """Test the complete bundle creation workflow."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            output_path = temp_path / "test_bundle.zip"
            
            orchestrator = Orchestrator("https://github.com/user/repo.git")
            
            # Mock the internal methods to avoid actual git operations
            with patch.object(orchestrator, '_clone_repository') as mock_clone, \
                 patch.object(orchestrator, '_get_branches_to_include') as mock_branches, \
                 patch.object(orchestrator, '_prepare_bundle_directory') as mock_prepare, \
                 patch.object(orchestrator, '_add_agor_tools') as mock_tools, \
                 patch.object(orchestrator, '_create_archive') as mock_archive:
                
                # Setup mocks
                mock_clone.return_value = temp_path / "repo"
                mock_branches.return_value = ["main"]
                mock_prepare.return_value = temp_path / "bundle"
                mock_archive.return_value = output_path
                
                # Run bundle creation
                result = await orchestrator.bundle(output_path)
                
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
        with patch('agor.orchestrator.Orchestrator') as mock_orchestrator_class:
            mock_orchestrator = Mock()
            mock_orchestrator.bundle.return_value = Path("test_bundle.zip")
            mock_orchestrator_class.return_value = mock_orchestrator
            
            result = await create_bundle("https://github.com/user/repo.git")
            
            # Verify orchestrator was created and bundle was called
            mock_orchestrator_class.assert_called_once_with("https://github.com/user/repo.git")
            mock_orchestrator.bundle.assert_called_once_with(None)
            assert result == Path("test_bundle.zip")
    
    @pytest.mark.asyncio
    async def test_create_bundle_with_custom_options(self):
        """Test create_bundle function with custom options."""
        with patch('agor.orchestrator.Orchestrator') as mock_orchestrator_class:
            mock_orchestrator = Mock()
            mock_orchestrator.bundle.return_value = Path("custom_bundle.gz")
            mock_orchestrator_class.return_value = mock_orchestrator
            
            output_path = Path("custom_bundle.gz")
            result = await create_bundle(
                "https://github.com/user/repo.git",
                output_path=output_path,
                compression_format="gz",
                depth=10
            )
            
            # Verify orchestrator was created with custom options
            mock_orchestrator_class.assert_called_once_with(
                "https://github.com/user/repo.git",
                compression_format="gz",
                depth=10
            )
            mock_orchestrator.bundle.assert_called_once_with(output_path)
            assert result == Path("custom_bundle.gz")
