import re
import shutil
import sys
import tempfile
from pathlib import Path
from textwrap import dedent
from typing import List, Optional

import platformdirs
import typer

from . import __version__
from .config import config
from .constants import (
    ARCHIVE_EXTENSIONS,
    SUCCESS_MESSAGES,
)
from .exceptions import ValidationError
from .platform import (
    copy_to_clipboard,
    get_downloads_dir,
    is_termux,
    reveal_file_in_explorer,
)
from .repo_mgmt import clone_git_repo_to_temp_dir, get_clone_url, valid_git_repo
from .settings import settings
from .utils import create_archive, download_file, move_directory
from .validation import validate_compression_format

app = typer.Typer(
    add_completion=False,
    help="🎼 AgentOrchestrator (AGOR) - Multi-Agent Development Coordination Platform",
    epilog="For more information, visit: https://github.com/jeremiah-k/agor",
)


@app.command()
def version():
    """Display AGOR version information"""
    print(f"🎼 AgentOrchestrator (AGOR) v{__version__}")


def config_cmd(
    show: bool = typer.Option(False, "--show", help="Show current configuration"),
    set_key: Optional[str] = typer.Option(
        None, "--set", help="Set configuration key (format: key=value)"
    ),
    reset: bool = typer.Option(
        False, "--reset", help="Reset configuration to defaults"
    ),
):
    """Manage AGOR configuration settings"""

    if reset:
        config.reset()
        print("🔄 Configuration reset to defaults!")
        return

    if set_key:
        try:
            if "=" not in set_key:
                raise ValueError("Format must be key=value")
            key, value = set_key.split("=", 1)

            # Convert string values to appropriate types
            if key in [
                "quiet",
                "preserve_history",
                "main_only",
                "interactive",
                "assume_yes",
                "clipboard_copy_default",
            ]:
                value = value.lower() in ("true", "1", "yes", "on")
            elif key in ["shallow_depth", "download_chunk_size", "progress_bar_width"]:
                value = int(value)

            config.set(key, value)
            print(f"✅ Set {key} = {value}")
        except (ValueError, TypeError) as e:
            print(f"❌ Error setting configuration: {e}")
            return

    if show or not (set_key or reset):
        print("📋 Current AGOR Configuration:")
        print("=" * 40)
        current_config = config.show()
        for key, value in current_config.items():
            print(f"{key:25} = {value}")

        print("\n🌍 Environment Variables:")
        print("=" * 40)
        env_vars = config.get_env_vars()
        if env_vars:
            for key, value in env_vars.items():
                print(f"{key:25} = {value}")
        else:
            print("No AGOR environment variables set")

        print(f"\n📁 Config file: {config.config_file}")


# Register the config command with proper name
config_cmd = app.command(name="config")(config_cmd)


# Define option for branches outside the function to avoid B008 warning
branches_option = typer.Option(
    None,
    "--branches",
    "-b",
    help="Specify additional branches to bundle with main/master (comma-separated list)",
)


@app.command()
def bundle(
    src_repo: str = typer.Argument(
        help="Local git repository path or GitHub URL (supports user/repo shorthand)",
        callback=valid_git_repo,
    ),
    format: str = typer.Option(
        None,
        "--format",
        "-f",
        help=f"Archive format: {', '.join(ARCHIVE_EXTENSIONS.keys())} (default: {settings.compression_format})",
    ),
    preserve_history: bool = typer.Option(
        None,
        "--preserve-history",
        "-p",
        help="Preserve full git history (default: shallow clone to save space)",
    ),
    main_only: bool = typer.Option(
        None,
        "--main-only",
        "-m",
        help="Bundle only main/master branch",
    ),
    all_branches: bool = typer.Option(
        False,
        "--all-branches",
        "-a",
        hidden=True,
        help="Legacy flag for backward compatibility",
    ),
    branches: Optional[List[str]] = branches_option,
    interactive: bool = typer.Option(
        None, "--no-interactive", help="Disable interactive prompts (batch mode)"
    ),
    assume_yes: bool = typer.Option(
        None, "--assume-yes", "-y", help="Assume 'yes' for all prompts"
    ),
    quiet: bool = typer.Option(
        None,
        "--quiet",
        "-q",
        help="Minimal output mode",
    ),
    include_sqlite: bool = typer.Option(
        None,
        "--sqlite",
        "-s",
        help="Include SQLite binary for database-based memory management (experimental)",
    ),
):
    """
    Bundle a git repository into an archive for AI assistant upload.

    Creates a compressed archive containing your project plus AGOR's multi-agent
    coordination tools. Supports ZIP (default), TAR.GZ, and TAR.BZ2 formats.

    Examples:
        agor bundle my-project                    # Bundle all branches as ZIP
        agor bundle user/repo --format gz        # GitHub repo as TAR.GZ
        agor bundle . -m --quiet                 # Main branch only, minimal output
        agor bundle /path/to/repo -f zip -y      # ZIP format, assume yes to prompts
    """
    # Apply configuration defaults with CLI overrides
    compression_format = format or config.get(
        "compression_format", settings.compression_format
    )
    preserve_hist = (
        preserve_history
        if preserve_history is not None
        else config.get("preserve_history", False)
    )
    main_branch_only = (
        main_only if main_only is not None else config.get("main_only", False)
    )
    is_interactive = (
        interactive if interactive is not None else config.get("interactive", True)
    )
    auto_yes = assume_yes if assume_yes is not None else config.get("assume_yes", False)
    quiet_mode = quiet if quiet is not None else config.get("quiet", False)
    sqlite_enabled = (
        include_sqlite
        if include_sqlite is not None
        else config.get("include_sqlite", settings.include_sqlite)
    )

    # Validate compression format
    try:
        compression_format = validate_compression_format(compression_format)
    except ValidationError as e:
        print(f"❌ {e}")
        raise typer.Exit(1) from e

    # Get repository information
    repo_name = get_clone_url(src_repo).split("/")[-1]
    short_name = re.sub(r"\.git$", "", repo_name)

    if not quiet_mode:
        print("🎼 AGOR Bundle Creation")
        print(f"📁 Repository: {repo_name}")
        print(f"📦 Format: {compression_format.upper()}")

    # Process branches parameter if provided
    branch_list = None
    if branches:
        branch_list = [b.strip() for b in branches if b.strip()]

    # Determine which branches to clone
    if main_branch_only:
        if not quiet_mode:
            print("📋 Bundling only main/master branch")
        temp_repo = clone_git_repo_to_temp_dir(
            src_repo, shallow=not preserve_hist, main_only=True
        )
    elif branch_list:
        if not quiet_mode:
            print(
                f"📋 Bundling main/master plus additional branches: {', '.join(branch_list)}"
            )
        temp_repo = clone_git_repo_to_temp_dir(
            src_repo, shallow=not preserve_hist, branches=branch_list
        )
    else:
        if not quiet_mode:
            print("📋 Bundling all branches from the repository (default)")
        temp_repo = clone_git_repo_to_temp_dir(
            src_repo, shallow=not preserve_hist, all_branches=True
        )

    if not quiet_mode:
        print(f"⚙️  Preparing to build '{short_name}'...")

    # Create output directory structure
    output_dir = Path(tempfile.mkdtemp())
    output_dir.mkdir(parents=True, exist_ok=True)
    tools_dir = Path(__file__).parent / "tools"

    # Move the cloned repo into output_dir/project
    project_dir = output_dir / "project"
    move_directory(temp_repo, project_dir)

    # Copy all files in tools to output_dir
    shutil.copytree(tools_dir, output_dir / "agor_tools")

    # Download and add git binary to bundle (simple approach that works)
    try:
        git_url = config.get("git_binary_url", settings.git_binary_url)

        # Use cache directory for git binary
        git_cache_dir = Path(platformdirs.user_cache_dir("agor")) / "git_binary"
        git_cache_dir.mkdir(parents=True, exist_ok=True)
        git_binary_cache_path = git_cache_dir / "git"

        # Download the git binary only if it doesn't exist in the cache
        if not git_binary_cache_path.exists():
            if not quiet_mode:
                print("📥 Downloading git binary...")
            download_file(git_url, git_binary_cache_path)
            git_binary_cache_path.chmod(0o755)

        # Copy the cached git binary to the bundle
        git_dest = output_dir / "agor_tools" / "git"
        shutil.copyfile(git_binary_cache_path, git_dest)
        git_dest.chmod(0o755)

        if not quiet_mode:
            print("📥 Added git binary to bundle")

    except Exception as e:
        if not quiet_mode:
            print(f"⚠️  Warning: Could not add git binary to bundle: {e}")
            print("   Bundle will still work if target system has git installed")

    # Download and add SQLite binary to bundle if requested (experimental)
    if sqlite_enabled:
        try:
            sqlite_url = config.get("sqlite_binary_url", settings.sqlite_binary_url)

            # Use cache directory for SQLite binary
            sqlite_cache_dir = Path(platformdirs.user_cache_dir("agor")) / "sqlite_binary"
            sqlite_cache_dir.mkdir(parents=True, exist_ok=True)
            sqlite_binary_cache_path = sqlite_cache_dir / "sqlite3"

            # Download the SQLite binary only if it doesn't exist in the cache
            if not sqlite_binary_cache_path.exists():
                if not quiet_mode:
                    print("📥 Downloading SQLite binary (experimental)...")
                download_file(sqlite_url, sqlite_binary_cache_path)
                sqlite_binary_cache_path.chmod(0o755)

            # Copy the cached SQLite binary to the bundle
            sqlite_dest = output_dir / "agor_tools" / "sqlite3"
            shutil.copyfile(sqlite_binary_cache_path, sqlite_dest)
            sqlite_dest.chmod(0o755)

            if not quiet_mode:
                print("📥 Added SQLite binary to bundle (experimental)")

        except Exception as e:
            if not quiet_mode:
                print(f"⚠️  Warning: Could not add SQLite binary to bundle: {e}")
                print("   Bundle will still work without SQLite database features")

    # Create archive with the specified format
    archive_extension = ARCHIVE_EXTENSIONS[compression_format]
    archive_path = Path(
        tempfile.NamedTemporaryFile(delete=False, suffix=archive_extension).name
    )

    if not quiet_mode:
        print(f"📦 Creating {compression_format.upper()} archive...")

    try:
        create_archive(output_dir, archive_path, compression_format)
    except Exception as e:
        print(f"❌ Failed to create archive: {e}")
        raise typer.Exit(1) from e

    # Determine where to save the bundled file
    final_filename = f"{short_name}{archive_extension}"

    if is_termux():
        # For Termux, always use the Downloads directory for easier access
        downloads_dir = get_downloads_dir()
        destination = Path(downloads_dir) / final_filename
        if not quiet_mode:
            print(f"📱 Running in Termux, saving to Downloads: {destination}")
    else:
        # For other platforms, ask the user where to save
        if is_interactive and not auto_yes:
            # Ask if they want to save to current directory
            save_to_current = typer.confirm(
                "Save the bundled file to the current directory?", default=True
            )

            if not save_to_current:
                # Ask if they want to save to Downloads directory
                save_to_downloads = typer.confirm(
                    "Save the bundled file to your Downloads directory?", default=True
                )

                if save_to_downloads:
                    downloads_dir = get_downloads_dir()
                    destination = Path(downloads_dir) / final_filename
                    if not quiet_mode:
                        print(f"💾 Saving to Downloads: {destination}")
                else:
                    # Use current directory as fallback
                    destination = Path.cwd() / final_filename
                    if not quiet_mode:
                        print(f"💾 Saving to current directory: {destination}")
            else:
                # Use current directory
                destination = Path.cwd() / final_filename
        else:
            # In non-interactive mode, use current directory
            destination = Path.cwd() / final_filename

    # Move the archive to the final destination
    shutil.move(str(archive_path), str(destination))

    # Success message and prompt
    if not quiet_mode:
        print(f"\n{SUCCESS_MESSAGES['bundle_created']}")
        print(f"📁 Location: {destination}")
        print(f"📦 Format: {compression_format.upper()}")
        print(f"📏 Size: {destination.stat().st_size / 1024 / 1024:.1f} MB")

        print("\n" + "=" * 60)
        print("🤖 AI ASSISTANT PROMPT")
        print("=" * 60)

    ai_prompt = (
        f"Extract the {compression_format.upper()} archive I've uploaded, "
        "read agor_tools/README_ai.md completely, "
        "and execute the AgentOrchestrator initialization protocol. "
        "You are now running AgentOrchestrator (AGOR), a multi-agent development coordination platform."
    )

    if not quiet_mode:
        print(ai_prompt)
        print("=" * 60)

    # Handle clipboard and file revelation
    if is_interactive:
        # Default to copying based on configuration
        should_copy = config.get("clipboard_copy_default", True)

        if not auto_yes and not should_copy:
            should_copy = typer.confirm("Copy the AI prompt to clipboard?")

        if should_copy or auto_yes:
            success, message = copy_to_clipboard(ai_prompt)
            if not quiet_mode:
                print(f"\n{message}")

        # Offer to reveal file in system explorer
        if not auto_yes:
            reveal = typer.confirm("Open file location?")
            if reveal:
                if reveal_file_in_explorer(destination):
                    if not quiet_mode:
                        print("📂 File location opened!")
                else:
                    if not quiet_mode:
                        print("⚠️  Could not open file location")

    if quiet_mode:
        # In quiet mode, just print the essential info
        print(f"{destination}")
    else:
        print(
            f"\n✅ Bundle creation complete! Upload {destination} to your AI assistant."
        )


@app.command()
def custom_instructions(
    copy: bool = typer.Option(
        True,
        "--copy/--no-copy",
        help="Copy custom instructions to clipboard",
    )
):
    """Generate custom instructions for AI assistants"""

    instructions = dedent(
        """
        You are AgentOrchestrator (AGOR), a sophisticated AI assistant specializing in
        multi-agent development coordination, project planning, and complex codebase management.
        You coordinate teams of AI agents to execute large-scale development projects.

        You have been provided with:
        - a statically compiled `git` binary (in /tmp/agor_tools/git)
        - the user's git repo (in the `/tmp/project` folder)
        - advanced coordination tools and prompt templates

        Before proceeding:
        - **Always use the git binary provided in this folder for git operations**
        - Configure `git` to make commits (use `git config` to set a name and
          email of AgentOrchestrator and agor@example.local)

        When working with the user, always:
        - Use `git ls-files` to get the layout of the codebase at the start
        - Use `git grep` when trying to find files in the codebase.
        - Once you've found likely files, display them in their entirety.
        - Make edits by targeting line ranges and rewriting the lines that differ.
        - Always work proactively and autonomously. Do not ask for input from the user
          unless you have fulfilled the user's request.
        - Keep your code cells short, 1-2 lines of code so that you can see
          where errors are. Do not write large chunks of code in one go.
        - Always be persistent and creative. When in doubt, ask yourself 'how would a
          proactive 10x engineer do this?', then do that.
        - Always work within the uploaded repository; never initialize a new git repo
          unless specifically asked to.
        - Verify that your changes worked as intended by running `git diff`.
        - Show a summary of the `git diff` output to the user and ask for
          confirmation before committing.
        - When analyzing the codebase, always work as far as possible without
          asking the user for input. Give a brief summary of your status and
          progress between each step, but do not go into detail until finished.

        You are now a project planning and multi-agent coordination specialist. Your primary
        functions include:

        - Analyzing codebases and planning implementation strategies
        - Designing multi-agent team structures for complex development projects
        - Creating specialized prompts for different types of coding agents
        - Coordinating workflows and handoff procedures between agents
        - Planning quality assurance and validation processes

        When displaying results, choose the appropriate format:
        - Full files: Complete files with all formatting preserved for copy/paste
        - Changes only: Show just the modified sections with context
        - Detailed analysis: Comprehensive explanation in a single codeblock for handoff
        - Agent prompts: Specialized prompts for coordinating multiple AI agents
        - Project plans: Strategic breakdowns and coordination workflows

        Show the comprehensive hotkey menu at the end of your replies with categories:
        📊 Analysis & Display, 🎯 Strategic Planning, 👥 Agent Team Management,
        📝 Prompt Engineering, 🔄 Coordination, and ⚙️ System commands.
        """
    )

    print("🤖 AGOR Custom Instructions for AI Assistants")
    print("=" * 60)
    print(instructions)

    if copy:
        success, message = copy_to_clipboard(instructions)
        print(f"\n{message}")


def cli():
    """Main CLI entry point"""
    if len(sys.argv) == 1:
        # Show help if no arguments provided
        sys.argv.append("--help")

    try:
        app()
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    cli()
