"""
AGOR Wrapper Command Handlers

This module contains the command handlers for the AGOR wrapper CLI tool.
Extracted to reduce cyclomatic complexity in the main wrapper script.
"""

from typing import Any, Callable, Dict

from agor.tools.external_integration import get_agor_tools


class CommandHandlers:
    """Command handlers for AGOR wrapper CLI."""

    def __init__(self, args: Any):
        """
        Initializes the CommandHandlers instance with parsed CLI arguments and AGOR tools.
        """
        self.args = args
        self.tools = get_agor_tools()

    def handle_status(self) -> int:
        """
        Displays the current status of AGOR tools and returns a success exit code.
        """
        self.tools.print_status()
        return 0

    def handle_test(self) -> int:
        """
        Executes tests for all AGOR tools and returns an appropriate exit code.
        
        Returns:
            0 if all tests pass successfully, 1 otherwise.
        """
        success = self.tools.test_all_tools()
        return 0 if success else 1

    def handle_pr(self) -> int:
        """
        Generates and prints a pull request description based on provided content.
        
        Returns:
            Exit code 0 after successful generation and output.
        """
        output = self.tools.generate_pr_description_output(self.args.content)
        print(output)
        return 0

    def handle_handoff(self) -> int:
        """
        Generates and prints a handoff prompt based on provided content.
        
        Returns:
            Exit code 0 after successful output.
        """
        output = self.tools.generate_handoff_prompt_output(self.args.content)
        print(output)
        return 0

    def handle_snapshot(self) -> int:
        """
        Creates a development snapshot using the provided title, context, and agent ID.
        
        Returns:
            0 if the snapshot was created successfully, 1 otherwise.
        """
        success = self.tools.create_development_snapshot(
            self.args.title, self.args.context, self.args.agent_id
        )
        if success:
            print(f"✅ Created snapshot: {self.args.title}")
        else:
            print(f"❌ Failed to create snapshot: {self.args.title}")
        return 0 if success else 1

    def handle_commit(self) -> int:
        """
        Commits changes and pushes them to the repository with a message and emoji.
        
        Returns:
            0 if the commit and push succeed, 1 otherwise.
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
            "status": self.handle_status,
            "test": self.handle_test,
            "pr": self.handle_pr,
            "handoff": self.handle_handoff,
            "snapshot": self.handle_snapshot,
            "commit": self.handle_commit,
        }


def execute_command(args: Any) -> int:
    """
    Executes the specified CLI command and returns an appropriate exit code.
    
    Attempts to dispatch and run the handler for the command provided in the parsed
    arguments. Returns 0 on success, or 1 if the command is unknown or an error occurs.
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
