import os
import re
import shutil
import sys
import tempfile
from pathlib import Path
from textwrap import dedent

import pyperclip
import typer
from plumbum import local

from .repo_mgmt import clone_git_repo_to_temp_dir, get_clone_url, valid_git_repo
from .utils import create_tarball, download_file, move_directory

app = typer.Typer(add_completion=False)


# Define option for branches outside the function to avoid B008 warning
branches_option = typer.Option(
    None,
    "--branches",
    help="Specify multiple branches to bundle (comma-separated list)",
)


@app.command()
def bundle(
    src_repo: str = typer.Argument(
        help="a local git repo or github url to agentgrunt-ify",
        callback=valid_git_repo,
    ),
    preserve_history: bool = typer.Option(
        False,
        "--preserve-history",
        "-p",
        help="Preserve the full git history (defaults to shallow clone to save space)",
    ),
    branch: str = typer.Option(
        None,
        "--branch",
        "-b",
        help="Specify a single branch to bundle (defaults to the current branch for local repos)",
    ),
    all_branches: bool = typer.Option(
        False,
        "--all-branches",
        "-a",
        help="Bundle all branches from the repository",
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

    By default, bundles only the current branch for local repos or the default branch for remote repos.
    Use --branch to specify a single branch, --branches for multiple specific branches,
    or --all-branches to include all branches in the repository.
    """
    # clone_url = get_clone_url(src_repo) -- Assigned to but never used
    repo_name = get_clone_url(src_repo).split("/")[-1]

    # Process branches parameter if provided
    branch_list = None
    if branches:
        branch_list = [b.strip() for b in branches]

    temp_repo = clone_git_repo_to_temp_dir(
        src_repo,
        shallow=not preserve_history,
        branch=branch,
        all_branches=all_branches,
        branches=branch_list,
    )
    print(  # "\033[92m" +
        f"Preparing to build '{repo_name}'..."
        # + "\033[0m"
    )

    output_dir = Path(tempfile.mkdtemp())
    output_dir.mkdir(parents=True, exist_ok=True)
    gpt_tools_dir = Path(__file__).parent / "gpt_tools"

    # use shutil to move the temp_repo dir into output_dir/user_code
    user_code_dir = output_dir / "uc"
    move_directory(temp_repo, user_code_dir)

    # copy all files in gpt_tools to output_dir
    shutil.copytree(gpt_tools_dir, output_dir / "tools_for_ai")

    # download the linux git binary, make it executable
    git_binary_url = "https://github.com/nikvdp/1bin/releases/download/v0.0.40/git"

    git_cache_dir = (
        Path(os.environ.get("XDG_CACHE_HOME", os.path.expanduser("~/.cache")))
        / "agentgrunt"
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
    destination = Path.cwd() / f"{short_name}.tar.gz"
    shutil.move(str(tarball), str(destination))

    final_msg = (
        dedent(
            f"""
            Wrote archive to: {destination}

            Please upload this file to ChatGPT, and paste the following message into the chat:
            """
        ).strip()
        + "\n"
    )

    gpt_prompt = (
        dedent(
            """
        Please extract the archive I've uploaded, read the contents of
        tools_for_ai/README_ai.md in its entirety, and follow the directions
        listed inside that file.
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
            # Try to copy using pyperclip first
            try:
                pyperclip.copy(gpt_prompt)
                print("Message copied to clipboard!")
            except Exception as e:
                print(f"Failed to copy with pyperclip: {e}")
                # Try platform-specific clipboard commands as fallbacks
                if shutil.which("pbcopy"):  # macOS
                    try:
                        pbcopy = local["pbcopy"]
                        (pbcopy << gpt_prompt)()
                        print("Message copied to clipboard using pbcopy!")
                    except Exception as e2:
                        print(f"Failed to copy with pbcopy: {e2}")
                elif shutil.which("xclip"):  # Linux with X11
                    try:
                        xclip = local["xclip"]
                        (xclip["-selection", "clipboard"] << gpt_prompt)()
                        print("Message copied to clipboard using xclip!")
                    except Exception as e2:
                        print(f"Failed to copy with xclip: {e2}")
                elif shutil.which("wl-copy"):  # Linux with Wayland
                    try:
                        wlcopy = local["wl-copy"]
                        (wlcopy << gpt_prompt)()
                        print("Message copied to clipboard using wl-copy!")
                    except Exception as e2:
                        print(f"Failed to copy with wl-copy: {e2}")
                else:
                    print(
                        "No clipboard command found. Please copy the message manually."
                    )
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
        You are AgentGrunt, a proactive and intelligent AI assistant specializing in
        exploring and editing large codebases and git repos. You have been provided with:

        - a statically compiled `git` binary (in /tmp/tools_for_ai/git)
        - the user's git repo (in the `/tmp/uc` folder)

        Before proceeding, please:
        - **Always use the git binary provided in this folder for git operations**
        - Configure `git` to make commits (use `git config` to set a name and
          email of AgentGrunt and grunt@agentgrunt.com)

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

        When the user is happy with your work, use the provided git binary's
        `format-patch` command to generate a patch file and send it to the user so they
        can apply your changes **as a commit** to their local copy. You must always use
        `format-patch` with `--stdout`.

        Show a hotkey menu at the end of your replies:
        - a ) analyze codebase
        - c ) continue
        - d ) download changes as patch
        - dr) download entire repo
        - m ) show diff of last change
        - r ) refresh/reload agentgrunt
        - w ) work autonomously until complete
        - ? ) show this hotkey list
        """
    )

    print(instructions)

    if copy:
        # Try to copy using pyperclip first
        try:
            pyperclip.copy(instructions)
            print("Instructions copied to clipboard!")
        except Exception as e:
            print(f"Failed to copy with pyperclip: {e}")
            # Try platform-specific clipboard commands as fallbacks
            if shutil.which("pbcopy"):  # macOS
                try:
                    pbcopy = local["pbcopy"]
                    (pbcopy << instructions)()
                    print("Instructions copied to clipboard using pbcopy!")
                except Exception as e2:
                    print(f"Failed to copy with pbcopy: {e2}")
            elif shutil.which("xclip"):  # Linux with X11
                try:
                    xclip = local["xclip"]
                    (xclip["-selection", "clipboard"] << instructions)()
                    print("Instructions copied to clipboard using xclip!")
                except Exception as e2:
                    print(f"Failed to copy with xclip: {e2}")
            elif shutil.which("wl-copy"):  # Linux with Wayland
                try:
                    wlcopy = local["wl-copy"]
                    (wlcopy << instructions)()
                    print("Instructions copied to clipboard using wl-copy!")
                except Exception as e2:
                    print(f"Failed to copy with wl-copy: {e2}")
            else:
                print(
                    "No clipboard command found. Please copy the instructions manually."
                )


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
