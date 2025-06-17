"""
AGOR External Project Integration System

This module provides a standardized way to integrate AGOR tools with external projects
where AGOR is installed separately from the project being worked on.

Addresses critical issues:
1. Tool location and path resolution when AGOR is installed separately
2. Module import failures due to internal dependencies
3. Missing standardized integration workflow for external projects

Usage:
    from agor.tools.external_integration import AgorExternalTools

    # Initialize with automatic AGOR detection
    tools = AgorExternalTools()

    # Use AGOR functions with fallback support
    tools.generate_pr_description_output("PR content here")
    tools.create_development_snapshot("Title", "Context")
"""

import importlib.util
import logging
import os
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Callable, Dict, Optional


class AgorExternalTools:
    """
    External project integration for AGOR tools.

    Provides access to AGOR development functions with automatic fallback
    when AGOR tools are not available or have import issues.
    """

    def __init__(self, agor_path: Optional[str] = None):
        """
        Initializes the AGOR external tools integration, attempting to locate and load AGOR tools.
        
        If an explicit AGOR installation path is provided, it is used for detection; otherwise, automatic detection strategies are applied. Sets internal state flags for AGOR availability and fallback mode.
        """
        self.agor_path = agor_path
        self.agor_available = False
        self.dev_tools = None
        self.fallback_mode = False
        self.logger = logging.getLogger(__name__)

        # Attempt to initialize AGOR tools
        self._initialize_agor_tools()

    def _initialize_agor_tools(self):
        """
        Attempts to initialize AGOR tools using multiple detection strategies, enabling fallback mode if all methods fail.
        
        Tries direct import, path-based detection, and searching common installation locations in sequence. If none succeed, activates fallback mode to ensure continued functionality.
        """
        try:
            # Method 1: Try direct import (AGOR installed in same environment)
            self._try_direct_import()
            if self.agor_available:
                return

            # Method 2: Try path-based detection
            self._try_path_detection()
            if self.agor_available:
                return

            # Method 3: Try common installation locations
            self._try_common_locations()
            if self.agor_available:
                return

        except Exception as e:
            self.logger.warning(f"AGOR tools initialization failed: {e}")

        # If all methods fail, enable fallback mode
        self._enable_fallback_mode()

    def _try_direct_import(self):
        """
        Attempts to import AGOR development tools directly and sets availability flags on success.
        """
        try:
            import agor.tools.dev_tools as dev_tools

            self.dev_tools = dev_tools
            self.agor_available = True
            self.logger.info("AGOR tools loaded via direct import")
        except ImportError:
            pass

    def _try_path_detection(self):
        """
        Attempts to locate and load AGOR tools by searching specified or common installation paths.
        
        If a custom AGOR path is provided, it is checked first; otherwise, several standard directories are probed. On successful detection and loading, updates internal state to reflect AGOR availability.
        """
        if self.agor_path:
            search_paths = [Path(self.agor_path)]
        else:
            # Common locations where AGOR might be installed
            search_paths = [
                Path.home() / "agor",
                Path.home() / "dev" / "agor",
                Path("/opt/agor"),
                Path("/usr/local/agor"),
                Path.cwd().parent / "agor",  # Sibling directory
            ]

        for path in search_paths:
            if self._try_load_from_path(path):
                self.agor_path = str(path)
                self.agor_available = True
                self.logger.info(f"AGOR tools loaded from: {path}")
                return

    def _try_common_locations(self):
        """
        Attempts to locate and load AGOR tools from common Python site-packages directories.
        
        If AGOR is found and successfully loaded from any site-packages location, updates the internal state to reflect availability and records the path. Logs the outcome of the search.
        """
        # Look for AGOR in Python site-packages
        try:
            import site

            for site_dir in site.getsitepackages():
                agor_path = Path(site_dir) / "agor"
                if self._try_load_from_path(agor_path):
                    self.agor_path = str(agor_path)
                    self.agor_available = True
                    self.logger.info(
                        f"AGOR tools loaded from site-packages: {agor_path}"
                    )
                    return
        except (ImportError, OSError) as e:
            self.logger.debug(f"Site-packages probing failed: {e}")

    @contextmanager
    def _temp_sys_path(self, path: str):
        """
        Context manager that temporarily adds a directory to sys.path for module imports.
        
        Args:
            path: The directory to add to sys.path during the context.
        """
        sys.path.insert(0, path)
        try:
            yield
        finally:
            if path in sys.path:
                sys.path.remove(path)

    def _try_load_from_path(self, path: Path) -> bool:
        """
        Attempts to load the AGOR development tools module from a specified installation path.
        
        Returns:
            True if the module is successfully loaded and assigned; False otherwise.
        """
        try:
            dev_tools_path = path / "src" / "agor" / "tools" / "dev_tools.py"
            if not dev_tools_path.exists():
                return False

            # Add path to sys.path temporarily with context manager
            src_path = str(path / "src")
            with self._temp_sys_path(src_path):
                # Try to import dev_tools
                spec = importlib.util.spec_from_file_location(
                    "agor.tools.dev_tools", dev_tools_path
                )
                if spec is None or spec.loader is None:
                    return False

                dev_tools_module = importlib.util.module_from_spec(spec)
                # Insert module into sys.modules to prevent duplicate reloads
                sys.modules["agor.tools.dev_tools"] = dev_tools_module
                spec.loader.exec_module(dev_tools_module)

                self.dev_tools = dev_tools_module
                return True

        except Exception as e:
            self.logger.exception(f"Failed to load AGOR from {path}: {e}")
            return False

    def _enable_fallback_mode(self):
        """
        Enables fallback mode, activating manual implementations when AGOR tools are unavailable.
        
        Sets the fallback mode flag and logs warnings to indicate that limited functionality will be used.
        """
        self.fallback_mode = True
        self.logger.warning("AGOR tools not available - using fallback mode")
        self.logger.info("Some functions will have limited functionality")

    def _call_with_fallback(
        self, func_name: str, fallback_func: Callable, *args, **kwargs
    ):
        """
        Attempts to call a specified function from the AGOR tools module, falling back to a provided function if unavailable or if an error occurs.
        
        Args:
            func_name: Name of the AGOR function to call.
            fallback_func: Function to execute if the AGOR function is unavailable or fails.
            *args: Positional arguments to pass to the function.
            **kwargs: Keyword arguments to pass to the function.
        
        Returns:
            The result of the AGOR function if successful, otherwise the result of the fallback function.
        """
        if self.agor_available and hasattr(self.dev_tools, func_name):
            try:
                func = getattr(self.dev_tools, func_name)
                return func(*args, **kwargs)
            except Exception as e:
                self.logger.warning(f"AGOR function {func_name} failed: {e}")
                self.logger.info("Falling back to manual implementation")

        return fallback_func(*args, **kwargs)

    # Core AGOR Functions with Fallbacks
    # ==================================

    def generate_pr_description_output(self, content: str) -> str:
        """
        Generates a formatted pull request description from the provided content.
        
        If AGOR tools are unavailable, falls back to a basic implementation that replaces triple backticks with double backticks and wraps the content in code block markers.
        
        Args:
            content: The pull request description content to format.
        
        Returns:
            The formatted pull request description as a string.
        """

        def fallback(content: str) -> str:
            # Manual implementation for PR description formatting
            """
            Formats PR description content by replacing triple backticks with double backticks and wrapping the result in a code block.
            
            Args:
                content: The PR description content to format.
            
            Returns:
                The formatted PR description as a string.
            """
            processed_content = content.replace("```", "``")  # Basic deticking
            return f"```\n{processed_content}\n```"

        return self._call_with_fallback(
            "generate_pr_description_output", fallback, content
        )

    def generate_handoff_prompt_output(self, content: str) -> str:
        """
        Generates a formatted handoff prompt from the provided content.
        
        If AGOR tools are unavailable, formats the content by replacing triple backticks with double backticks and wrapping it in a code block.
        	
        Args:
        	content: The handoff prompt content to format.
        
        Returns:
        	A string containing the formatted handoff prompt.
        """

        def fallback(content: str) -> str:
            """
            Formats content as a code block, replacing triple backticks with double backticks.
            
            Args:
                content: The string content to be formatted.
            
            Returns:
                The content wrapped in triple backticks, with all original triple backticks replaced by double backticks.
            """
            processed_content = content.replace("```", "``")
            return f"```\n{processed_content}\n```"

        return self._call_with_fallback(
            "generate_handoff_prompt_output", fallback, content
        )

    def generate_release_notes_output(self, content: str) -> str:
        """
        Generates formatted release notes from the provided content.
        
        If AGOR tools are unavailable, formats the content by replacing triple backticks with double backticks and wrapping it in a code block.
        """

        def fallback(content: str) -> str:
            """
            Formats content as a code block, replacing triple backticks with double backticks.
            
            Args:
                content: The string content to be formatted.
            
            Returns:
                The content wrapped in triple backticks, with all original triple backticks replaced by double backticks.
            """
            processed_content = content.replace("```", "``")
            return f"```\n{processed_content}\n```"

        return self._call_with_fallback(
            "generate_release_notes_output", fallback, content
        )

    def create_development_snapshot(
        self, title: str, context: str, agent_id: str = None
    ) -> bool:
        """
        Creates a development snapshot using AGOR tools, with a fallback that logs the action and returns success if AGOR is unavailable.
        
        Args:
            title: The title of the snapshot.
            context: Contextual information to include in the snapshot.
            agent_id: Optional identifier for the agent associated with the snapshot.
        
        Returns:
            True if the snapshot was created successfully or the fallback was executed.
        """

        def fallback(title: str, context: str, agent_id: str = None) -> bool:
            """
            Fallback implementation for creating a development snapshot.
            
            Logs the intent to create a snapshot with the given title and context, but does not perform any actual operation. Always returns True to indicate success.
            """
            self.logger.info(f"Fallback: Would create snapshot '{title}' with context")
            self.logger.debug(f"Context: {context[:100]}...")
            return True

        return self._call_with_fallback(
            "create_development_snapshot", fallback, title, context, agent_id
        )

    def quick_commit_and_push(self, message: str, emoji: str = "🔧") -> bool:
        """
        Commits all changes and pushes to the current Git branch with a single command.
        
        If AGOR tools are unavailable, performs the equivalent Git operations directly using subprocess calls. Handles empty commit scenarios and disables interactive prompts in fallback mode.
        
        Args:
            message: Commit message to use.
            emoji: Emoji prefix for the commit message.
        
        Returns:
            True if the commit and push succeed or if there are no changes to commit; False otherwise.
        """

        def fallback(message: str, emoji: str = "🔧") -> bool:
            """
            Performs a git add, commit, and push operation with a fallback implementation.
            
            Attempts to stage all changes, commit with the provided message and emoji, and push to the remote repository. Handles scenarios where there are no changes to commit and disables interactive prompts. Returns True on success, or False if any git operation fails or times out.
            """
            import subprocess

            try:
                # Environment to disable interactive prompts
                git_env = {
                    **dict(os.environ),
                    "GIT_TERMINAL_PROMPT": "0",
                    "GIT_EDITOR": "true",  # Use 'true' as no-op editor
                }

                # Basic git operations with timeout
                subprocess.run(["git", "add", "."], check=True, timeout=30, env=git_env)

                # Try to commit - handle empty commit scenario
                try:
                    subprocess.run(
                        [
                            "git",
                            "commit",
                            "--no-edit",  # Don't open editor
                            "--no-gpg-sign",  # Don't prompt for GPG signing
                            "-m",
                            f"{emoji} {message}",
                        ],
                        check=True,
                        timeout=30,
                        env=git_env,
                    )
                except subprocess.CalledProcessError as e:
                    if e.returncode == 1:
                        # Check if it's a "nothing to commit" scenario
                        result = subprocess.run(
                            ["git", "status", "--porcelain"],
                            capture_output=True,
                            text=True,
                            timeout=10,
                            env=git_env,
                        )
                        if not result.stdout.strip():
                            self.logger.info(f"No changes to commit: {emoji} {message}")
                            return True  # Success - nothing to commit is not an error
                    raise  # Re-raise if it's a different error

                subprocess.run(["git", "push"], check=True, timeout=60, env=git_env)
                self.logger.info(f"Fallback commit and push: {emoji} {message}")
                return True

            except subprocess.TimeoutExpired as e:
                self.logger.error(f"Git operation timed out: {e}")
                return False
            except FileNotFoundError as e:
                self.logger.error(f"Git not found in PATH - please install Git: {e}")
                return False
            except subprocess.CalledProcessError as e:
                self.logger.error(f"Fallback git operation failed: {e}")
                return False

        return self._call_with_fallback(
            "quick_commit_and_push", fallback, message, emoji
        )

    def get_workspace_status(self) -> dict:
        """
        Returns the current workspace status, using AGOR tools if available or a fallback status otherwise.
        
        If AGOR tools are unavailable, the fallback provides a dictionary indicating fallback mode and unknown Git status.
        
        Returns:
            A dictionary describing the workspace status.
        """

        def fallback() -> dict:
            """
            Returns a dictionary indicating that AGOR tools are unavailable and fallback mode is active.
            """
            return {
                "mode": "fallback",
                "agor_available": False,
                "git_status": "unknown",
                "message": "AGOR tools not available - using fallback mode",
            }

        return self._call_with_fallback("get_workspace_status", fallback)

    def test_all_tools(self) -> bool:
        """
        Tests the availability of all integrated AGOR tools.
        
        Returns:
            True if tools are available or fallback mode is active.
        """

        def fallback() -> bool:
            """
            Logs the current AGOR integration status and indicates fallback mode is operational.
            
            Returns:
                True, indicating the fallback test completed successfully.
            """
            self.logger.info("Testing fallback mode...")
            self.logger.info(f"AGOR Available: {self.agor_available}")
            self.logger.info(f"Fallback Mode: {self.fallback_mode}")
            if self.agor_path:
                self.logger.info(f"AGOR Path: {self.agor_path}")
            return True

        return self._call_with_fallback("test_all_tools", fallback)

    # Utility Methods
    # ===============

    def get_status(self) -> Dict[str, Any]:
        """
        Returns a dictionary summarizing the current AGOR integration status.
        
        The returned dictionary includes flags for AGOR availability and fallback mode, the detected AGOR installation path, and a list of available core function names.
        """
        return {
            "agor_available": self.agor_available,
            "fallback_mode": self.fallback_mode,
            "agor_path": self.agor_path,
            "functions_available": [
                "generate_pr_description_output",
                "generate_handoff_prompt_output",
                "generate_release_notes_output",
                "create_development_snapshot",
                "quick_commit_and_push",
                "get_workspace_status",
                "test_all_tools",
            ],
        }

    def print_status(self):
        """
        Prints a summary of the current AGOR integration status, including availability, fallback mode, AGOR path, and number of available functions.
        """
        status = self.get_status()
        print("\n🔧 AGOR External Integration Status:")
        print(f"✅ AGOR Available: {status['agor_available']}")
        print(f"🔄 Fallback Mode: {status['fallback_mode']}")
        if status["agor_path"]:
            print(f"📁 AGOR Path: {status['agor_path']}")
        print(f"🛠️  Available Functions: {len(status['functions_available'])}")


# Convenience function for quick initialization
def get_agor_tools(agor_path: Optional[str] = None) -> AgorExternalTools:
    """
    Creates and returns an AgorExternalTools instance for integrating AGOR tools.
    
    Args:
        agor_path: Optional path to the AGOR installation directory.
    
    Returns:
        An initialized AgorExternalTools object for accessing AGOR development tools with fallback support.
    """
    return AgorExternalTools(agor_path)


# Example usage and testing
if __name__ == "__main__":
    print("🧪 Testing AGOR External Integration...")

    tools = get_agor_tools()
    tools.print_status()

    # Test basic functionality
    print("\n🧪 Testing functions...")
    tools.test_all_tools()

    # Test output generation
    test_content = "This is test content with ```code blocks``` inside"
    pr_output = tools.generate_pr_description_output(test_content)
    print(f"\n📝 PR Output Preview:\n{pr_output[:100]}...")
