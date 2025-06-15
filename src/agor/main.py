import os
import re
import shutil
import subprocess
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
from .strategy import StrategyManager
from .utils import create_archive, download_file, move_directory
from .validation import validate_compression_format

app = typer.Typer(
    add_completion=False,
    help="🎼 AgentOrchestrator (AGOR) - Multi-Agent Development Coordination Platform",
    epilog="For more information, visit: https://github.com/jeremiah-k/agor",
)


@app.command()
def init(
    task: str = typer.Argument(help="Task description for the strategy"),
    agents: int = typer.Option(3, "--agents", "-a", help="Number of agents (2-6)"),
):
    """[AGENT] Initialize .agor/ directory and coordination files"""
    strategy_manager = StrategyManager()
    strategy_manager.init_coordination(task, agents)


@app.command()
def pd(
    task: str = typer.Argument(help="Task description for parallel divergent strategy"),
    agents: int = typer.Option(3, "--agents", "-a", help="Number of agents (2-6)"),
):
    """[AGENT] Set up Parallel Divergent strategy (multiple independent agents)"""
    strategy_manager = StrategyManager()
    strategy_manager.setup_parallel_divergent(task, agents)


@app.command()
def status():
    """[AGENT] Check all agent memory files and communication log"""
    strategy_manager = StrategyManager()
    strategy_manager.show_status()


@app.command()
def sync():
    """[AGENT] Pull latest changes and update coordination status"""
    strategy_manager = StrategyManager()
    strategy_manager.sync_state()


@app.command()
def ss(
    complexity: str = typer.Option(
        "medium", help="Project complexity: simple, medium, complex"
    ),
    team_size: int = typer.Option(3, help="Preferred team size"),
):
    """[AGENT] Analyze project and recommend optimal development strategy"""
    strategy_manager = StrategyManager()
    strategy_manager.suggest_strategy(complexity, team_size)


@app.command()
def agent_status(
    agent_id: str = typer.Argument(help="Agent ID (e.g., agent1)"),
    status: str = typer.Argument(help="Status: pending, in-progress, completed"),
):
    """[AGENT] Update agent status in coordination system"""
    strategy_manager = StrategyManager()
    strategy_manager.update_agent_status(agent_id, status)


def config_cmd(
    show: bool = typer.Option(False, "--show", help="Show current configuration"),
    set_key: Optional[str] = typer.Option(
        None, "--set", help="Set configuration key (format: key=value)"
    ),
    reset: bool = typer.Option(
        False, "--reset", help="Reset configuration to defaults"
    ),
):
    """
    Manages AGOR configuration settings via the CLI.

    Supports resetting to defaults, setting configuration keys with flexible input formats, and displaying current configuration and environment variables. Boolean and integer values are parsed automatically based on the key.
    """

    if reset:
        config.reset()
        print("🔄 Configuration reset to defaults!")
        return

    if set_key:
        try:
            # Support flexible formats: key=value, key value, or just key (for booleans)
            if "=" in set_key:
                key, value = set_key.split("=", 1)
            elif " " in set_key:
                parts = set_key.split(" ", 1)
                key, value = parts[0], parts[1] if len(parts) > 1 else "true"
            else:
                # Just key provided - assume boolean true
                key = set_key
                value = "true"

            # Convert string values to appropriate types
            if key in [
                "quiet",
                "preserve_history",
                "main_only",
                "interactive",
                "assume_yes",
                "clipboard_copy_default",
            ]:
                # Support flexible boolean values
                value = value.lower() in ("true", "1", "yes", "on", "t", "y")
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
):
    """
    [CLI] Bundle a git repository into an archive for AI assistant upload.

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

    # Create archive with the specified format
    archive_extension = ARCHIVE_EXTENSIONS[compression_format]
    archive_path = Path(
        tempfile.NamedTemporaryFile(delete=False, suffix=archive_extension).name
    )

    if not quiet_mode:
        print(f"📦 Creating {compression_format.upper()} archive...")

    try:
        create_archive(output_dir, archive_path, compression_format)

        # Verify archive contents for debugging
        if not quiet_mode:
            from .utils import verify_archive_contents

            verify_archive_contents(archive_path)

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
    """[AGENT] Generate custom instructions for AI assistants"""

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
        - Coordinating workflows and snapshot procedures between agents
        - Planning quality assurance and validation processes

        When displaying results, choose the appropriate format:
        - Full files: Complete files with all formatting preserved for copy/paste
        - Changes only: Show just the modified sections with context
        - Detailed analysis: Comprehensive explanation in a single codeblock for snapshot (replaces detailed snapshot)
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


@app.command()
def git_config(
    import_env: bool = typer.Option(
        False,
        "--import-env",
        help="Import git configuration from environment variables",
    ),
    name: Optional[str] = typer.Option(
        None, "--name", help="Set git user.name (overrides environment)"
    ),
    email: Optional[str] = typer.Option(
        None, "--email", help="Set git user.email (overrides environment)"
    ),
    global_config: bool = typer.Option(
        False,
        "--global",
        help="Set configuration globally instead of for current repository",
    ),
    show: bool = typer.Option(False, "--show", help="Show current git configuration"),
):
    """[CLI] Configure git user settings for AGOR development"""

    if show:
        print("🔍 Current Git Configuration:")
        try:
            current_name = subprocess.check_output(
                ["git", "config", "user.name"], stderr=subprocess.DEVNULL, text=True
            ).strip()
            current_email = subprocess.check_output(
                ["git", "config", "user.email"], stderr=subprocess.DEVNULL, text=True
            ).strip()
            print(f"   Name: {current_name}")
            print(f"   Email: {current_email}")
        except subprocess.CalledProcessError:
            print("   No git configuration found")

        # Show environment variables if available
        env_name = os.getenv("GIT_AUTHOR_NAME") or os.getenv("GIT_USER_NAME")
        env_email = os.getenv("GIT_AUTHOR_EMAIL") or os.getenv("GIT_USER_EMAIL")

        if env_name or env_email:
            print("\n🌍 Environment Variables:")
            if env_name:
                print(f"   GIT_AUTHOR_NAME/GIT_USER_NAME: {env_name}")
            if env_email:
                print(f"   GIT_AUTHOR_EMAIL/GIT_USER_EMAIL: {env_email}")

        return

    # Determine configuration values
    config_name = name
    config_email = email

    if import_env:
        # Import from environment variables
        env_name = os.getenv("GIT_AUTHOR_NAME") or os.getenv("GIT_USER_NAME")
        env_email = os.getenv("GIT_AUTHOR_EMAIL") or os.getenv("GIT_USER_EMAIL")

        if env_name and not config_name:
            config_name = env_name
        if env_email and not config_email:
            config_email = env_email

        if not env_name and not env_email:
            print("⚠️  No git environment variables found.")
            print(
                "   Set GIT_AUTHOR_NAME/GIT_USER_NAME and GIT_AUTHOR_EMAIL/GIT_USER_EMAIL"
            )
            print("   Or use --name and --email options")
            return

    if not config_name and not config_email:
        print("❌ No configuration provided.")
        print("   Use --import-env to import from environment")
        print("   Or use --name and --email to set manually")
        print("   Use --show to see current configuration")
        return

    # Apply git configuration
    print("🔧 Setting up git configuration...")

    config_scope = ["--global"] if global_config else []

    try:
        if config_name:
            subprocess.run(
                ["git", "config"] + config_scope + ["user.name", config_name],
                check=True,
            )
            print(f"✅ Set user.name: {config_name}")

        if config_email:
            subprocess.run(
                ["git", "config"] + config_scope + ["user.email", config_email],
                check=True,
            )
            print(f"✅ Set user.email: {config_email}")

        # Show repository info if in a git repo
        try:
            repo_root = subprocess.check_output(
                ["git", "rev-parse", "--show-toplevel"],
                stderr=subprocess.DEVNULL,
                text=True,
            ).strip()
            repo_name = os.path.basename(repo_root)
            current_branch = subprocess.check_output(
                ["git", "branch", "--show-current"],
                stderr=subprocess.DEVNULL,
                text=True,
            ).strip()

            print(f"\n📁 Repository: {repo_name}")
            print(f"🌿 Current branch: {current_branch}")

            if current_branch == "main":
                print("💡 Ready to create feature branch when needed")

        except subprocess.CalledProcessError:
            scope_text = "globally" if global_config else "for current repository"
            print(f"\nℹ️  Configuration applied {scope_text}")

        print("\n🚀 Git configuration complete!")

    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to set git configuration: {e}")
        return


@app.command()
def version():
    """[CLI] Show version information and check for updates"""
    from .version_check import display_version_info

    display_version_info(check_updates=True)


@app.command(name="generate-agor-feedback")
def generate_agor_feedback(
    copy: bool = typer.Option(
        True, "--copy/--no-copy", help="Copy feedback to clipboard"
    ),
    commit: bool = typer.Option(
        False, "--commit", help="Attempt to commit feedback directly to repository"
    ),
):
    """
    Generates a detailed AGOR feedback and improvement suggestions template, including system and repository information.

    If inside a git repository and `commit` is enabled, writes the feedback to `agor_feedback.md` and commits it. Otherwise, prints the feedback form for manual copy/paste and optionally copies it to the clipboard.
    """
    import platform
    import subprocess
    from datetime import datetime
    from pathlib import Path

    from .constants import PROTOCOL_VERSION
    from .platform import copy_to_clipboard

    print("📝 Generating AGOR Feedback and Improvement Suggestions...")

    # Get current time with NTP if possible
    try:
        import httpx

        with httpx.Client(timeout=5.0) as client:
            response = client.get("http://worldtimeapi.org/api/timezone/UTC")
            response.raise_for_status()
            time_data = response.json()
            current_time = time_data["datetime"][:19].replace("T", " ") + " UTC"
    except Exception:
        current_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    # Collect system information
    system_info = {
        "agor_version": __version__,
        "protocol_version": PROTOCOL_VERSION,
        "platform": platform.system(),
        "python_version": platform.python_version(),
        "timestamp": current_time,
    }

    # Try to get git repository information
    repo_info = {}
    try:
        repo_root = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        repo_name = Path(repo_root).name
        current_branch = subprocess.check_output(
            ["git", "branch", "--show-current"], stderr=subprocess.DEVNULL, text=True
        ).strip()

        repo_info = {
            "repository_name": repo_name,
            "current_branch": current_branch,
            "repository_root": repo_root,
        }
    except subprocess.CalledProcessError:
        repo_info = {"note": "Not in a git repository"}

    # Generate feedback content
    feedback_content = f"""# AGOR Feedback and Improvement Suggestions

**Generated**: {current_time}
**AGOR Version**: {system_info['agor_version']}
**Protocol Version**: {system_info['protocol_version']}
**Platform**: {system_info['platform']} (Python {system_info['python_version']})
**Repository**: {repo_info.get('repository_name', 'Unknown')}
**Branch**: {repo_info.get('current_branch', 'Unknown')}

## 🎯 Usage Experience

### What worked well:
- [ ] Strategy selection and setup
- [ ] Bundle creation and extraction
- [ ] Agent coordination protocols
- [ ] Documentation clarity
- [ ] CLI interface usability
- [ ] Multi-agent workflow

### What could be improved:
- [ ] Performance issues
- [ ] Documentation gaps
- [ ] CLI command confusion
- [ ] Strategy effectiveness
- [ ] Error handling
- [ ] Setup complexity

## 🐛 Issues Encountered

### Technical Issues:
- [ ] Installation problems
- [ ] Dependency conflicts
- [ ] Platform compatibility
- [ ] Git integration issues
- [ ] Archive/bundle problems

### Workflow Issues:
- [ ] Agent coordination confusion
- [ ] Strategy selection difficulty
- [ ] Snapshot process unclear
- [ ] Status tracking problems
- [ ] Communication breakdowns

## 💡 Feature Requests

### High Priority:
- [ ] Better error messages
- [ ] Improved documentation
- [ ] Simplified setup process
- [ ] Enhanced CLI help
- [ ] Better agent status tracking

### Medium Priority:
- [ ] Additional strategies
- [ ] Better integration with IDEs
- [ ] Improved bundle formats
- [ ] Enhanced git workflows
- [ ] Better progress indicators

### Low Priority:
- [ ] GUI interface
- [ ] Web dashboard
- [ ] Mobile support
- [ ] Cloud integration
- [ ] Advanced analytics

## 🔧 Specific Improvements

### Documentation:
- [ ] More examples needed
- [ ] Better getting started guide
- [ ] Video tutorials
- [ ] FAQ section
- [ ] Troubleshooting guide

### CLI Interface:
- [ ] Better command names
- [ ] More intuitive options
- [ ] Better help text
- [ ] Command aliases
- [ ] Auto-completion

### Agent Coordination:
- [ ] Clearer snapshot process
- [ ] Better status visibility
- [ ] Improved communication templates
- [ ] Enhanced strategy protocols
- [ ] Better conflict resolution

## 📊 Performance Feedback

### Speed:
- Bundle creation: ⭐⭐⭐⭐⭐ (1=slow, 5=fast)
- Strategy setup: ⭐⭐⭐⭐⭐
- Agent coordination: ⭐⭐⭐⭐⭐
- Documentation loading: ⭐⭐⭐⭐⭐

### Reliability:
- Git operations: ⭐⭐⭐⭐⭐ (1=unreliable, 5=rock solid)
- Archive creation: ⭐⭐⭐⭐⭐
- Cross-platform: ⭐⭐⭐⭐⭐
- Error handling: ⭐⭐⭐⭐⭐

## 🎨 User Experience

### Ease of Use:
- First-time setup: ⭐⭐⭐⭐⭐ (1=confusing, 5=intuitive)
- Daily usage: ⭐⭐⭐⭐⭐
- Learning curve: ⭐⭐⭐⭐⭐
- Documentation quality: ⭐⭐⭐⭐⭐

## 💬 Additional Comments

```
[Please add any additional feedback, suggestions, or comments here]




```

## 🔗 Contact Information

**How to submit this feedback:**
1. **GitHub Issues**: https://github.com/jeremiah-k/agor/issues
2. **Discussions**: https://github.com/jeremiah-k/agor/discussions
3. **Email**: jeremiahk@gmx.com

**Thank you for helping improve AGOR!** 🙏

---
*This feedback was generated automatically by AGOR v{system_info['agor_version']} (Protocol v{system_info['protocol_version']})*
"""

    # Determine output method
    if commit and repo_info.get("repository_root"):
        # Try to commit directly to repository
        try:
            feedback_file = Path(repo_info["repository_root"]) / "agor_feedback.md"
            feedback_file.write_text(feedback_content)

            # Add and commit the file
            subprocess.run(["git", "add", str(feedback_file)], check=True)
            subprocess.run(
                ["git", "commit", "-m", f"📝 Add AGOR feedback form ({current_time})"],
                check=True,
            )

            print(f"✅ Feedback committed to repository: {feedback_file}")
            print(f"📁 File: {feedback_file}")
            print("\n🚀 You can now edit the file and submit feedback via GitHub!")

        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to commit feedback: {e}")
            print("\n📋 Feedback content (copy and save manually):")
            print("=" * 60)
            print(feedback_content)
            print("=" * 60)
    else:
        # Output as codeblock for copy/paste
        print("\n📋 AGOR Feedback Form (ready for copy/paste):")
        print("=" * 60)
        print(feedback_content)
        print("=" * 60)

        # Copy to clipboard if requested
        if copy:
            success, message = copy_to_clipboard(feedback_content)
            print(f"\n{message}")

        print(
            "\n💡 Save this as 'agor_feedback.md' and submit via GitHub Issues or Discussions"
        )


@app.command()
def detick(
    content: Optional[str] = typer.Argument(
        None, help="Content to detick (uses clipboard if not provided)"
    ),
    show: bool = typer.Option(
        False,
        "--show",
        help="Show processed content instead of just updating clipboard",
    ),
):
    """
    Converts triple backticks to double backticks in the provided content or clipboard.

    If no content is given, reads from the clipboard, processes it, and updates the clipboard with the result. Optionally displays the processed content.
    """
    try:
        import pyperclip

        from .tools.dev_tools import detick_content

        # Get content from clipboard if not provided as argument
        if content is None:
            try:
                content = pyperclip.paste()
                if not content.strip():
                    print(
                        "❌ Clipboard is empty. Copy some content first or provide content as argument."
                    )
                    raise typer.Exit(1)
                print("📋 Processing clipboard content...")
            except Exception as e:
                print(f"❌ Could not access clipboard: {e}")
                print("💡 Provide content as argument: agor detick 'your content'")
                raise typer.Exit(1) from e

        # Process the content
        processed = detick_content(content)

        # Update clipboard with processed content
        pyperclip.copy(processed)

        # Show results
        original_backticks = content.count("```")
        processed_backticks = processed.count("``")

        if show:
            print("📝 Processed content:")
            print("-" * 40)
            print(processed)
            print("-" * 40)

        print(
            f"✅ Deticked content updated in clipboard ({original_backticks} ``` → {processed_backticks} ``)"
        )

    except ImportError:
        print("❌ pyperclip not available. Install with: pip install pyperclip")
        raise typer.Exit(1) from None
    except Exception as e:
        print(f"❌ Error processing content: {e}")
        raise typer.Exit(1) from e


@app.command()
def retick(
    content: Optional[str] = typer.Argument(
        None, help="Content to retick (uses clipboard if not provided)"
    ),
    show: bool = typer.Option(
        False,
        "--show",
        help="Show processed content instead of just updating clipboard",
    ),
):
    """
    Converts double backticks in the provided content or clipboard to triple backticks and updates the clipboard.

    If no content is given, reads from the clipboard, processes it, and writes the result back to the clipboard. Optionally displays the processed content.
    """
    try:
        import pyperclip

        from .tools.dev_tools import retick_content

        # Get content from clipboard if not provided as argument
        if content is None:
            try:
                content = pyperclip.paste()
                if not content.strip():
                    print(
                        "❌ Clipboard is empty. Copy some content first or provide content as argument."
                    )
                    raise typer.Exit(1)
                print("📋 Processing clipboard content...")
            except Exception as e:
                print(f"❌ Could not access clipboard: {e}")
                print("💡 Provide content as argument: agor retick 'your content'")
                raise typer.Exit(1) from e

        # Process the content
        processed = retick_content(content)

        # Update clipboard with processed content
        pyperclip.copy(processed)

        # Show results
        original_backticks = content.count("``")
        processed_backticks = processed.count("```")

        if show:
            print("📝 Processed content:")
            print("-" * 40)
            print(processed)
            print("-" * 40)

        print(
            f"✅ Reticked content updated in clipboard ({original_backticks} `` → {processed_backticks} ```)"
        )

    except ImportError:
        print("❌ pyperclip not available. Install with: pip install pyperclip")
        raise typer.Exit(1) from None
    except Exception as e:
        print(f"❌ Error processing content: {e}")
        raise typer.Exit(1) from e


def cli():
    """
    Entry point for the AGOR CLI application.

    Checks for version updates on certain commands, displays help if no arguments are provided, and runs the Typer CLI app. Handles keyboard interrupts and unexpected exceptions with user-friendly messages and exits with an error code.
    """
    # Check for version updates for important commands
    from .version_check import check_versions_if_needed

    if len(sys.argv) == 1:
        # Show help if no arguments provided
        sys.argv.append("--help")
        check_versions_if_needed()
    elif len(sys.argv) > 1:
        command = sys.argv[1]
        # Check versions for help, bundle, version commands - skip for config commands
        if command in ["--help", "-h", "bundle", "version", "--version", "-v"]:
            check_versions_if_needed()

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
