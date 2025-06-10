"""
Unified Subprocess Management for AGOR 0.5.1

This module provides a unified interface for subprocess calls with
comprehensive error handling, logging, and resilience features.

Key Features:
- Unified subprocess interface
- Comprehensive error handling
- Logging and debugging support
- Timeout management
- Cross-platform compatibility
"""

import datetime
import logging
import shlex
import subprocess
import sys
import tempfile
from contextlib import suppress
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

# Configure logging
logger = logging.getLogger(__name__)


class SubprocessError(Exception):
    """Custom exception for subprocess-related errors."""

    def __init__(
        self,
        message: str,
        command: List[str],
        returncode: int,
        stdout: str = "",
        stderr: str = "",
    ):
        super().__init__(message)
        self.command = command
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


class SubprocessManager:
    """
    Unified subprocess manager with error handling and logging.

    Provides a consistent interface for all subprocess operations
    with comprehensive error handling, logging, and resilience.
    """

    def __init__(self, default_timeout: int = 30, log_commands: bool = True):
        """
        Initialize the subprocess manager.

        Args:
            default_timeout: Default timeout for subprocess calls in seconds
            log_commands: Whether to log command execution
        """
        self.default_timeout = default_timeout
        self.log_commands = log_commands
        self.command_history: List[Dict[str, Any]] = []

    def run_command(
        self,
        command: Union[str, List[str]],
        cwd: Optional[Path] = None,
        timeout: Optional[int] = None,
        capture_output: bool = True,
        check: bool = False,
        env: Optional[Dict[str, str]] = None,
        input_text: Optional[str] = None,
        shell: bool = False,
    ) -> Tuple[bool, str, str, int]:
        """
        Run a command with unified error handling and logging.

        Args:
            command: Command to run (string or list)
            cwd: Working directory for the command
            timeout: Timeout in seconds (uses default if None)
            capture_output: Whether to capture stdout/stderr
            check: Whether to raise exception on non-zero exit
            env: Environment variables
            input_text: Input to send to the process
            shell: Whether to run through shell

        Returns:
            Tuple of (success, stdout, stderr, returncode)
        """
        # Normalize command to list
        if isinstance(command, str):
            cmd_list = command if shell else shlex.split(command)
        else:
            cmd_list = command

        # Use default timeout if not specified
        timeout = timeout or self.default_timeout

        # Log command execution
        if self.log_commands:
            logger.info(f"Executing command: {cmd_list}")
            if cwd:
                logger.info(f"Working directory: {cwd}")

        try:
            # Prepare subprocess arguments
            kwargs = {
                "cwd": str(cwd) if cwd else None,
                "timeout": timeout,
                "env": env,
                "shell": shell,
            }

            if capture_output:
                kwargs.update(
                    {"stdout": subprocess.PIPE, "stderr": subprocess.PIPE, "text": True}
                )

            if input_text:
                kwargs["input"] = input_text

            # Execute command
            result = subprocess.run(cmd_list, **kwargs)

            # Extract outputs
            stdout = result.stdout if capture_output else ""
            stderr = result.stderr if capture_output else ""
            returncode = result.returncode

            # Log result
            success = returncode == 0
            if self.log_commands:
                if success:
                    logger.info(f"Command succeeded: {cmd_list}")
                else:
                    logger.warning(f"Command failed with code {returncode}: {cmd_list}")
                    if stderr:
                        logger.warning(f"Error output: {stderr}")

            # Record command history
            self.command_history.append(
                {
                    "command": cmd_list,
                    "success": success,
                    "returncode": returncode,
                    "cwd": str(cwd) if cwd else None,
                    "timestamp": self._get_timestamp(),
                }
            )

            # Raise exception if check=True and command failed
            if check and not success:
                raise SubprocessError(
                    f"Command failed with exit code {returncode}",
                    cmd_list,
                    returncode,
                    stdout,
                    stderr,
                )

            return success, stdout, stderr, returncode

        except subprocess.TimeoutExpired as e:
            error_msg = f"Command timed out after {timeout} seconds: {cmd_list}"
            logger.error(error_msg)

            # Record timeout in history
            self.command_history.append(
                {
                    "command": cmd_list,
                    "success": False,
                    "returncode": -1,
                    "error": "timeout",
                    "cwd": str(cwd) if cwd else None,
                    "timestamp": self._get_timestamp(),
                }
            )

            if check:
                raise SubprocessError(error_msg, cmd_list, -1) from e

            return False, "", f"Timeout after {timeout} seconds", -1

        except FileNotFoundError as e:
            error_msg = f"Command not found: {cmd_list[0] if cmd_list else 'unknown'}"
            logger.error(error_msg)

            # Record error in history
            self.command_history.append(
                {
                    "command": cmd_list,
                    "success": False,
                    "returncode": -2,
                    "error": "not_found",
                    "cwd": str(cwd) if cwd else None,
                    "timestamp": self._get_timestamp(),
                }
            )

            if check:
                raise SubprocessError(error_msg, cmd_list, -2) from e

            return False, "", error_msg, -2

        except Exception as e:
            error_msg = f"Unexpected error running command {cmd_list}: {str(e)}"
            logger.error(error_msg)

            # Record error in history
            self.command_history.append(
                {
                    "command": cmd_list,
                    "success": False,
                    "returncode": -3,
                    "error": str(e),
                    "cwd": str(cwd) if cwd else None,
                    "timestamp": self._get_timestamp(),
                }
            )

            if check:
                raise SubprocessError(error_msg, cmd_list, -3) from e

            return False, "", error_msg, -3

    def run_git_command(
        self,
        git_args: List[str],
        cwd: Optional[Path] = None,
        timeout: Optional[int] = None,
    ) -> Tuple[bool, str]:
        """
        Run a git command with specialized error handling.

        Args:
            git_args: Git command arguments (without 'git')
            cwd: Working directory for the command
            timeout: Timeout in seconds

        Returns:
            Tuple of (success, output)
        """
        command = ["git"] + git_args
        success, stdout, stderr, returncode = self.run_command(
            command, cwd=cwd, timeout=timeout
        )

        # For git commands, combine stdout and stderr for output
        output = stdout if success else stderr

        return success, output

    def run_python_command(
        self,
        python_args: List[str],
        cwd: Optional[Path] = None,
        timeout: Optional[int] = None,
        use_current_python: bool = True,
    ) -> Tuple[bool, str, str, int]:
        """
        Run a Python command with appropriate interpreter.

        Args:
            python_args: Python command arguments (without 'python')
            cwd: Working directory for the command
            timeout: Timeout in seconds
            use_current_python: Whether to use current Python interpreter

        Returns:
            Tuple of (success, stdout, stderr, returncode)
        """
        python_cmd = sys.executable if use_current_python else "python3"

        command = [python_cmd] + python_args
        return self.run_command(command, cwd=cwd, timeout=timeout)

    def run_with_input(
        self,
        command: Union[str, List[str]],
        input_text: str,
        cwd: Optional[Path] = None,
        timeout: Optional[int] = None,
    ) -> Tuple[bool, str, str, int]:
        """
        Run a command with input text.

        Args:
            command: Command to run
            input_text: Text to send to the process
            cwd: Working directory
            timeout: Timeout in seconds

        Returns:
            Tuple of (success, stdout, stderr, returncode)
        """
        return self.run_command(
            command, cwd=cwd, timeout=timeout, input_text=input_text
        )

    def run_with_temp_file(
        self,
        command: Union[str, List[str]],
        file_content: str,
        file_suffix: str = ".tmp",
        cwd: Optional[Path] = None,
        timeout: Optional[int] = None,
    ) -> Tuple[bool, str, str, int]:
        """
        Run a command with a temporary file.

        Args:
            command: Command to run (use {temp_file} placeholder)
            file_content: Content to write to temporary file
            file_suffix: Suffix for temporary file
            cwd: Working directory
            timeout: Timeout in seconds

        Returns:
            Tuple of (success, stdout, stderr, returncode)
        """
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=file_suffix, delete=False
        ) as temp_file:
            temp_file.write(file_content)
            temp_file_path = temp_file.name

        try:
            # Replace placeholder in command
            if isinstance(command, str):
                command = command.replace("{temp_file}", temp_file_path)
            else:
                command = [
                    arg.replace("{temp_file}", temp_file_path) for arg in command
                ]

            return self.run_command(command, cwd=cwd, timeout=timeout)

        finally:
            # Clean up temporary file
            with suppress(Exception):
                Path(temp_file_path).unlink()

    def get_command_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get command execution history.

        Args:
            limit: Maximum number of commands to return

        Returns:
            List of command history entries
        """
        if limit:
            return self.command_history[-limit:]
        return self.command_history.copy()

    def clear_history(self) -> None:
        """Clear command execution history."""
        self.command_history.clear()

    def get_stats(self) -> Dict[str, Any]:
        """
        Get execution statistics.

        Returns:
            Dictionary with execution statistics
        """
        total_commands = len(self.command_history)
        successful_commands = sum(1 for cmd in self.command_history if cmd["success"])
        failed_commands = total_commands - successful_commands

        return {
            "total_commands": total_commands,
            "successful_commands": successful_commands,
            "failed_commands": failed_commands,
            "success_rate": (
                successful_commands / total_commands if total_commands > 0 else 0
            ),
        }

    def _get_timestamp(self) -> str:
        """Get current timestamp for logging."""
        return datetime.datetime.now().isoformat()


# Global subprocess manager instance
_subprocess_manager = SubprocessManager()


# Convenience functions for backward compatibility
def run_command(command: Union[str, List[str]], **kwargs) -> Tuple[bool, str, str, int]:
    """Run a command using the global subprocess manager."""
    return _subprocess_manager.run_command(command, **kwargs)


def run_git_command(git_args: List[str], **kwargs) -> Tuple[bool, str]:
    """Run a git command using the global subprocess manager."""
    return _subprocess_manager.run_git_command(git_args, **kwargs)


def run_python_command(python_args: List[str], **kwargs) -> Tuple[bool, str, str, int]:
    """Run a Python command using the global subprocess manager."""
    return _subprocess_manager.run_python_command(python_args, **kwargs)


def get_subprocess_stats() -> Dict[str, Any]:
    """Get subprocess execution statistics."""
    return _subprocess_manager.get_stats()
