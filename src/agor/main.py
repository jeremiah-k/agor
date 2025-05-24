import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from textwrap import dedent

import platformdirs
import pyperclip
import typer
from plumbum import local

from .repo_mgmt import clone_git_repo_to_temp_dir, get_clone_url, valid_git_repo
from .utils import create_tarball, download_file, move_directory


def is_termux():
    """Check if running in Termux environment"""
    return "com.termux" in os.environ.get("HOME", "")


def get_downloads_dir():
    """Get the Downloads directory path based on the platform"""
    if is_termux():
        # For Termux, use ~/storage/downloads
        storage_downloads = os.path.expanduser("~/storage/downloads")
        if os.path.exists(storage_downloads):
            return storage_downloads

    # For other environments, use platformdirs to get the standard downloads directory
    try:
        downloads_dir = platformdirs.user_downloads_dir()
        if os.path.exists(downloads_dir):
            return downloads_dir
    except Exception:
        pass

    # Fallback to standard Downloads directories
    home_dir = os.path.expanduser("~")
    downloads_dir = os.path.join(home_dir, "Downloads")
    if os.path.exists(downloads_dir):
        return downloads_dir

    downloads_dir = os.path.join(home_dir, "Download")
    if os.path.exists(downloads_dir):
        return downloads_dir

    # Fallback to current directory
    return os.getcwd()


def copy_to_clipboard(text):
    """Copy text to clipboard with platform-specific handling"""
    # First try pyperclip as it works on many platforms
    try:
        pyperclip.copy(text)
        return True, "Message copied to clipboard!"
    except Exception:
        # If pyperclip fails, try platform-specific methods
        if is_termux():
            # Termux environment
            try:
                subprocess.run(
                    ["termux-clipboard-set"],
                    input=text.encode("utf-8"),
                    check=True,
                )
                return True, "Message copied to clipboard using termux-api!"
            except Exception as e2:
                return (
                    False,
                    f"Failed to copy with termux-api: {e2}. Install termux-api package with 'pkg install termux-api'.",
                )
        else:
            # Other platforms
            system = platform.system()
            try:
                if system == "Darwin":  # macOS
                    subprocess.run("pbcopy", text=True, input=text, check=True)
                    return True, "Message copied to clipboard using pbcopy!"
                elif system == "Linux":  # Linux
                    if shutil.which("xclip"):
                        subprocess.run(
                            ["xclip", "-selection", "clipboard"],
                            input=text.encode("utf-8"),
                            check=True,
                        )
                        return True, "Message copied to clipboard using xclip!"
                    elif shutil.which("xsel"):
                        subprocess.run(
                            ["xsel", "--clipboard", "--input"],
                            input=text.encode("utf-8"),
                            check=True,
                        )
                        return True, "Message copied to clipboard using xsel!"
                    elif shutil.which("wl-copy"):  # Wayland
                        subprocess.run(
                            ["wl-copy"],
                            input=text.encode("utf-8"),
                            check=True,
                        )
                        return True, "Message copied to clipboard using wl-copy!"
                    else:
                        return (
                            False,
                            "No clipboard command found. On Linux, install xclip, xsel, or wl-clipboard.",
                        )
                else:
                    return False, f"Clipboard functionality not supported on {system}."
            except Exception as e2:
                return False, f"Failed to copy to clipboard: {e2}"


app = typer.Typer(add_completion=False)


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
        help="a local git repo or github url to bundle",
        callback=valid_git_repo,
    ),
    preserve_history: bool = typer.Option(
        False,
        "--preserve-history",
        "-p",
        help="Preserve the full git history (defaults to shallow clone to save space)",
    ),
    main_only: bool = typer.Option(
        False,
        "--main-only",
        "-m",
        help="Bundle only main/master branch",
    ),
    branches: list[str] = branches_option,
    interactive: bool = typer.Option(
        True, "--no-interactive", help="don't ask questions (batch) mode"
    ),
    assume_yes: bool = typer.Option(
        False, "--assume-yes", "-y", help="assume yes for all prompts"
    ),
):
    """Bundle up a local or remote git repo.

    By default, bundles ALL branches from the repository.
    Use -m/--main-only to bundle only main/master branch.
    Use -b/--branches to bundle main/master plus specified additional branches.
    """
    # clone_url = get_clone_url(src_repo) -- Assigned to but never used
    repo_name = get_clone_url(src_repo).split("/")[-1]

    # Process branches parameter if provided
    branch_list = None
    if branches:
        branch_list = [b.strip() for b in branches]

    # Determine which branches to clone based on new simplified logic
    if main_only:
        print("Bundling only main/master branch")
        temp_repo = clone_git_repo_to_temp_dir(
            src_repo, shallow=not preserve_history, main_only=True
        )
    elif branch_list:
        print(f"Bundling main/master plus additional branches: {branch_list}")
        temp_repo = clone_git_repo_to_temp_dir(
            src_repo, shallow=not preserve_history, branches=branch_list
        )
    else:
        print("Bundling all branches from the repository (default)")
        temp_repo = clone_git_repo_to_temp_dir(
            src_repo, shallow=not preserve_history, all_branches=True
        )
    print(  # "\033[92m" +
        f"Preparing to build '{repo_name}'..."
        # + "\033[0m"
    )

    output_dir = Path(tempfile.mkdtemp())
    output_dir.mkdir(parents=True, exist_ok=True)
    tools_dir = Path(__file__).parent / "tools"

    # use shutil to move the temp_repo dir into output_dir/project
    project_dir = output_dir / "project"
    move_directory(temp_repo, project_dir)

    # copy all files in tools to output_dir
    shutil.copytree(tools_dir, output_dir / "tools_for_ai")

    # download the linux git binary, make it executable
    git_binary_url = "https://github.com/nikvdp/1bin/releases/download/v0.0.40/git"

    git_cache_dir = (
        Path(os.environ.get("XDG_CACHE_HOME", os.path.expanduser("~/.cache")))
        / "agor"
        / "git_binary"
    )
    git_cache_dir.mkdir(parents=True, exist_ok=True)
    git_binary_dest_path = git_cache_dir / "git"

    # Download the git binary only if it doesn't exist in the cache
    if not git_binary_dest_path.exists():
        download_file(git_binary_url, git_binary_dest_path)
        git_binary_dest_path.chmod(0o755)

    shutil.copyfile(git_binary_dest_path, output_dir / "tools_for_ai" / "git")

    # create a tarball of output_dir, and once it's written move it to the
    # current PWD, and tell the user about it
    tarball_path = Path(
        tempfile.NamedTemporaryFile(delete=False, suffix=".tar.gz").name
    )
    tarball = create_tarball(output_dir, tarball_path)
    short_name = re.sub(r"\.git$", "", repo_name)

    # Determine where to save the bundled file
    if is_termux():
        # For Termux, always use the Downloads directory for easier access
        downloads_dir = get_downloads_dir()
        destination = Path(downloads_dir) / f"{short_name}.tar.gz"
        print(f"Running in Termux, saving to Downloads: {destination}")
    else:
        # For other platforms, ask the user where to save
        if interactive and not assume_yes:
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
                    destination = Path(downloads_dir) / f"{short_name}.tar.gz"
                    print(f"Saving to Downloads: {destination}")
                else:
                    # Use current directory as fallback
                    destination = Path.cwd() / f"{short_name}.tar.gz"
                    print(f"Saving to current directory: {destination}")
            else:
                # Use current directory
                destination = Path.cwd() / f"{short_name}.tar.gz"
        else:
            # In non-interactive mode, use current directory
            destination = Path.cwd() / f"{short_name}.tar.gz"

    shutil.move(str(tarball), str(destination))

    final_msg = (
        dedent(
            f"""
            🎼 AgentOrchestrator (AGOR) Bundle Created: {destination}

            This bundle contains your project plus AgentOrchestrator's multi-agent coordination platform.

            BUNDLE MODE: Upload this file to any AI platform and use the prompt below.
            STANDALONE MODE: AI agents can also clone https://github.com/jeremiah-k/agor.git directly.

            Please upload this file to your AI assistant and paste the following message:
            """
        ).strip()
        + "\n"
    )

    gpt_prompt = (
        dedent(
            """
        Please extract the archive I've uploaded, read the contents of
        tools_for_ai/README_ai.md in its entirety, and follow the AgentOrchestrator
        initialization protocol listed inside that file. You are now AgentOrchestrator (AGOR),
        a multi-agent development coordination platform.
        """
        )
        .strip()
        .replace("\n", " ")
    )

    print(final_msg)
    print(f"---\n{gpt_prompt}\n---")

    if interactive:
        # prompt user if they want to copy it and reveal the file, then do it if they say yes
        copy = (
            True if assume_yes else typer.confirm("Copy the message to your clipboard?")
        )
        if copy:
            success, message = copy_to_clipboard(gpt_prompt)
            print(message)
        # Only show the Finder prompt on macOS
        if sys.platform == "darwin":
            open_finder = (
                True if assume_yes else typer.confirm("Reveal the file in Finder?")
            )
            if open_finder:
                local["open"]("-R", destination)


@app.command()
def custom_instructions(
    copy: bool = typer.Option(
        True,
        "--copy/--no-copy",
        help="Copy custom instructions to clipboard (macOS only)",
    )
):
    """Copy ChatGPT custom instructions to the clipboard"""

    instructions = dedent(
        """
        You are AgentOrchestrator (AGOR), a sophisticated AI assistant specializing in
        multi-agent development coordination, project planning, and complex codebase management.
        You coordinate teams of AI agents to execute large-scale development projects.

        You have been provided with:
        - a statically compiled `git` binary (in /tmp/tools_for_ai/git)
        - the user's git repo (in the `/tmp/project` folder)
        - advanced coordination tools and prompt templates

        Before proceeding, please:
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

    print(instructions)

    if copy:
        success, message = copy_to_clipboard(instructions)
        print(message)


def cli():
    import sys

    if len(sys.argv) == 1:
        # show help even if user didn't pass --help
        sys.argv += ["--help"]
        app()
    else:
        app()


if __name__ == "__main__":
    cli()
