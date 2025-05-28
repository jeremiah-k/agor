# 🤖 AGOR Integration: Jules Direct Access Guide

This guide provides specific instructions for AI agents like "Jules by Google" that have direct file system access and can execute commands like `git` directly within a project repository. These agents operate in AGOR's "Standalone Mode."

## Core Principles for Jules

*   **Operating within Project:** You are assumed to be operating *within* an already cloned user project repository.
*   **No Bundles:** You do not operate from a pre-packaged `.zip` or `.tar.gz` bundle. Ignore instructions related to `/tmp/project/` or `/tmp/agor_tools/` as bundle-specific paths.
*   **Direct File I/O:** You can read and write files directly in the user's project directory.
*   **Direct Command Execution:** You can typically execute `git` and other shell commands directly.
*   **AGOR Protocol Files:** You need access to AGOR's core instruction files (`README_ai.md`, `AGOR_INSTRUCTIONS.md`) and potentially its Python utility scripts.

## Initialization and Setup

These steps assume you are already operating within the target project's repository. The main task is to access AGOR's instructional files and utility scripts.

**1. Locate or Obtain AGOR Tooling:**

The AGOR tooling includes essential instructional markdown files and Python utility scripts. Determine how these tools are accessible:

*   **Scenario A: Working on the AGOR Project Itself**
    *   If your task involves modifications to the AGOR framework, you are already in the AGOR repository.
    *   The tools are located in `src/agor/tools/`.
    *   Path to instructions: `src/agor/tools/README_ai.md` and `src/agor/tools/AGOR_INSTRUCTIONS.md`.
    *   Path to Python utilities: e.g., `src/agor/tools/code_exploration.py`.

*   **Scenario B: Working on a User Project with Embedded AGOR Tools**
    *   The user project may already include a copy of the necessary AGOR tools, often in a directory like `.agor_tools/` or `vendor/agor_tools/`.
    *   You will need to be provided with the path to this directory by the user or through context.
    *   Path to instructions: e.g., `.agor_tools/README_ai.md`.
    *   Path to Python utilities: e.g., `.agor_tools/code_exploration.py`.

*   **Scenario C: Working on a User Project, AGOR Tools Accessed Separately**
    *   If the user project does not embed AGOR tools, and they are not provided alongside, you may need to clone the AGOR repository to a known, stable temporary path. This path should persist for your session if you need to refer to the tools multiple times. This is solely for accessing AGOR's *protocol files and utilities*, not for working on the AGOR project itself.
    *   Example:
        ```bash
        git clone https://github.com/jeremiah-k/agor.git /tmp/agor_jules_tools_protocols
        ```
    *   Path to instructions: `/tmp/agor_jules_tools_protocols/src/agor/tools/README_ai.md`.
    *   Path to Python utilities: e.g., `/tmp/agor_jules_tools_protocols/src/agor/tools/code_exploration.py`.

**IMPORTANT:** Clarify with the user or through context which scenario applies to determine the correct paths for AGOR's instructional and utility files.

**2. Load AGOR Instructions:**

First, read and internalize `README_ai.md` from the determined path. This will guide you through role selection with the user.
```bash
# Adjust path based on Scenario A, B, or C from Step 1
cat path/to/agor/tools/README_ai.md
```
After role selection, read and internalize `AGOR_INSTRUCTIONS.md`. This is your primary operational guide.
```bash
# Adjust path based on Scenario A, B, or C from Step 1
cat path/to/agor/tools/AGOR_INSTRUCTIONS.md
```

**3. Git Configuration:**

Ensure your Git identity is configured in the project repository you are working on. `AGOR_INSTRUCTIONS.md` (Section 1.2) provides guidance. If the project has AGOR tools embedded that include `git_setup.py` (from `src/agor/tools/`), you can use that. Otherwise, direct `git config` commands may be needed if not already set up in your environment.

```bash
# Example using direct git commands if git_setup.py is not directly usable
# (Ensure these are appropriate for the user's project context)
git config user.name "Jules Agent (via AGOR Protocol)"
git config user.email "jules.agent.agor@example.com"
```

**4. Python Utility Scripts:**

When `AGOR_INSTRUCTIONS.md` refers to executing a Python script (e.g., for code exploration, strategy management, or dev tooling):
*   You will invoke it using `python path/to/agor/tools/script_name.py [arguments]`. The path is determined by Scenarios A, B, or C in Step 1.
*   Example using path from Scenario C:
    ```bash
    python /tmp/agor_jules_tools_protocols/src/agor/tools/code_exploration.py --pattern "my_function" .
    ```
*   Some scripts, like those in `src/agor/tools/dev_tooling.py`, might require adding their `src` directory to `sys.path` if you are importing them from a script that is *not* in their directory, or if they have relative imports. The AGOR Development Guide mentions:
    ```python
    # This setup is typically for developing AGOR itself.
    # If using AGOR tools in a separate project (Scenario C), adapt paths carefully.
    # import sys
    # sys.path.insert(0, 'path/to/agor_protocols_clone/src') # e.g., /tmp/agor_jules_tools_protocols/src
    # from agor.tools.dev_tooling import quick_commit_push
    ```
    For most direct access scenarios where you are *using* AGOR tools on a target project, direct execution of the scripts with full paths is more common than importing their functions into a separate ad-hoc script.

## Operational Guidelines

*   **File Paths:** When AGOR instructions refer to file paths (e.g., for editing, reading), these are direct paths within the project you are working on.
*   **Git Binary:** Unlike bundle mode, you do not use a `/tmp/agor_tools/git`. Use the `git` command available in your execution environment, operating on the current project repository.
*   **`.agor/` Directory:** All coordination files (e.g., `memory.md`, `agentconvo.md`, `snapshots/`) are created and managed directly within the `.agor/` directory of the project you are working on.
*   **Hotkey Interaction:** Present hotkey menus and interpret user selections as detailed in `AGOR_INSTRUCTIONS.md`.
*   **Memory System:** Interact with the memory system primarily through markdown files (`.agor/memory.md`, `agentN-memory.md`) and snapshot creation/loading hotkeys. The Memory Synchronization System will handle persistence in the background using Memory Branches.

## Example: Analyzing a File

If the user asks you to analyze `src/module.py` in their project:

1.  You'd use the `a` (analyze codebase) hotkey flow.
2.  To read the file: `read_files(["src/module.py"])` (or your agent's equivalent file reading tool).
3.  If using AGOR's Python-based analysis tools (assuming Scenario C for tool path):
    ```bash
    # This example assumes you'd run the script directly.
    python /tmp/agor_jules_tools_protocols/src/agor/tools/code_exploration.py --analyze src/module.py
    ```

By following these guidelines, you can effectively use AGOR's coordination capabilities while leveraging your direct access to the file system and development environment.
