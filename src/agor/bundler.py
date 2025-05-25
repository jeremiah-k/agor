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

        # Capture current git configuration and create agent manifest
        await self._capture_git_config(tools_dir)
        await self._create_agent_manifest(tools_dir)

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
        import json
        import subprocess

        git_config = {
            "user_name": None,
            "user_email": None,
            "captured_at": None,
            "environment_vars": {},
            "setup_script": None,
        }

        try:
            # Get current git configuration
            try:
                git_config["user_name"] = subprocess.check_output(
                    ["git", "config", "user.name"], stderr=subprocess.DEVNULL, text=True
                ).strip()
            except subprocess.CalledProcessError:
                pass

            try:
                git_config["user_email"] = subprocess.check_output(
                    ["git", "config", "user.email"],
                    stderr=subprocess.DEVNULL,
                    text=True,
                ).strip()
            except subprocess.CalledProcessError:
                pass

            # Capture environment variables that might be relevant
            import os

            env_vars = [
                "GIT_AUTHOR_NAME",
                "GIT_USER_NAME",
                "GIT_COMMITTER_NAME",
                "GIT_AUTHOR_EMAIL",
                "GIT_USER_EMAIL",
                "GIT_COMMITTER_EMAIL",
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
                git_config[
                    "setup_script"
                ] = f"""#!/bin/bash
# Git configuration captured during bundle creation
# Run this script to apply the same git configuration

echo "🔧 Setting up git configuration from bundle..."
git config user.name "{git_config["user_name"]}"
git config user.email "{git_config["user_email"]}"
echo "✅ Git configured as: {git_config["user_name"]} <{git_config["user_email"]}>"
echo "🚀 Ready for development!"
"""

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
                    email=git_config["user_email"],
                )
            else:
                log.warning("No git configuration found to capture")

        except Exception as e:
            log.warning("Failed to capture git configuration", error=str(e))

    async def _create_agent_manifest(self, tools_dir: Path) -> None:
        """Create comprehensive agent manifest with all essential information."""
        import json
        import platform
        import subprocess
        from datetime import datetime

        from .. import __version__
        from ..constants import PROTOCOL_VERSION

        manifest = {
            "agor_version": __version__,
            "protocol_version": PROTOCOL_VERSION,
            "bundle_created_at": datetime.now().isoformat(),
            "bundle_creator": {
                "platform": platform.system(),
                "python_version": platform.python_version(),
                "hostname": platform.node(),
            },
            "git_configuration": {},
            "environment_info": {},
            "project_info": {},
            "available_tools": [],
            "setup_instructions": [],
            "quick_start_commands": [],
        }

        try:
            # Load git configuration if available
            git_config_file = tools_dir / "git_config.json"
            if git_config_file.exists():
                with open(git_config_file, "r") as f:
                    manifest["git_configuration"] = json.load(f)

            # Gather environment information
            manifest["environment_info"] = {
                "working_directory": str(Path.cwd()),
                "bundle_format": self.compression_format,
                "preserve_history": self.preserve_history,
                "main_only": self.main_only,
                "git_binary_included": True,
                "sqlite_available": (tools_dir / "sqlite3").exists()
                or (tools_dir / "sqlite_memory.py").exists(),
            }

            # Try to gather project information
            try:
                # Get repository information
                repo_root = subprocess.check_output(
                    ["git", "rev-parse", "--show-toplevel"],
                    stderr=subprocess.DEVNULL,
                    text=True,
                ).strip()

                repo_name = Path(repo_root).name
                current_branch = subprocess.check_output(
                    ["git", "branch", "--show-current"],
                    stderr=subprocess.DEVNULL,
                    text=True,
                ).strip()

                # Get recent commits
                recent_commits = (
                    subprocess.check_output(
                        ["git", "log", "--oneline", "-5"],
                        stderr=subprocess.DEVNULL,
                        text=True,
                    )
                    .strip()
                    .split("\n")
                )

                manifest["project_info"] = {
                    "repository_name": repo_name,
                    "current_branch": current_branch,
                    "recent_commits": recent_commits,
                    "repository_root": repo_root,
                }

            except subprocess.CalledProcessError:
                manifest["project_info"] = {
                    "repository_name": "Unknown",
                    "current_branch": "Unknown",
                    "note": "Not a git repository or git not available",
                }

            # List available tools
            tool_files = [
                "git",
                "git_setup.py",
                "code_exploration.py",
                "sqlite_memory.py",
                "agent_prompt_templates.py",
                "handoff_templates.py",
                "project_planning_templates.py",
                "README_ai.md",
            ]

            for tool in tool_files:
                tool_path = tools_dir / tool
                if tool_path.exists():
                    manifest["available_tools"].append(
                        {
                            "name": tool,
                            "path": f"/tmp/agor_tools/{tool}",
                            "executable": tool_path.is_file()
                            and tool_path.stat().st_mode & 0o111,
                            "description": self._get_tool_description(tool),
                        }
                    )

            # Setup instructions
            git_config = manifest["git_configuration"]
            if git_config.get("user_name") and git_config.get("user_email"):
                manifest["setup_instructions"] = [
                    "1. Apply git configuration: python /tmp/agor_tools/git_setup.py --apply-bundle",
                    "2. Verify git setup: python /tmp/agor_tools/git_setup.py --show",
                    "3. Make git binary executable: chmod 755 /tmp/agor_tools/git",
                    "4. Read full instructions: cat /tmp/agor_tools/README_ai.md",
                ]

                manifest["quick_start_commands"] = [
                    "python /tmp/agor_tools/git_setup.py --apply-bundle",
                    "chmod 755 /tmp/agor_tools/git",
                    "/tmp/agor_tools/git status",
                ]
            else:
                manifest["setup_instructions"] = [
                    "1. Set up git configuration manually or from environment",
                    "2. Make git binary executable: chmod 755 /tmp/agor_tools/git",
                    "3. Configure git: python /tmp/agor_tools/git_setup.py --set 'Your Name' 'your@email.com'",
                    "4. Read full instructions: cat /tmp/agor_tools/README_ai.md",
                ]

                manifest["quick_start_commands"] = [
                    "chmod 755 /tmp/agor_tools/git",
                    "python /tmp/agor_tools/git_setup.py --show",
                    "python /tmp/agor_tools/git_setup.py --set 'Your Name' 'your@email.com'",
                ]

            # Save manifest
            manifest_file = tools_dir / "agent_manifest.json"
            with open(manifest_file, "w") as f:
                json.dump(manifest, f, indent=2)

            # Create human-readable manifest
            readable_manifest = self._create_readable_manifest(manifest)
            readable_file = tools_dir / "AGENT_MANIFEST.md"
            with open(readable_file, "w") as f:
                f.write(readable_manifest)

            log.info(
                "Created agent manifest",
                tools_count=len(manifest["available_tools"]),
                git_configured=bool(git_config.get("user_name")),
            )

        except Exception as e:
            log.warning("Failed to create agent manifest", error=str(e))

    def _get_tool_description(self, tool_name: str) -> str:
        """Get description for a tool."""
        descriptions = {
            "git": "Portable git binary for version control operations",
            "git_setup.py": "Git configuration management and setup",
            "code_exploration.py": "Advanced code analysis and exploration tools",
            "sqlite_memory.py": "SQLite-based memory management system",
            "agent_prompt_templates.py": "Standardized prompt templates for agents",
            "handoff_templates.py": "Agent handoff and coordination templates",
            "project_planning_templates.py": "Project planning and breakdown templates",
            "README_ai.md": "Complete AI agent instructions and protocol",
        }
        return descriptions.get(tool_name, "AGOR tool")

    def _create_readable_manifest(self, manifest: dict) -> str:
        """Create human-readable version of the manifest."""
        git_config = manifest["git_configuration"]
        project_info = manifest["project_info"]

        readable = f"""# 🤖 AGOR Agent Manifest

**Bundle Created**: {manifest['bundle_created_at']}
**AGOR Version**: {manifest['agor_version']}
**Protocol Version**: {manifest['protocol_version']}
**Project**: {project_info.get('repository_name', 'Unknown')}
**Current Branch**: {project_info.get('current_branch', 'Unknown')}

## 🔧 Git Configuration

"""

        if git_config.get("user_name") and git_config.get("user_email"):
            readable += f"""**Ready to apply**: Git configuration captured from bundle creator
- **Name**: {git_config['user_name']}
- **Email**: {git_config['user_email']}
- **Captured**: {git_config.get('captured_at', 'Unknown')}

**Quick Setup**: `python /tmp/agor_tools/git_setup.py --apply-bundle`
"""
        else:
            readable += """**Manual setup required**: No git configuration captured

**Setup Options**:
- Environment: `python /tmp/agor_tools/git_setup.py --import-env`
- Manual: `python /tmp/agor_tools/git_setup.py --set "Your Name" "your@email.com"`
"""

        readable += """

## 🛠️ Available Tools

"""

        for tool in manifest["available_tools"]:
            executable_marker = " (executable)" if tool["executable"] else ""
            readable += (
                f"- **{tool['name']}**{executable_marker}: {tool['description']}\n"
            )

        readable += """

## 🚀 Quick Start

"""

        for i, cmd in enumerate(manifest["quick_start_commands"], 1):
            readable += f"{i}. `{cmd}`\n"

        readable += """

## 📋 Setup Instructions

"""

        for instruction in manifest["setup_instructions"]:
            readable += f"- {instruction}\n"

        readable += f"""

## 📊 Environment Info

- **Bundle Format**: {manifest['environment_info']['bundle_format']}
- **Git Binary**: {'✅ Included' if manifest['environment_info']['git_binary_included'] else '❌ Missing'}
- **SQLite Available**: {'✅ Yes' if manifest['environment_info']['sqlite_available'] else '❌ No'}
- **Preserve History**: {'✅ Yes' if manifest['environment_info']['preserve_history'] else '❌ No'}
- **Main Only**: {'✅ Yes' if manifest['environment_info']['main_only'] else '❌ No (all branches)'}

---

**For complete instructions, read**: `/tmp/agor_tools/README_ai.md`
"""

        return readable

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
