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
    
    def __init__(self, message: str, command: List[str], returncode: int, 
                 stdout: str = "", stderr: str = ""):
        """
                 Initializes a SubprocessError with details about a failed subprocess execution.
                 
                 Args:
                     message: Description of the error.
                     command: The command that was executed as a list of arguments.
                     returncode: The exit code returned by the subprocess.
                     stdout: Standard output captured from the subprocess.
                     stderr: Standard error captured from the subprocess.
                 """
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
        Initializes a SubprocessManager with default timeout and logging preferences.
        
        Args:
            default_timeout: Timeout in seconds to use for subprocess calls if not specified.
            log_commands: If True, enables logging of executed commands.
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
        shell: bool = False
    ) -> Tuple[bool, str, str, int]:
        """
        Executes a command as a subprocess with unified error handling, logging, and optional input.
        
        Args:
            command: The command to execute, as a string or list of arguments.
            cwd: Optional working directory for the command.
            timeout: Timeout in seconds; uses the default if not specified.
            capture_output: If True, captures stdout and stderr.
            check: If True, raises SubprocessError on non-zero exit or failure.
            env: Optional environment variables for the subprocess.
            input_text: Optional text to send to the process's stdin.
            shell: If True, executes the command through the shell.
        
        Returns:
            A tuple (success, stdout, stderr, returncode), where success is True if the command exited with code 0.
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
                'cwd': str(cwd) if cwd else None,
                'timeout': timeout,
                'env': env,
                'shell': shell
            }
            
            if capture_output:
                kwargs.update({
                    'stdout': subprocess.PIPE,
                    'stderr': subprocess.PIPE,
                    'text': True
                })
            
            if input_text:
                kwargs['input'] = input_text
            
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
            self.command_history.append({
                'command': cmd_list,
                'success': success,
                'returncode': returncode,
                'cwd': str(cwd) if cwd else None,
                'timestamp': self._get_timestamp()
            })
            
            # Raise exception if check=True and command failed
            if check and not success:
                raise SubprocessError(
                    f"Command failed with exit code {returncode}",
                    cmd_list, returncode, stdout, stderr
                )
            
            return success, stdout, stderr, returncode
            
        except subprocess.TimeoutExpired as e:
            error_msg = f"Command timed out after {timeout} seconds: {cmd_list}"
            logger.error(error_msg)

            # Record timeout in history
            self.command_history.append({
                'command': cmd_list,
                'success': False,
                'returncode': -1,
                'error': 'timeout',
                'cwd': str(cwd) if cwd else None,
                'timestamp': self._get_timestamp()
            })

            if check:
                raise SubprocessError(error_msg, cmd_list, -1) from e

            return False, "", f"Timeout after {timeout} seconds", -1
            
        except FileNotFoundError as e:
            error_msg = f"Command not found: {cmd_list[0] if cmd_list else 'unknown'}"
            logger.error(error_msg)

            # Record error in history
            self.command_history.append({
                'command': cmd_list,
                'success': False,
                'returncode': -2,
                'error': 'not_found',
                'cwd': str(cwd) if cwd else None,
                'timestamp': self._get_timestamp()
            })

            if check:
                raise SubprocessError(error_msg, cmd_list, -2) from e

            return False, "", error_msg, -2
            
        except Exception as e:
            error_msg = f"Unexpected error running command {cmd_list}: {str(e)}"
            logger.error(error_msg)

            # Record error in history
            self.command_history.append({
                'command': cmd_list,
                'success': False,
                'returncode': -3,
                'error': str(e),
                'cwd': str(cwd) if cwd else None,
                'timestamp': self._get_timestamp()
            })

            if check:
                raise SubprocessError(error_msg, cmd_list, -3) from e

            return False, "", error_msg, -3
    
    def run_git_command(
        self,
        git_args: List[str],
        cwd: Optional[Path] = None,
        timeout: Optional[int] = None
    ) -> Tuple[bool, str]:
        """
        Executes a git command and returns its success status and output.
        
        Runs the specified git command arguments, combining standard output and error output into a single string. Returns the output from stdout if the command succeeds, or stderr if it fails.
        
        Args:
            git_args: List of arguments for the git command, excluding the 'git' executable.
            cwd: Optional working directory in which to run the command.
            timeout: Optional timeout in seconds for command execution.
        
        Returns:
            A tuple containing a boolean indicating success and the combined output string.
        """
        command = ['git'] + git_args
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
        use_current_python: bool = True
    ) -> Tuple[bool, str, str, int]:
        """
        Executes a Python command using the specified interpreter.
        
        Runs a Python subprocess with the given arguments, optionally using the current Python interpreter or the system default. Returns a tuple containing a success flag, standard output, standard error, and the process return code.
        
        Args:
            python_args: Arguments to pass to the Python interpreter (excluding the interpreter itself).
            cwd: Optional working directory for the subprocess.
            timeout: Optional timeout in seconds for the command.
            use_current_python: If True, uses the current Python interpreter; otherwise, uses 'python3'.
        
        Returns:
            A tuple (success, stdout, stderr, returncode) indicating execution result.
        """
        python_cmd = sys.executable if use_current_python else 'python3'
        
        command = [python_cmd] + python_args
        return self.run_command(command, cwd=cwd, timeout=timeout)
    
    def run_with_input(
        self,
        command: Union[str, List[str]],
        input_text: str,
        cwd: Optional[Path] = None,
        timeout: Optional[int] = None
    ) -> Tuple[bool, str, str, int]:
        """
        Runs a command and sends the specified input text to its standard input.
        
        Args:
            command: The command to execute, as a string or list of arguments.
            input_text: The text to provide to the process's standard input.
            cwd: Optional working directory for the command.
            timeout: Optional timeout in seconds for command execution.
        
        Returns:
            A tuple containing a success flag, standard output, standard error, and return code.
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
        timeout: Optional[int] = None
    ) -> Tuple[bool, str, str, int]:
        """
        Runs a command after creating a temporary file with specified content and replacing the `{temp_file}` placeholder in the command with the file's path.
        
        Args:
            command: The command to execute, containing a `{temp_file}` placeholder to be replaced with the temporary file path.
            file_content: The content to write into the temporary file.
            file_suffix: The suffix to use for the temporary file name.
            cwd: Optional working directory for the command.
            timeout: Optional timeout in seconds for command execution.
        
        Returns:
            A tuple containing a success flag, stdout, stderr, and the command's return code.
        """
        with tempfile.NamedTemporaryFile(
            mode='w', suffix=file_suffix, delete=False
        ) as temp_file:
            temp_file.write(file_content)
            temp_file_path = temp_file.name
        
        try:
            # Replace placeholder in command
            if isinstance(command, str):
                command = command.replace('{temp_file}', temp_file_path)
            else:
                command = [arg.replace('{temp_file}', temp_file_path) for arg in command]
            
            return self.run_command(command, cwd=cwd, timeout=timeout)
        
        finally:
            # Clean up temporary file
            with suppress(Exception):
                Path(temp_file_path).unlink()
    
    def get_command_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Returns the history of executed commands.
        
        If a limit is specified, only the most recent entries up to that limit are returned; otherwise, the full history is provided.
        
        Args:
            limit: The maximum number of recent command entries to return.
        
        Returns:
            A list of dictionaries containing metadata for each executed command.
        """
        if limit:
            return self.command_history[-limit:]
        return self.command_history.copy()
    
    def clear_history(self) -> None:
        """
        Clears the command execution history.
        """
        self.command_history.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Returns statistics on executed subprocess commands.
        
        The returned dictionary includes the total number of commands run, counts of successful and failed executions, and the success rate as a float between 0 and 1.
        
        Returns:
            A dictionary with keys: 'total_commands', 'successful_commands', 'failed_commands', and 'success_rate'.
        """
        total_commands = len(self.command_history)
        successful_commands = sum(1 for cmd in self.command_history if cmd['success'])
        failed_commands = total_commands - successful_commands
        
        return {
            'total_commands': total_commands,
            'successful_commands': successful_commands,
            'failed_commands': failed_commands,
            'success_rate': successful_commands / total_commands if total_commands > 0 else 0
        }
    
    def _get_timestamp(self) -> str:
        """
        Returns the current timestamp as an ISO 8601 formatted string.
        """
        return datetime.datetime.now().isoformat()


# Global subprocess manager instance
_subprocess_manager = SubprocessManager()


# Convenience functions for backward compatibility
def run_command(command: Union[str, List[str]], **kwargs) -> Tuple[bool, str, str, int]:
    """
    Executes a command using the global subprocess manager.
    
    Args:
        command: The command to execute, as a string or list of arguments.
        **kwargs: Additional options forwarded to the subprocess manager, such as working directory, timeout, environment variables, input text, shell execution, and output capture.
    
    Returns:
        A tuple containing a success flag, standard output, standard error, and return code.
    """
    return _subprocess_manager.run_command(command, **kwargs)


def run_git_command(git_args: List[str], **kwargs) -> Tuple[bool, str]:
    """
    Executes a git command using the global subprocess manager.
    
    Args:
        git_args: List of arguments for the git command (excluding 'git' itself).
    
    Returns:
        A tuple containing a success flag and the combined output (stdout if successful, otherwise stderr).
    """
    return _subprocess_manager.run_git_command(git_args, **kwargs)


def run_python_command(python_args: List[str], **kwargs) -> Tuple[bool, str, str, int]:
    """
    Executes a Python command using the global subprocess manager.
    
    Args:
    	python_args: List of arguments to pass to the Python interpreter.
    
    Returns:
    	A tuple containing a success flag, stdout, stderr, and return code.
    """
    return _subprocess_manager.run_python_command(python_args, **kwargs)


def get_subprocess_stats() -> Dict[str, Any]:
    """
    Returns statistics about all subprocess commands executed via the global manager.
    
    The statistics include the total number of commands run, the number of successful and failed commands, and the overall success rate.
     
    Returns:
        A dictionary containing execution statistics for subprocess commands.
    """
    return _subprocess_manager.get_stats()
