"""
Bundle creation service for AGOR.

Separates business logic from CLI interface to enable programmatic use
and better testing. Handles the complete bundle creation workflow.
"""

import shutil
import tempfile
from pathlib import Path
from typing import List, Optional

from .logging import get_logger
from .repo_mgmt import clone_repository, get_branches
from .settings import settings
from .utils import create_archive, download_file
from .validation import validate_repository_url

log = get_logger(__name__)


class BundleBuilder:
    """Main bundle creation service for AGOR."""

    def __init__(
        self,
        repo_url: str,
        *,
        depth: Optional[int] = None,
        branches: Optional[List[str]] = None,
        compression_format: Optional[str] = None,
        preserve_history: Optional[bool] = None,
        main_only: Optional[bool] = None,
    ):
        """Initialize bundle builder with repository and options.

        Args:
            repo_url: Repository URL or local path
            depth: Git clone depth (None for full history)
            branches: Specific branches to include
            compression_format: Archive format (zip, gz, bz2)
            preserve_history: Whether to preserve full git history
            main_only: Whether to include only main/master branch
        """
        self.repo_url = validate_repository_url(repo_url)
        self.depth = depth or settings.default_shallow_depth
        self.branches = branches
        self.compression_format = compression_format or settings.compression_format
        self.preserve_history = preserve_history or settings.preserve_history
        self.main_only = main_only or settings.main_only

        log.info(
            "BundleBuilder initialized",
            repo_url=self.repo_url,
            depth=self.depth,
            compression_format=self.compression_format,
            preserve_history=self.preserve_history,
            main_only=self.main_only,
        )

    async def bundle(self, output_path: Optional[Path] = None) -> Path:
        """Create a bundle of the repository.

        Args:
            output_path: Optional custom output path

        Returns:
            Path to the created bundle file

        Raises:
            ValueError: If repository URL is invalid
            RuntimeError: If bundle creation fails
        """
        log.info("Starting bundle creation", repo_url=self.repo_url)

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            try:
                # Clone repository
                repo_path = await self._clone_repository(temp_path)

                # Get branches to include
                branches_to_include = await self._get_branches_to_include(repo_path)

                # Prepare bundle directory
                bundle_dir = await self._prepare_bundle_directory(
                    temp_path, repo_path, branches_to_include
                )

                # Add AGOR tools
                await self._add_agor_tools(bundle_dir)

                # Create archive
                archive_path = await self._create_archive(bundle_dir, output_path)

                log.info("Bundle creation completed", archive_path=str(archive_path))
                return archive_path

            except Exception as e:
                log.error(
                    "Bundle creation failed", error=str(e), repo_url=self.repo_url
                )
                raise RuntimeError(f"Failed to create bundle: {e}") from e

    async def _clone_repository(self, temp_path: Path) -> Path:
        """Clone the repository to temporary directory."""
        log.info("Cloning repository", repo_url=self.repo_url, depth=self.depth)

        repo_path = temp_path / "repo"

        # For now, use synchronous clone (async implementation would go here)
        clone_repository(
            self.repo_url,
            repo_path,
            depth=None if self.preserve_history else self.depth,
        )

        return repo_path

    async def _get_branches_to_include(self, repo_path: Path) -> List[str]:
        """Determine which branches to include in the bundle."""
        if self.branches:
            log.info("Using specified branches", branches=self.branches)
            return self.branches

        if self.main_only:
            # Get main/master branch
            all_branches = get_branches(repo_path)
            main_branch = next(
                (b for b in all_branches if b in ["main", "master"]),
                all_branches[0] if all_branches else "main",
            )
            log.info("Using main branch only", branch=main_branch)
            return [main_branch]

        # Get all branches
        all_branches = get_branches(repo_path)
        log.info("Using all branches", branches=all_branches)
        return all_branches

    async def _prepare_bundle_directory(
        self, temp_path: Path, repo_path: Path, branches: List[str]
    ) -> Path:
        """Prepare the bundle directory with repository content."""
        bundle_dir = temp_path / "bundle"
        bundle_dir.mkdir()

        # Copy repository content
        project_dir = bundle_dir / "project"
        shutil.copytree(repo_path, project_dir)

        log.info(
            "Prepared bundle directory",
            bundle_dir=str(bundle_dir),
            branches_included=len(branches),
        )

        return bundle_dir

    async def _add_agor_tools(self, bundle_dir: Path) -> None:
        """Add AGOR tools and git binary to the bundle."""
        tools_dir = bundle_dir / "agor_tools"
        tools_dir.mkdir()

        # Copy AGOR tools
        agor_tools_src = Path(__file__).parent / "tools"
        if agor_tools_src.exists():
            shutil.copytree(agor_tools_src, tools_dir)

        # Capture current git configuration
        await self._capture_git_config(tools_dir)

        # Download git binary
        try:
            git_binary_path = tools_dir / "git"
            await self._download_git_binary(git_binary_path)
            git_binary_path.chmod(0o755)
            log.info("Added git binary to bundle", path=str(git_binary_path))
        except Exception as e:
            log.warning("Failed to add git binary", error=str(e))

    async def _capture_git_config(self, tools_dir: Path) -> None:
        """Capture current git configuration and save it for agents."""
        import subprocess
        import json

        git_config = {
            "user_name": None,
            "user_email": None,
            "captured_at": None,
            "environment_vars": {},
            "setup_script": None
        }

        try:
            # Get current git configuration
            try:
                git_config["user_name"] = subprocess.check_output(
                    ["git", "config", "user.name"],
                    stderr=subprocess.DEVNULL,
                    text=True
                ).strip()
            except subprocess.CalledProcessError:
                pass

            try:
                git_config["user_email"] = subprocess.check_output(
                    ["git", "config", "user.email"],
                    stderr=subprocess.DEVNULL,
                    text=True
                ).strip()
            except subprocess.CalledProcessError:
                pass

            # Capture environment variables that might be relevant
            import os
            env_vars = [
                "GIT_AUTHOR_NAME", "GIT_USER_NAME", "GIT_COMMITTER_NAME",
                "GIT_AUTHOR_EMAIL", "GIT_USER_EMAIL", "GIT_COMMITTER_EMAIL"
            ]

            for var in env_vars:
                value = os.getenv(var)
                if value:
                    git_config["environment_vars"][var] = value

            # Add timestamp
            from datetime import datetime
            git_config["captured_at"] = datetime.now().isoformat()

            # Generate setup script
            if git_config["user_name"] and git_config["user_email"]:
                git_config["setup_script"] = f'''#!/bin/bash
# Git configuration captured during bundle creation
# Run this script to apply the same git configuration

echo "🔧 Setting up git configuration from bundle..."
git config user.name "{git_config["user_name"]}"
git config user.email "{git_config["user_email"]}"
echo "✅ Git configured as: {git_config["user_name"]} <{git_config["user_email"]}>"
echo "🚀 Ready for development!"
'''

            # Save git configuration
            config_file = tools_dir / "git_config.json"
            with open(config_file, "w") as f:
                json.dump(git_config, f, indent=2)

            # Save setup script if we have configuration
            if git_config["setup_script"]:
                setup_script = tools_dir / "setup_git.sh"
                with open(setup_script, "w") as f:
                    f.write(git_config["setup_script"])
                setup_script.chmod(0o755)

                log.info(
                    "Captured git configuration",
                    name=git_config["user_name"],
                    email=git_config["user_email"]
                )
            else:
                log.warning("No git configuration found to capture")

        except Exception as e:
            log.warning("Failed to capture git configuration", error=str(e))

    async def _download_git_binary(self, output_path: Path) -> None:
        """Download the portable git binary."""
        log.info("Downloading git binary", url=settings.git_binary_url)

        # For now, use synchronous download (async implementation would go here)
        download_file(settings.git_binary_url, output_path)

    async def _create_archive(
        self, bundle_dir: Path, output_path: Optional[Path] = None
    ) -> Path:
        """Create the final archive file."""
        if output_path is None:
            output_path = Path.cwd() / f"agor_bundle.{self.compression_format}"

        log.info(
            "Creating archive",
            bundle_dir=str(bundle_dir),
            output_path=str(output_path),
            format=self.compression_format,
        )

        # For now, use synchronous archive creation
        create_archive(bundle_dir, output_path, self.compression_format)

        return output_path


# Convenience function for simple use cases
async def create_bundle(
    repo_url: str, output_path: Optional[Path] = None, **kwargs
) -> Path:
    """Create a bundle with default settings.

    Args:
        repo_url: Repository URL or local path
        output_path: Optional custom output path
        **kwargs: Additional options for BundleBuilder

    Returns:
        Path to the created bundle file
    """
    builder = BundleBuilder(repo_url, **kwargs)
    return await builder.bundle(output_path)
