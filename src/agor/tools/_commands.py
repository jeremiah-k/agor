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
        """Initialize command handlers with parsed arguments."""
        self.args = args
        self.tools = get_agor_tools()

    def handle_status(self) -> int:
        """Handle status command."""
        self.tools.print_status()
        return 0

    def handle_test(self) -> int:
        """Handle test command."""
        success = self.tools.test_all_tools()
        return 0 if success else 1

    def handle_pr(self) -> int:
        """Handle PR description generation command."""
        output = self.tools.generate_pr_description_output(self.args.content)
        print(output)
        return 0

    def handle_handoff(self) -> int:
        """Handle handoff prompt generation command."""
        output = self.tools.generate_handoff_prompt_output(self.args.content)
        print(output)
        return 0

    def handle_snapshot(self) -> int:
        """Handle snapshot creation command."""
        success = self.tools.create_development_snapshot(
            self.args.title, self.args.context, self.args.agent_id
        )
        if success:
            print(f"✅ Created snapshot: {self.args.title}")
        else:
            print(f"❌ Failed to create snapshot: {self.args.title}")
        return 0 if success else 1

    def handle_commit(self) -> int:
        """Handle commit and push command."""
        success = self.tools.quick_commit_and_push(self.args.message, self.args.emoji)
        if success:
            print(f"✅ Committed and pushed: {self.args.emoji} {self.args.message}")
        else:
            print(f"❌ Failed to commit: {self.args.message}")
        return 0 if success else 1

    def get_dispatch_table(self) -> Dict[str, Callable[[], int]]:
        """Get the command dispatch table."""
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
    Execute a command using the dispatch table.

    Args:
        args: Parsed command line arguments

    Returns:
        Exit code (0 for success, 1 for failure)
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
