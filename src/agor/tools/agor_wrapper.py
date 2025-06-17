#!/usr/bin/env python3
"""
AGOR Wrapper Script for External Projects

This script provides a simple command-line interface for accessing AGOR tools
from external projects where AGOR is installed separately.

Usage:
    python agor_wrapper.py status                    # Check integration status
    python agor_wrapper.py test                      # Test all tools
    python agor_wrapper.py pr "PR description"       # Generate PR description
    python agor_wrapper.py handoff "Handoff content" # Generate handoff prompt
    python agor_wrapper.py snapshot "Title" "Context" # Create snapshot
    python agor_wrapper.py commit "Commit message"   # Quick commit and push

This addresses the critical meta feedback about tool integration issues.
"""

import argparse
import sys
from pathlib import Path


def main():
    """Main wrapper function with command-line interface."""
    parser = argparse.ArgumentParser(
        description="AGOR Tools Wrapper for External Projects",
        epilog="Addresses tool integration issues for external project usage",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Status command
    subparsers.add_parser("status", help="Check AGOR integration status")

    # Test command
    subparsers.add_parser("test", help="Test all AGOR tools")

    # PR description command
    pr_parser = subparsers.add_parser("pr", help="Generate PR description")
    pr_parser.add_argument("content", help="PR description content")

    # Handoff command
    handoff_parser = subparsers.add_parser("handoff", help="Generate handoff prompt")
    handoff_parser.add_argument("content", help="Handoff content")

    # Snapshot command
    snapshot_parser = subparsers.add_parser(
        "snapshot", help="Create development snapshot"
    )
    snapshot_parser.add_argument("title", help="Snapshot title")
    snapshot_parser.add_argument("context", help="Snapshot context")
    snapshot_parser.add_argument("--agent-id", help="Optional agent ID")

    # Commit command
    commit_parser = subparsers.add_parser("commit", help="Quick commit and push")
    commit_parser.add_argument("message", help="Commit message")
    commit_parser.add_argument(
        "--emoji", default="🔧", help="Commit emoji (default: 🔧)"
    )

    # Parse arguments
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Initialize AGOR tools
    try:
        # Add current directory to path for development environment
        try:
            # Try to get the src directory (2 levels up from this file)
            script_path = Path(__file__).resolve()
            if len(script_path.parents) > 2:
                current_dir = script_path.parents[2]  # …/src
            else:
                # Fallback: use the directory containing this script
                current_dir = script_path.parent
        except (IndexError, OSError):
            # Fallback: use current working directory
            current_dir = Path.cwd()

        if current_dir.is_dir() and str(current_dir) not in sys.path:
            sys.path.insert(0, str(current_dir))

        from agor.tools._commands import execute_command

        return execute_command(args)
    except ImportError as e:
        print(f"❌ Failed to import AGOR command handlers: {e}")
        print("💡 Make sure AGOR is installed and accessible")
        print(f"💡 Current working directory: {Path.cwd()}")
        print(f"💡 Script location: {Path(__file__).parent}")
        return 1


def install_wrapper():
    """Install wrapper script to a convenient location."""
    import shutil

    script_path = Path(__file__).resolve()

    # Try to install to user's local bin
    local_bin = Path.home() / ".local" / "bin"
    if local_bin.exists():
        target = local_bin / "agor-tools"
        try:
            shutil.copy2(script_path, target)
            target.chmod(0o755)
            print(f"✅ Installed AGOR wrapper to: {target}")
            print(f"💡 Add {local_bin} to your PATH if not already there")
            print("Usage: agor-tools status")
            return True
        except Exception as e:
            print(f"⚠️  Failed to install to {target}: {e}")

    # Fallback: suggest manual installation
    print("💡 Manual installation:")
    print(f"   cp {script_path} ~/.local/bin/agor-tools")
    print("   chmod +x ~/.local/bin/agor-tools")
    print("   # Add ~/.local/bin to PATH if needed")
    return False


def show_usage_examples():
    """Show usage examples for the wrapper."""
    print(
        """
🛠️  AGOR Wrapper Usage Examples:

## Development Usage (from source):

# Check integration status
python agor_wrapper.py status

# Test all tools
python agor_wrapper.py test

# Generate PR description
python agor_wrapper.py pr "Added authentication system with OAuth support"

# Generate handoff prompt
python agor_wrapper.py handoff "Completed feature X, next agent should work on Y"

# Create development snapshot
python agor_wrapper.py snapshot "Feature Implementation" "Added OAuth and user management"

# Quick commit and push
python agor_wrapper.py commit "Implement OAuth authentication" --emoji "✨"

## Installed Usage (after running --install):

# Check integration status
agor-tools status

# Test all tools
agor-tools test

# Generate PR description
agor-tools pr "Added authentication system with OAuth support"

# Generate handoff prompt
agor-tools handoff "Completed feature X, next agent should work on Y"

# Create development snapshot
agor-tools snapshot "Feature Implementation" "Added OAuth and user management"

# Quick commit and push
agor-tools commit "Implement OAuth authentication" --emoji "✨"

# Install wrapper for easier access
python agor_wrapper.py --install

📚 For complete documentation, see EXTERNAL_INTEGRATION_GUIDE.md
"""
    )


if __name__ == "__main__":
    # Handle special arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--install":
            install_wrapper()
            sys.exit(0)
        elif sys.argv[1] == "--examples":
            show_usage_examples()
            sys.exit(0)
        elif sys.argv[1] in ["--help", "-h"] and len(sys.argv) == 2:
            # Show enhanced help
            main()
            show_usage_examples()
            sys.exit(0)

    # Run main function
    sys.exit(main())
