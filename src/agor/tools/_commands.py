"""
AGOR Wrapper Command Handlers

This module contains the command handlers for the AGOR wrapper CLI tool.
Extracted to reduce cyclomatic complexity in the main wrapper script.
"""

from typing import Dict, Callable, Any
from agor.tools.external_integration import get_agor_tools


class CommandHandlers:
    """Command handlers for AGOR wrapper CLI."""
    
    def __init__(self, args: Any):
        """
        Initializes the CommandHandlers instance with parsed command-line arguments.
        
        Args:
            args: Parsed command-line arguments used to configure command handling.
        """
        self.args = args
        self.tools = get_agor_tools()
    
    def handle_status(self) -> int:
        """
        Displays the current status of AGOR tools and returns a success exit code.
        
        Returns:
            int: Exit code 0 indicating successful execution.
        """
        self.tools.print_status()
        return 0
    
    def handle_test(self) -> int:
        """
        Runs all available tool tests and returns an exit code indicating success.
        
        Returns:
            0 if all tests pass, 1 otherwise.
        """
        success = self.tools.test_all_tools()
        return 0 if success else 1
    
    def handle_pr(self) -> int:
        """
        Generates and prints a pull request description based on provided content.
        
        Returns:
            int: Exit code 0 after successful output.
        """
        output = self.tools.generate_pr_description_output(self.args.content)
        print(output)
        return 0
    
    def handle_handoff(self) -> int:
        """
        Generates and prints a handoff prompt output using the provided content.
        
        Returns:
            int: Exit code 0 indicating successful execution.
        """
        output = self.tools.generate_handoff_prompt_output(self.args.content)
        print(output)
        return 0
    
    def handle_snapshot(self) -> int:
        """
        Creates a development snapshot using the provided title, context, and agent ID.
        
        Prints a success message if the snapshot is created, or a failure message otherwise.
        
        Returns:
            0 if the snapshot was created successfully, 1 otherwise.
        """
        success = self.tools.create_development_snapshot(
            self.args.title, 
            self.args.context, 
            self.args.agent_id
        )
        if success:
            print(f"✅ Created snapshot: {self.args.title}")
        else:
            print(f"❌ Failed to create snapshot: {self.args.title}")
        return 0 if success else 1
    
    def handle_commit(self) -> int:
        """
        Attempts to commit and push changes using the provided message and emoji.
        
        Returns:
            0 if the commit and push were successful, 1 otherwise.
        """
        success = self.tools.quick_commit_and_push(self.args.message, self.args.emoji)
        if success:
            print(f"✅ Committed and pushed: {self.args.emoji} {self.args.message}")
        else:
            print(f"❌ Failed to commit: {self.args.message}")
        return 0 if success else 1
    
    def get_dispatch_table(self) -> Dict[str, Callable[[], int]]:
        """
        Returns a mapping of command names to their corresponding handler methods.
        
        Each key is a command string, and each value is a method that executes the command and returns an exit code.
        """
        return {
            'status': self.handle_status,
            'test': self.handle_test,
            'pr': self.handle_pr,
            'handoff': self.handle_handoff,
            'snapshot': self.handle_snapshot,
            'commit': self.handle_commit,
        }


def execute_command(args: Any) -> int:
    """
    Executes the specified CLI command using the appropriate handler.
    
    Initializes command handlers with the provided arguments, dispatches the command to its handler, and returns the corresponding exit code. Prints an error message and returns 1 if the command is unknown or if an exception occurs.
    
    Args:
        args: Parsed command-line arguments containing the command to execute.
    
    Returns:
        0 if the command executes successfully; 1 on failure or unknown command.
    """
    try:
        handlers = CommandHandlers(args)
        dispatch_table = handlers.get_dispatch_table()
        
        handler = dispatch_table.get(args.command)
        if handler:
            return handler()
        
        print(f"❌ Unknown command: {args.command}")
        return 1
        
    except Exception as e:
        print(f"❌ Error executing command '{args.command}': {e}")
        return 1
